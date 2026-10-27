// ESP32 From Zero - Episode 5: mix colors with an RGB LED
// RGB LED on the upper breadboard: red leg -> 220 ohm -> GPIO 25, green -> 220 ohm -> GPIO 26,
// blue -> 220 ohm -> GPIO 27, the longest (common) leg -> minus rail (GND).
// What it does: shows 8 colors, one per second: red, green, blue, yellow, magenta, cyan, white, orange.
// If the colors come out inverted (white when it should be off), your LED is common anode:
// move its long leg to 3V3 and set COMMON_ANODE to true.

const int RED_PIN = 25;        // one pin for each of the three tiny LEDs inside
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const bool COMMON_ANODE = false;  // false for most kits (long leg to GND)

// Our helper: one line sets any color. r, g, b = how bright red, green and blue are (0..255 each).
void setColor(int r, int g, int b) {
  if (COMMON_ANODE) {          // common anode works the other way round: 255 means off
    r = 255 - r;               // so we flip every value: 0 <-> 255
    g = 255 - g;
    b = 255 - b;
  }
  analogWrite(RED_PIN, r);     // PWM on each color's pin
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {
  //       red  green blue
  setColor(255,   0,   0); delay(1000);  // red
  setColor(  0, 255,   0); delay(1000);  // green
  setColor(  0,   0, 255); delay(1000);  // blue
  setColor(255, 255,   0); delay(1000);  // red + green = yellow
  setColor(255,   0, 255); delay(1000);  // red + blue = magenta
  setColor(  0, 255, 255); delay(1000);  // green + blue = cyan
  setColor(255, 255, 255); delay(1000);  // all three = white
  setColor(255,  40,   0); delay(1000);  // a little green in red = orange
}
