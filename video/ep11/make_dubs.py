"""Source of video/ep11/dub/{hi,pt,es}.json (the Turkish dub, spelled phonetically, comes from make_script.py via dub/tr.json).
Numbers are spelled out in words so the length check below measures what the voice really says.
The same text is the subtitle for hi/pt/es (see make_subs.py: dub and subtitle must be the same sentences).
Hindi: English tech terms are written in Devanagari (no Latin letters inside Hindi lines).
Ep11 is written tighter than ep10 (mean <= 0.68, max <= 0.85): in ep10 even ratio 0.75 ran 10-30 % long when narrated,
because the voices pause at every punctuation mark. Prefer commas over full stops, few colons.
Usage: python video/ep11/make_dubs.py"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
IDS = [s["id"] for s in json.loads((ROOT / "script.json").read_text(encoding="utf-8"))["segments"]]

HI = [
    # s01
    "मेज़ पर पहरेदार है। चालू करता हूँ, दस सेकंड हैं।",
    # s02
    "हाथ बिस्कुट के डिब्बे की ओर... फ़ौरन पकड़ा गया!",
    # s03
    "लौटता हूँ, तो ये बताता है कब हुआ: दो मिनट पहले।",
    # s04
    "आज ये अलार्म बनाते हैं, एक नया पुर्ज़ा, बाकी पिछला सर्किट।",
    # s05
    "ये सफ़ेद गुंबद मोशन सेंसर है, बस गर्मी देखता है।",
    # s06
    "गर्म चीज़ें इन्फ़्रारेड में चमकती हैं, हाथ, बिल्ली, चाय। सेंसर देखता है, हम नहीं।",
    # s07
    "गुंबद खिड़कियों वाला लेंस है, हर खिड़की कमरे का एक हिस्सा देखती है, टॉर्चों जैसी।",
    # s08
    "गर्मी एक खिड़की से दूसरी में गई, तो सेंसर जवाब वाला पिन चालू करता है।",
    # s09
    "कोड के लिए ये बस अंगूठा है, हलचल हुई तो ऊपर, नहीं तो नीचे।",
    # s10
    "दो नारंगी घुंडियाँ हैं, हाँ कितनी देर रहे, और कितनी दूर तक देखे।",
    # s11
    "सुझाव, चालू करके तीस सेकंड गरम होने दें, तब तक बेवजह हाँ कह सकता है।",
    # s12
    "जोड़ते हैं। स्क्रीन, बटन और बज़र वहीं रहेंगे।",
    # s13
    "सेंसर के तीन पैर। लाल तार वी-इन पिन से पाँच वोल्ट लाता है, काला ग्राउंड पर।",
    # s14
    "बीच का पैर जवाब, बैंगनी तार पिन तैंतीस पर।",
    # s15
    "चिंता नहीं, जवाब तीन पॉइंट तीन वोल्ट का है, सुरक्षित।",
    # s16
    "पिन तैंतीस पर डिजिटल रीड, हाई यानी हलचल।",
    # s17
    "चरण, वॉशिंग मशीन जैसे, बंद, निकलना, तैयार, अलार्म।",
    # s18
    "बटन दबाइए, उलटी गिनती शुरू, हर सेकंड हल्की टिक, ताकि बाहर निकल सकें।",
    # s19
    "शून्य पर पहरेदार तैयार, अब बस सेंसर के हाँ का इंतज़ार।",
    # s20
    "हाँ आते ही सायरन बजता है, दो सुर, एक सेकंड में चार बार बदलते।",
    # s21
    "रोकने के लिए बटन दबाएँ, या पंद्रह सेकंड में ख़ुद चुप, पड़ोसी खुश रहें।",
    # s22
    "चतुर हिस्सा, हलचल के पल समय की मुहर, एपिसोड नौ के पार्किंग टिकट जैसे।",
    # s23
    "लास्ट मोशन बराबर मिलिस, मिलिस बोर्ड की स्टॉपवॉच है।",
    # s24
    "नाउ घटा लास्ट मोशन, कितना पहले, साठ हज़ार से भाग दें, मिनट।",
    # s25
    "स्क्रीन कहे, दो बार देखा, तीन मिनट पहले।",
    # s26
    "एक सवाल, किट में लगभग वैसा ही दूसरा बज़र है, फ़र्क़ क्या?",
    # s27
    "हमारा पैसिव है, छोटा स्पीकर, जो भेजा सुर बजाता है। एक्टिव संगीत-डिब्बा है, बिजली दो, तो एक तय बीप।",
    # s28
    "आसान, पर सायरन नहीं, इसलिए पैसिव।",
    # s29
    "परखें, चालू किया, गिनती चली, मैं बाहर।",
    # s30
    "हाथ डिब्बे की ओर... पकड़ा गया!",
    # s31
    "बटन दबाता हूँ, एक बार देखा, बारह सेकंड पहले।",
    # s32
    "आम समस्या, चालू करते ही अलार्म बजे, अक्सर सेंसर गरम हो रहा होता है, या टाइम घुंडी हाँ लंबा रखती है।",
    # s33
    "तीस सेकंड रुकें और टाइम घुंडी पूरी घटा दें, बाकी कोड करेगा।",
    # s34
    "आपकी बारी, प्रेफ़रेंसेज़ से गिनती बिजली जाने पर भी बचाइए।",
    # s35
    "पूरा कोड और हल लेसन फ़ोल्डर में, लिंक नीचे। आप इससे क्या बचाएँगे? कमेंट में बताइए।",
    # s36
    "अगली बार बोर्ड फ़ोन से चलेगा, बिना ऐप, बिना राउटर। फिर मिलते हैं।",
]

PT = [
    # s01
    "Minha mesa tem guarda. Armo e tenho dez segundos.",
    # s02
    "Uma mão vai ao pote de biscoitos... e é flagrada na hora.",
    # s03
    "Volto, e ele diz quando foi: dois minutos atrás.",
    # s04
    "Hoje montamos este alarme, uma peça nova, o resto já temos.",
    # s05
    "Esta cúpula é um sensor de movimento, só observa o calor.",
    # s06
    "Tudo quente brilha em infravermelho, mão, gato, chá. Só o sensor vê.",
    # s07
    "A cúpula é uma lente de janelinhas, cada uma vê uma fatia, como lanternas.",
    # s08
    "Calor passando de janela em janela, o sensor percebe e liga o pino.",
    # s09
    "Pro código, é um joinha, para cima se mexeu, para baixo se não.",
    # s10
    "Dois botões laranja ajustam quanto dura o sim, e o alcance.",
    # s11
    "Dica, espere uns trinta segundos após ligar, ele ainda esquenta.",
    # s12
    "Vamos ligar. Tela, botão e buzzer ficam onde estavam.",
    # s13
    "Três pernas. Fio vermelho, cinco volts do pino V-in, preto no terra.",
    # s14
    "Perna do meio, fio roxo ao pino trinta e três.",
    # s15
    "Sem medo, sai três vírgula três volts, é seguro.",
    # s16
    "Ler, digital read no pino trinta e três. High é movimento.",
    # s17
    "Passos, como a máquina de lavar, desligado, saindo, armado, alarme.",
    # s18
    "Aperte o botão, contagem com um tique por segundo, para você sair.",
    # s19
    "No zero, armado. Só espera o sensor dizer sim.",
    # s20
    "Aí a sirene toca, duas notas, quatro vezes por segundo.",
    # s21
    "Botão para parar, ou para sozinha em quinze segundos, pelos vizinhos.",
    # s22
    "A parte esperta, ao detectar, carimbamos a hora, como o ticket do episódio nove.",
    # s23
    "Uma linha, last motion igual a millis, o cronômetro da placa.",
    # s24
    "Depois, now menos last motion é o tempo. Divida por sessenta mil, minutos.",
    # s25
    "A tela diz, visto duas vezes, há três minutos.",
    # s26
    "Seu kit tem outro buzzer quase igual. Qual a diferença?",
    # s27
    "Passivo, um alto-falantezinho que toca a nota enviada. Ativo, uma caixinha de música, liga e toca um bipe só.",
    # s28
    "Mais fácil, mas sem sirene. Por isso o passivo.",
    # s29
    "Vamos testar, armo, a contagem corre e saio da sala.",
    # s30
    "Uma mão vai ao pote... flagrada!",
    # s31
    "Volto, aperto, visto uma vez, há doze segundos.",
    # s32
    "Problema comum, toca logo ao armar. O sensor ainda esquenta, ou o botão de tempo está alto.",
    # s33
    "Espere trinta segundos e baixe o botão de tempo. O resto é o código.",
    # s34
    "Sua vez, guarde as capturas com Preferences, mesmo sem energia.",
    # s35
    "Código e solução na pasta, abaixo. O que você vigiaria? Comente.",
    # s36
    "Próximo, controle a placa pelo celular, sem app nem roteador. Até lá!",
]

ES = [
    # s01
    "Mi mesa tiene guardia. Armo y tengo diez segundos.",
    # s02
    "Una mano va al frasco de galletas... ¡atrapada!",
    # s03
    "Al volver, dice cuándo fue: hace dos minutos.",
    # s04
    "Hoy armamos esta alarma, una pieza nueva y el resto igual.",
    # s05
    "Esta cúpula es un sensor de movimiento, solo vigila el calor.",
    # s06
    "Lo caliente brilla en infrarrojo, mano, gato, té. Solo el sensor lo ve.",
    # s07
    "La cúpula es un lente de ventanitas, cada una ve un trozo, como linternas.",
    # s08
    "Calor que pasa de ventana a ventana, el sensor lo nota y activa el pin.",
    # s09
    "Para el código, es un pulgar arriba si algo se movió, abajo si no.",
    # s10
    "Dos perillas naranja, cuánto dura el sí, y qué tan lejos ve.",
    # s11
    "Tip, espera unos treinta segundos tras encender, aún se calienta.",
    # s12
    "Conectemos. Pantalla, botón y zumbador no se mueven.",
    # s13
    "Tres patas. Cable rojo, cinco voltios del pin V-in, negro a tierra.",
    # s14
    "Pata del medio, cable morado al pin treinta y tres.",
    # s15
    "Tranquilo, salen tres coma tres voltios, es seguro.",
    # s16
    "Leer, digital read en el pin treinta y tres. High, movimiento.",
    # s17
    "Pasos, como la lavadora, apagado, saliendo, armado, alarma.",
    # s18
    "Pulsa el botón, cuenta atrás con un tic por segundo, para salir.",
    # s19
    "En cero, armado. Solo espera que el sensor diga sí.",
    # s20
    "Entonces suena la sirena, dos notas, cuatro veces por segundo.",
    # s21
    "Botón para parar, o calla sola a los quince segundos.",
    # s22
    "Lo astuto, al detectar, sellamos la hora, como el ticket del episodio nueve.",
    # s23
    "Una línea, last motion igual a millis, el cronómetro.",
    # s24
    "Luego now menos last motion da el tiempo, entre sesenta mil, minutos.",
    # s25
    "Pantalla, visto dos veces, hace tres minutos.",
    # s26
    "Tu kit trae otro zumbador casi igual. ¿Qué cambia?",
    # s27
    "Pasivo, un parlantito que toca la nota enviada. Activo, caja de música, enciendes y suena un pitido fijo.",
    # s28
    "Más fácil, pero sin sirena. Por eso, el pasivo.",
    # s29
    "Probemos, armo, corre la cuenta y salgo del cuarto.",
    # s30
    "Una mano va al frasco... ¡atrapada!",
    # s31
    "Vuelvo y pulso, visto una vez, hace doce segundos.",
    # s32
    "Problema común, suena apenas armas. El sensor aún calienta, o la perilla de tiempo está alta.",
    # s33
    "Espera treinta segundos y baja la perilla. El código hace el resto.",
    # s34
    "Tu turno, guarda las capturas con Preferences, aunque desconectes.",
    # s35
    "Código y solución en la carpeta, abajo. ¿Qué vigilarías? Cuéntame.",
    # s36
    "La próxima, la placa desde tu celular, sin app ni router. ¡Nos vemos!",
]

# Lines shortened after the narrated fit report (dub.py --report): the voice reads slower than the char ratio suggests
# (pauses at punctuation), and the picture must not stretch (3D is rendered). Empty until ep11 is narrated.
PT_FIT = {
    "s25": "Na tela: visto duas vezes, há três minutos.",
    "s34": "Sua vez: guarde as capturas com Preferences.",
}
ES_FIT = {
    "s31": "Pulso: visto una vez, hace doce segundos.",
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
