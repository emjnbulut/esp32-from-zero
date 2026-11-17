// Pin by Pin Lab - extra project 05: Treasure Detector
// Needs episodes 1-8. The course circuit: knob (potentiometer) on GPIO 34, button on GPIO 22,
// RGB LED on GPIO 25 (red) / 26 (green) / 27 (blue), red LED on GPIO 23.
//
// A treasure is hidden somewhere on the knob (a number 0 .. 99). Turn the knob to search:
//   far away  -> the RGB LED glows cold blue, the red LED "beeps" slowly
//   closer    -> the color warms up to red, and the red LED beeps faster, like a metal detector
// Standing on it? Press the button: a rainbow party, and the treasure hides somewhere new.
// Press in the wrong place: a short blue "nothing here" blink.

const int POT_PIN = 34;
const int BUTTON_PIN = 22;
const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int BEEP_PIN = 23;       // the red LED is our "beeper"
const bool COMMON_ANODE = false;

int secret = 63;               // where the treasure is hidden (0 .. 99)
int lastState = HIGH;          // the button, as in episode 4
unsigned long lastChange = 0;
unsigned long lastBeep = 0;
bool beepOn = false;
unsigned long lastPrint = 0;

void setColor(int r, int g, int b) {
  if (COMMON_ANODE) {
    r = 255 - r;
    g = 255 - g;
    b = 255 - b;
  }
  analogWrite(RED_PIN, r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

void party() {                 // treasure found: a quick rainbow, then a new hiding place
  for (int round = 0; round < 3; round++) {
    setColor(255, 0, 0);   delay(90);
    setColor(255, 120, 0); delay(90);
    setColor(255, 255, 0); delay(90);
    setColor(0, 255, 0);   delay(90);
    setColor(0, 120, 255); delay(90);
    setColor(150, 0, 255); delay(90);
  }
  secret = secret + 37;        // hide it somewhere else
  if (secret > 99) {
    secret = secret - 100;
  }
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(BEEP_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();
  int number = map(analogRead(POT_PIN), 0, 4095, 0, 99);

  int distance = number - secret;        // how far from the treasure?
  if (distance < 0) {
    distance = -distance;                // only the size counts, not the direction
  }
  if (distance > 50) {
    distance = 50;
  }

  int heat = map(distance, 0, 50, 255, 0);       // 255 = right on it, 0 = far away
  setColor(heat, 0, 255 - heat);                  // cold blue ... hot red

  int beepEvery = map(distance, 0, 50, 40, 700);  // close = fast beeps, like a metal detector
  if (now - lastBeep >= beepEvery) {
    lastBeep = now;
    beepOn = !beepOn;
    digitalWrite(BEEP_PIN, beepOn);
  }

  if (now - lastPrint >= 200) {          // the dial on the Serial Monitor, 5 times a second
    lastPrint = now;
    Serial.println(number);
  }

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {                  // a new press: dig here!
      if (distance <= 2) {
        Serial.println("TREASURE FOUND!");
        party();
      } else {
        setColor(0, 0, 0);   delay(120); // nothing here: a short blink
        setColor(0, 0, 255); delay(120);
      }
    }
  }
}
