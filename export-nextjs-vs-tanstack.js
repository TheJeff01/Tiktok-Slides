const { chromium } = require('/Users/mac/.npm-global/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const SLIDE_COUNT = 9;
const SLIDE_W = 420;
const SLIDE_H = 525;
const OUTPUT_DIR = path.join(__dirname, 'nextjs-vs-tanstack-slides');

(async () => {
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  // 3x scale → crisp ~1260x1575 PNGs (Instagram portrait is 1080x1350)
  const context = await browser.newContext({
    viewport: { width: 480, height: 600 },
    deviceScaleFactor: 3,
  });
  const page = await context.newPage();

  const filePath = 'file://' + path.join(__dirname, 'nextjs-vs-tanstack.html');
  await page.goto(filePath, { waitUntil: 'load' });

  // Pin the viewport to exact dimensions (aspect-ratio was rounding ~26px short)
  await page.addStyleTag({
    content: `.carousel-viewport{width:${SLIDE_W}px !important;height:${SLIDE_H}px !important;aspect-ratio:auto !important;}`,
  });

  // Wait for fonts to load
  await page.waitForTimeout(2000);
  await page.evaluate(() => document.fonts.ready);

  // Geometry sanity check: 9 track children at lefts 0,420,...,3360
  const geo = await page.evaluate(() => {
    const track = document.getElementById('track');
    const kids = Array.from(track.children);
    return { count: kids.length, lefts: kids.map((k) => k.offsetLeft) };
  });
  console.log('track children:', geo.count, 'lefts:', geo.lefts.join(','));
  if (geo.count !== SLIDE_COUNT) {
    console.error('GEOMETRY CHECK FAILED — expected 9 slides');
    await browser.close();
    process.exit(1);
  }

  const viewport = await page.$('.carousel-viewport');

  for (let i = 0; i < SLIDE_COUNT; i++) {
    // Navigate to slide i
    await page.evaluate((idx) => {
      const track = document.getElementById('track');
      const SLIDE_W = 420;
      track.style.transition = 'none';
      track.style.transform = `translateX(${-idx * SLIDE_W}px)`;
    }, i);

    await page.waitForTimeout(100);

    // Screenshot the element directly → exact 420x525 box, scaled 3x by deviceScaleFactor
    const slideNum = String(i + 1).padStart(2, '0');
    const outPath = path.join(OUTPUT_DIR, `slide_${slideNum}.png`);
    await viewport.screenshot({ path: outPath });

    console.log(`Exported slide ${i + 1}/${SLIDE_COUNT}: ${outPath}`);
  }

  await browser.close();
  console.log(`\nDone! ${SLIDE_COUNT} slides saved to: ${OUTPUT_DIR}`);
})();
