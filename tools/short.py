"""Build a vertical summary Short for an episode, in one language.

Usage: python tools/short.py video/shorts/ep01 en
Output: video/shorts/ep01/build/<lang>/<episode>_short_<lang>.mp4

short.json lists narration segments; each has text per language ("say" is spoken,
"show" is the on-screen caption), a headline, and shots. Only "say" is needed per
language; on-screen text (show, headline, chip, cta) falls back to English.
Shots are moments of the rendered episode video ("src" seconds, optional "speed", optional "pan" = end x) cropped to a region [x, y, w, h].
Instead of "src", "at": ["s10", "Pull", -0.3] anchors a shot to a word of the episode narration (word text or index,
optional offset in seconds; needs "schedule" = the episode's build/schedule.json), so shots stay right when the narration changes.
"engine": "chatterbox" (optional "cbx" settings, see tools/cbx.py) narrates with Chatterbox instead of edge-tts.
"loop": true makes the Short seamless: no tail, music wraps around, and the last frame is the first shot.
"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

import edge_tts
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import cbx  # noqa: E402
import music  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
FPS = 30
PANEL = {"x": 70, "y": 380, "w": 940, "h": 940}
LEAD, GAP, TAIL = 0.35, 0.3, 2.4
VOICES = {"en": ("en-US-EricNeural", "+5%"), "tr": ("tr-TR-EmelNeural", "+0%"),
          "hi": ("hi-IN-MadhurNeural", "+10%"), "pt": ("pt-BR-AntonioNeural", "+0%")}


def loc(v, lang):
    """A text that is either one string for every language or {lang: text}.
    On-screen text may stay English: only "say" must exist per language, the rest falls back to en."""
    return v.get(lang, v["en"]) if isinstance(v, dict) else v


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


def narrate_chatterbox(spec, lang, out):
    """All lines in one Chatterbox run (cached by text + settings); word times from whisper."""
    import align
    cfg = cbx.settings(spec, lang)
    cache_p = out / "cbx_cache.json"
    cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}
    todo = []
    for s in spec["segments"]:
        k = cbx.key(cfg, s["say"][lang])
        if cache.get(s["id"], {}).get("key") != k or not (out / f"{s['id']}.mp3").exists():
            todo.append(s)
            cache[s["id"]] = {"key": k}
    cbx.say(cfg, [(s["say"][lang], out / f"{s['id']}.mp3") for s in todo])
    for s in todo:
        cache[s["id"]]["words"] = [w["t"] for w in align.align(out / f"{s['id']}.mp3", s["say"][lang], lang)]
    cache_p.write_text(json.dumps(cache, indent=1), encoding="utf-8")
    return {sid: c["words"] for sid, c in cache.items()}


def word_time(seg, word):
    if isinstance(word, int):
        return seg["words"][word]["t"]
    norm = lambda w: "".join(c for c in w.lower() if c.isalnum())
    for w in seg["words"]:
        if norm(w["w"]) == norm(word):
            return w["t"]
    raise SystemExit(f"word {word!r} not in narration")


def resolve_src(spec):
    """Turn "at" anchors into "src" seconds of the episode video."""
    if "schedule" not in spec:
        return
    segs = json.loads((ROOT / spec["schedule"]).read_text(encoding="utf-8"))["segments"]
    for s in spec["segments"]:
        for sh in s["shots"]:
            if "at" in sh:
                sid, word, off = (sh["at"] + [0])[:3]
                sh["src"] = round(segs[sid]["start"] + (word_time(segs[sid], word) if word is not None else 0) + off, 3)


def decode(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32)


def main(sdir: Path, lang: str):
    spec = json.loads((sdir / "short.json").read_text(encoding="utf-8"))
    out = sdir / "build" / lang
    out.mkdir(parents=True, exist_ok=True)
    resolve_src(spec)
    chatterbox = cbx.engine(spec) == "chatterbox"
    if chatterbox:
        cbx_words = narrate_chatterbox(spec, lang, out)
        if "--narrate" in sys.argv:  # only the takes (then tools/cbx_retake.py --short, then the full build)
            return
    else:
        voice, rate = VOICES[lang]

    # 1. narration + timing
    t, sched = LEAD, {}
    for s in spec["segments"]:
        mp3 = out / f"{s['id']}.mp3"
        spoken = cbx_words[s["id"]] if chatterbox else asyncio.run(narrate(s["say"][lang], voice, rate, mp3))
        dur = probe(mp3)
        shown = loc(s["show"], lang).split()
        # map on-screen words onto spoken word times (they can differ, e.g. "C P 2102" vs "CP2102")
        words = [{"w": w, "t": round(t + spoken[min(len(spoken) - 1, int(j * len(spoken) / len(shown)))], 3)}
                 for j, w in enumerate(shown)] if spoken else []
        sched[s["id"]] = {"start": round(t, 3), "end": round(t + dur, 3), "words": words}
        t += dur + GAP
    # loop: no tail - the end runs straight back into the start (LEAD gives the pause between them)
    loop = spec.get("loop", False)
    duration = round(t - GAP + (0.05 if loop else TAIL), 3)
    ids = [s["id"] for s in spec["segments"]]
    data = {"schedule": {"duration": duration, "segments": sched}, "panel": PANEL, "lang": lang, "loop": loop,
            "segs": [{"id": s["id"], "chip": loc(s["chip"], lang), "headline": loc(s["headline"], lang)} for s in spec["segments"]],
            "cta": {"title": loc(spec["cta"], lang), "sub": loc(spec["cta"].get("sub", ""), lang)}}
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
    segments = [dict(s) for s in spec["segments"]]
    if loop:  # end on the first shot's opening frame, so the jump back to the start is invisible
        first = segments[0]["shots"][0]
        segments[-1]["shots"] = segments[-1]["shots"] + [{"src": first["src"], "crop": first["crop"], "dur": 0.9}]
    for i, s in enumerate(segments):
        a = 0 if i == 0 else sched[s["id"]]["start"]
        b = sched[ids[i + 1]]["start"] if i + 1 < len(ids) else duration
        fixed = sum(sh["dur"] for sh in s["shots"] if "dur" in sh)
        free = [sh for sh in s["shots"] if "dur" not in sh]
        for j, sh in enumerate(s["shots"]):
            # optional "footage": {"file", "src", "crop"} replaces the shot once that creator clip exists
            if "footage" in sh and (ROOT / sh["footage"]["file"]).exists():
                sh = {**sh, **sh["footage"]}
            d = sh.get("dur", (b - a - fixed) / max(1, len(free)))
            sp = sh.get("speed", 1.0)
            k = len(labels)
            inputs += ["-ss", f"{sh['src']:.3f}", "-t", f"{d * sp + 0.5:.3f}", "-i", str(ROOT / sh["file"] if "file" in sh else src)]
            x, y, w, h = sh["crop"]
            # optional "pan": crop x slides from x to pan over the shot (for content wider than the panel)
            if "pan" in sh:
                x = f"'{x}+({sh['pan']}-{x})*min(1,max(0,(t-0.4)/{max(d - 0.8, 0.1):.3f}))'"
            # wide shots: fill the rest of the square panel with a blurred, darkened copy instead of flat colour
            W, H = PANEL["w"], PANEL["h"]
            filters.append(f"[{k}:v]setpts=(PTS-STARTPTS)/{sp},fps={FPS},crop={w}:{h}:{x}:{y},split[f{k}][b{k}];"
                           f"[b{k}]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                           f"boxblur=28:2,eq=brightness=-0.1:saturation=0.8[bg{k}];"
                           f"[f{k}]scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos[fg{k}];"
                           f"[bg{k}][fg{k}]overlay=(W-w)/2:(H-h)/2,"
                           f"tpad=stop_mode=clone:stop_duration={d + 0.1:.3f},trim=duration={d:.3f},setpts=PTS-STARTPTS,setsar=1[s{k}]")
            labels.append(f"[s{k}]")
    filters.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[panel]")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[panel]",
         "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(out / "panel.mp4")])

    # 4. audio: narration + music bed
    buf = np.zeros(int((duration + (0 if loop else 1)) * SR), dtype=np.float32)
    for sid in ids:
        a = decode(out / f"{sid}.mp3")
        i = int(sched[sid]["start"] * SR)
        buf[i:i + len(a)] += a[: len(buf) - i]
    if loop:
        buf = music.mix(buf, SR, decode, level=0.12, seamless=True)
    else:
        buf = music.mix(buf, SR, decode, level=0.12, fade_in=0, fade_out=1.5)
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
