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

## State (9 November 2026, ~22:30)

- [x] Dub fit: first schedule stretched +107 s (HI +44, ES +49, PT +11, TR alone +20). Two passes shortened 71 + 14 HI/PT/ES lines (commits 7c87451, 78a395f); ES/PT s25b spell "te equis dos" / "tê xis dois". Stretch now +24.5 s, mostly TR (accepted, TR is a priority track). Body 569.2 s, final with bumpers 592.7 s.
- [x] Render, audio, compose (clips C0-C4 in place, checked in frames), dub_tr/hi/pt/es mp4 + m4a, 12 SRTs, localize (chapters from final schedule).
- [x] Frames checked: one per segment (scratchpad sheets) + composed clip moments; nothing to fix.
- dub.py "sped up more than 1.03" warnings on 10 lines are exactly 1.03x (the designed DUB_FIT ceiling), not real speed-ups.
- Known: ES s25b, Whisper hears "de quiz dos" for "te equis dos"; on-screen says TX2.

## RESUME HERE

- [x] Short EN 40.9 s / TR 43.5 s built, frames checked, under-10 MB copies; Short titles/descriptions in video/shorts/ep08/youtube.md (add the Episode 8 youtu.be link after upload).
- [x] YAYIN/ep08 packaged (production_resume.py package ep08): video, 12 descriptions, 12 SRTs, 4 dubs + upload_10mb, thumbnails A/B, shorts/, dinleme/.

1. Creator listens to YAYIN/ep08/dinleme (TR first: ep08_tr_yeni_terimler, ep08_tr_dub_270-330, ep08_short_tr_son = "Devreyi kurun" check; EN: ep08_en_isaretli).
4. Upload: long video 13 Nov 17:00, TR Short 14 Nov 17:00, EN Short 15 Nov 22:00. API token expires about 11 Nov: run `publish.py auth` before the subtitles.

## Footage facts (checked in frames, 8 Nov)

- The knob sits at the top of the right board, about 2100 px (upright 4K frame) above the green LED: a 16:9 band cannot hold both, hence the tall crops.
- C0/C3: knob left end + dark at the start, all three on at about 7-10 s (C0) / 6-8 s (C3), back to dark at the end.
- C4: yellow reversed; red + green lit while yellow stays dark at about 4.4-10.2 s.
- Pin 17 is printed TX2 on the creator's board (right header, 9th pin); yellow is on D18.
- Real layout used in the drawing: knob rows 22-26 right board, wiper -> D34 with the long red wire; yellow resistor D18 row -> LED, green resistor TX2 row -> LED, short legs -> minus rail.

## 11 November 2026
- Creator heard problems in ep08_tr_yeni_terimler (50-55 s = s30/s33, 65-70 s = s34, small ones elsewhere). New TR takes (seeds 41-46, text variants) in build/dub_tr/retakes; picks: s01 v0_43, s10 v0_41, s16 v0_43, s25b v0_43, s30 v0_41, s33 v1_42 (text "İşte, skeç: levıl bar. Setap, üç pini..."), s34 v0_43. Listening file YAYIN/ep08/dinleme/ep08_tr_yeni_terimler_v2.mp3. NOT yet copied into dub_tr: waiting for the creator's OK (then copy picks, update dub/tr.json s33 + cache keys/durations, rerun dub.py ep08 tr, repackage).
- New rule (creator): TR-dub Shorts get Turkish on-screen text. Ep8 TR Short rebuilt with Turkish chip/headline/captions/CTA (short.json), frames checked, copied to YAYIN/ep08/shorts (+ upload_10mb).
