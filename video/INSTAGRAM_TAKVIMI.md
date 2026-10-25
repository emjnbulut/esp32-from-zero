# Instagram takvimi ve proje Reel'leri (v1, 25 Ekim 2026)

Kullanıcı kararı (25 Ekim 2026): Instagram'da bölüm tanıtımları tek başına tutmadı → ağırlık **müfredata bağlı ama
farklı tarzda küçük projelere** geçiyor. Aynı video YouTube'da Short olarak da paylaşılır (YouTube takvimi esnek,
yoğun takvimin boş günlerine konur). Projelerde **seslendirme yok**: müzik + büyük İngilizce ekran yazıları
(sessiz izlenir, dil sorunu yok, yapay zekâ ses etiketi gerekmez). Caption EN + TR.

**Düzen** (19:00 Türkiye): Pazartesi + Perşembe proje Reel'i · Cumartesi o haftanın bölüm tanıtımı.

| Tarih | Instagram (19:00) | Çekim (senden) |
|---|---|---|
| Per 29 Eki | Proje 01 · SOS beacon | 27 Eki'ye kadar |
| Cmt 31 Eki | Bölüm 04 tanıtımı (Ep04 Short EN) | — |
| Pzt 2 Kas | Proje 02 · Pomodoro focus light | 31 Eki'ye kadar |
| Per 5 Kas | Proje 03 · Sunrise light | 3 Kas'a kadar |
| Cmt 7 Kas | Bölüm 05 tanıtımı (Ep05 Short EN) | — |
| Pzt 9 Kas | Proje 04 · Electric candle | 7 Kas'a kadar |

Sonraki projeler (05+) Bölüm 06–08'den sonra eklenir (potansiyometre, ses, ışık sensörü).

## Reel yapısı (20–35 sn, dikey 1080×1920)
1. **0–2 sn** sonuç (senin çekimin) + büyük yazı, ör. "I built an SOS beacon".
2. **2–25 sn** 3–4 hızlı adım: devre (senin çekimin) → kodun kilit satırı (benim büyük kod animasyonum) → sonuç.
3. **son 2–3 sn** "Code + wiring: link in bio · Full course: Pin by Pin Lab".
Müzik: telifsiz, caption'da kaynak. Kod ve açıklama: `projects/` (GitHub).

## Çekim listeleri (telefon DİKEY, devre yukarıdan/hafif açıyla, sabit; oda biraz loş olursa LED'ler daha iyi görünür)
Genel: her çekimin başında ve sonunda 1 sn fazla. Ses önemli değil. Dosyalar: `footage/projects/NN/S1.mp4` …

**01 · SOS beacon** (Bölüm 3–4 devresiyle; `sos_beacon` yüklü)
- S1 (6–8 sn): yakın plan kırmızı LED, karanlıkça oda, en az bir tam "... --- ..." döngüsü.
- S2 (3 sn): devrenin genel görüntüsü (kart + LED).
- S3 (3–4 sn): Serial Monitor'de "S O S" yazıları (ekrandan telefonla çekim yeterli).

**02 · Pomodoro focus light** (Bölüm 4 devresi: kırmızı 23, yeşil 25, buton 22; `pomodoro_light` yüklü) — Ep04 çekimleriyle aynı gün çekilebilir
- S1 (4 sn): parmak butona basıyor, kırmızı yavaş yanıp sönmeye başlıyor.
- S2 (25–27 sn, tek çekim): bütün tur: yavaş → hızlı → çok hızlı → yeşil yanıyor (ben hızlandırırım).
- S3 (3 sn): yeşil yanarken genel görüntü.

**03 · Sunrise light** (Bölüm 5 devresi: RGB 25/26/27, buton 22; `sunrise_light` yüklü) — Ep05 çekimleriyle aynı gün
- S1 (62–65 sn, tek çekim, karanlık oda): bas → 60 sn gün doğumu (ben timelapse yaparım).
- S2 (4 sn): RGB LED'e yakın plan, beyazken.
- S3 (3 sn): bir kâğıt/duvar üzerinde LED'in ışığı (renk ortama vursun).

**04 · Electric candle** (Bölüm 5 devresi; `candle_light` yüklü)
- S1 (8 sn, karanlık oda): titreyen turuncu "alev", mümkünse LED'in üstüne beyaz bir kâğıt/pipet kapağı (ışığı yayar).
- S2 (4 sn): butona bas → söner, bas → yanar.
- S3 (3 sn): devrenin genel görüntüsü.

## Üretim (Reel aracı)
`python tools/reel.py projects/01-sos-beacon` → `projects/01-sos-beacon/build/reel.mp4` (1080×1920, ~20–25 sn, müzik + yazı, seslendirme yok).
Sahne listesi her projenin `reel.json` dosyasında (çekim parçaları, kod kartları, ekran yazıları). Çekim dosyası yoksa yer tutucu kart çıkar;
çekimler `footage/projects/NN/` klasörüne konunca aynı komut gerçek videoyu üretir (~5 dk). Instagram ve YouTube Short için aynı dosya.
