# Episode 14 — I Turned Bananas into a Piano

> DRAFT (24 Nov 2026). The sketch compiles (esp32 core 3.3.12) but has not been tested on a real board yet.

Three fruits become piano keys: touch the banana and the buzzer plays DO, the apple MI, the orange SOL. Hold the button to
record eight notes, press it once to play your tune back.

**You need:** three pieces of fruit (or aluminium foil), three jumper wires. Everything else is the Episode 10 circuit.

| Part | Pin |
|---|---|
| Touch pad 1 (banana) | GPIO 14 (touch T6) |
| Touch pad 2 (apple) | GPIO 2 (touch T2) — also the board's blue LED, it may glow a little |
| Touch pad 3 (orange) | GPIO 15 (touch T3) |
| Passive buzzer `+` | GPIO 32 |
| Button | GPIO 19 ↔ GND |
| OLED `SDA` / `SCL` | GPIO 21 / GPIO 22 |

Stick a wire end into each fruit. Nothing else goes on the touch pins: no resistor, no ground.

## 1. Your body is a tiny capacitor

`touchRead(14)` returns a number (often 40–80 with a wire, it depends on the wire and the fruit). When your finger touches
the fruit, your body adds a little capacitance and **the number drops**. The sketch learns each pad's calm number at start-up
(don't touch anything for the first half second) and calls a key "touched" when the number falls 20 below that.
If a key fires on its own or never fires, change `DROP`.

## 2. A list of notes = an array

```cpp
const int KEY_PIN[3] = {14, 2, 15};
const int NOTE[3]    = {523, 659, 784};   // DO, MI, SOL
int song[8];                              // 8 boxes in a row for the recording
```

The same index belongs to the same key in every list: `KEY_PIN[1]` is pad 2, and it plays `NOTE[1]`.

## 3. Record and play back

- Hold the button **1 second** → recording: each touch goes into the next box of `song`, the screen counts `3/8`.
- Short press → the buzzer plays the boxes in order.

## Your turn

Add a fourth key on GPIO 4 (touch T0) that plays a high DO (1047 Hz). Three lists get one more value each.

## Code

- [`code/fruit_piano`](code/fruit_piano/fruit_piano.ino)
