"""Build the picture of a v2 episode (Blender shots + Motion Canvas scenes) and its sound effects.

    .venv/Scripts/python video/b3d/assemble.py video/ep10            # video.mp4 + sfx.wav into video/ep10/build
    .venv/Scripts/python video/b3d/assemble.py video/ep10 --check    # only list the runs and what is missing

A run = consecutive segments with the same "vis". It lasts from its first segment's start (0 for the first run) to
the next run's start (the episode end for the last), the same cut points ep10_3d.py uses for its shots.
  b3d:<id>  -> <ep>/b3d/build/shots/<id>/f_*.png, labels drawn by overlay.py into shots_ov/<id>/ (cached)
  mc:<id>   -> video/mc/output/<id>.mp4
A run that is too short is padded with its last frame, a long one is trimmed. Missing sources -> dark placeholder
with the run name, so the cut can be checked before everything is rendered.
Then tools/build.py <ep> audio (mixes build/sfx.wav under the narration), subs, compose (bumpers, final mp4).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FPS = 30
SR = 48000
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def runs(ep: Path):
    script = json.loads((ep / "script.json").read_text(encoding="utf-8"))
    sch = json.loads((ep / "build" / "schedule.json").read_text(encoding="utf-8"))
    out = []
    for s in script["segments"]:
        st = sch["segments"][s["id"]]["start"]
        if out and out[-1]["vis"] == s["vis"]:
            out[-1]["segs"].append(s["id"])
            continue
        if out:
            out[-1]["end"] = st
        out.append({"vis": s["vis"], "segs": [s["id"]], "start": 0.0 if not out else st})
    out[-1]["end"] = sch["duration"]
    return out, sch["duration"]


def source(ep: Path, r):
    kind, name = r["vis"].split(":", 1)
    if kind == "b3d":
        d = ep / "b3d" / "build" / "shots" / name
        frames = sorted(d.glob("f_*.png")) if d.exists() else []
        return ("frames", d, len(frames)) if frames else None
    if kind == "mc":
        f = ROOT / "video" / "mc" / "output" / f"{name}.mp4"
        return ("mp4", f, 0) if f.exists() else None
    return None


def overlaid(ep: Path, d: Path) -> Path:
    """labels on top of the Blender frames (overlay.py), redone only when frames or labels are newer"""
    ovj = d / "overlay.json"
    if not ovj.exists():
        return d
    out = ep / "b3d" / "build" / "shots_ov" / d.name
    newest = max(p.stat().st_mtime for p in [ovj, *d.glob("f_*.png")])
    done = sorted(out.glob("f_*.png")) if out.exists() else []
    if len(done) != len(list(d.glob("f_*.png"))) or min(p.stat().st_mtime for p in done) < newest:
        out.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(ROOT / "video" / "b3d" / "overlay.py"), str(d), str(ovj), str(out)], check=True)
    return out


def piece(ep: Path, r, i, tmp: Path) -> Path:
    dur = r["end"] - r["start"]
    out = tmp / f"run_{i:03d}.mp4"
    src = source(ep, r)
    fit = f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0b1220," \
          f"fps={FPS},tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f},setpts=PTS-STARTPTS,format=yuv420p"
    if src is None:
        label = r["vis"].replace(":", "\\:")
        cmd = ["-f", "lavfi", "-i", f"color=c=0x0b1220:s=1920x1080:r={FPS}:d={dur:.3f}",
               "-vf", f"drawtext=fontfile='C\\:/Windows/Fonts/segoeuib.ttf':text='{label}':fontcolor=0x5b6b85:"
                      f"fontsize=64:x=(w-tw)/2:y=(h-th)/2,format=yuv420p"]
    elif src[0] == "frames":
        d = overlaid(ep, src[1])
        cmd = ["-framerate", str(FPS), "-i", str(d / "f_%04d.png"), "-vf", fit]
    else:
        cmd = ["-i", str(src[1]), "-an", "-vf", fit]
    subprocess.run(["ffmpeg", "-v", "error", "-y", *cmd, *ENC, "-t", f"{dur:.3f}", str(out)], check=True)
    return out


# ------------------------------------------------------------------ sound effects
def tone(f, d, vol, f2=None):
    t = np.arange(int(d * SR)) / SR
    fr = f if f2 is None else np.linspace(f, f2, len(t))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    w = np.sign(np.sin(ph)) * 0.35 + np.sin(ph) * 0.65  # a little square = piezo buzzer bite
    env = np.minimum(1, np.minimum(t / 0.004, (d - t) / 0.03).clip(0))
    return (w * env * vol).astype(np.float32)


def noise(d, vol, hp=True, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(int(d * SR)).astype(np.float32)
    if hp:
        x = np.diff(x, prepend=0)  # crude high-pass: clicky, not hissy
    env = np.exp(-np.arange(len(x)) / (SR * d / 4))
    return (x * env * vol).astype(np.float32)


def seq(*parts):
    """[(offset_s, wave)] -> one wave"""
    n = max(int(o * SR) + len(w) for o, w in parts)
    out = np.zeros(n, np.float32)
    for o, w in parts:
        out[int(o * SR):int(o * SR) + len(w)] += w
    return out


SFX = {
    "beep_hi": lambda: tone(1568, 0.20, 0.30),
    "beep_lo": lambda: tone(220, 0.45, 0.30),
    "tone_hi_long": lambda: tone(1760, 0.70, 0.25),
    "tone_lo_long": lambda: tone(196, 0.70, 0.28),
    "click": lambda: noise(0.03, 0.35, seed=1),
    "snap": lambda: noise(0.025, 0.22, seed=2),
    "pop": lambda: seq((0, tone(660, 0.05, 0.12, 990)),),
    "record": lambda: seq((0, tone(1047, 0.14, 0.25)), (0.22, tone(1319, 0.14, 0.25)), (0.44, tone(1568, 0.26, 0.25))),
    "unplug": lambda: noise(0.05, 0.30, seed=3),
    "plug": lambda: noise(0.05, 0.30, seed=4),
    "boot": lambda: tone(2093, 0.08, 0.18),
}


def sfx(ep: Path, duration: float):
    p = ep / "b3d" / "build" / "shots.json"
    events = [e for sh in json.loads(p.read_text()) for e in sh["sfx"]] if p.exists() else []
    buf = np.zeros(int((duration + 2) * SR), np.float32)
    unknown = set()
    for e in events:
        make = SFX.get(e["kind"])
        if not make:
            unknown.add(e["kind"])
            continue
        w = make()
        i = int(e["t"] * SR)
        buf[i:i + len(w)] += w[:len(buf) - i]
    if unknown:
        print("sfx: no sound for", sorted(unknown))
    pcm = (np.clip(buf, -1, 1) * 32767).astype(np.int16)
    out = ep / "build" / "sfx.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(out)],
                   input=pcm.tobytes(), check=True)
    print(f"sfx: {len(events)} events -> {out}")


def main():
    ep = (ROOT / sys.argv[1]).resolve()
    rs, duration = runs(ep)
    missing = 0
    for r in rs:
        src = source(ep, r)
        need = round((r["end"] - r["start"]) * FPS)
        note = "MISSING" if src is None else (f"{src[2]} frames (need {need})" if src[0] == "frames" else src[1].name)
        missing += src is None
        print(f"{r['start']:7.2f}-{r['end']:7.2f}  {r['vis']:<22} {','.join(r['segs']):<14} {note}")
    print(f"{len(rs)} runs, {duration:.1f} s, {missing} missing")
    if "--check" in sys.argv:
        return
    tmp = ep / "build" / "runs"
    tmp.mkdir(parents=True, exist_ok=True)
    parts = [piece(ep, r, i, tmp) for i, r in enumerate(rs)]
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    str(ep / "build" / "video.mp4")], check=True)
    print("video:", ep / "build" / "video.mp4")
    sfx(ep, duration)


if __name__ == "__main__":
    main()
