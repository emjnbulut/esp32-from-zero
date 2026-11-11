"""Source of video/ep09/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, comes from make_script.py via dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
The same text is the subtitle for hi/pt/es (see make_subs.py: dub and subtitle must be the same sentences).
Usage: python video/ep09/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "देखिए ये पैदल पार पथ। गाड़ियों को हरी है। Button दबाता हूँ, बत्ती पीली, फिर लाल, और अब पैदल यात्री को हरी।",
    # s02
    "ये हमारा पहला mini project है। अंत तक आप ये पार पथ बनाएँगे, एक variable के साथ जो याद रखता है कि कौन सा कदम चल रहा है।",
    # s03
    "नए हैं? पहला episode स्क्रीन पर है। अब पिछले episodes से दो सवाल।",
    # s04
    "छोटा सवाल: पिछली बार वाली सीधी level line तीनों LED लगभग कभी क्यों नहीं जलाती थी?",
    # s05
    "क्योंकि map() नीचे गोल करता है। सबसे ऊँचा level पैमाने के आख़िरी निशान पर ही आता था।",
    # s06
    "छोटा सवाल: delay से program को रोके बिना, board कैसे जाने कि दो सेकंड बीत गए?",
    # s07
    "वो दीवार घड़ी, यानी millis() देखता है। याद रखे पल को अब से घटाता है, और देखता है कि फ़र्क दो हज़ार हुआ या नहीं।",
    # s08
    "योजना ये है। तीन LED गाड़ियों की बत्तियाँ हैं। रंगीन LED पैदल बत्ती: लाल रुकिए, हरी चलिए।",
    # s09
    "Button पैदल यात्री का अनुरोध button है। और knob तय करता है कि गाड़ियों की हरी कितनी देर रहे, तीन से दस सेकंड।",
    # s10
    "अच्छी ख़बर: एक भी नया तार नहीं चाहिए। सब कुछ पिछले episodes से board पर लगा है।",
    # s11
    "कोई पुर्ज़ा कम हो, तो pins स्क्रीन पर हैं, और पूरी wiring lesson folder में है।",
    # s12
    "पहला विचार delay() की ज़ंजीर है: हरी, रुको, पीली, रुको, लाल, रुको।",
    # s13
    "Video रोकिए, अंदाज़ा लगाइए: इस ज़ंजीर में, रुकने के दौरान button दबाने का क्या होगा?",
    # s14
    "वो खो जाता है। delay() में और कुछ नहीं चलता, तो button कोई नहीं देखता। रुके बिना इंतज़ार चाहिए।",
    # s15
    "कपड़े धोने की मशीन सोचिए। वो कदमों से गुज़रती है: धोना, खंगालना, सुखाना। हर पल उसे पता है कि वो किस कदम में है, और समय पूरा होते ही आगे बढ़ती है।",
    # s16
    "हमारे पार पथ में चार कदम हैं, शून्य से: गाड़ियों को हरी, पीली, पैदल यात्री पार करता है, और आख़िर में बत्ती टिमटिमाती है, जल्दी कीजिए।",
    # s17
    "असल में कदम बस एक पूर्ण संख्या है, state नाम के variable में। Loop का हर चक्कर वो संख्या देखता है, और सिर्फ़ उसी कदम का code चलाता है।",
    # s18
    "आगे बढ़ना एक assignment है: state में अगली संख्या रखिए, और समय लिख लीजिए। वही पल नए कदम की शुरुआत है।",
    # s19
    "मशीन से फ़र्क: मशीन सचमुच अपना कदम करती है। हमारा loop कदम के अंदर इंतज़ार नहीं करता; वो सेकंड में हज़ारों बार संख्या देखकर फ़ैसला लेता है।",
    # s20
    "ये रहा sketch, crossing। ऊपर pins, फिर state जो शून्य से शुरू होता है, और मौजूदा कदम शुरू होने का समय।",
    # s21
    "दो छोटे सहायक कदम छोटे रखते हैं। lights() पाँचों बत्तियाँ एक बार में तय करता है, जैसे colour LED वाले episode का coffee machine button।",
    # s22
    "दूसरा goTo() आगे बढ़ने के दो काम करता है: state में नई संख्या रखता है, और समय लिख लेता है।",
    # s23
    "Loop में पहला हिस्सा button है, episode चार जैसा। नया दबाव तभी गिना जाता है जब गाड़ियों को हरी हो, और board याद रखता है कि कोई इंतज़ार में है।",
    # s23b
    "Video रोकिए, अंदाज़ा लगाइए: पैदल यात्री पहले से पार कर रहा है और आप button दबाते हैं। क्या वो दबाव गिना जाएगा?",
    # s23c
    "नहीं। दबाव सिर्फ़ कदम शून्य में गिने जाते हैं, इसलिए पार पथ दोबारा शुरू नहीं होता।",
    # s24
    "दूसरा हिस्सा एक घटाव से शुरू होता है: अब, घटा कदम शुरू होने का पल। यही बताता है कि इस कदम में कितनी देर हुई।",
    # s25
    "फिर map() knob को हरी के समय में बदलता है, तीन से दस सेकंड। पिछले episode का function असली काम करता हुआ।",
    # s26
    "कदम शून्य: गाड़ियों को हरी, पैदल बत्ती लाल। कोई इंतज़ार में हो और हरी काफ़ी देर रह चुकी हो, तो कदम एक पर जाते हैं।",
    # s27
    "दो ampersand वही and हैं, पिछले episode की चुनौती वाला: दोनों जाँचें सही होनी चाहिए।",
    # s28
    "अब video रोकिए और ख़ुद कोशिश कीजिए: कदम एक लिखिए। गाड़ियों को दो सेकंड पीली, फिर कदम दो पर जाइए।",
    # s29
    "एक तरीका ये। पीली जलाइए, और दो सेकंड बीतते ही अनुरोध भूलकर कदम दो पर जाइए।",
    # s30
    "कदम दो: गाड़ियों को लाल, और पैदल यात्री को चार सेकंड हरी।",
    # s31
    "कदम तीन उसी घड़ी की तरकीब से पैदल बत्ती टिमटिमाता है, हर चौथाई सेकंड पलटकर। दो सेकंड बाद फिर कदम शून्य।",
    # s32
    "Video रोकिए, अंदाज़ा लगाइए: गाड़ियों को अभी हरी मिली है, और आप तुरंत button दबाते हैं। क्या पैदल यात्री को एकदम हरी मिलेगी?",
    # s33
    "नहीं। दबाव याद रहता है, पर knob का समय पूरा होने तक गाड़ियों की हरी चलती है। तभी पीली आती है।",
    # s34
    "ये रहा असली। पूरा चक्कर देखिए, और पैदल बत्ती को लाल से हरी होते देखिए।",
    # s35
    "पास से, आख़िरी दो सेकंड: पैदल बत्ती टिमटिमाकर कहती है जल्दी, और गाड़ियों को अब भी लाल है।",
    # s36
    "अब एक संख्या बदलिए। रुकिए और अंदाज़ा लगाइए: चार हज़ार की जगह आठ हज़ार हो, तो क्या बदलेगा?",
    # s37
    "पैदल यात्री को पार करने का दुगुना समय मिलता है। बाकी कुछ नहीं बदलता, हर कदम का अपना समय है।",
    # s38
    "Project में एक और तरकीब है: button कितनी देर दबा रहा, ये नापना। पार्किंग टिकट सोचिए।",
    # s39
    "अंदर जाते समय टिकट पर समय की मुहर लगती है। निकलते समय मशीन उस समय को अब से घटाती है, और आप फ़र्क का दाम देते हैं।",
    # s40
    "असल में दबाते ही हम अब को pressStart variable में रखते हैं। छोड़ते समय now घटा pressStart बताता है कि कितनी देर दबा रहा।",
    # s41
    "टिकट से फ़र्क: कागज़ नहीं है। pressStart याददाश्त में सिर्फ़ एक संख्या है, और अगला दबाव उसे मिटाकर लिखता है।",
    # s42
    "ये sketch है, press_time। Button दबे रहने तक पीली LED जलती है। छोड़ने पर Serial Monitor समय छापता है, और बताता है कि छोटा था या लंबा।",
    # s43
    "चौथाई सेकंड से कम छोटा गिना जाता है। रुकिए, अंदाज़ा लगाइए: आप button को जितना तेज़ हो सके थपथपाते हैं। क्या छपेगा?",
    # s44
    "करीब सौ मिलीसेकंड, और छोटा। एक सेकंड दबाए रखें, तो करीब हज़ार छपता है, और लंबा।",
    # s45
    "ऐसे एक button दो काम करता है। आपका फ़ोन भी: थपथपाइए तो जागता है, देर तक दबाइए तो बंद होता है।",
    # s46
    "अब एक ग़लती जो हो सकती है। कोई आगे बढ़ने के लिए बस state बराबर एक लिख देता है, और समय लिखना भूल जाता है।",
    # s47
    "छोटा सवाल: तब पार पथ क्या करेगा?",
    # s48
    "पीली पल भर चमककर बुझ जाती है। कदम का शुरुआती समय पुराना ही है, इसलिए घटाव कहता है कि दो सेकंड कब के बीत चुके।",
    # s49
    "इसीलिए goTo() हमेशा दोनों काम साथ करता है। हर कदम बदलने पर उसी को इस्तेमाल कीजिए।",
    # s50
    "Video रोकिए, और अपने शब्दों में बताइए कि हर कदम को अपना शुरुआती समय क्यों चाहिए। एक वाक्य काफ़ी है।",
    # s51
    "एक तरीका: हर कदम अपना समय अपनी शुरुआत से नापता है। तो नए कदम को नया समय चाहिए, वरना वो सोचता है कि समय पहले ही पूरा हो चुका।",
    # s52
    "आपकी बारी: धीमा राहगीर मोड। Request button एक सेकंड से ज़्यादा दबा रहे, तो पैदल बत्ती दुगुनी देर हरी रहे।",
    # s53
    "दोनों टुकड़े आप जानते हैं: पार्किंग टिकट, और अपना समय रखने वाला कदम। एक हल lesson folder में है।",
    # s54
    "आज आपने तीन चीज़ें बनाईं। कदम याद रखने वाला state variable। हर कदम का अपना शुरुआती समय, ताकि कुछ रुकना न पड़े। और button दबाव के लिए पार्किंग टिकट।",
    # s55
    "अगली बार, इसी circuit पर: reflex game, ऐसे high score के साथ जो board निकालने पर भी बचा रहे। Comments में बताइए आपके पार पथ की हरी कितनी देर चलती है। फिर मिलते हैं!",
]

PT = [
    # s01
    "Veja esta faixa. Os carros têm verde. Aperto o botão, a luz fica amarela, depois vermelha, e o pedestre ganha verde.",
    # s02
    "Este é nosso primeiro mini projeto. No fim, você monta esta faixa, com uma variável que lembra em que passo estamos.",
    # s03
    "Novo aqui? O episódio um está na tela. Agora, duas perguntas dos anteriores.",
    # s04
    "Pergunta rápida: a linha de nível óbvia quase nunca acendia os três LEDs. Por quê?",
    # s05
    "Porque o map() arredonda para baixo. O nível mais alto só vinha na última marca.",
    # s06
    "Pergunta rápida: como a placa sabe que passaram dois segundos, sem travar o programa com delay?",
    # s07
    "Ela olha o relógio de parede, o millis(). Subtrai o instante guardado do agora e vê se a diferença chegou a dois mil.",
    # s08
    "O plano: três LEDs são as luzes dos carros. O LED colorido é a luz do pedestre: vermelho espera, verde anda.",
    # s09
    "O botão é o pedido do pedestre. E o knob define quanto tempo o verde dos carros dura, de três a dez segundos.",
    # s10
    "Boa notícia: não precisa de nenhum fio novo. Tudo já está na placa, dos episódios passados.",
    # s11
    "Falta uma peça? Os pinos estão na tela, e a ligação completa está na pasta da lição.",
    # s12
    "Primeira ideia: delays em cadeia: verde, espera, amarelo, espera, vermelho, espera.",
    # s13
    "Pause o vídeo e preveja: com essa corrente, o que acontece com um aperto de botão durante a espera?",
    # s14
    "Se perde. Num delay(), nada mais roda, e ninguém olha o botão. Precisamos esperar sem parar.",
    # s15
    "Pense numa máquina de lavar. Ela passa por etapas: lavar, enxaguar, centrifugar. Sempre sabe em que etapa está, e segue quando o tempo da etapa acaba.",
    # s16
    "Nossa faixa tem quatro passos, de zero: carros no verde, carros no amarelo, o pedestre atravessa, e por fim a luz pisca, depressa.",
    # s17
    "Na real, o passo é só um número inteiro numa variável chamada state. A cada volta do loop, vemos esse número e rodamos só o código daquele passo.",
    # s18
    "Avançar é uma atribuição: ponha o próximo número em state e anote a hora. Esse instante é o começo do novo passo.",
    # s19
    "A diferença da máquina: ela realmente faz sua etapa. Nosso loop não espera dentro de um passo; olha o número milhares de vezes por segundo e decide.",
    # s20
    "Este é o sketch crossing. No topo, os pinos, depois state, que começa em zero, e a hora em que o passo atual começou.",
    # s21
    "Dois ajudantes encurtam os passos. lights() acerta as cinco luzes numa chamada, como o botão da cafeteira do episódio do LED colorido.",
    # s22
    "O outro, goTo(), faz os dois trabalhos de avançar: põe o novo número em state e anota a hora.",
    # s23
    "No loop, a parte um é o botão, como no episódio quatro. Um aperto novo só conta com verde para os carros, e a placa lembra que alguém espera.",
    # s23b
    "Pause e preveja: você aperta o botão com o pedestre já atravessando. Esse aperto conta?",
    # s23c
    "Não. Só contam no passo zero, então a faixa nunca recomeça por acidente.",
    # s24
    "A parte dois começa com uma subtração: agora menos a hora em que o passo começou. É há quanto tempo estamos nele.",
    # s25
    "Depois, o map() vira o knob no tempo do verde, de três a dez segundos. A função passada, num trabalho de verdade.",
    # s26
    "Passo zero: carros no verde, pedestre no vermelho. Se alguém espera e o verde durou bastante, vamos ao passo um.",
    # s27
    "Os dois e comerciais são o and do desafio passado: as duas condições devem valer.",
    # s28
    "Agora pause e tente: escreva o passo um. Os carros ficam dois segundos no amarelo, depois vamos ao passo dois.",
    # s29
    "Um jeito: amarelo ligado e, passados dois segundos, esquecemos o pedido e vamos ao passo dois.",
    # s30
    "Passo dois: carros no vermelho e pedestre no verde por quatro segundos.",
    # s31
    "O passo três pisca a luz com o mesmo truque do relógio, a cada quarto de segundo. Após dois segundos, voltamos ao passo zero.",
    # s32
    "Pause e preveja: os carros acabaram de ficar verdes e você aperta já. O pedestre ganha verde na hora?",
    # s33
    "Não. O pedido fica guardado, mas os carros mantêm o verde até o tempo do knob acabar. Só então vem o amarelo.",
    # s34
    "Aqui de verdade. Veja a rodada toda e note a luz do pedestre passando de vermelho a verde.",
    # s35
    "De perto, os dois últimos segundos: a luz pisca, pressa, e os carros seguem no vermelho.",
    # s36
    "Agora mude um número. Pause e preveja: se quatro mil virar oito mil, o que muda?",
    # s37
    "O pedestre ganha o dobro de tempo para atravessar. Nada mais muda: cada passo guarda seu tempo.",
    # s38
    "O projeto tem mais um truque: medir quanto o botão ficou apertado. Pense num ticket.",
    # s39
    "Ao entrar, o ticket recebe a hora carimbada. Ao sair, a máquina subtrai essa hora do agora, e você paga a diferença.",
    # s40
    "Na real, ao apertar guardamos o agora numa variável, pressStart. Ao soltar, now menos pressStart é o tempo apertado.",
    # s41
    "A diferença do ticket: não há papel. pressStart é só um número na memória, e o próximo aperto escreve por cima.",
    # s42
    "Este é o sketch press_time. O LED amarelo acende enquanto você segura. Ao soltar, o Serial Monitor imprime o tempo e se foi curto ou longo.",
    # s43
    "Menos de um quarto de segundo é curto. Pause e preveja: você toca o botão o mais rápido possível. O que imprime?",
    # s44
    "Uns cem milissegundos, e curto. Segure por um segundo e imprime uns mil, e longo.",
    # s45
    "Assim um botão faz dois trabalhos. Seu celular também: um toque acorda, um aperto longo desliga.",
    # s46
    "Agora um erro possível. Alguém avança escrevendo só state igual a um, e esquece de anotar a hora.",
    # s47
    "Pergunta rápida: o que a faixa faz então?",
    # s48
    "O amarelo pisca por um instante e some. A hora de início do passo é a antiga, e a subtração diz que dois segundos já passaram faz tempo.",
    # s49
    "Uma dica: uma variável chamada step lembra quantos já estão certos.",
    # s50
    "Pause o vídeo e explique com suas palavras por que cada passo precisa da sua hora de início. Uma frase basta.",
    # s51
    "Um jeito: cada passo mede o tempo desde que começou. Passo novo precisa de início novo, ou acha que seu tempo já acabou.",
    # s52
    "Sua vez: modo pedestre lento. Se o botão ficar apertado mais de um segundo, a luz do pedestre fica verde o dobro.",
    # s53
    "Você já sabe as duas peças: o ticket de estacionamento e um passo com tempo próprio. Uma solução está na pasta da lição.",
    # s54
    "Hoje você fez três coisas. Uma variável state que lembra o passo. Uma hora de início por passo, sem esperar. E um ticket para os apertos do botão.",
    # s55
    "Na próxima, no mesmo circuito: um jogo de reflexo, com recorde que sobrevive até se você desligar a placa. Diga nos comentários quanto dura o verde da sua faixa. Até lá!",
]

ES = [
    # s01
    "Mira este cruce. Los autos tienen verde. Pulso el botón, la luz pasa a amarillo, luego rojo, y el peatón tiene verde.",
    # s02
    "Este es nuestro primer mini proyecto. Al final armarás este cruce, con una variable que recuerda en qué paso vamos.",
    # s03
    "¿Eres nuevo? El episodio uno está en pantalla. Ahora, dos preguntas.",
    # s04
    "Pregunta rápida: la línea de nivel obvia casi nunca encendía los tres LEDs. ¿Por qué?",
    # s05
    "Porque map() redondea hacia abajo. El nivel más alto solo llegaba al final.",
    # s06
    "Pregunta rápida: ¿cómo sabe la placa que pasaron dos segundos, sin congelar el programa con delay?",
    # s07
    "Mira el reloj de pared, millis(). Resta el momento guardado al ahora y ve si la diferencia llegó a dos mil.",
    # s08
    "El plan: tres LEDs son las luces de los autos. El LED de color es la luz peatonal: rojo espera, verde cruza.",
    # s09
    "El botón es el pedido del peatón. Y la perilla fija cuánto dura el verde de los autos, de tres a diez segundos.",
    # s10
    "Buena noticia: no necesitas ningún cable nuevo. Todo ya está en la placa, de los episodios anteriores.",
    # s11
    "¿Falta una pieza? Los pines están en pantalla; el cableado, en la carpeta.",
    # s12
    "Primera idea: delays en cadena: verde, espera, amarillo, espera, rojo, espera.",
    # s13
    "Pausa el video y predice: con esa cadena, ¿qué pasa con un pulso del botón mientras el programa espera?",
    # s14
    "Se pierde. En un delay() nada más corre, y nadie mira el botón. Hay que esperar sin detenerse.",
    # s15
    "Piensa en una lavadora. Pasa por pasos: lavar, enjuagar, centrifugar. Siempre sabe en qué paso está, y sigue cuando el tiempo se acaba.",
    # s16
    "Nuestro cruce tiene cuatro pasos, desde cero: autos en verde, autos en amarillo, el peatón cruza, y al final la luz parpadea, apúrate.",
    # s17
    "Realmente, el paso es solo un número entero en una variable llamada state. En cada vuelta del loop vemos ese número y corremos solo el código de ese paso.",
    # s18
    "Avanzar es una asignación: pon el siguiente número en state y anota la hora. Ese momento es el inicio del nuevo paso.",
    # s19
    "La diferencia con la lavadora: ella sí hace su paso. Nuestro loop no espera dentro de un paso; mira el número miles de veces por segundo y decide.",
    # s20
    "Este es el sketch crossing. Arriba, los pines, luego state, que empieza en cero, y la hora en que empezó el paso actual.",
    # s21
    "Dos ayudantes acortan los pasos. lights() fija las cinco luces en una llamada, como el botón de la cafetera del episodio del LED de color.",
    # s22
    "El otro, goTo(), hace los dos trabajos de avanzar: pone el número nuevo en state y anota la hora.",
    # s23
    "En el loop, la parte uno es el botón, como en el episodio cuatro. Un pulso nuevo solo cuenta con verde para los autos, y la placa recuerda que alguien espera.",
    # s23b
    "Pausa y predice: pulsas el botón con el peatón ya cruzando. ¿Cuenta ese pulso?",
    # s23c
    "No. Solo cuentan en el paso cero, así el cruce nunca reinicia por accidente.",
    # s24
    "La parte dos empieza con una resta: ahora menos el momento en que empezó el paso. Es cuánto llevamos en él.",
    # s25
    "Luego, map() vuelve la perilla el tiempo del verde, de tres a diez segundos. La función pasada, en un trabajo real.",
    # s26
    "Paso cero: autos en verde, peatón en rojo. Si alguien espera y el verde duró suficiente, pasamos al paso uno.",
    # s27
    "Los dos ampersands son el and del reto pasado: ambas condiciones deben cumplirse.",
    # s28
    "Ahora pausa e inténtalo: escribe el paso uno. Los autos van dos segundos en amarillo, luego pasamos al paso dos.",
    # s29
    "Una forma: amarillo encendido y, pasados dos segundos, olvidamos el pedido y vamos al paso dos.",
    # s30
    "Paso dos: autos en rojo y peatón en verde por cuatro segundos.",
    # s31
    "El paso tres parpadea la luz con el mismo truco del reloj, cada cuarto de segundo. Tras dos segundos, volvemos al paso cero.",
    # s32
    "Pausa y predice: los autos acaban de ponerse en verde y pulsas ya. ¿El peatón recibe verde al instante?",
    # s33
    "No. El pulso queda guardado, pero los autos mantienen el verde hasta que acabe el tiempo de la perilla.",
    # s34
    "Aquí de verdad. Mira la ronda completa y fíjate en la luz peatonal pasando de rojo a verde.",
    # s35
    "De cerca, los dos últimos segundos: la luz parpadea, apúrate, y los autos siguen en rojo.",
    # s36
    "Ahora cambia un número. Pausa y predice: si cuatro mil pasa a ocho mil, ¿qué cambia?",
    # s37
    "El peatón tiene el doble de tiempo. Nada más cambia: cada paso guarda su propio tiempo.",
    # s38
    "El proyecto tiene un truco más: medir cuánto se mantuvo el botón. Piensa en un ticket.",
    # s39
    "Al entrar, al ticket le estampan la hora. Al salir, la máquina resta esa hora al ahora, y pagas la diferencia.",
    # s40
    "Realmente, al pulsar guardamos el ahora en una variable, pressStart. Al soltar, now menos pressStart es el tiempo pulsado.",
    # s41
    "La diferencia con el ticket: no hay papel. pressStart es solo un número en memoria, y el próximo pulso lo sobrescribe.",
    # s42
    "Este es el sketch press_time. El LED amarillo está encendido mientras mantienes el botón. Al soltar, el Serial Monitor imprime el tiempo y si fue corto o largo.",
    # s43
    "Menos de un cuarto de segundo es corto. Pausa y predice: tocas el botón lo más rápido posible. ¿Qué imprime?",
    # s44
    "Unos cien milisegundos, y corto. Mantenlo un segundo e imprime unos mil, y largo.",
    # s45
    "Así un botón hace dos trabajos. Tu celular también: un toque lo despierta, una pulsación larga lo apaga.",
    # s46
    "Ahora un error posible. Alguien avanza escribiendo solo state igual a uno, y olvida anotar la hora.",
    # s47
    "Pregunta rápida: ¿qué hace entonces el cruce?",
    # s48
    "El amarillo parpadea un instante y desaparece. La hora de inicio del paso es la vieja, y la resta dice que dos segundos pasaron hace rato.",
    # s49
    "Una pista: una variable llamada step recuerda cuántos números van bien.",
    # s50
    "Pausa el video y explica con tus palabras por qué cada paso necesita su hora de inicio. Una frase basta.",
    # s51
    "Una forma: cada paso mide su tiempo desde que empezó. Un paso nuevo necesita un inicio nuevo, o cree que su tiempo ya se acabó.",
    # s52
    "Tu turno: modo peatón lento. Si mantienes el botón más de un segundo, la luz peatonal queda en verde el doble.",
    # s53
    "Ya conoces las dos piezas: el ticket de estacionamiento y un paso con su propio tiempo. Hay una solución en la carpeta.",
    # s54
    "Hoy hiciste tres cosas. Una variable state que recuerda el paso. Una hora de inicio por paso, sin esperar. Y un ticket para los pulsos del botón.",
    # s55
    "La próxima, con el mismo circuito: un juego de reflejos, con un récord que sobrevive aunque desconectes la placa. Cuéntame en los comentarios cuánto dura el verde de tu cruce. ¡Nos vemos!",
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
        assert len(lines) == len(IDS), (lang, len(lines), len(IDS))
        seg = dict(zip(IDS, lines))
        langs[lang] = seg
        (out / f"{lang}.json").write_text(json.dumps({"voice": voice, "rate": "+0%", "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("dubs written:", ", ".join(langs))
    check(langs, english)
