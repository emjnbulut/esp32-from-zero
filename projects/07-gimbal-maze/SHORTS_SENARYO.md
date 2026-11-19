# 🎬 Shorts Çekim & Kurgu Senaryosu — 2 Eksenli Gimbal Labirent

**Format:** YouTube Shorts / Instagram Reels / TikTok (`9:16` — `1080×1920`, `30 fps`)  
**Hedef Süre:** `45 – 52 saniye`  
**Ana Fikir:** *Kodlama anlatmadan, sadece breadboard'un altındaki gizli bağlantıları ve kabloların "sohbetini" eğlenceli hale getirerek öğretmek.*

---

## ⏱️ Saniye Saniye Çekim Planı

| Süre | Görüntü / Kamera | Seslendirme (Senin Sesin) | Ekranda Büyük Yazı (Caption) | Ses / Efekt |
| :--- | :--- | :--- | :--- | :--- |
| **0:00 – 0:03** | **HOOK:** Yakın çekim! Başparmağın Joystick'i oynattığı anda 3D baskı turuncu gimbal labirent akıcı şekilde yatıyor ve parlak çelik bilye köşeden dönüyor. | *"Kod yok! Bu labirenti oynatan 10 kablo, bu delikli tahtada aslında ne konuşuyor?"* | **KOD YOK! 🚫💻** / **10 KABLO NE İŞE YARIYOR?** | Bilyenin *tıkır-tıkır* yuvarlanma sesi + hızlı *whoosh* |
| **0:03 – 0:11** | **BREADBOARD SIRRI:** Gerçek breadboard'a üstten yakın çekim → **Blender X-Ray animasyonu** (`breadboard_xray_shorts.blend`, kare `1 → 70`) ile plastik şeffaflaşıp altındaki bakır şeritler ortaya çıkıyor! | *"Bu delikler rastgele değil. Altında gizli metal otoyollar var: kenardaki kırmızı-mavi çizgiler yatay uzun yol, ortadaki 5 delikse dikey küçük köprüler."* | **KENARLAR: YATAY OTOYOL ↔️** / **ORTA: 5'Lİ KÖPRÜ ↕️** | Hafif *sci-fi scan* X-Ray geçiş sesi |
| **0:11 – 0:21** | **GÜÇ & ORTAK ZEMİN:** Kırmızı, mor ve siyah kablolar breadboard'a hızlı jump-cut ile takılıyor + **Blender X-Ray** (`kare 70 → 125`: kırmızı 5V & cyan GND akışı). | *"Önce enerji! Motorlar güçlü 5 Volt ister; o yüzden kırmızı otoyola dizdik. Ama Joystick nazik, ona 3.3 Volt veriyoruz ki ESP32'nin kulakları yanmasın! Hepsi mavi GND hattında buluşuyor — ortak zemin olmazsa kimse kimseyi duymaz."* | **MOTORLAR: 5V 🔴** / **JOYSTICK: 3.3V 🟣** / **ORTAK ZEMİN: GND 🔵** | Her kablo takılışında keskin *tık-tık* ASMR |
| **0:21 – 0:29** | **GİRİŞ (JOYSTICK):** Joystick'i sağa-sola oynatırken Yeşil (`D34`) ve Mavi (`D35`) kablolara odaklan + **Blender X-Ray** (`kare 125 → 180`: yeşil & mavi enerji topları ESP32'ye akıyor). | *"Joystick aslında iki tane gizli ses açma düğmesi. Kolu ittikçe voltaj değişiyor, yeşil ve mavi kablolar bu haberi ESP32'ye fısıldıyor."* | **GİRİŞ: JOYSTICK → ESP32 🕹️** | Minik *bip-bip* veri akışı sesi |
| **0:29 – 0:39** | **ÇIKIŞ (2 EKSEN TESTİ):** <br>1) Sadece **Turuncu kabloyu** (`D18`) tak → sadece dış turuncu halka sağa-sola yatar!<br>2) **Sarı kabloyu** (`D19`) tak → iç labirent de öne-arkaya canlanır! (+ **Blender X-Ray** `kare 180 → 240`). | *"Sonra orkestra şefi emri veriyor: Turuncu kabloyu taktım, dış halka sağa-sola yattı. Sarıyı taktım, iç labirent de uyandı!"* | **TURUNCU (D18) → X EKSENİ 🟠** / **SARI (D19) → Y EKSENİ 🟡** | Servo motorların hafif *vızz-vızz* sesi |
| **0:39 – 0:46** | **BÜYÜK FİNAL:** Bilyeyi başlangıçtan hedef çukuruna soktuğun 4 saniyelik tatmin edici oyun anı (çelik bilye hedefe *çınk* diye oturuyor!). | *"Ve sıfır kod karmaşasıyla çalışan 2 eksenli 3D baskı labirent hazır!"* | **HEDEF! 🎯** | Başarı *ding!* efekti |
| **0:46 – 0:50** | **GITHUB KANCASI:** Ekranda 3D baskı parçaları + renkli bağlantı şeması hızlı geçiş. | *"Blender dosyaları, 3D baskı STL'leri, renkli şema ve tak-çalıştır kodu `esp32fromzero` GitHub repomda — link yorumda!"* | **TÜM DOSYALAR: esp32fromzero 🚀** | Çıkış ritmi |

---

## 🎥 Blender "Tek Tek Montaj & X-Ray" Sahnesi (`breadboard_xray_shorts.blend`)

Hazırlanan `blender/breadboard_xray_shorts.blend` (v2 Ultra Kalite) sahnesi **1080×1920 (9:16)** ve **360 kare (12 sn @ 30fps)** olarak tüm parçaları **boş breadboard üzerine tek tek** takar:

1. **Kare 1–50 (`1/6`):** Boş breadboard → X-Ray açılır, içteki 5-parmaklı fosfor-bronz yay klipsleri ve yatay güç rayları görünür.
2. **Kare 50–90 (`2/6`):** **ESP32 DevKit V1** yukarıdan inerek breadboard'a oturur, kırmızı ve mavi SMD LED'leri yanar.
3. **Kare 90–150 (`3/6`):** **5V Kırmızı**, **GND Siyah**, **Sağ Ray Köprüleri** ve **470µF Kondansatör** tek tek takılır; her kablo takıldığı anda altındaki güç rayı parlar.
4. **Kare 150–220 (`4/6`):** **KY-023 Joystick** gelir; **GND**, **3.3V (Mor)**, **VRx (Yeşil → D34)** ve **VRy (Mavi → D35)** kabloları tek tek yuvalarına saplanır.
5. **Kare 220–275 (`5/6`):** **MG90S Servo X** gelir; **5V**, **GND** ve **Turuncu (D18)** kablosu tek tek takılır ve hemen test dönüşü yapar.
6. **Kare 275–360 (`6/6`):** **MG90S Servo Y** gelir; **5V**, **GND** ve **Sarı (D19)** kablosu takılır; finalde Joystick iki eksende hareket ederken ince neon sinyal darbeleri akar ve her iki servo kolu senkronize döner!

---

## 💡 Bonus Çekim Tüyoları
* **Kondansatör Şakası (Opsiyonel Ekstra 3 sn):** Eğer 470µF kondansatörü takarsan kameraya gösterip *"Şu siyah silindir de motorların mini powerbank'i — ikisi aynı anda çalışınca ESP32 bayılmasın diye!"* diyebilirsin. İzleyici bu tür benzetmeleri yorumlarda çok seviyor.
* **İnteraktif Şema Ekran Kaydı:** `wiring/breadboard_interaktif.html` dosyasını tarayıcıda açıp X-Ray düğmesine basarak ekran kaydı alabilir, hatta GitHub Pages üzerinden takipçilerinin kendi telefonundan oynayabileceği canlı demo linki olarak paylaşabilirsin!
