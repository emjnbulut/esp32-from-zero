# Episode 17 (DRAFT, not reviewed) — shot plan

Script: `make_script.py` (25 segments, ~2.9 min narration + 20 s code pages). Pipeline = Episode 10-12 v2 (HANDOFF.md):
narration -> schedule -> `b3d/ep17_3d.py` (copy of ep12_3d.py: phone on its stand, radio ripples, packets, phone screens
via `video/ep12/b3d/phone_screens.py` with a new "Desk fan" page) -> Motion Canvas (`timing.mjs ep17`, scenes prefixed
`ep17_`) -> `video/b3d/assemble.py video/ep17` -> build.py audio/subs/compose -> ffprobe + Whisper on the ending.

## Circuit

Relay module (VCC -> VIN 5 V, GND, IN1 -> 16), USB desk fan whose + wire runs through relay 1 COM -> NO, OLED 21/22.
No buzzer, no button on the board in this episode (unplug the Ep 10 ones or leave them dim in the background).
SAFETY: every shot with the fan shows a small "5 V USB only" tag; never a wall plug anywhere in the scene.

## New 3D parts (additive module `video/b3d/parts_ep17.py`)

- **2-channel relay module**: PCB with two blue relay cubes ("SRD-05VDC" style, no brand), screw terminals (NO COM NC) per
  channel, input header (GND IN1 IN2 VCC), two red channel LEDs.
- **Relay cutaway** (for s07): transparent cube, copper coil, metal arm that snaps over on a keyframe, contact spark.
- **USB desk fan**: round stand fan with a USB cable; blades spin (driver on the relay state) with a slight blur.
- **Phone page**: "Desk fan" page with ON (green), ON for 10 min (blue), OFF (red), matching the sketch's PAGE colours.

## Shots (b3d)

| id | seg | what |
|---|---|---|
| open_click | s01 | finger taps ON, packet flies, relay LED + click, fan spins up |
| open_timer | s02 | tap "ON for 10 min", OLED "fan on, off in 10 min" |
| open_orbit | s03 | orbit: phone, board, relay, fan |
| open_title | s04 | Ep 12 phone page tagged "episode 12", relay + fan tagged "new" |
| safety | s05 | USB fan + USB lamp with a green check, a wall socket icon (2D) with a red X |
| relay_module | s06 | module turning, terminal labels |
| relay_inside | s07 | cutaway: coil glows, arm snaps over, contact closes, click |
| relay_two | s08 | two coloured loops: pin -> coil (blue), fan power -> contact (orange), never touching |
| wire_relay | s10 | VIN, GND, IN1 -> 16 wires go in |
| wire_fan | s11 | fan + wire into COM, out of NO; NC tagged "not used" |
| wire_screen | s12 | OLED tagged "stays (21/22)" |
| boot_click | s14 | board plugged in, relay clicks on briefly by itself (red flash) |
| try_on | s19 | Wi-Fi list -> page -> tap ON -> click, fan spins |
| try_timer | s20 | tap 10 min, OLED counts down 10 -> 9 (time-lapse) |
| try_off | s21 | OLED "1 min" -> click, fan slows down and stops |
| trouble_reverse | s22 | wire on NC: tap OFF, fan runs (red X); wire moved one hole to NO (check) |
| challenge | s23 | second relay with a USB lamp, tag "pin 17 - your turn" |
| outro | s25 | orbit, OLED "see you in" / "ep 18" |

## Motion Canvas scenes

| id | seg | what |
|---|---|---|
| two_circuits | s09 | two separate circuits side by side: 3.3 V pin + coil, 5 V + fan through the contact |
| active_low | s13 | LOW -> relay ON, HIGH -> OFF, a light-switch icon flipping "upside down" |
| code_boot | s15 | `digitalWrite(RELAY1, RELAY_OFF);` before `pinMode(RELAY1, OUTPUT);` order swap animation |
| page_again | s16 | Episode 12 page morphs into the "Desk fan" page (hotspot + menu named only) |
| code_links | s17 | `server.on("/on", handleOn);` x3 -> `setFan(true/false)` |
| code_timer | s18 | `offAt = millis() + 10 min` + parking ticket "valid until" card, `(long)(now - offAt) >= 0` |
| code_full | s24 | readable pages (codeFull `{pages: true}`) + lesson folder chip + comment bubble |

## Sounds

Relay click (`assemble.SFX` "click", a bit louder and sharper), fan motor hum (low filtered noise, follows the spin),
phone tap + packet whoosh (Ep 12 kinds). No piezo in this episode.

## Before production

Creator review of the script + the relay analogy; the safety wording; episode-length decision (4-5 min vs 6-8 min).
Sketch TODO: "auto above 28 C" with the Episode 13 DHT11 - decide after Ep 13 exists.
