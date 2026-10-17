// Render YouTube thumbnails (1280x720 PNG) from video/thumbs/thumbs.js.
// Usage: node video/tools/thumbs.mjs [ep03_A ...]   (default: all) -> video/thumbs/build/<key>.png
import { chromium } from "playwright";
import { fileURLToPath, pathToFileURL } from "url";
import fs from "fs";
import path from "path";

const dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../thumbs");
const out = path.join(dir, "build");
fs.mkdirSync(out, { recursive: true });
const page0 = pathToFileURL(path.join(dir, "thumbs.html")).href;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
page.on("pageerror", (e) => console.error("[page]", e.message));
await page.goto(page0 + "?ep01_A");
await page.waitForFunction(() => window.__ready === true);
const keys = process.argv.length > 2 ? process.argv.slice(2) : await page.evaluate(() => window.__keys);
for (const k of keys) {
  await page.goto(page0 + "?" + k);
  await page.waitForFunction(() => window.__ready === true);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(out, k + ".png") });
  console.log(k);
}
await browser.close();
