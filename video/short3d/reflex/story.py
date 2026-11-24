"""The single source of timing for the reflex-game Short (Episode 10), EN or TR (pure Python: runs inside Blender
and in the repo venv). Language: env REFLEX_LANG (en|tr, make.py sets it). Everything is a function of the global
time T (seconds) and the narration's word times (build/<lang>/schedule.json from voice.py):

  shots           [{id, lines, start, end, F0, n}]  (a shot = consecutive lines with the same "vis"; frames F0 .. F0+n-1)
  state(T)        what the 3D scene shows: parts, OLED screen, button, USB, power LED, tags, camera
  events()        sound effects [(T, kind, arg)]: buzzer tones at the sketch's frequencies, clicks, plugs, pops
  waves()         [(T, kind)] for the 2D sound-wave rings at the buzzer (one burst per buzzer tone)

The device follows lessons/10-reflex-oled/code/reflex_oled/reflex_oled.ino: show(top, big) draws every screen
(size-1 line at 0,0, size-3 line at 0,28 - oledfont.Screen.show), press to start -> "get ready..." WAIT (1.5-4 s)
-> " GO!" + tone(1500, 150) -> press -> "NEW RECORD!" <ms>ms + tone(2000, 300) (or "your time"), 2 s later
"REFLEX 2.0  best:" <best>ms; the best time is read back from Preferences at boot, so it survives the unplug.
The hook (first ~3 s) is a flash-forward of the record round; the story then plays that round on the narration.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
from oledfont import Screen  # noqa: E402

LANG = os.environ.get("REFLEX_LANG", "en")
FPS = 30

# part anchors (mm, same maths as pbl.py / the Ep10 circuit)
OC = (44.45, 19.88, 13.5)            # OLED screen centre
BT = (17.78, 28.0, 17.0)             # button cap
BZ = (34.29, -38.16, 18.2)           # buzzer top
USBP = (-50.56, 0.0, 14.0)
CHIP = (-6.7, 0.0, 9.0)              # ESP32 module shield

RECORD, OLD_BEST, LATER = 214, 231, 263   # the record round, the best before it, the CTA round ("your time")
GO_TONE, REC_TONE = (1500, 0.15), (2000, 0.30)

# spoken words the events sit on, per language (prefix match, lower case)
WORDS = {
    "en": {"go": ("l02", "Go"), "pull": ("l04", "pull"), "dark": ("l04", "dark"), "plug": ("l05", "Plug"),
           "still": ("l05", "still"), "watch": ("l06", "stopwatch"), "drawer": ("l07", "drawer"),
           "power": ("l07", "without"), "screen": ("l08", "screen"), "buzzer": ("l08", "buzzer"),
           "button": ("l08", "button"), "follow": ("l09", "Follow"), "comments": ("l09", "comments")},
    "tr": {"go": ("l02", "Başla"), "pull": ("l04", "çekiyorum"), "dark": ("l04", "kararıyor"), "plug": ("l05", "takıyorum"),
           "still": ("l05", "hâlâ"), "watch": ("l06", "kronometresiyle"), "drawer": ("l07", "çekmecede"),
           "power": ("l07", "elektrik"), "screen": ("l08", "ekran"), "buzzer": ("l08", "buzzer"),
           "button": ("l08", "düğme"), "follow": ("l09", "takip"), "comments": ("l09", "yorumlara")},
}


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


def fade(t, t0, t1, ramp=0.25):
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


# ------------------------------------------------------------------ the sketch's screens (show(top, big))
def show(top, big):
    return Screen().show(top, big)


def scr_ready(best):
    return show("REFLEX 2.0  best:", "%dms" % best)


SCR_WAIT = show("get ready...", "WAIT")
SCR_GO = show("", " GO!")


def scr_record(ms):
    return show("NEW RECORD!", "%dms" % ms)


def scr_time(ms):
    return show("your time", "%dms" % ms)


def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


class Story:
    def __init__(self, lang=None):
        self.lang = lang or LANG
        self.B = os.path.join(HERE, "build", self.lang)
        self.sched = json.load(open(os.path.join(self.B, "schedule.json"), encoding="utf-8"))
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

    def word(self, name):
        lid, wd = WORDS[self.lang][name]
        return self.w(lid, wd)

    # -------------------------------------------------------------- the plan (all global times)
    def _plan(self):
        S = self.S
        self.HOOK_END = S["play"]["start"]
        # hook: flash-forward of the record round (WAIT -> GO! -> press 214 ms later -> NEW RECORD) inside 1 s
        self.H_GO = 0.7
        self.H_PRESS = self.H_GO + RECORD / 1000
        # the record round on the narration: press to start, GO on the spoken "GO"/"BAŞLA", press 214 ms later
        self.GO = self.word("go")
        # the sketch waits random(1500, 4000) ms; when "GO" comes early in the line the round started during the hook
        # (off camera): the play shot then opens on WAIT already, without the start press
        self.START = max(self.HOOK_END + 0.15, self.GO - 3.9)
        if self.GO - self.START < 1.6:
            self.START = self.GO - 2.0
        self.WAIT_S = self.GO - self.START
        self.PRESS = self.GO + RECORD / 1000
        self.READY1 = self.PRESS + 2.0      # state 3 -> 0 after 2 s: "REFLEX 2.0  best:" 214ms
        # unplug / replug (the record comes back from Preferences in setup())
        self.UNPLUG = self.word("pull") - 0.05
        self.DARK = self.word("dark")
        self.REPLUG = self.word("plug") - 0.25
        self.REBOOT = self.REPLUG + 0.6
        self.STILL = self.word("still")
        # parts: a label on each spoken name; the last round starts on "button" (state 0 -> press -> WAIT)
        self.PART_T = {"oled": self.word("screen"), "buzzer": self.word("buzzer"), "button": self.word("button")}
        self.START2 = self.PART_T["button"] + 0.25
        self.GO2 = max(self.START2 + 1.6, self.t1("l08") + 0.12)
        self.PRESS2 = self.GO2 + LATER / 1000
        self.READY2 = self.PRESS2 + 2.0
        self.TAP = self.word("follow") + 0.1

    # -------------------------------------------------------------- the simulated device
    def power(self, T):
        return not (self.UNPLUG + 0.12 <= T < self.REPLUG + 0.3)

    def best(self, T):
        if T < self.HOOK_END:
            return OLD_BEST if T < self.H_PRESS else RECORD
        return RECORD if T >= self.PRESS else OLD_BEST

    def screen(self, T):
        if T < self.HOOK_END:
            if T < self.H_GO:
                return SCR_WAIT
            return SCR_GO if T < self.H_PRESS else scr_record(RECORD)
        if not self.power(T):
            return None
        if self.REPLUG + 0.3 <= T < self.REBOOT:
            return Screen()
        if T < self.START:
            return scr_ready(OLD_BEST)
        if T < self.GO:
            return SCR_WAIT
        if T < self.PRESS:
            return SCR_GO
        if T < self.READY1 and T < self.UNPLUG:
            return scr_record(RECORD)
        if T < self.START2:
            return scr_ready(RECORD)
        if T < self.GO2:
            return SCR_WAIT
        if T < self.PRESS2:
            return SCR_GO
        if T < self.READY2:
            return scr_time(LATER)
        return scr_ready(RECORD)

    def presses(self):
        return [self.H_PRESS] + ([self.START] if self.START >= self.HOOK_END else []) +             [self.PRESS, self.START2, self.PRESS2]

    def press_dz(self, T, hold=0.16):
        dz = 0.0
        for t0 in self.presses():
            if t0 - 0.05 <= T <= t0 + hold:
                u = T - (t0 - 0.05)
                dz += -0.9 * min(1.0, u / 0.05) * (1.0 if T <= t0 + hold - 0.05 else max(0.0, (t0 + hold - T) / 0.05))
        return dz

    def usb_pull(self, T):
        return smooth((T - self.UNPLUG) / 0.35) - smooth((T - self.REPLUG) / 0.3)

    def dark(self, T):
        """2D dimming of the whole picture while the board is unplugged ("everything goes dark")"""
        return 0.55 * smooth((T - (self.UNPLUG + 0.1)) / 0.5) * (1 - smooth((T - (self.REPLUG + 0.25)) / 0.3))

    # -------------------------------------------------------------- sound + rings
    def tones(self):
        """buzzer tones [(T, Hz, s)] exactly where the sketch calls tone()"""
        return [(self.H_GO, *GO_TONE), (self.H_PRESS, *REC_TONE), (self.GO, *GO_TONE), (self.PRESS, *REC_TONE),
                (self.GO2, *GO_TONE)]

    def waves(self):
        """[(T, kind)] sound-wave bursts at the buzzer (2D overlay, overlay.WAVE kinds)"""
        return sorted((t, "go" if f == GO_TONE[0] else "rec") for t, f, d in self.tones())

    def events(self):
        """sound effects [(T, kind, arg)] for mix.py"""
        ev = [(t, "tone", {"f": f, "d": d}) for t, f, d in self.tones()]
        for t0 in self.presses():
            ev.append((t0, "click", None))
        ev.append((self.UNPLUG, "unplug", None))
        ev.append((self.UNPLUG + 0.1, "down", None))
        ev.append((self.REPLUG + 0.2, "plug", None))
        ev.append((self.REBOOT, "boot", None))
        for p, t in self.PART_T.items():
            ev.append((t + 0.05, "pop", None))
        ev.append((self.STILL, "ding", None))
        ev.append((self.TAP, "tap", None))
        ev.append((self.TAP + 0.15, "ding", None))
        return sorted(ev, key=lambda e: e[0])

    # -------------------------------------------------------------- 3D state per frame
    def state(self, T):
        sid = self.shot_at(T)["id"]
        st = {"shot": sid, "screen": self.screen(T), "press": self.press_dz(T), "pull": self.usb_pull(T),
              "pwr": self.power(T), "tags": {}, "hop": {}}
        if sid == "parts":
            end = self.S["parts"]["end"]
            labels = {"en": {"oled": "OLED · D21 D22", "buzzer": "BUZZER · D32", "button": "BUTTON · D19"},
                      "tr": {"oled": "EKRAN · D21 D22", "buzzer": "BUZZER · D32", "button": "DÜĞME · D19"}}[self.lang]
            for p, t in self.PART_T.items():
                st["tags"][p] = (fade(T, t - 0.05, end - 0.1, 0.2), labels[p])
                u = (T - t) / 0.35
                st["hop"][p] = 4.0 * math.sin(math.pi * u) if 0 <= u <= 1 else 0.0
        st["cam"] = self.camera(T)
        return st

    # -------------------------------------------------------------- cameras (mm; pos, target, lens)
    def camera(self, T):
        """portrait framing: the circuit sits in the middle ~45 % of the frame, titles above, captions below"""
        s = self.shot_at(T)
        sid, t, dur = s["id"], T - s["start"], s["end"] - s["start"]
        cl = (32.0, 2.0, 10.0)  # middle of the game cluster (OLED, button, buzzer)
        cg = (32.0, -9.0, 10.0)  # between OLED and buzzer: the buzzer stays above the caption band
        if sid == "hook":
            ks = [(0.0, (add(cg, (-4, -86, 132)), cg, 30)),
                  (self.H_PRESS, (add(cg, (-1, -78, 120)), add(cg, (0, 1, 0)), 30)),
                  (dur, (add(cg, (3, -72, 112)), add(cg, (0, 2, 0)), 30))]
        elif sid == "play":
            p0 = self.PRESS - s["start"]
            ks = [(0.0, (add(cg, (8, -92, 138)), cg, 30)),
                  (max(0.5, p0 - 0.4), (add(cg, (2, -78, 120)), add(cg, (0, 1, 0)), 30)),
                  (dur, (add(OC, (-6, -60, 92)), add(OC, (-4, -4, 0)), 30))]
        elif sid == "power":
            mu = (-24.0, 4.0, 12.0)
            rp = self.REPLUG - s["start"]
            ks = [(0.0, (add(mu, (-6, -86, 136)), mu, 30)), (rp + 0.3, (add(mu, (2, -82, 130)), add(mu, (4, 0, 0)), 30)),
                  (max(rp + 1.2, dur - 0.6), (add(OC, (-4, -58, 88)), add(OC, (-2, -4, 0)), 30)),
                  (dur, (add(OC, (-2, -54, 82)), add(OC, (-2, -4, 0)), 30))]
        elif sid == "how_time":
            ks = [(0.0, (add(CHIP, (-14, -62, 96)), add(CHIP, (0, 4, 0)), 32)),
                  (dur, (add(CHIP, (6, -54, 84)), add(CHIP, (2, 4, 0)), 32))]
        elif sid == "how_save":
            mid = lerp(CHIP, OC, 0.5)
            ks = [(0.0, (add(CHIP, (6, -54, 84)), add(CHIP, (2, 4, 0)), 32)),
                  (dur, (add(mid, (8, -84, 128)), add(mid, (0, 2, 0)), 30))]
        elif sid == "parts":
            ks = [(0.0, ((14, -112, 176), (16, -2, 0), 28)), (dur, ((30, -100, 160), (20, -2, 0), 28))]
        else:  # cta: slow orbit of the running circuit
            u = t / max(dur, 1e-6)
            a = math.radians(-112.0 + 40.0 * u)
            c = (16.0, -2.0, 0.0)
            return (c[0] + 105 * math.cos(a), c[1] + 105 * math.sin(a), 182.0), c, 28.0
        p = keys([(k[0], k[1][0]) for k in ks], t)
        q = keys([(k[0], k[1][1]) for k in ks], t)
        lens = keys([(k[0], float(k[1][2])) for k in ks], t)
        return p, q, lens


if __name__ == "__main__":
    s = Story()
    for sh in s.shots:
        print(f"{sh['id']:<10} {sh['start']:6.2f}-{sh['end']:6.2f}  frames {sh['F0']:5d}+{sh['n']}")
    print(f"{s.lang}: dur {s.dur}  start {s.START:.2f} GO {s.GO:.2f} (wait {s.WAIT_S:.2f} s) press {s.PRESS:.2f} "
          f"unplug {s.UNPLUG:.2f} replug {s.REPLUG:.2f} go2 {s.GO2:.2f} (wait {s.GO2 - s.START2:.2f}) tap {s.TAP:.2f}")
