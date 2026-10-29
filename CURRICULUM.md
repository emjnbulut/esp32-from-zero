# Curriculum (v5, 28 October 2026)

Target viewer: knows basic C (variables, `if/else`, loops, functions), has never used a microcontroller.
Language: C-style code on the Arduino framework (Arduino IDE 2.x + Espressif ESP32 core).
Format (from Ep 05): every episode is **two parts of 6–9 minutes** (10 min hard limit), one new topic per part plus practice; Ep 01–04 are single videos. A numberless **Recap** follows every few episodes (after 04, 07, 11 and 14). Step-by-step practice with 2–4 sketches per part, English narration, 4 dubs (TR, HI, PT, ES) and 12 subtitle languages. Lesson rules: `video/PRODUCTION_GUIDELINES.md` sections 8 and 10; analogies: `video/ANALOGIES.md`; pins: [`PINMAP.md`](PINMAP.md); release dates: `video/YAYIN_TAKVIMI.md`.

Kit: direnc.net "ESP-32S WiFi Başlangıç Seti" — ESP32 dev board (30-pin), 2× 830-point breadboards (clipped side by side so both rows of pins have free holes), digital multimeter, 0.96" OLED,
DHT11, HC-SR501 PIR, obstacle sensor module, LDR module, 10k potentiometer, active + passive buzzer,
2-channel 5V relay, 6 push buttons, red, yellow and green LEDs (4 of each in the creator's kit), 2 RGB LEDs, 220Ω / 1kΩ / 10kΩ resistors,
jumper wires (M-M, F-M, F-F), micro USB cable.

---

## Learning Format & The "Zero Unlearned Syntax" Rule

1. **"Zero Unlearned Syntax" Rule (Sıfır Yabancı Kod Kuralı):**
   A viewer challenge or milestone project **never** requires a C syntax feature, library function, or hardware trick that was not explicitly taught in that episode or an earlier episode.
   * No surprise functions (e.g., no `random()`, no C++ `String` manipulation, no pointer arithmetic, no JavaScript `fetch()` in web episodes).
   * The difficulty comes **100% from algorithmic thinking**—combining `if/else`, state variables (`int step`, `int mode`), `millis()` subtraction, and the exact functions taught in the lesson.
2. **"Naive Way First → Clean Way Second" in Lessons:**
   Every concept starts with the intuitive approach a beginner would try first (e.g., `delay()` with a button, single-threshold LDR, polling a fast sensor), shows why it breaks on real hardware, and then teaches the clean engineering tool (`millis()`, debouncing, hysteresis, state machines, interrupts).
3. **Hands-Free Multimeter Clips (Only 5 Key Episodes, 1 Short Clip Each):**
   Real-camera multimeter shots (**1 single 5–8 s clip per episode, probes fixed hands-free**) are used **only in Episodes 05, 06, 08, 12 and 14**, where the meter provides an instant visual "aha!" moment. All other episodes have **0 multimeter camera clips**.
4. **Algorithmic Challenges:**
   Every episode ends (in Part 2) with a logic puzzle that uses the exact circuit and functions from the lesson. The solution is in the lesson folder; a **solution Short** is made only for Ep 04 and the projects (07, 13, 17). In other episodes the script says "write your answer in the comments, the solution is in the lesson folder", never "I'll show it in a Short".
5. **Debugging is taught, not assumed (new in v5):**
   From Ep 06 every episode shows one real mistake and the three checks that find it: *is it the circuit or the code?* → print the value with `Serial`, test the LED alone, measure with the multimeter.
6. **Schematics next to breadboards (new in v5):**
   From Ep 06 each new circuit is shown twice: the breadboard picture and a small schematic with standard symbols (resistor, LED, button, potentiometer, ground), so viewers learn to read both.
7. **One pin plan for the whole season (new in v5):**
   Every part keeps its pin from the first episode it appears in ([`PINMAP.md`](PINMAP.md)), so circuits grow instead of being rebuilt. Pin rules (input-only 34–39, ADC2 off during Wi-Fi, boot pins) are taught in Ep 06·1.

---

## Season 1 — Starter Kit (17 Episodes)

### Stage 1: Digital I/O, Timing & Analog Foundations (Episodes 01–07)

| # | Episode | Exact Syntax & Functions Taught in Lesson | Multimeter Clip (Phone Camera) | Creative Coding Challenge (Uses *Only* Taught Syntax) | Parts |
|---|---------|-------------------------------------------|--------------------------------|-------------------------------------------------------|-------|
| 01 | **Setting Up Your Computer** | `setup()`, `loop()`, `Serial.begin(115200)`, `Serial.println()`, `delay()`, `int` counter variable | — | **Launch Countdown:** Using `int count = 10;`, `if/else` and `delay(1000)`, count down from 10 to 0, print `"WARNING"` on the last 3 seconds, and stop printing after `"LIFTOFF!"` | Board, USB cable |
| 02 | **Meet the Board and the Breadboard** | Hardware only: 30-pin layout on 2 side-by-side breadboards, `3V3`/`5V`/`GND`, breadboard strips, `3V3` → 220Ω → LED → `GND` | — | **Circuit Detective:** 3 broken breadboard circuits are shown (unconnected rail, middle gap, shorted LED legs)—diagnose why each stays dark and fix it by moving 1 wire | Board, breadboard, LED, 220Ω |
| 03 | **Your First Circuit: Blink an LED** | `const int`, `pinMode(pin, OUTPUT)`, `digitalWrite(pin, HIGH/LOW)`, custom helper function `void blinkOnce(int ms)` | — | **Emergency Double-Strobe:** Wire a second (green) LED and write a helper function to make a police double-flash pattern (Red-Red pause, Green-Green pause) | Red & green LEDs, 2× 220Ω |
| 04 | **Buttons and Doing Two Things at Once** | `pinMode(pin, INPUT_PULLUP)`, `digitalRead()`, `bool`, `!`, ternary `?:`, `unsigned long`, `millis()`, edge detection + 50 ms debounce (`now - last >= 50`) | — | **Speed-Shifter (`challenge_speed`):** Red blinks every `500 ms` while Green blinks at `greenInterval`; make each button press swap `greenInterval` between `150 ms` and `600 ms` without disturbing Red | Button, red & green LEDs, 2× 220Ω |
| R1 | **Recap: How to Read a Sketch (Ep 01–04)** | No new syntax: live trace of 5 sketches (code line highlight + memory panel), practice quiz | — | Quiz inside the video | — |
| 05·1 | **PWM: Make an LED Breathe** | `analogWrite(pin, 0..255)`, duty cycle, naive fade with `delay()` (button stops working) → fade with `millis()` | **1 Clip (6 s, hands-free):** Code steps PWM 25% → 50% → 100% while meter shows `0.8V → 1.65V → 3.3V` | (practice task: change the fade step and predict the speed) | Red LED, button, multimeter |
| 05·2 | **RGB Color Mixing** | RGB LED wiring (`GPIO 25/26/27`), helper `void setColor(int r, int g, int b)`, `int mode` cycling with the button | — | **Smart Camping Headlamp:** 1 button cycles `mode` (`0`: Off, `1`: Dim White, `2`: Bright White, `3`: Red Blink). **The logic puzzle:** Using `now - lastPress >= 3000`, if the lamp stays in *any* ON mode for over 3 seconds, the next button press must set `mode = 0` (directly OFF) instead of advancing | RGB LED, button, 3× 220Ω |
| 06·1 | **Analog Input, Pin Rules and Debugging with Serial** | Voltage divider (the potentiometer), `analogRead(34)` (`0–4095`), averaging 4 reads, knob → LED brightness (`value / 16`), knob zones with `if / else if`; **pin rules** (34–39 input only, ADC2 pins stop working with Wi-Fi, boot pins 0/2/5/12/15); **debugging**: print the value before trusting it; first schematic | **1 Clip (6 s, one hand):** Turn the knob while the meter next to the breadboard sweeps `0.0V → 3.3V` | (practice task: **Knob Blink Speed** — three zones pick the blink interval, `challenge_knob_blink`) | Potentiometer, red LED, 220Ω, multimeter |
| 06·2 | **map(), Dimmer Knobs and Level Bars** | `map(val, 0, 4095, min, max)`, smooth dimmer knob, 3-LED level bar (`if/else if`) | — | **Rotary Safe Lock:** Map the knob to `0–99` and print it. Using `int step = 0;`, unlock the safe (RGB Green) only if the user dials **3 target numbers in order** (`25` → press button → `70` → press → `40` → press, checked with `val >= 22 && val <= 28`). Any wrong press flashes Red and resets `step = 0` | Potentiometer, RGB LED, R/Y/G LEDs, button, 220Ω |
| 07·1 | **🏆 Mini-Project 1: Smart Pedestrian Crossing** | Combine 3 car LEDs + RGB walk light + button + potentiometer with a `millis()` state variable (`int state = 0, 1, 2, 3`); measuring **how long a button was held** (`now - pressStart`) | — | (project part; the challenge is in 07·2) | R/Y/G LEDs, RGB LED, button, potentiometer |
| 07·2 | **Reflex Game with a Record that Survives Power Off** | Reflex game on the same circuit and `state` pattern; `#include <Preferences.h>`, `prefs.begin()`, `prefs.getULong()`, `prefs.putULong()` (the record survives unplugging) | — | **Milestone Challenge — Anti-Cheat (`challenge_false_start`):** If the button is pressed *while still in Yellow*, jump to a flashing Red "False Start!" state and do not save a record | R/Y/G LEDs, RGB LED, button, potentiometer |
| R2 | **Recap 2 (Ep 05–07)** | No new syntax: trace PWM, `analogRead`/`map` and the state machine; quiz | — | Quiz inside the video | — |

---

### Stage 2: Sensors, Sound, Display & Interrupts (Episodes 08–13)

| # | Episode | Exact Syntax & Functions Taught in Lesson | Multimeter Clip (Phone Camera) | Creative Coding Challenge (Uses *Only* Taught Syntax) | Parts |
|---|---------|-------------------------------------------|--------------------------------|-------------------------------------------------------|-------|
| 08·1 | **Light Sensing (LDR) and Hysteresis** | LDR module on **GPIO 35** (ADC1, so it still works with Wi-Fi later), `analogRead` + hysteresis (`if (light < 1500)` ON, `if (light > 2200)` OFF); why one threshold flickers (naive way first) | **1 Clip (6 s, one hand):** Cover the LDR with your hand while the meter in `Ω` mode jumps from `~2 kΩ` to `50+ kΩ` | (practice task: night light with hysteresis) | LDR module, red LED, multimeter |
| 08·2 | **Touch Pins: a Button Without a Button** | `touchRead(14)` (value drops when touched), finding a threshold with `Serial`, touch with the same edge detection as Ep 04 | — | **Dark Drawer Alarm (3-Second Grace Period, LED only):** In a dark drawer (`light < 1500`), if opened (`light > 2200`), start a 3-second countdown with `millis()`, blinking the LED once per second. If the touch pin is touched *or* the drawer closes within 3 s, return to silent watch; if 3 s expire, the LED flashes fast | LDR module, red LED, a jumper wire as touch pad |
| 09·1 | **Buzzers and Notes** | Active buzzer (`digitalWrite`) vs passive buzzer (`tone(pin, freq)`, `noTone(pin)`), beeps timed with `millis()` | — | (practice task: two-tone siren) | Active + passive buzzers |
| 09·2 | **Arrays and Commands from the Serial Monitor** | 1D C arrays (`int notes[] = {...}`) played with `millis()`; `Serial.available()`, `Serial.read()` (one character → one note) | — | **Secret Drawer Trap (now with sound):** The Ep 08 drawer alarm, but each grace second plays a short `tone()` beep, the alarm is an alternating two-tone siren from an array, and typing `x` in the Serial Monitor disarms it | LDR module, passive buzzer, LED, button |
| 10·1 | **Temperature & Humidity with DHT11** | Installing a library, `#include <DHT.h>`, `dht.begin()`, `float t = dht.readTemperature()`, `float h = dht.readHumidity()`, `isnan(t)`, timed 2-second reads | — | (practice task: print a comfort label) | DHT11 |
| 10·2 | **DHT11 Practice: Comfort Light** | `float` comparison, comfort color on the RGB LED, `isnan` → error blink | — | **Rapid-Change (Draft / Fire) Detector:** Remembering `float baselineTemp` from 10 seconds ago (updated with `millis()`), compare `t - baselineTemp`: if temperature rose by `>= 1.0 °C` within 10 s, blink Red rapidly; if it dropped by `>= 1.0 °C` (open window), turn RGB Blue; otherwise show normal comfort color | DHT11, RGB LED, button |
| 11·1 | **I2C and the OLED Screen: Text** | Button moves **GPIO 22 → 19** (the screen needs 21/22); `#include <Wire.h>`, `#include <Adafruit_SSD1306.h>`, `display.clearDisplay()`, `setTextSize()`, `setCursor(x,y)`, `print()`, `display.display()` | — | (practice task: show the knob value and the temperature) | 0.96" OLED, button, potentiometer |
| 11·2 | **OLED Drawing and Charts** | `drawRect()`, `fillRect()`, `drawLine()`, a live bar | — | **5-Bar Live History Chart + Hold Button:** Using a 5-element array `int bars[5]` (from Ep 09) and `fillRect()`, shift past readings left every second (`bars[0] = bars[1]...`) to draw a 5-column history chart of the sensor/knob, and let the button pause (`bool hold`) the chart on screen | OLED, DHT11, potentiometer, button |
| R3 | **Recap 3 (Ep 08–11)** | No new syntax: hysteresis, arrays, libraries, the screen buffer; quiz | — | Quiz inside the video | — |
| 12·1 | **Motion (PIR) and Obstacle Sensors** | PIR on GPIO 33 (`digitalRead`), IR obstacle sensor on GPIO 13; saving `lastMotion = millis()` | **1 Clip (6 s, one hand):** Move hand in front of IR sensor while meter shows `DO` dropping from `3.3V` to `0.0V` (`FALLING` edge) | (practice task: **Motion Hold Light** — LED on for 5 s after the last motion, button arms / disarms) | PIR, IR obstacle module, LED, button, multimeter |
| 12·2 | **Hardware Interrupts** | Why polling misses fast pulses (naive way first); `volatile int count`, `void IRAM_ATTR onSensor()`, `attachInterrupt(digitalPinToInterrupt(pin), onSensor, FALLING)`, saving `lastHit = millis()` inside the handler | — | **Touchless Speedometer (Passes Per Minute):** Using two `unsigned long` timestamps (`prevHit`, `lastHit`), calculate `dt = lastHit - prevHit` on each interrupt, convert to passes per minute (`60000 / dt`), draw it as a speed bar on the OLED with `fillRect()`, and reset to `0` if `now - lastHit > 3000` | IR obstacle module, OLED, buzzer, button |
| 13·1 | **🏆 Mini-Project 2: Smart Desk Assistant** | Combine OLED + DHT11 + PIR + buzzer + button: study timer that automatically **pauses** when the PIR sees no motion for 15 s; the study record kept with `Preferences` | — | (project part; the challenge is in 13·2) | OLED, DHT11, PIR, buzzer, button |
| 13·2 | **Security Station** | Armed security mode on the same circuit (`int state`), 8-second alarm countdown, siren from an array | — | **Milestone Challenge — Single-Button Rhythm Disarm (Short-Short-Long):** Using the press-duration measurement from Ep 07 (`pressTime = now - pressStart`), disarm the alarm only if the user enters **Short (`<250 ms`), Short (`<250 ms`), Long (`>500 ms`)** tracked with `int step = 0, 1, 2`. Draw `.` or `-` on the OLED as each press finishes | OLED, DHT11, PIR, IR obstacle sensor, buzzer, button, RGB LED |

---

### Stage 3: High-Power Switching, Wi-Fi & IoT (Episodes 14–17)

| # | Episode | Exact Syntax & Functions Taught in Lesson | Multimeter Clip (Phone Camera) | Creative Coding Challenge (Uses *Only* Taught Syntax) | Parts |
|---|---------|-------------------------------------------|--------------------------------|-------------------------------------------------------|-------|
| 14·1 | **Relays: Switching Real Loads Safely** | 2-channel relay on GPIO 16/17 (the green LED on 17 is retired, see PINMAP), 5V module power, **Active-LOW** logic (`const int RELAY_ON = LOW;`), boot-safe initialization (`digitalWrite(pin, HIGH)` before `pinMode`) | **1 Clip (6 s, hands-free):** Probes in relay `COM` & `NO` in **Continuity (Beep)** mode — meter beeps every time the relay clicks | (practice task: relay follows the button) | 2-channel relay, button, multimeter |
| 14·2 | **Automatic Control** | DHT11 thermostat and LDR night switch driving the relays, status on the OLED | — | **Compressor Anti-Short-Cycle & Safety Cutoff:** Using `millis()` and `bool relayOn`, enforce two rules on Relay 1: (1) after turning OFF, block it from turning back ON for 15 seconds (show `"COOLDOWN"` countdown on OLED), and (2) if ON continuously for 30 seconds, force it OFF into a `"FAULT"` state until the button is pressed | 2-channel relay, DHT11, LDR, OLED, button |
| R4 | **Recap 4 (Ep 12–14)** | No new syntax: interrupts, project state machines, active-LOW; quiz | — | Quiz inside the video | — |
| 15·1 | **Wi-Fi and Network Time** | `#include <WiFi.h>`, `WiFi.scanNetworks()`, `WiFi.RSSI(i)`, non-blocking `WiFi.begin(ssid, pass)` with `WiFi.status() == WL_CONNECTED`, `configTime()`, `struct tm timeinfo`, `getLocalTime(&timeinfo)` (`tm_hour`, `tm_min`, `tm_sec`) | — | **Offline-Resilient Hybrid Clock:** Fetch hour/min/sec **once** when Wi-Fi connects, then advance `sec++` every `1000 ms` with `millis()` (rolling over `sec == 60 -> min++`, `min == 60 -> hour++`, `hour == 24 -> 0`) so the OLED clock keeps ticking even with the router off | Board, OLED, button |
| 15·2 | **Access Point Mode: No Router Needed** | `WiFi.softAP(ssid, pass)`, `WiFi.softAPIP()`, the phone joins the board's own network; first one-page `WebServer` | — | (practice task: AP page that shows the knob value) | Board, OLED, potentiometer |
| 16·1 | **Web Server: Control from the Phone** | `#include <WebServer.h>`, `WebServer server(80)`, `server.on("/...", handler)`, `server.send(200, "text/html", html)`, `server.handleClient()`, HTML links that switch the LED and the relay (**zero JavaScript**) | — | (practice task: `/on`, `/off`, `/toggle` pages) | LED, RGB LED, relay |
| 16·2 | **Live Sensor Dashboard** | Sensor values in the page, `<meta http-equiv='refresh' content='2'>` | — | **Auto-Off Web Timer (`/run10` & `/run30`):** Two links turn Relay 1 ON with `unsigned long offDuration = 10000` (or `30000`); count down the remaining seconds on both the OLED and the auto-refreshing page, and let the physical button cancel the timer early | 2-channel relay, DHT11, LDR, OLED, button |
| 17·1 | **🏆 Final Project: Smart Room Monitor** | Full integration using only learned functions: multi-page OLED (`int page`), DHT11 + LDR + PIR, relay automation, buzzer alarm | — | (project part; the challenge is in 17·2) | Most of the starter kit |
| 17·2 | **Smart Room Controller on the Phone** | `WebServer` dashboard for the whole room, settings kept with `Preferences` | — | **Season 1 Graduation Challenge — Event Counter & Last-Seen Dashboard:** Track daily activations (`int motionCount`, `int relayCount`) and record the `hour` and `min` of the last PIR motion and the highest temperature peak. Show the summary on OLED Page 3 **and** on the phone page, with a physical + web `"Reset Stats"` button | Most of the starter kit |

---

## What changed in v5 (28 October 2026, creator approved)

- Every episode from 05 is two parts of 6–9 min instead of one ~10 min video; 19 → 17 episodes, but more videos (26 parts + 3 recaps after Recap 1).
- Merged: old 07 `map()` → 06·2; old 14 interrupts → 12·2; old 08 mini-project 1 → 07; old 09/10 now 08/09 with new second parts.
- Added: pin plan and pin rules (06·1), debugging as a skill (06·1 and every episode after), schematics, touch pins (08·2), `Preferences` (07·2), Serial input (09·2), Wi-Fi access point mode (15·2), Recaps 2–4.
- Multimeter clips follow their topics: 05, 06, 08 (LDR), 12 (IR), 14 (relay).

## Season 2 — Going Deeper (Extra Parts & Advanced ESP32)

Deep sleep and battery power (measuring µA/mA sleep current with the multimeter) · Bluetooth Low Energy (BLE) ·
MQTT and cloud dashboards · Servo, DC and stepper motors · ESP-NOW board-to-board wireless ·
Pure C with ESP-IDF and FreeRTOS tasks.
