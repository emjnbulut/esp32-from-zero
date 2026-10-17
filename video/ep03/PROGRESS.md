# Episode 3 — "Your First Circuit: Blink an LED" — progress

Resume rule: do the first unchecked step; commands are run from the repo root.

- [x] 1. Script (EN + tr) in `video/ep03/make_script.py` → `script.json`; lesson `lessons/03-blink-an-led/README.md`; creator clip plan
- [x] 2. Scenes `video/ep03/ep03.js` + `index.html`; review stills (`node video/engine/render.mjs ep03 --stills ...` from `video/`)
- [ ] 3. `python tools/tts.py video/ep03` → `python tools/build.py video/ep03 schedule` → full render (`cd video && node engine/render.mjs ep03`) → `build.py video/ep03 audio` / `subs` / `compose`
- [ ] 4. Dubs `video/ep03/dub/{tr,hi,pt,es}.json` → `python tools/dub.py video/ep03 <lang>` (no segment > ~1.18x); subs `video/ep03/subs/{id,ar,ru,de,fr,vi,ja}.json`; `make_localize.py` → `localize.json` + `youtube.md`

## Notes
- Continues ep02: the always-on LED (3V3 → 220 Ω → LED → GND). We move the 3V3 wire to GPIO 23 (a "safe" pin in ep02) and blink it from code.
- No Shorts for ep03 (main session does those).
- Step 1 done: 30 segments / 649 words; sketch compiles (arduino-cli, esp32:esp32:esp32: 271672 bytes, 22116 globals) — use these numbers in the upload log.
- Breadboard layout = ep02 build scene: 30-pin board at column 2 (bottom row i: 3V3=col 2, GND=col 3, D23=col 16); red wire j2 → + rail; resistor + rail col 20 → h20; LED f20 (long) / f21; black wires j3 → −, j21 → −. ep03 moves the red wire's pin end from j2 to j16.
- Clips: C1 move the wire (s10), C2 LED blinking (s23), C3 fast blink (s26).
- Step 2 done: scenes reviewed with stills (narration 5:02 + intro/outro). Shared breadboard drawing moved to video/engine/breadboard.js (copied from ep02.js; ep02 untouched). tts + schedule already ran.

## Status 2026-10-17 18:33 (session closing)
- Done: steps 1-2; dub texts `dub/{tr,hi,pt,es}.json` (tr written by hand, phonetic; others from `make_dubs.py`);
  subtitle texts `subs/{id,ar,ru,de,fr,vi,ja}.json` (from `make_subs.py`). Not yet reviewed by native speakers.
- In progress: full picture render was running (`cd video && node engine/render.mjs ep03`, ~60% done at 18:32).
  It may not have finished — check that `video/ep03/build/video.mp4` exists and is ~5:01 long; if not, rerun it.
- NEXT (step 3, then 4), from the repo root:
  1. `cd video && node engine/render.mjs ep03` (only if build/video.mp4 is missing/short), then `cd ..`
  2. `python tools/build.py video/ep03 audio` → `subs` → `compose` (compose adds the channel intro/outro)
  3. `python tools/dub.py video/ep03 tr` (then hi, pt, es) — fix any line flagged "shorten" / sped up > ~1.18x
  4. Write `video/ep03/make_localize.py` (copy ep02's: TIMES_BODY from the schedule + INTRO 3.5 s, CREDIT line,
     12-language titles/descriptions, creator clip list C1-C3 from script.json) → `localize.json` + `youtube.md`
  5. Check stills/contact sheet of the final, commit + push.
- No Shorts for ep03 (main session decides later).
