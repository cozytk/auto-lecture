import { chromium } from 'playwright';
import { mkdirSync } from 'fs';

const BASE = 'http://localhost:3030';
const OUT = './screenshots';
mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 980, height: 552 } });

  // First, determine total slide count by navigating to page 1
  await page.goto(`${BASE}/1`, { waitUntil: 'networkidle' });

  // Try to get total slides from the slide counter
  const totalText = await page.locator('.slidev-nav-total, [class*="total"]').textContent().catch(() => null);
  let total = totalText ? parseInt(totalText) : 0;

  if (!total) {
    // Fallback: try navigating until we get redirected or 404
    total = 50; // reasonable upper bound
    for (let i = 50; i >= 1; i--) {
      const resp = await page.goto(`${BASE}/${i}`, { waitUntil: 'networkidle' });
      const url = page.url();
      // If we land on the page we requested, this slide exists
      if (url.includes(`/${i}`) && resp.status() === 200) {
        total = i;
        break;
      }
    }
  }

  console.log(`Total slides: ${total}`);

  for (let i = 1; i <= total; i++) {
    await page.goto(`${BASE}/${i}?clicks=99`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500); // let animations settle
    const path = `${OUT}/slide-${String(i).padStart(2, '0')}.png`;
    await page.screenshot({ path });
    console.log(`Screenshot: slide ${i}/${total}`);
  }

  await browser.close();
  console.log('Done!');
})();
