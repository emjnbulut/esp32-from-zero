/* Episode 1 - Setting Up Your Computer. All times come from the narration schedule. */
const stage = $("#stage");
const SC = (cls = "") => { const s = el("div", "scene " + cls, '<div class="grid"></div>', stage); return s; };
const T = (id) => S0(id);

/* ======================================================================
 * INTRO
 * ==================================================================== */
const sIntro = SC();
SET(sIntro, 0, { opacity: 1 });
{
  const kick = box(sIntro, 140, 300, 600, 40, "kicker", "Episode 01");
  const title = box(sIntro, 136, 336, 1000, 140, "h1", "ESP32 From Zero");
  title.style.fontSize = "112px";
  const sub = box(sIntro, 140, 486, 900, 60, "h3", "Setting Up Your Computer");
  sub.style.color = "var(--teal)";
  const persp = box(sIntro, 1130, 70, 560, 900, "");
  persp.style.perspective = "1600px";
  const b3d = box(persp, 0, 0, 560, 900, "", boardSVG({ pins: 30, chip: "cp2102", p: "bi", width: 520 }));
  css(b3d, { filter: "drop-shadow(0 40px 60px rgba(0,0,0,.6)) drop-shadow(0 0 40px rgba(25,195,180,.25))", transformStyle: "preserve-3d" });
  gsap.set(b3d, { rotationY: -28, rotationX: 18, y: 60, opacity: 0 });
  TO(b3d, 0.3, 1.6, { opacity: 1, y: 0, ease: "power3.out" });
  TO(b3d, 0.3, 30, { rotationY: 12, rotationX: 8, ease: "sine.inOut" });
  for (const [e, t] of [[kick, 0.5], [title, 0.75], [sub, 1.1]]) {
    gsap.set(e, { opacity: 0, y: 30 });
    TO(e, t, 0.8, { opacity: 1, y: 0, ease: "power3.out" });
  }
  // s02: who is this for
  const p1 = box(sIntro, 140, 600, 0, 0, "pill", "✓&nbsp; A little C: variables, if, loops");
  const p2 = box(sIntro, 140, 664, 0, 0, "pill", "✓&nbsp; No electronics experience needed");
  css(p1, { width: "auto", height: "auto" }); css(p2, { width: "auto", height: "auto", background: "rgba(255,181,71,.14)", color: "var(--amber)" });
  gsap.set([p1, p2], { opacity: 0 });
  pop(p1, W("s02", "C")); pop(p2, W("s02", "electronics"));
  hide([p1, p2], T("s03") - 0.1, 0.3);
  // s03: today's plan
  const steps = ["Set up the computer", "Connect the board", "Run our first program"];
  const wds = ["set", "connect", "run"];
  steps.forEach((s, i) => {
    const c = box(sIntro, 140 + i * 330, 600, 300, 130, "card", `<div style="padding:22px 24px"><div class="kicker" style="font-size:16px">Today · ${i + 1}</div><div style="font:600 27px var(--display);margin-top:10px">${s}</div></div>`);
    gsap.set(c, { opacity: 0 });
    pop(c, W("s03", wds[i]));
  });
  sceneOut(sIntro, S1("s03") + 0.3);
}

/* ======================================================================
 * WHAT IS AN ESP32
 * ==================================================================== */
const sWhat = SC();
sceneIn(sWhat, S1("s03") + 0.3);
{
  const g1 = box(sWhat, 0, 0, 1920, 1080, "");
  const bx = 250, by = 90, bw = 460, k = bw / 323;
  box(g1, bx, by, bw, 900, "", boardSVG({ pins: 30, chip: "cp2102", p: "bw", width: bw }));
  const P = (x, y) => [bx + (x + 20) * k, by + (y + 20) * k];
  const head = box(g1, 840, 150, 1000, 80, "h2", "A tiny computer on one chip");
  gsap.set(head, { opacity: 0 }); pop(head, T("s04") + 0.3);
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  css(svg, { position: "absolute", left: 0, top: 0, width: "1920px", height: "1080px", overflow: "visible" });
  g1.appendChild(svg);
  const marks = [
    { at: W("s04", "computer"), from: P(141, 160), to: [840, 330], text: "Processor + memory", sub: "runs your C program" },
    { at: W("s04", "WiFi"), from: P(141, 32), to: [840, 470], text: "WiFi + Bluetooth", sub: "talks to your phone and the internet" },
    { at: W("s04", "pins"), from: P(261, 290), to: [840, 610], text: "Pins (GPIO)", sub: "connect LEDs, buttons, sensors" },
  ];
  marks.forEach((m) => {
    const line = document.createElementNS("http://www.w3.org/2000/svg", "path");
    const [x1, y1] = m.from, [x2, y2] = m.to;
    line.setAttribute("d", `M${x1} ${y1} C ${x1 + 160} ${y1}, ${x2 - 160} ${y2}, ${x2 - 16} ${y2}`);
    line.setAttribute("fill", "none"); line.setAttribute("stroke", "#ffb547"); line.setAttribute("stroke-width", "3");
    line.setAttribute("stroke-dasharray", "1200"); line.setAttribute("stroke-dashoffset", "1200");
    svg.appendChild(line);
    const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    dot.setAttribute("cx", x1); dot.setAttribute("cy", y1); dot.setAttribute("r", "9"); dot.setAttribute("fill", "#ffb547");
    dot.style.opacity = 0; svg.appendChild(dot);
    TO(dot, m.at, 0.3, { opacity: 1 });
    TO(line, m.at, 0.7, { strokeDashoffset: 0, ease: "power2.out" });
    const lab = box(g1, x2, y2 - 34, 900, 90, "", `<div style="font:700 38px var(--display)">${m.text}</div><div class="muted" style="font-size:24px">${m.sub}</div>`);
    gsap.set(lab, { opacity: 0, x: -20 });
    TO(lab, m.at + 0.35, 0.5, { opacity: 1, x: 0, ease: "power2.out" });
  });
  hide(g1, T("s05") - 0.3, 0.5);

  // s05 pipeline
  const g2 = box(sWhat, 0, 0, 1920, 1080, "");
  const h2 = box(g2, 0, 170, 1920, 80, "h2", "The big picture");
  h2.style.textAlign = "center";
  gsap.set(h2, { opacity: 0 }); show(h2, T("s05") + 0.1);
  const nodes = [
    ["You write C", `<div class="codecard" style="font-size:21px;padding:0;line-height:1.5"><span class="tk-kw">int</span> x = <span class="tk-num">5</span>;\n<span class="tk-fn">delay</span>(<span class="tk-num">100</span>);</div>`, W("s05", "write")],
    ["Compiler", `<div style="font-size:84px;line-height:1">⚙</div>`, W("s05", "compiler")],
    ["Machine code", `<div style="font:700 26px var(--mono);color:var(--teal);line-height:1.3">01001011<br>11010010<br>00111001</div>`, W("s05", "machine")],
    ["USB cable", `<svg width="120" height="80" viewBox="0 0 120 80"><path d="M6 40 C 40 10, 70 70, 96 40" fill="none" stroke="#ccd" stroke-width="7" stroke-linecap="round"/><rect x="92" y="30" width="24" height="20" rx="3" fill="#aab"/></svg>`, W("s05", "USB")],
    ["ESP32 runs it", boardSVG({ pins: 30, chip: "cp2102", p: "bp", width: 90, labels: false }), W("s05", "runs")],
  ];
  nodes.forEach(([lab, inner, t], i) => {
    const x = 110 + i * 350;
    const c = box(g2, x, 380, 290, 300, "card", `<div style="height:210px;display:flex;align-items:center;justify-content:center">${inner}</div><div style="text-align:center;font:600 28px var(--display)">${lab}</div>`);
    gsap.set(c, { opacity: 0 }); pop(c, t);
    if (i < 4) {
      const a = box(g2, x + 296, 505, 50, 50, "", `<svg width="50" height="50" viewBox="0 0 50 50"><path d="M6 25h34M30 14l11 11-11 11" fill="none" stroke="#19c3b4" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`);
      gsap.set(a, { opacity: 0 }); show(a, t + 0.3, 0.3);
    }
  });
  gsap.set(g2, { opacity: 1 });
  sceneOut(sWhat, S1("s05") + 0.35);
}

/* ======================================================================
 * PLAN (4 things) - also reused by the outro
 * ==================================================================== */
function planCards(parent) {
  const items = [["Arduino IDE", "where we write code"], ["ESP32 board package", "so the IDE can build for this chip"],
    ["USB driver", "so Windows can talk to the board"], ["First program", "Hello, ESP32!"]];
  return items.map(([t, s], i) => {
    const c = box(parent, 110 + i * 435, 400, 400, 300, "card",
      `<div style="padding:34px"><div style="width:64px;height:64px;border-radius:50%;background:rgba(25,195,180,.15);color:var(--teal);font:700 32px var(--display);display:flex;align-items:center;justify-content:center">${i + 1}</div>
       <div style="font:700 34px var(--display);margin-top:28px">${t}</div><div class="muted" style="font-size:23px;margin-top:8px">${s}</div></div>
       <div class="ok" style="position:absolute;right:26px;top:26px;width:58px;height:58px;border-radius:50%;background:var(--green);color:#052;font:700 34px var(--ui);display:flex;align-items:center;justify-content:center;opacity:0">✓</div>`);
    gsap.set(c, { opacity: 0 });
    return c;
  });
}
const sPlan = SC();
sceneIn(sPlan, S1("s05") + 0.35);
{
  const h = box(sPlan, 110, 220, 1200, 80, "h2", "What we need today");
  gsap.set(h, { opacity: 0 }); show(h, T("s06"));
  const cards = planCards(sPlan);
  ["Arduino", "package", "driver", "first"].forEach((w, i) => pop(cards[i], W("s06", w)));
  sceneOut(sPlan, S1("s06") + 0.35);
}

/* ======================================================================
 * DESKTOP
 * ==================================================================== */
const DK = buildDesktop(stage);
const camera = DK.camera;
initCamera(camera);
initCursor(camera);
const chip = el("div", "", "", stage); chip.id = "chip";
textAt(chip, [[0, ""], [T("s07") - 1, "<b>STEP 1</b> Install the Arduino IDE"], [T("s20") - 1, "<b>STEP 2</b> Add ESP32 support"],
  [T("s30") - 1, "<b>STEP 3</b> USB driver and port"], [T("s38") - 1, "<b>STEP 4</b> Our first program"]]);
sceneIn(DK.desk, S1("s06") + 0.35);
for (const sid of ["s07", "s20", "s30", "s38"]) { show(chip, T(sid) - 0.6, 0.3); hide(chip, T(sid) + 5, 0.4); }

/* ---------- download ---------- */
const BR = buildBrowser(camera, { x: 160, y: 24, w: 1600, h: 986, title: "New Tab", url: "" });
const PX = 160, PY = 110; // page origin in desktop coords
const imgSoft = addPageImg(BR, "assets/web/arduino_software_ide.png");
{
  const s = "s07";
  clickAt(DK.iconPos.globe.x, DK.iconPos.globe.y, W(s, "browser") + 0.2);
  pop(BR.win, W(s, "browser") + 0.35);
  // address bar typing
  const url = "arduino.cc/en/software";
  const tt = typingTimes(url, W(s, "go") + 0.1, 16, 3);
  dyn((t) => { const n = countAt(tt, t); BR.url.textContent = url.slice(0, n); });
  clickAt(PX + 400, 66, W(s, "go"), 0.6);
  const loaded = tt.end + 0.45;
  textAt(BR.tab, [[0, "New Tab"], [loaded, "Software | Arduino"]]);
  show(imgSoft, loaded, 0.35);

  // s08: version, Windows option, Download
  const s8 = "s08";
  cam(T(s8) - 0.2, 1.2, 1180, 690, 1.45);
  ring(camera, PX + 885, PY + 456, 200, 38, W(s8, "newest"), W(s8, "Windows") - 0.2);
  ring(camera, PX + 812, PY + 676, 418, 36, W(s8, "Windows"), W(s8, "Download") - 0.1);
  clickAt(PX + 1304, PY + 694, W(s8, "Download"), 0.7);

  // s09: optional donation page
  const don = box(BR.page, 0, 0, 1600, 900, "", `<div style="position:absolute;inset:0;background:rgba(0,30,35,.55)"></div>
    <div style="position:absolute;left:400px;top:170px;width:800px;height:470px;background:#fff;border-radius:6px;color:#1b1b1b;text-align:center;padding:60px 70px;font-family:'Segoe UI'">
      <div style="font:700 30px 'Segoe UI';color:#008184">Support the Arduino IDE</div>
      <div style="font-size:19px;margin-top:22px;line-height:1.5;color:#444">Since its release, the Arduino Software has been downloaded millions of times. Consider supporting its development with a donation. This is optional.</div>
      <div style="display:flex;gap:24px;justify-content:center;margin-top:70px">
        <span class="jd" style="border:2px solid #008184;color:#008184;border-radius:24px;padding:12px 30px;font:700 17px 'Segoe UI'">JUST DOWNLOAD</span>
        <span style="background:#008184;color:#fff;border-radius:24px;padding:12px 30px;font:700 17px 'Segoe UI'">CONTRIBUTE &amp; DOWNLOAD</span></div></div>`);
  gsap.set(don, { opacity: 0 });
  show(don, W(s8, "Download") + 0.5, 0.3);
  camReset(T("s09") - 0.3, 1.0);
  const jd = rect($(".jd", don));
  ring(camera, jd.x - 8, jd.y - 8, jd.w + 16, jd.h + 16, W("s09", "optional"), W("s09", "download") + 0.2);
  clickAt(jd.cx, jd.cy, W("s09", "download"), 0.7);
  hide(don, W("s09", "download") + 0.25, 0.3);
  // download popup
  BR.pop.innerHTML = `<div style="font-weight:600;margin-bottom:6px">Downloads</div><div style="display:flex;gap:10px;align-items:center">
    ${ICONS.arduino.replace(/width="24" height="24"/, 'width="28" height="28"')}<div style="flex:1"><div>arduino-ide_2.3.10_Windows_64bit.exe</div>
    <div class="st" style="color:#aaa;font-size:12px"></div><div class="dl-bar"><i></i></div></div></div>
    <div class="of" style="color:#8ab4f8;margin-top:8px;font-weight:600">Open file</div>`;
  const d0 = W("s09", "download") + 0.3, d1 = S1("s09") + 1.2;
  show(BR.pop, d0, 0.25);
  TO($(".dl-bar i", BR.pop), d0, d1 - d0, { width: "100%", ease: "power1.inOut" });
  dyn((t) => {
    const p = Math.max(0, Math.min(1, (t - d0) / (d1 - d0)));
    $(".st", BR.pop).textContent = p < 1 ? `${(166.4 * p).toFixed(1)} MB of 166 MB` : "166 MB · Done";
    $(".of", BR.pop).style.opacity = p < 1 ? 0 : 1;
  });
}

/* ---------- install ---------- */
const INS = buildInstaller(camera, 650, 270);
const insBtn = rect($('[data-b="agree"]', INS.d));
insBtn.x = insBtn.cx; insBtn.y = insBtn.cy;
{
  const s = "s10";
  const of = rect($(".of", BR.pop));
  clickAt(of.x + 30, of.cy, W(s, "open") + 0.1, 0.8);
  hide(BR.pop, W(s, "open") + 0.3, 0.2);
  pop(INS.d, W(s, "open") + 0.6);
  cam(W(s, "open") + 0.5, 1.0, 960, 512, 1.35);
  const pg = INS.pages;
  const flip = (from, to, t) => { SET(from, t, { opacity: 0 }); SET(to, t, { opacity: 1 }); };
  SET(pg.license, W(s, "open") + 0.6, { opacity: 1 });
  clickAt(insBtn.x, insBtn.y, W(s, "Agree"), 0.7);
  flip(pg.license, pg.options, W(s, "Agree") + 0.15);
  // s11
  ring(camera, 660, 270 + 38 + 84 + 74, 420, 74, W("s11", "everyone") - 0.2, W("s11", "fine") + 0.2);
  clickAt(insBtn.x, insBtn.y, W("s11", "fine") + 0.35, 0.6);
  flip(pg.options, pg.location, W("s11", "fine") + 0.5);
  ring(camera, 664, 270 + 38 + 84 + 104, 590, 52, W("s11", "default"), W("s11", "Install", 2) - 0.1);
  clickAt(insBtn.x, insBtn.y, W("s11", "Install", 2), 0.7);
  const i0 = W("s11", "Install", 2) + 0.15, i1 = T("s12") - 0.1;
  flip(pg.location, pg.installing, i0);
  TO(INS.prog, i0, i1 - i0, { width: "100%", ease: "power1.inOut" });
  textAt(INS.iline, [[0, "Extract: app-64.7z..."], [i0 + (i1 - i0) * 0.55, "Extract: resources\\app\\lib\\backend\\resources\\arduino-cli.exe"], [i1 - 0.4, "Created uninstaller: C:\\Users\\student\\AppData\\Local\\Programs\\Arduino IDE\\Uninstall Arduino IDE.exe"]]);
  flip(pg.installing, pg.finish, W("s12", "done"));
  const rc = rect($(".run", pg.finish));
  ring(camera, rc.x - 8, rc.y - 6, 190, rc.h + 12, W("s12", "Run"), W("s12", "Finish") - 0.1);
  clickAt(insBtn.x, insBtn.y, W("s12", "Finish"), 0.7);
  hide(INS.d, W("s12", "Finish") + 0.15, 0.25);
  hide(BR.win, W("s12", "Finish") + 0.15, 0.25);
  show(DK.icons.arduino, W("s12", "Finish") + 0.3, 0.3);
  SET(DK.icons.arduino, W("s12", "Finish") + 0.3, { className: "tb-ic active" });
  camReset(W("s12", "Finish") + 0.2, 0.9);
  // s13: firewall + driver prompt
  const FW = buildFirewall(camera, 680, 330);
  const DP = buildDriverPrompt(camera, 680, 400);
  pop(FW.d, T("s13") + 0.2);
  const al = rect($(".allow", FW.d));
  clickAt(al.cx, al.cy, W("s13", "driver") - 0.2, 0.7);
  hide(FW.d, W("s13", "driver") - 0.05, 0.2);
  pop(DP.d, W("s13", "driver") + 0.1);
  const di = rect($(".inst", DP.d));
  clickAt(di.cx, di.cy, W("s13", "yes"), 0.7);
  hide(DP.d, W("s13", "yes") + 0.15, 0.2);
}

/* ======================================================================
 * ARDUINO IDE
 * ==================================================================== */
const ide = buildIDE(camera);
const DEFAULT_SKETCH = "void setup() {\n  // put your setup code here, to run once:\n\n}\n\nvoid loop() {\n  // put your main code here, to run repeatedly:\n\n}\n";
const SKETCH = `// ESP32 From Zero - Episode 1: Hello, ESP32!
// Prints a greeting once, then counts the seconds forever.

int seconds = 0;

void setup() {
  Serial.begin(115200);   // open the USB text channel at 115200 baud
  delay(1000);            // give the Serial Monitor a moment to connect
  Serial.println("Hello, ESP32!");
}

void loop() {
  seconds = seconds + 1;
  Serial.printf("I have been running for %d seconds\\n", seconds);
  delay(1000);            // wait one second
}
`;
const lineY = (i) => IDE.codeTop + i * IDE.lineH;
const ideOpen = T("s14") - 0.4;
pop(ide.w, ideOpen, 0.45);
{
  // tour
  const s15 = "s15", s16 = "s16", s17 = "s17";
  cam(T(s15) - 0.3, 1.1, 230, 110, 2.3);
  ring(camera, 15, 61, 36, 36, W(s15, "Verify") - 0.3, W(s15, "arrow") - 0.1);
  callout(camera, "Verify = compile + check", 14, 104, W(s15, "Verify"), W(s15, "arrow") - 0.1);
  ring(camera, 55, 61, 36, 36, W(s15, "arrow"), S1(s15));
  callout(camera, "Upload = compile + send to board", 54, 104, W(s15, "Upload"), S1(s15));
  ring(camera, 132, 61, 240, 36, W(s16, "dropdown") - 0.2, W(s16, "left") - 0.2);
  callout(camera, "Board selector", 160, 104, W(s16, "dropdown"), W(s16, "left") - 0.2);
  cam(W(s16, "left") - 0.3, 1.0, 260, 250, 2.0);
  callout(camera, "Sketchbook", 62, 116, W(s16, "sketchbook"), W(s16, "magnifying") - 0.5);
  callout(camera, "Boards Manager", 62, 166, W(s16, "Boards"), W(s16, "magnifying") - 0.5);
  callout(camera, "Library Manager", 62, 216, W(s16, "Library"), W(s16, "magnifying") - 0.5);
  cam(W(s16, "magnifying") - 0.3, 1.1, 1700, 130, 2.2);
  ring(camera, 1872, 61, 36, 36, W(s16, "magnifying"), S1(s16));
  callout(camera, "Serial Monitor", 1752, 104, W(s16, "Serial"), S1(s16) + 0.2);
  cam(T(s17) - 0.4, 1.1, 520, 250, 1.8);
  dyn((t) => {
    if (t < T("s38")) renderCode(ide.code, DEFAULT_SKETCH, DEFAULT_SKETCH.length, false, 10);
  });
  ring(camera, 112, lineY(0) - 2, 420, 4 * 22 + 4, W(s17, "setup"), W(s17, "loop") + 0.8);
  ring(camera, 112, lineY(5) - 2, 420, 4 * 22 + 4, W(s17, "loop"), S1(s17) + 0.3);
}

/* ======================================================================
 * WHERE IS MAIN?
 * ==================================================================== */
const sMain = SC();
sceneIn(sMain, S1("s17") + 0.4);
{
  const left = box(sMain, 150, 250, 700, 520, "card", `<div class="kicker" style="padding:30px 44px 0">What you write</div>
    <div class="codecard" style="font-size:30px">${hlLines("void setup() {\n  // prepare things\n}\n\nvoid loop() {\n  // repeating work\n}").map((l) => `<div>${l || " "}</div>`).join("")}</div>`);
  const right = box(sMain, 1000, 250, 770, 520, "card", `<div class="kicker" style="padding:30px 44px 0;color:var(--amber)">What Arduino adds for you</div>
    <div class="codecard mc" style="font-size:30px">${hlLines("int main(void) {\n  setup();\n\n  while (1) {\n    loop();\n  }\n}").map((l) => `<div>${l || " "}</div>`).join("")}</div>`);
  const h = box(sMain, 150, 130, 1600, 80, "h2", "Where is <span style=\"color:var(--amber)\">main()</span>?");
  gsap.set([left, right, h], { opacity: 0 });
  pop(h, T("s18") + 0.2); pop(left, W("s18", "Arduino")); pop(right, W("s18", "Behind"));
  // highlights inside the right card: line 2 (setup) and lines 4-6 (loop)
  const ML = [...$(".mc", right).children].map(rect);
  ring(sMain, ML[1].x + 22, ML[1].y - 2, 220, ML[1].h + 4, W("s19", "setup"), W("s19", "loop") - 0.1);
  ring(sMain, ML[3].x + 22, ML[3].y - 2, 300, ML[5].y + ML[5].h - ML[3].y + 4, W("s19", "loop"), S1("s19") + 0.3);
  const once = box(sMain, ML[1].x + 290, ML[1].y + 4, 300, 40, "label", "← runs once");
  const ever = box(sMain, ML[1].x + 370, ML[4].y + 4, 340, 40, "label", "↻ runs forever");
  css(once, { color: "var(--amber)" }); css(ever, { color: "var(--amber)" });
  gsap.set([once, ever], { opacity: 0 });
  pop(once, W("s19", "once")); pop(ever, W("s19", "forever"));
  // spinning loop arrow
  const spin = box(sMain, ML[1].x + 600, ML[4].y - 12, 70, 70, "", `<svg width="70" height="70" viewBox="0 0 70 70"><path d="M58 35a23 23 0 1 1-7-16.5" fill="none" stroke="#ffb547" stroke-width="6" stroke-linecap="round"/><path d="M54 8v14H40" fill="none" stroke="#ffb547" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`);
  gsap.set(spin, { opacity: 0 });
  show(spin, W("s19", "forever"), 0.3);
  TO(spin, W("s19", "forever"), 8, { rotation: 720, ease: "none" });
  sceneOut(sMain, S1("s19") + 0.4);
}

/* ======================================================================
 * STEP 2 - ESP32 board package
 * ==================================================================== */
const URL_ESP = "https://espressif.github.io/arduino-esp32/package_esp32_index.json";
{
  camReset(S1("s19") + 0.3, 0.01);
  const s20 = "s20", s21 = "s21", s22 = "s22", s23 = "s23", s24 = "s24";
  const FM = buildFileMenu(camera);
  cam(T(s20), 1.0, 300, 200, 1.9);
  clickAt(IDE.file.x, IDE.file.y, W(s20, "File"), 0.8);
  show(FM.m, W(s20, "File") + 0.05, 0.12);
  SET(ide.fileMenuLabel, W(s20, "File"), { className: "m-file hl" });
  SET(FM.rows["Preferences..."], W(s20, "Preferences") - 0.4, { className: "hl" });
  const prefY = 54 + 4 + 30 * 9 + 8 * 2 + 15;
  clickAt(90, prefY, W(s20, "Preferences"), 0.6);
  hide(FM.m, W(s20, "Preferences") + 0.1, 0.1);
  SET(ide.fileMenuLabel, W(s20, "Preferences") + 0.1, { className: "m-file" });

  // preferences modal
  const PX0 = 560, PY0 = 170, PW = 800, PH = 680;
  const pref = box(camera, PX0, PY0, PW, PH, "ide-modal");
  const rows = [["Sketchbook location:", `<div class="ide-in" style="width:520px">C:\\Users\\student\\Documents\\Arduino</div>`],
    ["", `<label style="display:flex;gap:8px;align-items:center"><span style="width:14px;height:14px;border:1px solid #888"></span>Show files inside Sketches</label>`],
    ["Editor font size:", `<div class="ide-in" style="width:80px">14</div>`], ["Interface scale:", `<div class="ide-in" style="width:160px">☑ Automatic &nbsp; 100 %</div>`],
    ["Theme:", `<div class="ide-in" style="width:200px">Dark</div>`], ["Language:", `<div class="ide-in" style="width:200px">English</div>`],
    ["Show verbose output during", `<span>☐ compile &nbsp; ☐ upload</span>`], ["Compiler warnings", `<div class="ide-in" style="width:120px">None</div>`],
    ["", `<span>☑ Verify code after upload</span>`], ["", `<span>☑ Auto save</span>`], ["", `<span>☐ Editor Quick Suggestions</span>`],
    ["Additional boards manager URLs:", `<div class="ide-in url" style="width:440px"></div><span style="margin-left:8px">⧉</span>`]];
  pref.innerHTML = `<div class="mh">Preferences <span style="margin-left:auto;font-weight:400">✕</span></div>
    <div style="display:flex;gap:24px;padding:0 24px;border-bottom:1px solid #2e373a;height:34px;align-items:center"><span style="color:#fff;border-bottom:2px solid #0ca1a6;padding-bottom:6px">Settings</span><span style="color:#999;padding-bottom:6px">Network</span></div>
    <div style="padding:16px 24px">${rows.map(([a, b]) => `<div style="display:flex;align-items:center;gap:12px;height:40px"><span style="width:230px">${a}</span>${b}</div>`).join("")}</div>
    <div style="position:absolute;right:24px;bottom:20px;display:flex;gap:12px"><span class="ide-pbtn s">CANCEL</span><span class="ide-pbtn p okb">OK</span></div>`;
  pop(pref, W(s20, "Preferences") + 0.3);
  const urlR = rect($(".url", pref)), okR = rect($(".okb", pref));
  const urlY = urlR.cy;
  cam(T(s21) - 0.2, 1.0, 960, urlY, 1.7);
  ring(camera, PX0 + 16, urlY - 22, urlR.x + urlR.w - PX0 + 34, 44, W(s21, "Find"), W(s21, "paste") + 1.2);
  const urlEl = $(".url", pref);
  textAt(urlEl, [[0, ""], [W(s21, "paste") + 0.3, `<span style="background:#264f78">${URL_ESP}</span>`], [W(s21, "paste") + 0.9, URL_ESP]]);
  const big = box(stage, 260, 880, 1400, 80, "", `<div style="background:rgba(11,18,32,.92);border:1px solid var(--teal);border-radius:16px;padding:16px 26px;font:600 27px var(--mono);color:var(--teal);text-align:center">${URL_ESP}</div>`);
  css(big, { zIndex: 55 }); gsap.set(big, { opacity: 0 });
  pop(big, W(s21, "paste") + 0.4); hide(big, W(s21, "OK") - 0.3);
  const desc = box(stage, 760, 820, 400, 50, "", `<div class="pill" style="background:rgba(255,181,71,.18);color:var(--amber)">📋 Link in the description</div>`);
  css(desc, { zIndex: 55 }); gsap.set(desc, { opacity: 0 });
  pop(desc, W(s21, "description")); hide(desc, W(s21, "OK") - 0.3);
  clickAt(okR.cx, okR.cy, W(s21, "OK"), 0.8);
  hide(pref, W(s21, "OK") + 0.1, 0.2);

  // boards manager
  cam(T(s22) - 0.3, 1.0, 330, 330, 1.9);
  clickAt(IDE.side.boards.x, IDE.side.boards.y, W(s22, "Boards"), 0.8);
  const PANW = 340;
  TO(ide.panel, W(s22, "Boards") + 0.05, 0.25, { width: PANW, ease: "power2.out" });
  TO(ide.main, W(s22, "Boards") + 0.05, 0.25, { left: 56 + PANW, ease: "power2.out" });
  SET(ide.sIcons.sbBoard, W(s22, "Boards"), { className: "si on" });
  ide.panel.innerHTML = `<div style="width:${PANW}px;padding:12px 14px">
    <div style="font-size:12px;font-weight:700;letter-spacing:.5px;margin-bottom:10px">BOARDS MANAGER</div>
    <div class="ide-in q" style="width:100%">&nbsp;</div>
    <div style="display:flex;gap:8px;margin:10px 0;font-size:12px;color:#aaa"><span style="width:40px">Type:</span><div class="ide-in" style="height:24px;width:110px">All</div></div>
    <div class="cards" style="opacity:0">
      <div class="bc c1" style="padding:12px 0;border-bottom:1px solid #2a3336">
        <div><b>Arduino ESP32 Boards</b> <span style="color:#aaa">by Arduino</span></div>
        <div style="color:#aaa;margin:4px 0">2.0.18-arduino.5</div>
        <div style="color:#ccc;line-height:1.45">Boards included in this package:<br>Arduino Nano ESP32</div>
        <div style="color:#0ca1a6;margin:4px 0">More info</div>
        <div style="display:flex;gap:8px;justify-content:flex-end"><div class="ide-in" style="height:28px;width:150px">2.0.18-arduino.5 ▾</div><span class="ide-pbtn s">INSTALL</span></div></div>
      <div class="bc c2" style="padding:12px 0">
        <div><b>esp32</b> <span style="color:#aaa">by Espressif Systems</span></div>
        <div class="ver" style="color:#aaa;margin:4px 0">3.3.12</div>
        <div style="color:#ccc;line-height:1.45">Boards included in this package:<br>ESP32 Dev Board, ESP32-S2 Dev Board, ESP32-S3 Dev Board, ESP32-C3 Dev Board, ESP32-C6 Dev Board, ...</div>
        <div style="color:#0ca1a6;margin:4px 0">More info</div>
        <div style="display:flex;gap:8px;justify-content:flex-end"><div class="ide-in" style="height:28px;width:150px">3.3.12 ▾</div><span class="ide-pbtn s ib">INSTALL</span></div></div>
    </div></div>`;
  const q = $(".q", ide.panel);
  const qt = typingTimes("esp32", W(s22, "search") + 0.3, 8, 5);
  dyn((t) => { const n = countAt(qt, t); const v = "esp32".slice(0, n) || "&nbsp;"; if (q.__v !== v) { q.innerHTML = v; q.__v = v; } });
  show($(".cards", ide.panel), qt.end + 0.3, 0.2);
  // card positions (measured from layout): card1 top ~ 104+12+18+30+42, card2 ~ +190
  const C1 = rect($(".c1", ide.panel)), C2 = rect($(".c2", ide.panel)), IB = rect($(".ib", ide.panel));
  const c1y = C1.y, c2y = C2.y;
  const wrong = ring(camera, 62, c1y - 4, PANW - 12, C1.h + 4, W(s23, "Careful"), W(s23, "Install") - 0.2);
  wrong.style.borderColor = "#ff5d6c";
  wrong.style.boxShadow = "0 0 0 4px rgba(255,93,108,.25)";
  callout(camera, "✕ only for Arduino Nano ESP32", 400, c1y + 70, W(s23, "Careful"), W(s23, "Install") - 0.2, { style: { background: "#ff5d6c", color: "#fff" } });
  ring(camera, 62, c2y - 2, PANW - 12, C2.h + 4, W(s23, "esp32"), W(s23, "Careful") - 0.1);
  callout(camera, "✓ this one", 400, c2y + 80, W(s23, "Espressif", 1), W(s23, "Careful") - 0.1);
  const ib = { x: IB.cx, y: IB.cy };
  clickAt(ib.x, ib.y, W(s23, "Install"), 0.8);
  // install progress
  const i0 = W(s23, "Install") + 0.2, i1 = S1(s24) + 2.2;
  textAt($(".ib", ide.panel), [[0, "INSTALL"], [i0, "INSTALLING"], [i1, "REMOVE"]]);
  textAt($(".ver", ide.panel), [[0, "3.3.12"], [i1, '<span style="color:#0ca1a6">3.3.12 installed</span>']]);
  show(ide.toast, i0, 0.2); TO(ide.toastBar, i0, i1 - i0, { width: "100%", ease: "power1.inOut" }); hide(ide.toast, i1, 0.2);
  logLines(ide.out, [[i0, "Downloading packages"], [i0 + 0.5, "esp32:esp-x32@2511"], [i0 + 1.6, "esp32:xtensa-esp-elf-gdb@16.3_20250913"],
    [i0 + 2.8, "esp32:esptool_py@5.1.0"], [i0 + 4.0, "esp32:mkspiffs@0.2.3"], [i0 + 5.0, "esp32:esp32-arduino-libs@idf-release_v5.5"],
    [i0 + 7.0, "Installing esp32:esp-x32@2511"], [i0 + 8.8, "Configuring platform."], [i1, "Platform <b>esp32:esp32@3.3.12</b> installed"]], 8, [i0 - 0.1, S1("s34") + 0.9]);
  camReset(T(s24) - 0.5, 1.2);
}

/* ======================================================================
 * THE HARDWARE
 * ==================================================================== */
const sBoard = SC();
sceneIn(sBoard, S1("s24") + 2.3);
{
  const s25 = "s25", s26 = "s26", s27 = "s27", s28 = "s28";
  const g = box(sBoard, 0, 0, 1920, 1080, "");
  const bA = box(g, 330, 130, 470, 900, "", boardSVG({ pins: 30, chip: "cp2102", p: "ba", width: 420 }));
  const bB = box(g, 1060, 100, 470, 900, "", boardSVG({ pins: 38, chip: "ch340", p: "bb", width: 420 }));
  const tA = box(g, 330, 990 - 950 + 40, 420, 50, "label", ""); // spacer
  const lA = box(g, 360, 70, 420, 50, "pill", "30 pins"); const lB = box(g, 1090, 40, 420, 50, "pill", "38 pins");
  css(lA, { width: "auto", height: "auto" }); css(lB, { width: "auto", height: "auto" });
  gsap.set([bA, bB, lA, lB], { opacity: 0 });
  pop(bA, T(s25) + 0.3); pop(bB, W(s25, "different"));
  pop(lA, W(s26, "thirty")); pop(lB, W(s26, "thirtyeight"));
  // part rings via svg element boxes
  const kA = 420 / 323, kB = 420 / 323;
  const rA = (x, y, w, h, t0, t1, color) => { const r = ring(g, 330 + (x + 20) * kA, 130 + (y + 20) * kA, w * kA, h * kA, t0, t1); if (color) r.style.borderColor = color; return r; };
  const rB = (x, y, w, h, t0, t1) => ring(g, 1060 + (x + 20) * kB, 100 + (y + 20) * kB, w * kB, h * kB, t0, t1);
  rA(51, 6, 181, 256, W(s26, "metal"), W(s26, "pins") - 0.1); rB(51, 6, 181, 256, W(s26, "metal"), W(s26, "pins") - 0.1);
  rA(4, 60, 30, 370, W(s26, "pins"), W(s26, "buttons") - 0.2); rA(249, 60, 30, 370, W(s26, "pins"), W(s26, "buttons") - 0.2);
  rB(4, 40, 30, 470, W(s26, "pins"), W(s26, "buttons") - 0.2); rB(249, 40, 30, 470, W(s26, "pins"), W(s26, "buttons") - 0.2);
  rA(56, 515 - 100, 48, 64, W(s26, "EN"), S1(s26) + 0.3); rA(283 - 104, 515 - 100, 48, 64, W(s26, "BOOT"), S1(s26) + 0.3);
  rB(56, 544 - 100, 48, 64, W(s26, "EN"), S1(s26) + 0.3); rB(283 - 104, 544 - 100, 48, 64, W(s26, "BOOT"), S1(s26) + 0.3);
  // s27: zoom on usb-serial chips
  hide(g, T(s27) + 0.6, 0.5);
  const g2 = box(sBoard, 0, 0, 1920, 1080, "");
  gsap.set(g2, { opacity: 0 }); show(g2, T(s27) + 0.8, 0.5);
  const hh = box(g2, 0, 120, 1920, 80, "h2", "The USB-to-serial chip"); hh.style.textAlign = "center";
  const sub = box(g2, 0, 200, 1920, 50, "h3 muted", "the bridge between your computer and the ESP32"); sub.style.textAlign = "center";
  const chipCard = (x, title, svg, t) => {
    const c = box(g2, x, 330, 620, 520, "card", `<div style="height:380px;display:flex;align-items:center;justify-content:center">${svg}</div><div style="text-align:center;font:700 44px var(--display)">${title}</div>`);
    gsap.set(c, { opacity: 0 }); pop(c, t); return c;
  };
  chipCard(260, "CP2102", `<svg width="300" height="300" viewBox="0 0 60 60"><rect x="8" y="8" width="44" height="44" rx="3" fill="#121418" stroke="#444"/>${Array.from({ length: 7 }, (_, i) => `<rect x="${13 + i * 5.5}" y="4" width="3" height="4" fill="#b8bec6"/><rect x="${13 + i * 5.5}" y="52" width="3" height="4" fill="#b8bec6"/><rect x="4" y="${13 + i * 5.5}" width="4" height="3" fill="#b8bec6"/><rect x="52" y="${13 + i * 5.5}" width="4" height="3" fill="#b8bec6"/>`).join("")}<circle cx="14" cy="14" r="2" fill="#333"/><text x="30" y="28" text-anchor="middle" font-family="Segoe UI" font-size="6" fill="#aab">SiLabs</text><text x="30" y="37" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="7" fill="#aab">CP2102</text></svg>`, W(s27, "C"));
  chipCard(1040, "CH340", `<svg width="420" height="220" viewBox="0 0 110 50">${Array.from({ length: 8 }, (_, i) => `<rect x="${9 + i * 12.4}" y="2" width="5" height="8" fill="#b8bec6"/><rect x="${9 + i * 12.4}" y="40" width="5" height="8" fill="#b8bec6"/>`).join("")}<rect x="4" y="10" width="102" height="30" rx="2" fill="#121418" stroke="#444"/><circle cx="11" cy="17" r="2" fill="#333"/><text x="55" y="29" text-anchor="middle" font-family="Segoe UI" font-weight="700" font-size="9" fill="#aab">CH340C</text></svg>`, W(s27, "C", 2));
  const rd = box(g2, 560, 880, 800, 60, "", `<div class="pill" style="font-size:26px;background:rgba(255,181,71,.16);color:var(--amber)">🔍 Read the tiny text on yours</div>`);
  rd.style.textAlign = "center"; gsap.set(rd, { opacity: 0 }); pop(rd, W(s27, "read"));
  hide(g2, T(s28) - 0.2, 0.4);
  // s28: cables
  const g3 = box(sBoard, 0, 0, 1920, 1080, "");
  gsap.set(g3, { opacity: 0 }); show(g3, T(s28) + 0.1, 0.4);
  const h3 = box(g3, 0, 130, 1920, 80, "h2", "Not every USB cable carries data"); h3.style.textAlign = "center";
  const cable = (x, title, wires, ok, t) => {
    const c = box(g3, x, 300, 640, 520, "card", `<svg width="640" height="360" viewBox="0 0 640 360"><circle cx="320" cy="180" r="140" fill="#2a2f3a" stroke="#556" stroke-width="6"/>
      ${wires.map(([c, a], i) => `<circle cx="${320 + 70 * Math.cos(a)}" cy="${180 + 70 * Math.sin(a)}" r="34" fill="${c}"/>`).join("")}</svg>
      <div style="text-align:center;font:700 38px var(--display);color:${ok ? "var(--green)" : "var(--red)"}">${title}</div>`);
    gsap.set(c, { opacity: 0 }); pop(c, t);
  };
  cable(240, "✕ Charge-only: 2 wires", [["#e33", Math.PI], ["#222", 0]], false, W(s28, "charge"));
  cable(1040, "✓ Data cable: 4 wires", [["#e33", Math.PI], ["#222", 0], ["#2c4", -Math.PI / 2], ["#eee", Math.PI / 2]], true, W(s28, "detected"));
  hide(g3, T("s29") - 0.2, 0.4);
  // s29: creator clip
  clipFrame(sBoard, "C1", 320, 150, 1280, 720, T("s29") - 0.1, S1("s29") + 1.3, "Plug the USB cable into the board. The red power LED turns on.");
  sceneOut(sBoard, S1("s29") + 1.6);
}

/* ======================================================================
 * STEP 3 - driver (desktop, IDE hidden)
 * ==================================================================== */
{
  const s30 = "s30", s31 = "s31", s32 = "s32", s33 = "s33", s34 = "s34";
  const tHideIDE = S1("s29") + 1.5;
  SET(ide.w, tHideIDE, { opacity: 0 });
  camReset(tHideIDE, 0.01);
  move(1100, 700, tHideIDE, 0.01);
  const WX = buildWinX(camera);
  clickAt(DK.iconPos.start.x, DK.iconPos.start.y, W(s30, "rightclick"), 0.8);
  show(WX.m, W(s30, "rightclick") + 0.1, 0.12);
  SET(WX.rows[5], W(s30, "Device") - 0.4, { className: "hl" });
  clickAt(930, WX.itemY(5), W(s30, "Device") + 0.1, 0.6);
  hide(WX.m, W(s30, "Device") + 0.2, 0.1);
  const DM = buildDevMgr(camera, 580, 110);
  pop(DM.w, W(s30, "Device") + 0.4);
  const rowY = (i) => 110 + 88 + 6 + i * 24;
  dmStates(DM, [[0, "collapsed"], [W(s31, "Open") + 0.5, "ok-cp"], [W(s31, "USB", 1) - 0.1, "ok-ch"], [T(s32) + 0.2, "unknown"], [W(s34, "plug") + 0.2, "ok-ch"]]);
  cam(T(s31) - 0.3, 1.0, 900, 520, 1.7);
  clickAt(640, rowY(13) + 12, W(s31, "Open") + 0.4, 0.7);
  ring(camera, 588, rowY(14), 420, 24, W(s31, "Silicon") - 0.1, W(s31, "USB", 1) - 0.15);
  ring(camera, 588, rowY(14), 280, 24, W(s31, "USB", 1), S1(s31) + 0.2);
  callout(camera, "COM3 ← write it down", 880, rowY(14) - 2, W(s31, "COM", 3), S1(s31) + 0.2);
  ring(camera, 588, rowY(14), 380, 24, W(s32, "unknown"), S1(s32) + 0.4);
  callout(camera, "⚠ no driver yet", 980, rowY(14) - 2, W(s32, "unknown") + 0.2, S1(s32) + 0.4);
  camReset(T(s33) - 0.2, 0.8);
  // driver chooser overlay (screen space)
  const ch = box(stage, 0, 0, 1920, 1080, "");
  css(ch, { zIndex: 45, background: "rgba(8,13,24,.86)" }); gsap.set(ch, { opacity: 0 });
  show(ch, T(s33) - 0.1, 0.4); hide(ch, T(s34) + 0.1, 0.4);
  const dc = (x, chipName, vendor, file, site, t) => {
    const c = box(ch, x, 260, 700, 460, "card", `<div style="padding:44px">
      <div class="kicker">Your chip</div><div style="font:700 64px var(--display);margin:8px 0 26px">${chipName}</div>
      <div class="muted" style="font-size:24px">Download from ${vendor}</div><div style="font:700 34px var(--mono);color:var(--teal);margin:8px 0 24px">${file}</div>
      <div class="muted" style="font:400 22px var(--mono)">${site}</div></div>`);
    gsap.set(c, { opacity: 0 }); pop(c, t);
  };
  dc(200, "CP2102", "Silicon Labs", "CP210x VCP driver", "silabs.com", W(s33, "C", 1));
  dc(1020, "CH340", "WCH", "CH341SER.EXE", "wch-ic.com", W(s33, "C", 3));
  const lk = box(ch, 710, 790, 500, 60, "", `<div class="pill" style="font-size:26px;background:rgba(255,181,71,.16);color:var(--amber)">📋 Both links are in the description</div>`);
  gsap.set(lk, { opacity: 0 }); pop(lk, W(s33, "description"));
  // s34: run the installer
  const DS = buildDriverSetup(camera, 740, 300);
  pop(DS.d, T(s34) + 0.1);
  clickAt(DS.install.x, DS.install.y, W(s34, "installer") + 0.2, 0.7);
  pop(DS.msg, W(s34, "installer") + 0.9);
  hide([DS.d, DS.msg], W(s34, "unplug") - 0.1, 0.25);
  cam(W(s34, "unplug"), 0.9, 900, 520, 1.7);
  ring(camera, 588, rowY(14), 280, 24, W(s34, "COM"), S1(s34) + 0.6);
  hide(DM.w, S1(s34) + 0.7, 0.3);
}

/* ======================================================================
 * SELECT BOARD AND PORT
 * ==================================================================== */
{
  const s35 = "s35", s36 = "s36", s37 = "s37";
  const tIDE = S1("s34") + 0.9;
  camReset(tIDE, 0.01);
  // close the boards manager panel for a clean editor
  SET(ide.panel, tIDE, { width: 0 }); SET(ide.main, tIDE, { left: 56 });
  SET(ide.sIcons.sbBoard, tIDE, { className: "si" });
  pop(ide.w, tIDE, 0.35);
  cam(T(s35), 1.0, 300, 200, 2.0);
  clickAt(IDE.board.x, IDE.board.y, W(s35, "dropdown"), 0.8);
  const dd = box(camera, 136, 96, 300, 76, "menu");
  dd.innerHTML = `<div>${ICONS.usb}&nbsp; COM3 <span style="color:#999;margin-left:6px">Serial Port (USB)</span></div><div class="sel">Select other board and port...</div>`;
  show(dd, W(s35, "dropdown") + 0.05, 0.12);
  SET($(".sel", dd), W(s35, "Select") - 0.35, { className: "sel hl" });
  clickAt(260, 96 + 4 + 30 + 15, W(s35, "Select"), 0.5);
  hide(dd, W(s35, "Select") + 0.1, 0.1);
  // modal
  const MX = 560, MY = 230, MW = 800, MH = 580;
  const md = box(camera, MX, MY, MW, MH, "ide-modal");
  const boards = ["ESP32C3 Dev Module", "ESP32C6 Dev Module", "ESP32-WROOM-DA Module", "ESP32 Dev Module", "ESP32 Wrover Module", "ESP32S3 Dev Module"];
  md.innerHTML = `<div class="mh">Select Other Board and Port <span style="margin-left:auto;font-weight:400">✕</span></div>
    <div style="padding:0 24px 12px;color:#bbb;line-height:1.5">Select both a Board and a Port if you want to upload a sketch.<br>If you only select a Board you will be able to compile, but not to upload your sketch.</div>
    <div style="display:flex;gap:20px;padding:0 24px">
      <div style="flex:1.2"><div style="font-weight:700;font-size:12px;margin-bottom:8px">BOARDS</div><div class="ide-in q">&nbsp;</div>
        <div class="bl" style="margin-top:6px"></div></div>
      <div style="flex:1"><div style="font-weight:700;font-size:12px;margin-bottom:8px">PORTS</div>
        <div class="pt" style="height:30px;display:flex;align-items:center;padding:0 10px">${ICONS.usb}&nbsp; COM3 Serial Port (USB)</div></div></div>
    <div style="position:absolute;left:24px;bottom:24px;color:#888;font-size:12px">☐ Show all ports</div>
    <div style="position:absolute;right:24px;bottom:20px;display:flex;gap:12px"><span class="ide-pbtn s">CANCEL</span><span class="ide-pbtn p">OK</span></div>`;
  pop(md, W(s35, "Select") + 0.3);
  cam(W(s35, "Select") + 0.3, 1.0, 960, 480, 1.55);
  const q = $(".q", md), bl = $(".bl", md), pt = $(".pt", md);
  const qs = "esp32 dev";
  const qt = typingTimes(qs, W(s36, "Search") + 0.2, 10, 9);
  const tPick = W(s36, "Module") + 0.1, tPort = W(s36, "port") + 0.1;
  dyn((t) => {
    const n = countAt(qt, t);
    const v = qs.slice(0, n) || "&nbsp;";
    if (q.__v !== v) { q.innerHTML = v; q.__v = v; }
    const list = n >= qs.length ? boards.filter((b) => /dev/i.test(b)) : boards;
    const sel = t >= tPick;
    const html = list.map((b) => `<div style="height:30px;display:flex;align-items:center;padding:0 10px;${sel && b === "ESP32 Dev Module" ? "background:#0ca1a6;color:#fff" : ""}">${b}${sel && b === "ESP32 Dev Module" ? '<span style="margin-left:auto">✓</span>' : ""}</div>`).join("");
    if (bl.__v !== html) { bl.innerHTML = html; bl.__v = html; }
    const ps = t >= tPort ? "background:#0ca1a6;color:#fff" : "";
    if (pt.__v !== ps) { pt.style.cssText = "height:30px;display:flex;align-items:center;padding:0 10px;" + ps; pt.__v = ps; }
  });
  // list after filter: ESP32C3, ESP32C6, ESP32 Dev Module, ESP32S3 -> "ESP32 Dev Module" is 3rd row
  const listTop = MY + 44 + 56 + 12 + 20 + 6;
  clickAt(MX + 24 + 120, listTop + 2 * 30 + 15, tPick, 0.8);
  clickAt(MX + 24 + 400 + 140, MY + 44 + 56 + 12 + 20 + 15, tPort, 0.8);
  clickAt(MX + MW - 24 - 30, MY + MH - 35, W(s36, "OK"), 0.7);
  hide(md, W(s36, "OK") + 0.1, 0.2);
  textAt(ide.boardText, [[0, "Select Board"], [W(s36, "OK") + 0.1, "ESP32 Dev Module"]]);
  textAt(ide.statusBoard, [[0, "✕ No board selected"], [W(s36, "OK") + 0.1, "ESP32 Dev Module on COM3"]]);
  cam(T(s37) - 0.2, 1.1, 1700, 1000, 2.2);
  ide.statusBoard.textContent = "ESP32 Dev Module on COM3";
  const sbR = rect(ide.statusBoard);
  ring(camera, sbR.x - 8, sbR.y - 3, sbR.w + 16, sbR.h + 6, W(s37, "bottom"), S1(s37) + 0.2);
}

/* ======================================================================
 * STEP 4 - code
 * ==================================================================== */
{
  const s38 = "s38";
  camReset(T(s38) - 0.2, 1.0);
  cam(T(s38) + 1.0, 1.2, 640, 330, 1.6);
  // select all + delete
  const selFlash = box(camera, 120, lineY(0), 520, 22 * 9, "");
  css(selFlash, { background: "rgba(38,79,120,.85)", opacity: 0 });
  const tSel = W(s38, "Delete") - 0.1, tDel = W(s38, "Delete") + 0.4;
  SET(selFlash, tSel, { opacity: 1 }); SET(selFlash, tDel, { opacity: 0 });
  const keys = box(stage, 760, 900, 400, 70, "", "");
  css(keys, { zIndex: 55, textAlign: "center" }); gsap.set(keys, { opacity: 0 });
  textAt(keys, [[0, ""], [tSel - 0.1, `<span class="pill" style="font-size:30px;background:#1b2430;color:#fff">Ctrl + A &nbsp;→&nbsp; Delete</span>`],
    [W("s43", "Control") - 0.1, `<span class="pill" style="font-size:30px;background:#1b2430;color:#fff">Ctrl + S</span>`]]);
  show(keys, tSel - 0.1, 0.2); hide(keys, tDel + 0.8, 0.2);
  // typing plan: pieces aligned to narration
  const pieces = [
    ["// ESP32 From Zero - Episode 1: Hello, ESP32!\n// Prints a greeting once, then counts the seconds forever.\n\n", tDel + 0.6, S1(s38) + 1.3],
    ["int seconds = 0;\n\n", T("s39") + 0.8, S1("s39")],
    ["void setup() {\n  Serial.begin(115200);   // open the USB text channel at 115200 baud\n", T("s40") + 0.2, W("s40", "Serial", 2)],
    ["  delay(1000);            // give the Serial Monitor a moment to connect\n", T("s41") + 0.2, W("s41", "first") + 0.5],
    ["  Serial.println(\"Hello, ESP32!\");\n}\n\n", W("s41", "println") - 0.4, S1("s41")],
    ["void loop() {\n  seconds = seconds + 1;\n", T("s42") + 0.2, W("s42", "print")],
    ["  Serial.printf(\"I have been running for %d seconds\\n\", seconds);\n", W("s42", "print") + 0.1, W("s42", "wait") - 0.3],
    ["  delay(1000);            // wait one second\n}\n", W("s42", "wait") - 0.2, S1("s42") - 0.3],
  ];
  let all = "";
  const times = [];
  pieces.forEach(([txt, a, b], i) => {
    const cps = Math.min(40, Math.max(9, txt.length / Math.max(0.6, b - a)));
    const tt = typingTimes(txt, a, cps, 11 + i);
    all += txt; times.push(...tt);
  });
  if (all !== SKETCH) console.warn("typed text differs from SKETCH");
  dyn((t) => {
    if (t < T(s38)) return;
    const n = t < tDel ? -1 : countAt(times, t);
    if (n < 0) { renderCode(ide.code, DEFAULT_SKETCH, DEFAULT_SKETCH.length, false, 10); return; }
    const blink = Math.floor(t * 1.9) % 2 === 0 || (n > 0 && n < all.length && t - times[n - 1] < 0.5);
    renderCode(ide.code, all, n, blink, 1);
    const lines = all.slice(0, n).split("\n");
    ide.statusLC.textContent = `Ln ${lines.length}, Col ${lines[lines.length - 1].length + 1}`;
  });
  // explanations
  const cx = (col) => IDE.codeX + col * IDE.charW;
  ring(camera, cx(0) - 4, lineY(3) - 1, cx(16) - cx(0) + 8, 24, S1("s39") - 0.6, S1("s39") + 0.6);
  ring(camera, cx(15) - 4, lineY(6) - 1, cx(21) - cx(15) + 8, 24, W("s40", "speed"), S1("s40"));
  callout(camera, "baud rate", cx(15), lineY(6) + 28, W("s40", "baud"), S1("s40"));
  ring(camera, cx(2) - 4, lineY(7) - 1, cx(14) - cx(2) + 8, 24, W("s41", "wait"), W("s41", "println") - 0.2);
  callout(camera, "1000 ms = 1 second", cx(14) + 10, lineY(7) + 26, W("s41", "second"), W("s41", "println") - 0.2);
  ring(camera, cx(2) - 4, lineY(13) - 1, cx(67) - cx(2) + 8, 24, W("s42", "printf"), W("s42", "wait") - 0.3);
  callout(camera, "just like printf in C:  %d → number,  \\n → new line", cx(2), lineY(13) + 28, W("s42", "printf") + 0.2, W("s42", "wait") - 0.3);
  // s43 save
  const SV = box(camera, 170, 200, 800, 380, "w11");
  SV.innerHTML = `<div style="padding:12px 18px;font-size:13px">Save sketch folder as...</div>
    <div style="background:#202020;height:250px;padding:20px 24px;color:#ccc">📁 Documents › Arduino<div style="margin-top:20px;line-height:2;color:#aaa">📁 libraries</div></div>
    <div style="display:flex;align-items:center;gap:12px;padding:14px 24px"><span style="width:110px">File name:</span><div class="tbox fn" style="flex:1;background:#2d2d2d;color:#fff;border-color:#555">sketch_oct16a</div>
    <span class="btn acc svb">Save</span><span class="btn">Cancel</span></div>`;
  const tS = W("s43", "Control") + 0.3;
  pop(SV, tS);
  const fn = $(".fn", SV);
  const nm = "hello_esp32";
  const nt = typingTimes(nm, W("s43", "name") + 0.1, 10, 4);
  dyn((t) => { const n = countAt(nt, t); const v = t < nt[0] ? "sketch_oct16a" : nm.slice(0, n); if (fn.__v !== v) { fn.textContent = v || "\u00a0"; fn.__v = v; } });
  const saveAt = S1("s43") + 0.3;
  const svb = rect($(".svb", SV));
  clickAt(svb.cx, svb.cy, saveAt, 0.6);
  hide(SV, saveAt + 0.1, 0.2);
  textAt(ide.tab, [[0, "sketch_oct16a.ino"], [saveAt + 0.1, "hello_esp32.ino"]]);
  textAt(ide.title, [[0, "sketch_oct16a | Arduino IDE 2.3.10"], [saveAt + 0.1, "hello_esp32 | Arduino IDE 2.3.10"]]);
}

/* ======================================================================
 * UPLOAD
 * ==================================================================== */
{
  const s44 = "s44", s45 = "s45", s46 = "s46", s47 = "s47";
  camReset(T(s44) - 0.6, 1.0);
  clickAt(IDE.upload.x, IDE.upload.y, W(s44, "Upload"), 0.9);
  const u0 = W(s44, "Upload") + 0.1;
  cam(T(s45) - 0.2, 1.1, 560, 880, 1.7);
  const tConn = W(s45, "Connecting") - 0.2;
  const tGo = W(s46, "percentages");
  const tW = W(s47, "Writing"), tW1 = W(s47, "hundred") + 0.2, tHR = W(s47, "Hard");
  textAt(ide.toastText, [[0, "Downloading esp32:esp32@3.3.12"], [u0, "Compiling sketch..."], [tConn - 0.5, "Uploading..."], [tHR + 0.3, "Done uploading."]]);
  SET(ide.toastBar, u0 - 0.01, { width: "0%" });
  show(ide.toast, u0, 0.2); TO(ide.toastBar, u0, tHR - u0, { width: "100%", ease: "none" }); hide(ide.toast, S1(s47) + 1.0, 0.3);
  const dots = (dt) => "Connecting" + ".".repeat(1 + Math.floor(dt * 4) % 60).replace(/(.{5})/g, "$1_");
  const bar = (p) => { const n = Math.round(p * 30); return `Writing at 0x000${(0x10000 + Math.floor(p * 152303)).toString(16)} [${"=".repeat(Math.max(0, n - 1))}${n ? ">" : ""}${" ".repeat(30 - n)}] ${(p * 100).toFixed(1).padStart(5)}% ${Math.floor(p * 152303)}/152303 bytes...`; };
  logLines(ide.out, [
    [u0 + 0.6, ""],
    [W(s45, "compiles") + 0.6, "Sketch uses 269120 bytes (20%) of program storage space. Maximum is 1310720 bytes."],
    [W(s45, "compiles") + 0.7, "Global variables use 22116 bytes (6%) of dynamic memory, leaving 305564 bytes for local variables. Maximum is 327680 bytes."],
    [tConn - 0.6, "esptool v5.1.0"], [tConn - 0.4, "Serial port COM3:"],
    [tConn, (dt) => (dt < tGo - tConn ? dots(dt) : dots(tGo - tConn))],
    [tGo + 0.1, "Connected to ESP32 on COM3:"], [tGo + 0.3, "Chip type:          ESP32-D0WD-V3 (revision v3.1)"],
    [tGo + 0.5, "Features:           Wi-Fi, BT, Dual Core, 240MHz"], [tGo + 0.8, "Uploading stub flasher..."], [tGo + 1.2, "Stub flasher running."],
    [tGo + 1.6, "Configuring flash size..."],
    [tW, (dt) => bar(Math.min(1, dt / (tW1 - tW)))],
    [tW1 + 0.2, "Wrote 269488 bytes (152303 compressed) at 0x00010000 in 2.4 seconds."], [tW1 + 0.4, "Hash of data verified."],
    [tHR, '<span style="color:#0ca1a6">Hard resetting via RTS pin...</span>'],
  ], 8, [S1("s34") + 0.9, 1e9]);
  cam(tW - 0.4, 0.8, 620, 900, 1.6);
  // creator clip: BOOT button (picture in picture)
  clipFrame(stage, "C2", 1140, 90, 720, 405, T(s46) + 0.3, W(s46, "percentages") + 1.6, "Press and hold BOOT, release when the upload starts.");
}

/* ======================================================================
 * SERIAL MONITOR
 * ==================================================================== */
{
  const s48 = "s48", s49 = "s49", s50 = "s50", s51 = "s51", s52 = "s52";
  camReset(T(s48) - 0.4, 0.9);
  clickAt(IDE.monitor.x, IDE.monitor.y, W(s48, "Serial"), 0.9);
  const tOpen = W(s48, "Serial") + 0.1;
  const o1 = $(".o1", ide.btabs), o2 = $(".o2", ide.btabs);
  styleAt(o2, "display", [[0, "none"], [tOpen, "flex"]]);
  dyn((t) => { o1.className = t >= tOpen ? "o1" : "on o1"; o2.className = t >= tOpen ? "on o2" : "o2"; });
  styleAt(ide.out, "display", [[0, "block"], [tOpen, "none"]]);
  styleAt(ide.serial, "display", [[0, "none"], [tOpen, "block"]]);
  cam(T(s49) - 0.2, 1.0, 1640, 860, 1.8);
  cam(T(s50) - 0.3, 1.0, 600, 900, 1.7);
  const tBaud = W(s49, "115200") + 0.2, tEN = W(s51, "EN") + 0.2;
  const garbage = ["⸮⸮⸮xx⸮⸮⸮⸮x⸮⸮x", "x⸮⸮⸮⸮⸮x⸮x⸮⸮⸮x⸮", "⸮x⸮⸮x⸮⸮⸮⸮xx⸮⸮", "⸮⸮⸮x⸮x⸮⸮⸮⸮⸮x"];
  const base = 14; // seconds already counted when we open the monitor
  dyn((t) => {
    if (t < tOpen) return;
    const baudTxt = t < tBaud ? "9600 baud" : "115200 baud";
    let lines = [];
    if (t < tBaud) {
      const k = Math.floor((t - tOpen) * 1.0);
      for (let i = 0; i <= k; i++) lines.push(garbage[i % 4]);
    } else if (t < tEN) {
      const k = Math.floor(t - tBaud);
      for (let i = 0; i <= k; i++) lines.push(`I have been running for ${base + i} seconds`);
    } else {
      lines = ["ets Jul 29 2019 12:21:46", "", "rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)", "load:0x3fff0030,len:4980", "entry 0x400805f0"];
      if (t > tEN + 1.0) lines.push('<span style="color:#7fcbcd">Hello, ESP32!</span>');
      const k = Math.floor(t - tEN - 1.0);
      for (let i = 1; i <= k; i++) lines.push(`I have been running for ${i} seconds`);
    }
    const html = `<div style="display:flex;gap:12px;align-items:center;margin:-2px 0 8px;font-family:var(--ui)"><div class="ide-in" style="flex:1;color:#888">Message (Enter to send message to 'ESP32 Dev Module' on 'COM3')</div>
      <div class="ide-in" style="width:110px">New Line ▾</div><div class="ide-in" style="width:130px;${t >= tBaud - 1.2 && t < tBaud + 1.5 ? "border-color:#ffb547" : ""}">${baudTxt} ▾</div></div>` +
      lines.slice(-6).map((l) => `<div>${l || "&nbsp;"}</div>`).join("");
    if (ide.serial.__v !== html) { ide.serial.innerHTML = html; ide.serial.__v = html; }
  });
  callout(camera, "must match Serial.begin(115200)", 1560, 790, W(s49, "same"), S1(s49) + 0.4);
  clipFrame(stage, "C3", 1140, 90, 720, 405, T(s51), S1(s51) + 1.0, "Press the EN button once.");
  // s52 side by side
  const cmp = box(stage, 0, 0, 1920, 1080, "");
  css(cmp, { zIndex: 45, background: "rgba(8,13,24,.86)" }); gsap.set(cmp, { opacity: 0 });
  show(cmp, T(s52) - 0.1, 0.35); hide(cmp, S1(s52) + 0.5, 0.35);
  box(cmp, 220, 340, 700, 300, "card", `<div style="padding:40px"><div class="kicker" style="color:var(--red)">9600 ≠ 115200</div><div style="font:600 40px var(--mono);margin-top:30px">⸮⸮⸮xx⸮⸮x⸮⸮⸮</div></div>`);
  box(cmp, 1000, 340, 700, 300, "card", `<div style="padding:40px"><div class="kicker" style="color:var(--green)">115200 = 115200</div><div style="font:600 40px var(--mono);margin-top:30px">Hello, ESP32!</div></div>`);
}

/* ======================================================================
 * TROUBLESHOOTING + OUTRO
 * ==================================================================== */
const sTrouble = SC();
sceneIn(sTrouble, S1("s52") + 0.6);
SET(DK.desk, S1("s52") + 1.3, { opacity: 0 });
hide(chip, S1("s52") + 0.4, 0.3);
{
  const s = "s53";
  const h = box(sTrouble, 160, 150, 1600, 80, "h2", "Common problems"); gsap.set(h, { opacity: 0 }); pop(h, T(s));
  const rows = [["No COM port?", "Check the cable, then the driver", W(s, "COM")], ["Stuck at “Connecting...”?", "Hold the BOOT button", W(s, "Stuck")],
    ["Strange characters?", "Set the baud rate to match your code", W(s, "Strange")]];
  rows.forEach(([a, b, t], i) => {
    const c = box(sTrouble, 160, 300 + i * 190, 1600, 160, "card", `<div style="display:flex;align-items:center;height:160px;padding:0 50px;gap:40px">
      <div style="font:700 42px var(--display);width:640px">${a}</div><div style="font-size:40px;color:var(--teal)">→</div><div style="font:600 36px var(--ui);color:var(--muted)">${b}</div></div>`);
    gsap.set(c, { opacity: 0 }); pop(c, t);
  });
  sceneOut(sTrouble, S1(s) + 0.4);
}
const sOutro = SC();
sceneIn(sOutro, S1("s53") + 0.4);
{
  const h = box(sOutro, 110, 220, 1500, 80, "h2", "Episode 1 complete!"); gsap.set(h, { opacity: 0 }); pop(h, T("s54"));
  const cards = planCards(sOutro);
  cards.forEach((c) => SET(c, T("s54") - 0.1, { opacity: 1 }));
  ["installed", "added", "found", "ran"].forEach((w, i) => {
    const ok = $(".ok", cards[i]);
    SET(ok, W("s54", w) - 0.001, { scale: 0.4 });
    TO(ok, W("s54", w), 0.4, { opacity: 1, scale: 1, ease: "back.out(2)" });
  });
  hide(cards, T("s55") - 0.1, 0.4); hide(h, T("s55") - 0.1, 0.4);
  const nx = box(sOutro, 260, 260, 1400, 330, "card", `<div style="padding:50px 60px"><div class="kicker">Next episode</div>
    <div style="font:700 60px var(--display);margin:14px 0 18px">Pins, the Breadboard &amp; Your First Circuit</div>
    <div class="muted" style="font-size:28px">We'll meet the board's pins and blink a real LED.</div></div>`);
  gsap.set(nx, { opacity: 0 }); pop(nx, T("s55") + 0.2);
  const gh = box(sOutro, 260, 640, 1400, 120, "card", `<div style="display:flex;align-items:center;gap:26px;height:120px;padding:0 50px">
    <svg width="54" height="54" viewBox="0 0 16 16"><path fill="#fff" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
    <div style="font:600 36px var(--mono)">github.com/emjnbulut/esp32-from-zero</div></div>`);
  gsap.set(gh, { opacity: 0 }); pop(gh, W("s55", "GitHub"));
  const fade = box(stage, 0, 0, 1920, 1080, ""); css(fade, { background: "#000", zIndex: 200, opacity: 0 });
  TO(fade, D.schedule.duration - 1.2, 1.2, { opacity: 1, ease: "none" });
}

window.__seek(0);
window.__ready = true;
