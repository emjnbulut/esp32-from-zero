# Episode 11 — I Built a Motion Alarm That Catches Anyone Sneaking In

> DRAFT (24 Nov 2026). The sketches compile (esp32 core 3.3.12) but have not been tested on a real board yet.

A white dome on the breadboard guards your desk. Press the button, walk out within ten seconds, and from then on anything warm
that moves sets off a siren. When you come back, the screen tells you how many times someone was caught, and how long ago.

**You need:** one new part, the **HC-SR501 PIR motion sensor** from the starter kit. Everything else is the Episode 10 circuit.

| Part | Pin |
|---|---|
| PIR sensor `OUT` (middle leg) | GPIO 33 |
| PIR sensor `VCC` | VIN (5 V from USB) |
| PIR sensor `GND` | GND |
| OLED `SDA` / `SCL` | GPIO 21 / GPIO 22 |
| Button | GPIO 19 ↔ GND |
| Passive buzzer `+` | GPIO 32 |

```
VIN ─────────► PIR VCC        (the sensor wants 5 V for its own electronics)
GND ─────────► PIR GND
GPIO 33 ◄──── PIR OUT         (answers with 3.3 V: safe for the ESP32)
GPIO 21/22 ── OLED SDA/SCL    (from Episode 10)
GPIO 19 ◄──── button ── GND   (INPUT_PULLUP: pressed = LOW)
GPIO 32 ────► passive buzzer + ── - ──► GND
```

The PIR is the only part on 5 V. Its **output** is 3.3 V, so it can go straight into GPIO 33. The OLED still runs on **3.3 V**.

## 1. Thumbs up or thumbs down

Everything warm glows in infrared: your hand, a cat, a cup of tea. We can't see that glow; the PIR can. Its white dome is a lens made
of many small windows, each one looking at its own slice of the room, like a row of flashlights. When something warm moves from one
window to the next, the sensor notices the change and turns its `OUT` pin on.

So for our code the whole sensor is one line:

```cpp
bool motion = digitalRead(PIR_PIN) == HIGH;   // something moved: true
```

**The two orange knobs** on the side: one sets how long `OUT` stays on after a movement (time), the other how far the sensor sees
(sensitivity). For this project turn **time all the way down** (about 3 s); the code decides how long the siren plays.

**Warm-up:** after power-on the sensor needs about **30 seconds** before it can be trusted. The sketch ignores it during that time.

## 2. The alarm's steps (the washing machine again)

| `state` | Step | Moves on when |
|---|---|---|
| 0 | warming up | 30 s after power-on |
| 1 | off: shows "seen 2x, last: 3 min ago" | button → 2 |
| 2 | leaving: 10 s countdown, a tick every second | 10 s → 3 (button cancels → 1) |
| 3 | armed: waits for the PIR | motion → 4 (button → 1) |
| 4 | alarm: two-tone siren | button or 15 s → 1 |

The siren is one `tone()` whose note switches every quarter second:

```cpp
tone(BUZZER_PIN, (inState / 250) % 2 ? 2600 : 1800);
```

## 3. Remembering *when* (the parking ticket again)

At the moment of motion we stamp the time, like the parking ticket from Episode 9 (`pressStart`):

```cpp
lastMotion = now;            // now = millis(), the board's stopwatch since power-on
```

Later, `now - lastMotion` is how long ago it happened, in milliseconds. The helper `ago()` turns that into words: under a minute
→ seconds, under an hour → minutes (`/ 60000`), else hours.

## 4. Active or passive buzzer?

Your kit has two buzzers that look almost the same. Ours is **passive**: a tiny speaker that plays whatever note `tone()` sends, so it
can make a siren. The **active** one has its own beeper inside, like a music box with one tune: give it power and it beeps, always the same note.
Easier, but no siren. (Tell them apart: the passive one usually shows a green circuit board underneath; the active one is sealed and
often has a sticker on top.)

## 5. Common problem: it goes off the moment you arm it

- The sensor is still **warming up**: wait 30 s after plugging in (the sketch already does).
- The **time knob** is turned up, so `OUT` stays on for a long time after *your own* movement. Turn it all the way down.
- The sensor sees **you leaving**: point the dome away from the door, or turn sensitivity down.

## 6. Your turn

Keep the number of catches even after unplugging, with `Preferences`, like the record in Episode 10.
Solution: [`code/challenge_saved_count`](code/challenge_saved_count/challenge_saved_count.ino) (read the count in `setup()`, write it
only when it changes). Why isn't `lastMotion` saved too? Because `millis()` starts at 0 again after power-on: an old time would
mean nothing.

## Code

- [`code/motion_alarm`](code/motion_alarm/motion_alarm.ino) — the episode's sketch
- [`code/challenge_saved_count`](code/challenge_saved_count/challenge_saved_count.ino) — challenge solution

Libraries (Library Manager): **Adafruit SSD1306** and **Adafruit GFX** (already installed in Episode 10).
