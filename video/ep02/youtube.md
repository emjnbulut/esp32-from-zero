# YouTube upload — Episode 2

## Title
ESP32 From Zero #2 — Pins, Breadboard & Your First LED Circuit

## Description
Meet your ESP32's pins and the breadboard! We learn the power pins (3V3, 5V, GND), which GPIO pins are safe to use and which to avoid (flash, input-only, strapping, TX/RX), how a breadboard is wired inside, and build our first circuit: an LED with a 220 Ω resistor. No code needed.

🔗 Links
• Lesson + pin tables: https://github.com/emjnbulut/esp32-from-zero/tree/main/lessons/02-board-and-breadboard
• All code + lessons: https://github.com/emjnbulut/esp32-from-zero

⏱ Chapters
0:00 Intro
0:21 What you need
0:35 The pins
1:16 Power pins
1:44 Two safety rules
2:04 GPIO pins
2:28 Pins to avoid
3:20 Safe pins
3:29 The breadboard
4:30 Board on the breadboard
5:08 LED and resistor
5:57 Build the circuit
6:30 Power on!
6:53 Recap and next episode

#ESP32 #Arduino #Breadboard #Electronics #LED #Microcontroller

## Creator clips (footage/ep02/)
- `C1` — Close-up of the board's pin labels (3V3, GND, D2...). Slowly pan along one header so the tiny printed names are readable. Landscape, 5-8 s.
- `C2` — Hands pressing the ESP32 board into the breadboard across the middle gap, evenly on both sides. Landscape, 5-8 s.
- `C3` — The finished circuit (3V3 -> resistor -> LED -> GND). Plug in the USB cable and the LED turns on. Landscape, 5-8 s.

Then: `python tools/build.py video/ep02 compose`.

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep02 <VIDEO_ID>

It uploads every `build/ep02_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`
