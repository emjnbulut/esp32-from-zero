"""Source of video/ep05/localize.json (YouTube title + description per language) and youtube.md.
Chapter times are read from build/schedule.json, so rerun this after the narration changes.
Usage: python video/ep05/make_localize.py"""
import json
import sys
from pathlib import Path

here = Path(__file__).parent
# first segment of each chapter; times come from the schedule
CHAPTERS = ["s01", "s04", "s05", "s10", "s14", "s23", "s29", "s36", "s41", "s43", "s44"]
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
LESSON = REPO + "/tree/main/lessons/05-pwm-and-rgb"
TAGS = "#ESP32 #Arduino #PWM #RGB #LED #Electronics"

# lang: (title, intro, links header, lesson label, repo label, chapters header, chapter names)
T = {
    "en": ("ESP32 PWM & RGB LED: Smooth Fades and Any Color with analogWrite() | ESP32 From Zero #5",
           "One LED breathes in and out, another mixes any color you want, and a button switches between them. In this lesson you learn how PWM makes an on/off pin dim an LED, use analogWrite() with values from 0 to 255, check the average voltage with a multimeter, build a smooth fade with millis() that never blocks the button, wire an RGB LED with three resistors, write your own setColor() function and cycle color modes with one button. At the end: a challenge for you, the smart camping headlamp.",
           "🔗 Links", "Lesson + all 5 sketches", "All code + lessons", "⏱ Chapters",
           ["Fade it, mix it (demo)", "What you need", "PWM: on and off, fast", "analogWrite() and the multimeter", "A fade that never waits", "The RGB LED and its wiring", "setColor() and mixing light",
            "One button, four color modes", "Your turn: the camping headlamp", "Troubleshooting", "Recap and next episode"]),
    "tr": ("ESP32 PWM ve RGB LED: analogWrite() ile Yumuşak Geçişler ve İstediğin Renk | ESP32 From Zero #5",
           "Bir LED nefes alıp verir, bir başkası istediğiniz rengi karıştırır ve bir buton ikisi arasında geçiş yapar. Bu derste PWM'in aç/kapa bir pini nasıl kısılmış bir LED'e çevirdiğini öğreniyor, analogWrite() ile 0'dan 255'e değerler kullanıyor, ortalama gerilimi multimetreyle kontrol ediyor, butonu asla engellemeyen millis() tabanlı yumuşak bir geçiş kuruyor, üç dirençle bir RGB LED bağlıyor, kendi setColor() fonksiyonunuzu yazıyor ve tek butonla renk modları arasında dönüyorsunuz. Sonunda size bir meydan okuma var: akıllı kamp kafa lambası.",
           "🔗 Bağlantılar", "Ders + 5 kodun hepsi", "Tüm kodlar + dersler", "⏱ Bölümler",
           ["Soldur, karıştır (demo)", "Neler gerekli", "PWM: hızlı aç-kapa", "analogWrite() ve multimetre", "Asla beklemeyen geçiş", "RGB LED ve bağlantısı", "setColor() ve ışık karıştırma",
            "Tek buton, dört renk modu", "Sıra sizde: kamp kafa lambası", "Sorun giderme", "Özet ve sonraki bölüm"]),
    "hi": ("ESP32 PWM और RGB LED: analogWrite() से Smooth Fade और कोई भी रंग | ESP32 From Zero #5",
           "एक LED साँस लेती है, दूसरी आपके मनचाहे रंग मिलाती है, और एक button दोनों के बीच बदलता है। इस lesson में आप सीखते हैं कि PWM कैसे on/off pin से LED को dim करता है, analogWrite() को 0 से 255 तक के मानों के साथ इस्तेमाल करते हैं, multimeter से औसत voltage जाँचते हैं, millis() से ऐसा smooth fade बनाते हैं जो button को कभी नहीं रोकता, तीन resistors के साथ RGB LED wire करते हैं, अपना setColor() function लिखते हैं और एक button से color modes घुमाते हैं। अंत में आपके लिए एक challenge है: smart camping headlamp।",
           "🔗 Links", "Lesson + सारे 5 sketches", "सारा code + lessons", "⏱ Chapters",
           ["Fade करें, mix करें (demo)", "आपको क्या चाहिए", "PWM: तेज़ on और off", "analogWrite() और multimeter", "ऐसा fade जो कभी नहीं रुकता", "RGB LED और उसकी wiring", "setColor() और रोशनी मिलाना",
            "एक button, चार color modes", "आपकी बारी: camping headlamp", "Troubleshooting", "Recap और अगला episode"]),
    "pt": ("ESP32 PWM e LED RGB: Fades Suaves e Qualquer Cor com analogWrite() | ESP32 From Zero #5",
           "Um LED respira, outro mistura a cor que você quiser, e um botão alterna entre eles. Nesta aula você aprende como o PWM faz um pino liga/desliga reduzir o brilho de um LED, usa analogWrite() com valores de 0 a 255, confere a tensão média com um multímetro, monta um fade suave com millis() que nunca trava o botão, liga um LED RGB com três resistores, escreve sua própria função setColor() e alterna modos de cor com um botão. No final, um desafio para você: a lanterna de cabeça inteligente para acampar.",
           "🔗 Links", "Aula + os 5 sketches", "Todo o código + aulas", "⏱ Capítulos",
           ["Fade e mistura (demo)", "O que você precisa", "PWM: liga e desliga, rápido", "analogWrite() e o multímetro", "Um fade que nunca espera", "O LED RGB e a fiação", "setColor() e mistura de luz",
            "Um botão, quatro modos de cor", "Sua vez: a lanterna de camping", "Solução de problemas", "Resumo e próximo episódio"]),
    "es": ("ESP32 PWM y LED RGB: Fades Suaves y Cualquier Color con analogWrite() | ESP32 From Zero #5",
           "Un LED respira, otro mezcla el color que tú quieras, y un botón cambia entre ellos. En esta lección aprendes cómo el PWM hace que un pin de encendido/apagado atenúe un LED, usas analogWrite() con valores de 0 a 255, compruebas el voltaje promedio con un multímetro, armas un fade suave con millis() que nunca bloquea el botón, conectas un LED RGB con tres resistencias, escribes tu propia función setColor() y recorres modos de color con un botón. Al final, un reto para ti: la linterna frontal inteligente para acampar.",
           "🔗 Enlaces", "Lección + los 5 sketches", "Todo el código + lecciones", "⏱ Capítulos",
           ["Fade y mezcla (demo)", "Lo que necesitas", "PWM: encendido y apagado, rápido", "analogWrite() y el multímetro", "Un fade que nunca espera", "El LED RGB y su cableado", "setColor() y mezcla de luz",
            "Un botón, cuatro modos de color", "Tu turno: la linterna de camping", "Solución de problemas", "Resumen y próximo episodio"]),
    "id": ("ESP32 PWM & LED RGB: Fade Halus dan Warna Apa Saja dengan analogWrite() | ESP32 From Zero #5",
           "Satu LED bernapas naik turun, yang lain mencampur warna apa pun yang kamu mau, dan satu tombol berpindah di antara keduanya. Di pelajaran ini kamu belajar bagaimana PWM membuat pin on/off meredupkan LED, memakai analogWrite() dengan nilai 0 sampai 255, mengecek tegangan rata-rata dengan multimeter, membuat fade halus dengan millis() yang tak pernah memblokir tombol, memasang LED RGB dengan tiga resistor, menulis fungsi setColor() sendiri, dan memutar mode warna dengan satu tombol. Di akhir: tantangan untukmu, senter kepala camping pintar.",
           "🔗 Link", "Materi + kelima sketch", "Semua kode + materi", "⏱ Bab",
           ["Fade dan campur (demo)", "Yang kamu butuhkan", "PWM: nyala dan mati, cepat", "analogWrite() dan multimeter", "Fade yang tak pernah menunggu", "LED RGB dan pengkabelannya", "setColor() dan campuran cahaya",
            "Satu tombol, empat mode warna", "Giliranmu: senter kepala camping", "Pemecahan masalah", "Ringkasan dan episode berikutnya"]),
    "ar": ("ESP32 PWM وLED RGB: إخفات ناعم وأي لون مع analogWrite() | ESP32 From Zero #5",
           "LED واحد يتنفس صعودًا وهبوطًا، وآخر يمزج أي لون تريده، وزر يبدّل بينهما. في هذا الدرس تتعلم كيف يجعل PWM طرفًا يعمل بالتشغيل والإطفاء يخفّت LED، وتستخدم analogWrite() بقيم من 0 إلى 255، وتفحص الجهد المتوسط بجهاز multimeter، وتبني fade ناعمًا بـ millis() لا يعطّل الزر أبدًا، وتوصّل LED من نوع RGB بثلاث مقاومات، وتكتب دالة setColor() الخاصة بك، وتتنقل بين أوضاع الألوان بزر واحد. وفي النهاية تحدٍّ لك: مصباح الرأس الذكي للتخييم.",
           "🔗 روابط", "الدرس + السكتشات الخمسة", "كل الكود + الدروس", "⏱ الفصول",
           ["أخفت وامزج (عرض)", "ما الذي تحتاجه", "PWM: تشغيل وإطفاء بسرعة", "analogWrite() وجهاز multimeter", "fade لا ينتظر أبدًا", "الـ LED من نوع RGB وتوصيله", "setColor() ومزج الضوء",
            "زر واحد وأربعة أوضاع للون", "دورك: مصباح التخييم", "حل المشاكل", "ملخص والحلقة القادمة"]),
    "ru": ("ESP32 PWM и RGB-светодиод: плавное затухание и любой цвет через analogWrite() | ESP32 From Zero #5",
           "Один светодиод плавно дышит, другой смешивает любой цвет, а кнопка переключает между ними. В этом уроке вы узнаете, как ШИМ (PWM) позволяет пину «включено/выключено» приглушать светодиод, воспользуетесь analogWrite() со значениями от 0 до 255, проверите среднее напряжение мультиметром, соберёте плавный переход на millis(), который никогда не блокирует кнопку, подключите RGB-светодиод через три резистора, напишете собственную функцию setColor() и переберёте режимы цвета одной кнопкой. В конце вас ждёт задание: умный налобный фонарь для кемпинга.",
           "🔗 Ссылки", "Урок + все 5 скетчей", "Весь код + уроки", "⏱ Главы",
           ["Плавно и в цвете (демо)", "Что понадобится", "PWM: быстро вкл и выкл", "analogWrite() и мультиметр", "Плавный переход без ожидания", "RGB-светодиод и подключение", "setColor() и смешивание света",
            "Одна кнопка, четыре режима цвета", "Ваша очередь: налобный фонарь", "Если не работает", "Итоги и следующий выпуск"]),
    "de": ("ESP32 PWM & RGB-LED: Sanfte Fades und jede Farbe mit analogWrite() | ESP32 From Zero #5",
           "Eine LED atmet ein und aus, eine andere mischt jede Farbe, die du willst, und ein Taster schaltet zwischen beiden um. In dieser Lektion lernst du, wie PWM einen An/Aus-Pin eine LED dimmen lässt, nutzt analogWrite() mit Werten von 0 bis 255, prüfst die mittlere Spannung mit einem Multimeter, baust mit millis() einen sanften Fade, der den Taster nie blockiert, verdrahtest eine RGB-LED mit drei Widerständen, schreibst deine eigene Funktion setColor() und schaltest mit einem Taster durch Farbmodi. Am Ende wartet eine Aufgabe auf dich: die smarte Camping-Stirnlampe.",
           "🔗 Links", "Lektion + alle 5 Sketches", "Gesamter Code + Lektionen", "⏱ Kapitel",
           ["Faden und mischen (Demo)", "Was du brauchst", "PWM: schnell an und aus", "analogWrite() und das Multimeter", "Ein Fade, der nie wartet", "Die RGB-LED und ihre Verdrahtung", "setColor() und Licht mischen",
            "Ein Taster, vier Farbmodi", "Du bist dran: die Camping-Stirnlampe", "Fehlersuche", "Rückblick und nächste Folge"]),
    "fr": ("ESP32 PWM et LED RGB : fondus doux et toutes les couleurs avec analogWrite() | ESP32 From Zero #5",
           "Une LED respire, une autre mélange la couleur que vous voulez, et un bouton passe de l'une à l'autre. Dans cette leçon, vous apprenez comment le PWM permet à une broche tout ou rien d'atténuer une LED, utilisez analogWrite() avec des valeurs de 0 à 255, vérifiez la tension moyenne au multimètre, construisez un fondu doux avec millis() qui ne bloque jamais le bouton, câblez une LED RGB avec trois résistances, écrivez votre propre fonction setColor() et faites défiler des modes de couleur avec un seul bouton. À la fin, un défi vous attend : la lampe frontale de camping intelligente.",
           "🔗 Liens", "Leçon + les 5 sketchs", "Tout le code + les leçons", "⏱ Chapitres",
           ["Fondu et mélange (démo)", "Ce qu'il vous faut", "PWM : allumé et éteint, très vite", "analogWrite() et le multimètre", "Un fondu qui n'attend jamais", "La LED RGB et son câblage", "setColor() et mélange de lumière",
            "Un bouton, quatre modes de couleur", "À vous : la lampe frontale de camping", "Dépannage", "Récap et prochain épisode"]),
    "vi": ("ESP32 PWM & LED RGB: Mờ dần mượt mà và mọi màu với analogWrite() | ESP32 From Zero #5",
           "Một LED thở nhẹ nhàng, một LED khác trộn bất kỳ màu nào bạn muốn, và một nút chuyển qua lại giữa chúng. Trong bài này bạn học cách PWM giúp chân bật/tắt làm mờ LED, dùng analogWrite() với giá trị từ 0 đến 255, kiểm tra điện áp trung bình bằng đồng hồ vạn năng, tạo fade mượt bằng millis() không bao giờ chặn nút, đấu LED RGB với ba điện trở, tự viết hàm setColor() và xoay vòng các chế độ màu bằng một nút. Cuối bài có một thử thách dành cho bạn: đèn pin đội đầu cắm trại thông minh.",
           "🔗 Liên kết", "Bài học + cả 5 sketch", "Toàn bộ code + bài học", "⏱ Chương",
           ["Làm mờ, trộn màu (demo)", "Bạn cần gì", "PWM: bật tắt thật nhanh", "analogWrite() và đồng hồ vạn năng", "Fade không bao giờ chờ", "LED RGB và cách đấu dây", "setColor() và trộn ánh sáng",
            "Một nút, bốn chế độ màu", "Đến lượt bạn: đèn pin đội đầu", "Khắc phục sự cố", "Tóm tắt và tập sau"]),
    "ja": ("ESP32 PWMとRGB LED：analogWrite()でなめらかなフェードと自由な色 | ESP32 From Zero #5",
           "1つのLEDは呼吸するように明滅し、もう1つは好きな色を混ぜ、ボタン1つで切り替えます。このレッスンでは、PWMでオンオフのピンがLEDを調光できる仕組みを学び、0から255の値でanalogWrite()を使い、テスターで平均電圧を確かめ、ボタンを決して止めないmillis()のなめらかなフェードを作り、3本の抵抗でRGB LEDを配線し、自作のsetColor()関数を書き、ボタン1つでカラーモードを切り替えます。最後にはあなたへの課題があります。スマートなキャンプ用ヘッドランプです。",
           "🔗 リンク", "レッスン + 5つのスケッチ", "すべてのコード + レッスン", "⏱ チャプター",
           ["フェードして、混ぜる（デモ）", "必要なもの", "PWM：高速でオンとオフ", "analogWrite()とテスター", "待たないフェード", "RGB LEDと配線", "setColor()と光の混色",
            "ボタン1つ、4つのカラーモード", "あなたの番：キャンプ用ヘッドランプ", "うまく動かないとき", "まとめと次回予告"]),
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
(here / "youtube.md").write_text(f"""# YouTube upload — Episode 5

## Title
{en['title']}

## Description
{en['description']}

## Creator clips (footage/ep05/)
""" + "".join(f"- `{k}` — {v}\n" for k, v in clips.items()) + """
Then: `python tools/build.py video/ep05 compose`.

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep05 <VIDEO_ID>

It uploads every `build/ep05_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`
""", encoding="utf-8")
print("ok", len(out), "languages")
