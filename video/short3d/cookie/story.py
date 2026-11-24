"""The single source of timing for the cookie-jar-guard Short (Episode 11 motion alarm), EN or TR (pure Python: runs
inside Blender and in the repo venv). Language: env COOKIE_LANG (en|tr, make.py sets it). Everything is a function of
the global time T (seconds) and the narration's word times (build/<lang>/schedule.json from voice.py):

  shots           [{id, lines, start, end, F0, n}]  (a shot = consecutive lines with the same "vis"; frames F0 .. F0+n-1)
  screen(T)       the OLED, exactly as lessons/11-motion-alarm/code/motion_alarm/motion_alarm.ino draws it
  tones()         buzzer tones [(T, Hz, s)] where the sketch calls tone(): countdown tick tone(2000, 30) once a second,
                  siren tone((inState / 250) % 2 ? 2600 : 1800) = 1800 Hz first, the note flips every 250 ms
  events()        sound effects [(T, kind, arg)] for mix.py;  waves() [(T, kind)] 2D sound-wave rings at the buzzer

Story: hook (flash-forward of the catch: the warm hand reaches for the jar, the lens windows light up, INTRUDER +
siren) -> arm (press, "leave the room!" 10 s countdown with a tick every second) -> catch (time skip: ARMED; the hand
sneaks in, INTRUDER + siren on the spoken "siren") -> ago (time skip, the siren stopped by itself after 15 s: "seen 1x,
last:" "2 min ago") -> how_lens (dome x-ray, the windows light one by one) -> how_yes (the hand crosses windows, OUT =
HIGH, thumbs up on "yes") -> how_stamp (the hand again: INTRUDER, the parking-ticket stamp lastMotion = now, siren) ->
parts (labels on the spoken names) -> cta (follow card, the guard stays armed behind it).
Screens: the Ep 11 sketch's show(): textSize(1) line at (0,0), textSize(2) line at (0,28) (video/ep11/b3d/ep11_3d.py).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
from oledfont import Screen  # noqa: E402

LANG = os.environ.get("COOKIE_LANG", "en")
FPS = 30

TICK = (2000, 0.03)          # countdown: tone(BUZZER_PIN, 2000, 30)
SIREN_LO, SIREN_HI, SIREN_STEP = 1800, 2600, 0.25
GRACE = 10.0                 # GRACE_MS
H_CATCH = 1.25               # hook: the moment the PIR says yes (s)
STAMP_MS = 754213            # the millis() value stamped on the ticket in how_stamp (12.5 min after power-on)

# spoken words the events sit on, per language (prefix match, lower case)
WORDS = {
    "en": {"arm": ("l02", "arm"), "leave": ("l02", "leave"), "sneak": ("l03", "sneaks"), "siren": ("l03", "siren"),
           "two": ("l04", "two"), "motion": ("l05", "motion"), "warmth": ("l05", "warmth"), "windows": ("l05", "windows"),
           "moves": ("l06", "moves"), "next": ("l06", "next"), "yes": ("l06", "yes"), "stamps": ("l07", "stamps"),
           "parking": ("l07", "parking"), "siren2": ("l07", "siren"), "sensor": ("l08", "sensor"),
           "screen": ("l08", "screen"), "buzzer": ("l08", "buzzer"), "guard": ("l08", "guard"),
           "follow": ("l09", "Follow"), "comments": ("l09", "tell")},
    "tr": {"arm": ("l02", "Kuruyorum"), "leave": ("l02", "çıkmak"), "sneak": ("l03", "sinsice"), "siren": ("l03", "siren"),
           "two": ("l04", "iki"), "motion": ("l05", "hareket"), "warmth": ("l05", "Sıcaklığı"), "windows": ("l05", "pencereden"),
           "moves": ("l06", "pencereden"), "next": ("l06", "diğerine"), "yes": ("l06", "evet"), "stamps": ("l07", "damgalıyor"),
           "parking": ("l07", "otopark"), "siren2": ("l07", "siren"), "sensor": ("l08", "sensör"),
           "screen": ("l08", "ekran"), "buzzer": ("l08", "buzzer"), "guard": ("l08", "bekçi"),
           "follow": ("l09", "takip"), "comments": ("l09", "yorumlara")},
}


# ------------------------------------------------------------------ helpers
def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def fade(t, t0, t1, ramp=0.25):
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


# ------------------------------------------------------------------ the sketch's screens
def show(top, big):
    """the Ep 11 sketch's show(): textSize(1) at (0,0), textSize(2) at (0,28)"""
    s = Screen()
    s.text(0, 0, top, 1)
    s.text(0, 28, big, 2)
    return s


SCR_READY = show("press to arm", "READY")
SCR_ARMED = show("guarding...", "ARMED")
SCR_INTRUDER = show("motion detected!", "INTRUDER")
SCR_SEEN = show("seen 1x, last:", "2 min ago")


def scr_leave(left):
    return show("leave the room!", f"{left} s")


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
        self.HOOK_END = S["arm"]["start"]
        self.H_CATCH = H_CATCH
        # the arm press (countdown starts, state 2): on the spoken "arm", but never before the arm shot is on screen
        # (TR "Kuruyorum" opens the line)
        self.PRESS = max(self.word("arm") - 0.05, S["arm"]["start"] + 0.25)
        self.ARM_END = S["arm"]["end"]
        c = S["catch"]
        self.TC = self.word("siren") - 0.08             # the PIR says yes: INTRUDER + siren
        self.CATCH_END = c["end"]
        self.AGO0 = S["ago"]["start"]
        self.TWO = self.word("two")
        self.WIN = self.word("windows")
        self.MOVES = self.word("moves")
        self.YES = self.word("yes") - 0.1
        self.STAMP = self.word("stamps") - 0.1          # how_stamp: detection, lastMotion = now, siren
        self.SIREN2 = self.word("siren2")
        self.STAMP_END = S["how_stamp"]["end"]
        self.PART_T = {"pir": self.word("sensor"), "oled": self.word("screen"), "buzzer": self.word("buzzer"),
                       "button": self.word("guard")}
        self.TAP = self.word("follow") + 0.1

    # -------------------------------------------------------------- the simulated device
    def screen(self, T):
        sid = self.shot_at(T)["id"]
        if sid == "hook":
            return SCR_ARMED if T < self.H_CATCH else SCR_INTRUDER
        if sid == "arm":
            if T < self.PRESS:
                return SCR_READY
            ms = int(round((T - self.PRESS) * 1000))
            return scr_leave((int(GRACE * 1000) - ms + 999) // 1000) if ms < GRACE * 1000 else SCR_ARMED
        if sid == "catch":
            return SCR_ARMED if T < self.TC else SCR_INTRUDER
        if sid == "ago":
            return SCR_SEEN
        if sid in ("how_lens", "how_yes"):
            return SCR_ARMED
        if sid == "how_stamp":
            return SCR_ARMED if T < self.STAMP else SCR_INTRUDER
        return SCR_ARMED  # parts, cta: the guard is armed again

    def presses(self):
        return [self.PRESS]

    def press_dz(self, T, hold=0.16):
        dz = 0.0
        for t0 in self.presses():
            if t0 - 0.05 <= T <= t0 + hold:
                u = T - (t0 - 0.05)
                dz += -0.9 * min(1.0, u / 0.05) * (1.0 if T <= t0 + hold - 0.05 else max(0.0, (t0 + hold - T) / 0.05))
        return dz

    def countdown_left(self, T):
        """seconds left on the 'leave the room!' screen (None outside the countdown)"""
        if self.shot_at(T)["id"] != "arm" or T < self.PRESS:
            return None
        ms = int(round((T - self.PRESS) * 1000))
        return (int(GRACE * 1000) - ms + 999) // 1000 if ms < GRACE * 1000 else 0

    # -------------------------------------------------------------- sound + rings
    @staticmethod
    def _siren(t0, t1):
        out, i = [], 0
        while t0 + SIREN_STEP * i < t1 - 0.02:
            out.append((t0 + SIREN_STEP * i, SIREN_HI if i % 2 else SIREN_LO, min(SIREN_STEP, t1 - (t0 + SIREN_STEP * i))))
            i += 1
        return out

    def tones(self):
        """buzzer tones [(T, Hz, s)] exactly where the sketch calls tone(); a cut (time skip) ends a siren"""
        ts = self._siren(self.H_CATCH, self.HOOK_END)
        for i in range(int(GRACE)):  # one tick per new countdown number, only while the arm shot is on screen
            t = self.PRESS + i
            if t < self.ARM_END - 0.05:
                ts.append((t, *TICK))
        ts += self._siren(self.TC, self.CATCH_END)
        ts += self._siren(self.STAMP, self.STAMP_END)
        return sorted(ts)

    def waves(self):
        """[(T, kind)] sound-wave bursts at the buzzer (2D overlay): tick / lo (1800 Hz) / hi (2600 Hz)"""
        out = []
        for t, f, d in self.tones():
            out.append((t, "tick" if f == TICK[0] else ("hi" if f == SIREN_HI else "lo")))
        return out

    def events(self):
        """sound effects [(T, kind, arg)] for mix.py"""
        ev = [(t, "tone", {"f": f, "d": d}) for t, f, d in self.tones()]
        for t0 in self.presses():
            ev.append((t0, "click", None))
        ev.append((self.HOOK_END - 0.02, "whoosh", None))
        ev.append((self.CATCH_END - 0.02, "whoosh", None))
        ev.append((self.STAMP + 0.2, "stamp", None))  # the ticket stamp lands (compose.ticket)
        ev.append((self.YES, "ding", None))
        for p, t in self.PART_T.items():
            ev.append((t + 0.05, "pop", None))
        ev.append((self.TAP, "tap", None))
        ev.append((self.TAP + 0.15, "ding", None))
        return sorted(ev, key=lambda e: e[0])

    # -------------------------------------------------------------- per-frame state shared by scene3d / compose
    def tags(self, T):
        sid = self.shot_at(T)["id"]
        out = {}
        if sid == "parts":
            end = self.S["parts"]["end"]
            labels = {"en": {"pir": "PIR SENSOR · D33", "oled": "OLED · D21 D22", "buzzer": "BUZZER · D32", "button": "BUTTON · D19"},
                      "tr": {"pir": "PIR SENSÖR · D33", "oled": "EKRAN · D21 D22", "buzzer": "BUZZER · D32", "button": "DÜĞME · D19"}}[self.lang]
            for p, t in self.PART_T.items():
                out[p] = (fade(T, t - 0.05, end - 0.1, 0.2), labels[p])
        elif sid == "how_yes":
            hi = T >= self.YES
            txt = {"en": ("OUT = LOW", "OUT = HIGH (yes!)"), "tr": ("OUT = LOW", "OUT = HIGH (evet!)")}[self.lang]
            out["out"] = (fade(T, self.S["how_yes"]["start"] + 0.2, self.S["how_yes"]["end"] - 0.1, 0.2), txt[1] if hi else txt[0])
        elif sid == "how_lens":
            txt = {"en": "lens = many little windows", "tr": "mercek = birçok küçük pencere"}[self.lang]
            out["dome"] = (fade(T, self.WIN - 0.1, self.S["how_lens"]["end"] - 0.1, 0.2), txt)
        return out


if __name__ == "__main__":
    s = Story()
    for sh in s.shots:
        print(f"{sh['id']:<10} {sh['start']:6.2f}-{sh['end']:6.2f}  frames {sh['F0']:5d}+{sh['n']}")
    print(f"{s.lang}: dur {s.dur}  press {s.PRESS:.2f} (arm end {s.ARM_END:.2f}) catch {s.TC:.2f} stamp {s.STAMP:.2f} "
          f"yes {s.YES:.2f} tap {s.TAP:.2f}")
    print("tones", len(s.tones()))
