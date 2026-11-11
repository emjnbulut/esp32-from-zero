# Episode 9 — Mini Project 1: a Smart Pedestrian Crossing

Our first mini project puts everything together: car lights, a walk light, a request button and a knob. One variable, `state`,
remembers which step the crossing is in, and `millis()` times every step, so the program never freezes inside a `delay()`.

**You need:** nothing new. No new wire is needed: everything is already on the board from the earlier episodes.

| Part | Pin |
|---|---|
| Car light red | GPIO 23 |
| Car light yellow | GPIO 18 |
| Car light green | GPIO 17 |
| Walk light (the RGB LED), red leg | GPIO 25 |
| Walk light (the RGB LED), green leg | GPIO 26 |
| Request button | GPIO 22 |
| Knob (potentiometer middle leg) | GPIO 34 |

```
GPIO 23 ──► 220 Ω ──► red LED     (long leg) ─ short leg ──► GND
GPIO 18 ──► 220 Ω ──► yellow LED  (long leg) ─ short leg ──► GND
GPIO 17 ──► 220 Ω ──► green LED   (long leg) ─ short leg ──► GND
GPIO 25 ──► RGB LED red leg      (walk light: red = wait)
GPIO 26 ──► RGB LED green leg    (walk light: green = walk)
GPIO 22 ◄── button ── GND        (INPUT_PULLUP: pressed = LOW)
GPIO 34 ◄── knob middle leg      (outer legs: 3V3 and GND)
```

If a part is missing, the wiring of each earlier episode is in its own lesson folder. The plus rail must be **3.3 V, never 5 V**.

## 1. A quick look back

- **Why did the obvious level line almost never light all three LEDs (episode 8)?** Because `map()` rounds down. The top level only came at the very last mark of the ruler.
- **How can the board tell that two seconds have passed, without freezing the program with `delay()`?** It glances at the wall clock, `millis()`. It subtracts the moment it remembered from now, and checks whether the difference has reached 2000.

## 2. The plan, and why a chain of `delay()` fails

- The three LEDs are the **car lights**. The RGB LED is the **walk light**: red means wait, green means walk.
- The button is the walker's **request button**. The knob sets how long the cars keep their green, from **3 to 10 seconds**.

The first idea is a chain: green, `delay()`, yellow, `delay()`, red, `delay()`. Pause-and-predict: what happens to a button press while
the program is waiting? **It is lost.** During a `delay()` nothing else runs, so nobody looks at the button. We need a way to wait
without stopping.

## 3. A washing machine remembers its step

Think of a washing machine. It goes through steps: wash, rinse, spin. At any moment it knows exactly which step it is in, and it moves
on when that step's time is up.

What actually happens in our code: the step is just a **whole number** in a variable called `state`. Every round of `loop()` checks that
number and runs only the code of that step. Moving on is one assignment: put the next number into `state`, and **write down the time**.
That moment is when the new step started.

The difference from a washing machine: the machine really does its step. Our loop does not wait inside a step; it just looks at the
number thousands of times a second, and decides.

Our crossing has four steps, numbered from zero:

| `state` | Step | Cars | Walk light | It ends when |
|---|---|---|---|---|
| 0 | Cars green | green | red | somebody is waiting **and** the green has lasted long enough (knob: 3 to 10 s) |
| 1 | Cars yellow | yellow | red | 2 seconds have passed |
| 2 | The walker crosses | red | green | 4 seconds have passed |
| 3 | Hurry up | red | green, blinking | 2 seconds have passed, then back to step 0 |

## 4. The crossing — [`code/crossing`](code/crossing/crossing.ino)

```c
// ESP32 From Zero - Episode 9 (mini project 1): a smart pedestrian crossing
// Car lights: red GPIO 23, yellow GPIO 18, green GPIO 17. Pedestrian light: the RGB LED (red 25, green 26).
// Button on GPIO 22 (the pedestrian's "request" button), potentiometer on GPIO 34.
// What it does: cars have green. A press asks to cross. Once the cars had green long enough
// (3 .. 10 s, set with the knob), the light goes yellow, then red, and the pedestrian gets green;
// in the last 2 seconds the pedestrian green blinks. Then the cars get green again.
// One variable, state, says which step we are in; millis() says how long we have been in it.

const int CAR_RED = 23;
const int CAR_YELLOW = 18;
const int CAR_GREEN = 17;
const int WALK_RED = 25;       // RGB red leg
const int WALK_GREEN = 26;     // RGB green leg
const int BUTTON_PIN = 22;
const int POT_PIN = 34;

int state = 0;                 // the step: 0 cars green, 1 cars yellow, 2 walk, 3 walk blinking
unsigned long stateStart = 0;  // when the current step began (ms)
bool request = false;          // somebody pressed the button and waits

int lastButton = HIGH;         // the button, as in episode 4
unsigned long lastChange = 0;
bool blinkOn = true;
unsigned long lastBlink = 0;

// helper 1: set all five lights in one call (HIGH = on, LOW = off)
void lights(int red, int yellow, int green, int walkRed, int walkGreen) {
  digitalWrite(CAR_RED, red);
  digitalWrite(CAR_YELLOW, yellow);
  digitalWrite(CAR_GREEN, green);
  digitalWrite(WALK_RED, walkRed);
  digitalWrite(WALK_GREEN, walkGreen);
}

// helper 2: move to a new step = new number in state + write down the time
void goTo(int newState, unsigned long now) {
  state = newState;
  stateStart = now;
  Serial.print("state ");
  Serial.println(state);
}

void setup() {
  pinMode(CAR_RED, OUTPUT);
  pinMode(CAR_YELLOW, OUTPUT);
  pinMode(CAR_GREEN, OUTPUT);
  pinMode(WALK_RED, OUTPUT);
  pinMode(WALK_GREEN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  // PART 1 - the button: a new press while the cars have green is a request to cross
  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW && state == 0) {
      request = true;
      Serial.println("request");
    }
  }

  // PART 2 - the steps
  unsigned long inState = now - stateStart;              // how long we have been in this step
  unsigned long greenTime = map(analogRead(POT_PIN), 0, 4095, 3000, 10000);

  if (state == 0) {                                       // step 0: cars green, pedestrians wait
    lights(LOW, LOW, HIGH, HIGH, LOW);
    if (request && inState >= greenTime) {
      goTo(1, now);
    }
  } else if (state == 1) {                                // step 1: cars yellow for 2 s
    lights(LOW, HIGH, LOW, HIGH, LOW);
    if (inState >= 2000) {
      request = false;
      goTo(2, now);
    }
  } else if (state == 2) {                                // step 2: cars red, pedestrians walk for 4 s
    lights(HIGH, LOW, LOW, LOW, HIGH);
    if (inState >= 4000) {
      goTo(3, now);
    }
  } else {                                                // step 3: the walk light blinks for 2 s
    if (now - lastBlink >= 250) {
      lastBlink = now;
      blinkOn = !blinkOn;
    }
    lights(HIGH, LOW, LOW, LOW, blinkOn ? HIGH : LOW);
    if (inState >= 2000) {
      goTo(0, now);
    }
  }
}
```

**Line by line**

| Part | What it does |
|---|---|
| `CAR_RED`, `CAR_YELLOW`, `CAR_GREEN`, `WALK_RED`, `WALK_GREEN` | The five lights on 23, 18, 17, 25 and 26, all outputs in `setup()`. |
| `BUTTON_PIN`, `POT_PIN` | The request button on 22 (`INPUT_PULLUP`, pressed = `LOW`) and the knob on 34. |
| `int state = 0;` | The step the crossing is in. It starts at 0: cars green. |
| `unsigned long stateStart = 0;` | The time the current step began, in milliseconds. |
| `bool request = false;` | `true` when somebody pressed the button and is waiting. |
| `lights(red, yellow, green, walkRed, walkGreen)` | Helper 1: sets all five lights in one call, like the coffee machine button from the color LED episode. |
| `goTo(newState, now)` | Helper 2: does the two jobs of moving on. It puts the new number into `state` and writes down the time in `stateStart`. It also prints the step. |
| `unsigned long now = millis();` | The wall clock, read once per round. |
| `if (b != lastButton && now - lastChange >= 50)` | The button from episode 4: a change that is at least 50 ms after the last one, so bounce is ignored. |
| `if (b == LOW && state == 0)` | A new press only counts while the cars have green (step 0). Then `request` is set to `true`. |
| `unsigned long inState = now - stateStart;` | One subtraction: now minus the moment the step began. That is how long we have been in this step. |
| `map(analogRead(POT_PIN), 0, 4095, 3000, 10000)` | Last episode's function with a real job: the knob becomes the green time, 3000 to 10,000 ms. |
| `if (state == 0)` | Step 0: cars green, walk light red. If `request` and the green lasted `greenTime`, `goTo(1, now)`. |
| `else if (state == 1)` | Step 1: cars yellow. After 2000 ms the request is forgotten and `goTo(2, now)`. |
| `else if (state == 2)` | Step 2: cars red, walk light green. After 4000 ms, `goTo(3, now)`. |
| `else` | Step 3: the walk light blinks. `lastBlink` and `blinkOn` flip it every 250 ms, with the same clock trick. After 2000 ms, `goTo(0, now)`. |
| `&&` | The *and* from episode 8's challenge: both checks must be true. |

Pause-and-predict: you press the button while the walker is already crossing. Does that press count? **No.** Presses only count in
step 0, so the crossing never starts over by accident.

Pause-and-predict: the cars have just turned green and you press the button right away. Does the walker get green at once? **No.**
The press is remembered, but the cars keep their green until the knob's time is up. Only then does yellow come.

Try it: watch a whole round and notice the walk light going from red to green. In the last 2 seconds it blinks to say *hurry*, while the
cars are still red. Now change one number: if `4000` becomes `8000`, the walker gets **twice as long** to cross. Nothing else changes,
because every step keeps its own time.

## 5. How long was the button held? — [`code/press_time`](code/press_time/press_time.ino)

The project has one more trick: measuring how long the button was held. Think of a **parking ticket**. When you drive in, the ticket
gets the time stamped on it. When you leave, the machine subtracts that time from now, and you pay for the difference.

What actually happens in our code: at the press, we save `now` in a variable called `pressStart`. At the release, `now - pressStart`
is how long the button was held. The difference from a ticket: there is no paper. `pressStart` is just one number in memory, and the
next press writes over it.

```c
// ESP32 From Zero - Episode 9 (mini project 1): how long was the button held?
// Button on GPIO 22, yellow LED on GPIO 18.
// What it does: the yellow LED is on while you hold the button. When you let go, the Serial Monitor
// prints how long you held it, and whether that was a short press (< 250 ms) or a long one.
// The trick is a parking ticket: remember the time of the press (pressStart);
// at the release, now - pressStart is how long it was held.

const int BUTTON_PIN = 22;
const int LED_PIN = 18;

int lastButton = HIGH;
unsigned long lastChange = 0;
unsigned long pressStart = 0;  // when the button went down

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();
  int b = digitalRead(BUTTON_PIN);

  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW) {                        // pressed: stamp the ticket
      pressStart = now;
      digitalWrite(LED_PIN, HIGH);
    } else {                               // released: how long was it?
      digitalWrite(LED_PIN, LOW);
      unsigned long held = now - pressStart;
      Serial.print(held);
      Serial.print(" ms: ");
      if (held < 250) {
        Serial.println("short");
      } else {
        Serial.println("long");
      }
    }
  }
}
```

**Line by line**

| Part | What it does |
|---|---|
| `BUTTON_PIN`, `LED_PIN` | The button on 22 and the yellow LED on 18. |
| `unsigned long pressStart = 0;` | The parking ticket: the time the button went down. |
| `if (b != lastButton && now - lastChange >= 50)` | A real change of the button, with bounce ignored (episode 4). |
| `if (b == LOW)` | Pressed: `pressStart = now;` stamps the ticket, and the yellow LED turns on. |
| `else` | Released: the LED turns off, and the time is worked out. |
| `unsigned long held = now - pressStart;` | Now minus the stamped time: how long the button was held. |
| `if (held < 250)` | Anything under a quarter of a second is `short`, anything else is `long`. |
| `Serial.print(held);` | Prints the time, then ` ms: `, then the word. |

Pause-and-predict: you tap the button as fast as you can. What does it print? Something like **100 ms** and `short`. Hold it for a second,
and it prints about **1000** and `long`. That is how one button can do two jobs. Your phone does the same: a tap wakes it up, and a long
press turns it off.

## 6. A mistake you might make: a new step without a new start time

Someone moves on by just writing `state = 1;` and forgets to write down the time. What does the crossing do then? The yellow flashes
for a split second, and it is gone. The step's start time (`stateStart`) is still the **old** one, so the subtraction says that
2 seconds have long passed.

That is why `goTo()` always does both jobs together. **Use it for every change of step.**

## 7. Pause and explain

Say in your own words why each step needs its own start time. One way to say it: every step measures its time from the moment it began.
So a new step needs a new start, or it thinks its time is already up.

## 8. Your turn: slow walker mode

If the request button is **held for more than a second**, the walk light stays green **twice as long** (8 seconds instead of 4).

You already know both pieces: the parking ticket (`pressStart`), and a step that keeps its own time. Try it yourself first.

<details>
<summary>One solution: <a href="code/slow_walker/slow_walker.ino"><code>code/slow_walker</code></a></summary>

It is the crossing plus a `pressStart` ticket and a `walkTime` variable. At the press, the ticket is stamped and `walkTime` goes back to
4000. At the release, if the button was held for 1000 ms or more, `walkTime` becomes 8000. Step 2 then lasts `walkTime`.

```c
// ESP32 From Zero - Episode 9 (mini project 1), your turn: slow walker mode (one possible solution)
// Same as crossing, plus: hold the request button for more than 1 s and the walk light stays green twice as long.
// Car lights: red GPIO 23, yellow GPIO 18, green GPIO 17. Pedestrian light: the RGB LED (red 25, green 26).
// Button on GPIO 22 (the pedestrian's "request" button), potentiometer on GPIO 34.
// What it does: cars have green. A press asks to cross. Once the cars had green long enough
// (3 .. 10 s, set with the knob), the light goes yellow, then red, and the pedestrian gets green;
// in the last 2 seconds the pedestrian green blinks. Then the cars get green again.
// One variable, state, says which step we are in; millis() says how long we have been in it.

const int CAR_RED = 23;
const int CAR_YELLOW = 18;
const int CAR_GREEN = 17;
const int WALK_RED = 25;       // RGB red leg
const int WALK_GREEN = 26;     // RGB green leg
const int BUTTON_PIN = 22;
const int POT_PIN = 34;

int state = 0;                 // the step: 0 cars green, 1 cars yellow, 2 walk, 3 walk blinking
unsigned long stateStart = 0;  // when the current step began (ms)
bool request = false;          // somebody pressed the button and waits
unsigned long pressStart = 0;  // the parking ticket: when the button went down
unsigned long walkTime = 4000; // how long step 2 lasts: 4 s, or 8 s for a slow walker

int lastButton = HIGH;         // the button, as in episode 4
unsigned long lastChange = 0;
bool blinkOn = true;
unsigned long lastBlink = 0;

// helper 1: set all five lights in one call (HIGH = on, LOW = off)
void lights(int red, int yellow, int green, int walkRed, int walkGreen) {
  digitalWrite(CAR_RED, red);
  digitalWrite(CAR_YELLOW, yellow);
  digitalWrite(CAR_GREEN, green);
  digitalWrite(WALK_RED, walkRed);
  digitalWrite(WALK_GREEN, walkGreen);
}

// helper 2: move to a new step = new number in state + write down the time
void goTo(int newState, unsigned long now) {
  state = newState;
  stateStart = now;
  Serial.print("state ");
  Serial.println(state);
}

void setup() {
  pinMode(CAR_RED, OUTPUT);
  pinMode(CAR_YELLOW, OUTPUT);
  pinMode(CAR_GREEN, OUTPUT);
  pinMode(WALK_RED, OUTPUT);
  pinMode(WALK_GREEN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();

  // PART 1 - the button: a new press while the cars have green is a request to cross
  int b = digitalRead(BUTTON_PIN);
  if (b != lastButton && now - lastChange >= 50) {
    lastChange = now;
    lastButton = b;
    if (b == LOW && state == 0) {
      request = true;
      pressStart = now;
      walkTime = 4000;
      Serial.println("request");
    }
    if (b == HIGH && request && now - pressStart >= 1000) {   // released after a long hold
      walkTime = 8000;
      Serial.println("slow walker: 8 s");
    }
  }

  // PART 2 - the steps
  unsigned long inState = now - stateStart;              // how long we have been in this step
  unsigned long greenTime = map(analogRead(POT_PIN), 0, 4095, 3000, 10000);

  if (state == 0) {                                       // step 0: cars green, pedestrians wait
    lights(LOW, LOW, HIGH, HIGH, LOW);
    if (request && inState >= greenTime) {
      goTo(1, now);
    }
  } else if (state == 1) {                                // step 1: cars yellow for 2 s
    lights(LOW, HIGH, LOW, HIGH, LOW);
    if (inState >= 2000) {
      request = false;
      goTo(2, now);
    }
  } else if (state == 2) {                                // step 2: cars red, pedestrians walk for walkTime
    lights(HIGH, LOW, LOW, LOW, HIGH);
    if (inState >= walkTime) {
      goTo(3, now);
    }
  } else {                                                // step 3: the walk light blinks for 2 s
    if (now - lastBlink >= 250) {
      lastBlink = now;
      blinkOn = !blinkOn;
    }
    lights(HIGH, LOW, LOW, LOW, blinkOn ? HIGH : LOW);
    if (inState >= 2000) {
      goTo(0, now);
    }
  }
}
```

</details>

## All sketches

| Sketch | What it does |
|---|---|
| [`crossing`](code/crossing/crossing.ino) | the smart pedestrian crossing, four steps driven by `state` and `millis()` |
| [`press_time`](code/press_time/press_time.ino) | measures how long the button was held, short or long |
| [`slow_walker`](code/slow_walker/slow_walker.ino) | one solution to the challenge |

## Something not working?

- The light never changes? Press the button while the cars have **green**: presses only count in step 0. Then wait for the knob's green time (3 to 10 s).
- A light stays dark? An LED may be in **backwards**: long leg toward the pin, short leg toward the minus rail. Nothing is damaged, flip it.
- The walk light shows the wrong color? Check the RGB LED's legs: red on 25, green on 26.
- Yellow flashes for a split second? A step was changed without a new start time. Use `goTo()` for every change.
- The press never registers? Check the button wiring on GPIO 22 (the other leg to GND) and `INPUT_PULLUP`: pressed means `LOW`.
- Nothing printed? Set the Serial Monitor to 115200 baud.
- Rails split in the middle? Add a bridge wire to each rail.

## Next time

On the same circuit: a reflex game, with a high score that survives even when you unplug the board.
