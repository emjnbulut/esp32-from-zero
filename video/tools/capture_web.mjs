import { chromium } from 'playwright';
import fs from 'fs';
const OUT = 'C:/Users/emin/esp32-from-zero/video/ep01/assets/web/';
fs.mkdirSync(OUT, { recursive: true });
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';
const pages = [
  ['arduino_software', 'https://www.arduino.cc/en/software'],
  ['silabs_cp210x', 'https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads'],
  ['wch_ch341', 'https://www.wch-ic.com/downloads/CH341SER_EXE.html'],
  ['espressif_install', 'https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html'],
];
const browser = await chromium.launch({ args: ['--disable-blink-features=AutomationControlled'] });
const ctx = await browser.newContext({ userAgent: UA, viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1, locale: 'en-US' });
const boxes = {};
async function dismiss(page) {
  for (let i = 0; i < 2; i++) {
    for (const t of ['Accept all cookies','Accept all','Accept All','Accept','Reject all','Reject','Got it','I agree','Allow all','OK','Close']) {
      try {
        const b = page.getByRole('button', { name: t, exact: true }).first();
        if (await b.isVisible({ timeout: 200 })) await b.click({ timeout: 1000 });
      } catch {}
    }
    await page.waitForTimeout(500);
  }
  await page.evaluate(() => {
    for (const el of document.querySelectorAll('body *')) {
      const s = getComputedStyle(el);
      const txt = (el.id + ' ' + el.className).toString().toLowerCase();
      if ((s.position === 'fixed' || s.position === 'sticky') && el.getBoundingClientRect().top > 100 - 1 ? /cookie|consent|onetrust|cmp|gdpr|popup|modal|banner/.test(txt) : /cookie|consent|onetrust|gdpr|truste|osano/.test(txt) && s.position === 'fixed') el.remove();
    }
    document.querySelectorAll('#onetrust-consent-sdk,#onetrust-banner-sdk,.onetrust-pc-dark-filter,#CybotCookiebotDialog').forEach(e => e.remove());
    document.body.style.overflow = 'auto';
  }).catch(() => {});
}
const bb = async (loc) => { try { const b = await loc.first().boundingBox({ timeout: 3000 }); if (!b) return null; const s = await loc.first().page().evaluate(() => ({ x: scrollX, y: scrollY })); return { x: Math.round(b.x + s.x), y: Math.round(b.y + s.y), width: Math.round(b.width), height: Math.round(b.height) }; } catch { return null; } };
for (const [name, url] of pages) {
  const page = await ctx.newPage();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
    await page.waitForTimeout(2000);
    await dismiss(page);
    await page.waitForTimeout(500);
    const info = { url };
    if (name === 'arduino_software') {
      const card = page.locator('xpath=//*[contains(text(),"Arduino IDE 2.3")]/ancestor::*[self::div or self::section][.//a[contains(.,"Windows")] or .//a[contains(.,"Download")]][1]');
      await card.first().scrollIntoViewIfNeeded({ timeout: 5000 }).catch(() => {});
      await page.waitForTimeout(500);
      await page.screenshot({ path: OUT + 'arduino_software_ide.png' });
      info.ide_card = await bb(card);
      info.ide_download_button = await bb(card.locator('a:has-text("Windows"), a:has-text("Download")'));
      await page.evaluate(() => scrollTo(0, 0));
    } else if (name === 'wch_ch341') {
      info.download_button = await bb(page.locator('a:has-text("Download"), button:has-text("Download"), a[href*="CH341SER.EXE"]'));
    } else if (name === 'espressif_install') {
      const t = page.locator('text=package_esp32_index.json');
      await t.first().scrollIntoViewIfNeeded().catch(() => {});
      info.index_json_text = await bb(t);
      await page.evaluate(() => scrollTo(0, 0));
    }
    await page.waitForTimeout(300);
    await page.screenshot({ path: OUT + name + '.png' });
    await page.screenshot({ path: OUT + name + '_full.png', fullPage: true });
    const d = await page.evaluate(() => ({ width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight }));
    info.full_size = d;
    boxes[name] = info;
  } catch (e) { boxes[name] = { url, error: String(e) }; }
  await page.close();
}
fs.writeFileSync(OUT + 'boxes.json', JSON.stringify(boxes, null, 2));
console.log(JSON.stringify(boxes, null, 2));
await browser.close();
