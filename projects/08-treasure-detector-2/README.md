# 08 · Hazine Dedektörü 2.0 / Treasure Detector 2.0

Sketch: [`treasure_detector_2/treasure_detector_2.ino`](treasure_detector_2/treasure_detector_2.ino) · 3D Short: `video/short3d/treasure_tr`

## Türkçe

Düğmenin (potansiyometre) üstünde 0-99 arasında bir yere hazine saklı. Düğmeyi çevirerek ara:

- **Uzaktaysan** RGB LED buz mavisi, buzzer yavaş ve kalın tıklıyor, ekranda **SOĞUK**.
- **Yaklaştıkça** renk kırmızıya döner, tıklar Geiger sayacı gibi hızlanır ve incelir: **ILIK**, **SICAK**, **YANIYOR!**
- **KAZ!** (butona bas): doğru yerdeysen buzzer'da zafer melodisi, ekranda **HAZİNE!** ve bulma süren. En iyi süre
  `Preferences` ile saklanır, fişi çeksen bile silinmez (Bölüm 10'daki gibi). Sonra hazine yeni bir yere saklanır.
  Yanlış yerdeysen kalın bir vızıltı: **BOŞ!**

**Devre:** Bölüm 10'un devresi aynen kalır (OLED SDA 21 / SCL 22, buton D19, pasif buzzer D32), üstüne iki parça eklenir:

| Parça | Bağlantı |
|---|---|
| Potansiyometre (10k) | dış bacaklar 3V3 ve GND, orta bacak → GPIO 34 |
| RGB LED (ortak katot) | kırmızı → 25, yeşil → 26, mavi → 27 (her biri 220 Ω dirençle), uzun bacak → GND |

Kütüphane: Kütüphane Yöneticisi'nden **Adafruit SSD1306** (Adafruit GFX ve BusIO ile birlikte gelir).
Ortak anotlu RGB LED'de `COMMON_ANODE = true` yap ve uzun bacağı 3V3'e bağla (Bölüm 5).

Nasıl çalışır: `analogRead(34)` 0-4095 verir, `map()` bunu 0-99'a çevirir. `abs(sayi - hazine)` uzaklığı ölçer;
uzaklık rengi (`heat`), tık aralığını (60-700 ms) ve tık sesini (3000-800 Hz) belirler. Ekranın yazı tipinde Türkçe
harf olmadığı için Ğ, İ ve Ş'nin işaretleri `bigWord()` içinde piksel piksel çizilir.

Dene: hazine bölgesini daralt (`distance <= 1`), ya da tıkları daha da hızlandır (`map(distance, 0, 50, 30, 700)`).

## English

A treasure hides somewhere on the knob (0-99). Turn to search: far away the RGB LED is ice blue, the passive buzzer
ticks slowly and low and the OLED says SOĞUK (cold); closer, the colour warms to red and the ticks get faster and
higher like a Geiger counter (ILIK, SICAK, YANIYOR! = warm, hot, burning). Press the button to dig (KAZ!): on the spot
you get a fanfare, HAZİNE! (treasure) and your time; the best time is saved with `Preferences` and survives unplugging
(as in Episode 10), then the treasure hides again. Wrong spot: a low buzz, BOŞ! (empty).

Circuit: the Episode 10 circuit unchanged (OLED SDA 21 / SCL 22, button D19, passive buzzer D32) plus a 10k knob
(outer legs 3V3/GND, wiper GPIO 34) and a common-cathode RGB LED on 25/26/27 through 220 Ω resistors.
Library: Adafruit SSD1306 (+ GFX, BusIO). The OLED's built-in font has no Turkish letters, so `bigWord()` prints the
capital letter and draws the breve/dot/cedilla of Ğ, İ, Ş itself (in the word strings a lowercase g/i/s marks them).

Compiled with arduino-cli for `esp32:esp32:esp32` (core 3.3.12); not yet tried on hardware.
