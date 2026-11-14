/* Recap 2 (episodes 5-10): segment-anchored scenes. One montage clip (footage/recap2/M.mp4), then three parts, each:
 * the episode's own picture -> what actually happens -> a live trace with a memory panel -> scored quiz questions.
 * Helpers are shared with episode 10 (copied, so each episode page stays self-contained). */
const stage = $("#stage");
const CLIP_SECONDS = { M: 8.8 }; // footage/recap2/M.mp4 (grows to ~13 s when the ep09/ep10 clips are added)
function hero(id, t0, requestedEnd, description, opts = {}) {
  const lead = opts.full ? Math.min(0.3, t0) : 0;
  const tail = opts.full ? 0.35 : 0;
  const t1 = Math.min(requestedEnd, t0 + CLIP_SECONDS[id] - lead - tail - 1 / 30);
  if (!(t1 > t0)) throw new Error("No usable recap 2 footage: " + id);
  return heroClip(stage, id, t0, t1, description, opts);
}
const WIN = { x: 60, y: 170, w: 1200, h: 675 };
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
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const mapI = (v, a, b, c, d) => Math.trunc((v - a) * (d - c) / (b - a) + c);
const txt = (g, x, y, s, attrs) => { const e = svgEl(g, "text", Object.assign({ x, y, "font-family": "Segoe UI", "font-weight": 700, "font-size": 26, fill: "#8fa1c0" }, attrs)); e.textContent = s; return e; };
const pill = (parent, x, y, html, style = "") => {
  const p = box(parent, x, y, 0, 0, "", `<span class="pill" style="font-size:30px;${style}">${html}</span>`);
  css(p, { width: "auto", height: "auto", whiteSpace: "nowrap" });
  return hidden(p);
};

/* ---- the reflex game simulator: the same rules as reflex_game.ino, in seconds ----
 * game({ t0, start, red, yellow, react, show, early }) -> (t) => { state, inState, color }
 * start: the start press; react: seconds from green to the press (null = no press yet); early: presses during red/yellow
 * (drawn only: the real sketch ignores them). color = the RGB result: "blue" (press to start), "off", "green", "yellow", "red" */
const RESULT = (r) => (r < 0.25 ? "green" : r < 0.5 ? "yellow" : "red");
function game(o) {
  const red = o.red != null ? o.red : 1, ye = o.yellow != null ? o.yellow : 2, sh = o.show != null ? o.show : 3;
  return (t) => {
    if (o.start == null || t < o.start) return { state: 0, inState: 0, color: "blue" };
    const a2 = o.start + red, a3 = a2 + ye;
    if (t < a2) return { state: 1, inState: t - o.start, color: "off" };
    if (t < a3) return { state: 2, inState: t - a2, color: "off" };
    if (o.react == null || t < a3 + o.react) return { state: 3, inState: t - a3, color: "off" };
    const a4 = a3 + o.react;
    if (t < a4 + sh) return { state: 4, inState: t - a4, color: RESULT(o.react), reaction: o.react };
    return { state: 0, inState: 0, color: "blue", reaction: o.react };
  };
}
/** the three lamps for a step: [red, yellow, green] */
const LAMPS = (s) => [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0]][s.state];
const RGB = { blue: "#3d6bff", off: "#2a3140", green: "#36e07a", yellow: "#ffb62e", red: "#ff4d5a", flash: "#ff4d5a" };

/** a drawn signal (three lamps) + the result light (the RGB LED); drive(fn) with fn(t) = game state */
function reflexIcon(parent, x, y, s = 1) {
  const r = box(parent, x, y, 420 * s, 470 * s, "");
  r.innerHTML = `<svg width="${420 * s}" height="${470 * s}" viewBox="0 0 420 470" style="position:absolute;left:0;top:0;overflow:visible">
    <rect x="20" y="10" width="150" height="400" rx="30" fill="#1b2130" stroke="#3a4560" stroke-width="5"/>
    <path d="M95 410 V465" stroke="#3a4560" stroke-width="16"/>
    <circle class="c0" cx="95" cy="85" r="50"/><circle class="c1" cx="95" cy="210" r="50"/><circle class="c2" cx="95" cy="335" r="50"/>
    <rect x="240" y="120" width="160" height="200" rx="26" fill="#1b2130" stroke="#3a4560" stroke-width="5"/>
    <path d="M320 320 V465" stroke="#3a4560" stroke-width="16"/>
    <circle class="w" cx="320" cy="220" r="62"/>
    <text x="95" y="-14" text-anchor="middle" font-size="28" font-weight="700" fill="#8fa1c0" font-family="Segoe UI">lights</text>
    <text x="320" y="96" text-anchor="middle" font-size="28" font-weight="700" fill="#8fa1c0" font-family="Segoe UI">result</text></svg>`;
  const cs = [$(".c0", r), $(".c1", r), $(".c2", r)], wl = $(".w", r);
  const ON = ["#ff4d5a", "#ffd23a", "#36e07a"], OFF = ["#4a1f25", "#4a3f17", "#173d26"];
  const drive = (fn) => dyn((t) => {
    const st = fn(t), L = LAMPS(st);
    cs.forEach((c, i) => { c.setAttribute("fill", L[i] ? ON[i] : OFF[i]); c.style.filter = L[i] ? `drop-shadow(0 0 22px ${ON[i]})` : "none"; });
    const col = RGB[st.color] || RGB.off, lit = st.color !== "off";
    wl.setAttribute("fill", st.color === "blue" ? "#22356e" : col); wl.style.filter = lit ? `drop-shadow(0 0 26px ${col})` : "none";
  });
  return { r, drive };
}
/** the five steps as a row of boxes with a way back; fn(t) = game state, the current step is lit */
const STEPS = [["0", "wait for a start", "#3d6bff"], ["1", "red", "#ff4d5a"], ["2", "yellow", "#ffd23a"], ["3", "green: go!", "#36e07a"], ["4", "show the result", "#b48cff"]];
function stepRow(parent, x, y, w = 1700, fn = null, o = {}) {
  const n = STEPS.length, gap = o.gap || 40, bw = (w - gap * (n - 1)) / n, bh = o.bh || 170, H = bh + 90;
  const g = box(parent, x, y, w, H, "");
  const els = STEPS.map(([k, lab, col], i) => {
    const e = box(g, i * (bw + gap), 0, bw, bh, "stepbox", `<div class="n" style="color:${col}">${k}</div><div class="l">${lab}</div>`);
    e.style.setProperty("--c", col);
    return e;
  });
  const sv = svgEl(g, "svg", { width: w, height: H, viewBox: `0 0 ${w} ${H}` }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible", pointerEvents: "none" });
  svgEl(sv, "defs").innerHTML = '<marker id="ah10" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#5f6f8f"/></marker>';
  const arr = (d) => svgEl(sv, "path", { d, fill: "none", stroke: "#5f6f8f", "stroke-width": 6, "marker-end": "url(#ah10)" });
  for (let i = 0; i < n - 1; i++) arr(`M${i * (bw + gap) + bw + 4} ${bh / 2} H${(i + 1) * (bw + gap) - 10}`);
  arr(`M${w - bw / 2} ${bh + 6} V${bh + 60} H${bw / 2} V${bh + 16}`);
  if (fn) dyn((t) => { const s = fn(t).state; els.forEach((e, i) => e.classList.toggle("on", i === s)); });
  return { g, els };
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
function knobIcon(parent, x, y, w = 240) {
  const r = box(parent, x, y, w, w, "");
  const ticks = Array.from({ length: 11 }, (_, i) => { const a = (-225 + 27 * i) * Math.PI / 180; return `<path d="M${100 + 78 * Math.cos(a)} ${100 + 78 * Math.sin(a)} L${100 + 92 * Math.cos(a)} ${100 + 92 * Math.sin(a)}" stroke="#5f6f8f" stroke-width="5" stroke-linecap="round"/>`; }).join("");
  r.innerHTML = `<svg width="${w}" height="${w}" viewBox="0 0 200 200" style="position:absolute;left:0;top:0">${ticks}
    <circle cx="100" cy="100" r="68" fill="#c9a24a" stroke="#8a6f2c" stroke-width="4"/><circle cx="100" cy="100" r="52" fill="#2b3140" stroke="#48526a" stroke-width="4"/>
    <g class="ptr"><rect x="94" y="52" width="12" height="42" rx="6" fill="#ffb547"/></g></svg>`;
  const ptr = $(".ptr", r);
  const drive = (fn) => dyn((t) => ptr.setAttribute("transform", `rotate(${-135 + 270 * fn(t)} 100 100)`));
  return { r, drive };
}
/** a recreated Serial Monitor; lines = [[t, text], ...] appear at their times */
function serialAt(parent, x, y, w, h, lines, size = 40) {
  const c = box(parent, x, y, w, h, "card", `<div style="height:58px;display:flex;align-items:center;padding:0 24px;border-bottom:2px solid #2c3b5e;font:700 26px var(--ui);color:var(--muted)">Serial Monitor<span style="margin-left:auto;font:600 22px var(--mono)">115200 baud</span></div><div class="ln" style="padding:12px 28px;font:600 ${size}px/${Math.round(size * 1.35)}px var(--mono);color:#b9f3ec;white-space:pre"></div>`);
  const ln = $(".ln", c);
  dyn((t) => { const s = lines.filter(([ts]) => t >= ts).map(([, s]) => s).slice(-6).join("\n"); if (ln.__s !== s) { ln.textContent = s; ln.__s = s; } });
  return c;
}
function live(parent, x, y, w, label, fn, color = "var(--amber)") {
  const c = box(parent, x, y, w, 160, "live", `<div class="k">${label}</div><div class="v" style="color:${color}"></div>`);
  const v = $(".v", c);
  dyn((t) => { const s = String(fn(t)); if (v.__s !== s) { v.textContent = s; v.__s = s; } });
  return hidden(c);
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
const repo = "Full code: <b>github.com/emjnbulut/esp32-from-zero</b> &rarr; lessons";
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
const ms = (s) => Math.round(s * 1000);
const dot = (col) => `<span style="display:inline-block;width:34px;height:34px;border-radius:50%;background:${col};vertical-align:-5px;box-shadow:0 0 14px ${col}"></span>`;
const LEGEND = `<div style="font:700 36px/1.8 var(--ui)">${dot(RGB.green)} &nbsp;under <b>250 ms</b>: fast<br>${dot(RGB.yellow)} &nbsp;under <b>500 ms</b>: okay<br>${dot(RGB.red)} &nbsp;slower: slow</div>`;

/* ---- recap helpers ---- */
const Q = (n, ep) => `QUESTION ${n} / 7 &middot; EPISODE ${ep}`;
const quiz = (n, ep, q, id, ans, answer, o = {}) => askTop(stage, Q(n, ep), q, T(id), T(ans), answer, Object.assign({ x: 210, y: 790, w: 1500, t1: S1(ans) }, o));
/** a PWM wave: duty(t) in 0..1; three periods drawn */
function pwmWave(parent, x, y, w, h, duty) {
  const g = box(parent, x, y, w, h, "");
  const sv = svgEl(g, "svg", { width: w, height: h, viewBox: `0 0 ${w} ${h}` }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  svgEl(sv, "path", { d: `M0 ${h - 10} H${w}`, stroke: "#2c3b5e", "stroke-width": 3 });
  const p = svgEl(sv, "path", { fill: "none", stroke: "#ffb547", "stroke-width": 7, "stroke-linejoin": "round" });
  const lab = txt(sv, w, -14, "", { "text-anchor": "end", "font-size": 30, fill: "#ffb547" });
  dyn((t) => {
    const d = clamp(duty(t), 0, 1), per = w / 3, top = 10, bot = h - 10;
    let s = `M0 ${bot}`;
    for (let i = 0; i < 3; i++) { const x0 = i * per, x1 = x0 + per * d; s += ` V${top} H${x1} V${bot} H${x0 + per}`; }
    if (p.__s !== s) { p.setAttribute("d", s); p.__s = s; }
    const l = `on ${Math.round(d * 100)} % of every cycle`; if (lab.textContent !== l) lab.textContent = l;
  });
  return g;
}
/** a glowing LED disc; level(t) in 0..1, color = css rgb */
function glowLed(parent, x, y, r, level, color = "255,77,90") {
  const e = box(parent, x, y, r * 2, r * 2, "");
  css(e, { borderRadius: "50%" });
  dyn((t) => { const v = clamp(level(t), 0, 1); e.style.background = `rgba(${color},${0.12 + 0.88 * v})`; e.style.boxShadow = `0 0 ${10 + 80 * v}px rgba(${color},${v})`; });
  return e;
}
/** a number line from a to b with a moving marker; val(t) */
function numLine(parent, x, y, w, a, b, val, label, col = "#ffb547") {
  const g = box(parent, x, y, w, 130, "");
  const sv = svgEl(g, "svg", { width: w, height: 130, viewBox: `0 0 ${w} 130` }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  svgEl(sv, "rect", { x: 0, y: 50, width: w, height: 16, rx: 8, fill: "#22304d" });
  txt(sv, 0, 110, String(a), { "font-size": 28 }); txt(sv, w, 110, String(b), { "font-size": 28, "text-anchor": "end" });
  txt(sv, 0, 30, label, { "font-size": 28, fill: "#c9d1dc" });
  const m = svgEl(sv, "g", {}); svgEl(m, "circle", { cx: 0, cy: 58, r: 20, fill: col });
  const mt = txt(m, 0, 30, "", { "font-size": 34, "text-anchor": "middle", fill: col, "font-family": "Cascadia Code, Consolas, monospace" });
  dyn((t) => { const v = val(t); m.setAttribute("transform", `translate(${((v - a) / (b - a)) * w} 0)`); const s = String(Math.round(v)); if (mt.textContent !== s) mt.textContent = s; });
  return g;
}

/* ======================================================================
 * COLD OPEN: the montage, then the promise
 * ==================================================================== */
const cold = SC(); SET(cold, 0, { opacity: 1 }); SET(cold, CUT, { opacity: 0 });
{
  const h = box(cold, 1310, 150, 560, 200, "", '<div style="font:800 58px/1.15 var(--display)">Recap 2<br><span style="color:var(--amber)">episodes 5&ndash;10</span></div>');
  hidden(h); show(h, 0.4);
  const list = box(cold, 1310, 380, 560, 420, "", ["&#128308; a breathing LED", "&#127752; any color", "&#127899;&#65039; a knob dimmer", "&#128267; a level bar", "&#128678; a crossing", "&#9889; a reflex game"].map((s) => `<div style="font:700 34px/1.75 var(--ui)">${s}</div>`).join(""));
  hidden(list); show(list, 0.8);
  const pr = tile(cold, 1310, 380, 560, 380, '<div class="kicker">TODAY</div><div style="font:800 44px/1.3 var(--display);margin-top:20px">Nothing new.<br>Read, trace, and</div><div style="font:800 60px var(--display);margin-top:16px;color:var(--amber)">7 questions</div>', "var(--amber)");
  hidden(pr); hide(list, T("s02") - 0.2, 0.25); show(pr, T("s02"));
}
hero("M", 0, CUT, "Montage: ep05 breathing LED, ep06 colors, ep07 knob dimmer, ep08 level bar (+ ep09 crossing, ep10 reflex game).", WIN);

/* ======================================================================
 * THE RULES: paper, pause, a point
 * ==================================================================== */
const ru = chapter("s03", "s05"); title(ru, "How this works", "s03");
{
  const paper = tile(ru, 160, 200, 760, 560, '<div style="font-size:120px;line-height:1">&#128221;</div><div style="font:700 38px/1.7 var(--ui);margin-top:24px">1. a question<br>2. <b style="color:var(--amber)">pause</b> and answer<br>3. right? <b style="color:var(--teal)">+1 point</b></div>', "var(--amber)");
  hidden(paper); show(paper, T("s03"));
  const sc = live(ru, 300, 790, 480, "your score", (t) => (t < W("s03", "point") ? "0 / 7" : "1 / 7"), "#36e07a"); show(sc, T("s03") + 0.6);
  const parts = [["1", "Making light", "PWM &middot; the color LED", "5&ndash;6", "#ff7a59"], ["2", "Reading a knob", "analogRead &middot; map()", "7&ndash;8", "#ffb547"], ["3", "Remembering steps", "state &middot; millis &middot; the drawer", "9&ndash;10", "#36e07a"]];
  parts.forEach(([n, a, b, ep, c], i) => {
    const e = tile(ru, 1000, 200 + i * 190, 800, 170, `<div style="display:flex;gap:28px;align-items:center"><div style="font:800 76px var(--mono);color:${c}">${n}</div><div><div style="font:800 40px var(--display)">${a}</div><div style="font:600 28px var(--ui);color:var(--muted);margin-top:6px">${b} &middot; episodes ${ep}</div></div></div>`, c);
    hidden(e); show(e, T("s04") + 0.3 + i * 0.5);
  });
  const nw = pill(ru, 1340, 150, "New here? Start at Episode 1 &rarr;", "font-size:28px;color:var(--teal)"); show(nw, W("s04", "New")); hide(nw, T("s05") - 0.3, 0.2);
}

/* ======================================================================
 * PART 1: making light: PWM (fan), the breathing trace, Q1; the color LED, Q2
 * ==================================================================== */
const p1 = chapter("s05", "s08"); const p1h = title(p1, "", "s05");
textAt(p1h, [[0, "Part 1: making light"], [T("s06") - 0.2, "PWM: on and off, very fast"]]);
{
  exCard("&#127744;", "The ceiling fan", "It spins so fast that your eye sees a blur, not the blades.", T("s05") + 0.5, T("s06") - 0.25);
  const duty = (t) => 0.5 + 0.42 * Math.sin((t - T("s06")) * 1.3);
  const wv = pwmWave(p1, 160, 300, 1100, 240, duty); hidden(wv); show(wv, T("s06"));
  const led = glowLed(p1, 1450, 280, 130, duty); hidden(led); show(led, T("s06") + 0.3);
  note(p1, "about 1000 times a second: the eye only sees the average", W("s06", "longer"), 640);
  const lim = tile(p1, 160, 760, 1600, 170, '<div style="font:700 34px/1.5 var(--ui);color:#ffe3b8"><b style="color:var(--amber)">The difference:</b> the fan really moves. The LED is never half on: only ever on or off.</div>', "var(--amber)");
  hidden(lim); show(lim, T("s07"));
}
const tr1 = chapter("s08", "s10"); title(tr1, "Trace: the breathing LED", "s08");
{
  const t0 = T("s08") + 1.0, RATE = 70;                 // 70 brightness steps per second of video (the real one: 250 per s)
  const sim1 = (t) => { const k = Math.max(0, (t - t0) * RATE) % 510; return k <= 255 ? { b: Math.round(k), step: 1 } : { b: Math.round(510 - k), step: -1 }; };
  const c = bigCode(tr1, 90, 200, 1180, "if (now - lastStep >= 4) {\n  lastStep = now;\n  brightness = brightness + step;\n  if (brightness >= 255) {\n    step = -1;\n  }\n  analogWrite(LED_PIN, brightness);\n}", { size: 34 });
  show(c.c, T("s08")); c.hl([[T("s08") + 0.4, 0], [W("s08", "brightness"), 2], [W("s08", "top"), 3], [W("s08", "negative"), 4], [T("s09"), 4]]);
  const mem = tile(tr1, 1340, 200, 480, 120, '<div class="kicker">MEMORY</div>', "var(--teal)"); hidden(mem); show(mem, T("s08") + 0.3);
  const vb = live(tr1, 1340, 340, 480, "brightness", (t) => sim1(t).b, "#ffb547"); show(vb, T("s08") + 0.6);
  const vs = live(tr1, 1340, 520, 480, "step", (t) => (sim1(t).step > 0 ? "+1" : "-1"), "#5aa9ff"); show(vs, T("s08") + 0.9);
  const led = glowLed(tr1, 1480, 720, 100, (t) => sim1(t).b / 255); hidden(led); show(led, T("s08") + 0.6);
  const sw = pill(tr1, 120, 760, "&#127904; like a swing turning around at the top", "font-size:30px;color:var(--teal)"); show(sw, W("s08", "swing"));
  ask(tr1, "PAUSE AND PREDICT", "Brightness just reached the top. What is the step now?", T("s09"), W("s09", "Watch"), "-1: from now on, every step goes down.", { x: 110, y: 820, w: 1200, t1: S1("s09") });
}
const q1 = chapter("s10", "s12"); title(q1, "Question 1", "s10");
{
  const c = bigCode(q1, 360, 200, 1200, "analogWrite(LED_PIN, 64);", { size: 52 }); show(c.c, T("s10"));
  const wv = pwmWave(q1, 360, 420, 1200, 220, () => 64 / 255); hidden(wv); show(wv, T("s11"));
  quiz(1, 5, "analogWrite(pin, 64): how much of each cycle is the pin on?", "s10", "s11", "About a quarter: 255 is always on.");
}
const rg = chapter("s12", "s14"); const rgh = title(rg, "", "s12");
textAt(rgh, [[0, "The color LED: three lights in one"], [T("s13") - 0.2, "Light adds up"]]);
{
  exCard("&#128241;", "Dots on a phone screen", "Three small lights in one package: red, green and blue.", T("s12") + 0.4, T("s13") - 0.25);
  const mix = box(rg, 160, 220, 900, 460, "", `<svg width="900" height="460" viewBox="0 0 900 460" style="position:absolute;left:0;top:0;mix-blend-mode:normal">
    <g style="mix-blend-mode:screen"><circle cx="330" cy="220" r="170" fill="#ff2a2a"/><circle cx="560" cy="220" r="170" fill="#2aff4a"/></g>
    <text x="445" y="236" text-anchor="middle" font-family="Segoe UI" font-weight="800" font-size="40" fill="#1b1600">yellow</text></svg>`);
  css($("svg", mix), { isolation: "isolate" }); hidden(mix); show(mix, T("s13"));
  const pt = tile(rg, 160, 720, 900, 170, '<div style="font:700 32px/1.5 var(--ui);color:#ffe3b8"><b style="color:var(--amber)">The difference:</b> paint subtracts (red + green = brown), light adds (red + green = yellow).</div>', "var(--amber)");
  hidden(pt); show(pt, T("s13") + 0.3);
  const c = bigCode(rg, 1140, 260, 680, "setColor(255, 255, 0);", { size: 42 }); show(c.c, W("s13", "coffee") - 0.3);
  const cm = pill(rg, 1150, 420, "&#9749; one call, three analogWrites", "font-size:30px;color:var(--teal)"); show(cm, W("s13", "coffee"));
}
const q2 = chapter("s14", "s16"); title(q2, "Question 2", "s14");
{
  const c = bigCode(q2, 360, 200, 1200, "setColor(255, 0, 255);", { size: 56 }); show(c.c, T("s14"));
  const sw = box(q2, 810, 400, 300, 300, "", '<div style="width:260px;height:260px;margin:20px;border-radius:50%;background:#ff3df0;box-shadow:0 0 80px #ff3df0"></div>');
  hidden(sw); show(sw, T("s15"));
  quiz(2, 6, "setColor(255, 0, 255). Which color?", "s14", "s15", "Magenta: full red + full blue, no green.");
}

/* ======================================================================
 * PART 2: reading a knob: the slide, the ruler, the city map, the dimmer trace, Q3, Q4
 * ==================================================================== */
const p2 = chapter("s16", "s20"); const p2h = title(p2, "", "s16");
textAt(p2h, [[0, "Part 2: reading a knob"], [T("s17") - 0.2, "analogRead: a ruler with 4096 marks"], [T("s18") - 0.2, "map(): the city map"], [T("s19") - 0.2, "Whole numbers, rounded down"]]);
{
  exCard("&#128719;", "A playground slide", "A strip of resistance, a contact that slides along it: the middle leg gives the voltage where it sits.", T("s16") + 0.4, T("s17") - 0.25);
  const pos = (t) => sweep(t, T("s17"), 5);
  const k = knobIcon(p2, 160, 230, 260); hidden(k.r); show(k.r, T("s17")); k.drive(pos); hide(k.r, T("s18") - 0.2, 0.25);
  const rl = numLine(p2, 520, 300, 1260, 0, 4095, (t) => Math.round(4095 * pos(t)), "analogRead(34)"); hidden(rl); show(rl, T("s17")); hide(rl, T("s18") - 0.2, 0.25);
  note(p2, "0 V &rarr; 0 &nbsp;&middot;&nbsp; 3.3 V &rarr; 4095", T("s17") + 1.5, 520, T("s18") - 0.2);
  exCard("&#128506;&#65039;", "The city map", "Same spot, different range: how far along the first range, the same spot in the second.", T("s18") + 0.3, T("s19") - 0.25);
  const top = numLine(p2, 330, 260, 1260, 0, 4095, () => 2048, "value"); hidden(top); show(top, T("s19"));
  const bot = numLine(p2, 330, 470, 1260, 0, 255, () => 127, "map(value, 0, 4095, 0, 255)", "#36e07a"); hidden(bot); show(bot, T("s19"));
  const lim = tile(p2, 330, 700, 1260, 170, '<div style="font:700 34px/1.5 var(--ui);color:#ffe3b8"><b style="color:var(--amber)">The difference:</b> whole numbers only, always rounded down (2048 &rarr; 127, not 127.5).</div>', "var(--amber)");
  hidden(lim); show(lim, T("s19") + 0.3);
}
const tr2 = chapter("s20", "s22"); title(tr2, "Trace: the knob dimmer", "s20");
{
  const pos = (t) => (t < T("s21") ? 0.5 : clamp(0.5 + (t - W("s21", "up")) * 0.5, 0.5, 1));
  const val = (t) => Math.round(4095 * pos(t)), br = (t) => mapI(val(t), 0, 4095, 0, 255);
  const c = bigCode(tr2, 90, 200, 1180, "int value = analogRead(POT_PIN);\nint brightness = map(value, 0, 4095, 0, 255);\nanalogWrite(LED_PIN, brightness);", { size: 34 });
  show(c.c, T("s20")); c.hl([[W("s20", "reading"), 0], [W("s20", "map"), 1], [W("s20", "brightness"), 2], [T("s21"), 1]]);
  const k = knobIcon(tr2, 160, 470, 240); hidden(k.r); show(k.r, T("s20")); k.drive(pos);
  const mem = tile(tr2, 1340, 200, 480, 120, '<div class="kicker">MEMORY</div>', "var(--teal)"); hidden(mem); show(mem, T("s20") + 0.3);
  const vv = live(tr2, 1340, 340, 480, "value", val, "#c9d1dc"); show(vv, W("s20", "reading"));
  const vb = live(tr2, 1340, 520, 480, "brightness", br, "#ffb547"); show(vb, W("s20", "map"));
  const led = glowLed(tr2, 1480, 720, 100, (t) => br(t) / 255); hidden(led); show(led, W("s20", "brightness"));
  ask(tr2, "PAUSE AND PREDICT", "The knob goes all the way up. What does the brightness become?", T("s21"), W("s21", "top"), "255, the top: every number follows the knob.", { x: 480, y: 780, w: 820, t1: S1("s21") });
}
const q3 = chapter("s22", "s24"); title(q3, "Question 3", "s22");
{
  const c = bigCode(q3, 210, 190, 1500, "waitTime = map(analogRead(POT_PIN), 0, 4095, 1000, 4000);", { size: 38 }); show(c.c, T("s22"));
  const k = knobIcon(q3, 230, 380, 200); hidden(k.r); show(k.r, T("s22") + 0.5); k.drive(() => 0.5);
  const nl = numLine(q3, 520, 430, 1180, 1000, 4000, () => 2500, "waitTime (ms)", "#ffd23a"); hidden(nl); show(nl, T("s23"));
  quiz(3, 8, "The knob is at the middle. About how long is the yellow?", "s22", "s23", "About 2.5 s: halfway between 1 and 4 seconds.");
}
const q4 = chapter("s24", "s26"); title(q4, "Question 4", "s24");
{
  const pins = [["23", 1], ["22", 1], ["21", 1], ["35", 0], ["34", 0], ["39", 0]];
  const g = box(q4, 260, 210, 1400, 300, "", `<div style="display:flex;gap:22px">${pins.map(([p, out]) => `<div class="pp" data-in="${out ? 0 : 1}" style="flex:1;height:260px;border-radius:18px;background:#121b2e;border:3px solid #22304d;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px"><div style="font:800 54px var(--mono)">${p}</div><div style="font:700 26px var(--ui);color:var(--muted)">${out ? "in + out" : "in only"}</div></div>`).join("")}</div>`);
  hidden(g); show(g, T("s24"));
  dyn((t) => { const on = t >= T("s25"); g.querySelectorAll(".pp").forEach((e) => { const inOnly = e.dataset.in === "1"; e.style.borderColor = on && inOnly ? "#ff5d6c" : "#22304d"; e.style.opacity = on && !inOnly ? 0.5 : 1; }); });
  const door = pill(q4, 300, 540, "&#128682; 34&ndash;39: one-way doors, they can only listen", "font-size:34px;color:#ff8a8f"); show(door, T("s25"));
  quiz(4, 7, "An LED moved to pin 34 stays dark. The wiring is fine. Why?", "s24", "s25", "34-39 are input-only: they can't drive an LED.");
}

/* ======================================================================
 * PART 3: remembering steps: the washing machine, the reflex trace, Q5 (the mistake), Q6, Q7
 * ==================================================================== */
const p3 = chapter("s26", "s29"); const p3h = title(p3, "", "s26");
textAt(p3h, [[0, "Part 3: remembering steps"], [T("s27") - 0.2, "state + goTo(): a number and the time"], [T("s28") - 0.2, "The loop never waits"]]);
{
  exCard("&#129530;", "The washing machine", "Wash, rinse, spin: it always knows its step, and moves on when the step's time is up.", T("s26") + 0.5, T("s27") - 0.25);
  const run = game({ start: T("s27") + 0.3, red: 1.0, yellow: 1.4, react: 0.5, show: 1.6 });
  const row = stepRow(p3, 110, 230, 1700, run); hidden(row.g); show(row.g, T("s27"));
  const c = bigCode(p3, 110, 560, 980, "void goTo(int newState, unsigned long now) {\n  state = newState;\n  stateStart = now;\n}", { size: 32 }); show(c.c, W("s27", "jobs"));
  const lim = tile(p3, 1150, 560, 660, 300, '<div style="font:700 32px/1.5 var(--ui);color:#ffe3b8"><b style="color:var(--amber)">The difference:</b> the machine really does its step. Our loop only looks at the number, thousands of times a second.</div>', "var(--amber)");
  hidden(lim); show(lim, T("s28"));
}
const tr3 = chapter("s29", "s31"); title(tr3, "Trace: the reflex game", "s29");
{
  const g0 = W("s29", "green") + 0.2, react = Math.max(0.6, W("s30", "press") - g0);
  const sim3 = game({ start: T("s29") + 0.2, red: Math.max(0.4, (g0 - T("s29") - 0.2) * 0.4), yellow: Math.max(0.4, (g0 - T("s29") - 0.2) * 0.6), react, show: 30 });
  const ri = reflexIcon(tr3, 140, 220, 0.9); hidden(ri.r); show(ri.r, T("s29")); ri.drive(sim3);
  const mem = tile(tr3, 620, 200, 1200, 110, '<div class="kicker">MEMORY</div>', "var(--teal)"); hidden(mem); show(mem, T("s29") + 0.3);
  const vs = live(tr3, 620, 330, 360, "state", (t) => sim3(t).state, "#b48cff"); show(vs, T("s29") + 0.5);
  const vi = live(tr3, 1010, 330, 400, "time in step (ms)", (t) => { const s = sim3(t); return s.state === 3 ? ms(s.inState) : s.state === 4 ? ms(react) : "-"; }, "#ffb547"); show(vi, W("s29", "step"));
  const vb = live(tr3, 1440, 330, 380, "drawer: best", (t) => (t < W("s30", "drawer") ? "9999" : String(ms(react))), "#36e07a"); show(vb, T("s30"));
  const tk = pill(tr3, 620, 540, "&#127915; stamped when green comes on", "font-size:30px;color:var(--teal)"); show(tk, W("s29", "ticket"));
  const dr = pill(tr3, 620, 610, "&#128452;&#65039; a new record goes into the drawer (flash: kept without power)", "font-size:30px;color:var(--teal)"); show(dr, W("s30", "drawer"));
  ask(tr3, "PAUSE AND PREDICT", "Which number becomes the reaction?", T("s30"), W("s30", "press"), "The time in step 3 at the press.", { x: 620, y: 760, w: 1200, t1: S1("s30") });
}
const mk = chapter("s31", "s33"); title(mk, "Question 5: a mistake", "s31");
{
  const bad = bigCode(mk, 260, 200, 1400, "state = 1;          // no new start time!", { size: 46 }); css(bad.c, { borderColor: "#ff5d6c" }); show(bad.c, T("s31"));
  const good = bigCode(mk, 260, 400, 1400, "goTo(1, now);       // new number + the time", { size: 46 }); css(good.c, { borderColor: "#4ade80" }); show(good.c, T("s32"));
  quiz(5, 9, "Moved on with just state = 1, no time. What happens to the next step?", "s31", "s32", "It ends almost at once: the old start time says its time is long gone.");
}
const q6 = chapter("s33", "s35"); title(q6, "Question 6", "s33");
{
  const c = bigCode(q6, 260, 200, 1400, "if (b == LOW && state == 0) {\n  request = true;\n}", { size: 44 }); show(c.c, T("s33")); c.hl([[T("s34"), 0]]);
  const ci = crossingLite(q6, 760, 420); show(ci, T("s33") + 0.4);
  quiz(6, 9, "The walker is already crossing. You press. Does it count?", "s33", "s34", "No: presses only count in step 0.");
}
function crossingLite(parent, x, y) {
  return hidden(box(parent, x, y, 400, 300, "", '<div style="display:flex;gap:40px;align-items:center;justify-content:center;height:300px"><div style="font-size:120px">&#128678;</div><div style="font-size:120px">&#128694;</div></div>'));
}
const q7 = chapter("s35", "s36b"); title(q7, "Question 7", "s35");
{
  const plug = box(q7, 300, 230, 400, 300, "", '<div style="font-size:220px;line-height:300px;text-align:center">&#128268;</div>'); hidden(plug); show(plug, T("s35"));
  const sm = serialAt(q7, 820, 230, 820, 300, [[T("s36") + 0.2, "record: 213"]], 54); hidden(sm); show(sm, T("s35") + 0.4);
  const em = pill(q7, 820, 560, "only an empty page gives back 9999", "font-size:32px;color:var(--amber)"); show(em, W("s36", "empty"));
  quiz(7, 10, "The record is in the drawer. You unplug. After the restart, getULong() gives back...?", "s35", "s36", "The old record.");
}

/* ======================================================================
 * EXPLAIN, SCORE, OUTRO
 * ==================================================================== */
const ex = chapter("s36b", "s37"); title(ex, "In your own words", "s36b");
{
  const a = tile(ex, 210, 470, 1500, 300, '<div style="font:700 40px/1.5 var(--ui)">map() finds where a number sits in one range, and gives back the same spot in another range.</div>', "var(--teal)");
  hidden(a); show(a, T("s36c"));
  ask(ex, "PAUSE AND EXPLAIN", "What does map() do? One sentence.", T("s36b"), T("s36c"), "One sentence is enough.", { x: 210, y: 200, w: 1500, t1: S1("s36c") });
}
const scr = chapter("s37", "s39"); title(scr, "Your score", "s37"); likeTop(T("s37") + 0.6);
{
  const rows = [["1", "PWM duty: 64 &asymp; a quarter", "5"], ["2", "setColor: magenta", "6"], ["3", "map(): the yellow time", "8"], ["4", "pins 34&ndash;39: input only", "7"], ["5", "goTo(): number + time", "9"], ["6", "presses only in step 0", "9"], ["7", "the drawer keeps the record", "10"]];
  const tb = tile(scr, 260, 190, 1400, 640, `<div style="display:grid;gap:10px;font:700 34px/1.5 var(--ui)">${rows.map(([n, a, ep]) => `<div style="display:flex;gap:26px;align-items:center"><b style="font-family:var(--mono);color:var(--amber);width:40px">${n}</b><span style="flex:1">${a}</span><span class="epc" style="font:700 28px var(--ui);color:var(--muted)">episode ${ep}</span></div>`).join("")}</div>`);
  hidden(tb); show(tb, T("s37"));
  const ok = pill(scr, 300, 860, "6&ndash;7 points: ready for the next part", "font-size:32px;color:#36e07a"); show(ok, W("s37", "ready"));
  const rw = pill(scr, 1020, 860, "fewer? rewatch that episode, then come back", "font-size:32px;color:var(--amber)"); show(rw, T("s38"));
}
const out = chapter("s39", null); title(out, "Next", "s39");
{
  const next = tile(out, 210, 200, 1500, 420, '<div class="kicker">NEXT: EPISODE 11</div><div style="font:800 62px var(--display);margin-top:26px">A light sensor</div><div style="font:600 36px var(--ui);margin-top:20px;color:var(--muted)">A lamp that turns itself on when the room gets dark.</div><div style="font-size:90px;margin-top:20px">&#127769;&#128161;</div>');
  hidden(next); show(next, T("s39"));
  note(out, "Your score out of 7? Tell me in the comments.", W("s39", "comments") - 0.6, 690);
  note(out, "github.com/emjnbulut/esp32-from-zero &rarr; lessons", W("s39", "comments") - 0.6, 820);
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 }); TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}
window.__seek(0);
window.__ready = true;
