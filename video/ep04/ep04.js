/* Episode 4 - Buttons and Doing Two Things at Once (v2, 2026-10-25).
 * Follows video/PRODUCTION_GUIDELINES.md: cold open with the real result, big 3-6 line code cards,
 * code -> pin -> LED cause and effect, one idea at a time, quick questions, a millis() timeline,
 * full-screen real results. Hardware: two breadboards, the board across both.
 * All times come from the narration schedule (segment ids: see make_script.py). */
const stage = $("#stage");
const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const hidden = (e) => { gsap.set(e, { opacity: 0 }); return e; };
const CUT = S0("s04") - 0.1; // the channel sting is inserted here (tools/bumpers.py cut())
// full-code card after each sketch's real result (user 2026-10-27); make_script.py gives those segments the extra pad
const FC = 4.5, REPO = "Full code: <b>github.com/emjnbulut/esp32-from-zero</b> → lessons/04-buttons-and-millis · link in the description";
const fullAfter = (file, next) => fullCode(stage, file + ".ino", SKETCHES[file], T(next) - 0.3 - FC, T(next) - 0.3, REPO);
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
function btnIcon(parent, x, y, w = 150, label = true) {
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
    const txt = !label ? "" : on ? `<span style="color:var(--amber)">pressed</span>` : `<span style="color:var(--muted)">released</span>`;
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
/** a small labelled value box ("ledOn = true") whose html follows a schedule */
function valBox(parent, x, y, w, list, size = 34) {
  const b = box(parent, x, y, w, 0, "card", "");
  css(b, { height: "auto", padding: "16px 24px", font: `700 ${size}px var(--mono)`, whiteSpace: "nowrap" });
  textAt(b, list);
  return hidden(b);
}
const fn = (s) => `<span class="tk-fn">${s}</span>`;
const num = (s) => `<span class="tk-num">${s}</span>`;
const kw = (s) => `<span class="tk-kw">${s}</span>`;
const T_ = (v) => `<span style="color:var(--teal)">${v}</span>`;
const F_ = (v) => `<span style="color:var(--red)">${v}</span>`;
/** camera for a zoom container: centre container point (cx, cy) at scale s */
const zcam = (z, t, dur, cx, cy, s) => TO(z, t, dur, { x: 960 - s * cx, y: 540 - s * cy, scale: s, ease: "power2.inOut" });
const zset = (z, t, cx, cy, s) => SET(z, t, { x: 960 - s * cx, y: 540 - s * cy, scale: s });

/* ======================================================================
 * COLD OPEN (s01-s03): the finished project, full screen, then the promise
 * ==================================================================== */
const sCold = SC();
SET(sCold, 0, { opacity: 1 });
SET(sCold, CUT, { opacity: 0 });
heroClip(stage, "C0", 0, S1("s02") + 0.35, "The finished circuit: red blinks, green blinks fast; a press stops red, another starts it again.", { full: true });
{
  const kick = box(sCold, 140, 250, 900, 40, "kicker", "ESP32 From Zero · Episode 4");
  const title = box(sCold, 134, 296, 1100, 260, "h1", "Two things<br>at once");
  css(title, { fontSize: "118px", lineHeight: "1.02" });
  const sub = box(sCold, 140, 566, 1000, 60, "h3", "one button + a clock called <span style='font-family:var(--mono);color:var(--teal)'>millis()</span>");
  for (const e of [kick, title, sub]) gsap.set(e, { opacity: 0, y: 30 });
  [[kick, T("s03") - 0.3], [title, T("s03")], [sub, W("s03", "button")]].forEach(([e, t]) => TO(e, t, 0.7, { opacity: 1, y: 0, ease: "power3.out" }));
  // the result again, as a drawing: red + green blinking, the button stopping red
  const R = ledIcon(sCold, 1260, 250, 130, "red"), G = ledIcon(sCold, 1560, 250, 130, "green");
  const B = btnIcon(sCold, 1395, 640, 150, false);
  hidden(R.r); hidden(G.r); hidden(B.r);
  show([R.r, G.r], T("s03") - 0.2, 0.4); show(B.r, W("s03", "button") - 0.2, 0.4);
  const tP = W("s03", "button") + 0.2;
  B.press([[tP, tP + 0.3]]);
  R.drive((t) => (t < tP ? blink(t, 0, 0.5, 0.5) : 0));
  G.drive((t) => blink(t, 0, 0.15, 0.15));
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
  const bb = `<svg width="200" height="190" viewBox="0 0 200 190">${[0, 100].map((y) => `<rect x="4" y="${y + 4}" width="192" height="82" rx="8" fill="#ecebe6" stroke="#c9c6bd" stroke-width="2"/><rect x="10" y="${y + 40}" width="180" height="10" rx="3" fill="#d6d3cb"/>` +
    Array.from({ length: 12 }, (_, i) => `<rect x="${16 + i * 15}" y="${y + 18}" width="7" height="16" fill="#4a4842" opacity=".5"/><rect x="${16 + i * 15}" y="${y + 56}" width="7" height="16" fill="#4a4842" opacity=".5"/>`).join("")).join("")}</svg>`;
  const btn = `<svg width="130" height="130" viewBox="0 0 100 100"><rect x="22" y="2" width="8" height="16" rx="2" fill="#aab2bd"/><rect x="70" y="2" width="8" height="16" rx="2" fill="#aab2bd"/><rect x="22" y="82" width="8" height="16" rx="2" fill="#aab2bd"/><rect x="70" y="82" width="8" height="16" rx="2" fill="#aab2bd"/><rect x="10" y="12" width="80" height="76" rx="8" fill="#23272f" stroke="#3a404b" stroke-width="2"/><circle cx="50" cy="50" r="24" fill="#4a5262" stroke="#11141a" stroke-width="3"/></svg>`;
  const led = (a, b) => `<svg width="80" height="153" viewBox="0 0 120 230"><path d="M44 96 V226 M76 96 V186" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/><path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="${b}"/><path d="M36 60 a20 20 0 0 1 20 -24" stroke="${a}" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M22 92 h70 v14 h-70 z" fill="${b}" opacity=".8"/></svg>`;
  const wires = `<svg width="190" height="120" viewBox="0 0 190 120">${[["#ffd34d", 20], ["#3ddc84", 50], ["#2b2f36", 80], ["#ff5d6c", 110]].map(([c, y]) => `<path d="M10 ${y} Q95 ${y - 40} 180 ${y}" stroke="${c}" stroke-width="9" fill="none" stroke-linecap="round"/>`).join("")}</svg>`;
  const items = [["board", boardSVG({ pins: 30, chip: "cp2102", p: "pp", width: 112 }), "ESP32 board", "30-pin"], ["breadboards", bb, "2 breadboards", "one above the other"],
    ["button", btn, "push button", "4 legs"], ["red", led("#ffb3b3", "#d4202c"), "red LED", ""], ["green", led("#b3ffd0", "#1fae55"), "green LED", ""],
    ["resistors", res, "2 × 220 Ω", "resistors"], ["wires", wires, "jumper wires", "a few"]];
  items.forEach(([w, art, nm, ds], i) => {
    const c = box(sParts, 70 + i * 258, 300, 238, 420, "card partcard", `<div class="art" style="height:270px;padding-top:20px">${art}</div><div class="nm" style="font-size:26px">${nm}</div><div class="ds">${ds}</div>`);
    hidden(c); pop(c, W("s04", w) - 0.1);
  });
}

/* ======================================================================
 * THE PUSH BUTTON (s05-s07)
 * ==================================================================== */
const sBtn = SC();
sceneIn(sBtn, S1("s04") + 0.4);
sceneOut(sBtn, S1("s07") + 0.4);
{
  const h = head(sBtn, "The push button", 80); show(h, T("s05"));
  const sv = svgLayer(sBtn);
  const g = svgEl(sv, "g", { opacity: 0 });
  TO(g, T("s05") + 0.2, 0.5, { opacity: 1 });
  const L = 600, R = 820, TOP = 380, BOT = 760, CX = 710, CY = 570;
  for (const x of [L, R]) for (const [y0, y1] of [[TOP - 80, TOP + 10], [BOT - 10, BOT + 80]])
    svgEl(g, "rect", { x: x - 10, y: y0, width: 20, height: y1 - y0, rx: 4, fill: "#b8bec6" });
  svgEl(g, "rect", { x: L - 60, y: TOP, width: R - L + 120, height: BOT - TOP, rx: 22, fill: "#22262d", stroke: "#3a404b", "stroke-width": 4 });
  const cap = svgEl(g, "circle", { cx: CX, cy: CY, r: 110, fill: "#4a5262", stroke: "#11141a", "stroke-width": 6 });
  const pairs = [L, R].map((x) => svgEl(g, "path", { d: `M${x} ${TOP - 75} V${BOT + 75}`, stroke: "#19c3b4", "stroke-width": 10, "stroke-linecap": "round", fill: "none" }));
  drawOn(pairs[0], W("s06", "left"), 0.8); drawOn(pairs[1], W("s06", "right"), 0.8);
  const plate = svgEl(g, "path", { d: `M${L} ${CY} H${R}`, stroke: "#ffb547", "stroke-width": 16, "stroke-linecap": "round", opacity: 0 });
  const flow = svgEl(g, "path", { d: `M${L} ${TOP - 75} V${CY} H${R} V${BOT + 75}`, stroke: "#fff3d6", "stroke-width": 5, fill: "none", "stroke-dasharray": "10 18", opacity: 0 });
  const tP = W("s07", "press") + 0.1, tR = W("s07", "Let") + 0.1;
  dyn((t) => {
    const on = t >= tP && t < tR;
    cap.setAttribute("r", on ? 96 : 110);
    cap.setAttribute("fill", on ? "#5d6576" : "#4a5262");
    const pl = t >= W("s07", "plate") && t < tR;
    plate.setAttribute("opacity", pl ? 1 : 0);
    flow.setAttribute("opacity", pl && t >= W("s07", "connects") ? 0.9 : 0);
    flow.setAttribute("stroke-dashoffset", String(-((t * 80) % 28)));
  });
  for (const [x, txt, w] of [[L, "left pair", "left"], [R, "right pair", "right"]]) {
    const l = box(sBtn, x - 110, BOT + 100, 220, 40, "", `<div style="text-align:center;font:700 26px var(--ui);color:var(--teal)">${txt}</div>`);
    hidden(l); pop(l, W("s06", w) + 0.3);
  }
  const notes = [["4 legs, 1 simple switch", W("s05", "four")], ["each pair is always connected", W("s06", "always")],
    ["<b style='color:var(--amber)'>pressed:</b> left ↔ right connected", W("s07", "connects")], ["released: apart again", W("s07", "apart")]];
  notes.forEach(([txt, t], i) => {
    const n = box(sBtn, 1120, 330 + i * 110, 720, 80, "card", `<div style="padding:20px 28px;font:600 30px var(--display)">${txt}</div>`);
    hidden(n); pop(n, t);
  });
}

/* ======================================================================
 * BREADBOARDS: one is not enough (s08), two (s09), episode 3 circuit (s10),
 * the button (s11-s13); later the green LED on the upper one (s53-s55)
 * ==================================================================== */
const sBB = SC();
sceneIn(sBB, S1("s07") + 0.4);
sceneOut(sBB, S1("s13") + 0.4);
sceneIn(sBB, S1("s52") + 0.4);
sceneOut(sBB, S1("s55") + 0.5);
const Z = box(sBB, 0, 0, 1920, 1080, ""); // zoom container for the two breadboards
Z.style.transformOrigin = "0 0";
const bb = makeBB2(Z, 0, 0);
const VIEW = { all: [667, 760, 0.56], lower: [900, 1350, 0.95], button: [880, 1300, 1.25], upper: [900, 380, 0.95] };
{
  const band = box(sBB, 0, 0, 1920, 150, ""); // keeps the heading readable over the zoomed breadboards
  css(band, { zIndex: 29, background: "linear-gradient(rgba(11,18,32,.96) 55%, rgba(11,18,32,0))" });
  const hd = box(sBB, 0, 26, 1920, 80, "h2", ""); hd.style.textAlign = "center"; css(hd, { zIndex: 30 });
  panelAt(hd, [[0, ""], [T("s08"), "One breadboard is not enough"], [T("s09"), "Two breadboards, one board across both"], [W("s10", "rebuild"), "The circuit from episode 3"],
    [T("s11"), "Add the button"], [T("s13"), "Pressed: GPIO 22 → GND"], [T("s53") - 0.2, "A second LED, upper breadboard"]]);
  // s08: a single breadboard, the board covers one side completely
  const one = box(sBB, 0, 0, 1920, 1080, "");
  const bbS = makeBB(one, 0, 0);
  gsap.set(bbS.root, { x: 393, y: 220, scale: 0.85, transformOrigin: "0 0" });
  bbBoard(bbS, 30, 2, ["a", "i"]);
  gsap.set(one, { opacity: 0 });
  show(one, T("s08"), 0.4); hide(one, T("s09"), 0.5);
  const noTop = box(one, 1050, 150, 0, 0, "badge", "✕&nbsp; top side: no free holes");
  const okBot = box(one, 1050, 905, 0, 0, "badge", "✓&nbsp; bottom side: row j is free");
  css(noTop, { width: "auto", height: "auto", background: "var(--red)", color: "#fff" });
  css(okBot, { width: "auto", height: "auto", background: "var(--green)", color: "#05210f" });
  hidden(noTop); hidden(okBot); pop(noTop, W("s08", "one") + 0.1); pop(okBot, W("s08", "one") + 0.5);
  gsap.set(bbS.strips, { opacity: 1 });
  for (let c = 1; c <= 30; c++) bbS.colStrip[c].forEach((e) => e.setAttribute("opacity", 0));
  for (let c = 2; c <= 16; c++) TO(bbS.colStrip[c][1], W("s08", "one") + 0.5, 0.4, { opacity: 0.6 });
  const both = pillC(one, 980, "today: free holes on <b>both</b> sides", "font-size:30px");
  pop(both, W("s08", "both"));

  // s09: two breadboards
  gsap.set(Z, { opacity: 0 });
  zset(Z, 0, ...VIEW.all);
  SET(Z, T("s09") - 0.01, { scale: VIEW.all[2] * 0.92, x: 960 - VIEW.all[2] * 0.92 * VIEW.all[0], y: 540 - VIEW.all[2] * 0.92 * VIEW.all[1] });
  TO(Z, T("s09"), 0.8, { opacity: 1, scale: VIEW.all[2], x: 960 - VIEW.all[2] * VIEW.all[0], y: 540 - VIEW.all[2] * VIEW.all[1], ease: "power3.out" });
  SET(Z, T("s53") - 0.6, { opacity: 1 });
  bbBoard(bb, 30, 2, ["1j", "2a"]);
  gsap.set(bb.strips, { opacity: 1 });
  for (const k of [1, 2]) for (let c = 1; c <= 30; c++) bb.colStrip[k][c].forEach((e) => e.setAttribute("opacity", 0));
  const freeS = [];
  for (let c = 2; c <= 16; c++) freeS.push(bb.colStrip[1][c][1], bb.colStrip[2][c][0]);
  TO(freeS, W("s09", "free"), 0.4, { opacity: 0.6 }); TO(freeS, T("s10"), 0.4, { opacity: 0 });
  callout(Z, "top pins → upper breadboard", bb.L(17, "1j")[0] + 20, bb.L(17, "1j")[1] - 30, W("s09", "upper"), T("s10"), { style: { fontSize: "46px" } });
  callout(Z, "bottom pins → lower breadboard", bb.L(17, "2a")[0] + 20, bb.L(17, "2a")[1] - 10, W("s09", "lower"), T("s10"), { style: { fontSize: "46px" } });
  // USB status badge
  const usb = box(sBB, 60, 40, 0, 0, "badge", "");
  css(usb, { width: "auto", height: "auto", background: "rgba(11,18,32,.9)", border: "1px solid var(--line)", zIndex: 31 });
  const on = `<span style="color:var(--green)">● USB plugged in</span>`, off = `<span style="color:var(--red)">● USB unplugged</span>`;
  panelAt(usb, [[0, ""], [W("s10", "Unplug"), off], [T("s53") - 0.2, on], [W("s53", "Unplug"), off]], 0);

  // s10: rebuild the episode 3 circuit on the lower breadboard
  zcam(Z, W("s10", "Unplug") + 0.3, 1.2, ...VIEW.lower);
  const t10 = (w, n = 1) => W("s10", w, n);
  const pin23 = bb.L(16, "2a");
  callout(Z, "D23", pin23[0] - 30, pin23[1] + 26, t10("twentythree"), S1("s10"), { style: { fontSize: "26px" } });
  const resG = svgEl(bb.parts, "g", { opacity: 0 });
  resG.appendChild(bbResistor(bb, bb.L(16, "2e"), bb.L(20, "2g")));
  TO(resG, t10("resistor") - 0.2, 0.4, { opacity: 1 });
  const red = bbLED(bb, bb.L(20, "2h"), bb.L(21, "2h"), 1);
  gsap.set(red.g, { opacity: 0 }); TO(red.g, t10("red") - 0.1, 0.4, { opacity: 1 });
  callout(Z, "long leg", bb.L(20, "2h")[0] - 150, bb.L(20, "2h")[1] + 30, t10("red") + 0.3, t10("two") + 0.3, { style: { fontSize: "24px" } });
  bbWire(bb, bb.L(21, "2j"), bb.L(21, "2bm"), "#2b2f36", t10("LED", 2) - 0.1, -0.35);
  bbWire(bb, bb.L(3, "2e"), bb.L(3, "2bm"), "#2b2f36", t10("GND") - 0.1, 0.12);
  callout(Z, "GND", bb.L(3, "2b")[0] + 22, bb.L(3, "2b")[1] - 18, t10("GND"), S1("s10") + 0.3, { style: { fontSize: "26px" } });
  heroClip(stage, "C1", t10("rebuild") + 0.2, S1("s10") + 0.9, "Two breadboards, the board across both; rebuild the red LED circuit on the lower one.", { w: 620, h: 349, x: 1270, y: 140, sketch: "two breadboards" });

  // s11-s13: the button across the lower gap, columns 25 and 27
  zcam(Z, T("s11") - 0.2, 1.1, ...VIEW.button);
  const [x1, ye] = bb.L(25, "2e"), [x2, yf] = bb.L(27, "2f");
  const bg = svgEl(bb.parts, "g", { opacity: 0 });
  for (const [c, r] of [[25, "2e"], [27, "2e"], [25, "2f"], [27, "2f"]]) { const [lx, ly] = bb.L(c, r); svgEl(bg, "rect", { x: lx - 7, y: ly - 7, width: 14, height: 14, rx: 2, fill: "#9aa1aa" }); }
  const bcx = (x1 + x2) / 2, bcy = (ye + yf) / 2;
  svgEl(bg, "rect", { x: x1 - 22, y: ye - 4, width: x2 - x1 + 44, height: yf - ye + 8, rx: 10, fill: "#22262d", stroke: "#3a404b", "stroke-width": 2 });
  const bcap = svgEl(bg, "circle", { cx: bcx, cy: bcy, r: 34, fill: "#4a5262", stroke: "#11141a", "stroke-width": 3 });
  TO(bg, W("s11", "Press") + 0.1, 0.5, { opacity: 1 });
  for (const c of [25, 27]) {
    const st = bb.colStrip[2][c];
    TO(st, W("s11", "columns"), 0.4, { opacity: 0.6 }); TO(st, T("s12"), 0.4, { opacity: 0 });
  }
  callout(Z, "across the middle gap", x2 + 50, bcy - 20, W("s11", "gap"), T("s12"), { style: { fontSize: "24px" } });
  bbWire(bb, bb.L(15, "2c"), bb.L(25, "2c"), "#ffd34d", W("s12", "yellow"), -0.08);
  const p22 = bb.L(15, "2a");
  callout(Z, "D22", p22[0] - 32, p22[1] + 30, W("s12", "twentytwo"), S1("s12"), { style: { fontSize: "24px" } });
  bbWire(bb, bb.L(27, "2j"), bb.L(27, "2bm"), "#2b2f36", W("s12", "black"), -0.35);
  callout(Z, "− rail = GND", bb.L(27, "2bm")[0] - 230, bb.L(27, "2bm")[1] - 64, W("s12", "minus"), S1("s12"), { style: { fontSize: "24px" } });
  heroClip(stage, "C2", W("s11", "Press") - 0.2, S1("s12") + 0.3, "Button across the lower gap (columns 25-27), yellow wire D22 -> left side, black wire right side -> minus rail.",
    { w: 600, h: 338, x: 40, y: 160, sketch: "the button" });
  // s13: pressed -> GPIO 22 is connected to ground
  const pts = [bb.L(15, "2a"), bb.L(15, "2c"), bb.L(25, "2c"), bb.L(25, "2e"), [bcx, bcy], bb.L(27, "2f"), bb.L(27, "2j"), bb.L(27, "2bm"), bb.L(3, "2bm"), bb.L(3, "2e"), bb.L(3, "2a")];
  const path = svgEl(bb.over, "path", { d: "M" + pts.map((p) => p.join(" ")).join(" L"), fill: "none", stroke: "#19c3b4", "stroke-width": 7, "stroke-linejoin": "round", opacity: 0.95 });
  drawOn(path, W("s13", "connected"), 1.6);
  TO(path, S1("s13"), 0.3, { opacity: 0 });
  zcam(Z, W("s13", "connected") - 0.3, 1.2, 667, 1300, 0.82);
  const tPr = W("s13", "press");
  dyn((t) => { const pr = t >= tPr && t < S1("s13"); bcap.setAttribute("r", pr ? 28 : 34); bcap.setAttribute("fill", pr ? "#ffb547" : "#4a5262"); });
  // s53-s55: the green LED on the upper breadboard
  zset(Z, T("s53") - 0.6, ...VIEW.all);
  zcam(Z, W("s53", "upper"), 1.2, ...VIEW.upper);
  const t54 = (w) => W("s54", w), t55 = (w) => W("s55", w);
  bbWire(bb, bb.L(9, "1g"), bb.L(18, "1g"), "#3ddc84", t54("green"), -0.06);
  const p25 = bb.L(9, "1j");
  callout(Z, "D25", p25[0] - 32, p25[1] - 82, t54("twentyfive"), t54("resistor"), { style: { fontSize: "26px" } });
  const gr = svgEl(bb.parts, "g", { opacity: 0 });
  gr.appendChild(bbResistor(bb, bb.L(18, "1f"), bb.L(21, "1d")));
  TO(gr, t54("resistor"), 0.4, { opacity: 1 });
  for (const [c, w] of [[18, "eighteen"], [21, "twentyone"]]) {
    const st = bb.colStrip[1][c];
    TO(st, t54(w), 0.3, { opacity: 0.6 }); TO(st, S1("s54"), 0.3, { opacity: 0 });
  }
  const gled = bbLED(bb, bb.L(21, "1c"), bb.L(22, "1c"), -1, "green");
  gsap.set(gled.g, { opacity: 0 }); TO(gled.g, t55("long"), 0.4, { opacity: 1 });
  callout(Z, "long leg", bb.L(21, "1c")[0] - 150, bb.L(21, "1c")[1] + 20, t55("long"), t55("black"), { style: { fontSize: "24px" } });
  bbWire(bb, bb.L(22, "1a"), bb.L(22, "1tm"), "#2b2f36", t55("black"), 0.35);
  bbWire(bb, bb.L(3, "1f"), bb.L(3, "1tm"), "#2b2f36", t55("connects"), 0.12);
  callout(Z, "GND", bb.L(3, "1i")[0] + 22, bb.L(3, "1i")[1] - 10, t55("GND"), S1("s55") + 0.3, { style: { fontSize: "26px" } });
  heroClip(stage, "C6", T("s55") + 0.2, S1("s55") + 0.9, "Upper breadboard: green wire D25 -> 18, resistor 18 -> 21, green LED 21/22, black wire -> minus rail, black wire GND -> rail.",
    { w: 620, h: 349, x: 1270, y: 140, sketch: "the green LED" });
  for (const [t0, t1] of [[W("s12", "yellow"), S1("s13")], [W("s54", "green"), S1("s55")]]) {
    const n38 = box(sBB, 0, 1000, 1920, 50, "", `<div style="display:flex;justify-content:center"><span class="badge" style="position:static;background:rgba(11,18,32,.92);border:1px solid var(--line);color:#e8eef7;font-size:22px">38-pin board? Same pins, other columns: follow the labels (22, 23, 25, GND)</span></div>`);
    css(n38, { zIndex: 31 }); hidden(n38); pop(n38, t0 + 0.8); hide(n38, t1);
  }
}

/* ======================================================================
 * FLOATING PINS AND PULL-UPS (s14-s19)
 * ==================================================================== */
const sFloat = SC();
sceneIn(sFloat, S1("s13") + 0.4);
sceneOut(sFloat, S1("s19") + 0.4);
{
  const hd = box(sFloat, 0, 70, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s14"), "Not pressed: what does the pin read?"], [W("s16", "fix"), "The fix: a pull-up resistor"],
    [T("s18"), "Pull-up or pull-down"], [W("s19", "good"), "Built into the ESP32"]]);
  const sv = svgLayer(sFloat);
  const NX = 720, NY = 560, SX0 = 900, SX1 = 1060;
  const pinBox = box(sFloat, 180, NY - 60, 300, 120, "card", `<div style="height:120px;display:flex;align-items:center;justify-content:center;font:700 40px var(--mono);color:var(--teal)">GPIO 22</div>`);
  hidden(pinBox); show(pinBox, T("s14") - 0.2, 0.4);
  const g = svgEl(sv, "g", { opacity: 0 }); TO(g, T("s14") - 0.2, 0.4, { opacity: 1 });
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
  const closed = [[T("s14") - 0.3, W("s14", "Quick")], [W("s17", "pressed", 2), W("s17", "LOW") + 1.2]];
  // the pull-up: from the node up to 3.3 V
  const pu = svgEl(sv, "g", { opacity: 0 });
  const zz = [];
  for (let i = 0; i <= 6; i++) zz.push(`L${NX + (i === 0 || i === 6 ? 0 : i % 2 ? 26 : -26)} ${450 - i * 22}`);
  svgEl(pu, "path", Object.assign({ d: `M${NX} ${NY} V450 ${zz.join(" ")} V250 M${NX - 70} 250 H${NX + 70}` }, wire, { stroke: "#ffb547" }));
  svgEl(pu, "circle", { cx: NX, cy: NY, r: 10, fill: "#ffb547" });
  const v33 = svgEl(pu, "text", { x: NX, y: 228, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 30, fill: "#ffb547" });
  v33.textContent = "3.3 V";
  TO(pu, W("s16", "pullup") - 0.1, 0.5, { opacity: 1 });
  // current through the pull-up and the pressed button
  const cur = svgEl(sv, "path", { d: `M${NX} 250 V${NY} H${SX0} H${SX1} H1180 V700`, stroke: "#fff3d6", "stroke-width": 4, fill: "none", "stroke-dasharray": "8 16", opacity: 0 });
  const puLab = box(sFloat, NX + 50, 330, 360, 50, "", "");
  css(puLab, { font: "700 28px var(--ui)", color: "var(--amber)" });
  panelAt(puLab, [[0, ""], [W("s16", "pullup") + 0.3, "pull-up resistor"], [W("s19", "fortyfive"), "pull-up ≈ 45 kΩ"]]);
  const card = box(sFloat, 1350, 250, 440, 300, "card", "");
  hidden(card); show(card, T("s14"), 0.4);
  box(card, 0, 30, 440, 40, "", `<div style="text-align:center;font:600 26px var(--ui);color:var(--muted)">GPIO 22 reads</div>`);
  const val = box(card, 0, 90, 440, 150, "", "");
  const rnd = (k) => { let x = Math.sin(k * 12.9898) * 43758.5453; return x - Math.floor(x); };
  const tQ = W("s14", "Quick"), tFl = W("s15", "floating"), tPU = W("s16", "pullup") + 0.4;
  dyn((t) => {
    const c = inAny(t, closed);
    const a = c ? 0 : -0.5;
    lever.setAttribute("d", `M${SX0} ${NY} L${SX0 + Math.cos(a) * (SX1 - SX0)} ${NY + Math.sin(a) * (SX1 - SX0)}`);
    cur.setAttribute("opacity", c && t >= tPU ? 0.9 : 0);
    cur.setAttribute("stroke-dashoffset", String(-((t * 70) % 24)));
    let txt, col;
    if (c) { txt = "LOW"; col = "#6ea8ff"; }
    else if (t >= tPU) { txt = "HIGH"; col = "#19c3b4"; }
    else if (t >= tFl) { txt = rnd(Math.floor(t * 7)) < 0.5 ? "HIGH?" : "LOW?"; col = "#ffb547"; }
    else { txt = "?"; col = "#ffb547"; }
    const html = `<div style="text-align:center;font:800 96px var(--display);color:${col}">${txt}</div><div style="text-align:center;font:600 26px var(--ui);color:var(--muted)">${c ? "0 V" : t >= tPU ? "3.3 V" : t >= tQ ? "connected to nothing" : ""}</div>`;
    if (val.__v !== html) { val.innerHTML = html; val.__v = html; }
  });
  quizCard(sFloat, "The button is NOT pressed. What does GPIO 22 read?", tQ, T("s15"), "Nobody knows: the pin is floating", { t1: W("s16", "fix") - 0.2, y: 800, w: 1100 });
  const hand = box(sFloat, 600, 380, 120, 120, "", `<div style="font-size:90px">✋</div>`);
  hidden(hand); pop(hand, W("s15", "hand")); hide(hand, S1("s15"), 0.3);
  const tbl = pill(sFloat, 1360, 590, "not pressed = HIGH · pressed = LOW", "");
  pop(tbl, W("s17", "LOW") + 0.2); hide(tbl, T("s18"), 0.3);
  // s18: pull-down (small diagram)
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
  hidden(pd); pop(pd, W("s18", "ten")); hide(pd, T("s19"), 0.35);
  const pdr = pill(sFloat, 1330, 990, "pressed = HIGH", "font-size:24px");
  pop(pdr, W("s18", "Then")); hide(pdr, T("s19"), 0.3);
  const inside = box(sFloat, 150, 200, 670, 460, "", `<div style="position:absolute;left:18px;top:-18px;background:var(--bg);padding:0 10px;font:700 24px var(--ui);color:var(--teal)">inside the ESP32</div>`);
  css(inside, { border: "3px dashed var(--teal)", borderRadius: "22px" }); hidden(inside);
  pop(inside, W("s19", "built")); hide(inside, S1("s19"), 0.3);
  const ok = pillC(sFloat, 900, "✓ no extra part: INPUT_PULLUP switches it on", "font-size:32px");
  pop(ok, W("s19", "code"));
}

/* ======================================================================
 * THE CODE, LINE BY LINE (s20-s24): big code on the left, the circuit reacting on the right
 * ==================================================================== */
const sCode = SC();
sceneIn(sCode, S1("s19") + 0.4);
sceneOut(sCode, S1("s24") + 0.4);
{
  const hd = box(sCode, 80, 60, 1000, 60, "", `<span class="kicker">The code, line by line</span> &nbsp; <span class="pill" style="font:600 22px var(--mono);padding:6px 16px">button_led.ino</span>`);
  hidden(hd); show(hd, T("s20") - 0.2);
  const cA = bigCode(sCode, 80, 200, 1000, "const int BUTTON_PIN = 22;\nconst int LED_PIN = 23;", { size: 42 });
  const cB = bigCode(sCode, 80, 200, 1000, "void setup() {\n  pinMode(BUTTON_PIN, INPUT_PULLUP);\n  pinMode(LED_PIN, OUTPUT);\n  Serial.begin(115200);\n}", { size: 40 });
  const cC = bigCode(sCode, 80, 200, 1000, "void loop() {\n  int state = digitalRead(BUTTON_PIN);\n  Serial.println(state);\n  ...", { size: 40 });
  const cD = bigCode(sCode, 80, 200, 1000, "if (state == LOW) {\n  digitalWrite(LED_PIN, HIGH);\n} else {\n  digitalWrite(LED_PIN, LOW);\n}\ndelay(50);", { size: 42 });
  const slots = [[cA, T("s20"), T("s21")], [cB, T("s21"), T("s22")], [cC, T("s22"), T("s23")], [cD, T("s23"), S1("s24") + 1]];
  for (const [c, a, b] of slots) { show(c.c, a, 0.35); hide(c.c, b - 0.15, 0.25); }
  cA.hl([[0, -1], [W("s20", "button"), 0], [W("s20", "LED"), 1]]);
  cB.hl([[0, -1], [W("s21", "pin"), 1], [W("s21", "LED"), 2], [S1("s21"), -1]]);
  cC.hl([[0, -1], [W("s22", "digital"), 1], [W("s22", "print"), 2]]);
  cD.hl([[0, -1], [W("s23", "If"), 0], [W("s23", "write"), 1], [W("s24", "Otherwise"), 3], [W("s24", "delay"), 5]]);
  // explanations under the code (never on top of it)
  const notes = [
    [W("s21", "INPUT", 2), T("s22"), 470 + 40, "<b>INPUT</b> = we read the pin &nbsp;·&nbsp; <b>PULLUP</b> = built-in resistor on"],
    [W("s22", "HIGH"), T("s23"), 470, "digitalRead → <b>1</b> (HIGH) or <b>0</b> (LOW)"],
  ];
  for (const [a, b, y, html] of notes) {
    const n = box(sCode, 80, y, 1000, 70, "", `<span class="pill" style="font-size:28px">${html}</span>`);
    hidden(n); pop(n, a); hide(n, b - 0.1, 0.25);
  }
  // the circuit, live: button -> GPIO 22 -> ESP32 -> GPIO 23 -> resistor -> LED
  const panel = box(sCode, 1140, 170, 720, 780, "card", "");
  hidden(panel); show(panel, T("s20"), 0.4);
  const sv = svgLayer(sCode);
  const g = svgEl(sv, "g", { opacity: 0 }); TO(g, T("s20") + 0.1, 0.4, { opacity: 1 });
  const chipX = 1560, chipY = 260, chipW = 260, chipH = 600;
  svgEl(g, "rect", { x: chipX, y: chipY, width: chipW, height: chipH, rx: 18, fill: "#1b1f26", stroke: "#2b313b", "stroke-width": 3 });
  svgEl(g, "text", { x: chipX + chipW / 2, y: chipY + 50, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 30, fill: "#8fa1c0" }).textContent = "ESP32";
  const P22 = [chipX, 400], P23 = [chipX, 720];
  const pinTag = (p, label) => {
    svgEl(g, "rect", { x: p[0] - 14, y: p[1] - 14, width: 28, height: 28, rx: 4, fill: "#d4af37" });
    svgEl(g, "text", { x: p[0] + 26, y: p[1] + 10, "font-family": "Consolas, monospace", "font-weight": 700, "font-size": 28, fill: "#e8eef7" }).textContent = label;
  };
  pinTag(P22, "GPIO 22"); pinTag(P23, "GPIO 23");
  const wire = (d, col = "#cfd6e2") => svgEl(g, "path", { d, stroke: col, "stroke-width": 7, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" });
  // button between GPIO 22 and GND
  wire(`M${P22[0] - 14} 400 H1400`); wire("M1280 400 H1200 V480");
  for (const [w2, dy] of [[60, 0], [38, 12], [18, 24]]) wire(`M${1200 - w2 / 2} ${480 + dy} h${w2}`);
  svgEl(g, "text", { x: 1200, y: 540, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 22, fill: "#8fa1c0" }).textContent = "GND";
  const B = btnIcon(sCode, 1280, 340, 120, false);
  hidden(B.r); show(B.r, T("s20") + 0.1, 0.4);
  // GPIO 23 -> resistor -> LED -> GND
  const out = wire(`M${P23[0] - 14} 720 H1470`);
  const zz = []; for (let i = 0; i <= 6; i++) zz.push(`L${1470 - i * 16} ${720 + (i === 0 || i === 6 ? 0 : i % 2 ? -18 : 18)}`);
  wire(`M1470 720 ${zz.join(" ")} H1330`);
  svgEl(g, "text", { x: 1420, y: 690, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 22, fill: "#ffb547" }).textContent = "220 Ω";
  wire("M1230 720 H1200 V800");
  for (const [w2, dy] of [[60, 0], [38, 12], [18, 24]]) wire(`M${1200 - w2 / 2} ${800 + dy} h${w2}`);
  const L = ledIcon(sCode, 1245, 640, 70);
  hidden(L.r); show(L.r, T("s20") + 0.1, 0.4);
  const flow = svgEl(g, "path", { d: `M${P23[0] - 14} 720 H1330`, stroke: "#fff3d6", "stroke-width": 4, fill: "none", "stroke-dasharray": "8 16", opacity: 0 });
  // pull-up appears with INPUT_PULLUP (s21)
  const pu = svgEl(sv, "g", { opacity: 0 });
  const zz2 = []; for (let i = 0; i <= 6; i++) zz2.push(`L${1450 + (i === 0 || i === 6 ? 0 : i % 2 ? 16 : -16)} ${370 - i * 16}`);
  svgEl(pu, "path", { d: `M1450 400 V370 ${zz2.join(" ")} V250 M1410 250 H1490`, stroke: "#ffb547", "stroke-width": 6, fill: "none" });
  svgEl(pu, "text", { x: 1450, y: 236, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 24, fill: "#ffb547" }).textContent = "3.3 V (pull-up)";
  TO(pu, W("s21", "pull") - 0.1, 0.4, { opacity: 1 });
  // live labels
  const presses = [[W("s22", "LOW") - 0.1, W("s22", "LOW") + 1.3], [W("s23", "pressed"), W("s24", "Otherwise")]];
  B.press(presses);
  const tHigh = W("s23", "HIGH"), tLow = W("s24", "LOW");
  const v22 = box(sCode, 1290, 420, 260, 50, ""), v23 = box(sCode, 1300, 760, 240, 50, ""), st = box(sCode, chipX, 470, chipW, 120, "");
  css(v22, { font: "700 26px var(--mono)", textAlign: "center" }); css(v23, { font: "700 26px var(--mono)", textAlign: "center" });
  css(st, { font: "700 30px var(--mono)", textAlign: "center", lineHeight: "1.5" });
  for (const e of [v22, v23, st]) { hidden(e); show(e, T("s21") + 0.3, 0.3); }
  const ledOn = (t) => t >= tHigh && t < tLow;
  dyn((t) => {
    const pr = inAny(t, presses);
    const a = pr ? `<span style="color:#6ea8ff">0 · LOW</span>` : `<span style="color:var(--teal)">1 · HIGH</span>`;
    if (v22.__v !== a) { v22.innerHTML = a; v22.__v = a; }
    const o = t < W("s21", "OUTPUT") ? "" : ledOn(t) ? `<span style="color:var(--amber)">HIGH · 3.3 V</span>` : `<span style="color:var(--muted)">LOW · 0 V</span>`;
    if (v23.__v !== o) { v23.innerHTML = o; v23.__v = o; }
    const s = t < W("s22", "state") ? `<span style="color:var(--muted)">INPUT_PULLUP<br>OUTPUT</span>` : `state = <span style="color:${pr ? "#6ea8ff" : "var(--teal)"}">${pr ? 0 : 1}</span>`;
    if (st.__v !== s) { st.innerHTML = s; st.__v = s; }
    const on = ledOn(t);
    out.setAttribute("stroke", on ? "#ffb547" : "#cfd6e2");
    flow.setAttribute("opacity", on && t >= W("s23", "Three") ? 0.9 : 0);
    flow.setAttribute("stroke-dashoffset", String(-((t * 70) % 24)));
  });
  L.drive((t) => (ledOn(t) && t >= W("s23", "lights") - 0.1 ? 1 : 0));
  const why = pill(sCode, 80, 700, "pressed → state is LOW → write HIGH → LED on", "font-size:28px");
  pop(why, W("s23", "lights")); hide(why, W("s24", "Otherwise"), 0.25);
  const why2 = pill(sCode, 80, 700, "released → state is HIGH → write LOW → LED off", "font-size:28px");
  pop(why2, W("s24", "dark") - 0.2);
}

/* ======================================================================
 * ARDUINO IDE: save, upload, Serial Monitor (s25-s26), floating experiment (s27-s28)
 * ==================================================================== */
const DK = buildDesktop(stage);
const camera = DK.camera;
initCamera(camera);
initCursor(camera);
sceneIn(DK.desk, S1("s24") + 0.4);
sceneOut(DK.desk, S1("s28") + 0.5);
const ide = buildIDE(camera);
ide.boardText.textContent = "ESP32 Dev Module";
ide.statusBoard.textContent = "ESP32 Dev Module on COM3";
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
show(ide.w, S1("s24") + 0.4, 0.01);
const tFloatEdit = W("s27", "plain"), tFloatBack = W("s28", "back");
{
  const s25 = "s25", s26 = "s26", s27 = "s27", s28 = "s28";
  dyn((t) => {
    if (t < S1("s24")) return;
    const src = t >= tFloatEdit && t < tFloatBack ? FLOATING : SKETCH;
    if (ide.code.__v !== src) { renderCode(ide.code, src, src.length, false, 1); ide.code.__v = src; }
  });
  const keys = box(stage, 760, 900, 400, 70, "", `<span class="pill" style="font-size:30px;background:#1b2430;color:#fff">Ctrl + S</span>`);
  css(keys, { zIndex: 55, textAlign: "center" }); hidden(keys);
  show(keys, W(s25, "Save") - 0.1, 0.2); hide(keys, W(s25, "click"), 0.2);
  const tSave = W(s25, "Save") + 0.3;
  textAt(ide.tab, [[0, "sketch_oct25a.ino"], [tSave, "button_led.ino"]]);
  textAt(ide.title, [[0, "sketch_oct25a | Arduino IDE 2.3.10"], [tSave, "button_led | Arduino IDE 2.3.10"]]);
  const uploads = [[W(s25, "Upload"), W(s25, "Serial") - 0.2], [W(s27, "upload") + 0.1, W(s28, "Now") - 0.1]];
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
  clickAt(IDE.monitor.x, IDE.monitor.y, W(s25, "Serial"), 0.9);
  const tOpen = W(s25, "Serial") + 0.1;
  const o1 = $(".o1", ide.btabs), o2 = $(".o2", ide.btabs);
  styleAt(o2, "display", [[0, "none"], [tOpen, "flex"]]);
  dyn((t) => { o1.className = t >= tOpen ? "o1" : "on o1"; o2.className = t >= tOpen ? "on o2" : "o2"; });
  styleAt(ide.out, "display", [[0, "block"], [tOpen, "none"]]);
  styleAt(ide.serial, "display", [[0, "none"], [tOpen, "block"]]);
  cam(tOpen + 0.3, 1.0, 560, 900, 1.9);
  // s27: back to the code for the floating experiment, then the monitor again
  cam(W(s27, "Change") - 0.2, 0.9, 520, 300, 2.0);
  ring(camera, cx(2) - 4, lineY(7) - 1, cx(36) - cx(2) + 8, 24, W(s27, "Change"), W(s27, "upload"));
  cam(W(s27, "upload") + 0.2, 0.8, 960, 540, 1);
  cam(T(s28) - 0.1, 0.9, 560, 900, 1.9);
  const pressed = [[W(s26, "Press"), W(s26, "Let")]];
  const tFloatRun = uploads[1][1] + 0.3;
  const rnd = (k2) => { let x = Math.sin(k2 * 78.233) * 43758.5453; return x - Math.floor(x); };
  dyn((t) => {
    if (t < tOpen) return;
    const kk = Math.floor((t - tOpen) / 0.08);
    const lines = [];
    for (let i = Math.max(0, kk - 6); i <= kk; i++) {
      const ti = tOpen + i * 0.08;
      let v;
      if (ti >= uploads[1][0] && ti < tFloatRun) v = null;
      else if (ti >= tFloatRun && ti < tFloatBack) v = rnd(i) < (ti >= W(s28, "Touch") ? 0.5 : 0.25) ? 0 : 1;
      else v = inAny(ti, pressed) ? 0 : 1;
      if (v !== null) lines.push(v);
    }
    const html = `<div style="display:flex;gap:12px;align-items:center;margin:-2px 0 8px;font-family:var(--ui)"><div class="ide-in" style="flex:1;color:#888">Message (Enter to send message to 'ESP32 Dev Module' on 'COM3')</div>
      <div class="ide-in" style="width:110px">New Line ▾</div><div class="ide-in" style="width:130px;${t >= W(s25, "115200") - 0.3 && t < W(s25, "115200") + 1.5 ? "border-color:#ffb547" : ""}">115200 baud ▾</div></div>` +
      lines.map((l) => `<div>${l}</div>`).join("");
    if (ide.serial.__v !== html) { ide.serial.innerHTML = html; ide.serial.__v = html; }
  });
  callout(camera, "1 = HIGH (not pressed)", 220, IDE.outTop + 70, W(s26, "one"), W(s26, "Press"), { style: { zIndex: 60 } });
  callout(camera, "0 = LOW (pressed)", 220, IDE.outTop + 70, W(s26, "zero"), S1(s26) + 0.3);
  heroClip(stage, "C3", W(s26, "lights") - 0.3, T(s27) - 0.25, "button_led: holding the button lights the LED; let go: dark.", { full: true });
  const fl = box(stage, 1240, 120, 620, 80, "", `<span class="pill" style="font-size:30px;background:rgba(255,181,71,.18);color:var(--amber)">floating: the numbers jump around</span>`);
  css(fl, { zIndex: 55 }); hidden(fl); pop(fl, W(s28, "jump")); hide(fl, tFloatBack, 0.3);
  const calm = box(stage, 1240, 120, 620, 80, "", `<span class="pill" style="font-size:30px">INPUT_PULLUP again: calm</span>`);
  css(calm, { zIndex: 55 }); hidden(calm); pop(calm, tFloatBack + 0.2); hide(calm, S1(s28) + 0.4, 0.3);
}

/* ======================================================================
 * TOGGLE (s29-s36): 1. catch the edge, 2. flip a bool with if/else, 3. the short forms
 * ==================================================================== */
const sTog = SC();
sceneIn(sTog, S1("s28") + 0.5);
sceneOut(sTog, S1("s36") + 0.4);
{
  const hd = box(sTog, 0, 50, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s29"), "Press once: on · press again: off"], [T("s30"), "1 · Catch the moment of the press"],
    [T("s34"), "2 · Flip the LED"], [T("s35"), "3 · The short way to write it"]]);
  // s29: what we want
  const B0 = btnIcon(sTog, 700, 330, 170), L0 = ledIcon(sTog, 1060, 290, 130);
  const pr0 = [[W("s29", "once"), W("s29", "once") + 0.35], [W("s29", "again"), W("s29", "again") + 0.35]];
  B0.press(pr0); L0.drive((t) => (t >= pr0[0][0] && t < pr0[1][0] ? 1 : 0));
  for (const e of [B0.r, B0.lab, L0.r]) { hidden(e); show(e, T("s29"), 0.4); hide(e, T("s30") - 0.1, 0.3); }
  const want = pillC(sTog, 720, "not “is the button down?” but “did it <b>just</b> go down?”", "font-size:32px");
  pop(want, W("s29", "moment")); hide(want, T("s30") - 0.1, 0.3);
  // s30-s33: readings on a timeline
  const vals = ["HIGH", "HIGH", "HIGH", "LOW", "LOW", "LOW", "LOW", "HIGH"];
  const CW = 170, X0 = 280, Y0 = 200;
  const tl1 = box(sTog, 0, 0, 1920, 1080, ""); hidden(tl1); show(tl1, T("s30"), 0.3); hide(tl1, T("s34") - 0.1, 0.3);
  const cellT = [W("s30", "HIGH", 1), W("s30", "HIGH", 2), W("s30", "HIGH", 3), W("s30", "LOW"), W("s30", "LOW") + 0.4, W("s30", "LOW") + 0.8, W("s30", "LOW") + 1.2, W("s30", "LOW") + 1.6];
  const cells = vals.map((v, i) => {
    const c = box(tl1, X0 + i * CW, Y0, CW - 14, 90, "card", `<div style="height:90px;display:flex;align-items:center;justify-content:center;font:800 34px var(--mono);color:${v === "HIGH" ? "var(--teal)" : "#6ea8ff"}">${v}</div>`);
    hidden(c); pop(c, cellT[i]);
    return c;
  });
  const timeLab = box(tl1, X0, Y0 + 100, 8 * CW, 30, "", `<div style="font:600 22px var(--ui);color:var(--muted)">readings, one per loop → time</div>`);
  hidden(timeLab); show(timeLab, cellT[0] + 0.3);
  const edgeX = X0 + 3 * CW - 7;
  const edge = box(tl1, edgeX - 6, Y0 - 30, 12, 150, "");
  css(edge, { background: "var(--red)", borderRadius: "6px", boxShadow: "0 0 18px var(--red)" }); hidden(edge); pop(edge, W("s30", "moment"));
  const eLab = box(tl1, edgeX - 200, Y0 - 82, 400, 44, "", `<div style="text-align:center;font:800 30px var(--ui);color:var(--red)">the edge = the press</div>`);
  hidden(eLab); pop(eLab, W("s30", "edge") - 0.2);
  // s31: lastState vs state, a pointer walking along the readings
  const code1 = bigCode(sTog, 120, 400, 1050, "int state = digitalRead(BUTTON_PIN);\nif (state != lastState) {\n  if (state == LOW) {\n    // a new press!\n  }\n}\nlastState = state;", { size: 34 });
  show(code1.c, T("s31"), 0.4); hide(code1.c, T("s34") - 0.1, 0.3);
  const steps = [[W("s31", "remember"), 1], [W("s31", "new"), 2], [W("s31", "different"), 3], [T("s33"), 4], [W("s33", "LOW") + 0.4, 5], [W("s33", "changes"), 6]];
  const ptr = box(tl1, 0, Y0 - 14, CW * 2 - 14, 118, "");
  css(ptr, { border: "4px solid var(--amber)", borderRadius: "16px", opacity: 0 });
  const pl = box(tl1, 0, Y0 + 128, CW * 2, 60, "", "");
  css(pl, { font: "700 24px var(--mono)", display: "flex", justifyContent: "space-between", opacity: 0 });
  pl.innerHTML = `<span style="color:var(--muted)">lastState</span><span style="color:var(--amber);padding-right:30px">state</span>`;
  dyn((t) => {
    let i = -1;
    for (const [ts, k] of steps) if (t >= ts) i = k;
    const vis = i >= 1 && t < T("s34") ? 1 : 0;
    ptr.style.opacity = vis; pl.style.opacity = vis;
    if (i >= 1) { const x = X0 + (i - 1) * CW - 7; ptr.style.left = x + "px"; pl.style.left = x + 10 + "px"; }
  });
  const vwrap = box(sTog, 1230, 420, 620, 220, "card", "");
  hidden(vwrap); show(vwrap, W("s31", "remember") + 0.2, 0.3); hide(vwrap, T("s34") - 0.1, 0.3);
  const verdict = box(vwrap, 0, 0, 620, 220, "");
  panelAt(verdict, [[0, ""],
    [W("s31", "remember") + 0.2, `<div style="padding:30px 36px;font:700 34px var(--display)">HIGH → HIGH<div style="font:600 28px var(--ui);color:var(--muted);margin-top:10px">same: nothing happens</div></div>`],
    [W("s31", "different"), `<div style="padding:30px 36px;font:700 34px var(--display)">HIGH → LOW<div style="font:700 30px var(--ui);color:var(--red);margin-top:10px">changed, and LOW: a new press!</div></div>`],
    [T("s33"), `<div style="padding:30px 36px;font:700 34px var(--display)">LOW → LOW<div style="font:600 28px var(--ui);color:var(--muted);margin-top:10px">same: no new edge</div></div>`]], 8);
  code1.hl([[0, -1], [W("s31", "different"), 1], [W("s31", "LOW"), 2], [W("s31", "press"), 3], [T("s32"), -1], [T("s33"), 1], [S1("s33"), -1]]);
  quizCard(sTog, "You hold the button down. Does the LED keep flipping?", W("s32", "Quick"), T("s33"), "No: state and lastState both stay LOW, so there's no new edge", { y: 820, w: 1500, t1: T("s34") - 0.1 });
  // s34: if / else with a bool
  const code2 = bigCode(sTog, 120, 200, 980, "if (ledOn) {\n  ledOn = false;\n  digitalWrite(LED_PIN, LOW);\n} else {\n  ledOn = true;\n  digitalWrite(LED_PIN, HIGH);\n}", { size: 40 });
  show(code2.c, T("s34") + 0.2, 0.4); hide(code2.c, T("s35") + 0.6, 0.4);
  const tA = W("s34", "If"), tF = W("s34", "false", 2), tO = W("s34", "Otherwise"), tTr = W("s34", "true", 3), tM = W("s34", "match");
  code2.hl([[0, -1], [tA, 0], [tF, 1], [tF + 0.6, 2], [tO, 3], [tTr, 4], [tTr + 0.6, 5], [tM, -1]]);
  const flips = [[0, true], [tF, false], [tTr, true]];
  const lv = valBox(sTog, 1250, 260, 520, [[0, `bool ledOn = ${T_("true")}`], [tF, `bool ledOn = ${F_("false")}`], [tTr, `bool ledOn = ${T_("true")}`]], 36);
  show(lv, T("s34") + 0.3, 0.4); hide(lv, T("s35") + 0.6, 0.4);
  const B2 = btnIcon(sTog, 1290, 470, 150), L2 = ledIcon(sTog, 1590, 430, 120);
  B2.press([[tA - 0.1, tA + 0.3], [tO - 0.1, tO + 0.3]]);
  L2.drive((t) => (stateAt(flips, t) ? 1 : 0));
  for (const e of [B2.r, B2.lab, L2.r]) { hidden(e); show(e, T("s34") + 0.3, 0.4); hide(e, T("s35") + 0.6, 0.4); }
  const easy = pill(sTog, 120, 760, "✓ works, and easy to read", "");
  pop(easy, W("s35", "works")); hide(easy, T("s35") + 0.6, 0.3);
  // s35-s36: the short forms
  const code3 = bigCode(sTog, 220, 300, 1480, "ledOn = !ledOn;", { size: 56 });
  const code4 = bigCode(sTog, 220, 300, 1480, "ledOn = !ledOn;\ndigitalWrite(LED_PIN, ledOn ? HIGH : LOW);", { size: 56 });
  show(code3.c, T("s35") + 0.9, 0.4); SET(code3.c, T("s36"), { opacity: 0 }); SET(code4.c, T("s36"), { opacity: 1 });
  code3.hl([[0, -1], [W("s35", "not", 2), 0]]);
  code4.hl([[0, -1], [W("s36", "question"), 1], [W("s36", "Same"), -1]]);
  const nb = [["! means “not”", W("s35", "not")], ["!true → false &nbsp;·&nbsp; !false → true", W("s35", "flips")]];
  nb.forEach(([html, t], i) => { const c = pill(sTog, 260 + i * 520, 520, html, "font-size:30px"); pop(c, t); hide(c, T("s36") - 0.1, 0.3); });
  const qb = [["ledOn ? HIGH : LOW", W("s36", "picks")], [`${T_("true")} → HIGH`, W("s36", "HIGH")], [`${F_("false")} → LOW`, W("s36", "LOW")]];
  qb.forEach(([html, t], i) => { const c = pill(sTog, 260 + i * 470, 620, html, "font-size:30px;font-family:var(--mono)"); pop(c, t); });
  const same = pillC(sTog, 800, "same result: 6 lines → 2 lines", "font-size:34px;background:rgba(74,222,128,.16);color:var(--green)");
  pop(same, W("s36", "Same"));
}

/* ======================================================================
 * BOUNCE AND DEBOUNCE (s37-s40)
 * ==================================================================== */
const sBo = SC();
sceneIn(sBo, S1("s36") + 0.4);
sceneOut(sBo, S1("s40") + 0.4);
{
  const hd = head(sBo, "Count the presses", 60); show(hd, T("s37"));
  const cA = bigCode(sBo, 90, 190, 960, "if (state != lastState) {\n  if (state == LOW) {\n    presses++;\n    Serial.println(presses);\n  }\n}", { size: 36 });
  const cB = bigCode(sBo, 90, 190, 960, "if (state != lastState) {\n  if (state == LOW) {\n    presses++;\n    Serial.println(presses);\n  }\n  delay(50);   // debounce\n}", { size: 36 });
  show(cA.c, T("s37"), 0.4); SET(cA.c, W("s39", "wait"), { opacity: 0 }); SET(cB.c, W("s39", "wait"), { opacity: 1 });
  cA.hl([[0, -1], [W("s37", "count"), 2], [W("s37", "print"), 3], [S1("s37"), -1]]);
  cB.hl([[0, -1], [W("s39", "wait"), 5]]);
  const presses = [[W("s37", "Press") + 0.3, W("s37", "Press") + 0.65], [W("s40", "every"), W("s40", "every") + 0.35], [W("s40", "flips"), W("s40", "flips") + 0.35]];
  const B = btnIcon(sBo, 1180, 190, 150); B.press(presses);
  hidden(B.r); hidden(B.lab); show([B.r, B.lab], T("s37"), 0.4);
  const ctr = box(sBo, 1380, 220, 480, 90, "", "");
  css(ctr, { font: "700 44px var(--mono)" }); hidden(ctr); show(ctr, T("s37"), 0.3); hide(ctr, T("s38") - 0.1, 0.3);
  const tJ = W("s37", "Press") + 0.3;
  textAt(ctr, [[0, "presses: 0"], [tJ, "presses: 3 <span style='color:var(--red);font-size:30px'>?!</span>"], [W("s37", "two"), "presses: 5 <span style='color:var(--red);font-size:30px'>+2 ?!</span>"],
    [W("s37", "three"), "presses: 8 <span style='color:var(--red);font-size:30px'>+3 ?!</span>"]]);
  const ctr2 = box(sBo, 1380, 220, 480, 90, "", "");
  css(ctr2, { font: "700 44px var(--mono)" }); hidden(ctr2); show(ctr2, T("s40"), 0.3);
  textAt(ctr2, [[0, "presses: 0"], [W("s40", "every"), "presses: 1"], [W("s40", "flips"), "presses: 2"]]);
  // s38-s39: the bounce, magnified
  const X0 = 1100, X1 = 1820, YH = 560, YL = 720;
  const zoomBox = box(sBo, X0 - 30, YH - 110, X1 - X0 + 60, YL - YH + 260, "card", `<div class="kicker" style="padding:18px 24px;font-size:18px">the pin, magnified: one press</div>`);
  const sv = svgLayer(sBo);
  hidden(zoomBox); show(zoomBox, T("s38") - 0.1, 0.3); hide(zoomBox, T("s40") - 0.1, 0.3);
  const bg = svgEl(sv, "g", { opacity: 0 });
  TO(bg, T("s38"), 0.4, { opacity: 1 }); TO(bg, T("s40") - 0.1, 0.3, { opacity: 0 });
  let d = `M${X0} ${YH} H1300`;
  const bx = [1300, 1322, 1340, 1362, 1376, 1396, 1406, 1424, 1432];
  bx.forEach((x, i) => { d += ` H${x} V${i % 2 ? YH : YL}`; });
  d += ` H${X1}`;
  const wave = svgEl(bg, "path", { d, stroke: "#ffb547", "stroke-width": 6, fill: "none" });
  drawOn(wave, T("s38") + 0.2, 1.4);
  svgEl(bg, "text", { x: X0 + 10, y: YH - 16, "font-family": "Segoe UI", "font-weight": 700, "font-size": 22, fill: "#19c3b4" }).textContent = "HIGH";
  svgEl(bg, "text", { x: X1 - 70, y: YL + 36, "font-family": "Segoe UI", "font-weight": 700, "font-size": 22, fill: "#6ea8ff" }).textContent = "LOW";
  const few = svgEl(bg, "text", { x: 1370, y: YH - 24, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 24, fill: "#8fa1c0", opacity: 0 });
  few.textContent = "a few ms"; TO(few, W("s38", "few"), 0.3, { opacity: 1 });
  const fiveT = svgEl(bg, "text", { x: 1460, y: YL + 70, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 30, fill: "#ff5d6c", opacity: 0 });
  fiveT.textContent = "1 press → 5 edges";
  TO(fiveT, W("s38", "five") - 0.2, 0.3, { opacity: 1 }); TO(fiveT, W("s39", "wait"), 0.3, { opacity: 0 });
  const win = svgEl(bg, "rect", { x: 1300, y: YH - 40, width: 360, height: YL - YH + 80, rx: 10, fill: "rgba(25,195,180,.18)", stroke: "#19c3b4", "stroke-width": 3, opacity: 0 });
  TO(win, W("s39", "wait"), 0.4, { opacity: 1 });
  const winT = svgEl(bg, "text", { x: 1480, y: YL + 70, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 30, fill: "#19c3b4", opacity: 0 });
  winT.textContent = "wait 50 ms: bounce ignored";
  TO(winT, W("s39", "fifty"), 0.3, { opacity: 1 });
  const ok = pill(sBo, 1180, 560, "✓ one press = one count = one flip", "");
  pop(ok, W("s40", "exactly")); hide(ok, W("s40", "sketch"), 0.3);
  heroClip(stage, "C4", W("s40", "This") - 0.1, T("s41") - 0.3 - FC, "button_toggle: press, LED on; press again, LED off.", { full: true });
  fullAfter("button_toggle", "s41");
}

/* ======================================================================
 * PART 2: WHY delay() GETS IN THE WAY (s41-s44)
 * ==================================================================== */
const sBlock = SC();
sceneIn(sBlock, S1("s40") + 0.4);
sceneOut(sBlock, S1("s44") + 0.4);
{
  const hd = box(sBlock, 0, 60, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s41"), "Part 2: blink + button"], [W("s43", "freezes"), "delay() freezes everything"]]);
  const src = (n) => `if (digitalRead(BUTTON_PIN) == LOW) {\n  blinking = !blinking;\n}\ndigitalWrite(LED_PIN, HIGH);\ndelay(${n});\ndigitalWrite(LED_PIN, LOW);\ndelay(${n});`;
  const c1 = bigCode(sBlock, 90, 180, 900, src(500), { size: 36 }), c2 = bigCode(sBlock, 90, 180, 900, src(100), { size: 36 });
  show(c1.c, W("s42", "obvious"), 0.4); SET(c1.c, W("s44", "Shorter"), { opacity: 0 }); SET(c2.c, W("s44", "Shorter"), { opacity: 1 });
  const tB = T("s41") + 0.5;
  // the highlight follows the running loop: button check (instant), then the two delays
  const loopHl = (period, t0, t1) => {
    const list = [[0, -1]];
    for (let t = t0; t < t1; t += period * 2) list.push([t, 0, "rgba(74,222,128,.25)"], [t + 0.06, 4, "rgba(255,93,108,.28)"], [t + period, 6, "rgba(255,93,108,.28)"]);
    return list;
  };
  c1.hl(loopHl(0.5, W("s43", "Delay"), W("s44", "Shorter")));
  c2.hl(loopHl(0.1, W("s44", "Shorter"), S1("s44") + 1));
  const L = ledIcon(sBlock, 1730, 150, 90);
  hidden(L.r); show(L.r, T("s41"), 0.4);
  L.drive((t) => (t < W("s44", "Shorter") ? blink(t, tB, 0.5, 0.5) : blink(t, tB, 0.1, 0.1)));
  const sv = svgLayer(sBlock);
  const X0 = 1040, X1 = 1820;
  const mk = (y, period, t0, t1) => {
    const g = svgEl(sv, "g", { opacity: 0 });
    TO(g, t0, 0.4, { opacity: 1 }); if (t1) TO(g, t1, 0.3, { opacity: 0 });
    const px = (X1 - X0) / 3;
    for (let x = X0; x < X1 - 1; x += px * period * 2) {
      svgEl(g, "rect", { x, y, width: 8, height: 70, fill: "#4ade80" });
      svgEl(g, "rect", { x: x + 10, y, width: Math.min(px * period * 2 - 12, X1 - x - 10), height: 70, rx: 6, fill: "rgba(255,93,108,.55)" });
    }
    return g;
  };
  mk(470, 0.5, W("s42", "Quick"), W("s44", "Shorter"));
  mk(470, 0.1, W("s44", "Shorter"));
  const k1 = box(sBlock, X0, 560, 800, 40, "", `<div style="font:600 24px var(--ui)"><span style="color:#4ade80">▮ looks at the button</span> &nbsp; <span style="color:#ff8a94">▮ waiting in delay()</span></div>`);
  hidden(k1); show(k1, W("s42", "Quick"), 0.4);
  const arrow = box(sBlock, X0 + 300, 340, 300, 120, "", `<div style="text-align:center;font:800 30px var(--ui);color:var(--amber)">a short press<div style="font-size:50px;line-height:50px">↓</div></div>`);
  hidden(arrow); pop(arrow, W("s42", "press")); hide(arrow, T("s43"), 0.2);
  const miss = box(sBlock, X0 + 300, 340, 300, 120, "", `<div style="text-align:center;font:800 30px var(--ui);color:var(--red)">press ✕ missed<div style="font-size:50px;line-height:50px">↓</div></div>`);
  hidden(miss); pop(miss, W("s43", "missed")); hide(miss, W("s44", "Shorter"), 0.3);
  const miss2 = box(sBlock, X0 + 470, 340, 300, 120, "", `<div style="text-align:center;font:800 30px var(--ui);color:var(--red)">still slips through<div style="font-size:50px;line-height:50px">↓</div></div>`);
  hidden(miss2); pop(miss2, W("s44", "slip"));
  const goal = pillC(sBlock, 600, "the LED blinks · the button switches the blinking on and off", "font-size:32px");
  pop(goal, W("s41", "blinking")); hide(goal, W("s42", "obvious"), 0.3);
  quizCard(sBlock, "You press during a delay(). Will the ESP32 notice?", W("s42", "Quick"), T("s43"), "No: delay() freezes everything, the press is missed", { y: 760, w: 1500, t1: T("s44") - 0.1 });
  const real = pillC(sBlock, 900, "the real fix: a different way of thinking", "font-size:32px");
  pop(real, W("s44", "real"));
}

/* ======================================================================
 * millis(): CHECK THE CLOCK, DON'T WAIT (s45-s52)
 * ==================================================================== */
const sMil = SC();
sceneIn(sMil, S1("s44") + 0.4);
sceneOut(sMil, S1("s52") + 0.4);
{
  const hd = box(sMil, 0, 50, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s45"), "Never wait: look at the clock"], [T("s46"), "One question, every loop"], [T("s47"), "On a timeline"],
    [T("s49"), "unsigned long, and always subtract"], [T("s50"), "The button: same trick"], [T("s51"), "A loop that never waits"]]);
  // s45: the clock counts by itself
  const t0 = T("s45") - 0.6;
  const clock = box(sMil, 0, 300, 1920, 150, "", "");
  hidden(clock); show(clock, T("s45"), 0.4); hide(clock, T("s46") - 0.1, 0.3);
  dyn((t) => {
    if (t < t0 || t > T("s46") + 1) return;
    const ms = Math.max(0, Math.round((t - t0) * 1000) + 3000);
    const html = `<div style="text-align:center;font:700 110px var(--mono)">${fn("millis")}() = <span style="color:var(--teal)">${ms.toLocaleString("en-US")}</span></div>`;
    if (clock.__v !== html) { clock.innerHTML = html; clock.__v = html; }
  });
  const sub = pillC(sMil, 490, "milliseconds since the board started", "background:transparent;color:var(--muted)");
  pop(sub, W("s45", "milliseconds")); hide(sub, T("s46") - 0.1, 0.3);
  const self = pillC(sMil, 600, "it keeps counting by itself, while your code does other things", "font-size:30px");
  pop(self, W("s45", "itself")); hide(self, T("s46") - 0.1, 0.3);
  // s46-s48: the pattern + the timeline
  const code = bigCode(sMil, 80, 160, 1000, "unsigned long now = millis();\nif (now - lastBlink >= 500) {\n  lastBlink = now;\n  // flip the LED\n}", { size: 38 });
  show(code.c, T("s46"), 0.4); hide(code.c, T("s49") - 0.1, 0.3);
  // simulated clock value "now" during the timeline
  const tN1 = W("s47", "Now"), tN2 = W("s48", "fourteen"), tN3 = W("s48", "later"), tSet = W("s48", "set"), tNew = W("s48", "new");
  const nowV = (t) => {
    if (t < tN1) return 1000;
    if (t < tN1 + 0.7) return 1000 + Math.round((t - tN1) / 0.7 * 200);
    if (t < tN2) return 1200;
    if (t < tN2 + 0.9) return 1200 + Math.round((t - tN2) / 0.9 * 299);
    if (t < tN3) return 1499;
    if (t < tNew) return 1500;
    return Math.min(1700, 1500 + Math.round((t - tNew) / 1.2 * 200));
  };
  const lastV = (t) => (t < tSet ? 1000 : 1500);
  code.hl([[0, -1], [W("s46", "save"), 2], [W("s46", "now"), 0], [W("s46", "question"), 1], [S1("s46"), -1],
    [W("s47", "Twelve", 2), 1, "rgba(255,93,108,.25)"], [W("s47", "moves"), -1], [W("s48", "still"), 1, "rgba(255,93,108,.25)"],
    [tN3, 1, "rgba(74,222,128,.28)"], [tSet, 2, "rgba(74,222,128,.28)"], [tNew + 0.6, -1]]);
  const vars = box(sMil, 1150, 170, 700, 330, "card", "");
  hidden(vars); show(vars, W("s46", "save"), 0.4); hide(vars, T("s49") - 0.1, 0.3);
  dyn((t) => {
    if (t < T("s46") || t > T("s49")) return;
    const n = nowV(t), l = lastV(t), e = n - l, ok = e >= 500;
    const html = `<div style="padding:28px 36px;font:700 38px/1.6 var(--mono)">
      <div>now &nbsp; &nbsp; &nbsp;= <span style="color:var(--teal)">${t < W("s46", "now") ? "…" : n}</span></div>
      <div>lastBlink = <span style="color:var(--amber)">${l}</span></div>
      <div style="border-top:2px solid var(--line);margin-top:8px;padding-top:8px">now − lastBlink = <span style="color:${ok ? "var(--green)" : "var(--red)"}">${t < tN1 ? "…" : e}</span></div>
      <div style="font:700 30px var(--ui);color:${ok ? "var(--green)" : "var(--muted)"}">${t < tN1 ? "≥ 500 ?" : ok ? "≥ 500 → flip the LED!" : "&lt; 500 → not yet, move on"}</div></div>`;
    if (vars.__v !== html) { vars.innerHTML = html; vars.__v = html; }
  });
  // the timeline: 900 ... 2100 ms
  const AX0 = 150, AX1 = 1770, A0 = 900, A1 = 2100, AY = 800;
  const X = (ms) => AX0 + (ms - A0) / (A1 - A0) * (AX1 - AX0);
  const tlg = box(sMil, 0, 0, 1920, 1080, ""); hidden(tlg); show(tlg, T("s47"), 0.4); hide(tlg, T("s49") - 0.1, 0.3);
  const sv = svgLayer(tlg);
  svgEl(sv, "path", { d: `M${AX0} ${AY} H${AX1}`, stroke: "#8fa1c0", "stroke-width": 4 });
  for (let ms = 1000; ms <= 2000; ms += 100) {
    svgEl(sv, "path", { d: `M${X(ms)} ${AY - 10} V${AY + 10}`, stroke: "#8fa1c0", "stroke-width": ms % 500 ? 2 : 4 });
    if (ms % 500 === 0) svgEl(sv, "text", { x: X(ms), y: AY + 46, "text-anchor": "middle", "font-family": "Consolas, monospace", "font-weight": 700, "font-size": 26, fill: "#8fa1c0" }).textContent = ms;
  }
  svgEl(sv, "text", { x: AX1, y: AY + 46, "text-anchor": "end", "font-family": "Segoe UI", "font-weight": 600, "font-size": 22, fill: "#8fa1c0" }).textContent = "ms →";
  const elapsed = svgEl(sv, "rect", { x: X(1000), y: AY - 64, width: 0, height: 36, rx: 8, fill: "rgba(255,181,71,.6)" });
  const thr = svgEl(sv, "path", { d: "", stroke: "#ff5d6c", "stroke-width": 4, "stroke-dasharray": "10 8" });
  const thrL = svgEl(sv, "text", { "text-anchor": "middle", "font-family": "Consolas, monospace", "font-weight": 700, "font-size": 24, fill: "#ff5d6c" });
  const flag = svgEl(sv, "g", {});
  svgEl(flag, "path", { d: `M0 ${AY} V${AY - 150}`, stroke: "#ffb547", "stroke-width": 5 });
  svgEl(flag, "path", { d: `M0 ${AY - 150} h120 v40 h-120 z`, fill: "#ffb547" });
  svgEl(flag, "text", { x: 60, y: AY - 122, "text-anchor": "middle", "font-family": "Consolas, monospace", "font-weight": 700, "font-size": 22, fill: "#1b1200" }).textContent = "lastBlink";
  const cur = svgEl(sv, "g", {});
  svgEl(cur, "path", { d: `M0 ${AY + 60} V${AY - 100}`, stroke: "#19c3b4", "stroke-width": 5 });
  svgEl(cur, "circle", { cx: 0, cy: AY, r: 12, fill: "#19c3b4" });
  svgEl(cur, "text", { x: 0, y: AY - 110, "text-anchor": "middle", "font-family": "Consolas, monospace", "font-weight": 700, "font-size": 26, fill: "#19c3b4" }).textContent = "now";
  const nextB = svgEl(sv, "path", { d: `M${X(1500)} ${AY - 46} H${X(2000)}`, stroke: "#4ade80", "stroke-width": 5, "stroke-dasharray": "12 8", opacity: 0 });
  TO(nextB, tNew, 0.4, { opacity: 1 });
  const nextL = box(tlg, X(1500), AY - 200, X(2000) - X(1500), 40, "", `<div style="text-align:center;font:700 26px var(--ui);color:var(--green)">new interval: next flip at 2000</div>`);
  hidden(nextL); pop(nextL, tNew + 0.2);
  const L = ledIcon(tlg, 1790, 560, 70);
  L.drive((t) => (t >= tN3 ? 1 : 0));
  dyn((t) => {
    if (t < T("s46") || t > T("s49")) return;
    const n = nowV(t), l = lastV(t);
    cur.setAttribute("transform", `translate(${X(n)} 0)`);
    flag.setAttribute("transform", `translate(${X(l)} 0)`);
    elapsed.setAttribute("x", X(l)); elapsed.setAttribute("width", Math.max(0, X(n) - X(l)));
    elapsed.setAttribute("fill", n - l >= 500 ? "rgba(74,222,128,.7)" : "rgba(255,181,71,.6)");
    elapsed.setAttribute("opacity", t >= tN1 && t < tSet ? 1 : 0);
    thr.setAttribute("d", `M${X(l + 500)} ${AY - 90} V${AY + 14}`);
    thrL.setAttribute("x", X(l + 500)); thrL.setAttribute("y", AY - 98);
    thrL.textContent = "lastBlink + 500";
  });
  // s49: unsigned long + roll-over
  const ty = box(sMil, 150, 220, 760, 230, "card", `<div style="padding:30px 38px"><div style="font:700 40px var(--mono);color:var(--amber)">unsigned long</div>
    <div style="font:600 30px var(--ui);margin-top:12px">0 … 4,294,967,295</div><div class="muted" style="font-size:26px;margin-top:8px">a big whole number, never negative</div></div>`);
  hidden(ty); pop(ty, W("s49", "unsigned")); hide(ty, S1("s49") + 0.1, 0.3);
  const sb = pill(sMil, 150, 500, "always: now − lastTime", "font-size:32px");
  pop(sb, W("s49", "subtract")); hide(sb, S1("s49") + 0.1, 0.3);
  const ro = box(sMil, 1000, 220, 780, 300, "card", `<div style="padding:28px 38px;font:600 30px var(--mono);line-height:1.6">
    <div style="font:700 28px var(--ui);color:var(--muted)">after ~49.7 days: … 4,294,967,295 → 0</div>
    <div>lastBlink = 4,294,967,000</div><div>now = 200</div><div>now − lastBlink = <span style="color:var(--teal)">496 ✓</span></div></div>`);
  hidden(ro); pop(ro, W("s49", "fortynine")); hide(ro, S1("s49") + 0.1, 0.3);
  const okS = pill(sMil, 1000, 560, "✓ the subtraction still works", "");
  pop(okS, W("s49", "subtraction")); hide(okS, S1("s49") + 0.1, 0.3);
  // s50: the button with the same trick
  const db = bigCode(sMil, 120, 220, 1680, "if (state != lastState && now - lastChange >= 50) {\n  lastChange = now;\n  lastState = state;\n  if (state == LOW) blinking = !blinking;\n}", { size: 38 });
  show(db.c, T("s50"), 0.4); hide(db.c, T("s51") - 0.1, 0.3);
  db.hl([[0, -1], [W("s50", "ignore"), 0]]);
  const bn = pillC(sMil, 640, "a change within 50 ms of the last one → ignored (that's the bounce)", "font-size:30px");
  pop(bn, W("s50", "ignore") + 0.3); hide(bn, T("s51") - 0.1, 0.3);
  // s51: the never-waiting loop
  const spin = box(sMil, 610, 250, 700, 560, "", `<svg width="700" height="560" viewBox="0 0 700 560">
    <circle cx="350" cy="280" r="200" fill="none" stroke="#22304d" stroke-width="18"/>
    <path class="arc" d="M350 80 A200 200 0 0 1 550 280" fill="none" stroke="#19c3b4" stroke-width="18" stroke-linecap="round"/>
    <text x="350" y="270" text-anchor="middle" font-family="Consolas, monospace" font-weight="700" font-size="44" fill="#e8eef7">loop()</text>
    <text x="350" y="320" text-anchor="middle" font-family="Segoe UI" font-weight="600" font-size="26" fill="#8fa1c0">thousands of times a second</text></svg>`);
  hidden(spin); show(spin, T("s51"), 0.4); hide(spin, S1("s51") + 0.1, 0.3);
  const arc = $(".arc", spin);
  dyn((t) => { if (t >= T("s51") - 0.5 && t < S1("s51") + 0.5) arc.setAttribute("transform", `rotate(${(t * 900) % 360} 350 280)`); });
  for (const [txt, x, y, w] of [["✓ button?", 330, 500, "button"], ["✓ clock?", 1330, 500, "clock"]]) {
    const c = box(sMil, x, y, 260, 70, "", `<span class="pill" style="font-size:30px">${txt}</span>`);
    hidden(c); pop(c, W("s51", w)); hide(c, S1("s51") + 0.1, 0.3);
  }
  // s52: the real result
  heroClip(stage, "C5", W("s52", "Upload") + 0.6, T("s53") - 0.3 - FC, "blink_button: the LED blinks; a press stops it at once, another starts it again.", { full: true });
  fullAfter("blink_button", "s53");
}

/* ======================================================================
 * TWO LEDS, TWO TIMERS (s56-s58); the wiring (s53-s55) is in the breadboard scene
 * ==================================================================== */
const sTwo = SC();
sceneIn(sTwo, S1("s55") + 0.5);
sceneOut(sTwo, S1("s58") + 0.4);
{
  const h = head(sTwo, "Two LEDs, two timers", 50); show(h, T("s56"));
  const src = (g) => `if (now - lastRed >= 500) {\n  lastRed = now;     // flip red\n}\nif (now - lastGreen >= ${g}) {\n  lastGreen = now;   // flip green\n}`;
  const c1 = bigCode(sTwo, 80, 170, 1000, src(150), { size: 38 }), c2 = bigCode(sTwo, 80, 170, 1000, src(300), { size: 38 });
  show(c1.c, T("s56"), 0.4); SET(c1.c, T("s58"), { opacity: 0 }); SET(c2.c, T("s58"), { opacity: 1 });
  c1.hl([[0, -1], [W("s56", "Red"), 0], [W("s56", "green", 2), 3], [S1("s56"), -1]]);
  c2.hl([[0, -1], [T("s58"), 3, "rgba(74,222,128,.25)"], [W("s58", "Upload"), -1]]);
  // two lanes of flips: red every 500 ms, green every 150 (300 after the change)
  const LX0 = 1180, LX1 = 1840, WIN = 3; // seconds shown
  const lanes = box(sTwo, 0, 0, 1920, 1080, ""); hidden(lanes); show(lanes, T("s56") + 0.2, 0.4); hide(lanes, W("s58", "Upload"), 0.3);
  box(lanes, LX0, 214, 600, 34, "", `<div style="font:700 24px var(--ui);color:#ff8a8f">red: every 500 ms</div>`);
  const rl = box(lanes, LX0, 260, LX1 - LX0, 70, "card", "");
  const glab = box(lanes, LX0, 374, 600, 34, "", "");
  const gl = box(lanes, LX0, 420, LX1 - LX0, 70, "card", "");
  textAt(glab, [[0, `<div style="font:700 24px var(--ui);color:#8af5b0">green: every 150 ms</div>`], [T("s58"), `<div style="font:700 24px var(--ui);color:#8af5b0">green: every <b>300</b> ms</div>`]]);
  const tA = T("s56"), tChg = T("s58");
  dyn((t) => {
    if (t < tA - 0.5 || t > S1("s58") + 1) return;
    // ticks of the last WIN seconds, scrolling left
    const mk = (per, col, t0) => {
      let s = "";
      const first = Math.ceil((t - WIN - t0) / per);
      for (let k = Math.max(0, first); t0 + k * per <= t; k++) {
        const tk = t0 + k * per, x = (1 - (t - tk) / WIN) * (LX1 - LX0 - 20) + 10;
        s += `<i style="position:absolute;left:${x}px;top:12px;width:6px;height:46px;border-radius:3px;background:${col}"></i>`;
      }
      return s;
    };
    const r = mk(0.5, "#ff5d6c", tA);
    const g = t < tChg ? mk(0.15, "#4ade80", tA) : mk(0.3, "#4ade80", tChg);
    if (rl.__v !== r) { rl.innerHTML = r; rl.__v = r; }
    if (gl.__v !== g) { gl.innerHTML = g; gl.__v = g; }
  });
  const R = ledIcon(sTwo, 1260, 560, 110, "red"), G = ledIcon(sTwo, 1590, 560, 110, "green");
  hidden(R.r); hidden(G.r); show([R.r, G.r], T("s56") + 0.2, 0.4); hide([R.r, G.r], W("s58", "Upload"), 0.3);
  R.drive((t) => blink(t, tA, 0.5, 0.5));
  G.drive((t) => (t < tChg ? blink(t, tA, 0.15, 0.15) : blink(t, tChg, 0.3, 0.3)));
  quizCard(sTwo, "Green interval 150 → 300. Does the red LED change too?", W("s57", "Quick"), T("s58"), "No: each if checks only its own timer", { y: 800, w: 1500, t1: W("s58", "Upload") - 0.2 });
  const unchanged = pill(sTwo, 1500, 210, "red: unchanged ✓", "font-size:24px;background:rgba(74,222,128,.16);color:var(--green)");
  pop(unchanged, W("s58", "only")); hide(unchanged, W("s58", "Upload"), 0.3);
  heroClip(stage, "C7", W("s58", "Upload") + 0.3, T("s59") - 0.3 - FC, "two_leds: red and green blink at their own speeds; a press stops red, green keeps going.", { full: true });
  fullAfter("two_leds", "s59");
}

/* ======================================================================
 * YOUR TURN (s59-s60)
 * ==================================================================== */
const sCh = SC();
sceneIn(sCh, S1("s58") + 0.4);
sceneOut(sCh, S1("s60") + 0.4);
{
  const dot = (c) => `<span style="display:inline-block;width:26px;height:26px;border-radius:50%;background:${c};box-shadow:0 0 14px ${c}"></span>`;
  yourTurnScene(sCh, {
    kicker: "YOUR TURN · CHALLENGE",
    title: "The speed-shifter",
    subtitle: "same circuit, same sketch (two_leds) as a starting point",
    rule1Title: "Red never changes",
    rule1Desc: "it keeps blinking every 500 ms, whatever you press",
    rule1FlowHtml: `${dot("#ff5d6c")} <span>500 ms</span><span class="muted">·</span><span>500 ms</span><span class="muted">·</span><span>500 ms</span>`,
    rule2Tag: "RULE 2 · THE TWIST",
    rule2Title: "Each press switches green",
    rule2Desc: "fast (150 ms) ↔ slow (600 ms): one change per press",
    rule2FlowHtml: `${dot("#4ade80")} <span>150 ms</span><span style="color:var(--amber)">→ press →</span><span>600 ms</span><span style="color:var(--amber)">→ press →</span><span>150 ms</span>`,
    hintHtml: "a variable <span style='font-family:var(--mono);color:var(--text)'>greenInterval</span> + the edge from button_toggle + one if",
    t0: T("s59"), tR1: W("s59", "Red"), tR2: W("s59", "Make"), tHint: W("s60", "variable"), tCom: W("s60", "comments"), tShort: W("s60", "Short"),
  });
}

/* ======================================================================
 * NOT WORKING? (s61)
 * ==================================================================== */
const sTrouble = SC();
sceneIn(sTrouble, S1("s60") + 0.4);
sceneOut(sTrouble, S1("s61") + 0.5);
{
  const chk = box(sTrouble, 300, 220, 1320, 600, "card", "");
  const rows = [["Button across the middle gap", "across"], ["Yellow wire in the D22 column", "yellow"], ["Always 0? Button turned sideways", "always"], ["Green dark? Black wire from its − rail to GND", "green"]];
  chk.innerHTML = `<div style="padding:44px 60px"><div class="kicker">Something not working?</div>` + rows.map(([a]) => `<div class="row" style="display:flex;gap:22px;align-items:center;margin-top:40px;opacity:0">
    <div style="width:56px;height:56px;border-radius:50%;background:var(--green);color:#052;font:800 32px var(--ui);display:flex;align-items:center;justify-content:center">✓</div>
    <div style="font:600 40px var(--display)">${a}</div></div>`).join("") + `</div>`;
  chk.querySelectorAll(".row").forEach((r, i) => TO(r, W("s61", rows[i][1]), 0.4, { opacity: 1 }));
}

/* ======================================================================
 * OUTRO (s62-s63)
 * ==================================================================== */
const sOutro = SC();
sceneIn(sOutro, S1("s61") + 0.5);
{
  const h = box(sOutro, 110, 170, 1500, 80, "h2", "Episode 4 complete!"); hidden(h); pop(h, T("s62"));
  const items = [["digitalRead", "HIGH or LOW", "digital"], ["INPUT_PULLUP", "the built-in pull-up", "pullup"], ["The edge", "the moment of a press", "edge"],
    ["Debounce", "wait out the bounce", "bounce"], ["millis()", "check the clock, don't wait", "millis"]];
  const cards = items.map(([a, b, w], i) => {
    const c = box(sOutro, 110 + i * 345, 360, 320, 300, "card", `<div style="padding:30px"><div style="width:60px;height:60px;border-radius:50%;background:rgba(25,195,180,.15);color:var(--teal);font:700 30px var(--display);display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div style="font:700 32px var(--display);margin-top:26px">${a}</div><div class="muted" style="font-size:22px;margin-top:8px">${b}</div></div>
      <div class="ok" style="position:absolute;right:22px;top:22px;width:54px;height:54px;border-radius:50%;background:var(--green);color:#052;font:700 32px var(--ui);display:flex;align-items:center;justify-content:center;opacity:0">✓</div>`);
    hidden(c);
    pop(c, W("s62", w) - 0.15);
    const ok = $(".ok", c);
    SET(ok, W("s62", w) + 0.2, { scale: 0.4 });
    TO(ok, W("s62", w) + 0.2, 0.4, { opacity: 1, scale: 1, ease: "back.out(2)" });
    return c;
  });
  hide(cards, T("s63") - 0.1, 0.4); hide(h, T("s63") - 0.1, 0.4);
  const nx = box(sOutro, 260, 230, 1400, 360, "card", `<div style="padding:50px 60px"><div class="kicker">Next episode</div>
    <div style="font:700 60px var(--display);margin:14px 0 18px">PWM: fades and colors</div>
    <div class="muted" style="font-size:28px">Fade an LED smoothly with PWM, and mix any color with an RGB LED.</div></div>`);
  hidden(nx); pop(nx, T("s63") + 0.2);
  const gh = box(sOutro, 260, 640, 1400, 120, "card", `<div style="display:flex;align-items:center;gap:26px;height:120px;padding:0 50px">
    <svg width="54" height="54" viewBox="0 0 16 16"><path fill="#fff" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.290 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
    <div style="font:600 36px var(--mono)">github.com/emjnbulut/esp32-from-zero</div></div>`);
  hidden(gh); pop(gh, W("s63", "GitHub"));
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 });
  TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}

window.__seek(0);
window.__ready = true;
