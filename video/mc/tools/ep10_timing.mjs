#!/usr/bin/env node
/**
 * Ep10 Motion Canvas timing: node video/mc/tools/ep10_timing.mjs   (rerunnable)
 *
 * Reads video/ep10/script.json + video/ep10/build/schedule.json (EN narration,
 * word times) and writes video/mc/src/timing/ep10.json:
 *
 *   { "<sceneId>": { "total": s, "estimated": bool,
 *                    "segments": [{ "id", "start", "dur", "words": [{w, t}] }] } }
 *
 * Same convention as video/ep10/b3d/ep10_3d.py: a scene = a run of consecutive
 * segments whose vis is "mc:<sceneId>"; each segment lasts from its start to
 * the next segment's start (so the pause after it belongs to it). start and
 * word times are relative to the scene start. Without schedule.json the times
 * are estimated from the text (2.45 words/s, same formula as the 3D script).
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const EP = path.join(HERE, '..', '..', 'ep10');
const OUT = path.join(HERE, '..', 'src', 'timing', 'ep10.json');
const SKETCH = path.join(HERE, '..', '..', '..', 'lessons', '10-reflex-oled', 'code', 'reflex_oled', 'reflex_oled.ino');
const SKETCH_OUT = path.join(HERE, '..', 'src', 'timing', 'ep10_sketch.json');
// segments that are Motion Canvas scenes even if script.json still says otherwise
const FORCE_VIS = {s39: 'mc:code_full'};

const script = JSON.parse(fs.readFileSync(path.join(EP, 'script.json'), 'utf8'));
const schedPath = path.join(EP, 'build', 'schedule.json');
const estimated = !fs.existsSync(schedPath);

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
  const v = FORCE_VIS[sid] ?? segs[sid].vis;
  if (!v.startsWith('mc:')) {
    prev = null;
    return;
  }
  const name = v.slice(3);
  const next = i + 1 < order.length ? segs[order[i + 1]].start : segs[sid].end + 1.5;
  const dur = next - segs[sid].start;
  if (prev === name && scenes[name]) {
    const sc = scenes[name];
    sc.segments.push({id: sid, abs: segs[sid].start, dur, words: segs[sid].words});
  } else {
    if (scenes[name]) throw new Error(`scene ${name} appears in two separate runs`);
    scenes[name] = {segments: [{id: sid, abs: segs[sid].start, dur, words: segs[sid].words}]};
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

// the real sketch text, for the full-code glimpses (scenes import it as JSON)
const sketchLines = fs.readFileSync(SKETCH, 'utf8').split(/\r?\n/);
while (sketchLines.length && sketchLines[sketchLines.length - 1] === '') sketchLines.pop();
fs.mkdirSync(path.dirname(OUT), {recursive: true});
fs.writeFileSync(SKETCH_OUT, JSON.stringify({file: 'reflex_oled.ino', lines: sketchLines}, null, 1) + String.fromCharCode(10));
fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n');
console.log(`${estimated ? 'ESTIMATED (no schedule.json yet)' : 'from schedule.json'} -> ${OUT}`);
for (const [k, v] of Object.entries(out)) {
  console.log(`  ${k.padEnd(14)} ${v.total.toFixed(2).padStart(6)} s  ${v.segments.map(s => `${s.id}@${s.start.toFixed(2)}`).join(' ')}`);
}
