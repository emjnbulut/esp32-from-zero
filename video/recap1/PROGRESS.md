# Recap: episodes 1-4 (numberless special) - progress

Release: Fri 30 Oct 2026 17:00 (video/YAYIN_TAKVIMI.md). Topic: how to read a sketch (user 2026-10-27: the code is confusing).
Footage: reused clips only (footage/recap1/C1-C4, trimmed from ep03 C2 and ep04 C3/C4/C5). EN + TR first; HI/PT/ES later.
Resume rule: do the first unchecked step; commands from the repo root.

- [x] 1. Script make_script.py (46 segments, EN + TR sub + TR spoken) + page index.html + scenes recap1.js (live trace component)
- [ ] 2. EN narration: python tools/tts.py video/recap1 ; python tools/cbx_retake.py video/recap1 en ; python tools/build.py video/recap1 schedule
- [ ] 3. lesson_lint + stills review (node engine/render.mjs recap1 --stills ...)
- [ ] 4. TR dub: tools/dub.py video/recap1 tr --report ; cbx_retake ... tr ; schedule
- [ ] 5. Render, audio, compose, dub tr, subs
- [ ] 6. Thumbnail, youtube.md, user review
