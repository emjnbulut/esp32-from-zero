"""PRODUCTION_GUIDELINES.md section 6: the TR subtitles must say exactly what the TR dub says.
Compares <ep>/subs/tr.json (display spelling) with <ep>/dub/tr.json (spoken spelling) word by word, after turning
digits into Turkish number words and dropping punctuation. Spelling-only differences of English terms
(GPIO / Ge Pe I O, LED / led, HIGH / hay) still show up: they are expected; reworded lines are not.

Usage: python tools/check_tr_subs.py ep01 [ep02 ...]      (add --all to print every line that differs)
"""
import json, re, sys, difflib
ONES = "sıfır bir iki üç dört beş altı yedi sekiz dokuz".split()
TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
def num(n):
    n = int(n)
    if n == 0: return "sıfır"
    out = []
    for val, word in ((1000000, "milyon"), (1000, "bin"), (100, "yüz")):
        if n >= val:
            q, n = divmod(n, val)
            out += ([] if q == 1 and val != 1000000 else num(q).split()) + [word]
    if n >= 10: out.append(TENS[n // 10]); n %= 10
    if n: out.append(ONES[n])
    return " ".join(out)
def norm(t):
    t = t.lower().replace("ı", "i").replace("İ", "i")
    t = re.sub(r"(\d+),(\d+)", lambda m: num(m.group(1)) + " virgül " + num(m.group(2)), t)
    t = re.sub(r"\d+", lambda m: " " + num(m.group(0)).replace("ı", "i") + " ", t)
    t = re.sub(r"[^a-zçğöşü ]", " ", t)
    return t.split()
def main():
    show_all = "--all" in sys.argv
    for ep in [a for a in sys.argv[1:] if not a.startswith("--")]:
        sc = json.load(open(f"video/{ep}/script.json", encoding="utf-8"))["segments"]
        dub = json.load(open(f"video/{ep}/dub/tr.json", encoding="utf-8"))["segments"]
        try:
            sub = json.load(open(f"video/{ep}/subs/tr.json", encoding="utf-8"))["segments"]
            src = "subs/tr.json"
        except FileNotFoundError:
            sub, src = {s["id"]: s["tr"] for s in sc}, "script.json tr"
        rs = []
        for s in sc:
            a, b = norm(sub.get(s["id"], "")), norm(dub.get(s["id"], ""))
            sm = difflib.SequenceMatcher(None, a, b)
            diffs = [(" ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
            rs.append((sm.ratio(), s["id"], diffs))
        print(f"{ep} ({src} vs dub/tr.json): {len(rs)} segments, mean {sum(r for r, _, _ in rs) / len(rs):.3f}, "
              f"identical {sum(1 for r, _, _ in rs if r == 1)}")
        for r, sid, diffs in sorted(rs):
            if r < 1 and (show_all or r < 0.9):
                print(f"  {sid} {r:.2f}: " + " | ".join(f"{x!r}->{y!r}" for x, y in diffs[:6]))


if __name__ == "__main__":
    main()
