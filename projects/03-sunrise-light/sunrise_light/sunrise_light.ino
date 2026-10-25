// Pin by Pin Lab project 03: sunrise light
// Uses only episodes 1-5: analogWrite, setColor(), millis(), button + edge + debounce.
// RGB LED on GPIO 25/26/27 (episode 5), button on GPIO 22.
// Press: a 60-second sunrise. Deep red, then orange, then warm white. Press again: off.

const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int BUTTON_PIN = 22;
const bool COMMON_ANODE = false;

const unsigned long HALF = 30000;  // 30 s red -> orange, 30 s orange -> warm white

bool rising = false;
unsigned long startTime = 0;

int lastState = HIGH;
unsigned long lastChange = 0;

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
  setColor(0, 0, 0);
}

void loop() {
  unsigned long now = millis();

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {
      rising = !rising;        // start the sunrise, or switch it off
      startTime = now;
      setColor(0, 0, 0);
    }
  }

  if (rising) {
    unsigned long t = now - startTime;
    if (t < HALF) {
      // first half: red rises 0 -> 255, a little green follows -> deep red to orange
      int r = t * 255 / HALF;
      setColor(r, r / 5, 0);
    } else if (t < 2 * HALF) {
      // second half: green and blue catch up -> warm white
      int k = (t - HALF) * 255 / HALF;
      setColor(255, 51 + k * 129 / 255, k * 80 / 255);
    } else {
      setColor(255, 180, 80);  // morning: warm white stays on
    }
  }
}
