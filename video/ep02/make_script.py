"""Source of video/ep02/script.json (kept as Python so long lines stay readable).
Usage: python video/ep02/make_script.py"""
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


s("s01", "intro", "Welcome back to ESP32 From Zero. Last time, we set up the computer, and ran our first program.",
  "ESP32 From Zero'ya tekrar hoş geldiniz. Geçen sefer bilgisayarı hazırladık ve ilk programımızı çalıştırdık.")
s("s02", "intro", "Today, we leave the screen, and work with our hands. We'll meet the pins, learn how a breadboard works, and build our first circuit.",
  "Bugün ekrandan ayrılıp ellerimizle çalışıyoruz. Pinleri tanıyacak, breadboard'un nasıl çalıştığını öğrenecek ve ilk devremizi kuracağız.")
s("s03", "kit", "Here's what you need. Your ESP32 board, a breadboard, one LED, one 220 ohm resistor, and two or three jumper wires. All of them are in a typical starter kit.",
  "İhtiyacınız olanlar: ESP32 kartınız, bir breadboard, bir LED, bir 220 ohm direnç ve iki üç jumper kablo. Hepsi tipik bir başlangıç setinde var.",
  sub="Here's what you need. Your ESP32 board, a breadboard, one LED, one 220 Ω resistor, and two or three jumper wires. All of them are in a typical starter kit.")
s("s04", "pins", "Let's start with the board. Along both long edges, there's a row of pins. They are the ESP32's connections to the outside world.",
  "Kartla başlayalım. İki uzun kenar boyunca birer sıra pin var. Bunlar ESP32'nin dış dünyayla bağlantıları.")
s("s05", "pins", "Look closely at your board. Next to every pin, there's a tiny printed label. That label is the pin's name.",
  "Kartınıza yakından bakın. Her pinin yanında minik bir yazı var. O yazı pinin adı.", clip="C1", pad=1.2)
s("s06", "pins", "Your board has thirty, or thirty-eight pins. The order is a little different, but the same names appear on both.",
  "Kartınızda otuz ya da otuz sekiz pin var. Sıralama biraz farklı ama iki kartta da aynı isimler var.")
s("s07", "pins", "The pins fall into three groups: power pins, ground pins, and GPIO pins. GPIO means general purpose input and output.",
  "Pinler üç gruba ayrılır: güç pinleri, toprak pinleri ve GPIO pinleri. GPIO, genel amaçlı giriş çıkış demek.")
s("s08", "power", "First, power. The pin labeled three V three gives out three point three volts. That's the voltage the ESP32 works with.",
  "Önce güç. 3V3 yazan pin 3,3 volt verir. ESP32'nin çalıştığı gerilim budur.",
  sub="First, power. The pin labeled 3V3 gives out 3.3 volts. That's the voltage the ESP32 works with.")
s("s09", "power", "The pin labeled VIN, or five V, is connected to the five volts that come from USB.",
  "VIN ya da 5V yazan pin, USB'den gelen 5 volta bağlıdır.",
  sub="The pin labeled VIN, or 5V, is connected to the 5 volts that come from USB.")
s("s10", "power", "And GND means ground. Zero volts. Every circuit needs a path back to ground. That's where the current returns.",
  "GND ise toprak demek. Sıfır volt. Her devrenin toprağa dönen bir yolu olmalı. Akım oradan geri döner.")
s("s11", "power", "Two safety rules. Never connect a power pin straight to ground with a wire. That's a short circuit, and it can damage your board, or even your USB port.",
  "İki güvenlik kuralı. Bir güç pinini asla doğrudan bir kabloyla toprağa bağlamayın. Bu kısa devredir ve kartınıza, hatta USB portunuza zarar verebilir.")
s("s12", "power", "And never feed five volts into a GPIO pin. They are made for three point three volts only.",
  "Ve bir GPIO pinine asla 5 volt vermeyin. Onlar yalnızca 3,3 volt için yapılmıştır.",
  sub="And never feed 5 volts into a GPIO pin. They are made for 3.3 volts only.")
s("s13", "gpio", "Now, the GPIO pins. In code, we use their numbers. On a thirty pin board, D two simply means GPIO two. Thirty-eight pin boards print just the number, two.",
  "Şimdi GPIO pinleri. Kodda onların numaralarını kullanırız. 30 pinli bir kartta D2, basitçe GPIO 2 demek. 38 pinli kartlarda sadece numara yazar: 2.",
  sub="Now, the GPIO pins. In code, we use their numbers. On a 30-pin board, \"D2\" simply means GPIO 2. 38-pin boards print just the number: \"2\".")
s("s14", "gpio", "Most of them can be an input, or an output. But a few are special. As a beginner, it's best to leave them alone.",
  "Çoğu giriş ya da çıkış olabilir. Ama birkaçı özel. Yeni başlarken onlara dokunmamak en iyisi.")
s("s15", "gpio", "GPIO six to eleven connect to the flash memory, where your program is stored. Never use them. On thirty-eight pin boards, they're labeled C L K, C M D, and D zero to D three.",
  "GPIO 6 ile 11 arası, programınızın saklandığı flash belleğe bağlı. Onları asla kullanmayın. 38 pinli kartlarda CLK, CMD ve D0 ile D3 arası diye yazar.",
  sub="GPIO 6 to 11 connect to the flash memory, where your program is stored. Never use them. On 38-pin boards, they're labeled CLK, CMD, and D0 to D3.")
s("s16", "gpio", "GPIO thirty-four, thirty-five, thirty-six, and thirty-nine are input only. They can read a sensor, but they can't light an LED. Thirty-six and thirty-nine are labeled V P and V N.",
  "GPIO 34, 35, 36 ve 39 yalnızca giriştir. Bir sensörü okuyabilirler ama LED yakamazlar. 36 ve 39, VP ve VN diye yazılır.",
  sub="GPIO 34, 35, 36 and 39 are input only. They can read a sensor, but they can't light an LED. 36 and 39 are labeled VP and VN.")
s("s17", "gpio", "GPIO zero, two, five, twelve, and fifteen are strapping pins. The chip reads them at startup, to decide how to boot. Connect the wrong thing, and the board may not start.",
  "GPIO 0, 2, 5, 12 ve 15 strapping pinleridir. Çip, nasıl açılacağına karar vermek için onları başlangıçta okur. Yanlış bir şey bağlarsanız kart açılmayabilir.",
  sub="GPIO 0, 2, 5, 12 and 15 are strapping pins. The chip reads them at startup, to decide how to boot. Connect the wrong thing, and the board may not start.")
s("s18", "gpio", "And T X and R X carry the USB serial connection. Keep them free, so uploading and the Serial Monitor keep working.",
  "TX ve RX de USB seri bağlantısını taşır. Yükleme ve Serial Monitor çalışmaya devam etsin diye onları boş bırakın.",
  sub="And TX and RX carry the USB serial connection. Keep them free, so uploading and the Serial Monitor keep working.")
s("s19", "gpio", "That still leaves plenty of safe pins. These green ones are the pins we'll use in our projects.",
  "Yine de bolca güvenli pin kalıyor. Bu yeşil olanlar, projelerimizde kullanacağımız pinler.", pad=1.0)
s("s20", "bb", "Now, the breadboard. It lets us build circuits without soldering. We just push the wires and parts into the holes.",
  "Şimdi breadboard. Lehim yapmadan devre kurmamızı sağlar. Kabloları ve parçaları deliklere takmamız yeterli.")
s("s21", "bb", "Under the holes, there are metal strips. In the middle area, each short column of five holes is connected together. A to E is one group, and F to J is another.",
  "Deliklerin altında metal şeritler var. Orta bölgede, beş delikten oluşan her kısa sütun birbirine bağlı. A'dan E'ye bir grup, F'den J'ye başka bir grup.",
  sub="Under the holes, there are metal strips. In the middle area, each short column of five holes is connected together. a to e is one group, and f to j is another.")
s("s22", "bb", "The gap down the middle separates the two halves. Holes on opposite sides of the gap are not connected.",
  "Ortadaki boşluk iki yarıyı ayırır. Boşluğun iki yanındaki delikler birbirine bağlı değildir.")
s("s23", "bb", "Along the long edges are the power rails, marked with a red plus, and a blue minus. Each rail is connected along its whole length. We use them to share power and ground.",
  "Uzun kenarlar boyunca güç rayları var; kırmızı artı ve mavi eksi ile işaretli. Her ray boydan boya bağlıdır. Onları gücü ve toprağı paylaştırmak için kullanırız.")
s("s24", "bb", "On some long breadboards, the rails are split in the middle. If the red line has a break, join the two halves with a short wire.",
  "Bazı uzun breadboard'larda raylar ortadan bölünmüştür. Kırmızı çizgide bir kesinti varsa iki yarıyı kısa bir kabloyla birleştirin.")
s("s25", "bb", "And here's the most common beginner mistake: putting both legs of a part in the same column. Both legs are then connected together, and the part does nothing.",
  "En sık yapılan acemi hatası da şu: bir parçanın iki bacağını aynı sütuna takmak. O zaman iki bacak birbirine bağlanır ve parça hiçbir işe yaramaz.")
s("s26", "mount", "Now, let's put the board on the breadboard. It sits across the middle gap, so that every pin gets its own column.",
  "Şimdi kartı breadboard'a takalım. Kart ortadaki boşluğun üzerine oturur, böylece her pin kendi sütununu alır.")
s("s27", "mount", "Line up the pins with the holes, and press down gently and evenly, on both sides.",
  "Pinleri deliklerle hizalayın ve iki taraftan da nazikçe ve eşit şekilde bastırın.", clip="C2", pad=1.5)
s("s28", "mount", "Most ESP32 boards are wide. A narrow board leaves one free hole next to each pin, on both sides. But many boards, with thirty or thirty-eight pins, leave free holes on one side only.",
  "ESP32 kartlarının çoğu geniştir. Dar bir kart, iki tarafta da her pinin yanında bir boş delik bırakır. Ama 30 ya da 38 pinli birçok kart, yalnızca bir tarafta boş delik bırakır.",
  sub="Most ESP32 boards are wide. A narrow board leaves one free hole next to each pin, on both sides. But many boards, with 30 or 38 pins, leave free holes on one side only.")
s("s29", "mount", "That's enough for today. Later, when we need more room, we can use two breadboards side by side.",
  "Bugün için bu yeterli. İleride daha fazla yere ihtiyacımız olunca iki breadboard'u yan yana kullanabiliriz.")
s("s30", "circuit", "Time for our first circuit. We'll light an LED, using power from the three point three volt pin. No code needed.",
  "İlk devremizin zamanı. 3,3 volt pininden aldığımız güçle bir LED yakacağız. Kod gerekmiyor.",
  sub="Time for our first circuit. We'll light an LED, using power from the 3.3 volt pin. No code needed.")
s("s31", "circuit", "An LED has two legs. The long leg is the plus side, called the anode. The short leg is the minus side, the cathode. Current must flow from the long leg to the short one.",
  "LED'in iki bacağı var. Uzun bacak artı taraf, yani anot. Kısa bacak eksi taraf, yani katot. Akım uzun bacaktan kısa bacağa doğru akmalı.")
s("s32", "circuit", "On its own, the LED would pull too much current, and burn out. So we add a resistor to limit it. 220 ohms is a good value. Its color bands are red, red, brown.",
  "Tek başına LED çok fazla akım çeker ve yanar. Bu yüzden akımı sınırlamak için bir direnç ekleriz. 220 ohm iyi bir değer. Renk bantları kırmızı, kırmızı, kahverengi.",
  sub="On its own, the LED would pull too much current, and burn out. So we add a resistor to limit it. 220 Ω is a good value. Its color bands are red, red, brown.")
s("s33", "circuit", "Here's the plan. Three V three goes to the resistor. The resistor goes to the LED's long leg. And the short leg goes to ground.",
  "Plan şu: 3V3 dirence gider. Direnç LED'in uzun bacağına gider. Kısa bacak da toprağa gider.",
  sub="Here's the plan. 3V3 goes to the resistor. The resistor goes to the LED's long leg. And the short leg goes to ground.")
s("s34", "build", "Always build with the USB cable unplugged. Step one: a jumper wire from the three V three pin to the red plus rail, and one from a GND pin to the blue minus rail.",
  "Devreyi her zaman USB kablosu takılı değilken kurun. Birinci adım: 3V3 pininden kırmızı artı raya bir jumper kablo, bir GND pininden de mavi eksi raya bir kablo.",
  sub="Always build with the USB cable unplugged. Step one: a jumper wire from the 3V3 pin to the red plus rail, and one from a GND pin to the blue minus rail.")
s("s35", "build", "Step two: the resistor goes from the plus rail into a free column.",
  "İkinci adım: direnç artı raydan boş bir sütuna takılır.")
s("s36", "build", "Step three: the LED's long leg goes in that same column. The short leg goes in the next column.",
  "Üçüncü adım: LED'in uzun bacağı aynı sütuna takılır. Kısa bacak bir sonraki sütuna.")
s("s37", "build", "Step four: a wire from the short leg's column, to the minus rail. That closes the loop.",
  "Dördüncü adım: kısa bacağın sütunundan eksi raya bir kablo. Bu, döngüyü kapatır.")
s("s38", "build", "Now, plug in the USB cable. And the LED lights up! Current flows out of three V three, through the resistor and the LED, and back to ground.",
  "Şimdi USB kablosunu takın. Ve LED yanıyor! Akım 3V3'ten çıkıp direnç ve LED'den geçerek toprağa geri dönüyor.",
  sub="Now, plug in the USB cable. And the LED lights up! Current flows out of 3V3, through the resistor and the LED, and back to ground.", clip="C3", pad=1.5)
s("s39", "build", "LED stays dark? Check that the long leg is on the resistor side, that the two legs are in different columns, and that the rail isn't split.",
  "LED yanmıyor mu? Uzun bacağın direnç tarafında olduğunu, iki bacağın farklı sütunlarda olduğunu ve rayın bölünmüş olmadığını kontrol edin.")
s("s40", "outro", "Today, we met the power pins, the safe GPIO pins, and the breadboard. And we built our first circuit.",
  "Bugün güç pinlerini, güvenli GPIO pinlerini ve breadboard'u tanıdık. Ve ilk devremizi kurduk.")
s("s41", "outro", "But this LED is always on. Next time, we'll move one wire to a GPIO pin, and blink the LED from our code. The diagrams are on GitHub, linked below. See you there!",
  "Ama bu LED hep yanıyor. Gelecek sefer bir kabloyu bir GPIO pinine taşıyacak ve LED'i kodumuzla yakıp söndüreceğiz. Şemalar GitHub'da, bağlantısı aşağıda. Orada görüşmek üzere!")

script = {
    "episode": 2, "title": "Meet the Board and the Breadboard", "voice": "en-US-EricNeural", "rate": "+5%",
    "clips": {
        "C1": "Close-up of the board's pin labels (3V3, GND, D2...). Slowly pan along one header so the tiny printed names are readable. Landscape, 5-8 s.",
        "C2": "Hands pressing the ESP32 board into the breadboard across the middle gap, pressing evenly on both sides. Landscape, 5-8 s.",
        "C3": "The finished circuit (3V3 -> resistor -> LED -> GND). Plug in the USB cable and the LED turns on. Landscape, 5-8 s.",
    },
    "segments": S,
}
out = Path(__file__).with_name("script.json")
out.write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
print(out, len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
