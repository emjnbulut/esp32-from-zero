// ESP32 From Zero - Episode 4: toggle the LED with each press (with debounce)
// GPIO 22 -> button -> GND (internal pull-up), LED on GPIO 23

const int BUTTON_PIN = 22;
const int LED_PIN = 23;

int lastState = HIGH;          // the button is not pressed at the start
bool ledOn = false;
int presses = 0;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState) {    // the button changed
    if (state == LOW) {        // ...and it's now pressed: a new press
      presses++;
      ledOn = !ledOn;
      digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
      Serial.print("presses: ");
      Serial.println(presses);
    }
    delay(50);                 // debounce: wait until the contacts stop bouncing
  }
  lastState = state;
}
