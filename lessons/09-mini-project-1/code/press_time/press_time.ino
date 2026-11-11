// ESP32 From Zero - Episode 9 (mini project 1): how long was the button held?
// Button on GPIO 22, yellow LED on GPIO 18.
// What it does: the yellow LED is on while you hold the button. When you let go, the Serial Monitor
// prints how long you held it, and whether that was a short press (< 250 ms) or a long one.
// The trick is a parking ticket: remember the time of the press (pressStart);
// at the release, now - pressStart is how long it was held.

const int BUTTON_PIN = 22;
const int LED_PIN = 18;

int lastButton = HIGH;
unsigned long lastChange = 0;
unsigned long pressStart = 0;  // when the button went down

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();
  int b = digitalRead(BUTTON_PIN);

  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW) {                        // pressed: stamp the ticket
      pressStart = now;
      digitalWrite(LED_PIN, HIGH);
    } else {                               // released: how long was it?
      digitalWrite(LED_PIN, LOW);
      unsigned long held = now - pressStart;
      Serial.print(held);
      Serial.print(" ms: ");
      if (held < 250) {
        Serial.println("short");
      } else {
        Serial.println("long");
      }
    }
  }
}
