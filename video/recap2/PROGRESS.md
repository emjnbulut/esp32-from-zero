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
- [x] Narration in all 5 languages; stretch +30.3 s (TR alone 16.1 s), accepted without a fit pass. Schedule 7:48, audio.
- [x] HI/PT/ES dub texts (mean ~0.70x EN), 7 subtitle languages, localize, youtube.md (commit after 52d9eee line).
- [x] Stills reviewed (RGB overlap fix). TR term scan + 8 retakes (build/tr_fixline.summary); listening file
  YAYIN/recap2/dinleme/recap2_tr_terimler.mp3 (+ .txt) for the creator. Thumbnail recap2_A in 5 languages.
- [ ] Add ep09/ep10 C0 to the montage when they exist, full render, compose, dubs, subs, rerun make_localize.py,
  package YAYIN/recap2, listening samples. Upload Tue 24 Nov 17:00.
