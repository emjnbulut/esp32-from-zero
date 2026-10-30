"""Source of video/ep05/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, is edited in dub/tr.json).
Spoken text: numbers in words, code names as written. 2026-10-30: wording shortened using measured per-line durations, preserving examples, definitions, limits and questions.
Character counts below are a heuristic; final duration must be checked against the EN/TR slots after new takes.
Usage: python video/ep05/make_dubs.py"""
import json
from pathlib import Path

HI = {
    "s01": "LED धीरे चमकती, फिर मंद होती है, जैसे कोई नींद में साँस ले रहा हो।",
    "s02": "बटन दबाते ही साँस बीच में रुकती है। फिर दबाएँ, तो चलती है।",
    "s03": "Pin सिर्फ़ on या off होता है। आज इसे साँस दिलाने की तरकीब सीखेंगे।",
    "s04": "पिछले पाठ से दो सवाल। अंदरूनी pull-up वाले बटन को दबाएँ, तो pin HIGH पढ़ेगा या LOW?",
    "s05": "LOW। दबाने पर ground, pin ऊपर खींचने वाले कमज़ोर resistor को हरा देता है।",
    "s06": "लंबे delay में बटन का दबना क्यों छूटता है?",
    "s07": "Delay में program रुकता है और बटन नहीं पढ़ता। यही समस्या फिर आएगी।",
    "s08": "Episode चार का circuit लें: GPIO तेईस पर लाल LED, बाईस पर बटन। Multimeter वैकल्पिक है।",
    "s09": "digitalWrite() आम switch जैसा है: पूरा on या पूरा off।",
    "s10": "सिर्फ़ on-off वाला pin आधी रोशनी कैसे देगा? सोचिए।",
    "s11": "जवाब है रफ़्तार। तेज़ पंखे के blades नहीं दिखते, बस धुंधलापन।",
    "s12": "Pin LED को सेकंड में हज़ार बार on-off करता है। आँख औसत देखती है।",
    "s13": "यह PWM, यानी pulse width modulation है। असल में pin तीन दशमलव तीन volt या शून्य देता है। सिर्फ़ timing बदलती है।",
    "s14": "फ़र्क: पंखा बीच से गुज़रता है; LED सिर्फ़ on-off है। बीच की चमक आँख बनाती है।",
    "s15": "हर चक्र में pin जितना हिस्सा on रहे, उसे duty cycle कहते हैं।",
    "s16": "नल हर सेकंड चौथाई खोलें, तो थोड़ा पानी। पूरा खुला छोड़ें, तो पूरी धार।",
    "s17": "फ़र्क: नल आधा खुलता है, PWM नहीं।",
    "s18": "पच्चीस प्रतिशत मंद, पचास मध्यम, सौ पूरा तेज़।",
    "s19": "analogWrite() को pin और शून्य से दो सौ पचपन तक संख्या दें।",
    "s20": "Clicks वाले dimmer जैसा: शून्य off, दो सौ पचपन on। आधी रोशनी की संख्या क्या होगी?",
    "s21": "आधा चक्र on: एक सौ अट्ठाईस। असली dimmer सहज घूमता है; यहाँ दो सौ छप्पन steps हैं।",
    "s23": "pwm_levels में pin तेईस को नाम दें। setup() उसे output बनाता है, Serial Monitor खोलता है।",
    "s24": "अपना showLevel() खाली जगह वाली recipe जैसा है। हर call का नंबर वह जगह भरता है।",
    "s25": "चौंसठ दें: value वही है। analogWrite() दिखाए, print करे, दो सेकंड रुके।",
    "s26": "काग़ज़ से फ़र्क: function पूरा होते ही value भूलता है।",
    "s27": "showLevel() को शून्य, चौंसठ, एक सौ अट्ठाईस, दो सौ पचपन दें। रोकिए: हर step पर LED क्या करेगी?",
    "s28": "चलाएँ: off, मंद, मध्यम, पूरा तेज़। यही चार levels दोहरते हैं।",
    "s29": "Multimeter तेज़ switching नहीं पकड़ता, इसलिए औसत voltage दिखाता है।",
    "s30": "पच्चीस प्रतिशत: शून्य दशमलव आठ volt; पचास: एक दशमलव पैंसठ; सौ: तीन दशमलव तीन। यानी on समय के अनुपात में।",
    "s31": "चौंसठ को दस करें। क्या दिखेगा? हल्की चमक और दशमांश volt।",
    "s32": "दो for loops से साँस बनाएँ: एक हर step पर delay लेकर brightness बढ़ाता है, दूसरा घटाता है।",
    "s34": "Fade में बटन दबाएँ, तो क्या होगा?",
    "s35": "कई बार दबाने पर भी fade चलता है।",
    "s36": "वही delay। जैसे headphones में सीढ़ियाँ चढ़ते हुए ऊपर तक doorbell न सुनना।",
    "s37": "असल में दो सेकंड के fades के बीच बटन पढ़ता है, इसलिए छोटे press छूटते हैं।",
    "s38": "कंधे की थपकी आप महसूस करेंगे; board को loop पूरा होने तक पता नहीं चलता।",
    "s39": "Episode चार की घड़ी हर चक्कर देखें, समय होने पर काम करें।",
    "s40": "हर चार milliseconds brightness एक बढ़ती है। दो सौ पचपन steps लगभग एक सेकंड हैं।",
    "s41": "ऊपर से नीचे गिनें, नीचे फिर मुड़ें: अगली साँस शुरू।",
    "s43": "यह fade_millis है। brightness अभी की रोशनी है। step हर बार जुड़ता है: ऊपर plus एक, नीचे minus एक।",
    "s44": "lastStep पिछला समय रखता है; fading, चलना या रुकना बताता है। नीचे बटन की memory है।",
    "s45": "हर चक्कर घड़ी पढ़ें। नया press fading पलटे; विस्मय चिह्न का मतलब not है।",
    "s46": "दूसरा हिस्सा fade है। रोककर सोचिए: fade चल रहा है, पर सिर्फ़ दो milliseconds हुए। क्या करेगा?",
    "s47": "कुछ नहीं। Loop आगे बढ़कर बटन फिर पढ़ता है, इसलिए press नहीं छूटते।",
    "s48": "चार milliseconds बाद समय लिखें, step जोड़ें। दो सौ पचपन पर minus एक, शून्य पर plus एक।",
    "s49": "analogWrite() चमक दिखाए।",
    "s50": "चलाएँ: साँस लेती LED दबाते ही रुकती है। फिर दबाएँ, तो चलती है।",
    "s51": "Line उनतालीस में चार को दस करें। तेज़ या धीमी?",
    "s52": "धीमी: हर step दस milliseconds; एक तरफ़ ढाई सेकंड।",
    "s53": "रोकिए, अपने शब्दों में कहिए कि बटन अब क्यों चलता है, पहले क्यों नहीं।",
    "s54": "पहला हर step पर रुककर बटन छोड़ देता था। यह घड़ी देखकर आगे बढ़ता है।",
    "s55": "अब PWM से रोशनी घटाना, analogWrite() में शून्य से दो सौ पचपन देना, और बटन सुनता clock-based fade बनाना आता है।",
    "s56": "अगले episode छह में RGB रंग बनाएँगे। Comments में बताइए: किसे साँस दिलाएँगे? फिर मिलेंगे!"
}

PT = {
    "s01": "Olha este LED: clareia e escurece devagar, como alguém respirando enquanto dorme.",
    "s02": "Aperto e ele para no meio da respiração. Outro aperto, e continua.",
    "s03": "O pino só liga ou desliga. Hoje você aprende o truque para fazer um LED respirar.",
    "s04": "Duas perguntas anteriores. O botão usa pull-up interno. Ao apertar, o pino lê HIGH ou LOW?",
    "s05": "LOW. Ao apertar, o terra vence o resistor interno fraco que puxa o pino para cima.",
    "s06": "Pergunta rápida: por que um delay longo faz a placa perder um clique?",
    "s07": "No delay, o programa para e ninguém lê o botão. Hoje isso volta.",
    "s08": "Só precisa do circuito do episódio quatro: o LED vermelho no GPIO vinte e três, e o botão no GPIO vinte e dois. Um multímetro é um bom extra.",
    "s09": "Até agora, digitalWrite() dava duas opções, como um interruptor comum: ligado ou desligado.",
    "s10": "Pergunta rápida: como um pino que só liga e desliga pode deixar um LED com metade do brilho? Pense um pouco.",
    "s11": "A chave é velocidade. Num ventilador rápido, as pás viram um borrão.",
    "s12": "O pino liga e desliga o LED mil vezes por segundo. Você vê a média.",
    "s13": "Esse truque se chama PWM, modulação por largura de pulso. Na prática, o pino está sempre em três vírgula três volts ou em zero volt. Só o tempo muda.",
    "s14": "O ventilador passa pelas posições intermediárias; o LED não. A diferença está no seu olho.",
    "s15": "A fração do ciclo em que o pino fica ligado chama-se ciclo de trabalho.",
    "s16": "Pense numa torneira: aberta um quarto de cada segundo, dá pouca água. Sempre aberta, dá o jato todo.",
    "s17": "A torneira abre pela metade; o pino PWM, não.",
    "s18": "Vinte e cinco por cento fica fraco; cinquenta, médio; cem, máximo.",
    "s19": "analogWrite() recebe um pino e um valor de zero a duzentos e cinquenta e cinco.",
    "s20": "Como um dimmer por passos: zero apaga; duzentos e cinquenta e cinco acende. Qual valor dá meio brilho?",
    "s21": "Meio ciclo: cento e vinte e oito. São duzentos e cinquenta e seis passos, sem giro suave.",
    "s23": "Em pwm_levels, nomeamos o pino vinte e três. setup() o torna saída e abre o Monitor Serial.",
    "s24": "Nossa função showLevel() é uma receita com uma lacuna. Cada chamada preenche com seu número.",
    "s25": "Com sessenta e quatro em showLevel(), value recebe esse número. analogWrite() o usa, o código imprime e espera dois segundos.",
    "s26": "Diferente do papel, a função esquece o valor ao terminar.",
    "s27": "showLevel() recebe zero, sessenta e quatro, cento e vinte e oito e duzentos e cinquenta e cinco. Pause: o que o LED fará?",
    "s28": "Vamos ver: apagado, fraco, médio e máximo. Quatro níveis que se repetem.",
    "s29": "O multímetro não segue o pisca: mostra a tensão média.",
    "s30": "Um quarto ligado dá zero vírgula oito volt; metade dá um vírgula sessenta e cinco; sempre dá três vírgula três.",
    "s31": "Troque sessenta e quatro por dez. O que verá? Luz fraca e um décimo de volt.",
    "s32": "Para respirar, dois loops for: um aumenta o brilho com delay em cada passo; o outro diminui.",
    "s34": "Durante o fade, o que faz o botão?",
    "s35": "Aperto várias vezes, mas o fade continua.",
    "s36": "Volta o delay. Como subir escadas de fone: só lá em cima ouve a campainha.",
    "s37": "Na prática, lê o botão entre fades de dois segundos. Assim perde apertos curtos.",
    "s38": "Você sentiria um toque no ombro; a placa não percebe nada até o loop acabar.",
    "s39": "Use o relógio do episódio quatro: olhe a cada volta e aja na hora certa.",
    "s40": "O brilho sobe um a cada quatro milissegundos. Duzentos e cinquenta e cinco passos dão um segundo.",
    "s41": "No topo, contamos para baixo. Embaixo, viramos de novo e começa outra respiração.",
    "s43": "Este é fade_millis. brightness guarda o brilho atual. step é somado a cada passo: mais um subindo, menos um descendo.",
    "s44": "lastStep guarda a hora anterior; fading, se respira ou está pausado. Abaixo, a memória do botão.",
    "s45": "Lemos o relógio uma vez por volta. Primeiro, o botão: um aperto inverte fading; a exclamação significa não.",
    "s46": "A parte dois faz o fade. Pause: só passaram dois milissegundos, e ele está ativo. O que faz?",
    "s47": "Nada. O loop segue e confere o botão, sem perder apertos.",
    "s48": "A cada quatro milissegundos, marca a hora e soma step. Em duzentos e cinquenta e cinco, desce; em zero, sobe.",
    "s49": "analogWrite() mostra o brilho novo.",
    "s50": "Respira, aperto e para na hora. Outro aperto, e continua.",
    "s51": "Na linha trinta e nove, quatro vira dez. Mais rápido ou devagar?",
    "s52": "Devagar: cada passo leva dez milissegundos; subir leva dois segundos e meio.",
    "s53": "Pause e explique: por que este sketch lê o botão e o primeiro não? Uma frase basta.",
    "s54": "O primeiro esperava em cada passo e não lia o botão. Este olha o relógio e segue.",
    "s55": "Você já usa PWM para regular o brilho, analogWrite() de zero a duzentos e cinquenta e cinco e um fade que escuta o botão.",
    "s56": "Na próxima, vamos misturar RGB. Comente: o que você faria respirar? Até lá!"
}

ES = {
    "s01": "El LED sube y baja su brillo, como alguien que respira dormido.",
    "s02": "Presiono y se para a mitad del respiro. Otra pulsación, y sigue.",
    "s03": "El pin solo se enciende o se apaga. Hoy aprenderás el truco para hacer respirar un LED.",
    "s04": "Dos preguntas anteriores. El botón usa pull-up interno. Al presionarlo, ¿el pin lee HIGH o LOW?",
    "s05": "LOW. Al pulsar, tierra vence la débil resistencia interna que sube el pin.",
    "s06": "¿Por qué un delay largo hace perder un clic?",
    "s07": "Durante un delay nadie lee el botón: el programa está parado. Hoy veremos ese problema otra vez.",
    "s08": "Solo necesitas el circuito del episodio cuatro: el LED rojo en GPIO veintitrés y el botón en GPIO veintidós. Un multímetro es un buen extra.",
    "s09": "Hasta ahora, digitalWrite() daba dos opciones, como un interruptor normal: encendido o apagado.",
    "s10": "¿Cómo da media luz un pin que solo se enciende o se apaga? Piénsalo.",
    "s11": "Un ventilador rápido parece un borrón: no distingues las aspas.",
    "s12": "Con mil encendidos por segundo, tu ojo ve el promedio.",
    "s13": "Es PWM, modulación por ancho de pulso. En realidad, el pin solo da tres coma tres voltios o cero. Cambia el tiempo.",
    "s14": "La diferencia: el ventilador pasa por posiciones intermedias. El LED no; ese término medio lo crea tu ojo.",
    "s15": "La proporción encendida de cada ciclo se llama ciclo de trabajo.",
    "s16": "Una llave abierta un cuarto de cada segundo da poca agua. Siempre abierta, da toda.",
    "s17": "La llave sí abre a medias; el pin PWM nunca.",
    "s18": "Veinticinco por ciento: tenue; cincuenta: medio; cien: máximo.",
    "s19": "Usa analogWrite() con un pin y un valor de cero a doscientos cincuenta y cinco.",
    "s20": "Como una perilla por pasos: cero apaga, doscientos cincuenta y cinco enciende. ¿Y medio brillo?",
    "s21": "Ciento veintiocho: medio ciclo encendido. La perilla gira suave, pero aquí hay doscientos cincuenta y seis pasos.",
    "s23": "En pwm_levels, nombramos el pin veintitrés. setup() lo hace salida e inicia el Monitor Serie.",
    "s24": "Nuestra función showLevel() es una receta con un hueco. Cada llamada lo llena con su número.",
    "s25": "Con showLevel() de sesenta y cuatro, value recibe ese número. analogWrite() lo usa, se imprime y espera dos segundos.",
    "s26": "A diferencia del papel, al terminar olvida el valor.",
    "s27": "showLevel() recibe cero, sesenta y cuatro, ciento veintiocho y doscientos cincuenta y cinco. Pausa: ¿qué hará el LED?",
    "s28": "Probemos: apagado, tenue, medio y máximo. Son cuatro niveles que se repiten.",
    "s29": "El multímetro no sigue la conmutación tan rápida: muestra el voltaje promedio.",
    "s30": "Un cuarto encendido, cero coma ocho voltios; la mitad, uno sesenta y cinco; siempre, tres coma tres.",
    "s31": "Cambia sesenta y cuatro por diez. ¿Qué verás? Luz tenue y una décima de voltio.",
    "s32": "Para hacerlo respirar, dos bucles for: uno aumenta el brillo con delay en cada paso; el otro lo reduce.",
    "s34": "Durante el fade, ¿qué pasa si pulsas?",
    "s35": "Pulso varias veces, pero el fade sigue.",
    "s36": "Es el delay: como subir con audífonos y oír el timbre solo al acabar las escaleras.",
    "s37": "En realidad, lee el botón entre fades de dos segundos. Por eso pierde los pulsos cortos.",
    "s38": "Tú sentirías un toque en el hombro. La placa no nota nada hasta acabar el bucle.",
    "s39": "Usa el reloj del episodio cuatro: míralo cada vuelta y actúa cuando toque.",
    "s40": "Sube uno cada cuatro milisegundos. Doscientos cincuenta y cinco pasos tardan un segundo.",
    "s41": "Arriba, contamos hacia abajo. Abajo, giramos otra vez: empieza otro respiro.",
    "s43": "Este es fade_millis. brightness guarda el brillo actual. step se suma en cada paso: más uno al subir y menos uno al bajar.",
    "s44": "lastStep guarda la hora anterior; fading, si respira o para. Debajo, la memoria del botón.",
    "s45": "Leemos el reloj una vez por vuelta. Primero, el botón: una pulsación invierte fading; la admiración significa no.",
    "s46": "La segunda parte hace el fade. Pausa: solo pasaron dos milisegundos y está activo. ¿Qué hará?",
    "s47": "Nada. Sigue el loop y revisa el botón sin perder pulsaciones.",
    "s48": "Cada cuatro milisegundos, guarda hora y suma step. En doscientos cincuenta y cinco baja; en cero sube.",
    "s49": "analogWrite() muestra el brillo nuevo.",
    "s50": "Respira, pulso y se para al instante. Otra pulsación, y continúa.",
    "s51": "En la línea treinta y nueve, cuatro pasa a diez. ¿Más rápido o lento?",
    "s52": "Más lento: cada paso tarda diez milisegundos; subir lleva dos segundos y medio.",
    "s53": "Pausa y explica en tus palabras: ¿por qué este sketch lee el botón y el anterior no? Basta una frase.",
    "s54": "El primero esperaba en cada paso y no leía el botón. Este mira el reloj y sigue.",
    "s55": "Ya sabes usar PWM para atenuar, analogWrite() con cero a doscientos cincuenta y cinco, y un fade con reloj que escucha al botón.",
    "s56": "En el episodio seis mezclaremos colores RGB. Cuéntame en comentarios: ¿qué harías respirar? ¡Nos vemos!"
}

ep = Path(__file__).parent
script = json.loads((ep / "script.json").read_text(encoding="utf-8"))
ids = [s["id"] for s in script["segments"]]
english = {s["id"]: s["text"] for s in script["segments"]}
TARGET = {"hi": 1.05, "pt": 1.00, "es": 1.00}

out = ep / "dub"
out.mkdir(exist_ok=True)
for lang, voice, seg in (("hi", "hi-IN-MadhurNeural", HI), ("pt", "pt-BR-AntonioNeural", PT), ("es", "es-MX-JorgeNeural", ES)):
    assert list(seg) == ids, (lang, set(ids) ^ set(seg))
    assert len(seg) == 53, (lang, len(seg))
    (out / f"{lang}.json").write_text(json.dumps({"voice": voice, "rate": "+0%", "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
print("dubs written:", len(ids), "segments each")

# Length check: a dub line may not take longer to say than the English line.
bad = 0
for lang, seg in (("hi", HI), ("pt", PT), ("es", ES)):
    ratios = {k: len(seg[k]) / len(english[k]) for k in ids}
    worst = max(ratios, key=ratios.get)
    print(f"{lang}: max {ratios[worst]:.2f} ({worst}), mean {sum(ratios.values()) / len(ratios):.2f}, target <= {TARGET[lang]:.2f}")
    for k in ids:
        if ratios[k] > TARGET[lang]:
            bad += 1
            print(f"  OVER {k}: {ratios[k]:.2f} ({len(seg[k])} vs {len(english[k])})")
print("length check:", "OK" if not bad else f"{bad} line(s) over target")
