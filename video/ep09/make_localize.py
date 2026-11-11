"""Episode 9 metadata: regenerate after the final schedule.
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
TAG=' | ESP32 From Zero #9'
TITLES={
 "en":"ESP32 State Machine: Build a Smart Pedestrian Crossing",
 "tr":"ESP32 State Machine: Akıllı Yaya Geçidi Projesi",
 "hi":"ESP32 State Machine: स्मार्ट पैदल पार पथ बनाएँ",
 "pt":"ESP32 Máquina de Estados: Faixa de Pedestres Inteligente",
 "es":"ESP32 Máquina de Estados: Cruce Peatonal Inteligente",
 "de":"ESP32 Zustandsautomat: Intelligenter Fußgängerüberweg",
 "fr":"ESP32 Machine à états : passage piéton intelligent",
 "ar":"ESP32 آلة الحالات: معبر مشاة ذكي",
 "id":"ESP32 State Machine: Membuat Penyeberangan Pintar",
 "ja":"ESP32 ステートマシン：スマート横断歩道を作る",
 "ru":"ESP32 конечный автомат: умный пешеходный переход",
 "vi":"ESP32 máy trạng thái: làm vạch qua đường thông minh",
}
T={
 "en": [
  "Our first mini project: a pedestrian crossing with car lights, a walk light, a request button and a knob. One variable, state, remembers which step we're in, and millis() times every step without delay(). Plus: measuring how long a button was held, the common start-time mistake, and your turn: a slow walker mode.",
  ["The crossing in action","Recall: map() and millis()","The plan: parts and no new wire","Why a chain of delay() fails","The idea: a washing machine","crossing code tour","Steps 0 to 3 and the clock","Predict and run the crossing","The idea: a parking ticket","press_time code tour","Common mistake: no new start time","Your turn: slow walker mode","Recap and next lesson"]
 ],
 "tr": [
  "İlk mini projemiz: araba ışıkları, yaya ışığı, istek butonu ve bir düğmeyle akıllı bir yaya geçidi. state adlı tek bir değişken hangi adımda olduğumuzu hatırlıyor, millis() her adımı delay() kullanmadan zamanlıyor. Ayrıca: bir butonun ne kadar basılı tutulduğunu ölçmek, yaygın başlangıç zamanı hatası ve sıra sizde: yavaş yürüyen modu.",
  ["Yaya geçidi iş başında","Hatırlatma: map() ve millis()","Plan: parçalar ve yeni kablo yok","delay() zinciri neden olmaz","Fikir: bir çamaşır makinesi","crossing kod turu","0'dan 3'e adımlar ve saat","Tahmin et ve çalıştır","Fikir: bir otopark bileti","press_time kod turu","Yaygın hata: yeni başlangıç zamanı yok","Sıra sizde: yavaş yürüyen modu","Özet ve sonraki ders"]
 ],
 "hi": [
  "हमारा पहला mini project: car lights, walk light, request button और एक knob वाला पैदल पार पथ। state नाम का एक variable याद रखता है कि कौन सा कदम चल रहा है, और millis() हर कदम को delay() के बिना नापता है। साथ में: button कितनी देर दबा रहा ये नापना, शुरुआती समय की आम गलती और आपकी बारी: धीमा राहगीर मोड।",
  ["पार पथ चलता हुआ","दोहराव: map() और millis()","योजना: पुर्ज़े और कोई नया तार नहीं","delay() की ज़ंजीर क्यों नहीं चलती","विचार: कपड़े धोने की मशीन","crossing कोड","कदम शून्य से तीन और घड़ी","अंदाज़ा लगाइए और चलाइए","विचार: पार्किंग टिकट","press_time कोड","आम गलती: नया शुरुआती समय नहीं","आपकी बारी: धीमा राहगीर मोड","सारांश और अगला पाठ"]
 ],
 "pt": [
  "Nosso primeiro mini projeto: uma faixa de pedestres com luzes de carro, luz de travessia, botão de pedido e um knob. Uma variável, state, lembra em que passo estamos, e o millis() cronometra cada passo sem delay(). Também: medir por quanto tempo um botão foi segurado, o erro comum do tempo de início e sua vez: o modo pedestre lento.",
  ["A faixa em ação","Revisão: map() e millis()","O plano: peças e nenhum fio novo","Por que uma corrente de delay() falha","A ideia: uma máquina de lavar","Código crossing","Passos 0 a 3 e o relógio","Preveja e rode a faixa","A ideia: um ticket de estacionamento","Código press_time","Erro comum: sem novo tempo de início","Sua vez: modo pedestre lento","Resumo e próxima aula"]
 ],
 "es": [
  "Nuestro primer mini proyecto: un cruce peatonal con luces de autos, luz peatonal, botón de pedido y una perilla. Una variable, state, recuerda en qué paso vamos, y millis() cronometra cada paso sin delay(). Además: medir cuánto tiempo se mantuvo un botón, el error común del tiempo de inicio y tu turno: un modo peatón lento.",
  ["El cruce en acción","Repaso: map() y millis()","El plan: piezas y ningún cable nuevo","Por qué falla una cadena de delay()","La idea: una lavadora","Código crossing","Pasos 0 a 3 y el reloj","Predice y ejecuta el cruce","La idea: un ticket de estacionamiento","Código press_time","Error común: sin nuevo tiempo de inicio","Tu turno: modo peatón lento","Resumen y próxima lección"]
 ],
 "de": [
  "Unser erstes Mini-Projekt: ein Fußgängerüberweg mit Autoampel, Fußgängerlicht, Anforderungsknopf und einem Regler. Eine Variable, state, merkt sich den aktuellen Schritt, und millis() misst jeden Schritt ohne delay(). Dazu: messen, wie lange ein Knopf gehalten wurde, der typische Fehler mit der Startzeit und deine Aufgabe: ein Modus für langsame Fußgänger.",
  ["Der Überweg in Aktion","Rückblick: map() und millis()","Der Plan: Teile und kein neues Kabel","Warum eine delay()-Kette scheitert","Die Idee: eine Waschmaschine","crossing erklärt","Schritte 0 bis 3 und die Uhr","Raten und Überweg starten","Die Idee: ein Parkschein","press_time erklärt","Häufiger Fehler: keine neue Startzeit","Deine Aufgabe: Modus für langsame Fußgänger","Rückblick und nächste Lektion"]
 ],
 "fr": [
  "Notre premier mini-projet : un passage piéton avec feux de voitures, feu piéton, bouton de demande et un potentiomètre. Une variable, state, retient l'étape en cours, et millis() chronomètre chaque étape sans delay(). Et aussi : mesurer combien de temps un bouton a été tenu, l'erreur classique de l'heure de début et votre défi : un mode piéton lent.",
  ["Le passage en action","Rappel : map() et millis()","Le plan : pièces et aucun fil neuf","Pourquoi une chaîne de delay() échoue","L'idée : un lave-linge","Le code crossing","Étapes 0 à 3 et l'horloge","Prédire et lancer le passage","L'idée : un ticket de parking","Le code press_time","Erreur courante : pas de nouveau départ","À vous : le mode piéton lent","Bilan et prochain cours"]
 ],
 "ar": [
  "مشروعنا الصغير الأول: معبر مشاة بأضواء السيارات وضوء العبور وزر الطلب ومقبض. متغيّر واحد، state، يتذكر أي خطوة نحن فيها، وmillis() تقيس زمن كل خطوة بلا delay(). مع قياس مدة الضغط على الزر، والخطأ الشائع في وقت البدء، وتحديك: وضع المشاة البطيء.",
  ["المعبر أثناء العمل","مراجعة: map() وmillis()","الخطة: القطع بلا أسلاك جديدة","لماذا تفشل سلسلة delay()","الفكرة: غسالة ملابس","شرح crossing","الخطوات 0 إلى 3 والساعة","توقّع وشغّل المعبر","الفكرة: تذكرة موقف سيارات","شرح press_time","خطأ شائع: بلا وقت بدء جديد","دورك: وضع المشاة البطيء","ملخص والدرس القادم"]
 ],
 "id": [
  "Proyek mini pertama kita: penyeberangan pejalan kaki dengan lampu mobil, lampu jalan, tombol permintaan, dan sebuah knob. Satu variabel, state, mengingat kita di langkah mana, dan millis() menghitung waktu tiap langkah tanpa delay(). Plus: mengukur berapa lama tombol ditahan, kesalahan umum waktu mulai, dan giliranmu: mode pejalan kaki lambat.",
  ["Penyeberangan beraksi","Ulasan: map() dan millis()","Rencana: komponen tanpa kabel baru","Mengapa rantai delay() gagal","Idenya: mesin cuci","Kode crossing","Langkah 0 sampai 3 dan jam","Tebak dan jalankan penyeberangan","Idenya: karcis parkir","Kode press_time","Kesalahan umum: tanpa waktu mulai baru","Giliranmu: mode pejalan kaki lambat","Ringkasan dan pelajaran berikut"]
 ],
 "ja": [
  "最初のミニプロジェクト：車用ライト、歩行者用ライト、リクエストボタン、つまみを備えた横断歩道。stateという1つの変数が今のステップを覚え、millis()がdelay()なしで各ステップの時間を測ります。さらに、ボタンを押していた時間の測り方、開始時刻のよくある間違い、そして課題：ゆっくり歩く人モード。",
  ["動く横断歩道","復習：map()とmillis()","計画：部品と新しい配線なし","delay()の連なりがダメな理由","アイデア：洗濯機","crossingのコード","ステップ0から3と時計","予想して横断歩道を動かす","アイデア：駐車券","press_timeのコード","よくある間違い：新しい開始時刻がない","課題：ゆっくり歩く人モード","まとめと次のレッスン"]
 ],
 "ru": [
  "Наш первый мини-проект: пешеходный переход с огнями для машин, огнём для пешеходов, кнопкой запроса и ручкой. Одна переменная, state, помнит текущий шаг, а millis() отмеряет время каждого шага без delay(). А ещё: как измерить, сколько держали кнопку, частая ошибка со временем начала и ваше задание: режим медленного пешехода.",
  ["Переход в действии","Повторение: map() и millis()","План: детали и никаких новых проводов","Почему цепочка delay() не работает","Идея: стиральная машина","Разбор crossing","Шаги 0 до 3 и часы","Предскажите и запустите переход","Идея: парковочный талон","Разбор press_time","Частая ошибка: нет нового времени начала","Ваше задание: режим медленного пешехода","Итоги и следующий урок"]
 ],
 "vi": [
  "Dự án nhỏ đầu tiên của ta: vạch qua đường với đèn xe, đèn đi bộ, nút yêu cầu và một núm xoay. Một biến, state, nhớ ta đang ở bước nào, và millis() đo thời gian từng bước mà không cần delay(). Cùng cách đo nút được giữ bao lâu, lỗi hay gặp về thời điểm bắt đầu và thử thách: chế độ người đi bộ chậm.",
  ["Vạch qua đường hoạt động","Ôn tập: map() và millis()","Kế hoạch: linh kiện, không dây mới","Vì sao chuỗi delay() thất bại","Ý tưởng: máy giặt","Mã crossing","Bước 0 đến 3 và đồng hồ","Dự đoán và chạy vạch qua đường","Ý tưởng: vé gửi xe","Mã press_time","Lỗi thường gặp: thiếu thời điểm bắt đầu mới","Đến lượt bạn: chế độ người đi bộ chậm","Tóm tắt và bài tiếp theo"]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nCode + lesson: '+repo+'/tree/main/lessons/09-mini-project-1\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n#ESP32 #Arduino #StateMachine #TrafficLight #Electronics'
loc={}
for lang,(intro,names) in T.items():
    title=TITLES[lang]+TAG
    assert len(names)==len(times)==len(chapters),(lang,len(names))
    assert len(title)<=100,(lang,len(title))
    loc[lang]={'title':title,'description':intro+links+'\n\n'+'\n'.join(t+' '+n for t,n in zip(times,names))+credit}
assert set(loc)==set(TITLES)==set("en tr hi pt es de fr ar id ja ru vi".split())
(here/'localize.json').write_text(json.dumps(loc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
md='# Episode 9 - Mini Project 1: a Smart Pedestrian Crossing\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Original language: English. Category: Education.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Upload checklist\n\n- Final EN video, four separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('ep09 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
