// ESP32 From Zero - Episode 10 (mini project 1): reflex game with a record that survives a power cut
// Lights: red GPIO 23, yellow GPIO 18, green GPIO 17. Result: RGB LED (25 / 26 / 27).
// Button on GPIO 22, potentiometer on GPIO 34 (sets how long yellow waits: 1 .. 4 s).
// What it does: press to start. Red, then yellow, then GREEN: press as fast as you can.
// Your time is printed and shown in color: green < 250 ms, yellow < 500 ms, otherwise red.
// The best time is saved with Preferences (the ESP32's own small memory that keeps values
// when the power is off), so the record is still there after unplugging the board.
// Same pattern as the crossing in episode 9: state says which step we are in, millis() how long.

#include <Preferences.h>

const int RED_PIN = 23;
const int YELLOW_PIN = 18;
const int GREEN_PIN = 17;
const int RGB_R = 25;
const int RGB_G = 26;
const int RGB_B = 27;
const int BUTTON_PIN = 22;
const int POT_PIN = 34;

Preferences prefs;             // the ESP32's little drawer that keeps values without power
unsigned long best = 9999;     // the record in ms (9999 = no record yet)

int state = 0;                 // the step: 0 wait to start, 1 red, 2 yellow, 3 green (go!), 4 show the result
unsigned long stateStart = 0;  // when the current step began (ms)
unsigned long waitTime = 2000; // yellow time, from the knob

int lastButton = HIGH;         // the button, as in episode 4
unsigned long lastChange = 0;

// the RGB result light, as in episode 6
void setColor(int r, int g, int b) {
  analogWrite(RGB_R, r);
  analogWrite(RGB_G, g);
  analogWrite(RGB_B, b);
}

// helper 1: set the three lights in one call (HIGH = on, LOW = off)
void lights(int red, int yellow, int green) {
  digitalWrite(RED_PIN, red);
  digitalWrite(YELLOW_PIN, yellow);
  digitalWrite(GREEN_PIN, green);
}

// helper 2: move to a new step = new number in state + write down the time
void goTo(int newState, unsigned long now) {
  state = newState;
  stateStart = now;
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

  prefs.begin("reflex", false);              // open our drawer called "reflex"
  best = prefs.getULong("best", 9999);       // read the record (9999 if there is none yet)
  Serial.print("record: ");
  Serial.println(best);
  setColor(0, 0, 40);                        // dim blue: press to start
}

void loop() {
  unsigned long now = millis();

  // PART 1 - the button: pressed is true only at the moment of a new press
  bool pressed = false;
  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW) {
      pressed = true;
    }
  }

  // PART 2 - the steps
  unsigned long inState = now - stateStart;        // how long we have been in this step

  if (state == 0) {                                  // step 0: waiting for a start press
    if (pressed) {
      setColor(0, 0, 0);
      lights(HIGH, LOW, LOW);
      goTo(1, now);
    }
  } else if (state == 1) {                           // step 1: red for 1 s
    if (inState >= 1000) {
      lights(LOW, HIGH, LOW);
      waitTime = map(analogRead(POT_PIN), 0, 4095, 1000, 4000);
      goTo(2, now);
    }
  } else if (state == 2) {                           // step 2: yellow, for waitTime
    if (inState >= waitTime) {
      lights(LOW, LOW, HIGH);                        // GO!
      goTo(3, now);
    }
  } else if (state == 3) {                           // step 3: green, measure the reaction
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
      lights(LOW, LOW, LOW);
      goTo(4, now);
    }
  } else {                                           // step 4: show the result for 3 s
    if (inState >= 3000) {
      setColor(0, 0, 40);
      goTo(0, now);
    }
  }
}
