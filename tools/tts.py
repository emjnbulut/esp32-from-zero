"""Narrate an episode script with edge-tts.

Usage: python tools/tts.py video/ep01

Writes to <episode>/build/audio/:
  <id>.mp3          one file per segment
  timings.json      per-segment duration and word timings (seconds)
Already generated segments are reused unless their text changed.
"""
import asyncio
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import edge_tts


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
    )
    return float(out.strip())


async def narrate(text: str, voice: str, rate: str, mp3: Path):
    words = []
    comm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    with open(mp3, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append({
                    "w": chunk["text"],
                    "t": chunk["offset"] / 1e7,
                    "d": chunk["duration"] / 1e7,
                })
    return words


async def main(ep_dir: Path):
    script = json.loads((ep_dir / "script.json").read_text(encoding="utf-8"))
    out = ep_dir / "build" / "audio"
    out.mkdir(parents=True, exist_ok=True)
    timings_path = out / "timings.json"
    old = json.loads(timings_path.read_text(encoding="utf-8")) if timings_path.exists() else {}

    voice, rate = script["voice"], script.get("rate", "+0%")
    timings = {}
    for seg in script["segments"]:
        sid, text = seg["id"], seg["text"]
        key = hashlib.sha1(f"{voice}|{rate}|{text}".encode()).hexdigest()
        mp3 = out / f"{sid}.mp3"
        if sid in old and old[sid]["key"] == key and mp3.exists():
            timings[sid] = old[sid]
            continue
        words = await narrate(text, voice, rate, mp3)
        timings[sid] = {"key": key, "duration": probe_duration(mp3), "words": words}
        print(f"{sid}: {timings[sid]['duration']:.2f}s")

    timings_path.write_text(json.dumps(timings, indent=1), encoding="utf-8")
    total = sum(t["duration"] for t in timings.values())
    print(f"total narration: {total:.1f}s")


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1])))
