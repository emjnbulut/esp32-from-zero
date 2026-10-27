"""Source of video/recap1/script.json (and dub/tr.json). Usage: python video/recap1/make_script.py

"Recap: episodes 1-4" (user 2026-10-27: the code was confusing, so one numbered-less special episode before episode 5).
ONE topic: how to read a sketch. Only syntax taught in episodes 1-4. Every sketch is run as a live trace: the
highlighted line moves, a "memory" panel shows every variable changing. Quick questions, two like/subscribe icons,
the end invites the comments (PRODUCTION_GUIDELINES.md sections 2, 4, 5, 8).
Each s(...) gives: id, scene, English narration (numbers spelled out), Turkish subtitle text, Turkish spoken text.
"""
import json
from pathlib import Path

S = []
THINK = 2.6  # silence after a "quick question"


def s(id, scene, text, tr, dub, sub=None, **kw):
    d = {"id": id, "scene": scene, "text": text}
    if sub:
        d["sub"] = sub
    d["tr"] = tr
    d["dub"] = dub
    d.update(kw)
    S.append(d)


# ---- cold open: the four results, then the promise
s("s01", "cold", "Five sketches. You've already run all of them. Watch them work, one after another.",
  "Beş sketch. Hepsini zaten çalıştırdınız. Birbiri ardına çalışmalarını izleyin.",
  "Beş sketç. Hepsini zaten çalıştırdınız. Birbiri ardına çalışmalarını izleyin.")
s("s02", "cold", "By the end of this video, you'll read any of them like a sentence. We'll go slowly, with every value on screen.",
  "Bu videonun sonunda hepsini bir cümle gibi okuyabileceksiniz. Yavaş gideceğiz; her değer ekranda olacak.",
  "Bu videonun sonunda hepsini bir cümle gibi okuyabileceksiniz. Yavaş gideceğiz; her değer ekranda olacak.")
# ---- the skeleton (hello_esp32)
s("s03", "skel", "Every sketch has the same three parts. Names at the top. Then setup. Then loop.",
  "Her sketch'in üç parçası aynıdır. Üstte isimler. Sonra setup. Sonra loop.",
  "Her sketçin üç parçası aynıdır. Üstte isimler. Sonra set ap. Sonra lup.")
s("s04", "skel", "A name is a variable: a small box with a label. This box is called seconds, and right now it holds zero.",
  "İsim, bir değişkendir: üzerinde etiket olan küçük bir kutu. Bu kutunun adı seconds ve şu an içinde sıfır var.",
  "İsim, bir değişkendir: üzerinde etiket olan küçük bir kutu. Bu kutunun adı sekınds ve şu an içinde sıfır var.")
s("s05", "skel", "Setup runs once, when the board starts. Here it opens the serial channel, and says hello.",
  "Setup, kart başladığında bir kez çalışır. Burada seri kanalı açar ve merhaba der.",
  "Set ap, kart başladığında bir kez çalışır. Burada seri kanalı açar ve merhaba der.")
s("s06", "skel", "Loop runs forever. When it reaches the bottom, it jumps straight back to the top.",
  "Loop sonsuza kadar çalışır. En alta varınca doğrudan başa döner.",
  "Lup sonsuza kadar çalışır. En alta varınca doğrudan başa döner.")
s("s07", "skel", "Watch the box. Seconds is zero. Add one: now it's one. Print it. Wait a second. Back to the top, add one again: two.",
  "Kutuya bakın. Seconds sıfır. Bir ekle: artık bir. Yazdır. Bir saniye bekle. Başa dön, bir daha ekle: iki.",
  "Kutuya bakın. Sekınds sıfır. Bir ekle: artık bir. Yazdır. Bir saniye bekle. Başa dön, bir daha ekle: iki.")
s("s08", "skel", "That's the first big idea. A variable is the sketch's memory. It keeps its value, round after round.",
  "İlk büyük fikir bu. Değişken, sketch'in hafızasıdır. Değerini tur tur korur.",
  "İlk büyük fikir bu. Değişken, sketçin hafızasıdır. Değerini tur tur korur.")
s("s09", "skel", "Quick question: after the loop has run five times, what does seconds hold?",
  "Kısa bir soru: loop beş kez çalıştıktan sonra seconds içinde ne var?",
  "Kısa bir soru: lup beş kez çalıştıktan sonra sekınds içinde ne var?", pad=THINK)
s("s10", "skel", "Five. Each round adds one, and the box remembers.",
  "Beş. Her tur bir ekler ve kutu hatırlar.",
  "Beş. Her tur bir ekler ve kutu hatırlar.")
# ---- outputs (blink_led)
s("s11", "blink", "Blink is the same three parts. The name at the top is a constant: LED pin, twenty-three. That's the pin our LED is wired to.",
  "Blink de aynı üç parçadır. Üstteki isim bir sabit: LED_PIN, 23. LED'imizin bağlı olduğu pin bu.",
  "Blink de aynı üç parçadır. Üstteki isim bir sabit: led pin, yirmi üç. Led'imizin bağlı olduğu pin bu.",
  sub="Blink is the same three parts. The name at the top is a constant: LED_PIN, 23. That's the pin our LED is wired to.")
s("s12", "blink", "In setup, pin mode says: this pin is an output. Our code will drive it.",
  "Setup içinde pinMode şunu söyler: bu pin bir çıkıştır. Kodumuz onu sürecek.",
  "Set apta pin mod şunu söyler: bu pin bir çıkıştır. Kodumuz onu sürecek.")
s("s13", "blink", "In loop, digital write HIGH puts three point three volts on the pin, and the LED lights. Digital write LOW puts zero volts, and it goes dark.",
  "Loop içinde digitalWrite HIGH pine 3,3 volt verir ve LED yanar. digitalWrite LOW sıfır volt verir ve LED söner.",
  "Lup içinde dijital rayt hay pine üç virgül üç volt verir ve led yanar. Dijital rayt lov sıfır volt verir ve led söner.",
  sub="In loop, digitalWrite HIGH puts 3.3 volts on the pin, and the LED lights. digitalWrite LOW puts 0 volts, and it goes dark.")
s("s14", "blink", "And delay means: wait. For that time, the sketch does nothing at all. Half a second on, half a second off, forever.",
  "delay ise şu demek: bekle. O süre boyunca sketch hiçbir şey yapmaz. Yarım saniye açık, yarım saniye kapalı, sonsuza kadar.",
  "Dilay ise şu demek: bekle. O süre boyunca sketç hiçbir şey yapmaz. Yarım saniye açık, yarım saniye kapalı, sonsuza kadar.")
# ---- decisions (button_led)
s("s15", "btn", "Now a button. A new name: button pin, twenty-two. And in setup: input pull up. Input means we read the pin. Pull up means: when nobody touches it, it reads HIGH.",
  "Şimdi bir buton. Yeni bir isim: BUTTON_PIN, 22. Setup içinde de INPUT_PULLUP. Input, pini okuyacağımız anlamına gelir. Pull-up ise: kimse dokunmazsa HIGH okur demektir.",
  "Şimdi bir buton. Yeni bir isim: batın pin, yirmi iki. Set apta da input pul ap. Input, pini okuyacağımız anlamına gelir. Pul ap ise: kimse dokunmazsa hay okur demektir.",
  sub="Now a button. A new name: BUTTON_PIN, 22. And in setup: INPUT_PULLUP. Input means we read the pin. Pull-up means: when nobody touches it, it reads HIGH.")
s("s16", "btn", "So the button works backwards. Not pressed: HIGH. Pressed: LOW, because the button connects the pin to ground.",
  "Yani buton tersine çalışır. Basılmamış: HIGH. Basılı: LOW, çünkü buton pini toprağa bağlar.",
  "Yani buton tersine çalışır. Basılmamış: hay. Basılı: lov, çünkü buton pini toprağa bağlar.")
s("s17", "btn", "In loop, digital read is a question: what is the pin right now? The answer, HIGH or LOW, goes into a box called state.",
  "Loop içinde digitalRead bir sorudur: pin şu an ne durumda? Cevap, HIGH ya da LOW, state adlı kutuya girer.",
  "Lup içinde dijital rid bir sorudur: pin şu an ne durumda? Cevap, hay ya da lov, steyt adlı kutuya girer.")
s("s18", "btn", "Then an if. If state is LOW, the button is pressed, so the LED gets HIGH. Otherwise, it gets LOW.",
  "Sonra bir if. State LOW ise buton basılıdır, LED'e HIGH veririz. Değilse LOW veririz.",
  "Sonra bir if. Steyt lov ise buton basılıdır, led'e hay veririz. Değilse lov veririz.")
s("s19", "btn", "Notice what this sketch remembers. Nothing. Every round it asks again, and decides from scratch.",
  "Bu sketch'in neyi hatırladığına dikkat edin. Hiçbir şeyi. Her turda yeniden sorar ve sıfırdan karar verir.",
  "Bu sketçin neyi hatırladığına dikkat edin. Hiçbir şeyi. Her turda yeniden sorar ve sıfırdan karar verir.")
s("s20", "btn", "Quick question: this sketch has no memory. Can it tell that you pressed the button just now?",
  "Kısa bir soru: bu sketch'in hafızası yok. Butona şimdi bastığınızı anlayabilir mi?",
  "Kısa bir soru: bu sketçin hafızası yok. Butona şimdi bastığınızı anlayabilir mi?", pad=THINK)
s("s21", "btn", "No. It only knows pressed, or not pressed. To know just pressed, a sketch must remember the last reading.",
  "Hayır. Yalnızca basılı ya da basılı değil bilir. Yeni basıldığını anlamak için sketch'in son okumayı hatırlaması gerekir.",
  "Hayır. Yalnızca basılı ya da basılı değil bilir. Yeni basıldığını anlamak için sketçin son okumayı hatırlaması gerekir.")
# ---- memory 1 (button_toggle)
s("s22", "tog", "So we add a second box: last state. It keeps the reading from the round before.",
  "O yüzden ikinci bir kutu ekliyoruz: lastState. Bir önceki turdaki okumayı tutar.",
  "O yüzden ikinci bir kutu ekliyoruz: last steyt. Bir önceki turdaki okumayı tutar.")
s("s23", "tog", "Each round, we compare. If state is different from last state, something changed. And if it's now LOW, that's a new press.",
  "Her turda karşılaştırırız. State, lastState'ten farklıysa bir şey değişmiştir. Şimdi LOW ise bu yeni bir basıştır.",
  "Her turda karşılaştırırız. Steyt, last steyttan farklıysa bir şey değişmiştir. Şimdi lov ise bu yeni bir basıştır.")
s("s24", "tog", "On a new press, we flip a true-or-false box called LED on. Not LED on means the opposite. And we count the press.",
  "Yeni bir basışta, ledOn adlı doğru-yanlış kutusunu çeviririz. !ledOn tersi demektir. Basışı da sayarız.",
  "Yeni bir basışta, led on adlı doğru yanlış kutusunu çeviririz. Not led on tersi demektir. Basışı da sayarız.",
  sub="On a new press, we flip a true-or-false box called ledOn. !ledOn means the opposite. And we count the press.")
s("s25", "tog", "At the very end of the round, we copy state into last state. So next round, the box remembers this round.",
  "Turun en sonunda state'i lastState'e kopyalarız. Böylece sonraki tur, bu turu hatırlar.",
  "Turun en sonunda steyti last steyte kopyalarız. Böylece sonraki tur, bu turu hatırlar.")
s("s26", "tog", "Let's run it. Not pressed: state HIGH, last state HIGH. Same, nothing happens. Now press: state LOW, last state HIGH. Different, and LOW: a new press. The LED turns on.",
  "Çalıştıralım. Basılmamış: state HIGH, lastState HIGH. Aynı, hiçbir şey olmaz. Şimdi basın: state LOW, lastState HIGH. Farklı ve LOW: yeni bir basış. LED yanar.",
  "Çalıştıralım. Basılmamış: steyt hay, last steyt hay. Aynı, hiçbir şey olmaz. Şimdi basın: steyt lov, last steyt hay. Farklı ve lov: yeni bir basış. Led yanar.",
  sub="Let's run it. Not pressed: state HIGH, lastState HIGH. Same, nothing happens. Now press: state LOW, lastState HIGH. Different, and LOW: a new press. The LED turns on.")
s("s27", "tog", "Keep holding: LOW and LOW. Same again, nothing happens. Let go: HIGH, different, but not LOW. So it's not a press.",
  "Basılı tutmaya devam: LOW ve LOW. Yine aynı, hiçbir şey olmaz. Bırakın: HIGH, farklı ama LOW değil. Yani bu bir basış değil.",
  "Basılı tutmaya devam: lov ve lov. Yine aynı, hiçbir şey olmaz. Bırakın: hay, farklı ama lov değil. Yani bu bir basış değil.", pad=0.7)
s("s28", "tog", "The short delay of fifty milliseconds is the debounce: it waits until the metal contacts stop bouncing.",
  "Elli milisaniyelik kısa bekleme, sıçrama önleyicidir: metal temaslar sıçramayı bırakana kadar bekler.",
  "Elli milisaniyelik kısa bekleme, sıçrama önleyicidir: metal temaslar sıçramayı bırakana kadar bekler.")
# ---- memory 2 (blink_button)
s("s29", "ms", "One problem is left. Delay freezes everything. To blink and read a button at the same time, we need a different tool: the clock.",
  "Bir sorun kaldı. delay her şeyi dondurur. Aynı anda hem yanıp sönmek hem butonu okumak için başka bir araç gerekir: saat.",
  "Bir sorun kaldı. Dilay her şeyi dondurur. Aynı anda hem yanıp sönmek hem butonu okumak için başka bir araç gerekir: saat.", pad=0.7)
s("s30", "ms", "Millis is the number of milliseconds since the board started. It keeps counting by itself. We never wait: we just look at it.",
  "millis, kart başladığından beri geçen milisaniye sayısıdır. Kendi kendine saymaya devam eder. Hiç beklemeyiz: sadece ona bakarız.",
  "Milis, kart başladığından beri geçen milisaniye sayısıdır. Kendi kendine saymaya devam eder. Hiç beklemeyiz: sadece ona bakarız.")
s("s31", "ms", "Now is the time right now. Last blink is the time the LED last changed. Now minus last blink is how long ago that was.",
  "now, şu anki zamandır. lastBlink, LED'in en son değiştiği zamandır. now eksi lastBlink, bunun ne kadar önce olduğudur.",
  "Nau, şu anki zamandır. Last blink, led'in en son değiştiği zamandır. Nau eksi last blink, bunun ne kadar önce olduğudur.")
s("s32", "ms", "At one thousand, the LED flips, and last blink becomes one thousand. At twelve hundred: two hundred ago, not yet. At fifteen hundred: five hundred. Flip, and last blink is now fifteen hundred.",
  "1000'de LED değişir ve lastBlink 1000 olur. 1200'de: 200 önce, daha değil. 1500'de: 500. LED değişir ve lastBlink artık 1500 olur.",
  "Bin de led değişir ve last blink bin olur. Bin iki yüzde: iki yüz önce, daha değil. Bin beş yüzde: beş yüz. Led değişir ve last blink artık bin beş yüz olur.",
  sub="At 1000, the LED flips, and lastBlink becomes 1000. At 1200: 200 ago, not yet. At 1500: 500. Flip, and lastBlink is now 1500.")
s("s33", "ms", "The button uses the same trick: last change remembers when the button last changed, and we ignore anything faster than fifty milliseconds.",
  "Buton da aynı numarayı kullanır: lastChange butonun en son ne zaman değiştiğini hatırlar ve elli milisaniyeden hızlı olan her şeyi yok sayarız.",
  "Buton da aynı numarayı kullanır: last çeynç butonun en son ne zaman değiştiğini hatırlar ve elli milisaniyeden hızlı olan her şeyi yok sayarız.")
s("s34", "ms", "And blinking is a true-or-false box. A press flips it. When it's false, the LED part is skipped, but the button still works, because the loop never waits.",
  "blinking de bir doğru-yanlış kutusudur. Bir basış onu çevirir. Yanlış olduğunda LED kısmı atlanır ama buton çalışmaya devam eder, çünkü loop hiç beklemez.",
  "Blinking de bir doğru yanlış kutusudur. Bir basış onu çevirir. Yanlış olduğunda led kısmı atlanır ama buton çalışmaya devam eder, çünkü lup hiç beklemez.")
# ---- the four questions
s("s35", "four", "That's all five sketches. And every sketch answers the same four questions.",
  "Beş sketch bu kadar. Ve her sketch aynı dört soruya cevap verir.",
  "Beş sketç bu kadar. Ve her sketç aynı dört soruya cevap verir.")
s("s36", "four", "One: what are the names? Two: what happens once, in setup? Three: what repeats, in loop? And four: what does it remember?",
  "Bir: isimler neler? İki: setup içinde bir kez ne olur? Üç: loop içinde ne tekrar eder? Dört: neyi hatırlar?",
  "Bir: isimler neler? İki: set apta bir kez ne olur? Üç: lupta ne tekrar eder? Dört: neyi hatırlar?")
s("s37", "four", "The fourth matters most. A box that keeps its value between rounds is how a sketch knows what happened before.",
  "En önemlisi dördüncüsü. Turlar arasında değerini koruyan kutu, bir sketch'in daha önce ne olduğunu bilme yoludur.",
  "En önemlisi dördüncüsü. Turlar arasında değerini koruyan kutu, bir sketçin daha önce ne olduğunu bilme yoludur.")
# ---- practice
s("s38", "prac", "Your turn: three quick ones. Pause the video if you want to think.",
  "Sıra sizde: üç kısa soru. Düşünmek isterseniz videoyu durdurun.",
  "Sıra sizde: üç kısa soru. Düşünmek isterseniz videoyu durdurun.")
s("s39", "prac", "One. Count starts at zero, and each round adds two. What are the first three prints?",
  "Bir. count sıfırdan başlıyor ve her tur iki ekliyor. İlk üç çıktı nedir?",
  "Bir. Kaunt sıfırdan başlıyor ve her tur iki ekliyor. İlk üç çıktı nedir?", pad=THINK + 1.0)
s("s40", "prac", "Two, four, six. The box remembers, and adds two every round.",
  "İki, dört, altı. Kutu hatırlar ve her tur iki ekler.",
  "İki, dört, altı. Kutu hatırlar ve her tur iki ekler.")
s("s41", "prac", "Two. You hold the button for five rounds. The sketch counts a press only when state is LOW and last state is HIGH. How many presses?",
  "İki. Butona beş tur boyunca basılı tutuyorsunuz. Sketch yalnızca state LOW ve lastState HIGH iken bir basış sayıyor. Kaç basış olur?",
  "İki. Butona beş tur boyunca basılı tutuyorsunuz. Sketç yalnızca steyt lov ve last steyt hay iken bir basış sayıyor. Kaç basış olur?", pad=THINK + 1.0)
s("s42", "prac", "One. Only the first round has a change. After that it's LOW and LOW, the same.",
  "Bir. Yalnızca ilk turda değişiklik var. Sonrasında LOW ve LOW, aynı.",
  "Bir. Yalnızca ilk turda değişiklik var. Sonrasında lov ve lov, aynı.")
s("s43", "prac", "Three. Last blink is zero, and now is seven hundred. The rule is: now minus last blink, at least five hundred. Does the LED flip?",
  "Üç. lastBlink sıfır ve now yedi yüz. Kural: now eksi lastBlink en az beş yüz. LED değişir mi?",
  "Üç. Last blink sıfır ve nau yedi yüz. Kural: nau eksi last blink en az beş yüz. Led değişir mi?", pad=THINK + 1.0)
s("s44", "prac", "Yes: seven hundred minus zero is seven hundred, and that's at least five hundred. Then last blink becomes seven hundred.",
  "Evet: yedi yüz eksi sıfır yedi yüz eder ve bu en az beş yüzdür. Sonra lastBlink yedi yüz olur.",
  "Evet: yedi yüz eksi sıfır yedi yüz eder ve bu en az beş yüzdür. Sonra last blink yedi yüz olur.")
# ---- outro
s("s45", "outro", "Today, we read five sketches with the same four questions, and watched their memory change. If one of them still feels unclear, tell me which one in the comments.",
  "Bugün beş sketch'i aynı dört soruyla okuduk ve hafızalarının değişmesini izledik. Hâlâ net olmayan biri varsa yorumlarda hangisi olduğunu yazın.",
  "Bugün beş sketçi aynı dört soruyla okuduk ve hafızalarının değişmesini izledik. Hâlâ net olmayan biri varsa yorumlarda hangisi olduğunu yazın.")
s("s46", "outro", "Next time: PWM. We'll fade an LED smoothly, and mix any color. Let's meet in the comments: which sketch was the hardest to read? See you there!",
  "Gelecek sefer: PWM. Bir LED'i yumuşakça yakıp söndüreceğiz ve istediğimiz rengi karıştıracağız. Yorumlarda buluşalım: hangi sketch okumak için en zordu? Görüşmek üzere!",
  "Gelecek sefer: Pe Ve Me. Bir led'i yumuşakça yakıp söndüreceğiz ve istediğimiz rengi karıştıracağız. Yorumlarda buluşalım: hangi sketç okumak için en zordu? Görüşmek üzere!")

dub = {d["id"]: d.pop("dub") for d in S}
script = {
    "episode": "recap1", "title": "Recap: Episodes 1-4, how to read a sketch", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": "s02",
    "clips": {
        "C1": "REUSED from episode 3 (footage/ep03/C2.mp4): the LED blinking once per second.",
        "C2": "REUSED from episode 4 (footage/ep04/C3.mp4): button_led, the LED lights while the button is held.",
        "C3": "REUSED from episode 4 (footage/ep04/C4.mp4): button_toggle, press on, press off.",
        "C4": "REUSED from episode 4 (footage/ep04/C5.mp4): blink_button, the LED blinks; a press stops it.",
    },
    "segments": S,
}
here = Path(__file__).parent
(here / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "dub").mkdir(exist_ok=True)
(here / "dub" / "tr.json").write_text(json.dumps({
    "voice": "tr-TR-EmelNeural", "rate": "+0%",
    "note": "Spoken text only. English terms are written the way a Turkish speaker says them (dijital rid, hay, lov, milis...).",
    "segments": dub}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
