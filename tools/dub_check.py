"""Pronunciation check for a dub: transcribe every narrated segment with Whisper
and compare it to the intended text. Segments that are not recognised as the
target language, or whose transcript differs a lot, are probably mispronounced.

Usage: python tools/dub_check.py video/ep01 tr [--model small]
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent


def load16k(path: Path) -> np.ndarray:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"])
    return np.frombuffer(raw, dtype=np.float32)


def words(s: str):
    s = s.lower().replace("’", "'")
    s = re.sub(r"'\w+", "", s)          # drop Turkish suffixes after apostrophes (ESP32'yi -> esp32)
    return re.findall(r"\w+", s)


def main(ep: Path, lang: str, model_name: str):
    dub = json.loads((ep / "dub" / f"{lang}.json").read_text(encoding="utf-8"))
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    bad = []
    for sid, text in dub["segments"].items():
        audio = load16k(ep / "build" / f"dub_{lang}" / f"{sid}.mp3")
        _, info = model.transcribe(audio, beam_size=1)
        segs, _ = model.transcribe(audio, language=lang, beam_size=5)
        heard = " ".join(s.text.strip() for s in segs)
        score = difflib.SequenceMatcher(None, words(text), words(heard)).ratio()
        ok = info.language == lang and score >= 0.72
        mark = "ok " if ok else "BAD"
        print(f"{mark} {sid} lang={info.language}({info.language_probability:.2f}) match={score:.2f}")
        if not ok:
            print(f"     want: {text}\n     heard: {heard}")
            bad.append(sid)
    print(f"\n{len(bad)} suspicious segment(s): {', '.join(bad)}")


if __name__ == "__main__":
    m = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "small"
    main((ROOT / sys.argv[1]).resolve(), sys.argv[2], m)
