/* Episode 7 Analog Input, Pin Rules and Debugging: segment-anchored scenes, creator footage C0-C2, code tours.
 * Helpers from episode 6 (vertical breadboards as the creator built them). s36 has no clip: animated LED plus knob. */
const stage = $("#stage");
const EP07_CLIP_SECONDS = {"C0": 13.233333, "C1": 13.766667, "C2": 15.333333};
function ep07Hero(id, t0, requestedEnd, description, opts = {}) {
  const lead = opts.full ? Math.min(0.3, t0) : 0;
  const tail = opts.full ? 0.35 : 0;
  const t1 = Math.min(requestedEnd, t0 + EP07_CLIP_SECONDS[id] - lead - tail - 1 / 30);
  if (!(t1 > t0)) throw new Error('No usable episode 7 footage: ' + id);
  return heroClip(stage, id, t0, t1, description, opts);
}
const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const hidden = (e) => { gsap.set(e, { opacity: 0 }); return e; };
const CUT = S0("s03") - 0.1; // the channel sting is inserted here (tools/bumpers.py cut(), script "sting_after": "s02")
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
      const hot = nm === "D23" || nm === "D22" || nm === "GND" || nm === "D34" || nm === "3V3";
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
  return { root, svg, L, S, RY, p, w: W_, h: H_, led, btn, parts, over, wire };
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
 * EPISODE 7 HELPERS
 * ==================================================================== */
const sweep = (t, t0, period) => { const x = (((t - t0) % period) + period) % period / period; return 0.5 - 0.5 * Math.cos(2 * Math.PI * x); };
const nz = (i, seed = 1) => { const s = Math.sin(i * 12.9898 + seed * 78.233) * 43758.5453; return s - Math.floor(s); };
/** what analogRead gives for a knob position 0..1: flattened a little near both ends, with a small jitter */
const reading = (pos, i = 0) => Math.max(0, Math.min(4095, Math.round(4095 * pos + (nz(i, 3) - 0.5) * 24)));
const lerp = (a, b, k) => a + (b - a) * Math.max(0, Math.min(1, k));
const repo = "Full code: <b>github.com/emjnbulut/esp32-from-zero</b> &rarr; lessons/07-analog-input";
function tour(file, t0, t1, marks) { return fullCode(stage, file + ".ino", SKETCHES[file], t0, t1, repo, marks); }
function chapter(first, next) { const sc = SC(); span(sc, Math.max(0, T(first) - 0.45), next ? T(next) - 0.45 : null); return sc; }
function askTop(...a) { const c = ask(...a); css(c, { zIndex: 95 }); return c; }
function title(sc, text, id) { const h = head(sc, text); show(h, T(id)); return h; }
function note(sc, text, t0, y = 840, t1 = null) {
  const n = box(sc, 130, y, 1660, 100, "", '<div style="font:600 34px/1.4 var(--ui);text-align:center;color:var(--muted)">' + text + "</div>");
  hidden(n); show(n, t0); if (t1) hide(n, t1, 0.25);
  return n;
}
function tile(sc, x, y, w, h, text, col = "var(--teal)") {
  return box(sc, x, y, w, h, "card", '<div style="padding:32px;border-top:4px solid ' + col + ';border-radius:20px;height:100%;box-sizing:border-box">' + text + "</div>");
}
/** a top view of the knob; drive(fn) turns its pointer, fn(t) = position 0..1 */
function knobIcon(parent, x, y, w = 240, legs = false) {
  const r = box(parent, x, y, w, legs ? w * 1.25 : w, "");
  const ticks = Array.from({ length: 11 }, (_, i) => { const a = (-225 + 27 * i) * Math.PI / 180; return `<path d="M${100 + 78 * Math.cos(a)} ${100 + 78 * Math.sin(a)} L${100 + 92 * Math.cos(a)} ${100 + 92 * Math.sin(a)}" stroke="#5f6f8f" stroke-width="5" stroke-linecap="round"/>`; }).join("");
  const lg = legs ? '<path d="M60 170 V248 M100 176 V248 M140 170 V248" stroke="#c3c9d1" stroke-width="9" stroke-linecap="round"/>' : "";
  r.innerHTML = `<svg width="${w}" height="${legs ? w * 1.25 : w}" viewBox="0 0 200 ${legs ? 250 : 200}" style="position:absolute;left:0;top:0">${lg}${ticks}
    <circle cx="100" cy="100" r="68" fill="#c9a24a" stroke="#8a6f2c" stroke-width="4"/><circle cx="100" cy="100" r="52" fill="#2b3140" stroke="#48526a" stroke-width="4"/>
    <g class="ptr"><rect x="94" y="52" width="12" height="42" rx="6" fill="#ffb547"/></g></svg>`;
  const ptr = $(".ptr", r);
  const drive = (fn) => dyn((t) => ptr.setAttribute("transform", `rotate(${-135 + 270 * fn(t)} 100 100)`));
  return { r, drive };
}
/** a recreated Serial Monitor; fn(i, time) = the number printed on line i, one line every dt seconds from t0 */
function serialMon(parent, x, y, w, h, fn, t0, dt = 0.1, rows = 9, size = 38) {
  const c = box(parent, x, y, w, h, "card", `<div style="height:58px;display:flex;align-items:center;padding:0 24px;border-bottom:2px solid #2c3b5e;font:700 26px var(--ui);color:var(--muted)">Serial Monitor<span style="margin-left:auto;font:600 22px var(--mono)">115200 baud</span></div><div class="ln" style="padding:12px 28px;font:600 ${size}px/${Math.round(size * 1.3)}px var(--mono);color:#b9f3ec;white-space:pre"></div>`);
  const ln = $(".ln", c);
  dyn((t) => {
    if (t < t0 - 1) { if (ln.__s !== "") { ln.innerHTML = ""; ln.__s = ""; } return; }
    const n = Math.max(0, Math.floor((t - t0) / dt)), a = Math.max(0, n - rows + 1), out = [];
    for (let k = a; k <= n; k++) out.push(String(fn(k, t0 + k * dt)));
    const s = out.join("\n");
    if (ln.__s !== s) { ln.textContent = s; ln.__s = s; }
  });
  return c;
}
/** the ruler: 0 .. 4095 under 0 .. 3.3 V, with a pointer driven by fn(t) = 0..1 */
function ruler(parent, x, y, w, fn) {
  const r = box(parent, x, y, w, 190, "");
  const svg = svgEl(r, "svg", { width: w, height: 190, viewBox: `0 0 ${w} 190` });
  css(svg, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  svgEl(svg, "rect", { x: 0, y: 70, width: w, height: 56, rx: 8, fill: "#e8d9a8", stroke: "#a58f4f", "stroke-width": 2 });
  for (let i = 0; i <= 40; i++) svgEl(svg, "path", { d: `M${w * i / 40} 70 V${70 + (i % 10 === 0 ? 40 : i % 5 === 0 ? 28 : 16)}`, stroke: "#5b4d20", "stroke-width": i % 10 === 0 ? 4 : 2 });
  txt(svg, 0, 165, "0", { "font-size": 36, fill: "#ffb547", "font-family": "Consolas" });
  txt(svg, w, 165, "4095", { "font-size": 36, fill: "#ffb547", "text-anchor": "end", "font-family": "Consolas" });
  txt(svg, 0, 50, "0 V", { "font-size": 32, fill: "#b9f3ec" });
  txt(svg, w, 50, "3.3 V", { "font-size": 32, fill: "#b9f3ec", "text-anchor": "end" });
  const p = svgEl(svg, "path", { d: "M-16 44 H16 L0 72 Z", fill: "#ff5d6c" });
  dyn((t) => p.setAttribute("transform", `translate(${w * fn(t)} 0)`));
  return r;
}
/** the proportional bar of a scale, used for "4095 versus 255" */
function scaleBar(parent, x, y, w, col, label, val) {
  const b = box(parent, x, y, w, 96, "");
  css(b, { background: col, borderRadius: "14px", display: "flex", alignItems: "center", padding: "0 26px", boxSizing: "border-box", color: "#0b1220", font: "800 36px var(--mono)", whiteSpace: "nowrap" });
  b.innerHTML = val;
  const l = box(parent, x, y - 52, 900, 44, "", `<div style="font:700 32px var(--ui);color:var(--text)">${label}</div>`);
  return { b, l };
}
/** draws the knob on the creator's circuit (right board, rows 46-52, shaft towards the rails) and its four new wires */
function addPot(bb) {
  const p = bb.p, [x0] = bb.L("G", 46), [x1] = bb.L("I", 46), y0 = bb.RY(45.9), y1 = bb.RY(52.1);
  const body = svgEl(bb.parts, "g", {});
  svgEl(body, "rect", { x: x1 + 0.5 * p, y: bb.RY(47.7), width: 3.2 * p, height: 2.6 * p, rx: 0.3 * p, fill: "#c6ccd4", stroke: "#8e96a1", "stroke-width": 1.5 });
  for (let i = 0; i < 6; i++) svgEl(body, "path", { d: `M${x1 + (1.1 + i * 0.45) * p} ${bb.RY(47.8)} V${bb.RY(50.2)}`, stroke: "#8e96a1", "stroke-width": 2 });
  svgEl(body, "rect", { x: x0 - 0.5 * p, y: y0, width: x1 - x0 + p, height: y1 - y0, rx: 0.5 * p, fill: "#c9a24a", stroke: "#8a6f2c", "stroke-width": 2 });
  const lug = (r) => { const [lx, ly] = bb.L("H", r); svgEl(body, "circle", { cx: lx, cy: ly, r: 0.34 * p, fill: "#e4e8ee", stroke: "#6e7681", "stroke-width": 1 }); };
  [47, 49, 51].forEach(lug);
  const outlined = (a, b, color, bend) => {
    const [ax, ay] = bb.L(...a), [bx, by] = bb.L(...b), mx = (ax + bx) / 2, my = (ay + by) / 2;
    const g = svgEl(bb.parts, "g", {}), d = `M${ax} ${ay} Q${mx - (by - ay) * bend} ${my + (bx - ax) * bend} ${bx} ${by}`;
    svgEl(g, "path", { d, fill: "none", stroke: "#e7ebf0", "stroke-width": 0.82 * p, "stroke-linecap": "round" });
    svgEl(g, "path", { d, fill: "none", stroke: color, "stroke-width": 0.5 * p, "stroke-linecap": "round" });
    return g;
  };
  const plus = bb.wire(["H", 47], ["rp", 47], "#d0262f", 0);
  const minus = bb.wire(["H", 51], ["rm", 51], "#5b3a22", 0);
  const power = bb.wire(["D", 60], ["rp", 59], "#d0262f", 0.02);
  const signal = outlined(["H", 49], ["i", 49], "#23262c", -0.28);
  const bridges = [bb.wire(["rp", 29], ["rp", 33], "#d0262f", 0.28), bb.wire(["rm", 29], ["rm", 33], "#1d1f24", -0.28)];
  return { body, plus, minus, power, signal, bridges };
}
/** a ring around a hole, in the drawing's own coordinates */
function holeRing(bb, c, r, color) {
  const [x, y] = bb.L(c, r);
  return svgEl(bb.over, "circle", { cx: x, cy: y, r: 1.15 * bb.p, fill: "none", stroke: color, "stroke-width": 0.3 * bb.p, opacity: 0 });
}

/* ======================================================================
 * COLD OPEN: the real result, then the promise of the episode
 * ==================================================================== */
const cold = SC(); SET(cold, 0, { opacity: 1 }); SET(cold, CUT, { opacity: 0 });
title(cold, "One line of code reads this knob", "s02");
{
  const c = bigCode(cold, 210, 200, 1500, "int value = analogRead(POT_PIN);", { size: 60 });
  show(c.c, T("s02") + 2.0);
  const k = knobIcon(cold, 240, 400, 300); k.drive((t) => sweep(t, T("s02"), 5));
  hidden(k.r); show(k.r, T("s02") + 2.0);
  const m = serialMon(cold, 640, 400, 480, 440, (i, tm) => reading(sweep(tm, T("s02"), 5), i), T("s02") + 2.0, 0.1, 6, 44);
  hidden(m); show(m, T("s02") + 2.0);
  const fix = box(cold, 1180, 430, 560, 300, "card", '<div style="padding:34px;font:700 40px/1.4 var(--display)">Not working?<div style="font:600 34px/1.4 var(--ui);color:var(--muted);margin-top:16px">The number shows you where the problem is.</div></div>');
  hidden(fix); show(fix, W("s02", "when"));
}
ep07Hero("C0", 0, T("s02") + 2.0, "pot_dimmer: a hand turns the knob and the red LED follows it.", { full: true });

/* ======================================================================
 * RETRIEVAL (episode 6): answers stay hidden until they are spoken
 * ==================================================================== */
const ret = chapter("s03", "s07"); title(ret, "Two questions from episode 6", "s03");
{
  const a = bigCode(ret, 330, 170, 1260, "setColor(255, 255, 0);", { size: 64 });
  show(a.c, T("s03")); hide(a.c, T("s05") - 0.2);
  const L = rgbIcon(ret, 860, 350, 180); hidden(L.r);
  show(L.r, T("s03")); hide(L.r, T("s05") - 0.2);
  L.drive((t) => (t < T("s04") ? [0, 0, 0] : [255, 220, 0]));
  ask(ret, "QUICK QUESTION", "setColor(255, 255, 0): which color?", T("s03"), T("s04"), "Yellow: red light + green light.", { y: 720, w: 1500, t1: T("s05") - 0.2 });

  const L2 = rgbIcon(ret, 520, 220, 220); hidden(L2.r);
  show(L2.r, T("s05")); L2.drive(() => [0, 0, 0]);
  const legs = tile(ret, 900, 230, 760, 330, '<div style="font:700 38px/1.9 var(--mono)"><span style="color:#ff5d6c">Red &rarr; D25</span><br><span style="color:#4ade80">Green &rarr; D26</span><br><span style="color:#5aa9ff">Blue &rarr; D27</span></div>');
  hidden(legs); show(legs, T("s05"));
  ask(ret, "QUICK QUESTION", "All three colors go dark at once. Which wire first?", T("s05"), T("s06"), "The shared wire on the longest leg: every color returns through it.", { y: 720, w: 1500, t1: S1("s06") });
}

/* ======================================================================
 * PARTS
 * ==================================================================== */
const parts = chapter("s07", "s08"); title(parts, "What you need", "s07");
[["Episode 6 circuit", "ESP32, red LED, button, RGB", "#ffb547"], ["10 k&Omega; potentiometer", "A knob with three legs", "#19c3b4"], ["A few wires", "One of them long", "#b48cff"]].forEach(([h, d, col], i) => {
  const c = tile(parts, 115 + i * 575, 250, 540, 480, `<div style="height:230px"></div><div style="font:800 40px var(--display)">${h}</div><div style="font:600 32px/1.4 var(--ui);margin-top:16px;color:var(--muted)">${d}</div>`, col);
  hidden(c); show(c, i === 0 ? T("s07") : i === 1 ? W("s07", "ten") : W("s07", "few"));
  if (i === 1) { const k = knobIcon(c, 165, 25, 190, true); k.drive((t) => sweep(t, T("s07"), 6)); }
  if (i === 0) { const L = ledIcon(c, 215, 30, 90); L.drive(() => 0.8); }
  if (i === 2) c.insertAdjacentHTML("beforeend", '<svg width="440" height="180" viewBox="0 0 440 180" style="position:absolute;left:50px;top:50px"><path d="M20 150 C140 10 300 170 420 30" fill="none" stroke="#c7ccd4" stroke-width="10" stroke-linecap="round"/><path d="M20 100 C120 170 240 40 300 130" fill="none" stroke="#d0262f" stroke-width="10" stroke-linecap="round"/></svg>');
});

/* ======================================================================
 * THE IDEA: two answers -> how much; slide -> resistor strip -> schematic
 * ==================================================================== */
const idea = chapter("s08", "s15"); const ih = title(idea, "", "s08");
textAt(ih, [[0, "A button has two answers. A knob says how much."], [T("s09") - 0.2, "Picture a playground slide"], [T("s10") - 0.2, "Inside the knob"], [T("s11") - 0.2, "A voltage divider"], [T("s12") - 0.2, "Knob in the middle"], [T("s14") - 0.2, "The same circuit as a schematic"]]);
const ideaPos = (t) => {
  if (t < T("s11")) return sweep(t, T("s09"), 8);
  const frozen = sweep(T("s11"), T("s09"), 8);
  if (t < T("s12")) return frozen;
  if (t < W("s13", "Every")) return lerp(frozen, 0.5, (t - T("s12")) / 0.7);
  return 0.5 + 0.45 * Math.sin((t - W("s13", "Every")) * 1.3);
};
{
  // s08: two states against a scale
  const a = tile(idea, 150, 220, 760, 520, '<div style="font:800 44px var(--display)">Button</div><div style="margin-top:210px;font:700 36px/1.6 var(--mono);color:var(--muted)"><span class="p1">pressed</span> / <span class="p2">not pressed</span></div>');
  const bi = btnIcon(a, 300, 110, 170); bi.press([[T("s08"), T("s08") + 1.2], [T("s08") + 2.4, T("s08") + 3.6], [T("s08") + 4.8, T("s08") + 6]]);
  const b = tile(idea, 1010, 220, 760, 520, '<div style="font:800 44px var(--display)">Knob</div>', "var(--amber)");
  const k0 = knobIcon(b, 270, 90, 220); k0.drive((t) => sweep(t, T("s08"), 5));
  const tr = box(b, 90, 370, 580, 34, ""); css(tr, { background: "#22304d", borderRadius: "16px" });
  const fl = box(tr, 0, 0, 0, 34, ""); css(fl, { background: "var(--amber)", borderRadius: "16px" });
  dyn((t) => { fl.style.width = 580 * sweep(t, T("s08"), 5) + "px"; });
  const hm = box(b, 0, 425, 760, 60, "", '<div style="font:800 40px var(--display);color:var(--amber);text-align:center">how much?</div>');
  hidden(a); hidden(b); hidden(hm); show(a, T("s08")); show(b, W("s08", "knob")); show(hm, W("s08", "how"));
  hide([a, b, hm], T("s09") - 0.25, 0.25);

  // s09: the playground slide (analogy)
  const sl = box(idea, 90, 150, 960, 760, ""); hidden(sl); show(sl, T("s09")); hide(sl, T("s10") - 0.2, 0.25);
  const sv = svgEl(sl, "svg", { width: 960, height: 760, viewBox: "0 0 960 760" }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  svgEl(sv, "path", { d: "M170 120 V690 M240 120 V690", stroke: "#6b7a99", "stroke-width": 10 });
  for (let i = 0; i < 8; i++) svgEl(sv, "path", { d: `M170 ${180 + i * 70} H240`, stroke: "#6b7a99", "stroke-width": 8 });
  svgEl(sv, "path", { d: "M240 120 C460 180 560 560 880 660", fill: "none", stroke: "#19c3b4", "stroke-width": 28, "stroke-linecap": "round" });
  svgEl(sv, "path", { d: "M60 690 H920", stroke: "#3a4766", "stroke-width": 8 });
  txt(sv, 60, 110, "3.3 V", { "font-size": 54, fill: "#ff8a8f" });
  txt(sv, 930, 745, "ground: 0 V", { "font-size": 44, fill: "#8fa1c0", "text-anchor": "end" });
  const person = svgEl(sv, "circle", { r: 30, fill: "#ffb547", stroke: "#fff", "stroke-width": 4 });
  const bez = (u) => { const m = 1 - u; return [m * m * m * 240 + 3 * m * m * u * 460 + 3 * m * u * u * 560 + u * u * u * 880, m * m * m * 120 + 3 * m * m * u * 180 + 3 * m * u * u * 560 + u * u * u * 660]; };
  dyn((t) => { const [x, y] = bez(1 - ideaPos(t)); person.setAttribute("cx", x); person.setAttribute("cy", y - 34); });

  // s10 - s13: what actually happens, a resistor strip and a sliding contact
  const st = box(idea, 150, 160, 900, 720, ""); hidden(st); show(st, T("s10")); hide(st, T("s14") - 0.2, 0.25);
  const sg = svgEl(st, "svg", { width: 900, height: 720, viewBox: "0 0 900 720" }); css(sg, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  const yTop = 90, yBot = 630, xS = 250;
  svgEl(sg, "rect", { x: xS - 34, y: yTop, width: 68, height: yBot - yTop, rx: 16, fill: "#6e5533", stroke: "#a58f4f", "stroke-width": 4 });
  svgEl(sg, "path", { d: `M${xS} ${yTop} V30 H60`, stroke: "#ff5d6c", "stroke-width": 10, fill: "none" });
  svgEl(sg, "path", { d: `M${xS} ${yBot} V690 H60`, stroke: "#6fa0ff", "stroke-width": 10, fill: "none" });
  txt(sg, 290, 44, "outer leg: 3.3 V", { "font-size": 36, fill: "#ff8a8f" });
  txt(sg, 290, 700, "outer leg: GND", { "font-size": 36, fill: "#9dbcff" });
  const wip = svgEl(sg, "g", {});
  svgEl(wip, "path", { d: `M${xS + 44} 0 H620`, stroke: "#ffb547", "stroke-width": 10 });
  svgEl(wip, "path", { d: `M${xS + 36} 0 l34 -22 v44 z`, fill: "#ffb547" });
  txt(wip, 370, -24, "middle leg", { "font-size": 36, fill: "#ffb547" });
  dyn((t) => wip.setAttribute("transform", `translate(0 ${yBot - (yBot - yTop) * ideaPos(t)})`));
  const pk = box(idea, 1040, 520, 780, 100, "", '<div style="font:700 40px var(--ui);color:var(--amber);text-align:center">The knob picks how high up you sit.</div>'); hidden(pk); show(pk, W("s09", "knob")); hide(pk, T("s10") - 0.2, 0.25);
  const k = knobIcon(idea, 1240, 170, 300); k.drive(ideaPos); hidden(k.r); show(k.r, T("s09")); hide(k.r, T("s14") - 0.2, 0.25);
  const vb = box(idea, 1120, 510, 540, 150, "card", '<div class="v" style="font:800 84px/150px var(--mono);text-align:center;color:var(--amber)"></div>');
  hidden(vb); show(vb, T("s10")); hide(vb, T("s14") - 0.2, 0.25);
  const vt = $(".v", vb);
  dyn((t) => { const s = t >= T("s12") + 0.5 && t < T("s13") ? "? V" : (3.3 * ideaPos(t)).toFixed(2) + " V"; if (vt.__s !== s) { vt.textContent = s; vt.__s = s; } });
  const dv = pillC(idea, 700, "voltage divider", "font-size:42px;color:var(--teal)", 1000, 780); show(dv, T("s11")); hide(dv, T("s12") - 0.2, 0.25);
  const lim = box(idea, 1040, 780, 780, 150, "", '<div style="font:600 34px/1.4 var(--ui);color:#ffe3b8;text-align:center"><b style="color:var(--amber)">The difference:</b> nothing slides by itself. The contact stays where you leave it.</div>');
  hidden(lim); show(lim, W("s11", "difference")); hide(lim, T("s12") - 0.2, 0.25);
  ask(idea, "QUICK QUESTION", "Knob exactly in the middle: how many volts on the middle leg?", T("s12"), T("s13"), "About 1.65 V, half of 3.3.", { x: 1000, y: 700, w: 820, t1: S1("s13") });

  // s14: the schematic
  const sc = box(idea, 300, 160, 1320, 740, ""); hidden(sc); show(sc, T("s14"));
  const g = svgEl(sc, "svg", { width: 1320, height: 740, viewBox: "0 0 1320 740" }); css(g, { position: "absolute", left: 0, top: 0 });
  svgEl(g, "path", { d: "M360 70 V190 l-44 20 l88 40 l-88 40 l88 40 l-88 40 l88 40 l-88 40 l44 20 V680", fill: "none", stroke: "#e8eef7", "stroke-width": 10, "stroke-linejoin": "round" });
  svgEl(g, "path", { d: "M360 58 H300 M420 58 H360", stroke: "#ff5d6c", "stroke-width": 12 });
  svgEl(g, "path", { d: "M300 680 H420 M322 702 H398 M345 724 H375", stroke: "#6fa0ff", "stroke-width": 10 });
  txt(g, 460, 72, "3.3 V", { "font-size": 52, fill: "#ff8a8f" });
  txt(g, 460, 710, "GND", { "font-size": 52, fill: "#9dbcff" });
  const zig = pill(sc, -80, 300, "zigzag = resistor", "font-size:38px"); show(zig, W("s14", "zigzag"));
  const arrow = svgEl(g, "g", { opacity: 0 });
  svgEl(arrow, "path", { d: "M900 370 H440", stroke: "#ffb547", "stroke-width": 10 });
  svgEl(arrow, "path", { d: "M420 370 l40 -26 v52 z", fill: "#ffb547" });
  txt(arrow, 925, 392, "D34", { "font-size": 60, fill: "#ffb547", "font-family": "Consolas" });
  txt(arrow, 470, 340, "arrow = sliding contact", { "font-size": 38, fill: "#ffe3b8" });
  TO(arrow, W("s14", "arrow"), 0.4, { opacity: 1, ease: "power1.out" });
}

/* ======================================================================
 * WIRING: the creator's real layout, then the real clip next to the drawing
 * ==================================================================== */
const wire = chapter("s15", "s18"); const wh = title(wire, "Wire the knob", "s15"); css(wh, { zIndex: 35, background: "#0b1220" });
{
  const bb = deskCircuit(wire, 90, 17, 26, 160);
  bb.led.drive(() => 0);
  const pot = addPot(bb);
  const parts_ = [pot.body, pot.plus, pot.minus, pot.power, pot.signal, ...pot.bridges];
  parts_.forEach((e) => gsap.set(e, { opacity: 0 }));
  show(pot.body, W("s15", "knob"));
  show([pot.plus, pot.power], W("s15", "plus"));
  show(pot.minus, W("s15", "minus"));
  show(pot.signal, W("s16", "long"));
  show(pot.bridges, W("s16", "bridge"));
  const r34 = holeRing(bb, "i", 49, "#ffb547"); TO(r34, W("s16", "D"), 0.4, { opacity: 1 }); TO(r34, T("s17") - 0.2, 0.3, { opacity: 0 });
  const r3 = holeRing(bb, "D", 60, "#4ade80"); TO(r3, T("s17"), 0.4, { opacity: 1 });
  const rv = holeRing(bb, "j", 60, "#ff5d6c"); TO(rv, W("s17", "never"), 0.4, { opacity: 1 });

  const usb = box(wire, 840, 190, 960, 96, "", '<div class="banner" style="position:static;display:inline-flex">USB unplugged</div>'); hidden(usb); show(usb, T("s15")); hide(usb, T("s16") - 0.2, 0.25);
  const steps = [["Knob: right board, below the LED", "knob"], ["One outer leg &rarr; <b style=\"color:#ff5d6c\">+ rail</b>", "plus"], ["Other outer leg &rarr; <b style=\"color:#6fa0ff\">&minus; rail</b>", "minus"]];
  steps.forEach(([txt_, w], i) => {
    const c = box(wire, 840, 310 + i * 130, 960, 110, "card", `<div style="font:700 40px/110px var(--ui);padding-left:34px;white-space:nowrap">${txt_}</div>`);
    hidden(c); show(c, W("s15", w)); hide(c, T("s16") - 0.2, 0.25);
  });
  const lb = box(wire, 840, 720, 960, 90, "", '<div style="font:700 38px var(--ui);color:var(--amber);text-align:center">Middle leg &rarr; D34. Rails split? Add the bridges.</div>');
  hidden(lb); show(lb, W("s16", "long")); hide(lb, T("s17") - 0.2, 0.25);

  const rule = tile(wire, 840, 240, 960, 500, '<div style="font:800 52px var(--display)">The + rail is 3.3 V</div><div style="font:800 56px/1.6 var(--mono);margin-top:40px"><span style="color:#4ade80">3V3 &check;</span><br><span style="color:#ff5d6c">VIN (5 V) &times;</span></div><div style="font:600 34px/1.4 var(--ui);margin-top:30px;color:var(--muted)">An ESP32 input can only take 3.3 V.</div>', "var(--red)");
  hidden(rule); show(rule, T("s17"));
}
ep07Hero("C1", T("s16"), T("s17") - 0.35, "The knob and its wires going in, played from the creator's removal take.", { x: 840, y: 190, w: 960, h: 520 });

/* ======================================================================
 * analogRead: a ruler along the slide, the real function, its limit
 * ==================================================================== */
const rd = chapter("s18", "s21"); title(rd, "analogRead(): volts become a number", "s18");
{
  const pos = (t) => sweep(t, T("s18"), 7);
  const code = bigCode(rd, 260, 170, 1400, "int value = analogRead(POT_PIN);", { size: 58 }); show(code.c, T("s18"));
  const r = ruler(rd, 210, 340, 1500, pos); hidden(r); show(r, W("s18", "ruler") - 0.2); hide(r, T("s20") - 0.2, 0.25);
  const mp = box(rd, 300, 590, 1320, 240, "", '<div style="display:flex;gap:40px;justify-content:center"><div class="card" style="position:static;padding:30px 50px;font:800 56px var(--mono);white-space:nowrap">0 V &rarr; <span style="color:var(--amber)">0</span></div><div class="card" style="position:static;padding:30px 50px;font:800 56px var(--mono);white-space:nowrap">3.3 V &rarr; <span style="color:var(--amber)">4095</span></div></div>');
  hidden(mp); show(mp, T("s19")); hide(mp, T("s20") - 0.2, 0.25);
  const nowv = box(rd, 460, 590, 1000, 120, "", '<div class="n" style="font:800 72px var(--mono);text-align:center;color:var(--teal)"></div>');
  hidden(nowv); show(nowv, W("s18", "ruler")); hide(nowv, T("s19") - 0.2, 0.25);
  const nv = $(".n", nowv);
  dyn((t) => { const s = (3.3 * pos(t)).toFixed(2) + " V  →  " + Math.round(4095 * pos(t)); if (nv.__s !== s) { nv.textContent = s; nv.__s = s; } });

  // s20: the imperfect ruler
  const gr = box(rd, 250, 320, 1420, 560, ""); hidden(gr); show(gr, T("s20"));
  const g = svgEl(gr, "svg", { width: 1420, height: 560, viewBox: "0 0 1420 560" }); css(g, { position: "absolute", left: 0, top: 0 });
  svgEl(g, "path", { d: "M120 30 V490 H1000", stroke: "#3a4766", "stroke-width": 6, fill: "none" });
  svgEl(g, "path", { d: "M120 490 L1000 40", stroke: "#5f6f8f", "stroke-width": 6, "stroke-dasharray": "16 14", fill: "none" });
  svgEl(g, "path", { d: "M120 490 H170 C210 490 220 462 260 442 L880 112 C930 84 950 40 1000 40", stroke: "#ffb547", "stroke-width": 10, fill: "none", "stroke-linecap": "round" });
  txt(g, 560, 545, "volts on the pin", { "font-size": 34, "text-anchor": "middle" });
  txt(g, 0, 50, "4095", { "font-size": 36, fill: "#ffb547", "font-family": "Consolas" });
  txt(g, 40, 500, "0", { "font-size": 36, fill: "#ffb547", "font-family": "Consolas" });
  const fl = tile(gr, 1040, 120, 380, 280, '<div style="font:700 36px/1.4 var(--ui)">Flat near both ends</div><div style="font:600 30px/1.4 var(--ui);color:var(--muted);margin-top:18px">You may never see exactly 0 or 4095.</div>', "var(--amber)");
  hidden(fl); show(fl, W("s20", "flattens"));
}

/* ---- code tour: pot_read ---- */
const runr = chapter("s23", "s24"); title(runr, "Turn the knob and watch the number", "s23");
{
  const pos = (t) => sweep(t, W("s23", "As"), 8);
  const k = knobIcon(runr, 180, 260, 380); k.drive(pos);
  serialMon(runr, 660, 200, 620, 690, (i, tm) => reading(pos(tm), i), W("s23", "As") - 0.3, 0.1, 11, 42);
  const r = box(runr, 1340, 300, 460, 400, "card", '<div style="padding:28px;font:700 34px var(--ui);color:var(--muted)">now<div class="n" style="font:800 84px var(--mono);color:var(--amber);margin-top:24px"></div><div style="font:600 32px/1.5 var(--ui);margin-top:30px">Bottom of the scale: 0<br>Top of the scale: 4095</div></div>');
  const n = $(".n", r); dyn((t) => { const s = String(reading(pos(t), Math.floor(t * 10))); if (n.__s !== s) { n.textContent = s; n.__s = s; } });
}
tour("pot_read", T("s21") - 0.4, W("s23", "As") - 0.3, [
  [T("s21"), "const int POT_PIN"], [W("s21", "setup"), "void setup", "Serial.begin"], [W("s21", "pin", 2), null],
  [T("s22"), "int value = analogRead"], [W("s22", "print"), "Serial.println(value)"], [W("s22", "wait"), "delay(100)"], [W("s22", "Pause"), "int value = analogRead"]]);
askTop(stage, "PAUSE AND PREDICT", "Knob in the middle: what number do you expect?", W("s22", "Pause"), T("s23"), "Around 2000: half of the scale.", { x: 210, y: 790, w: 1500, t1: W("s23", "As") - 0.3 });

/* ======================================================================
 * THE DIMMER: two scales, one division
 * ==================================================================== */
const dm = chapter("s24", "s26"); title(dm, "Two scales that don't fit", "s24");
{
  const big = scaleBar(dm, 180, 320, 1560, "#ffb547", "the knob gives", "0 .. 4095");
  const small = scaleBar(dm, 180, 540, 98, "#ff5d6c", "analogWrite() takes", "");
  const lab = box(dm, 300, 540, 500, 96, "", '<div style="font:800 40px/96px var(--mono);color:#ff8a8f">0 .. 255</div>');
  hidden(big.b); hidden(big.l); hidden(small.b); hidden(small.l); hidden(lab);
  show([big.b, big.l], W("s24", "knob")); show([small.b, small.l, lab], W("s24", "Analog"));
  TO(big.b, T("s25") + 0.8, 1.4, { width: 98, ease: "power2.inOut" });
  const lb = box(dm, 300, 320, 700, 96, "", '<div style="font:800 40px/96px var(--mono);color:#ffb547">4095 / 16 &asymp; 255</div>');
  hidden(lb); show(lb, T("s25") + 2.0);
  styleAt(big.b, "color", [[0, "#0b1220"], [T("s25") + 0.8, "transparent"]]);
  ask(dm, "QUICK QUESTION", "0 .. 4095 into 0 .. 255: how do we make that fit?", W("s24", "Quick"), T("s25"), "We divide by 16: both ends land on both ends.", { y: 700, w: 1500, t1: S1("s25") });
}
tour("pot_dimmer", T("s26") - 0.4, S1("s28") + 0.3, [
  [T("s26"), "int value = analogRead"], [W("s26", "divide"), "int brightness = value / 16"], [W("s26", "Analog"), "analogWrite(LED_PIN, brightness)"],
  [T("s27"), "int brightness = value / 16"]]);
askTop(stage, "PAUSE AND PREDICT", "What if we divided by 32 instead?", T("s27"), T("s28"), "The biggest number would be about 127: about half power at most.", { x: 210, y: 790, w: 1500, t1: S1("s28") + 0.2 });
ep07Hero("C2", T("s29"), T("s30") - 0.35, "pot_dimmer with a meter on the middle leg: 0.00 to 3.33 V, and the LED follows.", { full: true });

/* ======================================================================
 * ZONES: one number, three choices
 * ==================================================================== */
const zn = chapter("s30", "s33"); title(zn, "One number, three choices", "s30"); likeTop(T("s30") + 0.4);
{
  const X = 180, Wd = 1560, cut = (v) => X + Wd * v / 4095;
  const bar = box(zn, X, 400, Wd, 110, ""); hidden(bar); show(bar, T("s31"));
  css(bar, { display: "flex", borderRadius: "14px", overflow: "hidden", font: "800 40px/110px var(--ui)", textAlign: "center", color: "#0b1220" });
  bar.innerHTML = '<div style="flex:1;background:#7a3b3f;color:#fff">dim</div><div style="flex:1;background:#c7535b;color:#fff">medium</div><div style="flex:1;background:#ff5d6c">full</div>';
  [[0, "0"], [1365, "1365"], [2730, "2730"], [4095, "4095"]].forEach(([v, s], i) => {
    const l = box(zn, cut(v) - 120, 520, 240, 60, "", `<div style="font:800 42px var(--mono);text-align:center;color:var(--amber)">${s}</div>`);
    hidden(l); show(l, i === 1 ? W("s31", "cut") : i === 2 ? W("s31", "cut") + 1.2 : T("s31"));
  });
  const eq = pillC(zn, 240, "4095 / 3 &asymp; 1365", "font-size:48px;font-family:var(--mono)"); show(eq, W("s31", "divided") - 0.3);
  const lead = box(zn, 300, 640, 1320, 100, "", '<div style="font:600 36px var(--ui);text-align:center;color:var(--muted)">The knob still gives one number. Our code sorts it.</div>');
  hidden(lead); show(lead, T("s31"));
  exCard("🍳", "The marks on a stove", "Low, medium and high: a few choices instead of every value.", T("s30"), T("s31") - 0.25);
  exCard("🍳", "No clicks on this knob", "The zones exist only in the code.", T("s32"), T("s33") - 0.3);
}
tour("pot_zones", T("s33") - 0.4, S1("s35") + 0.3, [
  [W("s33", "Below"), "if (value < 1365)", "analogWrite(LED_PIN, 20)"], [W("s33", "Else"), "else if (value < 2730)", "analogWrite(LED_PIN, 120)"], [W("s33", "Otherwise"), "} else {", "analogWrite(LED_PIN, 255)"],
  [T("s34"), "if (value < 1365)"], [T("s35"), "else if (value < 2730)"]]);
askTop(stage, "PAUSE AND PREDICT", "The reading is exactly 1365. Which zone?", T("s34"), T("s35"), "The middle one: 1365 is not less than 1365.", { x: 560, y: 790, w: 1180, t1: S1("s35") + 0.2 });

/* s36: no clip was filmed for pot_zones; the same LED and knob, in the three steps of the sketch */
const rz = chapter("s36", "s37"); title(rz, "Dim, medium, full", "s36");
{
  const pos = (t) => sweep(t, T("s36") - 0.2, 8.2);
  const value = (t) => reading(pos(t), Math.floor(t * 10));
  const zone = (t) => (value(t) < 1365 ? 0 : value(t) < 2730 ? 1 : 2);
  const k = knobIcon(rz, 170, 300, 380); k.drive(pos);
  const L = ledIcon(rz, 770, 240, 220); L.drive((t) => [20 / 255 + 0.08, 120 / 255, 1][zone(t)]);
  const c = box(rz, 1190, 250, 640, 200, "card", '<div style="padding:30px;font:700 30px var(--ui);color:var(--muted)">analogRead<div class="n" style="font:800 80px var(--mono);color:var(--amber);margin-top:10px"></div></div>');
  const n = $(".n", c); dyn((t) => { const s = String(value(t)); if (n.__s !== s) { n.textContent = s; n.__s = s; } });
  const w = box(rz, 1190, 480, 640, 200, "card", '<div style="padding:30px;font:700 30px var(--ui);color:var(--muted)">analogWrite<div class="n" style="font:800 80px var(--mono);color:#ff8a8f;margin-top:10px"></div></div>');
  const m = $(".n", w); dyn((t) => { const s = String([20, 120, 255][zone(t)]); if (m.__s !== s) { m.textContent = s; m.__s = s; } });
  const tags = ["dim", "medium", "full"].map((s, i) => { const e = box(rz, 1190 + i * 215, 710, 205, 90, "", `<div style="font:800 38px/90px var(--ui);text-align:center;border-radius:14px;background:#16203a">${s}</div>`); return e; });
  dyn((t) => tags.forEach((e, i) => { e.style.opacity = i === zone(t) ? "1" : ".3"; }));
}

/* ======================================================================
 * A CALMER READING
 * ==================================================================== */
const sm = chapter("s37", "s40"); title(sm, "Why does the number wobble?", "s37");
{
  const base = 2044, noisy = (i) => base + Math.round((nz(i, 5) - 0.5) * 34);
  const num = box(sm, 180, 260, 700, 260, "card", '<div style="padding:30px;font:700 34px var(--ui);color:var(--muted)">knob untouched<div class="n" style="font:800 120px var(--mono);color:var(--amber);margin-top:14px"></div></div>');
  const n = $(".n", num); dyn((t) => { const s = String(noisy(Math.floor(t * 8))); if (n.__s !== s) { n.textContent = s; n.__s = s; } });
  const sc = tile(sm, 980, 260, 760, 260, '<div style="display:flex;gap:30px;align-items:center"><div style="font-size:120px;line-height:1">⚖️</div><div style="font:700 38px/1.35 var(--ui)">A bathroom scale that never quite settles</div></div>', "var(--amber)");
  hidden(sc); show(sc, W("s37", "bathroom")); hide(sc, T("s38") - 0.2, 0.25);
  const noise = tile(sm, 980, 260, 760, 260, '<div style="font:800 42px var(--display)">Electrical noise</div><div style="font:600 34px/1.4 var(--ui);margin-top:16px;color:var(--muted)">Tiny noise changes every single reading.</div>', "var(--red)");
  hidden(noise); show(noise, T("s38"));
  const row = box(sm, 180, 590, 1560, 230, ""); hidden(row); show(row, W("s38", "measure"));
  row.innerHTML = [2051, 2038, 2047, 2040].map((v, i) => `<div class="card" style="position:absolute;left:${i * 250}px;top:0;width:220px;height:130px;font:800 56px/130px var(--mono);text-align:center">${v}</div>`).join("") +
    '<div style="position:absolute;left:1010px;top:0;width:550px;height:130px;border-radius:18px;border:3px solid var(--teal);font:800 50px/130px var(--mono);text-align:center;color:var(--teal)">avg = 2044</div>' +
    '<div style="position:absolute;left:0;top:160px;width:1560px;font:600 36px var(--ui);text-align:center;color:var(--muted)">Measure four times, and take the average.</div>';
  exCard("⏱️", "Not like a real scale", "Four readings take well under a millisecond, so you lose no time.", T("s39"), T("s40") - 0.3);
}
/* s41: the Serial Plotter */
const pl = chapter("s41", "s42"); title(pl, "Serial Plotter: raw against average", "s41");
{
  const X = 160, Y = 190, Wd = 1600, H = 620;
  const c = box(pl, X, Y, Wd, H, "card", "");
  const g = svgEl(c, "svg", { width: Wd, height: H, viewBox: `0 0 ${Wd} ${H}` }); css(g, { position: "absolute", left: 0, top: 0 });
  for (let i = 1; i < 5; i++) svgEl(g, "path", { d: `M40 ${i * H / 5} H${Wd - 40}`, stroke: "#22304d", "stroke-width": 2 });
  const raw = svgEl(g, "path", { fill: "none", stroke: "#5aa9ff", "stroke-width": 3, opacity: 0.8 }), avg = svgEl(g, "path", { fill: "none", stroke: "#ffb547", "stroke-width": 8 });
  const y = (v) => H / 2 - (v - 2044) * 8;
  const line = (t, f) => { let d = ""; const n0 = Math.floor(t * 20) - 120; for (let i = 0; i <= 120; i++) { const k = n0 + i; d += (i ? "L" : "M") + (40 + (Wd - 80) * i / 120).toFixed(1) + " " + y(f(k)).toFixed(1); } return d; };
  const fR = (k) => 2044 + (nz(k, 5) - 0.5) * 50, fA = (k) => 2044 + (nz(k, 5) + nz(k + 0.25, 7) + nz(k + 0.5, 9) + nz(k + 0.75, 11) - 2) / 4 * 30;
  dyn((t) => { if (t < T("s41") - 1 || t > T("s42")) return; raw.setAttribute("d", line(t, fR)); avg.setAttribute("d", line(t, fA)); });
  const la = pill(pl, 210, 215, "raw: one reading", "color:#5aa9ff"), lb = pill(pl, 620, 215, "avg: the average of 4", "color:#ffb547");
  show(la, W("s41", "single")); show(lb, W("s41", "average", 2));
}
tour("pot_smooth", T("s40") - 0.4, T("s41") + 1.0, [
  [W("s40", "sum"), "int sum = 0"], [W("s40", "for"), "for (int i = 0", "sum = sum + analogRead"], [W("s40", "Then"), "int avg = sum / 4"], [T("s40b"), "Serial.print(\"raw:\")", "Serial.println(avg)"]]);
askTop(stage, "PAUSE AND PREDICT", "On a graph, which line jitters less: single reading or average?", T("s40b"), T("s41"), "The average.", { x: 210, y: 790, w: 1500, t1: T("s41") + 0.9 });

/* ======================================================================
 * THE COMMON PROBLEM: print first
 * ==================================================================== */
const mk = chapter("s42", "s45"); title(mk, "The LED doesn't react. Now what?", "s42");
{
  const k = knobIcon(mk, 200, 210, 340); k.drive((t) => sweep(t, T("s42"), 4));
  const L = ledIcon(mk, 720, 190, 170); L.drive(() => 0);
  const x = box(mk, 660, 560, 300, 70, "", '<div style="font:800 40px var(--ui);color:#ff8a8f;text-align:center">still dark</div>');
  const parts2 = box(mk, 1090, 240, 680, 340, "", ["LED?", "knob?", "code?"].map((s, i) => `<div class="card" style="position:absolute;left:0;top:${i * 110}px;width:680px;height:92px;font:800 46px/92px var(--ui);text-align:center">${s}</div>`).join(""));
  hidden(parts2); show(parts2, W("s42", "Quick")); hide(parts2, T("s44") - 0.2, 0.25);
  hide([k.r, L.r, x], T("s44") - 0.2, 0.25);
  ask(mk, "QUICK QUESTION", "Is it the LED, the knob, or the code? What would you do first?", W("s42", "Quick"), T("s43"), "<span style=\"font-family:var(--mono)\">Serial.println(value);</span> Print it before you trust anything.", { y: 690, w: 1500, t1: T("s44") - 0.2 });
  exCard("🌡️", "Temperature first, then medicine", "The print line is your thermometer.", W("s43", "doctor") - 0.1, T("s44") - 0.25);

  // s44: the number splits the search in half
  const a = tile(mk, 130, 210, 800, 540, '<div style="font:800 40px var(--display);color:#ff8a8f">Stuck at 0 or at the top</div><div style="height:300px"></div><div style="font:700 36px/1.4 var(--ui)">The knob side: a loose wire, or a rail gap at the knob.</div>', "var(--red)");
  serialMon(a, 60, 110, 680, 260, () => 0, T("s44"), 0.1, 3, 42);
  const b = tile(mk, 990, 210, 800, 540, '<div style="font:800 40px var(--display);color:#4ade80">Moves normally</div><div style="height:300px"></div><div style="font:700 36px/1.4 var(--ui)">The knob is fine. Look at the LED side.</div>', "#4ade80");
  serialMon(b, 60, 110, 680, 260, (i, tm) => reading(0.5 + 0.42 * Math.sin((tm - T("s44")) * 1.1), i), T("s44"), 0.1, 3, 42);
  hidden(a); hidden(b); show(a, W("s44", "Stuck")); show(b, W("s44", "If"));
  exCard("🌡️", "A thermometer takes no time. A print does.", "Too many prints can slow a fast loop. Remove them when you're done.", T("s44b"), T("s45") - 0.3);
}

/* ======================================================================
 * PIN RULES: the board itself, three kinds of pin
 * ==================================================================== */
const pn = chapter("s45", "s48"); title(pn, "Pins aren't all equal", "s45");
{
  const LP = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"];
  const RP = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"];
  const X = 200, Y = 160, rowH = 48;
  const bd = box(pn, X + 170, Y, 400, 15 * rowH + 20, ""); css(bd, { background: "#1b1f26", border: "2px solid #2b313b", borderRadius: "16px" });
  const chip = box(bd, 90, 30, 220, 240, ""); css(chip, { background: "#c9ced6", borderRadius: "6px", font: "800 34px/240px var(--ui)", textAlign: "center", color: "#5d6670" }); chip.textContent = "ESP32";
  const chipOf = {};
  const mkPin = (nm, x, y, right) => {
    const e = box(pn, x, y, 160, rowH - 6, "", `<div style="font:700 28px/${rowH - 6}px var(--mono);text-align:center;border-radius:8px;background:#141c30;color:#c9d1dc;border:2px solid transparent">${nm}</div>`);
    (chipOf[nm] = chipOf[nm] || []).push(e.firstChild);
  };
  LP.forEach((n, i) => mkPin(n, X, Y + 10 + i * rowH, false));
  RP.forEach((n, i) => mkPin(n, X + 580, Y + 10 + i * rowH, true));
  const paint = (names, col, t0, t1) => dyn((t) => names.forEach((n) => (chipOf[n] || []).forEach((e) => { const on = t >= t0 && (t1 == null || t < t1); if (on) { e.style.background = col; e.style.color = "#0b1220"; } })));
  const reset = () => dyn((t) => Object.values(chipOf).flat().forEach((e) => { e.style.background = "#141c30"; e.style.color = "#c9d1dc"; }));
  reset();
  paint(["VP", "VN", "D34", "D35"], "#19c3b4", W("s45", "thirty-four", 2), T("s46") - 0.1);
  paint(["D25", "D26", "D27"], "#ffb547", W("s46", "twenty-five"), T("s47") - 0.1);
  paint(["D34"], "#4ade80", W("s46", "Pin"), T("s47") - 0.1);
  paint(["D2", "D5", "D12", "D15"], "#ff8a8f", W("s47", "pins"), null);
  const c1 = tile(pn, 1010, 200, 800, 420, '<div style="font-size:90px;line-height:1">🚪</div><div style="font:800 44px var(--display);margin-top:20px;color:#19c3b4">34 .. 39: one-way doors</div><div style="font:600 36px/1.4 var(--ui);margin-top:18px">They can only listen. They can\'t drive an LED.</div>', "#19c3b4");
  hidden(c1); show(c1, W("s45", "thirty-four", 2)); hide(c1, T("s46") - 0.2, 0.25);
  const c2 = tile(pn, 1010, 200, 800, 420, '<div style="font:800 44px var(--display);color:var(--amber)">25 .. 27: no analogRead with Wi-Fi on</div><div style="font:600 36px/1.4 var(--ui);margin-top:26px"><b style="color:#4ade80">Pin 34 keeps working</b>, so our sensors live there.</div>', "var(--amber)");
  hidden(c2); show(c2, T("s46")); hide(c2, T("s47") - 0.2, 0.25);
  const c3 = tile(pn, 1010, 200, 800, 460, '<div style="font:800 44px var(--display);color:#ff8a8f">0, 2, 5, 12, 15: checked at power-on</div><div style="font:600 36px/1.4 var(--ui);margin-top:22px">We leave them free. Pin 0 is the board\'s BOOT button.</div><div style="font:700 34px/1.4 var(--ui);margin-top:30px;color:var(--teal)">No need to memorize: the full pin map is in the lesson folder.</div>', "var(--red)");
  hidden(c3); show(c3, T("s47"));
}

/* ======================================================================
 * EXPLAIN, CHALLENGE, OUTRO
 * ==================================================================== */
const ex = chapter("s48", "s50"); title(ex, "In your own words", "s48");
{
  const li = bigCode(ex, 360, 480, 1200, "int brightness = value / 16;", { size: 54 }); show(li.c, T("s48")); hide(li.c, T("s49") - 0.2, 0.25);
  const big = scaleBar(ex, 180, 620, 1560, "#ffb547", "knob", "0 .. 4095");
  const small = scaleBar(ex, 180, 800, 98, "#ff5d6c", "brightness", "");
  const lab = box(ex, 300, 800, 500, 96, "", '<div style="font:800 40px/96px var(--mono);color:#ff8a8f">0 .. 255</div>');
  hidden(big.b); hidden(big.l); hidden(small.b); hidden(small.l); hidden(lab);
  show([big.b, big.l, small.b, small.l, lab], T("s49"));
  ask(ex, "PAUSE AND EXPLAIN", "Why do we divide by 16? One sentence is enough.", T("s48"), T("s49"), "The knob's scale is 16 times bigger than the brightness scale, so dividing makes them match.", { x: 210, y: 210, w: 1500, t1: S1("s49") });
  likeTop(T("s49") + 0.3);
}
const ch = chapter("s50", "s52"); title(ch, "Your turn: Knob Blink Speed", "s50");
{
  [["left zone", 100], ["middle zone", 400], ["right zone", 1000]].forEach(([z, ms], i) => {
    const c = tile(ch, 115 + i * 575, 200, 540, 440, `<div style="font:700 36px var(--ui);color:var(--muted);text-align:center">${z}</div><div style="height:210px"></div><div style="font:800 52px var(--mono);text-align:center;color:var(--amber)">${ms} ms</div>`);
    hidden(c); show(c, W("s50", "knob") + i * 0.4);
    const L = ledIcon(c, 215, 90, 100); L.drive((t) => blink(t, 0, ms / 1000, ms / 1000));
  });
  const tw = tile(ch, 130, 680, 1660, 190, '<div style="font:800 42px var(--display);color:var(--amber)">The twist: no delay()</div><div style="font:600 36px/1.4 var(--ui);margin-top:14px">Today\'s zones choose the interval. The millis() trick from episode 4 does the blinking.</div>', "var(--amber)");
  hidden(tw); show(tw, T("s51"));
}
const out = chapter("s52", null); title(out, "Three things you can now explain", "s52");
{
  [["Position &rarr; voltage", "The knob", T("s52") + 2.0], ["Voltage &rarr; number", "analogRead()", W("s52", "Analog")], ["Number &rarr; the problem", "Print it first", W("s52", "printing")]].forEach(([a, b, t0], i) => {
    const c = tile(out, 115 + i * 575, 230, 540, 340, `<div style="font:800 42px var(--display);color:var(--teal)">${a}</div><div style="font:700 38px/1.5 var(--mono);margin-top:40px">${b}</div>`);
    hidden(c); show(c, t0); hide(c, T("s53") - 0.15, 0.25);
  });
  const next = tile(out, 210, 200, 1500, 400, '<div class="kicker">NEXT: EPISODE 8</div><div style="font:800 62px var(--display);margin-top:26px">A function that divides for us</div><div style="font:600 36px var(--ui);margin-top:20px;color:var(--muted)">...and a bar of LEDs that fills up as you turn.</div>');
  hidden(next); show(next, T("s53"));
  const bar = box(next, 1040, 170, 400, 180, "");
  [["#4ade80", 0], ["#ffe14d", 1], ["#ff5d6c", 2]].forEach(([c, i]) => {
    const d = box(bar, i * 130, 40, 100, 100, ""); css(d, { borderRadius: "50%", background: c });
    dyn((t) => { d.style.opacity = sweep(t, T("s53"), 4) * 3 > i ? "1" : ".15"; });
  });
  note(out, "Post your blink speed code in the comments. One solution is in the lesson folder.", W("s53", "Post"), 650);
  note(out, "github.com/emjnbulut/esp32-from-zero &rarr; lessons/07-analog-input", W("s53", "Post"), 790);
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 }); TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}
window.__seek(0);
window.__ready = true;
