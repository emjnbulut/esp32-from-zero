# YouTube upload — Recap (episodes 1-4: how to read a sketch)

Numberless special, scheduled Fri 30 Oct 2026 17:00 (video/YAYIN_TAKVIMI.md). Not a numbered episode, so no "#N" in the title.
Thumbnail: video/thumbs/build/recap_A.png ("READ ANY SKETCH", Claude's choice, user 2026-10-25 rule).
AI label: own-voice clone narration, no realistic synthetic people or events -> "No" (PRODUCTION_GUIDELINES.md).

## Title
How to Read ESP32 Code: Variables, setup() and loop() Explained | ESP32 From Zero Recap

## Description
Code still confusing? In this recap we go through all five sketches from episodes 1 to 4 and watch every variable change, line by line. You learn the three parts every sketch has (names, setup, loop), why a variable is the sketch's memory, how a button press is detected with lastState, and how millis() lets a sketch blink and read a button at the same time. Then three quick practice questions to test yourself.

🔗 Links
• All lessons + sketches: https://github.com/emjnbulut/esp32-from-zero/tree/main/lessons
• All code: https://github.com/emjnbulut/esp32-from-zero

⏱ Chapters
0:00 Five sketches (demo)
0:33 The skeleton: names, setup, loop
4:41 Outputs: pinMode and digitalWrite
7:03 Decisions: digitalRead and if
10:36 Memory: lastState and presses
14:01 The clock: millis()
17:02 The four questions
17:52 Your turn: three quick ones
19:27 Recap and next episode

🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
🎙 Narration: Chatterbox TTS (Resemble AI, MIT). Voice references: LibriVox (public domain) and FLEURS by Google (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Programming #Electronics #Beginners

## Footage used (reused, footage/recap1/)
- `C1` — REUSED from episode 3 (footage/ep03/C2.mp4): the LED blinking once per second.
- `C2` — REUSED from episode 4 (footage/ep04/C3.mp4): button_led, the LED lights while the button is held.
- `C3` — REUSED from episode 4 (footage/ep04/C4.mp4): button_toggle, press on, press off.
- `C4` — REUSED from episode 4 (footage/ep04/C5.mp4): blink_button, the LED blinks; a press stops it.

## Files
- English video: `build/recap1_final.mp4`
- Subtitles: `build/recap1_en.srt`, `build/recap1_tr.srt`
- Turkish dub (audio track + video): `build/dub_tr.m4a`, `build/recap1_tr_dub.mp4`
- Titles/descriptions per language: `localize.json` (en, tr). After the upload: `python tools/publish.py video/recap1 <VIDEO_ID>`
