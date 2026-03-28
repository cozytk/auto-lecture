#!/usr/bin/env node
/**
 * Slidev 슬라이드 스크린샷 도구
 * Usage: node scripts/screenshot-slides.mjs <slides-dir> [--port 3030] [--start]
 *
 * --start: slidev dev 서버를 자동으로 시작/종료
 * --port:  slidev 포트 (기본 3030)
 * --max:   최대 스크린샷 수 (기본 전체)
 */
import { chromium } from 'playwright';
import { mkdirSync, existsSync } from 'fs';
import { spawn } from 'child_process';
import { resolve, join } from 'path';

const args = process.argv.slice(2);
const slidesDir = args.find(a => !a.startsWith('--'));
const port = args.includes('--port') ? args[args.indexOf('--port') + 1] : '3030';
const shouldStart = args.includes('--start');
const maxSlides = args.includes('--max') ? parseInt(args[args.indexOf('--max') + 1]) : Infinity;

if (!slidesDir) {
  console.error('Usage: node scripts/screenshot-slides.mjs <slides-dir> [--start] [--port 3030]');
  process.exit(1);
}

const absDir = resolve(slidesDir);
const outDir = join(absDir, 'screenshots');
mkdirSync(outDir, { recursive: true });

const BASE = `http://localhost:${port}`;

async function waitForServer(url, timeoutMs = 30000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await fetch(url);
      if (res.ok) return true;
    } catch {}
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error(`Server not ready at ${url} after ${timeoutMs}ms`);
}

async function getTotalSlides(page) {
  await page.goto(`${BASE}/1`, { waitUntil: 'networkidle' });
  // Slidev embeds total in the nav
  const total = await page.evaluate(() => {
    // Method 1: __slidev__ global
    if (window.__slidev__?.nav?.total) return window.__slidev__.nav.total;
    // Method 2: DOM counter
    const el = document.querySelector('.slidev-nav-total');
    if (el) return parseInt(el.textContent);
    return 0;
  });
  if (total > 0) return total;

  // Fallback: binary search
  let lo = 1, hi = 200;
  while (lo < hi) {
    const mid = Math.ceil((lo + hi) / 2);
    await page.goto(`${BASE}/${mid}`, { waitUntil: 'networkidle' });
    const url = page.url();
    if (url.includes(`/${mid}`)) lo = mid;
    else hi = mid - 1;
  }
  return lo;
}

(async () => {
  let serverProc = null;

  if (shouldStart) {
    console.log(`Starting slidev in ${absDir} on port ${port}...`);
    serverProc = spawn('npx', ['slidev', '--port', port, '--remote'], {
      cwd: absDir,
      stdio: 'pipe',
      shell: true,
    });
    serverProc.stdout.on('data', d => process.stderr.write(d));
    serverProc.stderr.on('data', d => process.stderr.write(d));
    await waitForServer(BASE);
    console.log('Slidev server ready.');
  }

  try {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 980, height: 552 } });

    const total = await getTotalSlides(page);
    const count = Math.min(total, maxSlides);
    console.log(`Total slides: ${total}, capturing: ${count}`);

    const paths = [];
    for (let i = 1; i <= count; i++) {
      // clicks=99 to reveal all v-clicks
      await page.goto(`${BASE}/${i}?clicks=99`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(400);
      const path = join(outDir, `slide-${String(i).padStart(3, '0')}.png`);
      await page.screenshot({ path });
      paths.push(path);
      console.log(`[${i}/${count}] ${path}`);
    }

    await browser.close();
    console.log(`\nDone! Screenshots saved to ${outDir}`);
    // Output paths as JSON for programmatic use
    console.log(JSON.stringify({ total, captured: count, dir: outDir, files: paths }));
  } finally {
    if (serverProc) {
      serverProc.kill('SIGTERM');
      console.log('Slidev server stopped.');
    }
  }
})();
