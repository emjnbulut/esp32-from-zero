# Episode 4 — Buttons and Doing Two Things at Once

Last time our code switched an LED on and off. Today the ESP32 **listens**: we read a push button with
`digitalRead`, and then teach the board to do **two things at once** with `millis()`.

**You need:** the board, **two breadboards**, a push button, a red and a green LED, two 220 Ω resistors and a few
jumper wires (yellow, black, green).

## 1. How the push button works

The button has four legs, but inside it is just a simple switch.

- The two legs on the **left** are always connected to each other, and so are the two on the **right**.
- When you **press** the button, a small metal plate connects the left side to the right side.
- Let go, and the two sides are apart again.

## 2. Two breadboards and the wiring

On a single breadboard a 30-pin board leaves free holes on **one side only**. From this episode on we use **two
breadboards, one above the other**: the board's top pins go into the upper breadboard's row `j`, its bottom pins
into the lower breadboard's row `a`. Now every pin has free holes next to it.

1. **Unplug the USB cable** first.
2. Rebuild the circuit from episode 3 on the **lower** breadboard: `D23` → 220 Ω resistor → red LED, and two black
   wires to the lower minus rail (one from the LED's short leg, one from a `GND` pin).
3. Press the button into the lower breadboard **across the middle gap**, at columns **25–27**.
4. **Yellow wire:** `D22` → column 25 (the button's left side).
5. **Black wire:** column 27 (the button's right side) → the **minus rail** (ground).

```
GPIO 22 ──► button (left side) … press … (right side) ──► − rail ──► GND
```

Pressed, GPIO 22 is connected straight to ground. That is all the wiring the button needs.

## 3. Floating pins and pull-ups

Pressed, the pin is at 0 V. But **not pressed**, the pin is connected to nothing. A pin connected to nothing is
**floating**: it picks up noise from the air, even from your hand, and reads random HIGHs and LOWs.

The fix is a resistor that gently pulls the pin to a known level.

- **Pull-up resistor:** pulls the pin up to 3.3 V. Not pressed = **HIGH**. Pressed, the button wins (it connects
  the pin straight to ground) = **LOW**.
- **Pull-down resistor:** the opposite. A **10 kΩ** resistor from the pin to ground, and the button wired to 3.3 V.
  Pressed = HIGH.

Both work. The ESP32 has pull-up resistors **built in** (about **45 kΩ**: weak enough that the button easily wins,
strong enough to hold the pin steady), so we need no extra part. We switch one on in code with `INPUT_PULLUP`.

| Mode | Not pressed | Pressed |
|---|---|---|
| `INPUT_PULLUP` | `HIGH` (1) | `LOW` (0) |

## 4. The code — [`code/button_led/button_led.ino`](code/button_led/button_led.ino)

```c
const int BUTTON_PIN = 22;     // the button pulls this pin to GND
const int LED_PIN = 23;        // our LED from episode 3

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP); // HIGH until pressed
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int state = digitalRead(BUTTON_PIN); // HIGH or LOW
  Serial.println(state);

  if (state == LOW) {          // pressed: pulled to GND
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(50);
}
```

| Call | What it does |
|---|---|
| `pinMode(pin, INPUT_PULLUP)` | read this pin, with the built-in pull-up switched on |
| `digitalRead(pin)` | returns `HIGH` or `LOW` |

Upload it, open the **Serial Monitor** at **115200** baud. Not pressed it prints `1` (HIGH). Press the button:
it prints `0` and the LED lights. Let go, and it goes dark.

**See a floating pin yourself:** change `INPUT_PULLUP` to plain `INPUT` and upload again. Touch the yellow wire
or move your hand near it and the numbers jump around. Change it back and it is calm again.

## 5. Toggle, edges and bounce — [`code/button_toggle/button_toggle.ino`](code/button_toggle/button_toggle.ino)

Instead of holding the button: press once for on, once more for off.

- We remember the last state. When the state **changes** and is now `LOW`, that is a new press.
- On a timeline `HIGH, HIGH, HIGH, LOW`, the single moment HIGH turns into LOW is the press. It is called an **edge**.
- Quick question: hold the button down. Does the LED keep flipping? No: `state` and `lastState` both stay `LOW`,
  nothing changes, so there is no new edge.
- On a press we flip a `bool ledOn` (`true` or `false`), first the long, easy-to-read way:

```cpp
if (ledOn) {
  ledOn = false;
  digitalWrite(LED_PIN, LOW);
} else {
  ledOn = true;
  digitalWrite(LED_PIN, HIGH);
}
```

- The short way, same result in two lines (this is what the sketch uses):
  - `ledOn = !ledOn;` — the `!` means *not*, so it swaps the value.
  - `digitalWrite(LED_PIN, ledOn ? HIGH : LOW);` — the `?:` picks `HIGH` when `ledOn` is true, otherwise `LOW`.

**Bounce:** count the presses and sometimes one press counts twice or three times. When metal contacts touch they
bounce for a few milliseconds, and the ESP32 checks the pin hundreds of thousands of times a second, so one press
can look like five. The simple fix is **debouncing**: after every change, pressed or released, wait **50 ms**
until the bouncing is over. Now every press counts exactly once.

## 6. Why `delay()` gets in the way

Part two: blink the LED like last episode, and let the button switch the blinking on and off.

The obvious way is to blink with `delay()` and read the button in the same loop. But `delay()` **freezes
everything**: while it waits, the ESP32 does not look at the button at all. A press during the delay is simply
missed. Shorter delays make the blinking messy and presses still slip through.

## 7. `millis()`: check the clock — [`code/blink_button/blink_button.ino`](code/blink_button/blink_button.ino)

The fix: **never wait**, look at the clock instead. `millis()` returns the milliseconds since the board started.
It counts by itself, 1000 more every second, while your code does other things.

For each thing that happens "every so often" we remember when it last happened. Every time round the loop we ask:
*have 500 ms passed since then?* If yes, do it and note the time. If not, move on.

Example: the LED last changed at 700. Now it is 1000: 1000 − 700 = 300, not yet. Later now is 1200:
1200 − 700 = 500, flip the LED, and the last time becomes 1200.

```c
void loop() {
  unsigned long now = millis(); // milliseconds since the board started

  // 1. the button: a new press switches blinking on or off
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) { // ignore the bounce
    lastChange = now;
    lastState = state;
    if (state == LOW) {
      blinking = !blinking;
      Serial.println(blinking ? "blinking" : "stopped");
    }
  }

  // 2. the LED: flip it every 500 ms, without waiting
  if (blinking && now - lastBlink >= 500) {
    lastBlink = now;
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
  }
  if (!blinking && ledOn) {    // stopped: make sure the LED is off
    ledOn = false;
    digitalWrite(LED_PIN, LOW);
  }
}
```

(The variables `blinking`, `ledOn`, `lastBlink`, `lastState`, `lastChange` are declared above `setup()`; see the
full file.)

- Times live in an **`unsigned long`**: a big whole number that cannot go negative.
- We **always subtract**: `now - last`. After about **49.7 days** `millis()` rolls over to 0. With subtraction the
  math still works out; with other tricks it does not.
- The button uses the same trick: instead of a `delay()` for debouncing, we ignore changes less than 50 ms after the
  last one.

Now the loop never waits. It runs thousands of times a second and every time checks the button and the clock.
Upload it: the LED blinks, a press stops it at once, another press starts it again. Two things at once.

## 8. A second LED — [`code/two_leds/two_leds.ino`](code/two_leds/two_leds.ino)

This scales. Add a green LED that blinks at its own speed. **Unplug the USB cable.** This time we use the **upper
breadboard**:

1. **Green wire:** `D25` → column 18.
2. **220 Ω resistor:** column 18 → column 21.
3. **Green LED:** long leg in column 21, short leg in column 22.
4. **Black wire:** column 22 → the upper breadboard's **minus rail**.
5. **Black wire:** the top `GND` pin (column 3) → that minus rail.

```
GPIO 25 ──► 220 Ω ──► green LED (long leg … short leg) ──► top − rail ──► GND
```

In the code each LED gets its own timer: red flips every **500 ms**, green every **150 ms**. Upload: both blink at
their own pace while the button (it switches the red one on and off) still reacts instantly.

Quick question: change green to 300 ms. Does red change too? No: each `if` checks only its own timer.

## 9. Challenge — [`code/challenge_speed/challenge_speed.ino`](code/challenge_speed/challenge_speed.ino)

**The speed-shifter.** Red keeps blinking every 500 ms. Make each button press switch the **green LED** between fast
(150 ms) and slow (600 ms), without disturbing red. You only need what this episode used: a variable for the green
interval, the edge of a press and an `if`. Post your solution in the comments; one solution is in the folder and in
a Short — try it yourself first.

## All five sketches

| Sketch | What it does |
|---|---|
| [`button_led`](code/button_led/button_led.ino) | LED on while the button is held |
| [`button_toggle`](code/button_toggle/button_toggle.ino) | each press flips the LED, with debounce |
| [`blink_button`](code/blink_button/blink_button.ino) | blinking with `millis()`, the button starts/stops it |
| [`two_leds`](code/two_leds/two_leds.ino) | red and green at their own speeds + button |
| [`challenge_speed`](code/challenge_speed/challenge_speed.ino) | one solution to the challenge |

## Not working?

- Is the button really across the **middle gap**, at columns 25–27?
- Is the yellow wire in the **D22** column (and the code says `22`)?
- Always reads `0`? The button is probably turned **sideways** (the always-connected legs sit in the same row pair).
- Numbers jump around? You probably used `INPUT` instead of `INPUT_PULLUP`.
- Green LED stays dark? Check the black wire from the upper minus rail to `GND`, and that the long leg is in column 21.
- Count jumps by two on one press? Add the 50 ms debounce.

**Next episode:** dimming with PWM, RGB colors, and a potentiometer knob.
