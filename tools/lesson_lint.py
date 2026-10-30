"""Lesson quality check: how learnable is an episode's narration/timing? (text + schedule only: it does not hear audio or see frames)

Reads video/<ep>/script.json and video/<ep>/build/schedule.json and prints warnings for:
  FAST    segment spoken faster than MAX_WPM
  LONG    sentence longer than MAX_SENT words (30 in dub texts)
  DENSE   segment longer than MAX_WORDS
  FRAGMENT segment with 2+ sentences of <= 3 words (telegraphic style)
  JARGON  sentence with 3+ code terms chained
  EXAMPLE scene of 3+ segments without an everyday-example phrase
  NEWTERM segment introduces >1 new term, or a new term right after a short gap (< MIN_TERM_GAP s)
  QUESTION "Quick question" without a 2.5-4.5 s thinking pause after it
  RULES   production-guideline checks: cold open shows the result, no spoken "subscribe", comments invitation at the end
Section-10 checks (only when script.json has "music": "results"):
  LENGTH  body above the approximate 12-minute target (info line always)   QGAP  over 180 s between question moments
  RETRIEVAL no "retrieval" scene right after the sting   LIMIT  everyday example without its limit
  PREDICT tour/trace scene without a prediction pause   MISTAKE no "mistake" scene   EXPLAIN no "in your own words"

Usage: python tools/lesson_lint.py ep05 [ep04 ...] [--estimate]
(--estimate, or no build/schedule.json yet: timeline estimated from word counts, for the script stage)
"""
import glob, json, os, re, sys

MAX_WPM = 175
MAX_WORDS = 85
MAX_SENT = 24
CODE_TERMS = ["HIGH", "LOW", "state", "last state", "last blink", "last change", "LED on", "now", "millis", "delay", "setup", "loop",
              "digital read", "digital write", "pin mode", "input", "output", "pull up", "const", "true", "false", "analog read",
              "analog write", "map", "blinking", "presses"]
CODE_RX = re.compile(r"\b(?:" + "|".join(CODE_TERMS) + r")\b", re.I)
NO_EXAMPLE = {"cold", "outro", "prac", "parts", "trouble", "challenge"}
EXAMPLE_RX = re.compile(r"\b(like (a|an|the|your)|just like|it's like|works like|think of|imagine|picture an?|say you're|as if)\b", re.I)
MIN_TERM_GAP = 0.8
Q_MIN, Q_MAX = 2.5, 4.5
# first appearance of any of these in narration = "introduction" of a new concept
TERMS = {
    "pull-up": r"pull[- ]up", "pull-down": r"pull[- ]down", "floating": r"\bfloating\b", "edge": r"\bedge\b",
    "bool": r"\bbool\b", "bounce": r"\bbounc", "millis": r"\bmillis\b", "unsigned long": r"unsigned long",
    "PWM": r"\bpwm\b", "duty cycle": r"duty cycle", "analog write": r"analog write", "function": r"\bour own function\b|\bhelper function\b",
    "RGB": r"\brgb\b", "common cathode": r"common cathode", "common anode": r"common anode", "else if": r"else if",
    "serial plotter": r"serial plotter", "potentiometer": r"potentiometer", "analog read": r"analog read", "ADC": r"\badc\b",
    "interrupt": r"\binterrupt", "LDR": r"\bldr\b", "tone": r"\btone\b",
}

def sentences(t):
    return [x for x in re.split(r"(?<=[.!?:;])\s+", t.strip()) if x]

def fragments(t):
    # full stops only: "Quick question:" or "Part two:" lead into a sentence, they are not fragments
    full = [x for x in re.split(r"(?<=[.!?])\s+", t.strip()) if x]
    return sum(len(x.split()) <= 3 for x in full) >= 2

def dubs(ep):
    out = {}
    for f in sorted(glob.glob(f"video/{ep}/dub/*.json")):
        out[os.path.basename(f)[:-5]] = json.load(open(f, encoding="utf-8")).get("segments", {})
    return out

EST_WPM, EST_GAP = 148, 0.5  # --estimate: measured on the recap v3 narration (2026-10-29)

def estimate(sc, lead_in=0.8):
    """Script-stage timeline before any narration exists: words at EST_WPM, EST_GAP + pad between segments."""
    t, out = lead_in, {}
    for s in sc:
        dur = len(s["text"].split()) / EST_WPM * 60
        out[s["id"]] = {"start": t, "dur": dur, "end": t + dur, "scene": s["scene"]}
        t += dur + EST_GAP + s.get("pad", 0)
    return out, t

def load(ep, est=False):
    meta = json.load(open(f"video/{ep}/script.json", encoding="utf-8"))
    sc = meta["segments"]
    path = f"video/{ep}/build/schedule.json"
    if est or not os.path.exists(path):
        segs, total = estimate(sc, meta.get("lead_in", 0.8))
        return sc, segs, total
    sch = json.load(open(path, encoding="utf-8"))
    return sc, sch["segments"], sch["duration"]

Q_RX = re.compile(r"quick question|pause the video|pause now|predict|what do you think|what will|your turn", re.I)
EX_RX = re.compile(r"(like (a|an|the|your)|just like|it's like|works like|think of|imagine|picture an?|say you're)", re.I)
LIMIT_RX = re.compile(r"the difference|unlike|but a real|where the picture breaks|the picture stops", re.I)
PRED_RX = re.compile(r"pause|predict|what will|what do you think", re.I)
QGAP_MAX, RETR_MAX, LEN_MAX = 180, 120, 720

def section10(sc, sch, ids, total, sting):
    warns = []
    info = f"{total/60:.1f} min (target about 8-12 min; average 10)"
    if total > LEN_MAX:
        warns.append(("-", "LENGTH", f"{total/60:.1f} min: above the approximate 8-12 min target; review pacing"))
    qs = [sch[s["id"]]["start"] for s in sc if s["id"] in sch and Q_RX.search(s["text"])]
    end = sch[sting]["end"] if sting in sch else 0
    pts = [end] + qs + [total]
    for a, b in zip(pts, pts[1:]):
        if b - a > QGAP_MAX:
            warns.append(("-", "QGAP", f"{b-a:.0f} s without a question moment ({a:.0f}-{b:.0f} s)"))
    if not any(s["scene"] == "retrieval" and s["id"] in sch and 0 <= sch[s["id"]]["start"] - end <= RETR_MAX for s in sc):
        warns.append(("-", "RETRIEVAL", f"no retrieval scene within {RETR_MAX} s after the sting"))
    scenes = {}
    for s in sc:
        if s["id"] in sch:
            scenes.setdefault(s["scene"], []).append(s)
    for name, segs in scenes.items():
        t = " ".join(x["text"] for x in segs)
        if EX_RX.search(t) and not LIMIT_RX.search(t):
            warns.append((segs[0]["id"], "LIMIT", f"scene {name}: example without its limit"))
        if (name.startswith("tour") or "trace" in name) and not PRED_RX.search(t):
            warns.append((segs[0]["id"], "PREDICT", f"scene {name}: no prediction pause"))
    if "mistake" not in scenes:
        warns.append(("-", "MISTAKE", "no common-mistake scene"))
    if not re.search(r"in your own words", " ".join(s["text"] for s in sc), re.I):
        warns.append(("-", "EXPLAIN", "no 'in your own words' invitation"))
    return warns, info

def main():
    eps = [a for a in sys.argv[1:] if not a.startswith("--")]
    for ep in eps:
        sc, sch, total = load(ep, "--estimate" in sys.argv)
        if "--estimate" in sys.argv or not os.path.exists(f"video/{ep}/build/schedule.json"):
            print(f"(estimated timeline: {EST_WPM} wpm, no narration yet)")
        meta = json.load(open(f"video/{ep}/script.json", encoding="utf-8"))
        ids = [s["id"] for s in sc if s["id"] in sch]
        text = {s["id"]: s["text"] for s in sc}
        warns = []
        seen = set()
        spoken = sum(len(text[i].split()) for i in ids)
        for n, i in enumerate(ids):
            t, seg = text[i], sch[i]
            w = len(t.split())
            wpm = w / seg["dur"] * 60
            if wpm > MAX_WPM:
                warns.append((i, "FAST", f"{wpm:.0f} wpm: {t[:70]}"))
            if w > MAX_WORDS:
                warns.append((i, "DENSE", f"{w} words, {seg['dur']:.0f} s: {t[:70]}"))
            for x in sentences(t):
                if len(x.split()) > MAX_SENT:
                    warns.append((i, "LONG", f"{len(x.split())}-word sentence: {x[:70]}"))
                if len(CODE_RX.findall(x)) >= 3:
                    warns.append((i, "JARGON", f"{len(CODE_RX.findall(x))} code terms: {x[:70]}"))
            if fragments(t):
                warns.append((i, "FRAGMENT", f"telegraphic: {t[:70]}"))
            teaser = re.search(r"next time", t, re.I)  # outro teaser names future topics: not taught here
            new = [] if teaser else [k for k, rx in TERMS.items() if k not in seen and re.search(rx, t, re.I)]
            seen.update(new)
            gap = seg["start"] - sch[ids[n - 1]]["end"] if n else 9
            if len(new) > 1:
                warns.append((i, "NEWTERM", f"{len(new)} new terms at once: {', '.join(new)}"))
            elif new and gap < MIN_TERM_GAP:
                warns.append((i, "NEWTERM", f"'{new[0]}' starts after only {gap:.2f} s of silence"))
            if re.search(r"quick question", t, re.I) and n + 1 < len(ids):
                g = sch[ids[n + 1]]["start"] - seg["end"]
                if not Q_MIN <= g <= Q_MAX:
                    warns.append((i, "QUESTION", f"thinking pause {g:.2f} s (want {Q_MIN}-{Q_MAX})"))
        # episode-level rules
        first = " ".join(text[i] for i in ids[:3]).lower()
        if sc[0]["scene"] != "cold":
            warns.append(("-", "RULES", "episode does not open with a cold-open result scene"))
        if re.search(r"\b(subscribe|like and)\b", " ".join(text.values()), re.I):
            warns.append(("-", "RULES", "narration says 'subscribe'/'like and' (icons only)"))
        if int(re.sub(r"\D", "", ep) or 0) >= 5 and not re.search(r"comments", " ".join(text[i] for i in ids[-3:]), re.I):  # rule applies from ep05
            warns.append(("-", "RULES", "last segments do not invite viewers to the comments"))
        info = None
        if meta.get("music") == "results":
            w10, info = section10(sc, sch, ids, total, meta.get("sting_after"))
            warns += w10
        print(f"\n== {ep}: {len(ids)} segments, {total/60:.1f} min narration timeline, avg {spoken/ (total/60):.0f} wpm incl. pauses ==")
        if info:
            print(f"  -       INFO     {info}")
        for i, kind, msg in warns:
            print(f"  {i:7s} {kind:8s} {msg}")
        print(f"  -> {len(warns)} warnings")

if __name__ == "__main__":
    main()
