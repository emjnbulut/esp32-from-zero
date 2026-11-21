#!/usr/bin/env node
/**
 * Headless Motion Canvas render.
 *
 *   node video/mc/render.mjs prefsRecord                 (from repo root, 30 fps)
 *   node video/mc/render.mjs prefsRecord --fps 60
 *   node video/mc/render.mjs prefsRecord --frames        (+4 check PNGs)
 *   node video/mc/render.mjs prefsRecord --to 3          (first 3 s only)
 *   node video/mc/render.mjs prefsRecord --exporter ffmpeg
 *
 * 1. starts the Vite dev server on :9000 (or reuses one that is already up)
 * 2. opens /render.html?scene=<name> in headless Chromium (Playwright from
 *    video/node_modules); that page drives Motion Canvas' own Renderer - no
 *    editor clicking involved
 * 3. exporter "images" (default): Motion Canvas' image-sequence exporter
 *    writes JPEG q98 frames (--png for PNG); browser PNG encoding of a busy
 *    1080p frame costs ~190 ms, JPEG ~20 ms. The system ffmpeg then encodes
 *    them with x264 CRF 16. exporter "ffmpeg": @motion-canvas/ffmpeg writes the mp4
 *    itself (bundled ffmpeg, CRF 23 default, smaller/softer).
 * 4. checks the mp4 with ffprobe, then stops the server.
 *
 * Output: video/mc/output/<scene>.mp4
 */
import {spawn, spawnSync} from 'node:child_process';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PORT = 9000;
const BASE = `http://localhost:${PORT}`;

const VALUE_FLAGS = new Set(['fps', 'to', 'exporter', 'crf']);
const opts = {};
const positional = [];
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) {
    const k = a.slice(2);
    opts[k] = VALUE_FLAGS.has(k) ? process.argv[++i] : true;
  } else positional.push(a);
}
const scene = positional[0];
// 30 fps matches the rest of the course pipeline (video/engine); --fps 60 works too
const fps = Number(opts.fps ?? 30);
const wantFrames = !!opts.frames;
const to = opts.to; // optional: stop after N seconds (quick tests)
const exporter = opts.exporter ?? 'images';
const crf = String(opts.crf ?? 16);
const ext = opts.png ? 'png' : 'jpeg'; // image-sequence frame format
const launchArgs = (process.env.MC_CHROME_ARGS ?? '').split(' ').filter(Boolean);
if (!scene || !['images', 'ffmpeg'].includes(exporter)) {
  console.error(
    'usage: node video/mc/render.mjs <sceneName> [--fps 30] [--to <sec>] [--frames]\n' +
      '                                [--exporter images|ffmpeg] [--crf 16] [--png]',
  );
  process.exit(2);
}

const require = createRequire(path.join(HERE, '..', 'package.json'));
const {chromium} = require('playwright');

const outFile = path.join(HERE, 'output', `${scene}.mp4`);
const seqDir = path.join(HERE, 'output', scene); // image-sequence exporter target
const t0 = Date.now();
const log = (...m) => console.log(`[${((Date.now() - t0) / 1000).toFixed(1)}s]`, ...m);

async function isUp() {
  try {
    const r = await fetch(`${BASE}/render.html`);
    return r.ok;
  } catch {
    return false;
  }
}

async function startServer() {
  if (await isUp()) {
    log(`reusing dev server already running on :${PORT}`);
    return null;
  }
  const viteBin = path.join(HERE, 'node_modules', 'vite', 'bin', 'vite.js');
  // same as `npx vite --port 9000 --strictPort`, but without a shell so the
  // process can be stopped cleanly on Windows
  const child = spawn(process.execPath, [viteBin, '--port', String(PORT), '--strictPort'], {
    cwd: HERE,
    stdio: ['ignore', 'pipe', 'pipe'],
    env: {...process.env, BROWSER: 'none'},
  });
  let output = '';
  child.stdout.on('data', d => (output += d));
  child.stderr.on('data', d => (output += d));
  child.on('exit', code => {
    if (code) console.error(`vite exited with ${code}\n${output}`);
  });
  for (let i = 0; i < 120; i++) {
    if (child.exitCode !== null) throw new Error(`vite failed to start:\n${output}`);
    if (await isUp()) {
      log('vite dev server up');
      return child;
    }
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error(`vite did not come up in 60 s:\n${output}`);
}

function stopServer(child) {
  if (!child || child.exitCode !== null) return;
  if (process.platform === 'win32') {
    spawnSync('taskkill', ['/pid', String(child.pid), '/T', '/F'], {stdio: 'ignore'});
  } else {
    child.kill('SIGTERM');
  }
}

function probeDuration(file) {
  const r = spawnSync(
    'ffprobe',
    ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file],
    {encoding: 'utf8'},
  );
  const d = parseFloat(r.stdout);
  return Number.isFinite(d) ? d : null;
}

function dumpFrames(file, duration) {
  const dir = path.join(HERE, 'output', `${scene}_frames`);
  fs.mkdirSync(dir, {recursive: true});
  for (const f of fs.readdirSync(dir)) fs.unlinkSync(path.join(dir, f));
  const times = [0.18, 0.4, 0.62, 0.84].map(p => +(p * duration).toFixed(2));
  times.forEach((t, i) => {
    spawnSync('ffmpeg', ['-y', '-v', 'error', '-ss', String(t), '-i', file, '-frames:v', '1',
      path.join(dir, `${i + 1}_${t.toFixed(2)}s.png`)]);
  });
  log(`frames -> ${dir}`);
}

let server = null;
let browser = null;
let code = 0;
try {
  fs.rmSync(outFile, {force: true});
  fs.rmSync(seqDir, {recursive: true, force: true});
  server = await startServer();

  browser = await chromium.launch({headless: true, args: launchArgs});
  const page = await browser.newPage({viewport: {width: 800, height: 450}});
  page.on('pageerror', e => console.error('[page error]', e.message));
  page.on('console', m => {
    if (m.type() === 'error') console.error('[console]', m.text());
  });
  const query =
    `scene=${encodeURIComponent(scene)}&fps=${fps}&exporter=${exporter}` + (to ? `&to=${to}` : '') + (opts.png ? '&format=png' : '');
  await page.goto(`${BASE}/render.html?${query}`, {
    waitUntil: 'load',
    timeout: 120_000,
  });

  let last = -1;
  let lastChange = Date.now();
  for (;;) {
    const s = await page.evaluate(() => window.__mc ?? null);
    if (s?.state === 'done') break;
    if (s?.state === 'failed') throw new Error(`render failed:\n${s.error}\n${s.logs.join('\n')}`);
    if (s && s.frame !== last) {
      if (s.frame % 60 === 0 || last < 0) log(`frame ${s.frame}`);
      last = s.frame;
      lastChange = Date.now();
    }
    if (Date.now() - lastChange > 120_000) throw new Error(`render stalled at frame ${last}`);
    await new Promise(r => setTimeout(r, 250));
  }

  if (exporter === 'images') {
    const imgs = fs.readdirSync(seqDir).filter(f => f.endsWith(`.${ext}`));
    log(`${imgs.length} frames written, encoding with ffmpeg (crf ${crf})`);
    const enc = spawnSync(
      'ffmpeg',
      ['-y', '-v', 'error', '-framerate', String(fps), '-i', path.join(seqDir, `%06d.${ext}`),
        '-c:v', 'libx264', '-preset', 'medium', '-crf', crf, '-pix_fmt', 'yuv420p',
        '-r', String(fps), '-movflags', '+faststart', outFile],
      {encoding: 'utf8'},
    );
    if (enc.status !== 0) throw new Error(`ffmpeg encode failed:\n${enc.stderr}`);
    fs.rmSync(seqDir, {recursive: true, force: true});
  }

  // the ffmpeg exporter only acks "end" after ffmpeg exits; double-check anyway
  let duration = null;
  for (let i = 0; i < 40 && duration === null; i++) {
    if (fs.existsSync(outFile)) duration = probeDuration(outFile);
    if (duration === null) await new Promise(r => setTimeout(r, 250));
  }
  if (duration === null) throw new Error(`no readable mp4 at ${outFile}`);
  const mb = (fs.statSync(outFile).size / 1e6).toFixed(1);
  log(`done: ${outFile} (${duration.toFixed(2)} s, ${mb} MB, ${last + 1} frames @ ${fps} fps)`);
  if (wantFrames) dumpFrames(outFile, duration);
} catch (e) {
  console.error(e?.message ?? e);
  code = 1;
} finally {
  await browser?.close().catch(() => {});
  stopServer(server);
}
log(`total ${((Date.now() - t0) / 1000).toFixed(1)} s`);
process.exit(code);
