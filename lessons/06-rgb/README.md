# Episode 6 — Mix RGB Colors with One Button

One LED, any color you like: red, green, blue, and with a single press a slow fade from blue to red.
Today we mix colors with an RGB LED, write a helper function called `setColor()`, and let one button choose
between four color modes.

**You need:** the circuit from episode 5 (two breadboards, red LED on GPIO 23, button on GPIO 22), one RGB LED,
three more 220 Ω resistors and a few jumper wires.

## 1. Light adds up

Look at your phone screen from very close: it is made of tiny red, green and blue dots, and every color you see is a mix of
those three. An **RGB LED** is the same idea: three small LEDs (red, green, blue) in one package, sharing one leg,
the longest one.

The difference from paint: **light adds**. Red + green light = yellow (paint would give brown), and all three together = white.

| Mix | Color |
|---|---|
| red + green | yellow |
| red + blue | magenta (pink-purple) |
| green + blue | cyan (turquoise) |
| red + green + blue | white |

## 2. Wiring the RGB LED (upper breadboard)

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

**Why three resistors, not one on the shared leg?** Each color is its own LED with its own current. One shared
resistor is like three people drinking through one straw: whoever pulls hardest gets the most. In real life the colors
would steal current from each other and your mix would change (red, which needs the least voltage, wins).

**Common anode?** Most kits have common **cathode** RGB LEDs (long leg to GND). Upload `rgb_colors` once: if it shows
white when it should be off, yours is common **anode**: move the long leg to `3V3` and set `COMMON_ANODE = true`.

## 3. `setColor(r, g, b)` — [`code/rgb_colors`](code/rgb_colors/rgb_colors.ino)

`setColor()` is our own helper function, like the button on a coffee machine: one press mixes three ingredients.
Inside, it is three `analogWrite()` calls, one per color, each from 0 to 255. Unlike a coffee machine, it does not remember a recipe:
you give all three amounts every time you call it.

```c
// ESP32 From Zero - Episode 6: mix colors with an RGB LED
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
| `setup()` | Runs once: the three color pins become outputs. |
| `loop()` | Eight colors, one per second. Read each line as *red, green, blue*: `setColor(255, 255, 0)` = full red + full green = yellow. |

Quick question: `setColor(255, 0, 255)`? Red and blue: magenta. And `setColor(255, 40, 0)`? A little green in red: orange.
Green usually looks strongest, and magenta looks a bit blue, so the three colors are not equally bright: for a cleaner
white try `setColor(255, 200, 255)`.

## 4. One button, four modes — [`code/color_modes`](code/color_modes/color_modes.ino)

Think of the channel button on a TV remote: every new press adds one to a number, and after the last channel it goes
back to the first. `int mode` goes 0 → 1 → 2 → 3 → 0 on every new press (edge + 50 ms debounce from episode 4):
red, green, blue, and a slow blue-to-red fade with the same `millis()` step. Nothing ever waits.

```c
// ESP32 From Zero - Episode 6: one button, four color modes
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

**Line by line.** Nothing here is new: it is the button from episode 4, `setColor` from section 3 and the fade from episode 5, put together.

| Part | What it does |
|---|---|
| `mode` | Which mode we are in: 0 red, 1 green, 2 blue, 3 fade. |
| `level`, `step`, `lastStep` | Only for mode 3. Same idea as `brightness`, `step`, `lastStep` in `fade_millis`. `level` 0 = all blue, 255 = all red. |
| `lastState`, `lastChange` | The button's memory, exactly as in episode 4. |
| **Part 1 – the button** | The same press check as before. On a new press: `mode = mode + 1;`, and `if (mode > 3) mode = 0;` so 3 → 0 and the modes go round in a circle. The mode lives in memory, not on a screen, so we print it to check. |
| **Part 2 – the color** | One `if` per mode. `else if` means: only check the next one if the one before was false. The last `else` catches mode 3. |
| mode 3 | Every 8 ms `level` moves one step; it turns around at 255 and at 0, exactly like the fade. |
| `setColor(level, 0, 255 - level);` | Red gets `level`, blue gets the rest. At 0: all blue. At 128: half and half, purple. At 255: all red. |

Pause-and-predict check: with `level` at 128, the fade is purple (half red, half blue, 128 + 127 = 255 in total).
Press three times and you get red, green, blue, then the fade; a fourth press goes back to red, because after mode 3 the
counter starts again at 0. The button reacts at once, even in the middle of a fade.

## 5. Your turn: the smart camping headlamp — [`code/challenge_headlamp`](code/challenge_headlamp/challenge_headlamp.ino)

Build a camping headlamp. One button cycles **off → dim white → bright white → red blink**.
The twist: if the lamp has been on for **3 seconds or more**, the next press switches it **straight off**.
Hint: remember when the mode last changed. Post your solution in the comments; one solution is in the
[`challenge_headlamp`](code/challenge_headlamp/challenge_headlamp.ino) file. Try it yourself first.

## All sketches

| Sketch | What it does |
|---|---|
| [`rgb_colors`](code/rgb_colors/rgb_colors.ino) | eight colors with `setColor()` |
| [`color_modes`](code/color_modes/color_modes.ino) | the button cycles red, green, blue, fade |
| [`challenge_headlamp`](code/challenge_headlamp/challenge_headlamp.ino) | one solution to the challenge |

## Something not working?

- All three colors dark? Check the shared wire on the longest leg first: all three colors return to ground through it. One color alone is dark: check that color's resistor and wire (D25 red, D26 green, D27 blue).
- Everything inverted (white when it should be off)? Common anode: long leg to `3V3`, `COMMON_ANODE = true`.
- The mode seems wrong? Print `mode` to the Serial Monitor (115200 baud) and look at the number.
