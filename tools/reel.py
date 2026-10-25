"""Build a project Reel / Short (1080x1920, no narration: music + big on-screen text) from projects/<NN>/reel.json.

Usage: python tools/reel.py projects/01-sos-beacon            -> projects/01-sos-beacon/build/reel.mp4

reel.json: {"segments": [...]} played in order; each segment has "dur" (seconds of the final video) and one of
  {"footage": "footage/projects/01/S1.mp4", "in": 0.5, "speed": 1.0, "text": "...", "sub": "...", "desc": "..."}
      the creator's vertical clip (cropped to fill 9:16); "speed" > 1 for timelapses. While the file is missing,
      a placeholder card with "desc" is shown, so the Reel can be previewed before filming.
  {"code": "line\\nline", "hl": [0, 2], "text": "..."}   one big code card (lines in "hl" are lit in turn)
  {"end": true, "text": "...", "sub": "..."}            the closing card
Text uses <b>..</b> for the amber highlight. Music: the channel track (tools/music.py), faded out at the end.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import music  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SR, FPS = 48000, 30


def run(cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


def decode(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32)


def main(pdir: Path):
    spec = json.loads((pdir / "reel.json").read_text(encoding="utf-8"))
    out = pdir / "build"
    out.mkdir(parents=True, exist_ok=True)

    # 1. timeline
    t, segs = 0.0, []
    for s in spec["segments"]:
        kind = "end" if s.get("end") else "code" if "code" in s else "footage"
        seg = {"kind": kind, "t0": round(t, 3), "t1": round(t + s["dur"], 3), "text": s.get("text", ""), "sub": s.get("sub", "")}
        if kind == "code":
            seg.update(code=s["code"], hl=s.get("hl"))
        if kind == "footage" and not (ROOT / s["footage"]).exists():
            seg.update(missing=Path(s["footage"]).stem, desc=s.get("desc", ""))
        segs.append(seg)
        t += s["dur"]
    duration = round(t, 3)
    data = {"schedule": {"duration": duration, "segments": {}}, "segments": segs}
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    missing = [s["missing"] for s in segs if s.get("missing")]
    print(f"{pdir.name}: {duration:.1f}s" + (f" (placeholders for {', '.join(missing)})" if missing else ""))

    # 2. text / code / end-card layer, transparent
    run(["node", "engine/render.mjs", "reel", "--page", str(ROOT / "video" / "reel" / "index.html"), "--data", str(out / "data.json"),
         "--size", "1080x1920", "--alpha", "--out", str(out / "overlay.mov")], cwd=ROOT / "video")

    # 3. base video: the creator's clips filling 9:16 (black where the overlay is opaque)
    inputs, filters, labels = [], [], []
    for s, seg in zip(spec["segments"], segs):
        k, d = len(labels), seg["t1"] - seg["t0"]
        if seg["kind"] == "footage" and not seg.get("missing"):
            sp = s.get("speed", 1.0)
            inputs += ["-ss", f"{s.get('in', 0):.3f}", "-t", f"{d * sp + 0.5:.3f}", "-i", str(ROOT / s["footage"])]
            filters.append(f"[{k}:v]setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase,"
                           f"crop=1080:1920,trim=duration={d:.3f},setpts=PTS-STARTPTS,setsar=1[s{k}]")
        else:
            inputs += ["-f", "lavfi", "-t", f"{d:.3f}", "-i", f"color=c=black:s=1080x1920:r={FPS}"]
            filters.append(f"[{k}:v]setsar=1[s{k}]")
        labels.append(f"[s{k}]")
    filters.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[base]")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[base]",
         "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(out / "base.mp4")])

    # 4. music only (no narration)
    buf = music.mix(np.zeros(int((duration + 0.5) * SR), dtype=np.float32), SR, decode, level=1.0, fade_in=0.3, fade_out=2.0)
    buf = buf / (np.max(np.abs(buf)) or 1) * 0.8
    run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(out / "audio.wav")],
        input=(buf * 32767).astype(np.int16).tobytes())

    # 5. compose
    final = out / "reel.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(out / "base.mp4"), "-i", str(out / "overlay.mov"), "-i", str(out / "audio.wav"),
         "-filter_complex", "[0:v][1:v]overlay=0:0[v]", "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(duration),
         "-movflags", "+faststart", str(final)])
    print("reel:", final)


if __name__ == "__main__":
    main((ROOT / sys.argv[1]).resolve())
