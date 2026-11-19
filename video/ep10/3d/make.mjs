// Episode 10 3D clips: event times from the narration schedule -> data files -> render (three.js, GPU).
//   node ep10/3d/make.mjs                 all four clips -> footage/ep10/C0.mp4 ... (what compose overlays)
//   node ep10/3d/make.mjs C2 --stills     review stills of one clip -> ep10/3d/build/stills
// A clip plays from its own 0 at (window start + 0.35 s), see heroClip() in engine/lib.js. Rerun after any
// schedule change (dub stretch, new narration): the lights follow the words.
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const video = path.resolve(here, "../..");
const root = path.resolve(video, "..");
const sched = JSON.parse(fs.readFileSync(path.join(video, "ep10/build/schedule.json"), "utf8"));
const seg = (id) => sched.segments[id];
const S0 = (id) => seg(id).start;
const words = (id) => (typeof seg(id).words === "string" ? JSON.parse(seg(id).words.replace(/'/g, '"')) : seg(id).words);
function W(id, w, nth = 1) {
  let k = 0;
  for (const x of words(id)) if (x.w.toLowerCase().replace(/[^a-z']/g, "") === w.toLowerCase() && ++k === nth) return S0(id) + x.t;
  throw new Error(`word ${w} not in ${id}`);
}
const LEAD = 0.35, r2 = (x) => Math.round(x * 100) / 100;

// windows must match ep10.js: hero(id, t0, t1) -> clip time 0 = t0 + 0.35, the window closes at t1
const CUT = S0("s03") - 0.1;
const r213 = 0.213, r1046 = 1.046;
const round = (press, react, wait = 1) => ({ start: press - react - wait - 1, wait, press });
const CLIPS = {
  C0: (() => {
    const o = LEAD, press = 4.11 - o;
    return { dur: CUT - o + 0.3, rounds: [round(press, r213, 2.15)], record: W("s02", "best") - 0.2 - o };
  })(),
  C4: (() => { const o = S0("s27") + LEAD; return { dur: S0("s28") - 0.35 - o + 0.3, rounds: [round(S0("s27") + 2.5 - o, r213)] }; })(),
  C1: (() => { const o = S0("s28") + LEAD; return { dur: S0("s29") - 0.35 - o + 0.3, rounds: [round(S0("s28") + 2.5 - o, r1046)] }; })(),
  C2: (() => { const o = S0("s41") + LEAD; return { dur: S0("s42") - 0.35 - o + 0.3, unplug: W("s41", "unplug") - 0.1 - o, plug: W("s41", "plug") - o }; })(),
  // Short clips, centred for the square panel crop [420, 0, 1080, 1080]
  S0: { dur: 7, rounds: [round(3.69, 0.19)], short: true },
  S2: { dur: 6, unplug: 1.2, plug: 3.6, short: true },
  S4: { dur: 8, short: true },
  S5: { dur: 11, rounds: [{ start: 0.6, wait: 2, falseAt: 2.6 }, round(7.0, 0.205)], short: true },
};
const rr = (x) => (typeof x === "number" ? Math.round(x * 1000) / 1000 : x);
for (const c of Object.values(CLIPS)) {
  for (const k of Object.keys(c)) c[k] = Array.isArray(c[k]) ? c[k].map((r) => (typeof r === "object" ? Object.fromEntries(Object.entries(r).map(([a, b]) => [a, rr(b)])) : rr(r))) : rr(c[k]);
}

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
  const common = ["engine/render.mjs", "ep10", "--page", "ep10/3d/index.html", "--data", dataFile, "--gpu"];
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
  if (!stills) { // compose takes footage/ep10/<id>.mp4
    fs.mkdirSync(path.join(root, "footage/ep10"), { recursive: true });
    fs.copyFileSync(path.join(build, id, `${id}.mp4`), path.join(root, "footage/ep10", `${id}.mp4`));
  }
}
