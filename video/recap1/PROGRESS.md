# Recap: episodes 1-4 (numberless special) - progress

Release: Fri 30 Oct 2026 17:00 (video/YAYIN_TAKVIMI.md). Topic: how to read a sketch (user 2026-10-27: the code is confusing).
Footage: reused clips only (footage/recap1/C1-C4, trimmed from ep03 C2 and ep04 C3/C4/C5). EN + TR first; HI/PT/ES later.
Resume rule: do the first unchecked step; commands from the repo root.

- [x] 1. Script make_script.py (46 segments, EN + TR sub + TR spoken) + page index.html + scenes recap1.js (live trace component)
- [x] 2. EN narration: python tools/tts.py video/recap1 ; python tools/cbx_retake.py video/recap1 en ; python tools/build.py video/recap1 schedule
- [x] 3. lesson_lint + stills review (node engine/render.mjs recap1 --stills ...)
- [x] 4. TR dub: tools/dub.py video/recap1 tr --report ; cbx_retake ... tr ; schedule
- [x] 5. Render, audio, compose, dub tr, subs
- [ ] 6. Thumbnail, youtube.md, user review

## State 2026-10-27 23:32 (session paused by the user)
Built end to end: build/recap1_final.mp4 (EN, 7.6 min), build/recap1_tr_dub.mp4, build/recap1_en.srt + recap1_tr.srt. lesson_lint 0 warnings.
Not watched by the user yet. Open points: user review (does the MEMORY panel make the code clear? blink_button code is small on a phone),
thumbnail (Claude decides), youtube.md + localize (titles/descriptions), HI/PT/ES dubs later, Short for the recap, upload Fri 30 Oct 17:00.
Re-run all: bash video/recap1/build_all.sh (delete build/rebuild.done first); scenes: video/recap1/recap1.js; text: make_script.py.

## State 2026-10-28 ~00:40 (user closed the session mid-rebuild)
Changes since the last full build: real-footage insets next to every trace (footage/recap1/C1-C4 are looped 70 s files, gitignored) and two analogies
(s21 door, s29 kitchen timer vs wall clock) in EN + TR; EN narration + schedule are redone, the TR dub was being retaken, render/audio/compose/dub_tr/subs were NOT finished.
build/recap1_final.mp4 on disk = the previous version (insets, WITHOUT the analogies).
RESUME: `bash video/recap1/build_all.sh >> video/recap1/build_all3.log 2>&1` (resumable through build/rebuild.done; it skips finished steps; run it in short foreground chunks or let it run in the background).
If build/rebuild.done lists schedule, render, audio, compose, dub_tr and subs the build is complete: then rerun `python video/recap1/make_localize.py` (chapter times moved) and watch the video.
Open: user has not given feedback on clarity yet; HI/PT/ES dubs not made (EN + TR first); upload Fri 30 Oct 17:00; thumbnail = video/thumbs/build/recap_A.png.
Also pending from this session: ep06 lessons/06-analog-input sketches written and compiled (not committed yet), no script/scenes for ep06 until the recap feedback is in.

## v3 2026-10-28 afternoon: rewritten narration (user feedback) - resume here
User on the first full build: the TR dub explains badly (jumbled at punctuation, robotic term lists); same in every language;
wants human explanation with many everyday examples AND the objective meaning of every term. Guidelines section 9.
- make_script.py v3: 50 segments (new s11b, s15b, s24b, s29b), 2145 words; every idea = everyday picture + "What actually
  happens: ..." + code. recap1.js: exCard() example cards (engine/lib.js exampleCard, stage.css .excard), new chips for the
  objective sentences, like/subscribe moved to the top right (insets cover the bottom right). tools/anchor_check.py recap1 = 0 problems.
- Voice engine (tools/cbx.py, chatterbox_say.py): punctuation pauses 0.5/0.7/0.35/0.22 s, NO time-stretch (rubberband pilot
  sounded robotic/slow), dubs never sped up (DUB_TEMPO_MAX 1.0, build.py DUB_FIT 1.03), cbx_retake rate band 0.85-1.18.
  User approved pilot C (video/recap1/build/pilot/PILOT_tr_C.mp3).
- HI/PT/ES dub texts: dub/{hi,pt,es}.json (Sonnet agents, 27 changed segments re-translated for v3).
- Build: `bash tools/rebuild_voices.sh recap1 >> video/recap1/build_v2.log 2>&1` (resumable via build/rebuild.done; all 5
  languages are narrated BEFORE schedule/render so the picture waits for the longest dub). Then: pace_check.py, listen
  excerpts for the user (TR first), thumbnail recap_A, youtube.md/localize, upload Fri 30 Oct 17:00.
- ep05 v2 draft (same style, not yet with objective sentences): video/ep05/make_script.v2-draft.py - only after the user
  likes the recap (user: "şu an recapa odaklanalım, beğenirsem bölüm 5'e sonra geçeriz").
