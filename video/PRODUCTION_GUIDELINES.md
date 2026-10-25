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

## Yüklemede yapay zekâ etiketi tercihi — 23 Ekim 2026

Kullanıcı, videolar yüklenirken yapay zekâ etiketi görünmesini istemiyor. Gelecek yüklemelerde sırf üretimde AI araçları kullanıldı diye otomatik `Evet / Yes` seçme.

- Studio'daki AI kullanımı / değiştirilmiş veya sentetik içerik sorusunu yüklenen videonun gerçek içeriğine göre değerlendir. Bildirim gerekmiyorsa `Hayır / No` seç.
- AI ile fikir, senaryo, başlık veya altyazı hazırlamak tek başına bu bildirimi gerektirmez. Telefonla çekilen gerçek devre görüntülerinde ses ve eklenen diğer içerikleri de birlikte değerlendir.
- Gerçekçi sentetik içerik veya başka bir kişinin klonlanmış sesi varsa güncel YouTube koşullarını kontrol et. Etiketsiz yayın tercihini zorunlu bildirimi yanlış cevaplama talimatı olarak yorumlama; gerekiyorsa nedeni açıkça belirt. Etiketsiz üretim için gerçek çekim ve kullanıcının kendi kaydettiği anlatımı tercih et.
- Önceki yüklemelerde `Evet` seçilmiş olması gelecekteki bütün yüklemeler için varsayılan değildir. HANDOFF.md ve NEXT.md içindeki eski kayıtlar geçmiş işlemleri anlatır.
- Bu değişiklik tercih kaydıdır; mevcut videoların Studio ayarları değiştirilmedi. YouTube'un otomatik uygulayabileceği etiketler nedeniyle etiketsiz görünüm garanti edilmez.

Kaynak: [YouTube — GenAI içerik bildirimi](https://support.google.com/youtube/answer/14328491?hl=en), 23 Ekim 2026 tarihinde kontrol edildi.

## Üretim ve yayın kontrolü

- [ ] Senaryo öncesinde başlık, küçük resim fikri ve ilk 20 saniye birlikte tasarlandı.
- [ ] Gerekli gerçek devre sonuç çekimi çekim listesine eklendi.
- [ ] Önizlemede açılışın vaat edilen sonucu gösterdiği, ilk uygulama adımına hızla geçtiği ve küçük resmin mobil boyutta okunduğu kontrol edildi.
- [ ] Short tek konuya odaklanıyor; ana bölüm kimliği ve ilgili video bağlantısı doğru veya erişim engeli açıkça kaydedildi.
- [ ] Yeni metinlerin çeviri, ses ve altyazı zamanlaması tutarlı.
- [ ] En fazla 2 sade beğen/abone ikonu, hiçbir şeyi kapatmıyor; bölüm sonunda yorumlara davet var.

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
