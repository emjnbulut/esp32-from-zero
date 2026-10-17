# YouTube Shorts — Episode 2 summary (EN + TR)

Files: `build/en/ep02_short_en.mp4`, `build/tr/ep02_short_tr.mp4` (1080x1920, ~64 s).
On-screen text is English in both; the Turkish one has Turkish narration.

## English

### Title
Don't fry your ESP32! The pins to know + your first circuit ⚡ #esp32 #arduino

### Description
Before you plug anything into an ESP32: the power pins, two safety rules, the pins to leave alone, how a breadboard connects, and a first LED circuit — no code needed.
Full episode: (link the long video)
🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Electronics #Breadboard #Shorts

## Türkçe

### Başlık
ESP32'nizi yakmayın! Bilmeniz gereken pinler + ilk devre ⚡ #esp32 #arduino

### Açıklama
ESP32'ye bir şey takmadan önce: güç pinleri, iki güvenlik kuralı, dokunulmaması gereken pinler, breadboard'un nasıl bağlandığı ve kodsuz ilk LED devresi.
Bölümün tamamı: (uzun videonun linki)
🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Elektronik #Breadboard #Shorts

## Related video
YouTube Studio → Short → Details → **Related video** → select "ESP32 From Zero #2".

## After the creator clips are filmed
Scene h7 ("It lights up!") should use the real C3 footage: once `footage/ep02/C3.mp4` exists and
`build.py video/ep02 compose` has run, point `source` in short.json to `video/ep02/build/ep02_final.mp4`
(add 3.5 s to every `src`, the intro) or crop the clip region, and rebuild both Shorts.
