// ESP32 From Zero - Episode 6 (part 2): the dimmer with map()
// Potentiometer on GPIO 34, red LED on GPIO 23.
// What it does: the same dimmer as pot_dimmer, but map() does the scaling for us:
// it turns the knob's 0 .. 4095 into the LED's 0 .. 255.

const int POT_PIN = 34;        // the knob
const int LED_PIN = 23;        // the red LED

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(POT_PIN);                  // the knob: 0 .. 4095
  int brightness = map(value, 0, 4095, 0, 255);     // from range 0..4095 to range 0..255
  analogWrite(LED_PIN, brightness);
  Serial.println(brightness);
  delay(20);
}
