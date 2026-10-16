# Episode 1 — Setting Up Your Computer

In this episode we install everything we need and run our first program on the ESP32.

**You need:** an ESP32 development board, a micro USB **data** cable, a Windows PC.

## 1. Install the Arduino IDE

1. Go to <https://www.arduino.cc/en/software>.
2. Under **Arduino IDE 2.3.10** (or newer), select *Windows Win 10 or newer (64-bit)* and click **Download**.
3. If the site asks for a donation, that's optional — click **Just Download**.
4. Run the installer: **I Agree** → *Only for me* (or all users) → **Next** → **Install** → **Finish**.
5. If Windows asks about the firewall or a USB driver from Arduino, click **Allow** / **Install**.

## 2. Add ESP32 support

1. In the IDE, open **File → Preferences**.
2. Paste this into **Additional boards manager URLs** and click **OK**:

   ```
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```

3. Open the **Boards Manager** (second icon on the left), search for `esp32`.
4. Install **esp32 by Espressif Systems** (not *Arduino ESP32 Boards*, which is only for the Arduino Nano ESP32).

## 3. Connect the board and check the driver

1. Plug the board in with a USB cable. Some cables only charge — if nothing is detected, try another cable first.
2. Right-click **Start → Device Manager → Ports (COM & LPT)**.
   - If you see *Silicon Labs CP210x …* or *USB-SERIAL CH340 …* with a COM number, you're done. Note the COM number.
   - If you see an unknown device with a yellow warning sign, install the driver for the chip next to your board's USB connector:

| Chip on your board | Driver | Download |
|---|---|---|
| CP2102 / CP2104 | CP210x Universal Windows Driver (VCP) | <https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers> |
| CH340 / CH341 | CH341SER.EXE | <https://www.wch-ic.com/downloads/CH341SER_EXE.html> |

3. Unplug and replug the board; the COM port should now appear.

## 4. Select the board and port

Click the board dropdown → **Select other board and port…** → search **ESP32 Dev Module** → pick your COM port → **OK**.
The status bar should say `ESP32 Dev Module on COMx`.

## 5. Our first program

Open [`code/hello_esp32/hello_esp32.ino`](code/hello_esp32/hello_esp32.ino) or type it in:

```c
int seconds = 0;

void setup() {
  Serial.begin(115200);   // open the USB text channel at 115200 baud
  delay(1000);            // give the Serial Monitor a moment to connect
  Serial.println("Hello, ESP32!");
}

void loop() {
  seconds = seconds + 1;
  Serial.printf("I have been running for %d seconds\n", seconds);
  delay(1000);            // wait one second
}
```

**Where is `main()`?** Arduino writes it for you. Roughly:

```c
int main(void) {
  setup();          // once, at power-on
  while (1) {
    loop();         // forever
  }
}
```

Click **Upload** (→). When it finishes with `Hard resetting via RTS pin...`, open the **Serial Monitor** (🔍 top right) and set it to **115200 baud**.

## Troubleshooting

| Problem | Fix |
|---|---|
| No COM port | Try a different (data) cable, then install the driver |
| Stuck at `Connecting.....` | Hold the **BOOT** button until the percentages start |
| Strange characters in the Serial Monitor | Baud rate must match `Serial.begin(115200)` |

Tested with Arduino IDE 2.3.10 and esp32 core 3.3.12 (compiles to 269,120 bytes).
