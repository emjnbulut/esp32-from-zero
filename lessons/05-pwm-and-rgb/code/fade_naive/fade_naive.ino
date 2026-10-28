// ESP32 From Zero - Episode 5: the naive fade (it breathes, but it does not listen)
// Red LED on GPIO 23, button on GPIO 22 (internal pull-up, from episode 4).
// What it does: fades the LED up and down with two for loops and a short delay() on every step.
// A press is SUPPOSED to pause the fade, but the button is only read between two whole fades
// (once every 2 seconds), so almost every press is missed. Compare it with fade_millis.

const int LED_PIN = 23;
const int BUTTON_PIN = 22;

bool fading = true;            // true = the LED breathes, false = paused

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // HIGH when not pressed, LOW when pressed
}

void loop() {
  // the button is checked only here: once per full fade
  if (digitalRead(BUTTON_PIN) == LOW) {
    fading = !fading;
    delay(300);                // a crude way to skip the bounce
  }

  if (fading) {
    for (int b = 0; b <= 255; b++) {   // up: 256 steps x 4 ms = about 1 second
      analogWrite(LED_PIN, b);
      delay(4);                        // while this waits, nobody looks at the button
    }
    for (int b = 255; b >= 0; b--) {   // down: about 1 more second
      analogWrite(LED_PIN, b);
      delay(4);
    }
  }
}
