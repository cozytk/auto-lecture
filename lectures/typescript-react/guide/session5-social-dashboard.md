# Session 5: 종합 실습 — Social Dashboard

**시간**: 2시간 (15:00–17:00) | **유형**: I DO 시연 + YOU DO 독립 실습
**실습 파일**: `social-dashboard-starter/social-dashboard-starter/`

---

## 세션 목표

이번 세션은 오늘 수업 전체의 결산입니다. TypeScript의 타입 시스템과 React의 핵심 개념을 실제 API와 연동하는 완성된 앱을 만들며 통합합니다.

세션을 마치면 수강생은 다음을 할 수 있습니다.

- `useState<T>()` 제네릭을 사용해 타입이 안전한 상태를 선언할 수 있습니다.
- `useEffect`의 의존성 배열을 정확히 이해하고, 데이터 페치 패턴을 스스로 작성할 수 있습니다.
- `fetch` + `async/await`로 REST API의 GET, POST, DELETE, PATCH 요청을 구현할 수 있습니다.
- 불변 상태 업데이트(`filter`, 스프레드 연산자)를 올바르게 적용할 수 있습니다.
- 콜백 props 패턴으로 자식 컴포넌트에서 부모 상태를 갱신할 수 있습니다.

---

## 앱 구조 안내 (5분)

### 강사 안내

실습 시작 전 브라우저와 에디터를 나란히 열고 앱 구조를 5분간 소개합니다.

```bash
# 터미널에서 실행 (이미 실행 중이라면 생략)
cd social-dashboard-starter/social-dashboard-starter
npm install
npm run dev
```

브라우저에서 `http://localhost:5173`을 엽니다. 지금은 왼쪽 사이드바에 "TODO: UserCard를 렌더링하세요"라는 안내문과 스켈레톤만 보입니다. 오늘 실습을 마치면 이 화면이 완전한 소셜 대시보드로 바뀝니다.

> "에디터에서 `src/App.tsx`를 열어 보겠습니다. 이 파일이 오늘 주로 작업할 메인 파일입니다. 파일 위쪽에는 이미 작성된 `import` 구문들이 있고, 그 아래에 `TODO` 주석으로 여러분이 채워야 할 부분이 표시되어 있습니다.
>
> `src/types.ts`에는 이 앱에서 사용하는 모든 타입이 정의되어 있습니다. `User`, `Post`, `Comment`, `Todo`, `Album`, `Photo` — JSONPlaceholder API가 반환하는 데이터 구조를 TypeScript interface로 미리 정의해 두었습니다.
>
> `src/components/` 폴더에는 UI 컴포넌트들이 이미 완성되어 있습니다. 여러분은 이 컴포넌트들을 직접 수정하지 않아도 됩니다. 단, Task 5(TodoSection)와 Task 6(CommentList)는 해당 파일에서 TODO를 채워야 합니다.
>
> `solutions/` 폴더에는 정답 코드가 있습니다. 막히면 참고할 수 있습니다."

---

## React 핵심 개념 정리 (10분)

> **강사 안내**: 코딩 전에 이 세션에서 쓰이는 핵심 React 개념 세 가지를 짧게 리뷰합니다. 칠판이나 화면에 구조를 그리며 설명하면 효과적입니다.

### 개념 1: `useState<T>()` — 제네릭 타입과 상태

세션 3에서 이미 배운 `useState`입니다. 오늘은 **TypeScript 제네릭**을 함께 사용합니다. 세션 1에서 제네릭 문법(`<T>`)을 미리 소개했던 것을 기억하십니까? 바로 오늘 그것이 실전에서 쓰입니다.

```typescript
// 세션 1에서 본 제네릭 예시
function identity<T>(value: T): T {
  return value;
}

// useState도 똑같은 제네릭 패턴입니다
const [users, setUsers] = useState<User[]>([]);
//                                  ^^^^^^^^
//                          T = User[]  →  초기값 []는 User[] 타입
```

**왜 제네릭을 쓰는가?**

제네릭 없이 `useState([])` 만 쓰면 TypeScript는 이 배열이 `never[]` 타입이라고 추론합니다. 즉, 아무것도 넣을 수 없는 배열이 됩니다. `useState<User[]>([])` 라고 쓰면 "이 배열은 `User` 객체들만 담는다"는 것을 TypeScript에게 명시적으로 알려줍니다. 그러면 `users[0].name` 이라고 쓸 때 TypeScript가 자동완성과 타입 검사를 제공합니다.

**`User | null` 패턴:**

```typescript
const [selectedUser, setSelectedUser] = useState<User | null>(null);
```

"선택된 유저가 있을 수도 없을 수도 있다"는 상황을 Union 타입으로 표현합니다. 초기값이 `null`이고, 사용자가 클릭하면 `User` 객체가 됩니다. 이후 `selectedUser.name`에 접근할 때 TypeScript는 "null일 수도 있으니 확인하라"고 알려줍니다. 이것이 런타임 오류를 사전에 방지하는 TypeScript의 힘입니다.

---

### 개념 2: `useEffect` — 사이드 이펙트와 의존성 배열

`useEffect`는 오늘 처음 본격적으로 다루는 개념입니다. **컴포넌트 렌더링 이후에 실행해야 할 작업**을 정의합니다.

```
렌더링 (JSX → DOM 반영)  →  useEffect 실행
```

**의존성 배열의 세 가지 형태:**

```typescript
// 형태 1: 빈 배열 [] — 컴포넌트가 처음 마운트될 때 딱 한 번만 실행
useEffect(() => {
  fetchUsers(); // 페이지 로드 시 사용자 목록 한 번만 가져오기
}, []);

// 형태 2: 값이 있는 배열 — selectedUser가 바뀔 때마다 실행
useEffect(() => {
  fetchPosts(); // 선택된 유저가 바뀔 때마다 게시글을 새로 가져오기
}, [selectedUser]);

// 형태 3: 배열 없음 — 매 렌더링마다 실행 (거의 쓰지 않습니다)
useEffect(() => {
  console.log("매번 실행!");
});
```

> "useEffect는 '조건부 자동 실행기'라고 생각하면 됩니다. 의존성 배열에 있는 값이 바뀔 때마다 자동으로 실행됩니다. 빈 배열이면 '처음 한 번만', 특정 값이 있으면 '그 값이 바뀔 때마다'입니다."

---

### 개념 3: `useEffect` 안에서 async/await 사용하는 패턴

`useEffect`의 콜백 함수 자체를 `async`로 만들 수 없습니다. 이것은 React의 설계 상 제약입니다.

```typescript
// 잘못된 방법 — useEffect 콜백을 직접 async로 만들면 안 됩니다
useEffect(async () => {   // ❌ 이렇게 하지 마세요
  const data = await fetch(...);
}, []);

// 올바른 방법 — 내부에 async 함수를 만들고 즉시 호출합니다
useEffect(() => {
  const fetchData = async () => {   // ① async 함수 정의
    const res = await fetch(...);   // ② await 사용
    const data = await res.json();  // ③ JSON 파싱
    setState(data);                 // ④ 상태 업데이트
  };
  fetchData();   // ⑤ 즉시 호출 (함수 정의 후 바로 실행)
}, []);
```

> "왜 직접 async를 쓰면 안 되나요? useEffect의 반환값은 '정리(cleanup) 함수' 또는 undefined여야 합니다. async 함수는 항상 Promise를 반환하므로 React가 혼란스러워합니다. 내부에 async 함수를 만들어 호출하는 이 패턴을 외워두십시오. 실무에서도 항상 이 방식을 씁니다."

---

## I DO — Task 1: 사용자 목록 표시 (강사 시연, 30분)

### 개요

> **강사 안내**: 지금부터 30분은 강사가 직접 코딩하며 시연합니다. 수강생은 보면서 이해하되 아직 타이핑하지 않아도 됩니다. 코드를 입력할 때는 반드시 한 줄씩 직접 타이핑하십시오 — 붙여넣기 금지.

**구현할 내용**: `App.tsx`의 TODO (필수 1-a) ~ (필수 1-d)

---

### Step 1-a: `users` 상태 선언 (5분)

`src/App.tsx`를 열고 상단의 TODO 주석을 찾습니다.

```typescript
// ── State 선언 ──

// TODO (필수 1-a): users 상태를 만드세요
// const [users, setUsers] = useState<User[]>([])
```

주석 아래에 다음을 입력합니다:

```typescript
const [users, setUsers] = useState<User[]>([]);
```

**각 부분을 한 줄씩 설명합니다:**

> "`const [users, setUsers]` — 세션 3에서 배운 배열 구조분해입니다. `useState`는 항상 [현재값, 변경함수] 쌍을 반환합니다. `users`는 현재 사용자 목록이고, `setUsers`는 그 목록을 바꾸는 함수입니다.
>
> `useState<User[]>` — 제네릭입니다. 꺾쇠 안에 `User[]`를 넣어서 '이 상태는 User 배열이다'라고 TypeScript에게 알립니다. `User`는 `src/types.ts`에 정의된 interface입니다.
>
> `([])` — 초기값입니다. 처음에는 빈 배열에서 시작합니다. API에서 데이터를 받아오기 전까지는 유저가 0명인 상태입니다."

**에디터에서 확인해 볼 것:**

`users.` 를 입력하면 TypeScript가 `.length`, `.map`, `.filter` 등의 메서드 자동완성을 보여줍니다. `users[0].` 를 입력하면 `name`, `email`, `username` 등 `User` interface의 속성들이 나타납니다. 이것이 제네릭의 효과입니다.

---

### Step 1-b: `selectedUser` 상태 선언 (3분)

바로 아래 줄에 이어서 입력합니다:

```typescript
const [selectedUser, setSelectedUser] = useState<User | null>(null);
```

**설명:**

> "`User | null` — Union 타입입니다. '유저가 선택되었거나, 아무것도 선택되지 않았거나' 두 상태를 표현합니다. 세션 1에서 배운 Union 타입 기억하십니까? `string | number` 처럼 `|` 기호로 여러 타입을 묶는 것입니다.
>
> 초기값은 `null`입니다. 처음에는 아무도 선택되지 않은 상태입니다."

**중요 — 임시 변수 삭제:**

아래로 스크롤하면 렌더링 직전에 이런 코드가 있습니다:

```typescript
// 임시 변수 (TODO 구현 전 에러 방지용 — state 만든 후 삭제하세요)
const users: User[] = [];
const selectedUser: User | null = null;
```

**이 두 줄을 반드시 삭제해야 합니다.** 삭제하지 않으면 같은 이름의 변수가 두 번 선언되어 TypeScript 오류가 발생합니다.

> "이 임시 변수들은 여러분이 state를 만들기 전에 앱이 오류 없이 실행되도록 미리 넣어둔 플레이스홀더입니다. 이제 진짜 useState 변수를 만들었으니 반드시 삭제해야 합니다."

두 줄을 선택하고 삭제합니다. 저장 후 브라우저를 보면 스켈레톤 로딩 애니메이션이 보여야 합니다(아직 fetch를 구현하지 않았으므로 로딩 상태가 계속 유지됩니다).

---

### Step 1-c: 사용자 목록 fetch (15분)

이제 앱이 마운트될 때 JSONPlaceholder API에서 사용자 10명을 가져오는 코드를 작성합니다.

```typescript
// TODO (필수 1-c): 컴포넌트 마운트 시 사용자 목록을 fetch하세요
useEffect(() => {
  // 여기에 fetch 로직을 구현하세요
}, []);
```

이 useEffect 안을 다음과 같이 채웁니다:

```typescript
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

**한 줄씩 설명합니다:**

> **`const fetchUsers = async () => {`**
>
> "async 함수를 만듭니다. 방금 전 개념 정리에서 설명한 패턴 그대로입니다. useEffect 콜백 자체를 async로 만들 수 없으므로, 내부에 async 함수를 정의합니다."

> **`const res = await fetch(\`${API}/users\`)`**
>
> "`fetch`는 브라우저 내장 함수로 URL에 HTTP 요청을 보냅니다. 파일 맨 위에 `const API = 'https://jsonplaceholder.typicode.com'` 이 있으므로 백틱 템플릿 리터럴로 URL을 조합하면 `https://jsonplaceholder.typicode.com/users`가 됩니다.
>
> `await`은 이 요청이 완료될 때까지 기다립니다. 결과는 `Response` 객체입니다. 아직 데이터 자체가 아닙니다 — 봉투만 받은 상태입니다."

> **`const data: User[] = await res.json()`**
>
> "`res.json()`은 Response 본문을 JSON으로 파싱합니다. 이것도 비동기 작업이므로 `await`가 필요합니다. 파싱 결과를 `User[]` 타입으로 명시했습니다. TypeScript는 API 응답이 실제로 `User[]` 형식인지 런타임에서는 확인하지 못합니다. 우리가 올바른 타입을 직접 지정해야 합니다."

> **`setUsers(data)`**
>
> "가져온 데이터를 상태에 저장합니다. 상태가 바뀌면 React가 자동으로 컴포넌트를 다시 렌더링합니다. 이것이 React의 핵심 동작 원리입니다."

> **`setLoading(false)`**
>
> "`loading` 상태는 파일 위쪽에서 `useState(true)`로 시작합니다. 데이터를 다 받아오면 false로 바꿉니다. 이 값이 false가 되면 렌더링 부분의 조건부 렌더링이 스켈레톤 대신 실제 컴포넌트를 보여줍니다."

> **마지막 줄 `fetchUsers()`**
>
> "함수를 정의했으면 반드시 호출해야 합니다. 이 줄이 없으면 fetchUsers는 정의만 되고 실행되지 않습니다. 처음 배울 때 이 줄을 빠트리는 실수를 자주 합니다."

> **닫는 `}, [])`**
>
> "빈 의존성 배열입니다. '컴포넌트가 처음 화면에 나타날 때(마운트) 딱 한 번만 실행한다'는 의미입니다. 사용자 목록은 앱 시작 시 한 번만 가져오면 됩니다."

**저장 후 브라우저 확인:**

잠깐 스켈레톤 로딩이 보이다가 왼쪽 사이드바에 사용자 카드들이 나타납니다. 개발자 도구 Network 탭을 열어 `users` 요청이 Status 200으로 성공했는지 확인합니다.

---

### Step 1-d: UserCard 렌더링 (7분)

가져온 사용자들을 화면에 렌더링합니다. `App.tsx`의 렌더링 부분으로 스크롤합니다:

```tsx
{/* TODO (필수 1-d): users.map()으로 UserCard를 렌더링하세요 */}
{/* <UserCard
      key={user.id}
      user={user}
      selected={selectedUser?.id === user.id}
      onClick={setSelectedUser}
    /> */}
<p className="text-sm text-slate-400 text-center py-4">
  TODO: UserCard를 렌더링하세요
</p>
```

`<p>` 태그를 포함한 안내문을 지우고, 주석 처리된 UserCard 코드의 주석을 해제합니다. 최종 형태:

```tsx
{users.map((user) => (
  <UserCard
    key={user.id}
    user={user}
    selected={selectedUser?.id === user.id}
    onClick={setSelectedUser}
  />
))}
```

**각 부분 설명:**

> **`users.map((user) => (...))`**
>
> "세션 4 Thinking in React에서 배운 리스트 렌더링 패턴입니다. `users` 배열의 각 요소를 JSX 컴포넌트로 변환합니다. `users`에 10개의 User 객체가 있으면 UserCard가 10개 렌더링됩니다."

> **`key={user.id}`**
>
> "React가 리스트 항목들을 효율적으로 업데이트하기 위해 필요한 고유 식별자입니다. `user.id`는 JSONPlaceholder가 제공하는 1~10 정수입니다. key가 없으면 React가 경고를 출력합니다."

> **`selected={selectedUser?.id === user.id}`**
>
> "옵셔널 체이닝 `?.`입니다. `selectedUser`가 null이면 `undefined`를 반환하고 `undefined === user.id`는 false가 됩니다. null이 아니면 id를 비교합니다. 이 값이 true인 카드는 파란색 테두리로 강조 표시됩니다."

> **`onClick={setSelectedUser}`**
>
> "콜백 props 패턴입니다. 세션 4 Thinking in React에서 배운 '상태 끌어올리기'와 같은 원리입니다. UserCard가 클릭되면 UserCard 내부에서 `onClick(user)` 를 호출하고, 그것이 App의 `setSelectedUser(user)` 를 실행합니다. 클릭된 사용자가 `selectedUser` 상태에 저장되고 컴포넌트가 다시 렌더링됩니다."

**저장 후 브라우저 확인:**

- 왼쪽 사이드바에 10명의 사용자 카드가 표시됩니다.
- 카드를 클릭하면 오른쪽 메인 영역에 해당 사용자의 이름, 이메일, 회사 정보가 나타납니다.
- 선택된 카드가 강조 표시됩니다.
- 아직 게시글은 보이지 않습니다(Task 2가 미완성이므로).

**Task 1 완료 체크리스트:**

- [ ] 왼쪽에 사용자 10명이 카드 형태로 표시된다
- [ ] 클릭 시 오른쪽에 해당 사용자 정보(이름, 이메일, 회사)가 표시된다
- [ ] 선택된 카드가 하이라이트된다
- [ ] 임시 변수 두 줄이 삭제되었다

---

## YOU DO — 독립 실습 (90분)

> **강사 안내**: 이제 수강생이 스스로 구현합니다. 강사는 순회하며 질문에 답합니다. 막히면 아래의 단계별 힌트를 순서대로 제공하십시오. 힌트를 한 번에 다 주지 말고 Hint 1 → 2 → 3 순으로 단계적으로 제공하는 것이 학습 효과가 좋습니다.

---

### Task 2: 게시글 목록 가져오기 ★★☆☆☆

**예상 시간**: 15분
**난이도**: ★★☆☆☆ (Task 1과 거의 동일한 패턴)
**파일**: `src/App.tsx`
**연결 개념**: useEffect 의존성 배열, Task 1-c 패턴 응용

**구현 내용:**
선택된 사용자가 바뀔 때마다 해당 사용자의 게시글을 API에서 가져옵니다.

**예상 결과:**
사용자를 클릭하면 오른쪽 Posts 탭에 그 사용자의 게시글 목록이 나타납니다. 다른 사용자를 클릭하면 게시글 목록이 바뀝니다.

**구현할 TODO:**
- `(필수 2-a)`: posts 상태 선언
- `(필수 2-b)`: selectedUser 의존 useEffect 구현
- 렌더링 부분에서 PostCard 주석 해제

---

**Hint 1 — 어디서 시작할지 모르겠다면:**

Task 1-a, 1-c를 다시 보십시오. 2-a는 1-a와 똑같은 패턴으로 `posts` 상태를 만들면 됩니다. 타입은 `Post[]`이고 초기값은 `[]`입니다.

---

**Hint 2 — state는 만들었는데 useEffect가 막힌다면:**

```typescript
useEffect(() => {
  if (!selectedUser) return;  // null이면 여기서 종료
  const fetchPosts = async () => {
    // Task 1-c와 같은 패턴으로 작성하세요
    // URL: `${API}/posts?userId=${selectedUser.id}`
    // 타입: Post[]
    // setter: setPosts
  };
  fetchPosts();
}, [/* 여기에 무엇을 넣어야 할까요? */]);
```

---

**Hint 3 — 의존성 배열과 렌더링 처리:**

```typescript
}, [selectedUser]);
```

`selectedUser`가 바뀔 때마다 새 사용자의 게시글을 가져와야 합니다. "이 useEffect는 selectedUser가 달라질 때 재실행되어야 한다"는 것을 React에게 알리려면 의존성 배열에 `selectedUser`를 넣습니다.

렌더링 부분에서도 `{/* TODO: filteredPosts (또는 posts)를 map으로 렌더링 */}` 주석과 `<p>` 안내문을 찾아 교체합니다:

```tsx
{posts.map((post) => (
  <PostCard key={post.id} post={post} onDelete={deletePost} />
))}
```

---

### Task 3: 게시글 추가 ★★★☆☆

**예상 시간**: 20분
**난이도**: ★★★☆☆ (POST 요청 — 처음 다루는 패턴)
**파일**: `src/App.tsx`
**연결 개념**: HTTP POST 메서드, 불변 상태 업데이트, 스프레드 연산자

**구현 내용:**
화면 상단의 PostForm에서 제목과 내용을 입력하고 Submit을 누르면 API에 게시글을 추가하고 목록 앞에 표시합니다.

**예상 결과:**
PostForm에 내용을 입력하고 제출하면 목록 맨 위에 새 게시글이 나타납니다.

**중요 주의사항:**
JSONPlaceholder는 실제 데이터베이스에 저장하지 않습니다. POST 요청을 보내면 서버가 응답은 돌려주지만 실제로는 저장되지 않습니다. 또한 서버는 항상 id: 101을 반환합니다. 이 때문에 `Date.now()`로 고유한 id를 만들어 줍니다.

**구현할 TODO:**
`addPost` 함수 안의 TODO (필수 3)

---

**Hint 1 — fetch 요청 구조를 어떻게 만드나요?**

GET과 달리 POST는 fetch의 두 번째 인자에 옵션을 전달합니다:

```typescript
const res = await fetch(`${API}/posts`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title, body, userId: selectedUser!.id }),
});
```

`Content-Type: application/json` 헤더는 "내가 보내는 데이터가 JSON 형식이다"라고 서버에 알리는 것입니다. `JSON.stringify`는 JavaScript 객체를 JSON 문자열로 변환합니다.

---

**Hint 2 — `selectedUser!.id`의 느낌표가 무엇인가요?**

`!`는 TypeScript의 **Non-null assertion 연산자**입니다.

```typescript
// TypeScript는 selectedUser가 null일 수 있다고 알고 있습니다
selectedUser.id   // ❌ 오류: Object is possibly 'null'
selectedUser!.id  // ✅ "나는 이 시점에 null이 아님을 보장한다"
```

`addPost`는 PostForm을 통해서만 호출됩니다. PostForm은 `selectedUser`가 존재할 때(사용자를 선택한 후)만 화면에 표시됩니다. 따라서 `addPost`가 실행되는 시점에는 반드시 `selectedUser`가 null이 아닙니다. 개발자가 이것을 알고 있으므로 `!`로 TypeScript에게 알려주는 것입니다.

---

**Hint 3 — 상태 업데이트를 어떻게 하나요?**

```typescript
const newPost: Post = await res.json();
setPosts((prev) => [{ ...newPost, id: Date.now() }, ...prev]);
```

`(prev) => [새 게시글, ...prev]` 패턴은 "새 배열을 만들되, 맨 앞에 새 항목을 추가하고 기존 항목들은 그대로 뒤에 붙인다"는 의미입니다.

`{ ...newPost, id: Date.now() }`는 서버 응답 객체를 복사하면서 `id`만 `Date.now()`(현재 타임스탬프 밀리초)로 덮어씁니다. 서버가 항상 id: 101을 반환하기 때문에, 여러 번 추가하면 모두 같은 id가 되어 React의 `key`가 충돌합니다. 이를 방지하기 위해 고유한 타임스탬프로 id를 대체합니다.

---

### Task 4: 게시글 삭제 ★★☆☆☆

**예상 시간**: 10분
**난이도**: ★★☆☆☆ (DELETE 요청 + 필터링)
**파일**: `src/App.tsx` + `src/components/PostCard.tsx`
**연결 개념**: HTTP DELETE 메서드, `Array.filter()`, 불변 상태 업데이트

**구현 내용:**
각 게시글 카드 우측 상단의 ✕ 버튼을 누르면 API에 삭제 요청을 보내고 목록에서 해당 게시글을 제거합니다.

**예상 결과:**
게시글 카드의 ✕ 버튼을 클릭하면 해당 게시글이 목록에서 사라집니다.

**구현할 TODO:**
1. `App.tsx`의 `deletePost` 함수 안의 TODO (필수 4)
2. `src/components/PostCard.tsx`의 버튼 onClick 연결

---

**Hint 1 — App.tsx의 deletePost 함수 구조:**

```typescript
const deletePost = async (id: number): Promise<void> => {
  await fetch(`${API}/posts/${id}`, { method: "DELETE" });
  // id에 해당하는 게시글을 posts 배열에서 제거하세요
  // 힌트: filter를 사용합니다
};
```

---

**Hint 2 — filter로 상태 업데이트:**

```typescript
setPosts((prev) => prev.filter((p) => p.id !== id));
```

"id가 일치하지 않는 것들만 남겨라" = "id가 일치하는 것을 제거해라"와 같습니다. 세션 4 Tic-Tac-Toe에서 배운 불변 업데이트와 동일한 원리입니다. 기존 배열을 수정하는 것이 아니라 새 배열을 만듭니다.

---

**Hint 3 — PostCard.tsx의 버튼 onClick 연결:**

`src/components/PostCard.tsx`를 열면 삭제 버튼에 onClick이 없습니다:

```tsx
<button
  // TODO (필수 4): onClick={() => onDelete(post.id)}
  className="..."
  title="Delete"
>
  ✕
</button>
```

주석을 지우고 onClick을 추가합니다:

```tsx
<button
  onClick={() => onDelete(post.id)}
  className="..."
  title="Delete"
>
  ✕
</button>
```

---

### Task 5: 할 일 완료 토글 ★★★☆☆

**예상 시간**: 20분
**난이도**: ★★★☆☆ (다른 파일 수정 + map으로 특정 항목 변경)
**파일**: `src/components/TodoSection.tsx`
**연결 개념**: useEffect, HTTP PATCH, map으로 특정 항목만 변경하는 불변 업데이트

**구현 내용:**
Todos 탭에서 할 일 항목을 클릭하면 완료/미완료 상태가 토글됩니다.

**예상 결과:**
할 일 항목을 클릭하면 체크 표시가 토글되고 배경색이 초록색으로 바뀝니다.

**구현할 TODO:**
`src/components/TodoSection.tsx`의:
- `(필수 5-a)`: todos 상태 선언
- `(필수 5-b)`: userId 의존 useEffect로 할 일 fetch
- `(필수 5-c)`: toggleTodo 함수 구현
- 파일 아래쪽의 임시 변수 `const todos: Todo[] = []` 삭제

---

**Hint 1 — 파일을 처음 열었을 때 어디서 시작할지:**

`TodoSection.tsx`를 열고 `// TODO (필수 5-a)` 주석을 찾습니다. `App.tsx`의 Task 1-a, 2-a와 완전히 동일한 방식입니다. 타입만 `Todo[]`로 바꾸면 됩니다.

파일 아래쪽에 `const todos: Todo[] = [];` 임시 변수가 있습니다. state를 만든 후 이 줄도 반드시 삭제해야 합니다.

---

**Hint 2 — toggleTodo의 구조:**

```typescript
const toggleTodo = (id: number): void => {
  setTodos((prev) =>
    prev.map((t) => {
      if (t.id !== id) return t;                    // 해당 항목이 아니면 그대로 반환
      return { ...t, completed: !t.completed };     // 해당 항목만 completed 반전
    })
  );

  // PATCH 요청 (서버에 변경 알리기 — 응답은 사용하지 않아도 됩니다)
  fetch(`${API}/todos/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed: true }),
  });
};
```

---

**Hint 3 — map으로 특정 항목만 변경하는 패턴 설명:**

이 패턴은 실무에서 매우 자주 쓰이는 React 불변 업데이트 패턴입니다:

```typescript
// "id가 일치하는 항목만 바꾸고, 나머지는 그대로"
prev.map((item) => {
  if (item.id !== id) return item;                          // 해당 아님 → 원본 그대로 반환
  return { ...item, completed: !item.completed };           // 해당 → 변경된 복사본 반환
})
```

`{ ...item, completed: !item.completed }` — 스프레드 연산자로 기존 객체를 복사하고, `completed` 속성만 반전시킵니다. 세션 4 Tic-Tac-Toe에서 squares 배열을 불변으로 업데이트한 패턴과 동일합니다.

---

### Task 6: 댓글 표시 ★★★☆☆

**예상 시간**: 20분
**난이도**: ★★★☆☆ (조건부 렌더링 + 클릭 시 지연 fetch)
**파일**: `src/components/CommentList.tsx`
**연결 개념**: 조건부 fetch (처음 클릭 시만), 토글 UI 패턴

**구현 내용:**
각 게시글 카드 하단의 "Show comments" 버튼을 클릭하면 해당 게시글의 댓글 목록이 펼쳐집니다. 다시 클릭하면 접힙니다. 댓글은 처음 클릭 시에만 fetch합니다(이미 불러왔으면 캐시된 데이터를 사용).

**예상 결과:**
"Show comments"를 클릭하면 버튼 텍스트가 "Hide comments"로 바뀌고 댓글 목록이 나타납니다.

**구현할 TODO:**
`src/components/CommentList.tsx`의:
- `(필수 6-a)`: comments, open 상태 선언
- `(필수 6-b)`: toggle 함수 구현 (조건부 fetch + open 토글)
- `(필수 6-c)`: 댓글 목록 렌더링

---

**Hint 1 — 어떤 상태가 필요한가요?**

```typescript
const [comments, setComments] = useState<Comment[]>([]);
const [open, setOpen] = useState(false);
```

두 개의 상태가 필요합니다. `comments`는 가져온 댓글 데이터, `open`은 펼침/접힘 여부입니다. `open`은 boolean 값이므로 `useState<boolean>(false)` 또는 짧게 `useState(false)`로 씁니다. TypeScript가 `false`에서 boolean 타입을 자동 추론합니다.

---

**Hint 2 — toggle 함수의 로직:**

```typescript
const toggle = async (): Promise<void> => {
  // 처음 펼칠 때만 fetch (이미 댓글이 있으면 다시 fetch하지 않음)
  if (!open && comments.length === 0) {
    setLoading(true);
    const res = await fetch(`${API}/posts/${postId}/comments`);
    const data: Comment[] = await res.json();
    setComments(data);
    setLoading(false);
  }
  setOpen((prev) => !prev);
};
```

핵심 조건: `!open && comments.length === 0` — "현재 닫혀있고 댓글을 아직 한 번도 불러오지 않았을 때"만 fetch합니다. 이미 댓글을 불러온 적 있으면 그냥 open 상태만 토글합니다.

---

**Hint 3 — 렌더링 부분 완성:**

버튼 텍스트 (삼항 연산자 중첩):
```tsx
{loading ? "Loading..." : open ? "Hide comments" : "Show comments"}
```

댓글 목록 (`{false && ...}` 부분을 다음으로 교체):
```tsx
{open && (
  <div className="mt-3 space-y-2 pl-3 border-l-2 border-slate-200">
    {comments.map((c) => (
      <div key={c.id} className="text-xs">
        <span className="font-semibold text-slate-700">{c.name}</span>
        <span className="text-slate-400 ml-1">({c.email})</span>
        <p className="text-slate-500 mt-0.5 leading-relaxed">{c.body}</p>
      </div>
    ))}
  </div>
)}
```

---

## 도전 과제 (빠른 수강생용)

Task 1–6을 먼저 완료한 수강생을 위한 추가 과제입니다. `solutions/` 폴더에서 정답을 확인할 수 있습니다.

---

### 도전 7: AlbumGallery 구현 ★★★☆☆

**파일**: `src/components/AlbumGallery.tsx`
**구현 내용**: Albums 탭에서 사용자의 앨범 목록 fetch 및 사진 갤러리 표시
**핵심 패턴**: userId 의존 useEffect + 앨범 클릭 시 사진 fetch

```typescript
// 앨범 목록: useEffect로 userId가 바뀔 때마다 fetch
// URL: `${API}/albums?userId=${userId}`

// 사진 목록: 앨범 클릭 시 비동기 함수 (openAlbum)로 fetch
// URL: `${API}/albums/${album.id}/photos`
```

---

### 도전 8: Promise.all로 대시보드 통계 ★★★★☆

**파일**: `src/App.tsx`
**구현 내용**: 앱 로드 시 5개 API를 병렬로 호출해 상단 통계 카드를 채웁니다.
**핵심 패턴**: `Promise.all`로 여러 fetch를 동시에 실행하고 모두 완료되면 stats 업데이트

```typescript
useEffect(() => {
  Promise.all([
    fetch(`${API}/posts`).then((r) => r.json()),
    fetch(`${API}/comments`).then((r) => r.json()),
    fetch(`${API}/todos`).then((r) => r.json()),
    fetch(`${API}/albums`).then((r) => r.json()),
    fetch(`${API}/photos`).then((r) => r.json()),
  ]).then(([posts, comments, todos, albums, photos]) => {
    setStats({
      posts: posts.length,
      comments: comments.length,
      todoDone: todos.filter((t: { completed: boolean }) => t.completed).length,
      todoTotal: todos.length,
      albums: albums.length,
      photos: photos.length,
    });
  });
}, []);
```

**학습 포인트**: `Promise.all`은 배열 안의 모든 Promise가 완료될 때까지 기다립니다. 5개 API를 순서대로 호출하면 최대 2.5초가 걸리지만, `Promise.all`로 병렬 호출하면 가장 느린 요청 하나 분의 시간만 걸립니다.

---

### 도전 9: useMemo로 검색 필터링 ★★★☆☆

**파일**: `src/App.tsx`
**구현 내용**: SearchBar의 입력값으로 게시글 제목과 본문을 실시간 필터링
**핵심 패턴**: `useMemo` — 의존하는 값이 바뀔 때만 재계산

```typescript
// import에 useMemo 추가
import { useState, useEffect, useMemo } from "react";

const filteredPosts = useMemo(() => {
  if (!search.trim()) return posts;
  const q = search.toLowerCase();
  return posts.filter(
    (p) => p.title.toLowerCase().includes(q) || p.body.toLowerCase().includes(q)
  );
}, [posts, search]);
```

기존의 `const filteredPosts: Post[] = [];` 임시 코드를 이것으로 교체합니다.

**학습 포인트**: `useMemo`는 메모이제이션(memoization) — 이전 계산 결과를 기억해 두었다가, 의존하는 값(`posts`, `search`)이 바뀔 때만 재계산합니다. 매 렌더링마다 filter를 돌리는 것보다 효율적입니다.

---

### 도전 10: Skeleton 로딩 상태 ★★★★☆

**파일**: `src/components/TodoSection.tsx`, `src/components/AlbumGallery.tsx`
**구현 내용**: 데이터를 fetch하는 동안 Skeleton 컴포넌트를 표시합니다.
**참고**: `src/components/ui/Skeleton.tsx` 컴포넌트가 이미 완성되어 있습니다.

```tsx
import { Skeleton } from "./ui/Skeleton";

// loading이 true인 동안 보여줄 UI:
if (loading) {
  return (
    <div className="space-y-2">
      {[1, 2, 3].map((i) => (
        <Skeleton key={i} className="h-10 w-full" />
      ))}
    </div>
  );
}
```

---

### 도전 11: StatsUpdateFn 콜백 패턴 ★★★★★

**파일**: `src/App.tsx`, `src/components/TodoSection.tsx`
**구현 내용**: 자식 컴포넌트(TodoSection)에서 부모(App)의 통계를 갱신하는 콜백 패턴 구현
**핵심 타입**: `StatsUpdateFn = (key: keyof DashboardStats, value: number | ((prev: number) => number)) => void`

이 도전 과제는 React의 핵심 데이터 흐름 패턴을 깊이 이해해야 합니다. `solutions/App.tsx`와 `solutions/TodoSection.tsx`를 함께 참고하십시오.

---

## 트러블슈팅 가이드

### 오류 1: `selectedUser` is possibly null

```
Error: Object is possibly 'null'. (ts2531)
```

**원인**: `selectedUser`가 `User | null` 타입인데, null 체크 없이 접근하려 할 때 발생합니다.

**해결책 A — 조건부 조기 반환 (useEffect 안에서)**:
```typescript
useEffect(() => {
  if (!selectedUser) return;  // null이면 여기서 종료
  // 이 아래에서는 selectedUser가 반드시 User 타입임이 보장됩니다
  fetchPosts();
}, [selectedUser]);
```

**해결책 B — 옵셔널 체이닝 (JSX 안에서)**:
```tsx
{selectedUser?.name}  // selectedUser가 null이면 undefined를 렌더링 (아무것도 안 보임)
```

**해결책 C — Non-null assertion (확실히 null이 아님을 알 때만 사용)**:
```typescript
selectedUser!.id  // "여기선 절대 null이 아니야"라고 TypeScript에게 보장
```

---

### 오류 2: 같은 이름의 변수 중복 선언

```
Error: Cannot redeclare block-scoped variable 'users'. (ts2451)
```

**원인**: `useState`로 `users`를 만들었는데, 아래쪽의 임시 변수 `const users: User[] = []`를 아직 삭제하지 않은 것입니다.

**해결책**: `App.tsx` 아래쪽에 있는 다음 두 줄을 삭제합니다:
```typescript
const users: User[] = [];               // 삭제
const selectedUser: User | null = null; // 삭제
```

`TodoSection.tsx`에도 동일한 임시 변수가 있습니다:
```typescript
const todos: Todo[] = [];  // 삭제
```

---

### 오류 3: 사용자를 바꿔도 게시글이 업데이트되지 않음

**원인**: Task 2의 useEffect 의존성 배열에 `selectedUser`를 넣지 않았습니다.

**잘못된 코드**:
```typescript
useEffect(() => {
  // selectedUser를 사용하는 fetch 로직
}, []);  // ❌ 빈 배열이면 처음 한 번만 실행
```

**올바른 코드**:
```typescript
useEffect(() => {
  if (!selectedUser) return;
  // fetch 로직
}, [selectedUser]);  // ✅ selectedUser가 바뀔 때마다 재실행
```

---

### 오류 4: useEffect 안에서 async 직접 사용

```
Warning: An effect function must not return anything besides a function,
which is used for clean-up.
```

**원인**: useEffect 콜백 자체를 async로 만들면 Promise를 반환하게 됩니다.

**잘못된 코드**:
```typescript
useEffect(async () => {  // ❌
  const data = await fetch(url);
}, []);
```

**올바른 코드**:
```typescript
useEffect(() => {  // ✅
  const fetchData = async () => {
    const data = await fetch(url);
  };
  fetchData();  // 반드시 호출해야 합니다
}, []);
```

---

### 오류 5: fetch 후 빈 화면 또는 데이터가 나타나지 않음

확인 순서:

1. 개발자 도구 → Network 탭에서 API 요청이 Status 200으로 성공했는지 확인합니다.
2. 개발자 도구 → Console 탭에서 JavaScript 오류가 있는지 확인합니다.
3. `setUsers(data)` 대신 `setUsers([data])` 처럼 배열로 잘못 감싸지 않았는지 확인합니다.
4. 렌더링 부분에서 `posts.map(...)` 코드가 올바르게 작성되었는지 확인합니다. PostCard 주석 처리된 코드를 해제해야 합니다.
5. `fetchUsers()` 호출 줄이 useEffect 안에 있는지 확인합니다 (정의만 하고 호출하지 않은 경우).

---

### 오류 6: 게시글 삭제/추가 후 목록이 바뀌지 않음

**원인 A**: 직접 배열을 변경했습니다. React는 배열의 참조가 바뀌어야 리렌더링됩니다.

```typescript
// ❌ 직접 변경 (리렌더링 안 됨)
posts.push(newPost);
setPosts(posts);  // 같은 배열 참조이므로 React가 변화를 감지하지 못합니다

// ✅ 새 배열 생성 (리렌더링 됨)
setPosts((prev) => [newPost, ...prev]);
```

**원인 B**: `deletePost`를 `App.tsx`에 구현했는데 `PostCard.tsx`의 버튼 onClick을 연결하지 않았습니다. Task 4는 두 파일을 모두 수정해야 합니다.

---

### 오류 7: TodoSection의 todos가 항상 비어 있음

`TodoSection.tsx`에서 state를 만들었는데 파일 아래쪽에 있는 임시 변수를 삭제하지 않으면 `filtered`, `doneCount` 등의 계산이 모두 빈 배열을 기준으로 실행됩니다.

```typescript
const todos: Todo[] = [];  // ← 이 줄이 있으면 반드시 삭제
```

이 줄이 실제 `useState`로 만든 `todos` 변수를 shadow(가리기)하기 때문입니다.

---

## Q&A 예상 질문

### Q1. JSONPlaceholder가 실제로 데이터를 저장하지 않으면 POST/DELETE가 왜 필요한가요?

> "연습용 서버에서 HTTP 메서드의 형식과 패턴을 익히는 것이 목적입니다. 실제 서비스에서는 동일한 코드가 진짜 데이터베이스에 저장됩니다. 패턴을 먼저 익히고, 나중에 실제 서버에 연결하는 것이 학습 순서입니다."

### Q2. `useEffect`에서 return을 쓰는 경우가 있던데, 오늘 실습에는 없네요. 왜 없나요?

> "useEffect의 return은 '정리(cleanup) 함수'입니다. 컴포넌트가 화면에서 사라질 때 실행됩니다. WebSocket 연결 해제, 타이머 취소 등에 사용합니다. 오늘 실습은 단순 fetch이므로 cleanup이 필요 없습니다. 실무에서는 메모리 누수 방지를 위해 cleanup을 자주 씁니다."

### Q3. `useState`에 제네릭을 안 써도 동작하던데, 꼭 써야 하나요?

> "안 쓸 수도 있지만, 안 쓰면 TypeScript가 타입을 잘못 추론할 수 있습니다. `useState([])` 만 쓰면 `never[]`로 추론되어 아무것도 넣을 수 없게 됩니다. 초기값으로부터 타입을 추론할 수 없는 경우(null, 빈 배열)에는 반드시 제네릭을 명시해야 합니다."

### Q4. `const [posts, setPosts]` 에서 `posts`는 왜 `const`인데 값이 바뀌나요?

> "좋은 질문입니다. `posts` 변수 자체는 바뀌지 않습니다. 리렌더링이 일어날 때 함수 전체가 다시 실행되고, 그때 `useState`가 새로운 값을 반환합니다. 즉, `posts`는 매 렌더링마다 새로 선언되고 새 값을 가집니다. `const`는 '이 렌더링 사이클 안에서는 이 변수에 직접 재할당하지 않겠다'는 의미입니다."

### Q5. Task 3에서 왜 `Date.now()`를 id로 쓰나요?

> "JSONPlaceholder가 항상 id: 101을 반환하기 때문입니다. 여러 게시글을 추가하면 모두 id: 101이 되어 React의 `key`가 중복됩니다. `Date.now()`는 현재 시각을 밀리초 정수로 반환해서 사실상 유니크합니다. 실제 프로덕션에서는 서버가 진짜 유니크 id를 부여하므로 이런 처리가 필요 없습니다."

### Q6. `setPosts((prev) => [...])` 에서 왜 함수 형태로 쓰나요?

> "대부분의 경우 `setPosts([newPost, ...posts])`도 동작합니다. 하지만 함수 형태 `setPosts(prev => ...)` 는 '현재 상태의 최신 값'을 보장합니다. React의 상태 업데이트는 비동기이기 때문에, 연속으로 여러 번 setState를 호출하는 경우 `posts` 변수가 최신 값이 아닐 수 있습니다. 함수 형태는 항상 최신 값을 `prev`로 받으므로 더 안전합니다. 이 패턴을 습관화하는 것을 권장합니다."

### Q7. `selectedUser?.id` 와 `selectedUser!.id` 의 차이가 뭔가요?

> "`?.` (옵셔널 체이닝): null이면 오류 없이 undefined를 반환합니다. 안전하게 접근합니다.
>
> `!` (Non-null assertion): null이 아님을 TypeScript에게 보장합니다. 만약 실제로 null이라면 런타임 오류가 납니다.
>
> 규칙: 값이 null일 수도 있고 그때는 건너뛰어야 한다면 `?.`, 로직상 절대 null이 될 수 없다는 확신이 있을 때만 `!`를 씁니다."

### Q8. `async/await` 대신 `.then()` 을 써도 되나요?

> "완전히 동일한 동작입니다. `async/await`는 `.then()` 체인을 더 읽기 쉽게 만든 문법적 설탕(syntactic sugar)입니다. 최신 코드에서는 `async/await`를 선호합니다. 도전 8의 `Promise.all` 예제처럼 특정 상황에서는 `.then()`이 더 간결할 때도 있습니다."

### Q9. `filter`가 배열을 바꾸나요, 아니면 새 배열을 만드나요?

> "새 배열을 만듭니다. `filter`, `map`, `slice` 같은 배열 메서드는 원본을 바꾸지 않고 새 배열을 반환합니다. 이것이 React에서 이 메서드들을 선호하는 이유입니다. 반대로 `push`, `splice`, `sort`는 원본을 직접 변경합니다. React 상태에서는 이 메서드들을 직접 쓰면 안 됩니다."

### Q10. 타입 에러가 빨간 밑줄로 표시되는데 그냥 무시하면 되지 않나요?

> "개발 중에는 실행이 될 수도 있지만, 타입 에러는 잠재적 런타임 오류의 신호입니다. TypeScript를 쓰는 이유가 바로 이 경고를 무시하지 않기 위해서입니다. 에러 메시지를 읽고 이해하는 습관이 중요합니다. 오늘 수업에서 나오는 에러들은 모두 이 가이드의 트러블슈팅 섹션에서 해결책을 찾을 수 있습니다."

### Q11. 다른 사용자를 선택할 때마다 게시글을 새로 fetch하면 느리지 않나요?

> "좋은 포인트입니다. 실무에서는 한 번 가져온 데이터를 캐시하는 방법을 씁니다. React Query나 SWR 같은 라이브러리가 이것을 도와줍니다. 오늘은 기본 패턴을 배우는 것이 목적이므로 캐싱 없이 구현했습니다. 나중에 실제 프로젝트를 만들 때는 React Query를 살펴보시기 바랍니다."

### Q12. `useEffect`가 두 번 실행되는 것 같아요. 버그인가요?

> "React 18의 개발 모드에서는 의도적으로 useEffect를 두 번 실행합니다. Strict Mode라는 기능인데, 개발자가 cleanup 함수를 올바르게 작성했는지 검증하기 위해서입니다. 프로덕션 빌드에서는 한 번만 실행됩니다. 지금 단계에서는 무시해도 괜찮습니다."

---

## 세션 종료 정리 (5분)

### 오늘 배운 핵심 패턴 요약

**useState + TypeScript 제네릭 — 세 가지 형태:**
```typescript
useState<User[]>([])          // 빈 배열에서 시작하는 User 배열
useState<User | null>(null)   // null에서 시작하는 nullable User
useState<Post[]>([])          // 빈 배열에서 시작하는 Post 배열
```

**useEffect 데이터 페치 패턴 — 두 가지 형태:**
```typescript
// 마운트 시 한 번만
useEffect(() => {
  const fetchData = async () => { ... };
  fetchData();
}, []);

// 특정 값이 바뀔 때마다
useEffect(() => {
  if (!value) return;
  const fetchData = async () => { ... };
  fetchData();
}, [value]);
```

**불변 상태 업데이트 — 세 가지 패턴:**
```typescript
// 앞에 추가
setPosts(prev => [newPost, ...prev]);

// 제거
setPosts(prev => prev.filter(p => p.id !== id));

// 특정 항목 변경
setTodos(prev => prev.map(t =>
  t.id === id ? { ...t, completed: !t.completed } : t
));
```

### 더 나아가려면

- **React Query**: 서버 상태 관리, 캐싱, 로딩/에러 처리 자동화
- **React Router**: SPA 페이지 전환
- **Zustand / Jotai**: 전역 상태 관리 (useState의 한계를 넘어서)
- **TypeScript `unknown` vs `any`**: any 대신 unknown으로 타입 안전성 유지
- **Error Boundary**: fetch 실패 시 UI 복구 패턴
