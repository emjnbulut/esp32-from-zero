/* Secret knock lock - vertical 3D Short (1080x1920), three.js kit + crisp HTML overlay in one page.
 * __DATA: { lang, sched } (sched = build/<lang>_schedule.json from voice.py). Timing: story.mjs. */
import { makeKit, makeTag, clamp01 } from "../../engine3d/kit.js";
import { buildP1 } from "../../engine3d/circuit_p1.js";
import { makeStory } from "./story.mjs";

const D = window.__DATA || {};
const LANG = D.lang || "en";
const S = makeStory(D.sched);
const K = makeKit({ pixelRatio: 2, w: 1080, h: 1920, persp: true, fov: 30 });
const { esp, red, yel, grn, btn, rgb, pot } = buildP1(K, ["D23", "D22", "D18", "TX2", "D25", "D26", "D27"]);

const TXT = {
  en: { chip: "ESP32 PROJECT", hook: "Secret<br><b>knock lock</b>", locked: "LOCKED", open: "OPEN", wrong: "WRONG!",
    short: "SHORT", long: "LONG", mont: "Same parts as<br><b style=\"color:var(--amber)\">Episode 9</b>", montS: "no new wires · just new code",
    ticket: "THE PARKING TICKET", stepK: "ONE VARIABLE", forgetK: "3 S OF QUIET", cta: "Build it with<br><b>Episode 9</b>", ctaS: "Which rhythm would you pick? 💬",
    redTag: "LOCKED", btnTag: "KNOCK HERE" },
  tr: { chip: "ESP32 PROJESİ", hook: "Gizli<br><b>ritim kilidi</b>", locked: "KİLİTLİ", open: "AÇIK", wrong: "YANLIŞ!",
    short: "KISA", long: "UZUN", mont: "Parçalar<br><b style=\"color:var(--amber)\">9. bölümle aynı</b>", montS: "yeni kablo yok · sadece yeni kod",
    ticket: "OTOPARK BİLETİ", stepK: "TEK DEĞİŞKEN", forgetK: "3 SN SESSİZLİK", cta: "<b>9. bölümle</b><br>kendin kur", ctaS: "Sen hangi ritmi seçerdin? 💬",
    redTag: "KİLİTLİ", btnTag: "BURAYA VUR" },
}[LANG];

/* ---------------- overlay ---------------- */
const ui = document.getElementById("ui");
const E = (cls, html) => { const e = el("div", cls, html, ui); e.style.opacity = 0; return e; };
const chip = E("chip", TXT.chip), hook = E("hook", TXT.hook);
show(chip, 0.15, 0.3); show(hook, 0.25, 0.35); hide(hook, S.t0("l02") + 0.2, 0.3); hide(chip, S.t0("l02") + 0.2, 0.3);

const meter = E("meter", `<div class="lk">🔒</div><div class="slot"></div><div class="slot"></div><div class="slot long"></div><div class="lab"></div>`);
const slots = [...meter.querySelectorAll(".slot")], lk = meter.querySelector(".lk"), mlab = meter.querySelector(".lab");
const meterOn = [[S.t0("l02") + 0.3, S.MONT[0] - 0.1], [S.MONT[1], S.t0("l11") - 0.2]];
for (const [a, b] of meterOn) { show(meter, a, 0.3); hide(meter, b, 0.3); }

const capEl = E("cap", "");
show(capEl, 0.2, 0.2);
// captions: chunks of the written text, each word timed to the spoken word with the same relative position
const CAP = [];
for (const ln of S.L ? Object.values(S.L) : []) {
  const shown = (ln.show || ln.text).split(/\s+/).filter(Boolean);
  const n = shown.length, m = ln.words.length;
  const wt = shown.map((_, j) => ln.words[Math.min(m - 1, Math.round((j * m) / n))].t);
  let chunk = [];
  const flush = () => { if (chunk.length) CAP.push({ words: chunk, t0: chunk[0].t, t1: null }); chunk = []; };
  shown.forEach((w, j) => {
    chunk.push({ w, t: wt[j] });
    const len = chunk.map((c) => c.w).join(" ").length;
    if (len >= 16 || /[.!?,:]$/.test(w) || chunk.length >= 4) flush();
  });
  flush();
  CAP[CAP.length - 1].lineEnd = ln.t1;
}
CAP.forEach((c, i) => { c.t1 = c.lineEnd != null ? c.lineEnd + 0.15 : CAP[i + 1].t0; });
let capKey = "";
dyn((t) => {
  const c = CAP.find((x) => t >= x.t0 - 0.05 && t < x.t1);
  const key = c ? CAP.indexOf(c) + ":" + c.words.filter((w) => t >= w.t).length : "";
  if (key === capKey) return;
  capKey = key;
  capEl.innerHTML = c ? c.words.map((w, i) => {
    const next = c.words[i + 1];
    const cls = t >= w.t && (!next || t < next.t) ? "now" : t >= w.t ? "done" : "";
    return `<span class="w ${cls}">${w.w}</span>`;
  }).join(" ") : "";
});

// code cards (l08 ticket, l09 step counter, l10 forget)
const card1 = E("code", `<span class="k">${TXT.ticket}</span>pressStart = now;\nheld = now - pressStart;\n<span class="f">if</span> (held &lt; <span class="n">250</span>) → ${TXT.short}`);
const card2 = E("code", `<span class="k">${TXT.stepK}</span><span class="f">int</span> step = <span class="big">0</span>;\nstep = step + <span class="n">1</span>;`);
const card3 = E("code", `<span class="k">${TXT.forgetK}</span><span class="f">if</span> (now - lastKnock &gt;= <span class="n">3000</span>)\n  step = <span class="n">0</span>;`);
const stepNum = card2.querySelector(".big");
show(card1, S.t0("l08") + 0.1, 0.3); hide(card1, S.t0("l09") - 0.1, 0.25);
show(card2, S.t0("l09"), 0.3); hide(card2, S.c1 - 0.25, 0.25);
show(card3, S.c1 - 0.15, 0.3); hide(card3, Math.min(S.FORGET_AT + 0.7, S.t0("l11") - 0.3), 0.25);
const count = E("count", "3");
show(count, S.c1 + 0.2, 0.2); hide(count, Math.min(S.FORGET_AT + 0.5, S.t0("l11") - 0.3), 0.25);

const mont = E("mont", `${TXT.mont}<small>${TXT.montS}</small>`);
show(mont, S.MONT[0] + 0.2, 0.35); hide(mont, S.MONT[1] - 0.2, 0.3);
const cta = E("cta", `<div class="a">${TXT.cta}</div><div class="s">${TXT.ctaS}</div>`);
show(cta, S.t0("l11") - 0.1, 0.35);

// 3D-anchored tags
const tags = [];
function tag(html, p, t0, t1, o = {}) {
  const tg = makeTag(ui, html, (o.side && o.side !== "up" ? o.side : "") + " big3d " + (o.cls || ""));
  show(tg.el, t0, 0.25); if (t1 != null) hide(tg.el, t1, 0.25);
  tags.push({ tg, p, dy: o.dy || 0 });
  return tg;
}
tag(TXT.redTag, red.top, S.Wi("l02", 0) - 0.1, S.Wi("l02", 0) + 1.6, { cls: "act" });
tag(TXT.btnTag, btn.top, S.presses[0][0] - 0.9, S.presses[0][0] + 0.3, { cls: "act" });
// press timers: the held time of every press from l08 on
for (const [a, b] of S.presses) {
  if (a < S.t0("l08")) continue;
  const tg = tag("", btn.top, a, b + 1.0, { cls: "act" });
  dyn((t) => {
    if (t < a || t > b + 1.1) return;
    const ms = Math.round((Math.min(t, b) - a) * 1000);
    tg.el.textContent = t < b ? `${ms} ms` : `${ms} ms · ${ms >= 250 ? TXT.long : TXT.short}`;
  });
}

/* ---------------- montage: parts snap in during l07 ---------------- */
const esp32 = K.parts.find((p) => p.drop);
const wires = K.parts.filter((p) => p.kind === "wire");
const res = K.parts.filter((p) => p.kind === "resistor");
const others = K.parts.filter((p) => p !== esp32 && !wires.includes(p) && !res.includes(p));
const [m0, m1] = S.MONT, md = m1 - m0;
const plan = [[esp32, m0 + 0.05 * md, 0.5]];
others.forEach((p, i) => plan.push([p, m0 + (0.2 + (i / others.length) * 0.22) * md, 0.3]));
res.forEach((p, i) => plan.push([p, m0 + (0.42 + (i / res.length) * 0.15) * md, 0.25]));
wires.forEach((p, i) => plan.push([p, m0 + (0.57 + (i / wires.length) * 0.33) * md, 0.35]));
function montage(t) {
  if (t < m0 - 0.4 || t > m1 + 0.4) { for (const [p] of plan) p.reveal(1); return; }
  // just before the montage the board empties (quick fade out by shrinking), then everything snaps in again
  const k = (t - (m0 - 0.4)) / 0.4;
  for (const [p, a, d] of plan) p.reveal(t < m0 ? 1 - clamp01(k) : (t - a) / d);
}

/* ---------------- camera ---------------- */
const cam = (th, el, hh, p, dz = 0, dx = 0, dy = 0) => ({ th, el, hh, tx: p[0] + dx, ty: p[1] * 0.7 + dy, tz: p[2] + dz });
const C = K.centre;
const pairBR = C(btn.top, rgb.top), WIDE = [0, 10, -6];
const keys = [
  [0, cam(58, 26, 15, C(red.top, btn.top), 0, 2)],
  [S.t0("l02") - 0.3, cam(70, 30, 22, C(red.top, btn.top))],
  [S.Wi("l02", 1), cam(80, 34, 16, red.top)],
  [S.Wi("l02", -4), cam(80, 36, 17, red.top)],
  [S.t0("l03") - 0.2, cam(90, 45, 58, pairBR, 0, 4)],
  [S.OPEN_AT, cam(98, 47, 56, pairBR, 0, 4)],
  [S.OPEN_AT + 0.6, cam(104, 50, 66, C(rgb.top, grn.top), -4)],
  [S.t0("l05"), cam(112, 50, 64, C(rgb.top, grn.top), -4)],
  [S.t0("l05") + 0.7, cam(80, 44, 56, pairBR, 0, 4)],
  [S.MONT[0] - 0.2, cam(86, 45, 56, pairBR, 0, 4)],
  [S.MONT[0] + 0.3, cam(90, 58, 92, WIDE)],
  [S.MONT[1], cam(112, 54, 86, WIDE)],
  [S.t0("l08") + 0.3, cam(96, 46, 50, C(btn.top, yel.top), 0, 2)],
  [S.q3 - 0.3, cam(92, 47, 52, C(btn.top, yel.top), 0, 2)],
  [S.OPEN2 + 0.4, cam(100, 50, 66, C(rgb.top, grn.top), -4)],
  [S.c1 - 0.6, cam(124, 48, 62, C(rgb.top, grn.top), -4)],
  [S.c1 - 0.1, cam(86, 45, 56, pairBR, 0, 4)],
  [S.FORGET_AT + 0.4, cam(80, 44, 54, pairBR, 0, 4)],
  [S.t0("l11") + 0.2, cam(60, 34, 74, WIDE)],
  [S.DUR, cam(42, 30, 68, WIDE)],
];
keys.sort((a, b) => a[0] - b[0]);
const path = K.camPath(keys);

/* ---------------- per frame ---------------- */
dyn((t) => {
  montage(t);
  const L = S.lock(t);
  red.set(L.red); yel.set(L.yellow); grn.set(L.green); rgb.set(...L.rgb);
  const b = S.button(t); btn.set(b.p, b.pulse);
  // meter
  slots.forEach((s, i) => { s.className = "slot" + (i === 2 ? " long" : "") + (L.mode === "wrong" ? " bad" : L.mode === "party" || L.mode === "open" ? " ok" : i < L.step ? " on" : ""); });
  lk.textContent = L.mode === "party" || L.mode === "open" ? "🔓" : "🔒";
  mlab.textContent = L.mode === "wrong" ? TXT.wrong : L.mode === "party" || L.mode === "open" ? TXT.open : TXT.locked;
  mlab.style.color = L.mode === "wrong" ? "#ff6a6a" : L.mode === "party" || L.mode === "open" ? "#5dff8a" : "#c9d4e8";
  stepNum.textContent = String(L.mode === "party" || L.mode === "open" ? 3 : L.step);
  count.textContent = String(Math.max(1, Math.ceil(S.FORGET_AT - t)));
  if (t >= S.FORGET_AT) count.textContent = "0";
  K.placeCamera(path(t));
  for (const { tg, p, dy } of tags) tg.at(p, K.toScreen, dy);
  K.render();
});
window.__seek(0);
window.__ready = true;
