// Pin by Pin Lab - extra project 08: Treasure Detector 2.0 (Hazine Dedektörü 2.0)
// The episode 10 circuit (OLED, button, passive buzzer) + a knob and an RGB LED.
//   OLED 0.96" I2C (SSD1306, 0x3C): SDA -> GPIO 21, SCL -> GPIO 22, VCC -> 3V3, GND -> GND   (as in episode 10)
//   button: GPIO 19 -> button -> GND (INPUT_PULLUP)                                         (as in episode 10)
//   passive buzzer: GPIO 32 -> buzzer + , buzzer - -> GND                                     (as in episode 10)
//   knob (10k potentiometer): outer legs 3V3 and GND, middle leg -> GPIO 34                  (new)
//   RGB LED (common cathode): red 25, green 26, blue 27, each through a 220 ohm resistor     (new)
// Libraries: "Adafruit SSD1306" (Library Manager also installs "Adafruit GFX" and "Adafruit BusIO").
//
// How to play: a treasure is hidden somewhere on the knob (a number 0 .. 99). Turn the knob to search.
//   far away -> the LED glows cold blue, the buzzer ticks slowly and low, the screen says SOĞUK (cold)
//   closer   -> the color warms up to red, the ticks get faster and higher, like a Geiger counter
//   on it    -> YANIYOR! (burning). Press the button to dig (KAZ!):
//               right spot  -> a fanfare, HAZİNE! and your time; the best time is saved with Preferences
//                              (it survives unplugging, as in episode 10), then the treasure hides again
//               wrong spot  -> a low buzz: BOŞ! (empty)

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Preferences.h>

const int KNOB_PIN = 34;
const int RED_PIN = 25;
const int GREEN_PIN = 26;
const int BLUE_PIN = 27;
const int BUTTON_PIN = 19;
const int BUZZER_PIN = 32;
const bool COMMON_ANODE = false;   // common anode RGB LED? set true (long leg to 3V3, episode 5)

Adafruit_SSD1306 screen(128, 64, &Wire, -1);
Preferences prefs;

int secret = 73;                 // where the treasure is hidden (0 .. 99)
unsigned long huntStart = 0;     // when this hunt started (ms)
unsigned long best = 0;          // best time in ms (0 = no record yet)

unsigned long lastTick = 0;      // the Geiger clicks
unsigned long lastDraw = 0;      // the screen is redrawn 10 times a second
int lastButton = HIGH;           // edge detection + debounce, as in episode 4
unsigned long lastChange = 0;

void setColor(int r, int g, int b) {
  if (COMMON_ANODE) {
    r = 255 - r;
    g = 255 - g;
    b = 255 - b;
  }
  analogWrite(RED_PIN, r);
  analogWrite(GREEN_PIN, g);
  analogWrite(BLUE_PIN, b);
}

// The OLED's built-in font has no Turkish letters. So in our words a small letter means
// "the capital letter with its Turkish mark": g = Ğ, i = İ, s = Ş. We print the capital
// and draw the little mark (breve, dot, cedilla) ourselves, pixel by pixel.
void bigWord(const char* word, int y) {
  int size = 2;                                // every letter is 12 x 16 pixels
  int x = (128 - strlen(word) * 6 * size) / 2; // centered
  screen.setTextSize(size);
  for (int i = 0; word[i] != 0; i++) {
    char c = word[i];
    int cx = x + i * 6 * size;
    screen.setCursor(cx, y);
    if (c == 'g') {
      screen.print('G');
      screen.fillRect(cx + 2, y - 6, 2, 2, SSD1306_WHITE);   // the breve of Ğ: a tiny "v"
      screen.fillRect(cx + 4, y - 4, 4, 2, SSD1306_WHITE);
      screen.fillRect(cx + 8, y - 6, 2, 2, SSD1306_WHITE);
    } else if (c == 'i') {
      screen.print('I');
      screen.fillRect(cx + 4, y - 5, 2, 2, SSD1306_WHITE);   // the dot of İ
    } else if (c == 's') {
      screen.print('S');
      screen.fillRect(cx + 4, y + 15, 2, 2, SSD1306_WHITE);  // the cedilla of Ş
      screen.fillRect(cx + 2, y + 17, 2, 2, SSD1306_WHITE);
    } else {
      screen.print(c);
    }
  }
}

// top line: the record, e.g. "REKOR 12.4 sn"
void topLine() {
  screen.setTextSize(1);
  screen.setCursor(0, 0);
  if (best == 0) {
    screen.print("REKOR --.- sn");
  } else {
    screen.print("REKOR ");
    screen.print(best / 1000.0, 1);
    screen.print(" sn");
  }
}

// the search screen: a word for the heat and a hot-cold meter of 12 blocks
void drawHunt(int heat) {          // heat: 0 = far away .. 255 = right on it
  screen.clearDisplay();
  screen.setTextColor(SSD1306_WHITE);
  topLine();
  if (heat < 100) {
    bigWord("SOgUK", 22);          // cold
  } else if (heat < 180) {
    bigWord("ILIK", 22);           // warm
  } else if (heat < 230) {
    bigWord("SICAK", 22);          // hot
  } else {
    bigWord("YANIYOR!", 22);       // burning
  }
  screen.drawRect(4, 48, 120, 14, SSD1306_WHITE);
  int blocks = map(heat, 0, 255, 0, 12);
  for (int i = 0; i < blocks; i++) {
    screen.fillRect(7 + i * 10, 51, 8, 8, SSD1306_WHITE);
  }
  screen.display();
}

void hideTreasure(int knob) {      // a new hiding place, far enough from the knob
  do {
    secret = random(0, 100);
  } while (abs(secret - knob) < 30);
  huntStart = millis();
}

void fanfare() {                   // C6 E6 G6 C7 on the buzzer
  int notes[] = {1047, 1319, 1568, 2093};
  for (int i = 0; i < 4; i++) {
    tone(BUZZER_PIN, notes[i]);
    delay(i < 3 ? 120 : 350);
  }
  noTone(BUZZER_PIN);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
  screen.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  prefs.begin("treasure", false);              // our drawer called "treasure"
  best = prefs.getULong("best", 0);            // the record survives unplugging
  randomSeed(analogRead(KNOB_PIN) + micros());
  hideTreasure(map(analogRead(KNOB_PIN), 0, 4095, 0, 99));
}

void loop() {
  unsigned long now = millis();
  int number = map(analogRead(KNOB_PIN), 0, 4095, 0, 99);  // the knob: 0 .. 99

  int distance = abs(number - secret);         // how far from the treasure?
  if (distance > 50) {
    distance = 50;
  }
  int heat = map(distance, 0, 50, 255, 0);      // 255 = right on it, 0 = far away
  setColor(heat, 0, 255 - heat);                // cold blue ... hot red

  // Geiger counter: close = fast and high ticks
  int tickEvery = map(distance, 0, 50, 60, 700);    // ms between ticks
  int pitch = map(distance, 0, 50, 3000, 800);      // Hz
  if (now - lastTick >= tickEvery) {
    lastTick = now;
    tone(BUZZER_PIN, pitch, 15);                     // a 15 ms click
  }

  if (now - lastDraw >= 100) {
    lastDraw = now;
    drawHunt(heat);
  }

  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW) {                              // KAZ! (dig here)
      if (distance <= 2) {
        unsigned long found = now - huntStart;
        bool record = (best == 0 || found < best);
        if (record) {
          best = found;
          prefs.putULong("best", best);          // into the drawer
        }
        screen.clearDisplay();
        screen.setTextSize(1);
        screen.setCursor(0, 2);
        if (record) {
          screen.print("YENI REKOR!");
          screen.drawPixel(20, 0, SSD1306_WHITE);      // the dot of İ in YENİ (small font)
        } else {
          screen.print("BULDUN!");                     // found it!
        }
        bigWord("HAZiNE!", 22);
        screen.setTextSize(2);
        screen.setCursor(22, 46);
        screen.print(found / 1000.0, 1);
        screen.print(" sn");
        screen.display();
        setColor(255, 160, 0);                   // gold
        fanfare();
        delay(3000);                             // 3 s to enjoy the find
        hideTreasure(number);
      } else {
        screen.clearDisplay();
        topLine();
        bigWord("BOs!", 22);                     // BOŞ! = empty
        screen.display();
        setColor(0, 0, 0);
        tone(BUZZER_PIN, 150, 400);              // low buzz
        delay(1000);
      }
    }
  }
}
