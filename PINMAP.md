# Pin map — Season 1 (v6 numbering, 29 October 2026)

One pin plan for the whole season: a part keeps its pin from the first episode it appears in, so the circuit on the
two breadboards grows instead of being rebuilt. Scripts, sketches, shoot packs and wiring pictures must follow this table.

| GPIO | Part | From episode | Notes |
|---|---|---|---|
| 23 | Red LED (220 Ω) | 03 | Car red light in 09 |
| 25 | Green LED (220 Ω) | 03–05 | Removed in 06: GPIO 25 becomes the RGB red leg |
| 22 | Button (`INPUT_PULLUP`) | 04 | **Moves to GPIO 19 in 17** (the OLED needs 22) |
| 25 / 26 / 27 | RGB LED red / green / blue (3× 220 Ω), common cathode | 06 | Walk light in 09, result light in the reflex game (10) |
| 34 | Potentiometer wiper | 07 | Input-only pin; ADC1 (works with Wi-Fi on). Pot ends on 3V3 and GND, never 5 V |
| 18 | Yellow LED (220 Ω) | 08 | Level bar, car yellow light |
| 17 | Green LED (220 Ω) | 08 | Level bar, car green light. **Retired in 23**: GPIO 17 becomes relay 2 |
| 35 | LDR module `AO` | 11 | Input-only, ADC1 (works with Wi-Fi on) |
| 14 | Touch pad (a bare jumper wire) | 12 | `touchRead(14)` = T6 |
| 32 | Buzzer (passive; active buzzer on the same pin when compared) | 13 | |
| 4 | DHT11 data | 15 | |
| 21 / 22 | OLED I2C SDA / SCL | 17 | ESP32 default I2C pins |
| 19 | Button (new place) | 17 | Same button, same code with `BUTTON_PIN = 19` |
| 33 | PIR `OUT` | 19 | |
| 13 | IR obstacle `DO` | 19 | Interrupt pin in 20 |
| 16 / 17 | Relay `IN1` / `IN2` (active-LOW, module powered from 5 V / VIN) | 23 | Boot-safe: `digitalWrite(pin, HIGH)` before `pinMode` |

## Pin rules taught in 07 (Espressif)

- **GPIO 34–39 are input only** (no `pinMode(OUTPUT)`, no internal pull-up). The 30-pin board has 34, 35, 36 (VP), 39 (VN).
- **ADC2 pins (0, 2, 4, 12–15, 25–27) cannot `analogRead` while Wi-Fi is on.** Every analog sensor in the season is on ADC1 (32–39): pot 34, LDR 35.
  (Pin 4 is ADC2 but the DHT11 is digital, so it is fine.)
- **Boot (strapping) pins 0, 2, 5, 12, 15** are read at power-on; nothing in the season is wired to them.
- **GPIO 1 / 3** are the USB serial (TX/RX) and **6–11** are the flash chip: never used.

## Free pins left

2, 5, 12, 15 (all strapping pins: only for outputs that are safe at boot, e.g. Season 2), 36, 39 (input only).
