// ESP32 From Zero - Episode 4 challenge (one solution):
// the button switches the green LED between fast and slow; the red LED keeps blinking.

const int BUTTON_PIN = 22;
const int RED_PIN = 23;
const int GREEN_PIN = 25;

unsigned long greenInterval = 150;   // ms: 150 = fast, 600 = slow
bool redOn = false, greenOn = false;
unsigned long lastRed = 0, lastGreen = 0;

int lastState = HIGH;
unsigned long lastChange = 0;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {
      greenInterval = (greenInterval == 150) ? 600 : 150;
      Serial.print("green every ");
      Serial.print(greenInterval);
      Serial.println(" ms");
    }
  }

  if (now - lastRed >= 500) {
    lastRed = now;
    redOn = !redOn;
    digitalWrite(RED_PIN, redOn ? HIGH : LOW);
  }
  if (now - lastGreen >= greenInterval) {
    lastGreen = now;
    greenOn = !greenOn;
    digitalWrite(GREEN_PIN, greenOn ? HIGH : LOW);
  }
}
