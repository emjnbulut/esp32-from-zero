"""Adds the learning-site line to a YouTube description (all 12 languages), once.

The line goes just before the chapter list (or, when there is none, before the music credit / hashtags),
so every episode and Short points to the free practice site with the extra homework.
"""
SITE = "https://emjnbulut.github.io/esp32-learning-lab/"

LINE = {
    "en": "🧪 Extra practice & homework, free in your browser:",
    "tr": "🧪 Ek alıştırmalar ve ödevler (ücretsiz, tarayıcıda):",
    "hi": "🧪 अतिरिक्त अभ्यास और होमवर्क (मुफ़्त, ब्राउज़र में):",
    "pt": "🧪 Exercícios extras e lição de casa (grátis, no navegador):",
    "es": "🧪 Práctica extra y tareas (gratis, en el navegador):",
    "id": "🧪 Latihan tambahan dan PR (gratis, di browser):",
    "ar": "🧪 تمارين ومهام إضافية (مجانًا، في المتصفح):",
    "ru": "🧪 Дополнительная практика и домашние задания (бесплатно, в браузере):",
    "de": "🧪 Zusätzliche Übungen und Hausaufgaben (kostenlos, im Browser):",
    "fr": "🧪 Exercices et devoirs supplémentaires (gratuit, dans le navigateur) :",
    "vi": "🧪 Bài tập và luyện tập thêm (miễn phí, ngay trên trình duyệt):",
    "ja": "🧪 追加の練習と宿題（無料、ブラウザで）：",
}
ANCHORS = ("⏱", "🎵", "#")  # first one found, at the start of a line


def apply(desc: str, lang: str = "en") -> str:
    if SITE in desc:
        return desc
    block = f"{LINE.get(lang, LINE['en'])}\n{SITE}\n\n"
    lines = desc.split("\n")
    for anchor in ANCHORS:
        for i, ln in enumerate(lines):
            if ln.startswith(anchor):
                return "\n".join(lines[:i]) + ("\n" if i else "") + block + "\n".join(lines[i:])
    return desc.rstrip("\n") + "\n\n" + block.rstrip("\n") + "\n"
