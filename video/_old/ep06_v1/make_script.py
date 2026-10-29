"""Source of video/ep06/script.json (kept as Python so long lines stay readable).
Usage: python video/ep06/make_script.py

Episode 6 "Analog Input and the Potentiometer" (2026-10-28), follows video/PRODUCTION_GUIDELINES.md incl. section 8:
ONE new topic (analogRead), the rest is practice. Cold open with the working result, sting after it, the sketch grows
in small steps (pot_read -> pot_dimmer -> pot_zones -> pot_smooth), a code tour before every result clip, quick questions,
one multimeter clip (CURRICULUM.md), subtle like/subscribe icons in the scenes (section 5, max 2),
the end invites viewers to the comments. Not a mini-project: no challenge-solution Short is promised.
Hardware: the episode 5 circuit (red LED GPIO 23 + button GPIO 22 on the lower breadboard; the RGB LED stays unused).
The potentiometer goes into the upper breadboard: outer legs 3V3 and GND, middle leg GPIO 34 (input only).
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


THINK = 2.6  # silence after a "quick question"

# ---- cold open
s("cold1", "cold", "Watch this. I turn a knob, and the LED follows my hand. Brighter, dimmer, instantly, with no delay at all.",
  "İzleyin. Bir düğmeyi çeviriyorum ve LED elimi takip ediyor. Daha parlak, daha loş, anında, hiç delay olmadan.")
s("cold2", "cold", "A little later, we cut the knob into three zones, and each zone gives the LED its own brightness.",
  "Biraz sonra düğmeyi üç bölgeye ayıracağız ve her bölge LED'e kendi parlaklığını verecek.")
s("cold3", "cold", "By the end of this video, you'll read any knob, or any analog sensor, with one function: analog read.",
  "Bu videonun sonunda herhangi bir düğmeyi ya da analog sensörü tek bir fonksiyonla okuyacaksınız: analogRead.",
  sub="By the end of this video, you'll read any knob, or any analog sensor, with one function: analogRead().")
# ---- parts
s("parts", "parts", "You need last episode's circuit with the red LED. Plus one ten kilo-ohm potentiometer, that's a knob with three legs, and a few wires. A multimeter is a nice extra.",
  "Geçen bölümün kırmızı LED'li devresi gerekiyor. Bir de 10 kilo-ohm'luk bir potansiyometre, yani üç bacaklı bir düğme, ve birkaç kablo. Multimetre de güzel bir ekstra.",
  sub="You need last episode's circuit with the red LED. Plus one 10 kΩ potentiometer, that's a knob with three legs, and a few wires. A multimeter is a nice extra.")
# ---- the idea, without code
s("idea1", "idea", "Until now, every input we read was a button: pressed, or not pressed. Two answers. A knob is different. It can give every answer in between.",
  "Şimdiye kadar okuduğumuz her giriş bir butondu: basılı ya da basılı değil. İki cevap. Düğme farklı. Aradaki her cevabı verebilir.")
s("idea2", "idea", "Inside, a knob is a resistor with a sliding contact. The two outer legs connect to three point three volts and to ground. The middle leg gives us a voltage anywhere between them.",
  "İçinde bir düğme, kayan bir temas noktası olan bir dirençtir. İki dış bacak 3,3 volta ve toprağa bağlanır. Orta bacak bize ikisinin arasında herhangi bir voltaj verir.",
  sub="Inside, a knob is a resistor with a sliding contact. The two outer legs connect to 3.3 V and to ground. The middle leg gives us a voltage anywhere between them.")
s("idea3", "idea", "Turn the knob to one end, and the middle leg sits at zero volts. Turn it to the other end, and it sits at three point three. In the middle, about half of that.",
  "Düğmeyi bir uca çevirin: orta bacak sıfır voltta durur. Diğer uca çevirin: 3,3 voltta durur. Ortada yaklaşık yarısı.",
  sub="Turn the knob to one end, and the middle leg sits at 0 V. Turn it to the other end, and it sits at 3.3 V. In the middle, about half of that.")
s("idea4", "idea", "Quick question: the knob is exactly in the middle. Roughly how many volts are on the middle leg?",
  "Kısa bir soru: düğme tam ortada. Orta bacakta yaklaşık kaç volt var?", pad=THINK)
s("idea5", "idea", "About one point six five volts. Half of three point three. Every position of the knob is its own voltage.",
  "Yaklaşık 1,65 volt. 3,3'ün yarısı. Düğmenin her konumu kendi voltajıdır.",
  sub="About 1.65 V. Half of 3.3. Every position of the knob is its own voltage.")
# ---- wiring
s("wire1", "wire", "Unplug the USB cable. Push the potentiometer into the upper breadboard. The left leg goes to the minus rail, the right leg to three point three volts, and the middle leg to G P I O thirty-four.",
  "USB kablosunu çıkarın. Potansiyometreyi üstteki breadboard'a takın. Sol bacak eksi raya, sağ bacak 3,3 volta, orta bacak da GPIO 34'e gider.",
  sub="Unplug the USB cable. Push the potentiometer into the upper breadboard. The left leg goes to the minus rail, the right leg to 3.3 V, and the middle leg to GPIO 34.",
  clip="C2", pad=3.0)
s("wire2", "wire", "Swap the two outer legs and nothing breaks. The knob just works backwards. And pin thirty-four only does input, which makes it a perfect home for sensors.",
  "İki dış bacağı değiştirirseniz hiçbir şey bozulmaz; düğme sadece ters çalışır. Ayrıca 34. pin yalnızca giriş yapar, bu da onu sensörler için ideal yapar.",
  sub="Swap the two outer legs and nothing breaks. The knob just works backwards. And pin 34 only does input, which makes it a perfect home for sensors.")
# ---- analogRead
s("ar1", "read", "The function is analog read. Give it a pin, and it gives back a number. The ESP32 measures the voltage in four thousand ninety-six steps, from zero up to four thousand ninety-five.",
  "Fonksiyonun adı analogRead. Ona bir pin verirsiniz, size bir sayı geri verir. ESP32 voltajı 4096 adımda ölçer; sıfırdan 4095'e kadar.",
  sub="The function is analogRead(). Give it a pin, and it gives back a number. The ESP32 measures the voltage in 4096 steps, from 0 up to 4095.")
s("ar2", "read", "Zero means zero volts. Four thousand ninety-five means three point three volts. Everything else is in between.",
  "Sıfır, sıfır volt demektir. 4095, 3,3 volt demektir. Geri kalan her şey ikisinin arasındadır.",
  sub="0 means 0 V. 4095 means 3.3 V. Everything else is in between.")
# ---- code tour: pot_read
s("tpr1", "tourread", "Here's the whole sketch, and it's tiny. Pin thirty-four gets a name: pot pin. Setup only starts the Serial Monitor. An input needs no pin mode.",
  "İşte sketch'in tamamı ve çok küçük. 34. pine bir ad veriyoruz: POT_PIN. setup yalnızca Seri Monitör'ü başlatır. Bir giriş için pinMode gerekmez.",
  sub="Here's the whole sketch, and it's tiny. Pin 34 gets a name: POT_PIN. setup() only starts the Serial Monitor. An input needs no pinMode().", tour=True)
s("tpr2", "tourread", "In the loop, analog read goes into a box called value. We print the box, and wait a tenth of a second. That's ten readings every second.",
  "loop'ta analogRead'in sonucu value adlı bir kutuya girer. Kutuyu yazdırır ve saniyenin onda biri kadar bekleriz. Yani saniyede on okuma.",
  sub="In the loop, analogRead() goes into a box called value. We print the box, and wait a tenth of a second. That's ten readings every second.", tour=True)
s("ar3", "read", "Turn the knob and watch the number: zero at one end, about four thousand at the other. A multimeter on the middle leg shows the same sweep in volts. This sketch is pot read.",
  "Düğmeyi çevirin ve sayıyı izleyin: bir uçta sıfır, diğer uçta yaklaşık dört bin. Orta bacaktaki multimetre aynı geçişi volt olarak gösterir. Bu sketch'in adı pot_read.",
  sub="Turn the knob and watch the number: 0 at one end, about 4000 at the other. A multimeter on the middle leg shows the same sweep in volts. This sketch is pot_read.",
  clip="C1", pad=3.0)
s("ar3b", "read", "Near the very ends, the ESP32's reader flattens a little, so you may not see exactly zero or exactly four thousand ninety-five. That's normal.",
  "Uçlara çok yakın yerlerde ESP32'nin okuyucusu biraz düzleşir; bu yüzden tam sıfırı ya da tam 4095'i görmeyebilirsiniz. Bu normal.",
  sub="Near the very ends, the ESP32's reader flattens a little, so you may not see exactly 0 or exactly 4095. That's normal.")
s("ar4", "read", "Quick question: the Serial Monitor says two thousand. About where is the knob?",
  "Kısa bir soru: Seri Monitör iki bin diyor. Düğme yaklaşık nerede?",
  sub="Quick question: the Serial Monitor says 2000. About where is the knob?", pad=THINK)
s("ar5", "read", "A little before the middle. Two thousand is just under half of four thousand ninety-five.",
  "Ortanın biraz öncesinde. İki bin, 4095'in yarısının hemen altında.",
  sub="A little before the middle. 2000 is just under half of 4095.")
# ---- practice 1: the dimmer
s("dm1", "dim", "Now let the knob do something. In episode five, analog write set the brightness. It takes a number from zero to two fifty-five.",
  "Şimdi düğme bir şey yapsın. 5. bölümde analogWrite parlaklığı ayarlıyordu. Sıfır ile 255 arasında bir sayı alıyor.",
  sub="Now let the knob do something. In episode 5, analogWrite() set the brightness. It takes a number from 0 to 255.")
s("dm2", "dim", "But the knob gives zero to four thousand ninety-five. Quick question: how do we squeeze a big range into a smaller one?",
  "Ama düğme sıfırdan 4095'e kadar veriyor. Kısa bir soru: büyük bir aralığı küçük bir aralığa nasıl sığdırırız?",
  sub="But the knob gives 0 to 4095. Quick question: how do we squeeze a big range into a smaller one?", pad=THINK)
s("dm3", "dim", "We divide. Four thousand ninety-five divided by sixteen is about two fifty-five. So the knob value divided by sixteen is the brightness, and both ends of the knob fit both ends of the scale.",
  "Bölüyoruz. 4095 bölü 16 yaklaşık 255 eder. Yani düğme değeri bölü 16 parlaklıktır; düğmenin iki ucu ölçeğin iki ucuna oturur.",
  sub="We divide. 4095 divided by 16 is about 255. So the knob value divided by 16 is the brightness, and both ends of the knob fit both ends of the scale.")
# ---- code tour: pot_dimmer
s("tpd1", "tourdim", "The whole sketch: two pin names, the knob and the red LED. Setup makes the LED an output and starts the Serial Monitor.",
  "Sketch'in tamamı: iki pin adı, düğme ve kırmızı LED. setup LED'i çıkış yapar ve Seri Monitör'ü başlatır.", tour=True)
s("tpd2", "tourdim", "In the loop: read the knob into value. Divide by sixteen into brightness. Then analog write shows it on the LED. We print it, and wait twenty milliseconds.",
  "loop'ta: düğmeyi value'ya okuruz. 16'ya bölüp brightness'a koyarız. Sonra analogWrite bunu LED'de gösterir. Yazdırır ve yirmi milisaniye bekleriz.",
  sub="In the loop: read the knob into value. Divide by 16 into brightness. Then analogWrite() shows it on the LED. We print it, and wait 20 milliseconds.", tour=True)
s("dm4", "dim", "Turn the knob, and the LED follows instantly. This sketch is pot dimmer.",
  "Düğmeyi çevirin; LED anında takip ediyor. Bu sketch'in adı pot_dimmer.",
  sub="Turn the knob, and the LED follows instantly. This sketch is pot_dimmer.", clip="C3", pad=2.5)
s("dm5", "dim", "Quick question: what if we divide by thirty-two instead of sixteen?",
  "Kısa bir soru: 16 yerine 32'ye bölersek ne olur?",
  sub="Quick question: what if we divide by 32 instead of 16?", pad=THINK)
s("dm6", "dim", "The biggest number is now only about one twenty-seven. The LED never gets brighter than half, even with the knob all the way up.",
  "En büyük sayı artık yalnızca 127 civarında. Düğme sonuna kadar çevrilse bile LED yarıdan fazla parlamaz.",
  sub="The biggest number is now only about 127. The LED never gets brighter than half, even with the knob all the way up.")
# ---- practice 2: zones
s("zn1", "zones", "Sometimes you don't want every value. You just want a few choices. Let's cut the knob into three zones: left, middle and right.",
  "Bazen her değeri istemezsiniz; sadece birkaç seçenek istersiniz. Düğmeyi üç bölgeye ayıralım: sol, orta ve sağ.")
s("zn2", "zones", "Four thousand ninety-five divided by three is about thirteen sixty-five. So below thirteen sixty-five is the left zone. Below twenty-seven thirty, the middle zone. And everything else, the right zone.",
  "4095 bölü 3 yaklaşık 1365 eder. Yani 1365'in altı sol bölge. 2730'un altı orta bölge. Geri kalan her şey sağ bölge.",
  sub="4095 divided by 3 is about 1365. So below 1365 is the left zone. Below 2730, the middle zone. And everything else, the right zone.")
s("zn3", "zones", "In code, that's an if, an else if, and an else. Check the first. Only check the next one if the one before was false.",
  "Kodda bu bir if, bir else if ve bir else. Birincisini kontrol et. Bir öncekisi yanlışsa sıradakini kontrol et.")
# ---- code tour: pot_zones
s("tpz1", "tourzones", "The whole sketch: the knob, the red LED, and a read at the top of the loop. Then the first if. Below thirteen sixty-five, the LED gets twenty: dim.",
  "Sketch'in tamamı: düğme, kırmızı LED ve loop'un başında bir okuma. Sonra ilk if. 1365'in altında LED 20 alır: loş.",
  sub="The whole sketch: the knob, the red LED, and a read at the top of the loop. Then the first if. Below 1365, the LED gets 20: dim.", tour=True)
s("tpz2", "tourzones", "Else if below twenty-seven thirty: the middle zone, one twenty, medium. Else: the right zone, two fifty-five, full brightness.",
  "Yoksa 2730'un altındaysa: orta bölge, 120, orta parlaklık. Değilse: sağ bölge, 255, tam parlaklık.",
  sub="Else if below 2730: the middle zone, 120, medium. Else: the right zone, 255, full brightness.", tour=True)
s("tpz3", "tourzones", "Only one of the three branches runs each time around the loop. Then we print the value, and wait twenty milliseconds.",
  "Loop'un her turunda üç daldan yalnızca biri çalışır. Sonra değeri yazdırır ve yirmi milisaniye bekleriz.",
  sub="Only one of the three branches runs each time around the loop. Then we print the value, and wait 20 milliseconds.", tour=True)
s("zn4", "zones", "Turn the knob slowly: dim, medium, full, in three clear steps. This sketch is pot zones.",
  "Düğmeyi yavaşça çevirin: loş, orta, tam; üç net adımda. Bu sketch'in adı pot_zones.",
  sub="Turn the knob slowly: dim, medium, full, in three clear steps. This sketch is pot_zones.", clip="C4", pad=2.5)
# ---- practice 3: a calmer reading
s("sm1", "smooth", "One last thing. Watch the number while you don't touch the knob at all. It wobbles a little. That's electrical noise, and every analog reading has some.",
  "Son bir şey. Düğmeye hiç dokunmazken sayıyı izleyin. Biraz titriyor. Bu elektriksel gürültü ve her analog okumada biraz vardır.")
s("sm2", "smooth", "The fix: read four times, add the readings up, and divide by four. An average is calmer than a single reading.",
  "Çözüm: dört kez oku, okumaları topla ve dörde böl. Ortalama, tek bir okumadan daha sakindir.")
s("tps1", "toursmooth", "Raw is one single reading. Sum starts at zero. Then a for loop runs four times, and every time it adds a fresh reading to sum.",
  "raw tek bir okuma. sum sıfırdan başlar. Sonra bir for döngüsü dört kez çalışır ve her seferinde sum'a yeni bir okuma ekler.", tour=True)
s("tps2", "toursmooth", "Read the for like this: start i at zero, keep going while i is less than four, and add one to i every round. Four rounds.",
  "for'u şöyle okuyun: i sıfırdan başlasın, i dörtten küçük olduğu sürece devam etsin ve her turda i'ye bir eklensin. Dört tur.", tour=True)
s("tps3", "toursmooth", "After the loop, sum divided by four is the average. We print raw and average, each with a name, so the Serial Plotter can draw two lines.",
  "Döngüden sonra sum bölü dört ortalamadır. raw ve avg'yi her biri bir adla yazdırırız; böylece Serial Plotter iki çizgi çizebilir.",
  sub="After the loop, sum divided by 4 is the average. We print raw and avg, each with a name, so the Serial Plotter can draw two lines.", tour=True)
s("sm3", "smooth", "Open the Serial Plotter, right next to the Serial Monitor. The raw line jitters. The average line is smoother. This sketch is pot smooth.",
  "Seri Monitör'ün hemen yanındaki Serial Plotter'ı açın. raw çizgisi titrer. Ortalama çizgisi daha düzgündür. Bu sketch'in adı pot_smooth.",
  sub="Open the Serial Plotter, right next to the Serial Monitor. The raw line jitters. The average line is smoother. This sketch is pot_smooth.")
# ---- your turn (not a mini-project: the solution stays in the lesson folder)
s("ch1", "challenge", "Your turn: Knob Blink Speed. The red LED blinks all the time, and the knob picks how fast, in three zones: left, every one hundred milliseconds. Middle, four hundred. Right, one second.",
  "Sıra sizde: Düğmeyle Yanıp Sönme Hızı. Kırmızı LED sürekli yanıp söner ve düğme ne kadar hızlı olacağını üç bölgede seçer: solda her 100 milisaniyede. Ortada 400. Sağda bir saniye.",
  sub="Your turn: Knob Blink Speed. The red LED blinks all the time, and the knob picks how fast, in three zones: left, every 100 milliseconds. Middle, 400. Right, one second.")
s("ch2", "challenge", "Hint: today's zones choose the interval, and the millis blink from episode four does the blinking. Nothing may wait with delay. Post your solution in the comments. One solution is in the lesson folder.",
  "İpucu: bugünkü bölgeler aralığı seçsin, yanıp sönmeyi de 4. bölümdeki millis yöntemi yapsın. Hiçbir şey delay ile beklemesin. Çözümünüzü yorumlara yazın. Bir çözüm ders klasöründe.",
  sub="Hint: today's zones choose the interval, and the millis() blink from episode 4 does the blinking. Nothing may wait with delay(). Post your solution in the comments. One solution is in the lesson folder.")
# ---- troubleshooting
s("tb1", "trouble", "Something not working? If the number jumps wildly, check that the middle leg is on pin thirty-four. If it's stuck at zero or at four thousand ninety-five, one outer leg is loose or on the wrong rail.",
  "Bir şey çalışmıyor mu? Sayı çılgınca zıplıyorsa orta bacağın 34. pinde olduğunu kontrol edin. Sıfırda ya da 4095'te takılı kalıyorsa bir dış bacak gevşektir ya da yanlış raydadır.",
  sub="Something not working? If the number jumps wildly, check that the middle leg is on pin 34. If it's stuck at 0 or at 4095, one outer leg is loose or on the wrong rail.")
# ---- outro
s("out1", "outro", "Today, we read a knob with analog read, turned it into brightness by dividing, cut it into zones with if and else if, and calmed the noise with an average.",
  "Bugün bir düğmeyi analogRead ile okuduk, bölerek parlaklığa çevirdik, if ve else if ile bölgelere ayırdık ve ortalama ile gürültüyü yatıştırdık.",
  sub="Today, we read a knob with analogRead(), turned it into brightness by dividing, cut it into zones with if and else if, and calmed the noise with an average.")
s("out2", "outro", "Next time: a function that does the dividing for us, called map, and a bar of LEDs that fills up as you turn the knob. Let's meet in the comments: tell me what you would control with a knob. See you there!",
  "Gelecek sefer: bölme işini bizim yerimize yapan map adında bir fonksiyon ve düğmeyi çevirdikçe dolan bir LED çubuğu. Yorumlarda buluşalım: bir düğmeyle neyi kontrol ederdiniz, yazın. Görüşmek üzere!",
  sub="Next time: a function that does the dividing for us, called map(), and a bar of LEDs that fills up as you turn the knob. Let's meet in the comments: tell me what you would control with a knob. See you there!")

# ids: segments keep s01..sNN (narration and dub caches are keyed by id);
# code-tour segments (tour=True) are named after the segment before them: s11t1, s11t2, ...
NAMES = {}
n = k = 0
for d in S:
    if d.pop("tour", False):
        k += 1
        NAMES[d["id"]] = f"s{n:02d}t{k}"
    else:
        n += 1
        k = 0
        NAMES[d["id"]] = f"s{n:02d}"
    d["id"] = NAMES[d["id"]]

script = {
    "episode": 6, "title": "Analog Input and the Potentiometer", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": NAMES["cold3"],
    "clips": {
        "C0": "OPENING, full screen, 12-15 s: one hand turns the knob slowly from one end to the other and back; the red LED gets brighter and dimmer with the knob (pot_dimmer). Landscape, steady, knob and LED in frame, room slightly dim so the brightness change is clear.",
        "C1": "MULTIMETER, hands-free, 8-10 s: pot_read running; probes on the knob's middle leg strip and the minus rail (DC volts). One hand turns the knob from one end to the other and the display sweeps 0.0 -> ~3.3 V. Meter display readable.",
        "C2": "USB unplugged, close-up from above, 8-12 s: potentiometer in the upper breadboard; left leg -> minus rail, right leg -> 3V3 rail, middle leg -> wire to D34. Exact columns: see the lesson README drawing.",
        "C3": "pot_dimmer, full screen, 6-8 s: slow turn of the knob, the red LED follows. (Can be the same take as C0.)",
        "C4": "pot_zones, full screen, 8-10 s: slow turn through the three zones, the LED clearly steps dim -> medium -> full (and back). Slightly dim room.",
    },
    "segments": S,
}
out = Path(__file__).with_name("script.json")
out.write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
print(out, len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
