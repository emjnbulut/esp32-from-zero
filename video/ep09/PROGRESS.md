# Episode 9 - Mini Project 1: a Smart Pedestrian Crossing

Release target: Tuesday 17 November 2026, 17:00 Turkey time. Shorts: TR 18 Nov 17:00, EN 19 Nov 22:00. Curriculum v6.
Creator clips due Sun 15 Nov (shoot pack p07-1: C0 full round, C1 press_time short + long, C2 walk light blinking close-up).

## State (11 November 2026, night)

- [x] Sketches (lessons/09-mini-project-1/code): crossing (lights() helper now uses digitalWrite HIGH/LOW, button vars renamed lastButton so `state` only means the step), press_time (button var `b`, comments "parking ticket"), NEW slow_walker (your-turn solution). All three compile for esp32:esp32:esp32. Behaviour unchanged, so clips filmed with the older pack code are still valid.
- [x] Script make_script.py -> script.json + dub/tr.json: 57 segments, ~1270 words, lint 0 warnings, estimated 9.8 min. New analogies in ANALOGIES.md: washing machine (state), parking ticket (press duration).
- [x] Scenes ep09.js + index.html (crossing simulator `sim()`, crossingIcon, stepLoop, code tours with marks), sketches.js. NOT yet rendered: needs build/schedule.json from the narration. Clip window WIN 1200x675 and EP09_CLIP_SECONDS are placeholders until footage/ep09 exists.
- [x] Short spec video/shorts/ep09/short.json (puzzle: pressed, why still red?), TR on-screen text. Footage crops are placeholders.
- [ ] Narration EN + TR running: `bash video/ep09/build/voice_en_tr.sh` (log build/voice_en_tr.log, resumable via build/rebuild.done).
- [ ] HI/PT/ES dub texts, 7 subtitle languages, make_localize.py, youtube.md, lesson README: given to a Sonnet subagent (check its output: dub length <= 1.0x EN, native first words).

## RESUME HERE

1. When EN narration + schedule0 exist: render stills (`node video/engine/render.mjs ep09 --stills ...`), fix scene overlaps; check every W() anchor resolves.
2. Narrate HI/PT/ES (tools/dub.py ep09 <lang> --report + cbx_retake), dub fit, schedule, render, audio, compose (after clips), dubs, subs, localize, thumbnails A/B, Short EN/TR, package, listening samples for the creator (TR first).
3. Upload: 17 Nov 17:00 video, 18 Nov TR Short 17:00, 19 Nov EN Short 22:00.
