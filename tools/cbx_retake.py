"""Retakes for Chatterbox narration: Whisper listens to every line; a line that is heard too differently
from its text is narrated again with other seeds and the clearest take is kept.

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
import cbx  # noqa: E402
from dub_check import load16k, words  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MIN = {"en": 0.9, "hi": 0.6}  # Whisper writes Hindi's English terms in Devanagari, so Hindi scores low anyway


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

    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8")

    def score(mp3: Path, text: str) -> float:
        segs, _ = model.transcribe(load16k(mp3), language=lang, beam_size=5)
        return difflib.SequenceMatcher(None, words(text), words(" ".join(s.text for s in segs))).ratio()

    scores = {sid: score(out / f"{sid}.mp3", t) for sid, t in texts.items() if (out / f"{sid}.mp3").exists()}
    weak = [sid for sid, s in scores.items() if s < floor]
    print(f"{lang}: {len(scores)} lines, {len(weak)} below {floor}: {', '.join(weak)}", flush=True)
    if not weak:
        return
    tmp = out / "retakes"
    tmp.mkdir(exist_ok=True)
    jobs = [(texts[sid], tmp / f"{sid}_{seed}.mp3", seed) for sid in weak for seed in range(2, 2 + a.takes)]
    cbx.say(cfg, [j for j in jobs if not j[1].exists()])
    changed = []
    for sid in weak:
        best, best_s = None, scores[sid]
        for seed in range(2, 2 + a.takes):
            s = score(tmp / f"{sid}_{seed}.mp3", texts[sid])
            if s > best_s + 0.02:
                best, best_s = tmp / f"{sid}_{seed}.mp3", s
        print(f"  {sid}: {scores[sid]:.2f} -> {best_s:.2f}{'' if best else ' (kept)'}", flush=True)
        if best:
            shutil.copy(best, out / f"{sid}.mp3")
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
