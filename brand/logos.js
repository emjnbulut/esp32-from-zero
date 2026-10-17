// Pin by Pin Lab - logo concepts as SVG strings (viewBox 0 0 512 512, drawn for a circular crop)
const C = { teal: "#19c3b4", amber: "#ffb547", bg: "#0b1220", panel: "#111c30", line: "#22304d", ink: "#e8eef7" };

const bgCircle = `<circle cx="256" cy="256" r="256" fill="${C.bg}"/>`;

// A - a chip whose body carries a bold P; pins on both sides
function chipP() {
  let pins = "";
  for (let i = 0; i < 4; i++) {
    const y = 176 + i * 52;
    pins += `<rect x="112" y="${y}" width="48" height="22" rx="5" fill="${C.teal}"/>`;
    pins += `<rect x="352" y="${y}" width="48" height="22" rx="5" fill="${C.teal}"/>`;
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">${bgCircle}${pins}
    <rect x="152" y="140" width="208" height="232" rx="22" fill="${C.panel}" stroke="${C.line}" stroke-width="6"/>
    <circle cx="180" cy="168" r="9" fill="${C.line}"/>
    <path d="M222 330 V182 h52 a40 40 0 0 1 0 80 h-52" fill="none" stroke="${C.amber}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;
}

// B - a header-hole grid; the lit holes trace a P like a PCB route, the last one glows
function gridP() {
  const cols = 4, rows = 5, gap = 62, x0 = 256 - 1.5 * gap, y0 = 256 - 2 * gap;
  const lit = [[0, 4], [0, 3], [0, 2], [0, 1], [0, 0], [1, 0], [2, 0], [3, 1], [2, 2], [1, 2]];
  const key = (c, r) => c + "," + r, on = new Set(lit.map(([c, r]) => key(c, r)));
  let holes = "";
  for (let c = 0; c < cols; c++) for (let r = 0; r < rows; r++) {
    const x = x0 + c * gap, y = y0 + r * gap;
    holes += on.has(key(c, r)) ? "" : `<circle cx="${x}" cy="${y}" r="13" fill="none" stroke="${C.line}" stroke-width="6"/>`;
  }
  const pts = lit.map(([c, r]) => `${x0 + c * gap},${y0 + r * gap}`).join(" ");
  const dots = lit.map(([c, r], i) => `<circle cx="${x0 + c * gap}" cy="${y0 + r * gap}" r="${i === lit.length - 1 ? 22 : 16}" fill="${i === lit.length - 1 ? C.amber : C.teal}"/>`).join("");
  const [lc, lr] = lit[lit.length - 1];
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">${bgCircle}
    <defs><radialGradient id="g"><stop offset="0" stop-color="${C.amber}" stop-opacity=".55"/><stop offset="1" stop-color="${C.amber}" stop-opacity="0"/></radialGradient></defs>
    ${holes}<polyline points="${pts}" fill="none" stroke="${C.teal}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" opacity=".55"/>
    <circle cx="${x0 + lc * gap}" cy="${y0 + lr * gap}" r="60" fill="url(#g)"/>${dots}
  </svg>`;
}

// C - one male header pin: black plastic block, gold pin, a spark at the tip
function headerPin() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">${bgCircle}
    <defs><linearGradient id="gold" x1="0" x2="1"><stop offset="0" stop-color="#ffcf7a"/><stop offset=".5" stop-color="${C.amber}"/><stop offset="1" stop-color="#c98420"/></linearGradient>
    <radialGradient id="sp"><stop offset="0" stop-color="${C.teal}" stop-opacity=".9"/><stop offset="1" stop-color="${C.teal}" stop-opacity="0"/></radialGradient></defs>
    <circle cx="256" cy="118" r="70" fill="url(#sp)"/>
    <rect x="236" y="112" width="40" height="300" rx="8" fill="url(#gold)"/>
    <path d="M236 120 l20 -22 l20 22 z" fill="url(#gold)"/>
    <rect x="176" y="268" width="160" height="78" rx="12" fill="#1b2438" stroke="${C.teal}" stroke-width="6"/>
    <rect x="236" y="268" width="40" height="78" fill="url(#gold)" opacity=".25"/>
  </svg>`;
}

// D - wordmark monogram "pbp" where the dots are header holes
function monogram() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">${bgCircle}
    <text x="256" y="300" text-anchor="middle" font-family="Bahnschrift, Segoe UI" font-weight="700" font-size="190" fill="${C.ink}" letter-spacing="-6">p<tspan fill="${C.amber}">b</tspan>p</text>
    <g fill="none" stroke="${C.teal}" stroke-width="7">${[0, 1, 2, 3, 4].map(i => `<rect x="${151 + i * 44}" y="350" width="26" height="26" rx="4"/>`).join("")}</g>
    <rect x="${151 + 2 * 44 + 5}" y="355" width="16" height="16" rx="2" fill="${C.amber}"/>
  </svg>`;
}

// scale the artwork up inside the circle (YouTube shows avatars small)
const zoom = (fn, k) => () => fn().replace(bgCircle, bgCircle + `<g transform="translate(256 256) scale(${k}) translate(-256 -256)">`).replace(/<\/svg>\s*$/, "</g></svg>");
const LOGOS = { A: zoom(chipP, 1.3), B: zoom(gridP, 1.45), C: zoom(headerPin, 1.25), D: zoom(monogram, 1.3) };
if (typeof module !== "undefined") module.exports = { LOGOS, C };
