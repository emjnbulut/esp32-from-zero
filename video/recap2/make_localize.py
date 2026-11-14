"""Recap 2 (episodes 5-10) metadata: regenerate after the final schedule.
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
# Recap without an episode number: titles lead with the search terms and end with the series name.
TAG=' | ESP32 From Zero'
TITLES={
 "en":"ESP32 Recap: PWM, RGB LED, analogRead, map() and State Machines in 7 Questions",
 "tr":"ESP32 Tekrar: PWM, RGB LED, analogRead, map() ve Durum Makineleri, 7 Soruda",
 "hi":"ESP32 Recap: PWM, RGB LED, analogRead, map() और State Machine, 7 सवालों में",
 "pt":"ESP32 Revisão: PWM, LED RGB, analogRead, map() e Máquinas de Estado em 7 Perguntas",
 "es":"ESP32 Repaso: PWM, LED RGB, analogRead, map() y Máquinas de Estado en 7 Preguntas",
 "de":"ESP32 Rückblick: PWM, RGB-LED, analogRead, map() und Zustandsautomaten in 7 Fragen",
 "fr":"ESP32 Récap : PWM, LED RVB, analogRead, map() et machines à états en 7 questions",
 "ar":"ESP32 مراجعة: PWM وLED RGB وanalogRead وmap() وآلات الحالة في 7 أسئلة",
 "id":"ESP32 Rangkuman: PWM, LED RGB, analogRead, map() dan State Machine dalam 7 Soal",
 "ja":"ESP32 総復習：PWM、RGB LED、analogRead、map()、ステートマシンを7問で",
 "ru":"ESP32 Повторение: PWM, RGB-светодиод, analogRead, map() и автоматы за 7 вопросов",
 "vi":"ESP32 Ôn tập: PWM, LED RGB, analogRead, map() và State Machine qua 7 câu hỏi",
}
T={
 "en": [
  "A recap of episodes 5 to 10 in seven questions: how PWM makes a breathing LED, how the color LED mixes light, how analogRead() and map() turn a knob into a number, and how a state machine with goTo() remembers its steps. Grab a paper, pause after every question, and count your points at the end.",
  ["Start","How it works: paper and pause","Part 1: making light (PWM and color LED)","Part 2: reading a knob (analogRead and map)","Part 3: remembering steps (state and the drawer)","Your score and what's next"]
 ],
 "tr": [
  "5. bölümden 10. bölüme kadar yedi soruda bir tekrar: PWM nefes alan LED'i nasıl yapar, renkli LED ışığı nasıl karıştırır, analogRead() ve map() bir düğmeyi nasıl sayıya çevirir ve goTo() ile çalışan durum makinesi adımlarını nasıl hatırlar. Bir kağıt alın, her sorudan sonra videoyu durdurun ve sonda puanlarınızı sayın.",
  ["Başlangıç","Nasıl işliyor: kağıt ve duraklat","Bölüm 1: ışık yapmak (PWM ve renkli LED)","Bölüm 2: düğme okumak (analogRead ve map)","Bölüm 3: adımları hatırlamak (state ve çekmece)","Puanınız ve sırada ne var"]
 ],
 "hi": [
  "episode पाँच से दस का सात सवालों में recap: PWM साँस लेती LED कैसे बनाता है, color LED रोशनी कैसे मिलाती है, analogRead() और map() knob को संख्या कैसे बनाते हैं, और goTo() वाली state machine अपने कदम कैसे याद रखती है। काग़ज़ उठाइए, हर सवाल के बाद वीडियो रोकिए, और आख़िर में अंक गिनिए।",
  ["शुरुआत","कैसे काम करता है: काग़ज़ और pause","हिस्सा 1: रोशनी बनाना (PWM और color LED)","हिस्सा 2: knob पढ़ना (analogRead और map)","हिस्सा 3: कदम याद रखना (state और दराज़)","आपका स्कोर और आगे क्या"]
 ],
 "pt": [
  "Uma revisão dos episódios 5 a 10 em sete perguntas: como o PWM faz um LED respirar, como o LED colorido mistura luz, como analogRead() e map() transformam um knob em número, e como uma máquina de estados com goTo() lembra seus passos. Pegue um papel, pause depois de cada pergunta e conte seus pontos no final.",
  ["Início","Como funciona: papel e pausa","Parte 1: fazer luz (PWM e LED colorido)","Parte 2: ler um knob (analogRead e map)","Parte 3: lembrar passos (state e a gaveta)","Sua pontuação e o que vem depois"]
 ],
 "es": [
  "Un repaso de los episodios 5 al 10 en siete preguntas: cómo el PWM hace respirar un LED, cómo el LED de color mezcla luz, cómo analogRead() y map() convierten una perilla en un número, y cómo una máquina de estados con goTo() recuerda sus pasos. Toma un papel, pausa tras cada pregunta y cuenta tus puntos al final.",
  ["Inicio","Cómo funciona: papel y pausa","Parte 1: hacer luz (PWM y LED de color)","Parte 2: leer una perilla (analogRead y map)","Parte 3: recordar pasos (state y el cajón)","Tu puntaje y lo que sigue"]
 ],
 "de": [
  "Ein Rückblick auf die Episoden 5 bis 10 in sieben Fragen: wie PWM eine atmende LED macht, wie die Farb-LED Licht mischt, wie analogRead() und map() einen Drehknopf in eine Zahl verwandeln und wie ein Zustandsautomat mit goTo() sich seine Schritte merkt. Nimm ein Blatt Papier, pausiere nach jeder Frage und zähle am Ende deine Punkte.",
  ["Start","So funktioniert es: Papier und Pause","Teil 1: Licht erzeugen (PWM und Farb-LED)","Teil 2: einen Drehknopf lesen (analogRead und map)","Teil 3: Schritte merken (state und die Schublade)","Deine Punktzahl und wie es weitergeht"]
 ],
 "fr": [
  "Un récap des épisodes 5 à 10 en sept questions : comment le PWM fait respirer une LED, comment la LED couleur mélange la lumière, comment analogRead() et map() transforment un bouton en nombre, et comment une machine à états avec goTo() se souvient de ses étapes. Prenez une feuille, mettez en pause après chaque question et comptez vos points à la fin.",
  ["Début","Comment ça marche : papier et pause","Partie 1 : fabriquer de la lumière (PWM et LED couleur)","Partie 2 : lire un bouton (analogRead et map)","Partie 3 : se souvenir des étapes (state et le tiroir)","Votre score et la suite"]
 ],
 "ar": [
  "مراجعة للحلقات من 5 إلى 10 في سبعة أسئلة: كيف يصنع PWM مصباح LED يتنفّس، وكيف يمزج LED الملوّن الضوء، وكيف تحوّل analogRead() وmap() مقبضاً إلى رقم، وكيف تتذكّر آلة الحالة مع goTo() خطواتها. أحضر ورقة، وأوقف الفيديو بعد كل سؤال، واحسب نقاطك في النهاية.",
  ["البداية","كيف تعمل: الورقة والإيقاف","الجزء 1: صنع الضوء (PWM وLED الملوّن)","الجزء 2: قراءة مقبض (analogRead وmap)","الجزء 3: تذكّر الخطوات (state والدرج)","نتيجتك وما التالي"]
 ],
 "id": [
  "Rangkuman episode 5 sampai 10 dalam tujuh pertanyaan: bagaimana PWM membuat LED bernapas, bagaimana LED warna mencampur cahaya, bagaimana analogRead() dan map() mengubah knob menjadi angka, dan bagaimana state machine dengan goTo() mengingat langkahnya. Siapkan kertas, jeda setelah setiap pertanyaan, dan hitung poinmu di akhir.",
  ["Mulai","Cara kerjanya: kertas dan jeda","Bagian 1: membuat cahaya (PWM dan LED warna)","Bagian 2: membaca knob (analogRead dan map)","Bagian 3: mengingat langkah (state dan laci)","Skormu dan selanjutnya"]
 ],
 "ja": [
  "第5回から第10回までを7つの問題で総復習します。PWMがどう呼吸するLEDを作るか、カラーLEDがどう光を混ぜるか、analogRead()とmap()がつまみをどう数字にするか、goTo()を使うステートマシンがどうステップを覚えるか。紙を用意し、問題のたびに止めて、最後に点数を数えてください。",
  ["スタート","しくみ：紙と一時停止","パート1：光をつくる（PWMとカラーLED）","パート2：つまみを読む（analogReadとmap）","パート3：ステップを覚える（stateと引き出し）","あなたのスコアと次回"]
 ],
 "ru": [
  "Повторение эпизодов с 5 по 10 в семи вопросах: как PWM делает дышащий светодиод, как цветной светодиод смешивает свет, как analogRead() и map() превращают ручку в число и как автомат состояний с goTo() помнит свои шаги. Возьмите листок, ставьте паузу после каждого вопроса и посчитайте баллы в конце.",
  ["Начало","Как это работает: листок и пауза","Часть 1: создаём свет (PWM и цветной светодиод)","Часть 2: читаем ручку (analogRead и map)","Часть 3: помним шаги (state и ящик)","Ваш результат и что дальше"]
 ],
 "vi": [
  "Ôn tập các tập 5 đến 10 qua bảy câu hỏi: PWM tạo ra LED biết thở thế nào, LED màu trộn ánh sáng ra sao, analogRead() và map() biến núm xoay thành con số thế nào, và state machine với goTo() ghi nhớ các bước ra sao. Hãy lấy giấy, tạm dừng sau mỗi câu hỏi và đếm điểm ở cuối.",
  ["Bắt đầu","Cách hoạt động: giấy và tạm dừng","Phần 1: tạo ra ánh sáng (PWM và LED màu)","Phần 2: đọc núm xoay (analogRead và map)","Phần 3: nhớ các bước (state và ngăn kéo)","Điểm của bạn và tiếp theo"]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nLessons: '+repo+'/tree/main/lessons\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n#ESP32 #Arduino #PWM #Electronics #Recap'
TAGS='ESP32 recap, ESP32 PWM, ESP32 analogWrite, ESP32 RGB LED, ESP32 analogRead, Arduino map function, ESP32 state machine, ESP32 millis, ESP32 Preferences, ESP32 quiz, ESP32 for beginners, ESP32 tutorial, ESP32 From Zero'
loc={}
for lang,(intro,names) in T.items():
    title=TITLES[lang]+TAG
    assert len(names)==len(times)==len(chapters),(lang,len(names))
    assert len(title)<=100,(lang,len(title))
    loc[lang]={'title':title,'description':intro+links+'\n\n'+'\n'.join(t+' '+n for t,n in zip(times,names))+credit}
assert set(loc)==set(TITLES)==set("en tr hi pt es de fr ar id ja ru vi".split())
(here/'localize.json').write_text(json.dumps(loc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
md='# Recap 2: episodes 5-10 (PWM, RGB LED, analogRead, map(), state machines) in 7 questions\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Original language: English. Category: Education.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Tags\n\n'+TAGS+'\n'
md+='\n\n## Upload checklist\n\n- Final EN video, separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('recap2 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
