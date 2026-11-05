"""Source of video/ep07/script.json (and dub/tr.json). Usage: python video/ep07/make_script.py

Episode 7 "Analog Input, Pin Rules and Debugging with Serial" (curriculum v6), rules: PRODUCTION_GUIDELINES.md sections 9, 10, 11;
video/ANALOGIES.md (slide, ruler, stove marks, bathroom scale, thermometer, one-way door); retrieval minute on episode 6, PRIMM for
pot_read and pot_dimmer, one common mistake (no reaction: print the value first), one "in your own words", the challenge at the end.
Not a mini-project: no challenge-solution Short; the solution stays in the lesson folder.

Clips (creator, footage/gelen/ep06/CLIPS.md, prepared into footage/ep07):
C0 opening, pot_dimmer. C1 wiring, filmed as removal, played reversed. C2 multimeter: the sketch on the board in that take makes the LED
follow the knob, so it belongs to pot_dimmer (s29), NOT to pot_read; the digits sweep 0.00 -> 3.33 V. pot_zones (s36) was not on the shoot pack: animated LED plus knob.
pot_read and pot_smooth results are recreated Serial Monitor / Plotter scenes.
TR dub: lines start with native words; "sketç" after "İşte" is unreadable for the engine (comes out "Disketçin"): use "skeç" and "Şimdi".
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


# ---- cold open
s("s01", "cold", "Watch my hand. I turn a knob, and the LED follows it, brighter and dimmer, the moment I move.",
  "Elime bakın. Bir düğmeyi çeviriyorum ve LED onu takip ediyor; ben hareket ettiğim anda parlıyor ve kısılıyor.",
  "Elime bakın. Bir düğmeyi çeviriyorum ve led onu takip ediyor; ben hareket ettiğim anda parlıyor ve kısılıyor.", clip="C0")
s("s02", "cold", "By the end of this video, you'll read any knob with one line of code. And when it doesn't work, you'll know how to find the problem.",
  "Bu videonun sonunda herhangi bir düğmeyi tek satır kodla okuyacaksınız. Çalışmadığında da sorunu nasıl bulacağınızı bileceksiniz.")
# ---- retrieval minute (episode 6)
s("s03", "retrieval", "First, two questions from the last episode. Quick question: set color with two fifty-five, two fifty-five and zero. Which color does the RGB LED show?",
  "Önce geçen bölümden iki soru. Kısa bir soru: setColor'a 255, 255 ve sıfır veriyoruz. RGB LED hangi rengi gösterir?",
  "Önce geçen bölümden iki soru. Kısa bir soru: set kalıra iki yüz elli beş, iki yüz elli beş ve sıfır veriyoruz. Ar Ce Be led hangi rengi gösterir?",
  sub="First, two questions from the last episode. Quick question: setColor() with 255, 255 and 0. Which color does the RGB LED show?", pad=THINK)
s("s04", "retrieval", "Yellow. Red light plus green light makes yellow, because light adds up.",
  "Sarı. Kırmızı ışık artı yeşil ışık sarı yapar, çünkü ışık toplanır.")
s("s05", "retrieval", "Quick question: the RGB LED goes dark, all three colors at once. Which wire do you check first?",
  "Kısa bir soru: RGB LED sönüyor, üç renk birden. Önce hangi kabloya bakarsınız?",
  "Kısa bir soru: Ar Ce Be led sönüyor, üç renk birden. Önce hangi kabloya bakarsınız?", pad=THINK)
s("s06", "retrieval", "The shared wire, on the longest leg. All three colors return to ground through it.",
  "En uzun bacaktaki ortak kabloya. Üç renk de toprağa onun üzerinden döner.")
# ---- parts
s("s07", "parts", "You need the circuit from the last episode, one ten kilo-ohm potentiometer, which is a knob with three legs, and a few wires.",
  "Geçen bölümün devresi, bir 10 kiloohm potansiyometre, yani üç bacaklı bir düğme, ve birkaç kablo gerekiyor.",
  "Geçen bölümün devresi, bir on kiloohm potansiyometre, yani üç bacaklı bir düğme, ve birkaç kablo gerekiyor.",
  sub="You need the circuit from the last episode, one 10 kΩ potentiometer, which is a knob with three legs, and a few wires.")
# ---- the idea, without code
s("s08", "idea", "Until now, the only thing we've read is a button, and a button has two answers: pressed, or not pressed. A knob can answer how much.",
  "Şimdiye kadar yalnızca buton okuduk ve butonun iki cevabı var: basılı ya da değil. Düğme ise ne kadar sorusunu cevaplayabilir.")
s("s09", "idea", "Picture a playground slide. The top is three point three volts, the bottom is ground, and the knob decides how high up the slide you're sitting.",
  "Parktaki bir kaydırak düşünün. Tepesi 3,3 volt, dibi toprak; düğme de kaydırağın ne kadar yukarısında oturduğunuzu seçiyor.",
  "Parktaki bir kaydırak düşünün. Tepesi üç virgül üç volt, dibi toprak; düğme de kaydırağın ne kadar yukarısında oturduğunuzu seçiyor.",
  sub="Picture a playground slide. The top is 3.3 V, the bottom is ground, and the knob decides how high up the slide you're sitting.")
s("s10", "idea", "What actually happens: inside the knob is a strip of resistor, with a contact that slides along it. The outer legs go to three point three volts and ground, and the middle leg gives you the voltage at the contact.",
  "Gerçekte olan şu: düğmenin içinde bir direnç şeridi ve onun üzerinde kayan bir temas var. Dış bacaklar 3,3 volta ve toprağa gider; orta bacak da temasın olduğu yerdeki voltajı verir.",
  "Gerçekte olan şu: düğmenin içinde bir direnç şeridi ve onun üzerinde kayan bir temas var. Dış bacaklar üç virgül üç volta ve toprağa gider; orta bacak da temasın olduğu yerdeki voltajı verir.",
  sub="What actually happens: inside the knob is a strip of resistor, with a contact that slides along it. The outer legs go to 3.3 V and ground, and the middle leg gives you the voltage at the contact.")
s("s11", "idea", "That's called a voltage divider. The difference from a slide: nothing slides down by itself. The contact stays exactly where you leave it.",
  "Buna gerilim bölücü denir. Kaydıraktan farkı şu: hiçbir şey kendiliğinden aşağı kaymaz. Temas, bıraktığınız yerde kalır.")
s("s12", "idea", "Quick question: the knob is exactly in the middle. Roughly how many volts are on the middle leg?",
  "Kısa bir soru: düğme tam ortada. Orta bacakta yaklaşık kaç volt vardır?", pad=THINK)
s("s13", "idea", "About one point six five volts, half of three point three. Every position of the knob is its own voltage.",
  "Yaklaşık 1,65 volt, yani 3,3'ün yarısı. Düğmenin her konumu kendi voltajıdır.",
  "Yaklaşık bir virgül altmış beş volt, yani üç virgül üçün yarısı. Düğmenin her konumu kendi voltajıdır.",
  sub="About 1.65 V, half of 3.3. Every position of the knob is its own voltage.")
s("s14", "idea", "Here's the same circuit as a schematic, a drawing that shows only the connections. The zigzag is the resistor, and the arrow is the sliding contact.",
  "Şimdi aynı devreyi şema olarak görelim; şema yalnızca bağlantıları gösteren bir çizimdir. Zikzak direnç, ok da kayan temas.")
# ---- wiring
s("s15", "wire", "Unplug the USB cable. The knob goes on the right breadboard, below the LED. One outer leg goes to the plus rail, and the other to the minus rail.",
  "USB kablosunu çıkarın. Düğme sağdaki breadboard'a, LED'in altına gidiyor. Dış bacaklardan biri artı raya, diğeri eksi raya bağlanıyor.",
  "Yu Es Be kablosunu çıkarın. Düğme sağdaki breadborda, ledin altına gidiyor. Dış bacaklardan biri artı raya, diğeri eksi raya bağlanıyor.")
s("s16", "wire", "A long wire takes the middle leg across to D thirty-four. If your power rails are split in the middle, add a bridge wire to each one.",
  "Uzun bir kablo orta bacağı D34'e götürüyor. Güç raylarınız ortada kesikse her birine bir köprü kablosu ekleyin.",
  "Uzun bir kablo orta bacağı De otuz dörde götürüyor. Güç raylarınız ortada kesikse her birine bir köprü kablosu ekleyin.",
  sub="A long wire takes the middle leg across to D34. If your power rails are split in the middle, add a bridge wire to each one.", clip="C1", pad=3.0)
s("s17", "wire", "One rule here: the plus rail must be three point three volts, never five. An ESP32 input can only take three point three.",
  "Burada bir kural var: artı ray 3,3 volt olmalı, asla 5 değil. ESP32'nin girişi en fazla 3,3 volt alabilir.",
  "Burada bir kural var: artı ray üç virgül üç volt olmalı, asla beş değil. E Es Pe otuz ikinin girişi en fazla üç virgül üç volt alabilir.",
  sub="One rule here: the plus rail must be 3.3 V, never 5. An ESP32 input can only take 3.3 V.")
# ---- analogRead
s("s18", "read", "To read that voltage, we use a new function, analog read. Think of a ruler with four thousand ninety-six marks, laid along the slide.",
  "Bu voltajı okumak için yeni bir fonksiyon kullanıyoruz: analogRead. Kaydırağın boyunca uzanan, 4096 çizgili bir cetvel düşünün.",
  "Bu voltajı okumak için yeni bir fonksiyon kullanıyoruz: analog rid. Kaydırağın boyunca uzanan, dört bin doksan altı çizgili bir cetvel düşünün.",
  sub="To read that voltage, we use a new function, analogRead(). Think of a ruler with 4096 marks, laid along the slide.")
s("s19", "read", "What actually happens: analog read measures the voltage on a pin, and gives back a number. Zero means zero volts, and four thousand ninety-five means three point three volts.",
  "Gerçekte olan şu: analogRead bir pindeki voltajı ölçer ve bir sayı döndürür. Sıfır, sıfır volt demektir; 4095 de 3,3 volt demektir.",
  "Gerçekte olan şu: analog rid bir pindeki voltajı ölçer ve bir sayı döndürür. Sıfır, sıfır volt demektir; dört bin doksan beş de üç virgül üç volt demektir.",
  sub="What actually happens: analogRead() measures the voltage on a pin, and gives back a number. 0 means 0 V, and 4095 means 3.3 V.")
s("s20", "read", "The difference from a ruler: this one isn't perfect. Near the two ends it flattens a little, so you may never see exactly zero or exactly four thousand ninety-five.",
  "Cetvelden farkı şu: bu cetvel kusursuz değil. İki uca yakın biraz düzleşir; bu yüzden tam sıfırı ya da tam 4095'i hiç görmeyebilirsiniz.",
  "Cetvelden farkı şu: bu cetvel kusursuz değil. İki uca yakın biraz düzleşir; bu yüzden tam sıfırı ya da tam dört bin doksan beşi hiç görmeyebilirsiniz.",
  sub="The difference from a ruler: this one isn't perfect. Near the two ends it flattens a little, so you may never see exactly 0 or exactly 4095.")
# ---- code tour: pot_read
s("s21", "tourread", "Here's the whole sketch, pot read, and it's tiny. Pin thirty-four gets a name, and setup only starts the Serial Monitor. A pin we only read this way needs no pin mode.",
  "Şimdi sketch'in tamamına bakalım: pot_read, çok küçük. 34. pine bir ad veriyoruz; setup yalnızca Seri Monitör'ü başlatıyor. Bu şekilde okuduğumuz bir pin için pinMode gerekmez.",
  "Şimdi skeçin tamamına bakalım: pot rid, çok küçük. Otuz dördüncü pine bir ad veriyoruz; set ap yalnızca Seri Monitörü başlatıyor. Bu şekilde okuduğumuz bir pin için pin mod gerekmez.",
  sub="Here's the whole sketch, pot_read, and it's tiny. Pin 34 gets a name, and setup() only starts the Serial Monitor. A pin we only read this way needs no pinMode().")
s("s22", "tourread", "In the loop, analog read puts a number into value. We print it, and wait a tenth of a second. Pause the video and predict: with the knob in the middle, what number do you expect?",
  "loop'ta analogRead, value'ya bir sayı koyuyor. Onu yazdırıp saniyenin onda biri kadar bekliyoruz. Videoyu durdurun ve tahmin edin: düğme ortadayken hangi sayıyı beklersiniz?",
  "Lupta analog rid, velyuya bir sayı koyuyor. Onu yazdırıp saniyenin onda biri kadar bekliyoruz. Videoyu durdurun ve tahmin edin: düğme ortadayken hangi sayıyı beklersiniz?",
  sub="In the loop, analogRead() puts a number into value. We print it, and wait a tenth of a second. Pause the video and predict: with the knob in the middle, what number do you expect?", pad=3.0)
s("s23", "runread", "Around two thousand, half of the scale. As the knob turns, the number on the Serial Monitor climbs with it, from the bottom of the scale to the top.",
  "Yaklaşık iki bin, yani ölçeğin yarısı. Düğme döndükçe Seri Monitör'deki sayı da onunla birlikte, ölçeğin dibinden tepesine çıkıyor.",
  "Yaklaşık iki bin, yani ölçeğin yarısı. Düğme döndükçe Seri Monitördeki sayı da onunla birlikte, ölçeğin dibinden tepesine çıkıyor.", pad=2.0)
# ---- practice 1: the dimmer
s("s24", "dim", "Now the knob should do something. Analog write sets the brightness, but it only takes zero to two fifty-five, and the knob gives up to four thousand ninety-five. Quick question: how do we make that fit?",
  "Şimdi düğme bir işe yarasın. analogWrite parlaklığı ayarlıyor ama yalnızca sıfırdan 255'e kadar alıyor; düğme ise 4095'e kadar veriyor. Kısa bir soru: bunu nasıl sığdırırız?",
  "Şimdi düğme bir işe yarasın. Analog rayt parlaklığı ayarlıyor ama yalnızca sıfırdan iki yüz elli beşe kadar alıyor; düğme ise dört bin doksan beşe kadar veriyor. Kısa bir soru: bunu nasıl sığdırırız?",
  sub="Now the knob should do something. analogWrite() sets the brightness, but it only takes 0 to 255, and the knob gives up to 4095. Quick question: how do we make that fit?", pad=THINK)
s("s25", "dim", "We divide. Four thousand ninety-five divided by sixteen is about two fifty-five, so both ends of the knob land on both ends of the brightness.",
  "Bölüyoruz. 4095 bölü 16 yaklaşık 255 eder; böylece düğmenin iki ucu parlaklığın iki ucuna oturur.",
  "Bölüyoruz. Dört bin doksan beş bölü on altı yaklaşık iki yüz elli beş eder; böylece düğmenin iki ucu parlaklığın iki ucuna oturur.",
  sub="We divide. 4095 divided by 16 is about 255, so both ends of the knob land on both ends of the brightness.")
s("s26", "tourdim", "Here's pot dimmer. We read the knob into value, divide by sixteen into brightness, and analog write shows it on the LED.",
  "Bu da pot_dimmer. Düğmeyi value'ya okuyor, 16'ya bölüp brightness'a koyuyoruz; analogWrite da bunu LED'de gösteriyor.",
  "Bu da pot dimır. Düğmeyi velyuya okuyor, on altıya bölüp braytnısa koyuyoruz; analog rayt da bunu ledde gösteriyor.",
  sub="Here's pot_dimmer. We read the knob into value, divide by 16 into brightness, and analogWrite() shows it on the LED.")
s("s27", "tourdim", "Pause the video and predict: if we divided by thirty-two instead, what would change?",
  "Videoyu durdurun ve tahmin edin: 32'ye bölseydik ne değişirdi?",
  "Videoyu durdurun ve tahmin edin: otuz ikiye bölseydik ne değişirdi?",
  sub="Pause the video and predict: if we divided by 32 instead, what would change?", pad=3.0)
s("s28", "tourdim", "The biggest number would be about one twenty-seven, so the LED would stay at about half power, however far you turn the knob.",
  "En büyük sayı yaklaşık 127 olurdu; yani düğmeyi ne kadar çevirirseniz çevirin LED yarım güçte kalırdı.",
  "En büyük sayı yaklaşık yüz yirmi yedi olurdu; yani düğmeyi ne kadar çevirirseniz çevirin led yarım güçte kalırdı.",
  sub="The biggest number would be about 127, so the LED would stay at about half power, however far you turn the knob.")
s("s29", "rundim", "Now the real thing, with a meter on the middle leg. As I turn the knob, the volts sweep from zero to three point three, and the LED follows them.",
  "Şimdi gerçek devre, orta bacakta da bir multimetre var. Düğmeyi çevirdikçe voltaj sıfırdan 3,3'e çıkıyor ve LED onu takip ediyor.",
  "Şimdi gerçek devre, orta bacakta da bir multimetre var. Düğmeyi çevirdikçe voltaj sıfırdan üç virgül üçe çıkıyor ve led onu takip ediyor.",
  sub="Now the real thing, with a meter on the middle leg. As I turn the knob, the volts sweep from 0 to 3.3, and the LED follows them.", clip="C2", pad=3.0)
# ---- practice 2: zones
s("s30", "zones", "Sometimes you don't want every value, only a few choices, like the low, medium and high marks on a stove.",
  "Bazen her değeri istemezsiniz, yalnızca birkaç seçenek istersiniz; ocaktaki kısık, orta ve yüksek işaretleri gibi.")
s("s31", "zones", "What actually happens: the knob still gives one number, and our code sorts it. Four thousand ninety-five divided by three is about thirteen sixty-five, so we cut at thirteen sixty-five and twenty-seven thirty.",
  "Gerçekte olan şu: düğme yine tek bir sayı veriyor, kodumuz onu sınıflandırıyor. 4095 bölü 3 yaklaşık 1365 eder; bu yüzden 1365 ve 2730'dan kesiyoruz.",
  "Gerçekte olan şu: düğme yine tek bir sayı veriyor, kodumuz onu sınıflandırıyor. Dört bin doksan beş bölü üç yaklaşık bin üç yüz altmış beş eder; bu yüzden bin üç yüz altmış beş ve iki bin yedi yüz otuzdan kesiyoruz.",
  sub="What actually happens: the knob still gives one number, and our code sorts it. 4095 divided by 3 is about 1365, so we cut at 1365 and 2730.")
s("s32", "zones", "The difference from a stove: this knob has no clicks. The zones exist only in the code.",
  "Ocaktan farkı şu: bu düğmede tık sesi yok. Bölgeler yalnızca kodda var.")
s("s33", "tourzones", "Here's the sketch, pot zones. Below thirteen sixty-five, the LED gets twenty, which is dim. Else, if it's below twenty-seven thirty, it gets one twenty. Otherwise, it gets full brightness.",
  "Bu da pot_zones. 1365'in altında LED 20 alıyor, yani loş. Değilse ve 2730'un altındaysa 120 alıyor. Hiçbiri değilse tam parlaklık alıyor.",
  "Bu da pot zons. Bin üç yüz altmış beşin altında led yirmi alıyor, yani loş. Değilse ve iki bin yedi yüz otuzun altındaysa yüz yirmi alıyor. Hiçbiri değilse tam parlaklık alıyor.",
  sub="Here's the sketch, pot_zones. Below 1365, the LED gets 20, which is dim. Else, if it's below 2730, it gets 120. Otherwise, it gets full brightness.")
s("s34", "tourzones", "Pause the video and predict: the reading is exactly thirteen sixty-five. Which zone is it in?",
  "Videoyu durdurun ve tahmin edin: okunan değer tam 1365. Hangi bölgede?",
  "Videoyu durdurun ve tahmin edin: okunan değer tam bin üç yüz altmış beş. Hangi bölgede?",
  sub="Pause the video and predict: the reading is exactly 1365. Which zone is it in?", pad=3.0)
s("s35", "tourzones", "The middle one. Less than means strictly less, so thirteen sixty-five fails the first test, and passes the second.",
  "Ortadaki. Küçüktür işareti tam olarak küçük demek; bu yüzden 1365 ilk testten geçemez, ikinciden geçer.",
  "Ortadaki. Küçüktür işareti tam olarak küçük demek; bu yüzden bin üç yüz altmış beş ilk testten geçemez, ikinciden geçer.",
  sub="The middle one. < means strictly less, so 1365 fails the first test, and passes the second.")
s("s36", "runzones", "Turn it slowly: dim, medium and full, in three clear steps.",
  "Yavaşça çevirin: loş, orta ve tam; üç net adımda.", pad=3.0)
# ---- practice 3: a calmer reading
s("s37", "smooth", "One more thing. Leave the knob alone and watch the number. It still wobbles a little, like a bathroom scale that never quite settles.",
  "Bir şey daha. Düğmeye dokunmayın ve sayıyı izleyin. Yine de biraz titriyor; bir türlü sabitlenmeyen banyo tartısı gibi.")
s("s38", "smooth", "What actually happens: tiny electrical noise changes every reading. The fix is what you'd do on that scale: measure four times, and take the average.",
  "Gerçekte olan şu: küçük bir elektriksel gürültü her okumayı değiştiriyor. Çözüm, o tartıda yapacağınız şey: dört kez ölçün ve ortalamasını alın.")
s("s39", "smooth", "The difference from a scale: four readings take the board well under a millisecond, so you lose no time.",
  "Tartıdan farkı şu: dört okuma kartın bir milisaniyesini bile almaz; yani zaman kaybetmezsiniz.")
s("s40", "toursmooth", "In pot smooth, sum starts at zero. A for loop runs four times, and adds a fresh reading each round. Then sum divided by four is the average.",
  "pot_smooth'ta sum sıfırdan başlıyor. Bir for döngüsü dört kez çalışıyor ve her turda yeni bir okuma ekliyor. Sonra sum bölü dört ortalamayı veriyor.",
  "Pot smutta sam sıfırdan başlıyor. Bir for döngüsü dört kez çalışıyor ve her turda yeni bir okuma ekliyor. Sonra sam bölü dört ortalamayı veriyor.",
  sub="In pot_smooth, sum starts at 0. A for loop runs four times, and adds a fresh reading each round. Then sum divided by 4 is the average.")
s("s40b", "toursmooth", "Pause the video and predict: on a graph, which line jitters less, the single reading or the average?",
  "Videoyu durdurun ve tahmin edin: grafikte hangi çizgi daha az titrer, tek okuma mı, ortalama mı?", pad=3.0)
s("s41", "toursmooth", "The average. The Serial Plotter draws both as lines: the single reading jitters, and the average is calmer.",
  "Ortalama. Seri Plotter ikisini de çizgi olarak çiziyor: tek okuma titriyor, ortalama daha sakin.")
# ---- common mistake + debugging
s("s42", "mistake", "Now the problem you will meet. The LED doesn't react to the knob at all. Quick question: is it the LED, the knob, or the code? What would you do first?",
  "Şimdi karşınıza çıkacak sorun. LED düğmeye hiç tepki vermiyor. Kısa bir soru: LED mi, düğme mi, kod mu? İlk olarak ne yaparsınız?",
  "Şimdi karşınıza çıkacak sorun. Led düğmeye hiç tepki vermiyor. Kısa bir soru: led mi, düğme mi, kod mu? İlk olarak ne yaparsınız?", pad=THINK)
s("s43", "mistake", "Print the value, before you trust anything. A doctor takes your temperature before choosing a medicine, and the print line is your thermometer.",
  "Hiçbir şeye güvenmeden önce değeri yazdırın. Doktor ilaç seçmeden önce ateşinizi ölçer; yazdırma satırı da sizin termometreniz.")
s("s44", "mistake", "What actually happens: the number tells you which half is broken. Stuck at zero or stuck at the top means a loose wire or a rail gap at the knob. If it moves normally, the knob is fine, so look at the LED side.",
  "Gerçekte olan şu: sayı hangi tarafın bozuk olduğunu söyler. Sıfırda ya da tepede takılıysa düğmede gevşek bir kablo ya da ray boşluğu vardır. Normal değişiyorsa düğme sağlamdır; LED tarafına bakın.",
  "Gerçekte olan şu: sayı hangi tarafın bozuk olduğunu söyler. Sıfırda ya da tepede takılıysa düğmede gevşek bir kablo ya da ray boşluğu vardır. Normal değişiyorsa düğme sağlamdır; led tarafına bakın.")
s("s44b", "mistake", "The difference from a thermometer: printing takes time, so too many prints can slow a fast loop. Remove them when you're done.",
  "Termometreden farkı şu: yazdırmak zaman alır; çok fazla yazdırma hızlı bir döngüyü yavaşlatabilir. İşiniz bitince onları silin.")
# ---- pin rules
s("s45", "pins", "Why pin thirty-four? Because pins aren't all equal. Thirty-four to thirty-nine are like one-way doors: they can only listen, so they can't drive an LED.",
  "Neden 34. pin? Çünkü bütün pinler eşit değil. 34 ile 39 arası tek yönlü kapı gibidir: yalnızca dinleyebilirler, LED süremezler.",
  "Neden otuz dördüncü pin? Çünkü bütün pinler eşit değil. Otuz dört ile otuz dokuz arası tek yönlü kapı gibidir: yalnızca dinleyebilirler, led süremezler.",
  sub="Why pin 34? Because pins aren't all equal. 34 to 39 are like one-way doors: they can only listen, so they can't drive an LED.")
s("s46", "pins", "Second rule: some pins, like twenty-five to twenty-seven, can't read analog while Wi-Fi is on. Pin thirty-four keeps working, so our sensors live there.",
  "İkinci kural: 25 ile 27 gibi bazı pinler Wi-Fi açıkken analog okuyamaz. 34. pin çalışmaya devam eder; bu yüzden sensörlerimiz orada.",
  "İkinci kural: yirmi beş ile yirmi yedi gibi bazı pinler vay fay açıkken analog okuyamaz. Otuz dördüncü pin çalışmaya devam eder; bu yüzden sensörlerimiz orada.",
  sub="Second rule: some pins, like 25 to 27, can't read analog while Wi-Fi is on. Pin 34 keeps working, so our sensors live there.")
s("s47", "pins", "Third rule: pins zero, two, five, twelve and fifteen are checked at power-on, so we leave them free. You don't need to memorize this. The full pin map is in the lesson folder.",
  "Üçüncü kural: 0, 2, 5, 12 ve 15. pinler açılışta kontrol edilir; bu yüzden onları boş bırakıyoruz. Bunları ezberlemeniz gerekmez. Pin haritasının tamamı ders klasöründe.",
  "Üçüncü kural: sıfır, iki, beş, on iki ve on beşinci pinler açılışta kontrol edilir; bu yüzden onları boş bırakıyoruz. Bunları ezberlemeniz gerekmez. Pin haritasının tamamı ders klasöründe.",
  sub="Third rule: pins 0, 2, 5, 12 and 15 are checked at power-on, so we leave them free. You don't need to memorize this. The full pin map is in the lesson folder.")
# ---- explain in your own words
s("s48", "explain", "Now pause the video, and explain in your own words why we divide by sixteen. One sentence is enough.",
  "Şimdi videoyu durdurun ve neden 16'ya böldüğümüzü kendi cümlenizle açıklayın. Tek cümle yeter.",
  "Şimdi videoyu durdurun ve neden on altıya böldüğümüzü kendi cümlenizle açıklayın. Tek cümle yeter.",
  sub="Now pause the video, and explain in your own words why we divide by 16. One sentence is enough.", pad=4.0)
s("s49", "explain", "One way to say it: the knob's scale is sixteen times bigger than the brightness scale, so dividing makes them match.",
  "Şöyle söylenebilir: düğmenin ölçeği parlaklık ölçeğinden 16 kat büyük; bölünce ikisi eşleşiyor.",
  "Şöyle söylenebilir: düğmenin ölçeği parlaklık ölçeğinden on altı kat büyük; bölünce ikisi eşleşiyor.",
  sub="One way to say it: the knob's scale is 16 times bigger than the brightness scale, so dividing makes them match.")
# ---- your turn (not a mini-project: the solution stays in the lesson folder)
s("s50", "challenge", "Your turn: Knob Blink Speed. The LED blinks all the time, and the knob picks the speed in three zones: every hundred milliseconds, every four hundred, and every second.",
  "Sıra sizde: düğmeyle yanıp sönme hızı. LED sürekli yanıp sönüyor; düğme de hızı üç bölgede seçiyor: 100 milisaniyede bir, 400 milisaniyede bir ve saniyede bir.",
  "Sıra sizde: düğmeyle yanıp sönme hızı. Led sürekli yanıp sönüyor; düğme de hızı üç bölgede seçiyor: yüz milisaniyede bir, dört yüz milisaniyede bir ve saniyede bir.",
  sub="Your turn: Knob Blink Speed. The LED blinks all the time, and the knob picks the speed in three zones: every 100 milliseconds, every 400, and every second.")
s("s51", "challenge", "The twist: nothing may wait with delay. Today's zones choose the interval, and the millis trick from episode four does the blinking.",
  "İşin püf noktası: hiçbir şey delay ile beklemesin. Bugünkü bölgeler aralığı seçsin, yanıp sönmeyi de dördüncü bölümdeki millis yöntemi yapsın.",
  "İşin püf noktası: hiçbir şey dilay ile beklemesin. Bugünkü bölgeler aralığı seçsin, yanıp sönmeyi de dördüncü bölümdeki milis yöntemi yapsın.",
  sub="The twist: nothing may wait with delay(). Today's zones choose the interval, and the millis() trick from episode 4 does the blinking.")
# ---- outro
s("s52", "outro", "Today you learned three things. A knob turns position into voltage. Analog read turns voltage into a number. And printing that number shows you where a problem is.",
  "Bugün üç şey öğrendiniz. Düğme konumu voltaja çevirir. analogRead voltajı sayıya çevirir. O sayıyı yazdırmak da sorunun nerede olduğunu gösterir.",
  "Bugün üç şey öğrendiniz. Düğme konumu voltaja çevirir. Analog rid voltajı sayıya çevirir. O sayıyı yazdırmak da sorunun nerede olduğunu gösterir.",
  sub="Today you learned three things. A knob turns position into voltage. analogRead() turns voltage into a number. And printing that number shows you where a problem is.")
s("s53", "outro", "Next time: a function that does the dividing for us, and a bar of LEDs that fills up as you turn. Post your blink speed code in the comments; one solution is in the lesson folder. See you there!",
  "Gelecek sefer: bölme işini bizim yerimize yapan bir fonksiyon ve siz çevirdikçe dolan bir LED çubuğu. Yanıp sönme kodunuzu yorumlara yazın; bir çözüm ders klasöründe. Görüşmek üzere!",
  "Gelecek sefer: bölme işini bizim yerimize yapan bir fonksiyon ve siz çevirdikçe dolan bir led çubuğu. Yanıp sönme kodunuzu yorumlara yazın; bir çözüm ders klasöründe. Görüşmek üzere!")

# breathing room before a new term (lesson_lint NEWTERM: >= 0.8 s of silence before it)
NEW_TERM = ("s03", "s07", "s09", "s11", "s14", "s18", "s21", "s30", "s37", "s41", "s45", "s51")
for a, b in zip(S, S[1:]):
    if b["id"] in NEW_TERM:
        a["pad"] = a.get("pad", 0) + 0.4

dub = {d["id"]: d.pop("dub") for d in S}
script = {
    "episode": 7, "title": "Analog Input, Pin Rules and Debugging with Serial", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": "s02",
    "music": "results",
    "clips": {
        "C0": "OPENING: pot_dimmer, hand turns the knob, red LED follows (footage/gelen/ep06/20261029_171053).",
        "C1": "WIRING: filmed as removal, played reversed and speed-ramped (20261029_171259).",
        "C2": "MULTIMETER: LED follows the knob, digits sweep 0.00 -> 3.33 V; rotate so the digits read (20261029_172304).",
    },
    "segments": S,
}
here = Path(__file__).parent
(here / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "dub").mkdir(exist_ok=True)
(here / "dub" / "tr.json").write_text(json.dumps({
    "voice": "tr-TR-EmelNeural", "rate": "+0%",
    "note": "Spoken text only. English terms are written the way a Turkish speaker says them (analog rid, pot dimır, lup...).",
    "segments": dub}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
