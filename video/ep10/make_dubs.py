"""Source of video/ep10/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, comes from make_script.py via dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
The same text is the subtitle for hi/pt/es (see make_subs.py: dub and subtitle must be the same sentences).
Hindi: English tech terms are written in Devanagari (no Latin letters inside Hindi lines).
Usage: python video/ep10/make_dubs.py"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "रुकिए... गो! दो सौ चौदह मिलीसेकंड। नया रिकॉर्ड।",
    # s02
    "अब देखिए। केबल खींचता हूँ। स्क्रीन बुझी, बोर्ड बंद।",
    # s03
    "वापस लगाया... और रिकॉर्ड वहीं है। बिना बिजली बोर्ड को याद रहा।",
    # s04
    "आज ये खेल शुरू से बनाएँगे: असली स्क्रीन, असली बीप, और कभी न भूलने वाला रिकॉर्ड। बस किट और बीस मिनट।",
    # s05
    "पहला नया पुर्ज़ा: एक इंच से छोटी स्क्रीन।",
    # s06
    "इसमें आठ हज़ार बिंदु हैं, हर बिंदु की अपनी रोशनी। इसलिए काला सचमुच काला है: बिंदु बस बंद हैं।",
    # s07
    "और बस चार तार चाहिए। दो बिजली के, दो पूरी तस्वीर के।",
    # s08
    "ये दो तार ग्रुप चैट जैसे हैं। एक तार संदेश टुकड़ों में ले जाता है। दूसरा ताल देता है, ताकि दोनों साथ पढ़ें।",
    # s09
    "चैट में हर डिवाइस का छोटा नाम होता है, पता। स्क्रीन अपने पते पर बोलती है, तो इन्हीं तारों पर और पुर्ज़े जुड़ेंगे।",
    # s10
    "दूसरा पुर्ज़ा ये बज़र। ये पैसिव है: सुर दें, तभी बोलेगा।",
    # s11
    "अंदर एक पतली धातु की प्लेट मुड़ती है। तेज़ तो ऊँची बीप, धीमी तो भारी भनभन।",
    # s12
    "पुराना साथी बटन भी है। बस पिन बदलता है, स्क्रीन को उसकी जगह चाहिए।",
    # s13
    "अब जोड़ें। हर छेद पर नंबर और अक्षर छपा है, स्क्रीन पर भी दिखेगा। बस नकल कीजिए।",
    # s14
    "पहले बिजली। लाल तार तीन पॉइंट तीन वोल्ट पीछे की प्लस लाइन पर, काला तार ग्राउंड माइनस लाइन पर।",
    # s15
    "अब स्क्रीन। चारों पैर एक कॉलम में। दो छोटे तार लाइनों से बिजली देते हैं।",
    # s16
    "चैट के दो तार: हरा पिन बाईस से क्लॉक पैर, नीला पिन इक्कीस से डेटा पैर।",
    # s17
    "बटन बीच की खाई पर। पीला पिन उन्नीस से एक तरफ़, दूसरी तरफ़ ग्राउंड।",
    # s18
    "आख़िर में बज़र। नारंगी तार पिन बत्तीस से प्लस पैर तक, दूसरा पैर ग्राउंड।",
    # s19
    "बस यही पूरा सर्किट: स्क्रीन, बटन, बज़र। अपने से मिलाने के लिए रोकिए।",
    # s20
    "स्क्रीन से बात के लिए मुफ़्त लाइब्रेरी। मैनेजर से एक बार इंस्टॉल करें।",
    # s21
    "तरकीब ये: प्रिंट करने पर कुछ नहीं दिखता। बोर्ड परदे के पीछे व्हाइटबोर्ड पर बनाता है।",
    # s22
    "डिस्प्ले बुलाते ही परदा खुलता है, पूरी तस्वीर साथ दिखती है। न झिलमिल, न अधूरे शब्द।",
    # s23
    "इसलिए एक छोटा सहायक, शो। बोर्ड साफ़, ऊपर छोटी पंक्ति, बीच में बड़ी, फिर परदा खुलता है।",
    # s24
    "एक कॉल, और स्क्रीन लिख देती है।",
    # s25
    "खेल के चार कदम हैं, वॉशिंग मशीन जैसे: तैयार, इंतज़ार, गो, और नतीजा।",
    # s26
    "दबाते ही बेतरतीब इंतज़ार चुनते हैं, डेढ़ से चार सेकंड, ताकि कोई पल न भाँप सके।",
    # s27
    "समय पूरा होते ही स्क्रीन पर गो आता है और बज़र बजता है। अब घड़ी चल पड़ी।",
    # s28
    "बीप एक पंक्ति है: टोन, पिन, सुर कितना ऊँचा, और कितनी देर।",
    # s29
    "आपका दबाव घड़ी रोकता है। गो के बाद का समय आपकी प्रतिक्रिया है, स्क्रीन पर।",
    # s30
    "और जल्दी दबाया? ग़लत शुरुआत। भारी भनभन, फिर कोशिश।",
    # s31
    "कुछ राउंड खेलें। तीन सौ पचास... ठीक। दो सौ अस्सी... बेहतर।",
    # s32
    "अब सबसे बढ़िया बात। हर वेरिएबल उस मेमोरी में रहता है जो बिजली जाते ही सब भूल जाती है। जैसे मेज़ की पर्चियाँ, जो हर रात झाड़ दी जाएँ।",
    # s33
    "पर ई-एस-पी बत्तीस में एक दराज़ है, जो बिना बिजली रखती है। प्रेफ़रेंसेज़।",
    # s34
    "रिकॉर्ड टूटे तो एक पंक्ति नया समय दराज़ में रखती है, लेबल: बेस्ट।",
    # s35
    "चालू होते ही एक पंक्ति उसे निकाल लेती है। दराज़ खाली हो, तो बहुत बड़ी संख्या मिलती है, तो पहला राउंड हमेशा रिकॉर्ड।",
    # s36
    "परखें। दो सौ चौदह, नया रिकॉर्ड। निकालिए... वापस लगाइए... अब भी दो सौ चौदह।",
    # s37
    "सुझाव: सिर्फ़ नया रिकॉर्ड बनने पर सेव कीजिए। हर राउंड सेव हुआ, तो धीमा समय बेस्ट मिटा देगा, और दराज़ जल्दी घिसेगी।",
    # s38
    "आपकी बारी। तैयार स्क्रीन पर बटन तीन सेकंड दबाने से रिकॉर्ड मिटे। लंबा दबाव नापना आप जानते हैं।",
    # s39
    "पूरा कोड और हल लेसन फ़ोल्डर में है, लिंक नीचे। अपना बेस्ट टाइम कमेंट में लिखिए।",
    # s40
    "अगली बार बोर्ड को आँखें मिलेंगी: मोशन सेंसर, जो इसे अलार्म बना देगा। सब्सक्राइब कीजिए। फिर मिलते हैं!",
]

PT = [
    # s01
    "Espere... JÁ! Duzentos e catorze milissegundos. Recorde!",
    # s02
    "Olha só. Puxo o cabo. A tela apaga, a placa está desligada.",
    # s03
    "Ligo de novo... e o recorde continua lá. A placa lembrou, sem energia.",
    # s04
    "Hoje montamos este jogo do zero: tela, bipe e um recorde que não esquece. Só o kit e vinte minutos.",
    # s05
    "A primeira peça: uma telinha minúscula.",
    # s06
    "Tem oito mil pontinhos, cada um com luz própria. Por isso o preto é preto de verdade: ponto apagado.",
    # s07
    "Só quatro fios: dois de energia, dois para as imagens.",
    # s08
    "Os dois fios são um grupo de conversa. Um leva a mensagem, bit a bit. O outro marca o ritmo.",
    # s09
    "Cada aparelho tem um nome curto, o endereço. A tela responde ao dela, e cabem mais peças nos mesmos fios.",
    # s10
    "A segunda peça é este buzzer passivo. Fica mudo até a gente dar uma nota.",
    # s11
    "Dentro, um disco vibra. Rápido, bipe agudo. Devagar, zumbido grave.",
    # s12
    "O velho botão volta. Só muda de pino, porque a tela usa o antigo.",
    # s13
    "Vamos ligar. Cada furo tem número e letra, e eles aparecem na tela. É só copiar.",
    # s14
    "Primeiro, energia. Fio vermelho: três vírgula três volts no positivo. Fio preto: terra no negativo.",
    # s15
    "Agora a tela. Quatro pernas na mesma coluna. Dois fios curtos dão energia a ela.",
    # s16
    "Verde: pino vinte e dois, ao relógio. Azul: pino vinte e um, aos dados.",
    # s17
    "O botão cruza o vão do meio. Amarelo do pino dezenove a um lado, o outro no terra.",
    # s18
    "Por fim, o buzzer. Laranja: pino trinta e dois ao positivo. Outra perna no terra.",
    # s19
    "Esse é o circuito todo: tela, botão e buzzer. Pause e compare com o seu.",
    # s20
    "Para falar com a tela, uma biblioteca grátis. Instale pelo Gerenciador.",
    # s21
    "O truque: ao imprimir, nada aparece. A placa desenha num quadro atrás de uma cortina.",
    # s22
    "Só com display a cortina abre e tudo aparece junto. Sem piscar.",
    # s23
    "Então criamos um ajudante, show. Limpa o quadro, escreve uma linha pequena, uma grande, e abre a cortina.",
    # s24
    "Uma chamada, e a tela escreve.",
    # s25
    "Quatro passos, como numa máquina de lavar: pronto, espera, já, resultado.",
    # s26
    "Ao apertar, sorteamos uma espera de um e meio a quatro segundos. Ninguém adivinha o momento.",
    # s27
    "Acabou a espera: a tela mostra GO e o buzzer apita. Aí o relógio corre.",
    # s28
    "O bipe é uma linha: tone, com o pino, a nota e a duração.",
    # s29
    "Seu aperto para o relógio. O tempo desde o GO é sua reação, direto na tela.",
    # s30
    "Apertou cedo? Largada falsa. Zumbido grave, e tenta de novo.",
    # s31
    "Vamos jogar. Trezentos e cinquenta... ok. Duzentos e oitenta... melhor.",
    # s32
    "A melhor parte. Toda variável vive numa memória que esquece tudo sem energia. Como post-its na mesa, varridos toda noite.",
    # s33
    "Mas o ESP32 tem uma gaveta que guarda sem energia. Chama-se Preferences.",
    # s34
    "Recorde? Uma linha guarda o tempo na gaveta, etiqueta best.",
    # s35
    "Ao ligar, outra linha tira o valor de volta. Gaveta vazia dá um número enorme, e a primeira rodada sempre é recorde.",
    # s36
    "Prova: duzentos e catorze, recorde. Desligo... ligo... ainda duzentos e catorze.",
    # s37
    "Dica: salve só com recorde novo. Salvar toda rodada trocaria seu melhor por um tempo lento, e gasta a gaveta.",
    # s38
    "Sua vez. Segure o botão três segundos na tela inicial para apagar o recorde. Você já sabe medir toque longo.",
    # s39
    "Código e solução na pasta da lição, abaixo. Poste seu melhor tempo nos comentários.",
    # s40
    "No próximo, a placa ganha olhos: um sensor de movimento que vira alarme. Inscreva-se. Até lá!",
]

ES = [
    # s01
    "Espera... ¡YA! Doscientos catorce milisegundos. ¡Récord!",
    # s02
    "Mira. Saco el cable. La pantalla se apaga, la placa también.",
    # s03
    "Lo conecto... y el récord sigue ahí. La placa lo recordó sin corriente.",
    # s04
    "Hoy armamos este juego desde cero: pantalla, pitido y un récord que no olvida. Solo el kit y veinte minutos.",
    # s05
    "La primera pieza: una pantallita diminuta.",
    # s06
    "Tiene ocho mil puntitos con luz propia. Por eso el negro es negro de verdad: puntos apagados.",
    # s07
    "Solo cuatro cables: dos de energía, dos para las imágenes.",
    # s08
    "Los dos cables son un chat grupal. Uno lleva el mensaje, bit a bit. El otro marca el ritmo.",
    # s09
    "Cada aparato tiene un nombre corto, su dirección. La pantalla responde a la suya, y caben más piezas.",
    # s10
    "La segunda pieza es este zumbador pasivo. Calla hasta que le damos una nota.",
    # s11
    "Adentro, un disco vibra. Rápido, pitido agudo. Lento, zumbido grave.",
    # s12
    "Vuelve el botón. Solo cambia de pin, porque la pantalla usa el suyo.",
    # s13
    "Vamos a conectar. Cada hueco tiene número y letra, y salen en pantalla. Solo copia.",
    # s14
    "Primero, energía. Cable rojo: tres coma tres voltios al positivo. Cable negro: tierra al negativo.",
    # s15
    "Ahora la pantalla. Sus cuatro patas en una columna. Dos cables cortos le dan energía.",
    # s16
    "Cables del chat: verde, pin veintidós, al reloj. Azul, pin veintiuno, a los datos.",
    # s17
    "El botón cruza el hueco. Amarillo, pin diecinueve, a un lado; el otro a tierra.",
    # s18
    "Al final, el zumbador. Naranja, pin treinta y dos, al positivo. Otra pata a tierra.",
    # s19
    "Ese es todo el circuito: pantalla, botón y zumbador. Pausa y compáralo con el tuyo.",
    # s20
    "Para hablar con la pantalla, una biblioteca gratis. Instálala desde el Gestor.",
    # s21
    "El truco: al imprimir no aparece nada. La placa dibuja en una pizarra tras una cortina.",
    # s22
    "Solo con display se abre la cortina y todo aparece junto. Sin parpadeos.",
    # s23
    "Por eso hacemos un ayudante, show. Borra la pizarra, escribe una línea chica y una grande, y abre la cortina.",
    # s24
    "Una llamada, y la pantalla escribe.",
    # s25
    "Cuatro pasos, como una lavadora: listo, espera, ya, resultado.",
    # s26
    "Al pulsar, sorteamos una espera de uno y medio a cuatro segundos. Nadie adivina el momento.",
    # s27
    "Se acaba la espera: la pantalla dice GO y suena el zumbador. El reloj corre.",
    # s28
    "El pitido es una línea: tone, con el pin, la nota y su duración.",
    # s29
    "Pulsas y el reloj se detiene. El tiempo desde GO es tu reacción.",
    # s30
    "¿Pulsas antes? Salida falsa. Zumbido grave, y reintentas.",
    # s31
    "Juguemos. Trescientos cincuenta... bien. Doscientos ochenta... mejor.",
    # s32
    "Ahora lo mejor. Toda variable vive en una memoria que olvida todo sin corriente. Como notas adhesivas barridas cada noche.",
    # s33
    "Pero el ESP32 tiene un cajón que guarda sin corriente: Preferences.",
    # s34
    "¿Récord? Una línea guarda el tiempo en el cajón, etiqueta best.",
    # s35
    "Al arrancar, otra línea lo saca. Cajón vacío da un número enorme, y la primera ronda siempre es récord.",
    # s36
    "Prueba: doscientos catorce, récord. Desconecto... conecto... sigue en doscientos catorce.",
    # s37
    "Consejo: guarda solo con récord nuevo. Guardar cada ronda cambiaría tu mejor tiempo por uno lento, y gasta el cajón.",
    # s38
    "Tu turno. Mantén el botón tres segundos en la pantalla inicial para borrar el récord. Ya sabes medir pulsaciones largas.",
    # s39
    "Código y solución en la carpeta de la lección, abajo. Publica tu mejor tiempo en los comentarios.",
    # s40
    "La próxima, la placa tendrá ojos: un sensor de movimiento, y será alarma. Suscríbete. ¡Nos vemos!",
]

# Lines shortened after the narrated fit report (2026-11-25, dub.py --report after cbx_retake): the voice reads slower
# than the char ratio suggests (pauses at punctuation), and the picture must not stretch (3D is rendered).
PT_FIT = {
    "s06": "Oito mil pontinhos, cada um com luz própria. Por isso o preto é preto de verdade.",
    "s10": "A segunda peça é este buzzer passivo. Fica mudo até ganhar uma nota.",
    "s13": "Vamos ligar. Cada furo tem número e letra na tela. É só copiar.",
    "s14": "Primeiro, energia. Vermelho: três vírgula três volts no positivo. Preto: terra.",
    "s15": "Agora a tela: quatro pernas numa coluna, e dois fios curtos de energia.",
    "s17": "O botão cruza o vão. Amarelo do pino dezenove a um lado, o outro no terra.",
    "s18": "Por fim, o buzzer. Laranja do pino trinta e dois ao positivo, a outra perna no terra.",
    "s23": "Então criamos o ajudante show: limpa, escreve uma linha pequena e uma grande, e abre a cortina.",
    "s37": "Dica: salve só com recorde novo. Salvar toda rodada estraga o recorde e gasta a gaveta.",
    "s39": "Código e solução na pasta da lição, abaixo. Poste seu tempo nos comentários.",
}
ES_FIT = {}
FIT = {"pt": PT_FIT, "es": ES_FIT}

TARGET = {"hi": 0.95, "pt": 0.95, "es": 0.95}
MEAN_TARGET = 0.75


def check(langs, english):
    """Print per-language max/mean char ratio vs the English narration; return the failures."""
    over = []
    for lang, seg in langs.items():
        ratios = {k: len(seg[k]) / len(english[k]) for k in english}
        worst = max(ratios, key=ratios.get)
        mean = sum(ratios.values()) / len(ratios)
        print(f"{lang}: max {ratios[worst]:.2f} ({worst}), mean {mean:.2f}, target max <= {TARGET[lang]:.2f}, mean <= {MEAN_TARGET:.2f}")
        if mean > MEAN_TARGET:
            print(f"  OVER {lang} mean {mean:.2f}")
            over.append((lang, "mean", mean))
        for k, r in ratios.items():
            if r > TARGET[lang] + 1e-9:
                print(f"  OVER {lang} {k}: {r:.2f} ({len(seg[k])} vs {len(english[k])} chars)")
                over.append((lang, k, r))
        if lang == "hi":
            for k, v in seg.items():
                if re.search(r"[A-Za-z]", v):
                    print(f"  LATIN letters in hi {k}")
                    over.append((lang, k, 0))
        for k, v in seg.items():
            if re.search(r"\d", v.replace("ESP32", "")):
                print(f"  DIGITS in {lang} {k}")
                over.append((lang, k, 0))
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
        seg.update(FIT.get(lang, {}))  # lines shortened after the narrated fit report
        langs[lang] = seg
        (out / f"{lang}.json").write_text(json.dumps({"voice": voice, "rate": "+0%", "segments": seg}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("dubs written:", ", ".join(langs))
    over = check(langs, english)
    if over:
        raise SystemExit(f"{len(over)} length check failure(s)")
