"""Builds the creator's shoot pack page (video/shoot/build/cekim_paketi.html, published as an Artifact).
For every video part: the breadboard pictures (video/shoot/build/<setup>.png, rendered by wiring.js), the sketches to
upload (full code from lessons/), and the list of real clips to film. Usage: python video/shoot/make_pack.py
User 2026-10-28: "sen planlamaları yaparsın, bana her video için çekimler ve kodları ver, breadboarda nasıl dizmem
gerek fotoğrafla göster; ben teker teker çekip atarım, sen kontrol edersin."
"""
import base64
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "video" / "shoot" / "build"
INBOX = r"C:\Users\emin\esp32-from-zero\footage\gelen"


def img(name, ext="png"):
    if ext == "png" and not (B / f"{name}.png").exists():
        ext = "jpg"  # photos annotated over a real clip frame
    mime = "jpeg" if ext == "jpg" else "png"
    return f"data:image/{mime};base64," + base64.b64encode((B / f"{name}.{ext}").read_bytes()).decode()


def code(lesson, sketch):
    p = ROOT / "lessons" / lesson / "code" / sketch / f"{sketch}.ino"
    return {"name": sketch, "path": str(p), "src": p.read_text(encoding="utf-8")}


L5, L6, L7 = "05-pwm-and-rgb", "06-analog-input", "07-mini-project-1"

# id, title, release date, pictures (setup, caption), steps, sketches, clips (id, what, seconds, framing, check)
PARTS = [
    {"id": "p05-1", "tag": "05 · Kısım 1", "title": "PWM: LED'i nefes aldırmak", "date": "Sal 3 Kas",
     "pics": [("base", "Devre: hiçbir şeyi değiştirmeyin (Bölüm 04 sonundaki hali)"),
              ("05-1-meter", "C1 için multimetre probları")],
     "steps": ["Devre olduğu gibi kalıyor: kırmızı LED D23, buton D22, yeşil LED D25."],
     "code": [code(L5, "fade_millis"), code(L5, "pwm_levels"), code(L5, "fade_naive")],
     "clips": [
         ("C0", "Açılış: fade_millis yüklü. Kırmızı LED yavaşça nefes alıyor. Bir kez butona basın: anında durur. 2 sn sonra tekrar basın: devam eder.", "12–15", "Kırmızı LED ve buton ortada, yakın plan.", "LED yumuşakça parlayıp sönüyor; basınca anında duruyor."),
         ("C1", "Multimetre: pwm_levels yüklü. Problar görseldeki gibi, multimetre DC volt. Ekran 0 → ~0,8 → ~1,65 → ~3,3 V, her değer 2 sn.", "10–12", "Multimetre ekranı okunur, LED de kadrajda. Eller kadrajda değil.", "Dört değer sırayla görünüyor, ekran net."),
         ("C2", "pwm_levels: LED dört adımda parlıyor: kapalı, %25, %50, %100.", "10", "LED yakın plan, oda biraz loş.", "Dört parlaklık farkı gözle seçiliyor."),
         ("C3", "Yaygın hata: fade_naive yüklü. LED nefes alırken butona 3–4 kez kısa kısa basın: LED durmuyor.", "10–12", "LED, buton ve parmak kadrajda.", "Basışlara rağmen nefes devam ediyor."),
         ("C4", "Çalıştır: fade_millis yüklü. Nefes alırken basın: durur; tekrar basın: devam eder.", "10", "C0'dan daha yakın: LED ve buton.", "Durma ve devam anı net görünüyor."),
         ("C5", "İsteğe bağlı, değiştir görevi: fade_millis'te 39. satırdaki 4'ü 10 yapıp yükleyin. Nefes daha yavaş.", "8", "C4 ile aynı kadraj.", "Nefes belirgin şekilde yavaş."),
     ]},
    {"id": "p05-2", "tag": "05 · Kısım 2", "title": "RGB renk karıştırma", "date": "Cum 6 Kas",
     "pics": [("05-2-remove", "Adım 1: üst breadboard'daki yeşil LED devresini sökün"),
              ("05-2", "Adım 2: RGB LED'i takın")],
     "steps": ["USB kablosunu çıkarın.",
               "Yeşil LED'in 4 parçasını sökün: LED, direnci, yeşil kablo, 22a'daki siyah kablo.",
               "RGB LED'i c sırasına, 20–23. sütunlara takın. EN UZUN bacak soldan 2. delikte (21).",
               "Siyah kablo: 21a → üst eksi ray.",
               "Üç 220 Ω direnç boşluğun üstünden: 20f→20e, 22f→22e, 23f→23e.",
               "Kablolar: D25 → 20g (kırmızı), D26 → 22h (yeşil), D27 → 23i (mavi).",
               "İlk deneme: rgb_colors'ı yükleyin. Renkler tersse (kapalıyken beyaz yanıyorsa) RGB'niz ortak anotlu demektir; çekime başlamadan bana yazın."],
     "code": [code(L5, "rgb_colors"), code(L5, "color_modes")],
     "clips": [
         ("C0", "Açılış: color_modes yüklü. RGB ortada. 3 kez basın: kırmızı → yeşil → mavi → yavaş geçiş. Geçişte 3–4 sn bekleyin.", "12–15", "RGB LED ve buton, RGB kadrajın tam ortasında.", "Dört mod net, renkler doygun."),
         ("C1", "Kurulum: USB çıkarılmış. Yeşil LED'i sökmek, RGB'yi takmak (uzun bacak 2.), siyah kablo, 3 direnç, 3 kablo. Tek parça ya da birkaç kısa parça.", "20–40", "Üstten, üst breadboard yakın plan. Hızlandırmayı ben yaparım.", "Her parçanın deliği seçiliyor."),
         ("C2", "rgb_colors: 8 renk sırayla: kırmızı, yeşil, mavi, sarı, macenta, camgöbeği, beyaz, turuncu.", "10–12", "RGB yakın plan, oda biraz loş.", "Sekiz renk de görünüyor."),
         ("C3", "Yaygın hata: rgb_colors çalışırken RGB'nin siyah kablosunu (21a) çekin: LED söner. Geri takın: renkler döner.", "8–10", "RGB ve siyah kablo, el kadrajda.", "Sönme ve geri gelme net."),
         ("C4", "Çalıştır: color_modes. 3 basış: kırmızı → yeşil → mavi → geçiş başlıyor.", "10", "C0'dan daha yakın.", "Her basışta anında değişiyor."),
     ]},
    {"id": "p06-1", "tag": "06 · Kısım 1", "title": "Analog giriş ve potansiyometre", "date": "Sal 10 Kas",
     "pics": [("06", "Potansiyometreyi alt breadboard'un sağına ekleyin"),
              ("06-meter", "C2 için multimetre probları"),
              ("06-pot-fix", "Sizin devrenizin fotoğrafı üzerinde: ray ortada kesik, iki köprü kablo şart")],
     "steps": ["USB kablosunu çıkarın. RGB, kırmızı LED ve buton yerinde kalır.",
               "Potansiyometrenin 3 bacağı alt breadboard'da h sırasında: 28–30–32 (bacaklar bitişikse 28–29–30).",
               "Kırmızı kablo: 3V3 (2. sütun, d sırası) → alt artı ray.",
               "Sol bacak → eksi ray, sağ bacak → ARTI ray (3,3 V). Asla VIN ya da 5 V'a bağlamayın: ESP32'nin girişi en fazla 3,3 V.",
               "Turuncu kablo: orta bacak (30i) → üst breadboard 13f (D34'ün sütunu).",
               "ÖNEMLİ: alt breadboard'un artı ve eksi rayı ortada (30. sütun civarı) kesik. Kırmızı köprü: artı ray 29 → 35, siyah köprü: eksi ray 29 → 35. Bunlar olmadan pot elektrik almaz, LED yanmaz ve düğme çalışmaz."],
     "code": [code(L6, "pot_dimmer"), code(L6, "pot_read")],
     "clips": [
         ("C0", "Açılış: pot_dimmer yüklü. Düğmeyi yavaşça bir uçtan diğerine, sonra geri çevirin: kırmızı LED elinizi takip ediyor.", "12", "Düğme, el ve kırmızı LED kadrajda.", "Parlaklık düğmeyle birlikte değişiyor."),
         ("C1", "Kurulum: USB çıkarılmış. Pot, 3V3 kablosu, iki ray kablosu, turuncu kablo.", "20–30", "Üstten, alt breadboard'un sağ tarafı.", "Her bağlantı seçiliyor."),
         ("C2", "Multimetre: pot_read yüklü. Problar görseldeki gibi. Tek elle düğmeyi yavaşça çevirin: ekran 0,0 → 3,3 V.", "10", "Multimetre ekranı okunur, düğme kadrajda.", "Değer yumuşakça 0'dan 3,3 V'a çıkıyor."),
     ]},
    {"id": "p06-2", "tag": "06 · Kısım 2", "title": "map(), dimmer ve seviye çubuğu", "date": "Cum 13 Kas",
     "pics": [("06-2", "Sarı (D18) ve yeşil (D17) LED'i alt breadboard'a ekleyin")],
     "steps": ["USB kablosunu çıkarın. Önceki her şey yerinde kalır.",
               "Sarı: 220 Ω direnç D18 sütunundan (10e) boşluğun üstünden 12g'ye. LED'in uzun bacağı 12h, kısa bacağı 13h. Siyah kablo 13j → eksi ray.",
               "Yeşil: 220 Ω direnç D17 sütunundan (8d) 9g'ye. Uzun bacak 9h, kısa bacak 10h. Siyah kablo 10j → eksi ray.",
               "Bu iki LED Bölüm 07'de trafik ışığı olarak da kullanılacak; sökmeyin."],
     "code": [code(L6, "level_bar"), code(L6, "map_dimmer")],
     "clips": [
         ("C0", "Açılış: level_bar yüklü. Düğmeyi yavaşça sağa çevirin: önce yeşil, sonra sarı, sonra kırmızı yanıyor. Sonra geri çevirin.", "12", "Üç LED ve düğme kadrajda.", "LED'ler sırayla doluyor ve boşalıyor."),
         ("C1", "Kurulum: USB çıkarılmış. Sarı ve yeşil LED, dirençleri ve siyah kabloları.", "20–30", "Üstten, alt breadboard'un sol tarafı.", "Uzun bacakların yeri seçiliyor."),
         ("C2", "map_dimmer yüklü: düğmeyi çevirin, kırmızı LED parlaklığı takip ediyor.", "8–10", "Kırmızı LED ve düğme.", "Parlaklık yumuşakça değişiyor."),
         ("C3", "Çalıştır: level_bar, C0'dan daha yakın. Düğmeyi ileri geri çevirin.", "8–10", "Üç LED yakın plan.", "Her seviye net."),
         ("C4", "Yaygın hata: level_bar çalışırken sarı LED'i çıkarıp ters takın: o seviyede sarı yanmıyor. Doğru takın: yanıyor.", "10–12", "Sarı LED ve el kadrajda.", "Ters takılıyken sönük, düzeltince yanıyor."),
     ]},
    {"id": "p07-1", "tag": "07 · Kısım 1", "title": "Mini proje 1: akıllı yaya geçidi", "date": "Sal 17 Kas",
     "pics": [("07", "Devre 06·2 ile aynı, yeni kablo yok")],
     "steps": ["Kablolamaya dokunmayın. Araba ışıkları: kırmızı D23, sarı D18, yeşil D17. Yaya ışığı: RGB LED. Buton: yaya düğmesi. Düğme: arabaların yeşil süresi (3–10 sn)."],
     "code": [code(L7, "crossing"), code(L7, "press_time")],
     "clips": [
         ("C0", "Açılış: crossing yüklü. Arabalar yeşildeyken butona basın ve bir tam turu bekleyin: yeşil → sarı → kırmızı + yaya yeşili → yaya yeşili yanıp söner → yine yeşil. Düğmeyi en sola alırsanız tur daha kısa sürer.", "20–25", "Üç LED, RGB ve buton aynı kadrajda (iki breadboard).", "Bütün tur ve RGB'nin kırmızıdan yeşile geçişi görünüyor."),
         ("C1", "press_time yüklü: önce kısa bir basış, sonra 1 sn'lik uzun bir basış. Sarı LED basılıyken yanıyor.", "8–10", "Buton ve sarı LED.", "İki basış da net, LED basılı tutulduğu sürece yanıyor."),
         ("C2", "crossing: yaya yeşilinin son 2 sn'si yanıp sönüyor. RGB'ye yakın plan.", "8", "RGB yakın plan.", "Yanıp sönme net görünüyor."),
     ]},
    {"id": "p07-2", "tag": "07 · Kısım 2", "title": "Refleks oyunu ve kalıcı rekor", "date": "Cum 20 Kas",
     "pics": [("07", "Devre aynı")],
     "steps": ["Kablolamaya dokunmayın. Düğme: sarı ışığın bekleme süresi (1–4 sn)."],
     "code": [code(L7, "reflex_game")],
     "clips": [
         ("C0", "Açılış: reflex_game yüklü. Butona basıp başlatın: kırmızı → sarı → YEŞİL. Yeşil yanınca hemen basın: RGB yeşil (hızlı).", "10–12", "Üç LED, RGB ve buton aynı kadrajda.", "Işık sırası ve sonuç rengi görünüyor."),
         ("C1", "Yavaş tepki: aynı oyun, yeşilden yaklaşık 1 sn sonra basın: RGB kırmızı.", "10", "C0 ile aynı kadraj.", "Sonuç kırmızı."),
         ("C2", "Rekor kalıcı: USB kablosunu çıkarıp 2 sn sonra geri takın.", "5", "USB fişi ve kart yakın plan.", "Çıkarma ve takma anı net."),
     ]},
]

LATER = [("08", "Işık sensörü ve dokunmatik pin (ışık sensörü modülünün fotoğrafını bekliyorum)", "Cum 27 Kas / Sal 1 Ara")]

RULES = ["Telefon yatay (16:9), 1080p, 30 fps.",
         "Telefonu sabitleyin: tripod ya da kitaplara yaslayın. Elde çekim titrer.",
         "Her klip 10–20 sn; mümkünse iki deneme çekin. Baştaki ve sondaki fazlalığı ben keserim.",
         "Odak LED'de olsun: çekmeden önce ekranda LED'e dokunun.",
         "Renkli LED çekimlerinde odayı biraz karartın; renkler daha doygun çıkar.",
         "El yalnızca butona basarken ya da düğmeyi çevirirken kadrajda olsun.",
         "Kurulum çekimlerinde (C1) USB takılı olmasın."]

CSS = """
:root { --bg:#f3f1ec; --panel:#ffffff; --ink:#1d2330; --muted:#5c6575; --line:#d9d5cb; --accent:#c77700; --accent-ink:#ffffff;
  --teal:#0f8f84; --code-bg:#1b1f29; --code-ink:#e6ebf3; --chip:#efe9dd; --ok:#1f8a4c;
  --display:"Barlow Condensed","Arial Narrow",system-ui,sans-serif; --body:"IBM Plex Sans",system-ui,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Consolas,monospace; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#0f141d; --panel:#171e2a; --ink:#e9edf4; --muted:#9aa6b8; --line:#2a3445;
  --accent:#ffb547; --accent-ink:#1d1300; --teal:#3ad2c3; --code-bg:#0b0f16; --code-ink:#e6ebf3; --chip:#1f2836; --ok:#4ade80; color-scheme:dark } }
:root[data-theme="dark"] { --bg:#0f141d; --panel:#171e2a; --ink:#e9edf4; --muted:#9aa6b8; --line:#2a3445;
  --accent:#ffb547; --accent-ink:#1d1300; --teal:#3ad2c3; --code-bg:#0b0f16; --code-ink:#e6ebf3; --chip:#1f2836; --ok:#4ade80; color-scheme:dark }
body { background:var(--bg); color:var(--ink); font-family:var(--body); font-size:16px; line-height:1.55; }
.wrap { max-width:980px; margin:0 auto; padding-block:24px 64px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); }
h1 { font-family:var(--display); font-weight:700; font-size:clamp(2.2rem, 6vw, 3.2rem); line-height:1; margin:0 0 6px; letter-spacing:.01em; text-wrap:balance; }
h2 { font-family:var(--display); font-weight:700; font-size:2rem; line-height:1.05; margin:0; text-wrap:balance; }
h3 { font-family:var(--display); font-weight:600; font-size:1.3rem; margin:22px 0 10px; letter-spacing:.02em; text-transform:uppercase; color:var(--muted); }
.lede { color:var(--muted); margin:0 0 20px; }
.box { background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:18px; }
.how { display:grid; gap:12px; }
.how ol { margin:0; padding-left:22px; display:grid; gap:6px; }
.inbox { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:6px; }
.inbox code { font-family:var(--mono); background:var(--chip); padding:6px 10px; border-radius:8px; word-break:break-all; min-width:0; }
button { font:600 14px var(--body); border:1px solid var(--line); background:var(--chip); color:var(--ink); border-radius:8px; padding:6px 12px; cursor:pointer; }
button:focus-visible, a:focus-visible, input:focus-visible { outline:3px solid var(--accent); outline-offset:2px; }
.rules { margin:0; padding-left:20px; display:grid; gap:4px; }
nav.parts { display:flex; flex-wrap:wrap; gap:8px; margin:22px 0 8px; }
nav.parts a { font:600 15px var(--mono); text-decoration:none; color:var(--ink); background:var(--chip); border:1px solid var(--line); padding:6px 12px; border-radius:999px; }
section.part { margin-top:36px; padding-top:22px; border-top:2px solid var(--line); }
.phead { display:flex; flex-wrap:wrap; gap:6px 14px; align-items:baseline; }
.tag { font:700 15px var(--mono); color:var(--accent-ink); background:var(--accent); padding:3px 10px; border-radius:6px; }
.date { color:var(--muted); font-size:.95rem; }
figure { margin:0; display:grid; gap:6px; }
figure img { width:100%; height:auto; border-radius:12px; border:1px solid var(--line); background:#0b1220; }
figcaption { color:var(--muted); font-size:.92rem; }
.pics { display:grid; gap:16px; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); }
.steps { margin:0; padding-left:22px; display:grid; gap:6px; }
details.code { background:var(--panel); border:1px solid var(--line); border-radius:12px; margin-bottom:10px; }
details.code summary { cursor:pointer; padding:12px 14px; font:600 15px var(--mono); display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
details.code .path { font:400 12.5px var(--mono); color:var(--muted); word-break:break-all; min-width:0; }
.codebar { display:flex; justify-content:flex-end; padding:0 12px 8px; }
pre { margin:0; background:var(--code-bg); color:var(--code-ink); font:13px/1.5 var(--mono); padding:14px; overflow-x:auto; border-radius:0 0 12px 12px; }
.clips { display:grid; gap:10px; }
.clip { display:grid; grid-template-columns:auto 1fr; gap:4px 14px; background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:14px; }
.clip .cid { font:700 1.4rem var(--display); color:var(--accent); grid-row:span 4; min-width:2.4em; }
.clip .what { font-weight:600; min-width:0; }
.clip .meta { color:var(--muted); font-size:.92rem; min-width:0; }
.clip .check { font-size:.92rem; min-width:0; }
.clip .check b { color:var(--teal); }
.clip label { display:flex; gap:8px; align-items:center; font-size:.92rem; color:var(--muted); }
.clip.done { opacity:.6; }
.clip .shot { grid-column:1 / -1; width:100%; height:auto; border-radius:10px; border:1px solid var(--line); margin-top:8px; background:#0b1220; }
.later { display:grid; gap:6px; margin:0; padding-left:20px; color:var(--muted); }
@media (prefers-reduced-motion: reduce) { * { scroll-behavior:auto !important; } }
"""

JS = """
const KEY = 'esp32-shoot-done';
let done = {};
try { done = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { done = {}; }
document.querySelectorAll('.clip input[type=checkbox]').forEach((cb) => {
  cb.checked = !!done[cb.id];
  cb.closest('.clip').classList.toggle('done', cb.checked);
  cb.addEventListener('change', () => {
    done[cb.id] = cb.checked;
    cb.closest('.clip').classList.toggle('done', cb.checked);
    try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (e) {}
  });
});
document.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', async () => {
  const el = document.getElementById(b.dataset.copy);
  const text = el.innerText;
  try { await navigator.clipboard.writeText(text); b.textContent = 'Kopyalandı'; }
  catch (e) { const r = document.createRange(); r.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = 'Seçildi: Ctrl+C'; }
  setTimeout(() => (b.textContent = b.dataset.label), 1800);
}));
"""


def part_html(p):
    e = html.escape
    out = [f'<section class="part" id="{p["id"]}"><div class="phead"><span class="tag">{e(p["tag"])}</span>'
           f'<h2>{e(p["title"])}</h2><span class="date">Yayın: {e(p["date"])}</span></div>']
    out.append("<h3>Devre</h3><div class=\"pics\">" + "".join(
        f'<figure><img src="{img(s)}" alt="{e(c)}" loading="lazy"><figcaption>{e(c)}</figcaption></figure>' for s, c in p["pics"]) + "</div>")
    out.append('<ol class="steps">' + "".join(f"<li>{e(s)}</li>" for s in p["steps"]) + "</ol>")
    out.append("<h3>Kod</h3>")
    for c in p["code"]:
        cid = f'{p["id"]}-{c["name"]}'
        out.append(f'<details class="code"><summary>{e(c["name"])}.ino <span class="path">{e(c["path"])}</span></summary>'
                   f'<div class="codebar"><button type="button" data-copy="{cid}" data-label="Kodu kopyala">Kodu kopyala</button></div>'
                   f'<pre id="{cid}">{e(c["src"])}</pre></details>')
    out.append('<h3>Çekimler</h3><div class="clips">')
    for cid, what, secs, frame, check in p["clips"]:
        k = f'{p["id"]}-{cid}'
        out.append(f'<div class="clip"><div class="cid">{cid}</div><div class="what">{e(what)}</div>'
                   f'<div class="meta">{e(secs)} sn · {e(frame)}</div><div class="check"><b>Kontrol ederken baktığım:</b> {e(check)}</div>'
                   f'<label><input type="checkbox" id="{k}"> çekildi</label>'
                   + (f'<img class="shot" src="{img("clip_" + k[1:], "jpg")}" alt="{e(cid)} kadrajı" loading="lazy">'
                      if (B / f"clip_{k[1:]}.jpg").exists() else "") + '</div>')
    out.append("</div></section>")
    return "".join(out)


def main():
    nav = "".join(f'<a href="#{p["id"]}">{html.escape(p["tag"])}</a>' for p in PARTS)
    body = f"""<title>ESP32 Çekim Paketi</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
<h1>ESP32 Çekim Paketi</h1>
<p class="lede">Pin by Pin Lab · Bölüm 05–08 gerçek çekimleri. Her video için devre, kod ve çekim listesi.</p>
<div class="box how"><ol>
<li>Devreyi görseldeki gibi kurun (numaralar takma sırası, ✕ sökülecek parça).</li>
<li>Kodu Arduino IDE'de açıp yükleyin (dosya yolu kodun başlığında).</li>
<li>Listedeki klipleri çekip bilgisayara aktarın, sonra bana hangi klibi attığınızı yazın. Her klibi kontrol edip "tamam" ya da "şunu düzelt" diyeceğim.</li>
</ol>
<div class="inbox"><span>Klipleri bu klasöre koyun:</span><code id="inbox">{INBOX}</code>
<button type="button" data-copy="inbox" data-label="Kopyala">Kopyala</button></div></div>
<h3>Çekim kuralları</h3>
<ul class="rules">{"".join(f"<li>{html.escape(r)}</li>" for r in RULES)}</ul>
<nav class="parts">{nav}</nav>
{"".join(part_html(p) for p in PARTS)}
<section class="part"><h2>Sırada</h2><p class="lede">Kodları ve devre görselleri hazır oldukça bu sayfaya eklenecek.</p>
<ul class="later">{"".join(f"<li><b>{html.escape(t)}</b> · {html.escape(n)} · {html.escape(d)}</li>" for t, n, d in LATER)}</ul></section>
</div>
<script>{JS}</script>
"""
    out = B / "cekim_paketi.html"
    out.write_text(body, encoding="utf-8")
    print(out, round(out.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
