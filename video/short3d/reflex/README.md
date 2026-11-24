# 3D Short (EN + TR): "Can you beat 214 ms?" / "214 ms'yi geçebilir misin?"

Vertical Short (1080x1920, ~40 s) for `lessons/10-reflex-oled` (Episode 10, https://youtu.be/0tr5Sf8dJDY), in the
Blender look of Episode 10 and the treasure Short (`video/short3d/treasure_tr`, this pipeline is a copy of it with a
language switch). Circuit = the Ep10 circuit exactly (`video/ep10/b3d/ep10_3d.py` wires/holes, `video/b3d/pbl.py`
parts: OLED, passive buzzer, button); the OLED shows the sketch's own screens pixel-exact (`oledfont.Screen.show`,
the sketch's `show(top, big)`). Texts: `script_en.json` / `script_tr.json`; upload texts: `youtube.md`.

Structure: hook (flash-forward: WAIT -> GO! beep -> press -> "NEW RECORD! 214ms" + record tone, title 214 ms) ->
the round on the narration (WAIT... GO! on the spoken word, press 214 ms later, NEW RECORD) -> unplug (screen and
power LED off, picture dims) -> replug: setup() reads the record back, "REFLEX 2.0 best: 214ms" -> how it works
(stopwatch card counting 0 -> 214 ms, `millis()`; Preferences drawer with `prefs.putULong("best", best);`) ->
the three parts with labels (OLED D21/D22, buzzer D32, button D19) and a new round starting -> CTA follow card
("Follow for more builds!" / "Daha fazlası için takip et!", the round finishes behind it: GO! beep, "your time 263ms").

## Build (from the repo root, repo venv)

    .venv/Scripts/python video/short3d/reflex/make.py --lang en
    .venv/Scripts/python video/short3d/reflex/make.py --lang tr

does every missing step; single steps: `make.py --lang en voice | render | repair | compose | mix | final | thumb`.

| step | file | output |
|---|---|---|
| voice | `voice.py` (writes `short.json` from the two scripts) | `build/<lang>/<id>.mp3` (`cbx.settings({}, lang)`: EN creator voice B, TR creator TR voice), `tools/cbx_retake.py video/short3d/reflex <lang> --short` Whisper retakes, `build/<lang>/voice.wav`, `build/<lang>/schedule.json` |
| render | `scene3d.py` (Blender, one process per shot, `PBL_SAMPLES=16`, resumable) | `build/<lang>/shots/<shot>/f_*.png` + `anchors.json` |
| compose | `compose.py` (2 workers, frames written in windows of 24) | `build/<lang>/picture.mp4`: sound-wave rings at the buzzer on every tone, labels, word-timed captions, on-screen text in the Short's language, CTA |
| mix | `mix.py` | `build/<lang>/audio.wav`: narration + buzzer (`assemble.piezo()` at 1500 Hz/150 ms and 2000 Hz/300 ms, whole effects track x `assemble.SFX_GAIN`) + clicks/plugs + music bed (level 0.11), two-pass loudnorm -16 LUFS |
| final | `make.py final` | `build/reflex_<lang>_final.mp4`, `build/reflex_<lang>_upload.mp4` (HEVC < 10 MB) |
| thumb | `compose.py --thumb 2.0` | `build/thumb_<lang>.jpg` (no captions, the 214 ms moment) |

`story.py` is the single source of timing (language from env `REFLEX_LANG`, make.py sets it): shots come from the
lines' "vis" (voice.py `VIS`), every event sits on a spoken word (`WORDS` per language), and the device follows the
sketch's state machine (WAIT 1.5-4 s; the record round starts off camera during the hook, GO! tone(1500, 150), NEW RECORD tone(2000, 300), result for 2 s, then
"REFLEX 2.0  best:"), so the OLED, the sounds and the rings always agree.
Narration notes: EN l02 says "Go!" and TR l02 "Bip sesini bekle... Başla!" (Chatterbox spelled "GO" / garbled "BAŞLA");
EN l09 is seed 4 picked by hand (the retake pass kept a take that said "If you want to build..."), so a plain
`voice.py --lang en` re-run can swap it again - check its first words. Buzzer level: mix.py sets the tones 8 dB (RMS)
under the narration's speech, then applies `assemble.SFX_GAIN` to the whole effects track.
Renders wait for at least `MIN_FREE_GB` (3.5) free RAM and no other Blender; they may share the GPU with a TTS job.

Checks: `blender -b -P video/short3d/reflex/scene3d.py -- --lang en --at 1.0,12.0` and
`compose.py --lang en --at 1.0,12.0` (-> `build/<lang>/stills`, `build/<lang>/comp_stills`).
Heavy steps wait while another `blender.exe` or Chatterbox job runs (16 GB PC).
