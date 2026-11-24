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
| potentiometer / voltage divider | playground slide / kaydırak | a resistor strip with a sliding contact; the middle leg gives the voltage at the contact | nothing slides down by itself: the contact stays where you leave it | ep07 |
| `analogRead` 0-4095 | ruler with 4096 marks / cetvel | 4096 steps from 0 V to 3.3 V | the ruler flattens near the ends: you may never see exactly 0 or 4095 | ep07 |
| knob zones | stove marks / ocak işaretleri | `if / else if` cuts one number into a few choices | the knob has no clicks; zones exist only in code | ep07 |
| averaging | bathroom scale / banyo tartısı | measure several times, take the average to calm noise | four readings take well under a millisecond, so no time is lost | ep07 |
| print before trusting | doctor's thermometer / doktor termometresi | print the value first to see which half is broken | printing takes time: too many prints slow a fast loop | ep07 |
| input-only pins (34-39) | one-way door / tek yönlü kapı | these pins can only listen, never drive an LED | — | ep07 |
| `map()` | city map / şehir haritası | arithmetic: finds how far along the first range the number is, returns the same position in the second range (whole numbers, rounds down) | a paper map only shrinks; map() can also stretch or flip a range | ep08 |
| level bar (cumulative LEDs) | phone battery bars / telefon pil simgesi | map() gives a level 0-3, if / else if lights that many LEDs from green up | a phone hides many small steps behind each bar; ours has only four states | ep08 |
| state variable (state machine) | washing machine: wash, rinse, spin / çamaşır makinesi | `int state` holds the step number; each loop round runs only that step's code; moving on = new number + new start time (`goTo`) | the machine really does its step; our loop never waits inside a step, it only looks at the number thousands of times a second | ep09 |
| press duration `now - pressStart` | parking ticket stamped at the entry / otopark bileti | save `now` at the press; at the release `now - pressStart` is how long it was held | no paper: one number in memory, the next press writes over it | ep09 |
| `Preferences` (flash that survives power off) | notebook in the desk drawer; variables = labeled boxes on the desk, cleared by a power cut / çekmecedeki defter | a small corner of the flash memory (the memory that holds the program); `begin("reflex")` opens a drawer, `getULong("best", 9999)` reads a page (or the default if empty), `putULong` writes it | the drawer is small and every write wears it a little: write only when something worth keeping happens | ep10 |
| I2C (SDA + SCL) | group chat on two wires / iki kablolu grup sohbeti | one wire carries the message bit by bit (SDA), the other is the beat both sides read on (SCL); every device has a short address (OLED 0x3C) | a chat has many speakers at once; on I2C only the ESP32 starts a conversation | ep10 |
| screen buffer + `display()` | whiteboard behind a curtain / perde arkasındaki beyaz tahta | `print()` draws in the board's memory; `display()` sends the whole picture at once, so there is no flicker | the "curtain" is a copy in RAM (1 KB for 128x64), nothing moves | ep10 |
| RAM vs flash (ep10 v2 wording) | sticky notes on a desk, swept off at a power cut / masadaki yapışkan notlar | normal variables live in RAM and are gone at power-off; Preferences = the drawer row above | — | ep10 |
| PIR output | thumbs up / thumbs down / başparmak yukarı / aşağı | the sensor does the hard work and only gives HIGH (something warm moved) or LOW | the "thumb" stays up for the time set by the orange knob, not just for the moment of motion | ep11 |
| PIR lens zones | row of flashlights / yan yana el fenerleri | the dome is a Fresnel lens: many windows, each looks at its own slice of the room; warmth moving from one slice to the next = motion | flashlights shine light out; the PIR sends nothing, it only receives warmth | ep11 |
| active vs passive buzzer | music box (one tune) vs little speaker / müzik kutusu vs küçük hoparlör | active: its own oscillator inside, power on = one fixed beep; passive: plays the note `tone()` sends | both are piezo discs; the "speaker" is only loud at a few kHz | ep11 |
| hysteresis (two thresholds) | thermostat that waits a little before switching back / termostat | switch on above the upper line, off only below the lower line; between them nothing changes, so a value hovering at one line cannot make the output flicker | a thermostat works with temperature and time; ours only compares numbers each loop | ep15 |
| interrupt (`attachInterrupt`) | doorbell instead of checking the door / kapıyı kontrol etmek yerine kapı zili | the pin itself makes the chip stop, run a tiny function (`IRAM_ATTR`) and go back; nothing fast is missed between two looks | a real doorbell waits for you to finish; the interrupt function runs at once, so it must be tiny (count, note the time) | ep16 |
| softAP (the board's own Wi-Fi) | the hotspot on your phone / telefondaki kişisel erişim noktası | WiFi.softAP(name, password) makes the board an access point; the phone joins it, the board's address inside is 192.168.4.1 | a phone hotspot shares the internet; the board's network has no internet at all, only the board | ep12 |
| web page buttons = commands | restaurant menu where every dish has a number you call out / numaralı restoran menüsü | each button is a link (/color, /ring); server.on() ties each link to a helper function | a waiter remembers your table; the board forgets each request as soon as it answered | ep12 |
| URL argument (?c=red) | the note on an order slip / sipariş fişindeki not | server.arg("c") reads the detail after "?" | — | ep12 |
