# 3D Short (EN + TR): "My ESP32 guards the cookie jar" / "ESP32'm kurabiye kavanozunu koruyor"

DRAFT - vertical Short (1080x1920, EN 48.5 s, TR 46.7 s) for `lessons/11-motion-alarm` (Episode 11, not published yet: `EP11_URL`
placeholder in `youtube.md`). Pipeline = a copy of `video/short3d/reflex/` (Ep10 Short) with a language switch.
Circuit + props = the Episode 11 shot script exactly (`video/ep11/b3d/ep11_3d.py`: Ep10 circuit + HC-SR501 PIR on
B50-52e, VIN / D33 wires; `video/b3d/parts_pir.py` PIR + 9 lens windows; `video/b3d/parts_ep11.py` warm hand, cookie
jar, thumbs icon). The OLED shows the sketch's screens pixel-exact (`show()`: size-1 line at 0,0, size-2 line at 0,28
like the Ep11 shot script): "leave the room!" / "10 s".."1 s", "guarding..." / "ARMED", "motion detected!" /
"INTRUDER", "seen 1x, last:" / "2 min ago". Texts: `script_en.json` / `script_tr.json`; upload texts: `youtube.md`.

Structure: hook (flash-forward: the warm hand reaches for the jar, the lens windows light up, INTRUDER + siren,
title "Who's stealing my cookies?") -> arm (press on "arm", 10 s countdown with a 2000 Hz tick per second) -> catch
(time skip "10 s later - ARMED"; the hand sneaks in, INTRUDER + siren on the spoken "siren", "CAUGHT!") -> ago (time
skip, the siren stopped by itself after 15 s: "seen 1x, last: 2 min ago") -> how it works 1 (dome x-ray, the lens
windows light one by one; the warm hand crosses windows -> OUT = HIGH, thumbs up on "yes") -> how it works 2 (the
hand again: INTRUDER, a parking ticket gets stamped "754 213 ms" + `lastMotion = now;`, two-tone siren) -> parts
(PIR D33, OLED D21 D22, buzzer D32, button D19) -> CTA follow card ("Follow for more builds!" / "Daha fazlası için
takip et!"), the guard stays armed behind it.

## Build (from the repo root, repo venv)

    .venv/Scripts/python video/short3d/cookie/make.py --lang en
    .venv/Scripts/python video/short3d/cookie/make.py --lang tr

does every missing step; single steps: `make.py --lang en voice | render | repair | compose | mix | final | thumb`.

| step | file | output |
|---|---|---|
| voice | `voice.py` (writes `short.json` from the two scripts) | `build/<lang>/<id>.mp3` (`cbx.settings({}, lang)`), `tools/cbx_retake.py video/short3d/cookie <lang> --short` Whisper retakes, `build/<lang>/voice.wav`, `build/<lang>/schedule.json` |
| render | `scene3d.py` (Blender, one process per shot, `PBL_SAMPLES=16`, resumable) | `build/<lang>/shots/<shot>/f_*.png` + `anchors.json` |
| compose | `compose.py` (2 workers, frames written in windows of 24) | `build/<lang>/picture.mp4`: sound-wave rings at the buzzer on every tone, red edge glow while the siren plays, labels, word-timed captions, on-screen text in the Short's language, CTA |
| mix | `mix.py` | `build/<lang>/audio.wav`: narration + buzzer (`assemble.piezo()`: tick 2000 Hz/30 ms, siren 1800/2600 Hz flipping every 250 ms, 8 dB under the speech, whole effects track x `assemble.SFX_GAIN`) + click/whoosh/stamp/pops + music bed (0.11), two-pass loudnorm -16 LUFS |
| final | `make.py final` | `build/cookie_<lang>_final.mp4`, `build/cookie_<lang>_upload.mp4` (HEVC < 10 MB) |
| thumb | `compose.py --thumb 1.85` | `build/thumb_<lang>.jpg` (no captions: hand at the jar, windows lit, INTRUDER) |

`story.py` is the single source of timing (language from env `COOKIE_LANG`, make.py sets it): shots come from the lines'
"vis" (voice.py `VIS`), events sit on spoken words (`WORDS` per language), and the device follows the sketch's state
machine (countdown ticks while the number changes, ARMED after 10 s, siren from the PIR's yes until a cut = time skip).
Captions: a line's "show" is used as the caption only when it re-spells the spoken line (TR l07 "E Se Pe otuz iki" ->
"ESP32"); the short "show" texts (hook title, "CAUGHT!", CTA headline) are on-screen text.
Narration (2026-11-24): Whisper (large-v3-turbo) hears every EN and TR line as written; the retake pass re-seeded EN
l09 (rate) and TR l01/l03/l05/l06 (seed 2 kept). TR l07 says "E Se Pe otuz iki" (caption "ESP32"); "buzzer" is
heard as "buzlar" in TR l08, like in the reflex Short. A plain `voice.py` re-run keeps the cached takes.
Cameras (scene3d.py `CAMS`) look at the desk diagonally from the front-right (~55 degrees down), so the long side of
the circuit runs along the tall frame. Renders wait for at least `MIN_FREE_GB` (3.5) free RAM and no other Blender.

Checks: `blender -b -P video/short3d/cookie/scene3d.py -- --lang en --at 1.7,31.0` and
`compose.py --lang en --at 1.7,31.0` (-> `build/<lang>/stills`, `build/<lang>/comp_stills`; rings and part labels
appear only after the shot is rendered, they come from its anchors.json).
