const { chromium } = require('/Users/mac/.npm-global/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const page = await browser.newPage();

  const filePath = 'file://' + path.join(__dirname, 'correct.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  const TOTAL = 7;
  const viewport = await page.$('.carousel-viewport');

  for (let i of [0, 6]) {
    await page.evaluate((idx) => {
      const track = document.getElementById('track');
      track.style.transition = 'none';
      track.style.transform = `translateX(${-idx * 420}px)`;
    }, i);
    await page.waitForTimeout(200);

    const box = await viewport.boundingBox();
    const label = i === 0 ? 'cover' : 'last';
    await page.screenshot({
      path: path.join(__dirname, `correct_slide_${label}.png`),
      clip: { x: box.x, y: box.y, width: box.width, height: box.height },
    });
    console.log(`Captured: correct_slide_${label}.png`);
  }

  await browser.close();
})();
