"""Narration pace check for every language of an episode (user 2026-10-28: rushed, jumpy narration).

Per language: syllables per voiced second (median, 10-90 %, max), lines above the language's pace limit
(cbx.MAX_SPS), stalls (silence inside a line longer than cbx_retake.MAX_GAP) and, for dubs, lines that would have to
be sped up more than dub.MAX_SPEEDUP to fit the current schedule (shorten those texts, or re-run build.py schedule).

Usage: python tools/pace_check.py video/recap1            # every language that has audio
       python tools/pace_check.py video/recap1 en tr      # only these
"""
import json
import statistics as st
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import cbx  # noqa: E402
from cbx_retake import MAX_GAP  # noqa: E402
from dub import BREATH, MAX_SPEEDUP  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def voiced(mp3: Path):
    """(voiced seconds, longest inner silence, total seconds) of a narrated line."""
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(mp3), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"])
    a = np.frombuffer(raw, np.float32)
    hop = 320  # 20 ms
    fr = a[: len(a) // hop * hop].reshape(-1, hop)
    db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
    v = np.where(db > db.max() - 38)[0]
    gap = float(np.diff(v).max() - 1) * 0.02 if len(v) > 1 else 0.0
    return max(len(v) * 0.02, 0.1), gap, len(a) / 16000


def lines(ep: Path, lang: str):
    if lang == "en":
        sc = json.loads((ep / "script.json").read_text(encoding="utf-8"))["segments"]
        return {s["id"]: s["text"] for s in sc}, ep / "build" / "audio"
    dub = json.loads((ep / "dub" / f"{lang}.json").read_text(encoding="utf-8"))
    return dub["segments"], ep / "build" / f"dub_{lang}"


def main():
    ep = (ROOT / sys.argv[1]).resolve()
    langs = sys.argv[2:] or ["en"] + sorted(p.stem for p in (ep / "dub").glob("*.json") if (ep / "build" / f"dub_{p.stem}").exists())
    sched_p = ep / "build" / "schedule.json"
    room = {}
    if sched_p.exists():
        sg = json.loads(sched_p.read_text(encoding="utf-8"))
        ids = list(sg["segments"])
        for i, sid in enumerate(ids):
            end = sg["segments"][ids[i + 1]]["start"] if i + 1 < len(ids) else sg["duration"] - 1.5
            room[sid] = end - sg["segments"][sid]["start"] - BREATH
    bad = 0
    for lang in langs:
        texts, d = lines(ep, lang)
        limit = cbx.MAX_SPS.get(lang)
        rows = []
        for sid, text in texts.items():
            mp3 = d / f"{sid}.mp3"
            if mp3.exists():
                talk, gap, total = voiced(mp3)
                rows.append((sid, cbx.syllables(text) / talk, gap, total))
        if not rows:
            print(f"{lang}: no audio")
            continue
        sps = [r[1] for r in rows]
        q = st.quantiles(sps, n=10) if len(sps) > 2 else [min(sps), max(sps)]
        fast = [(sid, s) for sid, s, _, _ in rows if limit and s > limit * 1.05]
        stalls = [(sid, g) for sid, _, g, _ in rows if g > MAX_GAP]
        tight = [(sid, t / room[sid]) for sid, _, _, t in rows if lang != "en" and sid in room and t / room[sid] > MAX_SPEEDUP]
        print(f"{lang}: {len(rows)} lines, {st.median(sps):.2f} syl/s median (10-90 % {q[0]:.2f}-{q[-1]:.2f}, max {max(sps):.2f}),"
              f" limit {limit}")
        for sid, s in fast:
            print(f"   FAST    {sid}: {s:.2f} syl/s")
        for sid, g in stalls:
            print(f"   STALL   {sid}: {g:.2f} s silence inside the line")
        for sid, r in tight:
            print(f"   TIGHT   {sid}: needs x{r:.2f} to fit its slot (shorten the text or re-run build.py schedule)")
        bad += len(fast) + len(stalls) + len(tight)
    print(f"-> {bad} warnings")


if __name__ == "__main__":
    main()
