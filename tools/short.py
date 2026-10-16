"""Build a vertical summary Short for an episode, in one language.

Usage: python tools/short.py video/shorts/ep01 en
Output: video/shorts/ep01/build/<lang>/<episode>_short_<lang>.mp4

short.json lists narration segments; each has text per language ("say" is spoken,
"show" is the on-screen caption), a headline, and shots: moments of the rendered
episode video ("src" seconds, optional "speed") cropped to a region [x, y, w, h].
"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

import edge_tts
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
FPS = 30
PANEL = {"x": 70, "y": 380, "w": 940, "h": 940}
LEAD, GAP, TAIL = 0.35, 0.3, 2.4
VOICES = {"en": ("en-US-EricNeural", "+5%"), "tr": ("de-DE-FlorianMultilingualNeural", "+0%"),
          "hi": ("hi-IN-MadhurNeural", "+0%"), "pt": ("pt-BR-AntonioNeural", "+0%")}


def run(cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


def probe(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


async def narrate(text, voice, rate, mp3):
    words = []
    for attempt in range(4):
        try:
            words = []
            with open(mp3, "wb") as f:
                async for ch in edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary").stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        words.append(ch["offset"] / 1e7)
            return words
        except edge_tts.exceptions.NoAudioReceived:
            if attempt == 3:
                raise
            await asyncio.sleep(5)


def decode(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32)


def main(sdir: Path, lang: str):
    spec = json.loads((sdir / "short.json").read_text(encoding="utf-8"))
    out = sdir / "build" / lang
    out.mkdir(parents=True, exist_ok=True)
    voice, rate = VOICES[lang]

    # 1. narration + timing
    t, sched = LEAD, {}
    for s in spec["segments"]:
        mp3 = out / f"{s['id']}.mp3"
        spoken = asyncio.run(narrate(s["say"][lang], voice, rate, mp3))
        dur = probe(mp3)
        shown = s["show"][lang].split()
        # map on-screen words onto spoken word times (they can differ, e.g. "C P 2102" vs "CP2102")
        words = [{"w": w, "t": round(t + spoken[min(len(spoken) - 1, int(j * len(spoken) / len(shown)))], 3)}
                 for j, w in enumerate(shown)] if spoken else []
        sched[s["id"]] = {"start": round(t, 3), "end": round(t + dur, 3), "words": words}
        t += dur + GAP
    duration = round(t - GAP + TAIL, 3)
    ids = [s["id"] for s in spec["segments"]]
    data = {"schedule": {"duration": duration, "segments": sched}, "panel": PANEL, "lang": lang,
            "segs": [{"id": s["id"], "chip": s["chip"], "headline": s["headline"][lang]} for s in spec["segments"]],
            "cta": {"title": spec["cta"][lang], "sub": spec["cta"].get("sub", "")}}
    data_txt = json.dumps(data, ensure_ascii=False, indent=1)
    same = (out / "data.json").exists() and (out / "data.json").read_text(encoding="utf-8") == data_txt
    (out / "data.json").write_text(data_txt, encoding="utf-8")
    print(f"{lang}: {duration:.1f}s")

    # 2. overlay layer (transparent) - only re-rendered when text or timing changed
    if not (same and (out / "overlay.mov").exists()):
        run(["node", "engine/render.mjs", "shorts/" + sdir.name, "--page", str(ROOT / "video" / "shorts" / "short.html"),
             "--data", str(out / "data.json"), "--size", "1080x1920", "--alpha", "--out", str(out / "overlay.mov")],
            cwd=ROOT / "video")

    # 3. panel: shots cut from the rendered episode, fitted into the panel
    src = ROOT / spec["source"]
    inputs, filters, labels = [], [], []
    for i, s in enumerate(spec["segments"]):
        a = 0 if i == 0 else sched[s["id"]]["start"]
        b = sched[ids[i + 1]]["start"] if i + 1 < len(ids) else duration
        n = len(s["shots"])
        for j, sh in enumerate(s["shots"]):
            d = (b - a) / n
            sp = sh.get("speed", 1.0)
            k = len(labels)
            inputs += ["-ss", f"{sh['src']:.3f}", "-t", f"{d * sp + 0.5:.3f}", "-i", str(src)]
            x, y, w, h = sh["crop"]
            filters.append(f"[{k}:v]setpts=(PTS-STARTPTS)/{sp},fps={FPS},crop={w}:{h}:{x}:{y},"
                           f"scale={PANEL['w']}:{PANEL['h']}:force_original_aspect_ratio=decrease:flags=lanczos,"
                           f"pad={PANEL['w']}:{PANEL['h']}:(ow-iw)/2:(oh-ih)/2:color=0x0b1220,"
                           f"trim=duration={d:.3f},setpts=PTS-STARTPTS,setsar=1[s{k}]")
            labels.append(f"[s{k}]")
    filters.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[panel]")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[panel]",
         "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(out / "panel.mp4")])

    # 4. audio: narration + music bed
    buf = np.zeros(int((duration + 1) * SR), dtype=np.float32)
    for sid in ids:
        a = decode(out / f"{sid}.mp3")
        i = int(sched[sid]["start"] * SR)
        buf[i:i + len(a)] += a
    music = ROOT / "video" / "assets" / "music.wav"
    if music.exists():
        m = decode(music)
        m = np.tile(m, int(np.ceil(len(buf) / len(m))))[: len(buf)] * 0.11
        f = int(1.5 * SR)
        m[-f:] *= np.linspace(1, 0, f)
        buf += m
    buf = buf / (np.max(np.abs(buf)) or 1) * 0.9
    run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(out / "audio.wav")],
        input=(buf * 32767).astype(np.int16).tobytes())

    # 5. compose
    final = out / f"{spec['episode']}_short_{lang}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0b1220:s=1080x1920:r={FPS}:d={duration}",
         "-i", str(out / "panel.mp4"), "-i", str(out / "overlay.mov"), "-i", str(out / "audio.wav"),
         "-filter_complex", f"[0:v][1:v]overlay={PANEL['x']}:{PANEL['y']}:eof_action=pass[a];[a][2:v]overlay=0:0[v]",
         "-map", "[v]", "-map", "3:a", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-t", str(duration), "-movflags", "+faststart", str(final)])
    print("short:", final)


if __name__ == "__main__":
    main((ROOT / sys.argv[1]).resolve(), sys.argv[2])
