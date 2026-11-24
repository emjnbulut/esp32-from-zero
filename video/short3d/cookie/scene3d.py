"""Blender shots of the cookie-jar-guard Short (vertical 1080x1920), driven by story.py. Language: env COOKIE_LANG.

    blender -b -P video/short3d/cookie/scene3d.py -- --lang en --shot catch          # all frames of one shot (resumable)
    blender -b -P video/short3d/cookie/scene3d.py -- --lang en --stills hook,catch   # 3 stills per shot -> build/<lang>/stills/
    blender -b -P video/short3d/cookie/scene3d.py -- --lang en --at 1.0,12.0         # stills at global times

One Blender process per shot (make.py does that): a process that renders thousands of frames grows in memory.
Output: build/<lang>/shots/<id>/f_0001.png ... + anchors.json (projected buzzer / OLED / tags per frame).
Circuit + props = the Episode 11 shot script exactly (video/ep11/b3d/ep11_3d.py; pbl layout, front board F, back B):
  Ep 10: B4e->B r+ 4 (3V3)  B5d->B r- 5 (GND)  OLED B34f..37f, B34j->r- 34, B35j->r+ 35  B17e->B36h green SCL (D22)
         B14e->B37g blue SDA (D21)  button B24/26 e,f; B13d->B24d yellow (D19); B26j->r- 26
         buzzer F30c(+)/F33c; F13i->F30a orange (D32); F5h->F l- 5 (GND); F33a->F l- 33
  PIR legs B50e VCC, B51e OUT, B52e GND (video/b3d/parts_pir.py, dy=12, 9 lens windows, spread 110, reach 160)
         F4h (VIN) -> F l+ 4 red;  F l+ 50 -> B50b red;  F l- 52 -> B52b black;  F12h (D33) -> B51d purple
  props (video/b3d/parts_ep11.py): warm hand (scale 0.6), cookie jar at (118, -98) r 12 h 30, thumbs icon (130, 24, 30)
"""
import json
import math
import os
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
import parts_ep11 as px  # noqa: E402
import parts_pir  # noqa: E402
import pbl  # noqa: E402
from pbl import MM, lin, smooth  # noqa: E402
import story as S  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default


ST = S.Story(opt("--lang"))
FPS = S.FPS
OUT = ST.B
V = Vector

# ======================================================================= scene (= video/ep11/b3d/ep11_3d.py)
k = pbl.Kit(fps=FPS, res=(1080, 1920))
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32", "D33", "VIN"})
usb = k.usb_cable()
cam, tgt = k.camera(lens=26, fstop=10.0)
oled = k.oled(B, (34, 35, 36, 37), "f")
btn = k.button([B.hole(24, "e"), B.hole(26, "e"), B.hole(24, "f"), B.hole(26, "f")])
bz = k.buzzer(F.hole(30, "c"), F.hole(33, "c"))
xray = k.buzzer_xray()
pir = parts_pir.pir(k, [B.hole(50, "e"), B.hole(51, "e"), B.hole(52, "e")], dy=12.0)
dome_xray = px.dome_xray(k, pir)
BEAMS = parts_pir.zones(k, pir, n=9, spread=110.0, reach=160.0, tilt=16.0)
W = {}
W["pwr_red"] = k.wire(B.hole(4, "e"), B.rail(4, "r", "+"), "red", name="pwr_red")
W["pwr_blk"] = k.wire(B.hole(5, "d"), B.rail(5, "r", "-"), "black", name="pwr_blk")
W["oled_gnd"] = k.wire(B.hole(34, "j"), B.rail(34, "r", "-"), "black", name="oled_gnd")
W["oled_vcc"] = k.wire(B.hole(35, "j"), B.rail(35, "r", "+"), "red", name="oled_vcc")
W["scl"] = k.wire(B.hole(17, "e"), B.hole(36, "h"), "green", h=9, name="scl")
W["sda"] = k.wire(B.hole(14, "e"), B.hole(37, "g"), "blue", h=11, name="sda")
W["btn"] = k.wire(B.hole(13, "d"), B.hole(24, "d"), "yellow", h=5, name="btn")
W["btn_gnd"] = k.wire(B.hole(26, "j"), B.rail(26, "r", "-"), "black", name="btn_gnd")
W["bz"] = k.wire(F.hole(13, "i"), F.hole(30, "a"), "orange", h=7, name="bz")
W["bz_gnd1"] = k.wire(F.hole(5, "h"), F.rail(5, "l", "-"), "black", name="bz_gnd1")
W["bz_gnd2"] = k.wire(F.hole(33, "a"), F.rail(33, "l", "-"), "black", name="bz_gnd2")
W["pir_vin"] = k.wire(F.hole(4, "h"), F.rail(4, "l", "+"), "red", name="pir_vin")
W["pir_vcc"] = k.wire(F.rail(50, "l", "+"), B.hole(50, "b"), "red", h=8, name="pir_vcc")
W["pir_gnd"] = k.wire(F.rail(52, "l", "-"), B.hole(52, "b"), "black", h=8, name="pir_gnd")
W["pir_out"] = k.wire(F.hole(12, "h"), B.hole(51, "d"), "purple", h=13, name="pir_out",
                      via=[(-11.0, -25.0), (66.0, -25.0), (83.82, -3.0)])
for w in W.values():
    w["draw"](1.0)
HAND = px.warm_hand(k, scale=0.6)
JAR = px.cookie_jar(k, (118, -98, 0), r=12.0, h=30.0)
THUMB = px.thumb(k, (130, 24, 30))
k.lights(center=(0.045, 0.0, 0.0), key=2.2)
k.glare(threshold=2.5)
sc = k.scene
OUT_MAT = k.mats["wire_purple"].node_tree.nodes["Principled BSDF"]
OUT_MAT.inputs["Emission Color"].default_value = (*lin("#c9a6ff"), 1)
xray(0.0)

PINS = pir["pins"]
LEG_TOP = V((0, 0, 5.0))
OC = oled["center"]
BT = btn["top"]
BZ = bz["top"]
PT = pir["top"]
CENTER = V((40, 0, 0))
FRONT = V((46, -2, 10))  # the desk-front framing: OLED, button, buzzer and the PIR all in view
BEAM_BASE = PT - V((0, 0, 3.0))
PRESS_Z = btn["press"].location.z
THUMB0 = THUMB["group"].location.copy()
TAGAT = {"pir": PT, "oled": OC + V((0, 4, 0)), "buzzer": BZ, "button": BT, "out": PINS["OUT"] + LEG_TOP, "dome": PT}
TAGCOL = {"pir": "#ffb547", "oled": "#2dd4bf", "buzzer": "#ff8a2a", "button": "#f2c037", "out": "#b48cff", "dome": "#ffb547"}


def vis(group, on):
    for o in [group] + list(group.children_recursive):
        o.hide_render = not on


# ======================================================================= ep11 helpers (same maths)
def beam_of(p):
    """index of the lens window (beam wedge) that sees point p, or None"""
    d = V(p) - BEAM_BASE
    if d.length > 185 or d.y > -5:
        return None
    ang = math.degrees(math.atan2(d.x, -d.y))
    i = int((ang + 55.0) // (110.0 / 9))
    return i if 0 <= i < 9 else None


def place_hand(pos, yaw, pitch=0.0):
    g = HAND["group"]
    g.location = pos
    g.rotation_euler = (0, pitch, yaw)


def hand_point(pos, yaw):
    return V(pos) + V((math.cos(yaw), math.sin(yaw), 0)) * 24


def hand_path(keys):
    """keys: [(t, pos, yaw)] -> f(t) = (pos, yaw), eased (global times)"""
    def f(t):
        if t <= keys[0][0]:
            return keys[0][1], keys[0][2]
        for (t0, p0, y0), (t1, p1, y1) in zip(keys, keys[1:]):
            if t <= t1:
                u = smooth((t - t0) / max(1e-6, t1 - t0))
                return p0.lerp(p1, u), y0 + (y1 - y0) * u
        return keys[-1][1], keys[-1][2]
    return f


def lit_by_path(path, t, tail=0.6):
    """windows lit by a moving warm hand: the window it is in now at full, the ones it just left fading"""
    lit = {}
    for j in range(13):
        s = t - tail * j / 12
        pos, yaw = path(s)
        i = beam_of(hand_point(pos, yaw))
        if i is not None:
            lit[i] = max(lit.get(i, 0.0), 1.0 - j / 12)
    return lit


def CATCH_KEYS(t0, tc, t_end, t_in):
    """ep11 CATCH_KEYS in global time: the warm hand sneaks in from the right toward the jar lid (crossing lens
    windows 8 -> 5), freezes when the alarm goes off at tc, then pulls back"""
    return [(t0, V((330, -120, 48)), math.pi), (t_in, V((300, -118, 48)), math.pi),
            (tc - 0.05, V((168, -100, 46)), math.pi + 0.05), (tc + 0.25, V((164, -100, 47)), math.pi + 0.05),
            (tc + 1.0, V((188, -106, 50)), math.pi), (max(t_end, tc + 1.1), V((205, -110, 52)), math.pi)]


def cam_path(keys):
    """keys: [(t, pos, target, lens)] -> f(t) with smoother easing (global times)"""
    def f(t):
        if t <= keys[0][0]:
            return keys[0][1:]
        for (t0, p0, q0, l0), (t1, p1, q1, l1) in zip(keys, keys[1:]):
            if t <= t1:
                u = (t - t0) / max(1e-6, t1 - t0)
                u = u * u * u * (u * (u * 6 - 15) + 10)
                return p0.lerp(p1, u), q0.lerp(q1, u), l0 + (l1 - l0) * u
        return keys[-1][1:]
    return f


# ======================================================================= per-shot plan (global times)
SH = ST.S
hook, arm, catch, ago = SH["hook"], SH["arm"], SH["catch"], SH["ago"]
lens_s, yes_s, stamp_s, parts_s, cta_s = SH["how_lens"], SH["how_yes"], SH["how_stamp"], SH["parts"], SH["cta"]

PATH = {
    "hook": hand_path([(0.0, V((265, -114, 48)), math.pi), (ST.H_CATCH - 0.05, V((168, -100, 46)), math.pi + 0.05),
                       (ST.H_CATCH + 0.25, V((164, -100, 47)), math.pi + 0.05), (ST.H_CATCH + 1.0, V((188, -106, 50)), math.pi),
                       (hook["end"] + 0.5, V((205, -110, 52)), math.pi)]),
    "catch": hand_path(CATCH_KEYS(catch["start"], ST.TC, catch["end"], max(catch["start"] + 0.2, ST.word("sneak") - 0.2))),
    "how_yes": hand_path([(yes_s["start"], V((190, -72, 36)), math.pi), (ST.MOVES - 0.15, V((190, -72, 36)), math.pi),
                          (ST.YES + 1.2, V((50, -72, 36)), math.pi), (yes_s["end"] + 1, V((30, -72, 36)), math.pi)]),
    "how_stamp": hand_path([(stamp_s["start"], V((300, -116, 48)), math.pi), (ST.STAMP - 0.05, V((172, -100, 46)), math.pi + 0.05),
                            (ST.STAMP + 0.3, V((168, -100, 47)), math.pi + 0.05), (stamp_s["end"] + 0.5, V((200, -108, 51)), math.pi)]),
}

def view(tgt_, dist, elev, az=0.0):
    """camera position at `dist` mm from tgt_, `elev` degrees above the desk, `az` degrees right of straight-on (-Y)"""
    e, z = math.radians(elev), math.radians(az)
    return V(tgt_) + V((dist * math.cos(e) * math.sin(z), -dist * math.cos(e) * math.cos(z), dist * math.sin(e)))


def K(t, tg, dist, elev, az=0.0, lens=25.0):
    return (t, view(tg, dist, elev, az), V(tg), lens)


# portrait framing: the action sits in the middle of the frame (titles above, captions below), seen from ~55 degrees
JARV = V((98, -30, 10))  # between the jar and the PIR, shifted back so the circuit sits under the titles
CAMS = {
    "hook": cam_path([K(0.0, JARV, 262, 52, 50), K(hook["end"], JARV + V((-4, 2, 0)), 232, 50, 44)]),
    "arm": cam_path([K(arm["start"], V((50, -10, 8)), 230, 56, -4), K(ST.PRESS + 0.5, OC + V((0, -14, 0)), 150, 55, -2),
                     K(arm["end"], OC + V((0, -6, 0)), 90, 54, 0)]),
    "catch": cam_path([K(catch["start"], JARV + V((-6, 0, 0)), 258, 54, 40), K(catch["end"], JARV, 228, 50, 48)]),
    "ago": cam_path([K(ago["start"], OC + V((0, -4, 0)), 100, 52, -4), K(ago["end"], OC + V((0, -2, 0)), 68, 50, 0)]),
    "how_lens": cam_path([K(lens_s["start"], PT + V((0, -6, -3)), 115, 38, -16), K(ST.WIN - 0.3, PT + V((0, -6, -3)), 90, 40, -12),
                          K(ST.WIN + 1.3, PT + V((0, -62, -12)), 300, 72, -4), K(lens_s["end"], PT + V((0, -66, -12)), 315, 74, -2)]),
    "how_yes": cam_path([K(yes_s["start"], V((108, -30, 20)), 235, 52, 34), K(yes_s["end"], V((104, -26, 20)), 210, 50, 28)]),
    "how_stamp": cam_path([K(stamp_s["start"], V((74, -18, 8)), 265, 56, 36), K(stamp_s["end"], V((78, -18, 8)), 240, 54, 42)]),
    "parts": cam_path([K(parts_s["start"], V((50, -2, 0)), 245, 60, 28), K(parts_s["end"], V((54, 0, 0)), 222, 58, 36)]),
}


def cta_cam(T):
    u = (T - cta_s["start"]) / max(1e-6, cta_s["end"] - cta_s["start"])
    c = V((40.0, 34.0, 0.0))  # aimed a little behind the circuit: it sits under the follow card
    return view(c, 260, 62, 20 + 40 * u), c, 25.0


FSTOP = {"ago": 22.0, "how_lens": 16.0}


def apply(T):
    sid = ST.shot_at(T)["id"]
    btn["press"].location.z = PRESS_Z + ST.press_dz(T)
    k.set_screen(ST.screen(T))
    vis(HAND["group"], sid in PATH)
    vis(JAR["group"], sid in ("hook", "catch", "how_stamp"))
    vis(THUMB["group"], False)
    dome_xray(0.0)
    zones, idle, glow = {}, 0.0, 0.0
    px.set_heat(HAND, 0.55)
    if sid in PATH:
        path = PATH[sid]
        pos, yaw = path(T)
        place_hand(pos, yaw, 0.05 if sid == "how_yes" else 0.08)
        zones = lit_by_path(path, T)
    if sid == "hook":
        idle = 0.05 if T < ST.H_CATCH else 0.0
        glow = S.fade(T, ST.H_CATCH - 0.05, 99, 0.1)
    elif sid == "catch":
        idle = 0.05 if T < ST.TC else 0.0
        glow = S.fade(T, ST.TC - 0.05, 99, 0.1)
    elif sid == "how_stamp":
        idle = 0.05 if T < ST.STAMP else 0.0
        glow = S.fade(T, ST.STAMP - 0.05, 99, 0.1)
    elif sid == "arm":
        left = ST.countdown_left(T)
        if left == 0:
            idle = 0.05
    elif sid == "how_lens":
        dome_xray(1.0 if T >= ST.word("motion") - 0.2 else 0.0)
        zones = {}
        for i in range(9):  # the windows appear one by one on "windows"
            zones[i] = 0.4 * S.smooth((T - (ST.WIN + 0.1 * i)) / 0.25)
        t_each = ST.WIN + 1.0
        if T >= t_each:  # each one looks at its own slice: a bright one sweeps across
            j = int((T - t_each) / 0.22) % 9
            zones[j] = 1.0
    elif sid == "how_yes":
        px.set_heat(HAND, 0.8)
        idle = 0.03
        hi = T >= ST.YES
        glow = 1.0 if hi else 0.0
        up = S.smooth((T - ST.YES) / 0.35)
        vis(THUMB["group"], T >= ST.YES - 0.05)
        THUMB["set"](1.0, "#2fbf71")
        THUMB["group"].location = THUMB0 + V((0, 0, -12 * (1 - up) + 2.0 * math.sin(T * 2.2)))
        THUMB["group"].scale = (0.4 + 0.6 * up,) * 3
    elif sid in ("parts", "cta"):
        idle = 0.04 + 0.03 * math.sin(T * 2.5)
    parts_pir.set_zones(BEAMS, zones, idle=idle)
    OUT_MAT.inputs["Emission Strength"].default_value = 4.0 * glow
    if sid == "cta":
        p, q, lens = cta_cam(T)
    else:
        p, q, lens = CAMS[sid](T)
    cam.location = V(p) * MM
    tgt.location = V(q) * MM
    cam.data.lens = lens
    cam.data.dof.aperture_fstop = FSTOP.get(sid, 10.0)


def proj(v):
    a = world_to_camera_view(sc, cam, V(v) * MM)
    return [round(a.x, 4), round(1 - a.y, 4)] if a.z > 0 else None


def anchors(T):
    d = {"buzzer": proj(BZ), "oled": proj(OC), "button": proj(BT), "pir": proj(PT), "jar": proj(JAR["top"]),
         "chip": proj(V((-6.7, 0.0, 9.0)))}
    tags = []
    for name, (on, text) in ST.tags(T).items():
        if on > 0.02:
            lift = 14 if name in ("out", "dome") else 10
            a, b = proj(TAGAT[name]), proj(TAGAT[name] + V((0, 0, lift)))
            if a and b:
                tags.append({"text": text, "color": TAGCOL[name], "on": round(on, 3), "scale": 1.0, "a": a, "b": b})
    d["tags"] = tags
    return d


sc.render.image_settings.file_format = "PNG"
REDO = "--redo" in argv


def render_frame(T, path):
    apply(T)
    bpy.context.view_layer.update()
    a = anchors(T)
    if path and (REDO or not os.path.exists(path)):
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
    return a


if opt("--at"):
    os.makedirs(os.path.join(OUT, "stills"), exist_ok=True)
    for x in opt("--at").split(","):
        T = float(x)
        p = os.path.join(OUT, "stills", f"at_{T:06.2f}.png")
        if os.path.exists(p):
            os.remove(p)
        render_frame(T, p)
elif opt("--stills"):
    os.makedirs(os.path.join(OUT, "stills"), exist_ok=True)
    for sid in opt("--stills").split(","):
        sh = ST.S[sid]
        for f in sorted({1, sh["n"] // 2 + 1, sh["n"]}):
            T = (sh["F0"] + f - 1) / FPS
            p = os.path.join(OUT, "stills", f"{sid}_f_{f:04d}.png")
            if os.path.exists(p):
                os.remove(p)
            render_frame(T, p)
else:
    sid = opt("--shot")
    sh = ST.S[sid]
    d = os.path.join(OUT, "shots", sid)
    os.makedirs(d, exist_ok=True)
    anc = {}
    ONLYF = {int(x) for x in opt("--frames").split(",")} if opt("--frames") else None  # re-render just these (broken files)
    for f in range(1, sh["n"] + 1):
        T = (sh["F0"] + f - 1) / FPS
        p = os.path.join(d, f"f_{f:04d}.png")
        if ONLYF and f not in ONLYF:
            continue
        if ONLYF:
            REDO = True
        anc[str(f)] = render_frame(T, p)
        print("frame", sid, f, "/", sh["n"], flush=True)
    if not ONLYF:
        json.dump({"F0": sh["F0"], "n": sh["n"], "frames": anc}, open(os.path.join(d, "anchors.json"), "w"))
    print("done", sid)
