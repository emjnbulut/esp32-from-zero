"""Source of video/ep07/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, is edited in dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
Usage: python video/ep07/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "मेरा हाथ देखिए: knob घुमाते ही LED साथ चलती है।",
    # s02
    "इस video के अंत तक आप किसी भी knob को एक line से पढ़ लेंगे। और न चले, तो गड़बड़ी ढूँढना भी जान जाएँगे।",
    # s03
    "पहले, पिछले episode से दो सवाल। छोटा सवाल: setColor() में दो सौ पचपन, दो सौ पचपन और शून्य दें। RGB LED कौन सा रंग दिखाएगी?",
    # s04
    "पीला। लाल और हरी रोशनी जुड़ती हैं।",
    # s05
    "छोटा सवाल: RGB LED बुझ गई, तीनों रंग एक साथ। सबसे पहले कौन सा wire जाँचेंगे?",
    # s06
    "साझा wire, सबसे लंबे पैर पर। रंग उसी से लौटते हैं।",
    # s07
    "पिछला circuit, दस किलो-ओम potentiometer, यानी तीन पैरों वाला knob, और कुछ wires।",
    # s08
    "अब तक हमने बटन पढ़ा, जिसके दो जवाब हैं: दबा या नहीं दबा। Knob बता सकता है कितना।",
    # s09
    "एक फिसलपट्टी सोचिए। ऊपर तीन दशमलव तीन volt, नीचे ground, और knob तय करता है आप कितना ऊपर बैठे हैं।",
    # s10
    "असल में knob में resistor की पट्टी पर एक संपर्क सरकता है। बाहरी पैर तीन दशमलव तीन volt और ground पर, बीच का पैर संपर्क का voltage देता है।",
    # s11
    "इसे voltage divider कहते हैं। फिसलपट्टी से फ़र्क: यहाँ कुछ अपने आप नहीं फिसलता। संपर्क वहीं रहता है जहाँ छोड़ें।",
    # s12
    "छोटा सवाल: knob ठीक बीच में है। बीच के पैर पर लगभग कितने volt होंगे?",
    # s13
    "लगभग एक दशमलव छह पाँच volt, तीन दशमलव तीन का आधा। Knob की हर स्थिति का अपना voltage है।",
    # s14
    "यही circuit schematic में। टेढ़ी रेखा resistor, तीर सरकता संपर्क।",
    # s15
    "USB cable निकालिए। Knob दाएँ breadboard पर, LED के नीचे लगाइए। एक बाहरी पैर plus rail पर, दूसरा minus rail पर।",
    # s16
    "एक लंबा wire बीच के पैर को D चौंतीस तक ले जाता है। Rails बीच से कटी हों, तो हर एक पर bridge wire लगाइए।",
    # s17
    "यहाँ एक नियम: plus rail तीन दशमलव तीन volt हो, पाँच कभी नहीं। ESP32 का input सिर्फ़ तीन दशमलव तीन सह सकता है।",
    # s18
    "Voltage पढ़ने का नया function: analogRead()। चार हज़ार छियानवे निशानों का पैमाना सोचिए।",
    # s19
    "analogRead() pin का voltage नापकर संख्या देता है। शून्य यानी शून्य volt, चार हज़ार पंचानवे यानी तीन दशमलव तीन।",
    # s20
    "पैमाने से फ़र्क: यह पूरा सटीक नहीं। दोनों सिरों के पास थोड़ा चपटा है, इसलिए शून्य या चार हज़ार पंचानवे ठीक-ठीक शायद न दिखे।",
    # s21
    "यह पूरा sketch, pot_read, बहुत छोटा है। Pin चौंतीस को नाम मिला, और setup() सिर्फ़ Serial Monitor शुरू करता है। सिर्फ़ पढ़ने वाले pin को pinMode() नहीं चाहिए।",
    # s22
    "Loop में analogRead() संख्या को value में रखता है। उसे print करते हैं, और दसवाँ हिस्सा second रुकते हैं। Video रोकिए और अंदाज़ा लगाइए: knob बीच में हो तो कौन सी संख्या?",
    # s23
    "लगभग दो हज़ार, पैमाने का आधा। Knob घुमाने पर Serial Monitor की संख्या साथ चढ़ती है।",
    # s24
    "अब knob को कुछ करना चाहिए। analogWrite() चमक तय करता है, पर शून्य से दो सौ पचपन ही लेता है, और knob चार हज़ार पंचानवे तक देता है। छोटा सवाल: इसे कैसे बिठाएँ?",
    # s25
    "भाग देकर। चार हज़ार पंचानवे में सोलह से भाग लगभग दो सौ पचपन है, तो knob और चमक के सिरे मिल जाते हैं।",
    # s26
    "यह pot_dimmer है। Knob value में, सोलह से भाग देकर brightness, और analogWrite() से LED।",
    # s27
    "रोकिए, अंदाज़ा लगाइए: सोलह नहीं, बत्तीस से भाग दें तो?",
    # s28
    "सबसे बड़ी संख्या लगभग एक सौ सत्ताईस होगी, तो knob जितना घुमाइए, LED आधी रहेगी।",
    # s29
    "अब meter बीच के पैर पर। Knob घुमाते volt शून्य से तीन दशमलव तीन चढ़ते हैं, LED साथ चलती है।",
    # s30
    "कभी सारी values नहीं चाहिए होतीं, बस कुछ विकल्प, जैसे चूल्हे पर कम, मध्यम और तेज़ के निशान।",
    # s31
    "असल में knob अब भी एक संख्या देता है, और हमारा code उसे छाँटता है। चार हज़ार पंचानवे में तीन से भाग लगभग तेरह सौ पैंसठ है, तो तेरह सौ पैंसठ और सत्ताईस सौ तीस पर काटते हैं।",
    # s32
    "चूल्हे से फ़र्क: क्लिक नहीं, हिस्से सिर्फ़ code में।",
    # s33
    "यह sketch pot_zones है। तेरह सौ पैंसठ से नीचे LED को बीस मिलता है, यानी धीमी। नहीं तो, सत्ताईस सौ तीस से नीचे एक सौ बीस। वरना पूरी चमक।",
    # s34
    "Video रोकिए और अंदाज़ा लगाइए: reading ठीक तेरह सौ पैंसठ है। यह किस हिस्से में है?",
    # s35
    "बीच वाले में। सख्ती से छोटा: तेरह सौ पैंसठ पहले फेल, दूसरे में पास।",
    # s36
    "धीरे घुमाइए: धीमी, मध्यम और पूरी।",
    # s37
    "एक बात और। Knob को छोड़कर संख्या देखिए। वह अब भी हिलती है, जैसे बाथरूम का तराज़ू जो कभी टिकता नहीं।",
    # s38
    "असल में बहुत छोटा बिजली का शोर हर reading बदलता है। इलाज वही जो तराज़ू पर करते: चार बार नापिए, और औसत लीजिए।",
    # s39
    "तराज़ू से फ़र्क: चार readings में एक millisecond से कम लगता है।",
    # s40
    "pot_smooth में sum शून्य से शुरू होता है। for loop चार बार चलकर नई reading जोड़ता है। फिर sum में चार से भाग औसत है।",
    # s40b
    "रोकिए, अंदाज़ा लगाइए: graph पर कौन सी रेखा कम काँपेगी, अकेली reading या औसत?",
    # s41
    "औसत। Serial Plotter दोनों को रेखा में खींचता है: अकेली reading काँपती है, औसत शांत है।",
    # s42
    "अब वह समस्या जो आपको मिलेगी। LED knob पर बिल्कुल नहीं चलती। छोटा सवाल: LED, knob या code? पहले क्या करेंगे?",
    # s43
    "पहले value print कीजिए। डॉक्टर दवा से पहले बुखार नापता है, और print line आपका thermometer है।",
    # s44
    "संख्या बताती है कौन सा आधा टूटा है। शून्य या सबसे ऊपर अटकी हो, तो knob पर ढीला wire या rail में खाली जगह। सामान्य चले, तो LED देखिए।",
    # s44b
    "Thermometer से फ़र्क: print में समय लगता है, ज़्यादा prints loop धीमा करते हैं। काम होने पर हटाइए।",
    # s45
    "Pin चौंतीस क्यों? सब pins बराबर नहीं। चौंतीस से उनतालीस एकतरफ़ा हैं: सिर्फ़ सुनते हैं, LED नहीं चलाते।",
    # s46
    "दूसरा नियम: पच्चीस से सत्ताईस जैसे कुछ pins Wi-Fi चालू हो तो analog नहीं पढ़ सकते। चौंतीस चलता रहता है, इसलिए हमारे sensors वहीं हैं।",
    # s47
    "तीसरा नियम: शून्य, दो, पाँच, बारह और पंद्रह की power-on पर जाँच होती है, इसलिए खाली छोड़ते हैं। Pin map lesson folder में है।",
    # s48
    "अब रोकिए, अपने शब्दों में बताइए सोलह से भाग क्यों देते हैं। एक वाक्य काफ़ी है।",
    # s49
    "एक तरीका: knob का पैमाना चमक के पैमाने से सोलह गुना बड़ा है, तो भाग देने से दोनों मिल जाते हैं।",
    # s50
    "आपकी बारी: Knob Blink Speed। LED हर समय blink करती है, और knob तीन गतियाँ चुनता है: हर सौ milliseconds, हर चार सौ, हर second।",
    # s51
    "मोड़: delay() नहीं चलेगा। हिस्से अंतराल चुनते हैं, और episode चार की millis() तरकीब blink कराती है।",
    # s52
    "आज आपने तीन बातें सीखीं। Knob स्थिति को voltage बनाता है। analogRead() voltage को संख्या बनाता है। और print करने से समस्या दिखती है।",
    # s53
    "अगली बार: भाग देने वाला function और भरती LEDs की पट्टी। Blink speed का code comments में डालिए; हल folder में है।",
]

PT = [
    # s01
    "Olhe minha mão. Giro um seletor e o LED o segue, mais forte, mais fraco.",
    # s02
    "No fim deste vídeo, você lê qualquer seletor com uma linha. E quando falhar, sabe achar o problema.",
    # s03
    "Duas do episódio passado. setColor() com duzentos e cinquenta e cinco, duzentos e cinquenta e cinco e zero: que cor?",
    # s04
    "Amarelo. Vermelho e verde somam luz: amarelo.",
    # s05
    "Pergunta rápida: o RGB apagou nas três cores. Que fio conferir primeiro?",
    # s06
    "O fio comum, na perna mais longa. As três cores voltam ao terra por ele.",
    # s07
    "Você precisa do circuito passado, um potenciômetro de dez quilo-ohms, um seletor de três pernas, e uns fios.",
    # s08
    "Até agora só lemos um botão, que tem duas respostas: apertado ou não. Um seletor responde quanto.",
    # s09
    "Um escorregador: topo três vírgula três volts, base terra, e o seletor escolhe a altura.",
    # s10
    "O seletor tem uma faixa de resistor com um contato deslizante. As pernas de fora vão a três vírgula três volts e ao terra, a do meio dá a tensão do contato.",
    # s11
    "É um divisor de tensão. Nada desce sozinho: o contato fica onde deixar.",
    # s12
    "Pergunta rápida: seletor no meio. Quantos volts há na perna do meio?",
    # s13
    "Uns um vírgula sessenta e cinco volts, metade de três vírgula três. Cada posição do seletor é uma tensão.",
    # s14
    "Aqui o mesmo circuito em esquema, só as ligações. O zigue-zague é o resistor, e a seta, o contato.",
    # s15
    "Tire o cabo USB. O seletor vai na protoboard da direita, abaixo do LED. Uma perna de fora vai ao positivo, a outra ao negativo.",
    # s16
    "Um fio longo leva a perna do meio ao D trinta e quatro. Se os trilhos forem cortados, uma ponte em cada um.",
    # s17
    "Uma regra: o trilho positivo tem de ser três vírgula três volts, nunca cinco. A entrada do ESP32 só aguenta três vírgula três.",
    # s18
    "Para ler essa tensão, uma função nova: analogRead(). Pense numa régua de quatro mil e noventa e seis marcas.",
    # s19
    "Na prática, analogRead() mede a tensão de um pino e devolve um número. Zero é zero volt, e quatro mil e noventa e cinco são três vírgula três volts.",
    # s20
    "Diferente da régua, esta não é perfeita. Perto das pontas achata, e talvez você nunca veja zero ou quatro mil e noventa e cinco.",
    # s21
    "Este é o sketch inteiro, pot_read, bem pequeno. O pino trinta e quatro ganha nome, e setup() só liga o Serial Monitor. Um pino só de leitura não precisa de pinMode().",
    # s22
    "No loop, analogRead() põe um número em value. Imprimimos e esperamos um décimo de segundo. Pause e preveja: com o seletor no meio, que número você espera?",
    # s23
    "Uns dois mil, metade da escala. Girando o seletor, o número no Serial Monitor sobe junto, do começo da escala ao topo.",
    # s24
    "Agora o seletor deve fazer algo. analogWrite() define o brilho, mas só aceita zero a duzentos e cinquenta e cinco, e o seletor dá até quatro mil e noventa e cinco. Como encaixar isso?",
    # s25
    "Dividindo. Quatro mil e noventa e cinco por dezesseis dão uns duzentos e cinquenta e cinco: as pontas do seletor caem nas do brilho.",
    # s26
    "Este é o pot_dimmer. Lemos o seletor em value, dividimos por dezesseis, e analogWrite() mostra no LED.",
    # s27
    "Pause e preveja: dividir por trinta e dois muda o quê?",
    # s28
    "O maior número seria uns cento e vinte e sete, e o LED ficaria na metade da força, por mais que girasse o seletor.",
    # s29
    "Agora com medidor na perna do meio. Girando, vai de zero a três vírgula três volts.",
    # s30
    "Às vezes você não quer todos os valores, só poucas escolhas, como os níveis baixo, médio e alto do fogão.",
    # s31
    "Separamos o número. Quatro mil e noventa e cinco por três são uns mil trezentos e sessenta e cinco: cortamos aí e em dois mil setecentos e trinta.",
    # s32
    "Diferente do fogão: sem cliques. As zonas são só código.",
    # s33
    "Em pot_zones, abaixo de mil trezentos e sessenta e cinco, LED vinte. Senão, abaixo de dois mil setecentos e trinta, cento e vinte. Senão, total.",
    # s34
    "Pause e preveja: a leitura é exatamente mil trezentos e sessenta e cinco. Em que zona está?",
    # s35
    "Na do meio. Menor que é estrito: mil trezentos e sessenta e cinco falha no primeiro e passa no segundo.",
    # s36
    "Gire devagar: fraco, médio e total.",
    # s37
    "Mais uma coisa. Deixe o seletor quieto e veja o número. Ainda oscila, como uma balança que nunca assenta.",
    # s38
    "Na prática, um ruído elétrico minúsculo muda cada leitura. A solução é a da balança: meça quatro vezes e tire a média.",
    # s39
    "Diferente da balança: quatro leituras levam à placa bem menos de um milissegundo.",
    # s40
    "Em pot_smooth, sum começa em zero. Um laço for roda quatro vezes somando leituras. Depois, sum por quatro é a média.",
    # s40b
    "Pause e preveja: qual linha treme menos, a leitura única ou a média?",
    # s41
    "A média. O Serial Plotter desenha as duas: a leitura única treme, e a média é mais calma.",
    # s42
    "O problema que você vai encontrar. O LED não reage ao seletor. Pergunta rápida: é o LED, o seletor ou o código? O que fazer primeiro?",
    # s43
    "Imprima o valor antes de confiar em algo. O médico mede a febre antes do remédio, e a impressão é seu termômetro.",
    # s44
    "O número diz qual metade está com defeito. Preso em zero ou no topo é fio solto ou falha no trilho, no seletor. Se mexe normal, olhe o lado do LED.",
    # s44b
    "Diferente do termômetro: imprimir leva tempo, e prints demais podem frear um loop rápido. Tire-os ao terminar.",
    # s45
    "Por que o pino trinta e quatro? Porque os pinos não são iguais. De trinta e quatro a trinta e nove são portas de mão única: só escutam, então não acendem um LED.",
    # s46
    "Segunda regra: pinos vinte e cinco a vinte e sete não leem analógico com Wi-Fi ligado. O trinta e quatro segue firme: sensores moram nele.",
    # s47
    "Terceira regra: os pinos zero, dois, cinco, doze e quinze são checados ao ligar, então os deixamos livres. Não precisa decorar. O mapa completo está na pasta da aula.",
    # s48
    "Agora pause e explique por que dividimos por dezesseis. Uma frase basta.",
    # s49
    "Um jeito de dizer: a escala do seletor é dezesseis vezes maior que a do brilho, então dividir as faz coincidir.",
    # s50
    "Sua vez: Knob Blink Speed. O LED pisca o tempo todo, e o seletor escolhe a velocidade em três zonas: a cada cem milissegundos, a cada quatrocentos e a cada segundo.",
    # s51
    "A reviravolta: nada pode esperar com delay(). As zonas de hoje escolhem o intervalo, e o truque millis() do episódio quatro faz o pisca.",
    # s52
    "Hoje você aprendeu três coisas. O seletor vira tensão, analogRead() vira número, e imprimir mostra o problema.",
    # s53
    "Na próxima: uma função que divide e uma barra de LEDs que enche ao girar. Poste seu código nos comentários; há solução na pasta. Até lá!",
]

ES = [
    # s01
    "Mira mi mano. Giro la perilla y el LED la sigue al instante.",
    # s02
    "Al final leerás cualquier perilla con una línea. Si falla, sabrás hallar el problema.",
    # s03
    "Dos del episodio pasado. Pregunta rápida: setColor() con doscientos cincuenta y cinco, doscientos cincuenta y cinco y cero. ¿Qué color?",
    # s04
    "Amarillo. Luz roja y verde dan amarillo: la luz suma.",
    # s05
    "Pregunta rápida: el LED RGB se apaga, los tres colores juntos. ¿Qué cable revisas primero?",
    # s06
    "El común, en la pata larga. Todo vuelve a tierra.",
    # s07
    "Necesitas el circuito del episodio pasado, un potenciómetro de diez kilo-ohmios, una perilla de tres patas, y unos cables.",
    # s08
    "Hasta ahora solo leímos un botón, que tiene dos respuestas: pulsado o no. Una perilla responde cuánto.",
    # s09
    "Imagina un tobogán. Arriba tres coma tres voltios, abajo tierra, y la perilla decide tu altura.",
    # s10
    "La perilla tiene una tira de resistencia con un contacto deslizante. Las patas de afuera van a tres coma tres voltios y a tierra, y la del medio da el voltaje del contacto.",
    # s11
    "Eso es un divisor de voltaje. A diferencia del tobogán, nada baja solo. El contacto queda donde lo dejes.",
    # s12
    "Pregunta: perilla en medio. ¿Cuántos voltios hay en la pata del medio?",
    # s13
    "Unos uno coma sesenta y cinco voltios. Cada posición es un voltaje.",
    # s14
    "Aquí el circuito en esquema. El zigzag es la resistencia, y la flecha, el contacto.",
    # s15
    "Desconecta el cable USB. La perilla va en la protoboard derecha, debajo del LED. Una pata de afuera va al riel positivo y la otra al negativo.",
    # s16
    "Un cable largo lleva la pata del medio a D treinta y cuatro. Con rieles cortados, un puente en cada uno.",
    # s17
    "Una regla: el riel positivo debe ser de tres coma tres voltios, nunca cinco. Una entrada del ESP32 solo aguanta tres coma tres.",
    # s18
    "Para leerlo, función nueva: analogRead(). Imagina una regla de cuatro mil noventa y seis marcas.",
    # s19
    "analogRead() mide el voltaje de un pin y da un número. Cero es cero voltios, y cuatro mil noventa y cinco son tres coma tres.",
    # s20
    "Esta regla no es perfecta. Cerca de los extremos se aplana, y quizá no veas cero ni cuatro mil noventa y cinco.",
    # s21
    "Este es el sketch completo, pot_read. El pin treinta y cuatro recibe nombre, y setup() solo inicia el Serial Monitor. Un pin que solo se lee no necesita pinMode().",
    # s22
    "En el loop, analogRead() pone un número en value. Lo imprimimos y esperamos. Predice: con la perilla en medio, ¿qué número esperas?",
    # s23
    "Unos dos mil, la mitad de la escala. Al girar la perilla, el número del Serial Monitor sube con ella.",
    # s24
    "Ahora la perilla debe hacer algo. analogWrite() fija el brillo, pero solo acepta de cero a doscientos cincuenta y cinco, y la perilla da hasta cuatro mil noventa y cinco. ¿Cómo lo ajustamos?",
    # s25
    "Dividiendo. Cuatro mil noventa y cinco entre dieciséis son unos doscientos cincuenta y cinco, y los extremos coinciden.",
    # s26
    "Es pot_dimmer. Leemos la perilla en value, dividimos entre dieciséis en brightness, y analogWrite() lo muestra.",
    # s27
    "Pausa y predice: si dividiéramos entre treinta y dos, ¿qué cambiaría?",
    # s28
    "El mayor sería unos ciento veintisiete, y el LED quedaría a media potencia, gires lo que gires.",
    # s29
    "Ahora en serio, con un medidor en la pata del medio. Al girar, los voltios van de cero a tres coma tres.",
    # s30
    "A veces quieres pocas opciones, como las marcas baja, media y alta de la estufa.",
    # s31
    "El código clasifica el número. Cuatro mil noventa y cinco entre tres son unos mil trescientos sesenta y cinco: cortamos ahí y en dos mil setecientos treinta.",
    # s32
    "Sin clics, a diferencia de la estufa. Las zonas son solo código.",
    # s33
    "Este es pot_zones. Bajo mil trescientos sesenta y cinco, el LED recibe veinte. Si no, bajo dos mil setecientos treinta, ciento veinte. Si no, total.",
    # s34
    "Pausa y predice: lectura de mil trescientos sesenta y cinco. ¿Qué zona?",
    # s35
    "En la del medio. Menor que es estricto: falla la primera y pasa la segunda.",
    # s36
    "Gira despacio: tenue, medio, total, tres pasos.",
    # s37
    "Una cosa más. Deja la perilla quieta y mira el número. Aún tiembla, como una báscula inquieta.",
    # s38
    "Un ruido eléctrico diminuto cambia cada lectura. La solución es la de la báscula: mide cuatro veces y saca el promedio.",
    # s39
    "Pero cuatro lecturas toman a la placa menos de un milisegundo.",
    # s40
    "En pot_smooth, sum empieza en cero. Un for suma cuatro lecturas. Luego, sum entre cuatro es el promedio.",
    # s40b
    "Predice: ¿qué línea tiembla menos, la lectura sola o el promedio?",
    # s41
    "El promedio. El Serial Plotter dibuja ambas: la lectura sola tiembla, y el promedio es más calmado.",
    # s42
    "El LED no reacciona a la perilla. Pregunta rápida: ¿es el LED, la perilla o el código? ¿Qué haces primero?",
    # s43
    "Imprime el valor antes de confiar. El médico mide la fiebre antes de recetar, y la línea de impresión es tu termómetro.",
    # s44
    "El número dice qué mitad falla. Pegado en cero o en el tope es un cable suelto o un hueco del riel en la perilla. Si se mueve normal, mira el LED.",
    # s44b
    "A diferencia del termómetro, imprimir toma tiempo, y demasiados prints pueden frenar un loop rápido. Quítalos al terminar.",
    # s45
    "¿Por qué el pin treinta y cuatro? Del treinta y cuatro al treinta y nueve son de un sentido: solo escuchan, no encienden un LED.",
    # s46
    "Segunda regla: pines como del veinticinco al veintisiete no leen analógico con Wi-Fi activo. El treinta y cuatro sigue firme.",
    # s47
    "Tercera regla: los pines cero, dos, cinco, doce y quince se revisan al encender, así que los dejamos libres. El mapa está en la carpeta.",
    # s48
    "Ahora pausa y explica por qué dividimos entre dieciséis. Una frase basta.",
    # s49
    "Una forma de decirlo: la escala de la perilla es dieciséis veces mayor que la del brillo.",
    # s50
    "Tu turno: Knob Blink Speed. El LED parpadea siempre, y la perilla elige la velocidad en tres zonas: cada cien milisegundos, cada cuatrocientos y cada segundo.",
    # s51
    "Giro: nada espera con delay(). Las zonas eligen el intervalo, y millis() del episodio cuatro parpadea.",
    # s52
    "Hoy aprendiste tres cosas. La perilla da voltaje, analogRead() lo vuelve número, e imprimir muestra dónde está el problema.",
    # s53
    "Después: una función que divide y una barra de LEDs que se llena al girar. Publica tu código en los comentarios; hay solución. ¡Nos vemos!",
]

TARGET = {"hi": 1.08, "pt": 1.08, "es": 1.08}


def check(langs, english):
    """Print per-language max/mean char ratio vs the English narration; return the over-target lines."""
    over = []
    for lang, seg in langs.items():
        ratios = {k: len(seg[k]) / len(english[k]) for k in english}
        worst = max(ratios, key=ratios.get)
        print(f"{lang}: max {ratios[worst]:.2f} ({worst}), mean {sum(ratios.values()) / len(ratios):.2f}, target <= {TARGET[lang]:.2f}")
        over += [(lang, k, r) for k, r in ratios.items() if r > TARGET[lang] + 1e-9]
    for lang, k, r in over:
        print(f"  OVER {lang} {k}: {r:.2f} ({len(langs[lang][k])} vs {len(english[k])} chars)")
    return over


if __name__ == "__main__":
    script = json.loads((ROOT / "script.json").read_text(encoding="utf-8"))
    english = {s["id"]: s["text"] for s in script["segments"]}
    out = ROOT / "dub"
    out.mkdir(exist_ok=True)
    langs = {}
    for lang, voice, lines in (("hi", "hi-IN-MadhurNeural", HI), ("pt", "pt-BR-AntonioNeural", PT), ("es", "es-MX-JorgeNeural", ES)):
        assert len(lines) == len(IDS) == 55, (lang, len(lines), len(IDS))
        seg = dict(zip(IDS, lines))
        langs[lang] = seg
        (out / f"{lang}.json").write_text(json.dumps({"voice": voice, "rate": "+0%", "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("dubs written:", ", ".join(langs))
    check(langs, english)
