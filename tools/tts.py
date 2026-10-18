"""Narrate an episode script with edge-tts, or Chatterbox when script.json has "engine": "chatterbox"
(settings in tools/cbx.py; word timings then come from tools/align.py).

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

sys.path.insert(0, str(Path(__file__).parent))
import cbx  # noqa: E402


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

    if cbx.engine(script) == "chatterbox":
        return chatterbox(script, out, timings_path, old)
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

    save(timings, timings_path)


def chatterbox(script, out, timings_path, old):
    import align
    cfg = cbx.settings(script, "en")
    keys = {seg["id"]: cbx.key(cfg, seg["text"]) for seg in script["segments"]}
    todo = [seg for seg in script["segments"]
            if not (seg["id"] in old and old[seg["id"]]["key"] == keys[seg["id"]] and (out / f"{seg['id']}.mp3").exists())]
    cbx.say(cfg, [(seg["text"], out / f"{seg['id']}.mp3") for seg in todo])
    timings = {}
    for seg in script["segments"]:
        sid, mp3 = seg["id"], out / f"{seg['id']}.mp3"
        if seg in todo:
            timings[sid] = {"key": keys[sid], "duration": probe_duration(mp3), "words": align.align(mp3, seg["text"])}
            print(f"{sid}: {timings[sid]['duration']:.2f}s")
        else:
            timings[sid] = old[sid]
    save(timings, timings_path)


def save(timings, timings_path):
    timings_path.write_text(json.dumps(timings, indent=1), encoding="utf-8")
    total = sum(t["duration"] for t in timings.values())
    print(f"total narration: {total:.1f}s")


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1])))
