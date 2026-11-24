# 3D Short (EN + TR): "My phone rings a doorbell through my ESP32" / "Telefonumla ESP32 üzerinden kapı zili çalıyorum"

DRAFT - vertical Short (1080x1920, EN ~46.7 s, TR ~45.4 s) for `lessons/12-phone-control` (Episode 12, not published
yet: `EP12_URL` placeholder in `youtube.md`). Pipeline = a copy of `video/short3d/cookie/` (Ep11 Short) with a
language switch. Circuit + props = the Episode 12 shot script (`video/ep12/b3d/ep12_3d.py`: Ep10 layout + RGB LED on
D25/D26/D27 with 220 ohm resistors; `video/b3d/parts_ep12.py` phone on its stand, antenna glow, radio ripples,
travelling packet, router; phone screens = the Ep12 images from `video/ep12/b3d/phone_screens.py`). For the tall frame
the phone stands in front of the board's right half (Ep12: to the right of the board), so phone and board stack up.
The OLED shows the sketch's screens pixel-exact (show(): size-1 line at 0,0, size-2 line at 0,28): "open 192.168.4.1" /
"READY", "command #N" / "RING!" | green | blue | red. Texts: `script_en.json` / `script_tr.json`; upload texts:
`youtube.md`.

Structure: hook (flash-forward: tap RING on the phone, the link flies to the antenna with "GET /ring", ding dong +
"command #1 / RING!", title "Doorbell from my phone?") -> no app / no router / no internet (the router shrinks away)
-> the board's own Wi-Fi ripples from the antenna ("Wi-Fi: PinByPin-ESP32", like a phone hotspot) -> phone close-up:
Wi-Fi list, tap PinByPin-ESP32, connected, 192.168.4.1 typed, the page -> every button = a link
(`<a href="/ring">RING</a>`), tap RING, the link flies in slow motion (labelled), ding dong on "plays" ("buzzer'da"
in TR) -> color buttons green #2, blue #3, red #4 with a command counter, push in on the OLED -> no new parts (RGB LED
D25 D26 D27, OLED D21 D22, buzzer D32) -> CTA follow card ("Follow for more builds!" / "Daha fazlası için takip et!").

## Build (from the repo root, repo venv)

    .venv/Scripts/python video/short3d/doorbell/make.py --lang en
    .venv/Scripts/python video/short3d/doorbell/make.py --lang tr

does every missing step; single steps: `make.py --lang en voice | render | repair | compose | mix | final | thumb`.

| step | file | output |
|---|---|---|
| voice | `voice.py` (writes `short.json` from the two scripts) | `build/<lang>/<id>.mp3` (`cbx.settings({}, lang)`), `tools/cbx_retake.py video/short3d/doorbell <lang> --short` Whisper retakes, `build/<lang>/voice.wav`, `build/<lang>/schedule.json` |
| render | `scene3d.py` (Blender, one process per shot, `PBL_SAMPLES=16`, resumable) | `build/<lang>/shots/<shot>/f_*.png` + `anchors.json` (buzzer, OLED, packet, ...) |
| compose | `compose.py` (2 workers, frames written in windows of 24) | `build/<lang>/picture.mp4`: sound-wave rings at the buzzer on both notes, "GET /ring" riding the packet, labels, word-timed captions, on-screen text in the Short's language, CTA |
| mix | `mix.py` | `build/<lang>/audio.wav`: narration + buzzer (`assemble.piezo()`: tone(1319, 180), 200 ms later tone(1047, 300), 8 dB under the speech, whole effects track x `assemble.SFX_GAIN`) + taps / whoosh / pops + music bed (0.11), two-pass loudnorm -16 LUFS |
| final | `make.py final` | `build/doorbell_<lang>_final.mp4`, `build/doorbell_<lang>_upload.mp4` (HEVC < 10 MB) |
| thumb | `compose.py --thumb 1.6` | `build/thumb_<lang>.jpg` (no captions: the ding, rings, "RING!" on the OLED) |

`story.py` is the single source of timing (language from env `DOORBELL_LANG`, make.py sets it): shots come from the
lines' "vis" (voice.py `VIS`), events sit on spoken words (`WORDS` per language), every tap is a `Cmd` (tap -> packet
-> the board acts on arrival, the command number counts up like the sketch's `commands++`).
Narration (2026-11-25): Whisper (large-v3-turbo) hears every line as written. EN: the retake pass re-seeded l06 and
l09. TR: l05 is seed 6 picked by hand ("Zile" was heard "Sire"); l06 is spoken "Ve kart, buzzer'da iki nota çalıyor:
ding dong." (seed 14 picked by hand: with the leading "..." Chatterbox said "Carp buzzer'da"), the caption keeps
"...ve kart buzzer'da ..."; l03 says "E Se Pe otuz iki" (caption "ESP32"). The hand-picked takes are recorded in
`build/tr/cbx_cache.json` ("picked"); a plain `voice.py --lang tr` keeps them while the text is unchanged.
Renders wait for at least `MIN_FREE_GB` (3.5) free RAM and no other Blender.

Checks: `blender -b -P video/short3d/doorbell/scene3d.py -- --lang en --at 1.6,22.6` and
`compose.py --lang en --at 1.6,22.6` (-> `build/<lang>/stills`, `build/<lang>/comp_stills`; rings, the packet label
and part labels appear only after the shot is rendered, they come from its anchors.json).
