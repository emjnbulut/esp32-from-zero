"""Source of video/ep04/script.json (kept as Python so long lines stay readable).
Usage: python video/ep04/make_script.py"""
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
s("s01", "intro", "Welcome back to ESP32 From Zero. Last time, our code switched an LED on and off. The ESP32 was talking to the world.",
  "ESP32 From Zero'ya tekrar hoş geldiniz. Geçen sefer kodumuz bir LED'i yakıp söndürdü. ESP32 dünyaya konuşuyordu.")
s("s02", "intro", "Today, it listens. We'll wire up a push button, read it with digital read, and use it to control the LED. Then we'll teach the ESP32 to do two things at once.",
  "Bugün dinliyor. Bir buton bağlayacak, onu digitalRead ile okuyacak ve LED'i onunla kontrol edeceğiz. Sonra ESP32'ye aynı anda iki iş yapmayı öğreteceğiz.",
  sub="Today, it listens. We'll wire up a push button, read it with digitalRead, and use it to control the LED. Then we'll teach the ESP32 to do two things at once.")
# ---- the push button
s("s03", "button", "This is the push button from the kit. It has four legs, but inside, it's just a simple switch.",
  "Bu, setteki buton. Dört bacağı var ama içinde basit bir anahtardan ibaret.")
s("s04", "button", "The two legs on the left are always connected to each other, and so are the two on the right.",
  "Soldaki iki bacak her zaman birbirine bağlıdır, sağdaki iki bacak da öyle.")
s("s05", "button", "When you press the button, a little metal plate connects the left side to the right side. Let go, and they're apart again.",
  "Butona bastığınızda küçük bir metal plaka sol tarafı sağ tarafa bağlar. Bırakınca yine ayrılırlar.")
# ---- wiring
s("s06", "wire", "Here's our circuit from last time, with the LED on GPIO twenty-three. As always, unplug the USB cable first.",
  "Geçen seferki devremiz burada, LED GPIO 23'te. Her zamanki gibi önce USB kablosunu çıkarın.",
  sub="Here's our circuit from last time, with the LED on GPIO 23. As always, unplug the USB cable first.")
s("s07", "wire", "Press the button into the breadboard across the middle gap, at columns twenty-five to twenty-seven.",
  "Butonu breadboard'a, ortadaki boşluğun üzerine, 25 ile 27. sütunlar arasına takın.",
  sub="Press the button into the breadboard across the middle gap, at columns 25 to 27.", clip="C1", pad=1.0)
s("s08", "wire", "A yellow wire goes from D twenty-two to the button's left side. A black wire goes from its right side to the minus rail, which is ground.",
  "Sarı bir kablo D22'den butonun sol tarafına gider. Siyah bir kablo da sağ tarafından eksi raya, yani toprağa gider.",
  sub="A yellow wire goes from D22 to the button's left side. A black wire goes from its right side to the minus rail, which is ground.")
s("s09", "wire", "So when you press the button, GPIO twenty-two is connected straight to ground. That's all the wiring we need.",
  "Yani butona bastığınızda GPIO 22 doğrudan toprağa bağlanır. İhtiyacımız olan bağlantı bu kadar.",
  sub="So when you press the button, GPIO 22 is connected straight to ground. That's all the wiring we need.")
# ---- floating pin and pull-ups
s("s10", "float", "Pressed, the pin is at zero volts. But what about when it's not pressed? Then the pin is connected to nothing at all.",
  "Basılıyken pin sıfır volttadır. Peki basılı değilken? O zaman pin hiçbir şeye bağlı değildir.")
s("s11", "float", "A pin connected to nothing is called floating. It picks up noise from the air, even from your hand, and reads random highs and lows.",
  "Hiçbir şeye bağlı olmayan pine boşta, yani floating denir. Havadan, hatta elinizden parazit toplar ve rastgele HIGH ve LOW okur.")
s("s12", "float", "The fix is a resistor that gently pulls the pin to a known level. A pull-up resistor pulls it up to three point three volts.",
  "Çözüm, pini bilinen bir seviyeye hafifçe çeken bir dirençtir. Pull-up direnci pini 3,3 volta çeker.",
  sub="The fix is a resistor that gently pulls the pin to a known level. A pull-up resistor pulls it up to 3.3 volts.")
s("s13", "float", "Now, not pressed, the pin reads HIGH. Pressed, the button wins, because it connects the pin straight to ground. The pin reads LOW.",
  "Artık basılı değilken pin HIGH okur. Basılıyken buton kazanır, çünkü pini doğrudan toprağa bağlar. Pin LOW okur.")
s("s14", "float", "A pull-down resistor does the opposite. You'd put a ten kilo ohm resistor from the pin to ground, and wire the button to three point three volts. Then pressed reads HIGH.",
  "Pull-down direnci bunun tersini yapar. Pinden toprağa 10 kiloohm'luk bir direnç koyar, butonu da 3,3 volta bağlarsınız. O zaman basılıyken HIGH okunur.",
  sub="A pull-down resistor does the opposite. You'd put a 10 kΩ resistor from the pin to ground, and wire the button to 3.3 volts. Then pressed reads HIGH.")
s("s15", "float", "Both work. But the good news is: the ESP32 has pull-up resistors built in. We don't need an extra part. We just switch one on in code.",
  "İkisi de çalışır. Ama iyi haber şu: ESP32'nin içinde hazır pull-up dirençleri var. Ekstra parçaya gerek yok. Kodda birini açmamız yeterli.")
# ---- the code
s("s15b", "float", "How strong is that built-in pull-up? About forty-five kilo ohms. Weak enough that the button easily wins, and strong enough to hold the pin steady.",
  "Bu dahili pull-up ne kadar güçlü? Yaklaşık 45 kiloohm. Butonun kolayca kazanacağı kadar zayıf, pini sabit tutacak kadar da güçlü.",
  sub="How strong is that built-in pull-up? About 45 kΩ. Weak enough that the button easily wins, and strong enough to hold the pin steady.")
s("s16", "code", "Plug the USB cable back in, and start a new sketch. We name both pins. The button is on twenty-two, the LED on twenty-three.",
  "USB kablosunu tekrar takın ve yeni bir sketch başlatın. İki pine de isim veriyoruz. Buton 22'de, LED 23'te.",
  sub="Plug the USB cable back in, and start a new sketch. We name both pins. The button is on 22, the LED on 23.")
s("s17", "code", "In setup, the button pin gets pin mode INPUT pull up. INPUT means we read the pin, and pull up switches on the built-in resistor.",
  "setup içinde buton pinine pinMode INPUT_PULLUP veriyoruz. INPUT pini okuyacağımız anlamına gelir, PULLUP da dahili direnci açar.",
  sub="In setup, the button pin gets pinMode INPUT_PULLUP. INPUT means we read the pin, and PULLUP switches on the built-in resistor.")
s("s18", "code", "The LED pin is an OUTPUT, like last time, and we open the serial connection.",
  "LED pini geçen seferki gibi OUTPUT ve seri bağlantıyı açıyoruz.")
s("s19", "code", "In the loop, digital read gives us the pin's state, HIGH or LOW. We store it in a variable called state, and print it.",
  "loop içinde digitalRead bize pinin durumunu verir, HIGH ya da LOW. Onu state adlı bir değişkende tutup ekrana yazdırıyoruz.",
  sub="In the loop, digitalRead gives us the pin's state, HIGH or LOW. We store it in a variable called state, and print it.")
s("s20", "code", "If state is LOW, the button is pressed, so we turn the LED on. Otherwise, we turn it off. A short delay, and the loop starts again.",
  "state LOW ise buton basılıdır, LED'i yakıyoruz. Değilse söndürüyoruz. Kısa bir bekleme ve loop baştan başlar.",
  sub="If state is LOW, the button is pressed, so we turn the LED on. Otherwise, we turn it off. A short delay, and the loop starts again.")
# ---- upload and try it
s("s21", "upload", "Save it as button LED, and click Upload. Then open the Serial Monitor at 115200 baud.",
  "button_led adıyla kaydedin ve Upload'a tıklayın. Sonra Serial Monitor'ü 115200 baud'da açın.",
  sub="Save it as button_led, and click Upload. Then open the Serial Monitor at 115200 baud.")
s("s22", "upload", "Not pressed, it prints one, which is HIGH. Press the button, and it prints zero, and the LED lights up. Let go, and it's off again.",
  "Basılı değilken 1 yazar, yani HIGH. Butona basın; 0 yazar ve LED yanar. Bırakın, yine söner.",
  sub="Not pressed, it prints 1, which is HIGH. Press the button, and it prints 0, and the LED lights up. Let go, and it's off again.",
  clip="C2", pad=2.0)
s("s23", "upload", "Want to see a floating pin with your own eyes? Change INPUT pull up to plain INPUT, and upload again.",
  "Boşta kalan bir pini kendi gözünüzle görmek ister misiniz? INPUT_PULLUP'ı düz INPUT yapın ve tekrar yükleyin.",
  sub="Want to see a floating pin with your own eyes? Change INPUT_PULLUP to plain INPUT, and upload again.")
s("s24", "upload", "Now nothing holds the pin. Touch the yellow wire, or just move your hand near it, and the numbers jump around. Change it back, and it's calm again.",
  "Artık pini hiçbir şey tutmuyor. Sarı kabloya dokunun ya da elinizi yaklaştırın; sayılar rastgele zıplar. Geri değiştirin, yine sakinleşir.")
# ---- toggle and bounce
s("s25", "toggle", "Now a classic upgrade. Instead of holding the button, let's press once for on, and once more for off.",
  "Şimdi klasik bir geliştirme. Butonu basılı tutmak yerine bir basışta açılsın, bir daha basınca kapansın.")
s("s26", "toggle", "We remember the last state. When the state changes, and it's now LOW, that's a new press, so we flip the LED.",
  "Son durumu hatırlıyoruz. Durum değiştiyse ve şimdi LOW ise bu yeni bir basıştır ve LED'i tersine çeviriyoruz.")
s("s26b", "toggle", "Think of it as a timeline. HIGH, HIGH, HIGH, then LOW. That one moment, where HIGH turns into LOW, is the press. It's called an edge.",
  "Bunu bir zaman çizelgesi gibi düşünün. HIGH, HIGH, HIGH, sonra LOW. HIGH'ın LOW'a döndüğü o tek an basıştır. Buna kenar, yani edge denir.")
s("s26c", "toggle", "To flip the LED, we keep a bool, which is true or false. The exclamation mark means not, so LED on equals not LED on swaps it. And the question mark picks HIGH when LED on is true, and LOW when it's not.",
  "LED'i çevirmek için true ya da false olan bir bool tutuyoruz. Ünlem işareti değil anlamına gelir; ledOn = !ledOn onu tersine çevirir. Soru işareti de ledOn true ise HIGH'ı, değilse LOW'u seçer.",
  sub="To flip the LED, we keep a bool, which is true or false. The exclamation mark means \"not\", so ledOn = !ledOn swaps it. And the question mark picks HIGH when ledOn is true, and LOW when it's not.")
s("s27", "toggle", "Let's also count the presses, and print the count. Press once, and sometimes the count jumps by two, or even three.",
  "Basışları sayıp sayıyı da yazdıralım. Bir kez basın; sayı bazen iki, hatta üç birden artar.")
s("s28", "toggle", "That's bouncing. When metal contacts touch, they bounce for a few milliseconds. To the ESP32, which checks the pin hundreds of thousands of times a second, one press can look like five.",
  "Buna sekme denir. Metal kontaklar birbirine değdiğinde birkaç milisaniye sekerler. Pini saniyede yüz binlerce kez kontrol eden ESP32 için tek bir basış beş basış gibi görünebilir.")
s("s29", "toggle", "The simple fix is called debouncing. After every change, pressed or released, we wait fifty milliseconds, until the bouncing is over.",
  "Basit çözümün adı debounce. Her değişiklikten sonra, basınca da bırakınca da, sekme bitene kadar 50 milisaniye bekliyoruz.",
  sub="The simple fix is called debouncing. After every change, pressed or released, we wait 50 milliseconds, until the bouncing is over.")
s("s30", "toggle", "Now every press counts exactly once, and flips the LED exactly once. This sketch is on GitHub as button toggle.",
  "Artık her basış tam bir kez sayılıyor ve LED'i tam bir kez çeviriyor. Bu sketch GitHub'da button_toggle adıyla duruyor.",
  sub="Now every press counts exactly once, and flips the LED exactly once. This sketch is on GitHub as button_toggle.", clip="C3", pad=1.5)
# ---- two things at once: why delay blocks
s("s31", "block", "Now, part two. Let's bring back the blinking from last episode, and let the button switch the blinking on and off.",
  "Şimdi ikinci kısım. Geçen bölümdeki yanıp sönmeyi geri getirelim ve butonun yanıp sönmeyi açıp kapatmasını sağlayalım.")
s("s32", "block", "The obvious way: blink with delay, and read the button in the same loop. But delay freezes everything. While it waits, the ESP32 doesn't look at the button at all.",
  "Akla gelen ilk yol: delay ile yakıp söndürmek ve butonu aynı loop'ta okumak. Ama delay her şeyi dondurur. Beklerken ESP32 butona hiç bakmaz.")
s("s33", "block", "Press during a delay, and the press is simply missed. You'd have to hold the button until the loop comes around again.",
  "Bir delay sırasında basarsanız basış kaybolur. Loop tekrar dönene kadar butonu basılı tutmanız gerekirdi.")
# ---- millis
s("s33b", "block", "You could try shorter delays, but then the blinking gets messy, and presses still slip through. The real fix is a different way of thinking.",
  "Daha kısa delay'ler deneyebilirsiniz ama o zaman yanıp sönme bozulur ve basışlar yine kaçar. Asıl çözüm farklı bir düşünme biçimi.")
s("s34", "millis", "The fix: never wait. Instead, look at the clock. millis gives the number of milliseconds since the board started.",
  "Çözüm: hiç beklememek. Onun yerine saate bakarız. millis, kart açıldığından beri geçen milisaniye sayısını verir.",
  sub="The fix: never wait. Instead, look at the clock. millis() gives the number of milliseconds since the board started.")
s("s34b", "millis", "Print millis in the loop, and you'll see it count: one thousand, two thousand, a thousand more every second, all by itself, while your code does other things.",
  "millis'i loop'ta yazdırırsanız saydığını görürsünüz: bin, iki bin; kodunuz başka işler yaparken kendi kendine her saniye bin artar.",
  sub="Print millis() in the loop, and you'll see it count: 1000, 2000, a thousand more every second, all by itself, while your code does other things.")
s("s35", "millis", "We remember when the LED last changed. In every loop, we ask: have five hundred milliseconds passed since then? If yes, we flip the LED, and note the time. If not, we just move on.",
  "LED'in en son ne zaman değiştiğini hatırlıyoruz. Her loop'ta soruyoruz: o zamandan beri 500 milisaniye geçti mi? Geçtiyse LED'i çeviriyor ve zamanı not ediyoruz. Geçmediyse devam ediyoruz.",
  sub="We remember when the LED last changed. In every loop, we ask: have 500 milliseconds passed since then? If yes, we flip the LED, and note the time. If not, we just move on.")
s("s35b", "millis", "An example. The LED last changed at seven hundred. Now it's one thousand. One thousand minus seven hundred is three hundred: not yet. Later, now is twelve hundred. Twelve hundred minus seven hundred is five hundred: flip, and the last time becomes twelve hundred.",
  "Bir örnek. LED en son 700'de değişti. Şimdi 1000. 1000 eksi 700, 300 eder: henüz değil. Biraz sonra şimdi 1200. 1200 eksi 700, 500 eder: çevir ve son zaman 1200 olsun.",
  sub="An example. The LED last changed at 700. Now it's 1000. 1000 minus 700 is 300: not yet. Later, now is 1200. 1200 minus 700 is 500: flip, and the last time becomes 1200.")
s("s36", "millis", "Times live in a type called unsigned long, a big whole number that can't go negative. And we always subtract: now, minus the last time.",
  "Zamanlar unsigned long adlı bir tipte tutulur; negatif olamayan büyük bir tam sayı. Ve her zaman çıkarma yaparız: şimdi eksi son zaman.")
s("s37", "millis", "Why subtract? After about forty-nine days, millis rolls over to zero. With subtraction, the math still works out. With other tricks, it doesn't.",
  "Neden çıkarma? Yaklaşık 49 günde bir millis sıfıra döner. Çıkarma yaparsanız hesap yine doğru çıkar. Başka yöntemlerle çıkmaz.",
  sub="Why subtract? After about 49 days, millis() rolls over to zero. With subtraction, the math still works out. With other tricks, it doesn't.")
s("s38", "millis", "The button uses the same trick. Instead of a delay for debouncing, we ignore changes that come less than fifty milliseconds after the last one.",
  "Buton da aynı yöntemi kullanıyor. Debounce için delay yerine, bir öncekinden sonraki 50 milisaniye içinde gelen değişiklikleri yok sayıyoruz.",
  sub="The button uses the same trick. Instead of a delay for debouncing, we ignore changes that come less than 50 milliseconds after the last one.")
s("s39", "millis", "Now the loop never waits. It runs thousands of times a second, and every time, it checks the button and the clock.",
  "Artık loop hiç beklemiyor. Saniyede binlerce kez dönüyor ve her seferinde butonu ve saati kontrol ediyor.")
s("s40", "millis", "Upload it. The LED blinks, and the moment you press the button, it stops. Press again, and it blinks again. Two things at once.",
  "Yükleyin. LED yanıp sönüyor ve butona bastığınız anda duruyor. Tekrar basın, yeniden yanıp sönüyor. Aynı anda iki iş.",
  clip="C4", pad=2.0)
# ---- a second LED
s("s41", "green", "And this scales. Let's add a second LED, a green one, that blinks at its own speed.",
  "Ve bu yöntem büyür. İkinci bir LED ekleyelim; kendi hızında yanıp sönen yeşil bir LED.")
s("s42", "green", "Unplug the USB cable. This time we use the top half of the breadboard. A green wire goes from D twenty-five to column eighteen, and a 220 ohm resistor from there to column twenty-one.",
  "USB kablosunu çıkarın. Bu sefer breadboard'un üst yarısını kullanıyoruz. Yeşil bir kablo D25'ten 18. sütuna, oradan da 220 ohm'luk bir direnç 21. sütuna gider.",
  sub="Unplug the USB cable. This time we use the top half of the breadboard. A green wire goes from D25 to column 18, and a 220 Ω resistor from there to column 21.")
s("s43", "green", "The green LED's long leg goes in column twenty-one, the short leg in twenty-two. A black wire takes it to the top minus rail, and one more black wire connects that rail to the GND pin.",
  "Yeşil LED'in uzun bacağı 21. sütuna, kısa bacağı 22. sütuna girer. Siyah bir kablo onu üstteki eksi raya götürür, bir siyah kablo daha o rayı GND pinine bağlar.",
  sub="The green LED's long leg goes in column 21, the short leg in 22. A black wire takes it to the top minus rail, and one more black wire connects that rail to the GND pin.",
  clip="C5", pad=1.0)
s("s44", "green", "In the code, each LED gets its own timer. The red one flips every five hundred milliseconds, the green one every one hundred fifty.",
  "Kodda her LED'in kendi zamanlayıcısı var. Kırmızı her 500 milisaniyede, yeşil her 150 milisaniyede bir değişiyor.",
  sub="In the code, each LED gets its own timer. The red one flips every 500 milliseconds, the green one every 150.")
s("s45", "green", "Upload, and both blink at their own pace, while the button still reacts instantly. Try building that with delay. It's a mess.",
  "Yükleyin; ikisi de kendi hızında yanıp sönüyor ve buton hâlâ anında tepki veriyor. Bunu delay ile yapmayı deneyin; tam bir karmaşa.",
  clip="C6", pad=2.0)
s("s46", "green", "Here's a challenge for you: make the button change the green LED's speed instead, fast, slow, fast. One solution is on GitHub.",
  "Size bir görev: butonun bunun yerine yeşil LED'in hızını değiştirmesini sağlayın; hızlı, yavaş, hızlı. Bir çözümü GitHub'da.")
# ---- troubleshooting
s("s47", "trouble", "Something not working? Check that the button really sits across the middle gap, and that the yellow wire is in the D twenty-two column. If it always reads zero, the button is probably turned sideways. And if the green LED stays dark, check that the top minus rail is wired to GND.",
  "Bir şey çalışmıyor mu? Butonun gerçekten ortadaki boşluğun üzerinde durduğunu ve sarı kablonun D22 sütununda olduğunu kontrol edin. Hep 0 okuyorsa buton muhtemelen yan dönmüştür. Yeşil LED yanmıyorsa üstteki eksi rayın GND'ye bağlı olduğunu kontrol edin.",
  sub="Something not working? Check that the button really sits across the middle gap, and that the yellow wire is in the D22 column. If it always reads 0, the button is probably turned sideways. And if the green LED stays dark, check that the top minus rail is wired to GND.")
# ---- outro
s("s48", "outro", "Today, we read a button with digital read and the built-in pull-up, tamed the bounce, and used millis to do two things at once.",
  "Bugün digitalRead ve dahili pull-up ile bir buton okuduk, sekmeyi evcilleştirdik ve millis ile aynı anda iki iş yaptık.",
  sub="Today, we read a button with digitalRead and the built-in pull-up, tamed the bounce, and used millis() to do two things at once.")
s("s48b", "outro", "That's five sketches today: button LED, button toggle, blink button, two LEDs, and the challenge. They're all in the lesson folder, ready to upload.",
  "Bugün beş sketch yazdık: button_led, button_toggle, blink_button, two_leds ve görev. Hepsi ders klasöründe, yüklemeye hazır.",
  sub="That's five sketches today: button_led, button_toggle, blink_button, two_leds, and the challenge. They're all in the lesson folder, ready to upload.")
s("s49", "outro", "Next time: dimming. We'll fade the LED with PWM, mix colors with an RGB LED, and control it all with a knob. The code is on GitHub, linked below. See you there!",
  "Gelecek sefer: parlaklık. LED'i PWM ile yavaşça yakıp söndürecek, RGB LED ile renk karıştıracak ve hepsini bir düğmeyle kontrol edeceğiz. Kod GitHub'da, bağlantısı aşağıda. Orada görüşmek üzere!")

for i, d in enumerate(S):
    d["id"] = f"s{i + 1:02d}"

script = {
    "episode": 4, "title": "Buttons and Doing Two Things at Once", "voice": "en-US-EricNeural", "rate": "+5%",
    "clips": {
        "C1": "USB unplugged. Press the push button into the breadboard across the middle gap (columns 25-27), then add the yellow wire (D22 -> left side) and the black wire (right side -> minus rail). Close-up from above, landscape, 6-10 s.",
        "C2": "button_led sketch: a finger presses and holds the button - the LED lights while it's held, goes dark on release. Landscape, 5-8 s.",
        "C3": "button_toggle sketch: press, LED on; press again, LED off (two or three presses). Landscape, 5-8 s.",
        "C4": "blink_button sketch: the LED blinks; one press stops it at once, another press starts it again. Landscape, 6-10 s.",
        "C5": "USB unplugged. Top half: green wire D25 -> column 18, 220 ohm resistor 18 -> 21, green LED (long leg 21, short leg 22), black wire 22 -> top minus rail, black wire GND pin -> top minus rail. Close-up from above, landscape, 8-12 s.",
        "C6": "two_leds sketch: red and green LEDs blink at different speeds; a press stops/starts the red one while the green keeps going. Landscape, 6-10 s.",
    },
    "segments": S,
}
out = Path(__file__).with_name("script.json")
out.write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
print(out, len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
