// ESP32 From Zero - Episode 4: Read a button
// GPIO 22 -> button -> GND (internal pull-up), LED on GPIO 23

const int BUTTON_PIN = 22;     // the button pulls this pin to GND
const int LED_PIN = 23;        // our LED from episode 3

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP); // HIGH until pressed
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int state = digitalRead(BUTTON_PIN); // HIGH or LOW
  Serial.println(state);

  if (state == LOW) {          // pressed: pulled to GND
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(50);
}
