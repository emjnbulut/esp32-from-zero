"""Source of video/ep08/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, is edited in dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
Usage: python video/ep08/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
EXTRA = {  # s25b, added after the first narration (pin 17 is printed TX2)
    "hi": "ध्यान दें: ज़्यादातर boards पर pin सत्रह पर D सत्रह नहीं, TX दो लिखा होता है।",
    "pt": "Atenção com o último: na maioria das placas, o pino dezessete aparece como TX dois, não D dezessete.",
    "es": "Cuidado con el último: en casi todas las placas, el pin diecisiete dice TX dos, no D diecisiete.",
}
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "देखिए ये रोशनी की पट्टी। Knob घुमाता हूँ, और ये भरती है: हरी, फिर पीली, फिर लाल, volume meter जैसी।",
    # s02
    "इस video के अंत तक आप एक function से संख्याओं का एक पैमाना दूसरे में बदलेंगे, और ये पट्टी खुद बनाएँगे।",
    # s03
    "पहले, पिछले episode से दो सवाल। छोटा सवाल: knob ठीक बीच में है। analogRead() लगभग कौन सी संख्या देगा?",
    # s04
    "करीब दो हज़ार, पैमाने का आधा। पूरा पैमाना लगभग चार हज़ार तक जाता है।",
    # s05
    "छोटा सवाल: LED knob की सुनती ही नहीं। सबसे पहले क्या करेंगे?",
    # s06
    "Value print करते हैं, जैसे डॉक्टर बुखार नापता है। संख्या बताती है circuit का कौन सा हिस्सा देखना है।",
    # s07
    "पिछले episode का circuit चाहिए, knob और लाल LED के साथ। एक पीली LED, एक हरी LED, हर एक के लिए दो सौ बीस ओम का resistor, और कुछ wires जोड़िए।",
    # s08
    "पिछली बार हमने knob के बड़े पैमाने को सोलह से भाग देकर LED के छोटे पैमाने में बिठाया। चला, पर code पढ़ने वाले को सोचना पड़ता है कि सोलह कहाँ से आया।",
    # s09
    "शहर का नक्शा सोचिए। शहर की हर सड़क की कागज़ पर अपनी जगह है, और शहर के बीच का मतलब नक्शे का बीच।",
    # s10
    "ठीक इसी नाम का एक function Arduino में है: map()। उसे संख्या दीजिए, जिस पैमाने से आई वो, और जो चाहिए वो, तो वो मिलती-जुलती संख्या लौटाता है।",
    # s11
    "असल में map() सीधा हिसाब है। वो देखता है आपकी संख्या पहले पैमाने में कितनी आगे है, और दूसरे पैमाने में वही जगह लौटाता है।",
    # s12
    "कागज़ी नक्शे से फ़र्क: वो सिर्फ़ छोटा कर सकता है। map() छोटे पैमाने को बड़ा भी कर सकता है, या उलट भी दे, यानी ऊपर वाला नीचे हो जाए।",
    # s13
    "ये रही line। पहले संख्या, यानी knob की value। फिर knob का पैमाना कहाँ से कहाँ तक। फिर चमक का पैमाना कहाँ से कहाँ तक।",
    # s14
    "छोटा सवाल: knob लगभग दो हज़ार पढ़ता है, करीब बीच में। map() कितनी चमक लौटाएगा?",
    # s15
    "करीब एक सौ सत्ताईस, चमक के पैमाने का बीच। बीच में अंदर, बीच में बाहर।",
    # s16
    "ये रहा पूरा sketch, map_dimmer। ये पिछला dimmer ही है, बस एक बदलाव: भाग वाली line अब map() वाली है।",
    # s17
    "Loop में analogRead() knob की संख्या value में रखता है। फिर map() उसे brightness बनाता है, और आख़िरी line उसे लाल LED को भेजती है।",
    # s18
    "Video रोकिए और अंदाज़ा लगाइए: क्या सोलह से भाग वाले पिछले version से LED अलग दिखेगी?",
    # s19
    "नहीं। वैसी ही, अँधेरे से पूरी चमक तक चिकनी। फ़र्क code में है: ये line पढ़ते ही दोनों पैमाने दिख जाते हैं।",
    # s20
    "अब एक चीज़ बदलते हैं। Video रोकिए, अंदाज़ा लगाइए: आख़िरी दो संख्याएँ पलट दें, चमक दो सौ पचपन से शून्य की ओर चले, तो?",
    # s21
    "Knob उल्टा चलता है। बाएँ घुमाओ तो LED तेज़, दाएँ घुमाओ तो बुझ जाती है। यही वो उलटना था।",
    # s22
    "अब रोशनी की पट्टी। फ़ोन का battery icon सोचिए: जितना charge, उतनी पट्टियाँ।",
    # s23
    "असल में हम knob की संख्या को छोटे level में बदलते हैं, शून्य से तीन तक। Level बताता है कितनी LED जलें, हरी से गिनकर।",
    # s24
    "फ़ोन से फ़र्क: फ़ोन हर पट्टी के पीछे कई छोटे कदम छिपाता है। हमारी पट्टी के सिर्फ़ चार हाल हैं, खाली से भरी तक।",
    # s25
    "Cable निकालिए। पीली LED pin अठारह पर, और हरी pin सत्रह पर। हर एक का अपना resistor, लाल की तरह।",
    # s26
    "लंबा पैर pin की तरफ़, छोटा पैर minus rail की तरफ़। ये याद रखिए, एक मिनट में काम आएगा।",
    # s27
    "भीड़ लगे तो knob को ऊपर सरका दीजिए, उसके wires साथ चले जाएँगे। Rails बीच से कटी हों, तो bridge wires रखिए।",
    # s28
    "अब level। सीधी line knob के पैमाने को शून्य से तीन पर बिठाती है।",
    # s29
    "Video रोकिए, अंदाज़ा लगाइए: इस line से तीनों LED कितनी बार एक साथ जलेंगी?",
    # s30
    "लगभग कभी नहीं। map() पूरी संख्याओं पर चलता है, दशमलव के बाद का हिस्सा गिरा देता है। दो दशमलव नौ, दो बनता है।",
    # s31
    "Level तीन पैमाने के आख़िरी निशान पर ही आता है। और पिछली बार देखा, पैमाना उस निशान तक शायद पहुँचे ही नहीं।",
    # s32
    "हल: चार level माँगिए, और मान लीजिए पैमाना एक निशान लंबा है। Reading चार तक नहीं जाती, तीन पर रुकती है, और हर level को knob का बराबर टुकड़ा मिलता है।",
    # s33
    "ये sketch है, level_bar। setup() तीन pins को output बनाता है। Loop में knob पढ़कर map() से level लेते हैं।",
    # s34
    "फिर चूल्हे के निशान, if और else if। Level शून्य पर तीनों बंद। Level एक पर सिर्फ़ हरी, level दो पर पीली भी।",
    # s35
    "इनमें से कोई नहीं, तो तीन होगा, इसलिए आख़िरी else सब जला देता है।",
    # s36
    "Video रोकिए, अंदाज़ा लगाइए: knob बीच से थोड़ा आगे है। कौन सी LED जलेंगी?",
    # s37
    "हरी और पीली। बीच से थोड़ा आगे level दो है।",
    # s38
    "असली में देखिए। धीरे घुमाइए, पट्टी एक-एक रोशनी से भरती है, फिर खाली होती है।",
    # s39
    "अब एक ग़लती जो हो सकती है। हरी और लाल जलती हैं, पर पीली बुझी है। छोटा सवाल: ग़लती code में है या wiring में?",
    # s40
    "पहले बुखार नापिए। Serial Monitor कहता है level तीन, यानी code पीली जलाना चाहता है। गड़बड़ी wiring की तरफ़ है।",
    # s41
    "पीली LED उल्टी लगी है। LED करंट सिर्फ़ एक तरफ़ जाने देती है, लंबे पैर से छोटे पैर की ओर।",
    # s42
    "उल्टी हो तो बस बुझी रहती है, कुछ ख़राब नहीं होता। पलट दीजिए, पट्टी पूरी हो जाएगी।",
    # s43
    "अब video रोकिए, और अपने शब्दों में बताइए कि पहली level वाली line तीनों LED लगभग कभी क्यों नहीं जलाती थी। एक वाक्य काफ़ी।",
    # s44
    "एक तरीका: map() नीचे गोल करता है, इसलिए सबसे ऊँचा level पैमाने के आख़िर में ही आता था, जहाँ पैमाना कम पहुँचता है।",
    # s45
    "आपकी बारी: Rotary Safe Lock। Knob को शून्य से निन्यानवे पर बिठाइए और संख्या print कीजिए, knob तिजोरी का dial बन जाए।",
    # s46
    "गुप्त code लगातार तीन संख्याएँ हैं, और हर एक के बाद button दबाते हैं। संख्याएँ screen पर दिखती हैं।",
    # s47
    "तीनों सही हों तो episode छह वाली colour LED हरी हो जाती है। एक ग़लत दबाव पर लाल चमकती है, और पहली संख्या से फिर शुरू।",
    # s48
    "पेंच: knob कभी ठीक नहीं होता, तो हर लक्ष्य के दोनों तरफ़ कुछ संख्याएँ मान लीजिए। आपको दो ampersand वाला and चाहिए, यानी दोनों जाँचें सही हों।",
    # s49
    "एक इशारा: step नाम का एक variable याद रख सकता है कि कितनी संख्याएँ सही हो चुकीं।",
    # s50
    "आज तीन बातें सीखीं। map() संख्या को एक पैमाने से दूसरे में बदलता है। वो हमेशा नीचे गोल करता है, इसलिए पैमाने सोचकर चुनिए। और उल्टी LED बस बुझी रहती है।",
    # s51
    "अगली बार हमारा पहला mini project: पैदल पार पथ, जिसमें car lights, walk light, button और आज का knob होगा। Safe lock का code comments में डालिए; हल lesson folder में है। फिर मिलते हैं!",
]

PT = [
    # s01
    "Olhe esta barra de luzes. Giro o seletor e ela enche: verde, amarela, vermelha, como um medidor.",
    # s02
    "No fim deste vídeo, você muda uma faixa de números em outra com uma só função, e monta esta barra sozinho.",
    # s03
    "Primeiro, duas perguntas do episódio passado. Pergunta rápida: seletor no meio. Que número analogRead() dá?",
    # s04
    "Uns dois mil, metade da régua. A régua toda vai até uns quatro mil.",
    # s05
    "Pergunta rápida: o LED ignora o seletor. Qual é a primeira coisa que você faz?",
    # s06
    "Imprime o valor, como o médico mede a febre. O número diz qual metade do circuito olhar.",
    # s07
    "Use o circuito passado, com o seletor e o LED vermelho. Junte um LED amarelo, um verde, um resistor de duzentos e vinte ohms para cada.",
    # s08
    "Da outra vez, encaixamos a escala grande do seletor na do LED, dividindo por dezesseis. Funcionou, mas quem lê o código precisa adivinhar esse dezesseis.",
    # s09
    "Pense num mapa da cidade. Cada rua tem seu lugar no papel, e o meio da cidade é o meio do mapa.",
    # s10
    "O Arduino tem uma função com esse nome: map(). Você dá um número, a faixa de origem e a faixa que quer, e ela devolve o número equivalente.",
    # s11
    "Na verdade, map() é só conta. Ela vê quanto o número andou na primeira faixa e devolve a mesma posição na segunda.",
    # s12
    "A diferença do mapa de papel: ele só encolhe. A map() também estica uma faixa pequena, ou inverte, e o topo vira o fundo.",
    # s13
    "Aqui está a linha. Primeiro o número, o valor do seletor. Depois onde a faixa do seletor começa e termina. Depois a faixa do brilho.",
    # s14
    "Pergunta rápida: o seletor lê uns dois mil, quase no meio. Que brilho a map() devolve?",
    # s15
    "Uns cento e vinte e sete, o meio do brilho. Entra no meio, sai no meio.",
    # s16
    "Aqui o sketch inteiro, map_dimmer. É o dimmer passado com uma mudança: a linha da divisão agora é map().",
    # s17
    "No loop, analogRead() põe o número do seletor em value. A map() transforma em brightness, e a última linha manda ao LED vermelho.",
    # s18
    "Pause o vídeo e preveja: o LED fica diferente da versão passada, a que dividia por dezesseis?",
    # s19
    "Não. Igual, suave do escuro ao máximo. A diferença está no código: quem lê a linha vê as duas faixas.",
    # s20
    "Agora mudamos uma coisa. Pause e preveja: se trocarmos os dois últimos números, e o brilho for de duzentos e cinquenta e cinco até zero?",
    # s21
    "O seletor funciona ao contrário. À esquerda o LED fica forte, à direita apaga. Essa é a inversão que citei.",
    # s22
    "Agora a barra de luzes. Pense no ícone de bateria do celular: mais carga, mais barras.",
    # s23
    "Na verdade, o número do seletor vira um nível, de zero a três. O nível diz quantos LEDs acendem, a partir do verde.",
    # s24
    "A diferença do celular: ele esconde muitos passinhos em cada barra. A nossa tem só quatro estados, de vazia a cheia.",
    # s25
    "Tire o cabo. O LED amarelo vai no pino dezoito e o verde no dezessete. Cada um com seu resistor, como o vermelho.",
    # s26
    "Perna longa para o pino, perna curta para o trilho de menos. Guarde isso, já volta.",
    # s27
    "Se apertar, suba o seletor, e os fios vão junto. Se os trilhos forem divididos no meio, mantenha as pontes.",
    # s28
    "Agora o nível. A linha óbvia leva a faixa para zero a três.",
    # s29
    "Pause e preveja: com essa linha, quantas vezes os três LEDs acendem?",
    # s30
    "Quase nunca. A map() usa números inteiros e corta o que vem depois da vírgula. Dois vírgula nove vira dois.",
    # s31
    "O nível três só vem na última marca da régua. E vimos que a régua pode nem chegar nessa marca.",
    # s32
    "A solução: peça quatro níveis e finja que a régua tem uma marca a mais. A leitura nunca chega a quatro, para em três, e cada nível ganha uma fatia igual.",
    # s33
    "Aqui o sketch, level_bar. O setup() põe três pinos como saída. No loop, lemos o seletor e a map() dá o nível.",
    # s34
    "Depois, as marcas do fogão, if e else if. Nível zero apaga tudo. Nível um acende o verde, e o dois soma o amarelo.",
    # s35
    "Se não for nenhum, só pode ser três: o último else acende tudo.",
    # s36
    "Pause e preveja: o seletor passou um pouco do meio. Quais LEDs acendem?",
    # s37
    "Verde e amarelo. Passou do meio: nível dois.",
    # s38
    "Agora de verdade. Gire devagar, e a barra enche uma luz por vez, depois esvazia.",
    # s39
    "Agora um erro possível. Verde e vermelho acendem, o amarelo não. Pergunta rápida: é o código ou a fiação?",
    # s40
    "Meça a febre primeiro. O Serial Monitor diz nível três, então o código quer o amarelo. O problema é a fiação.",
    # s41
    "O LED amarelo está ao contrário. Ele só deixa a corrente passar num sentido, da perna longa à curta.",
    # s42
    "Ao contrário, ele só fica apagado, sem estragar. Vire, e a barra fica completa.",
    # s43
    "Agora pause e explique com suas palavras por que a primeira linha quase nunca acendia os três LEDs. Uma frase basta.",
    # s44
    "Um jeito: a map() arredonda para baixo, então o nível máximo só vinha no fim da régua, e ela raramente chega lá.",
    # s45
    "Sua vez: o Rotary Safe Lock. Leve o seletor a zero até noventa e nove e imprima o número: ele vira o disco de um cofre.",
    # s46
    "O código são três números seguidos, e você aperta o botão após cada um. Os números aparecem na tela.",
    # s47
    "Acertou os três, o LED colorido do episódio seis fica verde. Um erro pisca vermelho, e você volta ao primeiro número.",
    # s48
    "A manha: o seletor nunca é exato, então aceite alguns números de cada lado do alvo. Use o and, dois e comerciais: as duas condições valem.",
    # s49
    "Uma dica: uma variável chamada step lembra quantos números já estão certos.",
    # s50
    "Hoje você aprendeu três coisas. A map() leva um número de uma faixa a outra. Sempre arredonda para baixo, então planeje. LED ao contrário só fica apagado.",
    # s51
    "Próximo: nosso primeiro mini projeto, uma faixa de pedestres, com luzes de carro, luz de travessia, botão e o seletor. Poste seu código do cofre nos comentários; há solução na pasta. Até lá!",
]

ES = [
    # s01
    "Mira esta barra de luces. Giro la perilla y se llena: verde, amarilla, roja, como un medidor.",
    # s02
    "Al final de este video, conviertes un rango de números en otro con una sola función, y armas esta barra tú mismo.",
    # s03
    "Primero, dos preguntas del episodio pasado. Pregunta rápida: perilla en el medio. ¿Qué número da analogRead()?",
    # s04
    "Unos dos mil, la mitad de la regla. La regla entera llega a unos cuatro mil.",
    # s05
    "Pregunta rápida: el LED ignora la perilla. ¿Qué es lo primero que haces?",
    # s06
    "Imprimes el valor, como el doctor que mide la fiebre. El número dice qué mitad del circuito revisar.",
    # s07
    "Usa el circuito pasado, con la perilla y el LED rojo. Suma un LED amarillo, uno verde, una resistencia de doscientos veinte ohmios para cada uno.",
    # s08
    "La vez pasada ajustamos la escala grande de la perilla a la del LED, dividiendo entre dieciséis. Funcionó, pero quien lee el código debe adivinar ese dieciséis.",
    # s09
    "Piensa en un mapa de la ciudad. Cada calle tiene su lugar en el papel, y la mitad de la ciudad es la mitad del mapa.",
    # s10
    "Arduino tiene una función con ese nombre: map(). Le das un número, el rango de origen y el que quieres, y devuelve el número equivalente.",
    # s11
    "En realidad, map() es pura aritmética. Calcula cuánto avanzó tu número en el primer rango y devuelve la misma posición en el segundo.",
    # s12
    "La diferencia con el mapa de papel: ese solo encoge. map() también estira un rango pequeño, o lo invierte, y lo de arriba queda abajo.",
    # s13
    "Esta es la línea. Primero el número, el valor de la perilla. Luego dónde empieza y termina el rango de la perilla. Luego el del brillo.",
    # s14
    "Pregunta rápida: la perilla lee unos dos mil, casi en el medio. ¿Qué brillo devuelve map()?",
    # s15
    "Unos ciento veintisiete, el medio del brillo. Entra en el medio, sale en el medio.",
    # s16
    "Aquí el sketch completo, map_dimmer. Es el dimmer pasado con un cambio: la división ahora es map().",
    # s17
    "En el loop, analogRead() guarda el número de la perilla en value. map() lo vuelve brightness, y la última línea lo manda al LED rojo.",
    # s18
    "Pausa el video y predice: ¿se verá distinto el LED que en la versión pasada, la que dividía entre dieciséis?",
    # s19
    "No. Igual, suave de oscuro a pleno. La diferencia está en el código: quien lee la línea ve los dos rangos.",
    # s20
    "Ahora cambiamos algo. Pausa y predice: si cambiamos los dos últimos números, y el brillo va de doscientos cincuenta y cinco a cero, ¿qué pasa?",
    # s21
    "La perilla funciona al revés. A la izquierda el LED brilla, a la derecha se apaga. Esa es la inversión que mencioné.",
    # s22
    "Ahora la barra de luces. Piensa en el ícono de batería del celular: más carga, más barras.",
    # s23
    "En realidad, el número de la perilla se vuelve un nivel, de cero a tres. El nivel dice cuántos LEDs encienden, desde el verde.",
    # s24
    "La diferencia con el celular: él esconde muchos pasitos en cada barra. La nuestra tiene solo cuatro estados.",
    # s25
    "Desconecta el cable. El LED amarillo va al pin dieciocho y el verde al diecisiete. Cada uno con su resistencia, como el rojo.",
    # s26
    "Pata larga hacia el pin, pata corta hacia el riel de menos. Recuérdalo, vuelve en un momento.",
    # s27
    "Si se aprieta, sube la perilla, y sus cables suben con ella. Si tus rieles están partidos en el medio, deja los puentes.",
    # s28
    "Ahora el nivel. La línea obvia lleva el rango a cero a tres.",
    # s29
    "Pausa y predice: con esta línea, ¿cuántas veces encienden los tres LEDs?",
    # s30
    "Casi nunca. map() usa enteros y corta lo que viene tras el punto. Dos coma nueve se vuelve dos.",
    # s31
    "El nivel tres solo llega en la última marca de la regla. Y vimos que la regla quizá nunca llega a esa marca.",
    # s32
    "La solución: pide cuatro niveles y finge que la regla tiene una marca más. La lectura nunca llega a cuatro, se queda en tres, y cada nivel recibe una porción igual.",
    # s33
    "Aquí el sketch, level_bar. setup() pone tres pines de salida. En el loop leemos la perilla y map() da el nivel.",
    # s34
    "Luego, las marcas de la estufa, if y else if. Nivel cero apaga todo. Nivel uno enciende el verde, y el dos suma el amarillo.",
    # s35
    "Si no es ninguno, tiene que ser tres: el último else enciende todo.",
    # s36
    "Pausa y predice: la perilla pasó un poco el medio. ¿Qué LEDs encienden?",
    # s37
    "Verde y amarillo. Pasó el medio: nivel dos.",
    # s38
    "Ahora de verdad. Gira despacio, y la barra se llena una luz a la vez, y luego se vacía.",
    # s39
    "Ahora un error posible. El verde y el rojo encienden, pero el amarillo no. Pregunta rápida: ¿es el código o el cableado?",
    # s40
    "Mide la fiebre primero. El Serial Monitor dice nivel tres: el código quiere el amarillo. El problema es el cableado.",
    # s41
    "El LED amarillo está al revés. Deja pasar la corriente en un solo sentido, de la pata larga a la corta.",
    # s42
    "Al revés solo queda apagado, sin dañarse. Dale la vuelta, y la barra queda completa.",
    # s43
    "Ahora pausa y explica con tus palabras por qué la primera línea casi nunca encendía los tres LEDs. Una frase basta.",
    # s44
    "Una forma: map() redondea hacia abajo, así que el nivel máximo solo venía al final de la regla, y casi nunca llega.",
    # s45
    "Tu turno: la Rotary Safe Lock. Lleva la perilla de cero a noventa y nueve e imprime el número: será el disco de la caja fuerte.",
    # s46
    "El código son tres números seguidos, y presionas el botón tras cada uno. Los números salen en pantalla.",
    # s47
    "Si aciertas los tres, el LED de color del episodio seis se pone verde. Un error parpadea rojo, y vuelves al primer número.",
    # s48
    "El truco: la perilla nunca es exacta, así que acepta unos números a cada lado del objetivo. Usa el and, dos ampersands: ambas condiciones deben cumplirse.",
    # s49
    "Una pista: una variable llamada step recuerda cuántos números ya están bien.",
    # s50
    "Hoy aprendiste tres cosas. map() lleva un número de un rango a otro. Siempre redondea hacia abajo, así que planea. Un LED al revés solo queda apagado.",
    # s51
    "Lo próximo: nuestro primer mini proyecto, un cruce peatonal, con luces de auto, luz de paso, botón y la perilla. Publica tu código de la caja fuerte en los comentarios; hay solución en la carpeta.",
]

TARGET = {"hi": 1.0, "pt": 1.0, "es": 1.0}


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
        if len(lines) == 51 and "s25b" in IDS:
            lines = lines[:IDS.index("s25b")] + [EXTRA[lang]] + lines[IDS.index("s25b"):]
        assert len(lines) == len(IDS), (lang, len(lines), len(IDS))
        seg = dict(zip(IDS, lines))
        langs[lang] = seg
        (out / f"{lang}.json").write_text(json.dumps({"voice": voice, "rate": "+0%", "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("dubs written:", ", ".join(langs))
    check(langs, english)
