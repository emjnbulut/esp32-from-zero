// Frame-accurate renderer: seeks a page to each frame time and pipes screenshots
// into ffmpeg.
//   node engine/render.mjs ep01                      full episode -> ep01/build/video.mp4
//   node engine/render.mjs ep01 --from 60 --to 90    partial render (preview)
//   node engine/render.mjs ep01 --stills 5,30.5,61   PNG stills -> ep01/build/stills/
// Generic pages (e.g. Shorts overlays):
//   --page <html> --data <json> --size 1080x1920 --alpha --out <file.mov>
//   --data JSON is injected as window.__DATA; it must contain schedule.duration.
//   --alpha renders with a transparent background into a QuickTime (qtrle) file.
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i >= 0 ? args[i + 1] : d; };
const flag = (k) => args.includes("--" + k);
const ep = path.resolve(here, "..", args[0]);
const fps = Number(opt("fps", 30));
const workers = Number(opt("workers", 4));
const [W, H] = opt("size", "1920x1080").split("x").map(Number);
const alpha = flag("alpha");
const pageFile = path.resolve(opt("page", path.join(ep, "index.html")));
const build = opt("out") ? path.dirname(path.resolve(opt("out"))) : path.join(ep, "build");

const data = opt("data")
  ? JSON.parse(fs.readFileSync(opt("data"), "utf8"))
  : {
      schedule: JSON.parse(fs.readFileSync(path.join(build, "schedule.json"), "utf8")),
      script: JSON.parse(fs.readFileSync(path.join(ep, "script.json"), "utf8")),
    };

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("[page]", e.message));
  page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") console.error("[console]", m.text()); });
  await page.addInitScript((d) => { window.__DATA = d; }, data);
  await page.goto(pathToFileURL(pageFile).href);
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  return page;
}

function ffmpegWriter(out) {
  const input = alpha ? ["-c:v", "png"] : ["-c:v", "mjpeg"];
  const enc = alpha ? ["-c:v", "qtrle", "-pix_fmt", "argb"] : ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p"];
  const p = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-framerate", String(fps), ...input, "-i", "-",
    ...enc, "-r", String(fps), out], { stdio: ["pipe", "inherit", "inherit"] });
  const done = new Promise((res, rej) => p.on("close", (c) => (c === 0 ? res() : rej(new Error("ffmpeg " + c)))));
  return { p, done };
}
const write = (stream, buf) => new Promise((res) => (stream.write(buf) ? res() : stream.once("drain", res)));
const shot = (page) => alpha ? page.screenshot({ type: "png", omitBackground: true }) : page.screenshot({ type: "jpeg", quality: 92 });

const browser = await chromium.launch({ args: ["--font-render-hinting=none", "--disable-gpu-vsync"] });
const stills = opt("stills");
if (stills) {
  const page = await openPage(browser);
  const dir = path.join(build, "stills");
  fs.mkdirSync(dir, { recursive: true });
  for (const t of stills.split(",").map(Number)) {
    await page.evaluate((t) => window.__seek(t), t);
    await page.screenshot({ path: path.join(dir, `t${t.toFixed(1)}.png`), omitBackground: alpha });
    console.log("still", t);
  }
  await browser.close();
  process.exit(0);
}

const duration = data.schedule.duration;
const from = Number(opt("from", 0)), to = Math.min(Number(opt("to", duration)), duration);
const f0 = Math.round(from * fps), f1 = Math.round(to * fps);
const per = Math.ceil((f1 - f0) / workers);
const ext = alpha ? ".mov" : ".mp4";
const t0 = Date.now();
let doneFrames = 0;

const parts = [];
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  const a = f0 + w * per, b = Math.min(f1, a + per);
  if (a >= b) return;
  const page = await openPage(browser);
  const out = path.join(build, `part${w}${ext}`);
  parts[w] = out;
  const { p, done } = ffmpegWriter(out);
  for (let f = a; f < b; f++) {
    await page.evaluate((t) => window.__seek(t), f / fps);
    await write(p.stdin, await shot(page));
    if (++doneFrames % 300 === 0) {
      const el = (Date.now() - t0) / 1000;
      console.log(`${doneFrames}/${f1 - f0} frames, ${el.toFixed(0)}s, eta ${((f1 - f0 - doneFrames) * el / doneFrames).toFixed(0)}s`);
    }
  }
  p.stdin.end();
  await done;
  if (w === 0) fs.writeFileSync(path.join(build, "clips.json"), JSON.stringify(await page.evaluate(() => window.__clips || []), null, 1));
}));
await browser.close();

const list = path.join(build, "parts.txt");
fs.writeFileSync(list, parts.filter(Boolean).map((p) => `file '${p.replace(/\\/g, "/")}'`).join("\n"));
const outFile = opt("out") ? path.resolve(opt("out"))
  : path.join(build, from === 0 && to === duration ? "video.mp4" : `preview_${from}-${to}.mp4`);
await new Promise((res, rej) => spawn("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-c", "copy", outFile], { stdio: "inherit" })
  .on("close", (c) => (c === 0 ? res() : rej(new Error("concat " + c)))));
for (const p of parts.filter(Boolean)) fs.unlinkSync(p);
console.log(`rendered ${path.basename(outFile)} in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
