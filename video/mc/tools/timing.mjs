#!/usr/bin/env node
/**
 * Motion Canvas timing for any episode (rerunnable):
 *
 *   node video/mc/tools/timing.mjs ep11        (ep10, ep11, ...)
 *
 * Reads video/<ep>/script.json + video/<ep>/build/schedule.json (EN narration,
 * word times) and writes video/mc/src/timing/<ep>.json:
 *
 *   { "<sceneId>": { "total": s, "estimated": bool,
 *                    "segments": [{ "id", "start", "dur", "words": [{w, t}] }] } }
 *
 * A scene = a run of consecutive segments whose vis is "mc:<sceneId>" (the id
 * from script.json, without the file prefix: scene file ep11_code_read.tsx
 * reads key "code_read"). Each segment lasts from its start to the next
 * segment's start, so the pause after it belongs to it - same rule as the
 * Blender shots. Start and word times are relative to the scene start.
 * Without schedule.json the times are estimated from the text (2.45 words/s,
 * same formula as the 3D scripts), so scenes can be drafted before the voice.
 *
 * It also copies the episode's real sketch (lessons/<NN>-*\/code/*\/*.ino) to
 * src/timing/<ep>_sketch.json for the full-code glimpses / code_full scenes.
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(HERE, '..', '..', '..');
const ep = process.argv[2];
if (!ep || !/^ep\d+$/.test(ep)) {
  console.error('usage: node video/mc/tools/timing.mjs <ep>   e.g. ep11');
  process.exit(2);
}

// segments that are Motion Canvas scenes even if script.json says otherwise
const FORCE_VIS = {
  ep10: {s39: 'mc:code_full'},
};

const EP = path.join(ROOT, 'video', ep);
const OUT_DIR = path.join(HERE, '..', 'src', 'timing');
const OUT = path.join(OUT_DIR, `${ep}.json`);

const script = JSON.parse(fs.readFileSync(path.join(EP, 'script.json'), 'utf8'));
const schedPath = path.join(EP, 'build', 'schedule.json');
const estimated = !fs.existsSync(schedPath);
const force = FORCE_VIS[ep] ?? {};

const segs = {};
if (!estimated) {
  const sch = JSON.parse(fs.readFileSync(schedPath, 'utf8')).segments;
  for (const d of script.segments) {
    const x = sch[d.id];
    if (!x) throw new Error(`schedule.json has no segment ${d.id}`);
    segs[d.id] = {start: x.start, end: x.end, words: x.words ?? [], vis: d.vis};
  }
} else {
  let t = 0.8;
  for (const d of script.segments) {
    const ws = d.text.split(/\s+/).filter(Boolean);
    const dur =
      ws.length / 2.45 +
      0.25 * (d.text.match(/,/g) ?? []).length +
      0.35 * (d.text.match(/[.!?]/g) ?? []).length;
    const words = ws.map((w, i) => ({w, t: +((dur * i) / ws.length).toFixed(3)}));
    segs[d.id] = {start: t, end: t + dur, words, vis: d.vis};
    t += dur + (d.pad ?? 0.35);
  }
}

const order = script.segments.map(d => d.id);
const scenes = {};
let prev = null;
order.forEach((sid, i) => {
  const v = force[sid] ?? segs[sid].vis;
  if (!v.startsWith('mc:')) {
    prev = null;
    return;
  }
  const name = v.slice(3);
  const next = i + 1 < order.length ? segs[order[i + 1]].start : segs[sid].end + 1.5;
  const seg = {id: sid, abs: segs[sid].start, dur: next - segs[sid].start, words: segs[sid].words};
  if (prev === name && scenes[name]) scenes[name].segments.push(seg);
  else {
    if (scenes[name]) throw new Error(`scene ${name} appears in two separate runs`);
    scenes[name] = {segments: [seg]};
  }
  prev = name;
});

const out = {};
for (const [name, sc] of Object.entries(scenes)) {
  const t0 = sc.segments[0].abs;
  const segments = sc.segments.map(s => ({
    id: s.id,
    start: +(s.abs - t0).toFixed(3),
    dur: +s.dur.toFixed(3),
    words: s.words.map(w => ({w: w.w, t: +(+w.t).toFixed(3)})),
  }));
  const total = +segments.reduce((a, s) => a + s.dur, 0).toFixed(3);
  out[name] = {total, estimated, segments};
}

fs.mkdirSync(OUT_DIR, {recursive: true});
fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n');

// the episode's real sketch (the main one, not the challenge solutions)
const SKETCH = {
  ep10: 'lessons/10-reflex-oled/code/reflex_oled/reflex_oled.ino',
  ep11: 'lessons/11-motion-alarm/code/motion_alarm/motion_alarm.ino',
  ep12: 'lessons/12-phone-control/code/phone_remote/phone_remote.ino',
};
function findSketch() {
  if (SKETCH[ep]) return SKETCH[ep];
  // guess: lessons/<NN>-<slug>/code/<slug_with_underscores>/<same>.ino
  const num = ep.slice(2).padStart(2, '0');
  const lessons = path.join(ROOT, 'lessons');
  if (!fs.existsSync(lessons)) return null;
  for (const l of fs.readdirSync(lessons).filter(d => d.startsWith(`${num}-`))) {
    const sub = l.slice(num.length + 1).replace(/-/g, '_');
    const rel = `lessons/${l}/code/${sub}/${sub}.ino`;
    if (fs.existsSync(path.join(ROOT, rel))) return rel;
  }
  return null;
}
const rel = findSketch();
let sketchMsg = 'no lesson sketch found (add it to SKETCH in timing.mjs)';
if (rel) {
  const lines = fs.readFileSync(path.join(ROOT, rel), 'utf8').split(/\r?\n/);
  while (lines.length && lines[lines.length - 1] === '') lines.pop();
  const parts = rel.split('/');
  fs.writeFileSync(
    path.join(OUT_DIR, `${ep}_sketch.json`),
    JSON.stringify({file: parts[parts.length - 1], folder: parts.slice(0, 2).join('/'), lines}, null, 1) + '\n',
  );
  sketchMsg = `sketch ${rel} (${lines.length} lines)`;
}

console.log(`${ep}: ${estimated ? 'ESTIMATED (no schedule.json yet)' : 'from schedule.json'} -> ${OUT}`);
console.log(`  ${sketchMsg}`);
for (const [k, v] of Object.entries(out)) {
  console.log(`  ${k.padEnd(16)} ${v.total.toFixed(2).padStart(6)} s  ${v.segments.map(s => `${s.id}@${s.start.toFixed(2)}`).join(' ')}`);
}
