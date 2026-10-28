"""Retakes for Chatterbox narration: Whisper listens to every line; a line that is heard too differently
from its text, has a long pause inside, or is much faster/slower than the rest is narrated again with
other seeds, and the most fluent, clearest take is kept.

Usage:
  python tools/cbx_retake.py video/ep03 en        # build/audio (script.json), updates timings.json
  python tools/cbx_retake.py video/ep03 tr        # build/dub_tr (dub/tr.json), updates cache.json
  python tools/cbx_retake.py video/shorts/ep03 tr --short   # build/<lang>/ of a Short (cbx_cache.json)
Options: --min 0.85 (score that needs no retake), --takes 4 (extra seeds to try)
Run it right after tts.py / dub.py --report and before build.py schedule.
"""
import argparse
import difflib
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np  # noqa: E402

import cbx  # noqa: E402
from dub_check import load16k, words  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MAX_GAP = 1.15  # seconds of silence inside a line (a question pause is 0.8 + trims; more is a stumble)
MAX_JUNK = 0.25  # seconds of sound away from every recognised word (Chatterbox mumbles/noise after a chunk)
MIN = {"en": 0.9, "hi": 0.0}  # Hindi: Whisper writes the English terms in Devanagari, so only fluency is checked


def probe(path: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(path)]).strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("lang")
    ap.add_argument("--short", action="store_true")
    ap.add_argument("--min", type=float)
    ap.add_argument("--takes", type=int, default=4)
    a = ap.parse_args()
    ep, lang = (ROOT / a.ep).resolve(), a.lang
    floor = a.min if a.min is not None else MIN.get(lang, 0.8)

    if a.short:
        spec = json.loads((ep / "short.json").read_text(encoding="utf-8"))
        texts = {s["id"]: s["say"][lang] for s in spec["shots"] if s.get("say", {}).get(lang)} \
            if "shots" in spec else {s["id"]: s["say"][lang] for s in spec["segments"] if s.get("say", {}).get(lang)}
        out, cfg = ep / "build" / lang, cbx.settings(spec, lang)
    elif lang == "en":
        spec = json.loads((ep / "script.json").read_text(encoding="utf-8"))
        texts = {s["id"]: s["text"] for s in spec["segments"]}
        out, cfg = ep / "build" / "audio", cbx.settings(spec, "en")
    else:
        spec = json.loads((ep / "dub" / f"{lang}.json").read_text(encoding="utf-8"))
        texts = spec["segments"]
        out, cfg = ep / "build" / f"dub_{lang}", cbx.settings(spec, lang)

    import whisper_dev
    model = whisper_dev.model("small")

    def check(mp3: Path, text: str) -> dict:
        """Whisper match + fluency: the longest pause inside the line, the speaking rate and stray sounds."""
        audio = load16k(mp3)
        segs, _ = model.transcribe(audio, language=lang, beam_size=5, word_timestamps=True)
        segs = list(segs)
        # letters, not words: "C P 2 1 0 2" in the script and "CP2102" from Whisper are the same
        match = difflib.SequenceMatcher(None, "".join(words(text)), "".join(words(" ".join(s.text for s in segs))),
                                        autojunk=False).ratio()
        hop = 320  # 20 ms
        fr = audio[: len(audio) // hop * hop].reshape(-1, hop)
        db = 10 * np.log10((fr ** 2).mean(1) + 1e-12)
        voiced = np.where(db > db.max() - 38)[0]
        gap, speech = 0.0, len(audio) / 16000
        if len(voiced):
            speech = (voiced[-1] - voiced[0] + 1) * 0.02
            gap = float(np.diff(voiced).max() - 1) * 0.02 if len(voiced) > 1 else 0.0
        talk = max(len(voiced) * 0.02, 0.1)  # voiced time only, so lines with many pauses don't look slow
        near = np.zeros(len(db), bool)  # frames within 0.3 s of a recognised word
        for w in (w for sg in segs for w in (sg.words or [])):
            near[max(0, int((w.start - 0.3) / 0.02)):int((w.end + 0.3) / 0.02) + 1] = True
        junk = float(((db > db.max() - 30) & ~near).sum()) * 0.02
        return {"match": match, "gap": gap, "rate": len(text) / talk, "junk": junk, "dur": len(audio) / 16000}

    res = {sid: {**check(out / f"{sid}.mp3", t), "sid": sid} for sid, t in texts.items() if (out / f"{sid}.mp3").exists()}
    med = float(np.median([r["rate"] for r in res.values()]))

    def problems(r):
        p = []
        if r["match"] < floor:
            p.append(f"match {r['match']:.2f}")
        if r["gap"] > MAX_GAP:
            p.append(f"pause {r['gap']:.1f}s")
        if r.get("junk", 0) > MAX_JUNK:
            p.append(f"stray sound {r['junk']:.1f}s")
        # a line much faster/slower than the rest makes the rhythm jump (user 2026-10-28: "karman çorman");
        # the band was 0.75-1.3 before, retakes are cheaper than time-stretching (which sounded robotic)
        if not 0.85 * med < r["rate"] < 1.18 * med:
            p.append(f"rate x{r['rate'] / med:.2f}")
        return p

    room = {}  # dub lines: time until the next line in the current schedule; takes that fit are preferred
    sched_p = ep / "build" / "schedule.json"
    if not a.short and lang != "en" and sched_p.exists():
        sg = json.loads(sched_p.read_text(encoding="utf-8"))["segments"]
        ids = list(sg)
        room = {sid: sg[ids[i + 1]]["start"] - sg[sid]["start"] - 0.2 for i, sid in enumerate(ids[:-1])}

    def rank(r):  # fluent takes first, then takes that fit their slot, then the clearest
        return (len(problems(r)) == 0, r.get("dur", 0) <= 1.03 * room.get(r.get("sid"), 1e9), r["match"] - 0.1 * max(0, r["gap"] - MAX_GAP) - 0.2 * r.get("junk", 0))

    weak = {sid: problems(r) for sid, r in res.items() if problems(r)}
    print(f"{lang}: {len(res)} lines, median {med:.1f} chars/s, {len(weak)} to retake", flush=True)
    for sid, p in weak.items():
        print(f"  {sid}: {', '.join(p)}", flush=True)
    if not weak:
        return
    tmp = out / "retakes"
    # the name carries the voice settings + text, so takes of an older voice or text are never reused
    take = lambda sid, seed: tmp / f"{sid}_{seed}_{cbx.key(cfg, texts[sid])[:8]}.mp3"
    tmp.mkdir(exist_ok=True)
    best = {sid: (None, res[sid]) for sid in weak}
    open_ = list(weak)  # one seed per round; a line leaves as soon as a take has no problems
    for seed in range(2, 2 + a.takes):
        if not open_:
            break
        cbx.say(cfg, [(texts[sid], take(sid, seed), seed) for sid in open_ if not take(sid, seed).exists()])
        for sid in list(open_):
            r = {**check(take(sid, seed), texts[sid]), "sid": sid}
            b = best[sid][1]
            if rank(r) > rank(b) and (len(problems(b)) > 0 or r["match"] > b["match"] + 0.02):
                best[sid] = (take(sid, seed), r)
            if not problems(best[sid][1]):
                open_.remove(sid)
    changed = []
    for sid in weak:
        path, r = best[sid]
        left = problems(r)
        print(f"  {sid}: {'took seed ' + path.stem.split('_')[1] if path else 'kept'}"
              f"{' - still ' + ', '.join(left) if left else ' - ok'}", flush=True)
        if path:
            shutil.copy(path, out / f"{sid}.mp3")
            changed.append(sid)
    if not changed:
        return
    # keep the caches pointing at the swapped files (same key, new duration / word times)
    import align
    if a.short:
        cp = out / "cbx_cache.json"
        cache = json.loads(cp.read_text(encoding="utf-8"))
        for sid in changed:
            cache[sid]["words"] = [w["t"] for w in align.align(out / f"{sid}.mp3", texts[sid], lang)]
        cp.write_text(json.dumps(cache, indent=1), encoding="utf-8")
    elif lang == "en":
        tp = out / "timings.json"
        tim = json.loads(tp.read_text(encoding="utf-8"))
        for sid in changed:
            tim[sid]["duration"] = probe(out / f"{sid}.mp3")
            tim[sid]["words"] = align.align(out / f"{sid}.mp3", texts[sid])
        tp.write_text(json.dumps(tim, indent=1), encoding="utf-8")
    else:
        cp = out / "cache.json"
        cache = json.loads(cp.read_text(encoding="utf-8"))
        for sid in changed:
            cache[sid]["duration"] = probe(out / f"{sid}.mp3")
        cp.write_text(json.dumps(cache, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
