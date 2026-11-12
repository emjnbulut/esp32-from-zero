/* YouTube thumbnails (1280x720). The variant comes from the URL: thumbs.html?ep03_A
 * Rendered by video/tools/thumbs.mjs. Big 2-4 word title on the left, one clear picture on the right. */
const T = document.getElementById("t");
const put = (x, y, w, h, html, cls = "", style = "") => {
  const e = document.createElement("div");
  e.className = "abs " + cls;
  if (x !== null) Object.assign(e.style, { left: x + "px", top: y + "px" });
  if (w) e.style.width = w + "px";
  if (h) e.style.height = h + "px";
  if (style) e.style.cssText += style;
  e.innerHTML = html;
  T.appendChild(e);
  return e;
};
/* Per-language versions (2026-11-12): thumbs.html?ep08_A_tr. Only the words change, never the picture;
 * hooks are rewritten natively in LOC (not word for word). Dub languages: tr hi pt es. */
const LANGS = ["tr", "hi", "pt", "es"];
const [key, lang] = (() => { const k = location.search.slice(1), m = k.match(/^(.*)_(tr|hi|pt|es)$/); return m ? [m[1], m[2]] : [k, "en"]; })();
const COL = { white: "var(--text)", amber: "var(--amber)", teal: "var(--teal)", red: "var(--red)", green: "var(--green)" };

/* ---- pictures ---- */
let gid = 0;
function led(x, y, w, color = "red", lit = true) {
  const col = color === "red" ? ["#ff8a8f", "#d4202c", "#b51d27", "rgba(255,70,70,.95)", "#ffe3e3"]
    : color === "yellow" ? ["#fff09a", "#e8b800", "#b38f00", "rgba(255,220,60,.9)", "#fff8d8"] : ["#8af5b0", "#1fae55", "#178a3a", "rgba(60,240,120,.9)", "#e3ffec"];
  const id = "g" + gid++;
  if (lit) put(x - w * 1.1, y - w * 1.0, w * 3.2, w * 3.2, "", "", `border-radius:50%;background:radial-gradient(circle, ${col[3]} 0%, rgba(0,0,0,0) 62%)`);
  put(x, y, w, w * 230 / 120, `<svg width="${w}" viewBox="0 0 120 230"><defs><radialGradient id="${id}" cx=".4" cy=".35"><stop offset="0" stop-color="${col[0]}"/><stop offset="1" stop-color="${col[1]}"/></radialGradient></defs>
    <path d="M44 96 V226" stroke="#c3c9d1" stroke-width="7" stroke-linecap="round"/><path d="M76 96 V186" stroke="#c3c9d1" stroke-width="7" stroke-linecap="round"/>
    <path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="url(#${id})"/>${lit ? `<path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="${col[4]}" opacity=".75"/>` : ""}
    <path d="M22 92 h70 v14 h-70 z" fill="${col[2]}"/></svg>`);
}
/** an RGB LED lit in color c = [r, g, b] */
function rgbLed(x, y, w, c) {
  const [r, g, b] = c;
  put(x - w * 1.1, y - w * 0.9, w * 3.2, w * 3.2, "", "", `border-radius:50%;background:radial-gradient(circle, rgba(${r},${g},${b},.95) 0%, rgba(${r},${g},${b},.35) 32%, rgba(0,0,0,0) 62%)`);
  const tint = `rgb(${Math.round(170 + r / 3)},${Math.round(170 + g / 3)},${Math.round(170 + b / 3)})`;
  put(x, y, w, w * 190 / 120, `<svg width="${w}" viewBox="0 0 120 190"><path d="M34 96 V176 M52 96 V190 M68 96 V176 M86 96 V172" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/>
    <path d="M24 96 V52 a36 36 0 0 1 72 0 V96 z" fill="${tint}"/><path d="M34 60 a24 24 0 0 1 20 -26" stroke="#fff" stroke-width="7" fill="none" opacity=".7" stroke-linecap="round"/>
    <path d="M18 92 h84 v12 h-84 z" fill="#c9d0d8"/></svg>`);
}
function board(x, y, w, rot = 0) {
  put(x, y, w, 0, boardSVG({ pins: 30, chip: "cp2102", p: "b", width: w }), "",
    `filter:drop-shadow(0 30px 50px rgba(0,0,0,.6)) drop-shadow(0 0 40px rgba(25,195,180,.3));transform:rotate(${rot}deg)`);
}
function button(x, y, w, pressed = false) {
  put(x, y, w, w, `<svg width="${w}" height="${w}" viewBox="0 0 100 100">
    <rect x="20" y="0" width="9" height="16" rx="2" fill="#b8bec6"/><rect x="71" y="0" width="9" height="16" rx="2" fill="#b8bec6"/>
    <rect x="20" y="84" width="9" height="16" rx="2" fill="#b8bec6"/><rect x="71" y="84" width="9" height="16" rx="2" fill="#b8bec6"/>
    <rect x="8" y="10" width="84" height="80" rx="9" fill="#23272f" stroke="#3a404b" stroke-width="2"/>
    <circle cx="50" cy="50" r="${pressed ? 23 : 27}" fill="${pressed ? "#ffb547" : "#4a5262"}" stroke="#11141a" stroke-width="3"/></svg>`, "",
    "filter:drop-shadow(0 20px 40px rgba(0,0,0,.6))");
}
/** a top view of a potentiometer knob, pointer at position 0..1 */
function knob(x, y, w, pos = 0.5) {
  const ticks = Array.from({ length: 11 }, (_, i) => { const a = (-225 + 27 * i) * Math.PI / 180; return `<path d="M${100 + 78 * Math.cos(a)} ${100 + 78 * Math.sin(a)} L${100 + 94 * Math.cos(a)} ${100 + 94 * Math.sin(a)}" stroke="#8fa1c0" stroke-width="6" stroke-linecap="round"/>`; }).join("");
  put(x, y, w, w, `<svg width="${w}" height="${w}" viewBox="0 0 200 200">${ticks}<circle cx="100" cy="100" r="68" fill="#c9a24a" stroke="#8a6f2c" stroke-width="4"/>
    <circle cx="100" cy="100" r="52" fill="#2b3140" stroke="#48526a" stroke-width="4"/><g transform="rotate(${-135 + 270 * pos} 100 100)"><rect x="93" y="52" width="14" height="44" rx="7" fill="#ffb547"/></g></svg>`, "",
    "filter:drop-shadow(0 20px 40px rgba(0,0,0,.6))");
}
function resistor(x, y, w) {
  put(x, y, w, w * 0.3, `<svg width="${w}" viewBox="0 0 300 90"><path d="M0 45 H300" stroke="#b8bec6" stroke-width="10" stroke-linecap="round"/>
    <rect x="70" y="8" width="160" height="74" rx="30" fill="#dcc79f" stroke="#b49e72" stroke-width="3"/>
    <rect x="98" y="8" width="16" height="74" fill="#d0262f"/><rect x="128" y="8" width="16" height="74" fill="#d0262f"/><rect x="158" y="8" width="16" height="74" fill="#7a4a21"/><rect x="198" y="8" width="16" height="74" fill="#c9a54a"/></svg>`);
}
function wave(x, y, w, h) {
  let d = `M0 ${h}`; const n = 4, p = w / n;
  for (let i = 0; i < n; i++) d += ` H${i * p + p * 0.15} V0 H${i * p + p * 0.65} V${h}`;
  d += ` H${w}`;
  put(x, y, w, h, `<svg width="${w}" height="${h + 10}" viewBox="-5 -5 ${w + 10} ${h + 10}"><path d="${d}" fill="none" stroke="#ffb547" stroke-width="12" stroke-linejoin="round"/></svg>`);
}
const title = (lines, top = 130, size = 132) => {
  if (L.title) lines = lines.map((ln, i) => [L.title[i] ?? ln[0], ln[1], ln[2]]);
  const t = put(40, top, 720, 0, lines.map(([s, c, extra]) => `<div style="color:${COL[c]};font-size:${size}px;${extra || ""}">${s}</div>`).join(""), "title");
  t.style.top = top + "px";
};
const card = (x, y, w, h, html, extra = "") => put(x, y, w, h, html, "card", extra);
let pillN = 0;
const pill = (x, y, html, bg, fg) => (html = L.pills?.[pillN++] ?? html, put(x, y, 0, 0, `<span class="pill" style="background:${bg};color:${fg}">${html}</span>`, "", "width:auto;height:auto"));
const tx = (s) => L.words?.[s] ?? s;  // other words inside cards

/* ---- localized hooks ---- */
const EP = { en: "EP", tr: "BÖLÜM", hi: "भाग", pt: "EP", es: "EP" };
const LOC = {
  ep08_A: {
    tr: { title: ["ÇUBUĞU", "DOLDUR!"], pills: ["pot → 3 LED · map()"], maxW: 650 },
    hi: { title: ["बार", "भर दो!"], pills: ["knob → 3 LED · map()"], maxW: 650 },
    pt: { title: ["ENCHA", "A BARRA"], pills: ["knob → 3 LEDs · map()"], maxW: 650 },
    es: { title: ["LLENA", "LA BARRA"], pills: ["perilla → 3 LEDs · map()"], maxW: 650 },
  },
  ep08_B: {
    tr: { title: ["SAYIYI", "ÇEVİR!"], maxW: 620 },
    hi: { title: ["रेंज", "बदलो!"], maxW: 620 },
    pt: { title: ["MAPEIE", "QUALQUER FAIXA"], maxW: 620 },
    es: { title: ["MAPEA", "CUALQUIER RANGO"], maxW: 620 },
  },
  ep09_A: {
    tr: { title: ["AKILLI", "YAYA GEÇİDİ"], pills: ["düğme · 4 adım · delay() yok"], maxW: 800 },
    hi: { title: ["स्मार्ट", "पार पथ"], pills: ["button · 4 कदम · delay() नहीं"], maxW: 800 },
    pt: { title: ["FAIXA", "INTELIGENTE"], pills: ["botão · 4 passos · sem delay()"], maxW: 800 },
    es: { title: ["CRUCE", "INTELIGENTE"], pills: ["botón · 4 pasos · sin delay()"], maxW: 800 },
  },
  ep09_B: {
    tr: { title: ["DURUM", "MAKİNESİ"], words: { GREEN: "YEŞİL", YELLOW: "SARI", WALK: "GEÇ", BLINK: "ACELE ET" }, maxW: 630 },
    hi: { title: ["स्टेट", "मशीन"], words: { GREEN: "हरी", YELLOW: "पीली", WALK: "चलिए", BLINK: "जल्दी!" }, maxW: 630 },
    pt: { title: ["MÁQUINA DE", "ESTADOS"], words: { GREEN: "VERDE", YELLOW: "AMARELO", WALK: "ATRAVESSE", BLINK: "PISCA" }, maxW: 630 },
    es: { title: ["MÁQUINA DE", "ESTADOS"], words: { GREEN: "VERDE", YELLOW: "ÁMBAR", WALK: "CRUZA", BLINK: "PARPADEA" }, maxW: 630 },
  },
};
const L = (LOC[key] || {})[lang] || {};
if (lang === "hi") document.documentElement.classList.add("hi");

/* ---- the variants ---- */
const V = {
  ep01_A() { title([["FIRST", "white"], ["UPLOAD!", "amber"]]); board(870, 70, 300, 8); pill(760, 590, "✓ Done uploading", "var(--green)", "#05210f"); },
  ep01_B() {
    title([["ZERO TO", "white"], ["CODE", "teal"]]);
    card(690, 150, 560, 380, `<div style="padding:22px 30px;font:600 22px var(--ui);color:var(--muted)">Serial Monitor</div>
      <div class="code" style="padding-top:0;font-size:30px">Hello, ESP32!\nrunning for 1 s\nrunning for 2 s\nrunning for 3 s</div>`);
  },
  ep01_C() { title([["START", "white"], ["HERE", "amber"]]); board(860, 60, 300, -6); pill(40, 440, "ESP32 for C programmers", "rgba(25,195,180,.18)", "var(--teal)"); },
  ep02_A() {
    title([["DON'T", "white"], ["FRY IT!", "red"]]); board(880, 60, 290, 0);
    for (const [y, t] of [[200, "✕ 5V → GPIO"], [330, "✕ 3V3 → GND"]]) pill(560, y, t, "var(--red)", "#fff");
  },
  ep02_B() {
    title([["WHICH", "white"], ["PINS?", "amber"]]); board(880, 60, 290, 0);
    pill(690, 170, "✓ safe", "var(--green)", "#05210f"); pill(690, 300, "✕ flash", "var(--red)", "#fff"); pill(690, 430, "! strapping", "var(--amber)", "#1d1300");
  },
  ep02_C() { title([["FIRST", "white"], ["CIRCUIT", "teal"]]); led(930, 120, 170); resistor(760, 470, 340); pill(40, 440, "no code needed", "rgba(25,195,180,.18)", "var(--teal)"); },
  ep03_A() {
    title([["BLINK!", "amber"]], 170, 170); led(990, 70, 190);
    card(640, 500, 600, 110, `<div class="code" style="font-size:31px"><span class="fn">digitalWrite</span>(<span class="num">23</span>, HIGH);</div>`);
  },
  ep03_B() { title([["WHY", "white"], ["220 Ω?", "amber"]]); led(1010, 80, 160); resistor(700, 460, 400); },
  ep03_C() { title([["FIRST", "white"], ["CODE", "teal"]]); wave(700, 230, 360, 200); led(1100, 150, 120); pill(700, 500, "on · wait · off · wait", "rgba(255,181,71,.18)", "var(--amber)"); },
  ep04_A() {
    title([["1 PRESS", "white"], ["= 3?!", "red"]]); button(800, 110, 300, true);
    card(760, 470, 420, 100, `<div class="code" style="font-size:40px;text-align:center">presses: <span style="color:var(--red)">3</span></div>`);
  },
  ep04_B() {
    title([["STOP", "white"], ["delay()", "red", "font-family:var(--mono);font-size:110px;letter-spacing:-2px;text-decoration:line-through;text-decoration-thickness:12px"]]);
    card(700, 200, 540, 300, `<div style="padding:40px 36px;text-align:center"><div style="font:800 64px var(--mono)"><span class="fn">millis</span>()</div>
      <div style="font:700 30px var(--ui);color:var(--teal);margin-top:20px">check the clock,<br>don't wait</div></div>`);
  },
  ep04_C() { title([["BUTTONS", "white"], ["+ millis()", "teal", "font-family:var(--mono);font-size:104px;letter-spacing:-2px"]]); button(740, 300, 220); led(1010, 90, 110, "red"); led(1140, 90, 110, "green"); },
  // v2 (2026-10-25, PRODUCTION_GUIDELINES.md): one focus (the working result), 2-3 words
  ep04_D() {
    title([["DO", "white"], ["BOTH!", "teal"]], 150, 176);
    led(800, 60, 150, "red"); led(1050, 60, 150, "green");
    button(880, 400, 230, true);
    pill(780, 640, "blink + button, no delay()", "rgba(25,195,180,.18)", "var(--teal)");
  },
  ep04_E() {
    title([["NEVER", "white"], ["WAIT", "amber"]], 150, 160);
    led(830, 50, 130, "red"); led(1060, 50, 130, "green");
    card(700, 380, 540, 200, `<div style="padding:30px 34px;text-align:center"><div style="font:800 60px var(--mono)"><span class="fn">millis</span>()</div>
      <div style="font:700 28px var(--ui);color:var(--amber);margin-top:14px">not <span style="font-family:var(--mono)">delay()</span></div></div>`);
  },
  // v6: Episode 5 teaches PWM; Episode 6 teaches RGB mixing.
  ep05_A() {
    title([["MAKE IT", "white", "font-size:132px"], ["BREATHE", "amber", "font-size:142px"]], 150, 142);
    led(930, 60, 210, "red");
    wave(760, 525, 430, 80);
    pill(760, 640, "PWM · analogWrite()", "rgba(25,195,180,.18)", "var(--teal)");
  },
  ep05_B() {
    title([["PAUSE", "white"], ["A BREATH", "teal", "font-size:128px"]], 150, 150);
    led(1020, 55, 165, "red");
    button(805, 420, 200, true);
    pill(960, 615, "no delay()", "rgba(255,181,71,.18)", "var(--amber)");
  },
  ep06_A() {
    title([["ANY", "white"], ["COLOR!", "amber"]], 150, 176);
    rgbLed(860, 40, 250, [255, 60, 220]);
    pill(790, 600, "red + green + blue", "rgba(25,195,180,.18)", "var(--teal)");
  },
  ep06_B() {
    title([["MIX", "white"], ["LIGHT", "teal"]], 150, 176);
    rgbLed(890, 45, 240, [255, 230, 20]);
    pill(790, 600, "RED + GREEN = YELLOW", "rgba(255,181,71,.18)", "var(--amber)");
  },
  // Episode 7: the knob. A = the visible result (knob -> light), B = the number in the code.
  ep07_A() {
    title([["TURN", "white"], ["IT UP!", "amber"]], 150, 176);
    knob(740, 180, 300, 0.8);
    led(1080, 90, 170, "red");
    pill(760, 600, "one knob · one line of code", "rgba(25,195,180,.18)", "var(--teal)");
  },
  ep07_B() {
    title([["READ", "white"], ["A KNOB", "teal"]], 150, 150);
    knob(860, 40, 270, 0.5);
    card(700, 370, 540, 120, `<div class="code" style="font-size:44px;text-align:center"><span class="fn">analogRead</span>(<span class="num">34</span>)</div>`);
    card(790, 520, 360, 110, `<div style="font:800 68px/110px var(--mono);text-align:center;color:var(--amber)">2048</div>`);
  },
  // Episode 8: map() and the level bar. A = the visible result (knob fills the bar), B = the one function.
  ep08_A() {
    title([["FILL", "white"], ["THE BAR", "amber"]], 150, 168);
    knob(720, 200, 260, 0.85);
    led(1010, 40, 110, "red"); led(1010, 230, 110, "yellow"); led(1010, 420, 110, "green");
    pill(560, 620, "knob → 3 LEDs · map()", "rgba(25,195,180,.18)", "var(--teal)");
  },
  ep08_B() {
    title([["MAP", "white"], ["ANY RANGE", "teal", "font-size:118px"]], 150, 150);
    card(680, 150, 580, 130, `<div class="code" style="font-size:35px;text-align:center"><span class="fn">map</span>(v, <span class="num">0</span>, <span class="num">4095</span>, <span class="num">0</span>, <span class="num">255</span>)</div>`);
    card(760, 330, 420, 110, `<div style="font:800 60px/110px var(--mono);text-align:center"><span style="color:var(--muted)">2048 →</span> <span style="color:var(--amber)">127</span></div>`);
    knob(780, 470, 170, 0.5); led(1030, 460, 90, "red");
  },
  // Episode 9: mini project 1, the pedestrian crossing. A = the working crossing, B = the idea (one variable holds the step).
  ep09_A() {
    title([["SMART", "white"], ["CROSSING", "amber", "font-size:128px"]], 150, 160);
    led(1150, 40, 95, "red", false); led(1150, 200, 95, "yellow", false); led(1150, 360, 95, "green", false);
    led(1150, 40, 95, "red");
    rgbLed(900, 70, 190, [40, 255, 120]);
    button(870, 400, 190, true);
    pill(560, 620, "button · 4 steps · no delay()", "rgba(25,195,180,.18)", "var(--teal)");
  },
  ep09_B() {
    title([["STATE", "white"], ["MACHINE", "teal"]], 150, 150);
    card(700, 120, 520, 130, `<div class="code" style="font-size:52px;text-align:center;line-height:126px">state = <span class="num">2</span>;</div>`);
    const steps = [["GREEN", "var(--green)"], ["YELLOW", "var(--amber)"], ["WALK", "var(--teal)"], ["BLINK", "var(--red)"]];
    card(700, 290, 520, 300, `<div style="padding:18px 26px;display:grid;gap:12px">${steps.map(([w, c], i) =>
      `<div style="display:flex;align-items:center;gap:18px;padding:4px 14px;border-radius:14px;${i === 2 ? "background:rgba(25,195,180,.22);outline:3px solid var(--teal)" : "opacity:.55"}">
        <span style="font:800 40px var(--mono);color:var(--amber);width:34px">${i}</span><span style="width:26px;height:26px;border-radius:50%;background:${c}"></span>
        <span style="font:800 34px var(--display);white-space:nowrap">${tx(w)}</span></div>`).join("")}</div>`);
  },
  // channel trailer: the promise of the whole course
  trailer_A() {
    title([["LEARN", "white", "font-size:128px"], ["ESP32", "amber", "font-size:176px"], ["FROM ZERO", "white", "font-size:92px"]], 130, 150);
    board(880, 50, 300, -6);
    rgbLed(690, 300, 150, [40, 200, 255]);
  },
  // recap (numberless special, 2026-10-27): one focus = a line of code and the box that remembers (MEMORY)
  recap_A() {
    title([["READ ANY", "white", "font-size:112px"], ["SKETCH", "amber"]], 150, 176);
    card(690, 110, 560, 250, `<div class="code" style="font-size:34px;line-height:1.55"><span class="kw">int</span> seconds = <span class="num">0</span>;
<span style="background:rgba(255,181,71,.25);border-radius:8px;padding:0 8px;margin:0 -8px;display:inline-block">seconds = seconds + <span class="num">1</span>;</span>
<span class="fn">delay</span>(<span class="num">1000</span>);</div>`);
    card(770, 400, 400, 170, `<div style="padding:22px 30px;text-align:center;border:3px solid var(--amber);border-radius:22px;height:100%"><div style="font:700 26px var(--ui);letter-spacing:.14em;color:var(--muted)">MEMORY</div>
      <div style="font:800 56px var(--mono);margin-top:6px">seconds <span style="color:var(--amber)">5</span></div></div>`);
    pill(760, 612, "5 sketches · 1 idea", "rgba(25,195,180,.18)", "var(--teal)");
  },
  recap_B() {
    title([["CODE", "white"], ["MEMORY", "teal"]], 150, 150);
    card(700, 130, 520, 200, `<div class="code" style="font-size:34px"><span class="kw">int</span> lastState = HIGH;
<span class="kw">bool</span> ledOn = <span class="kw">false</span>;
<span class="kw">int</span> presses = <span class="num">0</span>;</div>`);
    card(700, 380, 520, 210, `<div style="padding:20px 28px;font:800 44px/1.45 var(--mono)">lastState <span style="color:var(--amber);float:right">LOW</span><br>ledOn <span style="color:var(--amber);float:right">true</span><br>presses <span style="color:var(--amber);float:right">1</span></div>`);
    pill(740, 618, "how a sketch remembers", "rgba(255,181,71,.18)", "var(--amber)");
  },
  ep04_F() {
    title([["PRESS", "white"], ["= INSTANT", "red", "font-size:118px"]], 150, 150);
    button(760, 300, 250, true);
    led(1070, 80, 140, "red", false); led(1070, 420, 110, "green");
    pill(1010, 330, "stops", "var(--red)", "#fff");
  },
};

put(null, null, 0, 0, `${LOGOS.A().replace("<svg ", '<svg width="46" height="46" ')}<span>ESP32 From Zero</span>`, "brand", "width:auto;height:auto");
put(null, null, 0, 0, key.startsWith("recap") ? "RECAP" : key.startsWith("trailer") ? "FREE COURSE" : `${EP[lang]} ${Number(key.slice(2, 4))}`, "ep", "width:auto;height:auto");
V[key]();
if (LOC[key]) {  // shrink any title line (any language) that runs into the picture
  const maxW = L.maxW ?? LOC[key].tr?.maxW ?? 640;
  for (const d of T.querySelectorAll(".title div")) {
    d.style.width = "max-content";
    let f = parseFloat(getComputedStyle(d).fontSize);
    while (d.offsetWidth > maxW && f > 40) d.style.fontSize = (f -= 3) + "px";
  }
}
window.__keys = Object.keys(V).flatMap((k) => (LOC[k] ? [k, ...LANGS.filter((l) => LOC[k][l]).map((l) => `${k}_${l}`)] : [k]));
window.__ready = true;
