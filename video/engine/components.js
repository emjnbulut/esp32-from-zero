/* Desktop UI recreations: Windows 11 desktop, browser, installer, Arduino IDE 2,
 * Device Manager, dialogs. Everything is drawn in desktop coordinates (1920x1080,
 * taskbar 48px), and lives inside #camera so the camera can zoom into it. */

const ICONS = {
  start: `<svg width="22" height="22" viewBox="0 0 22 22"><rect x="1" y="1" width="9.5" height="9.5" fill="#4cc2ff"/><rect x="11.5" y="1" width="9.5" height="9.5" fill="#4cc2ff"/><rect x="1" y="11.5" width="9.5" height="9.5" fill="#4cc2ff"/><rect x="11.5" y="11.5" width="9.5" height="9.5" fill="#4cc2ff"/></svg>`,
  search: `<svg width="22" height="22" viewBox="0 0 22 22"><circle cx="9" cy="9" r="6.5" fill="none" stroke="#fff" stroke-width="2"/><path d="M14 14l6 6" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>`,
  folder: `<svg width="24" height="22" viewBox="0 0 24 22"><path d="M1 4a2 2 0 012-2h6l2 3h10a2 2 0 012 2v11a2 2 0 01-2 2H3a2 2 0 01-2-2z" fill="#f8c74a"/><path d="M1 8h22v10a2 2 0 01-2 2H3a2 2 0 01-2-2z" fill="#ffd866"/></svg>`,
  globe: `<svg width="24" height="24" viewBox="0 0 24 24"><defs><linearGradient id="gb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5ad1ff"/><stop offset="1" stop-color="#1a6dff"/></linearGradient></defs><circle cx="12" cy="12" r="11" fill="url(#gb)"/><path d="M1 12h22M12 1c4 4 4 18 0 22M12 1c-4 4-4 18 0 22" fill="none" stroke="#fff" stroke-width="1.4" opacity=".9"/></svg>`,
  arduino: `<svg width="24" height="24" viewBox="0 0 24 24"><rect x="0" y="0" width="24" height="24" rx="6" fill="#0ca1a6"/><path d="M7.5 8.5a3.5 3.5 0 100 7c2.3 0 3.4-2.2 4.5-3.5 1.1-1.3 2.2-3.5 4.5-3.5a3.5 3.5 0 110 7c-2.3 0-3.4-2.2-4.5-3.5-1.1-1.3-2.2-3.5-4.5-3.5z" fill="none" stroke="#fff" stroke-width="1.7"/><path d="M5.8 12h3.4M15.8 12h3.4M17.5 10.3v3.4" stroke="#fff" stroke-width="1.3"/></svg>`,
  check: `<svg width="16" height="16" viewBox="0 0 16 16"><path d="M3 8.5l3.2 3L13 4.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  arrow: `<svg width="16" height="16" viewBox="0 0 16 16"><path d="M2.5 8h10M9 4l4 4-4 4" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  debug: `<svg width="16" height="16" viewBox="0 0 16 16"><path d="M5 3l8 5-8 5z" fill="none" stroke="#9fb" stroke-opacity=".5" stroke-width="1.8"/></svg>`,
  usb: `<svg width="14" height="14" viewBox="0 0 14 14"><path d="M7 1v10M7 11a1.6 1.6 0 100 .1M4 5v2l3 2M10 4v2.5L7 8" fill="none" stroke="#ccc" stroke-width="1.2"/></svg>`,
  plotter: `<svg width="20" height="20" viewBox="0 0 20 20"><path d="M2 12l4-7 4 10 3-6 2 3h3" fill="none" stroke="#ddd" stroke-width="1.7"/></svg>`,
  monitor: `<svg width="22" height="22" viewBox="0 0 22 22"><circle cx="10" cy="10" r="5.5" fill="none" stroke="#ddd" stroke-width="1.8"/><path d="M14 14l5 5M1 10h3M16 10h3M10 1v3" stroke="#ddd" stroke-width="1.8" stroke-linecap="round"/><circle cx="10" cy="10" r="1.6" fill="#ddd"/></svg>`,
  sbFolder: `<svg width="26" height="22" viewBox="0 0 26 22"><path d="M2 3h8l2 3h12v14H2z" fill="none" stroke="#ccc" stroke-width="1.7"/></svg>`,
  sbBoard: `<svg width="26" height="24" viewBox="0 0 26 24"><rect x="2" y="4" width="22" height="16" rx="2" fill="none" stroke="#ccc" stroke-width="1.7"/><path d="M6 4V1M11 4V1M16 4V1M21 4V1M6 20v3M11 20v3M16 20v3M21 20v3" stroke="#ccc" stroke-width="1.5"/><rect x="8" y="9" width="10" height="6" fill="none" stroke="#ccc" stroke-width="1.4"/></svg>`,
  sbLib: `<svg width="26" height="24" viewBox="0 0 26 24"><path d="M3 2v20M8 2v20M13 4v18M17 3l6 18" stroke="#ccc" stroke-width="2.2"/></svg>`,
  sbDebug: `<svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="#ccc" stroke-width="1.8"/><path d="M5.5 18.5l13-13" stroke="#ccc" stroke-width="1.8"/></svg>`,
  sbSearch: `<svg width="24" height="24" viewBox="0 0 24 24"><circle cx="10" cy="10" r="7" fill="none" stroke="#ccc" stroke-width="1.8"/><path d="M15 15l6 6" stroke="#ccc" stroke-width="2"/></svg>`,
  lock: `<svg width="14" height="14" viewBox="0 0 14 14"><rect x="2.5" y="6" width="9" height="7" rx="1.5" fill="#bbb"/><path d="M4.5 6V4.5a2.5 2.5 0 015 0V6" fill="none" stroke="#bbb" stroke-width="1.4"/></svg>`,
  shield: `<svg width="20" height="20" viewBox="0 0 20 20"><path d="M10 1l8 3v6c0 5-4 8-8 9-4-1-8-4-8-9V4z" fill="#3a8ee6"/></svg>`,
  warn: `<svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 1l7 13H1z" fill="#ffcc00" stroke="#8a6d00" stroke-width=".8"/><path d="M8 5.5v4.5M8 11.5v1.2" stroke="#000" stroke-width="1.6"/></svg>`,
  port: `<svg width="18" height="16" viewBox="0 0 18 16"><rect x="1" y="3" width="16" height="10" rx="2" fill="#7a8a99"/><rect x="4" y="6" width="10" height="4" fill="#dfe7ee"/></svg>`,
  pc: `<svg width="18" height="16" viewBox="0 0 18 16"><rect x="1" y="1" width="16" height="10" rx="1" fill="#4a90d9"/><rect x="6" y="12" width="6" height="2" fill="#777"/></svg>`,
  dev: `<svg width="18" height="16" viewBox="0 0 18 16"><rect x="2" y="2" width="14" height="12" rx="2" fill="#9aa7b3"/></svg>`,
};

/* ---------- desktop ---------- */
function buildDesktop(stage) {
  const desk = el("div", "", "", stage); desk.id = "desk";
  const camera = el("div", "", "", desk); camera.id = "camera";
  el("div", "wallpaper", "", camera);
  const tb = el("div", "taskbar", "", camera);
  const names = ["start", "search", "folder", "globe", "arduino"];
  const icons = {};
  names.forEach((n) => { icons[n] = el("div", "tb-ic", ICONS[n], tb); });
  icons.arduino.style.opacity = 0;
  el("div", "tb-tray", `<span style="font-size:14px">⌃ &nbsp;📶 🔊</span><div>4:12 PM<br>10/16/2026</div>`, tb);
  // taskbar icon centres (desktop coords)
  const iconX = (i) => 960 - (5 * 40 + 4 * 6) / 2 + 20 + i * 46;
  const pos = {}; names.forEach((n, i) => (pos[n] = { x: iconX(i), y: 1056 }));
  return { desk, camera, taskbar: tb, icons, iconPos: pos };
}

function winCaps(dark = true) {
  return `<div class="caps"><span>—</span><span>☐</span><span>✕</span></div>`;
}

/* ---------- browser ---------- */
function buildBrowser(parent, { x, y, w, h, title, url }) {
  const win = box(parent, x, y, w, h, "win");
  const top = el("div", "br-top", "", win);
  const tabs = el("div", "br-tabs", "", top);
  const tab = el("div", "br-tab", `${ICONS.globe.replace('width="24" height="24"', 'width="14" height="14"')}<span class="t">${title}</span><span style="margin-left:auto;color:#aaa">✕</span>`, tabs);
  el("div", "", winCaps(), tabs);
  const bar = el("div", "br-bar", `<span class="br-nav">←</span><span class="br-nav">→</span><span class="br-nav">⟳</span>`, top);
  const urlBox = el("div", "br-url", `${ICONS.lock}<span class="u"></span>`, bar);
  el("span", "br-nav", "⤓", bar);
  const page = el("div", "br-page", "", win);
  const pop = el("div", "dl-pop", "", win);
  return { win, tab: $(".t", tab), url: $(".u", urlBox), page, pop };
}
function addPageImg(b, src, opts = {}) {
  const img = el("img", "", null, b.page);
  img.src = src; img.style.opacity = opts.visible ? 1 : 0;
  return img;
}

/* ---------- NSIS installer (Arduino IDE Setup) ---------- */
function buildInstaller(parent, x, y) {
  const W = 620, H = 484;
  const d = box(parent, x, y, W, H, "cl");
  el("div", "titlebar", `${ICONS.arduino.replace(/width="24" height="24"/, 'width="16" height="16"')}<span>Arduino IDE Setup</span>` +
    `<div class="caps"><span>—</span><span style="color:#bbb">☐</span><span>✕</span></div>`, d);
  const logo = ICONS.arduino.replace(/width="24" height="24"/, 'width="56" height="56" class="logo"');
  const pages = {};
  const page = (name, hdr, sub, body, buttons, noHeader) => {
    const p = box(d, 0, 38, W, H - 38, "");
    p.style.opacity = 0;
    if (!noHeader) el("div", "hdr", `<b>${hdr}</b><div class="sub">${sub}</div>${logo}`, p);
    el("div", "body", body, p);
    el("div", "foot", `<span class="nsis">Nullsoft Install System v3.08</span>${buttons}`, p);
    pages[name] = p;
    return p;
  };
  page("license", "License Agreement", "Please review the license terms before installing Arduino IDE.",
    `<div>Press Page Down to see the rest of the agreement.</div>
     <div class="tbox" style="height:170px;margin:8px 0;font-size:13px;line-height:1.4;overflow:hidden">GNU AFFERO GENERAL PUBLIC LICENSE<br>Version 3, 19 November 2007<br><br>Copyright (C) 2007 Free Software Foundation, Inc.<br>Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.<br><br>Preamble<br>The GNU Affero General Public License is a free, copyleft license for software and other kinds of works...</div>
     <div style="font-size:14px">If you accept the terms of the agreement, click I Agree to continue. You must accept the agreement to install Arduino IDE.</div>`,
    `<span class="btn" data-b="agree">I Agree</span><span class="btn">Cancel</span>`);
  page("options", "Choose Installation Options", "Who should this application be installed for?",
    `<div>Please select whether you wish to make this software available to all users or just yourself</div>
     <div style="margin:22px 0 0 10px"><div class="radio"><i></i>Anyone who uses this computer (all users)</div><div class="radio"><i class="on"></i>Only for me (student)</div></div>
     <div style="margin-top:40px;font-size:14px">Fresh install for current user only.</div>`,
    `<span class="btn">&lt; Back</span><span class="btn def" data-b="next">Next &gt;</span><span class="btn">Cancel</span>`);
  page("location", "Choose Install Location", "Choose the folder in which to install Arduino IDE.",
    `<div>Setup will install Arduino IDE in the following folder. To install in a different folder, click Browse and select another folder. Click Install to start the installation.</div>
     <div style="margin-top:28px;border:1px solid #c8c8c8;padding:14px 12px 16px;position:relative"><span style="position:absolute;top:-11px;left:8px;background:#f0f0f0;padding:0 4px">Destination Folder</span>
     <div style="display:flex;gap:10px"><div class="tbox" style="flex:1">C:\\Users\\student\\AppData\\Local\\Programs\\Arduino IDE</div><span class="btn">Browse...</span></div></div>
     <div style="margin-top:24px">Space required: 569.3 MB<br>Space available: 112.8 GB</div>`,
    `<span class="btn">&lt; Back</span><span class="btn def" data-b="install">Install</span><span class="btn">Cancel</span>`);
  page("installing", "Installing", "Please wait while Arduino IDE is being installed.",
    `<div class="iline" style="margin-top:10px">Extract: app-64.7z...</div><div class="prog" style="margin-top:12px"><i></i></div>`,
    `<span class="btn dis">&lt; Back</span><span class="btn dis">Next &gt;</span><span class="btn dis">Cancel</span>`);
  const fin = page("finish", "", "",
    `<div style="position:absolute;left:0;top:0;width:186px;height:368px;background:linear-gradient(160deg,#0ca1a6,#006468)">
       ${ICONS.arduino.replace(/width="24" height="24"/, 'width="92" height="92" style="margin:44px 47px"')}</div>
     <div style="position:absolute;left:206px;top:16px;right:18px">
       <div style="font-size:22px;font-weight:700;margin-bottom:18px">Completing Arduino IDE Setup</div>
       <div>Arduino IDE has been installed on your computer.<br><br>Click Finish to close Setup.</div>
       <div class="check run" style="margin-top:24px"><i class="on">✓</i>Run Arduino IDE</div></div>`,
    `<span class="btn dis">&lt; Back</span><span class="btn def" data-b="finish">Finish</span><span class="btn dis">Cancel</span>`, true);
  fin.style.background = "#fff";
  const btnPos = { right3: { x: x + W - 70 - 16, y: y + H - 29 }, mid3: { x: x + W - 16 - 100 - 10 - 50, y: y + H - 29 },
    first2: { x: x + W - 16 - 100 - 10 - 50, y: y + H - 29 } };
  return { d, pages, prog: $(".prog i", pages.installing), iline: $(".iline", pages.installing), btnPos, W, H };
}

/* ---------- Windows dialogs ---------- */
function buildFirewall(parent, x, y) {
  const d = box(parent, x, y, 560, 380, "w11");
  d.innerHTML = `<div style="padding:12px 18px;font-size:12px">Windows Security</div>
    <div style="padding:6px 24px 16px;font:600 20px var(--ui)">Do you want to allow public and private networks to access this app?</div>
    <div style="background:#202020;padding:18px 24px;height:190px">
      <div>Windows Firewall has blocked some features of mdns-discovery on all public and private networks.</div>
      <div style="display:flex;align-items:center;gap:12px;margin:18px 0 10px">${ICONS.dev}<span style="font:600 18px var(--ui)">mdns-discovery</span></div>
      <div><b>Publisher</b> &nbsp; Unknown</div><div style="color:#9cd0ff;margin-top:10px">Show more</div></div>
    <div style="display:flex;gap:10px;padding:14px 24px"><span class="btn acc allow" style="flex:1">Allow</span><span class="btn" style="flex:1">Cancel</span></div>`;
  return { d, allow: { x: x + 24 + 126, y: y + 380 - 30 } };
}
function buildDriverPrompt(parent, x, y) {
  const d = box(parent, x, y, 560, 250, "cl");
  d.innerHTML = `<div class="titlebar">${ICONS.shield}<span>Windows Security</span><div class="caps"><span>✕</span></div></div>
    <div style="background:#fff;padding:18px 22px 14px;height:150px">
      <div style="font-size:17px;color:#1a3f8a;margin-bottom:16px">Would you like to install this device software?</div>
      <div style="display:flex;gap:14px;align-items:flex-start">${ICONS.port}<div>Name: Arduino srl Ports (COM &amp; LPT)<br>Publisher: Arduino srl</div></div></div>
    <div style="display:flex;justify-content:flex-end;gap:10px;padding:16px 18px"><span class="btn def inst">Install</span><span class="btn">Don't Install</span></div>`;
  return { d, install: { x: x + 560 - 18 - 100 - 10 - 50, y: y + 250 - 32 } };
}

/* ---------- Device Manager ---------- */
const DM_ROWS = ["Audio inputs and outputs", "Batteries", "Bluetooth", "Computer", "Disk drives", "Display adapters", "Firmware",
  "Human Interface Devices", "Keyboards", "Mice and other pointing devices", "Monitors", "Network adapters"];
const DM_ROWS2 = ["Print queues", "Processors", "Security devices", "Software devices", "Sound, video and game controllers",
  "Storage controllers", "System devices", "Universal Serial Bus controllers"];
function buildDevMgr(parent, x, y, { variant = "ok" } = {}) {
  const W = 760, H = 760;
  const w = box(parent, x, y, W, H, "win dm");
  el("div", "titlebar", `${ICONS.pc}<span>Device Manager</span>${winCaps()}`, w);
  el("div", "dm-menu", `<span>File</span><span>Action</span><span>View</span><span>Help</span>`, w);
  el("div", "dm-tool", `← → ▦ ? ▣`, w);
  const tree = el("div", "dm-tree", "", w);
  const row = (txt, lvl, icon, cls = "", chev = "›") => el("div", "dm-row " + cls,
    `<span style="width:${lvl * 22}px"></span><span class="chev">${chev}</span>${icon}<span>${txt}</span>`, tree);
  row("DESKTOP-ESP32", 0, ICONS.pc, "", "⌄");
  DM_ROWS.forEach((r) => row(r, 1, ICONS.dev));
  const other = row("Other devices", 1, ICONS.dev, "", "⌄");
  const unk = row("CP2102 USB to UART Bridge Controller", 2, ICONS.warn, "", "");
  const ports = row("Ports (COM &amp; LPT)", 1, ICONS.port, "", "›");
  const p1 = row("Silicon Labs CP210x USB to UART Bridge (COM3)", 2, ICONS.port, "", "");
  const p2 = row("USB-SERIAL CH340 (COM3)", 2, ICONS.port, "", "");
  DM_ROWS2.forEach((r) => row(r, 1, ICONS.dev));
  // rows are re-laid out by the scene with setDM()
  return { w, tree, rows: { other, unk, ports, p1, p2 }, x, y };
}
/** device-manager tree state over time: list = [[t, 'collapsed'|'ok-cp'|'ok-ch'|'unknown'], ...] */
function dmStates(dm, list) {
  const R = dm.rows;
  dyn((t) => {
    const st = stateAt(list, t);
    if (dm.__st === st) return;
    dm.__st = st;
    const vis = { other: st === "unknown", unk: st === "unknown", ports: st !== "unknown", p1: st === "ok-cp", p2: st === "ok-ch" };
    for (const k in vis) R[k].style.display = vis[k] ? "flex" : "none";
    R.ports.querySelector(".chev").innerHTML = st === "collapsed" ? "›" : "⌄";
  });
}

function buildWinX(parent) {
  const items = ["Installed apps", "Mobility Center", "Power Options", "Event Viewer", "System", "Device Manager", "Network Connections",
    "Disk Management", "Computer Management", "Terminal", "Terminal (Admin)", "Task Manager", "Settings", "File Explorer", "Search", "Run", "Shut down or sign out  ›", "Desktop"];
  const m = box(parent, 846, 1032 - 4 - items.length * 30 - 12, 270, items.length * 30 + 10, "menu");
  const rows = items.map((i) => el("div", "", i, m));
  return { m, rows, itemY: (i) => 1032 - 4 - items.length * 30 - 12 + 4 + i * 30 + 15 };
}

/* ---------- WCH driver setup ---------- */
function buildDriverSetup(parent, x, y) {
  const d = box(parent, x, y, 440, 300, "cl");
  d.innerHTML = `<div class="titlebar"><span>DriverSetup(X64)</span><div class="caps"><span>✕</span></div></div>
    <div style="padding:14px 18px;position:relative;height:262px">
      <div style="border:1px solid #c8c8c8;padding:16px;position:relative;height:200px">
        <span style="position:absolute;top:-11px;left:8px;background:#f0f0f0;padding:0 4px">Device Driver Install / UnInstall</span>
        <div style="display:flex;gap:10px;align-items:center">Select INF <div class="tbox" style="flex:1;padding:4px 8px">CH341SER.INF</div></div>
        <div style="display:flex;flex-direction:column;gap:10px;margin:18px 0 0 120px;width:140px"><span class="btn" data-b="install">INSTALL</span><span class="btn">UNINSTALL</span><span class="btn">HELP</span></div>
        <div style="position:absolute;right:14px;bottom:10px;color:#2b6cb0;font-weight:700">WCH.CN</div></div></div>`;
  const msg = box(parent, x + 90, y + 100, 300, 150, "cl");
  msg.innerHTML = `<div class="titlebar"><span>DriverSetup</span><div class="caps"><span>✕</span></div></div>
    <div style="background:#fff;height:62px;padding:20px 18px;display:flex;gap:12px;align-items:center"><span style="color:#2b6cb0;font-size:22px">ℹ</span>Driver install success!</div>
    <div style="display:flex;justify-content:flex-end;padding:9px 14px"><span class="btn def">OK</span></div>`;
  return { d, msg, install: { x: x + 18 + 16 + 120 + 70, y: y + 38 + 14 + 16 + 34 + 18 + 16 } };
}

/* ---------- Arduino IDE 2 ---------- */
const IDE = { verify: { x: 33, y: 79 }, upload: { x: 73, y: 79 }, board: { x: 252, y: 79 }, plotter: { x: 1846, y: 79 }, monitor: { x: 1890, y: 79 },
  side: { sketchbook: { x: 28, y: 128 }, boards: { x: 28, y: 178 }, library: { x: 28, y: 228 }, debug: { x: 28, y: 278 }, search: { x: 28, y: 328 } },
  file: { x: 23, y: 42 }, codeTop: 144, lineH: 22, codeX: 120, charW: 9.03, outTop: 832, status: 1021 };

function buildIDE(parent) {
  const w = box(parent, 0, 0, 1920, 1032, "win max ide");
  const title = el("div", "titlebar", `${ICONS.arduino.replace(/width="24" height="24"/, 'width="15" height="15"')}<span class="t">sketch_oct16a | Arduino IDE 2.3.10</span>${winCaps()}`, w);
  const menu = el("div", "ide-menu", `<span class="m-file">File</span><span>Edit</span><span>Sketch</span><span>Tools</span><span>Help</span>`, w);
  const tool = el("div", "ide-tool", "", w);
  const bVerify = el("div", "ide-btn", ICONS.check, tool);
  const bUpload = el("div", "ide-btn", ICONS.arrow, tool);
  el("div", "ide-btn dis", ICONS.debug, tool);
  const board = el("div", "ide-board", `${ICONS.usb}<span class="bt">Select Board</span><span class="caret">▼</span>`, tool);
  el("div", "ide-right", `<span>${ICONS.plotter}</span><span class="mon">${ICONS.monitor}</span>`, tool);
  const side = el("div", "ide-side", "", w);
  const sIcons = {};
  for (const k of ["sbFolder", "sbBoard", "sbLib", "sbDebug", "sbSearch"]) sIcons[k] = el("div", "si", ICONS[k], side);
  el("div", "si", `<svg width="26" height="26" viewBox="0 0 26 26"><circle cx="13" cy="13" r="11" fill="none" stroke="#ccc" stroke-width="1.6"/><circle cx="13" cy="10" r="4" fill="none" stroke="#ccc" stroke-width="1.6"/><path d="M5.5 20.5c2-3.5 13-3.5 15 0" fill="none" stroke="#ccc" stroke-width="1.6"/></svg>`, side).style.marginTop = "auto";
  side.lastChild.style.marginBottom = "14px";
  const panel = el("div", "ide-panel", "", w);
  const main = el("div", "ide-main", "", w);
  const tabs = el("div", "ide-tabs", "", main);
  const tab = el("div", "ide-tab", `<span class="tt">sketch_oct16a.ino</span>`, tabs);
  const editor = el("div", "ide-editor", "", main);
  const code = el("div", "ide-code", "", editor);
  const bottom = el("div", "ide-bottom", "", main);
  const btabs = el("div", "ide-btabs", `<span class="on o1">Output</span><span class="o2" style="display:none">Serial Monitor &nbsp;✕</span>`, bottom);
  const out = el("div", "ide-out", "", bottom);
  const serial = el("div", "ide-out", "", bottom);
  serial.style.display = "none";
  const status = el("div", "ide-status", `<span class="lc">Ln 1, Col 1</span><span class="sb">✕ No board selected</span><span>🔔</span><span>▭</span>`, w);
  const toast = el("div", "ide-toast", `<div class="tx"></div><div class="bar"><i></i></div>`, w);
  return { w, title: $(".t", title), menu, fileMenuLabel: $(".m-file", menu), board, boardText: $(".bt", board), bVerify, bUpload,
    sIcons, panel, main, tab: $(".tt", tab), editor, code, bottom, btabs, out, serial, status, statusBoard: $(".sb", status),
    statusLC: $(".lc", status), toast, toastText: $(".tx", toast), toastBar: $(".bar i", toast) };
}

/** render code (first n chars) with line numbers and optional caret */
function renderCode(codeEl, src, n, caretOn, minLines = 1) {
  const lines = hlLines(src, n);
  const total = Math.max(lines.length, minLines);
  let html = "";
  for (let i = 0; i < total; i++) {
    const last = i === lines.length - 1;
    html += `<div><span class="ln${last ? " cur" : ""}">${i + 1}</span>${lines[i] || ""}${last && caretOn ? '<span class="caret"></span>' : ""}</div>`;
  }
  codeEl.innerHTML = html;
}

/** dyn helper: append log lines to an output element following a schedule [[t, text], ...] */
function logLines(target, schedule, maxLines = 9, active = [-1, 1e9]) {
  dyn((t) => {
    if (t < active[0] || t >= active[1]) return;
    const lines = [];
    for (const [ts, txt, replace] of schedule) {
      if (ts > t) break;
      if (replace) lines.pop();
      lines.push(typeof txt === "function" ? txt(t - ts) : txt);
    }
    target.innerHTML = lines.slice(-maxLines).map((l) => `<div>${l}</div>`).join("");
  });
}

function buildFileMenu(parent) {
  const items = [["New Sketch", "Ctrl+N"], ["New Cloud Sketch", "Alt+Ctrl+N"], ["Open...", "Ctrl+O"], ["Sketchbook", "›"], ["Examples", "›"],
    ["-"], ["Close", "Ctrl+W"], ["Save", "Ctrl+S"], ["Save As...", "Ctrl+Shift+S"], ["-"], ["Preferences...", "Ctrl+Comma"], ["Advanced", "›"], ["-"], ["Quit", "Ctrl+Q"]];
  const m = box(parent, 8, 54, 300, 10, "menu");
  m.style.height = "auto";
  const rows = {};
  items.forEach(([a, b]) => {
    if (a === "-") { el("hr", "", null, m); return; }
    rows[a] = el("div", "", `<span>${a}</span><span style="margin-left:auto;color:#aaa;font-size:12px">${b}</span>`, m);
  });
  return { m, rows };
}
