"""Episode 15 (DRAFT) - every Blender 3D shot of "My drawer screams when someone opens it", timed to the narration.

    blender -b -P video/ep15/b3d/ep15_3d.py -- [--shots open_scream,scream] [--frames 1,40] [--stills] [--top] [--cycles]

Same pipeline as video/ep14/b3d/ep14_3d.py (which follows ep12_3d.py). Timing: video/ep15/build/schedule.json (EN
narration, word times). A shot = a run of consecutive segments whose vis is "b3d:<id>"; its length = from the first
segment's start to the next segment's start. Output: video/ep15/b3d/build/shots/<id>/f_0001.png ... +
overlay.json/anchors.json per shot + shots.json (start, frames, sfx events, beeps). --stills renders 3 frames per shot
into build/stills/. --top renders a top-down check of the wire routes (build/stills/_top.png).

Behaviour follows lessons/15-drawer-spy/code/drawer_spy/drawer_spy.ino, simulated by Spy below:
  light = readLight() (0 dark .. 4095 bright); !isOpen && light > OPEN_AT 1800 -> isOpen, openings++,
  show("DRAWER OPEN!", "opened Nx"); isOpen && light < CLOSED_AT 1200 -> closed, noTone, show("drawer spy", ...)
  open and < 5 s since it opened -> tone(32, 1500 + (now % 400) * 3): a 0.4 s whoop 1500 -> 2700 Hz, repeated
  hold the button 2 s -> openings = 0, show("counter reset", "opened 0x"); setup() -> show("drawer spy", "opened Nx")
  (the counter lives in Preferences, so it survives a power cut).
Circuit = the Ep 10 layout (ep14_3d.py minus the fruit) + the LDR module on three long jumpers:
  B4e->B r+ 4 (3V3)  B5d->B r- 5 (GND)  OLED B34f..37f, B34j->r- 34, B35j->r+ 35  B17e->B36h green SCL (D22)
  B14e->B37g blue SDA (D21)  button B24/26 e,f; B13d->B24d yellow (D19); B26j->r- 26
  buzzer F30c(+)/F33c; F13i->F30a orange (D32); F5h->F l- 5 (GND); F33a->F l- 33
  + LDR module (parts_ep15.ldr_module, scaled 1.3) lying in the drawer (parts_ep15.drawer, scaled 1.5, right of the
  breadboard): VCC <- red from B r+ 58 (3V3), GND <- black from B r- 59, AO <- purple from F14h (D35); DO empty.
  The jumpers run along the desk behind the drawer and enter it through a slot in the back panel.
"""
import json
import math
import os
import re
import sys

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Euler, Vector

HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1]))
EP = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EP))
sys.path.insert(0, os.path.join(EP, "..", "b3d"))
sys.path.insert(0, HERE)
import parts_ep11 as px  # noqa: E402
import parts_ep15 as p15  # noqa: E402
import pbl  # noqa: E402
from oledfont import Screen  # noqa: E402
from parts_ep12 import _emit_val_mat  # noqa: E402
from pbl import MM, TOP, smooth  # noqa: E402

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


def word_t(shot, word, nth=0, seg=None, exact=False):
    """time of a spoken word, relative to the shot start (first match, or nth match); exact=True: whole word only"""
    want = _norm(word)
    k = 0
    for sid in ([seg] if seg else shot["segs"]):
        s = SEGS[sid]
        for w in s["words"]:
            nw = _norm(w["w"])
            if (nw == want) if exact else nw.startswith(want):
                if k == nth:
                    return s["start"] + w["t"] - shot["start"]
                k += 1
    raise KeyError(f"{shot['id']}: word {word!r} #{nth} not found")


# ======================================================================= the sketch, simulated
OPEN_AT, CLOSED_AT = 1800, 1200


def show(top, big):
    """the sketch's show(): textSize(1) at (0,0), textSize(2) at (0,28)"""
    s = Screen()
    s.text(0, 0, top, 1)
    s.text(0, 28, big, 2)
    return s


def scr_idle(n):
    return show("drawer spy", "opened %dx" % n)


def scr_open(n):
    return show("DRAWER OPEN!", "opened %dx" % n)


class Spy:
    """loop() of drawer_spy.ino stepped at 200 Hz over a light(t) curve. Produces a screen timeline and the tone
    intervals [(t0, t1)] of the 5 s whoop. presses = [(down, up)] of the button, off = [(t0, t1)] power cut windows
    (setup() runs again at t1)."""

    def __init__(self, openings=0, is_open=False, opened_at=-1e9, open_at=OPEN_AT, closed_at=CLOSED_AT, scr0=None):
        self.n, self.is_open, self.opened_at = openings, is_open, opened_at
        self.open_at, self.closed_at = open_at, closed_at
        self.tl = [(-1e9, scr0 or (scr_open(openings) if is_open else scr_idle(openings)))]
        self.tones = []

    def scr(self, t, s):
        self.tl.append((t, s))

    def run(self, light, t0, t1, presses=(), off=()):
        dt = 1.0 / 200
        tone_from = None
        was_off = False
        down = None
        prev_pressed = False
        steps = int((t1 - t0) / dt) + 1
        for i in range(steps):
            t = t0 + i * dt
            if any(a <= t < b for a, b in off):
                if not was_off:
                    self.scr(t, None)
                    was_off = True
                if tone_from is not None:
                    self.tones.append((tone_from, t))
                    tone_from = None
                continue
            if was_off:  # setup()
                was_off = False
                self.is_open = False
                self.scr(t, scr_idle(self.n))
            L = light(t)
            if not self.is_open and L > self.open_at:
                self.is_open = True
                self.opened_at = t
                self.n += 1
                self.scr(t, scr_open(self.n))
            elif self.is_open and L < self.closed_at:
                self.is_open = False
                self.scr(t, scr_idle(self.n))
            tone = self.is_open and t - self.opened_at < 5.0
            if tone and tone_from is None:
                tone_from = t
            elif not tone and tone_from is not None:
                self.tones.append((tone_from, t))
                tone_from = None
            pressed = any(a <= t < b for a, b in presses)
            if pressed and not prev_pressed:
                down = t
            if pressed and down is not None and t - down >= 2.0:
                self.n = 0
                self.scr(t, show("counter reset", "opened 0x"))
                down = None
            if not pressed:
                down = None
            prev_pressed = pressed
        if tone_from is not None:
            self.tones.append((tone_from, t1))
        self.tl.sort(key=lambda x: x[0])
        return self

    def screen(self, t):
        s = self.tl[0][1]
        for tt, sc in self.tl:
            if tt <= t:
                s = sc
        return s

    def export(self, sfx, beeps, dur):
        """the whoop: one 'whoop' event (0.4 s sweep) per cycle; a cycle cut short by the alarm stopping -> 'chirp'"""
        for a, b in self.tones:
            if a >= dur:
                continue
            j = 0
            while a + 0.4 * j < min(b, dur - 0.1):
                tk = a + 0.4 * j
                sfx.append((tk, "whoop" if b - tk >= 0.3 else "chirp"))
                beeps.append((tk, "hi", 1500, "whoop", -1))
                j += 1


# ======================================================================= scene
k = pbl.Kit(fps=FPS, engine="CYCLES" if "--cycles" in argv else "EEVEE")
k.desk()
F, B = k.boards()
esp = k.esp32(hot={"3V3", "GND", "D21", "D22", "D19", "D32", "D35"})
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

# ---- the drawer (scaled 1.5 x 1.5 x 1: a flat 96 x 78 x 34 mm desk drawer, so the camera sees into it), right of the
# breadboard, opening toward the camera
D_AT = V((190, 8, 0))
DS, DSZ = 1.5, 1.0
DRW = p15.drawer(k, D_AT)
DRW["group"].scale = (DS, DS, DSZ)
bpy.data.objects["drawer_knob"].scale = (1, 1, DS / DSZ)  # keep the knob round
# the back panel gets a slot for the three jumpers (local units of the drawer: W 64, D 52, H 34, t 2.2)
bpy.data.objects.remove(bpy.data.objects["drawer_back"], do_unlink=True)
_wd = p15._wood_mat("p15_wood_dark", "#6e4521", "#96653a")
for _nm, _sz, _lc in (("l", (17, 2.2, 34), (-23.5, 24.9, 17)), ("r", (42, 2.2, 34), (11, 24.9, 17)),
                      ("b", (5, 2.2, 24.5), (-12.5, 24.9, 12.25)), ("t", (5, 2.2, 4), (-12.5, 24.9, 32))):
    k.box("drawer_back_" + _nm, _sz, _lc, _wd, DRW["group"])
SLOT_X = D_AT.x - 12.5 * DS  # 171.25
SLOT_Z = 27.25 * DSZ         # 27.25
BACK_Y = D_AT.y + 26 * DS    # 47 (outer face of the back panel)
KNOB0 = D_AT + V((0, -29 * DS, 17 * DSZ))  # knob centre, drawer shut
FRONT_Y = D_AT.y - 26 * DS   # -31, the case opening
FLOOR_Z = (3.2 + 1.6) * DSZ  # 4.8, top of the inner box floor
TOP_Z = 34.0 * DSZ           # top of the drawer case
O_MAX = 50.0                 # fully open (world mm)


def knob(o):
    return KNOB0 + V((0, -o, 0))


# ---- the LDR module (scaled 1.3, it reads too small next to the drawer otherwise), lying across the drawer facing up,
# the header toward the back (the wires go straight back to the slot), the photoresistor on the right
MS = 1.3
MOD_AT = V((186, -4, FLOOR_Z))
MOD_YAW = 180.0
MOD = p15.ldr_module(k, MOD_AT, yaw_deg=MOD_YAW, name="ldr")
MOD["group"].scale = (MS, MS, MS)
PIN_X = {"AO": 2.0, "DO": 4.54, "GND": 7.08, "VCC": 9.62}
_blk = k.mat("dupont", "#15171c", 0.5)
DUP = {}
for _n, _col in (("AO", "purple"), ("GND", "black"), ("VCC", "red")):
    DUP[_n] = k.box("dup_" + _n, (2.5, 2.5, 11.0), (PIN_X[_n], -4.6, 6.4 + 5.5), _blk, MOD["group"], bevel=0.2)
    k.box("dupc_" + _n, (2.6, 2.6, 1.6), (PIN_X[_n], -4.6, 6.4 + 10.0),
          k.mat("wire_" + _col, pbl.COL[_col], 0.38, coat=0.35), MOD["group"])


def _rz(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return V((v.x * c - v.y * s, v.x * s + v.y * c, v.z))


MSTATE = {"o": 0.0, "lift": 0.0}


def mod_pt(local, o=None, lift=None):
    """world point of a module-local point (unscaled module units) for drawer opening o and lift"""
    o = MSTATE["o"] if o is None else o
    lift = MSTATE["lift"] if lift is None else lift
    return MOD_AT + V((0, -o, lift)) + _rz(V(local) * MS, MOD_YAW)


def ldr_pt(o=None):
    return mod_pt((-10.5, 0, 9.0), o)


def set_drawer(o, lift=0.0):
    MSTATE["o"], MSTATE["lift"] = o, lift
    DRW["set_open"](o / DS)
    MOD["group"].location = MOD_AT + V((0, -o, lift))


# ---- showcase module (s05/s06): a loose copy on the desk in front of the board, turning
SHOW_AT = V((70, -122, 0))
SMS = 1.7
SHOW = p15.ldr_module(k, SHOW_AT, yaw_deg=0.0, name="ldrshow")
SHOW["group"].scale = (SMS, SMS, SMS)


def show_pt(local, yaw):
    return SHOW_AT + _rz(V(local) * SMS, yaw)


# ---- the three long jumpers (dense polyline, recomputed when the drawer moves)
def _catmull(pts, n_per=24):
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


NPTS = 300


class LdrWire:
    """breadboard hole -> along the desk -> through the slot in the drawer's back -> onto the module pin"""

    def __init__(self, name, hole, ctrl, pin, sx, color):
        self.name, self.hole, self.ctrl, self.pin, self.sx = name, V(hole), [V(c) for c in ctrl], pin, sx
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
        self.sp = cu.splines.new("POLY")
        self.sp.points.add(NPTS - 1)
        self.cu = cu
        self.ob = bpy.data.objects.new(name, cu)
        cu.materials.append(k.mat("wire_" + color, pbl.COL.get(color, color), 0.38, coat=0.35))
        k._link(self.ob, g)
        tip = k.mat("tip", "#c8ced6", 0.25, metal=1.0)
        self.ta = k.cyl(name + "_tipA", 0.33, 3.6, (self.hole.x, self.hole.y, TOP + 0.6), tip, g, segs=12)
        self.key = None
        self.poly = None
        self.update()

    def points(self):
        pt = mod_pt((PIN_X[self.pin], -4.6, 17.2))  # top of the Dupont housing
        sy = BACK_Y
        inner = [V((self.sx, sy - 7, SLOT_Z - 0.3)), V(((self.sx + pt.x) / 2, (sy - 7 + pt.y + 9) / 2, SLOT_Z - 1.0)),
                 V((pt.x, pt.y + 7, min(pt.z + 5.0, TOP_Z - 3.4))), pt + V((0, 1.0, 2.6)), pt]
        if (sy - 7) - (pt.y + 9) < 8:  # drawer shut: the pin is close to the slot, skip the mid point
            inner = [inner[0]] + inner[2:]
        back = [V((self.sx, sy + 9, 4)), V((self.sx, sy + 5, 17)), V((self.sx, sy + 3, SLOT_Z)),
                V((self.sx, sy - 1.6, SLOT_Z))]
        return [self.hole + V((0, 0, 2.4)), self.hole + V((0, 0, 7.0))] + self.ctrl + back + inner

    def update(self):
        key = (round(MSTATE["o"], 3), round(MSTATE["lift"], 3))
        if key == self.key:
            return
        self.key = key
        poly, L = _resample(_catmull(self.points()), NPTS)
        for p_, q in zip(self.sp.points, poly):
            p_.co = (q.x, q.y, q.z, 1.0)
        self.poly = poly
        self.cu.update_tag() if hasattr(self.cu, "update_tag") else None

    def draw(self, x):
        x = max(0.0, min(1.0, x))
        self.cu.bevel_factor_end = max(0.001, x)
        self.ob.hide_render = x <= 0.0
        self.ta.hide_render = x <= 0.0

    def at(self, u):
        u = max(0.0, min(1.0, u))
        f = u * (len(self.poly) - 1)
        i = min(len(self.poly) - 2, int(f))
        return self.poly[i].lerp(self.poly[i + 1], f - i)


VCC_H, GND_H, AO_H = B.rail(58, "r", "+"), B.rail(59, "r", "-"), F.hole(14, "h")
LW = {}
LW["vcc"] = LdrWire("ldr_vcc", VCC_H, [(106, 55.5, 12.5), (112, 61, 6.5), (119, 63, 0.65), (150, 63, 0.65),
                                       (164, 62.5, 0.65)], "VCC", SLOT_X - 2.3, "red")
LW["gnd"] = LdrWire("ldr_gnd", GND_H, [(109, 57.5, 12.5), (115, 63.5, 6.0), (121, 66, 0.65), (152, 66, 0.65),
                                       (167, 65.5, 0.65)], "GND", SLOT_X, "black")
LW["ao"] = LdrWire("ldr_ao", AO_H, [(-6, -19.8, 21), (8, -22.2, 19), (30, -22.6, 13.2), (70, -22.6, 11.6),
                                    (108, -22.6, 11.6), (119, -23.5, 6.0), (126, -23.5, 0.65), (133, -12, 0.65),
                                    (133.5, 48, 0.65), (140, 59.5, 0.65), (162, 60.5, 0.65)], "AO", SLOT_X + 2.3,
                   "purple")
DUP_PIN = {"vcc": "VCC", "gnd": "GND", "ao": "AO"}

# ---- light flooding into the open drawer: a warm spot on the part that comes out (a visible light cone was tried in
# the stills and covered the drawer, 2026-11-25)
_sd = bpy.data.lights.new("flood_spot", "SPOT")
_sd.color = pbl.lin("#ffe7b8")
_sd.spot_size = math.radians(42)
_sd.spot_blend = 0.6
FSPOT = bpy.data.objects.new("flood_spot", _sd)
k.scene.collection.objects.link(FSPOT)
FSPOT.location = V((D_AT.x + 10, FRONT_Y - 50, 230)) * MM
FSPOT.rotation_euler = ((V((D_AT.x, FRONT_Y - 22, 5)) - V((D_AT.x + 10, FRONT_Y - 50, 230))) * MM).to_track_quat("-Z", "Y").to_euler()


def set_flood(level):
    _sd.energy = 3.0 * level


# ---- trouble: a crack in the drawer's top with sunlight coming through, and the tape that fixes it
GAP_C = V((198, -6, TOP_Z))
GAP_M, GAP_V = _emit_val_mat("gap_m", "#fff3c8", 9.0)
GAP = k.box("gap_slit", (26, 1.3, 0.25), GAP_C + V((0, 0, 0.1)), GAP_M)
k.box("gap_dark", (27, 1.7, 0.2), GAP_C + V((0, 0, 0.02)), k.mat("gapdark", "#120b06", 0.9))
BEAM_M, BEAM_V = _emit_val_mat("beam_m", "#fff1c2", 1.6)
BEAM = k.mesh("beam", k.bm_cyl(4, 120, 32, r2=22), BEAM_M, GAP_C + V((0, 0, 60)))
TAPE = k.box("tape", (36, 11, 0.5), GAP_C + V((0, 0, 0.3)), k.mat("tape", "#e6d7a6", 0.75, coat=0.2), bevel=0.15)


def set_gap(on, sun=0.0, tape=0.0):
    for o in (GAP, BEAM, TAPE, bpy.data.objects["gap_dark"]):
        o.hide_render = not on
    GAP_V.outputs[0].default_value = sun
    BEAM_V.outputs[0].default_value = 0.16 * sun
    BEAM.hide_render = not on or sun <= 0.01
    TAPE.hide_render = not on or tape <= 0.01
    s = max(0.01, tape)
    TAPE.scale = (s, 1, 1)
    TAPE.location = GAP_C + V((-18 * (1 - s), 0, 0.3))


# ---- laptop with the Serial Monitor (s21), left behind the board where the USB cable goes
LAP_AT = V((-150, 112, 0))
LAP_YAW = 22.0
LAP_TILT = 14.0
LAP = k.empty("laptop", LAP_AT)
LAP.rotation_euler = (0, 0, math.radians(LAP_YAW))
_alu = k.mat("lap_alu", "#4a515c", 0.35, metal=0.7)
k.box("lap_base", (150, 100, 7), (0, 0, 3.5), _alu, LAP, bevel=1.5)
k.box("lap_keys", (128, 44, 0.4), (0, 6, 7.1), k.mat("lap_keys", "#1c2027", 0.6), LAP)
k.box("lap_pad", (46, 26, 0.3), (0, -32, 7.05), k.mat("lap_pad", "#3d434d", 0.4, metal=0.5), LAP)
LID = k.empty("lap_lid", (0, 47, 7), LAP)
LID.rotation_euler = (math.radians(-LAP_TILT), 0, 0)
k.box("lap_lidbox", (150, 5, 98), (0, 2.5, 49), _alu, LID, bevel=1.5)
k.box("lap_screen", (142, 0.4, 88), (0, -0.2, 50), k.mat("lap_scr", "#0b0f14", 0.3, emit="#0b0f14", strength=1.0), LID)
k.box("lap_title", (142, 0.5, 8), (0, -0.35, 90), k.mat("lap_bar", "#263040", 0.4, emit="#263040", strength=1.0), LID)
CONSOLA = bpy.data.fonts.load("C:/Windows/Fonts/consola.ttf") if os.path.exists("C:/Windows/Fonts/consola.ttf") else None
_tm = k.mat("lap_text", "#d8f5e0", 0.5, emit="#d8f5e0", strength=2.2)
_tt = k.mat("lap_ttext", "#9fb3c8", 0.5, emit="#9fb3c8", strength=1.6)


def _ltext(name, body, size, x, z, mat):
    ob = k.text(name, body, size, (x, -0.7, z), mat, LID, align="LEFT")
    if CONSOLA:
        ob.data.font = CONSOLA
    ob.rotation_euler = (math.pi / 2, 0, 0)
    return ob


_ltext("lap_ttl", "Serial Monitor   COM3   115200 baud", 4.4, -68, 90, _tt)
NLINES = 8
LINES = [_ltext("lap_l%d" % i, "", 4.6, -68, 80 - i * 9.0, _tm) for i in range(NLINES)]


def lid_pt(x, z, out=0.0):
    """world point on the laptop screen (lid-local x, z), pushed `out` mm toward the viewer"""
    p = V((x, -0.7 - out, z))
    p = Euler((math.radians(-LAP_TILT), 0, 0)).to_matrix() @ p + V((0, 47, 7))
    return LAP_AT + _rz(p, LAP_YAW)


def serial(lines):
    shown = lines[-NLINES:]
    for i, ob in enumerate(LINES):
        ob.data.body = shown[i] if i < len(shown) else ""


# ---- hands: a gripping right hand for the drawer knob, a pointing left hand for the button (from behind the
# board), a pointing right hand that shades the showcase sensor
def _hand_common(g, m, name):
    bm = k.bm_box(32, 28, 11)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=3.5, segments=2, affect="EDGES")
    palm = px._flat(k, name + "_palm", bm, m, (16, 0, 0.5), g)
    sub = palm.modifiers.new("subsurf", "SUBSURF")
    sub.levels = sub.render_levels = 2
    px._flat(k, name + "_wrist", px._sphere(11.5, 20, 12), m, (0, 0, 0.5), g, scale=(1, 1.15, 0.78))
    arm = k.bm_cyl(11.0, 170, 24, r2=12.5)
    px._flat(k, name + "_arm", arm, m, (-85, 0, 0.5), g, rot=(0, -math.pi / 2, 0), scale=(1, 1.15, 0.85))


def _smooth_all(g):
    for o in g.children_recursive:
        if o.type == "MESH" and hasattr(o.data, "shade_smooth"):
            o.data.shade_smooth()


def pointing_hand(scale=0.78, name="hand", mirror=False):
    g = k.empty(name)
    g.scale = (scale, -scale if mirror else scale, scale)
    m = px.heat_mat(k, name + "_heat", "#e2a283", "#ffd166")
    _hand_common(g, m, name)
    ip, il, ir = 0.22, 28.0, 4.0
    kn = V((32, 9.6, 0.8))
    px._capsule(k, name + "_index", ir, il, kn, 0.0, ip, m, g, segs=16)
    for i, (y, r) in enumerate(((3.2, 4.2), (-3.6, 4.1), (-10.0, 3.7))):
        b0 = V((31, y, -0.5))
        px._capsule(k, f"{name}_c{i}a", r, 6.5, b0, 0.0, 1.5, m, g, segs=14)
        b1 = b0 + V((math.cos(1.5) * 6.5, 0, -math.sin(1.5) * 6.5))
        px._capsule(k, f"{name}_c{i}b", r * 0.95, 7.0, b1, math.pi, 0.25, m, g, segs=14)
    px._capsule(k, name + "_thumb", 4.4, 15, (13, 12.5, -3.0), 0.3, 0.75, m, g, segs=14)
    _smooth_all(g)
    d = V((math.cos(ip), 0, -math.sin(ip)))
    return {"group": g, "tipc": kn + d * il, "r": ir * scale, "scale": scale, "mirror": mirror, "dloc": d}


def grip_hand(scale=0.78, name="grip"):
    """all four fingers hooked down over a knob (the knob sits under the palm front, GRIP point), thumb under it"""
    g = k.empty(name)
    g.scale = (scale,) * 3
    m = px.heat_mat(k, name + "_heat", "#e2a283", "#ffd166")
    _hand_common(g, m, name)
    for i, (y, r) in enumerate(((9.6, 4.0), (3.2, 4.2), (-3.6, 4.1), (-10.0, 3.7))):
        b0 = V((31, y, -0.5))
        px._capsule(k, f"{name}_c{i}a", r, 9.5, b0, 0.0, 1.25, m, g, segs=14)
        b1 = b0 + V((math.cos(1.25) * 9.5, 0, -math.sin(1.25) * 9.5))
        px._capsule(k, f"{name}_c{i}b", r * 0.95, 8.0, b1, math.pi, 0.75, m, g, segs=14)
    px._capsule(k, name + "_thumb", 4.4, 17, (12, 13.5, -4.0), -0.25, 0.85, m, g, segs=14)
    _smooth_all(g)
    return {"group": g, "grip": V((22.5, 0, -14.5)), "scale": scale}


HAND = pointing_hand(0.78, "hand")
HAND_L = pointing_hand(0.78, "handL", mirror=True)
GRIP = grip_hand(0.78, "grip")


def place_hand(H, tip, yaw, pitch, lift=0.0):
    R = Euler((0.0, pitch, yaw), "XYZ").to_matrix()
    s = H["scale"]
    S = V((s, -s if H["mirror"] else s, s))
    tl = H["tipc"]
    fdir = R @ V((H["dloc"].x, H["dloc"].y * (-1 if H["mirror"] else 1), H["dloc"].z))
    tip = V(tip) + lift * (-fdir * 16.0 + V((0, 0, 12.0)))
    loc = tip - R @ V((tl.x * S.x, tl.y * S.y, tl.z * S.z))
    H["group"].location = loc
    H["group"].rotation_euler = (0.0, pitch, yaw)


GRIP_YAW, GRIP_PITCH = math.radians(118), 0.30


def place_grip(at, lift=0.0):
    """grip point on `at`; lift 0..3 pulls the hand back toward the camera / right and up"""
    R = Euler((0.0, GRIP_PITCH, GRIP_YAW), "XYZ").to_matrix()
    p = V(at) + lift * V((14, -30, 22))
    GRIP["group"].location = p - R @ (GRIP["grip"] * GRIP["scale"])
    GRIP["group"].rotation_euler = (0.0, GRIP_PITCH, GRIP_YAW)


TG = {"button": {"tip": V((btn["top"].x, btn["top"].y, TOP + 3.8 + 4.5 + HAND["r"] * 0.85)), "yaw": math.radians(-75),
                 "pitch": 0.8},
      "away_btn": {"tip": V((5, 95, 85)), "yaw": math.radians(-75), "pitch": 0.8}}

# ---- 'hold 2 s' ring around the button
_rc = bpy.data.curves.new("holdring", "CURVE")
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
    _a = math.pi / 2 - 2 * math.pi * _i / _N
    _p.co = (10.0 * math.cos(_a), 10.0 * math.sin(_a), 0, 1)
HOLD_RING = bpy.data.objects.new("holdring", _rc)
_rc.materials.append(k._emit_mat("holdring_m", "#ff4d5e", 6.0))
k._link(HOLD_RING)
HOLD_RING.location = btn["top"] + V((0, 0, -3.6))

k.lights(center=(0.10, -0.02, 0.0), key=2.2)
RIM = bpy.data.lights["rim"]  # teal back light: turned down when the camera looks at the drawer's back (green wood)
RIM_E = RIM.energy
k.glare(threshold=2.5)
sc = k.scene

TAGS = {}


def tag(name, text, at, color="#ffb547", lift=9.0):
    TAGS[name] = k.tag(text, at, color, lift)
    TAGS[name]["text0"] = text
    TAGS[name]["color0"] = color
    TAGS[name]["lift"] = lift
    return TAGS[name]


def move_tag(name, at):
    tg = TAGS[name]
    tg["at"] = V(at)
    tg["top"] = V(at) + V((0, 0, tg["lift"]))
    tg["group"].location = V(at)


OC = oled["center"]
BT = btn["top"]
BZ = bz["top"]
ESPC = V((-17, 0, 14))
DTOP = D_AT + V((-30, -24, TOP_Z + 0.5))  # front-left corner of the drawer's top

tag("light", "light 0", ldr_pt(0), "#ffd166", lift=26)
tag("sensor", "light sensor", ldr_pt(0), "#ffd166", lift=34)
tag("new", "new", ldr_pt(0), "#2fbf71", lift=34)
tag("ep10", "episode 10", OC + V((0, 4, 0)), "#2dd4bf", lift=16)
tag("stay_oled", "stays", OC + V((0, 4, 0)), "#2dd4bf", lift=12)
tag("stay_btn", "stays", BT, "#f2c037", lift=10)
tag("stay_bz", "stays", BZ, "#ff8a2a", lift=10)
tag("s_ao", "AO", show_pt((PIN_X["AO"], -4.6, 9), 0), "#c4a5ff", lift=10)
tag("s_do", "DO", show_pt((PIN_X["DO"], -4.6, 9), 0), "#9aa5b5", lift=17)
tag("s_gnd", "GND", show_pt((PIN_X["GND"], -4.6, 9), 0), "#e9edf2", lift=10)
tag("s_vcc", "VCC (power)", show_pt((PIN_X["VCC"], -4.6, 9), 0), "#ff6b6b", lift=17)
tag("s_light", "light 0", show_pt((-10.5, 0, 9), 0), "#ffd166", lift=16)
tag("s_range", "0 ... 4095", show_pt((-10.5, 0, 9), 0), "#2dd4bf", lift=30)
tag("b_3v3", "3V3", VCC_H, "#ff6b6b", lift=14)
tag("b_gnd", "GND", GND_H, "#e9edf2", lift=22)
tag("b_35", "pin 35", AO_H, "#c4a5ff", lift=14)
tag("m_vcc", "VCC", mod_pt((PIN_X["VCC"], -4.6, 17), O_MAX), "#ff6b6b", lift=12)
tag("m_gnd", "GND", mod_pt((PIN_X["GND"], -4.6, 17), O_MAX), "#e9edf2", lift=21)
tag("m_ao", "AO", mod_pt((PIN_X["AO"], -4.6, 17), O_MAX), "#c4a5ff", lift=30)
tag("m_do", "DO: empty", mod_pt((PIN_X["DO"], -4.6, 12), O_MAX), "#9aa5b5", lift=44)
tag("faceup", "facing up", ldr_pt(O_MAX), "#ffd166", lift=22)
tag("outback", "wires out the back", V((SLOT_X, BACK_Y + 1, SLOT_Z)), "#c4a5ff", lift=26)
tag("line1", "one line: 1500", DTOP, "#ff6b8b", lift=16)
tag("whoop", "whoop 5 s", BZ, "#ffd166", lift=12)
tag("kept", "still 3!", OC + V((0, 4, 0)), "#2fbf71", lift=16)
tag("hold", "hold 2 s", BT, "#ff6b8b", lift=12)
tag("shut", "drawer shut: ~240", lid_pt(62, 30), "#2dd4bf", lift=5)
tag("open", "drawer open: ~2650", lid_pt(62, 30), "#ff6b6b", lift=5)
tag("lines", "put the two lines in between", lid_pt(30, 94), "#ffd166", lift=14)
tag("gap", "light gets in!", GAP_C, "#ff6b6b", lift=22)
tag("raise", "or: OPEN_AT higher", DTOP, "#ffd166", lift=16)
tag("turn", "your turn", OC + V((0, 4, 0)), "#2fbf71", lift=16)
tag("hint", "hint: parking ticket", knob(0), "#ffd166", lift=34)

# ======================================================================= helpers
PARTS = {"oled": oled["group"], "button": btn["group"], "buzzer": bz["group"]}
press_obj = btn["press"]
PRESS_Z = press_obj.location.z
ALL_W = {n: 1.0 for n in W}
ALL_LW = {n: 1.0 for n in LW}
STATE = {"anchor": BZ}


def vis(group, on):
    for o in [group] + list(group.children_recursive):
        o.hide_render = not on


def set_pwr(on):
    k.pwr_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0 if on else 0.0


def set_usb(pull):
    usb.location.x = -16.0 * pull


def set_rings(t, beeps, center=None):
    for idx, (ob, val) in enumerate(rings):
        ob.location = center if center is not None else BZ
        a, s = 0.0, 1.0
        for b in beeps:
            u = (t - b[0] - idx * 0.07) / 0.45
            if 0 <= u <= 1:
                a = max(a, (1 - u) ** 1.5)
                s = 6.5 + 14 * u
        ob.scale = (s, s, 1)
        val.outputs[0].default_value = a


def fade(t, t0, t1, ramp=0.25):
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


def pop(t, t0):
    return 1.0 + 0.3 * max(0.0, 1 - (t - t0) / 0.3) * (t >= t0)


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


def ease_keys(keys):
    """[(t, value)] -> f(t), smoothstep between keys"""
    def f(t):
        if t <= keys[0][0]:
            return keys[0][1]
        for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
            if t <= t1:
                return v0 + (v1 - v0) * smooth((t - t0) / max(1e-6, t1 - t0))
        return keys[-1][1]
    return f


def grip_windows(keys, pre=0.08, post=0.08):
    """contact windows of the hand: every key pair where the drawer moves"""
    out = []
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if abs(v1 - v0) > 0.01:
            a, b = t0 - pre, t1 + post
            if out and a <= out[-1][1] + 0.35:
                out[-1] = (out[-1][0], b)
            else:
                out.append((a, b))
    return out


def grip_lift(t, wins, app=0.45):
    """0 on the knob, rising to 3 (out of the picture) away from the contact windows; None = hidden"""
    if not wins:
        return None
    d = min(0.0 if a <= t <= b else min(abs(t - a), abs(t - b)) for a, b in wins)
    if d >= app * 1.9:
        return None
    return 3.0 * smooth(d / (app * 1.9)) ** 0.8


def light_of(o):
    """the sketch's light number (0 = dark) for a drawer opened o mm: dark inside, the light floods in"""
    return 140 + 3060 * smooth(o / 40.0)


def jitter(t, amp=6.0):
    return amp * (math.sin(t * 23.1) * 0.6 + math.sin(t * 37.7 + 1.3) * 0.4)


def q10(t):
    return math.floor(t * 10) / 10.0  # the light number tag updates 10x a second, so it can be read


# ---- camera presets (mm)
WIDE_T = V((112, -14, 12))
WIDE_P = WIDE_T + V((-24, -470, 380))
DRAWER_T = V((188, -46, 10))
DRAWER_P = DRAWER_T + V((-60, -205, 235))
BOARD_T = V((28, -8, 8))
BOARD_P = BOARD_T + V((-6, -228, 205))
SPLIT_T = V((118, -18, 12))           # OLED (left) + drawer (right)
SPLIT_P = SPLIT_T + V((-20, -400, 350))


# ======================================================================= shots
def shot_spec(sh):
    """returns (camera f(t), state f(t) -> None, sfx list [(t, kind)])"""
    sid, dur = sh["id"], sh["end"] - sh["start"]
    wt = lambda w, n=0, exact=False: word_t(sh, w, n, exact=exact)  # noqa: E731
    sfx = []
    beeps = []
    global LAST_BEEPS
    LAST_BEEPS = beeps

    def base_state(t, scr, o=0.0, lift=0.0, wires=ALL_W, lwires=ALL_LW, pwr=True, pull=0.0, flood=None, rim=1.0):
        for n, g in PARTS.items():
            vis(g, True)
        for n, w in W.items():
            w["draw"](wires.get(n, 0.0))
        set_drawer(o, lift)
        for n, w in LW.items():
            w.update()
            w.draw(lwires.get(n, 0.0))
            DUP[DUP_PIN[n]].hide_render = lwires.get(n, 0.0) < 0.98
            bpy.data.objects["dupc_" + DUP_PIN[n]].hide_render = lwires.get(n, 0.0) < 0.98
        press_obj.location.z = PRESS_Z
        set_pwr(pwr)
        set_usb(pull)
        k.set_screen(scr)
        STATE["anchor"] = BZ
        set_rings(t, beeps)
        for tg in TAGS.values():
            tg["set"](0.0)
            tg["text"] = tg["text0"]
            tg["color"] = tg["color0"]
        for H in (HAND, HAND_L, GRIP):
            vis(H["group"], False)
        vis(SHOW["group"], False)
        vis(LAP, False)
        set_gap(False)
        HOLD_RING.hide_render = True
        set_flood(smooth(o / O_MAX) if flood is None else flood)
        RIM.energy = RIM_E * rim
        move_tag("light", ldr_pt(o))

    def drawer_hand(t, keys, of):
        lift = grip_lift(t, grip_windows(keys))
        if lift is None:
            return
        vis(GRIP["group"], True)
        place_grip(knob(of(t)), lift)

    def light_tag(t, L, on=1.0):
        v = int(round(L(q10(t))))
        TAGS["light"]["text"] = "light %d" % v
        TAGS["light"]["color"] = "#ff6b6b" if v > OPEN_AT else ("#2dd4bf" if v < CLOSED_AT else "#ffd166")
        TAGS["light"]["set"](on, 1.0)

    def drawer_light(of, extra=None):
        return lambda t: light_of(of(t)) + jitter(t) + (extra(t) if extra else 0.0)

    # ---------------- cold open
    if sid == "open_scream":
        topen = wt("opens") - 0.25
        keys = [(0.0, 0.0), (topen, 0.0), (topen + 0.75, O_MAX)]
        of = ease_keys(keys)
        L = drawer_light(of)
        spy = Spy(openings=2).run(L, 0.0, dur)
        spy.export(sfx, beeps, dur)
        sfx.append((topen, "drawer"))
        camf = cam_path([(0, SPLIT_P + V((40, 30, -20)), SPLIT_T + V((22, -8, 0))),
                         (dur, SPLIT_P + V((60, 75, -55)), SPLIT_T + V((28, -12, 0)))])

        def st(t):
            base_state(t, spy.screen(t), o=of(t))
            drawer_hand(t, keys, of)
            light_tag(t, L, fade(t, topen + 0.3, dur + 1))
        return camf, st, sfx

    if sid == "open_count":
        camf = cam_path([(0, OC + V((14, -95, 88)), OC + V((2, 0, 0))), (dur, OC + V((6, -72, 66)), OC)])

        def st(t):
            base_state(t, scr_idle(3))
        return camf, st, sfx

    if sid == "open_orbit":
        tlight = wt("light")
        camf = orbit(V((112, -14, 0)), 450, 320, -114, -70, dur, lift_target=12.0)

        def st(t):
            base_state(t, scr_open(3), o=O_MAX)
            TAGS["sensor"]["set"](fade(t, tlight - 0.2, dur + 1), pop(t, tlight - 0.2))
            move_tag("sensor", ldr_pt(O_MAX))
        return camf, st, sfx

    if sid == "open_title":
        tspy, tep = wt("spy"), wt("episode")
        camf = cam_path([(0, WIDE_P + V((30, 20, 10)), WIDE_T + V((5, 0, 0))), (dur, WIDE_P + V((0, 55, -30)), WIDE_T)])

        def st(t):
            base_state(t, scr_open(3), o=O_MAX)
            move_tag("new", ldr_pt(O_MAX))
            TAGS["new"]["set"](fade(t, tspy - 0.2, dur + 1), pop(t, tspy - 0.2))
            TAGS["ep10"]["set"](fade(t, tep - 0.1, dur + 1), pop(t, tep - 0.1))
        return camf, st, sfx

    # ---------------- the sensor
    if sid == "ldr_module":
        tfour = wt("Four")
        tw = {"s_ao": wt("A", exact=True), "s_do": wt("D", exact=True), "s_gnd": wt("ground"), "s_vcc": wt("power")}
        yawf = ease_keys([(0.0, -150.0), (tfour - 0.2, -8.0)])
        c = SHOW_AT + V((0, 0, 8))
        camf = cam_path([(0, c + V((20, -150, 110)), c + V((0, 2, 0))), (tfour, c + V((8, -118, 92)), c + V((2, 0, 0))),
                         (dur, c + V((4, -104, 80)), c + V((-1, 0, 0)))])

        def st(t):
            base_state(t, scr_idle(3))
            yaw = yawf(t)
            vis(SHOW["group"], True)
            SHOW["group"].rotation_euler = (0, 0, math.radians(yaw))
            for nm, pin in (("s_ao", "AO"), ("s_do", "DO"), ("s_gnd", "GND"), ("s_vcc", "VCC")):
                move_tag(nm, show_pt((PIN_X[pin], -4.6, 11.5), yaw))
                TAGS[nm]["set"](fade(t, tw[nm] - 0.15, dur + 1), pop(t, tw[nm] - 0.15))
        return camf, st, sfx

    if sid == "ldr_macro":
        tch, tnum, tzero, tfour = wt("changes"), wt("number"), wt("zero"), wt("four")
        lc = show_pt((-10.5, 0, 9), -8)
        # the hand shades the sensor (dark = low number), leaves, shades it fully on "zero", leaves on "four"
        hk = ease_keys([(0.0, 0.0), (tch - 0.1, 0.0), (tch + 0.6, 1.0), (tch + 1.5, 1.0), (tch + 2.1, 0.0),
                        (tzero - 0.6, 0.0), (tzero - 0.05, 1.25), (tfour - 0.25, 1.25), (tfour + 0.3, 0.0)])

        def L(t):
            h = hk(t)
            return max(0.0, min(4095.0, 3350 - 2700 * min(1.0, h) - 650 * max(0.0, h - 1.0) * 4 + jitter(t, 12)
                                + 745 * smooth((t - tfour - 0.1) / 0.5)))
        camf = cam_path([(0, lc + V((10, -112, 84)), lc + V((6, 0, 2))), (dur, lc + V((4, -92, 70)), lc + V((4, 0, 2)))])

        def st(t):
            base_state(t, scr_idle(3))
            vis(SHOW["group"], True)
            SHOW["group"].rotation_euler = (0, 0, math.radians(-8))
            h = hk(t)
            if h > 0.01:
                vis(HAND["group"], True)
                hh = min(1.0, h)
                tip = lc + V((-20 + 110 * (1 - hh) ** 1.5, -4, 27 - 40 * max(0.0, h - 1.0)))
                place_hand(HAND, tip, math.radians(170), 0.2)
            v = int(round(min(4095, max(0, L(q10(t))))))
            TAGS["s_light"]["text"] = "light %d" % v
            TAGS["s_light"]["set"](fade(t, tch - 0.3, dur + 1), 1.0)
            TAGS["s_range"]["set"](fade(t, tzero - 0.3, dur + 1), pop(t, tzero - 0.3))
        return camf, st, sfx

    # ---------------- wiring
    if sid == "wire_keep":
        tscr, tbtn, tbz = wt("screen"), wt("button"), wt("buzzer")
        camf = cam_path([(0, BOARD_P + V((10, -10, 10)), BOARD_T + V((5, 0, 0))), (dur, BOARD_P + V((10, 15, -10)), BOARD_T)])

        def st(t):
            base_state(t, scr_idle(0), o=O_MAX, lwires={})
            TAGS["stay_oled"]["set"](fade(t, tscr - 0.1, dur + 1), 1.0)
            TAGS["stay_btn"]["set"](fade(t, tbtn - 0.1, dur + 1), 1.0)
            TAGS["stay_bz"]["set"](fade(t, tbz - 0.1, dur + 1), 1.0)
        return camf, st, sfx

    if sid == "wire_ldr":
        tpw, tvolt, tg0, tg1 = wt("Power"), wt("volts"), wt("ground"), wt("ground", 1)
        tao, t35, tdo, tempty = wt("A", exact=True), wt("thirtyfive"), wt("D", exact=True), wt("empty")
        grow = {"vcc": (tpw - 0.1, tvolt + 0.5), "gnd": (tg0 - 0.1, tg1 + 0.6), "ao": (tao - 0.1, t35 + 1.0)}
        for w, (a, b) in grow.items():
            sfx.append((b, "snap"))
        mid = V((150, 5, 14))
        camf = cam_path([(0, mid + V((-40, -300, 300)), mid + V((0, 10, 0))),
                         (tg1 + 0.4, mid + V((-30, -290, 290)), mid + V((-4, 6, 0))),
                         (tao + 0.2, WIDE_P + V((-10, 20, -20)), WIDE_T + V((-14, -4, 0))),
                         (t35 + 1.0, WIDE_P + V((-10, 30, -30)), WIDE_T + V((-6, -6, 0))),
                         (tdo + 0.1, DRAWER_P + V((0, 20, 10)), DRAWER_T + V((4, 8, 0))),
                         (dur, DRAWER_P + V((10, 40, -5)), DRAWER_T + V((6, 8, 0)))])

        def st(t):
            lw = {w: smooth((t - a) / (b - a)) for w, (a, b) in grow.items()}
            base_state(t, scr_idle(0), o=O_MAX, lwires=lw)
            TAGS["b_3v3"]["set"](fade(t, tpw, tao), 1.0)
            TAGS["b_gnd"]["set"](fade(t, tg0, tao), 1.0)
            TAGS["b_35"]["set"](fade(t, tao, tdo - 0.2), 1.0)
            TAGS["m_vcc"]["set"](fade(t, grow["vcc"][1] - 0.15, dur + 1), 1.0)
            TAGS["m_gnd"]["set"](fade(t, grow["gnd"][1] - 0.15, dur + 1), 1.0)
            TAGS["m_ao"]["set"](fade(t, grow["ao"][1] - 0.15, dur + 1), 1.0)
            TAGS["m_do"]["set"](fade(t, tdo - 0.1, dur + 1), pop(t, tempty - 0.1))
        return camf, st, sfx

    if sid == "wire_drawer":
        tin, tface, twire, tback = wt("inside"), wt("facing"), wt("wires"), wt("back")
        liftf = ease_keys([(0.0, 12.0), (tin - 0.4, 12.0), (tin + 0.6, 0.0)])
        keys = [(0.0, O_MAX), (tface + 0.4, O_MAX), (tface + 1.4, 0.0)]
        of = ease_keys(keys)
        sfx.append((tin + 0.6, "tap"))
        sfx.append((tface + 0.4, "drawer"))
        camf = cam_path([(0, DRAWER_P + V((10, 30, 20)), DRAWER_T + V((4, 10, 6))),
                         (tface + 1.3, DRAWER_P + V((0, 40, 10)), DRAWER_T + V((2, 14, 0))),
                         (tback - 0.2, V((280, 215, 245)), V((168, 32, 14))),
                         (dur, V((268, 228, 232)), V((166, 36, 14)))])

        def st(t):
            o = of(t)
            base_state(t, scr_idle(0), o=o, lift=liftf(t), rim=1.0 - smooth((t - tface - 1.3) / 1.2))
            drawer_hand(t, keys, of)
            move_tag("faceup", ldr_pt(o))
            TAGS["faceup"]["set"](fade(t, tface - 0.15, tface + 0.9), pop(t, tface - 0.15))
            TAGS["outback"]["set"](fade(t, tback - 0.6, dur + 1), pop(t, tback - 0.6))
        return camf, st, sfx

    # ---------------- the flicker (first idea: one line at 1500)
    if sid == "flicker":
        topen, tcrack, twob = wt("open") - 0.1, wt("crack"), wt("wobbles")
        ons = [(twob + 0.05, twob + 0.42), (twob + 0.85, twob + 1.2), (wt("on", 1, True) - 0.04, wt("off", 0, True) - 0.04),
               (wt("on", 2, True) - 0.04, wt("off", 1, True) - 0.04)]
        o_crack = 18.5
        keys = [(0.0, 0.0), (topen, 0.0), (tcrack + 0.3, o_crack)]
        of = ease_keys(keys)

        def L(t):
            base = light_of(of(t))
            if t < twob - 0.4:
                return min(base, 1430) + jitter(t, 10)
            sgn = -1.0
            for a, b in ons:
                sgn = max(sgn, -1.0 + 2.0 * smooth((t - a + 0.03) / 0.06) * (1 - smooth((t - b + 0.03) / 0.06)))
            return 1500 + sgn * (55 + 45 * abs(math.sin(t * 8.3))) + jitter(t, 8)
        spy = Spy(openings=0, open_at=1500, closed_at=1500).run(L, 0.0, dur)
        spy.export(sfx, beeps, dur)
        sfx.append((topen, "drawer"))
        camf = cam_path([(0, SPLIT_P + V((30, 40, -25)), SPLIT_T + V((10, -10, 0))),
                         (dur, SPLIT_P + V((40, 80, -55)), SPLIT_T + V((14, -12, 0)))])

        def st(t):
            base_state(t, spy.screen(t), o=of(t))
            drawer_hand(t, keys, of)
            v = int(round(L(q10(t))))
            light_tag(t, L, fade(t, topen + 0.4, dur + 1))
            TAGS["light"]["color"] = "#ff6b6b" if v > 1500 else "#2dd4bf"
            TAGS["line1"]["set"](fade(t, twob - 0.3, dur + 1), 1.0)
        return camf, st, sfx

    if sid == "scream":
        topen = wt("opens") - 0.3
        keys = [(0.0, 0.0), (topen, 0.0), (topen + 0.6, O_MAX)]
        of = ease_keys(keys)
        L = drawer_light(of)
        spy = Spy(openings=2).run(L, 0.0, dur)
        spy.export(sfx, beeps, dur)
        sfx.append((topen, "drawer"))
        t_al = spy.tones[0][0] if spy.tones else topen + 0.4
        bz_d = (BZ + knob(O_MAX)) / 2
        camf = cam_path([(0, bz_d + V((-30, -390, 330)), bz_d + V((0, 8, 0))), (dur, bz_d + V((-10, -345, 290)), bz_d + V((4, 4, 0)))])

        def st(t):
            base_state(t, spy.screen(t), o=of(t))
            drawer_hand(t, keys, of)
            light_tag(t, L, fade(t, topen + 0.3, dur + 1))
            left = 5.0 - (t - t_al)
            if t >= t_al:
                TAGS["whoop"]["text"] = "whoop %d s" % max(1, math.ceil(left)) if left > 0 else "quiet"
                TAGS["whoop"]["color"] = "#ffd166" if left > 0 else "#2dd4bf"
                TAGS["whoop"]["set"](1.0, 1.0)
        return camf, st, sfx

    if sid == "power_cut":
        tpull, tplug, tstill = wt("Pull") + 0.15, wt("plug"), wt("still")
        pullf = ease_keys([(0.0, 0.0), (tpull, 0.0), (tpull + 0.35, 1.0), (tplug, 1.0), (tplug + 0.3, 0.0)])
        spy = Spy(openings=3).run(lambda t: 150.0, 0.0, dur, off=[(tpull + 0.12, tplug + 0.3)])
        sfx += [(tpull + 0.12, "unplug"), (tplug + 0.3, "plug")]
        c = (OC + V((esp["xU"], 0, 14))) / 2 + V((0, -8, 0))
        camf = cam_path([(0, c + V((-24, -190, 165)), c + V((-6, 0, 0))), (tplug + 0.5, c + V((-18, -175, 150)), c + V((-4, 0, 0))),
                         (dur, OC + V((-6, -95, 86)), OC + V((-2, 0, 0)))])

        def st(t):
            on = not (tpull + 0.12 <= t < tplug + 0.3)
            base_state(t, spy.screen(t), pull=pullf(t), pwr=on)
            TAGS["kept"]["set"](fade(t, tstill - 0.1, dur + 1), pop(t, tstill - 0.1))
        return camf, st, sfx

    if sid == "reset_hold":
        thold = wt("hold")
        tdown = thold + 0.05
        tup = tdown + 2.3
        spy = Spy(openings=3).run(lambda t: 150.0, 0.0, dur, presses=[(tdown, tup)])
        sfx += [(tdown, "click"), (tup, "click")]
        keys = [(0.0, "button", 1.0), (tdown - 0.3, "button", 0.7), (tdown, "button", 0.0), (tup, "button", 0.0),
                (tup + 0.3, "button", 0.7), (tup + 1.3, "away_btn", 0.0)]
        camf = cam_path([(0, BT + V((15, -130, 115)), (BT + OC) / 2), (tup, BT + V((20, -100, 95)), (BT + OC) / 2 + V((3, 0, 0))),
                         (dur, OC + V((0, -72, 70)), OC + V((-3, 0, 0)))])

        def hpose(t):
            if t <= keys[0][0]:
                a = b = keys[0]
                u = 0
            else:
                a, b, u = keys[-1], keys[-1], 0
                for x, y in zip(keys, keys[1:]):
                    if t <= y[0]:
                        a, b, u = x, y, smooth((t - x[0]) / max(1e-6, y[0] - x[0]))
                        break
            ga, gb = TG[a[1]], TG[b[1]]
            return ga["tip"].lerp(gb["tip"], u), ga["yaw"], ga["pitch"], a[2] + (b[2] - a[2]) * u

        def st(t):
            base_state(t, spy.screen(t))
            tip, yaw, pitch, lift = hpose(t)
            if tdown <= t < tup:
                press_obj.location.z = PRESS_Z - 1.2
                tip = tip - V((0, 0, 1.2))
            vis(HAND_L["group"], True)
            place_hand(HAND_L, tip, yaw, pitch, lift)
            prog = max(0.0, min(1.0, (t - tdown) / 2.0)) if t < tup else 0.0
            if prog > 0:
                HOLD_RING.hide_render = False
                _rc.bevel_factor_end = max(0.002, prog)
            TAGS["hold"]["set"](fade(t, tdown - 0.1, tup), 1.0)
        return camf, st, sfx

    # ---------------- tuning + troubles
    if sid == "tune_serial":
        tprint, tshut, topen, tlines = wt("prints"), wt("shut"), wt("open"), wt("lines")
        to = topen - 0.2
        keys = [(0.0, 0.0), (to, 0.0), (to + 0.6, O_MAX)]
        of = ease_keys(keys)

        def L(t):
            return 240 + 2410 * smooth(of(t) / 40.0) + jitter(t, 9)
        spy = Spy(openings=0).run(L, 0.0, dur)
        spy.export(sfx, beeps, dur)
        # the full 5 s alarm would sit on the narration: keep only its first 0.8 s (two whoops) in this shot
        _w = [i for i, e in enumerate(sfx) if e[1] == "whoop"][2:]
        for i in reversed(_w):
            del sfx[i]
        _b = [i for i, e in enumerate(beeps) if e[3] == "whoop"][2:]
        for i in reversed(_b):
            del beeps[i]
        sfx.append((to, "drawer"))
        tprints = [-4.0 + 0.5 * i for i in range(int((dur + 4.0) / 0.5) + 1)]  # it has been printing all along
        sc_c = lid_pt(0, 48)
        n_ = (lid_pt(0, 48, 1.0) - sc_c).normalized()
        scr_cam = sc_c + n_ * 245 + V((0, 0, 40))
        dk = knob(O_MAX) + V((0, 10, -4))
        camf = cam_path([(0, scr_cam + V((-6, 0, 8)), sc_c + V((6, 0, 0))), (to - 0.4, scr_cam, sc_c + V((4, 0, -2))),
                         (to + 0.25, dk + V((-80, -260, 250)), dk), (to + 1.15, dk + V((-80, -260, 250)), dk),
                         (to + 1.9, scr_cam + V((0, 0, 0)), sc_c + V((4, 0, -2))),
                         (dur, scr_cam + n_ * -12, sc_c + V((4, 0, -2)))])

        def st(t):
            base_state(t, spy.screen(t), o=of(t))
            drawer_hand(t, keys, of)
            vis(LAP, True)
            serial(["light %d  (open above %d, closed below %d)" % (int(round(L(x))), OPEN_AT, CLOSED_AT)
                    for x in tprints if x <= t])
            move_tag("shut", lid_pt(62, 80 - 9 * min(NLINES - 1, sum(1 for x in tprints if x <= tshut) - 1) + 1.5))
            TAGS["shut"]["set"](fade(t, tshut - 0.2, to - 0.3), 1.0)
            TAGS["open"]["set"](fade(t, to + 1.6, dur + 1), 1.0)
            move_tag("open", lid_pt(62, 80 - 9 * (NLINES - 1) + 1.5))
            TAGS["lines"]["set"](fade(t, tlines - 0.3, dur + 1), 1.0)
            light_tag(t, L, fade(t, to, to + 1.4))
        return camf, st, sfx

    if sid == "trouble_day":
        tscr, tgap, ttape, traise = wt("screams"), wt("gap"), wt("tape"), wt("raise")
        sunf = ease_keys([(0.0, 0.0), (0.25, 0.0), (0.7, 1.0)])
        tapef = ease_keys([(0.0, 0.0), (ttape - 0.15, 0.0), (ttape + 0.6, 1.0)])

        def L(t):
            return 150 + 1990 * sunf(t) * (1 - tapef(t)) ** 2 + jitter(t, 10)
        spy = Spy(openings=3).run(L, 0.0, dur)
        spy.export(sfx, beeps, dur)
        sfx.append((ttape - 0.1, "tape"))
        g = GAP_C
        camf = cam_path([(0, SPLIT_P + V((50, 60, 10)), SPLIT_T + V((26, -6, 6))),
                         (tgap - 0.6, SPLIT_P + V((60, 80, -10)), SPLIT_T + V((32, -4, 6))),
                         (tgap + 0.2, g + V((-50, -190, 205)), g + V((-6, -4, -10))),
                         (traise - 0.4, g + V((-56, -180, 192)), g + V((-8, -4, -10))),
                         (dur, SPLIT_P + V((60, 90, -30)), SPLIT_T + V((30, -4, 6)))])

        def st(t):
            base_state(t, spy.screen(t), o=0.0, flood=0.0)
            set_gap(True, sunf(t) * (1 - tapef(t)), tapef(t))
            light_tag(t, L, fade(t, 0.3, dur + 1))
            TAGS["gap"]["set"](fade(t, tgap - 0.3, ttape + 0.4), pop(t, tgap - 0.3))
            TAGS["raise"]["set"](fade(t, traise - 0.2, dur + 1), 1.0)
        return camf, st, sfx

    # ---------------- challenge + outro
    if sid == "challenge":
        tturn, tlong, tpark = wt("turn"), wt("long"), wt("parking")
        mock = show("opened 3x", "open 12 s")
        camf = cam_path([(0, OC + V((30, -150, 132)), OC + V((20, -6, 0))), (dur, OC + V((22, -120, 108)), OC + V((14, -6, 0)))])

        def st(t):
            base_state(t, mock if t >= tlong - 0.3 else scr_idle(3))
            TAGS["turn"]["set"](fade(t, tturn - 0.1, dur + 1), pop(t, tturn - 0.1))
        return camf, st, sfx

    if sid == "outro":
        camf = orbit(V((112, -14, 0)), 450, 320, -70, -116, dur, lift_target=12.0)

        def st(t):
            base_state(t, show("see you in", "ep 16"))
        return camf, st, sfx

    raise KeyError("no spec for shot " + sid)


# ======================================================================= render
os.makedirs(OUT, exist_ok=True)
sc.render.image_settings.file_format = "PNG"
FSTOP = {"ldr_module": 14.0, "ldr_macro": 12.0, "open_count": 12.0, "challenge": 14.0}
DEFAULT_FSTOP = 18.0

if "--top" in argv:  # top-down check of the wire routes
    for H in (HAND, HAND_L, GRIP):
        vis(H["group"], False)
    HOLD_RING.hide_render = True
    set_flood(0.0)
    set_gap(False)
    vis(LAP, False)
    o_top = float(opt("--open", "45"))
    set_drawer(o_top)
    for w in LW.values():
        w.update()
        w.draw(1.0)
    cam.data.dof.use_dof = False
    cam.location = V((100, -5, 1000)) * MM
    tgt.location = V((100, -4.9, 0)) * MM
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
