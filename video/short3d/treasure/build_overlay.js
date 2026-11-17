/* Overlay for the quick build montage: captions (same style as the main Short), part names as they snap in,
 * short GPIO tags at the pins while the wires zip in. __DATA = { schedule, sched, events, anchors } */
const D = window.__DATA;
const $ = (id) => document.getElementById(id);
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
for (const id of ["ruler", "code", "cta", "found"]) $(id).style.display = "none";

const SOFT = /^(a|an|the|to|my|and|this|of|from|with|is|it|into|that|than|on|in|for|can|you)$/i;
const groups = [];
for (const ln of D.sched.lines) {
  const toks = ln.text.split(/\s+/).filter((w) => /\w/.test(w));
  let g = [];
  toks.forEach((tok, i) => {
    const text = tok.replace(/[.,:]+$/, "");
    if (g.length >= 3 || (g.length >= 2 && SOFT.test(text))) { groups.push({ words: g, line: ln }); g = []; }
    g.push({ text, t: ln.words[i] ? ln.words[i].t : ln.t1 });
    if (/[.,:!?]$/.test(tok)) { groups.push({ words: g, line: ln }); g = []; }
  });
  if (g.length) groups.push({ words: g, line: ln });
}
groups.forEach((g, i) => {
  const next = groups[i + 1];
  g.t0 = g.words[0].t - 0.05;
  g.t1 = next && next.line === g.line ? next.words[0].t - 0.05 : g.line.t1 + 0.2;
});

const labels = D.events.labels.map((l) => {
  const e = document.createElement("div");
  e.className = "lbl" + (l.kind === "pin" ? " pin" : "");
  e.textContent = l.text;
  $("stage").appendChild(e);
  return { ...l, e };
});

function render(t) {
  const g = groups.find((x) => t >= x.t0 && t < x.t1);
  const cap = $("cap");
  if (g) {
    const key = groups.indexOf(g);
    if (cap.dataset.k !== String(key)) { cap.innerHTML = g.words.map((w) => `<span>${w.text}</span> `).join(""); cap.dataset.k = key; }
    [...cap.children].forEach((sp, i) => { const w = g.words[i], n = g.words[i + 1]; sp.className = t >= w.t ? (n && t >= n.t ? "done" : "now") : ""; });
    cap.style.opacity = 1;
  } else cap.style.opacity = 0;
  const f = Math.min(D.anchors.espTop.length - 1, Math.max(0, Math.round(t * D.anchors.fps)));
  for (const l of labels) {
    const a = Math.min(smooth((t - l.t0) / 0.12), 1 - smooth((t - (l.t1 - 0.2)) / 0.2));
    const p = D.anchors[l.key][f];
    const pop = 1 + 0.25 * (1 - smooth((t - l.t0) / 0.18));
    Object.assign(l.e.style, { opacity: a, left: Math.min(1000, Math.max(80, p[0])) + "px", top: Math.max(120, p[1] - (l.kind === "pin" ? 26 : 40)) + "px",
      transform: `translate(-50%, -100%) scale(${pop})` });
  }
}
window.__seek = render;
await document.fonts.ready;
render(0);
window.__ready = true;
