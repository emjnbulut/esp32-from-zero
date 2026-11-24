"""Source of video/ep15/script.json (and dub/tr.json). Usage: python video/ep15/make_script.py

DRAFT (25 Nov 2026, not reviewed by the creator). Curriculum v7 draft Ep 15: "My Drawer Screams When Someone Opens It".
New: the LDR light-sensor module (analog, GPIO 35), two thresholds (hysteresis), an opening counter kept in Preferences.
Circuit: Ep 10 layout (OLED 21/22, button 19, passive buzzer 32) + LDR module AO 35 / VCC 3V3 / GND. Sketch:
lessons/15-drawer-spy (OPEN_AT 1800, CLOSED_AT 1200, 5 s whoop 1500-2700 Hz, hold button 2 s = reset).
Rules as Ep 10-14 v2 (>= half 3D, MC for the few code lines, readable full-code pages, shrill piezo + rings, no
"subscribe" in narration, comments question at the end).
Analogies (video/ANALOGIES.md): hysteresis = thermostat (registered for ep15); Preferences = the notebook from Episode 10
(say "notebook", NOT "drawer", in this episode - the real drawer would make it confusing); challenge = parking ticket
(Ep 9/11 reuse); averaging 8 looks = Episode 7 (no new picture).
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
s("s01", "b3d:open_scream", "Somebody opens my drawer... and it screams.",
  "Biri çekmecemi açıyor... ve çekmece çığlık atıyor.")
s("s02", "b3d:open_count", "And when I come back, the little screen tells me: opened three times.",
  "Geri geldiğimde küçük ekran söylüyor: üç kez açıldı.")
s("s03", "b3d:open_orbit", "Even if the power went out in between. One tiny light sensor does it all.",
  "Arada elektrik kesilse bile. Hepsini küçücük bir ışık sensörü yapıyor.")
s("s04", "b3d:open_title", "Today we build a drawer spy. The rest is the circuit from episode ten.",
  "Bugün bir çekmece casusu yapıyoruz. Gerisi onuncu bölümün devresi.")

# ---- the sensor
s("s05", "b3d:ldr_module", "This is the light sensor module from the kit. Four pins: A O, D O, ground and power.",
  "Bu, setteki ışık sensörü modülü. Dört pin: A O, D O, toprak ve güç.")
s("s06", "b3d:ldr_macro", "The little round part changes with light. The board reads it as a number, from zero to "
  "four thousand ninety-five.",
  "Küçük yuvarlak parça ışıkla değişiyor. Kart onu sıfırdan dört bin doksan beşe kadar bir sayı olarak okuyor.")
s("s07", "mc:light_number", "In a closed drawer it's dark, so the light number is low. Open it, and the number jumps.",
  "Kapalı çekmece karanlık, yani ışık sayısı düşük. Açınca sayı fırlıyor.")
s("s08", "mc:code_read", "Careful: many of these modules give a higher number in the dark. One line in the code flips "
  "it, so for us zero always means dark.",
  "Dikkat: bu modüllerin çoğu karanlıkta daha yüksek sayı veriyor. Koddaki bir satır bunu çeviriyor, böylece "
  "bizim için sıfır her zaman karanlık demek.")

# ---- wiring
s("s09", "b3d:wire_keep", "Let's wire it. The screen, the button and the buzzer stay where they were.",
  "Hadi bağlayalım. Ekran, düğme ve buzzer yerinde kalıyor.",
  "Hadi bağlayalım. Ekran, düğme ve bazır yerinde kalıyor.")
s("s10", "b3d:wire_ldr", "Power to three point three volts, ground to ground, and A O to pin thirty-five. D O stays "
  "empty.",
  "Güç üç virgül üç volta, toprak toprağa, A O otuz beş numaralı pine. D O boş kalıyor.")
s("s11", "b3d:wire_drawer", "Then the sensor goes inside the drawer, facing up, with the wires coming out at the back.",
  "Sonra sensör çekmecenin içine giriyor, yukarı bakıyor, kablolar arkadan çıkıyor.")

# ---- one threshold is not enough
s("s12", "mc:one_line", "First idea: one line. Above it, the drawer is open. Below it, closed.",
  "İlk fikir: tek bir çizgi. Üstündeyse çekmece açık. Altındaysa kapalı.")
s("s13", "b3d:flicker", "But open the drawer just a crack, and the number wobbles right on that line. Alarm on, off, "
  "on, off.",
  "Ama çekmeceyi biraz aralayınca sayı tam o çizginin üstünde titriyor. Alarm açık, kapalı, açık, kapalı.")
s("s14", "mc:thermostat", "A thermostat has the same problem, and solves it by waiting a little before switching back.",
  "Termostatın da aynı sorunu var, geri dönmeden önce biraz bekleyerek çözüyor.")
s("s15", "mc:two_lines", "So we use two lines. Open above eighteen hundred, closed again only below twelve hundred. "
  "In between, nothing changes.",
  "Bu yüzden iki çizgi kullanıyoruz. Bin sekiz yüzün üstünde açık, ancak bin iki yüzün altında tekrar kapalı. "
  "Arada hiçbir şey değişmiyor.")
s("s16", "mc:code_hyst", "In code, that's two ifs: if it's closed and the light goes above the top line, it opened. If "
  "it's open and the light falls below the bottom line, it closed.",
  "Kodda bu iki if: kapalıysa ve ışık üst çizgiyi geçerse açıldı. Açıksa ve ışık alt çizginin altına düşerse "
  "kapandı.")

# ---- scream + counter
s("s17", "b3d:scream", "When it opens, the buzzer screams for five seconds, a fast up and down whoop.",
  "Açılınca buzzer beş saniye boyunca çığlık atıyor, hızlı inip çıkan bir siren.",
  "Açılınca bazır beş saniye boyunca çığlık atıyor, hızlı inip çıkan bir siren.")
s("s18", "mc:code_counter", "And the counter goes up by one, written into the notebook from episode ten. Only when the "
  "drawer opens, never every loop.",
  "Sayaç da bir artıyor ve onuncu bölümdeki deftere yazılıyor. Sadece çekmece açılınca, asla her döngüde değil.")
s("s19", "b3d:power_cut", "Pull the cable, plug it back in, and the screen still says: opened three times.",
  "Kabloyu çekin, geri takın, ekran hâlâ diyor ki: üç kez açıldı.")
s("s20", "b3d:reset_hold", "To start fresh, hold the button for two seconds. The counter goes back to zero.",
  "Sıfırdan başlamak için düğmeyi iki saniye basılı tutun. Sayaç sıfıra dönüyor.")

# ---- tuning + common problem
s("s21", "b3d:tune_serial", "Your drawer is different from mine. The board prints the light number twice a second: "
  "read it with the drawer shut and open, and move the two lines to fit.",
  "Sizin çekmeceniz benimkinden farklı. Kart ışık sayısını saniyede iki kez yazdırıyor: çekmece kapalıyken ve "
  "açıkken okuyun, iki çizgiyi ona göre kaydırın.")
s("s22", "b3d:trouble_day", "A common problem: it screams while the drawer is closed. Light is getting in through a gap, "
  "so tape over it, or raise the top line.",
  "Sık bir sorun: çekmece kapalıyken çığlık atıyor. Bir aralıktan ışık giriyordur, orayı bantlayın ya da üst "
  "çizgiyi yükseltin.")

# ---- challenge + outro
s("s23", "b3d:challenge", "Your turn: make the screen also show how long the drawer was open last time. Hint: the "
  "parking ticket again.",
  "Sıra sizde: ekran çekmecenin son seferde ne kadar açık kaldığını da göstersin. İpucu: yine otopark bileti.")
s("s24", "mc:code_full", "The full code and the solution are in the lesson folder, linked below. What would you guard "
  "with a light sensor? Tell me in the comments.",
  "Tam kod ve çözüm aşağıdaki bağlantıdaki ders klasöründe. Siz ışık sensörüyle neyi korurdunuz? Yorumlarda yazın.")
s("s25", "b3d:outro", "Next time, a basketball scoreboard for a paper ball. See you there.",
  "Bir dahaki sefere, kâğıt top için bir basketbol skorbordu. Orada görüşürüz.", pad=0.8)

# Full code must stay readable (creator 2026-11-25): drawer_spy.ino ~100 lines -> 5 pages x ~4 s.
for _d in S:
    if _d["id"] == "s24":
        _d["pad"] = 20.0

SCRIPT = {
    "episode": "ep15",
    "title": "My Drawer Screams When Someone Opens It (ESP32 Light Sensor)",
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
