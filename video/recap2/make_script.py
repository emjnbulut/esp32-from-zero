"""Source of video/recap2/script.json (and dub/tr.json). Usage: python video/recap2/make_script.py

"Recap 2: episodes 5-10" (curriculum v6 row R2; release Tue 24 Nov 2026 17:00). No new syntax: trace PWM, the color LED,
analogRead/map and the state machine (millis steps + Preferences), with a scored quiz inside the video.
Rules: PRODUCTION_GUIDELINES.md sections 9, 10, 11 (recap at most 12 minutes; numbers on screen, at most 1-2 spoken per
sentence). Every idea comes back with ITS analogy from video/ANALOGIES.md (never a new one): ceiling fan blur (PWM), tap
(duty cycle), dimmer knob (analogWrite), phone screen dots (RGB), coffee machine button (setColor), playground slide
(potentiometer), ruler with 4096 marks (analogRead), city map (map), phone battery bars (level bar), washing machine
(state), parking ticket (time since a moment), notebook in the drawer (Preferences). Each part: picture -> what actually
happens -> a live trace with a memory panel -> quiz questions (pause, answer, score). Seven questions; the score at the end
points to the episode to rewatch. Footage: existing creator clips from footage/ep05-ep08 (+ ep09/ep10 once they exist).
TR dub: lines start with native words; "skeç"; map -> "mep"; loop -> "lup"; millis -> "milis"; state -> "steyt";
analogWrite -> "anılog rayt"; analogRead -> "anılog rid"; the RGB LED is "üç renkli LED"; knob = "düğme".
"""
import json
from pathlib import Path

S = []
THINK = 3.2  # quiz pause: a bit longer than a quick question, the viewer is keeping score


def s(id, scene, text, tr, dub=None, sub=None, **kw):
    d = {"id": id, "scene": scene, "text": text}
    if sub:
        d["sub"] = sub
    d["tr"] = tr
    d["dub"] = dub or tr
    d.update(kw)
    S.append(d)


# ---- cold open: the results of episodes 5-10, then the promise
s("s01", "cold", "A breathing LED. Any color you like. A knob that dims the light, a level bar, a crossing, and a reflex game.",
  "Nefes alan bir LED. İstediğiniz her renk. Işığı kısan bir düğme, bir seviye çubuğu, bir yaya geçidi ve bir refleks oyunu.",
  "Nefes alan bir led. İstediğiniz her renk. Işığı kısan bir düğme, bir seviye çubuğu, bir yaya geçidi ve bir refleks oyunu.", clip="M")
s("s02", "cold", "Today, nothing new. We'll read these sketches again, watch their numbers change, and you'll test yourself with seven questions.",
  "Bugün yeni bir şey yok. Bu skeçleri yeniden okuyacağız, sayılarının değişmesini izleyeceğiz ve yedi soruyla kendinizi sınayacaksınız.")
# ---- how it works
s("s03", "retrieval", "Grab a piece of paper. After every question, pause the video, answer, and then give yourself a point if you were right.",
  "Bir kağıt alın. Her sorudan sonra videoyu durdurun, cevap verin; doğruysa kendinize bir puan yazın.")
s("s04", "retrieval", "Three parts: making light, reading a knob, and remembering steps. New here? Episode one is on the screen.",
  "Üç kısım var: ışık yapmak, düğme okumak ve adımları hatırlamak. Yeni misiniz? Birinci bölüm ekranda.")
# ==== PART 1: making light (episodes 5-6)
s("s05", "pwm", "Part one. Remember the ceiling fan? It spins so fast that your eye sees a blur, not the blades.",
  "Birinci kısım. Tavan vantilatörünü hatırlıyor musunuz? O kadar hızlı döner ki gözünüz kanatları değil, bir bulanıklık görür.")
s("s06", "pwm", "What actually happens: the pin switches fully on and off about a thousand times a second. The longer it stays on in each cycle, the brighter the LED looks.",
  "Gerçekte olan şu: pin saniyede yaklaşık bin kez tamamen açılıp kapanıyor. Her turda ne kadar uzun açık kalırsa LED o kadar parlak görünür.",
  "Gerçekte olan şu: pin saniyede yaklaşık bin kez tamamen açılıp kapanıyor. Her turda ne kadar uzun açık kalırsa led o kadar parlak görünür.")
s("s07", "pwm", "The difference from a fan: the fan really moves, but the LED is never half on. It's only ever on or off.",
  "Vantilatörden farkı şu: vantilatör gerçekten dönüyor ama LED asla yarı yanık değil. Ya açık ya kapalı.",
  "Vantilatörden farkı şu: vantilatör gerçekten dönüyor ama led asla yarı yanık değil. Ya açık ya kapalı.")
s("s08", "trace", "Let's trace the breathing LED. Every four milliseconds, brightness gets one step. At the top, the step turns negative, like a swing turning around.",
  "Nefes alan LED'in izini sürelim. Her dört milisaniyede parlaklık bir adım değişiyor. En üstte adım eksiye dönüyor; tıpkı geri dönen bir salıncak gibi.",
  "Nefes alan ledin izini sürelim. Her dört milisaniyede parlaklık bir adım değişiyor. En üstte adım eksiye dönüyor; tıpkı geri dönen bir salıncak gibi.")
s("s09", "trace", "Pause and predict: brightness has just reached the top. What is the step now? Watch the memory panel: it flips from plus one to minus one.",
  "Durdurun ve tahmin edin: parlaklık en üste yeni ulaştı. Adım şimdi kaç? Hafıza paneline bakın: artı birden eksi bire dönüyor.", pad=0.6)
s("s10", "q1", "Question one, pause the video to answer: with analog write sixty-four, how much of each cycle is the pin on?",
  "Birinci soru, cevap için videoyu durdurun: anılog rayt altmış dört ile pin her turun ne kadarında açık?",
  sub="Question one, pause the video to answer: with analogWrite(pin, 64), how much of each cycle is the pin on?", pad=THINK)
s("s11", "q1", "About a quarter. Two fifty-five is always on, so sixty-four is roughly one quarter of the time.",
  "Yaklaşık dörtte biri. İki yüz elli beş hep açık demek; altmış dört de zamanın kabaca dörtte biri.",
  sub="About a quarter. 255 is always on, so 64 is roughly one quarter of the time.")
s("s12", "rgb", "Then the color LED. Like the dots on your phone screen, it's three small lights in one package: red, green and blue.",
  "Sonra üç renkli LED. Telefon ekranınızdaki noktalar gibi, tek pakette üç küçük ışık: kırmızı, yeşil ve mavi.",
  "Sonra üç renkli led. Telefon ekranınızdaki noktalar gibi, tek pakette üç küçük ışık: kırmızı, yeşil ve mavi.")
s("s13", "rgb", "The difference from paint: light adds up. Red and green together make yellow, not brown. And set color is the coffee machine button: one call, three values.",
  "Boyadan farkı şu: ışık toplanır. Kırmızıyla yeşil birlikte kahverengi değil, sarı yapar. setColor da kahve makinesi düğmesi: tek çağrı, üç değer.",
  "Boyadan farkı şu: ışık toplanır. Kırmızıyla yeşil birlikte kahverengi değil, sarı yapar. Set kalır da kahve makinesi düğmesi: tek çağrı, üç değer.",
  sub="The difference from paint: light adds up. Red and green together make yellow, not brown. And setColor() is the coffee machine button: one call, three values.")
s("s14", "q2", "Here's question two, so pause the video: which color do you get from set color with two fifty-five, zero, two fifty-five?",
  "İkinci soru geliyor, videoyu durdurun: setColor iki yüz elli beş, sıfır, iki yüz elli beş ile hangi rengi elde edersiniz?",
  "İkinci soru geliyor, videoyu durdurun: set kalır iki yüz elli beş, sıfır, iki yüz elli beş ile hangi rengi elde edersiniz?",
  sub="Here's question two, so pause the video: which color do you get from setColor(255, 0, 255)?", pad=THINK)
s("s15", "q2", "Magenta, a pinkish purple. Full red plus full blue, and no green.",
  "Eflatun, pembemsi bir mor. Tam kırmızı artı tam mavi, hiç yeşil yok.")
# ==== PART 2: reading a knob (episodes 7-8)
s("s16", "pot", "Part two. The knob is a playground slide: a strip of resistance with a contact that slides along it. The middle leg gives the voltage where the contact sits.",
  "İkinci kısım. Düğme bir kaydırak: üzerinde bir kontağın kaydığı direnç şeridi. Orta bacak, kontağın durduğu yerdeki voltajı verir.")
s("s17", "pot", "Analog read measures that voltage like a ruler with four thousand ninety-six marks: zero at zero volts, and the top mark at three point three volts.",
  "anılog rid bu voltajı dört bin doksan altı çizgili bir cetvel gibi ölçer: sıfır voltta sıfır, üç virgül üç voltta en üst çizgi.",
  "Anılog rid bu voltajı dört bin doksan altı çizgili bir cetvel gibi ölçer: sıfır voltta sıfır, üç virgül üç voltta en üst çizgi.",
  sub="analogRead() measures that voltage like a ruler with 4096 marks: 0 at zero volts, and the top mark at 3.3 volts.")
s("s18", "map", "And map is the city map: it finds how far along the first range a number is, and returns the same spot in the second range.",
  "map de şehir haritası: bir sayının ilk aralığın neresinde olduğunu bulur ve ikinci aralıkta aynı yeri verir.",
  "Mep de şehir haritası: bir sayının ilk aralığın neresinde olduğunu bulur ve ikinci aralıkta aynı yeri verir.",
  sub="And map() is the city map: it finds how far along the first range a number is, and returns the same spot in the second range.")
s("s19", "map", "The difference from a paper map: it works with whole numbers, and it always rounds down.",
  "Kağıt haritadan farkı şu: tam sayılarla çalışır ve her zaman aşağı yuvarlar.")
s("s20", "trace2", "Let's trace the dimmer. The knob sits at the middle, the reading is about two thousand, and map turns it into a brightness of one hundred twenty-seven.",
  "Dimmer'ın izini sürelim. Düğme ortada, okuma yaklaşık iki bin; map bunu yüz yirmi yedi parlaklığa çeviriyor.",
  "Dimmerın izini sürelim. Düğme ortada, okuma yaklaşık iki bin; mep bunu yüz yirmi yedi parlaklığa çeviriyor.")
s("s21", "trace2", "Pause and predict: the knob goes all the way up. What does the brightness become? Two fifty-five, the top: every number in the panel follows the knob.",
  "Durdurun ve tahmin edin: düğme sonuna kadar çevriliyor. Parlaklık kaç olur? İki yüz elli beş, en üst: paneldeki her sayı düğmeyi takip ediyor.", pad=0.6)
s("s22", "q3", "Question three, pause the video when you need to. The yellow time in the reflex game is map from zero to four thousand ninety-five, onto one thousand to four thousand. The knob is at the middle. About how long is the yellow?",
  "Üçüncü soru; gerekirse videoyu durdurun. Refleks oyununda sarının süresi, sıfır ile dört bin doksan beş arasını bin ile dört bin arasına çeviren map. Düğme ortada. Sarı yaklaşık ne kadar sürer?",
  "Üçüncü soru; gerekirse videoyu durdurun. Refleks oyununda sarının süresi, sıfır ile dört bin doksan beş arasını bin ile dört bin arasına çeviren mep. Düğme ortada. Sarı yaklaşık ne kadar sürer?",
  sub="Question three, pause the video when you need to. The reflex game's yellow time is map(value, 0, 4095, 1000, 4000). The knob is at the middle. About how long is the yellow?", pad=THINK)
s("s23", "q3", "About two and a half seconds. Halfway along the knob is halfway between one and four seconds.",
  "Yaklaşık iki buçuk saniye. Düğmenin yarısı, bir ile dört saniyenin tam ortası.")
s("s24", "q4", "Question four, and pause the video again: someone moves an LED to pin thirty-four, and it stays dark, although the wiring is fine. Why?",
  "Dördüncü soru, yine videoyu durdurun: biri bir LED'i otuz dört numaralı pine taşıyor ve bağlantı doğru olduğu halde LED yanmıyor. Neden?",
  "Dördüncü soru, yine videoyu durdurun: biri bir ledi otuz dört numaralı pine taşıyor ve bağlantı doğru olduğu halde led yanmıyor. Neden?", pad=THINK)
s("s25", "q4", "Pins thirty-four to thirty-nine are one-way doors: they can only listen. They're perfect for a knob, but they can't drive an LED.",
  "Otuz dört ile otuz dokuz arası pinler tek yönlü kapılar: yalnızca dinleyebilirler. Düğme için harikalar ama bir LED'i süremezler.",
  "Otuz dört ile otuz dokuz arası pinler tek yönlü kapılar: yalnızca dinleyebilirler. Düğme için harikalar ama bir ledi süremezler.")
# ==== PART 3: remembering steps (episodes 9-10)
s("s26", "state", "Part three. The washing machine: wash, rinse, spin. At any moment it knows which step it's in, and it moves on when that step's time is up.",
  "Üçüncü kısım. Çamaşır makinesi: yıkama, durulama, sıkma. Her an hangi adımda olduğunu bilir ve o adımın süresi dolunca bir sonrakine geçer.")
s("s27", "state", "What actually happens: the step is one whole number called state. Moving on means two jobs, a new number and the time, and go to does both.",
  "Gerçekte olan şu: adım, state adlı tek bir tam sayı. İlerlemek iki iş demek: yeni sayı ve saat; goTo ikisini birden yapar.",
  "Gerçekte olan şu: adım, steyt adlı tek bir tam sayı. İlerlemek iki iş demek: yeni sayı ve saat; go tu ikisini birden yapar.",
  sub="What actually happens: the step is one whole number called state. Moving on means two jobs, a new number and the time, and goTo() does both.")
s("s28", "state", "The difference from a machine: our loop never waits inside a step. It looks at the number thousands of times a second, and decides.",
  "Makineden farkı şu: lup bir adımın içinde asla beklemez. Sayıya saniyede binlerce kez bakar ve karar verir.")
s("s29", "trace3", "Let's trace the reflex game. Red, yellow, and green: go to writes down the time. Now in step three, time in step counts up, like a parking ticket that's been stamped.",
  "Refleks oyununun izini sürelim. Kırmızı, sarı ve yeşil: goTo saati not ediyor. Şimdi üçüncü adımda adımdaki süre artıyor; damgası basılmış bir otopark bileti gibi.",
  "Refleks oyununun izini sürelim. Kırmızı, sarı ve yeşil: go tu saati not ediyor. Şimdi üçüncü adımda adımdaki süre artıyor; damgası basılmış bir otopark bileti gibi.")
s("s30", "trace3", "Pause and predict which number becomes the reaction. The press comes, and that time is the reaction. If it beats the record, it goes into the drawer, the flash memory that keeps it without power.",
  "Durdurun ve hangi sayının tepki süresi olacağını tahmin edin. Basış geliyor ve o süre tepki süresi oluyor. Rekoru geçerse çekmeceye, yani elektrik olmadan da saklayan flash belleğe gidiyor.",
  "Durdurun ve hangi sayının tepki süresi olacağını tahmin edin. Basış geliyor ve o süre tepki süresi oluyor. Rekoru geçerse çekmeceye, yani elektrik olmadan da saklayan flaş belleğe gidiyor.")
s("s31", "mistake", "Question five, pause the video. Someone moves on with just state equals one, and forgets the time. What happens to the next step?",
  "Beşinci soru, videoyu durdurun. Biri yalnızca state eşittir bir yazarak ilerliyor ve saati unutuyor. Bir sonraki adıma ne olur?",
  "Beşinci soru, videoyu durdurun. Biri yalnızca steyt eşittir bir yazarak ilerliyor ve saati unutuyor. Bir sonraki adıma ne olur?", pad=THINK)
s("s32", "mistake", "It ends almost at once. Its start time is the old one, so the subtraction says its time is long gone.",
  "Neredeyse hemen biter. Başlangıç zamanı eskisi; bu yüzden çıkarma, süresinin çoktan dolduğunu söyler.")
s("s33", "q6", "Question six, pause the video. In the crossing, you press the button while the walker is already crossing. Does that press count?",
  "Altıncı soru, videoyu durdurun. Geçitte yaya zaten geçerken butona basıyorsunuz. Bu basış sayılır mı?", pad=THINK)
s("s34", "q6", "No. Presses only count in step zero, when the cars have green, so the crossing never starts over by accident.",
  "Hayır. Basışlar yalnızca sıfırıncı adımda, arabalara yeşil yanarken sayılır; böylece geçit yanlışlıkla baştan başlamaz.")
s("s35", "q7", "Last question, pause the video one more time. The record is in the drawer, and you unplug the board. After the restart, what does get give back?",
  "Son soru, videoyu son kez durdurun. Rekor çekmecede ve kartı fişten çekiyorsunuz. Yeniden başlayınca get ne verir?",
  sub="Last question, pause the video one more time. The record is in the drawer, and you unplug the board. After the restart, what does getULong() give back?", pad=THINK)
s("s36", "q7", "The old record. Only an empty page gives back the default, nine nine nine nine.",
  "Eski rekoru. Varsayılan sayıyı, dokuz bin dokuz yüz doksan dokuzu yalnızca boş bir sayfa verir.",
  sub="The old record. Only an empty page gives back the default, 9999.")
s("s36b", "explain", "Before you count: pause the video, and explain in your own words what map does. One sentence is enough.",
  "Saymadan önce videoyu durdurun ve map'in ne yaptığını kendi cümlenizle açıklayın. Tek cümle yeter.",
  "Saymadan önce videoyu durdurun ve mepin ne yaptığını kendi cümlenizle açıklayın. Tek cümle yeter.", pad=4.0)
s("s36c", "explain", "One way to say it: it finds where a number sits in one range, and gives back the same spot in another range.",
  "Şöyle söylenebilir: bir sayının bir aralıkta nerede durduğunu bulur ve başka bir aralıkta aynı yeri geri verir.")
# ---- score, outro
s("s37", "score", "Count your points. Six or seven: you're ready for the next part of the course.",
  "Puanlarınızı sayın. Altı ya da yedi: kursun bir sonraki kısmına hazırsınız.")
s("s38", "score", "Fewer? Each question on the screen shows its episode. Rewatch that one, it's short, and come back.",
  "Daha az mı? Ekrandaki her sorunun yanında bölümü yazıyor. O bölümü yeniden izleyin, kısa zaten, sonra geri gelin.")
s("s39", "outro", "Next time: a light sensor, and a lamp that turns itself on when the room gets dark. Tell me your score in the comments. See you there!",
  "Gelecek sefer: bir ışık sensörü ve oda kararınca kendiliğinden yanan bir lamba. Puanınızı yorumlarda yazın. Görüşmek üzere!")

# breathing room before a new part / term (lesson_lint NEWTERM: >= 0.8 s of silence before it)
NEW_TERM = ("s03", "s05", "s08", "s10", "s12", "s16", "s17", "s18", "s20", "s26", "s29", "s36b", "s37")
for a, b in zip(S, S[1:]):
    if b["id"] in NEW_TERM:
        a["pad"] = a.get("pad", 0) + 0.4

dub = {d["id"]: d.pop("dub") for d in S}
script = {
    "episode": "recap2", "title": "Recap 2: episodes 5-10", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": "s02",
    "music": "results",
    "clips": {
        "M": "MONTAGE: existing creator clips, about 2 s each: ep05 breathing LED, ep06 colors, ep07 knob dimmer, ep08 level bar, ep09 crossing C0, ep10 reflex C0.",
    },
    "segments": S,
}
here = Path(__file__).parent
(here / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "dub").mkdir(exist_ok=True)
(here / "dub" / "tr.json").write_text(json.dumps({
    "voice": "tr-TR-EmelNeural", "rate": "+0%",
    "note": "Spoken text only. English terms are written the way a Turkish speaker says them (mep, lup, milis, steyt, skeç...).",
    "segments": dub}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
