# Slidev 다크 배경 위 카드 레이아웃 + v-click 애니메이션

## 1. 카드 스타일링에 쓰이는 UnoCSS 클래스

Slidev는 UnoCSS를 기본 CSS 프레임워크로 사용하므로, Tailwind CSS 스타일의 유틸리티 클래스를 슬라이드 마크다운 안에서 바로 쓸 수 있다.

### 배경 (Background)

| 클래스 | 설명 |
|--------|------|
| `bg-slate-800` | 불투명 어두운 슬레이트 배경 |
| `bg-slate-800/80` | 80% 투명도 (반투명 효과) |
| `bg-gray-800/50` | 50% 투명도 회색 배경 |
| `bg-blue-900/30` | 30% 투명도 파란 배경 (포인트 카드) |

> `/` 뒤의 숫자(20, 50, 80 등)는 투명도 퍼센트다. 다크 배경 슬라이드에서 카드를 살짝 띄우려면 `/50`~`/80` 범위가 적절하다.

### 둥근 모서리 (Border Radius)

| 클래스 | 반경 |
|--------|------|
| `rounded` | 4px |
| `rounded-md` | 6px |
| `rounded-lg` | 8px |
| `rounded-xl` | 12px |
| `rounded-2xl` | 16px |

### 그림자 (Shadow)

| 클래스 | 효과 |
|--------|------|
| `shadow` | 기본 그림자 |
| `shadow-md` | 중간 그림자 |
| `shadow-lg` | 큰 그림자 |
| `shadow-xl` | 매우 큰 그림자 |

> 다크 배경에서는 그림자가 잘 안 보일 수 있다. `shadow-xl`을 쓰거나, `border border-gray-700` 같은 테두리를 함께 적용하면 카드 경계가 더 뚜렷해진다.

### 패딩/마진 (Spacing)

| 클래스 | 설명 |
|--------|------|
| `p-4` | 패딩 16px (사방) |
| `p-6` | 패딩 24px |
| `px-6 py-4` | 좌우 24px, 상하 16px |
| `mt-4` | 상단 마진 16px |
| `gap-4` | 그리드/플렉스 자식 간격 16px |

### 테두리 (Border)

| 클래스 | 설명 |
|--------|------|
| `border border-gray-700` | 1px 회색 테두리 |
| `border-l-4 border-blue-400` | 왼쪽 4px 파란 포인트 라인 |
| `border-t-2 border-green-400` | 상단 2px 녹색 라인 |

---

## 2. 카드 레이아웃 기본 패턴

### 단일 카드

```md
<div class="bg-slate-800/80 rounded-xl p-6 shadow-xl border border-gray-700">

**카드 제목**

카드 내용을 여기에 작성한다.

</div>
```

### 그리드로 카드 배열 (2열)

```md
<div class="grid grid-cols-2 gap-4 mt-4">

<div class="bg-slate-800/80 rounded-xl p-5 shadow-lg border border-gray-700">

**첫 번째 카드**

내용

</div>

<div class="bg-slate-800/80 rounded-xl p-5 shadow-lg border border-gray-700">

**두 번째 카드**

내용

</div>

</div>
```

### 그리드로 카드 배열 (3열)

```md
<div class="grid grid-cols-3 gap-4 mt-4">

<div class="bg-slate-800/80 rounded-lg p-4 shadow-lg">

**카드 1**

</div>

<div class="bg-slate-800/80 rounded-lg p-4 shadow-lg">

**카드 2**

</div>

<div class="bg-slate-800/80 rounded-lg p-4 shadow-lg">

**카드 3**

</div>

</div>
```

---

## 3. v-click으로 카드 하나씩 나타내기

### 방법 A: 각 카드에 `v-click` 디렉티브

```md
<div class="grid grid-cols-3 gap-4 mt-4">

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-lg">

**1단계**: 설계

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-lg">

**2단계**: 구현

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-lg">

**3단계**: 배포

</div>

</div>
```

클릭할 때마다 카드가 하나씩 나타난다. 기본적으로 `opacity: 0 -> 1` 전환이 적용된다.

### 방법 B: `forward:delay-*`로 시차 애니메이션

각 카드에 서로 다른 딜레이를 주면 순차적으로 나타나는 효과를 줄 수 있다.

```md
<div class="grid grid-cols-3 gap-4 mt-4">

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-lg transition forward:delay-100">

**설계**

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-lg transition forward:delay-200">

**구현**

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-lg transition forward:delay-300">

**배포**

</div>

</div>
```

> `forward:delay-*`는 앞으로 넘길 때만 딜레이가 적용된다. 뒤로 돌아갈 때는 딜레이 없이 바로 사라져서 자연스럽다.

### 방법 C: `v-motion`으로 슬라이드인 효과

단순 opacity 전환 대신 위치/크기 변화를 주고 싶다면 `v-motion`을 활용한다.

```md
<div
  v-click
  v-motion
  :initial="{ y: 40, opacity: 0 }"
  :enter="{ y: 0, opacity: 1 }"
  class="bg-slate-800/80 rounded-xl p-5 shadow-lg"
>

**아래에서 올라오는 카드**

</div>
```

---

## 4. 다크 모드 대응

Slidev는 다크/라이트 모드를 모두 지원한다. `dark:` 접두사로 다크 모드 전용 스타일을 지정할 수 있다.

```md
<div class="bg-white dark:bg-slate-800/80 rounded-xl p-5 shadow-lg
            border border-gray-200 dark:border-gray-700
            text-gray-800 dark:text-gray-100">

라이트/다크 모드 모두에서 잘 보이는 카드

</div>
```

**다크모드 전용으로 작성할 경우** (프로젝트 CLAUDE.md에서 다크모드 기본으로 명시), `dark:` 접두사 없이 어두운 색상을 직접 쓰면 된다:

```md
<div class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700 text-gray-100">

다크모드 전용 카드

</div>
```

---

## 5. 재사용 가능한 UnoCSS 숏컷

같은 카드 스타일을 반복한다면 `uno.config.ts`에 숏컷을 등록할 수 있다.

```ts
// uno.config.ts
import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    'card': 'bg-slate-800/80 rounded-xl p-5 shadow-lg border border-gray-700',
    'card-highlight': 'bg-blue-900/30 rounded-xl p-5 shadow-lg border border-blue-500/50',
    'card-title': 'text-lg font-bold text-white mb-2',
  },
})
```

이후 슬라이드에서 간결하게 사용:

```md
<div v-click class="card">

<div class="card-title">제목</div>

내용

</div>
```

---

## 6. 캔버스 제약 주의사항

Slidev 캔버스는 **980 x 552px**로 고정이며 스크롤이 없다.

| 레이아웃 | 권장 카드 수 | 비고 |
|----------|-------------|------|
| 2열 그리드 | 2~4개 | 카드당 내용 3~4줄 이내 |
| 3열 그리드 | 3~6개 | 카드당 내용 2~3줄 이내 |
| 1열 세로 나열 | 2~3개 | 카드당 내용 4~5줄 이내 |

카드가 5개 이상이면 슬라이드를 분할하거나 `zoom: 0.9` (frontmatter)를 고려한다. `zoom`은 0.8 미만으로 내리지 않는다.

---

## 7. 완전한 예시 요약

```md
---
layout: default
---

# 핵심 개념 3가지

<div class="grid grid-cols-3 gap-4 mt-6">

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700 transition forward:delay-100">

<div class="text-2xl mb-2">1</div>

**설계**

요구사항을 분석하고 아키텍처를 설계한다

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700 transition forward:delay-200">

<div class="text-2xl mb-2">2</div>

**구현**

코드를 작성하고 테스트를 실행한다

</div>

<div v-click class="bg-slate-800/80 rounded-xl p-5 shadow-xl border border-gray-700 transition forward:delay-300">

<div class="text-2xl mb-2">3</div>

**배포**

CI/CD 파이프라인을 통해 배포한다

</div>

</div>
```
