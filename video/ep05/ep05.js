/* Episode 5 - PWM: Make an LED Breathe (v6 curriculum, 2026-10-30).
 * PRODUCTION_GUIDELINES.md sections 5, 7, 9, 10: cold open with the real result, retrieval minute, every idea as an everyday
 * picture (emoji card) + its limit ("The difference: ..."), PRIMM code tours with predict pauses, a common mistake, an
 * "explain in your own words" pause, a 3-point outro and the comments invite. Max 2 subtle like/subscribe reminders.
 * Everything is anchored to segment ids / words (S0, S1, W), never to absolute seconds: dub runs may shift the schedule.
 * Circuits are drawn the way the creator builds them: two breadboards standing VERTICAL side by side, the ESP32 at the
 * bottom across both with the USB cable pointing down; red LED (rows 38-40, 220 ohm below) and button (rows 33-36) on the
 * right board, black ground wire at row ~60 to the minus rail (footage/gelen/ep05/20261029_154331.mp4). */
const stage = $("#stage");
const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const hidden = (e) => { gsap.set(e, { opacity: 0 }); return e; };
const CUT = S0("s04") - 0.1; // the channel sting is inserted here (tools/bumpers.py cut(), script "sting_after": "s03")
const B = (a, b) => (S1(a) + S0(b)) / 2; // the scene boundary between two segments
const span = (sc, t0, t1) => { sceneIn(sc, t0, 0.45); if (t1 != null) sceneOut(sc, t1, 0.45); };

function head(parent, html, y = 52) {
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
/** side-view red LED with a glow behind it; drive(fn) sets brightness 0..1 from time */
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
  const drive = (fn) => dyn((t) => { const v = fn(t); glow.style.opacity = v; hot.setAttribute("opacity", v * 0.75); });
  return { r, glow, drive };
}
/** an RGB "light" (outro teaser): a frosted dome whose color follows fn(t) -> [r, g, b] */
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
    const [R, G, Bl] = fn(t), m = Math.max(R, G, Bl) / 255;
    dome.setAttribute("fill", m > 0.02 ? `rgb(${Math.round(150 + R * 0.41)},${Math.round(150 + G * 0.41)},${Math.round(150 + Bl * 0.41)})` : "#e8edf3");
    glow.style.opacity = m;
    glow.style.background = `radial-gradient(circle, rgba(${R},${G},${Bl},.9) 0%, rgba(${R},${G},${Bl},.4) 30%, rgba(${R},${G},${Bl},0) 65%)`;
  });
  return { r, glow, drive };
}
const blink = (t, t0, on, off) => (t < t0 ? 0 : ((t - t0) % (on + off)) < on ? 1 : 0);
const inAny = (t, list) => list.some(([a, b]) => t >= a && t < b);
/** the breathing fade of fade_millis: 0..1..0, one step every `ms` ms (255 steps up, 255 down) */
const tri = (t, t0, ms = 4) => { const P2 = 2 * 255 * ms / 1000, x = ((t - t0) % P2 + P2) % P2 / P2; return x < 0.5 ? x * 2 : 2 - x * 2; };
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
  const p = box(parent, x, y, 0, 0, "", `<span class="pill" style="font-size:30px;${style}">${html}</span>`);
  css(p, { width: "auto", height: "auto", whiteSpace: "nowrap" });
  return hidden(p);
};
const pillC = (parent, y, html, style = "", x = 0, w = 1920) => hidden(box(parent, x, y, w, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:32px;${style}">${html}</span></div>`));
const zcam = (z, t, dur, cx, cy, s) => TO(z, t, dur, { x: 960 - s * cx, y: 540 - s * cy, scale: s, ease: "power2.inOut" });
const zset = (z, t, cx, cy, s) => SET(z, t, { x: 960 - s * cx, y: 540 - s * cy, scale: s });
/** a PWM square wave in an svg group: duty 0..1, `cycles` periods across w px; returns the path */
function wave(g, x, y, w, h, duty, cycles = 6, color = "#ffb547", sw = 6) {
  let d = `M${x} ${y + h}`;
  const p = w / cycles;
  for (let i = 0; i < cycles; i++) {
    const x0 = x + i * p;
    if (duty >= 1) d += ` H${x0} V${y} H${x0 + p}`;
    else if (duty <= 0) d += ` H${x0 + p}`;
    else d += ` H${x0} V${y} H${x0 + p * duty} V${y + h} H${x0 + p}`;
  }
  return svgEl(g, "path", { d, stroke: color, "stroke-width": sw, fill: "none", "stroke-linejoin": "round" });
}
const txt = (g, x, y, s, attrs) => { const e = svgEl(g, "text", Object.assign({ x, y, "font-family": "Segoe UI", "font-weight": 700, "font-size": 26, fill: "#8fa1c0" }, attrs)); e.textContent = s; return e; };

/** everyday picture (section 9): emoji + head + line over the dimmed scene; `limit` (the analogy's limit, section 10)
 * appears at tLim under a divider: "The difference: ..." */
function exCard(emoji, hd, line, t0, t1, limit, tLim, opts = {}) {
  const dim = box(stage, 0, 0, 1920, 1080, ""); css(dim, { background: "rgba(6,10,20,.76)", zIndex: 79 });
  const w = opts.w || 1380, x = (1920 - w) / 2, y = opts.y || (limit ? 250 : 330);
  const c = box(stage, x, y, w, 0, "excard2",
    `<div class="em">${emoji}</div><div><div class="hd">${hd}</div><div class="ln">${line}</div>${limit ? `<div class="lim"><b>The difference:</b> ${limit}</div>` : ""}</div>`);
  css(c, { height: "auto" });
  gsap.set([dim, c], { opacity: 0 });
  TO(dim, t0 - 0.1, 0.3, { opacity: 1, ease: "power1.out" });
  pop(c, t0, 0.4);
  if (limit) { const l = $(".lim", c); gsap.set(l, { opacity: 0 }); TO(l, tLim != null ? tLim : t0 + 0.3, 0.4, { opacity: 1, ease: "power1.out" }); }
  TO([dim, c], t1, 0.35, { opacity: 0, ease: "power1.in" });
  return c;
}
/* like / subscribe (section 5): max 2, top-right corner, ~2.6 s */
const likeTop = (t0) => likeSub(stage, t0, 2.6, { style: { top: "36px", bottom: "auto" } });
/** a quick-question / predict card (lib quizCard) with its own kicker */
function ask(parent, kicker, q, t0, tAns, answer, opts) {
  const c = quizCard(parent, q, t0, tAns, answer, opts);
  $(".qk", c).innerHTML = kicker;
  return c;
}

/* ======================================================================
 * THE CREATOR'S CIRCUIT, drawn vertical (see header). vbb(parent, x, y, p): p = hole pitch in px.
 * Holes: L(col, row) with col "a".."j" (left board), "A".."J" (right board), "lp"/"lm" "rp"/"rm" (rails), row 1..60.
 * ==================================================================== */
let vbbN = 0;
function vbb(parent, X, Y, p = 15) {
  const id = "vb" + vbbN++;
  const COL = { lp: 1.0, lm: 2.0, a: 3.6, b: 4.6, c: 5.6, d: 6.6, e: 7.6, f: 9.6, g: 10.6, h: 11.6, i: 12.6, j: 13.6,
    A: 23.6, B: 24.6, C: 25.6, D: 26.6, E: 27.6, F: 29.6, G: 30.6, H: 31.6, I: 32.6, J: 33.6, rp: 35.2, rm: 36.2 };
  const RY = (r) => (1.6 + (r - 1)) * p;
  const L = (c, r) => [COL[c] * p, RY(r)];
  const W_ = 37.2 * p, bot = RY(60) + 2.2 * p, H_ = bot + 4 * p;
  const root = box(parent, X, Y, W_, H_, "");
  const svg = svgEl(root, "svg", { width: W_, height: H_ + 400, viewBox: `0 0 ${W_} ${H_ + 400}` });
  css(svg, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  svgEl(svg, "defs").innerHTML = `<linearGradient id="${id}sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9edf2"/><stop offset=".5" stop-color="#b9c0c9"/><stop offset="1" stop-color="#d9dee5"/></linearGradient>
    <radialGradient id="${id}gl"><stop offset="0" stop-color="#ff6b6b" stop-opacity=".95"/><stop offset=".35" stop-color="#ff4d4d" stop-opacity=".55"/><stop offset="1" stop-color="#ff3030" stop-opacity="0"/></radialGradient>`;
  const bg = svgEl(svg, "g", {});
  const hole = (g, x, y) => svgEl(g, "rect", { x: x - 0.25 * p, y: y - 0.25 * p, width: 0.5 * p, height: 0.5 * p, rx: 0.1 * p, fill: "#4a4842" });
  for (const [x0, groove, cols, rails, lineX] of [
    [0, 8.6, "abcdefghij", ["lp", "lm"], [[0.45, "#e5484d"], [2.55, "#3b6fe0"]]],
    [22.6, 28.6, "ABCDEFGHIJ", ["rp", "rm"], [[34.65, "#e5484d"], [36.75, "#3b6fe0"]]]]) {
    svgEl(bg, "rect", { x: x0 * p, y: 0, width: 14.6 * p, height: bot, rx: 0.8 * p, fill: "#ecebe6", stroke: "#c9c6bd", "stroke-width": 2 });
    svgEl(bg, "rect", { x: (groove - 0.4) * p, y: 0.5 * p, width: 0.8 * p, height: bot - p, rx: 0.3 * p, fill: "#d6d3cb" });
    for (const [lx, col] of lineX) svgEl(bg, "path", { d: `M${lx * p} ${0.6 * p} V${bot - 0.6 * p}`, stroke: col, "stroke-width": 0.18 * p });
    for (let r = 1; r <= 60; r++) {
      for (const c of cols) hole(bg, ...L(c, r));
      if (r % 6 !== 0) for (const c of rails) hole(bg, ...L(c, r));
      if (r === 1 || r % 5 === 0) txt(bg, groove * p, RY(r) + 0.22 * p, String(r), { "text-anchor": "middle", "font-size": 0.62 * p, fill: "#8d8a80", "font-weight": 600 });
    }
    for (const c of cols) txt(bg, COL[c] * p, bot - 0.55 * p, c, { "text-anchor": "middle", "font-size": 0.6 * p, fill: "#8d8a80", "font-weight": 600 });
    rails.forEach((c, k) => txt(bg, COL[c] * p, bot - 0.45 * p, k ? "−" : "+", { "text-anchor": "middle", "font-size": 1.1 * p, "font-weight": 800, fill: k ? "#3b6fe0" : "#e5484d" }));
  }
  // the ESP32 (30 pins), headers in left col j and right col A, rows 46-60, USB down, red cable to the bottom edge
  const esp = svgEl(svg, "g", {});
  const [xl] = L("j", 46), [xr] = L("A", 46), yT = RY(46), yB = RY(60);
  svgEl(esp, "path", { d: `M${(xl + xr) / 2} ${yB + 3.4 * p} V${yB + 30 * p}`, stroke: "#c8202b", "stroke-width": 1.6 * p, "stroke-linecap": "round" });
  svgEl(esp, "rect", { x: (xl + xr) / 2 - 1.0 * p, y: yB + 2.2 * p, width: 2.0 * p, height: 1.6 * p, rx: 0.2 * p, fill: "#f2f2f2" });
  svgEl(esp, "rect", { x: (xl + xr) / 2 - 1.3 * p, y: yB + 1.2 * p, width: 2.6 * p, height: 1.4 * p, rx: 0.2 * p, fill: `url(#${id}sh)`, stroke: "#7d8690" });
  svgEl(esp, "rect", { x: xl - 0.9 * p, y: yT - 1.9 * p, width: xr - xl + 1.8 * p, height: yB - yT + 3.6 * p, rx: 0.5 * p, fill: "#1b1f26", stroke: "#2b313b", "stroke-width": 2 });
  svgEl(esp, "rect", { x: xl + 1.6 * p, y: yT - 1.5 * p, width: xr - xl - 3.2 * p, height: 7.6 * p, rx: 0.2 * p, fill: "#24384f" });
  svgEl(esp, "rect", { x: xl + 2.0 * p, y: yT + 0.6 * p, width: xr - xl - 4.0 * p, height: 5.2 * p, rx: 0.2 * p, fill: `url(#${id}sh)` });
  svgEl(esp, "path", { d: `M${xl + 2.2 * p} ${yT - 0.8 * p} h${xr - xl - 4.4 * p}`, stroke: "#c9a54a", "stroke-width": 0.35 * p, "stroke-dasharray": `${0.9 * p} ${0.5 * p}` });
  txt(esp, (xl + xr) / 2, yT + 3.6 * p, "ESP32", { "text-anchor": "middle", "font-size": 1.1 * p, fill: "#5d6670" });
  for (const [bx, by] of [[xl + 1.2 * p, yB + 0.6 * p], [xr - 2.4 * p, yB + 0.6 * p]]) svgEl(esp, "rect", { x: bx, y: by, width: 1.2 * p, height: 0.9 * p, rx: 0.15 * p, fill: "#9aa1aa" });
  const LP = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"];
  const RP = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"];
  for (let k = 0; k < 15; k++) {
    for (const [c, nm, dx, anchor] of [["j", LP[k], 0.7, "start"], ["A", RP[k], -0.7, "end"]]) {
      const [px, py] = L(c, 46 + k);
      svgEl(esp, "rect", { x: px - 0.32 * p, y: py - 0.32 * p, width: 0.64 * p, height: 0.64 * p, rx: 0.08 * p, fill: "#d4af37" });
      const hot = nm === "D23" || nm === "D22" || nm === "GND";
      txt(esp, px + dx * p, py + 0.22 * p, nm, { "text-anchor": anchor, "font-size": 0.6 * p, fill: hot ? "#ffe3b8" : "#c9d1dc", "font-weight": hot ? 800 : 600 });
    }
  }
  const parts = svgEl(svg, "g", {});
  const over = svgEl(svg, "g", {});
  const wire = (a, b, color, bend = 0.15) => {
    const [ax, ay] = L(...a), [bx, by] = L(...b), mx = (ax + bx) / 2, my = (ay + by) / 2;
    const g = svgEl(parts, "g", {});
    svgEl(g, "path", { d: `M${ax} ${ay} Q${mx - (by - ay) * bend} ${my + (bx - ax) * bend} ${bx} ${by}`, fill: "none", stroke: color, "stroke-width": 0.5 * p, "stroke-linecap": "round" });
    for (const [ex, ey] of [[ax, ay], [bx, by]]) svgEl(g, "rect", { x: ex - 0.28 * p, y: ey - 0.28 * p, width: 0.56 * p, height: 0.56 * p, rx: 0.08 * p, fill: "#222" });
    return g;
  };
  // ground: GND (row 59) -> minus rail; D22 (row 47) -> button (row 36); the button and the LED's short leg -> minus rail
  wire(["D", 59], ["rm", 59], "#1d1f24", 0.04);
  wire(["C", 47], ["C", 36], "#8a9099", 0.08);
  wire(["I", 34], ["rm", 34], "#ff8a2a", 0);
  wire(["I", 39], ["rm", 39], "#ff8a2a", 0);
  // the 220 ohm resistor: D23's row (46) -> the LED's long leg (row 40)
  {
    const [ax, ay] = L("D", 46), [bx, by] = L("F", 40), ang = Math.atan2(by - ay, bx - ax) * 180 / Math.PI, len = Math.hypot(bx - ax, by - ay);
    const g = svgEl(parts, "g", { transform: `translate(${ax} ${ay}) rotate(${ang})` });
    svgEl(g, "path", { d: `M0 0 H${len}`, stroke: "#b8bec6", "stroke-width": 0.22 * p });
    const bl = 2.6 * p, b0 = (len - bl) / 2;
    svgEl(g, "rect", { x: b0, y: -0.5 * p, width: bl, height: p, rx: 0.42 * p, fill: "#5aa0d8", stroke: "#3a78ad", "stroke-width": 1 });
    [0.45, 0.85, 1.25, 1.9].forEach((o, k) => svgEl(g, "rect", { x: b0 + o * p, y: -0.5 * p, width: 0.22 * p, height: p, fill: ["#d0262f", "#d0262f", "#3b2a1a", "#c9a54a"][k] }));
  }
  // the red LED: long leg row 40, short leg row 39 (column G), dome above them
  const [gx, g39] = L("G", 39), [, g40] = L("G", 40), dc = [gx - 0.2 * p, RY(37.4)];
  const glow = svgEl(over, "circle", { cx: dc[0], cy: dc[1], r: 4.2 * p, fill: `url(#${id}gl)`, opacity: 0 });
  for (const yy of [g39, g40]) svgEl(parts, "path", { d: `M${gx} ${yy} L${dc[0] + (yy === g40 ? 0.3 : -0.3) * p} ${dc[1]}`, stroke: "#b8bec6", "stroke-width": 0.22 * p });
  svgEl(parts, "circle", { cx: dc[0], cy: dc[1], r: 0.95 * p, fill: "#b51d27" });
  svgEl(parts, "circle", { cx: dc[0], cy: dc[1], r: 0.8 * p, fill: "#d4202c" });
  const lit = svgEl(parts, "circle", { cx: dc[0], cy: dc[1], r: 0.8 * p, fill: "#ffd0d0", opacity: 0 });
  // the push button across the groove, legs in rows 34 and 36 (columns E and F)
  const [ex] = L("E", 34), [fx] = L("F", 34), by0 = RY(33.4), by1 = RY(36.6);
  for (const [lx, ly] of [[ex, RY(34)], [fx, RY(34)], [ex, RY(36)], [fx, RY(36)]]) svgEl(parts, "rect", { x: lx - 0.25 * p, y: ly - 0.25 * p, width: 0.5 * p, height: 0.5 * p, fill: "#aab2bd" });
  svgEl(parts, "rect", { x: ex - 0.7 * p, y: by0, width: fx - ex + 1.4 * p, height: by1 - by0, rx: 0.25 * p, fill: "#23272f", stroke: "#3a404b", "stroke-width": 2 });
  const cap = svgEl(parts, "circle", { cx: (ex + fx) / 2, cy: (by0 + by1) / 2, r: 1.0 * p, fill: "#4a5262", stroke: "#11141a", "stroke-width": 2 });
  const led = { cx: dc[0], cy: dc[1], drive: (fn) => dyn((t) => { const v = clamp01(fn(t)); glow.setAttribute("opacity", v); lit.setAttribute("opacity", v * 0.8); }) };
  const btn = { cx: (ex + fx) / 2, cy: (by0 + by1) / 2, press: (list) => dyn((t) => { const on = inAny(t, list); cap.setAttribute("r", on ? 0.8 * p : 1.0 * p); cap.setAttribute("fill", on ? "#ffb547" : "#4a5262"); }) };
  /** a point in the parent's coordinates (valid while the drawing is not scaled) */
  const S = (c, r) => { const [lx, ly] = L(c, r); return [X + lx, Y + ly]; };
  return { root, svg, L, S, RY, p, w: W_, h: H_, led, btn, parts, over };
}

/** the creator's circuit cropped to the interesting part: row `rowTop` sits at screen y `yTop`, the rows above fade out
 * at the top edge (the boards continue out of the frame, like the camera framing) */
function deskCircuit(parent, x, p, rowTop, yTop) {
  const Y = Math.round(yTop - (rowTop + 0.6) * p);
  const bb = vbb(parent, x, Y, p);
  const f = box(parent, x - 10, 0, bb.w + 20, yTop + p, "");
  css(f, { background: "linear-gradient(180deg, #0b1220 0%, #0b1220 25%, rgba(11,18,32,0) 100%)" });
  bb.Y = Y;
  return bb;
}

/* ======================================================================
 * COLD OPEN (s01-s03): the breathing LED, then the promise
 * ==================================================================== */
const sCold = SC();
SET(sCold, 0, { opacity: 1 });
SET(sCold, CUT, { opacity: 0 });
heroClip(stage, "C0", 0, S1("s02") + 0.35, "fade_millis: the red LED breathes; one press stops it at once, a second press resumes it.", { full: true });
{
  const kick = box(sCold, 140, 230, 900, 40, "kicker", "ESP32 From Zero · Episode 5");
  const title = box(sCold, 134, 276, 1100, 280, "h1", "Make an LED<br>breathe.");
  css(title, { fontSize: "118px", lineHeight: "1.02" });
  const sub = box(sCold, 140, 560, 1000, 60, "h3", "the trick is called <span style='color:var(--amber)'>PWM</span>");
  for (const e of [kick, title, sub]) gsap.set(e, { opacity: 0, y: 30 });
  [[kick, T("s03") - 0.3], [title, T("s03")], [sub, W("s03", "trick")]].forEach(([e, t]) => TO(e, t, 0.7, { opacity: 1, y: 0, ease: "power3.out" }));
  const L = ledIcon(sCold, 1400, 250, 170);
  hidden(L.r); show(L.r, T("s03") - 0.2, 0.4);
  L.drive((t) => tri(t, 0, 4));
  const onoff = pill(sCold, 1290, 690, "the pin: only <b style='color:var(--amber)'>fully on</b> or <b style='color:var(--muted)'>fully off</b>", "font-size:30px");
  pop(onoff, W("s03", "only"));
}

/* ======================================================================
 * RETRIEVAL MINUTE (s04-s07): two questions from episode 4, thinking pause, answer
 * ==================================================================== */
const sRet = SC();
span(sRet, CUT, B("s07", "s08"));
{
  const k = box(sRet, 0, 70, 1920, 40, "kicker", "Quick recall · from earlier episodes"); k.style.textAlign = "center"; hidden(k); show(k, CUT + 0.2);
  const n = box(sRet, 0, 112, 1920, 70, "h2", ""); n.style.textAlign = "center";
  panelAt(n, [[0, ""], [W("s04", "Quick"), "Question 1 of 2"], [W("s06", "Quick"), "Question 2 of 2"]]);
  // Q1 picture: the pull-up inside the chip, the pin, the button to ground
  const t1 = W("s04", "Quick"), a1 = T("s05"), e1 = T("s06") - 0.15;
  const pic1 = box(sRet, 0, 0, 1920, 1080, ""); hidden(pic1); show(pic1, t1, 0.4); hide(pic1, e1, 0.3);
  const sv = svgLayer(pic1);
  svgEl(sv, "rect", { x: 330, y: 230, width: 520, height: 420, rx: 22, fill: "#121b2e", stroke: "#2c3b5e", "stroke-width": 2, "stroke-dasharray": "10 8" });
  txt(sv, 590, 275, "inside the chip", { "text-anchor": "middle", "font-size": 28 });
  txt(sv, 590, 340, "3.3 V", { "text-anchor": "middle", "font-size": 36, fill: "#ff8a8f", "font-weight": 800 });
  svgEl(sv, "path", { d: "M590 355 V390 l-22 10 l44 16 l-44 16 l44 16 l-44 16 l22 10 V520 H1060", stroke: "#c3c9d1", "stroke-width": 6, fill: "none", "stroke-linejoin": "round" });
  txt(sv, 640, 450, "weak pull-up", { "font-size": 26 });
  svgEl(sv, "circle", { cx: 850, cy: 520, r: 12, fill: "#d4af37" });
  txt(sv, 850, 575, "GPIO 22", { "text-anchor": "middle", "font-size": 30, fill: "#e8eef7", "font-family": "Cascadia Mono, Consolas" });
  svgEl(sv, "path", { d: "M1260 520 H1400 V600", stroke: "#c3c9d1", "stroke-width": 6, fill: "none" });
  svgEl(sv, "path", { d: "M1350 600 H1450 M1365 618 H1435 M1382 636 H1418", stroke: "#c3c9d1", "stroke-width": 6 });
  txt(sv, 1400, 690, "GND", { "text-anchor": "middle", "font-size": 32, fill: "#e8eef7" });
  const bt = btnIcon(pic1, 1060, 440, 200); bt.press([[a1, e1 + 1]]);
  const flow = svgEl(sv, "path", { d: "M850 520 H1060 M1260 520 H1400 V600", stroke: "#19c3b4", "stroke-width": 10, fill: "none", opacity: 0, "stroke-linecap": "round" });
  TO(flow, a1 + 0.2, 0.4, { opacity: 0.9 });
  const low = pill(pic1, 1470, 470, "pin = <b>LOW</b> while pressed", "font-size:32px"); pop(low, W("s05", "ground"));
  ask(sRet, "QUICK QUESTION", "With the built-in pull-up: while you <b>press</b> the button, does the pin read HIGH or LOW?", t1, a1,
    "LOW: pressing connects the pin to ground, and ground wins against the weak pull-up", { y: 740, w: 1500, t1: e1 });
  // Q2 picture: delay() stops the program, the button is not looked at
  const t2 = W("s06", "Quick"), a2 = T("s07"), e2 = B("s07", "s08") - 0.1;
  const pic2 = box(sRet, 0, 0, 1920, 1080, ""); hidden(pic2); show(pic2, t2, 0.4);
  const code = bigCode(pic2, 260, 240, 760, "digitalWrite(LED_PIN, HIGH);\ndelay(2000);\ndigitalWrite(LED_PIN, LOW);", { size: 40 });
  show(code.c, t2, 0.4);
  code.hl([[0, -1], [a2, 1, "rgba(255,93,108,.3)"]]);
  const hg = box(pic2, 1110, 230, 200, 200, "", `<div style="font-size:150px;line-height:1;text-align:center">⏳</div>`);
  const b2 = btnIcon(pic2, 1400, 250, 170);
  const presses = [[W("s06", "miss") - 0.3, W("s06", "miss")], [a2 + 0.6, a2 + 0.9], [a2 + 1.8, a2 + 2.1]];
  b2.press(presses);
  const miss = pill(pic2, 1360, 450, "✕ nobody looks", "font-size:30px;background:rgba(255,93,108,.18);color:#ffc2c8");
  pop(miss, W("s07", "nobody"));
  const back = pillC(pic2, 640, "⟲ keep it in mind: it comes back today", "font-size:32px;background:rgba(255,181,71,.16);color:var(--amber)");
  pop(back, W("s07", "Keep"));
  hidden(hg); show(hg, t2, 0.4);
  ask(sRet, "QUICK QUESTION", "Why does a long <span style='font-family:var(--mono)'>delay()</span> make the board miss a button press?", t2, a2,
    "During a delay the program simply stops: nobody looks at the button", { y: 740, w: 1500, t1: W("s07", "Keep") - 0.1 });
  [back].forEach((e) => hide(e, e2, 0.3));
}

/* ======================================================================
 * PARTS (s08): the episode 4 circuit, drawn like the creator's desk
 * ==================================================================== */
const sParts = SC();
span(sParts, B("s07", "s08"), B("s08", "s09"));
{
  const h = box(sParts, 110, 60, 900, 80, "h2", "What you need"); hidden(h); show(h, T("s08"));
  const rows = [["🔁", "The episode 4 circuit", "already on your desk", "circuit"],
    ["🔴", "Red LED + 220 Ω", "on <b>GPIO 23</b>", "red"],
    ["🔘", "Push button", "on <b>GPIO 22</b>", "button"],
    ["📟", "Multimeter", "a nice extra (optional)", "multimeter"]];
  rows.forEach(([ic, nm, ds, w], i) => {
    const r = box(sParts, 110, 190 + i * 190, 860, 160, "partrow", `<div class="ic">${ic}</div><div><div class="nm">${nm}</div><div class="ds">${ds}</div></div>`);
    hidden(r); pop(r, W("s08", w) - 0.1);
  });
  const Z = box(sParts, 0, 0, 1920, 1080, "");
  const bb = deskCircuit(Z, 1040, 22, 27, 150);
  hidden(Z); show(Z, T("s08") + 0.2, 0.5);
  bb.led.drive((t) => tri(t, T("s08"), 4));
  bb.btn.press([[W("s08", "button"), W("s08", "button") + 0.5]]);
  const tag = (html, ty, px, py, t0) => {
    const s = svgLayer(sParts); css(s, { zIndex: 5 });
    const ln = svgEl(s, "path", { d: `M1290 ${ty} L${px} ${py}`, stroke: "#ffb547", "stroke-width": 4, opacity: 0 });
    svgEl(s, "circle", { cx: px, cy: py, r: 7, fill: "#ffb547" });
    callout(sParts, html, 1050, ty - 24, t0, null, { style: { fontSize: "28px", zIndex: 6 } });
    TO(ln, t0, 0.3, { opacity: 1 });
  };
  const at = (o) => [1040 + o.cx, bb.Y + o.cy];
  tag("button · GPIO 22", 290, ...at(bb.btn), W("s08", "button"));
  tag("red LED · GPIO 23", 400, ...at(bb.led), W("s08", "red"));
  tag("220 Ω", 500, 1040 + bb.L("E", 43)[0], bb.Y + bb.L("E", 43)[1], W("s08", "red") + 0.5);
}

/* ======================================================================
 * PWM, THE IDEA (s09-s14): light switch -> ceiling fan -> square wave -> the limit
 * ==================================================================== */
const sPwm = SC();
span(sPwm, B("s08", "s09"), B("s14", "s15"));
{
  const hd = box(sPwm, 0, 50, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s09"), "digitalWrite: only ON or OFF"], [T("s11"), "The answer is speed"], [T("s13"), "PWM · pulse width modulation"]]);
  exCard("💡", "An ordinary light switch", "two choices only: fully on, or fully off", W("s09", "like"), S1("s09") + 0.1);
  // s09-s10: on / off
  const L = ledIcon(sPwm, 860, 230, 150);
  hidden(L.r); show(L.r, T("s09"), 0.4); hide(L.r, T("s11") - 0.1, 0.3);
  L.drive((t) => (t < T("s10") ? blink(t, T("s09"), 0.9, 0.9) : 0));
  for (const [s, x, col] of [["HIGH → fully on", 470, "var(--amber)"], ["LOW → fully off", 1170, "var(--muted)"]]) {
    const c = pill(sPwm, x, 600, s, `font-size:34px;color:${col}`); pop(c, S1("s09") + 0.2); hide(c, T("s11") - 0.1, 0.3);
  }
  ask(sPwm, "QUICK QUESTION", "A pin is only ever ON or OFF. How could it make an LED glow at <b>half</b> brightness?", W("s10", "Quick"), T("s11"),
    "Speed: switch it on and off very fast", { y: 740, w: 1500, t1: W("s11", "Think") - 0.2 });
  // s11: the ceiling fan
  exCard("🌀", "A ceiling fan", "spinning fast, you can't see the single blades, only a soft blur", W("s11", "Think"), S1("s11") + 0.1);
  // s12: a fast square wave and the LED at its average
  const sv = svgLayer(sPwm);
  const g12 = svgEl(sv, "g", { opacity: 0 });
  TO(g12, T("s12"), 0.4, { opacity: 1 }); TO(g12, T("s15") - 0.6, 0.3, { opacity: 0 });
  const wv = wave(g12, 260, 300, 1000, 200, 0.5, 10);
  drawOn(wv, T("s12") + 0.1, 1.4);
  const yOn = txt(g12, 235, 312, "ON", { "text-anchor": "end", "font-size": 30 });
  const yOff = txt(g12, 235, 512, "OFF", { "text-anchor": "end", "font-size": 30 });
  textAt(yOn, [[0, "ON"], [W("s13", "three"), "3.3 V"]]);
  textAt(yOff, [[0, "OFF"], [W("s13", "zero"), "0 V"]]);
  const L12 = ledIcon(sPwm, 1500, 260, 140);
  hidden(L12.r); show(L12.r, T("s12") + 0.3, 0.4); hide(L12.r, T("s15") - 0.6, 0.3);
  L12.drive((t) => (t < W("s12", "eye") ? blink(t, T("s12"), 0.12, 0.12) : 0.5));
  const k1 = pill(sPwm, 330, 600, "on / off ≈ <b>1000 times a second</b>", "font-size:34px"); pop(k1, W("s12", "thousand")); hide(k1, T("s13") - 0.1, 0.3);
  const avg = pill(sPwm, 1380, 620, "your eye sees: the <b>average</b>", "font-size:30px"); pop(avg, W("s12", "average")); hide(avg, T("s15") - 0.6, 0.3);
  const only = pill(sPwm, 330, 600, "always 3.3 V or 0 V · only the <b>timing</b> changes", "font-size:34px;background:rgba(255,181,71,.16);color:var(--amber)");
  pop(only, W("s13", "timing")); hide(only, T("s15") - 0.6, 0.3);
  // s14: the fan again, with its limit
  exCard("🌀", "A ceiling fan", "spinning fast, you can't see the single blades, only a soft blur", T("s14"), S1("s14") + 0.2,
    "a fan really passes through every position. The LED is only ever fully on or fully off: the in-between happens in your eye.", W("s14", "difference"));
}

/* ======================================================================
 * DUTY CYCLE (s15-s18): one cycle, the tap, 25 / 50 / 100 %
 * ==================================================================== */
const sDuty = SC();
span(sDuty, B("s14", "s15"), B("s18", "s19"));
{
  const hd = box(sDuty, 0, 50, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s15"), "The duty cycle"], [T("s18"), "Duty cycle → brightness"]]);
  const sv = svgLayer(sDuty);
  const g = svgEl(sv, "g", { opacity: 0 });
  TO(g, T("s15"), 0.4, { opacity: 1 }); TO(g, T("s18") - 0.1, 0.3, { opacity: 0 });
  const X0 = 360, CW = 600, Y0 = 360, HH = 240;
  wave(g, X0, Y0, CW * 2, HH, 0.3, 2, "#ffb547", 8);
  const onR = svgEl(g, "rect", { x: X0, y: Y0 - 4, width: CW * 0.3, height: HH + 8, rx: 8, fill: "rgba(255,181,71,.25)", opacity: 0 });
  TO(onR, W("s15", "stays"), 0.4, { opacity: 1 });
  svgEl(g, "path", { d: `M${X0} ${Y0 + HH + 50} H${X0 + CW} M${X0} ${Y0 + HH + 36} V${Y0 + HH + 64} M${X0 + CW} ${Y0 + HH + 36} V${Y0 + HH + 64}`, stroke: "#19c3b4", "stroke-width": 5 });
  txt(g, X0 + CW / 2, Y0 + HH + 100, "one short cycle", { "text-anchor": "middle", "font-size": 34, fill: "#19c3b4" });
  const onT = txt(g, X0 + CW * 0.15, Y0 - 24, "ON", { "text-anchor": "middle", "font-size": 34, fill: "#ffb547", opacity: 0 });
  TO(onT, W("s15", "stays"), 0.4, { opacity: 1 });
  const dc = pillC(sDuty, 760, "how long it stays ON in each cycle = the <b>duty cycle</b>", "font-size:38px");
  pop(dc, W("s15", "duty")); hide(dc, T("s18") - 0.1, 0.3);
  exCard("🚰", "A tap you open briefly every second", "a quarter of each second: only a little water · always open: the full stream", W("s16", "Think"), S1("s16") + 0.1);
  exCard("🚰", "A tap you open briefly every second", "a quarter of each second: only a little water · always open: the full stream", T("s17"), S1("s17") + 0.15,
    "a real tap can be half open, but a PWM pin is never half on.", W("s17", "difference"));
  // s18: 25 / 50 / 100 %
  [[0.25, "25 %", "twentyfive", "dim"], [0.5, "50 %", "fifty", "medium"], [1, "100 %", "hundred", "fully bright"]].forEach(([duty, lab, w, nm], i) => {
    const y = 210 + i * 270, t0 = W("s18", w) - 0.1;
    const gg = svgEl(sv, "g", { opacity: 0 }); TO(gg, t0, 0.35, { opacity: 1 });
    wave(gg, 400, y, 900, 130, duty, 6);
    txt(gg, 350, y + 82, lab, { "text-anchor": "end", "font-size": 48, "font-weight": 800, fill: "#e8eef7" });
    const Li = ledIcon(sDuty, 1450, y - 30, 90);
    hidden(Li.r); show(Li.r, t0, 0.35); Li.drive(() => duty);
    const nmE = box(sDuty, 1600, y + 50, 300, 50, "", `<div style="font:700 32px var(--ui);color:var(--muted)">${nm}</div>`); hidden(nmE); show(nmE, t0, 0.35);
  });
}

/* ======================================================================
 * analogWrite (s19-s21): the dimmer knob, 0..255, quick question
 * ==================================================================== */
const sAw = SC();
span(sAw, B("s18", "s19"), B("s21", "s23"));
{
  const code = bigCode(sAw, 260, 90, 1400, "analogWrite(LED_PIN, 128);", { size: 66 });
  show(code.c, T("s19"), 0.4);
  // labels under the two arguments (mono 66 px: 0.6 em per character, code text starts at x = 300)
  const argLab = (s, cx) => hidden(box(sAw, cx - 150, 262, 300, 50, "", `<div style="text-align:center;font:700 32px var(--ui);color:var(--teal)">▲ ${s}</div>`));
  show(argLab("which pin", 300 + 15.5 * 39.6), W("s19", "pin"), 0.4);
  show(argLab("0 … 255", 300 + 22.5 * 39.6), W("s19", "number"), 0.4);
  const val = (t) => {
    if (t < W("s20", "zero")) return 128;
    if (t < W("s20", "two")) return 0;
    if (t < W("s20", "Quick")) return 255;
    return 128;
  };
  const quizOn = (t) => t >= W("s20", "Quick") && t < T("s21");
  const bar = box(sAw, 260, 420, 1400, 90, "card", "");
  hidden(bar); show(bar, W("s19", "number"), 0.4);
  const fill = box(bar, 0, 0, 0, 90, "");
  css(fill, { background: "linear-gradient(90deg, rgba(255,181,71,.35), rgba(255,181,71,.95))", borderRadius: "20px" });
  const ticks = box(sAw, 260, 520, 1400, 40, "", `<div style="display:flex;justify-content:space-between;font:700 28px var(--mono);color:var(--muted)"><span>0</span><span>128</span><span>255</span></div>`);
  hidden(ticks); show(ticks, W("s19", "number"), 0.4);
  const lab = box(sAw, 260, 590, 1400, 60, "", "");
  css(lab, { font: "700 40px var(--mono)", textAlign: "center" }); hidden(lab); show(lab, W("s19", "number"), 0.4);
  const L = ledIcon(sAw, 1720, 420, 100);
  hidden(L.r); show(L.r, W("s19", "number"), 0.4);
  L.drive((t) => (quizOn(t) ? 0 : val(t) / 255));
  dyn((t) => {
    const v = val(t), q = quizOn(t);
    fill.style.width = (q ? 0 : (v / 255) * 1400) + "px";
    const h = q ? `analogWrite(…, <span style="color:var(--amber)">?</span>) → <span style="color:var(--teal)">about 50 %</span>`
      : `analogWrite(…, <span style="color:var(--amber)">${v}</span>) → <span style="color:var(--teal)">${Math.round(v / 2.55)} %</span> on`;
    if (lab.__v !== h) { lab.innerHTML = h; lab.__v = h; }
  });
  exCard("🎚️", "A dimmer knob with many small clicks", "0 = always off · 255 = always on", W("s20", "like"), W("s20", "Quick") - 0.15);
  ask(sAw, "QUICK QUESTION", "Which number gives about <b>half</b> brightness?", W("s20", "Quick"), T("s21"),
    "About 128: on for half of every cycle", { y: 740, w: 1300, t1: W("s21", "difference") - 0.2 });
  exCard("🎚️", "A dimmer knob with many small clicks", "0 = always off · 255 = always on", W("s21", "difference") - 0.05, S1("s21") + 0.2,
    "a real dimmer turns smoothly, but analogWrite has exactly <b style='color:var(--text)'>256 steps</b> (0 … 255).", W("s21", "difference"));
}

/* ======================================================================
 * CODE TOUR 1: pwm_levels (s23-s27) - whole sketch, highlighted lines, live "now" value, predict pause
 * ==================================================================== */
const REPO = "<b>github.com/emjnbulut/esp32-from-zero</b> → lessons/05-pwm · link in the description";
/** footer of a code tour: live values on the left (filled by a dyn), the repo path on the right */
const nowFoot = (key) => `<div class="fc-now"><div class="live" id="${key}"></div><div class="repo">${REPO}</div></div>`;
function liveVals(key, fn) {
  let e = null;
  dyn((t) => {
    e = e || document.getElementById(key);
    const h = fn(t);
    if (e && e.__v !== h) { e.innerHTML = h; e.__v = h; }
  });
}
const vv = (name, v) => `<span class="v">${name} = <b>${v}</b></span>`;
{
  const t0 = T("s23") - 0.4, t1 = T("s28") - 0.3;
  fullCode(stage, "pwm_levels.ino", SKETCHES.pwm_levels, t0, t1, nowFoot("nowpwm"), [
    [T("s23"), null],
    [W("s23", "top"), "const int LED_PIN"],
    [W("s23", "Setup"), "void setup", "}"],
    [W("s24", "function"), "void showLevel"],
    [W("s25", "call"), "showLevel(64)"],
    [W("s25", "inside"), "void showLevel"],
    [W("s25", "Analog"), "analogWrite(LED_PIN, value)"],
    [W("s25", "prints"), 'Serial.print("analogWrite', 'Serial.println("% on'],
    [W("s25", "waits"), "delay(2000)"],
    [T("s26"), "void showLevel", "delay(2000)"],
    [T("s27"), "void loop", "showLevel(255)"],
  ]);
  const calls = [[W("s27", "zero"), 0], [W("s27", "sixtyfour"), 64], [W("s27", "twentyeight"), 128], [W("s27", "fiftyfive"), 255]];
  liveVals("nowpwm", (t) => {
    const k = `<span class="k">NOW</span>`;
    if (t < W("s25", "call")) return k + vv("value", "–");
    if (t < T("s26")) return k + vv("value", 64) + (t >= W("s25", "Analog") ? `<span class="v">LED ≈ <b>25 %</b></span>` : "");
    if (t < W("s26", "forgets")) return k + vv("value", 64);
    if (t < calls[0][0]) return k + vv("value", "<span style='color:var(--muted)'>gone</span>");
    if (t < W("s27", "Pause")) return k + vv("value", stateAt(calls, t));
    return k + vv("value", "?") + `<span class="v">LED = <b>?</b></span>`;
  });
  exCard("📝", "A recipe with a blank", "showLevel( ___ ): the number in the brackets fills the blank on every call", W("s24", "Think"), S1("s24") + 0.1);
  exCard("📝", "A recipe with a blank", "showLevel( ___ ): the number in the brackets fills the blank on every call", T("s26") - 0.05, S1("s26") + 0.2,
    "the function forgets the value as soon as it finishes.", W("s26", "difference"));
  const pr = ask(stage, "⏸ PAUSE AND PREDICT", "What will the LED do at each of the four steps?", W("s27", "Pause"), T("s28") + 1,
    "", { x: 1040, y: 560, w: 820, t1: t1 });
  css(pr, { zIndex: 85 });
}

/* ======================================================================
 * RUN (s28): clip C2, the four levels named under it
 * ==================================================================== */
heroClip(stage, "C2", T("s28"), T("s29") - 0.4, "pwm_levels: the LED in four steps: off, 25 %, 50 %, 100 %. Slightly dim room.", { full: true });
{
  const p = box(stage, 0, 930, 1920, 80, "", ""); css(p, { zIndex: 70, textAlign: "center" });
  const lv = (n, s) => `<span class="pill" style="font-size:36px;background:rgba(11,18,32,.85);border:2px solid #19c3b4;color:#d9fffa">analogWrite <b style="color:var(--amber)">${n}</b> · ${s}</span>`;
  panelAt(p, [[0, ""], [W("s28", "off"), lv(0, "off")], [W("s28", "dim"), lv(64, "dim")], [W("s28", "medium"), lv(128, "medium")],
    [W("s28", "bright"), lv(255, "fully bright")], [T("s29") - 0.5, ""]]);
}

/* ======================================================================
 * MULTIMETER (s29-s31): the meter shows the average; clip C1; your turn: 64 -> 10
 * ==================================================================== */
const sMeter = SC();
span(sMeter, T("s29") - 0.5, B("s31", "s32"));
likeTop(T("s29") + 0.6); // reminder 1 of 2: right after the first real result
{
  const hd = box(sMeter, 100, 40, 980, 80, "h2", "A multimeter shows the average"); css(hd, { fontSize: "50px" }); hidden(hd); show(hd, T("s29"));
  const bb = deskCircuit(sMeter, 900, 20, 26, 150);
  bb.led.drive((t) => stateAt([[0, 0.25], [W("s30", "one"), 0.5], [W("s30", "three"), 1], [T("s31"), 0.25], [W("s31", "A"), 0.06]], t));
  const mv = box(sMeter, 0, 0, 1920, 1080, "");
  mv.innerHTML = `<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0"><g transform="translate(0 -60)">
    <rect x="300" y="200" width="420" height="640" rx="40" fill="#f2c230"/><rect x="345" y="250" width="330" height="170" rx="14" fill="#cfe3c4"/>
    <circle cx="510" cy="600" r="105" fill="#2b2f36"/><path d="M510 600 l64 -64" stroke="#f2c230" stroke-width="16"/>
    <text x="510" y="770" text-anchor="middle" font-family="Segoe UI" font-weight="800" font-size="34" fill="#2b2f36">V ⎓</text></g></svg>`;
  const rd = box(mv, 345, 220, 330, 120, "");
  css(rd, { font: "800 92px Consolas, monospace", color: "#1c2a14", textAlign: "center" });
  textAt(rd, [[0, "0.80"], [W("s30", "one"), "1.65"], [W("s30", "three"), "3.30"], [T("s31"), "0.80"], [W("s31", "tenth"), "0.13"]]);
  // probes: red on GPIO 23's strip (row 46), black on the minus rail
  const sv = svgLayer(sMeter); css(sv, { zIndex: 3 });
  const [rx, ry] = bb.S("E", 46), [kx, ky] = bb.S("rm", 30);
  const pr = svgEl(sv, "path", { d: `M680 160 C 820 120, ${rx - 260} ${ry - 220}, ${rx} ${ry}`, stroke: "#d63b3b", "stroke-width": 9, fill: "none", "stroke-linecap": "round" });
  const pk = svgEl(sv, "path", { d: `M640 160 C 760 110, ${kx - 300} ${ky - 60}, ${kx} ${ky}`, stroke: "#1d1f24", "stroke-width": 9, fill: "none", "stroke-linecap": "round" });
  for (const [x, y, c] of [[rx, ry, "#d63b3b"], [kx, ky, "#555"]]) svgEl(sv, "circle", { cx: x, cy: y, r: 9, fill: c });
  drawOn(pr, T("s29") + 0.3, 0.8); drawOn(pk, T("s29") + 0.6, 0.8);
  const c1 = callout(sMeter, "GPIO 23's row", rx + 20, ry - 70, T("s29") + 1.0, null, { style: { fontSize: "24px" } });
  const c2 = callout(sMeter, "− rail", kx + 24, ky - 20, T("s29") + 1.2, null, { style: { fontSize: "24px" } });
  void c1; void c2;
  const slow = pill(sMeter, 120, 900, "too slow to follow the switching → it shows the <b>average</b>", "font-size:30px");
  pop(slow, W("s29", "slow")); hide(slow, T("s30") - 0.1, 0.3);
}
heroClip(stage, "C1", T("s30"), T("s31") - 0.4, "Multimeter, hands-free: pwm_levels; probes on GPIO 23's strip and the minus rail. 0 -> 0.8 -> 1.65 -> 3.3 V.", { full: true });
{
  const p = box(stage, 0, 930, 1920, 80, "", ""); css(p, { zIndex: 70, textAlign: "center" });
  const v = (pc, volts) => `<span class="pill" style="font-size:38px;background:rgba(11,18,32,.85);border:2px solid #ffb547;color:#ffe3b8">${pc} on → <b style="color:#fff">${volts}</b></span>`;
  panelAt(p, [[0, ""], [W("s30", "zero"), v("25 %", "≈ 0.8 V")], [W("s30", "one"), v("50 %", "≈ 1.65 V")], [W("s30", "three"), v("100 %", "3.3 V")],
    [W("s30", "exactly"), `<span class="pill" style="font-size:36px;background:rgba(11,18,32,.85);border:2px solid #19c3b4;color:#d9fffa">volts = 3.3 V × the share of time ON</span>`], [T("s31") - 0.45, ""]]);
}
{
  // s31: your turn, 64 -> 10 (the meter scene underneath still shows the meter and the circuit)
  const yt = ask(sMeter, "YOUR TURN", "In pwm_levels, replace <span style='font-family:var(--mono);color:var(--amber)'>showLevel(64)</span> with <span style='font-family:var(--mono);color:var(--amber)'>showLevel(10)</span>. What will you see?",
    W("s31", "replace"), W("s31", "A"), "A very faint glow, and about a tenth of a volt (10 / 255 × 3.3 V ≈ 0.13 V)", { x: 80, y: 790, w: 1000 });
  css(yt, { zIndex: 40 });
}

/* ======================================================================
 * THE OBVIOUS FADE (s32): two for loops with delay()
 * ==================================================================== */
const sFade = SC();
span(sFade, B("s31", "s32"), B("s32", "s34"));
{
  const hd = head(sFade, "Make it breathe: the obvious way", 40); show(hd, T("s32"));
  const naive = bigCode(sFade, 90, 160, 1180, "for (int b = 0; b <= 255; b++) {\n  analogWrite(LED_PIN, b);\n  delay(4);\n}\nfor (int b = 255; b >= 0; b--) {\n  analogWrite(LED_PIN, b);\n  delay(4);\n}", { size: 38 });
  show(naive.c, T("s32"), 0.4);
  naive.hl([[0, -1], [W("s32", "One"), 0], [W("s32", "delay"), 2], [W("s32", "other"), 4], [S1("s32") + 0.2, -1]]);
  const L = ledIcon(sFade, 1500, 200, 130);
  hidden(L.r); show(L.r, T("s32"), 0.4);
  L.drive((t) => tri(t, T("s32"), 4));
  const bv = box(sFade, 1380, 560, 440, 0, "nowbox", ""); css(bv, { height: "auto" }); hidden(bv); show(bv, T("s32") + 0.3, 0.4);
  dyn((t) => {
    if (t < T("s32") - 1 || t > S1("s32") + 2) return;
    const h = `<div class="k">NOW</div>b = <b>${Math.round(tri(t, T("s32"), 4) * 255)}</b>`;
    if (bv.__v !== h) { bv.innerHTML = h; bv.__v = h; }
  });
  const sec = pill(sFade, 1380, 770, "256 steps × 4 ms ≈ 1 s up, 1 s down", "font-size:26px"); pop(sec, W("s32", "down"));
}

/* ======================================================================
 * COMMON MISTAKE (s34-s38): the blocking fade misses the button
 * ==================================================================== */
const sMis = SC();
span(sMis, B("s32", "s34"), B("s38", "s39"));
{
  const ban = box(sMis, 860, 50, 980, 70, "", `<div style="display:flex;justify-content:center"><div class="banner" style="position:static">⚠ COMMON MISTAKE · a fade built from delay()</div></div>`);
  css(ban, { zIndex: 10 });
  hidden(ban); show(ban, T("s34"), 0.4);
  // s34: the circuit, the LED breathing, the button pressed (nothing happens)
  const Z = box(sMis, 0, 0, 1920, 1080, ""); Z.style.transformOrigin = "0 0";
  const bb = deskCircuit(Z, 110, 18, 28, 150);
  hidden(Z); show(Z, T("s34"), 0.4); hide(Z, T("s37") - 0.1, 0.3);
  bb.led.drive((t) => tri(t, T("s34"), 4));
  const pt = [W("s34", "press"), T("s35") - 1.5, T("s35") - 0.6];
  bb.btn.press(pt.map((a) => [a, a + 0.25]));
  const code = bigCode(sMis, 860, 170, 980, "for (int b = 0; b <= 255; b++) {\n  analogWrite(LED_PIN, b);\n  delay(4);\n}", { size: 34 });
  show(code.c, T("s34"), 0.4); hide(code.c, T("s37") - 0.1, 0.3);
  ask(sMis, "QUICK QUESTION", "While this LED is fading, what happens when you press the button?", W("s34", "Quick"), T("s35"),
    "Nothing: the fade just carries on", { x: 860, y: 560, w: 980, t1: T("s36") - 0.2 });
  // s36 / s38: headphones on the stairs (+ its limit)
  exCard("🎧", "Climbing stairs with headphones on", "until you reach the top, you don't hear the doorbell", W("s36", "like"), S1("s36") + 0.1);
  exCard("🎧", "Climbing stairs with headphones on", "until you reach the top, you don't hear the doorbell", T("s38") - 0.05, S1("s38") + 0.25,
    "you might still feel a tap on your shoulder, but the board notices nothing until the loop ends.", W("s38", "difference"));
  // s37: the timeline: whole fades, the button read only in between
  const tl0 = T("s37");
  const g = box(sMis, 0, 0, 1920, 1080, ""); hidden(g); show(g, tl0, 0.4);
  const sv = svgLayer(g);
  const X0 = 180, Wd = 1560, Y = 470, per = Wd / 3;
  txt(sv, X0, Y - 150, "one fade ≈ 2 s · the button is read only between two fades", { "font-size": 36, fill: "#e8eef7" });
  for (let i = 0; i < 3; i++) {
    const x = X0 + i * per + 14;
    svgEl(sv, "rect", { x, y: Y - 50, width: per - 28, height: 100, rx: 14, fill: "rgba(255,93,108,.35)", stroke: "#ff5d6c", "stroke-width": 2 });
    txt(sv, x + (per - 28) / 2, Y + 12, "fading · inside delay()", { "text-anchor": "middle", "font-size": 30, fill: "#ffc2c8" });
    svgEl(sv, "path", { d: `M${X0 + i * per} ${Y - 80} V${Y + 80}`, stroke: "#4ade80", "stroke-width": 6 });
  }
  svgEl(sv, "path", { d: `M${X0 + 3 * per} ${Y - 80} V${Y + 80}`, stroke: "#4ade80", "stroke-width": 6 });
  txt(sv, X0, Y + 130, "▲ button read", { "font-size": 28, fill: "#4ade80" });
  const pressX = [0.35, 1.55, 2.4];
  pressX.forEach((f, i) => {
    const x = X0 + f * per, gg = svgEl(sv, "g", { opacity: 0 });
    svgEl(gg, "path", { d: `M${x} ${Y + 230} V${Y + 70}`, stroke: "#ffb547", "stroke-width": 6 });
    svgEl(gg, "path", { d: `M${x - 14} ${Y + 92} L${x} ${Y + 66} L${x + 14} ${Y + 92}`, fill: "#ffb547" });
    txt(gg, x, Y + 275, "press ✕ missed", { "text-anchor": "middle", "font-size": 28, fill: "#ffb547" });
    TO(gg, W("s37", "short") + i * 0.35, 0.3, { opacity: 1 });
  });
}

/* ======================================================================
 * THE FIX (s39-s41): the wall clock, one small step every 4 ms, turn around at the ends
 * ==================================================================== */
const sFix = SC();
span(sFix, B("s38", "s39"), B("s41", "s43"));
{
  const hd = box(sFix, 0, 40, 1920, 80, "h2", ""); hd.style.textAlign = "center";
  panelAt(hd, [[0, ""], [T("s39"), "The fix: glance at the clock"], [T("s40"), "One small step every 4 ms"], [T("s41"), "Turn around at the top and the bottom"]]);
  exCard("🕰️", "The wall clock from episode 4", "glance at it on every round · act only when enough time has passed", W("s39", "wall") - 0.1, S1("s39") + 0.15);
  const step = bigCode(sFix, 90, 150, 1100, "if (now - lastStep >= 4) {\n  lastStep = now;\n  brightness = brightness + step;\n  if (brightness >= 255) step = -1;\n  if (brightness <= 0) step = 1;\n  analogWrite(LED_PIN, brightness);\n}", { size: 36 });
  show(step.c, T("s39") + 0.2, 0.4);
  step.hl([[0, -1], [W("s40", "Every"), 0], [W("s40", "brightness"), 2], [W("s41", "top"), 3], [W("s41", "bottom"), 4], [S1("s41"), -1]]);
  const tS = T("s40");
  const bv = box(sFix, 1290, 150, 540, 0, "nowbox", ""); css(bv, { height: "auto" }); hidden(bv); show(bv, tS, 0.4);
  dyn((t) => {
    if (t < tS - 1 || t > S1("s41") + 2) return;
    const b = Math.round(tri(t, tS, 4) * 255), up = ((t - tS) % 2.04) < 1.02;
    const h = `<div class="k">NOW</div>brightness = <b>${b}</b><br>step = <b style="color:${up ? "var(--teal)" : "var(--red)"}">${up ? "+1" : "-1"}</b>`;
    if (bv.__v !== h) { bv.innerHTML = h; bv.__v = h; }
  });
  const Ls = ledIcon(sFix, 1500, 420, 120);
  hidden(Ls.r); show(Ls.r, tS + 0.3, 0.4);
  Ls.drive((t) => (t < tS ? 0 : tri(t, tS, 4)));
  const sec = pill(sFix, 1290, 780, "255 steps × 4 ms ≈ 1 second", "font-size:30px");
  pop(sec, W("s40", "Two"));
  // s41: the triangle (brightness over time) with a moving dot
  const gp = box(sFix, 90, 700, 1100, 300, "card", ""); hidden(gp); show(gp, T("s41"), 0.4);
  const ps = svgLayer(gp, 1100, 300);
  txt(ps, 60, 62, "255", { "text-anchor": "end", "font-size": 22, "font-family": "Consolas" });
  txt(ps, 60, 262, "0", { "text-anchor": "end", "font-size": 22, "font-family": "Consolas" });
  let d = ""; for (let k = 0; k <= 8; k++) d += `${k ? "L" : "M"}${80 + k * 125} ${k % 2 ? 55 : 255} `;
  const tp = svgEl(ps, "path", { d, stroke: "#4fc1ff", "stroke-width": 5, fill: "none" });
  drawOn(tp, T("s41"), 2.0);
  for (const [k, s] of [[1, "top: step = −1"], [2, "bottom: step = +1"]]) {
    const e = txt(ps, 80 + k * 125, k % 2 ? 40 : 290, s, { "text-anchor": "middle", "font-size": 24, fill: k === 1 ? "#ff8a8f" : "#19c3b4", opacity: 0 });
    TO(e, W("s41", k === 1 ? "top" : "bottom"), 0.3, { opacity: 1 });
  }
}

/* ======================================================================
 * CODE TOUR 2: fade_millis (s43-s49) - live "now" values, predict pause
 * ==================================================================== */
{
  const t0 = T("s43") - 0.4, t1 = S1("s49") + 0.4;
  fullCode(stage, "fade_millis.ino", SKETCHES.fade_millis, t0, t1, nowFoot("nowfade"), [
    [T("s43"), null],
    [W("s43", "Brightness"), "int brightness"],
    [W("s43", "Step"), "int step"],
    [T("s44"), "unsigned long lastStep"],
    [W("s44", "fading"), "bool fading"],
    [W("s44", "Below"), "int lastState", "unsigned long lastChange"],
    [T("s45"), "unsigned long now = millis"],
    [W("s45", "Part"), "// PART 1", "fading = !fading"],
    [W("s45", "flips"), "fading = !fading"],
    [T("s46"), "// PART 2", "if (fading && now - lastStep"],
    [W("s46", "Pause"), "if (fading && now - lastStep"],
    [W("s47", "checks"), "int state = digitalRead"],
    [T("s48"), "if (fading && now - lastStep"],
    [W("s48", "note"), "lastStep = now;", "brightness = brightness + step"],
    [W("s48", "At"), "if (brightness >= 255)", "step = -1"],
    [W("s48", "zero"), "if (brightness <= 0)", "step = 1;"],
    [W("s49", "analog"), "analogWrite(LED_PIN, brightness)"],
  ]);
  // the simulation the live values follow: the real fade (one step every 4 ms), frozen 2 ms after a step during the predict pause
  const tA = T("s43"), fz0 = W("s46", "Pause"), fz1 = T("s48");
  const sim = (t) => {
    const tt = t < fz0 ? t : t < fz1 ? fz0 : t - (fz1 - fz0);
    const steps = Math.floor((tt - tA) * 250), ms = 5000 + steps * 4;
    const ph = ((steps % 510) + 510) % 510, b = ph <= 255 ? ph : 510 - ph, up = ph < 255;
    return { b, up, last: ms, now: t >= fz0 && t < fz1 ? ms + 2 : ms };
  };
  liveVals("nowfade", (t) => {
    const s = sim(t);
    return `<span class="k">NOW</span>` + vv("brightness", s.b) + vv("step", s.up ? "+1" : "-1") + vv("lastStep", s.last) +
      vv("now", t >= fz0 && t < fz1 ? `<span style="color:var(--red)">${s.now}</span>` : s.now) + vv("fading", "true");
  });
  const pr = ask(stage, "⏸ PAUSE AND PREDICT", "The LED is breathing, but only <b>2 ms</b> have passed since the last step. What does PART 2 do?", W("s46", "Pause"), T("s47"),
    "Nothing at all: 2 is less than 4, so the if is skipped. The loop runs on and checks the button again.", { x: 210, y: 690, w: 1500, t1: S1("s47") });
  css(pr, { zIndex: 85 });
}

/* ======================================================================
 * RUN 2 (s50-s52): clip C4, quick question 4 -> 10, clip C5
 * ==================================================================== */
heroClip(stage, "C4", T("s50"), T("s51") - 0.4, "fade_millis, closer than C0: a press pauses it mid-fade, another press resumes it.", { full: true });
const sRun2 = SC();
span(sRun2, T("s51") - 0.5, T("s53") - 0.5);
likeTop(T("s51") + 0.3); // reminder 2 of 2: after the "it works" moment
{
  const hd = head(sRun2, "Modify: line 39", 60); show(hd, T("s51") - 0.3);
  const c = bigCode(sRun2, 210, 200, 1500, "if (fading && now - lastStep >= 4) {", { size: 50 });
  show(c.c, T("s51") - 0.3, 0.4);
  const four = c.body.innerHTML;
  dyn((t) => {
    const h = t < W("s51", "ten") ? four : four.replace(/>4</, "><span style=\"background:rgba(255,181,71,.3);border-radius:8px;padding:0 6px\">10</span><");
    if (c.body.__v !== h) { c.body.innerHTML = h; c.body.__v = h; }
  });
  ask(sRun2, "QUICK QUESTION", "We change the <b>4</b> to a <b>10</b>. Will the breath get faster, or slower?", W("s51", "Quick"), T("s52"),
    "Slower: each step waits 10 ms, so one way takes about 2.5 s", { y: 520, w: 1400 });
}
heroClip(stage, "C5", W("s52", "Each"), T("s53") - 0.4, "MODIFY: fade_millis with line 39 changed from 4 to 10; a visibly slower breath.", { full: true });

/* ======================================================================
 * EXPLAIN IN YOUR OWN WORDS (s53-s54)
 * ==================================================================== */
const sExp = SC();
span(sExp, T("s53") - 0.5, B("s54", "s55"));
{
  const card = box(sExp, 210, 170, 1500, 0, "card quiz", `<div class="qk">⏸ EXPLAIN IN YOUR OWN WORDS</div>
    <div class="qq" style="font-size:46px">Why does the button work in <span style="font-family:var(--mono);color:var(--teal)">fade_millis</span>,
    but not in <span style="font-family:var(--mono);color:var(--red)">fade_naive</span>?</div>
    <div style="font:600 30px var(--ui);color:var(--muted);margin-top:14px">one or two sentences are enough · pause the video</div>
    <div class="qbar" style="display:block"><i></i></div>`);
  css(card, { height: "auto" }); hidden(card); pop(card, T("s53"));
  TO($(".qbar i", card), W("s53", "explain"), Math.max(0.5, T("s54") - W("s53", "explain")), { width: "100%", ease: "none" });
  const no = box(sExp, 210, 570, 720, 300, "yn", `<div class="t" style="color:var(--red)">✕ fade_naive</div><div class="d">waits on every step, so nobody reads the button</div><div class="c">delay(4) × 510</div>`);
  css(no, { border: "2px solid rgba(255,93,108,.6)" });
  const yes = box(sExp, 990, 570, 720, 300, "yn", `<div class="t" style="color:var(--green)">✓ fade_millis</div><div class="d">never waits: glances at the clock and moves on</div><div class="c">if (now - lastStep >= 4)</div>`);
  css(yes, { border: "2px solid rgba(74,222,128,.6)" });
  hidden(no); hidden(yes);
  pop(no, W("s54", "first")); pop(yes, W("s54", "never"));
  const one = pill(sExp, 210, 486, "one way to say it:", "font-size:30px"); pop(one, T("s54"));
  const ps = box(sExp, 0, 520, 1920, 300, "", `<div style="text-align:center;font-size:220px;line-height:1;opacity:.85">⏸</div>`);
  hidden(ps); show(ps, W("s53", "pause") + 0.2, 0.4); hide(ps, T("s54") - 0.2, 0.3);
}

/* ======================================================================
 * OUTRO (s55-s56): you can now (3), next episode (RGB), comments
 * ==================================================================== */
const sOut = SC();
span(sOut, B("s54", "s55"));
{
  const h = box(sOut, 110, 150, 1700, 80, "h2", "Today you learned to…"); hidden(h); pop(h, T("s55"));
  const items = [["PWM", "dim an LED by switching it very fast", "PWM"], ["analogWrite()", "a number from 0 to 255 sets the brightness", "Analog"], ["A clock-based fade", "breathes and never stops listening", "fade"]];
  const cards = items.map(([a, b, w], i) => {
    const c = box(sOut, 110 + i * 580, 320, 540, 360, "card", `<div style="padding:40px"><div style="width:72px;height:72px;border-radius:50%;background:rgba(25,195,180,.15);color:var(--teal);font:800 38px var(--display);display:flex;align-items:center;justify-content:center">${i + 1}</div>
      <div style="font:800 42px var(--display);margin-top:30px">${a}</div><div style="font:600 30px/1.35 var(--ui);color:var(--muted);margin-top:12px">${b}</div></div>`);
    hidden(c); pop(c, W("s55", w) - 0.15);
    return c;
  });
  hide(cards, T("s56") - 0.1, 0.4); hide(h, T("s56") - 0.1, 0.4);
  const nx = box(sOut, 160, 150, 1180, 360, "card", `<div style="padding:50px 60px"><div class="kicker">Next · Episode 6</div>
    <div style="font:800 64px var(--display);margin:14px 0 18px">Mix any color</div>
    <div style="font:600 32px var(--ui);color:var(--muted)">an RGB LED: three tiny LEDs, three analogWrite() calls</div></div>`);
  hidden(nx); pop(nx, W("s56", "Next") + 0.1);
  const G = rgbIcon(sOut, 1480, 150, 190); hidden(G.r); show(G.r, W("s56", "RGB") - 0.3, 0.5);
  G.drive((t) => { const k = tri(t, 0, 8) * 255; return [k, 255 - k * 0.6, 255 - k]; });
  const cm = box(sOut, 0, 640, 1920, 100, "", `<div style="display:flex;justify-content:center"><div class="yt-badge com" style="font-size:38px;padding:20px 40px">💬 &nbsp;Tell me in the comments: what would you make breathe?</div></div>`);
  hidden(cm); pop(cm, W("s56", "comments"));
  const gh = box(sOut, 360, 800, 1200, 100, "card", `<div style="display:flex;align-items:center;justify-content:center;height:100px;font:600 34px var(--mono)">github.com/emjnbulut/esp32-from-zero</div>`);
  hidden(gh); pop(gh, W("s56", "See"));
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 });
  TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}

window.__seek(0);
window.__ready = true;
