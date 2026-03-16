# Session 2: TypeScript 실습

**시간**: 30분 | **유형**: 독립 실습
**사이트**: https://typescript-exercises.github.io

---

## 학습 목표

- Session 1에서 배운 기본 타입 개념(string, number, interface 등)을 실제 코드에 적용합니다.
- TypeScript 컴파일러가 출력하는 타입 오류 메시지를 읽고 해결하는 연습을 합니다.
- Union 타입과 타입 가드(Type Guard) 개념을 실습을 통해 체득합니다.

---

## 실습 안내

### 사이트 접속 방법

1. 브라우저에서 https://typescript-exercises.github.io 에 접속합니다.
2. 상단 메뉴에서 **Exercise 1**부터 순서대로 진행합니다.
3. 각 문제는 왼쪽 편집기에 시작 코드가 제공됩니다. 오른쪽에는 컴파일 결과와 오류 메시지가 표시됩니다.
4. 코드를 수정하면 실시간으로 TypeScript 컴파일러가 오류를 확인해 줍니다. 오류가 없으면 초록색 체크가 표시됩니다.

### 실습 진행 방식

- 강사가 각 문제를 소개한 뒤, 학생 여러분이 직접 코드를 작성합니다.
- 막히는 경우 이 가이드의 **힌트** 섹션을 참고합니다. 힌트를 봐도 해결되지 않으면 **풀이** 섹션으로 넘어갑니다.
- 시간 안에 풀지 못한 문제는 풀이를 확인하고 다음 문제로 진행합니다.

### 사이트 접속이 안 될 경우

사이트가 JavaScript로 렌더링되어 접속이 어려울 수 있습니다. 이 경우 이 가이드에 수록된 시작 코드를 복사하여 로컬 파일(`exercise1.ts` 등)로 저장한 뒤, Session 0에서 설치한 `tsx` 도구로 실행하면 됩니다.

```bash
tsx exercise1.ts
```

타입 오류만 확인하고 싶으면 TypeScript Playground(https://www.typescriptlang.org/play)를 사용할 수도 있습니다. 모든 문제와 풀이가 이 가이드에 포함되어 있으므로 사이트 없이도 수업 진행이 가능합니다.

---

## Exercise 1: 기본 타입 선언 (5분)

### 문제 설명

사용자 목록을 관리하는 간단한 프로그램입니다. `User` 타입이 `unknown`으로 되어 있고, `users` 배열과 `logPerson` 함수의 타입도 `unknown`으로 선언되어 있습니다. 실제 데이터를 보면 사용자는 `name`(이름), `age`(나이), `occupation`(직업) 세 가지 정보를 가집니다. `User` 타입을 올바르게 정의하고, `users`와 `logPerson`의 타입을 `unknown`에서 `User`로 교체하여 오류를 해결하십시오.

### 시작 코드

```typescript
export type User = unknown;

export const users: unknown[] = [
    { name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' },
    { name: 'Kate Müller', age: 23, occupation: 'Astronaut' }
];

export function logPerson(user: unknown) {
    console.log(` - ${user.name}, ${user.age}`);
}

console.log('Users:');
users.forEach(logPerson);
```

### 컴파일러 오류 메시지 (풀기 전 상태)

시작 코드를 그대로 두면 TypeScript 컴파일러는 다음과 같은 오류를 출력합니다.

```
Property 'name' does not exist on type 'unknown'.
Property 'age' does not exist on type 'unknown'.
```

이 오류는 `logPerson` 함수의 매개변수 타입이 `unknown`이어서 발생합니다. TypeScript는 `unknown` 타입에서는 어떤 속성도 안전하게 접근할 수 없다고 판단합니다. `user.name`이나 `user.age`에 접근하려면 TypeScript가 해당 타입에 그 속성이 있음을 알아야 합니다.

### 핵심 개념

이 문제는 TypeScript의 **타입 별칭(type alias)** 과 **기본 타입(primitive types)** 을 테스트합니다.

- `type` 키워드로 객체 타입의 모양(shape)을 정의합니다.
- 각 필드에 `: string`, `: number` 처럼 타입을 명시합니다.
- `unknown`은 TypeScript에서 가장 안전한 "모름" 타입입니다. 어떤 값이든 담을 수 있지만, 타입을 좁히기 전까지는 아무 속성에도 접근할 수 없습니다.
- TypeScript는 정의된 타입과 실제 값이 일치하는지 컴파일 시점에 검사합니다.

### 힌트

**힌트 1**: `User` 타입 내부에 세 가지 필드가 필요합니다. 실제 데이터 객체의 키 `name`, `age`, `occupation` 을 모두 추가하십시오.

**힌트 2**: `name`과 `occupation` 필드에는 `string`을, `age` 필드에는 `number`를 사용합니다.

**힌트 3**: `User` 타입을 완성한 뒤, `users: unknown[]`을 `users: User[]`로, `logPerson(user: unknown)`을 `logPerson(user: User)`로 교체하십시오.

**힌트 4**: 타입 정의 구문은 다음과 같은 형태입니다.
```typescript
type MyType = {
    fieldName: fieldType;
};
```

### 풀이

```typescript
export type User = {
    name: string;
    age: number;
    occupation: string;
};

export const users: User[] = [
    { name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' },
    { name: 'Kate Müller', age: 23, occupation: 'Astronaut' }
];

export function logPerson(user: User) {
    console.log(` - ${user.name}, ${user.age}`);
}

console.log('Users:');
users.forEach(logPerson);
```

### 풀이 상세 설명

**1단계: 타입 정의 완성**

```typescript
export type User = {
    name: string;       // 이름: 문자열
    age: number;        // 나이: 숫자
    occupation: string; // 직업: 문자열
};
```

`type` 키워드 뒤에 타입 이름(`User`)을 쓰고, 중괄호 안에 각 필드와 타입을 선언합니다. 세미콜론(`;`)으로 각 줄을 구분합니다. 쉼표(`,`)를 써도 동작하지만, 타입 정의에서는 세미콜론이 관례적으로 더 많이 쓰입니다.

실제 데이터 `{ name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' }` 를 보면 필드가 세 개(`name`, `age`, `occupation`)입니다. 처음에 `name`과 `age`만 정의하면 `occupation` 필드 때문에 오류가 발생하므로 주의하십시오.

**2단계: `unknown`에서 `User`로 교체**

```typescript
// 변경 전
export const users: unknown[] = [ ... ];
export function logPerson(user: unknown) { ... }

// 변경 후
export const users: User[] = [ ... ];
export function logPerson(user: User) { ... }
```

`User` 타입을 올바르게 정의했다면, `unknown` 자리를 `User`로 바꾸기만 하면 됩니다. TypeScript는 이제 `user.name`, `user.age`, `user.occupation` 이 존재함을 알고 오류를 내지 않습니다.

**3단계: `type` vs `interface`**

이 문제에서는 `type` 키워드를 사용했지만, `interface`로도 동일하게 정의할 수 있습니다.

```typescript
// interface 버전 — 동일한 결과
interface User {
    name: string;
    age: number;
    occupation: string;
}
```

두 방식 모두 유효합니다. `type`은 Union, Intersection 등 더 복잡한 타입 조합에 사용할 수 있고, `interface`는 상속(`extends`)에 더 직관적입니다.

### 이해 확인

이 문제에서 배운 것을 정리합니다.

- **타입 별칭**: `type User = { ... }` 구문으로 객체의 모양을 정의할 수 있습니다.
- **기본 타입**: `string`은 텍스트, `number`는 숫자를 나타냅니다.
- **`unknown` 타입의 한계**: `unknown` 타입에서는 어떤 속성도 접근할 수 없습니다. 반드시 구체적인 타입을 선언해야 속성에 접근할 수 있습니다.
- **타입 오류 읽기**: 오류 메시지에 어떤 속성이 없는지 명확히 나옵니다. 메시지를 읽으면 무엇을 추가해야 하는지 알 수 있습니다.
- **타입 안전성**: TypeScript는 컴파일 시점에 타입 불일치를 잡아줍니다. 런타임에 `undefined` 오류가 발생하기 전에 미리 알 수 있습니다.

---

## Exercise 2: Union 타입 정의 (5분)

### 문제 설명

이제 사용자(`User`)와 관리자(`Admin`) 두 가지 역할이 생겼습니다. `User`와 `Admin` 인터페이스는 이미 정의되어 있습니다. `User`는 `name`, `age`, `occupation` 필드를, `Admin`은 `name`, `age`, `role` 필드를 가집니다. 여러분이 해야 할 일은 세 가지입니다.

1. `Person` 타입을 `unknown` 대신 `User | Admin`으로 정의합니다.
2. `persons` 배열의 타입을 `User[]`에서 `Person[]`으로 변경합니다.
3. `logPerson` 함수의 매개변수 타입을 `User`에서 `Person`으로 변경합니다.

### 시작 코드

```typescript
interface User {
    name: string;
    age: number;
    occupation: string;
}

interface Admin {
    name: string;
    age: number;
    role: string;
}

export type Person = unknown;

export const persons: User[] /* <- Person[] */ = [
    { name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' },
    { name: 'Jane Doe', age: 32, role: 'Administrator' },
    { name: 'Kate Müller', age: 23, occupation: 'Astronaut' },
    { name: 'Bruce Willis', age: 64, role: 'World saver' }
];

export function logPerson(user: User) {
    console.log(` - ${user.name}, ${user.age}`);
}

persons.forEach(logPerson);
```

### 컴파일러 오류 메시지 (풀기 전 상태)

```
Type '{ name: string; age: number; role: string; }' is not assignable to type 'User'.
  Object literal may only specify known properties, and 'role' does not exist in type 'User'.

Argument of type 'Person' is not assignable to parameter of type 'User'.
  Type 'unknown' is not assignable to type 'User'.
```

`persons` 배열이 `User[]`로 선언되어 있는데 `role` 필드를 가진 `Admin` 객체가 들어가 있어서 첫 번째 오류가 발생합니다. `Person`이 `unknown`이라 `logPerson(user: User)`에 전달할 수 없어서 두 번째 오류가 발생합니다.

### 핵심 개념

이 문제는 TypeScript의 **Union 타입(`|`)** 을 테스트합니다.

- Union 타입은 `A | B` 형태로 "A 또는 B" 를 의미합니다.
- Union 타입의 공통 속성에는 타입 좁히기(narrowing) 없이 접근할 수 있습니다.
- `User`와 `Admin` 모두 `name`과 `age`를 가지므로, `Person` 타입으로 두 속성에 접근 가능합니다.
- 배열 타입 `Person[]`은 `User`든 `Admin`이든 모두 담을 수 있습니다.

### 힌트

**힌트 1**: `Person` 타입을 `unknown` 대신 `User | Admin` 으로 변경하십시오. `|` 연산자는 "또는(or)"을 의미합니다.

**힌트 2**: `persons: User[]` 주석(`/* <- Person[] */`)이 힌트입니다. `User[]`를 `Person[]`으로 바꾸십시오.

**힌트 3**: `logPerson(user: User)`의 매개변수 타입을 `Person`으로 바꾸십시오. `User`와 `Admin` 모두 `name`과 `age`를 가지므로 함수 내부 코드는 그대로 동작합니다.

### 풀이

```typescript
interface User {
    name: string;
    age: number;
    occupation: string;
}

interface Admin {
    name: string;
    age: number;
    role: string;
}

// unknown 대신 User | Admin으로 정의합니다
export type Person = User | Admin;

// User[] 대신 Person[]으로 변경합니다
export const persons: Person[] = [
    { name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' },
    { name: 'Jane Doe', age: 32, role: 'Administrator' },
    { name: 'Kate Müller', age: 23, occupation: 'Astronaut' },
    { name: 'Bruce Willis', age: 64, role: 'World saver' }
];

// User 대신 Person으로 변경합니다
export function logPerson(user: Person) {
    console.log(` - ${user.name}, ${user.age}`);
}

persons.forEach(logPerson);
```

### 풀이 상세 설명

**1단계: Union 타입 정의**

```typescript
export type Person = User | Admin;
```

`User | Admin` 은 "User이거나 Admin이다"를 의미합니다. 이 타입의 변수는 두 타입 중 하나의 값을 가질 수 있습니다.

**2단계: 배열 타입 변경**

```typescript
export const persons: Person[] = [ ... ];
```

`Person[]`은 `User` 객체와 `Admin` 객체를 모두 담을 수 있는 배열입니다. 원래 `User[]`로 선언되어 있었기 때문에 `role` 필드를 가진 `Admin` 객체를 넣으려 하면 오류가 발생했습니다.

**3단계: 공통 속성 접근**

```typescript
export function logPerson(user: Person) {
    console.log(` - ${user.name}, ${user.age}`);
    // user.role 에 접근하면 오류 발생 — Admin에만 있는 속성이기 때문
    // user.occupation 에 접근해도 오류 발생 — User에만 있는 속성이기 때문
}
```

`Person`은 `User | Admin` 이므로, TypeScript는 `user`가 `User`일 수도 있고 `Admin`일 수도 있다고 인식합니다. `name`과 `age`는 두 타입 모두에 존재하므로 안전하게 접근할 수 있습니다. 반면 `role`(Admin만)이나 `occupation`(User만)은 타입 좁히기 없이 접근하면 컴파일 오류가 발생합니다.

**`type` vs `interface` 차이점 복습**

```typescript
// interface: 선언 병합(declaration merging) 가능
interface User { name: string; }
interface User { age: number; } // 기존 User에 자동으로 병합됩니다

// type: 선언 병합 불가, Union/Intersection 등 고급 타입 조합 가능
type Person = User | Admin; // interface로는 이런 형태 정의 불가
```

### 이해 확인

이 문제에서 배운 것을 정리합니다.

- **Union 타입**: `A | B` 로 "A 또는 B" 타입을 만듭니다. 두 타입 모두 가진 공통 속성에만 타입 좁히기 없이 접근할 수 있습니다.
- **배열 타입**: `Person[]`은 `Person` 타입 원소들의 배열입니다. Union 타입 배열은 여러 타입의 객체를 함께 담을 수 있습니다.
- **`unknown` vs 구체적인 타입**: `unknown` 은 어떤 속성에도 접근할 수 없습니다. 실제 타입을 명시해야 속성에 접근할 수 있습니다.
- **함수 매개변수 타입 확장**: `logPerson(user: User)`에서 `logPerson(user: Person)`으로 바꾸면 더 많은 타입을 받을 수 있습니다.

---

## Exercise 3: `in` 연산자로 타입 좁히기 (7분)

### 문제 설명

`User`와 `Admin`이 `Person` Union 타입으로 합쳐졌습니다. `logPerson` 함수가 각 사람을 출력할 때, `Admin`이면 `role`을, `User`이면 `occupation`을 함께 출력해야 합니다. 그런데 시작 코드에서 `person.role`과 `person.occupation`에 직접 접근하면 타입 오류가 발생합니다. `in` 연산자를 사용하여 런타임에 어떤 타입인지 판별하고 오류를 해결하십시오.

### 시작 코드

```typescript
interface User {
    name: string;
    age: number;
    occupation: string;
}

interface Admin {
    name: string;
    age: number;
    role: string;
}

export type Person = User | Admin;

export const persons: Person[] = [
    { name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' },
    { name: 'Jane Doe', age: 32, role: 'Administrator' },
    { name: 'Kate Müller', age: 23, occupation: 'Astronaut' },
    { name: 'Bruce Willis', age: 64, role: 'World saver' }
];

export function logPerson(person: Person) {
    let additionalInformation: string;
    if (person.role) {
        additionalInformation = person.role;
    } else {
        additionalInformation = person.occupation;
    }
    console.log(` - ${person.name}, ${person.age}, ${additionalInformation}`);
}

persons.forEach(logPerson);
```

### 컴파일러 오류 메시지 (풀기 전 상태)

```
Property 'role' does not exist on type 'Person'.
  Property 'role' does not exist on type 'User'.

Property 'occupation' does not exist on type 'Person'.
  Property 'occupation' does not exist on type 'Admin'.
```

`person.role`에 접근하면 TypeScript는 "Person 타입에는 role이 없을 수도 있다"고 오류를 냅니다. `Person = User | Admin`인데, `User`에는 `role`이 없기 때문입니다. 마찬가지로 `person.occupation`도 `Admin`에는 없습니다.

### 핵심 개념

이 문제는 TypeScript의 **`in` 연산자를 이용한 타입 좁히기(narrowing)** 를 테스트합니다.

- `'prop' in obj` 형태로 객체에 특정 속성이 존재하는지 런타임에 확인합니다.
- TypeScript는 `if ('role' in person)` 조건이 참인 블록 안에서 `person`이 `Admin` 타입임을 자동으로 파악합니다.
- 이것을 **타입 좁히기(type narrowing)** 라고 합니다. 넓은 Union 타입을 좁혀서 특정 타입의 속성에 안전하게 접근하는 기법입니다.
- `if (person.role)` 처럼 속성을 직접 접근하는 방식은 TypeScript가 Union 타입에서 허용하지 않습니다. 먼저 `in`으로 존재 여부를 확인해야 합니다.

### 힌트

**힌트 1**: `if (person.role)` 을 `if ('role' in person)` 으로 바꾸십시오. 따옴표 안에 속성 이름을 문자열로 넣어야 합니다.

**힌트 2**: `if ('role' in person)` 조건이 참인 블록 안에서 TypeScript는 `person`을 `Admin`으로 좁혀 줍니다. 그 블록 안에서 `person.role`에 안전하게 접근할 수 있습니다.

**힌트 3**: `else` 블록 안에서 TypeScript는 `person`이 `User`임을 압니다(`Admin`이 아니라면 `User`이기 때문). 따라서 `person.occupation`에 안전하게 접근할 수 있습니다.

### 풀이

```typescript
interface User {
    name: string;
    age: number;
    occupation: string;
}

interface Admin {
    name: string;
    age: number;
    role: string;
}

export type Person = User | Admin;

export const persons: Person[] = [
    { name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' },
    { name: 'Jane Doe', age: 32, role: 'Administrator' },
    { name: 'Kate Müller', age: 23, occupation: 'Astronaut' },
    { name: 'Bruce Willis', age: 64, role: 'World saver' }
];

export function logPerson(person: Person) {
    let additionalInformation: string;
    if ('role' in person) {
        // 이 블록 안에서 TypeScript는 person이 Admin임을 압니다
        additionalInformation = person.role;
    } else {
        // 이 블록 안에서 TypeScript는 person이 User임을 압니다
        additionalInformation = person.occupation;
    }
    console.log(` - ${person.name}, ${person.age}, ${additionalInformation}`);
}

persons.forEach(logPerson);
```

### 풀이 상세 설명

**1단계: `in` 연산자의 동작 원리**

```typescript
const person: Person = { name: 'Jane', age: 32, role: 'Administrator' };

console.log('role' in person);       // true  — Admin 객체에는 role이 있습니다
console.log('occupation' in person); // false — Admin 객체에는 occupation이 없습니다
```

JavaScript의 `in` 연산자는 객체에 특정 속성의 키가 존재하는지 런타임에 확인합니다. `'role' in person`이 `true`이면 해당 객체는 `Admin`입니다(`Admin`에만 `role`이 있기 때문).

**2단계: TypeScript가 `in`으로 타입을 좁히는 방식**

```typescript
if ('role' in person) {
    // TypeScript: "person에 role이 있다면 Admin이다"
    // person의 타입이 Admin으로 좁혀집니다
    person.role;        // 정상: Admin에 role이 있습니다
    person.occupation;  // 오류: Admin에 occupation이 없습니다
} else {
    // TypeScript: "person에 role이 없다면 User이다"
    // person의 타입이 User로 좁혀집니다
    person.occupation;  // 정상: User에 occupation이 있습니다
    person.role;        // 오류: User에 role이 없습니다
}
```

TypeScript는 `if ('role' in person)` 조건을 보고 각 분기에서 `person`의 타입을 추론합니다. 이것이 타입 좁히기(narrowing)입니다.

**3단계: 왜 `if (person.role)`이 안 되는가**

```typescript
// 잘못된 방법: TypeScript 오류 발생
if (person.role) {  // 오류: Property 'role' does not exist on type 'Person'
    // ...
}

// 올바른 방법: in 연산자 사용
if ('role' in person) {  // 정상
    // ...
}
```

`person.role`은 속성에 직접 접근하는 것이므로, TypeScript가 먼저 `person` 타입에 `role`이 있는지 확인합니다. `Person = User | Admin`에서 `User`에는 `role`이 없기 때문에 오류가 발생합니다. `in` 연산자는 속성에 접근하지 않고 존재 여부만 확인하므로 오류가 없습니다.

### 이해 확인

이 문제에서 배운 것을 정리합니다.

- **`in` 연산자**: `'prop' in obj` 로 객체에 특정 속성이 있는지 런타임에 확인합니다. Union 타입에서 각 타입을 구별하는 속성으로 타입을 좁힐 수 있습니다.
- **타입 좁히기(narrowing)**: 넓은 타입(Union)에서 조건 검사를 통해 구체적인 타입을 확정하는 기법입니다. `if/else` 분기 안에서 TypeScript가 자동으로 타입을 좁혀 줍니다.
- **속성 접근 vs 존재 확인**: `person.role` 은 속성에 직접 접근(타입 오류 가능)이고, `'role' in person` 은 존재 여부만 확인(타입 오류 없음)입니다.
- **`else` 블록의 자동 추론**: `if ('role' in person)`의 `else`에서 TypeScript는 자동으로 나머지 가능성(`User`)만 남긴다는 것을 압니다.

---

## Exercise 4: 타입 서술어(Type Predicate) (8분)

### 문제 설명

이번에는 `type` 필드로 `User`와 `Admin`을 구분할 수 있습니다. `isAdmin` 함수와 `isUser` 함수가 이미 있지만, 단순히 `boolean`을 반환하는 일반 함수입니다. 그래서 `if (isAdmin(person))` 블록 안에서도 TypeScript가 `person`을 `Admin`으로 좁혀 주지 않아 `person.role` 접근이 오류가 됩니다. `isAdmin`과 `isUser`의 반환 타입에 **타입 서술어(type predicate)** 를 추가하여 오류를 해결하십시오.

### 시작 코드

```typescript
interface User {
    type: 'user';
    name: string;
    age: number;
    occupation: string;
}

interface Admin {
    type: 'admin';
    name: string;
    age: number;
    role: string;
}

export type Person = User | Admin;

export const persons: Person[] = [
    { type: 'user', name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' },
    { type: 'admin', name: 'Jane Doe', age: 32, role: 'Administrator' },
    { type: 'user', name: 'Kate Müller', age: 23, occupation: 'Astronaut' },
    { type: 'admin', name: 'Bruce Willis', age: 64, role: 'World saver' }
];

export function isAdmin(person: Person) {
    return person.type === 'admin';
}

export function isUser(person: Person) {
    return person.type === 'user';
}

export function logPerson(person: Person) {
    let additionalInformation: string = '';
    if (isAdmin(person)) {
        additionalInformation = person.role;        // ERROR
    }
    if (isUser(person)) {
        additionalInformation = person.occupation;  // ERROR
    }
    console.log(` - ${person.name}, ${person.age}, ${additionalInformation}`);
}

console.log('Admins:');
persons.filter(isAdmin).forEach(logPerson);
console.log();
console.log('Users:');
persons.filter(isUser).forEach(logPerson);
```

### 컴파일러 오류 메시지 (풀기 전 상태)

```
Property 'role' does not exist on type 'Person'.
  Property 'role' does not exist on type 'User'.

Property 'occupation' does not exist on type 'Person'.
  Property 'occupation' does not exist on type 'Admin'.
```

`isAdmin(person)`이 `true`를 반환해도, TypeScript는 `person`이 `Admin`임을 모릅니다. 반환 타입이 `boolean`일 뿐이기 때문입니다. `person.role`에 접근하면 `Person` 타입에 `role`이 없다고 오류를 냅니다.

### 핵심 개념

이 문제는 TypeScript의 **타입 서술어(Type Predicate)** 를 테스트합니다.

- 함수의 반환 타입을 `boolean` 대신 `paramName is Type` 형태로 선언하면, 그 함수가 `true`를 반환할 때 TypeScript가 매개변수의 타입을 좁혀 줍니다.
- 예: `function isAdmin(person: Person): person is Admin` — 이 함수가 `true`를 반환하면 `person`이 `Admin`임을 보장합니다.
- 이것이 **사용자 정의 타입 가드(User-Defined Type Guard)** 입니다.
- `persons.filter(isAdmin)`의 결과 타입도 `Admin[]`으로 좁혀집니다. 타입 서술어가 없으면 `Person[]`으로 남습니다.

### 힌트

**힌트 1**: `isAdmin` 함수의 반환 타입을 `boolean`이 아닌 `person is Admin`으로 바꾸십시오.

```typescript
export function isAdmin(person: Person): person is Admin {
    return person.type === 'admin';
}
```

**힌트 2**: 마찬가지로 `isUser` 함수의 반환 타입을 `person is User`로 바꾸십시오.

**힌트 3**: 함수 본문(`return person.type === 'admin'`)은 변경하지 않아도 됩니다. 반환 타입 선언만 추가하면 됩니다.

### 풀이

```typescript
interface User {
    type: 'user';
    name: string;
    age: number;
    occupation: string;
}

interface Admin {
    type: 'admin';
    name: string;
    age: number;
    role: string;
}

export type Person = User | Admin;

export const persons: Person[] = [
    { type: 'user', name: 'Max Mustermann', age: 25, occupation: 'Chimney sweep' },
    { type: 'admin', name: 'Jane Doe', age: 32, role: 'Administrator' },
    { type: 'user', name: 'Kate Müller', age: 23, occupation: 'Astronaut' },
    { type: 'admin', name: 'Bruce Willis', age: 64, role: 'World saver' }
];

// 반환 타입을 'person is Admin'으로 선언합니다
export function isAdmin(person: Person): person is Admin {
    return person.type === 'admin';
}

// 반환 타입을 'person is User'로 선언합니다
export function isUser(person: Person): person is User {
    return person.type === 'user';
}

export function logPerson(person: Person) {
    let additionalInformation: string = '';
    if (isAdmin(person)) {
        // isAdmin이 true를 반환했으므로 TypeScript는 person을 Admin으로 좁혀 줍니다
        additionalInformation = person.role;       // 정상
    }
    if (isUser(person)) {
        // isUser가 true를 반환했으므로 TypeScript는 person을 User로 좁혀 줍니다
        additionalInformation = person.occupation;  // 정상
    }
    console.log(` - ${person.name}, ${person.age}, ${additionalInformation}`);
}

console.log('Admins:');
persons.filter(isAdmin).forEach(logPerson); // filter 결과가 Admin[]으로 좁혀집니다
console.log();
console.log('Users:');
persons.filter(isUser).forEach(logPerson);  // filter 결과가 User[]로 좁혀집니다
```

### 풀이 상세 설명

**1단계: 타입 서술어 없는 경우 vs 있는 경우 비교**

```typescript
// 타입 서술어 없는 경우 — 반환 타입이 boolean
function isAdminNaive(person: Person): boolean {
    return person.type === 'admin';
}

if (isAdminNaive(person)) {
    person.role; // 오류: TypeScript가 person을 Admin으로 좁혀 주지 않습니다
                 // person은 여전히 Person(= User | Admin) 타입입니다
}

// 타입 서술어 있는 경우 — 반환 타입이 person is Admin
function isAdmin(person: Person): person is Admin {
    return person.type === 'admin';
}

if (isAdmin(person)) {
    person.role; // 정상: TypeScript가 person을 Admin으로 좁혀 줍니다
}
```

반환 타입 `person is Admin`이 TypeScript에게 "이 함수가 `true`를 반환하면, `person` 인자가 `Admin` 타입이라고 보장한다"는 약속을 전달합니다.

**2단계: `filter`에서의 타입 서술어 활용**

```typescript
// 타입 서술어 없는 경우
const admins = persons.filter(isAdminNaive); // 타입: Person[]

// 타입 서술어 있는 경우
const admins = persons.filter(isAdmin); // 타입: Admin[]
```

`Array.filter`는 콜백이 타입 서술어를 반환하면 결과 배열의 타입도 자동으로 좁혀 줍니다. 실무에서 자주 사용되는 패턴입니다.

**3단계: Discriminated Union과의 조합**

이 문제에서 `User`의 `type: 'user'`와 `Admin`의 `type: 'admin'`은 리터럴 타입을 사용한 Discriminated Union입니다. `person.type === 'admin'`이라는 판별식이 있기 때문에 타입 서술어 함수의 본문을 간단하게 작성할 수 있습니다.

만약 `type` 필드 없이 속성 존재 여부로 구분해야 한다면 `in` 연산자(Exercise 3)를 사용합니다.

```typescript
// type 필드가 없는 경우 — in 연산자 활용
function isAdmin(person: Person): person is Admin {
    return 'role' in person;
}
```

### 이해 확인

이 문제에서 배운 것을 정리합니다.

- **타입 서술어**: `param is Type` 형태의 반환 타입을 선언하면, 함수가 `true`를 반환할 때 TypeScript가 매개변수의 타입을 좁혀 줍니다.
- **`boolean` vs `param is Type`**: `boolean` 반환 함수로는 타입 좁히기가 안 됩니다. 반드시 타입 서술어 반환 타입을 명시해야 합니다.
- **`filter`와의 궁합**: `Array.filter(fn)`에서 `fn`이 타입 서술어를 반환하면 필터링된 배열의 타입도 자동으로 좁혀집니다.
- **재사용성**: `isAdmin`, `isUser` 같은 타입 가드 함수를 한 번 정의해 두면 코드 여러 곳에서 재사용할 수 있어 타입 좁히기가 일관되게 유지됩니다.

---

## Exercise 5 (선택, 5분): `Partial`과 `Omit` 유틸리티 타입

### 문제 설명

`filterUsers` 함수가 `criteria` 인자를 받아 사용자를 필터링합니다. 현재 `criteria`의 타입이 `User`로 되어 있어서, `{ age: 23 }` 처럼 일부 필드만 전달하면 타입 오류가 발생합니다. 또한 `type` 필드(`'user'`)는 판별용이므로 필터 기준에서 제외해야 합니다. `Partial`과 `Omit` 유틸리티 타입을 조합하여 `criteria` 타입을 수정하십시오.

이 Exercise는 선택 사항으로, 앞의 문제를 모두 푼 뒤 시간이 남을 경우 진행합니다.

### 시작 코드 (핵심 부분)

```typescript
interface User {
    type: 'user';
    name: string;
    age: number;
    occupation: string;
}

// 문제: criteria가 User 전체를 요구하므로 { age: 23 }만 넘기면 오류
export function filterUsers(persons: Person[], criteria: User): User[] {
    return persons.filter(isUser).filter((user) => {
        const criteriaKeys = Object.keys(criteria) as (keyof User)[];
        return criteriaKeys.every((fieldName) => {
            return user[fieldName] === criteria[fieldName];
        });
    });
}

// 호출 시 타입 오류 발생
filterUsers(persons, { age: 23 });
```

### 컴파일러 오류 메시지 (풀기 전 상태)

```
Argument of type '{ age: number; }' is not assignable to parameter of type 'User'.
  Type '{ age: number; }' is missing the following properties from type 'User':
    type, name, occupation
```

`criteria: User`는 `User`의 모든 필드(`type`, `name`, `age`, `occupation`)가 필수입니다. 하지만 호출 시 `{ age: 23 }`만 넘겼으므로 오류가 발생합니다.

### 핵심 개념

이 문제는 두 가지 유틸리티 타입을 조합하는 법을 테스트합니다.

- **`Partial<T>`**: `T`의 모든 필드를 선택적(`?`)으로 만듭니다. `{ age: 23 }`처럼 일부 필드만 넘길 수 있게 됩니다.
- **`Omit<T, K>`**: `T`에서 `K`에 해당하는 필드를 제외한 타입을 만듭니다. `Omit<User, 'type'>`은 `type` 필드 없는 User 타입을 만듭니다.
- 두 가지를 조합하면: `Partial<Omit<User, 'type'>>` — `type` 필드를 제외하고, 나머지 필드는 모두 선택적입니다.

### 주요 유틸리티 타입 정리

```typescript
interface User {
    type: 'user';
    name: string;
    age: number;
    occupation: string;
}

// Partial<User>: 모든 필드가 선택적
type PartialUser = Partial<User>;
// { type?: 'user'; name?: string; age?: number; occupation?: string; }

// Omit<User, 'type'>: type 필드 제외
type UserWithoutType = Omit<User, 'type'>;
// { name: string; age: number; occupation: string; }

// Partial<Omit<User, 'type'>>: type 제외 + 모두 선택적
type FilterCriteria = Partial<Omit<User, 'type'>>;
// { name?: string; age?: number; occupation?: string; }
```

### 풀이

```typescript
// criteria 타입을 Partial<Omit<User, 'type'>>으로 변경합니다
export function filterUsers(
    persons: Person[],
    criteria: Partial<Omit<User, 'type'>>
): User[] {
    return persons.filter(isUser).filter((user) => {
        const criteriaKeys = Object.keys(criteria) as (keyof User)[];
        return criteriaKeys.every((fieldName) => {
            return user[fieldName] === criteria[fieldName];
        });
    });
}

// 이제 일부 필드만 넘겨도 오류 없음
filterUsers(persons, { age: 23 });
filterUsers(persons, { name: 'Kate Müller', occupation: 'Astronaut' });
filterUsers(persons, {}); // 빈 객체도 허용 — 필터 조건 없음
```

### 이해 확인

- **`Partial<T>`**: 모든 필드를 `?` (선택적)으로 변환합니다. 일부 필드만 제공해도 됩니다.
- **`Omit<T, K>`**: 특정 필드를 제외합니다. 외부에 노출하면 안 되거나 필터 기준에 불필요한 필드를 제거할 때 사용합니다.
- **타입 조합**: `Partial<Omit<T, K>>` 처럼 유틸리티 타입을 중첩해서 새로운 타입을 만들 수 있습니다.
- **실무 활용**: 업데이트 함수(`PATCH` API), 검색 필터, 폼 기본값 등에서 `Partial`이 자주 쓰입니다.

다른 유용한 유틸리티 타입:

| 유틸리티 타입 | 설명 | 예시 |
|--------------|------|------|
| `Partial<T>` | 모든 필드 선택적으로 | `Partial<User>` |
| `Required<T>` | 모든 필드 필수로 | `Required<Config>` |
| `Readonly<T>` | 모든 필드 읽기 전용으로 | `Readonly<User>` |
| `Pick<T, K>` | 특정 필드만 선택 | `Pick<User, 'name' \| 'age'>` |
| `Omit<T, K>` | 특정 필드 제외 | `Omit<User, 'type'>` |

---

## 시간 배분 가이드

| Exercise | 예상 시간 | 난이도 | 핵심 개념 |
|----------|----------|--------|-----------|
| 1 | 5분 | 쉬움 | type alias, 기본 타입(string, number), unknown |
| 2 | 5분 | 쉬움 | Union 타입(\|), Person 타입 정의, 배열 타입 변경 |
| 3 | 7분 | 보통 | `in` 연산자, 타입 좁히기(narrowing) |
| 4 | 8분 | 보통 | 타입 서술어(person is Admin), 사용자 정의 타입 가드 |
| 5 | 5분 | 도전 | Partial, Omit 유틸리티 타입 조합 (선택) |

---

## 강사 진행 팁

### 시간 관리

- 각 Exercise 시작 전에 문제를 1분 이내로 간략히 소개하십시오. 긴 설명보다 학생이 직접 오류를 경험하게 하는 것이 효과적입니다.
- Exercise 1과 2는 빠르게 진행할 수 있습니다. 5분이 지나도 대부분의 학생이 풀지 못했다면, 힌트 1을 공유하십시오.
- Exercise 1에서 흔한 실수: `occupation` 필드를 빠뜨리는 것입니다. 데이터 객체를 먼저 확인하도록 유도하십시오.
- Exercise 2에서 흔한 실수: `Person` 타입만 바꾸고 `persons`와 `logPerson`의 타입을 바꾸지 않는 것입니다. 세 곳을 모두 수정해야 한다고 안내하십시오.
- Exercise 3과 4는 난이도가 올라갑니다. 컴파일러 오류 메시지를 읽는 시간을 충분히 주십시오.
- 전체 30분 중 Exercise 4까지 완료하는 것을 목표로 합니다. Exercise 5는 10분 이상 남을 때만 진행합니다.

### 학생이 막힐 때

- 먼저 **컴파일러 오류 메시지**를 소리 내어 읽어보게 하십시오. 오류 메시지에 문제 해결의 단서가 대부분 담겨 있습니다.
- "어떤 타입이 기대되고, 어떤 타입이 실제로 전달됐는지"를 묻는 질문이 효과적입니다.
- 오류 위치에 마우스를 올리면 VS Code나 TypeScript Playground에서 더 상세한 오류 설명을 볼 수 있음을 안내하십시오.
- 힌트를 단계적으로 공개하십시오. 힌트 1 → 2 → 3 순서로, 바로 정답을 주지 않는 것이 학습 효과를 높입니다.

### 중간 체크 포인트

- Exercise 2 완료 후: "Union 타입이 무엇인지 이해한 분?" 간단히 손들기로 확인합니다.
- Exercise 3 완료 후: "`in` 연산자가 어떻게 타입을 좁혀 주는지 설명할 수 있는 분?" 질문합니다.
- Exercise 4 완료 후: "타입 서술어 반환 타입을 `boolean` 대신 쓰면 무엇이 달라지는지 설명할 수 있는 분?" 질문합니다.

### 사이트 접속 문제 시

https://typescript-exercises.github.io 가 접속되지 않을 경우, 이 가이드의 시작 코드를 다음 방법으로 활용하십시오.

1. **로컬 실행 (tsx)**: 시작 코드를 `exercise1.ts` 파일로 저장한 뒤 `tsx exercise1.ts` 로 실행합니다. Session 0에서 설치한 `tsx` 도구를 사용합니다.
2. **TypeScript Playground** (https://www.typescriptlang.org/play): 브라우저에서 바로 사용 가능하며, 실시간 타입 검사가 됩니다.
3. **가이드 풀이 참조**: 시간이 부족하면 풀이를 함께 읽으며 진행합니다.

---

## Q&A 예상 질문과 답변

**Q1. `type`과 `interface`의 차이가 무엇인가요? 언제 어느 것을 써야 하나요?**

`interface`는 선언 병합(Declaration Merging)을 지원합니다. 같은 이름으로 두 번 선언하면 TypeScript가 자동으로 합칩니다. `type`은 선언 병합이 안 되지만, Union(`|`), Intersection(`&`), Mapped Types 등 더 복잡한 타입 조합에 사용할 수 있습니다. 일반적인 객체 타입 정의에는 둘 중 어느 것을 써도 무방합니다. 팀 컨벤션을 따르는 것을 권장하며, 정해진 컨벤션이 없다면 객체 구조는 `interface`, 조합 타입은 `type`을 사용하는 것이 일반적인 관행입니다.

**Q2. `unknown`과 `any`의 차이는 무엇인가요?**

`any`는 TypeScript의 타입 검사를 완전히 비활성화합니다. `any` 타입 변수에는 어떤 속성이든 접근할 수 있어 타입 안전성이 사라집니다. `unknown`은 "타입을 모른다"는 의미이지만, 접근 전에 반드시 타입을 좁혀야(narrow) 합니다. `unknown`은 타입 안전한 방식으로 외부 데이터를 다룰 때 사용합니다. 일반적으로 `any` 사용은 최소화하고 `unknown`을 활용하는 것이 좋습니다.

**Q3. Union 타입에서 공통 속성이 아닌 속성에 접근하면 왜 오류가 나나요?**

`User | Admin` 타입의 변수는 런타임에 `User`일 수도 있고 `Admin`일 수도 있습니다. TypeScript는 컴파일 시점에 둘 중 어느 것인지 알 수 없기 때문에, 안전하게 접근할 수 있는 속성(두 타입 모두 가진 공통 속성)만 허용합니다. `role`은 `Admin`에만 있으므로, 타입 좁히기(타입 가드) 없이 접근하면 오류가 발생합니다.

**Q4. `in` 연산자 대신 다른 방법으로 타입을 좁힐 수 있나요?**

네, 여러 방법이 있습니다.

- `typeof` 연산자: `typeof value === 'string'` 으로 원시 타입을 좁힙니다.
- `instanceof` 연산자: `value instanceof Date` 로 클래스 인스턴스를 좁힙니다.
- 리터럴 타입 비교: `person.type === 'admin'` 처럼 discriminant 필드 값을 비교합니다(Exercise 4에서 사용).
- 사용자 정의 타입 가드: `function isAdmin(p): p is Admin { ... }` 처럼 직접 작성합니다(Exercise 4).

`in` 연산자는 속성 존재 여부로 타입을 구별할 때, discriminant 필드 비교는 명시적인 `type` 필드가 있을 때 적합합니다.

**Q5. 타입 서술어 함수의 반환 타입을 왜 `boolean` 대신 `person is Admin` 으로 써야 하나요?**

반환 타입이 `boolean` 이면 TypeScript는 이 함수가 타입 정보를 전달한다는 것을 모릅니다. `true`가 반환되어도 `person`의 타입은 여전히 `Person`으로 유지됩니다. 반환 타입을 `person is Admin` 으로 쓰면 "이 함수가 `true`를 반환할 때 `person`은 `Admin`이다"라는 약속을 TypeScript에 전달합니다. 이후 `if (isAdmin(person)) { ... }` 블록 안에서 TypeScript가 `person`을 `Admin` 으로 좁혀 줍니다.

**Q6. Exercise 1~4에서 배운 개념이 실제 프로젝트에서 어떻게 활용되나요?**

- **기본 타입 선언(Exercise 1)**: API 응답 객체, 컴포넌트 props, 함수 매개변수 등 모든 곳에 사용됩니다.
- **Interface와 Union(Exercise 2)**: 여러 상태를 가지는 데이터 모델에 사용됩니다. 예를 들어 로딩/성공/오류 상태를 Union으로 표현합니다.
- **`in` 연산자 타입 좁히기(Exercise 3)**: API로 받은 데이터를 런타임에 타입별로 분기 처리할 때 사용합니다.
- **타입 서술어(Exercise 4)**: `Array.filter`와 조합하여 특정 타입만 추출하거나, 재사용 가능한 타입 가드 함수를 만들 때 사용합니다.

---

## 핵심 요약

이번 실습에서 다룬 TypeScript의 핵심 개념을 정리합니다.

### 배운 개념 한눈에 보기

| 개념 | 구문 | 사용 목적 |
|------|------|-----------|
| 타입 별칭 | `type T = { ... }` | 객체 모양 정의 |
| 인터페이스 | `interface T { ... }` | 객체 모양 정의 (선언 병합 지원) |
| Union 타입 | `A \| B` | 여러 타입 중 하나 |
| `in` 연산자 | `'prop' in obj` | 속성 존재 여부로 타입 좁히기 |
| 타입 서술어 | `param is Type` 반환 타입 | 타입 가드 함수 |
| Partial | `Partial<T>` | 모든 필드 선택적으로 변환 |
| Omit | `Omit<T, 'key'>` | 특정 필드 제외 |
| Pick | `Pick<T, 'a' \| 'b'>` | 특정 필드만 선택 |

### 실습 흐름 정리

- **Exercise 1**: `unknown` → 구체적인 타입 선언 (기본기)
- **Exercise 2**: Union 타입(`User | Admin`)으로 여러 타입 합치기
- **Exercise 3**: `in` 연산자로 런타임에 타입 구분 (좁히기)
- **Exercise 4**: 타입 서술어로 재사용 가능한 타입 가드 만들기
- **Exercise 5**: 유틸리티 타입 조합으로 실용적인 타입 파생

### 다음 단계

다음 세션에서는 이 개념들을 React 컴포넌트에 적용합니다. `props` 타입 정의, 이벤트 핸들러 타입 지정, `useState` 제네릭 활용 등 React와 TypeScript를 함께 사용하는 실전 패턴을 다룹니다.

---

*이 가이드는 https://typescript-exercises.github.io 의 Exercise 1~5 내용을 기반으로 작성되었습니다. 사이트 접속이 가능한 경우 직접 풀어보는 것을 권장합니다. 실시간 컴파일러 피드백이 학습에 도움이 됩니다.*
