# Episode 5 — PWM and RGB Color Mixing

A pin can only be on or off. Switch it fast enough, and an LED glows at any brightness you like.
Today we dim and fade an LED with `analogWrite()`, build a fade that never waits, and mix colors with an RGB LED.

**You need:** the circuit from episode 4 (two breadboards, red LED on GPIO 23, button on GPIO 22), one RGB LED,
three more 220 Ω resistors and a few jumper wires. A multimeter is a nice extra.

## 1. PWM in one picture

`digitalWrite` gives two choices: fully on or fully off. **PWM** (pulse width modulation) switches the pin on and off
about a thousand times a second. What changes is how long it stays on in each cycle, the **duty cycle**:
25 % looks dim, 50 % medium, 100 % fully bright. Your eye (and a multimeter) sees the average.

## 2. `analogWrite(pin, 0..255)` — [`code/pwm_levels`](code/pwm_levels/pwm_levels.ino)

| value | duty cycle | multimeter on the pin (average) |
|---|---|---|
| 0 | 0 % | 0 V |
| 64 | 25 % | ≈ 0.8 V |
| 128 | 50 % | ≈ 1.65 V |
| 255 | 100 % | 3.3 V |

On the ESP32 almost every output pin can do PWM.

## 3. A fade that never waits — [`code/fade_millis`](code/fade_millis/fade_millis.ino)

The naive way, a `for` loop with `delay()` on every step, blocks the button for a whole fade (episode 4's problem).
Instead: every 4 ms, `brightness = brightness + step`; at 255 the step becomes −1, at 0 it becomes +1 again.
A press pauses or resumes the fade at once. Open **Tools → Serial Plotter** to see the brightness as a triangle.
Quick question: 4 ms → 10 ms? The triangle gets wider (≈ 2.5 s per fade); the height stays 0–255.

## 4. Wiring the RGB LED (upper breadboard)

1. **Unplug the USB cable.** Remove the green LED circuit from episode 4 (green wire, resistor, LED, its black wire).
   Keep the black wire from the top `GND` pin (column 3) to the upper minus rail.
2. **RGB LED** in row `c`, columns 20–23, the **longest leg second from the left**: red 20, common 21, green 22, blue 23.
3. **Black wire:** column 21 → the upper minus rail.
4. **Red:** wire `D25` (column 9) → column 20 (bottom half, row g), 220 Ω resistor from `f20` across the gap to `e20`.
5. **Green:** wire `D26` (column 8) → column 22 (row h), 220 Ω resistor `f22` → `e22`.
6. **Blue:** wire `D27` (column 7) → column 23 (row i), 220 Ω resistor `f23` → `e23`.

```
GPIO 25 ──► 220 Ω ──► red   ┐
GPIO 26 ──► 220 Ω ──► green ├─ RGB LED ── common leg ──► − rail ──► GND
GPIO 27 ──► 220 Ω ──► blue  ┘
```

Each color has its own resistor: they are three separate LEDs with their own current.

**Common anode?** Most kits have common **cathode** RGB LEDs (long leg to GND). Upload `rgb_colors` once: if it shows
white when it should be off, yours is common **anode**: move the long leg to `3V3` and set `COMMON_ANODE = true`.

## 5. `setColor(r, g, b)` — [`code/rgb_colors`](code/rgb_colors/rgb_colors.ino)

```cpp
void setColor(int r, int g, int b) {
  analogWrite(RED_PIN, r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}
```

Red + green = yellow, red + blue = magenta, green + blue = cyan, all three = white, 255/40/0 = orange.
Green usually looks strongest: for a cleaner white try `setColor(255, 200, 255)`.

## 6. One button, four modes — [`code/color_modes`](code/color_modes/color_modes.ino)

`int mode` goes 0 → 1 → 2 → 3 → 0 on every new press (edge + 50 ms debounce from episode 4):
red, green, blue, and a slow blue-to-red fade with the same `millis()` step. Nothing ever waits.

## 7. Your turn: the smart camping headlamp — [`code/challenge_headlamp`](code/challenge_headlamp/challenge_headlamp.ino)

One button cycles **off → dim white → bright white → red blink**. The twist: if the lamp has been on for
**3 seconds or more**, the next press switches it **straight off**. Hint: remember when the mode last changed
(`lastPress`, like `lastBlink`). Post your solution in the comments; one solution is in the folder — try it yourself first.

## All five sketches

| Sketch | What it does |
|---|---|
| [`pwm_levels`](code/pwm_levels/pwm_levels.ino) | 0 → 25 → 50 → 100 %, two seconds each |
| [`fade_millis`](code/fade_millis/fade_millis.ino) | a breathing LED, the button pauses it |
| [`rgb_colors`](code/rgb_colors/rgb_colors.ino) | eight colors with `setColor()` |
| [`color_modes`](code/color_modes/color_modes.ino) | the button cycles red, green, blue, fade |
| [`challenge_headlamp`](code/challenge_headlamp/challenge_headlamp.ino) | one solution to the challenge |

## Something not working?

- One color never lights? Check that leg's resistor and wire (D25 red, D26 green, D27 blue).
- Everything inverted (white when it should be off)? Common anode: long leg to `3V3`, `COMMON_ANODE = true`.
- No fade at all? The pin must be set with `pinMode(pin, OUTPUT)`.
