"""YouTube metadata for Episode 5 (PWM only).
Run after the final five-language schedule: python video/ep05/make_localize.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bumpers

CHAPTERS = ["s01", "s04", "s09", "s15", "s19", "s23", "s29", "s32", "s39", "s43", "s53"]
REPO = "https://github.com/emjnbulut/esp32-from-zero"
LESSON = REPO + "/tree/main/lessons/05-pwm"
LAB = "https://emjnbulut.github.io/esp32-learning-lab/"
CREDIT = ('Music: "Lobby Time" by Kevin MacLeod (incompetech.com), CC BY 4.0: '
          'https://creativecommons.org/licenses/by/4.0/\n'
          'Narration: Chatterbox TTS (Resemble AI, MIT), with the creator\'s own voice. '
          'Accent references: LibriVox (public domain) and Google FLEURS (CC BY 4.0).')
# Local files do not prove that any dub has been published.
TEXT = json.loads("{\"en\":[\"ESP32 PWM: Make an LED Breathe with analogWrite() and millis() | From Zero #5\",\"Make an LED fade smoothly and pause it instantly with a button. Learn PWM, duty cycle, analogWrite(), average voltage and a fade that uses millis() without missing a press.\",[\"A breathing LED\",\"Two questions to remember\",\"PWM: only on or off\",\"Duty cycle\",\"analogWrite(): 0 to 255\",\"Code tour: pwm_levels\",\"Check with a multimeter\",\"The fade that misses the button\",\"The clock-based fix\",\"Code tour: fade_millis and result\",\"Explain, recap and next lesson\"]],\"tr\":[\"ESP32 PWM: analogWrite() ve millis() ile Nefes Alan LED | From Zero #5\",\"LED'i yumuşakça parlatıp kısın ve bir butonla anında durdurun. PWM, görev döngüsü, analogWrite(), ortalama gerilim ve buton basışlarını kaçırmayan millis() tabanlı geçişi öğrenin.\",[\"Nefes alan LED\",\"Hatırlamak için iki soru\",\"PWM: yalnızca açık veya kapalı\",\"Görev döngüsü\",\"analogWrite(): 0 ile 255\",\"Kod turu: pwm_levels\",\"Multimetreyle kontrol\",\"Butonu kaçıran geçiş\",\"Saate bakan çözüm\",\"Kod turu: fade_millis ve sonuç\",\"Açıklama, özet ve sonraki ders\"]],\"hi\":[\"ESP32 PWM: analogWrite() और millis() से LED को धीरे जलाएँ-बुझाएँ | From Zero #5\",\"LED की रोशनी को धीरे बढ़ाएँ और घटाएँ, फिर बटन से तुरंत रोकें। PWM, duty cycle, analogWrite(), औसत voltage और बटन का दबना तुरंत पहचानने वाला millis() आधारित fade समझें।\",[\"धीरे जलती-बुझती LED\",\"याद करने के लिए दो सवाल\",\"PWM: सिर्फ चालू या बंद\",\"Duty cycle\",\"analogWrite(): 0 से 255\",\"कोड समझें: pwm_levels\",\"Multimeter से जाँच\",\"Fade बटन को नहीं पढ़ता\",\"घड़ी देखकर काम करना\",\"fade_millis का कोड और परिणाम\",\"समझाएँ, दोहराएँ और अगला पाठ\"]],\"pt\":[\"ESP32 PWM: Faça um LED Respirar com analogWrite() e millis() | From Zero #5\",\"Faça um LED aumentar e diminuir o brilho suavemente e pause tudo na hora com um botão. Entenda PWM, ciclo de trabalho, analogWrite(), tensão média e um fade com millis() que não perde os apertos.\",[\"Um LED que respira\",\"Duas perguntas para lembrar\",\"PWM: só ligado ou desligado\",\"Ciclo de trabalho\",\"analogWrite(): de 0 a 255\",\"O código: pwm_levels\",\"Confira no multímetro\",\"O fade que não escuta o botão\",\"A solução com o relógio\",\"Código: fade_millis e resultado\",\"Explique, revise e próxima aula\"]],\"es\":[\"ESP32 PWM: Haz Respirar un LED con analogWrite() y millis() | From Zero #5\",\"Haz que un LED suba y baje su brillo suavemente y páusalo al instante con un botón. Entiende PWM, ciclo de trabajo, analogWrite(), voltaje promedio y un fade con millis() que no pierde las pulsaciones.\",[\"Un LED que respira\",\"Dos preguntas para recordar\",\"PWM: encendido o apagado\",\"Ciclo de trabajo\",\"analogWrite(): de 0 a 255\",\"Código: pwm_levels\",\"Comprueba con el multímetro\",\"El fade que no escucha al botón\",\"La solución con el reloj\",\"Código: fade_millis y resultado\",\"Explícalo, resumen y próxima lección\"]],\"id\":[\"ESP32 PWM: LED Bernapas dengan analogWrite() dan millis() | From Zero #5\",\"Buat LED terang dan redup secara halus, lalu hentikan seketika dengan tombol. Pahami PWM, duty cycle, analogWrite(), tegangan rata-rata, dan fade dengan millis() yang tidak melewatkan penekanan tombol.\",[\"LED bernapas\",\"Dua pertanyaan pengingat\",\"PWM: hanya nyala atau mati\",\"Duty cycle\",\"analogWrite(): 0 sampai 255\",\"Tur kode: pwm_levels\",\"Periksa dengan multimeter\",\"Fade melewatkan tombol\",\"Solusi dengan jam\",\"Tur kode: fade_millis dan hasilnya\",\"Jelaskan, rangkuman, dan pelajaran berikutnya\"]],\"ar\":[\"ESP32 PWM: اجعل LED يتنفس باستخدام analogWrite() وmillis() | From Zero #5\",\"اجعل سطوع LED يرتفع وينخفض بسلاسة وأوقفه فورًا بزر. افهم PWM ودورة التشغيل وanalogWrite() ومتوسط الجهد، وأنشئ تدرجًا باستخدام millis() لا يفوّت ضغطات الزر.\",[\"LED يتنفس\",\"سؤالان للتذكّر\",\"PWM: تشغيل أو إيقاف فقط\",\"دورة التشغيل\",\"analogWrite(): من 0 إلى 255\",\"شرح الكود: pwm_levels\",\"الفحص بالملتيميتر\",\"تدرّج يتجاهل الزر\",\"الحل بمراقبة الساعة\",\"شرح fade_millis والنتيجة\",\"اشرح وراجع والدرس القادم\"]],\"ru\":[\"ESP32 PWM: плавное дыхание LED с analogWrite() и millis() | From Zero #5\",\"Плавно меняйте яркость светодиода и мгновенно останавливайте эффект кнопкой. Разберитесь с ШИМ, коэффициентом заполнения, analogWrite(), средним напряжением и плавным переходом с millis(), который не пропускает нажатия.\",[\"Дышащий светодиод\",\"Два вопроса для повторения\",\"ШИМ: включено или выключено\",\"Коэффициент заполнения\",\"analogWrite(): от 0 до 255\",\"Разбор pwm_levels\",\"Проверка мультиметром\",\"Переход пропускает кнопку\",\"Решение с часами\",\"Код fade_millis и результат\",\"Объяснение, итоги и следующий урок\"]],\"de\":[\"ESP32 PWM: Eine LED atmen lassen mit analogWrite() und millis() | From Zero #5\",\"Lass eine LED sanft heller und dunkler werden und halte sie mit einem Taster sofort an. Verstehe PWM, Tastgrad, analogWrite(), mittlere Spannung und einen Fade mit millis(), der keinen Tastendruck verpasst.\",[\"Eine atmende LED\",\"Zwei Fragen zum Wiederholen\",\"PWM: nur an oder aus\",\"Der Tastgrad\",\"analogWrite(): 0 bis 255\",\"Code: pwm_levels\",\"Mit dem Multimeter prüfen\",\"Der Fade verpasst den Taster\",\"Die Lösung mit der Uhr\",\"Code: fade_millis und Ergebnis\",\"Erklären, Rückblick und nächste Folge\"]],\"fr\":[\"ESP32 PWM : faire respirer une LED avec analogWrite() et millis() | From Zero #5\",\"Faites varier doucement la luminosité d'une LED et mettez-la en pause immédiatement avec un bouton. Comprenez le PWM, le rapport cyclique, analogWrite(), la tension moyenne et un fondu avec millis() qui ne manque aucun appui.\",[\"Une LED qui respire\",\"Deux questions de révision\",\"PWM : allumé ou éteint\",\"Le rapport cyclique\",\"analogWrite() : de 0 à 255\",\"Le code : pwm_levels\",\"Vérifier au multimètre\",\"Le fondu manque le bouton\",\"La solution avec l'horloge\",\"fade_millis et le résultat\",\"Expliquez, bilan et prochaine leçon\"]],\"vi\":[\"ESP32 PWM: LED nhịp thở với analogWrite() và millis() | From Zero #5\",\"Làm LED sáng dần rồi tối dần thật mượt và dừng ngay bằng nút nhấn. Hiểu PWM, chu kỳ nhiệm vụ, analogWrite(), điện áp trung bình và hiệu ứng với millis() không bỏ lỡ nút nhấn.\",[\"LED nhịp thở\",\"Hai câu hỏi ôn tập\",\"PWM: chỉ bật hoặc tắt\",\"Chu kỳ nhiệm vụ\",\"analogWrite(): từ 0 đến 255\",\"Đọc code: pwm_levels\",\"Kiểm tra bằng đồng hồ vạn năng\",\"Hiệu ứng bỏ lỡ nút nhấn\",\"Giải pháp nhìn đồng hồ\",\"fade_millis và kết quả\",\"Tự giải thích, ôn tập và bài tiếp theo\"]],\"ja\":[\"ESP32 PWM：analogWrite()とmillis()でLEDを呼吸させよう | From Zero #5\",\"LEDをなめらかに明るく、暗くし、ボタンですぐに止めてみましょう。PWM、デューティ比、analogWrite()、平均電圧を理解し、ボタンを見逃さないmillis()を使ったフェードを作ります。\",[\"呼吸するLED\",\"復習のための2つの質問\",\"PWM：オンかオフだけ\",\"デューティ比\",\"analogWrite()：0から255\",\"コード解説：pwm_levels\",\"テスターで確かめる\",\"ボタンを見逃すフェード\",\"時計を見る解決方法\",\"fade_millisのコードと実行結果\",\"自分の言葉で説明・まとめ・次回\"]]}")

def main():
    schedule = json.loads((HERE / "build/schedule.json").read_text(encoding="utf-8"))
    cut = bumpers.cut(HERE)
    starts = [0] + [int(bumpers.shift(schedule["segments"][sid]["start"], cut)) for sid in CHAPTERS[1:]]
    assert all(b - a >= 10 for a, b in zip(starts, starts[1:])), "Chapters must be at least 10 seconds apart"
    times = ["%d:%02d" % divmod(t, 60) for t in starts]
    out = {}
    for lang, (title, intro, labels) in TEXT.items():
        assert len(labels) == len(times) and len(title) <= 100, (lang, len(title))
        desc = (intro + "\n\n" + LESSON + "\n" + REPO + "\n" + LAB + "\n\n"
                + "\n".join(f"{t} {label}" for t, label in zip(times, labels))
                + "\n\n" + CREDIT + "\n\n#ESP32 #Arduino #PWM #LED #millis")
        assert len(desc) <= 5000 and "<" not in desc and ">" not in desc, lang
        out[lang] = {"title": title, "description": desc}
    (HERE / "chapters.json").write_text(json.dumps(CHAPTERS, indent=1) + "\n", encoding="utf-8")
    (HERE / "localize.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    clips = json.loads((HERE / "script.json").read_text(encoding="utf-8"))["clips"]
    note = ("# YouTube upload - Episode 5: PWM\n\nRelease: 3 November 2026, 17:00 Europe/Istanbul.\n"
            "Thumbnail: video/thumbs/build/ep05_A.png (breathing red LED).\n\n## Title\n"
            + out["en"]["title"] + "\n\n## Description\n" + out["en"]["description"]
            + "\n\n## Creator clips\n" + "".join(f"- {k}: {v}\n" for k, v in clips.items())
            + "\n## Upload checklist\n\n"
              "- Final file: build/ep05_final.mp4; review audio, code, and real footage before upload.\n"
              "- Set video language to English and category to Education.\n"
              "- Set the end screen in the last 20 seconds and verify it after saving.\n"
              "- Upload the 12 SRT files and the 12 metadata entries from localize.json.\n"
              "- Add TR/HI/PT/ES audio after checking the four build/dub_*.m4a files.\n"
              "- Check language availability in YouTube Studio; local files do not prove publication.\n"
              "- Shorts: TR 4 Nov 17:00; EN 5 Nov 22:00. Set each Related video to this episode.\n"
              "- Own-voice clone: follow the disclosure preference in PRODUCTION_GUIDELINES.md.\n")
    (HERE / "youtube.md").write_text(note, encoding="utf-8")
    print(f"ep05: {len(out)} languages; chapters: " + ", ".join(times))

if __name__ == "__main__":
    main()
