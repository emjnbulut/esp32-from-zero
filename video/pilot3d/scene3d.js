/* ESP32 From Zero - 3D pilot (PWM dims an LED), ~20 s.
 * Stylized look: toon shading (3 tones) + thin dark outlines, brand colors, orthographic "isometric" camera.
 * Everything is a pure function of time t: lib.js calls window.__seek(t) -> dyn() below renders that exact frame.
 * 1 scene unit = 1 mm. Breadboard pitch 2.54 mm. Board = 30-pin DevKit (same pinout as engine/board.js).
 * Pins/wiring follow episode 5: red LED on GPIO 23 (+220 ohm to GND).
 */
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import { GLTFExporter } from "three/addons/exporters/GLTFExporter.js";

const P = 2.54;
const BB = { len: 165, dep: 55, h: 9 };
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const backOut = (x) => { x = clamp01(x); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2; };
const lerp = (a, b, k) => a + (b - a) * k;
const V = (x, y, z) => new THREE.Vector3(x, y, z);

/* ---------------- renderer ---------------- */
const canvas = document.getElementById("c3d");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(1920, 1080, false);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
scene.background = new THREE.Color("#0b1220");

/* toon ramp: shadow / mid / lit */
const ramp = new THREE.DataTexture(new Uint8Array([88, 88, 88, 255, 168, 168, 168, 255, 236, 236, 236, 255, 255, 255, 255, 255]), 4, 1, THREE.RGBAFormat);
ramp.minFilter = ramp.magFilter = THREE.NearestFilter;
ramp.needsUpdate = true;

const MATS = {};
function mat(name, color, extra = {}) {
  if (MATS[name]) return MATS[name];
  const m = new THREE.MeshToonMaterial({ color, gradientMap: ramp, ...extra });
  m.name = name;
  return (MATS[name] = m);
}
const lineMat = new THREE.LineBasicMaterial({ color: "#070b14", transparent: true, opacity: 0.6 });

function add(parent, geo, m, pos, o = {}) {
  const mesh = new THREE.Mesh(geo, m);
  mesh.position.set(pos[0], pos[1], pos[2]);
  if (o.rot) mesh.rotation.set(o.rot[0], o.rot[1], o.rot[2]);
  mesh.castShadow = o.cast ?? true;
  mesh.receiveShadow = o.recv ?? true;
  if (o.edges !== false) {
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(geo, o.edgeAngle ?? 35), lineMat);
    e.userData.noExport = true;
    mesh.add(e);
  }
  parent.add(mesh);
  return mesh;
}
function instanced(parent, geo, m, positions, o = {}) {
  const im = new THREE.InstancedMesh(geo, m, positions.length);
  const M = new THREE.Matrix4();
  positions.forEach((p, i) => im.setMatrixAt(i, M.makeTranslation(p[0], p[1], p[2])));
  im.castShadow = o.cast ?? false;
  im.receiveShadow = true;
  parent.add(im);
  return im;
}
function canvasTex(w, h, draw) {
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

/* ---------------- desk ---------------- */
const deskTex = canvasTex(512, 512, (g, w, h) => {
  const r = g.createRadialGradient(w / 2, h / 2, 10, w / 2, h / 2, w / 2);
  r.addColorStop(0, "#1c2a47"); r.addColorStop(0.55, "#121c31"); r.addColorStop(1, "#0b1220");
  g.fillStyle = r; g.fillRect(0, 0, w, h);
});
const desk = new THREE.Mesh(new THREE.PlaneGeometry(700, 700), new THREE.MeshBasicMaterial({ map: deskTex }));
desk.rotation.x = -Math.PI / 2;
desk.userData.noExport = true;
scene.add(desk);
const shadowCatcher = new THREE.Mesh(new THREE.PlaneGeometry(700, 700), new THREE.ShadowMaterial({ opacity: 0.45, color: "#02040a" }));
shadowCatcher.rotation.x = -Math.PI / 2;
shadowCatcher.position.y = 0.02;
shadowCatcher.receiveShadow = true;
shadowCatcher.userData.noExport = true;
scene.add(shadowCatcher);

/* ---------------- lights ---------------- */
const hemi = new THREE.HemisphereLight("#d6e6ff", "#1a2238", 0.9);
hemi.userData.noExport = true;
scene.add(hemi);
const sun = new THREE.DirectionalLight("#fff6ea", 1.5);
sun.position.set(-70, 160, 90);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -110, right: 110, top: 110, bottom: -110, near: 10, far: 400 });
sun.shadow.bias = -0.0004;
sun.shadow.normalBias = 0.15;
sun.userData.noExport = true;
scene.add(sun);

/* ---------------- breadboard ---------------- */
const ROW = { a: -15.24, b: -12.7, c: -10.16, d: -7.62, e: -5.08, f: 5.08, g: 7.62, h: 10.16, i: 12.7, j: 15.24 };
const RAIL = { tp: -24.14, tm: -21.6, bp: 21.6, bm: 24.14 };
const COLS = 31; // columns k = -31..31
const top = BB.h;
const bb = new THREE.Group();
bb.name = "breadboard";
scene.add(bb);
add(bb, new RoundedBoxGeometry(BB.len, BB.h, BB.dep, 3, 1.4), mat("breadboard", "#ecebe6"), [0, BB.h / 2, 0], { edgeAngle: 60 });
add(bb, new THREE.BoxGeometry(BB.len - 8, 0.6, 2.9), mat("groove", "#cfccc3"), [0, top - 0.26, 0], { edges: false, cast: false });
const holes = [];
for (let k = -COLS; k <= COLS; k++) {
  for (const z of Object.values(ROW)) holes.push([k * P, top + 0.02, z]);
  if ((k + COLS) % 6 !== 5) for (const z of Object.values(RAIL)) holes.push([k * P, top + 0.02, z]);
}
instanced(bb, new THREE.BoxGeometry(1.35, 0.06, 1.35), mat("hole", "#4a4842"), holes);
for (const [z, c] of [[-26.0, "#e5484d"], [-19.7, "#3b6fe0"], [19.7, "#e5484d"], [26.0, "#3b6fe0"]])
  add(bb, new THREE.BoxGeometry(BB.len - 16, 0.08, 0.55), mat("rail" + c, c), [0, top + 0.03, z], { edges: false, cast: false });

/* ---------------- ESP32 DevKit (30 pins) ---------------- */
const esp = new THREE.Group();
esp.name = "esp32";
scene.add(esp);
const PIN0X = 17.78; // pin index 0 (D23 / EN) column, antenna end at +x
const pinX = (i) => PIN0X - i * P;
const BCX = PIN0X + 8.94 - 25.75; // board centre x (pin 0 sits 8.94 mm from the antenna edge)
const pcbY = top + 2.5; // header plastic is 2.5 mm tall
add(esp, new RoundedBoxGeometry(51.5, 1.6, 28.3, 2, 0.6), mat("pcb", "#1f2530"), [BCX, pcbY + 0.8, 0], { edgeAngle: 60 });
for (const z of [ROW.b, ROW.i]) add(esp, new THREE.BoxGeometry(15 * P, 2.5, 2.5), mat("header", "#15181d"), [0, top + 1.25, z], { edges: true });
const pads = [], posts = [];
for (let i = 0; i < 15; i++) for (const z of [ROW.b, ROW.i]) {
  pads.push([pinX(i), pcbY + 1.62, z]);
  posts.push([pinX(i), pcbY + 2.3, z]);
}
instanced(esp, new THREE.BoxGeometry(1.9, 0.06, 1.9), mat("gold", "#e0b84a"), pads);
instanced(esp, new THREE.BoxGeometry(0.64, 1.4, 0.64), mat("gold", "#e0b84a"), posts, { cast: true });
const pcbTop = pcbY + 1.6;
const modX = BCX + 25.75 - 12.75 - 0.4;
add(esp, new THREE.BoxGeometry(25.5, 0.8, 18), mat("module", "#24384f"), [modX, pcbTop + 0.4, 0]);
const shieldX = modX - 12.75 + 8.9 + 1.0;
const shield = add(esp, new RoundedBoxGeometry(17.8, 2.4, 15.5, 2, 0.35), mat("shield", "#c9d1db"), [shieldX, pcbTop + 0.8 + 1.2, 0], { edgeAngle: 60 });
const label = new THREE.Mesh(new THREE.PlaneGeometry(14, 7), new THREE.MeshBasicMaterial({
  transparent: true,
  map: canvasTex(560, 280, (g, w, h) => {
    g.fillStyle = "#5d6670"; g.textAlign = "center";
    g.font = "700 58px Segoe UI"; g.fillText("ESP32-WROOM-32", w / 2, 128);
    g.font = "500 38px Segoe UI"; g.fillText("WiFi + Bluetooth", w / 2, 196);
  }),
}));
label.rotation.set(-Math.PI / 2, 0, Math.PI / 2);
label.position.set(shieldX, pcbTop + 3.21, 0);
esp.add(label);
// antenna meander
const antX0 = modX + 12.75 - 4.6;
for (let s = 0; s < 7; s++) {
  const z = -6 + s * 2;
  add(esp, new THREE.BoxGeometry(3.6, 0.06, 0.45), mat("gold", "#e0b84a"), [antX0 + 1.8, pcbTop + 0.83, z], { edges: false, cast: false });
  if (s < 6) add(esp, new THREE.BoxGeometry(0.45, 0.06, 2.0), mat("gold", "#e0b84a"), [s % 2 ? antX0 : antX0 + 3.6, pcbTop + 0.83, z + 1], { edges: false, cast: false });
}
const bMin = BCX - 25.75;
add(esp, new RoundedBoxGeometry(5.8, 2.8, 7.8, 2, 0.4), mat("usb", "#d5dbe2"), [bMin + 1.9, pcbTop + 1.4, 0]);
add(esp, new THREE.BoxGeometry(5, 1, 5), mat("ic", "#121418"), [bMin + 12, pcbTop + 0.5, 4.5]);
add(esp, new THREE.BoxGeometry(3.6, 1.6, 6.5), mat("ic", "#121418"), [bMin + 13, pcbTop + 0.8, -5.5]);
for (const z of [-9.6, 9.6]) {
  add(esp, new THREE.BoxGeometry(4, 1.3, 3.6), mat("button", "#cfd5dc"), [bMin + 5.5, pcbTop + 0.65, z]);
  add(esp, new THREE.CylinderGeometry(1.1, 1.1, 0.8, 20), mat("ic", "#121418"), [bMin + 5.5, pcbTop + 1.6, z], { edges: false });
}
const pwrLedMat = new THREE.MeshToonMaterial({ color: "#5a1a1a", gradientMap: ramp, emissive: "#ff2a2a", emissiveIntensity: 0 });
pwrLedMat.name = "pwrled";
add(esp, new THREE.BoxGeometry(1.6, 0.7, 1), pwrLedMat, [bMin + 9.5, pcbTop + 0.35, -2.2], { edges: false });
add(esp, new THREE.BoxGeometry(1.6, 0.7, 1), mat("io2led", "#1d3f7a"), [bMin + 9.5, pcbTop + 0.35, 2.2], { edges: false });

/* ---------------- red LED on GPIO 23 (anode col x=38.1, cathode col x=40.64, row h) ---------------- */
const LED = { x: (38.1 + 40.64) / 2, z: ROW.h, y0: top + 3.4 };
const led = new THREE.Group();
led.name = "led";
led.position.set(LED.x, 0, LED.z);
scene.add(led);
const ledBodyMat = new THREE.MeshToonMaterial({ color: "#d42a2a", gradientMap: ramp, emissive: "#ff3030", emissiveIntensity: 0 });
ledBodyMat.name = "led";
const prof = [V(0.01, 0, 0), V(2.9, 0, 0), V(2.9, 1, 0), V(2.5, 1, 0), V(2.5, 5.2, 0)];
for (let a = 1; a <= 10; a++) { const q = (a / 10) * Math.PI / 2; prof.push(V(2.5 * Math.cos(q) + 0.001, 5.2 + 2.5 * Math.sin(q), 0)); }
add(led, new THREE.LatheGeometry(prof.map((p) => new THREE.Vector2(p.x, p.y)), 40), ledBodyMat, [0, LED.y0, 0], { edgeAngle: 40 });
for (const dx of [-1.27, 1.27]) add(led, new THREE.CylinderGeometry(0.25, 0.25, LED.y0 - top + 0.2, 8), mat("lead", "#b8bec6"), [dx, (LED.y0 + top) / 2, 0], { edges: false });
const glowTex = canvasTex(256, 256, (g, w) => {
  const r = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2);
  r.addColorStop(0, "rgba(255,120,110,1)"); r.addColorStop(0.25, "rgba(255,70,60,.55)"); r.addColorStop(1, "rgba(255,40,40,0)");
  g.fillStyle = r; g.fillRect(0, 0, w, w);
});
const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0 }));
glow.position.set(0, LED.y0 + 5.2, 0);
glow.userData.noExport = true;
led.add(glow);
const ledLight = new THREE.PointLight("#ff3b30", 0, 70, 1.6);
ledLight.position.set(0, LED.y0 + 6, 0);
ledLight.userData.noExport = true;
led.add(ledLight);

/* ---------------- 220 ohm resistor: col x=40.64, row j -> GND rail (bm) ---------------- */
const res = new THREE.Group();
res.name = "resistor";
const RZ0 = ROW.j, RZ1 = RAIL.bm, RZC = (RZ0 + RZ1) / 2, RY = top + 2.2;
res.position.set(40.64, 0, RZC);
scene.add(res);
add(res, new THREE.CapsuleGeometry(1.15, 3.6, 6, 18), mat("resistor", "#dcc59b"), [0, RY, 0], { rot: [Math.PI / 2, 0, 0], edgeAngle: 50 });
[["#d4352f", -1.35], ["#d4352f", -0.55], ["#6b3a1e", 0.25], ["#c9a54a", 1.45]].forEach(([c, dz], i) =>
  add(res, new THREE.CylinderGeometry(1.2, 1.2, 0.45, 18), mat("band" + i, c), [0, RY, dz], { rot: [Math.PI / 2, 0, 0], edges: false }));
for (const s of [-1, 1]) {
  const zEnd = s * ((RZ1 - RZ0) / 2);
  const lead = new THREE.CatmullRomCurve3([V(0, RY, s * 2.6), V(0, RY, zEnd - s * 0.6), V(0, RY - 0.8, zEnd), V(0, top - 0.2, zEnd)]);
  add(res, new THREE.TubeGeometry(lead, 16, 0.25, 6), mat("lead", "#b8bec6"), [0, 0, 0], { edges: false });
}

/* ---------------- wires ---------------- */
function wire(name, pts, color, emissive) {
  const curve = new THREE.CatmullRomCurve3(pts.map((p) => V(...p)), false, "centripetal");
  const geo = new THREE.TubeGeometry(curve, 80, 0.6, 10);
  const m = new THREE.MeshToonMaterial({ color, gradientMap: ramp, emissive: emissive || "#000000", emissiveIntensity: 0 });
  m.name = name;
  const mesh = add(scene, geo, m, [0, 0, 0], { edges: false });
  mesh.name = name;
  mesh.userData.total = geo.index.count;
  return mesh;
}
const sigWire = wire("wire_gpio23", [[PIN0X, top - 0.5, ROW.j], [PIN0X, top + 5, ROW.j + 0.4], [PIN0X + 5, top + 8.5, ROW.j + 1.8],
  [38.1 - 5, top + 8.5, ROW.j + 1.8], [38.1, top + 5, ROW.j + 0.4], [38.1, top - 0.5, ROW.j]], "#ff8a2a", "#ffb547");
const GNDX = pinX(13);
const gndWire = wire("wire_gnd", [[GNDX, top - 0.5, ROW.j], [GNDX, top + 4.5, ROW.j + 0.6], [GNDX + 2.5, top + 6.5, ROW.j + 4.5],
  [GNDX + 5.08, top + 4.5, RAIL.bm - 0.5], [GNDX + 5.08, top - 0.5, RAIL.bm]], "#1d1f24");
function drawWire(w, p) { w.geometry.setDrawRange(0, Math.floor((w.userData.total / 6) * clamp01(p)) * 6); w.visible = p > 0.001; }

/* ---------------- post-processing ---------------- */
const rt = new THREE.WebGLRenderTarget(1920, 1080, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, rt);
const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 1, 3000);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(1920, 1080), 0.55, 0.45, 1.05);
composer.addPass(bloom);
composer.addPass(new OutputPass());

/* ---------------- camera keys (deg, deg, half-height mm, target) ---------------- */
const KEYS = [
  [0.0, { th: -40, el: 46, hh: 40, tx: 6, ty: 8, tz: 3 }],
  [3.4, { th: -27, el: 38, hh: 47, tx: 2, ty: 8, tz: 3 }],
  [4.4, { th: -24, el: 37, hh: 49, tx: -24, ty: 8, tz: 3 }],
  [9.0, { th: -14, el: 35, hh: 49, tx: -24, ty: 8, tz: 3 }],
  [10.0, { th: 4, el: 30, hh: 20, tx: 30, ty: 13, tz: 10 }],
  [14.6, { th: 10, el: 30, hh: 21, tx: 30.5, ty: 13, tz: 10 }],
  [15.8, { th: -32, el: 40, hh: 52, tx: -2, ty: 14, tz: -8 }],
  [20.0, { th: -24, el: 38, hh: 50, tx: -2, ty: 14, tz: -8 }],
];
function camAt(t) {
  let i = 0;
  while (i < KEYS.length - 2 && t >= KEYS[i + 1][0]) i++;
  const [t0, a] = KEYS[i], [t1, b] = KEYS[i + 1];
  const k = smooth((t - t0) / (t1 - t0));
  const c = {};
  for (const key of Object.keys(a)) c[key] = lerp(a[key], b[key], k);
  return c;
}
function placeCamera(c) {
  const th = (c.th * Math.PI) / 180, el = (c.el * Math.PI) / 180, R = 800;
  const tg = V(c.tx, c.ty, c.tz);
  camera.position.set(tg.x + R * Math.cos(el) * Math.sin(th), tg.y + R * Math.sin(el), tg.z + R * Math.cos(el) * Math.cos(th));
  camera.lookAt(tg);
  const a = 1920 / 1080;
  Object.assign(camera, { left: -c.hh * a, right: c.hh * a, top: c.hh, bottom: -c.hh });
  camera.updateProjectionMatrix();
}
function toScreen(p) {
  const v = p.clone().project(camera);
  return { x: (v.x * 0.5 + 0.5) * 1920, y: (-v.y * 0.5 + 0.5) * 1080 };
}

/* ---------------- the PWM story ---------------- */
const T_BREATH = 3.6, T_SLOW0 = 9.0, T_SLOW = 9.6, T_FAST = 13.6, T_AVG = 14.8, T_FULL = 15.2;
const BREATH_PERIOD = 2.7, SLOW_PERIOD = 1.0, DUTY = 64 / 255;
// pin state in slow motion (true = HIGH). Frequency rises from 1 Hz to ~24 Hz after T_FAST.
function slowPhase(tau) {
  if (tau < T_FAST) return (tau - T_SLOW) / SLOW_PERIOD;
  let ph = (T_FAST - T_SLOW) / SLOW_PERIOD;
  const dt = 1 / 240;
  for (let s = T_FAST; s < tau; s += dt) ph += (1 + 23 * smooth((s - T_FAST) / (T_AVG - T_FAST))) * dt;
  return ph;
}
const pinHigh = (tau) => tau >= T_SLOW && ((slowPhase(tau) % 1) + 1) % 1 < DUTY;
function valueAt(t) {
  if (t < T_BREATH) return 0;
  if (t < T_SLOW0) return 255 * (0.5 - 0.5 * Math.cos((2 * Math.PI * (t - T_BREATH)) / BREATH_PERIOD));
  if (t < T_FULL) return lerp(0, 64, smooth((t - T_SLOW0) / 0.6));
  return lerp(64, 255, smooth((t - T_FULL) / 0.9));
}
// what the LED actually shows at time t (0..1)
function ledAt(t) {
  const v = valueAt(t) / 255;
  if (t < T_SLOW) return t < T_SLOW0 ? v : v * (1 - smooth((t - T_SLOW0) / 0.6)); // fade out before slow motion starts
  if (t < T_AVG) {
    const bin = pinHigh(t) ? 1 : 0;
    return lerp(bin, DUTY, t < T_FAST ? 0 : smooth((t - T_FAST) / (T_AVG - T_FAST)));
  }
  return v;
}

/* ---------------- 2D overlay (same engine as the 2D episodes) ---------------- */
// Overlay-only mode (for the Blender version): no 3D canvas, transparent page, tags placed from __DATA.overlay.
const OVERLAY = (window.__DATA && window.__DATA.overlay) || null;
if (OVERLAY) {
  canvas.style.display = "none";
  document.querySelector(".vig").style.display = "none";
  document.documentElement.style.background = document.body.style.background = "transparent";
  document.getElementById("stage").style.background = "transparent";
}
const ui = document.getElementById("ui");
const card = el("div", "card", `<div class="k">YOUR CODE</div>
  <div class="code"><span class="fn">analogWrite</span>(23, <span class="num">0</span>);</div>
  <div class="cm">// red LED on GPIO 23</div>
  <div class="wave"><svg width="540" height="110" viewBox="0 0 540 110"><path d="" fill="none" stroke="#ff8a2a" stroke-width="5" stroke-linejoin="round"/>
  <line x1="534" y1="0" x2="534" y2="110" stroke="#8fa1c0" stroke-width="2" stroke-dasharray="5 6" opacity="0"/></svg>
  <div class="lab"><span>pin 23: ON / OFF</span><span>ON <b>0%</b> of the time</span></div></div>`, ui);
const numEl = card.querySelector(".num"), path = card.querySelector("path"), nowLine = card.querySelector("line"), pctEl = card.querySelector(".lab b");
const tag = el("div", "tag", "GPIO 23", ui);
const ledTag = el("div", "tag", "LED", ui);
const bSlow = el("div", "banner", "SLOW MOTION · 1000× SLOWER", ui);
const bReal = el("div", "banner", "BACK TO REAL SPEED", ui);
const note = el("div", "note", "Too fast to see. Your eye sees the <b>average</b>: about 25%.", ui);
const title = el("div", "title", `<div class="s">ESP32 FROM ZERO · PWM</div><div class="h">How a pin<br><b>dims</b> an LED</div>`, ui);

show(tag, 3.3, 0.4); hide(tag, 8.8, 0.4);
show(card, 4.1, 0.5); hide(card, 15.0, 0.5);
show(ledTag, 10.1, 0.4); hide(ledTag, 13.4, 0.4);
show(bSlow, 10.0, 0.4); hide(bSlow, 13.5, 0.3);
show(bReal, 13.7, 0.3); hide(bReal, 15.0, 0.4);
show(note, 14.1, 0.4); hide(note, 15.4, 0.4);
SET(nowLine, T_SLOW0, { opacity: 1 });
show(title, 16.0, 0.6);

const WAVE = { w: 534, hi: 10, lo: 98 };
function wavePath(t) {
  if (t < T_SLOW0) { // static PWM pattern with the current duty
    const d = valueAt(t) / 255, per = WAVE.w / 6;
    let s = `M0 ${WAVE.lo}`;
    for (let i = 0; i < 6; i++) {
      const x0 = i * per, x1 = x0 + per * d;
      if (d > 0.995) { s += ` L${x0.toFixed(1)} ${WAVE.hi} L${(x0 + per).toFixed(1)} ${WAVE.hi}`; continue; }
      if (d > 0.004) s += ` L${x0.toFixed(1)} ${WAVE.lo} L${x0.toFixed(1)} ${WAVE.hi} L${x1.toFixed(1)} ${WAVE.hi} L${x1.toFixed(1)} ${WAVE.lo}`;
    }
    return s + ` L${WAVE.w} ${WAVE.lo}`;
  }
  // slow motion: the wave scrolls left, the dashed line at the right edge is "now"
  const pps = 150;
  let s = "", prev = null;
  for (let x = 0; x <= WAVE.w; x += 1) {
    const y = pinHigh(t - (WAVE.w - x) / pps) ? WAVE.hi : WAVE.lo;
    if (prev === null) s = `M${x} ${y}`;
    else if (y !== prev) s += ` L${x} ${prev} L${x} ${y}`;
    prev = y;
  }
  return s + ` L${WAVE.w} ${prev}`;
}

/* ---------------- per-frame state ---------------- */
const ESP_REST = 0, ESP_DROP = 70;
function apply(t) {
  // assembly
  const bd = backOut((t - 0.25) / 1.15);
  esp.position.y = ESP_REST + (1 - bd) * ESP_DROP;
  esp.visible = t > 0.2;
  const ls = backOut((t - 1.35) / 0.5);
  led.scale.setScalar(Math.max(0.001, ls));
  led.visible = t > 1.35;
  const rs = backOut((t - 1.6) / 0.5);
  res.scale.setScalar(Math.max(0.001, rs));
  res.visible = t > 1.6;
  drawWire(sigWire, smooth((t - 2.0) / 1.1));
  drawWire(gndWire, smooth((t - 2.4) / 0.9));
  pwrLedMat.emissiveIntensity = t > 3.1 ? 2.2 : 0;

  // light
  const L = ledAt(t);
  const vis = Math.pow(L, 0.6);
  ledBodyMat.emissiveIntensity = 0.1 + 1.25 * vis;
  ledBodyMat.emissiveIntensity *= L > 0.001 ? 1 : 0;
  glow.material.opacity = 0.7 * vis;
  glow.scale.setScalar(8 + 9 * vis);
  ledLight.intensity = 320 * vis;
  const pinOn = t >= T_SLOW && t < T_AVG ? (pinHigh(t) ? 1 : 0) : L;
  sigWire.material.emissiveIntensity = (t >= T_SLOW && t < T_FAST ? 0.5 : 0.35) * pinOn;

  // camera
  placeCamera(camAt(t));

  // overlay
  numEl.textContent = Math.round(valueAt(t));
  pctEl.textContent = Math.round((valueAt(t) / 255) * 100) + "%";
  path.setAttribute("d", wavePath(t));
  let a, b;
  if (OVERLAY) { // 3D anchors projected by the Blender camera (blender_anim.py writes them per frame)
    const f = Math.min(OVERLAY.gpio23.length - 1, Math.max(0, Math.round(t * OVERLAY.fps)));
    a = { x: OVERLAY.gpio23[f][0], y: OVERLAY.gpio23[f][1] };
    b = { x: OVERLAY.ledTop[f][0], y: OVERLAY.ledTop[f][1] };
  } else {
    a = toScreen(V(PIN0X, pcbTop + 3.2 + esp.position.y, ROW.i));
    b = toScreen(V(LED.x, LED.y0 + 8.5, LED.z));
  }
  css(tag, { left: a.x + "px", top: a.y - 14 + "px" });
  css(ledTag, { left: b.x + "px", top: b.y - 22 + "px" });

  if (!OVERLAY) composer.render();
}
dyn(apply);

/* ---------------- GLB export for the Blender hero frame ---------------- */
window.__exportGLB = async (t) => {
  window.__seek(t);
  scene.updateMatrixWorld(true);
  const out = new THREE.Scene();
  scene.traverse((o) => {
    if (!o.isMesh || o.userData.noExport || !o.visible) return;
    let hidden = false;
    o.traverseAncestors((p) => { if (p.visible === false) hidden = true; });
    if (hidden) return;
    let geo;
    if (o.isInstancedMesh) {
      const parts = [], M = new THREE.Matrix4();
      for (let i = 0; i < o.count; i++) { o.getMatrixAt(i, M); parts.push(o.geometry.clone().applyMatrix4(M)); }
      geo = mergeGeometries(parts);
    } else {
      geo = o.geometry.clone();
      if (geo.drawRange.count !== Infinity && geo.index) geo.setIndex(Array.from(geo.index.array.slice(geo.drawRange.start, geo.drawRange.start + geo.drawRange.count)));
    }
    const m = o.material.clone();
    const mesh = new THREE.Mesh(geo, m);
    // group prefix ("esp32|pcb") lets Blender re-parent the parts that animate together
    let grp = "";
    o.traverseAncestors((p) => { if (!grp && ["esp32", "led", "resistor"].includes(p.name)) grp = p.name; });
    mesh.name = (grp ? grp + "|" : "") + (o.name || m.name);
    o.matrixWorld.decompose(mesh.position, mesh.quaternion, mesh.scale);
    out.add(mesh);
  });
  const buf = await new GLTFExporter().parseAsync(out, { binary: true });
  const bytes = new Uint8Array(buf);
  let s = "";
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  const c = camAt(t);
  const wirePts = (w) => w.geometry.parameters.path.getSpacedPoints(120).map((p) => [p.x, p.y, p.z]);
  return {
    glb: btoa(s), cam: c, led: [LED.x, LED.y0 + 5.2, LED.z],
    groups: { esp32: [0, 0, 0], led: [LED.x, 0, LED.z], resistor: [40.64, 0, RZC] },
    wires: { wire_gpio23: wirePts(sigWire), wire_gnd: wirePts(gndWire) },
    anchors: { gpio23: [PIN0X, pcbTop + 3.2, ROW.i], ledTop: [LED.x, LED.y0 + 8.5, LED.z] },
  };
};

window.__seek(0);
window.__ready = true;
