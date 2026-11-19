/* ESP32 From Zero - 3D kit (three.js), shared by every episode's 3D clips.
 * Stylized look (PRODUCTION_GUIDELINES 12.6): toon shading + thin outlines, brand colors, orthographic camera.
 * Every frame is a pure function of t: lib.js calls window.__seek(t) -> dyn() -> the episode's apply(t).
 *
 * Units: 1 = 1 mm. Breadboards stand VERTICAL like the creator's desk: row numbers 1..63 run along -z (row 1 at the
 * bottom of the picture, row 63 at the top), letters a..j run along +x (a on the left). Two boards side by side,
 * the ESP32 straddles them with the USB end down. Coordinates are printed on the boards (numbers + letters) and on
 * the ESP32 (pin names), so a viewer can copy every connection.
 *
 *   const K = makeKit({ pixelRatio: 2 });
 *   const L = K.breadboard(-28), R = K.breadboard(28);          // board centre x
 *   K.esp32({ row0: 18 });                                        // pin 1 (EN / D23) on row 18, USB toward row 1
 *   K.led(R, 21, 22, "h", "red");  K.resistor(R.hole(18, "d"), R.hole(21, "g"));  K.wire([...], color)
 */
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

export const P = 2.54;
export const clamp01 = (x) => Math.min(1, Math.max(0, x));
export const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
export const smoother = (x) => { x = clamp01(x); return x * x * x * (x * (x * 6 - 15) + 10); };
export const backOut = (x) => { x = clamp01(x); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2; };
export const lerp = (a, b, k) => a + (b - a) * k;
export const V = (x, y, z) => new THREE.Vector3(x, y, z);

export const COL = {
  bg: "#0b1220", amber: "#ffb547", teal: "#3ad2c3",
  wireRed: "#e5484d", wireBlack: "#23262d", wireYellow: "#ffd34d", wireGreen: "#33c46e", wireBlue: "#4d8dff", wireOrange: "#ff8a2a",
};
// lamp colours: body tint, emissive, glow tint
export const LAMP = {
  red: { body: "#c8242a", emit: "#ff3a30", glow: "#ff5a4a" },
  yellow: { body: "#d9a514", emit: "#ffd23a", glow: "#ffd860" },
  green: { body: "#1f9a3a", emit: "#22ff3a", glow: "#3dff55" },
};

const BB = { w: 55, len: 165, h: 9 };
// x offset of each letter from the board centre, rails: (-) outer, (+) inner on both edges
export const LETTER = { a: -15.24, b: -12.7, c: -10.16, d: -7.62, e: -5.08, f: 5.08, g: 7.62, h: 10.16, i: 12.7, j: 15.24 };
export const RAILX = { lminus: -24.14, lplus: -21.6, rplus: 21.6, rminus: 24.14 };
const railHole = (n) => n % 6 !== 0; // rail holes come in groups of five

export function makeKit(opts = {}) {
  const pr = opts.pixelRatio || 2;
  const canvas = document.getElementById("c3d");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(pr); // drawn at 2x, the page shows it at 1x: supersampled, clean edges
  renderer.setSize(1920, 1080, false);
  canvas.style.width = "1920px"; canvas.style.height = "1080px";
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const maxAniso = renderer.capabilities.getMaxAnisotropy();

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(COL.bg);

  const ramp = new THREE.DataTexture(new Uint8Array([92, 92, 92, 255, 170, 170, 170, 255, 236, 236, 236, 255, 255, 255, 255, 255]), 4, 1, THREE.RGBAFormat);
  ramp.minFilter = ramp.magFilter = THREE.NearestFilter;
  ramp.needsUpdate = true;

  const parts = []; // everything placed on the boards, in creation order (for build montages)
  const MATS = {};
  const mat = (name, color, extra = {}) => MATS[name] || (MATS[name] = Object.assign(new THREE.MeshToonMaterial({ color, gradientMap: ramp, ...extra }), { name }));
  const lineMat = new THREE.LineBasicMaterial({ color: "#070b14", transparent: true, opacity: 0.55 });

  function add(parent, geo, m, pos, o = {}) {
    const mesh = new THREE.Mesh(geo, m);
    mesh.position.set(pos[0], pos[1], pos[2]);
    if (o.rot) mesh.rotation.set(o.rot[0], o.rot[1], o.rot[2]);
    mesh.castShadow = o.cast ?? true;
    mesh.receiveShadow = o.recv ?? true;
    if (o.edges !== false) mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo, o.edgeAngle ?? 35), lineMat));
    parent.add(mesh);
    return mesh;
  }
  /** registers a part; reveal(k) pops it in (scale) or drops it from above (the ESP32) */
  function part(o) {
    const g = o.group, base = g.position.y;
    o.reveal = (k) => {
      k = clamp01(k);
      g.visible = k > 0.001;
      if (o.drop) { g.position.y = base + (1 - backOut(k)) * 60; return; }
      g.scale.setScalar(Math.max(0.001, backOut(k)));
    };
    parts.push(o);
    return o;
  }
  function canvasTex(w, h, draw) {
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = maxAniso;
    t.generateMipmaps = true;
    t.minFilter = THREE.LinearMipmapLinearFilter;
    return t;
  }
  const glowTex = canvasTex(256, 256, (g, w) => {
    const r = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2);
    r.addColorStop(0, "rgba(255,255,255,1)"); r.addColorStop(0.22, "rgba(255,255,255,.5)"); r.addColorStop(1, "rgba(255,255,255,0)");
    g.fillStyle = r; g.fillRect(0, 0, w, w);
  });

  /* ---------------- desk + lights ---------------- */
  const deskTex = canvasTex(1024, 1024, (g, w, h) => {
    const r = g.createRadialGradient(w / 2, h / 2, 10, w / 2, h / 2, w / 2);
    r.addColorStop(0, "#1d2b48"); r.addColorStop(0.6, "#121c31"); r.addColorStop(1, "#0b1220");
    g.fillStyle = r; g.fillRect(0, 0, w, h);
  });
  const desk = new THREE.Mesh(new THREE.PlaneGeometry(900, 900), new THREE.MeshBasicMaterial({ map: deskTex }));
  desk.rotation.x = -Math.PI / 2;
  desk.position.z = -20;
  scene.add(desk);
  const catcher = new THREE.Mesh(new THREE.PlaneGeometry(900, 900), new THREE.ShadowMaterial({ opacity: 0.45, color: "#02040a" }));
  catcher.rotation.x = -Math.PI / 2;
  catcher.position.set(0, 0.02, -20);
  catcher.receiveShadow = true;
  scene.add(catcher);

  scene.add(new THREE.HemisphereLight("#d6e6ff", "#1a2238", 0.95));
  const sun = new THREE.DirectionalLight("#fff6ea", 1.45);
  sun.position.set(-90, 200, 120);
  sun.target.position.set(0, 0, -20);
  scene.add(sun.target);
  sun.castShadow = true;
  sun.shadow.mapSize.set(4096, 4096);
  Object.assign(sun.shadow.camera, { left: -140, right: 140, top: 140, bottom: -140, near: 10, far: 600 });
  sun.shadow.bias = -0.0003;
  sun.shadow.normalBias = 0.12;
  sun.shadow.radius = 3;
  scene.add(sun);

  /* ---------------- breadboard (printed numbers + letters, like the real one) ---------------- */
  const PXMM = 40; // texture pixels per mm: sharp even in close-ups
  const bbTex = canvasTex(BB.w * PXMM, BB.len * PXMM, (g, w, h) => {
    const X = (mm) => (mm + BB.w / 2) * PXMM, Z = (mm) => (mm + BB.len / 2) * PXMM;
    g.fillStyle = "#efeee9"; g.fillRect(0, 0, w, h);
    // centre groove
    g.fillStyle = "#d8d5cc"; g.fillRect(X(-1.6), Z(-80), 3.2 * PXMM, 160 * PXMM);
    const hole = (x, z) => {
      const s = 1.3 * PXMM;
      g.fillStyle = "#c9c6bd"; g.fillRect(X(x) - s / 2 - 5, Z(z) - s / 2 - 5, s + 10, s + 10);
      g.fillStyle = "#3d3b36"; g.fillRect(X(x) - s / 2, Z(z) - s / 2, s, s);
    };
    for (let n = 1; n <= 63; n++) {
      const z = (32 - n) * P;
      for (const x of Object.values(LETTER)) hole(x, z);
      if (railHole(n)) for (const x of Object.values(RAILX)) hole(x, z);
      // row numbers on both sides; every 5th bigger and darker (like the printed board)
      const big = n % 5 === 0 || n === 1;
      g.font = `${big ? 800 : 600} ${big ? 1.75 * PXMM : 1.35 * PXMM}px Segoe UI`;
      g.fillStyle = big ? "#3c4250" : "#7d8494";
      g.textAlign = "center"; g.textBaseline = "middle";
      for (const x of [-18.6, 18.6]) g.fillText(String(n), X(x), Z(z) + 2);
    }
    // letters a..j at both ends
    g.font = `800 ${1.9 * PXMM}px Segoe UI`; g.fillStyle = "#3c4250";
    for (const [l, x] of Object.entries(LETTER)) for (const z of [(32 - 0.15) * P + 0.3, -(32 - 0.15) * P - 0.3]) g.fillText(l, X(x), Z(z > 0 ? 80.9 : -80.9));
    // rail stripes and signs
    for (const [x, col] of [[-26.0, "#3b6fe0"], [-19.75, "#e5484d"], [19.75, "#e5484d"], [26.0, "#3b6fe0"]]) {
      g.fillStyle = col; g.fillRect(X(x) - 0.28 * PXMM, Z(-79), 0.56 * PXMM, 158 * PXMM);
    }
    g.font = `900 ${2.4 * PXMM}px Segoe UI`;
    for (const z of [-73, 0, 73]) {
      g.fillStyle = "#3b6fe0"; g.fillText("−", X(-24.14), Z(z) + (z === 0 ? 0 : 0)); g.fillText("−", X(24.14), Z(z));
      g.fillStyle = "#e5484d"; g.fillText("+", X(-21.6), Z(z)); g.fillText("+", X(21.6), Z(z));
    }
  });
  const bbTopMat = new THREE.MeshToonMaterial({ map: bbTex, gradientMap: ramp });
  const ROW_Z = (n) => 0; // replaced per board below
  function breadboard(xc, o = {}) {
    const g = new THREE.Group();
    const zc = o.zc ?? 0; // world z of the board centre
    g.position.set(xc, 0, zc);
    scene.add(g);
    add(g, new RoundedBoxGeometry(BB.w, BB.h, BB.len, 3, 1.2), mat("bbside", "#e4e2db"), [0, BB.h / 2 - 0.01, 0], { edgeAngle: 60 });
    const topPl = new THREE.Mesh(new THREE.PlaneGeometry(BB.w - 1.2, BB.len - 1.2), bbTopMat);
    topPl.rotation.x = -Math.PI / 2;
    topPl.position.y = BB.h + 0.01;
    topPl.receiveShadow = true;
    // uv: map the 1.2 mm smaller plane onto the matching part of the texture
    const uv = topPl.geometry.attributes.uv;
    for (let i = 0; i < uv.count; i++) uv.setXY(i, 0.6 / BB.w + uv.getX(i) * (1 - 1.2 / BB.w), 0.6 / BB.len + uv.getY(i) * (1 - 1.2 / BB.len));
    g.add(topPl);
    const zOf = (n) => zc + (32 - n) * P;
    return {
      group: g, x: xc,
      /** world position of hole <n><letter>, on the top surface */
      hole: (n, l) => [xc + LETTER[l], BB.h, zOf(n)],
      /** world position of a rail hole: side "l"/"r", sign "+"/"-" */
      rail: (n, side, sign) => {
        if (!railHole(n)) throw new Error("no rail hole at row " + n);
        return [xc + RAILX[(side === "l" ? "l" : "r") + (sign === "+" ? "plus" : "minus")], BB.h, zOf(n)];
      },
      zOf,
    };
  }
  const TOP = BB.h;

  /* ---------------- ESP32 DevKit, 30 pins, pin names printed ---------------- */
  const RIGHT_PINS = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"];
  const LEFT_PINS = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"];
  /** board: the ESP32 between two breadboards; pin 1 of both rows sits on row0, the pins go down to row0-14.
   *  rows: left pin row x, right pin row x. hot: pin names drawn in amber (used in this episode). */
  function esp32(o) {
    const xl = o.xl, xr = o.xr, z0 = o.z0; // world z of the first pin (EN / D23)
    const xc = (xl + xr) / 2, half = (xr - xl) / 2;
    const g = new THREE.Group();
    g.name = "esp32";
    scene.add(g);
    const pcbY = TOP + 2.5, pcbTop = pcbY + 1.6;
    const zA = z0 - 8.94, zU = zA + 51.5; // antenna edge, USB edge
    const W = 2 * half + 2.9;
    add(g, new RoundedBoxGeometry(W, 1.6, 51.5, 2, 0.6), mat("pcb", "#1b2029"), [xc, pcbY + 0.8, (zA + zU) / 2], { edgeAngle: 60 });
    for (const x of [xl, xr]) add(g, new THREE.BoxGeometry(2.5, 2.5, 15 * P), mat("header", "#15181d"), [x, TOP + 1.25, z0 + 7 * P]);
    // gold pads + pins
    const pad = new THREE.BoxGeometry(1.9, 0.06, 1.9), post = new THREE.BoxGeometry(0.64, 1.4, 0.64);
    const padsM = new THREE.InstancedMesh(pad, mat("gold", "#e0b84a"), 30), postM = new THREE.InstancedMesh(post, mat("gold", "#e0b84a"), 30);
    const M = new THREE.Matrix4();
    let k = 0;
    for (let i = 0; i < 15; i++) for (const x of [xl, xr]) {
      padsM.setMatrixAt(k, M.makeTranslation(x, pcbTop + 0.02, z0 + i * P));
      postM.setMatrixAt(k++, M.makeTranslation(x, pcbTop + 0.7, z0 + i * P));
    }
    postM.castShadow = true;
    g.add(padsM, postM);
    // module with shield + antenna, at the far (top) end
    const modLen = 25.5, modZ = zA + 0.4 + modLen / 2, modW = 2 * half - 9.5;
    add(g, new THREE.BoxGeometry(modW, 0.8, modLen), mat("module", "#24384f"), [xc, pcbTop + 0.4, modZ]);
    const shZ = zA + 0.4 + 6.3 + 17.8 / 2;
    add(g, new RoundedBoxGeometry(modW - 2.4, 2.4, 17.8, 2, 0.35), mat("shield", "#c9d1db"), [xc, pcbTop + 2.0, shZ], { edgeAngle: 60 });
    const lab = new THREE.Mesh(new THREE.PlaneGeometry(modW - 4, 9), new THREE.MeshBasicMaterial({
      transparent: true,
      map: canvasTex(640, 360, (c, w, h) => {
        c.fillStyle = "#59626d"; c.textAlign = "center";
        c.font = "800 70px Segoe UI"; c.fillText("ESP32", w / 2, 150);
        c.font = "600 44px Segoe UI"; c.fillText("WROOM-32", w / 2, 222);
      }),
    }));
    lab.rotation.x = -Math.PI / 2;
    lab.position.set(xc, pcbTop + 3.22, shZ);
    g.add(lab);
    for (let s = 0; s < 6; s++) {
      const x = xc - (modW - 4) / 2 + 1.2 + s * ((modW - 6.4) / 5);
      add(g, new THREE.BoxGeometry(0.45, 0.06, 4.0), mat("gold", "#e0b84a"), [x, pcbTop + 0.83, zA + 3.0], { edges: false, cast: false });
    }
    // USB, chips, buttons, power LED at the near (bottom) end
    add(g, new RoundedBoxGeometry(7.8, 2.8, 5.8, 2, 0.4), mat("usb", "#d5dbe2"), [xc, pcbTop + 1.4, zU - 1.9]);
    add(g, new THREE.BoxGeometry(5, 1, 5), mat("ic", "#121418"), [xc + 4.5, pcbTop + 0.5, zU - 12]);
    add(g, new THREE.BoxGeometry(6.5, 1.6, 3.6), mat("ic", "#121418"), [xc - 5.0, pcbTop + 0.8, zU - 13]);
    for (const dx of [-9.0, 9.0]) {
      add(g, new THREE.BoxGeometry(3.6, 1.3, 4), mat("button", "#cfd5dc"), [xc + dx, pcbTop + 0.65, zU - 5.5]);
      add(g, new THREE.CylinderGeometry(1.1, 1.1, 0.8, 20), mat("ic", "#121418"), [xc + dx, pcbTop + 1.6, zU - 5.5], { edges: false });
    }
    const pwr = new THREE.MeshToonMaterial({ color: "#5a1a1a", gradientMap: ramp, emissive: "#ff2a2a", emissiveIntensity: 2.0 });
    add(g, new THREE.BoxGeometry(1, 0.7, 1.6), pwr, [xc - 2.2, pcbTop + 0.35, zU - 9.5], { edges: false });
    // printed pin names, upright for the camera (it looks from the USB end), amber = used in this video
    const hot = new Set(o.hot || []);
    const SPAN = 51.5, Wd = W;
    const tex = canvasTex(Math.round(Wd * 60), Math.round(SPAN * 60), (c, w, h) => {
      const X = (x) => (x - (xc - Wd / 2)) * 60, Z = (z) => (z - zA) * 60;
      c.textBaseline = "middle";
      for (let i = 0; i < 15; i++) {
        for (const [names, x, align] of [[LEFT_PINS, xl + 1.55, "left"], [RIGHT_PINS, xr - 1.55, "right"]]) {
          const nm = names[i], on = hot.has(nm);
          c.font = `${on ? 900 : 700} ${on ? 1.75 * 60 : 1.45 * 60}px Segoe UI`;
          c.textAlign = align;
          c.fillStyle = on ? "#ffb547" : "#c7cfdb";
          c.fillText(nm, X(x), Z(z0 + i * P) + 3);
        }
      }
    });
    const names = new THREE.Mesh(new THREE.PlaneGeometry(Wd, SPAN), new THREE.MeshBasicMaterial({ map: tex, transparent: true }));
    names.rotation.x = -Math.PI / 2;
    names.position.set(xc, pcbTop + 0.03, (zA + zU) / 2);
    g.add(names);
    const power = (on) => { pwr.emissiveIntensity = on ? 2.0 : 0; };
    return part({ group: g, pcbTop, drop: true, power, xc, pin: (side, i) => [side === "l" ? xl : xr, pcbTop + 1.4, z0 + i * P]  , zA, zU });
  }

  /** micro-USB cable plugged into the board's USB end; set(k): 0 = plugged in, 1 = pulled out (~18 mm) */
  function usbCable(e) {
    const g = new THREE.Group();
    scene.add(g);
    const y = e.pcbTop + 1.4, z = e.zU;
    add(g, new RoundedBoxGeometry(10.5, 6.2, 13, 2, 1.6), mat("usbplug", "#2a2e36"), [e.xc, y, z + 7.2]);
    add(g, new THREE.BoxGeometry(7, 2.2, 3), mat("usbmetal", "#c9d0d8"), [e.xc, y, z + 0.6]);
    const curve = new THREE.CatmullRomCurve3([V(e.xc, y, z + 13), V(e.xc, y + 1.2, z + 30), V(e.xc + 4, y - 2, z + 48), V(e.xc + 12, 1.6, z + 80), V(e.xc + 24, 1.6, z + 160)]);
    add(g, new THREE.TubeGeometry(curve, 60, 2.0, 12), mat("usbcord", "#2a2e36"), [0, 0, 0], { edges: false });
    return { group: g, top: [e.xc, y + 4, z + 8], set(k) { g.position.z = 18 * smooth(k); } };
  }

  /* ---------------- lamps ---------------- */
  function glowSprite(parent, color, y) {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0 }));
    s.position.set(0, y, 0);
    parent.add(s);
    return s;
  }
  /** a 5 mm LED: long leg (+) at hole a, short leg (-) at hole b (same letter, neighbouring rows) */
  function led(a, b, kind) {
    const C = LAMP[kind];
    const g = new THREE.Group();
    const mx = (a[0] + b[0]) / 2, mz = (a[2] + b[2]) / 2;
    g.position.set(mx, 0, mz);
    g.rotation.y = Math.atan2(b[0] - a[0], b[2] - a[2]); // legs along the local z axis
    scene.add(g);
    const y0 = TOP + 3.6;
    const body = new THREE.MeshToonMaterial({ color: C.body, gradientMap: ramp, emissive: C.emit, emissiveIntensity: 0, transparent: true, opacity: 0.97 });
    const prof = [V(0.01, 0, 0), V(2.9, 0, 0), V(2.9, 1, 0), V(2.5, 1, 0), V(2.5, 5.2, 0)];
    for (let k = 1; k <= 12; k++) { const q = (k / 12) * Math.PI / 2; prof.push(V(2.5 * Math.cos(q) + 0.001, 5.2 + 2.5 * Math.sin(q), 0)); }
    add(g, new THREE.LatheGeometry(prof.map((p) => new THREE.Vector2(p.x, p.y)), 48), body, [0, y0, 0], { edgeAngle: 40 });
    const half = Math.hypot(b[0] - a[0], b[2] - a[2]) / 2;
    for (const [dz, len] of [[-half, y0 - TOP + 0.4], [half, y0 - TOP + 0.4]])
      add(g, new THREE.CylinderGeometry(0.25, 0.25, len, 8), mat("lead", "#b8bec6"), [0, TOP + len / 2 - 0.4, dz], { edges: false });
    const glow = glowSprite(g, C.glow, y0 + 5.0);
    const light = new THREE.PointLight(C.emit, 0, 40, 1.8);
    light.position.set(0, y0 + 6, 0);
    g.add(light);
    return part({
      group: g, top: [mx, y0 + 8.5, mz],
      set(on) { // on: 0..1
        const v = Math.pow(clamp01(on), 0.7);
        body.emissiveIntensity = v > 0.001 ? 0.2 + 0.9 * v : 0;
        glow.material.opacity = 0.5 * v;
        glow.scale.setScalar(7 + 6 * v);
        light.intensity = 45 * v;
      },
    });
  }
  /** RGB LED, common cathode: legs R, -, G, B in four neighbouring rows (holes given in that order) */
  function rgbLed(holes) {
    const g = new THREE.Group();
    const mx = holes.reduce((s, h) => s + h[0], 0) / 4, mz = holes.reduce((s, h) => s + h[2], 0) / 4;
    g.position.set(mx, 0, mz);
    scene.add(g);
    const y0 = TOP + 4.0;
    const body = new THREE.MeshToonMaterial({ color: "#e9eef6", gradientMap: ramp, emissive: "#000000", emissiveIntensity: 0, transparent: true, opacity: 0.93 });
    const prof = [V(0.01, 0, 0), V(3.0, 0, 0), V(3.0, 1, 0), V(2.6, 1, 0), V(2.6, 5.6, 0)];
    for (let k = 1; k <= 12; k++) { const q = (k / 12) * Math.PI / 2; prof.push(V(2.6 * Math.cos(q) + 0.001, 5.6 + 2.6 * Math.sin(q), 0)); }
    add(g, new THREE.LatheGeometry(prof.map((p) => new THREE.Vector2(p.x, p.y)), 48), body, [0, y0, 0], { edgeAngle: 40 });
    holes.forEach((h, i) => {
      const x = h[0] - mx, z = h[2] - mz, len = y0 - TOP + 0.4;
      const leg = new THREE.CatmullRomCurve3([V(x, TOP - 0.4, z), V(x, TOP + 1.2, z), V(x * 0.3, y0 - 0.4, z * 0.25), V(x * 0.25, y0 + 0.4, z * 0.2)]);
      add(g, new THREE.TubeGeometry(leg, 12, i === 1 ? 0.3 : 0.25, 6), mat("lead", "#b8bec6"), [0, 0, 0], { edges: false });
    });
    const glow = glowSprite(g, "#ffffff", y0 + 5.5);
    const light = new THREE.PointLight("#ffffff", 0, 40, 1.8);
    light.position.set(0, y0 + 6.5, 0);
    g.add(light);
    const tmp = new THREE.Color();
    return part({
      group: g, top: [mx, y0 + 9, mz],
      set(r, gr, b) { // 0..1 each
        const v = Math.max(r, gr, b);
        tmp.setRGB(r, gr, b);
        body.emissive.copy(tmp);
        body.emissiveIntensity = v > 0.001 ? 1.0 : 0;
        body.color.set(v > 0.001 ? tmp.clone().lerp(new THREE.Color("#ffffff"), 0.12) : new THREE.Color("#e9eef6"));
        glow.material.color.copy(tmp);
        glow.material.opacity = 0.55 * v;
        glow.scale.setScalar(8 + 7 * v);
        light.color.copy(tmp);
        light.intensity = 50 * v;
      },
    });
  }

  /* ---------------- resistor (220 ohm: red red brown gold) between two holes ---------------- */
  function resistor(a, b) {
    const g = new THREE.Group();
    const mx = (a[0] + b[0]) / 2, mz = (a[2] + b[2]) / 2;
    g.position.set(mx, 0, mz);
    g.rotation.y = Math.atan2(b[0] - a[0], b[2] - a[2]);
    scene.add(g);
    const L = Math.hypot(b[0] - a[0], b[2] - a[2]), RY = TOP + 2.4;
    add(g, new THREE.CapsuleGeometry(1.15, 3.6, 6, 18), mat("resistor", "#d9c49c"), [0, RY, 0], { rot: [Math.PI / 2, 0, 0], edgeAngle: 50 });
    [["#d4352f", -1.35], ["#d4352f", -0.55], ["#6b3a1e", 0.25], ["#c9a54a", 1.45]].forEach(([c, dz], i) =>
      add(g, new THREE.CylinderGeometry(1.2, 1.2, 0.42, 18), mat("band" + i, c), [0, RY, dz], { rot: [Math.PI / 2, 0, 0], edges: false }));
    for (const s of [-1, 1]) {
      const zEnd = s * L / 2;
      const lead = new THREE.CatmullRomCurve3([V(0, RY, s * 2.6), V(0, RY, zEnd - s * 0.7), V(0, RY - 0.9, zEnd), V(0, TOP - 0.3, zEnd)]);
      add(g, new THREE.TubeGeometry(lead, 16, 0.25, 6), mat("lead", "#b8bec6"), [0, 0, 0], { edges: false });
    }
    return part({ group: g, mid: [mx, RY + 1.2, mz], kind: "resistor" });
  }

  /* ---------------- jumper wire: hole -> hole, arched; via = extra waypoints [x, z] (height = arch) ---------------- */
  function wire(a, b, color, o = {}) {
    const h = o.h ?? Math.min(9, 3.5 + Math.hypot(b[0] - a[0], b[2] - a[2]) * 0.07);
    const pts = [V(a[0], TOP - 0.6, a[2]), V(a[0], TOP + h * 0.55, a[2])];
    const dx = b[0] - a[0], dz = b[2] - a[2], d = Math.hypot(dx, dz) || 1;
    const lift = Math.min(2.4, d * 0.3);
    if (o.via) for (const [x, z] of o.via) pts.push(V(x, TOP + h, z));
    else {
      pts.push(V(a[0] + dx * lift / d, TOP + h, a[2] + dz * lift / d));
      pts.push(V(b[0] - dx * lift / d, TOP + h, b[2] - dz * lift / d));
    }
    pts.push(V(b[0], TOP + h * 0.55, b[2]), V(b[0], TOP - 0.6, b[2]));
    const curve = new THREE.CatmullRomCurve3(pts, false, "centripetal", 0.5);
    const geo = new THREE.TubeGeometry(curve, Math.max(60, Math.round(d * 2)), 0.62, 10);
    const m = new THREE.MeshToonMaterial({ color, gradientMap: ramp, emissive: color, emissiveIntensity: 0 });
    const g = new THREE.Group();
    scene.add(g);
    const mesh = add(g, geo, m, [0, 0, 0], { edges: false });
    // metal pins at both ends
    const ends = [a, b].map((p) => add(g, new THREE.CylinderGeometry(0.72, 0.72, 2.2, 10), mat("wireend", "#2c2f36"), [p[0], TOP + 1.4, p[2]], { edges: false }));
    const total = geo.index.count;
    const w = {
      group: g, mesh, mat: m, mid: curve.getPoint(0.5).toArray(), kind: "wire",
      /** k: 0..1 how much of the wire is drawn (build animations) */
      reveal(k) {
        k = clamp01(k);
        geo.setDrawRange(0, Math.floor((total / 6) * k) * 6);
        g.visible = k > 0.001; ends[0].visible = k > 0.001; ends[1].visible = k > 0.98;
      },
    };
    parts.push(w);
    return w;
  }

  /* ---------------- push button (12 mm), legs at 4 holes ---------------- */
  function button(holes) {
    const mx = holes.reduce((s, h) => s + h[0], 0) / 4, mz = holes.reduce((s, h) => s + h[2], 0) / 4;
    const g = new THREE.Group();
    g.position.set(mx, 0, mz);
    scene.add(g);
    add(g, new RoundedBoxGeometry(12, 3.4, 12, 2, 0.5), mat("btnbase", "#2a2d33"), [0, TOP + 1.7, 0]);
    for (const [x, z] of [[-4.5, -4.5], [4.5, -4.5], [-4.5, 4.5], [4.5, 4.5]]) add(g, new THREE.CylinderGeometry(0.6, 0.6, 0.4, 12), mat("btndot", "#8c929b"), [x, TOP + 3.45, z], { edges: false });
    add(g, new THREE.BoxGeometry(9.6, 0.5, 9.6), mat("btnplate", "#a8afb8"), [0, TOP + 3.5, 0]);
    const cap = add(g, new THREE.CylinderGeometry(3.4, 3.6, 3.2, 32), mat("btncap", "#15171a"), [0, TOP + 5.3, 0], { edgeAngle: 50 });
    holes.forEach((h) => add(g, new THREE.BoxGeometry(0.7, 1.4, 0.4), mat("lead", "#b8bec6"), [h[0] - mx, TOP + 0.5, h[2] - mz], { edges: false }));
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.82, 1, 64), new THREE.MeshBasicMaterial({ color: COL.amber, transparent: true, opacity: 0, depthWrite: false, depthTest: false }));
    ring.rotation.x = -Math.PI / 2;
    ring.position.set(0, TOP + 7.2, 0);
    g.add(ring);
    return part({
      group: g, top: [mx, TOP + 7, mz], legs: holes.length,
      /** p: 0 up .. 1 fully pressed; pulse: 0..1 progress of the ring after a press (or <0 = none) */
      set(p, pulse = -1) {
        cap.position.y = TOP + 5.3 - 1.1 * clamp01(p);
        if (pulse >= 0 && pulse <= 1) { ring.material.opacity = 0.9 * (1 - pulse); ring.scale.setScalar(5 + 9 * smooth(pulse)); }
        else ring.material.opacity = 0;
      },
    });
  }

  /* ---------------- potentiometer, three legs (left, wiper, right) in a column ---------------- */
  function pot(holes, angle = 0) {
    const mx = holes.reduce((s, h) => s + h[0], 0) / 3, mz = holes.reduce((s, h) => s + h[2], 0) / 3;
    const g = new THREE.Group();
    g.position.set(mx - 4.2, 0, mz);
    scene.add(g);
    add(g, new RoundedBoxGeometry(9.5, 7, 12.5, 2, 0.6), mat("potbody", "#2f5fd0"), [0, TOP + 3.6, 0]);
    add(g, new THREE.CylinderGeometry(3.6, 3.6, 1.6, 32), mat("potneck", "#c9ced6"), [0, TOP + 7.9, 0]);
    const knob = add(g, new THREE.CylinderGeometry(3.0, 3.0, 6.5, 32), mat("potknob", "#e4e7ec"), [0, TOP + 11.6, 0], { edgeAngle: 50 });
    const mark = add(g, new THREE.BoxGeometry(0.6, 0.3, 2.4), mat("potmark", "#3a4250"), [0, TOP + 14.9, -1.4], { edges: false });
    holes.forEach((h) => add(g, new THREE.BoxGeometry(0.5, 1.6, 0.9), mat("lead", "#b8bec6"), [h[0] - (mx - 4.2), TOP + 0.6, h[2] - mz], { edges: false }));
    const set = (a) => { knob.rotation.y = a; mark.position.set(-1.4 * Math.sin(a), TOP + 14.9, -1.4 * Math.cos(a)); mark.rotation.y = a; };
    set(angle);
    return part({ group: g, top: [mx - 4.2, TOP + 15, mz], set });
  }

  /* ---------------- post + camera ---------------- */
  const rt = new THREE.WebGLRenderTarget(1920 * pr, 1080 * pr, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, rt);
  composer.setPixelRatio(pr);
  composer.setSize(1920, 1080);
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 1, 4000);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(1920, 1080), 0.42, 0.4, 1.05);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());

  /** camera state: th = turn around y (deg, 0 = from the USB end / row 1 side), el = height (deg), hh = half
   *  height of the picture in mm (zoom), tx/ty/tz = the point in the middle of the picture */
  function placeCamera(c) {
    const th = (c.th * Math.PI) / 180, el = (c.el * Math.PI) / 180, R = 1200;
    const tg = V(c.tx, c.ty, c.tz);
    camera.position.set(tg.x + R * Math.cos(el) * Math.sin(th), tg.y + R * Math.sin(el), tg.z + R * Math.cos(el) * Math.cos(th));
    camera.up.set(0, 1, 0);
    camera.lookAt(tg);
    const a = 1920 / 1080;
    Object.assign(camera, { left: -c.hh * a, right: c.hh * a, top: c.hh, bottom: -c.hh });
    camera.updateProjectionMatrix();
    camera.updateMatrixWorld(true); // tags project with this frame's camera, not the last one
  }
  /** keys: [[t, {th, el, hh, tx, ty, tz}], ...]; eased moves between keys, holds drift slowly (never a dead frame) */
  function camPath(keys) {
    return (t) => {
      if (t <= keys[0][0]) return { ...keys[0][1] };
      let i = 0;
      while (i < keys.length - 2 && t >= keys[i + 1][0]) i++;
      const [t0, a] = keys[i], [t1, b] = keys[i + 1];
      const k = smoother((t - t0) / (t1 - t0));
      const c = {};
      for (const key of Object.keys(a)) c[key] = lerp(a[key], b[key] ?? a[key], k);
      return c;
    };
  }
  /** a point between parts, for camera targets */
  const centre = (...ps) => ps.reduce((s, p) => [s[0] + p[0] / ps.length, s[1] + p[1] / ps.length, s[2] + p[2] / ps.length], [0, 0, 0]);
  function toScreen(p) {
    const v = V(p[0], p[1], p[2]).project(camera);
    return { x: (v.x * 0.5 + 0.5) * 1920, y: (-v.y * 0.5 + 0.5) * 1080, behind: v.z > 1 };
  }
  const render = () => composer.render();
  return { parts, usbCable, THREE, scene, renderer, mat, add, canvasTex, breadboard, esp32, led, rgbLed, resistor, wire, button, pot, placeCamera, camPath, centre, toScreen, render, TOP };
}

/* ---------------- 2D tags that follow 3D points (engine overlay, crisp text) ----------------
 * tag(ui, html, cls) -> { el, at(p3d, toScreen) }; style comes from engine3d/kit.css */
export function makeTag(ui, html, cls = "") {
  const e = document.createElement("div");
  e.className = "tag3d " + cls;
  e.innerHTML = html;
  e.style.opacity = 0;
  ui.appendChild(e);
  return {
    el: e,
    at(p, toScreen, dy = 0) { const s = toScreen(p); e.style.left = s.x + "px"; e.style.top = s.y + dy + "px"; },
  };
}
