# Session 3: React + TypeScript 프로젝트 설정

**시간**: 1시간 | **유형**: 강의 + Guided Coding

---

## 학습 목표

이 세션이 끝나면 수강생들은 다음을 할 수 있어야 합니다.

- React가 무엇인지, 왜 사용하는지 설명할 수 있다
- Vite로 React + TypeScript 프로젝트를 생성하고 개발 서버를 실행할 수 있다
- 생성된 프로젝트의 파일 구조를 이해하고 각 파일의 역할을 설명할 수 있다
- 첫 번째 React 함수형 컴포넌트를 직접 작성할 수 있다
- JSX의 핵심 문법 규칙 5가지를 숙지하고 코드에 적용할 수 있다

---

## 강사 준비 사항

> **강사 안내**: 수업 시작 전에 다음 항목을 확인합니다.
>
> - Node.js 18 이상 설치 여부 확인 (`node -v`)
> - npm 9 이상 설치 여부 확인 (`npm -v`)
> - 인터넷 연결이 불안정한 환경이라면, 미리 `npm create vite@latest`로 프로젝트를 생성해두고 `node_modules`를 포함한 zip 파일을 준비합니다
> - 브라우저(Chrome 권장)를 열어두고, `http://localhost:5173` 접속을 미리 테스트합니다
> - 코드 에디터(VS Code 권장)와 터미널을 준비합니다

---

## 시간 배분

| 단계 | 내용 | 시간 |
|------|------|------|
| 강의 | React 소개, 핵심 개념 | 10분 |
| Guided Coding | Vite 프로젝트 생성 + 구조 분석 | 30분 |
| 독립 실습 | 첫 컴포넌트 자력 작성 | 10분 |
| 정리 / Q&A | 핵심 요약 + 질문 | 10분 |

---

## 1. React 소개 (10분)

### 1.1 React란 무엇인가

React는 Meta(전 Facebook)가 만든 **사용자 인터페이스(UI) 라이브러리**입니다.

중요한 것은 React는 프레임워크(Framework)가 아니라 **라이브러리(Library)**라는 점입니다. 즉, 모든 것을 처음부터 규정하는 완전한 틀이 아니라, UI를 만드는 데 집중하는 도구입니다. 라우팅, 상태 관리 등은 별도의 라이브러리를 선택하여 조합합니다.

React의 핵심 아이디어는 **컴포넌트(Component)**입니다. 웹 페이지를 하나의 거대한 HTML 파일로 만드는 대신, 작은 독립적인 조각(컴포넌트)으로 나누어 만든 뒤 조합합니다.

예를 들어, 쇼핑몰 페이지는 다음과 같이 분해할 수 있습니다.

```
<App>
  <Header>
    <Logo />
    <SearchBar />
    <CartIcon />
  </Header>
  <ProductList>
    <ProductCard />
    <ProductCard />
    <ProductCard />
  </ProductList>
  <Footer />
</App>
```

각 컴포넌트는 자신의 HTML 구조, 스타일, 로직을 스스로 관리합니다. 재사용이 가능하며, 한 곳에서 수정하면 해당 컴포넌트를 사용하는 모든 곳에 반영됩니다.

> **강사 안내**: 화이트보드나 슬라이드에 위 컴포넌트 트리 구조를 그려가며 설명합니다. "레고 블록을 조립하듯이 UI를 만든다"는 비유가 효과적입니다.

---

### 1.2 선언적(Declarative) vs 명령적(Imperative)

React를 이해하는 데 가장 중요한 개념 중 하나가 **선언적 프로그래밍**입니다.

**명령적 방식 (Vanilla JavaScript)**

명령적 방식은 "어떻게(How)" 결과를 만들지 단계별로 지시합니다.

```javascript
// Vanilla JS — 명령적 방식
// 사용자 이름을 표시하고, 로그인 여부에 따라 버튼 텍스트를 바꾸는 코드

const container = document.getElementById('app');

// 1. h1 요소를 직접 생성
const h1 = document.createElement('h1');
h1.textContent = '안녕하세요, 김태민님!';
container.appendChild(h1);

// 2. 버튼을 직접 생성
const button = document.createElement('button');

// 3. 로그인 상태에 따라 텍스트를 직접 변경
const isLoggedIn = true;
if (isLoggedIn) {
  button.textContent = '로그아웃';
} else {
  button.textContent = '로그인';
}

container.appendChild(button);

// 4. 나중에 상태가 바뀌면, 다시 DOM을 직접 찾아서 수정
// document.querySelector('button').textContent = '로그인';
```

이 방식은 간단한 예시에서는 괜찮지만, 상태가 많아지고 UI가 복잡해질수록 DOM 조작 코드가 여기저기 흩어져 관리하기 어려워집니다.

**선언적 방식 (React)**

선언적 방식은 "무엇(What)"이 되어야 하는지를 선언합니다. "이 데이터가 이러한 상태라면, UI는 이렇게 보여야 한다"고 기술합니다.

```tsx
// React — 선언적 방식
// isLoggedIn 값에 따라 UI가 자동으로 결정됨

function UserSection({ name, isLoggedIn }: { name: string; isLoggedIn: boolean }) {
  return (
    <div>
      <h1>안녕하세요, {name}님!</h1>
      <button>{isLoggedIn ? '로그아웃' : '로그인'}</button>
    </div>
  );
}
```

이 코드는 `isLoggedIn`이 `true`면 "로그아웃"을, `false`면 "로그인"을 보여줍니다. DOM을 직접 건드리는 코드가 없습니다. **데이터가 바뀌면 React가 알아서 UI를 업데이트**합니다.

> **강사 안내**: "결과만 선언하면 React가 DOM 업데이트를 대신 해준다"는 점을 강조합니다. Vanilla JS 코드에서는 상태가 바뀔 때마다 개발자가 직접 DOM을 찾아서 수정해야 하지만, React에서는 상태 변수 하나만 바꾸면 화면이 자동으로 갱신됩니다.

---

### 1.3 Virtual DOM (간략 소개)

React가 선언적 방식을 효율적으로 구현하는 방법이 **Virtual DOM**입니다.

실제 DOM 조작은 비용이 큰 작업입니다. 브라우저는 DOM이 바뀔 때마다 레이아웃을 다시 계산하고 화면을 다시 그려야 합니다.

React는 다음 방식으로 이 문제를 해결합니다.

1. 실제 DOM과 동일한 구조의 **가상 DOM(Virtual DOM)**을 메모리에 유지합니다
2. 상태가 바뀌면, 새로운 가상 DOM을 생성합니다
3. 이전 가상 DOM과 새 가상 DOM을 **비교(Diffing)**하여 변경된 부분만 찾아냅니다
4. 변경된 부분만 실제 DOM에 반영합니다 — 이를 **Reconciliation(재조정)**이라고 합니다

> **강사 안내**: 내부 구현 원리보다는 "React가 알아서 최소한의 DOM 업데이트만 수행한다"는 결과에 집중합니다. 심화 내용(Fiber 아키텍처 등)은 이 수업의 범위를 벗어납니다.

---

### 1.4 React 생태계 개요

React 자체는 UI 라이브러리이지만, 실제 개발에는 다양한 도구가 함께 사용됩니다.

| 도구 | 역할 | 우리가 사용하는가 |
|------|------|------------------|
| **Vite** | 빠른 개발 서버 및 빌드 도구 | 사용 (이번 세션) |
| **React Router** | 클라이언트 사이드 라우팅 | 이후 세션 |
| **TanStack Query** | 서버 상태 관리 | 이후 세션 |
| **Zustand / Jotai** | 전역 클라이언트 상태 관리 | 이후 세션 |
| **Next.js** | 서버사이드 렌더링(SSR), 풀스택 | 별도 과정 |
| **Create React App** | 과거 표준 도구 (현재는 비권장) | 사용 안 함 |

**왜 Vite인가?**

Create React App(CRA)은 오랫동안 React 프로젝트의 표준 시작 도구였습니다. 하지만 프로젝트 규모가 커질수록 개발 서버 시작 속도가 느려지고, 더 이상 활발하게 관리되지 않습니다.

Vite는 **네이티브 ES Module**을 활용하여 개발 서버를 거의 즉시 시작합니다. 대규모 프로젝트에서도 파일 변경 후 브라우저 반영(HMR, Hot Module Replacement)이 수십 밀리초 안에 이루어집니다. 현재 React 공식 문서도 Vite 사용을 권장합니다.

---

## 2. Vite 프로젝트 생성 [실습 포인트] (15분)

> **강사 안내**: 이 섹션부터는 학생들이 직접 타이핑합니다. 강사가 먼저 전체 흐름을 1회 시연한 뒤, 학생들이 따라 실행합니다. 각 명령어 실행 후 터미널 출력을 함께 확인합니다.

### 2.1 프로젝트 생성 명령어

터미널을 열고 프로젝트를 만들 상위 디렉토리로 이동합니다. 예를 들어 바탕화면이나 `~/projects/` 폴더를 사용합니다.

```bash
npm create vite@latest my-react-app -- --template react-ts
```

**각 부분의 의미:**

- `npm create`: `npm init`의 alias입니다. `create-*` 형태의 패키지를 이용해 프로젝트를 초기화합니다
- `vite@latest`: `create-vite` 패키지의 최신 버전을 사용하겠다는 의미입니다. 특정 버전을 고정하려면 `vite@5.0.0` 처럼 명시할 수 있습니다
- `my-react-app`: 생성할 프로젝트 폴더 이름입니다. 원하는 이름으로 변경할 수 있습니다
- `--`: 이후의 인자(argument)가 `npm create` 자체가 아닌 `create-vite`에 전달됨을 의미합니다
- `--template react-ts`: React + TypeScript 템플릿을 사용합니다. `react`만 입력하면 JavaScript 버전이 생성됩니다

**예상 터미널 출력:**

```
Scaffolding project in /Users/username/my-react-app...

Done. Now run:

  cd my-react-app
  npm install
  npm run dev
```

> **강사 안내**: 출력 메시지가 보이면 "Scaffolding은 '비계(건물 외벽에 세우는 임시 구조물)'라는 뜻으로, 프로젝트 뼈대를 잡아준다는 의미입니다"라고 설명합니다.

---

### 2.2 프로젝트 폴더로 이동

```bash
cd my-react-app
```

이 명령어는 방금 생성된 `my-react-app` 폴더 안으로 진입합니다. 이후 모든 명령어는 이 폴더 안에서 실행합니다.

---

### 2.3 의존성 설치

```bash
npm install
```

**무슨 일이 일어나는가:**

`package.json`에 명시된 모든 의존성 패키지를 `node_modules/` 폴더에 다운로드하고 설치합니다. 처음 실행 시 수십 개의 패키지를 다운로드하므로 시간이 걸릴 수 있습니다.

**예상 터미널 출력:**

```
added 187 packages, and audited 188 packages in 8s

44 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

> **강사 안내**: "added 187 packages"라고 나왔다고 당황할 필요가 없습니다. 직접 사용하는 패키지(React, TypeScript 등)를 설치하면 그것들이 필요로 하는 패키지들(의존성의 의존성)도 함께 설치되기 때문에 숫자가 많아집니다.

**Fallback: 인터넷이 느리거나 없는 환경**

> **강사 안내**: 사전에 준비한 방법을 안내합니다.
>
> **방법 1 — USB/공유 드라이브 배포:**
> 미리 `npm install`까지 완료한 폴더를 zip으로 압축하여 배포합니다.
> 학생들은 zip을 압축 해제하면 `npm install` 없이 바로 `npm run dev`를 실행할 수 있습니다.
>
> **방법 2 — npm 로컬 캐시 활용:**
> 강사 컴퓨터에서 한 번 설치한 후, `~/.npm` 캐시를 공유 드라이브에 복사합니다.
> 학생들은 `npm install --prefer-offline`으로 캐시에서 설치합니다.

---

### 2.4 개발 서버 실행

```bash
npm run dev
```

**무슨 일이 일어나는가:**

`package.json`의 `scripts` 섹션에 정의된 `dev` 스크립트를 실행합니다. 이 스크립트는 `vite`를 실행하여 개발 서버를 시작합니다.

**예상 터미널 출력:**

```
  VITE v5.x.x  ready in 342 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

> **강사 안내**: 터미널에 위 메시지가 출력되면, 학생들에게 브라우저를 열고 `http://localhost:5173`에 접속하도록 안내합니다.

---

### 2.5 브라우저에서 기본 화면 확인

브라우저에서 `http://localhost:5173`에 접속하면 Vite + React 기본 화면이 표시됩니다.

**기본 화면에서 볼 수 있는 것:**

- Vite 로고와 React 로고 (클릭하면 각 공식 문서로 이동)
- "count is 0" 버튼 — 클릭할 때마다 숫자가 증가합니다
- "Edit `src/App.tsx` and save to test HMR" 안내 문구

> **강사 안내**: 학생들이 화면을 확인한 뒤, "이제 `src/App.tsx` 파일을 열어보세요"라고 안내합니다. 파일을 수정하고 저장하면 브라우저가 자동으로 갱신되는 것(HMR)을 직접 보여주면 효과적입니다. 예를 들어, `<h1>Vite + React</h1>`를 `<h1>안녕하세요!</h1>`로 바꾸면 저장 즉시 브라우저에 반영됩니다.

**포트 충돌이 발생하는 경우:**

이미 5173 포트가 사용 중이면 Vite가 자동으로 다음 포트(5174, 5175...)를 사용합니다. 터미널 출력에서 실제 URL을 확인합니다.

**개발 서버 종료 방법:**

터미널에서 `Ctrl + C`를 누르면 개발 서버가 종료됩니다.

---

## 3. 프로젝트 구조 이해 (15분)

> **강사 안내**: VS Code에서 프로젝트 폴더를 열고, 파일 탐색기를 보며 설명합니다. `code .` 명령어를 터미널에서 실행하면 현재 폴더를 VS Code로 바로 열 수 있습니다.

### 3.1 전체 파일 구조

```
my-react-app/
├── node_modules/          # 설치된 npm 패키지들 (git에 포함하지 않음)
├── public/
│   └── vite.svg           # 정적 자산 (URL로 직접 접근 가능)
├── src/
│   ├── assets/
│   │   └── react.svg      # 코드에서 import하는 자산
│   ├── App.css            # App 컴포넌트 스타일
│   ├── App.tsx            # 루트 컴포넌트
│   ├── index.css          # 전역 스타일
│   └── main.tsx           # React 앱 진입점
├── .eslintrc.cjs          # ESLint 설정 (코드 스타일 검사)
├── .gitignore             # Git에 포함하지 않을 파일 목록
├── index.html             # SPA의 HTML 진입점
├── package.json           # 프로젝트 메타데이터 및 의존성
├── package-lock.json      # 정확한 의존성 버전 고정 파일
├── tsconfig.json          # TypeScript 컴파일러 설정
├── tsconfig.node.json     # Vite 설정 파일용 TypeScript 설정
└── vite.config.ts         # Vite 빌드 도구 설정
```

---

### 3.2 `index.html` — SPA의 HTML 진입점

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React + TS</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**핵심 포인트:**

- `<div id="root"></div>`: React 앱이 마운트될 컨테이너입니다. React는 이 div 안에 모든 UI를 렌더링합니다
- `<script type="module" src="/src/main.tsx">`: 앱의 진입점 파일을 로드합니다. `type="module"`은 ES Module 방식을 사용한다는 의미입니다
- **SPA(Single Page Application)**란: 페이지 이동 시 새로운 HTML 파일을 서버에서 받는 것이 아니라, JavaScript가 동적으로 화면을 교체합니다. `index.html` 파일은 단 하나뿐이며, 모든 라우트가 이 파일을 기반으로 동작합니다

---

### 3.3 `src/main.tsx` — React 앱의 진입점

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**각 줄 상세 설명:**

**`import React from 'react'`**

React 라이브러리를 가져옵니다. React 17 이후부터는 JSX 변환이 자동으로 이루어지기 때문에 `import React`를 생략할 수 있는 경우도 있지만, 명시적으로 작성하는 것이 일반적입니다.

**`import ReactDOM from 'react-dom/client'`**

React를 실제 브라우저 DOM에 연결하는 역할을 하는 `ReactDOM`을 가져옵니다. `/client`를 명시하는 것은 React 18에서 도입된 클라이언트 렌더링 API를 사용한다는 의미입니다.

**`import App from './App.tsx'`**

루트 컴포넌트인 `App`을 가져옵니다. `.tsx` 확장자는 TypeScript + JSX 파일을 의미합니다.

**`import './index.css'`**

전역 CSS 파일을 가져옵니다. 이 파일의 스타일은 앱 전체에 적용됩니다.

**`document.getElementById('root')!`**

`index.html`의 `<div id="root">`를 찾아옵니다. 끝의 `!`는 TypeScript의 **Non-null Assertion Operator**입니다. `getElementById`는 요소를 찾지 못하면 `null`을 반환하므로, TypeScript는 타입을 `HTMLElement | null`로 추론합니다. `!`를 붙이면 "이 값은 절대 null이 아니다"라고 TypeScript에게 보장합니다. `index.html`에 `id="root"` div가 반드시 존재하므로 이 단언이 유효합니다.

**`ReactDOM.createRoot(...).render(...)`**

React 18에서 도입된 새 렌더링 방식입니다. `createRoot`로 루트를 생성하고, `render`로 컴포넌트 트리를 마운트합니다. React 17까지는 `ReactDOM.render(<App />, document.getElementById('root'))`를 사용했습니다.

**`<React.StrictMode>`**

개발 환경에서만 동작하는 도우미 컴포넌트입니다. 다음과 같은 잠재적 문제를 감지하여 경고를 출력합니다.

- 잘못된 생명주기 메서드 사용
- 예상치 못한 부수 효과(side effect) 감지를 위해 컴포넌트를 **의도적으로 두 번 렌더링** (이로 인해 `console.log`가 두 번 찍히는 것을 볼 수 있는데, 이는 정상입니다)
- 구식 API 사용 경고

빌드 배포 시(프로덕션)에는 자동으로 비활성화됩니다.

---

### 3.4 `src/App.tsx` — 루트 컴포넌트

```tsx
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
```

> **강사 안내**: 지금 이 코드의 모든 내용을 이해할 필요는 없습니다. `useState`와 이벤트 처리는 다음 세션에서 다룹니다. 지금은 "함수가 JSX를 반환하면 컴포넌트다"라는 점에 집중합니다.

---

### 3.5 `tsconfig.json` — TypeScript 설정

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**중요 옵션 설명:**

- **`"strict": true`**: TypeScript의 모든 엄격한 타입 검사를 활성화합니다. `noImplicitAny`, `strictNullChecks` 등이 포함됩니다. 처음에는 오류가 더 많이 발생하지만, 버그를 컴파일 시점에 잡아주므로 장기적으로 더 안전합니다
- **`"jsx": "react-jsx"`**: JSX를 어떻게 변환할지 지정합니다. `"react-jsx"`는 React 17에서 도입된 새 변환 방식으로, `import React from 'react'` 없이도 JSX를 사용할 수 있게 합니다
- **`"noEmit": true`**: TypeScript 컴파일러가 실제 JavaScript 파일을 생성하지 않습니다. 실제 빌드는 Vite가 담당하며, TypeScript는 타입 검사만 수행합니다
- **`"noUnusedLocals": true`**: 선언되었지만 사용되지 않는 지역 변수가 있으면 오류를 발생시킵니다
- **`"noUnusedParameters": true`**: 사용되지 않는 함수 파라미터가 있으면 오류를 발생시킵니다

---

### 3.6 `vite.config.ts` — Vite 설정

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

기본 설정은 매우 단순합니다. `@vitejs/plugin-react`는 Fast Refresh(파일 저장 시 컴포넌트 상태를 유지하면서 UI를 갱신하는 기능)와 JSX 변환을 처리합니다. 이후에 경로 별칭(`@/`), 프록시 설정 등을 추가하게 됩니다.

---

## 4. 첫 번째 컴포넌트 작성 [실습 포인트] (10분)

> **강사 안내**: 학생들이 `src/` 폴더 안에 새 파일 `Greeting.tsx`를 직접 만들어보는 시간입니다. VS Code에서 파일을 생성하는 방법(파일 탐색기에서 우클릭 → New File)을 안내합니다.

### 4.1 함수형 컴포넌트의 기본 구조

React 컴포넌트는 **JSX를 반환하는 TypeScript 함수**입니다.

반드시 지켜야 할 규칙이 두 가지 있습니다.

1. **함수 이름은 반드시 대문자로 시작합니다** — `greeting`이 아닌 `Greeting`. 소문자로 시작하면 React가 이를 HTML 태그로 해석합니다
2. **JSX를 반환해야 합니다** — 아무것도 표시할 게 없으면 `null`을 반환할 수 있습니다

---

### 4.2 `Greeting.tsx` 파일 작성

`src/Greeting.tsx` 파일을 새로 만들고 다음 코드를 작성합니다.

```tsx
// src/Greeting.tsx

interface GreetingProps {
  name: string;
  role?: string;  // ? 는 선택적 prop (없어도 됨)
}

function Greeting({ name, role }: GreetingProps) {
  return (
    <div>
      <h1>안녕하세요, {name}님!</h1>
      {role && <p>역할: {role}</p>}
    </div>
  );
}

export default Greeting;
```

**코드 설명:**

**`interface GreetingProps`**

컴포넌트가 받을 props의 타입을 정의합니다. TypeScript를 사용하는 React의 핵심 패턴입니다.

- `name: string` — 필수 prop. 없으면 TypeScript 오류가 발생합니다
- `role?: string` — 선택적 prop. `?`를 붙이면 `string | undefined` 타입이 됩니다

**`function Greeting({ name, role }: GreetingProps)`**

**구조 분해 할당(Destructuring)**으로 props를 받습니다. `props.name`, `props.role` 대신 바로 `name`, `role`로 사용할 수 있습니다.

만약 구조 분해를 사용하지 않는다면:

```tsx
// 구조 분해 없이 쓰는 경우 (권장하지 않음)
function Greeting(props: GreetingProps) {
  return <h1>안녕하세요, {props.name}님!</h1>;
}
```

구조 분해가 더 간결하고 읽기 쉬우므로 현업에서는 구조 분해를 사용하는 것이 일반적입니다.

**`{role && <p>역할: {role}</p>}`**

`role`이 전달된 경우에만 `<p>` 태그를 렌더링합니다. `role`이 `undefined`이면 아무것도 렌더링하지 않습니다. 이것이 React의 **조건부 렌더링** 패턴입니다.

**`export default Greeting`**

컴포넌트를 기본 내보내기(default export)로 내보냅니다. 다른 파일에서 `import Greeting from './Greeting'`으로 가져올 수 있습니다.

---

### 4.3 `App.tsx`에서 Greeting 사용

`App.tsx`를 수정하여 방금 만든 컴포넌트를 사용합니다. 기존 내용을 전부 지우고 다음과 같이 작성합니다.

```tsx
// src/App.tsx

import Greeting from './Greeting';

function App() {
  return (
    <div>
      <Greeting name="김태민" role="수강생" />
      <Greeting name="이선생" role="강사" />
      <Greeting name="박철수" />
    </div>
  );
}

export default App;
```

파일을 저장하면 브라우저가 자동으로 갱신됩니다.

**확인 사항:**

- "안녕하세요, 김태민님!" 과 "역할: 수강생"이 표시됩니다
- "안녕하세요, 이선생님!" 과 "역할: 강사"가 표시됩니다
- "안녕하세요, 박철수님!" 은 표시되지만 "역할:" 줄은 없습니다 (`role`을 전달하지 않았으므로)

> **강사 안내**: `App.tsx`에서 `<Greeting />` 태그를 작성할 때 VS Code가 자동 완성으로 `name` prop을 제안하는 것을 보여줍니다. `name`을 빠뜨리면 TypeScript가 오류를 표시합니다. "TypeScript가 우리 컴포넌트의 props를 이해하고 있다"는 점을 강조합니다.

---

### 4.4 named export vs default export

```tsx
// default export — 한 파일에 하나만 가능
export default function Greeting() { ... }

// import 시 이름 자유롭게 변경 가능
import Greeting from './Greeting';       // 정상
import MyGreeting from './Greeting';    // 이것도 정상 (이름 변경)


// named export — 한 파일에 여러 개 가능
export function Greeting() { ... }
export function Farewell() { ... }

// import 시 반드시 원래 이름 사용 (별칭을 쓰려면 as 사용)
import { Greeting, Farewell } from './Greeting';
import { Greeting as Hello } from './Greeting';  // 별칭
```

Vite 템플릿은 기본적으로 `export default`를 사용합니다. 하나의 파일에 하나의 컴포넌트만 두는 것이 일반적인 패턴이므로 default export가 자연스럽습니다.

---

## 5. JSX 규칙 [실습 포인트] (10분)

JSX는 JavaScript 안에 HTML처럼 보이는 문법을 작성할 수 있게 해주는 **JavaScript의 문법 확장**입니다. 브라우저는 JSX를 직접 이해하지 못하므로, Vite와 TypeScript가 빌드 시 일반 JavaScript로 변환합니다.

HTML과 비슷해 보이지만, 몇 가지 중요한 차이점이 있습니다.

---

### 규칙 1: 하나의 루트 요소

컴포넌트는 반드시 **하나의 최상위 요소**를 반환해야 합니다.

```tsx
// 오류 — 두 개의 최상위 요소
function Wrong() {
  return (
    <h1>제목</h1>
    <p>본문</p>
  );
}

// 해결 1 — div로 감싸기
function Solution1() {
  return (
    <div>
      <h1>제목</h1>
      <p>본문</p>
    </div>
  );
}

// 해결 2 — Fragment 사용 (불필요한 div 없이)
function Solution2() {
  return (
    <>
      <h1>제목</h1>
      <p>본문</p>
    </>
  );
}

// 해결 2의 명시적 표현 (key prop이 필요할 때 사용)
import { Fragment } from 'react';

function Solution2Explicit() {
  return (
    <Fragment>
      <h1>제목</h1>
      <p>본문</p>
    </Fragment>
  );
}
```

`<>...</>` 는 `<Fragment>...</Fragment>`의 단축 표현입니다. 실제 DOM에 불필요한 wrapper 요소를 추가하지 않으므로 `<div>`로 감싸는 것보다 선호됩니다.

---

### 규칙 2: `className` 사용

HTML에서는 `class` 속성을 사용하지만, JSX에서는 `className`을 사용합니다.

```tsx
// HTML
// <div class="container">...</div>

// JSX — class가 아닌 className
function Card() {
  return (
    <div className="container">
      <p className="text-large">내용</p>
    </div>
  );
}
```

`class`가 JavaScript의 예약어(클래스 선언에 사용)이기 때문에 `className`으로 대체되었습니다. 마찬가지로 HTML의 `for` 속성은 JSX에서 `htmlFor`를 사용합니다.

```tsx
// HTML
// <label for="username">이름</label>

// JSX
function Form() {
  return <label htmlFor="username">이름</label>;
}
```

---

### 규칙 3: 중괄호 `{}`로 JavaScript 표현식 삽입

JSX 내에서 JavaScript 코드를 실행하거나 변수를 사용하려면 `{}`로 감쌉니다.

```tsx
function Profile() {
  const userName = '김철수';
  const userAge = 25;
  const isVerified = true;

  return (
    <div>
      {/* 변수 삽입 */}
      <h1>{userName}</h1>

      {/* 연산 */}
      <p>내년 나이: {userAge + 1}세</p>

      {/* 함수 호출 */}
      <p>이름 길이: {userName.length}글자</p>

      {/* 삼항 연산자 */}
      <span>{isVerified ? '인증됨' : '미인증'}</span>

      {/* 주석은 이렇게 씁니다 — JSX 내부에서는 {/* */} 형식 사용 */}
    </div>
  );
}
```

`{}`안에는 **표현식(expression)**만 올 수 있습니다. `if` 문, `for` 문 같은 **구문(statement)**은 직접 넣을 수 없습니다.

```tsx
// 오류 — if 문은 표현식이 아님
function Wrong() {
  return (
    <div>
      {if (true) { return <p>참</p>; }}  {/* 불가능 */}
    </div>
  );
}

// 올바른 방법 — 삼항 연산자 사용
function Correct() {
  const show = true;
  return (
    <div>
      {show ? <p>참</p> : <p>거짓</p>}
    </div>
  );
}
```

---

### 규칙 4: 조건부 렌더링

화면에 표시할지 여부를 조건에 따라 결정하는 패턴입니다.

```tsx
interface AlertProps {
  message: string;
  isVisible: boolean;
  type: 'info' | 'warning' | 'error';
}

function Alert({ message, isVisible, type }: AlertProps) {
  // 방법 1: 컴포넌트 밖에서 조건 처리 (if 문 사용 가능)
  if (!isVisible) {
    return null;  // null을 반환하면 아무것도 렌더링하지 않음
  }

  return (
    <div className={`alert alert-${type}`}>
      {/* 방법 2: && 연산자 — 왼쪽이 true일 때만 오른쪽 렌더링 */}
      {type === 'error' && <strong>오류: </strong>}

      {/* 방법 3: 삼항 연산자 */}
      {type === 'warning' ? <span>경고</span> : <span>알림</span>}

      <span>{message}</span>
    </div>
  );
}
```

**주의: `&&` 연산자와 숫자 0**

```tsx
// 버그 위험 — count가 0이면 "0"이 화면에 출력됨
function Counter({ count }: { count: number }) {
  return <div>{count && <p>{count}개 항목</p>}</div>;
}

// 올바른 방법 — boolean으로 명시적 변환
function Counter({ count }: { count: number }) {
  return <div>{count > 0 && <p>{count}개 항목</p>}</div>;
}
```

JavaScript의 `&&` 연산자는 왼쪽 값이 falsy이면 왼쪽 값을 그대로 반환합니다. `0`은 falsy이므로 `0`이 그대로 반환되어 화면에 "0"이 표시될 수 있습니다. `count > 0`으로 명시적으로 boolean을 만들면 이 문제를 피할 수 있습니다.

---

### 규칙 5: 리스트 렌더링과 `key` prop

배열 데이터를 화면에 목록으로 표시할 때는 `.map()` 메서드를 사용합니다.

```tsx
interface Student {
  id: number;
  name: string;
  grade: string;
}

const students: Student[] = [
  { id: 1, name: '김철수', grade: 'A' },
  { id: 2, name: '이영희', grade: 'B' },
  { id: 3, name: '박민준', grade: 'A' },
];

function StudentList() {
  return (
    <ul>
      {students.map((student) => (
        <li key={student.id}>
          {student.name} — {student.grade}
        </li>
      ))}
    </ul>
  );
}
```

**`key` prop이 왜 필요한가:**

React는 리스트를 효율적으로 업데이트하기 위해 각 항목을 추적해야 합니다. `key`는 React가 어떤 항목이 추가되었고, 변경되었으며, 삭제되었는지 파악하는 데 사용됩니다.

`key`의 규칙:

- 같은 리스트 내에서 **유일한 값**이어야 합니다 (전체 앱에서 유일할 필요는 없음)
- **배열 인덱스(`index`)를 key로 사용하는 것은 가급적 피합니다.** 항목이 추가/삭제/재정렬될 때 React가 잘못 추적할 수 있습니다
- 데이터베이스 ID처럼 **안정적이고 유일한 값**을 사용합니다

```tsx
// 나쁜 예 — 인덱스를 key로 사용 (항목 순서가 바뀔 수 있는 경우)
{students.map((student, index) => (
  <li key={index}>{student.name}</li>  // 피해야 함
))}

// 좋은 예 — 안정적인 ID를 key로 사용
{students.map((student) => (
  <li key={student.id}>{student.name}</li>
))}
```

> **강사 안내**: `key`를 빠뜨리면 브라우저 개발자 도구의 콘솔에 "Warning: Each child in a list should have a unique 'key' prop." 경고가 표시됩니다. 학생들이 직접 key를 제거하고 경고를 확인해보도록 안내합니다.

---

## 독립 실습 (10분)

> **강사 안내**: 학생들이 혼자 해결하는 시간입니다. 힌트는 요청 시에만 제공합니다. 10분 후 솔루션 코드를 함께 리뷰합니다.

### 과제: `ProductCard` 컴포넌트 만들기

`src/ProductCard.tsx` 파일을 새로 만들고, 다음 요구사항을 만족하는 컴포넌트를 작성합니다.

**요구사항:**

1. 다음 타입의 props를 받습니다
   - `name: string` — 상품 이름 (필수)
   - `price: number` — 가격 (필수)
   - `inStock: boolean` — 재고 여부 (필수)
   - `description?: string` — 상품 설명 (선택)

2. 화면에 다음을 표시합니다
   - 상품 이름 (`<h2>` 태그)
   - 가격 (`{price.toLocaleString()}원` 형식 — 천 단위 구분자 자동 추가)
   - `inStock`이 `true`면 "재고 있음", `false`면 "품절" 표시
   - `description`이 있으면 표시, 없으면 표시하지 않음

3. `App.tsx`에서 `ProductCard` 컴포넌트를 3개 이상 사용합니다

**힌트:**
- `{price.toLocaleString()}` 은 숫자를 `1,234,567` 형식으로 변환합니다
- 조건부 렌더링은 `&&` 연산자 또는 삼항 연산자를 사용합니다

**솔루션 코드 (10분 후 공개):**

```tsx
// src/ProductCard.tsx

interface ProductCardProps {
  name: string;
  price: number;
  inStock: boolean;
  description?: string;
}

function ProductCard({ name, price, inStock, description }: ProductCardProps) {
  return (
    <div>
      <h2>{name}</h2>
      <p>가격: {price.toLocaleString()}원</p>
      <p>{inStock ? '재고 있음' : '품절'}</p>
      {description && <p>{description}</p>}
    </div>
  );
}

export default ProductCard;
```

```tsx
// src/App.tsx

import ProductCard from './ProductCard';

function App() {
  return (
    <div>
      <ProductCard
        name="TypeScript 핵심 가이드"
        price={28000}
        inStock={true}
        description="TypeScript를 처음 배우는 개발자를 위한 책"
      />
      <ProductCard
        name="React 완전 정복"
        price={35000}
        inStock={false}
      />
      <ProductCard
        name="Node.js 백엔드 개발"
        price={32000}
        inStock={true}
      />
    </div>
  );
}

export default App;
```

---

## 트러블슈팅 & 자주 하는 실수

### 오류 1: `npm create vite@latest` 실행 시 아무 것도 안 됨

**증상:** 명령어 입력 후 오랫동안 반응이 없음

**원인:** npm 캐시 문제 또는 네트워크 연결 문제

**해결:**
```bash
# npm 캐시 정리 후 재시도
npm cache clean --force
npm create vite@latest my-react-app -- --template react-ts
```

---

### 오류 2: `'vite' is not recognized as an internal or external command`

**증상:** `npm run dev` 실행 시 위 오류 발생

**원인:** `npm install`을 실행하지 않았거나, 올바른 프로젝트 폴더 안에 있지 않음

**해결:**
```bash
# 현재 위치 확인
pwd

# 올바른 폴더로 이동
cd my-react-app

# 의존성 설치
npm install

# 다시 실행
npm run dev
```

---

### 오류 3: `JSX element type does not have any construct or call signatures`

**증상:** 컴포넌트를 JSX로 사용할 때 TypeScript 오류

**원인:** 컴포넌트 함수 이름이 소문자로 시작함

```tsx
// 오류 유발 코드
function greeting() {  // 소문자 g
  return <p>안녕하세요</p>;
}

// <greeting /> 으로 사용하면 HTML 태그로 인식되어 오류 발생
```

**해결:** 함수 이름을 대문자로 시작하도록 변경합니다.

```tsx
function Greeting() {  // 대문자 G
  return <p>안녕하세요</p>;
}
```

---

### 오류 4: `Property 'name' does not exist on type 'GreetingProps'`

**증상:** props를 사용할 때 TypeScript 오류

**원인:** `interface`에 없는 prop을 사용하거나, 오타가 있음

**해결:** `interface` 정의와 실제 사용하는 prop 이름을 일치시킵니다.

```tsx
// 오류
interface GreetingProps {
  userName: string;  // userName
}
function Greeting({ name }: GreetingProps) {  // name — 불일치!
```

```tsx
// 해결
interface GreetingProps {
  name: string;
}
function Greeting({ name }: GreetingProps) {
```

---

### 오류 5: `Argument of type 'string | null' is not assignable to parameter of type 'Element'`

**증상:** `main.tsx`에서 `createRoot` 사용 시 오류

**원인:** `document.getElementById('root')`의 반환 타입이 `HTMLElement | null`인데, `createRoot`는 `null`을 받지 않음

**해결:** Non-null Assertion Operator(`!`)를 사용합니다.

```tsx
// 오류
ReactDOM.createRoot(document.getElementById('root')).render(...)

// 해결
ReactDOM.createRoot(document.getElementById('root')!).render(...)
```

또는 조건부 처리를 선호하는 경우:

```tsx
const rootElement = document.getElementById('root');
if (!rootElement) throw new Error('root element를 찾을 수 없습니다');
ReactDOM.createRoot(rootElement).render(...)
```

---

### 오류 6: Adjacent JSX elements must be wrapped in an enclosing tag

**증상:** 컴포넌트가 두 개 이상의 최상위 요소를 반환할 때 오류

**해결:** Fragment(`<>...</>`)나 div로 감쌉니다.

```tsx
// 오류
return (
  <h1>제목</h1>
  <p>내용</p>
);

// 해결
return (
  <>
    <h1>제목</h1>
    <p>내용</p>
  </>
);
```

---

### 오류 7: 화면에 아무것도 표시되지 않음 (흰 화면)

**증상:** 브라우저에서 `http://localhost:5173`에 접속하면 흰 화면만 보임

**확인 순서:**
1. 터미널에서 `npm run dev`가 실행 중인지 확인합니다
2. 브라우저 개발자 도구(F12) → Console 탭에서 오류 메시지를 확인합니다
3. `index.html`의 `<div id="root">`가 존재하는지 확인합니다
4. `main.tsx`의 `document.getElementById('root')`에서 `'root'`가 정확한지 확인합니다

---

### 오류 8: 콘솔에 `Warning: Each child in a list should have a unique "key" prop`

**증상:** 브라우저 콘솔에 경고 메시지 출력

**원인:** `.map()`으로 생성한 리스트 요소에 `key` prop이 없거나 중복됨

**해결:** 각 요소에 유일한 `key` prop을 추가합니다.

```tsx
// 경고 발생
{items.map((item) => (
  <li>{item.name}</li>
))}

// 해결
{items.map((item) => (
  <li key={item.id}>{item.name}</li>
))}
```

---

### 오류 9: 파일 저장 후 브라우저가 자동 갱신되지 않음

**증상:** 코드를 수정하고 저장해도 브라우저 화면이 바뀌지 않음

**확인 순서:**
1. 터미널에서 `npm run dev`가 아직 실행 중인지 확인합니다 (Ctrl+C로 종료되었을 수 있음)
2. 브라우저 주소가 `http://localhost:5173`이 맞는지 확인합니다 (다른 포트일 수 있음)
3. VS Code에서 파일이 실제로 저장되었는지 확인합니다 (탭 제목에 점(●)이 있으면 미저장 상태)
4. 브라우저에서 `Ctrl+Shift+R`로 강제 새로고침을 시도합니다

---

### 오류 10: `Cannot find module './Greeting' or its corresponding type declarations`

**증상:** 컴포넌트 import 시 TypeScript 오류

**원인:** 파일 이름 오타, 대소문자 불일치, 또는 파일이 존재하지 않음

**해결:**
1. 파일이 올바른 위치에 있는지 확인합니다 (`src/Greeting.tsx`)
2. import 경로의 대소문자가 정확한지 확인합니다 (파일 시스템은 대소문자를 구분할 수 있음)
3. 파일 확장자가 `.tsx`가 맞는지 확인합니다

```tsx
// import 경로 확인
import Greeting from './Greeting';    // src/Greeting.tsx가 있어야 함
import Greeting from './greeting';    // src/greeting.tsx — 대소문자 불일치 가능
```

---

### 오류 11: JSX 내에서 `/* 주석 */` 이 화면에 텍스트로 출력됨

**증상:** 코드에 작성한 주석이 그대로 화면에 표시됨

**원인:** JSX 내부에서 일반 JavaScript 주석 형식을 사용함

**해결:** JSX 내부 주석은 `{/* */}` 형식을 사용합니다.

```tsx
// 오류 — 주석이 텍스트로 렌더링될 수 있음
return (
  <div>
    // 이것은 주석입니다 — JSX 내에서는 텍스트로 렌더링됨
    <p>내용</p>
  </div>
);

// 해결
return (
  <div>
    {/* 이것이 올바른 JSX 주석 형식입니다 */}
    <p>내용</p>
  </div>
);
```

---

## Q&A 예상 질문과 답변

**Q1. React와 Angular, Vue는 어떻게 다른가요?**

A: 세 가지 모두 현대적인 프론트엔드 UI 개발에 사용됩니다. Angular는 Google이 만든 완전한 프레임워크로, 라우팅, 폼 처리, HTTP 클라이언트 등이 모두 내장되어 있습니다. 학습 곡선이 가장 가파릅니다. Vue는 React와 Angular의 중간 정도로, 진입 장벽이 낮고 공식 문서가 훌륭합니다. React는 UI 라이브러리이므로 다른 라이브러리와 자유롭게 조합할 수 있고, 가장 넓은 생태계와 커뮤니티를 가지고 있습니다. 국내외 취업 시장에서 React 수요가 가장 높습니다.

**Q2. `.tsx` 파일과 `.ts` 파일의 차이는 무엇인가요?**

A: `.ts`는 순수 TypeScript 파일이고, `.tsx`는 JSX 문법을 포함할 수 있는 TypeScript 파일입니다. React 컴포넌트는 JSX를 반환하므로 `.tsx`를 사용합니다. 유틸리티 함수, 타입 정의 등 JSX가 없는 파일은 `.ts`를 사용합니다.

**Q3. `node_modules/` 폴더를 왜 git에 포함하지 않나요?**

A: `node_modules/`는 크기가 수백 MB에 달할 수 있고, `package.json`과 `package-lock.json`만 있으면 `npm install`로 언제든지 재생성할 수 있습니다. `.gitignore` 파일에 `node_modules`가 자동으로 추가되어 있습니다. 다른 사람이 저장소를 clone하면 `npm install`을 실행하면 됩니다.

**Q4. `React.StrictMode`를 사용하면 컴포넌트가 두 번 렌더링된다고 했는데, 성능에 문제가 없나요?**

A: 개발 환경에서만 두 번 렌더링됩니다. `npm run build`로 프로덕션 빌드를 생성하면 `StrictMode`의 이중 렌더링이 비활성화됩니다. 개발 중 `console.log`가 두 번 찍히는 것도 이 때문입니다.

**Q5. `export default`와 `named export` 중 어느 것을 사용해야 하나요?**

A: 컴포넌트 파일에는 `export default`를 사용하는 것이 일반적인 관행입니다. 여러 유틸리티 함수나 상수를 한 파일에서 내보낼 때는 `named export`를 사용합니다. 프로젝트 팀의 컨벤션을 따르는 것이 가장 중요합니다.

**Q6. JSX를 쓰면 HTML이 JavaScript 파일 안에 섞이는 것 아닌가요? 이상하지 않나요?**

A: 처음에는 어색해 보일 수 있습니다. 전통적인 웹 개발에서는 HTML, CSS, JavaScript를 분리했습니다. React는 이 원칙에 의문을 제기합니다. "로직과 뷰가 같은 컴포넌트에 있어야 실제로 관련된 것들이 함께 관리된다"는 철학입니다. 경험상 컴포넌트 단위로 코드가 모여 있으면 수정이 필요할 때 찾기가 훨씬 쉽습니다.

**Q7. TypeScript를 쓰면 코드가 많아지고 복잡해지지 않나요?**

A: 초기에는 타입 정의 코드가 추가되어 코드가 조금 더 길어집니다. 그러나 VS Code의 자동 완성과 타입 오류 즉시 감지 기능 덕분에 실제로 개발 속도가 빨라집니다. 특히 팀 프로젝트나 대규모 코드베이스에서 TypeScript의 효과가 크게 나타납니다. "지금은 조금 더 타이핑하고, 나중에 디버깅 시간을 절약한다"고 이해하면 됩니다.

**Q8. `http://localhost:5173`에서 5173은 무엇인가요? 바꿀 수 있나요?**

A: 5173은 Vite 개발 서버가 사용하는 기본 포트 번호입니다. 변경하려면 `vite.config.ts`에 다음을 추가합니다.

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,  // 원하는 포트 번호
  },
})
```

**Q9. 컴포넌트 함수에서 `return` 없이 JSX를 화살표 함수로 반환할 수 있나요?**

A: 네, 가능합니다. 함수 선언식과 화살표 함수 표현식 두 가지 방식 모두 유효합니다.

```tsx
// 함수 선언식 (function declaration) — 이 수업에서 기본으로 사용
function Greeting({ name }: { name: string }) {
  return <h1>안녕하세요, {name}님!</h1>;
}

// 화살표 함수 표현식
const Greeting = ({ name }: { name: string }) => (
  <h1>안녕하세요, {name}님!</h1>
);

// 화살표 함수, 중괄호 사용 (여러 줄이 필요할 때)
const Greeting = ({ name }: { name: string }) => {
  return <h1>안녕하세요, {name}님!</h1>;
};
```

현업에서는 두 방식이 모두 사용됩니다. 팀 컨벤션에 따르면 됩니다.

**Q10. `interface` 대신 `type`을 사용해도 되나요?**

A: 대부분의 경우 `interface`와 `type`은 같은 역할을 합니다. Props 타입 정의에는 둘 다 사용됩니다.

```tsx
// interface 사용
interface GreetingProps {
  name: string;
}

// type 사용 (동일한 결과)
type GreetingProps = {
  name: string;
};
```

주요 차이점은 `interface`는 선언 병합(declaration merging)이 가능하고, `type`은 유니온 타입(`type Result = Success | Error`)처럼 더 복잡한 타입 구성이 가능합니다. React 컴포넌트 Props 정의에는 일반적으로 `interface`가 많이 사용되지만, 프로젝트 내에서 일관성을 유지하는 것이 더 중요합니다.

**Q11. Vite와 webpack의 차이는 무엇인가요?**

A: webpack은 오래되고 강력한 번들러로, Create React App이 내부적으로 사용합니다. 모든 파일을 처음부터 번들링하기 때문에 프로젝트가 커질수록 개발 서버 시작 시간이 길어집니다. Vite는 개발 시에는 번들링 없이 네이티브 ES Module을 직접 서빙하여 서버 시작이 매우 빠릅니다. 변경 파일만 처리하므로 HMR도 빠릅니다. 배포 빌드 시에는 rollup을 사용하여 최적화된 번들을 생성합니다.

---

## 핵심 요약

### React 핵심 개념

| 개념 | 핵심 내용 |
|------|-----------|
| 컴포넌트 | JSX를 반환하는 TypeScript 함수. 이름은 대문자로 시작 |
| Props | 부모 → 자식 컴포넌트로 데이터를 전달하는 방법. TypeScript `interface`로 타입 정의 |
| JSX | JavaScript 안에서 HTML처럼 보이는 문법. 빌드 시 JavaScript로 변환됨 |
| 선언적 UI | 상태를 정의하면 React가 DOM 업데이트를 담당. Vanilla JS의 명령적 방식과 대조 |

### JSX 규칙 5가지

1. **하나의 루트 요소** — Fragment `<>...</>`로 감싸기
2. **`className`** — HTML `class` 대신 사용
3. **`{}` 중괄호** — JavaScript 표현식 삽입
4. **조건부 렌더링** — `&&` 또는 삼항 연산자
5. **리스트 `key` prop** — `.map()` 사용 시 유일한 `key` 필수

### 오늘 만든 파일

```
src/
├── main.tsx      # React 앱 진입점. createRoot + StrictMode
├── App.tsx       # 루트 컴포넌트. 수정하여 사용
├── Greeting.tsx  # 첫 번째 커스텀 컴포넌트
└── ProductCard.tsx  # 독립 실습 컴포넌트
```

### 다음 세션 예고

다음 세션에서는 React의 핵심인 **useState 훅**을 배웁니다.

- `useState`로 컴포넌트 내부 상태 관리
- 버튼 클릭, 입력 폼 처리
- 상태 변경에 따른 UI 자동 업데이트

---

## 참고 자료

- [React 공식 문서 (한국어)](https://ko.react.dev) — React 팀이 직접 작성한 공식 튜토리얼
- [Vite 공식 문서](https://vitejs.dev/guide/) — Vite 설정 및 플러그인 안내
- [TypeScript 공식 문서](https://www.typescriptlang.org/docs/) — TypeScript 언어 레퍼런스
- [VS Code React/TypeScript 확장](https://marketplace.visualstudio.com/items?itemName=dsznajder.es7-react-js-snippets) — 컴포넌트 스니펫 도구
