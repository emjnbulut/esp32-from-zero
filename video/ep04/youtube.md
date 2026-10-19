# YouTube upload — Episode 4

## Title
ESP32 From Zero #4 — Buttons, Debounce & millis(): Doing Two Things at Once

## Description
Today the ESP32 listens! We wire up a push button, learn why floating pins misbehave and how pull-up resistors fix them, and read the button with digitalRead and INPUT_PULLUP. Then we toggle an LED, tame button bounce, see why delay() freezes everything, and use millis() to blink two LEDs at their own speed while the button still reacts instantly.

🔗 Links
• Lesson + all 5 sketches: https://github.com/emjnbulut/esp32-from-zero/tree/main/lessons/04-buttons-and-millis
• All code + lessons: https://github.com/emjnbulut/esp32-from-zero

⏱ Chapters
0:00 Intro
0:30 The push button
0:52 Wiring the button
1:24 Floating pins and pull-ups
2:41 Writing the code
3:27 Upload and Serial Monitor
4:09 Toggle, edges and bounce
5:36 Why delay() gets in the way
6:15 millis(): check the clock
7:58 A second LED
8:58 Troubleshooting
9:17 Recap and next episode

🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
🎙 Narration: Chatterbox TTS (Resemble AI, MIT). Voice references: LibriVox (public domain) and FLEURS by Google (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Button #millis #Electronics #Microcontroller

## Creator clips (footage/ep04/)
- `C1` — USB unplugged. Press the push button into the breadboard across the middle gap (columns 25-27), then add the yellow wire (D22 -> left side) and the black wire (right side -> minus rail). Close-up from above, landscape, 6-10 s.
- `C2` — button_led sketch: a finger presses and holds the button - the LED lights while it's held, goes dark on release. Landscape, 5-8 s.
- `C3` — button_toggle sketch: press, LED on; press again, LED off (two or three presses). Landscape, 5-8 s.
- `C4` — blink_button sketch: the LED blinks; one press stops it at once, another press starts it again. Landscape, 6-10 s.
- `C5` — USB unplugged. Top half: green wire D25 -> column 18, 220 ohm resistor 18 -> 21, green LED (long leg 21, short leg 22), black wire 22 -> top minus rail, black wire GND pin -> top minus rail. Close-up from above, landscape, 8-12 s.
- `C6` — two_leds sketch: red and green LEDs blink at different speeds; a press stops/starts the red one while the green keeps going. Landscape, 6-10 s.

Then: `python tools/build.py video/ep04 compose`.

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep04 <VIDEO_ID>

It uploads every `build/ep04_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`
