"""Episode 6 metadata: regenerate after the final schedule.
When no schedule exists, chapter times are provisional EN-based estimates.
"""
import json,sys
from pathlib import Path
here=Path(__file__).parent
root=here.parent.parent
sys.path.insert(0,str(root/'tools'))
import bumpers
chapters=json.loads((here/'chapters.json').read_text(encoding='utf-8'))
script=json.loads((here/'script.json').read_text(encoding='utf-8'))
schedule=here/'build/schedule.json'
provisional=not schedule.exists()
if provisional:
    audio=here/'build/audio/timings.json'
    timings=json.loads(audio.read_text(encoding='utf-8')) if audio.exists() else {}
    t=script.get('lead_in',0.8);segs={}
    for s in script['segments']:
        d=timings.get(s['id'],{}).get('duration',len(s['text'].split())/2.5)
        segs[s['id']]={'start':t,'end':t+d}
        t+=d+0.45+s.get('pad',0)
    tc=segs['s03']['start']-0.1
else:
    segs=json.loads(schedule.read_text(encoding='utf-8'))['segments']
    tc=bumpers.cut(here)
starts=[0]+[int(bumpers.shift(segs[c]['start'],tc)) for c in chapters[1:]]
assert all(b-a>=10 for a,b in zip(starts,starts[1:])), 'YouTube chapters must be >= 10 seconds'
times=['%d:%02d'%divmod(v,60) for v in starts]
T={
 "en": [
  "Mix RGB Colors with One Button | ESP32 From Zero #6",
  "Make eight colors with one RGB LED, then choose colors and a smooth fade with a button. Learn setColor(), common cathode and common anode, a mode counter and ground-wire troubleshooting. Your challenge: a smart camping headlamp.",
  [
   "One LED, your colors",
   "Recall: PWM and the loop",
   "Three LEDs in one",
   "Wire RGB safely",
   "The setColor() helper",
   "rgb_colors code tour",
   "Common ground mistake",
   "A button and four modes",
   "color_modes code tour",
   "Your turn: camping headlamp",
   "Recap and next lesson"
  ]
 ],
 "tr": [
  "Tek Butonla RGB Renkleri Kar\u0131\u015ft\u0131r | ESP32 From Zero #6",
  "Bir RGB LED ile sekiz renk \u00fcretin, ard\u0131ndan bir butonla renk ve yumu\u015fak ge\u00e7i\u015f se\u00e7in. setColor(), ortak katot ve anot, mod sayac\u0131 ve toprak kablosuyla hata bulmay\u0131 \u00f6\u011frenin. G\u00f6reviniz: ak\u0131ll\u0131 kamp kafa lambas\u0131.",
  [
   "Tek LED, istedi\u011finiz renkler",
   "Hat\u0131rlatma: PWM ve d\u00f6ng\u00fc",
   "Tek pakette \u00fc\u00e7 LED",
   "RGB ba\u011flant\u0131s\u0131",
   "setColor() yard\u0131mc\u0131s\u0131",
   "rgb_colors kod turu",
   "Ortak toprak kablosu hatas\u0131",
   "Bir buton, d\u00f6rt mod",
   "color_modes kod turu",
   "S\u0131ra sizde: kamp kafa lambas\u0131",
   "\u00d6zet ve sonraki ders"
  ]
 ],
 "hi": [
  "\u090f\u0915 \u092c\u091f\u0928 \u0938\u0947 RGB \u0930\u0902\u0917 \u092e\u093f\u0932\u093e\u090f\u0901 | ESP32 From Zero #6",
  "\u090f\u0915 RGB LED \u0938\u0947 \u0906\u0920 \u0930\u0902\u0917 \u092c\u0928\u093e\u090f\u0901 \u0914\u0930 \u092c\u091f\u0928 \u0938\u0947 \u0930\u0902\u0917 \u092f\u093e \u0927\u0940\u092e\u093e \u092c\u0926\u0932\u093e\u0935 \u091a\u0941\u0928\u0947\u0902\u0964 setColor(), \u0915\u0949\u092e\u0928 \u0915\u0948\u0925\u094b\u0921 \u0914\u0930 \u090f\u0928\u094b\u0921, \u092e\u094b\u0921 \u0915\u093e\u0909\u0902\u091f\u0930 \u0914\u0930 \u0917\u094d\u0930\u093e\u0909\u0902\u0921 \u0924\u093e\u0930 \u0915\u0940 \u091c\u093e\u0901\u091a \u0938\u0940\u0916\u0947\u0902\u0964 \u091a\u0941\u0928\u094c\u0924\u0940: \u0938\u094d\u092e\u093e\u0930\u094d\u091f \u0915\u0948\u0902\u092a\u093f\u0902\u0917 \u0939\u0947\u0921\u0932\u0948\u092e\u094d\u092a\u0964",
  [
   "\u090f\u0915 LED, \u0906\u092a\u0915\u0947 \u0930\u0902\u0917",
   "\u0926\u094b\u0939\u0930\u093e\u0935: PWM \u0914\u0930 loop",
   "\u090f\u0915 \u092a\u0948\u0915\u0947\u091c \u092e\u0947\u0902 \u0924\u0940\u0928 LED",
   "RGB \u0915\u0940 \u0935\u093e\u092f\u0930\u093f\u0902\u0917",
   "setColor() \u0938\u0939\u093e\u092f\u0915",
   "rgb_colors \u0915\u094b\u0921",
   "\u0938\u093e\u091d\u093e \u0917\u094d\u0930\u093e\u0909\u0902\u0921 \u0915\u0940 \u0917\u0932\u0924\u0940",
   "\u090f\u0915 \u092c\u091f\u0928, \u091a\u093e\u0930 \u092e\u094b\u0921",
   "color_modes \u0915\u094b\u0921",
   "\u0906\u092a\u0915\u0940 \u092c\u093e\u0930\u0940: \u0939\u0947\u0921\u0932\u0948\u092e\u094d\u092a",
   "\u0938\u093e\u0930\u093e\u0902\u0936 \u0914\u0930 \u0905\u0917\u0932\u093e \u092a\u093e\u0920"
  ]
 ],
 "pt": [
  "Misture Cores RGB com Um Bot\u00e3o | ESP32 From Zero #6",
  "Mostre oito cores com um LED RGB e escolha cores ou uma transi\u00e7\u00e3o suave com um bot\u00e3o. Aprenda setColor(), c\u00e1todo e \u00e2nodo comum, contador de modos e diagn\u00f3stico do fio de terra. Desafio: uma lanterna de cabe\u00e7a inteligente.",
  [
   "Um LED, suas cores",
   "Revis\u00e3o: PWM e loop",
   "Tr\u00eas LEDs em um",
   "Liga\u00e7\u00e3o do RGB",
   "A fun\u00e7\u00e3o setColor()",
   "C\u00f3digo rgb_colors",
   "Falha no terra comum",
   "Um bot\u00e3o, quatro modos",
   "C\u00f3digo color_modes",
   "Sua vez: lanterna de cabe\u00e7a",
   "Resumo e pr\u00f3xima aula"
  ]
 ],
 "es": [
  "Mezcla Colores RGB con Un Bot\u00f3n | ESP32 From Zero #6",
  "Muestra ocho colores con un LED RGB y elige colores o una transici\u00f3n suave con un bot\u00f3n. Aprende setColor(), c\u00e1todo y \u00e1nodo com\u00fan, contador de modos y diagn\u00f3stico de tierra. Reto: una linterna frontal inteligente.",
  [
   "Un LED, tus colores",
   "Repaso: PWM y loop",
   "Tres LED en uno",
   "Conexi\u00f3n del RGB",
   "La funci\u00f3n setColor()",
   "C\u00f3digo rgb_colors",
   "Falla de tierra com\u00fan",
   "Un bot\u00f3n, cuatro modos",
   "C\u00f3digo color_modes",
   "Tu turno: linterna frontal",
   "Resumen y pr\u00f3xima lecci\u00f3n"
  ]
 ],
 "de": [
  "RGB-Farben mit einem Taster mischen | ESP32 From Zero #6",
  "Erzeuge acht Farben mit einer RGB-LED und w\u00e4hle Farben oder einen sanften \u00dcbergang per Taster. Lerne setColor(), gemeinsame Kathode und Anode, Modusz\u00e4hler und Massefehler kennen. Aufgabe: eine intelligente Stirnlampe.",
  [
   "Eine LED, deine Farben",
   "R\u00fcckblick: PWM und loop",
   "Drei LEDs in einer",
   "RGB anschlie\u00dfen",
   "Die Funktion setColor()",
   "rgb_colors erkl\u00e4rt",
   "Fehler am Massekabel",
   "Ein Taster, vier Modi",
   "color_modes erkl\u00e4rt",
   "Deine Aufgabe: Stirnlampe",
   "R\u00fcckblick und n\u00e4chste Lektion"
  ]
 ],
 "fr": [
  "M\u00e9langer les couleurs RGB avec un bouton | ESP32 From Zero #6",
  "Affichez huit couleurs avec une LED RGB et choisissez couleurs ou fondu avec un bouton. D\u00e9couvrez setColor(), cathode et anode communes, compteur de modes et d\u00e9pannage de la masse. D\u00e9fi : une lampe frontale intelligente.",
  [
   "Une LED, vos couleurs",
   "Rappel : PWM et loop",
   "Trois LED en une",
   "Brancher la LED RGB",
   "La fonction setColor()",
   "Le code rgb_colors",
   "Erreur de masse commune",
   "Un bouton, quatre modes",
   "Le code color_modes",
   "\u00c0 vous : lampe frontale",
   "Bilan et prochain cours"
  ]
 ],
 "ar": [
  "\u0645\u0632\u062c \u0623\u0644\u0648\u0627\u0646 RGB \u0628\u0632\u0631 \u0648\u0627\u062d\u062f | ESP32 From Zero #6",
  "\u0627\u0639\u0631\u0636 \u062b\u0645\u0627\u0646\u064a\u0629 \u0623\u0644\u0648\u0627\u0646 \u0628\u0627\u0633\u062a\u062e\u062f\u0627\u0645 LED \u0645\u0646 \u0646\u0648\u0639 RGB\u060c \u062b\u0645 \u0627\u062e\u062a\u0631 \u0627\u0644\u0623\u0644\u0648\u0627\u0646 \u0623\u0648 \u0627\u0646\u062a\u0642\u0627\u0644\u0627\u064b \u0646\u0627\u0639\u0645\u0627\u064b \u0628\u0632\u0631 \u0648\u0627\u062d\u062f. \u062a\u0639\u0644\u0651\u0645 setColor() \u0648\u0627\u0644\u0643\u0627\u062b\u0648\u062f \u0648\u0627\u0644\u0623\u0646\u0648\u062f \u0627\u0644\u0645\u0634\u062a\u0631\u0643\u064a\u0646 \u0648\u0639\u062f\u0651\u0627\u062f \u0627\u0644\u0623\u0648\u0636\u0627\u0639 \u0648\u0641\u062d\u0635 \u0633\u0644\u0643 \u0627\u0644\u0623\u0631\u0636\u064a. \u0627\u0644\u062a\u062d\u062f\u064a: \u0645\u0635\u0628\u0627\u062d \u0631\u0623\u0633 \u0630\u0643\u064a \u0644\u0644\u062a\u062e\u064a\u064a\u0645.",
  [
   "LED \u0648\u0627\u062d\u062f \u0648\u0623\u0644\u0648\u0627\u0646\u0643",
   "\u0645\u0631\u0627\u062c\u0639\u0629 PWM \u0648\u0627\u0644\u062d\u0644\u0642\u0629",
   "\u062b\u0644\u0627\u062b\u0629 LEDs \u0641\u064a \u063a\u0644\u0627\u0641 \u0648\u0627\u062d\u062f",
   "\u062a\u0648\u0635\u064a\u0644 RGB",
   "\u0627\u0644\u062f\u0627\u0644\u0629 setColor()",
   "\u0634\u0631\u062d rgb_colors",
   "\u062e\u0637\u0623 \u0627\u0644\u0623\u0631\u0636\u064a \u0627\u0644\u0645\u0634\u062a\u0631\u0643",
   "\u0632\u0631 \u0648\u0627\u062d\u062f \u0648\u0623\u0631\u0628\u0639\u0629 \u0623\u0648\u0636\u0627\u0639",
   "\u0634\u0631\u062d color_modes",
   "\u062f\u0648\u0631\u0643: \u0645\u0635\u0628\u0627\u062d \u0631\u0623\u0633",
   "\u0645\u0644\u062e\u0635 \u0648\u0627\u0644\u062f\u0631\u0633 \u0627\u0644\u0642\u0627\u062f\u0645"
  ]
 ],
 "id": [
  "Campur Warna RGB dengan Satu Tombol | ESP32 From Zero #6",
  "Tampilkan delapan warna dengan LED RGB dan pilih warna atau transisi lembut lewat tombol. Pelajari setColor(), katode dan anode bersama, penghitung mode dan pemeriksaan kabel ground. Tantangan: lampu kepala pintar.",
  [
   "Satu LED, warna pilihanmu",
   "Ulasan: PWM dan loop",
   "Tiga LED dalam satu",
   "Merangkai RGB",
   "Fungsi setColor()",
   "Kode rgb_colors",
   "Kesalahan ground bersama",
   "Satu tombol, empat mode",
   "Kode color_modes",
   "Giliranmu: lampu kepala",
   "Ringkasan dan pelajaran berikut"
  ]
 ],
 "ja": [
  "\u30dc\u30bf\u30f31\u3064\u3067RGB\u306e\u8272\u3092\u6df7\u305c\u308b | ESP32 From Zero #6",
  "RGB LED\u30678\u8272\u3092\u4f5c\u308a\u3001\u30dc\u30bf\u30f3\u3067\u8272\u3084\u306a\u3081\u3089\u304b\u306a\u5909\u5316\u3092\u9078\u3073\u307e\u3059\u3002setColor()\u3001\u5171\u901a\u30ab\u30bd\u30fc\u30c9\u3068\u5171\u901a\u30a2\u30ce\u30fc\u30c9\u3001\u30e2\u30fc\u30c9\u30ab\u30a6\u30f3\u30bf\u30fc\u3001GND\u7dda\u306e\u8abf\u3079\u65b9\u3092\u5b66\u3073\u307e\u3059\u3002\u8ab2\u984c\u306f\u30b9\u30de\u30fc\u30c8\u306a\u30ad\u30e3\u30f3\u30d7\u7528\u30d8\u30c3\u30c9\u30e9\u30a4\u30c8\u3067\u3059\u3002",
  [
   "1\u3064\u306eLED\u3067\u597d\u304d\u306a\u8272",
   "\u5fa9\u7fd2\uff1aPWM\u3068loop",
   "1\u3064\u306e\u4e2d\u306b3\u3064\u306eLED",
   "RGB\u306e\u914d\u7dda",
   "setColor()\u95a2\u6570",
   "rgb_colors\u306e\u30b3\u30fc\u30c9",
   "\u5171\u901aGND\u7dda\u306e\u9593\u9055\u3044",
   "1\u3064\u306e\u30dc\u30bf\u30f3\u30684\u30e2\u30fc\u30c9",
   "color_modes\u306e\u30b3\u30fc\u30c9",
   "\u8ab2\u984c\uff1a\u30d8\u30c3\u30c9\u30e9\u30a4\u30c8",
   "\u307e\u3068\u3081\u3068\u6b21\u306e\u30ec\u30c3\u30b9\u30f3"
  ]
 ],
 "ru": [
  "\u0421\u043c\u0435\u0448\u0438\u0432\u0430\u0435\u043c \u0446\u0432\u0435\u0442\u0430 RGB \u043e\u0434\u043d\u043e\u0439 \u043a\u043d\u043e\u043f\u043a\u043e\u0439 | ESP32 From Zero #6",
  "\u0421\u043e\u0437\u0434\u0430\u0439\u0442\u0435 \u0432\u043e\u0441\u0435\u043c\u044c \u0446\u0432\u0435\u0442\u043e\u0432 \u0441 RGB-\u0441\u0432\u0435\u0442\u043e\u0434\u0438\u043e\u0434\u043e\u043c \u0438 \u0432\u044b\u0431\u0438\u0440\u0430\u0439\u0442\u0435 \u0446\u0432\u0435\u0442\u0430 \u0438\u043b\u0438 \u043f\u043b\u0430\u0432\u043d\u044b\u0439 \u043f\u0435\u0440\u0435\u0445\u043e\u0434 \u043a\u043d\u043e\u043f\u043a\u043e\u0439. \u0418\u0437\u0443\u0447\u0438\u0442\u0435 setColor(), \u043e\u0431\u0449\u0438\u0439 \u043a\u0430\u0442\u043e\u0434 \u0438 \u0430\u043d\u043e\u0434, \u0441\u0447\u0451\u0442\u0447\u0438\u043a \u0440\u0435\u0436\u0438\u043c\u043e\u0432 \u0438 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443 \u0437\u0435\u043c\u043b\u0438. \u0417\u0430\u0434\u0430\u043d\u0438\u0435: \u0443\u043c\u043d\u044b\u0439 \u043d\u0430\u043b\u043e\u0431\u043d\u044b\u0439 \u0444\u043e\u043d\u0430\u0440\u044c.",
  [
   "\u041e\u0434\u0438\u043d \u0441\u0432\u0435\u0442\u043e\u0434\u0438\u043e\u0434, \u0432\u0430\u0448\u0438 \u0446\u0432\u0435\u0442\u0430",
   "\u041f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u0435: PWM \u0438 loop",
   "\u0422\u0440\u0438 \u0441\u0432\u0435\u0442\u043e\u0434\u0438\u043e\u0434\u0430 \u0432 \u043e\u0434\u043d\u043e\u043c",
   "\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 RGB",
   "\u0424\u0443\u043d\u043a\u0446\u0438\u044f setColor()",
   "\u0420\u0430\u0437\u0431\u043e\u0440 rgb_colors",
   "\u041e\u0448\u0438\u0431\u043a\u0430 \u043e\u0431\u0449\u0435\u0439 \u0437\u0435\u043c\u043b\u0438",
   "\u041a\u043d\u043e\u043f\u043a\u0430 \u0438 \u0447\u0435\u0442\u044b\u0440\u0435 \u0440\u0435\u0436\u0438\u043c\u0430",
   "\u0420\u0430\u0437\u0431\u043e\u0440 color_modes",
   "\u0412\u0430\u0448\u0435 \u0437\u0430\u0434\u0430\u043d\u0438\u0435: \u043d\u0430\u043b\u043e\u0431\u043d\u044b\u0439 \u0444\u043e\u043d\u0430\u0440\u044c",
   "\u0418\u0442\u043e\u0433\u0438 \u0438 \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0438\u0439 \u0443\u0440\u043e\u043a"
  ]
 ],
 "vi": [
  "Tr\u1ed9n m\u00e0u RGB b\u1eb1ng m\u1ed9t n\u00fat nh\u1ea5n | ESP32 From Zero #6",
  "Hi\u1ec3n th\u1ecb t\u00e1m m\u00e0u b\u1eb1ng LED RGB v\u00e0 d\u00f9ng n\u00fat nh\u1ea5n ch\u1ecdn m\u00e0u ho\u1eb7c chuy\u1ec3n m\u00e0u nh\u1eb9. H\u1ecdc setColor(), cathode v\u00e0 anode chung, b\u1ed9 \u0111\u1ebfm ch\u1ebf \u0111\u1ed9 v\u00e0 c\u00e1ch ki\u1ec3m tra d\u00e2y GND. Th\u1eed th\u00e1ch: \u0111\u00e8n \u0111\u1ed9i \u0111\u1ea7u th\u00f4ng minh.",
  [
   "M\u1ed9t LED, nhi\u1ec1u m\u00e0u",
   "\u00d4n t\u1eadp: PWM v\u00e0 loop",
   "Ba LED trong m\u1ed9t",
   "N\u1ed1i d\u00e2y RGB",
   "H\u00e0m setColor()",
   "M\u00e3 rgb_colors",
   "L\u1ed7i d\u00e2y GND chung",
   "M\u1ed9t n\u00fat, b\u1ed1n ch\u1ebf \u0111\u1ed9",
   "M\u00e3 color_modes",
   "\u0110\u1ebfn l\u01b0\u1ee3t b\u1ea1n: \u0111\u00e8n \u0111\u1ed9i \u0111\u1ea7u",
   "T\u00f3m t\u1eaft v\u00e0 b\u00e0i ti\u1ebfp theo"
  ]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nCode + lesson: '+repo+'/tree/main/lessons/06-rgb\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), creator-authorized voice reference. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n#ESP32 #Arduino #RGBLED #PWM #Electronics'
loc={}
for lang,(title,intro,names) in T.items():
    assert len(names)==len(times),(lang,len(names))
    assert len(title)<=100,(lang,len(title))
    loc[lang]={'title':title,'description':intro+links+'\n\n'+'\n'.join(t+' '+n for t,n in zip(times,names))+credit}
(here/'localize.json').write_text(json.dumps(loc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
md='# Episode 6 - RGB Color Mixing\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Release target: 6 November 2026, 17:00 Turkey time. Category: Education. Original language: English.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Upload checklist\n\n- Final EN video, four separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('ep06 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
