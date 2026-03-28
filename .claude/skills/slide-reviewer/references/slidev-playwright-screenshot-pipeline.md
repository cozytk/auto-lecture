# Slidev Playwright Screenshot Pipeline

Slidev의 dev 서버 + Playwright 스크린샷 파이프라인에는 3가지 독립적인 비직관적 실패 지점이 있다. 각각 다른 계층(Node 모듈 시스템, 브라우저 DOM, HTTP 서버)에서 발생하므로 한꺼번에 디버깅하면 원인을 혼동하기 쉽다.

## 1. 모듈 해석: `createRequire` 패턴

`playwright`는 각 `lectures/{topic}/slides/node_modules/`에 설치되어 있다. 프로젝트 루트의 ESM 스크립트에서 import하면 실패한다.

**원칙**: 의존성이 서브디렉토리에 있으면 `createRequire`로 해당 디렉토리 기준 require를 생성한다.

```js
import { createRequire } from 'module';
const require = createRequire(join(slidesDir, 'node_modules', 'placeholder.js'));
const { chromium } = require('playwright');
```

## 2. 다크모드 이중 토글

Playwright의 `colorScheme: 'dark'`는 CSS `prefers-color-scheme` 미디어 쿼리만 제어한다. Slidev는 자체적으로 `<html class="dark">`와 내부 상태(`__slidev__.nav.colorSchema`)를 별도로 관리한다.

**원칙**: 두 계층 모두 설정해야 한다. 매 페이지 이동(goto) 후에 다시 설정해야 한다.

```js
// Playwright 레벨
const page = await browser.newPage({ viewport: { width: 980, height: 552 }, colorScheme: 'dark' });

// Slidev DOM 레벨 (매 goto 후)
await page.evaluate(() => {
  document.documentElement.classList.add('dark');
  if (window.__slidev__?.nav) window.__slidev__.nav.colorSchema = 'dark';
});
```

## 3. 서버 준비 타이밍

Slidev(Vite)는 배너를 stdout에 출력한 후에도 HTTP 서버가 아직 bind되지 않았을 수 있다. 별도 셸 세션에서는 백그라운드 프로세스가 유지되지 않으므로 **같은 프로세스 내에서** 서버를 spawn하고 fetch 폴링해야 한다.

**원칙**: `sleep`이 아닌 `fetch` 기반 폴링. 타임아웃 60초. AbortController로 개별 요청 제한.

```js
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
```

## 추가: spawn 옵션

- `shell: true`는 Node.js 24에서 DEP0190 deprecation warning을 발생시킨다 → 제거
- `stdio: 'pipe'`로 서버 출력을 제어 (stderr만 forward하면 디버깅 가능)
- `?clicks=99` 파라미터로 모든 v-click 애니메이션을 펼친 최종 상태 캡처

## 참조 스크립트

현재 동작하는 전체 스크립트: `scripts/capture-slide.mjs`
