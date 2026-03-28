# Slidev 다크 배경 카드 레이아웃 + v-click 애니메이션 가이드

## 핵심 개념

Slidev는 UnoCSS(Tailwind CSS 호환)를 내장하고 있어 유틸리티 클래스만으로 카드 UI를 구성할 수 있다. `v-click` 디렉티브를 조합하면 카드가 하나씩 순서대로 나타나는 애니메이션을 만들 수 있다.

---

## 1. 카드 스타일링에 사용하는 UnoCSS 클래스

### 배경 및 색상

| 클래스 | 설명 |
|--------|------|
| `bg-slate-800` | 다크 슬라이드 배경 |
| `bg-slate-700` / `bg-slate-700/80` | 카드 배경 (불투명도 조절 가능) |
| `bg-gray-800/60` | 반투명 카드 배경 |
| `text-white` | 흰색 텍스트 |
| `text-gray-300` | 연한 회색 본문 텍스트 |
| `text-blue-400` | 강조 포인트 색상 |

### 둥근 모서리 (Border Radius)

| 클래스 | 값 |
|--------|-----|
| `rounded` | 0.25rem |
| `rounded-lg` | 0.5rem |
| `rounded-xl` | 0.75rem |
| `rounded-2xl` | 1rem |
| `rounded-3xl` | 1.5rem |

### 그림자 (Box Shadow)

| 클래스 | 설명 |
|--------|------|
| `shadow` | 기본 그림자 |
| `shadow-md` | 중간 그림자 |
| `shadow-lg` | 큰 그림자 |
| `shadow-xl` | 매우 큰 그림자 |
| `shadow-2xl` | 최대 그림자 |

> 다크 배경에서는 `shadow-lg` 이상을 사용해야 시각적으로 구분된다.

### 패딩 및 간격

| 클래스 | 설명 |
|--------|------|
| `p-4` / `p-6` / `p-8` | 내부 여백 |
| `gap-4` / `gap-6` | 그리드/플렉스 아이템 간격 |
| `space-y-4` | 세로 방향 간격 |

### 테두리

| 클래스 | 설명 |
|--------|------|
| `border border-slate-600` | 연한 테두리 |
| `border-l-4 border-blue-500` | 왼쪽 강조 테두리 |

---

## 2. 레이아웃 구성 패턴

### 그리드 레이아웃 (가장 추천)

```html
<div class="grid grid-cols-3 gap-6">
  <div class="bg-slate-700 rounded-xl shadow-lg p-6">카드 1</div>
  <div class="bg-slate-700 rounded-xl shadow-lg p-6">카드 2</div>
  <div class="bg-slate-700 rounded-xl shadow-lg p-6">카드 3</div>
</div>
```

- `grid-cols-2`: 2열 레이아웃
- `grid-cols-3`: 3열 레이아웃
- `grid-cols-4`: 4열 레이아웃 (작은 카드)

### 플렉스 레이아웃

```html
<div class="flex gap-6">
  <div class="flex-1 bg-slate-700 rounded-xl shadow-lg p-6">카드 1</div>
  <div class="flex-1 bg-slate-700 rounded-xl shadow-lg p-6">카드 2</div>
</div>
```

---

## 3. v-click 애니메이션 적용

### 기본: 각 카드에 v-click

```html
<div class="grid grid-cols-3 gap-6">
  <div v-click class="bg-slate-700 rounded-xl shadow-lg p-6">
    <h3 class="text-blue-400 text-xl font-bold mb-2">제목 1</h3>
    <p class="text-gray-300">설명 텍스트</p>
  </div>
  <div v-click class="bg-slate-700 rounded-xl shadow-lg p-6">
    <h3 class="text-blue-400 text-xl font-bold mb-2">제목 2</h3>
    <p class="text-gray-300">설명 텍스트</p>
  </div>
  <div v-click class="bg-slate-700 rounded-xl shadow-lg p-6">
    <h3 class="text-blue-400 text-xl font-bold mb-2">제목 3</h3>
    <p class="text-gray-300">설명 텍스트</p>
  </div>
</div>
```

클릭할 때마다 카드가 하나씩 나타난다.

### 순서 지정: v-click 숫자

```html
<div v-click="1">첫 번째로 나타남</div>
<div v-click="2">두 번째로 나타남</div>
<div v-click="3">세 번째로 나타남</div>
```

### v-after: 이전 v-click과 동시에 나타남

```html
<div v-click>카드 A (클릭 1에 나타남)</div>
<div v-after>카드 B (카드 A와 동시에 나타남)</div>
```

---

## 4. 호버 효과 추가

UnoCSS에서 `hover:` 접두사로 호버 효과를 줄 수 있다:

```html
<div class="bg-slate-700 rounded-xl shadow-lg p-6
            hover:bg-slate-600 hover:shadow-xl
            transition-all duration-300">
  카드 내용
</div>
```

- `hover:bg-slate-600`: 호버 시 밝아짐
- `hover:shadow-xl`: 호버 시 그림자 강화
- `hover:scale-105`: 호버 시 약간 확대
- `hover:-translate-y-1`: 호버 시 살짝 올라감
- `transition-all duration-300`: 부드러운 전환 효과

---

## 5. 완성된 카드 컴포넌트 패턴

```html
<!-- 슬라이드 프론트매터 -->
---
layout: default
class: bg-slate-900
---

# 핵심 기능 소개

<div class="grid grid-cols-3 gap-6 mt-8">
  <div v-click class="bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-700
                       hover:border-blue-500 transition-all duration-300">
    <div class="text-3xl mb-3">🚀</div>
    <h3 class="text-blue-400 text-lg font-bold mb-2">빠른 시작</h3>
    <p class="text-gray-400 text-sm">5분 안에 프로젝트를 시작할 수 있습니다</p>
  </div>

  <div v-click class="bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-700
                       hover:border-green-500 transition-all duration-300">
    <div class="text-3xl mb-3">🔧</div>
    <h3 class="text-green-400 text-lg font-bold mb-2">간편 설정</h3>
    <p class="text-gray-400 text-sm">YAML 설정 하나로 모든 것을 관리합니다</p>
  </div>

  <div v-click class="bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-700
                       hover:border-purple-500 transition-all duration-300">
    <div class="text-3xl mb-3">📦</div>
    <h3 class="text-purple-400 text-lg font-bold mb-2">확장 가능</h3>
    <p class="text-gray-400 text-sm">플러그인으로 기능을 자유롭게 확장합니다</p>
  </div>
</div>
```

---

## 6. 자주 쓰는 조합 정리

### 기본 카드

```
bg-slate-700 rounded-xl shadow-lg p-6
```

### 테두리 강조 카드

```
bg-slate-800 rounded-2xl shadow-xl p-6 border border-slate-700
```

### 그라데이션 카드

```
bg-gradient-to-br from-blue-900/50 to-slate-800 rounded-xl shadow-lg p-6
```

### 글래스모피즘 카드

```
bg-white/5 backdrop-blur-md rounded-xl shadow-lg p-6 border border-white/10
```

---

## 7. 주의사항

1. **슬라이드 배경 설정**: 프론트매터에서 `class: bg-slate-900`으로 전체 배경을 어둡게 설정한다. 또는 Slidev 테마의 다크모드를 활성화한다.

2. **v-click과 그리드**: `v-click`은 `display: none`으로 시작하기 때문에 그리드 레이아웃이 깨질 수 있다. Slidev는 이를 `visibility: hidden`으로 처리하여 공간을 유지하므로 대부분 문제없지만, 레이아웃이 깨지면 각 카드를 래핑하는 방식을 시도한다.

3. **텍스트 크기**: 슬라이드에서는 `text-sm`~`text-lg` 범위가 적당하다. 제목은 `text-xl` 이상, 본문은 `text-sm` 또는 `text-base`를 사용한다.

4. **색상 대비**: 다크 배경에서 `text-gray-400` 이하는 가독성이 떨어질 수 있다. 본문 텍스트는 `text-gray-300` 이상을 권장한다.
