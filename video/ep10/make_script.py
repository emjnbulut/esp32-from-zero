"""Source of video/ep10/script.json (and dub/tr.json). Usage: python video/ep10/make_script.py

Episode 10 "Mini Project 1: a Reflex Game with a Record that Survives Power Off" (curriculum v6), rules:
PRODUCTION_GUIDELINES.md sections 9, 10, 11. Same circuit and the same state/goTo pattern as episode 9.
New syntax/idea: Preferences (#include <Preferences.h>, prefs.begin(), prefs.getULong() with a default, prefs.putULong()):
a value that survives unplugging the board. Practice (known pieces, no new logic): reaction time = time in the green step
(now - stateStart), a one-moment `pressed` flag, if / else if colour thresholds with setColor().
Analogies (video/ANALOGIES.md): NEW notebook in a drawer (Preferences; ordinary variables = boxes on a desk that is cleared
when the power goes). Reused: washing machine (state), parking ticket (time since a moment), wall clock (millis),
coffee machine button (helper), labeled box (variable), ruler + city map (knob -> wait time).
Retrieval minute on episodes 9 and 6 (+ series-entry card, section 11). PRIMM for reflex_game: predict how to measure the
reaction, short tour (support fades from episode 10: "pause and write step 2 yourself", more predictions), run C0/C1,
predict the record after a power cut, modify 250 -> 200. Common mistake: saving every result without the if (a slow round
erases the record; animation only). One "in your own words". Your turn = Project 1 homework with a solution Short:
false start (challenge_false_start in the lesson folder).
Section 9 (7 Nov): at most 1-2 spoken numbers per sentence; exact values stay on screen.

Clips (creator, shoot pack p07-2): C0 opening: start, red -> yellow -> green, quick press, RGB green.
C1 slow press ~1 s after green, RGB red. C2 USB cable unplugged and plugged back in (close-up).
TR dub: lines start with native words; "skeç"; map -> "mep"; loop -> "lup"; millis -> "milis"; state -> "steyt";
goTo -> "go tu"; Preferences -> "Prefırınsız"; the RGB LED is "üç renkli LED"; knob = "düğme", push button = "buton".
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
s("s01", "cold", "Red, yellow, and green! I press as fast as I can, and the color LED turns green: that was a fast one.",
  "Kırmızı, sarı ve yeşil! Olabildiğince hızlı basıyorum ve üç renkli LED yeşile dönüyor: bu hızlı bir tepkiydi.",
  "Kırmızı, sarı ve yeşil! Olabildiğince hızlı basıyorum ve üç renkli led yeşile dönüyor: bu hızlı bir tepkiydi.", clip="C0")
s("s02", "cold", "Today you'll build this reflex game, on the same circuit. And your best time stays saved, even when you unplug the board.",
  "Bugün aynı devrede bu refleks oyununu kuracaksınız. Üstelik en iyi süreniz kartı fişten çekseniz bile kayıtlı kalıyor.")
# ---- retrieval minute (episodes 9 and 6) + series-entry card
s("s03", "retrieval", "New here? Episode one is on the screen. Now, two questions from earlier episodes.",
  "Yeni misiniz? Birinci bölüm ekranda. Şimdi önceki bölümlerden iki soru.")
s("s04", "retrieval", "Quick question: in the crossing, the helper go to always did two jobs. Which two?",
  "Kısa bir soru: geçitte goTo yardımcısı her zaman iki iş yapıyordu. Hangi ikisi?",
  "Kısa bir soru: geçitte go tu yardımcısı her zaman iki iş yapıyordu. Hangi ikisi?",
  sub="Quick question: in the crossing, the helper goTo() always did two jobs. Which two?", pad=THINK)
s("s05", "retrieval", "It put the new step number into state, and it wrote down the time. Without the time, the new step thinks it's already over.",
  "Yeni adım numarasını state'e koyuyordu ve saati not ediyordu. Saat olmadan yeni adım, süresinin çoktan bittiğini sanıyor.",
  "Yeni adım numarasını steyte koyuyordu ve saati not ediyordu. Saat olmadan yeni adım, süresinin çoktan bittiğini sanıyor.")
s("s06", "retrieval", "Quick question: how do you make orange with the color LED?",
  "Kısa bir soru: üç renkli LED ile turuncuyu nasıl elde edersiniz?",
  "Kısa bir soru: üç renkli led ile turuncuyu nasıl elde edersiniz?", pad=THINK)
s("s07", "retrieval", "Red fully on, just a little green, and blue off. Light adds up, so red with a touch of green looks orange.",
  "Kırmızı tam açık, yeşil çok az, mavi kapalı. Işık toplanır; kırmızıya biraz yeşil katınca turuncu görünür.")
# ---- the game and the parts
s("s08", "plan", "Here are the rules. Press the button to start. The red light comes on, then the yellow, and then green. The moment you see green, press.",
  "Kurallar şöyle. Başlamak için butona basın. Önce kırmızı yanar, sonra sarı, sonra yeşil. Yeşili gördüğünüz an basın.")
s("s09", "plan", "The color LED shows how you did: green for fast, yellow for okay, and red for slow. And the knob sets how long the yellow waits, so you can't just count.",
  "Üç renkli LED nasıl yaptığınızı gösterir: hızlıysa yeşil, idare ederse sarı, yavaşsa kırmızı. Düğme de sarının ne kadar bekleyeceğini ayarlar; böylece sayarak tahmin edemezsiniz.",
  "Üç renkli led nasıl yaptığınızı gösterir: hızlıysa yeşil, idare ederse sarı, yavaşsa kırmızı. Düğme de sarının ne kadar bekleyeceğini ayarlar; böylece sayarak tahmin edemezsiniz.")
s("s10", "plan", "And again, not a single new wire. It's exactly the circuit from the crossing.",
  "Ve yine tek bir yeni kablo yok. Devre, geçitteki devrenin aynısı.")
# ---- the idea: same washing machine, five steps
s("s11", "idea", "The game is our washing machine again, this time with five steps: waiting for a start, red, yellow, green, and showing the result.",
  "Oyun yine bizim çamaşır makinemiz; bu sefer beş adımlı: başlamayı bekleme, kırmızı, sarı, yeşil ve sonucu gösterme.")
s("s12", "idea", "Pause the video and predict: how can the board measure your reaction time? You already know the trick.",
  "Videoyu durdurun ve tahmin edin: kart tepki sürenizi nasıl ölçebilir? Hileyi zaten biliyorsunuz.", pad=3.0)
s("s13", "idea", "It's the parking ticket. When green comes on, go to writes down the time. When you press, now minus that moment is your reaction.",
  "Otopark bileti. Yeşil yanınca goTo saati not ediyor. Bastığınızda şimdiki zaman eksi o an, sizin tepki süreniz.",
  "Otopark bileti. Yeşil yanınca go tu saati not ediyor. Bastığınızda şimdiki zaman eksi o an, sizin tepki süreniz.")
s("s14", "idea", "So the time you spent in the green step is your reaction time. No new code needed for that.",
  "Yani yeşil adımda geçirdiğiniz süre, sizin tepki süreniz. Bunun için yeni bir koda gerek yok.")
# ---- code tour: reflex_game (top, helpers, the button)
s("s15", "tour", "Here's the sketch, reflex game. At the top, the same pins and the same state and start time as the crossing, plus a variable called best for the record.",
  "İşte skeç: reflex_game. En üstte aynı pinler, geçitteki aynı state ve başlangıç zamanı; bir de rekor için best adlı bir değişken.",
  "İşte, skeç: refleks geym. En üstte aynı pinler, geçitteki aynı steyt ve başlangıç zamanı; bir de rekor için best adlı bir değişken.",
  sub="Here's the sketch, reflex_game. At the top, the same pins and the same state and start time as the crossing, plus a variable called best for the record.")
s("s16", "tour", "The helpers are old friends too: set color for the result light, lights for the three LEDs, and go to for moving on.",
  "Yardımcılar da eski dostlar: sonuç ışığı için setColor, üç LED için lights ve ilerlemek için goTo.",
  "Yardımcılar da eski dostlar: sonuç ışığı için set kalır, üç led için layts ve ilerlemek için go tu.",
  sub="The helpers are old friends too: setColor() for the result light, lights() for the three LEDs, and goTo() for moving on.")
s("s17", "tour", "Part one is the button. One new detail: a true or false variable called pressed. It's true only in the one loop round where a new press happens.",
  "Birinci kısım buton. Tek yeni ayrıntı: pressed adlı, doğru ya da yanlış tutan bir değişken. Yalnızca yeni bir basışın olduğu o tek turda doğru oluyor.",
  "Birinci kısım buton. Tek yeni ayrıntı: prest adlı, doğru ya da yanlış tutan bir değişken. Yalnızca yeni bir basışın olduğu o tek turda doğru oluyor.",
  sub="Part one is the button. One new detail: a true or false variable called pressed. It's true only in the one loop round where a new press happens.")
s("s18", "tour", "Pause and predict: you hold the button down for a whole second. In how many rounds is pressed true?",
  "Durdurun ve tahmin edin: butonu tam bir saniye basılı tutuyorsunuz. pressed kaç turda doğru olur?",
  "Durdurun ve tahmin edin: butonu tam bir saniye basılı tutuyorsunuz. Prest kaç turda doğru olur?", pad=3.0)
s("s19", "tour", "Just one. Holding doesn't count again, so every step can simply ask: was there a press just now?",
  "Yalnızca birinde. Basılı tutmak yeniden sayılmaz; böylece her adım kısaca şunu sorabilir: az önce basıldı mı?")
# ---- the steps
s("s20", "steps", "Step zero waits for that press. Then red comes on, and we go to step one.",
  "Sıfırıncı adım o basışı bekliyor. Sonra kırmızı yanıyor ve birinci adıma geçiyoruz.")
s("s21", "steps", "Step one keeps the red for one second. Then yellow comes on, and map turns the knob into the yellow time, from one to four seconds.",
  "Birinci adım kırmızıyı bir saniye tutuyor. Sonra sarı yanıyor ve map, düğmeyi sarının süresine çeviriyor: bir ile dört saniye arası.",
  "Birinci adım kırmızıyı bir saniye tutuyor. Sonra sarı yanıyor ve mep, düğmeyi sarının süresine çeviriyor: bir ile dört saniye arası.",
  sub="Step one keeps the red for one second. Then yellow comes on, and map() turns the knob into the yellow time, from one to four seconds.")
s("s22", "steps", "Now pause the video and try it yourself: write step two. When the yellow time is up, green comes on, and we go to step three.",
  "Şimdi videoyu durdurun ve kendiniz deneyin: ikinci adımı yazın. Sarının süresi dolunca yeşil yanıyor ve üçüncü adıma geçiyoruz.", pad=4.0)
s("s23", "steps", "Here's one way. It looks just like the crossing: one check of the time, the lights, and go to.",
  "İşte bir yolu. Tıpkı geçitteki gibi: zamana tek bir bakış, ışıklar ve goTo.",
  "İşte bir yolu. Tıpkı geçitteki gibi: zamana tek bir bakış, ışıklar ve go tu.")
s("s24", "step3", "Step three is the heart of the game. When pressed comes, the time in this step is the reaction, and the Serial Monitor prints it.",
  "Üçüncü adım oyunun kalbi. pressed geldiğinde bu adımdaki süre tepki süresidir ve Seri Monitör onu yazar.",
  "Üçüncü adım oyunun kalbi. Prest geldiğinde bu adımdaki süre tepki süresidir ve Seri Monitör onu yazar.")
s("s25", "step3", "Then if and else if pick the color: under a quarter second is green, under half a second is yellow, and anything slower is red.",
  "Sonra if ve else if rengi seçiyor: çeyrek saniyenin altı yeşil, yarım saniyenin altı sarı, daha yavaşı kırmızı.",
  "Sonra if ve els if rengi seçiyor: çeyrek saniyenin altı yeşil, yarım saniyenin altı sarı, daha yavaşı kırmızı.")
s("s26", "step3", "Step four shows that color for three seconds, then goes back to step zero for the next round.",
  "Dördüncü adım o rengi üç saniye gösteriyor, sonra bir sonraki tur için sıfırıncı adıma dönüyor.")
s("s27", "run", "Here it is for real. Watch the lights, and the color at the end.",
  "İşte gerçeği. Işıkları ve sondaki rengi izleyin.", clip="C0", pad=3.0)
s("s28", "run", "And now a slow press, about a second after green. The color LED says red.",
  "Şimdi de yavaş bir basış; yeşilden yaklaşık bir saniye sonra. Üç renkli LED kırmızı diyor.",
  "Şimdi de yavaş bir basış; yeşilden yaklaşık bir saniye sonra. Üç renkli led kırmızı diyor.", clip="C1", pad=2.0)
s("s29", "modify", "Change one number. Pause and predict: if two hundred fifty becomes two hundred, what happens to your green results?",
  "Tek bir sayıyı değiştirin. Durdurun ve tahmin edin: iki yüz elli, iki yüz olursa yeşil sonuçlarınıza ne olur?",
  sub="Change one number. Pause and predict: if 250 becomes 200, what happens to your green results?", pad=3.0)
s("s30", "modify", "Green gets harder to earn. Only really fast presses count now, and more of your rounds end yellow.",
  "Yeşil almak zorlaşır. Artık yalnızca gerçekten hızlı basışlar sayılır; turlarınızın çoğu sarıyla biter.")
# ---- the record: why it disappears, and Preferences
s("s31", "lost", "Now the record. Pause and predict: you set a great time, then unplug the board and plug it back in. Is the record still there?",
  "Şimdi rekor. Durdurun ve tahmin edin: harika bir süre yaptınız, sonra kartı fişten çekip geri taktınız. Rekor hâlâ orada mı?", pad=3.0)
s("s32", "lost", "With an ordinary variable, no. Every variable lives in memory that's wiped when the power goes. After a restart, best starts over.",
  "Sıradan bir değişkenle hayır. Her değişken, elektrik gidince silinen bir bellekte yaşar. Yeniden başlayınca best en baştan başlar.")
s("s33", "drawer", "Think of your desk. Variables are labeled boxes on the desk, and a power cut clears the whole desk. But a notebook in the drawer stays.",
  "Masanızı düşünün. Değişkenler masanın üstündeki etiketli kutular; elektrik kesilince bütün masa temizleniyor. Ama çekmecedeki defter yerinde kalıyor.")
s("s34", "drawer", "What actually happens: the ESP32 keeps a small corner of its flash memory, the same memory that holds your program. A library called Preferences lets you write numbers there.",
  "Gerçekte olan şu: ESP32, flash belleğinin küçük bir köşesini ayırıyor; programınızı tutan belleğin ta kendisi. Preferences adlı bir kütüphane oraya sayı yazmanızı sağlıyor.",
  "Gerçekte olan şu: ESP otuz iki, flaş belleğinin küçük bir köşesini ayırıyor; programınızı tutan belleğin ta kendisi. Prefırınsız adlı bir kütüphane oraya sayı yazmanızı sağlıyor.")
s("s35", "drawer", "The difference from a real notebook: this drawer is small, and every write wears it a little. So we write only when something worth keeping happens.",
  "Gerçek defterden farkı şu: bu çekmece küçük ve her yazış onu biraz yıpratıyor. Bu yüzden yalnızca saklamaya değer bir şey olduğunda yazıyoruz.")
s("s36", "prefs", "In the sketch, three lines. In setup, begin opens a drawer we call reflex.",
  "Skeçte üç satır var. setup'ta begin, adını reflex koyduğumuz bir çekmeceyi açıyor.",
  "Skeçte üç satır var. Setapta bigin, adını refleks koyduğumuz bir çekmeceyi açıyor.",
  sub="In the sketch, three lines. In setup(), begin() opens a drawer we call reflex.")
s("s37", "prefs", "Then get reads the page called best. If the page is still empty, it gives back the number in the second slot, here nine nine nine nine.",
  "Sonra get, best adlı sayfayı okuyor. Sayfa daha boşsa ikinci yerdeki sayıyı veriyor; burada dokuz bin dokuz yüz doksan dokuz.",
  sub="Then getULong() reads the page called best. If the page is still empty, it gives back the number in the second slot, here 9999.")
s("s38", "prefs", "Quick question: why such a big number as the starting record?",
  "Kısa bir soru: başlangıç rekoru neden bu kadar büyük bir sayı?", pad=THINK)
s("s39", "prefs", "Because any real reaction is smaller. So your very first round always becomes the record.",
  "Çünkü gerçek bir tepki her zaman ondan küçüktür. Böylece ilk turunuz her zaman rekor olur.")
s("s40", "prefs", "And in step three: if the reaction beats best, we put the new record into best, and put writes it into the drawer.",
  "Üçüncü adımda da: tepki best'ten iyiyse yeni rekoru best'e koyuyoruz ve put onu çekmeceye yazıyor.",
  "Üçüncü adımda da: tepki bestten iyiyse yeni rekoru beste koyuyoruz ve put onu çekmeceye yazıyor.",
  sub="And in step three: if the reaction beats best, we put the new record into best, and putULong() writes it into the drawer.")
s("s41", "unplug", "Here's the test. Unplug the cable, wait a moment, plug it back in.",
  "İşte deneme. Kabloyu çekin, biraz bekleyin, geri takın.", clip="C2", pad=1.0)
s("s42", "unplug", "The Serial Monitor starts again, and the first line shows the old record. The drawer kept it.",
  "Seri Monitör yeniden başlıyor ve ilk satır eski rekoru gösteriyor. Çekmece onu saklamış.")
# ---- common mistake (animation)
s("s43", "mistake", "Now a mistake you might make. Someone wants to save the result, so they write put after every round, without the if.",
  "Şimdi sizin de yapabileceğiniz bir hata. Biri sonucu kaydetmek istiyor ve if'i atlayıp her turdan sonra put yazıyor.")
s("s44", "mistake", "Quick question: what happens to a great record after one slow round?",
  "Kısa bir soru: tek bir yavaş turdan sonra harika bir rekora ne olur?", pad=THINK)
s("s45", "mistake", "It's gone. The slow time is written over it. The if is what makes it a record: only a better time goes into the drawer.",
  "Gider. Yavaş süre onun üzerine yazılır. Onu rekor yapan if'tir: çekmeceye yalnızca daha iyi bir süre girer.")
# ---- explain in your own words
s("s46", "explain", "Pause the video, and explain in your own words why best alone forgets the record, but the drawer keeps it. One sentence is enough.",
  "Videoyu durdurun ve best'in tek başına rekoru neden unuttuğunu ama çekmecenin neden sakladığını kendi cümlenizle açıklayın. Tek cümle yeter.",
  "Videoyu durdurun ve bestin tek başına rekoru neden unuttuğunu ama çekmecenin neden sakladığını kendi cümlenizle açıklayın. Tek cümle yeter.", pad=4.0)
s("s47", "explain", "One way to say it: variables live in memory that needs power. The drawer is flash memory, which keeps its contents without power.",
  "Şöyle söylenebilir: değişkenler elektriğe muhtaç bir bellekte yaşar. Çekmece ise flash bellek; elektrik olmadan da içindekini saklar.",
  "Şöyle söylenebilir: değişkenler elektriğe muhtaç bir bellekte yaşar. Çekmece ise flaş bellek; elektrik olmadan da içindekini saklar.")
# ---- your turn: the project homework (solution Short)
s("s48", "yourturn", "Pause and predict: what does the game do now if you press during the yellow?",
  "Durdurun ve tahmin edin: sarı yanarken basarsanız oyun şu an ne yapar?", pad=3.0)
s("s49", "yourturn", "Nothing at all. So a cheater can tap the button again and again, and catch the green by luck.",
  "Hiçbir şey. Yani hile yapan biri butona durmadan basıp yeşili şansla yakalayabilir.")
s("s50", "yourturn", "Your turn, the project homework: a false start. A press during red or yellow flashes the color LED red, and no time counts.",
  "Sıra sizde, projenin ödevi: erken başlama. Kırmızı ya da sarı yanarken basılırsa üç renkli LED kırmızı yanıp söner ve süre sayılmaz.",
  "Sıra sizde, projenin ödevi: erken başlama. Kırmızı ya da sarı yanarken basılırsa üç renkli led kırmızı yanıp söner ve süre sayılmaz.")
s("s51", "yourturn", "You need one more step number and one more check. The solution is in the lesson folder, and I'll show it in a Short.",
  "Bir adım numarası ve bir kontrol daha lazım. Çözüm ders klasöründe; bir Short'ta da göstereceğim.",
  "Bir adım numarası ve bir kontrol daha lazım. Çözüm ders klasöründe; bir şortta da göstereceğim.")
# ---- outro
s("s52", "outro", "Today you finished your first project. A game built from steps. A reaction time that's just the time in one step. And a record kept in the drawer.",
  "Bugün ilk projenizi bitirdiniz. Adımlardan kurulmuş bir oyun. Tek bir adımdaki süreden ibaret bir tepki süresi. Ve çekmecede saklanan bir rekor.")
s("s53", "outro", "Next time, a recap of everything since episode five, with a quiz. Tell me your best reaction time in the comments. See you there!",
  "Gelecek sefer beşinci bölümden bu yana her şeyin bir tekrarı var, içinde bir de quiz. En iyi tepki sürenizi yorumlarda yazın. Görüşmek üzere!",
  "Gelecek sefer beşinci bölümden bu yana her şeyin bir tekrarı var, içinde bir de kuiz. En iyi tepki sürenizi yorumlarda yazın. Görüşmek üzere!")

# breathing room before a new term (lesson_lint NEWTERM: >= 0.8 s of silence before it)
NEW_TERM = ("s03", "s08", "s11", "s15", "s17", "s25", "s31", "s33", "s34", "s36", "s43", "s48")
for a, b in zip(S, S[1:]):
    if b["id"] in NEW_TERM:
        a["pad"] = a.get("pad", 0) + 0.4

dub = {d["id"]: d.pop("dub") for d in S}
script = {
    "episode": 10, "title": "Mini Project 1: a Reflex Game with a Record that Survives Power Off", "voice": "en-US-EricNeural", "rate": "+5%",
    "lead_in": 0.8,
    "sting_after": "s02",
    "music": "results",
    "clips": {
        "C0": "OPENING + RUN: reflex_game, start press, red -> yellow -> GREEN, quick press, RGB turns green.",
        "C1": "SLOW: same game, press ~1 s after green, RGB turns red.",
        "C2": "UNPLUG: USB cable pulled out and plugged back in after ~2 s (close-up of plug and board).",
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
