// ESP32 From Zero - Episode 5: PWM levels
// Red LED on GPIO 23 (episode 3 circuit). analogWrite(pin, 0..255) sets the brightness.
// What it does: the LED steps 0% -> 25% -> 50% -> 100%, two seconds each, and prints every step.
// (A multimeter on the LED pin shows the average voltage of each step.)

const int LED_PIN = 23;        // the red LED's pin

void setup() {
  pinMode(LED_PIN, OUTPUT);    // we drive this pin
  Serial.begin(115200);        // so we can print to the Serial Monitor
}

// Our own function. "value" is the number we hand it each time we call it (0..255).
// It sets the brightness, prints what it did, and holds that level for 2 seconds.
void showLevel(int value) {
  analogWrite(LED_PIN, value);       // 0 = always off, 255 = always on, in between = dimmer or brighter
  Serial.print("analogWrite ");
  Serial.print(value);
  Serial.print(" = ");
  Serial.print(value * 100 / 255);   // the same value as a percentage
  Serial.println("% on");
  delay(2000);                       // keep this level for 2 seconds
}

void loop() {
  showLevel(0);     // off
  showLevel(64);    // about 25%
  showLevel(128);   // about 50%
  showLevel(255);   // fully on
}                   // then loop() starts again from the top
