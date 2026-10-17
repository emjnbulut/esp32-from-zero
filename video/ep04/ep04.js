/* Episode 4 - Buttons and Doing Two Things at Once. All times come from the narration schedule. */
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
const LEDCOL = {
  red: { a: "#ff8a8f", b: "#d4202c", rim: "#b51d27", hot: "#ffe0e0", glow: "rgba(255,90,90,.9) 0%, rgba(255,50,50,.45) 30%, rgba(255,40,40,0) 65%" },
  green: { a: "#8af5b0", b: "#1fae55", rim: "#178a3a", hot: "#e0ffe9", glow: "rgba(80,255,140,.9) 0%, rgba(40,220,110,.45) 30%, rgba(30,200,90,0) 65%" },
};
let ledN = 0;
/** side-view LED with a glow behind it; drive(fn) sets brightness 0..1 from time */
function ledIcon(parent, x, y, w = 110, color = "red") {
  const C = LEDCOL[color], id = "lg" + ledN++;
  const r = box(parent, x, y, w, w * 230 / 120, "");
  const glow = box(r, -w * 0.75, -w * 0.7, w * 2.5, w * 2.5, "");
  css(glow, { borderRadius: "50%", background: `radial-gradient(circle, ${C.glow})`, opacity: 0 });
  r.insertAdjacentHTML("beforeend", `<svg width="${w}" viewBox="0 0 120 230" style="position:absolute;left:0;top:0"><defs><radialGradient id="${id}" cx=".4" cy=".35"><stop offset="0" stop-color="${C.a}"/><stop offset="1" stop-color="${C.b}"/></radialGradient></defs>
    <path d="M44 96 V226" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/><path d="M76 96 V186" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/>
    <path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="url(#${id})" opacity=".95"/><path class="hot" d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="${C.hot}" opacity="0"/>
    <path d="M22 92 h70 v14 h-70 z" fill="${C.rim}"/></svg>`);
  const hot = $(".hot", r);
  const drive = (fn) => dyn((t) => { const v = fn(t); glow.style.opacity = v; hot.setAttribute("opacity", v * 0.75); });
  return { r, glow, drive };
}
/** square-wave blink: on for `on` s, off for `off` s, starting at t0 */
const blink = (t, t0, on, off) => (t < t0 ? 0 : ((t - t0) % (on + off)) < on ? 1 : 0);
/** is t inside one of the [t0, t1] intervals? */
const inAny = (t, list) => list.some(([a, b]) => t >= a && t < b);
/** a push button seen from above, as an icon; press(list of [t0, t1]) animates the cap */
function btnIcon(parent, x, y, w = 150) {
  const r = box(parent, x, y, w, w, "");
  r.innerHTML = `<svg width="${w}" height="${w}" viewBox="0 0 100 100" style="position:absolute;left:0;top:0">
    <rect x="22" y="2" width="8" height="16" rx="2" fill="#aab2bd"/><rect x="70" y="2" width="8" height="16" rx="2" fill="#aab2bd"/>
    <rect x="22" y="82" width="8" height="16" rx="2" fill="#aab2bd"/><rect x="70" y="82" width="8" height="16" rx="2" fill="#aab2bd"/>
    <rect x="10" y="12" width="80" height="76" rx="8" fill="#23272f" stroke="#3a404b" stroke-width="2"/>
    <circle class="cap" cx="50" cy="50" r="24" fill="#4a5262" stroke="#11141a" stroke-width="3"/></svg>`;
  const cap = $(".cap", r);
  const lab = box(parent, x - 40, y + w + 8, w + 80, 34, "", "");
  css(lab, { textAlign: "center", font: "700 22px var(--ui)" });
  const press = (list) => dyn((t) => {
    const on = inAny(t, list);
    cap.setAttribute("r", on ? 20 : 24);
    cap.setAttribute("fill", on ? "#ffb547" : "#4a5262");
    const txt = on ? `<span style="color:var(--amber)">pressed</span>` : `<span style="color:var(--muted)">released</span>`;
    if (lab.__v !== txt) { lab.innerHTML = txt; lab.__v = txt; }
  });
  return { r, lab, press };
}
const pill = (parent, x, y, html, style = "") => {
  const p = box(parent, x, y, 0, 0, "", `<span class="pill" style="font-size:28px;${style}">${html}</span>`);
  css(p, { width: "auto", height: "auto", whiteSpace: "nowrap" });
  return hidden(p);
};
const pillC = (parent, y, html, style = "") => {
  const p = box(parent, 0, y, 1920, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:30px;${style}">${html}</span></div>`);
  return hidden(p);
};
/** code card whose text follows a schedule: list = [[t, html], ...] */
function codeCard(parent, x, y, w, h, list, size = 30) {
  const c = box(parent, x, y, w, h, "card codecard", "");
  css(c, { fontSize: size + "px", lineHeight: "1.55", whiteSpace: "pre" });
  textAt(c, list);
  return hidden(c);
}
const fn = (s) => `<span class="tk-fn">${s}</span>`;
const num = (s) => `<span class="tk-num">${s}</span>`;
const cm = (s) => `<span class="tk-cm">${s}</span>`;
const kw = (s) => `<span class="tk-kw">${s}</span>`;
const hl = (s, col = "rgba(255,181,71,.22)") => `<span style="background:${col};border-radius:6px;padding:0 4px;margin:0 -4px">${s}</span>`;

/* ======================================================================
 * INTRO (s01-s02)
 * ==================================================================== */
const sIntro = SC();
SET(sIntro, 0, { opacity: 1 });
{
  const kick = box(sIntro, 140, 300, 600, 40, "kicker", "Episode 04");
  const title = box(sIntro, 136, 336, 1000, 140, "h1", "ESP32 From Zero");
  title.style.fontSize = "112px";
  const sub = box(sIntro, 140, 486, 1100, 60, "h3", "Buttons and Doing Two Things at Once");
  sub.style.color = "var(--teal)";
  const persp = box(sIntro, 1130, 70, 560, 900, "");
  persp.style.perspective = "1600px";
  const b3d = box(persp, 0, 0, 560, 900, "", boardSVG({ pins: 30, chip: "cp2102", p: "bi", width: 520 }));
  css(b3d, { filter: "drop-shadow(0 40px 60px rgba(0,0,0,.6)) drop-shadow(0 0 40px rgba(25,195,180,.25))" });
  gsap.set(b3d, { rotationY: -28, rotationX: 18, y: 60, opacity: 0 });
  TO(b3d, 0.3, 1.6, { opacity: 1, y: 0, ease: "power3.out" });
  TO(b3d, 0.3, 24, { rotationY: 12, rotationX: 8, ease: "sine.inOut" });
  for (const [e, t] of [[kick, 0.5], [title, 0.75], [sub, 1.1]]) {
    gsap.set(e, { opacity: 0, y: 30 });
    TO(e, t, 0.8, { opacity: 1, y: 0, ease: "power3.out" });
  }
  const items = [["Wire a button", "GPIO 22 → button → GND"], ["Read it", "digitalRead, pull-ups"], ["Two things at once", "millis() instead of delay()"]];
  ["button", "read", "two"].forEach((w, i) => {
    const c = box(sIntro, 140 + i * 330, 600, 300, 140, "card", `<div style="padding:22px 24px"><div class="kicker" style="font-size:16px">Today · ${i + 1}</div>
      <div style="font:600 29px var(--display);margin-top:8px">${items[i][0]}</div><div class="muted" style="font-size:19px;margin-top:4px">${items[i][1]}</div></div>`);
    hidden(c); pop(c, W("s02", w));
  });
  sceneOut(sIntro, S1("s02") + 0.4);
}

/* ======================================================================
 * THE PUSH BUTTON (s03-s05)
 * ==================================================================== */
const sBtn = SC();
sceneIn(sBtn, S1("s02") + 0.4);
sceneOut(sBtn, S1("s05") + 0.4);
{
  const h = head(sBtn, "The push button", 80); show(h, T("s03"));
  const sv = svgLayer(sBtn);
  const g = svgEl(sv, "g", { opacity: 0 });
  TO(g, T("s03") + 0.2, 0.5, { opacity: 1 });
  const L = 600, R = 820, TOP = 380, BOT = 760, CX = 710, CY = 570;
  for (const x of [L, R]) for (const [y0, y1] of [[TOP - 80, TOP + 10], [BOT - 10, BOT + 80]])
    svgEl(g, "rect", { x: x - 10, y: y0, width: 20, height: y1 - y0, rx: 4, fill: "#b8bec6" });
  svgEl(g, "rect", { x: L - 60, y: TOP, width: R - L + 120, height: BOT - TOP, rx: 22, fill: "#22262d", stroke: "#3a404b", "stroke-width": 4 });
  const cap = svgEl(g, "circle", { cx: CX, cy: CY, r: 110, fill: "#4a5262", stroke: "#11141a", "stroke-width": 6 });
  // the always-connected pairs (drawn on top, dashed)
  const pairs = [L, R].map((x) => svgEl(g, "path", { d: `M${x} ${TOP - 75} V${BOT + 75}`, stroke: "#19c3b4", "stroke-width": 10, "stroke-linecap": "round", fill: "none", "stroke-dasharray": "2 0" }));
  drawOn(pairs[0], W("s04", "left"), 0.8); drawOn(pairs[1], W("s04", "right"), 0.8);
  const plate = svgEl(g, "path", { d: `M${L} ${CY} H${R}`, stroke: "#ffb547", "stroke-width": 16, "stroke-linecap": "round", opacity: 0 });
  const tP = W("s05", "press") + 0.1, tR = W("s05", "Let") + 0.1;
  dyn((t) => {
    const on = t >= tP && t < tR;
    cap.setAttribute("r", on ? 96 : 110);
    cap.setAttribute("fill", on ? "#5d6576" : "#4a5262");
    plate.setAttribute("opacity", t >= W("s05", "plate") && t < tR ? 1 : 0);
  });
  for (const [x, txt, w] of [[L, "left pair", "left"], [R, "right pair", "right"]]) {
    const l = box(sBtn, x - 110, BOT + 100, 220, 40, "", `<div style="text-align:center;font:700 26px var(--ui);color:var(--teal)">${txt}</div>`);
    hidden(l); pop(l, W("s04", w) + 0.3);
  }
  const notes = [["4 legs, 1 simple switch", W("s03", "four")], ["each pair is always connected", W("s04", "always")],
    ["<b style='color:var(--amber)'>pressed:</b> left ↔ right connected", W("s05", "connects")], ["released: apart again", W("s05", "apart")]];
  notes.forEach(([txt, t], i) => {
    const n = box(sBtn, 1120, 330 + i * 110, 720, 80, "card", `<div style="padding:20px 28px;font:600 30px var(--display)">${txt}</div>`);
    hidden(n); pop(n, t);
  });
}

/* ======================================================================
 * BREADBOARD: the button (s06-s09) and the green LED (s47-s49)
 * ==================================================================== */
const BBX = 290, BBY = 236;
const sBB = SC();
sceneIn(sBB, S1("s05") + 0.4);
sceneOut(sBB, S1("s09") + 0.4);
sceneIn(sBB, S1("s46") + 0.4);
sceneOut(sBB, S1("s49") + 0.5);
{
  const hd = box(sBB, 0, 70, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s06"), "Our circuit from episode 3"], [T("s07"), "Add the button"], [T("s09"), "Pressed: GPIO 22 → GND"],
    [T("s47"), "A second LED"], [W("s48", "top"), "Top half: the green LED"]]);
  const bb = makeBB(sBB, BBX, BBY);
  bbBoard(bb, 30, 2);
  // the circuit from episode 3: GPIO 23 (j16) -> 220 ohm -> LED -> GND
  bbWire(bb, bb.L(3, "j"), bb.L(3, "bm"), "#2b2f36", 0, -0.35);
  bbResistor(bb, bb.L(16, "j"), bb.L(20, "h"));
  const led = bbLED(bb, bb.L(20, "f"), bb.L(21, "f"), -1);
  bbWire(bb, bb.L(21, "j"), bb.L(21, "bm"), "#2b2f36", 0, -0.35);
  gsap.set(bb.strips, { opacity: 1 });
  for (let c = 1; c <= 30; c++) bb.colStrip[c].forEach((e) => e.setAttribute("opacity", 0));
  // still running the blink sketch until the USB cable comes out
  const tUn = W("s06", "unplug") + 0.2;
  dyn((t) => { const v = t < tUn ? blink(t, 0, 0.5, 0.5) : 0; led.glow.setAttribute("opacity", v); led.lit.setAttribute("opacity", v * 0.85); });
  // USB status badge
  const usb = box(sBB, 70, 80, 0, 0, "badge", "");
  css(usb, { width: "auto", height: "auto", background: "rgba(11,18,32,.9)", border: "1px solid var(--line)" });
  const on = `<span style="color:var(--green)">● USB plugged in</span>`, off = `<span style="color:var(--red)">● USB unplugged</span>`;
  panelAt(usb, [[0, on], [W("s06", "unplug"), off], [T("s47"), on], [W("s48", "Unplug"), off]], 0);
  // s07: the button across the gap, columns 25 and 27
  const [x1, ye] = bb.L(25, "e"), [x2, yf] = bb.L(27, "f");
  const bg = svgEl(bb.parts, "g", { opacity: 0 });
  for (const [c, r] of [[25, "e"], [27, "e"], [25, "f"], [27, "f"]]) { const [lx, ly] = bb.L(c, r); svgEl(bg, "rect", { x: lx - 7, y: ly - 7, width: 14, height: 14, rx: 2, fill: "#9aa1aa" }); }
  const bcx = (x1 + x2) / 2, bcy = (ye + yf) / 2;
  svgEl(bg, "rect", { x: x1 - 22, y: ye - 4, width: x2 - x1 + 44, height: yf - ye + 8, rx: 10, fill: "#22262d", stroke: "#3a404b", "stroke-width": 2 });
  const bcap = svgEl(bg, "circle", { cx: bcx, cy: bcy, r: 34, fill: "#4a5262", stroke: "#11141a", "stroke-width": 3 });
  TO(bg, W("s07", "Press") + 0.1, 0.5, { opacity: 1 });
  for (const c of [25, 27]) {
    const st = bb.colStrip[c];
    TO(st, W("s07", "columns"), 0.4, { opacity: 0.6 }); TO(st, T("s08"), 0.4, { opacity: 0 });
  }
  callout(sBB, "across the middle gap", bb.S(27, "e")[0] + 50, bb.S(27, "e")[1] + 20, W("s07", "gap"), T("s08"));
  // s08: yellow wire D22 -> button left side, black wire right side -> minus rail
  bbWire(bb, bb.L(15, "j"), bb.L(25, "j"), "#ffd34d", W("s08", "yellow"), -0.1);
  const p22 = bb.S(15, "i");
  callout(sBB, "D22", p22[0] - 34, p22[1] - 72, W("s08", "twentytwo"), S1("s08"));
  bbWire(bb, bb.L(27, "j"), bb.L(27, "bm"), "#2b2f36", W("s08", "black"), -0.35);
  callout(sBB, "− rail = GND", bb.S(27, "bm")[0] + 30, bb.S(27, "bm")[1] - 20, W("s08", "minus"), S1("s08"));
  // s09: pressed -> GPIO 22 is connected to ground
  const pts = [bb.L(15, "i"), bb.L(15, "j"), bb.L(25, "j"), bb.L(25, "f"), bb.L(27, "f"), bb.L(27, "j"), bb.L(27, "bm"), bb.L(3, "bm"), bb.L(3, "j"), bb.L(3, "i")];
  const path = svgEl(bb.over, "path", { d: "M" + pts.map((p) => p.join(" ")).join(" L"), fill: "none", stroke: "#19c3b4", "stroke-width": 7, "stroke-linejoin": "round", opacity: 0.95 });
  drawOn(path, W("s09", "connected"), 1.6);
  TO(path, S1("s09"), 0.3, { opacity: 0 });
  const tPr = W("s09", "press");
  dyn((t) => { const on = t >= tPr && t < S1("s09"); bcap.setAttribute("r", on ? 28 : 34); bcap.setAttribute("fill", on ? "#ffb547" : "#4a5262"); });
  // s48-s49: the green LED in the top half
  const t48 = (w) => W("s48", w), t49 = (w) => W("s49", w);
  bbWire(bb, bb.L(9, "a"), bb.L(18, "a"), "#3ddc84", t48("green"), -0.06);
  const p25 = bb.S(9, "b");
  callout(sBB, "D25", p25[0] - 34, p25[1] - 100, t48("twentyfive"), t48("resistor"));
  const gr = svgEl(bb.parts, "g", { opacity: 0 });
  bb.parts.appendChild(gr);
  const res = bbResistor(bb, bb.L(18, "b"), bb.L(21, "b"));
  gr.appendChild(res);
  TO(gr, t48("resistor"), 0.4, { opacity: 1 });
  const gled = bbLED(bb, bb.L(21, "d"), bb.L(22, "d"), -1);
  const recol = { "#b51d27": "#178a3a", "#d4202c": "#2fd36b", "#ffd0d0": "#d8ffe4", "#7c121a": "#0f5c27" };
  gled.g.querySelectorAll("circle,path").forEach((e) => {
    for (const a of ["fill", "stroke"]) if (recol[e.getAttribute(a)]) e.setAttribute(a, recol[e.getAttribute(a)]);
  });
  gsap.set(gled.g, { opacity: 0 }); TO(gled.g, t49("long"), 0.4, { opacity: 1 });
  callout(sBB, "long leg", bb.S(21, "d")[0] - 140, bb.S(21, "d")[1] - 10, t49("long"), t49("black"));
  bbWire(bb, bb.L(22, "a"), bb.L(22, "tm"), "#2b2f36", t49("black"), 0.35);
  bbWire(bb, bb.L(3, "a"), bb.L(3, "tm"), "#2b2f36", t49("connects"), 0.35);
  const gnd = bb.S(3, "b");
  callout(sBB, "GND", gnd[0] - 30, gnd[1] - 100, t49("GND"), S1("s49") + 0.3);
  for (const [t0, t1] of [[W("s08", "yellow"), S1("s09")], [W("s48", "green"), S1("s49")]]) {
    const n38 = box(sBB, 380, 160, 0, 0, "badge", "38-pin board? Same pins, other columns: follow the labels (22, 23, 25, GND)");
    css(n38, { width: "auto", height: "auto", background: "rgba(11,18,32,.92)", border: "1px solid var(--line)", color: "#e8eef7", fontSize: "22px" });
    hidden(n38); pop(n38, t0 + 0.8); hide(n38, t1);
  }
  clipFrame(sBB, "C1", 1140, 150, 720, 405, W("s07", "Press") - 0.2, S1("s07") + 1.0, "USB unplugged: press the button in across the gap, then add the yellow and black wires.");
  clipFrame(sBB, "C5", 1140, 560, 720, 405, t49("black") - 0.3, S1("s49") + 0.9, "Top half: green wire, resistor, green LED, two black wires.");
}

/* ======================================================================
 * FLOATING PINS AND PULL-UPS (s10-s16)
 * ==================================================================== */
const sFloat = SC();
sceneIn(sFloat, S1("s09") + 0.4);
sceneOut(sFloat, S1("s16") + 0.4);
{
  const hd = box(sFloat, 0, 70, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s10"), "Not pressed: what does the pin read?"], [W("s12", "fix"), "The fix: a pull-up resistor"],
    [T("s14"), "Pull-up or pull-down"], [T("s15"), "Built into the ESP32"]]);
  const sv = svgLayer(sFloat);
  const NX = 720, NY = 560, SX0 = 900, SX1 = 1060;
  const pinBox = box(sFloat, 180, NY - 60, 300, 120, "card", `<div style="height:120px;display:flex;align-items:center;justify-content:center;font:700 40px var(--mono);color:var(--teal)">GPIO 22</div>`);
  hidden(pinBox); show(pinBox, T("s10") - 0.2, 0.4);
  const g = svgEl(sv, "g", { opacity: 0 }); TO(g, T("s10") - 0.2, 0.4, { opacity: 1 });
  const wire = { stroke: "#cfd6e2", "stroke-width": 6, fill: "none", "stroke-linecap": "round" };
  svgEl(g, "path", Object.assign({ d: `M480 ${NY} H${SX0}` }, wire));
  svgEl(g, "path", Object.assign({ d: `M${SX1} ${NY} H1180 V700` }, wire));
  for (const [w, dy] of [[80, 0], [52, 14], [24, 28]]) svgEl(g, "path", Object.assign({ d: `M${1180 - w / 2} ${700 + dy} h${w}` }, wire));
  const gl = svgEl(sv, "text", { x: 1180, y: 770, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 26, fill: "#8fa1c0" });
  gl.textContent = "GND (0 V)"; g.appendChild(gl);
  for (const x of [SX0, SX1]) svgEl(g, "circle", { cx: x, cy: NY, r: 10, fill: "#cfd6e2" });
  const lever = svgEl(g, "path", Object.assign({}, wire, { "stroke-width": 8 }));
  const bl = svgEl(sv, "text", { x: (SX0 + SX1) / 2, y: NY + 60, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 26, fill: "#8fa1c0" });
  bl.textContent = "button"; g.appendChild(bl);
  // when the button is closed
  const closed = [[T("s10"), W("s10", "what")], [W("s13", "pressed", 2), W("s13", "LOW") + 1.2], [W("s16", "button"), W("s16", "strong")]];
  // the pull-up: from the node up to 3.3 V
  const pu = svgEl(sv, "g", { opacity: 0 });
  const zz = [];
  for (let i = 0; i <= 6; i++) zz.push(`L${NX + (i === 0 || i === 6 ? 0 : i % 2 ? 26 : -26)} ${450 - i * 22}`);
  svgEl(pu, "path", Object.assign({ d: `M${NX} ${NY} V450 ${zz.join(" ")} V250 M${NX - 70} 250 H${NX + 70}` }, wire, { stroke: "#ffb547" }));
  svgEl(pu, "circle", { cx: NX, cy: NY, r: 10, fill: "#ffb547" });
  const v33 = svgEl(pu, "text", { x: NX, y: 228, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 30, fill: "#ffb547" });
  v33.textContent = "3.3 V";
  TO(pu, W("s12", "pullup") - 0.1, 0.5, { opacity: 1 });
  const puLab = box(sFloat, NX + 50, 330, 360, 50, "", "");
  css(puLab, { font: "700 28px var(--ui)", color: "var(--amber)" });
  panelAt(puLab, [[0, ""], [W("s12", "pullup") + 0.3, "pull-up resistor"], [W("s16", "fortyfive"), "pull-up ≈ 45 kΩ"]]);
  // pressed: current path from the pin to ground
  // readout
  const card = box(sFloat, 1350, 250, 440, 300, "card", "");
  hidden(card); show(card, T("s10"), 0.4);
  const lab = box(card, 0, 30, 440, 40, "", `<div style="text-align:center;font:600 26px var(--ui);color:var(--muted)">GPIO 22 reads</div>`);
  const val = box(card, 0, 90, 440, 150, "", "");
  const rnd = (k) => { let x = Math.sin(k * 12.9898) * 43758.5453; return x - Math.floor(x); };
  const tFl = W("s11", "floating"), tPU = W("s12", "pullup") + 0.4;
  dyn((t) => {
    const c = inAny(t, closed);
    const a = c ? 0 : -0.5;
    lever.setAttribute("d", `M${SX0} ${NY} L${SX0 + Math.cos(a) * (SX1 - SX0)} ${NY + Math.sin(a) * (SX1 - SX0)}`);
    let txt, col;
    if (c) { txt = "LOW"; col = "#6ea8ff"; }
    else if (t >= tPU) { txt = "HIGH"; col = "#19c3b4"; }
    else if (t >= tFl) { txt = rnd(Math.floor(t * 7)) < 0.5 ? "HIGH?" : "LOW?"; col = "#ffb547"; }
    else { txt = "?"; col = "#ffb547"; }
    const html = `<div style="text-align:center;font:800 96px var(--display);color:${col}">${txt}</div><div style="text-align:center;font:600 26px var(--ui);color:var(--muted)">${c ? "0 V" : t >= tPU ? "3.3 V" : "connected to nothing"}</div>`;
    if (val.__v !== html) { val.innerHTML = html; val.__v = html; }
  });
  const fl = pill(sFloat, 1360, 590, "floating = random readings", "background:rgba(255,181,71,.18);color:var(--amber)");
  pop(fl, tFl); hide(fl, tPU, 0.3);
  const hand = box(sFloat, 600, 380, 120, 120, "", `<div style="font-size:90px">✋</div>`);
  hidden(hand); pop(hand, W("s11", "hand")); hide(hand, S1("s11"), 0.3);
  const tbl = pill(sFloat, 1360, 590, "not pressed = HIGH · pressed = LOW", "");
  pop(tbl, W("s13", "LOW") + 0.2); hide(tbl, T("s14"), 0.3);
  // s14: pull-down (small diagram)
  const pd = box(sFloat, 1300, 600, 540, 380, "card", "");
  pd.innerHTML = `<div style="padding:18px 26px"><div class="kicker">pull-down instead</div></div>
    <svg width="540" height="300" viewBox="0 0 540 300" style="position:absolute;left:0;top:70">
      <g stroke="#cfd6e2" stroke-width="5" fill="none" stroke-linecap="round">
        <path d="M40 150 H270"/><path d="M270 150 V185 l18 10 l-36 12 l36 12 l-36 12 l18 10 V270"/><path d="M240 270 h60 M252 281 h36 M264 292 h12"/>
        <path d="M270 150 V120"/><path d="M270 120 L300 60"/><path d="M270 50 V30 M220 30 H320"/></g>
      <circle cx="270" cy="150" r="7" fill="#cfd6e2"/><circle cx="270" cy="120" r="6" fill="#cfd6e2"/><circle cx="270" cy="50" r="6" fill="#cfd6e2"/>
      <text x="40" y="135" font-family="Segoe UI" font-weight="700" font-size="22" fill="#19c3b4">GPIO</text>
      <text x="300" y="225" font-family="Segoe UI" font-weight="700" font-size="22" fill="#ffb547">10 kΩ → GND</text>
      <text x="310" y="95" font-family="Segoe UI" font-weight="700" font-size="22" fill="#8fa1c0">button → 3.3 V</text>
      <text x="340" y="36" font-family="Segoe UI" font-weight="700" font-size="22" fill="#8fa1c0">3.3 V</text></svg>`;
  hidden(pd); pop(pd, W("s14", "ten")); hide(pd, T("s15"), 0.35);
  const pdr = pill(sFloat, 1330, 990, "pressed = HIGH", "font-size:24px");
  pop(pdr, W("s14", "Then")); hide(pdr, T("s15"), 0.3);
  // s15: it's all inside the chip
  const inside = box(sFloat, 150, 200, 670, 460, "", `<div style="position:absolute;left:18px;top:-18px;background:var(--bg);padding:0 10px;font:700 24px var(--ui);color:var(--teal)">inside the ESP32</div>`);
  css(inside, { border: "3px dashed var(--teal)", borderRadius: "22px" }); hidden(inside);
  pop(inside, W("s15", "built")); hide(inside, S1("s16"), 0.3);
  const ok = pillC(sFloat, 900, "✓ no extra part: INPUT_PULLUP switches it on", "font-size:32px");
  pop(ok, W("s15", "code")); hide(ok, T("s16"), 0.3);
  const ok2 = pillC(sFloat, 900, "weak enough for the button to win · strong enough to hold the pin", "font-size:30px");
  pop(ok2, W("s16", "Weak"));
}

/* ======================================================================
 * ARDUINO IDE: button_led (s17-s21), upload + Serial Monitor (s22-s25)
 * ==================================================================== */
const DK = buildDesktop(stage);
const camera = DK.camera;
initCamera(camera);
initCursor(camera);
sceneIn(DK.desk, S1("s16") + 0.4);
sceneOut(DK.desk, S1("s25") + 0.5);
const ide = buildIDE(camera);
ide.boardText.textContent = "ESP32 Dev Module";
ide.statusBoard.textContent = "ESP32 Dev Module on COM3";
const DEFAULT_SKETCH = "void setup() {\n  // put your setup code here, to run once:\n\n}\n\nvoid loop() {\n  // put your main code here, to run repeatedly:\n\n}\n";
const SKETCH = `// ESP32 From Zero - Episode 4: Read a button
// GPIO 22 -> button -> GND (internal pull-up), LED on GPIO 23

const int BUTTON_PIN = 22;     // the button pulls this pin to GND
const int LED_PIN = 23;        // our LED from episode 3

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP); // HIGH until pressed
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int state = digitalRead(BUTTON_PIN); // HIGH or LOW
  Serial.println(state);

  if (state == LOW) {          // pressed: pulled to GND
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(50);
}
`;
const FLOATING = SKETCH.replace("pinMode(BUTTON_PIN, INPUT_PULLUP); // HIGH until pressed", "pinMode(BUTTON_PIN, INPUT);        // floating!");
const lineY = (i) => IDE.codeTop + i * IDE.lineH;
const cx = (col) => IDE.codeX + col * IDE.charW;
pop(ide.w, T("s17") - 0.3, 0.45);
const tFloatEdit = W("s24", "plain"), tFloatBack = W("s25", "back");
{
  const s = "s17";
  const tSel = W(s, "new") + 0.1, tDel = W(s, "sketch") + 0.3;
  const selFlash = box(camera, 120, lineY(0), 520, 22 * 9, "");
  css(selFlash, { background: "rgba(38,79,120,.85)", opacity: 0 });
  SET(selFlash, tSel, { opacity: 1 }); SET(selFlash, tDel, { opacity: 0 });
  const keys = box(stage, 760, 900, 400, 70, "", "");
  css(keys, { zIndex: 55, textAlign: "center" }); hidden(keys);
  textAt(keys, [[0, ""], [tSel - 0.1, `<span class="pill" style="font-size:30px;background:#1b2430;color:#fff">Ctrl + A &nbsp;→&nbsp; Delete</span>`],
    [W("s22", "Save") - 0.1, `<span class="pill" style="font-size:30px;background:#1b2430;color:#fff">Ctrl + S</span>`]]);
  show(keys, tSel - 0.1, 0.2); hide(keys, tDel + 0.6, 0.2);
  show(keys, W("s22", "Save") - 0.1, 0.2); hide(keys, W("s22", "click"), 0.2);
  cam(tDel, 1.2, 520, 300, 1.8);
  const pieces = [
    ["// ESP32 From Zero - Episode 4: Read a button\n// GPIO 22 -> button -> GND (internal pull-up), LED on GPIO 23\n\n", tDel + 0.3, W(s, "name")],
    ["const int BUTTON_PIN = 22;     // the button pulls this pin to GND\nconst int LED_PIN = 23;        // our LED from episode 3\n\n", W(s, "name") + 0.2, S1(s)],
    ["void setup() {\n", T("s18") + 0.1, T("s18") + 0.6],
    ["  pinMode(BUTTON_PIN, INPUT_PULLUP); // HIGH until pressed\n", T("s18") + 0.7, W("s18", "means")],
    ["  pinMode(LED_PIN, OUTPUT);\n  Serial.begin(115200);\n}\n\n", T("s19") + 0.1, S1("s19")],
    ["void loop() {\n  int state = digitalRead(BUTTON_PIN); // HIGH or LOW\n  Serial.println(state);\n\n", T("s20") + 0.1, W("s20", "print")],
    ["  if (state == LOW) {          // pressed: pulled to GND\n    digitalWrite(LED_PIN, HIGH);\n  } else {\n    digitalWrite(LED_PIN, LOW);\n  }\n  delay(50);\n}\n", T("s21") + 0.1, S1("s21")],
  ];
  let all = "";
  const times = [];
  pieces.forEach(([txt, a, b], i) => {
    const cps = Math.min(40, Math.max(9, txt.length / Math.max(0.6, b - a)));
    const tt = typingTimes(txt, a, cps, 31 + i);
    all += txt; times.push(...tt);
  });
  if (all !== SKETCH) console.warn("typed text differs from SKETCH");
  dyn((t) => {
    if (t < T(s) - 0.5) return;
    const n = t < tDel ? -1 : countAt(times, t);
    if (n < 0) { renderCode(ide.code, DEFAULT_SKETCH, DEFAULT_SKETCH.length, false, 10); return; }
    const src = t >= tFloatEdit && t < tFloatBack ? FLOATING : all;
    const on = Math.floor(t * 1.9) % 2 === 0 || (n > 0 && n < all.length && t - times[n - 1] < 0.5);
    renderCode(ide.code, src, src === all ? n : src.length, on && t < T("s22"), 1);
    const lines = all.slice(0, n).split("\n");
    ide.statusLC.textContent = `Ln ${lines.length}, Col ${lines[lines.length - 1].length + 1}`;
  });
  cam(T("s21"), 1.0, 520, 420, 1.8);
  // explanations
  ring(camera, cx(0) - 4, lineY(3) - 1, cx(26) - cx(0) + 8, 2 * 22 + 2, W(s, "name") + 0.8, S1(s) + 0.3);
  ring(camera, cx(2) - 4, lineY(7) - 1, cx(36) - cx(2) + 8, 24, W("s18", "INPUT") + 0.1, S1("s18") + 0.3);
  callout(camera, "INPUT = we read it · PULLUP = built-in resistor on", cx(2), lineY(7) + 30, W("s18", "means"), S1("s18") + 0.3);
  ring(camera, cx(2) - 4, lineY(13) - 1, cx(38) - cx(2) + 8, 24, W("s20", "digital"), S1("s20") + 0.2);
  callout(camera, "HIGH (1) or LOW (0)", cx(55), lineY(13) - 4, W("s20", "HIGH"), S1("s20") + 0.2);
  ring(camera, cx(2) - 4, lineY(16) - 4, cx(52) - cx(2) + 8, 5 * 22 + 8, W("s21", "If"), S1("s21") + 0.3);
  callout(camera, "LOW = pressed → LED on", cx(56), lineY(17) - 4, W("s21", "pressed"), S1("s21") + 0.3);
}
{
  // s22: save, upload, open the Serial Monitor
  const s22 = "s22", s23 = "s23", s24 = "s24", s25 = "s25";
  const tSave = W(s22, "Save") + 0.3;
  textAt(ide.tab, [[0, "sketch_oct17b.ino"], [tSave, "button_led.ino"]]);
  textAt(ide.title, [[0, "sketch_oct17b | Arduino IDE 2.3.10"], [tSave, "button_led | Arduino IDE 2.3.10"]]);
  camReset(W(s22, "click") - 0.4, 0.8);
  // two uploads: button_led, then the floating version
  const uploads = [[W(s22, "Upload"), W(s22, "Serial") - 0.2], [W(s24, "upload") + 0.1, W(s25, "Now") - 0.1]];
  clickAt(IDE.upload.x, IDE.upload.y, uploads[0][0], 0.9);
  clickAt(IDE.upload.x, IDE.upload.y, uploads[1][0], 0.9);
  const toasts = [[0, ""]];
  for (const [a, b] of uploads) toasts.push([a + 0.1, "Compiling sketch..."], [a + (b - a) * 0.45, "Uploading..."], [b, "Done uploading."]);
  textAt(ide.toastText, toasts);
  for (const [a, b] of uploads) {
    SET(ide.toastBar, a + 0.09, { width: "0%" });
    show(ide.toast, a + 0.1, 0.2); TO(ide.toastBar, a + 0.1, b - a - 0.1, { width: "100%", ease: "none" }); hide(ide.toast, b + 1.0, 0.3);
  }
  const u0 = uploads[0][0] + 0.1, tHR = uploads[0][1];
  const bar = (p) => { const n = Math.round(p * 30); return `Writing at 0x000${(0x10000 + Math.floor(p * 153950)).toString(16)} [${"=".repeat(Math.max(0, n - 1))}${n ? ">" : ""}${" ".repeat(30 - n)}] ${(p * 100).toFixed(1).padStart(5)}% ${Math.floor(p * 153950)}/153950 bytes...`; };
  const k = (f) => u0 + (tHR - u0) * f;
  logLines(ide.out, [
    [u0 + 0.3, ""],
    [k(0.25), "Sketch uses 271980 bytes (20%) of program storage space. Maximum is 1310720 bytes."],
    [k(0.3), "Global variables use 22116 bytes (6%) of dynamic memory, leaving 305564 bytes for local variables. Maximum is 327680 bytes."],
    [k(0.4), "esptool v5.1.0"], [k(0.45), "Connected to ESP32 on COM3:"],
    [k(0.5), (dt) => bar(Math.min(1, dt / ((tHR - u0) * 0.45)))],
    [tHR - 0.1, "Hash of data verified."],
    [tHR, '<span style="color:#0ca1a6">Hard resetting via RTS pin...</span>'],
  ], 8, [u0 - 0.5, 1e9]);
  // Serial Monitor
  clickAt(IDE.monitor.x, IDE.monitor.y, W(s22, "Serial"), 0.9);
  const tOpen = W(s22, "Serial") + 0.1;
  const o1 = $(".o1", ide.btabs), o2 = $(".o2", ide.btabs);
  styleAt(o2, "display", [[0, "none"], [tOpen, "flex"]]);
  dyn((t) => { o1.className = t >= tOpen ? "o1" : "on o1"; o2.className = t >= tOpen ? "on o2" : "o2"; });
  styleAt(ide.out, "display", [[0, "block"], [tOpen, "none"]]);
  styleAt(ide.serial, "display", [[0, "none"], [tOpen, "block"]]);
  cam(tOpen + 0.3, 1.0, 640, 900, 1.7);
  // s24: back to the code for the floating experiment, then the monitor again
  cam(W(s24, "Change") - 0.2, 0.9, 520, 300, 1.8);
  ring(camera, cx(2) - 4, lineY(7) - 1, cx(36) - cx(2) + 8, 24, W(s24, "Change"), W(s24, "upload"));
  cam(W(s24, "upload") + 0.2, 0.8, 960, 540, 1);
  cam(T(s25) - 0.1, 0.9, 640, 900, 1.7);
  const pressed = [[W(s23, "Press"), W(s23, "Let")]];
  const tFloatRun = uploads[1][1] + 0.3;
  const rnd = (k) => { let x = Math.sin(k * 78.233) * 43758.5453; return x - Math.floor(x); };
  dyn((t) => {
    if (t < tOpen) return;
    const k = Math.floor((t - tOpen) / 0.08);
    const lines = [];
    for (let i = Math.max(0, k - 6); i <= k; i++) {
      const ti = tOpen + i * 0.08;
      let v;
      if (ti >= uploads[1][0] && ti < tFloatRun) v = null;
      else if (ti >= tFloatRun && ti < tFloatBack) v = rnd(i) < (ti >= W(s25, "Touch") ? 0.5 : 0.25) ? 0 : 1;
      else v = inAny(ti, pressed) ? 0 : 1;
      if (v !== null) lines.push(v);
    }
    const html = `<div style="display:flex;gap:12px;align-items:center;margin:-2px 0 8px;font-family:var(--ui)"><div class="ide-in" style="flex:1;color:#888">Message (Enter to send message to 'ESP32 Dev Module' on 'COM3')</div>
      <div class="ide-in" style="width:110px">New Line ▾</div><div class="ide-in" style="width:130px;${t >= W(s22, "115200") - 0.3 && t < W(s22, "115200") + 1.5 ? "border-color:#ffb547" : ""}">115200 baud ▾</div></div>` +
      lines.map((l) => `<div>${l}</div>`).join("");
    if (ide.serial.__v !== html) { ide.serial.innerHTML = html; ide.serial.__v = html; }
  });
  // live button + LED next to the monitor
  const live = box(stage, 1380, 90, 480, 330, "card", "");
  css(live, { zIndex: 50 }); hidden(live); show(live, T(s23) - 0.3, 0.3); hide(live, S1(s23) + 0.6, 0.4);
  const B = btnIcon(live, 50, 70, 150); B.press(pressed);
  const L = ledIcon(live, 300, 50, 110);
  L.drive((t) => (inAny(t, pressed) ? 1 : 0));
  callout(camera, "1 = HIGH (not pressed)", 220, IDE.outTop + 70, W(s23, "one"), W(s23, "Press"), { style: { zIndex: 60 } });
  callout(camera, "0 = LOW (pressed)", 220, IDE.outTop + 70, W(s23, "zero"), S1(s23) + 0.3);
  clipFrame(stage, "C2", 1140, 560, 720, 405, W(s23, "Press") - 0.2, S1(s23) + 1.8, "Holding the button: the LED lights; let go: dark.");
  const fl = box(stage, 1240, 120, 620, 80, "", `<span class="pill" style="font-size:30px;background:rgba(255,181,71,.18);color:var(--amber)">floating: the numbers jump around</span>`);
  css(fl, { zIndex: 55 }); hidden(fl); pop(fl, W(s25, "jump")); hide(fl, tFloatBack, 0.3);
  const calm = box(stage, 1240, 120, 620, 80, "", `<span class="pill" style="font-size:30px">INPUT_PULLUP again: calm</span>`);
  css(calm, { zIndex: 55 }); hidden(calm); pop(calm, tFloatBack + 0.2); hide(calm, S1(s25) + 0.4, 0.3);
}

/* ======================================================================
 * TOGGLE, EDGES AND BOUNCE (s26-s33)
 * ==================================================================== */
const sTog = SC();
sceneIn(sTog, S1("s25") + 0.5);
sceneOut(sTog, S1("s33") + 0.4);
{
  const h = head(sTog, "Press once: on · press again: off", 70); show(h, T("s26"));
  const V = (cnt, deb, hlc) => {
    const H = (n, s) => (hlc === n ? hl(s) : s);
    let c = `${kw("int")} state = ${fn("digitalRead")}(BUTTON_PIN);\n` +
      H(1, `${kw("if")} (state != lastState) {`) + `   ${cm("// it changed")}\n` +
      `  ` + H(1, `${kw("if")} (state == LOW) {`) + `     ${cm("// ...to pressed")}\n`;
    if (cnt) c += `    presses++;\n    Serial.${fn("println")}(presses);\n`;
    c += `    ` + H(2, `ledOn = !ledOn;`) + `\n    ${fn("digitalWrite")}(LED_PIN, ` + H(3, `ledOn ? HIGH : LOW`) + `);\n  }\n`;
    if (deb) c += `  ` + hl(`${fn("delay")}(${num(50)});`, "rgba(25,195,180,.25)") + `       ${cm("// debounce")}\n`;
    c += `}\nlastState = state;`;
    return c;
  };
  const card = codeCard(sTog, 90, 190, 930, 640, [[0, V(0, 0, 0)], [W("s27", "changes"), V(0, 0, 1)], [W("s29", "exclamation"), V(0, 0, 2)],
    [W("s29", "question"), V(0, 0, 3)], [T("s30"), V(1, 0, 0)], [W("s32", "wait"), V(1, 1, 0)]], 29);
  show(card, T("s27") - 0.4, 0.4);
  // right side: button + LED + press counter
  const presses = [[W("s26", "once"), W("s26", "once") + 0.35], [W("s26", "more"), W("s26", "more") + 0.35],
    [W("s27", "new"), W("s27", "new") + 0.35], [W("s30", "Press") + 0.3, W("s30", "Press") + 0.65],
    [W("s33", "every"), W("s33", "every") + 0.35], [W("s33", "flips"), W("s33", "flips") + 0.35]];
  const B = btnIcon(sTog, 1150, 200, 150); B.press(presses);
  hidden(B.r); hidden(B.lab); show([B.r, B.lab], T("s26"), 0.4);
  const L = ledIcon(sTog, 1560, 190, 110);
  const flips = presses.map((p) => p[0]);
  L.drive((t) => flips.filter((f) => t >= f).length % 2);
  // s30: a counter that jumps
  const ctr = box(sTog, 1100, 480, 720, 90, "", "");
  css(ctr, { textAlign: "center", font: "700 44px var(--mono)" }); hidden(ctr); show(ctr, T("s30"), 0.3); hide(ctr, T("s31") + 0.2, 0.3);
  const tJ = W("s30", "Press") + 0.3;
  textAt(ctr, [[0, "presses: 0"], [tJ, "presses: 3 <span style='color:var(--red);font-size:30px'>?!</span>"], [W("s30", "two"), "presses: 5 <span style='color:var(--red);font-size:30px'>+2 ?!</span>"],
    [W("s30", "three"), "presses: 8 <span style='color:var(--red);font-size:30px'>+3 ?!</span>"]]);
  const ctr2 = box(sTog, 1100, 480, 720, 90, "", "");
  css(ctr2, { textAlign: "center", font: "700 44px var(--mono)" }); hidden(ctr2); show(ctr2, T("s33"), 0.3);
  textAt(ctr2, [[0, "presses: 0"], [W("s33", "every"), "presses: 1"], [W("s33", "flips"), "presses: 2"]]);
  // s28: the edge on a timeline
  const sv = svgLayer(sTog);
  const tlg = svgEl(sv, "g", { opacity: 0 });
  TO(tlg, T("s28"), 0.4, { opacity: 1 }); TO(tlg, T("s29") - 0.1, 0.3, { opacity: 0 });
  const X0 = 1100, X1 = 1800, YH = 690, YL = 830, XE = 1520;
  svgEl(tlg, "path", { d: `M${X0} ${YH} H${XE} V${YL} H${X1}`, stroke: "#ffb547", "stroke-width": 7, fill: "none" });
  ["HIGH", "HIGH", "HIGH"].forEach((s, i) => { const tx = svgEl(tlg, "text", { x: X0 + 70 + i * 140, y: YH - 20, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 26, fill: "#19c3b4" }); tx.textContent = s; });
  const lowT = svgEl(tlg, "text", { x: 1660, y: YL - 20, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 26, fill: "#6ea8ff" }); lowT.textContent = "LOW";
  const edge = svgEl(tlg, "circle", { cx: XE, cy: (YH + YL) / 2, r: 30, fill: "none", stroke: "#ff5d6c", "stroke-width": 5, opacity: 0 });
  TO(edge, W("s28", "moment"), 0.3, { opacity: 1 });
  const eLab = svgEl(tlg, "text", { x: XE, y: YL + 60, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 30, fill: "#ff5d6c", opacity: 0 });
  eLab.textContent = "the edge = the press";
  TO(eLab, W("s28", "edge") - 0.3, 0.3, { opacity: 1 });
  // s29: bool, !, ?:
  const notes = [["bool ledOn  →  true / false", W("s29", "bool")], ["!ledOn  →  not: swaps it", W("s29", "exclamation")], ["ledOn ? HIGH : LOW  →  picks one", W("s29", "question")]];
  notes.forEach(([txt, t], i) => {
    const n = box(sTog, 1080, 630 + i * 100, 760, 80, "card", `<div style="padding:18px 26px;font:600 28px var(--mono)">${esc(txt)}</div>`);
    hidden(n); pop(n, t); hide(n, T("s30"), 0.3);
  });
  // s31-s32: contact bounce
  const bg = svgEl(sv, "g", { opacity: 0 });
  TO(bg, W("s31", "bounce") - 0.2, 0.4, { opacity: 1 }); TO(bg, T("s33") - 0.1, 0.3, { opacity: 0 });
  let d = `M${X0} ${YH} H1300`;
  const bx = [1300, 1322, 1340, 1362, 1376, 1396, 1406, 1424, 1432];
  bx.forEach((x, i) => { d += ` H${x} V${i % 2 ? YH : YL}`; });
  d += ` H${X1}`;
  svgEl(bg, "path", { d, stroke: "#ffb547", "stroke-width": 6, fill: "none" });
  const fewT = svgEl(bg, "text", { x: 1370, y: YH - 24, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 24, fill: "#8fa1c0" }); fewT.textContent = "a few ms";
  const fiveT = svgEl(bg, "text", { x: 1450, y: YL + 60, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 30, fill: "#ff5d6c", opacity: 0 });
  fiveT.textContent = "1 press → 5 edges";
  TO(fiveT, W("s31", "five") - 0.2, 0.3, { opacity: 1 }); TO(fiveT, W("s32", "wait"), 0.3, { opacity: 0 });
  const win = svgEl(bg, "rect", { x: 1300, y: YH - 50, width: 360, height: YL - YH + 100, rx: 10, fill: "rgba(25,195,180,.18)", stroke: "#19c3b4", "stroke-width": 3, opacity: 0 });
  TO(win, W("s32", "wait"), 0.4, { opacity: 1 });
  const winT = svgEl(bg, "text", { x: 1480, y: YL + 90, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 30, fill: "#19c3b4", opacity: 0 });
  winT.textContent = "wait 50 ms: bounce ignored";
  TO(winT, W("s32", "fifty"), 0.3, { opacity: 1 });
  const ok = pill(sTog, 1110, 600, "✓ one press = one count = one flip", "");
  pop(ok, W("s33", "exactly")); hide(ok, W("s33", "sketch"), 0.3);
  clipFrame(sTog, "C3", 1100, 600, 720, 405, W("s33", "sketch") - 0.2, S1("s33") + 1.3, "Toggle: press, LED on; press again, LED off.");
}

/* ======================================================================
 * WHY delay() GETS IN THE WAY (s34-s37)
 * ==================================================================== */
const sBlock = SC();
sceneIn(sBlock, S1("s33") + 0.4);
sceneOut(sBlock, S1("s37") + 0.4);
{
  const hd = box(sBlock, 0, 70, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s34"), "Part 2: blink + button"], [W("s35", "freezes"), "delay() freezes everything"]]);
  const D2 = (hlDelay, n = 500) => {
    const dl = (s) => (hlDelay ? hl(s, "rgba(255,93,108,.3)") : s);
    return `${kw("void")} ${fn("loop")}() {\n  ${kw("if")} (${fn("digitalRead")}(BUTTON_PIN) == LOW) {\n    blinking = !blinking;\n  }\n  ${kw("if")} (blinking) {\n` +
      `    ${fn("digitalWrite")}(LED_PIN, HIGH);\n    ` + dl(`${fn("delay")}(${num(n)});`) + `\n    ${fn("digitalWrite")}(LED_PIN, LOW);\n    ` + dl(`${fn("delay")}(${num(n)});`) + `\n  }\n}`;
  };
  const card = codeCard(sBlock, 90, 190, 860, 620, [[0, D2(0)], [W("s35", "freezes"), D2(1)], [W("s37", "shorter"), D2(1, 100)]], 30);
  show(card, W("s35", "obvious"), 0.4);
  const L = ledIcon(sBlock, 1560, 190, 100);
  hidden(L.r); show(L.r, T("s34"), 0.4);
  const tB = T("s34") + 0.5;
  L.drive((t) => blink(t, tB, 0.5, 0.5));
  // what the loop spends its time on
  const sv = svgLayer(sBlock);
  const X0 = 1040, X1 = 1820;
  const mk = (y, period, t0, t1) => {
    const g = svgEl(sv, "g", { opacity: 0 });
    TO(g, t0, 0.4, { opacity: 1 }); if (t1) TO(g, t1, 0.3, { opacity: 0 });
    const px = (X1 - X0) / 3; // 3 seconds across
    for (let x = X0; x < X1 - 1; x += px * period * 2) {
      svgEl(g, "rect", { x, y, width: 8, height: 70, fill: "#4ade80" });
      svgEl(g, "rect", { x: x + 10, y, width: Math.min(px * period * 2 - 12, X1 - x - 10), height: 70, rx: 6, fill: "rgba(255,93,108,.55)" });
    }
    return g;
  };
  mk(540, 0.5, W("s35", "freezes"), W("s37", "shorter"));
  mk(540, 0.1, W("s37", "shorter"));
  const k1 = box(sBlock, X0, 630, 800, 40, "", `<div style="font:600 24px var(--ui)"><span style="color:#4ade80">▮ looks at the button</span> &nbsp; <span style="color:#ff8a94">▮ waiting in delay()</span></div>`);
  hidden(k1); show(k1, W("s35", "waits"), 0.4);
  const miss = box(sBlock, X0 + 300, 430, 300, 110, "", `<div style="text-align:center;font:800 30px var(--ui);color:var(--red)">press ✕ missed<div style="font-size:50px;line-height:50px">↓</div></div>`);
  hidden(miss); pop(miss, W("s36", "missed")); hide(miss, W("s37", "shorter"), 0.3);
  const miss2 = box(sBlock, X0 + 470, 430, 300, 110, "", `<div style="text-align:center;font:800 30px var(--ui);color:var(--red)">still slips through<div style="font-size:50px;line-height:50px">↓</div></div>`);
  hidden(miss2); pop(miss2, W("s37", "slip"));
  const goal = pillC(sBlock, 470, "the LED blinks · the button switches the blinking on and off", "font-size:32px");
  pop(goal, W("s34", "blinking")); hide(goal, W("s35", "obvious"), 0.3);
  const real = pillC(sBlock, 900, "the real fix: a different way of thinking", "font-size:32px");
  pop(real, W("s37", "real"));
}

/* ======================================================================
 * millis(): CHECK THE CLOCK, DON'T WAIT (s38-s46)
 * ==================================================================== */
const sMil = SC();
sceneIn(sMil, S1("s37") + 0.4);
sceneOut(sMil, S1("s46") + 0.4);
{
  const hd = box(sMil, 0, 60, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s38"), "Never wait: look at the clock"], [T("s42"), "unsigned long, and always subtract"],
    [T("s44"), "The button: same trick"], [T("s45"), "A loop that never waits"], [T("s46"), "Two things at once"]]);
  const t0 = T("s38") - 0.6;
  const clock = box(sMil, 0, 170, 1920, 150, "", "");
  hidden(clock); show(clock, T("s38"), 0.4); hide(clock, T("s44") - 0.1, 0.3);
  dyn((t) => {
    if (t < t0) return;
    const ms = Math.max(0, Math.round((t - t0) * 1000) + 3000);
    const html = `<div style="text-align:center;font:700 92px var(--mono)">${fn("millis")}() = <span style="color:var(--teal)">${ms.toLocaleString("en-US")}</span></div>`;
    if (clock.__v !== html) { clock.innerHTML = html; clock.__v = html; }
  });
  const sub = pillC(sMil, 330, "milliseconds since the board started", "background:transparent;color:var(--muted)");
  pop(sub, W("s38", "milliseconds")); hide(sub, T("s40"), 0.3);
  // s39: printed every second
  const con = box(sMil, 610, 430, 700, 380, "card", "");
  css(con, { font: "600 34px var(--mono)", padding: "24px 36px", lineHeight: "1.5" }); hidden(con); show(con, T("s39"), 0.4); hide(con, T("s40") - 0.1, 0.3);
  dyn((t) => {
    if (t < T("s39")) return;
    const n = Math.floor(t - T("s39")) + 1;
    const lines = [];
    for (let i = Math.max(1, n - 5); i <= n; i++) lines.push(`${i * 1000 + 3000}`);
    const html = `<div style="color:var(--muted);font:600 22px var(--ui);margin-bottom:6px">Serial Monitor</div>` + lines.map((l) => `<div>${l}</div>`).join("");
    if (con.__v !== html) { con.innerHTML = html; con.__v = html; }
  });
  // s40: the pattern
  const P1 = (hlc) => {
    const H = (n, s) => (hlc === n ? hl(s) : s);
    return `${kw("unsigned long")} now = ${fn("millis")}();\n${kw("if")} (` + H(1, `now - lastBlink >= ${num(500)}`) + `) {\n  ` + H(2, `lastBlink = now;`) +
      `\n  ledOn = !ledOn;\n  ${fn("digitalWrite")}(LED_PIN, ledOn ? HIGH : LOW);\n}`;
  };
  const P2 = `${kw("int")} state = ${fn("digitalRead")}(BUTTON_PIN);\n${kw("if")} (state != lastState &&\n    ` + hl(`now - lastChange >= ${num(50)}`) + `) {\n  lastChange = now;\n  lastState = state;\n  ${kw("if")} (state == LOW) blinking = !blinking;\n}`;
  const card = codeCard(sMil, 90, 400, 1000, 400, [[0, P1(0)], [W("s40", "passed"), P1(1)], [W("s40", "note"), P1(2)], [W("s40", "move"), P1(0)],
    [W("s42", "subtract"), P1(1)], [T("s43"), P1(0)], [T("s44"), P2]], 30);
  show(card, T("s40"), 0.4); hide(card, T("s45") - 0.1, 0.3);
  // s41: worked example
  const rows = [["last = 700", W("s41", "seven")], ["now = 1000 → 1000 − 700 = 300", W("s41", "minus")], ["<span style='color:var(--muted)'>not yet</span>", W("s41", "not")],
    ["now = 1200 → 1200 − 700 = 500", W("s41", "Later")], ["<span style='color:var(--teal)'>≥ 500: flip!</span>", W("s41", "flip")], ["last = 1200", W("s41", "becomes")]];
  const ex = box(sMil, 1150, 400, 690, 470, "card", "");
  hidden(ex); show(ex, T("s41"), 0.4); hide(ex, T("s42"), 0.3);
  rows.forEach(([txt, t], i) => {
    const r = box(ex, 34, 30 + i * 70, 640, 60, "", `<div style="font:600 30px var(--mono)">${txt}</div>`);
    hidden(r); pop(r, t);
  });
  // s42-s43: unsigned long, roll-over
  const ty = box(sMil, 1150, 400, 690, 200, "card", `<div style="padding:28px 34px"><div style="font:700 34px var(--mono);color:var(--amber)">unsigned long</div>
    <div style="font:600 28px var(--ui);margin-top:12px">0 … 4,294,967,295</div><div class="muted" style="font-size:24px;margin-top:8px">a big whole number, never negative</div></div>`);
  hidden(ty); pop(ty, W("s42", "unsigned")); hide(ty, S1("s43") + 0.1, 0.3);
  const ro = box(sMil, 1150, 630, 690, 240, "card", `<div style="padding:24px 34px;font:600 26px var(--mono);line-height:1.6">
    <div style="font:700 28px var(--ui);color:var(--muted)">after ~49.7 days: … 4,294,967,295 → 0</div>
    <div>last = 4,294,967,000</div><div>now = 200</div><div>now − last = <span style="color:var(--teal)">496 ✓</span></div></div>`);
  hidden(ro); pop(ro, W("s43", "fortynine")); hide(ro, T("s44"), 0.3);
  const okS = pill(sMil, 1150, 890, "✓ subtraction still works", "");
  pop(okS, W("s43", "subtraction")); hide(okS, T("s44"), 0.3);
  // s44: the button with the same trick (right side note)
  const bn = box(sMil, 1150, 400, 690, 200, "card", `<div style="padding:28px 34px;font:600 30px var(--display)">changes within 50 ms of the last one<br><span style="color:var(--teal)">→ ignored (that's the bounce)</span></div>`);
  hidden(bn); pop(bn, W("s44", "ignore")); hide(bn, T("s45"), 0.3);
  // s45: the never-waiting loop
  const spin = box(sMil, 610, 330, 700, 560, "", `<svg width="700" height="560" viewBox="0 0 700 560">
    <circle cx="350" cy="280" r="200" fill="none" stroke="#22304d" stroke-width="18"/>
    <path class="arc" d="M350 80 A200 200 0 0 1 550 280" fill="none" stroke="#19c3b4" stroke-width="18" stroke-linecap="round"/>
    <text x="350" y="270" text-anchor="middle" font-family="Consolas, monospace" font-weight="700" font-size="44" fill="#e8eef7">loop()</text>
    <text x="350" y="320" text-anchor="middle" font-family="Segoe UI" font-weight="600" font-size="26" fill="#8fa1c0">thousands of times a second</text></svg>`);
  hidden(spin); show(spin, T("s45"), 0.4); hide(spin, S1("s45") + 0.1, 0.3);
  const arc = $(".arc", spin);
  dyn((t) => { if (t >= T("s45") - 0.5 && t < S1("s45") + 0.5) arc.setAttribute("transform", `rotate(${(t * 900) % 360} 350 280)`); });
  for (const [txt, x, y, w] of [["✓ button?", 330, 420, "button"], ["✓ clock?", 1330, 420, "clock"]]) {
    const c = box(sMil, x, y, 260, 70, "", `<span class="pill" style="font-size:30px">${txt}</span>`);
    hidden(c); pop(c, W("s45", w)); hide(c, S1("s45") + 0.1, 0.3);
  }
  // s46: the result
  const tRun = T("s46"), tStop = W("s46", "press"), tGo = W("s46", "Press", 2);
  const B = btnIcon(sMil, 330, 470, 170); hidden(B.r); hidden(B.lab); show([B.r, B.lab], tRun, 0.4);
  B.press([[tStop, tStop + 0.35], [tGo, tGo + 0.35]]);
  const L = ledIcon(sMil, 700, 400, 130); hidden(L.r); show(L.r, tRun, 0.4);
  L.drive((t) => (t < tStop || t >= tGo ? blink(t, tRun, 0.5, 0.5) : 0));
  clipFrame(sMil, "C4", 1100, 300, 720, 405, tRun + 0.2, S1("s46") + 1.8, "The LED blinks; a press stops it at once, another starts it again.");
}

/* ======================================================================
 * TWO LEDS, TWO TIMERS (s50-s52)
 * ==================================================================== */
const sTwo = SC();
sceneIn(sTwo, S1("s49") + 0.5);
sceneOut(sTwo, S1("s52") + 0.4);
{
  const h = head(sTwo, "Two LEDs, two timers", 70); show(h, T("s50"));
  const C = `${kw("if")} (now - lastRed >= ${num(500)}) {     ${cm("// red")}\n  lastRed = now;\n  ${cm("// ...flip the red LED")}\n}\n` +
    `${kw("if")} (now - lastGreen >= ${num(150)}) {   ${cm("// green")}\n  lastGreen = now;\n  ${cm("// ...flip the green LED")}\n}`;
  const card = codeCard(sTwo, 90, 200, 960, 500, [[0, C]], 30);
  show(card, T("s50"), 0.4); hide(card, T("s51") - 0.1, 0.3);
  const tA = T("s50"), tStop = W("s51", "reacts");
  const R = ledIcon(sTwo, 1230, 220, 120, "red"), G = ledIcon(sTwo, 1560, 220, 120, "green");
  hidden(R.r); hidden(G.r); show([R.r, G.r], tA, 0.4);
  R.drive((t) => (t < tStop ? blink(t, tA, 0.5, 0.5) : 0));
  G.drive((t) => blink(t, tA, 0.15, 0.15));
  for (const [txt, x, w] of [["every 500 ms", 1180, "five"], ["every 150 ms", 1510, "fifty"]]) {
    const l = box(sTwo, x, 470, 220, 40, "", `<div style="text-align:center;font:700 26px var(--ui);color:var(--muted)">${txt}</div>`);
    hidden(l); pop(l, W("s50", w)); hide(l, T("s52") - 0.1, 0.3);
  }
  const B = btnIcon(sTwo, 1400, 580, 140); hidden(B.r); hidden(B.lab); show([B.r, B.lab], T("s51"), 0.4);
  B.press([[tStop, tStop + 0.35]]);
  clipFrame(sTwo, "C6", 120, 260, 720, 405, T("s51") + 0.2, S1("s51") + 1.8, "Red and green blink at their own speeds; a press stops the red one.");
  const ch = box(sTwo, 300, 300, 1320, 420, "card", `<div style="padding:44px 60px"><div class="kicker">Your challenge</div>
    <div style="font:700 48px var(--display);margin:16px 0 20px">The button switches the green LED<br>between fast and slow</div>
    <div class="muted" style="font-size:28px">fast (150 ms) → slow (600 ms) → fast … &nbsp;·&nbsp; one solution: <span style="font-family:var(--mono);color:var(--teal)">challenge_speed</span> on GitHub</div></div>`);
  hidden(ch); pop(ch, W("s52", "challenge"));
  hide([R.r, G.r, B.r, B.lab], T("s52") - 0.1, 0.3);
}

/* ======================================================================
 * NOT WORKING? (s53)
 * ==================================================================== */
const sTrouble = SC();
sceneIn(sTrouble, S1("s52") + 0.4);
sceneOut(sTrouble, S1("s53") + 0.5);
{
  const chk = box(sTrouble, 300, 170, 1320, 760, "card", "");
  const rows = [["Button across the middle gap", "across"], ["Yellow wire in the D22 column", "yellow"], ["Always 0? Button turned sideways", "always"], ["Green dark? Top − rail wired to GND", "green"]];
  chk.innerHTML = `<div style="padding:44px 60px"><div class="kicker">Something not working?</div>` + rows.map(([a]) => `<div class="row" style="display:flex;gap:22px;align-items:center;margin-top:40px;opacity:0">
    <div style="width:56px;height:56px;border-radius:50%;background:var(--green);color:#052;font:800 32px var(--ui);display:flex;align-items:center;justify-content:center">✓</div>
    <div style="font:600 40px var(--display)">${a}</div></div>`).join("") + `</div>`;
  chk.querySelectorAll(".row").forEach((r, i) => TO(r, W("s53", rows[i][1]), 0.4, { opacity: 1 }));
}

/* ======================================================================
 * OUTRO (s54-s56)
 * ==================================================================== */
const sOutro = SC();
sceneIn(sOutro, S1("s53") + 0.5);
{
  const h = box(sOutro, 110, 200, 1500, 80, "h2", "Episode 4 complete!"); hidden(h); pop(h, T("s54"));
  const items = [["digitalRead", "HIGH or LOW"], ["INPUT_PULLUP", "the built-in pull-up"], ["Debounce", "wait out the bounce"], ["millis()", "check the clock, don't wait"]];
  const cards = items.map(([a, b], i) => {
    const c = box(sOutro, 110 + i * 435, 380, 400, 300, "card", `<div style="padding:34px"><div style="width:64px;height:64px;border-radius:50%;background:rgba(25,195,180,.15);color:var(--teal);font:700 32px var(--display);display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div style="font:700 34px var(--display);margin-top:28px">${a}</div><div class="muted" style="font-size:23px;margin-top:8px">${b}</div></div>
      <div class="ok" style="position:absolute;right:26px;top:26px;width:58px;height:58px;border-radius:50%;background:var(--green);color:#052;font:700 34px var(--ui);display:flex;align-items:center;justify-content:center;opacity:0">✓</div>`);
    hidden(c);
    return c;
  });
  ["digital", "pullup", "bounce", "millis"].forEach((w, i) => {
    pop(cards[i], W("s54", w) - 0.15);
    const ok = $(".ok", cards[i]);
    SET(ok, W("s54", w) + 0.2, { scale: 0.4 });
    TO(ok, W("s54", w) + 0.2, 0.4, { opacity: 1, scale: 1, ease: "back.out(2)" });
  });
  hide(cards, T("s55") - 0.1, 0.4); hide(h, T("s55") - 0.1, 0.4);
  const sk = [["button_led", "LED"], ["button_toggle", "toggle"], ["blink_button", "blink"], ["two_leds", "two"], ["challenge_speed", "challenge"]];
  const h2 = box(sOutro, 110, 200, 1500, 80, "h2", "Five sketches, ready to upload"); hidden(h2); pop(h2, T("s55")); hide(h2, T("s56") - 0.1, 0.4);
  sk.forEach(([nm, w], i) => {
    const c = box(sOutro, 110 + (i % 3) * 580, 360 + Math.floor(i / 3) * 170, 540, 130, "card", `<div style="height:130px;display:flex;align-items:center;gap:20px;padding:0 34px">
      <div style="font:700 30px var(--display);color:var(--teal)">${i + 1}</div><div style="font:700 34px var(--mono)">${nm}</div></div>`);
    hidden(c); pop(c, W("s55", w) - 0.1); hide(c, T("s56") - 0.1, 0.4);
  });
  const nx = box(sOutro, 260, 260, 1400, 330, "card", `<div style="padding:50px 60px"><div class="kicker">Next episode</div>
    <div style="font:700 60px var(--display);margin:14px 0 18px">Dimming, colors and a knob</div>
    <div class="muted" style="font-size:28px">Fade an LED with PWM, mix colors with an RGB LED, read a potentiometer.</div></div>`);
  hidden(nx); pop(nx, T("s56") + 0.2);
  const gh = box(sOutro, 260, 640, 1400, 120, "card", `<div style="display:flex;align-items:center;gap:26px;height:120px;padding:0 50px">
    <svg width="54" height="54" viewBox="0 0 16 16"><path fill="#fff" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.290 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
    <div style="font:600 36px var(--mono)">github.com/emjnbulut/esp32-from-zero</div></div>`);
  hidden(gh); pop(gh, W("s56", "GitHub"));
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 });
  TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}

window.__seek(0);
window.__ready = true;
