/* ESP32 From Zero - timeline engine.
 * Everything visible is a pure function of time t: GSAP tweens on a paused
 * timeline plus "dyn" functions that redraw computed state (typing, logs...).
 * The renderer calls window.__seek(t) for each frame.
 */
const D = window.__DATA || { schedule: { duration: 10, segments: {} } };
const tl = gsap.timeline({ paused: true });
const dyns = [];
const clips = [];
const $ = (sel, root = document) => root.querySelector(sel);

function el(tag, cls, html, parent) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html != null) e.innerHTML = html;
  if (parent) parent.appendChild(e);
  return e;
}
/** element box in stage/desktop coords (valid at build time: camera is identity then) */
function rect(e) {
  const r = e.getBoundingClientRect();
  return { x: r.left, y: r.top, w: r.width, h: r.height, cx: r.left + r.width / 2, cy: r.top + r.height / 2 };
}
function css(e, styles) { Object.assign(e.style, styles); return e; }
function box(parent, x, y, w, h, cls = "", html = "") {
  return css(el("div", "abs " + cls, html, parent), { left: x + "px", top: y + "px", width: w + "px", height: h + "px" });
}

/* ---- schedule helpers ---- */
function seg(id) {
  const s = D.schedule.segments[id];
  if (!s) throw new Error("unknown segment " + id);
  return s;
}
const norm = (w) => w.toLowerCase().replace(/[^a-z0-9]/g, "");
/** absolute time of a word in a segment: W("s08", "download") or W("s08", 5) */
function W(id, word, nth = 1) {
  const s = seg(id);
  if (typeof word === "number") return s.start + (s.words[word] ? s.words[word].t : 0);
  const key = norm(word);
  for (const w of s.words) if (norm(w.w) === key && --nth === 0) return s.start + w.t;
  console.warn("word not found", id, word);
  return s.start;
}
const S0 = (id) => seg(id).start;
const S1 = (id) => seg(id).end;

/* ---- tween helpers (absolute times) ---- */
function TO(target, t, dur, vars) { tl.to(target, Object.assign({ duration: dur, ease: "power2.inOut" }, vars), t); }
function SET(target, t, vars) { tl.set(target, vars, t); }
function show(target, t, dur = 0.4) { TO(target, t, dur, { opacity: 1, ease: "power1.out" }); }
function hide(target, t, dur = 0.4) { TO(target, t, dur, { opacity: 0, ease: "power1.in" }); }
function pop(target, t, dur = 0.35) {
  SET(target, t - 0.001, { scale: 0.96, opacity: 0 });
  TO(target, t, dur, { scale: 1, opacity: 1, ease: "back.out(1.6)" });
}
function dyn(fn) { dyns.push(fn); }
/** discrete state over time: list = [[t, value], ...] sorted; value before first t = list[0][1] */
function stateAt(list, t) { let v = list[0][1]; for (const [ts, s] of list) if (t >= ts) v = s; return v; }
function textAt(e, list) {
  dyn((t) => { const v = stateAt(list, t); if (e.__v !== v) { e.innerHTML = v; e.__v = v; } });
}
function styleAt(e, prop, list) {
  dyn((t) => { const v = stateAt(list, t); if (e.style[prop] !== v) e.style[prop] = v; });
}

/* deterministic pseudo random */
function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

/** human-like typing schedule: returns array of char times starting at t0 */
function typingTimes(text, t0, cps = 11, seed = 7) {
  const r = rng(seed), times = [];
  let t = t0;
  for (let i = 0; i < text.length; i++) {
    times.push(t);
    const c = text[i];
    let d = (1 / cps) * (0.6 + r() * 0.8);
    if (c === "\n") d += 0.25;
    else if (c === " " && text[i + 1] === " ") d = 0.012; // indentation is fast (auto-indent feel)
    else if (/[;{}()]/.test(c)) d += 0.06;
    t += d;
  }
  times.end = t;
  return times;
}
function countAt(times, t) {
  let lo = 0, hi = times.length;
  while (lo < hi) { const m = (lo + hi) >> 1; if (times[m] <= t) lo = m + 1; else hi = m; }
  return lo;
}

/* ---- C syntax highlighting ---- */
const KW = new Set("int void char float double long unsigned bool const static volatile if else while for return true false".split(" "));
const FN = new Set("setup loop Serial begin println print printf delay pinMode digitalWrite digitalRead analogRead main".split(" "));
function tokenize(src) {
  const out = []; const re = /(\/\/[^\n]*)|("(?:[^"\\]|\\.)*"?)|(#\w+)|(\b\d+\b)|([A-Za-z_]\w*)|(\s+)|(.)/g;
  let m;
  while ((m = re.exec(src))) {
    const [s] = m;
    let c = "";
    if (m[1]) c = "tk-com"; else if (m[2]) c = "tk-str"; else if (m[3]) c = "tk-pre"; else if (m[4]) c = "tk-num";
    else if (m[5]) c = KW.has(s) ? "tk-kw" : FN.has(s) ? "tk-fn" : "tk-id";
    out.push([s, c]);
  }
  return out;
}
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
/** highlighted HTML lines of the first n chars of src */
function hlLines(src, n = src.length) {
  const toks = tokenize(src.slice(0, n));
  const lines = [""];
  for (const [s, c] of toks) {
    const parts = s.split("\n");
    parts.forEach((p, i) => {
      if (i > 0) lines.push("");
      if (p) lines[lines.length - 1] += c ? `<span class="${c}">${esc(p)}</span>` : esc(p);
    });
  }
  return lines;
}

/* ---- cursor, clicks and camera (desktop space) ---- */
let cursorEl, camEl;
const cur = { x: 960, y: 600 };
function initCursor(parent) {
  cursorEl = el("div", "abs", `<svg width="26" height="36" viewBox="0 0 13 18"><path d="M1 1v14.5l3.6-3.4 2.4 5.2 2.4-1.1-2.4-5H12z" fill="#fff" stroke="#000" stroke-width="1.1" stroke-linejoin="round"/></svg>`, parent);
  css(cursorEl, { left: 0, top: 0, zIndex: 100, filter: "drop-shadow(0 2px 3px rgba(0,0,0,.5))" });
  gsap.set(cursorEl, { x: cur.x, y: cur.y });
  return cursorEl;
}
function move(x, y, t, dur = 0.7) {
  TO(cursorEl, t, dur, { x, y, ease: "power3.inOut" });
  cur.x = x; cur.y = y;
}
/** move so the click lands exactly at time t */
function clickAt(x, y, t, dur = 0.7, parent) {
  move(x, y, t - dur - 0.08, dur);
  const r = el("div", "abs", "", parent || cursorEl.parentNode);
  css(r, { left: x - 22 + "px", top: y - 22 + "px", width: "44px", height: "44px", borderRadius: "50%",
    border: "3px solid rgba(255,190,80,.95)", background: "rgba(255,190,80,.25)", opacity: 0, zIndex: 99 });
  SET(r, t, { opacity: 1, scale: 0.3 });
  TO(r, t, 0.45, { scale: 1.25, opacity: 0, ease: "power2.out" });
  TO(cursorEl, t - 0.06, 0.06, { scale: 0.85, ease: "none" });
  TO(cursorEl, t + 0.02, 0.1, { scale: 1, ease: "none" });
}
function initCamera(e) { camEl = e; gsap.set(camEl, { x: 0, y: 0, scale: 1 }); }
/** zoom so desktop point (x,y) is centred at scale s (clamped to edges) */
function cam(t, dur, x, y, s) {
  let tx = 960 - s * x, ty = 540 - s * y;
  tx = Math.min(0, Math.max(1920 - 1920 * s, tx));
  ty = Math.min(0, Math.max(1080 - 1080 * s, ty));
  TO(camEl, t, dur, { x: tx, y: ty, scale: s, ease: "power2.inOut" });
}
const camReset = (t, dur = 1) => cam(t, dur, 960, 540, 1);

/* ---- callouts ---- */
function callout(parent, text, x, y, t0, t1, opts = {}) {
  const c = el("div", "callout", text, parent);
  css(c, { left: x + "px", top: y + "px" });
  if (opts.style) css(c, opts.style);
  pop(c, t0); if (t1) hide(c, t1, 0.3);
  return c;
}
function ring(parent, x, y, w, h, t0, t1) {
  const r = box(parent, x, y, w, h, "ring");
  pop(r, t0); if (t1) hide(r, t1, 0.3);
  return r;
}

/* ---- clips from the creator's camera ---- */
function clipFrame(parent, id, x, y, w, h, t0, t1, desc) {
  const f = box(parent, x, y, w, h, "clipframe",
    `<div class="ph"><div class="big">📹 ${id}</div><div class="small">${desc || ""}</div></div>`);
  const tag = box(parent, x + 24, y - 18, 0, 0, "cliptag", "ON MY DESK");
  css(tag, { width: "auto", height: "auto" });
  pop(f, t0); show(tag, t0 + 0.2, 0.3);
  hide(f, t1, 0.35); hide(tag, t1, 0.35);
  clips.push({ id, x, y, w, h, t0: t0 + 0.35, t1 });
  return f;
}

/* ---- scene switching ---- */
function sceneIn(e, t, dur = 0.6) { TO(e, t, dur, { opacity: 1, ease: "power1.out" }); }
function sceneOut(e, t, dur = 0.6) { TO(e, t, dur, { opacity: 0, ease: "power1.in" }); }

/* ---- render hook ---- */
window.__seek = (t) => {
  tl.seek(t, false);
  for (const f of dyns) f(t);
};
window.__clips = clips;
window.__duration = () => D.schedule.duration;
