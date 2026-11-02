# Review - 3 November 2026 (Claude, whole-package check)

- Cold open: the picture went empty from 12 to 18.5 s while the narrator spoke. footage/ep05/C0.mp4 is now 8 s of hand-free breathing (the clean tail of the take, played forward, back, forward) + the whole take, so the two presses land on "press" and "press again". Originals: footage/ep05/_orig/.
- C1 now starts 10.2 s into the take: 0.82 / 1.64 / 3.29 V show as the narrator says them (it showed 0.00 V and the hand moving in).
- Metadata: title ends "ESP32 From Zero #5" like the other episodes; TR says "doluluk oranı" as the narration does.
- Short: square, tighter panels (no clipped text, readable), h0 keeps the LED inside the frame.
- Upload copies under 10 MB: YAYIN/ep05/dublaj_sesleri/upload_10mb, YAYIN/ep05/shorts/upload_10mb.
- Creator listening approval still pending: YAYIN/ep05/dinleme/ep05_riskli_satirlar.mp3 holds the lines the tools flagged.

# Current production - 30 October 2026

Local production complete: 10:22 final (body 9:59), five voices, 12 subtitle languages, metadata, A/B thumbnails and EN/TR Shorts. Package: YAYIN/ep05/; listening samples: YAYIN/ep05/dinleme/.

Duration target: average 10 minutes, roughly 8-12. Creator final listening/publication review is separate from technical completion. No YouTube upload was performed. Proof: build/production/verification.json; final-media frames: build/review/.

---

Earlier progress notes follow.

# Episode 5 — "PWM: Make an LED Breathe" — progress

Curriculum v6 (CURRICULUM.md), release Tue 3 Nov 2026 17:00 (video/YAYIN_TAKVIMI.md). Episode 6 = video/ep06.
Old single-video version (v1/v2 draft) stays in video/_old/ep05_single as the source of scenes (ep05.js) and sketches.

- [x] 1. Script `make_script.py` (sections 9 + 10, 53 segments, ~1290 words, EN + TR subtitle + TR spoken),
      `lesson_lint ep05` 0 warnings with the estimated timeline (9.9 min).
- [ ] 2. User approves the narration style on the recap first (memory: ep05 voice work waits for that).
- [ ] 3. Scenes: split video/_old/ep05_single/ep05.js -> ep05 (cold, retrieval, pwm, duty, aw, tourpwm, run, meter, fade, mistake,
      fade2, tourfade, run2, explain, outro); new scenes: retrieval card, duty (tap), mistake, explain.
- [ ] 4. Narration (all dub languages before schedule), lint with the real schedule, render, compose with shoot-pack clips
      p05 C0-C5 (footage/gelen), subs, localize, thumbnail, Short (after Part 2).
