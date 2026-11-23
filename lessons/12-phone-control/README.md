# Episode 12 — Control Your ESP32 from Your Phone (No App, No Router)

> DRAFT (24 Nov 2026). The sketch compiles (esp32 core 3.3.12) but has not been tested on a real board yet.

Your phone becomes a remote control: tap RED and the color LED turns red, tap RING and the buzzer plays a doorbell, and the screen
shows every command as it arrives. No app to install and no home Wi-Fi needed: the board opens its **own** small Wi-Fi network and
serves a tiny web page.

**You need:** nothing new. The RGB LED (Episode 6), the OLED screen and the passive buzzer (Episode 10).

| Part | Pin |
|---|---|
| RGB LED red / green / blue | GPIO 25 / 26 / 27 (220 Ω each, common cathode to GND) |
| OLED `SDA` / `SCL` | GPIO 21 / GPIO 22 |
| Passive buzzer `+` | GPIO 32 |

## 1. The board opens its own Wi-Fi

```cpp
WiFi.softAP("PinByPin-ESP32", "esp32lab");   // network name, password (8+ characters)
```

The ESP32 becomes an **access point**, like the hotspot on a phone. Your phone joins it in its Wi-Fi settings. Inside that tiny
network the board always has the same address, **192.168.4.1** — think of it as the board's house number.

## 2. A web page where every button is a link

The page is a ready template in the sketch (`PAGE`). You only change labels and colors. Each button is a link:

| Button | Link | What the board does |
|---|---|---|
| RED | `/color?c=red` | `setColor(255, 0, 0)` |
| GREEN / BLUE / OFF | `/color?c=green` ... | the same with other colors |
| RING | `/ring` | two notes on the buzzer |

The sketch tells the web server which function answers which link:

```cpp
server.on("/", sendPage);
server.on("/color", handleColor);   // server.arg("c") reads the part after ?c=
server.on("/ring", handleRing);
```

and `loop()` only has one job: look for a phone knocking, many times a second.

```cpp
void loop() {
  server.handleClient();
}
```

## 3. Try it

1. Upload, open the Serial Monitor (115200): it prints `192.168.4.1`. The OLED says `open 192.168.4.1`.
2. On the phone: Wi-Fi settings → **PinByPin-ESP32**, password **esp32lab**. The phone may warn "no internet": stay connected.
3. Open the browser and type `192.168.4.1`. Tap the buttons.

## 4. Common problems

- **The page does not open:** the phone left the board's network because it has no internet. Turn off mobile data for a moment, or
  choose "stay connected" when the phone asks.
- **Wrong address:** type `192.168.4.1` exactly, without `www` or `https`.
- **Password not accepted:** a Wi-Fi password needs at least 8 characters, otherwise `softAP()` fails silently.

## 5. Your turn

Add a **PARTY** button that cycles through red, green and blue three times. Hint: a new `server.on("/party", ...)` and a new link
in the page.

## Code

- [`code/phone_remote`](code/phone_remote/phone_remote.ino) — the episode's sketch
- [`code/challenge_party`](code/challenge_party/challenge_party.ino) — challenge solution

Libraries: **Adafruit SSD1306** and **Adafruit GFX** (Episode 10). `WiFi` and `WebServer` come with the ESP32 core.
