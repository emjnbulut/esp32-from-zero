// ESP32 From Zero - Episode 11: Motion Alarm (room guard)
// Parts: HC-SR501 PIR motion sensor, plus the Episode 10 circuit (OLED screen, button, passive buzzer).
//   PIR    OUT -> GPIO 33, VCC -> 5V (VIN), GND -> GND   (the OUT pin gives 3.3 V, safe for the ESP32)
//   OLED   SDA -> GPIO 21, SCL -> GPIO 22, VCC -> 3V3, GND -> GND
//   button GPIO 19 <-> GND (internal pull-up)
//   passive buzzer + -> GPIO 32, - -> GND
// How it works:
//   press the button   -> 10 s to leave the room (countdown on the screen), then the guard is ARMED
//   motion while armed -> siren + "INTRUDER!" on the screen, and we remember WHEN it happened
//   press the button   -> alarm off; the screen tells you how long ago someone was seen
// The PIR does the hard work: it only answers "yes, something warm moved" (HIGH) or "no" (LOW).
// Its two orange trim knobs set how long it stays HIGH (time) and how far it sees (sensitivity).
// Libraries (Library Manager): "Adafruit SSD1306" and "Adafruit GFX".

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int PIR_PIN = 33;
const int BUTTON_PIN = 19;
const int BUZZER_PIN = 32;

const unsigned long WARMUP_MS = 30000;   // the PIR needs ~30 s after power-on before it can be trusted
const unsigned long GRACE_MS = 10000;    // time to leave the room after arming
const unsigned long SIREN_MS = 15000;    // the siren stops by itself after 15 s

Adafruit_SSD1306 screen(128, 64, &Wire, -1);

// 0 = warming up, 1 = off (disarmed), 2 = leaving (countdown), 3 = armed, 4 = alarm!
int state = 0;
unsigned long stateStart = 0;
unsigned long lastMotion = 0;            // the moment the PIR last said "yes" (0 = never)
int caught = 0;                          // how many times the alarm went off

unsigned long lastDraw = 0;              // when the "off" screen was last redrawn
int lastButton = HIGH;
unsigned long lastChange = 0;

// one helper draws every screen: a small line on top, a big line in the middle (from Episode 10)
void show(const char* top, String big) {
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

void goTo(int newState, unsigned long now) {
  state = newState;
  stateStart = now;
}

// "3 min ago", "45 s ago" - turns a time span into words people read at a glance
String ago(unsigned long ms) {
  unsigned long s = ms / 1000;
  if (s < 60) return String(s) + " s ago";
  if (s < 3600) return String(s / 60) + " min ago";
  return String(s / 3600) + " h ago";
}

bool buttonPressed(unsigned long now) {   // true only at the moment of a new press (Episode 4 style)
  int b = digitalRead(BUTTON_PIN);
  bool pressed = false;
  if (b != lastButton && now - lastChange > 50) {
    lastChange = now;
    lastButton = b;
    pressed = (b == LOW);
  }
  return pressed;
}

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
  screen.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  show("motion alarm", "warming..");
}

void loop() {
  unsigned long now = millis();
  bool pressed = buttonPressed(now);
  bool motion = digitalRead(PIR_PIN) == HIGH;   // the whole sensor in one line
  unsigned long inState = now - stateStart;

  if (state == 0) {                              // warming up: ignore the PIR for 30 s
    if (now >= WARMUP_MS) {
      show("press to arm", "READY");
      goTo(1, now);
    }
  } else if (state == 1) {                       // off: show when someone was last seen
    if (pressed) {
      goTo(2, now);
    } else if (now - lastDraw >= 1000) {         // refresh the "last seen" screen once a second
      lastDraw = now;
      if (lastMotion == 0) show("press to arm", "READY");
      else show(("seen " + String(caught) + "x, last:").c_str(), ago(now - lastMotion));
    }
  } else if (state == 2) {                       // leaving: 10 s countdown, a short tick every second
    unsigned long left = (GRACE_MS - inState + 999) / 1000;
    static unsigned long lastTick = 99;
    if (left != lastTick) {
      lastTick = left;
      show("leave the room!", String(left) + " s");
      tone(BUZZER_PIN, 2000, 30);
    }
    if (pressed) {                               // changed your mind
      show("press to arm", "OFF");
      goTo(1, now);
    } else if (inState >= GRACE_MS) {
      lastTick = 99;
      show("guarding...", "ARMED");
      goTo(3, now);
    }
  } else if (state == 3) {                       // armed: wait for the PIR to say yes
    if (motion) {
      lastMotion = now;
      caught++;
      show("motion detected!", "INTRUDER");
      goTo(4, now);
    } else if (pressed) {
      show("press to arm", "OFF");
      goTo(1, now);
    }
  } else if (state == 4) {                       // alarm: a two-tone siren until the button or 15 s
    if (motion) lastMotion = now;                // keep the "last seen" time fresh
    tone(BUZZER_PIN, (inState / 250) % 2 ? 2600 : 1800);   // switch the note every quarter second
    if (pressed || inState >= SIREN_MS) {
      noTone(BUZZER_PIN);
      show(("seen " + String(caught) + "x, last:").c_str(), ago(now - lastMotion));
      goTo(1, now);
    }
  }
}
