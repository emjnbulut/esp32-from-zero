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
const COL = { white: "var(--text)", amber: "var(--amber)", teal: "var(--teal)", red: "var(--red)", green: "var(--green)" };

/* ---- pictures ---- */
let gid = 0;
function led(x, y, w, color = "red", lit = true) {
  const col = color === "red" ? ["#ff8a8f", "#d4202c", "#b51d27", "rgba(255,70,70,.95)", "#ffe3e3"] : ["#8af5b0", "#1fae55", "#178a3a", "rgba(60,240,120,.9)", "#e3ffec"];
  const id = "g" + gid++;
  if (lit) put(x - w * 1.1, y - w * 1.0, w * 3.2, w * 3.2, "", "", `border-radius:50%;background:radial-gradient(circle, ${col[3]} 0%, rgba(0,0,0,0) 62%)`);
  put(x, y, w, w * 230 / 120, `<svg width="${w}" viewBox="0 0 120 230"><defs><radialGradient id="${id}" cx=".4" cy=".35"><stop offset="0" stop-color="${col[0]}"/><stop offset="1" stop-color="${col[1]}"/></radialGradient></defs>
    <path d="M44 96 V226" stroke="#c3c9d1" stroke-width="7" stroke-linecap="round"/><path d="M76 96 V186" stroke="#c3c9d1" stroke-width="7" stroke-linecap="round"/>
    <path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="url(#${id})"/>${lit ? `<path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="${col[4]}" opacity=".75"/>` : ""}
    <path d="M22 92 h70 v14 h-70 z" fill="${col[2]}"/></svg>`);
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
  const t = put(40, top, 720, 0, lines.map(([s, c, extra]) => `<div style="color:${COL[c]};font-size:${size}px;${extra || ""}">${s}</div>`).join(""), "title");
  t.style.top = top + "px";
};
const card = (x, y, w, h, html, extra = "") => put(x, y, w, h, html, "card", extra);
const pill = (x, y, html, bg, fg) => put(x, y, 0, 0, `<span class="pill" style="background:${bg};color:${fg}">${html}</span>`, "", "width:auto;height:auto");

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
  ep04_F() {
    title([["PRESS", "white"], ["= INSTANT", "red", "font-size:118px"]], 150, 150);
    button(760, 300, 250, true);
    led(1070, 80, 140, "red", false); led(1070, 420, 110, "green");
    pill(1010, 330, "stops", "var(--red)", "#fff");
  },
};

const key = location.search.slice(1);
put(null, null, 0, 0, `${LOGOS.A().replace("<svg ", '<svg width="46" height="46" ')}<span>ESP32 From Zero</span>`, "brand", "width:auto;height:auto");
put(null, null, 0, 0, `EP ${Number(key.slice(2, 4))}`, "ep", "width:auto;height:auto");
V[key]();
window.__keys = Object.keys(V);
window.__ready = true;
