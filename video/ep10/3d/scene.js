/* Episode 10 - 3D clips (reflex game), replacing the creator's phone clips. Same circuit as episode 9
 * (engine3d/circuit_p1.js, connections listed in ep09/3d/scene.js). window.__DATA: { clip, ev }, ev from make.mjs.
 *   C0  cold open: start, red, yellow, green, a fast press -> color LED green; then the record
 *   C4  "here it is": a fast round with every part labelled (213 ms -> green)
 *   C1  a slow press about a second after green (1046 ms -> red)
 *   C2  the unplug test: cable out, everything dark, cable in, the board boots again
 *   S0 / S2 / S4 / S5  Short clips (square crop [420, 0, 1080, 1080]); S5 = the false-start challenge solution
 * Game rules = reflex_game.ino / challenge_false_start.ino: red 1 s, yellow waitTime (knob 1-4 s), green until the
 * press; result color 3 s (green < 250 ms, orange < 500 ms, else red), then dim blue = "press to start".
 * False start (press in red/yellow): red flashes every 150 ms for 2 s, nothing saved. */
import { makeKit, makeTag, COL, clamp01 } from "../../engine3d/kit.js";
import { buildP1 } from "../../engine3d/circuit_p1.js";

const D = window.__DATA || {};
const CLIP = D.clip || "C4";
const EV = D.ev || {};
const K = makeKit({ pixelRatio: 2 });
const { esp, red, yel, grn, btn, rgb, pot } = buildP1(K, ["D23", "D22", "D18", "TX2", "D25", "D26", "D27", "D34", "GND", "3V3"]);
const usb = K.usbCable(esp);

/* ---------------- the game ---------------- */
const IDLE = [0, 0, 40 / 255];
/** rounds: [{ start, wait, press } | { start, wait, falseAt }] in clip seconds, sorted */
function game(t, rounds) {
  let r = null;
  for (const x of rounds) if (t >= x.start) r = x;
  const off = [0, 0, 0];
  if (!r) return { lights: off, rgb: IDLE };
  const g0 = r.start + 1 + r.wait;
  if (r.falseAt != null && t >= r.falseAt) {
    const k = t - r.falseAt;
    if (k < 2) return { lights: off, rgb: Math.floor(k / 0.15) % 2 === 0 ? [1, 0, 0] : [0, 0, 0] };
    return { lights: off, rgb: IDLE };
  }
  if (t < r.start + 1) return { lights: [1, 0, 0], rgb: [0, 0, 0] };
  if (t < g0) return { lights: [0, 1, 0], rgb: [0, 0, 0] };
  if (r.press == null || t < r.press) return { lights: [0, 0, 1], rgb: [0, 0, 0] };
  const react = r.press - g0;
  if (t < r.press + 3) return { lights: off, rgb: react < 0.25 ? [0, 1, 0] : react < 0.5 ? [1, 160 / 255, 0] : [1, 0, 0] };
  return { lights: off, rgb: IDLE };
}
function setGame(t, rounds) {
  const s = game(t, rounds);
  red.set(s.lights[0]); yel.set(s.lights[1]); grn.set(s.lights[2]); rgb.set(...s.rgb);
}
const pressesOf = (rounds) => rounds.flatMap((r) => [[r.start - 0.02, r.start + 0.18], r.press != null ? [r.press, r.press + 0.16] : null, r.falseAt != null ? [r.falseAt, r.falseAt + 0.16] : null].filter(Boolean));
function setButton(t, presses) {
  let p = 0, pulse = -1;
  for (const [a, b] of presses) {
    if (t >= a && t < b) p = Math.max(p, clamp01((t - a) / 0.07));
    else if (t >= b && t < b + 0.09) p = Math.max(p, 1 - (t - b) / 0.09);
    if (t >= a && t < a + 0.7) pulse = (t - a) / 0.7;
  }
  btn.set(p, pulse);
}

/* ---------------- tags ---------------- */
const ui = document.getElementById("ui");
const tags = [];
function tag(html, p, t0, t1, o = {}) {
  const tg = makeTag(ui, html, (o.side && o.side !== "up" ? o.side : "") + " " + (o.cls || ""));
  show(tg.el, t0, 0.35);
  if (t1 != null) hide(tg.el, t1, 0.3);
  tags.push({ tg, p, dx: o.dx || 0, dy: o.dy || 0 });
  return tg;
}
const T2 = (title, coord) => `${title}<span class="c">${coord}</span>`;
function partTags(t0) {
  tag(T2("RED", "D23 · 21h 22h"), red.top, t0, null, { side: "right" });
  tag(T2("YELLOW", "D18 · 14h 15h"), yel.top, t0 + 0.3, null, { side: "right" });
  tag(T2("GREEN", "D17 · 8h 7h"), grn.top, t0 + 0.6, null, { side: "right" });
  tag(T2("BUTTON", "D22 · 26–28 e/f"), btn.top, t0 + 0.9, null, {});
  tag(T2("RESULT (RGB)", "D25 D26 D27 · 24–27c"), rgb.top, t0 + 1.2, null, { side: "left", cls: "teal" });
  tag(T2("KNOB", "D34 · 8–12c"), pot.top, t0 + 1.5, null, { side: "left", cls: "teal" });
}

/* ---------------- camera ---------------- */
const cam = (th, el, hh, p, dz = 0, dx = 0) => ({ th, el, hh, tx: p[0] + dx, ty: p[1] * 0.6, tz: p[2] + dz });
const WIDE = [0, 10, -2];
const rightCol = K.centre(btn.top, grn.top);
const usbEnd = [esp.xc, esp.pcbTop, esp.zU - 10];

let path, apply;
const R = EV.rounds || [];
if (CLIP === "C0") {
  const r = R[0], g0 = r.start + 1 + r.wait;
  path = K.camPath([
    [0, cam(-30, 38, 31, rightCol, -2, -16)],
    [g0 - 0.5, cam(-26, 42, 31, rightCol, 0, -10)],
    [r.press + 0.5, cam(-12, 52, 44, WIDE)],
    [EV.dur, cam(10, 54, 41, WIDE)],
  ]);
  tag("GO!", grn.top, g0, r.press + 0.6, { cls: "act" });
  tag(T2("213 ms", "FAST: GREEN"), rgb.top, r.press + 0.3, r.press + 3, { cls: "teal" });
  tag(T2("RECORD", "213 ms · saved"), rgb.top, EV.record, null, { cls: "teal" });
  apply = (t) => { setGame(t, R); setButton(t, pressesOf(R)); usb.set(0); };
} else if (CLIP === "C4") {
  path = K.camPath([[0, cam(-18, 56, 50, WIDE)], [EV.dur, cam(-6, 54, 47, WIDE)]]);
  partTags(0.2);
  apply = (t) => { setGame(t, R); setButton(t, pressesOf(R)); usb.set(0); };
} else if (CLIP === "C1") {
  const r = R[0], g0 = r.start + 1 + r.wait;
  path = K.camPath([[0, cam(-14, 54, 46, WIDE)], [EV.dur, cam(-2, 53, 44, WIDE)]]);
  tag("GO!", grn.top, g0, g0 + 0.9, { cls: "act" });
  tag("…PRESS", btn.top, r.press - 0.05, r.press + 1.2, { cls: "act" });
  tag(T2("1046 ms", "SLOW: RED"), rgb.top, r.press + 0.3, null, { cls: "teal" });
  apply = (t) => { setGame(t, R); setButton(t, pressesOf(R)); usb.set(0); };
} else if (CLIP === "C2" || CLIP === "S2") {
  const { unplug, plug } = EV;
  const sq = CLIP === "S2";
  path = K.camPath([
    [0, cam(-28, 40, sq ? 30 : 26, usbEnd, 4, sq ? 0 : -6)],
    [EV.dur, cam(-16, 46, sq ? 34 : 30, usbEnd, 0, sq ? 0 : -6)],
  ]);
  tag("UNPLUG", usb.top, unplug - 0.1, unplug + 1.4, { cls: "act" });
  tag("PLUG BACK IN", usb.top, plug - 0.1, plug + 1.4, { cls: "act" });
  apply = (t) => {
    const out = t < unplug ? 0 : t < unplug + 0.35 ? (t - unplug) / 0.35 : t < plug ? 1 : t < plug + 0.3 ? 1 - (t - plug) / 0.3 : 0;
    usb.set(out);
    const powered = t < unplug + 0.25 || t >= plug + 0.25;
    esp.power(powered);
    red.set(0); yel.set(0); grn.set(0);
    rgb.set(...(powered && (t < unplug || t >= plug + 0.9) ? IDLE : [0, 0, 0]));
    btn.set(0);
  };
} else if (CLIP === "S0" || CLIP === "S5") {
  const top = [0, 10, -3];
  path = K.camPath([[0, cam(-8, 54, 52, top)], [EV.dur, cam(4, 56, 49, top)]]);
  for (const r of R) {
    const g0 = r.start + 1 + r.wait;
    if (r.falseAt != null) tag("FALSE START!", rgb.top, r.falseAt + 0.05, r.falseAt + 2, { cls: "act" });
    else { tag("GO!", grn.top, g0, r.press + 0.5, { cls: "act" }); tag(`${Math.round((r.press - g0) * 1000)} ms`, rgb.top, r.press + 0.2, r.press + 2.8, { cls: "act" }); }
  }
  apply = (t) => { setGame(t, R); setButton(t, pressesOf(R)); usb.set(0); };
} else if (CLIP === "S4") {
  const esp32 = K.parts.find((p) => p.drop);
  const wires = K.parts.filter((p) => p.kind === "wire");
  const res = K.parts.filter((p) => p.kind === "resistor");
  const others = K.parts.filter((p) => p !== esp32 && !wires.includes(p) && !res.includes(p));
  const plan = [[esp32, 0.25, 0.55]];
  others.forEach((p, i) => plan.push([p, 0.85 + i * 0.12, 0.35]));
  res.forEach((p, i) => plan.push([p, 1.45 + i * 0.09, 0.3]));
  wires.forEach((p, i) => plan.push([p, 2.0 + i * 0.09, 0.45]));
  const ready = 2.0 + wires.length * 0.09 + 0.5;
  const rounds = [{ start: ready + 0.2, wait: 1, press: ready + 2.2 + 0.19 }];
  path = K.camPath([[0, cam(-24, 60, 62, WIDE, 4)], [ready, cam(-10, 56, 58, WIDE, 4)], [EV.dur, cam(2, 54, 55, WIDE, 4)]]);
  apply = (t) => {
    for (const [p, a, d] of plan) p.reveal((t - a) / d);
    usb.group.visible = t > ready - 0.4;
    usb.set(t < ready ? 1 - clamp01((t - ready + 0.4) / 0.4) : 0);
    esp.power(t >= ready);
    if (t < ready) { red.set(0); yel.set(0); grn.set(0); rgb.set(0, 0, 0); } else setGame(t, rounds);
    setButton(t, pressesOf(rounds));
  };
} else throw new Error("unknown clip " + CLIP);

dyn((t) => {
  apply(t);
  K.placeCamera(path(t));
  for (const { tg, p, dx, dy } of tags) { tg.at(p, K.toScreen, dy); if (dx) tg.el.style.left = parseFloat(tg.el.style.left) + dx + "px"; }
  K.render();
});
window.__seek(0);
window.__ready = true;
