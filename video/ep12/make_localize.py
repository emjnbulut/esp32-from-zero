"""Episode 12 metadata: regenerate after the final schedule.
When no schedule exists, chapter times are provisional EN-based estimates.
PREVURL is a placeholder (EP11_URL) until episode 11 is uploaded: replace it, then re-run.
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
TAG=' | ESP32 From Zero #12'
TITLES={
 "en":"Control Your ESP32 from Your Phone - No App, No Router",
 "tr":"ESP32'yi Telefonundan Kontrol Et - Uygulama Yok, Modem Yok",
 "hi":"अपने फ़ोन से ESP32 कंट्रोल करें - न ऐप, न राउटर",
 "pt":"Controle o ESP32 pelo Celular - Sem App, Sem Roteador",
 "es":"Controla tu ESP32 desde el Celular - Sin App, Sin Router",
 "de":"Steuere deinen ESP32 per Handy - ohne App, ohne Router",
 "fr":"Contrôle ton ESP32 depuis ton téléphone - sans appli, sans box",
 "ar":"تحكّم في ESP32 من هاتفك - بلا تطبيق وبلا راوتر",
 "id":"Kendalikan ESP32 dari Ponselmu - Tanpa Aplikasi, Tanpa Router",
 "ja":"スマホでESP32を操作する - アプリなし、ルーターなし",
 "ru":"Управляй ESP32 с телефона - без приложения и без роутера",
 "vi":"Điều khiển ESP32 bằng điện thoại - không ứng dụng, không router",
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
PREVURL='EP11_URL'
PL={
 "en":"Full course playlist:","tr":"Tüm kurs oynatma listesi:","hi":"पूरे कोर्स की प्लेलिस्ट:","pt":"Playlist do curso completo:","es":"Lista de reproducción del curso completo:","de":"Playlist zum ganzen Kurs:","fr":"Playlist du cours complet :","ar":"قائمة تشغيل الدورة كاملة:","id":"Playlist kursus lengkap:","ja":"コース全体の再生リスト：","ru":"Плейлист всего курса:","vi":"Danh sách phát toàn khóa:",
}
PLID='PLEhjjsUBtWDk'
T={
 "en": [
  "Control your ESP32 from your phone, with no app, no cable and no home Wi-Fi: the board opens its own little network (like the hotspot on your phone), your phone joins it, and a tiny web page on the board becomes your remote. You'll meet softAP, a web page where every button is a link (like a restaurant menu with numbered dishes), the server.on() helpers that answer each link, the note after the question mark (like a note on an order slip) read with server.arg(), and a loop that keeps checking for knocks like a night guard. No new parts: it uses the color LED from episode 6 and the screen and buzzer from episode 10. Plus: the common problems (\"no internet\" and the password length), and your turn: add a party button.",
  ["Tap red, the light turns red","The board opens its own Wi-Fi","The menu page and server.on()","The loop and the order slip","The circuit you already have","Upload, join and tap","The common problems","Your turn"]
 ],
 "tr": [
  "ESP32'yi telefonundan kontrol et: uygulama yok, kablo yok, ev Wi-Fi'ı yok. Kart kendi küçük ağını açıyor (telefonundaki kişisel erişim noktası gibi), telefonun ona bağlanıyor ve kartın içindeki minik bir web sayfası uzaktan kumandan oluyor. softAP ile, her düğmesi bir bağlantı olan bir web sayfasıyla (numaralı yemekleri olan bir restoran menüsü gibi), her bağlantıya cevap veren server.on() yardımcılarıyla, soru işaretinden sonraki notla (sipariş fişindeki not gibi) ve server.arg() ile okunmasıyla, kapıyı çalan var mı diye bakan bir bekçi gibi loop ile tanışacaksın. Yeni parça yok: 6. bölümdeki renkli LED ile 10. bölümdeki ekran ve buzzer yeterli. Ayrıca: yaygın sorunlar (\"internet yok\" uyarısı ve şifre uzunluğu) ve sıra sende: bir parti düğmesi ekle.",
  ["Kırmızıya dokun, ışık kırmızı olsun","Kart kendi Wi-Fi'ını açıyor","Menü sayfası ve server.on()","Döngü ve sipariş fişi","Zaten elindeki devre","Yükle, bağlan ve dokun","Yaygın sorunlar","Sıra sende"]
 ],
 "hi": [
  "अपने ESP32 को फ़ोन से चलाइए: न ऐप, न तार, न घर का वाई-फ़ाई। बोर्ड अपना छोटा नेटवर्क खोलता है (आपके फ़ोन के हॉटस्पॉट जैसा), फ़ोन उससे जुड़ता है, और बोर्ड का नन्हा वेब पेज आपका रिमोट बन जाता है। इसमें मिलेगा softAP, ऐसा वेब पेज जिसका हर बटन एक लिंक है (नंबर वाली डिशों के रेस्टोरेंट मेन्यू जैसा), हर लिंक का जवाब देने वाले server.on() हेल्पर, सवालिया निशान के बाद का नोट (ऑर्डर पर्ची के नोट जैसा) जिसे server.arg() पढ़ता है, और रात के पहरेदार की तरह दस्तक देखता loop। कोई नया पुर्ज़ा नहीं: एपिसोड 6 की रंगीन LED और एपिसोड 10 की स्क्रीन और बज़र काफ़ी हैं। साथ में: आम समस्याएँ (\"इंटरनेट नहीं\" वाला संदेश और पासवर्ड की लंबाई), और आपकी बारी: एक पार्टी बटन जोड़िए।",
  ["लाल दबाइए, बत्ती लाल","बोर्ड अपना वाई-फ़ाई खोलता है","मेन्यू पेज और server.on()","लूप और ऑर्डर पर्ची","आपके पास पहले से मौजूद सर्किट","अपलोड, जुड़ना और दबाना","आम समस्याएँ","आपकी बारी"]
 ],
 "pt": [
  "Controle o ESP32 pelo celular, sem app, sem cabo e sem Wi-Fi de casa: a placa abre a própria redezinha (como o hotspot do celular), o celular entra nela, e uma página web minúscula na placa vira o seu controle remoto. Você vai conhecer o softAP, uma página em que cada botão é um link (como um cardápio de restaurante com pratos numerados), os ajudantes server.on() que respondem a cada link, o bilhete depois da interrogação (como o bilhete de um pedido) lido com server.arg(), e um loop que fica olhando se alguém bate à porta, como um guarda noturno. Sem peças novas: usa o LED de cor do episódio 6 e a tela e o buzzer do episódio 10. Também: os problemas comuns (\"sem internet\" e o tamanho da senha) e sua vez: adicionar um botão festa.",
  ["Toque no vermelho, a luz fica vermelha","A placa abre o próprio Wi-Fi","A página-cardápio e o server.on()","O loop e o bilhete do pedido","O circuito que você já tem","Enviar, conectar e tocar","Os problemas comuns","Sua vez"]
 ],
 "es": [
  "Controla tu ESP32 desde el celular, sin app, sin cable y sin el Wi-Fi de casa: la placa abre su propia redecita (como el hotspot de tu celular), el celular se une a ella, y una página web diminuta en la placa se convierte en tu control remoto. Conocerás softAP, una página donde cada botón es un enlace (como un menú de restaurante con platos numerados), los ayudantes server.on() que responden a cada enlace, la nota después del signo de interrogación (como la nota de un pedido) leída con server.arg(), y un loop que revisa si alguien toca, como un guardia nocturno. Sin piezas nuevas: usa el LED de color del episodio 6 y la pantalla y el zumbador del episodio 10. Además: los problemas comunes (\"sin internet\" y el largo de la contraseña) y tu turno: agregar un botón fiesta.",
  ["Toca rojo y la luz se pone roja","La placa abre su propio Wi-Fi","La página-menú y server.on()","El loop y la nota del pedido","El circuito que ya tienes","Subir, unirse y tocar","Los problemas comunes","Tu turno"]
 ],
 "de": [
  "Steuere deinen ESP32 per Handy, ohne App, ohne Kabel und ohne WLAN zu Hause: Das Board öffnet sein eigenes kleines Netz (wie der Hotspot auf deinem Handy), dein Handy tritt ihm bei, und eine winzige Webseite auf dem Board wird zu deiner Fernbedienung. Du lernst softAP kennen, eine Seite, auf der jeder Button ein Link ist (wie eine Speisekarte mit nummerierten Gerichten), die server.on()-Helfer, die jeden Link beantworten, die Notiz nach dem Fragezeichen (wie eine Notiz auf einem Bestellzettel), die mit server.arg() gelesen wird, und eine Loop, die wie ein Nachtwächter immer wieder nach Klopfzeichen schaut. Keine neuen Teile: Es nutzt die Farb-LED aus Folge 6 und das Display und den Buzzer aus Folge 10. Dazu: die häufigen Probleme (\"kein Internet\" und die Passwortlänge) und du bist dran: einen Party-Button hinzufügen.",
  ["Auf Rot tippen, das Licht wird rot","Das Board öffnet sein eigenes WLAN","Die Menü-Seite und server.on()","Die Loop und der Bestellzettel","Die Schaltung, die du schon hast","Hochladen, verbinden, tippen","Die häufigen Probleme","Du bist dran"]
 ],
 "fr": [
  "Contrôle ton ESP32 depuis ton téléphone, sans appli, sans câble et sans le Wi-Fi de la maison : la carte ouvre son propre petit réseau (comme le point d'accès de ton téléphone), ton téléphone le rejoint, et une toute petite page web sur la carte devient ta télécommande. Tu vas découvrir softAP, une page dont chaque bouton est un lien (comme un menu de restaurant avec des plats numérotés), les assistants server.on() qui répondent à chaque lien, la note après le point d'interrogation (comme une note sur un bon de commande) lue avec server.arg(), et une loop qui vérifie sans cesse si quelqu'un frappe, comme un veilleur de nuit. Aucune pièce nouvelle : il suffit de la LED de couleur de l'épisode 6 et de l'écran et du buzzer de l'épisode 10. En plus : les problèmes courants (\"pas d'Internet\" et la longueur du mot de passe), et à toi : ajouter un bouton fête.",
  ["Touche rouge, la lumière devient rouge","La carte ouvre son propre Wi-Fi","La page-menu et server.on()","La loop et le bon de commande","Le circuit que tu as déjà","Téléverser, rejoindre, toucher","Les problèmes courants","À toi de jouer"]
 ],
 "ar": [
  "تحكّم في ESP32 من هاتفك، بلا تطبيق وبلا كابل وبلا واي فاي المنزل: تفتح اللوحة شبكتها الصغيرة الخاصة (مثل نقطة الاتصال في هاتفك)، وينضم هاتفك إليها، وتصبح صفحة ويب صغيرة على اللوحة جهاز التحكم الخاص بك. ستتعرف على softAP، وعلى صفحة كل زر فيها رابط (مثل قائمة مطعم بأطباق مرقّمة)، ومساعدات server.on() التي تجيب على كل رابط، والملاحظة بعد علامة الاستفهام (مثل ملاحظة على ورقة الطلب) التي تُقرأ بـ server.arg()، وحلقة loop تتفقد الطرق على الباب مثل حارس ليلي. بلا قطع جديدة: تكفي ليد الألوان من الحلقة 6 والشاشة والبازر من الحلقة 10. وأيضًا: المشاكل الشائعة (\"بلا إنترنت\" وطول كلمة المرور)، ودورك: أضف زر حفلة.",
  ["اضغط الأحمر فيصير الضوء أحمر","اللوحة تفتح واي فاي الخاص بها","صفحة القائمة وserver.on()","الحلقة وورقة الطلب","الدارة التي لديك أصلًا","الرفع والانضمام والضغط","المشاكل الشائعة","دورك"]
 ],
 "id": [
  "Kendalikan ESP32 dari ponselmu, tanpa aplikasi, tanpa kabel, dan tanpa Wi-Fi rumah: board membuka jaringan kecilnya sendiri (seperti hotspot di ponselmu), ponselmu bergabung, dan halaman web mungil di board menjadi remote-mu. Kamu akan berkenalan dengan softAP, halaman yang setiap tombolnya adalah tautan (seperti menu restoran dengan hidangan bernomor), pembantu server.on() yang menjawab tiap tautan, catatan setelah tanda tanya (seperti catatan di kertas pesanan) yang dibaca dengan server.arg(), dan loop yang terus memeriksa ketukan seperti penjaga malam. Tanpa komponen baru: cukup LED warna dari episode 6 serta layar dan buzzer dari episode 10. Plus: masalah umum (\"tidak ada internet\" dan panjang kata sandi), dan giliranmu: tambahkan tombol pesta.",
  ["Ketuk merah, lampu jadi merah","Board membuka Wi-Fi sendiri","Halaman menu dan server.on()","Loop dan kertas pesanan","Rangkaian yang sudah kamu punya","Unggah, gabung, dan ketuk","Masalah umum","Giliranmu"]
 ],
 "ja": [
  "ESP32をスマホから操作します。アプリもケーブルも家のWi-Fiもいりません。ボードが自分専用の小さなネットワークを開き（スマホのテザリングのように）、スマホがそこに入り、ボード上の小さなウェブページがリモコンになります。softAP、すべてのボタンがリンクになったページ（番号つきの料理があるレストランのメニューのように）、各リンクに応えるserver.on()のヘルパー、疑問符のあとのメモ（注文伝票のメモのように）をserver.arg()で読むこと、そして夜警のようにノックを確かめ続けるloopを学びます。新しい部品はありません。第6回のカラーLEDと、第10回の画面とブザーを使います。さらに、よくある問題（「インターネットなし」とパスワードの長さ）と、あなたの番：パーティーボタンを足そう。",
  ["赤をタップ、ライトが赤に","ボードが自分のWi-Fiを開く","メニューのページとserver.on()","loopと注文伝票","もう手元にある回路","アップロード、接続、タップ","よくある問題","あなたの番"]
 ],
 "ru": [
  "Управляйте ESP32 с телефона: без приложения, без кабеля и без домашнего Wi-Fi. Плата открывает собственную маленькую сеть (как точка доступа на телефоне), телефон к ней подключается, а крошечная веб-страница на плате становится вашим пультом. Вы познакомитесь с softAP, страницей, где каждая кнопка это ссылка (как меню ресторана с пронумерованными блюдами), помощниками server.on(), которые отвечают на каждую ссылку, запиской после вопросительного знака (как записка на бланке заказа), которую читает server.arg(), и циклом loop, который снова и снова проверяет, не стучится ли кто-то, как ночной сторож. Новых деталей нет: хватит цветного светодиода из эпизода 6 и экрана с зуммером из эпизода 10. Плюс: частые проблемы (\"нет интернета\" и длина пароля) и ваша очередь: добавить кнопку вечеринки.",
  ["Нажми красный, свет станет красным","Плата открывает свой Wi-Fi","Страница-меню и server.on()","Цикл и бланк заказа","Схема, которая у вас уже есть","Загрузить, подключиться, нажать","Частые проблемы","Ваша очередь"]
 ],
 "vi": [
  "Điều khiển ESP32 bằng điện thoại, không ứng dụng, không dây cáp, không cần Wi-Fi nhà: bo mạch mở mạng nhỏ của riêng nó (giống điểm phát sóng trên điện thoại), điện thoại của bạn kết nối vào, và một trang web bé xíu trên bo mạch trở thành điều khiển từ xa của bạn. Bạn sẽ làm quen với softAP, một trang mà mỗi nút là một liên kết (như thực đơn nhà hàng có món đánh số), các trợ thủ server.on() trả lời từng liên kết, ghi chú sau dấu hỏi (như ghi chú trên phiếu gọi món) được đọc bằng server.arg(), và vòng loop liên tục kiểm tra xem có ai gõ cửa như người gác đêm. Không cần linh kiện mới: dùng đèn LED màu của tập 6, màn hình và còi của tập 10. Thêm nữa: các vấn đề thường gặp (\"không có internet\" và độ dài mật khẩu), và đến lượt bạn: thêm một nút tiệc.",
  ["Chạm đỏ, đèn thành đỏ","Bo mạch mở Wi-Fi riêng","Trang thực đơn và server.on()","Vòng loop và phiếu gọi món","Mạch bạn đã có sẵn","Nạp mã, kết nối và chạm","Các vấn đề thường gặp","Đến lượt bạn"]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nCode + lesson: '+repo+'/tree/main/lessons/12-phone-control\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n#ESP32 #Arduino #WiFi #WebServer #Electronics'
TAGS='ESP32 web server, ESP32 control from phone, ESP32 softAP, ESP32 access point, ESP32 WiFi, ESP32 no router, ESP32 WebServer library, ESP32 control LED from phone, ESP32 RGB LED web, ESP32 buzzer web, ESP32 phone remote, ESP32 hotspot, ESP32 without internet, ESP32 project, ESP32 projects for beginners, ESP32 for beginners, ESP32 tutorial, ESP32 From Zero, ESP32 starter kit, ESP32 Arduino IDE, ESP32 OLED'
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
md='# Episode 12 - Phone control: softAP, web page with link buttons, server.on() and URL notes\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Original language: English. Category: Education.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Tags\n\n'+TAGS+'\n'
md+='\n\n## Upload checklist\n\n- Replace EP11_URL with the real episode 11 link, then re-run make_localize.py.\n- Final EN video, four separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('ep12 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
