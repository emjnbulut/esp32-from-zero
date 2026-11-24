"""Source of video/ep16/script.json (and dub/tr.json). Usage: python video/ep16/make_script.py

DRAFT (25 Nov 2026, not reviewed by the creator). Curriculum v7 draft Ep 16: "I Built a Basketball Scoreboard That
Counts Every Shot". New: the IR obstacle sensor (OUT GPIO 13, LOW = something in front), the INTERRUPT
(attachInterrupt, FALLING, IRAM_ATTR, volatile), a 30 s round with a best score in Preferences.
Circuit: Ep 10 layout (OLED 21/22, button 19, passive buzzer 32) + IR module OUT 13 / VCC 3V3 / GND, taped under a
paper-cup hoop. Sketch: lessons/16-basket-scoreboard (start whistle 1500 Hz 300 ms, swish 2000 Hz 80 ms per basket,
horn 400 Hz 900 ms, 300 ms one-ball-one-point).
Rules as Ep 10-15 v2 (>= half 3D, MC for the few code lines, readable full-code pages, shrill piezo + rings, no
"subscribe" in narration, comments question at the end).
Analogies (video/ANALOGIES.md): interrupt = doorbell instead of checking the door (registered for ep16); 300 ms
one-ball-one-point = the Episode 4 button debounce (reuse, no new picture); best score in the notebook from Episode 10
(Preferences). `volatile` gets NO picture: one plain sentence.
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
s("s01", "b3d:open_swish", "Paper ball... swish. One point.",
  "Kâğıt top... şak. Bir sayı.")
s("s02", "b3d:open_round", "Thirty seconds on the clock, a beep for every basket, and a horn at the end.",
  "Saatte otuz saniye, her basket için bir bip ve sonunda bir korna.")
s("s03", "b3d:open_record", "New record! And it stays, even after I unplug the board.",
  "Yeni rekor! Üstelik kartı çıkarsam bile kalıyor.")
s("s04", "b3d:open_title", "Today we build a basketball scoreboard. A paper cup, one new sensor, and the circuit "
  "from episode ten.",
  "Bugün bir basketbol skorbordu yapıyoruz. Bir kâğıt bardak, yeni bir sensör ve onuncu bölümün devresi.", pad=0.4)

# ---- the sensor
s("s05", "b3d:ir_module", "This is the infrared obstacle sensor from the kit. One side sends invisible light, the other "
  "side watches for it bouncing back.",
  "Bu, setteki kızılötesi engel sensörü. Bir tarafı görünmez ışık gönderiyor, diğer tarafı geri yansımasını "
  "bekliyor.")
s("s06", "b3d:ir_out", "When something is right in front of it, its OUT pin goes low, and its little LED lights up.",
  "Önünde bir şey olunca OUT pini LOW oluyor ve küçük LED'i yanıyor.")
s("s07", "b3d:ir_trim", "Turn the tiny screw until the LED lights only when the ball passes.",
  "Küçük vidayı LED sadece top geçerken yanana kadar çevirin.")

# ---- wiring
s("s08", "b3d:wire_keep", "Let's wire it. The screen, the button and the buzzer stay where they were.",
  "Hadi bağlayalım. Ekran, düğme ve buzzer yerinde kalıyor.",
  "Hadi bağlayalım. Ekran, düğme ve bazır yerinde kalıyor.")
s("s09", "b3d:wire_ir", "Power to three point three volts, ground to ground, and OUT to pin thirteen.",
  "Güç üç virgül üç volta, toprak toprağa, OUT on üç numaralı pine.")
s("s10", "b3d:wire_cup", "Then tape the sensor under the cup's open bottom, looking across the hole.",
  "Sonra sensörü bardağın açık tabanının altına, deliğe bakacak şekilde bantlayın.")

# ---- why a doorbell
s("s11", "mc:ball_fast", "Here's the problem. A falling ball crosses the beam in just a few milliseconds.",
  "Sorun şu: düşen top ışını sadece birkaç milisaniyede geçiyor.")
s("s12", "mc:loop_miss", "If loop is busy drawing the screen at that moment, a simple digital read looks away, and the "
  "basket is lost.",
  "O anda loop ekranı çizmekle meşgulse basit bir digitalRead başka yere bakıyor ve basket kayboluyor.",
  "O anda luup ekranı çizmekle meşgulse basit bir dijital rid başka yere bakıyor ve basket kayboluyor.")
s("s13", "mc:doorbell", "Think of a door. You could keep walking over to check it, or you could install a doorbell.",
  "Bir kapı düşünün. Sürekli gidip kontrol edebilirsiniz, ya da bir kapı zili takabilirsiniz.", pad=0.4)
s("s14", "mc:interrupt", "That doorbell is called an interrupt. The moment the beam is blocked, the chip stops, runs "
  "our tiny function, and carries on.",
  "Bu kapı ziline interrupt, yani kesme deniyor. Işın kesildiği an çip duruyor, küçük fonksiyonumuzu çalıştırıyor "
  "ve devam ediyor.")
s("s15", "mc:code_attach", "One line rings it: attach interrupt, on pin thirteen, calling ball seen, when the pin falls "
  "from high to low.",
  "Tek satır zili kuruyor: on üç numaralı pinde attachInterrupt, pin HIGH'dan LOW'a düşünce ballSeen çağrılıyor.",
  "Tek satır zili kuruyor: on üç numaralı pinde ataç interapt, pin hay'dan lov'a düşünce bol siin çağrılıyor.")

# ---- the two rules
s("s16", "mc:code_tiny", "Rule one: keep that function tiny. Count, note the time, done. No screen, no delay.",
  "Birinci kural: o fonksiyonu küçücük tutun. Say, zamanı not et, bitti. Ekran yok, delay yok.",
  "Birinci kural: o fonksiyonu küçücük tutun. Say, zamanı not et, bitti. Ekran yok, dilay yok.")
s("s17", "mc:code_volatile", "Rule two: the counter gets the word volatile. It tells the compiler this value can change "
  "behind loop's back.",
  "İkinci kural: sayaç volatile kelimesini alıyor. Derleyiciye bu değerin loop'un arkasından değişebileceğini "
  "söylüyor.",
  "İkinci kural: sayaç volatayl kelimesini alıyor. Derleyiciye bu değerin luup'un arkasından değişebileceğini "
  "söylüyor.")
s("s18", "mc:one_ball", "And one ball can flicker the sensor a few times, so we only count if three hundred "
  "milliseconds have passed. Just like the button in episode four.",
  "Bir top sensörü birkaç kez titretebilir, bu yüzden ancak üç yüz milisaniye geçtiyse sayıyoruz. Tıpkı dördüncü "
  "bölümdeki düğme gibi.")

# ---- the game
s("s19", "b3d:play_start", "Press the button: a whistle, and thirty seconds start counting down.",
  "Düğmeye basın: bir düdük ve otuz saniye geri saymaya başlıyor.")
s("s20", "b3d:play_baskets", "Every basket: a short swish beep, and the score goes up.",
  "Her basket: kısa bir bip ve skor artıyor.")
s("s21", "b3d:play_horn", "Time's up: the horn. If you beat your best, it's saved in the notebook from episode ten.",
  "Süre bitti: korna. En iyi skorunuzu geçtiyseniz onuncu bölümdeki deftere kaydediliyor.")

# ---- common problem
s("s22", "b3d:trouble_sun", "A common problem: it counts by itself. Sunlight has infrared too, so move away from the "
  "window, or turn the little screw back a bit.",
  "Sık bir sorun: kendi kendine sayıyor. Güneş ışığında da kızılötesi var, pencereden uzaklaşın ya da küçük "
  "vidayı biraz geri çevirin.")

# ---- challenge + outro
s("s23", "b3d:challenge", "Your turn: a three point zone. Hold the button while you shoot, and that basket counts "
  "three.",
  "Sıra sizde: üç sayılık bölge. Atarken düğmeyi basılı tutun, o basket üç sayılsın.")
s("s24", "mc:code_full", "The full code and the solution are in the lesson folder, linked below. What's your best in "
  "thirty seconds? Tell me in the comments.",
  "Tam kod ve çözüm aşağıdaki bağlantıdaki ders klasöründe. Otuz saniyede en iyi skorunuz ne? Yorumlarda yazın.")
s("s25", "b3d:outro", "Next time, a fan you control from your phone. See you there.",
  "Bir dahaki sefere, telefondan kontrol ettiğiniz bir vantilatör. Orada görüşürüz.", pad=0.8)

# Full code must stay readable (creator 2026-11-25): basket_scoreboard.ino ~110 lines -> 5 pages x ~4 s.
for _d in S:
    if _d["id"] == "s24":
        _d["pad"] = 20.0

SCRIPT = {
    "episode": "ep16",
    "title": "I Built a Basketball Scoreboard That Counts Every Shot (ESP32 Interrupts)",
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
