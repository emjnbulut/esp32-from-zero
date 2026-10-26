# YouTube upload — Episode 4

## Title
ESP32 Buttons & millis(): Blink LEDs Without Blocking | ESP32 From Zero #4

## Description
Press a button and one LED stops at once, while the other keeps blinking at its own speed. In this lesson you build that yourself: wire a push button on two breadboards, learn why floating pins misbehave and how INPUT_PULLUP fixes them, read the button with digitalRead, catch the edge of a press, tame button bounce, see why delay() freezes everything, and use millis() to do two things at once. At the end there is a challenge for you: the speed-shifter.

🔗 Links
• Lesson + all 5 sketches: https://github.com/emjnbulut/esp32-from-zero/tree/main/lessons/04-buttons-and-millis
• All code + lessons: https://github.com/emjnbulut/esp32-from-zero

⏱ Chapters
0:00 Two things at once (demo)
0:29 What you need
0:42 The push button
1:05 Two breadboards and the wiring
2:10 Floating pins and pull-ups
3:19 The code, line by line
4:13 Upload and Serial Monitor
4:55 Toggle: catching the edge
6:29 Bounce and debounce
7:12 Why delay() gets in the way
7:56 millis(): check the clock
9:39 A second LED
10:49 Your turn: the speed-shifter
11:15 Troubleshooting
11:36 Recap and next episode

🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
🎙 Narration: Chatterbox TTS (Resemble AI, MIT). Voice references: LibriVox (public domain) and FLEURS by Google (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Button #millis #Electronics #Microcontroller

## Creator clips (footage/ep04/)
- `C0` — OPENING, full screen (same take can serve C7): finished two_leds circuit on the two breadboards, USB plugged in. Red blinks every 0.5 s, green blinks fast; after ~3 s a finger presses the button once (red stops at once, green keeps going), ~2 s later presses again (red starts again). Landscape, steady, both LEDs + button clearly in frame, 10-12 s.
- `C1` — USB unplugged. Two breadboards one above the other, the ESP32 across both (top pins in the upper breadboard's row j, bottom pins in the lower one's row a). Rebuild the red LED circuit on the lower breadboard as in the drawing. Top view, landscape, 8-12 s.
- `C2` — USB unplugged. Press the button into the lower breadboard across the middle gap (columns 25-27), then the yellow wire (D22 -> button left side) and the black wire (button right side -> minus rail). Close-up from above, landscape, 6-10 s.
- `C3` — button_led sketch, full screen: a finger presses and holds the button - the LED lights while it's held, goes dark on release (twice). Landscape, 5-8 s.
- `C4` — button_toggle sketch, full screen: press, LED on; press again, LED off (three or four presses). Landscape, 6-8 s.
- `C5` — blink_button sketch, full screen: the LED blinks; one press stops it at once, another press starts it again. Landscape, 6-10 s.
- `C6` — USB unplugged. Upper breadboard: green wire D25 -> column 18, 220 ohm resistor 18 -> 21, green LED (long leg 21, short leg 22), black wire 22 -> top minus rail, black wire GND pin -> top minus rail. Close-up from above, landscape, 8-12 s.
- `C7` — two_leds sketch, full screen: red and green blink at their own speeds; a press stops the red one while the green keeps going, another press starts red again. Landscape, 8-10 s (may be the same take as C0).

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
