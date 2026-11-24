"""Source of video/ep14/script.json (and dub/tr.json). Usage: python video/ep14/make_script.py

DRAFT (25 Nov 2026, not reviewed by the creator). Curriculum v7 draft Ep 14: "I Turned Bananas into a Piano".
New: the ESP32's built-in touch pins (touchRead on 14 / 2 / 15), a list of notes = an array, record and replay 8 notes.
Circuit: Ep 10 layout (OLED 21/22, button 19, passive buzzer 32) + three wires to fruit. Sketch: lessons/14-fruit-piano.
Rules as Ep 10-12 v2 (>= half 3D, MC for the few code lines, readable full-code pages at the end, shrill piezo +
rings, no "subscribe" in narration, comments question at the end).
Analogies: NEW your body as a tiny capacitor = "a tiny bucket that the pin keeps filling; your finger makes the bucket
bigger, so filling takes longer and the number drops"; NEW array = "a row of numbered boxes" - check the registry:
Variable is "labelled moving box", so the array becomes "a row of labelled boxes, all with the same name and a number".
Before production: add both new pictures to video/ANALOGIES.md and check they don't clash with existing entries.
"""
import json
from pathlib import Path

S = []


def s(id, vis, text, tr, dub=None, sub=None, **kw):
    d = {"id": id, "vis": vis, "text": text}
    if sub:
        d["sub"] = sub
    d["tr"] = tr
    d["dub"] = dub or tr
    d.update(kw)
    S.append(d)


# ---- cold open
s("s01", "b3d:open_play", "I touch a banana... do. An apple... mi. An orange... sol.",
  "Muza dokunuyorum... do. Elmaya... mi. Portakala... sol.")
s("s02", "b3d:open_tune", "Hold the button, play a little tune on the fruit, and the board plays it back.",
  "Düğmeyi basılı tutun, meyvelerde küçük bir melodi çalın, kart onu geri çalıyor.")
s("s03", "b3d:open_orbit", "No buttons, no keys. Just fruit, three wires, and the touch pins hidden inside the ESP32.",
  "Düğme yok, tuş yok. Sadece meyve, üç kablo ve ESP otuz ikinin içinde saklı dokunma pinleri.")
s("s04", "b3d:open_title", "Today we turn this into a fruit piano. Everything else is the circuit from episode ten.",
  "Bugün bunu bir meyve piyanosuna çeviriyoruz. Gerisi onuncu bölümün devresi.")

# ---- the idea: touch pins
s("s05", "b3d:touch_pins", "Some ESP32 pins can feel a touch. We'll use three of them: fourteen, two and fifteen.",
  "ESP otuz ikinin bazı pinleri dokunuşu hissedebilir. Üçünü kullanacağız: on dört, iki ve on beş.")
s("s06", "mc:bucket", "Here's the trick. The pin keeps filling a tiny bucket of charge, again and again, and counts "
  "how fast it fills.",
  "İşin sırrı şu: pin küçük bir yük kovasını tekrar tekrar dolduruyor ve ne kadar hızlı dolduğunu sayıyor.")
s("s07", "mc:bucket_finger", "When your finger touches the wire, your body makes the bucket bigger. It fills slower, "
  "and the number drops.",
  "Parmağınız kabloya dokununca vücudunuz kovayı büyütüyor. Daha yavaş doluyor ve sayı düşüyor.")
s("s08", "b3d:touch_banana", "A banana is full of water, so it passes that touch along. That's why fruit works as a key.",
  "Muzun içi su dolu, o yüzden dokunuşu iletiyor. Meyvenin tuş gibi çalışmasının sebebi bu.")
s("s09", "mc:code_touch", "In code, one line reads it: touch read, on pin fourteen. Touched means: the number fell "
  "well below its calm value.",
  "Kodda tek satırla okuyoruz: on dört numaralı pinde touchRead. Dokunuldu demek, sayı sakin değerinin "
  "epey altına düştü demek.",
  "Kodda tek satırla okuyoruz: on dört numaralı pinde taç rid. Dokunuldu demek, sayı sakin değerinin "
  "epey altına düştü demek.")
s("s10", "mc:calibrate", "So at start-up, the board measures each fruit once while nobody touches it, and remembers "
  "that calm number.",
  "Bu yüzden kart açılışta, kimse dokunmazken her meyveyi bir kez ölçüyor ve o sakin sayıyı hatırlıyor.")

# ---- wiring
s("s11", "b3d:wire_keep", "Let's wire it. The screen, the button and the buzzer stay where they were.",
  "Hadi bağlayalım. Ekran, düğme ve buzzer yerinde kalıyor.",
  "Hadi bağlayalım. Ekran, düğme ve bazır yerinde kalıyor.")
s("s12", "b3d:wire_fruit", "Three wires: pin fourteen to the banana, pin two to the apple, pin fifteen to the orange. "
  "Just push the wire into the fruit.",
  "Üç kablo: on dört numaralı pin muza, iki numaralı pin elmaya, on beş numaralı pin portakala. "
  "Kabloyu meyveye batırmanız yeterli.")
s("s13", "b3d:wire_led", "Pin two also lights the little blue LED on many boards, so don't worry if it glows a bit.",
  "İki numaralı pin birçok kartta küçük mavi LED'i de yakıyor, biraz parlarsa endişelenmeyin.")

# ---- notes as an array
s("s14", "mc:array_boxes", "Now the notes. Three keys, three notes. Instead of three separate variables, we use one "
  "row of labelled boxes, all with the same name and a number: an array.",
  "Şimdi notalar. Üç tuş, üç nota. Üç ayrı değişken yerine, aynı isimli ve numaralı kutulardan oluşan tek bir "
  "sıra kullanıyoruz: bir dizi.")
s("s15", "mc:code_array", "Box zero holds do, box one holds mi, box two holds sol. The pins get their own row, in the "
  "same order.",
  "Sıfır numaralı kutuda do, bir numarada mi, iki numarada sol var. Pinlerin de aynı sırada kendi dizisi var.")
s("s16", "mc:code_loop_keys", "A tiny loop checks the three pads, one after another. The first one that's touched "
  "plays its note.",
  "Küçük bir döngü üç meyveye sırayla bakıyor. İlk dokunulan kendi notasını çalıyor.")

# ---- record and replay
s("s17", "b3d:rec_hold", "To record, hold the button for one second. The screen says REC.",
  "Kaydetmek için düğmeyi bir saniye basılı tutun. Ekranda REC yazıyor.")
s("s18", "mc:song_boxes", "Every note you play goes into the next box of another array: the song, eight boxes long.",
  "Çaldığınız her nota başka bir dizinin bir sonraki kutusuna giriyor: sekiz kutuluk şarkı.")
s("s19", "b3d:rec_play", "Do, mi, sol, sol, mi, do, mi, sol. Eight boxes full.",
  "Do, mi, sol, sol, mi, do, mi, sol. Sekiz kutu doldu.")
s("s20", "b3d:replay", "A short press, and the board walks along the boxes and plays them back.",
  "Kısa bir basış, kart kutuların üzerinden geçip hepsini geri çalıyor.")

# ---- common problem
s("s21", "b3d:trouble_calm", "A common problem: a key plays by itself. Usually someone touched a fruit while the board "
  "was measuring, so restart it with your hands off.",
  "Sık bir sorun: bir tuş kendi kendine çalıyor. Genelde kart ölçerken biri meyveye dokunmuştur, ellerinizi "
  "çekip kartı yeniden başlatın.")
s("s22", "b3d:trouble_drop", "If a key never plays, change the drop value in the code a little, so a smaller change "
  "counts as a touch.",
  "Bir tuş hiç çalmıyorsa koddaki düşüş değerini biraz değiştirin, böylece daha küçük bir değişim de "
  "dokunuş sayılsın.")

# ---- challenge + outro
s("s23", "b3d:challenge", "Your turn: touch the banana and the orange at the same time, and play a high do. A fourth "
  "note without a new pin.",
  "Sıra sizde: muza ve portakala aynı anda dokunun ve ince bir do çalın. Yeni pin olmadan dördüncü nota.")
s("s24", "mc:code_full", "The full code and the solution are in the lesson folder, linked below. Which fruit would you "
  "use? Tell me in the comments.",
  "Tam kod ve çözüm aşağıdaki bağlantıdaki ders klasöründe. Siz hangi meyveyi kullanırdınız? Yorumlarda yazın.")
s("s25", "b3d:outro", "Next time, a drawer that screams when someone opens it. See you there.",
  "Bir dahaki sefere, biri açınca çığlık atan bir çekmece. Orada görüşürüz.", pad=0.8)

# Full code must stay readable (creator 2026-11-25): pages after the narration, silent pad set once the sketch length
# is known (about 4 s per 24-line page). fruit_piano.ino is ~120 lines -> 5 pages -> 20 s.
for _d in S:
    if _d["id"] == "s24":
        _d["pad"] = 20.0

SCRIPT = {
    "episode": "ep14",
    "title": "I Turned Bananas into a Piano (ESP32 Touch Pins)",
    "version": 2,
    "draft": True,
    "lead_in": 0.8,
    "sting_after": "s03",
    "scene_gap": 0.7,
    "dub_stretch": False,
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
