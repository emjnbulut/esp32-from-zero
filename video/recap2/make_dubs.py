"""Source of video/recap2/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, comes from make_script.py via dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
The same text is the subtitle for hi/pt/es (see make_subs.py: dub and subtitle must be the same sentences).
These voices speak slower than English: every line must be SHORT (mean ratio <= 0.72, max <= 0.92 vs the English text).
Usage: python video/recap2/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "साँस लेती LED। कोई भी रंग। knob, level bar, crossing और reflex game।",
    # s02
    "आज कुछ नया नहीं। पुराने sketches दोबारा पढ़ेंगे, और सात सवालों से ख़ुद को परखेंगे।",
    # s03
    "काग़ज़ उठाइए। हर सवाल के बाद वीडियो रोकिए, जवाब दीजिए, सही हो तो एक अंक।",
    # s04
    "तीन हिस्से: रोशनी, knob पढ़ना, और कदम याद रखना। नए हैं? पहला episode स्क्रीन पर है।",
    # s05
    "पहला हिस्सा। छत का पंखा याद है? इतना तेज़ घूमता है कि बस धुंधलापन दिखता है।",
    # s06
    "असल में pin एक सेकंड में हज़ार बार चालू-बंद होता है। जितनी देर चालू, LED उतनी तेज़।",
    # s07
    "पंखे से फ़र्क: LED कभी आधी चालू नहीं होती। बस चालू या बंद।",
    # s08
    "साँस लेती LED: हर चार millisecond में चमक एक कदम बढ़ती है। ऊपर पहुँचकर कदम उलटा, झूले की तरह।",
    # s09
    "रोकिए, अंदाज़ा लगाइए: चमक ऊपर पहुँची। कदम अब क्या है? प्लस एक से माइनस एक।",
    # s10
    "सवाल एक, वीडियो रोकिए: analogWrite(pin, 64) में pin हर चक्र में कितना चालू है?",
    # s11
    "लगभग चौथाई। दो सौ पचपन हमेशा चालू है, तो चौंसठ क़रीब चौथाई।",
    # s12
    "अब color LED। फ़ोन स्क्रीन की तरह, एक पैकेज में तीन बत्तियाँ: लाल, हरी, नीली।",
    # s13
    "पेंट से फ़र्क: रोशनी जुड़ती है। लाल और हरी मिलकर पीली, भूरी नहीं। setColor() कॉफ़ी मशीन का बटन: एक call, तीन मान।",
    # s14
    "सवाल दो, वीडियो रोकिए: setColor(255, 0, 255) कौन सा रंग देगा?",
    # s15
    "मैजेंटा। पूरा लाल, पूरा नीला, हरा नहीं।",
    # s16
    "दूसरा हिस्सा। knob फिसलपट्टी है: प्रतिरोध की पट्टी पर सरकता संपर्क। बीच का पैर वहाँ का voltage देता है।",
    # s17
    "analogRead() voltage को चार हज़ार छियानवे निशानों के फ़ीते से नापता है: शून्य वोल्ट पर शून्य, तीन दशमलव तीन पर आख़िरी।",
    # s18
    "map() शहर का नक्शा है: नंबर पहली range में कहाँ है, दूसरी में वही जगह लौटाता है।",
    # s19
    "फ़र्क: ये पूरे नंबरों पर चलता है, हमेशा नीचे गोल करता है।",
    # s20
    "dimmer: knob बीच में, रीडिंग क़रीब दो हज़ार, और map() उसे एक सौ सत्ताईस की चमक बनाता है।",
    # s21
    "रोकिए, अंदाज़ा लगाइए: knob पूरा ऊपर। चमक क्या होगी? दो सौ पचपन, सबसे ऊपर।",
    # s22
    "सवाल तीन, ज़रूरत हो तो रोकिए। पीली का समय map(value, 0, 4095, 1000, 4000) है। knob बीच में। पीली कितनी देर?",
    # s23
    "लगभग ढाई सेकंड। आधा knob, एक और चार का बीच।",
    # s24
    "सवाल चार, फिर रोकिए: LED pin चौंतीस पर लगाई, तार ठीक, फिर भी बुझी। क्यों?",
    # s25
    "Pin चौंतीस से उनतालीस एकतरफ़ा दरवाज़े हैं: सिर्फ़ सुनते हैं। knob के लिए बढ़िया, LED के लिए नहीं।",
    # s26
    "तीसरा हिस्सा। washing machine: धोना, खंगालना, सुखाना। उसे पता है वो किस कदम पर है, समय ख़त्म तो आगे।",
    # s27
    "कदम एक पूरा नंबर है, state। आगे बढ़ना दो काम: नया नंबर और समय, और goTo() दोनों करता है।",
    # s28
    "मशीन से फ़र्क: हमारा loop कदम में कभी इंतज़ार नहीं करता। हज़ारों बार नंबर देखकर फ़ैसला करता है।",
    # s29
    "reflex game: लाल, पीली, हरी, goTo() समय लिखता है। कदम तीन में समय बढ़ता है, मोहर लगे पार्किंग टिकट जैसा।",
    # s30
    "रोकिए, सोचिए कौन सा नंबर reaction बनेगा। press आई, वो समय reaction है। रिकॉर्ड तोड़े तो दराज़ में, यानी flash memory में।",
    # s31
    "सवाल पाँच, वीडियो रोकिए। किसी ने सिर्फ़ state बराबर एक किया, समय भूल गया। अगले कदम का क्या होगा?",
    # s32
    "वो लगभग तुरंत ख़त्म होगा। शुरुआती समय पुराना है, तो घटाने पर समय कब का बीत चुका।",
    # s33
    "सवाल छह, वीडियो रोकिए। crossing में पैदल यात्री के पार करते समय आपने button दबाया। क्या press गिनी जाएगी?",
    # s34
    "नहीं। press सिर्फ़ कदम शून्य में गिनी जाती है, जब गाड़ियों को हरी है।",
    # s35
    "आख़िरी सवाल, वीडियो रोकिए। रिकॉर्ड दराज़ में है, board निकाल दिया। restart के बाद getULong() क्या देगा?",
    # s36
    "पुराना रिकॉर्ड। सिर्फ़ ख़ाली पन्ना डिफ़ॉल्ट देता है: नौ नौ नौ नौ।",
    # s36b
    "गिनने से पहले: वीडियो रोकिए, और map() क्या करता है, अपने शब्दों में बताइए। एक वाक्य काफ़ी।",
    # s36c
    "एक तरीका: नंबर एक range में कहाँ है, दूसरी range में वही जगह देता है।",
    # s37
    "अंक गिनिए। छह या सात: आप अगले हिस्से के लिए तैयार हैं।",
    # s38
    "कम? हर सवाल के साथ उसका episode लिखा है। वो दोबारा देखिए, छोटा है।",
    # s39
    "अगली बार: light sensor, और अँधेरे में ख़ुद जलने वाला lamp। कमेंट में स्कोर बताइए। मिलते हैं!",
]

PT = [
    # s01
    "Um LED que respira. Qualquer cor. Knob, barra, cruzamento e jogo de reflexo.",
    # s02
    "Hoje nada novo. Vamos reler os sketches e você se testa com sete perguntas.",
    # s03
    "Pegue papel. Após cada pergunta, pause o vídeo, responda e ganhe um ponto se acertar.",
    # s04
    "Três partes: luz, ler um knob e lembrar passos. Novo aqui? O episódio um está na tela.",
    # s05
    "Parte um. Lembra do ventilador? Gira tão rápido que se vê um borrão, não as pás.",
    # s06
    "O pino liga e desliga umas mil vezes por segundo. Quanto mais tempo ligado, mais o LED brilha.",
    # s07
    "Diferença: o LED nunca fica meio ligado. Só liga ou desliga.",
    # s08
    "O LED que respira: a cada quatro milissegundos, um passo. No topo, o passo vira negativo, como um balanço.",
    # s09
    "Pause e preveja: o brilho chegou ao topo. Qual é o passo? De mais um para menos um.",
    # s10
    "Pergunta um, pause: com analogWrite(pin, 64), quanto do ciclo o pino fica ligado?",
    # s11
    "Um quarto. Duzentos e cinquenta e cinco é sempre ligado; sessenta e quatro, um quarto.",
    # s12
    "O LED colorido: como a tela do celular, três luzinhas num pacote: vermelha, verde e azul.",
    # s13
    "Diferença da tinta: a luz soma. Vermelho e verde dão amarelo. E setColor() é o botão da cafeteira: uma chamada, três valores.",
    # s14
    "Pergunta dois, pause o vídeo: que cor sai de setColor(255, 0, 255)?",
    # s15
    "Magenta. Vermelho total, azul total, sem verde.",
    # s16
    "Parte dois. O knob é um escorregador: um contato desliza numa resistência. A perna do meio dá a tensão.",
    # s17
    "analogRead() mede a tensão numa régua de quatro mil e noventa e seis marcas: de zero a três vírgula três volts.",
    # s18
    "map() é o mapa da cidade: acha onde o número está na primeira faixa e devolve o ponto na segunda.",
    # s19
    "Diferença: usa números inteiros e sempre arredonda para baixo.",
    # s20
    "O dimmer: knob no meio, leitura uns dois mil, e map() vira brilho cento e vinte e sete.",
    # s21
    "Pause e preveja: knob no máximo. Qual o brilho? Duzentos e cinquenta e cinco.",
    # s22
    "Pergunta três, pause quando precisar. O amarelo é map(value, 0, 4095, 1000, 4000). Knob no meio. Quanto dura o amarelo?",
    # s23
    "Uns dois segundos e meio. Meio knob é meio caminho entre um e quatro.",
    # s24
    "Pergunta quatro, pause: um LED no pino trinta e quatro fica apagado, com a fiação certa. Por quê?",
    # s25
    "Os pinos trinta e quatro a trinta e nove só escutam. Bons para knob, não para LED.",
    # s26
    "Parte três. A máquina de lavar: lavar, enxaguar, centrifugar. Sabe o passo e segue quando o tempo acaba.",
    # s27
    "O passo é um número inteiro, o state. Seguir são dois trabalhos, número e hora, e goTo() faz os dois.",
    # s28
    "Diferença: nosso loop nunca espera dentro do passo. Olha o número milhares de vezes e decide.",
    # s29
    "O jogo: goTo() anota a hora. No passo três o tempo cresce, como um ticket carimbado.",
    # s30
    "Pause e preveja qual número é a reação. O aperto vem, esse tempo. Se bate o recorde, vai para a gaveta, a memória flash.",
    # s31
    "Pergunta cinco, pause o vídeo. Alguém muda só state para um e esquece a hora. O que acontece com o próximo passo?",
    # s32
    "Acaba quase na hora. A hora de início é a antiga, então o tempo já passou faz tempo.",
    # s33
    "Pergunta seis, pause o vídeo. No cruzamento, você aperta o botão com o pedestre atravessando. Esse aperto conta?",
    # s34
    "Não. Só contam no passo zero, quando os carros têm verde.",
    # s35
    "Última pergunta, pause o vídeo. O recorde está na gaveta e você desliga a placa. Depois, o que getULong() devolve?",
    # s36
    "O antigo. Só página vazia dá o padrão: nove nove nove nove.",
    # s36b
    "Antes de contar: pause e explique com suas palavras o que map() faz. Uma frase basta.",
    # s36c
    "Um jeito: acha onde o número está numa faixa e devolve o ponto na outra.",
    # s37
    "Conte os pontos. Seis ou sete: pronto para a próxima parte.",
    # s38
    "Menos? Cada pergunta mostra seu episódio. Reveja, é curto, e volte.",
    # s39
    "Na próxima: sensor de luz e uma lâmpada que acende no escuro. Conte sua pontuação nos comentários. Até lá!",
]

ES = [
    # s01
    "Un LED que respira. Cualquier color. Perilla, barra, cruce y juego de reflejos.",
    # s02
    "Hoy nada nuevo. Releeremos los sketches y te pondrás a prueba con siete preguntas.",
    # s03
    "Toma papel. Tras cada pregunta, pausa el video, responde y gana un punto si aciertas.",
    # s04
    "Tres partes: luz, perilla y recordar pasos. ¿Nuevo? El episodio uno está en pantalla.",
    # s05
    "Parte uno. ¿Recuerdas el ventilador? Gira tan rápido que solo ves un borrón.",
    # s06
    "El pin se enciende y apaga mil veces por segundo. Más tiempo encendido, más brilla.",
    # s07
    "Diferencia: el LED nunca está medio encendido. Solo encendido o apagado.",
    # s08
    "El LED que respira: cada cuatro milisegundos, un paso. Arriba, el paso se vuelve negativo, como un columpio.",
    # s09
    "Pausa y predice: el brillo llegó arriba. ¿Cuál es el paso? De más uno a menos uno.",
    # s10
    "Pregunta uno, pausa: con analogWrite(pin, 64), ¿cuánto del ciclo está encendido el pin?",
    # s11
    "Un cuarto: doscientos cincuenta y cinco es siempre encendido.",
    # s12
    "El LED de color: como la pantalla del celular, tres lucecitas en un paquete: roja, verde y azul.",
    # s13
    "La luz suma: rojo y verde dan amarillo. Y setColor() es el botón de la cafetera: una llamada, tres valores.",
    # s14
    "Pregunta dos, pausa el video: ¿qué color da setColor(255, 0, 255)?",
    # s15
    "Magenta. Rojo total, azul total, sin verde.",
    # s16
    "Parte dos. La perilla es un tobogán: un contacto se desliza por una resistencia. La pata del medio da el voltaje.",
    # s17
    "analogRead() mide el voltaje con una regla de cuatro mil noventa y seis marcas: de cero a tres coma tres voltios.",
    # s18
    "map() es el mapa de la ciudad: ve dónde está el número en el primer rango y da el mismo punto del segundo.",
    # s19
    "Diferencia: usa enteros y siempre redondea hacia abajo.",
    # s20
    "El dimmer: perilla al medio, lectura unos dos mil, y map() da brillo ciento veintisiete.",
    # s21
    "Pausa y predice: perilla al máximo. ¿Qué brillo? Doscientos cincuenta y cinco.",
    # s22
    "Pregunta tres, pausa si quieres. El amarillo es map(value, 0, 4095, 1000, 4000). Perilla al medio. ¿Cuánto dura?",
    # s23
    "Unos dos segundos y medio. La perilla a la mitad: entre uno y cuatro.",
    # s24
    "Pregunta cuatro, pausa: un LED en el pin treinta y cuatro no enciende, con buen cableado. ¿Por qué?",
    # s25
    "Los pines treinta y cuatro a treinta y nueve solo escuchan. Sirven para perilla, no para LED.",
    # s26
    "Parte tres. La lavadora: lavar, enjuagar, centrifugar. Sabe su paso y sigue al acabar el tiempo.",
    # s27
    "El paso es un número entero, el state. Avanzar son dos trabajos, número y hora, y goTo() hace ambos.",
    # s28
    "Nuestro loop nunca espera dentro del paso. Mira el número miles de veces y decide.",
    # s29
    "El juego: goTo() anota la hora. En el paso tres el tiempo sube, como un ticket sellado.",
    # s30
    "Pausa y predice: ¿qué número es la reacción? La pulsación llega, ese tiempo. Si supera el récord, va al cajón, la memoria flash.",
    # s31
    "Pregunta cinco, pausa el video. Alguien pone state en uno y olvida la hora. ¿Qué pasa con el siguiente paso?",
    # s32
    "Termina casi al instante. La hora de inicio es la vieja, así que el tiempo ya pasó.",
    # s33
    "Pregunta seis, pausa el video. En el cruce pulsas con el peatón cruzando. ¿Cuenta esa pulsación?",
    # s34
    "No. Solo cuentan en el paso cero, cuando los autos tienen verde.",
    # s35
    "Última pregunta, pausa el video. Desconectas la placa con el récord en el cajón. Después, ¿qué devuelve getULong()?",
    # s36
    "El viejo. Solo una página vacía da nueve nueve nueve nueve.",
    # s36b
    "Antes de contar: pausa y explica con tus palabras qué hace map(). Una frase basta.",
    # s36c
    "Una forma: ve dónde está el número en un rango y da el mismo punto en otro.",
    # s37
    "Cuenta tus puntos. Seis o siete: listo para la siguiente parte.",
    # s38
    "¿Menos? Cada pregunta muestra su episodio. Míralo otra vez, es corto, y regresa.",
    # s39
    "La próxima: sensor de luz y una lámpara que se enciende sola. Cuéntame tu puntaje en los comentarios. ¡Nos vemos!",
]

TARGET = {"hi": 0.92, "pt": 0.92, "es": 0.92}
MEAN_TARGET = 0.72


def check(langs, english):
    """Print per-language max/mean char ratio vs the English narration; return the over-target lines."""
    over = []
    for lang, seg in langs.items():
        ratios = {k: len(seg[k]) / len(english[k]) for k in english}
        worst = max(ratios, key=ratios.get)
        mean = sum(ratios.values()) / len(ratios)
        print(f"{lang}: max {ratios[worst]:.2f} ({worst}), mean {mean:.2f}, target max <= {TARGET[lang]:.2f}, mean <= {MEAN_TARGET:.2f}")
        if mean > MEAN_TARGET:
            print(f"  OVER {lang} mean {mean:.2f}")
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
