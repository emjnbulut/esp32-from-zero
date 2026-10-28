"""Check a scene file's word anchors against the narration BEFORE narrating/rendering.

W("s08", "duty") or W("s26", "new", 4) in video/<ep>/<ep>.js needs that word (4 times) in segment s08's English text;
a missing word makes the engine fall back to the segment start, so the animation fires early (render.log only
says "word not found" after a 20-minute render). S0/S1/T("sNN") need the segment to exist.

Usage: python tools/anchor_check.py recap1 [ep05 ...]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())  # same as engine/lib.js norm()


def main():
    bad = 0
    for ep in sys.argv[1:]:
        d = ROOT / "video" / ep
        js = (d / f"{ep}.js").read_text(encoding="utf-8")
        seg = {s["id"]: [norm(w) for w in s["text"].split()]
               for s in json.loads((d / "script.json").read_text(encoding="utf-8"))["segments"]}
        found = 0
        for m in re.finditer(r'\bW\("([\w]+)",\s*"([^"]+)"(?:,\s*(\d+))?\)', js):
            sid, word, nth = m.group(1), m.group(2), int(m.group(3) or 1)
            line = js.count("\n", 0, m.start()) + 1
            found += 1
            if sid not in seg:
                print(f"  {ep}.js:{line}  W({sid!r}, {word!r}): no segment {sid}")
                bad += 1
            elif seg[sid].count(norm(word)) < nth:
                print(f"  {ep}.js:{line}  W({sid!r}, {word!r}{', ' + str(nth) if nth > 1 else ''}): "
                      f"only {seg[sid].count(norm(word))}x in: {' '.join(seg[sid])[:90]}")
                bad += 1
        for m in re.finditer(r'\b(?:S0|S1|T)\("([\w]+)"\)', js):
            if m.group(1) not in seg:
                print(f"  {ep}.js:{js.count(chr(10), 0, m.start()) + 1}  {m.group(0)}: no segment {m.group(1)}")
                bad += 1
        print(f"{ep}: {found} word anchors checked")
    print(f"-> {bad} problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
