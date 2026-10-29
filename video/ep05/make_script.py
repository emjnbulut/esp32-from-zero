"""Source of video/ep05-1/script.json (and dub/tr.json). Usage: python video/ep05/make_script.py

Episode 5 "PWM: Make an LED Breathe" (curriculum v6, 2026-10-29: was "Episode 5 · Part 1"). Written from the start in the settled style
(PRODUCTION_GUIDELINES.md sections 9 and 10, video/ANALOGIES.md): everyday picture -> objective meaning ("What actually
happens") -> the limit of the picture ("The difference") -> code; retrieval minute after the sting; every sketch in PRIMM
order (predict, run, inspect with a prediction pause, modify); one common-mistake scene (fade_naive); one "in your own
words" invitation; no music under the narration ("music": "results").
Reuses the ideas and pictures of the v2 draft (video/ep05/make_script.v2-draft.py): ceiling fan, tap, dimmer knob,
recipe with a blank, stairs with headphones, wall clock, swing. Episode 6 (RGB) is video/ep06.
Clips = shoot pack p05 (video/shoot/make_pack.py): C0 opening, C1 multimeter, C2 pwm_levels, C3 fade_naive mistake,
C4 fade_millis run, C5 modify (4 -> 10).
Each s(...) gives: id, scene, English narration (numbers spelled out), Turkish subtitle text, Turkish spoken text
(numbers as words, English terms spelled the way a Turkish speaker says them), optional English subtitle with digits.
"""
import json
from pathlib import Path

S = []
THINK = 2.6  # silence after a "quick question"


def s(id, scene, text, tr, dub=None, sub=None, **kw):
    d = {"id": id, "scene": scene, "text": text}
    if sub:
        d["sub"] = sub
    d["tr"] = tr
    d["dub"] = dub or tr
    d.update(kw)
    S.append(d)


# ---- cold open: the result first
s("s01", "cold", "Watch this LED. It slowly gets brighter, then dimmer, again and again, like someone breathing in their sleep.",
  "Şu LED'e bakın. Yavaşça parlıyor, sonra kısılıyor, tekrar tekrar; uykuda nefes alan biri gibi.",
  "Şu lede bakın. Yavaşça parlıyor, sonra kısılıyor, tekrar tekrar; uykuda nefes alan biri gibi.", clip="C0")
s("s02", "cold", "And when I press the button, it stops at once, right in the middle of a breath. Press again, and it carries on.",
  "Butona bastığımda da hemen duruyor, tam bir nefesin ortasında. Bir daha basınca kaldığı yerden devam ediyor.")
s("s03", "cold", "Yet this pin can only be fully on, or fully off. By the end of this video, you'll know the trick, and you'll make any LED breathe.",
  "Oysa bu pin yalnızca tamamen açık ya da tamamen kapalı olabiliyor. Bu videonun sonunda hileyi öğrenmiş olacaksınız ve her LED'i nefes aldırabileceksiniz.",
  "Oysa bu pin yalnızca tamamen açık ya da tamamen kapalı olabiliyor. Bu videonun sonunda hileyi öğrenmiş olacaksınız ve her ledi nefes aldırabileceksiniz.")
# ---- retrieval minute (episode 4 + recap)
s("s04", "retrieval", "Before we start, two questions from earlier episodes. Quick question: the button uses the built-in pull-up resistor. While you press it, does the pin read HIGH or LOW?",
  "Başlamadan önce önceki bölümlerden iki soru. Kısa bir soru: buton, çipin içindeki pull-up direncini kullanıyor. Butona basılıyken pin HIGH mı okur, LOW mu?",
  "Başlamadan önce önceki bölümlerden iki soru. Kısa bir soru: buton, çipin içindeki pul ap direncini kullanıyor. Butona basılıyken pin hay mı okur, lov mu?",
  pad=THINK)
s("s05", "retrieval", "LOW. Pressing connects the pin to ground, and ground wins against the weak resistor inside the chip that pulls it up.",
  "LOW. Basınca pin toprağa bağlanıyor ve toprak, çipin içinde pini yukarı çeken zayıf dirence karşı kazanıyor.",
  "Lov. Basınca pin toprağa bağlanıyor ve toprak, çipin içinde pini yukarı çeken zayıf dirence karşı kazanıyor.")
s("s06", "retrieval", "Quick question: why does a long delay make the board miss a button press?",
  "Kısa bir soru: uzun bir delay neden kartın bir buton basışını kaçırmasına yol açar?",
  "Kısa bir soru: uzun bir dilay neden kartın bir buton basışını kaçırmasına yol açar?", pad=THINK)
s("s07", "retrieval", "Because during a delay, the program simply stops, and nobody looks at the button. Keep that in mind: it comes back today.",
  "Çünkü delay sırasında program düpedüz durur ve butona kimse bakmaz. Bunu aklınızda tutun: bugün yeniden karşımıza çıkacak.",
  "Çünkü dilay sırasında program düpedüz durur ve butona kimse bakmaz. Bunu aklınızda tutun: bugün yeniden karşımıza çıkacak.")
# ---- parts
s("s08", "parts", "You only need the circuit from episode four: the red LED on GPIO twenty-three, and the button on GPIO twenty-two. A multimeter is a nice extra.",
  "Yalnızca dördüncü bölümün devresi gerekiyor: GPIO 23'teki kırmızı LED ve GPIO 22'deki buton. Multimetre de güzel bir ekstra.",
  "Yalnızca dördüncü bölümün devresi gerekiyor: Ge Pe I O yirmi üçteki kırmızı led ve Ge Pe I O yirmi ikideki buton. Multimetre de güzel bir ekstra.",
  sub="You only need the circuit from episode 4: the red LED on GPIO 23, and the button on GPIO 22. A multimeter is a nice extra.")
# ---- PWM: the idea
s("s09", "pwm", "So far, digital write gave us two choices, like an ordinary light switch: fully on, or fully off.",
  "Şimdiye kadar digitalWrite bize, sıradan bir ışık anahtarı gibi, yalnızca iki seçenek verdi: tamamen açık ya da tamamen kapalı.",
  "Şimdiye kadar dijital rayt bize, sıradan bir ışık anahtarı gibi, yalnızca iki seçenek verdi: tamamen açık ya da tamamen kapalı.",
  sub="So far, digitalWrite() gave us two choices, like an ordinary light switch: fully on, or fully off.")
s("s10", "pwm", "Quick question: how could a pin that's only ever on or off make an LED glow at half brightness? Think about it for a moment.",
  "Kısa bir soru: yalnızca açık ya da kapalı olabilen bir pin, bir LED'i nasıl yarı parlaklıkta yakabilir? Bir an düşünün.",
  "Kısa bir soru: yalnızca açık ya da kapalı olabilen bir pin, bir ledi nasıl yarı parlaklıkta yakabilir? Bir an düşünün.", pad=THINK)
s("s11", "pwm", "The answer is speed. Think of a ceiling fan. When it spins fast, you can't see the single blades anymore, only a soft blur.",
  "Cevap hız. Bir tavan vantilatörünü düşünün. Hızlı dönünce kanatları tek tek göremezsiniz, yalnızca yumuşak bir bulanıklık görürsünüz.")
s("s12", "pwm", "The pin does the same with light. It switches the LED on and off about a thousand times a second, and your eye only sees the average.",
  "Pin de ışıkla aynısını yapıyor. LED'i saniyede yaklaşık bin kez açıp kapatıyor ve gözünüz yalnızca ortalamayı görüyor.",
  "Pin de ışıkla aynısını yapıyor. Ledi saniyede yaklaşık bin kez açıp kapatıyor ve gözünüz yalnızca ortalamayı görüyor.")
s("s13", "pwm", "This trick is called PWM, short for pulse width modulation. What actually happens: the pin is always at either three point three volts, or zero volts. Only the timing changes.",
  "Bu yönteme PWM deniyor, yani darbe genişlik modülasyonu. Gerçekte olan şu: pin her an ya 3,3 volttadır ya da sıfır volttadır. Değişen yalnızca zamanlama.",
  "Bu yönteme Pe Ve Me deniyor, yani darbe genişlik modülasyonu. Gerçekte olan şu: pin her an ya üç virgül üç volttadır ya da sıfır volttadır. Değişen yalnızca zamanlama.",
  sub="This trick is called PWM, short for pulse width modulation. What actually happens: the pin is always at either 3.3 V, or 0 V. Only the timing changes.")
s("s14", "pwm", "The difference from the fan: a fan really passes through every position in between. The LED is only ever fully on, or fully off, and the in-between happens in your eye.",
  "Vantilatörden farkı şu: vantilatör aradaki her konumdan gerçekten geçer. LED ise ya tamamen açıktır ya tamamen kapalı; aradaki ton sizin gözünüzde oluşur.",
  "Vantilatörden farkı şu: vantilatör aradaki her konumdan gerçekten geçer. Led ise ya tamamen açıktır ya tamamen kapalı; aradaki ton sizin gözünüzde oluşur.")
# ---- duty cycle
s("s15", "duty", "What we control is how long the pin stays on in each short cycle. That share is called the duty cycle.",
  "Bizim kontrol ettiğimiz şey, pinin her kısa döngüde ne kadar süre açık kaldığı. Bu paya doluluk oranı deniyor; İngilizcesi duty cycle.",
  "Bizim kontrol ettiğimiz şey, pinin her kısa döngüde ne kadar süre açık kaldığı. Bu paya doluluk oranı deniyor; İngilizcesi duti sayk ıl.")
s("s16", "duty", "Think of a tap that you open briefly every second. Open it for a quarter of each second, and only a little water flows. Leave it open, and you get the full stream.",
  "Her saniye kısa bir an açtığınız bir musluk düşünün. Her saniyenin dörtte birinde açarsanız biraz su akar. Açık bırakırsanız tam akışı alırsınız.")
s("s17", "duty", "The difference: a real tap can be half open, but a PWM pin is never half on.",
  "Farkı şu: gerçek bir musluk yarı açık olabilir, ama bir PWM pini asla yarı açık olmaz.",
  "Farkı şu: gerçek bir musluk yarı açık olabilir, ama bir Pe Ve Me pini asla yarı açık olmaz.")
s("s18", "duty", "So twenty-five percent on looks dim, fifty percent looks medium, and a hundred percent is fully bright.",
  "Yani yüzde 25 açık loş görünür, yüzde 50 orta görünür, yüzde 100 ise tam parlaktır.",
  "Yani yüzde yirmi beş açık loş görünür, yüzde elli orta görünür, yüzde yüz ise tam parlaktır.",
  sub="So 25% on looks dim, 50% looks medium, and 100% is fully bright.")
# ---- analogWrite
s("s19", "aw", "In code, all of this is one function: analog write. You give it a pin, and a number from zero to two hundred fifty-five.",
  "Kodda bunların hepsi tek bir fonksiyon: analogWrite. Ona bir pin ve sıfır ile 255 arasında bir sayı veriyorsunuz.",
  "Kodda bunların hepsi tek bir fonksiyon: analog rayt. Ona bir pin ve sıfır ile iki yüz elli beş arasında bir sayı veriyorsunuz.",
  sub="In code, all of this is one function: analogWrite(). You give it a pin, and a number from 0 to 255.")
s("s20", "aw", "It works like a dimmer knob with many small clicks: zero is always off, and two fifty-five is always on. Quick question: which number gives about half brightness?",
  "Çok sayıda küçük kademesi olan bir dimmer düğmesi gibi çalışıyor: sıfır hep kapalı, 255 hep açık. Kısa bir soru: hangi sayı yaklaşık yarı parlaklık verir?",
  "Çok sayıda küçük kademesi olan bir dimır düğmesi gibi çalışıyor: sıfır hep kapalı, iki yüz elli beş hep açık. Kısa bir soru: hangi sayı yaklaşık yarı parlaklık verir?",
  sub="It works like a dimmer knob with many small clicks: 0 is always off, and 255 is always on. Quick question: which number gives about half brightness?", pad=THINK)
s("s21", "aw", "About one twenty-eight, on for half of every cycle. The difference from a real dimmer: a real one turns smoothly, but this one has exactly two hundred fifty-six steps.",
  "Yaklaşık 128; her döngünün yarısında açık. Gerçek bir dimmerdan farkı şu: gerçeği kesintisiz döner, bu ise tam 256 adımdan oluşur.",
  "Yaklaşık yüz yirmi sekiz; her döngünün yarısında açık. Gerçek bir dimırdan farkı şu: gerçeği kesintisiz döner, bu ise tam iki yüz elli altı adımdan oluşur.",
  sub="About 128, on for half of every cycle. The difference from a real dimmer: a real one turns smoothly, but this one has exactly 256 steps.")
# ---- code tour: pwm_levels (predict -> run -> inspect -> modify)
s("s23", "tourpwm", "Here is the first sketch, PWM levels. At the top, pin twenty-three gets a name. Setup makes it an output, and starts the Serial Monitor.",
  "İşte ilk sketch: pwm_levels. En üstte 23. pine bir ad veriyoruz. setup onu çıkış yapıyor ve Seri Monitör'ü başlatıyor.",
  "İşte ilk sketç: Pe Ve Me levıls. En üstte yirmi üçüncü pine bir ad veriyoruz. Set ap onu çıkış yapıyor ve Seri Monitörü başlatıyor.",
  sub="Here is the first sketch, pwm_levels. At the top, pin 23 gets a name. setup() makes it an output, and starts the Serial Monitor.")
s("s24", "tourpwm", "Then something new: our own function, show level. Think of it as a recipe with a blank: the number in the brackets fills that blank on every call.",
  "Sonra yeni bir şey: kendi fonksiyonumuz, showLevel. Bunu boşluğu olan bir tarif gibi düşünün: parantezdeki sayı her çağrıda o boşluğu dolduruyor.",
  "Sonra yeni bir şey: kendi fonksiyonumuz, şov levıl. Bunu boşluğu olan bir tarif gibi düşünün: parantezdeki sayı her çağrıda o boşluğu dolduruyor.",
  sub="Then something new: our own function, showLevel(). Think of it as a recipe with a blank: the number in the brackets fills that blank on every call.")
s("s25", "tourpwm", "What actually happens: when we call show level with sixty-four, the value inside the function becomes sixty-four. Analog write uses it, the sketch prints it, and then waits two seconds.",
  "Gerçekte olan şu: showLevel'ı 64 ile çağırdığımızda fonksiyonun içindeki value 64 oluyor. analogWrite onu kullanıyor, sketch onu yazdırıyor ve sonra iki saniye bekliyor.",
  "Gerçekte olan şu: şov levıli altmış dört ile çağırdığımızda fonksiyonun içindeki velyu altmış dört oluyor. Analog rayt onu kullanıyor, sketç onu yazdırıyor ve sonra iki saniye bekliyor.",
  sub="What actually happens: when we call showLevel() with 64, the value inside the function becomes 64. analogWrite() uses it, the sketch prints it, and then waits two seconds.")
s("s26", "tourpwm", "The difference from a paper recipe: the function forgets the value as soon as it finishes.",
  "Kâğıttaki bir tariften farkı şu: fonksiyon işi biter bitmez o değeri unutur.")
s("s27", "tourpwm", "The loop calls show level four times: with zero, sixty-four, one twenty-eight, and two fifty-five. Pause the video and predict: what will the LED do at each step?",
  "loop, showLevel'ı dört kez çağırıyor: sıfır, 64, 128 ve 255 ile. Videoyu durdurun ve tahmin edin: LED her adımda ne yapacak?",
  "Lup, şov levıli dört kez çağırıyor: sıfır, altmış dört, yüz yirmi sekiz ve iki yüz elli beş ile. Videoyu durdurun ve tahmin edin: led her adımda ne yapacak?",
  sub="The loop calls showLevel() four times: with 0, 64, 128, and 255. Pause the video and predict: what will the LED do at each step?", pad=3.0)
s("s28", "run", "Let's run it. The LED steps up in four clear levels: off, dim, medium, and fully bright. Then it starts again from the top.",
  "Çalıştıralım. LED dört belirgin seviyede parlıyor: kapalı, loş, orta ve tam parlak. Sonra en baştan yeniden başlıyor.",
  "Çalıştıralım. Led dört belirgin seviyede parlıyor: kapalı, loş, orta ve tam parlak. Sonra en baştan yeniden başlıyor.", clip="C2", pad=2.5)
s("s29", "meter", "Now a multimeter on the LED pin. It's too slow to follow the switching, so it shows the average voltage.",
  "Şimdi multimetreyi LED pinine bağlayalım. Hızlı geçişi takip edemeyecek kadar yavaş, bu yüzden ortalama voltajı gösteriyor.",
  "Şimdi multimetreyi led pinine bağlayalım. Hızlı geçişi takip edemeyecek kadar yavaş, bu yüzden ortalama voltajı gösteriyor.")
s("s30", "meter", "About zero point eight volts at twenty-five percent, one point six five at fifty, and three point three at a hundred: exactly the share of the time the pin is on.",
  "Yüzde 25'te yaklaşık 0,8 volt, yüzde 50'de 1,65, yüzde 100'de 3,3 volt: tam da pinin açık kaldığı süreyle orantılı.",
  "Yüzde yirmi beşte yaklaşık sıfır virgül sekiz volt, yüzde ellide bir virgül altmış beş, yüzde yüzde üç virgül üç volt: tam da pinin açık kaldığı süreyle orantılı.",
  sub="About 0.8 V at 25%, 1.65 V at 50%, and 3.3 V at 100%: exactly the share of the time the pin is on.",
  clip="C1", pad=3.0)
s("s31", "meter", "Your turn: replace sixty-four with ten. What do you think you'll see? A very faint glow, and about a tenth of a volt.",
  "Sıra sizde: 64 yerine 10 yazın. Sizce ne göreceksiniz? Çok sönük bir ışık ve voltun onda biri kadar bir değer.",
  "Sıra sizde: altmış dört yerine on yazın. Sizce ne göreceksiniz? Çok sönük bir ışık ve voltun onda biri kadar bir değer.",
  sub="Your turn: replace 64 with 10. What do you think you'll see? A very faint glow, and about a tenth of a volt.")
# ---- the naive fade
s("s32", "fade", "Now let's make the LED breathe. The obvious way is two for loops. One counts the brightness up with a tiny delay on every step, and the other counts it down.",
  "Şimdi LED'i nefes aldıralım. Akla gelen ilk yol iki for döngüsü. Biri parlaklığı her adımda küçücük bir delay ile yukarı sayıyor, diğeri aşağı sayıyor.",
  "Şimdi ledi nefes aldıralım. Akla gelen ilk yol iki for döngüsü. Biri parlaklığı her adımda küçücük bir dilay ile yukarı sayıyor, diğeri aşağı sayıyor.")
# ---- common mistake: the blocking fade
s("s34", "mistake", "Quick question: while this LED is fading, what happens when you press the button?",
  "Kısa bir soru: LED kısılıp parlarken butona basarsanız ne olur?",
  "Kısa bir soru: led kısılıp parlarken butona basarsanız ne olur?", pad=THINK)
s("s35", "mistake", "Watch. I press three, four times, and the fade just carries on, as if nothing happened.",
  "İzleyin. Üç, dört kez basıyorum ve geçiş hiçbir şey olmamış gibi devam ediyor.", clip="C3", pad=2.5)
s("s36", "mistake", "It's the delay problem from the start of this video. It's like climbing stairs with headphones on: until you reach the top, you don't hear the doorbell.",
  "Bu, videonun başındaki delay sorunu. Kulaklıkla merdiven çıkmak gibi: tepeye varana kadar kapı zilini duymazsınız.",
  "Bu, videonun başındaki dilay sorunu. Kulaklıkla merdiven çıkmak gibi: tepeye varana kadar kapı zilini duymazsınız.")
s("s37", "mistake", "What actually happens: one whole fade takes about two seconds, and the button is only read between two fades. So a short press is almost always missed.",
  "Gerçekte olan şu: bütün bir geçiş yaklaşık iki saniye sürüyor ve buton yalnızca iki geçişin arasında okunuyor. Bu yüzden kısa bir basış neredeyse her zaman kaçıyor.")
s("s38", "mistake", "The difference: you might still feel a tap on your shoulder, but the board notices nothing until the loop ends.",
  "Farkı şu: siz yine de omzunuza dokunulduğunu hissedebilirsiniz, ama kart döngü bitene kadar hiçbir şey fark etmez.")
# ---- the clean fade: the clock
s("s39", "fade2", "The fix is the wall clock from episode four. We glance at it on every round, and act only when enough time has passed.",
  "Çözüm, dördüncü bölümdeki duvar saati. Her turda ona bir göz atıyoruz ve yalnızca yeterince zaman geçtiyse harekete geçiyoruz.")
s("s40", "fade2", "Every four milliseconds, we take one small step, and the brightness grows by one. Two hundred fifty-five steps take about one second.",
  "Her dört milisaniyede bir küçük adım atıyoruz ve parlaklık bir artıyor. 255 adım yaklaşık bir saniye sürüyor.",
  "Her dört milisaniyede bir küçük adım atıyoruz ve parlaklık bir artıyor. İki yüz elli beş adım yaklaşık bir saniye sürüyor.",
  sub="Every 4 milliseconds, we take one small step, and the brightness grows by one. 255 steps take about one second.")
s("s41", "fade2", "At the top, we turn around and count down. At the bottom, we turn around again, and the next breath begins.",
  "Tepeye varınca dönüp geri sayıyoruz. Dibe varınca yine dönüyoruz ve sonraki nefes başlıyor.")
# ---- code tour: fade_millis
s("s43", "tourfade", "Here's the whole sketch, fade millis. Brightness is how bright the LED is right now. Step is what we add each time: plus one going up, and minus one going down.",
  "İşte sketch'in tamamı: fade_millis. brightness, LED'in şu anki parlaklığı. step, her seferinde eklediğimiz sayı: yukarı çıkarken artı bir, aşağı inerken eksi bir.",
  "İşte sketçin tamamı: feyd milis. Braytnıs, ledin şu anki parlaklığı. Step, her seferinde eklediğimiz sayı: yukarı çıkarken artı bir, aşağı inerken eksi bir.",
  sub="Here's the whole sketch, fade_millis. brightness is how bright the LED is right now. step is what we add each time: +1 going up, and -1 going down.")
s("s44", "tourfade", "Last step holds the time of the last step, and fading says whether the LED breathes or is paused. Below them sits the button's memory from episode four.",
  "lastStep son adımın zamanını tutuyor, fading de LED'in nefes mi aldığını yoksa durmuş mu olduğunu söylüyor. Altlarında dördüncü bölümden tanıdığımız buton hafızası var.",
  "Last step son adımın zamanını tutuyor, feyding de ledin nefes mi aldığını yoksa durmuş mu olduğunu söylüyor. Altlarında dördüncü bölümden tanıdığımız buton hafızası var.",
  sub="lastStep holds the time of the last step, and fading says whether the LED breathes or is paused. Below them sits the button's memory from episode 4.")
s("s45", "tourfade", "In the loop, we read the clock once. Part one is the button from episode four. A new press flips fading, because the exclamation mark means not.",
  "loop'ta saati bir kez okuyoruz. Birinci kısım dördüncü bölümün butonu. Yeni bir basış fading'i tersine çeviriyor, çünkü ünlem işareti \"değil\" demek.",
  "Lupta saati bir kez okuyoruz. Birinci kısım dördüncü bölümün butonu. Yeni bir basış feydingi tersine çeviriyor, çünkü ünlem işareti değil demek.",
  sub="In the loop, we read the clock once. Part one is the button from episode 4. A new press flips fading, because the exclamation mark means not.")
s("s46", "tourfade", "Part two is the fade. Pause the video and predict: the LED is breathing, but only two milliseconds have passed. What does this part do?",
  "İkinci kısım geçiş. Videoyu durdurun ve tahmin edin: LED nefes alıyor ama yalnızca iki milisaniye geçmiş. Bu kısım ne yapar?",
  "İkinci kısım geçiş. Videoyu durdurun ve tahmin edin: led nefes alıyor ama yalnızca iki milisaniye geçmiş. Bu kısım ne yapar?", pad=3.0)
s("s47", "tourfade", "Nothing at all. The loop simply runs on and checks the button again, which is why a press is never missed.",
  "Hiçbir şey. Döngü yoluna devam ediyor ve butonu yeniden kontrol ediyor; bir basışın hiç kaçmamasının nedeni bu.")
s("s48", "tourfade", "When four milliseconds have passed, we note the time, and add the step to the brightness. At two fifty-five, the step becomes minus one, and at zero, plus one again.",
  "Dört milisaniye geçtiğinde zamanı not ediyoruz ve adımı parlaklığa ekliyoruz. 255'te adım eksi bir oluyor, sıfırda yeniden artı bir.",
  "Dört milisaniye geçtiğinde zamanı not ediyoruz ve adımı parlaklığa ekliyoruz. İki yüz elli beşte adım eksi bir oluyor, sıfırda yeniden artı bir.",
  sub="When 4 milliseconds have passed, we note the time, and add the step to the brightness. At 255, the step becomes -1, and at 0, +1 again.")
s("s49", "tourfade", "Finally, analog write shows the new brightness on the LED.",
  "En sonda analogWrite yeni parlaklığı LED'de gösteriyor.",
  "En sonda analog rayt yeni parlaklığı ledde gösteriyor.",
  sub="Finally, analogWrite() shows the new brightness on the LED.")
s("s50", "run2", "Let's run it. The LED breathes, and a press stops it at once, right in the middle of a fade. Press again, and it carries on.",
  "Çalıştıralım. LED nefes alıyor ve bir basış onu anında, geçişin tam ortasında durduruyor. Bir daha basınca devam ediyor.",
  "Çalıştıralım. Led nefes alıyor ve bir basış onu anında, geçişin tam ortasında durduruyor. Bir daha basınca devam ediyor.", clip="C4", pad=2.5)
s("s51", "run2", "Quick question: in line thirty-nine, we change the four to a ten. Will the breath get faster, or slower?",
  "Kısa bir soru: 39. satırdaki 4'ü 10 yapıyoruz. Nefes hızlanır mı, yavaşlar mı?",
  "Kısa bir soru: otuz dokuzuncu satırdaki dördü on yapıyoruz. Nefes hızlanır mı, yavaşlar mı?",
  sub="Quick question: in line 39, we change the 4 to a 10. Will the breath get faster, or slower?", pad=THINK)
s("s52", "run2", "Slower. Each step now waits ten milliseconds, so one way takes about two and a half seconds, and the breath feels calmer.",
  "Yavaşlar. Her adım artık on milisaniye bekliyor, yani bir yön yaklaşık iki buçuk saniye sürüyor ve nefes daha sakin görünüyor.",
  clip="C5", pad=2.0)
# ---- explain in your own words
s("s53", "explain", "Now pause the video, and explain in your own words why the button works in this sketch, but not in the first one. One or two sentences are enough.",
  "Şimdi videoyu durdurun ve butonun neden bu sketch'te çalışıp ilkinde çalışmadığını kendi cümlelerinizle açıklayın. Bir iki cümle yeter.",
  "Şimdi videoyu durdurun ve butonun neden bu sketçte çalışıp ilkinde çalışmadığını kendi cümlelerinizle açıklayın. Bir iki cümle yeter.", pad=4.0)
s("s54", "explain", "Here's one way to say it. The first sketch waited on every step, so nobody read the button. This one never waits: it glances at the clock, and moves on.",
  "Şöyle söylenebilir. İlk sketch her adımda bekliyordu, bu yüzden butonu kimse okumuyordu. Bu ise hiç beklemiyor: saate bir göz atıyor ve yoluna devam ediyor.",
  "Şöyle söylenebilir. İlk sketç her adımda bekliyordu, bu yüzden butonu kimse okumuyordu. Bu ise hiç beklemiyor: saate bir göz atıyor ve yoluna devam ediyor.")
# ---- outro
s("s55", "outro", "Today you learned three things. PWM dims an LED by switching it very fast. Analog write takes a number from zero to two fifty-five. And a fade built on the clock never stops listening.",
  "Bugün üç şey öğrendiniz. PWM, bir LED'i çok hızlı açıp kapatarak kısar. analogWrite sıfır ile 255 arasında bir sayı alır. Saate dayanan bir geçiş de dinlemeyi hiç bırakmaz.",
  "Bugün üç şey öğrendiniz. Pe Ve Me, bir ledi çok hızlı açıp kapatarak kısar. Analog rayt sıfır ile iki yüz elli beş arasında bir sayı alır. Saate dayanan bir geçiş de dinlemeyi hiç bırakmaz.",
  sub="Today you learned three things. PWM dims an LED by switching it very fast. analogWrite() takes a number from 0 to 255. And a fade built on the clock never stops listening.")
s("s56", "outro", "Next time, in episode six, we'll mix any color you like with an RGB LED. Until then, tell me in the comments: what would you make breathe? See you there!",
  "Gelecek bölümde bir RGB LED ile istediğiniz her rengi karıştıracağız. O zamana kadar yorumlarda yazın: siz neyi nefes aldırırdınız? Görüşmek üzere!",
  "Gelecek bölümde bir Ar Ce Be led ile istediğiniz her rengi karıştıracağız. O zamana kadar yorumlarda yazın: siz neyi nefes aldırırdınız? Görüşmek üzere!")
# breathing room before a new term (lesson_lint NEWTERM: >= 0.8 s of silence before it)
NEW_TERM = ("s04", "s13", "s15", "s19", "s24", "s43")
for a, b in zip(S, S[1:]):
    if b["id"] in NEW_TERM:
        a["pad"] = a.get("pad", 0) + 0.4

dub = {d["id"]: d.pop("dub") for d in S}
script = {
    "episode": 5, "title": "PWM: Make an LED Breathe", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": "s03",
    "music": "results",
    "clips": {
        "C0": "OPENING, full screen, 12-15 s: fade_millis; the red LED breathes; one press stops it at once, a second press 2 s later resumes it. Red LED and button centred.",
        "C1": "MULTIMETER, hands-free, 10-12 s: pwm_levels; probes on the red LED's GPIO 23 strip and the minus rail (DC volts). The display steps 0 -> ~0.8 -> ~1.65 -> ~3.3 V, 2 s each.",
        "C2": "pwm_levels, 10 s: the LED in four steps: off, 25 %, 50 %, 100 %. Slightly dim room.",
        "C3": "COMMON MISTAKE, 10-12 s: fade_naive; 3-4 short presses while it breathes; the fade does not stop.",
        "C4": "fade_millis, 10 s, closer than C0: a press pauses it mid-fade, another press resumes it.",
        "C5": "MODIFY, optional, 8 s: fade_millis with line 39 changed from 4 to 10; a visibly slower breath.",
    },
    "segments": S,
}
here = Path(__file__).parent
(here / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "dub").mkdir(exist_ok=True)
(here / "dub" / "tr.json").write_text(json.dumps({
    "voice": "tr-TR-EmelNeural", "rate": "+0%",
    "note": "Spoken text only. English terms are written the way a Turkish speaker says them (analog rayt, dilay, lup, set ap...).",
    "segments": dub}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
