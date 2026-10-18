# Where we left off (2026-10-18 evening)

## NEW VOICES (2026-10-18) — rebuild in progress
All narration is now Chatterbox (local GPU): EN `mark` (LibriVox, public domain), TR `tr_fleurs2` (user's pick),
HI `hi_fleurs5`, PT `pt_fleurs2`, ES `es_fleurs2` (Google FLEURS, CC BY 4.0 — credit line is in every description).
Settings in `tools/cbx.py`; setup in `tools/CHATTERBOX.md`; voice prompts in `tools/voice_samples/` (gitignored, README there).
Lines are cut at punctuation and joined with fixed pauses; `tools/cbx_retake.py` re-narrates lines with long pauses,
odd speed or (not for Hindi) misheard words. The schedule grows a segment when a dub would not fit.

Resume (skips finished steps, listed in `video/<ep>/build/rebuild.done`):

    bash tools/rebuild_voices.sh ep01 ep02 ep03 ep04 >> build_rebuild_voices.log 2>&1
    bash tools/finish_all.sh          # Shorts (ep01 en/tr/hi/pt, ep02-04 en/tr) + trailer
    python tools/deliver.py           # clean upload folder YAYIN/ (then delete old test/voice_test files)

Run it alone: with Unity/Chrome open, parallel jobs ran out of memory (16 GB).
State at 18:35: ep01 en/tr/hi/pt narrated + retaken, es narrating; ep01 render and ep02-04 not started.

Release plan: `video/YAYIN_PLANI.md` (launch Mon 19 Oct 17:00 TR: ep01 + ep02 + trailer, then daily Shorts).
Creator clips needed first: footage/ep01/C1-C3 (board plugged in + red LED, BOOT held while "Connecting",
EN pressed + "Hello, ESP32!") and footage/ep02/C1-C3 (see video/ep02/youtube.md).

---

# Earlier notes (2026-10-17)

Commands run from the repo root (`.venv/Scripts/python`). Large media is gitignored and lives only on
the local PC; everything here regenerates it.

## Episodes
| | Status | Waiting for |
|---|---|---|
| ep01 Setup | final with intro/outro (10:15), dubs TR/HI/PT/ES, 12 subs, localize.json | creator clips `footage/ep01/C1–C3` → `python tools/build.py video/ep01 compose` |
| ep02 Board + breadboard | final with intro/outro (7:45), dubs, 12 subs, localize.json | clips `footage/ep02/C1–C3` (list in `video/ep02/youtube.md`) → compose. Check s13 "D2 = GPIO 2" and free-hole counts against the real board |
| ep03 Blink an LED | in progress, **render + dubs on hold until the Chatterbox voice decision**; scenes reviewed + fixed on a preview render, localize.json done. Chatterbox setup/test/switch: `tools/CHATTERBOX.md` — see `video/ep03/PROGRESS.md` (resume from the first unchecked step: render → audio/subs/compose → dubs/subs/localize) | clips C1 move the wire, C2 LED blinking, C3 fast blink |
| ep04 Buttons + millis (two topics, ~10:30) | script, 5 sketches, scenes (reviewed), lesson README, dub/sub texts, localize.json, Short spec done — **narration/render/dubs on hold for Chatterbox**, see `video/ep04/PROGRESS.md` | clips C1–C6 (list in `video/ep04/youtube.md`) |

Dubs are separate audio tracks: adding clips later only needs `build.py <ep> compose` and then
`tools/dub.py <ep> <lang>` (re-muxes the dub videos).

## Format (from 2026-10-17)
From ep04 on: two curriculum topics per episode, 10–15 minutes (CURRICULUM.md renumbered to 11 episodes).

## Tomorrow (2026-10-18)
Install Chatterbox and test it (`tools/CHATTERBOX.md`), then re-narrate + render ALL episodes (ep01-ep04, same voice everywhere),
dubs, Shorts (all four short.json now use word anchors, so shots follow the new narration), chapters:
`python tools/rechapter.py video/ep01` (ep02-04: rerun their make_localize.py), then the trailer: `python tools/trailer.py`.
Thumbnails: `node video/tools/thumbs.mjs` (3 variants per episode in video/thumbs/build/).

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

## Parked ideas (2026-10-17, not now)
- Website: MkDocs Material on GitHub Pages built from `lessons/`, domain pinbypinlab.com when the first video goes live.
- Instagram @pinbypinlab: Shorts as Reels (EN), plus one carousel per episode (scene stills + code, 1080x1350);
  music credit line in every caption.
