"""Build the channel trailer (16:9) from video/trailer/trailer.json.

Usage: python tools/trailer.py            -> video/trailer/build/trailer_en.mp4 (+ trailer_en.srt)

Each segment is narrated (edge-tts, or Chatterbox with "engine": "chatterbox" + "cbx"), then shows
moments of the rendered episodes ("shots": {"ep", "at": [segment, word, offset]} or {"ep", "src"},
optional "crop": [x, y, w, h]) or a full-screen card drawn by the overlay page ("card": "topics" | "end").
Text (lower thirds, cards) comes from video/trailer/trailer.html, rendered with a transparent background.
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
import cbx  # noqa: E402
import music  # noqa: E402
from short import decode, probe, run, word_time  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TDIR = ROOT / "video" / "trailer"
SR, FPS = 48000, 30
LEAD, GAP, TAIL = 0.5, 0.45, 2.5


def narrate(spec, out):
    """One mp3 per segment, cached by text + voice settings."""
    cache_p = out / "cache.json"
    cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}
    chatterbox = cbx.engine(spec) == "chatterbox"
    cfg = cbx.settings(spec, "en") if chatterbox else {"voice": spec["voice"], "rate": spec.get("rate", "+0%")}
    todo = []
    for s in spec["segments"]:
        k = hashlib.sha1(json.dumps([cfg, s["say"]], sort_keys=True).encode()).hexdigest()
        if cache.get(s["id"]) != k or not (out / f"{s['id']}.mp3").exists():
            todo.append(s)
            cache[s["id"]] = k
    if chatterbox:
        cbx.say(cfg, [(s["say"], out / f"{s['id']}.mp3") for s in todo])
    else:
        for s in todo:
            asyncio.run(edge_tts.Communicate(s["say"], cfg["voice"], rate=cfg["rate"]).save(str(out / f"{s['id']}.mp3")))
    cache_p.write_text(json.dumps(cache, indent=1), encoding="utf-8")


def shot_src(sh):
    if "src" in sh:
        return sh["src"]
    segs = json.loads((ROOT / "video" / sh["ep"] / "build" / "schedule.json").read_text(encoding="utf-8"))["segments"]
    sid, word, off = (sh["at"] + [0])[:3]
    return segs[sid]["start"] + (word_time(segs[sid], word) if word is not None else 0) + off


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    spec = json.loads((TDIR / "trailer.json").read_text(encoding="utf-8"))
    out = TDIR / "build"
    out.mkdir(parents=True, exist_ok=True)
    narrate(spec, out)

    # 1. timing
    t, sched = LEAD, {}
    for s in spec["segments"]:
        d = probe(out / f"{s['id']}.mp3")
        sched[s["id"]] = {"start": round(t, 3), "end": round(t + d, 3), "words": []}
        t += d + GAP
    duration = round(t - GAP + TAIL, 3)
    ids = [s["id"] for s in spec["segments"]]
    data = {"schedule": {"duration": duration, "segments": sched},
            "segs": [{k: s.get(k) for k in ("id", "kicker", "headline", "card")} for s in spec["segments"]]}
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"trailer: {duration:.1f}s")

    # 2. overlay (text, cards)
    run(["node", "engine/render.mjs", "trailer", "--page", str(TDIR / "trailer.html"), "--data", str(out / "data.json"),
         "--size", "1920x1080", "--alpha", "--out", str(out / "overlay.mov")], cwd=ROOT / "video")

    # 3. footage: shots cut from the episodes (cards get a plain background, the overlay covers them)
    inputs, filters, labels = [], [], []
    for i, s in enumerate(spec["segments"]):
        a = 0 if i == 0 else sched[s["id"]]["start"] - 0.2
        b = sched[ids[i + 1]]["start"] - 0.2 if i + 1 < len(ids) else duration
        shots = s.get("shots") or [None]
        for sh in shots:
            d = (b - a) / len(shots)
            k = len(labels)
            if sh is None:
                inputs += ["-f", "lavfi", "-t", f"{d:.3f}", "-i", f"color=c=0x0b1220:s=1920x1080:r={FPS}"]
                filters.append(f"[{k}:v]setsar=1[s{k}]")
            else:
                src = ROOT / "video" / sh["ep"] / "build" / "video.mp4"
                inputs += ["-ss", f"{shot_src(sh):.3f}", "-t", f"{d + 0.5:.3f}", "-i", str(src)]
                x, y, w, h = sh.get("crop", [0, 0, 1920, 1080])
                # a slow push-in keeps still scenes alive
                filters.append(f"[{k}:v]fps={FPS},crop={w}:{h}:{x}:{y},scale=2112:1188,"
                               f"crop=1920:1080:'96*(1-t/{d:.3f})':'54*(1-t/{d:.3f})',"
                               f"trim=duration={d:.3f},setpts=PTS-STARTPTS,setsar=1[s{k}]")
            labels.append(f"[s{k}]")
    filters.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[v]")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[v]",
         "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(out / "footage.mp4")])

    # 4. audio: narration + music
    buf = np.zeros(int((duration + 1) * SR), dtype=np.float32)
    for sid in ids:
        a = decode(out / f"{sid}.mp3")
        i = int(sched[sid]["start"] * SR)
        buf[i:i + len(a)] += a[: len(buf) - i]
    buf = music.mix(buf, SR, decode, level=0.12, fade_in=0.5, fade_out=2.0)
    buf = buf / (np.max(np.abs(buf)) or 1) * 0.9
    run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(out / "audio.wav")],
        input=(buf * 32767).astype(np.int16).tobytes())

    # 5. compose + subtitles
    final = out / "trailer_en.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(out / "footage.mp4"), "-i", str(out / "overlay.mov"), "-i", str(out / "audio.wav"),
         "-filter_complex", "[0:v][1:v]overlay=0:0[v]", "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(duration),
         "-movflags", "+faststart", str(final)])
    srt = "\n".join(f"{n}\n{srt_time(sched[s['id']]['start'])} --> {srt_time(sched[s['id']]['end'])}\n{s['say']}\n"
                    for n, s in enumerate(spec["segments"], 1))
    (out / "trailer_en.srt").write_text(srt, encoding="utf-8")
    print("trailer:", final)


if __name__ == "__main__":
    main()
