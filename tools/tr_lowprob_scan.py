import sys, json, subprocess, numpy as np
sys.path.insert(0, "tools"); sys.stdout.reconfigure(encoding="utf-8")
import whisper_dev
m = whisper_dev.model("small")
ep = sys.argv[1]; lang = sys.argv[2]
txt = json.load(open(f"{ep}/dub/{lang}.json", encoding="utf-8"))["segments"]
for sid in txt:
    raw = subprocess.run(["ffmpeg","-v","error","-i",f"{ep}/build/dub_{lang}/{sid}.mp3","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32)/32768
    segs = list(m.transcribe(a, language=lang, beam_size=5, word_timestamps=True)[0])
    ws = [w for s in segs for w in (s.words or [])]
    low = [f"{w.word.strip()}:{w.probability:.2f}" for w in ws if w.probability < 0.5]
    if low: print(sid, "|", " ".join(s.text.strip() for s in segs), "|", " ".join(low))
