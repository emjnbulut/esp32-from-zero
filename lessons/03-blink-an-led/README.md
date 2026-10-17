# Episode 3 — Your First Circuit: Blink an LED

Last time the LED was always on, powered from the `3V3` pin. Today we move **the resistor** to a GPIO pin
and let our program switch the LED on and off.

**You need:** the circuit from episode 2 (board on the breadboard, 220 Ω resistor, LED; 2 jumper wires — the black ones — are enough now).

## 1. Why 220 Ω? (Ohm's law, simply)

**Current = Voltage ÷ Resistance** (I = V / R)

- A red LED needs about **2 V** across it to light.
- The pin gives **3.3 V**, so about **1.3 V** is left across the resistor.
- 1.3 V ÷ 220 Ω ≈ **6 mA** — clearly visible, and far below what a GPIO pin can supply.

Without a resistor nothing limits the current and the LED (or the pin) can burn out.
A bigger resistor makes the LED dimmer: anything from **220 Ω to 1 kΩ** is fine.

## 2. Move the resistor

1. **Unplug the USB cable** — never rewire a powered circuit.
2. Take the **red wire** out completely — we don't need `3V3` today.
3. Move the resistor's leg from the **+** rail into hole **`j16`**, the column of **`D23`** (GPIO 23).
   On 38-pin boards the column is labeled just **`23`**.
4. Plug the USB cable back in. The LED stays dark — nothing has turned the pin on yet.

```
GPIO 23 ──► 220 Ω ──► LED (long leg … short leg) ──► − rail ──► GND
```

GPIO 23 is one of the **safe** pins from episode 2 (4, 13, 14, 16–19, 21–23, 25–27, 32, 33).
Any of them works — just change `LED_PIN` in the code.

## 3. The code — [`code/blink_led/blink_led.ino`](code/blink_led/blink_led.ino)

```c
const int LED_PIN = 23;        // the GPIO our LED is wired to

void setup() {
  pinMode(LED_PIN, OUTPUT);    // our code drives this pin
  Serial.begin(115200);
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // 3.3 V -> LED on
  Serial.println("LED on");
  delay(500);                  // half a second

  digitalWrite(LED_PIN, LOW);  // 0 V -> LED off
  Serial.println("LED off");
  delay(500);
}
```

| Call | What it does |
|---|---|
| `pinMode(pin, OUTPUT)` | the pin is driven by our code (the other choice, `INPUT`, comes next episode) |
| `digitalWrite(pin, HIGH)` | puts **3.3 V** on the pin |
| `digitalWrite(pin, LOW)` | puts **0 V** on the pin |
| `delay(ms)` | waits that many milliseconds (1000 ms = 1 s) |

Upload it (board **ESP32 Dev Module**, your COM port). If the upload hangs at `Connecting...`, hold **BOOT**
like in episode 1. Open the **Serial Monitor** at **115200** baud to see `LED on` / `LED off`.

On the pin this makes a **square wave**: 3.3 V for 500 ms, 0 V for 500 ms, forever.

## 4. Play with it

- Both delays `100` → five blinks per second.
- `delay(100)` on, `delay(1900)` off → a lighthouse.
- Changing the numbers can't damage anything.

## Not blinking?

- Is the resistor's leg really in the **D23** column (and the code says `23`)?
- Is the LED's **long leg** on the resistor side?
- LED **always on**? The resistor is probably still in the **+** rail.
- Upload fails at `Connecting...`? Hold **BOOT** while it connects.

**Next episode:** the other direction — reading a button with `digitalRead`.
