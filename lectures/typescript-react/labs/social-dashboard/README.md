# Social Dashboard 종합 실습

**시간**: 2시간 (15:00 - 17:00) | **유형**: I DO 시연 + YOU DO 독립 실습

---

## 실습 개요

JSONPlaceholder API를 활용하여 소셜 대시보드를 구현합니다. Session 1~4에서 배운 TypeScript 타입 정의, React 컴포넌트, useState, 이벤트 핸들링, 상태 끌어올리기, 콜백 Props 패턴을 모두 활용하는 종합 실습입니다.

**CSS는 이미 완성되어 있습니다.** React + TypeScript 로직에만 집중하세요.

### 실습 진행 방식

| 단계 | 시간 | 내용 |
|------|------|------|
| **I DO** (강사 시연) | 30분 | Task 1 — 사용자 목록 불러오기 |
| **YOU DO** (독립 실습) | 90분 | Task 2~6 필수 + Task 7~11 도전 |

---

## 사전 준비

### 프로젝트 셋업

> 상세 셋업 가이드는 `social-dashboard-starter/README.md`를 참조하세요.

```bash
# 1. Vite 프로젝트 생성
npm create vite@latest social-dashboard -- --template react-ts
cd social-dashboard

# 2. Tailwind CSS v4 설치
npm install -D tailwindcss @tailwindcss/vite

# 3. vite.config.ts에 tailwindcss 플러그인 추가 (README 참조)

# 4. src/index.css를 @import "tailwindcss"; 한 줄로 교체

# 5. 스타터 코드 복사
cp -r /path/to/social-dashboard-starter/src/* src/

# 6. 실행
npm run dev
```

헤더와 빈 카드 레이아웃이 보이면 준비 완료입니다.

### 코드 배포 방법

강사는 다음 중 하나의 방법으로 스타터 코드를 배포합니다.

- **방법 1 (권장)**: git clone 또는 zip 파일 다운로드
- **방법 2 (오프라인)**: USB 드라이브로 배포 (`node_modules` 포함 zip)
- **방법 3 (온라인)**: 공유 드라이브 링크

---

## API 정보 요약

| 리소스 | 엔드포인트 | 개수 | 관계 |
|--------|-----------|------|------|
| Users | `/users` | 10명 | — |
| Posts | `/posts?userId={id}` | 유저당 10개 | User → Posts |
| Comments | `/posts/{id}/comments` | 포스트당 5개 | Post → Comments |
| Todos | `/todos?userId={id}` | 유저당 20개 | User → Todos |
| Albums | `/albums?userId={id}` | 유저당 10개 | User → Albums |
| Photos | `/albums/{id}/photos` | 앨범당 50개 | Album → Photos |

**Base URL**: `https://jsonplaceholder.typicode.com`

> **중요**: POST, DELETE, PATCH 요청은 서버에 실제로 저장되지 않습니다. 반드시 로컬 state를 직접 업데이트해야 합니다.

---

## I DO: Task 1 — 사용자 목록 불러오기 (강사 시연, 30분)

> **강사 안내**: 이 섹션은 학생들 앞에서 코드를 입력하며 시연합니다. 각 단계에서 무엇을 하는지, 왜 이렇게 하는지를 설명하면서 진행합니다. 학생들은 관찰하며 이해하는 시간입니다.

### 시연 전 준비

1. VS Code에서 `src/App.tsx` 파일을 엽니다
2. 브라우저에서 `http://localhost:5173`을 엽니다
3. 터미널에서 `npm run dev`가 실행 중인지 확인합니다

### Step 1: useState로 상태 선언하기 (5분)

**설명할 내용**: "먼저 사용자 데이터를 저장할 상태(state)를 만들어야 합니다. Session 4에서 배운 useState를 TypeScript 제네릭과 함께 사용합니다."

`App.tsx`의 상단 State 선언 영역에서 TODO 주석을 찾아 다음 코드를 입력합니다.

```tsx
// TODO (필수 1-a) 주석을 찾아 아래 코드로 교체합니다
const [users, setUsers] = useState<User[]>([]);
```

**코드 설명**:
- `useState<User[]>([])` — User 타입 배열을 상태로 관리합니다. 초기값은 빈 배열 `[]`입니다
- `User[]`는 `types.ts`에 정의된 User 인터페이스의 배열입니다
- `users`는 현재 상태값, `setUsers`는 상태를 변경하는 함수입니다

```tsx
// TODO (필수 1-b) 주석을 찾아 아래 코드로 교체합니다
const [selectedUser, setSelectedUser] = useState<User | null>(null);
```

**코드 설명**:
- `User | null` — 선택된 사용자가 없을 수 있으므로 Union 타입을 사용합니다
- 초기값 `null`은 "아직 아무 사용자도 선택하지 않은 상태"를 의미합니다
- Session 1에서 배운 Union 타입이 여기서 실제로 쓰입니다

**중요**: 파일 하단에 있는 임시 변수 2줄을 삭제해야 합니다.

```tsx
// 이 두 줄을 삭제합니다 (State를 만들었으므로 더 이상 필요 없습니다)
const users: User[] = [];                    // ← 삭제
const selectedUser: User | null = null;      // ← 삭제
```

> **강사 안내**: 임시 변수를 삭제하지 않으면 "변수가 이미 선언되었습니다" 오류가 발생합니다. 학생들에게 왜 이 변수가 있었는지(TODO 구현 전 타입 에러 방지용) 설명합니다.

### Step 2: useEffect로 API 호출하기 (10분)

**설명할 내용**: "이제 컴포넌트가 화면에 나타날 때(마운트될 때) API에서 사용자 목록을 가져와야 합니다. React에서 이런 부수 효과(side effect)를 처리하는 훅이 `useEffect`입니다."

`App.tsx`에서 `TODO (필수 1-c)` 주석이 있는 useEffect를 찾아 다음과 같이 수정합니다.

```tsx
// TODO (필수 1-c) — useEffect 내부를 다음으로 교체합니다
useEffect(() => {
  const fetchUsers = async () => {
    const res = await fetch(`${API}/users`);
    const data: User[] = await res.json();
    setUsers(data);
    setLoading(false);
  };
  fetchUsers();
}, []);
```

**코드 한 줄씩 설명**:

1. **`useEffect(() => { ... }, [])`**
   - useEffect는 두 개의 인자를 받습니다: 실행할 함수와 의존성 배열
   - 빈 배열 `[]`은 "컴포넌트가 처음 마운트될 때 딱 한 번만 실행"을 의미합니다
   - 이것은 Java의 `@PostConstruct`나 Python의 `__init__`과 비슷한 역할입니다

2. **`const fetchUsers = async () => { ... }`**
   - useEffect 콜백 안에서 직접 async를 쓸 수 없습니다 (React 규칙)
   - 그래서 내부에 async 함수를 별도로 정의하고 바로 호출합니다
   - 이것은 React에서 매우 흔한 패턴입니다

3. **`const res = await fetch(\`${API}/users\`)`**
   - 브라우저 내장 `fetch` API로 HTTP GET 요청을 보냅니다
   - `API`는 상단에 `"https://jsonplaceholder.typicode.com"`으로 정의되어 있습니다
   - 템플릿 리터럴(백틱)을 사용하여 URL을 조합합니다

4. **`const data: User[] = await res.json()`**
   - 응답 본문을 JSON으로 파싱합니다
   - `User[]` 타입을 명시하여 TypeScript에게 데이터 구조를 알려줍니다
   - 이제 `data[0].name`, `data[0].email` 등에 타입 안전하게 접근할 수 있습니다

5. **`setUsers(data)`**
   - 가져온 데이터로 users 상태를 업데이트합니다
   - React가 자동으로 UI를 다시 렌더링합니다

6. **`setLoading(false)`**
   - 로딩이 완료되었음을 표시합니다. 스켈레톤 UI가 사라지고 실제 데이터가 표시됩니다

> **강사 안내**: 파일을 저장한 뒤 브라우저를 확인합니다. 아직 UserCard를 렌더링하지 않았으므로 화면에 변화가 없습니다. 브라우저 개발자 도구(F12) → Network 탭에서 `/users` 요청이 성공(200)했는지 확인하여 보여줍니다.

### Step 3: 사용자 목록 렌더링하기 (10분)

**설명할 내용**: "데이터를 가져왔으니 이제 화면에 표시해야 합니다. Session 4에서 배운 `.map()`으로 리스트를 렌더링합니다."

`App.tsx`에서 `TODO (필수 1-d)` 주석이 있는 부분을 찾습니다. 기존 placeholder를 삭제하고 다음 코드로 교체합니다.

```tsx
{/* TODO (필수 1-d) 주석 아래의 기존 코드를 삭제하고 다음으로 교체합니다 */}
{users.map((user) => (
  <UserCard
    key={user.id}
    user={user}
    selected={selectedUser?.id === user.id}
    onClick={setSelectedUser}
  />
))}
```

**코드 설명**:

1. **`users.map((user) => (...))`**
   - `users` 배열의 각 요소를 UserCard 컴포넌트로 변환합니다
   - Session 3에서 배운 JSX 리스트 렌더링 패턴입니다

2. **`key={user.id}`**
   - React가 각 항목을 추적하기 위한 고유 식별자입니다
   - Session 3에서 배운 key prop 규칙입니다

3. **`selected={selectedUser?.id === user.id}`**
   - 현재 선택된 사용자와 비교하여 하이라이트 여부를 결정합니다
   - `?.`는 옵셔널 체이닝 — selectedUser가 null이면 undefined를 반환하여 비교가 `false`가 됩니다

4. **`onClick={setSelectedUser}`**
   - UserCard를 클릭하면 `setSelectedUser(user)` 가 호출됩니다
   - UserCard 컴포넌트 내부에서 `onClick(user)`를 호출하도록 이미 구현되어 있습니다
   - 이것이 Session 4 Thinking in React에서 배운 **콜백 Props 패턴**입니다

> **강사 안내**: 파일을 저장하면 브라우저에 10명의 사용자 카드가 표시됩니다. 사용자를 클릭하면 우측에 상세 정보가 나타나는 것을 확인합니다. "지금 클릭해도 Posts 탭에는 아무것도 없습니다. 이것이 바로 Task 2에서 여러분이 구현할 내용입니다."

### Step 4: 시연 마무리 및 핵심 정리 (5분)

**시연에서 다룬 핵심 패턴 3가지를 정리합니다:**

| 패턴 | 코드 | 용도 |
|------|------|------|
| useState + TypeScript | `useState<User[]>([])` | 타입 안전한 상태 관리 |
| useEffect + fetch | `useEffect(() => { fetch... }, [])` | 컴포넌트 마운트 시 데이터 로딩 |
| map + key + 콜백 Props | `users.map(u => <UserCard onClick={set} />)` | 리스트 렌더링 + 이벤트 전달 |

> **강사 안내**: "이 세 가지 패턴이 Task 2~6에서 반복됩니다. Task 2는 지금 제가 한 것과 거의 동일한 구조이니 먼저 도전해보세요."

---

## YOU DO: Task 2~6 필수 과제 (독립 실습, 90분)

### 진행 가이드

1. **TODO 주석을 찾으세요**: `App.tsx`에서 `Ctrl+F`로 `TODO`를 검색합니다
2. **번호 순서대로 진행하세요**: 각 Task는 이전 Task에 의존합니다
3. **막히면 힌트를 참고하세요**: 각 Task에 3단계 힌트가 있습니다
4. **15분 이상 막히면 정답을 보세요**: `solutions/` 폴더에 정답이 있습니다

---

### Task 2: 사용자별 게시글 표시

| 항목 | 내용 |
|------|------|
| **난이도** | ★★☆☆☆ (Task 1과 거의 동일) |
| **예상 시간** | 10분 |
| **핵심 개념** | useState, useEffect 의존성 배열, 조건부 fetch |
| **수정 파일** | `App.tsx` |
| **관련 TODO** | `TODO (필수 2-a)`, `TODO (필수 2-b)`, PostCard 렌더링 |

**목표**: 사용자를 클릭하면 해당 사용자의 게시글이 표시되도록 합니다.

**해야 할 것**:
1. `posts` 상태를 `useState<Post[]>([])`로 선언합니다 (TODO 2-a)
2. `selectedUser`가 바뀔 때마다 게시글을 fetch합니다 (TODO 2-b)
3. `filteredPosts` 임시 변수를 `posts`로 교체합니다
4. PostCard 렌더링 부분의 주석을 해제합니다

**힌트 1**: useEffect의 의존성 배열에 `selectedUser`를 넣어야 합니다.

**힌트 2**: URL은 `${API}/posts?userId=${selectedUser.id}` 입니다. selectedUser가 null이면 fetch하지 마세요 (`if (!selectedUser) return;`이 이미 있습니다).

**힌트 3**: PostCard 렌더링 코드:
```tsx
{filteredPosts.map((post) => (
  <PostCard key={post.id} post={post} onDelete={deletePost} />
))}
```
(`filteredPosts`를 아직 구현하지 않았다면 `posts`를 직접 사용하세요)

**예상 결과**: 사용자를 클릭하면 Posts 탭에 10개의 게시글 카드가 표시됩니다.

---

### Task 3: 게시글 작성 (POST 요청)

| 항목 | 내용 |
|------|------|
| **난이도** | ★★★☆☆ |
| **예상 시간** | 15분 |
| **핵심 개념** | POST 요청, JSON body, 불변 state 업데이트 |
| **수정 파일** | `App.tsx` |
| **관련 TODO** | `TODO (필수 3)` |

**목표**: PostForm에서 제목과 본문을 입력하면 새 게시글이 목록 맨 위에 추가됩니다.

**해야 할 것**: `addPost` 함수를 완성합니다.

**힌트 1**: `fetch`에 두 번째 인자로 옵션 객체를 전달합니다.
```tsx
const res = await fetch(`${API}/posts`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title, body, userId: selectedUser!.id }),
});
```

**힌트 2**: JSONPlaceholder는 POST 응답으로 항상 `{ id: 101, ... }`을 반환합니다. 여러 개를 추가하면 id가 겹치므로 `Date.now()`로 고유 id를 만듭니다.

**힌트 3**: 완성 코드:
```tsx
const addPost = async ({ title, body }: { title: string; body: string }): Promise<void> => {
  const res = await fetch(`${API}/posts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, body, userId: selectedUser!.id }),
  });
  const newPost: Post = await res.json();
  setPosts((prev) => [{ ...newPost, id: Date.now() }, ...prev]);
};
```

**예상 결과**: 폼에 제목과 내용을 입력하고 Submit하면 게시글이 목록 맨 위에 추가됩니다.

---

### Task 4: 게시글 삭제 (DELETE 요청)

| 항목 | 내용 |
|------|------|
| **난이도** | ★★☆☆☆ |
| **예상 시간** | 10분 |
| **핵심 개념** | DELETE 요청, 배열 filter로 불변 업데이트 |
| **수정 파일** | `App.tsx` |
| **관련 TODO** | `TODO (필수 4)` |

**목표**: 게시글 카드의 ✕ 버튼을 클릭하면 해당 게시글이 삭제됩니다.

**해야 할 것**: `deletePost` 함수를 완성합니다.

**힌트 1**: DELETE 요청은 body가 필요 없습니다. `method: "DELETE"`만 지정하면 됩니다.

**힌트 2**: state에서 해당 id를 제거할 때 `filter`를 사용합니다. Session 4 Tic-Tac-Toe에서 배운 불변 업데이트 패턴입니다.

**힌트 3**: 완성 코드:
```tsx
const deletePost = async (id: number): Promise<void> => {
  await fetch(`${API}/posts/${id}`, { method: "DELETE" });
  setPosts((prev) => prev.filter((p) => p.id !== id));
};
```

**예상 결과**: 게시글 카드의 ✕ 버튼을 클릭하면 해당 카드가 목록에서 사라집니다.

---

### Task 5: 할 일 토글 (PATCH 요청)

| 항목 | 내용 |
|------|------|
| **난이도** | ★★★☆☆ |
| **예상 시간** | 20분 |
| **핵심 개념** | PATCH 요청, map으로 불변 업데이트, 별도 컴포넌트 수정 |
| **수정 파일** | `src/components/TodoSection.tsx` |
| **관련 TODO** | `TODO (필수 5-a)`, `TODO (필수 5-b)`, `TODO (필수 5-c)` |

**목표**: Todos 탭에서 할 일 항목을 클릭하면 완료/미완료 상태가 토글됩니다.

**해야 할 것**:
1. `TodoSection.tsx`를 열고 TODO를 찾습니다
2. `todos` 상태를 `useState<Todo[]>([])`로 선언합니다 (5-a)
3. `userId`가 바뀔 때 todos를 fetch합니다 (5-b)
4. `toggleTodo` 함수에서 map으로 completed를 반전시킵니다 (5-c)

**힌트 1**: fetch URL은 `${API}/todos?userId=${userId}` 입니다.

**힌트 2**: 토글은 `map`을 사용합니다 — 해당 id인 todo만 completed를 반전시킵니다:
```tsx
setTodos((prev) =>
  prev.map((t) => (t.id === id ? { ...t, completed: !t.completed } : t))
);
```

**힌트 3**: PATCH 요청은 토글 후에 보내되, 응답은 무시해도 됩니다 (JSONPlaceholder는 fake API이므로):
```tsx
fetch(`${API}/todos/${id}`, {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ completed: true }),
});
```

**예상 결과**: Todos 탭에서 항목을 클릭하면 체크/언체크 애니메이션이 동작하고, 진행률 바가 업데이트됩니다.

---

### Task 6: 댓글 펼치기/접기

| 항목 | 내용 |
|------|------|
| **난이도** | ★★★☆☆ |
| **예상 시간** | 15분 |
| **핵심 개념** | 조건부 렌더링, 지연 fetch (lazy loading), 토글 상태 |
| **수정 파일** | `src/components/CommentList.tsx` |
| **관련 TODO** | 파일 내 TODO 참조 |

**목표**: 게시글 카드 하단의 "Show comments" 버튼을 클릭하면 해당 게시글의 댓글이 표시됩니다.

**해야 할 것**:
1. `CommentList.tsx`를 열고 TODO를 찾습니다
2. `comments`와 `open` 상태를 만듭니다
3. `toggle` 함수에서 처음 열 때만 fetch하고, 이후에는 open/close만 토글합니다
4. `open`이 true일 때만 댓글 목록을 렌더링합니다

**힌트 1**: fetch URL은 `${API}/posts/${postId}/comments` 입니다.

**힌트 2**: "처음 열 때만 fetch" 패턴:
```tsx
if (!open && comments.length === 0) {
  // 처음 여는 경우 → fetch
}
setOpen((prev) => !prev);
```

**힌트 3**: `solutions/CommentList.tsx`에서 전체 코드를 확인할 수 있습니다.

**예상 결과**: "Show comments"를 클릭하면 5개의 댓글이 표시되고, "Hide comments"를 클릭하면 숨겨집니다.

---

## 도전 과제: Task 7~11 (빠르게 끝난 학생용)

필수 Task 1~6을 모두 완료한 학생은 아래 도전 과제에 도전합니다.

### Task 7: 앨범 갤러리 (★★★☆☆)

`src/components/AlbumGallery.tsx`에서 TODO를 구현합니다. Albums 탭에서 사용자의 앨범과 사진을 표시합니다. 중첩 fetch 패턴 (albums → photos)을 연습합니다.

### Task 8: 대시보드 통계 — Promise.all (★★★★☆)

`App.tsx`에서 `Promise.all`을 사용하여 5개 리소스를 동시에 fetch하고 상단 통계 카드에 표시합니다. `stats` state에 `DashboardStats` 객체를 저장합니다.

### Task 9: 게시글 검색 — useMemo (★★★☆☆)

`App.tsx`에서 `useMemo`를 import하고, `search` 키워드로 posts의 title과 body를 필터링합니다. `filteredPosts` 변수를 useMemo로 교체합니다.

### Task 10: 스켈레톤 로딩 UI (★★☆☆☆)

각 컴포넌트에 로딩 중일 때 `Skeleton` 컴포넌트를 표시합니다. `Skeleton`은 이미 `components/ui/Skeleton.tsx`에 제공되어 있습니다.

### Task 11: 콜백으로 통계 실시간 갱신 — StatsUpdateFn (★★★★★)

`StatsUpdateFn` 타입을 사용하여 자식 컴포넌트(TodoSection)에서 부모(App)의 stats를 실시간 갱신합니다. 게시글 추가/삭제, Todo 토글 시 상단 통계 숫자가 즉시 반영됩니다.

> 도전 11 상세 구현 흐름은 `social-dashboard-starter/README.md`의 "도전 11 상세" 섹션을 참조하세요.

---

## 정답 코드 참조

`social-dashboard-starter/solutions/` 폴더에 정답이 있습니다.

```
solutions/
├── App.tsx              ← 필수 1~4, 도전 8·9·11
├── PostForm.tsx         ← 필수 3 (폼 제출)
├── PostCard.tsx         ← 필수 4 (삭제 버튼) + 필수 6 (댓글)
├── CommentList.tsx      ← 필수 6 (댓글 펼치기/접기)
├── TodoSection.tsx      ← 필수 5 (토글) + 도전 11 (통계 콜백)
└── AlbumGallery.tsx     ← 도전 7 (앨범 갤러리)
```

**정답 비교 방법**:
```bash
# 스타터 코드와 정답 비교
diff src/App.tsx solutions/App.tsx
```

---

## 트러블슈팅

### "Cannot find name 'users'" 오류

useState로 상태를 만든 후, 파일 하단의 임시 변수(`const users: User[] = []`, `const selectedUser: User | null = null`)를 삭제했는지 확인하세요.

### "Property 'id' does not exist on type 'never'" 오류

useState의 제네릭 타입을 지정하지 않았을 수 있습니다. `useState([])` 대신 `useState<User[]>([])`로 작성하세요.

### useEffect가 무한 루프에 빠짐

의존성 배열에 매 렌더링마다 새로 생성되는 값(객체, 배열)을 넣지 않았는지 확인하세요. `selectedUser`처럼 참조가 변하는 값만 넣어야 합니다.

### 게시글이 추가되지 않음 (POST 후 화면 변화 없음)

`setPosts`로 state를 업데이트했는지 확인하세요. `fetch` 응답만 받고 state를 업데이트하지 않으면 화면이 갱신되지 않습니다.

### TypeScript에서 `selectedUser!.id`의 `!`는 무엇인가요?

Non-null Assertion Operator입니다. `selectedUser`가 `User | null` 타입인데, 이 시점에서 null이 아님을 확신할 때 사용합니다. addPost 함수는 selectedUser가 있을 때만 호출되므로 안전합니다.

### 콘솔에 "Warning: Each child in a list should have a unique key prop"

`.map()`으로 생성한 컴포넌트에 `key` prop을 추가했는지 확인하세요. `key={post.id}`, `key={user.id}` 등 고유한 값을 사용합니다.

---

## 핵심 패턴 요약

이 실습에서 반복적으로 사용한 패턴입니다.

### 1. 데이터 fetch 패턴

```tsx
const [data, setData] = useState<Type[]>([]);

useEffect(() => {
  const fetchData = async () => {
    const res = await fetch(url);
    const json: Type[] = await res.json();
    setData(json);
  };
  fetchData();
}, [dependency]);
```

### 2. 불변 state 업데이트 패턴

```tsx
// 추가: 배열 앞에 새 항목 추가
setItems((prev) => [newItem, ...prev]);

// 삭제: filter로 제거
setItems((prev) => prev.filter((item) => item.id !== id));

// 수정: map으로 특정 항목만 변경
setItems((prev) =>
  prev.map((item) => (item.id === id ? { ...item, done: !item.done } : item))
);
```

### 3. 콜백 Props 패턴

```tsx
// 부모: 함수를 props로 전달
<ChildComponent onAction={handleAction} />

// 자식: props로 받은 함수를 호출
function ChildComponent({ onAction }: { onAction: (value: string) => void }) {
  return <button onClick={() => onAction("hello")}>클릭</button>;
}
```
