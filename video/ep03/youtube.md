# YouTube upload — Episode 3

## Title
ESP32 From Zero #3 — Blink an LED: Your First Program That Controls Hardware

## Description
Time for code to take control! We find out why the LED needs a 220 Ω resistor (Ohm's law, simply), move the resistor's leg from the + rail to GPIO 23 (red wire out), and write the classic Blink sketch with pinMode, digitalWrite and delay. Then we upload it, watch the board report each change in the Serial Monitor, and play with the timing.

🔗 Links
• Lesson + Blink code: https://github.com/emjnbulut/esp32-from-zero/tree/main/lessons/03-blink-an-led
• All code + lessons: https://github.com/emjnbulut/esp32-from-zero

⏱ Chapters
0:00 Intro
0:26 Last episode's circuit
0:39 Why 220 Ω? Ohm's law
1:30 Move the resistor
2:12 Write the code
3:21 Upload and blink
3:51 What happens on the pin
4:03 Play with the timing
4:21 LED not blinking?
4:37 Recap and next episode

🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
🎙 Narration: Chatterbox TTS (Resemble AI, MIT). Voice references: LibriVox (public domain) and FLEURS by Google (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Blink #LED #Electronics #Microcontroller

## Creator clips (footage/ep03/)
- `C1` — USB unplugged. Take the red wire out, then move the resistor's leg from the plus rail into hole j16 (the D23 column). Close-up from above, landscape, 6-10 s.
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
