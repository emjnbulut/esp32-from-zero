# 3D Short (TR): "Hazine Dedektörü 2.0"

Turkish vertical Short (1080x1920, ~54 s) for `projects/08-treasure-detector-2`, in the Blender look of Episode 10
(`video/b3d/pbl.py` kit: horizontal breadboards, ESP32, OLED with the real Adafruit pixel font, passive buzzer, button,
plus the knob `Kit.pot()`, RGB LED `Kit.rgb_led()` and resistors `Kit.resistor()` added for this Short).
Upload texts: `youtube_tr.md`.

Structure: hook (the result: YANIYOR!, button, fanfare, HAZİNE!) -> build montage (each part drops in on its spoken
name, wires grow, labels with pins) -> hunt (knob turns, LED blue -> red, Geiger ticks faster/higher with sound-wave
rings, OLED + 2D meter SOĞUK/ILIK/SICAK/YANIYOR!) -> KAZ! fanfare + confetti + 12,4 sn record -> how it works
(knob number 0..99 with `analogRead`/`map` card, number line `uzaklik = abs(sayi - hazine)`, dig check -> BOŞ!,
unplug/replug: the record stays) -> CTA ("Böyle projeler yapmayı öğrenmek istiyorsan kanalımı takip et!" + follow
button tap, "Kodun tamamı açıklamada").

## Build (from the repo root, repo venv)

    .venv/Scripts/python video/short3d/treasure_tr/make.py

does every missing step; single steps: `make.py voice | render | repair | compose | mix | final`
(`repair` re-renders frames a killed Blender left half-written). Thumbnail: `compose.py --thumb 20.9` -> `build/thumb.jpg`
(no captions; `build/thumb_alt_hazine.jpg` = the HAZİNE! moment).

| step | file | output |
|---|---|---|
| voice | `voice.py` (text in `short.json`) | `build/tr/<id>.mp3` (creator's TR voice, `cbx.settings(spec, "tr")`), `tools/cbx_retake.py ... --short` Whisper retakes, `build/voice.wav`, `build/schedule.json` (word times) |
| render | `scene3d.py` (Blender, one process per shot, `PBL_SAMPLES=16`, resumable) | `build/shots/<shot>/f_*.png` + `anchors.json` (projected buzzer/LED/knob/OLED/button, part labels) |
| compose | `compose.py` (2 workers, `COMPOSE_WORKERS`) | `build/picture.mp4`: part labels, sound-wave rings (b3d `overlay.waves`), word-timed captions, Turkish on-screen text, CTA |
| mix | `mix.py` | `build/audio.wav`: narration + buzzer via b3d `assemble.piezo()` + clicks/pops + music bed (`tools/music.py`, level 0.11), two-pass loudnorm -16 LUFS |
| final | `make.py final` | `build/treasure_tr_final.mp4`, `build/treasure_tr_upload.mp4` (HEVC < 10 MB) |

`story.py` is the single source of timing: shots come from the narration's line "vis" fields, every event (knob
keyframes, button presses, unplug) sits on a spoken word, and the device is simulated with the sketch's own logic
(same `map()` maths, thresholds, tick interval 60-700 ms, tick pitch 3000-800 Hz, fanfare notes, delays), so the OLED,
the LED, the ticks, the rings and the sound always agree.

New narration (text change in `short.json`): `make.py --renarrate` = voice -> re-time -> re-render every shot ->
compose -> mix -> final (about 45 min of Blender on this PC). Checks: stills with
`blender -b -P video/short3d/treasure_tr/scene3d.py -- --at 1.0,21.0` and `compose.py --at 1.0,21.0`.
Heavy steps wait while another `blender.exe` or Chatterbox job runs (16 GB PC).
