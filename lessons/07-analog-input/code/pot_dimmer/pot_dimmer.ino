// ESP32 From Zero - Episode 7: the knob dims the LED
// Potentiometer on GPIO 34, red LED on GPIO 23 (episode 3 circuit).
// What it does: turn the knob and the LED gets brighter or dimmer, instantly.
// The knob gives 0 .. 4095, analogWrite wants 0 .. 255, so we divide by 16 (4095 / 16 is about 255).

const int POT_PIN = 34;        // the knob
const int LED_PIN = 23;        // the red LED

void setup() {
  pinMode(LED_PIN, OUTPUT);    // we drive the LED pin
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(POT_PIN);    // the knob: 0 .. 4095
  int brightness = value / 16;        // the same position, scaled to 0 .. 255
  analogWrite(LED_PIN, brightness);   // show it on the LED
  Serial.println(brightness);
  delay(20);
}
