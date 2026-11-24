"""Episode 11 (DRAFT) - every Blender 3D shot of the motion-alarm episode, timed to the narration.

    blender -b -P video/ep11/b3d/ep11_3d.py -- [--shots open_arm,pir_zones] [--frames 1,40] [--stills] [--cycles]

Same pipeline as video/ep10/b3d/ep10_3d.py. Timing: video/ep11/build/schedule.json (EN narration, word times); without
it the timing is estimated from script.json (2.45 words/s). A shot = a run of consecutive segments whose vis is
"b3d:<id>"; its length = from the first segment's start to the next segment's start.
Output: video/ep11/b3d/build/shots/<id>/f_0001.png ... + overlay.json/anchors.json per shot + shots.json (start,
frames, sfx events, beeps). --stills renders 3 frames per shot (start, middle, end) into build/stills/.
Screens are drawn exactly like lessons/11-motion-alarm/code/motion_alarm/motion_alarm.ino: size-1 line at (0,0),
size-2 line at (0,28) (the Ep 11 sketch uses textSize(2) for the big line, Ep 10's helper used 3).
Circuit = the Ep 10 layout unchanged + the PIR (pbl.py layout, front board F, back board B):
  Ep 10: B4e->B r+ 4 (3V3)  B5d->B r- 5 (GND)  OLED B34f..37f, B34j->r- 34, B35j->r+ 35  B17e->B36h green SCL (D22)
         B14e->B37g blue SDA (D21)  button B24/26 e,f; B13d->B24d yellow (D19); B26j->r- 26
         buzzer F30c(+)/F33c; F13i->F30a orange (D32); F5h->F l- 5 (GND); F33a->F l- 33
  PIR legs B50e VCC, B51e OUT, B52e GND (PCB + dome behind the legs, over B 45-57 f-j)
         F4h (VIN) -> F l+ 4 red (the front + line becomes 5 V);  F l+ 50 -> B50b red
         F l- 52 -> B52b black (the front - line is GND since Ep 10)
         F12h (D33) -> B51d purple (runs along the front board, then straight back between the red and the black)
"""
import json
import math
import os
import random
import re
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
EP = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(EP, "..", "b3d"))
import parts_ep11 as px  # noqa: E402
import parts_pir  # noqa: E402
import pbl  # noqa: E402
from oledfont import Screen  # noqa: E402
from pbl import MM, lin, smooth  # noqa: E402

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


def word_abs(seg, word, nth=0):
    """absolute time of a word in any segment (for events that run across a cut, e.g. countdown, siren)"""
    k = 0
    for w in SEGS[seg]["words"]:
        if _norm(w["w"]).startswith(_norm(word)):
            if k == nth:
                return SEGS[seg]["start"] + w["t"]
            k += 1
    raise KeyError(f"{seg}: word {word!r} not found")


# ======================================================================= scene
k = pbl.Kit(fps=FPS, engine="CYCLES" if "--cycles" in argv else "EEVEE")
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32", "D33", "VIN"})
usb = k.usb_cable()
cam, tgt = k.camera(lens=50, fstop=10.0)
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
EP10_W = list(W)
W["pir_vin"] = k.wire(F.hole(4, "h"), F.rail(4, "l", "+"), "red", name="pir_vin")
W["pir_vcc"] = k.wire(F.rail(50, "l", "+"), B.hole(50, "b"), "red", h=8, name="pir_vcc")
W["pir_gnd"] = k.wire(F.rail(52, "l", "-"), B.hole(52, "b"), "black", h=8, name="pir_gnd")
W["pir_out"] = k.wire(F.hole(12, "h"), B.hole(51, "d"), "purple", h=13, name="pir_out",
                      via=[(-11.0, -25.0), (66.0, -25.0), (83.82, -3.0)])
PIR_W = ["pir_vin", "pir_vcc", "pir_gnd", "pir_out"]
rings = k.sound_rings(bz["top"], 3)
# props (hidden unless a shot shows them)
HAND = px.warm_hand(k, scale=0.6)
JAR = px.cookie_jar(k, (118, -98, 0), r=12.0, h=30.0)
CAT = px.cat(k, (30, -100, 0))
CUP = px.tea_cup(k, (84, -92, 0))
THUMB = px.thumb(k, (130, 24, 30))
DUO = {"passive": px.buzzer_unit(k, "passive", (18, -112, 9.5)), "active": px.buzzer_unit(k, "active", (52, -112, 9.5))}
k.lights(center=(0.045, 0.0, 0.0), key=2.2)
k.glare(threshold=2.5)
sc = k.scene
LIGHTS = [(bpy.data.objects[n], bpy.data.objects[n].data.energy) for n in ("key", "rim", "fill")]
WORLD_BG = sc.world.node_tree.nodes["Background"]
OUT_MAT = k.mats["wire_purple"].node_tree.nodes["Principled BSDF"]
OUT_MAT.inputs["Emission Color"].default_value = (*lin("#c9a6ff"), 1)

TAGS = {}


def tag(name, text, at, color="#ffb547", lift=9.0):
    TAGS[name] = k.tag(text, at, color, lift)
    TAGS[name]["text0"] = text
    TAGS[name]["lift"] = lift
    TAGS[name]["at0"] = Vector(at)
    return TAGS[name]


def move_tag(name, at):
    tg = TAGS[name]
    tg["at"] = Vector(at)
    tg["top"] = tg["at"] + Vector((0, 0, tg["lift"]))
    tg["group"].location = tg["at"]


PINS = pir["pins"]
LEG_TOP = Vector((0, 0, 5.0))
OC = oled["center"]
BT = btn["top"]
BZ = bz["top"]
PT = pir["top"]
PC = Vector((pir["center"].x, pir["center"].y, pbl.TOP + 10))
# hole / pin tags used in the wiring shots (printed hole names, like Ep 10)
tag("vin", "VIN  F 4h", F.hole(4, "h"), "#ff6b6b", lift=12)
tag("lplus", "+ line (5 V)", F.rail(4, "l", "+"), "#ff6b6b", lift=8)
tag("vcc", "VCC  B 50b", B.hole(50, "b"), "#ff6b6b", lift=13)
tag("lminus", "- line (GND)", F.rail(52, "l", "-"), "#c3cbd7", lift=8)
tag("gnd", "GND  B 52b", B.hole(52, "b"), "#c3cbd7", lift=13)
tag("d33", "D33  F 12h", F.hole(12, "h"), "#b48cff", lift=12)
tag("out", "OUT  B 51d", B.hole(51, "d"), "#b48cff", lift=16)
for nm, col, lf in (("VCC", "#ff6b6b", 9), ("OUT", "#b48cff", 13), ("GND", "#c3cbd7", 9)):
    tag("leg_" + nm, nm, PINS[nm] + LEG_TOP, col, lift=lf)
tag("v33", "3.3 V - safe for the ESP32", PINS["OUT"] + LEG_TOP, "#2fbf71", lift=16)
tag("outstate", "OUT = LOW", PINS["OUT"] + LEG_TOP, "#b48cff", lift=14)
tag("stay_oled", "stays", OC + Vector((0, 4, 0)), "#2dd4bf", lift=12)
tag("stay_btn", "stays", BT, "#2dd4bf", lift=10)
tag("stay_bz", "stays", BZ, "#2dd4bf", lift=10)
tag("newpir", "new: PIR motion sensor", PT, "#ffb547", lift=14)
tag("ep10", "Ep 10 circuit", OC + Vector((0, 4, 0)), "#2dd4bf", lift=12)
tag("hcsr", "HC-SR501 motion sensor", PT, "#ffb547", lift=10)
tag("lens", "lens = many little windows", PT, "#ffb547", lift=10)
tag("time", "time: how long the yes lasts", PC, "#ff8a2a", lift=10)
tag("range", "range: how far it sees", PC, "#ff8a2a", lift=10)
tag("warm", "warm-up 0 s", PT, "#ffb547", lift=12)
tag("flick", "yes?!", PINS["OUT"] + LEG_TOP, "#ff6b6b", lift=10)
tag("warming", "still warming up", PT, "#ffb547", lift=12)
tag("knob", "time knob too high", PC, "#ff8a2a", lift=10)
tag("knobmin", "time knob: minimum", PC, "#2fbf71", lift=10)
tag("auto", "stops by itself after 15 s", BZ, "#ffb547", lift=12)
tag("passive", "passive: plays any note", DUO["passive"]["group"].location, "#7fe8de", lift=22)
tag("active", "active: one fixed beep", DUO["active"]["group"].location, "#ffb547", lift=22)
tag("open_btm", "open bottom", DUO["passive"]["group"].location, "#7fe8de", lift=20)
tag("sealed", "sealed", DUO["active"]["group"].location, "#ffb547", lift=20)
tag("siren", "siren = passive", DUO["passive"]["group"].location, "#7fe8de", lift=22)
tag("saved", "still 3 after unplugging", OC + Vector((0, 4, 0)), "#2fbf71", lift=12)

# ======================================================================= helpers
USBP = Vector((esp["xU"] - 8, 0, 14))
MID = (OC + BT) / 2
CENTER = Vector((40, 0, 0))
FRONT = Vector((46, -2, 10))  # the desk-front framing: OLED, button, buzzer and the PIR all in view
FSTOP = {"screen_ago": 22.0, "open_ago": 16.0, "pir_hero": 14.0}  # macro shots: more depth of field
BEAM_BASE = PT - Vector((0, 0, 3.0))


def vis(group, on):
    for o in [group] + list(group.children_recursive):
        o.hide_render = not on


PARTS = {"oled": oled["group"], "button": btn["group"], "buzzer": bz["group"], "pir": pir["group"]}
press_obj = btn["press"]
PRESS_Z = press_obj.location.z
BASE_Z = {n: g.location.z for n, g in PARTS.items()}
LIFT0 = (pir["lift"].location.copy(), pir["lift"].rotation_euler.copy())
PROPS = {"hand": HAND["group"], "jar": JAR["group"], "cat": CAT["group"], "cup": CUP["group"], "thumb": THUMB["group"],
         "passive": DUO["passive"]["group"], "active": DUO["active"]["group"]}
PROP_LOC = {n: (g.location.copy(), g.rotation_euler.copy()) for n, g in PROPS.items()}
STATE = {"anchor": BZ}


def show_parts(parts, wires, drop=None, t=0.0):
    """parts: set of part names visible; wires: dict name -> draw progress (missing = hidden);
    drop: {part: t_drop} -> part falls in at that time"""
    for n, g in PARTS.items():
        on = n in parts
        if drop and n in drop:
            on = on and t >= drop[n]
            if on:
                u = min(1.0, (t - drop[n]) / 0.45)
                back = 1 + 2.70158 * (u - 1) ** 3 + 1.70158 * (u - 1) ** 2
                g.location.z = BASE_Z[n] + 30 * (1 - back)
            else:
                g.location.z = BASE_Z[n]
        else:
            g.location.z = BASE_Z[n]
        vis(g, on)
    for n, w in W.items():
        w["draw"](wires.get(n, 0.0))


def press(t, t0, hold=0.16):
    """button cap pushed down while t0-0.05 .. t0+hold"""
    if t0 - 0.05 <= t <= t0 + hold:
        u = (t - (t0 - 0.05))
        return -0.9 * min(1.0, u / 0.05) * (1.0 if t <= t0 + hold - 0.05 else max(0.0, (t0 + hold - t) / 0.05))
    return 0.0


def set_press(dz):
    press_obj.location.z = PRESS_Z + dz


def set_usb(pull):
    usb.location.x = -16.0 * pull


def set_pwr(on):
    k.pwr_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0 if on else 0.0


def set_rings(t, beeps, center=None):
    """beeps: list of (time, kind); kind 'hi' small fast rings, 'lo' slow wide"""
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


def set_thermal(u):
    """0 = normal studio light, 1 = 'infrared camera': lights almost off, everything else deep blue"""
    for ob, e in LIGHTS:
        ob.data.energy = e * (1 - 0.93 * u)
    a, b = lin("#0d1424"), lin("#0b2f8a")
    WORLD_BG.inputs["Color"].default_value = (*[x + (y - x) * u for x, y in zip(a, b)], 1)
    WORLD_BG.inputs["Strength"].default_value = 0.35 + 0.75 * u


def set_out_glow(level):
    OUT_MAT.inputs["Emission Strength"].default_value = 4.0 * level


def wire_k(t, t0, dur=0.7):
    return smooth((t - t0) / dur)


def fade(t, t0, t1, ramp=0.25):
    """1 inside [t0, t1] with soft edges"""
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


def show(top, big):
    """the Ep 11 sketch's show(): textSize(1) at (0,0), textSize(2) at (0,28)"""
    s = Screen()
    s.text(0, 0, top, 1)
    s.text(0, 28, big, 2)
    return s


SCR_READY = show("press to arm", "READY")
SCR_ARMED = show("guarding...", "ARMED")
SCR_INTRUDER = show("motion detected!", "INTRUDER")
SCR_WARMING = show("motion alarm", "warming..")


def SCR_SEEN(n, ago):
    return show(f"seen {n}x, last:", ago)


def SCR_LEAVE(left):
    return show("leave the room!", f"{left} s")


def countdown_screen(t_abs, p_abs):
    """state 2 of the sketch: 'leave the room!' with the seconds left, then ARMED after 10 s"""
    ms = int(round((t_abs - p_abs) * 1000))
    if ms < 10000:
        return SCR_LEAVE((10000 - ms + 999) // 1000)
    return SCR_ARMED


def tick_events(sh, p_abs, sfx, beeps):
    """one tick (2000 Hz, 30 ms) whenever the countdown number changes, kept to this shot"""
    for i in range(10):
        tt = p_abs + i - sh["start"]
        if 0 <= tt < sh["end"] - sh["start"]:
            sfx.append((tt, "tick"))
            beeps.append((tt, "hi"))


def siren_events(sh, s_abs, e_abs, sfx, beeps):
    """tone(BUZZER_PIN, (inState / 250) % 2 ? 2600 : 1800): 1800 Hz first, the note flips every 250 ms"""
    i = 0
    while s_abs + 0.25 * i < e_abs:
        tt = s_abs + 0.25 * i - sh["start"]
        if 0 <= tt < sh["end"] - sh["start"]:
            hi = i % 2 == 1
            sfx.append((tt, "siren_hi" if hi else "siren_lo"))
            beeps.append((tt, "hi" if hi else "lo"))
        i += 1


def cam_path(keys):
    """keys: [(t, pos, target)] -> f(t) with smoother easing between keys"""
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


def beam_of(p):
    """index of the lens window (beam wedge) that sees point p, or None"""
    d = Vector(p) - BEAM_BASE
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
    return Vector(pos) + Vector((math.cos(yaw), math.sin(yaw), 0)) * 24


def lit_by_path(path, t, tail=0.6):
    """windows lit by a moving warm hand: the window it is in now at full, the ones it just left fading"""
    lit = {}
    for j in range(13):
        s = t - tail * j / 12
        if s < 0:
            break
        pos, yaw = path(s)
        i = beam_of(hand_point(pos, yaw))
        if i is not None:
            lit[i] = max(lit.get(i, 0.0), 1.0 - j / 12)
    return lit


def hand_path(keys):
    """keys: [(t, pos, yaw)] -> f(t) = (pos, yaw), eased"""
    def f(t):
        if t <= keys[0][0]:
            return keys[0][1], keys[0][2]
        for (t0, p0, y0), (t1, p1, y1) in zip(keys, keys[1:]):
            if t <= t1:
                u = smooth((t - t0) / max(1e-6, t1 - t0))
                return p0.lerp(p1, u), y0 + (y1 - y0) * u
        return keys[-1][1], keys[-1][2]
    return f


def CATCH_KEYS(tc, dur, t_in):
    """the warm hand sneaks in from the right toward the jar lid (crossing lens windows 8 -> 5), freezes when the
    alarm goes off at tc, then pulls back"""
    return [(0.0, V((330, -120, 48)), math.pi), (t_in, V((300, -118, 48)), math.pi),
            (tc - 0.05, V((168, -100, 46)), math.pi + 0.05), (tc + 0.25, V((164, -100, 47)), math.pi + 0.05),
            (tc + 1.0, V((188, -106, 50)), math.pi), (max(dur, tc + 1.1), V((205, -110, 52)), math.pi)]


def lift_pir(u):
    """u 0..1: the module rises and tips forward so the two trim pots underneath face the camera"""
    lift = pir["lift"]
    lift.location = LIFT0[0] + Vector((0, -4 * u, 24 * u))
    lift.rotation_euler = (math.radians(-125) * u, 0, 0)


def pot_world(name):
    bpy.context.view_layer.update()
    m = pir["pot_" + name].matrix_world
    return m @ Vector((0, 0, -1.6)) / MM


V = Vector
ALL_W = {n: 1.0 for n in W}
ALL_P = {"oled", "button", "buzzer", "pir"}
POT_HI, POT_LO = math.radians(120), math.radians(-120)


# ======================================================================= shots
def shot_spec(sh):
    """returns (camera f(t), state f(t) -> None, sfx list [(t, kind)])"""
    sid, dur = sh["id"], sh["end"] - sh["start"]
    wt = lambda w, n=0: word_t(sh, w, n)  # noqa: E731
    sfx = []
    beeps = []
    global LAST_BEEPS
    LAST_BEEPS = beeps  # filled below; exported to shots.json for the 2D sound-wave overlay

    def base_state(t, scr, parts=ALL_P, wires=ALL_W, pr=0.0, pull=0.0, pwr=True, drop=None, props=(), heat=0.0):
        show_parts(parts, wires, drop, t)
        set_press(pr)
        set_usb(pull)
        set_pwr(pwr)
        k.set_screen(scr)
        STATE["anchor"] = BZ
        set_rings(t, beeps)
        if "buzzer" in parts and not (drop and "buzzer" in drop and t < drop["buzzer"]):
            xray(0.0)
        for tg in TAGS.values():
            tg["set"](0.0)
            tg["text"] = tg["text0"]
        for n, g in PROPS.items():
            g.location, g.rotation_euler = PROP_LOC[n][0].copy(), PROP_LOC[n][1].copy()
            vis(g, n in props)
        for p in (HAND, CAT, CUP):
            px.set_heat(p, heat)
        for nm, d in DUO.items():
            if nm in props:  # set_xray un-hides parts, so only on a visible buzzer
                d["set_xray"](0.0)
        lift_pir(0.0)
        pir["pot_time"].rotation_euler.z = 0.0
        pir["pot_sens"].rotation_euler.z = 0.0
        parts_pir.set_zones(BEAMS, {})
        dome_xray(0.0)
        set_thermal(0.0)
        set_out_glow(0.0)

    # ---------------- cold open
    if sid == "open_arm":
        tp = wt("arm")
        p_abs = sh["start"] + tp
        tick_events(sh, p_abs, sfx, beeps)
        sfx.append((tp, "click"))
        camf = cam_path([(0, V((50, -215, 180)), V((48, -2, 10))), (dur, V((44, -178, 150)), V((44, 0, 11)))])

        def st(t):
            scr = SCR_READY if t < tp else countdown_screen(sh["start"] + t, p_abs)
            base_state(t, scr, pr=press(t, tp))
        return camf, st, sfx

    if sid == "open_catch":
        tc = wt("caught")
        siren_events(sh, sh["start"] + tc, sh["end"] + 5, sfx, beeps)
        path = hand_path(CATCH_KEYS(tc, dur, 1.0))
        camf = cam_path([(0, V((95, -335, 215)), V((126, -40, 14))), (dur, V((104, -305, 195)), V((124, -40, 14)))])

        def st(t):
            scr = SCR_ARMED if t < tc else SCR_INTRUDER
            base_state(t, scr, props={"hand", "jar"}, heat=0.55)
            pos, yaw = path(t)
            place_hand(pos, yaw, 0.08)
            lit = lit_by_path(path, t)
            parts_pir.set_zones(BEAMS, lit, idle=0.05 if t < tc else 0.0)
            set_out_glow(fade(t, tc - 0.05, dur + 1, 0.1))
        return camf, st, sfx

    if sid == "open_ago":
        camf = cam_path([(0, V((40, -150, 130)), OC + V((-2, -10, 0))), (dur, OC + V((-4, -40, 36)), OC + V((-1, 0, 0)))])
        return camf, lambda t: base_state(t, SCR_SEEN(1, "2 min ago")), sfx

    if sid == "open_orbit":
        tn, tcir = wt("One"), wt("circuit")
        camf = orbit(CENTER + V((0, 5, 0)), 250, 190, -118, -62, dur)

        def st(t):
            base_state(t, SCR_ARMED)
            parts_pir.set_zones(BEAMS, {}, idle=0.04 + 0.03 * math.sin(t * 2.5))
            TAGS["newpir"]["set"](fade(t, tn - 0.1, dur), 1.0)
            TAGS["ep10"]["set"](fade(t, tcir - 0.3, dur), 1.0)
        return camf, st, sfx

    # ---------------- the PIR
    if sid == "pir_hero":
        td = wt("dome")
        camf = cam_path([(0, PT + V((-60, -150, 95)), PT + V((0, 0, -4))), (dur, PT + V((-22, -72, 42)), PT + V((0, 0, -3)))])

        def st(t):
            base_state(t, SCR_READY)
            TAGS["hcsr"]["set"](fade(t, td, 4.6), 1.0)
        return camf, st, sfx

    if sid == "pir_glow":
        tir, th, tcat, ttea = wt("infrared"), wt("hand"), wt("cat"), wt("tea")
        tno, tcan = wt("can't"), wt("this")
        hp = V((146, -112, 26))
        camf = cam_path([(0, V((80, -330, 165)), V((80, -60, 20))), (dur, V((80, -300, 150)), V((80, -55, 22)))])

        def st(t):
            base_state(t, SCR_READY, props={"hand", "cat", "cup"})
            place_hand(hp + V((0, 0, 2.5 * math.sin(t * 2.0))), math.radians(172), 0.1)
            th_on = smooth((t - tir) / 0.6) * (1 - smooth((t - tno) / 0.5)) + smooth((t - tcan) / 0.5)
            set_thermal(th_on)
            px.set_heat(HAND, smooth((t - th) / 0.4) * th_on)
            px.set_heat(CAT, smooth((t - tcat) / 0.4) * th_on)
            px.set_heat(CUP, smooth((t - ttea) / 0.4) * th_on * 1.2)
        return camf, st, sfx

    if sid == "pir_lens":
        tl, twin, teach, trow = wt("lens"), wt("windows"), wt("Each"), wt("row")
        # close on the dome for the x-ray, then up to a bird's-eye view where the fan of windows reads as slices
        camf = cam_path([(0, PT + V((-40, -110, 70)), PT + V((0, -10, -3))), (twin - 0.2, PT + V((-30, -95, 60)), PT + V((0, -10, -3))),
                         (teach + 0.6, PT + V((-10, -165, 280)), PT + V((0, -34, -15))), (dur, PT + V((-5, -175, 295)), PT + V((0, -37, -15)))])

        def st(t):
            base_state(t, SCR_READY)
            dome_xray(1.0 if t >= tl else 0.0)
            TAGS["lens"]["set"](fade(t, tl, teach - 0.2), 1.0)
            lit = {}
            for i in range(9):  # window by window
                lit[i] = 0.2 * smooth((t - (twin + 0.12 * i)) / 0.25)
            if teach <= t < trow:  # each one looks at its own slice: sweep a bright one across
                j = int((t - teach) / ((trow - teach) / 9))
                lit[min(8, j)] = 0.7
            if t >= trow:
                lit = {i: 0.45 for i in range(9)}
            parts_pir.set_zones(BEAMS, lit)
        return camf, st, sfx

    if sid == "pir_zones":
        tturn = wt("turns")
        path = hand_path([(0.0, V((185, -68, 36)), math.pi), (4.6, V((40, -68, 36)), math.pi), (dur, V((20, -68, 36)), math.pi)])
        camf = cam_path([(0, V((75, -310, 195)), V((88, -30, 20))), (dur, V((92, -290, 180)), V((84, -25, 20)))])

        def st(t):
            base_state(t, SCR_READY, props={"hand"}, heat=0.8)
            pos, yaw = path(t)
            place_hand(pos, yaw, 0.05)
            parts_pir.set_zones(BEAMS, lit_by_path(path, t), idle=0.04)
            on = fade(t, tturn, dur + 1, 0.12)
            set_out_glow(on)
            TAGS["outstate"]["text"] = "OUT = HIGH (yes!)"
            TAGS["outstate"]["set"](on, 1.0)
        return camf, st, sfx

    if sid == "pir_answer":
        tup, tdown = wt("thumbs"), wt("thumbs", 1)
        path = hand_path([(0.0, V((175, -72, 36)), math.pi), (tup - 0.5, V((175, -72, 36)), math.pi),
                          (tup + 1.6, V((-40, -72, 36)), math.pi), (dur, V((-60, -72, 36)), math.pi)])
        camf = cam_path([(0, V((100, -285, 165)), V((100, -12, 26))), (dur, V((96, -260, 150)), V((100, -8, 26)))])

        def st(t):
            base_state(t, SCR_READY, props={"hand", "thumb"}, heat=0.8)
            pos, yaw = path(t)
            place_hand(pos, yaw, 0.05)
            parts_pir.set_zones(BEAMS, lit_by_path(path, t) if t < tup + 1.5 else {}, idle=0.03)
            high = tup - 0.2 <= t < tdown
            up = 1.0 - smooth((t - tdown) / 0.45)
            THUMB["set"](up, "#2fbf71" if up > 0.5 else "#ff5a4f")
            THUMB["group"].location = PROP_LOC["thumb"][0] + V((0, 0, 2.0 * math.sin(t * 2.2)))
            vis(THUMB["group"], t >= tup - 0.3)
            set_out_glow(1.0 if high else 0.0)
            TAGS["outstate"]["text"] = "OUT = HIGH" if high else "OUT = LOW"
            TAGS["outstate"]["set"](fade(t, tup - 0.3, dur), 1.0)
        return camf, st, sfx

    if sid == "pir_knobs":
        tone_, tlong, tother, tfar = wt("One"), wt("long"), wt("other"), wt("far")
        camf = cam_path([(0, PT + V((-30, -120, 70)), PT + V((0, 0, 4))), (1.6, PT + V((-12, -82, 52)), PT + V((0, -4, 14))),
                         (dur, PT + V((4, -76, 50)), PT + V((0, -4, 14)))])

        def st(t):
            base_state(t, SCR_READY)
            lift_pir(smooth((t - 0.2) / 1.3))
            pir["pot_time"].rotation_euler.z = math.radians(-100) + math.radians(200) * smooth((t - tlong) / 1.0)
            pir["pot_sens"].rotation_euler.z = math.radians(100) - math.radians(200) * smooth((t - tfar) / 1.0)
            move_tag("time", pot_world("time"))
            move_tag("range", pot_world("sens"))
            TAGS["time"]["set"](fade(t, tone_, dur), 1.0)
            TAGS["range"]["set"](fade(t, tother, dur), 1.0)
        return camf, st, sfx

    if sid == "pir_warmup":
        tpw, tw0, tend = wt("power"), wt("give"), dur - 0.5
        sfx += [(tpw - 0.15, "plug")]  # the Ep 11 sketch has no start-up beep
        rng = random.Random(11)
        flicks = [2.3, 3.6, 4.9] + [wt("yes") - 0.1 + 0.0, wt("reason") - 0.1]
        flick_len = [0.35 + 0.3 * rng.random() for _ in flicks]
        camf = cam_path([(0, V((30, -230, 170)), V((55, 5, 14))), (dur, V((50, -200, 150)), V((62, 8, 16)))])

        def st(t):
            on = t >= tpw
            pull = 1 - smooth((t - (tpw - 0.35)) / 0.3)
            secs = int(30 * max(0.0, min(1.0, (t - tw0 + 1.2) / (tend - tw0 + 1.2)))) if on else 0
            if not on:
                scr = None
            elif secs < 30:
                scr = SCR_WARMING
            else:
                scr = SCR_READY
            base_state(t, scr, pull=pull, pwr=on)
            fl = any(f0 <= t < f0 + ln for f0, ln in zip(flicks, flick_len)) and on and secs < 30
            parts_pir.set_zones(BEAMS, {i: 0.9 for i in range(9)} if fl else {})
            set_out_glow(1.0 if fl else 0.0)
            TAGS["flick"]["set"](1.0 if fl else 0.0, 1.0)
            TAGS["warm"]["text"] = "warm-up %d s" % secs if secs < 30 else "ready after 30 s"
            TAGS["warm"]["set"](fade(t, tpw + 0.2, dur), 1.0)
        return camf, st, sfx

    # ---------------- wiring
    if sid == "wire_keep":
        tsc, tbt, tbz = wt("screen"), wt("button"), wt("buzzer")
        camf = cam_path([(0, V((10, -220, 210)), V((15, 0, 5))), (dur, V((15, -190, 190)), V((18, 2, 6)))])
        w = {n: 1.0 for n in EP10_W}

        def st(t):
            base_state(t, SCR_READY, parts={"oled", "button", "buzzer"}, wires=w)
            TAGS["stay_oled"]["set"](fade(t, tsc - 0.1, dur), 1.0)
            TAGS["stay_btn"]["set"](fade(t, tbt - 0.1, dur), 1.0)
            TAGS["stay_bz"]["set"](fade(t, tbz - 0.1, dur), 1.0)
        return camf, st, sfx

    if sid == "wire_pir_power":
        ts, tlg, tr, tv, tb, tg = wt("sensor"), wt("legs"), wt("red"), wt("volts"), wt("black"), wt("ground")
        sfx += [(ts + 0.45, "pop"), (tr, "snap"), (tv + 0.5, "snap"), (tb + 0.5, "snap")]
        camf = cam_path([(0, V((30, -260, 225)), V((30, -8, 6))), (dur, V((32, -240, 210)), V((32, -6, 6)))])
        w0 = {n: 1.0 for n in EP10_W}

        def st(t):
            w = dict(w0, pir_vin=wire_k(t, tr, 0.5), pir_vcc=wire_k(t, tv - 0.2, 0.8), pir_gnd=wire_k(t, tb - 0.1, 0.8))
            base_state(t, SCR_READY, wires=w, drop={"pir": ts})
            for i, nm in enumerate(("VCC", "OUT", "GND")):
                TAGS["leg_" + nm]["set"](fade(t, tlg - 0.3 + i * 0.15, tr - 0.3), 0.9)
            TAGS["vin"]["set"](fade(t, tr - 0.2, dur), 0.85)
            TAGS["lplus"]["set"](fade(t, tr + 0.3, dur), 0.85)
            TAGS["vcc"]["set"](fade(t, tv + 0.3, dur), 0.85)
            TAGS["lminus"]["set"](fade(t, tb - 0.1, dur), 0.85)
            TAGS["gnd"]["set"](fade(t, tg - 0.1, dur), 0.85)
        return camf, st, sfx

    if sid == "wire_pir_out":
        tm, tpu, tpin = wt("middle"), wt("purple"), wt("pin")
        sfx += [(tpu + 1.0, "snap")]
        camf = cam_path([(0, V((40, -200, 170)), V((40, -10, 8))), (dur, V((48, -185, 160)), V((44, -8, 8)))])
        w0 = {n: 1.0 for n in W if n != "pir_out"}

        def st(t):
            base_state(t, SCR_READY, wires=dict(w0, pir_out=wire_k(t, tpu, 1.1)))
            TAGS["leg_OUT"]["set"](fade(t, tm - 0.1, tpu), 1.0)
            TAGS["d33"]["set"](fade(t, tpu - 0.2, dur), 0.9)
            TAGS["out"]["set"](fade(t, tpin - 0.2, dur), 0.9)
        return camf, st, sfx

    if sid == "wire_pir_done":
        t33, tsafe = wt("three"), wt("safe")
        camf = cam_path([(0, PT + V((-70, -150, 95)), PT + V((-5, -12, -10))), (dur, PT + V((-25, -130, 80)), PT + V((-5, -12, -10)))])

        def st(t):
            base_state(t, SCR_READY)
            TAGS["v33"]["text"] = "3.3 V" if t < tsafe else "3.3 V - safe for the ESP32"
            TAGS["v33"]["set"](fade(t, t33 - 0.1, dur), 1.0)
            set_out_glow(0.5 * fade(t, t33 - 0.1, dur))
        return camf, st, sfx

    # ---------------- demo: countdown, armed, siren
    if sid in ("demo_countdown", "demo_armed"):
        armed_abs = word_abs("s19", "armed")
        p_abs = max(SEGS["s18"]["start"] + 0.15, armed_abs - 10.0)
        tick_events(sh, p_abs, sfx, beeps)
        tp = p_abs - sh["start"]
        if sid == "demo_countdown":
            sfx.append((tp, "click"))
            camf = cam_path([(0, V((48, -215, 180)), FRONT), (dur, V((46, -180, 152)), FRONT + V((0, 2, 1)))])
        else:
            camf = cam_path([(0, V((50, -190, 150)), V((62, 8, 14))), (dur, V((70, -170, 135)), V((66, 8, 16)))])
        t_arm = p_abs + 10.0 - sh["start"]  # the moment the sketch shows ARMED

        def st(t):
            scr = SCR_READY if t < tp else countdown_screen(sh["start"] + t, p_abs)
            base_state(t, scr, pr=press(t, tp))
            if sid == "demo_armed" and t >= t_arm:
                parts_pir.set_zones(BEAMS, {}, idle=0.05 + 0.04 * math.sin((t - t_arm) * 3.0))
                TAGS["outstate"]["set"](fade(t, wt("sensor") - 0.2, dur), 1.0)
        return camf, st, sfx

    if sid == "demo_stop":
        tsp, tf = wt("stop"), wt("fifteen")
        siren_events(sh, sh["start"] - 6.0, sh["start"] + tsp, sfx, beeps)
        sfx.append((tsp, "click"))
        camf = cam_path([(0, V((44, -200, 168)), FRONT), (dur, V((38, -175, 148)), FRONT + V((-2, 0, 0)))])

        def st(t):
            scr = SCR_INTRUDER if t < tsp else SCR_SEEN(1, "%d s ago" % (6 + int(t - tsp + 0.0)))
            base_state(t, scr, pr=press(t, tsp))
            TAGS["auto"]["set"](fade(t, tf - 0.2, dur), 1.0)
        return camf, st, sfx

    if sid == "screen_ago":
        camf = cam_path([(0, OC + V((-8, -40, 34)), OC + V((-3, 0, 0))), (dur, OC + V((2, -30, 26)), OC + V((1, 0, 0)))])
        return camf, lambda t: base_state(t, SCR_SEEN(2, "3 min ago")), sfx

    # ---------------- passive vs active buzzer
    dp, da = DUO["passive"], DUO["active"]
    duo_c = (dp["group"].location + da["group"].location) / 2 + V((0, 0, 4))

    def duo_pose(t, tilt, spin):
        for d, sgn in ((dp, 1), (da, -1)):
            g = d["group"]
            g.rotation_euler = (math.radians(-80) * tilt, 0, math.radians(spin * sgn))
            g.location = PROP_LOC["passive" if d is dp else "active"][0] + V((0, 0, 9 * tilt + 0.6 * math.sin(t * 1.8)))

    def duo_top(d):
        bpy.context.view_layer.update()
        return d["group"].matrix_world @ d["top"] / MM

    if sid == "buzzers_two":
        tsame, tdiff = wt("same"), wt("difference")
        camf = cam_path([(0, duo_c + V((-10, -95, 55)), duo_c), (dur, duo_c + V((8, -78, 42)), duo_c)])

        def st(t):
            base_state(t, SCR_READY, props={"passive", "active"})
            duo_pose(t, smooth((t - tsame + 0.3) / 1.0), 25 * math.sin(t * 0.6))
            for nm, d in (("open_btm", dp), ("sealed", da)):
                move_tag(nm, d["group"].location.copy())  # the bottom (origin), facing the camera when tilted
                TAGS[nm]["set"](fade(t, tdiff + 0.4, dur), 0.9)
        return camf, st, sfx

    if sid == "buzzers_xray":
        tpas, tany, tact, tpow, tbeep = wt("passive"), wt("any"), wt("active"), wt("power"), wt("beep", 1)
        notes = [(tany + 0.0, "note_1"), (tany + 0.3, "note_2"), (tany + 0.6, "note_3")]
        sfx += notes + [(tpow + 0.35, "beep_active"), (tbeep, "beep_active")]
        beeps += [(x, "hi") for x, _ in notes] + [(tpow + 0.35, "hi"), (tpow + 0.55, "hi"), (tbeep, "hi"), (tbeep + 0.2, "hi")]
        camf = cam_path([(0, duo_c + V((0, -92, 52)), duo_c), (dur, duo_c + V((-6, -84, 47)), duo_c + V((0, 0, -1)))])

        def st(t):
            base_state(t, SCR_READY, props={"passive", "active"})
            duo_pose(t, 1 - smooth(t / 0.6), 0.0)
            xr = 1.0 if t > 0.4 else 0.0
            dp["set_xray"](xr)
            da["set_xray"](xr)
            move_tag("passive", duo_top(dp))
            move_tag("active", duo_top(da))
            TAGS["passive"]["set"](fade(t, tpas - 0.1, dur), 0.95)
            TAGS["active"]["set"](fade(t, tact - 0.1, dur), 0.95)
            act = t >= tpow
            STATE["anchor"] = duo_top(da if act else dp)
            set_rings(t, beeps, STATE["anchor"])
        return camf, st, sfx

    if sid == "buzzers_siren":
        talarm = wt("alarm")
        sfx.append((0.15, "beep_active"))
        beeps += [(0.15, "hi"), (0.35, "hi")]
        siren_events(sh, sh["start"] + talarm, sh["end"] + 1, sfx, beeps)
        camf = cam_path([(0, duo_c + V((-6, -76, 44)), duo_c), (dur, duo_c + V((-16, -68, 40)), duo_c + V((-4, 0, 0)))])

        def st(t):
            base_state(t, SCR_READY, props={"passive", "active"})
            duo_pose(t, 0.0, 0.0)
            STATE["anchor"] = duo_top(dp if t >= talarm else da)
            set_rings(t, beeps, STATE["anchor"])
            move_tag("siren", duo_top(dp))
            TAGS["siren"]["set"](fade(t, talarm - 0.1, dur), 1.0)
        return camf, st, sfx

    # ---------------- the demo
    if sid == "demo_walkout":
        ta = wt("arm")
        p_abs = sh["start"] + ta
        tick_events(sh, p_abs, sfx, beeps)
        sfx.append((ta, "click"))
        camf = cam_path([(0, V((44, -190, 160)), FRONT), (ta + 1.4, V((46, -200, 168)), FRONT),
                         (dur, V((60, -420, 330)), CENTER + V((10, -20, 0)))])

        def st(t):
            scr = SCR_READY if t < ta else countdown_screen(sh["start"] + t, p_abs)
            base_state(t, scr, pr=press(t, ta))
        return camf, st, sfx

    if sid in ("demo_cookie", "demo_back"):
        tc_abs = word_abs("s30", "caught")
        tp_abs = word_abs("s31", "press")
        siren_events(sh, tc_abs, tp_abs, sfx, beeps)
        if sid == "demo_cookie":
            tc = tc_abs - sh["start"]
            path = hand_path(CATCH_KEYS(tc, dur, 0.0))
            camf = cam_path([(0, V((98, -325, 208)), V((126, -40, 14))), (dur, V((106, -298, 190)), V((124, -40, 14)))])

            def st(t):
                base_state(t, SCR_ARMED if t < tc else SCR_INTRUDER, props={"hand", "jar"}, heat=0.55)
                pos, yaw = path(t)
                place_hand(pos, yaw, 0.08)
                parts_pir.set_zones(BEAMS, lit_by_path(path, t), idle=0.05 if t < tc else 0.0)
                set_out_glow(fade(t, tc - 0.05, dur + 1, 0.1))
            return camf, st, sfx
        tp = tp_abs - sh["start"]
        sfx.append((tp, "click"))
        camf = cam_path([(0, V((44, -195, 165)), FRONT), (dur, V((36, -160, 135)), FRONT + V((-2, 6, 2)))])

        def st(t):
            base_state(t, SCR_INTRUDER if t < tp else SCR_SEEN(1, "12 s ago"), pr=press(t, tp))
        return camf, st, sfx

    # ---------------- common problem
    if sid == "mistake_false":
        ta, tu, twm, ttk, tkeep = wt("arm"), wt("Usually"), wt("warming"), wt("time"), wt("keeps")
        p_abs = sh["start"] + ta - 10.0
        tick_events(sh, p_abs, sfx, beeps)
        tm = ta + 0.35
        tstop = tu + 0.45
        siren_events(sh, sh["start"] + tm, sh["start"] + tstop, sfx, beeps)
        sfx.append((tstop, "click"))
        camf = cam_path([(0, V((50, -200, 160)), V((58, 2, 14))), (tu, V((55, -185, 150)), V((62, 4, 14))),
                         (dur, PT + V((-40, -120, 75)), PT + V((-4, -10, -8)))])

        def st(t):
            if t < ta:
                scr = countdown_screen(sh["start"] + t, p_abs)
            elif t < tm:
                scr = SCR_ARMED
            elif t < tstop:
                scr = SCR_INTRUDER
            else:
                scr = SCR_SEEN(1, "%d s ago" % int(t - tm))
            base_state(t, scr, pr=press(t, tstop))
            high = t >= tm - 0.6
            parts_pir.set_zones(BEAMS, {i: 0.5 for i in range(9)} if tm - 0.6 <= t < tm + 0.4 else {})
            set_out_glow(1.0 if high else 0.0)
            TAGS["warming"]["set"](fade(t, twm - 0.2, dur), 1.0)
            move_tag("knob", pot_world("time"))
            TAGS["knob"]["set"](fade(t, ttk - 0.2, dur), 1.0)
            TAGS["outstate"]["text"] = "OUT stays HIGH"
            TAGS["outstate"]["set"](fade(t, tkeep - 0.2, dur), 1.0)
        return camf, st, sfx

    if sid == "mistake_fix":
        tw, tturn, tdown, tcode = wt("wait"), wt("turn"), wt("down"), wt("code")
        tp = tcode - 0.1
        tick_events(sh, sh["start"] + tp, sfx, beeps)
        sfx.append((tp, "click"))
        camf = cam_path([(0, PT + V((-50, -130, 80)), PT + V((-5, -8, 0))), (tturn - 0.6, PT + V((-14, -84, 54)), PT + V((0, -4, 12))),
                         (tdown + 0.4, PT + V((-10, -80, 52)), PT + V((0, -4, 12))), (dur, V((50, -200, 150)), V((62, 6, 14)))])

        def st(t):
            scr = SCR_READY if t < tp else countdown_screen(sh["start"] + t, sh["start"] + tp)
            base_state(t, scr, pr=press(t, tp))
            secs = int(30 * smooth((t - tw) / 2.2))
            TAGS["warm"]["text"] = "wait 30 s after power-on: %d s" % secs
            TAGS["warm"]["set"](fade(t, tw - 0.1, tturn - 0.8), 1.0)
            lift_pir(smooth((t - (tturn - 0.7)) / 0.7) * (1 - smooth((t - (tdown + 0.5)) / 0.7)))
            pir["pot_time"].rotation_euler.z = POT_HI + (POT_LO - POT_HI) * smooth((t - tturn) / (tdown - tturn + 0.2))
            move_tag("knobmin", pot_world("time"))
            TAGS["knobmin"]["set"](fade(t, tdown - 0.2, tdown + 0.9), 1.0)
        return camf, st, sfx

    # ---------------- challenge + outro
    if sid == "challenge":
        tu, tpl = wt("unplugging"), wt("Preferences")
        sfx += [(tu, "unplug"), (tpl + 0.2, "plug")]
        camf = cam_path([(0, V((40, -150, 125)), OC + V((-8, -14, 0))), (tu - 0.3, V((10, -170, 135)), (OC + USBP) / 2),
                         (tpl + 0.6, V((0, -165, 130)), (OC + USBP) / 2), (dur, V((40, -110, 95)), OC + V((-2, -6, 0)))])

        def st(t):
            pull = smooth((t - tu) / 0.3) - smooth((t - tpl) / 0.3)
            off = tu + 0.1 <= t < tpl + 0.3
            if off:
                scr = None
            elif t < tu:
                scr = SCR_SEEN(3, "5 min ago")
            else:
                scr = show("caught so far: 3", "warming..")
            base_state(t, scr, pull=pull, pwr=not off)
            TAGS["saved"]["set"](fade(t, tpl + 1.0, dur), 1.0)
        return camf, st, sfx

    if sid == "outro":
        camf = orbit(CENTER + V((0, 0, 0)), 260, 210, -80, -122, dur)

        def st(t):
            base_state(t, show("see you in", "ep 12"))
            parts_pir.set_zones(BEAMS, {}, idle=0.035 + 0.025 * math.sin(t * 2.5))
        return camf, st, sfx

    raise KeyError("no spec for shot " + sid)


# ======================================================================= render
os.makedirs(OUT, exist_ok=True)
sc.render.image_settings.file_format = "PNG"
index = []
OVL = {}
ANCH = {}
LAST_BEEPS = []
for sh in SHOTS:
    if ONLY and sh["id"] not in ONLY:
        continue
    camf, st, sfx = shot_spec(sh)
    cam.data.dof.aperture_fstop = FSTOP.get(sh["id"], 10.0)
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
        bp = world_to_camera_view(sc, cam, STATE["anchor"] * MM)  # sounding buzzer on screen, for the 2D sound waves
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
