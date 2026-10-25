# Episode 4 — "Buttons and Doing Two Things at Once" — progress (v2)

Resume rule: do the first unchecked step; commands are run from the repo root.
v2 (2026-10-25) rebuilds the episode to video/PRODUCTION_GUIDELINES.md: cold open with the real result,
the channel sting after the cold open (script.json "sting_after"), big 3-6 line code cards, code -> pin -> LED
cause and effect, if/else before `!` and `?:`, four quick questions, a millis() timeline, full-screen real results,
the "speed-shifter" challenge (solution comes as a Short). Hardware (user, 2026-10-25): TWO breadboards one above
the other, the board across both (top pins upper row j, bottom pins lower row a); red LED GPIO 23 + button GPIO 22
on the lower one, green LED GPIO 25 on the upper one.

- [x] 1. Engine: makeBB2 (two breadboards), bbBoard rows, green bbLED, bigCode, quizCard, full-frame heroClip,
      cold-open sting (tools/bumpers.py cut/shift, build.py compose/subs, rechapter.py), script "lead_in"
- [x] 2. Script v2 `make_script.py` (63 segments, ~1640 words)
- [x] 3. Translations: dub/{tr,hi,pt,es}.json, subs/*.json, make_localize.py (Sonnet subagent; TR dub had 34 lines
      longer than the subtitle text, mostly spelled numbers: check dub --report ratios)
- [x] 4. Scenes `ep04.js` v2 (first draft)
- [x] 5. Lesson README + two_leds comment for two breadboards
- [x] 6. EN narration (tts.py + cbx_retake.py en) -> schedule; re-run tts for s10 (text changed after the run began)
- [x] 7. Stills review (render.mjs ep04 --stills ...) and scene fixes; grep render log for "word not found"
- [x] 8. Dubs (2026-10-26 night, creator's own voice in every language, DeepFilterNet clean-up): was ON HOLD (user 2026-10-25: English only for now). Old dub caches parked in build/_dubs_parked; when dubs resume: dub.py --report per language, cbx_retake, schedule (stretches), re-render
- [x] 9. Full render, audio, compose (clips missing -> placeholders), dubs tr/hi/pt/es, subs (dub languages timed by their own dub words), make_localize.py — 2026-10-26 02:55, final 12:47 (body 743.5 s, +63 s stretched for dubs; es/pt base tempo 1.15/1.12)
- [x] 10. Short spec (built after the full render) (video/shorts/ep04/short.json): one question "Why does your button stop responding during delay()?"
- [ ] 12. Challenge solution Short (speed-shifter, challenge_speed.ino): spec + build once C8 is filmed
- [ ] 11. Creator clips C0-C7 (see script.json "clips"), then compose again

Thumbnail: ep04_D "DO BOTH!" (user, 2026-10-25) -> video/thumbs/build/ep04_D.png

## Clips (creator)
C0 opening (full screen, 14-16 s, press ~8 s and ~11 s), C1 two breadboards + red circuit, C2 button wiring,
C3 button_led, C4 button_toggle, C5 blink_button, C6 green LED wiring, C7 two_leds (may be the C0 take).
C8 (for the challenge solution Short): challenge_speed running, red steady 500 ms, each press switches green fast <-> slow, 8-10 s.
The drawing assumes the layout above; after C1 arrives, align the drawing with the real breadboards if needed.
