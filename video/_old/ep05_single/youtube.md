# YouTube upload — Episode 5

## Title
ESP32 PWM & RGB LED: Smooth Fades and Any Color with analogWrite() | ESP32 From Zero #5

## Description
One LED breathes in and out, another mixes any color you want, and a button switches between them. In this lesson you learn how PWM makes an on/off pin dim an LED, use analogWrite() with values from 0 to 255, check the average voltage with a multimeter, build a smooth fade with millis() that never blocks the button, wire an RGB LED with three resistors, write your own setColor() function and cycle color modes with one button. At the end: a challenge for you, the smart camping headlamp.

🔗 Links
• Lesson + all 5 sketches: https://github.com/emjnbulut/esp32-from-zero/tree/main/lessons/05-pwm-and-rgb
• All code + lessons: https://github.com/emjnbulut/esp32-from-zero

⏱ Chapters
0:00 Fade it, mix it (demo)
0:28 What you need
0:42 PWM: on and off, fast
1:42 analogWrite() and the multimeter
3:22 A fade that never waits
6:16 The RGB LED and its wiring
7:35 setColor() and mixing light
9:30 One button, four color modes
11:26 Your turn: the camping headlamp
11:55 Troubleshooting
12:12 Recap and next episode

🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
🎙 Narration: Chatterbox TTS (Resemble AI, MIT). Voice references: LibriVox (public domain) and FLEURS by Google (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #PWM #RGB #LED #Electronics

## Creator clips (footage/ep05/)
- `C0` — OPENING, full screen, 14-16 s: the red LED breathing (fade_millis) and the RGB LED changing colour (color_modes in mode 3, then ~8 s in one press to the next mode). Landscape, steady, both LEDs and the button in frame; the RGB LED in the CENTRE (the Short crops a square from the middle).
- `C1` — MULTIMETER, hands-free, 8-10 s: pwm_levels running; probes on the red LED's GPIO 23 strip and the minus rail (DC volts). The reading steps 0 -> ~0.8 -> ~1.65 -> ~3.3 V while the LED gets brighter. Meter display readable.
- `C2` — fade_millis, full screen, 6-8 s: the red LED breathes; one press pauses it mid-fade, another press resumes.
- `C3` — USB unplugged, close-up from above, 8-12 s: green LED off the upper breadboard; RGB LED in (longest leg second from the left), black wire long leg -> minus rail, three 220 ohm resistors + wires to D25 (red), D26 (green), D27 (blue). Exact columns: see the lesson README drawing.
- `C4` — rgb_colors, full screen, 8 s: the RGB LED steps red, green, blue, yellow, magenta, cyan, white, orange. Slightly dim room so the colours are clear.
- `C5` — color_modes, full screen, 8 s: three presses (red -> green -> blue -> fade), the fade starts.
- `NOTE` — Before filming: upload rgb_colors once. If you see white when it should be off, the RGB LED is common anode: move its long leg to 3V3 and set COMMON_ANODE = true in all three RGB sketches; tell Claude so the drawing and narration can be adjusted.

Then: `python tools/build.py video/ep05 compose`.

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep05 <VIDEO_ID>

It uploads every `build/ep05_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`
