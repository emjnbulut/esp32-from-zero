# Update - 12 November 2026 ~01:00 (read first)

Episode 9 (Mini Project 1, pedestrian crossing, due Tue 17 Nov 17:00) in production: sketches, script (57 segments, lint 0), scenes, translations, Short spec and ALL narration (EN/TR/HI/PT/ES) done. Next: dub fit (+115 s stretch, targets in video/ep09/fit_targets.json) and TR term retakes. Resume from "RESUME HERE" in video/ep09/PROGRESS.md. Creator clips C0-C2 due Sun 15 Nov.
Still open from 11 Nov: Related video on the Episode 7 EN Short (after 12 Nov 22:00); after 13 Nov 17:00 Episode 8 dubs check + Episode 7 end screen -> Episode 8; Episode 8 Shorts Related video (14/15 Nov).

# Update - 11 November 2026 ~22:30 (read first)

Episode 8 SCHEDULED on YouTube (creator approved the TR listening after a TR term-line fix):
- Long video `1GYzg84mmAM` 13 Nov 17:00: title/description/chapters, playlist, not for kids, AI = No, paid = No, tags, English (US), Education, A/B thumbnail test A FILL THE BAR vs B MAP ANY RANGE (starts when public), end screen imported from Episode 7, 12 subtitles + 12 titles via publish.py (token renewed 11 Nov), 4 dubs (YAYIN/ep08/dublaj_sesleri/upload_10mb) uploaded and processing.
- Shorts: TR `8EHI3o4kzm4` 14 Nov 17:00 (now with TURKISH on-screen text, new rule), EN `_wA8rWprwOg` 15 Nov 22:00; descriptions link Episode 8.
- TR dub fix 11 Nov: s01 s10 s16 s25b s30 s33 s34 re-narrated (creator heard bad terms at 50-55 s / 65-70 s of the sample); s16/s30/s34 sped up 1.04-1.05 to fit.
- Done 11 Nov: Episode 7 dubs confirmed; Episode 6 end screen -> Episode 7; Related video on Episode 7 TR Short.

Still to do by hand:
- After 12 Nov 22:00: Related video on Episode 7 EN Short `FBHKjGb1iJg`.
- After 13 Nov 17:00: confirm the 4 Episode 8 dubs; point the Episode 7 end screen at Episode 8.
- After 14 Nov 17:00 / 15 Nov 22:00: Related video on the Episode 8 TR / EN Shorts.
- New rule (creator 11 Nov): TR-dub Shorts get Turkish on-screen text (short.json tr values for chip/headline/show/cta).

# Update - 9 November 2026 ~23:00 (read first)

Episode 8 BUILT and packaged in YAYIN/ep08 (final 9:53 with bumpers, 4 dubs + upload_10mb, 12 subtitles, 12 descriptions, thumbnails A/B, Shorts EN/TR + upload_10mb, dinleme/). Dub fit: 85 HI/PT/ES lines shortened in two passes, timeline stretch 107 s -> 24.5 s. Waiting for the creator's listening approval (YAYIN/ep08/dinleme), then upload: long video 13 Nov 17:00, TR Short 14 Nov 17:00, EN Short 15 Nov 22:00 (Short texts: video/shorts/ep08/youtube.md, add the Episode 8 link). API token expires about 11 Nov: `publish.py auth` first.
Done 9 Nov: Related video set on Episode 6 TR and EN Shorts. Studio opened on the personal channel: switch account to Pin by Pin Lab first.
Still open: Episode 7 goes public 10 Nov 17:00 (confirm dubs, point the Episode 6 end screen at it); Related video on the Episode 7 Shorts after 11/12 Nov.
tools/dub.py now saves its narration cache every 10 lines (an interrupted run resumes).

# Update - 8 November 2026 ~22:50 (read first)

Episode 8 "map(), Dimmer Knobs and Level Bars" (due Fri 13 Nov 17:00) is in production: script, scenes, clips (tall knob+LED crops in footage/ep08), translations, metadata, thumbnails, Short spec and EN/TR/HI/PT narration are done. The build chain was cut at the ES narration when the session closed. Resume from "RESUME HERE" in video/ep08/PROGRESS.md.
Still open from 7 Nov: Episode 7 goes public 10 Nov 17:00 (confirm dubs, point the Episode 6 end screen at it); Related video on the Episode 6 EN Short (after 8 Nov 22:00) and Episode 7 Shorts (11/12 Nov); Instagram Episode 5 EN Short status unknown.

# Update - 7 November 2026 ~01:20 (read first)

Episode 7 SCHEDULED on YouTube (creator approved all listening samples + TR flagged lines by ear):
- Long video `g-fnxcOIyBI` 10 Nov 17:00: title/description/chapters, playlist, not for kids, AI = No, paid = No (Claude now ticks these itself, creator's request), tags, English, Education, A/B thumbnail test A TURN IT UP vs B READ A KNOB (shows "Uygun değil" until public), end screen imported from Episode 6 (subscribe + best for viewer + playlist), 12 subtitles + 12 titles via publish.py, 4 dubs (YAYIN/ep07/dublaj_sesleri/upload_10mb, 96k mono) uploaded and processing.
- Shorts: TR `nNUZynx55B4` 11 Nov 17:00, EN `FBHKjGb1iJg` 12 Nov 22:00 (descriptions link Episode 7).

Still to do by hand:
- 7 Nov 19:00 Instagram: Episode 5 EN Short. Episode 4 solution Short still needs a date.
- Related video: all 11 public Shorts checked 7 Nov ~01:40, all set (Episode 5 EN `SBtl26Fyf1o` fixed then). Still to do: Episode 6 TR `IDsdn3uqmas` (after 7 Nov 17:00) and EN `7mauqKSjls8` (after 8 Nov 22:00); Episode 7 Shorts after 11/12 Nov.
- After 10 Nov 17:00: confirm the 4 Episode 7 dubs; point the Episode 6 end screen at Episode 7. Check Episode 6 dubs + Episode 5 end screen -> Episode 6 (pending since 6 Nov).
- Narration rule from the Episode 7 listening (guidelines sec. 9): no stacked spoken numbers/acronyms from Episode 8 on.
- API token (.secrets/token.json, 4 Nov) expires around 11 Nov: run `publish.py auth` before Episode 8 subtitles.

Studio automation notes: in the Languages dialog the audio Ekle opens a sub-dialog whose file input only takes the file on the second file_upload try (check the dialog text shows the filename), then Yayınla, then Güncelle. Screenshots can time out while the tab is busy; JS reads still work.

# Update - 6 November 2026 03:15 (read first)

Episode 7 BUILT, not uploaded: YAYIN/ep07 (ep07_final.mp4 11:16 with bumpers, 4 dubs, 12 subtitles, 12 descriptions, thumbnails A/B, shorts/ + shorts/upload_10mb, dinleme/). Details in video/ep07/PROGRESS.md. Waiting for the creator's listening approval (dinleme/ samples + ep07_tr_flagged.mp3), then upload: long video 10 Nov 17:00, TR Short 11 Nov 17:00, EN Short 12 Nov 22:00.

Dub length lesson (ep07): Chatterbox HI/PT/ES takes ran far longer than their character ratio predicted (char ratio <= 1.08, audio +63-99 s per language). Fit dub texts from measured take durations against max(EN, TR) x 1.05, then re-narrate; two passes took the timeline from 760 s to 652.9 s.

Not done on 5 Nov (Chrome extension was not connected): Related video on the Episode 5 EN Short `SBtl26Fyf1o`.

# Update - 4 November 2026 15:50 (replaces the matching items below)

SCHEDULED on YouTube: Episode 6 `j0tZ9P7YrU8` 6 Nov 17:00 (12 subtitles + titles via publish.py, 4 dubs uploaded and processing at 15:45, end screen best for viewer + playlist + subscribe, playlist card 0:27, A/B thumbnail test A ANY COLOR vs B MIX LIGHT saved). Shorts: TR `IDsdn3uqmas` 7 Nov 17:00, EN `7mauqKSjls8` 8 Nov 22:00.

Episode 6 TR dub: s23 and s36 re-narrated with the spelling "skeç" (the engine cannot say "İşte sketçin", every seed came out as "Disketçin"); the creator approved by ear. Episode 5 and later TR lines with "sketçin" may have the same fault. The picture proof (production_resume verify) now reports stale because source_hash covers dub/tr.json; the picture did not change, do not re-render for this.

Still to do by hand (timed jobs die with the session):
- Related video: Episode 5 TR Short `mJjP6nf-5IQ` is done (seen in Studio 5 Nov). 5 Nov after 22:00: on EN Short `SBtl26Fyf1o`; 7 and 8 Nov: on the Episode 6 Shorts.
- Instagram: the 3 and 4 Nov slots were missed. 5 Nov: Episode 4 EN Short posted (video/shorts/ep04/build/en/ep04_short_en.mp4, AI label off, own-voice narration named in the caption). Still to post: Episode 4 solution Short (YAYIN/shorts_ep04c/ep04c_short_en.mp4, new date needed), 7 Nov 19:00 Episode 5 EN Short.
- After 6 Nov 17:00: confirm the 4 dubs, point the Episode 5 end screen at Episode 6.
- Episode 7 not started (due 10 Nov). Episode 5 first 21 h: 52 views, 280 impressions, CTR 2.9%, avg 2:01 (19%); retention still "not enough data", bring it to the creator before the Episode 7 script.

Studio automation: the permission system blocks some final clicks (Save on a public video's end screen, Planla), so the creator presses those, and the AI + paid-promotion radios. Language dialog: there are two file inputs; the first is the thumbnail, the second is the audio. Do not chain blind clicks over a failed upload.

Done before this: Episode 4 and Recap 1 end screens now point at Episode 5. tools/short.py overlay cache fixed (stamp after a finished render).

# Open work - 3 November 2026, session closed about 02:00

Scheduled on YouTube, nothing more needed: Episode 5 `VaqdZeV5tRQ` 3 Nov 17:00, TR Short `mJjP6nf-5IQ` 4 Nov 17:00, EN Short `SBtl26Fyf1o` 5 Nov 22:00.

Timed jobs were session-only and ended with the session. Do these by hand:
- After 3 Nov 17:00: confirm Episode 5 is public and its 4 dubs finished; check the thumbnail A/B test runs (it said "not public" before release); point the Episode 4 and Recap 1 end screens at Episode 5.
- Instagram, one Reel per slot, plan approved by the creator: 3 Nov 19:00 Episode 4 EN Short (video/shorts/ep04/build/en), 4 Nov 19:00 Episode 4 solution Short (YAYIN/shorts_ep04c), 7 Nov 19:00 Episode 5 EN Short (YAYIN/ep05/shorts/upload_10mb). Instagram web cannot schedule.
- After 4 Nov 17:00 and 5 Nov 22:00: set Related video on the Episode 5 TR and EN Shorts.

Episode 6, not uploaded, due 6 Nov 17:00. The long video and new titles are in YAYIN/ep06. Its Short has a new opening in video/shorts/ep06/short.json, but the rebuild was stopped by the creator before it finished: the Short mp4 files, including YAYIN/ep06/shorts/upload_10mb, are STILL THE OLD OPENING. Rebuild EN then TR with `tools/production_resume.py shorts ep06`, check the frames, make the under-10 MB copies, and only then upload.

Studio tip: enter a video from the channel content list and click its title; opening /video/ID/edit by URL leaves the pickers empty. Channel-data rules: video/PRODUCTION_GUIDELINES.md section 11. Episode 7 not started (due 10 Nov); check Episode 5 retention at 0:30-1:30 and bring the result to the creator before its script.

---

# Current state - 3 November 2026

Episodes 5 and 6 were reviewed end to end and rebuilt (see the top of video/ep05/PROGRESS.md and video/ep06/PROGRESS.md). Nothing was uploaded in that session; whether Episode 5 or 6 is already in Studio was not verified (extension not connected, API token expired). Upload from YAYIN/epXX, with the upload_10mb copies for dubs and Shorts. Episode 5 is due 3 Nov 17:00.

---

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
