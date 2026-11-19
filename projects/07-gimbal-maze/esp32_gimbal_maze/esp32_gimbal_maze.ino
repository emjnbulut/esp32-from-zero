/*
 * ============================================================================
 *  ESP32 From Zero - Shorts Projesi: 2 Eksenli Gimbal Labirent
 * ============================================================================
 *  Donanım:
 *    - ESP32 DevKit V1 (30 veya 38 pin, ESP-WROOM-32)
 *    - 2x MG90S Metal Dişli Mikro Servo (SG90 ile birebir uyumlu)
 *    - 1x KY-023 2 Eksenli Analog Joystick Modülü
 *    - 1x 470uF Kondansatör (opsiyonel ama 5V hattında tavsiye edilir)
 *
 *  Breadboard Bağlantı Özeti:
 *    [GÜÇ OTOYOLU]
 *      ESP32 VIN (5V)  ---> Breadboard (+) Kırmızı Ray
 *      ESP32 GND       ---> Breadboard (-) Mavi Ray
 *
 *    [GİRİŞ - JOYSTICK (Nazik 3.3V!)]
 *      Joystick GND    ---> Breadboard (-) Mavi Ray
 *      Joystick +5V    ---> ESP32 3V3 pini  (ADC pinlerini korumak için 3.3V!)
 *      Joystick VRx    ---> ESP32 GPIO 34   (Yeşil kablo - Sağ/Sol)
 *      Joystick VRy    ---> ESP32 GPIO 35   (Mavi kablo  - İleri/Geri)
 *      Joystick SW     ---> ESP32 GPIO 25   (Opsiyonel   - Basınca merkezler)
 *
 *    [ÇIKIŞ - SERVOLAR (Güçlü 5V!)]
 *      Servo X (Dış Halka)   : Kırmızı -> (+) Ray | Kahverengi -> (-) Ray | Turuncu -> GPIO 18
 *      Servo Y (İç Labirent) : Kırmızı -> (+) Ray | Kahverengi -> (-) Ray | Sarı    -> GPIO 19
 *
 *  Gerekli Kütüphane:
 *    Arduino IDE -> Library Manager -> "ESP32Servo" (Kevin Harrington)
 * ============================================================================
 */

#include <Arduino.h>
#include <ESP32Servo.h>

// ------------------------- PİN TANIMLARI -------------------------
constexpr int PIN_JOY_X   = 34; // ADC1_CH6 (Sadece giriş, temiz okuma)
constexpr int PIN_JOY_Y   = 35; // ADC1_CH7 (Sadece giriş, temiz okuma)
constexpr int PIN_JOY_SW  = 25; // Opsiyonel buton (takılmazsa sorun çıkarmaz)
constexpr int PIN_SERVO_X = 18; // X Ekseni: Dış Gimbal Halkası (Sağ - Sol)
constexpr int PIN_SERVO_Y = 19; // Y Ekseni: İç Labirent Tablası (İleri - Geri)
constexpr int PIN_LED     = 2;  // ESP32 üzerindeki dahili mavi LED

// ---------------------- HAREKET AYARLARI -------------------------
constexpr int   CENTER_X    = 90;    // X servosu tam yatay açısı (gerekirse 85-95 arası ince ayar yap)
constexpr int   CENTER_Y    = 90;    // Y servosu tam yatay açısı (gerekirse 85-95 arası ince ayar yap)
constexpr int   MAX_TILT    = 24;    // Maksimum eğim (±24°: bilye akıcı yürür, dışarı fırlamaz)
constexpr int   DEADZONE    = 180;   // Joystick merkez ölü bölge (titremeyi keser)
constexpr float SMOOTHING   = 0.16f; // 0.08 = çok yumuşak, 0.25 = çok seri

// Eksenlerden biri ters yöne yatarsa aşağıyı true yapman yeterli:
constexpr bool INVERT_X     = false;
constexpr bool INVERT_Y     = false;

// Açılışta kısa bir "selamlama" hareketi (videoda USB takınca çok şık durur)
constexpr bool STARTUP_WAVE = true;

// MG90S / SG90 darbe genişliği (mikrosaniye)
constexpr int SERVO_MIN_US  = 500;
constexpr int SERVO_MAX_US  = 2400;

// ---------------------- GLOBAL NESNELER --------------------------
Servo servoX;
Servo servoY;

int joyCenterX = 2048;
int joyCenterY = 2048;

float currentAngleX = CENTER_X;
float currentAngleY = CENTER_Y;

unsigned long lastDebugMs = 0;

// Joystick merkezini açılışta otomatik ölçer (ucuz modüllerdeki kaymayı yok eder)
void calibrateJoystickCenter() {
  long sumX = 0;
  long sumY = 0;
  constexpr int SAMPLES = 24;

  for (int i = 0; i < SAMPLES; i++) {
    sumX += analogRead(PIN_JOY_X);
    sumY += analogRead(PIN_JOY_Y);
    delay(8);
  }

  joyCenterX = sumX / SAMPLES;
  joyCenterY = sumY / SAMPLES;

  // Eğer joystick bağlı değilse (floating/uç değer) varsayılan 2048'e dön
  if (joyCenterX < 500 || joyCenterX > 3600) joyCenterX = 2048;
  if (joyCenterY < 500 || joyCenterY > 3600) joyCenterY = 2048;

  Serial.printf("[KALIBRASYON] Joystick Merkezi -> X: %d, Y: %d\n", joyCenterX, joyCenterY);
}

// Çoklu örneklemeli temiz ADC okuması
int readCleanADC(int pin) {
  long total = 0;
  for (int i = 0; i < 4; i++) {
    total += analogRead(pin);
  }
  return total / 4;
}

// Ham joystick değerini güvenli hedef açıya çevirir
float joyToTargetAngle(int raw, int centerRaw, int centerAngle, bool invert) {
  int delta = raw - centerRaw;

  // Ölü bölge içindeyse tam düz dur
  if (abs(delta) < DEADZONE) {
    return (float)centerAngle;
  }

  // Ölü bölgeden sonraki yumuşak ölçekleme
  float norm = 0.0f;
  if (delta > 0) {
    int span = max(1, 4095 - (centerRaw + DEADZONE));
    norm = (float)(delta - DEADZONE) / (float)span;
  } else {
    int span = max(1, (centerRaw - DEADZONE));
    norm = (float)(delta + DEADZONE) / (float)span;
  }

  norm = constrain(norm, -1.0f, 1.0f);
  if (invert) norm = -norm;

  return centerAngle + (norm * MAX_TILT);
}

// Açılışta labirenti nazikçe sağa-sola ve öne-arkaya yatırıp düzler
void runStartupWave() {
  constexpr int WAVE = 12;
  const int steps[][2] = {
    {CENTER_X + WAVE, CENTER_Y},
    {CENTER_X - WAVE, CENTER_Y},
    {CENTER_X,        CENTER_Y + WAVE},
    {CENTER_X,        CENTER_Y - WAVE},
    {CENTER_X,        CENTER_Y}
  };

  for (auto &target : steps) {
    for (int i = 0; i < 16; i++) {
      currentAngleX += (target[0] - currentAngleX) * 0.25f;
      currentAngleY += (target[1] - currentAngleY) * 0.25f;
      servoX.write((int)roundf(currentAngleX));
      servoY.write((int)roundf(currentAngleY));
      delay(18);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("\n=== ESP32 Gimbal Labirent Baslatiliyor ===");

  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_JOY_SW, INPUT_PULLUP);
  digitalWrite(PIN_LED, HIGH);

  // ESP32 ADC 12-bit (0..4095) ve 3.3V tam ölçek
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  // ESP32Servo için donanım PWM zamanlayıcılarını ayır
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);

  servoX.setPeriodHertz(50);
  servoY.setPeriodHertz(50);
  servoX.attach(PIN_SERVO_X, SERVO_MIN_US, SERVO_MAX_US);
  servoY.attach(PIN_SERVO_Y, SERVO_MIN_US, SERVO_MAX_US);

  // Başlangıçta düz konuma geç
  servoX.write(CENTER_X);
  servoY.write(CENTER_Y);
  delay(250);

  // Joystick'i otomatik sıfırla
  calibrateJoystickCenter();

  if (STARTUP_WAVE) {
    runStartupWave();
  }

  digitalWrite(PIN_LED, LOW);
  Serial.println("[HAZIR] Joystick ile labirenti kontrol edebilirsin!");
}

void loop() {
  // Opsiyonel: Joystick tuşuna basılırsa yeniden merkez kalibrasyonu yap
  if (digitalRead(PIN_JOY_SW) == LOW) {
    digitalWrite(PIN_LED, HIGH);
    calibrateJoystickCenter();
    delay(300);
    digitalWrite(PIN_LED, LOW);
  }

  int rawX = readCleanADC(PIN_JOY_X);
  int rawY = readCleanADC(PIN_JOY_Y);

  float targetX = joyToTargetAngle(rawX, joyCenterX, CENTER_X, INVERT_X);
  float targetY = joyToTargetAngle(rawY, joyCenterY, CENTER_Y, INVERT_Y);

  // Üstel yumuşatma filtresi (kamerada ipek gibi pürüzsüz eğim verir)
  currentAngleX += (targetX - currentAngleX) * SMOOTHING;
  currentAngleY += (targetY - currentAngleY) * SMOOTHING;

  int outX = constrain((int)roundf(currentAngleX), CENTER_X - MAX_TILT, CENTER_X + MAX_TILT);
  int outY = constrain((int)roundf(currentAngleY), CENTER_Y - MAX_TILT, CENTER_Y + MAX_TILT);

  servoX.write(outX);
  servoY.write(outY);

  // Seri monitörden canlı takip (isteğe bağlı)
  if (millis() - lastDebugMs >= 250) {
    lastDebugMs = millis();
    Serial.printf("Joy(%4d, %4d) -> ServoX: %3d° | ServoY: %3d°\n", rawX, rawY, outX, outY);
  }

  delay(15); // ~66 Hz kontrol döngüsü
}
