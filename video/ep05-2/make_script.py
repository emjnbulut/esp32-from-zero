"""Source of video/ep05-2/script.json (and dub/tr.json). Usage: python video/ep05-2/make_script.py

Episode 5 · Part 2 "RGB Color Mixing" (curriculum v5, 2026-10-29), same rules as Part 1 (video/ep05-1/make_script.py):
PRODUCTION_GUIDELINES.md sections 9 and 10, video/ANALOGIES.md (phone screen dots, one straw, coffee machine button,
TV remote channel button), retrieval minute on Part 1, PRIMM for rgb_colors and color_modes, one common-mistake scene
(the RGB LED's ground wire pulled out), one "in your own words", the challenge (smart camping headlamp) at the end.
Not a mini-project: no challenge-solution Short; the solution stays in the lesson folder.
Clips = shoot pack p05-2 (video/shoot/make_pack.py): C0 opening (color_modes), C1 wiring, C2 rgb_colors,
C3 mistake (ground wire out and back), C4 color_modes run.
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
s("s01", "cold", "One LED, any color you like. Red, green, blue, and with one press, a slow drift from blue to red.",
  "Tek bir LED, istediğiniz her renk. Kırmızı, yeşil, mavi ve bir basışla maviden kırmızıya yavaş bir geçiş.",
  "Tek bir led, istediğiniz her renk. Kırmızı, yeşil, mavi ve bir basışla maviden kırmızıya yavaş bir geçiş.", clip="C0")
s("s02", "cold", "By the end of this video, you'll mix your own colors, and let a button choose between them.",
  "Bu videonun sonunda kendi renklerinizi karıştıracak ve aralarından birini bir butonla seçtireceksiniz.")
# ---- retrieval minute (part 1)
s("s03", "retrieval", "First, two questions from part one. Quick question: what does analog write with one twenty-eight do to an LED?",
  "Önce birinci kısımdan iki soru. Kısa bir soru: analogWrite ile 128 vermek bir LED'e ne yapar?",
  "Önce birinci kısımdan iki soru. Kısa bir soru: analog rayt ile yüz yirmi sekiz vermek bir lede ne yapar?",
  sub="First, two questions from part 1. Quick question: what does analogWrite() with 128 do to an LED?", pad=THINK)
s("s04", "retrieval", "It switches the pin on for about half of every cycle, very fast. Your eye sees medium brightness, but the pin is never half on.",
  "Pini her döngünün yaklaşık yarısında, çok hızlı biçimde açık tutar. Gözünüz orta parlaklık görür, ama pin hiçbir zaman yarı açık değildir.")
s("s05", "retrieval", "Quick question: in the fade without delay, why does a button press work at any moment?",
  "Kısa bir soru: delay kullanmayan geçişte buton neden her an çalışıyor?",
  "Kısa bir soru: dilay kullanmayan geçişte buton neden her an çalışıyor?", pad=THINK)
s("s06", "retrieval", "Because the loop never waits. It glances at the clock, takes a step only when it's time, and checks the button on every round.",
  "Çünkü döngü hiç beklemiyor. Saate bir göz atıyor, yalnızca zamanı geldiğinde adım atıyor ve her turda butonu kontrol ediyor.")
# ---- parts
s("s07", "parts", "You need the circuit from part one, one RGB LED, three more two-hundred-twenty ohm resistors, and a few wires.",
  "Birinci kısmın devresi, bir RGB LED, üç tane daha 220 ohm direnç ve birkaç kablo gerekiyor.",
  "Birinci kısmın devresi, bir Ar Ce Be led, üç tane daha iki yüz yirmi ohm direnç ve birkaç kablo gerekiyor.",
  sub="You need the circuit from part 1, one RGB LED, three more 220 Ω resistors, and a few wires.")
# ---- what an RGB LED is
s("s08", "rgb", "Look very closely at your phone screen, and you'll find tiny red, green and blue dots everywhere. Every color you see is made from those three.",
  "Telefonunuzun ekranına çok yakından bakın: her yerde küçük kırmızı, yeşil ve mavi noktalar göreceksiniz. Gördüğünüz her renk bu üçünden yapılıyor.")
s("s09", "rgb", "An RGB LED is the same idea. What actually happens: it's three small LEDs in one package, red, green and blue. They share one leg, the longest one.",
  "RGB LED de aynı fikir. Gerçekte olan şu: tek pakette üç küçük LED var; kırmızı, yeşil ve mavi. Bir bacağı, en uzun olanı, üçü ortak kullanıyor.",
  "Ar Ce Be led de aynı fikir. Gerçekte olan şu: tek pakette üç küçük led var; kırmızı, yeşil ve mavi. Bir bacağı, en uzun olanı, üçü ortak kullanıyor.")
s("s10", "rgb", "The difference from paint: light adds up. Red and green paint make brown, but red and green light make yellow, and all three make white.",
  "Boyadan farkı şu: ışık toplanır. Kırmızı ve yeşil boya kahverengi yapar, ama kırmızı ve yeşil ışık sarı yapar; üçü birlikte de beyaz.")
# ---- wiring
s("s11", "wire", "Unplug the USB cable, and take the green LED off the upper breadboard. We need its pin, GPIO twenty-five.",
  "USB kablosunu çıkarın ve yeşil LED'i üstteki breadboard'dan sökün. Onun pinine, GPIO 25'e ihtiyacımız var.",
  "Yu Es Be kablosunu çıkarın ve yeşil ledi üstteki breadbordtan sökün. Onun pinine, Ge Pe I O yirmi beşe ihtiyacımız var.",
  sub="Unplug the USB cable, and take the green LED off the upper breadboard. We need its pin, GPIO 25.")
s("s12", "wire", "Push the RGB LED in, with the longest leg second from the left. A black wire takes that long leg to the minus rail.",
  "RGB LED'i en uzun bacağı soldan ikinci olacak şekilde takın. Siyah bir kablo o uzun bacağı eksi raya götürüyor.",
  "Ar Ce Be ledi en uzun bacağı soldan ikinci olacak şekilde takın. Siyah bir kablo o uzun bacağı eksi raya götürüyor.")
s("s13", "wire", "Each color gets its own resistor and its own pin: red to D twenty-five, green to D twenty-six, and blue to D twenty-seven.",
  "Her rengin kendi direnci ve kendi pini var: kırmızı D25'e, yeşil D26'ya, mavi D27'ye.",
  "Her rengin kendi direnci ve kendi pini var: kırmızı De yirmi beşe, yeşil De yirmi altıya, mavi De yirmi yediye.",
  sub="Each color gets its own resistor and its own pin: red to D25, green to D26, and blue to D27.", clip="C1", pad=3.0)
s("s14", "wire", "Quick question: why three resistors, and not just one on the shared leg?",
  "Kısa bir soru: neden ortak bacakta tek direnç değil de üç direnç?", pad=THINK)
s("s15", "wire", "Because each color is its own LED, with its own current. One shared resistor is like three people drinking through one straw: whoever pulls hardest gets the most.",
  "Çünkü her renk, kendi akımı olan ayrı bir LED. Tek ortak direnç, tek pipetle içen üç kişi gibidir: en güçlü çeken en çok alır.",
  "Çünkü her renk, kendi akımı olan ayrı bir led. Tek ortak direnç, tek pipetle içen üç kişi gibidir: en güçlü çeken en çok alır.")
s("s16", "wire", "What actually happens: the colors would steal current from each other, and your mix would change. The difference from the straw: here, the color that needs the least voltage, red, takes the most.",
  "Gerçekte olan şu: renkler birbirinden akım çalar ve karışımınız değişir. Pipetten farkı şu: burada en az voltaj isteyen renk, yani kırmızı, en çok akımı alır.")
s("s17", "wire", "One thing to check: most kits have common cathode LEDs, where the long leg goes to ground. If yours is the other way around, the code has one line for that.",
  "Bir şeyi kontrol edin: çoğu sette ortak katotlu LED olur; uzun bacak toprağa gider. Sizinki tersse kodda bunun için tek bir satır var.",
  "Bir şeyi kontrol edin: çoğu sette ortak katotlu led olur; uzun bacak toprağa gider. Sizinki tersse kodda bunun için tek bir satır var.")
# ---- setColor
s("s18", "color", "To set a color, we write a helper function: set color. It works like a button on a coffee machine. One press, and it adds the right amount of three ingredients.",
  "Bir renk ayarlamak için yardımcı bir fonksiyon yazıyoruz: setColor. Kahve makinesindeki bir düğme gibi çalışıyor. Bir basış, üç malzemeden doğru miktarı koyuyor.",
  "Bir renk ayarlamak için yardımcı bir fonksiyon yazıyoruz: set kalır. Kahve makinesindeki bir düğme gibi çalışıyor. Bir basış, üç malzemeden doğru miktarı koyuyor.",
  sub="To set a color, we write a helper function: setColor(). It works like a button on a coffee machine. One press, and it adds the right amount of three ingredients.")
s("s19", "color", "What actually happens: it calls analog write three times, once for each color pin, with three numbers from zero to two fifty-five.",
  "Gerçekte olan şu: analogWrite'ı üç kez çağırıyor, her renk pini için bir kez; sıfır ile 255 arasında üç sayıyla.",
  "Gerçekte olan şu: analog raytı üç kez çağırıyor, her renk pini için bir kez; sıfır ile iki yüz elli beş arasında üç sayıyla.",
  sub="What actually happens: it calls analogWrite() three times, once for each color pin, with three numbers from 0 to 255.")
s("s20", "color", "The difference from the coffee machine: it doesn't remember a recipe. You tell it all three amounts, every single time.",
  "Kahve makinesinden farkı şu: bir tarif hatırlamıyor. Üç miktarı da her seferinde siz söylüyorsunuz.")
s("s21", "color", "Quick question: red two fifty-five, green zero, blue two fifty-five. What color do you get?",
  "Kısa bir soru: kırmızı 255, yeşil sıfır, mavi 255. Hangi rengi elde edersiniz?",
  "Kısa bir soru: kırmızı iki yüz elli beş, yeşil sıfır, mavi iki yüz elli beş. Hangi rengi elde edersiniz?",
  sub="Quick question: red 255, green 0, blue 255. What color do you get?", pad=THINK)
s("s22", "color", "Magenta, a pinkish purple. And you're not limited to full values: red two fifty-five with just forty green gives orange.",
  "Macenta, pembemsi bir mor. Üstelik tam değerlerle sınırlı değilsiniz: kırmızı 255 ve yalnızca 40 yeşil turuncu verir.",
  "Macenta, pembemsi bir mor. Üstelik tam değerlerle sınırlı değilsiniz: kırmızı iki yüz elli beş ve yalnızca kırk yeşil turuncu verir.",
  sub="Magenta, a pinkish purple. And you're not limited to full values: red 255 with just 40 green gives orange.")
# ---- code tour: rgb_colors
s("s23", "tourrgb", "Here's the whole sketch, RGB colors. Three pin names, one for each color, and a switch called common anode, which stays false for most kits.",
  "İşte sketch'in tamamı: rgb_colors. Her renk için bir tane, üç pin adı ve COMMON_ANODE adında bir anahtar; çoğu sette false kalıyor.",
  "İşte sketçin tamamı: Ar Ce Be kalırs. Her renk için bir tane, üç pin adı ve komın anod adında bir anahtar; çoğu sette fols kalıyor.",
  sub="Here's the whole sketch, rgb_colors. Three pin names, one for each color, and a switch called COMMON_ANODE, which stays false for most kits.")
s("s24", "tourrgb", "Set color takes three numbers. If your LED is common anode, it flips each value first, because there, two fifty-five means off.",
  "setColor üç sayı alıyor. LED'iniz ortak anotluysa önce her değeri ters çeviriyor, çünkü orada 255 kapalı demek.",
  "Set kalır üç sayı alıyor. Lediniz ortak anotluysa önce her değeri ters çeviriyor, çünkü orada iki yüz elli beş kapalı demek.",
  sub="setColor() takes three numbers. If your LED is common anode, it flips each value first, because there, 255 means off.")
s("s25", "tourrgb", "In the loop, read every line as red, green, blue. Pause the video and predict the fourth line: two fifty-five, two fifty-five, zero. Which color is it?",
  "loop'ta her satırı kırmızı, yeşil, mavi diye okuyun. Videoyu durdurun ve dördüncü satırı tahmin edin: 255, 255, sıfır. Hangi renk?",
  "Lupta her satırı kırmızı, yeşil, mavi diye okuyun. Videoyu durdurun ve dördüncü satırı tahmin edin: iki yüz elli beş, iki yüz elli beş, sıfır. Hangi renk?",
  sub="In the loop, read every line as red, green, blue. Pause the video and predict the fourth line: 255, 255, 0. Which color is it?", pad=3.0)
s("s26", "tourrgb", "Full red plus full green: yellow. Each color stays for one second, and after orange, the list starts again.",
  "Tam kırmızı artı tam yeşil: sarı. Her renk bir saniye kalıyor; turuncudan sonra liste yeniden başlıyor.")
s("s27", "run", "Let's run it: red, green, blue, yellow, magenta, cyan, white, and orange.",
  "Çalıştıralım: kırmızı, yeşil, mavi, sarı, macenta, camgöbeği, beyaz ve turuncu.", clip="C2", pad=2.5)
s("s27b", "run", "Notice that yellow looks a little green, and magenta a little blue. The three colors aren't equally bright. Try lowering green and blue to balance them.",
  "Sarının biraz yeşil, macentanın biraz mavi göründüğüne dikkat edin. Üç renk eşit parlak değil. Dengelemek için yeşili ve maviyi biraz düşürmeyi deneyin.")
# ---- common mistake: no way back to ground
s("s28", "mistake", "Quick question: the colors are running. What happens if this black wire comes loose?",
  "Kısa bir soru: renkler dönüyor. Bu siyah kablo yerinden çıkarsa ne olur?", pad=THINK)
s("s29", "mistake", "Watch. The LED goes dark, every color at once. Push the wire back, and the colors return.",
  "İzleyin. LED sönüyor, bütün renkler aynı anda. Kabloyu geri takınca renkler geri geliyor.",
  "İzleyin. Led sönüyor, bütün renkler aynı anda. Kabloyu geri takınca renkler geri geliyor.", clip="C3", pad=2.5)
s("s30", "mistake", "Remember episode two: current has to flow in a full circle, out of the pin and back to ground. The shared leg is the only way back for all three colors.",
  "İkinci bölümü hatırlayın: akım tam bir tur atmak zorunda; pinden çıkıp toprağa geri dönmeli. Ortak bacak, üç rengin de tek dönüş yolu.")
s("s31", "mistake", "So when one color never lights, check that color's own wire. When all three go dark together, check the shared wire first.",
  "Yani bir renk hiç yanmıyorsa o rengin kendi kablosuna bakın. Üçü birden sönüyorsa önce ortak kabloya bakın.")
# ---- modes with the button
s("s32", "modes", "Now the button picks the color, like the channel button on a TV remote. We keep a number called mode, and every new press adds one.",
  "Şimdi rengi buton seçsin; televizyon kumandasındaki kanal düğmesi gibi. mode adında bir sayı tutuyoruz ve her yeni basış ona bir ekliyor.",
  "Şimdi rengi buton seçsin; televizyon kumandasındaki kanal düğmesi gibi. Mod adında bir sayı tutuyoruz ve her yeni basış ona bir ekliyor.")
s("s33", "modes", "Quick question: there are four modes, zero to three. Mode is three, and you press again. What should happen?",
  "Kısa bir soru: dört mod var, sıfırdan üçe. mode üç ve tekrar basıyorsunuz. Ne olmalı?",
  "Kısa bir soru: dört mod var, sıfırdan üçe. Mod üç ve tekrar basıyorsunuz. Ne olmalı?", pad=THINK)
s("s34", "modes", "It should go back to zero, just like the remote jumps from the last channel to the first. What actually happens: mode becomes four for a moment, and the next line sees that it's greater than three, and sets it to zero.",
  "Sıfıra dönmeli; tıpkı kumandanın son kanaldan ilk kanala atlaması gibi. Gerçekte olan şu: mode bir anlığına dört oluyor, sonraki satır üçten büyük olduğunu görüyor ve onu sıfır yapıyor.",
  "Sıfıra dönmeli; tıpkı kumandanın son kanaldan ilk kanala atlaması gibi. Gerçekte olan şu: mod bir anlığına dört oluyor, sonraki satır üçten büyük olduğunu görüyor ve onu sıfır yapıyor.")
s("s35", "modes", "The difference from a remote: there's no screen showing the number. Mode lives only in memory, so printing it is the easiest way to check it.",
  "Kumandadan farkı şu: sayıyı gösteren bir ekran yok. mode yalnızca hafızada yaşıyor; bu yüzden onu kontrol etmenin en kolay yolu yazdırmak.",
  "Kumandadan farkı şu: sayıyı gösteren bir ekran yok. Mod yalnızca hafızada yaşıyor; bu yüzden onu kontrol etmenin en kolay yolu yazdırmak.")
# ---- code tour: color_modes
s("s36", "tourmodes", "Here's the whole sketch, color modes. Good news: nothing in it is really new. It's the button from episode four, set color, and the fade from part one, put together.",
  "İşte sketch'in tamamı: color_modes. İyi haber: içinde gerçekten yeni bir şey yok. Dördüncü bölümün butonu, setColor ve birinci kısmın geçişi bir araya gelmiş.",
  "İşte sketçin tamamı: kalır mods. İyi haber: içinde gerçekten yeni bir şey yok. Dördüncü bölümün butonu, set kalır ve birinci kısmın geçişi bir araya gelmiş.",
  sub="Here's the whole sketch, color_modes. Good news: nothing in it is really new. It's the button from episode 4, setColor(), and the fade from part 1, put together.")
s("s37", "tourmodes", "Part two of the loop has one if for each mode. Else if means: only check this one if everything before it was false. Zero is red, one is green, and two is blue.",
  "loop'un ikinci kısmında her mod için bir if var. else if şu demek: bunu yalnızca öncekilerin hepsi yanlışsa kontrol et. Sıfır kırmızı, bir yeşil, iki mavi.",
  "Lupun ikinci kısmında her mod için bir if var. Els if şu demek: bunu yalnızca öncekilerin hepsi yanlışsa kontrol et. Sıfır kırmızı, bir yeşil, iki mavi.",
  sub="Part two of the loop has one if for each mode. else if means: only check this one if everything before it was false. 0 is red, 1 is green, and 2 is blue.")
s("s38", "tourmodes", "The last else is mode three, the slow fade. Every eight milliseconds, level takes a step, and set color gets level for red, and two fifty-five minus level for blue.",
  "Sondaki else üçüncü mod, yavaş geçiş. Her sekiz milisaniyede level bir adım atıyor; setColor kırmızı için level, mavi için 255 eksi level alıyor.",
  "Sondaki els üçüncü mod, yavaş geçiş. Her sekiz milisaniyede levıl bir adım atıyor; set kalır kırmızı için levıl, mavi için iki yüz elli beş eksi levıl alıyor.",
  sub="The last else is mode 3, the slow fade. Every 8 milliseconds, level takes a step, and setColor() gets level for red, and 255 minus level for blue.")
s("s39", "tourmodes", "Pause the video and predict: halfway through the fade, level is about one twenty-eight. What color do you see?",
  "Videoyu durdurun ve tahmin edin: geçişin yarısında level yaklaşık 128. Hangi rengi görürsünüz?",
  "Videoyu durdurun ve tahmin edin: geçişin yarısında levıl yaklaşık yüz yirmi sekiz. Hangi rengi görürsünüz?",
  sub="Pause the video and predict: halfway through the fade, level is about 128. What color do you see?", pad=3.0)
s("s40", "tourmodes", "Purple. Half red and half blue. As red goes up, blue goes down, so together they always add up to two fifty-five.",
  "Mor. Yarı kırmızı, yarı mavi. Kırmızı arttıkça mavi azalıyor; bu yüzden ikisinin toplamı hep 255.",
  "Mor. Yarı kırmızı, yarı mavi. Kırmızı arttıkça mavi azalıyor; bu yüzden ikisinin toplamı hep iki yüz elli beş.",
  sub="Purple. Half red and half blue. As red goes up, blue goes down, so together they always add up to 255.")
s("s41", "run2", "Let's run it. Three presses: red, green, blue, and the fade begins. Each press changes the color instantly, even in the middle of the fade.",
  "Çalıştıralım. Üç basış: kırmızı, yeşil, mavi ve geçiş başlıyor. Her basış rengi anında değiştiriyor, geçişin ortasında bile.", clip="C4", pad=2.5)
# ---- explain in your own words
s("s42", "explain", "Now pause the video, and explain in your own words why mode goes back to zero after three. One sentence is enough.",
  "Şimdi videoyu durdurun ve mode'un üçten sonra neden sıfıra döndüğünü kendi cümlenizle açıklayın. Tek cümle yeter.",
  "Şimdi videoyu durdurun ve modun üçten sonra neden sıfıra döndüğünü kendi cümlenizle açıklayın. Tek cümle yeter.", pad=4.0)
s("s43", "explain", "One way to say it: there are only four colors, so when the count goes past the last one, the code starts the circle again.",
  "Şöyle söylenebilir: yalnızca dört renk var; sayaç sonuncuyu geçince kod çemberi baştan başlatıyor.")
# ---- your turn (not a mini-project: the solution stays in the lesson folder)
s("s44", "challenge", "Your turn: build a smart camping headlamp. One button cycles four modes: off, dim white, bright white, and red blink.",
  "Sıra sizde: akıllı bir kamp kafa lambası yapın. Tek buton dört mod arasında geçiş yapsın: kapalı, loş beyaz, parlak beyaz ve yanıp sönen kırmızı.")
s("s45", "challenge", "The twist: if the lamp has been on for three seconds or more, the next press switches it straight off. Hint: remember when the mode last changed.",
  "İşin püf noktası: lamba üç saniye ya da daha uzun süredir açıksa sıradaki basış onu doğrudan kapatsın. İpucu: modun en son ne zaman değiştiğini hatırlayın.")
# ---- outro
s("s46", "outro", "Today you learned three things. An RGB LED is three LEDs in one. Set color mixes them with three numbers. And a mode counter lets one button choose.",
  "Bugün üç şey öğrendiniz. RGB LED, tek pakette üç LED'dir. setColor onları üç sayıyla karıştırır. Bir mod sayacı da tek butonla seçim yaptırır.",
  "Bugün üç şey öğrendiniz. Ar Ce Be led, tek pakette üç leddir. Set kalır onları üç sayıyla karıştırır. Bir mod sayacı da tek butonla seçim yaptırır.",
  sub="Today you learned three things. An RGB LED is three LEDs in one. setColor() mixes them with three numbers. And a mode counter lets one button choose.")
s("s47", "outro", "Next time: a knob. We'll read a potentiometer, and turn it into brightness. Post your headlamp in the comments; one solution is in the lesson folder. See you there!",
  "Gelecek sefer: bir düğme. Bir potansiyometreyi okuyup parlaklığa dönüştüreceğiz. Kafa lambanızı yorumlara yazın; bir çözüm ders klasöründe. Görüşmek üzere!")

# breathing room before a new term (lesson_lint NEWTERM: >= 0.8 s of silence before it)
NEW_TERM = ("s03", "s07", "s09", "s17", "s18", "s23", "s37")
for a, b in zip(S, S[1:]):
    if b["id"] in NEW_TERM:
        a["pad"] = a.get("pad", 0) + 0.4

dub = {d["id"]: d.pop("dub") for d in S}
script = {
    "episode": 5, "part": 2, "title": "RGB Color Mixing", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": "s02",
    "music": "results",
    "clips": {
        "C0": "OPENING, 12-15 s: color_modes; RGB LED centred; 3 presses: red -> green -> blue -> slow fade, 3-4 s of the fade.",
        "C1": "WIRING, USB unplugged, from above, 20-40 s: green LED off; RGB in (longest leg 2nd), black wire 21a -> minus rail, three 220 ohm resistors, wires D25/D26/D27. Speed-ramped in the edit.",
        "C2": "rgb_colors, 10-12 s: red, green, blue, yellow, magenta, cyan, white, orange. Slightly dim room.",
        "C3": "COMMON MISTAKE, 8-10 s: rgb_colors running; pull the RGB's black wire (21a): dark; push it back: colours return.",
        "C4": "color_modes, 10 s, closer than C0: three presses, the fade starts.",
    },
    "segments": S,
}
here = Path(__file__).parent
(here / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "dub").mkdir(exist_ok=True)
(here / "dub" / "tr.json").write_text(json.dumps({
    "voice": "tr-TR-EmelNeural", "rate": "+0%",
    "note": "Spoken text only. English terms are written the way a Turkish speaker says them (analog rayt, set kalır, lup...).",
    "segments": dub}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
