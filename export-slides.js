const { chromium } = require('/Users/mac/.npm-global/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const SLIDE_COUNT = 9;
const SLIDE_W = 420;
const SLIDE_H = 525;
const OUTPUT_DIR = path.join(__dirname, 'frontend-vs-backend-slides');

(async () => {
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const page = await browser.newPage();

  const filePath = 'file://' + path.join(__dirname, 'frontend-vs-backend.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });

  // Wait for fonts to load
  await page.waitForTimeout(1500);

  for (let i = 0; i < SLIDE_COUNT; i++) {
    // Navigate to slide i
    await page.evaluate((idx) => {
      const track = document.getElementById('track');
      const SLIDE_W = 420;
      track.style.transition = 'none';
      track.style.transform = `translateX(${-idx * SLIDE_W}px)`;
    }, i);

    await page.waitForTimeout(100);

    // Get the viewport element position
    const viewport = await page.$('.carousel-viewport');
    const box = await viewport.boundingBox();

    // Screenshot just the carousel viewport
    const slideNum = String(i + 1).padStart(2, '0');
    const outPath = path.join(OUTPUT_DIR, `slide_${slideNum}.png`);

    await page.screenshot({
      path: outPath,
      clip: {
        x: box.x,
        y: box.y,
        width: box.width,
        height: box.height,
      },
    });

    console.log(`Exported slide ${i + 1}/${SLIDE_COUNT}: ${outPath}`);
  }

  await browser.close();
  console.log(`\nDone! ${SLIDE_COUNT} slides saved to: ${OUTPUT_DIR}`);
})();
