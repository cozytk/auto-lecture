#!/usr/bin/env node
/**
 * Slidev 슬라이드 스크린샷 캡처 — 클릭 단계별 캡처
 * Usage: node scripts/capture-all-clicks.mjs <slides-dir> [slide-numbers...]
 * Output: screenshots-review/slide-NNN-cK.png (N=slide, K=click)
 */
import { mkdirSync, existsSync } from 'fs';
import { spawn } from 'child_process';
import { resolve, join } from 'path';
import { createRequire } from 'module';

const args = process.argv.slice(2);
const slidesDir = resolve(args.find(a => !a.startsWith('--')) || '.');
const requestedSlides = args.filter(a => !a.startsWith('--') && a !== args.find(b => !b.startsWith('--'))).map(Number).filter(n => n > 0);

const require = createRequire(join(slidesDir, 'node_modules', 'placeholder.js'));
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require('playwright-chromium')); }
const PORT = 3098;
const OUT = join(slidesDir, 'screenshots-review');
mkdirSync(OUT, { recursive: true });

async function waitForServer(port, timeout = 60000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    try {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), 2000);
      const res = await fetch(`http://localhost:${port}/1`, { signal: controller.signal });
      clearTimeout(id);
      if (res.ok) return true;
    } catch {}
    await new Promise(r => setTimeout(r, 1000));
  }
  throw new Error(`Server not ready after ${timeout}ms`);
}

console.log(`Starting slidev in ${slidesDir} on port ${PORT}...`);
const server = spawn('npx', ['slidev', '--port', String(PORT)], {
  cwd: slidesDir,
  stdio: 'pipe',
});
server.stderr.on('data', d => process.stderr.write(d));
const cleanup = () => { try { server.kill('SIGTERM'); } catch {} };
process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(1); });

try {
  await waitForServer(PORT);
  console.log('Server ready!');

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 980, height: 552 }, colorScheme: 'dark' });

  // Get total slides
  await page.goto(`http://localhost:${PORT}/1`, { waitUntil: 'networkidle' });
  await page.evaluate(() => {
    document.documentElement.classList.add('dark');
    if (window.__slidev__?.nav) window.__slidev__.nav.colorSchema = 'dark';
  });
  await page.waitForTimeout(300);
  let total = await page.evaluate(() => window.__slidev__?.nav?.total || 0);
  if (!total) {
    for (let i = 150; i >= 1; i--) {
      await page.goto(`http://localhost:${PORT}/${i}`, { waitUntil: 'networkidle' });
      if (page.url().includes(`/${i}`)) { total = i; break; }
    }
  }
  console.log(`Total slides: ${total}`);

  const slidesToCapture = requestedSlides.length > 0
    ? requestedSlides.filter(n => n <= total)
    : Array.from({ length: total }, (_, i) => i + 1);

  let fileCount = 0;
  for (const i of slidesToCapture) {
    // Capture click=0 (initial state)
    await page.goto(`http://localhost:${PORT}/${i}?clicks=0`, { waitUntil: 'networkidle' });
    await page.evaluate(() => {
      document.documentElement.classList.add('dark');
      if (window.__slidev__?.nav) window.__slidev__.nav.colorSchema = 'dark';
    });
    await page.waitForTimeout(400);

    // Take initial screenshot
    let prevPixels = await page.screenshot();
    const initPath = join(OUT, `slide-${String(i).padStart(3, '0')}-c0.png`);
    await page.screenshot({ path: initPath });
    fileCount++;
    console.log(`[${i}] c0 -> ${initPath}`);

    // Try clicks 1..20 (max), stop when screenshot doesn't change
    for (let c = 1; c <= 20; c++) {
      await page.goto(`http://localhost:${PORT}/${i}?clicks=${c}`, { waitUntil: 'networkidle' });
      await page.evaluate(() => {
        document.documentElement.classList.add('dark');
        if (window.__slidev__?.nav) window.__slidev__.nav.colorSchema = 'dark';
      });
      await page.waitForTimeout(400);

      const curPixels = await page.screenshot();
      // Compare buffers
      if (Buffer.compare(prevPixels, curPixels) === 0) {
        // No change — no more clicks on this slide
        break;
      }
      const clickPath = join(OUT, `slide-${String(i).padStart(3, '0')}-c${c}.png`);
      await page.screenshot({ path: clickPath });
      fileCount++;
      console.log(`[${i}] c${c} -> ${clickPath}`);
      prevPixels = curPixels;
    }
  }

  await browser.close();
  console.log(`\nDone! Captured ${fileCount} screenshots in ${OUT}`);
} finally {
  cleanup();
  await new Promise(r => setTimeout(r, 500));
  process.exit(0);
}
