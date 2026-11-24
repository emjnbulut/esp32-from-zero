# Episode 17 — My Phone Switches a Real Fan with an ESP32

> DRAFT (24 Nov 2026). The sketch compiles (esp32 core 3.3.12) but has not been tested on a real board yet.

> **Safety: 5 V USB loads only** (a USB desk fan or USB lamp). Never connect wall-socket (mains) voltage to the relay in this course.

Tap ON on your phone and a real desk fan starts with a satisfying *click*; tap "ON for 10 min" and it switches itself off later.

**You need:** the **2-channel 5 V relay module** from the kit and a USB fan (or USB lamp).

| Part | Pin |
|---|---|
| Relay `IN1` | GPIO 16 (`IN2` → GPIO 17 later) |
| Relay `VCC` / `GND` | VIN (5 V) / GND |
| Fan's USB `+` wire | through relay 1 `COM` → `NO` (normally open) |
| OLED `SDA` / `SCL` | GPIO 21 / GPIO 22 |

## 1. A switch flipped by a tiny magnet

Inside the blue box is a coil. Current through the coil makes a small electromagnet that pulls a metal arm over: *click*, the
contact closes, and the fan's own power flows. The ESP32 pin only drives the coil (through a transistor on the module), so a
weak 3.3 V pin can switch a separate circuit.

## 2. Active-LOW: LOW means ON

This module switches **on when the pin is LOW**. That is why the sketch writes HIGH *before* `pinMode(OUTPUT)` — otherwise the
pin starts LOW for a moment at boot and the relay clicks on by itself.

```cpp
digitalWrite(RELAY1, HIGH);   // off, before...
pinMode(RELAY1, OUTPUT);      // ...the pin starts driving
```

## 3. The phone page again

Same idea as Episode 12: the board opens its own Wi-Fi (`PinByPin-ESP32`), and `192.168.4.1` shows three buttons. The 10-minute
timer is the parking ticket once more: save the moment it should switch off, compare with `millis()`.

## Your turn

Add a second load on relay 2 (GPIO 17), e.g. a USB lamp, with its own ON/OFF buttons.

## Code

- [`code/phone_fan`](code/phone_fan/phone_fan.ino)
