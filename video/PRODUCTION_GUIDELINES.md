# Latest creator decision - 30 October 2026

The creator clarified the target: average about 10 minutes, generally around 8-12 minutes. This is an approximate pacing target. Do not shorten narration or regenerate voices merely to stay below 10 minutes. Prioritize clear, complete explanations and natural speech. Earlier 6-9-minute targets and strict 10-minute limits in this document are superseded by this decision.

# Sonraki videolar için üretim kuralları

Kullanıcı kararı: 23 Ekim 2026. Bölüm 4 ve sonraki yeni videolarda uygulanır.
Bu karar gelecekteki üretim içindir; yayımlanmış veya planlanmış videoların başlıklarını, küçük resimlerini, dosyalarını veya yayın tarihlerini değiştirme talimatı değildir.

## 1. Başlık ve küçük resim: sonucu öne çıkar

- Başlık, izleyicinin yapacağı işi veya çözeceği sorunu açıkça söylesin. ESP32 ve konuyla ilgili arama terimleri doğal biçimde yer alsın.
- Seri adı ve bölüm numarası kullanılacaksa başlığın sonuna gelsin; asıl faydayı geriye itmesin.
- Küçük resimde tek görsel odak kullan: gerçek ESP32 kartı, çalışan devre veya bölümün somut sonucu. Mobil ekranda okunabilen 2–3 kelimelik metin tercih et.
- Başlık ve küçük resim birbirini tamamlasın; videoda gösterilmeyen sonuç veya doğrulanmamış süre vaat etmesin.
- Bölüm 4 için taslak örnek: `ESP32 Buttons & millis(): Blink LEDs Without Blocking` ve `DO BOTH`. Görselde buton ile çalışan LED'ler öne çıkar. Bu bir üretim örneğidir; hazırlanmış veya yayımlanmış başlık değildir.

## 2. Açılış: önce çalışan sonucu göster

Hedef açılış düzeni:

| Süre | İçerik |
|---|---|
| 0–5 saniye | Gerçek devre, Serial Monitor veya bölümün çalışan sonucunu göster. |
| 5–12 saniye | İzleyicinin bölüm sonunda ne yapacağını tek cümleyle anlat. |
| 12–20 saniye | Gerekli parçaları kısaca göster ve ilk uygulama adımına geç. |

- Açılışın önüne uzun logo animasyonu, genel hoş geldiniz konuşması, önceki bölüm özeti veya abonelik çağrısı koyma.
- Her bölümün ilk saniyeleri kendi başına anlaşılır olsun; başlık ve küçük resmin verdiği sözü hemen desteklesin.
- İngilizce anlatım ve mevcut çeviri düzeni korunur. Yeni açılışı diğer dil metinlerine, altyazılara ve zamanlamaya da işle.
- Bölüm 4 için taslak açılış: `This LED keeps blinking while the button controls the other one. Let's make both work together using millis().` İki davranışı aynı gerçek devre görüntüsünde göster.
- Bu anlatım düzeni mevcut müfredatın sırasını ve yalnızca öğretilmiş kavramlarla alıştırma yapma kuralını değiştirmez.

## 3. Shorts: tek soru, tek kazanım, ilgili ders

- Her Short tek bir soruyu, hatayı veya küçük sonucu ele alsın ve kendi içinde faydalı bir cevap versin.
- İlk saniyelerde sorunu veya sonucu göster; sonunda tam dersin sağlayacağı ek faydayı tek cümleyle söyle.
- Örnek geçiş: `Build the full circuit step by step in the linked lesson.`
- Studio'daki `İlgili video / Related video` alanını doğru ana bölüme bağla ve kaydettikten sonra doğrula. Açıklamadaki URL bunun yerine geçmez; Shorts açıklamalarındaki URL'ler tıklanabilir değildir.
- İleri seviye özellik erişimi yoksa bu adımı bekleyen iş olarak kaydet; bağlantıyı tamamlanmış sayma. Ana bölüm kimliğini yayın planında tut.
- Short'un dili ile bağlı dersin kullanılabilir ses/altyazı seçeneklerini kontrol et. Henüz yüklenmemiş dublajı varmış gibi tanıtma.
- Bölüm 4 için örnek soru: `Why does your button stop responding during delay()?` Sorunu göster, millis() ile çalışan sonucu göster ve tam derse yönlendir.
- Müfredattaki alıştırma çözümü Shorts'ları da bu yapıyı izler; öğretilmemiş sözdizimi veya donanım tekniği gerektirmez.

## 4. Animasyon ve öğretim yaklaşımı — 23 Ekim 2026

Kullanıcı bu önerileri yeni videolar üretilirken dikkate almak üzere onayladı. Mevcut koyu zemin, tutarlı renkler, breadboard iç bağlantıları ve konuşulan satırı vurgulama yaklaşımı korunarak geliştirilir. Bu karar mevcut videoları yeniden üretme talimatı değildir.

### Okunabilir kod ve bağlantılar

- Kod açıklanırken ilgili 3–6 satırı büyük göster. IDE'nin tamamını menü, yükleme veya çalışma ortamını tanıtırken kullan.
- Bağlantıda önce devrenin tamamını göster, ardından hedef pin ve breadboard deliğine yakınlaş. GPIO etiketi, delik ve kablonun varış noktası telefon ekranında da ayırt edilebilsin.
- Her sahnede tek ana odak olsun: bir bağlantı, bir kod satırı veya bir davranış. Açıklama kutuları anlatılan parçayı kapatmasın; sorun giderme sırasında ilgili parçanın yanına yerleşsin.

### Koddan devredeki sonuca

- Animasyonlar anlatımla eşzamanlı olarak neden-sonuç ilişkisini göstersin. Örnek: `digitalWrite(LED_PIN, HIGH)` satırı vurgulanır, GPIO'da `HIGH / 3.3 V` gösterilir, bağlantı yolu vurgulanır ve LED yanar.
- `millis()` anlatımında yalnızca büyüyen sayaç gösterme; `now`, `lastBlink` ve geçen süreyi ilişkilendir. 499 ms'de koşulun sağlanmadığını, 500 ms'de LED'in değiştiğini ve `lastBlink = now` ile yeni aralığın başladığını göster.
- Görseldeki durumlar çalışan kodla tutarlı olsun. Animasyonun hareketi öğretilen kavramı açıklasın.

### Yeni kavramları sırayla ver

- Aynı anda çok sayıda yeni sözdizimi ve durum değişimi sunma. Buton örneğinde önce yeni basışı algılamayı, sonra LED durumunu değiştirmeyi, ardından kısa yazımı açıkla.
- İlk anlatımda açık `if/else` kullan; `?:` gibi eşdeğer kısa yazımı daha sonra göster. `bool`, `!`, kenar algılama ve koşullu ifadeleri ayrı adımlarda tanıt.
- Müfredattaki yalnızca öğretilmiş kavramlarla alıştırma yapma kuralını koru.

### Gerçek devreyle bağ kur

- Uygun kavramlarda şu akışı kullan: gerçek devre, açıklayıcı çizim, ilgili kod, yeniden gerçek devrede deneme.
- Sonuç gösterilirken gerçek çekime tam ekran alan ver; devrenin davranışını küçük bir pencereye sıkıştırma.
- Çizimdeki kart yönü, kablo renkleri ve bağlantılar gerçek çekimle eşleşsin. Gerekli çekimleri senaryo aşamasında çekim listesine ekle.

### Tahmin et, dene, değiştir

- Önemli kavramlardan sonra kısa bir tahmin sorusu sor, yaklaşık 2–3 saniye düşünme payı bırak ve sonucu göster.
- Örnekler: İki bekleme süresi farklı olursa ne değişir? Butonu basılı tutunca LED sürekli değişir mi? Bir LED'in süresi değişince diğeri etkilenir mi?
- Bölüm sonunda kısa özete ek olarak yalnızca öğretilmiş bilgilerle yapılabilecek küçük bir değişiklik görevi ver; mevcut müfredat alıştırmasını bu amaçla kullan.

### Bölüm 4 için ilk uygulama öncelikleri

Çalışan sonuçla açılış, büyük kod satırları, `millis()` için görünür zaman çizgisi ve tam ekran gerçek devre denemesi. Değerlendirme Bölüm 2–4'ten 18 örnek kare ve senaryo incelemesine dayanır; baştan sona ses/müzik değerlendirmesi veya ölçülmüş öğrenme sonucu değildir.

## 5. Beğen / abone ol hatırlatmaları ve kapanış — 25 Ekim 2026

Kullanıcı kararı: Bölüm 05 ve sonrasındaki yeni videolarda uygulanır (Bölüm 04 olduğu gibi kalır).

- Animasyonların arasına **küçük ve sade** beğen 👍 / abone ol 🔔 ikonları eklenir; dikkat dağıtmaz, göz boyamaz.
  - Bölüm başına en fazla 2 kez: biri ilk çalışan sonuçtan hemen sonra (~1. dakika), biri bölümün ortasında, bir "oldu!" anının ardından.
  - Ekranın köşesinde, yaklaşık 2–3 saniye, hafif bir giriş/çıkış animasyonuyla; kodu, devreyi veya açıklama kutularını kapatmaz. Ses efekti ve yanıp sönme yok.
  - Anlatımda ayrıca "abone olun" denmez; ikon kendi başına yeterli.
- Her bölümün sonunda anlatım izleyiciyi yorumlara davet eder; örnek: "Let's meet in the comments: tell me what you built." Ödevli bölümlerde ödev çözümleri için de yorumlara çağrılır.
- Shorts'a bu ikonlar konmaz (kısa ve tek odaklı kalır); kapanış cümlesi yine ilgili derse yönlendirir.

## 6. Dublaj ile altyazı aynı ve hizalı — 25 Ekim 2026

Kullanıcı kararı: bir dilin dublaj diyaloğu ile o dilin altyazısı **aynı cümleler** olmalı ve **birlikte akmalı**.
- Tek kaynak: her dilin metni bir kez yazılır. Altyazı bu metnin okunur hâlidir (rakamlar, kod adları), dublaj aynı
  kelimelerin sese uygun yazımıdır (TR'de sayıların okunuşu, İngilizce terimlerin Türkçe telaffuzu). Dublaj metninde
  kelime değiştirmek, kısaltmak, yeniden cümle kurmak yok; satır sığmıyorsa **iki metin birlikte** değiştirilir.
- Zamanlama: dublaj her bölümün (segment) İngilizce başlangıcına oturur; altyazı satırları da aynı segment
  sınırlarında kalır, böylece ses ve yazı birlikte ilerler.
- Kontrol: yayından önce her dublaj dili için metin karşılaştırması (altyazı ↔ dublaj) çalıştırılır.

## 7. Her kodun tam hali ekranda — 27 Ekim 2026

Kullanıcı kararı: anlatımdaki büyük 3–6 satırlık kod kartları kalır; ayrıca her kod dosyasının gerçek sonuç çekiminden hemen sonra **~4,5 saniyelik "FULL CODE" kartı** gelir. Kart dosyanın tamamını (baştaki açıklama satırları hariç) bir ya da iki sütunda, sığacak boyutta gösterir; köşede "pause to read", altta GitHub yolu yazar. Motor: `fullCode()` (`video/engine/lib.js`), kodlar `node tools/sketches.mjs epXX <ders-klasörü>` ile `epXX/sketches.js` dosyasına toplanır. İlgili segmente `make_script.py` içinde +4,5 s `pad` eklenir; sonuç çekiminin bitişi kart kadar öne alınır. Ödev çözümleri gösterilmez. Bölüm 4 ilk uygulamadır; Bölüm 5 ve sonrası aynı şekilde yapılır.

**Kod turu (27 Ekim 2026, kullanıcı: "kodlar kafa karıştırıcı olmaya başladı"):** Bölüm 5'ten itibaren her ana kodun sonuç çekiminden hemen önce 20–45 sn'lik bir **kod turu** gelir: tam kod ekranda (`fullCode` + `marks`), anlatıcı sırayla değişkenleri, setup'ı ve loop'un kısımlarını anlatır; anlatılan satırlar vurgulanır, yazı küçükse kamera o satırlara yaklaşır. Kod turu olan kodda ayrı tam kod kartı gerekmez. Kod dosyalarındaki yorumlar sade dille her bloğu açıklar ("What it does" özeti + PART 1 / PART 2 başlıkları); ders sayfasında her kodun tamamı ve "Line by line" tablosu bulunur. Yeni segmentler mevcut kimlikleri değiştirmez (`s11t1` gibi), böylece hazır seslendirmeler korunur.

## 8. Bir bölüm = bir konu + pratik, ~10 dk — 27 Ekim 2026

Kullanıcı kararı ("kodlama kısmı kafa karıştırıcı", izleyici gözüyle): bölüm 6'dan itibaren her bölüm **tek bir yeni konu** öğretir, kalan süre o konunun **pratiği** olur; hedef süre **yaklaşık 10 dk**. Bölüm 4–5'teki "iki konu" biçimi (27 Ekim'e kadar) bırakıldı; yayınlanmış/hazır bölümler (04, 05) olduğu gibi kalır.
- Yapı: açılış sonucu → konunun sade anlatımı (önce kodsuz, tek cümle) → kodu **parça parça büyüt** (3 satırlık çalışan sürüm, sonuç, sonra bir satır ekle) → pratik (önceki bilgilerle küçük görevler) → alıştırma.
- Zor fikir en fazla 1 tane; ikinci yarıda yeni mantık değil, bilinenlerin birleşmesi öğretilir.
- Kodun önemli değişkenleri anlatım sırasında ekranda "şu an" kutusunda canlı gösterilir (ör. `brightness = 128, step = +1`).
- Kontrol: `python tools/lesson_lint.py epXX` senaryo aşamasında çalıştırılır; uyarılar ses üretilmeden önce giderilir.

## 9. Anlatım: insan gibi, günlük örneklerle, nefes alarak — 28 Ekim 2026

Kullanıcı kararı (Recap TR dublajını dinledikten sonra): "konuyu çok kötü anlatıyor; noktalama ve nefese dikkat etmediği için her şey karman çorman; terimlere boğup geçiyor; daha açıklayıcı, insan gibi, günlük hayattan bol örnekle anlatsın". Bütün dillerde geçerli. **Recap ve Bölüm 05'ten itibaren** uygulanır (05 yayından önce yeniden yazılır); yayımlanmış 01–04 olduğu gibi kalır.

Ölçülen sorun (Recap, 28 Ekim): İngilizce konuşma hızı ~198 kelime/dk (hece 4,5/sn, tek satırlarda 5,6); Türkçe satırdan satıra 106–217 kelime/dk savruluyor; Hindi dublajda 24 yerde cümle ortasında >1 sn takılma; HI/PT/ES dublajlar yerleştirilirken 1,2× hızlandırılıyordu. Cümle sonu duraklaması sabit 0,32 sn, virgül 0,12 sn idi.

**Metin**
- Her yeni fikir **önce günlük hayattan bir örnekle** gelir, sonra adı (terim), sonra kod. Aynı örnek kod izlenirken yeniden anılır ("skor tabelası gibi"). Her bölüm kısmında en az bir örnek; ekranda emoji + kısa karşılık kartıyla gösterilir.
- **Benzetmeden hemen sonra nesnel tanım** (kullanıcı, 28 Ekim: "terimlerin gerçekten ne işe yaradığını nesnel anlamda da bilmeleri gerek"): "Gerçekte olan şu: …" / "Teknik olarak …" diye başlayan 1–2 cümle, terimin kartta/kodda gerçekte ne yaptığını söyler (ör. değişken = hafızada adı olan yer; `INPUT_PULLUP` = çipin içindeki direnç pini 3,3 V'a çeker; `delay(500)` = program 500 ms durur, hiçbir satır çalışmaz; `loop` dışında tanımlanan kutu değerini korur, içindeki her turda yeniden oluşur). Kod işaretleri (`==`, `!=`, `!`, `++`, `&&`, `? :`) ilk geçtikleri yerde anlamıyla söylenir. Benzetme tek başına bırakılmaz.
- Bir cümlede en fazla bir yeni terim; terimden hemen sonra sade anlamı.
- Konuşmada kod adları zincirlenmez: "state LOW, lastState HIGH" yerine "şu anki okuma LOW, bir önceki okuma HIGH". Kod adı ekranda yazılı kalır, anlatıcı ne anlama geldiğini söyler.
- Telgraf cümlesi yok ("Yazdır. Bekle."): tam, konuşma dilinde cümleler; izleyiciye "siz" diye hitap, küçük geçişler ("Peki neden?", "Şimdi bir turu izleyelim").
- Her dilin metni o dilde **doğal** yazılır, çeviri kokmaz. Dublaj ve altyazı aynı cümlelerdir (bölüm 6).
- Daha fazla açıklama süre ister: kullanıcı (28 Ekim) "uzunluk sorun değil" dedi. Bölüm 8'deki ~10 dk hedefi açıklama için aşılabilir; konu bölünmez, ama gereksiz tekrar da yapılmaz (Recap ~15–16 dk).

**Ses (tools/cbx.py, tools/chatterbox_say.py)**
- Duraklama noktalamaya göre: nokta 0,5 sn, soru 0,7 sn, iki nokta 0,35 sn, virgül 0,22 sn (0,6/0,28 denendi: kullanıcı "çok yavaş" dedi).
- Ses **asla zaman germe (time-stretch) ile yavaşlatılmaz**: 28 Ekim'de rubberband ile %15'e kadar yavaşlatma denendi, kullanıcı "çok yavaş ve robot gibi, ses tonu değişti" dedi. Hız farkı olan satırlar yeniden seslendirilir (`cbx_retake.py`: bölüm ortalamasının 0,85–1,18 katı dışındaki satırlar). `MAX_SPS` yalnızca raporda aykırı satırı gösterir.
- Dublajlar **hızlandırılmaz** (en çok %3): bir dil uzun sürerse görüntü onu bekler (`build.py schedule`). Bu yüzden önce bütün dillerin dublajı seslendirilir, sonra zamanlama ve render.
- Kontrol: `python tools/pace_check.py video/<ep>` her dilde hece hızı, satırlar arası savrulma ve takılmaları gösterir. Kullanıcıya her dilden kısa dinleme örneği verilmeden "bitti" denmez.

## 10. Kanıta dayalı ders tasarımı — 28 Ekim 2026 (Bölüm 05'ten itibaren)

Kullanıcı kararı: eğitim araştırmalarıyla karşılaştırmada (kaynaklar bölüm sonunda) eksik çıkan her şey **Bölüm 05'ten itibaren** uygulanır, video uzunluğu dahil. Recap 1 (v3) olduğu gibi kalır. Bölüm 8 ve 9'daki kurallar geçerliliğini korur; çelişirse bu bölüm geçerlidir.

**Uzunluk ve bölme** (Guo vd. 2014: izlenme ~6 dk'dan sonra azalıyor, 9–12 dk arasında sert düşüyor; Mayer: parçalara bölme)
- Bir video **6–9 dk** hedeflenir, **en fazla 10 dk** (açılış ve kapanış bumper'ları hariç). Sığmayan konu art arda **iki ayrı bölüme** yayılır (v6, kullanıcı 29 Eki: "1. kısım 2. kısım yerine hepsini ayrı bölüme ayıralım"; ör. Bölüm 5 PWM, Bölüm 6 RGB). Her bölüm kendi açılış sonucu, hatırlatma dakikası, kapanışı ve **kendi Short'u** ile tek başına izlenebilir; ödev, konunun ikinci bölümünün sonunda.
- Video içi parçalar 2–3 dk'dır (YouTube bölüm başlıkları). **En geç 3 dakikada bir** soru ya da tahmin molası olur (Szpunar vd. 2013: ara sorular dikkat dağılmasını yarıya indirir).

**Her videonun iskeleti**
1. 0–15 sn açılış: gerçek sonuç ve söz (bölüm 2) → sting.
2. **Hatırlatma dakikası** (30–45 sn): önceki bölümlerden 2 kısa soru, düşünme payı, cevap (aralıklı tekrar + kendini sınama: Dunlosky vd. 2013'te en yüksek fayda alan iki teknik).
3. Her yeni kavram: günlük örnek → nesnel anlam (bölüm 9) → **benzetmenin sınırı**, tek cümle: "Farkı şu: …" (Glynn'in benzetmeyle öğretme modelinin 5. adımı) → kod.
4. Her kod **PRIMM** sırasıyla: **Tahmin** (çalıştırmadan önce "sizce ne olacak?") → **Çalıştır** (gerçek çekim) → **İncele** (kod turu ya da canlı izleme; içinde 2–3 "durdurun: bu satırdan sonra ne olur?" molası, Naps vd. 2002) → **Değiştir** ("şu tek sayıyı değiştirin, ne olur?" sorusu + aynı görev Learning Lab'da). **Yap** = Kısım 2'deki ödev.
5. Videoda bir **yaygın hata** gösterimi: yanlış kod/bağlantı → neden olur → doğrusu (ör. `=` ile `==`, ters takılan LED).
6. Bir **kendi cümlenizle açıklayın** daveti: "Durdurun ve … neden … olduğunu kendi cümlenizle söyleyin."
7. Kapanış: 3 maddelik "artık şunları yapabilirsiniz" listesi (ekranda), Kısım 2'de ödev, yorumlara davet.

**Benzetmeler**: her kavramın tek bir benzetmesi vardır ve seri boyunca aynı kalır (`video/ANALOGIES.md`). Aynı benzetme iki farklı kavrama verilmez. Değişken: "etiketli kutu, ama aynı anda yalnızca **bir** değer tutar; yeni değer eskisini siler" (Hermans vd. 2018: kutu benzetmesi "kutuda birden çok değer olabilir" yanılgısını besliyor).

**Müzik** (Mayer tutarlılık ilkesi: öğrenmeye katkısı olmayan sesler çıkarılmalı): anlatım ve kod sırasında müzik **yok**. Müzik yalnızca açılış sonucunda, tam ekran gerçek çekimlerde ve kapanışta çalar (`script.json "music": "results"`, tools/music.py pencereleri). Sting ve bitiş ekranı eskisi gibi.

**Desteği azaltma** (uzmanlık tersine dönme etkisi, Kalyuga vd. 2003; adım adım azaltılan örnekler, Renkl & Atkinson; Salden vd. 2010): 05–07 tam çözümlü örnek + Learning Lab'da yarım kalmış kodu tamamlama; 09'dan (1. mini proje) itibaren önce "durdurun ve kendiniz deneyin", sonra çözüm; 10'dan itibaren kod turları kısalır, tahmin soruları artar. Learning Lab'a satır sıralama (Parsons) görevleri eklenir (Ericson vd. 2023: sıfırdan yazmaktan hızlı, öğrenme kazancı aynı).

**Tekrar videoları** (aralıklı tekrar): müfredat v6'da Recap 1 (01–04) hazır; Recap 2 → Bölüm 10'dan sonra, Recap 3 → 18'den sonra, Recap 4 → 24'ten sonra (`video/YAYIN_TAKVIMI.md`). Recap'ler de 10 dk sınırına uyar (gerekirse iki kısım).

**Ses** (Guo vd.: hevesli, akıcı anlatım ilgiyi artırır; Craig & Schroeder: modern sentetik ses insan sesi kadar iyi öğretir, eski "robot" ses daha kötü): doğal hız, işlemle yavaşlatma yok (bölüm 9).

**Kontrol**: `python tools/lesson_lint.py epXX` senaryo aşamasında: LENGTH (tahmini süre > 10 dk), QGAP (iki soru arası > 3 dk), RETRIEVAL (hatırlatma dakikası yok), LIMIT (benzetmenin sınırı söylenmemiş), PREDICT (kod turunda tahmin molası yok), MISTAKE (yaygın hata gösterimi yok), EXPLAIN (kendi cümlenle açıkla daveti yok).

**Kaynaklar (28 Ekim 2026 araştırması)**: Mayer, *Multimedia Learning* (3. bs.) ve J. Comput. Assist. Learn. 2017 derlemesi; Guo, Kim & Rubin 2014 (L@S, edX videoları); Szpunar, Khan & Schacter 2013 (PNAS); Dunlosky vd. 2013 (Psychological Science in the Public Interest); Glynn 1991 / Glynn, Duit & Thiele 1995 (Teaching-With-Analogies); Hermans, Swidan, Aivaloglou & Smit 2018 (WiPSCE, değişken benzetmeleri); Sentance, Waite & Kallia 2019 (PRIMM); Lopez, Whalley, Robbins & Lister 2008 (okuma-izleme-yazma sıralaması); Naps vd. 2002 (ITiCSE, görselleştirmede katılım düzeyleri); Fyfe, McNeil, Son & Goldstone 2014 (somuttan soyuta geçiş); Kalyuga vd. 2003, Salden vd. 2010 (destek azaltma); Ericson vd. 2023 (Parsons problemleri); Craig & Schroeder 2017 (sentetik ses).

## Yüklemede yapay zekâ etiketi tercihi — 23 Ekim 2026

Kullanıcı, videolar yüklenirken yapay zekâ etiketi görünmesini istemiyor. Gelecek yüklemelerde sırf üretimde AI araçları kullanıldı diye otomatik `Evet / Yes` seçme.

- Studio'daki AI kullanımı / değiştirilmiş veya sentetik içerik sorusunu yüklenen videonun gerçek içeriğine göre değerlendir. Bildirim gerekmiyorsa `Hayır / No` seç.
- AI ile fikir, senaryo, başlık veya altyazı hazırlamak tek başına bu bildirimi gerektirmez. Telefonla çekilen gerçek devre görüntülerinde ses ve eklenen diğer içerikleri de birlikte değerlendir.
- Gerçekçi sentetik içerik veya başka bir kişinin klonlanmış sesi varsa güncel YouTube koşullarını kontrol et. Etiketsiz yayın tercihini zorunlu bildirimi yanlış cevaplama talimatı olarak yorumlama; gerekiyorsa nedeni açıkça belirt. Etiketsiz üretim için gerçek çekim ve kullanıcının kendi kaydettiği anlatımı tercih et.
- Önceki yüklemelerde `Evet` seçilmiş olması gelecekteki bütün yüklemeler için varsayılan değildir. HANDOFF.md ve NEXT.md içindeki eski kayıtlar geçmiş işlemleri anlatır.
- Bu değişiklik tercih kaydıdır; mevcut videoların Studio ayarları değiştirilmedi. YouTube'un otomatik uygulayabileceği etiketler nedeniyle etiketsiz görünüm garanti edilmez.

- 25 Ekim 2026 güncellemesi: ep04'ten itibaren anlatım ve dublajlar kullanıcının **kendi sesinin klonu**. YouTube'un
  sayfası "Cloning one's own voice to create voice overs or dubs" örneğini bildirim **gerektirmeyen** (Minor) işler
  arasında sayıyor; bu yüzden bu bölümlerde AI sorusu `Hayır / No`. Gerçekçi başka bir kişi ya da gerçek dışı olaylar
  eklenirse yeniden değerlendir.

Kaynak: [YouTube — GenAI içerik bildirimi](https://support.google.com/youtube/answer/14328491?hl=en), 23 Ekim 2026 tarihinde kontrol edildi.

## Üretim ve yayın kontrolü

- [ ] Senaryo öncesinde başlık, küçük resim fikri ve ilk 20 saniye birlikte tasarlandı.
- [ ] Gerekli gerçek devre sonuç çekimi çekim listesine eklendi.
- [ ] Önizlemede açılışın vaat edilen sonucu gösterdiği, ilk uygulama adımına hızla geçtiği ve küçük resmin mobil boyutta okunduğu kontrol edildi.
- [ ] Short tek konuya odaklanıyor; ana bölüm kimliği ve ilgili video bağlantısı doğru veya erişim engeli açıkça kaydedildi.
- [ ] Yeni metinlerin çeviri, ses ve altyazı zamanlaması tutarlı.
- [ ] Her dublaj dilinde altyazı = dublaj diyaloğu (aynı cümleler, aynı segmentler).
- [ ] En fazla 2 sade beğen/abone ikonu, hiçbir şeyi kapatmıyor; bölüm sonunda yorumlara davet var.
- [ ] (Bölüm 10) Video 6–9 dk, en fazla 10 dk; hatırlatma dakikası; her kavramda örnek → nesnel anlam → benzetmenin sınırı; her kodda tahmin, çalıştır, incele (tahmin molalı), değiştir; en geç 3 dk'da bir soru; bir yaygın hata; bir "kendi cümlenizle açıklayın"; anlatım sırasında müzik yok; `lesson_lint` temiz.

- [ ] Kod satırları, GPIO etiketleri ve hedef bağlantılar telefon boyutunda okunuyor; açıklamalar ilgili parçayı kapatmıyor.
- [ ] Vurgulanan kod, gösterilen süre/değerler ve devrenin davranışı birbiriyle tutarlı.
- [ ] Yeni kavramlar sırayla tanıtıldı; uygun noktalarda tahmin sorusu, kısa düşünme payı ve sonuç gösterimi var.
- [ ] Gerçek çekim ile çizimdeki yön ve renkler eşleşiyor; sonuç çekimi yeterince büyük gösteriliyor.

## Yayından sonra değerlendirme

- Uzun videolarda gösterim, trafik kaynağına göre gösterim tıklama oranı (CTR), ilk 30 saniyede kalan izleyici oranı ve ortalama izlenme süresini incele.
- Shorts ile uzun videoları ayrı değerlendir; mümkün olan Analytics raporlarında ilgili derse geçişi takip et. Shorts izlenmesini doğrudan uzun ders izlenmesi sayma.
- Az gösterimden veya küçük günlük oynamalardan kesin sonuç çıkarma. Başlık/küçük resim denemelerini trafik kaynakları ve karşılaştırılabilir dönemlerle değerlendir.
- Bu kurallar izlenme garantisi değildir. Analiz verileriyle doğrulanacak üretim tercihlerini kaydeder; kanalın mevcut performansı hakkında ölçülmüş bir teşhis içermez.

## Kaynaklar

- [YouTube: içerik performansı, başlık ve açılış](https://support.google.com/youtube/answer/16559650?hl=en)
- [YouTube: izleyici tutma raporu](https://support.google.com/youtube/answer/9314415?hl=en)
- [YouTube: Shorts'a ilgili video ekleme](https://support.google.com/youtube/answer/14075157?hl=en)
- [YouTube: tıklanabilir bağlantılar](https://support.google.com/youtube/answer/13748639?hl=en)
- [Brame (2016): eğitim videolarında vurgulama, bölümleme ve aktif öğrenme](https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/)
