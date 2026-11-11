// ESP32 From Zero - Episode 9 (mini project 1), your turn: slow walker mode (one possible solution)
// Same as crossing, plus: hold the request button for more than 1 s and the walk light stays green twice as long.
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

int state = 0;                 // the step: 0 cars green, 1 cars yellow, 2 walk, 3 walk blinking
unsigned long stateStart = 0;  // when the current step began (ms)
bool request = false;          // somebody pressed the button and waits
unsigned long pressStart = 0;  // the parking ticket: when the button went down
unsigned long walkTime = 4000; // how long step 2 lasts: 4 s, or 8 s for a slow walker

int lastButton = HIGH;         // the button, as in episode 4
unsigned long lastChange = 0;
bool blinkOn = true;
unsigned long lastBlink = 0;

// helper 1: set all five lights in one call (HIGH = on, LOW = off)
void lights(int red, int yellow, int green, int walkRed, int walkGreen) {
  digitalWrite(CAR_RED, red);
  digitalWrite(CAR_YELLOW, yellow);
  digitalWrite(CAR_GREEN, green);
  digitalWrite(WALK_RED, walkRed);
  digitalWrite(WALK_GREEN, walkGreen);
}

// helper 2: move to a new step = new number in state + write down the time
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

  // PART 1 - the button: a new press while the cars have green is a request to cross
  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW && state == 0) {
      request = true;
      pressStart = now;
      walkTime = 4000;
      Serial.println("request");
    }
    if (b == HIGH && request && now - pressStart >= 1000) {   // released after a long hold
      walkTime = 8000;
      Serial.println("slow walker: 8 s");
    }
  }

  // PART 2 - the steps
  unsigned long inState = now - stateStart;              // how long we have been in this step
  unsigned long greenTime = map(analogRead(POT_PIN), 0, 4095, 3000, 10000);

  if (state == 0) {                                       // step 0: cars green, pedestrians wait
    lights(LOW, LOW, HIGH, HIGH, LOW);
    if (request && inState >= greenTime) {
      goTo(1, now);
    }
  } else if (state == 1) {                                // step 1: cars yellow for 2 s
    lights(LOW, HIGH, LOW, HIGH, LOW);
    if (inState >= 2000) {
      request = false;
      goTo(2, now);
    }
  } else if (state == 2) {                                // step 2: cars red, pedestrians walk for walkTime
    lights(HIGH, LOW, LOW, LOW, HIGH);
    if (inState >= walkTime) {
      goTo(3, now);
    }
  } else {                                                // step 3: the walk light blinks for 2 s
    if (now - lastBlink >= 250) {
      lastBlink = now;
      blinkOn = !blinkOn;
    }
    lights(HIGH, LOW, LOW, LOW, blinkOn ? HIGH : LOW);
    if (inState >= 2000) {
      goTo(0, now);
    }
  }
}
