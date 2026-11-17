/* Treasure-detector Short: the course circuit as 3D geometry (three.js), exported to Blender as GLB.
 * Units: 1 = 1 mm, y up, breadboard pitch 2.54. Pins = episodes 4-8: knob GPIO 34, button GPIO 22,
 * RGB LED GPIO 25/26/27 (+3 x 220 ohm), red LED GPIO 23 (+220 ohm). 30-pin board as in engine/board.js.
 * Mesh names carry a group prefix ("knob|cap") so Blender can animate parts together.
 * window.__export() -> { glb (base64), info (pivots, anchors) }.
 */
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";
import { GLTFExporter } from "three/addons/exporters/GLTFExporter.js";

const P = 2.54;
const BB = { len: 165, dep: 55, h: 9 };
const top = BB.h;
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const scene = new THREE.Scene();

const MATS = {};
const mat = (name, color, extra = {}) => MATS[name] || (MATS[name] = Object.assign(new THREE.MeshStandardMaterial({ color, roughness: 0.5, ...extra }), { name }));
function add(parent, geo, m, pos, rot) {
  const mesh = new THREE.Mesh(geo, m);
  mesh.position.set(pos[0], pos[1], pos[2]);
  if (rot) mesh.rotation.set(rot[0], rot[1], rot[2]);
  mesh.name = m.name;
  parent.add(mesh);
  return mesh;
}
function group(name, pivot = [0, 0, 0]) {
  const g = new THREE.Group();
  g.name = name;
  g.position.set(...pivot);
  scene.add(g);
  return g;
}
function merged(parent, geo, m, positions) {
  const parts = positions.map((p) => geo.clone().translate(p[0], p[1], p[2]));
  return add(parent, mergeGeometries(parts), m, [0, 0, 0]);
}

/* ---------------- breadboard ---------------- */
const ROW = { a: -15.24, b: -12.7, c: -10.16, d: -7.62, e: -5.08, f: 5.08, g: 7.62, h: 10.16, i: 12.7, j: 15.24 };
const RAIL = { tp: -24.14, tm: -21.6, bp: 21.6, bm: 24.14 };
const bb = group("breadboard");
add(bb, new RoundedBoxGeometry(BB.len, BB.h, BB.dep, 3, 1.4), mat("breadboard", "#ecebe6"), [0, BB.h / 2, 0]);
add(bb, new THREE.BoxGeometry(BB.len - 8, 0.6, 2.9), mat("groove", "#cfccc3"), [0, top - 0.26, 0]);
const holes = [];
for (let k = -31; k <= 31; k++) {
  for (const z of Object.values(ROW)) holes.push([k * P, top + 0.02, z]);
  if ((k + 31) % 6 !== 5) for (const z of Object.values(RAIL)) holes.push([k * P, top + 0.02, z]);
}
merged(bb, new THREE.BoxGeometry(1.35, 0.06, 1.35), mat("hole", "#4a4842"), holes);
for (const [z, c] of [[-26.0, "#e5484d"], [-19.7, "#3b6fe0"], [19.7, "#e5484d"], [26.0, "#3b6fe0"]])
  add(bb, new THREE.BoxGeometry(BB.len - 16, 0.08, 0.55), mat("rail" + c, c), [0, top + 0.03, z]);

/* ---------------- ESP32 (shifted left so the right half is free for the parts) ---------------- */
const PIN0X = -12.7; // D23 / EN column; antenna end towards +x
const pinX = (i) => PIN0X - i * P; // L and R pin i share a column
const BCX = PIN0X + 8.94 - 25.75;
const pcbY = top + 2.5, pcbTop = pcbY + 1.6;
const esp = group("esp32");
add(esp, new RoundedBoxGeometry(51.5, 1.6, 28.3, 2, 0.6), mat("pcb", "#1f2530"), [BCX, pcbY + 0.8, 0]);
for (const z of [ROW.b, ROW.i]) add(esp, new THREE.BoxGeometry(15 * P, 2.5, 2.5), mat("header", "#15181d"), [pinX(7), top + 1.25, z]);
const pads = [], posts = [];
for (let i = 0; i < 15; i++) for (const z of [ROW.b, ROW.i]) { pads.push([pinX(i), pcbY + 1.62, z]); posts.push([pinX(i), pcbY + 2.3, z]); }
merged(esp, new THREE.BoxGeometry(1.9, 0.06, 1.9), mat("gold", "#e0b84a"), pads);
merged(esp, new THREE.BoxGeometry(0.64, 1.4, 0.64), mat("gold", "#e0b84a"), posts);
const modX = BCX + 25.75 - 12.75 - 0.4;
add(esp, new THREE.BoxGeometry(25.5, 0.8, 18), mat("module", "#24384f"), [modX, pcbTop + 0.4, 0]);
const shieldX = modX - 12.75 + 8.9 + 1.0;
add(esp, new RoundedBoxGeometry(17.8, 2.4, 15.5, 2, 0.35), mat("shield", "#c9d1db"), [shieldX, pcbTop + 2.0, 0]);
const antX0 = modX + 12.75 - 4.6;
for (let s = 0; s < 7; s++) {
  const z = -6 + s * 2;
  add(esp, new THREE.BoxGeometry(3.6, 0.06, 0.45), mat("gold", "#e0b84a"), [antX0 + 1.8, pcbTop + 0.83, z]);
  if (s < 6) add(esp, new THREE.BoxGeometry(0.45, 0.06, 2.0), mat("gold", "#e0b84a"), [s % 2 ? antX0 : antX0 + 3.6, pcbTop + 0.83, z + 1]);
}
const bMin = BCX - 25.75;
add(esp, new RoundedBoxGeometry(5.8, 2.8, 7.8, 2, 0.4), mat("usb", "#d5dbe2"), [bMin + 1.9, pcbTop + 1.4, 0]);
add(esp, new THREE.BoxGeometry(5, 1, 5), mat("ic", "#121418"), [bMin + 12, pcbTop + 0.5, 4.5]);
add(esp, new THREE.BoxGeometry(3.6, 1.6, 6.5), mat("ic", "#121418"), [bMin + 13, pcbTop + 0.8, -5.5]);
for (const z of [-9.6, 9.6]) {
  add(esp, new THREE.BoxGeometry(4, 1.3, 3.6), mat("button", "#cfd5dc"), [bMin + 5.5, pcbTop + 0.65, z]);
  add(esp, new THREE.CylinderGeometry(1.1, 1.1, 0.8, 20), mat("ic", "#121418"), [bMin + 5.5, pcbTop + 1.6, z]);
}
add(esp, new THREE.BoxGeometry(1.6, 0.7, 1), mat("pwrled", "#ff3030"), [bMin + 9.5, pcbTop + 0.35, -2.2]);
add(esp, new THREE.BoxGeometry(1.6, 0.7, 1), mat("io2led", "#1d3f7a"), [bMin + 9.5, pcbTop + 0.35, 2.2]);

/* ---------------- small parts ---------------- */
function leg(parent, x, z, y0, y1) { add(parent, new THREE.CylinderGeometry(0.25, 0.25, y1 - y0, 8), mat("lead", "#b8bec6"), [x, (y0 + y1) / 2, z]); }
function ledBody(r) {
  const prof = [new THREE.Vector2(0.01, 0), new THREE.Vector2(r + 0.4, 0), new THREE.Vector2(r + 0.4, 1), new THREE.Vector2(r, 1), new THREE.Vector2(r, 5.2)];
  for (let a = 1; a <= 12; a++) { const q = (a / 12) * Math.PI / 2; prof.push(new THREE.Vector2(r * Math.cos(q) + 0.001, 5.2 + r * Math.sin(q))); }
  return new THREE.LatheGeometry(prof, 48);
}
function resistor(name, x0, z0, x1, z1) { // lying resistor between two holes
  const g = group(name);
  const a = V(x0, 0, z0), b = V(x1, 0, z1), mid = a.clone().add(b).multiplyScalar(0.5), dir = b.clone().sub(a);
  const len = dir.length(), ang = Math.atan2(dir.x, dir.z), RY = top + 2.2;
  const body = new THREE.Group();
  body.position.set(mid.x, RY, mid.z);
  body.rotation.y = ang;
  g.add(body);
  add(body, new THREE.CapsuleGeometry(1.15, 3.6, 6, 18), mat("resistor", "#dcc59b"), [0, 0, 0], [Math.PI / 2, 0, 0]);
  [["#d4352f", -1.35], ["#d4352f", -0.55], ["#6b3a1e", 0.25], ["#c9a54a", 1.45]].forEach(([c, dz], i) =>
    add(body, new THREE.CylinderGeometry(1.2, 1.2, 0.45, 18), mat("band" + i, c), [0, 0, dz], [Math.PI / 2, 0, 0]));
  for (const s of [-1, 1]) {
    const zEnd = (s * len) / 2;
    const lead = new THREE.CatmullRomCurve3([V(0, 0, s * 2.6), V(0, 0, zEnd - s * 0.6), V(0, -0.8, zEnd), V(0, top - 0.2 - RY, zEnd)]);
    add(body, new THREE.TubeGeometry(lead, 16, 0.25, 6), mat("lead", "#b8bec6"), [0, 0, 0]);
  }
  return g;
}
const WIRES = {};
function wire(name, color, a, b, h = 7) { // a, b = [x, z] holes; arc height h above the board
  const [x0, z0] = a, [x1, z1] = b;
  const d = Math.hypot(x1 - x0, z1 - z0), ux = (x1 - x0) / d, uz = (z1 - z0) / d;
  const lift = Math.min(3, d * 0.2);
  const pts = [V(x0, top - 0.5, z0), V(x0, top + h * 0.55, z0), V(x0 + ux * lift, top + h, z0 + uz * lift),
    V(x1 - ux * lift, top + h, z1 - uz * lift), V(x1, top + h * 0.55, z1), V(x1, top - 0.5, z1)];
  const curve = new THREE.CatmullRomCurve3(pts, false, "centripetal");
  const m = mat("wire" + color, color);
  const mesh = add(scene, new THREE.TubeGeometry(curve, 96, 0.6, 10), m, [0, 0, 0]);
  mesh.name = "wire|" + name;
  WIRES[name] = curve.getSpacedPoints(120).map((p) => [p.x, p.y, p.z]);
}

/* red LED on GPIO 23 */
const RLED = { x: (7.62 + 10.16) / 2, z: ROW.h, y0: top + 3.4 };
const rled = group("rled", [RLED.x, 0, RLED.z]);
add(rled, ledBody(2.5), mat("led", "#d42a2a"), [0, RLED.y0, 0]);
for (const dx of [-1.27, 1.27]) leg(rled, dx, 0, top - 0.2, RLED.y0);
resistor("r_red", 10.16, ROW.j, 10.16, RAIL.bm);
wire("gpio23", "#ff8a2a", [PIN0X, ROW.j], [7.62, ROW.j], 7);

/* button on GPIO 22 (12 mm tactile across the channel) */
const BTN = { x: 22.86, z: 0 };
const btn = group("btn", [BTN.x, 0, BTN.z]);
add(btn, new RoundedBoxGeometry(12, 3.4, 12, 2, 0.6), mat("btnbody", "#1a1c21"), [0, top + 1.9, 0]);
for (const [dx, dz] of [[-2.54, -5.08], [2.54, -5.08], [-2.54, 5.08], [2.54, 5.08]]) leg(btn, dx, dz, top - 0.2, top + 0.4);
const cap = group("btncap", [BTN.x, 0, BTN.z]);
add(cap, new THREE.CylinderGeometry(4.6, 4.9, 3.2, 40), mat("btncap", "#ffb547"), [0, top + 3.6 + 1.6, 0]);
wire("gpio22", "#f2d14a", [pinX(1), ROW.j], [20.32, ROW.g], 9);
wire("btn_gnd", "#1d1f24", [25.4, ROW.j], [25.4, RAIL.bm], 4);

/* RGB LED (common cathode) in the back half: R 35.56, GND 38.1, G 40.64, B 43.18 */
const RGB = { x: 39.37, z: ROW.c, y0: top + 4.2 };
const rgb = group("rgb", [RGB.x, 0, RGB.z]);
add(rgb, ledBody(2.6), mat("rgbled", "#f4f1ea"), [0, RGB.y0, 0]);
for (const dx of [-3.81, -1.27, 1.27, 3.81]) leg(rgb, dx, 0, top - 0.2, RGB.y0);
for (const [n, x] of [["r_rgb_r", 35.56], ["r_rgb_g", 40.64], ["r_rgb_b", 43.18]]) resistor(n, x, ROW.e, x, ROW.f);
wire("gpio25", "#e5484d", [pinX(7), ROW.a], [35.56, ROW.h], 15);
wire("gpio26", "#3fbf6a", [pinX(8), ROW.a], [40.64, ROW.i], 17);
wire("gpio27", "#3b6fe0", [pinX(9), ROW.a], [43.18, ROW.j], 19);
wire("rgb_gnd", "#1d1f24", [38.1, ROW.a], [38.1, RAIL.tm], 4);

/* potentiometer (shaft up) behind the back rows: legs GND 55.88, wiper 60.96, 3V3 66.04 in row a */
const POT = { x: 60.96, z: -20.5 };
const pot = group("pot", [POT.x, 0, POT.z]);
for (const dx of [-5.08, 0, 5.08]) {
  leg(pot, dx, ROW.a - POT.z, top - 0.2, top + 2.2);
  add(pot, new THREE.BoxGeometry(1.2, 0.5, 4.6), mat("lead", "#b8bec6"), [dx, top + 2.2, (ROW.a - POT.z) / 2 + 0.6]);
}
add(pot, new THREE.CylinderGeometry(8.2, 8.2, 2.2, 48), mat("potbase", "#1d2533"), [0, top + 3.2, 0]);
add(pot, new THREE.CylinderGeometry(7.8, 7.8, 4.4, 48), mat("potcan", "#c3c9d1"), [0, top + 6.5, 0]);
add(pot, new THREE.CylinderGeometry(3.6, 3.6, 2.2, 24), mat("potcan", "#c3c9d1"), [0, top + 9.8, 0]);
const KNOB_Y = top + 10.9;
const knob = group("knob", [POT.x, 0, POT.z]);
const flutes = new THREE.CylinderGeometry(7.4, 7.9, 9, 36);
add(knob, flutes, mat("knob", "#1b1d22"), [0, KNOB_Y + 4.5, 0]);
add(knob, new THREE.CylinderGeometry(6.6, 7.4, 1.2, 36), mat("knobtop", "#25282f"), [0, KNOB_Y + 9.6, 0]);
add(knob, new THREE.BoxGeometry(0.9, 0.3, 5.2), mat("knobmark", "#ffffff"), [0, KNOB_Y + 10.3, -3.2]);
wire("pot_wiper", "#c48bff", [pinX(3), ROW.a], [60.96, ROW.d], 22);
wire("pot_gnd", "#1d1f24", [55.88, ROW.c], [50.8, RAIL.tm], 5);
wire("pot_3v3", "#e5484d", [66.04, ROW.c], [71.12, RAIL.bp], 10);

/* power rails */
wire("esp_3v3", "#e5484d", [pinX(14), ROW.j], [pinX(14), RAIL.bp], 4);
wire("esp_gnd_b", "#1d1f24", [pinX(13), ROW.j], [pinX(13) + 2.54, RAIL.bm], 4);
wire("esp_gnd_t", "#1d1f24", [pinX(13), ROW.a], [pinX(13) + 2.54, RAIL.tm], 4);

/* ---------------- export ---------------- */
const pivots = {};
for (const g of ["esp32", "rled", "btn", "btncap", "rgb", "pot", "knob"]) pivots[g] = scene.getObjectByName(g).position.toArray();
const info = {
  pivots,
  wires: WIRES,
  anchors: {
    knobTop: [POT.x, KNOB_Y + 10.3, POT.z], knobCenter: [POT.x, KNOB_Y + 4, POT.z],
    rledTop: [RLED.x, RLED.y0 + 7.8, RLED.z], rgbTop: [RGB.x, RGB.y0 + 7.9, RGB.z],
    btnTop: [BTN.x, top + 6.8, BTN.z], board: [-29.5, top + 4, 0], center: [20, top, 0],
  },
};
window.__export = async () => {
  scene.updateMatrixWorld(true);
  const out = new THREE.Scene();
  scene.traverse((o) => {
    if (!o.isMesh) return;
    let grp = "";
    o.traverseAncestors((p) => { if (!grp && p.name && p.parent === scene && p.name !== "breadboard") grp = p.name; });
    const mesh = new THREE.Mesh(o.geometry.clone(), o.material);
    mesh.name = (grp ? grp + "|" : "") + o.name;
    o.matrixWorld.decompose(mesh.position, mesh.quaternion, mesh.scale);
    out.add(mesh);
  });
  const buf = await new GLTFExporter().parseAsync(out, { binary: true });
  const bytes = new Uint8Array(buf);
  let s = "";
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return { glb: btoa(s), info };
};

/* quick preview (top-left, so geometry can be checked without Blender) */
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("c"), antialias: true, preserveDrawingBuffer: true });
renderer.setSize(1080, 1920, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
scene.background = new THREE.Color("#0b1220");
scene.add(new THREE.HemisphereLight("#ffffff", "#334", 2.2));
const sun = new THREE.DirectionalLight("#ffffff", 2.0); sun.position.set(-60, 150, 80); scene.add(sun);
window.__preview = (pos, tgt, fov = 40) => {
  const cam = new THREE.PerspectiveCamera(fov, 1080 / 1920, 1, 3000);
  cam.position.set(...pos); cam.lookAt(...tgt);
  renderer.render(scene, cam);
};
window.__preview([20, 220, 120], [20, 0, 0]);
window.__ready = true;
