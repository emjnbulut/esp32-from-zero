// Treasure Short: evaluate story.mjs for every frame -> build/track.json (read by blender_short.py).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { makeStory, FPS } from "./story.mjs";
const here = path.dirname(fileURLToPath(import.meta.url));
const sched = JSON.parse(fs.readFileSync(path.join(here, "build", "schedule.json"), "utf8"));
const info = JSON.parse(fs.readFileSync(path.join(here, "build", "scene_info.json"), "utf8"));
const st = makeStory(sched, info);
const N = Math.ceil(st.DUR * FPS);
const frames = [];
for (let f = 0; f < N; f++) {
  const s = st.state(f / FPS);
  frames.push({ knobDeg: +s.knobDeg.toFixed(2), rgb: s.rgb, rled: s.rled, cap: +s.cap.toFixed(3), party: s.party,
    coin: s.coin && { y: +s.coin.y.toFixed(2), spin: +s.coin.spin.toFixed(1), scale: +s.coin.scale.toFixed(3) },
    rings: +s.rings.toFixed(3), dim: +s.dim.toFixed(3), cam: { pos: s.cam.pos.map((v) => +v.toFixed(2)), tgt: s.cam.tgt.map((v) => +v.toFixed(2)), fov: +s.cam.fov.toFixed(2) } });
}
fs.writeFileSync(path.join(here, "build", "track.json"), JSON.stringify({ fps: FPS, frames: N, duration: st.DUR, T: st.state(0).T, windows: { beep: [[st.L.l02.t0 - 0.2, st.L.l09.t0 - 0.3], [st.L.l13.t0, st.DUR]] }, heat: Array.from({ length: N }, (_, f) => st.state(f / FPS).heat), info, track: frames }));
console.log("track", N, "frames, press at", st.state(0).T.press.toFixed(2), "s, shots", st.SHOTS.map((s) => s[0].toFixed(1)).join(" "));
