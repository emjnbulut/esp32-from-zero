// ESP32 From Zero - Episode 1: Hello, ESP32!
// Prints a greeting once, then counts the seconds forever.

int seconds = 0;

void setup() {
  Serial.begin(115200);   // open the USB text channel at 115200 baud
  delay(1000);            // give the Serial Monitor a moment to connect
  Serial.println("Hello, ESP32!");
}

void loop() {
  seconds = seconds + 1;
  Serial.printf("I have been running for %d seconds\n", seconds);
  delay(1000);            // wait one second
}
