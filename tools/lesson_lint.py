"""Lesson quality check: how learnable is an episode's narration/timing? (text + schedule only: it does not hear audio or see frames)

Reads video/<ep>/script.json and video/<ep>/build/schedule.json and prints warnings for:
  FAST    segment spoken faster than MAX_WPM
  DENSE   segment longer than MAX_WORDS (a long run of facts in one breath)
  NEWTERM segment introduces >1 new term, or a new term right after a short gap (< MIN_TERM_GAP s)
  QUESTION "Quick question" without a 2.5-4.5 s thinking pause after it
  RULES   production-guideline checks: cold open shows the result, no spoken "subscribe", comments invitation at the end

Usage: python tools/lesson_lint.py ep05 [ep04 ...]
"""
import json, re, sys

MAX_WPM = 200
MAX_WORDS = 40
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

def load(ep):
    sc = json.load(open(f"video/{ep}/script.json", encoding="utf-8"))["segments"]
    sch = json.load(open(f"video/{ep}/build/schedule.json", encoding="utf-8"))
    return sc, sch["segments"], sch["duration"]

def main():
    eps = [a for a in sys.argv[1:] if not a.startswith("--")]
    for ep in eps:
        sc, sch, total = load(ep)
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
        if int(re.sub(r"\D", "", ep)) >= 5 and not re.search(r"comments", " ".join(text[i] for i in ids[-3:]), re.I):  # rule applies from ep05
            warns.append(("-", "RULES", "last segments do not invite viewers to the comments"))
        print(f"\n== {ep}: {len(ids)} segments, {total/60:.1f} min narration timeline, avg {spoken/ (total/60):.0f} wpm incl. pauses ==")
        for i, kind, msg in warns:
            print(f"  {i:7s} {kind:8s} {msg}")
        print(f"  -> {len(warns)} warnings")

if __name__ == "__main__":
    main()
