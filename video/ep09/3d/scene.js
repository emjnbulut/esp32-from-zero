/* Episode 9 - 3D clips that replace the creator's phone clips (no more filming, creator 19 Nov 2026).
 * One page, four clips; window.__DATA.clip picks the clip, __DATA.ev holds its event times (clip seconds),
 * written by ep09/3d/make.mjs from the narration schedule, so every light change lands on its word.
 *   C0  cold open: cars green, a press, yellow, red + walk green, blink, green again (then a slow orbit)
 *   C3  "here it is": one whole round, every part labelled with its breadboard coordinates
 *   C2  close-up: the walk light blinks in the last 2 s, cars still red, then the round ends
 *   C1  press_time: a quick tap, then a one-second hold; the yellow LED is on while the button is held
 *
 * The circuit is the creator's real layout (episodes 8-10): two vertical breadboards, the ESP32 between them with
 * the USB end down. Rows 1..63 bottom -> top, letters a..j left -> right on each board. Every connection:
 *   RIGHT board                                   LEFT board
 *   ESP32 right pins in column a, rows 18..4      ESP32 left pins in column j, rows 18..4
 *   D23 18a -> 220R 18d..21g -> RED + 21h, - 22h, black 22j -> (-) rail
 *   D22 17a -> yellow wire 17c..26c -> BUTTON 26e/28e/26f/28f, black 28j -> (-) rail
 *   D18 12a -> 220R 12d..14g -> YELLOW + 14h, - 15h, black 15j -> (-) rail
 *   D17 (TX2) 10a -> 220R 10d..8g -> GREEN + 8h, - 7h, black 7j -> (-) rail
 *   GND 5a -> black 5e -> (-) rail;  3V3 4a -> red 4e -> LEFT board (+) rail (around the USB end)
 *   LEFT: RGB legs R 24c, - 25c, G 26c, B 27c; 220R 24f..24e, 26f..26e, 27f..27e; black 25a -> (-) rail
 *         D25 11j -> red wire 11i..24g; D26 10j -> green 10i..26h; D27 9j -> blue 9i..27i
 *         POT legs 8c (GND) 10c (wiper) 12c (3.3 V): black 8a -> (-), red 12a -> (+) 13, orange 10d..15h (D34 15j)
 *         GND 5j -> black 5g -> (-) rail
 */
import { makeKit, makeTag, COL, smooth, clamp01 } from "../../engine3d/kit.js";
import { buildP1 } from "../../engine3d/circuit_p1.js";

const D = window.__DATA || {};
const CLIP = D.clip || "C3";
const EV = D.ev || {};
const K = makeKit({ pixelRatio: 2 });

/* ---------------- the circuit (shared: engine3d/circuit_p1.js) ---------------- */
const { L, R, esp, red, yel, grn, btn, rgb, pot } = buildP1(K);

/* ---------------- what the code does (same rules as crossing.ino / press_time.ino) ---------------- */
// crossing: y0 = the moment yellow starts; yellow 2 s, walk 4 s, blink 2 s (250 ms steps)
function crossing(t, y0) {
  if (y0 == null || t < y0) return { s: 0 };
  if (t < y0 + 2) return { s: 1 };
  if (t < y0 + 6) return { s: 2 };
  if (t < y0 + 8) return { s: 3, blinkOn: Math.floor((t - y0 - 6) / 0.25) % 2 === 1 };
  return { s: 0 };
}
const LIGHTS = (c) => [[0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, c.blinkOn ? 1 : 0]][c.s];
function setCrossing(t, y0) {
  const [r, y, g, wr, wg] = LIGHTS(crossing(t, y0));
  red.set(r); yel.set(y); grn.set(g); rgb.set(wr, wg, 0);
}
const inAny = (t, list) => list.some(([a, b]) => t >= a && t < b);
// the button cap: down in 70 ms, up in 90 ms; the ring starts at each press
function setButton(t, presses) {
  let p = 0, pulse = -1;
  for (const [a, b] of presses) {
    if (t >= a && t < b) p = Math.max(p, clamp01((t - a) / 0.07));
    else if (t >= b && t < b + 0.09) p = Math.max(p, 1 - (t - b) / 0.09);
    if (t >= a && t < a + 0.7) pulse = (t - a) / 0.7;
  }
  btn.set(p, pulse);
}

/* ---------------- 2D tags ---------------- */
const ui = document.getElementById("ui");
const tags = [];
/** a tag on a 3D point; side: "up" | "right" | "left"; dx/dy shift the anchor in screen px */
function tag(html, p, t0, t1, o = {}) {
  const tg = makeTag(ui, html, (o.side && o.side !== "up" ? o.side : "") + " " + (o.cls || ""));
  show(tg.el, t0, 0.35);
  if (t1 != null) hide(tg.el, t1, 0.3);
  tags.push({ tg, p, dx: o.dx || 0, dy: o.dy || 0 });
  return tg;
}
const T2 = (title, coord) => `${title}<span class="c">${coord}</span>`;

/* ---------------- camera points ---------------- */
const P_RGB = rgb.top, P_RED = red.top, P_YEL = yel.top, P_GRN = grn.top, P_BTN = btn.top, P_POT = pot.top;
const cam = (th, el, hh, p, dz = 0, dx = 0) => ({ th, el, hh, tx: p[0] + dx, ty: p[1] * 0.6, tz: p[2] + dz });
const WIDE = [0, 10, -2]; // middle of the whole circuit

let path, apply;
if (CLIP === "C0") {
  // ev: press (button down), y0 (yellow starts), dur
  const { press, y0 } = EV;
  const presses = [[press, press + 0.22]];
  const rightCol = K.centre(P_BTN, P_GRN);
  path = K.camPath([
    [0, cam(-34, 34, 30, rightCol, 4, -12)],
    [press - 1.4, cam(-28, 40, 30, rightCol, 0, -10)],
    [press - 0.2, cam(-22, 46, 32, rightCol, -2, -8)],
    [y0 + 1.4, cam(-18, 48, 33, rightCol, 0, -10)],
    [y0 + 2.6, cam(-12, 52, 42, WIDE)],
    [y0 + 8.6, cam(-2, 55, 41, WIDE)],
    [EV.dur, cam(12, 52, 39, WIDE)],
  ]);
  tag("PRESS", P_BTN, press - 0.05, press + 1.3, { cls: "act" });
  tag(T2("WALK LIGHT", "RGB LED"), P_RGB, y0 + 2.6, y0 + 6.2, { cls: "teal" });
  apply = (t) => { setCrossing(t, y0); setButton(t, presses); };
} else if (CLIP === "C3") {
  // ev: press, y0, dur. Every part gets its coordinates, one after another.
  const { press, y0 } = EV;
  const presses = [[press, press + 0.22]];
  path = K.camPath([
    [0, cam(-18, 56, 50, WIDE)],
    [EV.dur, cam(-6, 54, 47, WIDE)],
  ]);
  const s = 0.25;
  tag(T2("RED LED", "D23 · 21h 22h"), P_RED, s, null, { side: "right" });
  tag(T2("YELLOW", "D18 · 14h 15h"), P_YEL, s + 0.3, null, { side: "right" });
  tag(T2("GREEN", "D17 · 8h 7h"), P_GRN, s + 0.6, null, { side: "right" });
  tag(T2("BUTTON", "D22 · 26–28 e/f"), P_BTN, s + 0.9, null, {});
  tag(T2("WALK LIGHT", "D25 D26 · 24–27c"), P_RGB, s + 1.2, null, { side: "left", cls: "teal" });
  tag(T2("KNOB", "D34 · 8–12c"), P_POT, s + 1.5, null, { side: "left", cls: "teal" });
  tag("PRESS", P_BTN, press - 0.05, press + 1.2, { cls: "act", dy: -120 });
  apply = (t) => { setCrossing(t, y0); setButton(t, presses); };
} else if (CLIP === "C2") {
  // ev: blink (blink starts), dur. The walk light came on 4 s before the blink.
  const y0 = EV.blink - 6;
  const both = K.centre(P_RGB, P_RED);
  path = K.camPath([
    [0, cam(-12, 46, 15, P_RGB, -1)],
    [EV.blink + 0.6, cam(-4, 50, 13.5, P_RGB, -1)],
    [EV.blink + 1.3, cam(-4, 50, 31, both, 4)],
    [EV.blink + 2.1, cam(2, 50, 31, both, 4)],
    [EV.blink + 2.9, cam(-8, 52, 40, WIDE)],
    [EV.dur, cam(-2, 54, 39, WIDE)],
  ]);
  tag(T2("WALK LIGHT", "24–27c"), P_RGB, 0.3, EV.blink + 1.1, { cls: "teal", side: "right", dx: 40, dy: -30 });
  tag("HURRY!", P_RGB, EV.blink + 0.1, EV.blink + 1.1, { cls: "act", side: "left" });
  tag(T2("CARS", "RED · 21h 22h"), P_RED, EV.blink + 1.35, EV.blink + 2.2, {});
  apply = (t) => setCrossing(t, y0);
} else if (CLIP === "C1") {
  // ev: tap [a, b], hold [a, b], dur. press_time: the yellow LED follows the button.
  const presses = [EV.tap, EV.hold];
  const mid = K.centre(P_BTN, P_YEL);
  path = K.camPath([
    [0, cam(-26, 44, 23, mid, 0, -4)],
    [EV.hold[0] - 0.3, cam(-20, 46, 21, mid, 0, -4)],
    [EV.hold[1] + 0.5, cam(-16, 47, 20, mid, 0, -4)],
    [EV.dur, cam(-10, 48, 22, mid, 0, -4)],
  ]);
  tag(T2("BUTTON", "D22 · 26–28 e/f"), P_BTN, 0.15, null, { side: "left", dx: -70 });
  tag(T2("YELLOW", "D18 · 14h 15h"), P_YEL, 0.3, null, { side: "right" });
  tag("TAP", P_BTN, EV.tap[0] - 0.05, EV.tap[0] + 1.2, { cls: "act", dy: -10 });
  tag("HOLD 1 s", P_BTN, EV.hold[0] - 0.05, EV.hold[1] + 0.9, { cls: "act", dy: -10 });
  apply = (t) => {
    red.set(0); grn.set(0); rgb.set(0, 0, 0);
    yel.set(inAny(t, presses) ? 1 : 0);
    setButton(t, presses);
  };
} else if (CLIP === "S0") {
  // Short h0: "I press the button, but the walk light stays red. Is it broken?" Square crop in the middle (x 420-1500).
  const { press, y0 } = EV;
  const presses = [[press, press + 0.22]];
  const top = [0, 10, -3];
  path = K.camPath([
    [0, cam(-8, 54, 52, top)],
    [EV.dur, cam(4, 56, 49, top)],
  ]);
  tag("PRESS", P_BTN, press - 0.05, press + 1.3, { cls: "act" });
  tag("STILL RED?", P_RGB, press + 1.0, null, { cls: "act" });
  apply = (t) => { setCrossing(t, y0); setButton(t, presses); };
} else if (CLIP === "S4") {
  // Short h4: "Build the whole crossing, step by step": the parts snap in, wires zip in, then it runs.
  const esp32 = K.parts.find((p) => p.drop);
  const wires = K.parts.filter((p) => p.kind === "wire");
  const res = K.parts.filter((p) => p.kind === "resistor");
  const others = K.parts.filter((p) => p !== esp32 && !wires.includes(p) && !res.includes(p));
  const plan = [[esp32, 0.25, 0.55]];
  others.forEach((p, i) => plan.push([p, 0.85 + i * 0.12, 0.35]));
  res.forEach((p, i) => plan.push([p, 1.45 + i * 0.09, 0.3]));
  wires.forEach((p, i) => plan.push([p, 2.0 + i * 0.09, 0.45]));
  const ready = 2.0 + wires.length * 0.09 + 0.5;
  path = K.camPath([
    [0, cam(-24, 60, 62, WIDE, 4)],
    [ready, cam(-10, 56, 58, WIDE, 4)],
    [EV.dur, cam(2, 54, 55, WIDE, 4)],
  ]);
  apply = (t) => {
    for (const [p, a, d] of plan) p.reveal((t - a) / d);
    setCrossing(t, t < ready ? null : ready + 1.2);
    if (t < ready) { red.set(0); yel.set(0); grn.set(0); rgb.set(0, 0, 0); }
    setButton(t, [[ready + 0.5, ready + 0.72]]);
  };
} else if (CLIP === "TH") {
  // thumbnail hero still: cars red, walk light green, low and close (ev.cam overrides for trying angles)
  const c = EV.cam || cam(40, 24, 19, K.centre(P_RED, P_YEL, P_GRN), -6, -15);
  path = () => c;
  apply = () => { setCrossing(0, -3); btn.set(0); };
} else throw new Error("unknown clip " + CLIP);

dyn((t) => {
  apply(t);
  K.placeCamera(path(t));
  for (const { tg, p, dx, dy } of tags) { tg.at(p, K.toScreen, dy); if (dx) tg.el.style.left = parseFloat(tg.el.style.left) + dx + "px"; }
  K.render();
});
window.__seek(0);
window.__ready = true;
