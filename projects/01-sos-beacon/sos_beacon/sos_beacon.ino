// Pin by Pin Lab project 01: SOS beacon
// Uses only episodes 1-3: const int, pinMode, digitalWrite, delay, helper functions.
// Red LED on GPIO 23 (episode 3 circuit). Morse code: S = ...  O = ---  then a pause, forever.

const int LED_PIN = 23;
const int UNIT = 200;          // one Morse "unit" in ms: a dot is 1 unit, a dash is 3

void flash(int units) {
  digitalWrite(LED_PIN, HIGH);
  delay(units * UNIT);
  digitalWrite(LED_PIN, LOW);
  delay(UNIT);                 // 1 unit of dark between the parts of a letter
}

void letterS() {
  flash(1);
  flash(1);
  flash(1);
  delay(2 * UNIT);             // 3 units between letters (1 already waited)
}

void letterO() {
  flash(3);
  flash(3);
  flash(3);
  delay(2 * UNIT);
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  Serial.println("S O S");
  letterS();
  letterO();
  letterS();
  delay(4 * UNIT);             // 7 units between words
}
