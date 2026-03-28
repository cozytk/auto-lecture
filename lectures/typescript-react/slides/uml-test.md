---
theme: default
title: UML 다이어그램 HTML/CSS 테스트
---

# UML 다이어그램 — HTML/CSS 구현

복잡한 구조도 HTML/CSS로 표현 가능한지 검증

---
clicks: 2
---

## ① 클래스 다이어그램

<div class="flex justify-center gap-8 mt-6">
  <div class="bg-slate-800 rounded-xl border border-slate-600 w-56 shadow-lg transition-all duration-300" :class="$clicks === 0 ? 'ring-2 ring-blue-400' : ''">
    <div class="bg-blue-600 text-white px-4 py-2 rounded-t-xl font-bold text-center text-sm">Animal</div>
    <div class="px-4 py-2 text-xs border-b border-slate-600 space-y-1">
      <div><span class="text-green-400">+</span> name: string</div>
      <div><span class="text-green-400">+</span> age: number</div>
    </div>
    <div class="px-4 py-2 text-xs space-y-1">
      <div><span class="text-green-400">+</span> speak(): void</div>
      <div><span class="text-green-400">+</span> move(): void</div>
    </div>
  </div>

  <div class="flex flex-col items-center justify-center transition-all duration-500" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">
    <div class="text-xs opacity-50 mb-1">extends</div>
    <div class="text-lg">◁——</div>
  </div>

  <div class="transition-all duration-500" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">
    <div class="bg-slate-800 rounded-xl border border-slate-600 w-56 shadow-lg" :class="$clicks === 1 ? 'ring-2 ring-cyan-400' : ''">
      <div class="bg-cyan-600 text-white px-4 py-2 rounded-t-xl font-bold text-center text-sm">Dog</div>
      <div class="px-4 py-2 text-xs border-b border-slate-600 space-y-1">
        <div><span class="text-green-400">+</span> breed: string</div>
      </div>
      <div class="px-4 py-2 text-xs space-y-1">
        <div><span class="text-green-400">+</span> speak(): void</div>
        <div><span class="text-green-400">+</span> fetch(): void</div>
      </div>
    </div>
  </div>
</div>

<div class="text-center mt-4 text-xs opacity-40 transition-all duration-300" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">
  <span class="text-green-400 font-bold">TypeScript</span>: <code>class Dog extends Animal { breed: string; }</code>
</div>

---
clicks: 3
---

## ② 시퀀스 다이어그램 (HTML/CSS)

<div class="mt-4">
  <div class="flex justify-around">
    <div class="bg-indigo-600 text-white px-6 py-2 rounded-lg font-bold text-sm text-center shadow-lg">사용자</div>
    <div class="bg-emerald-600 text-white px-6 py-2 rounded-lg font-bold text-sm text-center shadow-lg">React</div>
    <div class="bg-amber-600 text-white px-6 py-2 rounded-lg font-bold text-sm text-center shadow-lg">API</div>
    <div class="bg-purple-600 text-white px-6 py-2 rounded-lg font-bold text-sm text-center shadow-lg">DB</div>
  </div>

  <div class="flex justify-around mt-1">
    <div class="w-0.5 h-64 bg-slate-600 mx-auto"></div>
    <div class="w-0.5 h-64 bg-slate-600 mx-auto"></div>
    <div class="w-0.5 h-64 bg-slate-600 mx-auto"></div>
    <div class="w-0.5 h-64 bg-slate-600 mx-auto"></div>
  </div>
</div>

<div class="absolute top-36 left-18 right-18">
  <div class="flex items-center ml-12 mr-56 mt-2 transition-all duration-500" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">
    <div class="flex-1 border-t-2 border-cyan-400"></div>
    <div class="text-xs text-cyan-400 font-bold ml-2">클릭 →</div>
  </div>

  <div class="flex items-center ml-36 mr-32 mt-6 transition-all duration-500" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">
    <div class="flex-1 border-t-2 border-green-400"></div>
    <div class="text-xs text-green-400 font-bold ml-2">GET /api →</div>
  </div>

  <div class="flex items-center ml-56 mr-12 mt-6 transition-all duration-500" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">
    <div class="flex-1 border-t-2 border-amber-400"></div>
    <div class="text-xs text-amber-400 font-bold ml-2">SELECT →</div>
  </div>

  <div class="flex items-center ml-56 mr-12 mt-6 transition-all duration-500" :class="$clicks >= 3 ? 'opacity-100' : 'opacity-0'">
    <div class="text-xs text-amber-400 font-bold mr-2">← 결과</div>
    <div class="flex-1 border-t-2 border-dashed border-amber-400"></div>
  </div>

  <div class="flex items-center ml-36 mr-32 mt-6 transition-all duration-500" :class="$clicks >= 3 ? 'opacity-100' : 'opacity-0'">
    <div class="text-xs text-green-400 font-bold mr-2">← JSON</div>
    <div class="flex-1 border-t-2 border-dashed border-green-400"></div>
  </div>
</div>

---

## ③ 컴포넌트 다이어그램

<div class="flex flex-col items-center gap-4 mt-6">
  <div v-click class="flex gap-4">
    <div class="bg-indigo-700 text-white px-6 py-3 rounded-xl font-bold shadow-lg border-2 border-indigo-500 text-center">
      <div class="text-xs opacity-70">📦 Component</div>
      <div>App</div>
    </div>
  </div>

  <div class="flex gap-2 text-sm opacity-40 transition-all duration-300" :class="$clicks >= 1 ? 'opacity-40' : 'opacity-0'">
    <span>↙</span><span>↓</span><span>↘</span>
  </div>

  <div v-click class="flex gap-4">
    <div class="bg-cyan-700 text-white px-4 py-2 rounded-xl font-bold shadow-lg border-2 border-cyan-500 text-center text-sm">
      <div class="text-xs opacity-70">📦</div>
      <div>Header</div>
    </div>
    <div class="bg-cyan-700 text-white px-4 py-2 rounded-xl font-bold shadow-lg border-2 border-cyan-500 text-center text-sm">
      <div class="text-xs opacity-70">📦</div>
      <div>TodoList</div>
    </div>
    <div class="bg-cyan-700 text-white px-4 py-2 rounded-xl font-bold shadow-lg border-2 border-cyan-500 text-center text-sm">
      <div class="text-xs opacity-70">📦</div>
      <div>Footer</div>
    </div>
  </div>

  <div class="text-sm opacity-40 transition-all duration-300" :class="$clicks >= 2 ? 'opacity-40' : 'opacity-0'">↓</div>

  <div v-click class="flex gap-4">
    <div class="bg-emerald-700 text-white px-4 py-2 rounded-xl font-bold shadow-lg border-2 border-emerald-500 text-center text-sm">
      <div class="text-xs opacity-70">📦</div>
      <div>TodoItem</div>
    </div>
    <div class="bg-emerald-700 text-white px-4 py-2 rounded-xl font-bold shadow-lg border-2 border-emerald-500 text-center text-sm">
      <div class="text-xs opacity-70">📦</div>
      <div>AddTodo</div>
    </div>
  </div>
</div>

---
clicks: 3
---

## ④ 상태 다이어그램

<div class="flex items-center justify-center gap-4 mt-8">
  <div class="w-4 h-4 rounded-full bg-white"></div>
  <div class="text-lg opacity-40">→</div>

  <div class="bg-blue-600 text-white px-5 py-3 rounded-full font-bold shadow-lg transition-all duration-300 text-sm" :class="$clicks === 0 ? 'ring-2 ring-blue-300 scale-105' : ''">
    idle
  </div>
  <div class="text-lg opacity-40">→</div>

  <div class="bg-amber-500 text-black px-5 py-3 rounded-full font-bold shadow-lg transition-all duration-300 text-sm" :class="$clicks === 1 ? 'ring-2 ring-amber-300 scale-105' : 'opacity-40'" >
    loading
  </div>

  <div class="flex flex-col gap-2">
    <div class="flex items-center gap-2">
      <div class="text-lg opacity-40">→</div>
      <div class="bg-green-500 text-black px-5 py-3 rounded-full font-bold shadow-lg transition-all duration-300 text-sm" :class="$clicks === 2 ? 'ring-2 ring-green-300 scale-105' : 'opacity-40'">
        success
      </div>
    </div>
    <div class="flex items-center gap-2">
      <div class="text-lg opacity-40">→</div>
      <div class="bg-red-500 text-white px-5 py-3 rounded-full font-bold shadow-lg transition-all duration-300 text-sm" :class="$clicks === 3 ? 'ring-2 ring-red-300 scale-105' : 'opacity-40'">
        error
      </div>
    </div>
  </div>
</div>

<div class="text-center mt-6 text-sm">
  <span class="transition-all duration-300" :class="$clicks === 0 ? 'text-blue-400 font-bold' : 'opacity-40'">대기</span>
  <span class="mx-2 opacity-30">→</span>
  <span class="transition-all duration-300" :class="$clicks === 1 ? 'text-amber-400 font-bold' : 'opacity-40'">로딩</span>
  <span class="mx-2 opacity-30">→</span>
  <span class="transition-all duration-300" :class="$clicks === 2 ? 'text-green-400 font-bold' : 'opacity-40'">성공</span>
  <span class="mx-1 opacity-30">/</span>
  <span class="transition-all duration-300" :class="$clicks === 3 ? 'text-red-400 font-bold' : 'opacity-40'">에러</span>
</div>

---

## ⑤ 유스케이스 다이어그램

<div class="flex gap-12 items-center justify-center mt-6">
  <div v-click class="text-center">
    <div class="text-5xl">🧑‍💻</div>
    <div class="text-sm font-bold mt-2">개발자</div>
  </div>

  <div class="flex flex-col gap-3">
    <div v-click class="bg-slate-800 border-2 border-blue-500 rounded-full px-6 py-2 text-sm text-center shadow-lg">
      코드 작성
    </div>
    <div v-click class="bg-slate-800 border-2 border-blue-500 rounded-full px-6 py-2 text-sm text-center shadow-lg">
      타입 정의
    </div>
    <div v-click class="bg-slate-800 border-2 border-green-500 rounded-full px-6 py-2 text-sm text-center shadow-lg">
      컴파일 확인
    </div>
    <div v-click class="bg-slate-800 border-2 border-amber-500 rounded-full px-6 py-2 text-sm text-center shadow-lg">
      디버깅
    </div>
  </div>

  <div v-click class="bg-slate-800/50 border border-slate-600 rounded-2xl px-6 py-8 text-center">
    <div class="text-xs opacity-50 mb-2">System</div>
    <div class="font-bold text-sm">TypeScript<br/>Compiler</div>
  </div>
</div>

---

## ⑥ 패키지/모듈 다이어그램

<div class="grid grid-cols-3 gap-4 mt-6">
  <div v-click class="bg-slate-800 rounded-xl border border-blue-500 p-4 shadow-lg">
    <div class="flex items-center gap-2 mb-3">
      <div class="bg-blue-600 text-white text-xs px-2 py-0.5 rounded font-bold">📁 components/</div>
    </div>
    <div class="space-y-1.5 text-xs">
      <div class="bg-slate-900 rounded px-2 py-1.5">Header.tsx</div>
      <div class="bg-slate-900 rounded px-2 py-1.5">TodoList.tsx</div>
      <div class="bg-slate-900 rounded px-2 py-1.5">TodoItem.tsx</div>
      <div class="bg-slate-900 rounded px-2 py-1.5">AddTodo.tsx</div>
    </div>
  </div>

  <div v-click class="bg-slate-800 rounded-xl border border-emerald-500 p-4 shadow-lg">
    <div class="flex items-center gap-2 mb-3">
      <div class="bg-emerald-600 text-white text-xs px-2 py-0.5 rounded font-bold">📁 hooks/</div>
    </div>
    <div class="space-y-1.5 text-xs">
      <div class="bg-slate-900 rounded px-2 py-1.5">useTodos.ts</div>
      <div class="bg-slate-900 rounded px-2 py-1.5">useFilter.ts</div>
      <div class="bg-slate-900 rounded px-2 py-1.5">useApi.ts</div>
    </div>
  </div>

  <div v-click class="bg-slate-800 rounded-xl border border-amber-500 p-4 shadow-lg">
    <div class="flex items-center gap-2 mb-3">
      <div class="bg-amber-600 text-white text-xs px-2 py-0.5 rounded font-bold">📁 types/</div>
    </div>
    <div class="space-y-1.5 text-xs">
      <div class="bg-slate-900 rounded px-2 py-1.5">Todo.ts</div>
      <div class="bg-slate-900 rounded px-2 py-1.5">User.ts</div>
      <div class="bg-slate-900 rounded px-2 py-1.5">Api.ts</div>
    </div>
  </div>
</div>

<div v-click class="flex justify-center gap-8 mt-4 text-xs">
  <span class="text-blue-400">components/ → hooks/ <span class="opacity-50">(import)</span></span>
  <span class="text-emerald-400">hooks/ → types/ <span class="opacity-50">(import)</span></span>
  <span class="text-amber-400">components/ → types/ <span class="opacity-50">(import)</span></span>
</div>
