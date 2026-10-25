/* Episode 5 - PWM and RGB Color Mixing (2026-10-25).
 * PRODUCTION_GUIDELINES.md: cold open with the real result, big code cards, quick questions, cause and effect
 * (value -> duty cycle -> brightness / color), full-screen real results, max 2 subtle like/subscribe reminders,
 * the end invites comments. Segment ids: see make_script.py (cold1 = s01 ... out2 = s45). */
const stage = $("#stage");
const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const hidden = (e) => { gsap.set(e, { opacity: 0 }); return e; };
const CUT = S0("s04") - 0.1; // the channel sting is inserted here (tools/bumpers.py cut())
function head(parent, html, y = 60) {
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
/** an RGB "light": a frosted dome whose color follows fn(t) -> [r, g, b] (0..255) */
function rgbIcon(parent, x, y, w = 160) {
  const r = box(parent, x, y, w, w * 1.6, "");
  const glow = box(r, -w * 0.8, -w * 0.75, w * 2.6, w * 2.6, "");
  css(glow, { borderRadius: "50%", opacity: 0 });
  r.insertAdjacentHTML("beforeend", `<svg width="${w}" viewBox="0 0 120 190" style="position:absolute;left:0;top:0">
    <path d="M34 96 V176 M52 96 V190 M68 96 V176 M86 96 V172" stroke="#c3c9d1" stroke-width="5" stroke-linecap="round"/>
    <path class="dome" d="M24 96 V52 a36 36 0 0 1 72 0 V96 z" fill="#e8edf3" opacity=".9"/>
    <path d="M18 92 h84 v12 h-84 z" fill="#c9d0d8"/></svg>`);
  const dome = $(".dome", r);
  const drive = (fn) => dyn((t) => {
    const [R, G, B] = fn(t), m = Math.max(R, G, B) / 255;
    const c = `rgb(${Math.round(150 + R * 0.41)},${Math.round(150 + G * 0.41)},${Math.round(150 + B * 0.41)})`;
    dome.setAttribute("fill", m > 0.02 ? c : "#e8edf3");
    glow.style.opacity = m;
    glow.style.background = `radial-gradient(circle, rgba(${R},${G},${B},.9) 0%, rgba(${R},${G},${B},.4) 30%, rgba(${R},${G},${B},0) 65%)`;
  });
  return { r, glow, drive };
}
const blink = (t, t0, on, off) => (t < t0 ? 0 : ((t - t0) % (on + off)) < on ? 1 : 0);
const inAny = (t, list) => list.some(([a, b]) => t >= a && t < b);
/** the breathing fade of fade_millis: 0..1..0, one step every `ms` ms (255 steps up, 255 down) */
const tri = (t, t0, ms = 4) => { const P = 2 * 255 * ms / 1000, x = ((t - t0) % P + P) % P / P; return x < 0.5 ? x * 2 : 2 - x * 2; };
function btnIcon(parent, x, y, w = 150) {
  const r = box(parent, x, y, w, w, "");
  r.innerHTML = `<svg width="${w}" height="${w}" viewBox="0 0 100 100" style="position:absolute;left:0;top:0">
    <rect x="22" y="2" width="8" height="16" rx="2" fill="#aab2bd"/><rect x="70" y="2" width="8" height="16" rx="2" fill="#aab2bd"/>
    <rect x="22" y="82" width="8" height="16" rx="2" fill="#aab2bd"/><rect x="70" y="82" width="8" height="16" rx="2" fill="#aab2bd"/>
    <rect x="10" y="12" width="80" height="76" rx="8" fill="#23272f" stroke="#3a404b" stroke-width="2"/>
    <circle class="cap" cx="50" cy="50" r="24" fill="#4a5262" stroke="#11141a" stroke-width="3"/></svg>`;
  const cap = $(".cap", r);
  const press = (list) => dyn((t) => { const on = inAny(t, list); cap.setAttribute("r", on ? 20 : 24); cap.setAttribute("fill", on ? "#ffb547" : "#4a5262"); });
  return { r, press };
}
const pill = (parent, x, y, html, style = "") => {
  const p = box(parent, x, y, 0, 0, "", `<span class="pill" style="font-size:28px;${style}">${html}</span>`);
  css(p, { width: "auto", height: "auto", whiteSpace: "nowrap" });
  return hidden(p);
};
const pillC = (parent, y, html, style = "") => hidden(box(parent, 0, y, 1920, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:30px;${style}">${html}</span></div>`));
function valBox(parent, x, y, w, list, size = 34) {
  const b = box(parent, x, y, w, 0, "card", "");
  css(b, { height: "auto", padding: "16px 24px", font: `700 ${size}px var(--mono)`, whiteSpace: "nowrap" });
  textAt(b, list);
  return hidden(b);
}
const zcam = (z, t, dur, cx, cy, s) => TO(z, t, dur, { x: 960 - s * cx, y: 540 - s * cy, scale: s, ease: "power2.inOut" });
const zset = (z, t, cx, cy, s) => SET(z, t, { x: 960 - s * cx, y: 540 - s * cy, scale: s });
/** a PWM square wave in an svg group: duty 0..1, `cycles` periods across w px; returns the path */
function wave(g, x, y, w, h, duty, cycles = 6, color = "#ffb547") {
  let d = `M${x} ${y + h}`;
  const p = w / cycles;
  for (let i = 0; i < cycles; i++) {
    const x0 = x + i * p;
    if (duty >= 1) d += ` H${x0} V${y} H${x0 + p}`;
    else if (duty <= 0) d += ` H${x0 + p}`;
    else d += ` H${x0} V${y} H${x0 + p * duty} V${y + h} H${x0 + p}`;
  }
  return svgEl(g, "path", { d, stroke: color, "stroke-width": 6, fill: "none", "stroke-linejoin": "round" });
}

/* ======================================================================
 * COLD OPEN (s01-s03)
 * ==================================================================== */
const sCold = SC();
SET(sCold, 0, { opacity: 1 });
SET(sCold, CUT, { opacity: 0 });
heroClip(stage, "C0", 0, S1("s02") + 0.35, "The red LED breathing, the RGB LED changing colour; one press -> next mode.", { full: true });
{
  const kick = box(sCold, 140, 250, 900, 40, "kicker", "ESP32 From Zero · Episode 5");
  const title = box(sCold, 134, 296, 1100, 260, "h1", "Fade it.<br>Mix it.");
  css(title, { fontSize: "118px", lineHeight: "1.02" });
  const sub = box(sCold, 140, 566, 1000, 60, "h3", "one function: <span style='font-family:var(--mono);color:var(--teal)'>analogWrite()</span>");
  for (const e of [kick, title, sub]) gsap.set(e, { opacity: 0, y: 30 });
  [[kick, T("s03") - 0.3], [title, T("s03")], [sub, W("s03", "function")]].forEach(([e, t]) => TO(e, t, 0.7, { opacity: 1, y: 0, ease: "power3.out" }));
  const R = ledIcon(sCold, 1250, 250, 130), G = rgbIcon(sCold, 1530, 250, 170);
  hidden(R.r); hidden(G.r); show([R.r, G.r], T("s03") - 0.2, 0.4);
  R.drive((t) => tri(t, 0, 4));
  G.drive((t) => { const k = tri(t, 0, 8) * 255; return [k, 0, 255 - k]; });
}

/* ======================================================================
 * WHAT YOU NEED (s04)
 * ==================================================================== */
const sParts = SC();
sceneIn(sParts, CUT, 0.4);
sceneOut(sParts, S1("s04") + 0.4);
{
  const h = head(sParts, "What you need", 90); show(h, CUT + 0.1);
  const res = `<svg width="180" height="60" viewBox="0 0 180 60"><path d="M0 30 H180" stroke="#b8bec6" stroke-width="5"/><rect x="50" y="14" width="80" height="32" rx="13" fill="#dcc79f" stroke="#b49e72"/>
    <rect x="62" y="14" width="8" height="32" fill="#d0262f"/><rect x="76" y="14" width="8" height="32" fill="#d0262f"/><rect x="90" y="14" width="8" height="32" fill="#7a4a21"/><rect x="112" y="14" width="8" height="32" fill="#c9a54a"/></svg>`;
  const rgb = `<svg width="90" height="150" viewBox="0 0 120 190"><path d="M34 96 V176 M52 96 V190 M68 96 V176 M86 96 V172" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/><path d="M24 96 V52 a36 36 0 0 1 72 0 V96 z" fill="#e8edf3"/><path d="M18 92 h84 v12 h-84 z" fill="#c9d0d8"/><circle cx="46" cy="66" r="8" fill="#ff5d6c"/><circle cx="62" cy="54" r="8" fill="#4ade80"/><circle cx="76" cy="68" r="8" fill="#5aa9ff"/></svg>`;
  const meter = `<svg width="120" height="170" viewBox="0 0 120 170"><rect x="8" y="4" width="104" height="162" rx="14" fill="#f2c230"/><rect x="20" y="18" width="80" height="44" rx="5" fill="#cfe3c4"/><text x="60" y="49" text-anchor="middle" font-family="Consolas" font-weight="700" font-size="22" fill="#1c2a14">1.65</text><circle cx="60" cy="108" r="26" fill="#2b2f36"/><path d="M60 108 l14 -14" stroke="#f2c230" stroke-width="6"/></svg>`;
  const items = [["circuit", `<div style="font:800 30px var(--display);color:var(--teal);line-height:1.2">episode 4<br>circuit</div>`, "red LED + button", "already built"], ["RGB", rgb, "RGB LED", "4 legs"],
    ["resistors", res, "3 × 220 Ω", "one per color"], ["wires", `<div style="font-size:70px">〰️</div>`, "jumper wires", "a few"], ["multimeter", meter, "multimeter", "optional"]];
  items.forEach(([w, art, nm, ds], i) => {
    const c = box(sParts, 160 + i * 330, 300, 300, 420, "card partcard", `<div class="art" style="height:270px;padding-top:20px">${art}</div><div class="nm" style="font-size:28px">${nm}</div><div class="ds">${ds}</div>`);
    hidden(c); pop(c, W("s04", w) - 0.1);
  });
}

/* ======================================================================
 * PWM, THE IDEA (s05-s09)
 * ==================================================================== */
const sPwm = SC();
sceneIn(sPwm, S1("s04") + 0.4);
sceneOut(sPwm, S1("s09") + 0.4);
{
  const hd = box(sPwm, 0, 50, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s05"), "digitalWrite: only ON or OFF"], [T("s07"), "The trick: switch it fast"], [T("s08"), "PWM · pulse width modulation"], [T("s09"), "The duty cycle sets the brightness"]]);
  // s05: on / off
  const L = ledIcon(sPwm, 860, 240, 150);
  hidden(L.r); show(L.r, T("s05"), 0.4); hide(L.r, T("s07") - 0.1, 0.3);
  const tOn = W("s05", "on", 2), tOff = W("s05", "off");
  L.drive((t) => (t >= tOn && t < tOff ? 1 : 0));
  for (const [txt, x, w, col] of [["HIGH → fully on", 480, "on", "var(--amber)"], ["LOW → fully off", 1180, "off", "var(--muted)"]]) {
    const c = pill(sPwm, x, 600, txt, `font-size:32px;color:${col}`); pop(c, W("s05", w)); hide(c, T("s07") - 0.1, 0.3);
  }
  quizCard(sPwm, "A pin is only ON or OFF. How does an LED glow at half brightness?", W("s06", "Quick"), T("s07"), "Switch it on and off very fast: on half the time", { y: 760, w: 1500, t1: T("s08") - 0.1 });
  // s07: a fast square wave and the LED at its average
  const sv = svgLayer(sPwm);
  const g7 = svgEl(sv, "g", { opacity: 0 });
  TO(g7, T("s07"), 0.4, { opacity: 1 }); TO(g7, T("s09") - 0.1, 0.3, { opacity: 0 });
  const wv = wave(g7, 220, 260, 1100, 160, 0.5, 8);
  drawOn(wv, T("s07") + 0.2, 1.2);
  for (const [txt, y] of [["ON", 270], ["OFF", 420]]) svgEl(g7, "text", { x: 190, y, "text-anchor": "end", "font-family": "Segoe UI", "font-weight": 700, "font-size": 26, fill: "#8fa1c0" }).textContent = txt;
  const L7 = ledIcon(sPwm, 1500, 230, 130);
  hidden(L7.r); show(L7.r, T("s07") + 0.3, 0.4); hide(L7.r, T("s09") - 0.1, 0.3);
  L7.drive((t) => (t < W("s07", "eye") ? blink(t, T("s07"), 0.25, 0.25) : 0.5));
  const avg = pill(sPwm, 1430, 520, "your eye sees: 50 %", ""); pop(avg, W("s07", "eye")); hide(avg, T("s09") - 0.1, 0.3);
  // s08: one cycle, the "on" part = duty cycle
  const cyc = svgEl(sv, "g", { opacity: 0 });
  TO(cyc, W("s08", "cycle"), 0.3, { opacity: 1 }); TO(cyc, T("s09") - 0.1, 0.3, { opacity: 0 });
  const p = 1100 / 8;
  svgEl(cyc, "path", { d: `M220 470 H${220 + p} M220 458 V482 M${220 + p} 458 V482`, stroke: "#19c3b4", "stroke-width": 4 });
  svgEl(cyc, "text", { x: 220 + p / 2, y: 512, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 24, fill: "#19c3b4" }).textContent = "1 cycle ≈ 1 ms";
  const on8 = svgEl(sv, "rect", { x: 220, y: 256, width: p / 2, height: 168, rx: 6, fill: "rgba(255,181,71,.28)", opacity: 0 });
  TO(on8, W("s08", "stays"), 0.3, { opacity: 1 }); TO(on8, T("s09") - 0.1, 0.3, { opacity: 0 });
  const dl = pill(sPwm, 220, 560, "how long it stays ON = the duty cycle", "font-size:30px");
  pop(dl, W("s08", "duty")); hide(dl, T("s09") - 0.1, 0.3);
  // s09: 25 / 50 / 100 %
  [[0.25, "25 %", "Twentyfive", 0.25], [0.5, "50 %", "Fifty", 0.5], [1, "100 %", "hundred", 1]].forEach(([duty, lab, w, k], i) => {
    const y = 220 + i * 250, t0 = W("s09", w) - 0.1;
    const g = svgEl(sv, "g", { opacity: 0 }); TO(g, t0, 0.35, { opacity: 1 });
    wave(g, 380, y, 900, 110, duty, 6);
    svgEl(g, "text", { x: 330, y: y + 70, "text-anchor": "end", "font-family": "Segoe UI", "font-weight": 800, "font-size": 40, fill: "#e8eef7" }).textContent = lab;
    const Li = ledIcon(sPwm, 1450, y - 40, 90);
    hidden(Li.r); show(Li.r, t0, 0.35); Li.drive(() => k);
  });
}

/* ======================================================================
 * analogWrite (s10-s13)
 * ==================================================================== */
const sAw = SC();
sceneIn(sAw, S1("s09") + 0.4);
sceneOut(sAw, S1("s13") + 0.4);
{
  const hd = head(sAw, "analogWrite(pin, 0 … 255)", 50); show(hd, T("s10"));
  hd.style.fontFamily = "var(--mono)";
  const code = bigCode(sAw, 160, 180, 1600, "analogWrite(LED_PIN, 128);", { size: 64 });
  show(code.c, T("s10"), 0.4); hide(code.c, T("s11") - 0.1, 0.3);
  // the value -> duty cycle -> brightness bar
  const val = (t) => {
    if (t < W("s10", "Zero", 2)) return 128;
    if (t < W("s10", "Two", 2)) return 0;
    if (t < T("s11")) return 255;
    if (t < W("s11", "one")) return 64;
    return 128;
  };
  const bar = box(sAw, 260, 470, 1400, 80, "card", "");
  hidden(bar); show(bar, T("s10") + 0.3, 0.4); hide(bar, T("s11") - 0.1, 0.3);
  const fill = box(bar, 0, 0, 0, 80, "");
  css(fill, { background: "linear-gradient(90deg, rgba(255,181,71,.35), rgba(255,181,71,.9))", borderRadius: "20px" });
  const lab = box(sAw, 260, 570, 1400, 60, "", "");
  css(lab, { font: "700 34px var(--mono)", textAlign: "center" }); hidden(lab); show(lab, T("s10") + 0.3, 0.4); hide(lab, T("s11") - 0.1, 0.3);
  const L = ledIcon(sAw, 1700, 620, 110);
  hidden(L.r); show(L.r, T("s10") + 0.3, 0.4); hide(L.r, T("s12") - 0.1, 0.3);
  L.drive((t) => val(t) / 255);
  dyn((t) => {
    const v = val(t);
    fill.style.width = (v / 255) * 1400 + "px";
    const h = `analogWrite(…, <span style="color:var(--amber)">${v}</span>) → <span style="color:var(--teal)">${Math.round(v / 2.55)} %</span> on`;
    if (lab.__v !== h) { lab.innerHTML = h; lab.__v = h; }
  });
  // s11: pwm_levels
  const c2 = bigCode(sAw, 160, 170, 1600, "showLevel(0);\nshowLevel(64);    // 25%\nshowLevel(128);   // 50%\nshowLevel(255);   // 100%", { size: 44 });
  show(c2.c, T("s11") + 0.4, 0.4); hide(c2.c, T("s12") - 0.1, 0.3);
  c2.hl([[0, -1], [W("s11", "sixtyfour"), 1], [W("s11", "twentyeight"), 2], [W("s11", "steps"), 3], [S1("s11"), -1]]);
  // s12: any pin
  const pins = pillC(sAw, 470, "ESP32: almost every output pin can do PWM", "font-size:36px");
  pop(pins, W("s12", "every")); hide(pins, T("s13") - 0.1, 0.3);
  likeSub(stage, W("s12", "pick") + 0.4); // reminder 1 of 2: right after the first results
  // s13: the multimeter shows the average
  const mv = box(sAw, 0, 0, 1920, 1080, ""); hidden(mv); show(mv, T("s13"), 0.4);
  mv.innerHTML = `<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0">
    <rect x="760" y="200" width="400" height="620" rx="40" fill="#f2c230"/><rect x="810" y="250" width="300" height="160" rx="14" fill="#cfe3c4"/>
    <circle cx="960" cy="560" r="100" fill="#2b2f36"/><path d="M960 560 l60 -60" stroke="#f2c230" stroke-width="16"/>
    <path d="M880 820 C 860 900, 700 920, 640 960 M1040 820 C 1060 900, 1220 920, 1280 960" stroke="#d63b3b" stroke-width="10" fill="none"/></svg>`;
  const rd = box(mv, 810, 280, 300, 110, "");
  css(rd, { font: "800 84px Consolas, monospace", color: "#1c2a14", textAlign: "center" });
  textAt(rd, [[0, "0.00"], [W("s13", "zero"), "0.80"], [W("s13", "one"), "1.65"], [W("s13", "three"), "3.30"]]);
  const vs = [["25 % → 0.8 V", "zero"], ["50 % → 1.65 V", "one"], ["100 % → 3.3 V", "three"]];
  vs.forEach(([txt, w], i) => { const c = pill(mv, 1260, 300 + i * 100, txt, "font-size:32px"); pop(c, W("s13", w)); });
  const av = pill(mv, 260, 300, "the meter shows the average", "font-size:30px"); pop(av, W("s13", "average"));
  heroClip(stage, "C1", S1("s13") + 0.2, T("s14") - 0.3, "Multimeter on the LED pin, pwm_levels running: 0 -> 0.8 -> 1.65 -> 3.3 V.", { full: true });
}

/* ======================================================================
 * THE FADE: naive first, then millis() (s14-s22)
 * ==================================================================== */
const sFade = SC();
sceneIn(sFade, S1("s13") + 0.4);
sceneOut(sFade, S1("s22") + 0.4);
{
  const hd = box(sFade, 0, 40, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s14"), "Make it breathe: the obvious way"], [T("s17"), "The episode 4 trick: one small step every 4 ms"],
    [T("s19"), "See it: the Serial Plotter"], [T("s22"), "A fade that never waits"]]);
  const naive = bigCode(sFade, 90, 160, 1000, "for (int b = 0; b <= 255; b++) {\n  analogWrite(LED_PIN, b);\n  delay(4);\n}\n// ...and another loop back down", { size: 40 });
  show(naive.c, T("s14"), 0.4); hide(naive.c, T("s17") - 0.1, 0.3);
  naive.hl([[0, -1], [W("s14", "loop"), 0], [W("s14", "delay"), 2], [W("s14", "another"), 4], [S1("s14"), -1], [W("s16", "delay"), 2, "rgba(255,93,108,.28)"]]);
  const Ln = ledIcon(sFade, 1500, 170, 120);
  hidden(Ln.r); show(Ln.r, T("s14"), 0.4); hide(Ln.r, T("s17") - 0.1, 0.3);
  Ln.drive((t) => tri(t, T("s14"), 4));
  quizCard(sFade, "While that loop is fading, you press the button. What happens?", W("s15", "Quick"), T("s16"), "Nothing: the loop is busy in delay() for the whole fade", { y: 770, w: 1500, t1: T("s17") - 0.1 });
  const blk = box(sFade, 1150, 520, 680, 150, "card", `<div style="padding:22px 28px"><div style="font:700 26px var(--ui);color:var(--muted)">one fade, up and down</div>
    <div style="margin-top:14px;height:44px;border-radius:10px;background:rgba(255,93,108,.55);display:flex;align-items:center;justify-content:center;font:800 26px var(--ui)">≈ 2 s not looking at the button</div></div>`);
  hidden(blk); pop(blk, W("s16", "two")); hide(blk, T("s17") - 0.1, 0.3);
  // s17-s18: the millis() step
  const step = bigCode(sFade, 90, 150, 1060, "if (now - lastStep >= 4) {\n  lastStep = now;\n  brightness = brightness + step;\n  if (brightness >= 255) step = -1;\n  if (brightness <= 0) step = 1;\n  analogWrite(LED_PIN, brightness);\n}", { size: 36 });
  show(step.c, T("s17"), 0.4); hide(step.c, T("s19") - 0.1, 0.3);
  step.hl([[0, -1], [W("s17", "Every"), 0], [W("s17", "brightness"), 2], [S1("s17"), -1], [W("s18", "top"), 3], [W("s18", "bottom"), 4], [S1("s18"), -1]]);
  const tS = T("s17");
  const bv = valBox(sFade, 1250, 200, 560, [[0, ""]], 38);
  show(bv, tS + 0.3, 0.4); hide(bv, T("s19") - 0.1, 0.3);
  dyn((t) => {
    if (t < tS || t > T("s19")) return;
    const b = Math.round(tri(t, tS, 4) * 255), up = ((t - tS) % 2.04) < 1.02;
    const h = `brightness = <span style="color:var(--amber)">${b}</span><br>step = <span style="color:${up ? "var(--teal)" : "var(--red)"}">${up ? "+1" : "-1"}</span>`;
    if (bv.__v !== h) { bv.innerHTML = h; bv.__v = h; }
  });
  const Ls = ledIcon(sFade, 1450, 450, 120);
  hidden(Ls.r); show(Ls.r, tS + 0.3, 0.4); hide(Ls.r, T("s19") - 0.1, 0.3);
  Ls.drive((t) => tri(t, tS, 4));
  const sec = pill(sFade, 1250, 760, "255 steps × 4 ms ≈ 1 second", "font-size:28px");
  pop(sec, W("s17", "Two")); hide(sec, T("s19") - 0.1, 0.3);
  // s19-s21: the Serial Plotter
  const plot = box(sFade, 200, 170, 1520, 560, "", "");
  css(plot, { background: "#111617", border: "1px solid #2e373a", borderRadius: "10px" }); hidden(plot);
  show(plot, T("s19"), 0.4); hide(plot, T("s22") - 0.1, 0.3);
  box(plot, 0, 0, 1520, 40, "", `<div style="height:40px;display:flex;align-items:center;padding-left:18px;font:600 18px var(--ui);color:#ddd;background:#0d1112;border-radius:10px 10px 0 0">Serial Plotter · 115200 baud</div>`);
  const ps = svgLayer(plot, 1520, 560);
  for (const [y, v] of [[90, "255"], [500, "0"]]) {
    svgEl(ps, "path", { d: `M70 ${y} H1490`, stroke: "#2a3336", "stroke-width": 2 });
    svgEl(ps, "text", { x: 58, y: y + 7, "text-anchor": "end", "font-family": "Consolas", "font-size": 20, fill: "#8fa1c0" }).textContent = v;
  }
  const trianglePath = (period) => { let d = "", x = 70; const w = 1420; for (let k = 0; x < 70 + w; k++) { d += `${k ? "L" : "M"}${x} ${k % 2 ? 90 : 500} `; x += period; } return d; };
  const p4 = svgEl(ps, "path", { d: trianglePath(170), stroke: "#4fc1ff", "stroke-width": 4, fill: "none" });
  drawOn(p4, W("s19", "Plotter"), 2.5);
  const p10 = svgEl(ps, "path", { d: trianglePath(425), stroke: "#4ade80", "stroke-width": 4, fill: "none", opacity: 0 });
  SET(p10, T("s21") - 0.01, { opacity: 1 });
  SET(p4, T("s21"), { opacity: 0.25 });
  drawOn(p10, T("s21"), 2.5);
  const tlab = pill(sFade, 220, 760, "<span style='color:#4fc1ff'>4 ms: 1 s up, 1 s down</span>", "font-size:28px");
  pop(tlab, W("s19", "triangle")); hide(tlab, T("s22") - 0.1, 0.3);
  const tlab2 = pill(sFade, 820, 760, "<span style='color:#4ade80'>10 ms: ≈ 2.5 s, same height</span>", "font-size:28px");
  pop(tlab2, W("s21", "wider")); hide(tlab2, T("s22") - 0.1, 0.3);
  quizCard(sFade, "4 ms → 10 ms. What changes in the picture?", W("s20", "Quick"), T("s21"), "The triangle gets wider; the height stays 0 to 255", { y: 850, w: 1300, t1: S1("s21") });
  heroClip(stage, "C2", W("s22", "pauses"), T("s23") - 0.3, "fade_millis: the LED breathes; a press pauses it mid-fade, another resumes.", { full: true });
}

/* ======================================================================
 * RGB LED: what it is, the wiring on the upper breadboard (s23-s28)
 * ==================================================================== */
const sRgb = SC();
sceneIn(sRgb, S1("s22") + 0.4);
sceneOut(sRgb, S1("s28") + 0.4);
{
  // s23: three LEDs in one package
  const hd = box(sRgb, 0, 40, 1920, 80, "h2", ""); hd.style.textAlign = "center"; css(hd, { zIndex: 30 });
  panelAt(hd, [[0, ""], [T("s23"), "Part 2: three LEDs in one"], [T("s24"), "The upper breadboard"], [T("s27"), "Why three resistors?"], [T("s28"), "Common cathode or common anode?"]]);
  const pk = box(sRgb, 0, 0, 1920, 1080, ""); hidden(pk); show(pk, T("s23"), 0.4); hide(pk, T("s24") - 0.1, 0.3);
  const big = rgbIcon(pk, 820, 200, 280);
  big.drive((t) => (t < W("s23", "red") ? [0, 0, 0] : t < W("s23", "green") ? [255, 0, 0] : t < W("s23", "blue") ? [0, 255, 0] : t < W("s23", "four") ? [0, 0, 255] : [255, 255, 255]));
  // one label per leg, in leg order, as a list beside the LED
  [["red", "● red leg", "#ff5d6c"], ["longest", "● common leg (the longest)", "#e8eef7"], ["green", "● green leg", "#4ade80"], ["blue", "● blue leg", "#5aa9ff"]].forEach(([w, txt, col], i) => {
    const c = pill(pk, 1200, 300 + i * 90, txt, `font-size:30px;color:${col}`); pop(c, W("s23", w));
  });
  // the breadboards (episode 4 circuit), then the green LED comes off and the RGB LED goes in
  const Z = box(sRgb, 0, 0, 1920, 1080, ""); Z.style.transformOrigin = "0 0";
  const bb = makeBB2(Z, 0, 0);
  bbBoard(bb, 30, 2, ["1j", "2a"]);
  hidden(Z); show(Z, T("s24") - 0.1, 0.4); hide(Z, T("s27") - 0.1, 0.3);
  zset(Z, 0, 900, 420, 0.95);
  // lower breadboard (episode 4): red LED, button
  bbResistor(bb, bb.L(16, "2e"), bb.L(20, "2g")); bbLED(bb, bb.L(20, "2h"), bb.L(21, "2h"), 1);
  bbWire(bb, bb.L(21, "2j"), bb.L(21, "2bm"), "#2b2f36", -1, -0.35); bbWire(bb, bb.L(3, "2e"), bb.L(3, "2bm"), "#2b2f36", -1, 0.12);
  bbWire(bb, bb.L(15, "2c"), bb.L(25, "2c"), "#ffd34d", -1, -0.08); bbWire(bb, bb.L(27, "2j"), bb.L(27, "2bm"), "#2b2f36", -1, -0.35);
  bbWire(bb, bb.L(3, "1f"), bb.L(3, "1tm"), "#2b2f36", -1, 0.12);
  // the green LED circuit of episode 4, removed at "green"
  const old = svgEl(bb.parts, "g", {});
  const gw = bbWire(bb, bb.L(9, "1g"), bb.L(18, "1g"), "#3ddc84", -1, -0.06); old.appendChild(gw);
  old.appendChild(bbResistor(bb, bb.L(18, "1f"), bb.L(21, "1d")));
  old.appendChild(bbLED(bb, bb.L(21, "1c"), bb.L(22, "1c"), -1, "green").g);
  old.appendChild(bbWire(bb, bb.L(22, "1a"), bb.L(22, "1tm"), "#2b2f36", -1, 0.35));
  TO(old, W("s24", "green") + 0.3, 0.6, { opacity: 0, y: -40, ease: "power2.in" });
  callout(Z, "green LED off", bb.L(19, "1b")[0], bb.L(19, "1b")[1] - 90, W("s24", "green"), W("s24", "pin"), { style: { fontSize: "26px" } });
  const usb = box(sRgb, 60, 40, 0, 0, "badge", `<span style="color:var(--red)">● USB unplugged</span>`);
  css(usb, { width: "auto", height: "auto", background: "rgba(11,18,32,.9)", border: "1px solid var(--line)", zIndex: 31 }); hidden(usb);
  show(usb, W("s24", "Unplug"), 0.3); hide(usb, T("s27") - 0.1, 0.3);
  // s25: the RGB LED in row c, columns 20-23 (R, common, G, B), black wire common -> minus rail
  const legs = svgEl(bb.parts, "g", { opacity: 0 });
  const [x20, yc] = bb.L(20, "1c"), [x23] = bb.L(23, "1c");
  svgEl(legs, "rect", { x: x20 - 22, y: yc - 64, width: x23 - x20 + 44, height: 52, rx: 26, fill: "#e8edf3", stroke: "#b9c1ca", "stroke-width": 2 });
  [[20, "#ff5d6c"], [21, "#9aa1aa"], [22, "#4ade80"], [23, "#5aa9ff"]].forEach(([c, col]) => {
    const [lx, ly] = bb.L(c, "1c"); svgEl(legs, "path", { d: `M${lx} ${ly - 14} V${ly}`, stroke: col, "stroke-width": 6 }); svgEl(legs, "circle", { cx: lx, cy: ly, r: 6, fill: col });
  });
  TO(legs, W("s25", "Push") + 0.1, 0.4, { opacity: 1 });
  callout(Z, "longest leg: 2nd from the left", bb.L(21, "1a")[0] - 40, bb.L(21, "1a")[1] - 120, W("s25", "longest"), T("s26"), { style: { fontSize: "26px" } });
  bbWire(bb, bb.L(21, "1a"), bb.L(21, "1tm"), "#2b2f36", W("s25", "black"), 0.35);
  // s26: one resistor + one pin per color
  const per = [["red", 9, 20, "1g", "#ff5d6c", "D25"], ["green", 8, 22, "1h", "#3ddc84", "D26"], ["blue", 7, 23, "1i", "#5aa9ff", "D27"]];
  for (const [w, pin, col, row, color, name] of per) {
    const t0 = W("s26", w);
    bbWire(bb, bb.L(pin, row), bb.L(col, row), color, t0, -0.05);
    const rg = svgEl(bb.parts, "g", { opacity: 0 }); rg.appendChild(bbResistor(bb, bb.L(col, "1f"), bb.L(col, "1e")));
    TO(rg, t0 + 0.4, 0.3, { opacity: 1 });
  }
  // the three pins sit side by side: one label for all of them, in pin order
  const pl = bb.L(7, "1j");
  callout(Z, `<span style="color:#1b3d7a">D27 blue</span> · <span style="color:#14532d">D26 green</span> · <span style="color:#7a1020">D25 red</span>`,
    pl[0] - 120, pl[1] - 250, W("s26", "red"), S1("s26"), { style: { fontSize: "26px" } });
  heroClip(stage, "C3", S1("s26") + 0.2, T("s27") - 0.3, "RGB LED wiring on the upper breadboard: long leg -> minus rail, three resistors + wires to D25/D26/D27.", { full: true });
  // s27: why three resistors
  const why = box(sRgb, 0, 0, 1920, 1080, ""); hidden(why); show(why, T("s27"), 0.4); hide(why, T("s28") - 0.1, 0.3);
  why.innerHTML = `<div class="card" style="position:absolute;left:230px;top:220px;width:680px;height:520px;padding:34px 40px">
      <div style="font:800 34px var(--display);color:var(--green)">✓ one resistor per color</div>
      <div style="font:600 28px var(--ui);color:var(--muted);margin-top:16px">three LEDs, three currents,<br>each one set by its own resistor</div>
      <div style="display:flex;gap:30px;margin-top:60px;justify-content:center">${["#ff5d6c", "#4ade80", "#5aa9ff"].map((c) => `<div style="text-align:center"><div style="width:22px;height:120px;margin:0 auto;background:${c};border-radius:6px"></div><div style="font:700 22px var(--ui);margin-top:10px">220 Ω</div></div>`).join("")}</div></div>
    <div class="card" style="position:absolute;left:1010px;top:220px;width:680px;height:520px;padding:34px 40px">
      <div style="font:800 34px var(--display);color:var(--red)">✕ one shared resistor</div>
      <div style="font:600 28px var(--ui);color:var(--muted);margin-top:16px">the colors steal current<br>from each other: the mix changes</div>
      <div style="display:flex;gap:30px;margin-top:60px;justify-content:center">${["#ff5d6c", "#4ade80", "#5aa9ff"].map((c) => `<div style="width:22px;height:120px;background:${c};border-radius:6px;opacity:.6"></div>`).join("")}</div></div>`;
  // s28: cathode vs anode
  const ca = box(sRgb, 0, 0, 1920, 1080, ""); hidden(ca); show(ca, T("s28"), 0.4);
  ca.innerHTML = `<div class="card" style="position:absolute;left:230px;top:230px;width:680px;height:420px;padding:34px 40px">
      <div class="kicker">most kits</div><div style="font:800 40px var(--display);margin-top:10px">common cathode</div>
      <div style="font:600 30px var(--ui);color:var(--muted);margin-top:22px">long leg → <b style="color:var(--text)">GND</b><br>255 = brightest</div>
      <div style="font:700 32px var(--mono);color:var(--teal);margin-top:30px">COMMON_ANODE = false</div></div>
    <div class="card" style="position:absolute;left:1010px;top:230px;width:680px;height:420px;padding:34px 40px">
      <div class="kicker" style="color:var(--amber)">if yours looks inverted</div><div style="font:800 40px var(--display);margin-top:10px">common anode</div>
      <div style="font:600 30px var(--ui);color:var(--muted);margin-top:22px">long leg → <b style="color:var(--text)">3.3 V</b><br>colors come out inverted</div>
      <div style="font:700 32px var(--mono);color:var(--amber);margin-top:30px">COMMON_ANODE = true</div></div>`;
}

/* ======================================================================
 * setColor() AND MIXING (s29-s35)
 * ==================================================================== */
const sCol = SC();
sceneIn(sCol, S1("s28") + 0.4);
sceneOut(sCol, S1("s35") + 0.4);
{
  const hd = box(sCol, 0, 40, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s29"), "One helper: setColor(r, g, b)"], [T("s31"), "Mixing light"], [T("s34"), "A cleaner white"]]);
  const code = bigCode(sCol, 90, 160, 980, "void setColor(int r, int g, int b) {\n  analogWrite(RED_PIN, r);\n  analogWrite(GREEN_PIN, g);\n  analogWrite(BLUE_PIN, b);\n}", { size: 38 });
  show(code.c, T("s29"), 0.4); hide(code.c, T("s31") - 0.1, 0.3);
  code.hl([[0, -1], [W("s29", "three"), 0], [T("s30"), 1], [T("s30") + 0.6, 2], [T("s30") + 1.2, 3], [W("s30", "Now"), -1]]);
  const call = bigCode(sCol, 90, 560, 980, "setColor(255, 0, 255);", { size: 44 });
  // the mixer: three sliders and the light
  const mixT = [[0, [255, 0, 0]], [W("s30", "Now"), [255, 0, 0]], [W("s31", "Quick"), [255, 0, 255]], [W("s32", "yellow"), [255, 255, 0]], [W("s32", "cyan"), [0, 255, 255]],
    [W("s32", "white"), [255, 255, 255]], [W("s33", "orange"), [255, 40, 0]], [T("s34"), [255, 255, 255]], [W("s34", "two"), [255, 200, 255]]];
  const mix = (t) => stateAt(mixT, t);
  const panel = box(sCol, 1130, 160, 700, 720, "card", ""); hidden(panel); show(panel, T("s29") + 0.3, 0.4);
  const rows = [["R", "#ff5d6c", 0], ["G", "#4ade80", 1], ["B", "#5aa9ff", 2]].map(([n, col, i]) => {
    box(panel, 40, 60 + i * 90, 40, 50, "", `<div style="font:800 32px var(--mono);color:${col}">${n}</div>`);
    const tr = box(panel, 100, 74 + i * 90, 420, 22, ""); css(tr, { background: "#22304d", borderRadius: "11px" });
    const f = box(tr, 0, 0, 0, 22, ""); css(f, { background: col, borderRadius: "11px" });
    const v = box(panel, 540, 60 + i * 90, 120, 50, ""); css(v, { font: "700 32px var(--mono)", textAlign: "right" });
    return [f, v];
  });
  const L = rgbIcon(panel, 270, 340, 160);
  const hideMix = (t) => t >= W("s31", "Quick") && t < T("s32"); // the quiz: keep the answer hidden
  L.drive((t) => (hideMix(t) ? [0, 0, 0] : mix(t)));
  const q = box(panel, 270, 380, 160, 120, "", `<div style="font:800 90px var(--display);text-align:center;color:var(--amber)">?</div>`);
  styleAt(q, "opacity", [[0, "0"], [W("s31", "Quick"), "1"], [T("s32"), "0"]]);
  dyn((t) => {
    const c = mix(t);
    rows.forEach(([f, v], i) => {
      f.style.width = (c[i] / 255) * 420 + "px";
      if (v.__v !== c[i]) { v.textContent = c[i]; v.__v = c[i]; }
    });
  });
  const name = box(panel, 0, 640, 700, 60, ""); css(name, { font: "800 36px var(--display)", textAlign: "center" });
  textAt(name, [[0, ""], [T("s32"), "<span style='color:#ff6bff'>magenta</span>"], [W("s32", "yellow"), "<span style='color:#ffe14d'>yellow</span>"],
    [W("s32", "cyan"), "<span style='color:#5ff'>cyan</span>"], [W("s32", "white"), "white"], [W("s33", "orange"), "<span style='color:#ff9a3c'>orange</span>"],
    [T("s34"), "white (255, 255, 255)"], [W("s34", "two"), "cleaner white (255, 200, 255)"]]);
  show(call.c, W("s31", "Quick"), 0.4); hide(call.c, T("s32") + 0.2, 0.3);
  quizCard(sCol, "setColor(255, 0, 255): what color is that?", W("s31", "Quick"), T("s32"), "Magenta: red + blue", { x: 90, y: 760, w: 980, t1: W("s32", "yellow") });
  const sw = box(sCol, 90, 200, 980, 560, ""); hidden(sw); show(sw, W("s32", "yellow") - 0.2, 0.3); hide(sw, T("s35") - 0.1, 0.3);
  sw.innerHTML = [["R + G", "yellow", "#ffe14d"], ["G + B", "cyan", "#5ff"], ["R + B", "magenta", "#ff6bff"], ["R + G + B", "white", "#fff"], ["255, 40, 0", "orange", "#ff9a3c"]]
    .map(([a, b, c], i) => `<div class="sw" style="position:absolute;left:${(i % 3) * 330}px;top:${Math.floor(i / 3) * 260}px;width:300px;height:230px;border-radius:22px;background:#121b2e;border:1px solid #22304d;opacity:0">
      <div style="width:110px;height:110px;border-radius:50%;margin:26px auto 10px;background:${c};box-shadow:0 0 50px ${c}"></div>
      <div style="text-align:center;font:700 26px var(--mono)">${a}</div><div style="text-align:center;font:600 22px var(--ui);color:var(--muted)">${b}</div></div>`).join("");
  const sws = sw.querySelectorAll(".sw");
  [W("s32", "yellow"), W("s32", "cyan"), W("s32", "Magenta"), W("s32", "white"), W("s33", "orange")].forEach((t, i) => pop(sws[i], t));
  const mil = pill(sCol, 90, 800, "256 × 256 × 256 ≈ 16.7 million colors", "font-size:30px");
  pop(mil, W("s33", "sixteen")); hide(mil, T("s34") - 0.1, 0.3);
  const gt = pill(sCol, 90, 800, "green looks strongest → try green at 200", "font-size:30px");
  pop(gt, W("s34", "Green")); hide(gt, T("s35") - 0.1, 0.3);
  likeSub(stage, W("s34", "two") + 0.6); // reminder 2 of 2: mid-episode, after the mixing payoff
  heroClip(stage, "C4", W("s35", "steps"), T("s36") - 0.3, "rgb_colors: red, green, blue, yellow, magenta, cyan, white, orange.", { full: true });
}

/* ======================================================================
 * ONE BUTTON, FOUR MODES (s36-s40)
 * ==================================================================== */
const sMode = SC();
sceneIn(sMode, S1("s35") + 0.4);
sceneOut(sMode, S1("s40") + 0.4);
{
  const hd = box(sMode, 0, 40, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s36"), "The button picks the mode"], [T("s39"), "One if per mode"]]);
  const c1 = bigCode(sMode, 90, 170, 980, "mode = mode + 1;\nif (mode > 3) {\n  mode = 0;\n}", { size: 46 });
  show(c1.c, T("s36"), 0.4); hide(c1.c, T("s39") - 0.1, 0.3);
  c1.hl([[0, -1], [W("s36", "adds"), 0], [W("s36", "zero"), 1], [S1("s36"), -1], [W("s38", "four"), 0], [W("s38", "greater"), 1], [W("s38", "zero"), 2], [S1("s38"), -1]]);
  // the circle of modes
  const cols = ["#ff5d6c", "#4ade80", "#5aa9ff", "linear-gradient(135deg,#5aa9ff,#ff5d6c)"], labs = ["red", "green", "blue", "fade"];
  const cx = 1500, cy = 520, R = 230;
  const ring = box(sMode, 0, 0, 1920, 1080, ""); hidden(ring); show(ring, T("s36") + 0.3, 0.4); hide(ring, T("s39") - 0.1, 0.3);
  const dots = labs.map((l, i) => {
    const a = -Math.PI / 2 + i * Math.PI / 2, x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
    return box(ring, x - 70, y - 70, 140, 140, "", `<div style="width:140px;height:140px;border-radius:50%;background:${cols[i]};display:flex;flex-direction:column;align-items:center;justify-content:center;font:800 40px var(--mono);color:#0b1220">${i}<span style="font:700 20px var(--ui)">${l}</span></div>`);
  });
  // the lit mode follows the narration: four presses around the circle, then the quiz (mode 3 -> back to 0)
  const modeAt = [[0, 0], [W("s36", "press"), 1], [W("s36", "adds") + 0.8, 2], [W("s36", "last"), 3], [W("s36", "zero"), 0],
    [W("s37", "Quick"), 3], [W("s38", "zero"), 0]];
  const cur = (t) => stateAt(modeAt, t);
  dyn((t) => dots.forEach((d, i) => { const on = cur(t) === i; d.style.transform = `scale(${on ? 1.15 : 0.85})`; d.style.opacity = on ? 1 : 0.45; }));
  const mv = valBox(sMode, 90, 520, 600, [[0, "mode = 0"], [W("s37", "Quick"), "mode = 3"], [W("s38", "four"), "mode = <span style='color:var(--red)'>4</span> ?"], [W("s38", "zero"), "mode = <span style='color:var(--teal)'>0</span>  → red"]], 40);
  show(mv, W("s37", "Quick") - 0.2, 0.3); hide(mv, T("s39") - 0.1, 0.3);
  quizCard(sMode, "mode is 3 and you press again. What happens?", W("s37", "Quick"), T("s38"), "It becomes 4 for a moment, then the if sends it back to 0", { x: 90, y: 760, w: 1000, t1: T("s39") - 0.1 });
  const c2 = bigCode(sMode, 90, 170, 1100, "if (mode == 0) {\n  setColor(255, 0, 0);\n} else if (mode == 1) {\n  setColor(0, 255, 0);\n} else if (mode == 2) {\n  setColor(0, 0, 255);\n} else {\n  // a slow fade, blue -> red\n}", { size: 34 });
  show(c2.c, T("s39"), 0.4);
  c2.hl([[0, -1], [W("s39", "zero"), 1], [W("s39", "one"), 3], [W("s39", "two"), 5], [W("s39", "three"), 7], [S1("s39"), -1]]);
  const L = rgbIcon(sMode, 1500, 260, 200);
  hidden(L.r); show(L.r, T("s39"), 0.4);
  L.drive((t) => (t < W("s39", "one") ? [255, 0, 0] : t < W("s39", "two") ? [0, 255, 0] : t < W("s39", "three") ? [0, 0, 255] : (() => { const k = tri(t, W("s39", "three"), 8) * 255; return [k, 0, 255 - k]; })()));
  heroClip(stage, "C5", W("s40", "Press"), T("s41") - 0.3, "color_modes: three presses red -> green -> blue -> fade.", { full: true });
}

/* ======================================================================
 * YOUR TURN (s41-s42): the solution stays in the lesson folder (not a mini-project)
 * ==================================================================== */
const sCh = SC();
sceneIn(sCh, S1("s40") + 0.4);
sceneOut(sCh, S1("s42") + 0.4);
{
  const dot = (c) => `<span style="display:inline-block;width:26px;height:26px;border-radius:50%;background:${c};box-shadow:0 0 14px ${c}"></span>`;
  yourTurnScene(sCh, {
    kicker: "YOUR TURN · CHALLENGE",
    title: "The smart camping headlamp",
    subtitle: "RGB LED + one button, everything from today",
    rule1Title: "One button, four modes",
    rule1Desc: "each press moves to the next mode",
    rule1FlowHtml: `<span class="muted">off</span><span>→</span>${dot("#9aa1aa")}<span>dim</span><span>→</span>${dot("#fff")}<span>bright</span><span>→</span>${dot("#ff5d6c")}<span>red blink</span>`,
    rule2Tag: "RULE 2 · THE TWIST",
    rule2Title: "On for 3 s or more? Straight off",
    rule2Desc: "if the lamp has been on for 3 seconds, the next press switches it off instead",
    rule2FlowHtml: `<span>on ≥ 3000 ms</span><span style="color:var(--amber)">→ press →</span><span class="muted">off</span>`,
    hintHtml: "remember when the mode last changed: <span style='font-family:var(--mono);color:var(--text)'>lastPress</span>, just like lastBlink",
    t0: T("s41"), tR1: W("s41", "cycles"), tR2: W("s42", "twist"), tHint: W("s42", "Hint"), tCom: W("s42", "comments"), tShort: W("s42", "folder"),
    shortText: "📁 &nbsp;One solution is in the lesson folder",
  });
}

/* ======================================================================
 * NOT WORKING? (s43)
 * ==================================================================== */
const sTrouble = SC();
sceneIn(sTrouble, S1("s42") + 0.4);
sceneOut(sTrouble, S1("s43") + 0.5);
{
  const chk = box(sTrouble, 300, 260, 1320, 440, "card", "");
  const rows = [["One color dark? Check that leg's resistor and wire", "color"], ["Inverted (white when off)? Common anode", "inverted"], ["COMMON_ANODE = true, long leg to 3.3 V", "set"]];
  chk.innerHTML = `<div style="padding:44px 60px"><div class="kicker">Something not working?</div>` + rows.map(([a]) => `<div class="row" style="display:flex;gap:22px;align-items:center;margin-top:40px;opacity:0">
    <div style="width:56px;height:56px;border-radius:50%;background:var(--green);color:#052;font:800 32px var(--ui);display:flex;align-items:center;justify-content:center">✓</div>
    <div style="font:600 38px var(--display)">${a}</div></div>`).join("") + `</div>`;
  chk.querySelectorAll(".row").forEach((r, i) => TO(r, W("s43", rows[i][1]), 0.4, { opacity: 1 }));
}

/* ======================================================================
 * OUTRO (s44-s45): recap, next episode, see you in the comments
 * ==================================================================== */
const sOutro = SC();
sceneIn(sOutro, S1("s43") + 0.5);
{
  const h = box(sOutro, 110, 170, 1500, 80, "h2", "Episode 5 complete!"); hidden(h); pop(h, T("s44"));
  const items = [["PWM", "fast on/off = any brightness", "PWM"], ["A fade", "that never waits", "fade"], ["RGB LED", "three LEDs in one", "RGB"], ["setColor()", "any color in one line", "function"]];
  const cards = items.map(([a, b, w], i) => {
    const c = box(sOutro, 110 + i * 435, 360, 400, 300, "card", `<div style="padding:34px"><div style="width:64px;height:64px;border-radius:50%;background:rgba(25,195,180,.15);color:var(--teal);font:700 32px var(--display);display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div style="font:700 34px var(--display);margin-top:28px">${a}</div><div class="muted" style="font-size:23px;margin-top:8px">${b}</div></div>`);
    hidden(c); pop(c, W("s44", w) - 0.15);
    return c;
  });
  hide(cards, T("s45") - 0.1, 0.4); hide(h, T("s45") - 0.1, 0.4);
  const nx = box(sOutro, 260, 200, 1400, 330, "card", `<div style="padding:50px 60px"><div class="kicker">Next episode</div>
    <div style="font:700 60px var(--display);margin:14px 0 18px">A knob: analogRead()</div>
    <div class="muted" style="font-size:28px">Read a potentiometer and turn it into brightness and color.</div></div>`);
  hidden(nx); pop(nx, T("s45") + 0.2);
  const cm = box(sOutro, 0, 580, 1920, 90, "", `<div style="display:flex;justify-content:center"><div class="yt-badge com">💬 &nbsp;Let's meet in the comments: which color did you mix?</div></div>`);
  hidden(cm); pop(cm, W("s45", "comments"));
  const gh = box(sOutro, 260, 720, 1400, 120, "card", `<div style="display:flex;align-items:center;gap:26px;height:120px;padding:0 50px">
    <div style="font:600 36px var(--mono)">github.com/emjnbulut/esp32-from-zero</div></div>`);
  hidden(gh); pop(gh, W("s45", "See"));
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 });
  TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}

window.__seek(0);
window.__ready = true;
