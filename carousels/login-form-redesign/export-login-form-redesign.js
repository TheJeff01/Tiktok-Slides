const { chromium } = require('/Users/mac/.npm-global/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const SLIDE_COUNT = 4;
const SLIDE_W = 420;
const SLIDE_H = 525;
const OUTPUT_DIR = path.join(__dirname, 'slides');

(async () => {
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const context = await browser.newContext({
    viewport: { width: 480, height: 600 },
    deviceScaleFactor: 3,
  });
  const page = await context.newPage();

  const filePath = 'file://' + path.join(__dirname, 'login-form-redesign.html');
  await page.goto(filePath, { waitUntil: 'load' });

  await page.addStyleTag({
    content: `.carousel-viewport{width:${SLIDE_W}px !important;height:${SLIDE_H}px !important;aspect-ratio:auto !important;}`,
  });

  await page.waitForTimeout(2000);
  await page.evaluate(() => document.fonts.ready);

  const viewport = await page.$('.carousel-viewport');

  for (let i = 0; i < SLIDE_COUNT; i++) {
    await page.evaluate((idx) => {
      const track = document.getElementById('track');
      const SLIDE_W = 420;
      track.style.transition = 'none';
      track.style.transform = `translateX(${-idx * SLIDE_W}px)`;
    }, i);

    await page.waitForTimeout(100);

    const slideNum = String(i + 1).padStart(2, '0');
    const outPath = path.join(OUTPUT_DIR, `slide_${slideNum}.png`);
    await viewport.screenshot({ path: outPath });

    console.log(`Exported slide ${i + 1}/${SLIDE_COUNT}: ${outPath}`);
  }

  await browser.close();
  console.log(`\nDone! ${SLIDE_COUNT} slides saved to: ${OUTPUT_DIR}`);
})();
