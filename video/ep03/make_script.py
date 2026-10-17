"""Source of video/ep03/script.json (kept as Python so long lines stay readable).
Usage: python video/ep03/make_script.py"""
import json
from pathlib import Path

S = []


def s(id, scene, text, tr, sub=None, **kw):
    d = {"id": id, "scene": scene, "text": text}
    if sub:
        d["sub"] = sub
    d["tr"] = tr
    d.update(kw)
    S.append(d)


# ---- intro
s("s01", "intro", "Welcome back to ESP32 From Zero. Last time, we built our first circuit, and the LED lit up.",
  "ESP32 From Zero'ya tekrar hoş geldiniz. Geçen sefer ilk devremizi kurduk ve LED yandı.")
s("s02", "intro", "But it was always on. Today, our code takes control. We'll move one part, write a short program, and make the LED blink.",
  "Ama hep yanıyordu. Bugün kontrolü kodumuz alıyor. Bir parçayı taşıyacak, kısa bir program yazacak ve LED'i yakıp söndüreceğiz.")
s("s03", "recap", "Here's the circuit from last time. Three V three goes to the resistor, the resistor goes to the LED's long leg, and the short leg goes to ground.",
  "Geçen seferki devre şu: 3V3 dirence gider, direnç LED'in uzun bacağına gider, kısa bacak da toprağa gider.",
  sub="Here's the circuit from last time. 3V3 goes to the resistor, the resistor goes to the LED's long leg, and the short leg goes to ground.")
# ---- why 220 ohms
s("s04", "ohm", "Before we change anything, let's answer a question from last time. Why exactly 220 ohms?",
  "Bir şeyi değiştirmeden önce geçen seferden kalan bir soruyu cevaplayalım. Neden tam olarak 220 ohm?",
  sub="Before we change anything, let's answer a question from last time. Why exactly 220 Ω?")
s("s05", "ohm", "The answer is Ohm's law. The current through a resistor equals the voltage across it, divided by its resistance.",
  "Cevap Ohm yasası. Bir dirençten geçen akım, üzerindeki gerilimin direnç değerine bölümüne eşittir.")
s("s06", "ohm", "A red LED needs about two volts to light. So out of our three point three volts, about one point three volts is left for the resistor.",
  "Kırmızı bir LED'in yanması için yaklaşık 2 volt gerekir. Yani 3,3 voltumuzdan dirence yaklaşık 1,3 volt kalır.",
  sub="A red LED needs about 2 volts to light. So out of our 3.3 volts, about 1.3 volts is left for the resistor.")
s("s07", "ohm", "One point three volts, divided by 220 ohms, is about six milliamps. That's enough to see the LED clearly, and well below what a GPIO pin can supply.",
  "1,3 volt bölü 220 ohm, yaklaşık 6 miliamper eder. Bu, LED'i net görmek için yeterli ve bir GPIO pininin verebileceğinin çok altında.",
  sub="1.3 volts, divided by 220 Ω, is about 6 milliamps. That's enough to see the LED clearly, and well below what a GPIO pin can supply.")
s("s08", "ohm", "Without the resistor, nothing limits the current, and the LED or the pin can burn out. A bigger resistor makes the LED dimmer. Anything from 220 ohms to one kilo ohm works.",
  "Direnç olmadan akımı hiçbir şey sınırlamaz ve LED ya da pin yanabilir. Daha büyük bir direnç LED'i daha sönük yapar. 220 ohm ile 1 kiloohm arası her değer çalışır.",
  sub="Without the resistor, nothing limits the current, and the LED or the pin can burn out. A bigger resistor makes the LED dimmer. Anything from 220 Ω to 1 kΩ works.")
# ---- move the resistor
s("s09", "move", "Now, the change. First, unplug the USB cable. We never rewire a circuit while it's powered.",
  "Şimdi değişiklik. Önce USB kablosunu çıkarın. Bir devreyi elektrik varken asla yeniden bağlamayız.")
s("s10", "move", "Take the red wire out completely. We don't need three V three today. Then pull the resistor's leg out of the plus rail, and push it into hole j sixteen, the column of D twenty-three.",
  "Kırmızı kabloyu tamamen çıkarın; bugün 3V3'e ihtiyacımız yok. Sonra direncin bacağını artı raydan çekin ve D23'ün sütunundaki j16 deliğine takın.",
  sub="Take the red wire out completely. We don't need 3V3 today. Then pull the resistor's leg out of the plus rail, and push it into hole j16, the column of D23.", clip="C1", pad=1.5)
s("s11", "move", "That's GPIO twenty-three, one of the safe pins from last time. On a thirty-eight pin board, it's simply labeled twenty-three.",
  "Bu GPIO 23, geçen seferki güvenli pinlerden biri. 38 pinli bir kartta sadece 23 diye yazar.",
  sub="That's GPIO 23, one of the safe pins from last time. On a 38-pin board, it's simply labeled \"23\".")
s("s12", "move", "Now the LED gets its power from GPIO twenty-three, through the resistor. Plug the USB cable back in. The LED stays dark, because nothing has told that pin to turn on yet.",
  "Artık LED gücünü direnç üzerinden GPIO 23'ten alıyor. USB kablosunu tekrar takın. LED sönük kalıyor, çünkü o pine henüz kimse yanmasını söylemedi.",
  sub="Now the LED gets its power from GPIO 23, through the resistor. Plug the USB cable back in. The LED stays dark, because nothing has told that pin to turn on yet.")
# ---- the code
s("s13", "code", "That's the job of our code. Open the Arduino IDE, and start a new sketch.",
  "Bu, kodumuzun işi. Arduino IDE'yi açın ve yeni bir sketch başlatın.")
s("s14", "code", "First, we give the pin a name. A constant called LED pin, set to twenty-three. If we ever move the LED to another pin, we change just this one line.",
  "Önce pine bir isim veriyoruz. LED_PIN adında bir sabit, değeri 23. LED'i bir gün başka bir pine taşırsak sadece bu satırı değiştiririz.",
  sub="First, we give the pin a name. A constant called LED_PIN, set to 23. If we ever move the LED to another pin, we change just this one line.")
s("s15", "code", "In setup, pin mode tells the ESP32 how we'll use this pin. OUTPUT means our code drives it.",
  "setup içinde pinMode, ESP32'ye bu pini nasıl kullanacağımızı söyler. OUTPUT, pini kodumuzun sürdüğü anlamına gelir.",
  sub="In setup, pinMode tells the ESP32 how we'll use this pin. OUTPUT means our code drives it.")
s("s16", "code", "And like last time, we open the serial connection, so the board can tell us what it's doing.",
  "Geçen seferki gibi seri bağlantıyı da açıyoruz ki kart bize ne yaptığını söyleyebilsin.")
s("s17", "code", "Now the loop. Digital write, LED pin, HIGH. HIGH puts three point three volts on the pin, and the LED lights up.",
  "Şimdi loop. digitalWrite, LED_PIN, HIGH. HIGH pine 3,3 volt verir ve LED yanar.",
  sub="Now the loop. digitalWrite(LED_PIN, HIGH). HIGH puts 3.3 volts on the pin, and the LED lights up.")
s("s18", "code", "We print LED on, and wait five hundred milliseconds. That's half a second.",
  "Ekrana LED on yazdırıp 500 milisaniye bekliyoruz. Bu yarım saniye.",
  sub="We print \"LED on\", and wait 500 milliseconds. That's half a second.")
s("s19", "code", "Then digital write LOW. LOW means zero volts, so the LED goes dark. We print LED off, and wait another half second.",
  "Sonra digitalWrite LOW. LOW sıfır volt demek, yani LED söner. LED off yazdırıp yarım saniye daha bekliyoruz.",
  sub="Then digitalWrite LOW. LOW means 0 volts, so the LED goes dark. We print \"LED off\", and wait another half second.")
s("s20", "code", "And because loop runs forever, it starts again: on, wait, off, wait. One blink every second.",
  "Ve loop sonsuza kadar çalıştığı için baştan başlar: aç, bekle, kapat, bekle. Her saniye bir yanıp sönme.")
# ---- upload and result
s("s21", "upload", "Save the sketch. Check that ESP32 Dev Module and your COM port are still selected, and click Upload.",
  "Sketch'i kaydedin. ESP32 Dev Module ve COM portunuzun hâlâ seçili olduğunu kontrol edin ve Upload'a tıklayın.")
s("s22", "upload", "If it hangs at Connecting, hold the BOOT button, just like in episode one.",
  "Connecting'de takılırsa, birinci bölümdeki gibi BOOT düğmesini basılı tutun.")
s("s23", "upload", "Done uploading. And there it is. Our LED blinks!",
  "Yükleme bitti. İşte oldu. LED'imiz yanıp sönüyor!", clip="C2", pad=2.0)
s("s24", "upload", "Open the Serial Monitor at 115200 baud, and you'll see the board report every change. LED on. LED off.",
  "Serial Monitor'ü 115200 baud'da açın; kartın her değişikliği bildirdiğini göreceksiniz. LED on. LED off.")
s("s25", "wave", "Here's what happens on the pin. Three point three volts, then zero, then three point three again. HIGH and LOW are just names for those two voltages.",
  "Pinde olan şu: 3,3 volt, sonra sıfır, sonra yine 3,3. HIGH ve LOW, bu iki gerilimin sadece isimleri.",
  sub="Here's what happens on the pin. 3.3 volts, then 0, then 3.3 again. HIGH and LOW are just names for those two voltages.")
# ---- play with it
s("s26", "play", "Now play with it. Change both delays to one hundred, and upload again. The LED blinks five times a second.",
  "Şimdi biraz oynayın. İki gecikmeyi de 100 yapın ve tekrar yükleyin. LED saniyede beş kez yanıp söner.",
  sub="Now play with it. Change both delays to 100, and upload again. The LED blinks five times a second.", clip="C3", pad=1.5)
s("s27", "play", "Try a short on time and a long off time, like a lighthouse. You can't break anything by changing the numbers.",
  "Kısa bir yanma ve uzun bir sönme süresi deneyin, bir deniz feneri gibi. Sayıları değiştirerek hiçbir şeyi bozamazsınız.")
s("s28", "trouble", "LED not blinking? Check that the resistor's leg is really in the D twenty-three column, that the code says twenty-three, and that the long leg faces the resistor. If it's always on, the resistor is probably still in the plus rail.",
  "LED yanıp sönmüyor mu? Direncin bacağının gerçekten D23 sütununda olduğunu, kodda 23 yazdığını ve uzun bacağın dirence baktığını kontrol edin. Hep yanıyorsa direnç muhtemelen hâlâ artı rayda.",
  sub="LED not blinking? Check that the resistor's leg is really in the D23 column, that the code says 23, and that the long leg faces the resistor. If it's always on, the resistor is probably still in the plus rail.")
# ---- outro
s("s29", "outro", "Today, we learned why the resistor is there, and we used pin mode, digital write, and delay to blink an LED.",
  "Bugün direncin neden orada olduğunu öğrendik ve bir LED'i yakıp söndürmek için pinMode, digitalWrite ve delay kullandık.",
  sub="Today, we learned why the resistor is there, and we used pinMode, digitalWrite, and delay to blink an LED.")
s("s30", "outro", "Next time, we'll go the other way, and read a button. The code is on GitHub, linked below. See you there!",
  "Gelecek sefer tersini yapacağız ve bir düğmeyi okuyacağız. Kod GitHub'da, bağlantısı aşağıda. Orada görüşmek üzere!")

script = {
    "episode": 3, "title": "Your First Circuit: Blink an LED", "voice": "en-US-EricNeural", "rate": "+5%",
    "clips": {
        "C1": "USB unplugged. Take the red wire out, then move the resistor's leg from the plus rail into hole j16 (the D23 column). Close-up from above, landscape, 6-10 s.",
        "C2": "The LED blinking once per second after the upload (board, breadboard and LED in frame). Landscape, 5-8 s.",
        "C3": "The LED blinking fast (delays set to 100 ms). Landscape, 4-6 s.",
    },
    "segments": S,
}
out = Path(__file__).with_name("script.json")
out.write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
print(out, len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
