"""Pick the best-pronounced wording for problem segments of a dub.

Each candidate is narrated, transcribed with Whisper (forced to the target
language), scored against its own text, and the best one that still fits the
time slot is written back to <episode>/dub/<lang>.json.

Usage: python tools/dub_pick.py video/ep01 tr candidates.json
candidates.json: {"s01": ["variant A", "variant B", ...], ...}  (current text is always included)
"""
import asyncio
import difflib
import json
import sys
from pathlib import Path

import edge_tts
from faster_whisper import WhisperModel

sys.path.insert(0, str(Path(__file__).parent))
from dub import MAX_SPEEDUP, probe, slots  # noqa: E402
from dub_check import load16k, words  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


async def say(text, voice, rate, path):
    for _ in range(3):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(str(path))
            return True
        except edge_tts.exceptions.NoAudioReceived:
            await asyncio.sleep(3)
    return False


def main(ep: Path, lang: str, cand_file: Path):
    p = ep / "dub" / f"{lang}.json"
    dub = json.loads(p.read_text(encoding="utf-8"))
    cands = json.loads(cand_file.read_text(encoding="utf-8"))
    sched = json.loads((ep / "build" / "schedule.json").read_text(encoding="utf-8"))
    room = {k: v[1] for k, v in slots(sched).items()}
    model = WhisperModel("small", device="cpu", compute_type="int8")
    tmp = ep / "build" / f"dub_{lang}_pick"
    tmp.mkdir(parents=True, exist_ok=True)
    for sid, variants in cands.items():
        best = None
        for i, text in enumerate([dub["segments"][sid]] + variants):
            mp3 = tmp / f"{sid}_{i}.mp3"
            if not asyncio.run(say(text, dub["voice"], dub.get("rate", "+0%"), mp3)):
                continue
            fit = probe(mp3) / room[sid]
            audio = load16k(mp3)
            _, info = model.transcribe(audio, beam_size=1)
            segs, _ = model.transcribe(audio, language=lang, beam_size=5)
            heard = " ".join(s.text.strip() for s in segs)
            score = difflib.SequenceMatcher(None, words(text), words(heard)).ratio()
            score -= 0.15 if info.language != lang else 0
            ok_fit = fit <= MAX_SPEEDUP
            print(f"{sid}[{i}] score={score:.2f} lang={info.language} fit=x{fit:.2f}{'' if ok_fit else ' (too long)'}\n   heard: {heard}")
            if ok_fit and (best is None or score > best[0]):
                best = (score, text)
        if best:
            dub["segments"][sid] = best[1]
            print(f"=> {sid}: {best[1]}\n")
    p.write_text(json.dumps(dub, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main((ROOT / sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]))
