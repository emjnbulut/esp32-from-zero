"""Episode 7 metadata: regenerate after the final schedule.
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
# Titles lead with the search term (channel analytics, 3 Nov 2026); every title ends with the series tag.
TAG=' | ESP32 From Zero #7'
TITLES={
 "en":"ESP32 Potentiometer: Read Any Knob with analogRead()",
 "tr":"ESP32 Potansiyometre: analogRead() ile Düğme Okuma",
 "hi":"ESP32 Potentiometer: analogRead() से कोई भी knob पढ़ें",
 "pt":"ESP32 Potenciômetro: Leia Qualquer Knob com analogRead()",
 "es":"ESP32 Potenciómetro: Lee Cualquier Perilla con analogRead()",
 "de":"ESP32 Potentiometer: Jeden Drehknopf mit analogRead() lesen",
 "fr":"ESP32 Potentiomètre : lire n'importe quel bouton avec analogRead()",
 "ar":"ESP32 مقياس الجهد: اقرأ أي مقبض بـ analogRead()",
 "id":"ESP32 Potensiometer: Baca Knob Apa Pun dengan analogRead()",
 "ja":"ESP32 ポテンショメーター：analogRead()でつまみを読む",
 "ru":"ESP32 потенциометр: считываем любую ручку через analogRead()",
 "vi":"ESP32 biến trở: đọc mọi núm xoay bằng analogRead()",
}
T={
 "en": [
  "Read a knob with analogRead(), dim an LED with it, split it into three zones, calm the reading by averaging, debug by printing first, and learn the ESP32 pin rules. Your challenge: Knob Blink Speed.",
  ["A knob controls an LED","Recall: color and the shared wire","The knob as a slide","Wiring the knob","The analogRead() function","pot_read code tour","Dimming an LED: pot_dimmer","Three zones: pot_zones","A calmer reading","Debugging: print first","ESP32 pin rules","Your turn: Knob Blink Speed","Recap and next lesson"]
 ],
 "tr": [
  "Düğmeyi analogRead() ile okuyun, LED'i kısın, değeri üç bölgeye ayırın, ortalamayla okumayı sakinleştirin, önce yazdırarak hata bulun ve ESP32 pin kurallarını öğrenin. Göreviniz: Knob Blink Speed.",
  ["Düğme LED'i yönetiyor","Hatırlatma: renk ve ortak kablo","Düğme bir kaydırak gibi","Düğmenin bağlantısı","analogRead() fonksiyonu","pot_read kod turu","LED'i kısmak: pot_dimmer","Üç bölge: pot_zones","Daha sakin okuma","Hata bulma: önce yazdır","ESP32 pin kuralları","Sıra sizde: Knob Blink Speed","Özet ve sonraki ders"]
 ],
 "hi": [
  "analogRead() से knob पढ़ें, LED को धीमा करें, मान को तीन हिस्सों में बाँटें, औसत से रीडिंग शांत करें, पहले print करके गड़बड़ी ढूँढें और ESP32 के pin नियम सीखें। चुनौती: Knob Blink Speed।",
  ["knob से LED","दोहराव: रंग और साझा तार","knob एक फिसलपट्टी","knob की वायरिंग","analogRead() फ़ंक्शन","pot_read कोड","LED धीमी: pot_dimmer","तीन हिस्से: pot_zones","शांत रीडिंग","पहले print करें","ESP32 pin नियम","आपकी बारी: Knob Blink Speed","सारांश और अगला पाठ"]
 ],
 "pt": [
  "Leia um knob com analogRead(), escureça um LED, divida em três zonas, acalme a leitura com média, depure imprimindo primeiro e aprenda as regras de pinos do ESP32. Desafio: Knob Blink Speed.",
  ["Um knob controla um LED","Revisão: cor e fio comum","O knob como escorregador","Ligação do knob","A função analogRead()","Código pot_read","Dimmer: pot_dimmer","Três zonas: pot_zones","Leitura mais calma","Depuração: imprima primeiro","Regras de pinos do ESP32","Sua vez: Knob Blink Speed","Resumo e próxima aula"]
 ],
 "es": [
  "Lee una perilla con analogRead(), atenúa un LED, divídela en tres zonas, calma la lectura con un promedio, depura imprimiendo primero y aprende las reglas de pines del ESP32. Reto: Knob Blink Speed.",
  ["Una perilla controla un LED","Repaso: color y cable común","La perilla como tobogán","Conexión de la perilla","La función analogRead()","Código pot_read","Atenuar un LED: pot_dimmer","Tres zonas: pot_zones","Una lectura más calmada","Depurar: imprime primero","Reglas de pines del ESP32","Tu turno: Knob Blink Speed","Resumen y próxima lección"]
 ],
 "de": [
  "Lies einen Drehknopf mit analogRead(), dimme eine LED, teile den Wert in drei Zonen, beruhige die Messung per Mittelwert, suche Fehler durch Ausgeben und lerne die ESP32-Pin-Regeln. Aufgabe: Knob Blink Speed.",
  ["Ein Knopf steuert eine LED","Rückblick: Farbe und gemeinsames Kabel","Der Knopf als Rutsche","Den Knopf anschließen","Die Funktion analogRead()","pot_read erklärt","LED dimmen: pot_dimmer","Drei Zonen: pot_zones","Ruhigerer Messwert","Fehlersuche: erst ausgeben","ESP32-Pin-Regeln","Deine Aufgabe: Knob Blink Speed","Rückblick und nächste Lektion"]
 ],
 "fr": [
  "Lisez un bouton avec analogRead(), faites varier une LED, découpez la valeur en trois zones, calmez la mesure par une moyenne, dépannez en affichant d'abord et apprenez les règles de broches de l'ESP32. Défi : Knob Blink Speed.",
  ["Un bouton commande une LED","Rappel : couleur et fil commun","Le bouton comme un toboggan","Brancher le bouton","La fonction analogRead()","Le code pot_read","Varier la LED : pot_dimmer","Trois zones : pot_zones","Une mesure plus calme","Dépannage : afficher d'abord","Règles des broches ESP32","À vous : Knob Blink Speed","Bilan et prochain cours"]
 ],
 "ar": [
  "اقرأ مقبضاً بـ analogRead()، وخفّت إضاءة LED، وقسّم القيمة إلى ثلاث مناطق، وهدّئ القراءة بالمتوسط، وصحّح الأخطاء بالطباعة أولاً، وتعلّم قواعد أطراف ESP32. التحدي: Knob Blink Speed.",
  ["مقبض يتحكم في LED","مراجعة: اللون والسلك المشترك","المقبض كزحليقة","توصيل المقبض","الدالة analogRead()","شرح pot_read","تخفيت LED: pot_dimmer","ثلاث مناطق: pot_zones","قراءة أهدأ","التصحيح: اطبع أولاً","قواعد أطراف ESP32","دورك: Knob Blink Speed","ملخص والدرس القادم"]
 ],
 "id": [
  "Baca knob dengan analogRead(), redupkan LED, bagi nilainya menjadi tiga zona, tenangkan pembacaan dengan rata-rata, cari masalah dengan mencetak dulu, dan pelajari aturan pin ESP32. Tantangan: Knob Blink Speed.",
  ["Knob mengatur LED","Ulasan: warna dan kabel bersama","Knob seperti perosotan","Merangkai knob","Fungsi analogRead()","Kode pot_read","Meredupkan LED: pot_dimmer","Tiga zona: pot_zones","Pembacaan lebih tenang","Debug: cetak dulu","Aturan pin ESP32","Giliranmu: Knob Blink Speed","Ringkasan dan pelajaran berikut"]
 ],
 "ja": [
  "analogRead()でつまみを読み、LEDを調光し、値を3つのゾーンに分け、平均で読み取りを安定させ、まず表示してから原因を探し、ESP32のピンのルールを学びます。課題：Knob Blink Speed。",
  ["つまみでLEDを操作","復習：色と共通の線","滑り台としてのつまみ","つまみの配線","analogRead()関数","pot_readのコード","LEDの調光：pot_dimmer","3つのゾーン：pot_zones","より安定した読み取り","デバッグ：まず表示","ESP32のピンのルール","課題：Knob Blink Speed","まとめと次のレッスン"]
 ],
 "ru": [
  "Считайте ручку через analogRead(), приглушите светодиод, разделите значение на три зоны, успокойте показания усреднением, ищите ошибки сначала печатью и узнайте правила выводов ESP32. Задание: Knob Blink Speed.",
  ["Ручка управляет светодиодом","Повторение: цвет и общий провод","Ручка как горка","Подключение ручки","Функция analogRead()","Разбор pot_read","Диммер: pot_dimmer","Три зоны: pot_zones","Более спокойные показания","Отладка: сначала печать","Правила выводов ESP32","Ваше задание: Knob Blink Speed","Итоги и следующий урок"]
 ],
 "vi": [
  "Đọc núm xoay bằng analogRead(), làm mờ LED, chia giá trị thành ba vùng, làm êm số đọc bằng trung bình, gỡ lỗi bằng cách in trước và học các quy tắc chân của ESP32. Thử thách: Knob Blink Speed.",
  ["Núm xoay điều khiển LED","Ôn tập: màu và dây chung","Núm xoay như cầu trượt","Nối dây núm xoay","Hàm analogRead()","Mã pot_read","Làm mờ LED: pot_dimmer","Ba vùng: pot_zones","Số đọc êm hơn","Gỡ lỗi: in trước","Quy tắc chân ESP32","Đến lượt bạn: Knob Blink Speed","Tóm tắt và bài tiếp theo"]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nCode + lesson: '+repo+'/tree/main/lessons/07-analog-input\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n#ESP32 #Arduino #Potentiometer #analogRead #Electronics'
loc={}
for lang,(intro,names) in T.items():
    title=TITLES[lang]+TAG
    assert len(names)==len(times)==len(chapters),(lang,len(names))
    assert len(title)<=100,(lang,len(title))
    loc[lang]={'title':title,'description':intro+links+'\n\n'+'\n'.join(t+' '+n for t,n in zip(times,names))+credit}
assert set(loc)==set(TITLES)==set("en tr hi pt es de fr ar id ja ru vi".split())
(here/'localize.json').write_text(json.dumps(loc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
md='# Episode 7 - Potentiometer and analogRead()\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Original language: English. Category: Education.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Upload checklist\n\n- Final EN video, four separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('ep07 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
