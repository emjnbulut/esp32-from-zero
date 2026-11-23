"""Source of video/ep10/script.json (and dub/tr.json). Usage: python video/ep10/make_script.py

Episode 10 v2 (21 Nov 2026, creator's new direction): "I Built a Reflex Game That Remembers Your Record (ESP32 + OLED)".
New parts: 0.96" I2C OLED (SDA 21 / SCL 22), passive buzzer (GPIO 32); button moves to GPIO 19.
New ideas, kept light: I2C = two shared wires; the screen draws in memory and shows it with display(); tone();
random(); Preferences (getULong / putULong) keeps the record without power. Sketch: lessons/10-reflex-oled.
Rules: PRODUCTION_GUIDELINES section 9 (human, everyday pictures, 1-2 spoken numbers per sentence), section 12
(result first, standalone), creator 21 Nov: at least HALF the runtime on the Blender 3D model (vis "b3d:*"),
Motion Canvas (vis "mc:*") only for the few code lines and abstract ideas; fast tempo, not drowning in code.
Analogies (video/ANALOGIES.md): NEW group chat on two wires (I2C), NEW whiteboard behind a curtain (screen buffer +
display()), NEW notebook in a drawer (Preferences: RAM = sticky notes on a desk that get swept off at power-off).
Reused: washing machine (state), wall clock (millis), labelled box (variable).
Segment keys: id, vis, text (EN narration), tr (TR subtitle), dub (TR spoken, if different), sub (EN subtitle if
different), pad (silence after, s).
"""
import json
from pathlib import Path

S = []
THINK = 2.4


def s(id, vis, text, tr, dub=None, sub=None, **kw):
    d = {"id": id, "vis": vis, "text": text}
    if sub:
        d["sub"] = sub
    d["tr"] = tr
    d["dub"] = dub or tr
    d.update(kw)
    S.append(d)


# ---------------- A. cold open: the finished game (3D)
s("s01", "b3d:open_play", "Wait for it... GO! Two hundred and fourteen milliseconds. A new record.",
  "Bekle... BAŞLA! İki yüz on dört milisaniye. Yeni rekor.", pad=0.3)
s("s02", "b3d:open_unplug", "Now watch this. I pull the cable. The screen goes dark, the board is completely off.",
  "Şimdi şuna bakın. Kabloyu çekiyorum. Ekran kararıyor, kart tamamen kapandı.")
s("s03", "b3d:open_replug", "I plug it back in... and the record is still there. The board remembered it, with no power at all.",
  "Geri takıyorum... ve rekor hâlâ orada. Kart, hiç elektrik yokken bile onu hatırladı.", pad=0.3)
s("s04", "b3d:open_orbit", "Today we build this game from scratch: a real screen, a real beep, and a record that never forgets. "
  "You only need the starter kit and about twenty minutes.",
  "Bugün bu oyunu sıfırdan kuruyoruz: gerçek bir ekran, gerçek bir bip sesi ve hiç unutmayan bir rekor. "
  "Sadece başlangıç setine ve yirmi dakika kadar zamana ihtiyacınız var.")

# ---------------- B. the two new parts (3D close-ups)
s("s05", "b3d:oled_hero", "Meet the first new part: a tiny screen, under one inch wide.",
  "İlk yeni parçayla tanışın: bir parmak boğumundan küçük bir ekran.")
s("s06", "b3d:oled_macro", "It has eight thousand little dots, and every dot makes its own light. "
  "That's why black on this screen is truly black: those dots are simply off.",
  "Üzerinde sekiz bine yakın küçük nokta var ve her nokta kendi ışığını üretiyor. "
  "Bu yüzden bu ekranda siyah gerçekten siyah: o noktalar sadece kapalı.")
s("s07", "b3d:oled_pins", "And it needs only four wires. Two are power. The other two carry all the pictures.",
  "Üstelik yalnızca dört kabloya ihtiyacı var. İkisi güç. Diğer ikisi bütün görüntüyü taşıyor.")
s("s08", "mc:i2c_chat", "Those two wires work like a group chat. One wire carries the message, bit by bit. "
  "The other one is the beat, so both sides read each bit at the same moment.",
  "Bu iki kablo bir grup sohbeti gibi çalışır. Kablolardan biri mesajı parça parça taşır. "
  "Diğeri ritim tutar, böylece iki taraf da her parçayı aynı anda okur.")
s("s09", "mc:i2c_chat", "Every device in the chat has its own name, a short address. Our screen answers to its address, "
  "so later we can add more parts on the very same two wires.",
  "Sohbetteki her cihazın kendi adı, yani kısa bir adresi vardır. Ekranımız kendi adresine cevap verir, "
  "böylece ileride aynı iki kabloya başka parçalar da ekleyebiliriz.")
s("s10", "b3d:buzzer_hero", "The second new part is this little buzzer. It's a passive one: it stays quiet until we give it a note.",
  "İkinci yeni parça bu küçük buzzer. Bu pasif bir buzzer: biz ona bir nota verene kadar sessiz kalır.")
s("s11", "b3d:buzzer_cut", "Inside, a thin metal disk bends back and forth. Fast bends make a high beep, slow bends a low buzz.",
  "İçinde ince bir metal disk ileri geri esner. Hızlı esnerse ince bir bip, yavaş esnerse kalın bir vızıltı duyarız.")
s("s12", "b3d:button_hero", "And our old friend, the push button, joins in. It just moves to a new pin, because the screen needs its old one.",
  "Bir de eski dostumuz buton aramıza katılıyor. Sadece yeni bir pine taşınıyor, çünkü eski pinine artık ekran ihtiyaç duyuyor.")

# ---------------- C. wiring, step by step (3D build, coordinates on screen)
s("s13", "b3d:wire_overview", "Let's wire it. Every hole has a printed number and letter, and you'll see them on the screen, so you can copy each step.",
  "Hadi bağlayalım. Her deliğin üzerinde basılı bir numara ve harf var, hepsini ekranda göreceksiniz; her adımı birebir kopyalayabilirsiniz.")
s("s14", "b3d:wire_power", "First, power. A red wire takes three point three volts to the plus line at the back, "
  "and a black wire takes ground to the minus line.",
  "Önce güç. Kırmızı kablo üç virgül üç voltu arkadaki artı hattına, siyah kablo da toprağı eksi hattına götürüyor.")
s("s15", "b3d:wire_oled", "Now the screen. Its four legs go into one column, side by side. Then two short wires give it power from those lines.",
  "Şimdi ekran. Dört bacağı yan yana aynı sütuna giriyor. Sonra iki kısa kablo ona bu hatlardan güç veriyor.")
s("s16", "b3d:wire_i2c", "The two chat wires: green from pin twenty-two to the clock leg, and blue from pin twenty-one to the data leg.",
  "İki sohbet kablosu: yeşil kablo yirmi iki numaralı pinden saat bacağına, mavi kablo da yirmi bir numaralı pinden veri bacağına.")
s("s17", "b3d:wire_button", "The button sits across the middle gap. Yellow goes from pin nineteen to one side, "
  "and the other side goes to ground.",
  "Buton ortadaki boşluğun üzerine oturuyor. Sarı kablo on dokuz numaralı pinden bir tarafına gidiyor, diğer taraf da toprağa.")
s("s18", "b3d:wire_buzzer", "Last, the buzzer on the front board. Orange from pin thirty-two to its plus leg, and its other leg to ground.",
  "Son olarak öndeki breadboarda buzzer. Turuncu kablo otuz iki numaralı pinden artı bacağına, diğer bacağı da toprağa.")
s("s19", "b3d:wire_done", "That's the whole circuit: one screen, one button, one buzzer. Pause here if you want to compare it with yours.",
  "Bütün devre bu kadar: bir ekran, bir buton, bir buzzer. Kendi devrenizle karşılaştırmak isterseniz burada durdurun.", pad=0.6)

# ---------------- D1. code: waking the screen (Motion Canvas)
s("s20", "mc:code_screen", "To talk to the screen we use a free library. You install it once, from the Library Manager.",
  "Ekranla konuşmak için ücretsiz bir kütüphane kullanıyoruz. Kütüphane Yöneticisi'nden bir kez kuruyorsunuz.")
s("s21", "mc:buffer", "Here's the trick of this screen. When we print, nothing appears yet. "
  "The board draws on a whiteboard behind a curtain.",
  "Bu ekranın bir püf noktası var. Yazdığımızda henüz hiçbir şey görünmez. Kart, perdenin arkasındaki bir beyaz tahtaya çizer.")
s("s22", "mc:buffer", "Only when we call display, the curtain opens and the whole picture shows at once. "
  "No flicker, no half-drawn words.",
  "Ancak display dediğimizde perde açılır ve bütün resim bir anda görünür. Titreme yok, yarım çizilmiş yazı yok.",
  "Ancak displey dediğimizde perde açılır ve bütün resim bir anda görünür. Titreme yok, yarım çizilmiş yazı yok.")
s("s23", "mc:code_show", "So we wrap it in one small helper called show. It clears the board, writes a small line on top, "
  "a big line in the middle, and opens the curtain.",
  "Bunu show adında küçük bir yardımcıya koyuyoruz. Tahtayı siliyor, üste küçük bir satır, ortaya büyük bir satır yazıyor ve perdeyi açıyor.",
  "Bunu şov adında küçük bir yardımcıya koyuyoruz. Tahtayı siliyor, üste küçük bir satır, ortaya büyük bir satır yazıyor ve perdeyi açıyor.")
s("s24", "b3d:screen_hello", "One call, and the screen says whatever we want.",
  "Tek bir çağrı ve ekran ne istersek onu yazıyor.")

# ---------------- D2. the game in four steps (Motion Canvas over 3D)
s("s25", "mc:steps", "The game itself has four steps, like a washing machine: ready, wait, go, and the result.",
  "Oyunun kendisi bir çamaşır makinesi gibi dört adımdan oluşuyor: hazır, bekle, başla ve sonuç.")
s("s26", "mc:steps", "When you press, we pick a random waiting time, somewhere between one and a half and four seconds, "
  "so nobody can guess the moment.",
  "Butona bastığınızda rastgele bir bekleme süresi seçiyoruz, bir buçuk ile dört saniye arasında bir yerde; "
  "böylece kimse o anı tahmin edemiyor.")
s("s27", "b3d:play_go", "When the time is up, the screen shows GO and the buzzer beeps. From that moment, the clock is running.",
  "Süre dolunca ekranda BAŞLA yazıyor ve buzzer ötüyor. O andan itibaren saat işliyor.")
s("s28", "mc:code_tone", "The beep is one line: tone, with the pin, how high the note is, and how long it lasts.",
  "Bip sesi tek satır: tone; içinde pin, notanın ne kadar ince olduğu ve ne kadar süreceği var.",
  "Bip sesi tek satır: ton; içinde pin, notanın ne kadar ince olduğu ve ne kadar süreceği var.")
s("s29", "b3d:play_press", "Your press stops the clock. The time since GO is your reaction, and it goes straight to the screen.",
  "Basışınız saati durduruyor. BAŞLA'dan beri geçen süre sizin tepki sürenizdir ve doğrudan ekrana gider.")
s("s30", "b3d:play_false", "And if you press too early? That's a false start. A low buzz, and you try again.",
  "Peki erken basarsanız? Bu bir hatalı çıkış. Kalın bir vızıltı ve yeniden deniyorsunuz.")
s("s31", "b3d:play_rounds", "Let's play a few rounds. Three hundred fifty... not bad. Two hundred eighty... better.",
  "Birkaç tur oynayalım. Üç yüz elli... fena değil. İki yüz seksen... daha iyi.")

# ---------------- E. the record that survives (Motion Canvas + 3D proof)
s("s32", "mc:prefs_ram", "Now the best part. Normally, every variable lives in memory that forgets everything when the power goes. "
  "Like sticky notes on a desk that get swept off every night.",
  "Şimdi en güzel kısım. Normalde her değişken, elektrik gidince her şeyi unutan bir bellekte yaşar. "
  "Her gece masadan süpürülen yapışkan notlar gibi.")
s("s33", "mc:prefs_drawer", "But the ESP32 also has a small drawer that keeps things without power. It's called Preferences.",
  "Ama ESP32'nin elektrik olmadan da bir şeyleri saklayan küçük bir çekmecesi var. Adı Preferences.",
  "Ama ESP otuz ikinin elektrik olmadan da bir şeyleri saklayan küçük bir çekmecesi var. Adı Preferıns.")
s("s34", "mc:prefs_put", "When you beat the record, one line puts the new time in the drawer, with a label: best.",
  "Rekoru kırdığınızda tek bir satır yeni süreyi çekmeceye koyuyor, üzerine de bir etiket: best.",
  "Rekoru kırdığınızda tek bir satır yeni süreyi çekmeceye koyuyor, üzerine de bir etiket: best.")
s("s35", "mc:prefs_get", "And when the board starts, one line takes it back out. If the drawer is still empty, "
  "we get a huge number instead, so the very first round is always a record.",
  "Kart açıldığında da tek bir satır onu geri çıkarıyor. Çekmece henüz boşsa onun yerine çok büyük bir sayı alıyoruz, "
  "böylece ilk tur her zaman rekor oluyor.")
s("s36", "b3d:prefs_proof", "Let's prove it. Two hundred and fourteen, new record. Unplug... plug back in... still two hundred and fourteen.",
  "Kanıtlayalım. İki yüz on dört, yeni rekor. Kabloyu çek... geri tak... hâlâ iki yüz on dört.")
s("s37", "mc:mistake", "One tip: save only when there's a new record. Saving every round would overwrite your best time with a slow one, "
  "and the drawer would wear out faster.",
  "Bir ipucu: sadece yeni rekor olduğunda kaydedin. Her turu kaydetmek, en iyi sürenizin üzerine yavaş bir süre yazar "
  "ve çekmece de daha çabuk yıpranır.")

# ---------------- F. your turn + next (3D)
s("s38", "b3d:challenge", "Your turn. Make the button erase the record when you hold it for three seconds on the ready screen. "
  "You already know how to measure a long press.",
  "Sıra sizde. Hazır ekranındayken butonu üç saniye basılı tutunca rekor silinsin. Uzun basışı ölçmeyi zaten biliyorsunuz.")
s("s39", "mc:code_full", "The full code and the solution are in the lesson folder, linked below. Post your best time in the comments.",
  "Tam kod ve çözüm, aşağıdaki bağlantıdaki ders klasöründe. En iyi sürenizi yorumlara yazın.")
s("s40", "b3d:outro", "Next time, the board gets eyes: a motion sensor that turns this setup into an alarm. "
  "Subscribe, so you don't miss it. See you there.",
  "Bir dahaki sefere kart göz sahibi oluyor: bu düzeneği bir alarma çeviren bir hareket sensörü. "
  "Kaçırmamak için abone olun. Orada görüşürüz.", pad=0.8)

SCRIPT = {
    "episode": "ep10",
    "title": "I Built a Reflex Game That Remembers Your Record (ESP32 + OLED)",
    "version": 2,
    "lead_in": 0.8,     # cold open starts on the game, no title card
    "sting_after": "s03",  # cold open: play, unplug, replug -> logo sting -> "Today we build..."
    "scene_gap": 0.7,   # fast tempo (creator 2026-11-21): shorter pause when the visual changes
    "segments": S,
}

if __name__ == "__main__":
    here = Path(__file__).parent
    (here / "script.json").write_text(json.dumps(SCRIPT, ensure_ascii=False, indent=1), encoding="utf-8")
    (here / "dub").mkdir(exist_ok=True)
    tr = {"lang": "tr", "segments": {d["id"]: d["dub"] for d in S}}
    (here / "dub" / "tr.json").write_text(json.dumps(tr, ensure_ascii=False, indent=1), encoding="utf-8")
    words = sum(len(d["text"].split()) for d in S)
    b3d = sum(len(d["text"].split()) for d in S if d["vis"].startswith("b3d"))
    print(f"{len(S)} segments, {words} words (~{words / 140:.1f} min at 140 wpm), 3D share by words {b3d / words:.0%}")
