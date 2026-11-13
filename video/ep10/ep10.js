/* Episode 10 Mini Project 1, a Reflex Game with a Record that Survives Power Off: segment-anchored scenes, creator
 * footage C0-C2, code tours. Same layout rules as episode 9: 16:9 clips in a 1200x675 window on the left, the drawing on
 * the right; the window size and EP10_CLIP_SECONDS get their final values once footage/ep10 is prepared.
 * A small simulator (game) drives every drawn reflex game, so the drawings follow the same rules as reflex_game.ino. */
const stage = $("#stage");
const EP10_CLIP_SECONDS = { C0: 12, C1: 10, C2: 6 }; // placeholders until footage/ep10 exists
function hero(id, t0, requestedEnd, description, opts = {}) {
  const lead = opts.full ? Math.min(0.3, t0) : 0;
  const tail = opts.full ? 0.35 : 0;
  const t1 = Math.min(requestedEnd, t0 + EP10_CLIP_SECONDS[id] - lead - tail - 1 / 30);
  if (!(t1 > t0)) throw new Error("No usable episode 10 footage: " + id);
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
const repo = "Full code: <b>github.com/emjnbulut/esp32-from-zero</b> &rarr; lessons/10-reflex-game";
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

/* ======================================================================
 * COLD OPEN: the real game, then the promise (a record that survives unplugging)
 * ==================================================================== */
const cold = SC(); SET(cold, 0, { opacity: 1 }); SET(cold, CUT, { opacity: 0 });
{
  const h = box(cold, 1310, 150, 560, 200, "", '<div style="font:800 58px/1.15 var(--display)">A reflex<br><span style="color:var(--amber)">game</span></div>');
  hidden(h); show(h, 0.6);
  const seq = box(cold, 1310, 400, 560, 330, "", [["#ff4d5a", "red"], ["#ffd23a", "yellow"], ["#36e07a", "GREEN: press!"]].map(([c, s]) => `<div style="font:700 40px/1.9 var(--ui)">${dot(c)} &nbsp;${s}</div>`).join(""));
  hidden(seq); show(seq, 1.2);
  const rec = tile(cold, 1310, 400, 560, 330, '<div class="kicker">MINI PROJECT 1 &middot; PART 2</div><div style="font:800 44px/1.3 var(--display);margin-top:20px">Your best time stays saved</div><div style="font:800 54px var(--mono);margin-top:26px;color:var(--amber)">&#127942; record</div><div style="font:700 30px var(--ui);margin-top:10px;color:var(--muted)">even after unplugging &#128268;</div>', "var(--amber)");
  hidden(rec); hide(seq, T("s02") - 0.2, 0.25); show(rec, T("s02"));
}
hero("C0", 0, CUT, "reflex_game: start, red, yellow, green, a quick press, the color LED turns green.", WIN);

/* ======================================================================
 * RETRIEVAL (episodes 9 and 6) + the way in for new viewers
 * ==================================================================== */
const ret = chapter("s03", "s08"); title(ret, "Two questions from earlier episodes", "s03");
{
  const nw = pill(ret, 1340, 150, "New here? Start at Episode 1 &rarr;", "font-size:28px;color:var(--teal)"); show(nw, T("s03") + 0.2); hide(nw, T("s04") + 1.5, 0.3);
  const c = bigCode(ret, 360, 220, 1200, "void goTo(int newState, unsigned long now) {\n  state = newState;\n  stateStart = now;\n}", { size: 42 });
  show(c.c, T("s04")); c.hl([[T("s05"), 1], [W("s05", "time"), 2]]); hide(c.c, T("s06") - 0.2, 0.25);
  ask(ret, "QUICK QUESTION", "goTo() always did two jobs. Which two?", T("s04"), T("s05"), "A new number in state + the time it started.", { y: 700, w: 1500, t1: T("s06") - 0.2 });
  const sw = box(ret, 360, 240, 360, 360, "", `<div style="width:300px;height:300px;margin:30px;border-radius:50%;background:#ff7a1a;box-shadow:0 0 90px #ff7a1a"></div>`);
  hidden(sw); show(sw, T("s07")); hide(sw, T("s08") - 0.3, 0.25);
  const c2 = bigCode(ret, 800, 300, 860, "setColor(255, 40, 0);", { size: 50 }); show(c2.c, T("s06") + 0.4); hide(c2.c, T("s08") - 0.3, 0.25);
  const lab = box(ret, 800, 470, 860, 120, "", '<div style="font:700 34px/1.5 var(--ui)"><b style="color:#ff5d6c">red full</b> &middot; <b style="color:#36e07a">a little green</b> &middot; <span style="color:var(--muted)">blue off</span></div>');
  hidden(lab); show(lab, T("s07")); hide(lab, T("s08") - 0.3, 0.25);
  ask(ret, "QUICK QUESTION", "How do you make orange with the color LED?", T("s06"), T("s07"), "Full red plus a touch of green: light adds up.", { y: 700, w: 1500, t1: S1("s07") });
}

/* ======================================================================
 * THE RULES + the parts (no new wire)
 * ==================================================================== */
const pl = chapter("s08", "s11"); title(pl, "The rules", "s08"); likeTop(T("s08") + 1.0);
{
  const demo = game({ start: T("s08") + 1.2, red: 1.0, yellow: 1.4, react: 0.21, show: 30 });
  const ri = reflexIcon(pl, 160, 220, 1.15); hidden(ri.r); show(ri.r, T("s08")); ri.drive(demo); hide(ri.r, T("s10") - 0.2, 0.25);
  const b = btnIcon(pl, 700, 640, 140); hidden(b.r); show(b.r, T("s08")); b.press([[T("s08") + 1.2, T("s08") + 1.5], [T("s08") + 3.81, T("s08") + 4.1]]); hide(b.r, T("s10") - 0.2, 0.25);
  const r1 = tile(pl, 900, 210, 900, 300, '<div style="font:800 40px var(--display)">Press to start</div><div style="font:700 36px/1.7 var(--ui);margin-top:14px">' + dot("#ff4d5a") + ' &rarr; ' + dot("#ffd23a") + ' &rarr; ' + dot("#36e07a") + ' &nbsp;<b>then press, fast!</b></div>', "var(--amber)");
  hidden(r1); show(r1, T("s08") + 0.4); hide(r1, T("s10") - 0.2, 0.25);
  const r2 = tile(pl, 900, 540, 900, 340, LEGEND, "var(--teal)"); hidden(r2); show(r2, T("s09")); hide(r2, W("s09", "knob") - 0.2, 0.25);
  const r3 = tile(pl, 900, 540, 900, 340, '<div style="padding-left:250px;padding-top:40px;font:700 36px/1.6 var(--ui)">Knob &rarr; how long the yellow waits: <b style="color:var(--amber)">1 &ndash; 4 s</b><br><span style="color:var(--muted)">so you can\'t just count</span></div>', "var(--amber)");
  hidden(r3); show(r3, W("s09", "knob")); hide(r3, T("s10") - 0.2, 0.25);
  const k = knobIcon(r3, 30, 70, 190); k.drive((t) => sweep(t, T("s09"), 4));
  const pins = tile(pl, 260, 200, 1400, 560, '<div style="font:800 46px var(--display)">No new wire: the crossing\'s circuit</div>' +
    '<div class="pins"><div><b style="color:#ff5d6c">red</b> D23</div><div><b style="color:#ffd23a">yellow</b> D18</div><div><b style="color:#36e07a">green</b> TX2 (pin 17)</div>' +
    '<div><b style="color:#b48cff">color LED</b> D25 D26 D27</div><div><b style="color:var(--amber)">button</b> D22</div><div><b style="color:var(--amber)">knob</b> D34</div></div>', "var(--teal)");
  hidden(pins); show(pins, T("s10"));
}

/* ======================================================================
 * THE IDEA: the washing machine again, five steps; reaction = time in the green step
 * ==================================================================== */
const idA = chapter("s11", "s15"); const ih = title(idA, "", "s11");
textAt(ih, [[0, "The washing machine again: five steps"], [T("s12") - 0.2, "How can the board measure your reaction?"], [T("s13") - 0.2, "The parking ticket"], [T("s14") - 0.2, "Reaction = time in the green step"]]);
{
  const run = game({ start: T("s11") + 0.6, red: 1.0, yellow: 1.5, react: 0.6, show: 2 });
  const row = stepRow(idA, 110, 210, 1700, (t) => (t < T("s12") ? run(t) : { state: 3 })); hidden(row.g); show(row.g, T("s11"));
  const g0 = T("s13") + 0.8, pr = g0 + 0.23;
  const tk = (t) => (t < g0 ? { state: 2, color: "off" } : t < pr ? { state: 3, color: "off" } : { state: 4, color: "green" });
  const ri = reflexIcon(idA, 160, 520, 0.8); hidden(ri.r); show(ri.r, T("s11")); ri.drive((t) => (t < T("s12") ? run(t) : t < T("s13") ? { state: 3, color: "off" } : tk(t)));
  askTop(stage, "PAUSE AND PREDICT", "How can the board measure your reaction time?", T("s12"), T("s13"), "The parking ticket: now minus the moment green came on.", { x: 210, y: 820, w: 1500, t1: T("s14") - 0.3 });
  const st = live(idA, 640, 540, 480, "stateStart (green on)", (t) => (t >= g0 ? ms(g0).toLocaleString("en-US") : "?"), "#36e07a"); show(st, T("s13"));
  const nw = live(idA, 1160, 540, 480, "now (press)", (t) => (t >= pr ? ms(pr).toLocaleString("en-US") : ms(Math.max(t, 0)).toLocaleString("en-US")), "#c9d1dc"); show(nw, T("s13") + 0.4);
  const ticket = pill(idA, 640, 740, "&#127915; stamped when green comes on &middot; now &minus; stamp = your reaction", "font-size:30px;color:var(--teal)"); show(ticket, T("s13") + 0.6);
  const re = bigCode(idA, 640, 740, 1100, "reaction = inState;   // time in step 3", { size: 42 }); show(re.c, T("s14")); hide(ticket, T("s14") - 0.1, 0.2);
}

/* ======================================================================
 * CODE TOUR: reflex_game (top, helpers, the button)
 * ==================================================================== */
tour("reflex_game", T("s15") - 0.4, T("s20") - 0.3, [
  [T("s15"), "const int RED_PIN", "const int POT_PIN"], [W("s15", "state"), "int state = 0;", "unsigned long stateStart"], [W("s15", "best"), "unsigned long best = 9999;"],
  [T("s16"), "void setColor(", "}"], [W("s16", "lights"), "void lights(", "}"], [W("s16", "moving"), "void goTo(", "}"],
  [T("s17"), "// PART 1", "unsigned long inState"], [W("s17", "pressed"), "bool pressed = false;"], [W("s17", "round"), "pressed = true;"],
  [T("s18"), "pressed = true;"], [T("s19"), "if (b != lastButton && now - lastChange >= 50) {"]]);
askTop(stage, "PAUSE AND PREDICT", "You hold the button for a whole second. In how many rounds is pressed true?", T("s18"), T("s19"), "Just one: only a new press counts.", { x: 210, y: 820, w: 1500, t1: T("s20") - 0.3 });

/* ======================================================================
 * THE STEPS (step 2: pause and try it yourself), step 3 = the heart, step 4
 * ==================================================================== */
const stp = chapter("s20", "s27"); const sh = title(stp, "", "s20");
textAt(sh, [[0, "Step 0: wait for a start"], [T("s21") - 0.2, "Step 1: red, then the yellow time"], [T("s22") - 0.2, "Your turn first: write step 2"], [T("s23") - 0.2, "Step 2: yellow, then GO"], [T("s24") - 0.2, "Step 3: the heart of the game"], [T("s26") - 0.2, "Step 4: show the result"]]);
{
  const fake = (t) => {
    if (t < T("s21")) return { state: 0, color: "blue" };
    if (t < T("s23")) return { state: 1, color: "off" };
    if (t < T("s24")) return { state: 2, color: "off" };
    if (t < W("s25", "pick")) return { state: 3, color: "off" };
    if (t < T("s26")) return { state: 4, color: ["green", "yellow", "red"][Math.floor((t - W("s25", "pick")) / 1.4) % 3] };
    return { state: t < T("s26") + 2.2 ? 4 : 0, color: t < T("s26") + 2.2 ? "green" : "blue" };
  };
  const ri = reflexIcon(stp, 1380, 190, 0.85); hidden(ri.r); show(ri.r, T("s20")); ri.drive((t) => (t >= T("s22") && t < T("s23") ? { state: 2, color: "off" } : fake(t)));
  const live0 = live(stp, 1380, 640, 440, "state", (t) => fake(t).state, "#b48cff"); show(live0, T("s20"));
  const s0 = bigCode(stp, 90, 200, 1200, "if (state == 0) {\n  if (pressed) {\n    setColor(0, 0, 0);\n    lights(HIGH, LOW, LOW);\n    goTo(1, now);\n  }", { size: 36 });
  show(s0.c, T("s20")); s0.hl([[W("s20", "press"), 1], [W("s20", "red"), 3], [W("s20", "step"), 4]]); hide(s0.c, T("s21") - 0.2, 0.25);
  const s1 = bigCode(stp, 90, 200, 1200, "} else if (state == 1) {\n  if (inState >= 1000) {\n    lights(LOW, HIGH, LOW);\n    waitTime = map(analogRead(POT_PIN), 0, 4095, 1000, 4000);\n    goTo(2, now);\n  }", { size: 32 });
  show(s1.c, T("s21")); s1.hl([[W("s21", "second"), 1], [W("s21", "yellow"), 2], [W("s21", "knob"), 3]]); hide(s1.c, T("s22") - 0.2, 0.25);
  const cm = pill(stp, 120, 560, "&#128506; the city map: knob &rarr; 1000 &hellip; 4000 ms", "font-size:30px;color:var(--teal)"); show(cm, W("s21", "knob")); hide(cm, T("s22") - 0.2, 0.25);
  const tryIt = tile(stp, 90, 210, 1200, 520, '<div class="kicker">PAUSE &middot; TRY IT YOURSELF</div><div style="font:800 46px/1.35 var(--display);margin-top:24px">Write step 2</div><div style="font:600 36px/1.6 var(--ui);margin-top:20px;color:var(--muted)">When the yellow time is up:<br><b style="color:#36e07a">green</b> on, then go to step 3.</div><div class="qbar" style="margin-top:36px"><i class="tb"></i></div>', "var(--amber)");
  hidden(tryIt); show(tryIt, T("s22")); hide(tryIt, T("s23") - 0.2, 0.25);
  TO($(".tb", tryIt), T("s22") + 0.6, Math.max(0.5, T("s23") - T("s22") - 0.8), { width: "100%", ease: "none" });
  const s2 = bigCode(stp, 90, 200, 1200, "} else if (state == 2) {\n  if (inState >= waitTime) {\n    lights(LOW, LOW, HIGH);   // GO!\n    goTo(3, now);\n  }", { size: 36 });
  show(s2.c, T("s23")); s2.hl([[W("s23", "time"), 1], [W("s23", "lights"), 2], [W("s23", "and"), 3]]); hide(s2.c, T("s24") - 0.2, 0.25);
  const s3 = bigCode(stp, 90, 200, 1200, "} else if (state == 3) {\n  if (pressed) {\n    unsigned long reaction = inState;\n    Serial.println(reaction);\n    if (reaction < 250) {\n      setColor(0, 255, 0);\n    } else if (reaction < 500) {\n      setColor(255, 160, 0);\n    } else {\n      setColor(255, 0, 0);\n    }", { size: 28 });
  show(s3.c, T("s24")); s3.hl([[W("s24", "pressed"), 1], [W("s24", "reaction"), 2], [W("s24", "prints"), 3], [W("s25", "green"), 4], [W("s25", "yellow"), 6], [W("s25", "red"), 8]]); hide(s3.c, T("s26") - 0.2, 0.25);
  const s4 = bigCode(stp, 90, 200, 1200, "} else {                 // step 4\n  if (inState >= 3000) {\n    setColor(0, 0, 40);    // dim blue: press to start\n    goTo(0, now);\n  }\n}", { size: 36 });
  show(s4.c, T("s26")); s4.hl([[W("s26", "three"), 1], [W("s26", "back"), 3]]);
}

/* s27 - s28: the real game: a fast press, then a slow one */
const rn = chapter("s27", "s29");
{
  const r1 = tile(rn, 1310, 200, 560, 560, '<div class="kicker">ON THE REAL BOARD</div><div style="font:700 36px/1.6 var(--ui);margin-top:24px">Watch the lights,<br>and the color at the end.</div>', "var(--teal)");
  hidden(r1); show(r1, T("s27")); hide(r1, T("s28") - 0.2, 0.25);
  const sm = serialAt(rn, 1310, 200, 560, 420, [[T("s27") + 2.5, "reaction: 213 ms"], [T("s28") + 2.5, "reaction: 1046 ms"]], 34);
  hidden(sm); show(sm, T("s28"));
  const r2 = box(rn, 1310, 650, 560, 120, "", `<div style="font:700 36px var(--ui)">${dot(RGB.red)} &nbsp;slow: red</div>`); hidden(r2); show(r2, T("s28") + 1.0);
}
hero("C0", T("s27"), T("s28") - 0.35, "reflex_game on the real board: a fast press, the color LED turns green.", WIN);
hero("C1", T("s28"), T("s29") - 0.35, "A slow press, about a second after green: the color LED turns red.", WIN);

/* s29 - s30: modify: 250 -> 200 */
const md = chapter("s29", "s31"); title(md, "Change one number", "s29"); likeTop(T("s30") + 1.2);
{
  const c = box(md, 210, 200, 1500, 150, "card", '<div style="font:800 54px/150px var(--mono);text-align:center;white-space:nowrap">if (reaction &lt; <span class="arg sw">250</span>) {</div>');
  hidden(c); show(c, T("s29")); textAt($(".sw", c), [[0, "250"], [T("s30"), "200"]]); styleAt($(".sw", c), "background", [[0, "transparent"], [T("s30"), "#5aa9ff55"]]);
  const X = 210, Wd = 1500, Y = 470, sx = (v) => (v / 700) * Wd;
  const bar = (y, g, lab, t0) => {
    const gr = box(md, X, y, Wd, 130, ""); hidden(gr); show(gr, t0);
    const sv = svgEl(gr, "svg", { width: Wd, height: 130, viewBox: `0 0 ${Wd} 130` }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible" });
    svgEl(sv, "rect", { x: 0, y: 10, width: sx(g) - 3, height: 70, rx: 10, fill: RGB.green });
    svgEl(sv, "rect", { x: sx(g) + 3, y: 10, width: sx(500 - g) - 6, height: 70, rx: 10, fill: RGB.yellow });
    svgEl(sv, "rect", { x: sx(500) + 3, y: 10, width: sx(200) - 3, height: 70, rx: 10, fill: RGB.red });
    txt(sv, sx(g), 118, g + " ms", { "font-size": 30, "text-anchor": "middle", fill: "#e6edf7" });
    txt(sv, sx(500), 118, "500 ms", { "font-size": 30, "text-anchor": "middle" });
    txt(sv, Wd, -8, lab, { "font-size": 30, "text-anchor": "end" });
    return gr;
  };
  bar(Y, 250, "now", T("s29") + 0.3);
  bar(Y + 190, 200, "green is harder to earn", T("s30"));
  askTop(stage, "PAUSE AND PREDICT", "250 becomes 200. What happens to your green results?", T("s29"), T("s30"), "Green gets harder: only really fast presses.", { x: 210, y: 820, w: 1500, t1: T("s30") - 0.05 });
}

/* ======================================================================
 * THE RECORD: a power cut wipes variables; the drawer keeps it (Preferences)
 * ==================================================================== */
const ls = chapter("s31", "s33"); title(ls, "And the record?", "s31");
{
  const cut = W("s32", "power");
  const bst = live(ls, 260, 260, 620, "best (ms)", (t) => (t < cut ? "213" : "9999"), "#ffb547"); show(bst, T("s31"));
  const plug = box(ls, 1040, 230, 600, 260, "", '<div class="pl" style="font-size:200px;line-height:260px;text-align:center">&#128268;</div>'); hidden(plug); show(plug, T("s31") + 0.5);
  TO($(".pl", plug), cut - 0.3, 0.4, { x: 160, opacity: 0.35 });
  TO($(".pl", plug), W("s32", "restart"), 0.4, { x: 0, opacity: 1 });
  const wipe = pill(ls, 260, 470, "&#9888; variables are wiped when the power goes", "font-size:32px;color:#ff8a8f"); show(wipe, cut);
  askTop(stage, "PAUSE AND PREDICT", "Great time, then unplug and plug back in. Is the record still there?", T("s31"), T("s32"), "Not with an ordinary variable: best starts over.", { x: 210, y: 760, w: 1500, t1: T("s33") - 0.3 });
}
const dr = chapter("s33", "s36"); const dh = title(dr, "", "s33");
textAt(dh, [[0, "The desk and the drawer"], [T("s34") - 0.2, "Flash memory: Preferences"], [T("s35") - 0.2, "Write only what's worth keeping"]]);
{
  exCard("&#128452;&#65039;", "The desk and the drawer", "Variables are labeled boxes on the desk: a power cut clears the desk. A notebook in the drawer stays.", T("s33") + 0.2, T("s34") - 0.25);
  const ram = tile(dr, 140, 220, 760, 520, '<div class="kicker">RAM &middot; THE DESK</div><div style="font:700 40px/1.7 var(--mono);margin-top:24px">state<br>stateStart<br>best</div><div style="font:600 30px var(--ui);margin-top:20px;color:#ff8a8f">wiped without power</div>', "#ff5d6c");
  hidden(ram); show(ram, T("s34"));
  const fl = tile(dr, 1020, 220, 760, 520, '<div class="kicker">FLASH &middot; THE DRAWER</div><div style="margin-top:24px;display:flex;flex-direction:column;gap:14px"><div style="height:200px;border-radius:14px;background:#1d2a47;font:700 32px/200px var(--ui);text-align:center;color:var(--muted)">your program</div><div class="pf" style="height:110px;border-radius:14px;background:#14324a;border:3px solid var(--teal);font:700 32px/104px var(--mono);text-align:center;color:var(--teal)">Preferences: best = 213</div></div><div style="font:600 30px var(--ui);margin-top:20px;color:#7be3d4">kept without power</div>', "var(--teal)");
  hidden(fl); show(fl, W("s34", "flash"));
  const lim = tile(dr, 140, 770, 1640, 170, '<div style="font:700 34px/1.5 var(--ui);color:#ffe3b8"><b style="color:var(--amber)">The difference:</b> the drawer is small, and every write wears it a little. Write only when something worth keeping happens.</div>', "var(--amber)");
  hidden(lim); show(lim, T("s35"));
}
const pf = chapter("s36", "s41"); const ph = title(pf, "", "s36");
textAt(ph, [[0, "Three lines: open the drawer"], [T("s37") - 0.2, "Read a page (or the default)"], [T("s40") - 0.2, "Write a new record"]]);
{
  const c = bigCode(pf, 110, 200, 1700, '#include <Preferences.h>\nPreferences prefs;\n\nprefs.begin("reflex", false);           // in setup()\nbest = prefs.getULong("best", 9999);', { size: 40 });
  show(c.c, T("s36")); c.hl([[T("s36"), 3], [T("s37"), 4], [W("s37", "second"), 4]]); hide(c.c, T("s40") - 0.2, 0.25);
  const dflt = pill(pf, 1060, 560, "empty page &rarr; <b style=\"font-family:var(--mono)\">9999</b>", "font-size:34px;color:var(--amber)"); show(dflt, W("s37", "empty")); hide(dflt, T("s40") - 0.2, 0.25);
  const sc = box(pf, 160, 580, 840, 130, "", '<div style="font:700 34px/1.5 var(--ui)">&#128452;&#65039; drawer <b style="font-family:var(--mono);color:var(--teal)">"reflex"</b> &rarr; page <b style="font-family:var(--mono);color:var(--teal)">"best"</b></div>');
  hidden(sc); show(sc, T("s37")); hide(sc, T("s38") - 0.2, 0.2);
  ask(pf, "QUICK QUESTION", "Why such a big number as the starting record?", T("s38"), T("s39"), "Any real reaction is smaller: the first round is always a record.", { x: 160, y: 600, w: 1600, t1: T("s40") - 0.2 });
  const w = bigCode(pf, 110, 200, 1700, 'if (reaction < best) {          // a new record: save it\n  best = reaction;\n  prefs.putULong("best", best);\n}', { size: 42 });
  show(w.c, T("s40")); w.hl([[W("s40", "beats"), 0], [W("s40", "record"), 1], [W("s40", "writes"), 2]]);
  const drw = box(pf, 760, 560, 400, 300, "", '<div style="font-size:220px;line-height:300px;text-align:center">&#128452;&#65039;</div>'); hidden(drw); show(drw, W("s40", "drawer") - 0.3);
}

/* s41 - s42: the unplug test */
const up = chapter("s41", "s43");
{
  const r = tile(up, 1310, 200, 560, 330, '<div class="kicker">THE TEST</div><div style="font:700 36px/1.6 var(--ui);margin-top:24px">Unplug &#128268;<br>wait a moment<br>plug back in</div>', "var(--teal)");
  hidden(r); show(r, T("s41"));
  const sm = serialAt(up, 1310, 560, 560, 260, [[T("s42") + 0.3, "record: 213"]], 40); hidden(sm); show(sm, T("s42"));
  const big = serialAt(up, 110, 200, 1100, 560, [[T("s42") + 0.3, "record: 213"]], 60); hidden(big); show(big, T("s42"));
  const ok = pill(up, 140, 800, "&#128452;&#65039; the drawer kept it", "font-size:36px;color:var(--teal)"); show(ok, W("s42", "kept"));
}
hero("C2", T("s41"), T("s42") - 0.35, "The USB cable unplugged and plugged back in.", WIN);

/* ======================================================================
 * THE COMMON MISTAKE: saving every result without the if
 * ==================================================================== */
const mk = chapter("s43", "s46"); const mh = title(mk, "", "s43");
textAt(mh, [[0, "A mistake you might make"], [T("s45") - 0.2, "The if is what makes it a record"]]);
{
  const bad = bigCode(mk, 90, 200, 1250, 'best = reaction;\nprefs.putULong("best", best);   // after every round!', { size: 38 });
  css(bad.c, { borderColor: "#ff5d6c" }); show(bad.c, T("s43")); bad.hl([[W("s43", "round"), 1, "rgba(255,93,108,.25)"]]); hide(bad.c, W("s45", "record") - 0.2, 0.25);
  const good = bigCode(mk, 90, 200, 1250, 'if (reaction < best) {\n  best = reaction;\n  prefs.putULong("best", best);\n}', { size: 38 });
  css(good.c, { borderColor: "#4ade80" }); show(good.c, W("s45", "record")); good.hl([[W("s45", "record"), 0, "rgba(74,222,128,.2)"]]);
  const slow = T("s45") + 0.2;
  const rows = serialAt(mk, 1400, 200, 440, 330, [[T("s44"), "reaction: 213"], [slow, "reaction: 870"]], 32); hidden(rows); show(rows, T("s44"));
  const b = live(mk, 160, 560, 520, "drawer: best", (t) => (t < slow ? "213" : t < W("s45", "record") ? "870 ✗" : "213 ✓"), "#ffb547"); show(b, T("s44"));
  ask(mk, "QUICK QUESTION", "Saved after every round, without the if. One slow round later, the record is...?", T("s44"), T("s45"), "Gone: the slow time is written over it.", { x: 110, y: 760, w: 1700, t1: W("s45", "record") - 0.2 });
}

/* ======================================================================
 * EXPLAIN, YOUR TURN (the project homework), OUTRO
 * ==================================================================== */
const ex = chapter("s46", "s48"); title(ex, "In your own words", "s46");
{
  const a = tile(ex, 210, 470, 1500, 330, '<div style="font:700 40px/1.5 var(--ui)">Variables live in memory that needs power. The drawer is flash memory: it keeps its contents without power.</div>', "var(--teal)");
  hidden(a); show(a, T("s47"));
  ask(ex, "PAUSE AND EXPLAIN", "Why does best alone forget the record, but the drawer keeps it?", T("s46"), T("s47"), "One sentence is enough.", { x: 210, y: 200, w: 1500, t1: S1("s47") });
}
const yt = chapter("s48", "s52"); const yh = title(yt, "", "s48");
textAt(yh, [[0, "A press during the yellow?"], [T("s50") - 0.2, "Your turn: a false start"]]);
{
  const mash = [0, 1, 2, 3, 4, 5].map((i) => [T("s49") + 0.3 + i * 0.32, T("s49") + 0.45 + i * 0.32]);
  const lucky = mash[3][0], goOn = lucky - 0.05;          // green happens to come on just before the 4th tap
  const cheat = (t) => (t < goOn ? { state: 2, color: "off" } : t < lucky ? { state: 3, color: "off" } : { state: 4, color: "green" });
  const flash = (t) => ({ state: 0, color: Math.floor((t - T("s50")) / 0.15) % 2 ? "red" : "off" });
  const ri = reflexIcon(yt, 160, 230, 0.9); hidden(ri.r); show(ri.r, T("s48")); ri.drive((t) => (t < T("s49") ? { state: 2, color: "off" } : t < T("s50") ? cheat(t) : flash(t)));
  const luck = pill(yt, 160, 800, "&#127922; green caught by luck: 50 ms", "font-size:30px;color:#ff8a8f"); show(luck, lucky + 0.2); hide(luck, T("s50") - 0.2, 0.2);
  const b = btnIcon(yt, 600, 560, 170); hidden(b.r); show(b.r, T("s48")); b.press(mash.concat([[W("s50", "press"), W("s50", "press") + 0.3]]));
  askTop(stage, "PAUSE AND PREDICT", "You press during the yellow. What does the game do now?", T("s48"), T("s49"), "Nothing: a cheater can tap again and again.", { x: 210, y: 820, w: 1500, t1: T("s50") - 0.3 });
  const hw = tile(yt, 880, 220, 940, 360, '<div class="kicker">PROJECT HOMEWORK</div><div style="font:800 48px var(--display);margin-top:16px">FALSE START!</div><div style="font:700 34px/1.6 var(--ui);margin-top:16px">Press during ' + dot("#ff4d5a") + ' or ' + dot("#ffd23a") + '<br>&rarr; the color LED flashes red, no time counts</div>', "#ff5d6c");
  hidden(hw); show(hw, T("s50"));
  const kn = tile(yt, 880, 610, 940, 260, '<div style="font:700 34px/1.6 var(--ui)">You need: <b style="color:var(--amber)">one more step number</b> + <b style="color:var(--amber)">one more check</b></div><div style="font:600 30px var(--ui);margin-top:14px;color:var(--muted)">Solution: lessons/10-reflex-game &rarr; challenge_false_start &middot; and in a Short</div>', "var(--teal)");
  hidden(kn); show(kn, T("s51"));
}
const out = chapter("s52", null); title(out, "Your first project: done", "s52");
{
  [["a game of steps", "state + goTo()", W("s52", "steps")], ["a reaction time", "= the time in one step", W("s52", "reaction")], ["a record", "kept in the drawer", W("s52", "drawer")]].forEach(([a, b, t0], i) => {
    const c = tile(out, 115 + i * 575, 230, 540, 340, `<div style="font:800 46px var(--display);color:var(--teal)">${a}</div><div style="font:700 36px/1.5 var(--mono);margin-top:40px">${b}</div>`);
    hidden(c); show(c, t0); hide(c, T("s53") - 0.15, 0.25);
  });
  const next = tile(out, 210, 200, 1500, 420, '<div class="kicker">NEXT: RECAP 2</div><div style="font:800 62px var(--display);margin-top:26px">Everything since episode 5</div><div style="font:600 36px var(--ui);margin-top:20px;color:var(--muted)">PWM, the color LED, the knob, map() and steps, with a quiz.</div><div style="font-size:90px;margin-top:20px">&#129504;&#9989;</div>');
  hidden(next); show(next, T("s53"));
  note(out, "Your best reaction time? Tell me in the comments.", W("s53", "comments") - 0.6, 690);
  note(out, "github.com/emjnbulut/esp32-from-zero &rarr; lessons/10-reflex-game", W("s53", "comments") - 0.6, 820);
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 }); TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}
window.__seek(0);
window.__ready = true;
