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
- [ ] Narration EN + TR running: `bash video/ep10/build/voice_en_tr.sh` (log build/voice_en_tr.log, resumable), then
  `bash video/ep10/build/voices_all.sh` for HI/PT/ES.
- [x] HI/PT/ES dub texts (mean 0.75x EN), 7 subtitle languages, make_localize.py (provisional chapters: rerun after the
  final schedule), youtube.md, lesson README (commit 52d9eee).
- [x] Thumbnails ep10_A (beat my time) / ep10_B (unplug it, record stays) EN + tr/hi/pt/es.
- [x] Short specs: video/shorts/ep10 (beat 200 ms / where does the record hide) and video/shorts/ep10c (false-start
  solution; needs creator clip C3, added to the shoot pack 14 Nov, + code-card clips C3_code1-3 rendered by us).
- [ ] Dub fit from measured takes (lesson from ep07/ep09: Chatterbox HI/PT/ES run far longer than the char ratio).
- [ ] Shorts EN/TR (Turkish on-screen text) + the false-start solution Short.
