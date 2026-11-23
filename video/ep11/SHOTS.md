# Episode 11 (DRAFT) — shot plan

Script: `make_script.py` (36 segments). Pipeline = Episode 10 v2 (see HANDOFF.md, "Episode 10 v2"): narration → schedule →
`b3d/ep11_3d.py` (copy of ep10_3d.py structure, one Blender process per shot, PBL_SAMPLES=16) → Motion Canvas scenes
(`video/mc`, timing from schedule.json) → `video/b3d/assemble.py video/ep11` → build.py audio/subs/compose.

## New 3D parts needed in `video/b3d/pbl.py` (additive only)

- **HC-SR501 PIR**: green PCB 32×24 mm, white faceted Fresnel dome (Ø23 mm, ~15 mm high, hexagonal facets), 3 header pins
  (VCC, OUT, GND) on one edge, two orange trim pots (time, sensitivity) with turnable slots, a yellow jumper (L/H).
  Methods: `k.pir(at, rot)` → `{"group", "dome", "pot_time", "pot_sens", "pins": {...}}`; `k.pir_zones(pir)` → fan of
  translucent beams (8-10 wedges, emission, per-beam value node like `sound_rings`) to show the lens windows.
- **Warm hand**: a stylised low-poly hand with an emissive orange "heat" shader (for the IR glow shots) — or a simple
  glowing capsule if the hand looks bad. Cookie jar: glass cylinder + lid + 3 cookies (toon-ish).
- **Active buzzer** twin of the passive one: same body, sealed bottom + white sticker; x-ray shows an oscillator chip.
- ESP32 `VIN` pin label must exist (`k.esp32(hot={"VIN", ...})`).

## Circuit (Ep 10 layout + PIR)

PIR on the back board B, right of the OLED, dome facing the camera; VIN → PIR VCC (red), GND → PIR GND (black),
GPIO 33 → PIR OUT (purple). Hole coordinates are chosen in ep11_3d.py like ep10's, tags with printed hole names.

## Shots (b3d) — 3D share ≈ 80 % by words

| id | seg | what |
|---|---|---|
| open_arm | s01 | button press, OLED "leave the room! 10 s", ticks (beeps + rings) |
| open_catch | s02 | glowing hand reaches toward the jar, beams light up zone by zone, OLED "INTRUDER", siren (lo/hi rings) |
| open_ago | s03 | press, OLED "seen 1x, last: 2 min ago" |
| open_orbit | s04 | slow orbit of the whole desk |
| pir_hero | s05 | macro of the dome, slow push-in |
| pir_glow | s06 | "thermal" look: hand, cat silhouette, tea cup glow orange (emission), the rest goes dark blue |
| pir_lens | s07 | x-ray: dome becomes see-through, fan of beam wedges appears window by window |
| pir_zones | s08 | warm hand crosses wedge → wedge (each lights), OUT pin wire pulses, "HIGH" tag |
| pir_answer | s09 | thumbs-up / thumbs-down tag (2D overlay) following OUT HIGH/LOW |
| pir_knobs | s10 | close-up, the two trim pots turn; tags "time", "range" |
| pir_warmup | s11 | power on, 30 s counter tag fast-forwarding, random flickers of OUT during warm-up |
| wire_keep | s12 | Ep 10 circuit, OLED/button/buzzer tagged "stays" |
| wire_pir_power | s13 | red VIN → VCC, black GND → GND, hole tags |
| wire_pir_out | s14 | purple 33 → OUT, hole tags |
| wire_pir_done | s15 | 3.3 V tag on OUT, "safe" check |
| demo_countdown | s18 | press, countdown 10..0 with ticks |
| demo_armed | s19 | OLED "ARMED", beams idle-pulse |
| demo_stop | s21 | siren running, press, silence |
| screen_ago | s25 | OLED macro "seen 2x, last: 3 min ago" |
| buzzers_two | s26 | passive + active side by side, slow turn (bottoms visible) |
| buzzers_xray | s27 | x-ray: passive disc only / active disc + oscillator chip |
| buzzers_siren | s28 | passive plays the two-tone siren (rings), active one fixed beep |
| demo_walkout | s29 | arm, countdown, camera pulls back "out of the room" |
| demo_cookie | s30 | hand → jar, caught, siren |
| demo_back | s31 | press, OLED "seen 1x, last: 12 s ago" |
| mistake_false | s32 | arm → immediately alarm; tags "warming up", "time knob high" |
| mistake_fix | s33 | time pot turns to minimum, re-arm, calm |
| challenge | s34 | unplug/replug, OLED keeps "caught so far: 3" |
| outro | s36 | orbit, OLED "see you in ep 12" |

## Motion Canvas scenes

| id | seg | what |
|---|---|---|
| code_read | s16 | full-code glimpse → `bool motion = digitalRead(PIR_PIN) == HIGH;`, a HIGH/LOW toggle with a thumb icon |
| alarm_steps | s17 | the washing-machine dial (reuse ep10 `steps`): OFF → LEAVING → ARMED → ALARM |
| code_siren | s20 | glimpse → `tone(BUZZER_PIN, (inState / 250) % 2 ? 2600 : 1800);`, two notes alternating on a timeline |
| parking_ticket | s22 | the Ep 9 parking ticket stamped with the time at the moment of motion |
| code_last | s23 | `lastMotion = now;` + a stopwatch (millis) running since power-on |
| ago_calc | s24 | `now - lastMotion` → 180000 ms → ÷ 60000 → "3 min ago" counter |
| code_full | s35 | full sketch scroll + lesson folder chip + "link below" + comment bubble (reuse ep10 `code_full`) |

## Sounds

Buzzer = `assemble.piezo()` at the sketch's notes: countdown tick 2000 Hz 30 ms, siren alternating 1800/2600 Hz every
250 ms, active buzzer comparison = fixed ~2.3 kHz. Every buzzer sound gets sound-wave rings (beeps in shots.json).
