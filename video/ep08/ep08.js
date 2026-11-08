/* Episode 8 map(), Dimmer Knobs and Level Bars: segment-anchored scenes, creator footage C0-C4, code tours.
 * Clips C0/C2/C3/C4 are tall crops (1080x1200) that keep the knob and the three LEDs in one frame; they sit in a tall
 * window on the left, the drawing or the code on the right. C1 (wiring) is a 16:9 crop. Helpers copied from episode 7. */
const stage = $("#stage");
const EP08_CLIP_SECONDS = { C0: 17.2, C1: 21.27, C2: 12.07, C3: 15.47, C4: 13.1 };
function hero(id, t0, requestedEnd, description, opts = {}) {
  const lead = opts.full ? Math.min(0.3, t0) : 0;
  const tail = opts.full ? 0.35 : 0;
  const t1 = Math.min(requestedEnd, t0 + EP08_CLIP_SECONDS[id] - lead - tail - 1 / 30);
  if (!(t1 > t0)) throw new Error("No usable episode 8 footage: " + id);
  return heroClip(stage, id, t0, t1, description, opts);
}
/** the tall knob + LEDs window (clip aspect 0.9) */
const TALL = { x: 110, y: 100, w: 846, h: 940 };
const SC = (cls = "") => el("div", "scene " + cls, '<div class="grid"></div>', stage);
const T = (id) => S0(id);
const hidden = (e) => { gsap.set(e, { opacity: 0 }); return e; };
const CUT = S0("s03") - 0.1; // the channel sting is inserted here (script "sting_after": "s02")
const span = (sc, t0, t1) => { sceneIn(sc, t0, 0.45); if (t1 != null) sceneOut(sc, t1, 0.45); };
function head(parent, html, y = 52) {
  const h = box(parent, 0, y, 1920, 80, "h2", html);
  h.style.textAlign = "center";
  return hidden(h);
}
const inAny = (t, list) => list.some(([a, b]) => t >= a && t < b);
const sweep = (t, t0, period) => { const x = (((t - t0) % period) + period) % period / period; return 0.5 - 0.5 * Math.cos(2 * Math.PI * x); };
const nz = (i, seed = 1) => { const s = Math.sin(i * 12.9898 + seed * 78.233) * 43758.5453; return s - Math.floor(s); };
const reading = (pos, i = 0) => Math.max(0, Math.min(4095, Math.round(4095 * pos + (nz(i, 3) - 0.5) * 24)));
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const mapI = (v, a, b, c, d) => Math.trunc((v - a) * (d - c) / (b - a) + c); // Arduino map(): whole numbers, cut toward zero
const txt = (g, x, y, s, attrs) => { const e = svgEl(g, "text", Object.assign({ x, y, "font-family": "Segoe UI", "font-weight": 700, "font-size": 26, fill: "#8fa1c0" }, attrs)); e.textContent = s; return e; };
const pill = (parent, x, y, html, style = "") => {
  const p = box(parent, x, y, 0, 0, "", `<span class="pill" style="font-size:30px;${style}">${html}</span>`);
  css(p, { width: "auto", height: "auto", whiteSpace: "nowrap" });
  return hidden(p);
};
const pillC = (parent, y, html, style = "", x = 0, w = 1920) => hidden(box(parent, x, y, w, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:32px;${style}">${html}</span></div>`));

const LEDC = {
  red: ["#ff8a8f", "#d4202c", "#b51d27", "255,80,80", "#ffd0d0"],
  yellow: ["#fff09a", "#e8b800", "#b38f00", "255,220,60", "#fff6c8"],
  green: ["#9dffb8", "#22b14c", "#178a3a", "80,255,120", "#d8ffe2"],
};
let ledN = 0;
/** side-view LED with a glow behind it; drive(fn) sets brightness 0..1 from time */
function ledIcon(parent, x, y, w = 110, color = "red") {
  const [c0, c1, c2, rgb, hotc] = LEDC[color], id = "lg" + ledN++;
  const r = box(parent, x, y, w, w * 230 / 120, "");
  const glow = box(r, -w * 0.75, -w * 0.7, w * 2.5, w * 2.5, "");
  css(glow, { borderRadius: "50%", background: `radial-gradient(circle, rgba(${rgb},.9) 0%, rgba(${rgb},.45) 30%, rgba(${rgb},0) 65%)`, opacity: 0 });
  r.insertAdjacentHTML("beforeend", `<svg width="${w}" viewBox="0 0 120 230" style="position:absolute;left:0;top:0"><defs><radialGradient id="${id}" cx=".4" cy=".35"><stop offset="0" stop-color="${c0}"/><stop offset="1" stop-color="${c1}"/></radialGradient></defs>
    <path d="M44 96 V226" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/><path d="M76 96 V186" stroke="#c3c9d1" stroke-width="6" stroke-linecap="round"/>
    <path d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="url(#${id})" opacity=".95"/><path class="hot" d="M28 96 V52 a32 32 0 0 1 64 0 V96 z" fill="${hotc}" opacity="0"/>
    <path d="M22 92 h70 v14 h-70 z" fill="${c2}"/></svg>`);
  const hot = $(".hot", r);
  const drive = (fn) => dyn((t) => { const v = clamp(fn(t), 0, 1); glow.style.opacity = v; hot.setAttribute("opacity", v * 0.75); });
  return { r, glow, drive };
}
/** the three LEDs of the bar, bottom (green) to top (red) or side by side; drive(fnLevel) lights `level` LEDs from green */
function barLeds(parent, x, y, w = 100, gap = 170, opts = {}) {
  const cols = ["green", "yellow", "red"];
  const leds = cols.map((c, i) => ledIcon(parent, opts.row ? x + i * gap : x, opts.row ? y : y + (2 - i) * gap, w, c));
  const drive = (fnLevel, dead = -1) => leds.forEach((L, i) => L.drive((t) => (i !== dead && fnLevel(t) > i ? 1 : 0)));
  return { leds, drive, all: leds.map((L) => L.r) };
}
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
/** a recreated Serial Monitor; fn(i, time) = the text printed on line i, one line every dt seconds from t0 */
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
/** a live value card: label + a number from fn(t) */
function live(parent, x, y, w, label, fn, color = "var(--amber)") {
  const c = box(parent, x, y, w, 160, "live", `<div class="k">${label}</div><div class="v" style="color:${color}"></div>`);
  const v = $(".v", c);
  dyn((t) => { const s = String(fn(t)); if (v.__s !== s) { v.textContent = s; v.__s = s; } });
  return hidden(c);
}
/** a horizontal range with end labels and a pointer at fn(t) = 0..1 */
function rangeBar(parent, x, y, w, lo, hi, col, label, fn) {
  const r = box(parent, x, y, w, 170, "");
  const svg = svgEl(r, "svg", { width: w, height: 170, viewBox: `0 0 ${w} 170` });
  css(svg, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  svgEl(svg, "rect", { x: 0, y: 60, width: w, height: 40, rx: 20, fill: col, opacity: 0.85 });
  txt(svg, 0, 145, lo, { "font-size": 40, fill: "#e8eef7", "font-family": "Consolas" });
  txt(svg, w, 145, hi, { "font-size": 40, fill: "#e8eef7", "text-anchor": "end", "font-family": "Consolas" });
  txt(svg, 0, 40, label, { "font-size": 32, fill: "#8fa1c0" });
  const p = svgEl(svg, "path", { d: "M-18 40 H18 L0 70 Z", fill: "#ffffff" });
  if (fn) dyn((t) => p.setAttribute("transform", `translate(${w * clamp(fn(t), 0, 1)} 0)`));
  return { r, svg, p };
}
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
const likeTop = (t0) => likeSub(stage, t0, 2.6, { style: { top: "36px", bottom: "auto" } });
function ask(parent, kicker, q, t0, tAns, answer, opts) {
  const c = quizCard(parent, q, t0, tAns, answer, opts);
  $(".qk", c).innerHTML = kicker;
  return c;
}
function askTop(...a) { const c = ask(...a); css(c, { zIndex: 95 }); return c; }
const repo = "Full code: <b>github.com/emjnbulut/esp32-from-zero</b> &rarr; lessons/08-map-and-level-bar";
function tour(file, t0, t1, marks) { return fullCode(stage, file + ".ino", SKETCHES[file], t0, t1, repo, marks); }
function chapter(first, next) { const sc = SC(); span(sc, Math.max(0, T(first) - 0.45), next ? T(next) - 0.45 : null); return sc; }
function title(sc, text, id) { const h = head(sc, text); show(h, T(id)); return h; }
function note(sc, text, t0, y = 840, t1 = null, x = 130, w = 1660) {
  const n = box(sc, x, y, w, 100, "", '<div style="font:600 34px/1.4 var(--ui);text-align:center;color:var(--muted)">' + text + "</div>");
  hidden(n); show(n, t0); if (t1) hide(n, t1, 0.25);
  return n;
}
function tile(sc, x, y, w, h, text, col = "var(--teal)") {
  return box(sc, x, y, w, h, "card", '<div style="padding:32px;border-top:4px solid ' + col + ';border-radius:20px;height:100%;box-sizing:border-box">' + text + "</div>");
}
/** the four states of the bar as rows: [level, dots] */
function levelRows(parent, x, y, w, fnLevel) {
  const COL = ["#4ade80", "#ffe14d", "#ff5d6c"];
  const rows = [0, 1, 2, 3].map((lv) => {
    const r = box(parent, x, y + (3 - lv) * 104, w, 88, "lvl",
      `<span style="width:150px;color:var(--muted)">level ${lv}</span>` + COL.map((c, i) => `<span class="d" style="${i < lv ? `background:${c};box-shadow:0 0 18px ${c}` : ""}"></span>`).join(""));
    return r;
  });
  if (fnLevel) dyn((t) => rows.forEach((r, lv) => { r.style.borderColor = fnLevel(t) === lv ? "var(--amber)" : "#22304d"; r.style.opacity = fnLevel(t) === lv ? "1" : ".45"; }));
  return rows;
}

/* ======================================================================
 * THE CREATOR'S CIRCUIT, drawn vertical (from episode 7): vbb(parent, x, y, p), holes L(col, row)
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
  svgEl(svg, "defs").innerHTML = `<linearGradient id="${id}sh" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9edf2"/><stop offset=".5" stop-color="#b9c0c9"/><stop offset="1" stop-color="#d9dee5"/></linearGradient>`;
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
  const esp = svgEl(svg, "g", {});
  const [xl] = L("j", 46), [xr] = L("A", 46), yT = RY(46), yB = RY(60);
  svgEl(esp, "path", { d: `M${(xl + xr) / 2} ${yB + 3.4 * p} V${yB + 30 * p}`, stroke: "#c8202b", "stroke-width": 1.6 * p, "stroke-linecap": "round" });
  svgEl(esp, "rect", { x: (xl + xr) / 2 - 1.0 * p, y: yB + 2.2 * p, width: 2.0 * p, height: 1.6 * p, rx: 0.2 * p, fill: "#f2f2f2" });
  svgEl(esp, "rect", { x: (xl + xr) / 2 - 1.3 * p, y: yB + 1.2 * p, width: 2.6 * p, height: 1.4 * p, rx: 0.2 * p, fill: `url(#${id}sh)`, stroke: "#7d8690" });
  svgEl(esp, "rect", { x: xl - 0.9 * p, y: yT - 1.9 * p, width: xr - xl + 1.8 * p, height: yB - yT + 3.6 * p, rx: 0.5 * p, fill: "#1b1f26", stroke: "#2b313b", "stroke-width": 2 });
  svgEl(esp, "rect", { x: xl + 1.6 * p, y: yT - 1.5 * p, width: xr - xl - 3.2 * p, height: 7.6 * p, rx: 0.2 * p, fill: "#24384f" });
  svgEl(esp, "rect", { x: xl + 2.0 * p, y: yT + 0.6 * p, width: xr - xl - 4.0 * p, height: 5.2 * p, rx: 0.2 * p, fill: `url(#${id}sh)` });
  txt(esp, (xl + xr) / 2, yT + 3.6 * p, "ESP32", { "text-anchor": "middle", "font-size": 1.1 * p, fill: "#5d6670" });
  const LP = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"];
  const RP = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"];
  const HOT = ["D23", "D18", "TX2", "GND", "D34", "3V3"];
  for (let k = 0; k < 15; k++) {
    for (const [c, nm, dx, anchor] of [["j", LP[k], 0.7, "start"], ["A", RP[k], -0.7, "end"]]) {
      const [px, py] = L(c, 46 + k);
      svgEl(esp, "rect", { x: px - 0.32 * p, y: py - 0.32 * p, width: 0.64 * p, height: 0.64 * p, rx: 0.08 * p, fill: "#d4af37" });
      const hot = HOT.includes(nm);
      txt(esp, px + dx * p, py + 0.22 * p, nm, { "text-anchor": anchor, "font-size": 0.6 * p, fill: hot ? "#ffe3b8" : "#c9d1dc", "font-weight": hot ? 800 : 600 });
    }
  }
  const parts = svgEl(svg, "g", {});
  const over = svgEl(svg, "g", {});
  const wire = (a, b, color, bend = 0.15, outline = false) => {
    const [ax, ay] = L(...a), [bx, by] = L(...b), mx = (ax + bx) / 2, my = (ay + by) / 2;
    const g = svgEl(parts, "g", {}), d = `M${ax} ${ay} Q${mx - (by - ay) * bend} ${my + (bx - ax) * bend} ${bx} ${by}`;
    if (outline) svgEl(g, "path", { d, fill: "none", stroke: "#e7ebf0", "stroke-width": 0.82 * p, "stroke-linecap": "round" });
    svgEl(g, "path", { d, fill: "none", stroke: color, "stroke-width": 0.5 * p, "stroke-linecap": "round" });
    for (const [ex, ey] of [[ax, ay], [bx, by]]) svgEl(g, "rect", { x: ex - 0.28 * p, y: ey - 0.28 * p, width: 0.56 * p, height: 0.56 * p, rx: 0.08 * p, fill: "#222" });
    return g;
  };
  const resistor = (a, b) => {
    const [ax, ay] = L(...a), [bx, by] = L(...b), ang = Math.atan2(by - ay, bx - ax) * 180 / Math.PI, len = Math.hypot(bx - ax, by - ay);
    const g = svgEl(parts, "g", { transform: `translate(${ax} ${ay}) rotate(${ang})` });
    svgEl(g, "path", { d: `M0 0 H${len}`, stroke: "#b8bec6", "stroke-width": 0.22 * p });
    const bl = 2.6 * p, b0 = (len - bl) / 2;
    svgEl(g, "rect", { x: b0, y: -0.5 * p, width: bl, height: p, rx: 0.42 * p, fill: "#5aa0d8", stroke: "#3a78ad", "stroke-width": 1 });
    [0.45, 0.85, 1.25, 1.9].forEach((o, k) => svgEl(g, "rect", { x: b0 + o * p, y: -0.5 * p, width: 0.22 * p, height: p, fill: ["#d0262f", "#d0262f", "#3b2a1a", "#c9a54a"][k] }));
    return g;
  };
  /** an LED standing in column G: long leg `longRow`, short leg `longRow - 1`, dome above; returns { g, drive } */
  const ledAt = (longRow, color) => {
    const [, , c2, rgb, hotc] = LEDC[color], c1 = LEDC[color][1];
    const g = svgEl(parts, "g", {}), go = svgEl(over, "g", {});
    const [gx, gs] = L("G", longRow - 1), [, gl] = L("G", longRow), dc = [gx - 0.2 * p, RY(longRow - 2.6)];
    const glow = svgEl(go, "circle", { cx: dc[0], cy: dc[1], r: 4.2 * p, fill: `rgba(${rgb},.55)`, opacity: 0 });
    css(glow, { filter: `blur(${p}px)` });
    for (const yy of [gs, gl]) svgEl(g, "path", { d: `M${gx} ${yy} L${dc[0] + (yy === gl ? 0.3 : -0.3) * p} ${dc[1]}`, stroke: "#b8bec6", "stroke-width": 0.22 * p });
    svgEl(g, "circle", { cx: dc[0], cy: dc[1], r: 0.95 * p, fill: c2 });
    svgEl(g, "circle", { cx: dc[0], cy: dc[1], r: 0.8 * p, fill: c1 });
    const lit = svgEl(g, "circle", { cx: dc[0], cy: dc[1], r: 0.8 * p, fill: hotc, opacity: 0 });
    return { g, glow, cx: dc[0], cy: dc[1], drive: (fn) => dyn((t) => { const v = clamp(fn(t), 0, 1); glow.setAttribute("opacity", v); lit.setAttribute("opacity", v * 0.8); }) };
  };
  // episode 7 circuit: GND -> minus rail, red LED on D23 (resistor D46 -> F40, LED G40/G39, short leg -> minus rail), button on D22
  wire(["D", 59], ["rm", 59], "#1d1f24", 0.04);
  wire(["C", 47], ["C", 36], "#8a9099", 0.08);
  wire(["I", 34], ["rm", 34], "#ff8a2a", 0);
  wire(["I", 39], ["rm", 39], "#ff8a2a", 0);
  resistor(["D", 46], ["F", 40]);
  const red = ledAt(40, "red");
  const [ex] = L("E", 34), [fx] = L("F", 34), by0 = RY(33.4), by1 = RY(36.6);
  for (const [lx, ly] of [[ex, RY(34)], [fx, RY(34)], [ex, RY(36)], [fx, RY(36)]]) svgEl(parts, "rect", { x: lx - 0.25 * p, y: ly - 0.25 * p, width: 0.5 * p, height: 0.5 * p, fill: "#aab2bd" });
  svgEl(parts, "rect", { x: ex - 0.7 * p, y: by0, width: fx - ex + 1.4 * p, height: by1 - by0, rx: 0.25 * p, fill: "#23272f", stroke: "#3a404b", "stroke-width": 2 });
  svgEl(parts, "circle", { cx: (ex + fx) / 2, cy: (by0 + by1) / 2, r: 1.0 * p, fill: "#4a5262", stroke: "#11141a", "stroke-width": 2 });
  return { root, svg, L, S: (c, r) => { const [lx, ly] = L(c, r); return [X + lx, Y + ly]; }, RY, p, w: W_, h: H_, red, parts, over, wire, resistor, ledAt };
}
function deskCircuit(parent, x, p, rowTop, yTop) {
  const Y = Math.round(yTop - (rowTop + 0.6) * p);
  const bb = vbb(parent, x, Y, p);
  const f = box(parent, x - 10, 0, bb.w + 20, yTop + p, "");
  css(f, { background: "linear-gradient(180deg, #0b1220 0%, #0b1220 25%, rgba(11,18,32,0) 100%)" });
  bb.Y = Y;
  return bb;
}
/** the knob where the creator moved it for this episode: top of the right board, rows 22-26, wiper -> D34 (long red wire) */
function addPotTop(bb) {
  const p = bb.p, [x0] = bb.L("G", 22), [x1] = bb.L("I", 22), y0 = bb.RY(21.4), y1 = bb.RY(26.6);
  const body = svgEl(bb.parts, "g", {});
  svgEl(body, "rect", { x: x0 - 3.6 * p, y: bb.RY(22.9), width: 3.2 * p, height: 2.4 * p, rx: 0.3 * p, fill: "#c6ccd4", stroke: "#8e96a1", "stroke-width": 1.5 });
  svgEl(body, "rect", { x: x0 - 0.5 * p, y: y0, width: x1 - x0 + p, height: y1 - y0, rx: 0.5 * p, fill: "#c9a24a", stroke: "#8a6f2c", "stroke-width": 2 });
  [22, 24, 26].forEach((r) => { const [lx, ly] = bb.L("H", r); svgEl(body, "circle", { cx: lx, cy: ly, r: 0.34 * p, fill: "#e4e8ee", stroke: "#6e7681", "stroke-width": 1 }); });
  bb.wire(["J", 22], ["rp", 22], "#ff8a2a", 0);
  bb.wire(["J", 26], ["rm", 26], "#5b3a22", 0);
  bb.wire(["D", 60], ["rp", 59], "#d0262f", 0.02);
  bb.wire(["rp", 29], ["rp", 33], "#d0262f", 0.28); bb.wire(["rm", 29], ["rm", 33], "#1d1f24", -0.28);
  bb.wire(["F", 24], ["i", 49], "#d0262f", 0.22, true);
  return body;
}
function holeRing(bb, c, r, color) {
  const [x, y] = bb.L(c, r);
  return svgEl(bb.over, "circle", { cx: x, cy: y, r: 1.15 * bb.p, fill: "none", stroke: color, "stroke-width": 0.3 * bb.p, opacity: 0 });
}

/* ======================================================================
 * COLD OPEN: the real bar, then the promise
 * ==================================================================== */
const cold = SC(); SET(cold, 0, { opacity: 1 }); SET(cold, CUT, { opacity: 0 });
{
  const h = box(cold, 1010, 120, 800, 120, "", '<div style="font:800 58px/1.2 var(--display)">Turn the knob,<br><span style="color:var(--amber)">fill the bar</span></div>');
  hidden(h); show(h, 0.6);
  const vm = tile(cold, 1010, 360, 800, 250, '<div style="display:flex;gap:30px;align-items:center"><div style="font-size:110px;line-height:1">🔊</div><div style="font:700 40px/1.35 var(--ui)">Like a volume meter</div></div>', "var(--amber)");
  hidden(vm); show(vm, W("s01", "volume") - 0.2); hide(vm, T("s02") - 0.2, 0.25);
  const c = bigCode(cold, 1010, 360, 800, "map(value, ...)", { size: 56 }); show(c.c, W("s02", "single"));
  const one = box(cold, 1010, 560, 800, 120, "", '<div style="font:700 38px/1.4 var(--ui);color:var(--muted)">One function turns one range of numbers into another.</div>');
  hidden(one); show(one, W("s02", "single") + 0.3);
  const yb = pill(cold, 1010, 760, "&rarr; and you build this bar yourself", "font-size:36px;color:var(--teal)"); show(yb, W("s02", "build"));
}
hero("C0", 0, CUT, "level_bar: a hand turns the knob, the bar fills green, yellow, red.", TALL);

/* ======================================================================
 * RETRIEVAL (episode 7) + the way in for new viewers
 * ==================================================================== */
const ret = chapter("s03", "s07"); title(ret, "Two questions from episode 7", "s03");
{
  const nw = pill(ret, 1360, 150, "New here? Start at Episode 1 &rarr;", "font-size:28px;color:var(--teal)"); show(nw, T("s03") + 0.2); hide(nw, T("s03") + 4.5, 0.3);
  const k = knobIcon(ret, 260, 220, 330); k.drive(() => 0.5); hidden(k.r); show(k.r, T("s03")); hide(k.r, T("s05") - 0.2, 0.25);
  const n = live(ret, 760, 260, 560, "analogRead()", (t) => (t < T("s04") ? "?" : "≈ 2000")); show(n, W("s03", "knob")); hide(n, T("s05") - 0.2, 0.25);
  const ru = rangeBar(ret, 760, 470, 1000, "0", "≈ 4000", "#ffb547", "the ruler", () => 0.5); hidden(ru.r); show(ru.r, T("s04")); hide(ru.r, T("s05") - 0.2, 0.25);
  ask(ret, "QUICK QUESTION", "Knob in the middle: roughly what does analogRead() give?", W("s03", "Quick"), T("s04"), "About 2000: half of the ruler.", { y: 720, w: 1500, t1: T("s05") - 0.2 });

  const k2 = knobIcon(ret, 300, 230, 300); k2.drive((t) => sweep(t, T("s05"), 3)); hidden(k2.r); show(k2.r, T("s05"));
  const L = ledIcon(ret, 790, 210, 150, "red"); L.drive(() => 0); hidden(L.r); show(L.r, T("s05"));
  const th = tile(ret, 1180, 230, 560, 330, '<div style="font-size:90px;line-height:1">🌡️</div><div style="font:700 36px/1.4 var(--mono);margin-top:20px">Serial.println(value);</div>', "var(--amber)");
  hidden(th); show(th, T("s06"));
  ask(ret, "QUICK QUESTION", "The LED ignores the knob. What's the very first thing you do?", T("s05"), T("s06"), "Print the value: it tells you which half to look at.", { y: 720, w: 1500, t1: S1("s06") });
}

/* ======================================================================
 * PARTS
 * ==================================================================== */
const parts = chapter("s07", "s08"); title(parts, "What you need", "s07");
[["Episode 7 circuit", "knob + red LED", "#ffb547", "s07", null], ["Yellow + green LED", "two new lights", "#ffe14d", "s07", "yellow"], ["2 &times; 220 &Omega;, a few wires", "a resistor for each LED", "#b48cff", "s07", "resistor"]].forEach(([h, d, col, id, w], i) => {
  const c = tile(parts, 115 + i * 575, 250, 540, 480, `<div style="height:230px"></div><div style="font:800 40px var(--display)">${h}</div><div style="font:600 32px/1.4 var(--ui);margin-top:16px;color:var(--muted)">${d}</div>`, col);
  hidden(c); show(c, w ? W(id, w) : T(id));
  if (i === 0) { const k = knobIcon(c, 90, 40, 170, true); k.drive((t) => sweep(t, T("s07"), 6)); const L = ledIcon(c, 330, 40, 90, "red"); L.drive(() => 0.8); }
  if (i === 1) { const a = ledIcon(c, 150, 40, 90, "yellow"); a.drive(() => 0.8); const b = ledIcon(c, 300, 40, 90, "green"); b.drive(() => 0.8); }
  if (i === 2) c.insertAdjacentHTML("beforeend", '<svg width="440" height="180" viewBox="0 0 440 180" style="position:absolute;left:50px;top:60px"><path d="M20 60 H420 M20 140 H420" stroke="#b8bec6" stroke-width="6"/><rect x="150" y="40" width="140" height="40" rx="18" fill="#5aa0d8"/><rect x="150" y="120" width="140" height="40" rx="18" fill="#5aa0d8"/><rect x="175" y="40" width="12" height="40" fill="#d0262f"/><rect x="200" y="40" width="12" height="40" fill="#d0262f"/><rect x="175" y="120" width="12" height="40" fill="#d0262f"/><rect x="200" y="120" width="12" height="40" fill="#d0262f"/></svg>');
});

/* ======================================================================
 * THE IDEA: dividing by 16 -> a city map -> map()
 * ==================================================================== */
const idea = chapter("s08", "s13"); const ih = title(idea, "", "s08");
textAt(ih, [[0, "Where did 16 come from?"], [T("s09") - 0.2, "Think of a city map"], [T("s10") - 0.2, "A function called map()"], [T("s11") - 0.2, "Same position, other range"]]);
{
  // s08: last episode's division
  const li = bigCode(idea, 360, 200, 1200, "int brightness = value / 16;", { size: 56 }); show(li.c, T("s08")); hide(li.c, T("s09") - 0.2, 0.25);
  const qm = box(idea, 360, 420, 1200, 300, "", '<div style="font:800 200px/300px var(--display);text-align:center;color:var(--amber)">16 ?</div>');
  hidden(qm); show(qm, W("s08", "figure")); hide(qm, T("s09") - 0.2, 0.25);

  // s09: a city and its map, one dot in the same relative place
  const pos = (t) => ({ x: 0.15 + 0.7 * sweep(t, T("s09"), 7), y: 0.3 + 0.4 * sweep(t, T("s09") + 1.3, 5.5) });
  const city = box(idea, 160, 200, 900, 640, ""); hidden(city); show(city, T("s09")); hide(city, T("s10") - 0.2, 0.25);
  const cs = svgEl(city, "svg", { width: 900, height: 640, viewBox: "0 0 900 640" }); css(cs, { position: "absolute", left: 0, top: 0 });
  svgEl(cs, "rect", { x: 0, y: 0, width: 900, height: 640, rx: 20, fill: "#16203a", stroke: "#2c3b5e", "stroke-width": 3 });
  for (let i = 1; i < 6; i++) svgEl(cs, "path", { d: `M${i * 150} 0 V640`, stroke: "#4a5a80", "stroke-width": 14 });
  for (let i = 1; i < 4; i++) svgEl(cs, "path", { d: `M0 ${i * 160} H900`, stroke: "#4a5a80", "stroke-width": 14 });
  txt(cs, 30, 610, "the city", { "font-size": 40, fill: "#c9d1dc" });
  const d1 = svgEl(cs, "circle", { r: 26, fill: "#ffb547", stroke: "#fff", "stroke-width": 4 });
  const mapc = box(idea, 1230, 330, 450, 320, ""); hidden(mapc); show(mapc, W("s09", "paper") - 0.1); hide(mapc, T("s10") - 0.2, 0.25);
  const ms = svgEl(mapc, "svg", { width: 450, height: 320, viewBox: "0 0 450 320" }); css(ms, { position: "absolute", left: 0, top: 0 });
  svgEl(ms, "rect", { x: 0, y: 0, width: 450, height: 320, rx: 10, fill: "#efe6cf", stroke: "#a58f4f", "stroke-width": 3 });
  for (let i = 1; i < 6; i++) svgEl(ms, "path", { d: `M${i * 75} 0 V320`, stroke: "#b9a777", "stroke-width": 6 });
  for (let i = 1; i < 4; i++) svgEl(ms, "path", { d: `M0 ${i * 80} H450`, stroke: "#b9a777", "stroke-width": 6 });
  const d2 = svgEl(ms, "circle", { r: 14, fill: "#d0262f", stroke: "#fff", "stroke-width": 3 });
  const ml = box(idea, 1230, 670, 450, 60, "", '<div style="font:700 36px var(--ui);text-align:center;color:#c9d1dc">the map</div>'); hidden(ml); show(ml, W("s09", "paper")); hide(ml, T("s10") - 0.2, 0.25);
  dyn((t) => { const q = pos(t); d1.setAttribute("cx", 900 * q.x); d1.setAttribute("cy", 640 * q.y); d2.setAttribute("cx", 450 * q.x); d2.setAttribute("cy", 320 * q.y); });
  const hw = pillC(idea, 880, "halfway across town = halfway across the map", "font-size:36px;color:var(--teal)"); show(hw, W("s09", "halfway")); hide(hw, T("s10") - 0.2, 0.25);

  // s10: the function, its five slots
  const sig = box(idea, 160, 220, 1600, 150, "card", '<div style="font:800 54px/150px var(--mono);text-align:center;white-space:nowrap">map(<span class="arg a0">number</span>, <span class="arg a1">from range</span>, <span class="arg a2">to range</span>)</div>');
  hidden(sig); show(sig, W("s10", "map")); hide(sig, T("s13") - 0.25, 0.25);
  [["a0", W("s10", "number"), "#ffb547"], ["a1", W("s10", "comes"), "#5aa9ff"], ["a2", W("s10", "want"), "#ff8a8f"]].forEach(([c, t0, col]) => styleAt($("." + c, sig), "background", [[0, "transparent"], [t0, col + "55"]]));
  // s11 - s12: same position in another range; then stretch / flip
  const frac = (t) => sweep(t, T("s11"), 6);
  const A = rangeBar(idea, 260, 440, 1400, "start", "end", "#5aa9ff", "first range", frac); hidden(A.r); show(A.r, W("s11", "first")); hide(A.r, T("s13") - 0.25, 0.25);
  const flipAt = W("s12", "flip");
  const Bfn = (t) => (t < flipAt ? frac(t) : 1 - frac(t));
  const B2 = rangeBar(idea, 560, 660, 800, "start", "end", "#ff8a8f", "second range", Bfn); hidden(B2.r); show(B2.r, W("s11", "second")); hide(B2.r, T("s13") - 0.25, 0.25);
  const tl2 = B2.svg.querySelectorAll("text");
  dyn((t) => { const f = t >= flipAt; tl2[0].textContent = f ? "end" : "start"; tl2[1].textContent = f ? "start" : "end"; });
  const lim = box(idea, 160, 880, 1600, 100, "", '<div style="font:600 34px/1.4 var(--ui);color:#ffe3b8;text-align:center"><b style="color:var(--amber)">The difference:</b> a paper map only shrinks. map() can also stretch a range, or flip it.</div>');
  hidden(lim); show(lim, T("s12")); hide(lim, T("s13") - 0.25, 0.25);
}

/* ======================================================================
 * THE MAP LINE, slot by slot
 * ==================================================================== */
const ml = chapter("s13", "s16"); title(ml, "The map() line", "s13");
{
  const c = box(ml, 110, 200, 1700, 160, "card", '<div style="font:800 52px/160px var(--mono);text-align:center;white-space:nowrap">map(<span class="arg b0">value</span>, <span class="arg b1">0, 4095</span>, <span class="arg b2">0, 255</span>)</div>');
  hidden(c); show(c, T("s13"));
  [["b0", W("s13", "First"), "#ffb547"], ["b1", W("s13", "knobs"), "#5aa9ff"], ["b2", W("s13", "brightness"), "#ff8a8f"]].forEach(([k, t0, col]) => styleAt($("." + k, c), "background", [[0, "transparent"], [t0, col + "55"]]));
  const lb = [["the knob's number", "#ffb547", W("s13", "First")], ["knob: start, end", "#5aa9ff", W("s13", "knobs")], ["brightness: start, end", "#ff8a8f", W("s13", "brightness")]];
  lb.forEach(([s, col, t0], i) => { const p = pill(ml, [330, 760, 1260][i], 380, s, `font-size:30px;color:${col}`); show(p, t0); });
  const mid = (t) => (t < T("s14") ? sweep(t, T("s13"), 6) : 0.49);
  const K = rangeBar(ml, 210, 490, 1150, "0", "4095", "#5aa9ff", "knob", mid); hidden(K.r); show(K.r, T("s14"));
  const Bv = rangeBar(ml, 210, 670, 1150, "0", "255", "#ff8a8f", "brightness", mid); hidden(Bv.r); show(Bv.r, T("s15"));
  const v = live(ml, 1440, 560, 380, "map() gives", (t) => (t < T("s15") ? "?" : "≈ 127")); css(v, { zIndex: 30 });
  ask(ml, "QUICK QUESTION", "The knob reads about 2000. What brightness does map() give?", T("s14"), T("s15"), "About 127: in at the middle, out at the middle.", { y: 870, w: 1500, t1: S1("s15") });
  show(v, T("s14") + 0.3);
}
tour("map_dimmer", T("s16") - 0.4, T("s19") - 0.3, [
  [T("s16"), "int brightness = map"], [W("s17", "loop"), "int value = analogRead"], [W("s17", "map"), "int brightness = map"], [W("s17", "last"), "analogWrite(LED_PIN, brightness)"], [T("s18"), "int brightness = map"]]);
askTop(stage, "PAUSE AND PREDICT", "Will the LED look any different from the divide-by-16 version?", T("s18"), T("s19"), "No: same smooth dimmer. The line just reads better.", { x: 210, y: 790, w: 1500, t1: T("s19") - 0.3 });

/* s19: the real dimmer, the knob in the same frame */
const rd = chapter("s19", "s20");
{
  const c = bigCode(rd, 1010, 200, 820, "map(value, 0, 4095, 0, 255)", { size: 40 }); show(c.c, T("s19"));
  const t1 = tile(rd, 1010, 400, 820, 330, '<div style="font:800 44px var(--display)">Looks the same</div><div style="font:600 34px/1.45 var(--ui);margin-top:20px;color:var(--muted)">Smooth from dark to full. The difference is in the code: anyone can read both ranges.</div>', "var(--teal)");
  hidden(t1); show(t1, W("s19", "difference"));
}
hero("C2", T("s19"), T("s20") - 0.35, "map_dimmer on the real board: the red LED follows the knob.", TALL);

/* s20 - s21: modify: flip the range */
const fl = chapter("s20", "s22"); title(fl, "Change one thing: swap the last two numbers", "s20");
{
  const c = box(fl, 110, 200, 1700, 160, "card", '<div style="font:800 52px/160px var(--mono);text-align:center;white-space:nowrap">map(value, 0, 4095, <span class="arg sw">255, 0</span>)</div>');
  hidden(c); show(c, T("s20")); styleAt($(".sw", c), "background", [[0, "transparent"], [W("s20", "swap"), "#ff8a8f55"]]);
  const pos = (t) => sweep(t, T("s21"), 5);
  const k = knobIcon(fl, 330, 420, 330); k.drive((t) => (t < T("s21") ? 0 : pos(t))); hidden(k.r); show(k.r, T("s21"));
  const L = ledIcon(fl, 900, 400, 170, "red"); L.drive((t) => (t < T("s21") ? 0 : 1 - pos(t))); hidden(L.r); show(L.r, T("s21"));
  const b = live(fl, 1250, 470, 520, "brightness", (t) => (t < T("s21") ? "" : mapI(Math.round(4095 * pos(t)), 0, 4095, 255, 0)), "#ff8a8f"); show(b, T("s21"));
  const lr = box(fl, 300, 800, 400, 60, "", '<div style="font:700 34px var(--ui);color:var(--muted);text-align:center">left: bright &nbsp; right: dark</div>'); hidden(lr); show(lr, W("s21", "left"));
  askTop(stage, "PAUSE AND PREDICT", "Swap the last two numbers: 255 down to 0. What happens?", T("s20"), T("s21"), "The knob works backwards: left is bright, right is dark.", { x: 210, y: 790, w: 1500, t1: T("s21") + 0.2 });
}

/* ======================================================================
 * THE BAR: phone battery -> four states
 * ==================================================================== */
const bar = chapter("s22", "s25"); title(bar, "A bar of lights", "s22"); likeTop(T("s22") + 0.4);
{
  const lv = (t) => Math.min(3, Math.floor(sweep(t, T("s23"), 6) * 4));
  const rows = levelRows(bar, 1050, 300, 620, lv); rows.forEach((r) => { hidden(r); show(r, W("s23", "level")); });
  const k = knobIcon(bar, 220, 280, 330); k.drive((t) => sweep(t, T("s23"), 6)); hidden(k.r); show(k.r, T("s23"));
  const L = barLeds(bar, 680, 270, 90, 180); L.all.forEach((e) => { hidden(e); show(e, T("s23")); }); L.drive(lv);
  const cg = pill(bar, 620, 860, "counting from green", "font-size:32px;color:#4ade80"); show(cg, W("s23", "green"));
  exCard("🔋", "Your phone's battery icon", "The more charge, the more bars.", T("s22"), T("s23") - 0.25);
  exCard("🔋", "Only four states", "From empty to full: level 0, 1, 2 or 3.", T("s24"), T("s25") - 0.3, "your phone hides many tiny steps behind each bar.", W("s24", "difference"));
}

/* ======================================================================
 * WIRING: yellow on D18, green on pin 17 (printed TX2), the knob moved up
 * ==================================================================== */
const wr = chapter("s25", "s28"); const wh = title(wr, "Add the yellow and the green LED", "s25"); css(wh, { zIndex: 35, background: "#0b1220" });
{
  const bb = deskCircuit(wr, 90, 17, 19, 160);
  bb.red.drive(() => 0);
  const pot = addPotTop(bb);
  const yR = bb.resistor(["D", 52], ["F", 49]), yL = bb.ledAt(49, "yellow"), yW = bb.wire(["I", 48], ["rm", 48], "#1d1f24", 0);
  const gR = bb.resistor(["D", 54], ["F", 53]), gL = bb.ledAt(53, "green"), gW = bb.wire(["I", 52], ["rm", 52], "#1d1f24", 0);
  yL.drive(() => 0); gL.drive(() => 0);
  [yR, yL.g, yW, gR, gL.g, gW].forEach((e) => gsap.set(e, { opacity: 0 }));
  show([yR, yL.g], W("s25", "yellow")); show([gR, gL.g], W("s25", "green")); show([yW, gW], W("s25", "resistor"));
  const r18 = holeRing(bb, "A", 52, "#ffe14d"); TO(r18, W("s25", "yellow"), 0.4, { opacity: 1 });
  const r17 = holeRing(bb, "A", 54, "#4ade80"); TO(r17, W("s25", "green"), 0.4, { opacity: 1 });
  const rPot = holeRing(bb, "H", 24, "#ffb547"); TO(rPot, W("s27", "knob"), 0.4, { opacity: 1 });

  const usb = box(wr, 840, 190, 960, 96, "", '<div class="banner" style="position:static;display:inline-flex">USB unplugged</div>'); hidden(usb); show(usb, T("s25")); hide(usb, W("s25", "yellow") - 0.2, 0.25);
  const tx = tile(wr, 840, 240, 960, 420, '<div style="font:800 46px var(--display)">Pin 17 is printed <span style="color:#4ade80;font-family:var(--mono)">TX2</span></div><div style="font:800 64px/1.6 var(--mono);margin-top:36px"><span style="color:#ffe14d">D18</span> &rarr; yellow<br><span style="color:#4ade80">TX2</span> &rarr; green</div>', "#4ade80");
  hidden(tx); show(tx, T("s25b")); hide(tx, T("s26") - 0.2, 0.25);
  const legs = tile(wr, 840, 240, 960, 420, '<div style="font:800 46px var(--display)">Which way round?</div><div style="font:700 44px/1.7 var(--ui);margin-top:30px">Long leg &rarr; toward the pin<br>Short leg &rarr; <b style="color:#6fa0ff">&minus; rail</b></div>', "var(--amber)");
  hidden(legs); show(legs, T("s26")); hide(legs, T("s27") - 0.2, 0.25);
  const mv = tile(wr, 840, 240, 960, 420, '<div style="font:800 46px var(--display)">Crowded board?</div><div style="font:600 38px/1.5 var(--ui);margin-top:30px">Move the knob higher up. Its wires move with it.<br><b style="color:var(--amber)">Rails split in the middle? Keep the bridges.</b></div>', "var(--teal)");
  hidden(mv); show(mv, T("s27"));
}
hero("C1", W("s25", "yellow"), T("s25b") - 0.35, "The yellow and green LEDs going in on the real board.", { x: 840, y: 190, w: 960, h: 540 });

/* ======================================================================
 * THE LEVEL LINE: a trap, then the fix
 * ==================================================================== */
const lv = chapter("s28", "s33"); const lh = title(lv, "", "s28");
textAt(lh, [[0, "The obvious level line"], [T("s30") - 0.2, "map() drops the decimals"], [T("s31") - 0.2, "Level 3 hides at the very end"], [T("s32") - 0.2, "The fix: four levels, one mark longer"]]);
{
  const c1 = box(lv, 210, 200, 1500, 150, "card", '<div style="font:800 54px/150px var(--mono);text-align:center;white-space:nowrap">int level = map(value, 0, 4095, 0, 3);</div>');
  hidden(c1); show(c1, T("s28")); hide(c1, T("s32") - 0.2, 0.25);
  const c2 = box(lv, 210, 200, 1500, 150, "card", '<div style="font:800 54px/150px var(--mono);text-align:center;white-space:nowrap">int level = map(value, 0, <span style="color:var(--amber)">4096</span>, 0, <span style="color:var(--amber)">4</span>);</div>');
  css(c2, { borderColor: "var(--amber)" }); hidden(c2); show(c2, T("s32"));
  askTop(stage, "PAUSE AND PREDICT", "With this line, how often do you see all three LEDs on?", T("s29"), T("s30"), "Almost never.", { x: 210, y: 790, w: 1500, t1: T("s30") + 1.2 });
  // s30: whole numbers
  const wn = box(lv, 360, 420, 1200, 220, "", '<div style="display:flex;gap:50px;justify-content:center;align-items:center;font:800 110px var(--mono)"><span style="color:#ffe3b8">2.9</span><span style="color:var(--muted)">&rarr;</span><span style="color:var(--amber)">2</span></div><div style="font:600 36px var(--ui);text-align:center;color:var(--muted);margin-top:10px">whole numbers only: everything after the point is dropped</div>');
  hidden(wn); show(wn, W("s30", "whole")); hide(wn, T("s31") - 0.2, 0.25);
  // s31 / s32: slices of the knob
  const X = 160, Wd = 1600, Y = 470;
  const strip = (cuts, labels, cols) => {
    const g = box(lv, X, Y, Wd, 300, "");
    cuts.forEach((a, i) => {
      const b = cuts[i + 1]; if (b == null) return;
      const s = box(g, Wd * a, 0, Math.max(6, Wd * (b - a) - 6), 120, ""); css(s, { background: cols[i], borderRadius: "12px", font: "800 40px/120px var(--ui)", textAlign: "center", color: "#0b1220", overflow: "visible", whiteSpace: "nowrap" });
      s.textContent = labels[i];
    });
    const sv = svgEl(g, "svg", { width: Wd, height: 300, viewBox: `0 0 ${Wd} 300` }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible" });
    txt(sv, 0, 180, "0", { "font-size": 38, fill: "#ffb547", "font-family": "Consolas" });
    txt(sv, Wd, 180, "4095", { "font-size": 38, fill: "#ffb547", "font-family": "Consolas", "text-anchor": "end" });
    return hidden(g);
  };
  const COLS = ["#2a3550", "#4ade80", "#ffe14d", "#ff5d6c"];
  const s1 = strip([0, 1 / 3, 2 / 3, 4094.5 / 4095, 1], ["level 0", "level 1", "level 2", ""], COLS);
  show(s1, T("s31")); hide(s1, T("s32") - 0.2, 0.25);
  const tip = pill(lv, X + Wd - 470, Y + 200, "level 3: only the very last mark &uarr;", "font-size:32px;color:#ff8a8f"); show(tip, W("s31", "last")); hide(tip, T("s32") - 0.2, 0.25);
  const nv = pill(lv, X + Wd - 470, Y + 270, "and the ruler may never get there", "font-size:30px;color:var(--muted)"); show(nv, W("s31", "never")); hide(nv, T("s32") - 0.2, 0.25);
  const s2 = strip([0, 0.25, 0.5, 0.75, 1], ["level 0", "level 1", "level 2", "level 3"], COLS);
  show(s2, W("s32", "equal") - 0.3);
  const lg = pill(lv, X + Wd - 560, Y + 200, "4096 / 4 = 1024 marks for every level", "font-size:32px;color:var(--teal)"); show(lg, W("s32", "equal"));
}
tour("level_bar", T("s33") - 0.4, T("s38") - 0.3, [
  [W("s33", "Setup"), "void setup()", "pinMode(RED_PIN"], [W("s33", "loop"), "int value = analogRead"], [W("s33", "map"), "int level = map"],
  [W("s34", "zero"), "if (level == 0)", "digitalWrite(RED_PIN, LOW);"], [W("s34", "one"), "} else if (level == 1)", "digitalWrite(RED_PIN, LOW);"], [W("s34", "two"), "} else if (level == 2)", "digitalWrite(RED_PIN, LOW);"],
  [W("s35", "else"), "} else {", "digitalWrite(RED_PIN, HIGH);"], [T("s36"), "int level = map"], [T("s37"), "} else if (level == 2)"]]);
askTop(stage, "PAUSE AND PREDICT", "The knob is just past the middle. Which LEDs are on?", T("s36"), T("s37"), "Green and yellow: just past the middle is level 2.", { x: 210, y: 790, w: 1500, t1: T("s38") - 0.3 });

/* s38: the real bar */
const rb = chapter("s38", "s39");
{
  const c = bigCode(rb, 1010, 200, 820, "map(value, 0, 4096, 0, 4)", { size: 40 }); show(c.c, T("s38"));
  const rows = levelRows(rb, 1060, 380, 720, null); rows.forEach((r) => { hidden(r); show(r, T("s38") + 0.3); });
}
hero("C3", T("s38"), T("s39") - 0.35, "level_bar on the real board: one light at a time, then back.", TALL);

/* ======================================================================
 * THE COMMON MISTAKE: yellow in backwards
 * ==================================================================== */
const mk = chapter("s39", "s43"); const mh = title(mk, "", "s39");
textAt(mh, [[0, ""], [T("s41") - 0.2, "An LED is a one-way street for current"]]);
{
  const sm = serialMon(mk, 1010, 200, 800, 420, () => "3", T("s39") + 0.5, 0.25, 6, 44); hidden(sm); show(sm, T("s40")); hide(sm, T("s41") - 0.2, 0.25);
  const cw = tile(mk, 1010, 650, 800, 200, '<div style="font:700 38px/1.4 var(--ui)">Level 3: the code wants yellow on.<br><b style="color:var(--amber)">So: the wiring.</b></div>', "var(--amber)");
  hidden(cw); show(cw, W("s40", "wiring") - 0.6); hide(cw, T("s41") - 0.2, 0.25);
  ask(mk, "QUICK QUESTION", "Green and red light up, yellow stays dark. Code, or wiring?", W("s39", "Quick"), T("s40"), "Take the temperature first: print the level.", { x: 1000, y: 200, w: 830, t1: T("s40") - 0.05 });
  // s41 - s42: the LED's direction
  const d = box(mk, 160, 220, 1600, 640, ""); hidden(d); show(d, T("s41"));
  const ok = ledIcon(d, 260, 60, 170, "yellow"); ok.drive((t) => (t > W("s41", "long") ? 1 : 0));
  const bad = ledIcon(d, 1180, 60, 170, "yellow"); bad.drive(() => 0); css(bad.r, { transform: "rotate(180deg)" });
  d.insertAdjacentHTML("beforeend", '<div style="position:absolute;left:120px;top:470px;width:460px;font:700 36px/1.4 var(--ui);text-align:center">long leg &rarr; short leg<br><span style="color:#4ade80">current flows</span></div>' +
    '<div style="position:absolute;left:1040px;top:470px;width:460px;font:700 36px/1.4 var(--ui);text-align:center">turned around<br><span style="color:#ff8a8f">dark, nothing damaged</span></div>');
  const fx = pillC(mk, 900, "Flip it, and the bar is complete.", "font-size:40px;color:var(--teal)"); show(fx, W("s42", "Flip"));
}
{ // after the clip ends (it is shorter than s39 + s40): the same fault, drawn: level 3, yellow dark
  const end = T("s39") + EP08_CLIP_SECONDS.C4 - 1 / 30;
  if (end < T("s41") - 0.5) {
    const g = box(mk, 380, 170, 300, 700, ""); hidden(g); show(g, end - 0.35); hide(g, T("s41") - 0.2, 0.25);
    const L = barLeds(g, 100, 40, 110, 210); L.drive(() => 3, 1);
    g.insertAdjacentHTML("beforeend", '<div style="position:absolute;left:-120px;top:660px;width:540px;font:700 34px var(--ui);text-align:center;color:#ffe3b8">yellow stays dark</div>');
  }
}
hero("C4", T("s39"), T("s41") - 0.35, "Mistake: the yellow LED is in backwards, red and green light, yellow stays dark.", TALL);

/* ======================================================================
 * EXPLAIN, CHALLENGE, OUTRO
 * ==================================================================== */
const ex = chapter("s43", "s45"); title(ex, "In your own words", "s43");
{
  const li = bigCode(ex, 210, 480, 1500, "int level = map(value, 0, 4095, 0, 3);", { size: 50 }); show(li.c, T("s43")); hide(li.c, T("s44") - 0.2, 0.25);
  const a = tile(ex, 210, 470, 1500, 330, '<div style="font:700 40px/1.5 var(--ui)">map() rounds down &rarr; level 3 only at the very end of the ruler &rarr; the ruler rarely gets there.</div>', "var(--teal)");
  hidden(a); show(a, T("s44"));
  ask(ex, "PAUSE AND EXPLAIN", "Why did the first level line almost never light all three LEDs?", T("s43"), T("s44"), "One sentence is enough.", { x: 210, y: 200, w: 1500, t1: S1("s44") });
  likeTop(T("s44") + 0.3);
}
const ch = chapter("s45", "s50"); title(ch, "Your turn: the Rotary Safe Lock", "s45");
{
  const pos = (t) => sweep(t, T("s45"), 7);
  const k = knobIcon(ch, 180, 220, 300); k.drive(pos);
  const dial = live(ch, 540, 260, 380, "dial: map(…, 0, 99)", (t) => mapI(reading(pos(t), Math.floor(t * 5)), 0, 4095, 0, 99)); show(dial, W("s45", "print"));
  const tg = tile(ch, 1000, 210, 800, 330, '<div style="font:700 32px var(--ui);color:var(--muted)">the secret code</div><div style="font:800 76px/1.5 var(--mono);margin-top:16px;white-space:nowrap">25 <span style="color:var(--muted);font-size:44px">&#9654; press</span><br>70 <span style="color:var(--muted);font-size:44px">&#9654; press</span> 40 <span style="color:var(--muted);font-size:44px">&#9654; press</span></div>', "var(--amber)");
  hidden(tg); show(tg, W("s46", "screen") - 0.4);
  const bt = btnIcon(ch, 220, 600, 150); bt.press([[T("s46") + 1, T("s46") + 1.4], [T("s46") + 2.4, T("s46") + 2.8]]); hidden(bt.r); show(bt.r, W("s46", "button"));
  const rg = rgbIcon(ch, 560, 560, 150); rg.drive((t) => (t >= W("s47", "red") && t < W("s47", "red") + 0.8 ? [255, 0, 0] : t > W("s47", "green") && t < W("s47", "red") ? [0, 255, 0] : [0, 0, 60])); hidden(rg.r); show(rg.r, T("s47"));
  const tw = tile(ch, 1000, 580, 800, 300, '<div style="font:800 40px var(--display);color:var(--amber)">The twist: a knob is never exact</div><div style="font:700 36px/1.5 var(--mono);margin-top:16px">value &gt;= 22 <b style="color:var(--teal)">&amp;&amp;</b> value &lt;= 28</div><div style="font:600 30px var(--ui);margin-top:10px;color:var(--muted)">&amp;&amp; = and: both checks must be true</div>', "var(--amber)");
  hidden(tw); show(tw, T("s48"));
  const hint = pill(ch, 860, 940, "hint: <b style=\"font-family:var(--mono)\">int step = 0;</b> counts the right numbers", "font-size:32px;color:var(--teal)"); show(hint, W("s49", "step") - 0.3);
}
const out = chapter("s50", null); title(out, "Three things you can now do", "s50");
{
  [["One range &rarr; another", "map()", W("s50", "Map")], ["It rounds down", "plan your ranges", W("s50", "rounds")], ["LED backwards = dark", "flip it, nothing breaks", W("s50", "LED")]].forEach(([a, b, t0], i) => {
    const c = tile(out, 115 + i * 575, 230, 540, 340, `<div style="font:800 42px var(--display);color:var(--teal)">${a}</div><div style="font:700 38px/1.5 var(--mono);margin-top:40px">${b}</div>`);
    hidden(c); show(c, t0); hide(c, T("s51") - 0.15, 0.25);
  });
  const next = tile(out, 210, 200, 1500, 400, '<div class="kicker">NEXT: EPISODE 9 &middot; MINI PROJECT 1</div><div style="font:800 62px var(--display);margin-top:26px">A pedestrian crossing</div><div style="font:600 36px var(--ui);margin-top:20px;color:var(--muted)">Car lights, a walk light, a button and today\'s knob.</div>');
  hidden(next); show(next, T("s51"));
  const L = barLeds(next, 1120, 110, 70, 110, { row: true });
  L.leds.forEach((Ld, i) => Ld.drive((t) => (((Math.floor((t - T("s51")) / 1.2) % 3) + 3) % 3 === 2 - i ? 1 : 0)));
  note(out, "Post your safe lock code in the comments. One solution is in the lesson folder.", W("s51", "Post"), 650);
  note(out, "github.com/emjnbulut/esp32-from-zero &rarr; lessons/08-map-and-level-bar", W("s51", "Post"), 790);
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 }); TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}
window.__seek(0);
window.__ready = true;
