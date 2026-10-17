"""Rewrite the chapter timestamps in <episode>/localize.json from the narration schedule.

<episode>/chapters.json lists the first segment of every chapter, e.g. ["s01", "s04", "s07"].
Run it after the narration changes (new voice, edited lines):  python tools/rechapter.py video/ep01
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTRO = 3.5  # the channel intro (tools/bumpers.py) plays before the episode


def chapter_times(ep: Path) -> list:
    ids = json.loads((ep / "chapters.json").read_text(encoding="utf-8"))
    segs = json.loads((ep / "build" / "schedule.json").read_text(encoding="utf-8"))["segments"]
    starts = [0] + [int(segs[c]["start"] + INTRO) for c in ids[1:]]
    assert all(b - a >= 10 for a, b in zip(starts, starts[1:])), "YouTube chapters must be at least 10 s"
    return ["%d:%02d" % divmod(s, 60) for s in starts]


def main(ep: Path):
    times = chapter_times(ep)
    p = ep / "localize.json"
    loc = json.loads(p.read_text(encoding="utf-8"))
    for lang, v in loc.items():
        it = iter(times)
        v["description"], n = re.subn(r"^\d+:\d\d(?= )", lambda m: next(it), v["description"], flags=re.M)
        assert n == len(times), (lang, n, len(times))
    p.write_text(json.dumps(loc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(ep.name, " ".join(times))


if __name__ == "__main__":
    main((ROOT / sys.argv[1]).resolve())
