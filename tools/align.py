"""Word timings for narration that comes without them (e.g. Chatterbox).

The words are the script's own words (so W("s10", "D") in the scenes keeps working);
faster-whisper only supplies the times. Script words whisper heard differently
("220" vs "two hundred twenty") are placed by interpolating between matched neighbours.

Usage (check against edge-tts timings that are already there):
  python tools/align.py video/ep03
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
_model = None


def model():
    global _model
    if _model is None:
        sys.path.insert(0, str(Path(__file__).parent))
        import whisper_dev
        _model = whisper_dev.model("small")
    return _model


def load16k(path: Path) -> np.ndarray:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"])
    return np.frombuffer(raw, dtype=np.float32)


def norm(w: str) -> str:
    return re.sub(r"[\W_]", "", w.lower())  # any script (Turkish, Devanagari), not only a-z


def script_words(text: str) -> list:
    """Split like edge-tts does: on spaces, outer punctuation dropped."""
    words = [re.sub(r"^[^\w']+|[^\w']+$", "", w) for w in text.split()]
    return [w for w in words if w]


def align(audio: Path, text: str, lang: str = "en") -> list:
    words = script_words(text)
    segs, _ = model().transcribe(load16k(audio), language=lang, word_timestamps=True, initial_prompt=text)
    heard = [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]
    times = [None] * len(words)
    sm = difflib.SequenceMatcher(None, [norm(w) for w in words], [h[0] for h in heard], autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            times[a + k] = heard[b + k][1]
    # interpolate the unmatched words between known neighbours (by character count)
    end = heard[-1][2] if heard else 0.0
    known = [(-1, 0.0)] + [(i, t) for i, t in enumerate(times) if t is not None] + [(len(words), end)]
    for (i0, t0), (i1, t1) in zip(known, known[1:]):
        gap = words[i0 + 1:i1]
        total = sum(len(w) for w in gap) + 1
        acc = 0
        for k, w in enumerate(gap):
            times[i0 + 1 + k] = t0 + (t1 - t0) * acc / total
            acc += len(w)
    return [{"w": w, "t": round(t, 3)} for w, t in zip(words, times)]


def check(ep: Path):
    script = json.loads((ep / "script.json").read_text(encoding="utf-8"))
    timings = json.loads((ep / "build" / "audio" / "timings.json").read_text(encoding="utf-8"))
    errs = []
    for seg in script["segments"]:
        ref = timings[seg["id"]]["words"]
        got = align(ep / "build" / "audio" / f"{seg['id']}.mp3", seg["text"])
        if [norm(w["w"]) for w in ref] != [norm(w["w"]) for w in got]:
            print(f"{seg['id']}: word lists differ\n  edge: {[w['w'] for w in ref]}\n  ours: {[w['w'] for w in got]}")
            continue
        e = [abs(r["t"] - g["t"]) for r, g in zip(ref, got)]
        errs += e
        print(f"{seg['id']}: mean {sum(e) / len(e):.3f}s  max {max(e):.3f}s")
    errs.sort()
    print(f"all words: mean {sum(errs) / len(errs):.3f}s  p95 {errs[int(len(errs) * 0.95)]:.3f}s  max {errs[-1]:.3f}s")


if __name__ == "__main__":
    check((ROOT / sys.argv[1]).resolve())
