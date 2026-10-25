"""Source of video/ep04/localize.json (YouTube title + description per language) and youtube.md.
Chapter times are read from build/schedule.json, so rerun this after the narration changes.
Usage: python video/ep04/make_localize.py"""
import json
import sys
from pathlib import Path

here = Path(__file__).parent
# first segment of each chapter; times come from the schedule
CHAPTERS = ["s01", "s04", "s05", "s08", "s14", "s20", "s25", "s29", "s37", "s41", "s45", "s53", "s59", "s61", "s62"]
# the channel sting (tools/bumpers.py) plays after the cold open, so only times after the cut shift
ROOT = here.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bumpers
segs = json.loads((here / "build" / "schedule.json").read_text(encoding="utf-8"))["segments"]
tc = bumpers.cut(here)
starts = [0] + [int(bumpers.shift(segs[c]["start"], tc)) for c in CHAPTERS[1:]]
assert all(b - a >= 10 for a, b in zip(starts, starts[1:])), "YouTube chapters must be at least 10 s"
TIMES = ["%d:%02d" % divmod(s, 60) for s in starts]
CREDIT = '🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\n🎙 Narration: Chatterbox TTS (Resemble AI, MIT). Voice references: LibriVox (public domain) and FLEURS by Google (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/'
REPO = "https://github.com/emjnbulut/esp32-from-zero"
LESSON = REPO + "/tree/main/lessons/04-buttons-and-millis"
TAGS = "#ESP32 #Arduino #Button #millis #Electronics #Microcontroller"

# lang: (title, intro, links header, lesson label, repo label, chapters header, chapter names)
T = {
    "en": ("ESP32 Buttons & millis(): Blink LEDs Without Blocking | ESP32 From Zero #4",
           "Press a button and one LED stops at once, while the other keeps blinking at its own speed. In this lesson you build that yourself: wire a push button on two breadboards, learn why floating pins misbehave and how INPUT_PULLUP fixes them, read the button with digitalRead, catch the edge of a press, tame button bounce, see why delay() freezes everything, and use millis() to do two things at once. At the end there is a challenge for you: the speed-shifter.",
           "🔗 Links", "Lesson + all 5 sketches", "All code + lessons", "⏱ Chapters",
           ["Two things at once (demo)", "What you need", "The push button", "Two breadboards and the wiring", "Floating pins and pull-ups", "The code, line by line", "Upload and Serial Monitor",
            "Toggle: catching the edge", "Bounce and debounce", "Why delay() gets in the way", "millis(): check the clock", "A second LED", "Your turn: the speed-shifter", "Troubleshooting", "Recap and next episode"]),
    "tr": ("ESP32 Butonlar ve millis(): LED'leri Engellemeden Yak-Söndür | ESP32 From Zero #4",
           "Bir butona basın, bir LED anında dursun, diğeri kendi hızında yanıp sönmeye devam etsin. Bu derste bunu kendiniz kuruyorsunuz: iki breadboard üzerinde bir push butonu bağlıyor, havada kalan (floating) pinlerin neden sorun çıkardığını ve INPUT_PULLUP'ın bunu nasıl çözdüğünü öğreniyor, butonu digitalRead ile okuyor, basışın kenarını yakalıyor, buton sıçramasını evcilleştiriyor, delay()'in neden her şeyi dondurduğunu görüyor ve millis() ile aynı anda iki iş yapıyorsunuz. Sonunda size bir meydan okuma var: hız değiştirici.",
           "🔗 Bağlantılar", "Ders + 5 kodun hepsi", "Tüm kodlar + dersler", "⏱ Bölümler",
           ["Aynı anda iki iş (demo)", "Neler gerekli", "Push buton", "İki breadboard ve bağlantı", "Havadaki pinler ve pull-up", "Kod, satır satır", "Yükle ve Seri Monitör",
            "Toggle: kenarı yakalamak", "Sıçrama ve debounce", "delay() neden engel olur", "millis(): saate bak", "İkinci bir LED", "Sıra sizde: hız değiştirici", "Sorun giderme", "Özet ve sonraki bölüm"]),
    "hi": ("ESP32 Button और millis(): LEDs को बिना रोके Blink कराएँ | ESP32 From Zero #4",
           "Button दबाइए और एक LED तुरंत रुक जाती है, जबकि दूसरी अपनी speed से blink करती रहती है। इस lesson में आप इसे खुद बनाते हैं: दो breadboards पर push button wire करते हैं, समझते हैं कि floating pins क्यों गड़बड़ करते हैं और INPUT_PULLUP इसे कैसे ठीक करता है, digitalRead से button पढ़ते हैं, press की edge पकड़ते हैं, button bounce को काबू में करते हैं, देखते हैं कि delay() सब कुछ क्यों freeze कर देता है, और millis() से एक साथ दो काम करते हैं। अंत में आपके लिए एक challenge है: speed-shifter।",
           "🔗 Links", "Lesson + सारे 5 sketches", "सारा code + lessons", "⏱ Chapters",
           ["एक साथ दो काम (demo)", "आपको क्या चाहिए", "Push button", "दो breadboards और wiring", "Floating pins और pull-up", "Code, लाइन दर लाइन", "Upload और Serial Monitor",
            "Toggle: edge पकड़ना", "Bounce और debounce", "delay() रास्ते में क्यों आता है", "millis(): घड़ी देखिए", "दूसरी LED", "आपकी बारी: speed-shifter", "Troubleshooting", "Recap और अगला episode"]),
    "pt": ("ESP32 Botões e millis(): Pisque LEDs Sem Travar | ESP32 From Zero #4",
           "Aperte um botão e um LED para na hora, enquanto o outro continua piscando na própria velocidade. Nesta aula você monta isso: liga um botão em duas protoboards, entende por que pinos flutuantes se comportam mal e como o INPUT_PULLUP resolve, lê o botão com digitalRead, pega a borda de um aperto, doma o bounce do botão, vê por que o delay() trava tudo e usa millis() para fazer duas coisas ao mesmo tempo. No final, um desafio para você: o speed-shifter.",
           "🔗 Links", "Aula + os 5 sketches", "Todo o código + aulas", "⏱ Capítulos",
           ["Duas coisas ao mesmo tempo (demo)", "O que você precisa", "O botão", "Duas protoboards e a fiação", "Pinos flutuantes e pull-up", "O código, linha por linha", "Enviar e Monitor Serial",
            "Toggle: pegando a borda", "Bounce e debounce", "Por que o delay() atrapalha", "millis(): olhe o relógio", "Um segundo LED", "Sua vez: o speed-shifter", "Solução de problemas", "Resumo e próximo episódio"]),
    "es": ("ESP32 Botones y millis(): Parpadea LEDs Sin Bloquear | ESP32 From Zero #4",
           "Presiona un botón y un LED se detiene al instante, mientras el otro sigue parpadeando a su propio ritmo. En esta lección lo construyes tú: conectas un pulsador en dos protoboards, aprendes por qué los pines flotantes se portan mal y cómo INPUT_PULLUP lo arregla, lees el botón con digitalRead, atrapas el flanco de una pulsación, domas el rebote, ves por qué delay() lo congela todo y usas millis() para hacer dos cosas a la vez. Al final hay un reto para ti: el speed-shifter.",
           "🔗 Enlaces", "Lección + los 5 sketches", "Todo el código + lecciones", "⏱ Capítulos",
           ["Dos cosas a la vez (demo)", "Lo que necesitas", "El pulsador", "Dos protoboards y el cableado", "Pines flotantes y pull-up", "El código, línea por línea", "Sube y Monitor Serie",
            "Toggle: atrapar el flanco", "Rebote y antirrebote", "Por qué delay() estorba", "millis(): mira el reloj", "Un segundo LED", "Tu turno: el speed-shifter", "Solución de problemas", "Resumen y próximo episodio"]),
    "id": ("ESP32 Tombol & millis(): Kedipkan LED Tanpa Memblokir | ESP32 From Zero #4",
           "Tekan tombol dan satu LED langsung berhenti, sementara yang lain terus berkedip dengan kecepatannya sendiri. Di pelajaran ini kamu membangunnya sendiri: memasang tombol tekan di dua breadboard, belajar kenapa pin mengambang (floating) bermasalah dan bagaimana INPUT_PULLUP memperbaikinya, membaca tombol dengan digitalRead, menangkap edge sebuah penekanan, menjinakkan bounce tombol, melihat kenapa delay() membekukan semuanya, dan memakai millis() untuk mengerjakan dua hal sekaligus. Di akhir ada tantangan untukmu: speed-shifter.",
           "🔗 Link", "Materi + kelima sketch", "Semua kode + materi", "⏱ Bab",
           ["Dua hal sekaligus (demo)", "Yang kamu butuhkan", "Tombol tekan", "Dua breadboard dan pengkabelan", "Pin mengambang dan pull-up", "Kode, baris demi baris", "Upload dan Serial Monitor",
            "Toggle: menangkap edge", "Bounce dan debounce", "Kenapa delay() menghalangi", "millis(): lihat jam", "LED kedua", "Giliranmu: speed-shifter", "Pemecahan masalah", "Ringkasan dan episode berikutnya"]),
    "ar": ("ESP32 الأزرار وmillis(): أومض LED دون تعطيل | ESP32 From Zero #4",
           "اضغط زرًا فيتوقف أحد الـ LED فورًا، بينما يواصل الآخر الوميض بسرعته الخاصة. في هذا الدرس تبني ذلك بنفسك: توصّل زر ضغط على breadboard اثنتين، وتعرف لماذا تتصرف الأطراف العائمة بشكل غريب وكيف يحل INPUT_PULLUP المشكلة، وتقرأ الزر بـ digitalRead، وتلتقط حافة الضغطة، وتروّض ارتداد الزر، وترى لماذا يجمّد delay() كل شيء، وتستخدم millis() لتنفيذ أمرين في وقت واحد. وفي النهاية هناك تحدٍّ لك: speed-shifter.",
           "🔗 روابط", "الدرس + السكتشات الخمسة", "كل الكود + الدروس", "⏱ الفصول",
           ["أمران في وقت واحد (عرض)", "ما الذي تحتاجه", "زر الضغط", "لوحتا breadboard والتوصيل", "الأطراف العائمة ومقاومة pull-up", "الكود سطرًا بسطر", "الرفع وSerial Monitor",
            "التبديل: التقاط الحافة", "الارتداد وإزالته", "لماذا يعطّلنا delay()", "millis(): انظر إلى الساعة", "LED ثانٍ", "دورك: speed-shifter", "حل المشاكل", "ملخص والحلقة القادمة"]),
    "ru": ("ESP32 Кнопки и millis(): мигаем светодиодами без блокировки | ESP32 From Zero #4",
           "Нажмите кнопку, и один светодиод сразу останавливается, а другой продолжает мигать в своём темпе. В этом уроке вы соберёте это сами: подключите кнопку на двух макетных платах, узнаете, почему «висящие» пины ведут себя странно и как их лечит INPUT_PULLUP, прочитаете кнопку через digitalRead, поймаете фронт нажатия, укротите дребезг, поймёте, почему delay() замораживает всё, и с помощью millis() будете делать два дела одновременно. В конце вас ждёт задание: speed-shifter.",
           "🔗 Ссылки", "Урок + все 5 скетчей", "Весь код + уроки", "⏱ Главы",
           ["Два дела одновременно (демо)", "Что понадобится", "Кнопка", "Две макетки и проводка", "Висящие пины и подтяжка", "Код строка за строкой", "Загрузка и монитор порта",
            "Переключение: ловим фронт", "Дребезг и его подавление", "Почему мешает delay()", "millis(): смотрим на часы", "Второй светодиод", "Ваша очередь: speed-shifter", "Если не работает", "Итоги и следующий выпуск"]),
    "de": ("ESP32 Taster & millis(): LEDs blinken ohne Blockieren | ESP32 From Zero #4",
           "Drück einen Taster, und eine LED stoppt sofort, während die andere in ihrem eigenen Tempo weiterblinkt. In dieser Lektion baust du das selbst: Taster auf zwei Breadboards verdrahten, verstehen, warum schwebende Pins Probleme machen und wie INPUT_PULLUP sie löst, den Taster mit digitalRead lesen, die Flanke eines Drucks fangen, das Prellen zähmen, sehen, warum delay() alles einfriert, und mit millis() zwei Dinge gleichzeitig tun. Am Ende wartet eine Aufgabe auf dich: der Speed-Shifter.",
           "🔗 Links", "Lektion + alle 5 Sketches", "Gesamter Code + Lektionen", "⏱ Kapitel",
           ["Zwei Dinge gleichzeitig (Demo)", "Was du brauchst", "Der Taster", "Zwei Breadboards und die Verdrahtung", "Schwebende Pins und Pull-ups", "Der Code, Zeile für Zeile", "Hochladen und serieller Monitor",
            "Umschalten: die Flanke fangen", "Prellen und Entprellen", "Warum delay() im Weg steht", "millis(): auf die Uhr schauen", "Eine zweite LED", "Du bist dran: der Speed-Shifter", "Fehlersuche", "Rückblick und nächste Folge"]),
    "fr": ("ESP32 Boutons et millis() : faire clignoter des LED sans bloquer | ESP32 From Zero #4",
           "Appuyez sur un bouton et une LED s'arrête aussitôt, pendant que l'autre continue de clignoter à son rythme. Dans cette leçon, vous le construisez vous-même : câbler un bouton poussoir sur deux breadboards, comprendre pourquoi les broches flottantes se comportent mal et comment INPUT_PULLUP règle ça, lire le bouton avec digitalRead, attraper le front d'un appui, dompter les rebonds, voir pourquoi delay() fige tout, et utiliser millis() pour faire deux choses à la fois. À la fin, un défi vous attend : le speed-shifter.",
           "🔗 Liens", "Leçon + les 5 sketchs", "Tout le code + les leçons", "⏱ Chapitres",
           ["Deux choses à la fois (démo)", "Ce qu'il vous faut", "Le bouton poussoir", "Deux breadboards et le câblage", "Broches flottantes et pull-up", "Le code, ligne par ligne", "Téléverser et moniteur série",
            "Bascule : attraper le front", "Rebond et anti-rebond", "Pourquoi delay() gêne", "millis() : regarder l'horloge", "Une deuxième LED", "À vous : le speed-shifter", "Dépannage", "Récap et prochain épisode"]),
    "vi": ("ESP32 Nút nhấn & millis(): Nháy LED không bị chặn | ESP32 From Zero #4",
           "Nhấn một nút và một LED dừng ngay, trong khi LED kia vẫn nháy theo tốc độ riêng. Trong bài này bạn tự làm điều đó: đấu nút nhấn trên hai breadboard, hiểu vì sao chân thả nổi (floating) hay bị nhiễu và INPUT_PULLUP khắc phục thế nào, đọc nút bằng digitalRead, bắt cạnh của một lần nhấn, xử lý hiện tượng rung phím, xem vì sao delay() làm treo mọi thứ, và dùng millis() để làm hai việc cùng lúc. Cuối bài có một thử thách dành cho bạn: speed-shifter.",
           "🔗 Liên kết", "Bài học + cả 5 sketch", "Toàn bộ code + bài học", "⏱ Chương",
           ["Hai việc cùng lúc (demo)", "Bạn cần gì", "Nút nhấn", "Hai breadboard và đấu dây", "Chân thả nổi và pull-up", "Code, từng dòng một", "Nạp code và Serial Monitor",
            "Bật/tắt: bắt cạnh", "Rung phím và chống rung", "Vì sao delay() gây vướng", "millis(): nhìn đồng hồ", "LED thứ hai", "Đến lượt bạn: speed-shifter", "Khắc phục sự cố", "Tóm tắt và tập sau"]),
    "ja": ("ESP32 ボタンとmillis()：LEDを止めずに点滅させる | ESP32 From Zero #4",
           "ボタンを押すと片方のLEDはすぐ止まり、もう片方は自分の速さで点滅し続けます。このレッスンでは、それを自分で作ります。2枚のブレッドボードにプッシュボタンを配線し、浮いたピンが不安定になる理由とINPUT_PULLUPでの解決法を学び、digitalReadでボタンを読み取り、押した瞬間のエッジを捕まえ、チャタリングを抑え、delay()がすべてを止めてしまう理由を見て、millis()で2つのことを同時に行います。最後にはあなたへの課題があります。スピードシフターです。",
           "🔗 リンク", "レッスン + 5つのスケッチ", "すべてのコード + レッスン", "⏱ チャプター",
           ["同時に2つのこと（デモ）", "必要なもの", "プッシュボタン", "2枚のブレッドボードと配線", "浮いたピンとプルアップ", "コードを1行ずつ", "書き込みとシリアルモニタ",
            "トグル：エッジを捕まえる", "チャタリングと対策", "delay()が邪魔になる理由", "millis()：時計を見る", "2つ目のLED", "あなたの番：スピードシフター", "うまく動かないとき", "まとめと次回予告"]),
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
