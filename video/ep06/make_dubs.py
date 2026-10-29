"""Source of video/ep06/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, is edited in dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
Usage: python video/ep06/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "एक LED, जो रंग आप चाहें। लाल, हरा, नीला, और एक बार दबाते ही नीले से लाल तक धीमा बदलाव।",
    # s02
    "इस video के अंत तक आप अपने रंग खुद मिलाएँगे, और एक बटन उनमें से चुनेगा।",
    # s03
    "पहले, पिछले episode से दो सवाल। छोटा सवाल: एक सौ अट्ठाईस के साथ analogWrite() LED का क्या करता है?",
    # s04
    "यह हर चक्र के करीब आधे समय pin on रखता है, बहुत तेज़ी से। आँख को मध्यम रोशनी दिखती है, पर pin कभी आधा on नहीं होता।",
    # s05
    "छोटा सवाल: बिना delay वाले fade में बटन किसी भी पल क्यों काम करता है?",
    # s06
    "क्योंकि loop कभी रुकता नहीं। वह घड़ी देखता है, समय होने पर ही कदम लेता है, और हर चक्कर में बटन जाँचता है।",
    # s07
    "आपको चाहिए episode पाँच का circuit, एक RGB LED, दो सौ बीस ohm के तीन और resistors, और कुछ wires।",
    # s08
    "अपने phone की screen को बहुत पास से देखिए, हर जगह छोटे लाल, हरे और नीले बिंदु मिलेंगे। हर रंग इन्हीं तीन से बनता है।",
    # s09
    "RGB LED भी यही है। असल में होता यह है: एक package में तीन छोटी LEDs, लाल, हरी और नीली। उनका एक पैर साझा है, सबसे लंबा वाला।",
    # s10
    "Paint से फ़र्क: रोशनी जुड़ती है। लाल और हरा paint भूरा बनाते हैं, पर लाल और हरी रोशनी पीला, और तीनों मिलकर सफ़ेद।",
    # s11
    "USB cable निकालिए, और ऊपर के breadboard से हरी LED हटाइए। हमें उसका pin चाहिए, GPIO पच्चीस।",
    # s12
    "RGB LED लगाइए, सबसे लंबा पैर बाएँ से दूसरा। एक काला wire उस लंबे पैर को minus rail से जोड़ता है।",
    # s13
    "हर रंग का अपना resistor और अपना pin: लाल D पच्चीस पर, हरा D छब्बीस पर, और नीला D सत्ताईस पर।",
    # s14
    "छोटा सवाल: तीन resistors क्यों, साझा पैर पर बस एक क्यों नहीं?",
    # s15
    "क्योंकि हर रंग अलग LED है, अपने current के साथ। एक साझा resistor ऐसा है जैसे तीन लोग एक straw से पिएँ: जो ज़ोर से खींचे, उसे ज़्यादा मिले।",
    # s16
    "असल में होता यह है: रंग एक-दूसरे का current छीनेंगे, और आपका mix बदल जाएगा। Straw से फ़र्क: यहाँ सबसे कम voltage वाला रंग, लाल, सबसे ज़्यादा लेता है।",
    # s17
    "एक बात जाँचिए: ज़्यादातर kits में common cathode LEDs होती हैं, लंबा पैर ground पर। आपकी उल्टी हो, तो code में उसके लिए एक line है।",
    # s18
    "रंग set करने के लिए हम एक helper function लिखते हैं: setColor()। यह coffee machine के बटन जैसा है। एक बार दबाइए, और तीन चीज़ें सही मात्रा में।",
    # s19
    "असल में यह analogWrite() को तीन बार चलाता है, हर रंग के pin पर एक बार, शून्य से दो सौ पचपन तक के तीन numbers के साथ।",
    # s20
    "Coffee machine से फ़र्क: यह कोई recipe याद नहीं रखता। तीनों मात्राएँ हर बार आपको बतानी होती हैं।",
    # s21
    "छोटा सवाल: लाल दो सौ पचपन, हरा शून्य, नीला दो सौ पचपन। कौन सा रंग बनेगा?",
    # s22
    "Magenta, गुलाबी-सा बैंगनी। और पूरे values ज़रूरी नहीं: लाल दो सौ पचपन के साथ बस चालीस हरा, नारंगी बनाता है।",
    # s23
    "यह रहा पूरा sketch, rgb_colors। तीन pin नाम, हर रंग का एक, और COMMON_ANODE नाम का switch, जो ज़्यादातर kits में false रहता है।",
    # s24
    "setColor() तीन numbers लेता है। LED common anode हो, तो पहले हर value उलट देता है, क्योंकि वहाँ दो सौ पचपन का मतलब off है।",
    # s25
    "Loop में हर line को लाल, हरा, नीला पढ़िए। Video रोकिए और चौथी line का अंदाज़ा लगाइए: दो सौ पचपन, दो सौ पचपन, शून्य। कौन सा रंग है?",
    # s26
    "पूरा लाल और पूरा हरा: पीला। हर रंग एक second रहता है, और नारंगी के बाद list फिर शुरू होती है।",
    # s27
    "चलाते हैं: लाल, हरा, नीला, पीला, magenta, cyan, सफ़ेद, और नारंगी।",
    # s27b
    "ध्यान दीजिए, पीला थोड़ा हरा दिखता है, और magenta थोड़ा नीला। तीनों रंग बराबर चमकीले नहीं हैं। संतुलन के लिए हरा और नीला कम करके देखिए।",
    # s28
    "छोटा सवाल: रंग बदल रहे हैं। यह काला wire निकल जाए तो क्या होगा?",
    # s29
    "देखिए। LED बुझ जाती है, सारे रंग एक साथ। Wire वापस लगाइए, और रंग लौट आते हैं।",
    # s30
    "Episode दो याद कीजिए: current को पूरा चक्कर चाहिए, pin से निकलकर ground तक वापस। साझा पैर ही तीनों रंगों का अकेला वापसी रास्ता है।",
    # s31
    "तो अगर एक रंग कभी न जले, उसी रंग का wire जाँचिए। अगर तीनों साथ बुझें, तो पहले साझा wire जाँचिए।",
    # s32
    "अब बटन रंग चुनता है, TV remote के channel बटन की तरह। हम mode नाम का number रखते हैं, और हर नया दबाव एक जोड़ता है।",
    # s33
    "छोटा सवाल: चार modes हैं, शून्य से तीन। mode तीन है, और आप फिर दबाते हैं। क्या होना चाहिए?",
    # s34
    "उसे शून्य पर लौटना चाहिए, जैसे remote आख़िरी channel से पहले पर कूदता है। असल में होता यह है: mode एक पल को चार बनता है, अगली line देखती है कि वह तीन से बड़ा है, और उसे शून्य कर देती है।",
    # s35
    "Remote से फ़र्क: number दिखाने वाली कोई screen नहीं। mode सिर्फ़ memory में रहता है, इसलिए print करना जाँचने का सबसे आसान तरीका है।",
    # s36
    "यह रहा पूरा sketch, color_modes। अच्छी खबर: इसमें सच में कुछ नया नहीं। यह episode चार का बटन, setColor(), और episode पाँच का fade है, एक साथ।",
    # s37
    "Loop के दूसरे हिस्से में हर mode का एक if है। else if का मतलब: इसे तभी जाँचो जब पहले वाले सब false हों। शून्य लाल, एक हरा, और दो नीला।",
    # s38
    "आख़िरी else mode तीन है, धीमा fade। हर आठ milliseconds पर level एक कदम लेता है, और setColor() को लाल के लिए level, नीले के लिए दो सौ पचपन माइनस level मिलता है।",
    # s39
    "Video रोकिए और अंदाज़ा लगाइए: fade के बीच में level करीब एक सौ अट्ठाईस है। कौन सा रंग दिखेगा?",
    # s40
    "बैंगनी। आधा लाल, आधा नीला। लाल बढ़े तो नीला घटता है, इसलिए दोनों मिलकर हमेशा दो सौ पचपन होते हैं।",
    # s41
    "चलाते हैं। तीन बार दबाया: लाल, हरा, नीला, और fade शुरू। हर दबाव रंग तुरंत बदलता है, fade के बीच में भी।",
    # s42
    "अब video रोकिए, और अपने शब्दों में बताइए कि तीन के बाद mode शून्य पर क्यों लौटता है। एक वाक्य काफ़ी है।",
    # s43
    "एक तरीका यह है: रंग सिर्फ़ चार हैं, तो जब गिनती आख़िरी से आगे जाती है, code चक्कर फिर से शुरू करता है।",
    # s44
    "आपकी बारी: camping के लिए smart headlamp बनाइए। एक बटन चार modes घुमाता है: off, हल्का सफ़ेद, तेज़ सफ़ेद, और लाल blink।",
    # s45
    "Twist: अगर lamp तीन second या ज़्यादा से on है, तो अगला दबाव उसे सीधे off कर दे। Hint: याद रखिए कि mode आख़िरी बार कब बदला।",
    # s46
    "आज आपने तीन बातें सीखीं। RGB LED एक में तीन LEDs है। setColor() उन्हें तीन numbers से मिलाता है। और mode counter से एक बटन चुन पाता है।",
    # s47
    "अगली बार: एक knob। हम potentiometer पढ़ेंगे, और उसे brightness में बदलेंगे। अपना headlamp comments में डालिए; एक हल lesson folder में है। वहीं मिलते हैं!",
]

PT = [
    # s01
    "Um LED, a cor que quiser. Vermelho, verde, azul e, num toque, uma troca lenta de azul a vermelho.",
    # s02
    "No fim do vídeo, você vai misturar suas cores e um botão vai escolher entre elas.",
    # s03
    "Antes, duas perguntas do último episódio. Pergunta rápida: o que analogWrite() com cento e vinte e oito faz num LED?",
    # s04
    "Ele liga o pino por cerca de metade de cada ciclo, bem rápido. Seu olho vê brilho médio, mas o pino nunca fica meio ligado.",
    # s05
    "Pergunta rápida: no fade sem delay, por que o botão funciona a qualquer momento?",
    # s06
    "Porque o loop nunca espera. Ele olha o relógio, dá um passo só quando é hora e confere o botão a cada volta.",
    # s07
    "Use o circuito do episódio cinco, um LED RGB, mais três resistores de duzentos e vinte ohms e alguns fios.",
    # s08
    "Olhe bem de perto a tela do celular e você verá pontinhos vermelhos, verdes e azuis por toda parte. Cada cor que você vê vem desses três.",
    # s09
    "Um LED RGB é a mesma ideia. Na verdade, são três LEDs pequenos numa peça só, vermelho, verde e azul. Eles dividem uma perna, a mais longa.",
    # s10
    "A diferença da tinta: luz se soma. Tinta vermelha e verde dá marrom, mas luz vermelha e verde dá amarelo, e as três dão branco.",
    # s11
    "Tire o cabo USB e o LED verde da protoboard de cima. Precisamos do pino dele, o GPIO vinte e cinco.",
    # s12
    "Encaixe o LED RGB com a perna mais longa na segunda posição da esquerda. Um fio preto a leva ao trilho negativo.",
    # s13
    "Cada cor tem seu resistor e seu pino: vermelho no D vinte e cinco, verde no D vinte e seis e azul no D vinte e sete.",
    # s14
    "Pergunta rápida: por que três resistores, e não só um na perna comum?",
    # s15
    "Porque cada cor é um LED próprio, com sua corrente. Um resistor só é como três pessoas bebendo pelo mesmo canudo: quem puxa mais forte leva mais.",
    # s16
    "O que acontece de fato: as cores roubariam corrente umas das outras, e sua mistura mudaria. A diferença do canudo: aqui leva mais a cor que precisa de menos tensão, o vermelho.",
    # s17
    "Algo a conferir: a maioria dos kits tem LEDs de catodo comum, com a perna longa no terra. Se o seu for ao contrário, o código tem uma linha pra isso.",
    # s18
    "Para definir uma cor, escrevemos uma função auxiliar: setColor(). É como um botão de cafeteira. Um toque, e ela põe a dose certa de três ingredientes.",
    # s19
    "Na prática, ela chama analogWrite() três vezes, uma por pino de cor, com três números de zero a duzentos e cinquenta e cinco.",
    # s20
    "A diferença da cafeteira: ela não lembra receitas. Você diz as três quantidades, toda vez.",
    # s21
    "Pergunta rápida: vermelho e azul em duzentos e cinquenta e cinco, verde zerado. Que cor dá?",
    # s22
    "Magenta, um roxo rosado. E nem tudo é máximo: vermelho duzentos e cinquenta e cinco com só quarenta de verde dá laranja.",
    # s23
    "Aqui está o sketch completo, rgb_colors. Três nomes de pino, um por cor, e uma chave, COMMON_ANODE, que fica false na maioria dos kits.",
    # s24
    "setColor() recebe três números. Com LED de anodo comum, ela inverte os valores, pois lá duzentos e cinquenta e cinco apaga.",
    # s25
    "No loop, leia cada linha como vermelho, verde, azul. Pause o vídeo e preveja a quarta: duas vezes duzentos e cinquenta e cinco, e zero. Que cor é?",
    # s26
    "Vermelho e verde no máximo: amarelo. Cada cor fica um segundo e, depois do laranja, a lista recomeça.",
    # s27
    "Rodando: vermelho, verde, azul, amarelo, magenta, ciano, branco, laranja.",
    # s27b
    "Repare que o amarelo puxa pro verde, e o magenta pro azul. As três cores não brilham igual. Tente baixar o verde e o azul para equilibrar.",
    # s28
    "Pergunta rápida: com as cores rodando, o que acontece se este fio preto soltar?",
    # s29
    "Veja. O LED apaga, todas as cores de uma vez. Recoloque o fio, e as cores voltam.",
    # s30
    "Lembre do episódio dois: a corrente precisa de um círculo completo, do pino de volta ao terra. A perna comum é a única volta para as três cores.",
    # s31
    "Então, se uma cor nunca acende, confira o fio dela. Se as três apagam juntas, confira primeiro o fio comum.",
    # s32
    "Agora o botão escolhe a cor, como trocar de canal no controle da TV. Guardamos um número chamado mode, e cada novo clique soma um.",
    # s33
    "Pergunta rápida: há quatro modos, zero a três. mode vale três e você aperta de novo. O que deve acontecer?",
    # s34
    "Deve voltar a zero, como o controle pula do último canal para o primeiro. O que acontece de fato: mode vira quatro por um instante, a linha seguinte vê que é maior que três e o zera.",
    # s35
    "A diferença do controle: não há tela mostrando o número. mode vive só na memória, então imprimir é o jeito mais fácil de conferir.",
    # s36
    "Aqui está o sketch completo, color_modes. Boa notícia: nada nele é realmente novo. É o botão do episódio quatro, setColor() e o fade do episódio cinco, juntos.",
    # s37
    "A parte dois do loop tem um if por modo. else if quer dizer: só confira este se tudo antes foi false. Zero é vermelho, um é verde e dois é azul.",
    # s38
    "O último else é o modo três, o fade lento. A cada oito milissegundos level anda. setColor() dá level ao vermelho e duzentos e cinquenta e cinco menos level ao azul.",
    # s39
    "Pause o vídeo e preveja: no meio do fade, level está em cerca de cento e vinte e oito. Que cor você vê?",
    # s40
    "Roxo, metade vermelho e metade azul. Um sobe, o outro desce, e juntos sempre somam duzentos e cinquenta e cinco.",
    # s41
    "Vamos rodar. Três cliques: vermelho, verde, azul, e o fade começa. Cada clique muda a cor na hora, mesmo no meio do fade.",
    # s42
    "Agora pause o vídeo e explique com suas palavras por que mode volta a zero depois do três. Uma frase basta.",
    # s43
    "Um jeito de dizer: só há quatro cores, então quando a contagem passa da última, o código recomeça o círculo.",
    # s44
    "Sua vez: uma lanterna de camping com um botão de quatro modos: apagada, branco fraco, branco forte e pisca vermelho.",
    # s45
    "O truque: se estiver acesa há três segundos ou mais, o próximo clique a desliga direto. Dica: lembre quando o modo mudou por último.",
    # s46
    "Hoje você aprendeu três coisas. Um LED RGB é três LEDs em um. setColor() os mistura com três números. E um contador de modo faz um botão escolher.",
    # s47
    "Na próxima, um botão de girar: vamos ler um potenciômetro e transformá-lo em brilho. Poste sua lanterna nos comentários; há uma solução na pasta da aula. Até lá!",
]

ES = [
    # s01
    "Un LED, el color que quieras. Rojo, verde, azul y, con un toque, un cambio lento de azul a rojo.",
    # s02
    "Al final de este video, mezclarás tus propios colores y un botón elegirá entre ellos.",
    # s03
    "Primero, dos preguntas del último episodio. Pregunta rápida: ¿qué hace analogWrite() con ciento veintiocho en un LED?",
    # s04
    "Enciende el pin cerca de la mitad de cada ciclo, muy rápido. Tu ojo ve brillo medio, pero el pin nunca está a medias.",
    # s05
    "Pregunta rápida: en el fade sin delay, ¿por qué el botón funciona en todo momento?",
    # s06
    "Porque el loop nunca espera. Mira el reloj, da un paso solo cuando toca y revisa el botón en cada vuelta.",
    # s07
    "Usa el circuito del episodio cinco, un LED RGB, tres resistencias más de doscientos veinte ohms y unos cables.",
    # s08
    "Mira muy de cerca la pantalla de tu celular y verás puntitos rojos, verdes y azules por todas partes. Cada color que ves sale de esos tres.",
    # s09
    "Un LED RGB es la misma idea. Lo que pasa en realidad: son tres LEDs pequeños en una pieza, rojo, verde y azul. Comparten una pata, la más larga.",
    # s10
    "La diferencia con la pintura: la luz se suma. Pintura roja y verde da café, pero luz roja y verde da amarillo, y las tres dan blanco.",
    # s11
    "Desconecta el USB y quita el LED verde de la protoboard de arriba. Necesitamos su pin, GPIO veinticinco.",
    # s12
    "Mete el LED RGB, con la pata larga en segundo lugar desde la izquierda. Un cable negro la lleva al riel negativo.",
    # s13
    "Cada color tiene su resistencia y su pin: rojo a D veinticinco, verde a D veintiséis y azul a D veintisiete.",
    # s14
    "Pregunta rápida: ¿por qué tres resistencias y no una en la pata común?",
    # s15
    "Porque cada color es un LED aparte, con su corriente. Una sola resistencia es como tres personas con un mismo popote: quien sorbe más fuerte se lleva más.",
    # s16
    "Lo que pasa en realidad: los colores se robarían corriente entre sí y tu mezcla cambiaría. La diferencia con el popote: aquí se lleva más el color que necesita menos voltaje, el rojo.",
    # s17
    "Algo que revisar: casi todos los kits traen LEDs de cátodo común, con la pata larga a tierra. Si el tuyo es al revés, el código tiene una línea para eso.",
    # s18
    "Para poner un color, escribimos una función de ayuda: setColor(). Es como un botón de cafetera. Un toque, y agrega la cantidad justa de tres ingredientes.",
    # s19
    "En realidad, llama tres veces a analogWrite(), una por cada pin de color, con números de cero a doscientos cincuenta y cinco.",
    # s20
    "La diferencia con la cafetera: no recuerda recetas. Le das las tres cantidades, cada vez.",
    # s21
    "Pregunta rápida: rojo y azul a doscientos cincuenta y cinco, verde a cero. ¿Qué color da?",
    # s22
    "Magenta, morado rosado. Y no todo es máximo: rojo doscientos cincuenta y cinco con solo cuarenta de verde da naranja.",
    # s23
    "Este es el sketch completo, rgb_colors. Tres nombres de pin, uno por color, y un interruptor, COMMON_ANODE, en false en casi todos los kits.",
    # s24
    "setColor() toma tres números. Si tu LED es de ánodo común, los invierte, porque ahí doscientos cincuenta y cinco apaga.",
    # s25
    "En el loop, cada línea es rojo, verde, azul. Pausa el video y predice la cuarta: dos veces doscientos cincuenta y cinco, y cero. ¿Qué color es?",
    # s26
    "Rojo y verde a tope: amarillo. Cada color dura un segundo y, tras el naranja, la lista vuelve a empezar.",
    # s27
    "A probarlo: rojo, verde, azul, amarillo, magenta, cian, blanco y naranja.",
    # s27b
    "Fíjate: el amarillo se ve algo verde, y el magenta algo azul. Los tres colores no brillan igual. Prueba bajar el verde y el azul para equilibrarlos.",
    # s28
    "Pregunta rápida: con los colores en marcha, ¿qué pasa si se suelta este cable negro?",
    # s29
    "Mira. El LED se apaga, todos los colores a la vez. Vuelve a meter el cable y regresan.",
    # s30
    "Recuerda el episodio dos: la corriente debe dar la vuelta completa, del pin a tierra. La pata común es el único camino de vuelta para los tres colores.",
    # s31
    "Así que si un color nunca enciende, revisa su propio cable. Si los tres se apagan juntos, revisa primero el cable común.",
    # s32
    "Ahora el botón elige el color, como cambiar de canal con el control. Guardamos un número, mode, y cada nueva pulsación suma uno.",
    # s33
    "Pregunta rápida: hay cuatro modos, de cero a tres. mode está en tres y presionas otra vez. ¿Qué debe pasar?",
    # s34
    "Debe volver a cero, como el control salta del último canal al primero. Lo que pasa en realidad: mode vale cuatro un momento, la siguiente línea ve que es mayor que tres, y lo pone en cero.",
    # s35
    "La diferencia con el control: no hay pantalla con el número. mode solo vive en memoria, y lo más fácil para revisarlo es imprimirlo.",
    # s36
    "Este es el sketch completo, color_modes. Buena noticia: nada aquí es realmente nuevo. Es el botón del episodio cuatro, setColor() y el fade del episodio cinco, juntos.",
    # s37
    "La parte dos del loop tiene un if por modo. else if significa: revisa este solo si todo lo anterior fue false. Cero es rojo, uno es verde y dos es azul.",
    # s38
    "El último else, modo tres, es el fade lento. Cada ocho milisegundos level avanza; setColor() da level al rojo y doscientos cincuenta y cinco menos level al azul.",
    # s39
    "Pausa el video y predice: a mitad del fade, level vale unos ciento veintiocho. ¿Qué color ves?",
    # s40
    "Morado: mitad rojo y mitad azul. El rojo sube, el azul baja, y juntos siempre suman doscientos cincuenta y cinco.",
    # s41
    "A probarlo. Tres pulsaciones: rojo, verde, azul, y empieza el fade. Cada pulsación cambia el color al instante, incluso a mitad del fade.",
    # s42
    "Ahora pausa el video y explica con tus palabras por qué mode vuelve a cero después del tres. Basta una frase.",
    # s43
    "Una forma de decirlo: solo hay cuatro colores, así que cuando la cuenta pasa del último, el código reinicia el círculo.",
    # s44
    "Arma tú una linterna para acampar. Un botón recorre cuatro modos: apagada, blanco tenue, blanco vivo y parpadeo rojo.",
    # s45
    "El truco: si lleva tres segundos o más encendida, la siguiente pulsación la apaga directo. Pista: guarda cuándo cambió el modo por última vez.",
    # s46
    "Hoy aprendiste tres cosas. Un LED RGB son tres LEDs en uno. setColor() los mezcla con tres números. Y un contador de modo deja que un botón elija.",
    # s47
    "La próxima vez, una perilla: leeremos un potenciómetro y lo convertiremos en brillo. Sube tu linterna a los comentarios; hay una solución en la carpeta. ¡Nos vemos!",
]

TARGET = {"hi": 1.05, "pt": 1.00, "es": 1.00}


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
        assert len(lines) == len(IDS) == 48, (lang, len(lines), len(IDS))
        seg = dict(zip(IDS, lines))
        langs[lang] = seg
        (out / f"{lang}.json").write_text(json.dumps({"voice": voice, "rate": "+0%", "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("dubs written:", ", ".join(langs))
    check(langs, english)
