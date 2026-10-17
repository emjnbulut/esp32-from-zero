# YouTube Shorts — Episode 3 summary (EN + TR)

Files: `build/en/ep03_short_en.mp4`, `build/tr/ep03_short_tr.mp4` (1080x1920). Preview (edge-tts, 2026-10-17) was 64 s; text trimmed since, aim < 60 s.
On-screen text is English in both; the Turkish one has Turkish narration.
Shots are anchored to words of the episode narration (`"at"` in short.json), so after the episode is
re-narrated (Chatterbox) and re-rendered, just rebuild: `python tools/short.py video/shorts/ep03 en` (and `tr`).

## English

### Title
Blink an LED with an ESP32: one wire + a few lines of code 💡 #esp32 #arduino

### Description
Why the LED needs a 220 Ω resistor, moving one wire to GPIO 23, and the Blink code: pinMode, digitalWrite and delay.
Full episode: (link the long video)
🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Electronics #LED #Shorts

## Türkçe

### Başlık
ESP32 ile LED yakıp söndürme: bir kablo + birkaç satır kod 💡 #esp32 #arduino

### Açıklama
LED'in neden 220 Ω dirence ihtiyaç duyduğu, bir kabloyu GPIO 23'e taşımak ve Blink kodu: pinMode, digitalWrite ve delay.
Bölümün tamamı: (uzun videonun linki)
🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Elektronik #LED #Shorts

## Related video
YouTube Studio → Short → Details → **Related video** → select "ESP32 From Zero #3".

## After the creator clips are filmed
Scene h6 ("It blinks!") would be stronger with the real C2 footage (LED blinking on the desk): once
`footage/ep03/C2.mp4` exists, add it as a shot (crop the clip region of `ep03_final.mp4`, or point a shot
at the clip file) and rebuild both Shorts.
