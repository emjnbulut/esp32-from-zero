"""Source of video/ep11/script.json (and dub/tr.json). Usage: python video/ep11/make_script.py

DRAFT (24 Nov 2026, overnight, not yet reviewed by the creator). Curriculum v7 draft Ep 11:
"I Built a Motion Alarm That Catches Anyone Sneaking In". New part: HC-SR501 PIR (OUT -> GPIO 33, VCC 5 V, GND);
the Ep 10 circuit stays (OLED SDA 21 / SCL 22, button 19, passive buzzer 32). Sketch: lessons/11-motion-alarm.
New ideas, kept light: the sensor does the hard work and only answers yes/no (digitalRead); the steps of an alarm
(state, reused washing machine); remember WHEN something happened (lastMotion = millis(), "how long ago");
15 s aside: active vs passive buzzer.
Rules as Ep 10 v2: PRODUCTION_GUIDELINES section 9 + 12, at least half the runtime on the Blender model (b3d:*),
Motion Canvas (mc:*) only for the few code lines / abstract ideas, short full-code glimpses (creator 24 Nov),
buzzer beeps = shrill piezo sound + sound-wave rings (creator 24 Nov), fast tempo.
Analogies: NEW thumbs up / thumbs down (PIR output), NEW row of windows / flashlight beams (Fresnel lens zones),
NEW doorbell vs little speaker (active vs passive buzzer).
Reused: washing machine (state), parking ticket stamped at the entry (lastMotion = millis(), as pressStart in Ep 9).
Segment keys: id, vis, text (EN narration), tr (TR subtitle), dub (TR spoken, if different), sub, pad.
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


# ---- cold open: the result first
s("s01", "b3d:open_arm", "My desk has a guard now. I arm it, and I have ten seconds to leave.",
  "Masamın artık bir bekçisi var. Kuruyorum ve çıkmak için on saniyem var.")
s("s02", "b3d:open_catch", "Then a hand sneaks toward the cookie jar... and it gets caught instantly.",
  "Sonra bir el kurabiye kavanozuna uzanıyor... ve anında yakalanıyor.")
s("s03", "b3d:open_ago", "And when I come back, it even tells me when it happened: two minutes ago.",
  "Geri döndüğümde bunun ne zaman olduğunu bile söylüyor: iki dakika önce.")
s("s04", "b3d:open_orbit", "Today we build this motion alarm. One new part, and the rest is the circuit from last time.",
  "Bugün bu hareket alarmını kuruyoruz. Tek yeni parça var, gerisi geçen bölümün devresi.")

# ---- the new part: PIR
s("s05", "b3d:pir_hero", "This white dome is a motion sensor. It doesn't send anything out. It just watches for warmth.",
  "Bu beyaz kubbe bir hareket sensörü. Dışarı hiçbir şey göndermiyor. Sadece sıcaklığı izliyor.")
s("s06", "b3d:pir_glow", "Everything warm glows in infrared: your hand, a cat, a cup of tea. We can't see that glow, "
  "but this sensor can.",
  "Sıcak olan her şey kızılötesinde parlar: eliniz, bir kedi, bir fincan çay. Biz bu parıltıyı göremeyiz, "
  "ama bu sensör görebilir.")
s("s07", "b3d:pir_lens", "The dome is a lens made of many little windows. Each one looks at a different slice of the "
  "room, like a row of flashlights.",
  "Kubbe, birçok küçük pencereden oluşan bir mercek. Her biri odanın farklı bir dilimine bakıyor, "
  "yan yana dizilmiş el fenerleri gibi.")
s("s08", "b3d:pir_zones", "When something warm moves from one window to the next, the sensor notices the change, "
  "and its answer pin turns on.",
  "Sıcak bir şey bir pencereden diğerine geçince sensör bu değişimi fark ediyor ve cevap pini açılıyor.")
s("s09", "b3d:pir_answer", "So for our code, the whole sensor is just a thumbs up when something moved, and a thumbs down "
  "when nothing did.",
  "Yani kodumuz için bütün sensör, bir şey kıpırdayınca başparmak yukarı, kıpırdamayınca başparmak aşağı.")
s("s10", "b3d:pir_knobs", "On the side there are two orange knobs. One sets how long the yes lasts, the other how far "
  "it can see.",
  "Yanında iki turuncu düğme var. Biri evetin ne kadar süreceğini, diğeri ne kadar uzağı göreceğini ayarlıyor.")
s("s11", "b3d:pir_warmup", "One tip: after power-on, give it about thirty seconds to warm up. Until then it may say yes "
  "for no reason.",
  "Bir ipucu: güç verdikten sonra ona otuz saniye kadar ısınma süresi tanıyın. O zamana kadar sebepsiz yere "
  "evet diyebilir.")

# ---- wiring (printed hole numbers, like Ep 10)
s("s12", "b3d:wire_keep", "Let's wire it. The screen, the button and the buzzer stay exactly where they were.",
  "Hadi bağlayalım. Ekran, düğme ve buzzer oldukları yerde kalıyor.",
  "Hadi bağlayalım. Ekran, düğme ve bazır oldukları yerde kalıyor.")
s("s13", "b3d:wire_pir_power", "The sensor has three legs. A red wire brings five volts from the board's V-in pin, "
  "and a black wire goes to ground.",
  "Sensörün üç bacağı var. Kırmızı kablo kartın VIN pininden beş volt getiriyor, siyah kablo toprağa gidiyor.",
  "Sensörün üç bacağı var. Kırmızı kablo kartın Vi-in pininden beş volt getiriyor, siyah kablo toprağa gidiyor.")
s("s14", "b3d:wire_pir_out", "The middle leg is the answer. A purple wire takes it to pin thirty-three.",
  "Ortadaki bacak cevap. Mor kablo onu otuz üç numaralı pine taşıyor.")
s("s15", "b3d:wire_pir_done", "And don't worry: the answer comes out at three point three volts, safe for our board.",
  "Merak etmeyin: cevap üç virgül üç voltla çıkıyor, kartımız için güvenli.")

# ---- code: one line for the sensor, steps for the alarm
s("s16", "mc:code_read", "Reading it is one line: digital read on pin thirty-three. High means motion.",
  "Okumak tek satır: otuz üç numaralı pinde digitalRead. HIGH, hareket demek.",
  "Okumak tek satır: otuz üç numaralı pinde dicitıl rid. Hay, hareket demek.")
s("s17", "mc:alarm_steps", "But an alarm needs a plan, so again we use steps, like our washing machine: off, leaving, "
  "armed, and alarm.",
  "Ama bir alarmın bir plana ihtiyacı var, o yüzden yine adımlar kullanıyoruz, çamaşır makinemiz gibi: kapalı, "
  "çıkış, kurulu ve alarm.")
s("s18", "b3d:demo_countdown", "Press the button, and the countdown starts, with a tiny tick every second, so you have "
  "time to walk out.",
  "Düğmeye basınca geri sayım başlıyor, her saniye küçük bir tık sesiyle, böylece çıkmaya vaktiniz oluyor.")
s("s19", "b3d:demo_armed", "At zero, the guard is armed. Now it waits for only one thing: the sensor saying yes.",
  "Sıfırda bekçi kuruluyor. Artık tek bir şeyi bekliyor: sensörün evet demesini.")
s("s20", "mc:code_siren", "When it does, the siren starts: two notes, switching four times a second, so it really "
  "sounds like an alarm.",
  "Evet dediğinde siren başlıyor: saniyede dört kez değişen iki nota, gerçekten alarm gibi duyulsun diye.")
s("s21", "b3d:demo_stop", "Press the button to stop it. Or it stops by itself after fifteen seconds, so the neighbors "
  "stay friendly.",
  "Durdurmak için düğmeye basın. Ya da on beş saniye sonra kendiliğinden susuyor, komşular dost kalsın diye.")

# ---- remembering WHEN
s("s22", "mc:parking_ticket", "Now the clever part. At the moment of motion, we stamp the time, like the parking ticket from "
  "episode nine.",
  "Şimdi işin akıllıca kısmı. Hareket anında saati damgalıyoruz, dokuzuncu bölümdeki otopark bileti gibi.", pad=0.5)
s("s23", "mc:code_last", "It's one line: last motion equals millis. Millis is the board's stopwatch since power-on.",
  "Tek satır: lastMotion eşittir millis. Millis, kartın güç verildiğinden beri çalışan kronometresi.",
  "Tek satır: last moşın eşittir milis. Milis, kartın güç verildiğinden beri çalışan kronometresi.")
s("s24", "mc:ago_calc", "Later, now minus last motion tells us how long ago it was. Divide by sixty thousand, and "
  "you have minutes.",
  "Sonra, şimdiki zamandan lastMotion'ı çıkarınca ne kadar önce olduğunu buluyoruz. Altmış bine bölün, dakikayı "
  "bulun.",
  "Sonra, şimdiki zamandan last moşını çıkarınca ne kadar önce olduğunu buluyoruz. Altmış bine bölün, dakikayı "
  "bulun.")
s("s25", "b3d:screen_ago", "So the screen can say: seen twice, last time three minutes ago.",
  "Böylece ekran şunu söyleyebiliyor: iki kez görüldü, sonuncusu üç dakika önce.")

# ---- 15 s aside: active vs passive buzzer
s("s26", "b3d:buzzers_two", "Quick question: your kit has a second buzzer that looks almost the same. What's the "
  "difference?",
  "Kısa bir soru: kitinizde neredeyse aynı görünen ikinci bir buzzer var. Farkı ne?",
  "Kısa bir soru: kitinizde neredeyse aynı görünen ikinci bir bazır var. Farkı ne?", pad=2.6)
s("s27", "b3d:buzzers_xray", "Ours is passive: a little speaker that plays any note we send. The active one is a "
  "doorbell with its own beeper inside: power on, one fixed beep.",
  "Bizimki pasif: gönderdiğimiz her notayı çalan küçük bir hoparlör. Aktif olan ise içinde kendi biperi olan bir "
  "kapı zili: güç verince hep aynı bip.")
s("s28", "b3d:buzzers_siren", "Easier, but no siren. That's why the alarm uses the passive one.",
  "Daha kolay ama siren yok. O yüzden alarm pasif olanı kullanıyor.")

# ---- demo
s("s29", "b3d:demo_walkout", "Let's test it. I arm it, the countdown runs, and I walk out of the room.",
  "Hadi deneyelim. Kuruyorum, geri sayım işliyor ve odadan çıkıyorum.")
s("s30", "b3d:demo_cookie", "A hand sneaks toward the cookie jar... caught!",
  "Bir el kurabiye kavanozuna uzanıyor... yakalandı!")
s("s31", "b3d:demo_back", "I come back and press the button: seen once, last time twelve seconds ago.",
  "Geri dönüp düğmeye basıyorum: bir kez görüldü, sonuncusu on iki saniye önce.")

# ---- common problem
s("s32", "b3d:mistake_false", "A common problem: the alarm goes off right after you arm it. Usually the sensor is "
  "still warming up, or the time knob keeps the yes on too long.",
  "Sık görülen bir sorun: alarm siz kurar kurmaz çalıyor. Genelde sensör hâlâ ısınıyordur ya da süre düğmesi "
  "eveti çok uzun tutuyordur.")
s("s33", "b3d:mistake_fix", "So wait thirty seconds after power-on, and turn the time knob all the way down. Our code "
  "does the rest.",
  "O yüzden güç verdikten sonra otuz saniye bekleyin ve süre düğmesini sonuna kadar kısın. Gerisini kodumuz "
  "hallediyor.")

# ---- challenge + outro
s("s34", "b3d:challenge", "Your turn. Keep the number of catches even after unplugging, with Preferences, like last "
  "episode.",
  "Sıra sizde. Yakalama sayısını, geçen bölümdeki gibi Preferences ile, fiş çekilince bile saklayın.",
  "Sıra sizde. Yakalama sayısını, geçen bölümdeki gibi Preferıns ile, fiş çekilince bile saklayın.")
s("s35", "mc:code_full", "The full code and the solution are in the lesson folder, linked below. What would you guard "
  "with it? Tell me in the comments.",
  "Tam kod ve çözüm, aşağıdaki bağlantıdaki ders klasöründe. Siz bununla neyi korurdunuz? Yorumlarda yazın.")
s("s36", "b3d:outro", "Next time, you control this board from your phone, with no app and no router. See you there.",
  "Bir dahaki sefere bu kartı telefonunuzdan kontrol ediyorsunuz, uygulama ve modem olmadan. Orada görüşürüz.",
  pad=0.8)

SCRIPT = {
    "episode": "ep11",
    "title": "I Built a Motion Alarm That Catches Anyone Sneaking In (ESP32 + PIR)",
    "version": 2,
    "draft": True,
    "lead_in": 0.8,
    "sting_after": "s03",
    "scene_gap": 0.7,
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
