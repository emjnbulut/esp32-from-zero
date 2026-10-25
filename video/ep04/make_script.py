"""Source of video/ep04/script.json (kept as Python so long lines stay readable).
Usage: python video/ep04/make_script.py

Version 2 (2026-10-25), follows video/PRODUCTION_GUIDELINES.md: cold open with the working result,
the sting after the cold open, if/else before the short forms, predict-then-show questions,
a millis() timeline, full-screen real results. Hardware: two breadboards side by side
(the board sits across both), red LED on GPIO 23, button on GPIO 22, green LED on GPIO 25.
"""
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


THINK = 2.6  # silence after a "quick question", so the viewer can think

# ---- cold open: the finished project first
s("cold1", "cold", "Watch this. The red LED blinks every half second, and the green one keeps its own fast rhythm.",
  "İzleyin. Kırmızı LED yarım saniyede bir yanıp sönüyor, yeşil olan da kendi hızlı ritmini koruyor.")
s("cold2", "cold", "Now I press the button. The red one stops instantly, and the green one doesn't even notice. Press again, and red is back.",
  "Şimdi butona basıyorum. Kırmızı anında duruyor, yeşil fark etmiyor bile. Tekrar basınca kırmızı geri geliyor.")
s("cold3", "cold", "By the end of this video, you'll build exactly this, with one button and a clock called millis.",
  "Bu videonun sonunda tam olarak bunu kuracaksınız: bir buton ve millis adında bir saatle.",
  sub="By the end of this video, you'll build exactly this, with one button and a clock called millis().")
# ---- parts
s("parts", "parts", "You need the board, two breadboards, one push button, a red and a green LED, two two-hundred-twenty ohm resistors, and a few jumper wires.",
  "Gerekenler: kart, iki breadboard, bir buton, bir kırmızı ve bir yeşil LED, iki tane 220 ohm direnç ve birkaç jumper kablo.",
  sub="You need the board, two breadboards, one push button, a red and a green LED, two 220 Ω resistors, and a few jumper wires.")
# ---- the push button
s("btn1", "button", "Let's start with the push button. It has four legs, but inside, it's just a simple switch.",
  "Butonla başlayalım. Dört bacağı var ama içinde basit bir anahtardan ibaret.")
s("btn2", "button", "The two legs on the left are always connected to each other, and so are the two on the right.",
  "Soldaki iki bacak her zaman birbirine bağlıdır, sağdaki iki bacak da öyle.")
s("btn3", "button", "When you press it, a little metal plate connects the left side to the right side. Let go, and they're apart again.",
  "Bastığınızda küçük bir metal plaka sol tarafı sağ tarafa bağlar. Bırakınca yine ayrılırlar.")
# ---- two breadboards, the circuit from episode 3, the button
s("bb1", "wire", "One change before we wire. On a single breadboard, our board leaves free holes on one side only. Today we need both sides.",
  "Bağlantıdan önce bir değişiklik. Tek breadboard'da kartımız sadece bir tarafta boş delik bırakıyor. Bugün iki tarafa da ihtiyacımız var.")
s("bb2", "wire", "So we use two breadboards, one above the other. The board's top pins go into the upper breadboard, and its bottom pins into the lower one. Now every pin has free holes next to it.",
  "Bu yüzden iki breadboard'u alt alta koyuyoruz. Kartın üst pinleri üstteki breadboard'a, alt pinleri alttakine giriyor. Artık her pinin yanında boş delikler var.")
s("bb3", "wire", "Unplug the USB cable first. Then rebuild the LED circuit from episode three on the lower breadboard: D twenty-three, a two-hundred-twenty ohm resistor, the red LED, and two black wires to the minus rail: one from the LED, one from GND.",
  "Önce USB kablosunu çıkarın. Sonra üçüncü bölümdeki LED devresini alttaki breadboard'a yeniden kurun: D23, 220 ohm'luk direnç, kırmızı LED ve eksi raya giden iki siyah kablo: biri LED'den, biri GND'den.",
  sub="Unplug the USB cable first. Then rebuild the LED circuit from episode 3 on the lower breadboard: D23, a 220 Ω resistor, the red LED, and two black wires to the minus rail: one from the LED, one from GND.",
  clip="C1", pad=1.0)
s("wire1", "wire", "Now the button. Press it into the lower breadboard, across the middle gap, at columns twenty-five to twenty-seven.",
  "Şimdi buton. Onu alttaki breadboard'a, ortadaki boşluğun üzerine, 25 ile 27. sütunlar arasına takın.",
  sub="Now the button. Press it into the lower breadboard, across the middle gap, at columns 25 to 27.", clip="C2")
s("wire2", "wire", "A yellow wire goes from D twenty-two to the button's left side. A black wire goes from its right side to the minus rail, which is ground.",
  "Sarı bir kablo D22'den butonun sol tarafına gider. Siyah bir kablo da sağ tarafından eksi raya, yani toprağa gider.",
  sub="A yellow wire goes from D22 to the button's left side. A black wire goes from its right side to the minus rail, which is ground.")
s("wire3", "wire", "So when you press the button, GPIO twenty-two is connected straight to ground. That's all the wiring for now.",
  "Yani butona bastığınızda GPIO 22 doğrudan toprağa bağlanır. Şimdilik bağlantı bu kadar.",
  sub="So when you press the button, GPIO 22 is connected straight to ground. That's all the wiring for now.")
# ---- floating pin and pull-ups
s("fl1", "float", "Pressed, the pin sits at zero volts. Quick question: when the button is not pressed, what does the pin read? Think about it for a second.",
  "Basılıyken pin sıfır volttadır. Kısa bir soru: buton basılı değilken pin ne okur? Bir saniye düşünün.", pad=THINK)
s("fl2", "float", "The answer: nobody knows. The pin is connected to nothing at all. We call that floating. It picks up noise from the air, even from your hand, and reads random highs and lows.",
  "Cevap: kimse bilemez. Pin hiçbir şeye bağlı değil. Buna boşta, yani floating deriz. Havadan, hatta elinizden parazit toplar ve rastgele HIGH ve LOW okur.")
s("fl3", "float", "The fix is a resistor that gently pulls the pin to a known level. A pull-up resistor pulls it up to three point three volts.",
  "Çözüm, pini bilinen bir seviyeye hafifçe çeken bir dirençtir. Pull-up direnci pini 3,3 volta çeker.",
  sub="The fix is a resistor that gently pulls the pin to a known level. A pull-up resistor pulls it up to 3.3 volts.")
s("fl4", "float", "Now, not pressed, the pin reads HIGH. Pressed, the button wins, because it connects the pin straight to ground. The pin reads LOW.",
  "Artık basılı değilken pin HIGH okur. Basılıyken buton kazanır, çünkü pini doğrudan toprağa bağlar. Pin LOW okur.")
s("fl5", "float", "A pull-down resistor does the opposite: ten kilo ohms from the pin to ground, and the button to three point three volts. Then pressed reads HIGH.",
  "Pull-down direnci bunun tersini yapar: pinden toprağa 10 kiloohm, buton da 3,3 volta. O zaman basılıyken HIGH okunur.",
  sub="A pull-down resistor does the opposite: 10 kΩ from the pin to ground, and the button to 3.3 volts. Then pressed reads HIGH.")
s("fl6", "float", "Both work. But the good news is: the ESP32 has pull-up resistors built in, about forty-five kilo ohms. No extra part. We just switch one on in code.",
  "İkisi de çalışır. Ama iyi haber şu: ESP32'nin içinde yaklaşık 45 kiloohm'luk hazır pull-up dirençleri var. Ekstra parça yok. Kodda birini açmamız yeterli.",
  sub="Both work. But the good news is: the ESP32 has pull-up resistors built in, about 45 kΩ. No extra part. We just switch one on in code.")
# ---- the first sketch, line by line, with the circuit reacting
s("code1", "code", "Plug the USB cable back in, and start a new sketch. First, we name both pins. The button is on twenty-two, the LED on twenty-three.",
  "USB kablosunu tekrar takın ve yeni bir sketch başlatın. Önce iki pine de isim veriyoruz. Buton 22'de, LED 23'te.",
  sub="Plug the USB cable back in, and start a new sketch. First, we name both pins. The button is on 22, the LED on 23.")
s("code2", "code", "In setup, the button pin gets pin mode INPUT pull up. INPUT means we read the pin, and pull up switches on that built-in resistor. The LED pin is an OUTPUT, like last time.",
  "setup içinde buton pinine pinMode INPUT_PULLUP veriyoruz. INPUT pini okuyacağımız anlamına gelir, PULLUP da o dahili direnci açar. LED pini geçen seferki gibi OUTPUT.",
  sub="In setup, the button pin gets pinMode INPUT_PULLUP. INPUT means we read the pin, and PULLUP switches on that built-in resistor. The LED pin is an OUTPUT, like last time.")
s("code3", "code", "In the loop, digital read looks at the pin and gives us HIGH or LOW. We store it in a variable called state, and print it.",
  "loop içinde digitalRead pine bakar ve bize HIGH ya da LOW verir. Onu state adlı bir değişkende tutup yazdırıyoruz.",
  sub="In the loop, digitalRead looks at the pin and gives us HIGH or LOW. We store it in a variable called state, and print it.")
s("code4", "code", "Then a simple if. If state is LOW, the button is pressed, so we write HIGH to the LED pin. Three point three volts reach the resistor, and the LED lights up.",
  "Sonra basit bir if. state LOW ise buton basılıdır, LED pinine HIGH yazarız. 3,3 volt dirence ulaşır ve LED yanar.",
  sub="Then a simple if. If state is LOW, the button is pressed, so we write HIGH to the LED pin. 3.3 volts reach the resistor, and the LED lights up.")
s("code5", "code", "Otherwise, we write LOW, and the LED goes dark. A short delay, and the loop starts again.",
  "Değilse LOW yazarız ve LED söner. Kısa bir bekleme ve loop baştan başlar.")
# ---- upload and try it
s("up1", "upload", "Save it as button LED, and click Upload. Then open the Serial Monitor at 115200 baud.",
  "button_led adıyla kaydedin ve Upload'a tıklayın. Sonra Serial Monitor'ü 115200 baud'da açın.",
  sub="Save it as button_led, and click Upload. Then open the Serial Monitor at 115200 baud.")
s("up2", "upload", "Not pressed, it prints one, which is HIGH. Press the button, and it prints zero, and the LED lights up. Let go, and it's off again.",
  "Basılı değilken 1 yazar, yani HIGH. Butona basın; 0 yazar ve LED yanar. Bırakın, yine söner.",
  sub="Not pressed, it prints 1, which is HIGH. Press the button, and it prints 0, and the LED lights up. Let go, and it's off again.",
  clip="C3", pad=2.0)
s("up3", "upload", "Want to see a floating pin with your own eyes? Change INPUT pull up to plain INPUT, and upload again.",
  "Boşta kalan bir pini kendi gözünüzle görmek ister misiniz? INPUT_PULLUP'ı düz INPUT yapın ve tekrar yükleyin.",
  sub="Want to see a floating pin with your own eyes? Change INPUT_PULLUP to plain INPUT, and upload again.")
s("up4", "upload", "Now nothing holds the pin. Touch the yellow wire, or just move your hand near it, and the numbers jump around. Change it back, and it's calm again.",
  "Artık pini hiçbir şey tutmuyor. Sarı kabloya dokunun ya da elinizi yaklaştırın; sayılar rastgele zıplar. Geri değiştirin, yine sakinleşir.")
# ---- toggle: one idea at a time
s("tog1", "toggle", "Now a classic upgrade: press once for on, press again for off. For that, the ESP32 has to notice the moment you press, not just whether the button is down.",
  "Şimdi klasik bir geliştirme: bir basışta açılsın, bir daha basınca kapansın. Bunun için ESP32'nin butonun basılı olup olmadığını değil, bastığınız anı fark etmesi gerekir.")
s("tog2", "toggle", "Think of the readings as a timeline. HIGH, HIGH, HIGH, then LOW. That one moment, where HIGH turns into LOW, is the press. It's called an edge.",
  "Okumaları bir zaman çizgisi gibi düşünün. HIGH, HIGH, HIGH, sonra LOW. HIGH'ın LOW'a döndüğü o tek an basıştır. Buna kenar, yani edge denir.")
s("tog3", "toggle", "To catch it, we remember the last reading in a variable called last state. If the new state is different, and it's LOW, that's a new press.",
  "Onu yakalamak için son okumayı lastState adlı bir değişkende hatırlıyoruz. Yeni durum farklıysa ve LOW ise, bu yeni bir basıştır.",
  sub="To catch it, we remember the last reading in a variable called lastState. If the new state is different, and it's LOW, that's a new press.")
s("tog4", "toggle", "Quick question: if you hold the button down, does the LED keep flipping?",
  "Kısa bir soru: butonu basılı tutarsanız LED sürekli değişir mi?", pad=THINK)
s("tog5", "toggle", "No. While you hold it, state stays LOW, and so does last state. Nothing changes, so there's no new edge.",
  "Hayır. Basılı tuttuğunuz sürece state LOW kalır, lastState de öyle. Hiçbir şey değişmez, yani yeni bir kenar yoktur.",
  sub="No. While you hold it, state stays LOW, and so does lastState. Nothing changes, so there's no new edge.")
s("tog6", "toggle", "So what do we do on a press? We keep a bool called LED on, which is true or false. If it's true, we make it false. Otherwise, we make it true. Then we write HIGH or LOW to match.",
  "Peki bir basışta ne yapıyoruz? ledOn adında, true ya da false olan bir bool tutuyoruz. true ise false yapıyoruz, değilse true. Sonra ona uygun HIGH ya da LOW yazıyoruz.",
  sub="So what do we do on a press? We keep a bool called ledOn, which is true or false. If it's true, we make it false. Otherwise, we make it true. Then we write HIGH or LOW to match.")
s("tog7", "toggle", "That works, and it's easy to read. Programmers often write it shorter. The exclamation mark means not, so LED on equals not LED on flips it in one line.",
  "Bu çalışır ve okunması kolaydır. Programcılar bunu çoğu zaman daha kısa yazar. Ünlem işareti değil anlamına gelir; ledOn = !ledOn onu tek satırda çevirir.",
  sub="That works, and it's easy to read. Programmers often write it shorter. The exclamation mark means \"not\", so ledOn = !ledOn flips it in one line.")
s("tog8", "toggle", "And the question mark picks one of two values: HIGH when LED on is true, LOW when it's not. Same result, two lines instead of six.",
  "Soru işareti de iki değerden birini seçer: ledOn true ise HIGH, değilse LOW. Aynı sonuç, altı satır yerine iki satır.",
  sub="And the question mark picks one of two values: HIGH when ledOn is true, LOW when it's not. Same result, two lines instead of six.")
# ---- bounce
s("bo1", "bounce", "Let's also count the presses, and print the count. Press once, and sometimes the count jumps by two, or even three.",
  "Basışları sayıp sayıyı da yazdıralım. Bir kez basın; sayı bazen iki, hatta üç birden artar.")
s("bo2", "bounce", "That's bouncing. When the metal contacts touch, they bounce for a few milliseconds. The ESP32 checks the pin hundreds of thousands of times a second, so one press can look like five.",
  "Buna sekme denir. Metal kontaklar birbirine değdiğinde birkaç milisaniye sekerler. ESP32 pini saniyede yüz binlerce kez kontrol eder, bu yüzden tek bir basış beş basış gibi görünebilir.")
s("bo3", "bounce", "The simple fix is called debouncing. After every change, pressed or released, we wait fifty milliseconds, until the bouncing is over.",
  "Basit çözümün adı debounce. Her değişiklikten sonra, basınca da bırakınca da, sekme bitene kadar 50 milisaniye bekliyoruz.",
  sub="The simple fix is called debouncing. After every change, pressed or released, we wait 50 milliseconds, until the bouncing is over.")
s("bo4", "bounce", "Now every press counts exactly once, and flips the LED exactly once. This sketch is in the lesson folder as button toggle.",
  "Artık her basış tam bir kez sayılıyor ve LED'i tam bir kez çeviriyor. Bu sketch ders klasöründe button_toggle adıyla duruyor.",
  sub="Now every press counts exactly once, and flips the LED exactly once. This sketch is in the lesson folder as button_toggle.",
  clip="C4", pad=2.0)
# ---- part two: why delay() gets in the way
s("bl1", "block", "Now, part two. Let's bring back the blinking from last episode, and let the button switch the blinking on and off.",
  "Şimdi ikinci kısım. Geçen bölümdeki yanıp sönmeyi geri getirelim ve butonun yanıp sönmeyi açıp kapatmasını sağlayalım.")
s("bl2", "block", "The obvious way: blink with delay, and read the button in the same loop. Quick question: if you press during a delay, will the ESP32 notice?",
  "Akla gelen ilk yol: delay ile yakıp söndürmek ve butonu aynı loop'ta okumak. Kısa bir soru: bir delay sırasında basarsanız ESP32 fark eder mi?",
  pad=THINK)
s("bl3", "block", "It won't. Delay freezes everything. For half a second, the ESP32 doesn't look at the button at all, so a short press is simply missed.",
  "Etmez. delay her şeyi dondurur. Yarım saniye boyunca ESP32 butona hiç bakmaz, yani kısa bir basış kaybolur gider.")
s("bl4", "block", "Shorter delays don't really help. The blinking gets messy, and presses still slip through. The real fix is a different way of thinking.",
  "Daha kısa delay'ler pek işe yaramaz. Yanıp sönme bozulur ve basışlar yine kaçar. Asıl çözüm farklı bir düşünme biçimi.")
# ---- millis()
s("mi1", "millis", "Never wait. Instead, look at the clock. millis gives the number of milliseconds since the board started, and it keeps counting by itself, while your code does other things.",
  "Hiç beklemeyin. Onun yerine saate bakın. millis, kart açıldığından beri geçen milisaniye sayısını verir ve kodunuz başka işler yaparken kendi kendine saymaya devam eder.",
  sub="Never wait. Instead, look at the clock. millis() gives the number of milliseconds since the board started, and it keeps counting by itself, while your code does other things.")
s("mi2", "millis", "We save the time of the last blink in a variable called last blink. Then, in every loop, we read the clock into now, and ask one question: has now minus last blink reached five hundred?",
  "Son yanıp sönmenin zamanını lastBlink adlı bir değişkende saklıyoruz. Sonra her loop'ta saati now değişkenine okuyup tek bir soru soruyoruz: now eksi lastBlink 500'e ulaştı mı?",
  sub="We save the time of the last blink in a variable called lastBlink. Then, in every loop, we read the clock into now, and ask one question: has now minus lastBlink reached 500?")
s("mi3", "millis", "Let's watch it on a timeline. The LED changed at one thousand. Now it's twelve hundred. Twelve hundred minus one thousand is two hundred: not yet. The loop just moves on.",
  "Bir zaman çizgisinde izleyelim. LED 1000'de değişti. Şimdi 1200. 1200 eksi 1000, 200 eder: henüz değil. Loop yoluna devam eder.",
  sub="Let's watch it on a timeline. The LED changed at 1000. Now it's 1200. 1200 minus 1000 is 200: not yet. The loop just moves on.")
s("mi4", "millis", "Now it's fourteen ninety-nine. Four hundred ninety-nine: still not. One millisecond later, five hundred. Flip the LED, and set last blink to now. A new interval starts.",
  "Şimdi 1499. 499: hâlâ değil. Bir milisaniye sonra 500. LED'i çevir ve lastBlink'i now yap. Yeni bir aralık başlar.",
  sub="Now it's 1499. 499: still not. One millisecond later, 500. Flip the LED, and set lastBlink to now. A new interval starts.")
s("mi5", "millis", "Times live in a type called unsigned long, a big whole number that can't go negative. And we always subtract: now minus the last time. After about forty-nine days, millis rolls over to zero, and the subtraction still works out.",
  "Zamanlar unsigned long adlı bir tipte tutulur; negatif olamayan büyük bir tam sayı. Ve her zaman çıkarma yaparız: şimdi eksi son zaman. Yaklaşık 49 günde bir millis sıfıra döner ve çıkarma yine doğru sonuç verir.",
  sub="Times live in a type called unsigned long, a big whole number that can't go negative. And we always subtract: now minus the last time. After about 49 days, millis() rolls over to zero, and the subtraction still works out.")
s("mi6", "millis", "The button uses the same trick. Instead of a delay for debouncing, we ignore changes that come less than fifty milliseconds after the last one.",
  "Buton da aynı yöntemi kullanıyor. Debounce için delay yerine, bir öncekinden sonraki 50 milisaniye içinde gelen değişiklikleri yok sayıyoruz.",
  sub="The button uses the same trick. Instead of a delay for debouncing, we ignore changes that come less than 50 milliseconds after the last one.")
s("mi7", "millis", "Now the loop never waits. It runs thousands of times a second, and every time, it checks the button and the clock.",
  "Artık loop hiç beklemiyor. Saniyede binlerce kez dönüyor ve her seferinde butonu ve saati kontrol ediyor.")
s("mi8", "millis", "Upload it. The LED blinks, and the moment you press the button, it stops. Press again, and it blinks again.",
  "Yükleyin. LED yanıp sönüyor ve butona bastığınız anda duruyor. Tekrar basın, yeniden yanıp sönüyor.",
  clip="C5", pad=2.0)
# ---- a second LED on the upper breadboard
s("gr1", "green", "And this scales. Let's add a second LED, a green one, with its own speed. Unplug the USB cable. This time we use the upper breadboard.",
  "Ve bu yöntem büyür. Kendi hızı olan ikinci bir LED ekleyelim, yeşil bir LED. USB kablosunu çıkarın. Bu sefer üstteki breadboard'u kullanıyoruz.")
s("gr2", "green", "A green wire goes from D twenty-five to column eighteen. A two-hundred-twenty ohm resistor goes from there to column twenty-one.",
  "Yeşil bir kablo D25'ten 18. sütuna gider. 220 ohm'luk bir direnç de oradan 21. sütuna.",
  sub="A green wire goes from D25 to column 18. A 220 Ω resistor goes from there to column 21.")
s("gr3", "green", "The green LED's long leg goes in column twenty-one, the short leg in twenty-two. A black wire takes it to the minus rail, and one more black wire connects that rail to a GND pin.",
  "Yeşil LED'in uzun bacağı 21. sütuna, kısa bacağı 22. sütuna girer. Siyah bir kablo onu eksi raya götürür, bir siyah kablo daha o rayı bir GND pinine bağlar.",
  sub="The green LED's long leg goes in column 21, the short leg in 22. A black wire takes it to the minus rail, and one more black wire connects that rail to a GND pin.",
  clip="C6", pad=1.0)
s("gr4", "green", "In the code, each LED gets its own timer: last red and last green. Red flips every five hundred milliseconds, green every one hundred fifty.",
  "Kodda her LED'in kendi zamanlayıcısı var: lastRed ve lastGreen. Kırmızı her 500 milisaniyede, yeşil her 150 milisaniyede bir değişiyor.",
  sub="In the code, each LED gets its own timer: lastRed and lastGreen. Red flips every 500 milliseconds, green every 150.")
s("gr5", "green", "Quick question: if we change the green interval to three hundred, does the red LED change too?",
  "Kısa bir soru: yeşilin aralığını 300 yaparsak kırmızı LED de değişir mi?",
  sub="Quick question: if we change the green interval to 300, does the red LED change too?", pad=THINK)
s("gr6", "green", "No. Each if checks only its own timer. Change one number, and only that LED changes. Upload, and both blink at their own pace, while the button still reacts instantly.",
  "Hayır. Her if yalnızca kendi zamanlayıcısına bakar. Bir sayıyı değiştirin, yalnızca o LED değişir. Yükleyin; ikisi de kendi hızında yanıp sönüyor ve buton hâlâ anında tepki veriyor.",
  clip="C7", pad=2.0)
# ---- your turn
s("ch1", "challenge", "Your turn. Red keeps blinking every five hundred milliseconds. Make each button press switch the green LED between fast, one hundred fifty, and slow, six hundred, without disturbing red.",
  "Sıra sizde. Kırmızı her 500 milisaniyede yanıp sönmeye devam etsin. Her basışta yeşil LED hızlı, yani 150, ile yavaş, yani 600, arasında değişsin; kırmızı hiç etkilenmesin.",
  sub="Your turn. Red keeps blinking every 500 milliseconds. Make each button press switch the green LED between fast (150) and slow (600), without disturbing red.")
s("ch2", "challenge", "You only need what we used today: a variable for the green interval, an edge, and an if. Post your solution in the comments. I'll show one in a Short.",
  "Bugün kullandıklarımız yeterli: yeşil aralık için bir değişken, bir kenar ve bir if. Çözümünüzü yorumlara yazın. Bir çözümü bir Short'ta göstereceğim.")
# ---- troubleshooting
s("tr1", "trouble", "Something not working? Check that the button really sits across the middle gap, and that the yellow wire is in the D twenty-two column. If it always reads zero, the button is probably turned sideways. And if the green LED stays dark, check the black wire from its minus rail to GND.",
  "Bir şey çalışmıyor mu? Butonun gerçekten ortadaki boşluğun üzerinde durduğunu ve sarı kablonun D22 sütununda olduğunu kontrol edin. Hep 0 okuyorsa buton muhtemelen yan dönmüştür. Yeşil LED yanmıyorsa da eksi rayından GND'ye giden siyah kabloyu kontrol edin.",
  sub="Something not working? Check that the button really sits across the middle gap, and that the yellow wire is in the D22 column. If it always reads 0, the button is probably turned sideways. And if the green LED stays dark, check the black wire from its minus rail to GND.")
# ---- outro
s("out1", "outro", "Today, we read a button with digital read and the built-in pull-up, caught the edge of a press, tamed the bounce, and used millis to do two things at once.",
  "Bugün digitalRead ve dahili pull-up ile bir buton okuduk, basışın kenarını yakaladık, sekmeyi evcilleştirdik ve millis ile aynı anda iki iş yaptık.",
  sub="Today, we read a button with digitalRead and the built-in pull-up, caught the edge of a press, tamed the bounce, and used millis() to do two things at once.")
s("out2", "outro", "Next time: PWM. We'll fade an LED smoothly, and mix any color with an RGB LED. All five sketches are on GitHub, linked below. See you there!",
  "Gelecek sefer: PWM. Bir LED'i yumuşakça yakıp söndürecek ve RGB LED ile istediğimiz rengi karıştıracağız. Beş sketch'in hepsi GitHub'da, bağlantısı aşağıda. Orada görüşmek üzere!")

NAMES = {}
for i, d in enumerate(S):
    NAMES[d["id"]] = f"s{i + 1:02d}"
    d["id"] = NAMES[d["id"]]

script = {
    "episode": 4, "title": "Buttons and Doing Two Things at Once", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": NAMES["cold3"],
    "clips": {
        "C0": "OPENING, full screen (same take can serve C7): finished two_leds circuit on the two breadboards, USB plugged in. Red blinks every 0.5 s, green blinks fast; after ~3 s a finger presses the button once (red stops at once, green keeps going), ~2 s later presses again (red starts again). Landscape, steady, both LEDs + button clearly in frame, 10-12 s.",
        "C1": "USB unplugged. Two breadboards one above the other, the ESP32 across both (top pins in the upper breadboard's row j, bottom pins in the lower one's row a). Rebuild the red LED circuit on the lower breadboard as in the drawing. Top view, landscape, 8-12 s.",
        "C2": "USB unplugged. Press the button into the lower breadboard across the middle gap (columns 25-27), then the yellow wire (D22 -> button left side) and the black wire (button right side -> minus rail). Close-up from above, landscape, 6-10 s.",
        "C3": "button_led sketch, full screen: a finger presses and holds the button - the LED lights while it's held, goes dark on release (twice). Landscape, 5-8 s.",
        "C4": "button_toggle sketch, full screen: press, LED on; press again, LED off (three or four presses). Landscape, 6-8 s.",
        "C5": "blink_button sketch, full screen: the LED blinks; one press stops it at once, another press starts it again. Landscape, 6-10 s.",
        "C6": "USB unplugged. Upper breadboard: green wire D25 -> column 18, 220 ohm resistor 18 -> 21, green LED (long leg 21, short leg 22), black wire 22 -> top minus rail, black wire GND pin -> top minus rail. Close-up from above, landscape, 8-12 s.",
        "C7": "two_leds sketch, full screen: red and green blink at their own speeds; a press stops the red one while the green keeps going, another press starts red again. Landscape, 8-10 s (may be the same take as C0).",
    },
    "segments": S,
}
out = Path(__file__).with_name("script.json")
out.write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
print(out, len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
