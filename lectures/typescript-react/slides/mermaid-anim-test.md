---
theme: default
title: Mermaid 애니메이션 테스트
---

# Mermaid 애니메이션 탐구

3가지 접근법 테스트

---

## 접근법 1: v-click으로 Mermaid 단계별 교체

<v-click-hide>

```mermaid
graph LR
    A[브라우저]
```

</v-click-hide>

<v-click>
<v-click-hide>

```mermaid
graph LR
    A[브라우저] -->|요청| B[웹 서버]
```

</v-click-hide>
</v-click>

<v-click>

```mermaid
graph LR
    A[브라우저] -->|요청| B[웹 서버] -->|쿼리| C[(DB)]
    C -->|결과| B -->|응답| A
```

</v-click>

---

## 접근법 2: CSS로 Mermaid SVG 노드 타겟팅

Mermaid는 노드에 `id="flowchart-A-N"` 형태의 ID를 부여

<div :class="'mermaid-step-' + $clicks">

```mermaid
graph LR
    A[브라우저] -->|요청| B[웹 서버]
    B -->|쿼리| C[(DB)]
    C -->|결과| B
    B -->|응답| A
```

</div>

<style>
.mermaid-step-0 .node:not(:first-child) { opacity: 0.15; }
.mermaid-step-0 .edgePath { opacity: 0.1; }
.mermaid-step-0 .edgeLabel { opacity: 0.1; }
.mermaid-step-1 .node { opacity: 1; transition: opacity 0.3s; }
.mermaid-step-1 .edgePath { opacity: 0.3; transition: opacity 0.3s; }
.mermaid-step-1 .edgeLabel { opacity: 0.3; transition: opacity 0.3s; }
.mermaid-step-2 .node { opacity: 1; }
.mermaid-step-2 .edgePath { opacity: 1; transition: opacity 0.3s; }
.mermaid-step-2 .edgeLabel { opacity: 1; transition: opacity 0.3s; }
</style>

---

## 접근법 3: HTML/CSS 다이어그램 (대조군)

같은 내용을 HTML/CSS + $clicks로 구현

<div class="flex items-center justify-center gap-3 mt-12">
  <div class="bg-cyan-500 text-black px-6 py-4 rounded-xl text-center font-bold shadow-lg transition-all duration-300" :class="$clicks === 0 ? 'ring-2 ring-cyan-300 scale-105' : $clicks >= 3 ? 'opacity-100' : 'opacity-40'">
    <div>브라우저</div>
  </div>
  <div class="text-xl transition-all duration-300" :class="$clicks >= 1 ? 'opacity-50' : 'opacity-0'">→</div>
  <div class="transition-all duration-500" :class="$clicks >= 1 ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'">
    <div class="bg-green-500 text-black px-6 py-4 rounded-xl text-center font-bold shadow-lg" :class="$clicks === 1 ? 'ring-2 ring-green-300 scale-105' : ''">
      <div>웹 서버</div>
    </div>
  </div>
  <div class="text-xl transition-all duration-300" :class="$clicks >= 2 ? 'opacity-50' : 'opacity-0'">→</div>
  <div class="transition-all duration-500" :class="$clicks >= 2 ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'">
    <div class="bg-orange-500 text-black px-6 py-4 rounded-xl text-center font-bold shadow-lg" :class="$clicks === 2 ? 'ring-2 ring-orange-300 scale-105' : ''">
      <div>DB</div>
    </div>
  </div>
</div>

<div class="text-center mt-6 transition-all duration-500" :class="$clicks >= 3 ? 'opacity-100' : 'opacity-0'">
  <div class="text-sm text-green-400 font-bold">← 전체 흐름 완성: 요청 → 처리 → 응답 →</div>
</div>
