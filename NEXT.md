# Where we left off (2026-10-17, end of session)

Commands run from the repo root (`.venv/Scripts/python`). Large media is gitignored and lives only on
the local PC; everything here regenerates it.

## Episodes
| | Status | Waiting for |
|---|---|---|
| ep01 Setup | final with intro/outro (10:15), dubs TR/HI/PT/ES, 12 subs, localize.json | creator clips `footage/ep01/C1–C3` → `python tools/build.py video/ep01 compose` |
| ep02 Board + breadboard | final with intro/outro (7:45), dubs, 12 subs, localize.json | clips `footage/ep02/C1–C3` (list in `video/ep02/youtube.md`) → compose. Check s13 "D2 = GPIO 2" and free-hole counts against the real board |
| ep03 Blink an LED | in progress — see `video/ep03/PROGRESS.md` (resume from the first unchecked step: render → audio/subs/compose → dubs/subs/localize) | clips C1 move the wire, C2 LED blinking, C3 fast blink |

Dubs are separate audio tracks: adding clips later only needs `build.py <ep> compose` and then
`tools/dub.py <ep> <lang>` (re-muxes the dub videos).

## Shorts
- ep01: EN/TR/HI/PT done (regular ending, Lobby Time music).
- ep02: EN + TR, regular ending. The rebuild may have been cut off when the session closed — if
  `video/shorts/ep02/build/tr/ep02_short_tr.mp4` is older than `short.json`, run
  `python tools/short.py video/shorts/ep02 en` and `... tr` again (~12 min each).
  Scene h7 should switch to real C3 footage once filmed (notes in `video/shorts/ep02/youtube.md`).
- ep03: no Shorts yet. New Shorts: EN + TR only, on-screen text English, narration translated.
- Loop mode exists (`"loop": true` in short.json) but is shelved for now.

## Channel / publishing
- Channel "Pin by Pin Lab" (@pinbypinlab); logo/banner in `brand/export/`; domain postponed.
- YouTube API ready: `python tools/publish.py video/epXX <VIDEO_ID>` uploads all subtitles + translated
  titles/descriptions. Token may need `python tools/publish.py auth` again (app in Testing mode, ~7 days).
- Upload by hand in Studio: the video, dub audio tracks (`build/dub_<lang>.m4a`), end screen on the last 20 s.
- Music "Lobby Time" (Kevin MacLeod, CC BY 4.0) — credit line is in every description; the track file
  is gitignored, see `video/assets/music/README.md`.
