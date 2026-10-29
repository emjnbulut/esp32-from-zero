/* Wiring diagrams for the creator's shoot pack (2026-10-28): the same two-breadboard drawing as the episodes
 * (engine/breadboard.js), one still per setup. New parts get numbered badges, parts to remove a red ✕.
 * Render: node engine/render.mjs shoot --page shoot/index.html --data shoot/build/<setup>.json --size 1700x1900 --stills 1
 * Positions follow the episodes: board at column 2 (top pins in the upper row j, bottom pins in the lower row a),
 * so D23 = col 16, D22 = col 15, 3V3 = col 2 (lower); D25/26/27 = col 9/8/7, D34 = col 13 (upper). */
const stage = $("#stage");
const CLIP = CLIPS_SPEC()[(window.__DATA || {}).clip];   // per-clip picture: a camera frame over a setup
const setup = CLIP ? CLIP.setup : (window.__DATA || {}).setup || "base";
const H = {};  // handles to parts whose state a clip picture shows (red LED, RGB dome)
const bb = makeBB2(stage, 99, 170, 34);
bbBoard(bb, 30, 2, ["1j", "2a"]);
const BLACK = "#2b2f36", RED = "#e5484d", YEL = "#ffd34d", GRN = "#3ddc84", BLU = "#4d8dff", ORG = "#ff9a3d";
BBLED.yellow = { rim: "#b58b10", dome: "#ffd23f", lit: "#fff6c8", flat: "#7a5d05", glow: "ledglow" };
const L = (c, r) => bb.L(c, r);

function badge(n, [x, y], dx = 0, dy = -46, col = "#ffb547") {
  if (CLIP && !CLIP.badges) return null;
  const g = svgEl(bb.over, "g", {});
  svgEl(g, "circle", { cx: x + dx, cy: y + dy, r: 24, fill: col, stroke: "#0b1220", "stroke-width": 4 });
  const t = svgEl(g, "text", { x: x + dx, y: y + dy + 10, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 28, fill: "#1a1200" });
  t.textContent = n;
  return g;
}
function cross([x, y], dx = 0, dy = 0) {
  const g = svgEl(bb.over, "g", {});
  svgEl(g, "circle", { cx: x + dx, cy: y + dy, r: 30, fill: "rgba(229,72,77,.92)", stroke: "#0b1220", "stroke-width": 4 });
  svgEl(g, "path", { d: `M${x + dx - 12} ${y + dy - 12} l24 24 M${x + dx + 12} ${y + dy - 12} l-24 24`, stroke: "#fff", "stroke-width": 6, "stroke-linecap": "round" });
}
function probe([x, y], plus, label) {
  // probe tip + a label on a dark tag (to the left near the right edge, so it stays on the picture)
  const g = svgEl(bb.over, "g", {});
  svgEl(g, "circle", { cx: x, cy: y, r: 14, fill: plus ? RED : "#111", stroke: "#fff", "stroke-width": 4 });
  const w = label.length * 13 + 24, left = x > 900, tx = left ? x - 26 - w : x + 26, ty = y - 58;
  svgEl(g, "path", { d: `M${x} ${y - 14} L${left ? tx + w : tx} ${ty + 20}`, stroke: plus ? RED : "#111", "stroke-width": 4 });
  svgEl(g, "rect", { x: tx, y: ty, width: w, height: 40, rx: 10, fill: "#0b1220", stroke: plus ? RED : "#8a9ab8", "stroke-width": 3 });
  const t = svgEl(g, "text", { x: tx + 12, y: ty + 28, "font-family": "Segoe UI", "font-weight": 800, "font-size": 23, fill: plus ? "#ffb3b6" : "#e3e9f5" });
  t.textContent = label;
}
function text(cls, html, own) {  // position from the class; in a clip picture only the clip's own texts
  if (CLIP && !own) return null;
  const e = box(stage, 0, 0, 0, 0, cls, html); css(e, { left: "", top: "", width: "", height: "" }); return e;
}
const fade = (g) => { g.setAttribute("opacity", "0.38"); return g; };

/* the parts, in the positions the episodes use */
function gnd() {
  bbWire(bb, L(3, "2e"), L(3, "2bm"), BLACK, -1, 0.12);   // bottom GND pin -> lower minus rail
  bbWire(bb, L(3, "1f"), L(3, "1tm"), BLACK, -1, 0.12);   // top GND pin -> upper minus rail
}
function redLed() {
  bbResistor(bb, L(16, "2e"), L(20, "2g"));               // D23 -> 220 ohm across the gap
  H.red = bbLED(bb, L(20, "2h"), L(21, "2h"), 1);         // long leg 20, short leg 21
  bbWire(bb, L(21, "2j"), L(21, "2bm"), BLACK, -1, -0.35);
}
function button() {
  bbWire(bb, L(15, "2c"), L(25, "2c"), YEL, -1, -0.08);   // D22 -> button left side
  const [x0, y0] = L(25, "2e"), [x1, y1] = L(27, "2f");
  const g = svgEl(bb.parts, "g", {});
  for (const [c, r] of [[25, "2e"], [27, "2e"], [25, "2f"], [27, "2f"]]) { const [x, y] = L(c, r); svgEl(g, "circle", { cx: x, cy: y, r: 6, fill: "#9aa1aa" }); }
  svgEl(g, "rect", { x: x0 - 8, y: y0 - 4, width: x1 - x0 + 16, height: y1 - y0 + 8, rx: 10, fill: "#2a2d33", stroke: "#4b5058", "stroke-width": 3 });
  svgEl(g, "circle", { cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, r: 30, fill: "#151719", stroke: "#3a3e45", "stroke-width": 3 });
  bbWire(bb, L(27, "2j"), L(27, "2bm"), BLACK, -1, -0.35); // button right side -> minus rail
  return g;
}
function greenLed() {
  const g = svgEl(bb.parts, "g", {});
  g.appendChild(bbWire(bb, L(9, "1g"), L(18, "1g"), GRN, -1, -0.06));
  g.appendChild(bbResistor(bb, L(18, "1f"), L(21, "1d")));
  g.appendChild(bbLED(bb, L(21, "1c"), L(22, "1c"), -1, "green").g);
  g.appendChild(bbWire(bb, L(22, "1a"), L(22, "1tm"), BLACK, -1, 0.35));
  return g;
}
function rgb() {
  bbWire(bb, L(9, "1g"), L(20, "1g"), RED, -1, -0.05);    // D25 -> red
  bbWire(bb, L(8, "1h"), L(22, "1h"), GRN, -1, -0.05);    // D26 -> green
  bbWire(bb, L(7, "1i"), L(23, "1i"), BLU, -1, -0.05);    // D27 -> blue
  for (const c of [20, 22, 23]) bbResistor(bb, L(c, "1f"), L(c, "1e"));
  bbWire(bb, L(21, "1a"), L(21, "1tm"), BLACK, -1, 0.35); // long (common) leg -> minus rail
  // top view: the clear dome sits over its four legs (row c, columns 20-23), the long common leg is 21
  const g = svgEl(bb.parts, "g", {});
  const [xa, yc] = L(20, "1c"), [xb] = L(23, "1c"), cx = (xa + xb) / 2, cy = L(21, "1b")[1] + 4;
  [[20, RED, "R"], [21, "#c9ced6", "−"], [22, GRN, "G"], [23, BLU, "B"]].forEach(([c, col, lab]) => {
    const [x, y] = L(c, "1c");
    svgEl(g, "path", { d: `M${x} ${y} L${cx + (x - cx) * 0.6} ${cy}`, stroke: col, "stroke-width": c === 21 ? 8 : 5, "stroke-linecap": "round" });
    svgEl(g, "circle", { cx: x, cy: y, r: 7, fill: col, stroke: "#333", "stroke-width": 1.5 });
    const t = svgEl(g, "text", { x, y: L(c, "1d")[1] + 9, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 22, fill: col === "#c9ced6" ? "#555" : col });
    t.textContent = lab;
  });
  H.rgb = svgEl(g, "circle", { cx, cy, r: 34, fill: "rgba(235,240,255,.88)", stroke: "#aeb6c4", "stroke-width": 3 });
  H.rgbXY = [cx, cy];
  const t = svgEl(g, "text", { x: cx, y: cy + 8, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 21, fill: "#3a4252" });
  t.textContent = "RGB";
}
function pot() {
  // 10 k potentiometer, three legs in the lower breadboard (row h): left 28 -> GND, middle 30 -> D34, right 32 -> 3.3 V
  bbWire(bb, L(2, "2d"), L(2, "2bp"), RED, -1, 0.1);      // 3V3 pin -> lower plus rail
  bbWire(bb, L(28, "2j"), L(28, "2bm"), BLACK, -1, -0.35);
  bbWire(bb, L(32, "2j"), L(32, "2bp"), RED, -1, 0.35);
  bbWire(bb, L(30, "2i"), L(13, "1f"), ORG, -1, 0.22);     // middle leg -> D34 (upper, column 13, row f)
  // the creator's rails are split in the middle (2026-10-29: the pot stayed dark): bridge both lower rails across the gap
  bbWire(bb, L(29, "2bp"), L(35, "2bp"), RED, -1, 0.5);
  bbWire(bb, L(29, "2bm"), L(35, "2bm"), BLACK, -1, -0.5);
  const g = svgEl(bb.parts, "g", {});
  const [x0, y] = L(28, "2h"), [x1] = L(32, "2h");
  for (const c of [28, 30, 32]) { const [x, yy] = L(c, "2h"); svgEl(g, "path", { d: `M${x} ${yy} V${yy - 40}`, stroke: "#b8bec6", "stroke-width": 5 }); svgEl(g, "circle", { cx: x, cy: yy, r: 6, fill: "#9aa1aa" }); }
  svgEl(g, "rect", { x: x0 - 24, y: y - 118, width: x1 - x0 + 48, height: 84, rx: 10, fill: "#2f5fd0", stroke: "#1d3f94", "stroke-width": 3 });
  svgEl(g, "circle", { cx: (x0 + x1) / 2, cy: y - 76, r: 30, fill: "#d9dde3", stroke: "#8f97a3", "stroke-width": 3 });
  svgEl(g, "path", { d: `M${(x0 + x1) / 2} ${y - 76} l0 -26`, stroke: "#5b6470", "stroke-width": 6, "stroke-linecap": "round" });
}
function trafficLeds() {
  bbResistor(bb, L(10, "2e"), L(12, "2g"));                // D18 -> yellow
  H.yellow = bbLED(bb, L(12, "2h"), L(13, "2h"), 1, "yellow");
  bbWire(bb, L(13, "2j"), L(13, "2bm"), BLACK, -1, -0.35);
  bbResistor(bb, L(8, "2d"), L(9, "2g"));                  // D17 -> green
  H.green = bbLED(bb, L(9, "2h"), L(10, "2h"), 1, "green");
  bbWire(bb, L(10, "2j"), L(10, "2bm"), BLACK, -1, -0.35);
}

/* the setups */
const SETUPS = {
  base() {
    text("wtitle", "Şu anki devreniz (Bölüm 04 sonu)");
    text("wsub", "Bölüm 05 · Kısım 1 için hiçbir şeyi değiştirmeyin.");
    gnd(); redLed(); button(); greenLed();
    text("wnote", "Kırmızı LED → D23 · Buton → D22 · Yeşil LED → D25 (üst breadboard). İki siyah kablo GND pinlerinden eksi raylara.");
  },
  "05-1-meter"() {
    text("wtitle", "05 · Kısım 1 — multimetre çekimi (C1)");
    text("wsub", "Kod: pwm_levels · Multimetre: DC volt (V⎓), 20 V kademesi");
    gnd(); redLed(); button(); greenLed();
    probe(L(16, "2d"), true, "kırmızı prob: 16d (D23 sütunu)");
    probe(L(24, "2bm"), false, "siyah prob: eksi ray");
    text("wnote", "Probları sabitleyin (kıskaç ya da bant), elleriniz kadrajda olmasın. Ekran: 0 → ~0,8 → ~1,65 → ~3,3 V, her biri 2 saniye.");
  },
  "05-2-remove"() {
    text("wtitle", "05 · Kısım 2 — adım 1: yeşil LED'i sökün");
    text("wsub", "Önce USB'yi çıkarın. Üst breadboard'daki yeşil LED devresinin 4 parçası çıkar (✕).");
    gnd(); redLed(); button(); greenLed();
    cross(L(21.5, "1c"), 0, 34); cross(L(19.5, "1e"), 0, 0); cross(L(13.5, "1g"), 0, -2); cross(L(22, "1a"), 34, -30);
    text("wnote", "✕ yeşil LED (21c–22c) · ✕ direnci (18f → 21d) · ✕ yeşil kablo (D25 → 18g) · ✕ siyah kablo (22a → üst eksi ray). Kırmızı LED, buton ve GND kabloları yerinde kalır.");
  },
  "05-2"() {
    text("wtitle", "05 · Kısım 2 — adım 2: RGB LED'i takın");
    text("wsub", "Numaralar takma sırası. RGB'nin EN UZUN bacağı soldan 2. delikte (21).");
    gnd(); redLed(); button(); rgb();
    badge(1, L(19.5, "1b"), -40, -8); badge(2, L(21, "1a"), 50, 4); badge(3, L(18.5, "1f"), 0, -4);
    badge(4, L(14, "1g"), 0, -28, "#ff8f8f"); badge(5, L(15, "1h"), 0, 30, "#7ee2a8"); badge(6, L(17, "1i"), 0, 32, "#8fb4ff");
    text("wnote", "① RGB: c sırası, 20–23 (R, −, G, B) · ② siyah: 21a → üst eksi ray · ③ üç 220 Ω direnç, boşluğun üstünden: 20f→20e, 22f→22e, 23f→23e · ④ kırmızı: D25 → 20g · ⑤ yeşil: D26 → 22h · ⑥ mavi: D27 → 23i.");
  },
  "06"() {
    text("wtitle", "06 — Potansiyometre (alt breadboard, sağ)");
    text("wsub", "Önce USB'yi çıkarın. RGB ve kırmızı LED yerinde kalır.");
    gnd(); redLed(); button(); rgb(); pot();
    badge(1, L(30, "2h"), 0, -150); badge(2, L(2, "2d"), 34, 40); badge(3, L(28, "2j"), -30, 30); badge(4, L(32, "2j"), 30, 30); badge(5, L(13, "1f"), -40, 6); badge(6, L(35, "2bp"), 40, 60);
    text("wnote", "① Pot: 3 bacak h sırasında, 28–30–32 (bacaklar bitişikse 28–29–30 da olur) · ② kırmızı: 3V3 (2. sütun) → alt artı ray · ③ sol bacak → eksi ray · ④ sağ bacak → ARTI ray (3,3 V; asla VIN/5 V değil) · ⑤ turuncu: orta bacak (30i) → D34 sütunu (üst, 13f) · ⑥ ÖNEMLİ: artı ve eksi ray ortada kesik; iki köprü kablo (29 → 35) iki yarıyı birleştirir, yoksa pot elektrik almaz.");
  },
  "06-meter"() {
    text("wtitle", "06 — multimetre çekimi");
    text("wsub", "Kod: pot_read · Multimetre: DC volt (V⎓), 20 V kademesi");
    gnd(); redLed(); button(); rgb(); pot();
    probe(L(30, "2j"), true, "kırmızı prob: 30j (orta bacak)");
    probe(L(24, "2bm"), false, "siyah prob: eksi ray");
    text("wnote", "Tek elle düğmeyi yavaşça bir uçtan diğerine çevirin: ekran 0,0 → 3,3 V. Prob uçları sabit kalsın.");
  },
  "07"() {
    text("wtitle", "07 — Devre 06·2 ile aynı (yeni kablo yok)");
    text("wsub", "Araba ışıkları: kırmızı D23, sarı D18, yeşil D17 · Yaya ışığı: RGB (kırmızı/yeşil)");
    gnd(); redLed(); button(); rgb(); pot(); trafficLeds();
    text("wnote", "Buton = yaya düğmesi (07·1) ve oyun düğmesi (07·2) · Potansiyometre: yeşil süresi (07·1), sarı bekleme süresi (07·2).");
  },
  "06-2"() {
    text("wtitle", "06·2 — Sarı ve yeşil LED (seviye çubuğu)");
    text("wsub", "Önce USB'yi çıkarın. Bu iki LED 07'de trafik ışığı olarak da kalacak.");
    gnd(); redLed(); button(); rgb(); pot(); trafficLeds();
    badge(1, L(11, "2f"), 0, 30); badge(2, L(12.5, "2i"), 0, 70); badge(3, L(8.5, "2f"), 0, 30); badge(4, L(9.5, "2i"), 0, 70);
    text("wnote", "Kırmızı = D23 (var olan) · ① sarı direnç: D18 (10e) → 12g · ② sarı LED: uzun bacak 12h, kısa 13h, siyah 13j → eksi · ③ yeşil direnç: D17 (8d) → 9g · ④ yeşil LED: uzun 9h, kısa 10h, siyah 10j → eksi.");
  },
};
(SETUPS[setup] || SETUPS.base)();

/* per-clip picture: LED state, a dashed camera frame (outside dimmed) and what the hand does */
function CLIPS_SPEC() {
  const LOW = ["2b", "2bm"], RGBA = ["1tm", "1g"];
  return {
    "05-1-C0": { setup: "base", t: "05·1 · C0 — açılış", s: "fade_millis yüklü", f: [14, "2b", 29, "2bm"], red: 0.6,
      m: [["press", 26, "2e", "bas: durur · tekrar bas: devam"], ["note", 20, "2i", "nefes alıyor"]] },
    "05-1-C1": { setup: "05-1-meter", t: "05·1 · C1 — multimetre", s: "pwm_levels yüklü · DC volt", f: [12, "2a", 31, "2bm"], red: 0.5,
      m: [["note", 27, "2c", "multimetre ekranı da kadrajda (sağda)"]] },
    "05-1-C2": { setup: "base", t: "05·1 · C2 — pwm_levels", s: "LED yakın plan, oda biraz loş", f: [16, "2e", 24, "2bm"], red: 0.3,
      m: [["note", 20, "2g", "kapalı → %25 → %50 → %100"]] },
    "05-1-C3": { setup: "base", t: "05·1 · C3 — yaygın hata", s: "fade_naive yüklü", f: [14, "2b", 29, "2bm"], red: 0.6,
      m: [["press", 26, "2e", "3–4 kez kısa bas: LED durmuyor"]] },
    "05-1-C4": { setup: "base", t: "05·1 · C4 — çalıştır", s: "fade_millis yüklü, C0'dan yakın", f: [17, "2c", 29, "2bm"], red: 0.5,
      m: [["press", 26, "2e", "bas: anında durur"]] },
    "05-1-C5": { setup: "base", t: "05·1 · C5 — değiştir (isteğe bağlı)", s: "fade_millis, 39. satır: 4 → 10", f: [17, "2c", 29, "2bm"], red: 0.4,
      m: [["note", 20, "2i", "nefes daha yavaş"]] },
    "05-2-C0": { setup: "05-2", t: "05·2 · C0 — açılış", s: "color_modes yüklü", f: [14, "1a", 30, "2j"], rgb: "#ff3b3b",
      m: [["press", 26, "2e", "3 kez bas"], ["note", 21.5, "1e", "kırmızı → yeşil → mavi → geçiş"]] },
    "05-2-C1": { setup: "05-2", badges: true, t: "05·2 · C1 — kurulum", s: "USB çıkarılmış · üstten yakın", f: [5, "1tm", 26, "1j"],
      m: [] },
    "05-2-C2": { setup: "05-2", t: "05·2 · C2 — rgb_colors", s: "RGB yakın plan, oda biraz loş", f: [17, "1tm", 26, "1g"], rgb: "#ffd400",
      m: [["note", 21.5, "1e", "8 renk sırayla"]] },
    "05-2-C3": { setup: "05-2", t: "05·2 · C3 — yaygın hata", s: "rgb_colors çalışırken", f: [16, "1tm", 26, "1g"], rgb: "#00e5ff",
      m: [["pull", 21, "1a", "siyah kabloyu çek: söner · geri tak: döner"]] },
    "05-2-C4": { setup: "05-2", t: "05·2 · C4 — çalıştır", s: "color_modes, C0'dan yakın", f: [14, "1a", 30, "2j"], rgb: "#2f6bff",
      m: [["press", 26, "2e", "her basışta renk değişir"]] },
    "06-1-C0": { setup: "06", t: "06·1 · C0 — açılış", s: "pot_dimmer yüklü", f: [17, "2c", 34, "2bm"], red: 0.7,
      m: [["turn", 30, "2f", "yavaşça çevir, geri çevir"], ["note", 20, "2i", "parlaklık takip ediyor"]] },
    "06-1-C1": { setup: "06", badges: true, t: "06·1 · C1 — kurulum", s: "USB çıkarılmış · üstten", f: [1, "1f", 34, "2bm"], m: [] },
    "06-1-C2": { setup: "06-meter", t: "06·1 · C2 — multimetre", s: "pot_read yüklü · DC volt", f: [20, "2c", 34, "2bm"],
      m: [["turn", 30, "2f", "tek elle yavaşça çevir: 0 → 3,3 V"], ["note", 23, "2c", "multimetre ekranı kadrajda"]] },
    "06-2-C0": { setup: "06-2", t: "06·2 · C0 — açılış", s: "level_bar yüklü", f: [6, "2c", 34, "2bm"], red: 0.7, yellow: 0.7, green: 0.7,
      m: [["turn", 30, "2f", "yavaşça sağa çevir: yeşil → +sarı → +kırmızı"]] },
    "06-2-C1": { setup: "06-2", badges: true, t: "06·2 · C1 — kurulum", s: "USB çıkarılmış · üstten", f: [5, "2a", 16, "2bm"], m: [] },
    "06-2-C2": { setup: "06-2", t: "06·2 · C2 — map_dimmer", s: "map_dimmer yüklü", f: [17, "2c", 34, "2bm"], red: 0.6,
      m: [["turn", 30, "2f", "yavaşça çevir"], ["note", 20, "2i", "parlaklık takip ediyor"]] },
    "06-2-C3": { setup: "06-2", t: "06·2 · C3 — çalıştır", s: "level_bar, C0'dan yakın", f: [6, "2e", 34, "2bm"], yellow: 0.7, green: 0.7,
      m: [["turn", 30, "2f", "ileri geri çevir"]] },
    "06-2-C4": { setup: "06-2", t: "06·2 · C4 — yaygın hata", s: "level_bar çalışırken", f: [6, "2e", 22, "2bm"], green: 0.7, red: 0.7,
      m: [["pull", 12.5, "2h", "sarı LED'i ters tak: yanmaz · düzelt: yanar"]] },
    "07-1-C0": { setup: "07", t: "07·1 · C0 — açılış", s: "crossing yüklü · tam bir tur (~20 sn)", f: [6, "1a", 30, "2bm"], green: 0.7, rgb: "#ff3b3b",
      m: [["press", 26, "2e", "bas: istek"], ["note", 21.5, "1e", "yaya ışığı"]] },
    "07-1-C1": { setup: "07", t: "07·1 · C1 — basma süresi", s: "press_time yüklü", f: [6, "2c", 29, "2bm"], yellow: 0.8,
      m: [["press", 26, "2e", "bir kısa, bir uzun bas"], ["note", 12.5, "2i", "basılıyken yanar"]] },
    "07-1-C2": { setup: "07", t: "07·1 · C2 — yaya ışığı yanıp sönüyor", s: "crossing, yaya yeşili", f: [16, "1tm", 26, "1g"], rgb: "#2bff6a",
      m: [["note", 21.5, "1e", "son 2 sn yanıp söner"]] },
    "07-2-C0": { setup: "07", t: "07·2 · C0 — açılış", s: "reflex_game yüklü", f: [6, "1a", 30, "2bm"], green: 0.8, rgb: "#2bff6a",
      m: [["press", 26, "2e", "başlat · yeşil yanınca hemen bas"]] },
    "07-2-C1": { setup: "07", t: "07·2 · C1 — yavaş tepki", s: "reflex_game: yeşilden ~1 sn sonra bas", f: [6, "1a", 30, "2bm"], rgb: "#ff3b3b",
      m: [["press", 26, "2e", "geç bas → RGB kırmızı"]] },
    "07-2-C2": { setup: "07", t: "07·2 · C2 — elektrik kesilse de rekor kalır", s: "USB kablosunu çıkarıp geri tak (3–5 sn)", f: [0.2, "1h", 9, "2c"],
      m: [["pull", 2.2, "1j", "USB'yi çek, geri tak", 205]] },
  };
}
if (CLIP) {
  text("wtitle", CLIP.t, true);
  text("wsub", CLIP.s, true);
  if (CLIP.red != null && H.red) {
    H.red.lit.setAttribute("opacity", CLIP.red); H.red.glow.setAttribute("opacity", CLIP.red);
  }
  for (const k of ["yellow", "green"]) if (CLIP[k] != null && H[k]) { H[k].lit.setAttribute("opacity", CLIP[k]); H[k].glow.setAttribute("opacity", CLIP[k] * 0.7); }
  if (CLIP.rgb && H.rgb) {
    H.rgb.setAttribute("fill", CLIP.rgb);
    svgEl(bb.parts, "circle", { cx: H.rgbXY[0], cy: H.rgbXY[1], r: 90, fill: CLIP.rgb, opacity: 0.28 });
  }
  const [c0, r0, c1, r1] = CLIP.f, [x0, y0] = L(c0, r0), [x1, y1] = L(c1, r1), pad = 30;
  const fx = x0 - pad, fy = y0 - pad, fw = x1 - x0 + 2 * pad, fh = y1 - y0 + 2 * pad;
  svgEl(bb.over, "path", { d: `M-200 -200 H${bb.w + 200} V${bb.h + 200} H-200 Z M${fx} ${fy} V${fy + fh} H${fx + fw} V${fy} Z`,
    fill: "rgba(5,8,14,.62)", "fill-rule": "evenodd" });
  svgEl(bb.over, "rect", { x: fx, y: fy, width: fw, height: fh, rx: 14, fill: "none", stroke: "#ffb547", "stroke-width": 6, "stroke-dasharray": "22 14" });
  const k = svgEl(bb.over, "text", { x: fx + 14, y: fy - 14, "font-family": "Segoe UI", "font-weight": 800, "font-size": 30, fill: "#ffb547" });
  k.textContent = "📷 KADRAJ";
  for (const [kind, c, r, label, dy = 0] of CLIP.m) {
    const [x, y0] = L(c, r), y = y0 + dy, icon = { press: "👆", turn: "↻", pull: "✋", note: "" }[kind];
    const g = svgEl(bb.over, "g", {});
    if (icon) svgEl(g, "text", { x, y: y + 18, "text-anchor": "middle", "font-size": 56 }).textContent = icon;
    const w = label.length * 14 + 28, ty = kind === "note" ? y - 22 : y + 46;
    svgEl(g, "rect", { x: x - w / 2, y: ty, width: w, height: 44, rx: 12, fill: "#0b1220", stroke: "#ffb547", "stroke-width": 3 });
    svgEl(g, "text", { x, y: ty + 31, "text-anchor": "middle", "font-family": "Segoe UI", "font-weight": 800, "font-size": 25, fill: "#ffe3b8" }).textContent = label;
  }
  if (CLIP.n) text("wnote", CLIP.n, true);
}
window.__seek = window.__seek || (() => {});
window.__ready = true;
