// ESP32 From Zero - Episode 5: a smooth fade that never waits
// Red LED on GPIO 23, button on GPIO 22 (internal pull-up, from episode 4).
// What it does: the LED slowly gets brighter, then dimmer, again and again (it "breathes").
// A button press pauses the fade, the next press resumes it. Nothing ever waits with delay().

const int LED_PIN = 23;
const int BUTTON_PIN = 22;

// --- the fade ---
int brightness = 0;            // the LED's brightness right now: 0 (off) .. 255 (full)
int step = 1;                  // what we add every time: +1 = getting brighter, -1 = getting dimmer
unsigned long lastStep = 0;    // the time of the last step, in ms
bool fading = true;            // true = the LED breathes, false = paused

// --- the button (same as episode 4) ---
int lastState = HIGH;          // the button's reading last time round (HIGH = not pressed)
unsigned long lastChange = 0;  // when that reading last changed, to ignore the bounce

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // built-in pull-up: HIGH when not pressed, LOW when pressed
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();  // the clock: milliseconds since the board started

  // PART 1 - the button: a NEW press flips "fading" (pause <-> resume)
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {  // it changed, and it's not bounce
    lastChange = now;
    lastState = state;
    if (state == LOW) {        // the change was a press, not a release
      fading = !fading;        // true becomes false, false becomes true
    }
  }

  // PART 2 - the fade: every 4 ms, one small step (255 steps up = about 1 second)
  if (fading && now - lastStep >= 4) {
    lastStep = now;                    // remember when this step happened
    brightness = brightness + step;    // one step brighter (+1) or dimmer (-1)
    if (brightness >= 255) {           // reached the top?
      brightness = 255;
      step = -1;                       // from now on, go down
    }
    if (brightness <= 0) {             // reached the bottom?
      brightness = 0;
      step = 1;                        // from now on, go up
    }
    analogWrite(LED_PIN, brightness);  // show the new brightness on the LED
    Serial.println(brightness);        // Tools > Serial Plotter draws this as a triangle
  }
}
