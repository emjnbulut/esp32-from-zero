"""The single source of timing for the Turkish treasure-detector Short (pure Python: runs inside Blender and in the
repo venv). Everything is a function of the global time T (seconds) and the narration's word times
(build/schedule.json from voice.py):

  shots           [{id, lines, start, end, F0, n}]  (a shot = consecutive lines with the same "vis"; frames F0 .. F0+n-1)
  state(T)        what the 3D scene shows: parts, wires, knob, LED colour, OLED screen, button, USB, tags, camera
  events()        sound effects [(T, kind, arg)]: buzzer ticks/tones at the sketch's frequencies, clicks, plugs, pops
  ticks()         [(T, kind)] for the 2D sound-wave rings at the buzzer

The device is simulated with the logic of projects/08-treasure-detector-2 (same map() maths, thresholds, tones,
delays), so screen, LED, ticks and sound always agree.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
from oledfont import Screen  # noqa: E402

FPS = 30
P = 2.54
LETTER = {"a": -15.24, "b": -12.7, "c": -10.16, "d": -7.62, "e": -5.08,
          "f": 5.08, "g": 7.62, "h": 10.16, "i": 12.7, "j": 15.24}


def hole(board, n, l):
    return ((32 - 18) * P + (n - 32) * P, (-28.0 if board == "F" else 28.0) + LETTER[l], 9.0)


# part anchors (mm, same maths as pbl.py)
OC = (44.45, 19.88, 13.5)            # OLED screen centre
BT = (17.78, 28.0, 17.0)             # button cap
BZ = (34.29, -38.16, 18.2)           # buzzer top
POT = (60.96, -27.08, 25.0)          # knob top
LED = (13.97, -40.7, 21.0)           # RGB LED dome
USBP = (-50.56, 0.0, 14.0)
CENTER = (22.0, 0.0, 0.0)

SECRET1, SECRET2, SECRET3 = 73, 21, 88   # hiding places: the hunt, after the find, after the replug
FOUND_S = 12.4                           # the find time on the OLED (narration: "on iki saniye")
FANFARE = [(1047, 0.12), (1319, 0.12), (1568, 0.12), (2093, 0.35)]


# ------------------------------------------------------------------ helpers
def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def smoother(x):
    x = max(0.0, min(1.0, x))
    return x * x * x * (x * (x * 6 - 15) + 10)


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def keys(ks, t, ease=smoother):
    """ks [(t, value)] (value number or tuple) -> eased value at t"""
    if t <= ks[0][0]:
        return ks[0][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if t <= t1:
            u = ease((t - t0) / max(1e-6, t1 - t0))
            return v0 + (v1 - v0) * u if isinstance(v0, (int, float)) else lerp(v0, v1, u)
    return ks[-1][1]


def amap(x, a, b, c, d):
    """Arduino map() (integer, truncating)"""
    return int((x - a) * (d - c) / (b - a)) + c


def fade(t, t0, t1, ramp=0.25):
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


# ------------------------------------------------------------------ the sketch's screens
def big_word(sc, word, y):
    size = 2
    x = (128 - len(word) * 6 * size) // 2
    for i, c in enumerate(word):
        cx = x + i * 12
        if c == "g":
            sc.char(cx, y, "G", 2)
            sc.rect(cx + 2, y - 6, 2, 2); sc.rect(cx + 4, y - 4, 4, 2); sc.rect(cx + 8, y - 6, 2, 2)
        elif c == "i":
            sc.char(cx, y, "I", 2)
            sc.rect(cx + 4, y - 5, 2, 2)
        elif c == "s":
            sc.char(cx, y, "S", 2)
            sc.rect(cx + 4, y + 15, 2, 2); sc.rect(cx + 2, y + 17, 2, 2)
        else:
            sc.char(cx, y, c, 2)


def top_line(sc, best):
    sc.text(0, 0, "REKOR --.- sn" if best is None else "REKOR %.1f sn" % best, 1)


def word_for(heat):
    return "SOgUK" if heat < 100 else "ILIK" if heat < 180 else "SICAK" if heat < 230 else "YANIYOR!"


def scr_hunt(heat, best):
    sc = Screen()
    top_line(sc, best)
    big_word(sc, word_for(heat), 22)
    sc.rect(4, 48, 120, 14, fill=False)
    for i in range(amap(heat, 0, 255, 0, 12)):
        sc.rect(7 + i * 10, 51, 8, 8)
    return sc


def scr_found(found, record=True):
    sc = Screen()
    if record:
        sc.text(0, 2, "YENI REKOR!", 1)
        sc.set(20, 0)
    else:
        sc.text(0, 2, "BULDUN!", 1)
    big_word(sc, "HAZiNE!", 22)
    sc.text(22, 46, "%.1f sn" % found, 2)
    return sc


def scr_empty(best):
    sc = Screen()
    top_line(sc, best)
    big_word(sc, "BOs!", 22)
    return sc


def heat_of(pos, secret):
    d = min(50, abs(int(round(pos)) - secret))
    return amap(d, 0, 50, 255, 0), d


def heat_rgb(heat):
    return (heat / 255.0, 0.0, (255 - heat) / 255.0)


HEAT_WORD_TR = {"SOgUK": "SOĞUK", "ILIK": "ILIK", "SICAK": "SICAK", "YANIYOR!": "YANIYOR!"}


# ------------------------------------------------------------------ timing
def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


class Story:
    def __init__(self):
        b = os.path.join(HERE, "build")
        self.sched = json.load(open(os.path.join(b, "schedule.json"), encoding="utf-8"))
        self.dur = self.sched["duration"]
        self.L = {ln["id"]: ln for ln in self.sched["lines"]}
        shots = []
        for ln in self.sched["lines"]:
            if shots and shots[-1]["id"] == ln["vis"]:
                shots[-1]["lines"].append(ln["id"])
            else:
                shots.append({"id": ln["vis"], "lines": [ln["id"]], "start": ln["t0"] if shots else 0.0})
        for a, b2 in zip(shots, shots[1:]):
            a["end"] = b2["start"]
        shots[-1]["end"] = self.dur
        for s in shots:
            s["F0"] = round(s["start"] * FPS)
            s["n"] = round(s["end"] * FPS) - s["F0"]
        self.shots = shots
        self.S = {s["id"]: s for s in shots}
        self._plan()

    def nframes(self):
        return round(self.dur * FPS)

    def shot_at(self, T):
        for s in self.shots:
            if T < s["end"]:
                return s
        return self.shots[-1]

    def t0(self, lid):
        return self.L[lid]["t0"]

    def t1(self, lid):
        return self.L[lid]["t1"]

    def w(self, lid, word, nth=0):
        """global time of a spoken word in line lid"""
        want, k = norm(word), 0
        for x in self.L[lid]["words"]:
            if norm(x["w"]).startswith(want):
                if k == nth:
                    return x["t"]
                k += 1
        raise KeyError(f"{lid}: word {word!r} #{nth} not found")

    # -------------------------------------------------------------- the plan (all global times)
    def _plan(self):
        S = self.S
        self.HOOK_PRESS = 1.15
        b = S["build"]
        # build montage: a part lands on each spoken name, its wires follow
        self.DROP = {"oled": self.w("l02", "Ekran"), "buzzer": self.w("l02", "buzzer"), "button": self.w("l02", "buton"),
                     "pot": self.w("l02", "potansiyometre"), "rgb": self.w("l02", "Ar")}
        d = self.DROP
        self.WIRE_T = {}
        groups = {"oled": ["oled_gnd", "oled_vcc", "scl", "sda"], "buzzer": ["bz", "bz_gnd1", "bz_gnd2"],
                  "button": ["btn", "btn_gnd"], "pot": ["bridge", "pot_vcc", "pot_gnd", "pot_sig"],
                  "rgb": ["res_r", "res_g", "res_b", "rgb_r", "rgb_g", "rgb_b", "rgb_k"]}
        for part, ws in groups.items():
            gap = 0.07 if part != "rgb" else 0.06
            for i, wn in enumerate(ws):
                self.WIRE_T[wn] = d[part] + 0.22 + i * gap
        self.WIRE_T["pwr_red"] = b["start"] + 0.0
        self.WIRE_T["pwr_blk"] = b["start"] + 0.08
        self.BOOT = max(self.WIRE_T.values()) + 0.5
        # the hunt: knob keyframes on the spoken words
        h = S["hunt"]
        kz = self.w("l06", "Kaz")
        self.PRESS_FOUND = kz + 0.25
        self.HUNT_START = self.PRESS_FOUND - FOUND_S
        self.FOUND_END = self.PRESS_FOUND + sum(x[1] for x in FANFARE) + 3.0
        hk = [(h["start"] - 0.5, 12.0), (self.t1("l03"), 19.0), (self.w("l04", "tıklar"), 22.0), (self.t0("l05"), 24.0),
              (self.t1("l05"), 44.0), (self.w("l06", "Ilık") - 0.05, 48.0), (self.w("l06", "sıcak") - 0.3, 52.0),
              (self.w("l06", "sıcak") - 0.05, 63.0), (self.w("l06", "yanıyor") - 0.3, 65.0),
              (self.w("l06", "yanıyor") - 0.05, 76.0), (self.w("l06", "yanıyor") + 0.3, 72.0)]
        # explanation: the knob sweeps 0 -> 99 (l08), then walks to the new hiding place (l09),
        # stops on a wrong spot for the dig (l10)
        k8 = [(self.t0("l08") + 0.3, 72.0), (self.w("l08", "sıfırdan") - 0.1, 0.0), (self.w("l08", "doksan") + 0.6, 99.0),
              (self.t1("l08") + 0.1, 60.0)]
        k9 = [(self.w("l09", "Uzaklık") - 0.2, 60.0), (self.t1("l09") - 0.1, 23.0)]
        self.PRESS_EMPTY = self.w("l10", "Yanlış") - 0.05
        k10 = [(self.t0("l10"), 23.0), (self.PRESS_EMPTY - 0.6, 48.0)]
        kc = [(self.t0("l12"), 48.0), (self.t0("l12") + 2.5, 70.0), (self.dur, 82.0)]
        self.KNOB = hk + k8 + k9 + k10 + kc
        self.EMPTY_END = self.PRESS_EMPTY + 1.0
        # unplug / replug for the record (l11)
        self.UNPLUG = self.w("l11", "fişi") - 0.05
        self.REPLUG = self.w("l11", "silinmiyor") - 0.35
        self.REBOOT = self.REPLUG + 0.45

    # -------------------------------------------------------------- the simulated device
    def knob(self, T):
        sid = self.shot_at(T)["id"]
        if sid == "hook":
            return 72.0 + 0.6 * math.sin(T * 5)
        if sid == "build":
            return 12.0
        return keys(self.KNOB, T)

    def secret(self, T):
        if T < self.FOUND_END:
            return SECRET1
        if T < self.REBOOT:
            return SECRET2
        return SECRET3

    def best(self, T):
        return FOUND_S if T >= self.PRESS_FOUND else None

    def power(self, T):
        return not (self.UNPLUG + 0.12 <= T < self.REPLUG + 0.3)

    def running(self, T):
        """the sketch's loop() is running (not booting, not blocked in delay())"""
        sid = self.shot_at(T)["id"]
        if sid == "hook":
            return T < self.HOOK_PRESS
        if T < self.BOOT or not self.power(T) or self.REPLUG + 0.3 <= T < self.REBOOT:
            return False
        if self.PRESS_FOUND <= T < self.FOUND_END or self.PRESS_EMPTY <= T < self.EMPTY_END:
            return False
        return True

    def screen(self, T):
        sid = self.shot_at(T)["id"]
        if sid == "hook":
            if T < self.HOOK_PRESS:
                return scr_hunt(heat_of(self.knob(T), SECRET1)[0], None)
            return scr_found(FOUND_S)
        if sid == "build" and T < self.BOOT:
            return Screen() if T >= self.DROP["oled"] else None
        if not self.power(T):
            return None
        if T < self.BOOT or self.REPLUG + 0.3 <= T < self.REBOOT:
            return Screen()
        if self.PRESS_FOUND <= T < self.FOUND_END:
            return scr_found(FOUND_S)
        if self.PRESS_EMPTY <= T < self.EMPTY_END:
            return scr_empty(self.best(T))
        Tq = math.floor(T * 10) / 10  # the sketch redraws 10x a second
        return scr_hunt(heat_of(self.knob(Tq), self.secret(Tq))[0], self.best(Tq))

    def led(self, T):
        """(rgb 0..1, level)"""
        sid = self.shot_at(T)["id"]
        if sid == "build" and T < self.BOOT:
            return (0, 0, 0), 0.0
        if sid == "hook" and T >= self.HOOK_PRESS:
            return (1.0, 160 / 255, 0.0), 1.0
        if sid != "hook":
            if not self.power(T) or T < self.BOOT or self.REPLUG + 0.3 <= T < self.REBOOT:
                return (0, 0, 0), 0.0
            if self.PRESS_FOUND <= T < self.FOUND_END:
                return (1.0, 160 / 255, 0.0), 1.0
            if self.PRESS_EMPTY <= T < self.EMPTY_END:
                return (0, 0, 0), 0.0
        heat, _ = heat_of(self.knob(T), self.secret(T) if sid != "hook" else SECRET1)
        return heat_rgb(heat), 1.0

    def presses(self):
        return [self.HOOK_PRESS, self.PRESS_FOUND, self.PRESS_EMPTY]

    def press_dz(self, T, hold=0.16):
        dz = 0.0
        for t0 in self.presses():
            if t0 - 0.05 <= T <= t0 + hold:
                u = T - (t0 - 0.05)
                dz += -0.9 * min(1.0, u / 0.05) * (1.0 if T <= t0 + hold - 0.05 else max(0.0, (t0 + hold - T) / 0.05))
        return dz

    def usb_pull(self, T):
        return smooth((T - self.UNPLUG) / 0.35) - smooth((T - self.REPLUG) / 0.3)

    # -------------------------------------------------------------- sound + rings
    def ticks(self):
        """Geiger ticks of the sketch: [(T, pitch Hz, heat)] - tone(BUZZER, pitch, 15) every tickEvery ms"""
        if hasattr(self, "_ticks"):
            return self._ticks
        out = []
        T, step = 0.0, 1.0 / 1000
        last = None
        while T < self.dur - 0.3:
            if not self.running(T):
                last = None
                T += step
                continue
            sid = self.shot_at(T)["id"]
            sec = SECRET1 if sid == "hook" else self.secret(T)
            heat, d = heat_of(self.knob(T), sec)
            every = amap(d, 0, 50, 60, 700) / 1000.0
            if last is None or T - last >= every:
                out.append((round(T, 3), amap(d, 0, 50, 3000, 800), heat))
                last = T
            T += step
        self._ticks = out
        return out

    def waves(self):
        """[(T, kind)] sound-wave bursts at the buzzer (2D overlay)"""
        out = [(t, "tick%d" % min(4, heat * 5 // 256)) for t, _, heat in self.ticks()]
        for t0 in (self.HOOK_PRESS + 0.02, self.PRESS_FOUND + 0.02):
            acc = 0.0
            for f, dd in FANFARE:
                out.append((t0 + acc, "hi"))
                acc += dd
        out.append((self.PRESS_EMPTY + 0.02, "lo"))
        return sorted(out)

    def events(self):
        """sound effects [(T, kind, arg)] for mix.py"""
        ev = []
        for t, f, heat in self.ticks():
            sid = self.shot_at(t)["id"]
            ev.append((t, "tick", {"f": f, "vol": 0.30 if sid in ("hook", "hunt") else 0.16}))
        for t0 in (self.HOOK_PRESS, self.PRESS_FOUND, self.PRESS_EMPTY):
            ev.append((t0, "click", None))
        for t0 in (self.HOOK_PRESS + 0.02, self.PRESS_FOUND + 0.02):
            ev.append((t0, "fanfare", None))
        ev.append((self.PRESS_EMPTY + 0.02, "buzz_lo", None))
        for part, t in self.DROP.items():
            ev.append((t - 0.12, "whoosh", None))
            ev.append((t + 0.33, "pop", None))
        for wn, t in self.WIRE_T.items():
            ev.append((t + 0.35, "snap", None))
        ev.append((self.BOOT, "boot", None))
        ev.append((self.UNPLUG, "unplug", None))
        ev.append((self.REPLUG + 0.2, "plug", None))
        ev.append((self.REBOOT, "boot", None))
        ev.append((self.w("l12", "takip") + 0.1, "tap", None))
        ev.append((self.w("l12", "takip") + 0.25, "ding", None))
        return sorted(ev, key=lambda e: e[0])

    # -------------------------------------------------------------- 3D state per frame
    def state(self, T):
        sid = self.shot_at(T)["id"]
        st = {"shot": sid, "knob": self.knob(T), "screen": self.screen(T), "press": self.press_dz(T),
              "pull": self.usb_pull(T), "pwr": self.power(T) or sid in ("hook", "build"), "mark": None, "tags": {}}
        st["led"], st["led_level"] = self.led(T)
        parts = {"oled", "button", "buzzer", "pot", "rgb"}
        wires = None  # None = all wires drawn
        drop = {}
        if sid == "build":
            parts = {p for p, t in self.DROP.items() if T >= t - 0.3}
            drop = {p: t for p, t in self.DROP.items()}
            wires = {n: smooth((T - t) / 0.35) for n, t in self.WIRE_T.items()}
            labels = {"oled": "EKRAN · D21 D22", "buzzer": "BUZZER · D32", "button": "BUTON · D19",
                      "pot": "POT · D34", "rgb": "RGB LED · D25 D26 D27"}
            for p, t in self.DROP.items():
                st["tags"][p] = (fade(T, t + 0.15, self.BOOT + 0.6, 0.2), labels[p])
        st["parts"], st["wires"], st["drop"] = parts, wires, drop
        if sid in ("found", "how_dist") or (sid == "hunt" and T >= self.PRESS_FOUND):
            st["mark"] = SECRET1 if T < self.FOUND_END else SECRET2
        if sid == "hook" and T >= self.HOOK_PRESS:
            st["mark"] = SECRET1
        if sid == "how_dig":
            st["tags"]["dig"] = (fade(T, self.t0("l10") + 0.1, self.S["how_dig"]["end"], 0.2), "KAZ!")
        st["cam"] = self.camera(T)
        return st

    # -------------------------------------------------------------- cameras (mm; pos, target, lens)
    def camera(self, T):
        """portrait framing: the circuit sits in the middle ~45 % of the frame, titles above, captions below"""
        s = self.shot_at(T)
        sid, t, dur = s["id"], T - s["start"], s["end"] - s["start"]
        cl = (38.0, -8.0, 12.0)  # middle of the action cluster (knob, LED, buzzer, OLED, button)
        if sid == "hook":
            ks = [(0.0, (add(cl, (-4, -70, 112)), add(cl, (0, 2, 0)), 30)),
                  (self.HOOK_PRESS, (add(cl, (0, -62, 100)), add(cl, (0, 4, 0)), 30)),
                  (dur, (add(cl, (3, -56, 92)), add(cl, (0, 6, 0)), 30))]
        elif sid == "build":
            ks = [(0.0, ((12, -112, 178), (20, -2, 0), 28)), (dur, ((30, -98, 162), (22, -2, 0), 28))]
        elif sid == "hunt":
            pf = self.PRESS_FOUND - s["start"]
            ks = [(0.0, (add(POT, (-4, -46, 72)), add(POT, (-4, 2, -14)), 32)),
                  (self.t1("l03") - s["start"], (add(POT, (-10, -52, 80)), add(POT, (-8, 4, -14)), 32)),
                  (self.t0("l04") - s["start"] + 0.5, (add(cl, (-2, -74, 124)), add(cl, (0, 2, 0)), 32)),
                  (pf - 0.3, (add(cl, (2, -64, 108)), add(cl, (0, 4, 0)), 32)),
                  (dur, (add(cl, (2, -60, 102)), add(cl, (0, 6, 0)), 32))]
        elif sid == "found":
            ks = [(0.0, (add(cl, (2, -60, 102)), add(cl, (0, 6, 0)), 32)), (dur, (add(cl, (-4, -76, 128)), add(cl, (0, 2, 0)), 32))]
        elif sid == "how_knob":
            ks = [(0.0, (add(POT, (-8, -46, 70)), add(POT, (-4, 2, -14)), 34)), (dur, (add(POT, (4, -40, 62)), add(POT, (-2, 2, -14)), 34))]
        elif sid == "how_dist":
            mid = (38.0, -30.0, 12.0)
            ks = [(0.0, (add(mid, (-6, -62, 104)), add(mid, (0, 6, 0)), 32)), (dur, (add(mid, (6, -56, 96)), add(mid, (0, 6, 0)), 32))]
        elif sid == "how_dig":
            m = (32.0, 18.0, 12.0)
            ks = [(0.0, (add(m, (-8, -66, 100)), add(m, (0, 2, 0)), 32)), (dur, (add(m, (0, -58, 90)), add(m, (0, 2, 0)), 32))]
        elif sid == "how_save":
            mu = (-24.0, 4.0, 12.0)
            rp = self.REPLUG - s["start"]
            ks = [(0.0, (add(mu, (-6, -86, 136)), mu, 30)), (rp + 0.3, (add(mu, (2, -82, 130)), add(mu, (4, 0, 0)), 30)),
                  (dur, (add(cl, (-20, -80, 128)), add(cl, (-14, 2, 0)), 30))]
        else:  # cta: slow orbit of the running circuit
            u = t / max(dur, 1e-6)
            a = math.radians(-112.0 + 40.0 * u)
            c = (20.0, -2.0, 0.0)
            return (c[0] + 105 * math.cos(a), c[1] + 105 * math.sin(a), 182.0), c, 28.0
        p = keys([(k[0], k[1][0]) for k in ks], t)
        q = keys([(k[0], k[1][1]) for k in ks], t)
        lens = keys([(k[0], float(k[1][2])) for k in ks], t)
        return p, q, lens


if __name__ == "__main__":
    s = Story()
    for sh in s.shots:
        print(f"{sh['id']:<10} {sh['start']:6.2f}-{sh['end']:6.2f}  frames {sh['F0']:5d}+{sh['n']}")
    print("ticks", len(s.ticks()), "boot", round(s.BOOT, 2), "found press", round(s.PRESS_FOUND, 2), "dur", s.dur)
