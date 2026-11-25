"""Episode 16 props for the Pin by Pin Lab Blender kit (additive). DRAFT 2026-11-25.

    import pbl, parts_ep16 as p16
    m = p16.ir_module(k, at, yaw_deg=0)  # {"group","pins":{"OUT","GND","VCC"},"emitter","receiver","top","set"(level)}
    h = p16.hoop(k, at)                  # {"group","rim","sensor_spot","top"}
    b = p16.paper_ball(k, at)            # {"group","ob","radius"}; keyframe b["group"].location
    s = p16.ir_beam(k, a, b)             # {"group","set"(level)}   a, b in kit-root mm
Module front edge (diodes) points +Y before yaw. mm under the kit root, objects rest on the desk at z = 0.
"""
import math
import random

import bmesh
import bpy
from mathutils import Vector

from pbl import lin


def _rz(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return Vector((v.x * c - v.y * s, v.x * s + v.y * c, v.z))


def _glass(k, name, color, alpha):
    m = k.mat(name, color, 0.08, coat=0.6, alpha=alpha)
    try:
        m.surface_render_method = "BLENDED"
    except Exception:
        pass
    return m


def _diode(k, g, name, x, y, z, clear):
    """5 mm through-hole diode lying along +Y: body, domed tip, flange, two legs."""
    body_m = _glass(k, "p16_ir_clear", "#dbe6f5", 0.55) if clear else k.mat("p16_ir_dark", "#2a1018", 0.25, coat=0.5)
    cy = k.cyl(name + "_body", 2.5, 5.0, (x, y, z), body_m, g, segs=32)
    cy.rotation_euler = (math.pi / 2, 0, 0)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=2.5)
    dome = k.mesh(name + "_dome", bm, body_m, (x, y + 2.5, z), g, smooth_shade=True)
    dome.scale = (1, 0.8, 1)
    fl = k.cyl(name + "_flange", 3.0, 0.8, (x, y - 2.5, z), body_m, g, segs=32)
    fl.rotation_euler = (math.pi / 2, 0, 0)
    steel = k.mat("p16_steel", "#c9ced6", 0.3, metal=1.0)
    for dx in (-0.9, 0.9):
        k.box(name + "_leg", (0.4, 4.0, 0.4), (x + dx, y - 4.8, z - 0.0), steel, g)
        k.box(name + "_legd", (0.4, 0.4, z - 2.2), (x + dx, y - 6.8, (z - 2.2) / 2 + 2.2), steel, g)
    if clear:                                     # tiny die visible inside the clear lens
        k.box(name + "_die", (1.2, 1.2, 1.2), (x, y - 0.5, z), k.mat("p16_die", "#e8e0c0", 0.4, emit="#ffd9d9", strength=0.6), g)


def ir_module(k, at, yaw_deg=0.0, name="ir_mod"):
    at = Vector(at)
    g = k.empty(name, at)
    g.rotation_euler = (0, 0, math.radians(yaw_deg))
    z0 = 3.0
    pcb = k.mat("p16_pcb", "#1f4fa8", 0.45, coat=0.3)
    k.box(name + "_pcb", (32, 14, 1.6), (0, 0, z0), pcb, g, bevel=0.3)
    black = k.mat("p16_black", "#15171c", 0.5)
    gold = k.mat("p16_gold", "#d8b04a", 0.3, metal=1.0)
    lbl = k.mat("p16_label", "#e9eef5", 0.6)
    for sx in (-13, 13):
        for sy in (-4.5, 4.5):
            k.cyl(name + "_foot", 0.8, z0, (sx, sy, z0 / 2 - 0.8), black, g, segs=8)
    for sx in (-14, 14):
        k.cyl(name + "_hole", 1.2, 1.7, (sx, 0, z0), k.mat("p16_hole", "#0b0f1a", 0.8), g, segs=16)
    zd = z0 + 4.6
    _diode(k, g, name + "_tx", -5.5, 4.0, zd, True)
    _diode(k, g, name + "_rx", 5.5, 4.0, zd, False)
    # trim pot
    k.box(name + "_pot", (7, 7, 4.2), (-9.5, -1.0, z0 + 2.9), k.mat("p16_pot", "#2b6fd6", 0.4, coat=0.3), g, bevel=0.3)
    k.cyl(name + "_dial", 1.6, 0.5, (-9.5, -1.0, z0 + 5.2), k.mat("p16_brass", "#d9b24c", 0.3, metal=1.0), g, segs=24)
    k.box(name + "_slot", (2.4, 0.4, 0.3), (-9.5, -1.0, z0 + 5.5), black, g)
    k.box(name + "_ic", (5.0, 3.0, 1.0), (1.0, -1.0, z0 + 1.3), black, g)
    # pins OUT GND VCC on the back edge (-Y)
    pins = {}
    k.box(name + "_hdr", (7.7, 2.54, 2.4), (9.0, -5.0, z0 + 2.0), black, g, bevel=0.2)
    for n, x in (("OUT", 6.46), ("GND", 9.0), ("VCC", 11.54)):
        k.box(name + "_pin" + n, (0.64, 0.64, 11.0), (x, -5.0, z0 + 3.0), gold, g)
        pins[n] = at + _rz(Vector((x, -5.0, z0 + 8.4)), yaw_deg)
        k.text(name + "_t" + n, n, 1.0, (x, -2.8, z0 + 0.85), lbl, g)
    # red status LED + glow
    led_body = k.mat("p16_led_dim", "#7a1410", 0.25, coat=0.5)
    k.cyl(name + "_led", 1.5, 2.2, (0.5, 4.5, z0 + 2.0), led_body, g, segs=24)
    from parts_ep12 import _emit_val_mat
    gm, val = _emit_val_mat(name + "_glow", "#ff3b30", 6.0)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=1.8)
    k.mesh(name + "_glowball", bm, gm, (0.5, 4.5, z0 + 3.2), g, smooth_shade=True)

    def set_level(level):
        val.outputs[0].default_value = max(0.0, min(1.0, level))

    set_level(0.0)
    return {"group": g, "pins": pins, "set": set_level,
            "emitter": at + _rz(Vector((-5.5, 4.0 + 5.4, zd)), yaw_deg),
            "receiver": at + _rz(Vector((5.5, 4.0 + 5.4, zd)), yaw_deg),
            "top": at + Vector((0, 0, z0 + 14))}


def _book(k, g, name, size, loc, color, spine_color="#f2ead8"):
    w, d, h = size
    k.box(name + "_pages", (w - 1.0, d - 0.8, h - 3.0), (loc[0] + 0.3, loc[1], loc[2]), k.mat("p16_pages", spine_color, 0.7), g)
    k.box(name + "_cover_t", (w, d, 1.4), (loc[0], loc[1], loc[2] + h / 2 - 0.7), k.mat("p16_cov_" + name, color, 0.55, coat=0.15), g, bevel=0.3)
    k.box(name + "_cover_b", (w, d, 1.4), (loc[0], loc[1], loc[2] - h / 2 + 0.7), k.mat("p16_cov_" + name, color, 0.55, coat=0.15), g, bevel=0.3)
    k.box(name + "_spine", (1.4, d, h), (loc[0] - w / 2 + 0.7, loc[1], loc[2]), k.mat("p16_cov_" + name, color, 0.55, coat=0.15), g, bevel=0.3)


def _tube(r_bot, r_top, h, wall, z0=0.0, segs=48, grow=0.0):
    """Open tapered tube (both ends open) with wall thickness; grow > 0 pushes the outside out a hair."""
    bm = bmesh.new()
    rings = []
    for (r, z) in ((r_bot + grow, z0), (r_top + grow, z0 + h), (r_top - wall, z0 + h), (r_bot - wall, z0)):
        rings.append([bm.verts.new((r * math.cos(2 * math.pi * i / segs), r * math.sin(2 * math.pi * i / segs), z))
                      for i in range(segs)])
    for a in range(4):
        b = (a + 1) % 4
        for i in range(segs):
            j = (i + 1) % segs
            bm.faces.new((rings[a][i], rings[a][j], rings[b][j], rings[b][i]))
    return bm


def hoop(k, at, scale=0.62, name="hoop"):
    """Paper cup (open both ends) upright on two books with a card backboard behind it (+Y)."""
    at = Vector(at)
    g = k.empty(name, at)
    g.scale = (scale,) * 3
    _book(k, g, name + "_b1", (96, 68, 15), (0, 0, 7.5), "#2f6f8f")
    _book(k, g, name + "_b2", (82, 60, 12), (3, -1, 15 + 6), "#b5452f")
    zb = 15 + 12
    ch, rb, rt = 62.0, 21.0, 31.0
    cup = k.mesh(name + "_cup", _tube(rb, rt, ch, 0.9), k.mat("p16_cup", "#f4f1ea", 0.5), (3, -1, zb), g, smooth_shade=True)
    cup.data.shade_smooth() if hasattr(cup.data, "shade_smooth") else None
    band_r = lambda f: rb + (rt - rb) * f
    k.mesh(name + "_stripe", _tube(band_r(0.62), band_r(0.78), ch * 0.16, 0.9, z0=ch * 0.62, grow=0.25),
           k.mat("p16_stripe", "#e0463a", 0.5), (3, -1, zb), g, smooth_shade=True)
    k.box(name + "_card", (96, 2.0, 90), (0, 36, 15 + 45), k.mat("p16_card", "#d9c29a", 0.8), g, bevel=0.3)
    k.box(name + "_card_f", (96, 0.3, 90), (0, 34.9, 15 + 45), k.mat("p16_card_face", "#efe3c6", 0.8), g)
    rim_z = zb + ch
    S = scale
    return {"group": g, "rim": at + Vector((3 * S, -1 * S, rim_z * S)),
            "sensor_spot": at + Vector((3 * S, -1 * S, (rim_z - 9.0) * S)),
            "top": at + Vector((3 * S, -1 * S, (rim_z + 12) * S)), "rim_radius": rt * S}


def paper_ball(k, at, r=7.0, seed=7, name="paperball"):
    """Crumpled paper ball ~14 mm: icosphere + seeded random displacement. at = centre of the ball."""
    at = Vector(at)
    g = k.empty(name, at)
    rnd = random.Random(seed)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=r)
    for v in bm.verts:
        v.co *= 1.0 + rnd.uniform(-0.18, 0.12)
    bm.normal_update()
    ob = k.mesh(name + "_mesh", bm, k.mat("p16_paper", "#f1ede2", 0.85), (0, 0, 0), g)
    for p in ob.data.polygons:
        p.use_smooth = False
    return {"group": g, "ob": g, "radius": r}


def ir_beam(k, a, b, radius=0.45, color="#ff2a20", name="irbeam"):
    """Thin red emissive beam between a and b (kit-root mm). set(level 0..1)."""
    from parts_ep12 import _emit_val_mat
    a, b = Vector(a), Vector(b)
    d = b - a
    m, val = _emit_val_mat(name + "_mat", color, 8.0)
    ob = k.cyl(name, radius, d.length, (a + b) / 2, m, None, segs=12)
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = d.normalized().to_track_quat("Z", "Y")

    def set_level(level):
        val.outputs[0].default_value = max(0.0, min(1.0, level))

    set_level(1.0)
    return {"group": ob, "set": set_level}
