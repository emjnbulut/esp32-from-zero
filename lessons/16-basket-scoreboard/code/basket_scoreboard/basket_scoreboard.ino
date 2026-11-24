// ESP32 From Zero - Episode 16: I built a basketball scoreboard that counts every shot  [DRAFT 2026-11-24]
// An IR obstacle sensor under the rim of a paper-cup hoop sees every ball that drops through. A fast ball blocks the
// beam for only a few milliseconds, so instead of checking the pin in loop() (and maybe looking away at the wrong
// moment), we let the pin ring a doorbell: an INTERRUPT. The chip stops whatever it does, runs our tiny function,
// and goes back. Press the button: a 30-second round starts. The best score is kept in Preferences.
//
// Parts:
//   IR obstacle module OUT -> GPIO 13, VCC -> 3V3, GND -> GND   (OUT goes LOW when something is in front of it)
//   passive buzzer + -> GPIO 32, button GPIO 19 <-> GND, OLED SDA 21 / SCL 22   (Episode 10)
// Libraries: "Adafruit SSD1306" + "Adafruit GFX".

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Preferences.h>

const int IR_PIN = 13;
const int BUZZER_PIN = 32;
const int BUTTON_PIN = 19;
const unsigned long ROUND_MS = 30000;

Adafruit_SSD1306 screen(128, 64, &Wire, -1);
Preferences prefs;

// changed inside the interrupt -> "volatile": tells the compiler this value can change behind loop()'s back
volatile int baskets = 0;
volatile unsigned long lastHit = 0;

int best = 0;
bool playing = false;
unsigned long roundStart = 0;
int shown = -1;
unsigned long lastSecond = 99;
int lastButton = HIGH;
unsigned long lastChange = 0;

// the doorbell: runs the moment the beam is blocked. Keep it tiny: count, remember the time, done.
// IRAM_ATTR = "keep this function in the fast memory" - interrupt functions on the ESP32 need it.
void IRAM_ATTR ballSeen() {
  unsigned long t = millis();
  if (t - lastHit > 300) {     // one ball can flicker the sensor a few times: count it once
    baskets++;
    lastHit = t;
  }
}

void show(const char* top, String big) {   // same helper as Episode 10
  screen.clearDisplay();
  screen.setTextColor(SSD1306_WHITE);
  screen.setTextSize(1);
  screen.setCursor(0, 0);
  screen.print(top);
  screen.setTextSize(2);
  screen.setCursor(0, 28);
  screen.print(big);
  screen.display();
}

void setup() {
  pinMode(IR_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
  screen.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  prefs.begin("basket", false);
  best = prefs.getInt("best", 0);
  attachInterrupt(digitalPinToInterrupt(IR_PIN), ballSeen, FALLING);   // ring when OUT goes HIGH -> LOW
  show(("best: " + String(best)).c_str(), "PRESS");
}

void loop() {
  unsigned long now = millis();

  int b = digitalRead(BUTTON_PIN);           // button starts a round (Episode 4 edge)
  if (b != lastButton && now - lastChange > 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW && !playing) {
      baskets = 0;
      shown = -1;
      playing = true;
      roundStart = now;
      tone(BUZZER_PIN, 1500, 300);           // start whistle
    }
  }

  if (!playing) return;

  unsigned long left = (ROUND_MS - (now - roundStart) + 999) / 1000;
  int score = baskets;                        // copy once: the interrupt may change it any moment
  if (score != shown || left != lastSecond) { // redraw only when something changed
    if (score > shown && shown >= 0) tone(BUZZER_PIN, 2000, 80);   // a short "swish" beep per basket
    shown = score;
    lastSecond = left;
    show(("time " + String(left) + " s   best " + String(best)).c_str(), String(score) + " pts");
  }

  if (now - roundStart >= ROUND_MS) {         // the horn
    playing = false;
    tone(BUZZER_PIN, 400, 900);
    if (score > best) {
      best = score;
      prefs.putInt("best", best);             // only when it is a new record (Episode 10)
      show("NEW RECORD!", String(score) + " pts");
    } else {
      show(("best: " + String(best)).c_str(), String(score) + " pts");
    }
  }
}
