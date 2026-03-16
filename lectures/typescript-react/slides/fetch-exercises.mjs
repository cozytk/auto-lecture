import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'fs';

const BASE = 'https://typescript-exercises.github.io';
const OUT = './exercises-raw';
mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // First load the site and wait for it to initialize
  await page.goto(BASE, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);

  for (let ex = 1; ex <= 10; ex++) {
    console.log(`\n=== Exercise ${ex} ===`);

    // Navigate to index.ts
    await page.goto(`${BASE}/#exercise=${ex}&file=%2Findex.ts`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // Get Monaco editor content using the model API
    const indexContent = await page.evaluate(() => {
      // Try Monaco editor models
      if (window.monaco) {
        const models = window.monaco.editor.getModels();
        for (const model of models) {
          const uri = model.uri.toString();
          if (uri.includes('index.ts') || uri.includes('/index')) {
            return model.getValue();
          }
        }
        // If no matching model found, get all model URIs for debugging
        if (models.length > 0) {
          return models[0].getValue();
        }
      }
      return null;
    });

    if (indexContent) {
      writeFileSync(`${OUT}/exercise${ex}-index.ts`, indexContent);
      console.log(`index.ts: ${indexContent.split('\n').length} lines`);
      // Print first and last few lines
      const lines = indexContent.split('\n');
      if (lines.length > 5) {
        console.log(`  First: ${lines[0].substring(0, 80)}`);
        console.log(`  Last:  ${lines[lines.length - 2].substring(0, 80)}`);
      }
    } else {
      // Fallback: try to get all model values
      const debug = await page.evaluate(() => {
        if (window.monaco) {
          const models = window.monaco.editor.getModels();
          return models.map(m => ({ uri: m.uri.toString(), lines: m.getLineCount() }));
        }
        return 'no monaco';
      });
      console.log('index.ts: Could not extract. Debug:', JSON.stringify(debug));
    }

    // Fetch test.ts
    await page.goto(`${BASE}/#exercise=${ex}&file=%2Ftest.ts`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    const testContent = await page.evaluate(() => {
      if (window.monaco) {
        const models = window.monaco.editor.getModels();
        for (const model of models) {
          const uri = model.uri.toString();
          if (uri.includes('test.ts') || uri.includes('/test')) {
            return model.getValue();
          }
        }
        if (models.length > 0) {
          return models[0].getValue();
        }
      }
      return null;
    });

    if (testContent) {
      writeFileSync(`${OUT}/exercise${ex}-test.ts`, testContent);
      console.log(`test.ts: ${testContent.split('\n').length} lines`);
    }

    // Try to get ALL models for the exercise (there may be multiple files)
    const allModels = await page.evaluate(() => {
      if (window.monaco) {
        const models = window.monaco.editor.getModels();
        return models.map(m => ({
          uri: m.uri.toString(),
          lineCount: m.getLineCount(),
          content: m.getValue()
        }));
      }
      return [];
    });

    for (const model of allModels) {
      const fname = model.uri.replace(/.*\//, '').replace(/[^a-zA-Z0-9._-]/g, '_');
      if (fname && !fname.includes('index') && !fname.includes('test')) {
        writeFileSync(`${OUT}/exercise${ex}-${fname}`, model.content);
        console.log(`${fname}: ${model.lineCount} lines`);
      }
    }
  }

  await browser.close();
  console.log('\nDone!');
})();
