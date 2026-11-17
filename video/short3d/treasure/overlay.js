/* Treasure Short overlay (transparent 1080x1920): word-by-word captions, the detector ruler, the live code card,
 * "TREASURE FOUND!" + confetti, CTA. Everything is a function of t, from the same story as the 3D render.
 * __DATA = { schedule: { duration }, sched: build/schedule.json, info: build/scene_info.json }
 */
import { makeStory } from "./story.mjs";

const D = window.__DATA;
const st = makeStory(D.sched, D.info);
const { L } = st;
const $ = (id) => document.getElementById(id);
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const fade = (t, a, b, d = 0.25) => Math.min(smooth((t - a) / d), 1 - smooth((t - (b - d)) / d));

/* ---- caption groups: up to 3 words, a group also ends at punctuation ---- */
const groups = [];
for (const ln of D.sched.lines) {
  if (ln.id === "l08") continue; // "Treasure found!" gets its own big title
  const toks = ln.text.split(/\s+/).filter((w) => /[\w]/.test(w));
  let g = [];
  const SOFT = /^(a|an|the|to|my|and|this|of|from|with|is|it|into|that|than|on|in|for|can|you)$/i;
  toks.forEach((tok, i) => {
    const text = tok.replace(/[.,]+$/, "");
    if (g.length >= 3 || (g.length >= 2 && SOFT.test(text))) { groups.push({ words: g, line: ln }); g = []; }
    g.push({ text, t: ln.words[i] ? ln.words[i].t : ln.t1 });
    if (/[.,!?…]$/.test(tok)) { groups.push({ words: g, line: ln }); g = []; }
  });
  if (g.length) groups.push({ words: g, line: ln });
}
groups.forEach((g, i) => {
  const next = groups[i + 1];
  g.t0 = g.words[0].t - 0.05;
  g.t1 = next && next.line === g.line ? next.words[0].t - 0.05 : g.line.t1 + 0.2;
});

/* ---- confetti (seeded) ---- */
let seed = 7;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
const COLORS = ["#ffb547", "#19c3b4", "#ff5d6c", "#4ade80", "#7aa7ff", "#ffd25e", "#c48bff"];
const conf = Array.from({ length: 80 }, () => {
  const e = document.createElement("div");
  e.className = "conf";
  e.style.background = COLORS[Math.floor(rnd() * COLORS.length)];
  $("confetti").appendChild(e);
  return { e, x: 60 + rnd() * 960, vx: (rnd() - 0.5) * 260, vy: -900 - rnd() * 700, rot: rnd() * 360, vr: (rnd() - 0.5) * 900, d: rnd() * 0.25 };
});

const heatColor = (h) => { const k = h / 255; return `rgb(${Math.round(59 + (255 - 59) * k)},${Math.round(111 - 34 * k)},${Math.round(224 - 147 * k)})`; };

function render(t) {
  const s = st.state(t);
  const T = s.T;
  // captions
  const g = groups.find((x) => t >= x.t0 && t < x.t1);
  const cap = $("cap");
  if (g) {
    const key = groups.indexOf(g);
    if (cap.dataset.k !== String(key)) { cap.innerHTML = g.words.map((w) => `<span>${w.text}</span> `).join(""); cap.dataset.k = key; }
    [...cap.children].forEach((sp, i) => {
      const w = g.words[i], nxt = g.words[i + 1];
      sp.className = t >= w.t ? (nxt && t >= nxt.t ? "done" : "now") : "";
    });
    cap.style.opacity = t >= s.T.party - 0.02 && t < L.l09.t0 - 0.2 ? 0 : 1;
  } else cap.style.opacity = 0;

  // ruler: the knob position 0..99, coloured by heat; the treasure only shows when found
  const rulerOn = fade(t, 0.3, L.l09.t0 - 0.1, 0.3) + fade(t, L.l12.t0, st.DUR + 1, 0.4);
  $("ruler").style.opacity = Math.min(1, rulerOn);
  const c = heatColor(s.heat);
  $("ptr").style.left = (s.number / 99) * 100 + "%";
  $("ptr").textContent = s.number;
  $("ptr").style.background = c;
  $("ptr").style.borderTopColor = c;
  $("fill").style.width = (s.number / 99) * 100 + "%";
  $("fill").style.background = c;
  let chestA = 0, chestPos = 63, chestS = 1;
  if (t >= T.party && t < L.l09.t0) { chestA = smooth((t - T.party) / 0.2); chestS = 1 + 0.4 * (1 - smooth((t - T.party) / 0.35)); }
  if (t >= L.l12.t0) {
    const hop0 = st.W("l12", "treasure"), hop1 = st.W("l12", "somewhere"), end = L.l12.t1;
    chestA = smooth((t - L.l12.t0) / 0.3) * (1 - smooth((t - hop1 - 0.4) / 0.6));
    const k = smooth((t - hop0) / (hop1 - hop0));
    chestPos = 63 + (37 - 63) * k;
    chestS = 1 + 0.25 * Math.sin(Math.PI * k);
    if (t > end + 0.5) chestA = 0;
  }
  $("chest").style.opacity = chestA;
  $("chest").style.left = (chestPos / 99) * 100 + "%";
  $("chest").style.transform = `translate(-50%, ${-60 * Math.sin(Math.PI * smooth((t - st.W("l12", "treasure")) / (st.W("l12", "somewhere") - st.W("l12", "treasure"))))}px) scale(${chestS})`;

  // live code card (how it works)
  const codeOn = fade(t, L.l09.t0 + 0.2, L.l12.t0 - 0.1, 0.35);
  $("code").style.opacity = codeOn;
  $("code").style.transform = `translateY(${(1 - smooth((t - L.l09.t0 - 0.2) / 0.4)) * -30}px)`;
  const hl = t < L.l10.t0 ? [1] : t < L.l11.t0 ? [2] : t < st.W("l11", "speed", -0.3) ? [3, 4] : [5];
  for (let i = 1; i <= 5; i++) $("c" + i).classList.toggle("on", hl.includes(i));
  $("vd").textContent = `// ${s.distance}`;
  $("vh").textContent = `// ${s.heat}`;

  // treasure found
  const fk = fade(t, T.party, L.l09.t0 - 0.2, 0.2);
  $("found").style.opacity = fk;
  $("found").style.transform = `scale(${0.6 + 0.4 * smooth((t - T.party) / 0.22) + 0.06 * Math.sin((t - T.party) * 9) * fk})`;
  const ct = t - T.party;
  for (const p of conf) {
    const u = ct - p.d;
    if (u < 0 || u > 2.6) { p.e.style.opacity = 0; continue; }
    const x = p.x + p.vx * u, y = 1250 + p.vy * u + 900 * u * u;
    Object.assign(p.e.style, { opacity: Math.min(1, (2.6 - u) * 2), transform: `translate(${x}px, ${y}px) rotate(${p.rot + p.vr * u}deg)` });
  }

  // call to action
  $("cta").style.opacity = fade(t, L.l13.t0 + 0.3, st.DUR + 1, 0.4);
}

window.__seek = render;
window.__duration = () => st.DUR;
await document.fonts.ready;
render(0);
window.__ready = true;
