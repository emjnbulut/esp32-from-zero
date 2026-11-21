# TTS upgrade research (EN / TR / HI, PT / ES secondary), 2026-11-21

Goal: dubs that sound clearly better, mainly a natural delivery, a native accent, and correct technical terms
(GPIO, ESP32, millis, OLED, "Preferences", "214 milliseconds"). The voice stays the creator's own clone
(no AI label, see section 2c). No time-stretch, no speed-up (guidelines section 9).
Hardware: RTX 4060 Laptop with 8 GB VRAM, Windows 11. Today's stack: chatterbox-tts 0.1.7, Multilingual **V2** T3,
creator timbre + FLEURS accent prompt, Whisper-small checks (`dub_check.py`, `tr_lowprob_scan.py`, `cbx_fixline.py`).
Numbers marked "vendor" come from the model's own README. They show a direction and are not a neutral benchmark.

## 0. Four findings that change the plan

1. **Chatterbox has a newer multilingual checkpoint we don't use.** `t3_mtl23ls_v3.safetensors` (2.1 GB) gives
   "better speaker similarity and accent preservation across languages" and "reduc[es] unwanted continuation,
   repetition, and off-prompt speech", which is exactly the Hindi rambling problem. There is also a **Hindi-only
   finetune** (`ResembleAI/Chatterbox-Multilingual-hi`, MIT). Our pip 0.1.7 (2026-03-26) hard-codes `t3_mtl23ls_v2`.
   GitHub master loads `t3_model="v3"` and keeps the same `s3gen.pt` we already have.
   Caveat: the README says "As of August 2026, Chatterbox is retired research and is no longer maintained" (MIT
   archive), so no further fixes will come. https://github.com/resemble-ai/chatterbox ,
   https://huggingface.co/ResembleAI/chatterbox/tree/main , https://huggingface.co/ResembleAI/Chatterbox-Multilingual-hi
2. **VoxCPM2 (OpenBMB, 2026-04, Apache-2.0, 2B, ~8 GB VRAM) has the best published open Turkish numbers.** On
   MiniMax-MLS (vendor): Turkish WER 0.82 / SIM 87.1, against ElevenLabs 0.70 / 59.6, MiniMax 1.52 / 77.9 and Fish S2
   0.87 / 83.5. Hindi is its weak spot: WER 19.7 against ElevenLabs 5.8 and MiniMax 7.0. It outputs 48 kHz and supports
   "ultimate cloning" (reference audio plus its transcript) and LoRA from 5-10 min of audio.
   https://github.com/OpenBMB/VoxCPM , https://huggingface.co/openbmb/VoxCPM2
3. **ElevenLabs Eleven v4 (Sept 2026) brings back Professional Voice Clones and speaks 90+ languages incl. TR and HI.**
   Docs: "Cross-language generation produces fluent speech in the target language by default, without the reference
   accent." That is the native-accent behaviour we currently fake with FLEURS prompts.
   https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4.md
4. **Google Gemini 3.8 Flash TTS (2026-09-24) offers self-serve voice replication** with a consent recording.
   tr-TR and hi-IN are among the consent locales, and the Gemini API is available in Türkiye. It is very cheap
   (see 2a) and adds a SynthID watermark. https://ai.google.dev/gemini-api/docs/voice-replication ,
   https://ai.google.dev/gemini-api/docs/pricing , https://ai.google.dev/gemini-api/docs/available-regions

## 1. Open / local models (zero-shot cloning, 8 GB VRAM, Windows)

"OK commercial" means the weights may be used on a monetized channel. NC = non-commercial, so it is ruled out.

| Model | EN / TR / HI | Clone quality and accent (evidence) | VRAM, size | License | Windows friction | Verdict |
|---|---|---|---|---|---|---|
| **Chatterbox Multilingual V3** (Resemble) | yes / yes / yes (23 langs) | Vendor: better SIM and accent, fewer hallucinations than V2. TR still has open issue #261 "Turkish doesn't sound right". | same as now (~5-6 GB), +2.1 GB file | MIT, OK commercial (PerTh watermark) | none, drop-in for our venv | **Try first** (cheapest win) |
| **Chatterbox Multilingual-hi** (Single Language Pack) | HI only | Hindi finetune of V3. No numbers published. | `t3_hi` 2.1 GB + `s3gen_v3` 1.1 GB | MIT | low (needs master code or a small loader patch) | **Try for HI** |
| Chatterbox Turbo / Nano | EN only | 350M, paralinguistic tags, 1-step decoder | less than now | MIT | low | EN speed only, not quality |
| **VoxCPM2** (OpenBMB) | yes / yes / yes (30 langs) | TR best open (see 0.2). HI WER 19.7 (weak). 48 kHz. Reference+transcript cloning. | **~8 GB (tight on 8 GB laptop)**, 4.6 GB + 0.38 GB | Apache-2.0, OK commercial | medium: separate venv, `pip install voxcpm`, Python 3.10-3.12, torch >= 2.5 | **Try for TR and EN** |
| ZONOS3-Mini (Zyphra, 2026-11-12) | yes / yes / yes (43 langs) | Vendor "ranks first among open-weight models", but no per-language numbers. No text normalization for tr/hi. | 0.9B (100M active), size n/a | Apache-2.0 | unknown: Windows not documented, 10 days old | Watch list, round 2 |
| MOSS-TTS v1.5 (OpenMOSS) | yes / yes / yes | stable cloning (vendor) | 8B (4B smallest), needs llama.cpp tricks for 8 GB | Apache-2.0 | high | Too big |
| Fish Audio S2 Pro (open weights) | yes / tier 3 / tier 3 | strong SIM | 5B | Fish Research License, **NC** | high | No (use their API instead) |
| OmniVoice (k2-fsa) | 600+ langs | n/a | 0.6B | weights **CC-BY-NC** (Emilia data) | medium | No |
| XTTS-v2 (Coqui) | yes / yes / yes | dated, accent leaks | ~4 GB | CPML **NC**, company closed, no paid license | medium | No |
| F5-TTS + `marduk-ra/F5-TTS-Turkish` | TR finetune on Common Voice | community, ~45 h data | 1.35 GB | base and finetune **CC-BY-NC** | medium | No |
| IndicF5 (AI4Bharat) | HI (+10 Indic) | native Indic speakers (1,417 h), ref audio + transcript | 0.4B fp32, ~1.4 GB, gated | MIT | medium | Optional HI candidate |
| Indic Parler-TTS | HI | NSS Hindi 84.8 %, but **no cloning** (preset Rohit/Divya) | 0.9B | Apache-2.0 | medium | No (not creator's voice) |
| Kokoro-82M | EN, HI (grade C), PT, ES; no TR | no cloning | tiny | Apache-2.0 | low | No |
| Qwen3-TTS (2026-01) | EN, PT, ES, no TR/HI | 3-s clone | 0.6B / 1.7B | Apache-2.0 | medium | Maybe for PT/ES later |
| Fun-CosyVoice3 | EN, ES, no TR/HI/PT | good | 0.5B | Apache-2.0 | medium | No |
| Higgs Audio v2, IndexTTS2, Spark-TTS, MegaTTS3, VibeVoice, Orpheus-multi, Zonos v0.1 | mostly EN/ZH; Orpheus has HI but no zero-shot clone | n/a | 3-6B for Higgs | custom / NC / partly withheld | n/a | No |

Sources: https://huggingface.co/k2-fsa/OmniVoice , https://huggingface.co/fishaudio/s2-pro ,
https://huggingface.co/blog/Zyphra/zonos3-mini , https://github.com/OpenMOSS/MOSS-TTS ,
https://huggingface.co/marduk-ra/F5-TTS-Turkish , https://huggingface.co/ai4bharat/IndicF5 ,
https://huggingface.co/ai4bharat/indic-parler-tts , https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md ,
https://github.com/QwenLM/Qwen3-TTS , https://github.com/FunAudioLLM/CosyVoice ,
https://github.com/resemble-ai/chatterbox/issues/261 . Turkish-specific research: Alania-2 (arXiv 2611.13845) finds that
text normalization dominated digit errors (0/96 → 86/96 digit sentences correct) and that 20-30 s of reference audio
works best for cloning. Our TR reference is 14.2 s and the raw recording is 48 s, so a longer cut is free to try.
Hindi research: Praxy Voice (arXiv 2604.25441) builds on Chatterbox and reports code-mixed Hindi as the big failure
mode (LLM-WER 0.80 → 0.14-0.27 after transliterating English words into native script).

## 2. Paid APIs

### 2a. Cost for our volume
Volume: 2 episodes/week × ~7,000 chars ≈ **61k chars per language per month**. EN+TR+HI is ~183k, five languages
~305k. Add ~30 % for retakes and best-of-N: **~240k (3 langs) / ~400k (5 langs)** per month.

| Service | Clone of creator? | TR / HI | Price for our volume | Notes |
|---|---|---|---|---|
| **ElevenLabs v4** | IVC from ~1-2 min audio (Starter+), PVC (Creator+, 1 slot) | yes / yes (90+ langs) | UI credits: Creator $22 = 121k (only HI fits), **Pro $99 = 600k (5 langs + retakes)**. API rate: $0.08 per 1k chars (v4, v3, Multilingual v2), $0.04 per 1k (v4 Turbo, Flash), so 240k ≈ $19, 400k ≈ $32. | Black Friday until **Dec 1**: Creator annual $99/yr (55 % off). v3 Hindi WER 5.8 in VoxCPM's table (best listed). No SSML on v4. |
| **Gemini 3.8 Flash TTS** voice replication | yes (10-30 s sample + consent clip, paid tier) | yes / yes (30 consent locales) | $18 per 1M audio tokens from 2027-01-01 ($9 until then), 25 tokens/s, ≈ **$1.6 per hour of audio**. 5 langs × ~12 min × 8.7 eps ≈ 8.7 h ≈ **$14/month** (batch tier half). | SynthID watermark plus C2PA. Quality for TR/HI unknown, so it needs the bake-off. |
| Cartesia Sonic-3.6 | IVC (Pro $5), PVC (Startup $49) | yes / yes (44 langs, Hinglish improved) | Pro $5 = 100k credits, Startup $49 = 1.25M | Praxy: Hindi LLM-WER tied with Sonic-3. Good dark horse. |
| Fish Audio (API, S2.1 Pro) | yes | "other" tier (below tier 1-2) | Plus $15/mo (or $11 annual), 250k credits ≈ 400 min, commercial OK | TR/HI are not their focus |
| MiniMax Speech (API) | yes | yes / yes | not checked | MLS table: HI WER 7.0 / SIM 81.8, TR 1.52 / 77.9 |
| Sarvam Bulbul v4-flash | **no cloning** (83 preset voices) | – / native HI | ₹20 per 10k chars (~₹1.2k/month for HI) | Most native Hindi, but loses the creator's voice |
| Azure personal voice | yes | yes / yes | per pricing page | Gated: intake form, "business customers ... for their users", approved use cases only. Poor fit for us. |
| Google Chirp 3 instant custom voice | yes | yes / yes | sales | Allow-list via sales; Gemini 3.8 replaces it for us |
| OpenAI TTS | custom voices gated via sales | presets | – | Not usable for a clone |

Sources: https://elevenlabs.io/pricing , https://elevenlabs.io/pricing/api , https://elevenlabs.io/docs/overview/models ,
https://elevenlabs.io/blog/eleven-v4 , https://cartesia.ai/pricing , https://docs.cartesia.ai/build-with-cartesia/tts-models/latest ,
https://fish.audio/plan/ , https://www.sarvam.ai/apis/text-to-speech ,
https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-overview ,
https://docs.cloud.google.com/text-to-speech/docs/chirp3-instant-custom-voice ,
https://developers.openai.com/api/docs/guides/custom-voices

### 2b. Licensing for a monetized channel
Paid ElevenLabs, Cartesia and Fish plans include commercial use (free tiers do not). Gemini needs a paid-tier
project. MIT and Apache local models (Chatterbox, VoxCPM2, ZONOS3, IndicF5) are fine. NC weights (XTTS, F5,
Fish S2 open, OmniVoice) are not. All cloud clones need the creator's own consent recording, and he has that right
for his own voice.

### 2c. YouTube AI disclosure
YouTube lists "Cloning one's own voice to create voice overs or dubs" under **Minor (no disclosure)**
(https://support.google.com/youtube/answer/14328491, checked 2026-11-21). So **every option above that clones the
creator** (Chatterbox, VoxCPM2, ElevenLabs, Gemini, Cartesia, Fish) keeps the answer **"No"**. A **preset voice**
(Sarvam, Indic Parler, Kokoro, OpenAI) is not his voice, so that reasoning no longer covers it. Such a voice is not
on YouTube's must-disclose list either (that list is about real people and real events), but it would need a fresh
decision and it breaks the channel's "creator's own voice" rule. One risk: Gemini audio carries SynthID and C2PA.
C2PA is stripped by our ffmpeg mix, but YouTube says it may add labels itself, and whether it detects SynthID audio
is unverified.

## 3. Automatic quality checks (auto-pick the best of N takes)

Score every take, pick the best, and flag a line for a human only when even the best take fails a gate.

| Metric | Tool (size) | What it catches | Per-language note |
|---|---|---|---|
| **CER vs the script** | faster-whisper `large-v3-turbo` (~1.6 GB) or `large-v3` (~3 GB) instead of `small` | wrong words, skipped words, **rambling/hallucinated tails** (insertions) | Normalize both sides first (numbers spelled out, punctuation stripped). For HI compare in Devanagari. Whisper-HI is noisier, so set a looser threshold. |
| **Duration ratio** | ffprobe (free) | rambling (too long), truncation (too short) | ratio to chars × the language's median sec/char. Reject outside 0.8-1.25. Already partly in `cbx_retake.py`. |
| **Speaker similarity** | SpeechBrain ECAPA `spkrec-ecapa-voxceleb` (~80 MB, Apache) or WavLM-large-SV (Seed-TTS-eval's SIM) | voice drift away from the creator | language-independent. Compare to `creator_en.wav` / `creator_tr.wav`. |
| **Naturalness MOS** | UTMOSv2 (MIT, https://github.com/sarulab-speech/UTMOSv2) | flat or robotic delivery, artefacts | trained mostly on English; arXiv 2601.20185 reports it usable on multilingual data. Use it as a *relative* ranker within one line. |
| Signal quality | DNSMOS P.835 (ONNX, few MB, microsoft/DNS-Challenge) or Distill-MOS | noise, clicks, denoiser damage | language-agnostic |
| Aesthetics | Meta Audiobox Aesthetics (CC-BY 4.0, https://github.com/facebookresearch/audiobox-aesthetics) | production quality (PQ) and "content enjoyment" (CE) | language-agnostic, but a newer and less proven ranker |
| Word confidence | existing `tr_lowprob_scan.py` | mispronounced single terms | keep it. Run it on the chosen take only. |

Selection rule (suggested `tools/take_score.py`, works with any engine):
1. Generate N = 4 takes per line (different seeds or temperature).
2. Hard gates: CER ≤ 3 % (EN), 5 % (TR), 8 % (HI); duration ratio within 0.8-1.25; no pause > 1.0 s mid-sentence.
3. Rank the survivors by `z(SIM) + z(UTMOSv2) + 0.5·z(DNSMOS) − z(CER)`, with z-scores computed within the line.
4. If nothing passes, try 4 more takes. If that fails too, list the line for a text rewrite (shorter sentence,
   respelled term).
Speaker similarity, UTMOS and DNSMOS run in a few hundred ms per line on the 4060, so cost is dominated by generation.
For paid APIs, N = 2 is usually enough, and best-of-N multiplies character cost.

## 4. Recommendation

### 4a. The text front-end comes first (free, helps every engine)
Most term errors are text problems, not engine problems (Alania-2, Praxy).
- `tools/lexicon/{tr,hi,pt,es}.json`: respellings the creator approves once, for example TR `GPIO → "ci pi ay o"`
  (or `"ge pe ı o"`, his choice), `ESP32 → "e es pe otuz iki"`, `millis → "milis"`, `OLED → "o-led"`,
  `Preferences → "prefıranses"`. Applied only to the TTS text, while subtitles keep the real spelling.
- Numbers: `num2words` (supports tr, hi, pt, es) plus units: "214 ms" → "iki yüz on dört milisaniye".
- Hindi: write every English term in **Devanagari** (जीपीआईओ, मिलिस, ओएलईडी). Latin words inside Devanagari are a
  known trigger for rambling and accent breaks. Keep sentences ≤ 20 words.
- Chatterbox setting: with a cross-language prompt the README says to lower `cfg_weight` (0 removes accent
  transfer). Test 0.3 and 0.0 on HI/PT/ES, where the timbre prompt is the English recording.
- Cut a longer reference from the raw recordings (EN 58 s, TR 48 s available) to ~25 s for VoxCPM2 and Chatterbox,
  and use the whole ~1 min for an ElevenLabs IVC.

### 4b. Engines per language (expected result, to be confirmed by the bake-off)
| Lang | Primary | Fallback | Why |
|---|---|---|---|
| EN | keep Chatterbox EN (already approved) unless VoxCPM2 or ElevenLabs clearly wins | VoxCPM2 | EN is already the strongest; low priority |
| TR | **VoxCPM2** (local, Apache) | Chatterbox V3 + lexicon | best published open TR WER/SIM; 48 kHz; LoRA on the creator's TR audio is possible later |
| HI | **ElevenLabs v4 IVC** (or Gemini 3.8 if it scores close: about 5× cheaper) | Chatterbox Multilingual-hi | open models trail on Hindi (VoxCPM2 WER 19.7); ElevenLabs is best in the only cross-vendor table, and v4 speaks the target language natively by default |
| PT/ES | Chatterbox V3 (or the PT/ES language packs) | ElevenLabs if a plan is bought anyway | secondary |

Cost if the bake-off confirms this: local TR and EN cost nothing. HI only on ElevenLabs is ~80k chars/month incl.
retakes, which fits Creator ($22/mo, or $99/yr until Dec 1). If ElevenLabs also wins TR, take Pro ($99/mo) or pay
API rates (~$20-30/mo).

### 4c. Downloads (ask before each, they are all > 100 MB)
| Item | Size | For |
|---|---|---|
| `ResembleAI/chatterbox` → `t3_mtl23ls_v3.safetensors` | 2.14 GB | TR/HI/PT/ES V3 (reuses our `s3gen.pt`) |
| `ResembleAI/Chatterbox-Multilingual-hi` → `t3_hi.safetensors` + `s3gen_v3.safetensors` | 2.14 + 1.06 GB | Hindi pack |
| `openbmb/VoxCPM2` → `model.safetensors` + `audiovae.pth` | 4.58 + 0.38 GB | TR/EN trial (new venv `.venv-vox`, torch cu124 wheel ~2.5 GB unless it reuses the cache) |
| faster-whisper `large-v3-turbo` | ~1.6 GB | CER scorer |
| SpeechBrain ECAPA + UTMOSv2 + DNSMOS | ~0.1 GB + a few hundred MB + < 10 MB | scorer |
| optional `ai4bharat/IndicF5` (gated) | ~1.4 GB | 2nd local HI candidate |
Total for the core trial is ~11 GB (~13 GB with the scorers).
Cloud trials need no download: ElevenLabs Starter is $1 for the first month (IVC), Gemini needs a paid-tier key
(cents).

### 4d. A/B bake-off (one evening, the creator listens blind)
Lines: take 3 lines per language from the next episode's script/dubs:
1. **Plain explanation**: an everyday-example sentence with a question ("Peki neden bekliyoruz?"). Tests natural delivery and breathing.
2. **Term-dense**: "GPIO 2'yi çıkış yapıyoruz; millis() ile tam 214 milisaniye ölçüyoruz." Tests terms and numbers.
3. **OLED + Preferences**: "Ayarı Preferences ile hafızaya yazıyoruz, OLED ekranda da görüyoruz." Tests mixed-language words.
(Write HI and EN versions in the same spirit, with the Devanagari respelling for HI.)

Engines (each one best-of-4 picked by `take_score.py`, so the creator hears every engine at its best):
| EN | TR | HI |
|---|---|---|
| A Chatterbox EN (now) | A Chatterbox V2 (now) | A Chatterbox V2 (now) |
| B VoxCPM2 | B Chatterbox V3 + lexicon | B Chatterbox V3 + lexicon, cfg 0.3 |
| C ElevenLabs v4 IVC | C VoxCPM2 + lexicon | C Chatterbox Multilingual-hi |
| D Gemini 3.8 Flash TTS | D ElevenLabs v4 IVC | D ElevenLabs v4 IVC |
| | E Gemini 3.8 Flash TTS | E Gemini 3.8 Flash TTS |
| | | F (optional) Cartesia Sonic-3.6 or IndicF5 |

Output goes to `build/voice_test/bakeoff/<lang>_<letter>_<line>.wav`, loudness-matched (-18 LUFS, same POLISH and
DeepFilterNet chain), with letters shuffled per language and the key kept in a separate file. The creator rates
each one 1-5 on (a) sounds like me, (b) native accent, (c) terms right, (d) natural, and picks a winner per language.
For HI, ask one native listener if possible, because the creator cannot judge Hindi accent. The automatic scores
(section 3) go next to the ratings, so the gates can be calibrated against his ears.
