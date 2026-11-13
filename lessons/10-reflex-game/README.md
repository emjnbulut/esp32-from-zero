# Episode 10 — Mini Project 1: a Reflex Game with a Record that Survives Power Off

Press the button, wait for the red, yellow and then **green** light, and press again as fast as you can. The board measures your
reaction time, shows how you did with the color LED, and keeps your **best time** even when you unplug the board.

**You need:** nothing new. It is exactly the circuit from episode 9, so no new wire is needed.

| Part | Pin |
|---|---|
| Light red | GPIO 23 |
| Light yellow | GPIO 18 |
| Light green | GPIO 17 |
| Result light (the RGB LED), red leg | GPIO 25 |
| Result light (the RGB LED), green leg | GPIO 26 |
| Result light (the RGB LED), blue leg | GPIO 27 |
| Start / reaction button | GPIO 22 |
| Knob (potentiometer middle leg) | GPIO 34 |

```
GPIO 23 ──► 220 Ω ──► red LED     (long leg) ─ short leg ──► GND
GPIO 18 ──► 220 Ω ──► yellow LED  (long leg) ─ short leg ──► GND
GPIO 17 ──► 220 Ω ──► green LED   (long leg) ─ short leg ──► GND
GPIO 25 ──► RGB LED red leg      (result: red = slow)
GPIO 26 ──► RGB LED green leg    (result: green = fast)
GPIO 27 ──► RGB LED blue leg     (idle light: dim blue)
GPIO 22 ◄── button ── GND        (INPUT_PULLUP: pressed = LOW)
GPIO 34 ◄── knob middle leg      (outer legs: 3V3 and GND)
```

If a part is missing, the wiring of each earlier episode is in its own lesson folder. The plus rail must be **3.3 V, never 5 V**.

## 1. A quick look back

- **In the crossing, the helper `goTo()` always did two jobs. Which two?** It put the new step number into `state`, and it wrote down the time. Without the time, the new step thinks it is already over.
- **How do you make orange with the color LED?** Red fully on, just a little green, and blue off. Light adds up, so red with a touch of green looks orange.

## 2. The plan

- Press the button to start. The **red** light comes on, then the **yellow**, and then **green**. The moment you see green, press.
- The color LED shows how you did: **green** for fast (under 250 ms), **yellow** for okay (under 500 ms) and **red** for slow.
- The knob sets how long the yellow waits (1 to 4 seconds), so you cannot just count.

## 3. The idea: the same washing machine, five steps

The game is the washing machine from episode 9 again: one variable, `state`, says which step we are in, and `millis()` says how long.
This time there are five steps:

| `state` | Step | What happens | It ends when |
|---|---|---|---|
| 0 | Waiting | blue idle light | the button is pressed |
| 1 | Red | red light | 1 second has passed |
| 2 | Yellow | yellow light | the knob's time (1 to 4 s) has passed |
| 3 | Green: go! | green light | the button is pressed |
| 4 | Result | color LED shows the result | 3 seconds have passed, then back to step 0 |

**How can the board measure your reaction time?** You already know the trick: the parking ticket. When green comes on, `goTo()` writes
down the time. When you press, *now minus that moment* is your reaction. So the **time spent in the green step is your reaction time**:
no new code is needed for that. In the sketch it is the variable `inState`.

## 4. The reflex game — [`code/reflex_game`](code/reflex_game/reflex_game.ino)

New ideas in this sketch:

- **`pressed`**: a true-or-false variable. It is `true` only in the one `loop()` round where a *new* press happens. Holding the button
  does not count again, so every step can simply ask: was there a press just now?
- **`if` / `else if`** pick the result color from the reaction time, and `setColor()` shows it.
- **`Preferences`**: a value that survives unplugging the board (next section).

```c
// ESP32 From Zero - Episode 10 (mini project 1): reflex game with a record that survives a power cut
// Lights: red GPIO 23, yellow GPIO 18, green GPIO 17. Result: RGB LED (25 / 26 / 27).
// Button on GPIO 22, potentiometer on GPIO 34 (sets how long yellow waits: 1 .. 4 s).
// What it does: press to start. Red, then yellow, then GREEN: press as fast as you can.
// Your time is printed and shown in color: green < 250 ms, yellow < 500 ms, otherwise red.
// The best time is saved with Preferences (the ESP32's own small memory that keeps values
// when the power is off), so the record is still there after unplugging the board.
// Same pattern as the crossing in episode 9: state says which step we are in, millis() how long.

#include <Preferences.h>

const int RED_PIN = 23;
const int YELLOW_PIN = 18;
const int GREEN_PIN = 17;
const int RGB_R = 25;
const int RGB_G = 26;
const int RGB_B = 27;
const int BUTTON_PIN = 22;
const int POT_PIN = 34;

Preferences prefs;             // the ESP32's little drawer that keeps values without power
unsigned long best = 9999;     // the record in ms (9999 = no record yet)

int state = 0;                 // the step: 0 wait to start, 1 red, 2 yellow, 3 green (go!), 4 show the result
unsigned long stateStart = 0;  // when the current step began (ms)
unsigned long waitTime = 2000; // yellow time, from the knob

int lastButton = HIGH;         // the button, as in episode 4
unsigned long lastChange = 0;

// the RGB result light, as in episode 6
void setColor(int r, int g, int b) {
  analogWrite(RGB_R, r);
  analogWrite(RGB_G, g);
  analogWrite(RGB_B, b);
}

// helper 1: set the three lights in one call (HIGH = on, LOW = off)
void lights(int red, int yellow, int green) {
  digitalWrite(RED_PIN, red);
  digitalWrite(YELLOW_PIN, yellow);
  digitalWrite(GREEN_PIN, green);
}

// helper 2: move to a new step = new number in state + write down the time
void goTo(int newState, unsigned long now) {
  state = newState;
  stateStart = now;
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(RGB_R, OUTPUT);
  pinMode(RGB_G, OUTPUT);
  pinMode(RGB_B, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);

  prefs.begin("reflex", false);              // open our drawer called "reflex"
  best = prefs.getULong("best", 9999);       // read the record (9999 if there is none yet)
  Serial.print("record: ");
  Serial.println(best);
  setColor(0, 0, 40);                        // dim blue: press to start
}

void loop() {
  unsigned long now = millis();

  // PART 1 - the button: pressed is true only at the moment of a new press
  bool pressed = false;
  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW) {
      pressed = true;
    }
  }

  // PART 2 - the steps
  unsigned long inState = now - stateStart;        // how long we have been in this step

  if (state == 0) {                                  // step 0: waiting for a start press
    if (pressed) {
      setColor(0, 0, 0);
      lights(HIGH, LOW, LOW);
      goTo(1, now);
    }
  } else if (state == 1) {                           // step 1: red for 1 s
    if (inState >= 1000) {
      lights(LOW, HIGH, LOW);
      waitTime = map(analogRead(POT_PIN), 0, 4095, 1000, 4000);
      goTo(2, now);
    }
  } else if (state == 2) {                           // step 2: yellow, for waitTime
    if (inState >= waitTime) {
      lights(LOW, LOW, HIGH);                        // GO!
      goTo(3, now);
    }
  } else if (state == 3) {                           // step 3: green, measure the reaction
    if (pressed) {
      unsigned long reaction = inState;              // time since green came on
      Serial.print("reaction: ");
      Serial.print(reaction);
      Serial.println(" ms");
      if (reaction < 250) {
        setColor(0, 255, 0);
      } else if (reaction < 500) {
        setColor(255, 160, 0);
      } else {
        setColor(255, 0, 0);
      }
      if (reaction < best) {                         // a new record: save it
        best = reaction;
        prefs.putULong("best", best);
        Serial.println("new record!");
      }
      lights(LOW, LOW, LOW);
      goTo(4, now);
    }
  } else {                                           // step 4: show the result for 3 s
    if (inState >= 3000) {
      setColor(0, 0, 40);
      goTo(0, now);
    }
  }
}
```

Pause-and-predict moments to try while you read:

1. You hold the button down for a whole second. In how many rounds is `pressed` true? **Just one.**
2. Write step 2 yourself before you read it: when the yellow time is up, green comes on, and we go to step 3.
3. If `250` becomes `200`, what happens to your green results? **Green gets harder to earn**: only really fast presses count, and more rounds end yellow.

## 5. The record: why a variable forgets, and Preferences remembers

Pause and predict: you set a great time, then unplug the board and plug it back in. Is the record still there?

With an ordinary variable, **no**. Every variable lives in memory that is wiped when the power goes. After a restart, `best` starts over.

Think of your desk. Variables are labeled boxes on the desk, and a power cut clears the whole desk. But a **notebook in the drawer** stays.

What actually happens: the ESP32 keeps a small corner of its **flash memory** (the same memory that holds your program) where values
survive without power. The library `Preferences` lets you write numbers there. The difference from a real notebook: this drawer is
small, and every write wears it a little. So we write **only when something worth keeping happens**.

Three lines do the job:

```c
#include <Preferences.h>              // the library
Preferences prefs;                    // our drawer

prefs.begin("reflex", false);         // in setup(): open the drawer called "reflex"
best = prefs.getULong("best", 9999);  // in setup(): read the page "best" (9999 if it is still empty)
prefs.putULong("best", best);         // in step 3: write the new record
```

- `prefs.begin("reflex", false)` opens a drawer with a name. `false` means we may read **and** write.
- `prefs.getULong("best", 9999)` reads the page called `best`. If the page is still empty, it gives back the **default**, the number in the second slot.
- Why `9999` as the starting record? Any real reaction is smaller, so your very first round always becomes the record.
- `prefs.putULong("best", best)` writes the number into the drawer. We call it **only when the reaction beats `best`**.

**The test:** unplug the cable, wait a moment, plug it back in. The Serial Monitor starts again, and the first line (`record: ...`) shows the old record. The drawer kept it.

## 6. A mistake you might make: saving every result

Someone wants to save the result, so they write `prefs.putULong(...)` after **every** round, without the `if`.

What happens to a great record after one slow round? **It is gone.** The slow time is written over it. The `if (reaction < best)` is what
makes it a *record*: only a better time goes into the drawer. (It also saves wear: the drawer is written far less often.)

## 7. Pause and explain

Say in your own words why `best` alone forgets the record, but the drawer keeps it. One way to say it: variables live in memory that
needs power. The drawer is flash memory, which keeps its contents without power.

## 8. Your turn: the false start (project homework)

Pause and predict: what does the game do now if you press **during the yellow**? **Nothing at all.** So a cheater can tap the button
again and again, and catch the green by luck.

Add a **false start**: a press during red or yellow flashes the color LED **red**, and **no time counts** (no record is saved).

You need one more step number and one more check. Try it yourself first.

<details>
<summary>SOLUTION (spoiler): <a href="code/challenge_false_start/challenge_false_start.ino"><code>code/challenge_false_start</code></a></summary>

It is the reflex game plus a step 5 (the false start) and one more check *before* the normal steps: if the step is 1 or 2 and `pressed` is
true, print `FALSE START!`, turn the lights off and go to step 5. Step 5 flashes the color LED red for 2 seconds (the same flashing
trick as the walk light in episode 9), saves nothing, and goes back to step 0.

```c
// ESP32 From Zero - Episode 10 (mini project 1) challenge (one solution): reflex game with anti-cheat
// Lights: red GPIO 23, yellow GPIO 18, green GPIO 17. Result: RGB LED (25 / 26 / 27).
// Button on GPIO 22, potentiometer on GPIO 34 (sets how long yellow waits: 1 .. 4 s).
// What it does: press to start. Red, then yellow, then GREEN: press as fast as you can.
// Your time is printed and shown in color: green < 250 ms, yellow < 500 ms, otherwise red.
// The best time is saved with Preferences (the ESP32's own small memory that keeps values
// when the power is off), so the record is still there after unplugging the board.
// Same pattern as the crossing in episode 9: state says which step we are in, millis() how long.
// The catch: a press while still red or yellow is a FALSE START: the RGB flashes red for 2 s, no time counts.

#include <Preferences.h>

const int RED_PIN = 23;
const int YELLOW_PIN = 18;
const int GREEN_PIN = 17;
const int RGB_R = 25;
const int RGB_G = 26;
const int RGB_B = 27;
const int BUTTON_PIN = 22;
const int POT_PIN = 34;

Preferences prefs;             // the ESP32's little drawer that keeps values without power
unsigned long best = 9999;     // the record in ms (9999 = no record yet)

int state = 0;                 // the step: 0 wait, 1 red, 2 yellow, 3 green (go!), 4 result, 5 false start
unsigned long stateStart = 0;  // when the current step began (ms)
unsigned long waitTime = 2000; // yellow time, from the knob
bool flashOn = false;          // the false-start flash, like the walk light blink in episode 9
unsigned long lastFlash = 0;

int lastButton = HIGH;         // the button, as in episode 4
unsigned long lastChange = 0;

// the RGB result light, as in episode 6
void setColor(int r, int g, int b) {
  analogWrite(RGB_R, r);
  analogWrite(RGB_G, g);
  analogWrite(RGB_B, b);
}

// helper 1: set the three lights in one call (HIGH = on, LOW = off)
void lights(int red, int yellow, int green) {
  digitalWrite(RED_PIN, red);
  digitalWrite(YELLOW_PIN, yellow);
  digitalWrite(GREEN_PIN, green);
}

// helper 2: move to a new step = new number in state + write down the time
void goTo(int newState, unsigned long now) {
  state = newState;
  stateStart = now;
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(RGB_R, OUTPUT);
  pinMode(RGB_G, OUTPUT);
  pinMode(RGB_B, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);

  prefs.begin("reflex", false);              // open our drawer called "reflex"
  best = prefs.getULong("best", 9999);       // read the record (9999 if there is none yet)
  Serial.print("record: ");
  Serial.println(best);
  setColor(0, 0, 40);                        // dim blue: press to start
}

void loop() {
  unsigned long now = millis();

  // PART 1 - the button: pressed is true only at the moment of a new press
  bool pressed = false;
  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW) {
      pressed = true;
    }
  }

  // PART 2 - the steps
  unsigned long inState = now - stateStart;        // how long we have been in this step

  if (state == 0) {                                  // step 0: waiting for a start press
    if (pressed) {
      setColor(0, 0, 0);
      lights(HIGH, LOW, LOW);
      goTo(1, now);
    }
  } else if ((state == 1 || state == 2) && pressed) { // pressed too early: false start
    Serial.println("FALSE START!");
    lights(LOW, LOW, LOW);
    goTo(5, now);
  } else if (state == 1) {                           // step 1: red for 1 s
    if (inState >= 1000) {
      lights(LOW, HIGH, LOW);
      waitTime = map(analogRead(POT_PIN), 0, 4095, 1000, 4000);
      goTo(2, now);
    }
  } else if (state == 2) {                           // step 2: yellow, for waitTime
    if (inState >= waitTime) {
      lights(LOW, LOW, HIGH);                        // GO!
      goTo(3, now);
    }
  } else if (state == 3) {                           // step 3: green, measure the reaction
    if (pressed) {
      unsigned long reaction = inState;              // time since green came on
      Serial.print("reaction: ");
      Serial.print(reaction);
      Serial.println(" ms");
      if (reaction < 250) {
        setColor(0, 255, 0);
      } else if (reaction < 500) {
        setColor(255, 160, 0);
      } else {
        setColor(255, 0, 0);
      }
      if (reaction < best) {                         // a new record: save it
        best = reaction;
        prefs.putULong("best", best);
        Serial.println("new record!");
      }
      lights(LOW, LOW, LOW);
      goTo(4, now);
    }
  } else if (state == 4) {                          // step 4: show the result for 3 s
    if (inState >= 3000) {
      setColor(0, 0, 40);
      goTo(0, now);
    }
  } else {                                           // step 5: false start, flash red for 2 s
    if (now - lastFlash >= 150) {
      lastFlash = now;
      flashOn = !flashOn;
      setColor(flashOn ? 255 : 0, 0, 0);
    }
    if (inState >= 2000) {                         // no record is saved
      setColor(0, 0, 40);
      goTo(0, now);
    }
  }
}
```

</details>

## All sketches

| Sketch | What it does |
|---|---|
| [`reflex_game`](code/reflex_game/reflex_game.ino) | the reflex game: five steps, reaction time, colors, a record kept with `Preferences` |
| [`challenge_false_start`](code/challenge_false_start/challenge_false_start.ino) | one solution to the homework: a press too early is a false start |

## Something not working?

- Nothing happens when you press? Press at the **blue idle light** (step 0), and check the button on GPIO 22 (the other leg to GND) and `INPUT_PULLUP`: pressed means `LOW`.
- A light stays dark? An LED may be in **backwards**: long leg toward the pin, short leg toward the minus rail. Nothing is damaged, flip it.
- The result light shows the wrong color? Check the RGB LED's legs: red on 25, green on 26, blue on 27.
- The record is not there after unplugging? Make sure `#include <Preferences.h>` is there and the record is written with `putULong()` only when the reaction beats `best`.
- You want to start the record over? Upload a sketch once that runs `prefs.begin("reflex", false); prefs.clear();`, or simply let a faster round beat it.
- Nothing printed? Set the Serial Monitor to 115200 baud.
- Rails split in the middle? Add a bridge wire to each rail.

## Next time

A recap of everything since episode five, with a quiz.
