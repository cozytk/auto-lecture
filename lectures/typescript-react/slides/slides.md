---
theme: default
mdc: true
canvasWidth: 980
---

# TypeScript + React 프론트엔드 개발 입문

## 1일 7시간 과정

자바/파이썬 개발자를 위한 실무 중심 TypeScript & React 입문

<!--
[스크립트]
안녕하세요, 여러분. 오늘 하루 TypeScript와 React를 함께 배워갈 강사입니다. 반갑습니다.

오늘 과정의 공식 이름은 "TypeScript + React 프론트엔드 개발 입문"입니다. 총 7시간 과정으로, 아침 9시 30분부터 오후 5시 30분까지 진행합니다.

먼저 이 수업이 어떤 분들을 위한 수업인지 말씀드리겠습니다. 여러분은 이미 개발자이십니다. Java, Python, C#, 혹은 다른 언어로 개발 경험이 있으신 분들이 대상입니다. 프로그래밍의 기초, 변수, 함수, 조건문, 반복문 같은 개념은 이미 알고 계신다고 가정하고 수업을 진행하겠습니다.

오늘 우리가 달성할 목표는 세 가지입니다. 잠시 후 슬라이드에서 하나씩 소개해 드리겠습니다.

이 수업에서 가장 중요하게 생각하는 것은, 오늘 배운 내용을 바탕으로 생성형 AI의 도움을 받아 여러분이 직접 React 기반 웹 앱을 만들 수 있게 되는 것입니다. 완전한 전문가가 되는 것이 목표가 아닙니다. 핵심 개념을 이해하고, AI와 협업하여 실제로 동작하는 앱을 만들 수 있는 수준이 목표입니다.

그럼 오늘의 일정부터 살펴보겠습니다.

시간: 5분
-->

---

# 오늘의 일정

| 시간 | 세션 | 내용 |
|------|------|------|
| 09:30 – 10:00 | Session 1 | TypeScript 문법 기초 (강의, 30분) |
| 10:00 – 10:30 | Session 2 | TypeScript 실습 — typescript-exercises (30분) |
| 10:30 – 10:40 | — | **휴식 (10분)** |
| 10:40 – 11:40 | Session 3 | React + TypeScript 프로젝트 설정 (1시간) |
| 11:40 – 13:00 | — | **점심시간** |
| 13:00 – 15:00 | Session 4-5 | React QuickStart — Tic-Tac-Toe & Thinking in React (2시간) |
| 15:00 – 17:00 | Session 6 | 종합실습: Social Dashboard 앱 구현 (2시간) |
| 17:00 – 17:30 | Session 7 | 퀴즈 & Q&A (30분) |

<!--
[스크립트]
오늘 하루 일정입니다. 크게 두 파트로 나누어 볼 수 있습니다.

오전 파트는 TypeScript 중심입니다. 먼저 30분 동안 TypeScript의 핵심 문법을 강의로 살펴보고, 이어서 30분 동안 타이핑 실습 사이트에서 직접 코드를 작성해 보겠습니다. 짧은 시간이지만 TypeScript의 핵심은 모두 다룹니다.

점심 이후 오후 파트는 React 중심입니다. 프로젝트 설정부터 시작해서 React 공식 튜토리얼을 따라가며 핵심 개념을 익힌 뒤, 오늘의 메인 이벤트인 종합 실습을 2시간 동안 진행합니다.

중요한 사실 하나 말씀드립니다. 오늘 수업은 강의가 30%, 실습이 70%입니다. 코드를 직접 작성해 보는 시간이 훨씬 많습니다. 강의를 듣는 것보다 손을 움직여 보는 것이 훨씬 빠르게 익힐 수 있습니다. 막히는 부분이 있어도 괜찮습니다. 질문은 언제든지 해주세요.

시간: 2분
-->

---

# 오늘의 목표

<v-click>

## ① TypeScript 타입 시스템 이해

`string`, `number`, `interface`, `Union` 타입으로
**코드를 작성하기 전에 버그를 잡는** 방법을 배웁니다

</v-click>

<v-click>

## ② React 컴포넌트 개발 패턴 습득

`useState`, `props`, 이벤트 핸들러 — **함수형 컴포넌트**로
화면을 구성하는 React의 핵심 개념을 익힙니다

</v-click>

<v-click>

## ③ Social Dashboard 앱 완성

오늘 배운 모든 것을 활용해서
**실제로 동작하는 웹 앱**을 직접 만들어 봅니다

</v-click>

<!--
[스크립트]
오늘의 목표 세 가지입니다.

[click]
첫 번째 목표는 TypeScript 타입 시스템을 이해하는 것입니다. TypeScript가 무엇인지, 왜 쓰는지, 어떻게 사용하는지를 배웁니다. Java나 Python을 아시는 분들이라면 이미 타입의 개념에 익숙하실 겁니다. TypeScript는 JavaScript에 그 타입 개념을 더한 것입니다. 코드를 실행하기 전에 IDE가 오류를 미리 알려준다는 것이 핵심 장점입니다.

[click]
두 번째 목표는 React 컴포넌트 개발 패턴을 익히는 것입니다. React는 화면을 "컴포넌트"라는 조각으로 나눠서 만드는 라이브러리입니다. useState, props, 이벤트 핸들러 같은 React의 핵심 개념을 오늘 직접 코드로 작성해 보겠습니다.

[click]
세 번째이자 가장 중요한 목표는 Social Dashboard 앱을 완성하는 것입니다. 오늘 배운 모든 개념을 종합해서 실제로 동작하는 웹 앱을 만들어 보겠습니다. 소셜 미디어 대시보드처럼 데이터를 조회하고 필터링하는 기능을 가진 앱입니다.

이 세 목표는 순서가 있습니다. TypeScript 기초를 알아야 React 코드를 읽을 수 있고, React 개념을 알아야 종합 실습을 진행할 수 있습니다. 하나씩 차근차근 쌓아가는 방식으로 진행하겠습니다.

[Q&A 대비]
Q: TypeScript 경험이 전혀 없어도 괜찮나요?
A: 네, 전혀 없어도 됩니다. JavaScript도 몰라도 됩니다. Java나 Python 같은 다른 언어 경험이 있으면 충분합니다.

Q: 오늘 수업 후에 혼자서 React 앱을 만들 수 있게 되나요?
A: 간단한 앱은 가능합니다. 특히 AI 도구(GitHub Copilot, Claude 등)의 도움을 받으면 오늘 배운 내용으로도 상당히 복잡한 앱을 만들 수 있습니다. 오늘 수업의 목표 중 하나가 바로 그것입니다.

전환: 그럼 이제 본격적으로 첫 번째 세션을 시작하겠습니다. TypeScript가 도대체 무엇이고, 왜 사용하는지부터 살펴보겠습니다.
시간: 3분
-->

---
layout: section
---

# Session 1
# TypeScript 문법 기초

**30분** | 강의

<!--
[스크립트]
Session 1, TypeScript 문법 기초입니다. 30분 동안 진행합니다.

이 세션에서 다룰 내용은 오늘 하루 전체의 토대가 됩니다. TypeScript를 처음 접하신다면 처음에는 낯설게 느껴질 수 있지만, 사실 여러분이 이미 알고 계신 개념들과 크게 다르지 않습니다. 차근차근 따라오시면 됩니다.

시간: 30초
-->

---

# 왜 TypeScript인가? (1/2)

## JavaScript의 문제: 런타임까지 오류를 모릅니다

```js {1-5|7-10|12-15}{maxHeight:'340px'}
// JavaScript: 아무런 경고 없이 실행됩니다
function calculateTax(price, rate) {
  return price * rate;
}

// 정상 케이스: 1000원의 10% = 100
console.log(calculateTax(1000, 0.1));  // 100 ✓

// 실수 케이스: 문자열을 넘겨도 JavaScript는 경고하지 않습니다
console.log(calculateTax("1000", 0.1)); // 100 (암묵적 형변환!) ← 더 위험

// 최악의 케이스: 사용자가 결제 완료 후에야 버그를 발견합니다
function getUsername(user) {
  return user.name.toUpperCase(); // user가 null이면?
}
getUsername(null); // TypeError: 프로덕션 서버에서 터집니다
```

<div class="box-red">
JavaScript는 <strong>런타임</strong>까지 오류를 알 수 없습니다 — 코드가 실행되어야 버그가 드러납니다
</div>

<!--
[스크립트]
TypeScript를 배우기 전에, 먼저 왜 TypeScript가 필요한지 이해해야 합니다. JavaScript의 문제점을 먼저 보겠습니다.

화면에 있는 코드를 함께 봅시다. 첫 번째 코드 블록입니다. `calculateTax`라는 함수가 있습니다. `price`와 `rate`라는 두 개의 매개변수를 받아서 곱한 값을 반환합니다. 세금을 계산하는 함수입니다. 문법적으로 완전히 올바른 코드입니다. JavaScript 엔진은 아무런 경고도 내지 않습니다.

[click]
이제 이 함수를 실제로 호출해 봅니다. 첫 번째 호출은 `calculateTax(1000, 0.1)`입니다. 1000원의 10%이니 100이 나옵니다. 정상입니다. 그런데 두 번째 호출을 보십시오. `calculateTax("1000", 0.1)`입니다. 숫자가 아닌 문자열을 넘겼습니다. Java나 Python이었다면 즉시 오류가 났겠죠. 그런데 JavaScript는? 그냥 100이 나옵니다. JavaScript가 문자열 "1000"을 숫자 1000으로 자동으로 변환해버렸기 때문입니다. 이것을 암묵적 형변환이라고 합니다. 이게 왜 위험하냐면, 오류가 없으니까 문제가 있는지 모르고 그냥 넘어가게 됩니다.

[click]
세 번째 코드 블록은 더 심각합니다. `getUsername` 함수에 `null`을 넘기면 어떻게 될까요? `user.name`에 접근하는 순간 `TypeError`가 발생합니다. 문제는 이 오류가 언제 발생하느냐입니다. 코드를 저장할 때? 아닙니다. 빌드할 때? 아닙니다. 실제로 사용자가 기능을 사용할 때, 프로덕션 서버에서 터집니다. 사용자가 이미 결제를 완료했는데 서버가 죽어버리는 상황을 생각해 보십시오.

Java나 C# 개발자라면 이런 상황이 낯설게 느껴지실 겁니다. Java는 `NullPointerException`을 컴파일 타임에 잡아주는 경우가 많고, 타입이 맞지 않으면 아예 컴파일이 되지 않습니다. 바로 그 경험을 JavaScript에서도 하고 싶다면? 그게 바로 TypeScript입니다.

시간: 5분
-->

---

# 왜 TypeScript인가? (2/2)

## TypeScript: 컴파일 타임에 오류를 잡아냅니다

```ts {1-4|6-8|10-13}{maxHeight:'180px'}
// TypeScript: 코드를 저장하는 순간 IDE가 빨간 줄로 표시합니다
function calculateTax(price: number, rate: number): number {
  return price * rate;
}

// 컴파일 오류 — 저장하자마자 IDE가 경고합니다
calculateTax("1000", 0.1);
// Argument of type 'string' is not assignable to parameter of type 'number'

// TypeScript = JavaScript + 타입 시스템
// JavaScript ⊂ TypeScript (JS는 TS의 부분집합)
// 모든 JS 코드는 TS에서도 동작합니다
// TS 코드는 최종적으로 JS로 컴파일됩니다
```

<div class="grid grid-cols-2 gap-4">

<div class="col-left">

### TypeScript 위치
```
TypeScript 코드 (.ts)
      ↓  tsc 컴파일
JavaScript 코드 (.js)
      ↓  브라우저/Node.js 실행
```

</div>
<div class="col-right">

<div class="box-green">

**Java/C# 개발자에게**: TypeScript의 타입 시스템은 정적 타입과 개념적으로 유사합니다. 다만 **구조적 타이핑(Structural Typing)** 을 사용한다는 점이 다릅니다.

**Python 개발자에게**: Python 타입 힌트와 목적은 같지만, TypeScript는 타입 오류 시 **빌드 자체를 차단**합니다.

</div>

</div>

</div>

<!--
[스크립트]
이제 TypeScript 버전을 보겠습니다. `calculateTax` 함수를 TypeScript로 다시 작성했습니다. 달라진 점이 눈에 보이십니까? `price: number`와 `rate: number`처럼 매개변수 뒤에 콜론을 붙이고 타입을 적었습니다. 그리고 함수 이름 뒤에 `: number`를 추가해서 이 함수가 숫자를 반환한다고 선언했습니다.

[click]
이제 문자열을 넘기면 어떻게 될까요? `calculateTax("1000", 0.1)`를 작성하는 순간, 코드를 실행하기도 전에 VS Code에 빨간 줄이 생깁니다. 오류 메시지는 명확합니다. "string 타입은 number 타입 매개변수에 할당할 수 없습니다." Java에서 컴파일 오류를 보신 것과 비슷한 경험입니다. 코드를 저장하는 즉시 버그를 발견할 수 있습니다. 사용자가 기능을 쓰다가 버그를 발견하는 상황을 미리 막을 수 있습니다.

[click]
TypeScript의 위치를 정리하겠습니다. TypeScript는 JavaScript의 슈퍼셋, 즉 상위 집합입니다. 모든 JavaScript 코드는 TypeScript에서도 유효합니다. TypeScript는 컴파일 과정에서 타입 정보를 제거하고 순수한 JavaScript를 생성합니다. 브라우저나 Node.js는 TypeScript를 직접 실행하지 않습니다. React 프로젝트에서는 Vite 같은 빌드 도구가 이 과정을 자동으로 처리해 줍니다.

오른쪽의 박스를 보시면, 언어별 비교가 있습니다. Java나 C# 개발자 분들께는 TypeScript의 타입 시스템이 친숙하게 느껴지실 겁니다. 다만 하나 다른 점이 있습니다. Java는 클래스를 기반으로 타입을 구분하지만, TypeScript는 구조적 타이핑을 사용합니다. 이 차이는 이후 실습하면서 자연스럽게 이해하게 되실 겁니다. Python 개발자 분들께는, Python 3.5부터 추가된 타입 힌트와 목적이 같습니다. 다만 Python의 타입 힌트는 런타임에 무시되지만, TypeScript는 타입이 맞지 않으면 빌드 자체가 실패합니다.

전환: 자, 그럼 TypeScript의 기본 타입부터 하나씩 살펴보겠습니다.
시간: 5분
-->

---

# 기본 타입 (1/3) — 원시 타입

<div class="grid grid-cols-2 gap-4">

<div class="col-left">

```ts {1-6|8-12|14-17}{maxHeight:'340px'}
// 올바른 예시: 반드시 소문자를 사용합니다
const userName: string = "홍길동";
const userAge: number = 28;
const isPremium: boolean = true;
const productPrice: number = 29.99; // 실수도 number
const nothing: null = null;

// 잘못된 예시: 절대 사용하지 마십시오
const userName2: String = "홍길동"; // String은 래퍼 객체
const userAge2: Number = 28;        // Number는 래퍼 객체
const isPremium2: Boolean = true;   // Boolean은 래퍼 객체
// → VS Code에서 노란색 경고가 표시됩니다

// 배열 타입 — 두 가지 모두 동일합니다
const numbers: number[] = [1, 2, 3, 4, 5];
const names: string[] = ["홍길동", "김철수"];
const flags: Array<boolean> = [true, false, true]; // 제네릭 표기
```

</div>
<div class="col-right">

<div class="box-red">

**흔한 실수: 대문자 타입**

Java/C# 개발자가 가장 많이 하는 실수입니다.

| 올바른 사용 | 잘못된 사용 |
|------------|------------|
| `string` | `String` |
| `number` | `Number`, `Integer` |
| `boolean` | `Boolean` |

TypeScript에서 대문자 타입은 JavaScript의 **래퍼 객체**를 가리킵니다. 실무에서 `new String()`을 쓸 이유는 없습니다.

</div>

</div>

</div>

<!--
[스크립트]
TypeScript의 기본 타입입니다. 하나씩 살펴보겠습니다. 타입 어노테이션은 변수명 뒤에 콜론을 붙이고 타입 이름을 씁니다. `const userName: string = "홍길동"` — 여기서 `: string` 부분이 타입 어노테이션입니다. `number`는 정수와 실수를 모두 포함합니다. Java처럼 `int`, `float`, `double`을 구분하지 않습니다. 모든 숫자는 `number` 하나입니다. `boolean`은 `true`와 `false` 두 가지 값만 가집니다.

[click]
이제 가장 중요한 주의사항입니다. Java, C# 개발자 분들이 가장 많이 하는 실수가 바로 여기에 있습니다. Java에서는 `String`(대문자)이 맞지만, TypeScript에서는 반드시 소문자 `string`을 사용합니다. 대문자 `String`은 JavaScript의 래퍼 객체를 가리킵니다. `new String("hello")`처럼 생성하는 객체입니다. 실무에서 이렇게 쓸 일은 거의 없습니다. VS Code에서 `String`(대문자)을 쓰면 노란색 경고가 표시됩니다. 오른쪽 빨간 박스를 보시면 정리되어 있습니다. 소문자, 소문자, 소문자입니다. `string`, `number`, `boolean`.

[click]
배열 타입은 두 가지 방법으로 표현할 수 있습니다. `number[]`처럼 타입 뒤에 대괄호를 붙이거나, `Array<boolean>`처럼 제네릭 표기법을 사용합니다. 두 가지가 완전히 동일하게 동작합니다. 어떤 것을 쓸지는 팀 컨벤션을 따르면 됩니다. 일반적으로 `number[]`가 더 많이 쓰입니다.

시간: 3분
-->

---

# 기본 타입 (2/3) — 타입 추론과 any

```ts {1-8|10-18|20-26}{maxHeight:'280px'}
// 타입 추론 — TypeScript가 오른쪽 값을 보고 타입을 자동으로 결정합니다
const productName = "노트북";    // TypeScript가 string으로 추론
const productCount = 10;         // TypeScript가 number로 추론
const inStock = true;            // TypeScript가 boolean으로 추론

// 위 코드는 아래와 완전히 동일합니다 — 굳이 쓸 필요 없습니다
const productName2: string = "노트북";  // 명시적 타입 (중복)
const productCount2: number = 10;       // 명시적 타입 (중복)

// 타입을 반드시 명시해야 하는 경우
let totalPrice: number;           // 초기값 없이 선언할 때
totalPrice = 50000;               // 정상
totalPrice = "오만원";            // 컴파일 오류!

const items: string[] = [];       // 빈 배열은 반드시 명시
// const items2 = [];             // ← any[]로 추론됩니다 — 피하십시오

// 함수 매개변수는 추론이 되지 않으므로 항상 명시합니다
function greet(name: string): string {
  return `안녕하세요, ${name}님!`;
}

// any 타입 — TypeScript를 쓰는 이유를 없애버립니다
let data: any = "문자열";
data = 42;                   // 정상 — any이므로 뭐든 됩니다
data.nonExistentMethod();    // 컴파일 오류 없음 → 런타임에서 터집니다
```

<div class="box-red">

`any`를 쓰면 TypeScript 타입 검사가 전혀 이루어지지 않습니다. 타입을 모를 때는 `any` 대신 `unknown`을 사용하십시오.

</div>

<!--
[스크립트]
타입 추론과 any 타입입니다. TypeScript는 우리가 타입을 직접 적지 않아도 오른쪽 값을 보고 타입을 자동으로 결정합니다. 이것을 타입 추론이라고 합니다. `const productName = "노트북"` — 오른쪽이 문자열이니까 TypeScript는 `productName`의 타입을 `string`으로 추론합니다. 따라서 아래처럼 `string`을 명시적으로 적을 필요가 없습니다. 오히려 중복이라 코드가 지저분해집니다. 추론이 가능한 곳에서는 굳이 쓰지 않아도 됩니다.

[click]
그렇다면 언제 타입을 반드시 써야 할까요? 세 가지 경우입니다. 첫째, 초기값 없이 변수를 선언할 때입니다. `let totalPrice: number`처럼 선언하면 나중에 다른 타입의 값을 넣으려 할 때 오류가 납니다. 둘째, 빈 배열을 선언할 때입니다. `const items = []`라고 쓰면 TypeScript는 이 배열에 어떤 타입이 들어갈지 모르므로 `any[]`로 추론합니다. 이렇게 되면 배열에 아무 값이나 들어가도 오류가 나지 않습니다. 반드시 `const items: string[] = []`처럼 타입을 명시하십시오. 셋째, 함수 매개변수입니다. 함수 외부에서 어떤 값이 들어올지 모르기 때문에, 매개변수 타입은 항상 명시해야 합니다.

[click]
`any` 타입입니다. `any`는 TypeScript의 타입 시스템을 완전히 우회하는 탈출구입니다. `any` 타입 변수에는 어떤 값도 넣을 수 있고, 존재하지 않는 메서드도 호출할 수 있습니다. 컴파일 오류가 없으니까요. 하지만 그 결과는 런타임 오류입니다. 처음에 JavaScript를 쓰던 때와 똑같습니다. 어딘가 막히면 `any`로 해결하고 싶은 유혹이 생깁니다. 하지만 `any`를 쓰는 순간 TypeScript를 쓰는 이유가 사라집니다. 대신 `unknown`을 사용하십시오. `unknown`은 타입을 확인하기 전에는 사용할 수 없어서 훨씬 안전합니다.

시간: 4분
-->

---

# 기본 타입 (3/3) — 객체와 인라인 타입

```ts {1-9|11-20}{maxHeight:'280px'}
// 인라인 객체 타입 — 복잡해지면 읽기 어렵습니다
const user: { name: string; age: number; email: string } = {
  name: "홍길동",
  age: 28,
  email: "hong@example.com",
};

console.log(user.name);   // "홍길동" — 정상
console.log(user.phone);  // 컴파일 오류: 'phone' does not exist on type

// 해결책: interface나 type으로 이름을 붙여 재사용합니다 (다음 슬라이드에서 다룹니다)
// 지금은 이런 패턴이 있다는 것만 기억해 두십시오

// object 타입 — 피해야 합니다
const obj: object = { name: "홍길동" };
obj.name; // 컴파일 오류: Property 'name' does not exist on type 'object'

// 빈 객체 타입 {} — 거의 아무것도 막지 않습니다
const anything: {} = 42;      // 정상 (의도치 않음)
const anything2: {} = "hello"; // 정상 (의도치 않음)
// → 이런 타입은 실무에서 사용하지 않습니다
```

<div class="box-blue">

**실무 팁**: 객체 타입은 항상 `interface` 또는 `type`으로 이름을 붙여서 사용합니다.
인라인으로 쓰면 재사용이 불가능하고 코드가 지저분해집니다.

</div>

<!--
[스크립트]
객체 타입입니다. 객체 타입을 직접 중괄호 안에 적을 수 있습니다. 이것을 인라인 타입 정의라고 합니다. `const user: { name: string; age: number; email: string } = { ... }` — 변수명 뒤에 중괄호로 속성과 타입을 나열했습니다. 이 방법은 간단한 경우에는 동작하지만, 문제가 있습니다. 이 객체 타입을 다른 함수나 변수에서 재사용하려면 똑같이 긴 타입 정의를 반복해야 합니다. 그리고 정의되지 않은 속성에 접근하면 컴파일 오류가 납니다. `user.phone`은 타입 정의에 없으므로 오류입니다. 이것이 바로 TypeScript가 도움이 되는 순간입니다.

[click]
그래서 실무에서는 `interface`나 `type`을 사용합니다. 이것은 다음 슬라이드에서 바로 다루겠습니다. 지금은 인라인 타입 정의의 개념만 이해하고 넘어가겠습니다.

참고로 `object`라는 타입이 있습니다만, 이것은 사용하지 마십시오. `object` 타입의 변수에서는 어떤 속성도 접근할 수 없습니다. 빈 중괄호 `{}`도 마찬가지로 사용하지 마십시오. 숫자, 문자열, 거의 모든 것이 `{}`에 할당될 수 있어서 타입 안전성을 전혀 보장하지 않습니다.

파란 박스를 보시면 실무 팁이 있습니다. 객체 타입은 항상 `interface` 또는 `type`으로 이름을 붙여서 사용합니다. 이제 그 방법을 살펴보겠습니다.

시간: 3분
-->

---

# Interface와 Type (1/3)

## interface — 객체 구조에 이름을 붙입니다

```ts {1-7|9-19|21-29}{maxHeight:'300px'}
// interface 정의: 객체가 어떤 속성을 가져야 하는지 선언합니다
interface User {
  name: string;      // 필수 속성
  age: number;       // 필수 속성
  email: string;     // 필수 속성
  phone?: string;    // 선택적 속성 — ? 를 붙이면 없어도 됩니다
}

// interface를 타입으로 사용합니다
const user1: User = {
  name: "홍길동",
  age: 28,
  email: "hong@example.com",
  // phone 없어도 됩니다 — 선택적이므로
};

const user2: User = {
  name: "김철수",
  age: 30,
  // email 없으면 컴파일 오류: Property 'email' is missing in type
};

// 함수 매개변수로 interface를 사용합니다
function displayUser(user: User): void {
  console.log(`${user.name} (${user.age}세) — ${user.email}`);
  if (user.phone) {
    // phone은 undefined일 수 있으므로 확인 후 사용합니다
    console.log(`연락처: ${user.phone}`);
  }
}
```

<!--
[스크립트]
interface입니다. TypeScript에서 가장 자주 쓰는 기능 중 하나입니다. `interface User`로 User라는 이름의 타입을 정의합니다. 중괄호 안에 속성 이름과 타입을 나열합니다. Java의 인터페이스와 이름이 같지만 의미가 다릅니다. Java의 인터페이스는 메서드 시그니처만 정의하지만, TypeScript의 `interface`는 속성과 메서드를 모두 정의합니다. 오히려 Java의 POJO(Plain Old Java Object) 클래스나 record에 더 가깝습니다.

속성 이름 뒤에 `?`를 붙이면 선택적 속성이 됩니다. 있어도 되고 없어도 됩니다.

[click]
이제 이 `User` 인터페이스를 실제로 사용해 봅니다. `user1`은 name, age, email을 다 채웠으니 정상입니다. phone은 없어도 됩니다. `user2`는 email이 없습니다. email은 필수 속성이므로 컴파일 오류가 발생합니다. IDE에서 바로 빨간 줄이 생깁니다.

[click]
함수 매개변수에도 interface를 씁니다. `displayUser` 함수는 `User` 타입을 받습니다. 함수 내부에서 `user.name`, `user.age`, `user.email`에 접근할 수 있습니다. `user.phone`은 선택적이라 `undefined`일 수 있으므로, `if (user.phone)` 조건을 걸어서 사용합니다.

반환 타입이 `: void`인 것도 확인하십시오. void는 반환값이 없다는 의미입니다. Java의 `void`와 동일합니다.

[Q&A 대비]
Q: Java처럼 interface 이름 앞에 I를 붙여야 하나요? IUser 이렇게요.
A: 아닙니다. TypeScript 커뮤니티에서는 I 접두어를 권장하지 않습니다. TypeScript 공식 스타일 가이드와 대부분의 오픈소스 프로젝트에서 그냥 User, Product처럼 씁니다. Java 습관을 TypeScript에서 고쳐야 할 첫 번째 항목입니다.

시간: 4분
-->

---

# Interface와 Type (2/3)

## type alias — interface보다 더 유연합니다

```ts {1-8|10-16|18-27}{maxHeight:'280px'}
// type은 객체 타입뿐 아니라 어떤 타입에도 이름을 붙일 수 있습니다
type UserID = number;           // number에 별칭
type ProductName = string;      // string에 별칭
type ID = string | number;      // Union 타입 (다음 섹션에서 자세히 다룹니다)

// 객체 타입에 이름 붙이기 — interface와 유사합니다
type Point = { x: number; y: number };
const origin: Point = { x: 0, y: 0 };

// interface extends — 기존 인터페이스를 확장합니다
interface Animal {
  name: string;
}
interface Dog extends Animal {   // Animal의 모든 속성 + breed 추가
  breed: string;
}

// type 교차(intersection) — & 연산자로 합칩니다
type Animal2 = { name: string };
type Dog2 = Animal2 & { breed: string }; // 두 타입을 합칩니다

// 두 방법의 결과는 동일합니다
const myDog1: Dog = { name: "멍이", breed: "진돗개" };
const myDog2: Dog2 = { name: "멍이", breed: "진돗개" };

// 실무에서 자주 쓰는 패턴: interface와 type 혼용
type Status = "active" | "inactive" | "pending"; // Union → type
interface UserProfile { name: string; status: Status; } // 객체 → interface
```

<!--
[스크립트]
type alias입니다. `type` 키워드로 타입에 이름을 붙이는 또 다른 방법입니다. `type`은 `interface`와 달리 어떤 타입이든 이름을 붙일 수 있습니다. 원시 타입에도, Union 타입에도, 교차 타입에도 사용할 수 있습니다. `type UserID = number`처럼 숫자 타입에 UserID라는 더 의미있는 이름을 붙일 수 있습니다.

[click]
`interface`는 `extends` 키워드로 확장합니다. `Dog extends Animal`은 Animal의 모든 속성을 포함하고 breed를 추가합니다. Java의 상속과 비슷한 개념입니다.

[click]
`type`은 `&` 연산자, 교차 타입으로 확장합니다. `Animal2 & { breed: string }`은 Animal2의 모든 속성과 breed를 합친 새 타입을 만듭니다. 결과는 `extends`와 동일합니다.

마지막 예시를 보십시오. 실무에서 가장 많이 쓰는 패턴입니다. 상태처럼 여러 값 중 하나를 표현할 때는 `type`, 객체 구조를 정의할 때는 `interface`를 씁니다. 이 구분이 지금은 완전히 이해가 안 되어도 괜찮습니다. 다음 슬라이드에서 표로 정리해 드리겠습니다.

시간: 3분
-->

---

# Interface와 Type (3/3)

## 언제 interface? 언제 type?

<div class="grid grid-cols-[1fr_1.2fr] gap-4 mt-1">
<div>

<v-click>

| 상황 | 권장 | 이유 |
|------|------|------|
| 객체 구조 | `interface` | 확장 직관적 |
| 유니온 타입 | `type` | interface 불가 |
| 조합/변형 | `type` | `&`, 조건부 등 |
| React Props | 팀 컨벤션 | 일관성 핵심 |

</v-click>

<div class="box-blue mt-3 text-sm">

**핵심**: 객체 → `interface`, 조합 → `type`
팀 일관성이 가장 중요합니다

</div>

</div>
<div>

<v-click>

```ts {maxHeight:'280px'}
// 실무: interface + type 혼용
interface OrderItem {
  productId: number;
  quantity: number;
  unitPrice: number;
}

type PaymentMethod =
  | "card" | "bank_transfer"
  | "kakao_pay";
type OrderStatus =
  | "pending" | "confirmed"
  | "shipped" | "delivered";

interface Order {
  id: number;
  items: OrderItem[];
  status: OrderStatus;
  paymentMethod: PaymentMethod;
  totalAmount: number;
}
```

</v-click>

</div>
</div>

<!--
[스크립트]
interface vs type 정리입니다.

[click]
왼쪽 표를 보시면 상황별 권장 선택이 있습니다. 객체 구조를 정의할 때는 `interface`를 씁니다. 유니온 타입, 즉 "A이거나 B이거나"를 표현할 때는 `type`을 씁니다. interface로는 유니온 타입을 만들 수 없습니다. React 컴포넌트의 Props를 정의할 때는 둘 다 가능합니다. 팀 컨벤션을 따르는 것이 가장 중요합니다.

[click]
오른쪽 실무 예시를 보십시오. `OrderItem`은 객체 구조이므로 `interface`로 정의합니다. `PaymentMethod`는 결제 수단 중 하나를 표현하는 유니온이므로 `type`으로 정의합니다. `OrderStatus`도 마찬가지입니다. 그리고 `Order` 인터페이스는 이 두 가지를 모두 속성으로 가집니다. 실제로 이런 식으로 섞어서 사용하는 것이 자연스럽습니다.

이 코드를 보시면, TypeScript로 도메인 모델을 표현하는 방법이 보이실 겁니다. 주문(Order)은 주문 항목(OrderItem) 배열과 주문 상태(OrderStatus), 결제 수단(PaymentMethod)으로 구성됩니다. 이런 식으로 타입을 먼저 설계하면 코드를 짜기 전에 데이터 구조가 명확해집니다. Java의 클래스 설계와 비슷한 사고 과정입니다.

시간: 3분
-->

---

# Union & Literal 타입 (1/2)

## Union 타입 — "A 또는 B"

```ts {1-8|10-19}{maxHeight:'240px'}
// 기본 Union 타입: | 기호로 연결합니다
type StringOrNumber = string | number;

let value: StringOrNumber;
value = "안녕하세요"; // 정상 — string
value = 42;          // 정상 — number
value = true;        // 컴파일 오류 — boolean은 허용되지 않습니다

// API 응답 상태를 Literal Union으로 모델링합니다 — 실무에서 매우 자주 씁니다
type RequestStatus = "idle" | "loading" | "success" | "error";
//                   ↑ 정확히 이 4개의 문자열 값만 허용합니다

let status: RequestStatus;
status = "loading";    // 정상
status = "success";    // 정상
status = "completed";  // 컴파일 오류: "completed"는 허용되지 않습니다
status = "Loading";    // 컴파일 오류: 대소문자 구분 주의!

// 실무 패턴: API 응답 전체를 타입으로 모델링합니다
interface ApiResponse<T> {
  status: RequestStatus;
  data: T | null;
  errorMessage: string | null;
}
```

<!--
[스크립트]
Union 타입입니다. TypeScript에서 가장 강력하고 자주 쓰이는 기능 중 하나입니다. Union 타입은 `|` 기호, 파이프 기호로 여러 타입을 연결합니다. `string | number`는 "string이거나 number"입니다. Java의 제네릭이나 Python의 `Union[str, int]`와 비슷한 개념입니다. `value` 변수는 string도 되고 number도 되지만, boolean은 안 됩니다.

[click]
Literal Union 타입이 실무에서 가장 많이 쓰이는 패턴입니다. `"idle" | "loading" | "success" | "error"` — 이렇게 특정 문자열 값 자체를 타입으로 씁니다. 이 4가지 값 중 하나만 허용됩니다. `"completed"`는 이 목록에 없으니 컴파일 오류입니다. `"Loading"`은 대문자 L이 있으니 역시 오류입니다.

이 패턴이 왜 중요할까요? React로 화면을 만들 때, 데이터를 서버에서 불러오는 상태를 표현해야 합니다. "아직 요청 안 함", "불러오는 중", "성공", "오류" — 이 4가지 상태입니다. `RequestStatus`처럼 타입으로 정의해 두면, 오타가 나거나 잘못된 상태 값을 쓰면 즉시 오류를 잡아줍니다.

마지막 `ApiResponse<T>` 인터페이스는 제네릭을 사용합니다. `<T>`는 "어떤 타입이든"을 의미합니다. 이것은 다음 섹션에서 자세히 다루겠습니다.

시간: 3분
-->

---

# Union & Literal 타입 (2/2)

## 타입 좁히기 (Type Narrowing) — Union 타입을 다루는 방법

```ts {1-11|13-22|24-33}{maxHeight:'220px'}
// typeof로 원시 타입을 구분합니다
function processValue(value: string | number): string {
  if (typeof value === "string") {
    // 이 블록 안에서 TypeScript는 value가 string임을 압니다
    return value.toUpperCase(); // string 메서드 사용 가능
  }
  // 여기서는 TypeScript가 value가 number임을 압니다
  return value.toFixed(2); // number 메서드 사용 가능
}
console.log(processValue("hello")); // "HELLO"
console.log(processValue(3.14159)); // "3.14"

// in 연산자로 속성 존재를 확인합니다
interface Cat { name: string; meow(): void; }
interface Dog { name: string; bark(): void; }

function makeSound(animal: Cat | Dog): void {
  if ("meow" in animal) {
    animal.meow(); // Cat 타입으로 좁혀졌습니다
  } else {
    animal.bark(); // Dog 타입으로 좁혀졌습니다
  }
}

// 실무 예: API 상태에 따른 UI 분기
function handleResponse(response: ApiResponse<User>): void {
  if (response.status === "loading") {
    console.log("로딩 중...");
    return;
  }
  if (response.status === "error") {
    console.error(`오류: ${response.errorMessage}`);
    return;
  }
  if (response.status === "success" && response.data) {
    console.log(`사용자: ${response.data.name}`);
  }
}
```

<!--
[스크립트]
타입 좁히기입니다. Union 타입을 사용할 때 꼭 알아야 하는 개념입니다.
`value`가 `string | number`라면, TypeScript는 `value`가 string인지 number인지 모릅니다. 둘 중 어느 것일 수 있으니까요. `toUpperCase()`는 string에만 있는 메서드인데, number일 수도 있으니 바로 쓸 수 없습니다. 그래서 `if (typeof value === "string")` 조건으로 먼저 확인합니다. 이 블록 안에서 TypeScript는 value가 확실히 string임을 압니다. 블록 밖에서는 string이 아닌 것이 확인되었으니 number임을 압니다. 이렇게 조건문을 통해 타입을 좁혀나가는 것을 타입 좁히기라고 합니다.

[click]
`in` 연산자는 객체에 특정 속성이 있는지 확인합니다. `Cat`에는 `meow` 메서드가 있고 `Dog`에는 없습니다. `"meow" in animal`이 true이면 이것은 `Cat`입니다. else 블록에서는 `Dog`임이 확정됩니다.

[click]
실무에서 가장 많이 쓰이는 패턴입니다. API 응답의 status를 확인하면서 분기합니다. `status === "loading"`이면 로딩 화면을 보여줍니다. `status === "error"`이면 오류를 처리합니다. `status === "success"`이면 데이터를 사용합니다. React 컴포넌트에서 이 패턴을 정말 많이 사용합니다. 오늘 종합 실습에서도 바로 이 패턴을 활용할 것입니다.

[Q&A 대비]
Q: Python의 `isinstance`와 비슷한 건가요?
A: 개념적으로 유사합니다. Python의 `isinstance(value, str)`이 TypeScript의 `typeof value === "string"`과 비슷한 역할을 합니다. 다만 TypeScript는 이 조건문 이후의 블록에서 타입을 자동으로 좁혀주는 정적 분석 기능이 있다는 점이 다릅니다.

시간: 3분
-->

---

# 제네릭 맛보기

## `<T>` 패턴 — React에서 바로 사용합니다

```ts {1-9|11-20}{maxHeight:'250px'}
// 제네릭 없이: 타입별로 함수를 각각 만들어야 합니다
function getFirstNumber(arr: number[]): number { return arr[0]; }
function getFirstString(arr: string[]): string { return arr[0]; }
// → 로직이 동일한데 타입만 다릅니다. 비효율적입니다.

// 제네릭으로 하나의 함수로 합칩니다
function getFirst<T>(arr: T[]): T {
  return arr[0]; // T 타입 배열의 첫 번째 요소를 T 타입으로 반환
}
// 사용할 때 T가 자동으로 결정됩니다
const firstNum = getFirst([1, 2, 3]);       // T = number
const firstStr = getFirst(["a", "b", "c"]); // T = string

// React에서 가장 먼저 만나는 제네릭: useState
import { useState } from "react";

const [count, setCount] = useState<number>(0);
setCount(1);       // 정상
setCount("hello"); // 컴파일 오류: string은 number에 할당 불가

const [user, setUser] = useState<User | null>(null);
// user는 User 타입이거나 null입니다

const [users, setUsers] = useState<User[]>([]);
// users는 User 배열입니다 — 가장 자주 쓰는 패턴 중 하나입니다
```

<div class="box-yellow">

**지금 당장 완전히 이해 안 해도 됩니다.** `useState<User[]>([])`처럼 꺾쇠괄호 안에 타입을 적는 패턴을 기억해 두십시오. React 실습에서 반복하다 보면 자연스럽게 익힙니다.

</div>

<!--
[스크립트]
제네릭입니다. 이 세션의 마지막 주요 개념입니다. 제네릭이 왜 필요한지 먼저 보겠습니다. 배열의 첫 번째 요소를 반환하는 함수를 만들고 싶습니다. number 배열용, string 배열용을 각각 만들어야 할까요? 로직은 완전히 같은데 타입만 다릅니다. 비효율적입니다.

제네릭 함수 `getFirst<T>`는 이 문제를 해결합니다. `<T>`는 타입 매개변수입니다. "T를 제가 받을 타입으로 쓰겠습니다"라는 선언입니다. `getFirst([1, 2, 3])`을 호출하면 TypeScript가 배열을 보고 T를 `number`로 결정합니다. `getFirst(["a", "b", "c"])`를 호출하면 T를 `string`으로 결정합니다. T가 number일 때는 number를 반환하고, T가 string일 때는 string을 반환합니다.

[click]
React에서 가장 먼저 만나는 제네릭이 `useState`입니다. `useState<number>(0)`은 "이 상태는 number 타입입니다, 초기값은 0입니다"라는 선언입니다. 이 상태에 string을 넣으려 하면 컴파일 오류가 납니다.

`useState<User | null>(null)`은 "이 상태는 User 타입이거나 null입니다, 초기값은 null입니다"라는 뜻입니다. 데이터를 아직 불러오지 않은 상태는 null이고, 불러온 후에는 User 객체입니다.

`useState<User[]>([])`는 "이 상태는 User 배열입니다, 초기값은 빈 배열입니다"라는 뜻입니다. 오늘 종합 실습에서 바로 이 패턴을 사용합니다.

노란 박스를 보십시오. 지금 당장 제네릭을 완전히 이해하지 않아도 됩니다. `useState<타입>(초기값)` 패턴만 기억해 두십시오. React 실습에서 반복하다 보면 자연스럽게 익힙니다.

시간: 3분
-->

---

# 함수 타입

## 매개변수와 반환 타입 — React 이벤트 핸들러 예고

```ts {1-9|11-20}{maxHeight:'250px'}
// 기본 함수 타입
function add(a: number, b: number): number {
  return a + b;
}

function logMessage(message: string): void { // void = 반환값 없음
  console.log(`[LOG] ${message}`);
}

const multiply = (a: number, b: number): number => a * b; // 화살표 함수도 동일

// 함수 타입을 타입으로 표현할 수 있습니다
type AddFunction = (a: number, b: number) => number;
const myAdd: AddFunction = (a, b) => a + b; // 타입이 이미 선언되어 있어 생략 가능

// React 컴포넌트에서 이벤트 핸들러는 함수 타입이 필요합니다 (Session 3에서 자세히)
interface ButtonProps {
  label: string;
  onClick: () => void;                    // 매개변수 없고 반환값 없는 함수
  onChange?: (value: string) => void;     // 선택적 이벤트 핸들러
  onSubmit?: (event: React.FormEvent) => void;
}
```

<div class="box-blue">

**React에서 중요한 이유**: 컴포넌트가 다른 컴포넌트에 함수를 prop으로 전달할 때, 함수 타입을 정확하게 맞춰야 합니다. Session 3에서 실제 React 코드와 함께 다시 설명합니다.

</div>

<!--
[스크립트]
함수 타입입니다. 이것은 빠르게 훑고 넘어가겠습니다. React 실습에서 자연스럽게 익히게 됩니다. 함수에 타입을 붙이는 방법은 간단합니다. 매개변수 뒤에 타입을 붙이고, 함수 시그니처 뒤에 반환 타입을 붙입니다. 반환값이 없으면 `void`를 씁니다. Java의 `void`와 같습니다. 화살표 함수도 동일한 방식으로 타입을 붙입니다.

[click]
함수 타입 자체를 `type`으로 표현할 수 있습니다. `(a: number, b: number) => number`는 "number 두 개를 받아서 number를 반환하는 함수" 타입입니다.

아래 `ButtonProps`는 React 컴포넌트에서 사용하는 패턴입니다. 버튼 컴포넌트가 클릭 핸들러를 prop으로 받는 경우입니다. `onClick: () => void`는 "매개변수 없고 반환값 없는 함수"입니다. 이것은 Session 3에서 실제 React 코드와 함께 자세히 다루겠습니다. 지금은 이런 패턴이 있다는 것만 알고 넘어가겠습니다.

시간: 2분
-->

---

# Session 1 핵심 요약

<v-click>

| 개념 | 올바른 사용 | 주의사항 |
|------|------------|---------|
| 원시 타입 | `string` `number` `boolean` | 대문자 `String` `Number` 금지 |
| 배열 | `number[]` 또는 `Array<number>` | 빈 배열 `[]`은 타입 명시 필수 |
| `any` | 사용하지 않습니다 | 대신 `unknown` 사용 |
| 객체 구조 | `interface User { ... }` | 인라인 타입 `{...}` 재사용 불가 |
| 조합 타입 | `type Status = "a" \| "b"` | 유니온은 `type`으로 |
| 타입 좁히기 | `typeof`, `in`, Literal 비교 | Union 사용 시 필수 |
| 제네릭 | `useState<User[]>([])` | 꺾쇠 안에 타입 |

</v-click>

<v-click>

```ts
// 오늘 하루 자주 볼 핵심 패턴 3가지
interface User { id: number; name: string; }         // 객체 구조
type Status = "loading" | "success" | "error";       // 상태 값
const [users, setUsers] = useState<User[]>([]);       // React 상태
```

</v-click>

<div class="box-green">

**이 세 줄을 이해하면** Session 1의 핵심은 모두 이해한 것입니다.
Session 2 실습에서 이 개념들을 직접 타이핑해 보겠습니다.

</div>

<!--
[스크립트]
Session 1 핵심 요약입니다.

[click]
표를 보시면 오늘 배운 개념들이 정리되어 있습니다. 원시 타입은 소문자로, `any`는 쓰지 말고, 객체 구조는 `interface`로, 조합 타입은 `type`으로, Union을 쓸 때는 타입 좁히기를 하고, 제네릭은 꺾쇠 안에 타입을 씁니다.

[click]
오늘 하루 가장 많이 볼 패턴 세 가지입니다. User처럼 객체 구조를 `interface`로 정의하는 것, "loading" | "success" | "error"처럼 상태를 `type`으로 정의하는 것, 그리고 `useState<User[]>([])`처럼 React 상태에 타입을 지정하는 것입니다.

이 세 줄을 이해했다면 Session 1의 핵심은 모두 이해한 것입니다. 완벽하게 외울 필요는 없습니다. 오늘 하루 실습을 하면서 반복해서 쓰다 보면 자연스럽게 익혀집니다.

이제 30분 동안 실제로 코드를 작성해 보는 실습을 진행하겠습니다.

시간: 2분
-->

---

# Session 1 퀴즈

## 다음 중 올바른 TypeScript 코드는 무엇일까요?

<v-click>

```ts
// (A)
const name: String = "홍길동";
const age: Integer = 28;
const isActive: Boolean = true;

// (B)
const name: string = "홍길동";
const age: number = 28;
const isActive: boolean = true;

// (C)
const name = "홍길동";      // 타입 명시 없음
const age = 28;
const isActive = true;
```

</v-click>

<v-click>

<div class="box-green">

**정답: (B)와 (C) 모두 올바른 코드입니다!**

- **(A)**: `String`, `Integer`, `Boolean`은 TypeScript에서 사용하지 않습니다. Java/C# 습관입니다.
- **(B)**: 소문자 타입을 명시적으로 선언했습니다. 올바릅니다.
- **(C)**: 타입 추론을 활용했습니다. TypeScript가 자동으로 타입을 결정합니다. 올바릅니다.

초기값이 있을 때는 (C)처럼 추론을 활용하면 코드가 더 간결합니다.

</div>

</v-click>

<!--
[스크립트]
간단한 퀴즈입니다.

[click]
화면에 세 가지 코드가 있습니다. 각각 이름(name), 나이(age), 활성 여부(isActive)를 선언하는 코드입니다. 잠깐 생각해 보십시오. 어떤 것이 올바른 TypeScript 코드일까요?

30초 드리겠습니다. 옆 사람과 이야기해 봐도 좋습니다.

(30초 대기)

[click]
정답은 B와 C입니다. 둘 다 올바른 코드입니다.

A는 Java나 C# 개발자가 자주 하는 실수입니다. `String`, `Integer`, `Boolean`은 TypeScript에서 사용하지 않습니다. TypeScript에는 `Integer` 타입 자체가 없습니다. 모든 숫자는 `number`입니다.

B는 소문자 타입을 명시적으로 선언했습니다. 올바릅니다.

C는 타입을 쓰지 않았지만, TypeScript가 오른쪽 값을 보고 자동으로 타입을 결정합니다. 초기값이 있을 때는 이렇게 추론을 활용하는 것이 더 깔끔합니다.

B와 C 중에서는 C가 더 TypeScript다운 코드입니다.

전환: 이제 본격적인 실습으로 넘어가겠습니다.
시간: 2분
-->

---
layout: section
---

# Session 2
# TypeScript 실습

**30분** | 독립 실습

https://typescript-exercises.github.io

<!--
[스크립트]
Session 2입니다. 30분 동안 직접 코드를 작성해 보는 실습을 진행합니다.

지금부터 https://typescript-exercises.github.io 사이트를 사용할 것입니다. 이 사이트는 브라우저에서 바로 TypeScript 코드를 작성하고 컴파일 결과를 실시간으로 확인할 수 있습니다. 오른쪽에 녹색 체크가 나오면 정답입니다.

사이트 접속이 안 되는 경우 대비책을 미리 말씀드립니다. TypeScript Playground(typescriptlang.org/play)에서도 동일하게 진행할 수 있습니다. 가이드 문서에 모든 시작 코드와 풀이가 포함되어 있습니다.

시간: 30초
-->

---

# 실습 안내 — typescript-exercises.github.io

<v-click>

## 진행 방법

1. 브라우저에서 **https://typescript-exercises.github.io** 접속
2. Exercise 1부터 순서대로 진행합니다
3. 왼쪽 편집기에 코드를 작성합니다
4. 오른쪽 패널에서 실시간 컴파일 결과를 확인합니다
5. 초록색 체크가 나오면 다음 Exercise로 넘어갑니다

</v-click>

<v-click>

## 오늘 풀 문제: Exercise 1 ~ 4

| Exercise | 난이도 | 핵심 개념 |
|----------|--------|-----------|
| **Exercise 1** | 쉬움 | `type` 정의, 기본 타입 (`string`, `number`) |
| **Exercise 2** | 쉬움 | `interface`, Union 타입 (`\|`) |
| **Exercise 3** | 보통 | Literal 타입, Discriminated Union |
| **Exercise 4** | 보통 | `in` 연산자, 타입 가드 (`p is T`), 오버로드 |

</v-click>

<div class="box-blue">

**막힐 때 대처법**: 먼저 **오류 메시지를 소리내어 읽어보십시오.** 오류 메시지에 해결의 단서가 있습니다.
그래도 모르면 힌트 → 풀이 순서로 참고하십시오.

</div>

<!--
[스크립트]
실습 안내입니다.

[click]
진행 방법입니다. 사이트에 접속해서 Exercise 1부터 시작합니다. 왼쪽에 편집기가 있고 오른쪽에 컴파일 결과가 실시간으로 표시됩니다. 오류가 있으면 빨간 메시지가, 정상이면 초록색 체크가 나타납니다. 초록 체크가 나오면 다음 문제로 넘어가시면 됩니다.

[click]
오늘은 Exercise 1부터 4까지 진행합니다. Session 1에서 배운 개념들을 순서대로 적용하는 문제들입니다. Exercise 1과 2는 5분 이내로 풀 수 있습니다. Exercise 3과 4는 조금 더 생각해야 합니다. 전체 30분 안에 4까지 완료하는 것을 목표로 합니다.

막힐 때의 대처법이 중요합니다. 가장 먼저 할 것은 오류 메시지를 읽는 것입니다. TypeScript 오류 메시지는 상당히 구체적입니다. "어떤 타입이 기대되고 어떤 타입이 실제로 왔는지"가 정확하게 나옵니다. 오류 메시지를 읽다 보면 해결 방법이 보이는 경우가 많습니다. 그래도 모르겠으면 가이드 문서의 힌트를 참고하시고, 그래도 안 되면 풀이를 보면서 따라가 보시면 됩니다.

시간: 1분
-->

---

# Exercise 1-2 미리보기

## Exercise 1: `type` 정의로 User 타입 완성하기

```ts
// TODO: User 타입에 name(string)과 age(number) 필드를 추가하십시오
export type User = {
    // 여기를 완성하세요
};
```

<v-click>

## Exercise 2: `interface`와 Union 타입으로 Person 정의하기

```ts
// User와 Admin을 모두 포함하는 Person 타입을 정의하십시오
export interface Admin {
    // name, age, role 필드가 필요합니다
}

// Person은 User 또는 Admin 중 하나입니다
export type Person = unknown; // ← 이것을 수정하십시오

export function logPerson(person: Person) {
    console.log(` - ${person.name}, ${person.age}`); // ← 이것도 동작해야 합니다
}
```

<div class="box-blue">

핵심 힌트: Exercise 1은 `name: string; age: number;` 추가, Exercise 2는 `Person = User | Admin`

</div>

</v-click>

<!--
[스크립트]
Exercise 1과 2를 미리 살펴보겠습니다.

[click]
Exercise 1은 User 타입 정의입니다. `type User = {}` 안에 name과 age 필드를 추가해야 합니다. Session 1에서 배운 대로, `name: string; age: number;`를 추가하면 됩니다. 가장 간단한 문제입니다.

Exercise 2는 조금 더 복잡합니다. `Admin` 인터페이스를 완성하고, `Person` 타입을 `User | Admin`으로 정의해야 합니다. `logPerson` 함수가 `person.name`과 `person.age`에 접근하는데, User와 Admin 두 타입 모두 name과 age를 가지고 있으므로, Union 타입에서 공통 속성에는 바로 접근할 수 있습니다.

파란 박스에 핵심 힌트가 있습니다. 막히면 참고하십시오.

자, 이제 직접 풀어보겠습니다. 30분 시작합니다.

(실습 진행 — 강사는 돌아다니며 질문에 답변)

시간: 1분 (설명) + 29분 (실습)
-->

---

# Exercise 3-4 미리보기

## Exercise 3: Discriminated Union + Literal 타입

```ts
// type 필드로 User와 Admin을 구분합니다 (Discriminated Union)
export interface User {
    type: 'user';        // 리터럴 타입: 정확히 'user' 문자열만 허용
    name: string;
    occupation: string;
}
export interface Admin {
    type: 'admin';       // 리터럴 타입: 정확히 'admin' 문자열만 허용
    name: string;
    role: string;
}
// logPerson 함수의 매개변수 타입을 User에서 Person으로 변경하면 됩니다
```

<v-click>

## Exercise 4: `in` 연산자와 타입 가드

```ts
// person이 Admin인지 확인하는 타입 가드 함수
export function isAdmin(person: Person): person is Admin {
    return 'role' in person; // Admin에만 role 속성이 있습니다
}
// 반환 타입 "person is Admin" — 이 함수가 true를 반환하면
// TypeScript가 해당 블록에서 person을 Admin으로 처리합니다
```

<div class="box-yellow">

**심화 개념**: `person is Admin` 반환 타입은 "사용자 정의 타입 가드"입니다.
반환 타입이 `boolean`이면 TypeScript가 타입을 좁혀주지 않습니다.

</div>

</v-click>

<!--
[스크립트]
이미 실습을 시작하셨겠지만, Exercise 3과 4를 미리 살펴보겠습니다.

Exercise 3에서 핵심은 `type: 'user'`와 `type: 'admin'`처럼 Literal 타입을 사용하는 것입니다. 이 `type` 필드가 있으면 TypeScript가 조건문 안에서 어떤 타입인지 자동으로 구분해 줍니다. `person.type === 'admin'`이면 그 블록에서 `person`은 `Admin`입니다. `logPerson` 함수의 매개변수를 `User`에서 `Person`으로 바꾸면 됩니다.

[click]
Exercise 4의 핵심은 `isAdmin` 함수입니다. `'role' in person`은 `person` 객체에 `role` 속성이 있는지 확인합니다. Admin에는 role이 있고 User에는 없으니, role이 있으면 Admin입니다. 반환 타입에 `person is Admin`을 쓰는 것이 중요합니다. 그냥 `boolean`으로 쓰면 TypeScript가 타입을 좁혀주지 않습니다. `person is Admin`이라고 써야 `if (isAdmin(person)) { }` 블록 안에서 `person.role`에 접근할 수 있게 됩니다.

계속 실습을 진행해 주세요.

시간: 2분
-->

---

# 실습 팁 — 컴파일러 오류 읽는 법

<v-click>

## 오류 메시지 구조 이해하기

```
Argument of type 'string' is not assignable to parameter of type 'number'.
↑                ↑                                           ↑
오류 종류        실제로 넘긴 타입                            기대했던 타입
```

</v-click>

<v-click>

## 자주 보는 오류와 해결법

| 오류 메시지 | 의미 | 해결 방법 |
|------------|------|-----------|
| `Property 'X' does not exist on type 'Y'` | Y 타입에 X 속성이 없음 | interface에 X 속성 추가 |
| `Type 'X' is not assignable to type 'Y'` | X를 Y에 할당 불가 | 타입을 일치시키거나 Union으로 확장 |
| `Object literal may only specify known properties` | 타입에 없는 속성을 가진 객체 | 타입 정의에 해당 속성 추가 |
| `Property 'X' is missing in type` | 필수 속성 누락 | 객체에 X 속성 추가 또는 `?`로 선택적으로 변경 |

</v-click>

<v-click>

<div class="box-green">

**막힐 때 체크리스트**
1. 오류 메시지를 끝까지 읽었나요?
2. 어떤 타입이 기대되고, 어떤 타입을 넘겼는지 파악했나요?
3. 힌트를 한 단계씩 확인했나요?
4. 10분 이상 막히면 풀이를 보고 다음 문제로 넘어가세요

</div>

</v-click>

<!--
[스크립트]
컴파일러 오류 읽는 법을 정리해 드리겠습니다. 실습 중에 오류 메시지를 보고 무슨 말인지 모르겠다면 이 슬라이드를 참고하십시오.

[click]
TypeScript 오류 메시지는 구조가 있습니다. "Argument of type 'string' is not assignable to parameter of type 'number'"라는 오류가 나왔다면, 실제로 넘긴 타입은 string이고, 기대했던 타입은 number라는 뜻입니다. 해결법은 간단합니다. number를 넘기거나, 함수가 string도 받을 수 있도록 Union 타입으로 바꾸거나 입니다.

[click]
자주 보는 오류들을 정리했습니다. `Property 'X' does not exist on type 'Y'`는 Y 타입에 X 속성이 없다는 뜻입니다. interface에 X 속성을 추가하면 됩니다. `Object literal may only specify known properties`는 타입 정의에 없는 속성을 가진 객체를 만들었다는 뜻입니다. `Property 'X' is missing in type`은 필수 속성을 빠뜨렸다는 뜻입니다.

[click]
막힐 때 체크리스트입니다. 오류 메시지를 끝까지 읽었는지, 어떤 타입이 기대되고 어떤 타입을 넘겼는지 파악했는지 확인하십시오. 그래도 모르겠으면 힌트를 하나씩 확인하고, 10분 이상 막히면 풀이를 보고 다음 문제로 넘어가세요. 오늘 목표는 오류 없이 100% 완성하는 것이 아닙니다. TypeScript 타입 시스템을 직접 경험하는 것입니다.

실습을 계속 진행해 주세요.

시간: 2분
-->

---

# Session 1-2 마무리

## 배운 개념 정리

<v-click>

```ts {maxHeight:'340px'}
// Session 1-2에서 배운 모든 개념이 여기 담겨 있습니다
interface User {                            // 객체 구조 → interface
  type: 'user';                            // Literal 타입
  name: string;                            // 원시 타입 (소문자!)
  age: number;
  occupation?: string;                      // 선택적 속성
}

interface Admin {
  type: 'admin';
  name: string;
  age: number;
  role: string;
}

type Person = User | Admin;                 // Union 타입 → type

function describe(person: Person): string { // 함수 타입
  if (person.type === 'user') {             // Discriminated Union
    return `${person.name}: ${person.occupation ?? '직업 미상'}`; // 타입 좁히기
  }
  return `${person.name}: 관리자 (${person.role})`;
}
```

</v-click>

<div class="box-green">

**다음 세션 예고**: Session 3에서는 Vite로 React + TypeScript 프로젝트를 생성하고,
오늘 배운 타입들을 실제 React 컴포넌트에 적용합니다.

</div>

<!--
[스크립트]
Session 1과 2를 마무리합니다.

[click]
화면의 코드 하나에 Session 1-2에서 배운 거의 모든 개념이 담겨 있습니다. 한 줄씩 확인해 보겠습니다.

`interface User` — 객체 구조는 interface로 정의합니다.
`type: 'user'` — Literal 타입입니다. 정확히 이 문자열 값만 허용합니다.
`name: string` — 원시 타입은 소문자입니다.
`occupation?: string` — 물음표가 있으면 선택적 속성입니다.
`type Person = User | Admin` — Union 타입은 type으로 정의합니다.
`function describe(person: Person): string` — 매개변수와 반환 타입을 명시했습니다.
`if (person.type === 'user')` — Discriminated Union으로 타입을 좁힙니다.
`person.occupation ?? '직업 미상'` — `??`는 null이나 undefined일 때 기본값을 씁니다. Optional Chaining입니다.

실습 결과가 어떠셨나요? 처음에는 오류 메시지가 낯설어서 막막하셨을 수 있습니다. 하지만 이런 경험을 통해 TypeScript가 어떻게 도움이 되는지 느끼셨을 겁니다.

이제 10분 휴식 후 Session 3로 넘어갑니다. Session 3에서는 Vite로 React + TypeScript 프로젝트를 직접 만들고, 오늘 배운 타입들을 실제 React 컴포넌트에서 사용합니다.

시간: 2분
-->

---

# 휴식 시간

## 10분 쉬어 갑니다

**10:30 ~ 10:40**

<v-click>

## Session 3 준비사항

- 터미널(Terminal) 또는 명령 프롬프트를 열어 두십시오
- `node -v` 명령어로 Node.js가 설치되어 있는지 확인하십시오
- Node.js 18 이상이 필요합니다 (없으면 강사에게 알려 주십시오)

```bash
node -v    # v18.x.x 이상이어야 합니다
npm -v     # npm이 함께 설치되어 있습니다
```

</v-click>

<!--
[스크립트]
10분 쉬어 가겠습니다. 10시 40분에 Session 3를 시작하겠습니다.

[click]
쉬는 시간 동안 Session 3 준비를 미리 해두시면 좋겠습니다. 터미널을 열고 `node -v` 명령어로 Node.js 버전을 확인해 주십시오. Node.js 18 이상이 필요합니다. 버전이 낮거나 설치가 안 되어 있으면 강사에게 말씀해 주십시오.

쉬는 시간에 화장실을 다녀오시거나 물을 드시고 오십시오. 10분 후에 뵙겠습니다.

시간: 10분
-->

---
layout: section
---

# Session 3
## React + TypeScript 프로젝트 설정

<!--
[스크립트]
자, 오전 두 세션에서 TypeScript의 기초와 심화 타입을 배웠습니다. 이제 드디어 React를 시작할 시간입니다.

이번 세션에서는 실제로 React 프로젝트를 처음부터 만들어보겠습니다. 명령어 하나하나가 무슨 의미인지, 생성된 파일들이 어떤 역할을 하는지 꼼꼼하게 설명하겠습니다.

오늘 최종 목표인 Social Dashboard 앱을 만들려면 이 프로젝트 구조를 정확히 이해해야 합니다. 기초를 단단히 잡고 넘어가겠습니다.

시간: 1분
-->

---

# React란 무엇인가

**Meta(전 Facebook)가 만든 UI 라이브러리**

<div class="box-blue">

**핵심 아이디어: 컴포넌트(Component)**

웹 페이지를 하나의 거대한 HTML 파일로 만드는 대신,
작은 독립적인 조각(컴포넌트)으로 나누어 만든 뒤 조합합니다.

</div>

<v-click>

**레고 블록 비유**

- 레고 블록 하나 = 컴포넌트 하나
- 각 블록은 독립적으로 만들어지고, 조합하여 전체 구조물을 완성
- 같은 블록을 여러 곳에서 재사용 가능

</v-click>

<v-click>

**중요: React는 프레임워크가 아닙니다**

| 구분 | 예시 | React의 위치 |
|------|------|-------------|
| 프레임워크 | Angular, Next.js | UI 라이브러리 |
| 라이브러리 | React | **여기** |

라우팅, 상태관리 등은 별도 라이브러리 선택 조합

</v-click>

<!--
[스크립트]
React가 무엇인지부터 명확히 짚고 넘어가겠습니다.

React는 Meta, 예전의 Facebook이 만든 사용자 인터페이스 라이브러리입니다. 여기서 중요한 단어가 '라이브러리'입니다.

[click]

React의 핵심 아이디어는 레고 블록입니다. 레고를 생각해보세요. 레고 집을 만들 때 벽 하나짜리 블록, 창문 블록, 지붕 블록을 따로 만들어두고 조합하죠. React도 똑같습니다. 헤더 컴포넌트, 버튼 컴포넌트, 카드 컴포넌트를 따로 만들어서 조합합니다. 한 곳에서 블록을 고치면 그 블록을 쓰는 모든 곳에 자동으로 반영됩니다.

[click]

한 가지 꼭 짚고 싶은 부분이 있습니다. React는 프레임워크가 아니라 라이브러리입니다. Angular 같은 프레임워크는 "이 방식으로만 해야 합니다"라고 모든 걸 규정합니다. 반면 React는 UI를 만드는 것에만 집중하고, 나머지는 원하는 라이브러리를 골라서 쓸 수 있습니다. 이것이 React의 강점이기도 하고, 처음엔 뭘 써야 할지 몰라 혼란스러울 수 있는 부분이기도 합니다.

시간: 3분
-->

---

# 쇼핑몰 컴포넌트 트리

하나의 페이지를 컴포넌트로 분해하면?

```
<App>                          ← 최상위 컴포넌트
  <Header>
    <Logo />                   ← 로고 컴포넌트
    <SearchBar />              ← 검색창 컴포넌트
    <CartIcon />               ← 장바구니 아이콘 컴포넌트
  </Header>
  <ProductList>
    <ProductCard />            ← 상품 카드 (재사용!)
    <ProductCard />            ← 같은 컴포넌트, 다른 데이터
    <ProductCard />
  </ProductList>
  <Footer />
</App>
```

<v-click>

<div class="box-green">

**각 컴포넌트는 자신의 역할만 담당합니다**
- `Header`: 상단 네비게이션 전체
- `ProductCard`: 상품 카드 하나의 UI + 로직
- `Footer`: 하단 정보

`ProductCard`를 수정하면 모든 상품 카드에 일괄 반영!

</div>

</v-click>

<!--
[스크립트]
실제 쇼핑몰 페이지를 예로 들어보겠습니다. 화면에 보이는 것처럼 App 전체를 작은 조각으로 나눌 수 있습니다.

Header 안에는 Logo, SearchBar, CartIcon이 들어갑니다. ProductList 안에는 ProductCard가 반복됩니다. 3개든 100개든 같은 ProductCard 컴포넌트를 재사용합니다. 데이터만 다를 뿐입니다.

[click]

이 구조의 핵심 장점이 여기 있습니다. ProductCard 컴포넌트 하나를 수정하면 100개의 상품 카드 전부에 즉시 반영됩니다. 기존 방식대로라면 HTML 파일에서 100개의 카드를 일일이 수정해야 했겠죠.

그리고 Header를 고치고 싶으면 Header 파일만 열면 됩니다. ProductList를 고치고 싶으면 ProductList 파일만 열면 됩니다. 코드가 관심사에 따라 나뉘어 있어서 찾기 쉽고 수정하기 쉽습니다.

시간: 3분
-->

---

# 선언적 vs 명령적 프로그래밍

<div class="grid grid-cols-2 gap-4">

<div class="col-left">

**명령적 (Vanilla JS)**
"어떻게(How)" 만들지 단계별 지시

```javascript
const h1 = document.createElement('h1');
h1.textContent = '안녕하세요, 김태민님!';
container.appendChild(h1);

const button = document.createElement('button');
const isLoggedIn = true;
if (isLoggedIn) {
  button.textContent = '로그아웃';
} else {
  button.textContent = '로그인';
}
container.appendChild(button);
```

</div>

<div class="col-right">

**선언적 (React)**
"무엇(What)"이 되어야 하는지 선언

```tsx
function UserSection({ name, isLoggedIn }) {
  return (
    <div>
      <h1>안녕하세요, {name}님!</h1>
      <button>
        {isLoggedIn ? '로그아웃' : '로그인'}
      </button>
    </div>
  );
}
```

</div>

</div>

<v-click>

<div class="box-blue">

**핵심 차이**: 데이터(`isLoggedIn`)가 바뀌면 React가 DOM 업데이트를 자동으로 처리합니다.  
개발자는 "이 상태일 때 화면이 이렇게 보여야 한다"만 선언하면 됩니다.

</div>

</v-click>

<!--
[스크립트]
React를 이해하는 데 가장 중요한 개념이 바로 선언적 프로그래밍입니다. 이게 조금 추상적으로 들릴 수 있으니 직접 코드로 비교해보겠습니다.

왼쪽이 기존 Vanilla JavaScript 방식입니다. "h1 요소를 만들어서, 텍스트를 넣고, container에 붙이고, button을 만들어서, 로그인 상태를 확인해서, 텍스트를 정하고, container에 붙인다"는 식으로 단계를 일일이 지시합니다. 여기서 로그인 상태가 나중에 바뀌면 어떻게 해야 할까요? 다시 DOM을 찾아서 텍스트를 직접 바꿔야 합니다. 코드가 여기저기에 흩어지게 됩니다.

오른쪽이 React 방식입니다. "isLoggedIn이 true면 로그아웃, false면 로그인을 보여주는 UI다"라고 선언합니다. 그게 전부입니다.

[click]

핵심은 이겁니다. 데이터, 즉 `isLoggedIn` 값이 바뀌면 React가 알아서 화면을 다시 그려줍니다. 개발자가 직접 DOM을 찾아서 수정할 필요가 없습니다. 이것이 React가 복잡한 UI를 관리하기 쉽게 만들어주는 이유입니다.

시간: 4분
-->

---

# Vite로 프로젝트 생성

## 명령어 실행

```bash
npm create vite@latest my-react-app -- --template react-ts
```

<v-click>

**각 부분의 의미:**

| 부분 | 의미 |
|------|------|
| `npm create` | `npm init`의 alias. create-* 패키지로 프로젝트 초기화 |
| `vite@latest` | create-vite 패키지 최신 버전 사용 |
| `my-react-app` | 생성할 프로젝트 폴더 이름 |
| `--` | 이후 인자를 create-vite에 전달 |
| `--template react-ts` | React + TypeScript 템플릿 선택 |

</v-click>

<v-click>

<div class="box-yellow">

**왜 Vite인가?** Create React App(CRA)은 현재 비권장. Vite는 네이티브 ES Module 활용으로 개발 서버가 거의 즉시 시작됩니다. React 공식 문서도 Vite 권장.

</div>

</v-click>

<!--
[스크립트]
이제 실제로 프로젝트를 만들어보겠습니다. 다들 터미널을 열어주세요. 프로젝트를 만들 폴더로 이동한 다음에 화면에 보이는 명령어를 입력해주세요.

`npm create vite@latest my-react-app -- --template react-ts`

[click]

명령어가 길어 보이지만 하나씩 뜯어보면 간단합니다. `npm create`는 프로젝트를 초기화하는 명령어입니다. `vite@latest`는 최신 버전의 Vite를 쓰겠다는 뜻입니다. `my-react-app`은 폴더 이름인데, 원하는 이름으로 바꿔도 됩니다. `--`는 이후 옵션을 npm이 아닌 create-vite에 전달하겠다는 구분자입니다. 마지막으로 `--template react-ts`가 핵심인데, React와 TypeScript를 함께 쓰는 템플릿을 선택하는 것입니다. `react`만 입력하면 TypeScript 없이 JavaScript만 쓰는 프로젝트가 만들어집니다.

[click]

왜 Vite를 쓰는가에 대해 잠깐 설명드리겠습니다. 예전에는 Create React App, 줄여서 CRA를 많이 썼습니다. 지금도 구글에 React 시작하는 법을 검색하면 CRA 관련 글이 많이 나옵니다. 그런데 CRA는 현재 더 이상 활발하게 관리되지 않고, React 공식 문서에서도 Vite 사용을 권장하고 있습니다. Vite가 훨씬 빠르고 현대적이기 때문입니다.

시간: 4분
-->

---

# 프로젝트 설치 및 실행

```bash
cd my-react-app
npm install
npm run dev
```

<v-click>

**`npm install` — 무슨 일이 일어나는가:**

```
added 187 packages, and audited 188 packages in 8s
found 0 vulnerabilities
```

`package.json`에 적힌 모든 의존성을 `node_modules/`에 설치합니다.
187개라고 놀라지 마세요. React 하나를 설치해도 React가 필요로 하는 패키지들이 줄줄이 함께 설치됩니다.

</v-click>

<v-click>

**`npm run dev` — 개발 서버 시작:**

```
  VITE v5.x.x  ready in 342 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

브라우저에서 `http://localhost:5173` 접속!

</v-click>

<v-click>

<div class="box-red">

**HMR(Hot Module Replacement)**: 파일을 저장하면 브라우저가 자동으로 갱신됩니다.  
`App.tsx`의 텍스트를 수정하고 저장해보세요!  

</div>

</v-click>

<!--
[스크립트]
프로젝트가 생성됐으면 세 가지 명령어를 순서대로 실행합니다.

먼저 `cd my-react-app`으로 프로젝트 폴더 안으로 들어갑니다.

[click]

그 다음 `npm install`을 실행합니다. 이 명령어는 `package.json`에 적혀있는 모든 의존성 패키지를 `node_modules` 폴더에 내려받습니다. 터미널에 "added 187 packages"처럼 숫자가 크게 표시될 수 있는데, 놀라지 않아도 됩니다. React 하나를 설치하면 React가 필요로 하는 패키지들도 함께 설치되기 때문에 숫자가 불어납니다. 인터넷 연결에 따라 시간이 걸릴 수 있으니 기다려주세요.

[click]

설치가 완료되면 `npm run dev`를 실행합니다. 그러면 개발 서버가 시작되고 터미널에 `http://localhost:5173` 주소가 표시됩니다. 브라우저를 열고 이 주소로 접속해보세요. Vite + React 기본 화면이 보이면 성공입니다.

[click]

여기서 하나 꼭 체험해봐야 할 것이 있습니다. 바로 HMR입니다. Hot Module Replacement의 약자인데, 쉽게 말하면 파일을 저장하면 브라우저가 자동으로 갱신됩니다. `src/App.tsx` 파일을 열어서 `Vite + React`라고 적힌 텍스트를 `안녕하세요`로 바꾸고 저장해보세요. 브라우저가 즉시 바뀌는 것을 볼 수 있습니다. 새로고침 버튼을 누를 필요가 없습니다.

시간: 5분
-->

---

# 프로젝트 구조 전체 그림

```
my-react-app/
├── node_modules/          # 설치된 npm 패키지 (git에 포함 안 함)
├── public/
│   └── vite.svg           # 정적 자산 (URL로 직접 접근)
├── src/
│   ├── assets/
│   │   └── react.svg
│   ├── App.css            # App 컴포넌트 스타일
│   ├── App.tsx            # 루트 컴포넌트 ← 주로 여기서 작업
│   ├── index.css          # 전역 스타일
│   └── main.tsx           # React 앱 진입점
├── index.html             # SPA의 HTML 진입점
├── package.json           # 프로젝트 메타데이터 및 의존성
├── tsconfig.json          # TypeScript 컴파일러 설정
└── vite.config.ts         # Vite 빌드 도구 설정
```

<v-click>

<div class="box-blue">

**가장 자주 보는 파일:**
- `src/App.tsx` — 대부분의 작업이 여기서 시작
- `src/main.tsx` — React 앱을 HTML에 연결하는 진입점
- `index.html` — `<div id="root">` 하나가 전부인 SPA 뼈대

</div>

</v-click>

<!--
[스크립트]
생성된 프로젝트 폴더를 VS Code로 열어보겠습니다. 터미널에서 `code .`을 입력하면 현재 폴더를 바로 VS Code로 열 수 있습니다.

화면에 보이는 게 전체 구조입니다. 처음에는 파일이 많아 보여서 당황스러울 수 있는데, 실제로 우리가 작업하는 파일은 몇 개 안 됩니다.

`node_modules`는 npm install로 설치된 모든 패키지가 들어있는 폴더입니다. 크기가 수백 메가바이트가 될 수 있고, git에는 포함하지 않습니다. `.gitignore` 파일에 이미 등록되어 있습니다.

`src` 폴더가 우리가 작성하는 소스코드가 들어가는 곳입니다.

[click]

가장 자주 보게 될 파일 세 가지만 기억해두세요. `src/App.tsx`는 대부분의 작업이 시작되는 루트 컴포넌트입니다. `src/main.tsx`는 React 앱을 HTML에 연결하는 진입점입니다. `index.html`은 페이지 전체를 담는 뼈대 파일인데, 사실 내용이 거의 없습니다. `<div id="root">` 하나가 핵심입니다. React가 이 div 안에 모든 UI를 그려넣습니다.

시간: 3분
-->

---

# `index.html` → `main.tsx` → `App.tsx` 흐름

<v-click>

**1단계: `index.html`** — 브라우저가 처음 로드하는 파일

```html
<body>
  <div id="root"></div>   <!-- React가 여기에 그려넣음 -->
  <script type="module" src="/src/main.tsx"></script>
</body>
```

</v-click>

<v-click>

**2단계: `src/main.tsx`** — React를 DOM에 연결

```tsx
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

ReactDOM.createRoot(document.getElementById('root')!)
  .render(<App />)
// getElementById('root') → index.html의 <div id="root">를 찾아서
// 그 안에 <App /> 컴포넌트를 그려넣음
```

</v-click>

<v-click>

**3단계: `src/App.tsx`** — 실제 화면 내용

```tsx
function App() {
  return <h1>Hello React!</h1>  // 여기서부터 시작
}
export default App
```

</v-click>

<!--
[스크립트]
처음에 React 프로젝트 구조를 보면 "어디서부터 실행되는 거지?"가 헷갈립니다. 이 흐름을 한 번만 이해해두면 나중에 절대 헷갈리지 않습니다.

[click]

첫 번째로, 브라우저가 열면 `index.html`을 먼저 읽습니다. 이 파일을 열어보면 내용이 거의 없습니다. 중요한 것 딱 두 줄입니다. `<div id="root">`라는 빈 div가 있고, `main.tsx` 파일을 로드하는 스크립트 태그가 있습니다.

[click]

두 번째로, `main.tsx`가 실행됩니다. 이 파일이 하는 일은 딱 하나입니다. HTML에서 `id가 root인 div`를 찾아서, 그 안에 `App` 컴포넌트를 그려넣습니다. `getElementById('root')!` 끝에 느낌표가 붙어있는데, 이건 TypeScript에게 "이 값은 절대 null이 아니다"라고 보장하는 것입니다. `index.html`에 반드시 `id="root"` div가 있으니까 괜찮습니다.

[click]

세 번째로, `App.tsx`가 화면에 그려집니다. 결국 우리가 `App.tsx`에 작성한 내용이 `index.html`의 빈 div 안에 들어가게 됩니다. 이 흐름이 React 앱의 전체 시작 구조입니다.

전환: 이제 tsconfig.json을 잠깐 보고, 바로 첫 번째 컴포넌트를 직접 만들어보겠습니다.
시간: 4분
-->

---

# `tsconfig.json` 핵심 옵션

```json {1-3|4-5|6-7|8-9}
{
  "compilerOptions": {
    "strict": true,          // 모든 엄격한 타입 검사 활성화 (권장)
    "jsx": "react-jsx",      // JSX → React 자동 변환 (import React 불필요)
    "noEmit": true,          // JS 파일 생성 안 함 (빌드는 Vite가 담당)
    "noUnusedLocals": true,  // 사용 안 한 변수 선언 시 오류
    "noUnusedParameters": true, // 사용 안 한 파라미터 선언 시 오류
    "target": "ES2020",      // 컴파일 대상 JavaScript 버전
    "lib": ["ES2020", "DOM"] // 사용 가능한 API (브라우저 DOM 포함)
  }
}
```

<v-click>

<div class="box-yellow">

**실무 팁**: `"strict": true`를 처음에 켜두면 오류가 많이 나와서 힘들 수 있습니다. 하지만 이 오류들이 나중에 생길 버그를 미리 잡아줍니다. 처음부터 strict 모드로 개발하는 것을 강력히 권장합니다.

</div>

</v-click>

<!--
[스크립트]
`tsconfig.json`은 TypeScript 컴파일러 설정 파일입니다. 모든 옵션을 외울 필요는 없고, 핵심적인 것 몇 가지만 이해하면 됩니다.

줄별로 살펴보겠습니다. `"strict": true`가 가장 중요합니다. TypeScript의 모든 엄격한 검사를 켜는 옵션입니다. `null` 체크, 타입 추론 강화 등이 모두 활성화됩니다. 처음에는 오류가 더 많이 나오지만, 그만큼 버그도 일찍 잡힙니다.

[click]

`"jsx": "react-jsx"` 옵션은 JSX 문법을 어떻게 변환할지 설정합니다. `react-jsx`로 설정하면 파일 맨 위에 `import React from 'react'`를 안 써도 됩니다. React 17 이전에는 반드시 써야 했지만, 이 옵션 덕분에 생략 가능합니다.

[click]

`"noEmit": true`는 TypeScript가 JavaScript 파일을 직접 생성하지 않는다는 뜻입니다. TypeScript는 타입 검사만 하고, 실제 빌드는 Vite가 담당합니다. `"noUnusedLocals"`와 `"noUnusedParameters"`는 사용하지 않는 변수나 파라미터가 있으면 오류를 냅니다. 코드를 깔끔하게 유지하는 데 도움이 됩니다.

[click]

`"target": "ES2020"`은 컴파일 대상 JavaScript 버전을 지정합니다. `"lib": ["ES2020", "DOM"]`은 사용 가능한 API를 지정합니다. DOM이 포함되어 있어야 `document.getElementById` 같은 브라우저 API를 쓸 수 있습니다.

[click]

실무 팁으로, strict 모드를 처음부터 켜두세요. 나중에 큰 프로젝트에서 strict를 켜려고 하면 수백 개의 오류가 쏟아져서 수정하기 힘듭니다. 처음부터 켜두고 오류를 하나씩 고치는 습관을 들이는 게 훨씬 낫습니다.

시간: 3분
-->

---

# 첫 번째 컴포넌트: Greeting.tsx

`src/Greeting.tsx` 파일을 새로 만들어보겠습니다.

```tsx {1-4|6-10|12-15|17}{maxHeight:'340px'}
// src/Greeting.tsx

interface GreetingProps {
  name: string;
  role?: string;  // ? = 선택적 prop (없어도 오류 없음)
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

<v-click>

<div class="box-blue">

**구조 분해 할당**: `({ name, role }: GreetingProps)` = props를 분해해서 바로 변수로 사용. `props.name` 대신 `name`으로 쓸 수 있습니다.

</div>

</v-click>

<!--
[스크립트]
이제 첫 번째 컴포넌트를 직접 만들어보겠습니다. VS Code에서 `src` 폴더 우클릭 → New File로 `Greeting.tsx` 파일을 만들어주세요.

코드를 한 줄씩 살펴보겠습니다. 맨 위에 `interface GreetingProps`가 있습니다. 이 컴포넌트가 받을 props의 타입을 정의합니다. `name: string`은 필수 prop이고, `role?: string`은 선택적 prop입니다. 물음표가 붙으면 이 prop은 없어도 됩니다. 타입은 `string | undefined`가 됩니다.

[click]

함수 선언부를 보면 `({ name, role }: GreetingProps)`라고 되어 있습니다. 이게 구조 분해 할당입니다. props 객체에서 name과 role을 꺼내서 바로 변수로 사용합니다. `props.name`이라고 쓰는 대신 그냥 `name`으로 쓸 수 있습니다.

[click]

return 안을 보면 `{name}`처럼 중괄호로 변수를 넣고 있습니다. 이게 JSX 문법입니다. 중괄호 안에 JavaScript 표현식을 넣을 수 있습니다. `{role && <p>역할: {role}</p>}`는 role이 있을 때만 p 태그를 렌더링하는 조건부 렌더링입니다.

[click]

마지막에 `export default Greeting`으로 컴포넌트를 내보냅니다. 다른 파일에서 이 컴포넌트를 가져다 쓸 수 있게 됩니다.

[click]

구조 분해 할당 한 번 더 강조할게요. 이 패턴이 React에서 매우 자주 쓰입니다. 처음엔 `props.name`이라고 쓰고 싶어질 수 있는데, 실제 현업 코드는 거의 100% 구조 분해 할당을 씁니다.

시간: 5분
-->

---

# App.tsx에서 Greeting 사용

TypeScript 자동완성의 위력을 체험해봅시다.

```tsx {1|3-12|14}
// src/App.tsx
import Greeting from './Greeting';

function App() {
  return (
    <div>
      <Greeting name="김태민" role="수강생" />
      <Greeting name="이선생" role="강사" />
      <Greeting name="박철수" />   {/* role 없어도 OK */}
    </div>
  );
}

export default App;
```

<v-click>

<div class="box-green">

**TypeScript + React의 강점 체험:**
1. `<Greeting ` 입력 후 스페이스 → `name`, `role` 자동완성 제안
2. `name` prop을 빠뜨리면 → 빨간 줄 오류 즉시 표시
3. `name={123}` 처럼 잘못된 타입 넣으면 → 오류 즉시 표시

컴파일 전에 실수를 잡아줍니다!

</div>

</v-click>

<!--
[스크립트]
이제 만든 Greeting 컴포넌트를 App.tsx에서 사용해보겠습니다. App.tsx를 열어서 기존 내용을 전부 지우고 화면의 코드를 입력해주세요. 맨 위에 `import Greeting from './Greeting'`으로 방금 만든 컴포넌트를 가져옵니다.

[click]

그 다음 JSX 안에서 `<Greeting name="김태민" role="수강생" />`처럼 HTML 태그처럼 사용합니다. 세 번째에는 `role` 없이 `name`만 전달하고 있습니다. `role`이 선택적 prop이라서 에러가 나지 않습니다.

[click]

마지막 줄은 `export default App`입니다. 이 파일의 메인 컴포넌트를 내보냅니다. 파일을 저장하면 브라우저에서 세 가지 인사말이 표시됩니다.

[click]

이제 TypeScript와 React의 강점을 직접 체험해봅시다. VS Code에서 `<Greeting ` 입력 후 스페이스를 누르면 name, role 자동완성이 뜹니다. 제가 직접 해볼게요.

그 다음, `name` prop을 지우면 어떻게 되는지 보세요. 즉시 빨간 줄 오류가 표시됩니다. 브라우저를 열기도 전에 실수를 잡아주는 겁니다.

`name={123}`처럼 숫자를 넣어도 오류가 납니다. `name`은 string인데 number를 넣었기 때문입니다.

이것이 TypeScript를 React와 함께 쓰는 핵심 이유입니다. props를 잘못 전달하는 실수를 코드 작성 시점에 바로 잡아줍니다.

시간: 4분
-->

---

# named export vs default export

```tsx {1-6|8-13|15-20}{maxHeight:'340px'}
// ── default export ──────────────────────────────
// 파일 하나에 하나만 가능. import 시 이름 자유롭게 변경 가능.
export default function Greeting() { ... }

import Greeting from './Greeting';    // 정상
import MyGreeting from './Greeting';  // 이것도 정상! (이름 변경 가능)


// ── named export ─────────────────────────────────
// 파일 하나에 여러 개 가능. import 시 반드시 원래 이름 사용.
export function Greeting() { ... }
export function Farewell() { ... }
export const MAX_USERS = 100;

import { Greeting, Farewell } from './Greeting';      // 중괄호 필수
import { Greeting as Hello } from './Greeting';       // 별칭 사용 시 as
```

<v-click>

<div class="box-yellow">

**현업 관례**: 컴포넌트 파일은 `export default`, 여러 유틸리티/상수는 `named export`. 가장 중요한 것은 **팀 내 일관성**입니다.

</div>

</v-click>

<!--
[스크립트]
export 방식이 두 가지가 있어서 처음에 헷갈릴 수 있습니다. default export와 named export입니다. default export는 파일당 하나만 허용됩니다. 가져올 때 이름을 마음대로 바꿀 수 있습니다. `import Greeting from './Greeting'`이라고 써도 되고, `import MyGreeting from './Greeting'`이라고 써도 됩니다. 둘 다 같은 것을 가져옵니다.

[click]

named export는 파일 하나에서 여러 개를 내보낼 수 있습니다. 가져올 때는 반드시 중괄호를 쓰고 원래 이름을 사용해야 합니다. 이름을 바꾸고 싶으면 `as` 키워드를 씁니다.

[click]

import 문법을 정리하면, default export는 중괄호 없이 이름 자유롭게, named export는 중괄호 필수에 원래 이름을 사용해야 합니다. 별칭을 쓰려면 `as`를 사용합니다.

[click]

현업에서는 어떻게 쓰느냐면, 컴포넌트 파일에는 거의 default export를 씁니다. 유틸리티 함수나 상수처럼 한 파일에서 여러 개를 내보낼 때는 named export를 씁니다. 가장 중요한 건 팀 내에서 일관성 있게 쓰는 것입니다. 오늘 수업에서는 컴포넌트는 모두 default export로 통일하겠습니다.

시간: 3분
-->

---

# JSX 규칙 1-2: 루트 요소 + className

**규칙 1: 반드시 하나의 최상위(루트) 요소**

<div class="grid grid-cols-2 gap-4">

<div class="col-left">

```tsx
// 오류 — 루트 요소가 2개
function Wrong() {
  return (
    <h1>제목</h1>
    <p>본문</p>   // ❌
  );
}
```

</div>

<div class="col-right">

```tsx
// 해결 — Fragment로 감싸기
function Right() {
  return (
    <>
      <h1>제목</h1>
      <p>본문</p>
    </>
  );
}
```

</div>

</div>

<v-click>

**규칙 2: `class` 대신 `className`**

<div class="box-red">

```tsx
// ❌ HTML처럼 class를 쓰면 오류
<div class="container">...</div>

// ✅ JSX에서는 반드시 className
<div className="container">...</div>
// class는 JavaScript 예약어! 마찬가지로 for → htmlFor
```

</div>

</v-click>

<!--
[스크립트]
JSX는 HTML과 거의 비슷하게 생겼지만, 몇 가지 중요한 규칙이 있습니다. 이것들을 모르면 오류가 나도 왜 나는지 모를 수 있으니 꼭 기억해두세요.

첫 번째 규칙, 컴포넌트는 반드시 하나의 최상위 요소를 반환해야 합니다. 왼쪽처럼 h1과 p를 나란히 반환하면 오류가 납니다. React는 컴포넌트 하나가 하나의 요소 트리를 반환해야 한다고 규정합니다.

오른쪽처럼 `<>`와 `</>`로 감싸면 됩니다. 이것을 Fragment라고 합니다. 실제 DOM에 추가적인 div 같은 게 생기지 않아서 div로 감싸는 것보다 더 좋습니다.

[click]

두 번째 규칙, HTML에서는 `class`를 쓰지만 JSX에서는 `className`을 씁니다. `class`가 JavaScript의 예약어이기 때문입니다. JavaScript에서 클래스를 선언할 때 `class` 키워드를 쓰잖아요. 그래서 혼동을 피하기 위해 JSX에서는 `className`을 씁니다.

비슷하게, HTML의 `<label for="id">`도 JSX에서는 `<label htmlFor="id">`로 써야 합니다. 처음에 자주 하는 실수입니다.

시간: 4분
-->

---

# JSX 규칙 3-4: 중괄호 표현식 + 조건부 렌더링

**규칙 3: `{}`로 JavaScript 표현식 삽입**

```tsx {1-5|6-9}
const name = '김철수';
const age = 25;

// 변수, 연산, 함수 호출 모두 가능
<h1>{name}</h1>                    // 변수
<p>내년 나이: {age + 1}세</p>      // 연산
<p>길이: {name.length}글자</p>     // 메서드 호출
<span>{isOK ? '확인' : '취소'}</span>  // 삼항 연산자
```

<v-click>

**규칙 4: 조건부 렌더링 패턴**

```tsx
// 패턴 1: && 연산자 (보여주거나 / 안 보여주거나)
{isLoggedIn && <p>환영합니다!</p>}

// 패턴 2: 삼항 연산자 (A 보여주거나 / B 보여주거나)
{isLoggedIn ? <LogoutButton /> : <LoginButton />}

// 패턴 3: if 문은 {} 안에 직접 못 씀 — 함수 밖에서 처리
if (!isVisible) return null;  // 컴포넌트 return 전에 처리
```

</v-click>

<v-click>

<div class="box-red">

**흔한 실수 — && 와 숫자 0:**
`{count && <p>{count}개</p>}` → count가 0이면 "0"이 화면에 출력됩니다!
`{count > 0 && <p>{count}개</p>}` 처럼 명시적 boolean으로 변환하세요.

</div>

</v-click>

<!--
[스크립트]
세 번째 규칙입니다. JSX 안에서 JavaScript 코드를 실행하거나 변수를 표시하려면 중괄호로 감쌉니다. 변수를 그냥 넣을 수도 있고, `age + 1` 같은 연산도 됩니다. `name.length` 같은 메서드 호출도 됩니다. 중괄호 안에는 값을 반환하는 '표현식'이면 무엇이든 올 수 있습니다. 반면 `if`, `for`, `while` 같은 '구문'은 중괄호 안에 직접 넣을 수 없습니다.

[click]

삼항 연산자도 중괄호 안에서 사용할 수 있습니다. `{isOK ? '확인' : '취소'}`처럼 조건에 따라 다른 값을 표시할 수 있습니다.

[click]

네 번째 규칙, 조건부 렌더링입니다. 어떤 조건에 따라 UI를 보여주거나 숨기는 패턴입니다. 세 가지 패턴이 있습니다. 첫째로 `&&` 연산자입니다. 왼쪽이 true이면 오른쪽을 렌더링하고, false이면 아무것도 렌더링하지 않습니다. 있거나 없거나 할 때 씁니다. 둘째로 삼항 연산자입니다. A를 보여주거나 B를 보여주는 경우에 씁니다. 셋째로 컴포넌트 return 전에 if 문으로 처리하는 방법입니다. `if (!isVisible) return null`처럼 조건이 맞지 않으면 null을 반환해서 아무것도 렌더링하지 않습니다.

[click]

여기서 Java나 Python 개발자분들이 자주 빠지는 함정이 있습니다. `{count && <p>{count}개</p>}` 이 코드, count가 0이면 어떻게 될까요? "아무것도 안 보이겠지"라고 생각하기 쉽지만, 실제로는 화면에 "0"이라는 숫자가 그대로 출력됩니다. JavaScript의 `&&` 연산자는 왼쪽이 falsy이면 왼쪽 값 자체를 반환하기 때문입니다. 0이 falsy라서 0이 반환되고, 숫자 0은 화면에 표시됩니다. `count > 0 &&`처럼 명시적으로 boolean으로 만들어서 쓰세요.

시간: 5분
-->

---

# JSX 규칙 5: 리스트 렌더링 + key prop

**`.map()`으로 배열을 JSX로 변환**

```tsx {1-6|8-14|16-21}{maxHeight:'340px'}
const students = [
  { id: 1, name: '김철수', grade: 'A' },
  { id: 2, name: '이영희', grade: 'B' },
  { id: 3, name: '박민준', grade: 'A' },
];

// ✅ key에 안정적인 ID 사용
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

// ❌ 인덱스를 key로 사용하면 안 됩니다 (항목 추가/삭제 시 버그 위험)
{students.map((student, index) => (
  <li key={index}>{student.name}</li>  // 피해야 함
))}
```

<v-click>

<div class="box-yellow">

**`key` prop 규칙**: 같은 리스트 안에서 유일한 값이어야 합니다. 데이터베이스 ID처럼 안정적이고 고유한 값을 사용하세요. `key`를 빠뜨리면 콘솔에 경고가 나타납니다.

</div>

</v-click>

<!--
[스크립트]
배열 데이터를 화면에 목록으로 표시할 때는 `.map()` 메서드를 사용합니다. 이 패턴은 React에서 정말 자주 씁니다. Social Dashboard 실습에서도 게시글 목록, 사용자 목록을 표시할 때 이 방식을 씁니다. students 배열이 있고, 이 배열을 JSX로 변환하는 코드를 보겠습니다.

[click]

`students.map((student) => <li>{...}</li>)`처럼 배열의 각 요소를 JSX로 변환합니다. 이때 반드시 `key` prop을 붙여야 합니다. `key={student.id}`처럼 각 항목을 구별할 수 있는 고유한 값을 넣습니다.

[click]

왜 key가 필요할까요? React는 리스트가 변경될 때 어떤 항목이 추가되고, 변경되고, 삭제되었는지 추적해야 합니다. key가 있어야 "아, 이 항목이 바뀌었구나"를 효율적으로 판단할 수 있습니다.

인덱스를 key로 쓰는 것은 왜 안 될까요? 항목을 중간에 삭제하거나 순서가 바뀌면 인덱스도 바뀌어서 React가 잘못 추적합니다. 데이터베이스 ID처럼 항목 자체에 붙은 고유한 값을 쓰세요.

[click]

key를 빠뜨리면 브라우저 개발자 도구 콘솔에 "Warning: Each child in a list should have a unique 'key' prop" 경고가 나타납니다. 직접 해보세요. key를 지워보고 콘솔에서 경고를 확인해보겠습니다.

시간: 5분
-->

---

# 독립 실습: ProductCard 컴포넌트

<div class="practice-point">

**10분 독립 실습** — `src/ProductCard.tsx` 파일을 새로 만들어보세요!

</div>

<div class="grid grid-cols-2 gap-4">
<div>

**요구사항 (Props):**
```tsx
interface ProductCardProps {
  name: string;         // 상품 이름 (필수)
  price: number;        // 가격 (필수)
  inStock: boolean;     // 재고 여부 (필수)
  description?: string; // 설명 (선택)
}
```

</div>
<div>

**출력 내용:**
- `<h2>`로 상품 이름
- `{price.toLocaleString()}원` 형식으로 가격
- `inStock` true→"재고 있음" / false→"품절"
- `description` 있으면 표시, 없으면 숨김

**힌트:** `toLocaleString()`으로 `1,234,567` 형식 변환

</div>
</div>

<!--
[스크립트]
이제 10분 동안 혼자서 해보는 시간입니다. `src/ProductCard.tsx` 파일을 새로 만들어서 요구사항을 만족하는 컴포넌트를 작성해주세요.

interface를 먼저 정의하고, 함수 컴포넌트를 만들고, 조건부 렌더링을 적용하면 됩니다. 오전에 배운 TypeScript 인터페이스와 방금 배운 JSX 규칙을 종합해서 써보는 것입니다.

막히시면 손을 들어주세요. 힌트가 필요한 분들을 위해 `price.toLocaleString()`은 숫자를 천 단위 콤마가 있는 형식으로 바꿔줍니다.

10분 후에 솔루션 코드를 함께 리뷰하겠습니다.

[Q&A 대비]
Q: interface를 어디에 써야 하나요?
A: 컴포넌트 함수 위에 씁니다.

Q: 조건부 렌더링을 어떻게 해야 하나요?
A: `{inStock ? '재고 있음' : '품절'}`처럼 삼항 연산자를 쓰거나, `{description && <p>{description}</p>}`처럼 && 연산자를 씁니다.

시간: 10분
-->

---
layout: section
---

# 점심시간
## 11:40 — 13:00

**오후 첫 세션(13:00)에 돌아오면:**

Session 4: React QuickStart — 틱택토 게임 만들기<br>
`useState` 훅으로 상태 관리 시작<br>
클릭하면 반응하는 인터랙티브 UI 만들기

<div style="margin-top: 2rem">

**점심시간 전 체크리스트:**

`npm run dev` 실행 중인 터미널 탭 그대로 유지 (또는 종료 후 오후에 재시작)<br>
Node.js 설치 안 된 분은 강사에게 말씀해주세요 (점심 중 설치 도움)<br>
VS Code `Greeting.tsx`, `ProductCard.tsx` 작업 저장 확인

</div>

<!--
[스크립트]
수고하셨습니다! 오전 세션이 모두 끝났습니다. 점심 드시고 오후 1시에 돌아오시면 됩니다.

오후에는 오늘 수업의 하이라이트인 React QuickStart를 진행합니다. 틱택토 게임을 만들면서 useState 훅을 배우고, 클릭하면 실제로 반응하는 인터랙티브 UI를 만들어봅니다.

점심 드시기 전에 체크리스트를 확인해주세요. 개발 서버는 끄셔도 되고, 켜둬도 됩니다. Node.js 설치에 문제가 있으신 분은 지금 말씀해주시면 점심시간 중에 도와드리겠습니다.

시간: 1분
-->

---
layout: section
---

# Session 4
## React QuickStart: 틱택토 게임 만들기

<!--
[스크립트]
점심 잘 드셨나요? 오후 첫 세션입니다. 지금부터 React의 핵심인 상태(State) 관리를 배웁니다.

오전에 Props를 배웠는데, Props는 부모가 자식에게 전달하는 읽기 전용 데이터였습니다. 이제 State를 배울 차례입니다. State는 컴포넌트가 스스로 기억하고 변경할 수 있는 데이터입니다.

React 공식 튜토리얼 예제인 틱택토 게임을 만들면서 State, 이벤트 핸들링, 상태 끌어올리기를 자연스럽게 익히겠습니다.

시간: 1분
-->

---

# Props vs State

<div class="grid grid-cols-2 gap-4">

<div>

| 구분 | Props | State |
|------|-------|-------|
| **출처** | 부모 컴포넌트 | 컴포넌트 자신 |
| **변경 주체** | 부모만 변경 가능 | 자신이 `setState`로 변경 |
| **재렌더링** | 부모가 새 Props 내릴 때 | `setState` 호출 시 |
| **비유** | 함수의 파라미터 | 내부 메모리 |

</div>

<div>

**식당 비유:**

<v-click>

<div class="box-blue">

**Props = 주문서**
손님(부모)이 내용을 결정.
주방(자식)은 받은 대로 처리.
주방이 주문서 내용을 바꿀 수 없음.

</div>

</v-click>

<v-click>

<div class="box-green">

**State = 재고 목록**
주방이 스스로 관리.
재료를 쓸 때마다 주방이 직접 업데이트.
손님이 알 필요 없는 내부 정보.

</div>

</v-click>

</div>

</div>

<!--
[스크립트]
오전에 Props를 배웠습니다. 이제 State를 배울 차례인데, 먼저 두 개념의 차이부터 명확히 잡겠습니다.

표를 보면 Props와 State의 차이가 나옵니다. Props는 부모로부터 오고, State는 컴포넌트 자신이 관리합니다. Props는 부모만 변경할 수 있지만, State는 컴포넌트 자신이 `setState` 함수를 호출해서 변경합니다.

[click]

식당 비유로 설명하면 이렇습니다. Props는 손님이 주는 주문서입니다. 손님이 "파스타 주세요"라고 주문서를 주면, 주방은 그대로 만들어야 합니다. 주방이 주문서 내용을 마음대로 바꿀 수 없습니다.

[click]

State는 주방의 재고 목록입니다. 재고가 얼마나 남았는지는 주방이 스스로 관리합니다. 재료를 쓸 때마다 주방이 직접 업데이트합니다. 손님은 이 정보를 알 필요가 없습니다.

이 비유를 머릿속에 새겨두세요. 앞으로 "이 데이터가 Props인가, State인가?" 헷갈릴 때 이 비유를 떠올리면 됩니다.

전환: 그런데 왜 그냥 일반 변수를 쓰면 안 되는 걸까요? 다음 슬라이드에서 직접 확인해보겠습니다.
시간: 4분
-->

---

# 왜 일반 변수(let)로는 안 되는가

```tsx {1-4|6-13|15-20}{maxHeight:'260px'}
// ❌ 이 코드는 동작하지 않습니다
function Counter() {
  let count = 0; // 일반 변수

  function handleClick() {
    count = count + 1;
    console.log('클릭! count =', count); // 콘솔에는 1, 2, 3...으로 증가
  }

  return (
    <div>
      <p>클릭 수: {count}</p>   {/* 화면은 영원히 0에서 바뀌지 않음 */}
      <button onClick={handleClick}>+1</button>
    </div>
  );
}

// ✅ useState를 쓰면 됩니다
function Counter() {
  const [count, setCount] = useState(0);
  // setCount를 호출할 때마다 React가 화면을 다시 그립니다
}
```

<v-click>

<div class="box-red">

**React가 화면을 다시 그리는 조건은 단 두 가지:**
1. **State가 변경될 때** (`setState` 함수 호출)
2. **Props가 변경될 때** (부모가 새 값을 내릴 때)

일반 변수가 바뀌어도 React는 전혀 알지 못합니다!

</div>

</v-click>

<!--
[스크립트]
처음 React를 배우면 이런 의문이 생깁니다. "그냥 let 변수 쓰면 되지, 왜 useState가 필요한가?"

[click]

화면의 코드를 보세요. `let count = 0`으로 일반 변수를 만들고, 버튼을 클릭하면 count를 증가시킵니다. 콘솔을 보면 실제로 1, 2, 3...으로 올라갑니다. 그런데 화면은 여전히 0입니다.

왜일까요? 버튼을 아무리 눌러도 화면이 바뀌지 않습니다.

[click]

이유는 React의 동작 방식 때문입니다. React가 화면을 다시 그리는 조건이 딱 두 가지입니다. State가 변경되거나, Props가 변경될 때입니다. 일반 변수 값이 바뀐다고 해서 React는 전혀 알지 못합니다. "아, 뭔가 바뀌었으니 화면을 갱신해야겠다"는 신호를 받지 못하는 겁니다.

반면 useState를 쓰고 setCount를 호출하면, React에 "State가 바뀌었으니 화면을 다시 그려줘"라는 신호가 전달됩니다. 그러면 React가 컴포넌트 함수를 다시 실행하고 화면을 갱신합니다.

이것이 useState가 필요한 근본적인 이유입니다.

전환: 그러면 useState의 정확한 문법을 알아보겠습니다.
시간: 4분
-->

---

# `useState` 기본 문법

```tsx {1|3|4-6|8-11}
import { useState } from 'react';

function Counter() {
  //      ↓ 현재 값    ↓ 값을 바꾸는 함수     ↓ 초기값
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1); // 호출하면 React가 화면을 다시 그림
  }
  // ...
}
```

<v-click>

**TypeScript 타입 추론 + 제네릭:**

```tsx {1-3|5-7}
// 초기값이 있으면 TypeScript가 자동 추론
const [count, setCount] = useState(0);       // ← number 추론
const [name, setName]   = useState('');      // ← string 추론
const [flag, setFlag]   = useState(false);   // ← boolean 추론

// 초기값이 null이거나 타입이 복잡하면 제네릭 명시
const [user, setUser] = useState<User | null>(null);  // User | null
const [items, setItems] = useState<string[]>([]);      // string[]
```

</v-click>

<!--
[스크립트]
이제 useState 문법을 정확히 알아보겠습니다.

[click]

맨 위에 `import { useState } from 'react'`로 React에서 useState를 가져옵니다.

[click]

그 다음이 핵심입니다. `const [count, setCount] = useState(0)`. 이 한 줄이 처음에 낯설게 보일 수 있는데, 배열 구조 분해 할당입니다. useState는 항상 두 요소짜리 배열을 반환합니다. 첫 번째가 현재 값, 두 번째가 그 값을 바꾸는 함수입니다.

이름 짓는 관례가 있습니다. 값은 `count`, 함수는 `setCount`처럼 `set`을 앞에 붙입니다. `name`과 `setName`, `isOpen`과 `setIsOpen`처럼요.

[click]

setCount를 호출하면 React에 신호가 가고, React가 컴포넌트를 다시 렌더링합니다. 다시 렌더링될 때 count에는 새로운 값이 들어있습니다.

[click]

TypeScript에서는 초기값이 있으면 타입을 자동으로 추론합니다. 0을 넣으면 number로, 빈 문자열을 넣으면 string으로 알아서 추론합니다. 그런데 초기값이 null이거나, 나중에 다른 타입이 들어올 경우에는 제네릭으로 명시해야 합니다. `useState<User | null>(null)`처럼 꺾쇠 안이 타입이고 괄호 안이 초기값입니다.

시간: 4분
-->

---

# Tic-Tac-Toe: 컴포넌트 트리 설계

**왜 틱택토인가?** 9개 칸이라는 단순 구조에 React 핵심이 모두 들어있습니다.

```
Board (게임판 전체)
  ├── Square (칸 0)
  ├── Square (칸 1)
  ├── Square (칸 2)
  ├── ...
  └── Square (칸 8)
```

<v-click>

**Step 1-3: 구조 이해**

```tsx {1-5|7-15}{maxHeight:'200px'}
// Square: 틱택토 칸 하나
interface SquareProps {
  value: string | null; // 'X', 'O', 또는 null(비어있음)
}
function Square({ value }: SquareProps) {
  return <button className="square">{value}</button>;
}

// Board: 9개 칸을 담는 게임판
function Board() {
  return (
    <div className="board-row">
      <Square value="X" />
      <Square value="O" />
      <Square value={null} />
    </div>
  );
}
```

</v-click>

<!--
[스크립트]
React 공식 팀이 틱택토를 공식 튜토리얼로 선택한 이유가 있습니다. 9개 칸이라는 단순한 구조 안에 컴포넌트 분리, Props, State, 이벤트 핸들링, 상태 끌어올리기 이 다섯 가지가 모두 들어있습니다.

먼저 컴포넌트 트리를 설계합니다. Board라는 컴포넌트가 전체 게임판이고, 그 안에 Square 컴포넌트 9개가 있습니다.

[click]

코드를 보면, Square는 `value`라는 Props를 받아서 버튼 하나를 렌더링합니다. value는 `'X'`, `'O'`, 또는 `null`일 수 있습니다. TypeScript의 Union 타입으로 `string | null`로 표현합니다.

Board는 Square를 9개 배치해서 3행 3열 게임판을 만듭니다. 지금은 하드코딩된 값을 넣어서 구조만 만들었습니다.

이 코드를 `src/App.tsx`에 입력해보세요. 화면에 세 개의 버튼이 보이면 됩니다. 이제 여기서 출발해서 실제 게임을 만들어보겠습니다.

시간: 5분
-->

---

# Step 4-5: 클릭 이벤트 + Square State

**Step 4: onClick 연결**

```tsx {1-9}
function Square({ value }: SquareProps) {
  function handleClick() {
    console.log('Square 클릭됨!');
  }

  return (
    <button className="square" onClick={handleClick}>
      {value}
    </button>
  );
}
```

<v-click>

<div class="box-red">

**가장 흔한 실수 — 괄호 유무:**

```tsx
// ❌ onClick={handleClick()}  ← 렌더링될 때 즉시 실행! 클릭 시가 아님
// ✅ onClick={handleClick}    ← 클릭될 때 실행. 함수 자체를 전달

// ❌ onClick={handleClick(i)} ← 즉시 실행
// ✅ onClick={() => handleClick(i)} ← 클릭될 때 실행. 화살표 함수로 감싸기
```

Python도 동일: `button.command = handle_click` (O) vs `button.command = handle_click()` (X)

</div>

</v-click>

<!--
[스크립트]
버튼을 클릭했을 때 뭔가 일어나도록 이벤트를 연결해보겠습니다.

Square 컴포넌트 안에 `handleClick` 함수를 정의하고, `onClick={handleClick}`으로 연결합니다. 저장 후 버튼을 클릭하면 콘솔에 메시지가 출력됩니다.

[click]

여기서 반드시 멈추고 강조해야 할 부분이 있습니다. 정말 자주 하는 실수입니다.

`onClick={handleClick()}`처럼 괄호를 붙이면 안 됩니다. 괄호가 있으면 JSX가 렌더링될 때 즉시 함수가 실행됩니다. 클릭을 기다리지 않고 바로 실행됩니다. 게다가 handleClick의 반환값인 undefined가 onClick에 전달되어서 클릭해도 아무 일이 일어나지 않습니다.

`onClick={handleClick}`처럼 괄호 없이 함수 자체를 전달해야 합니다. "클릭되면 이 함수를 실행해"라고 함수 참조를 전달하는 것입니다.

인자가 필요한 경우는 어떻게 할까요? `onClick={() => handleClick(i)}`처럼 화살표 함수로 감쌉니다. 화살표 함수 자체가 "클릭되면 실행할 함수"가 되고, 그 함수가 클릭될 때 `handleClick(i)`를 실행합니다.

Python을 아시는 분들께는 이렇게 설명드릴 수 있습니다. `button.command = handle_click`은 맞고, `button.command = handle_click()`은 틀립니다. React도 동일한 원리입니다.

시간: 5분
-->

---

# Step 5 → 문제점 발견: State를 Square에 두면?

Square에 직접 State를 넣어서 클릭 시 X 표시:

```tsx
function Square({ value }: SquareProps) {
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

<v-click>

**동작은 하는데... 문제가 있습니다**

**[미니 퀴즈]** 이 코드로 실제 게임을 완성하려면 어떤 문제가 있을까요? 30초 생각해보세요.

</v-click>


<v-click>

<div class="box-red">

1. 모든 칸이 X만 표시됩니다 → O도 있어야 합니다
2. **Board가 각 칸의 상태를 알 수 없습니다** ← 핵심 문제!
3. Board가 전체 칸 상태를 모르니 승자 판정 불가

</div>

이것이 바로 **State Lifting Up(상태 끌어올리기)**이 필요한 이유입니다.

</v-click>

<!--
[스크립트]
클릭했을 때 X를 표시해봅시다. 가장 직관적인 방법은 Square 자체에 State를 넣는 것입니다. `useState(false)`로 clicked 상태를 만들고, 클릭하면 true로 바꿉니다.

저장하고 버튼을 클릭해보세요. 각 칸에 X가 표시됩니다.

[click]

동작은 하는데, 진짜 게임을 만들려면 문제가 있습니다. 30초 생각해보세요. 이 구조로는 어떤 문제가 있을까요?

첫 번째로 모든 칸이 X만 나옵니다. O도 번갈아 표시되어야 하는데, 이건 "몇 번째 클릭인지" 전체를 알아야 합니다.

두 번째가 핵심 문제입니다. Board가 각 Square의 상태를 알 수 없습니다. 지금은 clicked State가 각 Square 안에만 있어서, Board는 어떤 칸이 채워졌는지 알 방법이 없습니다.

세 번째는 이 결과입니다. Board가 전체 칸 상태를 모르니 "X가 한 줄을 완성했는가?"를 판단할 수 없습니다.

[click]

이것이 State Lifting Up이 필요한 이유입니다. 여러 컴포넌트가 공유해야 하는 State는 공통 부모로 끌어올려야 합니다.

시간: 5분
-->

---

# Step 6: State Lifting Up (상태 끌어올리기)

**Before → After 다이어그램:**

```
Before (각 Square에 State가 흩어져 있음):
  Board
    Square[0] → State: clicked=true  (Board가 모름)
    Square[1] → State: clicked=false (Board가 모름)

After (State를 Board로 끌어올림):
  Board → State: squares = ['X', null, 'O', null, ...] ← Board가 전부 앎
    Square[0] (Props로 value만 받아서 표시)
    Square[1]
```

<v-click>

**구현: Board에 squares State + handleClick 추가**

```tsx {1-5|7-13}{maxHeight:'200px'}
function Board() {
  // 9개 칸의 값 배열: 'X', 'O', 또는 null
  const [squares, setSquares] = useState<(string | null)[]>(
    Array(9).fill(null)   // [null, null, null, ..., null]
  );
  const [xIsNext, setXIsNext] = useState(true); // true=X차례, false=O차례

  function handleClick(i: number) {
    if (squares[i]) return; // 이미 채워진 칸 무시
    const nextSquares = squares.slice(); // ★ 불변성: 복사본 생성
    nextSquares[i] = xIsNext ? 'X' : 'O';
    setSquares(nextSquares);
    setXIsNext(!xIsNext);
  }
```

</v-click>

<!--
[스크립트]
State Lifting Up을 직접 구현해보겠습니다.

다이어그램을 보면, Before는 각 Square가 자기 State를 자기 안에만 갖고 있습니다. Board는 아무것도 모릅니다.

After는 State를 Board로 끌어올렸습니다. Board가 `squares` 배열 하나로 9개 칸의 상태를 전부 관리합니다. 각 Square는 Board에서 Props로 값을 받기만 합니다.

[click]

코드를 보겠습니다. Board에 두 개의 State를 추가합니다.

첫 번째는 `squares`입니다. `Array(9).fill(null)`로 9개가 모두 null인 배열을 초기값으로 만듭니다. 타입은 `(string | null)[]`입니다. string 또는 null로 이루어진 배열이라는 뜻입니다.

두 번째는 `xIsNext`입니다. true면 X 차례, false면 O 차례입니다.

[click]

handleClick 함수를 보겠습니다. i는 클릭된 칸의 인덱스입니다. `squares[i]`가 이미 채워져 있으면 무시합니다.

그 다음 중요한 줄입니다. `squares.slice()`로 배열 복사본을 만듭니다. 기존 squares 배열을 직접 수정하지 않습니다. 왜 그래야 하는지는 바로 다음 슬라이드에서 설명합니다.

복사본에 X 또는 O를 채우고, `setSquares`로 State를 업데이트합니다. `setXIsNext(!xIsNext)`로 차례를 바꿉니다.

시간: 6분
-->

---

# Step 6 완성: Square에 Callback Props 전달

Square의 Props 수정 — 클릭 핸들러도 Props로 받기:

```tsx {1-6|8-18}{maxHeight:'340px'}
interface SquareProps {
  value: string | null;
  onSquareClick: () => void; // 파라미터 없고 반환값 없는 함수 타입
}

function Square({ value, onSquareClick }: SquareProps) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

// Board의 return 안 — 각 Square에 값과 핸들러 전달
<div className="board-row">
  <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
  <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
  <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
</div>
```

<v-click>

<div class="box-blue">

**`() => handleClick(0)` 왜 이렇게 쓰나?**

`onSquareClick`은 파라미터 없는 함수를 기대합니다. `handleClick`은 인덱스 `i`가 필요합니다. 화살표 함수로 감싸서 "클릭되면 `handleClick(0)`을 실행하는 파라미터 없는 함수"를 만듭니다.

</div>

</v-click>

<!--
[스크립트]
Square의 Props를 수정합니다. 이제 Square는 value뿐만 아니라 onSquareClick이라는 함수도 Props로 받습니다. 타입은 `() => void`입니다. "파라미터 없이 호출되고 반환값이 없는 함수"의 타입입니다.

Square 컴포넌트는 내부 State를 전혀 갖지 않습니다. value를 Props로 받아서 표시하고, 클릭 시 Props로 받은 onSquareClick 함수를 호출하기만 합니다.

[click]

Board의 return에서 각 Square에 두 가지를 전달합니다. `value={squares[0]}`으로 표시할 값을, `onSquareClick={() => handleClick(0)}`으로 클릭 핸들러를 전달합니다.

[click]

`() => handleClick(0)` 문법이 낯설게 보일 수 있습니다. onSquareClick은 파라미터 없는 함수를 기대합니다. 그런데 handleClick은 몇 번째 칸인지 인덱스 i가 필요합니다. 그래서 화살표 함수로 감쌉니다. "호출되면 handleClick(0)을 실행하는 파라미터 없는 함수"를 만드는 것입니다.

이 패턴, Callback Props 패턴이라고 합니다. 부모가 State 변경 함수를 자식에게 Props로 전달하는 패턴입니다. Social Dashboard 실습에서도 게시글 삭제, Todo 토글에서 이 패턴을 그대로 씁니다.

코드를 저장하고 게임을 클릭해보세요. X와 O가 번갈아 표시되는지 확인하세요.

시간: 6분
-->

---

# 불변성(Immutability)이 중요한 이유

```tsx {1-6|8-12}
// ❌ 잘못된 방법 — 기존 배열을 직접 수정 (Mutation)
function handleClick(i: number) {
  squares[i] = 'X';      // 배열 직접 수정 → 같은 메모리 주소
  setSquares(squares);   // React: "이전이랑 같은 배열? 변경 없음" → 재렌더링 없음!
}

// ✅ 올바른 방법 — 새 배열 생성 (Immutability)
function handleClick(i: number) {
  const nextSquares = squares.slice(); // 새 배열 생성 → 다른 메모리 주소
  nextSquares[i] = 'X';
  setSquares(nextSquares); // React: "새 배열이네! 변경됨" → 재렌더링
}
```

<v-click>

**React 배열 불변성 치트시트:**

```tsx
const arr = [1, 2, 3, 4, 5];

// 추가 — spread 연산자
const added   = [...arr, 6];                         // [1,2,3,4,5,6]
// 삭제 — filter (새 배열 반환)
const removed = arr.filter(n => n !== 3);            // [1,2,4,5]
// 수정 — map (새 배열 반환)
const updated = arr.map(n => n === 3 ? 99 : n);     // [1,2,99,4,5]
// 복사 — slice 또는 spread
const copy    = arr.slice();  // 또는 [...arr]

// ❌ 직접 수정 금지: arr.push(), arr.splice(), arr[i] = ...
```

</v-click>

<!--
[스크립트]
handleClick에서 `squares.slice()`로 복사본을 만들었는데, 왜 기존 배열을 직접 수정하면 안 될까요? 이게 React에서 매우 중요한 규칙입니다. 왼쪽 코드를 보면, `squares[i] = 'X'`로 배열을 직접 수정하고 `setSquares(squares)`를 호출합니다. 실제로 해보면 화면이 갱신되지 않습니다.

왜냐면 React는 State가 변경되었는지 판단할 때 `===` 참조 비교를 씁니다. 기존 배열을 직접 수정하면 배열의 메모리 주소가 바뀌지 않습니다. React 입장에서는 "이전이랑 같은 배열이네, 변경 없음"으로 판단하고 화면을 갱신하지 않습니다.

[click]

오른쪽처럼 `squares.slice()`로 새 배열을 만들면, 새 배열은 다른 메모리 주소를 가집니다. React가 "다른 배열이 왔네, 변경됨"으로 판단하고 재렌더링합니다.

Python이나 Java 경험이 있으신 분들은 "리스트를 왜 복사해? 그냥 append 하면 되지"라고 생각하실 수 있습니다. React에서는 State를 직접 수정하는 것이 금지된 규칙입니다. 어기면 화면이 갱신이 안 되거나 예상치 못한 버그가 생깁니다.

[click]

그래서 이 치트시트를 기억해두세요. 배열에 항목 추가할 때는 spread 연산자 `[...arr, 새항목]`. 삭제할 때는 filter. 수정할 때는 map. 복사할 때는 slice 또는 spread. 이 패턴들은 Social Dashboard 실습에서도 게시글 삭제에 filter, Todo 토글에 map, 새 항목 추가에 spread를 씁니다.

시간: 5분
-->

---
layout: section
---

# Thinking in React
## React로 생각하는 5단계

<!--
[스크립트]
틱택토로 React의 핵심 메커니즘을 직접 체험했습니다. 이제 한 걸음 물러서서 "어떻게 생각해야 하는가"를 배웁니다.

React 공식 문서에서 "Thinking in React"라는 제목으로 소개하는 5단계 프로세스입니다. 이것을 익히면 앞으로 어떤 React UI를 만들든 막막하지 않습니다. 어디서 시작해야 할지, State를 어디 두어야 할지, 자식이 어떻게 부모 State를 바꾸는지 체계적으로 생각할 수 있게 됩니다.

시간: 1분
-->

---

# Thinking in React 5단계

React로 UI를 만들 때 막막하다면? 이 5단계를 따르세요.

| 단계 | 핵심 질문 | 우리 예제에서 |
|------|-----------|--------------|
| **Step 1**: 컴포넌트 분해 | UI를 어떻게 나눌 것인가? | 5개 컴포넌트로 분해 |
| **Step 2**: 정적 버전 | Props만으로 UI를 만들 수 있는가? | State 없이 UI 먼저 완성 |
| **Step 3**: 최소 State | 어떤 데이터가 진짜 State인가? | 검색어, 체크 여부만 State |
| **Step 4**: State 위치 | 어느 컴포넌트에 State를 두는가? | 공통 부모에 배치 |
| **Step 5**: 역방향 흐름 | 자식이 부모 State를 어떻게 바꾸는가? | Callback Props 전달 |

<v-click>

**오늘 만들 UI: 상품 검색 필터**

```
검색: [__________________________]
☑ 재고 있는 상품만 보기

이름          가격
─────────────────────
과일
사과          ₩1,500
용과          품절         ← 재고 없음: 빨간색
채소
시금치        ₩2,000
호박          ₩3,000
```

</v-click>

<!--
[스크립트]
React로 UI를 만들 때 가장 막히는 부분이 문법이 아닙니다. "이 UI를 몇 개 컴포넌트로 나눠야 하는가?" "State를 어디 두어야 하는가?" 같은 설계 질문들입니다.

이 5단계가 그 질문에 답을 줍니다.

Step 1은 UI를 컴포넌트로 분해하는 것입니다. Step 2는 State 없이 Props만으로 먼저 화면을 만드는 것입니다. Step 3은 어떤 데이터가 진짜 State인지 가려내는 것입니다. Step 4는 그 State를 어느 컴포넌트에 두어야 하는지 결정하는 것입니다. Step 5는 자식이 어떻게 부모 State를 바꾸는지 역방향 데이터 흐름을 연결하는 것입니다.

[click]

이 5단계를 적용해서 만들 UI입니다. 검색창에 입력하면 상품 목록이 필터링되고, 체크박스를 켜면 재고 없는 상품이 사라집니다. 단순해 보이지만 이 안에 React의 핵심 패턴이 모두 들어있습니다.

시간: 3분
-->

---

# Step 1: UI를 컴포넌트로 분해

**단일 책임 원칙**: 하나의 컴포넌트는 하나의 일만 해야 합니다.

```
┌── FilterableProductTable ─────────────────────────────┐
│                                                       │
│  ┌── SearchBar ──────────────────────────────────┐   │
│  │  검색: [__________________]                   │   │
│  │  ☑ 재고 있는 상품만 보기                        │   │
│  └───────────────────────────────────────────────┘   │
│                                                       │
│  ┌── ProductTable ────────────────────────────────┐  │
│  │  이름            가격                          │  │
│  │  ┌── ProductCategoryRow ─────────────────┐    │  │
│  │  │  과일                                 │    │  │
│  │  └───────────────────────────────────────┘    │  │
│  │  ┌── ProductRow ─────────────────────────┐    │  │
│  │  │  사과            ₩1,500              │    │  │
│  │  └───────────────────────────────────────┘    │  │
│  └────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

<v-click>

**컴포넌트 계층 구조:**

```
FilterableProductTable   ← 전체를 감싸는 최상위
  ├── SearchBar          ← 검색창 + 체크박스
  └── ProductTable       ← 상품 목록 테이블
        ├── ProductCategoryRow  ← 카테고리 헤더
        └── ProductRow          ← 상품 한 줄
```

</v-click>

<!--
[스크립트]
Step 1은 UI 스케치를 보고 컴포넌트 경계를 긋는 작업입니다. 기준은 소프트웨어 설계의 단일 책임 원칙입니다. 하나의 컴포넌트는 하나의 일만 해야 한다는 원칙입니다.

화면을 보면서 어디서 컴포넌트를 나눌지 생각해봅시다.

최상위에 FilterableProductTable이 전체를 감싸고 있습니다. 그 안에 SearchBar와 ProductTable이 있습니다. SearchBar는 검색창과 체크박스를 담당합니다. ProductTable은 상품 목록 전체를 담당합니다.

ProductTable 안을 더 들여다보면, 카테고리 헤더인 ProductCategoryRow와 상품 한 줄인 ProductRow로 나뉩니다. 카테고리 헤더를 별도 컴포넌트로 만드는 이유는 스타일과 레이아웃이 다르기 때문입니다.

[click]

계층 구조로 정리하면 이렇습니다. 총 5개의 컴포넌트입니다. 이 트리 구조를 그려두면 코딩을 시작하기 훨씬 쉽습니다.

실제 업무에서도 마찬가지입니다. 코드를 바로 짜기 전에 "이 UI는 몇 개의 컴포넌트로 나눌 것인가?"를 먼저 스케치하는 습관을 들이세요.

시간: 4분
-->

---

# Step 2: 정적 버전 만들기

**State 없이 Props만으로 먼저 UI를 완성합니다.**

왜? State와 동작을 동시에 고민하면 복잡해집니다. 먼저 "어떻게 보여야 하는가"를 해결하세요.

```tsx {1-8|10-18}{maxHeight:'340px'}
// 타입 정의 먼저
interface Product {
  category: string; // '과일', '채소'
  price: string;    // '₩1,500', '품절'
  stocked: boolean; // 재고 여부
  name: string;     // 상품 이름
}

// 정적 데이터
const PRODUCTS: Product[] = [
  { category: '과일', price: '₩1,500', stocked: true,  name: '사과'   },
  { category: '과일', price: '품절',   stocked: false, name: '용과'   },
  { category: '채소', price: '₩2,000', stocked: true,  name: '시금치' },
  { category: '채소', price: '₩3,000', stocked: true,  name: '호박'   },
];
```

<v-click>

<div class="box-blue">

**ProductRow: 재고 없는 상품 빨간색**

```tsx
function ProductRow({ product }: { product: Product }) {
  const nameElement = product.stocked
    ? product.name
    : <span style={{ color: 'red' }}>{product.name}</span>;
  return <tr><td>{nameElement}</td><td>{product.price}</td></tr>;
}
```

</div>

</v-click>

<!--
[스크립트]
Step 2는 정적 버전을 먼저 만드는 것입니다. 정적 버전이란 State 없이 Props만으로 UI를 완성하는 버전입니다. 검색창에 타이핑하거나 체크박스를 눌러도 아무것도 바뀌지 않지만, 화면이 올바르게 보입니다.

왜 이렇게 하냐면, State와 이벤트를 동시에 고민하면 머릿속이 복잡해집니다. 먼저 "화면이 어떻게 보여야 하는가"를 해결하고 나서 "어떻게 상호작용하는가"를 해결하면 훨씬 쉽습니다.

[click]

먼저 타입 정의를 합니다. Product 인터페이스를 만들어서 각 상품 데이터의 형태를 정의합니다.

그 다음 하드코딩된 데이터를 만듭니다. 실제 앱에서는 API에서 받아오겠지만 지금은 일단 상수로 정의합니다.

[click]

ProductRow 컴포넌트를 보면, 재고 없는 상품(`stocked: false`)은 이름을 빨간색으로 표시합니다. `product.stocked ? product.name : <span style={{ color: 'red' }}>{product.name}</span>`. JSX 안에서 삼항 연산자로 조건에 따라 다른 JSX를 반환합니다.

시간: 5분
-->

---

# Step 3: 최소 State 식별

**State는 최소한으로 유지합니다. DRY 원칙.**

**State가 아닌 것 판별 기준:**

<v-click>

1. 시간이 지나도 변하지 않는가? → **State 불필요** (상수)
2. 부모에게서 Props로 받는가? → **State 불필요** (Props 그대로 사용)
3. 다른 State나 Props로 계산할 수 있는가? → **State 불필요** (파생값)

</v-click>

<v-click>

**우리 예제 분석:**

| 데이터 | State? | 이유 |
|--------|--------|------|
| 상품 목록 원본 | ❌ | 외부 고정 데이터 (상수 또는 Props) |
| 검색어 (`filterText`) | ✅ | 사용자 입력으로 변하고 UI에 반영 |
| 체크 여부 (`inStockOnly`) | ✅ | 사용자 행동으로 변하고 UI에 반영 |
| 필터링된 상품 목록 | ❌ | 원본 + 검색어 + 체크로 **계산 가능** |

</v-click>

<v-click>

<div class="box-green">

**결론: State는 딱 두 개!**
```tsx
const [filterText, setFilterText]   = useState('');
const [inStockOnly, setInStockOnly] = useState(false);
```

</div>

</v-click>

<!--
[스크립트]
Step 3은 어떤 데이터가 진짜 State인지 가려내는 작업입니다. State는 최소한으로 유지해야 합니다. 불필요한 State는 버그를 만들고 코드를 복잡하게 합니다.

[click]

State인지 아닌지 판별하는 기준이 세 가지 있습니다.

첫째, 시간이 지나도 변하지 않으면 State가 아닙니다. 상수입니다.

둘째, 부모에게서 Props로 받는 데이터라면 State가 아닙니다. 그냥 Props를 쓰면 됩니다.

셋째, 다른 State나 Props로 계산할 수 있으면 State가 아닙니다. 이걸 파생값이라고 합니다.

[click]

우리 예제에서 분석해보면, 상품 목록 원본은 State가 아닙니다. 외부에서 받는 고정 데이터입니다. 검색어와 체크 여부는 State가 맞습니다. 사용자가 바꾸고, 그에 따라 UI가 달라지기 때문입니다. 필터링된 상품 목록은 State가 아닙니다. 원본 + 검색어 + 체크 여부를 갖고 있으면 계산할 수 있기 때문입니다.

[click]

따라서 State는 딱 두 개입니다. filterText와 inStockOnly. 필터링된 목록은 매 렌더링마다 이 두 값으로 계산합니다.

시간: 4분
-->

---

# Step 4: State 위치 결정

**규칙**: State는 그것을 필요로 하는 **모든 컴포넌트의 공통 부모**에 위치해야 합니다.

`filterText`와 `inStockOnly`를 누가 필요로 하는가?

<v-click>

```
FilterableProductTable  ← SearchBar와 ProductTable의 공통 부모 ✅
  ├── SearchBar          (입력값 표시에 filterText, inStockOnly 필요)
  └── ProductTable       (필터링에 filterText, inStockOnly 필요)
```

→ **FilterableProductTable에 State 배치!**

</v-click>

<v-click>

```tsx {maxHeight:'340px'}
function FilterableProductTable() {
  // Step 3에서 결정한 딱 두 개의 State
  const [filterText, setFilterText]   = useState('');
  const [inStockOnly, setInStockOnly] = useState(false);

  return (
    <div>
      <SearchBar
        filterText={filterText}
        inStockOnly={inStockOnly}
        // Step 5: 변경 함수도 Props로 전달 (역방향 흐름)
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
```

</v-click>

<!--
[스크립트]
Step 4는 State를 어느 컴포넌트에 둘지 결정하는 것입니다. 규칙은 간단합니다. 그 State를 필요로 하는 모든 컴포넌트의 공통 부모에 두면 됩니다.

filterText와 inStockOnly를 누가 필요로 할까요? SearchBar는 입력창의 현재 값을 표시하기 위해 필요합니다. ProductTable은 상품을 필터링하기 위해 필요합니다.

[click]

SearchBar와 ProductTable의 공통 부모가 FilterableProductTable입니다. 그러므로 State는 FilterableProductTable에 놓습니다.

[click]

코드를 보면, FilterableProductTable에 두 State를 선언합니다. 그리고 SearchBar에는 현재 값뿐만 아니라 변경 함수도 Props로 전달합니다. 이것이 Step 5인 역방향 데이터 흐름입니다.

ProductTable에는 현재 값만 전달합니다. ProductTable은 읽기만 하면 되기 때문입니다.

시간: 4분
-->

---

# Step 5: 역방향 데이터 흐름

React 데이터는 항상 **부모 → 자식** (단방향). 자식이 부모 State를 직접 수정할 수 없습니다.

대신 부모가 **State 변경 함수를 자식에게 Props로 전달**합니다.

<v-click>

**SearchBar — Callback Props 구현:**

```tsx {1-7|9-18}{maxHeight:'340px'}
interface SearchBarProps {
  filterText: string;
  inStockOnly: boolean;
  onFilterTextChange: (value: string) => void;
  onInStockOnlyChange: (value: boolean) => void;
}

function SearchBar({ filterText, inStockOnly, onFilterTextChange, onInStockOnlyChange }: SearchBarProps) {
  return (
    <form>
      <input
        type="text"
        value={filterText}                               // State가 현재 값 결정
        onChange={(e) => onFilterTextChange(e.target.value)} // 타이핑 시 부모 State 변경
      />
      <input
        type="checkbox"
        checked={inStockOnly}                            // checked 사용! (value 아님)
        onChange={(e) => onInStockOnlyChange(e.target.checked)}
      />
    </form>
  );
}
```

</v-click>

<!--
[스크립트]
Step 5는 역방향 데이터 흐름입니다. React의 데이터 흐름은 항상 부모에서 자식으로 내려갑니다. 자식이 부모의 State를 직접 수정하는 방법은 없습니다.

대신 부모가 State 변경 함수를 자식에게 Props로 전달합니다. 자식은 사용자 입력이 있을 때 이 함수를 호출합니다. 그러면 부모의 State가 바뀌고, 재렌더링이 일어나서 자식도 새 값을 받습니다.

[click]

SearchBarProps에 두 개의 콜백 함수 Props가 추가됐습니다. `onFilterTextChange`는 string을 받아서 void를 반환하는 함수 타입이고, `onInStockOnlyChange`는 boolean을 받는 함수 타입입니다.

SearchBar 컴포넌트 안을 보면, input의 `value`를 `filterText`에 연결하고, `onChange`에서 `onFilterTextChange(e.target.value)`를 호출합니다. 사용자가 타이핑할 때마다 부모의 State 변경 함수가 호출됩니다.

체크박스는 주의해야 합니다. 텍스트 input은 `value`와 `e.target.value`를 쓰지만, 체크박스는 `checked`와 `e.target.checked`를 씁니다. 이걸 혼동하면 체크박스가 전혀 동작하지 않습니다.

이 패턴, `value + onChange`를 쌍으로 쓰는 것을 제어 컴포넌트(Controlled Component) 패턴이라고 합니다. 다음 슬라이드에서 더 자세히 설명합니다.

시간: 6분
-->

---

# 제어 컴포넌트 패턴 + 완성

**Controlled Component**: `value`와 `onChange`를 반드시 쌍으로 사용합니다.

```tsx
// ✅ 완전한 제어 컴포넌트 — 양방향 연결
<input
  type="text"
  value={filterText}                              // State → input (표시)
  onChange={(e) => setFilterText(e.target.value)} // input → State (변경)
/>
```

<v-click>

<div class="box-red">

**흔한 실수:**
- `onChange`만 있고 `value` 없음 → 비제어 컴포넌트. 프로그래밍 방식으로 값 초기화 불가
- `value`만 있고 `onChange` 없음 → 타이핑해도 값이 안 바뀜. React 경고 발생
  - `"Warning: You provided a 'value' prop without an 'onChange' handler."`

</div>

</v-click>

<v-click>

<div class="box-blue">

**완성 후 동작 확인:**
1. "사과" 입력 → 사과만 표시
2. "체크박스 켜기" → 용과(품절) 사라짐
3. "사과" 지우기 → 전체 목록 복원

Social Dashboard 실습의 검색 기능도 이 패턴 그대로입니다!

</div>

</v-click>

<!--
[스크립트]
제어 컴포넌트 패턴에 대해 정리하겠습니다. 핵심은 value와 onChange를 반드시 쌍으로 써야 한다는 것입니다.

value는 "State가 현재 값을 결정한다"는 의미입니다. State가 바뀌면 input에 표시되는 값이 바뀝니다.

onChange는 "사용자가 값을 바꾸면 State를 업데이트한다"는 의미입니다. 사용자가 타이핑하면 State가 업데이트되고, 재렌더링되면서 input에 새 값이 표시됩니다.

[click]

자주 하는 실수 두 가지입니다.

onChange만 있고 value가 없으면 비제어 컴포넌트가 됩니다. 동작은 하지만 React가 값을 완전히 제어하지 못합니다. 예를 들어 "초기화" 버튼으로 input을 비우는 기능을 만들기 어렵습니다.

value만 있고 onChange가 없으면 타이핑해도 값이 바뀌지 않습니다. 사용자가 타이핑하면 input이 State 값으로 다시 덮어씌워지기 때문입니다. React가 경고를 내보냅니다.

둘 다 있어야 완전한 제어 컴포넌트입니다.

[click]

이제 코드를 저장하고 실제로 동작을 확인해보겠습니다. "사과"를 입력하면 사과만 표시되어야 합니다. 체크박스를 켜면 품절 상품인 용과가 사라져야 합니다. 검색어를 지우면 전체 목록이 복원되어야 합니다.

Social Dashboard 실습에서 검색 기능을 만들 때 이 패턴을 그대로 씁니다.

시간: 5분
-->

---

# Session 4 마무리 + Social Dashboard 연결

**오늘 배운 핵심 패턴 → Session 5에서 그대로 사용됩니다!**

| 오늘 패턴 | Social Dashboard 적용 |
|-----------|----------------------|
| `useState` + `[]` 초기값 | 게시글 목록, 사용자 목록 초기화 |
| `onClick` 이벤트 핸들러 | 게시글 삭제, Todo 토글 버튼 |
| `filter` 불변성 패턴 | `posts.filter(p => p.id !== id)` 삭제 |
| `map` 불변성 패턴 | `todos.map(t => t.id === id ? {...t, done: !t.done} : t)` |
| `[...arr, 새항목]` spread | 새 게시글 추가 |
| State Lifting Up | 여러 섹션에서 공유하는 선택된 userId |
| Callback Props | PostList → App으로 삭제 요청 전달 |
| Controlled Component | 게시글 작성 폼 input 관리 |

<v-click>

<div class="box-green">

**Session 5에서 새로 추가되는 것:**
- `useEffect`: "컴포넌트가 화면에 나타난 직후" API를 호출하는 훅
- `fetch`: JSONPlaceholder API에서 실제 데이터를 받아오는 Web API

나머지는 오늘 배운 패턴 그대로입니다!

</div>

</v-click>

<!--
[스크립트]
오늘 Session 4를 마무리하겠습니다. 정말 중요한 내용을 많이 배웠습니다.

표를 보면, 오늘 배운 패턴들이 Session 5 Social Dashboard에서 어떻게 쓰이는지 매핑되어 있습니다.

useState에 빈 배열을 넣는 것은 게시글 목록 초기화에 씁니다. filter로 배열을 새로 만드는 불변성 패턴은 게시글 삭제에 씁니다. map으로 특정 항목만 수정하는 패턴은 Todo 완료 토글에 씁니다. spread로 새 항목을 앞에 추가하는 패턴은 새 게시글 추가에 씁니다. Callback Props는 PostList에서 App으로 삭제 요청을 전달할 때 씁니다. Controlled Component는 게시글 작성 폼에 씁니다.

이 패턴들을 오늘 익혔기 때문에 Social Dashboard 실습이 가능합니다.

[click]

Session 5에서 새로 추가되는 것은 두 가지뿐입니다. useEffect와 fetch입니다. useEffect는 컴포넌트가 화면에 나타난 직후 API를 호출하는 훅이고, fetch는 외부 API에서 데이터를 받아오는 Web API입니다.

나머지는 오늘 배운 패턴 그대로입니다. API에서 받은 데이터를 State에 저장하고, State가 바뀌면 화면이 갱신됩니다.

수고하셨습니다! 잠깐 쉬고 Social Dashboard 실습을 시작하겠습니다.

[Q&A 대비]
Q: Thinking in React 5단계를 꼭 순서대로 해야 하나요?
A: 꼭 순서대로 할 필요는 없지만, 처음에는 이 순서가 가장 혼란이 적습니다. 특히 Step 2(정적 버전 먼저)와 Step 3(최소 State 식별)의 순서는 꼭 지키는 것이 좋습니다.

Q: State를 여러 컴포넌트에 나눠서 두면 안 되나요?
A: 각 컴포넌트가 독립적으로 관리해도 되는 State라면 나눠도 됩니다. 문제는 두 컴포넌트가 같은 State를 공유해야 할 때입니다. 그때는 반드시 공통 부모로 끌어올려야 합니다.

전환: 잠깐 쉬고 Social Dashboard 실습 세션으로 넘어가겠습니다.
시간: 5분
-->

---
layout: section
---

# Session 5: 종합 실습
## Social Dashboard

<div class="box-blue mt-6">
  <strong>2시간 실습</strong> (15:00 – 17:00)<br/>
  JSONPlaceholder REST API 연동 · TypeScript + React 통합 실습
</div>

<!--
[스크립트]
자, 드디어 오늘의 마지막이자 가장 중요한 세션입니다. 오전에 TypeScript 타입 시스템을 배우고, 오후에 React의 컴포넌트와 Props, State, Tic-Tac-Toe, Thinking in React까지 달려왔습니다. 이제 그 모든 것을 하나의 실제 앱으로 통합할 시간입니다.

오늘 2시간 동안 여러분은 "Social Dashboard"라는 앱을 완성하게 됩니다. JSONPlaceholder라는 무료 연습용 REST API에서 실제 데이터를 받아와 화면에 렌더링하는, 진짜 웹 앱의 구조와 거의 동일한 실습입니다.

제가 먼저 Task 1을 시연으로 보여드릴 것입니다. 그 시연을 보시면서 오늘 배운 모든 개념이 어떻게 연결되는지 눈으로 확인하십시오. 그리고 나서 Task 2부터는 여러분이 직접 완성합니다.

막히면 언제든지 손을 들어 주십시오. 순서대로 힌트를 드리겠습니다. 정답 코드는 solutions/ 폴더에 있으니, 정말 막혔을 때 참고하셔도 됩니다.

시작하기 전에 화장실 등 필요한 것을 먼저 해결하시고, 돌아오시면 바로 실습을 시작합니다.

시간: 2분
-->

---
layout: two-cols
---

# 앱 소개 & 목표

**완성하면 이런 앱이 됩니다**

<div class="space-y-2 mt-3">
  <div class="box-blue text-sm">
    <strong>왼쪽 사이드바</strong> — 사용자 10명 카드 목록<br/>
    클릭하면 오른쪽에 해당 사용자 정보 표시
  </div>
  <div class="box-green text-sm">
    <strong>오른쪽 메인 영역</strong> — Posts / Todos / Albums 탭<br/>
    선택된 사용자의 게시글, 할 일, 앨범 표시
  </div>
  <div class="box-yellow text-sm">
    <strong>상단 통계 카드</strong> — Users, Posts, Comments 등<br/>
    (도전 과제 8 완성 시 활성화)
  </div>
</div>

::right::

<div class="mt-8 ml-4">
  <div class="box-blue mb-3">
    <strong>필수 과제 6개</strong>
    <ul class="text-sm mt-1 space-y-0.5">
      <li>1. 사용자 목록 (강사 시연)</li>
      <li>2. 게시글 목록</li>
      <li>3. 게시글 추가 (POST)</li>
      <li>4. 게시글 삭제 (DELETE)</li>
      <li>5. Todo 완료 토글 (PATCH)</li>
      <li>6. 댓글 표시</li>
    </ul>
  </div>
  <div class="box-yellow">
    <strong>도전 과제 5개</strong>
    <p class="text-sm mt-1">Promise.all · useMemo · AlbumGallery · Skeleton · StatsUpdateFn</p>
  </div>
</div>

<!--
[스크립트]
앱 구조를 먼저 소개하겠습니다. 화면은 크게 세 부분으로 나뉩니다.

왼쪽에는 JSONPlaceholder에서 가져온 사용자 10명이 카드 형태로 나열됩니다. 카드를 클릭하면 오른쪽 메인 영역에 그 사용자의 정보가 표시됩니다.

오른쪽 메인 영역 상단에는 선택된 사용자의 이름, 이메일, 회사 정보가 보입니다. 그 아래에 Posts, Todos, Albums 세 개의 탭이 있습니다. Posts 탭에서는 그 사용자의 게시글 목록을 볼 수 있고, 게시글을 추가하거나 삭제할 수도 있습니다.

과제 구성을 보시면, 필수 과제가 6개이고 도전 과제가 5개입니다. 필수 1번은 제가 지금부터 직접 코딩해서 보여드리겠습니다. 나머지 2번부터 6번은 여러분이 스스로 구현합니다.

왼쪽의 박스에 있는 구조를 기억해 두십시오. Task 번호와 내용을 파악해두면 실습할 때 어디서 무엇을 해야 하는지 헷갈리지 않습니다.

시간: 2분
-->

---

# 핵심 개념 리뷰: useState + TypeScript 제네릭

<div class="box-blue mb-4">
  오늘 실습에서 가장 많이 쓰는 두 패턴을 빠르게 복습합니다
</div>

```tsx {1-3|5-8|10-13}
// 세션 1에서 본 제네릭 — T라는 자리표시자 타입
function identity<T>(value: T): T { return value; }

// useState도 동일한 제네릭 패턴
// useState<T>(): T 타입의 값을 상태로 관리
const [users, setUsers] = useState<User[]>([]);
//                                  ^^^^^^^^
//              T = User[]  →  초기값 []는 User[] 타입

// null이 될 수 있는 상태: Union 타입
const [selectedUser, setSelectedUser] = useState<User | null>(null);
//                                               ^^^^^^^^^^^
//          "User 객체이거나, null이거나" — 처음엔 아무도 선택 안 됨
```

<div v-click class="box-red mt-4">
  <strong>왜 제네릭을 반드시 써야 하나요?</strong><br/>
  <code>useState([])</code> → TypeScript가 <code>never[]</code> 로 추론 → 아무것도 넣을 수 없는 배열이 됨!<br/>
  <code>useState&lt;User[]&gt;([])</code> → "이 배열엔 User 객체만 들어간다" 명시 → 자동완성 + 타입 검사 활성화
</div>

<!--
[스크립트]
실습 시작 전 오늘 가장 핵심적인 두 가지 패턴을 5분 안에 빠르게 복습합니다. 이 두 패턴이 오늘 실습 전체의 뼈대이기 때문입니다.

첫 번째는 useState와 TypeScript 제네릭의 조합입니다. 세션 1에서 제네릭을 처음 소개할 때 identity 함수를 예로 들었습니다. T라는 자리표시자 타입을 사용해서 "어떤 타입이든 받아서 그 타입 그대로 반환한다"는 함수를 만들었습니다. useState도 완전히 동일한 패턴입니다.

[click]

코드 두 번째 블록을 보면, useState<User[]>([])라고 쓰면 "이 상태는 User 배열이다"라는 것을 TypeScript에게 명시합니다.

[click]

세 번째 블록은 null이 될 수 있는 상태입니다. useState<User | null>(null)은 "User 객체이거나, 아직 선택되지 않은 null 상태"를 표현합니다.

[click]

빨간 박스를 봐주십시오. 제네릭을 쓰지 않으면 어떤 일이 생기는지입니다. useState([])만 쓰면 TypeScript는 이 배열의 타입을 never[]로 추론합니다. never[]는 "절대 아무것도 넣을 수 없는 배열"이라는 뜻입니다. 그러면 나중에 setUsers(data)를 호출할 때 타입 오류가 납니다. 반드시 제네릭을 명시해야 합니다.

[Q&A 대비]
Q: User | null에서 | 기호가 뭔가요?
A: 세션 1에서 배운 Union 타입입니다. "이 두 타입 중 하나"라는 의미입니다. selectedUser는 User 객체일 수도 있고, 아직 아무도 선택하지 않은 null 상태일 수도 있습니다.

전환: 다음 슬라이드에서 useEffect 의존성 배열을 복습합니다.
시간: 3분
-->

---

# 핵심 개념 리뷰: useEffect 의존성 배열

<div class="grid grid-cols-2 gap-4">
<div>

**의존성 배열 3가지 형태**

```tsx {1-4|6-10|12-14}
// 형태 1: 빈 배열 — 마운트 시 딱 한 번만
useEffect(() => {
  fetchUsers();
}, []);

// 형태 2: 값 배열 — selectedUser 바뀔 때마다
useEffect(() => {
  if (!selectedUser) return;
  fetchPosts();
}, [selectedUser]);

// 형태 3: 배열 없음 — 매 렌더링마다 (거의 사용 안 함)
useEffect(() => { console.log("매번!"); });
```

</div>
<div>

<div class="box-red mt-2">
  <strong>useEffect 안에서 async 사용 — 잘못된 방법</strong>

```tsx
// ❌ 이렇게 하지 마세요
useEffect(async () => {
  const data = await fetch(url);
}, []);
```
</div>

<div class="box-green mt-3">
  <strong>올바른 방법 — 내부에 async 함수 정의</strong>

```tsx
// ✅ 이 패턴을 외워두세요
useEffect(() => {
  const fetchData = async () => {
    const res = await fetch(url);
    const data = await res.json();
    setState(data);
  };
  fetchData(); // ← 반드시 호출!
}, []);
```
</div>

</div>
</div>

<!--
[스크립트]
두 번째 핵심 패턴은 useEffect 의존성 배열입니다. 오늘 실습에서 이 패턴을 세 번 이상 직접 쓰게 됩니다.

왼쪽 코드를 보겠습니다. 의존성 배열은 세 가지 형태가 있습니다.

첫 번째, 빈 배열 []입니다. 컴포넌트가 처음 화면에 나타날 때, 즉 마운트될 때 딱 한 번만 실행합니다. 사용자 목록은 앱을 처음 열 때 한 번만 가져오면 충분하므로 빈 배열을 씁니다.

[click]

두 번째, 값이 들어있는 배열입니다. [selectedUser]라고 쓰면 selectedUser 값이 바뀔 때마다 useEffect가 다시 실행됩니다. 사용자를 클릭해서 selectedUser가 바뀌면 그 사용자의 게시글을 새로 가져오는 것이 이 패턴입니다.

[click]

세 번째는 배열 자체가 없는 경우로, 매 렌더링마다 실행됩니다. 실무에서는 거의 쓰지 않습니다.

오른쪽 빨간 박스를 보십시오. useEffect 콜백 자체를 async로 만들면 안 됩니다. async 함수는 항상 Promise를 반환하는데, React는 useEffect의 반환값으로 cleanup 함수 또는 undefined만 기대합니다. Promise를 반환하면 React가 경고를 출력하고 예기치 않은 동작이 생깁니다.

초록 박스가 올바른 방법입니다. useEffect 콜백은 일반 함수로 두고, 그 안에 async 함수를 따로 정의한 뒤 즉시 호출합니다. 마지막 fetchData() 호출 줄을 빠트리는 실수가 매우 흔합니다. 함수를 정의했으면 반드시 호출해야 합니다.

전환: 이제 프로젝트 구조를 확인하고 실습을 시작합니다.
시간: 4분
-->

---

# 프로젝트 구조 & 셋업

<div class="grid grid-cols-2 gap-4">
<div>

```
social-dashboard-starter/
├── src/
│   ├── App.tsx          ← 메인 파일 (주로 여기서 작업)
│   ├── types.ts         ← User, Post, Todo 등 타입 정의
│   ├── components/
│   │   ├── UserCard.tsx
│   │   ├── PostCard.tsx
│   │   ├── PostForm.tsx
│   │   ├── TodoSection.tsx  ← Task 5에서 수정
│   │   ├── CommentList.tsx  ← Task 6에서 수정
│   │   └── AlbumGallery.tsx ← 도전 7
│   └── main.tsx
└── solutions/           ← 정답 코드 (막히면 참고)
```

</div>
<div>

**터미널에서 실행**

```bash
cd social-dashboard-starter
npm install
npm run dev
# → http://localhost:5173 에서 확인
```

<div class="practice-point mt-4">
  <strong>셋업 체크리스트</strong>
  <ul class="text-sm mt-1 space-y-1">
    <li>☐ 브라우저에 스켈레톤 로딩 화면이 보인다</li>
    <li>☐ VS Code에서 src/App.tsx를 열었다</li>
    <li>☐ TODO 주석이 보인다</li>
    <li>☐ src/types.ts를 열어 인터페이스를 확인했다</li>
  </ul>
</div>

</div>
</div>

<!--
[스크립트]
프로젝트 구조를 보겠습니다. 오늘 가장 많이 작업할 파일은 src/App.tsx입니다. 이 파일 안에 TODO 주석으로 여러분이 채워야 할 부분이 표시되어 있습니다.

src/types.ts에는 User, Post, Comment, Todo, Album, Photo 인터페이스가 모두 정의되어 있습니다. JSONPlaceholder API가 반환하는 데이터 구조를 그대로 모델링한 것입니다. 세션 1에서 배운 interface 패턴이 실전에서 이렇게 쓰입니다.

src/components/ 폴더의 컴포넌트들은 대부분 이미 완성되어 있습니다. 여러분이 직접 수정해야 하는 파일은 App.tsx, 그리고 Task 5와 6에서 TodoSection.tsx와 CommentList.tsx입니다. AlbumGallery.tsx는 도전 과제입니다.

오른쪽 하단의 체크리스트를 확인하십시오. 지금 터미널에서 npm install과 npm run dev를 실행하고, 브라우저에서 localhost:5173을 열어두십시오. 스켈레톤 로딩 화면이 보여야 정상입니다. 아직 사용자 목록이 나타나지 않는 것이 맞습니다.

셋업이 완료된 분들은 손을 들어 주십시오.

[Q&A 대비]
Q: npm install이 오류가 납니다.
A: Node.js 버전을 확인해 주십시오. node --version으로 18 이상인지 확인합니다.

시간: 3분
-->

---
layout: section
---

# I DO — Task 1: 사용자 목록 표시
## 강사 시연 (약 30분)

<div class="box-yellow mt-6">
  지금부터 강사가 직접 코딩합니다. 여러분은 타이핑하지 말고 눈으로 먼저 확인하세요.<br/>
  코드를 한 줄씩 입력할 테니, 각 줄이 무엇을 하는지 집중해서 보십시오.
</div>

<!--
[스크립트]
자, 이제 본격적인 시연을 시작합니다. 지금부터 30분 동안 제가 직접 코딩하는 것을 보여드리겠습니다.

이 시간 동안 여러분은 직접 타이핑하지 않아도 됩니다. 코드를 눈으로 따라가면서 "아, 이 줄이 이런 의미구나" 하고 이해하는 것이 목표입니다.

제가 코드를 붙여넣지 않고 한 줄씩 직접 타이핑할 것입니다. 그래야 여러분도 속도를 맞춰서 따라올 수 있습니다. 궁금한 점은 손을 들어 언제든지 질문해 주십시오.

구현할 내용은 App.tsx의 TODO (필수 1-a)부터 (필수 1-d)까지입니다. 총 네 단계로 나눠서 설명합니다.

시간: 1분
-->

---

# Step 1-a: users 상태 선언

`src/App.tsx`를 열고 `// TODO (필수 1-a)` 주석을 찾습니다

<div v-click>

```tsx
// State 선언 영역 (파일 상단)
const [users, setUsers] = useState<User[]>([]);
//     ^^^^^  ^^^^^^^^             ^^^^^^  ^^
//  현재 값   변경 함수         타입: User배열  초기값
```

</div>

<div v-click class="box-blue mt-4">
  <strong>각 부분의 의미</strong>
  <ul class="text-sm mt-1 space-y-1">
    <li><code>const [users, setUsers]</code> — 배열 구조분해. useState는 항상 [값, 변경함수] 쌍을 반환</li>
    <li><code>useState&lt;User[]&gt;</code> — 제네릭. "이 상태는 User 객체의 배열"임을 TypeScript에게 명시</li>
    <li><code>([])</code> — 초기값. 처음엔 빈 배열, API 응답 받으면 채워짐</li>
  </ul>
</div>

<div v-click class="box-green mt-3 text-sm">
  <strong>에디터에서 확인:</strong> <code>users.</code> 입력 후 자동완성 → <code>.length</code>, <code>.map</code>, <code>.filter</code> 등 표시<br/>
  <code>users[0].</code> 입력 후 자동완성 → <code>.name</code>, <code>.email</code>, <code>.id</code> 등 User interface 속성 표시
</div>

<!--
[스크립트]
첫 번째 단계입니다. VS Code에서 App.tsx를 열고 파일 상단에서 "TODO (필수 1-a)" 주석을 찾아보겠습니다.

주석 바로 아래에 다음 한 줄을 입력합니다.

const [users, setUsers] = useState<User[]>([]);

[click]

입력한 코드의 각 부분을 설명합니다. 코드를 보면 네 개의 구분된 부분이 있습니다. 첫 번째, const [users, setUsers]는 배열 구조분해입니다. 세션 3에서 배운 내용이죠. useState는 항상 두 개짜리 배열을 반환합니다. 첫 번째가 현재 상태 값이고, 두 번째가 그 값을 변경하는 함수입니다. users는 현재 사용자 목록이고, setUsers는 "사용자 목록을 이 값으로 교체해라"라고 React에게 알리는 함수입니다.

두 번째, useState<User[]>에서 꺾쇠 안의 User[]가 제네릭입니다. "이 상태는 User 객체들의 배열이다"라고 TypeScript에게 명시합니다. User 타입은 types.ts에 정의되어 있습니다. id, name, email, phone 등의 속성을 가진 interface입니다.

세 번째, 괄호 안의 []는 초기값입니다. 앱이 처음 시작할 때는 사용자 목록이 없으므로 빈 배열로 시작합니다. API에서 데이터를 받아오면 setUsers로 채우게 됩니다.

[click]

이제 에디터에서 users.을 타이핑해보겠습니다. 자동완성 목록에 .length, .map, .filter 등 배열 메서드가 나타납니다. users[0].을 타이핑하면 User interface에 정의된 .name, .email, .id 등 속성이 나타납니다. 이것이 TypeScript 제네릭의 효과입니다. 타입을 명시했기 때문에 에디터가 정확히 어떤 속성이 있는지 알고 있습니다.

시간: 5분
-->

---

# Step 1-b: selectedUser 상태 선언

바로 아래 줄에 이어서 입력합니다

<div v-click>

```tsx {1|2-3}
const [selectedUser, setSelectedUser] = useState<User | null>(null);
//                                               ^^^^^^^^^^^
//                                    "User이거나 null이거나" — Union 타입
```

</div>

<div v-click class="grid grid-cols-2 gap-4 mt-4">
<div class="box-blue">
  <strong>Union 타입 복습</strong>
  <p class="text-sm mt-1">세션 1에서 배운 <code>string | number</code> 패턴과 동일<br/>
  지금은 "User 객체 <em>또는</em> null"</p>
  <p class="text-sm mt-2">초기값 null → 처음엔 아무도 선택 안 됨<br/>
  카드 클릭 → setSelectedUser(user) → User 객체가 됨</p>
</div>
<div class="box-red">
  <strong>임시 변수 반드시 삭제!</strong>
  <p class="text-sm mt-1">파일 아래쪽에 이런 줄이 있습니다:</p>

```tsx
// 이 두 줄을 찾아서 삭제하세요
const users = JSON.parse("[]") as User[];
const selectedUser = JSON.parse("null") as User | null;
```

  <p class="text-sm mt-1">useState와 변수 이름이 겹쳐 TypeScript 오류 발생!</p>
</div>
</div>

<!--
[스크립트]
이제 바로 아래 줄에 selectedUser 상태를 선언합니다.

const [selectedUser, setSelectedUser] = useState<User | null>(null);

[click]

이 코드의 핵심은 User | null이라는 Union 타입입니다. 세션 1에서 string | number 같은 Union 타입을 배웠습니다. 지금은 "User 객체이거나, null이거나" 두 가지 상태를 표현합니다.

처음에는 아무도 선택되지 않았으므로 초기값이 null입니다. 사용자가 카드를 클릭하면 setSelectedUser(user)가 호출되어 그 User 객체가 상태에 저장됩니다.

[click]

매우 중요한 것이 있습니다. App.tsx 파일을 아래로 스크롤하면 렌더링 영역 직전에 이런 임시 변수들이 있습니다. "TODO 구현 전 에러 방지용"이라고 주석이 달린 두 줄입니다. 이것을 반드시 삭제해야 합니다.

삭제하지 않으면 같은 이름의 변수가 두 번 선언되어 TypeScript가 "Cannot redeclare block-scoped variable" 오류를 냅니다. 파일에서 JSON.parse("[]")와 JSON.parse("null")이 있는 줄 두 개를 찾아서 지워주십시오.

지금 제가 그 두 줄을 찾아서 삭제하겠습니다. 보이시나요? 이 줄과 이 줄입니다. 삭제 완료했습니다. 저장 후 브라우저를 보면 스켈레톤 로딩 애니메이션이 계속 돌아가고 있어야 합니다. 아직 fetch를 구현하지 않았으니 로딩 상태가 지속되는 것이 정상입니다.

[Q&A 대비]
Q: 임시 변수를 왜 처음부터 넣어뒀나요?
A: 여러분이 useState를 만들기 전에도 앱이 타입 오류 없이 실행되도록 플레이스홀더로 넣어둔 것입니다. 이제 진짜 useState 변수를 만들었으니 불필요해졌습니다.

시간: 4분
-->

---

# Step 1-c: useEffect + fetch 구현 (1/2)

`// TODO (필수 1-c)` 주석 아래의 빈 useEffect를 채웁니다

```tsx {1-3|4-5|6|7|8|9|10}
useEffect(() => {
  const fetchUsers = async () => {         // ① 내부에 async 함수 정의
    const res = await fetch(`${API}/users`); // ② HTTP GET 요청
    const data: User[] = await res.json();   // ③ JSON 파싱 + 타입 명시
    setUsers(data);                          // ④ 상태 업데이트
    setLoading(false);                       // ⑤ 로딩 종료
  };
  fetchUsers();  // ⑥ 반드시 호출 (없으면 함수 정의만 되고 실행 안 됨)
}, []);          // ⑦ 빈 배열 = 마운트 시 한 번만
```

<div v-click class="box-blue mt-4 text-sm">
  <strong>API 상수가 뭔가요?</strong><br/>
  파일 맨 위에 <code>const API = 'https://jsonplaceholder.typicode.com'</code>이 선언되어 있습니다.<br/>
  백틱 템플릿 리터럴로 조합하면 → <code>https://jsonplaceholder.typicode.com/users</code>
</div>

<!--
[스크립트]
이제 가장 핵심적인 부분입니다. useEffect 안에 fetch 로직을 구현합니다. 코드가 9줄 정도 되는데, 한 줄씩 천천히 설명하겠습니다. 잠깐, 지금부터 화면에 집중해 주십시오.

먼저 파일에서 "TODO (필수 1-c)" 주석을 찾아봅니다. 그 아래에 이미 빈 useEffect가 있습니다. 이 useEffect의 콜백 안에 코드를 채웁니다. const fetchUsers = async () => { 라고 입력합니다. 앞서 설명한 패턴대로 useEffect 콜백 자체를 async로 만들 수 없으므로, 내부에 async 함수를 새로 정의합니다. 이름은 fetchUsers, 하는 일은 사용자 목록을 가져오는 것입니다.

[click — 두 번째 줄]

const res = await fetch(`${API}/users`);를 입력합니다.
fetch는 브라우저에 내장된 함수로, URL에 HTTP 요청을 보냅니다. 기본은 GET 요청입니다. await는 이 네트워크 요청이 완료될 때까지 기다립니다. 결과로 받는 res는 Response 객체입니다. 아직 실제 데이터가 아닙니다. 봉투만 받은 상태라고 생각하시면 됩니다.

[click — 세 번째 줄]

const data: User[] = await res.json();를 입력합니다.
res.json()은 Response 봉투를 열어 안의 JSON 데이터를 JavaScript 객체로 변환합니다. 이것도 비동기 작업이므로 await가 필요합니다. 결과를 User[] 타입으로 명시했습니다. TypeScript는 API 응답이 정말 User[]인지 런타임에서는 검증하지 않습니다. 우리가 올바른 타입을 직접 지정해야 합니다.

[click — 네 번째 줄]

setUsers(data)를 입력합니다.
가져온 사용자 10명 데이터를 users 상태에 저장합니다. 상태가 바뀌면 React가 컴포넌트를 자동으로 다시 렌더링합니다. 이것이 React의 핵심 동작 원리입니다.

[click — 다섯 번째 줄]

setLoading(false)를 입력합니다.
loading 상태는 파일 위쪽에서 useState(true)로 시작합니다. 데이터를 모두 받아오면 false로 바꿉니다. 이 값이 false가 되면 스켈레톤 대신 실제 컴포넌트가 표시됩니다.

[click — 여섯 번째 줄, 닫는 중괄호 이후]

fetchUsers()를 입력합니다. 이 줄이 없으면 함수를 정의만 하고 실행하지 않게 됩니다. 처음 배울 때 이 줄을 빠트리는 실수가 정말 많습니다. 반드시 함수 정의 바로 아래에 호출 줄을 넣으십시오.

[click — 마지막 줄]

}, []); 에서 빈 배열입니다. "마운트 시 딱 한 번만 실행"입니다. 사용자 목록은 앱 시작 시 한 번만 가져오면 됩니다.

[click]

파일 상단의 API 상수를 확인합니다. const API = 'https://jsonplaceholder.typicode.com'이 선언되어 있으므로 백틱 템플릿 리터럴로 ${API}/users라고 쓰면 완전한 URL이 조합됩니다.

시간: 8분
-->

---

# Step 1-c: 저장 후 브라우저 확인

<div class="box-green mb-4">
  저장(Ctrl+S / Cmd+S) 후 브라우저로 이동합니다
</div>

<div class="grid grid-cols-2 gap-4">
<div>

**브라우저에서 확인할 것**

<div v-click class="space-y-2 mt-2">
  <div class="box-blue text-sm">
    왼쪽 사이드바에 잠깐 스켈레톤이 보이다가<br/>사용자 카드 10개가 나타난다
  </div>
  <div class="box-blue text-sm mt-2">
    개발자 도구(F12) → Network 탭 →<br/>
    <code>users</code> 요청이 Status 200 OK
  </div>
</div>

</div>
<div>

<div v-click class="box-red mt-2">
  <strong>이 시점에서 흔한 실수</strong>
  <ul class="text-sm mt-1 space-y-1">
    <li>fetchUsers() 호출 줄 누락 → 계속 로딩만 됨</li>
    <li>setLoading(false) 누락 → 데이터는 있지만 스켈레톤 계속 표시</li>
    <li>의존성 배열 [] 누락 → 무한 루프 (계속 fetch 반복)</li>
  </ul>
</div>

</div>
</div>

<!--
[스크립트]
코드를 저장하고 브라우저로 이동합니다.

[click]

보이시나요? 잠깐 스켈레톤 로딩이 나타났다가 왼쪽 사이드바에 사용자 카드 10개가 채워집니다. JSONPlaceholder API에서 실제 데이터를 받아온 것입니다.

개발자 도구를 열어서 Network 탭을 확인해보겠습니다. 여기에 users라는 요청이 보입니다. Status가 200 OK입니다. 성공적으로 데이터를 받아왔습니다.

아직 카드를 클릭해도 오른쪽에 아무것도 나타나지 않습니다. Step 1-d를 구현하면 렌더링됩니다.

[click]

이 단계에서 흔히 나타나는 실수 세 가지입니다. fetchUsers() 호출 줄을 빠트리면 함수가 정의만 되고 실행되지 않아 계속 로딩 상태가 유지됩니다. setLoading(false)를 빠트리면 데이터는 상태에 저장됐지만 로딩 플래그가 true인 채로 있어서 스켈레톤이 계속 표시됩니다. 의존성 배열을 아예 안 쓰면 컴포넌트가 렌더링될 때마다 useEffect가 실행되어 무한 fetch 루프가 생깁니다.

시간: 3분
-->

---

# Step 1-d: UserCard 렌더링

렌더링 부분으로 스크롤 → `TODO (필수 1-d)` 주석 아래 찾기

<div class="grid grid-cols-2 gap-4">
<div>

**변경 전 (삭제할 것)**

```tsx
{/* TODO (필수 1-d): ... */}
<p className="text-sm text-slate-400">
  TODO: UserCard를 렌더링하세요
</p>
```

</div>
<div>

**변경 후 (입력할 것)**

```tsx {1|2-3|4|5}
{users.map((user) => (
  <UserCard
    key={user.id}
    user={user}
    selected={selectedUser?.id === user.id}
    onClick={setSelectedUser}
  />
))}
```

</div>
</div>

<div v-click class="box-blue mt-4 text-sm">
  <strong>각 prop 설명</strong>
  <ul class="mt-1 space-y-1">
    <li><code>key={user.id}</code> — React 리스트 고유 식별자. 1~10 정수. 없으면 경고 발생</li>
    <li><code>selected={selectedUser?.id === user.id}</code> — 옵셔널 체이닝. null이면 false, 같은 id면 true → 강조 표시</li>
    <li><code>onClick={setSelectedUser}</code> — 콜백 props 패턴. 카드 클릭 시 App의 state를 변경</li>
  </ul>
</div>

<!--
[스크립트]
이제 마지막 단계입니다. 렌더링 부분으로 스크롤합니다. "TODO (필수 1-d)" 주석과 함께 "TODO: UserCard를 렌더링하세요"라는 안내 문단이 있습니다. 이 p 태그를 삭제하고, 주석 처리된 UserCard 코드를 실제 코드로 입력합니다.

먼저 안내 p 태그를 삭제합니다. 그리고 다음 코드를 입력합니다.

users.map로 시작하는 코드를 입력하겠습니다. users.map((user) => ( — 세션 4 Thinking in React에서 배운 리스트 렌더링 패턴입니다. users 배열의 각 요소를 UserCard 컴포넌트로 변환합니다. users에 10개의 User 객체가 있으면 UserCard가 10개 렌더링됩니다.

[click — key와 user prop]

key={user.id}는 React가 리스트 항목들을 효율적으로 구별하기 위해 필요한 고유 식별자입니다. user.id는 JSONPlaceholder가 1부터 10까지 부여한 정수입니다.

user={user}는 UserCard 컴포넌트에 User 객체 전체를 props로 전달합니다.

[click — selected prop]

selected={selectedUser?.id === user.id}를 보겠습니다. ?. 기호가 있습니다. 이것이 옵셔널 체이닝입니다. selectedUser가 null이면 undefined를 반환하고, undefined === user.id는 false가 됩니다. selectedUser가 null이 아니면 id를 비교합니다. 이 값이 true인 카드는 파란색 테두리로 강조 표시됩니다.

[click — onClick prop]

onClick={setSelectedUser}는 콜백 props 패턴입니다. 세션 4 Thinking in React에서 배운 "상태 끌어올리기"와 같은 원리입니다. UserCard 내부에서 클릭 이벤트가 발생하면 onClick(user)를 호출하고, 그것이 App의 setSelectedUser(user)를 실행합니다. 클릭된 사용자가 selectedUser 상태에 저장되고 컴포넌트가 다시 렌더링됩니다.

이제 저장하고 브라우저에서 카드를 클릭해봅니다. 오른쪽에 사용자 정보가 나타나고, 클릭한 카드가 강조 표시되어야 합니다.

시간: 7분
-->

---

# Task 1 완료 확인 체크리스트

<div class="grid grid-cols-2 gap-6">
<div>

<div class="practice-point">
  <strong>브라우저에서 확인</strong>
  <ul class="mt-2 space-y-2 text-sm">
    <li v-click>✅ 왼쪽 사이드바에 사용자 10명 카드 표시</li>
    <li v-click>✅ 카드 클릭 시 오른쪽에 이름·이메일·회사 표시</li>
    <li v-click>✅ 선택된 카드가 파란 테두리로 강조</li>
    <li v-click>✅ 다른 카드 클릭 시 강조가 이동</li>
  </ul>
</div>

</div>
<div>

<div class="box-red mt-2">
  <strong>코드 체크</strong>
  <ul class="text-sm mt-1 space-y-1">
    <li v-click>☐ 임시 변수 두 줄 (JSON.parse) 삭제 완료</li>
    <li v-click>☐ fetchUsers() 호출 줄 있음</li>
    <li v-click>☐ 의존성 배열 <code>[]</code> 있음</li>
  </ul>
</div>

<div class="box-yellow mt-3 text-sm">
  아직 Posts 탭이 비어있는 것이 정상입니다.<br/>
  Task 2에서 게시글 fetch를 구현합니다.
</div>

</div>
</div>

<!--
[스크립트]
Task 1이 완성됐는지 확인합니다.

[click]
왼쪽 사이드바에 사용자 10명 카드가 표시됩니다.

[click]
카드를 클릭하면 오른쪽에 이름, 이메일, 회사 이름이 나타납니다.

[click]
선택된 카드가 파란 테두리로 강조 표시됩니다.

[click]
다른 카드를 클릭하면 강조가 그 카드로 이동합니다.

[click]
코드 측면에서는 임시 변수 두 줄이 삭제되었는지 확인합니다.

[click]
fetchUsers() 호출 줄이 있는지 확인합니다.

[click]
의존성 배열 빈 배열이 있는지 확인합니다.

오른쪽 메인 영역에서 Posts 탭이 아직 비어있는 것은 정상입니다. Task 2를 구현하면 채워집니다.

Task 1이 완성된 분들은 잠깐 기다려 주십시오. 5분 후부터 여러분이 직접 Task 2부터 구현합니다.

시간: 2분
-->

---

# YOU DO — Task 2: 게시글 목록

<div class="grid grid-cols-2 gap-4">
<div>

<div class="box-blue mb-3">
  <strong>난이도: ★★☆☆☆</strong> | 예상 시간: 15분<br/>
  Task 1-c 패턴을 거의 그대로 응용
</div>

**구현할 TODO**
- `(필수 2-a)`: posts 상태 선언 — `Post[]` 타입
- `(필수 2-b)`: selectedUser 의존 useEffect
- 렌더링 부분: PostCard 주석 해제

**핵심 힌트**
```tsx
useEffect(() => {
  if (!selectedUser) return;  // null이면 종료
  const fetchPosts = async () => {
    // URL: `${API}/posts?userId=${selectedUser.id}`
    // 타입: Post[]
    // setter: setPosts
  };
  fetchPosts();
}, [selectedUser]); // ← 이것이 Task 1-c와의 차이!
```

</div>
<div>

<div class="box-yellow">
  <strong>Task 1과의 차이점 2가지</strong>
  <ol class="text-sm mt-2 space-y-2">
    <li><strong>의존성 배열</strong>: <code>[]</code> → <code>[selectedUser]</code><br/>
    사용자가 바뀔 때마다 새 게시글을 가져와야 함</li>
    <li><strong>조건부 조기 반환</strong>: <code>if (!selectedUser) return;</code><br/>
    selectedUser가 null일 때 fetch 방지</li>
  </ol>
</div>

<div class="box-green mt-3 text-sm">
  <strong>예상 결과</strong><br/>
  사용자 클릭 → Posts 탭에 게시글 목록 표시<br/>
  다른 사용자 클릭 → 게시글 목록 교체
</div>

</div>
</div>

<!--
[스크립트]
자, 이제 여러분 차례입니다! Task 2부터는 여러분이 직접 구현합니다.

Task 2는 난이도 별 두 개짜리입니다. Task 1-c에서 시연한 패턴을 거의 그대로 쓰면 됩니다. 다른 점은 딱 두 가지입니다.

첫 번째, 의존성 배열에 selectedUser를 넣어야 합니다. 사용자 목록과 달리 게시글은 선택된 사용자가 바뀔 때마다 새로 가져와야 합니다. 빈 배열 []을 쓰면 처음 한 번만 실행되어 다른 사용자를 클릭해도 게시글이 바뀌지 않습니다.

두 번째, 함수 맨 위에 if (!selectedUser) return;을 추가합니다. 처음 컴포넌트가 마운트될 때 selectedUser는 null입니다. null인 상태에서 fetch를 시도하면 URL에 undefined가 들어가 잘못된 요청이 됩니다. return으로 일찍 종료하면 그 문제를 막을 수 있습니다.

힌트 코드를 보면서 빈 부분을 채워보십시오. 막히면 손을 들어 주시면 순서대로 추가 힌트를 드리겠습니다.

시간: 15분 (수강생 실습)
-->

---

# YOU DO — Task 3 & 4: 게시글 추가 / 삭제

<div class="grid grid-cols-2 gap-4">
<div>

<div class="box-blue mb-3">
  <strong>Task 3 — POST 요청</strong> | ★★★☆☆ | 20분
</div>

```tsx
// addPost 함수 안에 구현 (필수 3)
const res = await fetch(`${API}/posts`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    title,
    body,
    userId: selectedUser!.id,  // ! = null 아님 보장
  }),
});
const newPost: Post = await res.json();
// id 충돌 방지: 서버는 항상 101을 반환하므로
setPosts((prev) => [{ ...newPost, id: Date.now() }, ...prev]);
```

</div>
<div>

<div class="box-blue mb-3">
  <strong>Task 4 — DELETE 요청</strong> | ★★☆☆☆ | 10분
</div>

```tsx
// deletePost 함수 (필수 4)
const deletePost = async (id: number) => {
  await fetch(`${API}/posts/${id}`, {
    method: "DELETE",
  });
  // filter로 해당 id 제거 (불변 업데이트!)
  setPosts((prev) => prev.filter((p) => p.id !== id));
};
```

<div class="box-red mt-3 text-sm">
  Task 4는 파일 두 개 수정!<br/>
  <code>App.tsx</code>의 deletePost 함수 구현 +<br/>
  <code>PostCard.tsx</code>의 버튼 onClick 연결 필요
</div>

</div>
</div>

<!--
[스크립트]
Task 3과 4를 함께 안내합니다.

Task 3은 게시글 추가입니다. GET 요청과 달리 POST 요청은 fetch의 두 번째 인자에 옵션 객체를 전달합니다. method는 "POST", headers에는 Content-Type 헤더, body에는 JSON.stringify로 변환한 데이터를 넣습니다.

selectedUser!.id에서 느낌표가 있습니다. 이것은 Non-null assertion입니다. TypeScript에게 "이 시점에 selectedUser는 절대 null이 아님을 내가 보장한다"고 알리는 것입니다. addPost 함수는 사용자를 선택했을 때만 보이는 PostForm에서 호출되므로 이 시점에 selectedUser가 null일 수 없습니다.

상태 업데이트 부분에서 setPosts((prev) => [{ ...newPost, id: Date.now() }, ...prev])를 씁니다. 서버는 항상 id: 101을 반환하므로, 여러 게시글을 추가하면 모든 id가 101이 되어 React의 key가 충돌합니다. Date.now()로 유니크한 타임스탬프를 id로 사용합니다.

Task 4는 게시글 삭제입니다. DELETE 요청을 보내고, filter로 해당 id를 가진 게시글을 배열에서 제거합니다. 세션 4 Tic-Tac-Toe에서 배운 불변 업데이트 패턴과 동일합니다.

중요한 것은 Task 4가 두 개의 파일을 수정해야 한다는 점입니다. App.tsx에 deletePost 함수를 구현하고, PostCard.tsx의 삭제 버튼에 onClick을 연결해야 합니다. 두 번째 파일을 빠트리는 실수가 많습니다.

시간: 30분 (수강생 실습)
-->

---

# YOU DO — Task 5 & 6: Todo 토글 / 댓글

<div class="grid grid-cols-2 gap-4">
<div>

<div class="box-blue mb-2">
  <strong>Task 5 — Todo 완료 토글</strong> | ★★★☆☆ | 20분<br/>
  파일: <code>src/components/TodoSection.tsx</code>
</div>

**핵심 패턴: map으로 특정 항목만 변경**

```tsx
// toggleTodo 함수 (필수 5-c)
setTodos((prev) =>
  prev.map((t) => {
    if (t.id !== id) return t;               // 해당 아님 → 그대로
    return { ...t, completed: !t.completed }; // 해당 → completed 반전
  })
);
// PATCH 요청 (상태 업데이트 후)
fetch(`${API}/todos/${id}`, {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ completed: true }),
});
```

</div>
<div>

<div class="box-blue mb-2">
  <strong>Task 6 — 댓글 표시</strong> | ★★★☆☆ | 20분<br/>
  파일: <code>src/components/CommentList.tsx</code>
</div>

**핵심 패턴: 처음 클릭 시에만 fetch**

```tsx
// toggle 함수 (필수 6-b)
const toggle = async () => {
  // 처음 열 때만 fetch
  if (!open && comments.length === 0) {
    const res = await fetch(
      `${API}/posts/${postId}/comments`
    );
    const data: Comment[] = await res.json();
    setComments(data);
  }
  setOpen((prev) => !prev); // 토글
};
```

<div class="box-yellow mt-2 text-sm">
  Task 5: 파일 아래쪽의 <code>const todos: Todo[] = []</code> 임시 변수 삭제 필수!
</div>

</div>
</div>

<!--
[스크립트]
Task 5와 6을 함께 안내합니다.

Task 5는 Todos 탭의 할 일 완료 토글입니다. TodoSection.tsx 파일에서 작업합니다. App.tsx에서 했던 것처럼 todos 상태를 선언하고, userId를 의존성 배열로 갖는 useEffect로 할 일 목록을 fetch합니다.

핵심은 toggleTodo 함수입니다. 특정 id의 completed 속성만 반전시켜야 합니다. 이때 map을 씁니다. 배열을 순회하면서 id가 일치하지 않는 항목은 그대로 반환하고, 일치하는 항목만 스프레드 연산자로 복사하면서 completed를 !t.completed로 반전시킵니다. 이것이 "특정 항목만 변경하는 불변 업데이트" 패턴입니다. Tic-Tac-Toe에서 squares 배열을 불변으로 업데이트한 것과 똑같은 원리입니다.

중요: TodoSection.tsx 파일 아래쪽에 const todos: Todo[] = []라는 임시 변수가 있습니다. 반드시 삭제해야 합니다. 이것을 삭제하지 않으면 useState로 만든 todos가 이 임시 변수에 가려져서 항상 빈 배열로 보입니다.

Task 6은 댓글 표시입니다. "처음 클릭 시에만 fetch"하는 패턴이 핵심입니다. 조건을 보면 !open && comments.length === 0입니다. "현재 접혀있고 아직 댓글을 한 번도 불러오지 않았을 때"만 fetch합니다. 이미 댓글을 불러온 적이 있으면 open 상태만 토글합니다.

시간: 40분 (수강생 실습)
-->

---

# 도전 과제 소개 (Tasks 7–11)

<div class="box-yellow mb-4">
  필수 과제 6개를 먼저 완성한 수강생을 위한 추가 도전입니다
</div>

<div class="grid grid-cols-2 gap-4">
<div>

| Task | 내용 | 난이도 |
|------|------|--------|
| 7 | AlbumGallery 구현 | ★★★☆☆ |
| 8 | **Promise.all** 병렬 fetch | ★★★★☆ |
| 9 | **useMemo** 검색 필터링 | ★★★☆☆ |
| 10 | Skeleton 로딩 상태 | ★★★★☆ |
| 11 | StatsUpdateFn 콜백 | ★★★★★ |

</div>
<div>

<div class="box-blue text-sm">
  <strong>Task 8 — Promise.all 핵심 개념</strong><br/>
  5개 API를 순서대로 호출하면 최대 2.5초<br/>
  Promise.all로 병렬 호출하면 가장 느린 1개 분의 시간만!

```tsx
Promise.all([
  fetch(`${API}/posts`).then(r => r.json()),
  fetch(`${API}/comments`).then(r => r.json()),
  // ...
]).then(([posts, comments, ...]) => {
  setStats({ posts: posts.length, ... });
});
```
</div>

</div>
</div>

<!--
[스크립트]
필수 과제를 모두 완성한 분들을 위한 도전 과제를 소개합니다.

Task 7은 AlbumGallery입니다. userId가 바뀔 때마다 앨범을 fetch하고, 앨범을 클릭하면 사진 목록을 추가로 fetch하는 패턴입니다.

Task 8이 가장 흥미로운 도전입니다. Promise.all로 여러 API를 동시에 호출합니다. 5개 API를 순서대로 호출하면 각각 500ms씩 걸린다고 가정할 때 최대 2.5초가 걸립니다. Promise.all로 병렬 호출하면 가장 느린 요청 하나 분의 시간, 약 500ms만 걸립니다.

Task 9는 useMemo로 검색 필터링을 구현합니다. 검색창에 텍스트를 입력하면 게시글 제목과 본문에서 검색어가 포함된 것만 필터링합니다. useMemo는 의존하는 값이 바뀔 때만 재계산하는 메모이제이션 훅입니다.

Task 10, 11은 고급 패턴으로 자신 있는 분들만 도전하십시오.

solutions 폴더에 모든 도전 과제의 정답 코드가 있습니다. 스스로 먼저 시도해보고, 정말 막힐 때 참고하십시오.

시간: 2분
-->

---

# 트러블슈팅 Top 5

<div class="box-red">
  <strong>실습 중 가장 많이 나오는 오류들</strong>
</div>

<div class="grid grid-cols-2 gap-3 mt-3">
<div class="space-y-2">

<div class="box-red text-sm">
  <strong>① selectedUser is possibly null</strong><br/>
  useEffect 안 또는 함수에서 null 체크 없이 접근<br/>
  → <code>if (!selectedUser) return;</code> 추가
</div>

<div class="box-red text-sm">
  <strong>② Cannot redeclare block-scoped variable</strong><br/>
  useState를 만들었는데 임시 변수를 아직 삭제 안 함<br/>
  → App.tsx와 TodoSection.tsx의 임시 변수 삭제
</div>

<div class="box-red text-sm">
  <strong>③ 사용자 바꿔도 게시글 안 바뀜</strong><br/>
  의존성 배열에 <code>selectedUser</code> 미포함<br/>
  → <code>}, [selectedUser]);</code> 로 수정
</div>

</div>
<div class="space-y-2">

<div class="box-red text-sm">
  <strong>④ useEffect async 직접 사용</strong><br/>
  <code>useEffect(async () => ...</code> 패턴 사용 시 경고<br/>
  → 내부에 async 함수 정의 후 호출 패턴으로 변경
</div>

<div class="box-red text-sm">
  <strong>⑤ 게시글 삭제/추가 후 목록 안 바뀜</strong><br/>
  <code>posts.push(newPost)</code> 같은 직접 변경<br/>
  → <code>setPosts(prev =&gt; [newPost, ...prev])</code><br/>
  또는 PostCard.tsx onClick 연결 누락
</div>

</div>
</div>

<!--
[스크립트]
실습 중 가장 자주 만나는 오류 다섯 가지입니다. 오류가 났을 때 이 슬라이드를 먼저 확인하십시오.

첫 번째는 "selectedUser is possibly null" 오류입니다. selectedUser가 User | null 타입인데 null일 때도 접근하려 할 때 발생합니다. useEffect 안에서 발생한다면 맨 위에 if (!selectedUser) return;을 추가합니다.

두 번째는 "Cannot redeclare block-scoped variable" 오류입니다. useState로 변수를 만들었는데 아래쪽에 같은 이름의 임시 변수가 아직 남아있을 때 발생합니다. App.tsx의 JSON.parse 줄과 TodoSection.tsx의 const todos = [] 줄을 찾아 삭제합니다.

세 번째는 사용자를 바꿔도 게시글이 업데이트되지 않는 문제입니다. Task 2 useEffect의 의존성 배열을 확인합니다. []가 아닌 [selectedUser]여야 합니다.

네 번째는 useEffect 콜백을 async로 직접 만든 경우입니다. useEffect(async () => ...) 패턴은 사용하지 않습니다.

다섯 번째는 게시글을 추가하거나 삭제해도 화면이 안 바뀌는 경우입니다. posts 배열을 직접 변경하면 React가 변화를 감지하지 못합니다. 반드시 새 배열을 만드는 불변 업데이트를 써야 합니다. Task 4에서는 PostCard.tsx의 버튼 onClick을 연결했는지도 확인하십시오.

시간: 2분
-->

---
layout: section
---

# Quiz Time!

<div class="box-blue mt-6 text-center">
  오늘 배운 내용을 확인합니다<br/>
  <span class="text-sm">문제 풀이 10분 · 해설 5분</span>
</div>

<!--
[스크립트]
실습을 마무리하고 퀴즈 시간입니다. 오늘 하루 배운 TypeScript와 React의 핵심 개념들을 문제로 확인해봅니다.

문제는 10분간 각자 풀고, 이후 5분간 같이 해설합니다. 정답지를 넘기지 말고 먼저 스스로 생각해보십시오.

시간: 1분
-->

---

# 오늘 배운 핵심 정리

<div class="grid grid-cols-2 gap-4">
<div>

<div v-click class="box-blue mb-3">
  <strong>TypeScript 핵심</strong>
  <ul class="text-sm mt-2 space-y-1">
    <li>기본 타입: string, number, boolean, 배열, 객체</li>
    <li>interface: 객체 구조 정의 (User, Post, Todo...)</li>
    <li>Union 타입: <code>User | null</code>, <code>string | number</code></li>
    <li>제네릭: <code>useState&lt;User[]&gt;</code>, <code>identity&lt;T&gt;</code></li>
    <li>옵셔널 체이닝: <code>user?.name</code></li>
    <li>Non-null assertion: <code>user!.id</code></li>
  </ul>
</div>

</div>
<div>

<div v-click class="box-green mb-3">
  <strong>React 핵심</strong>
  <ul class="text-sm mt-2 space-y-1">
    <li>컴포넌트: JSX를 반환하는 함수</li>
    <li>Props: 부모 → 자식 데이터 전달 (단방향)</li>
    <li>useState: 상태 관리, 변경 시 리렌더링</li>
    <li>useEffect: 사이드 이펙트 (fetch, 구독 등)</li>
    <li>콜백 Props: 자식 → 부모 상태 변경 패턴</li>
    <li>불변 업데이트: filter, map, 스프레드 연산자</li>
  </ul>
</div>

</div>
</div>

<div v-click class="box-yellow mt-3 text-sm">
  <strong>오늘 실습에서 쓴 패턴 세 가지</strong><br/>
  <code>useState&lt;T[]&gt;([])</code> 제네릭 상태 선언 &nbsp;|&nbsp;
  useEffect + 내부 async 함수 패턴 &nbsp;|&nbsp;
  filter / map 불변 업데이트
</div>

<!--
[스크립트]
오늘 하루 동안 배운 핵심을 정리합니다.

[click]

TypeScript 핵심입니다. 기본 타입부터 시작해서 interface로 실제 데이터 구조를 모델링하는 방법을 배웠습니다. Union 타입으로 여러 상태를 안전하게 표현하고, 제네릭으로 useState를 타입 안전하게 사용했습니다. 옵셔널 체이닝과 Non-null assertion으로 null을 안전하게 다루는 법도 배웠습니다.

[click]

React 핵심입니다. 함수형 컴포넌트, Props, useState, useEffect의 네 가지가 React의 뼈대입니다. 콜백 Props 패턴으로 자식 컴포넌트에서 부모의 상태를 변경하는 "상태 끌어올리기"를 실습했습니다. filter, map, 스프레드 연산자로 배열을 불변으로 업데이트하는 패턴은 React 실무에서 매일 쓰는 패턴입니다.

[click]

오늘 실습에서 가장 많이 반복한 세 가지 패턴입니다. 이 세 가지만 완전히 이해해도 오늘 수업의 핵심을 모두 익힌 것입니다.

시간: 3분
-->

---

# 더 공부하려면

<div class="grid grid-cols-2 gap-4">
<div>

<div class="box-blue mb-3">
  <strong>다음 단계 라이브러리</strong>
  <ul class="text-sm mt-2 space-y-2">
    <li><strong>React Query (TanStack Query)</strong><br/>서버 상태 관리, 캐싱, 로딩/에러 자동 처리</li>
    <li><strong>React Router</strong><br/>SPA 페이지 전환 (/home, /about 라우팅)</li>
    <li><strong>Zustand / Jotai</strong><br/>전역 상태 관리 — useState의 한계를 넘어</li>
    <li><strong>TypeScript Handbook</strong><br/>unknown vs any, Mapped Types, Conditional Types</li>
  </ul>
</div>

</div>
<div>

<div class="box-green">
  <strong>공식 문서 링크</strong>
  <ul class="text-sm mt-2 space-y-2">
    <li>React 공식 문서<br/><code>react.dev</code></li>
    <li>TypeScript Handbook<br/><code>typescriptlang.org/docs/handbook</code></li>
    <li>TypeScript Exercises<br/><code>typescript-exercises.github.io</code></li>
    <li>JSONPlaceholder API<br/><code>jsonplaceholder.typicode.com</code></li>
  </ul>
</div>

<div class="box-yellow mt-3 text-sm">
  React 공식 문서는 한국어 번역도 있습니다.<br/>
  <code>ko.react.dev</code>
</div>

</div>
</div>

<!--
[스크립트]
오늘 수업을 마치고 더 공부하고 싶은 분들을 위해 다음 단계를 안내합니다.

React Query는 서버에서 데이터를 가져올 때 로딩 상태, 에러 처리, 캐싱을 자동으로 관리해주는 라이브러리입니다. 오늘 실습에서 직접 관리했던 loading 상태, fetch 로직을 훨씬 간결하게 처리할 수 있습니다. 실무에서 가장 많이 쓰는 React 라이브러리 중 하나입니다.

React Router는 한 페이지에서 여러 화면 전환을 처리합니다. /home, /about, /users/1 같은 URL 라우팅을 담당합니다.

Zustand는 컴포넌트 트리를 관통하는 전역 상태를 관리합니다. useState는 컴포넌트 단위 상태인데, 여러 컴포넌트가 같은 데이터를 공유해야 할 때 전역 상태 관리가 필요합니다.

공식 문서는 react.dev입니다. 한국어 번역 페이지도 ko.react.dev에서 제공됩니다. 오늘 실습한 Tic-Tac-Toe 튜토리얼과 Thinking in React 문서는 특히 추천합니다.

시간: 2분
-->

---
layout: center
---

# 수고하셨습니다!

<div class="text-center mt-6 space-y-4">
  <div class="box-green text-lg">
    오늘 하루 TypeScript와 React의 핵심을<br/>
    실제 앱으로 만들어 보셨습니다
  </div>

  <div class="grid grid-cols-3 gap-4 mt-6 text-sm">
    <div class="box-blue">
      <strong>참고 자료</strong><br/>
      react.dev<br/>
      ko.react.dev<br/>
      typescriptlang.org
    </div>
    <div class="box-blue">
      <strong>실습 코드</strong><br/>
      solutions/ 폴더에서<br/>
      정답 코드 확인 가능
    </div>
    <div class="box-blue">
      <strong>Q&A</strong><br/>
      궁금한 점은<br/>
      지금 질문해 주세요
    </div>
  </div>
</div>

<!--
[스크립트]
오늘 수업을 마칩니다. 수고 많으셨습니다.

아침에 TypeScript 기초부터 시작해서 interface, Union 타입, 제네릭을 배우고, Vite로 프로젝트를 만들었습니다. 오후에는 React Tic-Tac-Toe로 컴포넌트와 상태 관리의 기본을 익히고, Thinking in React로 데이터 흐름 설계 방식을 배웠습니다. 그리고 마지막으로 Social Dashboard 앱을 직접 만들며 모든 개념을 하나로 통합했습니다.

하루 만에 TypeScript와 React를 전부 완벽하게 익히기는 어렵습니다. 오늘 배운 내용을 집에서 한 번 더 처음부터 만들어보는 것이 가장 좋은 복습 방법입니다. 오늘 실습 코드를 혼자 다시 작성해보십시오.

solutions 폴더에 정답 코드가 있으니 참고하십시오. 더 공부하고 싶으신 분들은 react.dev의 공식 튜토리얼을 전부 따라해보시기를 추천합니다.

궁금한 점이 있으신 분들은 지금 질문해 주십시오. 감사합니다.

시간: 2분
-->
