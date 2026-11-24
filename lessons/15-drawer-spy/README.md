# Episode 15 — My Drawer Screams When Someone Opens It

> DRAFT (24 Nov 2026). The sketch compiles (esp32 core 3.3.12) but has not been tested on a real board yet.

A light sensor hides in a dark drawer. Someone opens it, light floods in, and the buzzer screams. Later the screen tells you:
"opened 3x" — even if the power went out in between.

**You need:** the **LDR light-sensor module** from the kit (4 pins: AO, DO, GND, VCC). Everything else is the Episode 10 circuit.

| Part | Pin |
|---|---|
| LDR module `AO` | GPIO 35 (input-only, analog) |
| LDR module `VCC` / `GND` | 3V3 / GND (`DO` stays unconnected) |
| Passive buzzer `+` | GPIO 32 |
| Button (hold 2 s = reset the counter) | GPIO 19 ↔ GND |
| OLED `SDA` / `SCL` | GPIO 21 / GPIO 22 |

## 1. Light becomes a number

`analogRead(35)` gives 0–4095. Many LDR modules give a **higher** number in the **dark**: open the Serial Monitor, cover the
sensor with your hand and watch. If the number drops in the dark instead, set `DARK_IS_HIGH = false`. The sketch turns either
kind into `light`: 0 = dark, 4095 = bright.

## 2. Two thresholds, not one

With one threshold, a drawer opened just a crack hovers around it and the alarm flickers on, off, on. So we use two lines:
**open** above 1800, **closed again** only below 1200. Between the lines nothing changes. (That gap is called *hysteresis*;
a thermostat does the same so the heater doesn't click on and off every second.)

Find your own numbers: read `light` with the drawer shut and open (the sketch prints it twice a second), then put `OPEN_AT`
a bit below the open value and `CLOSED_AT` a bit above the shut value.

## 3. A counter that survives a power cut

Like the record in Episode 10, the number of openings lives in the Preferences drawer: read once in `setup()`, written only
when the drawer opens.

## Your turn

Make the screen also show **how long** the drawer was open last time (hint: save `now` when it opens, subtract when it closes —
the parking ticket again).

## Code

- [`code/drawer_spy`](code/drawer_spy/drawer_spy.ino)
