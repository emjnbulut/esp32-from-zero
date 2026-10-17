# Curriculum

Target viewer: knows basic C (variables, `if`, loops, functions), has never used a microcontroller.
Language: C-style code on the Arduino framework (Arduino IDE 2.x + Espressif ESP32 core).
Each episode: 5–10 minutes (from 04 on: two topics, 10–15 minutes), English narration, English + Turkish subtitles.

Kit: direnc.net "ESP-32S WiFi Başlangıç Seti" — ESP32 dev board, 830-point breadboard, 0.96" OLED,
DHT11, HC-SR501 PIR, obstacle sensor module, LDR module, 10k potentiometer, active + passive buzzer,
2-channel 5V relay, 6 push buttons, red, yellow and green LEDs (4 of each in the creator's kit), 2 RGB LEDs, 220Ω / 1kΩ / 10kΩ resistors,
jumper wires (M-M, F-M, F-F), micro USB cable.

## Season 1 — Starter kit

| #  | Episode | You learn | Parts |
|----|---------|-----------|-------|
| 01 | Setting Up Your Computer | Install Arduino IDE, USB driver, ESP32 board package; first upload; Serial Monitor "Hello" | Board, USB cable |
| 02 | Meet the Board and the Breadboard | What the pins are, 3V3/5V/GND, safe GPIOs, how breadboard rows connect | Board, breadboard |
| 03 | Your First Circuit: Blink an LED | `pinMode`, `digitalWrite`, `delay`, why the 220Ω resistor (Ohm's law, simply) | LED, 220Ω |
| 04 | Buttons and Doing Two Things at Once | `digitalRead`, pull-up / pull-down, `INPUT_PULLUP`, debounce; why `delay()` blocks, `millis()` timing | Button, LED |
| 05 | PWM and the Potentiometer | PWM idea, `analogWrite` / LEDC, fading, RGB color mixing; ADC 0–4095, `analogRead`, `map`, a dimmer knob | LED, RGB LED, 220Ω, potentiometer |
| 06 | Light and Sound | LDR module (analog + digital out), automatic night light; active vs passive buzzer, `tone`, a melody from an array | LDR module, LED, both buzzers |
| 07 | Temperature and the OLED Screen | Installing a library, DHT11 readings; I2C in plain words, SSD1306 library, text and numbers on screen | DHT11, OLED |
| 08 | Motion, Obstacles and Interrupts | PIR (HC-SR501) and IR obstacle module, a simple alarm; `attachInterrupt`, ISRs, `volatile` | PIR, obstacle module, buzzer, button |
| 09 | Relays and WiFi | What a relay does, safety, driving the 2-channel module; station mode, scanning networks, getting an IP | Relay module, board |
| 10 | Web Server and a Live Sensor Page | Control an LED from your phone's browser; serve DHT11 + LDR readings, auto refresh | LED, DHT11, LDR |
| 11 | Final Project: Smart Room Monitor | Combine OLED + DHT11 + PIR + buzzer + web page | Most of the kit |

From episode 04 on, each episode covers two topics of the original 18-topic plan (decided 2026-10-17:
single-topic episodes came out too short), and episodes aim for 10–15 minutes (user, 2026-10-17).

## Season 2 — Ideas (needs extra parts or goes deeper)

Deep sleep and battery power · Bluetooth (BLE) · MQTT and cloud dashboards · Servo and motors ·
Pure C with ESP-IDF and FreeRTOS tasks.
