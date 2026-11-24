# Episode 16 (DRAFT, not reviewed) — shot plan

Script: `make_script.py` (25 segments, ~3.0 min narration + 20 s code pages). Pipeline = Episode 10-12 v2 (HANDOFF.md):
narration -> schedule -> `b3d/ep16_3d.py` (copy of ep12_3d.py structure, one Blender process per shot,
PBL_SAMPLES=16) -> Motion Canvas (`node video/mc/tools/timing.mjs ep16`, scenes prefixed `ep16_`) ->
`video/b3d/assemble.py video/ep16` -> build.py audio/subs/compose -> ffprobe + Whisper on the ending.

## Circuit

Ep 10 layout (OLED 21/22, button 19, passive buzzer 32). New: IR obstacle module (OUT 13, VCC 3V3, GND) taped under a
paper cup (bottom cut open) standing on two books as the hoop. Sketch: lessons/16-basket-scoreboard.

## New 3D parts (additive module `video/b3d/parts_ep16.py`)

- **IR module**: small PCB with the two 5 mm diodes (clear emitter, dark receiver), trim pot, 3 pins (OUT GND VCC), a
  status LED that lights when something is in front.
- **Hoop**: paper cup with the bottom cut out, a backboard made of a card, standing on two books; the sensor taped under
  the rim looking across the hole.
- **Paper ball**: crumpled sphere (noise displacement), thrown along keyframed arcs; a faint red beam line across the
  hole (stylized, the real IR is invisible - say so with a tag "invisible in real life").

## Shots (b3d)

| id | seg | what |
|---|---|---|
| open_swish | s01 | paper ball arcs in, drops through, sensor LED blinks, swish beep + rings, OLED "1 pts" |
| open_round | s02 | quick cuts: whistle, timer 30 -> 1, baskets, horn |
| open_record | s03 | OLED "NEW RECORD!", USB pulled and back, "best: 7" |
| open_title | s04 | Ep 10 circuit tagged "episode 10", IR module + cup tagged "new" |
| ir_module | s05 | module turning, beam out of the emitter, bounce back into the receiver (stylized) |
| ir_out | s06 | hand in front: LED on, OUT tag "LOW" |
| ir_trim | s07 | screwdriver turns the trim pot |
| wire_keep | s08 | OLED, button, buzzer tagged "stays" |
| wire_ir | s09 | three wires: VCC 3V3, GND, OUT 13 |
| wire_cup | s10 | sensor taped under the cup, looking across the hole |
| play_start | s19 | finger presses button, whistle, OLED "time 30 s" |
| play_baskets | s20 | three baskets, score 1..3 with swish beeps |
| play_horn | s21 | timer 0, horn, OLED "NEW RECORD!" |
| trouble_sun | s22 | window light on the cup, score climbing alone (red X), then cup moved away |
| challenge | s23 | button held during a throw, tag "+3?" |
| outro | s25 | orbit, OLED "see you in" / "ep 17" |

## Motion Canvas scenes

| id | seg | what |
|---|---|---|
| ball_fast | s11 | timeline: ball in the beam for ~8 ms, a ruler in milliseconds |
| loop_miss | s12 | loop() timeline: "draw screen" block covers the 8 ms window, the digitalRead look misses it |
| doorbell | s13 | person walking to check the door vs a doorbell ringing (registry ep16) |
| interrupt | s14 | loop timeline paused by a bell, tiny `ballSeen()` block, loop carries on |
| code_attach | s15 | glimpse -> `attachInterrupt(digitalPinToInterrupt(IR_PIN), ballSeen, FALLING);` + HIGH->LOW edge drawing |
| code_tiny | s16 | `void IRAM_ATTR ballSeen()` body highlighted: count, time, done; crossed-out `show()` / `delay()` |
| code_volatile | s17 | `volatile int baskets = 0;` one-line highlight (no picture) |
| one_ball | s18 | sensor flicker 3 pulses -> only the first counts, 300 ms window, "Episode 4 button" chip |
| code_full | s24 | readable pages (codeFull `{pages: true}`) + lesson folder chip + comment bubble |

## Sounds

`assemble.piezo()`: whistle 1500 Hz 300 ms, swish 2000 Hz 80 ms per basket, horn 400 Hz 900 ms (all from the sketch) with
rings; paper ball throw (soft whoosh) and drop (paper tap); SFX_GAIN applies.

## Before production

Creator review of the script; check the hoop prop; episode-length decision (4-5 min vs 6-8 min).
