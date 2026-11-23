"""Source of video/ep10/subs/<lang>.json (subtitle-only languages: id ar ru de fr vi ja).
Follows the "sub" field of script.json (digits, code names) where present, else "text".
en/tr subtitles come from script.json; hi/pt/es subtitles are the dub texts themselves (video/ep10/dub/*.json),
see PRODUCTION_GUIDELINES.md section 6.
Usage: python video/ep10/make_subs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

L = {}
L["id"] = [
    # s01
    "Tunggu... MULAI! Dua ratus empat belas milidetik. Rekor baru.",
    # s02
    "Sekarang lihat ini. Aku mencabut kabelnya. Layar jadi gelap, board-nya mati total.",
    # s03
    "Aku colok lagi... dan rekornya masih ada. Board mengingatnya, padahal tanpa daya sama sekali.",
    # s04
    "Hari ini kita buat game ini dari nol: layar sungguhan, bunyi bip sungguhan, dan rekor yang tak pernah lupa. Kamu hanya butuh starter kit dan sekitar dua puluh menit.",
    # s05
    "Kenali komponen baru pertama: layar mungil, lebarnya kurang dari satu inci.",
    # s06
    "Ada delapan ribu titik kecil, dan setiap titik menyalakan cahayanya sendiri. Karena itu hitam di layar ini benar-benar hitam: titik-titiknya memang mati.",
    # s07
    "Dan layar ini hanya butuh empat kabel. Dua untuk daya. Dua lainnya membawa semua gambar.",
    # s08
    "Kedua kabel ini bekerja seperti grup chat. Satu kabel membawa pesan, bit demi bit. Kabel satunya memberi ketukan, supaya kedua pihak membaca tiap bit di saat yang sama.",
    # s09
    "Setiap perangkat di chat punya nama sendiri, sebuah alamat singkat. Layar kita menjawab pada alamatnya, jadi nanti kita bisa menambah komponen lain di dua kabel yang sama.",
    # s10
    "Komponen baru kedua adalah buzzer kecil ini. Ini buzzer pasif: ia diam sampai kita memberinya sebuah nada.",
    # s11
    "Di dalamnya, sebuah cakram logam tipis melengkung bolak-balik. Lengkungan cepat menghasilkan bip tinggi, yang lambat menghasilkan dengung rendah.",
    # s12
    "Dan teman lama kita, tombol tekan, ikut bergabung. Ia hanya pindah ke pin baru, karena layar memakai pin lamanya.",
    # s13
    "Ayo kita rangkai. Setiap lubang punya nomor dan huruf tercetak, dan semuanya muncul di layar, jadi kamu bisa menyalin tiap langkah.",
    # s14
    "Pertama, daya. Kabel merah membawa tiga koma tiga volt ke jalur plus di belakang, dan kabel hitam membawa ground ke jalur minus.",
    # s15
    "Sekarang layarnya. Keempat kakinya masuk ke satu kolom, berdampingan. Lalu dua kabel pendek memberinya daya dari jalur-jalur itu.",
    # s16
    "Dua kabel chat: hijau dari pin dua puluh dua ke kaki clock, dan biru dari pin dua puluh satu ke kaki data.",
    # s17
    "Tombol dipasang melintasi celah tengah. Kabel kuning dari pin sembilan belas ke satu sisi, dan sisi lainnya ke ground.",
    # s18
    "Terakhir, buzzer di papan depan. Oranye dari pin tiga puluh dua ke kaki plusnya, dan kaki lainnya ke ground.",
    # s19
    "Itulah seluruh rangkaiannya: satu layar, satu tombol, satu buzzer. Jeda di sini kalau mau membandingkan dengan rangkaianmu.",
    # s20
    "Untuk bicara dengan layar, kita pakai library gratis. Kamu memasangnya sekali saja, lewat Library Manager.",
    # s21
    "Inilah trik layar ini. Saat kita print, belum ada yang muncul. Board menggambar di papan tulis di balik tirai.",
    # s22
    "Baru ketika kita memanggil display, tirainya terbuka dan seluruh gambar muncul sekaligus. Tanpa kedip, tanpa kata yang setengah tergambar.",
    # s23
    "Jadi kita bungkus dalam satu fungsi bantu kecil bernama show. Ia membersihkan papan, menulis baris kecil di atas, baris besar di tengah, lalu membuka tirai.",
    # s24
    "Satu panggilan, dan layar menampilkan apa pun yang kita mau.",
    # s25
    "Game-nya sendiri punya empat langkah, seperti mesin cuci: siap, tunggu, mulai, dan hasil.",
    # s26
    "Saat kamu menekan, kita pilih waktu tunggu acak, antara satu setengah dan empat detik, supaya tak ada yang bisa menebak saatnya.",
    # s27
    "Saat waktunya habis, layar menampilkan GO dan buzzer berbunyi. Sejak saat itu, jamnya berjalan.",
    # s28
    "Bunyi bip itu cuma satu baris: tone, dengan pin, setinggi apa nadanya, dan berapa lama.",
    # s29
    "Tekananmu menghentikan jam. Waktu sejak GO adalah reaksimu, dan langsung tampil di layar.",
    # s30
    "Dan kalau kamu menekan terlalu cepat? Itu false start. Dengung rendah, lalu coba lagi.",
    # s31
    "Ayo main beberapa ronde. Tiga ratus lima puluh... lumayan. Dua ratus delapan puluh... lebih baik.",
    # s32
    "Sekarang bagian terbaiknya. Biasanya, setiap variabel hidup di memori yang melupakan semuanya saat daya putus. Seperti sticky note di meja yang disapu bersih tiap malam.",
    # s33
    "Tapi ESP32 juga punya laci kecil yang menyimpan barang tanpa daya. Namanya Preferences.",
    # s34
    "Saat kamu memecahkan rekor, satu baris menaruh waktu baru ke laci, dengan label: best.",
    # s35
    "Dan saat board menyala, satu baris mengambilnya kembali. Kalau laci masih kosong, kita dapat angka raksasa, jadi ronde pertama selalu jadi rekor.",
    # s36
    "Kita buktikan. Dua ratus empat belas, rekor baru. Cabut... colok lagi... masih dua ratus empat belas.",
    # s37
    "Satu tips: simpan hanya saat ada rekor baru. Menyimpan tiap ronde akan menimpa waktu terbaikmu dengan waktu yang lambat, dan lacinya lebih cepat aus.",
    # s38
    "Giliranmu. Buat tombol menghapus rekor saat ditahan tiga detik di layar siap. Kamu sudah tahu cara mengukur tekanan panjang.",
    # s39
    "Kode lengkap dan solusinya ada di folder pelajaran, tautannya di bawah. Tulis waktu terbaikmu di komentar.",
    # s40
    "Lain kali, board mendapat mata: sensor gerak yang mengubah rangkaian ini jadi alarm. Subscribe, supaya tidak ketinggalan. Sampai jumpa di sana.",
]
L["ar"] = [
    # s01
    "انتظر... انطلق! مئتان وأربعة عشر ميلي ثانية. رقم قياسي جديد.",
    # s02
    "والآن شاهد هذا. أسحب الكابل. تُظلم الشاشة، واللوحة مطفأة تمامًا.",
    # s03
    "أعيد توصيله... والرقم القياسي ما زال هناك. تذكّرته اللوحة دون أي كهرباء.",
    # s04
    "اليوم نبني هذه اللعبة من الصفر: شاشة حقيقية، وصفّارة حقيقية، ورقم قياسي لا ينسى أبدًا. تحتاج فقط إلى طقم البداية وحوالي عشرين دقيقة.",
    # s05
    "تعرّف على أول قطعة جديدة: شاشة صغيرة جدًا، عرضها أقل من بوصة واحدة.",
    # s06
    "فيها ثمانية آلاف نقطة صغيرة، وكل نقطة تصنع ضوءها بنفسها. لهذا يكون الأسود في هذه الشاشة أسود حقًا: النقاط مطفأة ببساطة.",
    # s07
    "ولا تحتاج إلا إلى أربعة أسلاك. اثنان للطاقة. والاثنان الآخران يحملان كل الصور.",
    # s08
    "هذان السلكان يعملان مثل مجموعة محادثة. سلك يحمل الرسالة، بتًّا بعد بتّ. والآخر يعطي الإيقاع، فيقرأ الطرفان كل بتّ في اللحظة نفسها.",
    # s09
    "لكل جهاز في المحادثة اسمه الخاص، أي عنوان قصير. وشاشتنا تردّ على عنوانها، فيمكننا لاحقًا إضافة قطع أخرى على السلكين نفسيهما.",
    # s10
    "القطعة الجديدة الثانية هي هذا الجرس الصغير. إنه جرس سلبي: يبقى صامتًا حتى نعطيه نغمة.",
    # s11
    "في داخله قرص معدني رفيع ينحني ذهابًا وإيابًا. الانحناء السريع يعطي صفيرًا حادًا، والبطيء يعطي طنينًا غليظًا.",
    # s12
    "وينضم صديقنا القديم، زر الضغط. فقط ينتقل إلى طرف جديد، لأن الشاشة تحتاج طرفه القديم.",
    # s13
    "لنبدأ التوصيل. كل ثقب عليه رقم وحرف مطبوعان، وسترونهما على الشاشة، فيمكنك نسخ كل خطوة.",
    # s14
    "أولًا، الطاقة. سلك أحمر يأخذ ثلاثة فاصل ثلاثة فولت إلى خط الموجب في الخلف، وسلك أسود يأخذ الأرضي إلى خط السالب.",
    # s15
    "الآن الشاشة. أرجلها الأربع تدخل في عمود واحد، جنبًا إلى جنب. ثم سلكان قصيران يعطيانها الطاقة من هذين الخطين.",
    # s16
    "سلكا المحادثة: الأخضر من الطرف اثنين وعشرين إلى رجل الساعة، والأزرق من الطرف واحد وعشرين إلى رجل البيانات.",
    # s17
    "الزر يجلس عبر الفجوة الوسطى. الأصفر من الطرف تسعة عشر إلى أحد جانبيه، والجانب الآخر إلى الأرضي.",
    # s18
    "أخيرًا، الجرس على اللوحة الأمامية. البرتقالي من الطرف اثنين وثلاثين إلى رجله الموجبة، ورجله الأخرى إلى الأرضي.",
    # s19
    "هذه هي الدارة كاملة: شاشة واحدة، وزر واحد، وجرس واحد. أوقف الفيديو هنا إن أردت مقارنتها بدارتك.",
    # s20
    "لنتحدث مع الشاشة نستخدم مكتبة مجانية. تثبّتها مرة واحدة من مدير المكتبات.",
    # s21
    "وهنا حيلة هذه الشاشة. حين نطبع، لا يظهر شيء بعد. اللوحة ترسم على سبورة خلف ستارة.",
    # s22
    "فقط حين نستدعي display، تُفتح الستارة وتظهر الصورة كلها دفعة واحدة. بلا وميض، وبلا كلمات نصف مرسومة.",
    # s23
    "لذلك نغلّف ذلك في دالة مساعدة صغيرة اسمها show. تمسح السبورة، وتكتب سطرًا صغيرًا في الأعلى وسطرًا كبيرًا في الوسط، ثم تفتح الستارة.",
    # s24
    "استدعاء واحد، وتقول الشاشة ما نريد.",
    # s25
    "اللعبة نفسها فيها أربع خطوات، مثل الغسالة: جاهز، انتظار، انطلق، والنتيجة.",
    # s26
    "عندما تضغط، نختار زمن انتظار عشوائيًا، بين ثانية ونصف وأربع ثوانٍ، حتى لا يستطيع أحد تخمين اللحظة.",
    # s27
    "عندما ينتهي الوقت، تعرض الشاشة GO ويطلق الجرس صوته. ومن تلك اللحظة، الساعة تعمل.",
    # s28
    "الصفير سطر واحد: tone، مع الطرف، وارتفاع النغمة، ومدتها.",
    # s29
    "ضغطتك توقف الساعة. الزمن منذ GO هو ردّ فعلك، ويذهب مباشرة إلى الشاشة.",
    # s30
    "وإن ضغطت مبكرًا جدًا؟ تلك بداية خاطئة. طنين غليظ، ثم تحاول من جديد.",
    # s31
    "لنلعب بضع جولات. ثلاثمئة وخمسون... ليس سيئًا. مئتان وثمانون... أفضل.",
    # s32
    "والآن أجمل ما في الأمر. عادةً، كل متغيّر يعيش في ذاكرة تنسى كل شيء عندما تنقطع الكهرباء. مثل أوراق لاصقة على مكتب تُكنس كل ليلة.",
    # s33
    "لكن ESP32 يملك أيضًا درجًا صغيرًا يحفظ الأشياء دون كهرباء. اسمه Preferences.",
    # s34
    "عندما تكسر الرقم القياسي، سطر واحد يضع الزمن الجديد في الدرج، مع بطاقة اسمها: best.",
    # s35
    "وعندما تبدأ اللوحة، سطر واحد يخرجه من جديد. وإن كان الدرج فارغًا، نحصل على رقم ضخم، فتكون الجولة الأولى دائمًا رقمًا قياسيًا.",
    # s36
    "لنثبت ذلك. مئتان وأربعة عشر، رقم قياسي جديد. أفصل... أعيد التوصيل... ما زال مئتين وأربعة عشر.",
    # s37
    "نصيحة: احفظ فقط عند وجود رقم قياسي جديد. حفظ كل جولة سيمحو أفضل زمن لك بزمن بطيء، وسيبلى الدرج أسرع.",
    # s38
    "دورك الآن. اجعل الزر يمسح الرقم القياسي عند الضغط عليه ثلاث ثوانٍ في شاشة الاستعداد. أنت تعرف كيف تقيس الضغطة الطويلة.",
    # s39
    "الكود الكامل والحل في مجلد الدرس، والرابط في الأسفل. اكتب أفضل زمن لك في التعليقات.",
    # s40
    "في المرة القادمة، تحصل اللوحة على عيون: حسّاس حركة يحوّل هذه الدارة إلى إنذار. اشترك حتى لا يفوتك. أراك هناك.",
]
L["ru"] = [
    # s01
    "Ждём... СТАРТ! Двести четырнадцать миллисекунд. Новый рекорд.",
    # s02
    "А теперь смотрите. Я выдёргиваю кабель. Экран гаснет, плата полностью выключена.",
    # s03
    "Втыкаю обратно... и рекорд всё ещё здесь. Плата запомнила его совсем без питания.",
    # s04
    "Сегодня мы собираем эту игру с нуля: настоящий экран, настоящий писк и рекорд, который никогда не забывается. Вам нужен только стартовый набор и около двадцати минут.",
    # s05
    "Знакомьтесь, первая новая деталь: крошечный экран шириной меньше дюйма.",
    # s06
    "На нём восемь тысяч маленьких точек, и каждая сама излучает свет. Поэтому чёрный на этом экране по-настоящему чёрный: эти точки просто выключены.",
    # s07
    "И ему нужно всего четыре провода. Два для питания. Два других несут все картинки.",
    # s08
    "Эти два провода работают как групповой чат. По одному идёт сообщение, бит за битом. Другой задаёт ритм, чтобы обе стороны читали каждый бит в один и тот же момент.",
    # s09
    "У каждого устройства в чате есть своё имя, короткий адрес. Наш экран отзывается на свой адрес, так что позже мы сможем добавить другие детали на те же два провода.",
    # s10
    "Вторая новая деталь: этот маленький зуммер. Он пассивный: молчит, пока мы не дадим ему ноту.",
    # s11
    "Внутри тонкий металлический диск изгибается туда-сюда. Быстрые изгибы дают высокий писк, медленные низкое гудение.",
    # s12
    "И наш старый друг, кнопка, тоже в деле. Она просто переезжает на другой пин, потому что экрану нужен её прежний.",
    # s13
    "Давайте собирать. У каждого отверстия напечатаны номер и буква, вы увидите их на экране и сможете повторять каждый шаг.",
    # s14
    "Сначала питание. Красный провод несёт три целых три десятых вольта на плюсовую линию сзади, а чёрный провод несёт землю на минусовую линию.",
    # s15
    "Теперь экран. Его четыре ножки идут в один столбец, рядом друг с другом. Потом два коротких провода дают ему питание от этих линий.",
    # s16
    "Два провода чата: зелёный от пина двадцать два к ножке тактирования, и синий от пина двадцать один к ножке данных.",
    # s17
    "Кнопка стоит поперёк средней канавки. Жёлтый идёт от пина девятнадцать к одной стороне, а другая сторона идёт на землю.",
    # s18
    "И наконец, зуммер на передней плате. Оранжевый от пина тридцать два к его плюсовой ножке, а другая ножка на землю.",
    # s19
    "Вот вся схема: один экран, одна кнопка, один зуммер. Поставьте на паузу, если хотите сверить со своей.",
    # s20
    "Чтобы общаться с экраном, мы используем бесплатную библиотеку. Её устанавливают один раз, через менеджер библиотек.",
    # s21
    "Вот хитрость этого экрана. Когда мы печатаем, пока ничего не появляется. Плата рисует на доске за занавесом.",
    # s22
    "Только когда мы вызываем display, занавес открывается и вся картинка появляется разом. Без мерцания, без наполовину нарисованных слов.",
    # s23
    "Поэтому мы упаковываем это в один маленький помощник под названием show. Он стирает доску, пишет маленькую строку сверху, большую посередине и открывает занавес.",
    # s24
    "Один вызов, и экран говорит всё, что мы захотим.",
    # s25
    "В самой игре четыре шага, как в стиральной машине: готов, ждать, старт и результат.",
    # s26
    "Когда вы нажимаете, мы выбираем случайное время ожидания, где-то от полутора до четырёх секунд, чтобы никто не мог угадать момент.",
    # s27
    "Когда время вышло, экран показывает GO и пищит зуммер. С этого момента часы идут.",
    # s28
    "Писк это одна строка: tone, с пином, высотой ноты и тем, сколько она длится.",
    # s29
    "Ваше нажатие останавливает часы. Время с момента GO это ваша реакция, и оно сразу идёт на экран.",
    # s30
    "А если нажать слишком рано? Это фальстарт. Низкое гудение, и пробуете снова.",
    # s31
    "Давайте сыграем несколько раундов. Триста пятьдесят... неплохо. Двести восемьдесят... лучше.",
    # s32
    "Теперь самое интересное. Обычно каждая переменная живёт в памяти, которая забывает всё, когда пропадает питание. Как стикеры на столе, которые каждый вечер сметают.",
    # s33
    "Но у ESP32 есть ещё маленький ящик, который хранит вещи без питания. Он называется Preferences.",
    # s34
    "Когда вы побили рекорд, одна строка кладёт новое время в ящик с ярлыком: best.",
    # s35
    "А когда плата запускается, одна строка достаёт его обратно. Если ящик ещё пуст, мы получаем огромное число, так что первый раунд всегда рекорд.",
    # s36
    "Докажем. Двести четырнадцать, новый рекорд. Выдёргиваем... втыкаем обратно... всё ещё двести четырнадцать.",
    # s37
    "Один совет: сохраняйте только при новом рекорде. Если сохранять каждый раунд, лучшее время затрётся медленным, а ящик быстрее износится.",
    # s38
    "Ваша очередь. Сделайте так, чтобы кнопка стирала рекорд, если её держать три секунды на экране готовности. Вы уже умеете измерять долгое нажатие.",
    # s39
    "Полный код и решение лежат в папке урока, ссылка ниже. Напишите свой лучший результат в комментариях.",
    # s40
    "В следующий раз плата получит глаза: датчик движения, который превратит эту схему в сигнализацию. Подпишитесь, чтобы не пропустить. До встречи.",
]
L["de"] = [
    # s01
    "Warte... LOS! Zweihundertvierzehn Millisekunden. Ein neuer Rekord.",
    # s02
    "Jetzt pass auf. Ich ziehe das Kabel. Der Bildschirm wird dunkel, das Board ist komplett aus.",
    # s03
    "Ich stecke es wieder ein... und der Rekord ist immer noch da. Das Board hat ihn sich gemerkt, ganz ohne Strom.",
    # s04
    "Heute bauen wir dieses Spiel von Grund auf: ein echter Bildschirm, ein echter Piepton und ein Rekord, der nie vergisst. Du brauchst nur das Starterset und etwa zwanzig Minuten.",
    # s05
    "Das erste neue Bauteil: ein winziger Bildschirm, nicht einmal einen Zoll breit.",
    # s06
    "Er hat achttausend kleine Punkte, und jeder Punkt macht sein eigenes Licht. Deshalb ist Schwarz auf diesem Bildschirm wirklich schwarz: Die Punkte sind einfach aus.",
    # s07
    "Und er braucht nur vier Kabel. Zwei für den Strom. Die anderen beiden tragen alle Bilder.",
    # s08
    "Diese zwei Kabel funktionieren wie ein Gruppenchat. Ein Kabel trägt die Nachricht, Bit für Bit. Das andere gibt den Takt vor, damit beide Seiten jedes Bit im selben Moment lesen.",
    # s09
    "Jedes Gerät im Chat hat seinen eigenen Namen, eine kurze Adresse. Unser Bildschirm antwortet auf seine Adresse, so können wir später weitere Teile an dieselben zwei Kabel hängen.",
    # s10
    "Das zweite neue Teil ist dieser kleine Buzzer. Es ist ein passiver: Er bleibt still, bis wir ihm eine Note geben.",
    # s11
    "Innen biegt sich eine dünne Metallscheibe hin und her. Schnelles Biegen ergibt einen hohen Piepton, langsames ein tiefes Brummen.",
    # s12
    "Und unser alter Freund, der Taster, ist auch dabei. Er zieht nur auf einen neuen Pin um, weil der Bildschirm seinen alten braucht.",
    # s13
    "Lass uns verkabeln. Jedes Loch hat eine aufgedruckte Nummer und einen Buchstaben, die du auf dem Bildschirm siehst, damit du jeden Schritt nachmachen kannst.",
    # s14
    "Zuerst der Strom. Ein rotes Kabel bringt drei Komma drei Volt zur Plusleiste hinten, und ein schwarzes Kabel bringt Masse zur Minusleiste.",
    # s15
    "Jetzt der Bildschirm. Seine vier Beinchen stecken nebeneinander in einer Spalte. Dann geben ihm zwei kurze Kabel Strom von diesen Leisten.",
    # s16
    "Die zwei Chat-Kabel: Grün von Pin zweiundzwanzig zum Clock-Beinchen und Blau von Pin einundzwanzig zum Data-Beinchen.",
    # s17
    "Der Taster sitzt quer über der Mittelrille. Gelb geht von Pin neunzehn zu einer Seite, und die andere Seite geht an Masse.",
    # s18
    "Zuletzt der Buzzer auf dem vorderen Board. Orange von Pin zweiunddreißig zu seinem Plusbeinchen, und das andere Beinchen an Masse.",
    # s19
    "Das ist die ganze Schaltung: ein Bildschirm, ein Taster, ein Buzzer. Halte hier an, wenn du sie mit deiner vergleichen willst.",
    # s20
    "Um mit dem Bildschirm zu sprechen, nutzen wir eine kostenlose Bibliothek. Du installierst sie einmal, über den Bibliotheksverwalter.",
    # s21
    "Das ist der Trick dieses Bildschirms. Wenn wir etwas ausgeben, erscheint noch nichts. Das Board zeichnet auf eine Tafel hinter einem Vorhang.",
    # s22
    "Erst wenn wir display aufrufen, öffnet sich der Vorhang und das ganze Bild erscheint auf einmal. Kein Flackern, keine halb gezeichneten Wörter.",
    # s23
    "Deshalb packen wir das in einen kleinen Helfer namens show. Er löscht die Tafel, schreibt oben eine kleine Zeile, in der Mitte eine große und öffnet den Vorhang.",
    # s24
    "Ein Aufruf, und der Bildschirm sagt, was wir wollen.",
    # s25
    "Das Spiel selbst hat vier Schritte, wie eine Waschmaschine: bereit, warten, los und das Ergebnis.",
    # s26
    "Wenn du drückst, wählen wir eine zufällige Wartezeit, irgendwo zwischen anderthalb und vier Sekunden, damit niemand den Moment erraten kann.",
    # s27
    "Wenn die Zeit um ist, zeigt der Bildschirm GO und der Buzzer piept. Ab diesem Moment läuft die Uhr.",
    # s28
    "Der Piepton ist eine Zeile: tone, mit dem Pin, wie hoch die Note ist und wie lange sie dauert.",
    # s29
    "Dein Druck stoppt die Uhr. Die Zeit seit GO ist deine Reaktion, und sie geht direkt auf den Bildschirm.",
    # s30
    "Und wenn du zu früh drückst? Das ist ein Fehlstart. Ein tiefes Brummen, und du versuchst es noch einmal.",
    # s31
    "Spielen wir ein paar Runden. Dreihundertfünfzig... nicht schlecht. Zweihundertachtzig... besser.",
    # s32
    "Jetzt kommt das Beste. Normalerweise lebt jede Variable in einem Speicher, der alles vergisst, wenn der Strom weg ist. Wie Haftnotizen auf einem Schreibtisch, die jede Nacht weggefegt werden.",
    # s33
    "Aber der ESP32 hat auch eine kleine Schublade, die Dinge ohne Strom behält. Sie heißt Preferences.",
    # s34
    "Wenn du den Rekord brichst, legt eine Zeile die neue Zeit in die Schublade, mit einem Etikett: best.",
    # s35
    "Und wenn das Board startet, holt eine Zeile sie wieder heraus. Ist die Schublade noch leer, bekommen wir eine riesige Zahl, sodass die allererste Runde immer ein Rekord ist.",
    # s36
    "Beweisen wir es. Zweihundertvierzehn, neuer Rekord. Abziehen... wieder einstecken... immer noch zweihundertvierzehn.",
    # s37
    "Ein Tipp: Speichere nur bei einem neuen Rekord. Würdest du jede Runde speichern, überschriebe eine langsame Zeit deine beste, und die Schublade nutzte sich schneller ab.",
    # s38
    "Du bist dran. Lass den Taster den Rekord löschen, wenn man ihn drei Sekunden auf dem Bereit-Bildschirm hält. Du weißt schon, wie man einen langen Druck misst.",
    # s39
    "Der vollständige Code und die Lösung liegen im Lektionsordner, unten verlinkt. Poste deine Bestzeit in den Kommentaren.",
    # s40
    "Nächstes Mal bekommt das Board Augen: ein Bewegungssensor, der diesen Aufbau in eine Alarmanlage verwandelt. Abonniere, damit du es nicht verpasst. Bis dann.",
]
L["fr"] = [
    # s01
    "Attends... PARTEZ ! Deux cent quatorze millisecondes. Un nouveau record.",
    # s02
    "Maintenant, regarde ça. Je tire le câble. L'écran devient noir, la carte est complètement éteinte.",
    # s03
    "Je le rebranche... et le record est toujours là. La carte s'en est souvenue, sans aucun courant.",
    # s04
    "Aujourd'hui, on construit ce jeu à partir de zéro : un vrai écran, un vrai bip et un record qui n'oublie jamais. Il te faut seulement le kit de démarrage et une vingtaine de minutes.",
    # s05
    "Voici la première nouvelle pièce : un minuscule écran, large de moins d'un pouce.",
    # s06
    "Il a huit mille petits points, et chaque point fabrique sa propre lumière. C'est pour ça que le noir est vraiment noir sur cet écran : ces points sont simplement éteints.",
    # s07
    "Et il n'a besoin que de quatre fils. Deux pour l'alimentation. Les deux autres portent toutes les images.",
    # s08
    "Ces deux fils fonctionnent comme une conversation de groupe. Un fil porte le message, bit après bit. L'autre donne le rythme, pour que les deux côtés lisent chaque bit au même instant.",
    # s09
    "Chaque appareil de la conversation a son propre nom, une courte adresse. Notre écran répond à son adresse, donc plus tard on pourra ajouter d'autres pièces sur les deux mêmes fils.",
    # s10
    "La deuxième nouvelle pièce, c'est ce petit buzzer. C'est un buzzer passif : il reste muet tant qu'on ne lui donne pas une note.",
    # s11
    "À l'intérieur, un fin disque de métal se plie d'avant en arrière. Des plis rapides font un bip aigu, des plis lents un bourdonnement grave.",
    # s12
    "Et notre vieil ami, le bouton-poussoir, nous rejoint. Il change juste de broche, parce que l'écran a besoin de son ancienne.",
    # s13
    "Passons au câblage. Chaque trou a un numéro et une lettre imprimés, tu les verras à l'écran, donc tu pourras copier chaque étape.",
    # s14
    "D'abord, l'alimentation. Un fil rouge amène trois virgule trois volts à la ligne plus, à l'arrière, et un fil noir amène la masse à la ligne moins.",
    # s15
    "Maintenant l'écran. Ses quatre pattes vont dans une même colonne, côte à côte. Puis deux fils courts lui donnent du courant depuis ces lignes.",
    # s16
    "Les deux fils de la conversation : le vert de la broche vingt-deux à la patte d'horloge, et le bleu de la broche vingt et un à la patte de données.",
    # s17
    "Le bouton est posé à cheval sur la rainure centrale. Le jaune va de la broche dix-neuf à un côté, et l'autre côté va à la masse.",
    # s18
    "Enfin, le buzzer sur la carte de devant. L'orange va de la broche trente-deux à sa patte plus, et son autre patte à la masse.",
    # s19
    "Voilà tout le circuit : un écran, un bouton, un buzzer. Mets en pause ici si tu veux le comparer au tien.",
    # s20
    "Pour parler à l'écran, on utilise une bibliothèque gratuite. Tu l'installes une seule fois, depuis le gestionnaire de bibliothèques.",
    # s21
    "Voici l'astuce de cet écran. Quand on affiche, rien n'apparaît encore. La carte dessine sur un tableau blanc derrière un rideau.",
    # s22
    "Ce n'est que lorsqu'on appelle display que le rideau s'ouvre et que toute l'image apparaît d'un coup. Pas de scintillement, pas de mots à moitié dessinés.",
    # s23
    "Alors on emballe tout ça dans un petit assistant nommé show. Il efface le tableau, écrit une petite ligne en haut, une grande au milieu, et ouvre le rideau.",
    # s24
    "Un seul appel, et l'écran dit ce qu'on veut.",
    # s25
    "Le jeu lui-même a quatre étapes, comme un lave-linge : prêt, attente, partez, et le résultat.",
    # s26
    "Quand tu appuies, on choisit un temps d'attente au hasard, entre une seconde et demie et quatre secondes, pour que personne ne devine le moment.",
    # s27
    "Quand le temps est écoulé, l'écran affiche GO et le buzzer bipe. À partir de cet instant, le chrono tourne.",
    # s28
    "Le bip tient en une ligne : tone, avec la broche, la hauteur de la note et sa durée.",
    # s29
    "Ton appui arrête le chrono. Le temps depuis GO est ta réaction, et il va directement à l'écran.",
    # s30
    "Et si tu appuies trop tôt ? C'est un faux départ. Un bourdonnement grave, et tu réessaies.",
    # s31
    "Jouons quelques manches. Trois cent cinquante... pas mal. Deux cent quatre-vingts... mieux.",
    # s32
    "Maintenant, le meilleur. Normalement, chaque variable vit dans une mémoire qui oublie tout quand le courant disparaît. Comme des pense-bêtes sur un bureau qu'on balaie chaque nuit.",
    # s33
    "Mais l'ESP32 a aussi un petit tiroir qui garde les choses sans courant. Il s'appelle Preferences.",
    # s34
    "Quand tu bats le record, une ligne range le nouveau temps dans le tiroir, avec une étiquette : best.",
    # s35
    "Et au démarrage de la carte, une ligne le ressort. Si le tiroir est encore vide, on obtient un nombre énorme, donc la toute première manche est toujours un record.",
    # s36
    "Prouvons-le. Deux cent quatorze, nouveau record. Je débranche... je rebranche... toujours deux cent quatorze.",
    # s37
    "Un conseil : n'enregistre que lors d'un nouveau record. Enregistrer chaque manche écraserait ton meilleur temps par un temps lent, et le tiroir s'userait plus vite.",
    # s38
    "À toi de jouer. Fais en sorte que le bouton efface le record quand on le maintient trois secondes sur l'écran prêt. Tu sais déjà mesurer un appui long.",
    # s39
    "Le code complet et la solution sont dans le dossier de la leçon, lié ci-dessous. Poste ton meilleur temps dans les commentaires.",
    # s40
    "La prochaine fois, la carte reçoit des yeux : un capteur de mouvement qui transforme ce montage en alarme. Abonne-toi pour ne pas le manquer. À bientôt.",
]
L["vi"] = [
    # s01
    "Chờ nhé... BẮT ĐẦU! Hai trăm mười bốn mili giây. Kỷ lục mới.",
    # s02
    "Giờ xem này. Tôi rút dây cáp. Màn hình tắt đen, bo mạch hoàn toàn mất điện.",
    # s03
    "Tôi cắm lại... và kỷ lục vẫn còn đó. Bo mạch đã nhớ nó, dù không có chút điện nào.",
    # s04
    "Hôm nay ta làm trò chơi này từ đầu: một màn hình thật, một tiếng bíp thật, và một kỷ lục không bao giờ quên. Bạn chỉ cần bộ starter kit và khoảng hai mươi phút.",
    # s05
    "Làm quen với linh kiện mới đầu tiên: một màn hình nhỏ xíu, rộng chưa đến một inch.",
    # s06
    "Nó có tám nghìn chấm nhỏ, và mỗi chấm tự phát ra ánh sáng. Vì vậy màu đen trên màn hình này là đen thật sự: các chấm đó chỉ đơn giản là tắt.",
    # s07
    "Và nó chỉ cần bốn dây. Hai dây cấp nguồn. Hai dây còn lại mang toàn bộ hình ảnh.",
    # s08
    "Hai dây này hoạt động như một nhóm chat. Một dây chở tin nhắn, từng bit một. Dây kia giữ nhịp, để hai bên đọc mỗi bit đúng cùng một lúc.",
    # s09
    "Mỗi thiết bị trong nhóm chat có tên riêng, một địa chỉ ngắn. Màn hình của ta trả lời theo địa chỉ của nó, nên sau này ta có thể thêm linh kiện khác trên chính hai dây ấy.",
    # s10
    "Linh kiện mới thứ hai là chiếc còi nhỏ này. Đây là còi thụ động: nó im lặng cho đến khi ta đưa cho nó một nốt nhạc.",
    # s11
    "Bên trong, một đĩa kim loại mỏng uốn cong qua lại. Uốn nhanh cho tiếng bíp cao, uốn chậm cho tiếng ù trầm.",
    # s12
    "Và người bạn cũ, nút nhấn, cũng tham gia. Nó chỉ chuyển sang một chân mới, vì màn hình cần chân cũ của nó.",
    # s13
    "Bắt đầu nối dây nào. Mỗi lỗ có số và chữ in sẵn, và bạn sẽ thấy chúng trên màn hình, nên có thể làm theo từng bước.",
    # s14
    "Đầu tiên là nguồn. Một dây đỏ đưa ba phẩy ba vôn tới đường cộng ở phía sau, và một dây đen đưa đất tới đường trừ.",
    # s15
    "Giờ đến màn hình. Bốn chân của nó cắm vào một cột, cạnh nhau. Rồi hai dây ngắn cấp điện cho nó từ các đường đó.",
    # s16
    "Hai dây chat: dây xanh lá từ chân hai mươi hai tới chân clock, và dây xanh dương từ chân hai mươi mốt tới chân data.",
    # s17
    "Nút nhấn nằm vắt ngang rãnh giữa. Dây vàng đi từ chân mười chín tới một bên, và bên còn lại nối đất.",
    # s18
    "Cuối cùng, còi ở bo phía trước. Dây cam từ chân ba mươi hai tới chân cộng của nó, và chân còn lại nối đất.",
    # s19
    "Đó là toàn bộ mạch: một màn hình, một nút nhấn, một còi. Hãy dừng video ở đây nếu muốn so với mạch của bạn.",
    # s20
    "Để nói chuyện với màn hình, ta dùng một thư viện miễn phí. Bạn cài một lần, từ Library Manager.",
    # s21
    "Đây là mẹo của màn hình này. Khi ta print, chưa có gì hiện ra. Bo mạch vẽ lên một tấm bảng trắng sau tấm màn.",
    # s22
    "Chỉ khi ta gọi display, tấm màn mới mở ra và cả bức tranh hiện ra cùng lúc. Không nhấp nháy, không có chữ vẽ dở.",
    # s23
    "Nên ta gói nó vào một hàm trợ giúp nhỏ tên là show. Nó xóa bảng, viết một dòng nhỏ ở trên, một dòng lớn ở giữa, rồi mở màn.",
    # s24
    "Một lần gọi, và màn hình nói bất cứ điều gì ta muốn.",
    # s25
    "Bản thân trò chơi có bốn bước, như máy giặt: sẵn sàng, chờ, bắt đầu, và kết quả.",
    # s26
    "Khi bạn nhấn, ta chọn một thời gian chờ ngẫu nhiên, khoảng từ một giây rưỡi đến bốn giây, để không ai đoán được thời điểm.",
    # s27
    "Khi hết thời gian, màn hình hiện GO và còi kêu bíp. Từ khoảnh khắc đó, đồng hồ chạy.",
    # s28
    "Tiếng bíp chỉ là một dòng: tone, kèm chân, độ cao của nốt và thời gian kéo dài.",
    # s29
    "Cú nhấn của bạn dừng đồng hồ. Thời gian từ lúc GO là phản xạ của bạn, và nó hiện thẳng lên màn hình.",
    # s30
    "Còn nếu bạn nhấn quá sớm? Đó là xuất phát sai. Một tiếng ù trầm, rồi thử lại.",
    # s31
    "Chơi vài lượt nhé. Ba trăm năm mươi... không tệ. Hai trăm tám mươi... tốt hơn.",
    # s32
    "Giờ là phần hay nhất. Thông thường, mỗi biến sống trong bộ nhớ quên sạch mọi thứ khi mất điện. Như giấy nhớ trên bàn bị quét đi mỗi đêm.",
    # s33
    "Nhưng ESP32 còn có một ngăn kéo nhỏ giữ đồ khi không có điện. Nó tên là Preferences.",
    # s34
    "Khi bạn phá kỷ lục, một dòng đặt thời gian mới vào ngăn kéo, kèm nhãn: best.",
    # s35
    "Và khi bo mạch khởi động, một dòng lấy nó ra lại. Nếu ngăn kéo còn trống, ta nhận một con số khổng lồ, nên lượt đầu tiên luôn là kỷ lục.",
    # s36
    "Cùng chứng minh nhé. Hai trăm mười bốn, kỷ lục mới. Rút ra... cắm lại... vẫn là hai trăm mười bốn.",
    # s37
    "Một mẹo: chỉ lưu khi có kỷ lục mới. Lưu mỗi lượt sẽ ghi đè thời gian tốt nhất của bạn bằng một thời gian chậm, và ngăn kéo cũng mòn nhanh hơn.",
    # s38
    "Đến lượt bạn. Hãy làm cho nút nhấn xóa kỷ lục khi giữ ba giây ở màn hình sẵn sàng. Bạn đã biết cách đo một lần nhấn giữ lâu.",
    # s39
    "Mã đầy đủ và lời giải nằm trong thư mục bài học, có liên kết bên dưới. Hãy đăng thời gian tốt nhất của bạn vào phần bình luận.",
    # s40
    "Lần tới, bo mạch sẽ có mắt: một cảm biến chuyển động biến mạch này thành báo động. Hãy đăng ký để không bỏ lỡ. Hẹn gặp bạn ở đó.",
]
L["ja"] = [
    # s01
    "待って... スタート！ 二百十四ミリ秒。新記録です。",
    # s02
    "では、これを見てください。ケーブルを抜きます。画面は真っ暗、ボードは完全にオフです。",
    # s03
    "差し直すと... 記録がまだ残っています。電源がまったくなくても、ボードは覚えていたんです。",
    # s04
    "今日はこのゲームをゼロから作ります。本物の画面、本物のビープ音、そして決して忘れない記録。必要なのはスターターキットと、約二十分だけです。",
    # s05
    "最初の新しい部品はこちら。幅が一インチもない、小さな画面です。",
    # s06
    "八千個ほどの小さな点があり、どの点も自分で光を出します。だからこの画面の黒は本当に黒です。その点が消えているだけなんです。",
    # s07
    "しかも必要な配線はたった四本。二本は電源。残りの二本が映像のすべてを運びます。",
    # s08
    "この二本はグループチャットのように働きます。一本はメッセージを一ビットずつ運びます。もう一本は拍子を刻み、両側が同じ瞬間に各ビットを読めるようにします。",
    # s09
    "チャットの参加者にはそれぞれ名前、つまり短いアドレスがあります。この画面は自分のアドレスに答えるので、あとで同じ二本の線に別の部品も追加できます。",
    # s10
    "二つ目の新しい部品は、この小さなブザーです。パッシブ型なので、音の高さを与えるまで鳴りません。",
    # s11
    "中では薄い金属の円盤が前後にたわみます。速くたわむと高いビープ音、ゆっくりだと低いブーンという音になります。",
    # s12
    "そして古い友だち、押しボタンも仲間入りです。画面が元のピンを使うので、新しいピンに引っ越すだけです。",
    # s13
    "配線していきましょう。穴にはそれぞれ番号と文字が印刷されていて、画面にも表示されるので、各ステップをそのまま真似できます。",
    # s14
    "まず電源です。赤い線で三・三ボルトを奥のプラス側のラインへ、黒い線でグラウンドをマイナス側のラインへ引きます。",
    # s15
    "次は画面です。四本の足を一列に並べて差します。そして二本の短い線で、そのラインから電源を渡します。",
    # s16
    "チャットの二本の線です。緑は二十二番ピンからクロックの足へ、青は二十一番ピンからデータの足へ。",
    # s17
    "ボタンは中央の溝をまたいで置きます。黄色は十九番ピンから片側へ、もう片側はグラウンドへつなぎます。",
    # s18
    "最後に、手前のボードのブザーです。オレンジは三十二番ピンからプラスの足へ、もう一方の足はグラウンドへ。",
    # s19
    "これで回路は完成です。画面一つ、ボタン一つ、ブザー一つ。自分のものと比べたいなら、ここで一時停止してください。",
    # s20
    "画面と話すために、無料のライブラリを使います。ライブラリマネージャーから一度インストールするだけです。",
    # s21
    "この画面のコツはこうです。printしても、まだ何も表示されません。ボードはカーテンの裏のホワイトボードに描いているのです。",
    # s22
    "displayを呼んだときだけカーテンが開き、絵全体が一度に現れます。ちらつきも、描きかけの文字もありません。",
    # s23
    "そこで、showという小さなヘルパーにまとめます。ボードを消し、上に小さな行、真ん中に大きな行を書いて、カーテンを開きます。",
    # s24
    "呼び出しは一回だけで、画面は好きな言葉を表示します。",
    # s25
    "ゲーム自体は洗濯機のように四つのステップです。準備、待機、スタート、そして結果。",
    # s26
    "ボタンを押すと、一・五秒から四秒のどこかでランダムな待ち時間を選びます。誰にもタイミングを読ませないためです。",
    # s27
    "時間が来ると、画面にGOと出て、ブザーが鳴ります。その瞬間から、時計が動き始めます。",
    # s28
    "ビープ音は一行です。toneに、ピン、音の高さ、そして長さを渡します。",
    # s29
    "あなたが押すと時計が止まります。GOからの時間があなたの反応で、そのまま画面に表示されます。",
    # s30
    "早く押しすぎたら？ それはフライングです。低いブーンという音が鳴って、やり直しです。",
    # s31
    "何ラウンドか遊んでみましょう。三百五十... 悪くない。二百八十... もっといい。",
    # s32
    "ここからが一番のお楽しみです。ふつう、変数は電源が切れるとすべて忘れてしまうメモリに住んでいます。毎晩掃き捨てられる、机の上の付箋のように。",
    # s33
    "でもESP32には、電源なしで物を保管してくれる小さな引き出しもあります。名前はPreferencesです。",
    # s34
    "記録を更新すると、一行で新しいタイムが引き出しに入ります。ラベルはbestです。",
    # s35
    "そしてボードが起動したとき、一行でそれを取り出します。引き出しがまだ空なら、巨大な数が返るので、最初のラウンドは必ず記録になります。",
    # s36
    "証明してみましょう。二百十四、新記録。抜いて... 差し直して... まだ二百十四です。",
    # s37
    "ひとつコツです。保存は新記録のときだけにしましょう。毎ラウンド保存すると、ベストタイムが遅いタイムで上書きされ、引き出しも早くすり減ってしまいます。",
    # s38
    "あなたの番です。準備画面でボタンを三秒間押し続けたら、記録が消えるようにしてみてください。長押しの測り方はもう知っていますね。",
    # s39
    "完全なコードと答えはレッスンフォルダにあります。リンクは下です。ベストタイムをコメントで教えてください。",
    # s40
    "次回、ボードに目がつきます。この装置をアラームに変える、動きセンサーです。見逃さないよう、チャンネル登録をお願いします。ではまた。",
]

if __name__ == "__main__":
    out = ROOT / "subs"
    out.mkdir(exist_ok=True)
    for lang, lines in L.items():
        assert len(lines) == len(IDS), (lang, len(lines), len(IDS))
        seg = dict(zip(IDS, lines))
        (out / f"{lang}.json").write_text(json.dumps({"lang": lang, "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("subs written:", ", ".join(L), f"({len(IDS)} segments each)")
