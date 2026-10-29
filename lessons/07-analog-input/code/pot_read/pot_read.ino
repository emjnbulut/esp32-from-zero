// ESP32 From Zero - Episode 7: read the knob
// Potentiometer middle leg on GPIO 34 (outer legs: 3V3 and GND).
// What it does: prints the knob's position (0 .. 4095) ten times a second. Turn the knob and watch the number.

const int POT_PIN = 34;        // the knob's middle leg

void setup() {
  Serial.begin(115200);        // so we can print to the Serial Monitor
}

void loop() {
  int value = analogRead(POT_PIN);  // 0 = knob at one end (0 V), 4095 = other end (3.3 V)
  Serial.println(value);            // show it
  delay(100);                       // ten readings a second
}
