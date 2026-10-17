# Episode 3 — "Your First Circuit: Blink an LED" — progress

Resume rule: do the first unchecked step; commands are run from the repo root.

- [x] 1. Script (EN + tr) in `video/ep03/make_script.py` → `script.json`; lesson `lessons/03-blink-an-led/README.md`; creator clip plan
- [ ] 2. Scenes `video/ep03/ep03.js` + `index.html`; review stills (`node video/engine/render.mjs ep03 --stills ...` from `video/`)
- [ ] 3. `python tools/tts.py video/ep03` → `python tools/build.py video/ep03 schedule` → full render (`cd video && node engine/render.mjs ep03`) → `build.py video/ep03 audio` / `subs` / `compose`
- [ ] 4. Dubs `video/ep03/dub/{tr,hi,pt,es}.json` → `python tools/dub.py video/ep03 <lang>` (no segment > ~1.18x); subs `video/ep03/subs/{id,ar,ru,de,fr,vi,ja}.json`; `make_localize.py` → `localize.json` + `youtube.md`

## Notes
- Continues ep02: the always-on LED (3V3 → 220 Ω → LED → GND). We move the 3V3 wire to GPIO 23 (a "safe" pin in ep02) and blink it from code.
- No Shorts for ep03 (main session does those).
- Step 1 done: 30 segments / 649 words; sketch compiles (arduino-cli, esp32:esp32:esp32: 271672 bytes, 22116 globals) — use these numbers in the upload log.
- Breadboard layout = ep02 build scene: 30-pin board at column 2 (bottom row i: 3V3=col 2, GND=col 3, D23=col 16); red wire j2 → + rail; resistor + rail col 20 → h20; LED f20 (long) / f21; black wires j3 → −, j21 → −. ep03 moves the red wire's pin end from j2 to j16.
- Clips: C1 move the wire (s10), C2 LED blinking (s23), C3 fast blink (s26).
