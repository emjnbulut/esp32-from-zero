// ESP32 From Zero - Episode 5: a smooth fade that never waits
// Red LED on GPIO 23, button on GPIO 22 (internal pull-up, from episode 4).
// The LED breathes up and down; a press pauses or resumes the fade at once.

const int LED_PIN = 23;
const int BUTTON_PIN = 22;

int brightness = 0;            // 0..255
int step = 1;                  // +1 going up, -1 going down
unsigned long lastStep = 0;    // when the brightness last changed (ms)
bool fading = true;

int lastState = HIGH;
unsigned long lastChange = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  // the button: a new press pauses or resumes the fade
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {
      fading = !fading;
    }
  }

  // the fade: one small step every 4 ms, 255 steps up = about one second
  if (fading && now - lastStep >= 4) {
    lastStep = now;
    brightness = brightness + step;
    if (brightness >= 255) {
      brightness = 255;
      step = -1;               // top reached: go down
    }
    if (brightness <= 0) {
      brightness = 0;
      step = 1;                // bottom reached: go up
    }
    analogWrite(LED_PIN, brightness);
    Serial.println(brightness);  // open Tools > Serial Plotter to see the fade as a triangle
  }
}
