"""Episode 12 props for the Pin by Pin Lab Blender kit (additive; pbl.py stays untouched).

    import pbl, parts_ep12 as p12
    ph = p12.phone(k, at, tilt_deg=70)       # phone on a little stand, screen toward -Y; ph["set_screen"](bpy image)
    ph["world"](u, v)                        # world mm point of a screen spot (u, v = 0..1 from the top-left)
    ph["set_tap"](u, v, level)               # glowing finger-tap dot
    rp = p12.ripples(k, centre, "#7fe8de")   # radio ripples: rp["set"](t, t0, t1, ...) / rp["bubble"](r, a)
    pk = p12.packet(k)                       # pk["set"](pos or None, trail positions)
    ah = p12.antenna_glow(k)                 # ah(level): the ESP32 module's zig-zag antenna lights up
    rt = p12.router(k, at)                   # a home router (Wi-Fi box with two antennas)

All sizes in mm under the kit root. The phone is a desk miniature (~42 x 90 mm), like the Ep 11 hand.
"""
import math

import bmesh
import bpy
from mathutils import Vector

from pbl import lin


def _emit_val_mat(name, color, strength, edge=False):
    """emission <-> transparent mixed by a Value node (0 = invisible); edge=True: only the silhouette glows (bubble)"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*lin(color), 1)
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    val = nt.nodes.new("ShaderNodeValue")
    val.outputs[0].default_value = 0.0
    if edge:
        lw = nt.nodes.new("ShaderNodeLayerWeight")
        lw.inputs["Blend"].default_value = 0.12
        pw = nt.nodes.new("ShaderNodeMath")
        pw.operation = "POWER"
        pw.inputs[1].default_value = 3.0
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        nt.links.new(lw.outputs["Facing"], pw.inputs[0])
        nt.links.new(pw.outputs[0], mul.inputs[0])
        nt.links.new(val.outputs[0], mul.inputs[1])
        nt.links.new(mul.outputs[0], mix.inputs["Fac"])
    else:
        nt.links.new(val.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    if hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    elif hasattr(m, "blend_method"):
        m.blend_method = "BLEND"
    return m, val


# ---------------------------------------------------------------- phone
def phone(k, at, tilt_deg=70.0, yaw_deg=0.0, size=(42.0, 90.0, 4.6), name="phone"):
    """a phone leaning on a small stand; origin = the middle of its bottom edge on the desk.
    Local: x = width, y = length (up the screen), z = out of the screen. tilt_deg: screen normal from vertical."""
    at = Vector(at)
    w, l, th = size
    g = k.empty(name, at)
    g.rotation_euler = (math.radians(tilt_deg), 0, math.radians(yaw_deg))
    body = k.mat("phonebody", "#1b1f27", 0.35, metal=0.4, coat=0.5)
    k.box(name + "_body", (w, l, th), (0, l / 2, th / 2 + 2.0), body, g, bevel=3.0)
    glass = k.mat("phoneglass", "#05070b", 0.12, coat=1.0, spec=0.6)
    k.box(name + "_glass", (w - 1.2, l - 1.2, 0.3), (0, l / 2, th + 2.0 + 0.05), glass, g, bevel=0.15)
    for i, (y0, ln) in enumerate(((l * 0.70, 9.0), (l * 0.56, 6.0), (l * 0.47, 6.0))):  # side buttons
        k.box(f"{name}_key{i}", (0.8, ln, 1.6), (w / 2 + 0.3 if i == 0 else -w / 2 - 0.3, y0, th / 2 + 2.0), body, g)
    k.cyl(name + "_cam", 1.1, 0.3, (0, l - 3.2, th + 2.2), k.mat("phonecam", "#0e1116", 0.2), g, segs=20)
    # screen: emissive image plane, UV (0,0) bottom-left
    sw, sh = w - 3.0, (w - 3.0) * 1170 / 540
    m = bpy.data.materials.new(name + "_screen")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1)
    b.inputs["Roughness"].default_value = 0.2
    b.inputs["Coat Weight"].default_value = 0.0
    if "Specular IOR Level" in b.inputs:  # pure glowing screen: no washed-out reflection of the key light
        b.inputs["Specular IOR Level"].default_value = 0.0
    img = nt.nodes.new("ShaderNodeTexImage")
    img.interpolation = "Linear"
    nt.links.new(img.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = 1.6
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    uvl = bm.loops.layers.uv.new()
    for f in bm.faces:
        for loop in f.loops:
            loop[uvl].uv = (loop.vert.co.x + 0.5, loop.vert.co.y + 0.5)
    for v in bm.verts:
        v.co.x *= sw
        v.co.y *= sh
    sy = l / 2 + 0.3
    sz = th + 2.0 + 0.22
    k.mesh(name + "_screen", bm, m, (0, sy, sz), g)
    # stand behind the phone
    stand = k.mat("phonestand", "#3a4150", 0.5)
    k.box(name + "_standfoot", (w * 0.8, 3.0, 30.0), (0, 1.5, -14.0), stand, g)
    k.box(name + "_lip", (w * 0.8, 3.0, 4.0), (0, -0.5, 4.0), stand, g)
    # finger-tap dot
    tap_m, tap_v = _emit_val_mat(name + "_tapmat", "#ffffff", 6.0)
    bmt = bmesh.new()
    bmesh.ops.create_circle(bmt, cap_ends=True, segments=32, radius=2.6)
    tap = k.mesh(name + "_tap", bmt, tap_m, (0, sy, sz + 0.08), g)
    bmr = bmesh.new()
    bmesh.ops.create_circle(bmr, cap_ends=False, segments=40, radius=1.0)
    ring_m, ring_v = _emit_val_mat(name + "_tapring", "#ffffff", 5.0)
    ring = k.mesh(name + "_tapring", bmr, ring_m, (0, sy, sz + 0.1), g)
    wf = ring.modifiers.new("w", "WIREFRAME")
    wf.thickness = 0.09
    wf.use_relative_offset = False

    def local(u, v):
        return Vector(((u - 0.5) * sw, sy + (0.5 - v) * sh, sz))

    def _w(p):
        bpy.context.view_layer.update()
        return (g.matrix_world @ p) / 0.001

    def world(u, v):
        return _w(local(u, v))

    def set_screen(image):
        img.image = image

    def set_tap(u, v, level, age=0.0):
        p = local(u, v)
        tap.location = (p.x, p.y, sz + 0.08)
        ring.location = (p.x, p.y, sz + 0.1)
        tap_v.outputs[0].default_value = 0.85 * level
        tap.hide_render = level <= 0.01
        s = 2.6 + 9.0 * min(1.0, age / 0.35)
        ring.scale = (s, s, 1)
        ring_v.outputs[0].default_value = max(0.0, 1 - age / 0.35) * (1.0 if age >= 0 else 0.0)
        ring.hide_render = not (0 <= age <= 0.35)

    set_tap(0.5, 0.5, 0.0, -1)
    return {"group": g, "set_screen": set_screen, "set_tap": set_tap, "world": world, "local": local,
            "top": lambda: _w(Vector((0, l + 2, th / 2 + 2))), "screen_mat": m}


# ---------------------------------------------------------------- radio ripples
def ripples(k, centre, color="#7fe8de", n=4, half=True, name="rip"):
    """expanding glowing bubbles (only their rims glow) from `centre`. Returns {set(...), bubble(r, a), centre}"""
    shells = []
    for i in range(n):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=1.0)
        if half:
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.05], context="VERTS")
        m, val = _emit_val_mat(f"{name}_mat{i}", color, 3.0, edge=True)
        ob = k.mesh(f"{name}{i}", bm, m, tuple(centre))
        ob.data.shade_smooth() if hasattr(ob.data, "shade_smooth") else None
        ob.hide_render = True
        shells.append((ob, val))
    info = {"centre": Vector(centre)}

    def off():
        for ob, val in shells:
            ob.hide_render = True
            val.outputs[0].default_value = 0.0

    def set(t, t0, t1=1e9, level=1.0, period=1.1, rmax=110.0, r0=4.0, centre=None):
        """waves leave every period/n seconds between t0 and t1; each grows to rmax and fades"""
        for i, (ob, val) in enumerate(shells):
            if centre is not None:
                ob.location = centre
            best = None
            # the latest wave of this shell slot that has started
            if t >= t0:
                kk = math.floor(((t - t0) / period) - i / n)
                start = t0 + (kk + i / n) * period
                if start >= t0 and start <= t1:
                    best = (t - start) / period
            if best is None or not 0 <= best <= 1:
                ob.hide_render = True
                val.outputs[0].default_value = 0.0
                continue
            r = r0 + (rmax - r0) * best ** 0.8
            ob.scale = (r, r, r)
            ob.hide_render = False
            val.outputs[0].default_value = level * (1 - best) ** 1.2 * min(1.0, best * 8)

    def bubble(r, a, slot=0):
        ob, val = shells[slot]
        ob.scale = (r, r, r)
        ob.hide_render = a <= 0.01
        val.outputs[0].default_value = a

    info.update(set=set, bubble=bubble, off=off, shells=shells)
    off()
    return info


# ---------------------------------------------------------------- packet
def packet(k, color="#ffd166", trail=5, name="pkt"):
    m = k._emit_mat(name + "_core", color, 9.0)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=2.2)
    core = k.mesh(name, bm, m, (0, 0, 0), smooth_shade=True)
    tails = []
    for i in range(trail):
        tm, tv = _emit_val_mat(f"{name}_tail{i}", color, 5.0)
        bt = bmesh.new()
        bmesh.ops.create_uvsphere(bt, u_segments=12, v_segments=8, radius=1.9 * (1 - (i + 1) / (trail + 2)))
        ob = k.mesh(f"{name}_t{i}", bt, tm, (0, 0, 0), smooth_shade=True)
        tails.append((ob, tv))

    def set(pos, trail_pos=()):
        core.hide_render = pos is None
        if pos is not None:
            core.location = pos
        for i, (ob, tv) in enumerate(tails):
            if pos is not None and i < len(trail_pos) and trail_pos[i] is not None:
                ob.location = trail_pos[i]
                ob.hide_render = False
                tv.outputs[0].default_value = 0.7 * (1 - (i + 1) / (len(tails) + 1))
            else:
                ob.hide_render = True

    set(None)
    return {"set": set, "core": core}


def arc_path(a, b, lift=40.0):
    """point on a raised arc from a to b, u = 0..1"""
    a, b = Vector(a), Vector(b)

    def f(u):
        u = max(0.0, min(1.0, u))
        p = a.lerp(b, u)
        p.z += lift * 4 * u * (1 - u)
        return p
    return f


# ---------------------------------------------------------------- antenna highlight
def antenna_glow(k, color="#ffd166"):
    """glowing copy of the ESP32 module's PCB antenna as one zig-zag line; returns set(level 0..1)"""
    e = k.esp
    xA, z = e["xA"], e["pcb_top"] + 0.9
    modW = (12.76 * 2) - 9.5
    half = (modW - 5) / 2
    m = bpy.data.materials.new("antglow")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(color), 1)
    b.inputs["Emission Color"].default_value = (*lin(color), 1)
    g = k.empty("antglow")
    xs = [xA - 1.6 - s * 0.9 for s in range(5)]
    for i, x in enumerate(xs):
        k.box("ant_line", (0.55, half * 2, 0.12), (x, 0, z), m, g)
        if i < len(xs) - 1:  # connector at alternating ends -> one continuous meander
            y = half if i % 2 == 0 else -half
            k.box("ant_join", (0.9 + 0.55, 0.55, 0.12), ((x + xs[i + 1]) / 2, y, z), m, g)
    k.box("ant_feed", (0.55, 3.0, 0.12), (xs[-1] - 0.5, -half - 1.0, z), m, g)

    def set(level):
        b.inputs["Emission Strength"].default_value = 12.0 * level
        for o in g.children:
            o.hide_render = level <= 0.01

    set(0.0)
    return {"set": set, "centre": Vector(((xs[0] + xs[-1]) / 2, 0, z))}


# ---------------------------------------------------------------- home router
def router(k, at, name="router"):
    at = Vector(at)
    g = k.empty(name, at)
    body = k.mat("routerbody", "#e9edf2", 0.4, coat=0.3)
    k.box(name + "_body", (46, 30, 9), (0, 0, 4.5 + 3), body, g, bevel=2.0)
    for sx in (-1, 1):
        k.cyl(f"{name}_foot{sx}", 2.0, 3.0, (sx * 16, 0, 1.5), k.mat("routerfoot", "#9aa1aa", 0.5), g, segs=12)
        a = k.cyl(f"{name}_ant{sx}", 1.4, 34, (sx * 17, 12, 12 + 17), k.mat("routerant", "#2a2f3a", 0.4), g, segs=16, bevel=0.5)
        a.rotation_euler = (0.0, sx * 0.18, 0.0)
    for i in range(4):
        k.cyl(f"{name}_led{i}", 0.8, 0.3, (-9 + i * 6, -15.1, 9), k._emit_mat("routerled", "#2fbf71", 6.0), g, segs=10).rotation_euler = (math.pi / 2, 0, 0)
    return {"group": g, "top": at + Vector((0, 8, 46))}

