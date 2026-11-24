# Episode 15 (DRAFT, not reviewed) — shot plan

Script: `make_script.py` (25 segments, ~3.3 min narration + 20 s code pages). Pipeline = Episode 10-12 v2 (HANDOFF.md):
narration -> schedule -> `b3d/ep15_3d.py` (copy of ep12_3d.py structure, one Blender process per shot,
PBL_SAMPLES=16) -> Motion Canvas (`node video/mc/tools/timing.mjs ep15`, scenes prefixed `ep15_`) ->
`video/b3d/assemble.py video/ep15` -> build.py audio/subs/compose -> ffprobe + Whisper on the ending.

## Circuit

Ep 10 layout (OLED 21/22, button 19, passive buzzer 32). New: LDR module (AO 35, VCC 3V3, GND; DO empty) on three long
jumper wires so it can sit inside a drawer. Sketch: lessons/15-drawer-spy (OPEN_AT 1800, CLOSED_AT 1200).

## New 3D parts (additive module `video/b3d/parts_ep15.py`)

- **LDR module**: small blue PCB, 4 header pins (AO DO GND VCC), the round photoresistor with its zig-zag track, trim pot,
  two SMD LEDs.
- **Drawer**: a small wooden desk drawer (box + front panel + knob) that slides on a keyframed track; inside it is dark
  (no light), a spot light "floods in" as it opens (light cone through the gap).
- **Light number tag**: 2D overlay card with the live light number (0..4095) and the two lines when needed.

## Shots (b3d)

| id | seg | what |
|---|---|---|
| open_scream | s01 | hand pulls the drawer, light floods in, whoop + rings, OLED "DRAWER OPEN!" |
| open_count | s02 | OLED macro "opened 3x" |
| open_orbit | s03 | orbit: drawer + wires + board |
| open_title | s04 | Ep 10 circuit tagged "episode 10", LDR tagged "new" |
| ldr_module | s05 | module turning, pin labels AO DO GND VCC |
| ldr_macro | s06 | macro of the photoresistor, number tag 0..4095 |
| wire_keep | s09 | OLED, button, buzzer tagged "stays" |
| wire_ldr | s10 | three wires go in: VCC 3V3, GND, AO 35; DO tagged "empty" |
| wire_drawer | s11 | sensor placed in the drawer facing up, wires out at the back |
| flicker | s13 | drawer opened a crack, number tag wobbling around one line, alarm on/off/on (short chirps) |
| scream | s17 | full whoop 5 s (shortened in the edit), rings |
| power_cut | s19 | USB pulled, board dark, plugged back, OLED "opened 3x" |
| reset_hold | s20 | finger holds button, 2 s ring fills, OLED "opened 0x" |
| tune_serial | s21 | laptop corner with the Serial Monitor: "light 240 ... light 2650" |
| trouble_day | s22 | closed drawer with a light gap, false alarm, then a strip of tape over the gap |
| challenge | s23 | OLED mock "open 12 s", tag "your turn" |
| outro | s25 | orbit, OLED "see you in" / "ep 16" |

## Motion Canvas scenes

| id | seg | what |
|---|---|---|
| light_number | s07 | a bar meter: drawer closed = low, open = jumps high |
| code_read | s08 | glimpse -> `readLight()`: average of 8 looks (Episode 7), `DARK_IS_HIGH ? 4095 - raw : raw` |
| one_line | s12 | number over time with one line: above = open, below = closed |
| thermostat | s14 | thermostat picture: heater does not click back the moment it crosses (registry ep15) |
| two_lines | s15 | same graph with 1800 / 1200, the wobble in the gap changes nothing |
| code_hyst | s16 | the two ifs (`!isOpen && light > OPEN_AT`, `isOpen && light < CLOSED_AT`) |
| code_counter | s18 | `openings++; prefs.putInt("openings", openings);` + "notebook from episode 10" chip |
| code_full | s24 | readable pages (codeFull `{pages: true}`) + lesson folder chip + comment bubble |

## Sounds

Whoop = `assemble.piezo()` sweeping 1500 -> 2700 Hz in 0.4 s cycles (the sketch's `1500 + (now % 400) * 3`) with rings;
drawer slide (soft wood whoosh), tape tear; SFX_GAIN applies.

## Before production

Creator review of the script; check the drawer prop look; episode-length decision (4-5 min vs 6-8 min).
