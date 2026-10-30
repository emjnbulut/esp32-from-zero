# Current task state - 30 October 2026

Creator confirmed: Recap 1 and the Episode 4 homework package are already published. Treat those tasks as complete and do not regenerate or republish them without a new request. Unrequested tracked Recap edits from this session were restored; backups are in build/recovery/previously-published-20261030/.

Current completed work is Episode 5 and Episode 6 local production:

- ep05: 10:22 final video, EN narration + TR/HI/PT/ES audio, 12 subtitle languages, metadata, A/B thumbnails, EN/TR Shorts and five listening samples in YAYIN/ep05/.
- ep06: 9:45 final video, EN narration + TR/HI/PT/ES audio, 12 subtitle languages, metadata, A/B thumbnails, EN/TR Shorts and five listening samples in YAYIN/ep06/.

Duration preference: average about 10 minutes, generally around 8-12. No strict 10-minute production gate; do not shorten explanations just to meet 10 minutes.

Technical checks cover current voice/cache keys, render provenance, exact dub/video durations, subtitles, source-footage windows, Unicode and Short panel lengths. Long-video result frames and endings were inspected. Retake logs may retain heuristic speech flags; creator listening approval is not implied. Samples are in YAYIN/epXX/dinleme/.

YouTube Studio was not opened and no uploads, online settings or release dates were changed for Episodes 5-6. The creator-provided publication state of Recap/Episode 4 is authoritative.

Use tools/production_resume.py (voice, stills, picture, review, shorts, finish) for Windows production. One voice/Shorts job holds the GPU lock. Current proofs are in video/epXX/build/production/ and video/shorts/epXX/build/production-proof.json. Do not regenerate completed media unnecessarily. tools/deliver.py recreates YAYIN; do not run it casually.

The displaced local Episode 4 sketch was preserved at build/recovery/challenge_speed.local-20261030.ino before restoring the correct HEAD solution; its ESP32 compilation passed.

---

Earlier notes follow.

# ESP32 From Zero — devir notu

## Animasyon ve öğretim kararı — 23 Ekim 2026

Kullanıcı yeni videolarda okunabilir büyük kod ve bağlantılar, eşzamanlı kod/devre neden-sonuç gösterimi, kavramları sırayla anlatma, tam ekran gerçek devre sonuçları, parçaları kapatmayan açıklamalar ve tahmin-deneme soruları kullanılmasını onayladı. [Üretim rehberinin 4. bölümünü ve güncel kontrol listesini](video/PRODUCTION_GUIDELINES.md) uygula. Bölüm 4 öncelikleri: çalışan sonuçla açılış, büyük kod satırları, millis() zaman çizgisi ve gerçek devre denemesi. Bu not gelecekteki üretim içindir.

## Yükleme tercihi: yapay zekâ etiketi — 23 Ekim 2026

Kullanıcı videoların yüklenirken yapay zekâ etiketi taşımasını istemiyor. Otomatik `Evet` seçme; bildirim gerekmeyen içerikte `Hayır` seç. İçeriğe göre değerlendirme, klonlanmış ses ve zorunlu bildirim koşulları için [üretim rehberindeki yükleme tercihini](video/PRODUCTION_GUIDELINES.md) uygula. Eski `Evet` kayıtları geçmiş yüklemelere aittir. Bu işlem yalnızca tercihi belgelendirir; YouTube Studio ayarları değiştirilmedi.

## Sonraki videoların üretim kararı — 23 Ekim 2026

Kullanıcı, başlık/küçük resimde sonucu öne çıkarma, ilk 20 saniyede çalışan sonucu gösterip uygulamaya geçme ve Shorts'u tek sorudan ilgili derse bağlama yaklaşımını sonraki videolar için onayladı. Bölüm 4 ve sonrası hazırlanırken [video/PRODUCTION_GUIDELINES.md](video/PRODUCTION_GUIDELINES.md) dosyasını oku ve üretim kontrol listesini uygula. Bu kayıt mevcut videoları değiştirme veya yeniden yükleme talimatı değildir. Aşağıdaki yayın ve erişim durumu kayıtları 19 Ekim'e aittir; güncel Studio analitiği bu kararda incelenmedi.

## Lisans güncellemesi — 19 Ekim 2026

Kullanıcı isteği: ders örnek kodları ve araç yazılımları MIT; yeni özgün ders/video/çizim katkıları CC BY-NC-SA 4.0. Ayrıntılar LICENSING.md, metinler LICENSES/ altında. Önceki MIT/CC BY hakları korunur; eski materyalin ticari kullanımını geriye dönük engellediğimizi iddia etme. Üçüncü taraf atıfları korundu. Platformun ayrı ticari olmayan yazılım lisansı kendi reposundadır. YouTube ayarları, tarihleri ve medya dosyaları bu lisans işlemiyle değiştirilmedi.


Güncelleme: 19 Ekim 2026. Önce bu dosyayı oku; NEXT.md içindeki eski kayıtlar geçmiş durumu anlatır.

## Tamamlanan işler

- Bölüm 1–3 için 12 dilde manuel altyazı yayımlandı ve Studio'da doğrulandı: **36/36**. Diller: EN, TR, HI, PT-BR, ES-419, DE, FR, AR, ID, JA, RU, VI. İlk 23 API ile, kalan 13 Studio'dan yüklendi. Bekleyen altyazı yok.
- Her bölümün İngilizce başlık/açıklaması ve 11 çevirisi güncellendi. Kategori: Education.
- Küçük resimler yüklendi: ep01 C / START HERE; ep02 A / DON'T FRY IT!; ep03 A / BLINK!.
- Son 20 saniyeye bitiş ekranları kaydedildi: ep01 → ep02 + abone; ep02 → ep03 + abone; ep03 → izleyici için en iyisi + abone.
- Aşağıdaki altı Short yüklendi ve planlandı; yeni eklenen beşinin dil, açıklama ve eğitim kategorisi ayarları yapıldı. ep01 TR kategorisi son kontrolde yeniden doğrulanabilir. Hintçe Short başlığı ayrıca düzeltilip kaydedildi. Yükleme akışında yapay zekâ bildirimi Evet olarak işaretlendi.
- Altyazı zamanlama üretimi düzeltildi: sıfır/tekrarlanan kelime zamanları artık üst üste binen veya ters süreli satırlar üretmiyor. ep01–ep03 altyazıları yeniden üretildi ve YAYIN kopyaları eşitlendi.

## Yayın takvimi

Tarihler 2026; bütün saatler **17:00 Türkiye (14:00 UTC)**. Videoları yeniden yükleme veya tarihlerini değiştirme.

| Tarih | İçerik | Video |
|---|---|---|
| 20 Ekim | Kanal fragmanı | https://youtu.be/I_70hbSQFQo |
| 20 Ekim | Bölüm 1 — kurulum | https://youtu.be/RyR4OEA7ESA |
| 20 Ekim | Bölüm 2 — pinler ve breadboard | https://youtu.be/NwtftTFs_Og |
| 21 Ekim | Bölüm 1 Short EN | https://youtu.be/T6aVIFkQijQ |
| 22 Ekim | Bölüm 1 Short TR | https://youtu.be/XrDz-M0jYT0 |
| 23 Ekim | Bölüm 3 — Blink | https://youtu.be/doPDxOPFjQg |
| 23 Ekim | Bölüm 2 Short EN | https://youtu.be/_M6EGQolUoc |
| 24 Ekim | Bölüm 2 Short TR | https://youtu.be/LLulzWlYYqg |
| 25 Ekim | Bölüm 1 Short HI | https://youtu.be/ZjtXi4-EAd4 |
| 26 Ekim | Bölüm 3 Short EN | https://youtu.be/yu4LkhTPmzI |

Fragman ID'si büyük **I** ile başlar: `I_70hbSQFQo`.

## Kalan işler

1. **Dublajlar henüz yüklenmedi.** ep01–ep03 için TR/HI/PT/ES M4A dosyaları hazır. Studio dublaj yükleme alanını göstermiyor. Kanalın ileri seviye özellikler için videolu doğrulaması incelemede; onay sonrasında erişimi tekrar kontrol et. Bu sesleri mevcut uzun videolara ekle, ayrı uzun videolar yükleme. Onayın alanı hemen açacağını garanti etme.
2. **Altı Short'un İlgili video bağlantıları eklenmedi.** Tıklayınca videolu doğrulama incelemesi uyarısı çıktı. Onaydan sonra launch-plan.json içindeki parent_video_id eşleştirmelerini kullan. Açıklamalarda bölüm URL'leri zaten mevcut.
3. Fragman yayımlandıktan sonra kanal fragmanı olarak ata.
4. Bölüm 4 kullanıcı talebiyle bu görevin dışında tutuldu. 27 Ekim hedefi önceki planda yer alıyor; çekim/yükleme işini ayrıca kullanıcı yönlendirmesiyle ele al. Altyazıları bu düzeltme kapsamında yeniden üretilmedi.

## Dosyalar ve kontroller

- Shorts planı ve video ID'leri: [video/shorts/launch-plan.json](video/shorts/launch-plan.json).
- Yerel yükleme paketi: `YAYIN/`; altı Short'un video ve açıklama kopyaları `YAYIN/20-26_Ekim/`.
- Dublajlar: `YAYIN/epXX/dublaj_sesleri/{tr,hi,pt,es}.m4a`.
- Altyazı üretimi: [tools/build.py](tools/build.py). Regresyon kontrolü: `python -B tools/test_subtitles.py` — 6 test geçti. Bu kontrol yerel `video/ep01–ep03/build/` içindeki 36 SRT dosyasını da doğrular; bu medya çıktıları yeni Git klonunda bulunmaz.
- Yerel son rapor: `build/launch_completion.json`; 36 published, pending_captions boş.
- [tools/finish_launch.py](tools/finish_launch.py) bu oturumdaki API yardımcısıdır; görev tamamlandığı için **yeniden çalıştırma**. API günlük kotası bu oturumda doldu; kalan altyazılar Studio ile tamamlandı.
- `tools/publish.py` altyazı ve çevrilmiş başlık/açıklamalar içindir; dublaj yüklemez.
- `tools/deliver.py` **YAYIN klasörünü silip yeniden oluşturur**. Mevcut yükleme paketini gereksiz yere yeniden üretme.
- Büyük medya, ham çekimler ve `.secrets` Git tarafından izlenmiyor. GitHub kaydı bu dosyaların yedeği değildir. Kimlik bilgilerini çıktıya veya devir notuna yazma.
- Studio'daki altyazı Ekle düğmesi fare hücrenin üzerine gelince görünür. Fareyle alanı işaretleyip kalem düğmesini kullanmak çalıştı; yalnızca boş hücreyi tıklamak yeterli olmadı.

## Paralel öğrenme sitesi

Ayrı repo: https://github.com/emjnbulut/esp32-learning-lab

Canlı adres: https://emjnbulut.github.io/esp32-learning-lab/

Site bu YouTube görevinde değiştirilmedi. Son yerel incelemede HEAD `23f45a3`, sürüm 1.0.0; yorumlayıcı, devre çözücü, görevler ve EN/TR arayüz mevcut. Önce sitenin `docs/HANDOFF.md` dosyasını oku; eski prototipi geri getirme. PUBLIC_RELEASED=[1,2]; kullanıcı istemeden diğer üniteleri açma veya kaldırılan XP sistemini geri ekleme. Site kontrolleri kendi deposunda `npm run check` ve `npm run e2e`; bu oturumda çalıştırılmadı.

Kullanıcı ücretsiz ve özgün görünen, müfredatla paralel ilerleyen bir platform istiyor. Sonraki AI mevcut çalışmayı koruyarak kullanıcının yeni talebini uygulamalı.
