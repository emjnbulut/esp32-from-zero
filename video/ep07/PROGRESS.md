# Episode 7 - Analog Input, Pin Rules and Debugging with Serial

Release target: Tuesday 10 November 2026, 17:00 Turkey time. Shorts: TR 11 Nov 17:00, EN 12 Nov 22:00. Curriculum v6.

## State (4 November 2026)

- [x] Script EN + TR subtitle + TR spoken (make_script.py -> script.json, dub/tr.json), lint 0 warnings, estimated 10.4 min.
- [x] Sketches compile for esp32:esp32:esp32 (5 of 5); sketches.js generated.
- [x] Clips prepared in footage/ep07 (gitignored): C0 opening, C1 wiring reversed at 2x, C2 meter turned so the digits read.
- [x] HI/PT/ES dubs, 7 subtitle languages, metadata, lesson README (commit 82e9f2d).
- [x] Narration and schedule (6 Nov). First full narration ran to 760 s because HI/PT/ES takes were 63-99 s longer than EN/TR; 110 + 11 dub lines were shortened from measured take lengths and re-narrated (no speed-up). Final timeline 652.9 s body, 676.4 s with bumpers; anchors 0 problems.
- [x] Scenes rechecked on the final schedule from video.mp4 (one frame per segment). Fixed: s12 answer card now leaves before the knob moves; wiper label no longer overlaps the 3.3 V label at the top.
- [x] Thumbnails ep07_A, ep07_B.
- [x] Render, audio, compose, 4 dubs, 12 subtitle languages, verification.json, review frames; packaged in YAYIN/ep07.
- [x] Shorts EN 37.6 s / TR 35.7 s. Crops checked in frames: h1/h2 use wide crops without pan; h2 runs slower (EN 0.72, TR 0.77 via `by_lang`) so "around 2000" lands with the knob in the middle.
- [x] Creator listening approval (2026-11-07): all 5 samples + TR flagged lines approved by ear. Future scripts: no stacked numbers/acronyms (guidelines sec. 9).
- [ ] Upload: long video 10 Nov 17:00, TR Short 11 Nov 17:00, EN Short 12 Nov 22:00.

## Footage facts (checked in frames, 4 Nov)

- C2's sketch makes the LED follow the knob, so it is pot_dimmer, not pot_read as footage/gelen/ep06/CLIPS.md says. Used in s29. Digits sweep 3.33, 1.51, 0.00, 0.40, 1.72, 2.97, 3.33.
- C1 is mostly hands; only about the last 5 s of the reversed clip show the finished wiring clearly. The animation has to carry the wiring explanation.
- Real layout for the drawing: both boards vertical, USB down, knob on the right board around rows 47-52 below the red LED, black long wire from the knob's middle leg to D34 on the left side of the ESP32, two short wires at rows 59-60 from 3V3 and GND to the rails.
- pot_read and pot_smooth have no clip: recreated Serial Monitor / Plotter scenes.
- pot_zones (s36, C3) was never on the shoot pack: the creator filmed everything asked for Episodes 7-8 on 29 Oct (footage/gelen/ep06). Do not ask for a clip; s36 is an animated LED plus knob. The pot_dimmer clip must not stand in, it dims smoothly and s36 says three clear steps.

## Open question for the creator

Guidelines section 11: bring Episode 5 retention at 0:30-1:30 before this script. On 4 Nov Studio still said "not enough data", so the retrieval minute stays as in Episodes 5-6.
