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
- [ ] Scenes ep10.js + index.html + sketches.js (copy the ep09 engine use: code tours, sim of the 3 lights + RGB,
  drawer/desk animation, mistake animation, Serial Monitor "record: N" after replug).
- [ ] Narration EN + TR (voice_en_tr.sh like ep09), then HI/PT/ES dub texts (make_dubs.py, length <= EN), 7 subtitle
  languages (make_subs.py), make_localize.py, youtube.md, lesson README (all sketches in full).
- [ ] Dub fit from measured takes (lesson from ep07/ep09: Chatterbox HI/PT/ES run far longer than the char ratio).
- [ ] Shorts EN/TR (Turkish on-screen text) + the false-start solution Short.
