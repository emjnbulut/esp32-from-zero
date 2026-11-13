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
    "ये पहला mini project है। आप ये पार पथ बनाएँगे, एक variable से जो कदम याद रखता है।",
    # s03
    "नए हैं? पहला episode स्क्रीन पर है। अब दो पुराने सवाल।",
    # s04
    "छोटा सवाल: पिछली बार वाली सीधी level line तीनों LED लगभग कभी क्यों नहीं जलाती थी?",
    # s05
    "क्योंकि map() नीचे गोल करता है। ऊँचा level आख़िरी निशान पर आता था।",
    # s06
    "छोटा सवाल: delay के बिना board कैसे जाने कि दो सेकंड बीत गए?",
    # s07
    "वो दीवार घड़ी millis() देखता है, याद पल घटाता है: फ़र्क दो हज़ार?",
    # s08
    "योजना ये है। तीन LED गाड़ियों की बत्तियाँ हैं। रंगीन LED पैदल बत्ती: लाल रुकिए, हरी चलिए।",
    # s09
    "पैदल यात्री का अनुरोध button है। knob तय करता है गाड़ियों की हरी तीन से दस सेकंड रहे।",
    # s10
    "अच्छी ख़बर: एक भी नया तार नहीं चाहिए। सब कुछ पिछले episodes से board पर लगा है।",
    # s11
    "कोई पुर्ज़ा कम हो, तो pins स्क्रीन पर हैं, और पूरी wiring lesson folder में है।",
    # s12
    "पहले delay(): हरी, रुको, पीली, रुको, लाल, रुको।",
    # s13
    "रोकिए, अंदाज़ा लगाइए: रुकने में button दबाने का क्या हो?",
    # s14
    "वो खो जाता है। delay() में button कोई नहीं देखता। रुके बिना इंतज़ार चाहिए।",
    # s15
    "कपड़े धोने की मशीन सोचिए। वो कदमों से गुज़रती है: धोना, खंगालना, सुखाना। हर पल उसे पता है कि वो किस कदम में है, और समय पूरा होते ही आगे बढ़ती है।",
    # s16
    "चार कदम हैं, शून्य से: गाड़ियों को हरी, पीली, पैदल यात्री पार करता है, फिर बत्ती टिमटिमाती है।",
    # s17
    "असल में कदम बस एक पूर्ण संख्या है, state नाम के variable में। Loop का हर चक्कर वो संख्या देखता है, और सिर्फ़ उसी कदम का code चलाता है।",
    # s18
    "आगे बढ़ना एक assignment है: state में अगली संख्या रखिए, और समय लिख लीजिए। वही पल नए कदम की शुरुआत है।",
    # s19
    "मशीन से फ़र्क: मशीन सचमुच कदम करती है। हमारा loop कदम में इंतज़ार नहीं करता; सेकंड में हज़ारों बार संख्या देखकर फ़ैसला लेता है।",
    # s20
    "ये sketch: ऊपर pins, फिर state शून्य से, और कदम का समय।",
    # s21
    "दो सहायक। lights() पाँचों बत्तियाँ एक बार में तय करता है, जैसे coffee machine button।",
    # s22
    "दूसरा goTo(): state में संख्या रखता है, और समय लिखता है।",
    # s23
    "Loop में पहला हिस्सा button है, episode चार जैसा। नया दबाव तभी गिना जाता है जब गाड़ियों को हरी हो, और board याद रखता है कि कोई इंतज़ार में है।",
    # s23b
    "अंदाज़ा लगाइए: पैदल यात्री पार कर रहा, आपने button दबाया। गिना गया?",
    # s23c
    "नहीं। दबाव सिर्फ़ कदम शून्य में गिने जाते हैं, इसलिए पार पथ दोबारा शुरू नहीं होता।",
    # s24
    "दूसरा हिस्सा घटाव है: अब, घटा कदम शुरू होने का पल। यही बताता है कि कदम में कितनी देर हुई।",
    # s25
    "फिर map() knob को हरी के समय में बदलता है, तीन से दस सेकंड।",
    # s26
    "कदम शून्य: गाड़ियों को हरी। इंतज़ार हो और हरी रह चुकी, तो कदम एक।",
    # s27
    "दो ampersand यानी and: दोनों जाँचें सही हों।",
    # s28
    "अब video रोकिए और ख़ुद कोशिश कीजिए: कदम एक लिखिए। गाड़ियों को दो सेकंड पीली, फिर कदम दो पर जाइए।",
    # s29
    "एक तरीका: पीली जलाइए, दो सेकंड बाद अनुरोध भूलकर कदम दो पर जाइए।",
    # s30
    "कदम दो: गाड़ियों को लाल, पैदल को चार सेकंड हरी।",
    # s31
    "कदम तीन उसी घड़ी की तरकीब से पैदल बत्ती टिमटिमाता है, हर चौथाई सेकंड पलटकर। दो सेकंड बाद फिर कदम शून्य।",
    # s32
    "अंदाज़ा लगाइए: गाड़ियों को अभी हरी मिली, आप तुरंत button दबाते हैं। पैदल को हरी मिलेगी?",
    # s33
    "नहीं। दबाव याद रहता है, पर knob का समय पूरा होने तक गाड़ियों की हरी चलती है। तभी पीली आती है।",
    # s34
    "ये रहा असली। पूरा चक्कर देखिए, पैदल बत्ती हरी।",
    # s35
    "आख़िरी दो सेकंड: पैदल बत्ती टिमटिमाती है, गाड़ियों को लाल।",
    # s36
    "एक संख्या बदलिए। अंदाज़ा लगाइए: चार हज़ार की जगह आठ हज़ार, तो क्या बदले?",
    # s37
    "पैदल यात्री को पार करने का दुगुना समय मिलता है। बाकी कुछ नहीं बदलता, हर कदम का अपना समय है।",
    # s38
    "एक तरकीब: button कितनी देर दबा?",
    # s39
    "अंदर जाते समय टिकट पर समय की मुहर लगती है। निकलते समय मशीन उस समय को अब से घटाती है, और आप फ़र्क का दाम देते हैं।",
    # s40
    "असल में दबाते ही हम अब को pressStart variable में रखते हैं। छोड़ते समय now घटा pressStart बताता है कि कितनी देर दबा रहा।",
    # s41
    "टिकट से फ़र्क: कागज़ नहीं। pressStart बस एक संख्या है, अगला दबाव उसे मिटा देता है।",
    # s42
    "press_time: दबे रहने तक पीली LED जलती है। छोड़ने पर Serial Monitor समय छापता, छोटा या लंबा।",
    # s43
    "चौथाई सेकंड से कम छोटा गिना जाता है। अंदाज़ा लगाइए: button को तेज़ थपथपाएँ, तो क्या छपेगा?",
    # s44
    "करीब सौ मिलीसेकंड, और छोटा। एक सेकंड दबाएँ, तो करीब हज़ार, और लंबा।",
    # s45
    "ऐसे button दो काम करता है। फ़ोन: थपथपाओ जागे, दबाओ बंद।",
    # s46
    "अब एक ग़लती जो हो सकती है। कोई आगे बढ़ने के लिए बस state बराबर एक लिख देता है, और समय लिखना भूल जाता है।",
    # s47
    "छोटा सवाल: तब पार पथ क्या करेगा?",
    # s48
    "पीली पल भर चमकी, बुझी। समय पुराना, तो घटाव: दो सेकंड बीते।",
    # s49
    "इसीलिए goTo() दोनों काम साथ करता है। कदम बदलते समय उसी को लीजिए।",
    # s50
    "Video रोकिए, और अपने शब्दों में बताइए कि हर कदम को अपना शुरुआती समय क्यों चाहिए। एक वाक्य काफ़ी है।",
    # s51
    "हर कदम अपना समय अपनी शुरुआत से नापता है। नए कदम को नया समय चाहिए, वरना समय पूरा समझता है।",
    # s52
    "आपकी बारी: धीमा राहगीर मोड। Request button एक सेकंड से ज़्यादा दबा रहे, तो पैदल बत्ती दुगुनी देर हरी रहे।",
    # s53
    "दोनों टुकड़े आप जानते हैं: पार्किंग टिकट, और अपना समय रखने वाला कदम। एक हल lesson folder में है।",
    # s54
    "आज आपने तीन चीज़ें बनाईं। कदम याद रखने वाला state variable। हर कदम का अपना शुरुआती समय, ताकि कुछ रुकना न पड़े। और button दबाव के लिए पार्किंग टिकट।",
    # s55
    "अगली बार, इसी circuit पर: reflex game, high score के साथ जो board निकालने पर भी बचे। Comments में बताइए पार पथ की हरी कितनी चलती है। फिर मिलिए!",
]

PT = [
    # s01
    "Veja esta faixa. Os carros têm verde. Aperto o botão, a luz fica amarela, depois vermelha, e o pedestre ganha verde.",
    # s02
    "Este é nosso primeiro mini projeto. No fim, você monta esta faixa, com uma variável que lembra em que passo estamos.",
    # s03
    "Novo aqui? O episódio um está na tela. Duas perguntas antes.",
    # s04
    "Pergunta rápida: a linha de nível óbvia quase nunca acendia os três LEDs. Por quê?",
    # s05
    "O map() arredonda para baixo. O nível máximo só vinha na última marca.",
    # s06
    "Pergunta rápida: como a placa sabe que passaram dois segundos sem delay?",
    # s07
    "Ela olha o relógio de parede, o millis(). Subtrai o instante guardado do agora e vê se deu dois mil.",
    # s08
    "O plano: três LEDs são as luzes dos carros. O LED colorido é a luz do pedestre: vermelho espera, verde anda.",
    # s09
    "O botão é o pedido do pedestre. O knob define o verde dos carros: de três a dez segundos.",
    # s10
    "Boa notícia: nenhum fio novo. Tudo já está na placa.",
    # s11
    "Falta uma peça? Os pinos estão na tela, e a ligação na pasta da lição.",
    # s12
    "Cadeia de delays: verde, espera, amarelo, espera, vermelho.",
    # s13
    "Pare e preveja: nessa corrente, o que acontece com um aperto na espera?",
    # s14
    "Se perde. Num delay(), nada mais roda, e ninguém olha o botão. Precisamos esperar sem parar.",
    # s15
    "Pense numa máquina de lavar. Ela passa por etapas: lavar, enxaguar, centrifugar. Sempre sabe em que etapa está, e segue quando o tempo da etapa acaba.",
    # s16
    "Nossa faixa tem quatro passos, de zero: carros no verde, carros no amarelo, o pedestre atravessa, e por fim a luz pisca, depressa.",
    # s17
    "Na real, o passo é só um número inteiro numa variável chamada state. A cada volta do loop, vemos esse número e rodamos só o código daquele passo.",
    # s18
    "Avançar é atribuição: ponha o próximo número em state e anote a hora. É o começo do novo passo.",
    # s19
    "A diferença da máquina: ela faz sua etapa. Nosso loop não espera num passo; olha o número milhares de vezes por segundo e decide.",
    # s20
    "Este é o sketch crossing. No topo, os pinos, depois state, que começa em zero, e a hora do passo.",
    # s21
    "Dois ajudantes encurtam os passos. lights() acerta as cinco luzes de uma vez, como o botão da cafeteira do episódio do LED.",
    # s22
    "O outro, goTo(), faz os dois trabalhos de avançar: põe o novo número em state e anota a hora.",
    # s23
    "No loop, a parte um é o botão. Um aperto novo só conta com verde nos carros, e a placa lembra quem espera.",
    # s23b
    "Pare e preveja: você aperta o botão com o pedestre atravessando. Conta?",
    # s23c
    "Não. Só contam no passo zero, então a faixa nunca recomeça por acidente.",
    # s24
    "A parte dois começa com uma subtração: agora menos a hora de início do passo. É o tempo no passo.",
    # s25
    "Depois, o map() vira o knob no tempo do verde, de três a dez segundos.",
    # s26
    "Passo zero: carros no verde, pedestre vermelho. Com espera e verde longo, passo um.",
    # s27
    "Os dois e comerciais são o and do desafio: as duas condições valem.",
    # s28
    "Agora pause e tente: escreva o passo um. Os carros ficam dois segundos no amarelo, depois vamos ao passo dois.",
    # s29
    "Um jeito: amarelo ligado e, passados dois segundos, esquecemos o pedido e vamos ao passo dois.",
    # s30
    "Passo dois: carros no vermelho e pedestre no verde por quatro segundos.",
    # s31
    "O passo três pisca a luz com o truque do relógio, a cada quarto de segundo. Após dois, passo zero.",
    # s32
    "Pause e preveja: os carros acabaram de ficar verdes e você aperta já. O pedestre ganha verde na hora?",
    # s33
    "Não. O pedido fica guardado, mas os carros mantêm o verde até o fim do tempo do knob.",
    # s34
    "Aqui de verdade. Veja a rodada toda: a luz do pedestre vai de vermelho a verde.",
    # s35
    "Últimos dois segundos: a luz pisca, pressa, e os carros no vermelho.",
    # s36
    "Mude um número: de quatro mil para oito mil, o que muda?",
    # s37
    "O pedestre ganha o dobro de tempo para atravessar. Nada mais muda: cada passo guarda seu tempo.",
    # s38
    "O projeto tem mais um truque: medir quanto o botão ficou apertado. Pense num ticket.",
    # s39
    "Ao entrar, o ticket recebe a hora carimbada. Ao sair, a máquina subtrai essa hora do agora, e você paga a diferença.",
    # s40
    "Na real, ao apertar guardamos o agora numa variável, pressStart. Ao soltar, now menos pressStart é o tempo apertado.",
    # s41
    "Sem papel. pressStart é só um número na memória; o próximo aperto sobrescreve.",
    # s42
    "press_time: amarelo aceso ao segurar. Soltou, o Serial Monitor mostra o tempo, curto ou longo.",
    # s43
    "Menos de um quarto de segundo é curto. Pause e preveja: toca o botão bem rápido. O que imprime?",
    # s44
    "Uns cem milissegundos, e curto. Segure por um segundo e imprime uns mil, e longo.",
    # s45
    "Um botão faz dois trabalhos. Seu celular também: toque acorda, aperto longo desliga.",
    # s46
    "Erro possível: alguém escreve só state igual a um, sem anotar a hora.",
    # s47
    "Então, o que a faixa faz?",
    # s48
    "O amarelo pisca por um instante e some. O início do passo é o antigo, e a subtração diz que dois segundos já passaram.",
    # s49
    "Por isso goTo() faz as duas coisas. Use sempre.",
    # s50
    "Pause o vídeo e explique com suas palavras por que cada passo precisa da sua hora de início. Uma frase basta.",
    # s51
    "Um jeito: cada passo mede o tempo desde que começou. Passo novo precisa de início novo, ou acha que seu tempo já acabou.",
    # s52
    "Sua vez: modo pedestre lento. Botão apertado mais de um segundo, verde do pedestre dobra.",
    # s53
    "Você já sabe as duas peças: o ticket e um passo com tempo próprio. A solução está na pasta.",
    # s54
    "Hoje você fez três coisas. Uma variável state que lembra o passo. Uma hora de início por passo, sem esperar. E um ticket para os apertos do botão.",
    # s55
    "Na próxima: jogo de reflexo com recorde que sobrevive sem energia. Diga nos comentários quanto dura o verde da sua faixa.",
]

ES = [
    # s01
    "Mira el cruce. Autos en verde. Pulso: amarillo, rojo, verde al peatón.",
    # s02
    "Este es nuestro primer mini proyecto. Al final armarás este cruce, con una variable que recuerda en qué paso vamos.",
    # s03
    "¿Nuevo? El episodio uno está en pantalla. Dos preguntas.",
    # s04
    "Pregunta rápida: la línea de nivel obvia casi nunca encendía los tres LEDs. ¿Por qué?",
    # s05
    "Porque map() redondea hacia abajo. El nivel más alto solo llegaba al final.",
    # s06
    "Pregunta rápida: ¿cómo sabe la placa que pasaron dos segundos, sin delay?",
    # s07
    "Mira el reloj de pared, millis(). Resta el momento guardado al ahora y ve si la diferencia llegó a dos mil.",
    # s08
    "El plan: tres LEDs son las luces de los autos. El LED de color es la luz peatonal: rojo espera, verde cruza.",
    # s09
    "El botón es la petición del peatón. La perilla fija el verde de autos: tres a diez segundos.",
    # s10
    "Buena noticia: ningún cable nuevo. Ya está todo.",
    # s11
    "¿Falta algo? Pines en pantalla; cableado, en la carpeta.",
    # s12
    "Primera idea, delays en cadena: verde, espera, amarillo, espera, rojo.",
    # s13
    "Pausa el video y predice: con esa cadena, ¿qué pasa con un pulso en la espera?",
    # s14
    "Se pierde. En delay() nada corre, nadie mira el botón. Esperemos sin parar.",
    # s15
    "Piensa en una lavadora: lavar, enjuagar, centrifugar. Sabe en qué paso está, y sigue al acabar.",
    # s16
    "Nuestro cruce tiene cuatro pasos, desde cero: autos en verde, en amarillo, el peatón cruza, y la luz parpadea, apúrate.",
    # s17
    "El paso es solo un número entero en una variable llamada state. En cada vuelta del loop vemos ese número y corremos solo ese paso.",
    # s18
    "Avanzar es asignar: pon el siguiente número en state y anota la hora. Es el inicio del nuevo paso.",
    # s19
    "La lavadora sí hace su paso. Nuestro loop no espera dentro de un paso; mira el número miles de veces por segundo y decide.",
    # s20
    "Este es el sketch crossing. Arriba, los pines, luego state, que empieza en cero, y la hora del paso actual.",
    # s21
    "Dos ayudantes acortan los pasos. lights() fija las cinco luces de una vez, como el botón de la cafetera del LED de color.",
    # s22
    "El otro, goTo(), pone el número en state y anota la hora.",
    # s23
    "En el loop, la parte uno es el botón. Un pulso nuevo cuenta solo con verde, y se recuerda que alguien espera.",
    # s23b
    "Pausa y predice: pulsas el botón con el peatón ya cruzando. ¿Cuenta?",
    # s23c
    "No. Solo cuentan en el paso cero, así el cruce nunca reinicia por accidente.",
    # s24
    "La parte dos empieza con una resta: ahora menos el momento en que empezó el paso. Es cuánto llevamos en él.",
    # s25
    "Luego, map() vuelve la perilla el tiempo del verde, de tres a diez segundos.",
    # s26
    "Paso cero: autos en verde, peatón en rojo. Con espera y verde largo, paso uno.",
    # s27
    "Los dos ampersands son el and del reto: ambas se cumplen.",
    # s28
    "Ahora pausa e inténtalo: escribe el paso uno. Los autos van dos segundos en amarillo, luego pasamos al paso dos.",
    # s29
    "Una forma: amarillo y, a los dos segundos, olvida el pedido, paso dos.",
    # s30
    "Paso dos: autos en rojo y peatón en verde por cuatro segundos.",
    # s31
    "Paso tres: parpadea cada cuarto de segundo; a los dos, paso cero.",
    # s32
    "Pausa y predice: autos recién en verde y pulsas ya. ¿El peatón recibe verde al instante?",
    # s33
    "No. El pulso queda guardado, pero los autos mantienen el verde hasta que acabe el tiempo de la perilla.",
    # s34
    "Aquí de verdad. Mira la ronda completa: la luz peatonal pasa de rojo a verde.",
    # s35
    "Últimos dos segundos: la luz parpadea, apúrate, y los autos en rojo.",
    # s36
    "Ahora cambia un número. Pausa y predice: si cuatro mil pasa a ocho mil, ¿qué cambia?",
    # s37
    "El peatón tiene el doble de tiempo. Nada más cambia: cada paso guarda su propio tiempo.",
    # s38
    "El proyecto tiene un truco más: medir cuánto se mantuvo el botón. Piensa en un ticket.",
    # s39
    "Al entrar, el ticket marca la hora. Al salir, restas y pagas la diferencia.",
    # s40
    "Realmente, al pulsar guardamos el ahora en una variable, pressStart. Al soltar, now menos pressStart es el tiempo pulsado.",
    # s41
    "Sin papel. pressStart es un número en memoria, y el próximo pulso lo sobrescribe.",
    # s42
    "press_time: amarillo encendido al sostener. Al soltar, el Serial Monitor da el tiempo, corto o largo.",
    # s43
    "Menos de un cuarto de segundo es corto. Pausa y predice: tocas el botón rapidísimo. ¿Qué imprime?",
    # s44
    "Unos cien milisegundos, y corto. Mantenlo un segundo e imprime unos mil, y largo.",
    # s45
    "Un botón hace dos trabajos. Tu celular: toque despierta, largo apaga.",
    # s46
    "Error posible: state igual a uno, sin anotar la hora.",
    # s47
    "¿Qué hace entonces el cruce?",
    # s48
    "El amarillo parpadea y desaparece. La hora de inicio es la vieja, y la resta dice que pasaron dos segundos.",
    # s49
    "Por eso goTo() hace ambas cosas. Úsalo siempre.",
    # s50
    "Pausa el video y explica por qué cada paso necesita su hora de inicio. Una frase basta.",
    # s51
    "Cada paso mide su tiempo desde que empezó. Un paso nuevo necesita inicio nuevo, o cree que ya acabó.",
    # s52
    "Tu turno: modo lento. Botón más de un segundo y el verde dura el doble.",
    # s53
    "Ya conoces las dos piezas: el ticket y un paso con su tiempo. Solución en la carpeta.",
    # s54
    "Hoy hiciste tres cosas. Una variable state que recuerda el paso. Una hora de inicio por paso, sin esperar. Y un ticket para los pulsos del botón.",
    # s55
    "La próxima: juego de reflejos con récord que sobrevive sin corriente. Comenta cuánto dura el verde de tu cruce.",
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
