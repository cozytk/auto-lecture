# Session 1: TypeScript 문법 기초 및 핵심

**시간**: 30분 | **유형**: 강의

---

## 학습 목표

이 세션을 마치면 수강생은 다음을 할 수 있습니다.

- TypeScript가 JavaScript에 비해 왜 필요한지 설명할 수 있습니다.
- `string`, `number`, `boolean`, `array`, `object` 등 기본 타입을 올바르게 사용할 수 있습니다.
- `interface`와 `type alias`를 정의하고, 두 가지의 쓰임 차이를 구분할 수 있습니다.
- `Union` 타입과 `Literal` 타입으로 API 응답 상태를 모델링할 수 있습니다.
- `typeof`, `in` 연산자를 이용한 타입 좁히기(Type Narrowing)를 이해합니다.
- 제네릭 문법(`<T>`)의 기본 형태를 인식하고, `useState<User[]>([])` 같은 코드를 읽을 수 있습니다.
- 함수에 매개변수 타입과 반환 타입을 붙이는 기본 방법을 알고 있습니다.

---

## 강사 준비 안내

이 가이드는 TypeScript를 처음 가르치는 강사도 수업을 진행할 수 있도록 최대한 상세하게 작성하였습니다. 각 절의 "강사 설명 포인트"를 참고하여 화이트보드 또는 IDE에서 코드를 직접 입력하며 설명하십시오. 수강생이 Java, Python, C# 등 다양한 배경을 가지고 있다고 가정하며, 각 언어의 타입 시스템과 비교하는 설명을 포함하였습니다.

---

## 1. TypeScript가 왜 필요한가 (5분)

### 강사 설명 포인트

JavaScript는 1995년 넷스케이프 브라우저에 처음 등장한 이래 30년 가까이 웹 개발의 핵심 언어로 자리잡아 왔습니다. 그러나 JavaScript는 근본적으로 **동적 타입(dynamic typed)** 언어입니다. 변수에 어떤 타입의 값도 자유롭게 할당할 수 있고, 이 자유로움은 소규모 스크립트에서는 편리하지만 대규모 애플리케이션에서는 큰 위험이 됩니다.

### 1.1 JavaScript의 동적 타입이 만드는 문제

다음 코드를 IDE에서 직접 입력하며 설명하십시오.

```javascript
// JavaScript 예시: 런타임까지 오류를 알 수 없습니다

function calculateTax(price, rate) {
  return price * rate; // price가 숫자인지 문자열인지 알 수 없습니다
}

// 의도: 1000원에 10% 세금 계산 → 100
console.log(calculateTax(1000, 0.1)); // 100 (정상)

// 실수: 문자열을 넘겼을 때 JavaScript는 오류를 내지 않습니다
console.log(calculateTax("1000", 0.1)); // "10001000" 이 아니라... NaN이 됩니다
// 실제로는 "1000" * 0.1 = 100 (JS가 암묵적 형변환) — 이게 더 위험합니다
```

이 코드는 문법적으로 완전히 올바릅니다. JavaScript 엔진은 아무런 경고도 내지 않습니다. 오류는 오직 런타임(코드가 실제 실행될 때)에만 드러납니다. 사용자가 이미 결제를 진행한 뒤에야 세금 계산이 잘못되었다는 것을 알게 될 수도 있습니다.

```javascript
// 더 심각한 예시: undefined 접근
function getUsername(user) {
  return user.name.toUpperCase(); // user가 null이면?
}

getUsername(null);
// TypeError: Cannot read properties of null (reading 'name')
// — 이 오류는 프로덕션 서버에서 발생할 때까지 아무도 모릅니다
```

### 1.2 TypeScript = JavaScript + 타입 시스템

TypeScript는 Microsoft가 개발한 JavaScript의 **슈퍼셋(superset)** 언어입니다. 슈퍼셋이란 TypeScript가 JavaScript를 완전히 포함한다는 의미입니다. 즉, 모든 유효한 JavaScript 코드는 TypeScript에서도 유효합니다.

```
JavaScript  ⊂  TypeScript
(JS는 TS의 부분집합)
```

TypeScript는 최종적으로 JavaScript로 **컴파일(compile)** 됩니다. 브라우저나 Node.js는 TypeScript를 직접 실행하지 않습니다. TypeScript 컴파일러(`tsc`)가 타입 정보를 제거하고 순수 JavaScript를 생성합니다.

```
TypeScript 코드 (.ts)
      ↓  tsc 컴파일
JavaScript 코드 (.js)
      ↓  브라우저/Node.js 실행
```

### 1.3 컴파일 타임 오류 감지

앞의 예시를 TypeScript로 작성하면 어떻게 달라지는지 보여주십시오.

```typescript
// TypeScript 예시: 컴파일 시점에 오류를 잡아냅니다

function calculateTax(price: number, rate: number): number {
  return price * rate;
}

calculateTax("1000", 0.1);
// TS 컴파일 오류: Argument of type 'string' is not assignable
// to parameter of type 'number'.
// → 코드를 저장하는 순간 IDE가 빨간 줄로 표시합니다
```

코드를 실행하기 전에, 심지어 파일을 저장하는 순간에 IDE(VS Code 등)가 오류를 표시합니다. Java나 C# 개발자라면 이미 익숙한 경험이고, Python 개발자에게는 새로운 개념일 수 있습니다.

**Java/C# 개발자에게**: TypeScript의 타입 시스템은 Java나 C#의 정적 타입과 개념적으로 매우 유사합니다. 다만 TypeScript는 구조적 타이핑(structural typing)을 사용한다는 점이 다릅니다. 이 부분은 이후 섹션에서 자연스럽게 익히게 됩니다.

**Python 개발자에게**: Python 3.5+에서 도입된 타입 힌트(type hints)와 목적은 같습니다. 다만 TypeScript는 타입 오류를 컴파일 단계에서 강제로 차단합니다.

### 1.4 실무 채택률

TypeScript는 2023-2024년 Stack Overflow 개발자 설문에서 가장 많이 사용하는 언어 5위 안에 꾸준히 들어 있습니다. GitHub에서 공개된 주요 프론트엔드 프레임워크(React, Vue, Angular, Next.js, Vite 등)는 모두 TypeScript로 작성되어 있습니다. 신규 프로젝트에서 TypeScript를 기본으로 선택하는 것이 이미 업계 표준이 되었습니다.

---

## 2. 기본 타입 (8분)

### 강사 설명 포인트

TypeScript의 기본 타입은 JavaScript의 원시 타입과 1대1로 대응합니다. 타입 어노테이션은 변수명 뒤에 콜론(`:`)을 붙이고 타입 이름을 씁니다.

### 2.1 원시 타입: string, number, boolean

**반드시 소문자를 사용합니다.** 이것은 초보자가 가장 많이 틀리는 부분입니다.

```typescript
// 올바른 예시: 소문자 타입을 사용합니다
const userName: string = "홍길동";        // 문자열
const userAge: number = 28;              // 정수와 실수 모두 number입니다
const isPremium: boolean = true;          // 불리언
const productPrice: number = 29.99;      // 실수도 number입니다

// 잘못된 예시: 대문자 타입은 JavaScript 래퍼 객체입니다 (절대 사용하지 마십시오)
const userName2: String = "홍길동";      // String은 래퍼 객체 타입입니다
const userAge2: Number = 28;             // Number는 래퍼 객체 타입입니다
const isPremium2: Boolean = true;        // Boolean은 래퍼 객체 타입입니다
```

**왜 대문자를 사용하면 안 되는가?**

Java나 C# 개발자라면 `String`(대문자)에 익숙할 것입니다. JavaScript에는 원시값 `"hello"`와 래퍼 객체 `new String("hello")` 두 가지가 모두 존재합니다. TypeScript에서 `String`(대문자)은 래퍼 객체 타입을 가리킵니다. 실제 코드에서 `new String("hello")`를 쓸 일은 거의 없으므로, TypeScript에서는 항상 소문자 `string`을 사용합니다.

```typescript
// 래퍼 객체와 원시값의 차이 (이해를 위한 예시)
const primitive: string = "hello";       // 원시값 — 이것을 사용하십시오
const wrapper: String = new String("hello"); // 래퍼 객체 — 사용하지 마십시오

// 실무에서 new String()을 쓸 이유는 없습니다
// TypeScript 공식 문서에서도 String/Number/Boolean 대신
// string/number/boolean 사용을 강력히 권고합니다
```

> **흔한 실수 1**: Java/C# 배경의 개발자가 `String`, `Integer`, `Boolean`을 그대로 쓰는 경우가 많습니다. TypeScript에서는 반드시 `string`, `number`, `boolean` 소문자를 사용하십시오.

### 2.2 배열 타입

TypeScript에서 배열 타입을 표현하는 방법은 두 가지입니다. 두 가지 모두 완전히 동일하게 동작합니다.

```typescript
// 방법 1: 타입 뒤에 [] 붙이기 — 더 많이 사용됩니다
const numbers: number[] = [1, 2, 3, 4, 5];
const userNames: string[] = ["홍길동", "김철수", "이영희"];
const flags: boolean[] = [true, false, true];

// 방법 2: 제네릭 표기법 Array<타입>
const numbers2: Array<number> = [1, 2, 3, 4, 5];
const userNames2: Array<string> = ["홍길동", "김철수", "이영희"];

// 어떤 방법을 써야 하는가?
// → 팀 코딩 컨벤션을 따르십시오. 일반적으로 number[]가 더 간결합니다.
// → React 프로젝트에서는 두 방식이 혼용됩니다. 둘 다 읽을 수 있어야 합니다.
```

```typescript
// 혼합 배열은 유니온 타입으로 표현합니다 (유니온은 섹션 4에서 다룹니다)
const mixed: (string | number)[] = ["홍길동", 28, "서울", 100];

// 잘못된 예시: 타입 없이 섞으면 any[] 가 됩니다
// const mixed2 = ["홍길동", 28, "서울", 100]; // any[]로 추론됩니다
```

### 2.3 object 타입과 인라인 타입 정의

object 타입을 표현하는 가장 기본적인 방법은 인라인 타입 정의입니다. 중괄호 `{}` 안에 각 속성의 이름과 타입을 적습니다.

```typescript
// 인라인 object 타입 정의
const user: { name: string; age: number; email: string } = {
  name: "홍길동",
  age: 28,
  email: "hong@example.com",
};

// 존재하지 않는 속성에 접근하면 컴파일 오류가 발생합니다
console.log(user.name);    // "홍길동" — 정상
console.log(user.phone);   // 컴파일 오류: Property 'phone' does not exist
```

그러나 인라인 타입 정의는 복잡해지면 코드가 읽기 어려워집니다. 섹션 3에서 배울 `interface`와 `type`을 사용하면 타입에 이름을 붙여 재사용할 수 있습니다.

### 2.4 타입 추론 (Type Inference)

TypeScript는 값을 할당할 때 타입을 **자동으로 추론**합니다. 명시적으로 타입을 적지 않아도 됩니다.

```typescript
// 타입 추론: TypeScript가 오른쪽 값을 보고 타입을 결정합니다
const productName = "노트북";       // TypeScript가 string으로 추론합니다
const productCount = 10;            // TypeScript가 number로 추론합니다
const inStock = true;               // TypeScript가 boolean으로 추론합니다

// 위 코드는 아래와 완전히 동일합니다
const productName2: string = "노트북";
const productCount2: number = 10;
const inStock2: boolean = true;
```

**언제 타입을 명시적으로 적어야 하는가?**

```typescript
// 1. 초기값이 없을 때는 명시적으로 적어야 합니다
let totalPrice: number;          // 나중에 값을 할당할 예정
totalPrice = 50000;              // 정상
totalPrice = "오만원";           // 컴파일 오류: string은 number에 할당 불가

// 2. 함수 매개변수는 추론이 되지 않으므로 항상 명시합니다
function greet(name: string): string {
  return `안녕하세요, ${name}님!`;
}

// 3. 빈 배열을 선언할 때는 타입을 명시하십시오
const items: string[] = [];      // string 배열로 명확히 지정
const items2 = [];               // any[]로 추론됩니다 — 피하십시오
```

**실무 팁**: 타입 추론이 가능한 곳에서 굳이 타입을 명시할 필요는 없습니다. 코드가 더 간결해집니다. 그러나 함수 시그니처(매개변수와 반환 타입)는 명시적으로 적는 것이 팀원과의 커뮤니케이션에 도움이 됩니다.

### 2.5 any 타입 — 왜 피해야 하는가

`any`는 TypeScript 타입 시스템을 완전히 우회하는 탈출구입니다. `any` 타입의 변수에는 어떤 값도 할당할 수 있고, 어떤 속성에도 접근할 수 있습니다.

```typescript
// any 타입: TypeScript의 타입 검사를 무력화합니다
let data: any = "문자열";
data = 42;                    // 정상 — any이므로 number도 됩니다
data = { name: "홍길동" };   // 정상 — any이므로 객체도 됩니다
data = null;                  // 정상 — any이므로 null도 됩니다

// any를 사용하면 타입 검사가 전혀 일어나지 않습니다
data.nonExistentMethod();     // 컴파일 오류 없음 — 런타임에서 터집니다
data.foo.bar.baz;             // 컴파일 오류 없음 — 런타임에서 터집니다
```

**`any`가 왜 문제인가?**

`any`를 사용하는 순간 그 변수는 "TypeScript 없는 JavaScript"와 동일합니다. TypeScript를 사용하는 이유(컴파일 타임 타입 검사)가 사라집니다. 더 나쁜 것은 `any`가 전파된다는 점입니다.

```typescript
// any 전파 예시
function processData(data: any) {
  return data.value; // any를 반환합니다
}

const result = processData({ value: "hello" });
// result의 타입이 any가 됩니다
// result를 사용하는 모든 곳에서 타입 검사가 무력화됩니다
result.toUpperCase();    // string이면 정상이지만...
result.toFixed(2);       // any이므로 컴파일 오류가 나지 않습니다
```

> **흔한 실수 2**: 타입을 모를 때 `any`로 빠르게 해결하려는 유혹이 있습니다. 대신 `unknown` 타입을 사용하십시오. `unknown`은 타입을 좁히지 않고는 사용할 수 없어서 `any`보다 안전합니다.

```typescript
// any 대신 unknown 사용 예시
function processApiResponse(response: unknown) {
  // unknown은 타입을 확인하기 전에는 사용할 수 없습니다
  if (typeof response === "string") {
    console.log(response.toUpperCase()); // string으로 좁혀진 후 사용
  }
  if (typeof response === "object" && response !== null && "value" in response) {
    // 타입 검사 후 사용 가능
    console.log((response as { value: unknown }).value);
  }
}
```

---

## 3. Interface와 Type (7분)

### 강사 설명 포인트

앞 섹션에서 인라인 object 타입이 복잡해질 수 있다고 언급했습니다. `interface`와 `type`은 타입에 이름을 붙여 재사용 가능하게 만드는 방법입니다.

### 3.1 Interface 정의

`interface`는 객체의 구조(속성 이름과 타입)를 정의하는 방법입니다. Java나 C#의 인터페이스와 단어는 같지만 의미가 조금 다릅니다. TypeScript의 `interface`는 메서드 시그니처뿐 아니라 속성도 정의합니다.

```typescript
// interface 정의
interface User {
  name: string;        // 사용자 이름 (필수)
  age: number;         // 나이 (필수)
  email: string;       // 이메일 (필수)
}

// interface를 타입으로 사용합니다
const user1: User = {
  name: "홍길동",
  age: 28,
  email: "hong@example.com",
};

// 속성이 누락되면 컴파일 오류가 발생합니다
const user2: User = {
  name: "김철수",
  age: 30,
  // email이 없으므로 컴파일 오류: Property 'email' is missing
};

// 정의되지 않은 속성을 추가해도 컴파일 오류가 발생합니다
const user3: User = {
  name: "이영희",
  age: 25,
  email: "lee@example.com",
  phone: "010-1234-5678",  // 컴파일 오류: Object literal may only specify known properties
};
```

**실제 프로젝트에서 자주 쓰이는 interface 패턴**

```typescript
// 상품 인터페이스 예시
interface Product {
  id: number;            // 상품 고유 ID
  name: string;          // 상품명
  price: number;         // 가격 (원 단위)
  category: string;      // 카테고리
  inStock: boolean;      // 재고 여부
}

// 함수 매개변수로 interface를 사용합니다
function displayProduct(product: Product): void {
  console.log(`[${product.category}] ${product.name} - ${product.price}원`);
  if (!product.inStock) {
    console.log("품절");
  }
}

const laptop: Product = {
  id: 1,
  name: "MacBook Pro 16인치",
  price: 3500000,
  category: "노트북",
  inStock: true,
};

displayProduct(laptop);
// [노트북] MacBook Pro 16인치 - 3500000원
```

> **흔한 실수 3**: Java 개발자 중 인터페이스 이름 앞에 `I`를 붙이는 경우가 있습니다(`IUser`, `IProduct`). 이는 Java 관례이며 TypeScript 커뮤니티에서는 권장하지 않습니다. TypeScript 공식 스타일 가이드와 대부분의 오픈소스 프로젝트에서 `User`, `Product`처럼 `I` 없이 사용합니다.

### 3.2 Optional Property (선택적 속성)

모든 속성이 항상 필수는 아닙니다. 속성 이름 뒤에 `?`를 붙이면 해당 속성은 있어도 되고 없어도 됩니다.

```typescript
// 선택적 속성 예시
interface UserProfile {
  name: string;           // 필수
  email: string;          // 필수
  phone?: string;         // 선택적 — 없어도 됩니다
  bio?: string;           // 선택적 — 없어도 됩니다
  avatarUrl?: string;     // 선택적 — 없어도 됩니다
}

// phone, bio, avatarUrl 없이도 유효합니다
const profile1: UserProfile = {
  name: "홍길동",
  email: "hong@example.com",
};

// 선택적 속성이 있는 경우
const profile2: UserProfile = {
  name: "김철수",
  email: "kim@example.com",
  phone: "010-1234-5678",
  bio: "프론트엔드 개발자입니다.",
};

// 선택적 속성을 사용할 때는 undefined 여부를 확인해야 합니다
function formatPhone(profile: UserProfile): string {
  if (profile.phone) {
    // phone이 있을 때만 이 블록이 실행됩니다
    return profile.phone.replace(/-/g, "");
  }
  return "전화번호 없음";
}
```

### 3.3 Type Alias

`type` 키워드는 **타입에 이름을 붙이는** 또 다른 방법입니다. 객체 타입뿐 아니라 어떤 타입에도 이름을 붙일 수 있습니다.

```typescript
// 원시 타입에 별칭 붙이기
type UserID = number;           // number 타입에 UserID라는 이름을 붙입니다
type ProductName = string;      // string 타입에 ProductName이라는 이름을 붙입니다

const userId: UserID = 12345;
const productName: ProductName = "노트북";

// 유니온 타입에 이름 붙이기 (유니온은 섹션 4에서 다룹니다)
type ID = string | number;     // string 또는 number
type Status = "active" | "inactive" | "pending";

// 객체 타입에 이름 붙이기 — interface와 유사합니다
type Point = {
  x: number;
  y: number;
};

const origin: Point = { x: 0, y: 0 };
```

### 3.4 Interface vs Type: 언제 무엇을 쓰는가

이것은 TypeScript 커뮤니티에서 가장 자주 묻는 질문 중 하나입니다. 실무에서는 다음 기준을 따르면 됩니다.

| 상황 | 권장 |
|------|------|
| 객체의 구조를 정의할 때 | `interface` |
| 유니온 타입이 필요할 때 | `type` |
| 타입을 조합하거나 변형할 때 | `type` |
| 라이브러리 공개 API를 작성할 때 | `interface` |
| React 컴포넌트 Props를 정의할 때 | 팀 컨벤션 (둘 다 가능) |

```typescript
// 객체 구조 → interface 사용
interface OrderItem {
  productId: number;
  quantity: number;
  unitPrice: number;
}

// 유니온/조합 → type 사용
type PaymentMethod = "card" | "bank_transfer" | "kakao_pay" | "naver_pay";
type OrderStatus = "pending" | "confirmed" | "shipped" | "delivered" | "cancelled";

// interface와 type을 함께 사용하는 예시
interface Order {
  id: number;
  items: OrderItem[];          // interface를 배열 타입으로 사용
  status: OrderStatus;         // type alias를 사용
  paymentMethod: PaymentMethod; // type alias를 사용
  totalAmount: number;
}
```

> **참고 박스 (심화)**: interface와 type의 기술적 차이
>
> - **Declaration Merging**: `interface`는 같은 이름으로 여러 번 선언하면 자동으로 합쳐집니다. `type`은 중복 선언이 불가합니다.
> - **확장 방법**: `interface`는 `extends` 키워드로 확장하고, `type`은 `&` 연산자로 교차(intersection) 타입을 만듭니다.
> - 실무에서는 이 차이가 문제가 되는 경우가 드뭅니다. 팀 컨벤션을 따르는 것이 가장 중요합니다.

```typescript
// interface extends 예시
interface Animal {
  name: string;
}
interface Dog extends Animal {  // Animal의 모든 속성을 포함하고 추가
  breed: string;
}

// type & 교차 타입 예시
type Animal2 = { name: string };
type Dog2 = Animal2 & { breed: string }; // Animal2와 교차

// 두 방법의 결과는 동일합니다
const myDog1: Dog = { name: "멍이", breed: "진돗개" };
const myDog2: Dog2 = { name: "멍이", breed: "진돗개" };
```

---

## 4. Union & Literal 타입 (5분)

### 강사 설명 포인트

Union 타입은 TypeScript의 가장 강력한 기능 중 하나입니다. 실무 코드에서 매우 자주 사용되므로 충분히 이해해야 합니다.

### 4.1 Union 타입

Union 타입은 "A 또는 B" 타입을 표현합니다. `|` 기호(파이프)로 여러 타입을 연결합니다.

```typescript
// 기본 Union 타입
type StringOrNumber = string | number;

let value: StringOrNumber;
value = "안녕하세요";     // 정상 — string도 가능
value = 42;               // 정상 — number도 가능
value = true;             // 컴파일 오류 — boolean은 허용되지 않습니다

// 함수 매개변수에서의 Union 타입
function formatID(id: string | number): string {
  return `ID: ${id}`;
}

formatID(12345);           // "ID: 12345"
formatID("USR-001");       // "ID: USR-001"
```

### 4.2 Literal 타입

Literal 타입은 특정 **값 자체**를 타입으로 사용합니다. 예를 들어 `"success"`는 단순한 문자열이 아니라 정확히 `"success"` 값만 허용하는 타입입니다.

```typescript
// Literal 타입 예시
type Direction = "north" | "south" | "east" | "west";

let direction: Direction;
direction = "north";       // 정상
direction = "east";        // 정상
direction = "up";          // 컴파일 오류: Type '"up"' is not assignable to type 'Direction'
direction = "North";       // 컴파일 오류: 대소문자 구분 주의!
```

### 4.3 실무 예: API 응답 상태 모델링

Literal Union 타입이 실무에서 가장 많이 쓰이는 곳은 API 응답 상태 모델링입니다.

```typescript
// API 요청 상태를 Literal Union으로 모델링합니다
type RequestStatus = "idle" | "loading" | "success" | "error";

// API 응답 타입
interface ApiResponse<T> {
  status: RequestStatus;    // 정해진 4개의 값만 허용합니다
  data: T | null;           // 성공 시 데이터, 실패 시 null
  errorMessage: string | null; // 오류 시 메시지, 정상 시 null
}

// 실제 사용 예시
interface UserData {
  id: number;
  name: string;
  email: string;
}

const response: ApiResponse<UserData> = {
  status: "success",                 // 4가지 값 중 하나
  data: { id: 1, name: "홍길동", email: "hong@example.com" },
  errorMessage: null,
};

// 잘못된 상태값은 컴파일 시 바로 잡힙니다
const badResponse: ApiResponse<UserData> = {
  status: "completed",               // 컴파일 오류: "completed"는 허용되지 않습니다
  data: null,
  errorMessage: null,
};
```

### 4.4 타입 좁히기 (Type Narrowing)

Union 타입의 변수를 사용할 때, TypeScript는 특정 타입인지 확인한 후에야 해당 타입의 메서드를 사용할 수 있도록 강제합니다. 이를 **타입 좁히기(Type Narrowing)** 라고 합니다.

```typescript
// typeof를 이용한 타입 좁히기
function processValue(value: string | number): string {
  // 이 시점에서 value는 string 또는 number 둘 다 가능합니다

  if (typeof value === "string") {
    // 이 블록 안에서 TypeScript는 value가 string임을 압니다
    return value.toUpperCase();     // string의 메서드 사용 가능
  }

  // 이 시점에서 TypeScript는 value가 number임을 압니다 (string이 아니므로)
  return value.toFixed(2);          // number의 메서드 사용 가능
}

console.log(processValue("hello")); // "HELLO"
console.log(processValue(3.14159)); // "3.14"
```

```typescript
// in 연산자를 이용한 타입 좁히기
interface Cat {
  name: string;
  meow(): void;    // 고양이만 가진 메서드
}

interface Dog {
  name: string;
  bark(): void;    // 개만 가진 메서드
}

function makeSound(animal: Cat | Dog): void {
  if ("meow" in animal) {
    // meow 속성이 있으면 Cat 타입입니다
    animal.meow();
  } else {
    // meow가 없으면 Dog 타입입니다
    animal.bark();
  }
}
```

```typescript
// 실무 예: API 상태에 따른 분기 처리
function handleApiResponse(response: ApiResponse<UserData>): void {
  if (response.status === "loading") {
    console.log("데이터를 불러오는 중입니다...");
    return;
  }

  if (response.status === "error") {
    // status가 "error"이면 errorMessage가 있어야 합니다
    console.error(`오류 발생: ${response.errorMessage}`);
    return;
  }

  if (response.status === "success" && response.data !== null) {
    // status가 "success"이면 data가 있습니다
    console.log(`사용자: ${response.data.name}`);
    return;
  }

  // status가 "idle"이면 아무것도 하지 않습니다
  console.log("대기 중");
}
```

---

## 5. 제네릭 맛보기 (3분)

### 강사 설명 포인트

제네릭(Generic)은 TypeScript의 핵심 기능입니다. 이 섹션에서는 **존재를 인식하는 수준**으로만 다룹니다. React의 `useState`를 사용하면서 자연스럽게 익히게 됩니다.

### 5.1 제네릭이 필요한 이유

```typescript
// 제네릭 없이 타입별로 함수를 각각 만드는 비효율적인 방법
function getFirstNumber(arr: number[]): number {
  return arr[0];
}

function getFirstString(arr: string[]): string {
  return arr[0];
}

// 위 두 함수는 로직이 동일합니다. 타입만 다를 뿐입니다.
// 제네릭으로 하나의 함수로 합칠 수 있습니다.
```

### 5.2 제네릭 문법

꺾쇠괄호 `<T>`는 "타입 매개변수"를 나타냅니다. `T`는 관례적으로 사용하는 이름이며, 아무 이름이나 사용할 수 있습니다.

```typescript
// 제네릭 함수: <T>는 "어떤 타입이든 받겠다"는 선언입니다
function getFirst<T>(arr: T[]): T {
  return arr[0]; // T 타입 배열의 첫 번째 요소를 T 타입으로 반환합니다
}

// 사용할 때 T가 결정됩니다
const firstNum = getFirst([1, 2, 3]);           // T = number로 결정
const firstStr = getFirst(["a", "b", "c"]);     // T = string으로 결정

// TypeScript가 자동으로 T를 추론합니다
// 명시적으로 적을 수도 있습니다
const firstNum2 = getFirst<number>([1, 2, 3]);
const firstStr2 = getFirst<string>(["a", "b", "c"]);
```

### 5.3 React에서의 제네릭: useState

React를 사용할 때 가장 먼저 마주치는 제네릭입니다.

```typescript
// useState<T>: 상태의 타입을 T로 지정합니다
import { useState } from "react";

// 숫자 상태
const [count, setCount] = useState<number>(0);
setCount(1);           // 정상
setCount("hello");     // 컴파일 오류: string은 number에 할당 불가

// 문자열 상태
const [name, setName] = useState<string>("");
setName("홍길동");     // 정상

// interface를 사용하는 상태
interface User {
  id: number;
  name: string;
}

const [user, setUser] = useState<User | null>(null);
// user는 User 타입이거나 null입니다

// 배열 상태 — 자주 사용하는 패턴입니다
const [users, setUsers] = useState<User[]>([]);
// users는 User 배열로 시작합니다
```

이후 React 실습에서 `useState<T>`를 반복적으로 사용하게 됩니다. 꺾쇠괄호 안에 타입을 적는 패턴을 기억해 두십시오.

---

## 6. 함수 타입 (2분 - 참고)

### 강사 설명 포인트

이 섹션은 빠르게 훑고 넘어갑니다. React 컴포넌트를 작성하면서 자연스럽게 익히게 됩니다.

### 6.1 기본 함수 타입

```typescript
// 매개변수 타입과 반환 타입을 명시합니다
function add(a: number, b: number): number {
  return a + b;
}

// 반환값이 없으면 void를 사용합니다
function logMessage(message: string): void {
  console.log(`[LOG] ${message}`);
  // return 값 없음
}

// 화살표 함수도 동일하게 타입을 붙입니다
const multiply = (a: number, b: number): number => a * b;

const printUser = (user: { name: string; age: number }): void => {
  console.log(`${user.name} (${user.age}세)`);
};
```

```typescript
// 함수 타입을 변수에 할당하는 경우
type AddFunction = (a: number, b: number) => number;

const myAdd: AddFunction = (a, b) => a + b;    // 타입 어노테이션 생략 가능 (추론됨)
const myMultiply: AddFunction = (a, b) => a * b; // 동일한 시그니처이므로 호환됩니다
```

### 6.2 React 컴포넌트에서의 함수 타입 예고

```typescript
// React 이벤트 핸들러는 함수 타입이 필요합니다
// (Session 3-4에서 자세히 다룹니다)
interface ButtonProps {
  label: string;
  onClick: () => void;               // 매개변수 없고 반환값 없는 함수
  onHover?: (event: MouseEvent) => void; // 선택적 이벤트 핸들러
}
```

---

## 트러블슈팅 & 자주 하는 실수

### 실수 1: string vs String 혼동

```typescript
// 잘못된 방법 (대문자)
const name: String = "홍길동";      // String은 래퍼 객체 타입입니다

// 올바른 방법 (소문자)
const name2: string = "홍길동";     // string은 원시 타입입니다
```

**해결 방법**: TypeScript에서는 항상 `string`, `number`, `boolean`(소문자)를 사용합니다. 대문자는 JavaScript의 내장 래퍼 객체입니다. VS Code에서 대문자로 쓰면 노란 줄로 경고가 표시됩니다.

### 실수 2: any 남용

```typescript
// 잘못된 방법: 모르겠으니 any로 처리
function handleData(data: any) {
  data.process(); // any이므로 오류가 없지만 런타임에 터집니다
}

// 올바른 방법 1: 정확한 타입 정의
interface DataPayload {
  process: () => void;
}
function handleData2(data: DataPayload) {
  data.process(); // 타입 안전
}

// 올바른 방법 2: 타입을 모를 때는 unknown 사용
function handleData3(data: unknown) {
  if (typeof data === "object" && data !== null && "process" in data) {
    (data as { process: () => void }).process();
  }
}
```

**해결 방법**: `any`를 쓰고 싶을 때 잠시 멈추고 실제 타입이 무엇인지 생각해보십시오. 타입을 정확히 모른다면 `unknown`을 사용하고 타입 좁히기를 적용하십시오.

### 실수 3: Interface 이름에 I 접두어 붙이기

```typescript
// Java 스타일 (TypeScript에서는 비권장)
interface IUser { name: string; }       // I 접두어는 TypeScript 스타일이 아닙니다
interface IProductService { ... }

// TypeScript 스타일 (권장)
interface User { name: string; }         // 그냥 User
interface ProductService { ... }         // 그냥 ProductService
```

**해결 방법**: TypeScript 공식 스타일 가이드와 대부분의 TypeScript 기반 프로젝트(React, Angular, NestJS 등)는 `I` 접두어를 사용하지 않습니다. 코드 리뷰에서 지적 받기 전에 습관을 바꾸십시오.

### 실수 4: 빈 배열 초기화 시 타입 명시 누락

```typescript
// 잘못된 방법: 빈 배열은 any[]로 추론됩니다
const items = [];                        // any[]로 추론됩니다
items.push("hello");                     // 정상
items.push(42);                          // 정상 — 의도하지 않은 혼합

// 올바른 방법: 타입을 명시합니다
const items2: string[] = [];             // string 배열
items2.push("hello");                    // 정상
items2.push(42);                         // 컴파일 오류: number는 string에 할당 불가
```

### 실수 5: Optional Property를 undefined 확인 없이 사용

```typescript
interface Config {
  timeout?: number;    // 선택적 속성
  retries?: number;    // 선택적 속성
}

function runRequest(config: Config): void {
  // 잘못된 방법: undefined일 수 있는 속성을 바로 사용
  const delay = config.timeout * 1000;  // 컴파일 오류 또는 NaN

  // 올바른 방법: 기본값과 함께 사용하거나 확인 후 사용
  const delay2 = (config.timeout ?? 5000) * 1000;  // ?? 는 nullish coalescing
  const delay3 = config.timeout ? config.timeout * 1000 : 5000;
}
```

---

## Q&A 예상 질문과 답변

### Q1. TypeScript로 작성한 코드는 브라우저에서 직접 실행되나요?

아닙니다. TypeScript 코드는 반드시 JavaScript로 컴파일된 후에 브라우저나 Node.js에서 실행됩니다. TypeScript 컴파일러(`tsc`)가 이 변환을 담당합니다. React 프로젝트에서는 Vite나 Next.js 같은 빌드 도구가 자동으로 컴파일을 처리하므로 직접 `tsc`를 실행할 필요는 없습니다. 개발자는 TypeScript 코드만 작성하면 됩니다.

### Q2. 기존 JavaScript 프로젝트를 TypeScript로 마이그레이션하는 것이 어렵나요?

TypeScript는 JavaScript의 슈퍼셋이므로 `.js` 파일을 `.ts`로 바꾸고 `tsconfig.json`을 추가하는 것만으로 시작할 수 있습니다. `noImplicitAny: false`(기본값)로 설정하면 기존 코드에 오류가 거의 없습니다. 이후 점진적으로 타입을 추가해나가는 방식이 실무에서 일반적입니다. 전환을 강제로 한 번에 하려 하면 오히려 어렵습니다.

### Q3. `null`과 `undefined`는 어떻게 다루나요?

JavaScript에는 두 가지 "없음" 값이 있습니다. TypeScript의 `strictNullChecks` 옵션(기본적으로 활성화)을 사용하면 `null`과 `undefined`를 명시적으로 처리해야 합니다.

```typescript
// strictNullChecks 활성화 시
let name: string = "홍길동";
name = null;        // 컴파일 오류: null은 string에 할당 불가

// null을 허용하려면 Union 타입으로 명시합니다
let name2: string | null = "홍길동";
name2 = null;       // 정상

// undefined를 허용하려면
let name3: string | undefined;
// name3은 초기값 없이 선언 — undefined 상태
name3 = "홍길동";   // 나중에 할당 가능
```

### Q4. Java의 `enum`과 TypeScript의 `enum`은 같은가요?

비슷하지만 TypeScript의 `enum`은 JavaScript로 컴파일될 때 복잡한 코드를 생성합니다. 많은 TypeScript 전문가들이 `enum` 대신 **Literal Union 타입** 또는 **const object**를 권장합니다.

```typescript
// TypeScript enum (사용 가능하지만 권장하지 않음)
enum OrderStatus {
  Pending = "PENDING",
  Confirmed = "CONFIRMED",
  Delivered = "DELIVERED",
}

// 권장하는 방법 1: Literal Union 타입
type OrderStatusType = "PENDING" | "CONFIRMED" | "DELIVERED";

// 권장하는 방법 2: const object (enum의 장점을 살리면서 안전함)
const OrderStatus2 = {
  Pending: "PENDING",
  Confirmed: "CONFIRMED",
  Delivered: "DELIVERED",
} as const;
type OrderStatusType2 = typeof OrderStatus2[keyof typeof OrderStatus2];
```

### Q5. `interface`와 `type`이 기능적으로 거의 동일하다면 어떤 걸 선택해야 하나요?

팀 컨벤션이 없다면 다음 규칙을 따르십시오. 객체의 구조를 정의할 때는 `interface`, 유니온/교차/기타 복합 타입을 표현할 때는 `type`을 사용합니다. React 커뮤니티에서는 컴포넌트 Props에 `interface`를 사용하는 경향이 강합니다. 중요한 것은 팀 내 일관성입니다.

### Q6. 타입 추론이 있는데 왜 굳이 타입을 명시해야 하나요?

두 가지 이유가 있습니다. 첫째, **문서화 효과**입니다. 함수 시그니처에 타입을 명시하면 함수가 무엇을 받고 무엇을 반환하는지 코드를 읽는 사람이 즉시 알 수 있습니다. 둘째, **의도 강제**입니다. 초기값 없이 변수를 선언하거나 `[]`처럼 빈 컬렉션을 초기화할 때는 추론이 불가능하므로 명시해야 합니다.

### Q7. `unknown`과 `any`의 차이가 무엇인가요?

`any`는 타입 검사를 **완전히 비활성화**합니다. `unknown`은 "타입을 모른다"고 선언하지만 **사용 전에 반드시 타입을 확인**하도록 강제합니다. `unknown`이 훨씬 안전합니다. 예를 들어 외부 API 응답처럼 실제로 타입을 모르는 경우 `unknown`을 사용하고, `typeof`나 `instanceof`로 좁혀서 사용합니다.

### Q8. Python의 타입 힌트와 TypeScript의 타입 시스템은 어떻게 다른가요?

Python의 타입 힌트(Type Hints)는 **선택적**이고 런타임에는 완전히 무시됩니다. `mypy` 같은 별도 도구로 정적 분석을 해야 합니다. TypeScript는 **컴파일 단계에서 타입 오류를 강제로 차단**합니다. 타입이 맞지 않으면 빌드 자체가 실패합니다. TypeScript가 훨씬 강한 타입 보장을 제공합니다.

### Q9. 제네릭 `<T>`에서 `T` 말고 다른 이름을 써도 되나요?

네. `T`는 관례일 뿐 어떤 이름이든 사용할 수 있습니다. 다만 업계 관례가 있습니다.

```typescript
// 관례적인 제네릭 이름
// T: 일반 타입 (Type)
// K: 키 타입 (Key)
// V: 값 타입 (Value)
// E: 요소 타입 (Element)
// R: 반환 타입 (Return)

// 더 명확한 이름을 쓰면 가독성이 좋아집니다
function mapArray<InputType, OutputType>(
  arr: InputType[],
  transform: (item: InputType) => OutputType
): OutputType[] {
  return arr.map(transform);
}
```

### Q10. TypeScript에서 클래스(class)는 어떻게 사용하나요?

TypeScript는 ES6 클래스에 타입 어노테이션을 추가합니다. Java/C# 개발자에게 친숙한 `public`, `private`, `protected`, `readonly` 접근 제어자도 지원합니다.

```typescript
class UserService {
  private users: User[] = [];       // 외부에서 접근 불가
  readonly maxUsers: number = 100;  // 읽기 전용

  addUser(user: User): void {
    if (this.users.length >= this.maxUsers) {
      throw new Error("최대 사용자 수를 초과했습니다.");
    }
    this.users.push(user);
  }

  getUserById(id: number): User | undefined {
    return this.users.find((user) => user.id === id);
  }
}
```

다만 React 개발에서는 클래스형 컴포넌트보다 **함수형 컴포넌트와 Hooks**를 사용하는 것이 현재 표준입니다. 클래스는 Session에서 다루지 않습니다.

### Q11. TypeScript의 `as` 키워드는 무엇인가요?

`as`는 **타입 단언(Type Assertion)** 입니다. "나는 이 값이 이 타입임을 확신한다"고 컴파일러에게 알리는 방법입니다. 남용하면 `any`와 마찬가지로 타입 안전성을 해칩니다.

```typescript
// 타입 단언 예시
const input = document.getElementById("username") as HTMLInputElement;
// getElementById의 반환 타입은 HTMLElement | null 입니다
// 실제로 input[type="text"]임을 알고 있으므로 HTMLInputElement로 단언합니다

console.log(input.value); // HTMLInputElement의 value 속성에 접근 가능

// 주의: 틀린 단언은 런타임 오류를 만듭니다
const num = "hello" as unknown as number;  // 강제 단언 — 매우 위험합니다
```

### Q12. `readonly`는 언제 사용하나요?

속성이나 배열이 변경되어서는 안 될 때 사용합니다. React의 상태 불변성 원칙과 잘 맞습니다.

```typescript
interface Config {
  readonly apiUrl: string;     // 한 번 설정 후 변경 불가
  readonly version: string;
  timeout: number;             // 변경 가능
}

const config: Config = {
  apiUrl: "https://api.example.com",
  version: "1.0.0",
  timeout: 5000,
};

config.timeout = 10000;       // 정상
config.apiUrl = "다른 URL";  // 컴파일 오류: Cannot assign to 'apiUrl' because it is a read-only property.
```

---

## 핵심 요약

이 세션에서 다룬 내용을 정리합니다.

### TypeScript가 필요한 이유

- JavaScript의 동적 타입은 대규모 프로젝트에서 런타임 오류를 유발합니다.
- TypeScript는 컴파일 단계에서 타입 오류를 감지하여 프로덕션 버그를 줄입니다.
- TypeScript 코드는 최종적으로 JavaScript로 컴파일됩니다.

### 기본 타입 핵심

| 타입 | 올바른 사용 | 잘못된 사용 |
|------|------------|------------|
| 문자열 | `string` | `String` |
| 숫자 | `number` | `Number` |
| 불리언 | `boolean` | `Boolean` |
| 배열 | `number[]` 또는 `Array<number>` | — |
| 없음(피할 것) | `unknown` | `any` |

### Interface vs Type

```typescript
// 객체 구조 → interface
interface User { name: string; age: number; }

// 유니온/조합 → type
type Status = "active" | "inactive";
type ID = string | number;
```

### Union & Literal 타입

```typescript
// API 상태 모델링 패턴 — 실무에서 매우 자주 사용합니다
type RequestStatus = "idle" | "loading" | "success" | "error";
```

### 타입 좁히기

```typescript
// typeof로 원시 타입을 구분합니다
if (typeof value === "string") { /* string 처리 */ }

// in 연산자로 속성 존재를 확인합니다
if ("meow" in animal) { /* Cat 처리 */ }
```

### 제네릭 기본 형태

```typescript
// useState<T>: T가 상태의 타입입니다
const [users, setUsers] = useState<User[]>([]);
```

---

## 다음 세션 예고

Session 2에서는 이 세션에서 배운 TypeScript 기초를 직접 코드로 작성해보는 실습을 진행합니다. 타입 정의를 잘못 작성하면 IDE가 즉시 오류를 표시하는 경험을 통해 TypeScript의 장점을 체감하게 됩니다.

---

## 강사 참고: 시간 배분

| 섹션 | 권장 시간 | 핵심 강조 포인트 |
|------|----------|----------------|
| 1. 왜 TypeScript인가 | 5분 | JS 런타임 오류 → TS 컴파일 타임 감지 |
| 2. 기본 타입 | 8분 | 소문자 타입, any 금지, 타입 추론 |
| 3. Interface와 Type | 7분 | interface는 객체 구조, type은 유니온/조합 |
| 4. Union & Literal | 5분 | API 상태 모델링, 타입 좁히기 |
| 5. 제네릭 맛보기 | 3분 | useState<T> 패턴 인식 |
| 6. 함수 타입 | 2분 | 매개변수·반환 타입 기본 |
| **합계** | **30분** | |

수강생 질문이 많을 경우 섹션 5와 6은 빠르게 코드만 보여주고 넘어가도 됩니다. 제네릭과 함수 타입은 이후 React 실습에서 자연스럽게 익히게 됩니다.
