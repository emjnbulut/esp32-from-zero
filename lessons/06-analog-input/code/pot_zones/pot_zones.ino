// ESP32 From Zero - Episode 6: three zones
// Potentiometer on GPIO 34, red LED on GPIO 23.
// What it does: the knob has three zones. Left third: the LED is dim. Middle third: medium. Right third: full.
// The numbers 1365 and 2730 cut 0 .. 4095 into three equal parts.

const int POT_PIN = 34;        // the knob
const int LED_PIN = 23;        // the red LED

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(POT_PIN);     // the knob: 0 .. 4095

  if (value < 1365) {                  // left third
    analogWrite(LED_PIN, 20);          // dim
  } else if (value < 2730) {           // middle third
    analogWrite(LED_PIN, 120);         // medium
  } else {                             // right third
    analogWrite(LED_PIN, 255);         // full
  }

  Serial.println(value);
  delay(20);
}
