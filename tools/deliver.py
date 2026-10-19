"""Collect everything ready to upload into one clean folder: YAYIN/ (rebuilt from scratch each run).

Usage: python tools/deliver.py
YAYIN/
  OKU_BENI.txt
  kanal/                      logo, banner, trailer
  ep01/ video.mp4             final English video (intro + outro)
        aciklama_en.txt, aciklama_tr.txt   title + description (chapters included)
        dublaj_sesleri/       tr/hi/pt/es audio tracks (YouTube Studio > Languages)
        altyazilar/           12 .srt files
        kucuk_resimler/       3 thumbnail options
        shorts/               vertical Shorts + their texts
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import sitelink  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "YAYIN"
EPS = ["ep01", "ep02", "ep03", "ep04"]

README = """ESP32 From Zero — yüklemeye hazır dosyalar
==========================================

Her bölüm klasöründe:
  video.mp4            YouTube'a yüklenecek video (İngilizce anlatım)
  aciklama_en.txt      başlık + açıklama (bölüm zamanları dahil)
  aciklama_tr.txt      Türkçe başlık + açıklama
  dublaj_sesleri/      tr, hi, pt, es ses kanalları -> Studio > Diller > Dublaj ekle
  altyazilar/          12 dil .srt (istersen Claude API ile hepsini otomatik yükler)
  kucuk_resimler/      3 seçenek, birini seç
  shorts/              dikey Shorts videoları + açıklamaları

YAYIN_PLANI.md : hangi gün ne atılacak.
kanal/ : logo, banner ve kanal fragmanı.
Gerçek çekim klipleri (C1, C2...) gelince Claude videoları yeniden birleştirir.
"""


def copy(src: Path, dst: Path):
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return True
    print("  missing:", src.relative_to(ROOT))
    return False


def text(entry: dict, lang: str = "en") -> str:
    return f"{entry['title']}\n\n{sitelink.apply(entry['description'], lang)}\n"


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "OKU_BENI.txt").write_text(README, encoding="utf-8")
    copy(ROOT / "video" / "YAYIN_PLANI.md", OUT / "YAYIN_PLANI.md")
    for f in (ROOT / "brand" / "export").glob("*.png"):
        copy(f, OUT / "kanal" / f.name)
    copy(ROOT / "video" / "trailer" / "build" / "trailer_en.mp4", OUT / "kanal" / "fragman.mp4")
    for ep in EPS:
        e, b, d = ROOT / "video" / ep, ROOT / "video" / ep / "build", OUT / ep
        print(ep)
        copy(b / f"{ep}_final.mp4", d / "video.mp4")
        loc = json.loads((e / "localize.json").read_text(encoding="utf-8"))
        for lang in ("en", "tr"):
            (d / f"aciklama_{lang}.txt").write_text(text(loc[lang], lang), encoding="utf-8")
        for lang in ("tr", "hi", "pt", "es"):
            copy(b / f"dub_{lang}.m4a", d / "dublaj_sesleri" / f"{lang}.m4a")
        for srt in sorted(b.glob(f"{ep}_*.srt")):
            copy(srt, d / "altyazilar" / srt.name)
        for png in sorted((ROOT / "video" / "thumbs" / "build").glob(f"{ep}_*.png")):
            copy(png, d / "kucuk_resimler" / png.name)
        s = ROOT / "video" / "shorts" / ep
        for mp4 in sorted((s / "build").glob(f"*/{ep}_short_*.mp4")):
            copy(mp4, d / "shorts" / mp4.name)
        if (s / "youtube.md").exists():
            (d / "shorts").mkdir(parents=True, exist_ok=True)
            (d / "shorts" / "shorts_aciklama.md").write_text(
                sitelink.apply((s / "youtube.md").read_text(encoding="utf-8")), encoding="utf-8")
    size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file()) / 1e6
    print(f"YAYIN/ ready ({size:.0f} MB)")


if __name__ == "__main__":
    main()
