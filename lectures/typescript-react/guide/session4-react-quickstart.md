# Session 4: React QuickStart

**시간**: 2시간 (13:00 ~ 15:00) | **유형**: Guided Coding

**참고 원문**: [Tic-Tac-Toe 튜토리얼](https://react.dev/learn/tutorial-tic-tac-toe) · [Thinking in React](https://react.dev/learn/thinking-in-react)

---

## 학습 목표

이 세션이 끝나면 수강생들은 다음을 할 수 있어야 합니다.

- `useState` 훅을 사용하여 컴포넌트 내부 상태를 선언하고 변경할 수 있다
- 이벤트 핸들러(`onClick`, `onChange`)를 TypeScript 타입과 함께 올바르게 작성할 수 있다
- State Lifting Up(상태 끌어올리기) 패턴을 이해하고 직접 구현할 수 있다
- 불변성(Immutability) 원칙을 이해하고 배열을 올바르게 업데이트할 수 있다
- Callback Props 패턴으로 자식 컴포넌트에서 부모 컴포넌트의 상태를 변경할 수 있다
- UI를 컴포넌트 계층 구조로 분해하는 "Thinking in React" 5단계를 따를 수 있다
- Session 5 Social Dashboard에서 쓰일 핵심 패턴들(배열 불변성, Callback Props, Controlled Input)을 숙지한다

---

## 강사 준비 사항

> **강사 안내**: 수업 시작 전 다음 항목을 확인합니다.
>
> - Session 3에서 만든 Vite 프로젝트(`my-react-app`)가 실행 가능한 상태인지 확인합니다 (`npm run dev`)
> - 브라우저에 React 공식 튜토리얼 탭을 미리 열어둡니다: `https://react.dev/learn/tutorial-tic-tac-toe`
> - Tic-Tac-Toe 완성 코드를 별도 파일이나 메모장에 준비해둡니다 (진도가 느린 학생에게 붙여넣기 용)
> - Part B에서 사용할 FilterableProductTable UI 스케치를 화이트보드나 슬라이드로 준비합니다
> - 점심 직후 세션이므로, 짧은 질문으로 집중력을 끌어올리며 시작합니다
> - CSS 스타일은 타이핑 시간 절약을 위해 붙여넣기로 제공합니다

---

## 시간 배분

| 단계 | 내용 | 시간 |
|------|------|------|
| Part A 도입 | `useState` 개념 + Props vs State 비교 | 5분 |
| Part A Step 1–3 | 완성 코드 구조 설명 (Square, Board) | 15분 |
| Part A Step 4–6 | Guided Coding: 클릭·State·Lifting·승자 판정 | 35분 |
| Part A 정리 | Step 7 소개 + 미니 퀴즈 | 5분 |
| Part B 도입 | Thinking in React 5단계 개요 | 5분 |
| Part B Step 1–2 | 컴포넌트 분해 + 정적 버전 | 15분 |
| Part B Step 3–5 | 최소 State + 역방향 데이터 흐름 | 35분 |
| Part B 정리 | Social Dashboard 연결 + Q&A | 5분 |
| **합계** | | **120분** |

---

# Part A: Tic-Tac-Toe (1시간)

> **강사 안내**: "점심 잘 드셨나요? 오후 첫 세션은 오전에 배운 컴포넌트와 Props 위에 '상태(State)'라는 새 개념을 올립니다. React 공식 튜토리얼 예제인 틱택토 게임을 만들면서 자연스럽게 익히겠습니다. 오전에 `useState`를 잠깐 소개했는데, 지금부터 제대로 써봅니다."

---

## 1. `useState`란 무엇인가 (5분)

### 1.1 Props와 State의 차이

Session 3에서 Props를 배웠습니다. Props는 **부모가 자식에게 전달하는 읽기 전용 데이터**입니다. 자식 컴포넌트는 Props를 받아서 화면에 표시할 뿐, 직접 바꿀 수 없습니다.

State는 다릅니다. State는 **컴포넌트가 스스로 기억하고 관리하는 데이터**입니다.

비유를 들면 이렇습니다.

- **Props**: 식당에서 받는 주문서. 손님(부모)이 내용을 결정하고, 주방(자식)은 받은 대로 처리합니다.
- **State**: 주방이 관리하는 재고 목록. 주방 내부에서 직접 관리하며, 재료를 쓸 때마다 업데이트합니다.

| 구분 | Props | State |
|------|-------|-------|
| 출처 | 부모 컴포넌트 | 컴포넌트 자신 |
| 변경 주체 | 부모만 변경 가능 | 컴포넌트 자신이 `setState` 함수로 변경 |
| 변경 시 반응 | 부모가 새 Props를 내리면 재렌더링 | `setState` 호출 시 재렌더링 |
| 비유 | 함수의 파라미터 | 렌더링 간 값이 유지되는 내부 메모리 |

### 1.2 일반 변수로는 왜 안 되는가

처음에는 이런 의문이 생깁니다. "그냥 `let` 변수 쓰면 되지, 왜 `useState`가 필요한가?"

직접 확인해봅시다.

```tsx
// 이 코드는 동작하지 않습니다 — 이유를 이해하는 것이 핵심
function Counter() {
  let count = 0; // 일반 변수

  function handleClick() {
    count = count + 1;
    console.log('클릭! count =', count); // 콘솔에는 1, 2, 3... 으로 증가
  }

  return (
    <div>
      <p>클릭 수: {count}</p>  {/* 화면은 영원히 0에서 바뀌지 않음 */}
      <button onClick={handleClick}>+1</button>
    </div>
  );
}
```

버튼을 아무리 눌러도 화면의 숫자는 0입니다. 콘솔에서는 값이 올라가지만 화면은 그대로입니다.

**왜 그런가?** React가 화면을 다시 그리는 조건은 두 가지뿐입니다.

1. **State가 변경될 때** (`setState` 함수 호출)
2. **Props가 변경될 때** (부모가 새 Props를 내릴 때)

일반 변수 값이 바뀌어도 React는 전혀 알지 못합니다. 화면을 다시 그리지 않습니다.

### 1.3 `useState` 기본 문법

```tsx
import { useState } from 'react';

function Counter() {
  //      ↓ 현재 값   ↓ 값을 바꾸는 함수    ↓ 초기값
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1); // setCount를 호출하면 React가 화면을 다시 그림
  }

  return (
    <div>
      <p>클릭 수: {count}</p>
      <button onClick={handleClick}>+1</button>
    </div>
  );
}
```

**구조 분해 할당 복습**: `const [count, setCount] = useState(0)`은 배열의 구조 분해 할당입니다. `useState`는 항상 `[현재값, 변경함수]` 두 요소짜리 배열을 반환합니다.

**이름 규칙**: 관례적으로 `[값, set값]` 패턴을 사용합니다.

```tsx
const [count, setCount] = useState(0);
const [name, setName] = useState('');
const [isOpen, setIsOpen] = useState(false);
const [items, setItems] = useState<string[]>([]);
```

**TypeScript에서의 타입 추론**: 초기값이 있으면 TypeScript가 타입을 자동으로 추론합니다.

```tsx
const [count, setCount] = useState(0);       // number로 추론
const [name, setName]   = useState('');      // string으로 추론
const [flag, setFlag]   = useState(false);   // boolean으로 추론
```

초기값이 `null`이거나 나중에 다른 타입이 들어오는 경우 제네릭으로 명시합니다.

```tsx
// 초기값이 null이지만 나중에 User 객체가 들어오는 경우
const [user, setUser] = useState<User | null>(null);

// 빈 배열인데 나중에 string[] 이 들어오는 경우
const [items, setItems] = useState<string[]>([]);
```

> **강사 안내**: "`useState<User | null>(null)` 꺾쇠 안이 타입, 괄호 안이 초기값입니다. 제네릭은 Session 1에서 잠깐 소개했습니다. Session 5에서 API 데이터를 다룰 때 이 패턴을 자주 씁니다. 지금은 문법 모양만 기억해두세요."

---

## 2. Tic-Tac-Toe: 완성 코드 구조 이해 (15분)

### 2.1 왜 Tic-Tac-Toe인가

> **강사 안내**: "React 공식 팀이 이 예제를 공식 튜토리얼로 선정한 이유가 있습니다. 9개의 칸이라는 단순한 구조 안에 React의 핵심 개념 다섯 가지가 전부 들어 있습니다. 컴포넌트 분리, Props, State, 이벤트 핸들링, State 끌어올리기. 게임이니까 목표가 명확하고, 진행하면서 '왜 이렇게 해야 하는가'를 자연스럽게 이해하게 됩니다."

**Fast-Forward 계획:**

- **Steps 1–3** (15분): 완성 코드를 보면서 구조를 이해합니다
- **Steps 4–6** (35분): 직접 타이핑하면서 핵심 기능을 추가합니다
- **Step 7** (5분): 집에서 도전할 과제로 소개합니다

### 2.2 최종 완성 목표

```
Tic-Tac-Toe

다음 플레이어: O

[X] [O] [X]
[O] [X] [O]
[O] [ ] [X]

→ X가 이겼습니다!
```

- 두 플레이어(X, O)가 번갈아 빈 칸을 클릭합니다
- 한 줄(행·열·대각선)이 완성되면 승자를 알립니다
- 이미 채워진 칸이나 게임이 끝난 후에는 클릭이 무시됩니다

### 2.3 컴포넌트 구조 설계 (Step 1–3 설명)

먼저 전체 컴포넌트 트리를 이해합니다.

```
Board (게임판 전체 — State를 여기서 관리)
  ├── Square (칸 하나, 인덱스 0)
  ├── Square (칸 하나, 인덱스 1)
  ├── ...
  └── Square (칸 하나, 인덱스 8)
```

> **강사 안내**: "왜 Square를 별도 컴포넌트로 분리했을까요? 지금은 이상해 보일 수 있습니다. '그냥 Board에 버튼 9개 만들면 안 되나?' 라고 생각할 수 있습니다. 그 답을 Step 4–6에서 자연스럽게 경험하게 됩니다. 잠시 이 구조를 믿고 따라와 주세요."

**Step 1 — 시작 뼈대**

`src/App.tsx`를 완전히 비우고 다음을 작성합니다.

```tsx
// src/App.tsx — 시작 뼈대

// Square: 틱택토 칸 하나를 담당하는 컴포넌트
function Square() {
  return <button>?</button>;
}

// Board: 9개 칸을 담고 있는 게임판 컴포넌트
function Board() {
  return (
    <>
      <Square />
      <Square />
      <Square />
    </>
  );
}

// Board를 앱의 루트 컴포넌트로 내보냄
export default Board;
```

**Step 2 — Square에 `value` Props 추가**

각 칸이 `'X'`, `'O'`, 또는 비어있음(`null`)을 표시해야 합니다. 어떤 값을 표시할지는 Board가 결정하고 Props로 내려줍니다.

```tsx
// Props 타입 정의
// value는 'X', 'O', 또는 null(비어있음) 세 가지 값 중 하나
interface SquareProps {
  value: string | null;
}

function Square({ value }: SquareProps) {
  // value가 null이면 빈 버튼, 'X'/'O'이면 해당 값을 표시
  return <button>{value}</button>;
}

function Board() {
  return (
    <>
      {/* Board가 각 칸의 초기값을 결정해서 Props로 전달 */}
      <Square value="X" />
      <Square value="O" />
      <Square value={null} />
    </>
  );
}
```

> **강사 안내**: "`string | null`은 Session 1에서 배운 Union 타입입니다. `null`은 '아직 아무것도 없음'을 명시적으로 표현합니다. `undefined` 대신 `null`을 쓰는 것이 의도를 더 명확하게 전달합니다."

**Step 3 — 9개 칸으로 확장 + CSS 스타일 추가**

실제 게임은 3×3 = 9개의 칸이 필요합니다. CSS도 함께 추가합니다.

`src/App.css`에 다음 스타일을 붙여넣기합니다.

```css
/* src/App.css */
* { box-sizing: border-box; }
body { font-family: sans-serif; margin: 20px; padding: 0; }

.board-row { display: flex; }

.square {
  background: #fff;
  border: 1px solid #999;
  font-size: 24px;
  font-weight: bold;
  line-height: 1;
  height: 60px;
  width: 60px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.square:hover { background: #f0f0f0; }

.status { margin-bottom: 10px; font-size: 18px; }
```

`src/App.tsx`에 CSS를 import하고 Board를 완성합니다.

```tsx
// src/App.tsx
import './App.css';

interface SquareProps {
  value: string | null;
}

function Square({ value }: SquareProps) {
  return <button className="square">{value}</button>;
}

function Board() {
  return (
    <>
      {/* 1행 */}
      <div className="board-row">
        <Square value="X" />
        <Square value="O" />
        <Square value="X" />
      </div>
      {/* 2행 */}
      <div className="board-row">
        <Square value="O" />
        <Square value="X" />
        <Square value="O" />
      </div>
      {/* 3행 */}
      <div className="board-row">
        <Square value="X" />
        <Square value={null} />
        <Square value="O" />
      </div>
    </>
  );
}

export default Board;
```

> **강사 안내**: "지금 화면에 3×3 게임판이 보입니다. 버튼을 클릭해도 아무 일이 일어나지 않고, 값이 하드코딩되어 있습니다. 이제 Step 4부터 직접 타이핑해서 이 게임을 실제로 동작하게 만들겠습니다."

---

## 3. Tic-Tac-Toe: Guided Coding (35분)

> **강사 안내**: "이제부터 직접 타이핑하는 시간입니다. 강사가 한 단계씩 설명하면서 코드를 작성하면 학생들도 함께 타이핑합니다. 타이핑 속도보다 '왜 이렇게 하는가'를 이해하는 것이 목표입니다. 진도보다 이해를 우선합니다. 막히면 바로 질문하세요."

### 3.1 Step 4: 클릭 이벤트 연결 (5분)

버튼을 클릭하면 뭔가 일어나도록 만듭니다. 먼저 콘솔에 메시지를 출력해봅니다.

```tsx
function Square({ value }: SquareProps) {
  // 이벤트 핸들러 함수를 컴포넌트 안에 정의합니다
  function handleClick() {
    console.log('Square 클릭됨!');
  }

  return (
    // onClick 속성에 함수를 연결합니다
    // 주의: handleClick() 이 아니라 handleClick 입니다 (괄호 없음)
    <button className="square" onClick={handleClick}>
      {value}
    </button>
  );
}
```

> **강사 안내**: 이 부분에서 반드시 멈추고 강조합니다.

**가장 흔한 실수 — `onClick={handleClick()}` vs `onClick={handleClick}`**

```tsx
// ❌ 잘못된 방법 — 괄호가 있음
<button onClick={handleClick()}>

// 이것은 JSX가 렌더링될 때 즉시 handleClick()이 실행됩니다.
// React에 전달되는 것은 handleClick의 반환값(undefined)입니다.
// 클릭해도 아무 일이 일어나지 않거나, 심할 경우 무한 렌더링 오류가 납니다.

// ✅ 올바른 방법 — 괄호 없음
<button onClick={handleClick}>

// 이것은 "클릭되면 이 함수를 호출해"라고 함수 자체를 React에 전달합니다.
// 실제 클릭이 일어날 때만 실행됩니다.
```

**다른 언어와의 비교:**

```python
# Python에서 버튼 콜백 — 함수 객체를 전달 (실행 결과 x)
button.command = handle_click   # 함수 객체 (올바름)
button.command = handle_click() # 함수 실행 결과 (잘못됨)
```

React도 동일한 원리입니다. `onClick`에는 "나중에 실행할 함수"를 전달해야 합니다.

브라우저에서 각 버튼을 클릭하고 콘솔에 "Square 클릭됨!"이 출력되는지 확인합니다.

### 3.2 Step 5: Square에 State를 직접 추가해보기 (5분)

클릭할 때 X가 표시되도록 만들어봅니다. Square 자체에 State를 넣어보겠습니다.

```tsx
import { useState } from 'react';
import './App.css';

interface SquareProps {
  value: string | null;
}

function Square({ value }: SquareProps) {
  // 클릭 여부를 기억하는 State
  const [clicked, setClicked] = useState(false);

  function handleClick() {
    setClicked(true);
  }

  return (
    <button className="square" onClick={handleClick}>
      {clicked ? 'X' : null}
    </button>
  );
}
```

각 칸을 클릭하면 X가 표시됩니다.

> **강사 안내**: 여기서 잠시 멈추고 학생들에게 질문을 던집니다.

---

**[미니 퀴즈]** 지금 이 코드에서 실제 게임을 완성하려면 어떤 문제들이 남아 있을까요? 1분간 생각해봅시다.

*잠시 기다립니다. 손을 들거나 답변을 말하게 합니다.*

**문제점 목록:**

1. 모든 칸이 X만 표시합니다. O도 있어야 합니다.
2. **Board가 각 칸의 상태를 알 수 없습니다.** ← 이게 핵심 문제
3. Board가 전체 칸 상태를 모르니 승자를 판단할 수 없습니다.

두 번째 문제가 핵심입니다. 승자를 판단하려면 9개 칸의 상태를 **한꺼번에** 확인해야 합니다. 지금은 각 Square가 자신의 상태를 자기 안에만 갖고 있어서 Board가 확인할 방법이 없습니다.

이것이 바로 **State Lifting Up(상태 끌어올리기)**이 필요한 이유입니다.

---

### 3.3 Step 6: State Lifting Up — 핵심 패턴 (25분)

**상태 끌어올리기란?**

> 여러 자식 컴포넌트가 공유해야 하는 State는 그 자식들의 **공통 부모 컴포넌트**로 끌어올립니다.

```
Before — State가 각 Square에 흩어져 있음:
  Board
    Square[0] → State: clicked=true  (Board는 이 값을 모름)
    Square[1] → State: clicked=false (Board는 이 값을 모름)
    Square[2] → State: clicked=true  (Board는 이 값을 모름)
    ...

After — State를 Board로 끌어올림:
  Board → State: squares = ['X', null, 'O', null, 'X', ...]  ← Board가 전부 앎
    Square[0] (Board에서 value만 받아서 표시)
    Square[1]
    Square[2]
    ...
```

**구현 3단계:**

---

**1단계: Board에 9개 칸 상태를 관리하는 State 추가**

```tsx
function Board() {
  // 9개 칸의 값을 배열로 관리
  // Array(9).fill(null) = [null, null, null, null, null, null, null, null, null]
  const [squares, setSquares] = useState<(string | null)[]>(
    Array(9).fill(null)
  );

  // 누구 차례인지 State로 관리
  // true = X 차례, false = O 차례. 첫 번째 플레이어는 X
  const [xIsNext, setXIsNext] = useState(true);

  // ...
}
```

**`useState<(string | null)[]>` 타입 설명:**

```
(string | null)[]
      ↑ 요소 타입: string 또는 null
               ↑ 배열
```

`string | null` 요소들로 이루어진 배열입니다. 각 칸은 `'X'`, `'O'`, 또는 `null`(비어있음) 세 가지 값 중 하나입니다.

---

**2단계: Square의 Props 수정 — 클릭 핸들러도 Props로 받기**

Square 자체는 더 이상 State를 갖지 않습니다. 표시할 값과 클릭 시 호출할 함수를 모두 Board에서 받습니다.

```tsx
interface SquareProps {
  value: string | null;
  // 클릭 시 호출할 함수. 파라미터 없고, 반환값도 없는 함수 타입
  onSquareClick: () => void;
}

function Square({ value, onSquareClick }: SquareProps) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}
```

> **강사 안내**: "`onSquareClick: () => void`가 낯설게 보일 수 있습니다. `() => void`는 '파라미터 없이 호출되고 반환값이 없는 함수'의 타입입니다. 함수를 Props로 전달할 때 항상 이런 형태로 타입을 명시합니다."

---

**3단계: Board에서 클릭 핸들러 구현 + Square에 전달**

```tsx
function Board() {
  const [squares, setSquares] = useState<(string | null)[]>(
    Array(9).fill(null)
  );
  const [xIsNext, setXIsNext] = useState(true);

  // i번째 칸이 클릭되었을 때 호출되는 함수
  function handleClick(i: number) {
    // 이미 채워진 칸은 무시
    if (squares[i]) {
      return;
    }

    // ★ 불변성 — 기존 배열을 직접 수정하지 않고 복사본을 만듭니다
    const nextSquares = squares.slice(); // 배열 복사 (새 배열 생성)

    // 누구 차례인지에 따라 X 또는 O를 복사본에 설정
    nextSquares[i] = xIsNext ? 'X' : 'O';

    setSquares(nextSquares); // 복사본으로 State 업데이트
    setXIsNext(!xIsNext);   // 차례 전환 (X↔O)
  }

  return (
    <>
      <div className="board-row">
        {/* 각 Square에 해당 칸의 값과 클릭 핸들러를 Props로 전달 */}
        {/* () => handleClick(0) : "클릭되면 handleClick(0)을 실행하는 함수"를 전달 */}
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}
```

> **강사 안내**: "`() => handleClick(0)` 문법을 잠깐 설명합니다. `onSquareClick`은 파라미터 없는 함수를 기대합니다. 그런데 `handleClick`은 어느 칸인지 인덱스 `i`가 필요합니다. 그래서 `() => handleClick(0)`처럼 화살표 함수로 감쌉니다. 이 화살표 함수는 '호출되면 `handleClick(0)`을 실행하는 파라미터 없는 함수'입니다. 인자가 없는 핸들러라면 `onClick={handleClick}` 처럼 직접 전달할 수 있지만, 인자가 있을 때는 이렇게 감싸야 합니다."

**[실습 포인트]**: 코드를 저장하고 게임판을 클릭해봅니다. X와 O가 번갈아 표시되는지 확인합니다.

---

### 3.4 불변성(Immutability)이 중요한 이유

코드에서 `.slice()`로 배열을 복사한 뒤 수정했습니다. 왜 기존 배열을 직접 수정하면 안 될까요?

```tsx
// ❌ 잘못된 방법 — 기존 배열을 직접 수정 (Mutation)
function handleClick(i: number) {
  squares[i] = 'X';      // 배열을 직접 수정
  setSquares(squares);   // 동일한 배열 참조 → React가 변경을 감지 못함 → 재렌더링 없음
}

// ✅ 올바른 방법 — 새 배열 생성 후 수정 (Immutability)
function handleClick(i: number) {
  const nextSquares = squares.slice(); // 새 배열 생성
  nextSquares[i] = 'X';               // 새 배열을 수정
  setSquares(nextSquares);            // 새 배열로 State 업데이트 → 재렌더링
}
```

**왜 불변성이 중요한가 — 세 가지 이유:**

**이유 1: React의 변경 감지**

React는 State가 변경되었는지 판단할 때 `===` 참조 비교를 사용합니다. 기존 배열을 직접 수정하면 배열의 메모리 주소가 바뀌지 않아서 React가 "이전이랑 같은 배열이네, 변경 없음"으로 판단하고 화면을 갱신하지 않습니다.

```
Before mutation: squares → [메모리 주소 0x1234]
After  mutation: squares → [메모리 주소 0x1234] (같음!) → React: "변경 없음"

Before immutable: squares     → [메모리 주소 0x1234]
After  immutable: nextSquares → [메모리 주소 0x5678] (다름!) → React: "변경됨 → 재렌더링"
```

**이유 2: 히스토리 보존**

불변성을 지키면 과거 State가 그대로 남아 있습니다. 이후 Step 7(시간 여행)에서 "이전 수로 돌아가기" 기능을 구현할 수 있는 이유가 바로 이것입니다.

**이유 3: 디버깅 용이성**

이전 상태와 현재 상태를 별도로 유지하기 때문에 "어느 시점에 무엇이 바뀌었는가"를 추적하기 쉽습니다.

> **강사 안내**: "Python이나 Java 경험이 있으신 분들은 처음에 이게 어색합니다. 리스트 append 하면 되지 왜 복사하나 싶은 거죠. React에서는 State를 직접 수정(mutate)하지 않는 것이 매우 중요한 규칙입니다. 이것을 어기면 화면이 갱신이 안 되거나 예상치 못한 버그가 생깁니다."

**React에서 배열을 다루는 불변성 패턴 — 치트시트:**

```tsx
const arr = [1, 2, 3, 4, 5];

// ✅ 항목 추가 — spread 연산자
const added = [...arr, 6];            // [1, 2, 3, 4, 5, 6]

// ✅ 항목 삭제 — filter (새 배열 반환)
const removed = arr.filter(n => n !== 3);  // [1, 2, 4, 5]

// ✅ 항목 수정 — map (새 배열 반환)
const updated = arr.map(n => n === 3 ? 99 : n); // [1, 2, 99, 4, 5]

// ✅ 배열 복사 — slice() 또는 spread
const copy1 = arr.slice();  // [1, 2, 3, 4, 5] (새 배열)
const copy2 = [...arr];     // [1, 2, 3, 4, 5] (새 배열)

// ❌ 직접 수정 (React State에서 금지)
arr.push(6);    // 기존 배열 수정
arr.splice(2);  // 기존 배열 수정
arr[2] = 99;    // 기존 배열 수정
```

> **강사 안내**: "이 패턴들은 Session 5 Social Dashboard 실습에서 계속 사용됩니다. `filter`로 게시글 삭제, `map`으로 Todo 상태 토글, spread로 새 항목 추가. 꼭 기억해두세요."

---

### 3.5 승자 판정 로직 추가 (5분)

이제 게임의 핵심인 승자 판정 함수를 추가합니다.

```tsx
// Board 컴포넌트 밖에 정의합니다
// 이유: 컴포넌트 외부 상태에 의존하지 않는 순수 함수이므로
//       컴포넌트 재렌더링 시마다 재생성되지 않도록 밖에 둡니다
function calculateWinner(squares: (string | null)[]): string | null {
  // 이길 수 있는 모든 3칸 조합 (행 3개 + 열 3개 + 대각선 2개)
  const lines = [
    [0, 1, 2], // 1행
    [3, 4, 5], // 2행
    [6, 7, 8], // 3행
    [0, 3, 6], // 1열
    [1, 4, 7], // 2열
    [2, 5, 8], // 3열
    [0, 4, 8], // 우하향 대각선
    [2, 4, 6], // 좌하향 대각선
  ];

  for (const [a, b, c] of lines) {
    // 세 칸이 모두 같은 값이고 비어있지 않으면 승자
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a]; // 'X' 또는 'O' 반환
    }
  }

  return null; // 아직 승자 없음
}
```

Board에 승자 판정 UI를 추가합니다.

```tsx
function Board() {
  const [squares, setSquares] = useState<(string | null)[]>(
    Array(9).fill(null)
  );
  const [xIsNext, setXIsNext] = useState(true);

  function handleClick(i: number) {
    // 이미 승자가 있거나 칸이 채워진 경우 무시
    if (calculateWinner(squares) || squares[i]) {
      return;
    }

    const nextSquares = squares.slice();
    nextSquares[i] = xIsNext ? 'X' : 'O';
    setSquares(nextSquares);
    setXIsNext(!xIsNext);
  }

  // 매 렌더링마다 현재 상태를 계산 (State에서 파생되는 값)
  const winner = calculateWinner(squares);

  // 삼항 연산자로 상태 메시지 결정
  const status = winner
    ? `${winner}가 이겼습니다!`
    : `다음 플레이어: ${xIsNext ? 'X' : 'O'}`;

  return (
    <>
      {/* 상태 메시지 표시 */}
      <div className="status">{status}</div>

      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}
```

**[실습 포인트]**: 완성된 게임을 직접 플레이합니다. X와 O를 번갈아 클릭하면서 승자가 나오는지 확인합니다. 승자가 나온 뒤에는 클릭이 막히는지도 확인합니다.

---

### 3.6 최종 완성 코드 (전체)

```tsx
// src/App.tsx — Tic-Tac-Toe 완성 코드

import { useState } from 'react';
import './App.css';

// ===== 타입 정의 =====

interface SquareProps {
  value: string | null;
  onSquareClick: () => void;
}

// ===== 유틸리티 함수 =====

// 현재 squares 배열을 받아 승자('X' 또는 'O')를 반환하고, 없으면 null 반환
function calculateWinner(squares: (string | null)[]): string | null {
  const lines = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // 행
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // 열
    [0, 4, 8], [2, 4, 6],             // 대각선
  ];
  for (const [a, b, c] of lines) {
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

// ===== 컴포넌트 =====

// 칸 하나 컴포넌트 — value와 클릭 핸들러를 Props로 받음
function Square({ value, onSquareClick }: SquareProps) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

// 게임판 컴포넌트 — 모든 State를 여기서 관리
function Board() {
  // 9개 칸의 현재 값 배열
  const [squares, setSquares] = useState<(string | null)[]>(Array(9).fill(null));
  // 현재 차례: true = X, false = O
  const [xIsNext, setXIsNext] = useState(true);

  function handleClick(i: number) {
    // 승자가 이미 있거나 클릭한 칸이 이미 채워진 경우 무시
    if (calculateWinner(squares) || squares[i]) return;

    const nextSquares = squares.slice(); // 불변성: 복사본 생성
    nextSquares[i] = xIsNext ? 'X' : 'O';
    setSquares(nextSquares);
    setXIsNext(!xIsNext);
  }

  // State에서 파생되는 값 — State로 만들지 않고 매 렌더링마다 계산
  const winner = calculateWinner(squares);
  const status = winner
    ? `${winner}가 이겼습니다!`
    : `다음 플레이어: ${xIsNext ? 'X' : 'O'}`;

  return (
    <div style={{ padding: 20 }}>
      <h1>Tic-Tac-Toe</h1>
      <div className="status">{status}</div>
      {/* 3행 × 3열 = 9개 Square 렌더링 */}
      {[0, 3, 6].map((rowStart) => (
        <div key={rowStart} className="board-row">
          {[0, 1, 2].map((col) => (
            <Square
              key={rowStart + col}
              value={squares[rowStart + col]}
              onSquareClick={() => handleClick(rowStart + col)}
            />
          ))}
        </div>
      ))}
    </div>
  );
}

export default Board;
```

---

## 4. Step 7: 시간 여행 — 집에서 도전 (5분)

React 공식 튜토리얼의 마지막 단계는 **시간 여행(Time Travel)** 기능입니다. 이전 수로 되돌아갈 수 있게 만드는 기능입니다.

핵심 구조:

```tsx
// Game 컴포넌트가 이동 기록 전체를 관리
function Game() {
  // history[i]는 i번째 이동 시점의 squares 배열 스냅샷
  const [history, setHistory] = useState<(string | null)[][]>([
    Array(9).fill(null) // 초기 상태
  ]);
  const [currentMove, setCurrentMove] = useState(0);

  // 특정 이동 시점으로 돌아가기
  function jumpTo(move: number) {
    setCurrentMove(move);
  }
  // ...
}
```

이것이 가능한 이유가 바로 **불변성** 덕분입니다. 매번 새 배열을 만들었기 때문에 과거의 모든 상태가 그대로 보존되어 있습니다.

> **강사 안내**: "전체 구현은 React 공식 튜토리얼 `https://react.dev/learn/tutorial-tic-tac-toe`에 자세히 설명되어 있습니다. TypeScript 버전으로 포팅하는 것이 좋은 연습이 됩니다. 오늘 배운 불변성 개념의 실용적인 결과를 보여주는 기능이니 꼭 시도해보세요."

---

## Part A 미니 퀴즈 (5분)

> **강사 안내**: 다음 질문들을 하나씩 던집니다. 학생들이 손을 들거나 채팅으로 답하도록 합니다. 정답을 바로 말하지 말고 2~3명의 의견을 들은 뒤 설명합니다.

---

**퀴즈 1.** 다음 중 `useState`가 **필요한** 데이터는 무엇인가요?

```
① items 배열의 총 합계 (items.reduce로 계산 가능)
② 사용자가 입력 중인 검색어
③ 부모로부터 Props로 받은 사용자 이름
```

*정답: ②. 사용자 입력은 시간에 따라 바뀌고 화면에 즉시 반영되어야 하므로 State가 필요합니다. ①은 다른 State에서 계산 가능하므로 State 불필요. ③은 Props입니다.*

---

**퀴즈 2.** 다음 코드의 문제는 무엇인가요?

```tsx
function handleClick(i: number) {
  squares[i] = 'X';    // ← 여기
  setSquares(squares);
}
```

*정답: `squares` 배열을 직접 수정(mutate)합니다. 배열의 메모리 참조가 바뀌지 않아 React가 변경을 감지하지 못하고 화면을 갱신하지 않습니다. `squares.slice()`로 복사본을 만든 뒤 수정해야 합니다.*

---

**퀴즈 3.** State Lifting Up이 왜 필요했나요? 한 문장으로 설명해보세요.

*정답(예시): 각 Square가 자기 상태를 따로 갖고 있으면 Board가 전체 칸 상태를 볼 수 없어서 승자를 판단할 수 없기 때문에, State를 공통 부모인 Board로 끌어올렸습니다.*

---

# Part B: Thinking in React (1시간)

> **강사 안내**: "Part A에서 React의 핵심 메커니즘을 직접 체험했습니다. Part B는 한 걸음 물러서서 '어떻게 생각해야 하는가'를 배웁니다. React 공식 문서에서 'Thinking in React'라는 제목으로 소개하는 5단계 프로세스입니다. 이걸 익히면 앞으로 어떤 React UI를 만들든 어디서 시작해야 할지 알게 됩니다."

---

## 5. Thinking in React 개요 (5분)

### 5.1 왜 이 과정이 필요한가

React로 개발할 때 초보자를 가장 많이 막히게 하는 것은 문법이 아닙니다. 다음 질문들입니다.

- 이 UI를 몇 개의 컴포넌트로 나눠야 하는가?
- State는 몇 개 필요한가?
- State를 어느 컴포넌트에 두어야 하는가?
- 자식 컴포넌트에서 부모의 State를 어떻게 바꾸는가?

이 질문들에 체계적으로 답하는 방법이 **"Thinking in React" 5단계**입니다.

### 5.2 5단계 요약

| 단계 | 핵심 질문 | 우리 예제에서 |
|------|-----------|--------------|
| Step 1: 컴포넌트 분해 | UI를 어떻게 나눌 것인가? | 5개 컴포넌트로 분해 |
| Step 2: 정적 버전 | Props만으로 UI를 만들 수 있는가? | State 없이 UI 완성 |
| Step 3: 최소 State | 어떤 데이터가 진짜 State인가? | 검색어, 체크 여부만 State |
| Step 4: State 위치 | 어느 컴포넌트에 State를 두는가? | 공통 부모에 State 배치 |
| Step 5: 역방향 흐름 | 자식이 어떻게 부모 State를 바꾸는가? | Callback Props 전달 |

### 5.3 예제 소개: 상품 검색 필터 UI

우리가 구현할 UI입니다. React 공식 문서(https://react.dev/learn/thinking-in-react)와 동일한 예제를 TypeScript로 작성합니다.

```
┌──────────────────────────────────────┐
│  검색: [__________________________]  │
│  ☑ 재고 있는 상품만 보기              │
│                                      │
│  이름              가격              │
│  ─────────────────────────────────   │
│  과일                                │
│  사과              ₩1,500           │
│  용과              품절              │
│                                      │
│  채소                                │
│  시금치            ₩2,000           │
│  호박              ₩3,000           │
└──────────────────────────────────────┘
```

검색창에 "사과"를 입력하면 사과만 표시됩니다. 체크박스를 켜면 재고 없는 상품(용과)이 사라집니다.

---

## 6. Step 1: UI를 컴포넌트 계층으로 분해하기 (10분)

### 6.1 컴포넌트를 나누는 기준

> **강사 안내**: 화이트보드나 슬라이드에 UI 스케치를 직접 그리면서 컴포넌트 경계를 손으로 그려나갑니다. "이 부분은 왜 별도 컴포넌트인가요?"라고 학생들에게 물어보면서 진행합니다.

컴포넌트를 나누는 기준은 **단일 책임 원칙(Single Responsibility Principle)**입니다.

> "하나의 컴포넌트는 하나의 일만 해야 한다."

소프트웨어 설계의 SRP와 동일한 원칙입니다. 컴포넌트가 너무 많은 일을 하면 더 작은 컴포넌트들로 쪼개야 합니다.

```
┌── FilterableProductTable ───────────────────────────────┐
│                                                         │
│  ┌── SearchBar ─────────────────────────────────────┐  │
│  │  검색: [__________________________]              │  │
│  │  ☑ 재고 있는 상품만 보기                          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌── ProductTable ──────────────────────────────────┐  │
│  │  이름              가격                          │  │
│  │  ┌── ProductCategoryRow ─────────────────────┐  │  │
│  │  │  과일                                     │  │  │
│  │  └───────────────────────────────────────────┘  │  │
│  │  ┌── ProductRow ─────────────────────────────┐  │  │
│  │  │  사과              ₩1,500                │  │  │
│  │  └───────────────────────────────────────────┘  │  │
│  │  ┌── ProductRow ─────────────────────────────┐  │  │
│  │  │  용과              품절                   │  │  │
│  │  └───────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**컴포넌트 계층 구조:**

```
FilterableProductTable   ← 전체를 감싸는 최상위 컴포넌트
  ├── SearchBar          ← 검색창 + 체크박스
  └── ProductTable       ← 상품 목록 테이블
        ├── ProductCategoryRow  ← 카테고리 헤더 (과일, 채소)
        └── ProductRow          ← 상품 한 줄
```

---

## 7. Step 2: 정적 버전 먼저 만들기 (15분)

### 7.1 정적 버전이란

"정적 버전"은 **State 없이 Props만으로 UI를 완성**하는 버전입니다. 검색창에 타이핑하거나 체크박스를 눌러도 아무것도 바뀌지 않지만, 화면이 올바르게 표시됩니다.

**왜 정적 버전을 먼저 만드는가?**

State와 이벤트를 동시에 고민하면 복잡해집니다. 먼저 "어떻게 보여야 하는가(UI)"를 해결하고, 그 다음에 "어떻게 상호작용하는가(동작)"를 해결합니다. 컴포넌트 구조가 맞는지 빠르게 검증할 수도 있습니다.

### 7.2 타입 정의 먼저

```tsx
// src/App.tsx 상단

interface Product {
  category: string; // 카테고리 (예: '과일', '채소')
  price: string;    // 가격 문자열 (예: '₩1,500', '품절')
  stocked: boolean; // 재고 여부
  name: string;     // 상품 이름
}
```

### 7.3 정적 버전 전체 코드

```tsx
// src/App.tsx — 정적 버전 (State 없음)

import './App.css';

interface Product {
  category: string;
  price: string;
  stocked: boolean;
  name: string;
}

// 원본 데이터 — 실제 앱에서는 API에서 받아옵니다
const PRODUCTS: Product[] = [
  { category: '과일', price: '₩1,500', stocked: true,  name: '사과'   },
  { category: '과일', price: '품절',   stocked: false, name: '용과'   },
  { category: '채소', price: '₩2,000', stocked: true,  name: '시금치' },
  { category: '채소', price: '₩3,000', stocked: true,  name: '호박'   },
];

// ── 카테고리 헤더 컴포넌트 ──────────────────────────────

interface ProductCategoryRowProps {
  category: string;
}

function ProductCategoryRow({ category }: ProductCategoryRowProps) {
  return (
    <tr>
      {/* colSpan={2}: 이름 열과 가격 열에 걸쳐서 표시 */}
      <th colSpan={2} style={{ textAlign: 'left', paddingTop: 12 }}>
        {category}
      </th>
    </tr>
  );
}

// ── 상품 한 줄 컴포넌트 ────────────────────────────────

interface ProductRowProps {
  product: Product;
}

function ProductRow({ product }: ProductRowProps) {
  // 재고 없는 상품은 이름을 빨간색으로 표시
  const nameElement = product.stocked
    ? product.name
    : <span style={{ color: 'red' }}>{product.name}</span>;

  return (
    <tr>
      <td>{nameElement}</td>
      <td>{product.price}</td>
    </tr>
  );
}

// ── 상품 목록 테이블 컴포넌트 ──────────────────────────

interface ProductTableProps {
  products: Product[];
}

function ProductTable({ products }: ProductTableProps) {
  // React.ReactNode: JSX, string, number, null 등 렌더링 가능한 모든 것
  const rows: React.ReactNode[] = [];
  let lastCategory: string | null = null;

  products.forEach((product) => {
    // 새 카테고리가 시작되면 카테고리 헤더를 먼저 추가
    if (product.category !== lastCategory) {
      rows.push(
        <ProductCategoryRow
          key={product.category}    // key는 같은 목록 안에서 유일해야 함
          category={product.category}
        />
      );
      lastCategory = product.category;
    }
    // 상품 행 추가
    rows.push(
      <ProductRow
        key={product.name}  // 이름이 유일한 식별자라고 가정
        product={product}
      />
    );
  });

  return (
    <table>
      <thead>
        <tr>
          <th style={{ textAlign: 'left' }}>이름</th>
          <th style={{ textAlign: 'left' }}>가격</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}

// ── 검색창 컴포넌트 ────────────────────────────────────

function SearchBar() {
  return (
    <form>
      <input type="text" placeholder="검색..." />
      <label style={{ display: 'block', marginTop: 8 }}>
        <input type="checkbox" />
        {' '}재고 있는 상품만 보기
      </label>
    </form>
  );
}

// ── 최상위 컴포넌트 ────────────────────────────────────

function FilterableProductTable() {
  return (
    <div style={{ padding: 20 }}>
      <SearchBar />
      <ProductTable products={PRODUCTS} />
    </div>
  );
}

export default FilterableProductTable;
```

> **강사 안내**: "이 코드를 실행하면 상품 목록이 표시됩니다. 검색창에 타이핑하거나 체크박스를 눌러도 아무것도 바뀌지 않습니다. 완전히 정상입니다. 이제 Step 3–5에서 State와 상호작용을 추가하겠습니다."

---

## 8. Step 3: 최소한의 State 찾기 (10분)

### 8.1 어떤 데이터가 State인가

State는 최소한으로 유지해야 합니다. 이걸 **DRY(Don't Repeat Yourself) 원칙**이라고도 합니다. 불필요한 State는 버그를 만들고 관리를 복잡하게 합니다.

**State가 아닌 것의 세 가지 기준:**

1. **시간이 지나도 변하지 않는가?** → State 불필요 (상수)
2. **부모에게서 Props로 받는가?** → State 불필요 (Props를 그대로 사용)
3. **다른 State나 Props로 계산할 수 있는가?** → State 불필요 (파생값은 계산으로)

**우리 예제의 모든 데이터 분석:**

| 데이터 | State인가? | 이유 |
|--------|-----------|------|
| 상품 목록 원본 | ❌ 아님 | 외부에서 받는 고정 데이터 (Props 또는 상수) |
| 검색어 (`filterText`) | ✅ 맞음 | 사용자 입력으로 변하고, 이것으로 UI가 달라짐 |
| 재고 필터 체크 여부 (`inStockOnly`) | ✅ 맞음 | 사용자 행동으로 변하고, 이것으로 UI가 달라짐 |
| 필터링된 상품 목록 | ❌ 아님 | 원본 + 검색어 + 체크 여부로 **계산 가능** |

**필터된 목록이 왜 State가 아닌지 — 코드로 비교:**

```tsx
// ❌ 중복 State — 나쁜 예
// filterText가 바뀔 때마다 filteredProducts도 수동으로 업데이트해야 함
// 둘이 sync가 안 맞으면 버그 발생
const [filterText, setFilterText] = useState('');
const [inStockOnly, setInStockOnly] = useState(false);
const [filteredProducts, setFilteredProducts] = useState(PRODUCTS); // 불필요!

// ✅ 파생값으로 계산 — 좋은 예
// filterText나 inStockOnly가 바뀌면 컴포넌트가 재렌더링되고
// filteredProducts는 자동으로 올바른 값으로 계산됨
const [filterText, setFilterText] = useState('');
const [inStockOnly, setInStockOnly] = useState(false);

// State에서 파생 — 매 렌더링마다 자동으로 최신 값을 계산
const filteredProducts = PRODUCTS.filter(product => {
  if (inStockOnly && !product.stocked) return false;
  if (!product.name.toLowerCase().includes(filterText.toLowerCase())) return false;
  return true;
});
```

**결론: State는 딱 두 개입니다.**

```tsx
const [filterText, setFilterText] = useState('');    // 검색어
const [inStockOnly, setInStockOnly] = useState(false); // 재고 필터
```

---

## 9. Step 4: State가 어디에 있어야 하는가 (5분)

### 9.1 State 위치 결정 규칙

> **규칙**: State는 그것을 필요로 하는 **모든 컴포넌트의 공통 부모**에 위치해야 합니다.

`filterText`와 `inStockOnly`를 누가 필요로 하는가?

- **`SearchBar`**: 입력창과 체크박스의 현재 값을 표시해야 합니다 (제어 컴포넌트 패턴)
- **`ProductTable`**: 상품을 필터링하여 표시해야 합니다

```
FilterableProductTable  ← SearchBar와 ProductTable의 공통 부모
  ├── SearchBar          (filterText, inStockOnly를 받아 표시)
  └── ProductTable       (filterText, inStockOnly를 받아 필터링)
```

두 컴포넌트의 공통 부모는 `FilterableProductTable`이므로, State는 거기에 위치합니다.

---

## 10. Step 5: 역방향 데이터 흐름 추가 (20분)

### 10.1 문제 인식

지금까지 데이터 흐름은 단방향이었습니다.

```
FilterableProductTable (State 보유)
  ↓ Props (filterText, inStockOnly 전달)
SearchBar (Props 값을 표시만 함)
```

그런데 사용자가 SearchBar에서 타이핑하면 FilterableProductTable의 State가 변경되어야 합니다. 이것이 **역방향 데이터 흐름(Inverse Data Flow)**입니다.

### 10.2 React 데이터 흐름의 원칙

React의 데이터 흐름은 항상 **부모 → 자식** (단방향)입니다. 자식이 부모의 State를 직접 수정하는 방법은 없습니다.

대신 **부모가 State 변경 함수를 자식에게 Props로 전달**합니다.

```
부모: "내 State를 바꾸고 싶으면 이 함수를 호출해"
  → 자식: (사용자 입력 시) 부모가 준 함수를 호출
    → 부모의 State 변경 → 재렌더링 → 자식이 새 값으로 갱신됨
```

### 10.3 Callback Props 패턴 구현

**SearchBar Props에 변경 함수 추가:**

```tsx
interface SearchBarProps {
  filterText: string;
  inStockOnly: boolean;
  // 부모에서 내려주는 변경 함수들 — 이름은 관례적으로 on~ 으로 시작
  onFilterTextChange: (value: string) => void;    // string을 받아 반환값 없음
  onInStockOnlyChange: (value: boolean) => void;  // boolean을 받아 반환값 없음
}

function SearchBar({
  filterText,
  inStockOnly,
  onFilterTextChange,
  onInStockOnlyChange,
}: SearchBarProps) {
  return (
    <form>
      <input
        type="text"
        placeholder="검색..."
        // value를 State와 연결 — 제어 컴포넌트 패턴
        value={filterText}
        // 타이핑할 때마다 부모의 State 변경 함수를 호출
        onChange={(e) => onFilterTextChange(e.target.value)}
      />
      <label style={{ display: 'block', marginTop: 8 }}>
        <input
          type="checkbox"
          // checked를 State와 연결 — 체크박스는 value가 아닌 checked 사용
          checked={inStockOnly}
          // 체크/언체크할 때마다 부모의 State 변경 함수를 호출
          onChange={(e) => onInStockOnlyChange(e.target.checked)}
        />
        {' '}재고 있는 상품만 보기
      </label>
    </form>
  );
}
```

> **강사 안내**: "여기서 두 가지를 주목해주세요. 첫째, `<input value={filterText} ...>`처럼 `value`를 State와 연결하는 것을 '제어 컴포넌트(Controlled Component)' 패턴이라고 합니다. 잠시 후 자세히 설명하겠습니다. 둘째, 체크박스는 `value` 대신 `checked`를 사용합니다. `value`와 `checked`를 혼동하면 동작이 안 되는 흔한 실수입니다."

**ProductTable Props에 필터 조건 추가:**

```tsx
interface ProductTableProps {
  products: Product[];
  filterText: string;   // 검색어
  inStockOnly: boolean; // 재고 필터 여부
}

function ProductTable({ products, filterText, inStockOnly }: ProductTableProps) {
  const rows: React.ReactNode[] = [];
  let lastCategory: string | null = null;

  products.forEach((product) => {
    // Step 3에서 결정: 필터된 목록은 State가 아니라 여기서 계산
    // 재고 필터: inStockOnly가 true이고 재고 없는 상품은 건너뜀
    if (inStockOnly && !product.stocked) return;
    // 검색어 필터: 이름에 검색어가 포함되지 않으면 건너뜀 (대소문자 무시)
    if (!product.name.toLowerCase().includes(filterText.toLowerCase())) return;

    if (product.category !== lastCategory) {
      rows.push(
        <ProductCategoryRow key={product.category} category={product.category} />
      );
      lastCategory = product.category;
    }
    rows.push(<ProductRow key={product.name} product={product} />);
  });

  return (
    <table>
      <thead>
        <tr>
          <th style={{ textAlign: 'left' }}>이름</th>
          <th style={{ textAlign: 'left' }}>가격</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}
```

**FilterableProductTable에 State 추가 및 모든 것 연결:**

```tsx
function FilterableProductTable() {
  // Step 3에서 결정한 딱 두 개의 State
  const [filterText, setFilterText] = useState('');
  const [inStockOnly, setInStockOnly] = useState(false);

  return (
    <div style={{ padding: 20 }}>
      <SearchBar
        filterText={filterText}
        inStockOnly={inStockOnly}
        onFilterTextChange={setFilterText}      // setFilterText 함수 자체를 전달
        onInStockOnlyChange={setInStockOnly}    // setInStockOnly 함수 자체를 전달
      />
      <ProductTable
        products={PRODUCTS}
        filterText={filterText}
        inStockOnly={inStockOnly}
      />
    </div>
  );
}
```

> **강사 안내**: "`onFilterTextChange={setFilterText}`를 보면, `setFilterText` 함수 자체를 Props로 전달합니다. SearchBar에서 `onFilterTextChange('사과')`를 호출하면 실제로는 `setFilterText('사과')`가 실행됩니다. 부모의 State 변경 함수를 자식이 호출하는 구조입니다."

**[실습 포인트]**: 완성된 코드를 실행합니다. 검색창에 '사과'를 입력하거나 체크박스를 켜고 끄면서 목록이 실시간으로 필터링되는지 확인합니다.

---

### 10.4 제어 컴포넌트(Controlled Component) 패턴

`SearchBar`의 input은 **제어 컴포넌트** 패턴을 사용합니다.

```tsx
<input
  type="text"
  value={filterText}       // ← State가 현재 값을 결정
  onChange={(e) => onFilterTextChange(e.target.value)}  // ← 변경 시 State 업데이트
/>
```

**`value={filterText}` 없이 `onChange`만 있으면?**

```tsx
// 비제어 컴포넌트 — React가 값을 관리하지 않음
<input type="text" onChange={(e) => setFilterText(e.target.value)} />
// 타이핑은 되지만 React State와 연결이 느슨함
// 프로그래밍 방식으로 값을 설정하거나 초기화하기 어려움
```

**`value={filterText}`만 있고 `onChange`가 없으면?**

```tsx
// 읽기 전용 — 타이핑해도 값이 바뀌지 않음 (React가 State 값으로 덮어씀)
<input type="text" value={filterText} />
// React 경고: "You provided a `value` prop to a form field without an `onChange` handler."
```

**둘 다 있어야 완전한 제어 컴포넌트:**

```tsx
// 완전한 제어 컴포넌트
<input
  type="text"
  value={filterText}      // State → input (단방향)
  onChange={(e) => setFilterText(e.target.value)} // input → State (역방향)
/>
// 두 방향이 모두 연결되어야 합니다
```

### 10.5 이벤트 객체 타입 이해

```tsx
// text input의 onChange
onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
  e.target.value   // string — 현재 input 값
  e.target.checked // boolean — 체크박스 여부 (checkbox에서 사용)
}}

// button의 onClick
onClick={(e: React.MouseEvent<HTMLButtonElement>) => {
  e.preventDefault() // 기본 동작(폼 제출 등) 방지
}}

// form의 onSubmit
onSubmit={(e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault() // 페이지 새로고침 방지
}}
```

> **강사 안내**: "이 타입들을 외울 필요는 없습니다. VS Code에서 `onChange={(e) => ...}` 처럼 작성하면 `e` 위에 커서를 올렸을 때 타입이 표시됩니다. TypeScript가 이미 JSX 문맥에서 타입을 자동으로 추론합니다. 오류가 나면 오류 메시지가 올바른 타입을 알려줍니다."

---

### 10.6 최종 완성 코드 (전체)

```tsx
// src/App.tsx — Thinking in React 완성 코드

import { useState } from 'react';

// ===== 타입 =====

interface Product {
  category: string;
  price: string;
  stocked: boolean;
  name: string;
}

// ===== 원본 데이터 =====

const PRODUCTS: Product[] = [
  { category: '과일', price: '₩1,500', stocked: true,  name: '사과'   },
  { category: '과일', price: '품절',   stocked: false, name: '용과'   },
  { category: '채소', price: '₩2,000', stocked: true,  name: '시금치' },
  { category: '채소', price: '₩3,000', stocked: true,  name: '호박'   },
];

// ===== 컴포넌트 =====

function ProductCategoryRow({ category }: { category: string }) {
  return (
    <tr>
      <th colSpan={2} style={{ textAlign: 'left', paddingTop: 12 }}>
        {category}
      </th>
    </tr>
  );
}

function ProductRow({ product }: { product: Product }) {
  const nameElement = product.stocked
    ? product.name
    : <span style={{ color: 'red' }}>{product.name}</span>;
  return (
    <tr>
      <td>{nameElement}</td>
      <td>{product.price}</td>
    </tr>
  );
}

interface ProductTableProps {
  products: Product[];
  filterText: string;
  inStockOnly: boolean;
}

function ProductTable({ products, filterText, inStockOnly }: ProductTableProps) {
  const rows: React.ReactNode[] = [];
  let lastCategory: string | null = null;

  products.forEach((product) => {
    if (inStockOnly && !product.stocked) return;
    if (!product.name.toLowerCase().includes(filterText.toLowerCase())) return;

    if (product.category !== lastCategory) {
      rows.push(<ProductCategoryRow key={product.category} category={product.category} />);
      lastCategory = product.category;
    }
    rows.push(<ProductRow key={product.name} product={product} />);
  });

  return (
    <table>
      <thead>
        <tr>
          <th style={{ textAlign: 'left' }}>이름</th>
          <th style={{ textAlign: 'left' }}>가격</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}

interface SearchBarProps {
  filterText: string;
  inStockOnly: boolean;
  onFilterTextChange: (value: string) => void;
  onInStockOnlyChange: (value: boolean) => void;
}

function SearchBar({
  filterText,
  inStockOnly,
  onFilterTextChange,
  onInStockOnlyChange,
}: SearchBarProps) {
  return (
    <form>
      <input
        type="text"
        placeholder="검색..."
        value={filterText}
        onChange={(e) => onFilterTextChange(e.target.value)}
      />
      <label style={{ display: 'block', marginTop: 8 }}>
        <input
          type="checkbox"
          checked={inStockOnly}
          onChange={(e) => onInStockOnlyChange(e.target.checked)}
        />
        {' '}재고 있는 상품만 보기
      </label>
    </form>
  );
}

function FilterableProductTable() {
  const [filterText, setFilterText] = useState('');
  const [inStockOnly, setInStockOnly] = useState(false);

  return (
    <div style={{ padding: 20 }}>
      <h1>상품 검색</h1>
      <SearchBar
        filterText={filterText}
        inStockOnly={inStockOnly}
        onFilterTextChange={setFilterText}
        onInStockOnlyChange={setInStockOnly}
      />
      <ProductTable
        products={PRODUCTS}
        filterText={filterText}
        inStockOnly={inStockOnly}
      />
    </div>
  );
}

export default FilterableProductTable;
```

---

## 11. Social Dashboard와의 연결 (5분)

> **강사 안내**: "오늘 배운 내용이 어떻게 Session 5 Social Dashboard 실습에 쓰이는지 연결해서 설명합니다. '아, 그래서 이걸 배웠구나'를 느끼게 하는 중요한 순간입니다."

### 11.1 오늘 배운 패턴 → Social Dashboard 적용

| 오늘 배운 패턴 | Social Dashboard에서 사용하는 방식 |
|---------------|----------------------------------|
| `useState` + 초기값 `null` / `[]` | 사용자 목록, 게시글 목록을 `null` 또는 빈 배열로 초기화 |
| `onClick` 이벤트 핸들러 | 버튼 클릭으로 게시글 삭제, Todo 토글 |
| 불변성 — `filter` | 특정 ID의 게시글 삭제: `posts.filter(p => p.id !== id)` |
| 불변성 — `map` | Todo 완료 토글: `todos.map(t => t.id === id ? {...t, completed: !t.completed} : t)` |
| 불변성 — `spread` | 새 게시글 추가: `[newPost, ...posts]` |
| State Lifting Up | 여러 섹션에서 공유하는 선택된 사용자 ID 관리 |
| Callback Props | 하위 컴포넌트(PostList)에서 상위 컴포넌트(App)의 State 변경 |
| 제어 컴포넌트 | 게시글 작성 폼의 입력값 관리 |

**예시: Social Dashboard의 게시글 삭제 — 오늘 배운 패턴 그대로**

```tsx
// Board.handleClick과 동일한 패턴
function App() {
  const [posts, setPosts] = useState<Post[]>([]);

  // 불변성 — filter로 새 배열 생성 (직접 수정 금지)
  function handleDeletePost(postId: number) {
    const updatedPosts = posts.filter(post => post.id !== postId);
    setPosts(updatedPosts);
  }

  return (
    // Callback Props — 삭제 함수를 하위 컴포넌트에 전달
    <PostList
      posts={posts}
      onDeletePost={handleDeletePost}
    />
  );
}
```

**Session 5에서 새로 추가되는 것:**

- **`useEffect`**: "컴포넌트가 화면에 나타난 직후" API를 호출하는 훅
- **`fetch`**: JSONPlaceholder API에서 실제 데이터를 받아오는 Web API

나머지는 오늘 배운 패턴 그대로입니다. API에서 받은 데이터를 State에 저장하고, State가 바뀌면 화면이 갱신됩니다.

---

## 12. 트러블슈팅 & 자주 하는 실수

### 오류 1: `onClick={handleClick()}` — 이벤트 핸들러가 즉시 실행됨

**증상**: 컴포넌트가 렌더링될 때 핸들러가 자동으로 실행되거나, 무한 렌더링 오류가 납니다.

```
Warning: Cannot update a component while rendering a different component
```

**원인과 해결:**

```tsx
// ❌ 괄호 있음 — 렌더링 시 즉시 실행
<button onClick={handleClick()}>클릭</button>

// ✅ 괄호 없음 — 클릭 시 실행
<button onClick={handleClick}>클릭</button>

// ✅ 인자가 필요한 경우 — 화살표 함수로 감싸기
<button onClick={() => handleClick(id)}>클릭</button>
```

---

### 오류 2: State 직접 수정 — 화면이 갱신되지 않음

**증상**: 함수를 호출해도 화면이 바뀌지 않습니다.

**원인과 해결:**

```tsx
// ❌ 배열 직접 수정
const [items, setItems] = useState(['a', 'b', 'c']);

function addItem() {
  items.push('d');    // 기존 배열 직접 수정 (참조 불변)
  setItems(items);    // 같은 참조 → React가 변경 감지 못함
}

// ✅ 새 배열 생성
function addItem() {
  setItems([...items, 'd']); // 새 배열 → React가 변경 감지
}

// ❌ 객체 직접 수정
const [user, setUser] = useState({ name: '김철수', age: 25 });

function updateAge() {
  user.age = 26;      // 직접 수정
  setUser(user);      // 같은 참조 → 재렌더링 없음
}

// ✅ 새 객체 생성
function updateAge() {
  setUser({ ...user, age: 26 }); // spread로 복사 후 수정
}
```

---

### 오류 3: `Type 'string | null' is not assignable to type 'string'`

**증상**: `null`을 허용하는 값에서 타입 오류

**원인과 해결:**

```tsx
// ❌ null을 받을 수 없는 타입
interface SquareProps {
  value: string; // null 불허
}

// ✅ Union 타입으로 null 허용
interface SquareProps {
  value: string | null; // null 허용
}
```

---

### 오류 4: 체크박스에 `checked` 대신 `value` 사용

**증상**: 체크박스의 체크 상태가 UI에 반영되지 않습니다.

**원인과 해결:**

```tsx
// ❌ 체크박스에 value — 체크 여부와 무관
<input type="checkbox" value={inStockOnly} />

// ✅ 체크박스에 checked — 체크 여부를 제어
<input type="checkbox" checked={inStockOnly} onChange={(e) => setInStockOnly(e.target.checked)} />
// e.target.value → 폼 제출 시 전달할 문자열값 (기본 "on")
// e.target.checked → 체크 여부 (true/false)
```

---

### 오류 5: 제어 컴포넌트에서 `value` 없이 `onChange`만 쓰거나, `onChange` 없이 `value`만 쓰는 경우

**증상 1**: `onChange`만 있고 `value`가 없으면 — 비제어 컴포넌트처럼 동작. 프로그래밍 방식으로 값 초기화 불가.

**증상 2**: `value`만 있고 `onChange`가 없으면 — 타이핑해도 값이 변하지 않음. React 경고 발생.

```
Warning: You provided a `value` prop to a form field without an `onChange` handler.
```

**해결**: 반드시 `value`와 `onChange`를 쌍으로 사용합니다.

```tsx
// ✅ 완전한 제어 컴포넌트
<input
  type="text"
  value={filterText}
  onChange={(e) => setFilterText(e.target.value)}
/>
```

---

### 오류 6: State 업데이트의 비동기 특성 — setState 직후 값 읽기

**증상**: `setState` 직후 같은 함수에서 State를 읽으면 이전 값이 나옵니다.

```tsx
const [count, setCount] = useState(0);

function handleClick() {
  setCount(count + 1);
  console.log(count); // 0 출력! (업데이트된 1이 아님)
  // React는 setState를 즉시 처리하지 않고 배치(batch) 처리함
}
```

**해결:**

```tsx
// 계산된 값을 변수에 저장해서 사용
function handleClick() {
  const nextCount = count + 1;
  setCount(nextCount);
  console.log(nextCount); // 1 출력 (올바름)
}

// 또는 함수형 업데이트 — 이전 State 기반으로 업데이트할 때 권장
function handleClick() {
  setCount(prev => prev + 1); // prev는 항상 최신 State
}
```

---

### 오류 7: `key` prop 경고

**증상**: 콘솔에 다음 경고가 출력됩니다.

```
Warning: Each child in a list should have a unique "key" prop.
```

**원인과 해결:**

```tsx
// ❌ key 없음
products.forEach((product) => {
  rows.push(<ProductRow product={product} />);
});

// ✅ 유일한 key 추가
products.forEach((product) => {
  rows.push(<ProductRow key={product.name} product={product} />);
});
```

`key`는 같은 목록 안에서만 유일하면 됩니다. 안정적인 식별자(DB ID, 유일한 이름 등)를 사용합니다. 배열 인덱스는 항목 순서가 바뀔 때 문제를 일으킬 수 있어 가급적 피합니다.

---

### 오류 8: `calculateWinner`를 컴포넌트 안에 정의한 경우

**증상**: 기능상 문제는 없지만, 컴포넌트 재렌더링마다 함수가 새로 생성됩니다.

**원인과 해결:**

```tsx
// 비효율적 — 렌더링마다 새 함수 생성
function Board() {
  function calculateWinner(squares) { ... } // 안에 정의
  // ...
}

// 권장 — 컴포넌트 밖에 정의 (한 번만 생성)
function calculateWinner(squares) { ... } // 밖에 정의

function Board() {
  // ...
}
```

컴포넌트 외부 State나 Props에 의존하지 않는 순수 함수는 컴포넌트 밖에 정의합니다.

---

### 오류 9: Callback Props의 타입 정의 오류

**증상**: 함수를 Props로 전달할 때 타입 오류

**원인과 해결:**

```tsx
// ❌ 함수 타입 잘못 정의
interface SearchBarProps {
  onFilterTextChange: string;      // 함수가 아닌 string으로 잘못 정의
  onInStockOnlyChange: Function;   // 너무 느슨한 타입
}

// ✅ 정확한 함수 타입 정의
interface SearchBarProps {
  onFilterTextChange: (value: string) => void;  // string 받고 반환값 없음
  onInStockOnlyChange: (value: boolean) => void; // boolean 받고 반환값 없음
}
```

---

### 오류 10: State Lifting Up 후 Props 개수가 너무 많아지는 "Props Drilling"

**증상**: State를 공통 부모로 올렸더니 여러 단계를 거쳐 Props를 내려야 합니다.

```
A (State 보유)
  └── B (직접 안 씀, C에 전달만)
        └── C (직접 안 씀, D에 전달만)
              └── D (실제로 사용)
```

**설명**: 이를 "Props Drilling"이라고 합니다. 오늘 수준에서는 허용 범위입니다. 나중에 Context API 또는 Zustand 같은 전역 상태 관리 도구로 해결합니다. 지금은 "이런 문제가 있다"는 것을 인지하는 것으로 충분합니다.

---

## 13. Q&A 예상 질문과 답변

**Q1.** `useState`를 컴포넌트 밖에서 선언하면 안 되나요?

A: `useState`는 React 함수형 컴포넌트의 최상위 레벨에서만 호출해야 합니다. 컴포넌트 밖에서 호출하면 즉시 오류가 납니다. 이 규칙을 "Rules of Hooks"라고 하며, `if` 문이나 반복문 안에서도 훅을 호출할 수 없습니다.

```tsx
// ❌ 컴포넌트 밖 — 오류
const [count, setCount] = useState(0);

function Counter() {
  // ❌ if 문 안 — 오류 (훅 호출 순서가 렌더링마다 달라질 수 있음)
  if (show) {
    const [value, setValue] = useState('');
  }

  // ✅ 컴포넌트 최상위 레벨 — 올바름
  const [count, setCount] = useState(0);
}
```

---

**Q2.** `const [count, setCount] = useState(0)`에서 `count`가 바뀌는데 왜 `const`를 쓰나요?

A: `count`라는 변수 자체가 재할당되는 것이 아닙니다. `setCount(1)`을 호출하면 React가 컴포넌트 함수를 새로 실행합니다. 새 실행에서 `useState`는 업데이트된 값인 1을 반환하고, 그것이 새 `const count = 1`에 할당됩니다. 이전 `count = 0`은 이미 사라진 이전 렌더링의 것입니다. 매 렌더링은 독립적인 스냅샷이므로 `const`가 맞습니다.

---

**Q3.** State가 바뀌면 컴포넌트 전체 함수가 다시 실행되나요? 성능이 괜찮나요?

A: 맞습니다. State가 바뀌면 해당 컴포넌트와 그 자식들 전체가 다시 실행됩니다. 다만 React는 Virtual DOM 비교(Diffing)를 통해 실제 DOM 변경은 최소화합니다. 컴포넌트 함수를 다시 실행하는 것 자체는 매우 빠른 JavaScript 연산입니다. 대부분의 앱에서 이것이 성능 문제가 되지는 않습니다. 성능 최적화가 필요한 경우에는 `React.memo`, `useMemo`, `useCallback` 같은 도구를 사용합니다.

---

**Q4.** Props로 함수를 전달하는 Callback Props 패턴이 어색합니다. 더 좋은 방법은 없나요?

A: React의 단방향 데이터 흐름 원칙상, 작은 규모에서는 Callback Props가 가장 단순하고 직관적인 방법입니다. 컴포넌트 트리가 깊어져 Props Drilling이 심해지면 Context API, Zustand, Jotai 같은 전역 상태 관리 도구를 사용합니다. 그러나 학습 순서상 Callback Props를 먼저 이해해야 전역 상태 관리의 필요성을 느낄 수 있습니다.

---

**Q5.** `onFilterTextChange: (value: string) => void`에서 `void`가 뭔가요?

A: `void`는 "반환값이 없다"는 타입입니다. 이벤트 핸들러나 콜백 함수는 보통 무언가를 반환하지 않으므로 `void`를 씁니다.

```tsx
() => void                      // 파라미터도 없고 반환값도 없는 함수
(value: string) => void         // string을 받고 반환값 없는 함수
(id: number) => void            // number를 받고 반환값 없는 함수
(value: string) => string       // string을 받고 string을 반환하는 함수
```

---

**Q6.** `Array(9).fill(null)`이 왜 `[null, null, ..., null]`인가요?

A: `Array(9)`는 길이가 9인 빈 슬롯 배열을 만듭니다(요소가 없는 구멍 있는 배열). `.fill(null)`은 모든 슬롯을 `null`로 채웁니다. 결과는 `[null, null, null, null, null, null, null, null, null]`입니다.

```tsx
Array(3).fill(0)      // [0, 0, 0]
Array(5).fill('')     // ['', '', '', '', '']
Array(9).fill(null)   // [null, null, null, null, null, null, null, null, null]
```

---

**Q7.** `forEach + rows.push` 대신 `map`을 쓰면 더 깔끔하지 않나요?

A: 상품 데이터가 단순한 목록이라면 `map`이 더 깔끔합니다. 우리 예제는 카테고리 헤더(`ProductCategoryRow`)와 상품 행(`ProductRow`)이 섞여서 나오는 복잡한 구조라 `forEach + push`가 더 유연합니다. `map`은 입력 배열과 출력 배열의 크기가 같을 때 적합하지만, 여기서는 카테고리 헤더가 추가로 삽입되므로 출력이 더 많습니다. 두 방식 모두 유효합니다.

---

**Q8.** `React.ReactNode` 타입은 무엇이고 언제 쓰나요?

A: `React.ReactNode`는 React가 렌더링할 수 있는 모든 값의 타입입니다.

```
React.ReactNode = JSX 요소 | string | number | boolean | null | undefined | ReactNode[]
```

컴포넌트 반환 타입이나 `children` prop 타입에 주로 사용합니다. `JSX.Element`는 JSX 표현식(`<div>`, `<Component />`)만을 의미하는 더 좁은 타입입니다. 배열에 여러 종류의 렌더링 가능한 값을 담을 때는 `React.ReactNode[]`를 씁니다.

---

**Q9.** `calculateWinner` 함수를 외부에서 정의한 이유가 있나요?

A: 세 가지 이유가 있습니다. 첫째, 이 함수는 컴포넌트의 State나 Props에 접근하지 않는 순수 함수입니다. 컴포넌트 안에 넣을 이유가 없습니다. 둘째, 컴포넌트 밖에 두면 재렌더링마다 함수가 새로 생성되지 않습니다. 셋째, 테스트하기가 더 쉽습니다. 일반 원칙으로, 컴포넌트 State/Props에 의존하지 않는 함수는 컴포넌트 밖에 정의합니다.

---

**Q10.** 게임이 무승부로 끝나는 경우는 어떻게 처리하나요?

A: 현재 코드는 무승부 처리가 없습니다. 9개 칸이 전부 채워지고 승자가 없으면 "다음 플레이어: X(또는 O)"가 계속 표시됩니다. 처리하려면 다음을 추가합니다.

```tsx
const winner = calculateWinner(squares);
const isDraw = !winner && squares.every(sq => sq !== null); // 모든 칸이 채워지고 승자 없음

const status = winner
  ? `${winner}가 이겼습니다!`
  : isDraw
    ? '무승부입니다!'
    : `다음 플레이어: ${xIsNext ? 'X' : 'O'}`;
```

React 공식 튜토리얼의 추가 도전 과제 중 하나입니다.

---

**Q11.** `xIsNext ? 'X' : 'O'`와 `xIsNext ? 'O' : 'X'`를 헷갈립니다. 어떻게 구분하나요?

A: `xIsNext`가 `true`이면 "X가 다음"이므로 X가 놓여야 합니다. `xIsNext ? 'X' : 'O'`에서 `?` 뒤가 true일 때의 값입니다. "xIsNext가 true이면 X, false이면 O". 상태 메시지는 "다음에 놓을 사람"이므로 동일합니다. `xIsNext ? 'X' : 'O'`. 처음에는 헷갈리면 변수명을 더 명확하게 바꾸는 것도 방법입니다.

```tsx
const currentPlayer = xIsNext ? 'X' : 'O';
nextSquares[i] = currentPlayer;
const status = `다음 플레이어: ${currentPlayer}`;
```

---

**Q12.** Thinking in React 5단계를 항상 이 순서대로 해야 하나요?

A: 규칙이 아닌 권장 사항입니다. 처음에는 이 순서대로 하면 혼란이 줄어듭니다. 익숙해지면 이 과정을 동시에 수행하게 됩니다. 중요한 것은 "구현을 시작하기 전에 State의 개수와 위치를 먼저 생각한다"는 습관입니다. 코드를 먼저 짜고 나중에 구조를 뒤집는 것보다 훨씬 효율적입니다.

---

## 14. 핵심 요약

### Part A — Tic-Tac-Toe 핵심 개념

| 개념 | 핵심 포인트 |
|------|------------|
| `useState` | `const [값, set값] = useState(초기값)`. `setState` 호출 시 재렌더링 |
| 이벤트 핸들러 | `onClick={함수}` — 괄호 없음. 인자 있으면 `() => 함수(인자)` |
| State Lifting Up | 공유 State는 공통 부모로 올린다. 자식은 Props로 받아 표시만 |
| 불변성 | State 배열/객체는 직접 수정 금지. `.slice()` / spread / `filter` / `map`으로 새 값 생성 |
| Callback Props | 자식이 부모 State 변경 시 → 부모가 변경 함수를 Props로 내려준다 |

### Part B — Thinking in React 5단계

| 단계 | 핵심 질문 |
|------|-----------|
| Step 1: 컴포넌트 분해 | UI를 보고 단일 책임 원칙으로 경계 그리기 |
| Step 2: 정적 버전 | State 없이 Props만으로 먼저 UI 완성 |
| Step 3: 최소 State | "계산 가능하면 State 아님" 원칙 적용 |
| Step 4: State 위치 | 필요로 하는 모든 컴포넌트의 공통 부모에 배치 |
| Step 5: 역방향 흐름 | 자식 → 부모 변경은 Callback Props로 처리 |

### 배열 불변성 패턴 — Social Dashboard에서 계속 사용

```tsx
const arr = [1, 2, 3, 4, 5];

// 추가 (새 항목을 앞이나 뒤에)
[...arr, 6]                       // [1, 2, 3, 4, 5, 6]
[0, ...arr]                       // [0, 1, 2, 3, 4, 5]

// 삭제 (특정 값 제거)
arr.filter(n => n !== 3)          // [1, 2, 4, 5]

// 수정 (특정 값 업데이트)
arr.map(n => n === 3 ? 99 : n)    // [1, 2, 99, 4, 5]

// 복사
arr.slice()  또는  [...arr]        // [1, 2, 3, 4, 5] (새 배열)
```

### 다음 세션 예고 (Session 5: Social Dashboard)

Session 5에서는 오늘 배운 패턴 위에 두 가지가 추가됩니다.

- **`useEffect`**: "컴포넌트가 화면에 표시된 직후" 사이드 이펙트를 실행하는 훅 — API 호출, 타이머 설정 등
- **`fetch` + `async/await`**: JSONPlaceholder API에서 실제 사용자, 게시글, Todo 데이터를 받아오기

강사가 먼저 사용자 목록 기능(Task 1)을 시연한 뒤, 나머지 Task 2~6을 직접 구현합니다. 오늘 배운 `useState`, 불변성 패턴, Callback Props가 그대로 사용됩니다.

---

## 참고 자료

- [React 공식 튜토리얼: Tic-Tac-Toe](https://react.dev/learn/tutorial-tic-tac-toe) — TypeScript 버전 포팅 도전 가능
- [Thinking in React 원문](https://react.dev/learn/thinking-in-react) — Part B의 원본 문서
- [State: A Component's Memory](https://react.dev/learn/state-a-components-memory) — `useState` 심화
- [Sharing State Between Components](https://react.dev/learn/sharing-state-between-components) — State Lifting Up 공식 설명
- [Responding to Events](https://react.dev/learn/responding-to-events) — 이벤트 핸들링 공식 문서
- [Updating Arrays in State](https://react.dev/learn/updating-arrays-in-state) — 배열 불변성 패턴 총정리
