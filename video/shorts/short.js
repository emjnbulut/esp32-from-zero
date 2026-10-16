/* Shorts overlay: everything is a pure function of time t.
 * __DATA = { schedule: {duration, segments: {id: {start, end, words: [{w, t}]}}},
 *            segs: [{id, chip, headline}], panel: {x, y, w, h}, cta: {title, sub}, lang } */
const D = window.__DATA;
const $ = (s) => document.querySelector(s);
const P = D.panel;
for (const [k, v] of Object.entries({ x: P.x, y: P.y, width: P.w, height: P.h })) $("#holeRect").setAttribute(k, v);
Object.assign($("#frame").style, { left: P.x - 5 + "px", top: P.y - 5 + "px", width: P.w + 10 + "px", height: P.h + 10 + "px" });
document.documentElement.lang = D.lang || "en";

const segs = D.segs.map((s) => Object.assign({}, s, D.schedule.segments[s.id]));
const ease = (x) => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);

/* caption groups: a few words at a time, each word knows when it is spoken */
const groups = [];
for (const s of segs) {
  let g = null;
  s.words.forEach((w, i) => {
    const len = g ? g.words.reduce((a, x) => a + x.w.length + 1, 0) : 0;
    if (!g || g.words.length >= 4 || len + w.w.length > 22 || /[.!?,:]$/.test(g.words[g.words.length - 1].w)) {
      g = { words: [], start: w.t };
      groups.push(g);
    }
    g.words.push(w);
  });
}
groups.forEach((g, i) => { g.end = i + 1 < groups.length ? groups[i + 1].start : D.schedule.duration; });
const segOf = (t) => { let cur = segs[0]; for (const s of segs) if (t >= s.start - 0.15) cur = s; return cur; };

let last = {};
window.__seek = (t) => {
  // progress bar
  $("#prog").style.width = (1080 * Math.min(1, t / D.schedule.duration)).toFixed(1) + "px";
  // chip + headline with a quick slide-in whenever the segment changes
  const s = segOf(t);
  if (last.seg !== s.id) { $("#chip span").textContent = s.chip; $("#head").textContent = s.headline; last.seg = s.id; }
  const k = ease((t - (s.start - 0.15)) / 0.3);
  $("#head").style.transform = `translateY(${(1 - k) * 40}px)`;
  $("#head").style.opacity = k;
  $("#chip").style.opacity = k;
  // karaoke caption
  const g = groups.find((g) => t >= g.start - 0.05 && t < g.end) || null;
  if (g) {
    const html = g.words.map((w, i) => {
      const next = g.words[i + 1] ? g.words[i + 1].t : g.end;
      return `<span class="w${t >= w.t && t < next ? " on" : ""}">${w.w}</span>`;
    }).join("");
    if (last.cap !== html) { $("#cap").innerHTML = html; last.cap = html; }
    const p = ease((t - g.start + 0.05) / 0.12);
    $("#cap").style.transform = `scale(${0.92 + 0.08 * p})`;
    $("#cap").style.opacity = 1;
  } else $("#cap").style.opacity = 0;
  // call to action during the last segment, with a bouncing arrow
  const ls = segs[segs.length - 1];
  const c = ease((t - ls.start) / 0.4);
  $("#cta").style.opacity = c;
  $("#cta span").textContent = D.cta.title;
  $("#cta svg").style.transform = `translateY(${Math.abs(Math.sin(t * 5)) * 14}px)`;
};
window.__seek(0);
window.__ready = true;
