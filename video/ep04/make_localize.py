"""Source of video/ep04/localize.json (YouTube title + description per language) and youtube.md.
Chapter times are read from build/schedule.json, so rerun this after the narration changes.
Usage: python video/ep04/make_localize.py"""
import json
from pathlib import Path

here = Path(__file__).parent
# first segment of each chapter; times come from the schedule
CHAPTERS = ["s01", "s03", "s06", "s10", "s17", "s22", "s26", "s34", "s38", "s47", "s53", "s54"]
# the channel intro (tools/bumpers.py, 3.5 s) plays before the episode, so chapters shift
INTRO = 3.5
segs = json.loads((here / "build" / "schedule.json").read_text(encoding="utf-8"))["segments"]
starts = [0] + [int(segs[c]["start"] + INTRO) for c in CHAPTERS[1:]]
assert all(b - a >= 10 for a, b in zip(starts, starts[1:])), "YouTube chapters must be at least 10 s"
TIMES = ["%d:%02d" % divmod(s, 60) for s in starts]
CREDIT = '🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/'
REPO = "https://github.com/emjnbulut/esp32-from-zero"
LESSON = REPO + "/tree/main/lessons/04-buttons-and-millis"
TAGS = "#ESP32 #Arduino #Button #millis #Electronics #Microcontroller"

# lang: (title, intro, links header, lesson label, repo label, chapters header, chapter names)
T = {
    "en": ("ESP32 From Zero #4 — Buttons, Debounce & millis(): Doing Two Things at Once",
           "Today the ESP32 listens! We wire up a push button, learn why floating pins misbehave and how pull-up resistors fix them, and read the button with digitalRead and INPUT_PULLUP. Then we toggle an LED, tame button bounce, see why delay() freezes everything, and use millis() to blink two LEDs at their own speed while the button still reacts instantly.",
           "🔗 Links", "Lesson + all 5 sketches", "All code + lessons", "⏱ Chapters",
           ["Intro", "The push button", "Wiring the button", "Floating pins and pull-ups", "Writing the code", "Upload and Serial Monitor",
            "Toggle, edges and bounce", "Why delay() gets in the way", "millis(): check the clock", "A second LED", "Troubleshooting", "Recap and next episode"]),
    "tr": ("ESP32 From Zero #4 — Butonlar, Debounce ve millis(): Aynı Anda İki İş",
           "Bu kez ESP32 dinliyor! Bir push butonu bağlıyor, havada kalan (floating) pinlerin neden sorun çıkardığını ve pull-up dirençlerin bunu nasıl çözdüğünü öğreniyor, butonu digitalRead ve INPUT_PULLUP ile okuyoruz. Sonra bir LED'i aç-kapa yapıyor, buton sıçramasını (bounce) evcilleştiriyor, delay()'in neden her şeyi dondurduğunu görüyor ve millis() ile iki LED'i kendi hızında yakıp söndürürken butonun anında tepki vermesini sağlıyoruz.",
           "🔗 Bağlantılar", "Ders + 5 kodun hepsi", "Tüm kodlar + dersler", "⏱ Bölümler",
           ["Giriş", "Push buton", "Butonu bağlama", "Havadaki pinler ve pull-up", "Kodu yazma", "Yükle ve Seri Monitör",
            "Toggle, kenar ve sıçrama", "delay() neden engel olur", "millis(): saate bak", "İkinci bir LED", "Sorun giderme", "Özet ve sonraki bölüm"]),
    "hi": ("ESP32 From Zero #4 — Button, Debounce और millis(): एक साथ दो काम",
           "आज ESP32 सुनता है! हम एक push button wire करते हैं, समझते हैं कि floating pins क्यों गड़बड़ करते हैं और pull-up resistor इसे कैसे ठीक करता है, और digitalRead व INPUT_PULLUP से button पढ़ते हैं। फिर LED toggle करते हैं, button bounce को काबू में करते हैं, देखते हैं कि delay() सब कुछ क्यों freeze कर देता है, और millis() से दो LEDs को अपनी-अपनी speed पर blink कराते हैं, जबकि button तुरंत react करता रहता है।",
           "🔗 Links", "Lesson + सारे 5 sketches", "सारा code + lessons", "⏱ Chapters",
           ["Intro", "Push button", "Button की wiring", "Floating pins और pull-up", "Code लिखिए", "Upload और Serial Monitor",
            "Toggle, edge और bounce", "delay() रास्ते में क्यों आता है", "millis(): घड़ी देखिए", "दूसरी LED", "Troubleshooting", "Recap और अगला episode"]),
    "pt": ("ESP32 From Zero #4 — Botões, Debounce e millis(): Fazendo Duas Coisas ao Mesmo Tempo",
           "Hoje o ESP32 escuta! Ligamos um botão, entendemos por que pinos flutuantes se comportam mal e como os resistores pull-up resolvem isso, e lemos o botão com digitalRead e INPUT_PULLUP. Depois alternamos um LED, domamos o bounce do botão, vemos por que o delay() trava tudo e usamos millis() para piscar dois LEDs em velocidades diferentes enquanto o botão continua respondendo na hora.",
           "🔗 Links", "Aula + os 5 sketches", "Todo o código + aulas", "⏱ Capítulos",
           ["Introdução", "O botão", "Ligando o botão", "Pinos flutuantes e pull-up", "Escrevendo o código", "Enviar e Monitor Serial",
            "Toggle, bordas e bounce", "Por que o delay() atrapalha", "millis(): olhe o relógio", "Um segundo LED", "Solução de problemas", "Resumo e próximo episódio"]),
    "es": ("ESP32 From Zero #4 — Botones, Debounce y millis(): Hacer Dos Cosas a la Vez",
           "¡Hoy el ESP32 escucha! Conectamos un pulsador, vemos por qué los pines flotantes se portan mal y cómo lo arreglan las resistencias pull-up, y leemos el botón con digitalRead e INPUT_PULLUP. Luego alternamos un LED, domamos el rebote del botón, vemos por qué delay() lo congela todo y usamos millis() para parpadear dos LEDs a su propio ritmo mientras el botón sigue respondiendo al instante.",
           "🔗 Enlaces", "Lección + los 5 sketches", "Todo el código + lecciones", "⏱ Capítulos",
           ["Intro", "El pulsador", "Cableado del botón", "Pines flotantes y pull-up", "Escribe el código", "Sube y Monitor Serie",
            "Toggle, flancos y rebote", "Por qué delay() estorba", "millis(): mira el reloj", "Un segundo LED", "Solución de problemas", "Resumen y próximo episodio"]),
    "id": ("ESP32 From Zero #4 — Tombol, Debounce & millis(): Mengerjakan Dua Hal Sekaligus",
           "Hari ini ESP32 mendengarkan! Kita pasang tombol tekan, belajar kenapa pin mengambang (floating) bermasalah dan bagaimana resistor pull-up memperbaikinya, lalu membaca tombol dengan digitalRead dan INPUT_PULLUP. Setelah itu kita toggle LED, menjinakkan bounce tombol, melihat kenapa delay() membekukan semuanya, dan memakai millis() untuk mengedipkan dua LED dengan kecepatan masing-masing sementara tombol tetap bereaksi seketika.",
           "🔗 Link", "Materi + kelima sketch", "Semua kode + materi", "⏱ Bab",
           ["Intro", "Tombol tekan", "Memasang tombol", "Pin mengambang dan pull-up", "Tulis kodenya", "Upload dan Serial Monitor",
            "Toggle, edge, dan bounce", "Kenapa delay() menghalangi", "millis(): lihat jam", "LED kedua", "Pemecahan masalah", "Ringkasan dan episode berikutnya"]),
    "ar": ("ESP32 From Zero #4 — الأزرار وإزالة الارتداد وmillis(): تنفيذ مهمتين في وقت واحد",
           "اليوم يستمع ESP32! نوصّل زر ضغط، ونعرف لماذا تتصرف الأطراف العائمة بشكل غريب وكيف تحل مقاومات pull-up المشكلة، ثم نقرأ الزر باستخدام digitalRead وINPUT_PULLUP. بعد ذلك نبدّل حالة LED، ونروّض ارتداد الزر، ونرى لماذا يجمّد delay() كل شيء، ونستخدم millis() لإضاءة LED بسرعتين مختلفتين بينما يستجيب الزر فورًا.",
           "🔗 روابط", "الدرس + السكتشات الخمسة", "كل الكود + الدروس", "⏱ الفصول",
           ["مقدمة", "زر الضغط", "توصيل الزر", "الأطراف العائمة ومقاومة pull-up", "اكتب الكود", "الرفع وSerial Monitor",
            "التبديل والحافة والارتداد", "لماذا يعطّلنا delay()", "millis(): انظر إلى الساعة", "LED ثانٍ", "حل المشاكل", "ملخص والحلقة القادمة"]),
    "ru": ("ESP32 From Zero #4 — Кнопки, дребезг и millis(): делаем два дела одновременно",
           "Сегодня ESP32 слушает! Подключаем кнопку, узнаём, почему «висящие» пины ведут себя странно и как это лечат подтягивающие резисторы, и читаем кнопку через digitalRead и INPUT_PULLUP. Затем переключаем светодиод, укрощаем дребезг контактов, выясняем, почему delay() замораживает всё, и с помощью millis() мигаем двумя светодиодами с разной скоростью, пока кнопка реагирует мгновенно.",
           "🔗 Ссылки", "Урок + все 5 скетчей", "Весь код + уроки", "⏱ Главы",
           ["Вступление", "Кнопка", "Подключаем кнопку", "Висящие пины и подтяжка", "Пишем код", "Загрузка и монитор порта",
            "Переключение, фронты и дребезг", "Почему мешает delay()", "millis(): смотрим на часы", "Второй светодиод", "Если не работает", "Итоги и следующий выпуск"]),
    "de": ("ESP32 From Zero #4 — Taster, Entprellen & millis(): Zwei Dinge gleichzeitig",
           "Heute hört der ESP32 zu! Wir schließen einen Taster an, klären, warum schwebende Pins Probleme machen und wie Pull-up-Widerstände das lösen, und lesen den Taster mit digitalRead und INPUT_PULLUP. Dann schalten wir eine LED um, zähmen das Prellen, sehen, warum delay() alles einfriert, und blinken mit millis() zwei LEDs in eigenem Tempo, während der Taster sofort reagiert.",
           "🔗 Links", "Lektion + alle 5 Sketches", "Gesamter Code + Lektionen", "⏱ Kapitel",
           ["Intro", "Der Taster", "Den Taster verdrahten", "Schwebende Pins und Pull-ups", "Den Code schreiben", "Hochladen und serieller Monitor",
            "Umschalten, Flanken und Prellen", "Warum delay() im Weg steht", "millis(): auf die Uhr schauen", "Eine zweite LED", "Fehlersuche", "Rückblick und nächste Folge"]),
    "fr": ("ESP32 From Zero #4 — Boutons, anti-rebond et millis() : faire deux choses à la fois",
           "Aujourd'hui l'ESP32 écoute ! On câble un bouton poussoir, on voit pourquoi les broches flottantes se comportent mal et comment les résistances de rappel (pull-up) règlent ça, puis on lit le bouton avec digitalRead et INPUT_PULLUP. Ensuite on bascule une LED, on dompte les rebonds, on comprend pourquoi delay() fige tout, et on utilise millis() pour faire clignoter deux LED à leur propre rythme pendant que le bouton réagit instantanément.",
           "🔗 Liens", "Leçon + les 5 sketchs", "Tout le code + les leçons", "⏱ Chapitres",
           ["Intro", "Le bouton poussoir", "Câbler le bouton", "Broches flottantes et pull-up", "Écrire le code", "Téléverser et moniteur série",
            "Bascule, fronts et rebonds", "Pourquoi delay() gêne", "millis() : regarder l'horloge", "Une deuxième LED", "Dépannage", "Récap et prochain épisode"]),
    "vi": ("ESP32 From Zero #4 — Nút nhấn, chống rung & millis(): Làm hai việc cùng lúc",
           "Hôm nay ESP32 biết lắng nghe! Ta đấu nút nhấn, tìm hiểu vì sao chân thả nổi (floating) hay bị nhiễu và điện trở pull-up khắc phục thế nào, rồi đọc nút bằng digitalRead và INPUT_PULLUP. Sau đó ta bật/tắt LED bằng mỗi lần nhấn, xử lý hiện tượng rung phím, xem vì sao delay() làm treo mọi thứ, và dùng millis() để nháy hai LED theo tốc độ riêng trong khi nút vẫn phản hồi ngay lập tức.",
           "🔗 Liên kết", "Bài học + cả 5 sketch", "Toàn bộ code + bài học", "⏱ Chương",
           ["Mở đầu", "Nút nhấn", "Đấu nối nút", "Chân thả nổi và pull-up", "Viết code", "Nạp code và Serial Monitor",
            "Bật/tắt, cạnh và rung phím", "Vì sao delay() gây vướng", "millis(): nhìn đồng hồ", "LED thứ hai", "Khắc phục sự cố", "Tóm tắt và tập sau"]),
    "ja": ("ESP32 From Zero #4 — ボタン、チャタリング対策、millis()：同時に2つのことをする",
           "今回はESP32が「聞く」番です！プッシュボタンを配線し、浮いたピンが不安定になる理由とプルアップ抵抗での解決法を学び、digitalReadとINPUT_PULLUPでボタンを読み取ります。さらにLEDのトグル、チャタリング対策、delay()がすべてを止めてしまう理由を見て、millis()で2つのLEDをそれぞれの速さで点滅させつつ、ボタンにも即座に反応させます。",
           "🔗 リンク", "レッスン + 5つのスケッチ", "すべてのコード + レッスン", "⏱ チャプター",
           ["イントロ", "プッシュボタン", "ボタンの配線", "浮いたピンとプルアップ", "コードを書く", "書き込みとシリアルモニタ",
            "トグル、エッジ、チャタリング", "delay()が邪魔になる理由", "millis()：時計を見る", "2つ目のLED", "うまく動かないとき", "まとめと次回予告"]),
}

out = {}
for lang, (title, intro, links, lesson, repo, chap, names) in T.items():
    assert len(names) == len(TIMES) and len(title) <= 100, lang
    desc = (f"{intro}\n\n{links}\n• {lesson}: {LESSON}\n• {repo}: {REPO}\n\n{chap}\n"
            + "\n".join(f"{t} {n}" for t, n in zip(TIMES, names)) + f"\n\n{CREDIT}\n\n{TAGS}")
    assert "<" not in desc and ">" not in desc and len(desc) <= 5000, lang
    out[lang] = {"title": title, "description": desc}
(here / "localize.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

clips = json.loads((here / "script.json").read_text(encoding="utf-8"))["clips"]
en = out["en"]
(here / "youtube.md").write_text(f"""# YouTube upload — Episode 4

## Title
{en['title']}

## Description
{en['description']}

## Creator clips (footage/ep04/)
""" + "".join(f"- `{k}` — {v}\n" for k, v in clips.items()) + """
Then: `python tools/build.py video/ep04 compose`.

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep04 <VIDEO_ID>

It uploads every `build/ep04_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`
""", encoding="utf-8")
print("ok", len(out), "languages")
