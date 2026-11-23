// ESP32 From Zero - Episode 14: I turned bananas into a piano  [DRAFT 2026-11-24]
// The ESP32 has touch pins built in: your body is a tiny capacitor, and when you touch a wire (or a banana on that
// wire) the pin's touch number DROPS. Three fruits = three piano keys. Hold the button to record 8 notes, then
// press it once to play them back.
//
// Parts:
//   touch pads: a wire from GPIO 14 (T6), GPIO 2 (T2), GPIO 15 (T3) to a banana / apple / foil   (nothing else on them)
//   passive buzzer + -> GPIO 32                                                                    (Episode 10)
//   button GPIO 19 <-> GND                                                                         (Episode 10)
//   OLED SDA -> GPIO 21, SCL -> GPIO 22                                                            (Episode 10)
// GPIO 2 also drives the board's blue LED on many boards: it may glow faintly, that's fine.
// Libraries: "Adafruit SSD1306" + "Adafruit GFX".

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int BUZZER_PIN = 32;
const int BUTTON_PIN = 19;

// a list of keys = an array: the same index in each list belongs to the same key
const int KEY_PIN[3] = {14, 2, 15};
const int NOTE[3] = {523, 659, 784};          // C5, E5, G5: a happy chord
const char* NAME[3] = {"DO", "MI", "SOL"};

int calm[3];                                  // each pad's touch number when nobody touches it
const int DROP = 20;                          // touched = the number fell this far below calm (tune if needed)

int song[8];                                  // the recorded notes (key index), like a row of 8 boxes
int songLength = 0;
bool recording = false;

Adafruit_SSD1306 screen(128, 64, &Wire, -1);
int lastKey = -1;
int lastButton = HIGH;
unsigned long buttonDown = 0;

void show(const char* top, String big) {      // same helper as Episode 10
  screen.clearDisplay();
  screen.setTextColor(SSD1306_WHITE);
  screen.setTextSize(1);
  screen.setCursor(0, 0);
  screen.print(top);
  screen.setTextSize(2);
  screen.setCursor(0, 28);
  screen.print(big);
  screen.display();
}

int touchedKey() {                            // which fruit is touched? -1 = none
  for (int i = 0; i < 3; i++) {
    if (touchRead(KEY_PIN[i]) < calm[i] - DROP) return i;
  }
  return -1;
}

void playBack() {
  show("playing", String(songLength) + " notes");
  for (int i = 0; i < songLength; i++) {
    tone(BUZZER_PIN, NOTE[song[i]], 250);
    show("playing", NAME[song[i]]);
    delay(320);
  }
  show("touch a fruit", "PIANO");
}

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
  screen.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  show("don't touch...", "CALIBRATE");
  delay(500);
  for (int i = 0; i < 3; i++) {               // learn each pad's calm number (average of 8 looks, Episode 7)
    long sum = 0;
    for (int n = 0; n < 8; n++) sum += touchRead(KEY_PIN[i]);
    calm[i] = sum / 8;
    Serial.printf("pad %d calm = %d\n", KEY_PIN[i], calm[i]);
  }
  show("touch a fruit", "PIANO");
}

void loop() {
  unsigned long now = millis();

  int key = touchedKey();
  if (key != lastKey) {                       // a new touch (or a release)
    lastKey = key;
    if (key >= 0) {
      tone(BUZZER_PIN, NOTE[key], 200);
      if (recording && songLength < 8) {
        song[songLength] = key;               // put the note in the next box
        songLength++;
        show(("recording " + String(songLength) + "/8").c_str(), NAME[key]);
        if (songLength == 8) {
          recording = false;
          show("saved 8 notes", "PRESS");
        }
      } else if (!recording) {
        show("touch a fruit", NAME[key]);
      }
    }
  }

  int b = digitalRead(BUTTON_PIN);            // short press = play back, hold 1 s = record a new song
  if (b == LOW && lastButton == HIGH) buttonDown = now;
  if (b == HIGH && lastButton == LOW) {
    if (now - buttonDown >= 1000) {
      recording = true;
      songLength = 0;
      show("record: touch 8", "REC");
    } else if (songLength > 0 && !recording) {
      playBack();
    }
  }
  lastButton = b;
  delay(10);                                  // 100 looks a second are plenty for fingers
}
