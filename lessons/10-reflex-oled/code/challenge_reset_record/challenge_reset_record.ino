// ESP32 From Zero - Episode 10 challenge solution: hold the button for 3 seconds to erase the record
// Same circuit as reflex_oled. New: in the "ready" step, measure how long the button is held
// (pressStart, as in episode 9). Held 3 s or more -> put 9999 back in the drawer.

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Preferences.h>

const int BUTTON_PIN = 19;
const int BUZZER_PIN = 32;

Adafruit_SSD1306 screen(128, 64, &Wire, -1);
Preferences prefs;

unsigned long best = 9999;
unsigned long waitTime = 0;
int state = 0;
unsigned long stateStart = 0;

int lastButton = HIGH;
unsigned long lastChange = 0;
unsigned long pressStart = 0;   // when the current press began (episode 9)
bool erased = false;            // so one long press erases only once

void show(const char* top, String big) {
  screen.clearDisplay();
  screen.setTextColor(SSD1306_WHITE);
  screen.setTextSize(1);
  screen.setCursor(0, 0);
  screen.print(top);
  screen.setTextSize(3);
  screen.setCursor(0, 28);
  screen.print(big);
  screen.display();
}

void goTo(int newState, unsigned long now) {
  state = newState;
  stateStart = now;
}

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
  screen.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  prefs.begin("reflex", false);
  best = prefs.getULong("best", 9999);
  show("REFLEX 2.0  best:", String(best) + "ms");
}

void loop() {
  unsigned long now = millis();

  bool pressed = false;
  bool released = false;
  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW) {
      pressed = true;
      pressStart = now;
    } else {
      released = true;
    }
  }

  unsigned long inState = now - stateStart;

  if (state == 0) {
    // NEW: still holding after 3 s? erase the record once
    if (lastButton == LOW && !erased && now - pressStart >= 3000) {
      best = 9999;
      prefs.putULong("best", best);
      erased = true;
      show("record erased", "----");
      tone(BUZZER_PIN, 600, 500);
    }
    // the game starts when a SHORT press is released
    if (released) {
      if (erased) {
        erased = false;
        show("REFLEX 2.0  best:", String(best) + "ms");
      } else {
        waitTime = random(1500, 4000);
        show("get ready...", "WAIT");
        goTo(1, now);
      }
    }
  } else if (state == 1) {
    if (pressed) {
      show("false start", "OOPS");
      tone(BUZZER_PIN, 200, 400);
      goTo(3, now);
    } else if (inState >= waitTime) {
      show("", " GO!");
      tone(BUZZER_PIN, 1500, 150);
      goTo(2, now);
    }
  } else if (state == 2) {
    if (pressed) {
      unsigned long reaction = inState;
      Serial.println(reaction);
      if (reaction < best) {
        best = reaction;
        prefs.putULong("best", best);
        show("NEW RECORD!", String(reaction) + "ms");
        tone(BUZZER_PIN, 2000, 300);
      } else {
        show("your time", String(reaction) + "ms");
      }
      goTo(3, now);
    }
  } else if (state == 3) {
    if (inState >= 2000 && lastButton == HIGH) {
      show("REFLEX 2.0  best:", String(best) + "ms");
      goTo(0, now);
    }
  }
}
