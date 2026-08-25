const { chromium } = require('/Users/mac/.npm-global/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.join(__dirname, 'slides');

(async () => {
  if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  const filePath = 'file://' + path.join(__dirname, 'profile-card-vote.html');
  await page.goto(filePath, { waitUntil: 'load' });

  await page.waitForTimeout(1000);
  await page.evaluate(() => document.fonts.ready);

  const outPath = path.join(OUTPUT_DIR, 'post.png');
  await page.screenshot({ path: outPath });

  console.log(`Exported: ${outPath}`);
  await browser.close();
})();
