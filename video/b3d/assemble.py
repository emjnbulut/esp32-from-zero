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
        out = ROOT / "video" / "mc" / "output"
        # Ep11+ scenes carry an episode prefix (ep11_code_read.mp4); Ep10's do not (code_read.mp4)
        f = next((x for x in (out / f"{ep.name}_{name}.mp4", out / f"{name}.mp4") if x.exists()), None)
        return ("mp4", f, 0) if f else None
    return None


def write_waves(ep: Path, d: Path):
    """waves.json for overlay.py: per frame, the beeps still ringing at the buzzer's screen position.
    Beep times come from shots.json ("beeps", shot-relative), positions from the shot's anchors.json."""
    idx, anc = ep / "b3d" / "build" / "shots.json", d / "anchors.json"
    if not (idx.exists() and anc.exists()):
        return
    sh = next((x for x in json.loads(idx.read_text()) if x["id"] == d.name), None)
    beeps = sh.get("beeps", []) if sh else []
    anchors = json.loads(anc.read_text())
    out = {}
    for f, pos in anchors.items():
        t = (int(f) - 1) / FPS
        items = [{"x": pos[0], "y": pos[1], "age": round(t - b["t"], 3), "kind": b["kind"]}
                 for b in beeps if pos and 0 <= t - b["t"] <= 1.2]
        if items:
            out[f] = items
    p = d / "waves.json"
    if json.loads(p.read_text()) != out if p.exists() else True:
        p.write_text(json.dumps(out))


def overlaid(ep: Path, d: Path) -> Path:
    """labels + buzzer sound waves on top of the Blender frames (overlay.py), redone only when something is newer"""
    ovj = d / "overlay.json"
    if not ovj.exists():
        return d
    write_waves(ep, d)
    out = ep / "b3d" / "build" / "shots_ov" / d.name
    extra = [p for p in (d / "waves.json",) if p.exists()]
    newest = max(p.stat().st_mtime for p in [ovj, *extra, *d.glob("f_*.png")])
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
        # a shot starts with its first segment; the first run starts at 0 -> hold the first frame until then
        idx = ep / "b3d" / "build" / "shots.json"
        sh = next((x for x in json.loads(idx.read_text()) if x["id"] == src[1].name), None) if idx.exists() else None
        lead = max(0.0, sh["start"] - r["start"]) if sh else 0.0
        hold = f"tpad=start_mode=clone:start_duration={lead:.3f}," if lead > 0.01 else ""
        cmd = ["-framerate", str(FPS), "-i", str(d / "f_%04d.png"), "-vf", hold + fit]
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


def resonate(x, f0=4000.0, q=2.5):
    """2-pole band-pass (RBJ biquad) - the piezo disc's resonance that makes a buzzer sound shrill"""
    w = 2 * np.pi * f0 / SR
    alpha = np.sin(w) / (2 * q)
    b0, b2 = alpha, -alpha
    a0, a1, a2 = 1 + alpha, -2 * np.cos(w), 1 - alpha
    b0, b2, a1, a2 = b0 / a0, b2 / a0, a1 / a0, a2 / a0
    y = np.zeros_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for i, v in enumerate(x):  # short sounds only, a python loop is fine
        o = b0 * v + b2 * x2 - a1 * y1 - a2 * y2
        x2, x1, y2, y1 = x1, v, y1, o
        y[i] = o
    return y


def piezo(f, d, vol):
    """passive buzzer driven by tone(): square wave at f, through the disc resonance (~4 kHz) + a bit of dry"""
    t = np.arange(int(d * SR)) / SR
    sq = np.sign(np.sin(2 * np.pi * f * t)).astype(np.float32)
    w = 0.75 * resonate(sq) + 0.25 * sq
    a = np.exp(-2 * np.pi * 6500 / SR)  # two one-pole low-passes: keeps the bite, drops the fizz/aliasing
    for _ in range(2):
        y, prev = np.empty_like(w), 0.0
        for i, v in enumerate(w):
            prev = (1 - a) * v + a * prev
            y[i] = prev
        w = y
    env = np.minimum(1, np.minimum(t / 0.002, (d - t) / 0.008).clip(0))
    w = w * env
    return (w / (np.max(np.abs(w)) or 1) * vol).astype(np.float32)


def noise(d, vol, hp=True, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(int(d * SR)).astype(np.float32)
    if hp:
        x = np.diff(x, prepend=0)  # crude high-pass: clicky, not hissy
    env = np.exp(-np.arange(len(x)) / (SR * d / 4))
    return (x * env * vol).astype(np.float32)


def whoosh(d, vol, seed=6):
    """soft air swish for a radio 'packet': noise through a moving box filter, swelling in and out"""
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(int(d * SR)).astype(np.float32)
    x = np.convolve(x, np.ones(24, np.float32) / 24, mode="same")  # drop the hiss, keep the air
    x = np.diff(x, prepend=0) * 6  # and the rumble
    t = np.arange(len(x)) / SR
    env = np.sin(np.pi * t / d) ** 2
    return (x / (np.max(np.abs(x)) or 1) * env * vol).astype(np.float32)


def seq(*parts):
    """[(offset_s, wave)] -> one wave"""
    n = max(int(o * SR) + len(w) for o, w in parts)
    out = np.zeros(n, np.float32)
    for o, w in parts:
        out[int(o * SR):int(o * SR) + len(w)] += w
    return out


# Buzzer sounds follow the sketch (lessons/10-reflex-oled): GO tone(1500, 150), false start tone(200, 400),
# new record tone(2000, 300). Creator 2026-11-24: the old soft sine beeps were not recognisable as a buzzer.
# Overall level of the effects track. Creator 2026-11-25 (Ep10 draft 2): the beeps sat on top of the voice -> -5 dB.
SFX_GAIN = 0.55

SFX = {
    "beep_hi": lambda: piezo(1500, 0.15, 0.55),
    "beep_lo": lambda: piezo(200, 0.40, 0.50),
    "tone_hi_long": lambda: piezo(2500, 0.70, 0.45),
    "tone_lo_long": lambda: piezo(200, 0.70, 0.50),
    "click": lambda: noise(0.03, 0.35, seed=1),
    "snap": lambda: noise(0.025, 0.22, seed=2),
    "pop": lambda: seq((0, tone(660, 0.05, 0.12, 990)),),
    "record": lambda: piezo(2000, 0.30, 0.55),
    "unplug": lambda: noise(0.05, 0.30, seed=3),
    "plug": lambda: noise(0.05, 0.30, seed=4),
    "boot": lambda: piezo(2000, 0.06, 0.35),
    "blip": lambda: piezo(1500, 0.05, 0.35),
    "tone_erase": lambda: seq((0, piezo(800, 0.15, 0.5)), (0.2, piezo(400, 0.25, 0.5))),  # record wiped
    # Episode 11 (lessons/11-motion-alarm): countdown tone(2000, 30); siren = 1800/2600 Hz flipping every 250 ms
    # (one event per quarter second, so a siren of any length is a run of siren_lo/siren_hi events)
    "tick": lambda: piezo(2000, 0.03, 0.45),
    "siren_lo": lambda: piezo(1800, 0.25, 0.42),
    "siren_hi": lambda: piezo(2600, 0.25, 0.42),
    "beep_active": lambda: piezo(2300, 0.45, 0.45),  # active buzzer: its one fixed note
    "note_1": lambda: piezo(1319, 0.2, 0.42),  # passive buzzer playing "any note"
    "note_2": lambda: piezo(1568, 0.2, 0.42),
    "note_3": lambda: piezo(2093, 0.25, 0.42),
    # Episode 12 (lessons/12-phone-control): ring = tone(1319, 180), delay(200), tone(1047, 300); phone taps; packets
    "ring_1": lambda: piezo(1319, 0.18, 0.5),
    "ring_2": lambda: piezo(1047, 0.30, 0.5),
    "tap": lambda: noise(0.018, 0.16, hp=False, seed=5),
    "whoosh": lambda: whoosh(0.32, 0.10),
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
    buf *= SFX_GAIN
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
    if "--sfx" in sys.argv:  # only the sound effects (picture unchanged)
        sfx(ep, duration)
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
