"""Source of video/ep05/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, is edited in dub/tr.json).
Spoken text: numbers in words, code names as written. Every line must be no longer than the English
narration (es/pt <= 1.00x, hi <= 1.05x characters), because dubs are never sped up.
Usage: python video/ep05/make_dubs.py"""
import json
from pathlib import Path

HI = {
    "s01": "इस LED को देखिए। यह धीरे-धीरे तेज़ होती है, फिर धीमी, बार-बार, जैसे कोई नींद में साँस ले रहा हो।",
    "s02": "और बटन दबाते ही यह तुरंत रुक जाती है, साँस के ठीक बीच में। फिर दबाएँ, तो यह चल पड़ती है।",
    "s03": "पर यह pin या तो पूरा on हो सकता है, या पूरा off। इस video के अंत तक आप तरकीब जान लेंगे, और हर LED को साँस दिला देंगे।",
    "s04": "शुरू करने से पहले, पिछले episodes से दो सवाल। छोटा सवाल: बटन अंदर वाला pull-up resistor इस्तेमाल करता है। दबाने पर pin HIGH पढ़ता है या LOW?",
    "s05": "LOW। दबाने से pin ground से जुड़ता है, और ground चिप के अंदर उस कमज़ोर resistor से जीत जाता है जो उसे ऊपर खींचता है।",
    "s06": "छोटा सवाल: लंबे delay में board बटन का दबना क्यों चूक जाता है?",
    "s07": "क्योंकि delay के दौरान program बस रुक जाता है, और बटन को कोई नहीं देखता। इसे याद रखिए: आज यह फिर आएगा।",
    "s08": "बस episode चार का circuit चाहिए: GPIO तेईस पर लाल LED, और GPIO बाईस पर बटन। Multimeter हो, तो और अच्छा।",
    "s09": "अब तक digitalWrite() ने, आम light switch की तरह, दो ही विकल्प दिए: पूरा on, या पूरा off।",
    "s10": "छोटा सवाल: जो pin सिर्फ़ on या off होता है, वह LED को आधी रोशनी पर कैसे जलाए? एक पल सोचिए।",
    "s11": "जवाब है रफ़्तार। छत के पंखे को सोचिए। तेज़ घूमने पर उसके blades अलग नहीं दिखते, बस एक हल्का धुंधलापन।",
    "s12": "Pin रोशनी के साथ यही करता है। वह LED को सेकंड में लगभग हज़ार बार on-off करता है, और आँख को बस औसत दिखता है।",
    "s13": "इस तरकीब को PWM कहते हैं, यानी pulse width modulation। असल में pin हमेशा या तो तीन दशमलव तीन volt पर होता है, या शून्य पर। बदलती है बस timing।",
    "s14": "पंखे से फ़र्क: पंखा सच में बीच की हर जगह से गुज़रता है। LED बस पूरी on या पूरी off होती है, और बीच का हिस्सा आपकी आँख में बनता है।",
    "s15": "हम तय करते हैं कि हर छोटे चक्र में pin कितनी देर on रहे। इस हिस्से को duty cycle कहते हैं।",
    "s16": "एक नल सोचिए, जिसे आप हर सेकंड थोड़ी देर खोलते हैं। हर सेकंड का चौथाई खोलें, तो थोड़ा पानी बहता है। खुला छोड़ दें, तो पूरी धार।",
    "s17": "फ़र्क यह है: असली नल आधा खुल सकता है, पर PWM pin कभी आधा on नहीं होता।",
    "s18": "तो पच्चीस प्रतिशत on मंद दिखता है, पचास मध्यम, और सौ प्रतिशत पूरी तेज़।",
    "s19": "Code में यह सब एक function है: analogWrite()। इसे एक pin दीजिए, और शून्य से दो सौ पचपन तक की कोई संख्या।",
    "s20": "यह कई छोटे clicks वाले dimmer knob जैसा है: शून्य हमेशा off, और दो सौ पचपन हमेशा on। छोटा सवाल: लगभग आधी रोशनी कौन सी संख्या देगी?",
    "s21": "लगभग एक सौ अट्ठाईस, हर चक्र का आधा on। असली dimmer से फ़र्क: वह आराम से घूमता है, पर इसमें ठीक दो सौ छप्पन steps हैं।",
    "s23": "यह रहा पहला sketch, pwm_levels। सबसे ऊपर pin तेईस को एक नाम मिलता है। setup() उसे output बनाता है, और Serial Monitor शुरू करता है।",
    "s24": "फिर कुछ नया: हमारा अपना function, showLevel()। इसे खाली जगह वाली recipe समझिए: brackets वाली संख्या हर call पर वह जगह भरती है।",
    "s25": "असल में होता यह है: showLevel() को चौंसठ के साथ call करें, तो function के अंदर value चौंसठ हो जाती है। analogWrite() उसे लेता है, sketch उसे print करता है, फिर दो सेकंड रुकता है।",
    "s26": "काग़ज़ की recipe से फ़र्क: function ख़त्म होते ही value भूल जाता है।",
    "s27": "Loop showLevel() को चार बार call करता है: शून्य, चौंसठ, एक सौ अट्ठाईस, और दो सौ पचपन के साथ। Video रोकिए और अंदाज़ा लगाइए: हर step पर LED क्या करेगी?",
    "s28": "चलाते हैं। LED चार साफ़ levels में बढ़ती है: off, मंद, मध्यम, और पूरी तेज़। फिर शुरू से दोबारा।",
    "s29": "अब LED pin पर multimeter। वह switching के साथ नहीं चल पाता, इसलिए औसत voltage दिखाता है।",
    "s30": "पच्चीस प्रतिशत पर लगभग शून्य दशमलव आठ volt, पचास पर एक दशमलव पैंसठ, और सौ पर तीन दशमलव तीन: ठीक उतना, जितना समय pin on रहता है।",
    "s31": "आपकी बारी: चौंसठ की जगह दस लिखिए। आपको क्या दिखेगा? बहुत हल्की चमक, और volt का लगभग दसवाँ हिस्सा।",
    "s32": "अब LED को साँस दिलाते हैं। सीधा तरीका है दो for loops। एक हर step पर छोटे delay के साथ brightness ऊपर गिनता है, दूसरा नीचे।",
    "s34": "छोटा सवाल: जब यह LED fade हो रही हो, तब बटन दबाने पर क्या होगा?",
    "s35": "देखिए। मैं तीन, चार बार दबाता हूँ, और fade चलता रहता है, जैसे कुछ हुआ ही न हो।",
    "s36": "यह इस video की शुरुआत वाली delay की समस्या है। जैसे headphones लगाकर सीढ़ियाँ चढ़ना: ऊपर पहुँचने तक doorbell सुनाई नहीं देती।",
    "s37": "असल में होता यह है: एक पूरा fade लगभग दो सेकंड लेता है, और बटन बस दो fades के बीच पढ़ा जाता है। इसलिए छोटा press लगभग हमेशा छूट जाता है।",
    "s38": "फ़र्क यह है: कंधे पर थपकी तो आप शायद फिर भी महसूस करें, पर loop ख़त्म होने तक board को कुछ पता नहीं चलता।",
    "s39": "हल है episode चार वाली दीवार घड़ी। हम हर चक्कर में उस पर नज़र डालते हैं, और तभी कुछ करते हैं जब काफ़ी समय बीत जाए।",
    "s40": "हर चार milliseconds में हम एक छोटा step लेते हैं, और brightness एक बढ़ती है। दो सौ पचपन steps में लगभग एक सेकंड लगता है।",
    "s41": "ऊपर पहुँचकर हम मुड़ते हैं और नीचे गिनते हैं। नीचे फिर मुड़ते हैं, और अगली साँस शुरू होती है।",
    "s43": "यह रहा पूरा sketch, fade_millis। brightness बताता है कि LED अभी कितनी तेज़ है। step वह है जो हम हर बार जोड़ते हैं: ऊपर जाते हुए plus एक, नीचे आते हुए minus एक।",
    "s44": "lastStep पिछले step का समय रखता है, और fading बताता है कि LED साँस ले रही है या रुकी है। इनके नीचे episode चार वाली बटन की memory है।",
    "s45": "Loop में हम घड़ी एक बार पढ़ते हैं। पहला हिस्सा episode चार वाला बटन है। नया press fading को उलट देता है, क्योंकि exclamation mark का मतलब है not।",
    "s46": "दूसरा हिस्सा fade है। Video रोकिए और अंदाज़ा लगाइए: LED साँस ले रही है, पर सिर्फ़ दो milliseconds बीते हैं। यह हिस्सा क्या करेगा?",
    "s47": "कुछ भी नहीं। Loop बस आगे चलता है और फिर से बटन देखता है, इसीलिए कोई press कभी नहीं छूटता।",
    "s48": "चार milliseconds बीतने पर हम समय नोट करते हैं, और step को brightness में जोड़ते हैं। दो सौ पचपन पर step minus एक बनता है, और शून्य पर फिर plus एक।",
    "s49": "आख़िर में analogWrite() नई brightness LED पर दिखाता है।",
    "s50": "चलाते हैं। LED साँस लेती है, और press करते ही fade के बीच में तुरंत रुक जाती है। फिर दबाएँ, तो चल पड़ती है।",
    "s51": "छोटा सवाल: line उनतालीस में हम चार को दस कर दें। साँस तेज़ होगी, या धीमी?",
    "s52": "धीमी। अब हर step दस milliseconds रुकता है, तो एक तरफ़ जाने में लगभग ढाई सेकंड लगते हैं, और साँस शांत लगती है।",
    "s53": "अब video रोकिए, और अपने शब्दों में समझाइए कि बटन इस sketch में क्यों चलता है, पर पहले में नहीं। एक-दो वाक्य काफ़ी हैं।",
    "s54": "एक तरह से कहें तो: पहला sketch हर step पर रुकता था, तो बटन कोई नहीं पढ़ता था। यह कभी नहीं रुकता: घड़ी देखता है, और आगे बढ़ जाता है।",
    "s55": "आज आपने तीन बातें सीखीं। PWM बहुत तेज़ switching से LED को मंद करता है। analogWrite() शून्य से दो सौ पचपन तक की संख्या लेता है। और घड़ी पर बना fade कभी सुनना नहीं छोड़ता।",
    "s56": "अगली बार, episode छह में, हम RGB LED से आपकी पसंद का कोई भी रंग बनाएँगे। तब तक comments में बताइए: आप किसे साँस दिलाना चाहेंगे? फिर मिलते हैं!",
}

PT = {
    "s01": "Olha este LED. Ele brilha devagar, depois enfraquece, sem parar, como alguém respirando enquanto dorme.",
    "s02": "E quando aperto o botão, ele para na hora, bem no meio de uma respiração. Aperto de novo, e ele continua.",
    "s03": "Mas este pino só fica ligado ou desligado. No fim do vídeo, você vai saber o truque e fazer qualquer LED respirar.",
    "s04": "Antes de começar, duas perguntas dos episódios anteriores. Pergunta rápida: o botão usa o resistor de pull-up interno. Enquanto você aperta, o pino lê HIGH ou LOW?",
    "s05": "LOW. Apertar liga o pino ao terra, e o terra vence o resistor fraco dentro do chip que puxa o pino para cima.",
    "s06": "Pergunta rápida: por que um delay longo faz a placa perder um clique?",
    "s07": "Porque durante um delay, o programa simplesmente para, e ninguém olha o botão. Guarde isso: hoje ele volta.",
    "s08": "Só precisa do circuito do episódio quatro: o LED vermelho no GPIO vinte e três, e o botão no GPIO vinte e dois. Um multímetro é um bom extra.",
    "s09": "Até agora, digitalWrite() dava duas opções, como um interruptor comum: ligado ou desligado.",
    "s10": "Pergunta rápida: como um pino que só liga e desliga pode deixar um LED com metade do brilho? Pense um pouco.",
    "s11": "A resposta é velocidade. Pense num ventilador de teto. Girando rápido, você não vê mais as pás, só um borrão suave.",
    "s12": "O pino faz o mesmo com a luz. Ele liga e desliga o LED umas mil vezes por segundo, e seu olho só vê a média.",
    "s13": "Esse truque se chama PWM, modulação por largura de pulso. Na prática, o pino está sempre em três vírgula três volts ou em zero volt. Só o tempo muda.",
    "s14": "A diferença do ventilador: ele passa mesmo por todas as posições do meio. O LED só fica todo ligado ou todo desligado, e o meio-termo acontece no seu olho.",
    "s15": "Controlamos quanto tempo o pino fica ligado em cada ciclo curto. Essa fração é o ciclo de trabalho.",
    "s16": "Pense numa torneira que você abre rapidinho a cada segundo. Aberta um quarto de cada segundo, sai pouca água. Deixe aberta, e vem o jato todo.",
    "s17": "A diferença: uma torneira abre pela metade, mas um pino PWM, nunca.",
    "s18": "Então vinte e cinco por cento fica fraco, cinquenta, médio, e cem por cento, brilho total.",
    "s19": "No código, tudo isso é uma função: analogWrite(). Você passa um pino e um número de zero a duzentos e cinquenta e cinco.",
    "s20": "É como um dimmer com muitos cliques: zero é sempre desligado, e duzentos e cinquenta e cinco, sempre ligado. Pergunta rápida: qual número dá meio brilho?",
    "s21": "Uns cento e vinte e oito, ligado metade de cada ciclo. A diferença do dimmer real: ele gira suave, mas este tem exatamente duzentos e cinquenta e seis passos.",
    "s23": "Aqui está o primeiro sketch, pwm_levels. No topo, o pino vinte e três ganha um nome. O setup() o torna saída e liga o Monitor Serial.",
    "s24": "Depois, algo novo: nossa própria função, showLevel(). É como uma receita com uma lacuna: o número entre parênteses a preenche a cada chamada.",
    "s25": "Na prática: quando chamamos showLevel() com sessenta e quatro, o valor dentro da função vira sessenta e quatro. O analogWrite() usa esse valor, o sketch imprime, e espera dois segundos.",
    "s26": "A diferença de uma receita no papel: a função esquece o valor assim que termina.",
    "s27": "O loop chama showLevel() com zero, sessenta e quatro, cento e vinte e oito e duzentos e cinquenta e cinco. Pause o vídeo: o que o LED faz em cada passo?",
    "s28": "Vamos rodar. O LED sobe em quatro níveis claros: apagado, fraco, médio e brilho total. Depois começa de novo.",
    "s29": "Agora, um multímetro no pino do LED. Lento demais para seguir o pisca, ele mostra a tensão média.",
    "s30": "Uns zero vírgula oito volt em vinte e cinco por cento, um vírgula sessenta e cinco em cinquenta, e três vírgula três em cem: o tempo que o pino fica ligado.",
    "s31": "Sua vez: troque sessenta e quatro por dez. O que você vai ver? Um brilho bem fraquinho, e um décimo de volt.",
    "s32": "Agora vamos fazer o LED respirar. O jeito óbvio são dois loops for. Um sobe o brilho com um pequeno delay a cada passo, e o outro desce.",
    "s34": "Pergunta rápida: durante o fade, o que acontece se você apertar o botão?",
    "s35": "Olha. Aperto três, quatro vezes, e o fade continua, como se nada fosse.",
    "s36": "É o problema do delay do começo do vídeo. É como subir a escada de fone de ouvido: até chegar lá em cima, você não ouve a campainha.",
    "s37": "Na prática: um fade inteiro leva uns dois segundos, e o botão só é lido entre dois fades. Então um aperto curto quase sempre se perde.",
    "s38": "A diferença: você ainda sentiria um toque no ombro, mas a placa não percebe nada até o loop acabar.",
    "s39": "A solução é o relógio de parede do episódio quatro. Olhamos ele a cada volta e só agimos se passou tempo bastante.",
    "s40": "A cada quatro milissegundos, damos um passinho, e o brilho sobe um. Duzentos e cinquenta e cinco passos levam cerca de um segundo.",
    "s41": "No topo, damos meia-volta e contamos para baixo. Embaixo, viramos de novo, e começa a próxima respiração.",
    "s43": "Aqui está o sketch inteiro, fade_millis. brightness é o brilho atual do LED. step é o que somamos a cada vez: mais um subindo, menos um descendo.",
    "s44": "lastStep guarda a hora do último passo, e fading diz se o LED respira ou está pausado. Logo abaixo fica a memória do botão do episódio quatro.",
    "s45": "No loop, lemos o relógio uma vez. A parte um é o botão do episódio quatro. Um novo aperto inverte fading: o ponto de exclamação quer dizer não.",
    "s46": "A parte dois é o fade. Pause o vídeo e preveja: o LED está respirando, mas só passaram dois milissegundos. O que esta parte faz?",
    "s47": "Nada. O loop só segue em frente e confere o botão de novo, por isso nenhum aperto se perde.",
    "s48": "Passados quatro milissegundos, anotamos a hora e somamos o step ao brilho. Em duzentos e cinquenta e cinco, o step vira menos um, e em zero, mais um de novo.",
    "s49": "Por fim, analogWrite() mostra o novo brilho no LED.",
    "s50": "Vamos rodar. O LED respira, e um aperto o para na hora, bem no meio do fade. Aperto de novo, e ele continua.",
    "s51": "Pergunta rápida: na linha trinta e nove, o quatro vira dez. Respira mais rápido, ou mais devagar?",
    "s52": "Mais devagar. Cada passo espera dez milissegundos; subir leva uns dois segundos e meio, e a respiração fica mais calma.",
    "s53": "Agora pause o vídeo e explique com suas palavras por que o botão funciona neste sketch, mas não no primeiro. Uma ou duas frases bastam.",
    "s54": "Um jeito de dizer: o primeiro sketch esperava a cada passo, então ninguém lia o botão. Este nunca espera: olha o relógio e segue em frente.",
    "s55": "Hoje você aprendeu três coisas. O PWM regula um LED piscando muito rápido. analogWrite() recebe de zero a duzentos e cinquenta e cinco. E um fade com relógio sempre escuta.",
    "s56": "Na próxima, no episódio seis, vamos misturar a cor que quiser com um LED RGB. Até lá, me conta nos comentários: o que você faria respirar? Te vejo lá!",
}

ES = {
    "s01": "Mira este LED. Sube de brillo despacio, luego baja, una y otra vez, como alguien que respira dormido.",
    "s02": "Y si presiono el botón, se detiene al instante, a mitad de un respiro. Presiono otra vez y sigue.",
    "s03": "Pero este pin solo puede estar encendido o apagado. Al final del video sabrás el truco y harás respirar cualquier LED.",
    "s04": "Antes de empezar, dos preguntas de episodios anteriores. Pregunta rápida: el botón usa la resistencia pull-up interna. Al presionarlo, ¿el pin lee HIGH o LOW?",
    "s05": "LOW. Al presionar, el pin se conecta a tierra, y la tierra le gana a la débil resistencia interna que lo sube.",
    "s06": "Pregunta rápida: ¿por qué un delay largo hace perder una pulsación?",
    "s07": "Porque durante un delay, el programa se detiene y nadie mira el botón. Recuérdalo: hoy vuelve a aparecer.",
    "s08": "Solo necesitas el circuito del episodio cuatro: el LED rojo en GPIO veintitrés y el botón en GPIO veintidós. Un multímetro es un buen extra.",
    "s09": "Hasta ahora, digitalWrite() daba dos opciones, como un interruptor normal: encendido o apagado.",
    "s10": "Pregunta rápida: ¿cómo puede un pin que solo se enciende o se apaga dar media luz a un LED? Piénsalo un momento.",
    "s11": "La respuesta es la velocidad. Piensa en un ventilador de techo: si gira rápido, ya no ves las aspas, solo un borrón.",
    "s12": "El pin hace lo mismo con la luz. Enciende y apaga el LED unas mil veces por segundo, y tu ojo solo ve el promedio.",
    "s13": "Este truco se llama PWM, modulación por ancho de pulso. Lo que pasa en realidad: el pin siempre está en tres coma tres voltios o en cero. Solo cambia el tiempo.",
    "s14": "La diferencia con el ventilador: este sí pasa por cada posición intermedia. El LED solo está encendido o apagado, y lo intermedio ocurre en tu ojo.",
    "s15": "Controlamos cuánto dura encendido el pin en cada ciclo corto. Esa parte se llama ciclo de trabajo.",
    "s16": "Piensa en una llave de agua que abres un momento cada segundo. Si la abres un cuarto de segundo, sale poca agua. Si la dejas abierta, sale el chorro completo.",
    "s17": "La diferencia: una llave puede abrirse a medias, pero un pin PWM nunca.",
    "s18": "Así, veinticinco por ciento se ve tenue, cincuenta, medio, y cien por ciento, a todo brillo.",
    "s19": "En código, todo esto es una función: analogWrite(). Le das un pin y un número de cero a doscientos cincuenta y cinco.",
    "s20": "Es como una perilla con muchos clics: cero es siempre apagado y doscientos cincuenta y cinco, siempre encendido. Pregunta rápida: ¿qué número da medio brillo?",
    "s21": "Cerca de ciento veintiocho, encendido la mitad de cada ciclo. La diferencia con una perilla real: gira suave, pero esta tiene justo doscientos cincuenta y seis pasos.",
    "s23": "Aquí está el primer sketch, pwm_levels. Arriba, el pin veintitrés recibe un nombre. setup() lo hace salida e inicia el Monitor Serie.",
    "s24": "Luego algo nuevo: nuestra propia función, showLevel(). Es como una receta con un hueco: el número entre paréntesis lo llena en cada llamada.",
    "s25": "Lo que pasa en realidad: al llamar a showLevel() con sesenta y cuatro, el valor dentro de la función vale sesenta y cuatro. analogWrite() lo usa, se imprime, y espera dos segundos.",
    "s26": "La diferencia con una receta en papel: la función olvida el valor al terminar.",
    "s27": "El loop llama a showLevel() con cero, sesenta y cuatro, ciento veintiocho y doscientos cincuenta y cinco. Pausa el video y adivina: ¿qué hará el LED en cada paso?",
    "s28": "Vamos a correrlo. El LED sube en cuatro niveles claros: apagado, tenue, medio y a todo brillo. Luego vuelve a empezar.",
    "s29": "Un multímetro en el pin del LED es muy lento para seguir el cambio, así que marca el voltaje promedio.",
    "s30": "Unos cero coma ocho voltios con veinticinco por ciento, uno sesenta y cinco con cincuenta, y tres coma tres con cien: justo el tiempo que el pin pasa encendido.",
    "s31": "Tu turno: cambia sesenta y cuatro por diez. ¿Qué crees que verás? Un brillo muy débil, y una décima de voltio.",
    "s32": "Ahora hagamos que el LED respire. Lo obvio son dos bucles for. Uno sube el brillo con un pequeño delay en cada paso, y el otro lo baja.",
    "s34": "Pregunta rápida: mientras este LED se atenúa, ¿qué pasa si presionas el botón?",
    "s35": "Mira. Presiono tres, cuatro veces, y el fade sigue como si nada.",
    "s36": "Es el problema del delay del inicio del video. Es como subir escaleras con audífonos: hasta llegar arriba, no oyes el timbre.",
    "s37": "En realidad, un fade completo tarda unos dos segundos, y el botón solo se lee entre dos fades. Así, una pulsación corta casi siempre se pierde.",
    "s38": "La diferencia: tú aún sentirías un toque en el hombro, pero la placa no nota nada hasta que acaba el bucle.",
    "s39": "La solución: el reloj de pared del episodio cuatro. Lo miramos en cada vuelta y actuamos solo si pasó bastante tiempo.",
    "s40": "Cada cuatro milisegundos damos un pasito, y el brillo sube uno. Doscientos cincuenta y cinco pasos tardan casi un segundo.",
    "s41": "Arriba, damos la vuelta y contamos hacia abajo. Abajo, otra vuelta, y empieza la siguiente respiración.",
    "s43": "Aquí está el sketch completo, fade_millis. brightness es el brillo actual del LED. step es lo que sumamos cada vez: más uno al subir y menos uno al bajar.",
    "s44": "lastStep guarda la hora del último paso, y fading dice si el LED respira o está en pausa. Debajo está la memoria del botón del episodio cuatro.",
    "s45": "En el loop leemos el reloj una vez. Primero, el botón del episodio cuatro. Un clic nuevo invierte fading: el signo de admiración significa no.",
    "s46": "La parte dos es el fade. Pausa el video y predice: el LED respira, pero solo pasaron dos milisegundos. ¿Qué hace esta parte?",
    "s47": "Nada. El loop sigue y vuelve a revisar el botón, por eso nunca se pierde una pulsación.",
    "s48": "Al pasar cuatro milisegundos, anotamos la hora y sumamos el step al brillo. En doscientos cincuenta y cinco, el step pasa a menos uno, y en cero, a más uno.",
    "s49": "Por último, analogWrite() pone el nuevo brillo en el LED.",
    "s50": "Vamos a correrlo. El LED respira, y al presionar se detiene al instante, a mitad del fade. Presiono otra vez y sigue.",
    "s51": "Pregunta rápida: en la línea treinta y nueve, el cuatro pasa a diez. ¿Respira más rápido, o más lento?",
    "s52": "Más lento. Cada paso espera diez milisegundos; subir tarda unos dos segundos y medio, y la respiración se calma.",
    "s53": "Ahora pausa el video y explica con tus palabras por qué el botón funciona en este sketch y no en el primero. Basta con una o dos frases.",
    "s54": "Una forma de decirlo: el primer sketch esperaba en cada paso, y nadie leía el botón. Este nunca espera: mira el reloj y sigue.",
    "s55": "Hoy aprendiste tres cosas. PWM atenúa un LED conmutándolo muy rápido. analogWrite() recibe un número de cero a doscientos cincuenta y cinco. Y un fade con reloj siempre escucha.",
    "s56": "La próxima vez, en el episodio seis, mezclaremos cualquier color con un LED RGB. Mientras, dime en los comentarios: ¿qué harías respirar? ¡Nos vemos!",
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
