// ESP32 From Zero - Episode 6 challenge (one solution): Rotary Safe Lock
// Potentiometer on GPIO 34, button on GPIO 22, RGB LED on GPIO 25 (red) / 26 (green) / 27 (blue).
// What it does: the knob dials a number 0 .. 99 (printed on the Serial Monitor). Dial 25, press;
// dial 70, press; dial 40, press: the safe opens (RGB green). A wrong number flashes red and starts over.
// Each target accepts +-3 (for example 22 .. 28), because a knob is never exact.

const int POT_PIN = 34;
const int BUTTON_PIN = 22;
const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const bool COMMON_ANODE = false;

int step = 0;                  // how many numbers were right so far: 0, 1, 2 (3 = open)
int lastState = HIGH;          // the button, as in episode 4
unsigned long lastChange = 0;
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

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
  setColor(0, 0, 40);          // dim blue: locked
}

void loop() {
  unsigned long now = millis();
  int number = map(analogRead(POT_PIN), 0, 4095, 0, 99);

  if (now - lastPrint >= 200) {          // show the dial 5 times a second
    lastPrint = now;
    Serial.println(number);
  }

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {                  // a new press: check the number for this step
      int target = 25;
      if (step == 1) {
        target = 70;
      } else if (step == 2) {
        target = 40;
      }
      if (number >= target - 3 && number <= target + 3) {
        step = step + 1;
        Serial.print("ok, step ");
        Serial.println(step);
        if (step == 3) {
          setColor(0, 255, 0);           // open!
          Serial.println("OPEN");
        }
      } else {
        step = 0;                        // wrong: flash red, start over
        setColor(255, 0, 0);
        delay(400);                      // a short flash is fine here: nothing else to watch
        setColor(0, 0, 40);
        Serial.println("wrong, start again");
      }
    }
  }
}
