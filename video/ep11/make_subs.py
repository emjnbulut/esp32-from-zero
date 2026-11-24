"""Source of video/ep11/subs/<lang>.json (subtitle-only languages: id ar ru de fr vi ja).
Follows the "sub" field of script.json (digits, code names) where present, else "text" (none in ep11: numbers are words).
en/tr subtitles come from script.json; hi/pt/es subtitles are the dub texts themselves (video/ep11/dub/*.json),
see PRODUCTION_GUIDELINES.md section 6.
Usage: python video/ep11/make_subs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

L = {}
L["id"] = [
    # s01
    "Mejaku sekarang punya penjaga. Aku mengaktifkannya, dan aku punya sepuluh detik untuk keluar.",
    # s02
    "Lalu sebuah tangan menyelinap ke arah toples kue... dan langsung tertangkap.",
    # s03
    "Dan saat aku kembali, ia bahkan memberi tahu kapan itu terjadi: dua menit lalu.",
    # s04
    "Hari ini kita membuat alarm gerak ini. Satu komponen baru, sisanya rangkaian dari episode lalu.",
    # s05
    "Kubah putih ini adalah sensor gerak. Ia tidak memancarkan apa pun. Ia hanya mengawasi kehangatan.",
    # s06
    "Semua yang hangat bersinar dalam inframerah: tanganmu, kucing, secangkir teh. Kita tidak bisa melihat cahaya itu, tetapi sensor ini bisa.",
    # s07
    "Kubah ini adalah lensa dari banyak jendela kecil. Tiap jendela melihat satu irisan ruangan yang berbeda, seperti sederet senter.",
    # s08
    "Ketika sesuatu yang hangat berpindah dari satu jendela ke jendela berikutnya, sensor merasakan perubahannya, dan pin jawabannya menyala.",
    # s09
    "Jadi bagi kode kita, seluruh sensor ini hanya jempol ke atas kalau ada yang bergerak, dan jempol ke bawah kalau tidak ada.",
    # s10
    "Di sisinya ada dua knob oranye. Satu mengatur berapa lama jawaban ya bertahan, satu lagi seberapa jauh ia bisa melihat.",
    # s11
    "Satu tips: setelah dinyalakan, beri sensor sekitar tiga puluh detik untuk pemanasan. Sebelum itu ia bisa menjawab ya tanpa alasan.",
    # s12
    "Ayo kita rangkai. Layar, tombol, dan buzzer tetap persis di tempatnya.",
    # s13
    "Sensor ini punya tiga kaki. Kabel merah membawa lima volt dari pin V-in board, dan kabel hitam ke ground.",
    # s14
    "Kaki tengah adalah jawabannya. Kabel ungu membawanya ke pin tiga puluh tiga.",
    # s15
    "Dan jangan khawatir: jawabannya keluar pada tiga koma tiga volt, aman untuk board kita.",
    # s16
    "Membacanya cukup satu baris: digital read di pin tiga puluh tiga. High berarti ada gerakan.",
    # s17
    "Tapi alarm butuh rencana, jadi lagi-lagi kita memakai langkah, seperti mesin cuci kita: mati, pergi, siaga, dan alarm.",
    # s18
    "Tekan tombol, dan hitung mundur dimulai, dengan tik kecil tiap detik, jadi kamu punya waktu untuk keluar.",
    # s19
    "Di angka nol, penjaga siaga. Sekarang ia menunggu satu hal saja: sensor berkata ya.",
    # s20
    "Begitu itu terjadi, sirene menyala: dua nada, berganti empat kali per detik, jadi benar-benar terdengar seperti alarm.",
    # s21
    "Tekan tombol untuk menghentikannya. Atau ia berhenti sendiri setelah lima belas detik, supaya tetangga tetap ramah.",
    # s22
    "Sekarang bagian cerdasnya. Saat gerakan terjadi, kita mencap waktunya, seperti karcis parkir dari episode sembilan.",
    # s23
    "Cukup satu baris: last motion sama dengan millis. Millis adalah stopwatch board sejak dinyalakan.",
    # s24
    "Nanti, now dikurangi last motion memberi tahu berapa lama yang lalu. Bagi dengan enam puluh ribu, dan kamu dapat menit.",
    # s25
    "Jadi layar bisa berkata: terlihat dua kali, terakhir tiga menit lalu.",
    # s26
    "Pertanyaan singkat: kitmu punya buzzer kedua yang bentuknya hampir sama. Apa bedanya?",
    # s27
    "Punya kita pasif: speaker kecil yang memainkan nada apa pun yang kita kirim. Yang aktif adalah kotak musik dengan pembunyi sendiri di dalamnya: beri daya, dan ia memainkan satu bip tetapnya.",
    # s28
    "Lebih mudah, tapi tidak bisa sirene. Karena itu alarm memakai yang pasif.",
    # s29
    "Ayo kita uji. Aku mengaktifkannya, hitung mundur berjalan, dan aku berjalan keluar ruangan.",
    # s30
    "Sebuah tangan menyelinap ke arah toples kue... tertangkap!",
    # s31
    "Aku kembali dan menekan tombol: terlihat satu kali, terakhir dua belas detik lalu.",
    # s32
    "Masalah umum: alarm berbunyi tepat setelah kamu mengaktifkannya. Biasanya sensor masih memanas, atau knob waktu membuat ya bertahan terlalu lama.",
    # s33
    "Jadi tunggu tiga puluh detik setelah dinyalakan, dan putar knob waktu sampai paling kecil. Sisanya dikerjakan kode kita.",
    # s34
    "Giliranmu. Simpan jumlah tangkapan walau kabel dicabut, dengan Preferences, seperti episode lalu.",
    # s35
    "Kode lengkap dan solusinya ada di folder pelajaran, tautannya di bawah. Apa yang akan kamu jaga dengan ini? Tulis di komentar.",
    # s36
    "Lain kali, kamu mengendalikan board ini dari ponsel, tanpa aplikasi dan tanpa router. Sampai jumpa di sana.",
]
L["ar"] = [
    # s01
    "صار لمكتبي حارس الآن. أُفعّله، ولدي عشر ثوانٍ لأغادر.",
    # s02
    "ثم تتسلل يد نحو جرّة البسكويت... ويُمسك بها فورًا.",
    # s03
    "وحين أعود، يخبرني متى حدث ذلك: قبل دقيقتين.",
    # s04
    "اليوم نبني جهاز الإنذار هذا. قطعة جديدة واحدة، والباقي هو دارة الحلقة السابقة.",
    # s05
    "هذه القبة البيضاء حساس حركة. إنه لا يرسل شيئًا. هو فقط يراقب الدفء.",
    # s06
    "كل شيء دافئ يتوهج بالأشعة تحت الحمراء: يدك، قطة، كوب شاي. لا نرى هذا التوهج، لكن هذا الحساس يراه.",
    # s07
    "القبة عدسة من نوافذ صغيرة كثيرة. كل نافذة تنظر إلى شريحة مختلفة من الغرفة، كصف من المصابيح اليدوية.",
    # s08
    "حين ينتقل شيء دافئ من نافذة إلى التي تليها، يلاحظ الحساس التغيّر، ويُفعَّل طرف إجابته.",
    # s09
    "لذلك، بالنسبة إلى كودنا، الحساس كله مجرد إبهام للأعلى حين يتحرك شيء، وإبهام للأسفل حين لا يتحرك شيء.",
    # s10
    "على الجانب مقبضان برتقاليان. الأول يحدد كم تدوم كلمة نعم، والثاني إلى أي مدى يرى.",
    # s11
    "نصيحة: بعد التشغيل، امنحه نحو ثلاثين ثانية ليسخن. قبل ذلك قد يقول نعم بلا سبب.",
    # s12
    "لنوصّل الأسلاك. الشاشة والزر والجرس تبقى تمامًا حيث كانت.",
    # s13
    "للحساس ثلاث أرجل. سلك أحمر يجلب خمسة فولت من طرف V-in في اللوحة، وسلك أسود إلى الأرضي.",
    # s14
    "الرجل الوسطى هي الإجابة. سلك بنفسجي يأخذها إلى الطرف ثلاثة وثلاثين.",
    # s15
    "ولا تقلق: الإجابة تخرج بثلاثة فاصل ثلاثة فولت، آمنة للوحتنا.",
    # s16
    "قراءته سطر واحد: digital read على الطرف ثلاثة وثلاثين. وHigh تعني حركة.",
    # s17
    "لكن الإنذار يحتاج خطة، لذلك نستخدم الخطوات مجددًا، مثل غسالتنا: متوقف، مغادرة، مفعّل، وإنذار.",
    # s18
    "اضغط الزر، فيبدأ العدّ التنازلي، مع نقرة صغيرة كل ثانية، فيكون لديك وقت لتخرج.",
    # s19
    "عند الصفر يصير الحارس مفعّلًا. وينتظر الآن أمرًا واحدًا فقط: أن يقول الحساس نعم.",
    # s20
    "وحين يحدث ذلك تبدأ الصفارة: نغمتان تتبدلان أربع مرات في الثانية، فتبدو فعلًا كإنذار.",
    # s21
    "اضغط الزر لإيقافها. أو تتوقف من نفسها بعد خمس عشرة ثانية، ليبقى الجيران ودودين.",
    # s22
    "الآن الجزء الذكي. لحظة الحركة نختم الوقت، مثل تذكرة الموقف من الحلقة التاسعة.",
    # s23
    "إنه سطر واحد: last motion يساوي millis. وmillis هي ساعة إيقاف اللوحة منذ التشغيل.",
    # s24
    "لاحقًا، now ناقص last motion يخبرنا كم مضى. اقسم على ستين ألفًا فتحصل على الدقائق.",
    # s25
    "فتستطيع الشاشة أن تقول: شوهد مرتين، آخر مرة قبل ثلاث دقائق.",
    # s26
    "سؤال سريع: في عدّتك جرس ثانٍ يشبه الأول تقريبًا. ما الفرق؟",
    # s27
    "جرسنا سلبي: مكبّر صغير يعزف أي نغمة نرسلها. أما الفعّال فصندوق موسيقى فيه صافرته الخاصة: شغّله فيعزف صفيره الثابت الوحيد.",
    # s28
    "أسهل، لكن بلا صفارة إنذار. لهذا يستخدم الإنذار الجرس السلبي.",
    # s29
    "لنجرّب. أُفعّله، ويجري العدّ التنازلي، وأخرج من الغرفة.",
    # s30
    "تتسلل يد نحو جرّة البسكويت... أُمسك بها!",
    # s31
    "أعود وأضغط الزر: شوهد مرة واحدة، آخر مرة قبل اثنتي عشرة ثانية.",
    # s32
    "مشكلة شائعة: ينطلق الإنذار بعد التفعيل مباشرة. غالبًا ما يكون الحساس لا يزال يسخن، أو أن مقبض الوقت يُبقي نعم طويلًا جدًا.",
    # s33
    "فانتظر ثلاثين ثانية بعد التشغيل، وأدر مقبض الوقت إلى أقصى الأسفل. وكودنا يتولى الباقي.",
    # s34
    "دورك. احتفظ بعدد الإمساكات حتى بعد فصل الكهرباء، باستخدام Preferences، مثل الحلقة الماضية.",
    # s35
    "الكود الكامل والحل في مجلد الدرس، والرابط في الأسفل. ماذا ستحرس بهذا؟ أخبرني في التعليقات.",
    # s36
    "في المرة القادمة تتحكم بهذه اللوحة من هاتفك، بلا تطبيق وبلا راوتر. أراكم هناك.",
]
L["ru"] = [
    # s01
    "У моего стола теперь есть охранник. Я включаю его, и у меня десять секунд, чтобы уйти.",
    # s02
    "Потом рука крадётся к банке с печеньем... и её тут же ловят.",
    # s03
    "А когда я возвращаюсь, он даже говорит, когда это случилось: две минуты назад.",
    # s04
    "Сегодня мы собираем эту сигнализацию. Одна новая деталь, остальное схема с прошлого раза.",
    # s05
    "Этот белый купол это датчик движения. Он ничего не излучает. Он просто следит за теплом.",
    # s06
    "Всё тёплое светится в инфракрасном: ваша рука, кошка, чашка чая. Мы этого свечения не видим, а датчик видит.",
    # s07
    "Купол это линза из множества маленьких окошек. Каждое смотрит на свой кусок комнаты, как ряд фонариков.",
    # s08
    "Когда что-то тёплое переходит из одного окошка в другое, датчик замечает перемену, и его выходной пин включается.",
    # s09
    "Так что для нашего кода весь датчик это просто большой палец вверх, когда что-то двинулось, и вниз, когда нет.",
    # s10
    "Сбоку два оранжевых регулятора. Один задаёт, как долго длится «да», другой как далеко он видит.",
    # s11
    "Совет: после включения дайте ему около тридцати секунд на прогрев. До этого он может говорить «да» просто так.",
    # s12
    "Давайте подключим. Экран, кнопка и зуммер остаются ровно там, где были.",
    # s13
    "У датчика три ножки. Красный провод несёт пять вольт с пина V-in платы, а чёрный идёт на землю.",
    # s14
    "Средняя ножка это ответ. Фиолетовый провод ведёт её к пину тридцать три.",
    # s15
    "И не волнуйтесь: ответ выходит на трёх целых трёх десятых вольта, это безопасно для нашей платы.",
    # s16
    "Читать его можно одной строкой: digital read на пине тридцать три. High значит движение.",
    # s17
    "Но сигнализации нужен план, поэтому снова шаги, как в нашей стиральной машине: выключено, выход, на охране и тревога.",
    # s18
    "Нажимаете кнопку, и начинается обратный отсчёт, с тихим щелчком каждую секунду, чтобы вы успели выйти.",
    # s19
    "На нуле охранник включён. Теперь он ждёт только одного: чтобы датчик сказал «да».",
    # s20
    "Когда это случается, включается сирена: две ноты, меняющиеся четыре раза в секунду, чтобы звучало как настоящая тревога.",
    # s21
    "Нажмите кнопку, чтобы её выключить. Или она сама замолчит через пятнадцать секунд, чтобы соседи не сердились.",
    # s22
    "Теперь самое умное. В момент движения мы ставим штамп времени, как на парковочном талоне из девятого эпизода.",
    # s23
    "Это одна строка: last motion равно millis. Millis это секундомер платы с момента включения.",
    # s24
    "Позже now минус last motion говорит, как давно это было. Делим на шестьдесят тысяч, и получаем минуты.",
    # s25
    "И экран может сказать: замечено дважды, последний раз три минуты назад.",
    # s26
    "Быстрый вопрос: в вашем наборе есть второй зуммер, почти такой же. В чём разница?",
    # s27
    "Наш пассивный: маленький динамик, который играет любую ноту, что мы пошлём. Активный это музыкальная шкатулка со своей пищалкой внутри: подали питание, и он играет свой единственный писк.",
    # s28
    "Проще, но сирены не будет. Поэтому в сигнализации стоит пассивный.",
    # s29
    "Давайте проверим. Я включаю охрану, идёт отсчёт, и я выхожу из комнаты.",
    # s30
    "Рука крадётся к банке с печеньем... поймана!",
    # s31
    "Возвращаюсь и нажимаю кнопку: замечено один раз, последний раз двенадцать секунд назад.",
    # s32
    "Частая проблема: сигнализация срабатывает сразу после включения. Обычно датчик ещё прогревается, или регулятор времени держит «да» слишком долго.",
    # s33
    "Поэтому ждите тридцать секунд после включения и выкрутите регулятор времени до минимума. Остальное сделает наш код.",
    # s34
    "Ваше задание. Сохраните число пойманных даже после отключения питания, с помощью Preferences, как в прошлом эпизоде.",
    # s35
    "Полный код и решение лежат в папке урока, ссылка ниже. Что бы вы охраняли с её помощью? Напишите в комментариях.",
    # s36
    "В следующий раз вы управляете этой платой с телефона, без приложения и без роутера. До встречи.",
]
L["de"] = [
    # s01
    "Mein Schreibtisch hat jetzt einen Wächter. Ich schalte ihn scharf, und ich habe zehn Sekunden, um zu gehen.",
    # s02
    "Dann schleicht sich eine Hand zum Keksglas... und wird sofort erwischt.",
    # s03
    "Und wenn ich zurückkomme, sagt er mir sogar, wann es passiert ist: vor zwei Minuten.",
    # s04
    "Heute bauen wir diese Bewegungsalarmanlage. Ein neues Teil, der Rest ist die Schaltung von letztem Mal.",
    # s05
    "Diese weiße Kuppel ist ein Bewegungssensor. Er sendet nichts aus. Er achtet nur auf Wärme.",
    # s06
    "Alles Warme leuchtet im Infrarot: deine Hand, eine Katze, eine Tasse Tee. Wir sehen dieses Leuchten nicht, aber dieser Sensor schon.",
    # s07
    "Die Kuppel ist eine Linse aus vielen kleinen Fenstern. Jedes schaut auf einen anderen Ausschnitt des Raums, wie eine Reihe von Taschenlampen.",
    # s08
    "Wenn etwas Warmes von einem Fenster zum nächsten wandert, bemerkt der Sensor die Änderung, und sein Antwortpin schaltet ein.",
    # s09
    "Für unseren Code ist der ganze Sensor also nur ein Daumen nach oben, wenn sich etwas bewegt hat, und ein Daumen nach unten, wenn nicht.",
    # s10
    "An der Seite sitzen zwei orangefarbene Drehknöpfe. Einer legt fest, wie lange das Ja anhält, der andere, wie weit er sehen kann.",
    # s11
    "Ein Tipp: Gib ihm nach dem Einschalten etwa dreißig Sekunden zum Aufwärmen. Bis dahin sagt er vielleicht grundlos Ja.",
    # s12
    "Verkabeln wir ihn. Bildschirm, Taster und Buzzer bleiben genau da, wo sie waren.",
    # s13
    "Der Sensor hat drei Beine. Ein rotes Kabel bringt fünf Volt vom V-in-Pin des Boards, und ein schwarzes Kabel geht an Masse.",
    # s14
    "Das mittlere Bein ist die Antwort. Ein lila Kabel führt sie zu Pin dreiunddreißig.",
    # s15
    "Und keine Sorge: Die Antwort kommt mit drei Komma drei Volt heraus, sicher für unser Board.",
    # s16
    "Ihn zu lesen ist eine Zeile: digital read an Pin dreiunddreißig. High heißt Bewegung.",
    # s17
    "Aber ein Alarm braucht einen Plan, also nutzen wir wieder Schritte, wie bei unserer Waschmaschine: aus, Weggehen, scharf und Alarm.",
    # s18
    "Drück den Taster, und der Countdown startet, mit einem winzigen Ticken jede Sekunde, damit du Zeit hast, hinauszugehen.",
    # s19
    "Bei null ist der Wächter scharf. Jetzt wartet er auf nur eins: dass der Sensor Ja sagt.",
    # s20
    "Tut er das, startet die Sirene: zwei Töne, die viermal pro Sekunde wechseln, damit es wirklich nach Alarm klingt.",
    # s21
    "Drück den Taster, um sie zu stoppen. Oder sie hört nach fünfzehn Sekunden von selbst auf, damit die Nachbarn freundlich bleiben.",
    # s22
    "Jetzt der clevere Teil. Im Moment der Bewegung stempeln wir die Zeit, wie das Parkticket aus Folge neun.",
    # s23
    "Es ist eine Zeile: last motion gleich millis. Millis ist die Stoppuhr des Boards seit dem Einschalten.",
    # s24
    "Später sagt uns now minus last motion, wie lange es her ist. Teile durch sechzigtausend, und du hast Minuten.",
    # s25
    "So kann der Bildschirm sagen: zweimal gesehen, zuletzt vor drei Minuten.",
    # s26
    "Kurze Frage: Dein Kit hat einen zweiten Buzzer, der fast gleich aussieht. Was ist der Unterschied?",
    # s27
    "Unserer ist passiv: ein kleiner Lautsprecher, der jede Note spielt, die wir senden. Der aktive ist eine Spieluhr mit eigenem Piepser darin: Strom an, und er spielt seinen einen festen Piepton.",
    # s28
    "Einfacher, aber keine Sirene. Deshalb nutzt der Alarm den passiven.",
    # s29
    "Testen wir es. Ich schalte scharf, der Countdown läuft, und ich gehe aus dem Raum.",
    # s30
    "Eine Hand schleicht zum Keksglas... erwischt!",
    # s31
    "Ich komme zurück und drücke den Taster: einmal gesehen, zuletzt vor zwölf Sekunden.",
    # s32
    "Ein häufiges Problem: Der Alarm geht direkt nach dem Scharfschalten los. Meist wärmt sich der Sensor noch auf, oder der Zeitknopf hält das Ja zu lange.",
    # s33
    "Warte also dreißig Sekunden nach dem Einschalten und dreh den Zeitknopf ganz herunter. Den Rest erledigt unser Code.",
    # s34
    "Du bist dran. Behalte die Anzahl der Erwischten auch nach dem Abziehen, mit Preferences, wie in der letzten Folge.",
    # s35
    "Der vollständige Code und die Lösung liegen im Lektionsordner, Link unten. Was würdest du damit bewachen? Schreib es in die Kommentare.",
    # s36
    "Beim nächsten Mal steuerst du dieses Board vom Handy aus, ohne App und ohne Router. Bis dann.",
]
L["fr"] = [
    # s01
    "Mon bureau a maintenant un gardien. Je l'arme, et j'ai dix secondes pour partir.",
    # s02
    "Puis une main s'approche du pot de biscuits... et se fait attraper aussitôt.",
    # s03
    "Et quand je reviens, il me dit même quand c'est arrivé : il y a deux minutes.",
    # s04
    "Aujourd'hui, on construit cette alarme de mouvement. Une seule pièce nouvelle, le reste est le circuit de la dernière fois.",
    # s05
    "Ce dôme blanc est un capteur de mouvement. Il n'envoie rien. Il surveille seulement la chaleur.",
    # s06
    "Tout ce qui est chaud brille en infrarouge : ta main, un chat, une tasse de thé. On ne voit pas cette lueur, mais ce capteur, si.",
    # s07
    "Le dôme est une lentille faite de nombreuses petites fenêtres. Chacune regarde une tranche différente de la pièce, comme une rangée de lampes de poche.",
    # s08
    "Quand quelque chose de chaud passe d'une fenêtre à la suivante, le capteur remarque le changement, et sa broche de réponse s'active.",
    # s09
    "Pour notre code, tout le capteur est donc un pouce levé quand quelque chose a bougé, et un pouce baissé quand rien n'a bougé.",
    # s10
    "Sur le côté, il y a deux boutons orange. L'un règle combien de temps le oui dure, l'autre jusqu'où il voit.",
    # s11
    "Un conseil : après la mise sous tension, laisse-lui une trentaine de secondes pour chauffer. Avant, il peut dire oui sans raison.",
    # s12
    "Câblons-le. L'écran, le bouton et le buzzer restent exactement où ils étaient.",
    # s13
    "Le capteur a trois pattes. Un fil rouge apporte cinq volts depuis la broche V-in de la carte, et un fil noir va à la masse.",
    # s14
    "La patte du milieu est la réponse. Un fil violet l'emmène à la broche trente-trois.",
    # s15
    "Et pas d'inquiétude : la réponse sort à trois virgule trois volts, sans danger pour notre carte.",
    # s16
    "La lire tient en une ligne : digital read sur la broche trente-trois. High veut dire mouvement.",
    # s17
    "Mais une alarme a besoin d'un plan, alors on utilise encore des étapes, comme notre machine à laver : éteint, départ, armé et alarme.",
    # s18
    "Appuie sur le bouton, et le compte à rebours démarre, avec un petit tic chaque seconde, pour que tu aies le temps de sortir.",
    # s19
    "À zéro, le gardien est armé. Maintenant il n'attend qu'une chose : que le capteur dise oui.",
    # s20
    "Quand c'est le cas, la sirène démarre : deux notes, qui alternent quatre fois par seconde, pour que ça sonne vraiment comme une alarme.",
    # s21
    "Appuie sur le bouton pour l'arrêter. Ou elle s'arrête toute seule après quinze secondes, pour que les voisins restent aimables.",
    # s22
    "Maintenant la partie astucieuse. Au moment du mouvement, on tamponne l'heure, comme le ticket de parking de l'épisode neuf.",
    # s23
    "Une seule ligne : last motion égale millis. Millis est le chronomètre de la carte depuis la mise sous tension.",
    # s24
    "Plus tard, now moins last motion nous dit il y a combien de temps. Divise par soixante mille, et tu as des minutes.",
    # s25
    "L'écran peut donc dire : vu deux fois, la dernière il y a trois minutes.",
    # s26
    "Petite question : ton kit a un deuxième buzzer qui ressemble presque au premier. Quelle est la différence ?",
    # s27
    "Le nôtre est passif : un petit haut-parleur qui joue n'importe quelle note envoyée. L'actif est une boîte à musique avec son propre bipeur à l'intérieur : alimente-le, et il joue son seul bip fixe.",
    # s28
    "Plus simple, mais pas de sirène. C'est pourquoi l'alarme utilise le passif.",
    # s29
    "Testons. Je l'arme, le compte à rebours tourne, et je sors de la pièce.",
    # s30
    "Une main s'approche du pot de biscuits... attrapée !",
    # s31
    "Je reviens et j'appuie sur le bouton : vu une fois, la dernière il y a douze secondes.",
    # s32
    "Un problème courant : l'alarme se déclenche juste après l'armement. Souvent le capteur chauffe encore, ou le bouton de durée garde le oui trop longtemps.",
    # s33
    "Alors attends trente secondes après la mise sous tension, et tourne le bouton de durée au minimum. Notre code fait le reste.",
    # s34
    "À toi de jouer. Garde le nombre d'attrapés même après le débranchement, avec Preferences, comme à l'épisode précédent.",
    # s35
    "Le code complet et la solution sont dans le dossier de la leçon, lien ci-dessous. Que garderais-tu avec ça ? Dis-le en commentaire.",
    # s36
    "La prochaine fois, tu commandes cette carte depuis ton téléphone, sans appli et sans routeur. À bientôt.",
]
L["vi"] = [
    # s01
    "Bàn của tôi giờ có một người bảo vệ. Tôi bật chế độ canh, và tôi có mười giây để rời đi.",
    # s02
    "Rồi một bàn tay rón rén tới lọ bánh quy... và bị bắt ngay lập tức.",
    # s03
    "Và khi tôi quay lại, nó còn cho biết chuyện xảy ra lúc nào: hai phút trước.",
    # s04
    "Hôm nay ta làm chiếc báo động chuyển động này. Một linh kiện mới, còn lại là mạch của lần trước.",
    # s05
    "Chiếc vòm trắng này là cảm biến chuyển động. Nó không phát ra gì cả. Nó chỉ canh hơi ấm.",
    # s06
    "Mọi thứ ấm đều phát sáng trong tia hồng ngoại: bàn tay bạn, một con mèo, một tách trà. Ta không thấy ánh sáng đó, nhưng cảm biến này thì thấy.",
    # s07
    "Chiếc vòm là một thấu kính gồm nhiều ô cửa nhỏ. Mỗi ô nhìn một lát khác nhau của căn phòng, như một hàng đèn pin.",
    # s08
    "Khi một vật ấm di chuyển từ ô này sang ô kế tiếp, cảm biến nhận ra sự thay đổi, và chân trả lời của nó bật lên.",
    # s09
    "Vì vậy với mã của ta, cả cảm biến chỉ là ngón cái giơ lên khi có gì đó động đậy, và ngón cái chúc xuống khi không.",
    # s10
    "Bên cạnh có hai núm màu cam. Một núm đặt việc có kéo dài bao lâu, núm kia đặt nó nhìn được xa đến đâu.",
    # s11
    "Một mẹo: sau khi bật nguồn, hãy cho nó khoảng ba mươi giây để khởi động. Trước đó nó có thể nói có mà không có lý do.",
    # s12
    "Ta nối dây nhé. Màn hình, nút nhấn và còi vẫn nằm đúng chỗ cũ.",
    # s13
    "Cảm biến có ba chân. Một dây đỏ đưa năm vôn từ chân V-in của bo mạch, và một dây đen nối xuống đất.",
    # s14
    "Chân giữa là câu trả lời. Một dây tím đưa nó tới chân ba mươi ba.",
    # s15
    "Và đừng lo: câu trả lời ra ở ba phẩy ba vôn, an toàn cho bo mạch của ta.",
    # s16
    "Đọc nó chỉ một dòng: digital read ở chân ba mươi ba. High nghĩa là có chuyển động.",
    # s17
    "Nhưng báo động cần một kế hoạch, nên ta lại dùng các bước, như chiếc máy giặt của ta: tắt, rời đi, đã canh, và báo động.",
    # s18
    "Nhấn nút, và đếm ngược bắt đầu, với một tiếng tích nhỏ mỗi giây, để bạn có thời gian đi ra.",
    # s19
    "Về không, người bảo vệ đã canh. Giờ nó chỉ chờ đúng một điều: cảm biến nói có.",
    # s20
    "Khi điều đó xảy ra, còi hú bắt đầu: hai nốt, đổi bốn lần mỗi giây, để nghe đúng là báo động.",
    # s21
    "Nhấn nút để tắt nó. Hoặc nó tự tắt sau mười lăm giây, để hàng xóm vẫn thân thiện.",
    # s22
    "Giờ là phần khéo léo. Ngay lúc có chuyển động, ta đóng dấu thời gian, như tấm vé đỗ xe ở tập chín.",
    # s23
    "Chỉ một dòng: last motion bằng millis. Millis là đồng hồ bấm giờ của bo mạch từ lúc bật nguồn.",
    # s24
    "Sau đó, now trừ last motion cho ta biết đã bao lâu. Chia cho sáu mươi nghìn, và bạn có số phút.",
    # s25
    "Nhờ vậy màn hình có thể nói: thấy hai lần, lần cuối ba phút trước.",
    # s26
    "Một câu hỏi nhanh: bộ kit của bạn có chiếc còi thứ hai trông gần giống. Khác nhau chỗ nào?",
    # s27
    "Còi của ta là thụ động: một chiếc loa nhỏ phát bất kỳ nốt nào ta gửi. Còi chủ động là hộp nhạc có bộ kêu riêng bên trong: cấp điện là nó phát một tiếng bíp cố định.",
    # s28
    "Dễ hơn, nhưng không có còi hú. Vì thế báo động dùng loại thụ động.",
    # s29
    "Ta thử nhé. Tôi bật canh, đếm ngược chạy, và tôi bước ra khỏi phòng.",
    # s30
    "Một bàn tay rón rén tới lọ bánh quy... bị bắt rồi!",
    # s31
    "Tôi quay lại và nhấn nút: thấy một lần, lần cuối mười hai giây trước.",
    # s32
    "Một vấn đề thường gặp: báo động kêu ngay sau khi bạn bật canh. Thường là cảm biến vẫn đang khởi động, hoặc núm thời gian giữ chữ có quá lâu.",
    # s33
    "Vì vậy hãy chờ ba mươi giây sau khi bật nguồn, và vặn núm thời gian xuống thấp nhất. Phần còn lại mã của ta lo.",
    # s34
    "Đến lượt bạn. Giữ lại số lần bắt được ngay cả sau khi rút điện, bằng Preferences, như tập trước.",
    # s35
    "Toàn bộ mã và lời giải nằm trong thư mục bài học, liên kết bên dưới. Bạn sẽ canh gì bằng nó? Hãy kể trong phần bình luận.",
    # s36
    "Lần sau, bạn điều khiển bo mạch này từ điện thoại, không cần ứng dụng và không cần router. Hẹn gặp lại.",
]
L["ja"] = [
    # s01
    "僕の机に番人ができました。作動させると、出ていくまで十秒あります。",
    # s02
    "すると、一本の手がクッキーの瓶にそっと伸びて... すぐに捕まります。",
    # s03
    "そして戻ってくると、いつ起きたかまで教えてくれます。二分前です。",
    # s04
    "今日はこの動きアラームを作ります。新しい部品は一つだけで、あとは前回の回路です。",
    # s05
    "この白いドームは人感センサーです。何も発しません。ただ暖かさを見張っています。",
    # s06
    "暖かいものはすべて赤外線で光っています。あなたの手も、猫も、お茶のカップも。その光は見えませんが、このセンサーには見えます。",
    # s07
    "ドームは、たくさんの小さな窓でできたレンズです。それぞれが部屋の別の一切れを見ていて、懐中電灯が並んだようです。",
    # s08
    "暖かいものが一つの窓から次の窓へ動くと、センサーは変化に気づき、答えのピンがオンになります。",
    # s09
    "つまりコードにとって、センサー全体は、何かが動いたら親指を上げ、動かなければ親指を下げるだけです。",
    # s10
    "側面にはオレンジ色のつまみが二つあります。一つは「はい」が続く長さ、もう一つはどこまで遠くが見えるかを決めます。",
    # s11
    "ひとつコツです。電源を入れたら、三十秒ほど温まるのを待ってください。それまでは理由なく「はい」と言うことがあります。",
    # s12
    "配線しましょう。画面、ボタン、ブザーは、これまでとまったく同じ場所のままです。",
    # s13
    "センサーの足は三本です。赤い線はボードのVinピンから五ボルトを運び、黒い線はグラウンドへ行きます。",
    # s14
    "真ん中の足が答えです。紫の線で三十三番ピンへつなぎます。",
    # s15
    "心配はいりません。答えは三・三ボルトで出てくるので、ボードに安全です。",
    # s16
    "読むのは一行です。三十三番ピンでdigital read。Highは動きがあったという意味です。",
    # s17
    "でもアラームには計画が必要です。洗濯機のときのように、またステップを使います。オフ、外出、警戒、そしてアラームです。",
    # s18
    "ボタンを押すとカウントダウンが始まり、一秒ごとに小さなチクという音が鳴るので、外へ出る時間があります。",
    # s19
    "ゼロで番人が警戒状態になります。あとは一つのことだけを待ちます。センサーが「はい」と言うことです。",
    # s20
    "それが起きるとサイレンが始まります。二つの音が一秒に四回切り替わり、本当にアラームらしく聞こえます。",
    # s21
    "止めるにはボタンを押します。あるいは十五秒で自動的に止まるので、ご近所とも仲良くいられます。",
    # s22
    "ここからが賢い部分です。動きがあった瞬間に時刻をスタンプします。第九回の駐車券のようにです。",
    # s23
    "一行です。last motion イコール millis。millisは、電源を入れてからのボードのストップウォッチです。",
    # s24
    "あとで、now引くlast motionで、どれだけ前かがわかります。六万で割れば、分になります。",
    # s25
    "だから画面はこう言えます。二回検知、最後は三分前。",
    # s26
    "ここで質問です。キットには、ほとんど同じ見た目の二つ目のブザーがあります。何が違うのでしょう。",
    # s27
    "僕たちのはパッシブです。送った音をそのまま鳴らす小さなスピーカーです。アクティブは中に自前の発音体があるオルゴールで、電源を入れると決まった一つのビープ音を鳴らします。",
    # s28
    "簡単ですが、サイレンは鳴らせません。だからアラームにはパッシブを使います。",
    # s29
    "試してみましょう。作動させて、カウントダウンが進み、僕は部屋を出ます。",
    # s30
    "一本の手がクッキーの瓶にそっと伸びて... 捕まりました！",
    # s31
    "戻ってボタンを押します。一回検知、最後は十二秒前。",
    # s32
    "よくある問題です。作動させた直後にアラームが鳴る。たいていはセンサーがまだ温まっているか、時間のつまみが「はい」を長く保ちすぎています。",
    # s33
    "なので、電源を入れて三十秒待ち、時間のつまみをいちばん下まで回してください。あとはコードがやってくれます。",
    # s34
    "あなたの番です。検知した回数を、プラグを抜いても残してください。前回と同じPreferencesを使います。",
    # s35
    "完全なコードと答えはレッスンフォルダにあります。リンクは下です。これで何を見張りますか？ コメントで教えてください。",
    # s36
    "次回は、このボードをスマホから操作します。アプリもルーターもいりません。ではまた。",
]

if __name__ == "__main__":
    out = ROOT / "subs"
    out.mkdir(exist_ok=True)
    for lang, lines in L.items():
        assert len(lines) == len(IDS), (lang, len(lines), len(IDS))
        seg = dict(zip(IDS, lines))
        (out / f"{lang}.json").write_text(json.dumps({"lang": lang, "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("subs written:", ", ".join(L), f"({len(IDS)} segments each)")
