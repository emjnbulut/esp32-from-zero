"""Source of video/ep12/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, comes from make_script.py via dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says (the IP address is said digit by digit, like the English).
The same text is the subtitle for hi/pt/es (see make_subs.py: dub and subtitle must be the same sentences).
Hindi: English tech terms are written in Devanagari (no Latin letters inside Hindi lines).
Written tight like ep11 (mean <= 0.68, max <= 0.85): the voices pause at every punctuation mark, so prefer commas over full stops, few colons.
Analogies kept (video/ANALOGIES.md): phone hotspot, restaurant menu with numbered dishes, order-slip note, night guard doing rounds.
Usage: python video/ep12/make_dubs.py"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "फ़ोन पर लाल दबाता हूँ, मेज़ की बत्ती लाल।",
    # s02
    "रिंग दबाया, घंटी बजी। न ऐप, न तार, न घर का वाई-फ़ाई।",
    # s03
    "छोटी स्क्रीन हर कमांड गिनती है।",
    # s04
    "आज बोर्ड को रिमोट मिलता है, आपका फ़ोन। कोई नया पुर्ज़ा नहीं।",
    # s05
    "ईएसपी बत्तीस में वाई-फ़ाई है। ये एंटीना, टेढ़ी लकीर।",
    # s06
    "आम तौर पर डिवाइस राउटर से जुड़ता है। आज उल्टा, बोर्ड अपना नेटवर्क खोलता है, फ़ोन के हॉटस्पॉट जैसा।",
    # s07
    "फ़ोन जुड़ता है। अंदर बोर्ड का पता हमेशा एक नौ दो, एक छह आठ, चार, एक।",
    # s08
    "कोड में नेटवर्क खोलना एक लाइन, सॉफ्ट ए पी, नाम और पासवर्ड।",
    # s09
    "फिर बोर्ड छोटा वेब पेज देता है, रेस्टोरेंट के मेन्यू जैसा, हर डिश का नंबर, बटन दबाओ, फ़ोन नंबर बोलता है।",
    # s10
    "यहाँ नंबर लिंक हैं, बत्ती का स्लैश कलर, बज़र का स्लैश रिंग।",
    # s11
    "हर लिंक की एक लाइन चुनती है कौन सा हेल्पर जवाब दे। सर्वर ऑन।",
    # s12
    "लूप का एक काम, रात के पहरेदार जैसे बार-बार देखना, कोई फ़ोन दस्तक दे रहा है?",
    # s12b
    "कुछ लिंक में नोट होता है, ऑर्डर पर्ची जैसा। स्लैश कलर क्वेश्चन मार्क सी बराबर रेड, नोट रंग बताता है।",
    # s12c
    "हेल्पर नोट पढ़ता है, सर्वर आर्ग सी, और इफ़ से रंग चुनता है, एपिसोड छह जैसे।",
    # s12d
    "फिर वही पेज लौटाता है, रिमोट स्क्रीन पर रहे।",
    # s13
    "पेज स्केच में तैयार टेम्पलेट है। बस लेबल और रंग बदलिए।",
    # s14
    "सर्किट मेज़ पर है, एपिसोड छह की एल ई डी, एपिसोड दस की स्क्रीन और बज़र।",
    # s15
    "लाल, हरा, नीला पिन पच्चीस, छब्बीस, सत्ताईस पर, रेज़िस्टर के साथ।",
    # s16
    "अपलोड करें, स्क्रीन पता दिखाती है।",
    # s17
    "फ़ोन में वाई-फ़ाई खोलिए, बोर्ड के नेटवर्क से पासवर्ड से जुड़िए।",
    # s18
    "ब्राउज़र में पता लिखिए, रिमोट हाज़िर, चार रंग और रिंग।",
    # s19
    "लाल दबाइए, लिंक हवा से जाता है, हेल्पर रंग बदलता है, स्क्रीन पर कमांड एक।",
    # s19b
    "असल में फ़ोन हवा से संदेश भेजता है, बोर्ड पढ़ता है, बत्ती बदलता है, पेज लौटाता है। पलक झपकते।",
    # s19c
    "हरा, नीला, बंद। हर दबाव नया कमांड, गिनती बढ़ती है।",
    # s20
    "रिंग दबाइए, बज़र दो सुर बजाता है।",
    # s21
    "आम समस्या, फ़ोन कहता है नेटवर्क में इंटरनेट नहीं, और चुपचाप मोबाइल डेटा पर लौटता है। जुड़ा रहने दें।",
    # s22
    "पासवर्ड कम से कम आठ अक्षर, वरना नेटवर्क दिखता नहीं।",
    # s22b
    "बस नंबर लिखें, न डब्ल्यू डब्ल्यू डब्ल्यू, न एच टी टी पी एस।",
    # s23
    "आपकी बारी, पार्टी बटन, लाल, हरा, नीला तीन बार चमके। एक लिंक, एक हेल्पर।",
    # s24
    "पूरा कोड और हल लेसन फ़ोल्डर में, लिंक नीचे। फ़ोन से आप क्या चलाएँगे? कमेंट में बताइए।",
    # s25
    "अगली बार मौसम स्टेशन, तापमान और नमी स्क्रीन पर और इसी फ़ोन पेज पर। फिर मिलते हैं।",
]

PT = [
    # s01
    "Toco o vermelho, a luz da mesa fica vermelha.",
    # s02
    "Toco ring, soa a campainha. Sem app, cabo ou Wi-Fi.",
    # s03
    "A telinha conta cada comando.",
    # s04
    "Hoje a placa ganha um controle, seu celular. Sem peça nova.",
    # s05
    "O ESP32 tem Wi-Fi. A antena é esta linha em zigue-zague.",
    # s06
    "Normal é entrar no roteador. Hoje é o contrário, a placa abre sua rede, como o hotspot do celular.",
    # s07
    "O celular entra, e o endereço da placa é sempre um nove dois, um seis oito, quatro, um.",
    # s08
    "Em código, uma linha, soft A P, com nome e senha.",
    # s09
    "Ela serve uma página, como um cardápio de pratos numerados, e o toque chama o número.",
    # s10
    "Os números são links, barra color acende a luz, barra ring toca.",
    # s11
    "Uma linha por link escolhe quem responde. Server on, link, ajudante.",
    # s12
    "O loop só faz uma coisa, como o guarda noturno, ver se um celular bate à porta.",
    # s12b
    "Links levam um bilhete, como no pedido. Barra color, interrogação, c igual red, diz a cor.",
    # s12c
    "Lê o bilhete com server arg c, e escolhe a cor com ifs, como no episódio seis.",
    # s12d
    "Depois devolve a mesma página, o controle fica na tela.",
    # s13
    "A página é um modelo pronto. Você só troca rótulos e cores.",
    # s14
    "O circuito? Já está na mesa, o LED do episódio seis, a tela e o buzzer do dez.",
    # s15
    "Cores nos pinos vinte e cinco, vinte e seis e vinte e sete, com resistor.",
    # s16
    "Envie, a tela mostra o endereço.",
    # s17
    "No celular, entre no Wi-Fi da placa, com a senha.",
    # s18
    "Digite o endereço, e aparece o controle, quatro cores e ring.",
    # s19
    "Vermelho, o link viaja, o ajudante troca a cor, a tela conta comando um.",
    # s19b
    "Na verdade, o celular manda uma mensagem, a placa lê, muda a luz e devolve a página, num piscar.",
    # s19c
    "Verde, azul, apagar. Cada toque é um comando, o contador sobe.",
    # s20
    "Toque ring, o buzzer toca duas notas.",
    # s21
    "Problema comum, o celular diz rede sem internet e volta aos dados móveis. Peça para ficar.",
    # s22
    "A senha precisa de oito caracteres, ou a rede some.",
    # s22b
    "Digite só os números, sem www nem https.",
    # s23
    "Sua vez, um botão festa que pisca as cores três vezes. Um link, um ajudante.",
    # s24
    "Código e solução na pasta, link abaixo. O que você controlaria pelo celular? Comente.",
    # s25
    "Próximo, estação do tempo, temperatura e umidade, na tela e no celular. Até lá!",
]

ES = [
    # s01
    "Toco rojo, y la luz de la mesa se pone roja.",
    # s02
    "Toco ring, suena el timbre. Sin app, cable ni Wi-Fi.",
    # s03
    "La pantallita cuenta cada comando.",
    # s04
    "Hoy la placa tiene control, tu celular. Sin piezas nuevas.",
    # s05
    "El ESP32 trae Wi-Fi. La antena es esta línea en zigzag.",
    # s06
    "Lo normal es entrar al router. Hoy la placa abre su propia red, como el hotspot del celular.",
    # s07
    "El celular entra, y su dirección es siempre uno nueve dos, uno seis ocho, cuatro, uno.",
    # s08
    "En código, una línea, soft A P, con nombre y contraseña.",
    # s09
    "La placa sirve una página, como un menú de platos numerados, y tocar un botón pide el número.",
    # s10
    "Los números son enlaces, barra color enciende, barra ring suena.",
    # s11
    "Cada enlace tiene una línea que elige quién responde. Server on.",
    # s12
    "El loop hace una cosa, como el guardia nocturno, ver si un celular toca.",
    # s12b
    "Un enlace lleva nota, como un pedido. Barra color, interrogación, c igual red, dice el color.",
    # s12c
    "Lo lee con server arg c y elige el color con if, como en el episodio seis.",
    # s12d
    "Luego devuelve la misma página, y el control sigue ahí.",
    # s13
    "La página es una plantilla lista. Solo cambias etiquetas y colores.",
    # s14
    "El circuito ya está en tu mesa, LED del seis, pantalla y zumbador del diez.",
    # s15
    "Rojo, verde y azul, pines veinticinco, veintiséis y veintisiete, con resistencia.",
    # s16
    "Sube, y la pantalla da la dirección.",
    # s17
    "Entra al Wi-Fi de la placa con su contraseña.",
    # s18
    "Escribe la dirección, y sale el control, cuatro colores y ring.",
    # s19
    "Toca rojo, viaja el enlace, cambia el color, y la pantalla cuenta uno.",
    # s19b
    "En realidad, el celular manda un mensaje, la placa lo lee, cambia la luz y devuelve la página.",
    # s19c
    "Verde, azul, apagar. Cada toque es un comando, el contador sube.",
    # s20
    "Toca ring, y el zumbador suena dos notas.",
    # s21
    "Problema común, el celular avisa sin internet y vuelve a datos móviles. Dile que se quede.",
    # s22
    "La contraseña necesita ocho caracteres, o no hay red.",
    # s22b
    "Escribe solo los números, sin www ni https.",
    # s23
    "Tu turno, botón fiesta que parpadee los tres colores. Un enlace, un ayudante.",
    # s24
    "Código y solución en la carpeta, abajo. ¿Qué controlarías con tu celular? Cuéntame.",
    # s25
    "La próxima, estación del clima, en la pantalla y en esta página. ¡Nos vemos!",
]

# Lines shortened after the narrated fit report (dub.py --report): the voice reads slower than the char ratio suggests
# (pauses at punctuation), and the picture must not stretch (3D is rendered). Empty until ep12 is narrated.
PT_FIT = {
    "s01": "Toco no vermelho, a luz fica vermelha.",
    "s02": "Toco ring, toca a campainha. Sem app, sem cabo.",
    "s04": "Hoje o celular vira controle, sem peça nova.",
    "s06": "Normalmente ela entra no roteador. Hoje a placa abre sua rede, como um hotspot.",
}
ES_FIT = {
    "s01": "Toco rojo y la luz se pone roja.",
    "s03": "La pantalla cuenta los comandos.",
    "s12b": "Un enlace lleva una nota, como un pedido: color, interrogación, c igual red.",
    "s12d": "Luego devuelve la página, y el control sigue ahí.",
    "s17": "Entra al Wi-Fi de la placa con la clave.",
    "s18": "Escribe la dirección y sale el control, con cuatro colores y ring.",
}
HI_FIT = {}
FIT = {"hi": HI_FIT, "pt": PT_FIT, "es": ES_FIT}

TARGET = {"hi": 0.85, "pt": 0.85, "es": 0.85}
MEAN_TARGET = 0.68


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
