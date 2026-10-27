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

```c
// ESP32 From Zero - Episode 5: PWM levels
// Red LED on GPIO 23 (episode 3 circuit). analogWrite(pin, 0..255) sets the brightness.
// What it does: the LED steps 0% -> 25% -> 50% -> 100%, two seconds each, and prints every step.
// (A multimeter on the LED pin shows the average voltage of each step.)

const int LED_PIN = 23;        // the red LED's pin

void setup() {
  pinMode(LED_PIN, OUTPUT);    // we drive this pin
  Serial.begin(115200);        // so we can print to the Serial Monitor
}

// Our own function. "value" is the number we hand it each time we call it (0..255).
// It sets the brightness, prints what it did, and holds that level for 2 seconds.
void showLevel(int value) {
  analogWrite(LED_PIN, value);       // 0 = always off, 255 = always on, in between = dimmer or brighter
  Serial.print("analogWrite ");
  Serial.print(value);
  Serial.print(" = ");
  Serial.print(value * 100 / 255);   // the same value as a percentage
  Serial.println("% on");
  delay(2000);                       // keep this level for 2 seconds
}

void loop() {
  showLevel(0);     // off
  showLevel(64);    // about 25%
  showLevel(128);   // about 50%
  showLevel(255);   // fully on
}                   // then loop() starts again from the top
```

**Line by line**

| Part | What it does |
|---|---|
| `const int LED_PIN = 23;` | Gives pin 23 a name, so the code says *what* the pin is for. |
| `setup()` | Runs once: the pin becomes an output, and the Serial Monitor connection starts. |
| `void showLevel(int value)` | **Our own function.** `void` means it gives nothing back. `int value` is a box for the number we hand it each time we call it. |
| `analogWrite(LED_PIN, value);` | Sets the brightness: 0 = always off, 255 = always on, anything in between is dimmer or brighter. |
| `value * 100 / 255` | The same number as a percentage, just for printing. 64 → 25. |
| `delay(2000);` | Holds that level for two seconds (here waiting is fine: there is no button to listen to). |
| `loop()` | Calls `showLevel` four times with 0, 64, 128 and 255, then starts again from the top. |

## 3. A fade that never waits — [`code/fade_millis`](code/fade_millis/fade_millis.ino)

The naive way, a `for` loop with `delay()` on every step, blocks the button for a whole fade (episode 4's problem).
Instead: every 4 ms, `brightness = brightness + step`; at 255 the step becomes −1, at 0 it becomes +1 again.
A press pauses or resumes the fade at once. Open **Tools → Serial Plotter** to see the brightness as a triangle.
Quick question: 4 ms → 10 ms? The triangle gets wider (≈ 2.5 s per fade); the height stays 0–255.

```c
// ESP32 From Zero - Episode 5: a smooth fade that never waits
// Red LED on GPIO 23, button on GPIO 22 (internal pull-up, from episode 4).
// What it does: the LED slowly gets brighter, then dimmer, again and again (it "breathes").
// A button press pauses the fade, the next press resumes it. Nothing ever waits with delay().

const int LED_PIN = 23;
const int BUTTON_PIN = 22;

// --- the fade ---
int brightness = 0;            // the LED's brightness right now: 0 (off) .. 255 (full)
int step = 1;                  // what we add every time: +1 = getting brighter, -1 = getting dimmer
unsigned long lastStep = 0;    // the time of the last step, in ms
bool fading = true;            // true = the LED breathes, false = paused

// --- the button (same as episode 4) ---
int lastState = HIGH;          // the button's reading last time round (HIGH = not pressed)
unsigned long lastChange = 0;  // when that reading last changed, to ignore the bounce

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // built-in pull-up: HIGH when not pressed, LOW when pressed
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();  // the clock: milliseconds since the board started

  // PART 1 - the button: a NEW press flips "fading" (pause <-> resume)
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {  // it changed, and it's not bounce
    lastChange = now;
    lastState = state;
    if (state == LOW) {        // the change was a press, not a release
      fading = !fading;        // true becomes false, false becomes true
    }
  }

  // PART 2 - the fade: every 4 ms, one small step (255 steps up = about 1 second)
  if (fading && now - lastStep >= 4) {
    lastStep = now;                    // remember when this step happened
    brightness = brightness + step;    // one step brighter (+1) or dimmer (-1)
    if (brightness >= 255) {           // reached the top?
      brightness = 255;
      step = -1;                       // from now on, go down
    }
    if (brightness <= 0) {             // reached the bottom?
      brightness = 0;
      step = 1;                        // from now on, go up
    }
    analogWrite(LED_PIN, brightness);  // show the new brightness on the LED
    Serial.println(brightness);        // Tools > Serial Plotter draws this as a triangle
  }
}
```

**Line by line.** The sketch has three kinds of variables and a `loop()` in two parts.

| Part | What it does |
|---|---|
| `brightness` | How bright the LED is right now, 0 to 255. |
| `step` | What we add every time: **+1** while getting brighter, **−1** while getting dimmer. Flipping `step` is how the fade turns around. |
| `lastStep` | The clock time of the last step. `unsigned long` because `millis()` gets big. |
| `fading` | `true` = breathing, `false` = paused. The button flips it. |
| `lastState`, `lastChange` | The button's memory, exactly as in episode 4: the last reading, and when it last changed. |
| `now = millis();` | Reads the clock once at the top of every loop. |
| **Part 1 – the button** | `state != lastState` = the reading changed. `now - lastChange >= 50` = it's not contact bounce. `state == LOW` = it was a press, not a release. Then `fading = !fading;` swaps pause and resume. |
| **Part 2 – the fade** | Only when `fading` is true **and** 4 ms have passed since `lastStep`. Then: note the time, add `step` to `brightness`. |
| `if (brightness >= 255)` | At the top: stay at 255 and set `step = -1`, so from now on it goes down. |
| `if (brightness <= 0)` | At the bottom: stay at 0 and set `step = 1`, so it goes up again. |
| `analogWrite(LED_PIN, brightness);` | Shows the new brightness on the LED. |

The loop never waits, so it checks the button thousands of times a second, and a press works even in the middle of a fade.

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

```c
// ESP32 From Zero - Episode 5: mix colors with an RGB LED
// RGB LED on the upper breadboard: red leg -> 220 ohm -> GPIO 25, green -> 220 ohm -> GPIO 26,
// blue -> 220 ohm -> GPIO 27, the longest (common) leg -> minus rail (GND).
// What it does: shows 8 colors, one per second: red, green, blue, yellow, magenta, cyan, white, orange.
// If the colors come out inverted (white when it should be off), your LED is common anode:
// move its long leg to 3V3 and set COMMON_ANODE to true.

const int RED_PIN = 25;        // one pin for each of the three tiny LEDs inside
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const bool COMMON_ANODE = false;  // false for most kits (long leg to GND)

// Our helper: one line sets any color. r, g, b = how bright red, green and blue are (0..255 each).
void setColor(int r, int g, int b) {
  if (COMMON_ANODE) {          // common anode works the other way round: 255 means off
    r = 255 - r;               // so we flip every value: 0 <-> 255
    g = 255 - g;
    b = 255 - b;
  }
  analogWrite(RED_PIN, r);     // PWM on each color's pin
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {
  //       red  green blue
  setColor(255,   0,   0); delay(1000);  // red
  setColor(  0, 255,   0); delay(1000);  // green
  setColor(  0,   0, 255); delay(1000);  // blue
  setColor(255, 255,   0); delay(1000);  // red + green = yellow
  setColor(255,   0, 255); delay(1000);  // red + blue = magenta
  setColor(  0, 255, 255); delay(1000);  // green + blue = cyan
  setColor(255, 255, 255); delay(1000);  // all three = white
  setColor(255,  40,   0); delay(1000);  // a little green in red = orange
}
```

**Line by line**

| Part | What it does |
|---|---|
| `RED_PIN`, `GREEN_PIN`, `BLUE_PIN` | One pin for each of the three tiny LEDs inside the RGB LED. |
| `COMMON_ANODE` | `false` for most kits. Set it to `true` only if your colors come out inverted. |
| `void setColor(int r, int g, int b)` | Our helper. It takes **three** numbers: how bright red, green and blue should be (0–255 each). |
| `if (COMMON_ANODE) { r = 255 - r; ... }` | A common anode LED works the other way round (255 = off), so we flip each value: 0 ↔ 255, 40 ↔ 215. |
| `analogWrite(...)` ×3 | PWM on each color's pin. That's the whole trick: three brightnesses, one mixed color. |
| `loop()` | Eight colors, one per second. Read each line as *red, green, blue*: `setColor(255, 255, 0)` = full red + full green = yellow. |

Red + green = yellow, red + blue = magenta, green + blue = cyan, all three = white, 255/40/0 = orange.
Green usually looks strongest: for a cleaner white try `setColor(255, 200, 255)`.

## 6. One button, four modes — [`code/color_modes`](code/color_modes/color_modes.ino)

`int mode` goes 0 → 1 → 2 → 3 → 0 on every new press (edge + 50 ms debounce from episode 4):
red, green, blue, and a slow blue-to-red fade with the same `millis()` step. Nothing ever waits.

```c
// ESP32 From Zero - Episode 5: one button, four color modes
// RGB LED on GPIO 25/26/27 (see rgb_colors), button on GPIO 22.
// What it does: each press moves to the next mode: 0 red, 1 green, 2 blue, 3 a slow blue <-> red fade,
// then back to 0. The button always reacts at once, because nothing ever waits.

const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int BUTTON_PIN = 22;
const bool COMMON_ANODE = false;

int mode = 0;                  // which mode we are in: 0, 1, 2 or 3
int level = 0;                 // mode 3 only: the fade, 0 (all blue) .. 255 (all red)
int step = 1;                  // mode 3 only: +1 = towards red, -1 = back towards blue
unsigned long lastStep = 0;    // mode 3 only: the time of the last fade step (ms)

int lastState = HIGH;          // the button, as in episode 4
unsigned long lastChange = 0;

// the same helper as in rgb_colors: one line sets any color
void setColor(int r, int g, int b) {
  if (COMMON_ANODE) {
    r = 255 - r;
    g = 255 - g;
    b = 255 - b;
  }
  analogWrite(RED_PIN, r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  // PART 1 - the button: every new press goes to the next mode
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {        // a new press
      mode = mode + 1;         // next mode
      if (mode > 3) {
        mode = 0;              // after the last mode (3), start again at 0
      }
      Serial.print("mode ");
      Serial.println(mode);
    }
  }

  // PART 2 - the color for the current mode
  if (mode == 0) {
    setColor(255, 0, 0);       // red
  } else if (mode == 1) {
    setColor(0, 255, 0);       // green
  } else if (mode == 2) {
    setColor(0, 0, 255);       // blue
  } else {
    // mode 3: fade from blue to red and back, one step every 8 ms (like fade_millis)
    if (now - lastStep >= 8) {
      lastStep = now;
      level = level + step;
      if (level >= 255) {
        level = 255;
        step = -1;             // all red: turn back
      }
      if (level <= 0) {
        level = 0;
        step = 1;              // all blue: turn back
      }
    }
    setColor(level, 0, 255 - level);  // more red = less blue; together always 255
  }
}
```

**Line by line.** Nothing here is new: it is the button from episode 4, `setColor` from section 5 and the fade from section 3, put together.

| Part | What it does |
|---|---|
| `mode` | Which mode we are in: 0 red, 1 green, 2 blue, 3 fade. |
| `level`, `step`, `lastStep` | Only for mode 3. Same idea as `brightness`, `step`, `lastStep` in `fade_millis`. `level` 0 = all blue, 255 = all red. |
| **Part 1 – the button** | The same press check as before. On a new press: `mode = mode + 1;`, and `if (mode > 3) mode = 0;` so 3 → 0 and the modes go round in a circle. |
| **Part 2 – the color** | One `if` per mode. `else if` means: only check the next one if the one before was false. The last `else` catches mode 3. |
| mode 3 | Every 8 ms `level` moves one step; it turns around at 255 and at 0, exactly like the fade. |
| `setColor(level, 0, 255 - level);` | Red gets `level`, blue gets the rest. At 0: all blue. At 128: half and half, purple. At 255: all red. |

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
