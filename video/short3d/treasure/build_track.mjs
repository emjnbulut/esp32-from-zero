// Quick build montage (inserted after the hook line): parts snap onto an empty breadboard on the narration words,
// then all wires zip in. Writes build/build_track.json (same frame format as track.json + parts/wires/anchors3d)
// and build/build_events.json (labels for the overlay, clicks/zips for the sound).
//   node short3d/treasure/build_track.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
const B = path.join(here, "build");
const sched = JSON.parse(fs.readFileSync(path.join(B, "build_schedule.json"), "utf8"));
const info = JSON.parse(fs.readFileSync(path.join(B, "scene_info.json"), "utf8"));
const FPS = 30, DUR = sched.duration, N = Math.round(DUR * FPS);
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const lerp = (a, b, k) => a + (b - a) * k;
const back = (x) => { x = clamp01(x); const c = 0.9; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2; };
const norm = (w) => w.toLowerCase().replace(/[^a-z0-9]/g, "");
const L = Object.fromEntries(sched.lines.map((l) => [l.id, l]));
const W = (id, word, off = 0) => { const w = L[id].words.find((x) => norm(x.w) === norm(word)); if (!w) throw new Error(word); return w.t + off; };

// when each group lands (seconds) and its label
const drops = [
  [["esp32"], W("b01", "inside", -0.05), "ESP32"],
  [["pot", "knob"], W("b01", "knob"), "knob"],
  [["btn", "btncap"], W("b01", "button"), "button"],
  [["rgb", "r_rgb_r", "r_rgb_g", "r_rgb_b"], W("b01", "color"), "color LED"],
  [["rled", "r_red"], W("b01", "red"), "red LED"],
];
const DROP = 0.3, HIGH = 45;
const landAt = {};
for (const [gs, t] of drops) gs.forEach((g, i) => { landAt[g] = t + (g.startsWith("r_") ? 0.12 + 0.06 * i : 0); });
// wires: all zip in during "A few wires", power first, then signals
const order = ["esp_3v3", "esp_gnd_b", "esp_gnd_t", "pot_wiper", "pot_gnd", "pot_3v3", "gpio22", "btn_gnd", "gpio25", "gpio26", "gpio27", "rgb_gnd", "gpio23"];
const w0 = W("b02", "few", -0.1), wEnd = W("b02", "ready", -0.15);
const ZIP = 0.32, step = (wEnd - w0 - ZIP) / (order.length - 1);
const wireAt = Object.fromEntries(order.map((n, i) => [n, w0 + i * step]));
const tReady = W("b02", "ready");
const GPIO = { pot_wiper: "GPIO 34", gpio22: "GPIO 22", gpio25: "GPIO 25", gpio26: "GPIO 26", gpio27: "GPIO 27", gpio23: "GPIO 23" };

// camera: high over the empty board, slowly lower and closer while it fills up
const C0 = { tgt: [12, 6, 0], a: 16, d: 300, fov: 34 }, C1 = { tgt: [14, 8, -2], a: 32, d: 240, fov: 34 };
function cam(t) {
  const k = smooth(t / DUR) * 0.8 + clamp01(t / DUR) * 0.2;
  const tgt = C0.tgt.map((v, i) => lerp(v, C1.tgt[i], k)), a = (lerp(C0.a, C1.a, k) * Math.PI) / 180, d = lerp(C0.d, C1.d, k);
  return { pos: [tgt[0] - d * Math.sin(a), tgt[1] + d * Math.cos(a), tgt[2] + 0.001], tgt, fov: lerp(C0.fov, C1.fov, k) };
}

const frames = [];
let beepOn = false, lastBeep = 0;
for (let f = 0; f < N; f++) {
  const t = f / FPS;
  const parts = {};
  for (const [g, tl] of Object.entries(landAt)) {
    const t0 = tl - DROP;
    parts[g] = t < t0 ? 9999 : +(HIGH * (1 - back((t - t0) / DROP))).toFixed(2);
  }
  const wires = Object.fromEntries(order.map((n) => [n, +smooth((t - wireAt[n]) / ZIP).toFixed(3)]));
  const on = t >= tReady;
  if (on && t * 1000 - lastBeep >= 58) { lastBeep = t * 1000; beepOn = !beepOn; } // map(2, 0, 50, 40, 700) = 66 ms in the sketch
  const c = cam(t);
  frames.push({ knobDeg: -135 + (61 / 99) * 270, rgb: on ? [244, 0, 11] : [0, 0, 0], rled: on && beepOn ? 1 : 0, cap: 0, party: 0, coin: null,
    rings: 0, dim: 0, parts, wires, cam: { pos: c.pos.map((v) => +v.toFixed(2)), tgt: c.tgt.map((v) => +v.toFixed(2)), fov: +c.fov.toFixed(2) } });
}

const A = info.anchors, top = 9;
const anchors3d = { espTop: [-29.5, top + 8, 0] };
for (const n of Object.keys(GPIO)) { const p = info.wires[n][0]; anchors3d["pin_" + n] = [p[0], top + 2, p[2]]; }
const anchorKeys = ["espTop", "knobTop", "btnTop", "rgbTop", "rledTop", ...Object.keys(GPIO).map((n) => "pin_" + n)];
const labelAnchor = { ESP32: "espTop", knob: "knobTop", button: "btnTop", "color LED": "rgbTop", "red LED": "rledTop" };
const events = {
  labels: [...drops.map(([, t, text]) => ({ text, key: labelAnchor[text], t0: t - 0.05, t1: t + 0.85, kind: "part" })),
    ...Object.entries(GPIO).map(([n, text]) => ({ text, key: "pin_" + n, t0: wireAt[n] + 0.1, t1: wireAt[n] + 0.95, kind: "pin" }))],
  clicks: Object.values(landAt).sort((a, b) => a - b),
  zips: order.map((n) => wireAt[n]),
  ready: tReady,
};
fs.writeFileSync(path.join(B, "build_track.json"), JSON.stringify({ fps: FPS, frames: N, duration: DUR, info, anchors3d, anchorKeys, track: frames }));
fs.writeFileSync(path.join(B, "build_events.json"), JSON.stringify(events, null, 1));
console.log("build montage", DUR.toFixed(2), "s,", N, "frames; wires", w0.toFixed(2), "-", wEnd.toFixed(2), "ready", tReady.toFixed(2));
