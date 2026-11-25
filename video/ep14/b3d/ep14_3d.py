"""Episode 14 (DRAFT) - every Blender 3D shot of "I Turned Bananas into a Piano", timed to the narration.

    blender -b -P video/ep14/b3d/ep14_3d.py -- [--shots open_play,replay] [--frames 1,40] [--stills] [--top] [--cycles]

Same pipeline as video/ep12/b3d/ep12_3d.py. Timing: video/ep14/build/schedule.json (EN narration, word times). A shot =
a run of consecutive segments whose vis is "b3d:<id>"; its length = from the first segment's start to the next
segment's start. Output: video/ep14/b3d/build/shots/<id>/f_0001.png ... + overlay.json/anchors.json per shot +
shots.json (start, frames, sfx events, beeps). --stills renders 3 frames per shot into build/stills/. --top renders a
top-down check of the wire routes (build/stills/_top.png).

Behaviour follows lessons/14-fruit-piano/code/fruit_piano/fruit_piano.ino, simulated by Piano below:
  KEY_PIN {14, 2, 15} = banana / apple / orange, NOTE {523, 659, 784}, NAME {"DO", "MI", "SOL"}
  touch -> tone(NOTE, 200) + show("touch a fruit", NAME); hold the button >= 1 s (on release) -> show("record: touch 8", "REC")
  recording -> show("recording N/8", NAME), the 8th note -> show("saved 8 notes", "PRESS")
  short press -> playBack(): tone(NOTE, 250) + show("playing", NAME) every 320 ms, then show("touch a fruit", "PIANO")
  setup() -> show("don't touch...", "CALIBRATE"), 500 ms, then "touch a fruit" / "PIANO"
  challenge (README, not in the sketch): banana + orange together = high DO, 1047 Hz.
Circuit = the Ep 10 layout (ep12_3d.py minus the RGB LED / phone):
  B4e->B r+ 4 (3V3)  B5d->B r- 5 (GND)  OLED B34f..37f, B34j->r- 34, B35j->r+ 35  B17e->B36h green SCL (D22)
  B14e->B37g blue SDA (D21)  button B24/26 e,f; B13d->B24d yellow (D19); B26j->r- 26
  buzzer F30c(+)/F33c; F13i->F30a orange (D32); F5h->F l- 5 (GND); F33a->F l- 33
  + touch wires: F8g (D14) purple -> banana, B7c (D2) white -> apple, B6e (D15) teal -> orange (the fruit lie on the
  desk in front of / right of the breadboard; each wire ends in the fruit's wire_point from parts_ep14.py).
"""
import json
import math
import os
import re
import sys

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
EP = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EP))
sys.path.insert(0, os.path.join(EP, "..", "b3d"))
sys.path.insert(0, HERE)
import parts_ep11 as px  # noqa: E402
import parts_ep14 as p14  # noqa: E402
import pbl  # noqa: E402
from oledfont import Screen  # noqa: E402
from parts_ep12 import _emit_val_mat  # noqa: E402
from pbl import MM, P, TOP, smooth  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default


ONLY = opt("--shots", "").split(",") if opt("--shots") else None
FRAMES = [int(x) for x in opt("--frames").split(",")] if opt("--frames") else None
STILLS = "--stills" in argv
FPS = 30
OUT = os.path.join(HERE, "build")
V = Vector


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


# ======================================================================= the sketch, simulated
NOTE = [523, 659, 784]
NAME = ["DO", "MI", "SOL"]
FRUIT = ["banana", "apple", "orange"]
HIGH_DO = 1047


def show(top, big):
    """the sketch's show(): textSize(1) at (0,0), textSize(2) at (0,28)"""
    s = Screen()
    s.text(0, 0, top, 1)
    s.text(0, 28, big, 2)
    return s


SCR_PIANO = show("touch a fruit", "PIANO")
SCR_REC = show("record: touch 8", "REC")


class Piano:
    """event-driven copy of fruit_piano.ino. events: (t, kind, arg) with kind touch(key 0..2) / down / up / boot /
    hido (the challenge). Produces a screen timeline and the buzzer notes [(t, freq, key, dur)]."""

    def __init__(self, scr0=SCR_PIANO, recording=False, song=(), calib=0.5):
        self.calib = calib
        self.tl = [(-1e9, scr0)]
        self.notes = []
        self.recording = recording
        self.song = list(song)
        self.down = None
        self.busy = -1e9

    def scr(self, t, s):
        self.tl.append((t, s))

    def run(self, events):
        for t, kind, arg in sorted(events, key=lambda e: e[0]):
            if t < self.busy and kind in ("touch", "down", "up", "hido"):
                continue  # playBack() blocks loop()
            if kind == "touch":
                self.notes.append((t, NOTE[arg], arg, 0.2))
                if self.recording and len(self.song) < 8:
                    self.song.append(arg)
                    self.scr(t, show("recording %d/8" % len(self.song), NAME[arg]))
                    if len(self.song) == 8:
                        self.recording = False
                        self.scr(t + 0.001, show("saved 8 notes", "PRESS"))
                elif not self.recording:
                    self.scr(t, show("touch a fruit", NAME[arg]))
            elif kind == "hido":
                self.notes.append((t, HIGH_DO, -1, 0.2))
                self.scr(t, show("touch a fruit", "HIGH DO"))
            elif kind == "down":
                self.down = t
            elif kind == "up":
                if self.down is not None and t - self.down >= 1.0:
                    self.recording = True
                    self.song = []
                    self.scr(t, SCR_REC)
                elif self.song and not self.recording:
                    for i, key in enumerate(self.song):
                        self.notes.append((t + 0.32 * i, NOTE[key], key, 0.25))
                        self.scr(t + 0.32 * i, show("playing", NAME[key]))
                    self.busy = t + 0.32 * len(self.song)
                    self.scr(self.busy, SCR_PIANO)
            elif kind == "boot":
                self.scr(t, None)  # power cycle: screen dark
                self.scr(t + 0.15, show("don't touch...", "CALIBRATE"))
                self.scr(t + 0.15 + self.calib, SCR_PIANO)
        self.tl.sort(key=lambda x: x[0])
        return self

    def screen(self, t):
        s = self.tl[0][1]
        for tt, sc in self.tl:
            if tt <= t:
                s = sc
        return s

    def export(self, sfx, beeps):
        for t, f, key, dur in self.notes:
            name = "HIDO" if key < 0 else NAME[key]
            sfx.append((t, "fp_%s%s" % (name.lower(), "_pb" if dur > 0.21 else "")))
            beeps.append((t, "hi", f, name, key))


# ======================================================================= scene
k = pbl.Kit(fps=FPS, engine="CYCLES" if "--cycles" in argv else "EEVEE")
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32", "D14", "D2", "D15"})
usb = k.usb_cable()
cam, tgt = k.camera(lens=50, fstop=10.0)
oled = k.oled(B, (34, 35, 36, 37), "f")
btn = k.button([B.hole(24, "e"), B.hole(26, "e"), B.hole(24, "f"), B.hole(26, "f")])
bz = k.buzzer(F.hole(30, "c"), F.hole(33, "c"))
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

# ---- fruit
BAN = p14.banana(k, (52, -104, 0), yaw_deg=6)
APL = p14.apple(k, (136, -108, 0))
ORG = p14.orange(k, (194, -100, 0))
FR = {"banana": BAN, "apple": APL, "orange": ORG}
GLOW_COL = {"banana": "#ffd166", "apple": "#ff6b6b", "orange": "#ffa62b"}
GLOW = {"banana": p14.touch_glow(k, BAN["centre"] + V((0, 0, 1)), GLOW_COL["banana"], radius=30, name="glow_banana"),
        "apple": p14.touch_glow(k, APL["centre"], GLOW_COL["apple"], radius=28, name="glow_apple"),
        "orange": p14.touch_glow(k, ORG["centre"], GLOW_COL["orange"], radius=27, name="glow_orange")}
_gb = bpy.data.objects["glow_banana"]
_gb.scale = (1.75, 0.55, 0.62)
_gb.rotation_euler = (0, 0, math.radians(6))


# ---- touch wires (dense smooth polyline, so the 'touch' pulse can ride along it exactly)
def _catmull(pts, n_per=24):
    """centripetal Catmull-Rom through pts -> dense list"""
    pts = [V(p) for p in pts]
    ext = [pts[0] * 2 - pts[1]] + pts + [pts[-1] * 2 - pts[-2]]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        t0 = 0.0
        t1 = t0 + max(1e-4, (p1 - p0).length ** 0.5)
        t2 = t1 + max(1e-4, (p2 - p1).length ** 0.5)
        t3 = t2 + max(1e-4, (p3 - p2).length ** 0.5)
        for j in range(n_per):
            t = t1 + (t2 - t1) * j / n_per
            a1 = p0 * ((t1 - t) / (t1 - t0)) + p1 * ((t - t0) / (t1 - t0))
            a2 = p1 * ((t2 - t) / (t2 - t1)) + p2 * ((t - t1) / (t2 - t1))
            a3 = p2 * ((t3 - t) / (t3 - t2)) + p3 * ((t - t2) / (t3 - t2))
            b1 = a1 * ((t2 - t) / (t2 - t0)) + a2 * ((t - t0) / (t2 - t0))
            b2 = a2 * ((t3 - t) / (t3 - t1)) + a3 * ((t - t1) / (t3 - t1))
            out.append(b1 * ((t2 - t) / (t2 - t1)) + b2 * ((t - t1) / (t2 - t1)))
    out.append(pts[-1])
    return out


def _resample(pts, n):
    d = [0.0]
    for a, b in zip(pts, pts[1:]):
        d.append(d[-1] + (b - a).length)
    L = d[-1]
    out, j = [], 0
    for i in range(n):
        s = L * i / (n - 1)
        while j < len(d) - 2 and d[j + 1] < s:
            j += 1
        u = (s - d[j]) / max(1e-9, d[j + 1] - d[j])
        out.append(pts[j].lerp(pts[j + 1], u))
    return out, L


def fruit_wire(name, hole, ctrl, fruit, color):
    """jumper from a breadboard hole, over the board, along the desk, pushed into the fruit's wire_point"""
    hole = V(hole)
    wp = V(fruit["wire_point"])
    c = V(fruit["centre"])
    out = V((wp.x - c.x, wp.y - c.y, max(0.0, wp.z - c.z))).normalized()
    if name == "w14":  # banana: outward = away from the banana's axis, front-top
        out = V((0.08, -0.8, 0.6)).normalized()
    pts = [hole + V((0, 0, 2.4)), hole + V((0, 0, 7.0))] + [V(p) for p in ctrl] + [wp + out * 7.0, wp]
    poly, L = _resample(_catmull(pts), 220)
    g = k.empty("wg_" + name)
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.62
    cu.bevel_resolution = 3
    cu.use_fill_caps = True
    try:
        cu.bevel_factor_mapping_end = "SPLINE"
    except (TypeError, AttributeError):
        pass
    sp = cu.splines.new("POLY")
    sp.points.add(len(poly) - 1)
    for p_, q in zip(sp.points, poly):
        p_.co = (q.x, q.y, q.z, 1.0)
    ob = bpy.data.objects.new(name, cu)
    cu.materials.append(k.mat("wire_" + color, pbl.COL.get(color, color), 0.38, coat=0.35))
    k._link(ob, g)
    tip = k.mat("tip", "#c8ced6", 0.25, metal=1.0)
    ta = k.cyl(name + "_tipA", 0.33, 3.6, (hole.x, hole.y, TOP + 0.6), tip, g, segs=12)

    def draw(x):
        x = max(0.0, min(1.0, x))
        cu.bevel_factor_end = max(0.001, x)
        ob.hide_render = x <= 0.0
        ta.hide_render = x <= 0.0

    def at(u):
        """point at fraction u (0 = hole, 1 = fruit) along the wire"""
        u = max(0.0, min(1.0, u))
        f = u * (len(poly) - 1)
        i = min(len(poly) - 2, int(f))
        return poly[i].lerp(poly[i + 1], f - i)

    return {"group": g, "draw": draw, "at": at, "len": L, "hole": hole, "fruit": fruit}


FW = {}
FW["w14"] = fruit_wire("w14", F.hole(8, "g"), [(-24, -36, 15), (-21, -58, 11), (-22, -76, 0.65), (-12, -112, 0.65),
                                               (8, -127, 0.65), (25, -125, 4.0)], BAN, "purple")
FW["w2"] = fruit_wire("w2", B.hole(7, "c"), [(-27, 6, 25), (-24, -16, 26), (-15, -40, 19), (-9, -60, 10), (-6, -76, 0.65),
                                             (20, -77, 0.65), (96, -77, 0.65), (106, -96, 0.65), (106, -117, 2.5),
                                             (109, -122, 13)], APL, "white")
FW["w15"] = fruit_wire("w15", B.hole(6, "e"), [(-30, 10, 28), (-28, -14, 30), (-22, -42, 24), (-15, -62, 12),
                                               (-12, -84, 0.65), (20, -85, 0.65), (156, -85, 0.65), (166, -97, 0.65),
                                               (165, -111, 3.0), (166, -112, 13)], ORG, "#2dd4bf")
WIRE_OF = {"banana": "w14", "apple": "w2", "orange": "w15"}

# ---- on-board blue LED (GPIO 2), next to the red power LED
BLUE_M, BLUE_V = _emit_val_mat("blueled", "#4aa3ff", 40.0)
_blue_body = k.box("esp_blue_body", (1.6, 1.0, 0.7), (esp["xU"] + 9.5, 0.4, esp["pcb_top"] + 0.35),
                   k.mat("blueledbody", "#1a2a55", 0.4), esp["group"])
_blue = k.box("esp_blue", (1.7, 1.1, 0.72), (esp["xU"] + 9.5, 0.4, esp["pcb_top"] + 0.37), BLUE_M, esp["group"])
BLUE_LED = V((esp["xU"] + 9.5, 0.4, esp["pcb_top"] + 0.8))

# ---- 'hold 1 s' ring around the button
_rc = bpy.data.curves.new("recring", "CURVE")
_rc.dimensions = "3D"
_rc.bevel_depth = 0.75
_rc.bevel_resolution = 2
try:
    _rc.bevel_factor_mapping_end = "SPLINE"
except (TypeError, AttributeError):
    pass
_sp = _rc.splines.new("POLY")
_N = 96
_sp.points.add(_N)
for _i, _p in enumerate(_sp.points):
    _a = math.pi / 2 - 2 * math.pi * _i / _N  # clockwise from 12 o'clock (seen from the front camera)
    _p.co = (10.0 * math.cos(_a), 10.0 * math.sin(_a), 0, 1)
REC_RING = bpy.data.objects.new("recring", _rc)
_rc.materials.append(k._emit_mat("recring_m", "#ff4d5e", 6.0))
k._link(REC_RING)
REC_RING.location = btn["top"] + V((0, 0, -3.6))

# ---- red X (key plays by itself)
XG = k.empty("redx", APL["top"] + V((0, 0, 32)))
_xm = k._emit_mat("redx_m", "#ff3b3b", 7.0)
for _s in (1, -1):
    _b = k.box("redx_bar", (2.6, 2.6, 17.0), (0, 0, 0), _xm, XG, bevel=0.8)
    _b.rotation_euler = (0, math.radians(45 * _s), 0)

# ---- wire pulse (a glowing bead + trail riding a touch wire)
PULSE = []
for _i in range(6):
    _m = k._emit_mat("pulse_m%d" % _i, "#ffd166", 9.0 * (1 - _i / 7))
    PULSE.append(k.mesh("pulse%d" % _i, px._sphere(1.0, 16, 10), _m, (0, 0, 0)))


def set_pulse(wire, u, trail=0.035):
    for i, ob in enumerate(PULSE):
        uu = None if u is None else u - trail * i * 0.5
        if wire is None or uu is None or not (0.0 <= uu <= 1.0):
            ob.hide_render = True
            continue
        ob.hide_render = False
        ob.location = FW[wire]["at"](uu)
        s = 2.1 * (1 - i / 7)
        ob.scale = (s, s, s * 0.9)


# ---- pointing hands (index finger out, the rest curled into a fist), right hand + a mirrored left hand
def pointing_hand(scale=0.78, name="hand", mirror=False):
    g = k.empty(name)
    g.scale = (scale, -scale if mirror else scale, scale)
    m = px.heat_mat(k, name + "_heat", "#e2a283", "#ffd166")
    bm = k.bm_box(32, 28, 11)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=3.5, segments=2, affect="EDGES")
    palm = px._flat(k, name + "_palm", bm, m, (16, 0, 0.5), g)
    sub = palm.modifiers.new("subsurf", "SUBSURF")
    sub.levels = sub.render_levels = 2
    ip, il, ir = 0.22, 28.0, 4.0
    kn = V((32, 9.6, 0.8))  # index knuckle
    px._capsule(k, name + "_index", ir, il, kn, 0.0, ip, m, g, segs=16)
    for i, (y, r) in enumerate(((3.2, 4.2), (-3.6, 4.1), (-10.0, 3.7))):  # curled: down, then back under the palm
        b0 = V((31, y, -0.5))
        px._capsule(k, f"{name}_c{i}a", r, 6.5, b0, 0.0, 1.5, m, g, segs=14)
        b1 = b0 + V((math.cos(1.5) * 6.5, 0, -math.sin(1.5) * 6.5))
        px._capsule(k, f"{name}_c{i}b", r * 0.95, 7.0, b1, math.pi, 0.25, m, g, segs=14)
    px._capsule(k, name + "_thumb", 4.4, 15, (13, 12.5, -3.0), 0.3, 0.75, m, g, segs=14)
    px._flat(k, name + "_wrist", px._sphere(11.5, 20, 12), m, (0, 0, 0.5), g, scale=(1, 1.15, 0.78))
    arm = k.bm_cyl(11.0, 170, 24, r2=12.5)
    px._flat(k, name + "_arm", arm, m, (-85, 0, 0.5), g, rot=(0, -math.pi / 2, 0), scale=(1, 1.15, 0.85))
    for o in g.children_recursive:
        if o.type == "MESH" and hasattr(o.data, "shade_smooth"):
            o.data.shade_smooth()
    d = V((math.cos(ip), 0, -math.sin(ip)))
    tipc = kn + d * il  # centre of the fingertip sphere (local)
    return {"group": g, "heat": [m], "tipc": tipc, "r": ir * scale, "scale": scale, "mirror": mirror, "dloc": d}


HAND = pointing_hand(0.78, "hand")
HAND_L = pointing_hand(0.78, "handL", mirror=True)


def _rot(yaw, pitch):
    from mathutils import Euler
    return Euler((0.0, pitch, yaw), "XYZ").to_matrix()


def place_hand(H, tip, yaw, pitch, lift=0.0):
    """put the fingertip sphere centre at `tip` (mm); lift 0..: the finger backs off along itself and up"""
    R = _rot(yaw, pitch)
    s = H["scale"]
    S = V((s, -s if H["mirror"] else s, s))
    tl = H["tipc"]
    fdir = R @ V((H["dloc"].x, H["dloc"].y * (-1 if H["mirror"] else 1), H["dloc"].z))
    tip = V(tip) + lift * (-fdir * 16.0 + V((0, 0, 12.0)))
    loc = tip - R @ V((tl.x * S.x, tl.y * S.y, tl.z * S.z))
    g = H["group"]
    g.location = loc
    g.rotation_euler = (0.0, pitch, yaw)


# ---- touch targets: fingertip centre resting on the surface (closest point from an approach point outside)
bpy.context.view_layer.update()
DG = bpy.context.evaluated_depsgraph_get()


def surface_point(ob, p_mm):
    ev = ob.evaluated_get(DG)
    mw = ob.matrix_world
    ok, loc, nrm, _ = ev.closest_point_on_mesh(mw.inverted() @ (V(p_mm) * MM))
    pw = (mw @ loc) / MM
    nw = (mw.to_3x3() @ nrm).normalized()
    return pw, nw


TG = {}
FRUIT_YAW = math.radians(150)  # right hand: fingers point left/back, the arm comes in from the right side
for nm, fr, appr in (("banana", BAN, V((10, -8, 26))), ("apple", APL, V((12, -8, 30))), ("orange", ORG, V((12, -8, 30)))):
    p_, n_ = surface_point(bpy.data.objects[nm + "_body"], fr["centre"] + appr)
    TG[nm] = {"tip": p_ + n_ * HAND["r"] * 0.85, "yaw": FRUIT_YAW, "pitch": 0.5, "surf": p_}
# left hand (challenge): from the left, fingers pointing right
p_, n_ = surface_point(bpy.data.objects["banana_body"], BAN["centre"] + V((-12, -6, 26)))
TG["banana_L"] = {"tip": p_ + n_ * HAND["r"] * 0.85, "yaw": math.radians(25), "pitch": 0.5, "surf": p_}
# left hand on the button: from behind the board, finger toward the camera (keeps the OLED and the ESP32 clear)
TG["button"] = {"tip": V((btn["top"].x, btn["top"].y, TOP + 3.8 + 4.5 + HAND["r"] * 0.85)), "yaw": math.radians(-75),
                "pitch": 0.8}
TG["away"] = {"tip": V((215, -170, 75)), "yaw": FRUIT_YAW, "pitch": 0.5}
TG["away_btn"] = {"tip": V((5, 95, 85)), "yaw": math.radians(-75), "pitch": 0.8}
TG["away_L"] = {"tip": V((-70, -150, 75)), "yaw": math.radians(25), "pitch": 0.5}

k.lights(center=(0.07, -0.04, 0.0), key=2.2)
k.glare(threshold=2.5)
sc = k.scene

TAGS = {}


def tag(name, text, at, color="#ffb547", lift=9.0):
    TAGS[name] = k.tag(text, at, color, lift)
    TAGS[name]["text0"] = text
    TAGS[name]["color0"] = color
    TAGS[name]["lift"] = lift
    return TAGS[name]


OC = oled["center"]
BT = btn["top"]
BZ = bz["top"]
ESPC = V((-17, 0, 14))
PIN14 = k.pin("f", 10)
PIN2 = k.pin("b", 11)
PIN15 = k.pin("b", 12)

tag("do", "do", BAN["top"] + V((-4, 0, -23)), GLOW_COL["banana"], lift=14)
tag("mi", "mi", APL["top"] + V((0, 0, -6)), GLOW_COL["apple"], lift=12)
tag("sol", "sol", ORG["top"] + V((0, 0, -6)), GLOW_COL["orange"], lift=12)
NOTE_TAG = ["do", "mi", "sol"]
tag("new", "new", APL["top"], "#2fbf71", lift=26)
tag("ep10", "episode 10", OC + V((0, 4, 0)), "#2dd4bf", lift=16)
tag("g14", "GPIO 14", PIN14, "#c4a5ff", lift=12)
tag("g2", "GPIO 2", PIN2, "#e9edf2", lift=12)
tag("g15", "GPIO 15", PIN15, "#2dd4bf", lift=22)
tag("tpins", "touch pins", ESPC + V((5, 0, 3)), "#ffd166", lift=26)
tag("stay_oled", "stays", OC + V((0, 4, 0)), "#2dd4bf", lift=12)
tag("stay_btn", "stays", BT, "#f2c037", lift=10)
tag("stay_bz", "stays", BZ, "#ff8a2a", lift=10)
tag("p14", "pin 14", F.hole(8, "g"), "#c4a5ff", lift=12)
tag("p2", "pin 2", B.hole(7, "c"), "#e9edf2", lift=14)
tag("p15", "pin 15", B.hole(6, "e"), "#2dd4bf", lift=22)
tag("led2", "pin 2 = blue LED too", BLUE_LED, "#5b9cff", lift=12)
tag("hold", "hold 1 s", BT, "#ff6b8b", lift=12)
tag("short", "short press", BT, "#ffd166", lift=12)
tag("song", "song", OC + V((0, 4, 0)), "#ffd166", lift=20)
tag("bytself", "plays by itself!", APL["top"] + V((0, 0, 41)), "#ff6b6b", lift=8)
tag("measure", "touched while measuring", APL["top"], "#ff6b6b", lift=10)
tag("handsoff", "hands off!", APL["top"], "#2fbf71", lift=10)
tag("tnum", "touch: 48", ORG["top"] + V((0, 0, -6)), "#ffa62b", lift=12)
tag("needs", "needs < 40", ORG["centre"] + V((10, -14, 0)), "#ff6b6b", lift=40)
tag("drop", "DROP 20", OC + V((0, 4, 0)), "#ffd166", lift=16)
tag("hido", "high do?", (BAN["top"] + ORG["top"]) / 2 + V((0, 0, 8)), "#ffd166", lift=14)
tag("nonew", "4th note, no new pin", ESPC + V((5, 0, 3)), "#2dd4bf", lift=22)

# ======================================================================= helpers
PARTS = {"oled": oled["group"], "button": btn["group"], "buzzer": bz["group"]}
press_obj = btn["press"]
PRESS_Z = press_obj.location.z
ALL_W = {n: 1.0 for n in W}
ALL_FW = {n: 1.0 for n in FW}
STATE = {"anchor": BZ}


def vis(group, on):
    for o in [group] + list(group.children_recursive):
        o.hide_render = not on


def set_pwr(on):
    k.pwr_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0 if on else 0.0


def set_rings(t, beeps, center=None):
    for idx, (ob, val) in enumerate(rings):
        ob.location = center if center is not None else BZ
        a, s = 0.0, 1.0
        for b in beeps:
            tb = b[0]
            u = (t - tb - idx * 0.07) / 0.45
            if 0 <= u <= 1:
                a = max(a, (1 - u) ** 1.5)
                s = 6.5 + 14 * u
        ob.scale = (s, s, 1)
        val.outputs[0].default_value = a


def fade(t, t0, t1, ramp=0.25):
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


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
        p = center + V((radius * math.cos(a), radius * math.sin(a), height))
        return p, center + V((0, 0, lift_target))
    return f


# a press/touch sequence: [(t, target, hold)] -> hand key poses + the sketch's input events
def hand_keys(seq, t_end, start=None, end=None, lift_hover=0.7, app=0.28):
    keys = []
    if start:
        keys.append((0.0, start[0], start[1]))
    for i, (tc, tg, hd) in enumerate(seq):
        prev_rel = seq[i - 1][0] + seq[i - 1][2] if i else (0.0 if not start else -1.0)
        nxt = seq[i + 1][0] if i + 1 < len(seq) else t_end + 1.0
        a = min(app, max(0.04, 0.32 * (tc - prev_rel))) if i or start else app
        b = min(app, max(0.04, 0.32 * (nxt - tc - hd)))
        keys += [(tc - a, tg, lift_hover), (tc, tg, 0.0), (tc + hd, tg, 0.0), (tc + hd + b, tg, lift_hover)]
    if end:
        keys.append((max(keys[-1][0] + 0.3, end[2] if len(end) > 2 else keys[-1][0] + 0.5), end[0], end[1]))
    keys.sort(key=lambda x: x[0])
    return keys


def hand_at(keys, t):
    """eased pose between keys -> (tip, yaw, pitch, lift)"""
    def pose(kk):
        g = TG[kk[1]]
        return g["tip"], g["yaw"], g["pitch"], kk[2]
    if t <= keys[0][0]:
        return pose(keys[0])
    for a, b in zip(keys, keys[1:]):
        if t <= b[0]:
            u = smooth((t - a[0]) / max(1e-6, b[0] - a[0]))
            pa, pb = pose(a), pose(b)
            tip = pa[0].lerp(pb[0], u)
            travel = (pa[0] - pb[0]).length
            arc = math.sin(math.pi * u) * min(1.2, travel / 60.0) if travel > 1 else 0.0
            return tip, pa[1] + (pb[1] - pa[1]) * u, pa[2] + (pb[2] - pa[2]) * u, pa[3] + (pb[3] - pa[3]) * u + arc
    return pose(keys[-1])


def seq_events(seq):
    ev = []
    for tc, tg, hd in seq:
        if tg == "button":
            ev += [(tc, "down", None), (tc + hd, "up", None)]
        elif tg in FRUIT:
            ev.append((tc, "touch", FRUIT.index(tg)))
    return ev


def pressed_at(seq, t):
    return any(tg == "button" and tc <= t < tc + hd for tc, tg, hd in seq)


def contacts(seq, t):
    """fruit glow levels from finger contacts"""
    lv = {f: 0.0 for f in FRUIT}
    for tc, tg, hd in seq:
        f = tg.split("_")[0]
        if f not in lv or t < tc:
            continue
        if t < tc + hd:
            lv[f] = max(lv[f], 0.75 + 0.15 * math.sin((t - tc) * 14))
        else:
            lv[f] = max(lv[f], 0.75 * math.exp(-(t - tc - hd) / 0.22))
    return lv


def note_tags(t, beeps, stay=False, hold=0.55):
    for i, nm in enumerate(NOTE_TAG):
        last = None
        first = None
        for b in beeps:
            if b[4] == i and b[0] <= t + 0.03:
                last = b[0]
                first = b[0] if first is None else first
        if last is None:
            continue
        age = t - last
        on = 1.0 if stay else (1.0 - smooth((age - hold) / 0.3))
        TAGS[nm]["set"](max(TAGS[nm]["on"], on), 1.0 + 0.35 * max(0.0, 1 - max(0.0, age) / 0.25))


def beep_glow(t, beeps, lv, k_=0.6):
    """playback: the fruit of each note glows softly (no finger)"""
    for b in beeps:
        if b[4] >= 0 and 0 <= t - b[0] <= 0.5:
            f = FRUIT[b[4]]
            lv[f] = max(lv[f], k_ * (1 - (t - b[0]) / 0.5))
    return lv


# ---- camera presets (mm)
DESK_T = V((98, -52, 14))
DESK_P = DESK_T + V((-14, -322, 236))
WIDE_T = V((86, -40, 12))
WIDE_P = WIDE_T + V((-18, -370, 275))
FRUIT_T = V((124, -104, 18))
FRUIT_P = FRUIT_T + V((-10, -235, 150))
BOARD_T = V((28, -8, 8))
BOARD_P = BOARD_T + V((-6, -228, 205))


# ======================================================================= shots
def shot_spec(sh):
    """returns (camera f(t), state f(t) -> None, sfx list [(t, kind)])"""
    sid, dur = sh["id"], sh["end"] - sh["start"]
    wt = lambda w, n=0: word_t(sh, w, n)  # noqa: E731
    sfx = []
    beeps = []
    global LAST_BEEPS
    LAST_BEEPS = beeps

    def base_state(t, scr, wires=ALL_W, fwires=ALL_FW, pwr=True, glow=None, blue=0.0):
        for n, g in PARTS.items():
            vis(g, True)
        for n, w in W.items():
            w["draw"](wires.get(n, 0.0))
        for n, w in FW.items():
            w["draw"](fwires.get(n, 0.0))
        press_obj.location.z = PRESS_Z
        set_pwr(pwr)
        k.set_screen(scr)
        STATE["anchor"] = BZ
        set_rings(t, beeps)
        for tg in TAGS.values():
            tg["set"](0.0)
            tg["text"] = tg["text0"]
            tg["color"] = tg["color0"]
        vis(HAND["group"], False)
        vis(HAND_L["group"], False)
        for f in FRUIT:
            GLOW[f]((glow or {}).get(f, 0.0))
        BLUE_V.outputs[0].default_value = blue
        REC_RING.hide_render = True
        vis(XG, False)
        set_pulse(None, None)

    def hand_state(t, keys, seq, H=HAND):
        if not keys:
            return
        tip, yaw, pitch, lift = hand_at(keys, t)
        if pressed_at(seq, t) and H is HAND_L:
            press_obj.location.z = PRESS_Z - 1.2
            tip = tip - V((0, 0, 1.2))
        vis(H["group"], True)
        place_hand(H, tip, yaw, pitch, lift)

    def tap_sfx(seq):
        for tc, tg, hd in seq:
            sfx.append((tc, "click" if tg == "button" else "tap"))
            if tg == "button":
                sfx.append((tc + hd, "click"))

    def play_shot(seq, piano, camf, startR=None, endR=None, startL=None, endL=None, stay=False, extra=None,
                  glow_pb=True):
        """button presses = left hand (from behind the board), fruit touches = right hand (from the right)"""
        seqL = [x for x in seq if x[1] == "button"]
        seqR = [x for x in seq if x[1] != "button"]
        keysR = hand_keys(seqR, dur, start=startR, end=endR) if seqR else None
        keysL = hand_keys(seqL, dur, start=startL, end=endL) if seqL else None
        piano.run(seq_events(seq))
        piano.export(sfx, beeps)
        tap_sfx(seq)

        def st(t):
            lv = contacts(seq, t)
            if glow_pb:
                lv = beep_glow(t, [b for b in beeps if not any(tg in FRUIT and abs(tc - b[0]) < 0.02
                                                                for tc, tg, _ in seq)], lv)
            base_state(t, piano.screen(t), glow=lv)
            hand_state(t, keysR, seq, HAND)
            hand_state(t, keysL, seq, HAND_L)
            note_tags(t, beeps, stay=stay)
            if extra:
                extra(t)
        return camf, st, sfx

    # ---------------- cold open
    if sid == "open_play":
        seq = [(wt("do") - 0.15, "banana", 0.3), (wt("mi") - 0.15, "apple", 0.3), (wt("sol") - 0.15, "orange", 0.3)]
        camf = cam_path([(0, DESK_P + V((35, 25, -15)), DESK_T + V((22, -15, 0))),
                         (dur, DESK_P + V((25, 45, -30)), DESK_T + V((20, -20, 0)))])
        return play_shot(seq, Piano(), camf, startR=("banana", 1.0), endR=("away", 0.0, dur + 0.4), stay=True)

    if sid == "open_tune":
        song = [0, 1, 2, 2, 1, 0, 1, 2]
        t0 = 1.85
        seq = [(0.2, "button", 1.15)] + [(t0 + 0.15 * i, FRUIT[n], 0.07) for i, n in enumerate(song)]
        tpress = wt("and") + 0.05
        seq.append((tpress, "button", 0.14))
        camf = cam_path([(0, WIDE_P + V((-10, 30, -20)), WIDE_T), (dur, WIDE_P + V((10, 60, -45)), WIDE_T + V((0, -8, 0)))])
        return play_shot(seq, Piano(), camf, startR=("banana", 1.3), endR=("away", 0.0, 3.6), startL=("button", 0.8),
                         endL=("away_btn", 0.0, dur + 0.5))

    if sid == "open_orbit":
        ttouch = wt("touch")
        camf = orbit(V((80, -48, 0)), 395, 250, -112, -66, dur, lift_target=14.0)

        def st(t):
            base_state(t, SCR_PIANO)
            TAGS["tpins"]["set"](fade(t, ttouch - 0.2, dur), 1.0)
        return camf, st, sfx

    if sid == "open_title":
        tfr, tev = wt("fruit"), wt("Everything")
        camf = cam_path([(0, WIDE_P + V((30, 20, 10)), WIDE_T + V((5, 0, 0))), (dur, WIDE_P + V((0, 50, -25)), WIDE_T)])

        def st(t):
            base_state(t, SCR_PIANO)
            TAGS["new"]["set"](fade(t, tfr - 0.2, dur), 1.0)
            TAGS["ep10"]["set"](fade(t, tev - 0.1, dur), 1.0)
        return camf, st, sfx

    if sid == "touch_pins":
        ttch, t14, t2, t15 = wt("touch"), wt("fourteen"), wt("two"), wt("fifteen")
        cpt = V((-24, -2, 12))
        camf = cam_path([(0, cpt + V((30, -150, 150)), cpt + V((10, 0, 0))), (dur, cpt + V((10, -105, 112)), cpt)])

        def st(t):
            base_state(t, SCR_PIANO)
            TAGS["tpins"]["set"](fade(t, ttch - 0.2, t14 - 0.4), 1.0)
            TAGS["g14"]["set"](fade(t, t14 - 0.1, dur), 1.0 + 0.3 * max(0, 1 - (t - t14) / 0.3) * (t >= t14))
            TAGS["g2"]["set"](fade(t, t2 - 0.1, dur), 1.0 + 0.3 * max(0, 1 - (t - t2) / 0.3) * (t >= t2))
            TAGS["g15"]["set"](fade(t, t15 - 0.1, dur), 1.0 + 0.3 * max(0, 1 - (t - t15) / 0.3) * (t >= t15))
        return camf, st, sfx

    if sid == "touch_banana":
        tpass, tkey = wt("passes"), wt("key")
        seq = [(0.45, "banana", dur)]
        keys = hand_keys(seq, dur, start=("banana", 1.0))
        t_p0, t_p1 = tpass - 0.1, tpass + 1.5
        piano = Piano()
        piano.run([(t_p1, "touch", 0)])  # the note sounds when the pulse arrives (slow-motion picture)
        piano.export(sfx, beeps)
        sfx.append((0.45, "tap"))
        bt = BAN["top"] + V((-14, 0, -18))
        camf = cam_path([(0, bt + V((40, -150, 85)), bt + V((0, 0, 0))), (t_p0, bt + V((30, -160, 95)), bt + V((-8, 4, 0))),
                         (t_p1, V((-4, -205, 150)), V((-14, -50, 8))), (dur, V((0, -225, 168)), V((-12, -48, 8)))])

        def st(t):
            lv = contacts(seq, t)
            base_state(t, piano.screen(t), glow=lv)
            hand_state(t, keys, seq)
            if t_p0 <= t <= t_p1 + 0.2:
                set_pulse("w14", 1.0 - (t - t_p0) / (t_p1 - t_p0), trail=-0.035)
            TAGS["g14"]["set"](fade(t, t_p1 - 0.15, dur), 1.0 + 0.3 * max(0, 1 - (t - t_p1) / 0.3) * (t >= t_p1))
            note_tags(t, beeps, stay=True)
        return camf, st, sfx

    # ---------------- wiring
    if sid == "wire_keep":
        tscr, tbtn, tbz = wt("screen"), wt("button"), wt("buzzer")
        camf = cam_path([(0, BOARD_P + V((10, -10, 10)), BOARD_T + V((5, 0, 0))), (dur, BOARD_P + V((10, 15, -10)), BOARD_T)])

        def st(t):
            base_state(t, SCR_PIANO, fwires={})
            TAGS["stay_oled"]["set"](fade(t, tscr - 0.1, dur), 1.0)
            TAGS["stay_btn"]["set"](fade(t, tbtn - 0.1, dur), 1.0)
            TAGS["stay_bz"]["set"](fade(t, tbz - 0.1, dur), 1.0)
        return camf, st, sfx

    if sid == "wire_fruit":
        t14, tban, t2, tapl, t15, torg, tpush = (wt("fourteen"), wt("banana"), wt("two"), wt("apple"), wt("fifteen"),
                                                 wt("orange"), wt("push"))
        grow = {"w14": (t14 - 0.2, tban + 0.35), "w2": (t2 - 0.2, tapl + 0.35), "w15": (t15 - 0.2, torg + 0.3)}
        for w, (a, b) in grow.items():
            sfx.append((b, "snap"))
        camf = cam_path([(0, WIDE_P + V((-30, 40, -30)), WIDE_T + V((-15, -10, 0))),
                         (t15, WIDE_P + V((0, 30, -30)), WIDE_T + V((10, -20, 0))),
                         (tpush - 0.6, WIDE_P + V((20, 40, -40)), WIDE_T + V((20, -30, 0))),
                         (dur, V((134, -265, 118)), V((150, -112, 14)))])

        def st(t):
            fw = {w: smooth((t - a) / (b - a)) for w, (a, b) in grow.items()}
            base_state(t, SCR_PIANO, fwires=fw)
            TAGS["p14"]["set"](fade(t, t14 - 0.1, tpush - 0.5), 1.0)
            TAGS["p2"]["set"](fade(t, t2 - 0.1, tpush - 0.5), 1.0)
            TAGS["p15"]["set"](fade(t, t15 - 0.1, tpush - 0.5), 1.0)
            for nm, fr in (("do", "banana"), ("mi", "apple"), ("sol", "orange")):
                w = WIRE_OF[fr]
                TAGS[nm]["set"](fade(t, grow[w][1] - 0.1, tpush - 0.5), 1.0)
        return camf, st, sfx

    if sid == "wire_led":
        tblue, tglow = wt("blue"), wt("glows")
        camf = cam_path([(0, V((-10, -150, 130)), V((-30, -2, 12))), (dur, BLUE_LED + V((8, -62, 58)), BLUE_LED)])

        def st(t):
            lvl = smooth((t - 0.4) / 0.6) * (0.10 + 0.05 * math.sin(t * 9) + (0.08 if t > tglow else 0.0))
            base_state(t, SCR_PIANO, blue=lvl)
            TAGS["led2"]["set"](fade(t, tblue - 0.2, dur), 1.0)
        return camf, st, sfx

    # ---------------- record + replay
    if sid == "rec_hold":
        thold, tone_, trec = wt("hold"), wt("one"), wt("REC", 1)  # #0 would be "record"
        tdown = thold + 0.05
        tup = trec - 1.0
        seq = [(tdown, "button", tup - tdown)]
        keys = hand_keys(seq, dur, start=("button", 1.0), end=("away_btn", 0.0, tup + 1.2))
        piano = Piano().run(seq_events(seq))
        tap_sfx(seq)
        camf = cam_path([(0, BT + V((15, -130, 115)), (BT + OC) / 2), (tup, BT + V((20, -100, 95)), (BT + OC) / 2 + V((3, 0, 0))),
                         (dur, OC + V((0, -70, 68)), OC + V((-3, 0, 0)))])

        def st(t):
            base_state(t, piano.screen(t))
            hand_state(t, keys, seq, HAND_L)
            prog = max(0.0, min(1.0, (t - tdown) / 1.0)) if t < tup else 0.0
            if prog > 0:
                REC_RING.hide_render = False
                _rc.bevel_factor_end = max(0.002, prog)
            TAGS["hold"]["set"](fade(t, tdown - 0.1, tup), 1.0)
        return camf, st, sfx

    if sid == "rec_play":
        words = [("Do", 0), ("mi", 0), ("sol", 0), ("sol", 1), ("mi", 1), ("do", 1), ("mi", 2), ("sol", 2)]
        song = [0, 1, 2, 2, 1, 0, 1, 2]
        seq = [(wt(w, n) - 0.08, FRUIT[song[i]], 0.1) for i, (w, n) in enumerate(words)]
        piano = Piano(scr0=SCR_REC, recording=True)
        camf = cam_path([(0, DESK_P + V((10, 40, -30)), DESK_T + V((0, -8, 0))),
                         (dur, DESK_P + V((-10, 65, -50)), DESK_T + V((-8, -2, 0)))])

        def extra(t):
            n = sum(1 for tc, _, _ in seq if tc <= t)
            TAGS["song"]["text"] = "song  " + "●" * n + "○" * (8 - n)
            TAGS["song"]["set"](1.0, 1.0)
        return play_shot(seq, piano, camf, startR=("banana", 1.0), endR=("away", 0.0, dur + 0.6), extra=extra)

    if sid == "replay":
        tpress = wt("press") + 0.02
        seq = [(tpress, "button", 0.14)]
        piano = Piano(scr0=show("saved 8 notes", "PRESS"), song=[0, 1, 2, 2, 1, 0, 1, 2])
        camf = cam_path([(0, DESK_P + V((-10, 50, -35)), DESK_T + V((-10, 0, 0))),
                         (dur, DESK_P + V((10, 30, -20)), DESK_T + V((0, -6, 0)))])

        def extra(t):
            TAGS["short"]["set"](fade(t, tpress - 0.2, tpress + 0.9), 1.0)
        return play_shot(seq, piano, camf, startL=("button", 1.0), endL=("away_btn", 0.0, tpress + 0.9), extra=extra)

    # ---------------- troubles
    if sid == "trouble_calm":
        titself, tus, ttch, tmeas, trst, thand = (wt("plays"), wt("Usually"), wt("touched"), wt("measuring"), wt("restart"),
                                                  wt("hands"))
        self_t = [0.9, titself - 0.1, titself + 0.55]  # the apple fires with nobody touching it
        tboot1 = ttch - 0.3
        tboot2 = trst + 0.25
        seq = [(tboot1 + 0.05, "apple", 2.0)]  # arrives while the board is dark, rests through CALIBRATE
        keys = hand_keys(seq, dur, start=("away", 0.0), end=("away", 0.0, tboot1 + 2.8))
        piano = Piano(scr0=SCR_PIANO, calib=1.6)  # the 500 ms measuring screen, held longer so it can be read
        ev = [(x, "touch", 1) for x in self_t] + [(tboot1, "boot", None), (tboot2, "boot", None)]
        piano.run(ev)
        piano.export(sfx, beeps)
        sfx += [(tboot1, "unplug"), (tboot1 + 0.05, "plug"), (tboot2, "unplug"), (tboot2 + 0.05, "plug")]
        camf = cam_path([(0, FRUIT_P + V((-30, 10, 40)), FRUIT_T + V((-18, 30, 6))),
                         (tus, FRUIT_P + V((-40, 0, 50)), FRUIT_T + V((-26, 36, 6))),
                         (dur, FRUIT_P + V((-48, -5, 55)), FRUIT_T + V((-30, 40, 6)))])

        def st(t):
            on = not (tboot1 <= t < tboot1 + 0.15 or tboot2 <= t < tboot2 + 0.15)
            lv = {"apple": 0.0, "banana": 0.0, "orange": 0.0}
            for x in self_t:
                if 0 <= t - x <= 0.5:
                    lv["apple"] = max(lv["apple"], 0.7 * (1 - (t - x) / 0.5))
            base_state(t, piano.screen(t), pwr=on, glow=lv)
            hand_state(t, keys, seq)
            xs = max([1.0 - smooth((t - x - 0.6) / 0.3) if t >= x - 0.02 else 0.0 for x in self_t] + [0.0])
            if xs > 0.02 and t < tus:
                vis(XG, True)
                age = min(t - x for x in self_t if t >= x - 0.02)
                s = xs * (1.0 + 0.3 * max(0.0, 1 - age / 0.2))
                XG.scale = (s, s, s)
            TAGS["bytself"]["set"](fade(t, titself - 0.3, tus - 0.3), 1.0)
            TAGS["measure"]["set"](fade(t, ttch - 0.1, trst - 0.4), 1.0)
            TAGS["handsoff"]["set"](fade(t, thand - 0.2, dur), 1.0)
            note_tags(t, beeps)
        return camf, st, sfx

    if sid == "trouble_drop":
        tnever, tdrop, tval, tcount = wt("never"), wt("drop"), wt("value"), wt("counts")
        seq = [(tnever - 0.15, "orange", 1.15), (tcount - 0.1, "orange", 0.5)]
        keys = hand_keys(seq, dur, start=("orange", 1.4), end=("away", 0.0, dur + 0.6))
        piano = Piano().run([(tcount - 0.1, "touch", 2)])  # the first touch is too weak: no note
        piano.export(sfx, beeps)
        tap_sfx(seq)
        camf = cam_path([(0, FRUIT_P + V((50, -10, 10)), FRUIT_T + V((40, 0, 4))),
                         (tdrop - 0.3, FRUIT_P + V((15, 0, 25)), FRUIT_T + V((25, 12, 4))),
                         (dur, FRUIT_P + V((20, -10, 30)), FRUIT_T + V((28, 8, 4)))])

        def st(t):
            lv = contacts(seq, t)
            if t < tcount - 0.1:
                lv["orange"] *= 0.25  # touched, but not enough
            base_state(t, piano.screen(t), glow=lv)
            hand_state(t, keys, seq)
            TAGS["tnum"]["set"](fade(t, tnever - 0.2, dur), 1.0)
            TAGS["needs"]["text"] = "needs < 50" if t >= tval + 0.3 else "needs < 40"
            TAGS["needs"]["color"] = "#2fbf71" if t >= tval + 0.3 else "#ff6b6b"
            TAGS["needs"]["set"](fade(t, tnever + 0.1, dur), 1.0 + 0.25 * max(0.0, 1 - abs(t - tval - 0.3) / 0.3))
            TAGS["drop"]["text"] = "DROP 10" if t >= tval + 0.3 else "DROP 20"
            TAGS["drop"]["set"](fade(t, tdrop - 0.2, dur), 1.0)
            note_tags(t, beeps)
        return camf, st, sfx

    # ---------------- challenge + outro
    if sid == "challenge":
        tban, torg, thigh, tfourth = wt("banana"), wt("orange"), wt("high"), wt("fourth")
        tt = thigh - 0.15
        seqR = [(tt, "orange", dur - tt - 0.6)]
        seqL = [(tt, "banana_L", dur - tt - 0.6)]
        keysR = [(0.0, "away", 0.0), (torg - 0.2, "orange", 1.1), (tt - 0.25, "orange", 0.7), (tt, "orange", 0.0),
                 (dur - 0.6, "orange", 0.0), (dur, "orange", 0.8)]
        keysL = [(0.0, "away_L", 0.0), (tban - 0.2, "banana_L", 1.1), (tt - 0.25, "banana_L", 0.7), (tt, "banana_L", 0.0),
                 (dur - 0.6, "banana_L", 0.0), (dur, "banana_L", 0.8)]
        piano = Piano().run([(tt, "hido", None)])
        piano.export(sfx, beeps)
        sfx += [(tt, "tap")]
        ct = V((118, -86, 18))
        camf = cam_path([(0, ct + V((-10, -330, 215)), ct + V((0, 6, 0))), (dur, ct + V((5, -300, 190)), ct)])

        def st(t):
            lv = contacts(seqR + seqL, t)
            base_state(t, piano.screen(t), glow=lv)
            for H, kk in ((HAND, keysR), (HAND_L, keysL)):
                tip, yaw, pitch, lift = hand_at(kk, t)
                vis(H["group"], True)
                place_hand(H, tip, yaw, pitch, lift)
            TAGS["hido"]["set"](fade(t, tt + 0.05, dur), 1.0 + 0.3 * max(0.0, 1 - (t - tt) / 0.3) * (t >= tt))
            TAGS["nonew"]["set"](fade(t, tfourth - 0.2, dur), 1.0)
        return camf, st, sfx

    if sid == "outro":
        camf = orbit(V((80, -48, 0)), 400, 255, -70, -116, dur, lift_target=14.0)

        def st(t):
            base_state(t, show("see you in", "ep 15"))
        return camf, st, sfx

    raise KeyError("no spec for shot " + sid)


# ======================================================================= render
os.makedirs(OUT, exist_ok=True)
sc.render.image_settings.file_format = "PNG"
FSTOP = {"touch_banana": 14.0, "wire_led": 16.0, "touch_pins": 16.0}
DEFAULT_FSTOP = 18.0

if "--top" in argv:  # top-down check of the wire routes
    for f in FRUIT:
        GLOW[f](0.0)
    for H in (HAND, HAND_L):
        vis(H["group"], False)
    REC_RING.hide_render = True
    vis(XG, False)
    set_pulse(None, None)
    cam.data.dof.use_dof = False
    cam.location = V((80, -45, 900)) * MM
    tgt.location = V((80, -44.9, 0)) * MM
    os.makedirs(os.path.join(OUT, "stills"), exist_ok=True)
    sc.render.filepath = os.path.join(OUT, "stills", "_top.png")
    bpy.ops.render.render(write_still=True)
    sys.exit(0)

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
                  "beeps": [{"t": round(b[0], 3), "kind": b[1], "freq": b[2], "note": b[3]}
                            for b in sorted(LAST_BEEPS)]})  # shot-relative
    if STILLS:
        frames = [f for f in FRAMES if f <= n] if FRAMES else sorted({1, n // 2 + 1, n})
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
