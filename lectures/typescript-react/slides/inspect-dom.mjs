import { chromium } from 'playwright';

const BASE = 'http://localhost:3030';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 980, height: 552 } });

  // 콘텐츠 양이 다양한 슬라이드 샘플
  for (const slideNum of [1, 2, 3, 10, 20, 30, 40, 50]) {
    await page.goto(`${BASE}/${slideNum}?clicks=99`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);

    const info = await page.evaluate(() => {
      const results = {};

      // 주요 셀렉터들의 크기와 overflow 속성 확인
      const selectors = ['.slidev-page', '.slidev-layout', '.slide-content', '#slide-content'];
      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el) {
          const rect = el.getBoundingClientRect();
          const style = getComputedStyle(el);
          results[sel] = {
            tagName: el.tagName,
            className: (el.className || '').substring(0, 80),
            scrollHeight: el.scrollHeight,
            clientHeight: el.clientHeight,
            rectHeight: Math.round(rect.height),
            rectTop: Math.round(rect.top),
            rectBottom: Math.round(rect.bottom),
            overflow: style.overflow,
            overflowY: style.overflowY,
            height: style.height,
            maxHeight: style.maxHeight,
            position: style.position,
          };
        }
      }

      // DOM 트리: .slidev-layout부터 body까지 올라가며 각 노드 정보
      const layout = document.querySelector('.slidev-layout');
      if (layout) {
        const chain = [];
        let el = layout;
        while (el && el.tagName !== 'BODY') {
          const s = getComputedStyle(el);
          chain.unshift({
            tag: el.tagName,
            cls: (el.className || '').split(' ')[0],
            h: Math.round(el.getBoundingClientRect().height),
            sH: el.scrollHeight,
            cH: el.clientHeight,
            ovY: s.overflowY,
          });
          el = el.parentElement;
        }
        results._parentChain = chain;

        // 마지막 자식 요소의 bottom 좌표
        const children = layout.children;
        if (children.length > 0) {
          const last = children[children.length - 1];
          const lastRect = last.getBoundingClientRect();
          results._lastChildBottom = Math.round(lastRect.bottom);
          results._layoutTop = Math.round(layout.getBoundingClientRect().top);
          results._contentHeight = Math.round(lastRect.bottom - layout.getBoundingClientRect().top);
        }
      }

      results._viewportHeight = window.innerHeight;

      return results;
    });

    console.log(`\n=== Slide ${slideNum} ===`);
    console.log(JSON.stringify(info, null, 2));
  }

  await browser.close();
  console.log('\nDone!');
})();
