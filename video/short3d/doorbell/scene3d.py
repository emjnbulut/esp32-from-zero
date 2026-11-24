"""Blender shots of the phone-doorbell Short (vertical 1080x1920), driven by story.py. Language: env DOORBELL_LANG.

    blender -b -P video/short3d/doorbell/scene3d.py -- --lang en --shot send          # all frames of one shot (resumable)
    blender -b -P video/short3d/doorbell/scene3d.py -- --lang en --at 1.0,12.0       # stills at global times

One Blender process per shot (make.py does that). Output: build/<lang>/shots/<id>/f_0001.png ... + anchors.json
(projected buzzer / OLED / LED / phone / packet / tags per frame).
Circuit + props = the Episode 12 shot script (video/ep12/b3d/ep12_3d.py; pbl layout, front board F, back board B):
  Ep 10: B4e->B r+ 4 (3V3)  B5d->B r- 5 (GND)  OLED B34f..37f, B34j->r- 34, B35j->r+ 35  B17e->B36h green SCL (D22)
         B14e->B37g blue SDA (D21)  button B24/26 e,f; B13d->B24d yellow (D19); B26j->r- 26
         buzzer F30c(+)/F33c; F13i->F30a orange (D32); F5h->F l- 5 (GND); F33a->F l- 33
  RGB LED legs F22b R / F23b - / F24b G / F25b B, 220 ohm F22e-f, F24e-f, F25e-f,
         F11h->F22h red (D25), F10g->F24g green (D26), F9i->F25i blue (D27), F23a->F l- 23 black
  props (video/b3d/parts_ep12.py): phone on its stand, antenna glow, radio ripples, travelling packet, router.
  The phone stands in FRONT of the board's right half (Ep 12: to the right of the board) so the phone and the
  board stack up in the tall frame; its screens are the Ep 12 images (video/ep12/b3d/phone_screens.py).
"""
import json
import math
import os
import subprocess
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EP12 = os.path.join(ROOT, "video", "ep12", "b3d")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "video", "b3d"))
sys.path.insert(0, EP12)
import parts_ep12 as p12  # noqa: E402
import pbl  # noqa: E402
import phone_screens as PS  # noqa: E402
from pbl import MM, smooth  # noqa: E402
import story as S  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default


ST = S.Story(opt("--lang"))
FPS = S.FPS
OUT = ST.B
V = Vector

# phone screen images (PIL, the Ep 12 script's own; regenerated in the venv when missing)
PHONE_DIR = os.path.join(EP12, "build", "phone")
if not all(os.path.exists(os.path.join(PHONE_DIR, s + ".png")) for s in PS.STATES):
    subprocess.run([os.path.join(ROOT, ".venv", "Scripts", "python.exe"), os.path.join(EP12, "phone_screens.py")], check=True)

# ======================================================================= scene (= video/ep12/b3d/ep12_3d.py)
k = pbl.Kit(fps=FPS, res=(1080, 1920))
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32", "D25", "D26", "D27"})
usb = k.usb_cable()
cam, tgt = k.camera(lens=26, fstop=18.0)
oled = k.oled(B, (34, 35, 36, 37), "f")
btn = k.button([B.hole(24, "e"), B.hole(26, "e"), B.hole(24, "f"), B.hole(26, "f")])
bz = k.buzzer(F.hole(30, "c"), F.hole(33, "c"))
xray = k.buzzer_xray()
rgb = k.rgb_led([F.hole(22, "b"), F.hole(23, "b"), F.hole(24, "b"), F.hole(25, "b")])
RES = {"res_r": k.resistor(F.hole(22, "e"), F.hole(22, "f"), name="res_r"),
       "res_g": k.resistor(F.hole(24, "e"), F.hole(24, "f"), name="res_g"),
       "res_b": k.resistor(F.hole(25, "e"), F.hole(25, "f"), name="res_b")}
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
W["rgb_r"] = k.wire(F.hole(11, "h"), F.hole(22, "h"), "red", h=6, name="rgb_r")
W["rgb_g"] = k.wire(F.hole(10, "g"), F.hole(24, "g"), "green", h=8, name="rgb_g")
W["rgb_b"] = k.wire(F.hole(9, "i"), F.hole(25, "i"), "blue", h=10, name="rgb_b")
W["rgb_k"] = k.wire(F.hole(23, "a"), F.rail(23, "l", "-"), "black", name="rgb_k")
for w in W.values():
    w["draw"](1.0)
ANTG = p12.antenna_glow(k)
ANT = ANTG["centre"]
PHONE = p12.phone(k, (80, -114, 0), tilt_deg=66.0, yaw_deg=-6.0)
ROUTER = p12.router(k, (150, 70, 0))
RIP_B = p12.ripples(k, ANT, "#7fe8de", n=4, half=True, name="ripb")
RIP_P = p12.ripples(k, PHONE["top"](), "#ffd166", n=4, half=False, name="ripp")
RIP_R = p12.ripples(k, ROUTER["top"], "#c3cbd7", n=4, half=False, name="ripr")
PKT = p12.packet(k)
k.lights(center=(0.045, -0.04, 0.0), key=2.2)
k.glare(threshold=2.5)
sc = k.scene
IMG = {s: bpy.data.images.load(os.path.join(PHONE_DIR, s + ".png"), check_existing=True) for s in PS.STATES}
xray(0.0)

OC = oled["center"]
BT = btn["top"]
BZ = bz["top"]
LED = rgb["top"]
ESPC = V((-17, 0, 14))
PTOP = PHONE["top"]()
SCRC = PHONE["world"](0.5, 0.5)
SN = (PHONE["group"].matrix_world.to_3x3() @ V((0, 0, 1))).normalized()  # screen normal
PRESS_Z = btn["press"].location.z
TAGAT = {"rgb": LED, "oled": OC + V((0, 4, 0)), "buzzer": BZ}
TAGCOL = {"rgb": "#ff6b8b", "oled": "#2dd4bf", "buzzer": "#ff8a2a"}


def vis(group, on):
    for o in [group] + list(group.children_recursive):
        o.hide_render = not on


def tapw(key):
    u, v = PS.TAPS[key]
    return PHONE["world"](u, v) + SN * 0.6


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


def view(tgt_, dist, elev, az=0.0):
    """camera position at `dist` mm from tgt_, `elev` degrees above the desk, `az` degrees right of straight-on (-Y)"""
    e, z = math.radians(elev), math.radians(az)
    return V(tgt_) + V((dist * math.cos(e) * math.sin(z), -dist * math.cos(e) * math.cos(z), dist * math.sin(e)))


def K(t, tg, dist, elev, az=0.0, lens=25.0):
    return (t, view(tg, dist, elev, az), V(tg), lens)


def phone_k(t, dist=150.0, up=0.0, side=0.0, lens=26.0):
    """camera square on the phone screen (the board shows behind it)"""
    return (t, SCRC + SN * dist + V((side, 0, up)), SCRC + V((0, 0, 4.0)), lens)


# ======================================================================= cameras (portrait: phone low, board above)
SH = ST.S
hook, noapp, wifi, join, send = SH["hook"], SH["noapp"], SH["wifi"], SH["join"], SH["send"]
colors, parts, cta = SH["colors"], SH["parts"], SH["cta"]
DESK = V((46, -54, 20))  # the board with the phone in front of its right half
BOARD = V((26, -14, 10))  # OLED, buzzer, RGB LED
r_fly = ST.RING.t + 0.3
CAMS = {
    "hook": cam_path([K(0.0, DESK, 232, 46, -2), K(hook["end"], DESK + V((0, 4, 0)), 212, 47, 2)]),
    "noapp": cam_path([K(noapp["start"], V((78, -6, 16)), 300, 40, 2), K(noapp["end"], V((72, -12, 16)), 280, 42, -2)]),
    "wifi": cam_path([K(wifi["start"], ESPC + V((10, -6, 0)), 170, 40, -18),
                      K(ST.word("own"), ESPC + V((20, -10, 0)), 200, 44, -16),
                      K(wifi["end"], DESK, 215, 46, -2)]),
    "join": cam_path([phone_k(join["start"], 125, 6, -6), phone_k(join["end"], 108, 4, -2)]),
    "send": cam_path([phone_k(send["start"], 118, 6, -4), phone_k(r_fly, 112, 6, -4),
                      K(r_fly + 0.5 * (ST.RING.arrive - r_fly), DESK, 215, 46, -2),
                      K(ST.RING.arrive - 0.15, BOARD, 175, 48, -6), K(send["end"], BOARD + V((2, 2, 0)), 160, 50, -4)]),
    "colors": cam_path([K(colors["start"], DESK, 212, 46, -2), K(ST.word("counts") - 0.5, DESK + V((-6, 8, 0)), 195, 47, -2),
                        K(colors["end"], OC + V((0, -6, 0)), 95, 52, -4)]),
    "parts": cam_path([K(parts["start"], V((34, -10, 0)), 215, 58, -6), K(parts["end"], V((38, -8, 0)), 195, 58, 4)]),
}


def cta_cam(T):
    u = (T - cta["start"]) / max(1e-6, cta["end"] - cta["start"])
    c = V((48.0, -18.0, 0.0))  # board + phone under the follow card
    return view(c, 330, 58, -18 + 30 * u), c + V((0, 30, 0)), 25.0


FSTOP = {"join": 14.0, "colors": 18.0}


def apply(T):
    sid = ST.shot_at(T)["id"]
    btn["press"].location.z = PRESS_Z
    scr, led = ST.device(T)
    k.set_screen(scr)
    rgb["set"](led, 1.0 if any(led) else 0.0)
    ph, pressed = ST.phone(T)
    PHONE["set_screen"](IMG[ph])
    PHONE["set_tap"](0.5, 0.5, 0.0, -1)
    for c in ST.cmds(T):  # the finger-tap dot on the pressed button
        age = T - c.t
        if -0.05 <= age <= 0.35:
            u, v = PS.TAPS[c.key]
            PHONE["set_tap"](u, v, 1.0 - max(0.0, age) / 0.35, age)
    if sid == "join" and ST.J_TAP - 0.05 <= T <= ST.J_TAP + 0.35:
        u, v = PS.TAPS["wifi_net"]
        PHONE["set_tap"](u, v, 1.0 - max(0.0, T - ST.J_TAP) / 0.35, T - ST.J_TAP)
    # router: only in the "no router" shot, it shrinks away on "router"
    gone = smooth((T - ST.word("router")) / 0.6) if sid == "noapp" else 1.0
    vis(ROUTER["group"], sid == "noapp" and gone < 0.98)
    ROUTER["group"].scale = (max(0.02, 1 - gone),) * 3
    RIP_R["off"]()
    if sid == "noapp" and T < ST.word("router"):
        RIP_R["set"](T, noapp["start"], level=0.7, period=1.3, rmax=80, centre=ROUTER["top"])
    # the board's own Wi-Fi: ripples from the antenna (strong in the wifi shot, faint elsewhere)
    ANTG["set"](0.0)
    RIP_P["off"]()
    if sid == "noapp":
        RIP_B["off"]()
    elif sid == "wifi":
        tw = ST.word("wifi")
        RIP_B["set"](T, tw - 0.2, level=0.75, period=1.3, rmax=90)
        ANTG["set"](smooth((T - tw + 0.2) / 0.4) * (0.75 + 0.25 * math.sin(T * 6)))
    elif sid == "join":
        RIP_B["set"](T, join["start"] - 1.0, level=0.35, period=1.6, rmax=80)
        if T >= ST.J_TAP:
            RIP_P["set"](T, ST.J_TAP, level=0.3, period=1.3, rmax=32, centre=PTOP)
    else:
        RIP_B["set"](T, -10.0, level=0.22, period=1.6, rmax=90)
    # the link in the air: packet + trail along the phone -> antenna arc, the antenna flashes when it lands
    pk = ST.packet(T)
    pos = None
    if pk:
        c, u = pk
        path = p12.arc_path(tapw(c.key), ANT, lift=60 if c.fly > 0.5 else 40)
        pos = path(u)
        PKT["set"](pos, [path(u - 0.035 * (j + 1)) if u - 0.035 * (j + 1) > 0 else None for j in range(5)])
    else:
        PKT["set"](None)
    for c in ST.cmds(T):
        if c.arrive <= T < c.arrive + 0.5:
            ANTG["set"](1.0 - (T - c.arrive) / 0.5)
    vis(PHONE["group"], sid not in ("parts",))
    if sid == "cta":
        p, q, lens = cta_cam(T)
    else:
        p, q, lens = CAMS[sid](T)
    cam.location = V(p) * MM
    tgt.location = V(q) * MM
    cam.data.lens = lens
    cam.data.dof.aperture_fstop = FSTOP.get(sid, 18.0)
    return pos


def proj(v):
    a = world_to_camera_view(sc, cam, V(v) * MM)
    return [round(a.x, 4), round(1 - a.y, 4)] if a.z > 0 else None


def anchors(T, pos):
    d = {"buzzer": proj(BZ), "oled": proj(OC), "led": proj(LED), "ant": proj(ANT), "phone": proj(PTOP),
         "screen": proj(SCRC), "packet": proj(pos) if pos is not None else None}
    tags = []
    for name, (on, text) in ST.tags(T).items():
        if on > 0.02:
            a, b = proj(TAGAT[name]), proj(TAGAT[name] + V((0, 0, 10)))
            if a and b:
                tags.append({"text": text, "color": TAGCOL[name], "on": round(on, 3), "scale": 1.0, "a": a, "b": b})
    d["tags"] = tags
    return d


sc.render.image_settings.file_format = "PNG"
REDO = "--redo" in argv


def render_frame(T, path):
    pos = apply(T)
    bpy.context.view_layer.update()
    a = anchors(T, pos)
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
