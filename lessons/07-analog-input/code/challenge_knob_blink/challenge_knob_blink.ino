// ESP32 From Zero - Episode 7 challenge (one solution): Knob Blink Speed
// Potentiometer on GPIO 34, red LED on GPIO 23.
// What it does: the red LED blinks all the time, and the knob picks how fast, in three zones:
// left third: every 100 ms (fast), middle third: every 400 ms, right third: every 1000 ms (slow).
// Nothing waits with delay(): the blink uses millis(), so the knob is read all the time.

const int POT_PIN = 34;        // the knob
const int LED_PIN = 23;        // the red LED

unsigned long lastBlink = 0;   // when the LED last changed (ms)
bool ledOn = false;            // is the LED on right now?
int interval = 400;            // how long between changes, picked by the knob

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();        // the clock

  // PART 1 - the knob picks the interval
  int value = analogRead(POT_PIN);
  if (value < 1365) {
    interval = 100;
  } else if (value < 2730) {
    interval = 400;
  } else {
    interval = 1000;
  }

  // PART 2 - the blink (same trick as episode 4)
  if (now - lastBlink >= interval) {
    lastBlink = now;
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
  }
}
