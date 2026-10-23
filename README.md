# ESP32 From Zero

A free, beginner-friendly video series that teaches the ESP32 microcontroller step by step.
If you know a little C, you can follow along.

- **Videos:** YouTube (link coming soon), English narration with English and Turkish subtitles
- **Episode list:** see [CURRICULUM.md](CURRICULUM.md)

## Repository layout

```
lessons/
  01-setup/
    README.md     # written version of the episode
    code/         # sketches you can open in Arduino IDE
    wiring/       # wiring diagrams
video/            # source files for the animations and narration scripts
tools/            # scripts that build the videos
```

## Episodes

| # | Episode | Lesson |
|---|---------|--------|
| 01 | Setting Up Your Computer | [lessons/01-setup](lessons/01-setup) |
| 02 | Meet the Board and the Breadboard | [lessons/02-board-and-breadboard](lessons/02-board-and-breadboard) |
| 03 | Your First Circuit: Blink an LED | [lessons/03-blink-an-led](lessons/03-blink-an-led) |
| 04 | Buttons and Doing Two Things at Once | [lessons/04-buttons-and-millis](lessons/04-buttons-and-millis) |

## How the videos are made

Before producing episode 4 or later, follow the [production guidelines](video/PRODUCTION_GUIDELINES.md): outcome-focused titles and thumbnails, a result-first opening, and Shorts linked to their full lesson.

Each episode is code: `video/epXX/script.json` holds the narration (with Turkish subtitle text),
`video/epXX/epXX.js` animates a recreated desktop and 2D/3D diagrams in HTML/SVG + GSAP, and
`video/engine/render.mjs` renders it frame by frame with Playwright. Short real-hardware clips
are composited in at the end.

```
python tools/tts.py video/ep01                 # narration (edge-tts) + word timings
python tools/build.py video/ep01 schedule      # timeline
node   video/engine/render.mjs ep01            # frames -> video.mp4   (run inside video/)
python tools/build.py video/ep01 audio         # narration + music mix
python tools/build.py video/ep01 subs          # English + Turkish .srt
python tools/build.py video/ep01 compose       # + camera clips -> final mp4
```

## What you need

- An ESP32 development board (this series uses the ESP-32S WiFi starter kit)
- A micro USB data cable
- A computer with Windows, macOS or Linux
- [Arduino IDE 2](https://www.arduino.cc/en/software)

## License

- Arduino/ESP32 teaching examples and first-party tools software: **MIT**, including commercial reuse.
- New original videos, illustrations, lesson text and audiovisual sources: **CC BY-NC-SA 4.0**;
  commercial use requires separate permission.
- Historical MIT/CC BY grants and third-party terms remain valid; no retroactive restriction.

Read [LICENSING.md](LICENSING.md) for scope/history, [LICENSE](LICENSE) for license files,
and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for exclusions.
