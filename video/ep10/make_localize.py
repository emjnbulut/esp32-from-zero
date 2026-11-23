"""Episode 10 metadata: regenerate after the final schedule.
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
# Titles are result-first (guidelines section 12); every title ends with the series tag.
TAG=' | ESP32 From Zero #10'
TITLES={
 "en":"I Built a Reflex Game That Remembers Your Record (ESP32 + OLED)",
 "tr":"Rekorunu Hatırlayan Bir Refleks Oyunu Yaptım (ESP32 + OLED)",
 "hi":"मैंने ऐसा रिफ़्लेक्स गेम बनाया जो आपका रिकॉर्ड याद रखता है (ESP32 + OLED)",
 "pt":"Criei um Jogo de Reflexos que Lembra do Seu Recorde (ESP32 + OLED)",
 "es":"Hice un Juego de Reflejos que Recuerda tu Récord (ESP32 + OLED)",
 "de":"Ich baute ein Reaktionsspiel, das sich deinen Rekord merkt (ESP32 + OLED)",
 "fr":"J'ai fait un jeu de réflexes qui retient ton record (ESP32 + OLED)",
 "ar":"صنعت لعبة ردّ فعل تتذكر رقمك القياسي (ESP32 + OLED)",
 "id":"Aku Membuat Game Refleks yang Mengingat Rekormu (ESP32 + OLED)",
 "ja":"記録を覚えている反射神経ゲームを作った（ESP32 + OLED）",
 "ru":"Я сделал игру на реакцию, которая помнит ваш рекорд (ESP32 + OLED)",
 "vi":"Tôi làm game phản xạ nhớ kỷ lục của bạn (ESP32 + OLED)",
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
PL={
 "en":"Full course playlist:","tr":"Tüm kurs oynatma listesi:","hi":"पूरे कोर्स की प्लेलिस्ट:","pt":"Playlist do curso completo:","es":"Lista de reproducción del curso completo:","de":"Playlist zum ganzen Kurs:","fr":"Playlist du cours complet :","ar":"قائمة تشغيل الدورة كاملة:","id":"Playlist kursus lengkap:","ja":"コース全体の再生リスト：","ru":"Плейлист всего курса:","vi":"Danh sách phát toàn khóa:",
}
PLID='PLEhjjsUBtWDk'
T={
 "en": [
  "A reflex game with a real screen and a real beep, and a record that survives unplugging the board. You'll meet a 0.96 inch OLED screen (I2C: two shared wires), a passive buzzer played with tone(), and Preferences, the ESP32's small drawer that keeps values without power. Plus: the common mistake of saving every round, and your turn: erase the record with a long press.",
  ["The game that remembers","The OLED screen and I2C","The buzzer and the button","Wiring it step by step","Code: the library and show()","The game: four steps and a beep","Preferences: the drawer that remembers","Common mistake and your turn"]
 ],
 "tr": [
  "Gerçek bir ekranı ve gerçek bir bip sesi olan, kartı fişten çekseniz bile rekoru kaybolmayan bir refleks oyunu. 0,96 inç OLED ekranla (I2C: ortak iki kablo), tone() ile çalınan pasif bir buzzerla ve ESP32'nin elektriksiz de değer saklayan küçük çekmecesi Preferences ile tanışacaksınız. Ayrıca: her turu kaydetme hatası ve sıra sizde: uzun basışla rekoru silmek.",
  ["Hatırlayan oyun","OLED ekran ve I2C","Buzzer ve buton","Adım adım bağlantı","Kod: kütüphane ve show()","Oyun: dört adım ve bir bip","Preferences: hatırlayan çekmece","Yaygın hata ve sıra sizde"]
 ],
 "hi": [
  "असली स्क्रीन, असली बीप और ऐसा रिकॉर्ड वाला रिफ़्लेक्स गेम जो बोर्ड का प्लग निकालने पर भी बचा रहता है। इसमें 0.96 इंच की OLED स्क्रीन (I2C: दो साझा तार), tone() से बजने वाला पैसिव बज़र, और Preferences मिलेंगे, जो ESP32 की छोटी दराज़ है और बिना बिजली के भी मान रखती है। साथ में: हर राउंड सेव करने की आम गलती और आपकी बारी: लंबे दबाव से रिकॉर्ड मिटाना।",
  ["याद रखने वाला गेम","OLED स्क्रीन और I2C","बज़र और बटन","कदम दर कदम वायरिंग","कोड: लाइब्रेरी और show()","गेम: चार कदम और एक बीप","Preferences: याद रखने वाली दराज़","आम गलती और आपकी बारी"]
 ],
 "pt": [
  "Um jogo de reflexos com tela de verdade, bipe de verdade e um recorde que sobrevive mesmo desligando a placa. Você vai conhecer uma tela OLED de 0,96 polegada (I2C: dois fios compartilhados), um buzzer passivo tocado com tone() e a Preferences, a gaveta do ESP32 que guarda valores sem energia. Também: o erro comum de salvar toda rodada e sua vez: apagar o recorde com um toque longo.",
  ["O jogo que lembra","A tela OLED e o I2C","O buzzer e o botão","A ligação passo a passo","Código: a biblioteca e show()","O jogo: quatro passos e um bipe","Preferences: a gaveta que lembra","Erro comum e sua vez"]
 ],
 "es": [
  "Un juego de reflejos con pantalla de verdad, pitido de verdad y un récord que sobrevive aunque desconectes la placa. Conocerás una pantalla OLED de 0,96 pulgadas (I2C: dos cables compartidos), un zumbador pasivo que suena con tone() y Preferences, el cajón del ESP32 que guarda valores sin corriente. Además: el error común de guardar cada ronda y tu turno: borrar el récord con una pulsación larga.",
  ["El juego que recuerda","La pantalla OLED y el I2C","El zumbador y el botón","El cableado paso a paso","Código: la biblioteca y show()","El juego: cuatro pasos y un pitido","Preferences: el cajón que recuerda","Error común y tu turno"]
 ],
 "de": [
  "Ein Reaktionsspiel mit echtem Bildschirm, echtem Piepton und einem Rekord, der das Abziehen des Boards überlebt. Du lernst einen 0,96-Zoll-OLED-Bildschirm kennen (I2C: zwei gemeinsame Kabel), einen passiven Buzzer, der mit tone() spielt, und Preferences, die kleine Schublade des ESP32, die Werte ohne Strom behält. Dazu: der häufige Fehler, jede Runde zu speichern, und deine Aufgabe: den Rekord mit einem langen Druck löschen.",
  ["Das Spiel, das sich erinnert","Der OLED-Bildschirm und I2C","Der Buzzer und der Taster","Verkabelung Schritt für Schritt","Code: die Bibliothek und show()","Das Spiel: vier Schritte und ein Piepton","Preferences: die Schublade, die sich erinnert","Häufiger Fehler und deine Aufgabe"]
 ],
 "fr": [
  "Un jeu de réflexes avec un vrai écran, un vrai bip et un record qui survit au débranchement de la carte. Tu vas découvrir un écran OLED de 0,96 pouce (I2C : deux fils partagés), un buzzer passif joué avec tone(), et Preferences, le petit tiroir de l'ESP32 qui garde des valeurs sans courant. Et aussi : l'erreur classique d'enregistrer chaque manche, et ton défi : effacer le record par un appui long.",
  ["Le jeu qui se souvient","L'écran OLED et l'I2C","Le buzzer et le bouton","Le câblage pas à pas","Code : la bibliothèque et show()","Le jeu : quatre étapes et un bip","Preferences : le tiroir qui se souvient","Erreur courante et à toi de jouer"]
 ],
 "ar": [
  "لعبة ردّ فعل بشاشة حقيقية وصفّارة حقيقية ورقم قياسي ينجو حتى لو فصلت اللوحة عن الكهرباء. ستتعرف على شاشة OLED بحجم 0.96 بوصة (I2C: سلكان مشتركان)، وجرس سلبي يعزف بـ tone()، وPreferences، درج ESP32 الصغير الذي يحفظ القيم بلا كهرباء. مع الخطأ الشائع في حفظ كل جولة، وتحديك: مسح الرقم القياسي بضغطة طويلة.",
  ["اللعبة التي تتذكر","شاشة OLED وبروتوكول I2C","الجرس والزر","التوصيل خطوة بخطوة","الكود: المكتبة ودالة show()","اللعبة: أربع خطوات وصفّارة","Preferences: الدرج الذي يتذكر","خطأ شائع ودورك"]
 ],
 "id": [
  "Game refleks dengan layar sungguhan dan bunyi bip sungguhan, plus rekor yang bertahan meski board dicabut. Kamu akan mengenal layar OLED 0,96 inci (I2C: dua kabel bersama), buzzer pasif yang dimainkan dengan tone(), dan Preferences, laci kecil ESP32 yang menyimpan nilai tanpa daya. Plus: kesalahan umum menyimpan tiap ronde, dan giliranmu: menghapus rekor dengan tekan lama.",
  ["Game yang mengingat","Layar OLED dan I2C","Buzzer dan tombol","Merangkai langkah demi langkah","Kode: library dan show()","Game: empat langkah dan satu bip","Preferences: laci yang mengingat","Kesalahan umum dan giliranmu"]
 ],
 "ja": [
  "本物の画面と本物のビープ音を使い、ボードを抜いても記録が消えない反射神経ゲームです。0.96インチのOLED画面（I2C：共有する二本の線）、tone()で鳴らすパッシブブザー、そして電源なしで値を保存するESP32の小さな引き出しPreferencesを紹介します。さらに、毎ラウンド保存してしまうよくある間違いと、課題：長押しで記録を消す機能。",
  ["覚えているゲーム","OLED画面とI2C","ブザーとボタン","ステップごとの配線","コード：ライブラリとshow()","ゲーム：四つのステップとビープ音","Preferences：覚えている引き出し","よくある間違いと課題"]
 ],
 "ru": [
  "Игра на реакцию с настоящим экраном, настоящим писком и рекордом, который переживает отключение платы. Вы познакомитесь с OLED-экраном 0,96 дюйма (I2C: два общих провода), пассивным зуммером, который играет через tone(), и Preferences, маленьким ящиком ESP32, хранящим значения без питания. А ещё: частая ошибка сохранять каждый раунд и ваше задание: стереть рекорд долгим нажатием.",
  ["Игра, которая помнит","OLED-экран и I2C","Зуммер и кнопка","Подключение шаг за шагом","Код: библиотека и show()","Игра: четыре шага и писк","Preferences: ящик, который помнит","Частая ошибка и ваше задание"]
 ],
 "vi": [
  "Một trò chơi phản xạ với màn hình thật, tiếng bíp thật và kỷ lục còn nguyên dù bạn rút bo mạch. Bạn sẽ làm quen với màn hình OLED 0,96 inch (I2C: hai dây dùng chung), còi thụ động phát bằng tone(), và Preferences, ngăn kéo nhỏ của ESP32 giữ giá trị khi không có điện. Cùng lỗi hay gặp khi lưu mỗi lượt, và thử thách: xóa kỷ lục bằng cách nhấn giữ.",
  ["Trò chơi biết nhớ","Màn hình OLED và I2C","Còi và nút nhấn","Nối dây từng bước","Mã: thư viện và show()","Trò chơi: bốn bước và một tiếng bíp","Preferences: ngăn kéo biết nhớ","Lỗi thường gặp và đến lượt bạn"]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nCode + lesson: '+repo+'/tree/main/lessons/10-reflex-oled\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n#ESP32 #Arduino #OLED #ReflexGame #Electronics'
TAGS='ESP32 OLED, ESP32 OLED display tutorial, ESP32 SSD1306, ESP32 I2C OLED, ESP32 reflex game, ESP32 reaction time game, ESP32 Preferences, ESP32 save data power off, ESP32 putULong getULong, ESP32 passive buzzer, ESP32 tone, ESP32 buzzer, ESP32 push button, ESP32 project, ESP32 projects for beginners, ESP32 for beginners, ESP32 tutorial, Arduino reflex game, Arduino OLED, Adafruit SSD1306, ESP32 From Zero, ESP32 starter kit, ESP32 Arduino IDE'
assert 15<=len(TAGS.split(', '))<=25 and len(TAGS)<=500
loc={}
for lang,(intro,names) in T.items():
    title=TITLES[lang]+TAG
    assert len(names)==len(times)==len(chapters),(lang,len(names))
    assert len(title)<=100,(lang,len(title))
    NL='\n'
    loc[lang]={'title':title,'description':intro+NL+NL+START[lang]+' https://youtu.be/RyR4OEA7ESA'+links+NL+PL[lang]+' https://www.youtube.com/playlist?list='+PLID+NL+NL+NL.join(t+' '+n for t,n in zip(times,names))+credit}
assert set(loc)==set(TITLES)==set("en tr hi pt es de fr ar id ja ru vi".split())
(here/'localize.json').write_text(json.dumps(loc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
md='# Episode 10 - Reflex Game 2.0: OLED screen, buzzer and a record that survives power off\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Original language: English. Category: Education.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Tags\n\n'+TAGS+'\n'
md+='\n\n## Upload checklist\n\n- Final EN video, four separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('ep10 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
