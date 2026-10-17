# Episode 3 — "Your First Circuit: Blink an LED" — progress

Resume rule: do the first unchecked step; commands are run from the repo root.

- [ ] 1. Script (EN + tr) in `video/ep03/make_script.py` → `script.json`; lesson `lessons/03-blink-an-led/README.md`; creator clip plan
- [ ] 2. Scenes `video/ep03/ep03.js` + `index.html`; review stills (`node video/engine/render.mjs ep03 --stills ...` from `video/`)
- [ ] 3. `python tools/tts.py video/ep03` → `python tools/build.py video/ep03 schedule` → full render (`cd video && node engine/render.mjs ep03`) → `build.py video/ep03 audio` / `subs` / `compose`
- [ ] 4. Dubs `video/ep03/dub/{tr,hi,pt,es}.json` → `python tools/dub.py video/ep03 <lang>` (no segment > ~1.18x); subs `video/ep03/subs/{id,ar,ru,de,fr,vi,ja}.json`; `make_localize.py` → `localize.json` + `youtube.md`

## Notes
- Continues ep02: the always-on LED (3V3 → 220 Ω → LED → GND). We move the 3V3 wire to GPIO 23 (a "safe" pin in ep02) and blink it from code.
- No Shorts for ep03 (main session does those).
