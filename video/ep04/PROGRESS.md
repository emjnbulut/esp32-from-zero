# Episode 4 — "Buttons and Doing Two Things at Once" — progress

Resume rule: do the first unchecked step; commands are run from the repo root.
Two curriculum topics in one episode (user 2026-10-17), target 10-15 min.

- [x] 1. Script (EN + tr) `video/ep04/make_script.py` → `script.json` (56 segments, ~1415 words, preview 10:08 + intro/outro);
      sketches in `lessons/04-buttons-and-millis/code/` (button_led, button_toggle, blink_button, two_leds, challenge_speed — all compile)
- [x] 2. Scenes `video/ep04/ep04.js` (index.html done) + review stills
- [x] 3. Lesson README `lessons/04-buttons-and-millis/README.md`
- [ ] 4. Dub texts `dub/{tr,hi,pt,es}.json` (make_dubs.py), subtitle texts `subs/{id,ar,ru,de,fr,vi,ja}.json` (make_subs.py), make_localize.py (localize.json + youtube.md done)
- [ ] 5. Preview render + frame review; Short spec `video/shorts/ep04/short.json`
- ON HOLD until Chatterbox (2026-10-18): final narration, render, audio/subs/compose, dubs (see tools/CHATTERBOX.md)

## Notes
- Breadboard: ep03 circuit kept (red wire j16 → + rail, resistor + rail col 20 → h20, red LED f20/f21, black j21 → −, black j3 → −).
  Button straddles the gap at cols 25/27 (legs e25 e27 f25 f27); yellow wire j15 (D22) → j25; black j27 → − rail.
  Green LED (top half): green wire a9 (D25) → a18, resistor b18 → b21, LED d21 (long) / d22, black a22 → top − rail (tm), black a3 (GND, top row) → tm.
- Clips C1-C6 listed in script.json.
