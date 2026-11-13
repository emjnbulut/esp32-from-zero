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
# Titles lead with the search term (channel analytics, 3 Nov 2026); every title ends with the series tag.
TAG=' | ESP32 From Zero #10'
TITLES={
 "en":"ESP32 Reflex Game: a Record that Survives Power Off (Preferences)",
 "tr":"ESP32 Refleks Oyunu: Elektrik Kesilse de Kalan Rekor (Preferences)",
 "hi":"ESP32 Reflex Game: बिजली जाने पर भी बचा रहे रिकॉर्ड (Preferences)",
 "pt":"ESP32 Jogo de Reflexo: Recorde que Sobrevive sem Energia (Preferences)",
 "es":"ESP32 Juego de Reflejos: Récord que Sobrevive sin Energía (Preferences)",
 "de":"ESP32 Reaktionsspiel: Rekord, der den Stromausfall überlebt (Preferences)",
 "fr":"ESP32 Jeu de réflexes : un record qui survit sans courant (Preferences)",
 "ar":"ESP32 لعبة ردّ الفعل: رقم قياسي يبقى بعد انقطاع الكهرباء (Preferences)",
 "id":"ESP32 Game Refleks: Rekor yang Bertahan Saat Mati Listrik (Preferences)",
 "ja":"ESP32 反射神経ゲーム：電源を切っても残る記録 (Preferences)",
 "ru":"ESP32 игра на реакцию: рекорд после отключения питания (Preferences)",
 "vi":"ESP32 trò chơi phản xạ: kỷ lục còn mãi khi mất điện (Preferences)",
}
T={
 "en": [
  "Our first project finished: a reflex game. Red, yellow, then green, and you press as fast as you can. The reaction time is just the time spent in one step, the color LED shows how you did, and your best time is saved with Preferences, so it survives unplugging the board. Plus: the common mistake of saving every result, and your turn: a false start.",
  ["The reflex game in action","Recall: goTo() and the color LED","The plan: rules and no new wire","The idea: five steps and a parking ticket","reflex_game code tour","Steps 0 to 2: red and yellow","Step 3: measuring the reaction","Modify: 250 to 200","Why the record disappears","Preferences: the drawer","Common mistake: saving every result","Your turn: false start","Recap and next lesson"]
 ],
 "tr": [
  "İlk projemiz tamam: bir refleks oyunu. Kırmızı, sarı, sonra yeşil; olabildiğince hızlı basıyorsunuz. Tepki süresi yalnızca tek bir adımda geçen süre, üç renkli LED nasıl yaptığınızı gösteriyor ve en iyi süreniz Preferences ile kaydediliyor; yani kartı fişten çeksiniz de kalıyor. Ayrıca: her sonucu kaydetme hatası ve sıra sizde: erken başlama.",
  ["Refleks oyunu iş başında","Hatırlatma: goTo() ve üç renkli LED","Plan: kurallar ve yeni kablo yok","Fikir: beş adım ve bir otopark bileti","reflex_game kod turu","0'dan 2'ye adımlar: kırmızı ve sarı","Adım 3: tepkiyi ölçmek","Değiştir: 250'den 200'e","Rekor neden kayboluyor","Preferences: çekmece","Yaygın hata: her sonucu kaydetmek","Sıra sizde: erken başlama","Özet ve sonraki ders"]
 ],
 "hi": [
  "हमारा पहला project पूरा: एक reflex game। लाल, पीली, फिर हरी, और आप जितनी तेज़ हो सके दबाते हैं। reaction time बस एक कदम में बीता समय है, color LED बताती है कि आपने कैसा किया, और बेस्ट टाइम Preferences से सहेजा जाता है, इसलिए board निकालने पर भी बचा रहता है। साथ में: हर नतीजा सहेजने की आम गलती और आपकी बारी: ग़लत शुरुआत।",
  ["Reflex game चलता हुआ","दोहराव: goTo() और color LED","योजना: नियम और कोई नया तार नहीं","विचार: पाँच कदम और पार्किंग टिकट","reflex_game कोड","कदम शून्य से दो: लाल और पीली","कदम तीन: reaction नापना","बदलाव: 250 से 200","रिकॉर्ड क्यों गायब होता है","Preferences: दराज़","आम गलती: हर नतीजा सहेजना","आपकी बारी: ग़लत शुरुआत","सारांश और अगला पाठ"]
 ],
 "pt": [
  "Nosso primeiro projeto pronto: um jogo de reflexo. Vermelho, amarelo, depois verde, e você aperta o mais rápido que puder. O tempo de reação é só o tempo em um passo, o LED colorido mostra como você foi, e seu melhor tempo é salvo com Preferences, então sobrevive a desligar a placa. Também: o erro comum de salvar todo resultado e sua vez: a largada falsa.",
  ["O jogo de reflexo em ação","Revisão: goTo() e o LED colorido","O plano: regras e nenhum fio novo","A ideia: cinco passos e um ticket","Código reflex_game","Passos 0 a 2: vermelho e amarelo","Passo 3: medir a reação","Modifique: 250 para 200","Por que o recorde some","Preferences: a gaveta","Erro comum: salvar todo resultado","Sua vez: largada falsa","Resumo e próxima aula"]
 ],
 "es": [
  "Nuestro primer proyecto terminado: un juego de reflejos. Rojo, amarillo, luego verde, y pulsas lo más rápido que puedas. El tiempo de reacción es solo el tiempo en un paso, el LED de color muestra cómo lo hiciste, y tu mejor tiempo se guarda con Preferences, así sobrevive a desconectar la placa. Además: el error común de guardar cada resultado y tu turno: la salida falsa.",
  ["El juego de reflejos en acción","Repaso: goTo() y el LED de color","El plan: reglas y ningún cable nuevo","La idea: cinco pasos y un ticket","Código reflex_game","Pasos 0 a 2: rojo y amarillo","Paso 3: medir la reacción","Modifica: de 250 a 200","Por qué desaparece el récord","Preferences: el cajón","Error común: guardar cada resultado","Tu turno: salida falsa","Resumen y próxima lección"]
 ],
 "de": [
  "Unser erstes Projekt ist fertig: ein Reaktionsspiel. Rot, Gelb, dann Grün, und du drückst so schnell du kannst. Die Reaktionszeit ist nur die Zeit in einem Schritt, die Farb-LED zeigt, wie du warst, und deine Bestzeit wird mit Preferences gespeichert und überlebt das Abziehen des Boards. Dazu: der häufige Fehler, jedes Ergebnis zu speichern, und deine Aufgabe: ein Fehlstart.",
  ["Das Reaktionsspiel in Aktion","Rückblick: goTo() und die Farb-LED","Der Plan: Regeln und kein neues Kabel","Die Idee: fünf Schritte und ein Parkschein","reflex_game erklärt","Schritte 0 bis 2: Rot und Gelb","Schritt 3: die Reaktion messen","Ändern: 250 zu 200","Warum der Rekord verschwindet","Preferences: die Schublade","Häufiger Fehler: jedes Ergebnis speichern","Deine Aufgabe: Fehlstart","Rückblick und nächste Lektion"]
 ],
 "fr": [
  "Notre premier projet terminé : un jeu de réflexes. Rouge, jaune, puis vert, et vous appuyez aussi vite que possible. Le temps de réaction n'est que le temps passé dans une étape, la LED couleur montre votre performance, et votre meilleur temps est enregistré avec Preferences, donc il survit au débranchement de la carte. Et aussi : l'erreur classique d'enregistrer chaque résultat et votre défi : le faux départ.",
  ["Le jeu de réflexes en action","Rappel : goTo() et la LED couleur","Le plan : règles et aucun fil neuf","L'idée : cinq étapes et un ticket","Le code reflex_game","Étapes 0 à 2 : rouge et jaune","Étape 3 : mesurer la réaction","Modifier : 250 vers 200","Pourquoi le record disparaît","Preferences : le tiroir","Erreur courante : tout enregistrer","À vous : le faux départ","Bilan et prochain cours"]
 ],
 "ar": [
  "انتهى مشروعنا الأول: لعبة ردّ الفعل. أحمر ثم أصفر ثم أخضر، وتضغط بأسرع ما تستطيع. زمن ردّ الفعل هو الوقت في خطوة واحدة فقط، ويُظهر LED الملوّن أداءك، ويُحفظ أفضل وقت لك باستخدام Preferences فيبقى حتى بعد فصل اللوحة. مع الخطأ الشائع بحفظ كل نتيجة، وتحديك: البداية الخاطئة.",
  ["لعبة ردّ الفعل أثناء العمل","مراجعة: goTo() وLED الملوّن","الخطة: القواعد بلا أسلاك جديدة","الفكرة: خمس خطوات وتذكرة موقف","شرح reflex_game","الخطوات 0 إلى 2: الأحمر والأصفر","الخطوة 3: قياس ردّ الفعل","تعديل: من 250 إلى 200","لماذا يختفي الرقم القياسي","Preferences: الدرج","خطأ شائع: حفظ كل نتيجة","دورك: البداية الخاطئة","ملخص والدرس القادم"]
 ],
 "id": [
  "Proyek pertama kita selesai: game refleks. Merah, kuning, lalu hijau, dan kamu menekan secepat mungkin. Waktu reaksi hanyalah waktu di satu langkah, LED warna menunjukkan hasilmu, dan waktu terbaikmu disimpan dengan Preferences, jadi tetap ada setelah board dicabut. Plus: kesalahan umum menyimpan setiap hasil, dan giliranmu: false start.",
  ["Game refleks beraksi","Ulasan: goTo() dan LED warna","Rencana: aturan tanpa kabel baru","Idenya: lima langkah dan karcis parkir","Kode reflex_game","Langkah 0 sampai 2: merah dan kuning","Langkah 3: mengukur reaksi","Ubah: 250 jadi 200","Mengapa rekor hilang","Preferences: laci","Kesalahan umum: menyimpan setiap hasil","Giliranmu: false start","Ringkasan dan pelajaran berikut"]
 ],
 "ja": [
  "最初のプロジェクトが完成：反射神経ゲームです。赤、黄、そして緑、できるだけ速く押します。反応時間は1つのステップで過ごした時間にすぎず、カラーLEDが結果を表し、ベストタイムはPreferencesで保存されるので、ボードを抜いても残ります。さらに、毎回結果を保存してしまうよくある間違いと、課題：フライング。",
  ["動く反射神経ゲーム","復習：goTo()とカラーLED","計画：ルールと新しい配線なし","アイデア：5つのステップと駐車券","reflex_gameのコード","ステップ0から2：赤と黄","ステップ3：反応を測る","変更：250から200へ","記録が消える理由","Preferences：引き出し","よくある間違い：毎回保存する","課題：フライング","まとめと次のレッスン"]
 ],
 "ru": [
  "Наш первый проект готов: игра на реакцию. Красный, жёлтый, потом зелёный, и вы жмёте как можно быстрее. Время реакции это просто время в одном шаге, цветной светодиод показывает результат, а лучшее время сохраняется через Preferences и переживает отключение платы. А ещё: частая ошибка сохранять каждый результат и ваше задание: фальстарт.",
  ["Игра на реакцию в действии","Повторение: goTo() и цветной светодиод","План: правила и никаких новых проводов","Идея: пять шагов и парковочный талон","Разбор reflex_game","Шаги 0 до 2: красный и жёлтый","Шаг 3: измеряем реакцию","Правка: от 250 к 200","Почему рекорд пропадает","Preferences: ящик","Частая ошибка: сохранять каждый результат","Ваше задание: фальстарт","Итоги и следующий урок"]
 ],
 "vi": [
  "Dự án đầu tiên đã xong: một trò chơi phản xạ. Đỏ, vàng, rồi xanh, và bạn nhấn nhanh nhất có thể. Thời gian phản xạ chỉ là thời gian trong một bước, LED màu cho biết bạn làm thế nào, và thời gian tốt nhất được lưu bằng Preferences nên còn nguyên khi rút board. Cùng lỗi hay gặp là lưu mọi kết quả, và thử thách: xuất phát sớm.",
  ["Trò chơi phản xạ hoạt động","Ôn tập: goTo() và LED màu","Kế hoạch: luật chơi, không dây mới","Ý tưởng: năm bước và vé gửi xe","Mã reflex_game","Bước 0 đến 2: đỏ và vàng","Bước 3: đo phản xạ","Thay đổi: từ 250 thành 200","Vì sao kỷ lục biến mất","Preferences: ngăn kéo","Lỗi thường gặp: lưu mọi kết quả","Đến lượt bạn: xuất phát sớm","Tóm tắt và bài tiếp theo"]
 ]
}
repo='https://github.com/emjnbulut/esp32-from-zero'
links='\n\nCode + lesson: '+repo+'/tree/main/lessons/10-reflex-game\nLearning Lab: https://emjnbulut.github.io/esp32-learning-lab/\nCourse source: '+repo
credit='\n\nMusic: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nNarration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n#ESP32 #Arduino #ReflexGame #Preferences #Electronics'
TAGS='ESP32 reflex game, ESP32 Preferences, ESP32 save data power off, ESP32 getULong putULong, ESP32 reaction time, ESP32 state machine, ESP32 millis, ESP32 RGB LED, ESP32 for beginners, ESP32 projects, Arduino reflex game, ESP32 tutorial, ESP32 From Zero'
loc={}
for lang,(intro,names) in T.items():
    title=TITLES[lang]+TAG
    assert len(names)==len(times)==len(chapters),(lang,len(names))
    assert len(title)<=100,(lang,len(title))
    loc[lang]={'title':title,'description':intro+links+'\n\n'+'\n'.join(t+' '+n for t,n in zip(times,names))+credit}
assert set(loc)==set(TITLES)==set("en tr hi pt es de fr ar id ja ru vi".split())
(here/'localize.json').write_text(json.dumps(loc,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
md='# Episode 10 - Mini Project 1: a Reflex Game with a Record that Survives Power Off\n\nChapter times: '+('PROVISIONAL; regenerate after final schedule.' if provisional else 'generated from final schedule with the channel bumper offset.')+'\n\n'
md+='Original language: English. Category: Education.\n\n'
md+='## English\n\n'+loc['en']['title']+'\n\n'+loc['en']['description']+'\n\n## Turkish\n\n'+loc['tr']['title']+'\n\n'+loc['tr']['description']
md+='\n\n## Tags\n\n'+TAGS+'\n'
md+='\n\n## Upload checklist\n\n- Final EN video, four separate dub tracks, 12 subtitle languages.\n- Re-run make_localize.py after all narration and final schedule.\n- Review final video/audio and thumbnail before uploading.\n'
(here/'youtube.md').write_text(md,encoding='utf-8')
print('ep10 metadata:',len(loc),'languages;', 'PROVISIONAL' if provisional else 'final schedule',times)
