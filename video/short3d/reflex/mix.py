"""Soundtrack of the reflex-game Short -> build/<lang>/audio.wav (48 kHz stereo, loudness -16 LUFS).

    .venv/Scripts/python video/short3d/reflex/mix.py --lang en

Narration (build/<lang>/voice.wav) + effects from story.events() + the music bed (tools/music.py, ducked under the
voice, level 0.11 as in the other 3D Shorts). Every buzzer sound is video/b3d/assemble.py piezo() at the sketch's
frequencies (GO! tone(1500, 150), new record tone(2000, 300)); the whole effects track is scaled by
assemble.SFX_GAIN (creator: the Ep10 beeps sat on top of the voice), so the beeps stay under the narration.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LANG = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else os.environ.get("REFLEX_LANG", "en")
os.environ["REFLEX_LANG"] = LANG
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "video", "b3d"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import assemble as A  # noqa: E402
import music  # noqa: E402
import story as S  # noqa: E402

SR = A.SR
B = os.path.join(HERE, "build", LANG)
BUZZ_UNDER_DB = 8.0  # buzzer tones sit this far (RMS) under the narration's speech level (creator: beeps under the voice)


def decode(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def chime(vol=0.12):
    return A.seq((0, A.tone(1319, 0.18, vol)), (0.09, A.tone(1760, 0.3, vol)))


def power_down(vol=0.10):
    """soft falling sweep when the board goes dark (UI sound, not the buzzer)"""
    d = 0.45
    t = np.arange(int(d * SR)) / SR
    f = np.linspace(520, 90, len(t))
    w = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)
    return (w * vol).astype(np.float32)


def main():
    st = S.Story(LANG)
    voice = decode(os.path.join(B, "voice.wav"))
    n = len(voice)
    fx = np.zeros(n, np.float32)

    def put(sig, t):
        i = int(t * SR)
        if 0 <= i < n:
            j = min(n, i + len(sig))
            fx[i:j] += sig[: j - i]

    # the raw narration is quieter than an episode's mastered voice track, so the buzzer level is set relative to it:
    # tone RMS (after SFX_GAIN) = speech RMS - BUZZ_UNDER_DB
    hop = SR // 50
    fr = voice[: len(voice) // hop * hop].reshape(-1, hop)
    e = np.sqrt((fr ** 2).mean(1))
    speech = float(np.sqrt((e[e > e.max() * 0.1] ** 2).mean()))
    ref = A.piezo(1500, 0.15, 1.0)
    buzz_vol = speech * 10 ** (-BUZZ_UNDER_DB / 20) / (float(np.sqrt((ref ** 2).mean())) * A.SFX_GAIN)
    print(f"speech rms {20 * np.log10(speech):.1f} dB -> buzzer peak {buzz_vol * A.SFX_GAIN:.3f}")
    for t, kind, arg in st.events():
        if kind == "tone":
            put(A.piezo(arg["f"], arg["d"], buzz_vol), t)
        elif kind == "click":
            put(A.SFX["click"](), t)
        elif kind == "tap":
            put(A.SFX["click"]() * 0.6, t)
        elif kind in ("pop", "unplug", "plug"):
            put(A.SFX[kind](), t)
        elif kind == "down":
            put(power_down(), t)
        elif kind == "boot":
            put(A.tone(1200, 0.06, 0.06), t)  # soft UI blip (the sketch itself does not beep at boot)
        elif kind == "ding":
            put(chime(), t)
    fx *= A.SFX_GAIN
    mixed = music.mix(voice + fx, SR, decode, level=0.11, fade_in=0.5, fade_out=1.5)
    peak = float(np.max(np.abs(mixed)))
    if peak > 0.98:
        mixed *= 0.98 / peak
    # two-pass loudnorm with a limiter first (buzzer peaks), as in the treasure Short
    pre = "alimiter=limit=0.6:attack=2:release=40:level=false,"
    pcm = mixed.astype(np.float32).tobytes()
    m = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                        pre + "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       input=pcm, capture_output=True, check=True).stderr.decode("utf-8", "ignore")
    j = json.loads(re.findall(r"\{[^{}]*\}", m)[-1])
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                    pre + ln, "-ar", str(SR), "-ac", "2", os.path.join(B, "audio.wav")], input=pcm, check=True)
    print(f"audio.wav ({LANG})", round(n / SR, 2), "s, peak", round(peak, 3))


if __name__ == "__main__":
    main()
