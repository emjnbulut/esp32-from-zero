# Episode 7 - Analog Input, Pin Rules and Debugging with Serial

Release target: Tuesday 10 November 2026, 17:00 Turkey time. Shorts: TR 11 Nov 17:00, EN 12 Nov 22:00. Curriculum v6.

## State (4 November 2026)

- [x] Script EN + TR subtitle + TR spoken (make_script.py -> script.json, dub/tr.json), lint 0 warnings, estimated 10.4 min.
- [x] Sketches compile for esp32:esp32:esp32 (5 of 5); sketches.js generated.
- [x] Clips prepared in footage/ep07 (gitignored): C0 opening, C1 wiring reversed at 2x, C2 meter turned so the digits read.
- [x] HI/PT/ES dubs, 7 subtitle languages, metadata, lesson README (commit 82e9f2d).
- [ ] Narration (`tools/production_resume.py voice ep07`), then schedule. Running since 5 Nov 20:14; resumable.
- [x] Scenes: video/ep07/index.html + ep07.js (5 Nov), one still per segment reviewed. Recheck on the final schedule.
- [x] Thumbnails ep07_A, ep07_B. Short spec + youtube.md in video/shorts/ep07; check its crops once video.mp4 exists.
- [ ] Render, audio, compose, dubs, subtitles; thumbnails A/B; Short (question opening, section 11).
- [ ] Creator listening approval of flagged lines before upload.

## Footage facts (checked in frames, 4 Nov)

- C2's sketch makes the LED follow the knob, so it is pot_dimmer, not pot_read as footage/gelen/ep06/CLIPS.md says. Used in s29. Digits sweep 3.33, 1.51, 0.00, 0.40, 1.72, 2.97, 3.33.
- C1 is mostly hands; only about the last 5 s of the reversed clip show the finished wiring clearly. The animation has to carry the wiring explanation.
- Real layout for the drawing: both boards vertical, USB down, knob on the right board around rows 47-52 below the red LED, black long wire from the knob's middle leg to D34 on the left side of the ESP32, two short wires at rows 59-60 from 3V3 and GND to the rails.
- pot_read and pot_smooth have no clip: recreated Serial Monitor / Plotter scenes.
- pot_zones (s36, C3) was never on the shoot pack: the creator filmed everything asked for Episodes 7-8 on 29 Oct (footage/gelen/ep06). Do not ask for a clip; s36 is an animated LED plus knob. The pot_dimmer clip must not stand in, it dims smoothly and s36 says three clear steps.

## Open question for the creator

Guidelines section 11: bring Episode 5 retention at 0:30-1:30 before this script. On 4 Nov Studio still said "not enough data", so the retrieval minute stays as in Episodes 5-6.
