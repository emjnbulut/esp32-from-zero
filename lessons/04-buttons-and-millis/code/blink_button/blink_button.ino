// ESP32 From Zero - Episode 4: blink AND read a button at the same time
// GPIO 22 -> button -> GND (internal pull-up), LED on GPIO 23
// The button switches the blinking on and off. Nothing in loop() ever waits.

const int BUTTON_PIN = 22;
const int LED_PIN = 23;

bool blinking = true;
bool ledOn = false;
unsigned long lastBlink = 0;   // when the LED last changed (ms)

int lastState = HIGH;
unsigned long lastChange = 0;  // when the button last changed (ms)

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis(); // milliseconds since the board started

  // 1. the button: a new press switches blinking on or off
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) { // ignore the bounce
    lastChange = now;
    lastState = state;
    if (state == LOW) {
      blinking = !blinking;
      Serial.println(blinking ? "blinking" : "stopped");
    }
  }

  // 2. the LED: flip it every 500 ms, without waiting
  if (blinking && now - lastBlink >= 500) {
    lastBlink = now;
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
  }
  if (!blinking && ledOn) {    // stopped: make sure the LED is off
    ledOn = false;
    digitalWrite(LED_PIN, LOW);
  }
}
