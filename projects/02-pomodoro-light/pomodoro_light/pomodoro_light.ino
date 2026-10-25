// Pin by Pin Lab project 02: Pomodoro focus light
// Uses only episodes 1-4: button + edge + debounce, millis(), bool, unsigned long.
// Two breadboards (episode 4): red LED GPIO 23, green LED GPIO 25, button GPIO 22.
// Press: the timer starts. The red LED blinks slowly, then faster as time runs out.
// Time's up: green on, red off. Press again to start a new round.

const int RED_PIN = 23;
const int GREEN_PIN = 25;
const int BUTTON_PIN = 22;

const unsigned long FOCUS_TIME = 25000;   // 25 s for the demo; a real Pomodoro is 25 min = 1500000

bool running = false;
unsigned long startTime = 0;
bool redOn = false;
unsigned long lastBlink = 0;

int lastState = HIGH;
unsigned long lastChange = 0;

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) {        // a new press: start a round
      running = true;
      startTime = now;
      digitalWrite(GREEN_PIN, LOW);
      Serial.println("focus!");
    }
  }

  if (running) {
    unsigned long elapsed = now - startTime;
    if (elapsed >= FOCUS_TIME) {
      running = false;         // time's up
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, HIGH);
      Serial.println("break time");
    } else {
      unsigned long left = FOCUS_TIME - elapsed;
      unsigned long interval = 1000;          // plenty of time: slow
      if (left < FOCUS_TIME / 2) {
        interval = 400;                       // half gone: faster
      }
      if (left < FOCUS_TIME / 5) {
        interval = 120;                       // last fifth: hurry!
      }
      if (now - lastBlink >= interval) {
        lastBlink = now;
        redOn = !redOn;
        digitalWrite(RED_PIN, redOn ? HIGH : LOW);
      }
    }
  }
}
