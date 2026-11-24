# Episode 12 (DRAFT) — shot plan

Script: `make_script.py` (31 segments). Pipeline = Episode 10/11 v2 (HANDOFF.md): narration → schedule →
`b3d/ep12_3d.py` (copy of ep11_3d.py structure, one Blender process per shot, PBL_SAMPLES=16) → Motion Canvas
(`node video/mc/tools/timing.mjs ep12`, scenes prefixed `ep12_`) → `video/b3d/assemble.py video/ep12` → build.py
audio/subs/compose → ffprobe the final length.

## Circuit (nothing new on the board)

Ep 10 layout (OLED 21/22, button 19, buzzer 32) + the RGB LED from Ep 6 on GPIO 25/26/27 with three 220 Ω resistors,
common cathode to GND. No PIR (Ep 11 part is unplugged for this episode). Reuse `pbl.rgb_led()` / `pbl.resistor()`
(added for the treasure Short) and the Ep 10 wires from ep10_3d.py.

## New 3D parts (additive module `video/b3d/parts_ep12.py`)

- **Phone**: rounded slab ~70x150x8 mm (scale it down to desk-miniature like the Ep 11 hand), black glass front with a
  screen plane that shows a 2D image per frame (the web page: title + RED/GREEN/BLUE/OFF/RING buttons drawn with PIL,
  pressed button highlighted), side buttons. A finger tap = small glowing dot on the screen.
- **Radio ripples**: expanding translucent arcs from the ESP32's PCB antenna (the zig-zag at the module's end) and from
  the phone, value-node driven like pbl.sound_rings; a small glowing "packet" sphere that travels phone → board on taps.
- **Antenna highlight**: emissive outline of the ESP32 module's zig-zag antenna for s05.
- **Address label**: 2D overlay tag "192.168.4.1" floating over the board (house-number style card, not on the board).

## Shots (b3d)

| id | seg | what |
|---|---|---|
| open_tap | s01 | phone in the foreground, finger taps RED, packet flies, RGB LED turns red |
| open_ring | s02 | tap RING, buzzer plays two notes (rings), packet |
| open_count | s03 | OLED macro: "command #3" / "blue" counting up |
| open_orbit | s04 | orbit: phone + desk |
| wifi_rings | s05 | antenna highlight, ripples from the board |
| wifi_hotspot | s06 | board ripples form a bubble "PinByPin-ESP32" (2D tag), a crossed-out router icon (2D) |
| wifi_join | s07 | phone joins: its ripples meet the board's, tag "192.168.4.1" appears |
| wire_same | s14 | Ep 6 + Ep 10 parts tagged with their episodes |
| wire_rgb | s15 | RGB legs + resistors tagged with pins 25/26/27 |
| try_upload | s16 | USB, OLED "open 192.168.4.1" / "READY" |
| try_join | s17 | phone screen: Wi-Fi list, PinByPin-ESP32, password dots |
| try_page | s18 | phone screen: browser with the remote page |
| try_red | s19 | tap RED, packet, LED red, OLED "command #1" / "red" |
| try_packet | s19b | slow-motion packet: phone → board (tag "GET /color?c=red"), board → phone (page) |
| try_colors | s19c | green, blue, off in quick succession, counter 2..4 |
| try_ring | s20 | ring: two notes, rings |
| trouble_nointernet | s21 | phone shows "No internet - stay connected?" dialog |
| trouble_password | s22 | password field with 7 dots, red X, then 8 dots, check |
| trouble_address | s22b | address bar: "www.192..." red, "192.168.4.1" green |
| challenge | s23 | PARTY button pressed, LED cycles R/G/B three times |
| outro | s25 | orbit, OLED "see you in" / "ep 13" |

## Motion Canvas scenes

| id | seg | what |
|---|---|---|
| code_softap | s08 | glimpse → `WiFi.softAP("PinByPin-ESP32", "esp32lab");` + hotspot icon |
| page_menu | s09 | numbered restaurant menu card → the phone page (buttons = dishes with numbers) |
| page_links | s10 | buttons morph into `/color` and `/ring` links |
| code_on | s11 | glimpse → `server.on("/color", handleColor);` lines, link → helper arrows |
| code_loop | s12 | `server.handleClient();` in loop(), the night guard doing rounds (reuse picture) |
| order_slip | s12b | order slip with note "c = red" → `/color?c=red` |
| code_arg | s12c | `String c = server.arg("c");` + the three ifs → setColor |
| code_answer | s12d | `server.send(200, "text/html", PAGE);` page flies back to the phone |
| page_template | s13 | the PAGE template with only labels/colors highlighted as editable |
| code_full | s24 | full sketch scroll + lesson folder chip + comment bubble (reuse ep11_code_full) |

## Sounds

Buzzer = `assemble.piezo()` at the sketch's notes (ring: 1319 Hz 180 ms, then 1047 Hz 300 ms) with rings; a soft
"tap" click for each phone tap; a short whoosh (filtered noise) for packets. SFX_GAIN applies.
