// ESP32 From Zero - Episode 6: one button, four color modes
// RGB LED on GPIO 25/26/27 (see rgb_colors), button on GPIO 22.
// What it does: each press moves to the next mode: 0 red, 1 green, 2 blue, 3 a slow blue <-> red fade,
// then back to 0. The button always reacts at once, because nothing ever waits.

const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int BUTTON_PIN = 22;
const bool COMMON_ANODE = false;

int mode = 0;                  // which mode we are in: 0, 1, 2 or 3
int level = 0;                 // mode 3 only: the fade, 0 (all blue) .. 255 (all red)
int step = 1;                  // mode 3 only: +1 = towards red, -1 = back towards blue
unsigned long lastStep = 0;    // mode 3 only: the time of the last fade step (ms)

int lastState = HIGH;          // the button, as in episode 4
unsigned long lastChange = 0;

// the same helper as in rgb_colors: one line sets any color
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

  // PART 1 - the button: every new press goes to the next mode
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {        // a new press
      mode = mode + 1;         // next mode
      if (mode > 3) {
        mode = 0;              // after the last mode (3), start again at 0
      }
      Serial.print("mode ");
      Serial.println(mode);
    }
  }

  // PART 2 - the color for the current mode
  if (mode == 0) {
    setColor(255, 0, 0);       // red
  } else if (mode == 1) {
    setColor(0, 255, 0);       // green
  } else if (mode == 2) {
    setColor(0, 0, 255);       // blue
  } else {
    // mode 3: fade from blue to red and back, one step every 8 ms (like fade_millis)
    if (now - lastStep >= 8) {
      lastStep = now;
      level = level + step;
      if (level >= 255) {
        level = 255;
        step = -1;             // all red: turn back
      }
      if (level <= 0) {
        level = 0;
        step = 1;              // all blue: turn back
      }
    }
    setColor(level, 0, 255 - level);  // more red = less blue; together always 255
  }
}
