"""Final cut of the treasure Short: hook (main, up to the split) -> build montage -> rest of the main Short.

  python short3d/treasure/assemble.py          (run from video/, after make.sh pieces exist)
Needs: build/glow_frames_v2 + build/overlay.mov (main), build/glow_frames_build + build/build_overlay.mov (montage),
build/voice.wav + build/track.json, build/build_voice.wav + build/build_events.json.
Writes build/audio_final.wav and build/treasure_short_en.mp4. Music runs once over the whole cut (no jump at the joins).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import music  # noqa: E402

SR, FPS = 48000, 30
B = HERE / "build"
T = json.loads((B / "track.json").read_text())
sched = json.loads((B / "schedule.json").read_text())
EV = json.loads((B / "build_events.json").read_text())
L = {l["id"]: l for l in sched["lines"]}
S_FRAME = round((L["l02"]["t0"] - 0.12) * FPS)  # cut point in the main Short
NB = json.loads((B / "build_track.json").read_text())["frames"]


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def tone(freq, dur, attack=0.004, decay=None, square=False):
    tt = np.arange(int(dur * SR)) / SR
    w = np.sin(2 * np.pi * freq * tt)
    if square:
        w = np.sign(w) * 0.6 + w * 0.4
    return (w * np.minimum(1, tt / attack) * np.exp(-tt / (decay or dur / 3))).astype(np.float32)


def put(buf, sig, t, gain):
    i = int(t * SR)
    if 0 <= i < len(buf):
        j = min(len(buf), i + len(sig))
        buf[i:j] += sig[: j - i] * gain


rng = np.random.default_rng(3)
CLICK = (rng.standard_normal(int(0.012 * SR)) * np.exp(-np.arange(int(0.012 * SR)) / (0.002 * SR))).astype(np.float32)

# ---- main: narration + detector blips + button click + fanfare (same as mix.py, without music) ----
main = decode(B / "voice.wav")
tr, win = T["track"], T["windows"]["beep"]
for f in range(1, len(tr)):
    t = f / FPS
    if tr[f]["rled"] and not tr[f - 1]["rled"] and any(a <= t <= b for a, b in win) and not tr[f]["party"]:
        put(main, tone(950 + 650 * T["heat"][f] / 255, 0.05, decay=0.02, square=True), t, 0.11)
tp, tf = T["T"]["press"], T["T"]["party"]
put(main, CLICK, tp - 0.02, 0.35)
put(main, tone(180, 0.05, decay=0.012), tp - 0.02, 0.4)
for fr, dt in [(523.25, 0.0), (659.25, 0.09), (783.99, 0.18), (1046.5, 0.27), (1318.5, 0.36)]:
    put(main, tone(fr, 0.5, decay=0.18) + 0.3 * tone(fr * 2, 0.5, decay=0.1), tf + dt, 0.16)
r2 = np.random.default_rng(11)
for k in range(14):
    put(main, tone(2600 + r2.random() * 2200, 0.12, decay=0.03), tf + 0.3 + k * 0.07, 0.05)

# ---- montage: narration + a click when a part snaps in + a zip per wire + blips once it is "ready" ----
bld = decode(B / "build_voice.wav")
bld = np.concatenate([bld, np.zeros(max(0, int(NB / FPS * SR) - len(bld)), np.float32)])[: int(NB / FPS * SR)]
for t in EV["clicks"]:
    put(bld, CLICK, t, 0.3)
    put(bld, tone(220, 0.06, decay=0.015), t, 0.35)
for t in EV["zips"]:
    n = int(0.16 * SR)
    sweep = np.sin(2 * np.pi * np.cumsum(np.linspace(900, 2400, n)) / SR) * np.hanning(n) * 0.5
    put(bld, sweep.astype(np.float32), t, 0.07)
bt = json.loads((B / "build_track.json").read_text())["track"]
for f in range(1, len(bt)):
    if bt[f]["rled"] and not bt[f - 1]["rled"]:
        put(bld, tone(1560, 0.05, decay=0.02, square=True), f / FPS, 0.11)

cut = int(S_FRAME / FPS * SR)
voice = np.concatenate([main[:cut], bld, main[cut:]])
mixed = music.mix(voice, SR, decode, level=0.12, fade_in=0.5, fade_out=1.5)
mixed *= 0.98 / max(0.98, float(np.max(np.abs(mixed))))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", str(SR), "-ac", "2", str(B / "audio_final.wav")], input=mixed.astype(np.float32).tobytes(), check=True)

# ---- video: [main 0..S) + montage + [main S..] ----
fc = ("[0:v][1:v]overlay=format=auto[m];[2:v][3:v]overlay=format=auto[b];[m]split[m1][m2];"
      f"[m1]trim=end_frame={S_FRAME},setpts=PTS-STARTPTS[a];[m2]trim=start_frame={S_FRAME},setpts=PTS-STARTPTS[c];"
      "[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(B / "glow_frames_v2" / "f_%04d.png"), "-i", str(B / "overlay.mov"),
                "-framerate", str(FPS), "-i", str(B / "glow_frames_build" / "f_%04d.png"), "-i", str(B / "build_overlay.mov"),
                "-i", str(B / "audio_final.wav"), "-filter_complex", fc, "-map", "[v]", "-map", "4:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-shortest",
                str(B / "treasure_short_en.mp4")], check=True)
print("wrote", B / "treasure_short_en.mp4", "cut at frame", S_FRAME, "montage", NB, "frames")
