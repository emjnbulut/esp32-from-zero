# Pin by Pin Lab — extra projects

Small, real things you can build with what the course has taught so far. Every project uses **only** syntax and
parts from the episodes it lists — no surprise functions or libraries. Each one is also a short Reel / YouTube Short.

| # | Project | Needs episodes | Parts (the course circuit) | Sketch |
|---|---|---|---|---|
| 01 | SOS beacon | 1–3 | red LED on GPIO 23 | [`sos_beacon`](01-sos-beacon/sos_beacon/sos_beacon.ino) |
| 02 | Pomodoro focus light | 1–4 | red LED 23, green LED 25, button 22 | [`pomodoro_light`](02-pomodoro-light/pomodoro_light/pomodoro_light.ino) |
| 03 | Sunrise light | 1–5 | RGB LED 25/26/27, button 22 | [`sunrise_light`](03-sunrise-light/sunrise_light/sunrise_light.ino) |
| 04 | Electric candle | 1–5 | RGB LED 25/26/27, button 22 | [`candle_light`](04-candle-light/candle_light/candle_light.ino) |

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
