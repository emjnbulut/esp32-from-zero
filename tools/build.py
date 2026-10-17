"""Build an episode: schedule -> narration mix -> subtitles -> compose final video.

Usage:
  python tools/build.py video/ep01 schedule     # timings for the animation (after tts.py)
  python tools/build.py video/ep01 audio        # narration (+ music) mix as one WAV
  python tools/build.py video/ep01 subs         # en.srt and tr.srt
  python tools/build.py video/ep01 compose      # mux render + audio + creator clips -> final.mp4
  python tools/build.py video/ep01 all          # schedule, audio, subs (render separately), compose

Creator clips go in footage/ep01/<CLIP_ID>.<mp4|mov|...>; missing clips keep the placeholder card.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import music  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SR = 48000

LEAD_IN = 3.2      # title animation before the first word
GAP = 0.45         # pause between segments of the same scene
SCENE_GAP = 1.1    # pause when the scene changes
TAIL = 4.0         # outro hold after the last word


def load(ep: Path):
    script = json.loads((ep / "script.json").read_text(encoding="utf-8"))
    timings = json.loads((ep / "build" / "audio" / "timings.json").read_text(encoding="utf-8"))
    return script, timings


def schedule(ep: Path):
    script, timings = load(ep)
    t, prev_scene, segs = LEAD_IN, None, {}
    for s in script["segments"]:
        if prev_scene and s["scene"] != prev_scene:
            t += SCENE_GAP - GAP
        t += s.get("pre", 0)
        dur = timings[s["id"]]["duration"]
        segs[s["id"]] = {
            "start": round(t, 3), "dur": dur, "end": round(t + dur, 3), "scene": s["scene"],
            "words": [{"w": w["w"], "t": round(w["t"], 3)} for w in timings[s["id"]]["words"]],
        }
        t += dur + GAP + s.get("pad", 0)
        prev_scene = s["scene"]
    duration = round(t - GAP + TAIL, 3)
    out = {"duration": duration, "segments": segs}
    (ep / "build").mkdir(exist_ok=True)
    (ep / "build" / "schedule.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"schedule: {duration:.1f}s ({duration / 60:.2f} min)")
    return out


def decode(path: Path) -> np.ndarray:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32)


def audio(ep: Path):
    sched = json.loads((ep / "build" / "schedule.json").read_text(encoding="utf-8"))
    buf = np.zeros(int((sched["duration"] + 1) * SR), dtype=np.float32)
    for sid, s in sched["segments"].items():
        a = decode(ep / "build" / "audio" / f"{sid}.mp3")
        i = int(s["start"] * SR)
        buf[i:i + len(a)] += a
    buf = music.mix(buf, SR, decode, level=0.10)
    peak = np.max(np.abs(buf)) or 1
    buf = buf / peak * 0.89
    pcm = (buf * 32767).astype(np.int16)
    out = ep / "build" / "narration.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(out)],
                   input=pcm.tobytes(), check=True)
    print("audio:", out)


# ---------- subtitles ----------
def split_cues(text: str, max_chars=84):
    """Split text into cues at sentence / clause boundaries, each <= max_chars."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    cues = []
    for s in sentences:
        parts = -(-len(s) // max_chars)  # ceil
        while parts > 1:
            target = len(s) // parts
            # nearest clause break to the target, else nearest space
            cands = [i for i in range(len(s)) if s[i:i + 2] in (", ", ": ", "; ")]
            near = [i for i in cands if abs(i - target) < target * 0.45]
            if near:
                cut = min(near, key=lambda i: abs(i - target))
            else:
                spaces = [i for i in range(len(s)) if s[i] == " "]
                cut = min(spaces, key=lambda i: abs(i - target))
            cues.append(s[: cut + 1].strip())
            s = s[cut + 1:].strip()
            parts -= 1
        if s:
            cues.append(s)
    return cues


def wrap2(cue: str, width=42):
    if len(cue) <= width:
        return cue
    mid = len(cue) // 2
    left, right = cue.rfind(" ", 0, mid + 1), cue.find(" ", mid)
    cut = left if right == -1 or (left != -1 and mid - left <= right - mid) else right
    return cue[:cut] + "\n" + cue[cut + 1:]


def fmt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def seg_cues(text, seg):
    """Time cues by mapping their character position onto the spoken word timings."""
    cues = split_cues(text)
    total = sum(len(c) for c in cues)
    words = seg["words"]
    def time_at(frac):
        if not words:
            return seg["start"] + frac * seg["dur"]
        i = min(int(frac * len(words)), len(words) - 1)
        return seg["start"] + words[i]["t"]
    out, acc = [], 0
    for c in cues:
        t0 = seg["start"] if acc == 0 else time_at(acc / total)
        acc += len(c)
        t1 = seg["end"] if acc >= total else time_at(acc / total)
        out.append((t0, t1, wrap2(c)))
    return out


def subs(ep: Path):
    script, _ = load(ep)
    sched = json.loads((ep / "build" / "schedule.json").read_text(encoding="utf-8"))
    for lang in ("en", "tr"):
        cues = []
        for s in script["segments"]:
            text = s.get("sub", s["text"]) if lang == "en" else s["tr"]
            cues += seg_cues(text, sched["segments"][s["id"]])
        lines = []
        for n, (t0, t1, c) in enumerate(cues, 1):
            nxt = cues[n][0] if n < len(cues) else t1 + 10
            t1 = min(max(t1, t0 + 1.2), nxt - 0.05)
            lines.append(f"{n}\n{fmt(t0)} --> {fmt(t1)}\n{c}\n")
        p = ep / "build" / f"{ep.name}_{lang}.srt"
        p.write_text("\n".join(lines), encoding="utf-8")
        print("subs:", p)


# ---------- compose ----------
def compose(ep: Path):
    b = ep / "build"
    clips = json.loads((b / "clips.json").read_text(encoding="utf-8")) if (b / "clips.json").exists() else []
    footage = ROOT / "footage" / ep.name
    inputs = ["-i", str(b / "video.mp4"), "-i", str(b / "narration.wav")]
    filters, last, k = [], "[0:v]", 2
    for c in clips:
        src = next(iter(sorted(footage.glob(c["id"] + ".*"))), None) if footage.exists() else None
        if not src:
            print(f"clip {c['id']}: no footage yet, placeholder stays")
            continue
        inputs += ["-i", str(src)]
        w, h, d = c["w"] - 6, c["h"] - 6, c["t1"] - c["t0"]
        filters.append(f"[{k}:v]trim=0:{d:.3f},setpts=PTS-STARTPTS+{c['t0']:.3f}/TB,"
                       f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=30[c{k}]")
        filters.append(f"{last}[c{k}]overlay={c['x'] + 3}:{c['y'] + 3}:eof_action=pass:"
                       f"enable='between(t,{c['t0']:.3f},{c['t1']:.3f})'[v{k}]")
        last, k = f"[v{k}]", k + 1
        print(f"clip {c['id']}: {src.name}")
    out = b / f"{ep.name}_final.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs]
    if filters:
        cmd += ["-filter_complex", ";".join(filters), "-map", last]
    else:
        cmd += ["-map", "0:v"]
    cmd += ["-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print("final:", out)


if __name__ == "__main__":
    ep = (ROOT / sys.argv[1]).resolve()
    step = sys.argv[2]
    steps = {"schedule": [schedule], "audio": [audio], "subs": [subs], "compose": [compose],
             "all": [schedule, audio, subs, compose]}[step]
    for fn in steps:
        fn(ep)
