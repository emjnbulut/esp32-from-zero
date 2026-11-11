"""Source of video/ep09/script.json (and dub/tr.json). Usage: python video/ep09/make_script.py

Episode 9 "Mini Project 1: a Smart Pedestrian Crossing" (curriculum v6), rules: PRODUCTION_GUIDELINES.md sections 9, 10, 11.
New syntax/idea: a state variable (int state = 0..3) driven by millis() with a start time per step; measuring how long a
button was held (now - pressStart). Analogies (video/ANALOGIES.md): NEW washing machine (state machine) and parking ticket
(press duration). Reused: wall clock (millis), microwave (delay), coffee machine button (helper function), comparing two
photos (edge detection), city map (map()), ruler (analogRead), click pen (blinkOn toggle).
Retrieval minute on episodes 8 and 4 (+ series-entry card, section 11). PRIMM for crossing (predict delay chain, tour with a
"pause and write step 1 yourself" (section 10: support fades from episode 9), predict the early press, run C0/C2, modify
4000 -> 8000) and press_time (predict a quick tap, run C1). Common mistake: changing state without a new start time
(animation only, no clip). One "in your own words". Your turn: slow walker mode (solution in the lesson folder; the
project homework with a solution Short is in episode 10).
Section 9 (7 Nov): at most 1-2 spoken numbers per sentence; exact values stay on screen.

Clips (creator, shoot pack p07-1): C0 full crossing cycle (opening and run), C1 press_time short + long press,
C2 walk light blinking close-up.
TR dub: lines start with native words; "skeç" (never "İşte sketçin"); map -> "mep"; loop -> "lup"; delay -> "dilay";
millis -> "milis"; state -> "steyt"; the RGB LED is "üç renkli LED"; knob = "düğme", push button = "buton".
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
s("s01", "cold", "Watch this crossing. The cars have green. I press the button, the light turns yellow, then red, and now the walker gets green.",
  "Şu yaya geçidine bakın. Arabalara yeşil yanıyor. Butona basıyorum; ışık sarıya, sonra kırmızıya dönüyor ve şimdi yayaya yeşil yanıyor.", clip="C0")
s("s02", "cold", "This is our first mini project. By the end, you'll build this crossing yourself, with one variable that remembers which step we're in.",
  "Bu bizim ilk mini projemiz. Sonunda bu geçidi kendiniz kuracaksınız; hangi adımda olduğumuzu hatırlayan tek bir değişkenle.")
# ---- retrieval minute (episodes 8 and 4) + series-entry card
s("s03", "retrieval", "New here? Episode one is on the screen. Now, two questions from earlier episodes.",
  "Yeni misiniz? Birinci bölüm ekranda. Şimdi önceki bölümlerden iki soru.")
s("s04", "retrieval", "Quick question: last time, the obvious level line almost never lit all three LEDs. Why?",
  "Kısa bir soru: geçen sefer akla ilk gelen seviye satırı üç LED'i neredeyse hiç birden yakmıyordu. Neden?",
  "Kısa bir soru: geçen sefer akla ilk gelen seviye satırı üç ledi neredeyse hiç birden yakmıyordu. Neden?", pad=THINK)
s("s05", "retrieval", "Because map rounds down. The top level only came at the very last mark of the ruler.",
  "Çünkü map aşağı yuvarlar. En üst seviye yalnızca cetvelin en son çizgisinde geliyordu.",
  "Çünkü mep aşağı yuvarlar. En üst seviye yalnızca cetvelin en son çizgisinde geliyordu.",
  sub="Because map() rounds down. The top level only came at the very last mark of the ruler.")
s("s06", "retrieval", "Quick question: how can the board tell that two seconds have passed, without freezing the program with delay?",
  "Kısa bir soru: kart, programı delay ile dondurmadan iki saniyenin geçtiğini nasıl anlar?",
  "Kısa bir soru: kart, programı dilay ile dondurmadan iki saniyenin geçtiğini nasıl anlar?",
  sub="Quick question: how can the board tell that two seconds have passed, without freezing the program with delay()?", pad=THINK)
s("s07", "retrieval", "It glances at the wall clock, millis. It subtracts the moment it remembered from now, and checks whether the difference has reached two thousand.",
  "Duvar saatine, yani millis'e göz atar. Hatırladığı anı şimdiki zamandan çıkarır ve farkın iki bine ulaşıp ulaşmadığına bakar.",
  "Duvar saatine, yani milise göz atar. Hatırladığı anı şimdiki zamandan çıkarır ve farkın iki bine ulaşıp ulaşmadığına bakar.",
  sub="It glances at the wall clock, millis(). It subtracts the moment it remembered from now, and checks whether the difference has reached 2000.")
# ---- the project and the parts
s("s08", "plan", "Here's the plan. Three LEDs are the car lights. The color LED is the walk light: red means wait, and green means walk.",
  "Plan şu. Üç LED arabaların ışığı. Üç renkli LED de yaya ışığı: kırmızı bekle, yeşil geç demek.",
  "Plan şu. Üç led arabaların ışığı. Üç renkli led de yaya ışığı: kırmızı bekle, yeşil geç demek.")
s("s09", "plan", "The button is the walker's request button. And the knob sets how long the cars keep their green, from three to ten seconds.",
  "Buton, yayanın istek butonu. Düğme de arabaların yeşilinin ne kadar süreceğini ayarlıyor: üç ile on saniye arası.")
s("s10", "plan", "Good news: you don't need a single new wire. Everything is already on the board from the earlier episodes.",
  "İyi haber: tek bir yeni kabloya gerek yok. Her şey önceki bölümlerden zaten breadboard'da.",
  "İyi haber: tek bir yeni kabloya gerek yok. Her şey önceki bölümlerden zaten breadbordda.")
s("s11", "plan", "If you're missing a part, the pins are on the screen, and the full wiring is in the lesson folder.",
  "Eksik parçanız varsa pinler ekranda; bağlantının tamamı ders klasöründe.")
# ---- why not a chain of delays
s("s12", "delay", "The first idea is a chain of delays: green, wait, yellow, wait, red, wait.",
  "Akla gelen ilk fikir bir delay zinciri: yeşil, bekle, sarı, bekle, kırmızı, bekle.",
  "Akla gelen ilk fikir bir dilay zinciri: yeşil, bekle, sarı, bekle, kırmızı, bekle.",
  sub="The first idea is a chain of delay() calls: green, wait, yellow, wait, red, wait.")
s("s13", "delay", "Pause the video and predict: with that chain, what happens to a button press while the program is waiting?",
  "Videoyu durdurun ve tahmin edin: bu zincirde program beklerken butona basılırsa ne olur?", pad=3.0)
s("s14", "delay", "It's lost. During a delay, nothing else runs, so nobody looks at the button. We need a way to wait without stopping.",
  "Kaybolur. delay sırasında başka hiçbir satır çalışmaz; butona bakan kimse yok. Durmadan beklemenin bir yolu lazım.",
  "Kaybolur. Dilay sırasında başka hiçbir satır çalışmaz; butona bakan kimse yok. Durmadan beklemenin bir yolu lazım.",
  sub="It's lost. During a delay(), nothing else runs, so nobody looks at the button. We need a way to wait without stopping.")
# ---- the idea: steps (state)
s("s15", "idea", "Think of a washing machine. It goes through steps: wash, rinse, spin. At any moment it knows exactly which step it's in, and it moves on when that step's time is up.",
  "Bir çamaşır makinesi düşünün. Adım adım ilerler: yıkama, durulama, sıkma. Her an hangi adımda olduğunu bilir ve o adımın süresi dolunca bir sonrakine geçer.")
s("s16", "idea", "Our crossing has four steps, numbered from zero: cars green, cars yellow, the walker crosses, and finally the walk light blinks, so hurry up.",
  "Bizim geçidimizin sıfırdan başlayarak numaralanmış dört adımı var: arabalara yeşil, arabalara sarı, yaya geçiyor ve son olarak yaya ışığı yanıp sönüyor; yani acele edin.")
s("s17", "idea", "What actually happens: the step is just a whole number in a variable called state. Every round of the loop checks that number, and runs only the code of that step.",
  "Gerçekte olan şu: adım, state adlı bir değişkende duran bir tam sayıdan ibaret. loop her turda bu sayıya bakar ve yalnızca o adımın kodunu çalıştırır.",
  "Gerçekte olan şu: adım, steyt adlı bir değişkende duran bir tam sayıdan ibaret. Lup her turda bu sayıya bakar ve yalnızca o adımın kodunu çalıştırır.")
s("s18", "idea", "Moving on is one assignment: put the next number into state, and write down the time. That moment is when the new step started.",
  "Bir sonraki adıma geçmek tek bir atama: state'e yeni sayıyı koyun ve saati not edin. O an, yeni adımın başladığı andır.",
  "Bir sonraki adıma geçmek tek bir atama: steyte yeni sayıyı koyun ve saati not edin. O an, yeni adımın başladığı andır.")
s("s19", "idea", "The difference from a washing machine: the machine really does its step. Our loop doesn't wait inside a step; it just looks at the number thousands of times a second, and decides.",
  "Çamaşır makinesinden farkı şu: makine o adımı gerçekten yapar. Bizim loop'umuz bir adımın içinde beklemez; sayıya saniyede binlerce kez bakar ve karar verir.",
  "Çamaşır makinesinden farkı şu: makine o adımı gerçekten yapar. Bizim lupumuz bir adımın içinde beklemez; sayıya saniyede binlerce kez bakar ve karar verir.")
# ---- code tour: crossing (top, helpers, part 1)
s("s20", "tour", "Here's the sketch, crossing. At the top, the pins, then state, which starts at zero, and the time the current step began.",
  "İşte sketch: crossing. En üstte pinler, sonra sıfırdan başlayan state ve şu anki adımın başladığı zaman.",
  "İşte, skeç: krosing. En üstte pinler, sonra sıfırdan başlayan steyt ve şu anki adımın başladığı zaman.")
s("s21", "tour", "Two small helpers keep the steps short. Lights sets all five lights in one call, like the coffee machine button from the color LED episode.",
  "İki küçük yardımcı adımları kısa tutuyor. lights, beş ışığın hepsini tek çağrıda ayarlıyor; üç renkli LED bölümündeki kahve makinesi düğmesi gibi.",
  "İki küçük yardımcı adımları kısa tutuyor. Layts, beş ışığın hepsini tek çağrıda ayarlıyor; üç renkli led bölümündeki kahve makinesi düğmesi gibi.",
  sub="Two small helpers keep the steps short. lights() sets all five lights in one call, like the coffee machine button from the color LED episode.")
s("s22", "tour", "The other one, go to, does the two jobs of moving on: it puts the new number into state, and it writes down the time.",
  "Diğeri, goTo, ilerlemenin iki işini yapıyor: state'e yeni sayıyı koyuyor ve saati not ediyor.",
  "Diğeri, go tu, ilerlemenin iki işini yapıyor: steyte yeni sayıyı koyuyor ve saati not ediyor.",
  sub="The other one, goTo(), does the two jobs of moving on: it puts the new number into state, and it writes down the time.")
s("s23", "tour", "In the loop, part one is the button, just like episode four. A new press only counts while the cars have green, and then the board remembers that somebody is waiting.",
  "loop'ta birinci kısım buton; tıpkı dördüncü bölümdeki gibi. Yeni bir basış yalnızca arabalara yeşil yanarken sayılır; o zaman kart birinin beklediğini hatırlar.",
  "Lupta birinci kısım buton; tıpkı dördüncü bölümdeki gibi. Yeni bir basış yalnızca arabalara yeşil yanarken sayılır; o zaman kart birinin beklediğini hatırlar.")
s("s23b", "tour", "Pause the video and predict: you press the button while the walker is already crossing. Does that press count?",
  "Videoyu durdurun ve tahmin edin: yaya zaten geçerken butona basıyorsunuz. Bu basış sayılır mı?", pad=3.0)
s("s23c", "tour", "No. Presses only count in step zero, so the crossing never starts over by accident.",
  "Hayır. Basışlar yalnızca sıfırıncı adımda sayılır; böylece geçit hiçbir zaman yanlışlıkla baştan başlamaz.")
# ---- part 2: the clock and the steps
s("s24", "clock", "Part two starts with one subtraction: now, minus the moment the step began. That's how long we've been in this step.",
  "İkinci kısım tek bir çıkarmayla başlıyor: şimdiki zaman eksi adımın başladığı an. Bu adımda ne kadar süredir olduğumuz bu.")
s("s25", "clock", "Next, map turns the knob into the green time, from three to ten seconds. That's last episode's function, doing a real job.",
  "Sonra map, düğmeyi yeşil süresine çeviriyor: üç ile on saniye arası. Geçen bölümün fonksiyonu burada gerçek bir iş yapıyor.",
  "Sonra mep, düğmeyi yeşil süresine çeviriyor: üç ile on saniye arası. Geçen bölümün fonksiyonu burada gerçek bir iş yapıyor.",
  sub="Next, map() turns the knob into the green time, from three to ten seconds. That's last episode's function, doing a real job.")
s("s26", "step0", "Step zero: cars green, walk light red. If somebody is waiting, and the green has lasted long enough, we go to step one.",
  "Sıfırıncı adım: arabalara yeşil, yayaya kırmızı. Biri bekliyorsa ve yeşil yeterince sürdüyse birinci adıma geçiyoruz.")
s("s27", "step0", "The two ampersands are the and from last episode's challenge: both checks must be true.",
  "İki ve işareti, geçen bölümün görevindeki 've': iki kontrolün de doğru olması gerekiyor.")
s("s28", "step1", "Now pause the video and try it yourself: write step one. The cars get yellow for two seconds, then we move to step two.",
  "Şimdi videoyu durdurun ve kendiniz deneyin: birinci adımı yazın. Arabalara iki saniye sarı yanıyor, sonra ikinci adıma geçiyoruz.", pad=4.0)
s("s29", "step1", "Here's one way. Yellow on, and once two seconds have passed, we forget the request and go to step two.",
  "İşte bir yolu. Sarı yanıyor; iki saniye geçince isteği unutuyoruz ve ikinci adıma geçiyoruz.")
s("s30", "step2", "Step two: the cars get red, and the walker gets green for four seconds.",
  "İkinci adım: arabalara kırmızı, yayaya dört saniye yeşil.")
s("s31", "step3", "Step three blinks the walk light with the same clock trick, flipping it every quarter second. After two seconds, we're back at step zero.",
  "Üçüncü adım aynı saat hilesiyle yaya ışığını yakıp söndürüyor; her çeyrek saniyede bir çeviriyor. İki saniye sonra yeniden sıfırıncı adımdayız.")
s("s32", "early", "Pause the video and predict: the cars have just turned green, and you press the button right away. Does the walker get green at once?",
  "Videoyu durdurun ve tahmin edin: arabalara yeni yeşil yandı ve hemen butona bastınız. Yayaya hemen yeşil yanar mı?", pad=3.0)
s("s33", "early", "No. The press is remembered, but the cars keep their green until the knob's time is up. Only then does yellow come.",
  "Hayır. Basış hatırlanır ama arabalar düğmenin süresi dolana kadar yeşilde kalır. Sarı ancak o zaman gelir.")
s("s34", "run", "Here it is for real. Watch the whole round, and notice the walk light switching from red to green.",
  "İşte gerçeği. Bütün turu izleyin; yaya ışığının kırmızıdan yeşile geçişine dikkat edin.", clip="C0", pad=3.0)
s("s35", "run", "Up close, the last two seconds: the walk light blinks to say hurry, and the cars are still red.",
  "Yakından son iki saniye: yaya ışığı acele edin diye yanıp sönüyor; arabalar hâlâ kırmızı.", clip="C2", pad=2.0)
s("s36", "modify", "Now change one number. Pause and predict: if four thousand becomes eight thousand, what changes?",
  "Şimdi tek bir sayıyı değiştirin. Durdurun ve tahmin edin: dört bin sekiz bin olursa ne değişir?",
  sub="Now change one number. Pause and predict: if 4000 becomes 8000, what changes?", pad=3.0)
s("s37", "modify", "The walker gets twice as long to cross. Nothing else changes, because every step keeps its own time.",
  "Yaya karşıya geçmek için iki kat süre alır. Başka hiçbir şey değişmez; çünkü her adım kendi süresini tutar.")
# ---- how long was the button held (press_time)
s("s38", "ticket", "The project has one more trick: measuring how long the button was held. Think of a parking ticket.",
  "Projenin bir hilesi daha var: butonun ne kadar basılı tutulduğunu ölçmek. Bir otopark bileti düşünün.")
s("s39", "ticket", "When you drive in, the ticket gets the time stamped on it. When you leave, the machine subtracts that time from now, and you pay for the difference.",
  "Girerken bilete saat basılır. Çıkarken makine o saati şimdiki zamandan çıkarır ve aradaki fark kadar ödersiniz.")
s("s40", "ticket", "What actually happens: at the press, we save now in a variable called press start. At the release, now minus press start is how long it was held.",
  "Gerçekte olan şu: basıldığı an şimdiki zamanı pressStart adlı bir değişkene kaydediyoruz. Bırakıldığında şimdiki zaman eksi pressStart, basılı tutulan süredir.",
  "Gerçekte olan şu: basıldığı an şimdiki zamanı pres start adlı bir değişkene kaydediyoruz. Bırakıldığında şimdiki zaman eksi pres start, basılı tutulan süredir.",
  sub="What actually happens: at the press, we save now in a variable called pressStart. At the release, now minus pressStart is how long it was held.")
s("s41", "ticket", "The difference from a ticket: there's no paper. Press start is just one number in memory, and the next press writes over it.",
  "Biletten farkı şu: ortada kağıt yok. pressStart bellekte tek bir sayı ve bir sonraki basış onun üzerine yazar.",
  "Biletten farkı şu: ortada kağıt yok. Pres start bellekte tek bir sayı ve bir sonraki basış onun üzerine yazar.",
  sub="The difference from a ticket: there's no paper. pressStart is just one number in memory, and the next press writes over it.")
s("s42", "tourpress", "Here's the sketch, press time. The yellow LED is on while you hold the button. When you let go, the Serial Monitor prints the time, and whether it was short or long.",
  "İşte sketch: press_time. Butonu basılı tuttuğunuz sürece sarı LED yanıyor. Bıraktığınızda Seri Monitör süreyi ve basışın kısa mı uzun mu olduğunu yazıyor.",
  "İşte, skeç: pres taym. Butonu basılı tuttuğunuz sürece sarı led yanıyor. Bıraktığınızda Seri Monitör süreyi ve basışın kısa mı uzun mu olduğunu yazıyor.",
  sub="Here's the sketch, press_time. The yellow LED is on while you hold the button. When you let go, the Serial Monitor prints the time, and whether it was short or long.")
s("s43", "tourpress", "Anything under a quarter of a second counts as short. Pause and predict: you tap the button as fast as you can. What will it print?",
  "Çeyrek saniyenin altı kısa sayılıyor. Durdurun ve tahmin edin: butona olabildiğince hızlı dokunuyorsunuz. Ne yazar?", pad=3.0)
s("s44", "runpress", "Something like a hundred milliseconds, and short. Hold it for a second, and it prints about a thousand, and long.",
  "Yüz milisaniye civarı bir şey ve kısa. Bir saniye basılı tutun; yaklaşık bin ve uzun yazar.", clip="C1", pad=3.0)
s("s45", "runpress", "That's how one button can do two jobs. Your phone does the same: a tap wakes it up, and a long press turns it off.",
  "Tek buton iki işi böyle yapar. Telefonunuz da aynısını yapar: kısa dokunuş ekranı açar, uzun basış kapatır.")
# ---- common mistake (animation)
s("s46", "mistake", "Now a mistake you might make. Someone moves on by just writing state equals one, and forgets to write down the time.",
  "Şimdi sizin de yapabileceğiniz bir hata. Biri bir sonraki adıma yalnızca state eşittir bir yazarak geçiyor ve saati not etmeyi unutuyor.",
  "Şimdi sizin de yapabileceğiniz bir hata. Biri bir sonraki adıma yalnızca steyt eşittir bir yazarak geçiyor ve saati not etmeyi unutuyor.")
s("s47", "mistake", "Quick question: what does the crossing do then?",
  "Kısa bir soru: geçit o zaman ne yapar?", pad=THINK)
s("s48", "mistake", "The yellow flashes for a split second, and it's gone. The step's start time is still the old one, so the subtraction says two seconds have long passed.",
  "Sarı bir an yanıp kayboluyor. Adımın başlangıç zamanı hâlâ eskisi; bu yüzden çıkarma, iki saniyenin çoktan geçtiğini söylüyor.")
s("s49", "mistake", "That's why go to always does both jobs together. Use it for every change of step.",
  "goTo bu yüzden iki işi her zaman birlikte yapıyor. Her adım değişikliğinde onu kullanın.",
  "Go tu bu yüzden iki işi her zaman birlikte yapıyor. Her adım değişikliğinde onu kullanın.",
  sub="That's why goTo() always does both jobs together. Use it for every change of step.")
# ---- explain in your own words
s("s50", "explain", "Pause the video, and explain in your own words why each step needs its own start time. One sentence is enough.",
  "Videoyu durdurun ve her adımın neden kendi başlangıç zamanına ihtiyaç duyduğunu kendi cümlenizle açıklayın. Tek cümle yeter.", pad=4.0)
s("s51", "explain", "One way to say it: every step measures its time from the moment it began. So a new step needs a new start, or it thinks its time is already up.",
  "Şöyle söylenebilir: her adım süresini başladığı andan ölçer. Bu yüzden yeni adım yeni bir başlangıç ister, yoksa süresinin çoktan dolduğunu sanır.")
# ---- your turn (the project homework with a solution Short comes in episode 10)
s("s52", "yourturn", "Your turn: a slow walker mode. If the request button is held for more than a second, the walk light stays green twice as long.",
  "Sıra sizde: yavaş yürüyen modu. İstek butonu bir saniyeden uzun basılı tutulursa yaya ışığı iki kat uzun yeşil kalır.")
s("s53", "yourturn", "You already know both pieces: the parking ticket, and a step that keeps its own time. One solution is in the lesson folder.",
  "İki parçayı da zaten biliyorsunuz: otopark bileti ve kendi süresini tutan bir adım. Bir çözüm ders klasöründe.")
# ---- outro
s("s54", "outro", "Today you built three things. A state variable that remembers the step. A start time for every step, so nothing has to wait. And a parking ticket for button presses.",
  "Bugün üç şey kurdunuz. Adımı hatırlayan bir state değişkeni. Her adım için bir başlangıç zamanı; böylece hiçbir şey beklemek zorunda kalmıyor. Ve buton basışları için bir otopark bileti.",
  "Bugün üç şey kurdunuz. Adımı hatırlayan bir steyt değişkeni. Her adım için bir başlangıç zamanı; böylece hiçbir şey beklemek zorunda kalmıyor. Ve buton basışları için bir otopark bileti.")
s("s55", "outro", "Next time, on the same circuit: a reflex game, with a high score that survives even when you unplug the board. Tell me in the comments how long your crossing's green lasts. See you there!",
  "Gelecek sefer aynı devrede: kartı fişten çekseniz bile silinmeyen bir rekorla bir refleks oyunu. Geçidinizin yeşili kaç saniye sürüyor, yorumlarda yazın. Görüşmek üzere!")

# breathing room before a new term (lesson_lint NEWTERM: >= 0.8 s of silence before it)
NEW_TERM = ("s03", "s08", "s12", "s15", "s17", "s20", "s24", "s38", "s40", "s42", "s46", "s52")
for a, b in zip(S, S[1:]):
    if b["id"] in NEW_TERM:
        a["pad"] = a.get("pad", 0) + 0.4

dub = {d["id"]: d.pop("dub") for d in S}
script = {
    "episode": 9, "title": "Mini Project 1: a Smart Pedestrian Crossing", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": "s02",
    "music": "results",
    "clips": {
        "C0": "OPENING + RUN: crossing, cars green, button pressed, a full round: yellow -> red + walk green -> walk blinks -> green.",
        "C1": "PRESS_TIME: a short tap, then a ~1 s hold; the yellow LED is on while the button is held.",
        "C2": "BLINK: close-up of the RGB walk light blinking in the last 2 s, car red on.",
    },
    "segments": S,
}
here = Path(__file__).parent
(here / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "dub").mkdir(exist_ok=True)
(here / "dub" / "tr.json").write_text(json.dumps({
    "voice": "tr-TR-EmelNeural", "rate": "+0%",
    "note": "Spoken text only. English terms are written the way a Turkish speaker says them (mep, lup, dilay, milis, steyt, skeç...).",
    "segments": dub}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
