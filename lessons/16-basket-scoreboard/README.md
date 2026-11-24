# Episode 16 — I Built a Basketball Scoreboard That Counts Every Shot

> DRAFT (24 Nov 2026). The sketch compiles (esp32 core 3.3.12) but has not been tested on a real board yet.

A paper cup is the hoop, an IR sensor hides under the rim, and every ball that drops through scores a point. Press the button:
30 seconds on the clock, a swish beep for every basket, a horn at the end, and your best score survives unplugging.

**You need:** the **IR obstacle sensor** from the kit (3 pins: OUT, GND, VCC), a paper cup and a small ball (paper ball works).

| Part | Pin |
|---|---|
| IR sensor `OUT` | GPIO 13 (LOW when something is in front of it) |
| IR sensor `VCC` / `GND` | 3V3 / GND |
| Passive buzzer `+` | GPIO 32 |
| Button | GPIO 19 ↔ GND |
| OLED `SDA` / `SCL` | GPIO 21 / GPIO 22 |

Tape the sensor under the cup's open bottom, looking across the hole. Turn its little trim pot until its LED lights only
when the ball passes.

## 1. Checking the door vs a doorbell

A ball falls through the beam in a few milliseconds. If `loop()` happens to be busy redrawing the screen at that moment, a
simple `digitalRead()` looks away and misses it. So the pin gets a **doorbell**: an *interrupt*. The moment the beam is
blocked, the chip stops what it is doing, runs our tiny function, and carries on.

```cpp
attachInterrupt(digitalPinToInterrupt(IR_PIN), ballSeen, FALLING);   // ring when OUT goes HIGH -> LOW

void IRAM_ATTR ballSeen() {   // IRAM_ATTR: "just put this word here" - ESP32 interrupt functions need it
  baskets++;
}
```

Two rules: keep the interrupt function **tiny** (count, note the time, done — no screen, no `delay()`), and mark the shared
variable `volatile`, because it can change behind `loop()`'s back.

## 2. One ball, one point

A ball can flicker the sensor a few times on the way through. The function only counts when 300 ms have passed since the
last count — the same idea as the button debounce in Episode 4.

## Your turn

Add a **3-point zone**: hold the button while shooting and that basket counts 3. (Hint: read the button inside `loop()`, not in
the interrupt — compare `baskets` with the last value you saw.)

## Code

- [`code/basket_scoreboard`](code/basket_scoreboard/basket_scoreboard.ino)
