// ESP32 From Zero - Episode 5: PWM levels
// Red LED on GPIO 23 (episode 3 circuit). analogWrite(pin, 0..255) sets the brightness.
// Steps 0% -> 25% -> 50% -> 100%, two seconds each (a multimeter on the LED pin shows the average voltage).

const int LED_PIN = 23;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void showLevel(int value) {
  analogWrite(LED_PIN, value);  // 0 = always off, 255 = always on
  Serial.print("analogWrite ");
  Serial.print(value);
  Serial.print(" = ");
  Serial.print(value * 100 / 255);
  Serial.println("% on");
  delay(2000);
}

void loop() {
  showLevel(0);
  showLevel(64);    // 25%
  showLevel(128);   // 50%
  showLevel(255);   // 100%
}
