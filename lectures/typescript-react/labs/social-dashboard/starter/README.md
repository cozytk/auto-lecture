# Mini Social Dashboard — Starter Template

JSONPlaceholder API의 6개 리소스를 활용한 소셜 대시보드를 만듭니다.
**CSS는 이미 완성되어 있으니, React 로직에만 집중하세요!**

## 프로젝트 셋업

```bash
# 1. Vite + React 프로젝트 생성
npm create vite@latest social-dashboard -- --template react
cd social-dashboard

# 2. Tailwind CSS 설치
npm install -D tailwindcss @tailwindcss/vite

# 3. vite.config.js 수정
```

**vite.config.js** 를 아래처럼 수정하세요:

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

**src/index.css** 를 아래 한 줄로 교체하세요:

```css
@import "tailwindcss";
```

```bash
# 4. 스타터 파일 복사
# components/ 폴더의 파일들을 src/components/에 복사하세요

# 5. 실행
npm run dev
```

## API 정보

- Base URL: `https://jsonplaceholder.typicode.com`
- 리소스: `/users`, `/posts`, `/comments`, `/albums`, `/photos`, `/todos`
- 관계: `GET /posts?userId=1`, `GET /posts/1/comments`, `GET /albums/1/photos`
- 모든 HTTP 메서드 지원 (GET, POST, PUT, PATCH, DELETE)
- ⚠️ 실제 DB에 저장되지 않습니다 — **로컬 state 관리가 핵심!**

## 파일 구조

```
src/
├── App.jsx                  ← 메인 레이아웃 (시작점)
├── components/
│   ├── ui/
│   │   ├── StatCard.jsx     ← 통계 카드 (도전)
│   │   ├── Skeleton.jsx     ← 로딩 스켈레톤 (도전)
│   │   └── TabButton.jsx    ← 탭 버튼
│   ├── UserCard.jsx         ← 사용자 카드
│   ├── SearchBar.jsx        ← 검색바 (도전)
│   ├── PostForm.jsx         ← 게시글 작성 폼
│   ├── PostCard.jsx         ← 게시글 카드
│   ├── CommentList.jsx      ← 댓글 목록
│   ├── TodoSection.jsx      ← 할 일 관리
│   └── AlbumGallery.jsx     ← 포토 갤러리 (도전)
└── index.css
```

## 과제 구성

### ✅ 필수 구현사항 (Basic)

| # | 기능 | 핵심 학습 | 파일 |
|---|------|----------|------|
| 1 | 사용자 목록 불러오기 | `useEffect`, `fetch`, `useState` | `App.jsx` |
| 2 | 사용자별 게시글 표시 | 조건부 fetch, props 전달 | `App.jsx`, `PostCard.jsx` |
| 3 | 게시글 작성 (POST) | 폼 핸들링, POST 요청, state 업데이트 | `PostForm.jsx` |
| 4 | 게시글 삭제 (DELETE) | 이벤트 핸들링, DELETE 요청, 배열 필터 | `PostCard.jsx` |
| 5 | 완료 토글 (PATCH) | 상태 토글, PATCH 요청 | `TodoSection.jsx` |
| 6 | 댓글 펼치기/접기 | 조건부 렌더링, 중첩 fetch | `CommentList.jsx` |

### 🚀 도전 구현사항 (Challenge)

| # | 기능 | 핵심 학습 | 파일 |
|---|------|----------|------|
| 7 | 로딩 스켈레톤 UI | 로딩 상태 관리 | `Skeleton.jsx` |
| 8 | 대시보드 통계 | `Promise.all`, 데이터 집계 | `App.jsx`, `StatCard.jsx` |
| 9 | 게시글 검색 | `useMemo`, 파생 상태 | `SearchBar.jsx` |
| 10 | 포토 갤러리 | 중첩 리소스, 모달 | `AlbumGallery.jsx` |

## 진행 팁

1. **`// TODO` 주석을 찾으세요** — 구현해야 할 부분이 표시되어 있습니다
2. **필수부터 순서대로** — 번호 순서가 곧 구현 순서입니다
3. **`console.log`를 적극 활용하세요** — API 응답 구조를 먼저 확인!
4. **JSONPlaceholder는 fake API입니다** — POST/DELETE해도 서버에 반영 안 됩니다. 로컬 state를 업데이트하세요.
