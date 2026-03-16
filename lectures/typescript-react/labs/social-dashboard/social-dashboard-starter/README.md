# Mini Social Dashboard — Starter Template (TypeScript)

JSONPlaceholder API의 6개 리소스를 활용한 소셜 대시보드를 만듭니다.
**CSS는 이미 완성되어 있으니, React + TypeScript 로직에만 집중하세요!**

---

## 프로젝트 셋업

### Step 1. Vite 프로젝트 생성

```bash
npm create vite@latest social-dashboard -- --template react-ts
cd social-dashboard
```

생성된 파일 구조를 확인하세요:

```
social-dashboard/
├── node_modules/
├── public/
├── src/
│   ├── App.tsx          ← 이 파일들을 우리 스타터로 교체할 겁니다
│   ├── main.tsx
│   └── ...
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### Step 2. Tailwind CSS v4 설치

```bash
npm install -D tailwindcss @tailwindcss/vite
```

### Step 3. Vite에 Tailwind 플러그인 추가

`vite.config.ts`를 열고 아래처럼 수정하세요:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

### Step 4. CSS 파일 교체

`src/index.css` 파일 내용을 **전부 지우고** 아래 한 줄로 교체하세요:

```css
@import "tailwindcss";
```

`src/App.css`는 삭제해도 됩니다 (사용하지 않습니다).

### Step 5. Tailwind 동작 확인

```bash
npm run dev
```

브라우저에서 http://localhost:5173 에 접속합니다.
`src/App.tsx`를 아래로 바꿔서 Tailwind가 적용되는지 확인하세요:

```tsx
export default function App() {
  return (
    <h1 className="text-3xl font-bold text-blue-600 p-8">
      Tailwind 동작 확인!
    </h1>
  );
}
```

파란색 큰 글씨가 보이면 셋업 완료!

### Step 6. 스타터 코드 복사

이 폴더의 `src/` 안에 있는 파일들을 프로젝트의 `src/`에 **덮어씌우세요**:

```bash
# starter 폴더 위치에서 실행
cp -r src/* /path/to/social-dashboard/src/
```

> `App.tsx`, `main.tsx` 등 기존 파일은 덮어써도 됩니다.
> Vite가 자동으로 생성한 `App.css`, `assets/` 등은 삭제해도 OK.

### Step 7. 실행

```bash
npm run dev
```

헤더와 빈 카드 레이아웃이 보이면 과제를 시작할 준비가 된 겁니다!

---

## API 정보

| 리소스 | 엔드포인트 | 개수 |
|--------|-----------|------|
| Users | `/users` | 10명 |
| Posts | `/posts` | 100개 |
| Comments | `/comments` | 500개 |
| Albums | `/albums` | 100개 |
| Photos | `/photos` | 5000개 |
| Todos | `/todos` | 200개 |

- Base URL: `https://jsonplaceholder.typicode.com`
- 관계: `GET /posts?userId=1`, `GET /posts/1/comments`, `GET /albums/1/photos`
- 모든 HTTP 메서드 지원 (GET, POST, PUT, PATCH, DELETE)
- ⚠️ 실제 DB에 저장되지 않습니다 — **로컬 state 관리가 핵심!**

### 리소스 관계도

```
User (10명)
 ├── Posts (userId)       → 각 유저당 10개
 │    └── Comments (postId)  → 각 포스트당 5개
 ├── Albums (userId)      → 각 유저당 10개
 │    └── Photos (albumId)   → 각 앨범당 50개
 └── Todos (userId)       → 각 유저당 20개
```

---

## 파일 구조

```
src/
├── types.ts                     ← 공유 타입 정의 (수정 불필요)
├── App.tsx                      ← ⭐ 시작점 (TODO 다수)
├── main.tsx                     ← React 엔트리 (수정 불필요)
├── index.css                    ← Tailwind import (수정 불필요)
└── components/
    ├── ui/                      ← 수정 불필요, 그대로 사용
    │   ├── StatCard.tsx
    │   ├── Skeleton.tsx
    │   └── TabButton.tsx
    ├── UserCard.tsx             ← 수정 불필요, 그대로 사용
    ├── SearchBar.tsx            ← 수정 불필요, 그대로 사용
    ├── PostForm.tsx             ← ⭐ TODO 있음
    ├── PostCard.tsx             ← ⭐ TODO 있음
    ├── CommentList.tsx          ← ⭐ TODO 있음
    ├── TodoSection.tsx          ← ⭐ TODO 있음
    └── AlbumGallery.tsx         ← ⭐ TODO 있음
```

---

## 타입 안내

`src/types.ts`에 모든 타입이 정의되어 있습니다. fetch 후 이렇게 사용하세요:

```typescript
import type { User } from "./types";

const res = await fetch(`${API}/users`);
const data: User[] = await res.json();
```

| 타입 | 용도 |
|------|------|
| `User`, `Post`, `Comment`, `Todo`, `Album`, `Photo` | API 응답 |
| `DashboardStats` | 대시보드 통계 객체 |
| `StatsUpdateFn` | 통계 갱신 콜백 타입 (도전 11) |

---

## 과제 구성

### ✅ 필수 구현사항 (Basic)

| # | 기능 | 핵심 학습 | 파일 |
|---|------|----------|------|
| 1 | 사용자 목록 불러오기 | `useEffect`, `fetch`, `useState<User[]>` | `App.tsx` |
| 2 | 사용자별 게시글 표시 | 조건부 fetch, props 전달 | `App.tsx`, `PostCard.tsx` |
| 3 | 게시글 작성 (POST) | 폼 핸들링, POST 요청, state 업데이트 | `PostForm.tsx` |
| 4 | 게시글 삭제 (DELETE) | 이벤트 핸들링, DELETE 요청, 배열 필터 | `PostCard.tsx` |
| 5 | 할 일 토글 (PATCH) | 상태 토글, PATCH 요청 | `TodoSection.tsx` |
| 6 | 댓글 펼치기/접기 | 조건부 렌더링, 중첩 fetch | `CommentList.tsx` |

### 🚀 도전 구현사항 (Challenge)

| # | 기능 | 핵심 학습 | 파일 |
|---|------|----------|------|
| 7 | 로딩 스켈레톤 UI | 로딩 상태 관리 | `Skeleton.tsx` (이미 제공) |
| 8 | 대시보드 통계 | `Promise.all`, 데이터 집계 | `App.tsx` |
| 9 | 게시글 검색 | `useMemo`, 파생 상태 | `App.tsx` |
| 10 | 포토 갤러리 | 중첩 리소스, 모달 | `AlbumGallery.tsx` |
| 11 | **콜백으로 통계 실시간 갱신** | 콜백 패턴, 부모↔자식 통신 | `App.tsx`, `TodoSection.tsx` |

---

### 도전 11 상세: 콜백으로 Stats 갱신

도전 8에서 `Promise.all`로 초기 통계를 불러오면, 이후 CRUD 작업 시 통계 숫자가 안 맞게 됩니다.
**콜백 패턴으로 자식 컴포넌트가 부모의 stats를 실시간 갱신하도록 만드세요.**

**구현 흐름:**

```
1. App.tsx — handleStatsUpdate 함수 정의 (타입: StatsUpdateFn)
2. App.tsx → TodoSection — onStatsUpdate prop으로 전달
3. TodoSection — 완료 토글 시 onStatsUpdate("todoDone", prev => prev + 1) 호출
4. App.tsx — addPost / deletePost에서도 handleStatsUpdate("posts", prev => prev ± 1)
```

**완성되면:** 게시글 추가/삭제, 할 일 토글 시 상단 통계 카드 숫자가 실시간 반영됩니다.

---

## 진행 팁

1. **`// TODO` 주석을 찾으세요** — `grep -rn "TODO" src/` 로 한번에 확인 가능
2. **필수부터 순서대로** — 번호 순서가 곧 구현 순서입니다
3. **`console.log`를 적극 활용하세요** — API 응답 구조를 먼저 확인!
4. **타입 에러를 무시하지 마세요** — 빨간 줄이 뜨면 타입이 잘못된 겁니다
5. **JSONPlaceholder는 fake API입니다** — POST/DELETE해도 서버에 반영 안 됩니다. 로컬 state를 업데이트하세요.

---

## 정답 코드

`solutions/` 폴더에 TODO가 있는 파일들의 정답이 있습니다. **먼저 직접 해보세요!**

```
solutions/
├── App.tsx              ← 필수 1~4, 도전 8·9·11
├── PostForm.tsx         ← 필수 3
├── PostCard.tsx         ← 필수 4
├── CommentList.tsx      ← 필수 6
├── TodoSection.tsx      ← 필수 5, 도전 11
└── AlbumGallery.tsx     ← 도전 10
```

스타터 코드와 나란히 비교하며 보세요:

```bash
# 예: App.tsx 비교
diff src/App.tsx solutions/App.tsx
```

---

## 평가 기준

- **필수 6개 완료** → 통과 (CRUD + 관계형 데이터 fetch)
- **필수 + 도전 1~2개** → 우수 (비동기 최적화, UI 패턴)
- **필수 + 도전 3개 이상** → 최우수 (실무 수준 설계)
