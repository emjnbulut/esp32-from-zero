/* Channel trailer overlay: a pure function of time t.
 * __DATA = { schedule: {duration, segments: {id: {start, end, words: [t...]}}}, segs: [{id, kicker, headline, card}] } */
const D = window.__DATA;
const $ = (s) => document.querySelector(s);
const ease = (x) => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);
const segs = D.segs.map((s) => Object.assign({}, s, D.schedule.segments[s.id]));
const logo = (w) => LOGOS.A().replace("<svg ", `<svg width="${w}" height="${w}" `);
$("#logo").innerHTML = `${logo(48)}<span>Pin by Pin Lab</span>`;

// "what you'll build": topics pop in one by one while they are named
const TOPICS = [["🔘", "Buttons"], ["⏱️", "Timers"], ["🌗", "Dimming"], ["🌈", "RGB colors"], ["🌡️", "Sensors"], ["🖥️", "OLED screen"], ["📶", "WiFi"], ["📱", "Web page"]];
const tc = segs.find((s) => s.card === "topics");
const topicEls = TOPICS.map(([i, n], k) => {
  const e = document.createElement("div");
  e.className = "topic";
  e.style.left = 140 + (k % 4) * 420 + "px";
  e.style.top = 250 + Math.floor(k / 4) * 250 + "px";
  e.innerHTML = `<div class="i">${i}</div><div class="n">${n}</div>`;
  $("#topics").appendChild(e);
  return e;
});
const topicTimes = tc ? TOPICS.map((_, k) => tc.start + 0.15 + k * Math.max(0.25, (tc.end - tc.start - 0.6) / TOPICS.length)) : [];
// end card
$("#end").insertAdjacentHTML("beforeend", `<div class="abs" style="left:0;width:1920px;top:180px;text-align:center">${logo(220)}
  <div style="font:800 92px var(--display);letter-spacing:-2px;margin-top:20px">Pin by Pin Lab</div>
  <div class="ep1" style="margin-top:10px">ESP32 From Zero · all the code on GitHub</div>
  <div style="margin-top:46px"><span class="sub"><svg width="48" height="34" viewBox="0 0 48 34"><rect width="48" height="34" rx="9" fill="#fff"/><path d="M19 9 L32 17 L19 25 Z" fill="#ff3b3b"/></svg>Subscribe</span></div>
  <div class="ep1" style="margin-top:34px">Start here: <b style="color:#fff">Episode 1 — Setting Up Your Computer</b></div></div>`);

const segOf = (t) => { let cur = segs[0]; for (const s of segs) if (t >= s.start - 0.2) cur = s; return cur; };
let last = null;
window.__seek = (t) => {
  const s = segOf(t);
  const card = s.card || null;
  for (const id of ["topics", "end"]) {
    const c = segs.find((x) => x.card === id);
    $("#" + id).style.opacity = c && t >= c.start - 0.35 ? ease((t - (c.start - 0.35)) / 0.35) : 0;
  }
  topicEls.forEach((e, k) => { const p = ease((t - topicTimes[k]) / 0.3); e.style.opacity = p; e.style.transform = `translateY(${(1 - p) * 30}px) scale(${0.94 + 0.06 * p})`; });
  // lower third on the footage segments
  if (last !== s.id) { $("#lt .k").textContent = s.kicker; $("#lt .h").textContent = s.headline; last = s.id; }
  const k = card === "end" ? 0 : ease((t - (s.start - 0.2)) / 0.4);
  const top = card === "topics";
  Object.assign($("#lt").style, { opacity: k, transform: `translateY(${(1 - k) * 30}px)`, bottom: top ? "auto" : "90px", top: top ? "90px" : "auto" });
  $("#shade").style.opacity = card ? 0 : 1;
  $("#bar").style.opacity = card ? 0 : k;
  $("#bar").style.width = (k * 260).toFixed(1) + "px";
  $("#logo").style.opacity = card === "end" ? 0 : 0.9;
};
window.__seek(0);
window.__ready = true;
