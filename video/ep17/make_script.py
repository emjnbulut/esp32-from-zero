"""Source of video/ep17/script.json (and dub/tr.json). Usage: python video/ep17/make_script.py

DRAFT (25 Nov 2026, not reviewed by the creator). Curriculum v7 draft Ep 17: "My Phone Switches a Real Fan with an ESP32".
New: the relay module (2-channel, 5 V, ACTIVE-LOW, IN1 GPIO 16), switching a separate circuit, the boot-click trap
(digitalWrite HIGH before pinMode), a 10-minute auto-off timer. Reused: the Episode 12 phone page (softAP
PinByPin-ESP32 / esp32lab, 192.168.4.1, server.on links), the Episode 10 OLED.
Circuit: relay VCC -> VIN (5 V), GND, IN1 -> 16; a USB desk fan's + wire through relay 1 COM -> NO; OLED 21/22.
SAFETY (must be spoken AND shown): 5 V USB loads only, never wall-socket voltage in this course.
Sketch: lessons/17-phone-fan. No buzzer in this episode: the relay's own click is the sound (sfx "click", louder).
Rules as Ep 10-16 v2 (>= half 3D, MC for the few code lines, readable full-code pages, no "subscribe" in narration,
comments question at the end).
Analogies: NEW relay = "a light switch flipped by a tiny magnet" (add to video/ANALOGIES.md before production; limit:
a real light switch is moved by your finger, the relay's arm by a coil that only pulls while current flows, and it
springs back when it stops). REUSED: the phone hotspot + numbered restaurant menu (Episode 12, named only); the
10-minute timer = the parking ticket (save the moment it runs out, compare with millis, Ep 9/11/15).
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
s("s01", "b3d:open_click", "I tap my phone... click. And a real fan starts blowing.",
  "Telefona dokunuyorum... klik. Ve gerçek bir vantilatör esmeye başlıyor.")
s("s02", "b3d:open_timer", "Tap ON for ten minutes, and later it switches itself off.",
  "On dakika açık düğmesine dokunun, sonra kendi kendine kapanıyor.")
s("s03", "b3d:open_orbit", "The ESP32 can't power a fan. But it can flip a switch that does.",
  "ESP otuz iki bir vantilatörü çalıştıramaz. Ama onu çalıştıran bir anahtarı çevirebilir.")
s("s04", "b3d:open_title", "Today: a relay, a USB fan, and the phone page from episode twelve.",
  "Bugün: bir röle, bir USB vantilatör ve on ikinci bölümdeki telefon sayfası.", pad=0.4)

# ---- safety first
s("s05", "b3d:safety", "One rule first. Only five volt USB things in this course: a USB fan or a USB lamp. Never "
  "anything from a wall socket.",
  "Önce bir kural. Bu kursta sadece beş voltluk USB cihazlar: bir USB vantilatör ya da USB lamba. Asla prizden "
  "gelen bir şey değil.")

# ---- the relay
s("s06", "b3d:relay_module", "This blue box is a relay. Think of a light switch, flipped by a tiny magnet.",
  "Bu mavi kutu bir röle. Minicik bir mıknatısın çevirdiği bir ışık anahtarı düşünün.")
s("s07", "b3d:relay_inside", "Inside is a coil. Current through it pulls a metal arm over: click, the contact closes.",
  "İçinde bir bobin var. İçinden akım geçince metal bir kolu çekiyor: klik, kontak kapanıyor.")
s("s08", "b3d:relay_two", "The pin only moves the arm. The fan's own power flows through the contact, in a separate "
  "circuit.",
  "Pin sadece kolu hareket ettiriyor. Vantilatörün kendi gücü kontaktan, ayrı bir devreden akıyor.")
s("s09", "mc:two_circuits", "Two circuits that never touch: the weak three point three volt pin on one side, the fan on "
  "the other.",
  "Birbirine hiç değmeyen iki devre: bir tarafta zayıf üç virgül üç voltluk pin, diğer tarafta vantilatör.")

# ---- wiring
s("s10", "b3d:wire_relay", "The relay module: power to V I N, that's five volts, ground to ground, and IN one to pin "
  "sixteen.",
  "Röle modülü: güç V I N'e, yani beş volta, toprak toprağa, IN bir on altı numaralı pine.")
s("s11", "b3d:wire_fan", "The fan's plus wire goes through the relay: into COM, and out of N O, normally open. "
  "Off until the relay clicks.",
  "Vantilatörün artı kablosu röleden geçiyor: COM'a giriyor, N O'dan çıkıyor, yani normalde açık. Röle "
  "kliklenene kadar kapalı.")
s("s12", "b3d:wire_screen", "The screen stays on twenty-one and twenty-two, like before.",
  "Ekran önceki gibi yirmi bir ve yirmi ikide kalıyor.")

# ---- active-low
s("s13", "mc:active_low", "Now the surprise: this relay turns on when the pin is low, and off when it's high. Low "
  "means on.",
  "Şimdi sürpriz: bu röle pin LOW olunca açılıyor, HIGH olunca kapanıyor. LOW açık demek.",
  "Şimdi sürpriz: bu röle pin lov olunca açılıyor, hay olunca kapanıyor. Lov açık demek.")
s("s14", "b3d:boot_click", "That's why it can click on by itself for a moment when the board starts.",
  "Bu yüzden kart açılırken bir anlığına kendi kendine kliklenebiliyor.")
s("s15", "mc:code_boot", "The fix is the order: first write high, so it's off, and only then make the pin an output.",
  "Çözüm sıralamada: önce HIGH yazın, yani kapalı, ancak ondan sonra pini çıkış yapın.",
  "Çözüm sıralamada: önce hay yazın, yani kapalı, ancak ondan sonra pini çıkış yapın.")

# ---- the phone page again
s("s16", "mc:page_again", "The phone side is episode twelve again: the board's own Wi-Fi, and a page with three "
  "buttons.",
  "Telefon tarafı yine on ikinci bölüm: kartın kendi Wi-Fi ağı ve üç düğmeli bir sayfa.")
s("s17", "mc:code_links", "Three links: on, off, and timer. Each one calls a tiny helper that flips the relay.",
  "Üç bağlantı: açık, kapalı ve zamanlayıcı. Her biri röleyi çeviren küçük bir yardımcıyı çağırıyor.")
s("s18", "mc:code_timer", "The timer is the parking ticket again: write down when it should switch off, and keep "
  "comparing with millis.",
  "Zamanlayıcı yine otopark bileti: ne zaman kapanacağını not edin ve millis ile karşılaştırmaya devam edin.",
  "Zamanlayıcı yine otopark bileti: ne zaman kapanacağını not edin ve milis ile karşılaştırmaya devam edin.")

# ---- try it
s("s19", "b3d:try_on", "Join the Wi-Fi, open the page, tap ON. Click, and the fan blows.",
  "Wi-Fi'a bağlanın, sayfayı açın, açık düğmesine dokunun. Klik, vantilatör esiyor.")
s("s20", "b3d:try_timer", "Tap ON for ten minutes, and the screen counts down the minutes.",
  "On dakika açık düğmesine dokunun, ekran dakikaları geri sayıyor.")
s("s21", "b3d:try_off", "When it reaches zero... click. Off, all by itself.",
  "Sıfıra gelince... klik. Kendi kendine kapandı.")

# ---- common problem
s("s22", "b3d:trouble_reverse", "A common problem: everything works backwards, on means off. Your fan is on N C instead "
  "of N O. Move the wire one hole over.",
  "Sık bir sorun: her şey ters çalışıyor, açık kapalı demek. Vantilatörünüz N O yerine N C'de. Kabloyu bir delik "
  "kaydırın.")

# ---- challenge + outro
s("s23", "b3d:challenge", "Your turn: the module has a second relay. Put a USB lamp on it, on pin seventeen, with its "
  "own buttons.",
  "Sıra sizde: modülde ikinci bir röle var. On yedi numaralı pinle ona bir USB lamba bağlayın, kendi düğmeleriyle.")
s("s24", "mc:code_full", "The full code and the solution are in the lesson folder, linked below. What would you switch "
  "from your phone? Tell me in the comments.",
  "Tam kod ve çözüm aşağıdaki bağlantıdaki ders klasöründe. Siz telefondan neyi açıp kapatırdınız? Yorumlarda yazın.")
s("s25", "b3d:outro", "See you in the next episode.",
  "Bir sonraki bölümde görüşürüz.", pad=0.8)

# Full code must stay readable (creator 2026-11-25): phone_fan.ino ~105 lines -> 5 pages x ~4 s.
for _d in S:
    if _d["id"] == "s24":
        _d["pad"] = 20.0

SCRIPT = {
    "episode": "ep17",
    "title": "My Phone Switches a Real Fan with an ESP32 (Relay)",
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
