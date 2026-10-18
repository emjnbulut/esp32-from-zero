"""Build an episode: schedule -> narration mix -> subtitles -> compose final video.

Usage:
  python tools/build.py video/ep01 schedule     # timings for the animation (after tts.py)
  python tools/build.py video/ep01 audio        # narration (+ music) mix as one WAV
  python tools/build.py video/ep01 subs         # one .srt per language (script, subs/, dub/)
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
import bumpers  # noqa: E402
import cbx  # noqa: E402
import music  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SR = 48000

LEAD_IN = 3.2      # title animation before the first word
GAP = 0.45         # pause between segments of the same scene
SCENE_GAP = 1.1    # pause when the scene changes
TAIL = 4.0         # outro hold after the last word
DUB_FIT = 1.08     # a dub may be sped up this much; beyond it the segment's slot grows for every language
DUB_BREATH = 0.2   # same as tools/dub.py BREATH


def dub_durations(ep: Path) -> dict:
    """{sid: longest narrated dub duration} from build/dub_<lang>/cache.json (Chatterbox dubs only,
    narrate them first with `tools/dub.py <ep> <lang> --report`)."""
    longest = {}
    for f in sorted((ep / "dub").glob("*.json")):
        if cbx.engine(json.loads(f.read_text(encoding="utf-8"))) != "chatterbox":
            continue
        cache = ep / "build" / f"dub_{f.stem}" / "cache.json"
        if cache.exists():
            for sid, c in json.loads(cache.read_text(encoding="utf-8")).items():
                longest[sid] = max(longest.get(sid, 0), c["duration"])
    return longest


def load(ep: Path):
    script = json.loads((ep / "script.json").read_text(encoding="utf-8"))
    timings = json.loads((ep / "build" / "audio" / "timings.json").read_text(encoding="utf-8"))
    return script, timings


def schedule(ep: Path):
    script, timings = load(ep)
    dubs = dub_durations(ep)
    t, prev_scene, segs, stretched = LEAD_IN, None, {}, 0.0
    for s in script["segments"]:
        if prev_scene and s["scene"] != prev_scene:
            t += SCENE_GAP - GAP
        t += s.get("pre", 0)
        dur = timings[s["id"]]["duration"]
        segs[s["id"]] = {
            "start": round(t, 3), "dur": dur, "end": round(t + dur, 3), "scene": s["scene"],
            "words": [{"w": w["w"], "t": round(w["t"], 3)} for w in timings[s["id"]]["words"]],
        }
        start = t
        t += dur + GAP + s.get("pad", 0)
        extra = max(0.0, dubs.get(s["id"], 0) / DUB_FIT + DUB_BREATH - (t - start))
        t += extra  # the picture waits until the longest dub has finished too
        stretched += extra
        prev_scene = s["scene"]
    duration = round(t - GAP + TAIL, 3)
    if stretched:
        print(f"stretched for dubs: +{stretched:.1f}s")
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
    buf = music.mix(buf, SR, decode, level=0.08, fade_in=1.0)
    peak = np.max(np.abs(buf)) or 1
    buf = buf / peak * 0.89
    pcm = (buf * 32767).astype(np.int16)
    out = ep / "build" / "narration.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(out)],
                   input=pcm.tobytes(), check=True)
    print("audio:", out)


# ---------- subtitles ----------
CJK = re.compile(r"[぀-ヿ㐀-鿿가-힯]")


def wide(text: str) -> bool:
    """Japanese/Chinese/Korean: characters are twice as wide and words aren't space-separated."""
    return len(CJK.findall(text)) > len(text) * 0.3


def split_cues(text: str, max_chars=84):
    """Split text into cues at sentence / clause boundaries, each <= max_chars."""
    cjk = wide(text)
    if cjk:
        max_chars //= 2
    sentences = [x for x in re.split(r"(?<=[.!?])\s+|(?<=[。！？])\s*", text.strip()) if x]
    if cjk:  # CJK sentences are short: keep neighbours together while they fit one cue
        merged = []
        for x in sentences:
            if merged and len(merged[-1]) + len(x) <= max_chars:
                merged[-1] += x
            else:
                merged.append(x)
        sentences = merged
    cues = []
    for s in sentences:
        parts = -(-len(s) // max_chars)  # ceil
        while parts > 1:
            target = len(s) // parts
            # nearest clause break to the target, else nearest space (any character for CJK)
            cands = [i for i in range(len(s)) if s[i:i + 2] in (", ", ": ", "; ") or s[i] in "、，；："]
            near = [i for i in cands if abs(i - target) < target * 0.45]
            if near:
                cut = min(near, key=lambda i: abs(i - target))
            else:
                spaces = [target] if cjk else [i for i in range(len(s)) if s[i] == " "]
                cut = min(spaces, key=lambda i: abs(i - target)) if spaces else len(s) - 1
            cues.append(s[: cut + 1].strip())
            s = s[cut + 1:].strip()
            parts -= 1
        if s:
            cues.append(s)
    return cues


def wrap2(cue: str, width=42):
    if wide(cue):
        width //= 2
    if len(cue) <= width:
        return cue
    mid = len(cue) // 2
    if wide(cue):  # CJK: break after the clause mark nearest the middle, else in the middle
        marks = [i + 1 for i, ch in enumerate(cue) if ch in "、，。 " and 0 < i + 1 < len(cue)]
        best = min(marks, key=lambda i: abs(i - mid)) if marks else mid
        cut = best if abs(best - mid) < mid * 0.5 else mid
        while 0 < cut < len(cue) and cue[cut - 1].isascii() and cue[cut - 1].isalnum() and cue[cut].isascii() and cue[cut].isalnum():
            cut += 1  # never split inside a Latin word like "ESP32"
        return cue[:cut].rstrip() + "\n" + cue[cut:].lstrip()
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


def sub_texts(ep: Path, script) -> dict:
    """{lang: {segment id: subtitle text}}. en and tr come from script.json; other languages
    from <ep>/subs/<lang>.json, else from the dub translation <ep>/dub/<lang>.json.
    (The tr dub is spelled phonetically for the voice, so it is never used as subtitles.)"""
    texts = {"en": {s["id"]: s.get("sub", s["text"]) for s in script["segments"]},
             "tr": {s["id"]: s["tr"] for s in script["segments"]}}
    for folder in ("subs", "dub"):
        for f in sorted((ep / folder).glob("*.json")) if (ep / folder).exists() else []:
            if f.stem not in texts:
                texts[f.stem] = json.loads(f.read_text(encoding="utf-8"))["segments"]
    return texts


def subs(ep: Path):
    script, _ = load(ep)
    sched = json.loads((ep / "build" / "schedule.json").read_text(encoding="utf-8"))
    for lang, texts in sub_texts(ep, script).items():
        missing = [s["id"] for s in script["segments"] if s["id"] not in texts]
        if missing:
            print(f"subs {lang}: skipped, missing {', '.join(missing)}")
            continue
        cues = []
        for s in script["segments"]:
            cues += seg_cues(texts[s["id"]], sched["segments"][s["id"]])
        lines = []
        for n, (t0, t1, c) in enumerate(cues, 1):
            nxt = cues[n][0] if n < len(cues) else t1 + 10
            t1 = min(max(t1, t0 + 1.2), nxt - 0.05)
            lines.append(f"{n}\n{fmt(t0 + bumpers.INTRO)} --> {fmt(t1 + bumpers.INTRO)}\n{c}\n")
        p = ep / "build" / f"{ep.name}_{lang}.srt"
        p.write_text("\n".join(lines), encoding="utf-8")
        print("subs:", p)


# ---------- compose ----------
def compose(ep: Path):
    b = ep / "build"
    clips = json.loads((b / "clips.json").read_text(encoding="utf-8")) if (b / "clips.json").exists() else []
    footage = ROOT / "footage" / ep.name
    intro, outro = bumpers.render()
    full = b / "narration_full.wav"  # intro sting + narration + outro music
    pcm = (bumpers.wrap(decode(b / "narration.wav"), SR, decode, ep) * 32767).astype(np.int16)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", str(full)],
                   input=pcm.tobytes(), check=True)
    inputs = ["-i", str(b / "video.mp4"), "-i", str(full), "-i", str(intro), "-i", str(outro)]
    filters, last, k = [], "[0:v]", 4
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
    norm = "fps=30,scale=1920:1080,setsar=1,format=yuv420p"
    filters += [f"{last}{norm}[body]", f"[2:v]{norm}[in]", f"[3:v]{norm}[out]", "[in][body][out]concat=n=3:v=1:a=0[vid]"]
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[vid]"]
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
