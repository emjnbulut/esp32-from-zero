/* Episode 2 - Meet the Board and the Breadboard. All times come from the narration schedule. */
const stage = $("#stage");
const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const NS = "http://www.w3.org/2000/svg";
function svgEl(parent, tag, attrs = {}) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  parent.appendChild(e);
  return e;
}
function svgLayer(parent, w = 1920, h = 1080) {
  const s = svgEl(parent, "svg", { width: w, height: h, viewBox: `0 0 ${w} ${h}` });
  css(s, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  return s;
}
/** draw a path on over [t, t+dur] */
function drawOn(path, t, dur = 0.6) {
  const L = path.getTotalLength();
  path.setAttribute("stroke-dasharray", `${L} ${L}`);
  path.style.strokeDashoffset = L;
  TO(path, t, dur, { strokeDashoffset: 0, ease: "power2.out" });
}
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
const clamp01 = (v) => Math.max(0, Math.min(1, v));

/* ---------- part drawings (side views, for cards) ---------- */
const ART = {
  led: (w = 120) => `<svg width="${w}" viewBox="0 0 120 230"><defs><radialGradient id="ledg${w}" cx=".4" cy=".35"><stop offset="0" stop-color="#ff8a8f"/><stop offset="1" stop-color="#d4202c"/></radialGradient></defs>
    <path d="M44 96 V226" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/><path d="M76 96 V186" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/>
    <path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="url(#ledg${w})" opacity=".95"/><path d="M22 92 h70 v14 h-70 z" fill="#b51d27"/><path d="M92 92 v14" stroke="#7c121a" stroke-width="5"/></svg>`,
  resistor: (w = 240) => `<svg width="${w}" viewBox="0 0 240 70"><path d="M4 35 H236" stroke="#c3c9d1" stroke-width="5" stroke-linecap="round"/>
    <rect x="62" y="14" width="116" height="42" rx="18" fill="#dcc79f"/><rect x="82" y="14" width="11" height="42" fill="#d0262f"/><rect x="102" y="14" width="11" height="42" fill="#d0262f"/>
    <rect x="122" y="14" width="11" height="42" fill="#7a4a21"/><rect x="152" y="14" width="9" height="42" fill="#c9a54a"/></svg>`,
  wires: (w = 220) => `<svg width="${w}" viewBox="0 0 220 180"><g fill="none" stroke-width="9" stroke-linecap="round">
    <path d="M20 40 C 80 -10, 140 110, 200 50" stroke="#ff5d6c"/><path d="M20 95 C 80 45, 140 165, 200 105" stroke="#4f8dff"/><path d="M20 150 C 80 100, 140 220, 200 160" stroke="#ffd34d"/></g>
    <g fill="#222">${[40, 95, 150].map((y) => `<rect x="4" y="${y - 6}" width="20" height="12" rx="2"/><rect x="196" y="${y + 4}" width="20" height="12" rx="2"/>`).join("")}</g></svg>`,
  breadboard: (w = 230) => {
    let h = "";
    for (let c = 0; c < 12; c++) for (let r = 0; r < 10; r++) h += `<rect x="${22 + c * 16}" y="${(r < 5 ? 40 : 66) + r * 14}" width="7" height="7" rx="1.5" fill="#55534c"/>`;
    for (let c = 0; c < 12; c++) for (const y of [14, 26, 206, 218]) h += `<rect x="${22 + c * 16}" y="${y}" width="7" height="7" rx="1.5" fill="#55534c"/>`;
    return `<svg width="${w}" viewBox="0 0 230 240"><rect x="2" y="2" width="226" height="236" rx="12" fill="#ecebe6"/><rect x="8" y="113" width="214" height="12" rx="3" fill="#d6d3cb"/>
      <path d="M14 10 H216" stroke="#e5484d" stroke-width="2"/><path d="M14 36 H216" stroke="#3b6fe0" stroke-width="2"/><path d="M14 202 H216" stroke="#e5484d" stroke-width="2"/><path d="M14 228 H216" stroke="#3b6fe0" stroke-width="2"/>${h}</svg>`;
  },
};

/* ======================================================================
 * INTRO (s01-s02)
 * ==================================================================== */
const sIntro = SC();
SET(sIntro, 0, { opacity: 1 });
{
  const kick = box(sIntro, 140, 300, 600, 40, "kicker", "Episode 02");
  const title = box(sIntro, 136, 336, 1000, 140, "h1", "ESP32 From Zero");
  title.style.fontSize = "112px";
  const sub = box(sIntro, 140, 486, 1000, 60, "h3", "Meet the Board and the Breadboard");
  sub.style.color = "var(--teal)";
  const persp = box(sIntro, 1130, 70, 560, 900, "");
  persp.style.perspective = "1600px";
  const b3d = box(persp, 0, 0, 560, 900, "", boardSVG({ pins: 30, chip: "cp2102", p: "bi", width: 520 }));
  css(b3d, { filter: "drop-shadow(0 40px 60px rgba(0,0,0,.6)) drop-shadow(0 0 40px rgba(25,195,180,.25))" });
  gsap.set(b3d, { rotationY: -28, rotationX: 18, y: 60, opacity: 0 });
  TO(b3d, 0.3, 1.6, { opacity: 1, y: 0, ease: "power3.out" });
  TO(b3d, 0.3, 22, { rotationY: 12, rotationX: 8, ease: "sine.inOut" });
  for (const [e, t] of [[kick, 0.5], [title, 0.75], [sub, 1.1]]) {
    gsap.set(e, { opacity: 0, y: 30 });
    TO(e, t, 0.8, { opacity: 1, y: 0, ease: "power3.out" });
  }
  const items = [["The pins", "power, ground, GPIO"], ["The breadboard", "circuits without soldering"], ["First circuit", "light an LED"]];
  ["pins", "breadboard", "circuit"].forEach((w, i) => {
    const c = box(sIntro, 140 + i * 330, 600, 300, 140, "card", `<div style="padding:22px 24px"><div class="kicker" style="font-size:16px">Today · ${i + 1}</div>
      <div style="font:600 29px var(--display);margin-top:8px">${items[i][0]}</div><div class="muted" style="font-size:19px;margin-top:4px">${items[i][1]}</div></div>`);
    hidden(c); pop(c, W("s02", w));
  });
  sceneOut(sIntro, S1("s02") + 0.4);
}

/* ======================================================================
 * KIT (s03)
 * ==================================================================== */
const sKit = SC();
sceneIn(sKit, S1("s02") + 0.4);
{
  const h = head(sKit, "What you need", 150); show(h, T("s03"));
  const parts = [
    ["ESP32 board", "30 or 38 pins", boardSVG({ pins: 30, chip: "cp2102", p: "bk", width: 128, labels: false }), "ESP32"],
    ["Breadboard", "any size", ART.breadboard(220), "breadboard"],
    ["LED", "any color", ART.led(96), "LED"],
    ["Resistor", "220 Ω", ART.resistor(250), "resistor"],
    ["Jumper wires", "2 or 3", ART.wires(210), "jumper"],
  ];
  parts.forEach(([nm, ds, art, w], i) => {
    const c = box(sKit, 92 + i * 352, 300, 330, 420, "card partcard", `<div class="art" style="margin-top:34px">${art}</div><div class="nm" style="margin-top:22px">${nm}</div><div class="ds">${ds}</div>`);
    hidden(c); pop(c, W("s03", w));
  });
  const p = box(sKit, 0, 790, 1920, 60, "", `<div style="display:flex;justify-content:center"><span class="pill">✓&nbsp; All in a typical ESP32 starter kit</span></div>`);
  hidden(p); pop(p, W("s03", "kit"));
  sceneOut(sKit, S1("s03") + 0.4);
}

/* ======================================================================
 * PINS INTRO (s04-s05)
 * ==================================================================== */
const sPins = SC();
sceneIn(sPins, S1("s03") + 0.4);
{
  const bx = 250, by = 70, bw = 500, k = bw / 323;
  const b = box(sPins, bx, by, bw, 950, "", boardSVG({ pins: 30, chip: "cp2102", p: "bp", width: bw }));
  hidden(b); TO(b, T("s04"), 0.8, { opacity: 1, ease: "power2.out" });
  // header columns glow
  const n = 15, y0 = 515 - 40 - 14 * 25.4 - 30;
  for (const x of [22, 261]) {
    const r = box(sPins, bx + (x + 20) * k - 20, by + (y0 + 20) * k - 20, 40, 14 * 25.4 * k + 40, "ring");
    r.style.borderRadius = "14px";
    pop(r, W("s04", "row")); hide(r, S1("s05") + 1.0);
  }
  const t1 = box(sPins, 900, 300, 920, 200, "", `<div class="h2">Two rows of pins</div><div class="muted" style="font-size:32px;margin-top:16px">the ESP32's connections to the outside world</div>`);
  gsap.set(t1, { opacity: 0, x: -20 }); TO(t1, W("s04", "pins"), 0.6, { opacity: 1, x: 0 });
  const t2 = box(sPins, 900, 560, 920, 120, "", `<div style="display:flex;gap:18px;align-items:center"><span class="pill" style="font-size:26px">3V3 · GND · D2 · D4 …</span></div><div class="muted" style="font-size:28px;margin-top:16px">every pin has a tiny printed name</div>`);
  gsap.set(t2, { opacity: 0, x: -20 }); TO(t2, W("s05", "label"), 0.6, { opacity: 1, x: 0 });
  clipFrame(sPins, "C1", 320, 150, 1280, 720, T("s05") - 0.1, S1("s05") + 1.1, "Close-up: slowly pan along the pin labels (3V3, GND, D2...).");
  sceneOut(sPins, S1("s05") + 1.3);
}

/* ======================================================================
 * PIN CHARTS (s06-s19), safety overlay (s11-s12)
 * ==================================================================== */
const PINS = {
  30: {
    L: [["EN", null, "en"], ["VP", 36, "in"], ["VN", 39, "in"], ["D34", 34, "in"], ["D35", 35, "in"], ["D32", 32, "ok"], ["D33", 33, "ok"], ["D25", 25, "ok"],
      ["D26", 26, "ok"], ["D27", 27, "ok"], ["D14", 14, "ok"], ["D12", 12, "strap"], ["D13", 13, "ok"], ["GND", null, "gnd"], ["VIN", null, "5v"]],
    R: [["D23", 23, "ok"], ["D22", 22, "ok"], ["TX0", 1, "serial"], ["RX0", 3, "serial"], ["D21", 21, "ok"], ["D19", 19, "ok"], ["D18", 18, "ok"], ["D5", 5, "strap"],
      ["D17", 17, "ok"], ["D16", 16, "ok"], ["D4", 4, "ok"], ["D2", 2, "strap"], ["D15", 15, "strap"], ["GND", null, "gnd"], ["3V3", null, "3v3"]],
  },
  38: {
    L: [["3V3", null, "3v3"], ["EN", null, "en"], ["VP", 36, "in"], ["VN", 39, "in"], ["34", 34, "in"], ["35", 35, "in"], ["32", 32, "ok"], ["33", 33, "ok"], ["25", 25, "ok"],
      ["26", 26, "ok"], ["27", 27, "ok"], ["14", 14, "ok"], ["12", 12, "strap"], ["GND", null, "gnd"], ["13", 13, "ok"], ["D2", 9, "flash"], ["D3", 10, "flash"], ["CMD", 11, "flash"], ["5V", null, "5v"]],
    R: [["GND", null, "gnd"], ["23", 23, "ok"], ["22", 22, "ok"], ["TX", 1, "serial"], ["RX", 3, "serial"], ["21", 21, "ok"], ["GND", null, "gnd"], ["19", 19, "ok"], ["18", 18, "ok"],
      ["5", 5, "strap"], ["17", 17, "ok"], ["16", 16, "ok"], ["4", 4, "ok"], ["0", 0, "strap"], ["2", 2, "strap"], ["15", 15, "strap"], ["D1", 8, "flash"], ["D0", 7, "flash"], ["CLK", 6, "flash"]],
  },
};
const POWERNAME = { "3v3": "3.3 V", "5v": "5 V", gnd: "GND", en: "EN" };
function pinChart(parent, pins, bx, by, bw) {
  const k = bw / 323, Wb = 283, Hb = pins === 30 ? 515 : 544, n = pins / 2, pitch = 25.4;
  const y0 = Hb - 40 - (n - 1) * pitch - 30;
  const wrap = box(parent, 0, 0, 1920, 1080, "");
  box(wrap, bx, by, bw, (Hb + 70) * k, "", boardSVG({ pins, chip: pins === 30 ? "cp2102" : "ch340", p: "pc" + pins, width: bw }));
  const lines = svgLayer(wrap);
  const tags = [];
  for (const side of ["L", "R"]) PINS[pins][side].forEach(([label, gpio, cat], i) => {
    const px = bx + ((side === "L" ? 22 : Wb - 22) + 20) * k, py = by + (y0 + i * pitch + 20) * k;
    const tw = 138, th = 26, tx = side === "L" ? bx - 12 - tw : bx + bw + 12;
    const name = gpio == null ? POWERNAME[cat] : "GPIO " + gpio;
    const tag = box(wrap, tx, py - th / 2, tw, th, "ptag c-neutral", `<span class="n">${name}</span><span class="x"></span>`);
    const x1 = side === "L" ? tx + tw : tx, x2 = side === "L" ? px - 11 * k : px + 11 * k;
    const ln = svgEl(lines, "path", { d: `M${x1} ${py} H${x2}`, stroke: "#3a4a6c", "stroke-width": 2 });
    tags.push({ el: tag, ln, label, gpio, cat, side, i, pins, x: tx, y: py - th / 2, w: tw, h: th });
  });
  return { wrap, tags };
}

const sChart = SC();
sceneIn(sChart, S1("s05") + 1.3);
const spots = []; // [t, filter | null]
let allTags = [];
{
  const ch30 = pinChart(sChart, 30, 290, 196, 400);
  const ch38 = pinChart(sChart, 38, 1230, 196, 400);
  allTags = ch30.tags.concat(ch38.tags);
  for (const [x, txt] of [[490, "30-pin board"], [1430, "38-pin board"]]) {
    const l = box(sChart, x - 200, 146, 400, 40, "kicker", txt);
    l.style.textAlign = "center";
    hidden(l); show(l, T("s06"));
  }
  const hd = box(sChart, 0, 54, 1920, 80, "h2", "");
  hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s06"), "30 or 38 pins"], [T("s07"), "Three groups of pins"], [T("s08"), "Power pins"], [T("s10"), "Ground"],
    [T("s13"), "GPIO pins"], [T("s15"), "Flash pins: never use"], [T("s16"), "Input-only pins"], [T("s17"), "Strapping pins"],
    [T("s18"), "Serial pins (TX / RX)"], [W("s19", "safe"), "Safe pins for our projects"]]);
  // centre info panel between the two charts
  const info = box(sChart, 840, 380, 240, 320, "info", "");
  const I = (big, sub, color = "var(--text)") => `<div class="big" style="color:${color}">${big}</div><div class="sub">${sub}</div>`;
  panelAt(info, [[0, ""], [W("s06", "same"), I("Same names", "on both boards")],
    [W("s07", "power"), I("Power", "", "#ff8a95")], [W("s07", "ground"), I("Power<br><span style='color:#cfd8ea'>Ground</span>", "")],
    [W("s07", "GPIO"), I("<span style='color:#ff8a95'>Power</span><br><span style='color:#cfd8ea'>Ground</span><br><span style='color:var(--teal)'>GPIO</span>", "general purpose input / output")],
    [W("s08", "three"), I("3.3 V", "the ESP32's working voltage", "#ff8a95")], [W("s09", "VIN"), I("5 V", "straight from USB", "#ff8a95")],
    [W("s10", "GND"), I("0 V", "where the current returns", "#cfd8ea")], [S1("s10") + 0.5, ""],
    [W("s13", "two"), I("D2<br>= GPIO 2", "30-pin label: in code, we use the number", "var(--teal)")],
    [W("s13", "thirtyeight"), I("“2”<br>= GPIO 2", "38-pin boards print just the number", "var(--teal)")], [T("s14"), I("Input<br>or output", "but a few are special", "var(--teal)")],
    [W("s15", "flash"), I("✕ 6 – 11", "wired to the flash memory", "#ff8a95")], [W("s16", "input"), I("IN only", "34, 35, 36, 39<br>can't drive an LED", "#cdb6ff")],
    [W("s17", "strapping"), I("⚠ boot", "0, 2, 5, 12, 15<br>read at startup", "var(--amber)")], [W("s18", "serial"), I("USB serial", "TX = 1, RX = 3<br>keep free", "#9cc2ff")],
    [W("s19", "safe"), I("✓ safe", "4, 13, 14, 16 – 19,<br>21 – 23, 25 – 27,<br>32, 33", "var(--green)")]]);

  // tag colours over time
  const tPow = W("s07", "power"), tGnd = W("s07", "ground"), tGpio = W("s07", "GPIO");
  const special = { flash: [W("s15", "flash"), "flash", "✕"], in: [W("s16", "input"), "in", "IN"], strap: [W("s17", "strapping"), "strap", "⚠"],
    serial: [W("s18", "serial"), "serial", "USB"], ok: [W("s19", "safe"), "ok", "✓"] };
  allTags.forEach((g, idx) => {
    const list = [[0, ["neutral", ""]]];
    if (g.cat === "3v3" || g.cat === "5v") list.push([tPow, ["power", ""]]);
    else if (g.cat === "gnd") list.push([tGnd, ["gnd", ""]]);
    else if (g.cat === "en") list.push([tGnd, ["en", ""]]);
    else {
      list.push([tGpio, ["gpio", ""]]);
      const [ts, cls, mark] = special[g.cat];
      list.push([ts, [cls, mark]]);
    }
    g.list = list;
    g.t0 = T("s06") + 0.2 + (g.pins === 38 ? 0.4 : 0) + (g.side === "R" ? 0.2 : 0) + g.i * 0.035;
  });
  // spotlight: which tags are bright
  const isGpio = (g) => g.gpio != null;
  spots.push([T("s08"), (g) => g.cat === "3v3"], [T("s09"), (g) => g.cat === "5v"], [T("s10"), (g) => g.cat === "gnd"], [S1("s10") + 0.4, null],
    [T("s13"), isGpio], [W("s13", "two"), (g) => g.gpio === 2], [T("s14"), isGpio], [T("s15"), (g) => g.cat === "flash"], [T("s16"), (g) => g.cat === "in"],
    [T("s17"), (g) => g.cat === "strap"], [T("s18"), (g) => g.cat === "serial"], [W("s19", "safe"), (g) => g.cat === "ok"]);
  const spotOf = (g, t) => {
    let cur = null, prev = null, ts = -1;
    for (const [s, f] of spots) if (t >= s) { prev = cur; cur = f; ts = s; }
    if (ts < 0) return 1;
    const a = prev ? (prev(g) ? 1 : 0.16) : 1, b = cur ? (cur(g) ? 1 : 0.16) : 1;
    return a + (b - a) * clamp01((t - ts) / 0.35);
  };
  dyn((t) => {
    for (const g of allTags) {
      const [cls, mark] = stateAt(g.list, t);
      const key = cls + mark;
      if (g.el.__k !== key) {
        g.el.className = "abs ptag c-" + cls;
        g.el.lastChild.textContent = mark;
        g.el.__k = key;
      }
      const ap = clamp01((t - g.t0) / 0.3);
      // a small pop when the class changes
      let last = 0; for (const [ts] of g.list) if (t >= ts) last = ts;
      const pk = last > 0 ? clamp01((t - last) / 0.25) : 1;
      const o = ap * spotOf(g, t);
      g.el.style.opacity = o;
      g.ln.style.opacity = o;
      g.el.style.transform = `scale(${0.92 + 0.08 * pk})`;
    }
  });
  // rings on the power pins
  const ringTags = (filter, t0, t1) => allTags.filter(filter).forEach((g) => ring(sChart, g.x - 6, g.y - 6, g.w + 12, g.h + 12, t0, t1));
  ringTags((g) => g.cat === "3v3", W("s08", "three"), S1("s08") + 0.2);
  ringTags((g) => g.cat === "5v", W("s09", "VIN"), S1("s09") + 0.2);
  ringTags((g) => g.cat === "gnd", W("s10", "GND"), S1("s10") + 0.2);
  ringTags((g) => g.gpio === 2, W("s13", "two"), S1("s13") + 0.2);
  sceneOut(sChart, S1("s19") + 1.0);
}

const sSafe = SC();
sceneIn(sSafe, T("s11") - 0.4, 0.5);
{
  const h = head(sSafe, "Two safety rules", 130); show(h, T("s11"));
  const c1 = box(sSafe, 170, 280, 760, 560, "card", `<div style="padding:40px">
    <div class="kicker" style="color:var(--red)">Rule 1</div><div style="font:700 40px var(--display);margin-top:10px">Never wire power straight to GND</div>
    <svg width="680" height="300" viewBox="0 0 680 300" style="margin-top:20px">
      <rect x="40" y="110" width="150" height="64" rx="12" fill="rgba(255,93,108,.18)" stroke="#ff5d6c" stroke-width="3"/><text x="115" y="152" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="30" fill="#ffc2c8">3V3</text>
      <rect x="490" y="110" width="150" height="64" rx="12" fill="#222c40" stroke="#8a9ab8" stroke-width="3"/><text x="565" y="152" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="30" fill="#e3e9f5">GND</text>
      <path d="M190 142 C 290 40, 390 240, 490 142" fill="none" stroke="#ffd34d" stroke-width="9" stroke-linecap="round"/>
      <path d="M340 90 l14 30 l26 -16 l-8 30 l32 6 l-30 14 l18 26 l-32 -10 l-6 32 l-16 -28 l-24 22 l4 -32 l-32 -2 l26 -18 l-20 -24 l32 4 z" fill="#ff5d6c" opacity=".9"/>
    </svg><div style="font:600 26px var(--ui);color:var(--muted)">= short circuit: can damage the board or USB port</div></div>`);
  const c2 = box(sSafe, 990, 280, 760, 560, "card", `<div style="padding:40px">
    <div class="kicker" style="color:var(--red)">Rule 2</div><div style="font:700 40px var(--display);margin-top:10px">Never put 5 V into a GPIO</div>
    <svg width="680" height="300" viewBox="0 0 680 300" style="margin-top:20px">
      <rect x="40" y="110" width="150" height="64" rx="12" fill="rgba(255,93,108,.18)" stroke="#ff5d6c" stroke-width="3"/><text x="115" y="152" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="30" fill="#ffc2c8">5 V</text>
      <rect x="470" y="110" width="170" height="64" rx="12" fill="rgba(25,195,180,.16)" stroke="#19c3b4" stroke-width="3"/><text x="555" y="152" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="30" fill="#b9f3ec">GPIO</text>
      <path d="M200 142 H450" stroke="#ff5d6c" stroke-width="8" stroke-dasharray="18 12"/><path d="M432 120 l26 22 l-26 22" fill="none" stroke="#ff5d6c" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
      <g stroke="#ff5d6c" stroke-width="14" stroke-linecap="round"><path d="M285 100 l80 84"/><path d="M365 100 l-80 84"/></g>
    </svg><div style="font:600 26px var(--ui);color:var(--muted)">GPIO pins are for 3.3 V only</div></div>`);
  hidden(c1); hidden(c2);
  pop(c1, W("s11", "Never")); pop(c2, W("s12", "never"));
  sceneOut(sSafe, S1("s12") + 0.5, 0.5);
}

/* ======================================================================
 * BREADBOARD BUILDER
 * ==================================================================== */
const P = 42;
const ROWS = { tp: 0, tm: 1, a: 2.5, b: 3.5, c: 4.5, d: 5.5, e: 6.5, f: 9.5, g: 10.5, h: 11.5, i: 12.5, j: 13.5, bp: 15, bm: 16 };
const MID = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"];
function makeBB(parent, x, y, cols = 30) {
  const mx = 58, my = 50, w = mx * 2 + (cols - 1) * P, h = my * 2 + 16 * P;
  const root = box(parent, x, y, w, h, "");
  const svg = svgEl(root, "svg", { width: w, height: h, viewBox: `0 0 ${w} ${h}` });
  css(svg, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  const L = (c, r) => [mx + (c - 1) * P, my + ROWS[r] * P];
  const S = (c, r) => { const [lx, ly] = L(c, r); return [x + lx, y + ly]; };
  const defs = svgEl(svg, "defs");
  defs.innerHTML = `<linearGradient id="bbshield" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9edf2"/><stop offset=".5" stop-color="#b9c0c9"/><stop offset="1" stop-color="#d9dee5"/></linearGradient>
    <radialGradient id="ledglow"><stop offset="0" stop-color="#ff6b6b" stop-opacity=".95"/><stop offset=".35" stop-color="#ff4d4d" stop-opacity=".55"/><stop offset="1" stop-color="#ff3030" stop-opacity="0"/></radialGradient>`;
  svgEl(svg, "rect", { x: 0, y: 0, width: w, height: h, rx: 20, fill: "#ecebe6", stroke: "#c9c6bd", "stroke-width": 2 });
  const gy = my + (ROWS.e + ROWS.f) / 2 * P;
  const groove = svgEl(svg, "rect", { x: 12, y: gy - 15, width: w - 24, height: 30, rx: 7, fill: "#d6d3cb" });
  // rail markings: red line on the + side, blue on the - side
  const railY = { tp: my + ROWS.tp * P, tm: my + ROWS.tm * P, bp: my + ROWS.bp * P, bm: my + ROWS.bm * P };
  const marks = svgEl(svg, "g", {});
  for (const [r, dy, col] of [["tp", -0.55, "#e5484d"], ["tm", 0.55, "#3b6fe0"], ["bp", -0.55, "#e5484d"], ["bm", 0.55, "#3b6fe0"]]) {
    svgEl(marks, "path", { d: `M${mx - 10} ${railY[r] + dy * P} H${w - mx + 10}`, stroke: col, "stroke-width": 3 });
    for (const xx of [mx - 34, w - mx + 34])
      svgEl(marks, "text", { x: xx, y: railY[r] + 8, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 26, fill: col }).textContent = r.endsWith("p") ? "+" : "−";
  }
  // internal strips (hidden until revealed)
  const strips = svgEl(svg, "g", { opacity: 0 });
  const colStrip = {};
  for (let c = 1; c <= cols; c++) {
    const [sx, ya] = L(c, "a"), [, ye] = L(c, "e"), [, yf] = L(c, "f"), [, yj] = L(c, "j");
    colStrip[c] = [svgEl(strips, "rect", { x: sx - 11, y: ya - 13, width: 22, height: ye - ya + 26, rx: 7, fill: "#19c3b4", opacity: 0.55 }),
      svgEl(strips, "rect", { x: sx - 11, y: yf - 13, width: 22, height: yj - yf + 26, rx: 7, fill: "#19c3b4", opacity: 0.55 })];
  }
  const railStrip = {};
  for (const r of ["tp", "tm", "bp", "bm"])
    railStrip[r] = svgEl(svg, "rect", { x: mx - 13, y: railY[r] - 13, width: (cols - 1) * P + 26, height: 26, rx: 9, fill: r.endsWith("p") ? "#e5484d" : "#3b6fe0", opacity: 0 });
  // holes
  const holes = svgEl(svg, "g", {});
  for (let c = 1; c <= cols; c++) {
    for (const r of MID) { const [hx, hy] = L(c, r); svgEl(holes, "rect", { x: hx - 7, y: hy - 7, width: 14, height: 14, rx: 2.5, fill: "#4a4842" }); }
    if (c % 6 !== 0) for (const r of ["tp", "tm", "bp", "bm"]) { const [hx, hy] = L(c, r); svgEl(holes, "rect", { x: hx - 7, y: hy - 7, width: 14, height: 14, rx: 2.5, fill: "#4a4842" }); }
  }
  // labels
  const lab = svgEl(svg, "g", { "font-family": "Segoe UI", "font-size": 15, "font-weight": 600, fill: "#8d8a80", "text-anchor": "middle" });
  for (const r of MID) for (const xx of [mx - 30, w - mx + 30]) svgEl(lab, "text", { x: xx, y: my + ROWS[r] * P + 5 }).textContent = r;
  for (let c = 1; c <= cols; c++) if (c === 1 || c % 5 === 0) {
    svgEl(lab, "text", { x: mx + (c - 1) * P, y: my + (ROWS.a - 0.75) * P + 5 }).textContent = c;
    svgEl(lab, "text", { x: mx + (c - 1) * P, y: my + (ROWS.j + 0.75) * P + 5 }).textContent = c;
  }
  const parts = svgEl(svg, "g", {});
  const over = svgEl(svg, "g", {});
  return { root, svg, L, S, w, h, x, y, groove, strips, colStrip, railStrip, parts, over, mx, my, cols };
}

/** ESP32 board seen from the top, lying across the gap; pins: 30 (rows b/i) or 38 (rows a/i) */
const BBPINS = {
  30: { top: "b", T: ["VIN", "GND", "D13", "D12", "D14", "D27", "D26", "D25", "D33", "D32", "D35", "D34", "VN", "VP", "EN"],
    B: ["3V3", "GND", "D15", "D2", "D4", "D16", "D17", "D5", "D18", "D19", "D21", "RX0", "TX0", "D22", "D23"] },
  38: { top: "a", T: ["5V", "CMD", "D3", "D2", "13", "GND", "12", "14", "27", "26", "25", "33", "32", "35", "34", "VN", "VP", "EN", "3V3"],
    B: ["CLK", "D0", "D1", "15", "2", "0", "4", "16", "17", "5", "18", "19", "GND", "21", "RX", "TX", "22", "23", "GND"] },
};
function bbBoard(bb, pins, c0) {
  const spec = BBPINS[pins], n = pins / 2;
  const g = svgEl(bb.parts, "g", {});
  const [x0, yT] = bb.L(c0, spec.top), [x1, yB] = bb.L(c0 + n - 1, "i");
  const left = x0 - 0.6 * P, right = x1 + 0.6 * P + 34, top = yT - 0.55 * P, bot = yB + 0.55 * P, mid = (yT + yB) / 2;
  svgEl(g, "rect", { x: left - 62, y: mid - 34, width: 84, height: 68, rx: 6, fill: "url(#bbshield)", stroke: "#7d8690", "stroke-width": 2 }); // USB
  svgEl(g, "rect", { x: left, y: top, width: right - left, height: bot - top, rx: 12, fill: "#1b1f26", stroke: "#2b313b", "stroke-width": 2, opacity: 0.97 });
  const mL = x1 - 5.6 * P, mT = yT + 1.0 * P, mB = yB - 1.0 * P;
  svgEl(g, "rect", { x: mL, y: mT, width: right - 6 - mL, height: mB - mT, rx: 5, fill: "#24384f" });
  svgEl(g, "rect", { x: mL + 8, y: mT + 8, width: right - 6 - mL - 70, height: mB - mT - 16, rx: 5, fill: "url(#bbshield)" });
  svgEl(g, "path", { d: `M${right - 52} ${mT + 14} V${mB - 14}`, stroke: "#c9a54a", "stroke-width": 6, "stroke-dasharray": "14 8" });
  const tx = svgEl(g, "text", { x: mL + (right - 76 - mL) / 2, y: mid + 8, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 22, fill: "#5d6670" });
  tx.textContent = "ESP32-WROOM-32";
  const pinXY = {};
  for (let k = 0; k < n; k++) {
    for (const [row, names, dy] of [[spec.top, spec.T, 25], ["i", spec.B, -17]]) {
      const [px, py] = bb.L(c0 + k, row);
      svgEl(g, "rect", { x: px - 10, y: py - 10, width: 20, height: 20, rx: 3, fill: "#d4af37" });
      svgEl(g, "circle", { cx: px, cy: py, r: 4.5, fill: "#15181d" });
      const t = svgEl(g, "text", { x: px, y: py + dy, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 600, "font-size": 12.5, fill: "#e8ecf1" });
      t.textContent = names[k];
      pinXY[(row === "i" ? "B" : "T") + k] = [px, py];
    }
  }
  return { g, c0, n, top: spec.top };
}
/** jumper wire between two local points, drawn on at time t */
function bbWire(bb, a, b, color, t, bend = 0.18) {
  const [ax, ay] = a, [bx2, by2] = b, mx2 = (ax + bx2) / 2, my2 = (ay + by2) / 2, dx = bx2 - ax, dy = by2 - ay;
  const cx = mx2 - dy * bend, cy = my2 + dx * bend;
  const g = svgEl(bb.parts, "g", {});
  const p = svgEl(g, "path", { d: `M${ax} ${ay} Q${cx} ${cy} ${bx2} ${by2}`, fill: "none", stroke: color, "stroke-width": 10, "stroke-linecap": "round" });
  const ends = [a, b].map(([ex, ey]) => svgEl(g, "rect", { x: ex - 7, y: ey - 7, width: 14, height: 14, rx: 2, fill: "#222", opacity: 0 }));
  drawOn(p, t, 0.6);
  ends.forEach((e, i) => TO(e, t + (i ? 0.55 : 0), 0.1, { opacity: 1 }));
  return g;
}
/** resistor between two local points (top-view drawing) */
function bbResistor(bb, a, b) {
  const g = svgEl(bb.parts, "g", {});
  const [ax, ay] = a, [bx2, by2] = b, ang = Math.atan2(by2 - ay, bx2 - ax) * 180 / Math.PI, len = Math.hypot(bx2 - ax, by2 - ay);
  const inner = svgEl(g, "g", { transform: `translate(${ax} ${ay}) rotate(${ang})` });
  svgEl(inner, "path", { d: `M0 0 H${len}`, stroke: "#b8bec6", "stroke-width": 5, "stroke-linecap": "round" });
  const bl = 70, b0 = (len - bl) / 2;
  svgEl(inner, "rect", { x: b0, y: -14, width: bl, height: 28, rx: 12, fill: "#dcc79f", stroke: "#b49e72", "stroke-width": 1.5 });
  [[12, "#d0262f"], [24, "#d0262f"], [36, "#7a4a21"], [54, "#c9a54a"]].forEach(([o, c]) => svgEl(inner, "rect", { x: b0 + o, y: -14, width: 7, height: 28, fill: c }));
  for (const [ex, ey] of [a, b]) svgEl(g, "circle", { cx: ex, cy: ey, r: 5, fill: "#9aa1aa" });
  return g;
}
/** LED (top view): legs at a (anode, long) and b (cathode) with the dome beside them */
function bbLED(bb, a, b, side = -1) {
  const g = svgEl(bb.parts, "g", {});
  const [ax, ay] = a, [bx2, by2] = b, mx2 = (ax + bx2) / 2, my2 = (ay + by2) / 2;
  const dx = bx2 - ax, dy = by2 - ay, L2 = Math.hypot(dx, dy) || 1;
  const nx = -dy / L2 * side, ny = dx / L2 * side;
  const cx = mx2 + nx * 34, cy = my2 + ny * 34;
  const glow = svgEl(g, "circle", { cx, cy, r: 110, fill: "url(#ledglow)", opacity: 0 });
  for (const [ex, ey] of [a, b]) svgEl(g, "path", { d: `M${ex} ${ey} L${cx + (ex - mx2) * 0.45} ${cy + (ey - my2) * 0.45}`, stroke: "#b8bec6", "stroke-width": 5, "stroke-linecap": "round" });
  svgEl(g, "circle", { cx, cy, r: 24, fill: "#b51d27" });
  const dome = svgEl(g, "circle", { cx, cy, r: 20, fill: "#d4202c" });
  const lit = svgEl(g, "circle", { cx, cy, r: 20, fill: "#ffd0d0", opacity: 0 });
  svgEl(g, "path", { d: `M${cx + (bx2 - mx2) / L2 * 24 - ny * 14} ${cy + (by2 - my2) / L2 * 24 + nx * 14} l${ny * 28} ${-nx * 28}`, stroke: "#7c121a", "stroke-width": 4 });
  for (const [ex, ey] of [a, b]) svgEl(g, "circle", { cx: ex, cy: ey, r: 5, fill: "#9aa1aa" });
  return { g, glow, lit, dome, cx, cy };
}
/** small marker on the stage: ✓ or ✕ badge */
function mark(parent, x, y, ok, txt) {
  const m = box(parent, x, y, 0, 0, "badge", `${ok ? "✓" : "✕"}&nbsp; ${txt}`);
  css(m, { width: "auto", height: "auto", background: ok ? "var(--green)" : "var(--red)", color: ok ? "#05210f" : "#fff", zIndex: 20 });
  return hidden(m);
}

/* ======================================================================
 * BREADBOARD (s20-s25)
 * ==================================================================== */
const BBX = 290, BBY = 236;
const sBB = SC();
sceneIn(sBB, S1("s19") + 1.0);
{
  const hd = box(sBB, 0, 70, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s20"), "The breadboard"], [W("s21", "metal"), "Metal strips inside"], [T("s22"), "The middle gap"], [T("s23"), "Power rails"],
    [T("s24"), "Split rails"], [T("s25"), "Common mistake"]]);
  const bb = makeBB(sBB, BBX, BBY);
  hidden(bb.root); pop(bb.root, T("s20") + 0.2, 0.5);
  // s20: a wire pushed in
  const w0 = bbWire(bb, bb.L(6, "c"), bb.L(9, "c"), "#ffd34d", W("s20", "push"), 0.35);
  TO(w0, S1("s20") + 0.1, 0.3, { opacity: 0 });
  // s21: reveal strips, then one column a-e and f-j
  TO(bb.strips, W("s21", "metal"), 0.8, { opacity: 0.6 });
  const C = 12;
  const [ca, cb] = bb.colStrip[C];
  SET([ca, cb], W("s21", "column") - 0.01, { attr: { fill: "#19c3b4" } });
  TO(ca, W("s21", "column"), 0.4, { opacity: 1 });
  TO(cb, W("s21", "F"), 0.4, { opacity: 1 });
  const [sx, sya] = bb.S(C, "a"), [, sye] = bb.S(C, "e"), [, syf] = bb.S(C, "f"), [, syj] = bb.S(C, "j");
  const lab1 = callout(sBB, "a – e: connected", sx + 26, (sya + sye) / 2 - 18, W("s21", "A"), S1("s22") + 0.2);
  const lab2 = callout(sBB, "f – j: connected", sx + 26, (syf + syj) / 2 - 18, W("s21", "F"), S1("s22") + 0.2);
  lab1.style.zIndex = lab2.style.zIndex = 10;
  // s22: gap
  const [gx0, gy] = bb.S(1, "e"), gapY = gy + 1.5 * P;
  const gl = box(sBB, BBX + 10, gapY - 17, bb.w - 20, 34, "ring"); pop(gl, W("s22", "gap")); hide(gl, S1("s22") + 0.3);
  const nx = box(sBB, sx - 23, gapY - 23, 46, 46, "", `<div style="width:46px;height:46px;border-radius:50%;background:var(--red);color:#fff;font:800 30px var(--ui);display:flex;align-items:center;justify-content:center">✕</div>`);
  hidden(nx); pop(nx, W("s22", "not")); hide(nx, S1("s22") + 0.3);
  // s23: rails
  TO(bb.strips, T("s23"), 0.4, { opacity: 0.18 });
  for (const r of ["tp", "bp"]) { SET(bb.railStrip[r], W("s23", "red") - 0.01, { attr: { opacity: 0 } }); TO(bb.railStrip[r], W("s23", "red"), 0.5, { opacity: 0.55 }); }
  for (const r of ["tm", "bm"]) TO(bb.railStrip[r], W("s23", "blue"), 0.5, { opacity: 0.55 });
  for (const r of ["tp", "tm", "bp", "bm"]) {
    gsap.set(bb.railStrip[r], { opacity: 0 });
    const st = bb.railStrip[r];
    st.setAttribute("opacity", 1);
    gsap.set(st, { transformOrigin: "0% 50%", scaleX: 1 });
    SET(st, W("s23", "whole") - 0.01, { scaleX: 0.02 });
    TO(st, W("s23", "whole"), 1.0, { scaleX: 1, ease: "power1.inOut" });
  }
  const shareP = callout(sBB, "+ rail: power for the whole board", BBX + 420, BBY - 50, W("s23", "share"), S1("s23") + 0.3);
  // s24: split rail with a bridge
  const [bx15] = bb.L(15, "tp"), [bx18] = bb.L(18, "tp"), [, tpy] = bb.L(1, "tp");
  const cut = svgEl(bb.over, "rect", { x: (bx15 + bx18) / 2 - 30, y: tpy - 0.55 * P - 6, width: 60, height: 12, fill: "#ecebe6", opacity: 0 });
  TO(cut, W("s24", "split"), 0.3, { opacity: 1 });
  TO(bb.railStrip.tp, W("s24", "split"), 0.3, { opacity: 0.25 });
  const brk = callout(sBB, "break in the red line", BBX + (bx15 + bx18) / 2 - 110, BBY - 52, W("s24", "break"), S1("s24") + 0.3);
  const bridge = bbWire(bb, bb.L(15, "tp"), bb.L(18, "tp"), "#ff5d6c", W("s24", "join"), 0.4);
  TO([cut, bridge], S1("s24") + 0.2, 0.3, { opacity: 0 });
  TO(bb.railStrip.tp, S1("s24") + 0.2, 0.3, { opacity: 0 });
  for (const r of ["tm", "bp", "bm"]) TO(bb.railStrip[r], S1("s24") + 0.2, 0.3, { opacity: 0 });
  // s25: LED with both legs in the same column
  TO(bb.strips, T("s25"), 0.4, { opacity: 0.6 });
  const bad = bbLED(bb, bb.L(22, "b"), bb.L(22, "d"), 1);
  hidden(bad.g); pop(bad.g, W("s25", "both"));
  const bx22 = bb.S(22, "c");
  const m1 = mark(sBB, bx22[0] + 70, bx22[1] - 30, false, "same column: legs connected"); pop(m1, W("s25", "same"));
  const good = bbLED(bb, bb.L(26, "g"), bb.L(27, "g"), -1);
  hidden(good.g); pop(good.g, W("s25", "nothing") + 0.5);
  const gx = bb.S(26, "h");
  const m2 = mark(sBB, gx[0] - 150, gx[1] + 40, true, "two columns"); pop(m2, W("s25", "nothing") + 0.7);
  sceneOut(sBB, S1("s25") + 0.6);
}

/* ======================================================================
 * MOUNT THE BOARD (s26-s29)
 * ==================================================================== */
const sMount = SC();
sceneIn(sMount, S1("s25") + 0.6);
{
  const hd = box(sMount, 0, 70, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s26"), "Board across the gap"], [T("s28"), "Free holes next to the pins"], [T("s29"), "Need more room?"]]);
  const bb = makeBB(sMount, BBX, BBY);
  const b30 = bbBoard(bb, 30, 2);
  gsap.set(b30.g, { opacity: 0, y: -120 });
  TO(b30.g, W("s26", "board"), 0.9, { opacity: 1, y: 0, ease: "power3.out" });
  const gl = box(sMount, BBX + 10, BBY + bb.my + 8 * P - 17, bb.w - 20, 34, "ring"); pop(gl, W("s26", "gap")); hide(gl, S1("s26"));
  // columns under the pins
  TO(bb.strips, W("s26", "column"), 0.5, { opacity: 0.7 });
  for (let c = 17; c <= 30; c++) bb.colStrip[c].forEach((e) => e.setAttribute("opacity", 0.12));
  TO(bb.strips, S1("s26") + 0.4, 0.4, { opacity: 0 });
  clipFrame(sMount, "C2", 320, 150, 1280, 720, T("s27") - 0.1, S1("s27") + 1.3, "Press the board into the breadboard across the middle gap, evenly on both sides.");
  // s28: free holes
  const freeRow = (row, c0, n, ok, t0, t1) => {
    for (let c = c0; c < c0 + n; c++) {
      const [hx, hy] = bb.S(c, row);
      const r = box(sMount, hx - 12, hy - 12, 24, 24, "");
      css(r, { borderRadius: "6px", border: `3px solid ${ok ? "#4ade80" : "#ff5d6c"}`, boxShadow: `0 0 12px ${ok ? "rgba(74,222,128,.7)" : "rgba(255,93,108,.7)"}` });
      hidden(r); show(r, t0 + (c - c0) * 0.03, 0.2); hide(r, t1, 0.3);
    }
  };
  const t30 = W("s28", "thirty"), t38 = W("s28", "thirtyeight");
  freeRow("a", 2, 15, true, t30 + 0.2, t38 - 0.2);
  freeRow("j", 2, 15, true, t30 + 0.5, t38 - 0.2);
  const m30 = mark(sMount, BBX + bb.L(17, "a")[0] + 30, BBY + bb.L(1, "a")[1] - 26, true, "1 free hole");
  const m30b = mark(sMount, BBX + bb.L(17, "j")[0] + 30, BBY + bb.L(1, "j")[1] - 26, true, "1 free hole");
  pop(m30, t30 + 0.6); pop(m30b, t30 + 0.8); hide([m30, m30b], t38 - 0.2, 0.3);
  // swap to the 38-pin board
  const b38 = bbBoard(bb, 38, 2);
  gsap.set(b38.g, { opacity: 0 });
  TO(b30.g, t38 - 0.3, 0.4, { opacity: 0 });
  TO(b38.g, t38, 0.5, { opacity: 1 });
  freeRow("j", 2, 19, true, t38 + 0.6, S1("s28") + 0.6);
  const m38 = mark(sMount, BBX + bb.L(21, "j")[0] + 30, BBY + bb.L(1, "j")[1] - 26, true, "1 free hole");
  const m38t = mark(sMount, BBX + bb.L(21, "a")[0] + 30, BBY + bb.L(1, "a")[1] - 26, false, "no free holes");
  pop(m38, t38 + 0.8); pop(m38t, W("s28", "no")); hide([m38, m38t], S1("s28") + 0.6, 0.3);
  // s29: two breadboards
  const dim = box(sMount, 0, 0, 1920, 1080, ""); css(dim, { background: "rgba(8,13,24,.82)", zIndex: 30 }); hidden(dim);
  show(dim, W("s29", "two") - 0.3, 0.35);
  const two = box(sMount, 560, 300, 800, 520, "card", `<div style="padding:34px 40px"><div class="kicker">Tip</div><div style="font:700 38px var(--display);margin:8px 0 24px">Two breadboards side by side</div>
    <svg width="720" height="320" viewBox="0 0 720 320">
      <rect x="20" y="20" width="300" height="280" rx="14" fill="#ecebe6"/><rect x="400" y="20" width="300" height="280" rx="14" fill="#ecebe6"/>
      <rect x="40" y="150" width="260" height="18" rx="4" fill="#d6d3cb"/><rect x="420" y="150" width="260" height="18" rx="4" fill="#d6d3cb"/>
      <rect x="190" y="60" width="340" height="200" rx="12" fill="#1b1f26"/><rect x="420" y="96" width="96" height="128" rx="6" fill="#b9c0c9"/>
      ${[0, 1, 2, 3, 4, 5, 6, 7].map((i) => `<rect x="${206 + i * 40}" y="66" width="16" height="16" rx="2" fill="#d4af37"/><rect x="${206 + i * 40}" y="238" width="16" height="16" rx="2" fill="#d4af37"/>`).join("")}
    </svg></div>`);
  css(two, { zIndex: 31 }); hidden(two); pop(two, W("s29", "two"));
  sceneOut(sMount, S1("s29") + 0.5);
}

/* ======================================================================
 * THE PARTS (s30-s33)
 * ==================================================================== */
const sCirc = SC();
sceneIn(sCirc, S1("s29") + 0.5);
{
  const h = head(sCirc, "Our first circuit", 70); show(h, T("s30"));
  const nc = box(sCirc, 0, 160, 1920, 60, "", `<div style="display:flex;justify-content:center"><span class="pill" style="background:rgba(255,181,71,.14);color:var(--amber)">No code needed</span></div>`);
  hidden(nc); pop(nc, W("s30", "No")); hide(nc, S1("s30") + 0.3);
  // LED
  const g1 = box(sCirc, 0, 0, 1920, 1080, "");
  const led = box(g1, 330, 250, 300, 600, "", ART.led(280));
  hidden(led); pop(led, W("s30", "LED"));
  const lA = box(g1, 40, 760, 300, 120, "", `<div style="text-align:right"><div style="font:700 34px var(--display);color:#ff8a95">+ anode</div><div class="muted" style="font-size:24px">long leg</div></div>`);
  const lK = box(g1, 545, 640, 400, 120, "", `<div style="font:700 34px var(--display);color:#9cc2ff">− cathode</div><div class="muted" style="font-size:24px">short leg</div></div>`);
  gsap.set([lA, lK], { opacity: 0 });
  pop(lA, W("s31", "long")); pop(lK, W("s31", "short"));
  // current arrow: long leg -> short leg
  const sv = svgLayer(g1);
  const arr = svgEl(sv, "path", { d: "M433 770 V500 C 433 410, 507 410, 507 500 V680", fill: "none", stroke: "#ffb547", "stroke-width": 8, "stroke-linecap": "round", "stroke-dasharray": "2 22" });
  arr.style.opacity = 0;
  TO(arr, W("s31", "Current"), 0.3, { opacity: 1 });
  dyn((t) => { arr.style.strokeDashoffset = -((t * 60) % 24); });
  TO(arr, S1("s31") + 0.2, 0.3, { opacity: 0 });
  const cur = box(g1, 640, 420, 500, 60, "", `<span style="font:700 30px var(--display);color:var(--amber)">current: long → short</span>`);
  hidden(cur); pop(cur, W("s31", "Current")); hide(cur, S1("s31") + 0.2);
  // s32: burn, resistor
  const burn = box(g1, 640, 330, 560, 120, "", `<div style="font:700 34px var(--display);color:var(--red)">✕ LED alone: too much current</div>`);
  hidden(burn); pop(burn, W("s32", "burn")); hide(burn, W("s32", "resistor") - 0.1);
  const res = box(g1, 1180, 360, 560, 200, "", `<div style="display:flex;justify-content:center">${ART.resistor(520)}</div>`);
  hidden(res); pop(res, W("s32", "resistor"));
  const rv = box(g1, 1180, 540, 560, 70, "", `<div style="text-align:center;font:700 44px var(--display)">220 Ω</div>`);
  hidden(rv); pop(rv, W("s32", "220"));
  const bandX = [1180 + 20 + (82 + 5.5) * 520 / 240, 1180 + 20 + (102 + 5.5) * 520 / 240, 1180 + 20 + (122 + 5.5) * 520 / 240];
  const bands = [["red", W("s32", "red", 1)], ["red", W("s32", "red", 2)], ["brown", W("s32", "brown")]];
  bands.forEach(([nm, t], i) => { const r = box(g1, bandX[i] - 18, 372, 36, 120, "ring"); pop(r, t); });
  const R = '<span style="color:#ff8a95">red</span>', B = '<span style="color:#d0a070">brown</span>';
  const bl = box(g1, 1180, 625, 560, 50, "", "");
  css(bl, { textAlign: "center", font: "700 32px var(--ui)" });
  panelAt(bl, [[0, ""], [bands[0][1], R], [bands[1][1], `${R} · ${R}`], [bands[2][1], `${R} · ${R} · ${B}`]], 0);
  hide(g1, T("s33") - 0.2, 0.4);
  // s33: plan / schematic
  const g2 = box(sCirc, 0, 0, 1920, 1080, "");
  const nodes = [["3V3", "power", "#ff8a95", "Three"], ["220 Ω", "resistor", "#dcc79f", "resistor"], ["LED", "long → short", "#ff5d6c", "long"], ["GND", "ground", "#cfd8ea", "ground"]];
  nodes.forEach(([a, b, col, w], i) => {
    const x = 130 + i * 440;
    const c = box(g2, x, 400, 340, 220, "card", `<div style="height:220px;display:flex;flex-direction:column;align-items:center;justify-content:center">
      <div style="font:700 52px var(--display);color:${col}">${a}</div><div class="muted" style="font-size:24px;margin-top:8px">${b}</div></div>`);
    hidden(c); pop(c, W("s33", w));
    if (i < 3) {
      const ar = box(g2, x + 352, 485, 76, 50, "", `<svg width="76" height="50" viewBox="0 0 76 50"><path d="M6 25h56M48 12l14 13-14 13" fill="none" stroke="#ffb547" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`);
      hidden(ar); show(ar, W("s33", nodes[i + 1][3]) - 0.2, 0.3);
    }
  });
  sceneOut(sCirc, S1("s33") + 0.5);
}

/* ======================================================================
 * BUILD IT (s34-s39)
 * ==================================================================== */
const sBuild = SC();
sceneIn(sBuild, S1("s33") + 0.5);
{
  const hd = box(sBuild, 0, 70, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [W("s34", "one"), "Step 1 · Power rails"], [T("s35"), "Step 2 · Resistor"], [T("s36"), "Step 3 · LED"], [T("s37"), "Step 4 · Back to ground"],
    [T("s38"), "Power on!"], [T("s39"), "Not working?"]]);
  const bb = makeBB(sBuild, BBX, BBY);
  hidden(bb.root); show(bb.root, T("s34") - 0.3, 0.4);
  bbBoard(bb, 30, 2);
  // USB status badge
  const usb = box(sBuild, 70, 80, 0, 0, "badge", "");
  css(usb, { width: "auto", height: "auto" });
  panelAt(usb, [[0, ""], [W("s34", "unplugged"), `<span style="color:var(--red)">● USB unplugged</span>`], [W("s38", "plug"), `<span style="color:var(--green)">● USB plugged in</span>`]], 0);
  css(usb, { background: "rgba(11,18,32,.9)", border: "1px solid var(--line)" });
  // pin callouts
  const p3 = bb.S(2, "i"), pg = bb.S(3, "i");
  callout(sBuild, "3V3", p3[0] - 30, p3[1] - 72, W("s34", "three"), S1("s34") + 0.3);
  callout(sBuild, "GND", pg[0] + 4, pg[1] - 72, W("s34", "GND"), S1("s34") + 0.3);
  // step 1: power rails
  bbWire(bb, bb.L(2, "j"), bb.L(2, "bp"), "#ff5d6c", W("s34", "rail", 1) - 0.3, 0.35);
  bbWire(bb, bb.L(3, "j"), bb.L(3, "bm"), "#2b2f36", W("s34", "minus") - 0.2, -0.35);
  TO(bb.railStrip.bp, W("s34", "rail", 1) + 0.3, 0.4, { opacity: 0.45 });
  TO(bb.railStrip.bm, W("s34", "minus") + 0.4, 0.4, { opacity: 0.45 });
  TO([bb.railStrip.bp, bb.railStrip.bm], S1("s34") + 0.4, 0.4, { opacity: 0 });
  // step 2: resistor + rail -> column 20
  const res = bbResistor(bb, bb.L(20, "bp"), bb.L(20, "h"));
  gsap.set(res, { opacity: 0, y: -40 });
  TO(res, W("s35", "resistor"), 0.6, { opacity: 1, y: 0, ease: "power3.out" });
  // step 3: LED long leg in column 20 (row f), short leg in column 21
  const led = bbLED(bb, bb.L(20, "f"), bb.L(21, "f"), -1);
  gsap.set(led.g, { opacity: 0, y: -40 });
  TO(led.g, T("s36") + 0.4, 0.6, { opacity: 1, y: 0, ease: "power3.out" });
  const [c20a, c20b] = bb.colStrip[20], [, c21b] = bb.colStrip[21];
  gsap.set(bb.strips, { opacity: 1 });
  for (let c = 1; c <= 30; c++) bb.colStrip[c].forEach((e) => { e.setAttribute("opacity", 0); });
  TO(c20b, W("s36", "same"), 0.4, { opacity: 0.6 }); TO(c20b, S1("s36") + 0.6, 0.4, { opacity: 0 });
  TO(c21b, W("s36", "next"), 0.4, { opacity: 0.6, attr: { fill: "#4f8dff" } }); TO(c21b, S1("s36") + 0.6, 0.4, { opacity: 0 });
  const pl = bb.S(20, "f"), ps = bb.S(21, "f");
  callout(sBuild, "long leg", pl[0] - 128, pl[1] + 14, W("s36", "long"), S1("s36") + 0.4);
  callout(sBuild, "short leg", ps[0] + 24, ps[1] + 14, W("s36", "short"), S1("s36") + 0.4);
  // step 4: back to ground
  bbWire(bb, bb.L(21, "j"), bb.L(21, "bm"), "#2b2f36", W("s37", "wire"), -0.35);
  // the loop
  const pts = [bb.L(2, "i"), bb.L(2, "j"), bb.L(2, "bp"), bb.L(20, "bp"), bb.L(20, "h"), bb.L(20, "f"), [led.cx, led.cy], bb.L(21, "f"),
    bb.L(21, "j"), bb.L(21, "bm"), bb.L(3, "bm"), bb.L(3, "j"), bb.L(3, "i")];
  const loop = svgEl(bb.over, "path", { d: "M" + pts.map((p) => p.join(" ")).join(" L"), fill: "none", stroke: "#ffb547", "stroke-width": 6, "stroke-linejoin": "round", opacity: 0.9 });
  drawOn(loop, W("s37", "closes"), 1.2);
  TO(loop, W("s37", "closes") + 1.6, 0.4, { opacity: 0 });
  // s38: power on
  TO(led.glow, W("s38", "lights"), 0.5, { opacity: 1 });
  TO(led.lit, W("s38", "lights"), 0.3, { opacity: 0.85 });
  const Lp = loop.getTotalLength();
  const dots = [];
  for (let i = 0; i < 26; i++) dots.push(svgEl(bb.over, "circle", { r: 6, fill: "#ffd34d", opacity: 0 }));
  const tc0 = W("s38", "Current"), tc1 = S1("s39") + 0.5;
  dyn((t) => {
    const on = t >= tc0 && t < tc1;
    const fade = on ? clamp01((t - tc0) / 0.5) * clamp01((tc1 - t) / 0.4) : 0;
    dots.forEach((d, i) => {
      if (!on) { if (d.__o !== 0) { d.setAttribute("opacity", 0); d.__o = 0; } return; }
      const s = ((t - tc0) * 140 + i * Lp / dots.length) % Lp;
      const p = loop.getPointAtLength(s);
      d.setAttribute("cx", p.x); d.setAttribute("cy", p.y); d.setAttribute("opacity", 0.95 * fade); d.__o = 1;
    });
  });
  clipFrame(sBuild, "C3", 1140, 150, 720, 405, T("s38"), S1("s38") + 1.3, "Plug in the USB cable: the LED turns on.");
  // s39: checklist
  const chk = box(sBuild, 520, 300, 880, 430, "card", "");
  css(chk, { zIndex: 40 }); hidden(chk); show(chk, T("s39") - 0.1, 0.35);
  const rows = [["Long leg on the resistor side", "long"], ["Legs in different columns", "different"], ["Rail not split", "split"]];
  chk.innerHTML = `<div style="padding:40px 50px"><div class="kicker">LED stays dark?</div>` + rows.map(([a]) => `<div class="row" style="display:flex;gap:22px;align-items:center;margin-top:30px;opacity:0">
    <div style="width:52px;height:52px;border-radius:50%;background:var(--green);color:#052;font:800 30px var(--ui);display:flex;align-items:center;justify-content:center">✓</div>
    <div style="font:600 36px var(--display)">${a}</div></div>`).join("") + `</div>`;
  chk.querySelectorAll(".row").forEach((r, i) => TO(r, W("s39", rows[i][1]), 0.4, { opacity: 1 }));
  sceneOut(sBuild, S1("s39") + 0.6);
}

/* ======================================================================
 * OUTRO (s40-s41)
 * ==================================================================== */
const sOutro = SC();
sceneIn(sOutro, S1("s39") + 0.6);
{
  const h = box(sOutro, 110, 220, 1500, 80, "h2", "Episode 2 complete!"); hidden(h); pop(h, T("s40"));
  const items = [["Power pins", "3.3 V, 5 V, GND"], ["Safe GPIO pins", "and which to avoid"], ["Breadboard", "strips, gap, rails"], ["First circuit", "3V3 → resistor → LED → GND"]];
  const cards = items.map(([a, b], i) => {
    const c = box(sOutro, 110 + i * 435, 400, 400, 300, "card", `<div style="padding:34px"><div style="width:64px;height:64px;border-radius:50%;background:rgba(25,195,180,.15);color:var(--teal);font:700 32px var(--display);display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div style="font:700 34px var(--display);margin-top:28px">${a}</div><div class="muted" style="font-size:23px;margin-top:8px">${b}</div></div>
      <div class="ok" style="position:absolute;right:26px;top:26px;width:58px;height:58px;border-radius:50%;background:var(--green);color:#052;font:700 34px var(--ui);display:flex;align-items:center;justify-content:center;opacity:0">✓</div>`);
    hidden(c);
    return c;
  });
  ["power", "safe", "breadboard", "built"].forEach((w, i) => {
    pop(cards[i], W("s40", w) - 0.15);
    const ok = $(".ok", cards[i]);
    SET(ok, W("s40", w) + 0.2, { scale: 0.4 });
    TO(ok, W("s40", w) + 0.2, 0.4, { opacity: 1, scale: 1, ease: "back.out(2)" });
  });
  hide(cards, T("s41") - 0.1, 0.4); hide(h, T("s41") - 0.1, 0.4);
  const nx = box(sOutro, 260, 260, 1400, 330, "card", `<div style="padding:50px 60px"><div class="kicker">Next episode</div>
    <div style="font:700 60px var(--display);margin:14px 0 18px">Blink an LED from code</div>
    <div class="muted" style="font-size:28px">One wire moves to a GPIO pin, and our program takes control.</div></div>`);
  hidden(nx); pop(nx, T("s41") + 0.2);
  const gh = box(sOutro, 260, 640, 1400, 120, "card", `<div style="display:flex;align-items:center;gap:26px;height:120px;padding:0 50px">
    <svg width="54" height="54" viewBox="0 0 16 16"><path fill="#fff" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
    <div style="font:600 36px var(--mono)">github.com/emjnbulut/esp32-from-zero</div></div>`);
  hidden(gh); pop(gh, W("s41", "GitHub"));
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 });
  TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}

window.__seek(0);
window.__ready = true;
