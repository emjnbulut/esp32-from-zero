"""Source of video/recap1/localize.json (YouTube title + description, en + tr) and youtube.md.
Chapter times come from build/schedule.json (the channel sting after the cold open shifts later chapters).
Usage: python video/recap1/make_localize.py"""
import json
import sys
from pathlib import Path

here = Path(__file__).parent
ROOT = here.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bumpers  # noqa: E402

CHAPTERS = ["s01", "s03", "s11", "s15", "s22", "s29", "s35", "s38", "s45"]
segs = json.loads((here / "build" / "schedule.json").read_text(encoding="utf-8"))["segments"]
tc = bumpers.cut(here)
starts = [0] + [int(bumpers.shift(segs[c]["start"], tc)) for c in CHAPTERS[1:]]
assert all(b - a >= 10 for a, b in zip(starts, starts[1:])), "YouTube chapters must be at least 10 s"
TIMES = ["%d:%02d" % divmod(s, 60) for s in starts]
# the credit lines are the same on every episode: take them from episode 5's description
ep5 = json.loads((ROOT / "video" / "ep05" / "localize.json").read_text(encoding="utf-8"))["en"]["description"]
CREDIT = "\n".join(l for l in ep5.split("\n") if l.startswith(("🎵", "🎙")))
REPO = "https://github.com/emjnbulut/esp32-from-zero"
LESSONS = REPO + "/tree/main/lessons"
TAGS = "#ESP32 #Arduino #Programming #Electronics #Beginners"

T = {
    "en": ("How to Read ESP32 Code: Variables, setup() and loop() Explained | ESP32 From Zero Recap",
           "Code still confusing? In this recap we go through all five sketches from episodes 1 to 4 and watch every variable change, line by line. You learn the three parts every sketch has (names, setup, loop), why a variable is the sketch's memory, how a button press is detected with lastState, and how millis() lets a sketch blink and read a button at the same time. Then three quick practice questions to test yourself.",
           "🔗 Links", "All lessons + sketches", "All code", "⏱ Chapters",
           ["Five sketches (demo)", "The skeleton: names, setup, loop", "Outputs: pinMode and digitalWrite", "Decisions: digitalRead and if", "Memory: lastState and presses", "The clock: millis()", "The four questions", "Your turn: three quick ones", "Recap and next episode"]),
    "tr": ("ESP32 Kodu Nasıl Okunur: Değişkenler, setup() ve loop() | ESP32 From Zero Özet",
           "Kod hâlâ kafa mı karıştırıyor? Bu özette 1. ile 4. bölümler arasındaki beş sketch'in hepsini adım adım geziyor ve her değişkenin satır satır nasıl değiştiğini izliyoruz. Her sketch'in üç parçasını (isimler, setup, loop), değişkenin neden sketch'in hafızası olduğunu, bir buton basışının lastState ile nasıl yakalandığını ve millis() ile sketch'in aynı anda nasıl yanıp sönüp butonu okuduğunu öğreniyorsunuz. Sonunda kendinizi sınamak için üç kısa soru var.",
           "🔗 Bağlantılar", "Tüm dersler + sketch'ler", "Tüm kodlar", "⏱ Bölümler",
           ["Beş sketch (demo)", "İskelet: isimler, setup, loop", "Çıkışlar: pinMode ve digitalWrite", "Kararlar: digitalRead ve if", "Hafıza: lastState ve presses", "Saat: millis()", "Dört soru", "Sıra sizde: üç kısa soru", "Özet ve sonraki bölüm"]),
}
out = {}
for lang, (title, intro, links, lessons, repo, chap, names) in T.items():
    assert len(names) == len(TIMES) and len(title) <= 100, (lang, len(title))
    desc = (f"{intro}\n\n{links}\n• {lessons}: {LESSONS}\n• {repo}: {REPO}\n\n{chap}\n"
            + "\n".join(f"{t} {n}" for t, n in zip(TIMES, names)) + f"\n\n{CREDIT}\n\n{TAGS}")
    assert "<" not in desc and ">" not in desc and len(desc) <= 5000, lang
    out[lang] = {"title": title, "description": desc}
(here / "localize.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

clips = json.loads((here / "script.json").read_text(encoding="utf-8"))["clips"]
en = out["en"]
(here / "youtube.md").write_text(f"""# YouTube upload — Recap (episodes 1-4: how to read a sketch)

Numberless special, scheduled Fri 30 Oct 2026 17:00 (video/YAYIN_TAKVIMI.md). Not a numbered episode, so no "#N" in the title.
Thumbnail: video/thumbs/build/recap_A.png ("READ ANY SKETCH", Claude's choice, user 2026-10-25 rule).
AI label: own-voice clone narration, no realistic synthetic people or events -> "No" (PRODUCTION_GUIDELINES.md).

## Title
{en['title']}

## Description
{en['description']}

## Footage used (reused, footage/recap1/)
""" + "".join(f"- `{k}` — {v}\n" for k, v in clips.items()) + """
## Files
- English video: `build/recap1_final.mp4`
- Subtitles: `build/recap1_en.srt`, `build/recap1_tr.srt`
- Turkish dub (audio track + video): `build/dub_tr.m4a`, `build/recap1_tr_dub.mp4`
- Titles/descriptions per language: `localize.json` (en, tr). After the upload: `python tools/publish.py video/recap1 <VIDEO_ID>`
""", encoding="utf-8")
print("chapters:", ", ".join(f"{t} {n}" for t, n in zip(TIMES, T["en"][6])))
