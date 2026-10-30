# YouTube upload - Episode 5: PWM

Release: 3 November 2026, 17:00 Europe/Istanbul.
Thumbnail: video/thumbs/build/ep05_A.png (breathing red LED).

## Title
ESP32 PWM: Make an LED Breathe with analogWrite() and millis() | From Zero #5

## Description
Make an LED fade smoothly and pause it instantly with a button. Learn PWM, duty cycle, analogWrite(), average voltage and a fade that uses millis() without missing a press.

https://github.com/emjnbulut/esp32-from-zero/tree/main/lessons/05-pwm
https://github.com/emjnbulut/esp32-from-zero
https://emjnbulut.github.io/esp32-learning-lab/

0:00 A breathing LED
0:33 Two questions to remember
1:26 PWM: only on or off
2:35 Duty cycle
3:14 analogWrite(): 0 to 255
3:52 Code tour: pwm_levels
5:07 Check with a multimeter
5:41 The fade that misses the button
6:39 The clock-based fix
7:08 Code tour: fade_millis and result
9:03 Explain, recap and next lesson

Music: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
Narration: Chatterbox TTS (Resemble AI, MIT), with the creator's own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0).

#ESP32 #Arduino #PWM #LED #millis

## Creator clips
- C0: OPENING, full screen, 12-15 s: fade_millis; the red LED breathes; one press stops it at once, a second press 2 s later resumes it. Red LED and button centred.
- C1: MULTIMETER, hands-free, 10-12 s: pwm_levels; probes on the red LED's GPIO 23 strip and the minus rail (DC volts). The display steps 0 -> ~0.8 -> ~1.65 -> ~3.3 V, 2 s each.
- C2: pwm_levels, 10 s: the LED in four steps: off, 25 %, 50 %, 100 %. Slightly dim room.
- C3: COMMON MISTAKE, 10-12 s: fade_naive; 3-4 short presses while it breathes; the fade does not stop.
- C4: fade_millis, 10 s, closer than C0: a press pauses it mid-fade, another press resumes it.
- C5: MODIFY, optional, 8 s: fade_millis with line 39 changed from 4 to 10; a visibly slower breath.

## Upload checklist

- Final file: build/ep05_final.mp4; review audio, code, and real footage before upload.
- Set video language to English and category to Education.
- Set the end screen in the last 20 seconds and verify it after saving.
- Upload the 12 SRT files and the 12 metadata entries from localize.json.
- Add TR/HI/PT/ES audio after checking the four build/dub_*.m4a files.
- Check language availability in YouTube Studio; local files do not prove publication.
- Shorts: TR 4 Nov 17:00; EN 5 Nov 22:00. Set each Related video to this episode.
- Own-voice clone: follow the disclosure preference in PRODUCTION_GUIDELINES.md.
