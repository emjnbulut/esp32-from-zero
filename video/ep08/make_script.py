"""Source of video/ep08/script.json (and dub/tr.json). Usage: python video/ep08/make_script.py

Episode 8 "map(), Dimmer Knobs and Level Bars" (curriculum v6), rules: PRODUCTION_GUIDELINES.md sections 9, 10, 11;
video/ANALOGIES.md: new rows city map (map()) and phone battery bars (level bar); reused: ruler (analogRead), stove marks
(if / else if), doctor's thermometer (print first). Retrieval minute on episode 7, PRIMM for map_dimmer (predict, C2 run,
tour, modify = flipped range) and level_bar (predict the 0..3 trap, fix, tour, C3 run), one common mistake (yellow LED in
backwards, C4), one "in your own words", the challenge (Rotary Safe Lock) at the end.
Not a mini-project: no challenge-solution Short; the solution stays in the lesson folder.
Section 9 (7 Nov): at most 1-2 spoken numbers per sentence; full values stay on screen (the safe-lock targets are a card).

Clips (creator, footage/gelen/ep06/CLIPS.md part 06-2, prepared into footage/ep08):
C0 opening level_bar, C1 wiring (yellow/green LEDs placed, knob moved up), C2 map_dimmer, C3 level_bar run (closer), C4 yellow reversed.
TR dub: lines start with native words; "skeç" (never "İşte sketçin"); map -> "mep"; no "Ar Ce Be": the RGB LED is "üç renkli LED".
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
s("s01", "cold", "Watch this bar of lights. I turn the knob, and it fills up: green, then yellow, then red, like a volume meter.",
  "Şu ışık çubuğuna bakın. Düğmeyi çeviriyorum ve çubuk doluyor: önce yeşil, sonra sarı, sonra kırmızı; tıpkı bir ses göstergesi gibi.", clip="C0")
s("s02", "cold", "By the end of this video, you'll turn one range of numbers into another with a single function, and you'll build this bar yourself.",
  "Bu videonun sonunda tek bir fonksiyonla bir sayı aralığını başka bir aralığa çevireceksiniz ve bu çubuğu kendiniz kuracaksınız.")
# ---- retrieval minute (episode 7)
s("s03", "retrieval", "First, two questions from the last episode. Quick question: the knob sits in the middle. Roughly what number does analog read give you?",
  "Önce geçen bölümden iki soru. Kısa bir soru: düğme tam ortada. analogRead size yaklaşık hangi sayıyı verir?",
  "Önce geçen bölümden iki soru. Kısa bir soru: düğme tam ortada. Analog rid size yaklaşık hangi sayıyı verir?",
  sub="First, two questions from the last episode. Quick question: the knob sits in the middle. Roughly what number does analogRead() give you?", pad=THINK)
s("s04", "retrieval", "About two thousand, half of the ruler. The whole ruler goes up to about four thousand.",
  "Yaklaşık iki bin, yani cetvelin yarısı. Cetvelin tamamı yaklaşık dört bine kadar gidiyor.")
s("s05", "retrieval", "Quick question: the LED ignores the knob completely. What's the very first thing you do?",
  "Kısa bir soru: LED düğmeyi hiç umursamıyor. İlk iş ne yaparsınız?",
  "Kısa bir soru: led düğmeyi hiç umursamıyor. İlk iş ne yaparsınız?", pad=THINK)
s("s06", "retrieval", "You print the value, like a doctor taking your temperature. The number tells you which half of the circuit to look at.",
  "Değeri yazdırırsınız; tıpkı doktorun ateşinizi ölçmesi gibi. Sayı, devrenin hangi yarısına bakmanız gerektiğini söyler.")
# ---- parts
s("s07", "parts", "You need last episode's circuit, with the knob and the red LED. Add a yellow LED, a green LED, a two hundred twenty ohm resistor for each, and a few wires.",
  "Geçen bölümün devresi gerekiyor: düğme ve kırmızı LED. Buna bir sarı LED, bir yeşil LED, her birine bir 220 ohm direnç ve birkaç kablo ekleyin.",
  "Geçen bölümün devresi gerekiyor: düğme ve kırmızı led. Buna bir sarı led, bir yeşil led, her birine bir iki yüz yirmi ohm direnç ve birkaç kablo ekleyin.",
  sub="You need last episode's circuit, with the knob and the red LED. Add a yellow LED, a green LED, a 220 Ω resistor for each, and a few wires.")
# ---- the idea: map()
s("s08", "idea", "Last time, we squeezed the knob's big scale into the LED's small one by dividing by sixteen. It worked, but anyone reading the code has to figure out where sixteen came from.",
  "Geçen sefer düğmenin büyük ölçeğini 16'ya bölerek LED'in küçük ölçeğine sığdırdık. İşe yaradı; ama kodu okuyan herkes 16'nın nereden geldiğini kendisi çözmek zorunda.",
  "Geçen sefer düğmenin büyük ölçeğini on altıya bölerek ledin küçük ölçeğine sığdırdık. İşe yaradı; ama kodu okuyan herkes on altının nereden geldiğini kendisi çözmek zorunda.",
  sub="Last time, we squeezed the knob's big scale into the LED's small one by dividing by 16. It worked, but anyone reading the code has to figure out where 16 came from.")
s("s09", "idea", "Think of a city map. Every street in the city has its matching spot on the paper, and halfway across town is halfway across the map.",
  "Bir şehir haritası düşünün. Şehirdeki her sokağın kağıtta kendine denk gelen bir yeri var; şehrin yarısı, haritanın da yarısıdır.")
s("s10", "idea", "Arduino has a function with exactly that name: map. You give it a number, the range it comes from, and the range you want, and it gives back the matching number.",
  "Arduino'da tam da bu adı taşıyan bir fonksiyon var: map, yani İngilizcede harita. Ona bir sayı, sayının geldiği aralığı ve istediğiniz aralığı verirsiniz; o da size denk gelen sayıyı geri verir.",
  "Arduinoda tam da bu adı taşıyan bir fonksiyon var: mep, yani İngilizcede harita. Ona bir sayı, sayının geldiği aralığı ve istediğiniz aralığı verirsiniz; o da size denk gelen sayıyı geri verir.",
  sub="Arduino has a function with exactly that name: map(). You give it a number, the range it comes from, and the range you want, and it gives back the matching number.")
s("s11", "idea", "What actually happens: map is plain arithmetic. It works out how far along the first range your number is, and returns the same position in the second range.",
  "Gerçekte olan şu: map sıradan bir hesaplama. Sayınızın ilk aralıkta ne kadar ilerde olduğunu bulur ve ikinci aralıkta aynı konumu döndürür.",
  "Gerçekte olan şu: mep sıradan bir hesaplama. Sayınızın ilk aralıkta ne kadar ilerde olduğunu bulur ve ikinci aralıkta aynı konumu döndürür.",
  sub="What actually happens: map() is plain arithmetic. It works out how far along the first range your number is, and returns the same position in the second range.")
s("s12", "idea", "The difference from a paper map: a paper map can only shrink things. Map can also stretch a small range, or even flip one, so the top becomes the bottom.",
  "Kağıt haritadan farkı şu: kağıt harita her şeyi yalnızca küçültebilir. map ise küçük bir aralığı büyütebilir, hatta ters çevirebilir; tepe dibe döner.",
  "Kağıt haritadan farkı şu: kağıt harita her şeyi yalnızca küçültebilir. Mep ise küçük bir aralığı büyütebilir, hatta ters çevirebilir; tepe dibe döner.",
  sub="The difference from a paper map: a paper map can only shrink things. map() can also stretch a small range, or even flip one, so the top becomes the bottom.")
# ---- the map line
s("s13", "mapline", "Here's the line. First comes the number, the knob's value. Then where the knob's range starts and ends. Then where the brightness range starts and ends.",
  "İşte o satır. Önce sayı geliyor, yani düğmenin değeri. Sonra düğme aralığının başı ve sonu. Sonra da parlaklık aralığının başı ve sonu.")
s("s14", "mapline", "Quick question: the knob reads about two thousand, roughly the middle. What brightness does map give back?",
  "Kısa bir soru: düğme yaklaşık iki bin okuyor, kabaca ortası. map hangi parlaklığı geri verir?",
  "Kısa bir soru: düğme yaklaşık iki bin okuyor, kabaca ortası. Mep hangi parlaklığı geri verir?",
  sub="Quick question: the knob reads about 2000, roughly the middle. What brightness does map() give back?", pad=THINK)
s("s15", "mapline", "About one twenty-seven, the middle of the brightness range. In at the middle, out at the middle.",
  "Yaklaşık 127, parlaklık aralığının ortası. Ortadan girer, ortadan çıkar.",
  "Yaklaşık yüz yirmi yedi, parlaklık aralığının ortası. Ortadan girer, ortadan çıkar.",
  sub="About 127, the middle of the brightness range. In at the middle, out at the middle.")
# ---- code tour: map_dimmer (PRIMM)
s("s16", "tourdim", "Here's the whole sketch, map dimmer. It's last episode's dimmer with one change: the dividing line is now a map line.",
  "Şimdi sketch'in tamamı: map_dimmer. Geçen bölümün dimmer'ı, tek bir farkla: bölme satırı artık bir map satırı.",
  "Şimdi skeçin tamamı: mep dimır. Geçen bölümün dimırı, tek bir farkla: bölme satırı artık bir mep satırı.",
  sub="Here's the whole sketch, map_dimmer. It's last episode's dimmer with one change: the dividing line is now a map() line.")
s("s17", "tourdim", "In the loop, analog read puts the knob's number into value. Then map turns value into brightness, and the last line sends brightness to the red LED.",
  "loop'ta analogRead düğmenin sayısını value'ya koyuyor. Sonra map, value'yu brightness'a çeviriyor; son satır da brightness'ı kırmızı LED'e gönderiyor.",
  "Lupta analog rid düğmenin sayısını velyuya koyuyor. Sonra mep, velyuyu braytnısa çeviriyor; son satır da braytnısı kırmızı lede gönderiyor.",
  sub="In the loop, analogRead() puts the knob's number into value. Then map() turns value into brightness, and the last line sends brightness to the red LED.")
s("s18", "tourdim", "Pause the video and predict: will the LED look any different from last episode's version, the one that divided by sixteen?",
  "Videoyu durdurun ve tahmin edin: LED, geçen bölümün 16'ya bölen sürümünden farklı görünecek mi?",
  "Videoyu durdurun ve tahmin edin: led, geçen bölümün on altıya bölen sürümünden farklı görünecek mi?",
  sub="Pause the video and predict: will the LED look any different from last episode's version, the one that divided by 16?", pad=3.0)
s("s19", "rundim", "No. It looks the same, smooth from dark to full. The difference is in the code: anyone can read this line and see both ranges.",
  "Hayır. Aynı görünüyor; karanlıktan tam parlaklığa pürüzsüz. Fark kodda: bu satırı okuyan herkes iki aralığı da görüyor.", clip="C2", pad=3.0)
s("s20", "flip", "Now let's change one thing. Pause the video and predict: what happens if we swap the last two numbers, so the brightness range runs from two fifty-five down to zero?",
  "Şimdi tek bir şey değiştirelim. Videoyu durdurun ve tahmin edin: son iki sayının yerini değiştirirsek, yani parlaklık aralığı 255'ten sıfıra inerse ne olur?",
  "Şimdi tek bir şey değiştirelim. Videoyu durdurun ve tahmin edin: son iki sayının yerini değiştirirsek, yani parlaklık aralığı iki yüz elli beşten sıfıra inerse ne olur?",
  sub="Now let's change one thing. Pause the video and predict: what happens if we swap the last two numbers, so the brightness range runs from 255 down to 0?", pad=3.0)
s("s21", "flip", "The knob works backwards. Turned to the left, the LED is bright, and turned to the right, it goes dark. That's the flip I mentioned.",
  "Düğme ters çalışır. Sola çevrilince LED parlak, sağa çevrilince karanlık. Bahsettiğim ters çevirme buydu.",
  "Düğme ters çalışır. Sola çevrilince led parlak, sağa çevrilince karanlık. Bahsettiğim ters çevirme buydu.")
# ---- the level bar idea
s("s22", "bar", "Next, the bar of lights. Think of the battery icon on your phone: the more charge, the more bars.",
  "Sırada ışık çubuğu var. Telefonunuzdaki pil simgesini düşünün: şarj arttıkça çubuklar da artar.")
s("s23", "bar", "What actually happens: we turn the knob's number into a small level, from zero up to three. The level says how many LEDs are on, counting from green.",
  "Gerçekte olan şu: düğmenin sayısını sıfırdan üçe kadar küçük bir seviyeye çeviriyoruz. Seviye, yeşilden başlayarak kaç LED'in yanacağını söylüyor.",
  "Gerçekte olan şu: düğmenin sayısını sıfırdan üçe kadar küçük bir seviyeye çeviriyoruz. Seviye, yeşilden başlayarak kaç ledin yanacağını söylüyor.")
s("s24", "bar", "The difference from a phone: your phone hides many tiny steps behind each bar. Our bar has only four states, from empty to full.",
  "Telefondan farkı şu: telefonunuz her çubuğun arkasında birçok küçük adım saklar. Bizim çubuğumuzun ise yalnızca dört hâli var: boştan doluya.")
# ---- wiring
s("s25", "wire", "Unplug the cable. The yellow LED goes to pin eighteen, and the green one to pin seventeen. Each one gets its own resistor, just like the red one.",
  "Kabloyu çıkarın. Sarı LED 18. pine, yeşil LED de 17. pine gidiyor. Her biri, tıpkı kırmızı gibi, kendi direncini alıyor.",
  "Kabloyu çıkarın. Sarı led on sekizinci pine, yeşil led de on yedinci pine gidiyor. Her biri, tıpkı kırmızı gibi, kendi direncini alıyor.",
  sub="Unplug the cable. The yellow LED goes to pin 18, and the green one to pin 17. Each one gets its own resistor, just like the red one.", clip="C1", pad=3.0)
s("s25b", "wire", "Careful with that last one: on most boards, pin seventeen is printed as T X two, not D seventeen.",
  "Sonuncusuna dikkat: çoğu kartta 17. pinin üzerinde D17 değil, TX2 yazar.",
  "Sonuncusuna dikkat: çoğu kartta on yedinci pinin üzerinde De on yedi değil, Te İks iki yazar.",
  sub="Careful with that last one: on most boards, pin 17 is printed as TX2, not D17.")
s("s26", "wire", "Long leg toward the pin, short leg toward the minus rail. Keep that in mind, because it comes back in a minute.",
  "Uzun bacak pine doğru, kısa bacak eksi raya doğru. Bunu aklınızda tutun; birazdan geri gelecek.")
s("s27", "wire", "If the board gets crowded, move the knob higher up, and its wires simply move with it. If your power rails are split in the middle, keep the bridge wires.",
  "Breadboard kalabalıklaşırsa düğmeyi biraz yukarı taşıyın; kabloları da onunla birlikte taşınır. Güç raylarınız ortada kesikse köprü kablolarını yerinde bırakın.",
  "Breadbord kalabalıklaşırsa düğmeyi biraz yukarı taşıyın; kabloları da onunla birlikte taşınır. Güç raylarınız ortada kesikse köprü kablolarını yerinde bırakın.")
# ---- the level line: a trap and its fix
s("s28", "level", "Now the level. The obvious line maps the knob's range onto zero to three.",
  "Şimdi seviye. Akla ilk gelen satır, düğmenin aralığını sıfırdan üçe eşliyor.")
s("s29", "level", "Pause the video and predict: with this line, how often will you see all three LEDs on?",
  "Videoyu durdurun ve tahmin edin: bu satırla üç LED'in birden yandığını ne sıklıkla görürsünüz?",
  "Videoyu durdurun ve tahmin edin: bu satırla üç ledin birden yandığını ne sıklıkla görürsünüz?", pad=3.0)
s("s30", "level", "Almost never. Map works with whole numbers, and it simply drops anything after the point. So two point nine becomes two.",
  "Neredeyse hiç. map tam sayılarla çalışır ve virgülden sonrasını basitçe atar. Yani 2,9, iki olur.",
  "Neredeyse hiç. Mep tam sayılarla çalışır ve virgülden sonrasını basitçe atar. Yani iki virgül dokuz, iki olur.",
  sub="Almost never. map() works with whole numbers, and it simply drops anything after the point. So 2.9 becomes 2.")
s("s31", "level", "Level three only comes at the very last mark of the ruler. And last episode, we saw that the ruler may never reach that mark.",
  "Üçüncü seviye yalnızca cetvelin en son çizgisinde gelir. Geçen bölümde de cetvelin o çizgiye hiç ulaşmayabileceğini gördük.")
s("s32", "level", "The fix: ask for four levels, and pretend the ruler is one mark longer. The reading never gets to four, so it stops at three, and every level gets an equal slice of the knob.",
  "Çözüm şu: dört seviye isteyin ve cetveli bir çizgi daha uzunmuş gibi düşünün. Okuma hiçbir zaman dörde varmaz, üçte kalır; böylece her seviye düğmeden eşit bir dilim alır.")
# ---- code tour: level_bar
s("s33", "tourbar", "Here's the sketch, level bar. Setup makes three pins outputs. In the loop, we read the knob, and map gives us the level.",
  "İşte sketch: level_bar. setup üç pini çıkış yapıyor. loop'ta düğmeyi okuyoruz ve map bize seviyeyi veriyor.",
  "İşte skeç: levıl bar. Set ap üç pini çıkış yapıyor. Lupta düğmeyi okuyoruz ve mep bize seviyeyi veriyor.",
  sub="Here's the sketch, level_bar. setup() makes three pins outputs. In the loop, we read the knob, and map() gives us the level.")
s("s34", "tourbar", "Then come the stove marks from last time, if and else if. Level zero turns all three off. Level one lights only green, and level two adds yellow.",
  "Sonra geçen seferki ocak işaretleri geliyor: if ve else if. Seviye sıfır üçünü de söndürüyor. Seviye bir yalnızca yeşili yakıyor, seviye iki de sarıyı ekliyor.",
  "Sonra geçen seferki ocak işaretleri geliyor: if ve els if. Seviye sıfır üçünü de söndürüyor. Seviye bir yalnızca yeşili yakıyor, seviye iki de sarıyı ekliyor.")
s("s35", "tourbar", "If it's none of those, it must be three, so the last else lights everything.",
  "Hiçbiri değilse üç olmak zorunda; bu yüzden son else hepsini yakıyor.",
  "Hiçbiri değilse üç olmak zorunda; bu yüzden son els hepsini yakıyor.")
s("s36", "tourbar", "Pause the video and predict: the knob is just past the middle. Which LEDs are on?",
  "Videoyu durdurun ve tahmin edin: düğme ortanın biraz ilerisinde. Hangi LED'ler yanıyor?",
  "Videoyu durdurun ve tahmin edin: düğme ortanın biraz ilerisinde. Hangi ledler yanıyor?", pad=3.0)
s("s37", "tourbar", "Green and yellow. Just past the middle is level two.",
  "Yeşil ve sarı. Ortanın biraz ilerisi seviye ikidir.")
s("s38", "runbar", "Here it is for real. Turn slowly, and the bar fills one light at a time, then empties again.",
  "İşte gerçeği. Yavaşça çevirin; çubuk her seferinde bir ışık doluyor, sonra yeniden boşalıyor.", clip="C3", pad=3.0)
# ---- common mistake
s("s39", "mistake", "Now a mistake you might make. Green and red light up, but yellow stays dark. Quick question: is it the code, or the wiring?",
  "Şimdi sizin de yapabileceğiniz bir hata. Yeşil ve kırmızı yanıyor ama sarı karanlık kalıyor. Kısa bir soru: kod mu, bağlantı mı?",
  clip="C4", pad=THINK)
s("s40", "mistake", "Take the temperature first. The Serial Monitor says level three, so the code wants yellow on. The problem is on the wiring side.",
  "Önce ateşi ölçün. Seri Monitör seviye üç diyor; yani kod sarının yanmasını istiyor. Sorun bağlantı tarafında.")
s("s41", "mistake", "The yellow LED is in backwards. An LED lets current through only one way, from the long leg to the short leg.",
  "Sarı LED ters takılmış. LED akımı yalnızca tek yönde geçirir: uzun bacaktan kısa bacağa.",
  "Sarı led ters takılmış. Led akımı yalnızca tek yönde geçirir: uzun bacaktan kısa bacağa.")
s("s42", "mistake", "Turned around, it simply stays dark, and nothing is damaged. Flip it, and the bar is complete.",
  "Ters takılınca yalnızca karanlık kalır ve hiçbir şey zarar görmez. Çevirin, çubuk tamamlansın.")
# ---- explain in your own words
s("s43", "explain", "Now pause the video, and explain in your own words why the first level line almost never lit all three LEDs. One sentence is enough.",
  "Şimdi videoyu durdurun ve ilk seviye satırının neden üç LED'i neredeyse hiç birden yakmadığını kendi cümlenizle açıklayın. Tek cümle yeter.",
  "Şimdi videoyu durdurun ve ilk seviye satırının neden üç ledi neredeyse hiç birden yakmadığını kendi cümlenizle açıklayın. Tek cümle yeter.", pad=4.0)
s("s44", "explain", "One way to say it: map rounds down, so the top level only came at the very end of the ruler, and the ruler rarely gets there.",
  "Şöyle söylenebilir: map aşağı yuvarlar; bu yüzden en üst seviye yalnızca cetvelin en sonunda geliyordu, cetvel de oraya nadiren ulaşıyor.",
  "Şöyle söylenebilir: mep aşağı yuvarlar; bu yüzden en üst seviye yalnızca cetvelin en sonunda geliyordu, cetvel de oraya nadiren ulaşıyor.",
  sub="One way to say it: map() rounds down, so the top level only came at the very end of the ruler, and the ruler rarely gets there.")
# ---- your turn (not a mini-project: the solution stays in the lesson folder)
s("s45", "challenge", "Your turn: the Rotary Safe Lock. Map the knob onto zero to ninety-nine, and print the number, so the knob becomes the dial of a safe.",
  "Sıra sizde: döner kasa kilidi. Düğmeyi sıfırdan 99'a eşleyin ve sayıyı yazdırın; böylece düğme bir kasanın çarkı olur.",
  "Sıra sizde: döner kasa kilidi. Düğmeyi sıfırdan doksan dokuza eşleyin ve sayıyı yazdırın; böylece düğme bir kasanın çarkı olur.",
  sub="Your turn: the Rotary Safe Lock. Map the knob onto 0 to 99, and print the number, so the knob becomes the dial of a safe.")
s("s46", "challenge", "The secret code is three numbers in a row, and you press the button after each one. The numbers are on the screen.",
  "Gizli şifre art arda üç sayı; her birinden sonra butona basıyorsunuz. Sayılar ekranda.")
s("s47", "challenge", "Get all three right, and the color LED from episode six turns green. One wrong press flashes red, and you start again from the first number.",
  "Üçünü de doğru girerseniz altıncı bölümdeki üç renkli LED yeşil yanar. Tek bir yanlış basış kırmızı yakıp söndürür ve ilk sayıdan yeniden başlarsınız.",
  "Üçünü de doğru girerseniz altıncı bölümdeki üç renkli led yeşil yanar. Tek bir yanlış basış kırmızı yakıp söndürür ve ilk sayıdan yeniden başlarsınız.")
s("s48", "challenge", "The twist: a knob is never exact, so accept a few numbers on either side of each target. You'll need and, written as two ampersands, which means both checks must be true.",
  "İşin püf noktası: düğme hiçbir zaman tam değildir; bu yüzden her hedefin iki yanındaki birkaç sayıyı da kabul edin. Bunun için 've' gerekecek; iki tane ve işaretiyle yazılır ve iki kontrolün de doğru olması demektir.")
s("s49", "challenge", "One hint: a single variable called step can remember how many numbers are already right.",
  "Bir ipucu: step adında tek bir değişken, kaç sayının doğru girildiğini hatırlayabilir.",
  "Bir ipucu: step adında tek bir değişken, kaç sayının doğru girildiğini hatırlayabilir.")
# ---- outro
s("s50", "outro", "Today you learned three things. Map turns a number from one range into another. It always rounds down, so plan your ranges. And an LED in backwards simply stays dark.",
  "Bugün üç şey öğrendiniz. map bir sayıyı bir aralıktan başka bir aralığa çevirir. Her zaman aşağı yuvarlar; aralıklarınızı ona göre seçin. Ters takılan bir LED de yalnızca karanlık kalır.",
  "Bugün üç şey öğrendiniz. Mep bir sayıyı bir aralıktan başka bir aralığa çevirir. Her zaman aşağı yuvarlar; aralıklarınızı ona göre seçin. Ters takılan bir led de yalnızca karanlık kalır.",
  sub="Today you learned three things. map() turns a number from one range into another. It always rounds down, so plan your ranges. And an LED in backwards simply stays dark.")
s("s51", "outro", "Next time is our first mini project: a pedestrian crossing, with car lights, a walk light, a button and today's knob. Post your safe lock code in the comments; one solution is in the lesson folder. See you there!",
  "Gelecek sefer ilk mini projemiz var: araba ışıkları, yaya ışığı, bir buton ve bugünkü düğmeyle bir yaya geçidi. Kasa kilidi kodunuzu yorumlara yazın; bir çözüm ders klasöründe. Görüşmek üzere!")

# breathing room before a new term (lesson_lint NEWTERM: >= 0.8 s of silence before it)
NEW_TERM = ("s03", "s07", "s09", "s10", "s13", "s16", "s22", "s28", "s33", "s34", "s39", "s45")
for a, b in zip(S, S[1:]):
    if b["id"] in NEW_TERM:
        a["pad"] = a.get("pad", 0) + 0.4

dub = {d["id"]: d.pop("dub") for d in S}
script = {
    "episode": 8, "title": "map(), Dimmer Knobs and Level Bars", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": "s02",
    "music": "results",
    "clips": {
        "C0": "OPENING: level_bar, hand turns the knob, green -> yellow -> red fill (footage/gelen/ep06/20261029_175029).",
        "C1": "WIRING: yellow and green LEDs placed, knob moved to the top of the right board (20261029_175125).",
        "C2": "MAP_DIMMER: red LED dims and brightens with the knob, yellow/green off (20261029_175720).",
        "C3": "LEVEL_BAR RUN: same as C0, cropped closer (20261029_180038).",
        "C4": "MISTAKE: yellow LED reversed, stays dark while red and green light (20261029_180136).",
    },
    "segments": S,
}
here = Path(__file__).parent
(here / "script.json").write_text(json.dumps(script, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "dub").mkdir(exist_ok=True)
(here / "dub" / "tr.json").write_text(json.dumps({
    "voice": "tr-TR-EmelNeural", "rate": "+0%",
    "note": "Spoken text only. English terms are written the way a Turkish speaker says them (mep, analog rid, levıl bar, lup...).",
    "segments": dub}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "segments,", sum(len(x["text"].split()) for x in S), "words")
