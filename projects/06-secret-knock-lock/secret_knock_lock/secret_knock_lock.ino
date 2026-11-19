// Pin by Pin Lab - extra project 06: Secret Knock Lock
// Needs episodes 1-9. The course circuit from episodes 8-10, no new wire:
//   red LED 23 = "locked", yellow LED 18 = lights while you hold the button, green LED 17 = "open",
//   RGB LED 25 / 26 / 27 = the lock's mood, button on GPIO 22.
//
// Only one rhythm opens the lock: SHORT, SHORT, LONG.
// Every press is timed like a parking ticket (episode 9): under 250 ms is short, longer is long.
// One variable, step, counts how many beats were right so far (the state idea from episode 9).
//   right beat   -> the RGB LED shows the progress: blue, cyan, ...
//   wrong beat   -> red flashes for a second and the lock forgets everything
//   3 s of quiet -> the lock forgets too (you have to knock in one go)
//   whole rhythm -> OPEN: green LED, a rainbow, then it locks itself again after 2.5 s

const int RED_PIN = 23;
const int YELLOW_PIN = 18;
const int GREEN_PIN = 17;
const int RGB_R = 25;
const int RGB_G = 26;
const int RGB_B = 27;
const int BUTTON_PIN = 22;

const int SHORT = 0;
const int LONG = 1;
const unsigned long LONG_PRESS = 250;       // ms: shorter = SHORT, longer = LONG
const unsigned long FORGET = 3000;          // ms of quiet before the lock forgets

int step = 0;                  // how many beats were right so far (0 .. 3)
int lastButton = HIGH;         // the button, as in episode 4
unsigned long lastChange = 0;
unsigned long pressStart = 0;  // the parking ticket: when the press began
unsigned long lastKnock = 0;   // when the last beat ended

void setColor(int r, int g, int b) {
  analogWrite(RGB_R, r);
  analogWrite(RGB_G, g);
  analogWrite(RGB_B, b);
}

void showProgress() {          // the RGB LED tells how far you are
  if (step == 0) {
    setColor(0, 0, 40);        // dim blue: waiting
  } else if (step == 1) {
    setColor(0, 0, 255);       // blue: one right
  } else if (step == 2) {
    setColor(0, 200, 255);     // cyan: two right
  }
}

void wrong() {                 // wrong beat: flash red, forget everything
  for (int i = 0; i < 4; i++) {
    setColor(255, 0, 0);
    delay(120);
    setColor(0, 0, 0);
    delay(120);
  }
  step = 0;
  showProgress();
}

void unlock() {                // the whole rhythm was right
  digitalWrite(RED_PIN, LOW);
  digitalWrite(GREEN_PIN, HIGH);
  for (int round = 0; round < 3; round++) {
    setColor(255, 0, 0);   delay(90);
    setColor(255, 160, 0); delay(90);
    setColor(0, 255, 0);   delay(90);
    setColor(0, 120, 255); delay(90);
    setColor(150, 0, 255); delay(90);
  }
  setColor(0, 255, 0);
  delay(2500);                 // open for 2.5 s
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(RED_PIN, HIGH); // locked again
  step = 0;
  showProgress();
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
  digitalWrite(RED_PIN, HIGH); // locked
  showProgress();
}

void loop() {
  unsigned long now = millis();

  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW) {                          // pressed: stamp the ticket
      pressStart = now;
      digitalWrite(YELLOW_PIN, HIGH);
    } else {                                 // released: how long was it held?
      digitalWrite(YELLOW_PIN, LOW);
      unsigned long held = now - pressStart;
      int beat = SHORT;
      if (held >= LONG_PRESS) {
        beat = LONG;
      }
      Serial.print(held);
      if (beat == SHORT) {
        Serial.println(" ms: short");
      } else {
        Serial.println(" ms: long");
      }
      lastKnock = now;
      int want = SHORT;                      // the secret rhythm: SHORT, SHORT, LONG (try your own!)
      if (step == 2) {
        want = LONG;
      }
      if (beat == want) {                    // right beat: one step further
        step = step + 1;
        if (step == 3) {
          unlock();
        } else {
          showProgress();
        }
      } else {
        wrong();
      }
    }
  }

  // quiet for too long in the middle of a rhythm: forget it
  if (step > 0 && now - lastKnock >= FORGET) {
    step = 0;
    showProgress();
  }
}
