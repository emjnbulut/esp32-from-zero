# YouTube upload — Episode 1

## Title
ESP32 From Zero #1 — Setting Up Arduino IDE, Drivers & Your First Program

## Description
Learn the ESP32 from absolutely zero! In this first episode we install the Arduino IDE, add ESP32 support, fix the USB driver, and upload our very first C program to the board. If you know a little C (variables, if, loops), you're ready.

🔗 Links from the video
• Arduino IDE: https://www.arduino.cc/en/software
• ESP32 boards manager URL (copy this):
  https://espressif.github.io/arduino-esp32/package_esp32_index.json
• CP2102 driver (Silicon Labs): https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers
• CH340 driver (WCH): https://www.wch-ic.com/downloads/CH341SER_EXE.html
• All code + written lesson: https://github.com/emjnbulut/esp32-from-zero

⏱ Chapters
0:00 Intro
0:34 What is an ESP32?
1:19 Install the Arduino IDE
2:18 Arduino IDE tour
3:05 Where is main()?
3:28 Add ESP32 support
4:17 Know your board & USB chip
5:26 USB driver & COM port
6:27 Select board and port
6:53 Our first program
7:54 Upload
8:32 Serial Monitor
9:11 Troubleshooting

🎵 Music: "Lobby Time" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
🎙 Narration: Chatterbox TTS (Resemble AI, MIT). Voice references: LibriVox (public domain) and FLEURS by Google (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/

#ESP32 #Arduino #Microcontroller #Electronics #CProgramming #IoT

## Subtitles + translated titles (automatic)
After the video is up (any privacy), run from the repo root:

    python tools/publish.py video/ep01 <VIDEO_ID>

It uploads every `build/ep01_<lang>.srt` (en, tr, hi, pt, es, id, ar, ru, de, fr, vi, ja)
and the titles/descriptions in `localize.json`. One-time setup: see tools/publish.py.

## Dubbed audio tracks (by hand)
YouTube Studio → video → **Languages** → *Add language* → **Audio track**, upload:
- Turkish: `build/dub_tr.m4a`
- Hindi: `build/dub_hi.m4a`
- Portuguese (Brazil): `build/dub_pt.m4a`
- Spanish (Latin America): `build/dub_es.m4a`

If audio tracks are not available on the channel, upload `build/ep01_<lang>_dub.mp4` as separate videos instead.
