# Recap 2 - episodes 5-10

Release target: Tuesday 24 November 2026, 17:00 Turkey time (video/YAYIN_TAKVIMI.md). Recap rule: at most 12 minutes.
Work order (creator, 14 Nov): Ep9 -> Ep9 Shorts -> Ep10 -> Recap 2. Started 14 Nov while Ep9/Ep10 wait for the clips.

## State (14 November 2026)

- [x] Script make_script.py -> script.json + dub/tr.json: 41 segments, 949 words, lint 0 warnings, ~7.3 min.
  Three parts (light / knob / steps), each analogy from ANALOGIES.md, 3 live traces with a memory panel,
  7 scored questions (episode shown per question), one "in your own words", score table at the end.
- [x] Scenes recap2.js + index.html (helpers copied from ep10.js). NOT rendered yet (needs build/schedule.json).
- [x] Montage footage/recap2/M.mp4 (8.8 s: ep05 C0, ep06 C2, ep07 C0, ep08 C0_wide). ADD ep09 C0 + ep10 C0 when they
  exist (then set CLIP_SECONDS.M in recap2.js).
- [ ] Narration EN + TR running: `bash video/recap2/build/voice_en_tr.sh`, then `bash video/recap2/build/voices_all.sh`.
- [ ] HI/PT/ES dub texts, subs, localize, youtube.md: given to a Sonnet subagent (check: ratio, no shifted lines).
- [ ] Stills review, dub fit, TR term scan, thumbnails (recap2_A/B), render, compose, package YAYIN/recap2.
