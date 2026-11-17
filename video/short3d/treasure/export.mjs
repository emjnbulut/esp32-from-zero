// Treasure Short: export the 3D circuit (GLB + pivots/anchors/wires) and a preview PNG.
//   node video/short3d/treasure/export.mjs   -> build/scene.glb, build/scene_info.json, build/preview.png
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, "build");
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ args: ["--allow-file-access-from-files", "--enable-gpu", "--ignore-gpu-blocklist", "--use-angle=d3d11"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
page.on("pageerror", (e) => console.error("[page]", e.message));
page.on("console", (m) => { if (m.type() === "error") console.error("[console]", m.text()); });
await page.goto(pathToFileURL(path.join(here, "scene.html")).href);
await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
const views = JSON.parse(process.argv[2] || "[]");
await page.screenshot({ path: path.join(out, "preview.png") });
for (const [i, v] of views.entries()) {
  await page.evaluate((a) => window.__preview(...a), v);
  await page.screenshot({ path: path.join(out, `preview${i + 1}.png`) });
}
const r = await page.evaluate(() => window.__export());
fs.writeFileSync(path.join(out, "scene.glb"), Buffer.from(r.glb, "base64"));
fs.writeFileSync(path.join(out, "scene_info.json"), JSON.stringify(r.info));
console.log("scene.glb", fs.statSync(path.join(out, "scene.glb")).size);
await browser.close();
