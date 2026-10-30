/* Episode 6 RGB Color Mixing: segment-anchored scenes, creator footage C0-C4, and complete-code tours. */
const stage = $("#stage");
const EP06_CLIP_SECONDS = {"C0": 14.966667, "C1": 10.1, "C2": 15.033333, "C3": 14.8, "C4": 15.6};
function ep06Hero(id, t0, requestedEnd, description, opts = {}) {
  const lead = opts.full ? Math.min(0.3, t0) : 0;
  const tail = opts.full ? 0.35 : 0;
  const t1 = Math.min(requestedEnd, t0 + EP06_CLIP_SECONDS[id] - lead - tail - 1 / 30);
  if (!(t1 > t0)) throw new Error('No usable episode 6 footage: ' + id);
  return heroClip(stage, id, t0, t1, description, opts);
}

const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const hidden = (e) => { gsap.set(e, { opacity: 0 }); return e; };
const CUT = S0("s03") - 0.1; // the channel sting is inserted here (tools/bumpers.py cut(), script "sting_after": "s03")
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


function chapter(first,next) {
 const sc=SC();span(sc,Math.max(0,T(first)-0.45),next?T(next)-0.45:null);return sc;
}
function title(sc,text,id){const h=head(sc,text);show(h,T(id));return h;}
function note(sc,text,id,y=840){
 const n=box(sc,130,y,1660,100,"",'<div style="font:600 32px/1.4 var(--ui);text-align:center;color:var(--muted)">'+text+'</div>');
 hidden(n);pop(n,T(id));return n;
}
function tile(sc,x,y,w,h,text,col="var(--teal)"){
 return box(sc,x,y,w,h,"card",'<div style="padding:32px;border-top:4px solid '+col+';border-radius:20px;height:100%;box-sizing:border-box">'+text+'</div>');
}
const repo="Full code: <b>github.com/emjnbulut/esp32-from-zero</b> &rarr; lessons/06-rgb";
function tour(file,first,last,marks){return fullCode(stage,file+".ino",SKETCHES[file],T(first)-0.4,S1(last)+0.2,repo,marks);}

// Clip caps include compose fades and one extra frame of physical-source margin.
// Cold open: the real result fills the frame.
const cold=SC();SET(cold,0,{opacity:1});SET(cold,CUT,{opacity:0});
title(cold,"One LED. Your colors.","s01");
ep06Hero("C0",0,Math.min(CUT-0.2,14.5),"color_modes: red, green, blue, then a slow blue-red fade.",{full:true});

// Recall: two answers remain hidden until their spoken answer segments.
const ret=chapter("s03","s07");title(ret,"Quick recall: PWM and the loop","s03");
{
 const a=bigCode(ret,240,230,1440,"analogWrite(LED_PIN, 128);",{size:54});
 show(a.c,T("s03"));hide(a.c,T("s05")-0.2);
 const L=ledIcon(ret,850,450,130);hidden(L.r);show(L.r,T("s04"));hide(L.r,T("s05")-0.2);L.drive(()=>0.5);
 ask(ret,"QUICK QUESTION","What does a value of <b>128</b> actually do to the pin?",T("s03"),T("s04"),
 "About half of every fast cycle is ON. The pin is never halfway on.",{y:750,w:1500,t1:T("s05")-0.2});
 const c=bigCode(ret,240,230,1440,"if (now - lastStep >= 4) {\n  // take one fade step\n}\n// read the button again",{size:44});
 show(c.c,T("s05"));
 ask(ret,"QUICK QUESTION","Without delay(), why can the button react at any moment?",T("s05"),T("s06"),
 "The loop checks the clock, moves on, and reads the button on every round.",{y:750,w:1500,t1:S1("s06")});
}

const parts=chapter("s07","s08");title(parts,"Keep the episode 5 circuit; add RGB","s07");
[["1","Existing circuit","ESP32, red LED and button","#ffb547"],["2","One RGB LED","Four legs; check the common leg","#b48cff"],["3","Three resistors","220 &Omega; for EACH color","#19c3b4"]].forEach(([n,h,d,col],i)=>{
 const c=tile(parts,115+i*575,250,540,400,'<div style="font:800 88px var(--display);color:'+col+'">'+n+'</div><div style="font:800 42px var(--display);margin-top:25px">'+h+'</div><div style="font:600 32px/1.4 var(--ui);margin-top:18px;color:var(--muted)">'+d+'</div>',col);
 hidden(c);pop(c,T("s07")+i*0.2);
});
note(parts,"Unplug the USB cable before changing the wiring.","s07");

// RGB: screen analogy, objective package view, light/paint distinction.
const rgb=chapter("s08","s11");title(rgb,"Three tiny LEDs in one package","s08");
{
 const L=rgbIcon(rgb,380,220,220);
 L.drive(t=>t<T("s09")?[255,255,255]:t<W("s09","green")?[255,0,0]:t<W("s09","blue")?[0,255,0]:[0,0,255]);
 [["Red","#ff5d6c"],["Common: the longest leg","#e8eef7"],["Green","#4ade80"],["Blue","#5aa9ff"]].forEach(([txt,col],i)=>{
 const p=pill(rgb,800,250+i*100,txt,"font-size:38px;color:"+col);pop(p,T("s09")+i*0.15);});
 exCard("\uD83D\uDCF1","Zoom in on a phone screen","Tiny red, green and blue lights combine into the colors you see.",T("s08"),T("s09")-0.25);
 const mix=box(rgb,150,730,1620,170,"");
 mix.innerHTML=[["RED + GREEN","yellow","#ffe14d"],["RED + BLUE","magenta","#ff68ff"],["ALL THREE","white","#fff"]].map(([a,b,c],i)=>'<div style="position:absolute;left:'+i*550+'px;width:510px;border-radius:20px;border:2px solid '+c+';padding:24px;box-sizing:border-box;text-align:center"><div style="font:700 30px var(--mono)">'+a+'</div><div style="font:800 42px var(--display);color:'+c+';margin-top:12px">'+b+'</div></div>').join("");
 hidden(mix);pop(mix,T("s10"));note(rgb,"Light adds up. The same colors of paint behave differently.","s10",930);
}

// Wiring: full-frame real assembly, then a readable circuit map.
const wire=chapter("s11","s18");const wh=title(wire,"Three pins. Three resistors. One return path.","s11"); css(wh,{zIndex:35,background:"#0b1220"});
{
 const bb=deskCircuit(wire,120,13,17,170);
 const [cx,cy]=bb.L("c",21);
 svgEl(bb.parts,"rect",{x:cx-22,y:cy-58,width:44,height:49,rx:20,fill:"#e8edf3",stroke:"#98a5b8","stroke-width":2});
 [20,21,22,23].forEach(r=>{const [x,y]=bb.L("c",r);svgEl(bb.parts,"path",{d:"M"+(cx+(r-21.5)*8)+" "+(cy-10)+" L"+x+" "+y,stroke:"#c3c9d1","stroke-width":3,fill:"none"});});
 [["#ff5d6c",20,53],["#4ade80",22,54],["#5aa9ff",23,55]].forEach(([col,row,pinrow])=>{
 const [x,y]=bb.L("a",row),[px,py]=bb.L("i",pinrow),bend=175+(row-20)*26;
 svgEl(bb.parts,"path",{d:"M"+px+" "+py+" H"+bend+" V"+y+" H"+x,stroke:col,"stroke-width":5,fill:"none","stroke-linejoin":"round"});
 svgEl(bb.parts,"rect",{x:x+16,y:y-8,width:42,height:16,rx:6,fill:"#69a7d7",stroke:"#c5d8e6","stroke-width":1});});
 const [gx,gy]=bb.L("a",21),[mx]=bb.L("lm",21);svgEl(bb.parts,"path",{d:"M"+gx+" "+gy+" H"+mx,stroke:"#21242a","stroke-width":7,fill:"none"});
 const [gpx,gpy]=bb.L("i",59),[rx]=bb.L("lm",59);svgEl(bb.parts,"path",{d:"M"+gpx+" "+gpy+" H"+rx,stroke:"#21242a","stroke-width":7,fill:"none"});
 const labels=tile(wire,800,185,1000,470,'<div style="font:800 40px var(--display)">Common cathode wiring</div><div style="font:700 38px/1.8 var(--mono);margin-top:20px"><span style="color:#ff5d6c">Red &rarr; 220 &Omega; &rarr; D25</span><br><span style="color:#4ade80">Green &rarr; 220 &Omega; &rarr; D26</span><br><span style="color:#5aa9ff">Blue &rarr; 220 &Omega; &rarr; D27</span><br>Common leg &rarr; GND</div>');
 hidden(labels);show(labels,T("s11"));
 ask(wire,"QUICK QUESTION","Why three resistors instead of one on the common leg?",T("s14"),T("s15"),"Each color is a separate LED with its own current.",{x:800,y:720,w:1000,t1:T("s17")-0.2});
 exCard("\uD83E\uDD64","Three people, one straw","One shared resistor lets the colors compete for current.",T("s15"),T("s17")-0.2,
 "Here the LED needing the lowest voltage tends to take the most current.",T("s16"));
 const anode=tile(wire,800,700,1000,230,'<div style="font:800 36px var(--display)">Common anode?</div><div style="font:600 31px/1.4 var(--ui);margin-top:15px">Move the common leg to 3V3 and use<br><b style="color:var(--amber);font-family:var(--mono)">COMMON_ANODE = true;</b></div>');
 hidden(anode);pop(anode,T("s17"));
}
ep06Hero("C1",T("s13"),Math.min(T("s14")-0.4,T("s13")+9.5),"USB unplugged: RGB, common wire and three separate resistors.",{full:true});

// setColor: parameters and PWM values cause the displayed RGB mix.
const col=chapter("s18","s23");title(col,"One helper: setColor(r, g, b)","s18");
{
 const code=bigCode(col,80,170,1000,"void setColor(int r, int g, int b) {\n  analogWrite(RED_PIN, r);\n  analogWrite(GREEN_PIN, g);\n  analogWrite(BLUE_PIN, b);\n}",{size:38});show(code.c,T("s18"));
 code.hl([[T("s18"),0],[T("s19"),1],[T("s19")+1,2],[T("s19")+2,3],[T("s20"),-1]]);
 const call=bigCode(col,80,620,1000,"setColor(255, 0, 255);",{size:48});show(call.c,T("s21"));
 const panel=box(col,1140,170,690,700,"card","");
 const rows=[["R","#ff5d6c"],["G","#4ade80"],["B","#5aa9ff"]].map(([n,c],i)=>{
 box(panel,35,42+i*90,65,55,"",'<div style="font:800 38px var(--mono);color:'+c+'">'+n+'</div>');
 const tr=box(panel,100,60+i*90,390,20,"");css(tr,{background:"#22304d",borderRadius:10});
 const fill=box(tr,0,0,0,20,"");css(fill,{background:c,borderRadius:10});
 const val=box(panel,515,42+i*90,130,60,"");css(val,{font:"700 38px var(--mono)",textAlign:"right"});return {fill,val};});
 const values=t=>t<T("s21")?[255,0,0]:t<W("s22","orange")?[255,0,255]:[255,40,0];
 const L=rgbIcon(panel,270,340,150);L.drive(t=>t>=T("s21")&&t<T("s22")?[0,0,0]:values(t));
 dyn(t=>rows.forEach(({fill,val},i)=>{const v=values(t)[i];fill.style.width=390*v/255+"px";val.textContent=v;}));
 const q=box(panel,260,370,180,100,"",'<div style="font:800 90px var(--display);color:var(--amber);text-align:center">?</div>');
 styleAt(q,"opacity",[[0,"0"],[T("s21"),"1"],[T("s22"),"0"]]);
 ask(col,"QUICK QUESTION","Red 255, green 0, blue 255: which color?",T("s21"),T("s22"),"Magenta: red + blue.",{x:80,y:810,w:1000,t1:S1("s22")});
 exCard("\u2615","A button on a coffee machine","One call combines three amounts into one result.",T("s18"),T("s19")-0.3);
 exCard("\u2615","You supply the recipe every time","setColor() takes three numbers on every call.",T("s20"),T("s21")-0.3);
}

tour("rgb_colors","s23","s26",[
 [T("s23"),"const int RED_PIN","const bool COMMON_ANODE"],[T("s24"),"void setColor","analogWrite(BLUE_PIN, b)"],
 [T("s25"),"void loop","setColor(255, 255,   0)"],[T("s26"),"setColor(255, 255,   0)","setColor(255,  40,   0)"]]);
ask(stage,"PAUSE AND PREDICT","Fourth line: setColor(255, 255, 0). Which color?",W("s25","Pause"),T("s26"),"Yellow: full red + full green.",{x:210,y:740,w:1500,t1:S1("s26")-0.2});

const run=chapter("s27","s28");title(run,"Run it, then balance the channels","s27");
const balance=bigCode(run,100,260,730,"// reduce a strong channel\nsetColor(255, 180, 0);",{size:38});show(balance.c,T("s27b"));
note(run,"The channels are not equally bright. Adjust green and blue by eye.","s27b",820);
ep06Hero("C2",T("s27"),Math.min(T("s27b")-0.35,T("s27")+14.5),"Eight colors, one second each.",{full:true});
ep06Hero("C2",T("s27b"),Math.min(S1("s27b")-0.2,T("s27b")+14.5),"Compare the real colors before lowering green and blue.",{x:900,y:210,w:900,h:506});
likeTop(T("s27b")+0.3);

// Common ground mistake: predict, real result, then trace the complete path.
const bad=chapter("s28","s32");title(bad,"All three colors went dark. What do you check?","s28");
{
 const L=rgbIcon(bad,330,230,210);L.drive(t=>t<T("s29")?[255,0,255]:t<T("s30")?[0,0,0]:[255,0,255]);
 const g=bigCode(bad,790,250,1000,"pin -> LED -> common leg -> GND",{size:40});show(g.c,T("s30"));
 ask(bad,"QUICK QUESTION","What if the common black wire comes loose?",T("s28"),T("s29"),"Every color goes dark: all three share the same way back.",{y:760,w:1500,t1:T("s30")-0.25});
 const check=tile(bad,790,470,1000,300,'<div style="font:800 38px var(--display)">Trace the complete circuit</div><div style="font:600 32px/1.5 var(--ui);margin-top:20px">One color missing &rarr; check its own wire.<br>All colors missing &rarr; check the common wire.</div>');
 hidden(check);pop(check,T("s30"));
}
ep06Hero("C3",T("s29"),Math.min(T("s30")-0.4,T("s29")+14.2),"Pull the common black wire: dark. Reconnect it: colors return.",{full:true});

// One button and the counter's wrap from 3 to 0.
const modes=chapter("s32","s36");title(modes,"One button moves around four modes","s32");
{
 const c=bigCode(modes,100,190,920,"mode = mode + 1;\nif (mode > 3) {\n  mode = 0;\n}",{size:48});show(c.c,T("s32"));
 c.hl([[T("s32"),0],[T("s33"),-1],[W("s34","four"),0],[W("s34","greater"),1],[W("s34","zero"),2]]);
 const colors=["#ff5d6c","#4ade80","#5aa9ff","linear-gradient(135deg,#5aa9ff,#ff5d6c)"];
 const dots=["red","green","blue","fade"].map((lab,i)=>box(modes,1140+i%2*310,210+Math.floor(i/2)*250,230,180,"",'<div style="height:180px;border-radius:25px;background:'+colors[i]+';text-align:center;padding-top:20px;box-sizing:border-box;color:#0b1220"><div style="font:800 70px var(--mono)">'+i+'</div><div style="font:800 30px var(--ui)">'+lab+'</div></div>'));
 dyn(t=>dots.forEach((d,i)=>{const cur=t<T("s33")?Math.floor(Math.max(0,t-T("s32"))/2)%4:t<T("s34")?3:0;d.style.opacity=i===cur?"1":".35";}));
 ask(modes,"QUICK QUESTION","mode is 3. You press again. What should happen?",T("s33"),T("s34"),"4 for a moment, then the if sets it to 0.",{y:760,w:1500,t1:T("s35")-0.2});
 note(modes,"mode lives in memory. Serial.println(mode) makes it visible.","s35",800);
 exCard("\uD83D\uDCFA","Like the channel button on a remote","Each new press advances the counter. After the last, return to the first.",T("s32"),T("s33")-0.3);
}
tour("color_modes","s36","s40",[
 [T("s36"),null],[T("s37"),"// PART 2","setColor(0, 0, 255)"],
 [T("s38"),"if (now - lastStep >= 8)","setColor(level, 0, 255 - level)"],[T("s39"),"setColor(level, 0, 255 - level)"],[T("s40"),"setColor(level, 0, 255 - level)"]]);
ask(stage,"PAUSE AND PREDICT","level is 128. Red = level, blue = 255 - level. Which color?",W("s39","Pause"),T("s40"),"Purple: about half red and half blue.",{x:210,y:740,w:1500,t1:S1("s40")-0.2});

const run2=chapter("s41","s42");title(run2,"Each press changes the color instantly","s41");
ep06Hero("C4",T("s41"),Math.min(T("s42")-0.4,T("s41")+15.0),"Three presses: green, blue, and the fade starts.",{full:true});

const exp=chapter("s42","s44");title(exp,"Explain it in your own words","s42");
ask(exp,"PAUSE AND EXPLAIN","Why does mode return to 0 after 3? One sentence is enough.",T("s42"),T("s43"),"There are four modes. Past the last one, the code starts the circle again.",{x:210,y:290,w:1500,t1:S1("s43")});
const loop=bigCode(exp,420,650,1080,"if (mode > 3) mode = 0;",{size:54});show(loop.c,T("s43"));likeTop(T("s43")+0.3);

const ch=chapter("s44","s46");title(ch,"Your turn: the smart camping headlamp","s44");
{
 const a=tile(ch,130,220,1660,240,'<div style="font:800 40px var(--display)">One button, four modes</div><div style="font:700 40px var(--mono);margin-top:30px">off &rarr; dim white &rarr; bright white &rarr; red blink</div>');
 hidden(a);pop(a,T("s44"));
 const b=tile(ch,130,510,1660,270,'<div style="font:800 40px var(--display);color:var(--amber)">The twist: after 3 seconds, straight off</div><div style="font:600 34px/1.5 var(--ui);margin-top:20px">If the lamp has been on for at least 3000 ms,<br>the next press switches it off instead of advancing.</div>',"var(--amber)");
 hidden(b);pop(b,T("s45"));note(ch,"Hint: remember when the mode last changed.","s45",840);
}

const out=chapter("s46",null);title(out,"Three things you can now explain","s46");
{
 [["RGB LED","Three LEDs share one common leg."],["setColor(r, g, b)","Three numbers set three PWM amounts."],["mode","One counter lets a button choose."]].forEach(([a,b],i)=>{
 const c=tile(out,115+i*575,230,540,360,'<div style="font:800 45px var(--display);color:var(--teal)">'+a+'</div><div style="font:600 33px/1.5 var(--ui);margin-top:25px">'+b+'</div>');hidden(c);pop(c,T("s46")+i*0.2);hide(c,T("s47")-0.15);});
 const next=tile(out,210,220,1500,350,'<div class="kicker">NEXT: EPISODE 7</div><div style="font:800 66px var(--display);margin-top:30px">Read a knob. Control brightness.</div><div style="font:600 36px var(--ui);margin-top:25px;color:var(--muted)">Potentiometer &rarr; analogRead() &rarr; LED</div>');
 hidden(next);pop(next,T("s47"));note(out,"Post your headlamp in the comments. One solution is in the lesson folder.","s47",700);
 note(out,"github.com/emjnbulut/esp32-from-zero &rarr; lessons/06-rgb","s47",850);
 const fade=box(stage,0,0,1920,1080,"");css(fade,{background:"#000",zIndex:200,opacity:0});TO(fade,D.schedule.duration-1.2,1.2,{opacity:1,ease:"none"});
}
window.__seek(0);
window.__ready=true;
