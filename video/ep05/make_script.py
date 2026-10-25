"""Source of video/ep05/script.json (kept as Python so long lines stay readable).
Usage: python video/ep05/make_script.py

Episode 5 "PWM and RGB Color Mixing" (2026-10-25), follows video/PRODUCTION_GUIDELINES.md:
cold open with the working result, sting after it, naive way first (for + delay fade) then the millis() fade,
quick questions, one multimeter clip (CURRICULUM.md), subtle like/subscribe icons in the scenes (section 5),
the end invites viewers to the comments. Not a mini-project: no challenge-solution Short is promised.
Hardware: two breadboards (episode 4); red LED GPIO 23 + button GPIO 22 on the lower one; the green LED
comes off the upper one and an RGB LED takes its place: red GPIO 25, green GPIO 26, blue GPIO 27.
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
s("cold1", "cold", "Watch this. One LED breathes in and out, smoothly. And this one mixes any color you want.",
  "İzleyin. Bir LED yumuşakça nefes alıp veriyor. Bu da istediğiniz her rengi karıştırıyor.")
s("cold2", "cold", "One press, and it jumps to the next color. And it all comes from pins that can only be on, or off.",
  "Bir basış ve sıradaki renge geçiyor. Üstelik hepsi yalnızca açık ya da kapalı olabilen pinlerden geliyor.")
s("cold3", "cold", "By the end of this video, you'll fade any LED and mix your own colors, with one function: analog write.",
  "Bu videonun sonunda her LED'i yumuşakça yakıp söndürecek ve kendi renklerinizi karıştıracaksınız; tek bir fonksiyonla: analogWrite.",
  sub="By the end of this video, you'll fade any LED and mix your own colors, with one function: analogWrite().")
# ---- parts
s("parts", "parts", "You need last episode's circuit, with the red LED and the button. Plus one RGB LED, three more two-hundred-twenty ohm resistors, and a few wires. A multimeter is a nice extra.",
  "Geçen bölümün devresi gerekiyor: kırmızı LED ve buton. Bir de bir RGB LED, üç tane daha 220 ohm direnç ve birkaç kablo. Multimetre de güzel bir ekstra.",
  sub="You need last episode's circuit, with the red LED and the button. Plus one RGB LED, three more 220 Ω resistors, and a few wires. A multimeter is a nice extra.")
# ---- PWM: the idea
s("pwm1", "pwm", "Let's start with the red LED on GPIO twenty-three. So far, digital write gave us two choices: fully on, or fully off.",
  "Kırmızı LED ile, GPIO 23 ile başlayalım. Şimdiye kadar digitalWrite bize iki seçenek verdi: tamamen açık ya da tamamen kapalı.",
  sub="Let's start with the red LED on GPIO 23. So far, digitalWrite gave us two choices: fully on, or fully off.")
s("pwm2", "pwm", "Quick question: how could a pin that's only ever on or off make the LED glow at half brightness? Think about it for a second.",
  "Kısa bir soru: yalnızca açık ya da kapalı olabilen bir pin, LED'i nasıl yarı parlaklıkta yakabilir? Bir saniye düşünün.", pad=THINK)
s("pwm3", "pwm", "The answer: switch it on and off very fast, much faster than your eyes can follow. On half the time, off half the time, and your eye sees half brightness.",
  "Cevap: onu çok hızlı açıp kapatmak, gözünüzün takip edemeyeceği kadar hızlı. Yarı zaman açık, yarı zaman kapalı; gözünüz yarı parlaklık görür.")
s("pwm4", "pwm", "This is called PWM, pulse width modulation. The pin repeats a short cycle, about a thousand times a second. What changes is how long it stays on in each cycle. That's the duty cycle.",
  "Buna PWM, yani darbe genişlik modülasyonu denir. Pin kısa bir döngüyü saniyede yaklaşık bin kez tekrarlar. Değişen şey, her döngüde ne kadar açık kaldığıdır. Buna doluluk oranı, yani duty cycle denir.")
s("pwm5", "pwm", "Twenty-five percent on looks dim. Fifty percent, medium. A hundred percent, fully bright.",
  "Yüzde 25 açık loş görünür. Yüzde 50, orta. Yüzde 100, tam parlak.",
  sub="25% on looks dim. 50%, medium. 100%, fully bright.")
# ---- analogWrite
s("aw1", "aw", "In code, it's one function: analog write. Give it a pin, and a number from zero to two hundred fifty-five. Zero is always off. Two fifty-five is always on.",
  "Kodda bu tek bir fonksiyon: analogWrite. Ona bir pin ve sıfır ile 255 arasında bir sayı verin. Sıfır her zaman kapalı. 255 her zaman açık.",
  sub="In code, it's one function: analogWrite(). Give it a pin, and a number from 0 to 255. 0 is always off. 255 is always on.")
s("aw2", "aw", "So sixty-four is about twenty-five percent, and one twenty-eight is about fifty. The sketch PWM levels steps through them, two seconds each, and prints every step.",
  "Yani 64 yaklaşık yüzde 25, 128 de yaklaşık yüzde 50 eder. pwm_levels adlı sketch bunları ikişer saniye gösterir ve her adımı yazdırır.",
  sub="So 64 is about 25%, and 128 is about 50%. The sketch pwm_levels steps through them, two seconds each, and prints every step.")
s("aw2b", "aw", "And on the ESP32, almost every output pin can do PWM. On many classic Arduino boards, only a few marked pins can. Here, you just pick a pin.",
  "ESP32'de neredeyse her çıkış pini PWM yapabilir. Birçok klasik Arduino kartında yalnızca işaretli birkaç pin yapabilir. Burada bir pin seçmeniz yeterli.")
s("aw3", "aw", "Here's a neat check. Put a multimeter on the LED pin. It can't follow the fast switching, so it shows the average: about zero point eight volts at twenty-five percent, one point six five at fifty, and three point three at a hundred.",
  "Güzel bir kontrol: multimetreyi LED pinine bağlayın. Hızlı açıp kapanmayı takip edemez, bu yüzden ortalamayı gösterir: yüzde 25'te yaklaşık 0,8 volt, yüzde 50'de 1,65, yüzde 100'de 3,3 volt.",
  sub="Here's a neat check. Put a multimeter on the LED pin. It can't follow the fast switching, so it shows the average: about 0.8 V at 25%, 1.65 V at 50%, and 3.3 V at 100%.",
  clip="C1", pad=3.0)
# ---- the fade: naive first, then millis()
s("fd1", "fade", "Now let's make it breathe. The obvious way: a for loop that counts the brightness up from zero to two fifty-five, with a short delay on every step. Then another loop counts back down.",
  "Şimdi nefes aldıralım. Akla gelen ilk yol: parlaklığı sıfırdan 255'e sayan bir for döngüsü, her adımda kısa bir delay. Sonra başka bir döngü geri sayar.",
  sub="Now let's make it breathe. The obvious way: a for loop that counts the brightness up from 0 to 255, with a short delay on every step. Then another loop counts back down.")
s("fd2", "fade", "Quick question: while that loop is fading, what happens if you press the button?",
  "Kısa bir soru: döngü parlaklığı değiştirirken butona basarsanız ne olur?", pad=THINK)
s("fd3", "fade", "Nothing. It's the problem from last episode: delay blocks. The ESP32 only looks at the button after a whole fade, two seconds of not listening.",
  "Hiçbir şey. Geçen bölümdeki sorun: delay engeller. ESP32 butona ancak bütün bir geçiş bittikten sonra bakar; iki saniye boyunca dinlemez.")
s("fd4", "fade", "So we use the trick from episode four. Every four milliseconds, we take one small step: brightness plus step. Two hundred fifty-five steps take about one second.",
  "Bu yüzden dördüncü bölümdeki yöntemi kullanıyoruz. Her dört milisaniyede bir küçük adım atıyoruz: parlaklık artı adım. 255 adım yaklaşık bir saniye sürer.",
  sub="So we use the trick from episode 4. Every 4 milliseconds, we take one small step: brightness plus step. 255 steps take about one second.")
s("fd5", "fade", "At the top, step becomes minus one, and the LED fades down. At the bottom, it becomes plus one again.",
  "Tepeye varınca adım eksi bir olur ve LED kısılır. Dibe varınca yine artı bir olur.")
s("fd5b", "fade", "Want to see the fade as a picture? Print the brightness in the loop, and open the Serial Plotter, right next to the Serial Monitor. It draws a neat triangle: up for one second, down for one second.",
  "Geçişi bir resim olarak görmek ister misiniz? Parlaklığı loop'ta yazdırın ve Serial Monitor'ün hemen yanındaki Serial Plotter'ı açın. Düzgün bir üçgen çizer: bir saniye yukarı, bir saniye aşağı.")
s("fd5c", "fade", "Quick question: if we change the four milliseconds to ten, what changes in that picture?",
  "Kısa bir soru: dört milisaniyeyi ona çıkarırsak o resimde ne değişir?", pad=THINK)
s("fd5d", "fade", "The triangle gets wider. Each step waits longer, so one fade takes about two and a half seconds. A slower, calmer breath. The height stays the same: still zero to two fifty-five.",
  "Üçgen genişler. Her adım daha uzun sürdüğü için bir geçiş yaklaşık iki buçuk saniye alır. Daha yavaş, daha sakin bir nefes. Yükseklik aynı kalır: yine sıfır ile 255 arası.",
  sub="The triangle gets wider. Each step waits longer, so one fade takes about 2.5 seconds. A slower, calmer breath. The height stays the same: still 0 to 255.")
s("fd6", "fade", "And because the loop never waits, a press pauses the fade instantly. This sketch is fade millis.",
  "Loop hiç beklemediği için bir basış geçişi anında durdurur. Bu sketch'in adı fade_millis.",
  sub="And because the loop never waits, a press pauses the fade instantly. This sketch is fade_millis.", clip="C2", pad=2.5)
# ---- RGB: wiring
s("rgb1", "rgb", "Part two: color. An RGB LED is really three tiny LEDs in one package: red, green and blue. It has four legs, and the longest one is shared by all three.",
  "İkinci kısım: renk. Bir RGB LED aslında tek pakette üç küçük LED'dir: kırmızı, yeşil ve mavi. Dört bacağı var; en uzun bacağı üçü ortak kullanır.")
s("rgb2", "rgb", "Unplug the USB cable, and take the green LED from last episode off the upper breadboard. We need its pin.",
  "USB kablosunu çıkarın ve geçen bölümdeki yeşil LED'i üstteki breadboard'dan sökün. Onun pinine ihtiyacımız var.")
s("rgb3", "rgb", "Push the RGB LED into the upper breadboard, with the longest leg second from the left. A black wire takes that long leg to the minus rail.",
  "RGB LED'i üstteki breadboard'a, en uzun bacağı soldan ikinci olacak şekilde takın. Siyah bir kablo o uzun bacağı eksi raya götürür.")
s("rgb4", "rgb", "Each color gets its own two-hundred-twenty ohm resistor and its own pin: red to D twenty-five, green to D twenty-six, and blue to D twenty-seven.",
  "Her rengin kendi 220 ohm direnci ve kendi pini var: kırmızı D25'e, yeşil D26'ya, mavi D27'ye.",
  sub="Each color gets its own 220 Ω resistor and its own pin: red to D25, green to D26, and blue to D27.", clip="C3", pad=4.0)
s("rgb4b", "rgb", "Why three resistors, and not one on the shared leg? Because each color is its own LED, with its own current. One shared resistor would let the colors steal current from each other, and the mix would change.",
  "Neden ortak bacakta tek direnç değil de üç direnç? Çünkü her renk kendi akımı olan ayrı bir LED. Ortak tek bir direnç renklerin birbirinden akım çalmasına yol açar ve karışım değişir.")
s("rgb5", "rgb", "One thing to check: most kits have common cathode LEDs, where the long leg goes to ground. If yours is common anode, the long leg goes to three point three volts, and the colors come out inverted. The code has one line for that.",
  "Bir şeyi kontrol edin: çoğu sette ortak katotlu LED olur; uzun bacak toprağa gider. Sizinki ortak anotluysa uzun bacak 3,3 volta gider ve renkler ters çıkar. Kodda bunun için tek bir satır var.",
  sub="One thing to check: most kits have common cathode LEDs, where the long leg goes to ground. If yours is common anode, the long leg goes to 3.3 V, and the colors come out inverted. The code has one line for that.")
# ---- setColor
s("col1", "color", "To set a color, we write a small helper function: set color, with three numbers, red, green and blue, each from zero to two fifty-five.",
  "Bir renk ayarlamak için küçük bir yardımcı fonksiyon yazıyoruz: setColor; üç sayı alıyor, kırmızı, yeşil ve mavi, her biri sıfır ile 255 arası.",
  sub="To set a color, we write a small helper function: setColor(), with three numbers, red, green and blue, each from 0 to 255.")
s("col2", "color", "Inside, it simply calls analog write three times, once for each pin. Now one line sets any color.",
  "İçinde analogWrite'ı üç kez çağırıyor, her pin için bir kez. Artık tek satır herhangi bir rengi ayarlıyor.",
  sub="Inside, it simply calls analogWrite() three times, once for each pin. Now one line sets any color.")
s("col3", "color", "Quick question: red two fifty-five, green zero, blue two fifty-five. What color do you get?",
  "Kısa bir soru: kırmızı 255, yeşil sıfır, mavi 255. Hangi rengi elde edersiniz?",
  sub="Quick question: red 255, green 0, blue 255. What color do you get?", pad=THINK)
s("col4", "color", "Magenta, a pinkish purple. Red and green make yellow, green and blue make cyan, and all three together make white.",
  "Macenta, pembemsi bir mor. Kırmızı ile yeşil sarı yapar, yeşil ile mavi camgöbeği yapar, üçü birlikte beyaz yapar.")
s("col5", "color", "And you're not limited to full values. Red two fifty-five with a little green, just forty, gives orange. That's over sixteen million possible colors.",
  "Üstelik tam değerlerle sınırlı değilsiniz. Kırmızı 255 ve biraz yeşil, sadece 40, turuncu verir. Bu, on altı milyondan fazla olası renk demek.",
  sub="And you're not limited to full values. Red 255 with a little green, just 40, gives orange. That's over sixteen million possible colors.")
s("col5b", "color", "One more tip: the three colors aren't equally bright. Green usually looks the strongest. If your white looks a little greenish, try green at two hundred instead of two fifty-five.",
  "Bir ipucu daha: üç renk eşit parlak değildir. Yeşil genelde en güçlü görünür. Beyazınız biraz yeşilimsi duruyorsa yeşili 255 yerine 200 deneyin.",
  sub="One more tip: the three colors aren't equally bright. Green usually looks the strongest. If your white looks a little greenish, try green at 200 instead of 255.")
s("col6", "color", "The sketch RGB colors steps through them, one per second.",
  "rgb_colors adlı sketch bunları saniyede bir gösteriyor.",
  sub="The sketch rgb_colors steps through them, one per second.", clip="C4", pad=2.5)
# ---- modes with the button
s("mode1", "modes", "Finally, the button picks the color. We keep a variable called mode. Every new press adds one, and after the last mode, it goes back to zero.",
  "Son olarak rengi buton seçsin. mode adında bir değişken tutuyoruz. Her yeni basış ona bir ekliyor; son moddan sonra yeniden sıfıra dönüyor.")
s("mode1b", "modes", "Quick question: mode is three, and you press again. What happens?",
  "Kısa bir soru: mode üç ve tekrar basıyorsunuz. Ne olur?", pad=THINK)
s("mode1c", "modes", "It becomes four for a moment, but the very next line checks: is mode greater than three? Yes, so it goes back to zero, and we're on red again. Four modes, in a circle.",
  "Bir anlığına dört olur, ama hemen sonraki satır kontrol eder: mode üçten büyük mü? Evet, o yüzden sıfıra döner ve yine kırmızıdayız. Dört mod, bir daire gibi.")
s("mode2", "modes", "Then, an if for each mode: zero is red, one is green, two is blue, and three is a slow fade from blue to red, with the same millis step as before.",
  "Sonra her mod için bir if: sıfır kırmızı, bir yeşil, iki mavi; üç ise maviden kırmızıya yavaş bir geçiş, öncekiyle aynı millis adımıyla.")
s("mode3", "modes", "Press, and it changes instantly, even in the middle of the fade. That's color modes.",
  "Basın; anında değişiyor, geçişin ortasında bile. Bu sketch'in adı color_modes.",
  sub="Press, and it changes instantly, even in the middle of the fade. That's color_modes.", clip="C5", pad=2.5)
# ---- your turn (not a mini-project: the solution stays in the lesson folder)
s("ch1", "challenge", "Your turn: build a smart camping headlamp. One button cycles four modes: off, dim white, bright white, and red blink.",
  "Sıra sizde: akıllı bir kamp kafa lambası yapın. Tek buton dört mod arasında geçiş yapsın: kapalı, loş beyaz, parlak beyaz ve yanıp sönen kırmızı.")
s("ch2", "challenge", "The twist: if the lamp has been on for three seconds or more, the next press switches it straight off. Hint: remember when the mode last changed. Post your solution in the comments. One solution is in the lesson folder.",
  "İşin püf noktası: lamba üç saniye ya da daha uzun süredir açıksa, sıradaki basış onu doğrudan kapatsın. İpucu: modun en son ne zaman değiştiğini hatırlayın. Çözümünüzü yorumlara yazın. Bir çözüm ders klasöründe.")
# ---- troubleshooting
s("tr1", "trouble", "Something not working? If one color never lights, check that leg's resistor and wire. If everything is inverted, white when it should be off, your LED is common anode: set common anode to true, and move the long leg to three point three volts.",
  "Bir şey çalışmıyor mu? Bir renk hiç yanmıyorsa o bacağın direncini ve kablosunu kontrol edin. Her şey tersse, sönük olması gerekirken beyazsa, LED'iniz ortak anotludur: COMMON_ANODE'u true yapın ve uzun bacağı 3,3 volta taşıyın.",
  sub="Something not working? If one color never lights, check that leg's resistor and wire. If everything is inverted, white when it should be off, your LED is common anode: set COMMON_ANODE to true, and move the long leg to 3.3 V.")
# ---- outro
s("out1", "outro", "Today, we used PWM to dim an LED, built a fade that never waits, and mixed colors with an RGB LED and our own set color function.",
  "Bugün PWM ile bir LED'i kıstık, hiç beklemeyen bir geçiş yaptık ve bir RGB LED ile kendi setColor fonksiyonumuzla renk karıştırdık.",
  sub="Today, we used PWM to dim an LED, built a fade that never waits, and mixed colors with an RGB LED and our own setColor() function.")
s("out2", "outro", "Next time: a knob. We'll read a potentiometer with analog read, and turn it into brightness and color. Let's meet in the comments: tell me which color you mixed. See you there!",
  "Gelecek sefer: bir düğme. Bir potansiyometreyi analogRead ile okuyup parlaklığa ve renge dönüştüreceğiz. Yorumlarda buluşalım: hangi rengi karıştırdığınızı yazın. Görüşmek üzere!",
  sub="Next time: a knob. We'll read a potentiometer with analogRead(), and turn it into brightness and color. Let's meet in the comments: tell me which color you mixed. See you there!")

NAMES = {}
for i, d in enumerate(S):
    NAMES[d["id"]] = f"s{i + 1:02d}"
    d["id"] = NAMES[d["id"]]

script = {
    "episode": 5, "title": "PWM and RGB Color Mixing", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": NAMES["cold3"],
    "clips": {
        "C0": "OPENING, full screen, 14-16 s: the red LED breathing (fade_millis) and the RGB LED changing colour (color_modes in mode 3, then ~8 s in one press to the next mode). Landscape, steady, both LEDs and the button in frame; the RGB LED in the CENTRE (the Short crops a square from the middle).",
        "C1": "MULTIMETER, hands-free, 8-10 s: pwm_levels running; probes on the red LED's GPIO 23 strip and the minus rail (DC volts). The reading steps 0 -> ~0.8 -> ~1.65 -> ~3.3 V while the LED gets brighter. Meter display readable.",
        "C2": "fade_millis, full screen, 6-8 s: the red LED breathes; one press pauses it mid-fade, another press resumes.",
        "C3": "USB unplugged, close-up from above, 8-12 s: green LED off the upper breadboard; RGB LED in (longest leg second from the left), black wire long leg -> minus rail, three 220 ohm resistors + wires to D25 (red), D26 (green), D27 (blue). Exact columns: see the lesson README drawing.",
        "C4": "rgb_colors, full screen, 8 s: the RGB LED steps red, green, blue, yellow, magenta, cyan, white, orange. Slightly dim room so the colours are clear.",
        "C5": "color_modes, full screen, 8 s: three presses (red -> green -> blue -> fade), the fade starts.",
        "NOTE": "Before filming: upload rgb_colors once. If you see white when it should be off, the RGB LED is common anode: move its long leg to 3V3 and set COMMON_ANODE = true in all three RGB sketches; tell Claude so the drawing and narration can be adjusted.",
    },
    "segments": S,
}
out = Path(__file__).with_name("script.json")
out.write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
print(out, len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
