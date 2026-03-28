#!/usr/bin/env node
/**
 * Slidev 슬라이드 스크린샷 캡처 스크립트
 * Usage: node scripts/capture-slide.mjs <slides-dir> [--light] [slide-numbers...]
 * Example: node scripts/capture-slide.mjs lectures/typescript-react/slides 3 5 10
 *          node scripts/capture-slide.mjs lectures/typescript-react/slides   (all slides)
 *          node scripts/capture-slide.mjs lectures/typescript-react/slides --light 1 2 3  (light mode)
 */
import { mkdirSync } from 'fs';
import { spawn } from 'child_process';
import { resolve, join } from 'path';
import { createRequire } from 'module';

const args = process.argv.slice(2);
const slidesDir = resolve(args.find(a => !a.startsWith('--')) || '.');
const lightMode = args.includes('--light');
const darkMode = !lightMode; // dark mode is default
const requestedSlides = args.filter(a => !a.startsWith('--') && a !== args.find(b => !b.startsWith('--'))).map(Number).filter(n => n > 0);

// Resolve playwright from the slides directory (where it's installed)
const require = createRequire(join(slidesDir, 'node_modules', 'placeholder.js'));
const { chromium } = require('playwright');
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

// Forward stderr for debugging
server.stderr.on('data', d => process.stderr.write(d));

// Graceful cleanup
const cleanup = () => { try { server.kill('SIGTERM'); } catch {} };
process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(1); });

try {
  await waitForServer(PORT);
  console.log('Server ready!');

  const browser = await chromium.launch();
  const colorScheme = darkMode ? 'dark' : 'light';
  const page = await browser.newPage({ viewport: { width: 980, height: 552 }, colorScheme });
  console.log(`Color scheme: ${colorScheme}`);

  // Determine total slides
  await page.goto(`http://localhost:${PORT}/1`, { waitUntil: 'networkidle' });
  // Ensure Slidev dark mode is toggled via its internal API
  if (darkMode) {
    await page.evaluate(() => {
      document.documentElement.classList.add('dark');
      if (window.__slidev__?.nav) window.__slidev__.nav.colorSchema = 'dark';
    });
    await page.waitForTimeout(300);
  }
  let total = await page.evaluate(() => window.__slidev__?.nav?.total || 0);
  if (!total) {
    for (let i = 150; i >= 1; i--) {
      const resp = await page.goto(`http://localhost:${PORT}/${i}`, { waitUntil: 'networkidle' });
      if (page.url().includes(`/${i}`)) { total = i; break; }
    }
  }
  console.log(`Total slides: ${total}`);

  const slidesToCapture = requestedSlides.length > 0
    ? requestedSlides.filter(n => n <= total)
    : Array.from({ length: total }, (_, i) => i + 1);

  const results = [];
  for (const i of slidesToCapture) {
    await page.goto(`http://localhost:${PORT}/${i}?clicks=99`, { waitUntil: 'networkidle' });
    if (darkMode) {
      await page.evaluate(() => {
        document.documentElement.classList.add('dark');
        if (window.__slidev__?.nav) window.__slidev__.nav.colorSchema = 'dark';
      });
    }
    await page.waitForTimeout(400);
    const filePath = join(OUT, `slide-${String(i).padStart(3, '0')}.png`);
    await page.screenshot({ path: filePath });
    results.push(filePath);
    console.log(`[${i}/${total}] ${filePath}`);
  }

  await browser.close();
  console.log(JSON.stringify({ total, captured: results.length, dir: OUT, files: results }));
} finally {
  cleanup();
  // Give server time to shut down
  await new Promise(r => setTimeout(r, 500));
  console.log('Done.');
  process.exit(0);
}
