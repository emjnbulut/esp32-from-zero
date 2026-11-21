"""Episode 10 v2 - every Blender 3D shot of the episode, timed to the narration.

    blender -b -P video/ep10/b3d/ep10_3d.py -- [--shots open_play,wire_power] [--frames 1,40] [--stills] [--cycles]

Timing: video/ep10/build/schedule.json (EN narration, word times). Without it the timing is estimated from
script.json (2.45 words/s) so shots can be previewed before the voice exists. A shot = a run of consecutive
segments whose vis is "b3d:<id>"; its length = from the first segment's start to the next segment's start.
Output: video/ep10/b3d/build/shots/<id>/f_0001.png ... + shots.json (start, frames, sfx events).
--stills renders 3 frames per shot (start, middle, end) into build/stills/ for a quick look.
Circuit (pbl.py layout, front board F, back board B):
  B4e->B r+ 4 (3V3)  B5d->B r- 5 (GND)  OLED B34f..37f GND VCC SCL SDA, B34j->r- 34, B35j->r+ 35
  B17e->B36h green SCL (D22)  B14e->B37g blue SDA (D21)  button B24/26 e,f; B13d->B24d yellow (D19); B26j->r- 26
  buzzer F30c(+)/F33c; F13i->F30a orange (D32); F5h->F l- 5 (GND); F33a->F l- 33
"""
import json
import math
import os
import re
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
EP = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(EP, "..", "b3d"))
import pbl  # noqa: E402
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


def word_t(shot, word, nth=0, seg=None):
    """time of a spoken word, relative to the shot start (first match, or nth match)"""
    want = re.sub(r"[^a-z0-9]", "", word.lower())
    k = 0
    for sid in ([seg] if seg else shot["segs"]):
        s = SEGS[sid]
        for w in s["words"]:
            if re.sub(r"[^a-z0-9]", "", w["w"].lower()).startswith(want):
                if k == nth:
                    return s["start"] + w["t"] - shot["start"]
                k += 1
    raise KeyError(f"{shot['id']}: word {word!r} #{nth} not found")


# ======================================================================= scene
k = pbl.Kit(fps=FPS, engine="CYCLES" if "--cycles" in argv else "EEVEE")
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32"})
usb = k.usb_cable()
cam, tgt = k.camera(lens=50, fstop=10.0)
oled = k.oled(B, (34, 35, 36, 37), "f")
btn = k.button([B.hole(24, "e"), B.hole(26, "e"), B.hole(24, "f"), B.hole(26, "f")])
bz = k.buzzer(F.hole(30, "c"), F.hole(33, "c"))
xray = k.buzzer_xray()
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
rings = k.sound_rings(bz["top"], 3)
k.lights(center=(0.035, 0.0, 0.0), key=2.2)
k.glare(threshold=2.5)
sc = k.scene

TAGS = {}


def tag(name, text, at, color="#ffb547", lift=9.0):
    TAGS[name] = k.tag(text, at, color, lift)
    return TAGS[name]


# hole / pin tags used in the wiring shots
tag("b4e", "B 4e  3V3", B.hole(4, "e"), "#ff6b6b")
tag("rplus", "+ line", B.rail(4, "r", "+"), "#ff6b6b")
tag("b5d", "B 5d  GND", B.hole(5, "d"), "#c3cbd7")
tag("rminus", "- line", B.rail(5, "r", "-"), "#c3cbd7")
tag("oledcol", "B 34f-37f", B.hole(35, "f"), "#2dd4bf", lift=14)
tag("d22", "D22  B 17e", B.hole(17, "e"), "#2fbf71")
tag("scl", "SCL  B 36h", B.hole(36, "h"), "#2fbf71")
tag("d21", "D21  B 14e", B.hole(14, "e"), "#5b9cff", lift=13)
tag("sda", "SDA  B 37g", B.hole(37, "g"), "#5b9cff", lift=13)
tag("d19", "D19  B 13d", B.hole(13, "d"), "#f2c037")
tag("btnpin", "B 24d", B.hole(24, "d"), "#f2c037")
tag("d32", "D32  F 13i", F.hole(13, "i"), "#ff8a2a")
tag("bzplus", "+  F 30a", F.hole(30, "a"), "#ff8a2a")
tag("bzgnd", "GND", F.hole(5, "h"), "#c3cbd7")
tag("row24", "row 24 · e", B.hole(24, "e"), "#2dd4bf")
for nm, row, col in (("GND", 34, "#c3cbd7"), ("VCC", 35, "#ff6b6b"), ("SCL", 36, "#2fbf71"), ("SDA", 37, "#5b9cff")):
    tag("pin_" + nm, nm, B.hole(row, "f") + Vector((0, 0, 3.8)), col, lift=6 + (row - 34) * 2.2)

# ======================================================================= helpers
OC = oled["center"]
BT = btn["top"]
BZ = bz["top"]
USBP = Vector((esp["xU"] - 8, 0, 14))
MID = (OC + BT) / 2
CENTER = Vector((35, 0, 0))


def vis(group, on):
    for o in [group] + list(group.children_recursive):
        o.hide_render = not on


PARTS = {"oled": oled["group"], "button": btn["group"], "buzzer": bz["group"]}
press_obj = btn["press"]
PRESS_Z = press_obj.location.z
BASE_Z = {n: g.location.z for n, g in PARTS.items()}


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
        kk = wires.get(n, 0.0)
        w["draw"](kk)
        for o in w["group"].children_recursive:
            if o.name.startswith(n + "_tip") or o.name == n:
                pass
    if "buzzer" in parts:
        pass


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


def set_rings(t, beeps):
    """beeps: list of (time, kind); kind 'hi' small fast rings, 'lo' slow wide"""
    for idx, (ob, val) in enumerate(rings):
        a, s = 0.0, 1.0
        for tb, kind in beeps:
            span = 0.45 if kind != "lo" else 0.7
            u = (t - tb - idx * (0.07 if kind != "lo" else 0.15)) / span
            if 0 <= u <= 1:
                a = max(a, (1 - u) ** 1.5)
                s = 6.5 + (14 if kind != "lo" else 22) * u
        ob.scale = (s, s, 1)
        val.outputs[0].default_value = a


def wire_k(t, t0, dur=0.7):
    return smooth((t - t0) / dur)


def fade(t, t0, t1, ramp=0.25):
    """1 inside [t0, t1] with soft edges"""
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


def show(top, big):
    return Screen().show(top, big)


SCR_READY = lambda best="214": show("REFLEX 2.0  best:", best + "ms")  # noqa: E731
SCR_WAIT = show("get ready...", "WAIT")
SCR_GO = show("", " GO!")


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


V = Vector
ALL_W = {n: 1.0 for n in W}
ALL_P = {"oled", "button", "buzzer"}


# ======================================================================= shots
def shot_spec(sh):
    """returns (camera f(t), state f(t) -> None, sfx list [(t, kind)])"""
    sid, dur = sh["id"], sh["end"] - sh["start"]
    wt = lambda w, n=0: word_t(sh, w, n)  # noqa: E731
    sfx = []
    beeps = []

    def base_state(t, scr, parts=ALL_P, wires=ALL_W, pr=0.0, pull=0.0, pwr=True, drop=None):
        show_parts(parts, wires, drop, t)
        set_press(pr)
        set_usb(pull)
        set_pwr(pwr)
        k.set_screen(scr)
        set_rings(t, beeps)
        if "buzzer" in parts and not (drop and "buzzer" in drop and t < drop["buzzer"]):
            xray(0.0)
        for tg in TAGS.values():
            tg["set"](0.0)

    if sid == "open_play":
        go = wt("GO")
        hit = go + 0.214
        beeps += [(go, "hi"), (hit + 0.45, "hi"), (hit + 0.65, "hi"), (hit + 0.85, "hi")]
        sfx += [(go, "beep_hi"), (hit, "click"), (hit + 0.45, "record")]
        camf = cam_path([(0, V((44, -150, 140)), MID + V((-4, -6, 0))), (dur, V((50, -112, 100)), MID + V((0, -2, 2)))])

        def st(t):
            scr = SCR_WAIT if t < go else (SCR_GO if t < hit else show("NEW RECORD!", "214ms"))
            base_state(t, scr, pr=press(t, hit))
        return camf, st, sfx

    if sid == "open_unplug":
        tp = wt("pull")
        sfx += [(tp, "unplug")]
        camf = cam_path([(0, V((10, -150, 120)), (MID + USBP) / 2), (min(dur, 1.6), V((-55, -120, 95)), USBP + V((4, 0, 0))),
                         (dur, V((-50, -112, 88)), USBP + V((6, 0, 0)))])

        def st(t):
            pull = smooth((t - tp) / 0.35)
            off = t >= tp + 0.12
            base_state(t, None if off else show("NEW RECORD!", "214ms"), pull=pull, pwr=not off)
        return camf, st, sfx

    if sid == "open_replug":
        tp = wt("plug")
        sfx += [(tp + 0.25, "plug"), (tp + 0.4, "boot")]
        camf = cam_path([(0, V((-50, -112, 88)), USBP + V((6, 0, 0))), (tp + 0.6, V((-35, -135, 110)), USBP + V((20, 0, 0))),
                         (dur, V((44, -92, 82)), OC + V((0, -2, 0)))])

        def st(t):
            pull = 1 - smooth((t - tp) / 0.3)
            on = t >= tp + 0.3
            scr = None if not on else (Screen() if t < tp + 0.8 else SCR_READY())
            base_state(t, scr, pull=pull, pwr=on)
        return camf, st, sfx

    if sid == "open_orbit":
        camf = orbit(CENTER + V((-5, 5, 0)), 230, 175, -115, -55, dur)
        return camf, lambda t: base_state(t, SCR_READY()), sfx

    if sid == "oled_hero":
        camf = cam_path([(0, V((70, -140, 120)), OC), (dur, V((50, -70, 60)), OC + V((0, 0, 0)))])
        return camf, lambda t: base_state(t, SCR_READY()), sfx

    if sid == "oled_macro":
        tb = wt("black")
        camf = cam_path([(0, OC + V((-6, -34, 26)), OC + V((-4, 0, 0))), (dur, OC + V((4, -26, 20)), OC + V((2, 0, 0)))])

        def st(t):
            scr = SCR_READY() if t < tb else show("", " GO!")
            base_state(t, scr)
        return camf, st, sfx

    if sid == "oled_pins":
        tpw, tpic = wt("power"), wt("pictures")
        camf = cam_path([(0, OC + V((-10, -60, 55)), OC + V((0, 8, 0))), (dur, OC + V((6, -48, 48)), OC + V((0, 10, 0)))])

        def st(t):
            base_state(t, SCR_READY())
            for i, nm in enumerate(("GND", "VCC", "SCL", "SDA")):
                t0 = 0.4 + i * 0.25
                hot = (nm in ("GND", "VCC") and t >= tpw) or (nm in ("SCL", "SDA") and t >= tpic)
                TAGS["pin_" + nm]["set"](smooth((t - t0) / 0.3), 0.55 * (1.15 if hot else 0.85))
        return camf, st, sfx

    if sid == "buzzer_hero":
        camf = cam_path([(0, BZ + V((-60, -95, 70)), BZ), (dur, BZ + V((-20, -70, 48)), BZ + V((0, 0, -2)))])
        return camf, lambda t: base_state(t, SCR_READY()), sfx

    if sid == "buzzer_cut":
        th, tl = wt("high"), wt("low")
        beeps += [(th + i * 0.12, "hi") for i in range(4)] + [(tl + i * 0.3, "lo") for i in range(3)]
        sfx += [(th, "tone_hi_long"), (tl, "tone_lo_long")]
        camf = cam_path([(0, BZ + V((-20, -62, 40)), BZ + V((0, 0, -3))), (dur, BZ + V((14, -50, 34)), BZ + V((0, 0, -3)))])

        def st(t):
            base_state(t, SCR_READY())
            xr = smooth((t - 0.3) / 0.6)
            bend = 0.0
            if th <= t < th + 1.0:
                bend = math.sin((t - th) * 2 * math.pi * 9)
            elif tl <= t < tl + 1.2:
                bend = math.sin((t - tl) * 2 * math.pi * 2.5)
            xray(xr, bend)
        return camf, st, sfx

    if sid == "button_hero":
        tp = wt("pin")
        sfx += [(1.0, "click")]
        camf = cam_path([(0, BT + V((-40, -90, 75)), BT), (dur, BT + V((-10, -60, 50)), BT + V((-4, 0, -2)))])

        def st(t):
            base_state(t, SCR_READY(), pr=press(t, 1.0, 0.2))
            TAGS["d19"]["set"](fade(t, tp - 0.2, dur), 0.55)
        return camf, st, sfx

    # ---------------- wiring
    if sid == "wire_overview":
        camf = cam_path([(0, V((30, -230, 260)), CENTER + V((-5, 5, 0))), (dur, V((30, -170, 230)), CENTER + V((-5, 8, 0)))])

        def st(t):
            base_state(t, Screen(), parts=set(), wires={})
            TAGS["row24"]["set"](fade(t, wt("number") - 0.2, dur - 0.3), 1.1)
        return camf, st, sfx

    if sid == "wire_power":
        tr, tb = wt("red"), wt("black")
        sfx += [(tr, "snap"), (tb, "snap")]
        tgtp = V((-5, 40, 9))
        camf = cam_path([(0, tgtp + V((-30, -110, 105)), tgtp), (dur, tgtp + V((-10, -88, 88)), tgtp + V((2, 0, 0)))])

        def st(t):
            base_state(t, Screen(), parts=set(), wires={"pwr_red": wire_k(t, tr), "pwr_blk": wire_k(t, tb)})
            TAGS["b4e"]["set"](fade(t, tr - 0.3, dur), 0.8)
            TAGS["rplus"]["set"](fade(t, tr + 0.4, dur), 0.8)
            TAGS["b5d"]["set"](fade(t, tb - 0.3, dur), 0.8)
            TAGS["rminus"]["set"](fade(t, tb + 0.4, dur), 0.8)
        return camf, st, sfx

    if sid == "wire_oled":
        td, tpw = wt("legs"), wt("power")
        sfx += [(td + 0.4, "pop"), (tpw, "snap"), (tpw + 0.4, "snap")]
        camf = cam_path([(0, OC + V((-40, -120, 110)), OC + V((0, 8, 0))), (dur, OC + V((-5, -85, 85)), OC + V((2, 10, 0)))])
        pw = {"pwr_red": 1.0, "pwr_blk": 1.0}

        def st(t):
            w = dict(pw, oled_gnd=wire_k(t, tpw), oled_vcc=wire_k(t, tpw + 0.4))
            base_state(t, Screen(), parts={"oled"}, wires=w, drop={"oled": td}, pwr=True)
            TAGS["oledcol"]["set"](fade(t, td + 0.3, dur), 0.9)
        return camf, st, sfx

    if sid == "wire_i2c":
        tg, tbl = wt("green"), wt("blue")
        sfx += [(tg, "snap"), (tbl, "snap")]
        cpt = V((25, 25, 9))
        camf = cam_path([(0, cpt + V((-20, -120, 110)), cpt), (dur, cpt + V((5, -100, 100)), cpt + V((5, 2, 0)))])
        pw = {"pwr_red": 1.0, "pwr_blk": 1.0, "oled_gnd": 1.0, "oled_vcc": 1.0}

        def st(t):
            w = dict(pw, scl=wire_k(t, tg, 0.9), sda=wire_k(t, tbl, 0.9))
            base_state(t, Screen(), parts={"oled"}, wires=w)
            TAGS["d22"]["set"](fade(t, tg - 0.3, dur), 0.85)
            TAGS["scl"]["set"](fade(t, tg + 0.6, dur), 0.85)
            TAGS["d21"]["set"](fade(t, tbl - 0.3, dur), 0.85)
            TAGS["sda"]["set"](fade(t, tbl + 0.6, dur), 0.85)
        return camf, st, sfx

    if sid == "wire_button":
        tbn, ty, tgd = wt("button"), wt("Yellow"), wt("ground")
        sfx += [(tbn + 0.4, "pop"), (ty, "snap"), (tgd, "snap")]
        cpt = BT + V((-8, 0, -6))
        camf = cam_path([(0, cpt + V((-30, -105, 95)), cpt), (dur, cpt + V((-6, -85, 82)), cpt + V((2, 0, 0)))])
        pw = {n: 1.0 for n in ("pwr_red", "pwr_blk", "oled_gnd", "oled_vcc", "scl", "sda")}

        def st(t):
            w = dict(pw, btn=wire_k(t, ty), btn_gnd=wire_k(t, tgd))
            base_state(t, Screen(), parts={"oled", "button"}, wires=w, drop={"button": tbn})
            TAGS["d19"]["set"](fade(t, ty - 0.3, dur), 0.8)
            TAGS["btnpin"]["set"](fade(t, ty + 0.4, dur), 0.8)
        return camf, st, sfx

    if sid == "wire_buzzer":
        tbz, to, tgd = wt("buzzer"), wt("Orange"), wt("ground")
        sfx += [(tbz + 0.4, "pop"), (to, "snap"), (tgd, "snap"), (tgd + 0.4, "snap")]
        cpt = V((10, -38, 9))
        camf = cam_path([(0, cpt + V((-20, -120, 110)), cpt), (dur, cpt + V((5, -95, 92)), cpt + V((4, 2, 0)))])
        pw = {n: 1.0 for n in ("pwr_red", "pwr_blk", "oled_gnd", "oled_vcc", "scl", "sda", "btn", "btn_gnd")}

        def st(t):
            w = dict(pw, bz=wire_k(t, to, 0.8), bz_gnd1=wire_k(t, tgd), bz_gnd2=wire_k(t, tgd + 0.4))
            base_state(t, Screen(), parts=ALL_P, wires=w, drop={"buzzer": tbz})
            TAGS["d32"]["set"](fade(t, to - 0.3, dur), 0.85)
            TAGS["bzplus"]["set"](fade(t, to + 0.5, dur), 0.85)
            TAGS["bzgnd"]["set"](fade(t, tgd - 0.2, dur), 0.85)
        return camf, st, sfx

    if sid == "wire_done":
        camf = orbit(CENTER + V((-5, 0, 0)), 200, 190, -100, -70, dur)
        sfx += [(0.3, "boot")]

        def st(t):
            base_state(t, SCR_READY("9999") if t > 0.3 else Screen())
        return camf, st, sfx

    # ---------------- the game
    if sid == "screen_hello":
        tc = wt("call")
        sfx += [(tc, "blip")]
        camf = cam_path([(0, OC + V((-10, -75, 70)), OC), (dur, OC + V((0, -58, 55)), OC + V((0, 1, 0)))])
        return camf, lambda t: base_state(t, show("hello from", "Pin1") if t >= tc else Screen()), sfx

    if sid == "play_go":
        go = wt("GO")
        beeps.append((go, "hi"))
        sfx += [(go, "beep_hi")]
        camf = cam_path([(0, V((40, -130, 120)), MID), (dur, V((46, -105, 95)), MID + V((0, 0, 1)))])
        return camf, lambda t: base_state(t, SCR_WAIT if t < go else SCR_GO), sfx

    if sid == "play_press":
        tp = wt("press")
        sfx += [(tp, "click")]
        camf = cam_path([(0, V((30, -100, 95)), MID), (dur, V((38, -92, 84)), MID + V((0, 0, 1)))])
        return camf, lambda t: base_state(t, SCR_GO if t < tp else show("your time", "263ms"), pr=press(t, tp)), sfx

    if sid == "play_false":
        te = wt("early")
        beeps.append((te + 0.05, "lo"))
        sfx += [(te, "click"), (te + 0.05, "beep_lo")]
        camf = cam_path([(0, V((50, -120, 105)), MID), (dur, V((44, -100, 92)), MID)])
        return camf, lambda t: base_state(t, SCR_WAIT if t < te else show("false start", "OOPS"), pr=press(t, te)), sfx

    if sid == "play_rounds":
        t1, t2 = wt("fifty"), wt("eighty")
        g1, g2 = t1 - 0.55, t2 - 0.48
        beeps += [(g1 - 0.35, "hi"), (g2 - 0.28, "hi")]
        sfx += [(g1 - 0.35, "beep_hi"), (g1, "click"), (g2 - 0.28, "beep_hi"), (g2, "click")]
        camf = orbit(MID, 110, 95, -100, -80, dur)

        def st(t):
            if t < g1 - 0.35:
                scr = SCR_WAIT
            elif t < g1:
                scr = SCR_GO
            elif t < g1 + 1.0:
                scr = show("your time", "350ms")
            elif t < g2 - 0.28:
                scr = SCR_WAIT
            elif t < g2:
                scr = SCR_GO
            else:
                scr = show("your time", "280ms")
            base_state(t, scr, pr=press(t, g1) + press(t, g2))
        return camf, st, sfx

    if sid == "prefs_proof":
        t14 = wt("fourteen")
        tu, tpl = wt("Unplug"), wt("plug", 1)
        hit = t14 - 0.6
        beeps += [(hit + 0.2, "hi")]
        sfx += [(hit, "click"), (hit + 0.2, "record"), (tu, "unplug"), (tpl + 0.2, "plug"), (tpl + 0.4, "boot")]
        camf = cam_path([(0, V((44, -110, 98)), MID), (tu - 0.2, V((10, -150, 120)), (MID + USBP) / 2),
                         (tpl + 0.6, V((-30, -140, 115)), (USBP + MID) / 2), (dur, V((44, -95, 86)), OC)])

        def st(t):
            pull = smooth((t - tu) / 0.3) - smooth((t - tpl) / 0.3)
            off = tu + 0.1 <= t < tpl + 0.3
            if off:
                scr = None
            elif t < hit:
                scr = SCR_GO
            elif t < tu:
                scr = show("NEW RECORD!", "214ms")
            elif t < tpl + 0.8:
                scr = Screen()
            else:
                scr = SCR_READY()
            base_state(t, scr, pr=press(t, hit), pull=pull, pwr=not off)
        return camf, st, sfx

    if sid == "challenge":
        th = wt("hold")
        te = th + 3.0
        beeps.append((te, "lo"))
        sfx += [(th, "click"), (te, "tone_erase")]
        camf = cam_path([(0, BT + V((-20, -95, 85)), MID), (dur, BT + V((0, -80, 75)), MID + V((0, 0, 1)))])

        def st(t):
            held = th <= t < te + 0.6
            scr = SCR_READY() if t < te else (show("record erased", "----") if t < te + 2.5 else SCR_READY("9999"))
            base_state(t, scr, pr=-0.9 if held else 0.0)
        return camf, st, sfx

    if sid == "outro":
        camf = orbit(CENTER + V((-5, 0, 0)), 240, 200, -80, -120, dur)
        return camf, lambda t: base_state(t, show("see you in", "ep 11")), sfx

    raise KeyError("no spec for shot " + sid)


# ======================================================================= render
os.makedirs(OUT, exist_ok=True)
sc.render.image_settings.file_format = "PNG"
index = []
OVL = {}
for sh in SHOTS:
    if ONLY and sh["id"] not in ONLY:
        continue
    camf, st, sfx = shot_spec(sh)
    n = max(1, round((sh["end"] - sh["start"]) * FPS))
    index.append({"id": sh["id"], "segs": sh["segs"], "start": sh["start"], "frames": n,
                  "sfx": [{"t": round(sh["start"] + t, 3), "kind": kd} for t, kd in sfx]})
    if STILLS:
        frames = sorted({1, n // 2 + 1, n})
        outdir = os.path.join(OUT, "stills")
    else:
        frames = FRAMES or list(range(1, n + 1))
        outdir = os.path.join(OUT, "shots", sh["id"])
    os.makedirs(outdir, exist_ok=True)
    for f in frames:
        path = os.path.join(outdir, (sh["id"] + "_" if STILLS else "") + f"f_{f:04d}.png")
        if os.path.exists(path) and not (STILLS or FRAMES):
            continue
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
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        print("frame", sh["id"], f, "/", n, flush=True)
if not STILLS and not FRAMES:
    for sid, frames_ov in OVL.items():
        json.dump(frames_ov, open(os.path.join(OUT, "shots", sid, "overlay.json"), "w"))
elif STILLS:
    for sid, frames_ov in OVL.items():
        json.dump(frames_ov, open(os.path.join(OUT, "stills", sid + "_overlay.json"), "w"))
prev = []
ip = os.path.join(OUT, "shots.json")
if os.path.exists(ip) and ONLY:
    prev = [x for x in json.load(open(ip)) if x["id"] not in {i["id"] for i in index}]
json.dump(sorted(prev + index, key=lambda x: x["start"]), open(ip, "w"), indent=1)
print("shots:", len(index))
