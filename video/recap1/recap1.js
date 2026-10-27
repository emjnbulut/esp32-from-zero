/* Recap: episodes 1-4 - how to read a sketch (2026-10-27).
 * One topic: every sketch = names + setup + loop, and variables are its memory. Each sketch is run as a LIVE TRACE:
 * the highlighted line moves with the narration and a MEMORY panel shows every variable changing (PRODUCTION_GUIDELINES.md
 * section 8). Segment ids: see make_script.py. Only syntax from episodes 1-4. */
const stage = $("#stage");
const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const hidden = (e) => { gsap.set(e, { opacity: 0 }); return e; };
const CUT = S0("s03") - 0.1; // the channel sting is inserted here (tools/bumpers.py cut())
const END = S1("s46");

/* ---- the live trace: code card + MEMORY panel + (optional) LED, status chip and serial box ---- */
const st = (t, line, set, extra) => Object.assign({ t, line, set }, extra || {});
function trace(scene, o) {
  const size = o.size || 28, MX = 1170, MW = 690;
  const bc = bigCode(scene, o.x != null ? o.x : 80, o.y != null ? o.y : 120, o.w || 1040, o.code, { size, pad: 24 });
  const memk = box(scene, MX, 112, MW, 30, "memk", "MEMORY · the sketch's boxes"); hidden(memk);
  const rows = o.vars.map((v, i) => {
    const row = box(scene, MX, 150 + i * 84, MW, 70, "mrow", `<span class="nm">${v.label || v.name}</span><span class="vl">–</span>`);
    hidden(row);
    return { name: v.name, row, vl: $(".vl", row) };
  });
  const yEnd = 150 + o.vars.length * 84;
  const chipEl = box(scene, MX, yEnd + 8, MW, 56, "chip", ""); hidden(chipEl);
  let ledG = null;
  if (o.led) {
    ledG = box(scene, MX + 6, yEnd + 84, 110, 110, "", "");
    css(ledG, { borderRadius: "50%", border: "3px solid #5a1a20", background: "#3a1014" });
    hidden(ledG);
  }
  let ser = null;
  if (o.serial) { ser = box(scene, MX, yEnd + (o.led ? 210 : 84), MW, 190, "serial", ""); hidden(ser); }
  const steps = o.steps.slice().sort((a, b) => a.t - b.t);
  if (o.memFrom != null) { show([memk, ...rows.map((r) => r.row)], o.memFrom, 0.4); }
  else show([memk, ...rows.map((r) => r.row)], o.t0, 0.4);
  if (ledG) show(ledG, o.memFrom != null ? o.memFrom : o.t0, 0.4);
  if (ser) show(ser, o.memFrom != null ? o.memFrom : o.t0, 0.4);
  show(chipEl, o.t0, 0.3);
  show(bc.c, o.t0, 0.4);
  dyn((t) => {
    let k = -1;
    for (let i = 0; i < steps.length; i++) if (t >= steps[i].t) k = i;
    const vals = {}, ch = {}, lines = [];
    let led = false, chip = null, lineSel = -1;
    for (let i = 0; i <= k; i++) {
      const s = steps[i];
      if (s.set) for (const n in s.set) { vals[n] = s.set[n]; ch[n] = s.t; }
      if (s.led !== undefined) led = s.led;
      if (s.chip !== undefined) chip = s.chip;
      if (s.say) lines.push(s.say);
      lineSel = s.line == null ? -1 : s.line;
    }
    // code highlight (a line or a range of lines)
    if (lineSel === -1 || lineSel === undefined) bc.bar.style.opacity = 0;
    else {
      const [a, b] = Array.isArray(lineSel) ? lineSel : [lineSel, lineSel];
      Object.assign(bc.bar.style, { opacity: 1, top: bc.pad + a * bc.lh + "px", height: (b - a + 1) * bc.lh + "px",
        background: "rgba(255,181,71,.2)", borderColor: "rgba(255,181,71,.85)" });
    }
    rows.forEach((r) => {
      const v = vals[r.name], txt = v === undefined ? "–" : String(v);
      if (r.vl.__v !== txt) { r.vl.textContent = txt; r.vl.__v = txt; }
      const f = r.name in ch ? Math.max(0, 1 - (t - ch[r.name]) / 1.0) : 0;
      r.row.style.borderColor = f > 0.02 ? `rgba(255,181,71,${0.35 + 0.65 * f})` : "#2c3b5e";
      r.row.style.boxShadow = f > 0.02 ? `0 0 ${34 * f}px rgba(255,181,71,${0.7 * f})` : "none";
      r.vl.style.color = f > 0.02 ? "#ffd89a" : "#eef3fb";
    });
    if (chip) {
      const html = typeof chip === "string" ? chip : chip.html;
      const col = typeof chip === "string" ? "amber" : chip.col || "amber";
      const cm = { amber: ["rgba(255,181,71,.18)", "#ffb547", "#ffe3b8"], teal: ["rgba(25,195,180,.16)", "#19c3b4", "#b9f3ec"],
        red: ["rgba(255,93,108,.18)", "#ff5d6c", "#ffc2c8"], green: ["rgba(74,222,128,.18)", "#4ade80", "#d6ffe4"] }[col];
      if (chipEl.__v !== html) { chipEl.innerHTML = html; chipEl.__v = html; }
      Object.assign(chipEl.style, { background: cm[0], border: "2px solid " + cm[1], color: cm[2], visibility: "visible" });
    } else chipEl.style.visibility = "hidden";
    if (ledG) {
      ledG.style.background = led ? "radial-gradient(circle at 40% 35%, #ffd0d0, #e0202c 70%)" : "#3a1014";
      ledG.style.borderColor = led ? "#ff8a8f" : "#5a1a20";
      ledG.style.boxShadow = led ? "0 0 60px 18px rgba(255,70,80,.75)" : "none";
    }
    if (ser) { const html = lines.slice(-5).map((l) => `<div>${l}</div>`).join(""); if (ser.__v !== html) { ser.innerHTML = html; ser.__v = html; } }
  });
  return bc;
}
const title = (scene, html, t0) => { const e = box(scene, 0, 32, 1920, 60, "ptitle", html); hidden(e); show(e, t0, 0.4); return e; };
/* the real result next to the trace (reused creator clips, looped by footage prep): PRODUCTION_GUIDELINES.md section 4 */
const inset = (id, t0, t1, desc, sketch) => heroClip(stage, id, t0, t1, desc, { x: 1330, y: 744, w: 520, h: 293, sketch });
const SRC = {
  hello: `int seconds = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Hello, ESP32!");
}

void loop() {
  seconds = seconds + 1;
  Serial.printf("I have been running for %d seconds\\n", seconds);
  delay(1000);
}`,
  blink: `const int LED_PIN = 23;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}`,
  btn: `const int BUTTON_PIN = 22;
const int LED_PIN = 23;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int state = digitalRead(BUTTON_PIN);

  if (state == LOW) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(50);
}`,
  tog: `int lastState = HIGH;
bool ledOn = false;
int presses = 0;

void loop() {
  int state = digitalRead(BUTTON_PIN);
  if (state != lastState) {
    if (state == LOW) {
      presses++;
      ledOn = !ledOn;
      digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
    }
    delay(50);
  }
  lastState = state;
}`,
  ms: `bool blinking = true;
bool ledOn = false;
unsigned long lastBlink = 0;
int lastState = HIGH;
unsigned long lastChange = 0;

void loop() {
  unsigned long now = millis();

  int state = digitalRead(BUTTON_PIN);
  if (state != lastState && now - lastChange >= 50) {
    lastChange = now;
    lastState = state;
    if (state == LOW) blinking = !blinking;
  }

  if (blinking && now - lastBlink >= 500) {
    lastBlink = now;
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
  }
}`,
};

/* ======================================================================
 * COLD OPEN (s01-s02): the five results, one after another
 * ==================================================================== */
const sCold = SC();
SET(sCold, 0, { opacity: 1 });
SET(sCold, CUT, { opacity: 0 });
{
  const tC = S1("s02") + 0.35, n = 5, w = tC / n;
  // window 0: the serial monitor of hello_esp32 (recreated), windows 1-4: the real clips
  const serial = box(sCold, 160, 300, 1600, 560, "serial", ""); css(serial, { fontSize: "40px", lineHeight: "1.5", padding: "36px 44px" });
  textAt(serial, [[0, ""], [0.8, "Hello, ESP32!"], [1.8, "Hello, ESP32!<br>I have been running for 1 seconds"], [2.6, "Hello, ESP32!<br>I have been running for 1 seconds<br>I have been running for 2 seconds"]]);
  const names = ["hello_esp32 · episode 1", "blink_led · episode 3", "button_led · episode 4", "button_toggle · episode 4", "blink_button · episode 4"];
  [["C1", "The LED blinking once per second."], ["C2", "button_led: the LED lights while the button is held."], ["C3", "button_toggle: press on, press off."], ["C4", "blink_button: the LED blinks; a press stops it."]].forEach(([id, d], i) => {
    heroClip(stage, id, (i + 1) * w, (i + 2) * w, d, { full: true });
  });
  names.forEach((nm, i) => {
    const p = box(stage, 0, 930, 1920, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:34px;background:rgba(11,18,32,.82);border:2px solid #19c3b4;color:#d9fffa">${nm}</span></div>`);
    hidden(p); show(p, i * w + 0.25, 0.3); hide(p, (i + 1) * w - 0.2, 0.25);
  });
  const kick = box(sCold, 160, 120, 1200, 40, "kicker", "ESP32 From Zero · Recap"); hidden(kick);
  const ttl = box(sCold, 154, 160, 1500, 130, "h1", "Read any sketch."); css(ttl, { fontSize: "104px" }); hidden(ttl);
  show([kick, ttl], 0.3, 0.5);
  hide([kick, ttl], 2.9, 0.3); // the clips take over the frame; the line returns on the closing card
}

/* ======================================================================
 * PART 1 - THE SKELETON (hello_esp32): s03-s10
 * ==================================================================== */
const sSkel = SC();
sceneIn(sSkel, CUT, 0.4);
sceneOut(sSkel, S1("s10") + 0.4);
{
  title(sSkel, `Part 1 · the skeleton <small>hello_esp32.ino · episode 1</small>`, CUT + 0.1);
  // the three parts as colored tags next to the code (s03)
  const tags = [["NAMES", "#ffb547", "#2a1a00", 0, 0], ["SETUP · once", "#19c3b4", "#04201d", 2, 6], ["LOOP · forever", "#b48cff", "#1e1040", 8, 12]];
  const lh = Math.round(25 * 1.55);
  const tg = tags.map(([txt, bg, fg, a, b], i) => {
    const e = box(sSkel, 1130, 120 + 24 + a * lh + ((b - a + 1) * lh - 42) / 2, 0, 0, "tag3", txt);
    css(e, { background: bg, color: fg, width: "auto", height: "auto" });
    hidden(e);
    const strip = box(sSkel, 1118, 120 + 24 + a * lh + 4, 8, (b - a + 1) * lh - 8, "", ""); css(strip, { background: bg, borderRadius: "4px" }); hidden(strip);
    return [e, strip];
  });
  [W("s03", "Names"), W("s03", "setup"), W("s03", "loop")].forEach((t, i) => { show(tg[i], t - 0.05, 0.35); hide(tg[i], T("s04") - 0.1, 0.3); });
  const back = box(sSkel, 1130, 120 + 24 + 8 * lh + 6, 0, 0, "tag3", "↺ then back to the top"); css(back, { background: "#b48cff", color: "#1e1040", width: "auto", height: "auto" }); hidden(back);
  show(back, W("s06", "jumps") - 0.05, 0.35); hide(back, T("s07") - 0.1, 0.3);
  trace(sSkel, {
    code: SRC.hello, t0: CUT + 0.2, memFrom: T("s04") - 0.1, serial: true, size: 25,
    vars: [{ name: "seconds" }],
    steps: [
      st(T("s03"), -1),
      st(W("s03", "Names"), 0), st(W("s03", "setup"), [2, 6]), st(W("s03", "loop"), [8, 12]),
      st(T("s04"), 0, { seconds: 0 }, { chip: { html: "a box with a label", col: "amber" } }),
      st(T("s05"), [2, 5], null, { chip: { html: "runs once: serial opens, hello", col: "teal" } }),
      st(W("s05", "says"), 5, null, { say: "Hello, ESP32!" }),
      st(T("s06"), [8, 12], null, { chip: { html: "runs forever", col: "teal" } }),
      st(T("s07"), -1, { seconds: 0 }, { chip: { html: "round 1", col: "amber" } }),
      st(W("s07", "Add"), 9),
      st(W("s07", "now"), 9, { seconds: 1 }),
      st(W("s07", "Print"), 10, null, { say: "I have been running for 1 seconds" }),
      st(W("s07", "Wait"), 11),
      st(W("s07", "Back"), 8, null, { chip: { html: "round 2", col: "amber" } }),
      st(W("s07", "add", 2), 9),
      st(W("s07", "two"), 9, { seconds: 2 }),
      st(W("s07", "two") + 0.6, 10, null, { say: "I have been running for 2 seconds" }),
      st(T("s08"), -1, null, { chip: { html: "a variable = the sketch's MEMORY", col: "amber" } }),
      st(T("s09"), -1),
      st(T("s10") + 0.2, 9, { seconds: 3 }, { chip: { html: "round 3", col: "amber" } }),
      st(T("s10") + 0.9, 9, { seconds: 4 }, { chip: { html: "round 4", col: "amber" } }),
      st(T("s10") + 1.6, 9, { seconds: 5 }, { chip: { html: "round 5", col: "amber" } }),
    ],
  });
  quizCard(sSkel, "After the loop has run 5 times, what does <b>seconds</b> hold?", W("s09", "Quick"), T("s10"), "5: each round adds one, and the box remembers.", { y: 840, w: 1500, t1: S1("s10") });
}
likeSub(stage, T("s11") + 0.6, 2.6); // reminder 1 of 2

/* ======================================================================
 * PART 2 - OUTPUTS (blink_led): s11-s14
 * ==================================================================== */
const sBlink = SC();
sceneIn(sBlink, S0("s11") - 0.1, 0.4);
sceneOut(sBlink, S1("s14") + 0.4);
{
  title(sBlink, `Part 2 · outputs <small>blink_led.ino · episode 3</small>`, S0("s11"));
  const blinkSteps = [];
  const cyc = [[7, true, "GPIO 23 = 3.3 V"], [8, true, "GPIO 23 = 3.3 V"], [9, false, "GPIO 23 = 0 V"], [10, false, "GPIO 23 = 0 V"]];
  for (let k = 0; k < 10; k++) {
    const [ln, on, volt] = cyc[k % 4];
    blinkSteps.push(st(T("s14") + 1.2 + 0.7 * k, ln, null, { led: on, chip: { html: (ln === 8 || ln === 10 ? "delay: waiting, doing nothing" : volt), col: ln === 8 || ln === 10 ? "red" : "amber" } }));
  }
  trace(sBlink, {
    code: SRC.blink, t0: S0("s11") - 0.1, led: true,
    vars: [{ name: "LED_PIN", label: "LED_PIN (constant)" }],
    steps: [
      st(T("s11"), 0, { LED_PIN: 23 }, { chip: { html: "GPIO 23 → 220 Ω → LED → GND", col: "teal" } }),
      st(T("s12"), 3, null, { chip: { html: "pinMode: this pin is an OUTPUT", col: "teal" } }),
      st(T("s13"), [6, 11]),
      st(W("s13", "HIGH"), 7, null, { led: true, chip: { html: "HIGH = 3.3 V → LED on", col: "amber" } }),
      st(W("s13", "LOW"), 9, null, { led: false, chip: { html: "LOW = 0 V → LED off", col: "amber" } }),
      st(T("s14"), 8, null, { chip: { html: "delay: waiting, doing nothing", col: "red" } }),
      ...blinkSteps,
    ],
  });
}

inset("C1", T("s11") + 0.5, S1("s14") + 0.2, "blink_led: the LED blinking once per second.", "blink_led");

/* ======================================================================
 * PART 3 - DECISIONS (button_led): s15-s21
 * ==================================================================== */
const sBtn = SC();
sceneIn(sBtn, S0("s15") - 0.1, 0.4);
sceneOut(sBtn, S1("s21") + 0.4);
{
  title(sBtn, `Part 3 · decisions <small>button_led.ino · episode 4</small>`, S0("s15"));
  trace(sBtn, {
    code: SRC.btn, t0: S0("s15") - 0.1, led: true,
    vars: [{ name: "state" }],
    steps: [
      st(T("s15"), [0, 1], null, { chip: { html: "names: the two pins", col: "amber" } }),
      st(W("s15", "setup"), 4, null, { chip: { html: "INPUT: we read this pin", col: "teal" } }),
      st(W("s15", "Pull"), 4, null, { chip: { html: "PULL-UP: idle = HIGH", col: "teal" } }),
      st(T("s16"), 4, { state: "HIGH" }, { chip: { html: "not pressed → HIGH", col: "green" } }),
      st(W("s16", "Pressed"), 4, { state: "LOW" }, { chip: { html: "pressed → LOW", col: "red" } }),
      st(T("s17"), 9, null, { chip: { html: "digitalRead = a question", col: "teal" } }),
      st(W("s17", "answer"), 9, { state: "HIGH" }, { chip: { html: "the answer goes into state", col: "amber" } }),
      st(T("s18"), 11, { state: "LOW" }, { chip: { html: "button pressed", col: "red" } }),
      st(W("s18", "LED"), 12, null, { led: true, chip: { html: "LOW → LED gets HIGH", col: "amber" } }),
      st(W("s18", "Otherwise"), 14, { state: "HIGH" }, { led: false, chip: { html: "otherwise → LED gets LOW", col: "amber" } }),
      st(T("s19"), -1, null, { chip: { html: "remembers: nothing", col: "red" } }),
      st(T("s20"), -1, null, { chip: { html: "pressed? yes. JUST pressed? ?", col: "amber" } }),
      st(T("s21"), -1, null, { chip: { html: "🚪 closed now… was it open before?", col: "teal" } }),
      st(W("s21", "remember"), -1, null, { chip: { html: "needs the LAST reading", col: "teal" } }),
    ],
  });
  quizCard(sBtn, "No memory: can it tell you pressed the button <b>just now</b>?", W("s20", "Quick"), T("s21"), "No: only pressed or not pressed. It must remember the last reading.", { x: 1170, y: 480, w: 690, t1: S1("s21") });
}

inset("C2", T("s16"), W("s20", "Quick") - 0.3, "button_led: the LED lights while the button is held.", "button_led");

/* ======================================================================
 * PART 4 - MEMORY 1 (button_toggle): s22-s28
 * ==================================================================== */
const sTog = SC();
sceneIn(sTog, S0("s22") - 0.1, 0.4);
sceneOut(sTog, S1("s28") + 0.4);
{
  title(sTog, `Part 4 · memory <small>button_toggle.ino · episode 4</small>`, S0("s22"));
  trace(sTog, {
    code: SRC.tog, t0: S0("s22") - 0.1, led: true,
    vars: [{ name: "state" }, { name: "lastState" }, { name: "ledOn" }, { name: "presses" }],
    steps: [
      st(T("s22"), 0, { lastState: "HIGH", ledOn: "false", presses: 0 }, { chip: { html: "last state = the round before", col: "teal" } }),
      st(T("s23"), 5, null, { chip: { html: "compare state with lastState", col: "teal" } }),
      st(W("s23", "different"), 6, null, { chip: { html: "different = something changed", col: "amber" } }),
      st(W("s23", "LOW"), 7, null, { chip: { html: "…and now LOW = new press", col: "amber" } }),
      st(T("s24"), [8, 10], null, { chip: { html: "flip ledOn, count the press", col: "amber" } }),
      st(T("s25"), 14, null, { chip: { html: "copy state → lastState", col: "teal" } }),
      // the run (s26-s27)
      st(T("s26"), 5, { state: "HIGH" }, { chip: { html: "round: not pressed", col: "green" } }),
      st(W("s26", "Same"), 6, null, { chip: { html: "HIGH = HIGH: same, nothing", col: "green" } }),
      st(W("s26", "Now"), 5, { state: "LOW" }, { chip: { html: "round: PRESSED", col: "red" } }),
      st(W("s26", "Different"), 6, null, { chip: { html: "LOW ≠ HIGH: different", col: "amber" } }),
      st(W("s26", "new"), [7, 10], { presses: 1, ledOn: "true" }, { led: true, chip: { html: "new press! ledOn flips", col: "red" } }),
      st(W("s26", "turns") + 0.4, 14, { lastState: "LOW" }, { chip: { html: "lastState = LOW", col: "teal" } }),
      st(T("s27"), 5, { state: "LOW" }, { chip: { html: "round: still held", col: "red" } }),
      st(W("s27", "Same"), 6, null, { chip: { html: "LOW = LOW: same, nothing", col: "green" } }),
      st(W("s27", "Let"), 5, { state: "HIGH" }, { chip: { html: "round: let go", col: "green" } }),
      st(W("s27", "different"), 6, null, { chip: { html: "HIGH ≠ LOW: different", col: "amber" } }),
      st(W("s27", "not"), 7, null, { chip: { html: "…but not LOW: no press", col: "green" } }),
      st(W("s27", "So"), 14, { lastState: "HIGH" }, { chip: { html: "lastState = HIGH", col: "teal" } }),
      st(T("s28"), 12, null, { chip: { html: "50 ms: wait for the bounce to end", col: "amber" } }),
    ],
  });
}
inset("C3", T("s26"), S1("s28") + 0.2, "button_toggle: press on, press off.", "button_toggle");
likeSub(stage, T("s28") + 2.2, 2.6); // reminder 2 of 2

/* ======================================================================
 * PART 5 - MEMORY 2 (blink_button): s29-s34
 * ==================================================================== */
const sMs = SC();
sceneIn(sMs, S0("s29") - 0.1, 0.4);
sceneOut(sMs, S1("s34") + 0.4);
{
  title(sMs, `Part 5 · the clock <small>blink_button.ino · episode 4 (shortened)</small>`, S0("s29"));
  const tickSteps = [];
  for (let k = 0; k < 6; k++) tickSteps.push(st(T("s30") + 0.5 + k * ((S1("s30") - T("s30") - 1) / 6), 7, { now: 1000 + 120 * k }, { chip: { html: "millis() counts by itself", col: "teal" } }));
  trace(sMs, {
    code: SRC.ms, t0: S0("s29") - 0.1, led: true, size: 25,
    vars: [{ name: "now" }, { name: "lastBlink" }, { name: "diff", label: "now − lastBlink" }, { name: "ledOn" }, { name: "blinking" }],
    steps: [
      st(T("s29"), 6, { lastBlink: 0, ledOn: "false", blinking: "true" }, { chip: { html: "⏲ delay = staring at a kitchen timer", col: "red" } }),
      st(W("s29", "wall"), 6, null, { chip: { html: "🕒 millis = glancing at a wall clock", col: "teal" } }),
      ...tickSteps,
      st(T("s31"), 7, { now: 1200, lastBlink: 1000, diff: 200 }, { chip: { html: "now = the time right now", col: "teal" } }),
      st(W("s31", "Last"), 2, null, { chip: { html: "lastBlink = when it last changed", col: "teal" } }),
      st(W("s31", "minus"), 16, null, { chip: { html: "now − lastBlink = how long ago", col: "amber" } }),
      st(T("s32"), 16, { now: 1000, lastBlink: 1000, diff: 0, ledOn: "true" }, { led: true, chip: { html: "1000: LED flips, lastBlink = 1000", col: "amber" } }),
      st(W("s32", "twelve"), 16, { now: 1200, diff: 200 }, { chip: { html: "200 < 500: not yet", col: "green" } }),
      st(W("s32", "fifteen"), 16, { now: 1500, diff: 500 }, { chip: { html: "500 ≥ 500: flip!", col: "red" } }),
      st(W("s32", "Flip"), [17, 19], { lastBlink: 1500, diff: 0, ledOn: "false" }, { led: false, chip: { html: "flipped; lastBlink = 1500", col: "amber" } }),
      st(T("s33"), [10, 12], { lastBlink: 1500 }, { chip: { html: "same trick for the button: 50 ms", col: "teal" } }),
      st(T("s34"), 13, { blinking: "false" }, { chip: { html: "a press flips blinking", col: "amber" } }),
      st(W("s34", "false"), 16, null, { chip: { html: "false: the LED part is skipped", col: "red" } }),
      st(W("s34", "never"), 9, null, { chip: { html: "the loop never waits: button still works", col: "green" } }),
    ],
  });
}

inset("C4", T("s29"), S1("s34") + 0.2, "blink_button: the LED blinks; a press stops it.", "blink_button");

/* ======================================================================
 * THE FOUR QUESTIONS: s35-s37
 * ==================================================================== */
const sFour = SC();
sceneIn(sFour, S0("s35") - 0.1, 0.4);
sceneOut(sFour, S1("s37") + 0.4);
{
  title(sFour, "Every sketch answers the same four questions", S0("s35"));
  const qs = [["names", "What are the <b style='color:var(--amber)'>names</b>?", W("s36", "One")],
    ["once", "What happens <b style='color:var(--teal)'>once</b>? (setup)", W("s36", "Two")],
    ["repeats", "What <b style='color:#b48cff'>repeats</b>? (loop)", W("s36", "Three")],
    ["remember", "What does it <b style='color:var(--red)'>remember</b>?", W("s36", "four")]];
  const els = qs.map(([k, html, t], i) => {
    const r = box(sFour, 210, 170 + i * 175, 1500, 130, "qrow", `<span class="n">${i + 1}</span><span>${html}</span>`);
    hidden(r); pop(r, t - 0.05, 0.4);
    return r;
  });
  styleAt(els[3], "boxShadow", [[0, "none"], [T("s37"), "0 0 50px rgba(255,181,71,.55)"]]);
  dyn((t) => { els[3].classList.toggle("hot", t >= T("s37")); });
}

/* ======================================================================
 * PRACTICE: s38-s44
 * ==================================================================== */
const sPrac = SC();
sceneIn(sPrac, S0("s38") - 0.1, 0.4);
sceneOut(sPrac, S1("s44") + 0.4);
{
  title(sPrac, "Your turn <small>pause the video if you want to think</small>", S0("s38"));
  const snippets = [
    ["1", "int count = 0;\n\nvoid loop() {\n  count = count + 2;\n  Serial.println(count);\n  delay(1000);\n}", "s39", "s40", "Round after round, what are the first <b>3 prints</b>?", "2, 4, 6: the box remembers and adds 2 every round."],
    ["2", "if (state == LOW && lastState == HIGH) {\n  presses++;\n}\nlastState = state;", "s41", "s42", "You hold the button for <b>5 rounds</b>. How many presses?", "1: only the first round has a change; after that it's LOW and LOW."],
    ["3", "unsigned long lastBlink = 0;\nunsigned long now = 700;\n\nif (now - lastBlink >= 500) {\n  // flip the LED\n  lastBlink = now;\n}", "s43", "s44", "Does the LED flip?", "Yes: 700 − 0 = 700, and that's at least 500. Then lastBlink = 700."],
  ];
  snippets.forEach(([n, code, qa, an, q, a]) => {
    const t0 = S0(qa), t1 = S1(an) + 0.2;
    const lines = code.split("\n").length;
    const bc = bigCode(sPrac, 360, 150, 1200, code, { size: 40 });
    show(bc.c, t0, 0.4); hide(bc.c, t1, 0.3);
    const pill = box(sPrac, 330, 110, 0, 0, "", `<span class="pill" style="font-size:30px;background:var(--amber);color:#2a1a00">${n} / 3</span>`);
    css(pill, { width: "auto", height: "auto" }); hidden(pill); show(pill, t0, 0.3); hide(pill, t1, 0.3);
    quizCard(sPrac, q, t0 + 0.5, S0(an), a, { x: 360, y: 150 + lines * 62 + 90, w: 1200, t1 });
  });
}

/* ======================================================================
 * OUTRO: s45-s46
 * ==================================================================== */
const sOut = SC();
sceneIn(sOut, S0("s45") - 0.1, 0.5);
{
  const k = box(sOut, 160, 250, 1200, 40, "kicker", "Next episode"); hidden(k);
  const h = box(sOut, 154, 296, 1600, 160, "h1", "Fade it. Mix it."); css(h, { fontSize: "112px" }); hidden(h);
  const s = box(sOut, 160, 480, 1500, 60, "h3", "PWM and RGB colors"); hidden(s);
  show([k, h, s], W("s46", "Next") - 0.2, 0.6);
  // while "today we read five sketches" is spoken: the four questions and the five sketches, ticking in
  const sum = box(sOut, 0, 250, 1920, 120, "", `<div style="text-align:center;font:800 64px var(--display)"><span style="color:var(--amber)">Names</span> · <span style="color:var(--teal)">Setup</span> · <span style="color:#b48cff">Loop</span> · <span style="color:var(--red)">Memory</span></div>`);
  hidden(sum); show(sum, S0("s45") + 0.2, 0.5); hide(sum, W("s46", "Next") - 0.4, 0.4);
  ["hello_esp32", "blink_led", "button_led", "button_toggle", "blink_button"].forEach((nm, i) => {
    const p = box(sOut, 0, 450 + i * 78, 1920, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:34px;background:rgba(74,222,128,.14);border:2px solid #4ade80;color:#d6ffe4">✓ ${nm}</span></div>`);
    hidden(p); show(p, S0("s45") + 1.2 + i * 1.1, 0.4); hide(p, W("s46", "Next") - 0.4, 0.4);
  });
  const c1 = box(sOut, 160, 80, 1700, 120, "", `<span class="pill" style="font-size:40px;background:rgba(25,195,180,.16);border:2px solid #19c3b4;color:#d9fffa">💬 Which sketch was the hardest to read? Tell me in the comments.</span>`);
  css(c1, { width: "auto", height: "auto" }); hidden(c1);
  show(c1, W("s45", "tell") - 0.3, 0.5);
}

window.__seek(0);
window.__ready = true;
