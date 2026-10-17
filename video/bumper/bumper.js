/* Channel intro / outro. Everything is a pure function of time t.
 * __DATA = { kind: "intro" | "outro", schedule: { duration } } */
const D = window.__DATA || { kind: "intro", schedule: { duration: 3.5 } };
const C = { teal: "#19c3b4", amber: "#ffb547", panel: "#111c30", line: "#22304d", off: "#1c2a44" };
const stage = document.getElementById("stage");
const clamp = (x) => Math.min(1, Math.max(0, x));
const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
const span = (t, a, b) => ease((t - a) / (b - a));

// the logo chip (same geometry as brand/logos.js logo A), pins lit one by one
const PINS = [];
for (let i = 0; i < 4; i++) PINS.push({ x: 112, y: 176 + i * 52 });          // left, top -> bottom
for (let i = 3; i >= 0; i--) PINS.push({ x: 352, y: 176 + i * 52 });         // right, bottom -> top
const P_PATH = "M222 330 V182 h52 a40 40 0 0 1 0 80 h-52";
function chipSVG(size) {
  return `<svg viewBox="0 0 512 512" width="${size}" height="${size}">
    ${PINS.map((p, i) => `<rect id="pin${i}" x="${p.x}" y="${p.y}" width="48" height="22" rx="5" fill="${C.off}"/>`).join("")}
    <rect x="152" y="140" width="208" height="232" rx="22" fill="${C.panel}" stroke="${C.line}" stroke-width="6"/>
    <circle cx="180" cy="168" r="9" fill="${C.line}"/>
    <path id="pp" d="${P_PATH}" fill="none" stroke="${C.amber}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"
      stroke-dasharray="520" stroke-dashoffset="520"/>
  </svg>`;
}
const $ = (s) => document.querySelector(s);

if (D.kind === "intro") {
  stage.innerHTML = `<div id="chip" style="position:absolute;left:295px;top:350px">${chipSVG(380)}</div>
    <div class="word" id="wm" style="left:705px;top:410px;font-size:150px">Pin by Pin <b>Lab</b></div>
    <div class="tag" id="tg" style="left:713px;top:600px">Electronics &amp; embedded C — one pin at a time</div>`;
} else {
  stage.innerHTML = `<div id="chip" style="position:absolute;left:150px;top:150px">${chipSVG(200)}</div>
    <div class="word" id="wm" style="left:370px;top:185px;font-size:78px">Pin by Pin <b>Lab</b></div>
    <div class="word" id="ty" style="left:160px;top:380px;font-size:96px">Thanks for watching!</div>
    <div class="tag" id="tg" style="left:164px;top:520px">See you in the next episode.</div>
    <div class="slot" id="sub" style="left:250px;top:660px;width:240px;height:240px;border-radius:50%">SUBSCRIBE</div>
    <div class="slot" id="v1" style="left:1060px;top:180px;width:700px;height:394px">NEXT EPISODE</div>
    <div class="slot" id="v2" style="left:1060px;top:640px;width:700px;height:300px">MORE VIDEOS</div>
    <svg id="rail" width="1920" height="60" style="left:0;top:1000px"></svg>`;
  // a row of header pins along the bottom that light up as the end screen runs
  $("#rail").innerHTML = Array.from({ length: 36 }, (_, i) =>
    `<rect id="r${i}" x="${60 + i * 50}" y="20" width="22" height="22" rx="4" fill="none" stroke="${C.line}" stroke-width="4"/>`).join("");
}

window.__seek = (t) => {
  const T = D.schedule.duration;
  if (D.kind === "intro") {
    // 0.0-0.5 chip fades in; 0.35-1.55 pins light one by one; 1.45-2.1 the P is drawn;
    // 1.9-2.6 wordmark + tagline slide in; last 0.45 s fades to black
    const c = span(t, 0, 0.5);
    $("#chip").style.opacity = c;
    // the chip starts centred on screen and slides left to make room for the wordmark
    $("#chip").style.transform = `translateX(${475 * (1 - span(t, 1.85, 2.45))}px) scale(${0.85 + 0.15 * c})`;
    PINS.forEach((_, i) => $(`#pin${i}`).setAttribute("fill", t >= 0.35 + i * 0.15 ? C.teal : C.off));
    $("#pp").setAttribute("stroke-dashoffset", 520 * (1 - span(t, 1.45, 2.1)));
    const w = span(t, 1.9, 2.5), g = span(t, 2.1, 2.7);
    $("#wm").style.opacity = w; $("#wm").style.transform = `translateX(${(1 - w) * 40}px)`;
    $("#tg").style.opacity = g; $("#tg").style.transform = `translateX(${(1 - g) * 40}px)`;
    $("#fade").style.opacity = span(t, T - 0.45, T);
  } else {
    const a = span(t, 0, 0.6);
    $("#fade").style.opacity = Math.max(1 - span(t, 0, 0.5), span(t, T - 1.0, T));
    PINS.forEach((_, i) => $(`#pin${i}`).setAttribute("fill", C.teal));
    $("#pp").setAttribute("stroke-dashoffset", 0);
    for (const [id, d] of [["chip", 0], ["wm", 0.1], ["ty", 0.3], ["tg", 0.5], ["sub", 0.7], ["v1", 0.8], ["v2", 0.9]]) {
      const k = span(t, d, d + 0.6);
      $("#" + id).style.opacity = k * a;
      $("#" + id).style.transform = `translateY(${(1 - k) * 24}px)`;
    }
    for (let i = 0; i < 36; i++) {
      const on = t >= 1 + i * (T - 2) / 36;
      const r = $("#r" + i);
      r.setAttribute("fill", on ? C.teal : "none");
      r.setAttribute("stroke", on ? C.teal : C.line);
    }
  }
};
window.__seek(0);
window.__ready = true;
