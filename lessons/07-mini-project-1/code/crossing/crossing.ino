// ESP32 From Zero - Episode 7 (mini project 1): a smart pedestrian crossing
// Car lights: red GPIO 23, yellow GPIO 18, green GPIO 17. Pedestrian light: the RGB LED (red 25, green 26).
// Button on GPIO 22 (the pedestrian's "request" button), potentiometer on GPIO 34.
// What it does: cars have green. A press asks to cross. Once the cars had green long enough
// (3 .. 10 s, set with the knob), the light goes yellow, then red, and the pedestrian gets green;
// in the last 2 seconds the pedestrian green blinks. Then the cars get green again.
// One variable, state, says which step we are in; millis() says how long we have been in it.

const int CAR_RED = 23;
const int CAR_YELLOW = 18;
const int CAR_GREEN = 17;
const int WALK_RED = 25;       // RGB red leg
const int WALK_GREEN = 26;     // RGB green leg
const int BUTTON_PIN = 22;
const int POT_PIN = 34;

int state = 0;                 // 0 cars green, 1 cars yellow, 2 walk, 3 walk blinking
unsigned long stateStart = 0;  // when the current state began (ms)
bool request = false;          // somebody pressed the button and waits

int lastState = HIGH;          // the button, as in episode 4
unsigned long lastChange = 0;
bool blinkOn = true;
unsigned long lastBlink = 0;

// one helper sets all five lights: 1 = on, 0 = off
void lights(int red, int yellow, int green, int walkRed, int walkGreen) {
  digitalWrite(CAR_RED, red == 1 ? HIGH : LOW);
  digitalWrite(CAR_YELLOW, yellow == 1 ? HIGH : LOW);
  digitalWrite(CAR_GREEN, green == 1 ? HIGH : LOW);
  analogWrite(WALK_RED, walkRed == 1 ? 255 : 0);
  analogWrite(WALK_GREEN, walkGreen == 1 ? 255 : 0);
}

void goTo(int newState, unsigned long now) {
  state = newState;
  stateStart = now;
  Serial.print("state ");
  Serial.println(state);
}

void setup() {
  pinMode(CAR_RED, OUTPUT);
  pinMode(CAR_YELLOW, OUTPUT);
  pinMode(CAR_GREEN, OUTPUT);
  pinMode(WALK_RED, OUTPUT);
  pinMode(WALK_GREEN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  // PART 1 - the button: a new press is a request to cross
  int b = digitalRead(BUTTON_PIN);
  if (b != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = b;
    if (b == LOW && state == 0) {
      request = true;
      Serial.println("request");
    }
  }

  // PART 2 - the states
  unsigned long inState = now - stateStart;              // how long we have been in this state
  unsigned long greenTime = map(analogRead(POT_PIN), 0, 4095, 3000, 10000);

  if (state == 0) {                                       // cars green, pedestrians wait
    lights(0, 0, 1, 1, 0);
    if (request && inState >= greenTime) {
      goTo(1, now);
    }
  } else if (state == 1) {                                // cars yellow for 2 s
    lights(0, 1, 0, 1, 0);
    if (inState >= 2000) {
      request = false;
      goTo(2, now);
    }
  } else if (state == 2) {                                // cars red, pedestrians walk for 4 s
    lights(1, 0, 0, 0, 1);
    if (inState >= 4000) {
      goTo(3, now);
    }
  } else {                                                // state 3: walk light blinks for 2 s
    if (now - lastBlink >= 250) {
      lastBlink = now;
      blinkOn = !blinkOn;
    }
    lights(1, 0, 0, 0, blinkOn ? 1 : 0);
    if (inState >= 2000) {
      goTo(0, now);
    }
  }
}
