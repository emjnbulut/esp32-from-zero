"""Dub an episode into another language as an extra audio track.

The picture stays the same: each translated segment is narrated and fitted into
the time slot of the original English segment (sped up a little if needed).

Usage:
  python tools/dub.py video/ep01 tr            # build/dub_tr.wav, .m4a and ep01_tr_dub.mp4
  python tools/dub.py video/ep01 tr --report   # only narrate + show how well each segment fits

Translations live in <episode>/dub/<lang>.json:
  {"voice": "tr-TR-AhmetNeural", "rate": "+0%", "segments": {"s01": "...", ...}}
"""
import asyncio
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import edge_tts
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import music  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
MAX_SPEEDUP = 1.18   # beyond this the translation should be shortened
BREATH = 0.2         # silence kept before the next segment starts


def probe(path: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(path)]).strip())


def decode(path: Path, tempo: float = 1.0) -> np.ndarray:
    af = ["-af", f"atempo={tempo:.4f}"] if tempo > 1.001 else []
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), *af, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32)


async def narrate_all(dub: dict, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    cache_p = out / "cache.json"
    cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}
    voice, rate = dub["voice"], dub.get("rate", "+0%")
    for sid, text in dub["segments"].items():
        key = hashlib.sha1(f"{voice}|{rate}|{text}".encode()).hexdigest()
        mp3 = out / f"{sid}.mp3"
        if cache.get(sid, {}).get("key") == key and mp3.exists():
            continue
        for attempt in range(10):
            try:
                await edge_tts.Communicate(text, voice, rate=rate).save(str(mp3))
                break
            except edge_tts.exceptions.NoAudioReceived:
                if attempt == 9:
                    raise RuntimeError(f"{sid}: no audio for text: {text}")
                await asyncio.sleep(15)
        cache[sid] = {"key": key, "duration": probe(mp3)}
        cache_p.write_text(json.dumps(cache, indent=1), encoding="utf-8")
    return cache


def slots(sched: dict):
    """Available time for each segment: until the next segment starts."""
    ids = list(sched["segments"])
    res = {}
    for i, sid in enumerate(ids):
        s = sched["segments"][sid]
        end = sched["segments"][ids[i + 1]]["start"] if i + 1 < len(ids) else sched["duration"] - 1.5
        res[sid] = (s["start"], end - s["start"] - BREATH)
    return res


def main(ep: Path, lang: str, report_only: bool):
    dub = json.loads((ep / "dub" / f"{lang}.json").read_text(encoding="utf-8"))
    sched = json.loads((ep / "build" / "schedule.json").read_text(encoding="utf-8"))
    missing = [s for s in sched["segments"] if s not in dub["segments"]]
    if missing:
        sys.exit(f"missing translations: {missing}")
    out = ep / "build" / f"dub_{lang}"
    cache = asyncio.run(narrate_all(dub, out))

    sl = slots(sched)
    too_long = []
    for sid, (start, room) in sl.items():
        d = cache[sid]["duration"]
        ratio = d / room
        flag = "  <-- shorten" if ratio > MAX_SPEEDUP else ""
        if ratio > MAX_SPEEDUP:
            too_long.append(sid)
        if report_only or flag:
            print(f"{sid}: {d:5.2f}s in {room:5.2f}s  x{max(1, ratio):.2f}{flag}")
    if report_only:
        print(f"{len(too_long)} segment(s) need shortening")
        return

    buf = np.zeros(int((sched["duration"] + 1) * SR), dtype=np.float32)
    for sid, (start, room) in sl.items():
        d = cache[sid]["duration"]
        a = decode(out / f"{sid}.mp3", tempo=max(1.0, d / room))
        i = int(start * SR)
        buf[i:i + len(a)] += a[: len(buf) - i]
    buf = music.mix(buf, SR, decode, level=0.10)
    buf = buf / (np.max(np.abs(buf)) or 1) * 0.89
    wav = ep / "build" / f"dub_{lang}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(wav)],
                   input=(buf * 32767).astype(np.int16).tobytes(), check=True)
    m4a = wav.with_suffix(".m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "192k", str(m4a)], check=True)
    final = ep / "build" / f"{ep.name}_final.mp4"
    if final.exists():
        mp4 = ep / "build" / f"{ep.name}_{lang}_dub.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(final), "-i", str(m4a), "-map", "0:v", "-map", "1:a",
                        "-c", "copy", "-movflags", "+faststart", str(mp4)], check=True)
        print("video:", mp4)
    print("audio track:", m4a)
    if too_long:
        print("warning: sped up more than", MAX_SPEEDUP, "->", ", ".join(too_long))


if __name__ == "__main__":
    main((ROOT / sys.argv[1]).resolve(), sys.argv[2], "--report" in sys.argv)
