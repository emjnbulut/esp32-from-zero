"""Episode 14 props for the Pin by Pin Lab Blender kit (additive; pbl.py stays untouched). DRAFT 2026-11-25.

    import pbl, parts_ep14 as p14
    b = p14.banana(k, at, yaw_deg=20)    # {"group", "wire_point" (mm, where the jumper goes in), "top" (tag point)}
    a = p14.apple(k, at)
    o = p14.orange(k, at)
    g = p14.touch_glow(k, centre, "#ffd166")   # g(level): soft glow shell around a touched fruit (0 = invisible)

Stylized like the kit parts (clean shapes, a little procedural colour variation, no image textures). All sizes in mm
under the kit root; the fruit are desk-miniature scale next to the breadboard (banana ~95 mm long, apple/orange ~44 mm).
"""
import math

import bmesh
import bpy
from mathutils import Vector

from pbl import lin


def _fruit_mat(name, c0, c1, rough=0.45, scale=6.0, coat=0.25, dimples=0.0):
    """Principled skin with a noise colour blend c0 -> c1; dimples > 0 adds a fine bump (orange peel)."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = 3.0
    nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[0].color = (*lin(c0), 1)
    ramp.color_ramp.elements[1].color = (*lin(c1), 1)
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    if dimples > 0:
        vor = nt.nodes.new("ShaderNodeTexVoronoi")
        vor.inputs["Scale"].default_value = 260.0
        nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
        bump = nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = dimples
        nt.links.new(vor.outputs["Distance"], bump.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def _uv_sphere(r, segs=48, rings=32):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=r)
    return bm


def _subsurf(ob, levels=2):
    mod = ob.modifiers.new("subsurf", "SUBSURF")
    mod.levels = mod.render_levels = levels
    return ob


def _smooth(ob):
    if hasattr(ob.data, "shade_smooth"):
        ob.data.shade_smooth()
    return ob


def apple(k, at, r=22.0, name="apple"):
    at = Vector(at)
    g = k.empty(name, at)
    bm = _uv_sphere(r)
    for v in bm.verts:                       # apple profile: wider shoulders, dimple top + bottom, slightly flat
        x, y, z = v.co
        t = z / r                            # -1 .. 1
        s = 1.0 + 0.10 * (1 - t * t) + 0.06 * t
        v.co.x, v.co.y = x * s, y * s
        rho = math.hypot(x, y) / r
        v.co.z = z * 0.88 - 0.22 * r * math.exp(-(rho / 0.28) ** 2) * (1 if t > 0 else -0.6)
    ob = _smooth(k.mesh(name + "_body", bm, _fruit_mat("apple_skin", "#a50f1a", "#e8473c", 0.38, 3.5, 0.45),
                        (0, 0, r * 0.88), g))
    stem = k.cyl(name + "_stem", 1.0, 9.0, (1.0, 0, r * 0.88 + r * 0.62 + 2.5), k.mat("stem", "#5b3a1e", 0.7), g,
                 segs=10, r2=0.7)
    stem.rotation_euler = (0.0, 0.25, 0.0)
    leaf = bmesh.new()
    bmesh.ops.create_circle(leaf, cap_ends=True, segments=16, radius=5.0)
    for v in leaf.verts:
        v.co.x *= 1.0
        v.co.y *= 0.45
        v.co.z += 0.04 * v.co.x * v.co.x
    lf = _smooth(k.mesh(name + "_leaf", leaf, k.mat("leaf", "#3fa34d", 0.5), (5.5, 0, r * 0.88 + r * 0.62 + 4.0), g))
    lf.rotation_euler = (0.3, -0.35, 0.4)
    return {"group": g, "wire_point": at + Vector((-r * 0.75, -r * 0.35, r * 0.95)), "top": at + Vector((0, 0, r * 2.2)),
            "centre": at + Vector((0, 0, r * 0.88)), "radius": r}


def orange(k, at, r=22.0, name="orange"):
    at = Vector(at)
    g = k.empty(name, at)
    bm = _uv_sphere(r)
    for v in bm.verts:
        v.co.z *= 0.94
    _smooth(k.mesh(name + "_body", bm, _fruit_mat("orange_peel", "#f07f13", "#ffa62b", 0.55, 5.0, 0.15, dimples=0.35),
                   (0, 0, r * 0.94), g))
    k.cyl(name + "_navel", 2.2, 1.2, (0, 0, r * 1.88 - 0.2), k.mat("navel", "#5f7d2a", 0.6), g, segs=12)
    return {"group": g, "wire_point": at + Vector((-r * 0.8, -r * 0.3, r * 1.0)), "top": at + Vector((0, 0, r * 2.3)),
            "centre": at + Vector((0, 0, r * 0.94)), "radius": r}


def banana(k, at, length=95.0, r=9.0, yaw_deg=0.0, name="banana"):
    """A curved, slightly five-sided tube lying on the desk: bmesh rings along an arc, tapered ends + brown tips."""
    at = Vector(at)
    g = k.empty(name, at)
    g.rotation_euler = (0, 0, math.radians(yaw_deg))
    bm = bmesh.new()
    n_seg, n_side = 28, 10
    bend = math.radians(55)                  # total arc angle
    R = length / bend                        # arc radius
    rings = []
    for i in range(n_seg + 1):
        u = i / n_seg
        a = -bend / 2 + bend * u
        cx, cz = R * math.sin(a), R * (1 - math.cos(a))   # arc in the XZ plane, ends curl upward
        tx, tz = math.cos(a), math.sin(a)                 # tangent
        taper = math.sin(math.pi * u) ** 0.55
        rr = max(0.6, r * taper)
        ring = []
        for j in range(n_side):
            phi = 2 * math.pi * j / n_side
            flat = 1.0 - 0.06 * math.cos(5 * phi)         # faint ridges (five sides)
            ny, nn = math.cos(phi) * rr * flat, math.sin(phi) * rr * flat * 0.92
            # normal direction in XZ is (-tz, tx)
            ring.append(bm.verts.new((cx - tz * nn, ny, cz + tx * nn + r * 0.9)))
        rings.append(ring)
    for i in range(n_seg):
        for j in range(n_side):
            a0, a1 = rings[i][j], rings[i][(j + 1) % n_side]
            b0, b1 = rings[i + 1][j], rings[i + 1][(j + 1) % n_side]
            bm.faces.new((a0, a1, b1, b0))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    body = _subsurf(_smooth(k.mesh(name + "_body", bm, _fruit_mat("banana_skin", "#f2c91d", "#e0b313", 0.5, 4.0, 0.2),
                                   (-R * 0.0, 0, 0), g)), 1)
    for side in (-1, 1):                     # brown tips
        a = side * bend / 2
        tip = Vector((R * math.sin(a), 0, R * (1 - math.cos(a)) + r * 0.9))
        k.cyl(f"{name}_tip{side}", 1.4, 4.0, tip, k.mat("banana_tip", "#4a3317", 0.7), g, segs=10).rotation_euler = \
            (0.0, math.pi / 2 + a, 0.0)
    wp = Vector((-length * 0.18, -r * 0.6, r * 1.5))
    return {"group": g, "wire_point": at + _rot_z(wp, yaw_deg), "top": at + Vector((0, 0, r * 4.5)),
            "centre": at + Vector((0, 0, r * 1.2)), "radius": length * 0.5, "body": body}


def _rot_z(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return Vector((v.x * c - v.y * s, v.x * s + v.y * c, v.z))


def touch_glow(k, centre, color="#ffd166", radius=26.0, name="touchglow"):
    """Soft additive shell around a fruit; returns set(level 0..1)."""
    from parts_ep12 import _emit_val_mat
    m, val = _emit_val_mat(name + "_mat", color, 3.0, edge=True)
    bm = _uv_sphere(radius, 32, 20)
    ob = _smooth(k.mesh(name, bm, m, Vector(centre)))

    def set_level(level):
        val.outputs[0].default_value = max(0.0, min(1.0, level))

    set_level(0.0)
    return set_level
