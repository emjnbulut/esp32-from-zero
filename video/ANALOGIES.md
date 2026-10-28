# Analogy registry (PRODUCTION_GUIDELINES.md sections 9-10)

One everyday picture per concept, kept the same for the whole series. Every use = picture -> objective meaning -> the
limit of the picture ("The difference: ..."). Never give the same picture to two different concepts.
Add a row before using a new picture; reuse the existing row (same words) when a concept comes back.

| Concept | Picture (EN / TR) | Objective meaning | Where the picture breaks (say it) | First used |
|---|---|---|---|---|
| Sketch layout | recipe card: ingredients, preparation, steps / tarif kartı | names at the top, `setup()` and `loop()` are functions the board calls | a recipe ends; loop never does | recap |
| Variable | labelled moving box / etiketli taşınma kolisi | a named spot in memory; `int` = whole number; `=` puts a value in | a real box can hold many things; a variable holds exactly ONE value, a new value replaces the old one (Hermans 2018) | recap |
| Variable that remembers (global) | football scoreboard / skor tabelası | made outside setup/loop, lives as long as the board runs | — | recap |
| Variable inside loop (local) | goldfish / Japon balığı | made again from scratch every round | — | recap |
| `setup()` | morning routine / sabah rutini | runs exactly once after power-on or reset | pressing reset runs it again | recap |
| `loop()` | night guard doing rounds / tur atan bekçi | called again at its closing brace, forever | the board never gets tired: thousands of rounds a second if nothing waits | recap |
| `const` | house number / kapı numarası | the value can never change; the compiler refuses | — | recap |
| `pinMode` OUTPUT / INPUT | walkie-talkie: talk or listen / telsiz | OUTPUT: the chip drives the pin (3.3 V or GND); INPUT: it only measures | a walkie-talkie switches all the time; a pin keeps the job setup gave it | recap |
| `digitalWrite` | light switch / ışık anahtarı | HIGH = 3.3 V, current flows; LOW = 0 V | the pin can switch thousands of times a second (that is PWM) | recap |
| `delay()` | staring at the microwave timer / mikrodalga sayacına bakmak | the program stops; no other line runs | you would still hear the doorbell; the board really notices nothing | recap |
| `INPUT_PULLUP` | door with a spring / yaylı kapı | a weak resistor inside the chip pulls the pin to 3.3 V; pressing to GND wins | the "spring" is an electric resistor (tens of kΩ), nothing moves | recap |
| `digitalRead` | looking out of the window / pencereden bakmak | measures the pin's voltage now: ≈3.3 V HIGH, ≈0 V LOW | one look = one answer; changes between looks are missed | recap |
| `if / else` | umbrella decision / şemsiye kararı | the condition is exactly true or false; `==` compares | — | recap |
| change detection, `lastState` | comparing two photos / iki fotoğrafı karşılaştırmak | keep the previous reading, compare with `!=` | each "photo" is just one value (HIGH or LOW) | recap |
| (recap only, do not reuse) | door just closed / kapı az önce kapandı | — | clashes with the spring door: use the photos | recap |
| `bool`, `!` toggle | click pen / tükenmez kalem | `bool` holds true/false; `!` gives the opposite | the pen has a spring; `ledOn` only changes when the code flips it | recap |
| debounce | dropped ball bouncing / yere düşen top | contacts flicker for a few ms; wait ~50 ms | far too fast to see | recap |
| `millis()` | wall clock: glance, don't stare / duvar saati | a timer counts in the background; reading it takes no time | it counts ms since power-on and restarts at 0 after reset | recap |
| interval pattern `now - last >= x` | pasta and sauce at once / makarna ve sos | elapsed time since the last change | — | recap |
| PWM | ceiling fan blur / tavan vantilatörü | the pin switches fully on/off ~1000×/s; the eye averages | the fan really moves; the LED really is only ON or OFF | ep05 |
| duty cycle | tap opened part of every second / musluk | % of each cycle the pin is ON | a tap can be half open; a PWM pin is never "half on" | ep05 |
| `analogWrite` 0-255 | dimmer knob / dimmer düğmesi | 256 steps of duty cycle | a real dimmer is smooth; this one has 256 steps | ep05 |
| function with a parameter | recipe with a blank / boşluklu tarif | the value in the brackets fills the blank on every call | — | ep05 |
| blocking `for` + `delay` fade | stairs with headphones on / kulaklıkla merdiven | nothing is checked until the loop ends | — | ep05 |
| fade direction (`step = -step`) | swing / salıncak | turn around at the ends | — | ep05 |
| RGB LED | phone screen dots / telefon ekranındaki noktalar | three LEDs in one package, one shared leg | light adds (red+green = yellow), paint subtracts | ep05 |
| one resistor per color | one straw for three people / tek pipet | each LED needs its own current limit | — | ep05 |
| helper `setColor()` | coffee machine button / kahve makinesi düğmesi | one call sets three analogWrites | — | ep05 |
| mode counter + wrap-around | TV remote channel button; days of the week / kumanda, haftanın günleri | `mode++`, back to 0 after the last | — | ep05 |
