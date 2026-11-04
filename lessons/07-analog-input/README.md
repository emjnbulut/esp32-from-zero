# Episode 7 — ESP32 Potentiometer: Read Any Knob with `analogRead()`

Until now the only thing we have read is a button, and a button has two answers. A knob can answer *how much*.
Today we read a knob with `analogRead()`, dim an LED with it, cut it into three zones, calm the reading by averaging,
learn to debug by printing first, and meet the ESP32 pin rules.

**You need:** the circuit from episode 6 (two breadboards, red LED on GPIO 23), one 10 kΩ potentiometer
(a knob with three legs) and a few jumper wires.

## 1. The knob as a playground slide

Picture a slide. The top is 3.3 V, the bottom is ground, and the knob decides how high up the slide you are sitting.
Inside the knob is a strip of resistor with a contact that slides along it. The outer legs go to 3.3 V and ground, and the
**middle leg** gives the voltage at the contact. This is called a **voltage divider**. The difference from a slide:
nothing slides down by itself; the contact stays exactly where you leave it.

With the knob exactly in the middle, the middle leg is at about 1.65 V (half of 3.3). Every position is its own voltage.

## 2. Wiring the knob

1. **Unplug the USB cable.**
2. Put the knob on the **right breadboard, below the LED**.
3. One **outer leg** to the **plus rail**, the other outer leg to the **minus rail**.
4. A **long wire** takes the **middle leg** across to **D34**.
5. If your power rails are split in the middle, add a bridge wire to each one.

```
3.3 V ──► + rail ──► outer leg ┐
                               ├─ knob ── middle leg ──► long wire ──► GPIO 34
GND   ──► − rail ──► outer leg ┘
```

**The plus rail must be 3.3 V, never 5 V.** An ESP32 input can only take 3.3 V.

## 3. `analogRead()` — [`code/pot_read`](code/pot_read/pot_read.ino)

`analogRead(pin)` measures the voltage on a pin and gives back a number from **0 to 4095**: 0 means 0 V and 4095 means 3.3 V.
Think of a ruler with 4096 marks laid along the slide. The difference from a ruler: this one is not perfect. Near the two ends it
flattens a little, so you may never see exactly 0 or exactly 4095.

```c
// ESP32 From Zero - Episode 7: read the knob
// Potentiometer middle leg on GPIO 34 (outer legs: 3V3 and GND).
// What it does: prints the knob's position (0 .. 4095) ten times a second. Turn the knob and watch the number.

const int POT_PIN = 34;        // the knob's middle leg

void setup() {
  Serial.begin(115200);        // so we can print to the Serial Monitor
}

void loop() {
  int value = analogRead(POT_PIN);  // 0 = knob at one end (0 V), 4095 = other end (3.3 V)
  Serial.println(value);            // show it
  delay(100);                       // ten readings a second
}
```

**Line by line**

| Part | What it does |
|---|---|
| `const int POT_PIN = 34;` | Gives pin 34 a name: the knob's middle leg. |
| `setup()` | Runs once and only starts the Serial Monitor. A pin we only read this way needs **no `pinMode()`**. |
| `analogRead(POT_PIN)` | Measures the voltage on the pin and returns 0 to 4095. It is stored in `value`. |
| `Serial.println(value);` | Prints the number so you can see it. |
| `delay(100);` | Waits a tenth of a second: ten readings per second. |

Open the Serial Monitor at 115200 baud. Pause-and-predict: with the knob in the middle you should see about 2000, half of the scale.
Turn the knob and the number climbs with it, from the bottom of the scale to the top.

## 4. The knob dims the LED — [`code/pot_dimmer`](code/pot_dimmer/pot_dimmer.ino)

`analogWrite()` sets the brightness, but it only takes 0 to 255, and the knob gives up to 4095. We divide:
4095 / 16 is about 255, so both ends of the knob land on both ends of the brightness.

```c
// ESP32 From Zero - Episode 7: the knob dims the LED
// Potentiometer on GPIO 34, red LED on GPIO 23 (episode 3 circuit).
// What it does: turn the knob and the LED gets brighter or dimmer, instantly.
// The knob gives 0 .. 4095, analogWrite wants 0 .. 255, so we divide by 16 (4095 / 16 is about 255).

const int POT_PIN = 34;        // the knob
const int LED_PIN = 23;        // the red LED

void setup() {
  pinMode(LED_PIN, OUTPUT);    // we drive the LED pin
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(POT_PIN);    // the knob: 0 .. 4095
  int brightness = value / 16;        // the same position, scaled to 0 .. 255
  analogWrite(LED_PIN, brightness);   // show it on the LED
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
| `int brightness = value / 16;` | The same position scaled to 0 to 255. |
| `analogWrite(LED_PIN, brightness);` | Shows it on the LED. |
| `Serial.println(brightness);` | Prints the brightness (try the Serial Plotter). |
| `delay(20);` | A short pause between readings. |

Pause-and-predict: what if we divided by 32 instead? The biggest number would be about 127, so the LED would stay at about
half power, however far you turn the knob.

Why do we divide by 16? The knob's scale is 16 times bigger than the brightness scale, so dividing makes them match.

## 5. Three zones — [`code/pot_zones`](code/pot_zones/pot_zones.ino)

Sometimes you do not want every value, only a few choices, like the low, medium and high marks on a stove. The knob still
gives one number, and our code sorts it. 4095 / 3 is about 1365, so we cut at 1365 and 2730. The difference from a stove:
this knob has no clicks. The zones exist only in the code.

```c
// ESP32 From Zero - Episode 7: three zones
// Potentiometer on GPIO 34, red LED on GPIO 23.
// What it does: the knob has three zones. Left third: the LED is dim. Middle third: medium. Right third: full.
// The numbers 1365 and 2730 cut 0 .. 4095 into three equal parts.

const int POT_PIN = 34;        // the knob
const int LED_PIN = 23;        // the red LED

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(POT_PIN);     // the knob: 0 .. 4095

  if (value < 1365) {                  // left third
    analogWrite(LED_PIN, 20);          // dim
  } else if (value < 2730) {           // middle third
    analogWrite(LED_PIN, 120);         // medium
  } else {                             // right third
    analogWrite(LED_PIN, 255);         // full
  }

  Serial.println(value);
  delay(20);
}
```

**Line by line**

| Part | What it does |
|---|---|
| `int value = analogRead(POT_PIN);` | The knob, 0 to 4095. |
| `if (value < 1365)` | Left third: the LED gets 20, which is dim. |
| `else if (value < 2730)` | Only checked if the first test was false: the middle third, the LED gets 120. |
| `else` | Everything else, the right third: full brightness, 255. |
| `Serial.println(value);` | Prints the reading, so you can see where the cuts are. |

Pause-and-predict: the reading is exactly 1365. Which zone? The middle one: `<` means strictly less, so 1365 fails the first test and passes the second.
Turn the knob slowly and you get dim, medium and full in three clear steps.

## 6. A calmer reading — [`code/pot_smooth`](code/pot_smooth/pot_smooth.ino)

Leave the knob alone and watch the number: it still wobbles a little, like a bathroom scale that never quite settles.
Tiny electrical noise changes every reading. The fix is what you would do on that scale: measure four times and take the
average. The difference from a scale: four readings take the board well under a millisecond, so you lose no time.

```c
// ESP32 From Zero - Episode 7: a calmer reading (average of 4)
// Potentiometer on GPIO 34.
// What it does: prints two numbers: "raw" (one reading) and "avg" (the average of 4 readings).
// Open the Serial Plotter: the raw line jitters a little even when you do not touch the knob, the avg line is calmer.

const int POT_PIN = 34;        // the knob

void setup() {
  Serial.begin(115200);
}

void loop() {
  int raw = analogRead(POT_PIN);       // one reading: it jitters a little

  int sum = 0;                         // add up 4 readings...
  for (int i = 0; i < 4; i++) {
    sum = sum + analogRead(POT_PIN);
  }
  int avg = sum / 4;                   // ...and divide by 4: the average

  Serial.print("raw:");
  Serial.print(raw);
  Serial.print(",avg:");
  Serial.println(avg);
  delay(50);
}
```

**Line by line**

| Part | What it does |
|---|---|
| `int raw = analogRead(POT_PIN);` | One single reading, which jitters a little. |
| `int sum = 0;` | The running total starts at 0. |
| `for (int i = 0; i < 4; i++)` | A loop that runs four times (`i` is 0, 1, 2, 3). |
| `sum = sum + analogRead(POT_PIN);` | Adds a fresh reading each round. |
| `int avg = sum / 4;` | The total divided by 4 is the average. |
| `Serial.print("raw:") ... "avg:"` | Prints `raw:<number>,avg:<number>`, the format the Serial Plotter draws as two lines. |
| `delay(50);` | A short pause between rounds. |

Open **Tools → Serial Plotter**: the single reading jitters, and the average is calmer.

## 7. When it does not work: print first

Say the LED does not react to the knob at all. Is it the LED, the knob or the code? **Print the value, before you trust anything.**
A doctor takes your temperature before choosing a medicine, and the print line is your thermometer.

- The number tells you which half is broken. **Stuck at 0 or stuck at the top** means a **loose wire or a rail gap at the knob**
  (check the middle-leg wire to D34, the two outer legs and the bridge wires).
- If the number moves normally, the knob is fine, so look at the **LED side** (pin, resistor, wiring).

The difference from a thermometer: printing takes time, so too many prints can slow a fast loop. Remove them when you are done.

## 8. Pin rules

Not all pins are equal. See the full table in [`PINMAP.md`](../../PINMAP.md); you do not need to memorize it.

1. **Pins 34–39 are input only**, like one-way doors: they can only listen, so they cannot drive an LED. That is why the knob sits on 34.
2. **ADC2 pins, including 25–27, cannot use `analogRead()` while Wi-Fi is on.** Pin 34 keeps working, so our sensors live there.
3. **Boot pins 0, 2, 5, 12 and 15** are checked at power-on, so we leave them free.

## 9. Your turn: Knob Blink Speed — [`code/challenge_knob_blink`](code/challenge_knob_blink/challenge_knob_blink.ino)

The LED **blinks all the time**, and the knob picks the speed in **three zones**: every **100 milliseconds**,
every **400**, and every **second** (1000 ms). The twist: **nothing may wait with `delay()`**. Today's zones choose the interval,
and the `millis()` trick from episode 4 does the blinking.

Post your code in the comments; one solution is in the
[`challenge_knob_blink`](code/challenge_knob_blink/challenge_knob_blink.ino) file. Try it yourself first.

## All sketches

| Sketch | What it does |
|---|---|
| [`pot_read`](code/pot_read/pot_read.ino) | prints the knob's position, 0 to 4095 |
| [`pot_dimmer`](code/pot_dimmer/pot_dimmer.ino) | the knob dims the LED (divide by 16) |
| [`pot_zones`](code/pot_zones/pot_zones.ino) | dim, medium and full in three zones |
| [`pot_smooth`](code/pot_smooth/pot_smooth.ino) | raw reading vs average of four |
| [`challenge_knob_blink`](code/challenge_knob_blink/challenge_knob_blink.ino) | one solution to the challenge |

## Something not working?

- The number is stuck at 0 or at 4095? A loose wire or rail gap at the knob. Check the middle leg to D34 and both outer legs.
- Nothing printed? Set the Serial Monitor to 115200 baud.
- Is the plus rail 3.3 V? Never 5 V on an ESP32 input.
- The number moves but the LED does not? The knob is fine: check the LED's pin (23), resistor and ground wire.
- Rails split in the middle? Add a bridge wire to each rail.
