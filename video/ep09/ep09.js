/* Episode 9 Mini Project 1, a Smart Pedestrian Crossing: segment-anchored scenes, creator footage C0-C2, code tours.
 * Clips are 16:9 (the shoot pack asks for landscape): a 1200x675 window on the left, the drawing on the right; the
 * window size and EP09_CLIP_SECONDS get their final values once the creator's clips are prepared in footage/ep09.
 * A small simulator (sim) drives every drawn crossing, so the drawings follow the same rules as crossing.ino. */
const stage = $("#stage");
const EP09_CLIP_SECONDS = { C0: 25, C1: 10, C2: 8 }; // placeholders until footage/ep09 exists
function hero(id, t0, requestedEnd, description, opts = {}) {
  const lead = opts.full ? Math.min(0.3, t0) : 0;
  const tail = opts.full ? 0.35 : 0;
  const t1 = Math.min(requestedEnd, t0 + EP09_CLIP_SECONDS[id] - lead - tail - 1 / 30);
  if (!(t1 > t0)) throw new Error("No usable episode 9 footage: " + id);
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
const pillC = (parent, y, html, style = "", x = 0, w = 1920) => hidden(box(parent, x, y, w, 70, "", `<div style="display:flex;justify-content:center"><span class="pill" style="font-size:32px;${style}">${html}</span></div>`));

/* ---- the crossing simulator: the same rules as crossing.ino, in seconds ----
 * sim({ t0, press, green, yellow, walk, blink, mistake }) -> (t) => { state, inState, blinkOn, request }
 * press: when the button is pressed (or null); green: knob green time; mistake: step 1 never gets a new start time */
function sim(o) {
  const g = o.green != null ? o.green : 3, y = o.yellow != null ? o.yellow : 2, w = o.walk != null ? o.walk : 4, b = o.blink != null ? o.blink : 2;
  const t0 = o.t0, press = o.press;
  return (t) => {
    if (t < t0 || press == null || t < press) return { state: 0, inState: Math.max(0, t - t0), blinkOn: true, request: false };
    const a1 = Math.max(press, t0 + g);                 // leaves step 0
    const y1 = o.mistake ? 0.12 : y;                     // the forgotten start time: step 1 ends at once
    const a2 = a1 + y1, a3 = a2 + w, a0 = a3 + b;
    if (t < a1) return { state: 0, inState: t - t0, blinkOn: true, request: true };
    if (t < a2) return { state: 1, inState: o.mistake ? t - t0 : t - a1, blinkOn: true, request: true };
    if (t < a3) return { state: 2, inState: t - a2, blinkOn: true, request: false };
    if (t < a0) return { state: 3, inState: t - a3, blinkOn: Math.floor((t - a3) / 0.25) % 2 === 1, request: false };
    return { state: 0, inState: t - a0, blinkOn: true, request: false };
  };
}
/** the five lights for a step: [red, yellow, green, walkRed, walkGreen] */
const LIGHTS = (s) => [[0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, s.blinkOn ? 1 : 0]][s.state];

/** a drawn car signal (three lamps) + a walk signal (the RGB LED: ✋ red / 🚶 green); drive(fn) with fn(t) = sim state */
function crossingIcon(parent, x, y, s = 1) {
  const r = box(parent, x, y, 420 * s, 470 * s, "");
  r.innerHTML = `<svg width="${420 * s}" height="${470 * s}" viewBox="0 0 420 470" style="position:absolute;left:0;top:0;overflow:visible">
    <rect x="20" y="10" width="150" height="400" rx="30" fill="#1b2130" stroke="#3a4560" stroke-width="5"/>
    <path d="M95 410 V465" stroke="#3a4560" stroke-width="16"/>
    <circle class="c0" cx="95" cy="85" r="50"/><circle class="c1" cx="95" cy="210" r="50"/><circle class="c2" cx="95" cy="335" r="50"/>
    <rect x="240" y="120" width="160" height="200" rx="26" fill="#1b2130" stroke="#3a4560" stroke-width="5"/>
    <path d="M320 320 V465" stroke="#3a4560" stroke-width="16"/>
    <circle class="w" cx="320" cy="220" r="62"/>
    <text class="wi" x="320" y="246" text-anchor="middle" font-size="72"></text>
    <text x="95" y="-14" text-anchor="middle" font-size="28" font-weight="700" fill="#8fa1c0" font-family="Segoe UI">cars</text>
    <text x="320" y="96" text-anchor="middle" font-size="28" font-weight="700" fill="#8fa1c0" font-family="Segoe UI">walker</text></svg>`;
  const cs = [$(".c0", r), $(".c1", r), $(".c2", r)], wl = $(".w", r), wi = $(".wi", r);
  const ON = ["#ff4d5a", "#ffd23a", "#36e07a"], OFF = ["#4a1f25", "#4a3f17", "#173d26"];
  const drive = (fn) => dyn((t) => {
    const L = LIGHTS(fn(t));
    cs.forEach((c, i) => { c.setAttribute("fill", L[i] ? ON[i] : OFF[i]); c.style.filter = L[i] ? `drop-shadow(0 0 22px ${ON[i]})` : "none"; });
    const col = L[4] ? "#36e07a" : L[3] ? "#ff4d5a" : "#2a3140";
    wl.setAttribute("fill", col); wl.style.filter = L[3] || L[4] ? `drop-shadow(0 0 26px ${col})` : "none";
    const ic = L[4] ? "🚶" : L[3] ? "✋" : "";
    if (wi.textContent !== ic) wi.textContent = ic;
  });
  return { r, drive };
}
/** the four steps as a loop of boxes; fn(t) = sim state, the current step is lit */
const STEPS = [["0", "cars green", "#36e07a"], ["1", "cars yellow", "#ffd23a"], ["2", "walker crosses", "#5aa9ff"], ["3", "walk light blinks", "#b48cff"]];
function stepLoop(parent, x, y, w = 820, fn = null) {
  const g = box(parent, x, y, w, 520, "");
  const pos = [[0, 0], [w - 360, 0], [w - 360, 330], [0, 330]];
  const els = STEPS.map(([n, lab, col], i) => {
    const e = box(g, pos[i][0], pos[i][1], 360, 170, "stepbox", `<div class="n" style="color:${col}">${n}</div><div class="l">${lab}</div>`);
    e.style.setProperty("--c", col);
    return e;
  });
  const sv = svgEl(g, "svg", { width: w, height: 520, viewBox: `0 0 ${w} 520` }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible", pointerEvents: "none" });
  const arr = (d) => { svgEl(sv, "path", { d, fill: "none", stroke: "#5f6f8f", "stroke-width": 6, "marker-end": "url(#ah9)" }); };
  svgEl(sv, "defs").innerHTML = '<marker id="ah9" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#5f6f8f"/></marker>';
  arr(`M370 85 H${w - 375}`); arr(`M${w - 180} 180 V318`); arr(`M${w - 370} 415 H375`); arr("M180 320 V182");
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
const repo = "Full code: <b>github.com/emjnbulut/esp32-from-zero</b> &rarr; lessons/09-mini-project-1";
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

/* ======================================================================
 * COLD OPEN: the real crossing, then the promise
 * ==================================================================== */
const cold = SC(); SET(cold, 0, { opacity: 1 }); SET(cold, CUT, { opacity: 0 });
{
  const h = box(cold, 1310, 150, 560, 200, "", '<div style="font:800 58px/1.15 var(--display)">A smart<br><span style="color:var(--amber)">pedestrian crossing</span></div>');
  hidden(h); show(h, 0.6);
  const steps = box(cold, 1310, 400, 560, 330, "", ["🟢 cars green", "🟡 cars yellow", "🔴 cars red &middot; 🚶 walk"].map((s) => `<div style="font:700 38px/1.9 var(--ui)">${s}</div>`).join(""));
  hidden(steps); show(steps, W("s01", "press"));
  const one = tile(cold, 1310, 400, 560, 330, '<div class="kicker">MINI PROJECT 1</div><div style="font:800 46px/1.3 var(--display);margin-top:20px">One variable remembers the step</div><div style="font:700 44px var(--mono);margin-top:24px;color:var(--amber)">int state = 0;</div>', "var(--amber)");
  hidden(one); hide(steps, T("s02") - 0.2, 0.25); show(one, T("s02"));
}
hero("C0", 0, CUT, "crossing: cars green, a press, yellow, red + walk green.", WIN);

/* ======================================================================
 * RETRIEVAL (episodes 8 and 4) + the way in for new viewers
 * ==================================================================== */
const ret = chapter("s03", "s08"); title(ret, "Two questions from earlier episodes", "s03");
{
  const nw = pill(ret, 1340, 150, "New here? Start at Episode 1 &rarr;", "font-size:28px;color:var(--teal)"); show(nw, T("s03") + 0.2); hide(nw, T("s04") + 1.5, 0.3);
  const c = bigCode(ret, 260, 230, 1400, "int level = map(value, 0, 4095, 0, 3);", { size: 50 }); show(c.c, T("s04")); hide(c.c, T("s06") - 0.2, 0.25);
  const strip = box(ret, 260, 430, 1400, 120, "", '<div style="display:flex;gap:6px;font:800 36px/120px var(--ui);color:#0b1220;text-align:center"><div style="flex:1;background:#2a3550;color:#c9d1dc;border-radius:12px">level 0</div><div style="flex:1;background:#4ade80;border-radius:12px">level 1</div><div style="flex:1;background:#ffe14d;border-radius:12px">level 2</div><div style="width:12px;background:#ff5d6c;border-radius:6px"></div></div>');
  hidden(strip); show(strip, T("s05")); hide(strip, T("s06") - 0.2, 0.25);
  ask(ret, "QUICK QUESTION", "The obvious level line almost never lit all three LEDs. Why?", T("s04"), T("s05"), "map() rounds down: level 3 only at the very last mark.", { y: 700, w: 1500, t1: T("s06") - 0.2 });
  const clock = box(ret, 300, 230, 330, 330, "", '<div style="font-size:250px;line-height:330px;text-align:center">🕰️</div>'); hidden(clock); show(clock, T("s06")); hide(clock, T("s08") - 0.3, 0.25);
  const c2 = bigCode(ret, 700, 260, 960, "if (now - last >= 2000) {\n  // two seconds have passed\n}", { size: 44 }); show(c2.c, T("s07")); hide(c2.c, T("s08") - 0.3, 0.25);
  ask(ret, "QUICK QUESTION", "How can the board tell that 2 s have passed, without delay()?", T("s06"), T("s07"), "Glance at millis(): now minus the remembered moment.", { y: 700, w: 1500, t1: S1("s07") });
}

/* ======================================================================
 * THE PLAN: car lights, walk light, button, knob; no new wire
 * ==================================================================== */
const pl = chapter("s08", "s12"); title(pl, "The plan", "s08"); likeTop(T("s08") + 1.0);
{
  const demo = sim({ t0: T("s08"), press: T("s08") + 1.5, green: 0.5, yellow: 1.2, walk: 2.4, blink: 1.2 });
  const cx = crossingIcon(pl, 160, 220, 1.15); hidden(cx.r); show(cx.r, T("s08")); cx.drive(demo); hide(cx.r, T("s10") - 0.2, 0.25);
  const t1 = tile(pl, 820, 210, 980, 240, '<div style="font:800 40px var(--display)">Car lights &rarr; the 3 LEDs</div><div style="font:700 34px/1.6 var(--ui);margin-top:14px;color:var(--muted)">Walk light &rarr; the color LED: <b style="color:#ff5d6c">red</b> wait, <b style="color:#36e07a">green</b> walk</div>', "var(--amber)");
  hidden(t1); show(t1, T("s08") + 0.4); hide(t1, T("s10") - 0.2, 0.25);
  const t2 = tile(pl, 820, 480, 980, 300, '<div style="display:flex;gap:40px;align-items:center"><div style="width:170px;height:170px" class="bslot"></div><div style="font:700 34px/1.5 var(--ui)">Button &rarr; <b>request to cross</b><br>Knob &rarr; cars\' green: <b style="color:var(--amber)">3 &ndash; 10 s</b></div></div>', "var(--teal)");
  hidden(t2); show(t2, T("s09")); hide(t2, T("s10") - 0.2, 0.25);
  const b = btnIcon(t2, 40, 40, 110); b.press([[T("s09") + 0.6, T("s09") + 1.1]]);
  const k = knobIcon(t2, 160, 40, 120); k.drive((t) => sweep(t, T("s09"), 4));
  const pins = tile(pl, 260, 200, 1400, 560, '<div style="font:800 46px var(--display)">No new wire: everything is already on the board</div>' +
    '<div class="pins"><div><b style="color:#ff5d6c">car red</b> D23</div><div><b style="color:#ffd23a">car yellow</b> D18</div><div><b style="color:#36e07a">car green</b> TX2 (pin 17)</div>' +
    '<div><b style="color:#ff5d6c">walk red</b> D25</div><div><b style="color:#36e07a">walk green</b> D26</div><div><b style="color:var(--amber)">button</b> D22</div><div><b style="color:var(--amber)">knob</b> D34</div></div>', "var(--teal)");
  hidden(pins); show(pins, T("s10"));
  note(pl, "The full wiring is in the lesson folder: lessons/09-mini-project-1", T("s11"), 800);
}

/* ======================================================================
 * WHY NOT A CHAIN OF DELAYS
 * ==================================================================== */
const dl = chapter("s12", "s15"); title(dl, "The first idea: a chain of delays", "s12");
{
  const c = bigCode(dl, 160, 200, 980, "green();   delay(5000);\nyellow();  delay(2000);\nred();     delay(4000);", { size: 50 }); show(c.c, T("s12"));
  const hl = [[T("s12"), 0], [T("s13"), 2], [T("s14"), 2, "rgba(255,93,108,.25)"]];
  c.hl(hl);
  const b = btnIcon(dl, 1340, 230, 200); hidden(b.r); show(b.r, T("s13")); b.press([[T("s13") + 1.0, T("s13") + 1.5], [T("s14"), T("s14") + 0.5]]);
  const lost = box(dl, 1250, 470, 520, 160, "", '<div style="font:800 54px/1.3 var(--display);text-align:center;color:#ff8a8f">press lost &#10007;</div><div style="font:600 30px var(--ui);text-align:center;color:var(--muted)">nobody looks at the button</div>');
  hidden(lost); show(lost, T("s14"));
  askTop(stage, "PAUSE AND PREDICT", "What happens to a button press while the program waits in delay()?", T("s13"), T("s14"), "It's lost: during delay() no other line runs.", { x: 210, y: 790, w: 1500, t1: T("s15") - 0.3 });
}

/* ======================================================================
 * THE IDEA: a washing machine -> four numbered steps -> state
 * ==================================================================== */
const id9 = chapter("s15", "s20"); const ih = title(id9, "", "s15");
textAt(ih, [[0, "Think of a washing machine"], [T("s16") - 0.2, "Four steps, numbered from 0"], [T("s17") - 0.2, "The step is a number: state"], [T("s18") - 0.2, "Moving on = new number + the time"]]);
{
  exCard("🧺", "A washing machine", "Wash, rinse, spin: it always knows which step it is in, and moves on when the step's time is up.", T("s15"), T("s16") - 0.25);
  const run = sim({ t0: T("s16"), press: T("s16") + 0.5, green: 1.6, yellow: 1.6, walk: 2.2, blink: 1.6 });
  const loopU = stepLoop(id9, 140, 200, 900, run); hidden(loopU.g); show(loopU.g, T("s16"));
  const cx = crossingIcon(id9, 1230, 230, 1.0); hidden(cx.r); show(cx.r, T("s16")); cx.drive(run); hide(cx.r, T("s17") - 0.2, 0.25);
  const c = bigCode(id9, 1130, 210, 700, "int state = 0;", { size: 52 }); show(c.c, T("s17")); hide(c.c, T("s18") - 0.2, 0.25);
  const ex = bigCode(id9, 1130, 400, 700, "if (state == 0) {\n  ...\n} else if (state == 1) {\n  ...\n}", { size: 36 }); show(ex.c, W("s17", "checks")); hide(ex.c, T("s18") - 0.2, 0.25);
  const mv = bigCode(id9, 1130, 260, 700, "state = 1;\nstateStart = now;", { size: 48 }); show(mv.c, T("s18")); mv.hl([[W("s18", "next"), 0], [W("s18", "time"), 1]]); hide(mv.c, T("s19") - 0.2, 0.25);
  const ma = pill(id9, 1130, 520, "that moment = the start of the new step", "font-size:30px;color:var(--teal)"); show(ma, W("s18", "moment")); hide(ma, T("s19") - 0.2, 0.25);
  const lim = tile(id9, 1130, 230, 700, 520, '<div style="font-size:90px;line-height:1">🧺</div><div style="font:700 34px/1.45 var(--ui);margin-top:24px;color:#ffe3b8"><b style="color:var(--amber)">The difference:</b> the machine really does its step. Our loop never waits inside a step: it looks at the number thousands of times a second, and decides.</div>', "var(--amber)");
  hidden(lim); show(lim, T("s19"));
}

/* ======================================================================
 * CODE TOUR: crossing (top, helpers, the button)
 * ==================================================================== */
tour("crossing", T("s20") - 0.4, T("s24") - 0.3, [
  [W("s20", "pins"), "const int CAR_RED", "const int POT_PIN"], [W("s20", "state"), "int state = 0;"], [W("s20", "began"), "unsigned long stateStart"],
  [T("s21"), "void lights(", "}"], [T("s22"), "void goTo(", "}"],
  [T("s23"), "// PART 1", "Serial.println(\"request\")"], [W("s23", "counts"), "if (b == LOW && state == 0)"], [W("s23", "remembers"), "request = true;"],
  [T("s23b"), "if (b == LOW && state == 0)"], [T("s23c"), "if (b == LOW && state == 0)"]]);
askTop(stage, "PAUSE AND PREDICT", "The walker is already crossing. You press the button. Does it count?", T("s23b"), T("s23c"), "No: presses only count in step 0.", { x: 210, y: 820, w: 1500, t1: T("s24") - 0.3 });

/* ======================================================================
 * THE CLOCK: how long in this step + the green time from the knob
 * ==================================================================== */
const ck = chapter("s24", "s26"); title(ck, "Part 2: the clock", "s24");
{
  const c = bigCode(ck, 110, 200, 1700, "unsigned long inState = now - stateStart;", { size: 50 }); show(c.c, T("s24"));
  const tl0 = T("s24") + 0.3;
  const st = live(ck, 260, 420, 440, "stateStart", () => ms(tl0).toLocaleString("en-US") + "", "#5aa9ff"); show(st, W("s24", "began"));
  const nw = live(ck, 740, 420, 440, "now", (t) => ms(Math.max(t, tl0)).toLocaleString("en-US"), "#c9d1dc"); show(nw, W("s24", "minus") - 0.3);
  const ins = live(ck, 1220, 420, 440, "inState (ms)", (t) => ms(Math.max(0, t - tl0)).toLocaleString("en-US")); show(ins, W("s24", "long") - 0.2);
  const g = bigCode(ck, 110, 640, 1700, "greenTime = map(analogRead(POT_PIN), 0, 4095, 3000, 10000);", { size: 40 }); show(g.c, T("s25"));
  const k = knobIcon(ck, 260, 820, 200); hidden(k.r); show(k.r, W("s25", "knob")); const pos = (t) => sweep(t, T("s25"), 5); k.drive(pos);
  const gt = live(ck, 560, 840, 600, "greenTime (ms)", (t) => mapI(Math.round(4095 * pos(t)), 0, 4095, 3000, 10000).toLocaleString("en-US"), "#36e07a"); show(gt, W("s25", "green"));
  const cm = pill(ck, 1240, 880, "&#128506; last episode's city map, doing a real job", "font-size:30px;color:var(--teal)"); show(cm, W("s25", "real"));
}

/* ======================================================================
 * THE STEPS, one at a time (step 1: pause and try it yourself)
 * ==================================================================== */
const stp = chapter("s26", "s32"); const sh = title(stp, "", "s26");
textAt(sh, [[0, "Step 0: cars green"], [T("s28") - 0.2, "Your turn first: write step 1"], [T("s29") - 0.2, "Step 1: cars yellow"], [T("s30") - 0.2, "Step 2: the walker crosses"], [T("s31") - 0.2, "Step 3: the walk light blinks"]]);
{
  const fake = (t) => {
    if (t < T("s28")) return { state: 0, blinkOn: true };
    if (t < T("s30")) return { state: 1, blinkOn: true };
    if (t < T("s31")) return { state: 2, blinkOn: true };
    return { state: 3, blinkOn: Math.floor((t - T("s31")) / 0.25) % 2 === 1 };
  };
  const sl = stepLoop(stp, 1080, 210, 740, fake); hidden(sl.g); show(sl.g, T("s26"));
  const cx = crossingIcon(stp, 1250, 650, 0.62); hidden(cx.r); show(cx.r, T("s26")); cx.drive((t) => (t >= T("s28") && t < T("s29") ? { state: 0, blinkOn: true } : fake(t)));
  const s0 = bigCode(stp, 90, 200, 940, "if (state == 0) {\n  lights(LOW, LOW, HIGH, HIGH, LOW);\n  if (request && inState >= greenTime) {\n    goTo(1, now);\n  }\n}", { size: 34 });
  show(s0.c, T("s26")); s0.hl([[W("s26", "green"), 1], [W("s26", "waiting"), 2], [W("s26", "step", 2), 3], [T("s27"), 2]]); hide(s0.c, T("s28") - 0.2, 0.25);
  const amp = pill(stp, 120, 640, "<b style=\"font-family:var(--mono)\">&amp;&amp;</b> = and: both checks must be true", "font-size:34px;color:var(--teal)"); show(amp, T("s27")); hide(amp, T("s28") - 0.2, 0.25);
  const tryIt = tile(stp, 90, 210, 940, 520, '<div class="kicker">PAUSE &middot; TRY IT YOURSELF</div><div style="font:800 46px/1.35 var(--display);margin-top:24px">Write step 1</div><div style="font:600 36px/1.6 var(--ui);margin-top:20px;color:var(--muted)">Cars <b style="color:#ffd23a">yellow</b> for 2 s,<br>then go to step 2.</div><div class="qbar" style="margin-top:36px"><i class="tb"></i></div>', "var(--amber)");
  hidden(tryIt); show(tryIt, T("s28")); hide(tryIt, T("s29") - 0.2, 0.25);
  TO($(".tb", tryIt), T("s28") + 0.6, Math.max(0.5, T("s29") - T("s28") - 0.8), { width: "100%", ease: "none" });
  const s1 = bigCode(stp, 90, 200, 940, "} else if (state == 1) {\n  lights(LOW, HIGH, LOW, HIGH, LOW);\n  if (inState >= 2000) {\n    request = false;\n    goTo(2, now);\n  }", { size: 34 });
  show(s1.c, T("s29")); s1.hl([[W("s29", "Yellow"), 1], [W("s29", "passed"), 2], [W("s29", "forget"), 3], [W("s29", "step"), 4]]); hide(s1.c, T("s30") - 0.2, 0.25);
  const s2 = bigCode(stp, 90, 200, 940, "} else if (state == 2) {\n  lights(HIGH, LOW, LOW, LOW, HIGH);\n  if (inState >= 4000) {\n    goTo(3, now);\n  }", { size: 34 });
  show(s2.c, T("s30")); s2.hl([[T("s30"), 1], [W("s30", "four"), 2]]); hide(s2.c, T("s31") - 0.2, 0.25);
  const s3 = bigCode(stp, 90, 200, 940, "} else {\n  if (now - lastBlink >= 250) {\n    lastBlink = now;\n    blinkOn = !blinkOn;\n  }\n  lights(HIGH, LOW, LOW, LOW, blinkOn ? HIGH : LOW);\n  if (inState >= 2000) {\n    goTo(0, now);\n  }", { size: 30 });
  show(s3.c, T("s31")); s3.hl([[W("s31", "clock"), 1], [W("s31", "flipping"), 3], [W("s31", "seconds"), 6]]);
  const pen = pill(stp, 120, 920, "&#128394; the click pen from episode 4: <b style=\"font-family:var(--mono)\">!</b> flips it", "font-size:30px;color:var(--teal)"); show(pen, W("s31", "flipping")); hide(pen, T("s32") - 0.3, 0.2);
}

/* s32 - s33: predict the early press, on a timeline */
const er = chapter("s32", "s34"); title(er, "Pressed right after the cars got green", "s32");
{
  const X = 160, Wd = 1600, Y = 520, G = 6; // a 6 s knob time, drawn
  const tl = box(er, X, Y, Wd, 260, ""); hidden(tl); show(tl, T("s32"));
  const sv = svgEl(tl, "svg", { width: Wd, height: 260, viewBox: `0 0 ${Wd} 260` }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  const sx = (s) => (s / 11) * Wd;
  svgEl(sv, "rect", { x: 0, y: 60, width: sx(G), height: 70, rx: 12, fill: "#36e07a" });
  svgEl(sv, "rect", { x: sx(G) + 4, y: 60, width: sx(2) - 4, height: 70, rx: 12, fill: "#ffd23a" });
  svgEl(sv, "rect", { x: sx(G + 2) + 4, y: 60, width: sx(3) - 4, height: 70, rx: 12, fill: "#ff4d5a" });
  txt(sv, 20, 108, "cars green: the knob's time", { "font-size": 34, fill: "#0b1220" });
  txt(sv, sx(G) + 20, 108, "yellow", { "font-size": 34, fill: "#0b1220" });
  txt(sv, sx(G + 2) + 20, 108, "walk", { "font-size": 34, fill: "#0b1220" });
  const pr = svgEl(sv, "path", { d: `M${sx(0.4)} 10 V180`, stroke: "#ffb547", "stroke-width": 6, "stroke-dasharray": "10 8" });
  txt(sv, sx(0.4) - 6, 220, "press! (remembered)", { "font-size": 32, fill: "#ffb547" });
  const ptr = svgEl(sv, "path", { d: "M-16 0 H16 L0 34 Z", fill: "#ffffff" });
  dyn((t) => { const s = clamp((t - T("s33")) * 1.6, 0, 11); ptr.setAttribute("transform", `translate(${sx(s)} 20)`); });
  const rq = live(er, 260, 220, 520, "request", (t) => (t >= T("s32") + 1.2 ? "true" : "false"), "#ffb547"); show(rq, T("s32") + 0.8);
  const cx = crossingIcon(er, 1300, 120, 0.72); hidden(cx.r); show(cx.r, T("s33"));
  cx.drive((t) => { const s = (t - T("s33")) * 1.6; return { state: s < G ? 0 : s < G + 2 ? 1 : 2, blinkOn: true }; });
  askTop(stage, "PAUSE AND PREDICT", "Cars just turned green, you press at once. Does the walker get green at once?", T("s32"), T("s33"), "No: the cars keep green until the knob's time is up.", { x: 210, y: 820, w: 1500, t1: T("s34") - 0.3 });
}

/* s34 - s35: the real crossing, then the blink up close */
const rn = chapter("s34", "s36");
{
  const r1 = tile(rn, 1310, 200, 560, 560, '<div class="kicker">ON THE REAL BOARD</div><div style="font:700 36px/1.6 var(--ui);margin-top:24px">A whole round.<br><span style="color:var(--muted)">Watch the walk light:</span><br><b style="color:#ff5d6c">red</b> &rarr; <b style="color:#36e07a">green</b></div>', "var(--teal)");
  hidden(r1); show(r1, T("s34")); hide(r1, T("s35") - 0.2, 0.25);
  const r2 = tile(rn, 1310, 200, 560, 560, '<div class="kicker">THE LAST 2 SECONDS</div><div style="font:700 36px/1.6 var(--ui);margin-top:24px">The walk light blinks: <b style="color:var(--amber)">hurry!</b><br><span style="color:var(--muted)">Cars: still</span> <b style="color:#ff5d6c">red</b></div><div style="font:700 40px var(--mono);margin-top:30px;color:#b48cff">state = 3</div>', "#b48cff");
  hidden(r2); show(r2, T("s35"));
}
hero("C0", T("s34"), T("s35") - 0.35, "crossing on the real board: a whole round.", WIN);
hero("C2", T("s35"), T("s36") - 0.35, "Close-up: the walk light blinking in the last 2 s, car red on.", WIN);

/* s36 - s37: modify: 4000 -> 8000 */
const md = chapter("s36", "s38"); title(md, "Change one number", "s36"); likeTop(T("s37") + 1.2);
{
  const c = box(md, 210, 200, 1500, 150, "card", '<div style="font:800 54px/150px var(--mono);text-align:center;white-space:nowrap">if (inState &gt;= <span class="arg sw">4000</span>) {</div>');
  hidden(c); show(c, T("s36")); textAt($(".sw", c), [[0, "4000"], [T("s37"), "8000"]]); styleAt($(".sw", c), "background", [[0, "transparent"], [W("s36", "eight"), "#5aa9ff55"]]);
  const X = 210, Wd = 1500, Y = 470, sx = (s) => (s / 18) * Wd;
  const bars = (y, walk, lab, t0) => {
    const g = box(md, X, y, Wd, 120, ""); hidden(g); show(g, t0);
    const sv = svgEl(g, "svg", { width: Wd, height: 120, viewBox: `0 0 ${Wd} 120` }); css(sv, { position: "absolute", left: 0, top: 0, overflow: "visible" });
    let x = 0;
    for (const [d, col, n] of [[4, "#36e07a", "0"], [2, "#ffd23a", "1"], [walk, "#5aa9ff", "2"], [2, "#b48cff", "3"]]) {
      svgEl(sv, "rect", { x: sx(x) + 2, y: 10, width: sx(d) - 4, height: 70, rx: 10, fill: col }); txt(sv, sx(x) + 16, 58, n, { "font-size": 34, fill: "#0b1220" }); x += d;
    }
    txt(sv, Wd, 112, lab, { "font-size": 30, "text-anchor": "end" });
    return g;
  };
  bars(Y, 4, "walk: 4 s", T("s36") + 0.3);
  bars(Y + 170, 8, "walk: 8 s (twice as long)", T("s37"));
  note(md, "Nothing else moves: every step keeps its own time.", W("s37", "Nothing"), 860);
  askTop(stage, "PAUSE AND PREDICT", "4000 becomes 8000. What changes?", T("s36"), T("s37"), "The walker gets twice as long to cross.", { x: 210, y: 820, w: 1500, t1: T("s37") - 0.05 });
}

/* ======================================================================
 * HOW LONG WAS IT HELD: a parking ticket
 * ==================================================================== */
const tk = chapter("s38", "s42"); const th = title(tk, "", "s38");
textAt(th, [[0, "How long was the button held?"], [T("s40") - 0.2, "pressStart: the stamped ticket"]]);
{
  exCard("🎫", "A parking ticket", "Stamped with the time when you drive in. At the exit: now minus that time.", T("s38") + 0.6, T("s40") - 0.25);
  const pS = T("s40") + 1.6, pE = pS + 1.25;
  const b = btnIcon(tk, 230, 230, 220); hidden(b.r); show(b.r, T("s40")); b.press([[pS, pE]]);
  const c = bigCode(tk, 560, 220, 1250, "pressStart = now;            // at the press\nheld = now - pressStart;     // at the release", { size: 40 }); show(c.c, T("s40")); c.hl([[W("s40", "press"), 0], [W("s40", "release"), 1]]);
  const s = live(tk, 560, 470, 540, "pressStart", (t) => (t >= pS ? ms(pS).toLocaleString("en-US") : "?"), "#5aa9ff"); show(s, W("s40", "press"));
  const hd = live(tk, 1150, 470, 600, "held (ms)", (t) => (t < pS ? "" : ms(Math.min(t, pE) - pS).toLocaleString("en-US")), "#ffb547"); show(hd, W("s40", "release"));
  const lim = tile(tk, 230, 700, 1580, 200, '<div style="font:700 34px/1.5 var(--ui);color:#ffe3b8"><b style="color:var(--amber)">The difference:</b> there\'s no paper. pressStart is one number in memory, and the next press writes over it.</div>', "var(--amber)");
  hidden(lim); show(lim, T("s41"));
}
tour("press_time", T("s42") - 0.4, T("s44") - 0.3, [
  [W("s42", "yellow"), "if (b == LOW) {", "digitalWrite(LED_PIN, HIGH);"], [W("s42", "go"), "} else {", "unsigned long held"], [W("s42", "prints"), "Serial.print(held);", "Serial.println(\"long\");"],
  [T("s43"), "if (held < 250) {"]]);
askTop(stage, "PAUSE AND PREDICT", "You tap the button as fast as you can. What will it print?", W("s43", "Pause"), T("s44"), "About 100 ms: short.", { x: 210, y: 820, w: 1500, t1: T("s44") - 0.3 });

/* s44 - s45: the real presses + the phone */
const rp = chapter("s44", "s46");
{
  const sm = serialAt(rp, 1310, 200, 560, 420, [[T("s44") + 0.4, "112 ms: short"], [W("s44", "Hold") + 1.2, "1034 ms: long"]], 40);
  hidden(sm); show(sm, T("s44")); hide(sm, T("s45") - 0.2, 0.25);
  const ph = tile(rp, 1310, 200, 560, 560, '<div style="font-size:110px;line-height:1">📱</div><div style="font:700 36px/1.6 var(--ui);margin-top:24px">One button, two jobs:<br><b style="color:var(--teal)">tap</b> &rarr; wake up<br><b style="color:var(--amber)">long press</b> &rarr; power off</div>', "var(--teal)");
  hidden(ph); show(ph, T("s45"));
  const sm2 = serialAt(rp, 110, 200, 1100, 560, [[T("s45"), "112 ms: short"], [T("s45"), "1034 ms: long"]], 46);
  hidden(sm2); show(sm2, T("s45")); // after the clip window closes, the same two lines stay on the left
}
hero("C1", T("s44"), T("s45") - 0.35, "press_time: a quick tap, then a one-second hold; yellow is on while held.", WIN);

/* ======================================================================
 * THE COMMON MISTAKE: a new step without a new start time
 * ==================================================================== */
const mk = chapter("s46", "s50"); const mh = title(mk, "", "s46");
textAt(mh, [[0, "A mistake you might make"], [T("s48") - 0.2, "Yellow for a split second"], [T("s49") - 0.2, "goTo() does both jobs"]]);
{
  const bad = bigCode(mk, 110, 200, 900, "if (request && inState >= greenTime) {\n  state = 1;          // no new start time!\n}", { size: 36 });
  css(bad.c, { borderColor: "#ff5d6c" }); show(bad.c, T("s46")); bad.hl([[W("s46", "state"), 1, "rgba(255,93,108,.25)"]]); hide(bad.c, T("s49") - 0.2, 0.25);
  const good = bigCode(mk, 110, 200, 900, "if (request && inState >= greenTime) {\n  goTo(1, now);       // new number + the time\n}", { size: 36 });
  css(good.c, { borderColor: "#4ade80" }); show(good.c, T("s49")); good.hl([[T("s49"), 1, "rgba(74,222,128,.2)"]]);
  const flashAt = T("s48") + 0.5;
  const wrong = sim({ t0: T("s48") - 6, press: flashAt - 0.01, green: 0, mistake: true, walk: 6 });
  const right = sim({ t0: T("s49") - 6, press: T("s49") + 0.6, green: 0, walk: 6 });
  const cx = crossingIcon(mk, 1250, 190, 0.85); hidden(cx.r); show(cx.r, T("s47"));
  cx.drive((t) => (t < T("s48") ? { state: 0, blinkOn: true } : t < T("s49") ? wrong(t) : right(t)));
  const st = live(mk, 160, 560, 400, "stateStart", (t) => (t < T("s49") ? "old" : "now"), "#5aa9ff"); show(st, T("s48"));
  const ins = live(mk, 600, 560, 420, "inState", (t) => (t < T("s48") ? "" : t < T("s49") ? "≫ 2000" : ms(Math.max(0, t - T("s49") - 0.6)).toLocaleString("en-US")), "#ffb547"); show(ins, W("s48", "subtraction") - 0.3);
  ask(mk, "QUICK QUESTION", "Moved on with just state = 1. What does the crossing do?", T("s47"), T("s48"), "Yellow flashes for an instant: the old start time says 2 s are long gone.", { x: 110, y: 760, w: 1700, t1: T("s49") - 0.2 });
}

/* ======================================================================
 * EXPLAIN, YOUR TURN, OUTRO
 * ==================================================================== */
const ex = chapter("s50", "s52"); title(ex, "In your own words", "s50");
{
  const a = tile(ex, 210, 470, 1500, 330, '<div style="font:700 40px/1.5 var(--ui)">Every step measures from the moment it began &rarr; a new step needs a new start, or it thinks its time is already up.</div>', "var(--teal)");
  hidden(a); show(a, T("s51"));
  ask(ex, "PAUSE AND EXPLAIN", "Why does each step need its own start time?", T("s50"), T("s51"), "One sentence is enough.", { x: 210, y: 200, w: 1500, t1: S1("s51") });
}
const yt = chapter("s52", "s54"); title(yt, "Your turn: slow walker mode", "s52");
{
  const b = btnIcon(yt, 260, 250, 200); hidden(b.r); show(b.r, T("s52")); b.press([[T("s52") + 1.5, T("s52") + 3.2]]);
  const hd = live(yt, 160, 520, 420, "held", (t) => (t < T("s52") + 1.5 ? "" : ms(Math.min(t, T("s52") + 3.2) - T("s52") - 1.5) + " ms"), "#ffb547"); show(hd, T("s52") + 1.4);
  const rule = tile(yt, 700, 220, 1100, 300, '<div style="font:800 44px var(--display)">Held for more than <span style="color:var(--amber)">1 second</span>?</div><div style="font:700 38px/1.6 var(--ui);margin-top:20px">&rarr; the walk light stays green <b style="color:#36e07a">twice as long</b></div>', "var(--amber)");
  hidden(rule); show(rule, W("s52", "held"));
  const kn = tile(yt, 700, 560, 1100, 260, '<div style="font:700 36px/1.6 var(--ui)">You know both pieces:<br>&#127915; the parking ticket &nbsp;+&nbsp; &#129530; a step that keeps its own time</div><div style="font:600 30px var(--ui);margin-top:14px;color:var(--muted)">One solution: lessons/09-mini-project-1 &rarr; slow_walker</div>', "var(--teal)");
  hidden(kn); show(kn, T("s53"));
}
const out = chapter("s54", null); title(out, "Three things you built today", "s54");
{
  [["state", "remembers the step", W("s54", "variable")], ["a start time", "for every step: nothing waits", W("s54", "start")], ["a parking ticket", "for button presses", W("s54", "ticket")]].forEach(([a, b, t0], i) => {
    const c = tile(out, 115 + i * 575, 230, 540, 340, `<div style="font:800 46px var(--mono);color:var(--teal)">${a}</div><div style="font:700 36px/1.5 var(--ui);margin-top:40px">${b}</div>`);
    hidden(c); show(c, t0); hide(c, T("s55") - 0.15, 0.25);
  });
  const next = tile(out, 210, 200, 1500, 420, '<div class="kicker">NEXT: EPISODE 10 &middot; MINI PROJECT 1</div><div style="font:800 62px var(--display);margin-top:26px">A reflex game</div><div style="font:600 36px var(--ui);margin-top:20px;color:var(--muted)">On the same circuit, with a high score that survives unplugging.</div><div style="font-size:90px;margin-top:20px">⚡🏆</div>');
  hidden(next); show(next, T("s55"));
  note(out, "How long does your crossing's green last? Tell me in the comments.", W("s55", "comments") - 0.6, 690);
  note(out, "github.com/emjnbulut/esp32-from-zero &rarr; lessons/09-mini-project-1", W("s55", "comments") - 0.6, 820);
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 }); TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}
window.__seek(0);
window.__ready = true;
