// Secret knock lock Short: render picture (3D + overlay in one page), then mix.py adds the sound.
//   node short3d/knocklock/make.mjs en [--stills 1,5,9]     (run from video/)
// Needs build/<lang>_schedule.json + build/<lang>_voice.wav from voice.py.
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { makeStory } from "./story.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const video = path.resolve(here, "../..");
const lang = process.argv[2] || "en";
const sti = process.argv.indexOf("--stills");
const B = path.join(here, "build");
const sched = JSON.parse(fs.readFileSync(path.join(B, `${lang}_schedule.json`), "utf8"));
const S = makeStory(sched);
fs.writeFileSync(path.join(B, `${lang}_events.json`), JSON.stringify({ duration: S.DUR, ev: S.ev, presses: S.presses, mont: S.MONT }, null, 1));
const data = path.join(B, `${lang}_data.json`);
fs.writeFileSync(data, JSON.stringify({ schedule: { duration: sched.duration, segments: {} }, lang, sched }));
const out = path.join(B, lang, `knock_${lang}_picture.mp4`);
fs.mkdirSync(path.dirname(out), { recursive: true });
const args = ["engine/render.mjs", "short3d", "--page", "short3d/knocklock/index.html", "--data", data, "--size", "1080x1920", "--gpu", "--out", out];
if (sti > 0) args.push("--stills", process.argv[sti + 1]); else args.push("--workers", "2");
const r = spawnSync("node", args, { cwd: video, stdio: "inherit" });
process.exit(r.status || 0);
