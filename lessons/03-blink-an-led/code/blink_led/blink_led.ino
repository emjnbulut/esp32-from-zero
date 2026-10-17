// ESP32 From Zero - Episode 3: Blink an LED
// GPIO 23 -> 220 ohm resistor -> LED -> GND

const int LED_PIN = 23;        // the GPIO our LED is wired to

void setup() {
  pinMode(LED_PIN, OUTPUT);    // our code drives this pin
  Serial.begin(115200);
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // 3.3 V -> LED on
  Serial.println("LED on");
  delay(500);                  // half a second

  digitalWrite(LED_PIN, LOW);  // 0 V -> LED off
  Serial.println("LED off");
  delay(500);
}
