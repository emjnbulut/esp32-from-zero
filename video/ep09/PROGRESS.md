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

## State (12 November 2026, ~01:00, session closed by the creator)

- [x] Narration done in all 5 languages (EN + retakes, TR/HI/PT/ES + retakes; build/voices_all.sh, log build/voices_all.log). Memory reaper killed the chain twice; resumed fine.
- [x] Scenes rendered as stills with the EN timing, 5 layout fixes done (commit c0a1f24).
- [x] HI/PT/ES dub texts, 7 subtitle languages, localize, youtube.md, lesson README (commit 731a09c).
- [ ] DUB FIT: schedule with dubs stretches +115.5 s (overrun beyond max(EN,TR) x 1.05: HI 62 s, ES 55 s, PT 32 s; TR alone 31.6 s = accepted, priority track). Targets per line in video/ep09/fit_targets.json (hi 35, pt 33, es 38 lines; max_chars = chars x slot/dur x 0.95). The shortening agent was stopped before it wrote anything: make_dubs.py is unchanged.
- [ ] TR term check: tools/tr_lowprob_scan.py video/ep09 tr (Whisper small, words with probability < 0.5). Suspicious lines to retake with more seeds (6 seeds 41-46, pick best, like ep08 11 Nov): s18 ("steyte" -> "Tt"), s20 + s42 ("İşte, skeç" -> "de sketch"), s21 ("beş ışığın"), s23, s27 ("İki ve işareti" -> "tibe"), s31 ("çeyrek", "hilesiyle"), s38, s41 ("Biletten"), s43. The retake run was stopped before it finished.

## State (12 November 2026, afternoon)

- [x] Dub fit pass 1: 106 HI/PT/ES lines shortened to fit_targets.json max_chars (hi 35, pt 33, es 38), make_dubs.py + make_subs.py rerun. hi s14 and pt s53 kept their key clause ("wait without stopping", "solution in the folder").
- [ ] TR retakes running: `tools/cbx_fixline.py video/ep09 tr s18,s20,s21,s23,s27,s31,s38,s41,s42,s43 41,...,46` (log build/tr_fixline.log), then dub.py tr, then voices_all.sh re-narrates HI/PT/ES (narrate/retake hi/pt/es removed from rebuild.done).

## RESUME HERE

1. Shorten the HI/PT/ES lines in make_dubs.py to their max_chars (fit_targets.json), run make_dubs.py + make_subs.py, then `bash video/ep09/build/voices_all.sh` after removing narrate_hi/pt/es + retake_hi/pt/es from build/rebuild.done (dub.py only re-narrates changed lines). Re-measure; second pass if stretch is still > ~30 s.
2. TR retakes for the lines above (6 seeds each, pick by match + word probability), then `tools/tr_lowprob_scan.py` again; listening file YAYIN/ep09/dinleme/ep09_tr_yeni_terimler.mp3 for the creator (steyt, go tu, layts, krosing, pres start, pres taym, dilay, milis).
3. `tools/build.py video/ep09 schedule`, full render, audio, stills review on the final schedule.
4. When clips arrive (due Sun 15 Nov): prepare footage/ep09/C0-C2 (16:9, set EP09_CLIP_SECONDS + WIN in ep09.js, Short crops in video/shorts/ep09/short.json), compose, dubs, subs, localize, thumbnails A/B, Shorts EN/TR (Turkish on-screen text), package YAYIN/ep09, listening samples.
5. Upload: 17 Nov 17:00 video, 18 Nov TR Short 17:00, 19 Nov EN Short 22:00.
