// ESP32 From Zero - Episode 6 (part 2): a 3-LED level bar
// Potentiometer on GPIO 34; green LED on GPIO 17, yellow on GPIO 18, red on GPIO 23.
// What it does: like a volume meter. Knob at the left: all off. Turn it right:
// first green lights, then green + yellow, then all three.
// map() turns 0 .. 4095 into a level 0 .. 3; if / else if picks which LEDs are on.

const int POT_PIN = 34;
const int GREEN_PIN = 17;
const int YELLOW_PIN = 18;
const int RED_PIN = 23;

void setup() {
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(POT_PIN);       // 0 .. 4095
  int level = map(value, 0, 4096, 0, 4); // 0, 1, 2 or 3 (4096 and 4: so the right end still gives 3)

  if (level == 0) {                      // nothing
    digitalWrite(GREEN_PIN, LOW);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(RED_PIN, LOW);
  } else if (level == 1) {               // green
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(RED_PIN, LOW);
  } else if (level == 2) {               // green + yellow
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(YELLOW_PIN, HIGH);
    digitalWrite(RED_PIN, LOW);
  } else {                               // all three
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(YELLOW_PIN, HIGH);
    digitalWrite(RED_PIN, HIGH);
  }

  Serial.println(level);
  delay(20);
}
