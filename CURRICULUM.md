# Curriculum

Target viewer: knows basic C (variables, `if`, loops, functions), has never used a microcontroller.
Language: C-style code on the Arduino framework (Arduino IDE 2.x + Espressif ESP32 core).
Each episode: 5–10 minutes, English narration, English + Turkish subtitles.

Kit: direnc.net "ESP-32S WiFi Başlangıç Seti" — ESP32 dev board, 830-point breadboard, 0.96" OLED,
DHT11, HC-SR501 PIR, obstacle sensor module, LDR module, 10k potentiometer, active + passive buzzer,
2-channel 5V relay, 6 push buttons, 5 yellow + 5 green LEDs, 2 RGB LEDs, 220Ω / 1kΩ / 10kΩ resistors,
jumper wires (M-M, F-M, F-F), micro USB cable.

## Season 1 — Starter kit

| #  | Episode | You learn | Parts |
|----|---------|-----------|-------|
| 01 | Setting Up Your Computer | Install Arduino IDE, USB driver, ESP32 board package; first upload; Serial Monitor "Hello" | Board, USB cable |
| 02 | Meet the Board and the Breadboard | What the pins are, 3V3/5V/GND, safe GPIOs, how breadboard rows connect | Board, breadboard |
| 03 | Your First Circuit: Blink an LED | `pinMode`, `digitalWrite`, `delay`, why the 220Ω resistor (Ohm's law, simply) | LED, 220Ω |
| 04 | Buttons: Reading the Real World | `digitalRead`, pull-up / pull-down, `INPUT_PULLUP`, debounce | Button, LED |
| 05 | Doing Two Things at Once | Why `delay()` blocks; `millis()` timing | 2 LEDs, button |
| 06 | Dimming and Colors with PWM | PWM idea, `analogWrite` / LEDC, fading, RGB color mixing | LED, RGB LED, 220Ω |
| 07 | Analog Input: The Potentiometer | ADC 0–4095, `analogRead`, `map`, a dimmer knob | Potentiometer, LED |
| 08 | Sensing Light | LDR module (analog + digital out), automatic night light | LDR module, LED |
| 09 | Making Sound | Active vs passive buzzer, `tone`, playing a melody from an array | Both buzzers |
| 10 | Temperature and Humidity | Installing a library, DHT11, reading and printing data | DHT11 |
| 11 | The OLED Screen and I2C | I2C in plain words, SSD1306 library, text and numbers on screen | OLED, DHT11 |
| 12 | Motion and Obstacles | PIR (HC-SR501) and IR obstacle module, a simple alarm | PIR, obstacle module, buzzer |
| 13 | Interrupts | `attachInterrupt`, ISRs, `volatile` | Button, PIR |
| 14 | Relays: Switching Bigger Things | What a relay does, safety, driving the 2-channel module | Relay module |
| 15 | Connecting to WiFi | Station mode, scanning networks, getting an IP | Board |
| 16 | Your First Web Server | Control an LED from your phone's browser | LED |
| 17 | Live Sensor Web Page | Serve DHT11 + LDR readings, auto refresh | DHT11, LDR |
| 18 | Final Project: Smart Room Monitor | Combine OLED + DHT11 + PIR + buzzer + web page | Most of the kit |

## Season 2 — Ideas (needs extra parts or goes deeper)

Deep sleep and battery power · Bluetooth (BLE) · MQTT and cloud dashboards · Servo and motors ·
Pure C with ESP-IDF and FreeRTOS tasks.
