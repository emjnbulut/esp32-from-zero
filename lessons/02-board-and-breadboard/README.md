# Episode 2 — Meet the Board and the Breadboard

No code today. We learn what the pins on the board are, how a breadboard is wired inside,
and build our first circuit: an LED that lights from the 3.3 V pin.

**You need:** your ESP32 board, a breadboard, 1 LED, 1 × 220 Ω resistor (red-red-brown), 2–3 jumper wires.

## 1. The pins

Your board has **30 or 38 pins**. The order differs between boards, but the printed names are the same.
They fall into three groups:

| Group | Labels | What it is |
|---|---|---|
| Power | `3V3` | 3.3 V output — the ESP32's working voltage |
| Power | `VIN` / `5V` | the 5 V coming from USB |
| Ground | `GND` | 0 V — where the current returns |
| GPIO | `D2`, `D4`, `23`, … | general purpose input/output; `D2` = GPIO **2** in code |

> ⚠️ **Two safety rules**
> 1. Never connect a power pin (`3V3`, `5V`/`VIN`) straight to `GND` with a wire — that's a short circuit.
> 2. Never feed 5 V into a GPIO pin. GPIOs are 3.3 V only.

### Which GPIOs to use

| Kind | GPIOs | Labels | Advice |
|---|---|---|---|
| **Flash** | 6, 7, 8, 9, 10, 11 | `CLK`, `D0`, `D1`, `D2`, `D3`, `CMD` (38-pin boards only) | **Never use** — wired to the flash chip that holds your program |
| **Input only** | 34, 35, 36, 39 | `D34`, `D35`, `VP`, `VN` | Fine for buttons/sensors, can't drive an LED |
| **Strapping** | 0, 2, 5, 12, 15 | | Read at startup to choose the boot mode — avoid while learning |
| **USB serial** | 1 (TX), 3 (RX) | `TX0`, `RX0` | Keep free so uploading and the Serial Monitor work |
| **Safe** ✓ | 4, 13, 14, 16–19, 21–23, 25–27, 32, 33 | | Use these for projects |

Careful on 38-pin boards: the label `D2` there is a **flash** pin (GPIO 9), not GPIO 2 — GPIO 2 is labeled `2`.

## 2. The breadboard

```
   + ────────────────────────────  power rail (whole length connected)
   − ────────────────────────────
     a  ●  ●  ●  ●  ●  ●  ●  ●
     b  ●  ●  ●  ●  ●  ●  ●  ●     each column a–e is connected
     c  ●  ●  ●  ●  ●  ●  ●  ●
     d  ●  ●  ●  ●  ●  ●  ●  ●
     e  ●  ●  ●  ●  ●  ●  ●  ●
        ════════ middle gap ════════  (not connected across)
     f  ●  ●  ●  ●  ●  ●  ●  ●
     …                              each column f–j is connected
     j  ●  ●  ●  ●  ●  ●  ●  ●
   + ────────────────────────────
   − ────────────────────────────
```

- Each **short column of five holes** (a–e, or f–j) is one connection.
- The **middle gap** separates the two halves.
- The **rails** along the edges are connected along their length. On some long breadboards the rail is
  **split in the middle** (a break in the red/blue line) — bridge it with a short wire.
- Classic mistake: both legs of a part in the **same column** → they're shorted together and the part does nothing.

## 3. Board on the breadboard

Press the board in **across the middle gap**, so each pin gets its own column. Press gently and evenly.

- A **narrow** board leaves **one free hole** next to each pin on both sides.
- Many **30-pin** and **38-pin** boards are wider: they leave free holes on **one side only** — put the free side
  where you need most pins, or put two breadboards side by side.

## 4. First circuit: an always-on LED

**Build with the USB cable unplugged.**

```
3V3 ──► 220 Ω ──► LED long leg (+, anode) ── LED short leg (−, cathode) ──► GND
```

1. Jumper wire from **3V3** to the red **+** rail, and from a **GND** pin to the blue **−** rail.
2. Resistor from the **+** rail into a free column.
3. LED **long leg** in that same column, **short leg** in the next column.
4. Wire from the short leg's column to the **−** rail.

Plug in USB — the LED lights. (Current ≈ (3.3 V − 2 V) / 220 Ω ≈ 6 mA: safe for the LED and the board.)

**LED stays dark?** Long leg on the resistor side? Legs in different columns? Rail not split?

Next episode we move one wire to a GPIO pin and blink the LED from code.
