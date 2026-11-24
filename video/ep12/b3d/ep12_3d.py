"""Episode 12 (DRAFT) - every Blender 3D shot of "Control Your ESP32 from Your Phone", timed to the narration.

    blender -b -P video/ep12/b3d/ep12_3d.py -- [--shots open_tap,try_red] [--frames 1,40] [--stills] [--cycles]

Same pipeline as video/ep11/b3d/ep11_3d.py. Timing: video/ep12/build/schedule.json (EN narration, word times). A shot =
a run of consecutive segments whose vis is "b3d:<id>"; its length = from the first segment's start to the next
segment's start. Output: video/ep12/b3d/build/shots/<id>/f_0001.png ... + overlay.json/anchors.json per shot +
shots.json (start, frames, sfx events, beeps). --stills renders 3 frames per shot into build/stills/.
Phone screens: phone_screens.py (PIL, run in the repo venv automatically) -> build/phone/<state>.png.
OLED screens exactly as lessons/12-phone-control/code/phone_remote/phone_remote.ino prints them (show(): size-1 line
at (0,0), size-2 line at (0,28)): "open 192.168.4.1" / "READY", "command #N" / red|green|blue|off, "RING!";
the challenge (challenge_party) adds "PARTY!" and flashes red, green, blue three times, 200 ms each.
Ring = tone(1319, 180), delay(200), tone(1047, 300).
Circuit = the Ep 10 layout + the RGB LED of the treasure Short (no PIR):
  Ep 10: B4e->B r+ 4 (3V3)  B5d->B r- 5 (GND)  OLED B34f..37f, B34j->r- 34, B35j->r+ 35  B17e->B36h green SCL (D22)
         B14e->B37g blue SDA (D21)  button B24/26 e,f; B13d->B24d yellow (D19); B26j->r- 26
         buzzer F30c(+)/F33c; F13i->F30a orange (D32); F5h->F l- 5 (GND); F33a->F l- 33
  RGB LED legs F22b R / F23b - / F24b G / F25b B, 220 ohm F22e-f, F24e-f, F25e-f,
         F11h->F22h red (D25), F10g->F24g green (D26), F9i->F25i blue (D27), F23a->F l- 23 black
"""
import json
import math
import os
import re
import subprocess
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
EP = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EP))
sys.path.insert(0, os.path.join(EP, "..", "b3d"))
sys.path.insert(0, HERE)
import parts_ep12 as p12  # noqa: E402
import pbl  # noqa: E402
import phone_screens as PS  # noqa: E402
from oledfont import Screen  # noqa: E402
from pbl import MM, smooth  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default


ONLY = opt("--shots", "").split(",") if opt("--shots") else None
FRAMES = [int(x) for x in opt("--frames").split(",")] if opt("--frames") else None
STILLS = "--stills" in argv
FPS = 30
OUT = os.path.join(HERE, "build")


# ======================================================================= timing
def load_timing():
    script = json.load(open(os.path.join(EP, "script.json"), encoding="utf-8"))
    sched_p = os.path.join(EP, "build", "schedule.json")
    segs = {}
    if os.path.exists(sched_p):
        sch = json.load(open(sched_p, encoding="utf-8"))["segments"]
        for d in script["segments"]:
            x = sch[d["id"]]
            segs[d["id"]] = {"start": x["start"], "end": x["end"], "words": x["words"], "vis": d["vis"]}
    else:  # estimate
        t = 0.8
        for d in script["segments"]:
            ws = d["text"].split()
            dur = len(ws) / 2.45 + 0.25 * d["text"].count(",") + 0.35 * len(re.findall(r"[.!?]", d["text"]))
            words = [{"w": w, "t": dur * i / len(ws)} for i, w in enumerate(ws)]
            segs[d["id"]] = {"start": t, "end": t + dur, "words": words, "vis": d["vis"]}
            t += dur + d.get("pad", 0.35)
    order = [d["id"] for d in script["segments"]]
    shots = []
    for i, sid in enumerate(order):
        v = segs[sid]["vis"]
        if not v.startswith("b3d:"):
            continue
        name = v[4:]
        nxt = segs[order[i + 1]]["start"] if i + 1 < len(order) else segs[sid]["end"] + 1.5
        if shots and shots[-1]["id"] == name and shots[-1]["segs"][-1] == order[i - 1]:
            shots[-1]["segs"].append(sid)
            shots[-1]["end"] = nxt
        else:
            shots.append({"id": name, "segs": [sid], "start": segs[sid]["start"], "end": nxt})
    return segs, shots


SEGS, SHOTS = load_timing()


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_t(shot, word, nth=0, seg=None):
    """time of a spoken word, relative to the shot start (first match, or nth match)"""
    want = _norm(word)
    k = 0
    for sid in ([seg] if seg else shot["segs"]):
        s = SEGS[sid]
        for w in s["words"]:
            if _norm(w["w"]).startswith(want):
                if k == nth:
                    return s["start"] + w["t"] - shot["start"]
                k += 1
    raise KeyError(f"{shot['id']}: word {word!r} #{nth} not found")


# ======================================================================= phone screens (PIL runs in the venv)
PHONE_DIR = os.path.join(OUT, "phone")


def ensure_phone_screens():
    src = os.path.join(HERE, "phone_screens.py")
    pngs = [os.path.join(PHONE_DIR, s + ".png") for s in PS.STATES]
    if all(os.path.exists(p) and os.path.getmtime(p) >= os.path.getmtime(src) for p in pngs):
        return
    py = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
    subprocess.run([py if os.path.exists(py) else "python", src], check=True)


ensure_phone_screens()

# ======================================================================= scene
k = pbl.Kit(fps=FPS, engine="CYCLES" if "--cycles" in argv else "EEVEE")
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32", "D25", "D26", "D27"})
usb = k.usb_cable()
cam, tgt = k.camera(lens=50, fstop=10.0)
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
rings = k.sound_rings(bz["top"], 3)
ANTG = p12.antenna_glow(k)
ANT = ANTG["centre"]
PHONE = p12.phone(k, (152, -66, 0), tilt_deg=68.0, yaw_deg=-28.0)
ROUTER = p12.router(k, (150, 75, 0))
RIP_B = p12.ripples(k, ANT, "#7fe8de", n=4, half=True, name="ripb")
RIP_P = p12.ripples(k, PHONE["top"](), "#ffd166", n=4, half=False, name="ripp")
RIP_R = p12.ripples(k, ROUTER["top"], "#c3cbd7", n=4, half=False, name="ripr")
PKT = p12.packet(k)
k.lights(center=(0.045, -0.02, 0.0), key=2.2)
k.glare(threshold=2.5)
sc = k.scene
IMG = {s: bpy.data.images.load(os.path.join(PHONE_DIR, s + ".png"), check_existing=True) for s in PS.STATES}

TAGS = {}


def tag(name, text, at, color="#ffb547", lift=9.0):
    TAGS[name] = k.tag(text, at, color, lift)
    TAGS[name]["text0"] = text
    TAGS[name]["lift"] = lift
    return TAGS[name]


def move_tag(name, at):
    tg = TAGS[name]
    tg["at"] = Vector(at)
    tg["top"] = tg["at"] + Vector((0, 0, tg["lift"]))
    tg["group"].location = tg["at"]


OC = oled["center"]
BT = btn["top"]
BZ = bz["top"]
LED = rgb["top"]
ESPC = Vector((-17, 0, 14))
PTOP = PHONE["top"]()
SCRC = PHONE["world"](0.5, 0.5)
SN = (PHONE["group"].matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()  # screen normal
FRONT = Vector((40, -22, 14))
DESK_Q = Vector((84, -30, 24))  # board + phone side by side
DESK_P = Vector((72, -372, 218))
CENTER = Vector((35, -15, 0))


def tapw(key):
    u, v = PS.TAPS[key]
    return PHONE["world"](u, v) + SN * 0.6


tag("ant", "Wi-Fi antenna", ANT, "#ffd166", lift=14)
tag("net", "Wi-Fi: PinByPin-ESP32", ANT, "#7fe8de", lift=10)
tag("norouter", "no router needed", ROUTER["top"], "#ff6b6b", lift=8)
tag("hotspot", "like a phone hotspot", PTOP, "#ffd166", lift=8)
tag("addr", "192.168.4.1", ESPC, "#ffd166", lift=34)
tag("ep6", "Ep 6", LED, "#ff6b8b", lift=10)
tag("ep10_oled", "Ep 10", OC + Vector((0, 4, 0)), "#2dd4bf", lift=12)
tag("ep10_bz", "Ep 10", BZ, "#ff8a2a", lift=10)
tag("nonew", "no new parts", OC + Vector((0, 4, 0)), "#2dd4bf", lift=16)
tag("remote", "the remote: your phone", PTOP, "#ffd166", lift=6)
tag("leg_r", "red  F 22b", F.hole(22, "b") + Vector((0, 0, 4)), "#ff6b6b", lift=12)
tag("leg_g", "green  F 24b", F.hole(24, "b") + Vector((0, 0, 4)), "#2fbf71", lift=16)
tag("leg_b", "blue  F 25b", F.hole(25, "b") + Vector((0, 0, 4)), "#5b9cff", lift=20)
tag("d25", "D25  F 11h", F.hole(11, "h"), "#ff6b6b", lift=10)
tag("d26", "D26  F 10g", F.hole(10, "g"), "#2fbf71", lift=15)
tag("d27", "D27  F 9i", F.hole(9, "i"), "#5b9cff", lift=20)
tag("res", "220 Ω each", (F.hole(22, "e") + F.hole(25, "f")) / 2 + Vector((0, 0, 4)), "#e9bd55", lift=12)
tag("get", "GET /color?c=red", ANT, "#ffd166", lift=9)
tag("pagepk", "the page comes back", ANT, "#7fe8de", lift=9)
tag("colors", "4 colors", tapw("green"), "#ffffff", lift=6)
tag("ringbtn", "ring button", tapw("ring"), "#f59e0b", lift=6)
tag("newlink", "new link: /party", tapw("party"), "#ffd166", lift=6)
tag("newhelper", "new helper: handleParty()", ESPC, "#2dd4bf", lift=20)
tag("ip_phone", "192.168.4.1", tapw("addr"), "#2fbf71", lift=6)

# ======================================================================= helpers
PARTS = {"oled": oled["group"], "button": btn["group"], "buzzer": bz["group"], "rgb": rgb["group"]}
for n, r in RES.items():
    PARTS[n] = r["group"]
press_obj = btn["press"]
PRESS_Z = press_obj.location.z
BASE_Z = {n: g.location.z for n, g in PARTS.items()}
ALL_P = set(PARTS)
ALL_W = {n: 1.0 for n in W}
COL = {"red": (1, 0, 0), "green": (0, 1, 0), "blue": (0, 0, 1), "off": (0, 0, 0)}
STATE = {"anchor": BZ}
V = Vector


def vis(group, on):
    for o in [group] + list(group.children_recursive):
        o.hide_render = not on


def show_parts(parts, wires):
    for n, g in PARTS.items():
        g.location.z = BASE_Z[n]
        vis(g, n in parts)
    for n, w in W.items():
        w["draw"](wires.get(n, 0.0))


def set_usb(pull):
    usb.location.x = -16.0 * pull


def set_pwr(on):
    k.pwr_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0 if on else 0.0


def set_rings(t, beeps, center=None):
    for idx, (ob, val) in enumerate(rings):
        ob.location = center if center is not None else BZ
        a, s = 0.0, 1.0
        for tb, kind in beeps:
            span = 0.45 if kind != "lo" else 0.7
            u = (t - tb - idx * (0.07 if kind != "lo" else 0.15)) / span
            if 0 <= u <= 1:
                a = max(a, (1 - u) ** 1.5)
                s = 6.5 + (14 if kind != "lo" else 22) * u
        ob.scale = (s, s, 1)
        val.outputs[0].default_value = a


def fade(t, t0, t1, ramp=0.25):
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


def show(top, big):
    """the sketch's show(): textSize(1) at (0,0), textSize(2) at (0,28)"""
    s = Screen()
    s.text(0, 0, top, 1)
    s.text(0, 28, big, 2)
    return s


SCR_READY = show("open 192.168.4.1", "READY")


def SCR_CMD(n, what):
    return show("command #%d" % n, what)


def cam_path(keys):
    def f(t):
        if t <= keys[0][0]:
            return keys[0][1], keys[0][2]
        for (t0, p0, q0), (t1, p1, q1) in zip(keys, keys[1:]):
            if t <= t1:
                u = (t - t0) / max(1e-6, t1 - t0)
                u = u * u * u * (u * (u * 6 - 15) + 10)
                return p0.lerp(p1, u), q0.lerp(q1, u)
        return keys[-1][1], keys[-1][2]
    return f


def orbit(center, radius, height, a0, a1, dur, lift_target=0.0):
    def f(t):
        u = smooth(t / dur) * 0.6 + 0.4 * (t / dur)
        a = math.radians(a0 + (a1 - a0) * u)
        p = center + Vector((radius * math.cos(a), radius * math.sin(a), height))
        return p, center + Vector((0, 0, lift_target))
    return f


def phone_cam(dist=225.0, side=-18.0, up=8.0):
    """camera square on the phone screen, a little from the left so the board shows behind"""
    p = SCRC + SN * dist + Vector((side, 0, up))
    return p, SCRC + Vector((0, 0, 1.0))


FLY = 0.75  # seconds a command takes phone -> board in the normal-speed shots


class Cmd:
    """one tap on the phone: tap dot + click at t, packet phone -> board, the board acts at t + fly"""

    def __init__(self, t, key, n, fly=FLY):
        self.t, self.key, self.n, self.fly = t, key, n, fly
        self.arrive = t + 0.08 + fly

    def events(self, sfx, beeps):
        sfx += [(self.t, "tap"), (self.t + 0.08, "whoosh")]
        if self.key == "ring":
            sfx += [(self.arrive, "ring_1"), (self.arrive + 0.2, "ring_2")]
            beeps += [(self.arrive, "hi"), (self.arrive + 0.2, "lo")]


def apply_cmds(t, cmds, led0=(0, 0, 0), n0=None, scr0=None):
    """state after a list of Cmd at time t -> (led, screen, pressed key, packet pos, trail)"""
    led, scr, pressed, pkt = led0, scr0, None, None
    trail = []
    for c in cmds:
        if c.t - 0.05 <= t < c.t + 0.35:
            pressed = c.key
        if c.t + 0.08 <= t < c.arrive:
            path = p12.arc_path(tapw(c.key), ANT, lift=38)
            u = (t - c.t - 0.08) / c.fly
            pkt = path(u)
            trail = [path(u - 0.035 * (j + 1)) if u - 0.035 * (j + 1) > 0 else None for j in range(5)]
        if t >= c.arrive:
            if c.key in COL:
                led = COL[c.key]
                scr = SCR_CMD(c.n, c.key)
            elif c.key == "ring":
                scr = SCR_CMD(c.n, "RING!")
            elif c.key == "party":
                scr = SCR_CMD(c.n, "PARTY!")
                u = t - c.arrive
                led = [COL["red"], COL["green"], COL["blue"]][int(u / 0.2) % 3] if u < 1.8 else COL["off"]
    return led, scr, pressed, pkt, trail


def taps_dot(t, cmds, party=False):
    for c in cmds:
        age = t - c.t
        if -0.05 <= age <= 0.35:
            u, v = PS.TAPS[c.key]
            if party and c.key in PS.page_buttons(False):  # party page: buttons sit higher/smaller
                r = PS.page_buttons(True)[c.key]
                u, v = (r[0] + r[2]) / 2 / PS.W, (r[1] + r[3]) / 2 / PS.H
            PHONE["set_tap"](u, v, 1.0 - max(0.0, age) / 0.35, age)
            return
    PHONE["set_tap"](0.5, 0.5, 0.0, -1)


# ======================================================================= shots
def shot_spec(sh):
    """returns (camera f(t), state f(t) -> None, sfx list [(t, kind)])"""
    sid, dur = sh["id"], sh["end"] - sh["start"]
    wt = lambda w, n=0: word_t(sh, w, n)  # noqa: E731
    sfx = []
    beeps = []
    global LAST_BEEPS
    LAST_BEEPS = beeps

    def base_state(t, scr, led=(0, 0, 0), phone="page", parts=ALL_P, wires=ALL_W, pull=0.0, pwr=True, show_phone=True,
                   router=False, board_rip=0.0):
        show_parts(parts, wires)
        press_obj.location.z = PRESS_Z
        set_usb(pull)
        set_pwr(pwr)
        k.set_screen(scr)
        rgb["set"](led, 1.0 if any(led) else 0.0)
        STATE["anchor"] = BZ
        set_rings(t, beeps)
        xray(0.0)
        for tg in TAGS.values():
            tg["set"](0.0)
            tg["text"] = tg["text0"]
        vis(PHONE["group"], show_phone)
        PHONE["set_screen"](IMG[phone])
        PHONE["set_tap"](0.5, 0.5, 0.0, -1)
        vis(ROUTER["group"], router)
        ANTG["set"](0.0)
        RIP_P["off"]()
        RIP_R["off"]()
        if board_rip > 0 and pwr:
            RIP_B["set"](t, -10.0, level=board_rip, period=1.6, rmax=90)
        else:
            RIP_B["off"]()
        PKT["set"](None)

    def cmd_state(t, cmds, scr0, led0=(0, 0, 0), page="page", rip=0.2, party=False, **kw):
        led, scr, pressed, pkt, trail = apply_cmds(t, cmds, led0, scr0=scr0)
        ph = page
        if pressed and not party:
            ph = "page_" + pressed
        elif pressed and party:
            ph = "page_party_party" if pressed == "party" else page
        base_state(t, scr, led=led, phone=ph, board_rip=rip, **kw)
        taps_dot(t, cmds, party)
        PKT["set"](pkt, trail)
        return pkt

    # ---------------- cold open
    if sid == "open_tap":
        c = Cmd(wt("red"), "red", 1, fly=wt("turns") - 0.15 - wt("red"))
        c.events(sfx, beeps)
        camf = cam_path([(0, DESK_P + V((40, 40, -20)), DESK_Q + V((10, 0, 0))), (dur, DESK_P + V((20, 60, -30)), DESK_Q)])
        return camf, lambda t: cmd_state(t, [c], SCR_READY), sfx

    if sid == "open_ring":
        c = Cmd(0.15, "ring", 2, fly=wt("plays") - 0.23)
        c.events(sfx, beeps)
        camf = cam_path([(0, DESK_P + V((30, 20, 0)), DESK_Q), (dur, DESK_P + V((-20, 10, 10)), DESK_Q + V((-5, 0, 0)))])
        return camf, lambda t: cmd_state(t, [c], SCR_CMD(1, "red"), led0=COL["red"]), sfx

    if sid == "open_count":
        cs = [Cmd(-0.4, "blue", 3), Cmd(wt("command") - 0.75, "green", 4), Cmd(wt("sends") - 0.75, "red", 5)]
        for c in cs[1:]:
            sfx.append((c.t, "tap"))
        camf = cam_path([(0, OC + V((-10, -46, 40)), OC + V((-3, 0, 0))), (dur, OC + V((0, -36, 32)), OC + V((0, 0, 0)))])

        def st(t):
            led, scr, _, _, _ = apply_cmds(t, cs, scr0=SCR_CMD(2, "RING!"))
            base_state(t, scr, led=led)
        return camf, st, sfx

    if sid == "open_orbit":
        tph, tnew = wt("phone"), wt("single")
        camf = orbit(V((78, -25, 0)), 340, 225, -105, -62, dur, lift_target=16.0)

        def st(t):
            base_state(t, SCR_CMD(5, "red"), led=COL["red"], board_rip=0.25)
            RIP_P["set"](t, 0.0, level=0.3, period=1.6, rmax=45, centre=PTOP)
            TAGS["remote"]["set"](fade(t, tph - 0.2, dur), 1.0)
            TAGS["nonew"]["set"](fade(t, tnew - 0.2, dur), 1.0)
        return camf, st, sfx

    # ---------------- Wi-Fi
    if sid == "wifi_rings":
        twf, tant, tzig = wt("Wi-Fi"), wt("antenna"), wt("zig")
        camf = cam_path([(0, V((40, -190, 150)), ESPC + V((5, 0, 0))), (tant - 0.4, ANT + V((-30, -95, 75)), ANT),
                         (dur, ANT + V((-18, -70, 58)), ANT)])

        def st(t):
            base_state(t, SCR_READY, show_phone=False)
            RIP_B["set"](t, twf, level=0.7, period=1.3, rmax=80)
            ANTG["set"](smooth((t - tant) / 0.4) * (0.75 + 0.25 * math.sin(t * 6)))
            TAGS["ant"]["set"](fade(t, tzig - 0.2, dur), 1.0)
        return camf, st, sfx

    if sid == "wifi_hotspot":
        trt, tround, topen, tnet, thot = wt("router"), wt("round"), wt("opens"), wt("network"), wt("hotspot")
        camf = cam_path([(0, V((90, -280, 220)), V((80, 20, 15))), (tround, V((80, -290, 220)), V((70, 5, 15))),
                         (dur, DESK_P + V((0, 0, 20)), DESK_Q + V((0, 10, 10)))])

        def st(t):
            gone = smooth((t - tround) / 0.6)
            base_state(t, SCR_READY, router=gone < 0.98, show_phone=t >= thot - 0.5)
            ROUTER["group"].scale = (1 - gone,) * 3 if gone < 0.98 else (1, 1, 1)
            if t < tround:
                RIP_R["set"](t, 0.0, level=0.8, period=1.3, rmax=90, centre=ROUTER["top"])
            TAGS["norouter"]["set"](fade(t, tround - 0.3, tround + 0.5), 1.0)
            if t >= topen:
                u = smooth((t - topen) / 1.2)
                RIP_B["off"]()
                RIP_B["bubble"](10 + 95 * u, 0.6)
            else:
                RIP_B["set"](t, 0.0, level=0.5, period=1.6, rmax=80)
            TAGS["net"]["text"] = "Wi-Fi: PinByPin-ESP32"
            move_tag("net", ANT + V((0, 0, 70)))
            TAGS["net"]["set"](fade(t, tnet - 0.2, dur), 1.0)
            TAGS["hotspot"]["set"](fade(t, thot - 0.2, dur), 1.0)
        return camf, st, sfx

    if sid == "wifi_join":
        tj, taddr = wt("joins"), wt("address")
        nums = ["one", "nine", "two", "one", "six", "eight", "four", "one"]
        shown = ["1", "19", "192", "192.1", "192.16", "192.168", "192.168.4", "192.168.4.1"]
        spoken = [(SEGS[s]["start"] + w["t"] - sh["start"], _norm(w["w"])) for s in sh["segs"] for w in SEGS[s]["words"]]
        spoken = [x for x in spoken if x[0] > taddr]
        times = []
        for w in nums:  # the spoken digits, in order, after "address"
            i = next(j for j, x in enumerate(spoken) if x[1] == w)
            times.append(spoken[i][0])
            spoken = spoken[i + 1:]
        camf = cam_path([(0, DESK_P + V((10, 0, 0)), DESK_Q), (taddr - 0.5, DESK_P + V((0, 20, -5)), DESK_Q + V((-5, 0, 0))),
                         (dur, V((10, -220, 170)), ESPC + V((15, -10, 10)))])

        def st(t):
            base_state(t, SCR_READY, phone="wifi_connected" if t >= tj + 0.6 else "wifi_list")
            RIP_B["bubble"](95, 0.4)
            RIP_P["set"](t, tj - 0.2, level=0.6, period=1.1, rmax=75, centre=PTOP)
            txt = None
            for tt, s in zip(times, shown):
                if t >= tt - 0.05:
                    txt = s
            if txt:
                TAGS["addr"]["text"] = txt
                TAGS["addr"]["set"](1.0, 1.35)
        return camf, st, sfx

    # ---------------- the circuit
    if sid == "wire_same":
        tled, tscr, tbz = wt("LED"), wt("screen"), wt("buzzer")
        camf = cam_path([(0, V((20, -240, 220)), V((25, -10, 5))), (dur, V((25, -210, 200)), V((27, -8, 6)))])

        def st(t):
            base_state(t, SCR_READY, show_phone=False)
            TAGS["ep6"]["set"](fade(t, tled - 0.1, dur), 1.0)
            TAGS["ep10_oled"]["set"](fade(t, tscr - 0.1, dur), 1.0)
            TAGS["ep10_bz"]["set"](fade(t, tbz - 0.1, dur), 1.0)
        return camf, st, sfx

    if sid == "wire_rgb":
        tg, tb, t25, t26, t27, tres = wt("green"), wt("blue"), wt("twenty-five"), wt("twenty-six"), wt("twenty-seven"), wt("resistor")
        cpt = V((5, -32, 9))
        camf = cam_path([(0, cpt + V((-15, -120, 115)), cpt), (dur, cpt + V((0, -100, 100)), cpt + V((3, 0, 0)))])

        def st(t):
            base_state(t, SCR_READY, show_phone=False)
            TAGS["leg_r"]["set"](fade(t, -0.3, t25 - 0.3), 0.9)
            TAGS["leg_g"]["set"](fade(t, tg - 0.1, t25 - 0.3), 0.9)
            TAGS["leg_b"]["set"](fade(t, tb - 0.1, t25 - 0.3), 0.9)
            TAGS["d25"]["set"](fade(t, t25 - 0.1, tres - 0.5), 0.9)
            TAGS["d26"]["set"](fade(t, t26 - 0.1, tres - 0.5), 0.9)
            TAGS["d27"]["set"](fade(t, t27 - 0.1, tres - 0.5), 0.9)
            TAGS["res"]["set"](fade(t, tres - 0.4, dur), 1.0)
        return camf, st, sfx

    # ---------------- try it
    if sid == "try_upload":
        tscr = wt("screen")
        sfx += [(0.25, "plug")]
        camf = cam_path([(0, V((-10, -170, 140)), (OC + V(( -60, 0, 0)))), (dur, OC + V((-6, -48, 42)), OC + V((-2, 0, 0)))])

        def st(t):
            on = t >= 0.3
            base_state(t, SCR_READY if t >= tscr else (Screen() if on else None), pull=1 - smooth((t - 0.05) / 0.3),
                       pwr=on, show_phone=False)
        return camf, st, sfx

    if sid == "try_join":
        tjoin, tpw = wt("join"), wt("password")
        sfx += [(tjoin, "tap")] + [(tpw - 0.6 + i * 0.16, "tap") for i in range(8)]
        camf = cam_path([(0, *phone_cam(250, -30, 20)), (dur, *phone_cam(215, -14, 8))])

        def st(t):
            if t < tjoin:
                ph = "wifi_list"
            elif t < tjoin + 0.5:
                ph = "wifi_tap"
            elif t < tpw - 0.6:
                ph = "wifi_pass_0"
            else:
                ph = "wifi_pass_%d" % min(8, int((t - (tpw - 0.6)) / 0.16) + 1)
            base_state(t, SCR_READY, phone=ph, board_rip=0.2)
            if tjoin - 0.05 <= t <= tjoin + 0.35:
                u, v = PS.TAPS["wifi_net"]
                PHONE["set_tap"](u, v, 1 - max(0, t - tjoin) / 0.35, t - tjoin)
        return camf, st, sfx

    if sid == "try_page":
        ttype, tthere, tcol, tring = wt("Type"), wt("there's"), wt("colors"), wt("ring")
        t0 = ttype + 0.25
        n_chars = len(PS.ADDR)
        sfx += [(t0 + i * 0.1, "tap") for i in range(n_chars)]
        camf = cam_path([(0, *phone_cam(240, -14, 8)), (dur, *phone_cam(228, -6, 4))])

        def st(t):
            if t < tthere - 0.2:
                ph = "addr_type_%d" % max(0, min(n_chars, int((t - t0) / 0.1) + 1 if t >= t0 else 0))
            else:
                ph = "page"
            base_state(t, SCR_READY, phone=ph, board_rip=0.2)
            TAGS["colors"]["set"](fade(t, tcol - 0.2, tring - 0.4), 1.0)
            TAGS["ringbtn"]["set"](fade(t, tring - 0.1, dur), 1.0)
        return camf, st, sfx

    if sid == "try_red":
        c = Cmd(wt("red"), "red", 1, fly=wt("sets") - wt("red") - 0.08)
        c.events(sfx, beeps)
        tcount = wt("counts")
        camf = cam_path([(0, DESK_P + V((40, 40, -20)), DESK_Q + V((10, 0, 0))), (c.arrive - 0.6, DESK_P, DESK_Q),
                         (tcount - 0.6, V((80, -200, 140)), V((35, -10, 16))), (dur, OC + V((-10, -70, 60)), OC + V((-2, -4, 0)))])
        return camf, lambda t: cmd_state(t, [c], SCR_READY), sfx

    if sid == "try_packet":
        tsend, tair, tread, tchg, tback, tblink = wt("sends"), wt("air"), wt("reads"), wt("changes"), wt("page"), wt("blink")
        go = PHONE["world"](*PS.TAPS["red"]) + SN * 0.6
        out_path = p12.arc_path(go, ANT, lift=38)
        back_path = p12.arc_path(ANT, PTOP, lift=38)
        t_out0, t_out1 = tsend - 0.1, tread
        t_bk0, t_bk1 = tback - 0.3, tback + 1.2
        sfx += [(t_out0 - 0.3, "tap"), (t_out0, "whoosh"), (t_bk0, "whoosh"), (tblink - 0.2, "tap"), (tblink - 0.12, "whoosh")]
        camf = cam_path([(0, DESK_P + V((0, 30, 40)), DESK_Q + V((0, 0, 16))), (dur, DESK_P + V((-10, 20, 45)), DESK_Q + V((-5, 0, 15)))])

        def st(t):
            led = COL["red"] if t >= tchg else COL["off"]
            scr = SCR_CMD(1, "red") if t >= tchg else SCR_READY
            ph = "page_red" if t_out0 - 0.35 <= t < t_out0 + 0.4 else "page"
            if t_bk1 <= t < t_bk1 + 0.15:
                ph = "addr_type_0"  # the page is redrawn
            base_state(t, scr, led=led, phone=ph, board_rip=0.25)
            pkt, trail = None, []
            if t_out0 <= t < t_out1:
                u = (t - t_out0) / (t_out1 - t_out0)
                pkt, trail = out_path(u), [out_path(u - 0.03 * (j + 1)) if u - 0.03 * (j + 1) > 0 else None for j in range(5)]
                move_tag("get", pkt)
                TAGS["get"]["set"](1.0, 1.1)
            elif t_bk0 <= t < t_bk1:
                u = (t - t_bk0) / (t_bk1 - t_bk0)
                pkt, trail = back_path(u), [back_path(u - 0.03 * (j + 1)) if u - 0.03 * (j + 1) > 0 else None for j in range(5)]
                move_tag("pagepk", pkt)
                TAGS["pagepk"]["set"](1.0, 1.1)
            elif tblink - 0.12 <= t < tblink + 0.35:  # the real speed: there and back in a blink
                u = (t - (tblink - 0.12)) / 0.47
                pkt = out_path(u * 2) if u < 0.5 else back_path(u * 2 - 1)
            PKT["set"](pkt, trail)
            if t_out0 - 0.35 <= t <= t_out0 + 0.05:
                u, v = PS.TAPS["red"]
                PHONE["set_tap"](u, v, 1.0, t - (t_out0 - 0.35))
            if tread <= t < tread + 0.6:
                ANTG["set"](1 - (t - tread) / 0.6)
        return camf, st, sfx

    if sid == "try_colors":
        cs = [Cmd(0.05, "green", 2, 0.3), Cmd(wt("blue") - 0.05, "blue", 3, 0.3), Cmd(wt("off") - 0.05, "off", 4, 0.3),
              Cmd(wt("tap") - 0.05, "red", 5, 0.3), Cmd(wt("going") - 0.05, "green", 6, 0.3)]
        for c in cs:
            c.events(sfx, beeps)
        tcnt = wt("counter")
        camf = cam_path([(0, DESK_P + V((30, 40, -15)), DESK_Q), (tcnt - 1.2, DESK_P + V((10, 50, -15)), DESK_Q + V((-5, 0, 0))),
                         (dur, V((60, -170, 140)), OC + V((-10, -25, 0)))])
        return camf, lambda t: cmd_state(t, cs, SCR_CMD(1, "red"), led0=COL["red"]), sfx

    if sid == "try_ring":
        c = Cmd(wt("ring"), "ring", 7, fly=wt("plays") - wt("ring") - 0.08)
        c.events(sfx, beeps)
        camf = cam_path([(0, DESK_P + V((30, 30, -10)), DESK_Q), (dur, DESK_P + V((0, 60, -20)), DESK_Q + V((-15, -5, -2)))])
        return camf, lambda t: cmd_state(t, [c], SCR_CMD(6, "green"), led0=COL["green"]), sfx

    # ---------------- troubles (phone close-ups)
    if sid == "trouble_nointernet":
        tsays, tsw, tstay = wt("says"), wt("switches"), wt("stay")
        tap_t = wt("connected") + 0.1
        sfx.append((tap_t, "tap"))
        camf = cam_path([(0, *phone_cam(230, -20, 10)), (dur, *phone_cam(205, -10, 6))])

        def st(t):
            if t < tsays - 0.1:
                ph = "page"
            elif t < tsw:
                ph = "nointernet"
            elif t < tstay - 0.4:
                ph = "mobile"
            elif t < tap_t:
                ph = "nointernet"
            elif t < tap_t + 0.5:
                ph = "nointernet_stay"
            else:
                ph = "page"
            base_state(t, SCR_READY, phone=ph, board_rip=0.2)
            if tap_t - 0.05 <= t <= tap_t + 0.35:
                u, v = PS.TAPS["stay"]
                PHONE["set_tap"](u, v, 1 - max(0, t - tap_t) / 0.35, t - tap_t)
        return camf, st, sfx

    if sid == "trouble_password":
        t8 = wt("eight")
        camf = cam_path([(0, *phone_cam(225, -16, 8)), (dur, *phone_cam(205, -8, 5))])
        return camf, lambda t: base_state(t, SCR_READY, phone="pass8" if t >= t8 else "pass7", board_rip=0.2), sfx

    if sid == "trouble_address":
        tex, twww, thttps = wt("exactly"), wt("www"), wt("https")
        camf = cam_path([(0, *phone_cam(225, -16, 8)), (dur, *phone_cam(205, -8, 5))])

        def st(t):
            if t < twww - 0.2:
                ph = "addr_ok" if t >= tex - 0.3 else "page"
            elif t < thttps - 0.2:
                ph = "addr_www"
            elif t < thttps + 1.0:
                ph = "addr_https"
            else:
                ph = "addr_ok"
            base_state(t, SCR_READY, phone=ph, board_rip=0.2)
            TAGS["ip_phone"]["text"] = "just the numbers" if t < twww - 0.2 or t >= thttps + 1.0 else "no www, no https"
            TAGS["ip_phone"]["color"] = "#2fbf71" if ph == "addr_ok" else "#ff6b6b"
            TAGS["ip_phone"]["set"](fade(t, tex - 0.3, dur), 1.0)
        return camf, st, sfx

    # ---------------- challenge + outro
    if sid == "challenge":
        c = Cmd(wt("button"), "party", 1, fly=wt("flashes") - wt("button") - 0.08)
        c.events(sfx, beeps)
        tlink, thelp = wt("link"), wt("helper")
        camf = cam_path([(0, DESK_P + V((40, 40, -20)), DESK_Q + V((10, 0, 0))), (dur, DESK_P + V((10, 30, -10)), DESK_Q)])

        def st(t):
            cmd_state(t, [c], SCR_READY, page="page_party", party=True)
            TAGS["newlink"]["set"](fade(t, tlink - 0.2, dur), 1.0)
            TAGS["newhelper"]["set"](fade(t, thelp - 0.2, dur), 1.0)
        return camf, st, sfx

    if sid == "outro":
        camf = orbit(V((78, -25, 0)), 345, 230, -72, -118, dur, lift_target=16.0)

        def st(t):
            base_state(t, show("see you in", "ep 13"), led=COL["blue"], board_rip=0.25)
        return camf, st, sfx

    raise KeyError("no spec for shot " + sid)


# ======================================================================= render
os.makedirs(OUT, exist_ok=True)
sc.render.image_settings.file_format = "PNG"
FSTOP = {"open_count": 22.0, "try_upload": 16.0, "wifi_rings": 16.0}
DEFAULT_FSTOP = 18.0  # board and phone sit at different depths: keep both readable
index = []
OVL = {}
ANCH = {}
LAST_BEEPS = []
for sh in SHOTS:
    if ONLY and sh["id"] not in ONLY:
        continue
    camf, st, sfx = shot_spec(sh)
    cam.data.dof.aperture_fstop = FSTOP.get(sh["id"], DEFAULT_FSTOP)
    n = max(1, round((sh["end"] - sh["start"]) * FPS))
    index.append({"id": sh["id"], "segs": sh["segs"], "start": sh["start"], "frames": n,
                  "sfx": [{"t": round(sh["start"] + t, 3), "kind": kd} for t, kd in sorted(sfx)],
                  "beeps": [{"t": round(t, 3), "kind": kd} for t, kd in sorted(LAST_BEEPS)]})  # shot-relative
    if STILLS:
        frames = sorted({1, n // 2 + 1, n})
        outdir = os.path.join(OUT, "stills")
    else:
        frames = FRAMES or list(range(1, n + 1))
        outdir = os.path.join(OUT, "shots", sh["id"])
    os.makedirs(outdir, exist_ok=True)
    for f in frames:
        path = os.path.join(outdir, (sh["id"] + "_" if STILLS else "") + f"f_{f:04d}.png")
        # a resumed render skips frames already on disk, but still poses the scene so overlay.json stays complete
        skip = os.path.exists(path) and not (STILLS or FRAMES)
        t = (f - 1) / FPS
        p, q = camf(t)
        cam.location = p * MM
        tgt.location = q * MM
        st(t)
        bpy.context.view_layer.update()
        ov = []
        for tg in TAGS.values():
            if tg["on"] > 0.02:
                a2 = world_to_camera_view(sc, cam, tg["at"] * MM)
                b2 = world_to_camera_view(sc, cam, tg["top"] * MM)
                if a2.z > 0:
                    ov.append({"text": tg["text"], "color": tg["color"], "on": round(tg["on"], 3), "scale": tg["scale"],
                               "a": [round(a2.x, 4), round(1 - a2.y, 4)], "b": [round(b2.x, 4), round(1 - b2.y, 4)]})
        OVL.setdefault(sh["id"], {})[str(f)] = ov
        bp = world_to_camera_view(sc, cam, STATE["anchor"] * MM)  # buzzer on screen, for the 2D sound waves
        ANCH.setdefault(sh["id"], {})[str(f)] = [round(bp.x, 4), round(1 - bp.y, 4)] if bp.z > 0 else None
        if skip:
            continue
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        print("frame", sh["id"], f, "/", n, flush=True)
if not STILLS and not FRAMES:
    for sid, frames_ov in OVL.items():
        json.dump(frames_ov, open(os.path.join(OUT, "shots", sid, "overlay.json"), "w"))
        json.dump(ANCH.get(sid, {}), open(os.path.join(OUT, "shots", sid, "anchors.json"), "w"))
elif STILLS:
    for sid, frames_ov in OVL.items():
        json.dump(frames_ov, open(os.path.join(OUT, "stills", sid + "_overlay.json"), "w"))
prev = []
ip = os.path.join(OUT, "shots.json")
if os.path.exists(ip) and (ONLY or STILLS or FRAMES):
    prev = [x for x in json.load(open(ip)) if x["id"] not in {i["id"] for i in index}]
json.dump(sorted(prev + index, key=lambda x: x["start"]), open(ip, "w"), indent=1)
print("shots:", len(index))
