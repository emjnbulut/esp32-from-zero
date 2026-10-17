# YouTube upload — Episode 3

## Title
ESP32 From Zero #3 — Blink an LED: Your First Program That Controls Hardware

## Description
Time for code to take control! We find out why the LED needs a 220 Ω resistor (Ohm's law, simply), move one wire from 3V3 to GPIO 23, and write the classic Blink sketch with pinMode, digitalWrite and delay. Then we upload it, watch the board report each change in the Serial Monitor, and play with the timing.

🔗 Links
• Lesson + Blink code: https://github.com/emjnbulut/esp32-from-zero/tree/main/lessons/03-blink-an-led
• All code + lessons: https://github.com/emjnbulut/esp32-from-zero

⏱ Chapters
0:00 Intro
0:26 Last episode's circuit
0:36 Why 220 Ω? Ohm's law
1:29 Move one wire
2:12 Write the code
3:23 Upload and blink
3:57 What happens on the pin
4:09 Play with the timing
4:28 LED not blinking?
4:44 Recap and next episode

🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Blink #LED #Electronics #Microcontroller

## Creator clips (footage/ep03/)
- `C1` — USB unplugged. Pull the red wire's end out of the 3V3 column and push it into the D23 column (GPIO 23). Close-up from above, landscape, 5-8 s.
- `C2` — The LED blinking once per second after the upload (board, breadboard and LED in frame). Landscape, 5-8 s.
- `C3` — The LED blinking fast (delays set to 100 ms). Landscape, 4-6 s.

Then: `python tools/build.py video/ep03 compose`.

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep03 <VIDEO_ID>

It uploads every `build/ep03_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`
