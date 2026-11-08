# Episode 8 - map(), Dimmer Knobs and Level Bars

Release target: Friday 13 November 2026, 17:00 Turkey time. Shorts: TR 14 Nov 17:00, EN 15 Nov 22:00. Curriculum v6.

## State (8 November 2026)

- [x] Script EN + TR subtitle + TR spoken (make_script.py -> script.json, dub/tr.json), 52 segments, lint 0 warnings, estimated 9.3 min.
  Section 9 rule from Episode 7: at most 1-2 spoken numbers per sentence (safe-lock targets are a screen card, not spoken).
  New analogies (ANALOGIES.md): city map = map(), phone battery bars = level bar. Reused: ruler, stove marks, thermometer.
- [x] Sketches compile for esp32:esp32:esp32 (map_dimmer, level_bar, challenge_safe_lock); sketches.js generated.
- [x] Clips in footage/ep08 (gitignored): C0/C2/C3/C4 tall 1080x1200 crops (knob + three LEDs in one frame), C1 16:9. 16:9 versions kept as C*_wide.mp4.
- [x] Scenes ep08.js + index.html written (tall clip window left, drawing/code right).
- [x] s25b (pin 17 is printed TX2) added and narrated in EN + TR.
- [x] HI/PT/ES dub texts (<= 1.0x EN chars), 7 subtitle languages, 12-language metadata (make_localize.py), lesson README.
- [x] Narration: EN, TR (19 TR lines longer than EN: schedule waits, no speed-up), HI, PT done; ES was running when the session closed (8 Nov ~22:45).
- [x] Stills review on the first schedule (28 frames): fixed the map() line overlap and the empty left side after C4 ends.
- [x] Thumbnails ep08_A FILL THE BAR, ep08_B MAP ANY RANGE (video/thumbs/build).
- [x] Short spec video/shorts/ep08/short.json (puzzle: why does the top LED almost never light?). Crops NOT yet checked against final frames.
- [x] Listening samples: build/dinleme/ep08_tr_yeni_terimler.mp3 (mep, levıl bar, TX2, ve işareti) and ep08_en_isaretli.mp3 (flagged EN lines s04, s15, s25b, s28). Creator has not listened yet.

## RESUME HERE

1. `bash tools/rebuild_voices.sh ep08 >> video/ep08/build/rebuild.log 2>&1` (resumable; build/rebuild.done lists the finished steps). Remaining: narrate_es, retake_es, schedule, render, audio, compose, dub_tr/hi/pt/es, subs_dubtimed, localize. Run it with the session active (the idle memory reaper kills background jobs); the GPU ran at a low clock on 8 Nov, so expect ~40 min per dub language.
2. Check frames from build/video.mp4 against the narration (one frame per segment), especially s25-s27 wiring, s39-s42 mistake, and the challenge cards.
3. Short: `tools/production_resume.py` does not know ep08; build with tools/short.py (EN then TR), check crops in frames, make <10 MB copies.
4. Creator listens to the samples (TR first), then package YAYIN/ep08 and upload: long video 13 Nov 17:00, TR Short 14 Nov 17:00, EN Short 15 Nov 22:00. API token expires about 11 Nov: run `publish.py auth` before the subtitles.

## Footage facts (checked in frames, 8 Nov)

- The knob sits at the top of the right board, about 2100 px (upright 4K frame) above the green LED: a 16:9 band cannot hold both, hence the tall crops.
- C0/C3: knob left end + dark at the start, all three on at about 7-10 s (C0) / 6-8 s (C3), back to dark at the end.
- C4: yellow reversed; red + green lit while yellow stays dark at about 4.4-10.2 s.
- Pin 17 is printed TX2 on the creator's board (right header, 9th pin); yellow is on D18.
- Real layout used in the drawing: knob rows 22-26 right board, wiper -> D34 with the long red wire; yellow resistor D18 row -> LED, green resistor TX2 row -> LED, short legs -> minus rail.
