"""Source of video/ep02/localize.json (YouTube title + description per language) and youtube.md.
Usage: python video/ep02/make_localize.py"""
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from rechapter import chapter_times  # noqa: E402

# chapter starts come from chapters.json + the schedule (rerun after the narration changes)
TIMES = chapter_times(Path(__file__).parent)
# "Safe pins" (index 7) started only 9 s before "The breadboard"; YouTube needs >= 10 s, so it is merged into "Pins to avoid"
DROP = 7
CREDIT = '🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/'
REPO = "https://github.com/emjnbulut/esp32-from-zero"
LESSON = REPO + "/tree/main/lessons/02-board-and-breadboard"
TAGS = "#ESP32 #Arduino #Breadboard #Electronics #LED #Microcontroller"

# lang: (title, intro, links header, lesson label, repo label, chapters header, chapter names)
T = {
    "en": ("ESP32 From Zero #2 — Pins, Breadboard & Your First LED Circuit",
           "Meet your ESP32's pins and the breadboard! We learn the power pins (3V3, 5V, GND), which GPIO pins are safe to use and which to avoid (flash, input-only, strapping, TX/RX), how a breadboard is wired inside, and build our first circuit: an LED with a 220 Ω resistor. No code needed.",
           "🔗 Links", "Lesson + pin tables", "All code + lessons", "⏱ Chapters",
           ["Intro", "What you need", "The pins", "Power pins", "Two safety rules", "GPIO pins", "Pins to avoid", "Safe pins", "The breadboard",
            "Board on the breadboard", "LED and resistor", "Build the circuit", "Power on!", "Recap and next episode"]),
    "tr": ("ESP32 From Zero #2 — Pinler, Breadboard ve İlk LED Devren",
           "ESP32'nin pinleriyle ve breadboard ile tanış! Güç pinlerini (3V3, 5V, GND), hangi GPIO pinlerinin güvenli olduğunu ve hangilerinden kaçınman gerektiğini (flash, yalnızca giriş, strapping, TX/RX), breadboard'un içinin nasıl bağlı olduğunu öğreniyor ve ilk devremizi kuruyoruz: 220 Ω dirençli bir LED. Kod gerekmiyor.",
           "🔗 Bağlantılar", "Ders + pin tabloları", "Tüm kodlar + dersler", "⏱ Bölümler",
           ["Giriş", "Gerekenler", "Pinler", "Güç pinleri", "İki güvenlik kuralı", "GPIO pinleri", "Kaçınılacak pinler", "Güvenli pinler", "Breadboard",
            "Kart breadboard'da", "LED ve direnç", "Devreyi kur", "Güç ver!", "Özet ve sonraki bölüm"]),
    "hi": ("ESP32 From Zero #2 — Pins, Breadboard और आपका पहला LED Circuit",
           "ESP32 के pins और breadboard को जानिए! हम power pins (3V3, 5V, GND) सीखते हैं, कौन से GPIO pins safe हैं और किनसे बचना है (flash, input-only, strapping, TX/RX), breadboard अंदर से कैसे जुड़ा है, और अपना पहला circuit बनाते हैं: 220 Ω resistor के साथ एक LED। कोई code नहीं चाहिए।",
           "🔗 Links", "Lesson + pin tables", "सारा code + lessons", "⏱ Chapters",
           ["Intro", "क्या चाहिए", "Pins", "Power pins", "दो safety नियम", "GPIO pins", "किन pins से बचें", "Safe pins", "Breadboard",
            "Board breadboard पर", "LED और resistor", "Circuit बनाइए", "Power on!", "Recap और अगला episode"]),
    "pt": ("ESP32 From Zero #2 — Pinos, Protoboard e Seu Primeiro Circuito com LED",
           "Conheça os pinos do ESP32 e a protoboard! Vemos os pinos de alimentação (3V3, 5V, GND), quais GPIO são seguros e quais evitar (flash, só entrada, strapping, TX/RX), como a protoboard é ligada por dentro, e montamos nosso primeiro circuito: um LED com resistor de 220 Ω. Sem código.",
           "🔗 Links", "Aula + tabelas de pinos", "Todo o código + aulas", "⏱ Capítulos",
           ["Introdução", "O que você precisa", "Os pinos", "Pinos de alimentação", "Duas regras de segurança", "Pinos GPIO", "Pinos a evitar", "Pinos seguros", "A protoboard",
            "Placa na protoboard", "LED e resistor", "Montando o circuito", "Ligando!", "Resumo e próximo episódio"]),
    "es": ("ESP32 From Zero #2 — Pines, Protoboard y Tu Primer Circuito con LED",
           "¡Conoce los pines del ESP32 y la protoboard! Vemos los pines de alimentación (3V3, 5V, GND), qué GPIO son seguros y cuáles evitar (flash, solo entrada, arranque, TX/RX), cómo está conectada la protoboard por dentro, y armamos nuestro primer circuito: un LED con una resistencia de 220 Ω. Sin código.",
           "🔗 Enlaces", "Lección + tablas de pines", "Todo el código + lecciones", "⏱ Capítulos",
           ["Intro", "Lo que necesitas", "Los pines", "Pines de alimentación", "Dos reglas de seguridad", "Pines GPIO", "Pines que evitar", "Pines seguros", "La protoboard",
            "La placa en la protoboard", "LED y resistencia", "Arma el circuito", "¡Enciende!", "Resumen y próximo episodio"]),
    "id": ("ESP32 From Zero #2 — Pin, Breadboard & Rangkaian LED Pertamamu",
           "Kenali pin ESP32 dan breadboard! Kita belajar pin daya (3V3, 5V, GND), pin GPIO mana yang aman dan mana yang harus dihindari (flash, input saja, strapping, TX/RX), bagaimana breadboard tersambung di dalam, lalu merakit rangkaian pertama: LED dengan resistor 220 Ω. Tanpa kode.",
           "🔗 Link", "Materi + tabel pin", "Semua kode + materi", "⏱ Bab",
           ["Intro", "Yang dibutuhkan", "Pin", "Pin daya", "Dua aturan keselamatan", "Pin GPIO", "Pin yang dihindari", "Pin aman", "Breadboard",
            "Board di breadboard", "LED dan resistor", "Rakit rangkaian", "Nyalakan!", "Ringkasan dan episode berikutnya"]),
    "ar": ("ESP32 From Zero #2 — الأطراف ولوحة التجارب وأول دائرة LED لك",
           "تعرّف على أطراف ESP32 ولوحة التجارب! نتعلم أطراف التغذية (3V3 و5V وGND)، وأي أطراف GPIO آمنة وأيها يجب تجنبه (الفلاش، الدخل فقط، أطراف الإقلاع، TX/RX)، وكيف توصَّل لوحة التجارب من الداخل، ونبني أول دائرة: LED مع مقاومة 220 Ω. بدون كود.",
           "🔗 روابط", "الدرس + جداول الأطراف", "كل الكود + الدروس", "⏱ الفصول",
           ["مقدمة", "ما تحتاجه", "الأطراف", "أطراف التغذية", "قاعدتا أمان", "أطراف GPIO", "أطراف يجب تجنبها", "الأطراف الآمنة", "لوحة التجارب",
            "اللوحة على لوحة التجارب", "LED والمقاومة", "بناء الدائرة", "التشغيل!", "ملخص والحلقة القادمة"]),
    "ru": ("ESP32 From Zero #2 — Пины, макетная плата и первая схема со светодиодом",
           "Знакомимся с пинами ESP32 и макетной платой! Разбираем пины питания (3V3, 5V, GND), какие GPIO безопасны, а каких избегать (flash, только вход, стартовые, TX/RX), как макетка устроена внутри, и собираем первую схему: светодиод с резистором 220 Ω. Без кода.",
           "🔗 Ссылки", "Урок + таблицы пинов", "Весь код + уроки", "⏱ Главы",
           ["Вступление", "Что понадобится", "Пины", "Пины питания", "Два правила безопасности", "Пины GPIO", "Каких пинов избегать", "Безопасные пины", "Макетная плата",
            "Плата на макетке", "Светодиод и резистор", "Собираем схему", "Включаем!", "Итоги и следующий выпуск"]),
    "de": ("ESP32 From Zero #2 — Pins, Breadboard & deine erste LED-Schaltung",
           "Lerne die Pins deines ESP32 und das Breadboard kennen! Wir behandeln die Versorgungs-Pins (3V3, 5V, GND), welche GPIOs sicher sind und welche du meiden solltest (Flash, nur Eingang, Strapping, TX/RX), wie ein Breadboard innen verbunden ist, und bauen unsere erste Schaltung: eine LED mit 220-Ω-Widerstand. Ganz ohne Code.",
           "🔗 Links", "Lektion + Pin-Tabellen", "Gesamter Code + Lektionen", "⏱ Kapitel",
           ["Intro", "Das brauchst du", "Die Pins", "Versorgungs-Pins", "Zwei Sicherheitsregeln", "GPIO-Pins", "Pins, die du meiden solltest", "Sichere Pins", "Das Breadboard",
            "Board aufs Breadboard", "LED und Widerstand", "Schaltung aufbauen", "Strom an!", "Rückblick und nächste Folge"]),
    "fr": ("ESP32 From Zero #2 — Broches, breadboard et ton premier circuit LED",
           "Découvre les broches de l'ESP32 et la breadboard ! On voit les broches d'alimentation (3V3, 5V, GND), quelles GPIO sont sûres et lesquelles éviter (flash, entrée seule, strapping, TX/RX), comment une breadboard est câblée à l'intérieur, et on monte notre premier circuit : une LED avec une résistance de 220 Ω. Sans code.",
           "🔗 Liens", "Leçon + tableaux des broches", "Tout le code + les leçons", "⏱ Chapitres",
           ["Intro", "Le matériel", "Les broches", "Broches d'alimentation", "Deux règles de sécurité", "Broches GPIO", "Broches à éviter", "Broches sûres", "La breadboard",
            "La carte sur la breadboard", "LED et résistance", "Monter le circuit", "On allume !", "Récap et prochain épisode"]),
    "vi": ("ESP32 From Zero #2 — Chân, Breadboard và Mạch LED đầu tiên",
           "Làm quen với các chân của ESP32 và breadboard! Ta học chân nguồn (3V3, 5V, GND), chân GPIO nào an toàn và chân nào nên tránh (flash, chỉ vào, strapping, TX/RX), breadboard được nối bên trong ra sao, và lắp mạch đầu tiên: một LED với điện trở 220 Ω. Không cần code.",
           "🔗 Liên kết", "Bài học + bảng chân", "Toàn bộ code + bài học", "⏱ Chương",
           ["Mở đầu", "Cần chuẩn bị", "Các chân", "Chân nguồn", "Hai quy tắc an toàn", "Chân GPIO", "Chân nên tránh", "Chân an toàn", "Breadboard",
            "Board trên breadboard", "LED và điện trở", "Lắp mạch", "Cấp điện!", "Tóm tắt và tập sau"]),
    "ja": ("ESP32 From Zero #2 — ピン、ブレッドボード、はじめてのLED回路",
           "ESP32のピンとブレッドボードを知ろう！電源ピン（3V3、5V、GND）、安全に使えるGPIOと避けるべきピン（フラッシュ、入力専用、ストラッピング、TX/RX）、ブレッドボードの内部の配線を学び、最初の回路を作ります：220 Ωの抵抗付きLED。コードは不要です。",
           "🔗 リンク", "レッスン + ピン表", "すべてのコード + レッスン", "⏱ チャプター",
           ["イントロ", "必要なもの", "ピン", "電源ピン", "2つの安全ルール", "GPIOピン", "避けるべきピン", "安全なピン", "ブレッドボード",
            "ボードをブレッドボードに", "LEDと抵抗", "回路を組む", "電源オン！", "まとめと次回予告"]),
}

out = {}
for lang, (title, intro, links, lesson, repo, chap, names) in T.items():
    names = names[:DROP] + names[DROP + 1:]
    assert len(names) == len(TIMES) and len(title) <= 100, lang
    desc = (f"{intro}\n\n{links}\n• {lesson}: {LESSON}\n• {repo}: {REPO}\n\n{chap}\n"
            + "\n".join(f"{t} {n}" for t, n in zip(TIMES, names)) + f"\n\n{CREDIT}\n\n{TAGS}")
    assert "<" not in desc and ">" not in desc and len(desc) <= 5000, lang
    out[lang] = {"title": title, "description": desc}
here = Path(__file__).parent
(here / "localize.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

en = out["en"]
(here / "youtube.md").write_text(f"""# YouTube upload — Episode 2

## Title
{en['title']}

## Description
{en['description']}

## Creator clips (footage/ep02/)
- `C1` — Close-up of the board's pin labels (3V3, GND, D2...). Slowly pan along one header so the tiny printed names are readable. Landscape, 5-8 s.
- `C2` — Hands pressing the ESP32 board into the breadboard across the middle gap, evenly on both sides. Landscape, 5-8 s.
- `C3` — The finished circuit (3V3 -> resistor -> LED -> GND). Plug in the USB cable and the LED turns on. Landscape, 5-8 s.

Then: `python tools/build.py video/ep02 compose`.

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep02 <VIDEO_ID>

It uploads every `build/ep02_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`
""", encoding="utf-8")
print("ok", len(out), "languages")
