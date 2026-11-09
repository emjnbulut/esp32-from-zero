"""Source of video/ep08/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, is edited in dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
Usage: python video/ep08/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
EXTRA = {  # s25b, added after the first narration (pin 17 is printed TX2)
    "hi": "ध्यान दें: ज़्यादातर boards पर pin सत्रह को TX दो लिखते हैं।",
    "pt": "Atenção: na maioria das placas, o pino dezessete aparece como tê xis dois, não dê dezessete.",
    "es": "Ojo: el pin diecisiete no dice de diecisiete, dice te equis dos.",
}
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "देखिए ये रोशनी की पट्टी। Knob घुमाता हूँ, तो हरी, पीली, लाल भरती है।",
    # s02
    "इस video के अंत तक आप एक function से संख्याओं का पैमाना बदलेंगे, और ये पट्टी बनाएँगे।",
    # s03
    "पहले, पिछले episode से दो सवाल। छोटा सवाल: knob ठीक बीच में है। analogRead() लगभग कौन सी संख्या देगा?",
    # s04
    "करीब दो हज़ार, यानी आधा। पूरा चार हज़ार तक है।",
    # s05
    "छोटा सवाल: LED knob की सुनती ही नहीं। सबसे पहले क्या करेंगे?",
    # s06
    "Value print करते हैं, जैसे डॉक्टर बुखार नापता है। संख्या बताती है कहाँ देखना है।",
    # s07
    "पिछला circuit चाहिए, knob और लाल LED वाला। पीली और हरी LED, दो सौ बीस ओम के resistor, और wires जोड़िए।",
    # s08
    "पिछली बार knob का बड़ा पैमाना सोलह से भाग देकर LED में बिठाया। चला, पर सोलह समझना पड़ता है।",
    # s09
    "नक्शा सोचिए। शहर का बीच, कागज़ पर नक्शे का बीच।",
    # s10
    "ठीक इसी नाम का function है: map()। संख्या, उसका पैमाना और चाहिए वाला पैमाना दीजिए, मेल खाती संख्या मिलेगी।",
    # s11
    "असल में map() सीधा हिसाब है। वो देखता है आपकी संख्या पहले पैमाने में कितनी आगे है, और दूसरे पैमाने में वही जगह लौटाता है।",
    # s12
    "कागज़ी नक्शे से फ़र्क: वो सिर्फ़ छोटा कर सकता है। map() छोटे पैमाने को बड़ा भी कर सकता है, या उलट भी दे, यानी ऊपर वाला नीचे हो जाए।",
    # s13
    "ये रही line। पहले संख्या, यानी knob की value। फिर knob का पैमाना कहाँ से कहाँ तक। फिर चमक का पैमाना कहाँ से कहाँ तक।",
    # s14
    "छोटा सवाल: knob लगभग दो हज़ार पढ़ता है, करीब बीच में। map() कितनी चमक लौटाएगा?",
    # s15
    "करीब एक सौ सत्ताईस, चमक का बीच। बीच में अंदर, बीच में बाहर।",
    # s16
    "ये रहा पूरा sketch, map_dimmer। पिछला dimmer ही है, बस भाग वाली line map() हो गई।",
    # s17
    "Loop में analogRead() संख्या value में रखता है, map() उसे brightness बनाता है।",
    # s18
    "Video रोकिए और अंदाज़ा लगाइए: क्या सोलह से भाग वाले पिछले version से LED अलग दिखेगी?",
    # s19
    "नहीं। वैसी ही, अँधेरे से पूरी चमक तक चिकनी। फ़र्क code में है: ये line पढ़ते ही दोनों पैमाने दिख जाते हैं।",
    # s20
    "अब एक चीज़ बदलते हैं। Video रोकिए, अंदाज़ा लगाइए: आख़िरी दो संख्याएँ पलट दें, चमक दो सौ पचपन से शून्य की ओर चले, तो?",
    # s21
    "Knob उल्टा चलता है। बाएँ घुमाओ तो LED तेज़, दाएँ घुमाओ तो बुझ जाती है। यही वो उलटना था।",
    # s22
    "अब पट्टी। फ़ोन की battery सोचिए: जितना charge, उतनी पट्टी।",
    # s23
    "असल में हम knob की संख्या को छोटे level में बदलते हैं, शून्य से तीन तक। Level बताता है कितनी LED जलें, हरी से गिनकर।",
    # s24
    "फ़ोन हर पट्टी के पीछे कई छोटे कदम छिपाता है। हमारी पट्टी में सिर्फ़ चार हाल हैं।",
    # s25
    "Cable निकालिए। पीली LED pin अठारह पर, और हरी pin सत्रह पर। हर एक का अपना resistor, लाल की तरह।",
    # s26
    "लंबा पैर pin की तरफ़, छोटा minus rail की तरफ़। याद रखिए, काम आएगा।",
    # s27
    "भीड़ लगे तो knob को ऊपर सरका दीजिए, उसके wires साथ चले जाएँगे। Rails बीच से कटी हों, तो bridge wires रखिए।",
    # s28
    "अब level। सीधी line knob के पैमाने को शून्य से तीन पर बिठाती है।",
    # s29
    "Video रोकिए, अंदाज़ा लगाइए: इस line से तीनों LED कितनी बार एक साथ जलेंगी?",
    # s30
    "लगभग कभी नहीं। map() दशमलव का हिस्सा गिरा देता है।",
    # s31
    "Level तीन पैमाने के आख़िरी निशान पर ही आता है। और पिछली बार देखा, पैमाना उस निशान तक शायद पहुँचे ही नहीं।",
    # s32
    "हल: चार level माँगिए, पैमाना एक निशान लंबा मानिए। Reading तीन पर रुकती है, हर level को बराबर हिस्सा मिलता है।",
    # s33
    "ये sketch है, level_bar। setup() तीन pins को output बनाता है। Loop में knob पढ़कर map() से level लेते हैं।",
    # s34
    "फिर चूल्हे के निशान, if और else if। Level शून्य पर तीनों बंद। Level एक पर सिर्फ़ हरी, level दो पर पीली भी।",
    # s35
    "कोई नहीं, तो तीन। आख़िरी else सब जलाता है।",
    # s36
    "Video रोकिए, अंदाज़ा लगाइए: knob बीच से थोड़ा आगे है। कौन सी LED जलेंगी?",
    # s37
    "हरी और पीली, level दो।",
    # s38
    "देखिए। धीरे घुमाइए, पट्टी एक-एक करके भरती और खाली होती है।",
    # s39
    "अब एक ग़लती जो हो सकती है। हरी और लाल जलती हैं, पर पीली बुझी है। छोटा सवाल: ग़लती code में है या wiring में?",
    # s40
    "पहले बुखार नापिए। Serial Monitor कहता है level तीन, यानी code पीली चाहता है। गड़बड़ी wiring में है।",
    # s41
    "पीली LED उल्टी लगी है। LED करंट सिर्फ़ एक तरफ़ जाने देती है, लंबे पैर से छोटे पैर की ओर।",
    # s42
    "उल्टी हो तो बस बुझी रहती है, कुछ ख़राब नहीं होता। पलटिए, पट्टी पूरी।",
    # s43
    "अब video रोकिए, और अपने शब्दों में बताइए कि पहली level वाली line तीनों LED लगभग कभी क्यों नहीं जलाती थी। एक वाक्य काफ़ी।",
    # s44
    "एक तरीका: map() नीचे गोल करता है, इसलिए ऊँचा level पैमाने के आख़िर में ही आता था।",
    # s45
    "आपकी बारी: Rotary Safe Lock। Knob को शून्य से निन्यानवे पर बिठाइए, संख्या print कीजिए।",
    # s46
    "गुप्त code तीन संख्याएँ हैं, हर एक के बाद button दबाइए।",
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
    "No fim, você converte faixas de números com uma função e monta esta barra.",
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
    "Antes, encaixamos a escala do seletor na do LED dividindo por dezesseis. Funcionou, mas ninguém entende esse dezesseis.",
    # s09
    "Pense num mapa da cidade. Cada rua tem seu lugar no papel, e o meio da cidade é o meio do mapa.",
    # s10
    "O Arduino tem uma função com esse nome: map(). Você dá um número, a faixa de origem e a faixa que quer, e ela devolve o número equivalente.",
    # s11
    "Na real, map() é conta: acha a posição numa faixa e repete na outra.",
    # s12
    "A diferença do mapa de papel: ele só encolhe. A map() também estica uma faixa pequena, ou inverte, e o topo vira o fundo.",
    # s13
    "Aqui a linha. Primeiro o número, o valor do seletor. Depois onde a faixa dele começa e termina. Depois a do brilho.",
    # s14
    "Pergunta rápida: o seletor lê uns dois mil, quase no meio. Que brilho a map() devolve?",
    # s15
    "Uns cento e vinte e sete, o meio. Meio entra, meio sai.",
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
    "O seletor funciona ao contrário. À esquerda o LED fica forte, à direita apaga. É a inversão.",
    # s22
    "Agora a barra. Pense no ícone de bateria: mais carga, mais barras.",
    # s23
    "Na verdade, o número do seletor vira um nível, de zero a três. O nível diz quantos LEDs acendem, a partir do verde.",
    # s24
    "O celular esconde muitos passos em cada barra. A nossa tem só quatro estados.",
    # s25
    "Tire o cabo. O LED amarelo vai no pino dezoito e o verde no dezessete. Cada um com seu resistor, como o vermelho.",
    # s26
    "Perna longa para o pino, curta para o trilho de menos. Guarde isso.",
    # s27
    "Se apertar, suba o seletor, e os fios vão junto. Se os trilhos forem divididos no meio, mantenha as pontes.",
    # s28
    "Agora o nível. A linha óbvia leva a faixa para zero a três.",
    # s29
    "Pause e preveja: com essa linha, quantas vezes os três LEDs acendem?",
    # s30
    "Quase nunca. map() usa inteiros e corta depois da vírgula. Dois vírgula nove vira dois.",
    # s31
    "O nível três só vem na última marca da régua. E vimos que a régua pode nem chegar nessa marca.",
    # s32
    "A solução: peça quatro níveis e finja que a régua tem uma marca a mais. A leitura nunca chega a quatro, para em três, e cada nível ganha uma fatia igual.",
    # s33
    "Este é o level_bar. O setup() faz três saídas. No loop, a map() dá o nível.",
    # s34
    "Depois, as marcas do fogão, if e else if. Nível zero apaga tudo. Nível um acende o verde, e o dois soma o amarelo.",
    # s35
    "Se não for nenhum, é três: o último else acende tudo.",
    # s36
    "Pause e preveja: o seletor passou um pouco do meio. Quais LEDs acendem?",
    # s37
    "Verde e amarelo. Passou do meio: nível dois.",
    # s38
    "Agora de verdade. Gire devagar, e a barra enche uma luz por vez, depois esvazia.",
    # s39
    "Agora um erro possível. Verde e vermelho acendem, o amarelo não. Pergunta rápida: é o código ou a fiação?",
    # s40
    "Meça a febre. O Serial Monitor diz nível três: o código quer amarelo. É a fiação.",
    # s41
    "O LED amarelo está ao contrário. Ele só deixa a corrente passar num sentido, da perna longa à curta.",
    # s42
    "Ao contrário, ele só fica apagado, sem estragar. Vire, e a barra fica completa.",
    # s43
    "Agora pause e explique com suas palavras por que a primeira linha quase nunca acendia os três LEDs. Uma frase basta.",
    # s44
    "Um jeito: a map() arredonda para baixo, então o nível máximo só vinha no fim da régua, e ela raramente chega lá.",
    # s45
    "Sua vez: Rotary Safe Lock. Leve o seletor de zero a noventa e nove e imprima: é disco de cofre.",
    # s46
    "O código são três números. Aperte o botão após cada um.",
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
    "Al final, cambiarás rangos de números con una función, y harás esta barra.",
    # s03
    "Primero, dos preguntas del episodio pasado. Pregunta rápida: perilla en el medio. ¿Qué número da analogRead()?",
    # s04
    "Dos mil, la mitad. La regla entera llega a cuatro mil.",
    # s05
    "Pregunta rápida: el LED ignora la perilla. ¿Qué es lo primero que haces?",
    # s06
    "Imprimes el valor, como el doctor que mide la fiebre. El número dice qué mitad del circuito revisar.",
    # s07
    "Usa el circuito pasado, con perilla y LED rojo. Suma LED amarillo y verde, resistencias de doscientos veinte ohmios.",
    # s08
    "La vez pasada ajustamos la escala de la perilla a la del LED, dividiendo entre dieciséis. Funcionó, pero nadie entiende el dieciséis.",
    # s09
    "Piensa en un mapa de la ciudad. Cada calle tiene su lugar en el papel, y la mitad de la ciudad es la mitad del mapa.",
    # s10
    "Arduino tiene una función con ese nombre: map(). Le das un número, el rango de origen y el que quieres, y devuelve el número equivalente.",
    # s11
    "Realmente, map() es aritmética. Ve dónde está tu número en el primer rango y da esa posición en el otro.",
    # s12
    "Un mapa de papel solo encoge. map() también estira un rango, o lo invierte, y arriba queda abajo.",
    # s13
    "Esta es la línea. Primero el número, el valor de la perilla. Luego su rango y el brillo.",
    # s14
    "Pregunta rápida: la perilla lee unos dos mil, casi en el medio. ¿Qué brillo devuelve map()?",
    # s15
    "Unos ciento veintisiete: la mitad.",
    # s16
    "Aquí map_dimmer. Es el dimmer pasado, pero con map() en vez de dividir.",
    # s17
    "En el loop, analogRead() guarda la perilla en value. map() lo vuelve brightness, y se envía al LED.",
    # s18
    "Pausa el video y predice: ¿se verá distinto el LED que en la versión pasada, la que dividía entre dieciséis?",
    # s19
    "No. Igual, suave de oscuro a pleno. La diferencia está en el código: quien lee la línea ve los dos rangos.",
    # s20
    "Ahora cambiamos algo. Pausa y predice: si cambiamos los dos últimos números, y el brillo va de doscientos cincuenta y cinco a cero, ¿qué pasa?",
    # s21
    "La perilla va al revés. A la izquierda brilla, a la derecha se apaga. Es la inversión.",
    # s22
    "Ahora la barra de luces. Piensa en el ícono de batería: más carga, más barras.",
    # s23
    "En realidad, el número de la perilla se vuelve un nivel, de cero a tres. El nivel dice cuántos LEDs encienden, desde el verde.",
    # s24
    "El celular esconde muchos pasitos en cada barra. La nuestra tiene cuatro estados.",
    # s25
    "Desconecta el cable. El LED amarillo va al pin dieciocho y el verde al diecisiete. Cada uno con su resistencia, como el rojo.",
    # s26
    "Pata larga hacia el pin, corta hacia el riel de menos. Recuérdalo.",
    # s27
    "Si se aprieta, sube la perilla, y sus cables suben con ella. Si tus rieles están partidos en el medio, deja los puentes.",
    # s28
    "Ahora el nivel. La línea obvia lleva el rango a cero a tres.",
    # s29
    "Pausa y predice: con esta línea, ¿cuántas veces encienden los tres LEDs?",
    # s30
    "Casi nunca. map() usa enteros y corta los decimales. Dos coma nueve es dos.",
    # s31
    "El nivel tres solo llega en la última marca de la regla, y la regla quizá nunca llega.",
    # s32
    "La solución: pide cuatro niveles y finge que la regla tiene una marca más. La lectura se queda en tres, y cada nivel recibe una porción igual.",
    # s33
    "Aquí el sketch, level_bar. setup() pone tres pines de salida. En el loop leemos la perilla y map() da el nivel.",
    # s34
    "Luego, if y else if, como la estufa. Cero apaga todo, uno enciende el verde, dos suma amarillo.",
    # s35
    "Si no es ninguno, es tres: el else enciende todo.",
    # s36
    "Pausa y predice: la perilla pasó un poco el medio. ¿Qué LEDs encienden?",
    # s37
    "Verde y amarillo. Pasó el medio: nivel dos.",
    # s38
    "Ahora de verdad. Gira despacio: la barra se llena y se vacía luz a luz.",
    # s39
    "Un error posible. Verde y rojo encienden, pero el amarillo no. Pregunta rápida: ¿es el código o el cableado?",
    # s40
    "Mide la fiebre: el Serial Monitor dice nivel tres. Falla el cable.",
    # s41
    "El amarillo está al revés. La corriente va de la pata larga a la corta.",
    # s42
    "Al revés queda apagado, sin daño. Dale la vuelta.",
    # s43
    "Ahora pausa y explica con tus palabras por qué la primera línea casi nunca encendía los tres LEDs. Una frase basta.",
    # s44
    "Una forma: map() redondea hacia abajo, así que el nivel máximo solo venía al final de la regla.",
    # s45
    "Tu turno: Rotary Safe Lock. La perilla va de cero a noventa y nueve, como una caja fuerte.",
    # s46
    "Son tres números seguidos. Presiona el botón tras cada uno.",
    # s47
    "Si aciertas los tres, el LED se pone verde. Si fallas, parpadea rojo y empiezas.",
    # s48
    "El truco: la perilla nunca es exacta, así que acepta unos números a cada lado del objetivo. Usa el and, dos ampersands: ambas condiciones deben cumplirse.",
    # s49
    "Una pista: una variable llamada step recuerda cuántos números ya están bien.",
    # s50
    "Hoy aprendiste tres cosas. map() cambia un número de rango. Siempre redondea hacia abajo. Un LED al revés no enciende.",
    # s51
    "Próximo: mini proyecto, un cruce peatonal con luces y botón. Tu código de la caja fuerte, a los comentarios; hay solución en la carpeta.",
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
