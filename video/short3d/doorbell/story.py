"""The single source of timing for the phone-doorbell Short (Episode 12 phone control), EN or TR (pure Python: runs
inside Blender and in the repo venv). Language: env DOORBELL_LANG (en|tr, make.py sets it). Everything is a function
of the global time T (seconds) and the narration's word times (build/<lang>/schedule.json from voice.py):

  shots           [{id, lines, start, end, F0, n}]  (a shot = consecutive lines with the same "vis"; frames F0 .. F0+n-1)
  cmds            the taps on the phone: Cmd(t, key, n, fly) - tap at t, the link (packet) flies phone -> antenna,
                  the board acts at `arrive` (lessons/12-phone-control/code/phone_remote/phone_remote.ino)
  screen(T)/led(T) the OLED (show(): size-1 "command #N" at 0,0, size-2 colour / "RING!" at 0,28) and the RGB LED
  tones()         buzzer tones [(T, Hz, s)]: handleRing() = tone(1319, 180), delay(200), tone(1047, 300)
  events()        sound effects for mix.py;  waves() 2D sound-wave rings at the buzzer (one burst per tone)

Story: hook (flash-forward of the ring: tap RING -> packet -> ding dong + "command #1 / RING!") -> noapp (no app, no
router, no internet; the router shrinks away) -> wifi (the board's own Wi-Fi ripples from the antenna, like a phone
hotspot) -> join (phone close-up: Wi-Fi list, tap PinByPin-ESP32, connected, 192.168.4.1 typed, the page) -> send
(tap RING, the link flies through the air, ding dong on "plays") -> colors (green #2, blue #3, red #4, the screen
counts) -> parts (RGB LED D25 D26 D27, OLED D21 D22, buzzer D32) -> cta (follow card).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "b3d"))
from oledfont import Screen  # noqa: E402

LANG = os.environ.get("DOORBELL_LANG", "en")
FPS = 30

DING, DONG, DONG_AT = (1319, 0.18), (1047, 0.30), 0.20   # tone(1319, 180); delay(200); tone(1047, 300)
COL = {"red": (1, 0, 0), "green": (0, 1, 0), "blue": (0, 0, 1), "off": (0, 0, 0)}

# spoken words the events sit on, per language: (line, word prefix) or (line, word index)
WORDS = {
    "en": {"tap": ("l01", "tap"), "app": ("l02", 1), "router": ("l02", 3), "internet": ("l02", 5),
           "wifi": ("l03", "Wi"), "own": ("l03", "own"), "hotspot": ("l03", "hotspot"),
           "joins": ("l04", "joins"), "opens": ("l04", "opens"), "page": ("l04", "page"),
           "link": ("l05", "link"), "ring": ("l05", "ring"), "air": ("l05", "air"), "plays": ("l06", "plays"),
           "notes": ("l06", "notes"), "c1": ("l07", "color"), "c2": ("l07", "light"), "c3": ("l07", "screen"),
           "counts": ("l07", "counts"), "light": ("l08", "light"), "screen": ("l08", "screen"),
           "buzzer": ("l08", "buzzer"), "follow": ("l09", "Follow"), "comments": ("l09", "tell")},
    "tr": {"tap": ("l01", "dokunuyorum"), "app": ("l02", 0), "router": ("l02", 2), "internet": ("l02", 4),
           "wifi": ("l03", "Wi"), "own": ("l03", "kendi"), "hotspot": ("l03", "erişim"),
           "joins": ("l04", "bağlanıp"), "opens": ("l04", "açıyor"), "page": ("l04", "sayfasını"),
           "link": ("l05", "bağlantı"), "ring": ("l05", "dokununca"), "air": ("l05", "havadan"),
           "plays": ("l06", "buzzer"), "notes": ("l06", "nota"), "c1": ("l07", "Renk"), "c2": ("l07", "değiştiriyor"),
           "c3": ("l07", "ekran"), "counts": ("l07", "sayıyor"), "light": ("l08", "ışık"), "screen": ("l08", "ekran"),
           "buzzer": ("l08", "buzzer"), "follow": ("l09", "takip"), "comments": ("l09", "yorumlara")},
}


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def fade(t, t0, t1, ramp=0.25):
    return smooth((t - t0) / ramp) * (1 - smooth((t - t1) / ramp))


def show(top, big):
    """the sketch's show(): textSize(1) at (0,0), textSize(2) at (0,28)"""
    s = Screen()
    s.text(0, 0, top, 1)
    s.text(0, 28, big, 2)
    return s


SCR_READY = show("open 192.168.4.1", "READY")  # setup(): show(("open " + ip.toString()).c_str(), "READY")


def scr_cmd(n, what):
    return show("command #%d" % n, what)


def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


class Cmd:
    """one tap on the phone: tap dot + click at t, the link (packet) phone -> antenna, the board acts at arrive"""

    def __init__(self, t, key, n, fly=0.3):
        self.t, self.key, self.n, self.fly = t, key, n, fly
        self.arrive = t + 0.08 + fly


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
        """global time of a spoken word in line lid (word = prefix, or an index into the line's words)"""
        if isinstance(word, int):
            return self.L[lid]["words"][word]["t"]
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
        self.HOOK_END = S["noapp"]["start"]
        # hook: flash-forward of the ring (command #1)
        self.H_CMD = Cmd(max(0.3, self.word("tap") - 0.05), "ring", 1, fly=0.85)
        # send: tap RING on "ring", the link flies "through the air", the board plays on "plays"
        t_tap = self.word("ring")
        self.RING = Cmd(t_tap, "ring", 1, fly=max(0.6, self.word("plays") - 0.05 - t_tap - 0.08))
        # colors: green #2, blue #3, red #4 (fast, the real speed)
        self.COLS = [Cmd(self.word("c1") + 0.05, "green", 2), Cmd(self.word("c2"), "blue", 3), Cmd(self.word("c3") - 0.1, "red", 4)]
        self.PART_T = {"rgb": self.word("light"), "oled": self.word("screen"), "buzzer": self.word("buzzer")}
        self.TAP = self.word("follow") + 0.1
        # join: Wi-Fi list -> tap the network on "joins" -> connected -> the address typed on "opens" -> the page
        self.J_TAP = self.word("joins") - 0.1
        self.J_TYPE = self.word("opens") - 0.1
        self.J_PAGE = self.J_TYPE + 0.06 * 11 + 0.25

    def cmds(self, T):
        """the taps that belong to the shot at T"""
        sid = self.shot_at(T)["id"]
        if sid == "hook":
            return [self.H_CMD]
        if sid == "send":
            return [self.RING]
        if sid == "colors":
            return self.COLS
        return []

    # -------------------------------------------------------------- the simulated device
    def device(self, T):
        """(screen, led) after the commands so far (the hook is a flash-forward: its own timeline)"""
        sid = self.shot_at(T)["id"]
        if sid == "hook":
            return (scr_cmd(1, "RING!") if T >= self.H_CMD.arrive else SCR_READY), COL["off"]
        if sid in ("noapp", "wifi", "join"):
            return SCR_READY, COL["off"]
        if sid == "send":
            return (scr_cmd(1, "RING!") if T >= self.RING.arrive else SCR_READY), COL["off"]
        scr, led = scr_cmd(1, "RING!"), COL["off"]
        for c in self.COLS:
            if T >= c.arrive:
                scr, led = scr_cmd(c.n, c.key), COL[c.key]
        return scr, led

    def phone(self, T):
        """(phone screen state, pressed key) - video/ep12/b3d/phone_screens.py states"""
        sid = self.shot_at(T)["id"]
        if sid == "join":
            if T < self.J_TAP:
                return "wifi_list", None
            if T < self.J_TAP + 0.45:
                return "wifi_tap", "wifi_net"
            if T < self.J_TYPE:
                return "wifi_connected", None
            if T < self.J_PAGE:
                return "addr_type_%d" % max(0, min(11, int((T - self.J_TYPE) / 0.06) + 1)), None
            return "page", None
        for c in self.cmds(T):
            if c.t - 0.05 <= T < c.t + 0.35:
                return "page_" + c.key, c.key
        return "page", None

    def packet(self, T):
        """(command, u 0..1 along the phone -> antenna arc) or None"""
        for c in self.cmds(T):
            if c.t + 0.08 <= T < c.arrive:
                return c, (T - c.t - 0.08) / c.fly
        return None

    # -------------------------------------------------------------- sound + rings
    def tones(self):
        out = []
        for c in (self.H_CMD, self.RING):
            out += [(c.arrive, *DING), (c.arrive + DONG_AT, *DONG)]
        return sorted(out)

    def waves(self):
        return [(t, "ding" if f == DING[0] else "dong") for t, f, d in self.tones()]

    def events(self):
        ev = [(t, "tone", {"f": f, "d": d}) for t, f, d in self.tones()]
        for c in [self.H_CMD, self.RING] + self.COLS:
            ev += [(c.t, "tap", None), (c.t + 0.08, "whoosh", None)]
        ev.append((self.J_TAP, "tap", None))
        ev += [(self.J_TYPE + 0.06 * i, "key", None) for i in range(11)]
        for name in ("app", "router", "internet"):
            ev.append((self.word(name) + 0.1, "pop", None))
        for p, t in self.PART_T.items():
            ev.append((t + 0.05, "pop", None))
        ev.append((self.TAP, "tap", None))
        ev.append((self.TAP + 0.15, "ding", None))
        return sorted(ev, key=lambda e: e[0])

    def tags(self, T):
        sid = self.shot_at(T)["id"]
        out = {}
        if sid == "parts":
            end = self.S["parts"]["end"]
            labels = {"en": {"rgb": "RGB LED · D25 D26 D27", "oled": "OLED · D21 D22", "buzzer": "BUZZER · D32"},
                      "tr": {"rgb": "RGB LED · D25 D26 D27", "oled": "EKRAN · D21 D22", "buzzer": "BUZZER · D32"}}[self.lang]
            for p, t in self.PART_T.items():
                out[p] = (fade(T, t - 0.05, end - 0.1, 0.2), labels[p])
        return out


if __name__ == "__main__":
    s = Story()
    for sh in s.shots:
        print(f"{sh['id']:<10} {sh['start']:6.2f}-{sh['end']:6.2f}  frames {sh['F0']:5d}+{sh['n']}")
    print(f"{s.lang}: dur {s.dur}  hook tap {s.H_CMD.t:.2f} ding {s.H_CMD.arrive:.2f} | ring tap {s.RING.t:.2f} "
          f"fly {s.RING.fly:.2f} ding {s.RING.arrive:.2f} | colors {[round(c.arrive, 2) for c in s.COLS]} tap {s.TAP:.2f}")
