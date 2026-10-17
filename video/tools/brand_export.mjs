// Export the chosen channel art as PNGs for YouTube.
// Usage: node video/tools/brand_export.mjs   (writes brand/export/)
import { chromium } from "playwright";
import { fileURLToPath, pathToFileURL } from "url";
import path from "path";

const dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../brand");
const out = path.join(dir, "export");
const LOGO = "A", BANNER = 1;

const browser = await chromium.launch();
const src = await browser.newPage();
await src.goto(pathToFileURL(path.join(dir, "concepts.html")).href);
const { logo, banner } = await src.evaluate(([l, b]) => ({
  logo: LOGOS[l](),
  banner: banner(b, l).match(/<svg[\s\S]*<\/svg>/)[0],
}), [LOGO, BANNER]);

async function shot(svg, w, h, file) {
  const p = await browser.newPage({ viewport: { width: w, height: h } });
  await p.setContent(`<html><body style="margin:0;background:#0b1220">
    <div style="width:${w}px;height:${h}px">${svg.replace("<svg ", `<svg width="${w}" height="${h}" `)}</div></body></html>`);
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(out, file) });
  console.log(file, `${w}x${h}`);
}
await shot(logo, 800, 800, "profile_800.png");     // profile picture (YouTube crops it to a circle)
await shot(logo, 150, 150, "watermark_150.png");   // optional video watermark
await shot(banner, 2560, 1440, "banner_2560x1440.png");
await browser.close();
