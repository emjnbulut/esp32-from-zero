// ESP32 From Zero - Episode 17: My phone switches a real fan with an ESP32  [DRAFT 2026-11-24]
// A relay is a switch flipped by a tiny electromagnet: the ESP32's weak pin moves a real contact that can switch a
// USB desk fan. The phone page from Episode 12 gets ON / OFF / 10 MIN buttons; the fan switches off by itself when
// the timer runs out. (TODO for the episode: "auto above 28 C" mode with the DHT11 from Episode 13.)
//
// SAFETY: 5 V USB loads only (USB fan, USB lamp). Never mains / wall-socket voltage in this course.
//
// Parts:
//   2-channel relay module: VCC -> VIN (5 V), GND -> GND, IN1 -> GPIO 16   (IN2 -> GPIO 17 for a second load later)
//   USB fan: cut USB cable -> its + wire through relay 1 COM / NO (normally open). Or use a USB "switch" cable.
//   OLED SDA 21 / SCL 22 (Episode 10)
// This relay module is ACTIVE-LOW: IN1 LOW = relay ON (click), HIGH = OFF.
// Libraries: "Adafruit SSD1306" + "Adafruit GFX" (WiFi + WebServer come with the ESP32 core).

#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const char* WIFI_NAME = "PinByPin-ESP32";
const char* WIFI_PASSWORD = "esp32lab";

const int RELAY1 = 16;
const int RELAY_ON = LOW;                    // active-low module
const int RELAY_OFF = HIGH;

WebServer server(80);
Adafruit_SSD1306 screen(128, 64, &Wire, -1);
bool fanOn = false;
unsigned long offAt = 0;                     // 0 = no timer
unsigned long lastDraw = 0;

const char PAGE[] PROGMEM = R"HTML(
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP32 fan</title><style>
body{font-family:sans-serif;background:#0b1220;color:#fff;text-align:center;margin:0;padding:24px}
a{display:block;margin:14px auto;max-width:320px;padding:22px;border-radius:18px;font-size:26px;
  font-weight:bold;color:#fff;text-decoration:none}
</style></head><body><h1>Desk fan</h1>
<a href="/on" style="background:#2fbf71">ON</a>
<a href="/timer" style="background:#3b82f6">ON for 10 min</a>
<a href="/off" style="background:#e5484d">OFF</a>
</body></html>
)HTML";

void show(const char* top, String big) {    // same helper as Episode 10
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

void setFan(bool on) {
  fanOn = on;
  digitalWrite(RELAY1, on ? RELAY_ON : RELAY_OFF);   // click!
}

void sendPage() { server.send(200, "text/html", PAGE); }
void handleOn() { setFan(true); offAt = 0; sendPage(); }
void handleOff() { setFan(false); offAt = 0; sendPage(); }
void handleTimer() { setFan(true); offAt = millis() + 10UL * 60UL * 1000UL; sendPage(); }

void setup() {
  digitalWrite(RELAY1, RELAY_OFF);           // set HIGH *before* pinMode, so the relay doesn't click on at boot
  pinMode(RELAY1, OUTPUT);
  Serial.begin(115200);
  screen.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  WiFi.softAP(WIFI_NAME, WIFI_PASSWORD);      // the board's own Wi-Fi (Episode 12)
  server.on("/", sendPage);
  server.on("/on", handleOn);
  server.on("/off", handleOff);
  server.on("/timer", handleTimer);
  server.begin();
  show(("open " + WiFi.softAPIP().toString()).c_str(), "FAN OFF");
}

void loop() {
  server.handleClient();
  unsigned long now = millis();
  if (offAt && (long)(now - offAt) >= 0) {   // the timer ran out
    setFan(false);
    offAt = 0;
  }
  if (now - lastDraw >= 1000) {              // screen once a second
    lastDraw = now;
    if (!fanOn) show("phone: 192.168.4.1", "FAN OFF");
    else if (offAt) show("fan on, off in", String((offAt - now) / 60000 + 1) + " min");
    else show("phone: 192.168.4.1", "FAN ON");
  }
}
