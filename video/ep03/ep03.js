/* Episode 3 - Your First Circuit: Blink an LED. All times come from the narration schedule. */
const stage = $("#stage");
const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const hidden = (e) => { gsap.set(e, { opacity: 0 }); return e; };
function head(parent, html, y = 70) {
  const h = box(parent, 0, y, 1920, 80, "h2", html);
  h.style.textAlign = "center";
  return hidden(h);
}
/** text panel whose content follows a schedule, fading in on every change: list = [[t, html], ...] */
function panelAt(e, list, rise = 12) {
  dyn((t) => {
    let i = 0;
    for (let k = 0; k < list.length; k++) if (t >= list[k][0]) i = k;
    const [ts, html] = list[i];
    if (e.__v !== html) { e.innerHTML = html; e.__v = html; }
    const k = t < ts ? 0 : Math.min(1, (t - ts) / 0.3);
    e.style.opacity = html ? String(k) : "0";
    e.style.transform = `translateY(${(1 - k) * rise}px)`;
  });
}
let ledN = 0;
/** side-view LED with a glow behind it; returns {r, glow, setOn(list of [t, 0..1])} */
function ledIcon(parent, x, y, w = 110) {
  const id = "lg" + ledN++;
  const r = box(parent, x, y, w, w * 230 / 120, "");
  const glow = box(r, -w * 0.75, -w * 0.7, w * 2.5, w * 2.5, "");
  css(glow, { borderRadius: "50%", background: "radial-gradient(circle, rgba(255,90,90,.9) 0%, rgba(255,50,50,.45) 30%, rgba(255,40,40,0) 65%)", opacity: 0 });
  r.insertAdjacentHTML("beforeend", `<svg width="${w}" viewBox="0 0 120 230" style="position:absolute;left:0;top:0"><defs><radialGradient id="${id}" cx=".4" cy=".35"><stop offset="0" stop-color="#ff8a8f"/><stop offset="1" stop-color="#d4202c"/></radialGradient></defs>
    <path d="M44 96 V226" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/><path d="M76 96 V186" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/>
    <path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="url(#${id})" opacity=".95"/><path class="hot" d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="#ffe0e0" opacity="0"/>
    <path d="M22 92 h70 v14 h-70 z" fill="#b51d27"/></svg>`);
  const hot = $(".hot", r);
  /** brightness as a function of time */
  const drive = (fn) => dyn((t) => { const v = fn(t); glow.style.opacity = v; hot.setAttribute("opacity", v * 0.75); });
  return { r, glow, drive };
}
/** square-wave blink: on for `on` s, off for `off` s, starting at t0 */
const blink = (t, t0, on, off) => (t < t0 ? 0 : ((t - t0) % (on + off)) < on ? 1 : 0);

/* ======================================================================
 * INTRO (s01-s02)
 * ==================================================================== */
const sIntro = SC();
SET(sIntro, 0, { opacity: 1 });
{
  const kick = box(sIntro, 140, 300, 600, 40, "kicker", "Episode 03");
  const title = box(sIntro, 136, 336, 1000, 140, "h1", "ESP32 From Zero");
  title.style.fontSize = "112px";
  const sub = box(sIntro, 140, 486, 1000, 60, "h3", "Your First Circuit: Blink an LED");
  sub.style.color = "var(--teal)";
  const persp = box(sIntro, 1130, 70, 560, 900, "");
  persp.style.perspective = "1600px";
  const b3d = box(persp, 0, 0, 560, 900, "", boardSVG({ pins: 30, chip: "cp2102", p: "bi", width: 520 }));
  css(b3d, { filter: "drop-shadow(0 40px 60px rgba(0,0,0,.6)) drop-shadow(0 0 40px rgba(25,195,180,.25))" });
  gsap.set(b3d, { rotationY: -28, rotationX: 18, y: 60, opacity: 0 });
  TO(b3d, 0.3, 1.6, { opacity: 1, y: 0, ease: "power3.out" });
  TO(b3d, 0.3, 20, { rotationY: 12, rotationX: 8, ease: "sine.inOut" });
  for (const [e, t] of [[kick, 0.5], [title, 0.75], [sub, 1.1]]) {
    gsap.set(e, { opacity: 0, y: 30 });
    TO(e, t, 0.8, { opacity: 1, y: 0, ease: "power3.out" });
  }
  const items = [["Move one wire", "3V3 → GPIO 23"], ["A short program", "pinMode, digitalWrite"], ["Blink!", "on, wait, off, wait"]];
  ["move", "program", "blink"].forEach((w, i) => {
    const c = box(sIntro, 140 + i * 330, 600, 300, 140, "card", `<div style="padding:22px 24px"><div class="kicker" style="font-size:16px">Today · ${i + 1}</div>
      <div style="font:600 29px var(--display);margin-top:8px">${items[i][0]}</div><div class="muted" style="font-size:19px;margin-top:4px">${items[i][1]}</div></div>`);
    hidden(c); pop(c, W("s02", w));
  });
  sceneOut(sIntro, S1("s02") + 0.4);
}

/* ======================================================================
 * BREADBOARD: recap (s03) and moving the wire (s09-s12)
 * ==================================================================== */
const BBX = 290, BBY = 236;
const sBB = SC();
sceneIn(sBB, S1("s02") + 0.4);
sceneOut(sBB, S1("s03") + 0.4);
sceneIn(sBB, S1("s08") + 0.4);
sceneOut(sBB, S1("s12") + 0.5);
{
  const hd = box(sBB, 0, 70, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s03"), "The circuit from last time"], [T("s09"), "Move one wire"], [T("s12"), "Power from GPIO 23"]]);
  const bb = makeBB(sBB, BBX, BBY);
  bbBoard(bb, 30, 2);
  // the finished circuit from episode 2 (already in place when the scene appears)
  const red0 = bbWire(bb, bb.L(2, "j"), bb.L(2, "bp"), "#ff5d6c", 0, 0.35);
  bbWire(bb, bb.L(3, "j"), bb.L(3, "bm"), "#2b2f36", 0, -0.35);
  bbResistor(bb, bb.L(20, "bp"), bb.L(20, "h"));
  const led = bbLED(bb, bb.L(20, "f"), bb.L(21, "f"), -1);
  bbWire(bb, bb.L(21, "j"), bb.L(21, "bm"), "#2b2f36", 0, -0.35);
  gsap.set(bb.strips, { opacity: 1 });
  for (let c = 1; c <= 30; c++) bb.colStrip[c].forEach((e) => e.setAttribute("opacity", 0));
  // LED on during the recap, off once the USB cable is unplugged (and it stays dark)
  SET(led.glow, 0, { opacity: 1 }); SET(led.lit, 0, { opacity: 0.85 });
  TO(led.glow, W("s09", "unplug") + 0.2, 0.3, { opacity: 0 }); TO(led.lit, W("s09", "unplug") + 0.2, 0.3, { opacity: 0 });
  // USB status badge
  const usb = box(sBB, 70, 80, 0, 0, "badge", "");
  css(usb, { width: "auto", height: "auto", background: "rgba(11,18,32,.9)", border: "1px solid var(--line)" });
  panelAt(usb, [[0, `<span style="color:var(--green)">● USB plugged in</span>`], [W("s09", "unplug"), `<span style="color:var(--red)">● USB unplugged</span>`],
    [W("s12", "Plug"), `<span style="color:var(--green)">● USB plugged in</span>`]], 0);
  // s03: the current's path
  const pts = [bb.L(2, "i"), bb.L(2, "j"), bb.L(2, "bp"), bb.L(20, "bp"), bb.L(20, "h"), bb.L(20, "f"), [led.cx, led.cy], bb.L(21, "f"),
    bb.L(21, "j"), bb.L(21, "bm"), bb.L(3, "bm"), bb.L(3, "j"), bb.L(3, "i")];
  const loop = svgEl(bb.over, "path", { d: "M" + pts.map((p) => p.join(" ")).join(" L"), fill: "none", stroke: "#ffb547", "stroke-width": 6, "stroke-linejoin": "round", opacity: 0.9 });
  drawOn(loop, W("s03", "goes"), 2.2);
  TO(loop, S1("s03"), 0.3, { opacity: 0 });
  const p3 = bb.S(2, "i"), p23 = bb.S(16, "i");
  callout(sBB, "3V3", p3[0] - 30, p3[1] - 72, W("s03", "three"), S1("s03"));
  // s10: the red wire, its 3V3 end moves to the D23 column
  const glowW = svgEl(bb.over, "path", { d: `M${bb.L(2, "j").join(" ")} L${bb.L(2, "bp").join(" ")}`, stroke: "#ffd34d", "stroke-width": 22, "stroke-linecap": "round", fill: "none", opacity: 0 });
  TO(glowW, W("s10", "red"), 0.3, { opacity: 0.55 }); TO(glowW, W("s10", "Pull"), 0.3, { opacity: 0 });
  callout(sBB, "3V3", p3[0] - 30, p3[1] - 72, W("s10", "three"), W("s10", "plug"));
  hide(red0, W("s10", "Pull") + 0.15, 0.25);
  const [jx, jy] = bb.L(2, "j"), [kx] = bb.L(16, "j");
  const tip = svgEl(bb.over, "rect", { x: jx - 9, y: jy - 9, width: 18, height: 18, rx: 3, fill: "#ff5d6c", stroke: "#222", "stroke-width": 3, opacity: 0 });
  SET(tip, W("s10", "Pull") + 0.15, { opacity: 1 });
  TO(tip, W("s10", "Pull") + 0.2, W("s10", "plug") - W("s10", "Pull"), { attr: { x: kx - 9 }, ease: "power2.inOut" });
  SET(tip, W("s10", "plug") + 0.5, { opacity: 0 });
  // the other end stays in the + rail, so the wire follows the moving tip (same curve as the final wire)
  const [px, py] = bb.L(2, "bp"), mv0 = W("s10", "Pull") + 0.15, mv1 = W("s10", "plug") + 0.6;
  const live = svgEl(bb.parts, "path", { fill: "none", stroke: "#ff5d6c", "stroke-width": 10, "stroke-linecap": "round", opacity: 0 });
  dyn((t) => {
    const on = t >= mv0 && t < mv1;
    live.setAttribute("opacity", on ? 1 : 0);
    if (!on) return;
    const ex = +tip.getAttribute("x") + 9, dx = px - ex, dy = py - jy;
    live.setAttribute("d", `M${ex} ${jy} Q${(ex + px) / 2 - dy * 0.08} ${(jy + py) / 2 + dx * 0.08} ${px} ${py}`);
  });
  bbWire(bb, bb.L(16, "j"), bb.L(2, "bp"), "#ff5d6c", W("s10", "plug"), 0.08);
  const c16 = bb.colStrip[16][1];
  TO(c16, W("s10", "column"), 0.4, { opacity: 0.6 }); TO(c16, S1("s11"), 0.4, { opacity: 0 });
  callout(sBB, "D23 = GPIO 23", p23[0] - 80, p23[1] - 72, W("s10", "twentythree"), S1("s11") + 0.2);
  const safe = box(sBB, 380, 160, 0, 0, "badge", "✓&nbsp; a safe pin from episode 2");
  css(safe, { width: "auto", height: "auto", background: "var(--green)", color: "#05210f" }); hidden(safe);
  pop(safe, W("s11", "safe")); hide(safe, S1("s11") + 0.2);
  const p38 = box(sBB, 1000, 160, 0, 0, "badge", "38-pin board: the label is “23”");
  css(p38, { width: "auto", height: "auto", background: "rgba(11,18,32,.92)", border: "1px solid var(--line)", color: "var(--ink, #e8eef7)" }); hidden(p38);
  pop(p38, W("s11", "thirtyeight")); hide(p38, S1("s11") + 0.2);
  clipFrame(sBB, "C1", 1140, 150, 720, 405, W("s10", "Pull") - 0.2, S1("s10") + 1.2, "USB unplugged: move the red wire's end from 3V3 to the D23 column.");
  // s12: powered from GPIO 23, but dark
  const path2 = [bb.L(16, "i"), bb.L(16, "j"), bb.L(2, "bp"), bb.L(20, "bp"), bb.L(20, "h"), bb.L(20, "f"), [led.cx, led.cy]];
  const feed = svgEl(bb.over, "path", { d: "M" + path2.map((p) => p.join(" ")).join(" L"), fill: "none", stroke: "#19c3b4", "stroke-width": 6, "stroke-linejoin": "round", opacity: 0.9 });
  drawOn(feed, W("s12", "power"), 1.2);
  TO(feed, W("s12", "Plug"), 0.3, { opacity: 0 });
  const pl = bb.S(20, "f");
  callout(sBB, "dark: GPIO 23 isn't switched on yet", pl[0] - 180, pl[1] + 60, W("s12", "dark"), S1("s12") + 0.4);
}

/* ======================================================================
 * WHY 220 OHMS (s04-s08)
 * ==================================================================== */
const sOhm = SC();
sceneIn(sOhm, S1("s03") + 0.4);
sceneOut(sOhm, S1("s08") + 0.4);
{
  const h = head(sOhm, "Why 220 Ω?", 80); show(h, T("s04"));
  const q = box(sOhm, 0, 380, 1920, 200, "", `<div style="text-align:center;font:700 150px var(--display);color:var(--amber)">220 Ω ?</div>`);
  hidden(q); pop(q, W("s04", "Why")); hide(q, T("s05") - 0.1, 0.3);
  // s05: Ohm's law
  const law = box(sOhm, 0, 200, 1920, 200, "", `<div style="display:flex;justify-content:center;gap:40px;font:700 120px var(--mono)">
    <span class="lI" style="color:var(--teal)">I</span><span>=</span><span class="lV" style="color:var(--amber)">V</span><span>/</span><span class="lR" style="color:#d8c38f">R</span></div>`);
  hidden(law); pop(law, W("s05", "law"));
  const lab = [["current (A)", "current", ".lI"], ["voltage (V)", "voltage", ".lV"], ["resistance (Ω)", "resistance", ".lR"]];
  for (const [txt, w, sel] of lab) {
    const x = rect($(sel, law)).cx;
    const l = box(sOhm, x - 150, 410, 300, 50, "muted", `<div style="text-align:center;font-size:30px">${txt}</div>`);
    hidden(l); pop(l, W("s05", w)); hide(l, T("s06") - 0.1, 0.3);
  }
  TO(law, T("s06") - 0.2, 0.5, { y: -70, scale: 0.6 });
  // s06: where the 3.3 V goes
  const BX = 360, BW = 1200, BY = 470;
  const tot = box(sOhm, BX, BY - 70, BW, 50, "", `<div style="text-align:center;font:600 34px var(--display)">3.3 V from the pin</div>`);
  hidden(tot); pop(tot, W("s06", "three"));
  const segLED = box(sOhm, BX, BY, BW * 2 / 3.3, 110, "", `<div style="height:100%;border-radius:18px 0 0 18px;background:rgba(255,93,108,.85);display:flex;align-items:center;justify-content:center;font:700 40px var(--display);color:#2a0006">LED ≈ 2 V</div>`);
  const segR = box(sOhm, BX + BW * 2 / 3.3, BY, BW * 1.3 / 3.3, 110, "", `<div style="height:100%;border-radius:0 18px 18px 0;background:#ffb547;display:flex;align-items:center;justify-content:center;font:700 40px var(--display);color:#2a1b00">resistor ≈ 1.3 V</div>`);
  hidden(segLED); hidden(segR);
  pop(segLED, W("s06", "two")); pop(segR, W("s06", "one"));
  // s07: the current
  const calc = box(sOhm, 0, 690, 1920, 120, "", `<div style="display:flex;justify-content:center;gap:28px;font:700 76px var(--display)">
    <span class="c1">1.3 V</span><span class="c2">÷ 220 Ω</span><span class="c3" style="color:var(--teal)">≈ 6 mA</span></div>`);
  const [c1, c2, c3] = [".c1", ".c2", ".c3"].map((s) => $(s, calc));
  gsap.set([c1, c2, c3], { opacity: 0 });
  TO(c1, T("s07"), 0.3, { opacity: 1 }); TO(c2, W("s07", "divided"), 0.3, { opacity: 1 }); TO(c3, W("s07", "six"), 0.35, { opacity: 1 });
  const ok = box(sOhm, 0, 840, 1920, 60, "", `<div style="display:flex;justify-content:center;gap:20px"><span class="pill" style="font-size:28px">✓ easy to see</span><span class="pill" style="font-size:28px">✓ easy on the GPIO pin</span></div>`);
  hidden(ok); pop(ok, W("s07", "GPIO"));
  hide([tot, segLED, segR, calc, ok, law], T("s08") - 0.1, 0.35);
  // s08: no resistor / bigger resistor
  const opts = [["no resistor", "✕ too much current", 0, "Without"], ["220 Ω", "bright", 1, "bigger"], ["470 Ω", "dimmer", 0.6, "bigger"], ["1 kΩ", "dimmer still", 0.3, "bigger"]];
  opts.forEach(([nm, ds, v, w], i) => {
    const x = 250 + i * 390;
    const c = box(sOhm, x, 260, 330, 520, "card", `<div style="position:absolute;bottom:34px;left:0;right:0;text-align:center"><div style="font:700 40px var(--display)">${nm}</div>
      <div style="font-size:24px;margin-top:6px;color:${i ? "var(--muted)" : "var(--red)"}">${ds}</div></div>`);
    hidden(c); pop(c, W("s08", w) + (i > 1 ? (i - 1) * 0.35 : 0));
    const L = ledIcon(c, 110, 60, 110);
    if (i === 0) {
      L.drive((t) => { const t0 = W("s08", "Without") + 0.4; return t < t0 ? 0 : t < t0 + 0.6 ? 1 : 0; });
      const x2 = box(c, 70, 40, 190, 190, "", `<div style="font:800 170px var(--ui);color:var(--red);line-height:190px;text-align:center">✕</div>`);
      hidden(x2); pop(x2, W("s08", "Without") + 1.0);
    } else L.drive(() => v);
  });
  const range = box(sOhm, 0, 840, 1920, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:32px">✓ anything from 220 Ω to 1 kΩ works</span></div>`);
  hidden(range); pop(range, W("s08", "Anything"));
}

/* ======================================================================
 * ARDUINO IDE: code (s13-s20), upload and Serial Monitor (s21-s24)
 * ==================================================================== */
const DK = buildDesktop(stage);
const camera = DK.camera;
initCamera(camera);
initCursor(camera);
sceneIn(DK.desk, S1("s12") + 0.5);
sceneOut(DK.desk, S1("s24") + 0.5);
const ide = buildIDE(camera);
ide.boardText.textContent = "ESP32 Dev Module";
ide.statusBoard.textContent = "ESP32 Dev Module on COM3";
const DEFAULT_SKETCH = "void setup() {\n  // put your setup code here, to run once:\n\n}\n\nvoid loop() {\n  // put your main code here, to run repeatedly:\n\n}\n";
const SKETCH = `// ESP32 From Zero - Episode 3: Blink an LED
// GPIO 23 -> 220 ohm resistor -> LED -> GND

const int LED_PIN = 23;        // the GPIO our LED is wired to

void setup() {
  pinMode(LED_PIN, OUTPUT);    // our code drives this pin
  Serial.begin(115200);
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // 3.3 V -> LED on
  Serial.println("LED on");
  delay(500);                  // half a second

  digitalWrite(LED_PIN, LOW);  // 0 V -> LED off
  Serial.println("LED off");
  delay(500);
}
`;
const lineY = (i) => IDE.codeTop + i * IDE.lineH;
const cx = (col) => IDE.codeX + col * IDE.charW;
pop(ide.w, T("s13") - 0.3, 0.45);
{
  const s13 = "s13";
  const tSel = W(s13, "new") + 0.1, tDel = W(s13, "sketch") + 0.3;
  const selFlash = box(camera, 120, lineY(0), 520, 22 * 9, "");
  css(selFlash, { background: "rgba(38,79,120,.85)", opacity: 0 });
  SET(selFlash, tSel, { opacity: 1 }); SET(selFlash, tDel, { opacity: 0 });
  const keys = box(stage, 760, 900, 400, 70, "", "");
  css(keys, { zIndex: 55, textAlign: "center" }); hidden(keys);
  textAt(keys, [[0, ""], [tSel - 0.1, `<span class="pill" style="font-size:30px;background:#1b2430;color:#fff">Ctrl + A &nbsp;→&nbsp; Delete</span>`],
    [W("s21", "Save") - 0.1, `<span class="pill" style="font-size:30px;background:#1b2430;color:#fff">Ctrl + S</span>`]]);
  show(keys, tSel - 0.1, 0.2); hide(keys, tDel + 0.6, 0.2);
  show(keys, W("s21", "Save") - 0.1, 0.2); hide(keys, W("s21", "Check"), 0.2);
  cam(tDel, 1.2, 520, 300, 1.8);
  const pieces = [
    ["// ESP32 From Zero - Episode 3: Blink an LED\n// GPIO 23 -> 220 ohm resistor -> LED -> GND\n\n", tDel + 0.3, T("s14") + 0.3],
    ["const int LED_PIN = 23;        // the GPIO our LED is wired to\n\n", T("s14") + 0.5, W("s14", "If")],
    ["void setup() {\n", T("s15") + 0.1, T("s15") + 0.8],
    ["  pinMode(LED_PIN, OUTPUT);    // our code drives this pin\n", T("s15") + 0.9, W("s15", "OUTPUT")],
    ["  Serial.begin(115200);\n}\n\n", T("s16") + 0.4, S1("s16")],
    ["void loop() {\n  digitalWrite(LED_PIN, HIGH); // 3.3 V -> LED on\n", T("s17") + 0.2, W("s17", "puts")],
    ["  Serial.println(\"LED on\");\n  delay(500);                  // half a second\n\n", T("s18") + 0.1, S1("s18")],
    ["  digitalWrite(LED_PIN, LOW);  // 0 V -> LED off\n", T("s19") + 0.1, W("s19", "LOW", 2)],
    ["  Serial.println(\"LED off\");\n  delay(500);\n}\n", W("s19", "print"), S1("s19")],
  ];
  let all = "";
  const times = [];
  pieces.forEach(([txt, a, b], i) => {
    const cps = Math.min(40, Math.max(9, txt.length / Math.max(0.6, b - a)));
    const tt = typingTimes(txt, a, cps, 21 + i);
    all += txt; times.push(...tt);
  });
  if (all !== SKETCH) console.warn("typed text differs from SKETCH");
  dyn((t) => {
    if (t < T(s13) - 0.5) return;
    const n = t < tDel ? -1 : countAt(times, t);
    if (n < 0) { renderCode(ide.code, DEFAULT_SKETCH, DEFAULT_SKETCH.length, false, 10); return; }
    const on = Math.floor(t * 1.9) % 2 === 0 || (n > 0 && n < all.length && t - times[n - 1] < 0.5);
    renderCode(ide.code, all, n, on && t < T("s21"), 1);
    const lines = all.slice(0, n).split("\n");
    ide.statusLC.textContent = `Ln ${lines.length}, Col ${lines[lines.length - 1].length + 1}`;
  });
  // explanations
  ring(camera, cx(0) - 4, lineY(3) - 1, cx(23) - cx(0) + 8, 24, W("s14", "constant"), W("s14", "If") + 0.4);
  callout(camera, "change it here if the wire moves", cx(31), lineY(3) + 30, W("s14", "change"), S1("s14") + 0.3);
  ring(camera, cx(2) - 4, lineY(6) - 1, cx(27) - cx(2) + 8, 24, W("s15", "OUTPUT") + 0.1, S1("s15") + 0.3);
  callout(camera, "OUTPUT = our code drives the pin", cx(2), lineY(6) + 30, W("s15", "OUTPUT"), S1("s15") + 0.3);
  ring(camera, cx(2) - 4, lineY(11) - 1, cx(30) - cx(2) + 8, 24, W("s17", "puts") + 0.1, S1("s17") + 0.2);
  callout(camera, "HIGH = 3.3 V on the pin", cx(50), lineY(11) - 4, W("s17", "puts") + 0.1, S1("s17") + 0.2);
  callout(camera, "500 ms = ½ second", cx(16), lineY(13) + 30, W("s18", "five"), S1("s18") + 0.2);
  ring(camera, cx(2) - 4, lineY(15) - 1, cx(29) - cx(2) + 8, 24, W("s19", "means"), W("s19", "print"));
  callout(camera, "LOW = 0 V", cx(50), lineY(15) - 4, W("s19", "zero"), S1("s19") + 0.2);
  ring(camera, 112, lineY(11) - 4, 560, 7 * 22 + 8, W("s20", "runs"), S1("s20") + 0.3);
  callout(camera, "↻ loop() repeats forever: on · wait · off · wait", 120, lineY(18) + 34, W("s20", "forever"), S1("s20") + 0.3);
}
{
  // s21: save, check board + port, upload
  const s21 = "s21", s22 = "s22", s23 = "s23", s24 = "s24";
  const tSave = W(s21, "Save") + 0.3;
  textAt(ide.tab, [[0, "sketch_oct17a.ino"], [tSave, "blink_led.ino"]]);
  textAt(ide.title, [[0, "sketch_oct17a | Arduino IDE 2.3.10"], [tSave, "blink_led | Arduino IDE 2.3.10"]]);
  camReset(W(s21, "Check") - 0.3, 0.9);
  ring(camera, 132, 61, 240, 36, W(s21, "ESP32"), W(s21, "Upload") - 0.3);
  const sb = rect(ide.statusBoard);
  ring(camera, sb.x - 8, sb.y - 4, sb.w + 16, sb.h + 8, W(s21, "COM"), W(s21, "Upload") - 0.3);
  clickAt(IDE.upload.x, IDE.upload.y, W(s21, "Upload"), 0.9);
  const u0 = W(s21, "Upload") + 0.1;
  cam(u0 + 0.5, 1.1, 560, 880, 1.7);
  const tConn = W(s22, "Connecting") - 0.3, tGo = W(s22, "BOOT") + 0.6, tW = tGo + 0.9;
  const tW1 = Math.max(tW + 1.2, T(s23) - 0.4), tHR = tW1 + 0.25;
  textAt(ide.toastText, [[0, ""], [u0, "Compiling sketch..."], [tConn - 0.5, "Uploading..."], [tHR + 0.3, "Done uploading."]]);
  SET(ide.toastBar, u0 - 0.01, { width: "0%" });
  show(ide.toast, u0, 0.2); TO(ide.toastBar, u0, tHR - u0, { width: "100%", ease: "none" }); hide(ide.toast, S1(s23) + 0.5, 0.3);
  const dots = (dt) => "Connecting" + ".".repeat(1 + Math.floor(dt * 4) % 60).replace(/(.{5})/g, "$1_");
  const bar = (p) => { const n = Math.round(p * 30); return `Writing at 0x000${(0x10000 + Math.floor(p * 153842)).toString(16)} [${"=".repeat(Math.max(0, n - 1))}${n ? ">" : ""}${" ".repeat(30 - n)}] ${(p * 100).toFixed(1).padStart(5)}% ${Math.floor(p * 153842)}/153842 bytes...`; };
  logLines(ide.out, [
    [u0 + 0.6, ""],
    [u0 + 1.6, "Sketch uses 271672 bytes (20%) of program storage space. Maximum is 1310720 bytes."],
    [u0 + 1.7, "Global variables use 22116 bytes (6%) of dynamic memory, leaving 305564 bytes for local variables. Maximum is 327680 bytes."],
    [tConn - 0.6, "esptool v5.1.0"], [tConn - 0.4, "Serial port COM3:"],
    [tConn, (dt) => (dt < tGo - tConn ? dots(dt) : dots(tGo - tConn))],
    [tGo + 0.1, "Connected to ESP32 on COM3:"], [tGo + 0.3, "Chip type:          ESP32-D0WD-V3 (revision v3.1)"],
    [tGo + 0.6, "Uploading stub flasher..."], [tGo + 0.8, "Configuring flash size..."],
    [tW, (dt) => bar(Math.min(1, dt / (tW1 - tW)))],
    [tW1 + 0.1, "Hash of data verified."],
    [tHR, '<span style="color:#0ca1a6">Hard resetting via RTS pin...</span>'],
  ], 8, [u0 - 0.5, 1e9]);
  callout(camera, "stuck here? hold BOOT (episode 1)", 330, IDE.outTop + 4, W(s22, "BOOT"), S1(s22) + 0.6);
  // s23: the LED blinks (creator clip) - plus a little LED on screen in case
  clipFrame(stage, "C2", 1140, 90, 720, 405, W(s23, "there") - 0.2, S1(s23) + 1.8, "The LED blinking once per second.");
  // s24: Serial Monitor
  camReset(S1(s23) + 0.5, 0.9);
  clickAt(IDE.monitor.x, IDE.monitor.y, W(s24, "Serial"), 0.9);
  const tOpen = W(s24, "Serial") + 0.1;
  const o1 = $(".o1", ide.btabs), o2 = $(".o2", ide.btabs);
  styleAt(o2, "display", [[0, "none"], [tOpen, "flex"]]);
  dyn((t) => { o1.className = t >= tOpen ? "o1" : "on o1"; o2.className = t >= tOpen ? "on o2" : "o2"; });
  styleAt(ide.out, "display", [[0, "block"], [tOpen, "none"]]);
  styleAt(ide.serial, "display", [[0, "none"], [tOpen, "block"]]);
  cam(tOpen + 0.3, 1.0, 640, 900, 1.7);
  const tStart = tHR + 0.4;
  dyn((t) => {
    if (t < tOpen) return;
    const k = Math.floor((t - tStart) / 0.5);
    const lines = [];
    for (let i = Math.max(0, k - 5); i <= k; i++) lines.push(i % 2 === 0 ? "LED on" : "LED off");
    const html = `<div style="display:flex;gap:12px;align-items:center;margin:-2px 0 8px;font-family:var(--ui)"><div class="ide-in" style="flex:1;color:#888">Message (Enter to send message to 'ESP32 Dev Module' on 'COM3')</div>
      <div class="ide-in" style="width:110px">New Line ▾</div><div class="ide-in" style="width:130px;${t >= W(s24, "115200") - 0.3 && t < W(s24, "115200") + 1.5 ? "border-color:#ffb547" : ""}">115200 baud ▾</div></div>` +
      lines.map((l) => `<div>${l}</div>`).join("");
    if (ide.serial.__v !== html) { ide.serial.innerHTML = html; ide.serial.__v = html; }
  });
  // a small "live" LED next to the monitor, in step with the printed lines
  const live = box(stage, 1660, 90, 200, 330, "card", "");
  css(live, { zIndex: 50 }); hidden(live); show(live, W(s24, "report") - 0.3, 0.3); hide(live, S1(s24) + 0.5, 0.4);
  const L = ledIcon(live, 45, 60, 110);
  L.drive((t) => blink(t, tStart, 0.5, 0.5));
}

/* ======================================================================
 * THE SQUARE WAVE (s25)
 * ==================================================================== */
const sWave = SC();
sceneIn(sWave, S1("s24") + 0.5);
sceneOut(sWave, S1("s25") + 0.4);
{
  const h = head(sWave, "What the pin does", 90); show(h, T("s25"));
  const X0 = 300, X1 = 1450, YH = 380, YL = 720, PX = 230; // 230 px per second
  const sv = svgLayer(sWave);
  for (const [y, txt, col] of [[YH, "3.3 V  HIGH", "#19c3b4"], [YL, "0 V  LOW", "#8fa1c0"]]) {
    svgEl(sv, "path", { d: `M${X0} ${y} H${X1}`, stroke: "#22304d", "stroke-width": 2, "stroke-dasharray": "8 8" });
    svgEl(sv, "text", { x: X0 - 24, y: y + 12, "text-anchor": "end", "font-family": "Segoe UI", "font-weight": 700, "font-size": 34, fill: col }).textContent = txt;
  }
  const wave = svgEl(sv, "path", { fill: "none", stroke: "#ffb547", "stroke-width": 8, "stroke-linejoin": "round" });
  const tick = svgEl(sv, "g", {});
  const t0 = T("s25") + 0.2;
  dyn((t) => {
    if (t < t0 - 0.5 || t > S1("s25") + 0.5) return;
    // newest sample at the right edge, the wave scrolls left
    const now = Math.max(0, t - t0), span = (X1 - X0) / PX;
    let d = "";
    for (let x = X0; x <= X1; x += 4) {
      const ts = now - (X1 - x) / PX;
      const y = ts < 0 ? YL : (ts % 1) < 0.5 ? YH : YL;
      d += (d ? " L" : "M") + x + " " + y;
    }
    wave.setAttribute("d", d);
  });
  const lbl = box(sWave, X0, 780, X1 - X0, 60, "", `<div style="display:flex;justify-content:space-between;color:var(--muted);font-size:26px"><span>500 ms on</span><span>500 ms off</span><span>forever…</span></div>`);
  hidden(lbl); show(lbl, W("s25", "zero"), 0.4);
  const L = ledIcon(sWave, 1580, 420, 130);
  L.drive((t) => blink(t, t0, 0.5, 0.5));
  const nm = box(sWave, 0, 900, 1920, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:30px">HIGH and LOW are just names for 3.3 V and 0 V</span></div>`);
  hidden(nm); pop(nm, W("s25", "names"));
}

/* ======================================================================
 * PLAY WITH IT (s26-s27)
 * ==================================================================== */
const sPlay = SC();
sceneIn(sPlay, S1("s25") + 0.4);
sceneOut(sPlay, S1("s27") + 0.4);
{
  const h = head(sPlay, "Play with the numbers", 80); show(h, T("s26"));
  const card = box(sPlay, 120, 260, 940, 420, "card codecard", "");
  css(card, { fontSize: "36px", lineHeight: "1.6" }); hidden(card); show(card, T("s26"), 0.4);
  const tFast = W("s26", "Change") + 0.4, tLight = W("s27", "short");
  const num = (v, hl) => `<span class="tk-num" style="${hl ? "background:rgba(255,181,71,.25);border-radius:6px;padding:0 4px" : ""}">${v}</span>`;
  const code = (a, b, hl) => `<span class="tk-fn">digitalWrite</span>(LED_PIN, HIGH);\n<span class="tk-fn">delay</span>(${num(a, hl)});\n<span class="tk-fn">digitalWrite</span>(LED_PIN, LOW);\n<span class="tk-fn">delay</span>(${num(b, hl)});`;
  textAt(card, [[0, code(500, 500)], [tFast, code(100, 100, true)], [tLight, code(100, 1900, true)]]);
  const tag = box(sPlay, 120, 720, 940, 80, "", "");
  panelAt(tag, [[0, ""], [W("s26", "blinks"), `<span class="pill" style="font-size:30px">5 blinks per second</span>`],
    [W("s27", "lighthouse"), `<span class="pill" style="font-size:30px;background:rgba(255,181,71,.18);color:var(--amber)">🗼 a lighthouse: short flash, long pause</span>`]]);
  const L = ledIcon(sPlay, 1420, 600, 120);
  const tUp = W("s26", "upload");
  L.drive((t) => (t < tUp ? blink(t, T("s26"), 0.5, 0.5) : t < tLight ? blink(t, tUp, 0.1, 0.1) : blink(t, tLight, 0.1, 1.9)));
  clipFrame(sPlay, "C3", 1140, 190, 720, 405, tUp, S1("s26") + 1.0, "The LED blinking fast (delays set to 100).");
  const nb = box(sPlay, 0, 880, 1920, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:30px">✓ changing the numbers can't break anything</span></div>`);
  hidden(nb); pop(nb, W("s27", "break"));
}

/* ======================================================================
 * NOT BLINKING? (s28)
 * ==================================================================== */
const sTrouble = SC();
sceneIn(sTrouble, S1("s27") + 0.4);
sceneOut(sTrouble, S1("s28") + 0.5);
{
  const chk = box(sTrouble, 360, 190, 1200, 700, "card", "");
  const rows = [["Red wire in the D23 column", "red"], ["The code says 23", "code"], ["Long leg toward the resistor", "long"], ["Always on? Wire still on 3V3", "always"]];
  chk.innerHTML = `<div style="padding:44px 60px"><div class="kicker">LED not blinking?</div>` + rows.map(([a]) => `<div class="row" style="display:flex;gap:22px;align-items:center;margin-top:34px;opacity:0">
    <div style="width:56px;height:56px;border-radius:50%;background:var(--green);color:#052;font:800 32px var(--ui);display:flex;align-items:center;justify-content:center">✓</div>
    <div style="font:600 40px var(--display)">${a}</div></div>`).join("") + `</div>`;
  chk.querySelectorAll(".row").forEach((r, i) => TO(r, W("s28", rows[i][1]), 0.4, { opacity: 1 }));
}

/* ======================================================================
 * OUTRO (s29-s30)
 * ==================================================================== */
const sOutro = SC();
sceneIn(sOutro, S1("s28") + 0.5);
{
  const h = box(sOutro, 110, 220, 1500, 80, "h2", "Episode 3 complete!"); hidden(h); pop(h, T("s29"));
  const items = [["Ohm's law", "why 220 Ω"], ["pinMode", "OUTPUT"], ["digitalWrite", "HIGH = 3.3 V, LOW = 0 V"], ["delay", "milliseconds"]];
  const cards = items.map(([a, b], i) => {
    const c = box(sOutro, 110 + i * 435, 400, 400, 300, "card", `<div style="padding:34px"><div style="width:64px;height:64px;border-radius:50%;background:rgba(25,195,180,.15);color:var(--teal);font:700 32px var(--display);display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div style="font:700 34px var(--display);margin-top:28px">${a}</div><div class="muted" style="font-size:23px;margin-top:8px">${b}</div></div>
      <div class="ok" style="position:absolute;right:26px;top:26px;width:58px;height:58px;border-radius:50%;background:var(--green);color:#052;font:700 34px var(--ui);display:flex;align-items:center;justify-content:center;opacity:0">✓</div>`);
    hidden(c);
    return c;
  });
  ["resistor", "pin", "digital", "delay"].forEach((w, i) => {
    pop(cards[i], W("s29", w) - 0.15);
    const ok = $(".ok", cards[i]);
    SET(ok, W("s29", w) + 0.2, { scale: 0.4 });
    TO(ok, W("s29", w) + 0.2, 0.4, { opacity: 1, scale: 1, ease: "back.out(2)" });
  });
  hide(cards, T("s30") - 0.1, 0.4); hide(h, T("s30") - 0.1, 0.4);
  const nx = box(sOutro, 260, 260, 1400, 330, "card", `<div style="padding:50px 60px"><div class="kicker">Next episode</div>
    <div style="font:700 60px var(--display);margin:14px 0 18px">Buttons: reading the real world</div>
    <div class="muted" style="font-size:28px">The other direction: our code reads a pin with digitalRead.</div></div>`);
  hidden(nx); pop(nx, T("s30") + 0.2);
  const gh = box(sOutro, 260, 640, 1400, 120, "card", `<div style="display:flex;align-items:center;gap:26px;height:120px;padding:0 50px">
    <svg width="54" height="54" viewBox="0 0 16 16"><path fill="#fff" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.690-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
    <div style="font:600 36px var(--mono)">github.com/emjnbulut/esp32-from-zero</div></div>`);
  hidden(gh); pop(gh, W("s30", "GitHub"));
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 });
  TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}

window.__seek(0);
window.__ready = true;
