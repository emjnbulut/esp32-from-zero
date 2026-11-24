"""Source of video/ep12/subs/<lang>.json (subtitle-only languages: id ar ru de fr vi ja).
Follows the "sub" field of script.json (digits, code names) where present, else "text" (none in ep12: numbers are words,
the IP address is written digit by digit in words like the English narration; code names stay in Latin letters).
en/tr subtitles come from script.json; hi/pt/es subtitles are the dub texts themselves (video/ep12/dub/*.json),
see PRODUCTION_GUIDELINES.md section 6.
Usage: python video/ep12/make_subs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

L = {}
L["id"] = [
    # s01
    "Aku menekan merah di ponselku... dan lampu di mejaku menyala merah.",
    # s02
    "Aku menekan ring, dan terdengar bel pintu. Tanpa aplikasi, tanpa kabel, tanpa Wi-Fi rumah.",
    # s03
    "Dan layar kecil itu menghitung setiap perintah yang dikirim ponselku.",
    # s04
    "Hari ini board mendapat remote control: ponselmu. Dan kamu tidak menambah satu komponen baru pun.",
    # s05
    "ESP32 sudah punya Wi-Fi bawaan. Ini antenanya, garis zig-zag di board.",
    # s06
    "Biasanya sebuah perangkat tersambung ke router rumah. Hari ini kebalikannya: board membuka jaringan kecilnya sendiri, seperti hotspot di ponselmu.",
    # s07
    "Ponselmu bergabung ke jaringan itu, seperti Wi-Fi biasa. Di dalamnya, board selalu punya alamat yang sama: satu sembilan dua, satu enam delapan, empat, satu.",
    # s08
    "Di kode, membuka jaringan itu cukup satu baris: softAP, dengan nama dan kata sandi.",
    # s09
    "Lalu board menyajikan halaman web kecil. Bayangkan menu restoran yang setiap hidangannya bernomor: ketuk satu tombol, dan ponsel menyebutkan nomor itu.",
    # s10
    "Di sini, nomornya adalah tautan pendek: slash color untuk lampu, slash ring untuk buzzer.",
    # s11
    "Dan satu baris per tautan memberi tahu board pembantu mana yang menjawabnya. Server on: tautan ini, pembantu ini.",
    # s12
    "Loop sekarang punya satu tugas: seperti penjaga malam yang berkeliling, ia memeriksa berulang kali apakah ada ponsel yang mengetuk.",
    # s12b
    "Sebagian tautan membawa keterangan, seperti catatan di kertas pesanan. Pada slash color tanda tanya c sama dengan red, catatannya menyebut warna mana.",
    # s12c
    "Pembantu membaca catatan itu dengan satu baris, server arg c, lalu memilih warna dengan beberapa if, persis seperti episode enam.",
    # s12d
    "Lalu ia menjawab ponsel dengan halaman yang sama lagi, jadi remote-mu tetap ada di layar.",
    # s13
    "Halamannya sendiri adalah templat siap pakai di sketch. Kamu hanya mengganti label dan warnanya.",
    # s14
    "Rangkaiannya? Sudah ada di mejamu: LED warna dari episode enam, layar dan buzzer dari episode sepuluh.",
    # s15
    "Kaki merah, hijau, dan biru di pin dua puluh lima, dua puluh enam, dan dua puluh tujuh, masing-masing lewat resistornya.",
    # s16
    "Unggah, dan layar menampilkan alamat yang harus dibuka.",
    # s17
    "Di ponsel, buka pengaturan Wi-Fi dan gabung ke jaringan board dengan kata sandinya.",
    # s18
    "Ketik alamat itu di browser, dan remote-mu muncul: empat warna dan satu tombol ring.",
    # s19
    "Ketuk merah: tautannya melintas lewat udara, pembantu mengatur warnanya, dan layar menghitung perintah nomor satu.",
    # s19b
    "Yang sebenarnya terjadi: ponsel mengirim pesan kecil lewat udara, board membacanya, mengubah lampu, dan mengirim balik halamannya. Semua dalam sekejap.",
    # s19c
    "Hijau, biru, mati. Setiap ketukan adalah perintah baru, dan penghitung di layar terus naik.",
    # s20
    "Ketuk ring, dan buzzer memainkan dua nada, seperti bel pintu.",
    # s21
    "Masalah umum: ponsel bilang jaringan ini tidak punya internet, lalu diam-diam kembali ke data seluler. Suruh ia tetap tersambung.",
    # s22
    "Dan kata sandinya harus minimal delapan karakter, kalau tidak jaringannya tidak akan muncul.",
    # s22b
    "Dan ketik alamatnya persis: hanya angkanya, tanpa www dan tanpa https di depan.",
    # s23
    "Giliranmu: tambahkan tombol pesta yang mengedipkan merah, hijau, dan biru tiga kali. Satu tautan baru, satu pembantu baru.",
    # s24
    "Kode lengkap dan solusinya ada di folder pelajaran, tautannya di bawah. Apa yang akan kamu kendalikan dengan ponselmu? Tulis di komentar.",
    # s25
    "Lain kali, stasiun cuaca: suhu dan kelembapan di layar dan di halaman ponsel ini juga. Sampai jumpa.",
]
L["ar"] = [
    # s01
    "أضغط على الأحمر في هاتفي... فيتحول الضوء على مكتبي إلى الأحمر.",
    # s02
    "أضغط على ring، فيعزف جرس الباب. بلا تطبيق، بلا كابل، بلا واي فاي المنزل.",
    # s03
    "والشاشة الصغيرة تعدّ كل أمر يرسله هاتفي.",
    # s04
    "اليوم تحصل اللوحة على جهاز تحكم عن بُعد: هاتفك. ولا تضيف أي قطعة جديدة.",
    # s05
    "يحتوي ESP32 على واي فاي مدمج. وهذا هو الهوائي، الخط المتعرّج على اللوحة.",
    # s06
    "عادةً ينضم الجهاز إلى راوتر المنزل. اليوم العكس: اللوحة تفتح شبكتها الصغيرة الخاصة، مثل نقطة الاتصال في هاتفك.",
    # s07
    "ينضم هاتفك إلى تلك الشبكة كأي واي فاي. وداخلها، لدى اللوحة دائمًا العنوان نفسه: واحد تسعة اثنان، واحد ستة ثمانية، أربعة، واحد.",
    # s08
    "في الكود، فتح الشبكة سطر واحد: softAP، مع اسم وكلمة مرور.",
    # s09
    "ثم تقدّم اللوحة صفحة ويب صغيرة. فكّر في قائمة مطعم لكل طبق فيها رقم: تضغط زرًا، فينادي الهاتف ذلك الرقم.",
    # s10
    "هنا، الأرقام روابط قصيرة: slash color للضوء، slash ring للبازر.",
    # s11
    "وسطر واحد لكل رابط يخبر اللوحة أي مساعد يجيب عليه. Server on: هذا الرابط، هذا المساعد.",
    # s12
    "للحلقة loop مهمة واحدة الآن: مثل حارسنا الليلي في جولته، تفحص مرارًا وتكرارًا هل هناك هاتف يطرق الباب.",
    # s12b
    "بعض الروابط تحمل تفصيلة، مثل ملاحظة على ورقة الطلب. في slash color علامة استفهام c يساوي red، تقول الملاحظة أي لون.",
    # s12c
    "يقرأ المساعد تلك الملاحظة بسطر واحد، server arg c، ويختار اللون بعدة if، تمامًا مثل الحلقة السادسة.",
    # s12d
    "ثم يردّ على الهاتف بالصفحة نفسها من جديد، فيبقى جهاز التحكم على الشاشة.",
    # s13
    "الصفحة نفسها قالب جاهز في السكتش. أنت فقط تغيّر الأسماء والألوان.",
    # s14
    "والدارة؟ إنها موجودة على مكتبك أصلًا: ليد الألوان من الحلقة السادسة، والشاشة والبازر من الحلقة العاشرة.",
    # s15
    "أطراف الأحمر والأخضر والأزرق على الأطراف خمسة وعشرين وستة وعشرين وسبعة وعشرين، كل منها عبر مقاومته.",
    # s16
    "ارفع الكود، فتعرض الشاشة العنوان الذي يجب فتحه.",
    # s17
    "على الهاتف، افتح إعدادات واي فاي وانضم إلى شبكة اللوحة بكلمة مرورها.",
    # s18
    "اكتب العنوان في المتصفح، وها هو جهاز التحكم: أربعة ألوان وزر ring.",
    # s19
    "اضغط الأحمر: يسافر الرابط عبر الهواء، يضبط المساعد اللون، وتعدّ الشاشة الأمر رقم واحد.",
    # s19b
    "ما يحدث فعلًا: يرسل الهاتف رسالة صغيرة عبر الهواء، تقرأها اللوحة، وتغيّر الضوء، وترسل الصفحة عائدة. كل ذلك في لمح البصر.",
    # s19c
    "أخضر، أزرق، إطفاء. كل ضغطة أمر جديد، والعدّاد على الشاشة يواصل الصعود.",
    # s20
    "اضغط ring، فيعزف البازر نغمتين، مثل جرس الباب.",
    # s21
    "مشكلة شائعة: يقول الهاتف إن هذه الشبكة بلا إنترنت ويعود بهدوء إلى بيانات الجوال. قل له أن يبقى متصلًا.",
    # s22
    "وكلمة المرور تحتاج ثمانية أحرف على الأقل، وإلا فلن تظهر الشبكة أبدًا.",
    # s22b
    "واكتب العنوان بالضبط: الأرقام فقط، بلا www وبلا https في البداية.",
    # s23
    "دورك: أضف زر حفلة يومض بالأحمر والأخضر والأزرق ثلاث مرات. رابط جديد واحد، ومساعد جديد واحد.",
    # s24
    "الكود الكامل والحل في مجلد الدرس، والرابط أدناه. ماذا ستتحكم به بهاتفك؟ أخبرني في التعليقات.",
    # s25
    "في المرة القادمة، محطة طقس: الحرارة والرطوبة على الشاشة وعلى صفحة الهاتف هذه نفسها. أراكم هناك.",
]
L["ru"] = [
    # s01
    "Я нажимаю красный на телефоне... и лампа на моём столе становится красной.",
    # s02
    "Я нажимаю ring, и играет дверной звонок. Без приложения, без кабеля, без домашнего Wi-Fi.",
    # s03
    "А маленький экран считает каждую команду, которую отправляет мой телефон.",
    # s04
    "Сегодня плата получает пульт: ваш телефон. И вы не добавляете ни одной новой детали.",
    # s05
    "В ESP32 встроен Wi-Fi. Вот антенна, эта зигзагообразная линия на плате.",
    # s06
    "Обычно устройство подключается к домашнему роутеру. Сегодня наоборот: плата открывает собственную маленькую сеть, как точка доступа на вашем телефоне.",
    # s07
    "Ваш телефон подключается к этой сети, как к любому Wi-Fi. Внутри у платы всегда один и тот же адрес: один девять два, один шесть восемь, четыре, один.",
    # s08
    "В коде открыть сеть можно одной строкой: softAP, с именем и паролем.",
    # s09
    "Затем плата отдаёт крошечную веб-страницу. Представьте меню ресторана, где у каждого блюда есть номер: нажимаете кнопку, и телефон называет этот номер.",
    # s10
    "Здесь номера это короткие ссылки: slash color для лампы, slash ring для зуммера.",
    # s11
    "И по одной строке на ссылку сообщает плате, какой помощник на неё отвечает. Server on: эта ссылка, этот помощник.",
    # s12
    "У цикла loop теперь одна задача: как наш ночной сторож на обходе, он снова и снова проверяет, не стучится ли телефон.",
    # s12b
    "Некоторые ссылки несут уточнение, как записка на бланке заказа. В slash color вопросительный знак c равно red записка говорит, какой цвет.",
    # s12c
    "Помощник читает эту записку одной строкой, server arg c, и выбирает цвет несколькими if, как в шестом эпизоде.",
    # s12d
    "Затем он снова отвечает телефону той же страницей, так что пульт остаётся на экране.",
    # s13
    "Сама страница это готовый шаблон в скетче. Вы меняете только подписи и цвета.",
    # s14
    "Схема? Она уже на вашем столе: цветной светодиод из шестого эпизода, экран и зуммер из десятого.",
    # s15
    "Красная, зелёная и синяя ножки на пинах двадцать пять, двадцать шесть и двадцать семь, каждая через свой резистор.",
    # s16
    "Загружаем, и экран показывает адрес, который нужно открыть.",
    # s17
    "На телефоне откройте настройки Wi-Fi и подключитесь к сети платы с её паролем.",
    # s18
    "Введите адрес в браузере, и вот ваш пульт: четыре цвета и кнопка ring.",
    # s19
    "Нажимаем красный: ссылка летит по воздуху, помощник задаёт цвет, а экран считает команду номер один.",
    # s19b
    "Что происходит на самом деле: телефон отправляет крошечное сообщение по воздуху, плата его читает, меняет свет и отправляет страницу обратно. Всё это в одно мгновение.",
    # s19c
    "Зелёный, синий, выключить. Каждое нажатие это новая команда, а счётчик на экране продолжает расти.",
    # s20
    "Нажимаем ring, и зуммер играет две ноты, как дверной звонок.",
    # s21
    "Частая проблема: телефон пишет, что в этой сети нет интернета, и тихо переключается обратно на мобильные данные. Скажите ему оставаться подключённым.",
    # s22
    "И пароль должен содержать не меньше восьми символов, иначе сеть не появится.",
    # s22b
    "И вводите адрес точно: только цифры, без www и без https впереди.",
    # s23
    "Ваша очередь: добавьте кнопку вечеринки, которая мигает красным, зелёным и синим три раза. Одна новая ссылка, один новый помощник.",
    # s24
    "Полный код и решение лежат в папке урока, ссылка ниже. Чем бы вы управляли со своего телефона? Расскажите в комментариях.",
    # s25
    "В следующий раз метеостанция: температура и влажность на экране и на этой же странице в телефоне. До встречи.",
]
L["de"] = [
    # s01
    "Ich tippe auf meinem Handy auf Rot... und das Licht auf meinem Schreibtisch wird rot.",
    # s02
    "Ich tippe auf ring, und es spielt eine Türklingel. Keine App, kein Kabel, kein WLAN zu Hause.",
    # s03
    "Und das kleine Display zählt jeden Befehl, den mein Handy sendet.",
    # s04
    "Heute bekommt das Board eine Fernbedienung: dein Handy. Und du fügst kein einziges neues Teil hinzu.",
    # s05
    "Der ESP32 hat WLAN eingebaut. Hier ist die Antenne, diese Zickzacklinie auf dem Board.",
    # s06
    "Normalerweise verbindet sich ein Gerät mit deinem Router zu Hause. Heute ist es umgekehrt: Das Board öffnet sein eigenes kleines Netz, wie der Hotspot auf deinem Handy.",
    # s07
    "Dein Handy verbindet sich mit diesem Netz, wie mit jedem WLAN. Darin hat das Board immer dieselbe Adresse: eins neun zwei, eins sechs acht, vier, eins.",
    # s08
    "Im Code ist das Öffnen des Netzes eine Zeile: softAP, mit einem Namen und einem Passwort.",
    # s09
    "Dann liefert das Board eine winzige Webseite aus. Stell dir eine Speisekarte vor, auf der jedes Gericht eine Nummer hat: Du tippst auf einen Button, und das Handy ruft diese Nummer aus.",
    # s10
    "Hier sind die Nummern kurze Links: slash color für das Licht, slash ring für den Buzzer.",
    # s11
    "Und eine Zeile pro Link sagt dem Board, welcher Helfer ihn beantwortet. Server on: dieser Link, dieser Helfer.",
    # s12
    "Die Loop hat jetzt nur eine Aufgabe: Wie unser Nachtwächter auf seiner Runde prüft sie immer wieder, ob ein Handy anklopft.",
    # s12b
    "Manche Links tragen ein Detail, wie eine Notiz auf einem Bestellzettel. Bei slash color Fragezeichen c gleich red sagt die Notiz, welche Farbe.",
    # s12c
    "Der Helfer liest diese Notiz mit einer Zeile, server arg c, und wählt die Farbe mit ein paar ifs, genau wie in Folge sechs.",
    # s12d
    "Dann antwortet er dem Handy wieder mit derselben Seite, damit deine Fernbedienung auf dem Bildschirm bleibt.",
    # s13
    "Die Seite selbst ist eine fertige Vorlage im Sketch. Du änderst nur die Beschriftungen und die Farben.",
    # s14
    "Die Schaltung? Die liegt schon auf deinem Tisch: die Farb-LED aus Folge sechs, das Display und der Buzzer aus Folge zehn.",
    # s15
    "Rote, grüne und blaue Beinchen an den Pins fünfundzwanzig, sechsundzwanzig und siebenundzwanzig, jedes über seinen Widerstand.",
    # s16
    "Hochladen, und das Display zeigt die Adresse, die du öffnen sollst.",
    # s17
    "Öffne am Handy die WLAN-Einstellungen und verbinde dich mit dem Netz des Boards, mit seinem Passwort.",
    # s18
    "Tippe die Adresse im Browser ein, und da ist deine Fernbedienung: vier Farben und ein ring-Button.",
    # s19
    "Tippe auf Rot: Der Link reist durch die Luft, der Helfer stellt die Farbe ein, und das Display zählt Befehl Nummer eins.",
    # s19b
    "Was wirklich passiert: Das Handy schickt eine winzige Nachricht durch die Luft, das Board liest sie, ändert das Licht und schickt die Seite zurück. Alles in einem Augenblick.",
    # s19c
    "Grün, Blau, aus. Jeder Tipp ist ein neuer Befehl, und der Zähler auf dem Display zählt immer weiter hoch.",
    # s20
    "Tippe auf ring, und der Buzzer spielt zwei Töne, wie eine Türklingel.",
    # s21
    "Ein häufiges Problem: Das Handy sagt, dieses Netz habe kein Internet, und wechselt leise zurück zu den mobilen Daten. Sag ihm, es soll verbunden bleiben.",
    # s22
    "Und das Passwort braucht mindestens acht Zeichen, sonst erscheint das Netz gar nicht.",
    # s22b
    "Und tippe die Adresse genau so ein: nur die Zahlen, ohne www und ohne https davor.",
    # s23
    "Du bist dran: Füge einen Party-Button hinzu, der dreimal Rot, Grün und Blau blinkt. Ein neuer Link, ein neuer Helfer.",
    # s24
    "Den vollständigen Code und die Lösung findest du im Lektionsordner, der Link steht unten. Was würdest du mit deinem Handy steuern? Schreib es in die Kommentare.",
    # s25
    "Nächstes Mal eine Wetterstation: Temperatur und Luftfeuchtigkeit auf dem Display und auf genau dieser Handy-Seite. Bis dann.",
]
L["fr"] = [
    # s01
    "J'appuie sur rouge sur mon téléphone... et la lumière sur mon bureau devient rouge.",
    # s02
    "J'appuie sur ring, et une sonnette de porte retentit. Pas d'appli, pas de câble, pas de Wi-Fi à la maison.",
    # s03
    "Et le petit écran compte chaque commande que mon téléphone envoie.",
    # s04
    "Aujourd'hui, la carte reçoit une télécommande : ton téléphone. Et tu n'ajoutes aucune pièce nouvelle.",
    # s05
    "L'ESP32 a le Wi-Fi intégré. Voici l'antenne, cette ligne en zigzag sur la carte.",
    # s06
    "D'habitude, un appareil rejoint ta box. Aujourd'hui, c'est l'inverse : la carte ouvre son propre petit réseau, comme le point d'accès de ton téléphone.",
    # s07
    "Ton téléphone rejoint ce réseau, comme n'importe quel Wi-Fi. À l'intérieur, la carte a toujours la même adresse : un neuf deux, un six huit, quatre, un.",
    # s08
    "Dans le code, ouvrir le réseau tient en une ligne : softAP, avec un nom et un mot de passe.",
    # s09
    "Ensuite, la carte sert une toute petite page web. Pense à un menu de restaurant où chaque plat a un numéro : tu touches un bouton, et le téléphone annonce ce numéro.",
    # s10
    "Ici, les numéros sont des liens courts : slash color pour la lumière, slash ring pour le buzzer.",
    # s11
    "Et une ligne par lien dit à la carte quel assistant y répond. Server on : ce lien, cet assistant.",
    # s12
    "La loop n'a plus qu'une mission : comme notre veilleur de nuit en ronde, elle vérifie encore et encore si un téléphone frappe à la porte.",
    # s12b
    "Certains liens portent un détail, comme une note sur un bon de commande. Dans slash color point d'interrogation c égale red, la note dit quelle couleur.",
    # s12c
    "L'assistant lit cette note en une ligne, server arg c, et choisit la couleur avec quelques if, comme à l'épisode six.",
    # s12d
    "Puis il répond au téléphone avec la même page, pour que ta télécommande reste à l'écran.",
    # s13
    "La page elle-même est un modèle prêt à l'emploi dans le sketch. Tu changes seulement les libellés et les couleurs.",
    # s14
    "Le circuit ? Il est déjà sur ton bureau : la LED de couleur de l'épisode six, l'écran et le buzzer de l'épisode dix.",
    # s15
    "Les pattes rouge, verte et bleue sur les broches vingt-cinq, vingt-six et vingt-sept, chacune avec sa résistance.",
    # s16
    "Téléverse, et l'écran affiche l'adresse à ouvrir.",
    # s17
    "Sur le téléphone, ouvre les réglages Wi-Fi et rejoins le réseau de la carte avec son mot de passe.",
    # s18
    "Tape l'adresse dans le navigateur, et voilà ta télécommande : quatre couleurs et un bouton ring.",
    # s19
    "Touche rouge : le lien voyage dans l'air, l'assistant règle la couleur, et l'écran compte la commande numéro un.",
    # s19b
    "Ce qui se passe vraiment : le téléphone envoie un tout petit message dans l'air, la carte le lit, change la lumière et renvoie la page. Le tout en un clin d'œil.",
    # s19c
    "Vert, bleu, éteint. Chaque toucher est une nouvelle commande, et le compteur de l'écran ne cesse de monter.",
    # s20
    "Touche ring, et le buzzer joue deux notes, comme une sonnette.",
    # s21
    "Un problème courant : le téléphone dit que ce réseau n'a pas Internet et repasse discrètement en données mobiles. Dis-lui de rester connecté.",
    # s22
    "Et le mot de passe doit faire au moins huit caractères, sinon le réseau n'apparaît jamais.",
    # s22b
    "Et tape l'adresse exactement : juste les chiffres, sans www et sans https devant.",
    # s23
    "À toi : ajoute un bouton fête qui fait clignoter rouge, vert et bleu trois fois. Un nouveau lien, un nouvel assistant.",
    # s24
    "Le code complet et la solution sont dans le dossier de la leçon, lien ci-dessous. Que contrôlerais-tu avec ton téléphone ? Dis-le-moi en commentaire.",
    # s25
    "La prochaine fois, une station météo : température et humidité sur l'écran et sur cette même page du téléphone. À bientôt.",
]
L["vi"] = [
    # s01
    "Tôi chạm vào màu đỏ trên điện thoại... và đèn trên bàn tôi chuyển sang đỏ.",
    # s02
    "Tôi chạm vào ring, và chuông cửa vang lên. Không ứng dụng, không dây cáp, không Wi-Fi nhà.",
    # s03
    "Và màn hình nhỏ đếm từng lệnh mà điện thoại của tôi gửi.",
    # s04
    "Hôm nay bo mạch có một chiếc điều khiển từ xa: điện thoại của bạn. Và bạn không thêm một linh kiện mới nào.",
    # s05
    "ESP32 có sẵn Wi-Fi. Đây là ăng-ten, đường ngoằn ngoèo này trên bo mạch.",
    # s06
    "Thường thì một thiết bị kết nối vào bộ định tuyến ở nhà. Hôm nay ngược lại: bo mạch mở mạng nhỏ của riêng nó, giống điểm phát sóng trên điện thoại của bạn.",
    # s07
    "Điện thoại của bạn kết nối vào mạng đó như mọi Wi-Fi. Bên trong, bo mạch luôn có cùng một địa chỉ: một chín hai, một sáu tám, bốn, một.",
    # s08
    "Trong mã, mở mạng chỉ là một dòng: softAP, với một cái tên và một mật khẩu.",
    # s09
    "Rồi bo mạch phục vụ một trang web nhỏ xíu. Hãy nghĩ đến thực đơn nhà hàng mà món nào cũng có số: chạm một nút, và điện thoại gọi to con số đó.",
    # s10
    "Ở đây, các con số là những liên kết ngắn: slash color cho đèn, slash ring cho còi.",
    # s11
    "Và một dòng cho mỗi liên kết cho bo mạch biết trợ thủ nào trả lời nó. Server on: liên kết này, trợ thủ này.",
    # s12
    "Vòng lặp loop giờ chỉ có một việc: như người gác đêm đi tuần, nó kiểm tra đi kiểm tra lại xem có điện thoại nào đang gõ cửa không.",
    # s12b
    "Một số liên kết mang theo chi tiết, như ghi chú trên phiếu gọi món. Trong slash color dấu hỏi c bằng red, ghi chú cho biết màu nào.",
    # s12c
    "Trợ thủ đọc ghi chú đó bằng một dòng, server arg c, và chọn màu bằng vài lệnh if, giống hệt tập sáu.",
    # s12d
    "Rồi nó trả lời điện thoại bằng chính trang đó, để điều khiển của bạn vẫn nằm trên màn hình.",
    # s13
    "Bản thân trang là một mẫu làm sẵn trong sketch. Bạn chỉ đổi nhãn và màu.",
    # s14
    "Mạch ư? Nó đã nằm sẵn trên bàn bạn: đèn LED màu từ tập sáu, màn hình và còi từ tập mười.",
    # s15
    "Chân đỏ, xanh lá và xanh dương ở chân hai mươi lăm, hai mươi sáu và hai mươi bảy, mỗi chân qua điện trở của nó.",
    # s16
    "Nạp mã, và màn hình hiện địa chỉ cần mở.",
    # s17
    "Trên điện thoại, mở cài đặt Wi-Fi và kết nối vào mạng của bo mạch bằng mật khẩu của nó.",
    # s18
    "Gõ địa chỉ vào trình duyệt, và đây là điều khiển của bạn: bốn màu và một nút ring.",
    # s19
    "Chạm màu đỏ: liên kết bay qua không khí, trợ thủ đặt màu, và màn hình đếm lệnh số một.",
    # s19b
    "Điều thật sự xảy ra: điện thoại gửi một tin nhắn nhỏ xíu qua không khí, bo mạch đọc nó, đổi ánh sáng, và gửi trang trở lại. Tất cả trong chớp mắt.",
    # s19c
    "Xanh lá, xanh dương, tắt. Mỗi lần chạm là một lệnh mới, và bộ đếm trên màn hình cứ tăng lên.",
    # s20
    "Chạm ring, và còi phát hai nốt, như chuông cửa.",
    # s21
    "Một vấn đề thường gặp: điện thoại báo mạng này không có internet và lặng lẽ chuyển về dữ liệu di động. Hãy bảo nó ở lại kết nối.",
    # s22
    "Và mật khẩu cần ít nhất tám ký tự, nếu không mạng sẽ không bao giờ hiện ra.",
    # s22b
    "Và gõ địa chỉ thật chính xác: chỉ các con số, không có www và không có https phía trước.",
    # s23
    "Đến lượt bạn: thêm một nút tiệc nháy đỏ, xanh lá và xanh dương ba lần. Một liên kết mới, một trợ thủ mới.",
    # s24
    "Mã đầy đủ và lời giải nằm trong thư mục bài học, liên kết ở dưới. Bạn sẽ điều khiển gì bằng điện thoại? Hãy cho tôi biết trong phần bình luận.",
    # s25
    "Lần sau, một trạm thời tiết: nhiệt độ và độ ẩm trên màn hình và ngay trên trang điện thoại này. Hẹn gặp lại.",
]
L["ja"] = [
    # s01
    "スマホで赤をタップすると... 机の上のライトが赤くなります。",
    # s02
    "ringをタップすると、ドアベルが鳴ります。アプリも、ケーブルも、家のWi-Fiもいりません。",
    # s03
    "そして小さな画面が、スマホが送るコマンドを一つ残らず数えます。",
    # s04
    "今日はボードにリモコンがつきます。あなたのスマホです。しかも新しい部品は一つも足しません。",
    # s05
    "ESP32にはWi-Fiが内蔵されています。これがアンテナ、ボード上のこのジグザグの線です。",
    # s06
    "ふつうは機器が家のルーターにつながります。今日は逆です。ボードが自分だけの小さなネットワークを開きます。スマホのテザリングのようにです。",
    # s07
    "スマホは、ふつうのWi-Fiと同じようにそのネットワークに入ります。その中で、ボードのアドレスはいつも同じです。いち、きゅう、に、いち、ろく、はち、よん、いち。",
    # s08
    "コードでは、ネットワークを開くのは一行です。softAP、名前とパスワードをつけます。",
    # s09
    "次にボードが小さなウェブページを出します。どの料理にも番号があるレストランのメニューを思い浮かべてください。ボタンをタップすると、スマホがその番号を呼びます。",
    # s10
    "ここで番号は短いリンクです。ライトにはslash color、ブザーにはslash ringです。",
    # s11
    "そしてリンクごとの一行が、どのヘルパーが応えるかをボードに教えます。Server on。このリンク、このヘルパー。",
    # s12
    "loopの仕事は今は一つだけです。見回り中の夜警のように、スマホがノックしていないかを何度も確かめます。",
    # s12b
    "リンクには、注文伝票のメモのように、詳細がつくものがあります。slash color クエスチョンマーク c イコール red では、メモがどの色かを伝えます。",
    # s12c
    "ヘルパーはそのメモを一行、server arg cで読み、第六回と同じように、いくつかのifで色を選びます。",
    # s12d
    "そして同じページをもう一度スマホに返すので、リモコンは画面に残ります。",
    # s13
    "ページそのものはスケッチに入った出来合いのテンプレートです。変えるのはラベルと色だけです。",
    # s14
    "回路ですか？ もう机の上にあります。第六回のカラーLED、第十回の画面とブザーです。",
    # s15
    "赤、緑、青の脚は、二十五番、二十六番、二十七番のピンにつなぎ、それぞれ抵抗を通します。",
    # s16
    "アップロードすると、画面に開くべきアドレスが出ます。",
    # s17
    "スマホでWi-Fi設定を開き、ボードのネットワークにパスワードで入ります。",
    # s18
    "ブラウザにアドレスを入力すると、リモコンの出来上がりです。四つの色とringボタンがあります。",
    # s19
    "赤をタップします。リンクが空中を飛び、ヘルパーが色を設定し、画面がコマンド一番を数えます。",
    # s19b
    "実際に起きていること。スマホが小さなメッセージを空中に送り、ボードがそれを読み、ライトを変えて、ページを返します。すべて一瞬です。",
    # s19c
    "緑、青、オフ。タップするたびに新しいコマンドで、画面のカウンターは増え続けます。",
    # s20
    "ringをタップすると、ブザーが二つの音を鳴らします。ドアベルのようにです。",
    # s21
    "よくある問題です。スマホが「このネットワークはインターネットに接続されていません」と言って、そっとモバイルデータに戻ります。つながったままにするよう設定してください。",
    # s22
    "そしてパスワードは八文字以上にしてください。さもないとネットワークが現れません。",
    # s22b
    "アドレスはそのまま入力してください。数字だけで、前にwwwもhttpsもつけません。",
    # s23
    "あなたの番です。赤、緑、青を三回点滅させるパーティーボタンを足してください。新しいリンクが一つ、新しいヘルパーが一つです。",
    # s24
    "完全なコードと答えはレッスンフォルダにあります。リンクは下です。スマホで何を操作しますか？ コメントで教えてください。",
    # s25
    "次回は気象ステーションです。温度と湿度を画面と、このスマホのページに表示します。ではまた。",
]

if __name__ == "__main__":
    out = ROOT / "subs"
    out.mkdir(exist_ok=True)
    for lang, lines in L.items():
        assert len(lines) == len(IDS), (lang, len(lines), len(IDS))
        seg = dict(zip(IDS, lines))
        (out / f"{lang}.json").write_text(json.dumps({"lang": lang, "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("subs written:", ", ".join(L), f"({len(IDS)} segments each)")
