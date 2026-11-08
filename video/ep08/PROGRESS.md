# Episode 8 - map(), Dimmer Knobs and Level Bars

Release target: Friday 13 November 2026, 17:00 Turkey time. Shorts: TR 14 Nov 17:00, EN 15 Nov 22:00. Curriculum v6.

## State (8 November 2026)

- [x] Script EN + TR subtitle + TR spoken (make_script.py -> script.json, dub/tr.json), 52 segments, lint 0 warnings, estimated 9.3 min.
  Section 9 rule from Episode 7: at most 1-2 spoken numbers per sentence (safe-lock targets are a screen card, not spoken).
  New analogies (ANALOGIES.md): city map = map(), phone battery bars = level bar. Reused: ruler, stove marks, thermometer.
- [x] Sketches compile for esp32:esp32:esp32 (map_dimmer, level_bar, challenge_safe_lock); sketches.js generated.
- [x] Clips in footage/ep08 (gitignored): C0/C2/C3/C4 tall 1080x1200 crops (knob + three LEDs in one frame), C1 16:9. 16:9 versions kept as C*_wide.mp4.
- [x] Scenes ep08.js + index.html written (tall clip window left, drawing/code right).
- [ ] s25b (pin 17 is printed TX2) added after the first EN/TR narration: rerun tts/retake for it.
- [ ] HI/PT/ES dubs, 7 subtitle languages, lesson README (Sonnet agent).
- [ ] EN + TR narration, then HI/PT/ES narration, schedule, stills review, render, compose, dubs, subs, localize, thumbnails, Shorts.

## Footage facts (checked in frames, 8 Nov)

- The knob sits at the top of the right board, about 2100 px (upright 4K frame) above the green LED: a 16:9 band cannot hold both, hence the tall crops.
- C0/C3: knob left end + dark at the start, all three on at about 7-10 s (C0) / 6-8 s (C3), back to dark at the end.
- C4: yellow reversed; red + green lit while yellow stays dark at about 4.4-10.2 s.
- Pin 17 is printed TX2 on the creator's board (right header, 9th pin); yellow is on D18.
- Real layout used in the drawing: knob rows 22-26 right board, wiper -> D34 with the long red wire; yellow resistor D18 row -> LED, green resistor TX2 row -> LED, short legs -> minus rail.
