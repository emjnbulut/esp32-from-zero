// ESP32 From Zero - Episode 7 challenge (one solution): Reflex Tester with anti-cheat
// Lights: red GPIO 23, yellow GPIO 18, green GPIO 17. Result: RGB LED (25 / 26 / 27).
// Button on GPIO 22, potentiometer on GPIO 34 (sets how long yellow waits: 1 .. 4 s).
// What it does: press to start. Red, then yellow, then GREEN: press as fast as you can.
// Your time is printed and shown in color: green < 250 ms, yellow < 500 ms, otherwise red.
// The best time is saved with Preferences (the ESP32's own small memory that keeps values
// when the power is off), so the record is still there after unplugging the board.
// The catch: a press while still red or yellow is a FALSE START: the RGB flashes red for 2 s, no time counts.

#include <Preferences.h>

const int RED_PIN = 23;
const int YELLOW_PIN = 18;
const int GREEN_PIN = 17;
const int RGB_R = 25;
const int RGB_G = 26;
const int RGB_B = 27;
const int BUTTON_PIN = 22;
const int POT_PIN = 34;

Preferences prefs;
unsigned long best = 9999;     // the record in ms (9999 = no record yet)

int state = 0;                 // 0 wait, 1 red, 2 yellow, 3 green (go!), 4 result, 5 false start
bool flashOn = false;
unsigned long lastFlash = 0;
unsigned long stateStart = 0;
unsigned long waitTime = 2000; // yellow time, from the knob
int lastState = HIGH;
unsigned long lastChange = 0;

void setColor(int r, int g, int b) {
  analogWrite(RGB_R, r);
  analogWrite(RGB_G, g);
  analogWrite(RGB_B, b);
}

void lights(int red, int yellow, int green) {
  digitalWrite(RED_PIN, red == 1 ? HIGH : LOW);
  digitalWrite(YELLOW_PIN, yellow == 1 ? HIGH : LOW);
  digitalWrite(GREEN_PIN, green == 1 ? HIGH : LOW);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(RGB_R, OUTPUT);
  pinMode(RGB_G, OUTPUT);
  pinMode(RGB_B, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);

  prefs.begin("reflex", false);              // open our little drawer called "reflex"
  best = prefs.getULong("best", 9999);       // read the record (9999 if there is none yet)
  Serial.print("record: ");
  Serial.println(best);
  setColor(0, 0, 40);                        // dim blue: press to start
}

void loop() {
  unsigned long now = millis();
  unsigned long inState = now - stateStart;

  // the button: true only at the moment of a new press
  bool pressed = false;
  int b = digitalRead(BUTTON_PIN);
  if (b != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = b;
    if (b == LOW) {
      pressed = true;
    }
  }

  if (state == 0) {                                  // waiting for a start press
    if (pressed) {
      setColor(0, 0, 0);
      lights(1, 0, 0);
      state = 1;
      stateStart = now;
    }
  } else if ((state == 1 || state == 2) && pressed) { // pressed too early: false start
    Serial.println("FALSE START!");
    lights(0, 0, 0);
    state = 5;
    stateStart = now;
  } else if (state == 1) {                           // red for 1 s
    if (inState >= 1000) {
      lights(0, 1, 0);
      waitTime = map(analogRead(POT_PIN), 0, 4095, 1000, 4000);
      state = 2;
      stateStart = now;
    }
  } else if (state == 2) {                           // yellow, for waitTime
    if (inState >= waitTime) {
      lights(0, 0, 1);                               // GO!
      state = 3;
      stateStart = now;
    }
  } else if (state == 3) {                           // green: measure the reaction
    if (pressed) {
      unsigned long reaction = inState;              // time since green came on
      Serial.print("reaction: ");
      Serial.print(reaction);
      Serial.println(" ms");
      if (reaction < 250) {
        setColor(0, 255, 0);
      } else if (reaction < 500) {
        setColor(255, 160, 0);
      } else {
        setColor(255, 0, 0);
      }
      if (reaction < best) {                         // a new record: save it
        best = reaction;
        prefs.putULong("best", best);
        Serial.println("new record!");
      }
      lights(0, 0, 0);
      state = 4;
      stateStart = now;
    }
  } else if (state == 4) {                          // show the result for 3 s
    if (inState >= 3000) {
      setColor(0, 0, 40);
      state = 0;
    }
  } else {                                           // state 5: flash red for 2 s
    if (now - lastFlash >= 150) {
      lastFlash = now;
      flashOn = !flashOn;
      setColor(flashOn ? 255 : 0, 0, 0);
    }
    if (inState >= 2000) {
      setColor(0, 0, 40);
      state = 0;
    }
  }
}
