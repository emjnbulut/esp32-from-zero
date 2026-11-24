# Pin by Pin Lab — extra projects

Small, real things you can build with what the course has taught so far. Every project uses **only** syntax and
parts from the episodes it lists — no surprise functions or libraries. Each one is also a short Reel / YouTube Short.

| # | Project | Needs episodes | Parts (the course circuit) | Sketch |
|---|---|---|---|---|
| 01 | SOS beacon | 1–3 | red LED on GPIO 23 | [`sos_beacon`](01-sos-beacon/sos_beacon/sos_beacon.ino) |
| 02 | Pomodoro focus light | 1–4 | red LED 23, green LED 25, button 22 | [`pomodoro_light`](02-pomodoro-light/pomodoro_light/pomodoro_light.ino) |
| 03 | Sunrise light | 1–5 | RGB LED 25/26/27, button 22 | [`sunrise_light`](03-sunrise-light/sunrise_light/sunrise_light.ino) |
| 04 | Electric candle | 1–5 | RGB LED 25/26/27, button 22 | [`candle_light`](04-candle-light/candle_light/candle_light.ino) |
| 05 | Treasure detector | 1–8 | knob 34, button 22, RGB LED 25/26/27, red LED 23 | [`treasure_detector`](05-treasure-detector/treasure_detector/treasure_detector.ino) |
| 06 | Secret knock lock | 1–9 | the episode 9 circuit: LEDs 23/18/17, RGB 25/26/27, button 22 (no new wire) | [`secret_knock_lock`](06-secret-knock-lock/secret_knock_lock/secret_knock_lock.ino) |
| 07 | 2-Axis 3D Gimbal Maze (Blender + X-Ray Breadboard) | Standalone Short | ESP32 DevKit V1, KY-023 joystick (`3.3V`, `D34`, `D35`), 2× MG90S/SG90 servos (`5V`, `D18`, `D19`), 470µF capacitor, 3D-printed gimbal (`stl/`) | [`esp32_gimbal_maze`](07-gimbal-maze/esp32_gimbal_maze/esp32_gimbal_maze.ino) · [Full guide & 3D files](07-gimbal-maze/README.md) |
| 08 | Treasure Detector 2.0 (Hazine Dedektörü 2.0) | 1–10 | the episode 10 circuit (OLED 21/22, button 19, passive buzzer 32) + knob 34 + RGB LED 25/26/27 | [`treasure_detector_2`](08-treasure-detector-2/treasure_detector_2/treasure_detector_2.ino) · [README](08-treasure-detector-2/README.md) |

The wiring is always the circuit from the episodes: see `lessons/03-blink-an-led`, `lessons/04-buttons-and-millis`
(two breadboards) and `lessons/05-pwm-and-rgb` (RGB LED).

## 01 · SOS beacon
The red LED blinks `... --- ...` forever. Morse timing: a dot is 1 unit (200 ms), a dash 3, the gap inside a letter
1, between letters 3, between words 7. Two helper functions, `letterS()` and `letterO()`, built on one `flash(units)`.
Try: change `UNIT` to 120 for a faster beacon, or spell your own name.

## 02 · Pomodoro focus light
Press: a focus round starts. The red LED blinks slowly, faster after half the time, and very fast in the last fifth.
Time's up: green on. Press again for a new round. The demo uses 25 s; set `FOCUS_TIME` to `1500000` for a real
25-minute Pomodoro. Built on `millis()` and the button edge from episode 4.

## 03 · Sunrise light
Press: a 60-second sunrise on the RGB LED. Deep red → orange in the first 30 s, then green and blue catch up to a
warm white. Press again: off. The color is computed from the elapsed time: `r = t * 255 / HALF`.
Try: make `HALF` 15 minutes (`900000`) for a real wake-up light.

## 04 · Electric candle
An orange flame that flickers like a real candle; a press blows it out or lights it again. There is no `random()`:
a tiny number generator, `seed = seed * 109 + 89`, gives a new brightness (150–255) and a new wait (40–149 ms)
every flicker. Try: a blue "magic" flame, or a calmer candle with a longer wait.

If your RGB LED is common anode, set `COMMON_ANODE = true` and move its long leg to 3V3 (episode 5).

## 05 · Treasure detector
A treasure is hidden somewhere on the knob (0 .. 99). Far away the RGB LED glows cold blue and the red LED "beeps"
slowly; closer, the colour warms up to red and the beeps get faster, like a metal detector. Press the button on the
spot: a rainbow party, and the treasure hides somewhere new. `distance = number - secret` (flipped if negative),
`heat = map(distance, 0, 50, 255, 0)`, `beepEvery = map(distance, 0, 50, 40, 700)`.
Try: make the "on it" zone smaller (`distance <= 1`) for a harder game. Made as a 3D Short (`video/short3d/treasure`).

## 06 · Secret knock lock
Only one rhythm opens it: **short, short, long**. Every press is timed like the parking ticket in episode 9
(`held = now - pressStart`, under 250 ms = short). One variable, `step`, counts the right beats (the `state` idea).
Red LED = locked, yellow = lit while you hold, RGB = progress (dim blue, blue, cyan). A wrong beat flashes red and
the lock forgets; 3 s of quiet forgets too. The whole rhythm: rainbow, green LED, open for 2.5 s, then locked again.
Same circuit as episodes 8-10, no new wire. Try: change the rhythm (the `want` lines), or make it four beats long.

## 07 · 2-Axis 3D Gimbal Maze (Blender + X-Ray Breadboard Short)
A curriculum-independent 3D-printed 2-axis marble maze controlled by an analog joystick (`GPIO 34`/`35` on `3.3V`) and
two MG90S/SG90 micro servos (`GPIO 18`/`19` on `5V`), designed to teach **how breadboard rails, vertical 5-hole spring
clips, common GND, and signal wires work** without diving into code. Includes parametric Blender 5.2 scripts, support-free
3D printable STLs, an interactive X-Ray HTML simulator, and a 360-frame `1080×1920` step-by-step breadboard assembly
animation: see [`07-gimbal-maze/README.md`](07-gimbal-maze/README.md).

## 08 · Treasure Detector 2.0 (Hazine Dedektörü 2.0)
Project 05 grown up with the episode 10 parts: the knob hides a treasure (0..99), the RGB LED goes ice blue -> red,
the passive buzzer ticks faster and higher like a Geiger counter, and the OLED shows SOĞUK / ILIK / SICAK / YANIYOR! with
a hot-cold meter. The button digs: right spot = fanfare, HAZİNE! and your time (best time kept with `Preferences`,
it survives unplugging); wrong spot = a low buzz, BOŞ!. Details in [`08-treasure-detector-2/README.md`](08-treasure-detector-2/README.md).
Made as a Turkish 3D Short (`video/short3d/treasure_tr`).
