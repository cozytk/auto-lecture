---
theme: default
title: 다이어그램 애니메이션 종합 테스트
---

# 다이어그램 애니메이션 종합 테스트

복잡한 상황별 패턴 검증

---
clicks: 4
---

## ① 선형 흐름 — 빌드업 + 포커스

<div class="flex items-center justify-center gap-2 mt-12">
  <div class="bg-blue-600 text-white px-5 py-4 rounded-xl text-center font-bold shadow-lg transition-all duration-300" :class="$clicks === 0 ? 'ring-2 ring-blue-300 scale-105' : $clicks >= 4 ? 'opacity-100' : 'opacity-40'">
    <div class="text-xs opacity-70">.ts</div>
    <div>TypeScript</div>
  </div>
  <div class="text-xl transition-all duration-300" :class="$clicks >= 1 ? 'opacity-50' : 'opacity-0'">→</div>
  <div class="bg-yellow-500 text-black px-5 py-4 rounded-xl text-center font-bold shadow-lg transition-all duration-500" :class="$clicks >= 1 ? ($clicks === 1 ? 'ring-2 ring-yellow-300 scale-105' : $clicks >= 4 ? 'opacity-100' : 'opacity-40') : 'opacity-0'">
    <div class="text-xs opacity-70">tsc</div>
    <div>컴파일</div>
  </div>
  <div class="text-xl transition-all duration-300" :class="$clicks >= 2 ? 'opacity-50' : 'opacity-0'">→</div>
  <div class="bg-amber-400 text-black px-5 py-4 rounded-xl text-center font-bold shadow-lg transition-all duration-500" :class="$clicks >= 2 ? ($clicks === 2 ? 'ring-2 ring-amber-300 scale-105' : $clicks >= 4 ? 'opacity-100' : 'opacity-40') : 'opacity-0'">
    <div class="text-xs opacity-70">.js</div>
    <div>JavaScript</div>
  </div>
  <div class="text-xl transition-all duration-300" :class="$clicks >= 3 ? 'opacity-50' : 'opacity-0'">→</div>
  <div class="bg-cyan-400 text-black px-5 py-4 rounded-xl text-center font-bold shadow-lg transition-all duration-500" :class="$clicks >= 3 ? ($clicks === 3 ? 'ring-2 ring-cyan-300 scale-105' : $clicks >= 4 ? 'opacity-100' : 'opacity-40') : 'opacity-0'">
    <div class="text-xs opacity-70">실행</div>
    <div>브라우저</div>
  </div>
</div>

<div class="text-center mt-6 text-green-400 font-bold transition-all duration-500" :class="$clicks >= 4 ? 'opacity-100' : 'opacity-0'">
  ✅ 전체 파이프라인 완성
</div>

---

## ② N×M 문제 — 점진적 연결 증가

<div class="mt-6">
  <div class="flex justify-center gap-16">
    <div class="flex flex-col gap-2 items-center">
      <div class="text-xs opacity-50 mb-1">AI 앱</div>
      <div class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg">Claude</div>
      <div class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg transition-all duration-500" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">GPT</div>
      <div class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg transition-all duration-500" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Cursor</div>
    </div>
    <div class="flex flex-col gap-2 items-center">
      <div class="text-xs opacity-50 mb-1">도구</div>
      <div class="bg-emerald-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg">GitHub</div>
      <div class="bg-emerald-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg transition-all duration-500" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Slack</div>
      <div class="bg-emerald-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg transition-all duration-500" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">DB</div>
    </div>
  </div>

  <div class="text-center mt-4 transition-all duration-500">
    <div class="text-sm">1 앱 × 1 도구 = <strong class="text-yellow-400">1개</strong> 어댑터</div>
    <div v-click class="text-sm mt-1">2 앱 × 2 도구 = <strong class="text-orange-400">4개</strong> 어댑터</div>
    <div v-click class="text-lg mt-1 font-bold text-red-400">3 앱 × 3 도구 = 9개 어댑터 — 폭발적 증가!</div>
  </div>
</div>

---

## ③ N+M 해결 — MCP 등장

<div class="mt-6 flex justify-center items-center gap-6">
  <div class="flex flex-col gap-2 items-center">
    <div class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg">Claude</div>
    <div class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg">GPT</div>
    <div class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg">Cursor</div>
  </div>

  <div class="flex flex-col items-center gap-1">
    <div class="text-sm opacity-40">→</div>
    <div class="text-sm opacity-40">→</div>
    <div class="text-sm opacity-40">→</div>
  </div>

  <div v-click class="bg-green-500 text-black px-6 py-6 rounded-2xl font-bold shadow-xl text-center ring-2 ring-green-300">
    <div class="text-xs opacity-70">표준 프로토콜</div>
    <div class="text-xl">MCP</div>
  </div>

  <div v-click class="flex flex-col items-center gap-1">
    <div class="text-sm opacity-40">→</div>
    <div class="text-sm opacity-40">→</div>
    <div class="text-sm opacity-40">→</div>
  </div>

  <div v-click class="flex flex-col gap-2 items-center">
    <div class="bg-emerald-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg">GitHub</div>
    <div class="bg-emerald-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg">Slack</div>
    <div class="bg-emerald-600 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg">DB</div>
  </div>
</div>

<div v-click class="text-center mt-4">
  <span class="text-green-400 font-bold text-lg">3 + 3 = 6개</span>
  <span class="text-sm opacity-70"> 구현 — USB처럼 하나의 표준으로 연결</span>
</div>

---

## ④ 아키텍처 — 3단 레이어 빌드업

<div class="flex flex-col items-center gap-4 mt-6">
  <div class="bg-indigo-700 text-white px-12 py-4 rounded-2xl font-bold shadow-xl text-center transition-all duration-500" :class="$clicks === 0 ? 'ring-2 ring-indigo-400 scale-105' : ''">
    <div class="text-sm opacity-70">Layer 3 — 호스트</div>
    <div class="text-xl">AI 앱 (Claude Desktop)</div>
    <div class="flex gap-3 mt-2 justify-center">
      <div class="bg-indigo-500/50 px-3 py-1 rounded text-xs">MCP Client 1</div>
      <div class="bg-indigo-500/50 px-3 py-1 rounded text-xs">MCP Client 2</div>
    </div>
  </div>

  <div class="flex gap-8 text-sm transition-all duration-300" :class="$clicks >= 1 ? 'opacity-50' : 'opacity-0'">
    <span>↕ stdio</span>
    <span>↕ SSE</span>
  </div>

  <div v-click class="flex gap-4">
    <div class="bg-emerald-600 text-white px-6 py-3 rounded-xl font-bold shadow-lg text-center transition-all duration-300" :class="$clicks === 1 ? 'ring-2 ring-emerald-400 scale-105' : ''">
      <div class="text-xs opacity-70">로컬</div>
      <div>파일시스템 서버</div>
    </div>
    <div class="bg-emerald-600 text-white px-6 py-3 rounded-xl font-bold shadow-lg text-center transition-all duration-300" :class="$clicks === 1 ? 'ring-2 ring-emerald-400 scale-105' : ''">
      <div class="text-xs opacity-70">로컬</div>
      <div>GitHub 서버</div>
    </div>
    <div class="bg-amber-600 text-white px-6 py-3 rounded-xl font-bold shadow-lg text-center transition-all duration-300" :class="$clicks === 1 ? 'ring-2 ring-amber-400 scale-105' : ''">
      <div class="text-xs opacity-70">원격</div>
      <div>Slack 서버</div>
    </div>
  </div>

  <div class="flex gap-4 text-xs transition-all duration-300" :class="$clicks >= 2 ? 'opacity-40' : 'opacity-0'">
    <span>↕</span><span>↕</span><span>↕</span>
  </div>

  <div v-click class="flex gap-4">
    <div class="bg-slate-700 text-gray-300 px-5 py-2 rounded-lg text-sm shadow border border-slate-600">📁 로컬 파일</div>
    <div class="bg-slate-700 text-gray-300 px-5 py-2 rounded-lg text-sm shadow border border-slate-600">🔧 GitHub API</div>
    <div class="bg-slate-700 text-gray-300 px-5 py-2 rounded-lg text-sm shadow border border-slate-600">💬 Slack API</div>
  </div>
</div>

---

## ⑤ 분기 흐름 — 조건 분기

<div class="flex flex-col items-center gap-3 mt-8">
  <div class="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold shadow-lg transition-all duration-300" :class="$clicks === 0 ? 'ring-2 ring-blue-300 scale-105' : ''">
    TypeScript 코드
  </div>
  <div class="text-lg opacity-40 transition-all duration-300" :class="$clicks >= 1 ? 'opacity-50' : 'opacity-0'">↓ tsc 컴파일</div>

  <div v-click class="bg-yellow-500 text-black px-8 py-3 rounded-xl font-bold shadow-lg" :class="$clicks === 1 ? 'ring-2 ring-yellow-300 scale-105' : ''">
    타입 체크
  </div>

  <div class="flex gap-16 mt-2 transition-all duration-500" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">
    <div class="text-lg opacity-40">↙</div>
    <div class="text-lg opacity-40">↘</div>
  </div>

  <div v-click class="flex gap-8">
    <div class="bg-red-500 text-white px-6 py-3 rounded-xl font-bold shadow-lg text-center">
      <div class="text-xs opacity-70">❌ 실패</div>
      <div>컴파일 에러</div>
    </div>
    <div class="bg-green-500 text-black px-6 py-3 rounded-xl font-bold shadow-lg text-center">
      <div class="text-xs opacity-70">✅ 성공</div>
      <div>JS 빌드</div>
    </div>
  </div>
</div>

---
clicks: 3
---

## ⑥ 양방향 통신 — 요청/응답 쌍

<div class="flex items-center justify-center gap-8 mt-12">
  <div class="bg-indigo-600 text-white px-8 py-6 rounded-2xl font-bold shadow-xl text-center transition-all duration-300" :class="$clicks === 0 || $clicks === 3 ? 'ring-2 ring-indigo-300 scale-105' : 'opacity-60'">
    <div class="text-2xl">🧑‍💻</div>
    <div>클라이언트</div>
  </div>

  <div class="flex flex-col gap-3">
    <div class="flex items-center gap-2 transition-all duration-500" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">
      <span class="text-cyan-400 font-bold text-sm">요청</span>
      <span class="text-lg">→→→</span>
    </div>
    <div class="flex items-center gap-2 transition-all duration-500" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">
      <span class="text-lg">←←←</span>
      <span class="text-amber-400 font-bold text-sm">응답</span>
    </div>
  </div>

  <div class="bg-emerald-600 text-white px-8 py-6 rounded-2xl font-bold shadow-xl text-center transition-all duration-300" :class="$clicks === 1 || $clicks === 2 ? 'ring-2 ring-emerald-300 scale-105' : 'opacity-60'">
    <div class="text-2xl">🖥️</div>
    <div>서버</div>
  </div>
</div>

<div class="text-center mt-6 transition-all duration-500" :class="$clicks >= 3 ? 'opacity-100' : 'opacity-0'">
  <span class="text-green-400 font-bold">JSON-RPC 2.0</span> — 요청과 응답이 JSON으로 정형화
</div>

---
clicks: 4
---

## ⑦ 타임라인 — 기술 발전 과정

<div class="flex items-end justify-center gap-1 mt-12">
  <div class="flex flex-col items-center transition-all duration-500">
    <div class="bg-slate-600 text-white px-3 py-2 rounded-t-lg font-bold text-sm w-24 text-center shadow">CLI</div>
    <div class="bg-slate-700 w-24 h-20 rounded-b-lg"></div>
    <div class="text-xs opacity-50 mt-1">~2023</div>
  </div>
  <div class="flex flex-col items-center transition-all duration-500" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">
    <div class="bg-blue-600 text-white px-3 py-2 rounded-t-lg font-bold text-sm w-24 text-center shadow">Function<br/>Calling</div>
    <div class="bg-blue-700 w-24 h-32 rounded-b-lg"></div>
    <div class="text-xs opacity-50 mt-1">2023</div>
  </div>
  <div class="flex flex-col items-center transition-all duration-500" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">
    <div class="bg-purple-600 text-white px-3 py-2 rounded-t-lg font-bold text-sm w-24 text-center shadow">MCP<br/>출시</div>
    <div class="bg-purple-700 w-24 h-44 rounded-b-lg"></div>
    <div class="text-xs opacity-50 mt-1">2024.11</div>
  </div>
  <div class="flex flex-col items-center transition-all duration-500" :class="$clicks >= 3 ? 'opacity-100' : 'opacity-0'">
    <div class="bg-green-600 text-white px-3 py-2 rounded-t-lg font-bold text-sm w-24 text-center shadow">빅테크<br/>채택</div>
    <div class="bg-green-700 w-24 h-56 rounded-b-lg"></div>
    <div class="text-xs opacity-50 mt-1">2025</div>
  </div>
  <div class="flex flex-col items-center transition-all duration-500" :class="$clicks >= 4 ? 'opacity-100' : 'opacity-0'">
    <div class="bg-amber-500 text-black px-3 py-2 rounded-t-lg font-bold text-sm w-24 text-center shadow">Linux<br/>Foundation</div>
    <div class="bg-amber-600 w-24 h-64 rounded-b-lg"></div>
    <div class="text-xs opacity-50 mt-1">2025.12</div>
  </div>
</div>

---

## ⑧ 3열 카드 — 순차 공개

<div class="grid grid-cols-3 gap-6 mt-6">
  <div v-click class="bg-slate-800/50 rounded-xl p-5 border border-slate-700 transition-all duration-500">
    <div class="text-center">
      <div class="text-4xl mb-3">🔧</div>
      <div class="text-xl font-bold">Tools</div>
      <div class="text-sm opacity-70 mt-2">AI가 <strong class="text-cyan-400">호출</strong>하는 함수</div>
    </div>
    <div class="mt-4 text-xs space-y-2">
      <div class="bg-slate-900 rounded-lg px-3 py-2"><code>search_issues</code></div>
      <div class="bg-slate-900 rounded-lg px-3 py-2"><code>send_message</code></div>
      <div class="bg-slate-900 rounded-lg px-3 py-2"><code>run_query</code></div>
    </div>
    <div class="text-xs opacity-40 text-center mt-3">AI가 능동적으로 실행</div>
  </div>
  <div v-click class="bg-slate-800/50 rounded-xl p-5 border border-slate-700 transition-all duration-500">
    <div class="text-center">
      <div class="text-4xl mb-3">📄</div>
      <div class="text-xl font-bold">Resources</div>
      <div class="text-sm opacity-70 mt-2">AI가 <strong class="text-cyan-400">읽는</strong> 데이터</div>
    </div>
    <div class="mt-4 text-xs space-y-2">
      <div class="bg-slate-900 rounded-lg px-3 py-2">파일 내용</div>
      <div class="bg-slate-900 rounded-lg px-3 py-2">DB 스키마</div>
      <div class="bg-slate-900 rounded-lg px-3 py-2">API 응답 캐시</div>
    </div>
    <div class="text-xs opacity-40 text-center mt-3">AI가 참조만 함 (읽기전용)</div>
  </div>
  <div v-click class="bg-slate-800/50 rounded-xl p-5 border border-slate-700 transition-all duration-500">
    <div class="text-center">
      <div class="text-4xl mb-3">💬</div>
      <div class="text-xl font-bold">Prompts</div>
      <div class="text-sm opacity-70 mt-2">미리 정의된 <strong class="text-cyan-400">템플릿</strong></div>
    </div>
    <div class="mt-4 text-xs space-y-2">
      <div class="bg-slate-900 rounded-lg px-3 py-2">"코드 리뷰해줘"</div>
      <div class="bg-slate-900 rounded-lg px-3 py-2">"로그 분석해줘"</div>
      <div class="bg-slate-900 rounded-lg px-3 py-2">"SQL 생성해줘"</div>
    </div>
    <div class="text-xs opacity-40 text-center mt-3">사용자가 선택하여 활용</div>
  </div>
</div>
