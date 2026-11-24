"""Episode 11 metadata: regenerate after the final schedule.
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
    ids=[s['id'] for s in script['segments']]
    tc=segs[ids[ids.index(script['sting_after'])+1]]['start']-0.1
else:
    segs=json.loads(schedule.read_text(encoding='utf-8'))['segments']
    tc=bumpers.cut(here)
starts=[0]+[int(bumpers.shift(segs[c]['start'],tc)) for c in chapters[1:]]
assert all(b-a>=10 for a,b in zip(starts,starts[1:])), 'YouTube chapters must be >= 10 seconds'
times=['%d:%02d'%divmod(v,60) for v in starts]
# Titles are result-first (guidelines section 12); every title ends with the series tag.
TAG=' | ESP32 From Zero #11'
TITLES={
 "en":"I Built a Motion Alarm That Catches Anyone Sneaking In (ESP32 + PIR)",
 "tr":"Gizlice Girenleri Yakalayan Bir Hareket Alarmı Yaptım (ESP32 + PIR)",
 "hi":"मैंने चुपके से घुसने वाले को पकड़ने वाला मोशन अलार्म बनाया (ESP32 + PIR)",
 "pt":"Criei um Alarme de Movimento que Pega Qualquer Intruso (ESP32 + PIR)",
 "es":"Hice una Alarma que Atrapa a Quien se Cuele (ESP32 + PIR)",
 "de":"Ich baute einen Bewegungsalarm, der jeden Schleicher erwischt (ESP32 + PIR)",
 "fr":"J'ai fait une alarme de mouvement qui attrape tous les intrus (ESP32 + PIR)",
 "ar":"صنعت إنذار حركة يمسك بكل من يتسلل (ESP32 + PIR)",
 "id":"Aku Membuat Alarm Gerak yang Menangkap Penyelinap (ESP32 + PIR)",
 "ja":"こっそり侵入する人を捕まえる動きアラームを作った（ESP32 + PIR）",
 "ru":"Я сделал сигнализацию, которая ловит любого, кто крадётся (ESP32 + PIR)",
 "vi":"Tôi làm báo động chuyển động bắt mọi kẻ lẻn vào (ESP32 + PIR)",
}
START={
 "en":"New here? Start with Episode 1:",
 "tr":"Yeni misin? Bölüm 1'den başla:",
 "hi":"नए हैं? एपिसोड 1 से शुरू करें:",
 "pt":"Novo por aqui? Comece pelo Episódio 1:",
 "es":"¿Eres nuevo? Empieza por el Episodio 1:",
 "de":"Neu hier? Starte mit Folge 1:",
 "fr":"Nouveau ici ? Commence par l'épisode 1 :",
 "ar":"جديد هنا؟ ابدأ من الحلقة 1:",
 "id":"Baru di sini? Mulai dari Episode 1:",
 "ja":"初めての方は第1回から：",
 "ru":"Вы здесь впервые? Начните с эпизода 1:",
 "vi":"Bạn mới đến? Hãy bắt đầu từ tập 1:",
}
PREV={
 "en":"Previous episode:","tr":"Önceki bölüm:","hi":"पिछला एपिसोड:","pt":"Episódio anterior:","es":"Episodio anterior:","de":"Vorherige Folge:","fr":"Épisode précédent :","ar":"الحلقة السابقة:","id":"Episode sebelumnya:","ja":"前回：","ru":"Предыдущий эпизод:","vi":"Tập trước:",
}
PREVURL='https://youtu.be/0tr5Sf8dJDY'
PL={
 "en":"Full course playlist:","tr":"Tüm kurs oynatma listesi:","hi":"पूरे कोर्स की प्लेलिस्ट:","pt":"Playlist do curso completo:","es":"Lista de reproducción del curso completo:","de":"Playlist zum ganzen Kurs:","fr":"Playlist du cours complet :","ar":"قائمة تشغيل الدورة كاملة:","id":"Playlist kursus lengkap:","ja":"コース全体の再生リスト：","ru":"Плейлист всего курса:","vi":"Danh sách phát toàn khóa:",
}
PLID='PLEhjjsUBtWDk'
T={
 "en": [
  "A motion alarm for your desk: you arm it, walk out, and the moment a hand sneaks toward the cookie jar, a siren goes off, and the screen remembers when it happened. You'll meet the PIR motion sensor (to our code it is just a thumbs up or a thumbs down), a four-step state machine like a washing machine (off, leaving, armed, alarm), a two-note siren on the passive buzzer, and millis() for \"seen twice, last time three minutes ago\". Plus: the common mistake of the alarm going off right after arming (warm-up time and the time knob), and your turn: keep the catch count with Preferences.",
  ["The alarm that catches sneaks","The PIR motion sensor","Wiring it step by step","Code: four steps and a siren","Code: how long ago?","Active vs passive buzzer","The test and the common problem","Your turn"]
 ],
 "tr": [
  "Masanız için bir hareket alarmı: kuruyorsunuz, odadan çıkıyorsunuz ve bir el kurabiye kavanozuna uzandığı anda siren çalıyor, ekran da bunun ne zaman olduğunu hatırlıyor. PIR hareket sensörüyle (kodumuz için sadece başparmak yukarı ya da aşağı), çamaşır makinesi gibi dört adımlı bir durum makinesiyle (kapalı, çıkış, kurulu, alarm), pasif buzzer üzerinde iki notalı bir sirenle ve \"iki kez görüldü, sonuncusu üç dakika önce\" için millis() ile tanışacaksınız. Ayrıca: kurar kurmaz çalan alarm hatası (ısınma süresi ve süre düğmesi) ve sıra sizde: yakalama sayısını Preferences ile saklamak.",
  ["Gizlice girenleri yakalayan alarm","PIR hareket sensörü","Adım adım bağlantı","Kod: dört adım ve bir siren","Kod: ne kadar önce?","Aktif ve pasif buzzer","Test ve yaygın sorun","Sıra sizde"]
 ],
 "hi": [
  "आपकी मेज़ के लिए एक मोशन अलार्म: आप इसे चालू करते हैं, कमरे से बाहर जाते हैं, और जैसे ही कोई हाथ बिस्कुट के डिब्बे की ओर बढ़ता है, सायरन बज उठता है और स्क्रीन याद रखती है कि ये कब हुआ। इसमें PIR मोशन सेंसर मिलेगा (हमारे कोड के लिए बस अंगूठा ऊपर या नीचे), वॉशिंग मशीन जैसी चार चरणों वाली स्टेट मशीन (बंद, निकलना, तैयार, अलार्म), पैसिव बज़र पर दो सुरों का सायरन, और \"दो बार देखा, आख़िरी तीन मिनट पहले\" के लिए millis()। साथ में: चालू करते ही अलार्म बजने की आम समस्या (गरम होने का समय और टाइम घुंडी), और आपकी बारी: Preferences से पकड़ने की गिनती बचाना।",
  ["चुपके से घुसने वाले को पकड़ने वाला अलार्म","PIR मोशन सेंसर","कदम दर कदम वायरिंग","कोड: चार चरण और एक सायरन","कोड: कितना समय पहले?","एक्टिव और पैसिव बज़र","टेस्ट और आम समस्या","आपकी बारी"]
 ],
 "pt": [
  "Um alarme de movimento para a sua mesa: você arma, sai da sala, e no momento em que uma mão se aproxima do pote de biscoitos, a sirene toca e a tela lembra quando aconteceu. Você vai conhecer o sensor de movimento PIR (para o nosso código ele é só um joinha para cima ou para baixo), uma máquina de estados de quatro passos como uma máquina de lavar (desligado, saindo, armado, alarme), uma sirene de duas notas no buzzer passivo e o millis() para \"visto duas vezes, o último há três minutos\". Também: o erro comum do alarme tocar logo ao armar (tempo de aquecimento e o botão de tempo) e sua vez: guardar a contagem de capturas com Preferences.",
  ["O alarme que pega intrusos","O sensor de movimento PIR","A ligação passo a passo","Código: quatro passos e uma sirene","Código: há quanto tempo?","Buzzer ativo e passivo","O teste e o problema comum","Sua vez"]
 ],
 "es": [
  "Una alarma de movimiento para tu escritorio: la armas, sales, y en el momento en que una mano se acerca al frasco de galletas, suena la sirena y la pantalla recuerda cuándo pasó. Conocerás el sensor de movimiento PIR (para nuestro código es solo un pulgar arriba o abajo), una máquina de estados de cuatro pasos como una lavadora (apagado, saliendo, armado, alarma), una sirena de dos notas con el zumbador pasivo y millis() para \"visto dos veces, la última hace tres minutos\". Además: el error común de que la alarma suene apenas la armas (tiempo de calentamiento y la perilla de tiempo) y tu turno: guardar el número de capturas con Preferences.",
  ["La alarma que atrapa intrusos","El sensor de movimiento PIR","El cableado paso a paso","Código: cuatro pasos y una sirena","Código: ¿hace cuánto?","Zumbador activo y pasivo","La prueba y el problema común","Tu turno"]
 ],
 "de": [
  "Ein Bewegungsalarm für deinen Schreibtisch: Du schaltest ihn scharf, gehst hinaus, und sobald sich eine Hand zum Keksglas schleicht, heult eine Sirene los, und der Bildschirm merkt sich, wann es passiert ist. Du lernst den PIR-Bewegungssensor kennen (für unseren Code nur ein Daumen nach oben oder unten), eine Zustandsmaschine mit vier Schritten wie eine Waschmaschine (aus, Weggehen, scharf, Alarm), eine Sirene aus zwei Tönen am passiven Buzzer und millis() für \"zweimal gesehen, zuletzt vor drei Minuten\". Dazu: der häufige Fehler, dass der Alarm direkt nach dem Scharfschalten losgeht (Aufwärmzeit und Zeitknopf), und deine Aufgabe: die Zahl der Erwischten mit Preferences behalten.",
  ["Der Alarm, der Schleicher erwischt","Der PIR-Bewegungssensor","Verkabelung Schritt für Schritt","Code: vier Schritte und eine Sirene","Code: wie lange ist es her?","Aktiver und passiver Buzzer","Der Test und das häufige Problem","Du bist dran"]
 ],
 "fr": [
  "Une alarme de mouvement pour ton bureau : tu l'armes, tu sors, et dès qu'une main s'approche du pot de biscuits, une sirène retentit et l'écran retient quand c'est arrivé. Tu vas découvrir le capteur de mouvement PIR (pour notre code, juste un pouce levé ou baissé), une machine à états en quatre étapes comme une machine à laver (éteint, départ, armé, alarme), une sirène à deux notes sur le buzzer passif et millis() pour « vu deux fois, la dernière il y a trois minutes ». Et aussi : l'erreur classique de l'alarme qui se déclenche juste après l'armement (temps de chauffe et bouton de durée), et ton défi : garder le nombre d'attrapés avec Preferences.",
  ["L'alarme qui attrape les intrus","Le capteur de mouvement PIR","Le câblage pas à pas","Code : quatre étapes et une sirène","Code : il y a combien de temps ?","Buzzer actif et passif","Le test et le problème courant","À toi de jouer"]
 ],
 "ar": [
  "إنذار حركة لمكتبك: تُفعّله وتغادر، وفي اللحظة التي تتسلل فيها يد نحو جرّة البسكويت تنطلق صفارة الإنذار وتتذكر الشاشة متى حدث ذلك. ستتعرف على حساس الحركة PIR (بالنسبة إلى كودنا هو مجرد إبهام للأعلى أو للأسفل)، وآلة حالات من أربع خطوات مثل الغسالة (متوقف، مغادرة، مفعّل، إنذار)، وصفارة من نغمتين على الجرس السلبي، والدالة millis() لعبارة \"شوهد مرتين، آخر مرة قبل ثلاث دقائق\". مع المشكلة الشائعة: انطلاق الإنذار بعد التفعيل مباشرة (وقت التسخين ومقبض الوقت)، وتحديك: حفظ عدد الإمساكات باستخدام Preferences.",
  ["الإنذار الذي يمسك المتسللين","حساس الحركة PIR","التوصيل خطوة بخطوة","الكود: أربع خطوات وصفارة","الكود: كم مضى؟","الجرس الفعّال والسلبي","التجربة والمشكلة الشائعة","دورك"]
 ],
 "id": [
  "Alarm gerak untuk mejamu: kamu mengaktifkannya, berjalan keluar, dan begitu sebuah tangan menyelinap ke arah toples kue, sirene berbunyi dan layar mengingat kapan itu terjadi. Kamu akan mengenal sensor gerak PIR (bagi kode kita ia hanya jempol ke atas atau ke bawah), mesin status empat langkah seperti mesin cuci (mati, pergi, siaga, alarm), sirene dua nada pada buzzer pasif, dan millis() untuk \"terlihat dua kali, terakhir tiga menit lalu\". Plus: kesalahan umum alarm yang berbunyi tepat setelah diaktifkan (waktu pemanasan dan knob waktu), dan giliranmu: menyimpan jumlah tangkapan dengan Preferences.",
  ["Alarm yang menangkap penyelinap","Sensor gerak PIR","Merangkai langkah demi langkah","Kode: empat langkah dan sirene","Kode: berapa lama yang lalu?","Buzzer aktif dan pasif","Uji coba dan masalah umum","Giliranmu"]
 ],
 "ja": [
  "机の上の動きアラームです。作動させて部屋を出ると、手がクッキーの瓶にそっと伸びた瞬間にサイレンが鳴り、画面はそれがいつ起きたかを覚えています。人感センサーPIR（コードから見ると親指が上か下かだけ）、洗濯機のような四つのステップの状態機械（オフ、外出、警戒、アラーム）、パッシブブザーで鳴らす二音のサイレン、そして「二回検知、最後は三分前」のためのmillis()を紹介します。さらに、作動させた直後にアラームが鳴るよくある問題（温まる時間と時間のつまみ）と、課題：検知した回数をPreferencesで保存すること。",
  ["こっそり侵入する人を捕まえるアラーム","人感センサーPIR","ステップごとの配線","コード：四つのステップとサイレン","コード：どれだけ前？","アクティブとパッシブのブザー","テストとよくある問題","あなたの番"]
 ],
 "ru": [
  "Сигнализация движения для вашего стола: вы включаете её, выходите, и в тот момент, когда рука крадётся к банке с печеньем, звучит сирена, а экран запоминает, когда это случилось. Вы познакомитесь с датчиком движения PIR (для нашего кода это просто большой палец вверх или вниз), конечным автоматом из четырёх шагов, как стиральная машина (выключено, выход, на охране, тревога), сиреной из двух нот на пассивном зуммере и millis() для «замечено дважды, последний раз три минуты назад». А ещё: частая ошибка, когда сигнализация срабатывает сразу после включения (время прогрева и регулятор времени), и ваше задание: сохранить число пойманных с помощью Preferences.",
  ["Сигнализация, которая ловит тех, кто крадётся","Датчик движения PIR","Подключение шаг за шагом","Код: четыре шага и сирена","Код: как давно это было?","Активный и пассивный зуммер","Проверка и частая проблема","Ваше задание"]
 ],
 "vi": [
  "Một chiếc báo động chuyển động cho bàn của bạn: bạn bật canh, bước ra ngoài, và ngay khi một bàn tay rón rén tới lọ bánh quy, còi hú vang lên và màn hình nhớ lại chuyện đó xảy ra lúc nào. Bạn sẽ làm quen với cảm biến chuyển động PIR (với mã của ta nó chỉ là ngón cái giơ lên hoặc chúc xuống), một máy trạng thái bốn bước như máy giặt (tắt, rời đi, đã canh, báo động), còi hú hai nốt trên còi thụ động, và millis() cho \"thấy hai lần, lần cuối ba phút trước\". Cùng lỗi hay gặp là báo động kêu ngay sau khi bật canh (thời gian khởi động và núm thời gian), và thử thách: giữ số lần bắt được bằng Preferences.",
  ["Báo động bắt kẻ lẻn vào","Cảm biến chuyển động PIR","Nối dây từng bước","Mã: bốn bước và còi hú","Mã: cách đây bao lâu?","Còi chủ động và thụ động","Thử nghiệm và vấn đề thường gặp","Đến lượt bạn"]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nCode + lesson: '+repo+'/tree/main/lessons/11-motion-alarm\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n#ESP32 #Arduino #PIR #MotionSensor #Electronics'
TAGS='ESP32 PIR sensor, ESP32 motion sensor, ESP32 motion alarm, ESP32 HC-SR501, HC-SR501 tutorial, ESP32 alarm project, ESP32 security alarm, ESP32 PIR buzzer, ESP32 passive buzzer siren, ESP32 tone siren, ESP32 millis, ESP32 state machine, ESP32 OLED, ESP32 project, ESP32 projects for beginners, ESP32 for beginners, ESP32 tutorial, Arduino PIR sensor, Arduino motion detector, ESP32 From Zero, ESP32 starter kit, ESP32 Arduino IDE'
assert 15<=len(TAGS.split(', '))<=25 and len(TAGS)<=500
loc={}
for lang,(intro,names) in T.items():
    title=TITLES[lang]+TAG
    assert len(names)==len(times)==len(chapters),(lang,len(names))
    assert len(title)<=100,(lang,len(title))
    NL='\n'
    loc[lang]={'title':title,'description':intro+NL+NL+START[lang]+' https://youtu.be/RyR4OEA7ESA'+NL+PREV[lang]+' '+PREVURL+links+NL+PL[lang]+' https://www.youtube.com/playlist?list='+PLID+NL+NL+NL.join(t+' '+n for t,n in zip(times,names))+credit}
assert set(loc)==set(TITLES)==set("en tr hi pt es de fr ar id ja ru vi".split())
(here/'localize.json').write_text(json.dumps(loc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
md='# Episode 11 - Motion Alarm: PIR sensor, four-step state machine, siren and "last seen" time\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Original language: English. Category: Education.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Tags\n\n'+TAGS+'\n'
md+='\n\n## Upload checklist\n\n- Final EN video, four separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('ep11 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
