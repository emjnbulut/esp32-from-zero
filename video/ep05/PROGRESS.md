# Episode 5 — "PWM and RGB Color Mixing" — progress

Resume rule: do the first unchecked step; commands are run from the repo root.
Release: Fri 30 Oct 2026 17:00 (video/YAYIN_TAKVIMI.md); creator clips due Wed 28 Oct. Follows
video/PRODUCTION_GUIDELINES.md incl. section 5 (max 2 subtle like/subscribe icons, end invites comments).
Not a mini-project: no challenge-solution Short (solution stays in the lesson folder).
User 2026-10-25: script now, NO render yet; English only (dubs on hold).

- [x] 1. Sketches `lessons/05-pwm-and-rgb/code/` (pwm_levels, fade_millis, rgb_colors, color_modes, challenge_headlamp);
      COMMON_ANODE switch because the kit's RGB LED type is unknown (creator tests rgb_colors before filming)
- [x] 1b. Compile check: all 5 OK, no warnings (esp32 core 3.3.12)
- [x] 2. Script `make_script.py` (45 segments, ~1170 words) + clip list C0-C5 in script.json
- [x] 3. Lesson README (RGB layout: row c cols 20-23, R/K/G/B; resistors across the gap at 20/22/23)
- [x] 4. Scenes `ep05.js` + index.html (reuse ep04: makeBB2, bigCode, quizCard, heroClip full; add like/subscribe corner icon helper)
- [x] 5. EN narration (Mark voice, GPU Whisper) -> schedule (body 7:44) -> stills review + fixes. NOTE: the user may switch
      the narration to a clone of their OWN voice (YouTube AI-label exemption); then re-run tts + schedule, scenes follow the words
- [x] 6. Subs (7 langs), HI/PT/ES texts (dub + subtitles), make_localize.py run (11 chapters, 12 languages)
- [ ] 7. Render, compose with clips, Short spec (EN + TR), thumbnail

## Clips (creator, due Wed 28 Oct)
C0 opening (red breathing + RGB fade, 14-16 s), C1 multimeter (pwm_levels, hands-free), C2 fade_millis + press,
C3 RGB wiring close-up, C4 rgb_colors, C5 color_modes presses. Details in script.json "clips".
