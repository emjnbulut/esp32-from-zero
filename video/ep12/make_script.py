"""Source of video/ep12/script.json (and dub/tr.json). Usage: python video/ep12/make_script.py

DRAFT (24 Nov 2026, not yet reviewed by the creator). Curriculum v7 draft Ep 12:
"Control Your ESP32 from Your Phone - No App, No Router". Nothing new on the board: RGB LED (25/26/27, Ep 6), OLED
(21/22) and passive buzzer (32) from Ep 10. Sketch: lessons/12-phone-control (phone_remote + challenge_party).
New ideas, kept light: the board opens its own Wi-Fi (softAP) like a phone hotspot; inside it the board's address is
always 192.168.4.1; a web page where every button is a link and every link is a command (server.on); the part after
"?" carries the detail (server.arg); loop() only checks whether a phone is knocking (server.handleClient).
The page itself is a ready template: change labels/colors only.
Rules as Ep 10/11 v2: PRODUCTION_GUIDELINES 9 + 12, >= half the runtime 3D (b3d:*), MC (mc:*) for the few code lines,
full-code glimpses, buzzer = shrill piezo + rings, no "subscribe" in narration, ask for comments at the end.
Analogies (video/ANALOGIES.md): NEW phone hotspot (softAP), NEW restaurant menu where every dish has a number you
call out (page buttons = links = commands), NEW order slip with a note (?c=red = the detail of the order);
REUSED night guard doing rounds (loop + handleClient).
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


# ---- cold open
s("s01", "b3d:open_tap", "I tap red on my phone... and the light on my desk turns red.",
  "Telefonda kırmızıya dokunuyorum... ve masamdaki ışık kırmızı oluyor.")
s("s02", "b3d:open_ring", "I tap ring, and it plays a doorbell. No app, no cable, no home Wi-Fi.",
  "Zile dokunuyorum, kapı zili çalıyor. Uygulama yok, kablo yok, ev interneti yok.")
s("s03", "b3d:open_count", "And the little screen counts every command my phone sends.",
  "Küçük ekran da telefonun gönderdiği her komutu sayıyor.")
s("s04", "b3d:open_orbit", "Today the board gets a remote control: your phone. And you don't add a single new part.",
  "Bugün kartın bir uzaktan kumandası oluyor: telefonunuz. Üstelik tek bir yeni parça bile eklemiyorsunuz.")

# ---- the idea: its own Wi-Fi
s("s05", "b3d:wifi_rings", "The ESP32 has Wi-Fi built in. Here's the antenna, this zig-zag line on the board.",
  "ESP otuz ikinin içinde Wi-Fi var. Anteni de burada, karttaki şu zikzak çizgi.")
s("s06", "b3d:wifi_hotspot", "Usually a device joins your home router. Today it's the other way round: the board opens "
  "its own little network, like the hotspot on your phone.",
  "Normalde cihazlar evdeki modeme bağlanır. Bugün tam tersi: kart kendi küçük ağını açıyor, "
  "telefonunuzdaki kişisel erişim noktası gibi.")
s("s07", "b3d:wifi_join", "Your phone joins that network, like any Wi-Fi. Inside it, the board always has the same "
  "address: one nine two, one six eight, four, one.",
  "Telefonunuz bu ağa herhangi bir Wi-Fi gibi bağlanıyor. İçeride kartın adresi hep aynı: "
  "yüz doksan iki, yüz altmış sekiz, dört, bir.")
s("s08", "mc:code_softap", "In code, opening the network is one line: soft A P, with a name and a password.",
  "Kodda ağı açmak tek satır: softAP, bir isim ve bir şifreyle.",
  "Kodda ağı açmak tek satır: soft Ey Pi, bir isim ve bir şifreyle.")

# ---- the page: every button is a link
s("s09", "mc:page_menu", "Then the board serves a tiny web page. Think of a restaurant menu where every dish has a "
  "number: tap a button, and the phone calls out that number.",
  "Sonra kart küçük bir web sayfası sunuyor. Her yemeğin bir numarası olan bir restoran menüsü düşünün: "
  "bir düğmeye dokunursunuz, telefon o numarayı söyler.")
s("s10", "mc:page_links", "Here, the numbers are short links: slash color for the light, slash ring for the buzzer.",
  "Burada numaralar kısa bağlantılar: ışık için eğik çizgi color, buzzer için eğik çizgi ring.",
  "Burada numaralar kısa bağlantılar: ışık için eğik çizgi kalır, bazır için eğik çizgi ring.")
s("s11", "mc:code_on", "And one line per link tells the board which helper answers it. Server on: this link, this "
  "helper.",
  "Her bağlantı için tek satır, karta hangi yardımcının cevap vereceğini söylüyor. server.on: bu bağlantı, "
  "bu yardımcı.",
  "Her bağlantı için tek satır, karta hangi yardımcının cevap vereceğini söylüyor. Server on: bu bağlantı, "
  "bu yardımcı.")
s("s12", "mc:code_loop", "The loop has one job now: like our night guard doing rounds, it checks again and again "
  "whether a phone is knocking.",
  "Döngünün artık tek işi var: tur atan bekçimiz gibi, bir telefonun kapıyı çalıp çalmadığına tekrar "
  "tekrar bakıyor.")
s("s12b", "mc:order_slip", "Some links carry a detail, like a note on an order slip. In slash color question "
  "mark c equals red, the note says which color.",
  "Bazı bağlantılar bir ayrıntı taşır, sipariş fişindeki bir not gibi. color soru işareti c eşittir red "
  "bağlantısında not, hangi renk olduğunu söylüyor.",
  "Bazı bağlantılar bir ayrıntı taşır, sipariş fişindeki bir not gibi. Kalır soru işareti si eşittir red "
  "bağlantısında not, hangi renk olduğunu söylüyor.")
s("s12c", "mc:code_arg", "The helper reads that note with one line, server arg c, and picks the color with a few "
  "ifs, just like episode six.",
  "Yardımcı bu notu tek satırla okuyor, server.arg c, ve altıncı bölümdeki gibi birkaç if ile rengi seçiyor.",
  "Yardımcı bu notu tek satırla okuyor, server arg si, ve altıncı bölümdeki gibi birkaç if ile rengi seçiyor.")
s("s12d", "mc:code_answer", "Then it answers the phone with the same page again, so your remote stays on the screen.",
  "Sonra telefona aynı sayfayla cevap veriyor, böylece kumandanız ekranda kalıyor.")
s("s13", "mc:page_template", "The page itself is a ready template in the sketch. You only change the labels and the "
  "colors.",
  "Sayfanın kendisi koddaki hazır bir şablon. Sadece yazıları ve renkleri değiştiriyorsunuz.")

# ---- wiring: nothing new
s("s14", "b3d:wire_same", "The circuit? It's already on your desk: the color LED from episode six, the screen and the "
  "buzzer from episode ten.",
  "Devre mi? Zaten masanızda: altıncı bölümün renkli LED'i, onuncu bölümün ekranı ve buzzer'ı.",
  "Devre mi? Zaten masanızda: altıncı bölümün renkli LED'i, onuncu bölümün ekranı ve bazırı.")
s("s15", "b3d:wire_rgb", "Red, green and blue legs on pins twenty-five, twenty-six and twenty-seven, each through "
  "its resistor.",
  "Kırmızı, yeşil ve mavi bacaklar yirmi beş, yirmi altı ve yirmi yedi numaralı pinlerde, her biri kendi "
  "direncinden geçerek.")

# ---- try it
s("s16", "b3d:try_upload", "Upload, and the screen shows the address to open.",
  "Yükleyin, ekran açmanız gereken adresi gösteriyor.")
s("s17", "b3d:try_join", "On the phone, open Wi-Fi settings and join the board's network with its password.",
  "Telefonda Wi-Fi ayarlarını açın ve şifresiyle kartın ağına bağlanın.")
s("s18", "b3d:try_page", "Type the address in the browser, and there's your remote: four colors and a ring button.",
  "Adresi tarayıcıya yazın, işte kumandanız: dört renk ve bir zil düğmesi.")
s("s19", "b3d:try_red", "Tap red: the link travels through the air, the helper sets the color, and the screen counts "
  "command number one.",
  "Kırmızıya dokunun: bağlantı havadan gidiyor, yardımcı rengi ayarlıyor, ekran bir numaralı komutu sayıyor.")
s("s19b", "b3d:try_packet", "What really happens: the phone sends a tiny message through the air, the board reads it, "
  "changes the light, and sends the page back. All in a blink.",
  "Aslında olan şu: telefon havadan küçük bir mesaj gönderiyor, kart okuyor, ışığı değiştiriyor ve sayfayı "
  "geri gönderiyor. Hepsi bir göz kırpmasında.")
s("s19c", "b3d:try_colors", "Green, blue, off. Every tap is a new command, and the counter on the screen keeps "
  "going up.",
  "Yeşil, mavi, kapalı. Her dokunuş yeni bir komut ve ekrandaki sayaç artmaya devam ediyor.")
s("s20", "b3d:try_ring", "Tap ring, and the buzzer plays two notes, like a doorbell.",
  "Zile dokunun, buzzer kapı zili gibi iki nota çalıyor.",
  "Zile dokunun, bazır kapı zili gibi iki nota çalıyor.")

# ---- common problems
s("s21", "b3d:trouble_nointernet", "A common problem: the phone says this network has no internet and quietly "
  "switches back to mobile data. Tell it to stay connected.",
  "Sık bir sorun: telefon bu ağda internet yok deyip sessizce mobil veriye dönüyor. Bağlı kalmasını söyleyin.")
s("s22", "b3d:trouble_password", "And the password needs at least eight characters, or the network never appears.",
  "Bir de şifre en az sekiz karakter olmalı, yoksa ağ hiç görünmüyor.")

# ---- challenge + outro
s("s22b", "b3d:trouble_address", "And type the address exactly: just the numbers, no www and no https in front.",
  "Bir de adresi tam yazın: sadece sayılar, başında www ya da https yok.")
s("s23", "b3d:challenge", "Your turn: add a party button that flashes red, green and blue three times. One new link, "
  "one new helper.",
  "Sıra sizde: kırmızı, yeşil ve maviyi üç kez yakıp söndüren bir parti düğmesi ekleyin. Bir yeni bağlantı, "
  "bir yeni yardımcı.")
s("s24", "mc:code_full", "The full code and the solution are in the lesson folder, linked below. What would you "
  "control with your phone? Tell me in the comments.",
  "Tam kod ve çözüm aşağıdaki bağlantıdaki ders klasöründe. Siz telefonunuzla neyi kontrol ederdiniz? "
  "Yorumlarda yazın.")
s("s25", "b3d:outro", "Next time, a weather station: temperature and humidity on the screen and on this very phone "
  "page. See you there.",
  "Bir dahaki sefere hava istasyonu: sıcaklık ve nem hem ekranda hem bu telefon sayfasında. Orada görüşürüz.",
  pad=0.8)

# TR lines shortened to fit the English slots after the narrated fit report (2026-11-24, as Ep 10/11).
TR_FIT = {
    "s01": "Telefonda kırmızıya dokunuyorum... ışık kırmızı.",
    "s04": "Bugün kartın kumandası telefonunuz oluyor, tek yeni parça yok.",
    "s08": "Kodda ağı açmak tek satır: soft Ey Pi, isim ve şifreyle.",
    "s09": "Sonra kart küçük bir web sayfası sunuyor, numaralı bir restoran menüsü gibi: düğmeye dokunun, "
           "telefon numarayı söyler.",
    "s11": "Her bağlantı için tek satır: Server on, bu bağlantı, bu yardımcı.",
    "s12": "Döngünün tek işi var: tur atan bekçimiz gibi, kapıyı çalan telefon var mı diye bakıyor.",
    "s12b": "Bazı bağlantılar, sipariş fişindeki not gibi bir ayrıntı taşır: Kalır soru işareti si eşittir red, "
            "hangi renk olduğunu söylüyor.",
    "s13": "Sayfa hazır bir şablon, sadece yazıları ve renkleri değiştirin.",
    "s15": "Kırmızı, yeşil, mavi bacaklar yirmi beş, yirmi altı, yirmi yedide, dirençleriyle.",
    "s18": "Adresi yazın, işte kumanda: dört renk ve zil.",
    "s19": "Kırmızıya dokunun: mesaj havadan gidiyor, renk değişiyor, ekran sayıyor.",
    "s23": "Sıra sizde: kırmızı, yeşil, maviyi üç kez yakan bir parti düğmesi ekleyin, yeni bir bağlantı ve "
           "yardımcıyla.",
}
for _d in S:
    if _d["id"] in TR_FIT:
        _d["tr"] = _d["dub"] = TR_FIT[_d["id"]]

SCRIPT = {
    "episode": "ep12",
    "title": "Control Your ESP32 from Your Phone - No App, No Router",
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
