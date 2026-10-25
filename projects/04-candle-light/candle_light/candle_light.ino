// Pin by Pin Lab project 04: electric candle
// Uses only episodes 1-5: analogWrite, setColor(), millis(), button + edge + debounce, plain C arithmetic.
// RGB LED on GPIO 25/26/27 (episode 5), button on GPIO 22. A press blows the candle out / lights it.
// The flicker comes from a tiny number generator: next = next * 109 + 89 (no library needed).

const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int BUTTON_PIN = 22;
const bool COMMON_ANODE = false;

bool lit = true;
unsigned long seed = 12345;
unsigned long lastFlicker = 0;
unsigned long wait = 80;

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
}

void loop() {
  unsigned long now = millis();

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {
      lit = !lit;
      if (!lit) {
        setColor(0, 0, 0);
      }
    }
  }

  if (lit && now - lastFlicker >= wait) {
    lastFlicker = now;
    seed = seed * 109 + 89;                  // a new "random" number every flicker
    int flame = 150 + seed % 106;            // brightness 150..255
    wait = 40 + (seed / 7) % 110;            // next flicker in 40..149 ms
    setColor(flame, flame * 30 / 100, 0);    // candle orange: a little green, no blue
  }
}
