"""Episode 15 props for the Pin by Pin Lab Blender kit (additive). DRAFT 2026-11-25.

    import pbl, parts_ep15 as p15
    m = p15.ldr_module(k, at, yaw_deg=0)   # {"group", "pins": {"AO","DO","GND","VCC": Vector}, "ldr": Vector, "top"}
    d = p15.drawer(k, at)                  # {"group", "set_open"(mm), "inside", "top"}
    c = p15.light_cone(k, at)              # {"group", "set"(level 0..1), "top"}
All sizes in mm under the kit root; objects sit on the desk at z = 0.
"""
import math

import bmesh
import bpy
from mathutils import Vector

from pbl import lin


def _lbl(k):
    return k.mat("p15_label", "#e9eef5", 0.6)


def _rz(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return Vector((v.x * c - v.y * s, v.x * s + v.y * c, v.z))


def _sphere(r, segs=24, rings=16):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=r)
    return bm


def ldr_module(k, at, yaw_deg=0.0, name="ldr_mod"):
    at = Vector(at)
    g = k.empty(name, at)
    g.rotation_euler = (0, 0, math.radians(yaw_deg))
    z0 = 3.0                                                    # board rests on short feet
    pcb = k.mat("p15_pcb_blue", "#1f4fa8", 0.45, coat=0.3)
    k.box(name + "_pcb", (32, 14, 1.6), (0, 0, z0), pcb, g, bevel=0.3)
    gold = k.mat("p15_gold", "#d8b04a", 0.3, metal=1.0)
    steel = k.mat("p15_steel", "#c9ced6", 0.3, metal=1.0)
    black = k.mat("p15_black", "#15171c", 0.5)
    for sx in (-14, 14):
        for sy in (-5, 5):
            k.cyl(name + "_hole", 1.2, 1.7, (sx, sy, z0), k.mat("p15_hole", "#0b0f1a", 0.8), g, segs=16)
    for sx in (-13, 13):
        for sy in (-5, 5):
            k.cyl(name + "_foot", 0.8, z0, (sx * 1.0, sy * 0.7, z0 / 2 - 0.8), black, g, segs=8)
    pins = {}
    xs = {"AO": 2.0, "DO": 4.54, "GND": 7.08, "VCC": 9.62}
    k.box(name + "_hdr", (10.2, 2.54, 2.4), (5.8, -4.6, z0 + 2.0), black, g, bevel=0.2)
    for n, x in xs.items():
        k.box(name + "_pin" + n, (0.64, 0.64, 11.0), (x, -4.6, z0 + 3.0), gold, g)
        pins[n] = at + _rz(Vector((x, -4.6, z0 + 8.4)), yaw_deg)
        k.text(name + "_t" + n, n, 1.0, (x, -2.4, z0 + 0.85), _lbl(k), g)
    # photoresistor: orange-red disc with zig-zag track, on two legs, at the -X end
    lx = -10.5
    for dy in (-2.2, 2.2):
        k.cyl(name + "_leg", 0.3, 4.0, (lx, dy, z0 + 2.4), steel, g, segs=8)
    k.cyl(name + "_ldr", 4.2, 1.3, (lx, 0, z0 + 5.0), k.mat("p15_ldr", "#c44a1d", 0.35, coat=0.4), g, segs=40)
    track = k.mat("p15_track", "#e9c98a", 0.4, metal=0.6)
    for i in range(5):
        y = -2.6 + i * 1.3
        k.box(name + "_zz", (5.6, 0.45, 0.2), (lx, y, z0 + 5.72), track, g)
        if i < 4:
            xe = lx + (2.7 if i % 2 == 0 else -2.7)
            k.box(name + "_zzc", (0.45, 1.3, 0.2), (xe, y + 0.65, z0 + 5.72), track, g)
    # trim pot
    k.box(name + "_pot", (7, 7, 4.2), (-1.0, 2.2, z0 + 2.9), k.mat("p15_pot", "#2b6fd6", 0.4, coat=0.3), g, bevel=0.3)
    k.cyl(name + "_potdial", 1.6, 0.5, (-1.0, 2.2, z0 + 5.2), k.mat("p15_brass", "#d9b24c", 0.3, metal=1.0), g, segs=24)
    k.box(name + "_potslot", (2.4, 0.4, 0.3), (-1.0, 2.2, z0 + 5.5), black, g)
    # two tiny SMD LEDs (power red, output green)
    for x, c, nm in ((10.5, "#ff3b30", "r"), (13.0, "#47e05a", "g")):
        k.box(name + "_led" + nm, (1.8, 1.0, 0.7), (x, 4.2, z0 + 1.15), k.mat("p15_smd_" + nm, c, 0.3, emit=c, strength=1.2), g)
    k.box(name + "_ic", (4.0, 3.0, 1.0), (6.0, 3.5, z0 + 1.3), black, g)
    return {"group": g, "pins": pins, "ldr": at + _rz(Vector((lx, 0, z0 + 6.0)), yaw_deg),
            "top": at + Vector((0, 0, z0 + 14))}


def _wood_mat(name, c0="#8a5a2b", c1="#b98250"):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.35, 1.0, 1.0)         # stretch noise along X -> grain
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 0.35
    noise.inputs["Detail"].default_value = 6.0
    noise.inputs["Distortion"].default_value = 0.6
    nt.links.new(mp.outputs[0], noise.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[1].position = 0.7
    ramp.color_ramp.elements[0].color = (*lin(c0), 1)
    ramp.color_ramp.elements[1].color = (*lin(c1), 1)
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.55
    return m


def drawer(k, at, name="drawer"):
    """Desk drawer: case open at the front (-Y); inner box + front panel + knob slide along -Y via set_open(mm)."""
    at = Vector(at)
    g = k.empty(name, at)
    W, D, H, t = 64.0, 52.0, 34.0, 2.2
    wood = _wood_mat("p15_wood")
    wood2 = _wood_mat("p15_wood_dark", "#6e4521", "#96653a")
    k.box(name + "_bot", (W, D, t), (0, 0, t / 2), wood2, g)
    k.box(name + "_top", (W, D, t), (0, 0, H - t / 2), wood2, g)
    k.box(name + "_back", (W, t, H), (0, D / 2 - t / 2, H / 2), wood2, g)
    for s in (-1, 1):
        k.box(name + "_side", (t, D, H), (s * (W / 2 - t / 2), 0, H / 2), wood2, g)
    inner = k.empty(name + "_inner", (0, 0, 0), g)
    iw, idp, ih = W - 2 * t - 1.6, D - 6.0, 20.0
    iz = t + 1.0
    k.box(name + "_ib", (iw, idp, 1.6), (0, 2.0, iz + 0.8), wood, inner)
    k.box(name + "_iback", (iw, 1.6, ih), (0, 2.0 + idp / 2 - 0.8, iz + ih / 2), wood, inner)
    for s in (-1, 1):
        k.box(name + "_is", (1.6, idp, ih), (s * (iw / 2 - 0.8), 2.0, iz + ih / 2), wood, inner)
    fy = 2.0 - idp / 2 - 1.0
    k.box(name + "_ifront", (iw, 1.6, ih), (0, fy + 0.8, iz + ih / 2), wood, inner)
    fw, fh = W - 2 * t + 2.0, H - 2 * t - 1.0
    k.box(name + "_panel", (fw, 2.4, fh), (0, fy - 1.2, H / 2), _wood_mat("p15_wood_front", "#9b6a38", "#c18d57"), inner, bevel=0.4)
    brass = k.mat("p15_knob_m", "#cfa84d", 0.3, metal=1.0)
    k.cyl(name + "_knobstem", 1.0, 3.0, (0, fy - 3.6, H / 2), brass, inner, segs=12).rotation_euler = (math.pi / 2, 0, 0)
    k.mesh(name + "_knob", _sphere(4.2), brass, (0, fy - 7.0, H / 2), inner, smooth_shade=True)
    rest = inner.location.copy()

    def set_open(mm):
        inner.location = rest + Vector((0, -float(mm), 0))

    set_open(0)
    return {"group": g, "set_open": set_open, "inside": at + Vector((0, -2.0, iz + 9.0)), "top": at + Vector((0, 0, H + 8))}


def light_cone(k, at, height=70.0, r_bottom=26.0, r_top=5.0, color="#fff1c2", name="lightcone"):
    """Soft cone of light, narrow end up. set(level 0..1)."""
    from parts_ep12 import _emit_val_mat
    at = Vector(at)
    g = k.empty(name, at)
    m, val = _emit_val_mat(name + "_mat", color, 2.2, edge=True)
    ob = k.mesh(name + "_cone", k.bm_cyl(r_bottom, height, 48, r_top), m, (0, 0, height / 2), g)
    ob.data.shade_smooth() if hasattr(ob.data, "shade_smooth") else None

    def set_level(level):
        val.outputs[0].default_value = max(0.0, min(1.0, level))

    set_level(0.0)
    return {"group": g, "set": set_level, "top": at + Vector((0, 0, height))}
