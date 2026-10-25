// ESP32 From Zero - Episode 5: one button, four color modes
// RGB LED on GPIO 25/26/27 (see rgb_colors), button on GPIO 22.
// Each press moves to the next mode: 0 red, 1 green, 2 blue, 3 slow color fade. Nothing ever waits.

const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int BUTTON_PIN = 22;
const bool COMMON_ANODE = false;

int mode = 0;                  // 0..3
int level = 0;                 // for the fade in mode 3: 0..255
int step = 1;
unsigned long lastStep = 0;

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
      mode = mode + 1;
      if (mode > 3) {
        mode = 0;              // after the last mode, start again
      }
      Serial.print("mode ");
      Serial.println(mode);
    }
  }

  if (mode == 0) {
    setColor(255, 0, 0);
  } else if (mode == 1) {
    setColor(0, 255, 0);
  } else if (mode == 2) {
    setColor(0, 0, 255);
  } else {
    // mode 3: fade from blue to red and back, one step every 8 ms
    if (now - lastStep >= 8) {
      lastStep = now;
      level = level + step;
      if (level >= 255) {
        level = 255;
        step = -1;
      }
      if (level <= 0) {
        level = 0;
        step = 1;
      }
    }
    setColor(level, 0, 255 - level);
  }
}
