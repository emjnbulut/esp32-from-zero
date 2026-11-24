"""Episode 11 props for the Pin by Pin Lab Blender kit (additive; pbl.py and parts_pir.py stay untouched).

    import pbl, parts_ep11 as px
    hand = px.warm_hand(k)              # glowing low-poly hand, fingers along +X, wrist at the origin
    jar = px.cookie_jar(k, (60, -90, 0))
    cat, cup = px.cat(k, at), px.tea_cup(k, at)
    th = px.thumb(k, at)                # fist + thumb icon; th["set"](up 0..1, color)
    bz = px.buzzer_unit(k, "active", at)   # loose passive/active buzzer for the comparison shots, set_xray(0..1)
    xr = px.dome_xray(k, pir)           # PIR dome see-through + the sensor can inside
    px.set_heat(hand, 0.8)              # 0 = plain colours, 1 = bright infrared glow

All sizes in mm under the kit root, like every pbl part. Hand / cat / cup are stylised miniatures (the breadboard is
165 mm long), sized to read next to the circuit, not real scale.
"""
import math

import bmesh
import bpy
from mathutils import Vector

from pbl import TOP, lin


def heat_mat(k, name, base, glow):
    """principled material whose emission ('infrared glow') is turned up by set_heat"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(base), 1)
    b.inputs["Roughness"].default_value = 0.55
    b.inputs["Emission Color"].default_value = (*lin(glow), 1)
    b.inputs["Emission Strength"].default_value = 0.0
    if "Subsurface Weight" in b.inputs:
        b.inputs["Subsurface Weight"].default_value = 0.15
    return m


def set_heat(part, level, strength=7.0):
    for m in part["heat"]:
        m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = level * strength


def _flat(k, name, bm, mat, loc, parent, rot=(0, 0, 0), scale=(1, 1, 1)):
    ob = k.mesh(name, bm, mat, loc, parent)
    ob.rotation_euler = rot
    ob.scale = scale
    return ob


def _sphere(r, u=8, v=6):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=r)
    return bm


def _capsule(k, name, r, length, base, yaw, pitch, mat, parent, segs=8):
    """finger: cylinder + rounded tip from `base`, direction (cos p cos y, cos p sin y, -sin p)"""
    d = Vector((math.cos(pitch) * math.cos(yaw), math.cos(pitch) * math.sin(yaw), -math.sin(pitch)))
    base = Vector(base)
    mid = base + d * (length / 2)
    _flat(k, name, k.bm_cyl(r, length, segs), mat, mid, parent, rot=(0, math.pi / 2 + pitch, yaw))
    _flat(k, name + "_tip", _sphere(r, segs, 5), mat, base + d * length, parent)
    _flat(k, name + "_knuckle", _sphere(r * 1.05, segs, 5), mat, base, parent)


# ---------------------------------------------------------------- warm hand
def warm_hand(k, scale=0.6, name="hand"):
    """stylised low-poly hand, palm down, fingers toward local +X, wrist at the origin, forearm along -X.
    Returns {group (move/rotate this), heat [materials], tip (local fingertip point)}"""
    g = k.empty(name)
    g.scale = (scale,) * 3
    m = heat_mat(k, name + "_heat", "#e2a283", "#ff7a1a")
    bm = k.bm_box(36, 32, 11)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=3.0, segments=1, affect="EDGES")
    _flat(k, name + "_palm", bm, m, (18, 0, 0), g)
    for i, (y, ln, r) in enumerate(((-11.5, 24, 3.7), (-3.9, 30, 4.2), (3.9, 33, 4.3), (11.5, 30, 4.1))):
        _capsule(k, f"{name}_f{i}", r, ln, (35, y, 0.5), (y / 11.5) * 0.07, 0.28, m, g)
    _capsule(k, name + "_thumb", 4.8, 22, (14, 14, -2.0), 0.5, 0.32, m, g)
    _flat(k, name + "_wrist", _sphere(12.5, 10, 7), m, (0, 0, 0), g, scale=(1, 1.15, 0.75))
    arm = k.bm_cyl(11.5, 70, 10, r2=10.0)
    _flat(k, name + "_arm", arm, m, (-35, 0, 0), g, rot=(0, -math.pi / 2, 0), scale=(1, 1.15, 0.85))
    return {"group": g, "heat": [m], "tip": Vector((62, 0, -8))}


# ---------------------------------------------------------------- cookie jar
def cookie_jar(k, at, r=16.0, h=40.0, name="jar"):
    at = Vector(at)
    g = k.empty(name, at)
    glass = bpy.data.materials.new(name + "_glass")
    glass.use_nodes = True
    b = glass.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin("#d6ecff"), 1)
    b.inputs["Roughness"].default_value = 0.04
    b.inputs["Alpha"].default_value = 0.22
    b.inputs["Coat Weight"].default_value = 1.0
    if hasattr(glass, "surface_render_method"):
        glass.surface_render_method = "BLENDED"
    elif hasattr(glass, "blend_method"):
        glass.blend_method = "BLEND"
    jar = k.cyl(name + "_glass", r, h, (0, 0, h / 2), glass, g, segs=48, bevel=1.5)
    k.cyl(name + "_rim", r * 0.82, 3.0, (0, 0, h + 1.5), glass, g, segs=48)
    lid = k.mat("jarlid", "#c8402f", 0.35, coat=0.4)
    k.cyl(name + "_lid", r * 0.9, 3.6, (0, 0, h + 4.4), lid, g, segs=48, bevel=1.0)
    k.mesh(name + "_knob", _sphere(3.6, 16, 10), lid, (0, 0, h + 7.6), g, smooth_shade=True)
    dough = k.mat("cookie", "#c48a45", 0.75)
    chip = k.mat("chip", "#3b2214", 0.6)
    spots = [(0, 0, 2.5, 0.1, 0.0), (1.5, -1.0, 6.0, -0.25, 0.6), (-1.0, 1.5, 9.5, 0.3, 1.4), (0.5, 0.5, 13.0, -0.15, 2.2),
             (-1.5, -1.0, 16.4, 0.2, 3.0)]
    for i, (x, y, z, tilt, rz) in enumerate(spots):
        c = k.cyl(f"{name}_cookie{i}", r * 0.68, 2.6, (x, y, z), dough, g, segs=20, bevel=0.6)
        c.rotation_euler = (tilt, tilt * 0.6, rz)
        for j in range(6):
            a = rz + j * 1.1
            rr = (2.5 + (j * 3.7) % 6.0)
            ch = k.box(f"{name}_chip{i}{j}", (1.6, 1.4, 1.0), (rr * math.cos(a), rr * math.sin(a), 1.3), chip, c)
            ch.rotation_euler.z = a
    return {"group": g, "glass": jar, "top": at + Vector((0, 0, h + 8)), "center": at + Vector((0, 0, h / 2))}


# ---------------------------------------------------------------- cat + tea cup (infrared shot)
def cat(k, at, name="cat"):
    at = Vector(at)
    g = k.empty(name, at)
    m = heat_mat(k, name + "_heat", "#d9893d", "#ff8a2a")
    _flat(k, name + "_body", _sphere(1.0, 10, 8), m, (0, 0, 16), g, scale=(14, 12, 17))
    _flat(k, name + "_head", _sphere(9.5, 10, 8), m, (0, -4, 36), g)
    for sx in (-1, 1):
        ear = k.bm_cyl(3.8, 8, 4, r2=0.2)
        _flat(k, f"{name}_ear{sx}", ear, m, (sx * 5.2, -3.5, 45.5), g, rot=(0.15, sx * 0.25, 0))
        _flat(k, f"{name}_paw{sx}", _sphere(4.0, 8, 5), m, (sx * 6.0, -9.5, 2.5), g, scale=(1, 1.4, 0.7))
    cu = bpy.data.curves.new(name + "_tail", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 2.6
    cu.bevel_resolution = 1
    sp = cu.splines.new("BEZIER")
    pts = [(4, 9, 4), (16, 14, 3), (22, 6, 10), (19, -2, 20)]
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    tail = bpy.data.objects.new(name + "_tail", cu)
    cu.materials.append(m)
    k._link(tail, g)
    return {"group": g, "heat": [m], "top": at + Vector((0, 0, 50))}


def tea_cup(k, at, name="cup"):
    at = Vector(at)
    g = k.empty(name, at)
    m = heat_mat(k, name + "_heat", "#f1ede4", "#ffc23a")
    tea = heat_mat(k, name + "_tea", "#6b3a16", "#ffe27a")
    k.cyl(name + "_saucer", 17, 2.0, (0, 0, 1.0), m, g, segs=40, bevel=0.6)
    k.cyl(name + "_body", 9.5, 15, (0, 0, 2 + 7.5), m, g, segs=40, bevel=0.8, r2=12.0)
    k.cyl(name + "_tea", 11.2, 0.4, (0, 0, 2 + 13.6), tea, g, segs=40)
    cu = bpy.data.curves.new(name + "_handle", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 1.6
    cu.bevel_resolution = 2
    sp = cu.splines.new("BEZIER")
    pts = [(10.5, 0, 13.5), (17, 0, 13.5), (17, 0, 6.5), (10, 0, 5.5)]
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    ho = bpy.data.objects.new(name + "_handle", cu)
    cu.materials.append(m)
    k._link(ho, g)
    return {"group": g, "heat": [m, tea], "top": at + Vector((0, 0, 20))}


# ---------------------------------------------------------------- thumbs up / down icon
def thumb(k, at, size=1.0, name="thumb"):
    """fist with the thumb up (local +Z). Rotate group about Y by pi for thumbs down. set(up, rgb_hex)"""
    at = Vector(at)
    g = k.empty(name, at)
    g.scale = (size,) * 3
    m = bpy.data.materials.new(name + "_mat")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin("#2fbf71"), 1)
    b.inputs["Roughness"].default_value = 0.4
    b.inputs["Coat Weight"].default_value = 0.5
    b.inputs["Emission Color"].default_value = (*lin("#2fbf71"), 1)
    b.inputs["Emission Strength"].default_value = 1.2
    bm = k.bm_box(20, 16, 24)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=4.0, segments=2, affect="EDGES")
    _flat(k, name + "_fist", bm, m, (0, 0, 0), g)
    for i in range(4):  # curled fingers on the front (-Y)
        f = k.bm_cyl(3.6, 15, 10)
        _flat(k, f"{name}_curl{i}", f, m, (1.5, -8.5, 7.5 - i * 5.4), g, rot=(0, math.pi / 2, 0))
    _capsule(k, name + "_th", 4.4, 15, (-6, -3, 9), 0.0, -math.pi / 2, m, g, segs=10)
    k.cyl(name + "_cuff", 10.5, 6, (0, 0, -15), k.mat("thumbcuff", "#e9edf2", 0.5), g, segs=24, bevel=1.0)

    def set(up, color):
        g.rotation_euler = (0, math.pi * (1 - up), 0)
        b.inputs["Base Color"].default_value = (*lin(color), 1)
        b.inputs["Emission Color"].default_value = (*lin(color), 1)

    return {"group": g, "set": set, "top": at + Vector((0, 0, 30 * size))}


# ---------------------------------------------------------------- loose buzzers (passive vs active)
def _xray_mat(name="xray11"):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    fr = nt.nodes.new("ShaderNodeLayerWeight")
    fr.inputs["Blend"].default_value = 0.35
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*lin("#2dd4bf"), 1)
    em.inputs["Strength"].default_value = 2.5
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = "ADD"
    pw.inputs[1].default_value = 0.08
    nt.links.new(fr.outputs["Facing"], pw.inputs[0])
    nt.links.new(pw.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    elif hasattr(m, "blend_method"):
        m.blend_method = "BLEND"
    return m


def buzzer_unit(k, kind, at, name=None):
    """a loose 12 mm buzzer standing on its legs (origin = bottom centre of the body).
    passive: open bottom (green PCB visible), black top with the sound hole.
    active: sealed black bottom, a bit taller, white sticker on top; x-ray shows the oscillator chip inside.
    Returns {group, set_xray(x), top (local Vector), kind}"""
    name = name or "bz_" + kind
    at = Vector(at)
    g = k.empty(name, at)
    h = 8.5 if kind == "passive" else 9.5
    body_m = k.mats.get("buzzbody") or k.mat("buzzbody", "#16181c", 0.42)
    body = k.cyl(name + "_body", 6.0, h, (0, 0, h / 2), body_m, g, segs=48, bevel=0.6)
    caps = []
    dark = k.mats.get("holedark") or k.mat("holedark", "#0a0c10", 0.9)
    if kind == "passive":
        caps.append(k.cyl(name + "_hole", 1.1, 0.4, (0, 0, h - 0.15), dark, g, segs=24))
        caps.append(k.cyl(name + "_ring", 2.3, 0.1, (0, 0, h + 0.02), k.mats.get("buzzring") or k.mat("buzzring", "#2a2d33", 0.3), g, segs=40))
        caps.append(k.cyl(name + "_pcb", 5.4, 0.5, (0, 0, -0.2), k.mat("bzpcb", "#1f7a46", 0.45, coat=0.2), g, segs=40))
        for dx in (-1.9, 1.9):
            caps.append(k.cyl(name + "_solder", 0.9, 0.5, (dx, 0, -0.5), k.mat("solder", "#c8ced6", 0.25, metal=1.0), g, segs=12))
    else:
        caps.append(k.cyl(name + "_sticker", 4.9, 0.18, (0, 0, h + 0.05), k.mat("sticker", "#f4f4ef", 0.6), g, segs=40))
        caps.append(k.text(name + "_stk_txt", "REMOVE SEAL", 0.95, (0, 0, h + 0.16), k.mat("stickerink", "#9aa1aa", 0.6), g))
        caps.append(k.cyl(name + "_seal", 5.9, 0.6, (0, 0, -0.25), k.mat("epoxy", "#0b0c0e", 0.3, coat=0.4), g, segs=40))
    silk = k.mats.get("silk") or k.mat("silk", "#eef2f6", 0.6)
    caps.append(k.text(name + "_plus", "+", 2.4, (-2.5, 3.6, h + 0.1 + (0.12 if kind == "active" else 0)), silk, g))
    steel = k.mats.get("legsteel") or k.mat("legsteel", "#c8ced6", 0.3, metal=1.0)
    for dx, ln in ((-3.8, 7.0 if kind == "passive" else 9.0), (3.8, 7.0 if kind == "passive" else 7.5)):
        k.box(name + "_leg", (0.6, 0.6, ln), (dx, 0, -ln / 2), steel, g)
    inside = [k.cyl(name + "_disk", 4.6, 0.25, (0, 0, h - 2.4), k.mats.get("brass") or k.mat("brass", "#c8a24a", 0.3, metal=1.0), g, segs=48),
              k.cyl(name + "_ceramic", 3.0, 0.3, (0, 0, h - 2.15), k.mats.get("ceramic") or k.mat("ceramic", "#e8e4da", 0.5), g, segs=48)]
    if kind == "active":  # the built-in beeper: a tiny oscillator chip + a coil on a little board
        ic = k.mats.get("ic") or k.mat("ic", "#111317", 0.5)
        board = k.cyl(name + "_inpcb", 5.0, 0.5, (0, 0, 1.4), k.mat("bzpcb", "#1f7a46", 0.45, coat=0.2), g, segs=32)
        chip = k.box(name + "_chip", (3.6, 2.4, 1.2), (-1.2, 0, 2.3), ic, g)
        glow = k._emit_mat("chipglow", "#ffb547", 2.5)
        pins = []
        for i in range(4):
            for sy in (-1, 1):
                pins.append(k.box(name + "_cpin", (0.35, 0.5, 0.3), (-2.6 + i * 0.95, sy * 1.45, 1.9), k.mats.get("gold") or k.mat("gold", "#e9bd55", 0.25, metal=1.0), g))
        coil = k.cyl(name + "_coil", 1.3, 2.2, (2.4, 0, 2.7), k.mat("coil", "#b8642c", 0.35, metal=0.8), g, segs=16)
        dot = k.cyl(name + "_chipdot", 0.4, 0.1, (-2.4, -0.6, 2.95), glow, g, segs=10)
        inside += [board, chip, coil, dot] + pins
    solid = body.data.materials[0]
    xm = _xray_mat()

    def set_xray(x):
        on = x > 0.5
        body.data.materials[0] = xm if on else solid
        for o in caps:
            o.hide_render = on
        for o in inside:
            o.hide_render = not on

    set_xray(0.0)
    return {"group": g, "set_xray": set_xray, "top": Vector((0, 0, h + 0.5)), "kind": kind, "h": h}


# ---------------------------------------------------------------- PIR dome x-ray
def dome_xray(k, info):
    """the Fresnel dome turns into teal glass; inside: the pyroelectric sensor can (always there, hidden by the
    opaque dome). Returns set(x 0..1)"""
    lift = info["lift"]
    dome = info["dome"]
    ring = [o for o in lift.children if o.name.startswith("pir_ring")]
    can_m = k.mat("pircan", "#c9d0d9", 0.25, metal=1.0)
    k.cyl("pir_can", 4.6, 4.2, (0, 0, 1.6 + 2.1), can_m, lift, segs=32, bevel=0.3)
    k.box("pir_window", (3.4, 2.6, 0.1), (0, 0, 1.6 + 4.25), k._emit_mat("pirwin", "#3a2a6a", 1.2), lift)
    solid = dome.data.materials[0]
    solid_r = ring[0].data.materials[0] if ring else None
    xm = _xray_mat("xray_dome")

    def set(x):
        on = x > 0.5
        dome.data.materials[0] = xm if on else solid
        for r in ring:
            r.data.materials[0] = xm if on else solid_r

    set(0.0)
    return set
