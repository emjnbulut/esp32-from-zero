"""Source of video/ep07/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, is edited in dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
Usage: python video/ep07/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "मेरा हाथ देखिए। मैं knob घुमाता हूँ, और LED साथ चलती है, तेज़ और धीमी, मेरे घुमाते ही।",
    # s02
    "इस video के अंत तक आप किसी भी knob को एक line से पढ़ लेंगे। और न चले, तो गड़बड़ी ढूँढना भी जान जाएँगे।",
    # s03
    "पहले, पिछले episode से दो सवाल। छोटा सवाल: setColor() में दो सौ पचपन, दो सौ पचपन और शून्य दें। RGB LED कौन सा रंग दिखाएगी?",
    # s04
    "पीला। लाल रोशनी और हरी रोशनी मिलकर पीला बनाती है, क्योंकि रोशनी जुड़ती है।",
    # s05
    "छोटा सवाल: RGB LED बुझ गई, तीनों रंग एक साथ। सबसे पहले कौन सा wire जाँचेंगे?",
    # s06
    "साझा wire, सबसे लंबे पैर पर। तीनों रंग उसी से ground तक लौटते हैं।",
    # s07
    "पिछले episode का circuit चाहिए, एक दस किलो-ओम potentiometer, यानी तीन पैरों वाला knob, और कुछ wires।",
    # s08
    "अब तक हमने सिर्फ़ बटन पढ़ा है, और बटन के दो जवाब हैं: दबा, या नहीं दबा। Knob बता सकता है कितना।",
    # s09
    "एक playground की फिसलपट्टी सोचिए। ऊपर तीन दशमलव तीन volt है, नीचे ground, और knob तय करता है कि आप कितनी ऊँचाई पर बैठे हैं।",
    # s10
    "असल में knob के अंदर resistor की पट्टी है, जिस पर एक संपर्क सरकता है। बाहरी पैर तीन दशमलव तीन volt और ground पर हैं, और बीच का पैर संपर्क का voltage देता है।",
    # s11
    "इसे voltage divider कहते हैं। फिसलपट्टी से फ़र्क: यहाँ कुछ अपने आप नहीं फिसलता। संपर्क वहीं रहता है जहाँ छोड़ें।",
    # s12
    "छोटा सवाल: knob ठीक बीच में है। बीच के पैर पर लगभग कितने volt होंगे?",
    # s13
    "लगभग एक दशमलव छह पाँच volt, तीन दशमलव तीन का आधा। Knob की हर स्थिति का अपना voltage है।",
    # s14
    "यही circuit schematic में, यानी सिर्फ़ जोड़ दिखाने वाला चित्र। टेढ़ी-मेढ़ी रेखा resistor है, और तीर सरकने वाला संपर्क।",
    # s15
    "USB cable निकालिए। Knob दाएँ breadboard पर, LED के नीचे लगाइए। एक बाहरी पैर plus rail पर, दूसरा minus rail पर।",
    # s16
    "एक लंबा wire बीच के पैर को D चौंतीस तक ले जाता है। Rails बीच से कटी हों, तो हर एक पर bridge wire लगाइए।",
    # s17
    "यहाँ एक नियम: plus rail तीन दशमलव तीन volt हो, पाँच कभी नहीं। ESP32 का input सिर्फ़ तीन दशमलव तीन सह सकता है।",
    # s18
    "वह voltage पढ़ने के लिए नया function: analogRead()। फिसलपट्टी के साथ बिछा, चार हज़ार छियानवे निशानों वाला पैमाना सोचिए।",
    # s19
    "असल में analogRead() pin का voltage नापकर एक संख्या देता है। शून्य यानी शून्य volt, और चार हज़ार पंचानवे यानी तीन दशमलव तीन volt।",
    # s20
    "पैमाने से फ़र्क: यह पूरा सटीक नहीं। दोनों सिरों के पास थोड़ा चपटा है, इसलिए शून्य या चार हज़ार पंचानवे ठीक-ठीक शायद न दिखे।",
    # s21
    "यह पूरा sketch, pot_read, बहुत छोटा है। Pin चौंतीस को नाम मिला, और setup() सिर्फ़ Serial Monitor शुरू करता है। सिर्फ़ पढ़ने वाले pin को pinMode() नहीं चाहिए।",
    # s22
    "Loop में analogRead() संख्या को value में रखता है। उसे print करते हैं, और दसवाँ हिस्सा second रुकते हैं। Video रोकिए और अंदाज़ा लगाइए: knob बीच में हो तो कौन सी संख्या?",
    # s23
    "लगभग दो हज़ार, पैमाने का आधा। Knob घूमने पर Serial Monitor की संख्या साथ चढ़ती है, पैमाने के नीचे से ऊपर तक।",
    # s24
    "अब knob को कुछ करना चाहिए। analogWrite() चमक तय करता है, पर शून्य से दो सौ पचपन ही लेता है, और knob चार हज़ार पंचानवे तक देता है। छोटा सवाल: इसे कैसे बिठाएँ?",
    # s25
    "भाग देकर। चार हज़ार पंचानवे में सोलह से भाग लगभग दो सौ पचपन है, तो knob के दोनों सिरे चमक के दोनों सिरों पर आ जाते हैं।",
    # s26
    "यह pot_dimmer है। Knob को value में पढ़ते हैं, सोलह से भाग देकर brightness बनाते हैं, और analogWrite() उसे LED पर दिखाता है।",
    # s27
    "Video रोकिए और अंदाज़ा लगाइए: सोलह की जगह बत्तीस से भाग दें, तो क्या बदलेगा?",
    # s28
    "सबसे बड़ी संख्या लगभग एक सौ सत्ताईस होगी, तो knob कितना भी घुमाइए, LED करीब आधी शक्ति पर रहेगी।",
    # s29
    "अब असली प्रयोग, बीच के पैर पर meter के साथ। Knob घुमाने पर volt शून्य से तीन दशमलव तीन तक चढ़ते हैं, और LED उनके साथ चलती है।",
    # s30
    "कभी सारी values नहीं चाहिए होतीं, बस कुछ विकल्प, जैसे चूल्हे पर कम, मध्यम और तेज़ के निशान।",
    # s31
    "असल में knob अब भी एक संख्या देता है, और हमारा code उसे छाँटता है। चार हज़ार पंचानवे में तीन से भाग लगभग तेरह सौ पैंसठ है, तो तेरह सौ पैंसठ और सत्ताईस सौ तीस पर काटते हैं।",
    # s32
    "चूल्हे से फ़र्क: इस knob में क्लिक नहीं हैं। हिस्से सिर्फ़ code में हैं।",
    # s33
    "यह sketch pot_zones है। तेरह सौ पैंसठ से नीचे LED को बीस मिलता है, यानी धीमी। नहीं तो, सत्ताईस सौ तीस से नीचे एक सौ बीस। वरना पूरी चमक।",
    # s34
    "Video रोकिए और अंदाज़ा लगाइए: reading ठीक तेरह सौ पैंसठ है। यह किस हिस्से में है?",
    # s35
    "बीच वाले में। छोटा का मतलब सख्ती से छोटा, तो तेरह सौ पैंसठ पहली जाँच में फेल और दूसरी में पास।",
    # s36
    "धीरे घुमाइए: धीमी, मध्यम और पूरी, तीन साफ़ सीढ़ियों में।",
    # s37
    "एक बात और। Knob को छोड़कर संख्या देखिए। वह अब भी हिलती है, जैसे बाथरूम का तराज़ू जो कभी टिकता नहीं।",
    # s38
    "असल में बहुत छोटा बिजली का शोर हर reading बदलता है। इलाज वही जो तराज़ू पर करते: चार बार नापिए, और औसत लीजिए।",
    # s39
    "तराज़ू से फ़र्क: चार readings में board को एक millisecond से बहुत कम लगता है, तो समय नहीं जाता।",
    # s40
    "pot_smooth में sum शून्य से शुरू होता है। एक for loop चार बार चलता है, हर बार नई reading जोड़ता है। फिर sum में चार से भाग औसत है।",
    # s40b
    "Video रोकिए और अंदाज़ा लगाइए: graph पर कौन सी रेखा कम काँपेगी, अकेली reading या औसत?",
    # s41
    "औसत। Serial Plotter दोनों को रेखा में खींचता है: अकेली reading काँपती है, औसत शांत है।",
    # s42
    "अब वह समस्या जो आपको मिलेगी। LED knob पर बिल्कुल नहीं चलती। छोटा सवाल: LED, knob या code? पहले क्या करेंगे?",
    # s43
    "पहले value print कीजिए, किसी पर भरोसे से पहले। डॉक्टर दवा से पहले बुखार नापता है, और print line आपका thermometer है।",
    # s44
    "असल में संख्या बताती है कि कौन सा आधा टूटा है। शून्य पर या सबसे ऊपर अटकी हो, तो knob पर ढीला wire या rail में खाली जगह। सामान्य चले, तो knob ठीक है; LED की तरफ़ देखिए।",
    # s44b
    "Thermometer से फ़र्क: print में समय लगता है, तो ज़्यादा prints तेज़ loop को धीमा कर सकते हैं। काम होने पर हटा दीजिए।",
    # s45
    "Pin चौंतीस क्यों? क्योंकि सब pins बराबर नहीं। चौंतीस से उनतालीस एकतरफ़ा दरवाज़ों जैसे हैं: सिर्फ़ सुनते हैं, इसलिए LED नहीं चला सकते।",
    # s46
    "दूसरा नियम: पच्चीस से सत्ताईस जैसे कुछ pins Wi-Fi चालू हो तो analog नहीं पढ़ सकते। चौंतीस चलता रहता है, इसलिए हमारे sensors वहीं हैं।",
    # s47
    "तीसरा नियम: शून्य, दो, पाँच, बारह और पंद्रह की power-on पर जाँच होती है, इसलिए हम उन्हें खाली छोड़ते हैं। रटना ज़रूरी नहीं। पूरा pin map lesson folder में है।",
    # s48
    "अब video रोकिए, और अपने शब्दों में बताइए कि हम सोलह से भाग क्यों देते हैं। एक वाक्य काफ़ी है।",
    # s49
    "एक तरीका: knob का पैमाना चमक के पैमाने से सोलह गुना बड़ा है, तो भाग देने से दोनों मिल जाते हैं।",
    # s50
    "आपकी बारी: Knob Blink Speed। LED हर समय blink करती है, और knob तीन हिस्सों में गति चुनता है: हर सौ milliseconds, हर चार सौ, और हर second।",
    # s51
    "मोड़: कुछ भी delay() से नहीं रुकेगा। आज के हिस्से अंतराल चुनते हैं, और episode चार की millis() तरकीब blink कराती है।",
    # s52
    "आज आपने तीन बातें सीखीं। Knob स्थिति को voltage बनाता है। analogRead() voltage को संख्या बनाता है। और संख्या print करने से समस्या की जगह दिखती है।",
    # s53
    "अगली बार: भाग देने वाला एक function, और घुमाने पर भरती LEDs की पट्टी। Blink speed का code comments में डालिए; एक हल lesson folder में है। वहीं मिलते हैं!",
]

PT = [
    # s01
    "Olhe minha mão. Giro um seletor e o LED o segue, mais forte e mais fraco, assim que me mexo.",
    # s02
    "No fim deste vídeo, você lê qualquer seletor com uma linha de código. E quando não funcionar, sabe achar o problema.",
    # s03
    "Primeiro, duas do episódio passado. Pergunta rápida: setColor() com duzentos e cinquenta e cinco, duzentos e cinquenta e cinco e zero. Que cor o RGB mostra?",
    # s04
    "Amarelo. Luz vermelha mais luz verde dá amarelo, porque a luz soma.",
    # s05
    "Pergunta rápida: o LED RGB apaga, as três cores juntas. Qual fio você confere primeiro?",
    # s06
    "O fio comum, na perna mais longa. As três cores voltam ao terra por ele.",
    # s07
    "Você precisa do circuito do episódio passado, um potenciômetro de dez quilo-ohms, que é um seletor de três pernas, e uns fios.",
    # s08
    "Até agora só lemos um botão, que tem duas respostas: apertado ou não. Um seletor responde quanto.",
    # s09
    "Imagine um escorregador de parquinho. O topo são três vírgula três volts, a base é o terra, e o seletor decide a altura em que você senta.",
    # s10
    "Na prática, dentro do seletor há uma faixa de resistor com um contato que desliza. As pernas de fora vão a três vírgula três volts e ao terra, e a do meio dá a tensão do contato.",
    # s11
    "Isso é um divisor de tensão. Diferente do escorregador, nada desce sozinho. O contato fica onde você deixar.",
    # s12
    "Pergunta rápida: o seletor está bem no meio. Quantos volts, mais ou menos, há na perna do meio?",
    # s13
    "Uns um vírgula sessenta e cinco volts, metade de três vírgula três. Cada posição do seletor é uma tensão.",
    # s14
    "Aqui está o mesmo circuito num esquema, um desenho só com as ligações. O zigue-zague é o resistor, e a seta, o contato deslizante.",
    # s15
    "Tire o cabo USB. O seletor vai na protoboard da direita, abaixo do LED. Uma perna de fora vai ao positivo, a outra ao negativo.",
    # s16
    "Um fio longo leva a perna do meio ao D trinta e quatro. Se os trilhos forem cortados no meio, ponha um fio de ponte em cada um.",
    # s17
    "Uma regra: o trilho positivo tem de ser três vírgula três volts, nunca cinco. A entrada do ESP32 só aguenta três vírgula três.",
    # s18
    "Para ler essa tensão, uma função nova: analogRead(). Pense numa régua de quatro mil e noventa e seis marcas, ao longo do escorregador.",
    # s19
    "Na prática, analogRead() mede a tensão de um pino e devolve um número. Zero é zero volt, e quatro mil e noventa e cinco são três vírgula três volts.",
    # s20
    "Diferente da régua, esta não é perfeita. Perto das pontas ela achata um pouco, e você talvez nunca veja zero ou quatro mil e noventa e cinco exatos.",
    # s21
    "Este é o sketch inteiro, pot_read, bem pequeno. O pino trinta e quatro ganha nome, e setup() só liga o Serial Monitor. Um pino só de leitura não precisa de pinMode().",
    # s22
    "No loop, analogRead() põe um número em value. Imprimimos e esperamos um décimo de segundo. Pause e preveja: com o seletor no meio, que número você espera?",
    # s23
    "Uns dois mil, metade da escala. Girando o seletor, o número no Serial Monitor sobe junto, do começo da escala ao topo.",
    # s24
    "Agora o seletor deve fazer algo. analogWrite() define o brilho, mas só aceita zero a duzentos e cinquenta e cinco, e o seletor dá até quatro mil e noventa e cinco. Como encaixar isso?",
    # s25
    "Dividindo. Quatro mil e noventa e cinco divididos por dezesseis dão uns duzentos e cinquenta e cinco, e as pontas do seletor caem nas pontas do brilho.",
    # s26
    "Este é o pot_dimmer. Lemos o seletor em value, dividimos por dezesseis em brightness, e analogWrite() mostra no LED.",
    # s27
    "Pause e preveja: se dividíssemos por trinta e dois, o que mudaria?",
    # s28
    "O maior número seria uns cento e vinte e sete, e o LED ficaria na metade da força, por mais que girasse o seletor.",
    # s29
    "Agora de verdade, com um medidor na perna do meio. Girando, os volts vão de zero a três vírgula três, e o LED os acompanha.",
    # s30
    "Às vezes você não quer todos os valores, só poucas escolhas, como os níveis baixo, médio e alto do fogão.",
    # s31
    "Na prática, o seletor dá um número só, e o código o separa. Quatro mil e noventa e cinco por três são uns mil trezentos e sessenta e cinco: cortamos aí e em dois mil setecentos e trinta.",
    # s32
    "Diferente do fogão: este seletor não tem cliques. As zonas existem só no código.",
    # s33
    "Este é o sketch pot_zones. Abaixo de mil trezentos e sessenta e cinco, o LED recebe vinte, fraco. Senão, abaixo de dois mil setecentos e trinta, cento e vinte. Senão, brilho total.",
    # s34
    "Pause e preveja: a leitura é exatamente mil trezentos e sessenta e cinco. Em que zona está?",
    # s35
    "Na do meio. Menor que é estritamente menor: mil trezentos e sessenta e cinco falha no primeiro teste e passa no segundo.",
    # s36
    "Gire devagar: fraco, médio e total, em três degraus claros.",
    # s37
    "Mais uma coisa. Deixe o seletor quieto e veja o número. Ele ainda oscila um pouco, como uma balança de banheiro que nunca assenta.",
    # s38
    "Na prática, um ruído elétrico minúsculo muda cada leitura. A solução é a da balança: meça quatro vezes e tire a média.",
    # s39
    "Diferente da balança: quatro leituras levam à placa bem menos de um milissegundo, então não se perde tempo.",
    # s40
    "Em pot_smooth, sum começa em zero. Um laço for roda quatro vezes e soma uma leitura nova a cada volta. Depois, sum dividido por quatro é a média.",
    # s40b
    "Pause e preveja: num gráfico, qual linha treme menos, a leitura única ou a média?",
    # s41
    "A média. O Serial Plotter desenha as duas: a leitura única treme, e a média é mais calma.",
    # s42
    "Agora o problema que você vai encontrar. O LED não reage ao seletor. Pergunta rápida: é o LED, o seletor ou o código? O que você faz primeiro?",
    # s43
    "Imprima o valor, antes de confiar em qualquer coisa. O médico mede a febre antes do remédio, e a linha de impressão é seu termômetro.",
    # s44
    "Na prática, o número diz qual metade está com defeito. Preso em zero ou no topo é fio solto ou falha no trilho, no seletor. Se mexe normal, o seletor está bem: olhe o lado do LED.",
    # s44b
    "Diferente do termômetro: imprimir leva tempo, e prints demais podem frear um loop rápido. Tire-os ao terminar.",
    # s45
    "Por que o pino trinta e quatro? Porque os pinos não são iguais. De trinta e quatro a trinta e nove são portas de mão única: só escutam, então não acendem um LED.",
    # s46
    "Segunda regra: alguns pinos, como vinte e cinco a vinte e sete, não leem analógico com Wi-Fi ligado. O trinta e quatro segue firme: nossos sensores moram nele.",
    # s47
    "Terceira regra: os pinos zero, dois, cinco, doze e quinze são checados ao ligar, então os deixamos livres. Não precisa decorar. O mapa completo está na pasta da aula.",
    # s48
    "Agora pause e explique com suas palavras por que dividimos por dezesseis. Uma frase basta.",
    # s49
    "Um jeito de dizer: a escala do seletor é dezesseis vezes maior que a do brilho, então dividir as faz coincidir.",
    # s50
    "Sua vez: Knob Blink Speed. O LED pisca o tempo todo, e o seletor escolhe a velocidade em três zonas: a cada cem milissegundos, a cada quatrocentos e a cada segundo.",
    # s51
    "A reviravolta: nada pode esperar com delay(). As zonas de hoje escolhem o intervalo, e o truque millis() do episódio quatro faz o pisca.",
    # s52
    "Hoje você aprendeu três coisas. O seletor transforma posição em tensão. analogRead() transforma tensão em número. E imprimir o número mostra onde está o problema.",
    # s53
    "Na próxima: uma função que divide por nós e uma barra de LEDs que enche ao girar. Poste seu código de velocidade nos comentários; uma solução está na pasta da aula. Até lá!",
]

ES = [
    # s01
    "Mira mi mano. Giro una perilla y el LED la sigue, más fuerte y más débil, en cuanto me muevo.",
    # s02
    "Al final de este video leerás cualquier perilla con una línea de código. Y cuando no funcione, sabrás hallar el problema.",
    # s03
    "Primero, dos del episodio pasado. Pregunta rápida: setColor() con doscientos cincuenta y cinco, doscientos cincuenta y cinco y cero. ¿Qué color da el RGB?",
    # s04
    "Amarillo. Luz roja más luz verde da amarillo, porque la luz se suma.",
    # s05
    "Pregunta rápida: el LED RGB se apaga, los tres colores juntos. ¿Qué cable revisas primero?",
    # s06
    "El cable común, en la pata más larga. Los tres colores vuelven a tierra por ahí.",
    # s07
    "Necesitas el circuito del episodio pasado, un potenciómetro de diez kilo-ohmios, una perilla de tres patas, y unos cables.",
    # s08
    "Hasta ahora solo leímos un botón, que tiene dos respuestas: pulsado o no. Una perilla responde cuánto.",
    # s09
    "Imagina un tobogán de parque. Arriba hay tres coma tres voltios, abajo está tierra, y la perilla decide a qué altura te sientas.",
    # s10
    "En realidad, dentro de la perilla hay una tira de resistencia con un contacto que se desliza. Las patas de afuera van a tres coma tres voltios y a tierra, y la del medio da el voltaje del contacto.",
    # s11
    "Eso es un divisor de voltaje. A diferencia del tobogán, nada baja solo. El contacto queda donde lo dejes.",
    # s12
    "Pregunta rápida: perilla justo en medio. ¿Cuántos voltios hay, más o menos, en la pata del medio?",
    # s13
    "Unos uno coma sesenta y cinco voltios, mitad de tres coma tres. Cada posición de la perilla es un voltaje.",
    # s14
    "Aquí está el mismo circuito como esquema, un dibujo con solo las conexiones. El zigzag es la resistencia, y la flecha, el contacto deslizante.",
    # s15
    "Desconecta el cable USB. La perilla va en la protoboard derecha, debajo del LED. Una pata de afuera va al riel positivo y la otra al negativo.",
    # s16
    "Un cable largo lleva la pata del medio a D treinta y cuatro. Si los rieles están cortados al medio, pon un puente en cada uno.",
    # s17
    "Una regla: el riel positivo debe ser de tres coma tres voltios, nunca cinco. Una entrada del ESP32 solo aguanta tres coma tres.",
    # s18
    "Para leer ese voltaje usamos una función nueva: analogRead(). Piensa en una regla de cuatro mil noventa y seis marcas, a lo largo del tobogán.",
    # s19
    "En realidad, analogRead() mide el voltaje de un pin y devuelve un número. Cero es cero voltios, y cuatro mil noventa y cinco son tres coma tres voltios.",
    # s20
    "A diferencia de una regla, esta no es perfecta. Cerca de los extremos se aplana un poco, y quizá nunca veas cero o cuatro mil noventa y cinco exactos.",
    # s21
    "Este es el sketch completo, pot_read, y es pequeñito. El pin treinta y cuatro recibe nombre, y setup() solo inicia el Serial Monitor. Un pin que solo se lee no necesita pinMode().",
    # s22
    "En el loop, analogRead() pone un número en value. Lo imprimimos y esperamos una décima de segundo. Pausa y predice: con la perilla en medio, ¿qué número esperas?",
    # s23
    "Unos dos mil, la mitad de la escala. Al girar la perilla, el número del Serial Monitor sube con ella, del inicio de la escala al tope.",
    # s24
    "Ahora la perilla debe hacer algo. analogWrite() fija el brillo, pero solo acepta de cero a doscientos cincuenta y cinco, y la perilla da hasta cuatro mil noventa y cinco. ¿Cómo lo ajustamos?",
    # s25
    "Dividiendo. Cuatro mil noventa y cinco entre dieciséis son unos doscientos cincuenta y cinco, y los extremos de la perilla caen en los del brillo.",
    # s26
    "Este es pot_dimmer. Leemos la perilla en value, dividimos entre dieciséis en brightness, y analogWrite() lo muestra en el LED.",
    # s27
    "Pausa y predice: si dividiéramos entre treinta y dos, ¿qué cambiaría?",
    # s28
    "El número mayor sería unos ciento veintisiete, y el LED quedaría a media potencia, por mucho que gires la perilla.",
    # s29
    "Ahora en serio, con un medidor en la pata del medio. Al girar, los voltios van de cero a tres coma tres, y el LED los sigue.",
    # s30
    "A veces no quieres todos los valores, solo pocas opciones, como las marcas baja, media y alta de la estufa.",
    # s31
    "En realidad, la perilla da un número, y el código lo clasifica. Cuatro mil noventa y cinco entre tres son unos mil trescientos sesenta y cinco: cortamos ahí y en dos mil setecientos treinta.",
    # s32
    "A diferencia de la estufa, esta perilla no tiene clics. Las zonas existen solo en el código.",
    # s33
    "Este es el sketch pot_zones. Bajo mil trescientos sesenta y cinco, el LED recibe veinte, tenue. Si no, bajo dos mil setecientos treinta, ciento veinte. Si no, brillo total.",
    # s34
    "Pausa y predice: la lectura es exactamente mil trescientos sesenta y cinco. ¿En qué zona está?",
    # s35
    "En la del medio. Menor que es estricto: mil trescientos sesenta y cinco falla la primera prueba y pasa la segunda.",
    # s36
    "Gira despacio: tenue, medio y total, en tres escalones claros.",
    # s37
    "Una cosa más. Deja la perilla quieta y mira el número. Aún tiembla un poco, como una báscula de baño que nunca se asienta.",
    # s38
    "En realidad, un ruido eléctrico diminuto cambia cada lectura. La solución es la de la báscula: mide cuatro veces y saca el promedio.",
    # s39
    "A diferencia de la báscula, cuatro lecturas toman a la placa mucho menos de un milisegundo, y no pierdes tiempo.",
    # s40
    "En pot_smooth, sum empieza en cero. Un ciclo for corre cuatro veces y suma una lectura nueva en cada vuelta. Luego, sum entre cuatro es el promedio.",
    # s40b
    "Pausa y predice: en una gráfica, ¿qué línea tiembla menos, la lectura sola o el promedio?",
    # s41
    "El promedio. El Serial Plotter dibuja ambas: la lectura sola tiembla, y el promedio es más calmado.",
    # s42
    "Ahora el problema que encontrarás. El LED no reacciona a la perilla. Pregunta rápida: ¿es el LED, la perilla o el código? ¿Qué haces primero?",
    # s43
    "Imprime el valor, antes de confiar en nada. El médico toma la temperatura antes de recetar, y la línea de impresión es tu termómetro.",
    # s44
    "En realidad, el número dice qué mitad falla. Pegado en cero o en el tope es un cable suelto o un hueco del riel en la perilla. Si se mueve normal, la perilla está bien: mira el lado del LED.",
    # s44b
    "A diferencia del termómetro, imprimir toma tiempo, y demasiados prints pueden frenar un loop rápido. Quítalos al terminar.",
    # s45
    "¿Por qué el pin treinta y cuatro? No todos son iguales. Del treinta y cuatro al treinta y nueve son puertas de un sentido: solo escuchan, no encienden un LED.",
    # s46
    "Segunda regla: algunos pines, como del veinticinco al veintisiete, no leen analógico con Wi-Fi activo. El treinta y cuatro sigue firme: ahí viven nuestros sensores.",
    # s47
    "Tercera regla: los pines cero, dos, cinco, doce y quince se revisan al encender, así que los dejamos libres. No hace falta memorizar. El mapa completo está en la carpeta de la lección.",
    # s48
    "Ahora pausa y explica con tus palabras por qué dividimos entre dieciséis. Una frase basta.",
    # s49
    "Una forma de decirlo: la escala de la perilla es dieciséis veces mayor que la del brillo, y dividir las iguala.",
    # s50
    "Tu turno: Knob Blink Speed. El LED parpadea siempre, y la perilla elige la velocidad en tres zonas: cada cien milisegundos, cada cuatrocientos y cada segundo.",
    # s51
    "El giro: nada puede esperar con delay(). Las zonas de hoy eligen el intervalo, y el truco de millis() del episodio cuatro hace el parpadeo.",
    # s52
    "Hoy aprendiste tres cosas. Una perilla convierte posición en voltaje. analogRead() convierte voltaje en un número. E imprimir ese número muestra dónde está el problema.",
    # s53
    "Después: una función que divide por nosotros y una barra de LEDs que se llena al girar. Publica tu código de velocidad en los comentarios; hay una solución en la carpeta. ¡Nos vemos!",
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
