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
