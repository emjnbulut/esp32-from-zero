"""Source of video/ep10/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, comes from make_script.py via dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
The same text is the subtitle for hi/pt/es (see make_subs.py: dub and subtitle must be the same sentences).
These voices speak slower than English: every line must be SHORT (mean ratio <= 0.75, max <= 0.95 vs the English text).
Usage: python video/ep10/make_dubs.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "लाल, पीली, हरी! मैं जल्दी से दबाता हूँ, और color LED हरी: बहुत तेज़ था।",
    # s02
    "आज आप यही reflex game बनाएँगे, उसी circuit पर। और बेस्ट टाइम board निकालने पर भी बचा रहेगा।",
    # s03
    "नए हैं? पहला episode स्क्रीन पर है। अब दो पुराने सवाल।",
    # s04
    "छोटा सवाल: goTo() हमेशा दो काम करता था। कौन से?",
    # s05
    "नया कदम state में डालता था, और समय लिखता था। समय के बिना नया कदम सोचता है कि ख़त्म हो चुका।",
    # s06
    "छोटा सवाल: color LED से नारंगी कैसे बनाएँ?",
    # s07
    "लाल पूरा, हरी थोड़ी सी, नीली बंद। रोशनी जुड़ती है, इसलिए नारंगी दिखता है।",
    # s08
    "नियम: शुरू करने को button दबाइए। लाल, फिर पीली, फिर हरी जलती है। हरी दिखते ही दबाइए।",
    # s09
    "Color LED नतीजा दिखाती है: तेज़ हरी, ठीक पीली, धीमा लाल। knob पीली का समय बदलता है, गिनती बेकार।",
    # s10
    "फिर से, एक भी नया तार नहीं। वही circuit जो crossing का था।",
    # s11
    "खेल फिर वही washing machine है, पाँच कदमों में: इंतज़ार, लाल, पीली, हरी, नतीजा।",
    # s12
    "वीडियो रोकिए, अंदाज़ा लगाइए: board reaction time कैसे नापे? तरकीब आप जानते हैं।",
    # s13
    "टिकट: हरी पर goTo() समय लिखता है। press पर अभी घटा वो पल: reaction।",
    # s14
    "यानी हरी कदम में बीता समय ही reaction time है। इसके लिए नया code नहीं चाहिए।",
    # s15
    "ये sketch है, reflex_game। ऊपर वही pins, state और शुरुआती समय, और रिकॉर्ड के लिए best variable।",
    # s16
    "पुराने helpers: setColor() नतीजा, lights() तीन LED, goTo() आगे बढ़ना।",
    # s17
    "पहला हिस्सा button। नया: pressed, सही या ग़लत वाला variable। नई press वाले एक ही round में सही।",
    # s18
    "रोकिए, अंदाज़ा लगाइए: button पूरा एक सेकंड दबाए रखा। pressed कितने round में सही होगा?",
    # s19
    "सिर्फ़ एक में। दबाए रखना दोबारा नहीं गिना जाता, तो हर कदम पूछ सकता है: अभी press हुई?",
    # s20
    "कदम शून्य press का इंतज़ार करता है। फिर लाल, और कदम एक।",
    # s21
    "कदम एक लाल को एक सेकंड रखता है। फिर पीली, और map() knob को एक से चार सेकंड में बदलता है।",
    # s22
    "अब रोकिए, ख़ुद कोशिश कीजिए: कदम दो लिखिए। पीली का समय ख़त्म तो हरी, और कदम तीन।",
    # s23
    "एक तरीका ये। बिल्कुल crossing जैसा: समय की जाँच, बत्तियाँ, और goTo()।",
    # s24
    "कदम तीन खेल का दिल है। pressed आने पर इस कदम का समय reaction है, और Serial Monitor छापता है।",
    # s25
    "फिर if और else if रंग चुनते हैं: चौथाई सेकंड से कम हरी, आधे से कम पीली, बाक़ी लाल।",
    # s26
    "कदम चार: रंग तीन सेकंड, फिर कदम शून्य।",
    # s27
    "असली में देखिए। बत्तियाँ देखिए, और आख़िर का रंग।",
    # s28
    "अब धीमी press, हरी के एक सेकंड बाद। Color LED कहती है: लाल।",
    # s29
    "एक संख्या बदलिए। रोकिए, अंदाज़ा लगाइए: दो सौ पचास की जगह दो सौ हो, तो हरी नतीजों का क्या होगा?",
    # s30
    "हरी पाना कठिन। सिर्फ़ बहुत तेज़ press चलेगी, ज़्यादा round पीले।",
    # s31
    "अब रिकॉर्ड। रोकिए, अंदाज़ा लगाइए: शानदार समय बनाया, फिर board निकालकर लगाया। रिकॉर्ड बचा है?",
    # s32
    "आम variable से नहीं। हर variable ऐसी memory में है जो बिजली जाने पर मिट जाती है। best फिर शुरू से।",
    # s33
    "अपनी मेज़ सोचिए। variables मेज़ पर रखे डिब्बे हैं, बिजली जाए तो मेज़ साफ़। पर दराज़ की कॉपी बची रहती है।",
    # s34
    "असल में: ESP32 अपनी flash memory का एक छोटा कोना रखता है, जहाँ program भी है। Preferences library वहाँ संख्याएँ लिखवाती है।",
    # s35
    "असली कॉपी से फ़र्क: दराज़ छोटी है, और हर लिखाई उसे थोड़ा घिसती है। इसलिए सिर्फ़ ज़रूरी बात पर लिखते हैं।",
    # s36
    "Sketch में तीन पंक्तियाँ। setup() में begin() दराज़ खोलता है।",
    # s37
    "फिर getULong() पन्ना best पढ़ता है। पन्ना ख़ाली हो तो दूसरा नंबर देता है: नौ नौ नौ नौ।",
    # s38
    "छोटा सवाल: शुरुआती रिकॉर्ड इतना बड़ा क्यों?",
    # s39
    "असली reaction छोटा होता है, तो पहला round हमेशा रिकॉर्ड।",
    # s40
    "कदम तीन: बेहतर reaction best में, और putULong() दराज़ में।",
    # s41
    "ये परीक्षा। cable निकालिए, थोड़ा रुकिए, फिर लगाइए।",
    # s42
    "Serial Monitor फिर शुरू होता है, पहली पंक्ति में पुराना रिकॉर्ड। दराज़ ने रखा।",
    # s43
    "अब एक आम ग़लती: कोई if के बिना हर round के बाद put लिखता है।",
    # s44
    "छोटा सवाल: एक धीमे round के बाद शानदार रिकॉर्ड का क्या होगा?",
    # s45
    "मिट गया, धीमा समय ऊपर लिखा। if से रिकॉर्ड बनता है: सिर्फ़ बेहतर समय।",
    # s46
    "रोकिए, अपने शब्दों में बताइए कि best अकेला रिकॉर्ड क्यों भूलता है, पर दराज़ क्यों रखती है। एक वाक्य काफ़ी है।",
    # s47
    "यानी: variables को बिजली चाहिए। दराज़ flash memory है, बिना बिजली भी रखती है।",
    # s48
    "रोकिए, अंदाज़ा लगाइए: पीली के दौरान दबाएँ तो खेल क्या करता है?",
    # s49
    "कुछ नहीं। तो चीटर button दबाता रहे, और हरी को किस्मत से पकड़ ले।",
    # s50
    "आपकी बारी: ग़लत शुरुआत। लाल या पीली में press पर LED लाल चमके, समय न गिने।",
    # s51
    "एक कदम और एक जाँच और। हल folder में, और Short में।",
    # s52
    "आज पहला project पूरा हुआ। कदमों से बना खेल। reaction time यानी एक कदम का समय। और दराज़ में रिकॉर्ड।",
    # s53
    "अगली बार: episode पाँच से अब तक का recap, quiz के साथ। अपना बेस्ट time comments में!",
]

PT = [
    # s01
    "Vermelho, amarelo, verde! Aperto rápido e o LED colorido fica verde.",
    # s02
    "Hoje, este jogo no mesmo circuito. Seu recorde fica salvo, mesmo sem energia.",
    # s03
    "Novo aqui? O episódio um está na tela. Duas perguntas antigas.",
    # s04
    "Pergunta rápida: o goTo() sempre fazia dois trabalhos. Quais?",
    # s05
    "Colocava o novo passo em state e anotava a hora. Sem a hora, o passo novo acha que já acabou.",
    # s06
    "Rápido: como fazer laranja no LED colorido?",
    # s07
    "Vermelho total, um pouco de verde, azul apagado. A luz se soma: vira laranja.",
    # s08
    "As regras: aperte o botão para começar. Acende vermelho, amarelo, verde. Viu verde, aperte.",
    # s09
    "O LED mostra: verde rápido, amarelo médio, vermelho lento. O knob muda a espera do amarelo: não dá para contar.",
    # s10
    "De novo, nenhum fio novo. É o circuito da faixa.",
    # s11
    "O jogo é a máquina de lavar de novo, com cinco passos: espera, vermelho, amarelo, verde e resultado.",
    # s12
    "Pause e preveja: como a placa mede seu tempo de reação? Você já sabe o truque.",
    # s13
    "O ticket: no verde, goTo() anota a hora. Apertou: agora menos ela é a reação.",
    # s14
    "Então o tempo no passo verde é seu tempo de reação. Sem código novo.",
    # s15
    "Este é o sketch reflex_game. No topo, os mesmos pins, state e hora de início, mais best para o recorde.",
    # s16
    "Helpers conhecidos: setColor() no resultado, lights() nos três LEDs, goTo() para avançar.",
    # s17
    "Parte um, o botão. Novidade: pressed, verdadeiro ou falso. Só é verdadeiro na volta de uma nova pressão.",
    # s18
    "Pause e preveja: segurando o botão um segundo, quantas voltas pressed é verdadeiro?",
    # s19
    "Só uma. Segurar não conta de novo, então cada passo pergunta: apertou agora?",
    # s20
    "O passo zero espera o aperto. Acende o vermelho, passo um.",
    # s21
    "O passo um mantém o vermelho um segundo. Depois amarelo, e map() converte o knob em um a quatro segundos.",
    # s22
    "Pause e tente: escreva o passo dois. Acabou o amarelo, acende o verde e vamos ao passo três.",
    # s23
    "Uma forma. Igual à faixa: checar o tempo, as luzes e goTo().",
    # s24
    "O passo três é o coração. Com pressed, o tempo neste passo é a reação, e o Serial Monitor imprime.",
    # s25
    "Então if e else if escolhem a cor: menos de um quarto de segundo verde, menos de meio amarelo, senão vermelho.",
    # s26
    "O passo quatro mostra a cor por três segundos e volta ao passo zero.",
    # s27
    "Aqui de verdade. Veja as luzes e a cor no final.",
    # s28
    "Agora um aperto lento, após o verde. O LED fica vermelho.",
    # s29
    "Mude um número. Pause e preveja: se duzentos e cinquenta virar duzentos, o que muda nos verdes?",
    # s30
    "O verde fica difícil. Só apertos muito rápidos contam; mais rodadas ficam amarelas.",
    # s31
    "Agora o recorde. Pause e preveja: você faz um ótimo tempo e religa a placa. O recorde continua?",
    # s32
    "Com variável comum, não. Toda variável vive numa memória apagada sem energia. Depois, best recomeça.",
    # s33
    "Pense na mesa. Variáveis são caixas nela; sem energia, tudo some. O caderno na gaveta fica.",
    # s34
    "Na prática: o ESP32 reserva um cantinho da memória flash, a mesma do programa. A biblioteca Preferences grava números ali.",
    # s35
    "A diferença: a gaveta é pequena e cada gravação a desgasta um pouco. Então gravamos só o que vale guardar.",
    # s36
    "No sketch, três linhas. No setup(), begin() abre a gaveta.",
    # s37
    "Então getULong() lê a página best. Se vazia, devolve o segundo número, nove nove nove nove.",
    # s38
    "Rápido: por que um número tão grande?",
    # s39
    "Porque toda reação real é menor. A primeira rodada vira recorde.",
    # s40
    "No passo três: se a reação vence best, vira best, e putULong() grava.",
    # s41
    "O teste. Tire o cabo, espere e ligue de novo.",
    # s42
    "O Serial Monitor recomeça e a primeira linha mostra o recorde antigo.",
    # s43
    "Agora um erro comum. Para salvar o resultado, alguém escreve put em toda rodada, sem o if.",
    # s44
    "Rápido: e o recorde após uma rodada lenta?",
    # s45
    "Sumiu. O tempo lento foi gravado por cima. O if faz o recorde: só um tempo melhor entra.",
    # s46
    "Pause e explique com suas palavras por que best sozinho esquece o recorde e a gaveta guarda.",
    # s47
    "Ou seja: variáveis precisam de energia. A gaveta é flash, guarda sem energia.",
    # s48
    "Pause e preveja: o que o jogo faz se apertar no amarelo?",
    # s49
    "Nada. Um trapaceiro pode apertar sem parar e pegar o verde na sorte.",
    # s50
    "Sua vez, a largada falsa: apertar no vermelho ou amarelo faz o LED piscar vermelho, sem tempo.",
    # s51
    "Mais um passo e mais uma checagem. A solução está na pasta, e mostro num Short.",
    # s52
    "Hoje você terminou seu primeiro projeto. Um jogo de passos. Reação é o tempo de um passo. E um recorde na gaveta.",
    # s53
    "Na próxima, um resumo desde o episódio cinco, com quiz. Conte seu melhor tempo nos comentários!",
]

ES = [
    # s01
    "¡Rojo, amarillo, verde! Pulso rápido y el LED de color se pone verde.",
    # s02
    "Hoy armas este juego, mismo circuito. Y tu mejor tiempo queda guardado aunque desconectes.",
    # s03
    "¿Nuevo? El episodio uno está en pantalla. Dos preguntas.",
    # s04
    "Pregunta rápida: goTo() siempre hacía dos trabajos. ¿Cuáles?",
    # s05
    "Ponía el paso nuevo en state y anotaba la hora. Sin la hora, el paso nuevo cree que ya terminó.",
    # s06
    "Rápido: ¿cómo haces naranja con el LED?",
    # s07
    "Rojo al máximo, un poco de verde, azul apagado. La luz se suma: sale naranja.",
    # s08
    "Las reglas: pulsa el botón para empezar. Se enciende rojo, amarillo, verde. Al ver verde, pulsa.",
    # s09
    "El LED muestra: verde rápido, amarillo regular, rojo lento. La perilla cambia la espera del amarillo: no sirve contar.",
    # s10
    "Ningún cable nuevo: es el circuito del cruce.",
    # s11
    "El juego es otra vez la lavadora, con cinco pasos: espera, rojo, amarillo, verde y resultado.",
    # s12
    "Pausa y predice: ¿cómo mide la placa tu tiempo de reacción? Ya sabes el truco.",
    # s13
    "Es el ticket. Con el verde, goTo() anota la hora. Al pulsar, ahora menos esa hora es la reacción.",
    # s14
    "El tiempo del paso verde es tu reacción. Nada de código.",
    # s15
    "Este es el sketch reflex_game. Arriba, los mismos pines, state y hora de inicio, más best para el récord.",
    # s16
    "Helpers conocidos: setColor() el resultado, lights() los LEDs, goTo() avanzar.",
    # s17
    "Parte uno, el botón. Novedad: pressed, verdadero o falso. Solo es verdadero en la vuelta de una pulsación nueva.",
    # s18
    "Pausa y predice: botón un segundo, ¿cuántas vueltas es pressed verdadero?",
    # s19
    "Solo una. Mantener no cuenta otra vez, así cada paso pregunta: ¿pulsaron ahora?",
    # s20
    "El paso cero espera la pulsación. Se enciende el rojo.",
    # s21
    "El paso uno mantiene el rojo un segundo. Luego amarillo, y map() convierte la perilla en uno a cuatro s.",
    # s22
    "Pausa e intenta: escribe el paso dos. Acaba el amarillo, se enciende el verde y sigue el paso tres.",
    # s23
    "Una forma. Igual que el cruce: revisar el tiempo, las luces y goTo().",
    # s24
    "Paso tres, el corazón: con pressed, el tiempo del paso es tu reacción.",
    # s25
    "Luego if y else if eligen: menos de un cuarto de segundo verde, menos de medio amarillo, si no rojo.",
    # s26
    "El paso cuatro muestra el color tres segundos y vuelve al paso cero.",
    # s27
    "Aquí en vivo. Mira las luces y el color final.",
    # s28
    "Ahora una pulsación lenta, tras el verde. El LED sale rojo.",
    # s29
    "Cambia un número. Pausa y predice: si doscientos cincuenta pasa a doscientos, ¿qué pasa?",
    # s30
    "El verde cuesta más. Solo cuentan pulsaciones muy rápidas; más rondas salen amarillo.",
    # s31
    "Ahora el récord. Pausa y predice: haces un gran tiempo y reconectas la placa. ¿Sigue el récord?",
    # s32
    "Con una variable normal, no. Toda variable vive en memoria que se borra sin energía. best reinicia.",
    # s33
    "Variables: cajas sobre el escritorio; sin energía se limpia. El cuaderno del cajón queda.",
    # s34
    "En realidad: el ESP32 reserva un rincón de su memoria flash, la del programa. La biblioteca Preferences guarda números ahí.",
    # s35
    "La diferencia: el cajón es chico y se desgasta. Escribimos solo lo que vale.",
    # s36
    "En el sketch, tres líneas. En setup(), begin() abre el cajón.",
    # s37
    "getULong() lee la página best; si está vacía, da nueve nueve nueve nueve.",
    # s38
    "Rápido: ¿por qué un número tan grande?",
    # s39
    "Porque toda reacción real es menor. La primera ronda es récord.",
    # s40
    "En el paso tres: si la reacción mejora best, lo guardamos y putULong() lo escribe.",
    # s41
    "La prueba. Desconecta el cable, espera y conéctalo.",
    # s42
    "El Serial Monitor reinicia y la primera línea muestra el récord viejo.",
    # s43
    "Un error común: para guardar, alguien escribe put en cada ronda, sin el if.",
    # s44
    "Rápido: ¿qué pasa con un récord tras una ronda lenta?",
    # s45
    "Desapareció. El tiempo lento se escribió encima. El if hace el récord: solo entra uno mejor.",
    # s46
    "Pausa y explica con tus palabras por qué best solo olvida el récord y el cajón lo guarda.",
    # s47
    "Las variables viven en memoria que necesita energía. El cajón es flash, que no la necesita.",
    # s48
    "Pausa y predice: ¿qué hace el juego si pulsas en amarillo?",
    # s49
    "Nada. Un tramposo puede pulsar sin parar y atrapar el verde por suerte.",
    # s50
    "Tu turno, la salida falsa: pulsar en rojo o amarillo hace parpadear el LED rojo, sin tiempo.",
    # s51
    "Un paso y una revisión más. Solución: en la carpeta y en un Short.",
    # s52
    "Hoy terminaste tu primer proyecto. Un juego de pasos. La reacción es el tiempo de un paso. Y un récord en el cajón.",
    # s53
    "La próxima, un repaso desde el episodio cinco, con quiz. ¡Cuéntame tu mejor tiempo en los comentarios!",
]

TARGET = {"hi": 0.95, "pt": 0.95, "es": 0.95}
MEAN_TARGET = 0.75


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
