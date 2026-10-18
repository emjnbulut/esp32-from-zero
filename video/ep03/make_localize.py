"""Source of video/ep03/localize.json (YouTube title + description per language) and youtube.md.
Chapter times are read from build/schedule.json, so rerun this after the narration changes.
Usage: python video/ep03/make_localize.py"""
import json
from pathlib import Path

here = Path(__file__).parent
# first segment of each chapter; times come from the schedule
CHAPTERS = ["s01", "s03", "s04", "s09", "s13", "s21", "s25", "s26", "s28", "s29"]
# the channel intro (tools/bumpers.py, 3.5 s) plays before the episode, so chapters shift
INTRO = 3.5
segs = json.loads((here / "build" / "schedule.json").read_text(encoding="utf-8"))["segments"]
starts = [0] + [int(segs[c]["start"] + INTRO) for c in CHAPTERS[1:]]
assert all(b - a >= 10 for a, b in zip(starts, starts[1:])), "YouTube chapters must be at least 10 s"
TIMES = ["%d:%02d" % divmod(s, 60) for s in starts]
CREDIT = '🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\n🎙 Narration: Chatterbox TTS (Resemble AI, MIT). Voice references: LibriVox (public domain) and FLEURS by Google (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/'
REPO = "https://github.com/emjnbulut/esp32-from-zero"
LESSON = REPO + "/tree/main/lessons/03-blink-an-led"
TAGS = "#ESP32 #Arduino #Blink #LED #Electronics #Microcontroller"

# lang: (title, intro, links header, lesson label, repo label, chapters header, chapter names)
T = {
    "en": ("ESP32 From Zero #3 — Blink an LED: Your First Program That Controls Hardware",
           "Time for code to take control! We find out why the LED needs a 220 Ω resistor (Ohm's law, simply), move the resistor's leg from the + rail to GPIO 23 (red wire out), and write the classic Blink sketch with pinMode, digitalWrite and delay. Then we upload it, watch the board report each change in the Serial Monitor, and play with the timing.",
           "🔗 Links", "Lesson + Blink code", "All code + lessons", "⏱ Chapters",
           ["Intro", "Last episode's circuit", "Why 220 Ω? Ohm's law", "Move the resistor", "Write the code", "Upload and blink",
            "What happens on the pin", "Play with the timing", "LED not blinking?", "Recap and next episode"]),
    "tr": ("ESP32 From Zero #3 — LED Yakıp Söndürme: Donanımı Kontrol Eden İlk Programın",
           "Kontrolü kod alıyor! LED'in neden 220 Ω dirence ihtiyaç duyduğunu (basitçe Ohm yasası) öğreniyor, direncin bacağını + raydan GPIO 23'e taşıyor (kırmızı kablo çıkıyor) ve pinMode, digitalWrite ve delay ile klasik Blink programını yazıyoruz. Sonra programı yüklüyor, kartın her değişikliği Seri Monitör'de bildirmesini izliyor ve zamanlamayla oynuyoruz.",
           "🔗 Bağlantılar", "Ders + Blink kodu", "Tüm kodlar + dersler", "⏱ Bölümler",
           ["Giriş", "Geçen bölümün devresi", "Neden 220 Ω? Ohm yasası", "Direnci taşı", "Kodu yaz", "Yükle ve yak-söndür",
            "Pinde neler oluyor", "Zamanlamayla oyna", "LED yanıp sönmüyor mu?", "Özet ve sonraki bölüm"]),
    "hi": ("ESP32 From Zero #3 — LED Blink करें: Hardware चलाने वाला आपका पहला Program",
           "अब control code के हाथ में! हम जानते हैं कि LED को 220 Ω resistor क्यों चाहिए (आसान भाषा में Ohm's law), resistor की टाँग को + rail से GPIO 23 पर ले जाते हैं (लाल wire बाहर), और pinMode, digitalWrite और delay से classic Blink sketch लिखते हैं। फिर उसे upload करते हैं, Serial Monitor में board की हर report देखते हैं, और timing के साथ खेलते हैं।",
           "🔗 Links", "Lesson + Blink code", "सारा code + lessons", "⏱ Chapters",
           ["Intro", "पिछले episode का circuit", "220 Ω क्यों? Ohm's law", "Resistor को हटाइए", "Code लिखिए", "Upload और blink",
            "Pin पर क्या होता है", "Timing के साथ खेलिए", "LED blink नहीं हो रहा?", "Recap और अगला episode"]),
    "pt": ("ESP32 From Zero #3 — Pisque um LED: Seu Primeiro Programa que Controla Hardware",
           "Agora o código assume o controle! Descobrimos por que o LED precisa de um resistor de 220 Ω (a lei de Ohm, de forma simples), mudamos a perna do resistor do trilho + para o GPIO 23 (fio vermelho fora) e escrevemos o clássico Blink com pinMode, digitalWrite e delay. Depois enviamos o código, vemos a placa relatar cada mudança no Monitor Serial e brincamos com o tempo.",
           "🔗 Links", "Aula + código Blink", "Todo o código + aulas", "⏱ Capítulos",
           ["Introdução", "O circuito do último episódio", "Por que 220 Ω? Lei de Ohm", "Mude o resistor", "Escrevendo o código", "Enviar e piscar",
            "O que acontece no pino", "Brincando com o tempo", "O LED não pisca?", "Resumo e próximo episódio"]),
    "es": ("ESP32 From Zero #3 — Haz Parpadear un LED: Tu Primer Programa que Controla Hardware",
           "¡Ahora el código toma el control! Vemos por qué el LED necesita una resistencia de 220 Ω (la ley de Ohm, de forma sencilla), movemos la pata de la resistencia del riel + a GPIO 23 (sin el cable rojo) y escribimos el clásico Blink con pinMode, digitalWrite y delay. Luego lo subimos, vemos cómo la placa informa cada cambio en el Monitor Serie y jugamos con los tiempos.",
           "🔗 Enlaces", "Lección + código Blink", "Todo el código + lecciones", "⏱ Capítulos",
           ["Intro", "El circuito del episodio anterior", "¿Por qué 220 Ω? Ley de Ohm", "Mueve la resistencia", "Escribe el código", "Sube y parpadea",
            "Qué pasa en el pin", "Juega con los tiempos", "¿El LED no parpadea?", "Resumen y próximo episodio"]),
    "id": ("ESP32 From Zero #3 — Kedipkan LED: Program Pertamamu yang Mengendalikan Hardware",
           "Saatnya kode mengambil alih! Kita cari tahu kenapa LED butuh resistor 220 Ω (hukum Ohm secara sederhana), memindahkan kaki resistor dari rel + ke GPIO 23 (kabel merah dicabut), dan menulis sketch Blink klasik dengan pinMode, digitalWrite, dan delay. Lalu kita upload, melihat board melaporkan setiap perubahan di Serial Monitor, dan bermain dengan waktunya.",
           "🔗 Link", "Materi + kode Blink", "Semua kode + materi", "⏱ Bab",
           ["Intro", "Rangkaian episode lalu", "Kenapa 220 Ω? Hukum Ohm", "Pindahkan resistor", "Tulis kodenya", "Upload dan berkedip",
            "Apa yang terjadi di pin", "Bermain dengan waktu", "LED tidak berkedip?", "Ringkasan dan episode berikutnya"]),
    "ar": ("ESP32 From Zero #3 — اجعل LED يومض: أول برنامج لك يتحكم في العتاد",
           "حان وقت أن يتولى الكود التحكم! نعرف لماذا يحتاج LED إلى مقاومة 220 Ω (قانون أوم ببساطة)، وننقل ساق المقاومة من خط الموجب + إلى GPIO 23 (مع إزالة السلك الأحمر)، ونكتب برنامج Blink الشهير باستخدام pinMode وdigitalWrite وdelay. ثم نرفعه إلى اللوحة، ونشاهدها تبلغ عن كل تغيير في Serial Monitor، ونجرّب تغيير التوقيت.",
           "🔗 روابط", "الدرس + كود Blink", "كل الكود + الدروس", "⏱ الفصول",
           ["مقدمة", "دائرة الحلقة السابقة", "لماذا 220 Ω؟ قانون أوم", "انقل المقاومة", "اكتب الكود", "الرفع والوميض",
            "ماذا يحدث على الطرف", "جرّب التوقيت", "LED لا يومض؟", "ملخص والحلقة القادمة"]),
    "ru": ("ESP32 From Zero #3 — Мигаем светодиодом: первая программа, которая управляет железом",
           "Теперь управляет код! Разбираемся, зачем светодиоду резистор 220 Ω (закон Ома простыми словами), переносим ножку резистора с плюсовой шины на GPIO 23 (красный провод убираем) и пишем классический скетч Blink с pinMode, digitalWrite и delay. Затем загружаем его, смотрим, как плата сообщает о каждом изменении в мониторе порта, и играем с таймингом.",
           "🔗 Ссылки", "Урок + код Blink", "Весь код + уроки", "⏱ Главы",
           ["Вступление", "Схема из прошлого выпуска", "Почему 220 Ω? Закон Ома", "Переносим резистор", "Пишем код", "Загружаем и мигаем",
            "Что происходит на пине", "Играем с таймингом", "Светодиод не мигает?", "Итоги и следующий выпуск"]),
    "de": ("ESP32 From Zero #3 — LED blinken lassen: Dein erstes Programm, das Hardware steuert",
           "Jetzt übernimmt der Code! Wir klären, warum die LED einen 220-Ω-Widerstand braucht (das ohmsche Gesetz, ganz einfach), stecken das Beinchen des Widerstands von der Plusschiene auf GPIO 23 um (rotes Kabel raus) und schreiben den klassischen Blink-Sketch mit pinMode, digitalWrite und delay. Dann laden wir ihn hoch, sehen im seriellen Monitor, wie das Board jede Änderung meldet, und spielen mit dem Timing.",
           "🔗 Links", "Lektion + Blink-Code", "Gesamter Code + Lektionen", "⏱ Kapitel",
           ["Intro", "Die Schaltung aus der letzten Folge", "Warum 220 Ω? Ohmsches Gesetz", "Den Widerstand umstecken", "Den Code schreiben", "Hochladen und blinken",
            "Was am Pin passiert", "Mit dem Timing spielen", "LED blinkt nicht?", "Rückblick und nächste Folge"]),
    "fr": ("ESP32 From Zero #3 — Faire clignoter une LED : ton premier programme qui pilote du matériel",
           "Le code prend les commandes ! On voit pourquoi la LED a besoin d'une résistance de 220 Ω (la loi d'Ohm, simplement), on déplace la patte de la résistance du rail + vers la GPIO 23 (fil rouge retiré), et on écrit le célèbre sketch Blink avec pinMode, digitalWrite et delay. Puis on le téléverse, on regarde la carte signaler chaque changement dans le moniteur série, et on joue avec le timing.",
           "🔗 Liens", "Leçon + code Blink", "Tout le code + les leçons", "⏱ Chapitres",
           ["Intro", "Le circuit de l'épisode précédent", "Pourquoi 220 Ω ? La loi d'Ohm", "Déplacer la résistance", "Écrire le code", "Téléverser et clignoter",
            "Ce qui se passe sur la broche", "Jouer avec le timing", "La LED ne clignote pas ?", "Récap et prochain épisode"]),
    "vi": ("ESP32 From Zero #3 — Nháy LED: Chương trình đầu tiên điều khiển phần cứng",
           "Đến lúc code nắm quyền điều khiển! Ta tìm hiểu vì sao LED cần điện trở 220 Ω (định luật Ohm, thật đơn giản), chuyển chân điện trở từ thanh + sang GPIO 23 (bỏ dây đỏ), và viết sketch Blink kinh điển với pinMode, digitalWrite và delay. Sau đó nạp code, xem board báo từng thay đổi trên Serial Monitor, và thử thay đổi thời gian.",
           "🔗 Liên kết", "Bài học + code Blink", "Toàn bộ code + bài học", "⏱ Chương",
           ["Mở đầu", "Mạch của tập trước", "Vì sao 220 Ω? Định luật Ohm", "Chuyển điện trở", "Viết code", "Nạp code và nháy",
            "Điều gì xảy ra ở chân", "Thử thay đổi thời gian", "LED không nháy?", "Tóm tắt và tập sau"]),
    "ja": ("ESP32 From Zero #3 — LEDを点滅させよう：ハードウェアを動かす最初のプログラム",
           "いよいよコードの出番です！LEDに220 Ωの抵抗が必要な理由（かんたんなオームの法則）を学び、抵抗の足をプラスレールからGPIO 23に差し替え（赤いワイヤーは外す）、pinMode、digitalWrite、delayで定番のBlinkスケッチを書きます。書き込んだらシリアルモニタでボードの報告を確認し、タイミングを変えて遊んでみましょう。",
           "🔗 リンク", "レッスン + Blinkコード", "すべてのコード + レッスン", "⏱ チャプター",
           ["イントロ", "前回の回路", "なぜ220 Ω？オームの法則", "抵抗を差し替える", "コードを書く", "書き込んで点滅",
            "ピンで起きていること", "タイミングで遊ぶ", "LEDが点滅しない？", "まとめと次回予告"]),
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
(here / "youtube.md").write_text(f"""# YouTube upload — Episode 3

## Title
{en['title']}

## Description
{en['description']}

## Creator clips (footage/ep03/)
""" + "".join(f"- `{k}` — {v}\n" for k, v in clips.items()) + """
Then: `python tools/build.py video/ep03 compose`.

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep03 <VIDEO_ID>

It uploads every `build/ep03_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`
""", encoding="utf-8")
print("ok", len(out), "languages")
