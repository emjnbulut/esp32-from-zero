"""Find places in a dub where the voice sounds like another language.

Every narrated segment is cut into short overlapping windows and Whisper's
language identification runs on each one. A window that is not clearly the
target language is where a listener hears a "foreign voice".

Usage: python tools/dub_accent.py video/ep01 tr [--threshold 0.6]
"""
import json
import sys
from pathlib import Path

from faster_whisper import WhisperModel

sys.path.insert(0, str(Path(__file__).parent))
from dub_check import load16k  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WIN, HOP, SR = 2.5, 1.25, 16000


def main(ep: Path, lang: str, thr: float):
    dub = json.loads((ep / "dub" / f"{lang}.json").read_text(encoding="utf-8"))
    model = WhisperModel("small", device="cpu", compute_type="int8")
    bad = []
    for sid in dub["segments"]:
        audio = load16k(ep / "build" / f"dub_{lang}" / f"{sid}.mp3")
        worst = (1.0, 0.0, lang)
        t = 0.0
        while t + 1.0 < len(audio) / SR:
            win = audio[int(t * SR): int((t + WIN) * SR)]
            _, _, probs = model.detect_language(win)
            p = dict(probs).get(lang, 0.0)
            if p < worst[0]:
                worst = (p, t, probs[0][0])
            t += HOP
        flag = worst[0] < thr
        if flag:
            bad.append(sid)
        print(f"{'BAD' if flag else 'ok '} {sid} min {lang}={worst[0]:.2f} at {worst[1]:.1f}s (sounds like {worst[2]})")
    print(f"\n{len(bad)} segment(s) with a foreign-sounding part: {', '.join(bad)}")


if __name__ == "__main__":
    thr = float(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 0.6
    main((ROOT / sys.argv[1]).resolve(), sys.argv[2], thr)
