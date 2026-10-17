// ESP32 From Zero - Episode 4: two LEDs at their own speed + a button, nothing waits
// red LED on GPIO 23 (bottom half), green LED on GPIO 25 (top half), button on GPIO 22

const int BUTTON_PIN = 22;
const int RED_PIN = 23;        // switched on/off by the button
const int GREEN_PIN = 25;      // always blinking

bool redBlinking = true;
bool redOn = false, greenOn = false;
unsigned long lastRed = 0, lastGreen = 0;

int lastState = HIGH;
unsigned long lastChange = 0;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  // the button: a new press switches the red blinking on or off
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) redBlinking = !redBlinking;
  }

  // red: every 500 ms (only while blinking)
  if (redBlinking && now - lastRed >= 500) {
    lastRed = now;
    redOn = !redOn;
    digitalWrite(RED_PIN, redOn ? HIGH : LOW);
  }
  if (!redBlinking && redOn) {
    redOn = false;
    digitalWrite(RED_PIN, LOW);
  }

  // green: every 150 ms, always
  if (now - lastGreen >= 150) {
    lastGreen = now;
    greenOn = !greenOn;
    digitalWrite(GREEN_PIN, greenOn ? HIGH : LOW);
  }
}
