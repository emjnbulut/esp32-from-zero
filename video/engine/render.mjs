// Frame-accurate renderer: seeks the episode page to each frame time and pipes
// screenshots into ffmpeg.
//   node engine/render.mjs ep01                      full video -> ep01/build/video.mp4
//   node engine/render.mjs ep01 --from 60 --to 90    partial render (preview)
//   node engine/render.mjs ep01 --stills 5,30.5,61   PNG stills -> ep01/build/stills/
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const ep = path.resolve(here, "..", args[0]);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i >= 0 ? args[i + 1] : d; };
const fps = Number(opt("fps", 30));
const workers = Number(opt("workers", 4));
const build = path.join(ep, "build");

const data = {
  schedule: JSON.parse(fs.readFileSync(path.join(build, "schedule.json"), "utf8")),
  script: JSON.parse(fs.readFileSync(path.join(ep, "script.json"), "utf8")),
};

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("[page]", e.message));
  page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") console.error("[console]", m.text()); });
  await page.addInitScript((d) => { window.__DATA = d; }, data);
  await page.goto(pathToFileURL(path.join(ep, "index.html")).href);
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  return page;
}

function ffmpegWriter(out) {
  const p = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-framerate", String(fps), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", String(fps), out], { stdio: ["pipe", "inherit", "inherit"] });
  const done = new Promise((res, rej) => p.on("close", (c) => (c === 0 ? res() : rej(new Error("ffmpeg " + c)))));
  return { p, done };
}
const write = (stream, buf) => new Promise((res) => (stream.write(buf) ? res() : stream.once("drain", res)));

const browser = await chromium.launch({ args: ["--font-render-hinting=none", "--disable-gpu-vsync"] });
const stills = opt("stills");
if (stills) {
  const page = await openPage(browser);
  fs.mkdirSync(path.join(build, "stills"), { recursive: true });
  for (const t of stills.split(",").map(Number)) {
    await page.evaluate((t) => window.__seek(t), t);
    await page.screenshot({ path: path.join(build, "stills", `t${t.toFixed(1)}.png`) });
    console.log("still", t);
  }
  await browser.close();
  process.exit(0);
}

const duration = data.schedule.duration;
const from = Number(opt("from", 0)), to = Math.min(Number(opt("to", duration)), duration);
const f0 = Math.round(from * fps), f1 = Math.round(to * fps);
const per = Math.ceil((f1 - f0) / workers);
const t0 = Date.now();
let doneFrames = 0;

const parts = [];
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  const a = f0 + w * per, b = Math.min(f1, a + per);
  if (a >= b) return;
  const page = await openPage(browser);
  const out = path.join(build, `part${w}.mp4`);
  parts[w] = out;
  const { p, done } = ffmpegWriter(out);
  for (let f = a; f < b; f++) {
    await page.evaluate((t) => window.__seek(t), f / fps);
    const buf = await page.screenshot({ type: "jpeg", quality: 92 });
    await write(p.stdin, buf);
    if (++doneFrames % 300 === 0) {
      const el = (Date.now() - t0) / 1000;
      console.log(`${doneFrames}/${f1 - f0} frames, ${el.toFixed(0)}s, eta ${((f1 - f0 - doneFrames) * el / doneFrames).toFixed(0)}s`);
    }
  }
  p.stdin.end();
  await done;
  if (w === 0) fs.writeFileSync(path.join(build, "clips.json"), JSON.stringify(await page.evaluate(() => window.__clips), null, 1));
}));
await browser.close();

const list = path.join(build, "parts.txt");
fs.writeFileSync(list, parts.filter(Boolean).map((p) => `file '${p.replace(/\\/g, "/")}'`).join("\n"));
const outName = from === 0 && to === duration ? "video.mp4" : `preview_${from}-${to}.mp4`;
await new Promise((res, rej) => spawn("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-c", "copy", path.join(build, outName)], { stdio: "inherit" })
  .on("close", (c) => (c === 0 ? res() : rej(new Error("concat " + c)))));
for (const p of parts.filter(Boolean)) fs.unlinkSync(p);
console.log(`rendered ${outName} in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
