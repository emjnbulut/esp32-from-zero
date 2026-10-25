/* Breadboard drawing (top view): breadboard, ESP32 board lying across the gap, wires, resistor, LED.
 * Extracted from ep02.js so later episodes can reuse it. Needs lib.js (box, css, TO, ...). */
const NS = "http://www.w3.org/2000/svg";
function svgEl(parent, tag, attrs = {}) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  parent.appendChild(e);
  return e;
}
function svgLayer(parent, w = 1920, h = 1080) {
  const s = svgEl(parent, "svg", { width: w, height: h, viewBox: `0 0 ${w} ${h}` });
  css(s, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  return s;
}
/** draw a path on over [t, t+dur] */
function drawOn(path, t, dur = 0.6) {
  const L = path.getTotalLength();
  path.setAttribute("stroke-dasharray", `${L} ${L}`);
  path.style.strokeDashoffset = L;
  TO(path, t, dur, { strokeDashoffset: 0, ease: "power2.out" });
}
const clamp01 = (v) => Math.max(0, Math.min(1, v));

const P = 42;
const ROWS = { tp: 0, tm: 1, a: 2.5, b: 3.5, c: 4.5, d: 5.5, e: 6.5, f: 9.5, g: 10.5, h: 11.5, i: 12.5, j: 13.5, bp: 15, bm: 16 };
const MID = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"];
function makeBB(parent, x, y, cols = 30) {
  const mx = 58, my = 50, w = mx * 2 + (cols - 1) * P, h = my * 2 + 16 * P;
  const root = box(parent, x, y, w, h, "");
  const svg = svgEl(root, "svg", { width: w, height: h, viewBox: `0 0 ${w} ${h}` });
  css(svg, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  const L = (c, r) => [mx + (c - 1) * P, my + ROWS[r] * P];
  const S = (c, r) => { const [lx, ly] = L(c, r); return [x + lx, y + ly]; };
  const defs = svgEl(svg, "defs");
  defs.innerHTML = `<linearGradient id="bbshield" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9edf2"/><stop offset=".5" stop-color="#b9c0c9"/><stop offset="1" stop-color="#d9dee5"/></linearGradient>
    <radialGradient id="ledglow"><stop offset="0" stop-color="#ff6b6b" stop-opacity=".95"/><stop offset=".35" stop-color="#ff4d4d" stop-opacity=".55"/><stop offset="1" stop-color="#ff3030" stop-opacity="0"/></radialGradient>
    <radialGradient id="ledglowG"><stop offset="0" stop-color="#7dffb0" stop-opacity=".95"/><stop offset=".35" stop-color="#3ee887" stop-opacity=".55"/><stop offset="1" stop-color="#20d070" stop-opacity="0"/></radialGradient>`;
  svgEl(svg, "rect", { x: 0, y: 0, width: w, height: h, rx: 20, fill: "#ecebe6", stroke: "#c9c6bd", "stroke-width": 2 });
  const gy = my + (ROWS.e + ROWS.f) / 2 * P;
  const groove = svgEl(svg, "rect", { x: 12, y: gy - 15, width: w - 24, height: 30, rx: 7, fill: "#d6d3cb" });
  // rail markings: red line on the + side, blue on the - side
  const railY = { tp: my + ROWS.tp * P, tm: my + ROWS.tm * P, bp: my + ROWS.bp * P, bm: my + ROWS.bm * P };
  const marks = svgEl(svg, "g", {});
  for (const [r, dy, col] of [["tp", -0.55, "#e5484d"], ["tm", 0.55, "#3b6fe0"], ["bp", -0.55, "#e5484d"], ["bm", 0.55, "#3b6fe0"]]) {
    svgEl(marks, "path", { d: `M${mx - 10} ${railY[r] + dy * P} H${w - mx + 10}`, stroke: col, "stroke-width": 3 });
    for (const xx of [mx - 34, w - mx + 34])
      svgEl(marks, "text", { x: xx, y: railY[r] + 8, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 26, fill: col }).textContent = r.endsWith("p") ? "+" : "−";
  }
  // internal strips (hidden until revealed)
  const strips = svgEl(svg, "g", { opacity: 0 });
  const colStrip = {};
  for (let c = 1; c <= cols; c++) {
    const [sx, ya] = L(c, "a"), [, ye] = L(c, "e"), [, yf] = L(c, "f"), [, yj] = L(c, "j");
    colStrip[c] = [svgEl(strips, "rect", { x: sx - 11, y: ya - 13, width: 22, height: ye - ya + 26, rx: 7, fill: "#19c3b4", opacity: 0.55 }),
      svgEl(strips, "rect", { x: sx - 11, y: yf - 13, width: 22, height: yj - yf + 26, rx: 7, fill: "#19c3b4", opacity: 0.55 })];
  }
  const railStrip = {};
  for (const r of ["tp", "tm", "bp", "bm"])
    railStrip[r] = svgEl(svg, "rect", { x: mx - 13, y: railY[r] - 13, width: (cols - 1) * P + 26, height: 26, rx: 9, fill: r.endsWith("p") ? "#e5484d" : "#3b6fe0", opacity: 0 });
  // holes
  const holes = svgEl(svg, "g", {});
  for (let c = 1; c <= cols; c++) {
    for (const r of MID) { const [hx, hy] = L(c, r); svgEl(holes, "rect", { x: hx - 7, y: hy - 7, width: 14, height: 14, rx: 2.5, fill: "#4a4842" }); }
    if (c % 6 !== 0) for (const r of ["tp", "tm", "bp", "bm"]) { const [hx, hy] = L(c, r); svgEl(holes, "rect", { x: hx - 7, y: hy - 7, width: 14, height: 14, rx: 2.5, fill: "#4a4842" }); }
  }
  // labels
  const lab = svgEl(svg, "g", { "font-family": "Segoe UI", "font-size": 15, "font-weight": 600, fill: "#8d8a80", "text-anchor": "middle" });
  for (const r of MID) for (const xx of [mx - 30, w - mx + 30]) svgEl(lab, "text", { x: xx, y: my + ROWS[r] * P + 5 }).textContent = r;
  for (let c = 1; c <= cols; c++) if (c === 1 || c % 5 === 0) {
    svgEl(lab, "text", { x: mx + (c - 1) * P, y: my + (ROWS.a - 0.75) * P + 5 }).textContent = c;
    svgEl(lab, "text", { x: mx + (c - 1) * P, y: my + (ROWS.j + 0.75) * P + 5 }).textContent = c;
  }
  const parts = svgEl(svg, "g", {});
  const over = svgEl(svg, "g", {});
  return { root, svg, L, S, w, h, x, y, groove, strips, colStrip, railStrip, parts, over, mx, my, cols };
}

/** ESP32 board seen from the top, lying across the gap; pins: 30 (rows b/i) or 38 (rows a/i) */
const BBPINS = {
  30: { top: "b", T: ["VIN", "GND", "D13", "D12", "D14", "D27", "D26", "D25", "D33", "D32", "D35", "D34", "VN", "VP", "EN"],
    B: ["3V3", "GND", "D15", "D2", "D4", "D16", "D17", "D5", "D18", "D19", "D21", "RX0", "TX0", "D22", "D23"] },
  38: { top: "a", T: ["5V", "CMD", "D3", "D2", "13", "GND", "12", "14", "27", "26", "25", "33", "32", "35", "34", "VN", "VP", "EN", "3V3"],
    B: ["CLK", "D0", "D1", "15", "2", "0", "4", "16", "17", "5", "18", "19", "GND", "21", "RX", "TX", "22", "23", "GND"] },
};
function bbBoard(bb, pins, c0, rows) {
  const spec = BBPINS[pins], n = pins / 2;
  const [rT, rB] = rows || [spec.top, "i"]; // rows of the top and bottom pin header
  const g = svgEl(bb.parts, "g", {});
  const [x0, yT] = bb.L(c0, rT), [x1, yB] = bb.L(c0 + n - 1, rB);
  const left = x0 - 0.6 * P, right = x1 + 0.6 * P + 34, top = yT - 0.55 * P, bot = yB + 0.55 * P, mid = (yT + yB) / 2;
  svgEl(g, "rect", { x: left - 62, y: mid - 34, width: 84, height: 68, rx: 6, fill: "url(#bbshield)", stroke: "#7d8690", "stroke-width": 2 }); // USB
  svgEl(g, "rect", { x: left, y: top, width: right - left, height: bot - top, rx: 12, fill: "#1b1f26", stroke: "#2b313b", "stroke-width": 2, opacity: 0.97 });
  const mL = x1 - 5.6 * P, mT = yT + 1.0 * P, mB = yB - 1.0 * P;
  svgEl(g, "rect", { x: mL, y: mT, width: right - 6 - mL, height: mB - mT, rx: 5, fill: "#24384f" });
  svgEl(g, "rect", { x: mL + 8, y: mT + 8, width: right - 6 - mL - 70, height: mB - mT - 16, rx: 5, fill: "url(#bbshield)" });
  svgEl(g, "path", { d: `M${right - 52} ${mT + 14} V${mB - 14}`, stroke: "#c9a54a", "stroke-width": 6, "stroke-dasharray": "14 8" });
  const tx = svgEl(g, "text", { x: mL + (right - 76 - mL) / 2, y: mid + 8, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 700, "font-size": 22, fill: "#5d6670" });
  tx.textContent = "ESP32-WROOM-32";
  const pinXY = {};
  for (let k = 0; k < n; k++) {
    for (const [row, names, dy] of [[rT, spec.T, 25], [rB, spec.B, -17]]) {
      const [px, py] = bb.L(c0 + k, row);
      svgEl(g, "rect", { x: px - 10, y: py - 10, width: 20, height: 20, rx: 3, fill: "#d4af37" });
      svgEl(g, "circle", { cx: px, cy: py, r: 4.5, fill: "#15181d" });
      const t = svgEl(g, "text", { x: px, y: py + dy, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 600, "font-size": 12.5, fill: "#e8ecf1" });
      t.textContent = names[k];
      pinXY[(row === rB ? "B" : "T") + k] = [px, py];
    }
  }
  return { g, c0, n, top: rT, pinXY };
}
/** jumper wire between two local points, drawn on at time t */
function bbWire(bb, a, b, color, t, bend = 0.18) {
  const [ax, ay] = a, [bx2, by2] = b, mx2 = (ax + bx2) / 2, my2 = (ay + by2) / 2, dx = bx2 - ax, dy = by2 - ay;
  const cx = mx2 - dy * bend, cy = my2 + dx * bend;
  const g = svgEl(bb.parts, "g", {});
  const p = svgEl(g, "path", { d: `M${ax} ${ay} Q${cx} ${cy} ${bx2} ${by2}`, fill: "none", stroke: color, "stroke-width": 10, "stroke-linecap": "round" });
  const ends = [a, b].map(([ex, ey]) => svgEl(g, "rect", { x: ex - 7, y: ey - 7, width: 14, height: 14, rx: 2, fill: "#222", opacity: 0 }));
  drawOn(p, t, 0.6);
  ends.forEach((e, i) => TO(e, t + (i ? 0.55 : 0), 0.1, { opacity: 1 }));
  return g;
}
/** resistor between two local points (top-view drawing) */
function bbResistor(bb, a, b) {
  const g = svgEl(bb.parts, "g", {});
  const [ax, ay] = a, [bx2, by2] = b, ang = Math.atan2(by2 - ay, bx2 - ax) * 180 / Math.PI, len = Math.hypot(bx2 - ax, by2 - ay);
  const inner = svgEl(g, "g", { transform: `translate(${ax} ${ay}) rotate(${ang})` });
  svgEl(inner, "path", { d: `M0 0 H${len}`, stroke: "#b8bec6", "stroke-width": 5, "stroke-linecap": "round" });
  const bl = 70, b0 = (len - bl) / 2;
  svgEl(inner, "rect", { x: b0, y: -14, width: bl, height: 28, rx: 12, fill: "#dcc79f", stroke: "#b49e72", "stroke-width": 1.5 });
  [[12, "#d0262f"], [24, "#d0262f"], [36, "#7a4a21"], [54, "#c9a54a"]].forEach(([o, c]) => svgEl(inner, "rect", { x: b0 + o, y: -14, width: 7, height: 28, fill: c }));
  for (const [ex, ey] of [a, b]) svgEl(g, "circle", { cx: ex, cy: ey, r: 5, fill: "#9aa1aa" });
  return g;
}
/** LED (top view): legs at a (anode, long) and b (cathode) with the dome beside them */
const BBLED = { red: { rim: "#b51d27", dome: "#d4202c", lit: "#ffd0d0", flat: "#7c121a", glow: "ledglow" },
  green: { rim: "#178a3a", dome: "#2fd36b", lit: "#d8ffe4", flat: "#0f5c27", glow: "ledglowG" } };
function bbLED(bb, a, b, side = -1, color = "red") {
  const K = BBLED[color];
  const g = svgEl(bb.parts, "g", {});
  const [ax, ay] = a, [bx2, by2] = b, mx2 = (ax + bx2) / 2, my2 = (ay + by2) / 2;
  const dx = bx2 - ax, dy = by2 - ay, L2 = Math.hypot(dx, dy) || 1;
  const nx = -dy / L2 * side, ny = dx / L2 * side;
  const cx = mx2 + nx * 34, cy = my2 + ny * 34;
  const glow = svgEl(g, "circle", { cx, cy, r: 110, fill: `url(#${K.glow})`, opacity: 0 });
  for (const [ex, ey] of [a, b]) svgEl(g, "path", { d: `M${ex} ${ey} L${cx + (ex - mx2) * 0.45} ${cy + (ey - my2) * 0.45}`, stroke: "#b8bec6", "stroke-width": 5, "stroke-linecap": "round" });
  svgEl(g, "circle", { cx, cy, r: 24, fill: K.rim });
  const dome = svgEl(g, "circle", { cx, cy, r: 20, fill: K.dome });
  const lit = svgEl(g, "circle", { cx, cy, r: 20, fill: K.lit, opacity: 0 });
  svgEl(g, "path", { d: `M${cx + (bx2 - mx2) / L2 * 24 - ny * 14} ${cy + (by2 - my2) / L2 * 24 + nx * 14} l${ny * 28} ${-nx * 28}`, stroke: K.flat, "stroke-width": 4 });
  for (const [ex, ey] of [a, b]) svgEl(g, "circle", { cx: ex, cy: ey, r: 5, fill: "#9aa1aa" });
  return { g, glow, lit, dome, cx, cy };
}
/** small marker on the stage: ✓ or ✕ badge */
function mark(parent, x, y, ok, txt) {
  const m = box(parent, x, y, 0, 0, "badge", `${ok ? "✓" : "✕"}&nbsp; ${txt}`);
  css(m, { width: "auto", height: "auto", background: ok ? "var(--green)" : "var(--red)", color: ok ? "#05210f" : "#fff", zIndex: 20 });
  return hidden(m);
}



/** Animated current flow overlay on a wire path: activeFn(t) returns 0..1 */
function bbWireFlow(bb, a, b, color = "#ffb547", activeFn) {
  const [ax, ay] = a, [bx2, by2] = b, mx2 = (ax + bx2) / 2, my2 = (ay + by2) / 2, dx = bx2 - ax, dy = by2 - ay;
  const cx = mx2 - dy * 0.18, cy = my2 + dx * 0.18;
  const p = svgEl(bb.over, "path", {
    d: `M${ax} ${ay} Q${cx} ${cy} ${bx2} ${by2}`,
    fill: "none", stroke: color, "stroke-width": 6, "stroke-linecap": "round",
    "stroke-dasharray": "10 18", opacity: 0
  });
  dyn((t) => {
    const v = activeFn ? activeFn(t) : 0;
    p.setAttribute("opacity", v > 0 ? Math.min(1, v * 0.95) : 0);
    if (v > 0) p.setAttribute("stroke-dashoffset", String(-((t * 95) % 28)));
  });
  return p;
}


/** Two breadboards one above the other (ep04 on): the board sits across both, top pins in the
 * upper breadboard's row j, bottom pins in the lower one's row a, so every pin has free holes.
 * The upper breadboard keeps only its top rails, the lower one only its bottom rails.
 * Rows: "1tp" "1tm" "1a".."1j" (upper), "2a".."2j" "2bp" "2bm" (lower); colStrip[1|2][col]. */
const BB2_GAP = 10; // pitches from the upper row j to the lower row a (= the board's pin row spacing)
function makeBB2(parent, x, y, cols = 30) {
  const mx = 58, my = 50, edge = 0.9 * P, w = mx * 2 + (cols - 1) * P;
  const off2 = ROWS.j + BB2_GAP - ROWS.a;
  const R = {};
  for (const r of ["tp", "tm", ...MID]) R["1" + r] = ROWS[r];
  for (const r of [...MID, "bp", "bm"]) R["2" + r] = ROWS[r] + off2;
  const L = (c, r) => [mx + (c - 1) * P, my + R[r] * P];
  const S = (c, r) => { const [lx, ly] = L(c, r); return [x + lx, y + ly]; };
  const bot1 = L(1, "1j")[1] + edge, top2 = L(1, "2a")[1] - edge, h = L(1, "2bm")[1] + my;
  const root = box(parent, x, y, w, h, "");
  const svg = svgEl(root, "svg", { width: w, height: h, viewBox: `0 0 ${w} ${h}` });
  css(svg, { position: "absolute", left: 0, top: 0, overflow: "visible" });
  const defs = svgEl(svg, "defs");
  defs.innerHTML = `<linearGradient id="bbshield" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9edf2"/><stop offset=".5" stop-color="#b9c0c9"/><stop offset="1" stop-color="#d9dee5"/></linearGradient>
    <radialGradient id="ledglow"><stop offset="0" stop-color="#ff6b6b" stop-opacity=".95"/><stop offset=".35" stop-color="#ff4d4d" stop-opacity=".55"/><stop offset="1" stop-color="#ff3030" stop-opacity="0"/></radialGradient>
    <radialGradient id="ledglowG"><stop offset="0" stop-color="#7dffb0" stop-opacity=".95"/><stop offset=".35" stop-color="#3ee887" stop-opacity=".55"/><stop offset="1" stop-color="#20d070" stop-opacity="0"/></radialGradient>`;
  const boards = { 1: svgEl(svg, "g", {}), 2: svgEl(svg, "g", {}) };
  const strips = svgEl(svg, "g", { opacity: 0 });
  const holes = svgEl(svg, "g", {});
  const lab = svgEl(svg, "g", { "font-family": "Segoe UI", "font-size": 15, "font-weight": 600, fill: "#8d8a80", "text-anchor": "middle" });
  const colStrip = { 1: {}, 2: {} }, railStrip = {};
  for (const k of [1, 2]) {
    const g = boards[k], y0 = k === 1 ? 0 : top2, y1 = k === 1 ? bot1 : h;
    svgEl(g, "rect", { x: 0, y: y0, width: w, height: y1 - y0, rx: 20, fill: "#ecebe6", stroke: "#c9c6bd", "stroke-width": 2 });
    const gy = (L(1, k + "e")[1] + L(1, k + "f")[1]) / 2;
    svgEl(g, "rect", { x: 12, y: gy - 15, width: w - 24, height: 30, rx: 7, fill: "#d6d3cb" });
    const rails = k === 1 ? [["tp", -0.55, "#e5484d"], ["tm", 0.55, "#3b6fe0"]] : [["bp", -0.55, "#e5484d"], ["bm", 0.55, "#3b6fe0"]];
    for (const [r, dy, col] of rails) {
      const ry = L(1, k + r)[1];
      svgEl(g, "path", { d: `M${mx - 10} ${ry + dy * P} H${w - mx + 10}`, stroke: col, "stroke-width": 3 });
      for (const xx of [mx - 34, w - mx + 34])
        svgEl(g, "text", { x: xx, y: ry + 8, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 26, fill: col }).textContent = r.endsWith("p") ? "+" : "−";
      railStrip[k + r] = svgEl(svg, "rect", { x: mx - 13, y: ry - 13, width: (cols - 1) * P + 26, height: 26, rx: 9, fill: r.endsWith("p") ? "#e5484d" : "#3b6fe0", opacity: 0 });
      for (let c = 1; c <= cols; c++) if (c % 6 !== 0) svgEl(holes, "rect", { x: L(c, k + r)[0] - 7, y: ry - 7, width: 14, height: 14, rx: 2.5, fill: "#4a4842" });
    }
    for (let c = 1; c <= cols; c++) {
      const [sx, ya] = L(c, k + "a"), [, ye] = L(c, k + "e"), [, yf] = L(c, k + "f"), [, yj] = L(c, k + "j");
      colStrip[k][c] = [svgEl(strips, "rect", { x: sx - 11, y: ya - 13, width: 22, height: ye - ya + 26, rx: 7, fill: "#19c3b4", opacity: 0.55 }),
        svgEl(strips, "rect", { x: sx - 11, y: yf - 13, width: 22, height: yj - yf + 26, rx: 7, fill: "#19c3b4", opacity: 0.55 })];
      for (const r of MID) { const [hx, hy] = L(c, k + r); svgEl(holes, "rect", { x: hx - 7, y: hy - 7, width: 14, height: 14, rx: 2.5, fill: "#4a4842" }); }
      if (c === 1 || c % 5 === 0) {
        if (k === 1) svgEl(lab, "text", { x: sx, y: ya - 0.75 * P + 5 }).textContent = c;
        if (k === 2) svgEl(lab, "text", { x: sx, y: yj + 0.75 * P + 5 }).textContent = c;
      }
    }
    for (const r of MID) for (const xx of [mx - 30, w - mx + 30]) svgEl(lab, "text", { x: xx, y: L(1, k + r)[1] + 5 }).textContent = r;
  }
  const parts = svgEl(svg, "g", {});
  const over = svgEl(svg, "g", {});
  return { root, svg, L, S, w, h, x, y, strips, colStrip, railStrip, parts, over, boards, mx, my, cols };
}
