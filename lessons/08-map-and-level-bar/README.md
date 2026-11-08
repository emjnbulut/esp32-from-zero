# Episode 8 — ESP32 `map()`: Build a 3-LED Level Bar

Last time we squeezed the knob's big scale into the LED's small one by dividing by 16. It worked, but anyone reading the code
has to figure out where the 16 came from. Today we meet `map()`, which does that job in one readable line, and we use it
to build a **level bar** that fills up like a volume meter.

**You need:** the circuit from episode 7 (the knob on GPIO 34 and the red LED on GPIO 23), one yellow LED, one green LED,
a 220 Ω resistor for each of them, and a few jumper wires.

## 1. A quick look back

- **The knob in the middle:** `analogRead()` gives roughly **2000**, half of the ruler. The whole ruler goes up to about 4095.
- **The LED ignores the knob:** print the value first, like a doctor taking your temperature. The number tells you which half of the circuit to check.

## 2. `map()` is a city map

Think of a city map. Every street in the city has its matching spot on the paper, and halfway across town is halfway across the map.
Arduino has a function with exactly that name:

```c
map(value, fromLow, fromHigh, toLow, toHigh)
```

You give it a number, the range it comes from, and the range you want, and it gives back the matching number.
It works out how far along the first range your number is, and returns the same position in the second range.
For the knob and the LED:

```c
int brightness = map(value, 0, 4095, 0, 255);   // from range 0..4095 to range 0..255
```

- The first number is the **knob's value**.
- The next two are where the **knob's range** starts and ends (0 to 4095).
- The last two are where the **brightness range** starts and ends (0 to 255).

Pause-and-predict: the knob reads about 2000, roughly the middle. What does `map()` give back? About **127**, the middle of the
brightness range. In at the middle, out at the middle.

**Two things to know about `map()`**

1. **It uses whole numbers and rounds down.** `map()` works with integers and simply drops anything after the point, so 2.9 becomes 2. It never rounds up.
2. **It can stretch and flip.** The difference from a paper map: a paper map can only shrink things. `map()` can also stretch a small range, or even flip one so the top becomes the bottom. Swap the last two numbers (`map(value, 0, 4095, 255, 0)`) and the knob works backwards: turned left the LED is bright, turned right it goes dark.

## 3. Wiring

1. **Unplug the USB cable.**
2. Keep episode 7's circuit: the **red LED on GPIO 23** (with its 220 Ω resistor), and the **potentiometer's middle leg (the wiper) on GPIO 34**, with its **outer legs on 3V3 and GND**. The plus rail must be **3.3 V, never 5 V**.
3. Add the **yellow LED on GPIO 18** and the **green LED on GPIO 17**. Each LED gets **its own 220 Ω resistor**, just like the red one.
4. **Long leg toward the pin, short leg toward the minus rail** (through the resistor). Keep this in mind, because it comes back in section 6.
5. If the board gets crowded, move the knob higher up and its wires simply move with it. If your power rails are split in the middle, keep the bridge wires.

```
GPIO 34 ◄── knob middle leg  (outer legs: 3V3 and GND)
GPIO 23 ──► 220 Ω ──► red LED    (long leg) ─ short leg ──► GND
GPIO 18 ──► 220 Ω ──► yellow LED (long leg) ─ short leg ──► GND
GPIO 17 ──► 220 Ω ──► green LED  (long leg) ─ short leg ──► GND
```

## 4. The dimmer with `map()` — [`code/map_dimmer`](code/map_dimmer/map_dimmer.ino)

It is last episode's dimmer with one change: the dividing line is now a `map()` line.

```c
// ESP32 From Zero - Episode 8: the dimmer with map()
// Potentiometer on GPIO 34, red LED on GPIO 23.
// What it does: the same dimmer as pot_dimmer, but map() does the scaling for us:
// it turns the knob's 0 .. 4095 into the LED's 0 .. 255.

const int POT_PIN = 34;        // the knob
const int LED_PIN = 23;        // the red LED

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(POT_PIN);                  // the knob: 0 .. 4095
  int brightness = map(value, 0, 4095, 0, 255);     // from range 0..4095 to range 0..255
  analogWrite(LED_PIN, brightness);
  Serial.println(brightness);
  delay(20);
}
```

**Line by line**

| Part | What it does |
|---|---|
| `POT_PIN`, `LED_PIN` | The knob on 34, the red LED on 23. |
| `pinMode(LED_PIN, OUTPUT);` | The LED pin is driven by the board, so it is an output. The knob pin needs nothing. |
| `int value = analogRead(POT_PIN);` | The knob, 0 to 4095. |
| `map(value, 0, 4095, 0, 255)` | Turns the knob's range into the LED's range. |
| `analogWrite(LED_PIN, brightness);` | Sends `brightness` to the red LED. |
| `Serial.println(brightness);` | Prints the brightness (try the Serial Plotter). |
| `delay(20);` | A short pause between readings. |

Pause-and-predict: will the LED look any different from last episode's version, the one that divided by 16? No. It looks the same,
smooth from dark to full. The difference is in the code: anyone can read this line and see both ranges.

## 5. A level bar — [`code/level_bar`](code/level_bar/level_bar.ino)

Think of the battery icon on your phone: the more charge, the more bars. Here we turn the knob's number into a small **level**
from 0 up to 3. The level says how many LEDs are on, counting from green. The difference from a phone: your phone hides many tiny
steps behind each bar. Our bar has only four states, from empty to full.

### Why `map(value, 0, 4096, 0, 4)`?

The obvious line would be `map(value, 0, 4095, 0, 3)`. Pause-and-predict: how often would you see all three LEDs on? **Almost never.**
`map()` rounds down, so level 3 only comes at the very last mark of the ruler (a reading of exactly 4095), and the ruler may never
reach that mark.

The fix: **ask for four levels and pretend the ruler is one mark longer.** With `map(value, 0, 4096, 0, 4)` the reading never
gets to 4, so the answer stops at 3, and every level gets an equal slice of the knob (about 1024 readings each):

| Knob reading | `map(value, 0, 4096, 0, 4)` | LEDs on |
|---|---|---|
| 0 to 1023 | 0 | none |
| 1024 to 2047 | 1 | green |
| 2048 to 3071 | 2 | green + yellow |
| 3072 to 4095 | 3 | green + yellow + red |

```c
// ESP32 From Zero - Episode 8: a 3-LED level bar
// Potentiometer on GPIO 34; green LED on GPIO 17, yellow on GPIO 18, red on GPIO 23.
// What it does: like a volume meter. Knob at the left: all off. Turn it right:
// first green lights, then green + yellow, then all three.
// map() turns 0 .. 4095 into a level 0 .. 3; if / else if picks which LEDs are on.

const int POT_PIN = 34;
const int GREEN_PIN = 17;
const int YELLOW_PIN = 18;
const int RED_PIN = 23;

void setup() {
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(POT_PIN);       // 0 .. 4095
  int level = map(value, 0, 4096, 0, 4); // 0, 1, 2 or 3 (4096 and 4: so the right end still gives 3)

  if (level == 0) {                      // nothing
    digitalWrite(GREEN_PIN, LOW);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(RED_PIN, LOW);
  } else if (level == 1) {               // green
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(RED_PIN, LOW);
  } else if (level == 2) {               // green + yellow
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(YELLOW_PIN, HIGH);
    digitalWrite(RED_PIN, LOW);
  } else {                               // all three
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(YELLOW_PIN, HIGH);
    digitalWrite(RED_PIN, HIGH);
  }

  Serial.println(level);
  delay(20);
}
```

**Line by line**

| Part | What it does |
|---|---|
| `GREEN_PIN`, `YELLOW_PIN`, `RED_PIN` | The three LEDs on 17, 18 and 23, all outputs in `setup()`. |
| `int value = analogRead(POT_PIN);` | The knob, 0 to 4095. |
| `int level = map(value, 0, 4096, 0, 4);` | The knob turned into a level: 0, 1, 2 or 3. |
| `if (level == 0)` | Level 0 turns all three LEDs off. |
| `else if (level == 1)` | Level 1 lights only green. |
| `else if (level == 2)` | Level 2 adds yellow. |
| `else` | If it is none of those, it must be 3, so the last `else` lights everything. |
| `Serial.println(level);` | Prints the level, so you can check the code against the LEDs. |

Pause-and-predict: the knob is just past the middle. Which LEDs are on? **Green and yellow**: just past the middle is level 2.
Turn the knob slowly and the bar fills one light at a time, then empties again.

## 6. A mistake you might make: the LED in backwards

Green and red light up, but **yellow stays dark**. Is it the code or the wiring? **Take the temperature first:** the Serial Monitor
says level 3, so the code wants yellow on. The problem is on the wiring side.

The yellow LED is in **backwards**. An LED lets current through only one way, from the long leg to the short leg. Turned around,
it simply stays dark and **nothing breaks and nothing is damaged**. Flip it, and the bar is complete.

## 7. Pause and explain

Say in your own words why the first level line almost never lit all three LEDs. One way to say it: `map()` rounds down, so the
top level only came at the very end of the ruler, and the ruler rarely gets there.

## 8. Your turn: the Rotary Safe Lock — [`code/challenge_safe_lock`](code/challenge_safe_lock/challenge_safe_lock.ino)

Map the knob onto **0 to 99** and print the number, so the knob becomes the dial of a safe.

- The **secret code is three numbers in a row**, and you press the **button** after each one. The numbers are on the screen.
- Get all three right, and the **RGB LED from episode 6** (GPIO 25, 26, 27) turns **green**. One wrong press flashes **red**, and you start again from the first number.
- The twist: a knob is never exact, so **accept a few numbers on either side of each target**. You will need **`&&`**, which means *and*: both checks must be true.
- One hint: a single variable called **`step`** can remember how many numbers are already right.

Extra wiring for the challenge: the **RGB LED on GPIO 25 (red), 26 (green), 27 (blue)** as in episode 6, and the **button on GPIO 22**
(episode 4), read with `INPUT_PULLUP`, so pressed means `LOW`.

Post your safe lock code in the comments; one solution is below. Try it yourself first. In this solution the targets are 25, 70 and
40, each accepting plus or minus 3.

```c
// ESP32 From Zero - Episode 8 challenge (one solution): Rotary Safe Lock
// Potentiometer on GPIO 34, button on GPIO 22, RGB LED on GPIO 25 (red) / 26 (green) / 27 (blue).
// What it does: the knob dials a number 0 .. 99 (printed on the Serial Monitor). Dial 25, press;
// dial 70, press; dial 40, press: the safe opens (RGB green). A wrong number flashes red and starts over.
// Each target accepts +-3 (for example 22 .. 28), because a knob is never exact.

const int POT_PIN = 34;
const int BUTTON_PIN = 22;
const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const bool COMMON_ANODE = false;

int step = 0;                  // how many numbers were right so far: 0, 1, 2 (3 = open)
int lastState = HIGH;          // the button, as in episode 4
unsigned long lastChange = 0;
unsigned long lastPrint = 0;

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
  setColor(0, 0, 40);          // dim blue: locked
}

void loop() {
  unsigned long now = millis();
  int number = map(analogRead(POT_PIN), 0, 4095, 0, 99);

  if (now - lastPrint >= 200) {          // show the dial 5 times a second
    lastPrint = now;
    Serial.println(number);
  }

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {                  // a new press: check the number for this step
      int target = 25;
      if (step == 1) {
        target = 70;
      } else if (step == 2) {
        target = 40;
      }
      if (number >= target - 3 && number <= target + 3) {
        step = step + 1;
        Serial.print("ok, step ");
        Serial.println(step);
        if (step == 3) {
          setColor(0, 255, 0);           // open!
          Serial.println("OPEN");
        }
      } else {
        step = 0;                        // wrong: flash red, start over
        setColor(255, 0, 0);
        delay(400);                      // a short flash is fine here: nothing else to watch
        setColor(0, 0, 40);
        Serial.println("wrong, start again");
      }
    }
  }
}
```

## All sketches

| Sketch | What it does |
|---|---|
| [`map_dimmer`](code/map_dimmer/map_dimmer.ino) | the knob dims the LED, using `map()` |
| [`level_bar`](code/level_bar/level_bar.ino) | a 3-LED bar that fills as you turn the knob |
| [`challenge_safe_lock`](code/challenge_safe_lock/challenge_safe_lock.ino) | one solution to the challenge |

## Something not working?

- A bar LED stays dark while the others work? It is probably in **backwards**: long leg toward the pin, short leg toward the minus rail. Nothing is damaged, flip it.
- Print the level first: it tells you whether the code or the wiring is at fault.
- The bar never reaches all three LEDs? Use `map(value, 0, 4096, 0, 4)`, not `0, 4095, 0, 3`.
- The number is stuck at 0 or at 4095? A loose wire or rail gap at the knob. Check the middle leg to D34 and both outer legs.
- Is the plus rail 3.3 V? Never 5 V on an ESP32 input.
- Nothing printed? Set the Serial Monitor to 115200 baud.
- Rails split in the middle? Add a bridge wire to each rail.

## Next time

Our first mini project: a pedestrian crossing, with car lights, a walk light, a button and today's knob.
