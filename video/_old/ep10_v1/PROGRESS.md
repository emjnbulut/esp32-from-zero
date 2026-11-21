# Episode 10 - Mini Project 1: a Reflex Game with a Record that Survives Power Off

Release target: Friday 20 November 2026, 17:00 Turkey time. Shorts: TR 21 Nov 17:00, EN 22 Nov 22:00.
Project 1 homework solution Short (false start): TR 23 Nov 17:00, EN 24 Nov 22:00. Curriculum v6.
Creator clips: shoot pack p07-2 (C0 fast round -> RGB green, C1 slow press -> RGB red, C2 USB unplug/replug).
Work order (creator, 14 Nov): Ep9 -> Ep9 Shorts -> Ep10 -> Recap 2.

## State (14 November 2026, night)

- [x] Sketches (lessons/10-reflex-game/code): reflex_game + challenge_false_start rewritten in the episode 9 style
  (lastButton, goTo(), lights(HIGH/LOW...)); behaviour unchanged so the p07-2 clips stay valid. Both compile.
- [x] Script make_script.py -> script.json + dub/tr.json: 53 segments, 1110 words, lint 0 warnings, ~8.7 min.
  New analogy: notebook in the drawer (Preferences), in video/ANALOGIES.md.
- [x] Scenes ep10.js + index.html + sketches.js written (syntax OK); NOT rendered yet (needs build/schedule.json).
- [x] Narration in all 5 languages; dub-fit pass 1 (28 lines, fit_targets.json) -> stretch +31.8 s (TR alone 21.9 s),
  accepted. Schedule 536.9 s = 8:57, audio done. Stills reviewed (3 layout fixes, commit a2f1531).
- [x] HI/PT/ES dub texts (mean 0.75x EN), 7 subtitle languages, make_localize.py (provisional chapters: rerun after the
  final schedule), youtube.md, lesson README (commit 52d9eee).
- [x] Thumbnails ep10_A (beat my time) / ep10_B (unplug it, record stays) EN + tr/hi/pt/es.
- [x] Short specs: video/shorts/ep10 (beat 200 ms / where does the record hide) and video/shorts/ep10c (false-start
  solution; needs creator clip C3, added to the shoot pack 14 Nov, + code-card clips C3_code1-3 rendered by us).
- [ ] Shorts EN/TR (Turkish on-screen text) + the false-start solution Short.

## RESUME HERE (14 Nov, ~08:00)

1. TR term check: `tools/tr_lowprob_scan.py video/ep10 tr`, retake bad lines (cbx_fixline.py, 6 seeds), dub.py tr.
2. When clips arrive (p07-2: C0-C3): footage/ep10 (16:9), EP10_CLIP_SECONDS + WIN in ep10.js, full render, compose,
   dubs, subs, rerun make_localize.py on the final schedule, package YAYIN/ep10, Shorts ep10 EN/TR + ep10c.
3. Upload: 20 Nov 17:00 video, 21 Nov TR Short, 22 Nov EN Short; solution Short 23/24 Nov.
