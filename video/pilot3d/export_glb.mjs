// Exports the pilot scene at time t as a GLB (+ camera/LED info) for the Blender hero render.
//   node pilot3d/export_glb.mjs 18.5   -> pilot3d/build/scene.glb, pilot3d/build/scene.json
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
const t = Number(process.argv[2] || 18.5);
const browser = await chromium.launch({ args: ["--allow-file-access-from-files", "--enable-gpu", "--ignore-gpu-blocklist", "--use-angle=d3d11"] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on("pageerror", (e) => console.error("[page]", e.message));
await page.addInitScript(() => { window.__DATA = { schedule: { duration: 20, segments: {} } }; });
await page.goto(pathToFileURL(path.join(here, "index.html")).href);
await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
const r = await page.evaluate((x) => window.__exportGLB(x), t);
fs.mkdirSync(path.join(here, "build"), { recursive: true });
fs.writeFileSync(path.join(here, "build", "scene.glb"), Buffer.from(r.glb, "base64"));
fs.writeFileSync(path.join(here, "build", "scene.json"), JSON.stringify({ t, cam: r.cam, led: r.led, groups: r.groups, wires: r.wires, anchors: r.anchors }));
console.log("scene.glb", fs.statSync(path.join(here, "build", "scene.glb")).size, "bytes");
await browser.close();
