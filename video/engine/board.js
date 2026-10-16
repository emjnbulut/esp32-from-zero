/* Generic ESP32 dev board drawn as SVG (top view, USB at the bottom).
 * 1 mm = 10 units. pins: 30 (DOIT DevKit V1 style) or 38 (DevKitC style).
 * chip: "cp2102" (square QFN) or "ch340" (SOP-16).
 * Parts carry ids prefixed with `p` so scenes can highlight them.
 */
const PINOUT = {
  30: {
    L: ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"],
    R: ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "D17", "D16", "D4", "D2", "D15", "GND", "3V3"],
  },
  38: {
    L: ["3V3", "EN", "VP", "VN", "34", "35", "32", "33", "25", "26", "27", "14", "12", "GND", "13", "D2", "D3", "CMD", "5V"],
    R: ["GND", "23", "22", "TX", "RX", "21", "GND", "19", "18", "5", "17", "16", "4", "0", "2", "15", "D1", "D0", "CLK"],
  },
};

function boardSVG({ pins = 30, chip = "cp2102", p = "b", labels = true, width } = {}) {
  const n = pins / 2, pitch = 25.4;
  const W = 283, H = pins === 30 ? 515 : 544;
  const y0 = H - 40 - (n - 1) * pitch - 30;
  const xl = 22, xr = W - 22;
  const po = PINOUT[pins];
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -20 ${W + 40} ${H + 70}" ${width ? `width="${width}"` : ""}>
  <defs>
    <linearGradient id="${p}shield" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9edf2"/><stop offset=".5" stop-color="#b9c0c9"/><stop offset="1" stop-color="#d9dee5"/></linearGradient>
    <linearGradient id="${p}usb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe4ea"/><stop offset="1" stop-color="#9aa3ad"/></linearGradient>
  </defs>
  <rect id="${p}-pcb" x="0" y="0" width="${W}" height="${H}" rx="14" fill="#1b1f26" stroke="#2b313b" stroke-width="2"/>`;
  // mounting holes
  for (const [hx, hy] of [[16, 16], [W - 16, 16], [16, H - 16], [W - 16, H - 16]])
    s += `<circle cx="${hx}" cy="${hy}" r="9" fill="#0e1014" stroke="#c9a54a" stroke-width="3"/>`;
  // module
  const mx = (W - 180) / 2, my = 6;
  s += `<g id="${p}-module">
    <rect x="${mx}" y="${my}" width="180" height="255" rx="4" fill="#24384f"/>
    <path d="M${mx + 22} ${my + 46} v-28 h18 v24 h18 v-24 h18 v24 h18 v-24 h18 v24 h18 v-24 h18 v34" fill="none" stroke="#c9a54a" stroke-width="5"/>
    <rect x="${mx + 9}" y="${my + 68}" width="162" height="178" rx="5" fill="url(#${p}shield)" stroke="#8a929c" stroke-width="2"/>
    <text x="${mx + 90}" y="${my + 140}" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="17" fill="#5d6670">ESP32-WROOM-32</text>
    <text x="${mx + 90}" y="${my + 166}" text-anchor="middle" font-family="Segoe UI" font-size="12" fill="#6d7680">WiFi + Bluetooth</text>
    <rect x="${mx + 60}" y="${my + 188}" width="60" height="38" rx="3" fill="none" stroke="#8b939d" stroke-width="2"/>
  </g>`;
  // headers
  const pad = (x, y) => `<rect x="${x - 9}" y="${y - 9}" width="18" height="18" rx="3" fill="#d4af37"/><circle cx="${x}" cy="${y}" r="4.5" fill="#15181d"/>`;
  s += `<g id="${p}-pinsL">`; for (let i = 0; i < n; i++) s += pad(xl, y0 + i * pitch); s += `</g>`;
  s += `<g id="${p}-pinsR">`; for (let i = 0; i < n; i++) s += pad(xr, y0 + i * pitch); s += `</g>`;
  if (labels) {
    s += `<g font-family="Segoe UI" font-weight="600" font-size="10.5" fill="#e8ecf1">`;
    for (let i = 0; i < n; i++) {
      s += `<text x="${xl + 15}" y="${y0 + i * pitch + 4}">${po.L[i]}</text>`;
      s += `<text x="${xr - 15}" y="${y0 + i * pitch + 4}" text-anchor="end">${po.R[i]}</text>`;
    }
    s += `</g>`;
  }
  // regulator (SOT-223)
  s += `<g><rect x="70" y="${H - 175}" width="56" height="34" rx="2" fill="#2a2d33"/><rect x="78" y="${H - 186}" width="40" height="11" fill="#b8bec6"/>
    ${[0, 1, 2].map((i) => `<rect x="${76 + i * 18}" y="${H - 141}" width="8" height="9" fill="#b8bec6"/>`).join("")}</g>`;
  // usb-serial chip
  if (chip === "cp2102") {
    s += `<g id="${p}-chip"><rect x="${W / 2 + 6}" y="${H - 190}" width="50" height="50" rx="3" fill="#121418"/>
      <text x="${W / 2 + 31}" y="${H - 168}" text-anchor="middle" font-family="Segoe UI" font-size="8.5" fill="#9aa1aa">SiLabs</text>
      <text x="${W / 2 + 31}" y="${H - 156}" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="9" fill="#9aa1aa">CP2102</text></g>`;
  } else {
    const cx = W / 2 - 52, cy = H - 250;
    let legs = ""; for (let i = 0; i < 8; i++) legs += `<rect x="${cx + 6 + i * 12.7}" y="${cy - 8}" width="6" height="8" fill="#b8bec6"/><rect x="${cx + 6 + i * 12.7}" y="${cy + 40}" width="6" height="8" fill="#b8bec6"/>`;
    s += `<g id="${p}-chip">${legs}<rect x="${cx}" y="${cy}" width="104" height="40" rx="3" fill="#121418"/>
      <text x="${cx + 52}" y="${cy + 25}" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="11" fill="#9aa1aa">CH340C</text></g>`;
  }
  // leds
  s += `<g id="${p}-led"><rect x="${W / 2 - 40}" y="${H - 116}" width="14" height="9" rx="1.5" fill="#ff3b3b"/><text x="${W / 2 - 33}" y="${H - 122}" text-anchor="middle" font-family="Segoe UI" font-size="8" fill="#e8ecf1">PWR</text></g>
    <g id="${p}-led2"><rect x="${W / 2 + 26}" y="${H - 116}" width="14" height="9" rx="1.5" fill="#3b8bff"/><text x="${W / 2 + 33}" y="${H - 122}" text-anchor="middle" font-family="Segoe UI" font-size="8" fill="#e8ecf1">IO2</text></g>`;
  // buttons
  const btn = (id, x, label) => `<g id="${p}-${id}"><rect x="${x - 18}" y="${H - 80}" width="36" height="40" rx="4" fill="#cfd5dc"/><circle cx="${x}" cy="${H - 60}" r="11" fill="#2b2f36"/>
    <text x="${x}" y="${H - 86}" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="11" fill="#e8ecf1">${label}</text></g>`;
  s += btn("en", 80, "EN") + btn("boot", W - 80, "BOOT");
  // usb connector
  s += `<g id="${p}-usb"><rect x="${W / 2 - 38}" y="${H - 52}" width="76" height="62" rx="5" fill="url(#${p}usb)" stroke="#7d8690" stroke-width="2"/>
    <rect x="${W / 2 - 24}" y="${H + 0}" width="48" height="8" rx="2" fill="#2a2f36"/></g>`;
  s += `</svg>`;
  return s;
}
