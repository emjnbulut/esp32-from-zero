# Curriculum v7 — DRAFT (21 November 2026, not yet approved)

Proposal for Episodes 10–30 after the creator's 21 Nov direction. Episodes 01–09 stay as published. Nothing in
`CURRICULUM.md`, `PINMAP.md` or `video/YAYIN_TAKVIMI.md` is changed until the creator approves this draft.

## Özet (Türkçe)

- **Her bölüm = yeni bir parça + tek eğlenceli proje.** LED/buton/pot dönemi Bölüm 9'da kapanıyor. Önce kitteki
  kullanılmamış parçalar (OLED, buzzer, PIR, DHT11, LDR, IR, röle, dokunmatik, Wi-Fi), Bölüm 19'dan sonra ucuz ek
  modüller (servo, ultrasonik, RGB halka, joystick, MPU6050, toprak nem sensörü + pompa).
- **Telefondan kontrol öne çekildi:** v6'da Bölüm 25–28'deydi, şimdi **Bölüm 12**'de (uygulama yok, modem yok: kart
  kendi Wi-Fi'sini açar). Sonra hemen her bölümün telefon tarafı olabiliyor (hava istasyonu 13, röle 17, oda 18).
- **Daha az kod, daha az teknik detay:** ekranda yalnız işi yapan 3–8 satır; tam çizim ders klasöründe. Kütüphane
  fonksiyonları "şu üç satır" diye verilir, iç yapısı anlatılmaz. Hedef süre **6–8 dk** (v6: 8–12 dk).
- **3D her yerde:** her bölümde 3–6 kısa 3D çekim (parçanın içi / X-ray, kurulum montajı, sonuç). Her bölümün X-ray
  klibi ayrıca "45 saniyede nasıl çalışır?" Short'una malzeme olur.
- **Recap'ler kalkıyor:** tekrarın yerini **birleştirme projeleri** alıyor (18 akıllı oda, 21 radar, 25 oyun
  konsolu, 29–30 final). Recap 2 video olarak yayımlanmaz (bölüm 5'teki öneri).
- **30 bölüm korunuyor**, recap'ler düştüğü için sezon v6'dan ~1 hafta önce biter (Bölüm 10 = 27 Kas ise Bölüm 30 =
  5 Şubat). Ek modül maliyeti toplam ~12–15 USD; **Aralık başına kadar sipariş** gerekir.
- Başlıklar sonuç önde ("I Built …"), her bölüm tek başına izlenebilir, her bölümün EN + TR proje Short'u var
  (TR'de Türkçe ekran yazısı).

---

## 1. What changes vs v6 (and why)

| v6 | v7 | Why |
|---|---|---|
| One topic per episode, often a concept (map(), interrupts) | One **new part** + one **fun project** per episode | Creator: same 3 parts got boring; channel data: project titles beat concept titles (CTR 1.9–2.9% for concept titles) |
| Phone control at Ep 25–28 | **First phone control at Ep 12**, reused in 13, 17, 18, 22, 27, 28, 30 | Most attractive ESP32 feature; viewers are 97% new and arrive from recommendations |
| Full code on screen (guideline §7), code tours | **Key 3–8 lines only**, full sketch in lesson folder + learning site; libraries = "these three lines" | "kodlamaya boğmadan"; §7 needs an update if approved |
| 8–12 min target | **6–8 min**, 10 hard limit | "tempo çok yavaş"; Guo et al.: watch time drops after ~6 min |
| Recaps after 10/18/24 | **No recaps**; combination projects at 18, 21, 25, 29–30 do the reviewing | §12.5: no long recaps, at most an 8-min mini project |
| Multimeter clips 11/19/23 (camera) | 3D meter overlay inside the X-ray clip when useful | §12.8: no filming |
| Kit only | Kit first (10–18), then 6 cheap modules + a pump (19–28) | Variety; every module < 5 USD |

Kept: "Zero Unlearned Syntax" in a softer form (a challenge uses only lines that were shown), naive-way-first where it
fits in one minute, one common mistake per episode, one pin plan, `millis()` timers and `state` variables from 1–9.

---

## 2. Episodes 10–30

Price class: **$** < 2 USD · **$$** 2–5 USD. "Kit" = creator's starter kit. 3D = three.js kit (§12.8), Blender only
for thumbnail / hero frame.

| # | Title (EN, result-first; then `\| ESP32 From Zero #N`) | New part(s) | Big idea (plain words · key functions) | Fun project | 3D clips | Project Short (EN + TR) | Kit / buy |
|---|---|---|---|---|---|---|---|
| 10 | **I Built a Reflex Game with a Screen and Sound** *(decided)* | 0.96" OLED SSD1306 (I2C), passive buzzer | A screen is a drawing you prepare, then show; a buzzer plays a pitch; the record is kept in a drawer that survives power-off · `display.clearDisplay()`, `print()`, `display.display()`, `tone()`, `prefs.putULong()` | Reflex Game 2.0: "WAIT…GO!", ms on the OLED, fanfare on a new record, record survives unplugging | macro: OLED pixels light up row by row · X-ray: data dots travel along SDA/SCL · buzzer disc vibrating with sound rings · USB pulled out, record glows in the chip's "drawer" · assembly montage | "Can you beat 180 ms?" / "180 ms'yi geçebilir misin?" | Kit |
| 11 | **I Built a Motion Alarm That Catches Anyone Sneaking In** | HC-SR501 PIR (+15 s active vs passive buzzer) | The sensor does the hard work and only says yes/no; remember *when* it last said yes · `digitalRead()`, `lastMotion = millis()` | Room guard: button arms it, 10 s grace countdown on OLED, siren, "last seen 2 min ago" | PIR dome: lens zones fan out like flashlight beams · warm hand crosses zones, pin goes HIGH · the two trim knobs (time / sensitivity) turning · cutaway: active buzzer has its own beeper inside | "Cookie jar guard" / "Kurabiye kavanozu bekçisi" | Kit |
| 12 | **Control Your ESP32 from Your Phone — No App, No Router** | Wi-Fi (built in), access-point mode | The board opens its own Wi-Fi and serves a tiny web page; each button on the page is a link = a command · `WiFi.softAP()`, `server.on()`, `server.send()`, `server.handleClient()` (page = ready template, viewer edits labels only) | Phone remote: color buttons for the RGB LED, "ring" button for the buzzer, OLED shows the last command | radio ripples from the PCB antenna to a phone · tap → packet flies → LED changes color · zoom on the zig-zag antenna · "192.168.4.1" floating over the board like a house number | "Phone doorbell that plays a melody" / "Telefondan çalan kapı zili" | Kit |
| 13 | **I Built a Weather Station You Can Check from Your Phone** | DHT11 | First library you install yourself; three lines give temperature and humidity; read every 2 s; `isnan()` = sensor didn't answer · `dht.begin()`, `readTemperature()`, `readHumidity()` | OLED weather card (big numbers + comfort face), same values on the Ep 12 phone page with auto-refresh | DHT11 cage opens: humidity plate soaks droplets, thermistor glows · one-wire data pulses · OLED digits counting up · phone and OLED side by side | "Breathe on it: 40% → 90%" / "Nefesinle nemi 90'a çıkar" | Kit |
| 14 | **I Turned Bananas into a Piano** | Touch pins (built in) | Your body is a tiny capacitor: the number drops when you touch; a list of notes = an array · `touchRead()`, `int notes[]`, `tone()` | 3-key fruit piano (pads on 14, 2, 15) that can record and replay 8 notes | finger nears a banana, charge cloud, number on screen drops · array as a row of boxes lighting up as notes play · sound waves from fruit keys · wire entering pin T6 | "A plant that screams when you touch it" / "Dokununca bağıran çiçek" | Kit (+ fruit/foil) |
| 15 | **My Drawer Screams When Someone Opens It** | LDR module | Light becomes a number; two thresholds (hysteresis) stop the flicker · `analogRead(35)`, `if (light > ON) … if (light < OFF)`; counter in Preferences | Drawer spy: alarm + "opened 3× while you were away" on the OLED | dark drawer slides open, light floods the LDR · light graph: one threshold flickers vs two dashed lines calm · resistance squiggle shrinking · buzzer screams | "Night light that fades on at dusk" / "Hava kararınca kendi yanan gece lambası" | Kit |
| 16 | **I Built a Basketball Scoreboard That Counts Every Shot** | IR obstacle sensor | An interrupt is a doorbell instead of checking the door; you never miss a fast ball · `attachInterrupt()`, `volatile`, `IRAM_ATTR` ("just put this word here") | Paper-cup hoop: IR under the rim counts baskets, 30 s round, OLED score, horn, best score saved | ball through hoop breaks the (shown red) IR beam, pin drops LOW · split screen: polling ticks miss the ball, interrupt catches it · scoreboard digits flip | "Piggy bank that counts coins" / "Paraları sayan kumbara" | Kit |
| 17 | **My Phone Switches a Real Fan with an ESP32** | 2-channel 5 V relay | A relay is a switch flipped by a tiny electromagnet; this module is on when the pin is LOW; set HIGH before `pinMode` so it doesn't click at boot · `digitalWrite(RELAY1, LOW)` + Ep 12 page | Phone-controlled USB desk fan with auto-off timer and "auto above 28 °C" (DHT) mode | X-ray: coil energises, field lines, arm snaps over (click) · low-voltage side and load side with a glowing safety gap · phone tap → click → fan spins | "Desk lamp that turns on when you sit down" (PIR + relay) / "Masaya oturunca yanan lamba" | Kit (USB fan/lamp; **5 V loads only**, no mains in S1) |
| 18 | 🏆 **I Turned My Room into a Smart Room with a $10 Kit** | — (milestone: whole kit) | One `loop()`, many timers; OLED pages (`int page`); one phone dashboard for everything | Smart Room v1: weather, light, motion alarm, fan auto, phone dashboard | full assembly montage, every part flies to its breadboard coordinate · desk diorama day → night · OLED pages flipping · live phone dashboard | "Every sensor in my ESP32 kit in 45 s" / "Kitimdeki her sensör 45 saniyede" | Kit (end of kit block) |
| 19 | **I Built a Candy Machine with a $2 Servo** | SG90 servo | A servo goes to the angle you ask (0–180°); the library makes the pulses; power from 5 V · `servo.attach(18)`, `servo.write(angle)` | Candy dispenser: press (or beat your reflex record) → gate opens, candy drops, jingle | X-ray: motor, gears and a **potentiometer** inside reporting the angle · pulse width → arm angle dial · gate tilts, slow-mo candy fall · brownout mistake: board resets when servo jerks | "Desk robot that waves when you come near" / "Yaklaşınca el sallayan robot" | Buy $ |
| 20 | **I Built a Parking Sensor That Beeps Faster as You Get Closer** | HC-SR04 ultrasonic | Like a bat: send a click, time the echo; distance = time × speed of sound ÷ 2 · `pulseIn()`, `map()` (known) | Parking sensor: OLED distance bar, beeps speed up, red zone below 10 cm | sound rings leave the "eyes", bounce off a toy car, return · timeline "there + back ÷ 2" · divider X-ray 5 V → 3.3 V · car creeping to the wall | "A door frame that measures your height" / "Boyunu ölçen kapı" | Buy $ |
| 21 | 🏆 **I Built a Mini Radar with an ESP32** | — (milestone: servo + ultrasonic + OLED) | Sweep and draw: step the angle, measure, draw one line per angle (ready helper `drawRadarLine(angle, cm)`, no trig in the video) | Radar screen with sweeping beam, fading blips, ping when something is close | sensor-on-servo sweeping a desk diorama · green sweep with fading dots on the OLED · top view of beams hitting objects · hand appears → blip + ping | "Trash can that opens itself" / "Kendi açılan çöp kutusu" | Parts of 19–20 |
| 22 | **I Built an LED Ring with Rainbow Animations** | WS2812B 12-LED ring | Every LED has its own tiny chip; one data wire; set colors in a list, then `show()` · `ring.setPixelColor(i, r, g, b)`, `ring.show()`, `setBrightness()` | Focus-timer ring: empties LED by LED, rainbow when done; color picked on the phone page | data packet passed along the LEDs like a bucket chain (each keeps its 3 bytes) · macro of one LED: R/G/B dies + chip · rainbow spinning · a for-loop cursor moving over pixels | "A lamp that flickers like real fire" / "Gerçek ateş gibi titreyen lamba" | Buy $$ |
| 23 | **I Made a Handheld Game on a Tiny Screen** | KY-023 joystick | A joystick is just two knobs (and a button); a small dead zone in the middle · `analogRead(34)`, `analogRead(39)`, `map()` (known) | "Dodge": ship moves with the stick, blocks fall, score, high score saved | X-ray: two pots at 90° under the stick · tilt → two numbers change · ship dodging on the OLED · dead-zone circle | "Etch-a-sketch on an OLED" / "Joystick ile çizim tahtası" | Buy $ |
| 24 | **I Built a Tilt-Controlled Marble Game** | MPU6050 (on the same I2C wires as the OLED) | Two devices share two wires; each has its own address (OLED 0x3C, MPU 0x68); read the tilt · `mpu.begin()`, `mpu.getEvent()`, `a.acceleration.x / y` | Tilt maze: a ball rolls on the OLED, avoid holes; bonus spirit level | inside the chip: tiny mass on springs shifts as the board tilts · I2C as a street with two numbered houses · board tilts, ball rolls · spirit-level bubble | "Shake it to roll a dice" / "Salla, zar atsın" | Buy $ |
| 25 | 🏆 **I Built My Own Game Console with an ESP32** | — (milestone: joystick + MPU + OLED + ring + buzzer) | A menu is one `state` variable choosing which game runs; one high score per game | Console: Dodge, Tilt Maze, Reflex 2.0; ring shows lives | console assembly montage · menu carousel · ring lives draining · high-score fanfare | "3 games, one $5 board" / "Tek kartta 3 oyun" | Parts of 22–24 |
| 26 | **I Built a Clock That Sets Itself from the Internet** | Wi-Fi station mode (+ ring as clock face) | Join home Wi-Fi, ask a time server once, then count yourself · `WiFi.begin()`, `configTime()`, `getLocalTime()` | Ring clock: hour, minute and second LEDs in 3 colors, date on OLED, buzzer alarm | board → router → globe → time server, time packet returns · ring as clock face with three colored "hands" · sunrise glow alarm | "Alarm clock that wakes you like a sunrise" / "Güneş doğar gibi uyandıran saat" | Kit + ring |
| 27 | **My ESP32 Sends Notifications to My Phone** | Internet push (free ntfy app, `HTTPClient`) | Posting a message is like dropping a letter in a mailbox your phone watches; private topic name; cooldown so it doesn't spam · `http.begin(url)`, `http.POST("text")` | Doorbell / intruder notifier: button or PIR → "Someone's at the door 14:05" | letter flies board → router → cloud mailbox → phone, phone buzzes · notification banner · cooldown ring | "Mailbox that tells me when post arrives" (IR) / "Mektup gelince haber veren posta kutusu" | Kit (+ free app) |
| 28 | **I Built a Plant That Waters Itself** | Capacitive soil sensor v1.2 + 5 V mini pump (relay 2) | Calibrate dry vs wet; water in short bursts then wait (hysteresis + timer, both known) · `analogRead(36)`, relay | Self-watering pot: waters when dry, phone push "I just drank", log on OLED | pot cross-section, blue moisture gradient sinking · sensor field lines in soil · pump pushing water through the tube, relay click · push arrives | "A plant that texts you when it's thirsty" / "Susayınca mesaj atan çiçek" | Buy $ (sensor) + $$ (pump + tube) |
| 29 | 🏆 **Final Project: I Built a Smart Home Hub with an ESP32** | — (all) | Big project = small pieces as functions, one `state` per job, timers instead of `delay()` | Hub: ring clock, weather, motion alarm, fan, plant, OLED pages | full assembly montage with coordinates · desk diorama 24 h time-lapse · every module lights up in turn | "Everything my ESP32 can do" / "ESP32'mle yapabildiğim her şey" | Kit + bought |
| 30 | 🏆 **Final Project: My Whole Smart Home on My Phone** | — (all) | Phone dashboard + settings saved in Preferences + push alerts | Phone page: live values, fan / alarm / ring color buttons, alarm-temperature setting, alerts | phone dashboard with the board behind · settings survive unplugging · graduation montage of all 30 projects | "From a blinking LED to a smart home in 30 episodes" / "Yanıp sönen LED'den akıllı eve" | — |

**Buy list (before Ep 19):** SG90 servo, HC-SR04 (prefer the 3.3–5 V "HC-SR04P / RCWL-1601" version: no divider),
WS2812B 12-LED ring, KY-023 joystick, GY-521 MPU6050, capacitive soil sensor v1.2, 5 V mini submersible pump + 1 m
tube. Total ≈ 12–15 USD. Optional: 470 µF capacitor (servo), 5 V 2 A USB supply (pump + ring).

**Left out of Season 1 (→ Season 2):** RC522 RFID (needs 4–5 SPI wires; all sensible pins are taken, see §4),
DFPlayer + speaker (needs SD card + UART pins), 4-digit display (the OLED already does it), BLE, ESP-NOW (needs two
boards), deep sleep, motors.

**New 3D models needed (in order):** OLED, buzzer (10) · PIR (11) · phone (12) · DHT11 (13) · fruit/touch pad (14) ·
LDR module (15) · IR module, hoop (16) · relay, USB fan (17) · servo (19) · HC-SR04 (20) · WS2812 ring (22) ·
joystick (23) · MPU6050 (24) · soil sensor, pump, pot (28).

---

## 3. Ordering logic

- **Gentle libraries:** Ep 10 introduces the first library (OLED) with "three lines" style; 11 needs none (rest);
  12 uses built-in Wi-Fi libraries; 13 is the first library the viewer installs. After that one new library at most
  per episode (servo 19, NeoPixel 22, MPU 24, HTTPClient 27).
- **Known ideas reused, not re-taught:** `millis()` timers, `state`, edge detection, `map()`, Preferences show up in
  every project; new *ideas* are few and placed where a part needs them: arrays (14, piano), hysteresis (15, drawer),
  interrupts (16, fast ball), active-LOW (17, relay), I2C addresses (24), menus (25).
- **Phone control early (Ep 12),** right after one easy sensor episode, so the hook comes before viewers drift. AP mode
  first (no router password, works on iPhone and Android, no app). Station mode + internet only later (26–28), when
  there is a reason (time, push).
- **Milestones replace recaps:** 18 (end of kit), 21 (first two bought parts), 25 (game parts), 29–30 (final). Each is
  a combination of known parts = spaced review in project form, at most 1 milestone per 3–4 episodes.
- **Kit first, purchases from 19:** viewers can follow 10–18 with the kit alone; ordering time for the buy list.
- **Calendar (if Ep 10 = Fri 27 Nov, Tue + Fri 17:00):** 11 Tue 1 Dec · 12 Fri 4 Dec · 13 8 Dec · 14 11 Dec ·
  15 15 Dec · 16 18 Dec · 17 22 Dec · 18 25 Dec · 19 29 Dec · 20 Fri 1 Jan · 21 5 Jan · 22 8 Jan · 23 12 Jan ·
  24 15 Jan · 25 19 Jan · 26 22 Jan · 27 26 Jan · 28 29 Jan · 29 Tue 2 Feb · 30 Fri 5 Feb. Shorts as now: TR next day
  17:00, EN the day after 22:00. **Buy list must arrive by ~15 Dec** (script/test of Ep 19).

---

## 4. Pin plan proposal (v7)

Rule kept: a part keeps its pin for the whole season. New: the LED trio is retired after Ep 9, and its pins become
module pins.

| GPIO | Part | From ep | Notes |
|---|---|---|---|
| 19 | Button (`INPUT_PULLUP`) | 10 | Moves 22 → 19 in **Ep 10** (was 17 in v6) |
| 21 / 22 | I2C SDA / SCL: OLED (0x3C) | 10 | MPU6050 (0x68) joins the same two wires in 24 |
| 32 | Passive buzzer | 10 | Active buzzer only swapped in for the 15 s comparison in 11 |
| 25 / 26 / 27 | RGB LED | 06 | Kept: phone color remote (12), comfort color, status |
| 33 | PIR `OUT` | 11 | |
| 4 | DHT11 data | 13 | ADC2 pin but digital use: fine with Wi-Fi |
| 14 | Touch pad 1 (T6) | 14 | |
| 2 | Touch pad 2 (T2) | 14 | Strapping pin + on-board LED; touch only (nothing drives it). Free again after 14 |
| 15 | Touch pad 3 (T3) in 14 → **HC-SR04 TRIG** | 20 | Strapping: an output is safe; LOW at boot only silences the boot log |
| 35 | LDR `AO` | 15 | Input-only, ADC1 |
| 13 | IR obstacle `OUT` | 16 | Interrupt pin |
| 16 / 17 | Relay `IN1` / `IN2` (active-LOW, module on 5 V) | 17 | Relay 1 = fan/lamp, relay 2 = pump (28). 17 was the green LED |
| 18 | Servo signal (servo power from VIN 5 V) | 19 | Was the yellow LED |
| 5 | **HC-SR04 ECHO** (1 kΩ + 2 kΩ divider, or 3.3 V module) | 20 | Strapping (SDIO timing only); idle LOW is harmless for normal boot |
| 23 | WS2812B ring `DIN` (ring power 5 V, brightness ≤ 40) | 22 | Was the red LED. 3.3 V data usually fine for 12 LEDs; 330 Ω series resistor recommended |
| 34 | Potentiometer → **joystick VRx** | 23 | Input-only, ADC1. The pot retires in 23: "a joystick is two knobs" |
| 39 (VN) | Joystick VRy | 23 | Input-only, ADC1. Joystick SW not wired: the button on 19 does that job |
| 36 (VP) | Soil moisture `AO` | 28 | Input-only, ADC1 |
| 12 | **unused** | — | MTDI: HIGH at boot selects 1.8 V flash → board won't boot |

**Conflicts / flags**
- **Input-only 34–39:** used only for analog inputs (pot/joystick, LDR, soil). Joystick SW cannot go there (no
  internal pull-up) → not wired; it is also why no button or pull-up sensor moves onto 36/39.
- **ADC2 + Wi-Fi:** every analog read is on ADC1 (34, 35, 36, 39), so Wi-Fi episodes (12, 13, 17, 18, 22, 26–30)
  keep all sensors. Touch pins (14/2/15) and digital DHT on 4 work with Wi-Fi on.
- **Boot pins:** v6 used none; v7 uses 2 (touch, Ep 14 only), 5 (echo) and 15 (trig) in boot-safe roles. Lesson
  folders say: "if upload fails, unplug the module on 2/5/15 and retry".
- **5 V power:** servo + ring + relay coils + pump all hang on USB 5 V. Brownout resets are the common mistake in 19
  (servo jerk) and 28 (pump); fix = capacitor / separate 5 V supply / lower ring brightness.
- **I2C:** OLED 0x3C and MPU6050 0x68 never clash; no pin cost for the MPU.
- **projects/07 gimbal maze** uses joystick 34/35 and servos 18/19 (19 = button, 35 = LDR in v7). It stays a
  standalone build; if it ever becomes an episode: joystick 34/39, servos 18 + one free pin.
- **No pin left for RC522 RFID** (SCK/MOSI/MISO/SS) without retiring the RGB LED or the touch/ultrasonic pins: one
  more reason to keep it for Season 2.

---

## 5. Recap 2 — recommendation

State: script + narration in 5 languages done (7:48, 41 segments), not rendered. Its content traces PWM, `map()` and
the **old LED version** of Ep 10, as a quiz/trace recap.

Recommendation: **do not publish Recap 2 as a video.** (1) §12.5 allows a recap only as an ≤ 8 min mini *project*;
Recap 2 is a trace/quiz review (Recap 1: 20:33 → 177 views). (2) Its Ep 10 part describes the LED reflex game that
v7 replaces with Reflex Game 2.0. (3) The slot is better spent getting new parts on screen sooner.
Salvage the work: the 7 quiz questions + 3 traces go to the learning site (Unit 2 review page); the PWM and `map()`
trace scenes become two "45 s how it works" Shorts. No Recap 3/4: milestones 18, 21, 25 take that role.
The old narrated Ep 10 (LED version) is shelved the same way; its false-start idea stays as the Ep 10 2.0 challenge.

---

## 6. Open questions for the creator (max 4)

1. **Order + money:** is the 7-part buy list (~12–15 USD) OK, and can it be ordered by ~1 Dec so Ep 19 (29 Dec) is
   safe? Since nothing is filmed: will the sketches be tested on your real board, or is compile + Wokwi simulation
   enough for the bought modules?
2. **Code on screen:** OK to drop guideline §7 ("full code on screen") for v7 — only the 3–8 key lines on screen, full
   sketch in the lesson folder / learning site?
3. **Phone control at Ep 12** — fine, or even earlier as Ep 11 (straight after the reflex game)?
4. **Ep 10 2.0 date:** Fri 27 Nov (calendar above) or Tue 24 Nov (the old Recap 2 slot)?
