# Episode 14 (DRAFT, not reviewed) — shot plan

Script: `make_script.py` (25 segments, ~3.3 min narration + 20 s code pages). Pipeline = Episode 10-12 v2 (HANDOFF.md):
narration -> schedule -> `b3d/ep14_3d.py` (copy of ep12_3d.py structure, one Blender process per shot,
PBL_SAMPLES=16) -> Motion Canvas (`node video/mc/tools/timing.mjs ep14`, scenes prefixed `ep14_`) ->
`video/b3d/assemble.py video/ep14` -> build.py audio/subs/compose -> ffprobe + Whisper on the ending.

## Circuit

Ep 10 layout (OLED 21/22, button 19, passive buzzer 32). New: three jumper wires from GPIO 14, 2 and 15 to a banana,
an apple and an orange lying on the desk next to the breadboard. No resistors. Sketch: lessons/14-fruit-piano.

## New 3D parts (additive module `video/b3d/parts_ep14.py`)

- **Fruit**: banana (bent capsule, yellow with brown tips), apple (sphere with dimples + stem), orange (dimpled sphere,
  noise bump). Stylized, same look as the kit parts; a jumper wire end pushed into each.
- **Finger**: reuse the Ep 11 hand (scaled), index finger touching the fruit; a soft glow pulse on contact.
- **Note tags**: 2D overlay cards "do / mi / sol" over the touched fruit, colour per fruit.

## Shots (b3d)

| id | seg | what |
|---|---|---|
| open_play | s01 | finger touches banana, apple, orange; note tag + buzzer rings each time |
| open_tune | s02 | button held, OLED "REC", short tune, then replay with tags lighting in order |
| open_orbit | s03 | orbit: fruit + wires + board |
| open_title | s04 | Ep 10 circuit tagged "episode 10", fruit tagged "new" |
| touch_pins | s05 | GPIO 14 / 2 / 15 highlighted on the board (labels) |
| touch_banana | s08 | macro: finger on banana, glow travels the wire to pin 14 |
| wire_keep | s11 | OLED, button, buzzer tagged "stays" |
| wire_fruit | s12 | three wires go in one by one, pin tags |
| wire_led | s13 | on-board blue LED glows faintly, tag "pin 2 = blue LED too" |
| rec_hold | s17 | finger holds button, 1 s ring fills, OLED "REC" |
| rec_play | s19 | eight touches, OLED shows boxes filling 1..8 |
| replay | s20 | short press, tags light in order, buzzer rings |
| trouble_calm | s21 | hand resting on the apple while OLED says "calibrating", then the apple plays by itself (red X) |
| trouble_drop | s22 | a key that stays silent; OLED number shown next to the threshold |
| challenge | s23 | two fingers on banana + orange, tag "high do?" |
| outro | s25 | orbit, OLED "see you in" / "ep 15" |

## Motion Canvas scenes

| id | seg | what |
|---|---|---|
| bucket | s06 | the pin fills a little bucket, a counter shows how many fills per moment |
| bucket_finger | s07 | finger touches -> bucket gets bigger, fills slower, number drops (e.g. 60 -> 25) |
| code_touch | s09 | glimpse -> `touchRead(KEY_PIN[i]) < calm[i] - DROP` (DROP = 20) |
| calibrate | s10 | setup(): three calm values = average of 8 looks (Episode 7), "hands off!" label |
| array_boxes | s14 | three separate variables merge into one row of boxes `NOTE[0..2]` (Variable box picture extended) |
| code_array | s15 | `const int KEY_PIN[3] = {14, 2, 15};` + `const int NOTE[3] = {523, 659, 784};` aligned, box numbers 0 1 2 |
| code_loop_keys | s16 | `for (int i = 0; i < 3; i++)` walking the boxes, touched one plays |
| song_boxes | s18 | eight empty boxes `song[8]`, notes drop in one by one |
| code_full | s24 | readable pages (codeFull `{pages: true}`, ~5 pages x 4 s) + lesson folder chip + comment bubble |

## Sounds

Buzzer = `assemble.piezo()` at the sketch's notes (DO 523, MI 659, SOL 784; challenge high DO 1047) with rings on every note;
soft "tap" for finger contacts; SFX_GAIN applies.

## Before production

Creator review of the script + the two new analogies (bucket, row of boxes); verify note frequencies and pins against
fruit_piano.ino; check the episode-length decision (4-5 min vs 6-8 min).
