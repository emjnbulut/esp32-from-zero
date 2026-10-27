// ESP32 From Zero - Episode 6: a calmer reading (average of 4)
// Potentiometer on GPIO 34.
// What it does: prints two numbers: "raw" (one reading) and "avg" (the average of 4 readings).
// Open the Serial Plotter: the raw line jitters a little even when you do not touch the knob, the avg line is calmer.

const int POT_PIN = 34;        // the knob

void setup() {
  Serial.begin(115200);
}

void loop() {
  int raw = analogRead(POT_PIN);       // one reading: it jitters a little

  int sum = 0;                         // add up 4 readings...
  for (int i = 0; i < 4; i++) {
    sum = sum + analogRead(POT_PIN);
  }
  int avg = sum / 4;                   // ...and divide by 4: the average

  Serial.print("raw:");
  Serial.print(raw);
  Serial.print(",avg:");
  Serial.println(avg);
  delay(50);
}
