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

## How the videos are made

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

Code (`lessons/**/code`, `tools/`) is under the [MIT License](LICENSE).
Lesson text, diagrams and video sources are under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
