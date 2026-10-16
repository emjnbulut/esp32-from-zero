"""Generate male US-English voice samples so we can pick the series narrator."""
import asyncio
from pathlib import Path

import edge_tts
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "voice_samples"
OUT.mkdir(parents=True, exist_ok=True)

TEXT = (
    "Hi, and welcome to ESP32 From Zero. "
    "In this first lesson, we're going to set up everything we need on our computer. "
    "Don't worry if you've never touched a microcontroller before. "
    "If you know a little bit of C, you're already ready. "
    "Let's open the browser, and download the Arduino IDE together."
)

EDGE_VOICES = [
    "en-US-AndrewMultilingualNeural",
    "en-US-BrianMultilingualNeural",
    "en-US-ChristopherNeural",
    "en-US-GuyNeural",
    "en-US-EricNeural",
]

KOKORO_VOICES = ["am_michael", "am_adam", "am_fenrir", "am_puck", "am_echo", "am_onyx"]


async def edge_samples():
    for v in EDGE_VOICES:
        await edge_tts.Communicate(TEXT, v).save(str(OUT / f"edge_{v}.mp3"))
        print("ok", v)


def kokoro_samples():
    k = Kokoro(str(ROOT / ".models" / "kokoro-v1.0.onnx"), str(ROOT / ".models" / "voices-v1.0.bin"))
    for v in KOKORO_VOICES:
        samples, sr = k.create(TEXT, voice=v, speed=1.0, lang="en-us")
        sf.write(OUT / f"kokoro_{v}.wav", samples, sr)
        print("ok", v)


if __name__ == "__main__":
    asyncio.run(edge_samples())
    kokoro_samples()
