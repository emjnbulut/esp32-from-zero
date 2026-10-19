# Where we left off (2026-10-20 ~00:30) - YOUTUBE LAUNCH (read this first)

Claude runs the YouTube side through Claude-in-Chrome (Studio signed in as Pin by Pin Lab, channel UCOGFzocCfvfYWiA5-MfHHwQ).
Full notes: memory file `youtube-upload-progress.md`.

**Scheduled (all 17:00 Turkey time):** trailer `l_70hbSQFQo`, ep01 `RyR4OEA7ESA`, ep02 `NwtftTFs_Og` (all Tue 20 Oct),
ep01 EN Short (Wed 21 Oct), ep03 `doPDxOPFjQg` (Fri 23 Oct). Playlist "ESP32 From Zero - Full Beginner Course" (oldest first)
holds ep01-ep03. Channel description published (4 dubs, 12 subtitle languages, learning site, GitHub, contact).
Learning site: https://emjnbulut.github.io/esp32-learning-lab/ (public, GitHub Pages) - every episode/Short description
carries it via `tools/sitelink.py` (applied by `tools/deliver.py` and `tools/publish.py`).

**Still to do:** Shorts ep01 TR (22 Oct), ep02 EN (23), ep02 TR (24, 11 MB), ep01 HI (25), ep03 EN (26) - ep01 TR/HI need
their own titles/descriptions, Short descriptions link the episode URL; dub tracks (YAYIN/epXX/dublaj_sesleri) and
`python tools/publish.py video/epXX <VIDEO_ID>` for 12 subtitle languages + translated titles (token may need
`publish.py auth`); thumbnails (YAYIN/epXX/kucuk_resimler; chosen: ep01 C "START HERE", ep02 A "DON'T FRY IT!"; custom
thumbnails and clickable links need the creator to verify the channel by phone: youtube.com/verify); set the trailer as
channel trailer after it is public; end screens; Shorts "Related video"; check ep03 category = Education.

**How uploads work (important):** browser tool `file_upload` only takes <10 MB; the native file dialog is blocked and a
localhost fetch from Studio hangs. Files >10 MB = the creator presses "Dosya seç" and pastes the full path (Claude puts it
on the clipboard); copies live in `YAYIN/_buyuk_dosyalar/` (deliver.py wipes YAYIN, recreate with cp). Everything else
(title, description, radios via JS `tp-yt-paper-radio-button[name=...]`, tags, language, category, schedule: pick
the time from the list, typing it does not work, calendar day cells) is done by Claude.
AI disclosure was answered "Yes" on every video (cloned narration voice) - tell the creator.

# Earlier notes

# Where we left off (2026-10-19 morning)

## ALL REBUILT WITH THE NEW VOICES (done 2026-10-19 ~08:00)
- ep01 10:35, ep02 7:20, ep03 5:17, ep04 10:17 (incl. intro/outro), dubs tr/hi/pt/es, 12 subtitle languages,
  chapters/descriptions updated, trailer 37 s, 10 Shorts (ep01 en/tr/hi/pt, ep02-04 en/tr).
- Upload folder: `YAYIN/` (399 MB, `python tools/deliver.py` rebuilds it). Release plan `video/YAYIN_PLANI.md`:
  launch **Tue 20 Oct 17:00 TR** (ep01 + ep02 + trailer).
- Voices (tools/cbx.py VOICES): EN mark; TR **pt_fleurs2** (user approved after tr_fleurs2 had hiss); HI hi_fleurs5;
  PT pt_fleurs2; ES es_fleurs2. Videos are TV-range now (Windows players showed no picture with full range).
- New checks: `cbx_retake.py` flags "stray sound" (Chatterbox mumbles/hiss after a chunk, sound >0.3 s from any
  Whisper word) and never reuses takes of another voice/text; `cbx_fixline.py` = extra seeds for single weak lines.
  ep01 tr s26 tail was trimmed by hand (15.2 s).
- Run long jobs ONE at a time (16 GB RAM; Claude Code's memory guard kills background jobs otherwise).

## 2026-10-19 evening
- ep01 creator clips DONE: originals in footage/ep01/raw/, trimmed + stabilized + cropped to footage/ep01/C1-C3.mp4
  (ffmpeg vidstab, crop 1056x594 -> 1280x720); composed, dubs re-muxed, YAYIN/ rebuilt.
- ep02 s28 fixed (creator's 30-pin board leaves free holes on ONE side only): new line in all languages, new
  animation (narrow board both sides -> wide 30-pin -> 38-pin), ep02 re-rendered (7:21), dubs, Shorts, YAYIN/.
  s13 "D2 = GPIO 2" confirmed on the real board.
- Creator's board: 30-pin DevKit, CP2102 (COM6), red power LED, EN top-left / BOOT bottom-left of the USB port.
- Open: ep04 two_leds/challenge_speed use GPIO 25 (EN side) -> creator needs two breadboards side by side
  (advised) or move the green LED to GPIO 21 (not done).

- ep02 creator clips DONE (raw in footage/ep02/raw/; C1 = digital pan along the pin labels, C2/C3 end on a
  held frame via tpad): composed, dubs re-muxed. ep02 Short h7 now uses footage/ep02/C3.mp4 (short.json shot
  "footage" key, falls back to the episode render if the clip is missing). YAYIN/ rebuilt (426 MB).

- ep03 creator clips DONE (C1 speed-ramped 19 s -> 7.4 s: 3.4-7.6 @2x, 9.4-17.2 @2.6x, 17.2-19.5 @1x); composed,
  dubs re-muxed; ep03 Short h6 uses footage/ep03/C2.mp4.

## Waiting for the creator
Nothing for ep01-ep03. ep04 clips C1-C6 (lists in video/ep0X/youtube.md) when filming.

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
