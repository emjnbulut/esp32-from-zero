// Episode 9 3D clips: event times from the narration schedule -> data files -> render (three.js, GPU).
//   node ep09/3d/make.mjs                 all four clips -> footage/ep09/C0.mp4 ... (what compose overlays)
//   node ep09/3d/make.mjs C2 --stills     review stills of one clip -> ep09/3d/build/stills
// A clip plays from its own 0 at (window start + 0.35 s), see heroClip() in engine/lib.js. Rerun after any
// schedule change (dub stretch, new narration): the lights follow the words.
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const video = path.resolve(here, "../..");
const root = path.resolve(video, "..");
const sched = JSON.parse(fs.readFileSync(path.join(video, "ep09/build/schedule.json"), "utf8"));
const seg = (id) => sched.segments[id];
const S0 = (id) => seg(id).start;
const words = (id) => (typeof seg(id).words === "string" ? JSON.parse(seg(id).words.replace(/'/g, '"')) : seg(id).words);
function W(id, w, nth = 1) {
  let k = 0;
  for (const x of words(id)) if (x.w.toLowerCase().replace(/[^a-z']/g, "") === w.toLowerCase() && ++k === nth) return S0(id) + x.t;
  throw new Error(`word ${w} not in ${id}`);
}
const LEAD = 0.35, r2 = (x) => Math.round(x * 100) / 100;

// windows must match ep09.js: hero(id, t0, t1) -> clip time 0 = t0 + 0.35, the window closes at t1
const CUT = S0("s03") - 0.1;
const CLIPS = {
  C0: (() => { const o = LEAD; return { dur: CUT - o + 0.3, press: W("s01", "press") - o, y0: W("s01", "yellow") - 0.35 - o }; })(),
  C3: (() => { const o = S0("s34") + LEAD; return { dur: S0("s35") - 0.35 - o + 0.3, press: W("s34", "round") - 0.1 - o, y0: W("s34", "green") - 0.1 - 2 - o }; })(),
  C2: (() => { const o = S0("s35") + LEAD; return { dur: S0("s36") - 0.35 - o + 0.3, blink: W("s35", "hurry") - o }; })(),
  C1: (() => {
    const o = S0("s44") + LEAD;
    const h = W("s44", "hold") - 0.05 - o;
    return { dur: S0("s45") - 0.35 - o + 0.3, tap: [0.32, 0.43], hold: [h, h + 1.03] };
  })(),
  // Short clips (video/shorts/ep09/short.json), centred for the square panel crop [420, 0, 1080, 1080]
  S0: { dur: 8, press: 1.5, y0: 6.6, short: true },
  S4: { dur: 7, short: true },
  TH: { dur: 1, short: true },
};
for (const c of Object.values(CLIPS)) for (const k of Object.keys(c)) c[k] = Array.isArray(c[k]) ? c[k].map(r2) : r2(c[k]);

const args = process.argv.slice(2);
const only = args.filter((a) => /^([CS]\d|TH)$/.test(a));
const stills = args.includes("--stills");
const build = path.join(here, "build");
fs.mkdirSync(build, { recursive: true });
fs.writeFileSync(path.join(build, "events.json"), JSON.stringify(CLIPS, null, 1));
console.log(CLIPS);

for (const id of only.length ? only : Object.keys(CLIPS).filter((k) => !CLIPS[k].short || args.includes("--shorts"))) {
  const ev = CLIPS[id];
  const data = { schedule: { duration: ev.dur, segments: {} }, clip: id, ev };
  const dataFile = path.join(build, `${id}.json`);
  fs.writeFileSync(dataFile, JSON.stringify(data));
  const common = ["engine/render.mjs", "ep09", "--page", "ep09/3d/index.html", "--data", dataFile, "--gpu"];
  let a;
  if (stills) {
    const ts = (args.find((x) => x.startsWith("--t=")) || "").slice(4) || [0.5, ev.dur * 0.25, ev.dur * 0.5, ev.dur * 0.75, ev.dur - 0.4].map((x) => x.toFixed(1)).join(",");
    a = [...common, "--stills", ts, "--out", path.join(build, id, "x.mp4")];
  } else {
    a = [...common, "--workers", "2", "--out", path.join(build, id, `${id}.mp4`)];
  }
  console.log(id, stills ? "stills" : "render");
  const r = spawnSync("node", a, { cwd: video, stdio: "inherit" });
  if (r.status !== 0) process.exit(r.status || 1);
  if (!stills) { // compose takes footage/ep09/<id>.mp4
    fs.mkdirSync(path.join(root, "footage/ep09"), { recursive: true });
    fs.copyFileSync(path.join(build, id, `${id}.mp4`), path.join(root, "footage/ep09", `${id}.mp4`));
  }
}
