"""Episode 17 props for the Pin by Pin Lab Blender kit (additive). DRAFT 2026-11-25.

    import pbl, parts_ep17 as p17
    r = p17.relay_module(k, at, yaw_deg=0)  # {"group","terminals":{(ch,"NO"|"COM"|"NC"): Vector},"pins":{"GND","IN1","IN2","VCC"},
                                            #  "set_led"(i, level), "relay_top": [Vector, Vector], "top"}
    f = p17.usb_fan(k, at)                  # {"group","set_spin"(angle_rad),"cable_start","top"}; fan faces -Y
    c = p17.relay_cutaway(k, at)            # {"group","set_arm"(t 0..1),"set_spark"(level),"no","nc","coil","top"}
Relay board: header on the front edge (-Y), screw terminals on the back edge (+Y, wires enter facing +Y).
mm under the kit root, objects rest on the desk at z = 0 (the relay board sits on small feet).
"""
import math

import bmesh
import bpy
from mathutils import Vector


def _rz(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return Vector((v.x * c - v.y * s, v.x * s + v.y * c, v.z))


def _blend(m):
    try:
        m.surface_render_method = "BLENDED"
    except Exception:
        pass
    return m


def relay_module(k, at, yaw_deg=0.0, name="relay_mod"):
    at = Vector(at)
    g = k.empty(name, at)
    g.rotation_euler = (0, 0, math.radians(yaw_deg))
    z0 = 3.0
    black = k.mat("p17_black", "#15171c", 0.5)
    gold = k.mat("p17_gold", "#d8b04a", 0.3, metal=1.0)
    steel = k.mat("p17_steel", "#c9ced6", 0.3, metal=1.0)
    lbl = k.mat("p17_label", "#f2f5fa", 0.6)
    k.box(name + "_pcb", (50, 38, 1.6), (0, 0, z0), k.mat("p17_pcb", "#1c4ea0", 0.45, coat=0.3), g, bevel=0.35)
    for sx in (-22, 22):
        for sy in (-15.5, 15.5):
            k.cyl(name + "_hole", 1.5, 1.7, (sx, sy, z0), k.mat("p17_hole", "#0b0f1a", 0.8), g, segs=16)
            k.cyl(name + "_foot", 1.0, z0, (sx, sy, z0 / 2 - 0.8), black, g, segs=10)
    centres = (-12.5, 12.5)
    relay_top = []
    blue = k.mat("p17_relay", "#2a63d4", 0.35, coat=0.35)
    for i, cx in enumerate(centres):
        k.box(f"{name}_relay{i}", (19, 15, 15), (cx, 0, z0 + 0.8 + 7.5), blue, g, bevel=0.5)
        k.text(f"{name}_rt{i}", "5V RELAY", 2.0, (cx, 0, z0 + 15.85), lbl, g)
        relay_top.append(at + _rz(Vector((cx, 0, z0 + 16.0)), yaw_deg))
    # screw terminals (three-way) on the back edge
    terminals = {}
    green = k.mat("p17_term", "#2f9e5e", 0.4, coat=0.2)
    for ch, cx in enumerate(centres, start=1):
        k.box(f"{name}_term{ch}", (15, 8, 9.5), (cx, 15.2, z0 + 0.8 + 4.75), green, g, bevel=0.35)
        for j, label in enumerate(("NO", "COM", "NC")):
            x = cx + (j - 1) * 5.0
            k.cyl(f"{name}_scr{ch}{j}", 1.7, 0.8, (x, 15.2, z0 + 10.6), steel, g, segs=20)
            k.box(f"{name}_slot{ch}{j}", (2.6, 0.45, 0.4), (x, 15.2, z0 + 11.1), black, g).rotation_euler = (0, 0, 0.5 * j)
            k.box(f"{name}_hole{ch}{j}", (3.2, 0.5, 3.4), (x, 19.15, z0 + 5.4), black, g)
            k.text(f"{name}_tl{ch}{j}", label, 1.1, (x, 9.4, z0 + 0.85), lbl, g)
            terminals[(ch, label)] = at + _rz(Vector((x, 19.6, z0 + 5.4)), yaw_deg)
    # input header on the front edge
    pins = {}
    k.box(name + "_hdr", (10.2, 2.54, 2.4), (-14.0 + 3.81, -16.0, z0 + 2.0), black, g, bevel=0.2)
    for n, x in (("GND", -14.0), ("IN1", -11.46), ("IN2", -8.92), ("VCC", -6.38)):
        k.box(name + "_pin" + n, (0.64, 0.64, 11.0), (x + 0.0, -16.0, z0 + 3.0), gold, g)
        pins[n] = at + _rz(Vector((x, -16.0, z0 + 8.4)), yaw_deg)
        k.text(name + "_t" + n, n, 1.0, (x, -13.4, z0 + 0.85), lbl, g)
    # red channel LEDs (each: dim body + glow ball driven by set_led)
    from parts_ep12 import _emit_val_mat
    dim = k.mat("p17_led_dim", "#7a1410", 0.25, coat=0.5)
    vals = []
    for i, cx in enumerate(centres):
        x = cx + 8.0
        k.cyl(f"{name}_led{i}", 1.4, 2.0, (x, -9.5, z0 + 1.8), dim, g, segs=24)
        gm, val = _emit_val_mat(f"{name}_glow{i}", "#ff3b30", 6.0)
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=1.7)
        k.mesh(f"{name}_glowball{i}", bm, gm, (x, -9.5, z0 + 2.9), g, smooth_shade=True)
        vals.append(val)
    k.box(name + "_ic", (5.0, 3.5, 1.0), (0, -9.5, z0 + 1.3), black, g)

    def set_led(i, level):
        vals[i].outputs[0].default_value = max(0.0, min(1.0, level))

    for i in range(2):
        set_led(i, 0.0)
    return {"group": g, "terminals": terminals, "pins": pins, "set_led": set_led, "relay_top": relay_top,
            "top": at + Vector((0, 0, z0 + 22))}


def _torus(R, r, segs=64, rsegs=8):
    bm = bmesh.new()
    rings = []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        ring = []
        for j in range(rsegs):
            b = 2 * math.pi * j / rsegs
            rr = R + r * math.cos(b)
            ring.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), r * math.sin(b))))
        rings.append(ring)
    for i in range(segs):
        for j in range(rsegs):
            bm.faces.new((rings[i][j], rings[(i + 1) % segs][j], rings[(i + 1) % segs][(j + 1) % rsegs], rings[i][(j + 1) % rsegs]))
    return bm


def usb_fan(k, at, scale=0.7, name="usbfan"):
    """Desk fan facing -Y. set_spin(angle_rad) turns the blades."""
    at = Vector(at)
    g = k.empty(name, at)
    g.scale = (scale,) * 3
    body = k.mat("p17_fan_body", "#e8ecf2", 0.4, coat=0.3)
    dark = k.mat("p17_fan_dark", "#2b3140", 0.4)
    accent = k.mat("p17_fan_blade", "#4aa3e8", 0.35, coat=0.3)
    wire = k.mat("p17_fan_guard", "#b9c2d0", 0.3, metal=0.8)
    hz = 58.0
    k.cyl(name + "_base", 26.0, 5.0, (0, 0, 2.5), body, g, segs=48, bevel=0.8)
    k.cyl(name + "_stand", 3.4, 36.0, (0, 6, 5 + 18), body, g, segs=24)
    k.cyl(name + "_motor", 9.5, 16.0, (0, 6, hz), body, g, segs=40, bevel=0.8).rotation_euler = (math.pi / 2, 0, 0)
    k.cyl(name + "_cap", 5.5, 3.0, (0, 6 - 8.5, hz), dark, g, segs=32).rotation_euler = (math.pi / 2, 0, 0)
    # guard in front of the blades: rings + spokes (plane y = -9)
    gy = -8.0
    for R in (31.0, 23.0, 15.0, 7.5):
        k.mesh(f"{name}_ring{int(R)}", _torus(R, 0.7, 64, 6), wire, (0, gy, hz), g, smooth_shade=True).rotation_euler = (math.pi / 2, 0, 0)
    for i in range(8):
        a = i * math.pi / 8
        sp = k.box(f"{name}_spoke{i}", (62.0, 0.9, 0.9), (0, gy, hz), wire, g)
        sp.rotation_euler = (0, -a, 0)
    # rear ring + short struts joining front guard and motor
    k.mesh(name + "_ringb", _torus(31.0, 0.7, 64, 6), wire, (0, 6 + 3.0, hz), g, smooth_shade=True).rotation_euler = (math.pi / 2, 0, 0)
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        s = k.box(f"{name}_strut{i}", (0.9, 17.0, 0.9), (31.0 * math.cos(a), gy / 2 + 4.5 - 0.5, hz + 31.0 * math.sin(a)), wire, g)
    blades = k.empty(name + "_blades", (0, -3.0, hz), g)
    k.cyl(name + "_hub", 5.0, 5.0, (0, 0, 0), dark, blades, segs=32).rotation_euler = (math.pi / 2, 0, 0)
    for i in range(5):
        arm = k.empty(f"{name}_arm{i}", (0, 0, 0), blades)
        arm.rotation_euler = (0, i * 2 * math.pi / 5, 0)
        bl = k.box(f"{name}_blade{i}", (9.0, 0.9, 20.0), (0, 0, 5 + 10.0), accent, arm, bevel=0.3)
        bl.rotation_euler = (0, 0, math.radians(18))

    def set_spin(angle):
        blades.rotation_euler = (0, float(angle), 0)

    set_spin(0.0)
    cab = k.cyl(name + "_cable", 1.2, 30.0, (0, 6 + 15.0, 1.6), k.mat("p17_cable", "#15171c", 0.6), g, segs=12)
    cab.rotation_euler = (math.pi / 2, 0, 0)
    cab_end = at + Vector((0, 6 + 30.0, 1.6)) * scale
    return {"group": g, "set_spin": set_spin, "cable_start": cab_end, "top": at + Vector((0, 0, hz + 40)) * scale,
            "centre": at + Vector((0, -3.0, hz)) * scale}


def relay_cutaway(k, at, name="relay_cut"):
    """Transparent relay cube (XZ view): coil + core, pivoting arm, NO contact below, NC contact above."""
    from parts_ep12 import _emit_val_mat
    at = Vector(at)
    g = k.empty(name, at)
    S = 40.0
    glass = _blend(k.mat("p17_cut_glass", "#4d86e8", 0.1, coat=0.6, alpha=0.16))
    k.box(name + "_shell", (S, S * 0.75, S), (0, 0, S / 2), glass, g, bevel=0.5)
    frame = k.mat("p17_cut_frame", "#9fc0f5", 0.3)
    for x in (-S / 2, S / 2):
        for y in (-S * 0.375, S * 0.375):
            k.box(name + "_edge", (0.8, 0.8, S), (x, y, S / 2), frame, g)
    for y in (-S * 0.375, S * 0.375):
        for z in (0.4, S - 0.4):
            k.box(name + "_edgex", (S, 0.8, 0.8), (0, y, z), frame, g)
    for x in (-S / 2, S / 2):
        for z in (0.4, S - 0.4):
            k.box(name + "_edgey", (0.8, S * 0.75, 0.8), (x, 0, z), frame, g)
    iron = k.mat("p17_cut_iron", "#8b93a1", 0.3, metal=1.0)
    copper = k.mat("p17_cut_copper", "#c8692f", 0.3, metal=1.0)
    k.box(name + "_plate", (S - 2, S * 0.75 - 2, 1.2), (0, 0, 1.1), k.mat("p17_cut_plate", "#232a38", 0.5), g)
    cx = 3.0
    k.cyl(name + "_core", 2.6, 22.0, (cx, 0, 12.5), iron, g, segs=24)
    k.cyl(name + "_coil", 7.0, 15.0, (cx, 0, 10.0), copper, g, segs=40)
    for z in (3.0, 17.0):
        k.cyl(name + "_flange", 8.0, 1.0, (cx, 0, z), k.mat("p17_cut_flange", "#3a4254", 0.5), g, segs=40)
    # fixed contacts at x = -17: NO post from the floor, NC bracket from the roof
    fx = -17.0
    k.box(name + "_no_post", (4.0, 4.0, 20.0), (fx, 0, 11.0), iron, g)
    k.box(name + "_no_pad", (5.0, 4.0, 1.2), (fx, 0, 21.6), k.mat("p17_cut_pad", "#e9c98a", 0.25, metal=1.0), g)
    k.box(name + "_nc_post", (4.0, 4.0, 5.0), (fx, 0, S - 2.5 - 0.6), iron, g)
    k.box(name + "_nc_pad", (5.0, 4.0, 1.2), (fx, 0, 33.2 + 0.0), k.mat("p17_cut_pad", "#e9c98a", 0.25, metal=1.0), g)
    # moving arm: hinge at (17, 0, 26), extends toward -X
    hinge = Vector((17.0, 0.0, 26.0))
    k.box(name + "_hinge_post", (4.0, 6.0, 25.0), (hinge.x + 2.5, 0, 13.0), iron, g)
    arm = k.empty(name + "_arm", hinge, g)
    L = 34.0
    k.box(name + "_arm_bar", (L, 5.0, 1.6), (-L / 2, 0, 0), k.mat("p17_cut_arm", "#cfd5df", 0.25, metal=1.0), arm, bevel=0.2)
    k.box(name + "_arm_tip", (4.5, 5.0, 2.6), (-L + 1.0, 0, 0), k.mat("p17_cut_pad", "#e9c98a", 0.25, metal=1.0), arm)
    k.cyl(name + "_pivot", 1.8, 6.5, (0, 0, 0), iron, arm, segs=16).rotation_euler = (math.pi / 2, 0, 0)
    th0, th1 = math.radians(9.0), math.radians(-6.0)

    def set_arm(t):
        t = max(0.0, min(1.0, t))
        arm.rotation_euler = (0, th0 + (th1 - th0) * t, 0)

    set_arm(0.0)
    sm, sval = _emit_val_mat(name + "_spark", "#ffe08a", 10.0)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=2.4)
    k.mesh(name + "_spark", bm, sm, (fx, 0, 23.6), g, smooth_shade=True)

    def set_spark(level):
        sval.outputs[0].default_value = max(0.0, min(1.0, level))

    set_spark(0.0)
    return {"group": g, "set_arm": set_arm, "set_spark": set_spark, "no": at + Vector((fx, 0, 22.2)),
            "nc": at + Vector((fx, 0, 33.2)), "coil": at + Vector((cx, 0, 10.0)), "top": at + Vector((0, 0, S + 8))}
