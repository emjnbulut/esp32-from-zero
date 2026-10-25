// ESP32 From Zero - Episode 5 challenge (one solution): the smart camping headlamp
// RGB LED on GPIO 25/26/27, button on GPIO 22.
// Modes: 0 off, 1 dim white, 2 bright white, 3 red blink. A press goes to the next mode,
// BUT if the lamp has been on (any mode except 0) for 3 seconds or more, the next press switches it straight off.

const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int BUTTON_PIN = 22;
const bool COMMON_ANODE = false;

int mode = 0;
unsigned long lastPress = 0;   // when the mode last changed (ms)
bool redOn = false;
unsigned long lastBlink = 0;

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
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {
      if (mode != 0 && now - lastPress >= 3000) {
        mode = 0;              // on for 3 s or more: straight off
      } else {
        mode = mode + 1;
        if (mode > 3) {
          mode = 0;
        }
      }
      lastPress = now;
      Serial.print("mode ");
      Serial.println(mode);
    }
  }

  if (mode == 0) {
    setColor(0, 0, 0);
  } else if (mode == 1) {
    setColor(40, 40, 40);      // dim white
  } else if (mode == 2) {
    setColor(255, 255, 255);   // bright white
  } else {
    if (now - lastBlink >= 300) {
      lastBlink = now;
      redOn = !redOn;
    }
    setColor(redOn ? 255 : 0, 0, 0);
  }
}
