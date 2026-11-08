"""Episode 8 metadata: regenerate after the final schedule.
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
TAG=' | ESP32 From Zero #8'
TITLES={
 "en":"ESP32 map() Function: Knob Dimmer and LED Level Bar",
 "tr":"ESP32 map() Fonksiyonu: Düğmeyle Dimmer ve LED Seviye Çubuğu",
 "hi":"ESP32 map() फ़ंक्शन: knob dimmer और LED level bar",
 "pt":"ESP32 Função map(): Dimmer com Knob e Barra de Nível de LEDs",
 "es":"ESP32 Función map(): Dimmer con Perilla y Barra de Nivel LED",
 "de":"ESP32 map()-Funktion: Dreh-Dimmer und LED-Pegelanzeige",
 "fr":"ESP32 Fonction map() : variateur à bouton et jauge de LED",
 "ar":"ESP32 الدالة map(): خافت بمقبض ومؤشر مستوى LED",
 "id":"ESP32 Fungsi map(): Dimmer Knob dan Bar Level LED",
 "ja":"ESP32 map()関数：つまみ調光とLEDレベルバー",
 "ru":"ESP32 функция map(): диммер на ручке и шкала уровня из LED",
 "vi":"ESP32 hàm map(): dimmer núm xoay và thanh mức LED",
}
T={
 "en": [
  "Turn one range of numbers into another with map(): a clearer knob dimmer, a knob that works backwards, and a 3-LED level bar that fills up like a volume meter. Plus why map() rounds down, the common backwards-LED mistake, and your challenge: the Rotary Safe Lock.",
  ["The bar fills up","Recall: the knob and printing first","The idea: a city map","The map() line, slot by slot","map_dimmer code tour","Flip the range","A level bar like battery bars","Wiring the yellow and green LEDs","The level trap: map() rounds down","level_bar code tour","Common mistake: an LED in backwards","Your turn: Rotary Safe Lock","Recap and next lesson"]
 ],
 "tr": [
  "map() ile bir sayı aralığını başka bir aralığa çevirin: daha anlaşılır bir düğme dimmer'ı, ters çalışan bir düğme ve ses göstergesi gibi dolan 3 LED'li bir seviye çubuğu. Ayrıca map()'in neden aşağı yuvarladığı, ters takılan LED hatası ve göreviniz: Döner Kasa Kilidi.",
  ["Çubuk doluyor","Hatırlatma: düğme ve önce yazdırmak","Fikir: bir şehir haritası","map() satırı, parça parça","map_dimmer kod turu","Aralığı ters çevirmek","Pil simgesi gibi bir seviye çubuğu","Sarı ve yeşil LED'in bağlantısı","Seviye tuzağı: map() aşağı yuvarlar","level_bar kod turu","Yaygın hata: ters takılan LED","Sıra sizde: Döner Kasa Kilidi","Özet ve sonraki ders"]
 ],
 "hi": [
  "map() से एक संख्या-सीमा को दूसरी में बदलें: ज़्यादा साफ़ knob dimmer, उलटा चलने वाला knob और volume meter की तरह भरने वाला 3-LED level bar। साथ में map() नीचे क्यों गोल करता है, उलटी लगी LED की आम गलती और आपकी चुनौती: Rotary Safe Lock।",
  ["बार भरता है","दोहराव: knob और पहले print","विचार: शहर का नक्शा","map() की लाइन, हिस्से-हिस्से","map_dimmer कोड","रेंज उलटना","बैटरी बार जैसा level bar","पीली और हरी LED की वायरिंग","level का जाल: map() नीचे गोल करता है","level_bar कोड","आम गलती: उलटी LED","आपकी बारी: Rotary Safe Lock","सारांश और अगला पाठ"]
 ],
 "pt": [
  "Transforme uma faixa de números em outra com map(): um dimmer com knob mais claro, um knob que funciona ao contrário e uma barra de nível de 3 LEDs que enche como um medidor de volume. Também por que o map() arredonda para baixo, o erro comum do LED invertido e seu desafio: Rotary Safe Lock.",
  ["A barra enche","Revisão: o knob e imprimir primeiro","A ideia: um mapa da cidade","A linha do map(), parte por parte","Código map_dimmer","Inverter a faixa","Barra de nível como a da bateria","Ligação dos LEDs amarelo e verde","A armadilha do nível: map() arredonda para baixo","Código level_bar","Erro comum: LED ao contrário","Sua vez: Rotary Safe Lock","Resumo e próxima aula"]
 ],
 "es": [
  "Convierte un rango de números en otro con map(): un dimmer con perilla más claro, una perilla que funciona al revés y una barra de nivel de 3 LED que se llena como un medidor de volumen. Además, por qué map() redondea hacia abajo, el error común del LED al revés y tu reto: Rotary Safe Lock.",
  ["La barra se llena","Repaso: la perilla e imprimir primero","La idea: un mapa de la ciudad","La línea de map(), pieza por pieza","Código map_dimmer","Invertir el rango","Una barra de nivel como la de la batería","Conexión de los LED amarillo y verde","La trampa del nivel: map() redondea hacia abajo","Código level_bar","Error común: un LED al revés","Tu turno: Rotary Safe Lock","Resumen y próxima lección"]
 ],
 "de": [
  "Wandle mit map() einen Zahlenbereich in einen anderen um: ein klarerer Dreh-Dimmer, ein Knopf, der rückwärts arbeitet, und eine 3-LED-Pegelanzeige, die sich wie ein Lautstärkemesser füllt. Dazu: warum map() abrundet, der typische Fehler mit der verkehrt herum eingesetzten LED und deine Aufgabe: Rotary Safe Lock.",
  ["Die Anzeige füllt sich","Rückblick: Knopf und erst ausgeben","Die Idee: ein Stadtplan","Die map()-Zeile, Teil für Teil","map_dimmer erklärt","Den Bereich umdrehen","Pegelanzeige wie bei der Batterie","Gelbe und grüne LED anschließen","Die Pegelfalle: map() rundet ab","level_bar erklärt","Häufiger Fehler: LED verkehrt herum","Deine Aufgabe: Rotary Safe Lock","Rückblick und nächste Lektion"]
 ],
 "fr": [
  "Convertissez une plage de nombres en une autre avec map() : un variateur à bouton plus clair, un bouton qui marche à l'envers et une jauge de 3 LED qui se remplit comme un indicateur de volume. Et aussi pourquoi map() arrondit vers le bas, l'erreur classique de la LED à l'envers et votre défi : Rotary Safe Lock.",
  ["La jauge se remplit","Rappel : le bouton et afficher d'abord","L'idée : un plan de ville","La ligne map(), morceau par morceau","Le code map_dimmer","Inverser la plage","Une jauge comme celle de la batterie","Brancher les LED jaune et verte","Le piège du niveau : map() arrondit vers le bas","Le code level_bar","Erreur courante : une LED à l'envers","À vous : Rotary Safe Lock","Bilan et prochain cours"]
 ],
 "ar": [
  "حوّل نطاق أرقام إلى نطاق آخر بالدالة map(): خافت بمقبض أوضح، ومقبض يعمل بالعكس، ومؤشر مستوى من 3 LED يمتلئ مثل مقياس الصوت. مع سبب تقريب map() إلى الأسفل، والخطأ الشائع في عكس LED، وتحديك: Rotary Safe Lock.",
  ["المؤشر يمتلئ","مراجعة: المقبض والطباعة أولاً","الفكرة: خريطة مدينة","سطر map() قطعة قطعة","شرح map_dimmer","عكس النطاق","مؤشر مستوى مثل مؤشر البطارية","توصيل LED الأصفر والأخضر","فخ المستوى: map() تقرّب للأسفل","شرح level_bar","خطأ شائع: LED مقلوب","دورك: Rotary Safe Lock","ملخص والدرس القادم"]
 ],
 "id": [
  "Ubah satu rentang angka menjadi rentang lain dengan map(): dimmer knob yang lebih jelas, knob yang bekerja terbalik, dan bar level 3 LED yang terisi seperti pengukur volume. Plus alasan map() membulatkan ke bawah, kesalahan umum LED terpasang terbalik, dan tantanganmu: Rotary Safe Lock.",
  ["Bar terisi","Ulasan: knob dan cetak dulu","Idenya: peta kota","Baris map(), bagian demi bagian","Kode map_dimmer","Membalik rentang","Bar level seperti bar baterai","Merangkai LED kuning dan hijau","Jebakan level: map() membulatkan ke bawah","Kode level_bar","Kesalahan umum: LED terbalik","Giliranmu: Rotary Safe Lock","Ringkasan dan pelajaran berikut"]
 ],
 "ja": [
  "map()で数値の範囲を別の範囲に変換します。分かりやすいつまみ調光、逆向きに働くつまみ、音量メーターのように満ちていく3LEDのレベルバー。さらにmap()が切り捨てる理由、LEDを逆向きに付けるよくある間違い、そして課題：Rotary Safe Lock。",
  ["バーが満ちていく","復習：つまみとまず表示","アイデア：街の地図","map()の行をひとつずつ","map_dimmerのコード","範囲を反転する","電池残量のようなレベルバー","黄色と緑のLEDの配線","レベルの落とし穴：map()は切り捨て","level_barのコード","よくある間違い：LEDの逆向き","課題：Rotary Safe Lock","まとめと次のレッスン"]
 ],
 "ru": [
  "Превращайте один диапазон чисел в другой с помощью map(): более понятный диммер на ручке, ручка, работающая наоборот, и шкала уровня из 3 светодиодов, которая заполняется как индикатор громкости. А ещё почему map() округляет вниз, частая ошибка с перевёрнутым светодиодом и ваше задание: Rotary Safe Lock.",
  ["Шкала заполняется","Повторение: ручка и сначала печать","Идея: карта города","Строка map() по частям","Разбор map_dimmer","Переворачиваем диапазон","Шкала уровня как у батареи","Подключение жёлтого и зелёного светодиодов","Ловушка уровня: map() округляет вниз","Разбор level_bar","Частая ошибка: светодиод наоборот","Ваше задание: Rotary Safe Lock","Итоги и следующий урок"]
 ],
 "vi": [
  "Đổi một khoảng số thành khoảng khác bằng map(): dimmer núm xoay dễ hiểu hơn, núm xoay chạy ngược và thanh mức 3 LED đầy dần như đồng hồ âm lượng. Cùng lý do map() làm tròn xuống, lỗi hay gặp khi cắm LED ngược và thử thách: Rotary Safe Lock.",
  ["Thanh mức đầy dần","Ôn tập: núm xoay và in trước","Ý tưởng: bản đồ thành phố","Dòng map(), từng phần một","Mã map_dimmer","Đảo ngược khoảng","Thanh mức như thanh pin","Nối LED vàng và xanh lá","Cái bẫy mức: map() làm tròn xuống","Mã level_bar","Lỗi thường gặp: LED cắm ngược","Đến lượt bạn: Rotary Safe Lock","Tóm tắt và bài tiếp theo"]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nCode + lesson: '+repo+'/tree/main/lessons/08-map-and-level-bar\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n#ESP32 #Arduino #map #Potentiometer #Electronics'
loc={}
for lang,(intro,names) in T.items():
    title=TITLES[lang]+TAG
    assert len(names)==len(times)==len(chapters),(lang,len(names))
    assert len(title)<=100,(lang,len(title))
    loc[lang]={'title':title,'description':intro+links+'\n\n'+'\n'.join(t+' '+n for t,n in zip(times,names))+credit}
assert set(loc)==set(TITLES)==set("en tr hi pt es de fr ar id ja ru vi".split())
(here/'localize.json').write_text(json.dumps(loc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
md='# Episode 8 - map(), Dimmer Knobs and Level Bars\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Original language: English. Category: Education.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Upload checklist\n\n- Final EN video, four separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('ep08 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
