---
theme: default
title: AI Agent 전문 개발 과정 - Day 1
transition: slide-left
mdc: true
---

# AI Agent 전문 개발 과정

## Day 1: Agent 문제 정의에서 아키텍처 선택까지

<div class="mt-8 text-lg text-gray-500">
Session 1: Agent 문제 정의와 과제 도출<br>
Session 2: LLM 동작 원리 및 프롬프트 전략 심화<br>
Session 3: Agent 기획서 구조화<br>
Session 4: Tool Use · RAG · Hybrid 구조 판단
</div>

<!--
[스크립트]
안녕하세요, AI Agent 전문 개발 과정에 오신 것을 환영합니다. 오늘 Day 1에서는 Agent가 무엇인지, 어떤 문제에 적합한지, 어떻게 설계하는지, 그리고 어떤 아키텍처를 선택해야 하는지까지 전체 흐름을 다룹니다. 총 4개 세션으로 구성되어 있습니다.

전환: 첫 번째 세션을 시작하겠습니다.
시간: 1분
-->

<style>
:global(.slidev-layout.two-cols-header) {
  column-gap: 2rem !important;
}
:global(.slidev-layout.two-cols) {
  column-gap: 2rem !important;
}
</style>


---
layout: section
transition: fade
---

# Session 1
## Agent 문제 정의와 과제 도출

<!--
[스크립트]
안녕하세요. 오늘 첫 번째 세션에 오신 것을 환영합니다. 이 세션에서는 AI Agent를 실제로 만들기 전에, 반드시 먼저 물어야 할 질문들을 다룹니다. "이 문제가 정말 Agent가 필요한가?", "어떻게 문제를 분해해야 하는가?", "RAG와 Agent 중 어떤 것을 선택해야 하는가?" 이 세 가지 핵심 질문을 2시간 동안 함께 탐구하겠습니다.

[Q&A 대비]
Q: 이 세션에서 코딩은 없나요?
A: 개념 세션이지만 코드 예제가 포함됩니다. 실제 구현은 이후 세션에서 다룹니다.

전환: 첫 번째 주제로 바로 들어가겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# 이 세션에서 배울 것

<v-clicks>

- Agent가 적합한 문제 유형 vs 부적합한 문제 유형
- Pain → Task → Skill → Tool 프레임워크
- 업무 유형별 Agent 패턴 (자동화형 / 분석형 / 계획형)
- RAG vs Agent 판단 기준

</v-clicks>

<div v-click class="mt-8 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

<strong>세션 목표</strong>: 도구를 선택하기 전에, 문제를 올바르게 정의하는 능력을 갖춘다

</div>

<!--
[스크립트]
오늘 세션은 크게 네 개의 주제로 구성됩니다. [클릭] 첫 번째는 Agent가 적합한 문제 유형을 구분하는 방법입니다. [클릭] 두 번째는 Pain에서 출발해서 Tool까지 내려가는 설계 프레임워크입니다. [클릭] 세 번째는 Agent를 유형별로 분류하는 패턴입니다. [클릭] 네 번째는 RAG와 Agent 중 어떤 것을 선택해야 하는지 판단 기준입니다. [클릭] 이 모든 것의 핵심은 도구를 먼저 정하지 않고, 문제를 먼저 제대로 정의하는 것입니다.

[Q&A 대비]
Q: 왜 개념부터 시작하나요? 바로 코딩하면 안 되나요?
A: Agent 개발에서 가장 비싼 실수는 잘못된 설계를 코딩으로 구현하는 것입니다. 개념을 먼저 다지면 이후 구현이 훨씬 빠르고 정확해집니다.

전환: 첫 번째 주제, Agent가 적합한 문제 유형부터 시작하겠습니다.
시간: 2분
-->

---
layout: section
transition: fade
---

# 1. Agent가 적합한 문제 유형

<!--
[스크립트]
첫 번째 주제입니다. Agent라는 단어가 익숙해진 지금도 모든 문제에 Agent가 맞는 것은 아닙니다. 잘못 적용하면 단순 스크립트로 풀 수 있는 문제에 불필요한 복잡성만 추가됩니다. 그래서 Agent를 만들기 전에 반드시 먼저 이 질문을 던져야 합니다.

[Q&A 대비]
Q: Agent 도입 실패 사례가 많다고 하는데 구체적으로 어떤 경우인가요?
A: 가장 흔한 케이스는 단순 FAQ 답변에 Agent를 적용한 경우입니다. 고정된 질문-답변이면 RAG로 충분한데, Agent를 붙이면 비용이 10배 이상 늘고 응답도 느려집니다.

전환: 그렇다면 어떤 문제가 Agent에 적합한지 알아보겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# Agent를 만들기 전에 먼저 물어야 할 질문

<div class="flex items-center justify-center h-60">
  <div v-motion :initial="{ scale: 0.8, opacity: 0 }" :enter="{ scale: 1, opacity: 1 }" class="text-center bg-amber-50 dark:bg-amber-900/30 rounded-xl p-8 border-2 border-amber-300">
    <div class="text-3xl font-bold text-amber-700 dark:text-amber-300 mb-4">"이 문제가 정말 Agent가 필요한가?"</div>
    <div class="text-lg text-gray-600 dark:text-gray-300">도구를 정하기 전에 문제를 먼저 정의하라</div>
  </div>
</div>

<!--
[스크립트]
이것이 이 세션 전체를 관통하는 핵심 질문입니다. "이 문제가 정말 Agent가 필요한가?" Agent는 강력하지만 비용과 복잡성이 따릅니다. LLM을 호출할 때마다 비용이 발생하고, 응답 시간도 길어집니다. 그러니 Agent가 반드시 필요한 경우에만 써야 합니다. [잠깐 멈춤] 여러분이 지금 생각하고 있는 프로젝트가 있다면, 이 질문을 한번 스스로 던져보세요.

[Q&A 대비]
Q: 나중에 Agent로 업그레이드할 생각으로 처음부터 Agent로 만들면 안 되나요?
A: 과잉 설계입니다. 단순한 것으로 시작해서 필요할 때 복잡도를 높이는 것이 엔지니어링의 기본 원칙입니다.

전환: 그렇다면 어떤 기준으로 판단할까요?
시간: 2분
-->

---
layout: two-cols-header
transition: slide-left
---

# 전통적 자동화 vs AI Agent

::left::

<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-5 h-64 overflow-hidden">

**전통적 자동화**
(스크립트, ETL, 크론잡)

<v-clicks>

- 사전 정의된 **고정 경로** 실행
- 입력이 같으면 **항상 같은 결과**
- 분기가 코드에 **하드코딩**

</v-clicks>

</div>

::right::

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-5 h-64 overflow-hidden">

**AI Agent**

<v-clicks>

- 중간 결과를 **관찰**
- 다음 행동을 **동적으로 결정**
- **Observe → Think → Act** 루프

</v-clicks>

</div>

<!--
[스크립트]
전통적 자동화와 AI Agent의 핵심 차이를 살펴보겠습니다. [클릭] 전통적 자동화는 사전에 정의된 고정 경로를 실행합니다. [클릭] 입력이 같으면 항상 같은 결과가 나옵니다. [클릭] 모든 분기 조건이 코드에 하드코딩되어 있습니다. 반면 AI Agent는요. [클릭] 중간 결과를 관찰합니다. [클릭] 그 결과를 바탕으로 다음 행동을 동적으로 결정합니다. [클릭] 이것이 Observe, Think, Act 루프입니다. 핵심은 "판단"이 코드가 아니라 LLM이 한다는 것입니다.

[Q&A 대비]
Q: ETL 파이프라인에도 분기 로직이 있는데, 그것과 Agent의 차이는 뭔가요?
A: ETL의 분기는 개발자가 미리 모든 케이스를 정의합니다. Agent는 개발자가 정의하지 않은 새로운 상황에서도 LLM이 판단할 수 있습니다.

전환: 그럼 구체적으로 어떤 조건이 갖춰져야 Agent가 필요한지 보겠습니다.
시간: 3분
-->

---
layout: two-cols-header
transition: slide-left
---

# Agent 적합 vs 부적합 판단

::left::

<div class="text-center font-bold text-blue-600 dark:text-blue-400 mb-3 text-lg">✅ Agent가 필요한 경우</div>

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 mb-2">
  <strong class="text-blue-700 dark:text-blue-300">① 멀티스텝</strong><br>
  <span class="text-sm">2단계 이상 순차적 과정 요구</span>
</div>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 mb-2">
  <strong class="text-blue-700 dark:text-blue-300">② 동적 판단</strong><br>
  <span class="text-sm">중간 결과에 따라 다음 행동 변경</span>
</div>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3">
  <strong class="text-blue-700 dark:text-blue-300">③ 도구 활용</strong><br>
  <span class="text-sm">외부 API·DB·파일 시스템 상호작용</span>
</div>

</v-clicks>

::right::

<div class="text-center font-bold text-red-600 dark:text-red-400 mb-3 text-lg">❌ Agent가 부적합한 경우</div>

<v-clicks>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3 mb-2">
  <strong class="text-red-700 dark:text-red-300">단순 변환</strong><br>
  <span class="text-sm">판단 불필요 → 함수 하나로 충분</span>
</div>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3 mb-2">
  <strong class="text-red-700 dark:text-red-300">단일 질의응답</strong><br>
  <span class="text-sm">멀티스텝 없음 → LLM 단일 호출</span>
</div>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3">
  <strong class="text-red-700 dark:text-red-300">실시간 제어</strong><br>
  <span class="text-sm">지연 허용 불가 → LLM 응답 너무 느림</span>
</div>

</v-clicks>

<!--
[스크립트]
Agent가 적합한 경우와 부적합한 경우를 한눈에 비교해보겠습니다.

[클릭] 왼쪽부터 보겠습니다. 첫 번째 조건은 멀티스텝입니다. 작업이 2단계 이상의 순차적 과정을 요구해야 합니다. "데이터 수집 → 분석 → 보고서 생성"처럼요. 단일 API 호출이면 함수 하나로 충분합니다.

[클릭] 두 번째, 동적 판단입니다. 중간 결과에 따라 다음 행동이 달라져야 합니다. 분기 조건이 사전에 모두 정해져 있다면 if-else로 충분합니다.

[클릭] 세 번째, 도구 활용입니다. LLM만으로는 실세계에 영향을 줄 수 없습니다. 외부 API, DB, 파일 시스템과 상호작용이 필요할 때입니다.

이제 오른쪽, 부적합한 경우입니다.

[클릭] 단순 변환입니다. 날짜 형식 변환처럼 판단이 필요 없는 작업은 함수 하나면 됩니다.

[클릭] 단일 질의응답입니다. FAQ 답변처럼 멀티스텝이 없는 작업은 LLM 단일 호출로 충분합니다.

[클릭] 실시간 제어입니다. 긴급 차단 같은 지연 허용 불가 상황에서 LLM 응답 시간은 너무 깁니다.

[Q&A 대비]
Q: 3가지 조건을 모두 만족해야 Agent인가요?
A: 일반적으로 셋 다 만족할수록 적합합니다. 실무에서는 ①과 ②만 만족해도 Agent를 선택하는 경우가 많습니다.

Q: FAQ는 RAG가 맞나요?
A: 그렇습니다. 고정된 지식 기반에서 검색·답변하는 것은 RAG가 적합합니다. Agent는 단순 질의응답보다 훨씬 무거운 도구입니다.

전환: RPA와 비교해서 차이를 살펴보겠습니다.
시간: 5분
-->

---
layout: two-cols-header
transition: slide-left
---

# RPA vs AI Agent

::left::

<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 h-52 overflow-hidden">

**RPA** (Robotic Process Automation)

<v-clicks>

- UI 수준 **클릭/입력 재현**
- **고정 규칙** 의존
- UI 변경 시 **즉시 깨짐**
- LLM 비용 없음

</v-clicks>

</div>

::right::

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 h-52 overflow-hidden">

**AI Agent**

<v-clicks>

- API 수준 **동적 판단**
- **LLM 기반** 유연한 판단
- UI 변경 시 **영향 없음**
- LLM 호출 비용 발생

</v-clicks>

</div>

<!--
[스크립트]
RPA와 AI Agent를 비교해보겠습니다. [클릭] RPA는 UI 수준에서 클릭과 입력을 재현합니다. [클릭] 개발자가 사전에 정의한 고정 규칙을 따릅니다. [클릭] 따라서 화면 UI가 조금만 바뀌어도 즉시 깨집니다. [클릭] 반면 LLM 호출이 없으니 비용이 낮습니다. 반면 AI Agent는요. [클릭] API 수준에서 동적으로 판단합니다. [클릭] LLM이 상황을 보고 유연하게 판단합니다. [클릭] UI가 아닌 API를 통하니 UI 변경의 영향을 받지 않습니다. [클릭] 단, LLM 호출 비용이 발생합니다.

[Q&A 대비]
Q: RPA를 쓰고 있는데 AI Agent로 교체해야 하나요?
A: 반드시 그렇지는 않습니다. UI가 안정적이고, 규칙이 고정되어 있고, 판단이 필요 없다면 RPA가 더 적합하고 저렴합니다. "판단이 필요한 분기"가 생길 때 Agent를 고려하세요.

전환: 이제 Agent를 적합하게 판별하는 연습을 해보겠습니다.
시간: 3분
-->

---
transition: slide-left
---

# [Q] 퀴즈: 어떤 업무가 Agent에 적합한가?

<div class="mb-4 text-lg font-medium">다음 중 AI Agent가 가장 적합한 업무는?</div>

<div v-click="1" class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2"><strong>①</strong> CSV 파일 1000개의 컬럼명을 일괄 변경</div>

<div class="relative mb-2">
<div v-click="2" class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3"><strong>②</strong> 고객 리뷰를 분석하여 제품별 개선점을 도출하고 Jira 티켓 생성</div>
<div v-click="5" class="absolute inset-0 z-10 bg-green-50 dark:bg-green-900 border-2 border-green-400 rounded-lg p-3"><strong>② 정답!</strong> 고객 리뷰를 분석하여 제품별 개선점을 도출하고 Jira 티켓 생성</div>
</div>

<div v-click="3" class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2"><strong>③</strong> 사내 위키에서 특정 키워드로 문서 검색</div>

<div v-click="4" class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3"><strong>④</strong> 매일 9시에 서버 상태를 Slack으로 알림</div>

<div v-click="5" class="mt-4 text-sm">
①은 스크립트, ③은 RAG, ④는 크론잡으로 충분
</div>

<!--
[스크립트]
퀴즈를 풀어보겠습니다. 방금 배운 Agent의 3가지 조건을 기준으로 생각해보세요. [잠깐 멈춤] 30초 드리겠습니다. [클릭] 보기를 하나씩 살펴볼게요. [클릭] 1번, CSV 컬럼명 일괄 변경입니다. 판단이 필요 없고 단순 변환이니 스크립트가 적합합니다. [클릭] 2번, 고객 리뷰 분석 후 Jira 티켓 생성입니다. 분석이라는 동적 판단, 여러 단계, Jira API 호출까지 3가지 조건 모두 만족합니다. [클릭] 3번, 키워드로 문서 검색입니다. 이건 RAG가 적합합니다. [클릭] 4번, 서버 상태 알림입니다. 크론잡 + 스크립트면 충분합니다. [클릭] 정답은 2번입니다.

[Q&A 대비]
Q: 3번이 Agent가 될 수도 있지 않나요?
A: 단순 검색이면 RAG입니다. 하지만 "검색 후 발견된 문제를 자동으로 Jira에 등록"까지 한다면 Agent가 됩니다. 쓰기 작업이 추가되는 순간 Agent 영역입니다.

전환: 다음은 실제로 어떻게 문제를 설계하는지, 프레임워크를 배워보겠습니다.
시간: 4분
-->

---
layout: section
transition: fade
---

# 2. Pain → Task → Skill → Tool 프레임워크

<!--
[스크립트]
두 번째 주제입니다. Agent가 필요하다고 판단했다면, 이제 어떻게 설계를 시작해야 할까요? 가장 흔한 실수는 도구부터 정하고 문제를 끼워 맞추는 것입니다. "최신 LLM API가 있으니까 뭔가 만들어보자"는 식이죠. 이런 접근은 기술 데모로는 끝나기 쉽지만 실제 비즈니스 가치로 연결되기 어렵습니다.

[Q&A 대비]
Q: 해커톤이나 프로토타입에서는 Tool-first가 더 빠르지 않나요?
A: 맞습니다. 빠른 프로토타이핑에서는 Tool-first가 유효할 수 있습니다. 하지만 프로덕션 개발에서는 반드시 Pain-first로 접근해야 비즈니스 가치를 보장할 수 있습니다.

전환: 올바른 설계 순서를 알아보겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# 왜 Pain에서 시작해야 하는가

<div class="grid grid-cols-[6fr_4fr] gap-6">
<div>

<v-clicks>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-4 mb-3">
  <div class="font-bold text-red-700 dark:text-red-300">Tool-first (잘못된 접근)</div>
  <div class="text-sm mt-1">"최신 LLM API가 있으니 뭔가를 만들어보자"</div>
  <div class="text-sm mt-1">→ 기술 데모로 끝남, 비즈니스 가치 없음</div>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
  <div class="font-bold text-green-700 dark:text-green-300">Pain-first (올바른 접근)</div>
  <div class="text-sm mt-1">"주당 5시간 낭비되는 이 작업을 어떻게 없앨까?"</div>
  <div class="text-sm mt-1">→ 가치 검증 후 최적의 기술 선택</div>
</div>

</v-clicks>

</div>
<div class="flex items-center justify-center">
  <div v-click class="text-center">
    <div class="text-5xl mb-2">🔨</div>
    <div class="text-sm text-gray-500 italic">"망치를 들면 모든 것이 못으로 보인다"</div>
  </div>
</div>
</div>

<!--
[스크립트]
Tool-first와 Pain-first를 비교해보겠습니다. [클릭] Tool-first 접근은 "최신 LLM API가 있으니 뭔가 만들어보자"에서 시작합니다. 결과는 기술 데모로 끝나고 실제 비즈니스 가치를 만들지 못합니다. [클릭] 반면 Pain-first 접근은 "주당 5시간이 이 작업에 낭비된다, 어떻게 없앨까?"에서 시작합니다. 비즈니스 가치를 먼저 검증한 후 최적의 기술을 선택합니다. [클릭] 이것이 바로 "망치를 들면 모든 것이 못으로 보인다"는 함정입니다. Vector DB를 갖고 있으면 모든 문제에 RAG를 적용하게 됩니다.

[Q&A 대비]
Q: 기술을 먼저 배워야 Pain을 발견할 수 있지 않나요?
A: 기술을 이해하는 것과 기술로 시작하는 것은 다릅니다. 기술을 이해한 상태에서 Pain을 발견하고, 그 Pain에 적합한 기술을 선택하는 것이 올바른 순서입니다.

전환: 4단계 프레임워크를 구체적으로 살펴보겠습니다.
시간: 3분
-->

---
transition: slide-left
---

# Pain → Task → Skill → Tool 4단계

<v-clicks>

<div class="flex items-start gap-4 mb-3">
  <div class="bg-red-500 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold shrink-0">P</div>
  <div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3 flex-1">
    <div class="font-bold">Pain (고통점)</div>
    <div class="text-sm mt-1">수치로 측정 가능한 비효율 — "불편하다" ❌ / "주당 5시간 소비" ✅</div>
  </div>
</div>

<div class="flex items-start gap-4 mb-3">
  <div class="bg-orange-500 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold shrink-0">T</div>
  <div class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-3 flex-1">
    <div class="font-bold">Task (작업)</div>
    <div class="text-sm mt-1">Pain에서 반복되는 동사를 추출 — "수집한다", "분류한다", "작성한다"</div>
  </div>
</div>

<div class="flex items-start gap-4 mb-3">
  <div class="bg-yellow-500 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold shrink-0">S</div>
  <div class="bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-3 flex-1">
    <div class="font-bold">Skill (능력)</div>
    <div class="text-sm mt-1">Task를 수행하기 위해 Agent가 갖춰야 할 능력 — 과도한 기능 추가 방지</div>
  </div>
</div>

<div class="flex items-start gap-4">
  <div class="bg-green-500 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold shrink-0">T</div>
  <div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 flex-1">
    <div class="font-bold">Tool (도구)</div>
    <div class="text-sm mt-1">Skill을 실현하는 구체적 기술 — LLM API, Vector DB, Slack API (항상 교체 가능해야 함)</div>
  </div>
</div>

</v-clicks>

<!--
[스크립트]
Pain-Task-Skill-Tool 4단계를 하나씩 설명하겠습니다. [클릭] Pain입니다. 수치로 측정 가능한 비효율이어야 합니다. "불편하다"는 Pain이 아닙니다. "매주 5시간을 보고서 작성에 쓴다"가 Pain입니다. [클릭] Task입니다. Pain에서 반복적으로 등장하는 동사를 추출합니다. "수집한다", "분류한다", "작성한다" 각각이 하나의 Task가 됩니다. [클릭] Skill입니다. 각 Task를 수행하기 위해 Agent가 갖춰야 할 능력입니다. 이 단계가 과도한 기능 추가를 방지합니다. 필요한 능력만 설계합니다. [클릭] Tool입니다. Skill을 실현하는 구체적인 기술 구현체입니다. LLM API, Vector DB, Slack API 등입니다. 중요한 것은 Tool은 항상 교체 가능해야 한다는 것입니다.

[Q&A 대비]
Q: Skill과 Tool의 구분이 모호한데요?
A: Skill은 능력이고 Tool은 구현체입니다. "자연어 이해"가 Skill이라면, "최신 LLM API 호출"이 Tool입니다. Skill은 Tool이 바뀌어도 유지됩니다.

전환: 실제 예시를 통해 확인해보겠습니다.
시간: 4분
-->

---
transition: slide-left
---

# 실전 예시: 주간 보고서 자동화

<div class="grid grid-cols-[5fr_5fr] gap-4">
<div>

**Pain** (측정 가능)
```
매주 금요일 보고서 작성 = 3시간
· Jira 티켓 정리
· Git 커밋 요약
· Slack 논의 정리
```

**Task** (동사 추출)
```
· Jira 티켓 수집 및 분류
· Git 커밋 요약
· Slack 논의 추출
· 보고서 종합 작성
```

</div>
<div>

**Skill** (능력)
```
· API 호출 능력
· 텍스트 요약 능력
· 정보 통합 능력
· 문서 생성 능력
```

**Tool** (구현체)
```
· Jira REST API
· GitHub API
· Slack API
· LLM API (요약/생성)
· Confluence API
```

</div>
</div>

<!--
[스크립트]
실전 예시입니다. 주간 보고서 자동화를 Pain-Task-Skill-Tool로 분해해보겠습니다. Pain은 "매주 금요일 보고서 작성에 3시간이 걸린다"입니다. 구체적인 수치가 있습니다. 여기서 Task를 뽑으면, "수집", "요약", "추출", "작성" 이렇게 4개의 동사가 Task가 됩니다. 각 Task에 필요한 Skill을 정리하면, API 호출 능력, 텍스트 요약 능력, 정보 통합 능력, 문서 생성 능력입니다. 마지막으로 Tool은 Jira API, GitHub API, Slack API, LLM API, Confluence API입니다. 이 순서로 설계하면 필요한 것만 정확하게 만들 수 있습니다.

[Q&A 대비]
Q: Tool을 선택할 때 어떤 기준으로 고르나요?
A: Skill을 구현할 수 있는 가장 단순하고 안정적인 Tool을 선택합니다. 가능하면 교체가 용이한 Tool을 선택합니다. LLM은 특히 공급업체 종속을 피해야 합니다.

전환: 이 프레임워크의 또 다른 가치, 이해관계자 소통을 살펴보겠습니다.
시간: 4분
-->

---
transition: slide-left
---

# 프레임워크의 또 다른 가치: 이해관계자 소통

<div class="grid grid-cols-[5fr_5fr] gap-6 mt-4">
<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-5 overflow-hidden">

**개발팀이 말하는 것**
<div class="text-sm mt-2 text-gray-600 dark:text-gray-300">
"Vector DB에 임베딩하고, RAG 파이프라인으로 retrieval하고, LLM으로 generation합니다."
</div>

</div>
<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-5 overflow-hidden">

**비즈니스팀이 말하는 것**
<div class="text-sm mt-2 text-gray-600 dark:text-gray-300">
"고객 불만 줄이고 싶어요. 응답 속도 개선도 필요하고요."
</div>

</div>
</div>

<div v-click class="mt-6 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

**Pain-Task-Skill-Tool 프레임워크**는 두 팀이 **같은 언어로 대화**하게 만드는 공통 구조다

- Pain: 비즈니스팀이 이해하는 언어
- Tool: 개발팀이 이해하는 언어
- Task/Skill: 두 팀이 함께 검증하는 중간 계층

</div>

<!--
[스크립트]
이 프레임워크의 또 다른 중요한 가치를 설명드리겠습니다. 개발팀과 비즈니스팀은 서로 다른 언어를 씁니다. 개발팀은 "Vector DB, RAG, 임베딩"을 말하고, 비즈니스팀은 "고객 불만, 응답 속도"를 말합니다. 서로가 무슨 말을 하는지 이해하지 못합니다. [클릭] Pain-Task-Skill-Tool 프레임워크가 해결책입니다. Pain은 비즈니스팀이 이해하는 언어입니다. Tool은 개발팀이 이해하는 언어입니다. 그 사이 Task와 Skill은 두 팀이 함께 검증할 수 있는 중간 계층입니다. 이 프레임워크를 사용하면 두 팀이 같은 구조에서 대화할 수 있습니다.

[Q&A 대비]
Q: 실제로 미팅에서 이 프레임워크를 쓸 때 어떻게 시작하나요?
A: 비즈니스팀에게 "지금 가장 시간이 많이 드는 반복 작업이 뭔가요?"라고 물어서 Pain을 수집합니다. 그 Pain을 화이트보드에 써놓고 함께 Task를 뽑아나가는 방식으로 진행합니다.

전환: 세 번째 주제로 넘어가겠습니다. Agent 패턴입니다.
시간: 3분
-->

---
layout: section
transition: fade
---

# 3. 업무 유형별 Agent 패턴

<!--
[스크립트]
세 번째 주제입니다. Agent를 백지 상태에서 설계하면 시행착오가 많습니다. 하지만 반복적으로 등장하는 패턴을 알면 설계를 크게 가속할 수 있습니다. 이것은 소프트웨어 디자인 패턴과 같은 개념입니다. GoF 패턴이 소프트웨어 설계를 가속하듯, Agent 패턴은 Agent 설계를 가속합니다.

[Q&A 대비]
Q: 패턴이 세 가지뿐인가요?
A: 이 세션에서는 가장 기본적인 3가지를 다룹니다. 실제로는 이 패턴들의 조합과 변형이 무수히 많습니다. 기본 패턴을 이해하면 변형을 이해하는 것은 훨씬 쉽습니다.

전환: 3가지 패턴을 하나씩 살펴보겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# 3가지 Agent 패턴

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 mb-3">
  <div class="flex items-center gap-3 mb-2">
    <div class="bg-blue-500 text-white rounded-full px-3 py-1 text-sm font-bold">자동화형</div>
    <div class="font-bold">Executor Agent</div>
  </div>
  <div class="text-sm">외부 이벤트(트리거)를 받아 일련의 작업을 자동 실행 — 핵심 가치: <strong>"반복 업무 대신 실행"</strong></div>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4 mb-3">
  <div class="flex items-center gap-3 mb-2">
    <div class="bg-green-500 text-white rounded-full px-3 py-1 text-sm font-bold">분석형</div>
    <div class="font-bold">Analyst Agent</div>
  </div>
  <div class="text-sm">여러 소스에서 데이터를 수집하고 인사이트 도출 — 핵심 가치: <strong>"수 시간 분석을 자동화"</strong></div>
</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4">
  <div class="flex items-center gap-3 mb-2">
    <div class="bg-purple-500 text-white rounded-full px-3 py-1 text-sm font-bold">계획형</div>
    <div class="font-bold">Planner Agent</div>
  </div>
  <div class="text-sm">복잡한 목표를 서브태스크로 분해하고 실행 계획 수립 — 핵심 가치: <strong>"복잡한 프로젝트 계획 자동화"</strong></div>
</div>

</v-clicks>

<!--
[스크립트]
3가지 Agent 패턴입니다. [클릭] 첫 번째, 자동화형 즉 Executor Agent입니다. 외부 이벤트가 트리거가 되어 일련의 작업을 자동 실행합니다. 핵심 가치는 "사람이 반복적으로 수행하던 업무를 대신 실행"하는 것입니다. [클릭] 두 번째, 분석형 즉 Analyst Agent입니다. 여러 소스에서 데이터를 수집하고 인사이트를 도출합니다. 핵심 가치는 "수 시간 걸리는 데이터 분석을 자동화"하는 것입니다. [클릭] 세 번째, 계획형 즉 Planner Agent입니다. 복잡한 목표를 서브태스크로 분해하고 실행 계획을 수립합니다. 핵심 가치는 "복잡한 프로젝트의 계획과 추적을 자동화"하는 것입니다.

[Q&A 대비]
Q: 실제 프로젝트에서 어떤 패턴이 가장 많이 쓰이나요?
A: 자동화형이 가장 흔합니다. 반복 업무 자동화 니즈가 가장 많기 때문입니다. 분석형과 계획형은 자동화형에 보조적으로 결합되는 경우가 많습니다.

전환: 각 패턴의 설계 핵심과 주의사항을 살펴보겠습니다.
시간: 3분
-->

---
transition: slide-left
---

# 패턴별 설계 핵심

<div class="grid grid-cols-3 gap-4 overflow-hidden">

<div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
  <div class="font-bold text-blue-700 dark:text-blue-300 mb-2">자동화형</div>
  <div class="text-sm space-y-2">
    <div><strong>흐름</strong>: 트리거 → 판단 → 실행</div>
    <div><strong>설계 핵심</strong>: Tool 호출 안정성, 에러 복구</div>
    <div class="text-xs text-gray-500 mt-2">예: 이메일 → 분류 → 티켓 생성</div>
  </div>
</div>

<div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
  <div class="font-bold text-green-700 dark:text-green-300 mb-2">분석형</div>
  <div class="text-sm space-y-2">
    <div><strong>흐름</strong>: 수집 → 분석 → 보고</div>
    <div><strong>설계 핵심</strong>: 데이터 완전성, 분석 정확성</div>
    <div class="text-xs text-gray-500 mt-2">예: 로그 수집 → 이상 탐지 → 리포트</div>
  </div>
</div>

<div v-click class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4">
  <div class="font-bold text-purple-700 dark:text-purple-300 mb-2">계획형</div>
  <div class="text-sm space-y-2">
    <div><strong>흐름</strong>: 분해 → 계획 → 재계획</div>
    <div><strong>설계 핵심</strong>: 목표 분해 품질, 재계획 능력</div>
    <div class="text-xs text-gray-500 mt-2">예: 목표 → 서브태스크 → 실행 추적</div>
  </div>
</div>

</div>

<div v-click class="mt-4 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-3 text-sm">
<strong>실무 현실</strong>: 현업 Agent의 대부분은 하나의 주 패턴에 보조 패턴이 결합된 <strong>복합 형태</strong>다
</div>

<!--
[스크립트]
각 패턴의 설계 핵심을 정리해보겠습니다. [클릭] 자동화형은 트리거 → 판단 → 실행의 흐름입니다. 설계할 때 가장 중요한 것은 Tool 호출의 안정성과 에러 복구입니다. 외부 API가 실패했을 때 어떻게 복구할지가 핵심입니다. [클릭] 분석형은 수집 → 분석 → 보고의 흐름입니다. 데이터 수집의 완전성과 분석의 정확성이 설계 핵심입니다. 빠진 데이터가 없어야 하고, 분석 결과가 신뢰할 수 있어야 합니다. [클릭] 계획형은 목표 분해 → 계획 → 재계획의 흐름입니다. 목표를 잘게 쪼개는 품질과, 중간에 실패했을 때 재계획하는 능력이 핵심입니다. [클릭] 그리고 실무에서는 하나의 주 패턴에 보조 패턴이 결합된 복합 형태가 일반적입니다.

[Q&A 대비]
Q: 처음부터 복합 패턴을 설계해도 되나요?
A: 처음에는 주 패턴 하나에 집중하고, 필요할 때 보조 패턴을 추가하는 것을 권장합니다. 처음부터 "만능 Agent"를 만들려 하면 어느 패턴에서도 품질을 보장하기 어렵습니다.

전환: 전통 소프트웨어와 비교하면 차이가 명확해집니다.
시간: 3분
-->

---
layout: two-cols-header
transition: slide-left
---

# Agent 패턴 vs 전통 소프트웨어

::left::

<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 overflow-hidden">

<strong>전통 소프트웨어 대응</strong>

<v-clicks>

- 자동화형 → 메시지 큐 기반 Worker
- 분석형 → ETL/ELT 파이프라인
- 계획형 → Airflow, Temporal

</v-clicks>

</div>

::right::

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 overflow-hidden">

<strong>Agent가 추가하는 것</strong>

<v-clicks>

- 자동화형 → LLM 기반 <strong>유연한 판단</strong>
- 분석형 → <strong>비결정적 분석</strong> 가능
- 계획형 → <strong>동적 재계획</strong> 능력

</v-clicks>

</div>

<div v-click class="col-span-2 mt-4 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-3 text-sm">

<strong>주의</strong>: LLM 기반 판단은 <strong>비결정성(non-determinism)</strong>이 증가한다 → 테스트와 모니터링 전략이 달라져야 한다

</div>

<!--
[스크립트]
각 Agent 패턴과 전통 소프트웨어를 비교해보겠습니다. [클릭] 자동화형은 메시지 큐 기반 Worker와 유사하지만, [클릭] LLM 기반의 유연한 판단이 추가됩니다. 사전에 정의하지 않은 케이스도 처리할 수 있습니다. [클릭] 분석형은 ETL/ELT 파이프라인과 유사하지만, [클릭] 비결정적 분석이 가능합니다. 규칙 기반이 아닌 LLM이 상황에 따라 분석 방식을 달리할 수 있습니다. [클릭] 계획형은 Airflow나 Temporal과 유사하지만, [클릭] 실패 시 동적으로 재계획하는 능력이 있습니다. [클릭] 중요한 주의사항입니다. LLM 기반 판단은 비결정성이 증가합니다. 같은 입력에 항상 같은 결과가 나오지 않습니다. 따라서 테스트와 모니터링 전략이 전통 소프트웨어와 달라져야 합니다.

[Q&A 대비]
Q: 비결정성을 어떻게 테스트하나요?
A: 단위 테스트 대신 평가(evaluation) 기반 접근이 필요합니다. 여러 번 실행해서 평균적인 품질을 측정하거나, LLM-as-a-judge 패턴을 사용합니다.

전환: 이제 네 번째이자 마지막 주제, RAG vs Agent 판단 기준을 살펴보겠습니다.
시간: 3분
-->

---
layout: section
transition: fade
---

# 4. RAG vs Agent 판단 기준

<!--
[스크립트]
네 번째 주제입니다. 실무에서 가장 자주 마주치는 아키텍처 의사결정 중 하나가 "RAG로 충분한가, Agent가 필요한가"입니다. 잘못 판단하면 두 방향으로 실패합니다. RAG로 충분한 문제에 Agent를 쓰면 복잡도, 비용, 지연이 불필요하게 증가합니다. 반대로 Agent가 필요한 문제에 RAG만 적용하면, 검색은 잘 되는데 문제를 해결해주지 않는 시스템이 됩니다.

[Q&A 대비]
Q: RAG와 Agent가 뭔지 간단히 다시 설명해줄 수 있나요?
A: RAG는 검색 증강 생성입니다. 문서를 검색해서 LLM이 답변하는 패턴입니다. Agent는 LLM이 판단해서 도구를 호출하고 행동하는 패턴입니다.

전환: 5가지 축으로 체계적으로 비교해보겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# RAG vs Agent: 5가지 판단 축

<v-clicks>

<div class="grid grid-cols-[3fr_4fr_4fr] gap-2 text-sm overflow-hidden">
  <div class="font-bold text-gray-500 p-2">판단 축</div>
  <div class="font-bold text-center bg-blue-50 dark:bg-blue-900/30 rounded p-2">RAG</div>
  <div class="font-bold text-center bg-purple-50 dark:bg-purple-900/30 rounded p-2">Agent</div>

  <div class="p-2 border-b border-gray-100">① 상호작용</div>
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded p-2 border-b border-gray-100">단일 질의-응답 (1-turn)</div>
  <div class="bg-purple-50 dark:bg-purple-900/30 rounded p-2 border-b border-gray-100">멀티턴 + 중간 행동</div>

  <div class="p-2 border-b border-gray-100">② 외부 연동</div>
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded p-2 border-b border-gray-100">읽기 전용 ❌쓰기</div>
  <div class="bg-purple-50 dark:bg-purple-900/30 rounded p-2 border-b border-gray-100">읽기 + <strong>쓰기</strong> ✅</div>

  <div class="p-2 border-b border-gray-100">③ 판단 복잡도</div>
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded p-2 border-b border-gray-100">유사도 기반 검색</div>
  <div class="bg-purple-50 dark:bg-purple-900/30 rounded p-2 border-b border-gray-100">조건부 분기 + 다단계</div>

  <div class="p-2 border-b border-gray-100">④ 상태 관리</div>
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded p-2 border-b border-gray-100">Stateless</div>
  <div class="bg-purple-50 dark:bg-purple-900/30 rounded p-2 border-b border-gray-100">Stateful</div>

  <div class="p-2">⑤ 실패 처리</div>
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded p-2">"정보 없음" 응답</div>
  <div class="bg-purple-50 dark:bg-purple-900/30 rounded p-2">대안 시도 → 재시도 → 에스컬레이션</div>
</div>

</v-clicks>

<!--
[스크립트]
RAG와 Agent를 5가지 축으로 비교해보겠습니다. [클릭] 하나씩 살펴보겠습니다. 첫 번째, 상호작용 방식입니다. RAG는 단일 질의-응답에 최적화되어 있습니다. Agent는 멀티턴 대화와 중간 행동을 포함합니다. 두 번째, 외부 시스템 연동입니다. RAG는 본질적으로 읽기 전용입니다. Agent는 읽기와 쓰기 모두 가능합니다. 이것이 가장 핵심적인 차이입니다. 세 번째, 판단 복잡도입니다. RAG는 유사도 기반 검색을 합니다. Agent는 조건부 분기와 다단계 추론을 합니다. 네 번째, 상태 관리입니다. RAG는 각 질의가 독립적인 Stateless입니다. Agent는 이전 결과가 다음 행동에 영향을 주는 Stateful입니다. 다섯 번째, 실패 처리입니다. RAG는 정보를 못 찾으면 "없습니다"라고 응답합니다. Agent는 대안 전략을 시도하고, 재시도하고, 에스컬레이션합니다.

[Q&A 대비]
Q: 5가지 중 가장 중요한 판단 기준이 뭔가요?
A: ② 외부 연동의 쓰기 여부입니다. 외부 시스템에 쓰기 작업이 필요하면 Agent입니다. 읽고 답변하는 것만이라면 RAG로 충분한 경우가 많습니다.

전환: 핵심 기준을 좀 더 명확하게 짚어드리겠습니다.
시간: 4분
-->

---
transition: slide-left
---

# 핵심 판단 기준: "쓰기 능력"의 유무

<div class="flex items-center justify-center h-56 gap-8">

<div v-click class="text-center bg-blue-50 dark:bg-blue-900/30 rounded-xl p-6 w-52">
  <div class="text-4xl mb-3">📖</div>
  <div class="font-bold text-blue-700 dark:text-blue-300 text-lg">RAG</div>
  <div class="text-sm mt-2">읽기 전용<br>검색 → 답변</div>
</div>

<div v-click class="text-4xl font-bold text-gray-400">vs</div>

<div v-click class="text-center bg-purple-50 dark:bg-purple-900/30 rounded-xl p-6 w-52">
  <div class="text-4xl mb-3">✍️</div>
  <div class="font-bold text-purple-700 dark:text-purple-300 text-lg">Agent</div>
  <div class="text-sm mt-2">읽기 + <strong>쓰기</strong><br>검색 → 판단 → <strong>실행</strong></div>
</div>

</div>

<div v-click class="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4 text-center">
<strong>쓰기 작업이 필요한 순간 = Agent 도입 시점</strong><br>
<span class="text-sm">Jira 티켓 생성, 이메일 발송, Slack 메시지 전송 → Agent</span>
</div>

<!--
[스크립트]
가장 중요한 판단 기준을 정리하겠습니다. [클릭] RAG는 읽기 전용입니다. 문서를 검색하고 답변을 생성합니다. [클릭] 대(對) [클릭] Agent는 읽기와 쓰기 모두 합니다. 검색하고, 판단하고, 실행합니다. [클릭] 그러므로 쓰기 작업이 필요한 순간이 Agent 도입 시점입니다. Jira 티켓을 생성하거나, 이메일을 발송하거나, Slack 메시지를 보내야 한다면 Agent가 필요합니다. "알려주는 것 말고, 직접 처리해줬으면 좋겠다"는 요구가 나오는 순간입니다.

[Q&A 대비]
Q: Conversational RAG는 멀티턴인데 Agent와 다른 점이 뭔가요?
A: Conversational RAG는 대화 맥락을 유지하며 문서를 검색하고 답변합니다. 모든 작업이 "읽기"입니다. Agent는 그 답변을 바탕으로 Jira 티켓을 만들거나 이메일을 보내는 "쓰기" 작업을 수행합니다.

전환: RAG에서 Agent로 점진적으로 전환하는 방법도 알아보겠습니다.
시간: 3분
-->

---
transition: slide-left
---

# RAG에서 Agent로: 점진적 전환

<v-clicks>

<div class="flex items-center gap-3 mb-3">
  <div class="bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold shrink-0 text-sm">1</div>
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 flex-1">
    <div class="font-bold text-sm">Basic RAG</div>
    <div class="text-xs mt-1">단일 질의 → 문서 검색 → 답변 생성</div>
  </div>
</div>

<div class="flex items-center gap-3 mb-3">
  <div class="bg-cyan-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold shrink-0 text-sm">2</div>
  <div class="bg-cyan-50 dark:bg-cyan-900/30 rounded-lg p-3 flex-1">
    <div class="font-bold text-sm">Conversational RAG</div>
    <div class="text-xs mt-1">대화 맥락 유지 → 멀티턴 검색 → 답변</div>
  </div>
</div>

<div class="flex items-center gap-3 mb-3">
  <div class="bg-teal-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold shrink-0 text-sm">3</div>
  <div class="bg-teal-50 dark:bg-teal-900/30 rounded-lg p-3 flex-1">
    <div class="font-bold text-sm">Agentic RAG</div>
    <div class="text-xs mt-1">검색 재작성 → 멀티소스 검색 → 답변</div>
  </div>
</div>

<div class="flex items-center gap-3">
  <div class="bg-purple-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold shrink-0 text-sm">4</div>
  <div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3 flex-1">
    <div class="font-bold text-sm">Agent (RAG as Tool)</div>
    <div class="text-xs mt-1">RAG를 도구 중 하나로 포함 → 검색 + 판단 + <strong>쓰기 실행</strong></div>
  </div>
</div>

</v-clicks>

<!--
[스크립트]
점진적 전환이 가장 현실적인 접근입니다. [클릭] 1단계, Basic RAG입니다. 단일 질의에 문서를 검색해서 답변합니다. 가장 단순하고 빠르게 가치를 검증할 수 있습니다. [클릭] 2단계, Conversational RAG입니다. 대화 맥락을 유지하며 멀티턴 질의응답이 가능해집니다. [클릭] 3단계, Agentic RAG입니다. 검색 쿼리를 재작성하고, 여러 소스를 검색합니다. 여전히 쓰기 작업은 없습니다. [클릭] 4단계, Agent입니다. RAG가 Agent의 도구 중 하나가 됩니다. 검색, 판단, 쓰기 실행이 모두 가능해집니다. 이렇게 단계를 밟으면 리스크를 최소화하면서 빠르게 가치를 검증할 수 있습니다.

[Q&A 대비]
Q: 처음부터 4단계 Agent로 만들면 안 되나요?
A: 할 수는 있지만 추천하지 않습니다. 먼저 RAG로 "정보 검색과 답변"이라는 핵심 가치를 검증하고, 운영하면서 "자동 실행이 필요하다"는 요구가 나오면 Agent로 전환하는 것이 훨씬 안전합니다.

전환: 아키텍처 의사결정 트리를 코드로 정리해보겠습니다.
시간: 3분
-->

---
transition: slide-left
---

# 아키텍처 의사결정 트리

```python {1|3-5|7-10|12-16|18}
def decide_architecture(requirements: dict) -> str:
    """아키텍처 의사결정 트리"""
    # 외부 쓰기 작업이 필요하면 → Agent
    if requirements.get("needs_action"):
        return "Hybrid (Agent + RAG)" if requirements.get("knowledge_base") else "Agent"

    # 멀티스텝 + 동적 라우팅이면 → Agent
    if requirements.get("multi_step") and requirements.get("dynamic_routing"):
        return "Agent"

    # 지식 베이스가 있으면 → RAG
    if requirements.get("knowledge_base"):
        if requirements.get("needs_context"):
            return "Conversational RAG"
        return "Basic RAG"

    # 그 외 → 단순 LLM 호출
    return "Simple LLM Call"
```

<!--
[스크립트]
아키텍처 의사결정 로직을 코드로 정리해보겠습니다. [클릭] 함수 시작입니다. requirements 딕셔너리를 받아 아키텍처를 반환합니다. [클릭] 첫 번째 체크, 외부 쓰기 작업이 필요한가입니다. 쓰기가 필요하다면, 지식 베이스도 필요하면 Hybrid, 그렇지 않으면 Agent입니다. [클릭] 두 번째 체크, 멀티스텝과 동적 라우팅이 모두 필요한가입니다. 두 조건을 모두 만족하면 Agent입니다. [클릭] 세 번째 체크, 지식 베이스가 있는가입니다. 있다면 대화 맥락이 필요하면 Conversational RAG, 그렇지 않으면 Basic RAG입니다. [클릭] 그 외 나머지는 단순 LLM 호출로 충분합니다.

[Q&A 대비]
Q: 실제로 이런 코드를 프로젝트에서 쓰나요?
A: 코드 그 자체보다는, 이 로직을 팀 의사결정 체크리스트로 사용합니다. 요구사항 미팅에서 이 항목들을 하나씩 체크하면서 아키텍처를 결정합니다.

전환: 이제 오늘 배운 모든 내용을 정리해보겠습니다.
시간: 3분
-->

---
transition: slide-left
---

# 세션 핵심 정리

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 mb-2">
  <span class="font-bold text-blue-700 dark:text-blue-300">1.</span> Agent는 <strong>멀티스텝 + 동적 판단 + 도구 활용</strong> 3가지 조건을 만족하는 문제에 적합
</div>

<div class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-3 mb-2">
  <span class="font-bold text-orange-700 dark:text-orange-300">2.</span> Agent 설계는 <strong>Pain → Task → Skill → Tool</strong> 순서로 Top-Down 접근 (Tool-first는 함정)
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 mb-2">
  <span class="font-bold text-green-700 dark:text-green-300">3.</span> Agent 패턴은 <strong>자동화형 / 분석형 / 계획형</strong> 3가지이며 실무에서는 복합 패턴이 일반적
</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3">
  <span class="font-bold text-purple-700 dark:text-purple-300">4.</span> RAG vs Agent 핵심 기준은 <strong>외부 시스템 쓰기(side effect) 필요 여부</strong>
</div>

</v-clicks>

<!--
[스크립트]
오늘 Session 1에서 배운 내용을 정리하겠습니다. [클릭] 1., Agent는 멀티스텝, 동적 판단, 도구 활용 3가지 조건을 만족하는 문제에 적합합니다. 하나라도 빠지면 더 단순한 도구로 충분합니다. [클릭] 2., Agent 설계는 Pain에서 출발해서 Tool로 내려가는 Top-Down 접근이 올바릅니다. Tool부터 시작하면 비즈니스 가치 없는 기술 데모로 끝납니다. [클릭] 3., Agent 패턴은 자동화형, 분석형, 계획형 3가지입니다. 실무에서는 주 패턴에 보조 패턴이 결합된 복합 형태가 일반적입니다. [클릭] 4., RAG와 Agent를 구분하는 가장 핵심 기준은 외부 시스템에 쓰기 작업이 필요한가입니다.

[Q&A 대비]
Q: 이 네 가지 주제가 실습과 어떻게 연결되나요?
A: 이어지는 실습에서 여러분의 실제 업무를 Pain-Task-Skill-Tool로 분해하고, 어떤 아키텍처가 적합한지 직접 판단해보는 활동을 합니다.

전환: 이제 실습 시간입니다.
시간: 2분
-->

---
layout: section
transition: fade
---

# 실습 시간
## Pain → Task → Skill → Tool 실전 적용

<!--
[스크립트]
개념 설명을 마쳤습니다. 이제 실습 시간입니다. 3개의 실습을 통해 오늘 배운 프레임워크를 여러분의 실제 업무에 적용해보겠습니다. 실습은 I DO, WE DO, YOU DO 3단계로 진행됩니다. 먼저 강사가 시연하고, 함께 해보고, 여러분이 스스로 도전하는 순서입니다.

[Q&A 대비]
Q: 실습은 개인 작업인가요, 그룹 작업인가요?
A: I DO와 WE DO는 전체가 함께하고, YOU DO는 개인 또는 2인 1조로 진행합니다.

전환: 첫 번째 실습을 시작하겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# 실습 1: 개인 업무 기반 Agent 후보 도출

<div class="grid grid-cols-[6fr_4fr] gap-6">
<div>

<v-clicks>

**I DO** (5분) — 강사 시연
- "주간 보고서 작성" Pain을 Task-Skill-Tool로 분해

**WE DO** (10분) — 함께
- "고객 문의 분류 및 답변" 업무를 함께 분해
- 각 단계에서 멈추고 질문 받기

**YOU DO** (15분) — 독립 과제
- 본인 업무에서 반복 작업 3개 나열
- 각 작업에 Pain-Task-Skill-Tool 템플릿 작성
- 3개 중 Agent에 가장 적합한 2개 선정

</v-clicks>

</div>
<div>

<div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-sm">

**Pain 작성 기준**
- "불편하다" ❌
- "주당 3시간" ✅

**Agent 적합 체크**
- 멀티스텝? Y/N
- 동적 판단? Y/N
- 도구 활용? Y/N

</div>

</div>
</div>

<!--
[스크립트]
첫 번째 실습입니다. [클릭] 먼저 I DO 단계입니다. 제가 "주간 보고서 작성"을 Pain으로 선택하고, Task, Skill, Tool로 분해하는 과정을 보여드리겠습니다. [클릭] WE DO 단계에서는 "고객 문의 분류 및 답변"을 함께 분해해보겠습니다. 각 단계마다 멈추고 여러분의 의견을 들을 것입니다. [클릭] YOU DO 단계에서는 여러분이 현재 가장 시간이 많이 소요되는 반복 작업 3개를 나열하고, 각 작업에 템플릿을 작성합니다. [클릭] Pain을 작성할 때는 반드시 수치를 포함해야 합니다. "불편하다"는 Pain이 아닙니다. "주당 3시간"처럼 측정 가능해야 합니다. Agent 적합성은 3가지 체크리스트로 확인합니다.

[Q&A 대비]
Q: 현재 업무가 단순해서 Agent가 적합한 것이 없을 것 같은데요?
A: 그 자체가 중요한 발견입니다. "Agent가 불필요하다"는 결론도 올바른 분석 결과입니다. 억지로 Agent를 찾으려 하지 마세요.

전환: 30분 후 다음 실습으로 이어집니다.
시간: 2분
-->

---
transition: slide-left
---

# 실습 2: RAG vs Agent 구조 선택 이유 작성

<div class="grid grid-cols-[6fr_4fr] gap-6">
<div>

<v-clicks>

**I DO** (5분) — 강사 시연
- "사내 FAQ 챗봇"에 의사결정 트리 적용 → Basic RAG 선택 과정 시연

**WE DO** (10분) — 함께
- "고객 주문 처리 자동화" 시나리오
- 5가지 축을 하나씩 체크

**YOU DO** (15분) — 독립 과제
- 실습 1에서 선정한 2개 후보에 의사결정 트리 적용
- 선택 이유를 3가지 이상 작성
- 고려했다 배제한 대안도 작성

</v-clicks>

</div>
<div>

<div v-click class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4 text-sm">

**5가지 체크**
- ① 멀티턴 필요?
- ② 쓰기 작업?
- ③ 복잡한 판단?
- ④ 상태 유지?
- ⑤ 실패 복구?

</div>

</div>
</div>

<!--
[스크립트]
두 번째 실습입니다. [클릭] I DO 단계에서는 "사내 FAQ 챗봇" 요구사항에 방금 배운 의사결정 트리를 적용해서 Basic RAG를 선택하는 과정을 시연합니다. [클릭] WE DO 단계에서는 "고객 주문 처리 자동화" 시나리오를 함께 분석합니다. 5가지 축을 하나씩 체크리스트처럼 확인합니다. [클릭] YOU DO 단계에서는 실습 1에서 선정한 2개 후보에 직접 의사결정 트리를 적용합니다. 선택 이유를 3가지 이상 작성하고, 고려했지만 배제한 대안도 작성합니다. [클릭] 5가지 체크항목을 기준으로 판단하면 됩니다. 특히 ② 쓰기 작업 여부가 가장 핵심입니다.

[Q&A 대비]
Q: 판단이 모호할 때는 어떻게 하나요?
A: 그럴 때는 "더 단순한 쪽"을 선택합니다. RAG가 충분할 수도 있다면 RAG로 시작하고, 필요할 때 Agent로 전환합니다.

전환: 마지막 실습입니다.
시간: 2분
-->

---
transition: slide-left
---

# 실습 3: 업무 유형별 Agent 패턴 매핑

<div class="grid grid-cols-[6fr_4fr] gap-6">
<div>

<v-clicks>

**I DO** (5분) — 강사 시연
- "코드 리뷰 Agent" 복합 패턴(Planner + Analyst + Executor) 설명

**WE DO** (8분) — 함께
- "DevOps 장애 대응 자동화" 주 패턴 + 보조 패턴 도출

**YOU DO** (12분) — 독립 과제
- 실습 1 후보 2개의 패턴 판별
- 워크플로우 스케치 작성 (4단계)

</v-clicks>

</div>
<div>

<div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4 text-sm">

**패턴 판별 질문**
- "주로 실행하는가?" → 자동화형
- "주로 분석하는가?" → 분석형
- "주로 계획하는가?" → 계획형

**산출물이 무엇인가?**
- 행동 결과 → 자동화형
- 보고서 → 분석형
- 실행 계획 → 계획형

</div>

</div>
</div>

<!--
[스크립트]
마지막 실습입니다. [클릭] I DO 단계에서는 "코드 리뷰 Agent"를 예시로 복합 패턴인 Planner + Analyst + Executor를 설명하고 워크플로우 다이어그램을 그립니다. [클릭] WE DO 단계에서는 "DevOps 장애 대응 자동화"를 함께 분석하면서 주 패턴과 보조 패턴을 도출합니다. [클릭] YOU DO 단계에서는 실습 1에서 선정한 2개 후보의 패턴을 판별하고, 4단계 워크플로우를 스케치합니다. [클릭] 패턴 판별이 어렵다면 두 가지 질문을 던지세요. "이 Agent가 주로 무엇을 하는가?" 그리고 "최종 산출물이 무엇인가?" 행동 결과라면 자동화형, 보고서라면 분석형, 실행 계획이라면 계획형입니다.

[Q&A 대비]
Q: 워크플로우 스케치를 어떤 형식으로 작성하나요?
A: 텍스트로 "Step 1: (입력) → ..., Step 2: (판단) → ..., Step 3: (실행) → ..." 형식으로 작성하면 됩니다. 다이어그램 도구가 있다면 활용해도 좋습니다.

전환: 실습을 마친 후 전체 공유 시간을 갖겠습니다.
시간: 2분
-->

---
transition: fade
---

# Session 1 마무리

<div class="grid grid-cols-[5fr_5fr] gap-6 mt-4">
<div>

**오늘 배운 판단 기준**

<v-clicks>

- Agent 필요 조건: **멀티스텝 + 동적 판단 + 도구 활용**
- 설계 시작점: **Pain (수치 측정 가능한 비효율)**
- 올바른 흐름: **Pain → Task → Skill → Tool**
- RAG vs Agent: **쓰기 작업 유무**

</v-clicks>

</div>
<div>

**다음 세션 예고**

<div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 mt-2">
  <div class="font-bold">Session 2</div>
  <div class="text-sm mt-1">Agent 아키텍처 설계 — ReAct, Tool 설계, 단일 vs 멀티 에이전트</div>
</div>

<div v-click class="mt-4 text-sm text-gray-500">

**준비 사항**: 실습 1에서 선정한
Agent 후보를 메모해 오세요.
다음 세션 설계 실습에 활용합니다.

</div>

</div>
</div>

<!--
[스크립트]
Session 1을 마무리하겠습니다. [클릭] 오늘 배운 판단 기준 4가지를 다시 정리합니다. Agent 필요 조건은 멀티스텝, 동적 판단, 도구 활용입니다. [클릭] 설계 시작점은 수치로 측정 가능한 Pain입니다. [클릭] 올바른 설계 흐름은 Pain에서 Tool로 내려가는 Top-Down입니다. [클릭] RAG와 Agent의 핵심 구분 기준은 쓰기 작업의 유무입니다. [클릭] 다음 세션에서는 오늘 정의한 문제를 실제로 어떻게 설계하는지 배웁니다. ReAct 패턴, Tool 설계, 단일 vs 멀티 에이전트를 다룹니다. [클릭] 준비 사항이 있습니다. 실습 1에서 선정한 Agent 후보를 메모해 오세요. 다음 세션 설계 실습에서 그 후보를 바탕으로 실제 아키텍처를 설계해봅니다. 질문 있으신가요? [잠깐 멈춤] 없으시면 잠시 휴식 후 Session 2로 이어가겠습니다.

[Q&A 대비]
Q: 오늘 배운 프레임워크가 실제 업무에서 바로 적용 가능한가요?
A: 네, 오늘 실습에서 해본 Pain-Task-Skill-Tool 분석을 그대로 팀 미팅에 가져갈 수 있습니다. 이해관계자 소통에도 바로 활용할 수 있습니다.

전환: 10분 휴식 후 Session 2 시작합니다.
시간: 3분
-->

---
layout: section
---

# Session 2
## LLM 동작 원리 및 프롬프트 전략 심화

Token · Context Window · Hallucination · 프롬프트 전략 · Structured Output · 비용 최적화

<!--
[스크립트]
안녕하세요. Session 2에서는 LLM 기반 Agent를 설계할 때 반드시 알아야 할 핵심 동작 원리를 다룹니다.
이번 세션의 키워드는 여섯 가지입니다. Token, Context Window, Hallucination, 프롬프트 전략, Structured Output, 그리고 비용 최적화입니다.
이 개념들을 모르면 Agent가 왜 실패하는지 진단할 수 없고, 비용이 왜 폭발하는지 이해할 수 없습니다.
Session 1에서 Agent가 무엇인지 배웠다면, Session 2에서는 그 Agent를 움직이는 LLM 엔진의 작동 방식을 배웁니다.
준비되셨으면 시작하겠습니다.

[Q&A 대비]
Q: Session 1과 Session 2의 연결고리는 무엇인가요?
A: Session 1에서 Agent의 "Observe → Think → Act" 루프를 배웠습니다. Session 2는 그 중 "Think" 단계를 담당하는 LLM의 내부 동작을 다룹니다.

전환: 먼저 Agent 개발자가 반드시 알아야 할 3가지 제약부터 시작하겠습니다.
시간: 1분
-->

---

# 이번 세션에서 배울 것

<v-clicks>

- **Token** — LLM의 처리 단위, 비용의 근원
- **Context Window** — LLM의 작업 메모리 한계
- **Hallucination** — LLM이 사실을 "만들어내는" 현상
- **Zero-shot / Few-shot / CoT** — 프롬프트 전략 3가지
- **Structured Output** — Agent 응답을 안정적으로 통제하는 법
- **비용 최적화** — 80% 절감을 위한 4가지 전략

</v-clicks>

<!--
[스크립트]
이번 세션에서 다룰 내용을 미리 살펴보겠습니다.

[클릭] 첫 번째는 Token입니다. LLM이 텍스트를 어떻게 쪼개서 처리하는지, 그리고 비용이 왜 한국어에서 더 많이 나오는지 이해하게 됩니다.

[클릭] 두 번째는 Context Window입니다. LLM의 "작업 메모리"가 왜 Agent 설계의 핵심 제약인지 설명합니다.

[클릭] 세 번째는 Hallucination입니다. 일반 챗봇에서는 잘못된 정보 제공 수준이지만, Agent에서는 실제 시스템을 잘못 조작하는 결과로 이어집니다.

[클릭] 네 번째는 프롬프트 전략 3가지입니다. 같은 LLM이라도 프롬프트 구성에 따라 결과가 극적으로 달라집니다.

[클릭] 다섯 번째는 Structured Output입니다. Agent의 행동 결정을 안정적으로 파싱하려면 반드시 필요합니다.

[클릭] 마지막으로 비용 최적화입니다. 적절한 전략 조합으로 비용 80% 이상 절감이 가능합니다.

[Q&A 대비]
Q: 이 내용들이 실제 Agent 개발과 어떻게 연결되나요?
A: 이 개념들은 "왜 Agent가 실패하는가"를 진단하는 도구입니다. 나중에 실습에서 직접 체험하게 됩니다.

전환: 첫 번째 주제인 Token부터 시작하겠습니다.
시간: 2분
-->

---
layout: section
---

# Part 1
## Token · Context Window · Hallucination

LLM Agent 설계의 3대 제약

<!--
[스크립트]
Part 1에서는 LLM 기반 Agent를 설계할 때 반드시 이해해야 할 세 가지 제약을 다룹니다.
이 제약들을 모르면 Agent가 갑자기 엉뚱한 답을 하거나, 긴 문서를 처리하지 못하거나, 비용이 예상보다 10배 나오는 현상을 설명할 수 없습니다.
자동차 운전에 비유하면, 연료 탱크 크기, 연비, 브레이크 성능을 모르고 장거리 여행을 떠나는 것과 같습니다.

전환: 가장 먼저 Token의 개념을 살펴봅니다.
시간: 1분
-->

---

# Token — LLM의 처리 단위

<div class="grid grid-cols-2 gap-8">
<div>

**Token이란?**

<v-clicks>

- 글자나 단어 단위가 아닌 **서브워드(subword)** 단위
- BPE(Byte Pair Encoding) 알고리즘으로 생성
- 모델이 "읽고 쓰는" 기본 단위

</v-clicks>

</div>
<div>

**영어 vs 한국어**

<v-clicks>

- **영어**: 약 1 token ≈ 4글자 / 0.75 단어
- **한국어**: 약 1 token ≈ 1~2글자
- **결과**: 한국어는 영어 대비 **2~3배 토큰 소비**

</v-clicks>

</div>
</div>

<v-click>

<div class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4">

**실무 팁**: 시스템 프롬프트는 **영어**로 작성하고, 사용자 대면 응답만 한국어로 분리하면 성능과 비용 모두 최적화할 수 있다

</div>

</v-click>

<!--
[스크립트]
Token은 LLM이 텍스트를 처리하는 기본 단위입니다. 우리가 생각하는 "글자" 또는 "단어"와는 다릅니다.

[클릭] Token은 BPE라는 알고리즘으로 만들어지는 서브워드 단위입니다. 예를 들어 "unfriendly"라는 단어는 "un", "friend", "ly" 세 토큰으로 쪼개질 수 있습니다. 모델이 텍스트를 읽고 생성하는 모든 과정은 이 토큰 단위로 이루어집니다.

[클릭] 이제 언어별 차이를 보겠습니다. 영어는 평균적으로 4글자가 1토큰 정도입니다.

[클릭] 반면 한국어는 1~2글자가 1토큰입니다. 결과적으로 같은 내용을 한국어로 표현하면 영어 대비 2~3배 토큰을 소비합니다. 이것은 비용에 직접 영향을 줍니다.

[클릭] 따라서 실무에서는 시스템 프롬프트를 영어로 작성하는 것이 효과적입니다. 사용자에게 보여주는 응답만 한국어로 받으면, 성능과 비용 모두 최적화할 수 있습니다.

[Q&A 대비]
Q: 한국어 프롬프트가 영어보다 성능이 낮은가요?
A: 일반적으로 영어 프롬프트가 성능이 더 좋습니다. 학습 데이터에서 영어 비중이 압도적으로 높기 때문입니다. 한국어는 토큰도 더 소비하고 성능도 소폭 낮을 수 있습니다.

전환: 그럼 실제 토큰 수를 코드로 확인해보겠습니다.
시간: 3분
-->

---

# Token 실측 — 영어 vs 한국어

```python {1-8|10-14|16-22}
import tiktoken

enc = tiktoken.get_encoding("o200k_base")

# 영어: 약 1 token ≈ 4글자
english_text = "The quick brown fox jumps over the lazy dog."
en_tokens = enc.encode(english_text)
print(f"영어: 글자 수 {len(english_text)}, 토큰 수 {len(en_tokens)}")

# 한국어: 약 1 token ≈ 1-2글자 (영어 대비 2-3배)
korean_text = "빠른 갈색 여우가 게으른 개를 뛰어넘는다."
ko_tokens = enc.encode(korean_text)
print(f"한국어: 글자 수 {len(korean_text)}, 토큰 수 {len(ko_tokens)}")

# 실행 결과
# 영어:  글자 수 44, 토큰 수 10   ← 4.4글자/토큰
# 한국어: 글자 수 21, 토큰 수 22  ← 0.95글자/토큰
```

<v-click>

<div class="mt-4 bg-red-50 dark:bg-red-900/30 rounded-lg p-3 text-sm">

같은 의미, 같은 내용 → 영어 10토큰 vs 한국어 22토큰 → **비용 2.2배 차이**

</div>

</v-click>

<!--
[스크립트]
이 코드를 함께 보겠습니다.

[클릭] tiktoken 라이브러리로 실제 토큰 수를 측정하는 코드입니다. OpenAI 계열 최신 토크나이저 예시로 `o200k_base`를 사용합니다.

[클릭] 같은 의미의 영어 문장과 한국어 문장을 각각 인코딩합니다.

[클릭] 결과를 보면 충격적입니다. 영어 44글자는 10토큰인데, 한국어 21글자는 22토큰입니다. 글자 수는 영어가 2배 이상 많지만, 토큰 수는 한국어가 2배 이상 많습니다. 비용이 2.2배 차이납니다.

[DEMO] 실제 로컬 환경에서 `pip install tiktoken` 후 직접 실행해보면 이 차이를 체감할 수 있습니다.

[Q&A 대비]
Q: OpenAI가 아닌 Claude나 Gemini도 tiktoken으로 측정이 되나요?
A: tiktoken은 OpenAI 전용 라이브러리입니다. Claude는 Anthropic의 자체 토크나이저를 사용하고, 정확한 토큰 수는 API 응답의 usage 필드에서 확인할 수 있습니다. 하지만 대략적인 비율(한국어 > 영어)은 모든 모델에서 유사합니다.

전환: 이제 Context Window 개념으로 넘어가겠습니다.
시간: 3분
-->

---

# Context Window — LLM의 작업 메모리

<v-clicks>

- **정의**: LLM이 한 번에 처리할 수 있는 **최대 토큰 수**
- **핵심**: 입력(프롬프트) + 출력(응답)의 **합계**가 이 한도를 넘을 수 없다
- **비유**: RAM — 크다고 모든 걸 넣을 수 있는 게 아니다

</v-clicks>

<v-click>

<div class="mt-4 grid grid-cols-2 gap-4">
<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

**Agent에서 Context를 채우는 것들**
- 시스템 프롬프트
- Tool 스키마 정의
- 대화 이력 (턴이 쌓일수록 증가)
- 현재 사용자 입력

</div>
<div class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-4">

**"Lost in the Middle" 현상**

Context 중간에 위치한 정보를
잘 활용하지 못한다

→ Context가 크다고 무조건 좋지 않다

</div>
</div>

</v-click>

<!--
[스크립트]
Context Window는 LLM의 작업 메모리입니다.

[클릭] Context Window의 정의는 LLM이 한 번에 처리할 수 있는 최대 토큰 수입니다.

[클릭] 중요한 점은, 이 한도가 입력과 출력의 합산이라는 것입니다. 예를 들어 128,000토큰 모델에 127,000토큰을 입력하면 출력은 최대 1,000토큰밖에 못 받습니다.

[클릭] 컴퓨터의 RAM에 비유하면 이해하기 쉽습니다. RAM이 크다고 무한정 프로그램을 실행할 수 있는 게 아닌 것처럼요.

[클릭] Agent에서는 Context를 채우는 요소가 많습니다. 시스템 프롬프트, Tool 스키마, 대화 이력이 모두 들어가야 합니다. 특히 대화 이력은 턴이 쌓일수록 기하급수적으로 늘어납니다.

그리고 오른쪽을 보면 "Lost in the Middle" 현상이 있습니다. Context가 길어질수록 LLM은 중간에 위치한 정보를 잘 활용하지 못하는 경향이 있습니다. Context Window가 크다고 무조건 좋은 게 아닌 이유입니다.

[Q&A 대비]
Q: Agent가 10턴 대화를 할 때 마지막 턴의 입력 토큰이 급격히 증가하는 이유는?
A: LLM은 Stateless이므로 매 턴마다 이전 대화 이력 전체를 입력에 포함해야 합니다. 10턴째에는 1~9턴의 모든 입력과 출력이 누적되어 입력 토큰이 급격히 증가합니다.

전환: 주요 모델의 Context Window를 비교해보겠습니다.
시간: 3분
-->

---

# Context Window — 주요 모델 비교

```python {all|5-8|10-17}
context_windows = {
    "GPT-5.2":         {"window": 400_000,   "max_output": 128_000},
    "GPT-5.4":         {"window": 1_050_000, "max_output": 128_000},
    "Claude Opus 4.6": {"window": 200_000,   "max_output": 128_000},
}

def estimate_capacity(model, system_tokens, tool_tokens):
    spec = context_windows[model]
    usable = spec["window"] - spec["max_output"] - system_tokens - tool_tokens
    print(f"[{model}] 실제 사용 가능: {usable:,} tokens (~A4 {usable // 800}장)")

# Agent: 시스템 프롬프트 2000토큰, Tool 스키마 3000토큰 가정
for model in context_windows:
    estimate_capacity(model, 2000, 3000)
```

<v-click>

<div class="mt-3 text-sm bg-slate-50 dark:bg-slate-800 rounded-lg p-3 font-mono">

[GPT-5.2]         실제 사용 가능: 267,000 tokens (~A4 333장)<br>
[GPT-5.4]         실제 사용 가능: 917,000 tokens (~A4 1,146장)<br>
[Claude Opus 4.6] 실제 사용 가능: 67,000 tokens (~A4 83장)

</div>

</v-click>

<!--
[스크립트]
이 코드는 실제 사용 가능한 Context 공간을 계산합니다.

[클릭] 각 모델의 Context Window와 최대 출력 토큰을 정의했습니다. GPT-5.4는 100만 토큰급 장문 컨텍스트를 제공하고, GPT-5.2와 Claude Opus 4.6도 충분히 큰 작업 공간을 제공합니다.

[클릭] 하지만 Agent에서는 시스템 프롬프트 2,000토큰, Tool 스키마 3,000토큰을 미리 빼야 합니다. 그리고 출력 공간도 빼면, 실제로 대화 이력과 입력에 사용할 수 있는 공간이 계산됩니다.

[클릭] 결과를 보면, GPT-5.2 기준으로도 실제 사용 가능한 공간은 약 A4 333장 분량입니다. 적지 않지만, 복잡한 Agent가 긴 대화를 하다 보면 금방 차오를 수 있습니다.

핵심 교훈은: Context Window의 크기가 아니라, 어떤 정보를 넣을지 선별하는 설계가 중요하다는 것입니다.

[Q&A 대비]
Q: Context Window가 크면 그냥 다 넣으면 되지 않나요?
A: 세 가지 문제가 있습니다. 비용 증가(입력 토큰 비례), Lost in the Middle 현상, 그리고 응답 지연(TTFT 증가)입니다. 필요한 정보만 선별해서 넣는 것이 더 좋은 설계입니다.

전환: 이제 가장 위험한 제약인 Hallucination을 알아보겠습니다.
시간: 3분
-->

---

# Hallucination — LLM이 사실을 "만들어낸다"

<div class="grid grid-cols-2 gap-6">
<div>

**정의**

<v-clicks>

- LLM이 학습 데이터에 없는 정보를
  **사실인 것처럼 생성**하는 현상
- "가장 그럴듯한 다음 토큰"을 예측하다
  답이 없으면 **패턴으로 만들어냄**

</v-clicks>

</div>
<div>

**Agent에서 특히 위험한 이유**

<v-clicks>

- 잘못된 판단 → **실제 행동으로 실행**
- 존재하지 않는 API 엔드포인트 호출
- 잘못된 SQL 쿼리로 **데이터 손상**
- 잘못된 금액으로 **결제 처리**

</v-clicks>

</div>
</div>

<!--
[스크립트]
Hallucination은 LLM의 가장 위험한 특성입니다.

[클릭] Hallucination의 정의는, LLM이 학습 데이터에 없는 정보를 사실인 것처럼 생성하는 현상입니다.

[클릭] LLM은 본질적으로 "가장 그럴듯한 다음 토큰"을 예측하는 확률 모델입니다. 학습 데이터에서 답을 찾지 못하면, 패턴에 기반한 답을 만들어냅니다.

[클릭] 일반 챗봇에서는 잘못된 정보를 제공하는 수준입니다. 사용자가 확인하면 됩니다.

[클릭] 하지만 Agent에서는 다릅니다. 잘못된 판단이 실제 행동으로 실행됩니다. 존재하지 않는 API를 호출하거나, 잘못된 SQL로 데이터를 손상시키거나, 잘못된 금액으로 결제를 처리할 수 있습니다. 되돌리기 어렵거나 불가능한 결과가 생깁니다.

[Q&A 대비]
Q: Hallucination을 완전히 없애는 방법이 있나요?
A: 현재 기술로는 완전 제거가 불가능합니다. 따라서 완화 전략을 조합하는 것이 현실적인 접근입니다.

전환: 그렇다면 Hallucination을 어떻게 완화할 수 있는지 보겠습니다.
시간: 3분
-->

---

# Hallucination 완화 전략 5가지

<v-clicks>

- **Grounding** — 외부 데이터로 답변 근거를 제공 (RAG, 검색 도구)
- **Validation** — 행동 실행 전 파라미터를 코드로 검증
- **Confirmation** — 고위험 행동(결제, 삭제)에 인간 승인 요구
- **Structured Output** — JSON Schema로 출력 형식을 강제
- **Temperature 조절** — 사실 기반 작업에서 낮은 값 사용 (0~0.3)

</v-clicks>

<v-click>

<div class="mt-4 grid grid-cols-3 gap-3 text-sm">
<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3 text-center">

**일반 챗봇**
잘못된 정보 제공

</div>
<div class="bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-3 text-center">

**RAG**
검색 결과와 무관한 답변

</div>
<div class="bg-red-100 dark:bg-red-800/40 rounded-lg p-3 text-center font-bold">

**Agent**
실제 시스템 변경

</div>
</div>

</v-click>

<!--
[스크립트]
Hallucination을 완전히 없애는 것은 현재 기술로 불가능합니다. 대신 완화 전략을 조합합니다.

[클릭] 첫 번째는 Grounding입니다. 외부 데이터를 제공하여 LLM이 "지어내지 않아도" 되게 합니다. RAG나 검색 도구가 여기에 해당합니다.

[클릭] 두 번째는 Validation입니다. LLM의 판단을 실행하기 전에 코드로 검증합니다. 예를 들어 주문 ID가 실제로 존재하는지, 금액이 유효 범위인지 확인합니다.

[클릭] 세 번째는 Confirmation입니다. 결제나 삭제처럼 되돌리기 어려운 고위험 행동에는 인간의 승인을 요구합니다.

[클릭] 네 번째는 Structured Output입니다. JSON Schema로 출력 형식을 강제하면 형식 오류로 인한 잘못된 실행을 방지할 수 있습니다. 이 개념은 Part 3에서 자세히 다룹니다.

[클릭] 다섯 번째는 Temperature 조절입니다. 사실 기반 작업에서는 Temperature를 낮게 설정하여 LLM이 "창의적으로 지어내는" 것을 억제합니다.

아래 표를 보면, Hallucination의 영향은 Agent에서 가장 심각합니다. 실제 시스템 변경으로 이어지기 때문입니다.

[Q&A 대비]
Q: Temperature를 0으로 설정하면 Hallucination이 없어지나요?
A: 아닙니다. Temperature는 출력의 다양성을 제어할 뿐, Hallucination의 근본 원인을 제거하지 않습니다. 0으로 설정해도 학습 데이터에 없는 내용을 만들어낼 수 있습니다.

전환: 3가지 제약을 정리하고 프롬프트 전략으로 넘어가겠습니다.
시간: 4분
-->

---

# 3대 제약 — 실무에서의 의미

| 제약 | **이해하면** | **모르면** |
|------|------------|-----------|
| **Token** | 불필요한 비용을 줄일 수 있다 | 예상보다 10배 비용 발생 |
| **Context Window** | 대화 이력 관리 전략을 설계할 수 있다 | 긴 대화에서 예측 불가 실패 |
| **Hallucination** | 적절한 안전 장치를 배치할 수 있다 | 프로덕션에서 비가역적 오류 반복 |

<v-click>

<div class="mt-6 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

**핵심 메시지**: 이 3가지 제약은 Agent의 **비용 · 성능 · 안전성**에 직접 영향을 미친다.
알면 설계할 수 있고, 모르면 디버깅조차 할 수 없다.

</div>

</v-click>

<!--
[스크립트]
3가지 제약을 한 표로 정리했습니다.

Token을 이해하면 불필요한 비용을 줄일 수 있습니다. 모르면 예상보다 10배의 비용이 청구될 수 있습니다.

Context Window를 이해하면 대화 이력 관리 전략을 미리 설계할 수 있습니다. 모르면 긴 대화에서 갑자기 Agent가 이전 내용을 잊거나 실패하는 현상을 예측조차 못합니다.

Hallucination을 이해하면 적절한 안전 장치를 미리 배치할 수 있습니다. 모르면 프로덕션 환경에서 비가역적 오류가 반복됩니다.

[클릭] 핵심 메시지입니다. 이 3가지 제약은 Agent의 비용, 성능, 안전성에 직접 영향을 미칩니다. 알면 설계할 수 있고, 모르면 디버깅조차 할 수 없습니다.

[Q&A 대비]
Q: 세 가지 중 가장 중요한 것은 어떤 건가요?
A: 상황에 따라 다르지만, Agent 개발 초기에는 Hallucination 완화가 가장 중요합니다. 비가역적 피해가 생길 수 있기 때문입니다. 스케일이 커지면 Token/비용 최적화가 중요해집니다.

전환: 이제 Part 2로 넘어가서 프롬프트 전략을 알아보겠습니다.
시간: 2분
-->

---
layout: section
---

# Part 2
## Zero-shot · Few-shot · Chain-of-Thought

같은 LLM, 다른 결과 — 프롬프트 전략의 선택

<!--
[스크립트]
Part 2에서는 프롬프트 전략 3가지를 비교합니다.
같은 LLM, 같은 문제라도 프롬프트 구성에 따라 결과 품질이 극적으로 달라집니다.
Agent의 핵심인 "상황 판단 → 행동 결정"의 품질은 바로 이 프롬프트 전략에 좌우됩니다.
잘못된 전략을 선택하면 단순한 문제에 과도한 비용이 들거나, 복잡한 판단에서 부정확한 결과가 나옵니다.

전환: 먼저 세 전략의 개념부터 살펴보겠습니다.
시간: 1분
-->

---

# 프롬프트 전략 3가지 개요

<div class="grid grid-cols-3 gap-4 mt-2">

<v-clicks>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">

**Zero-shot**

예시 없이 지시만 전달

"고객 문의를 분류하세요"

- 토큰 사용량 최소
- 설정 간단
- 복잡한 작업에서 불안정

</div>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

**Few-shot**

입력-출력 예시 제공

"이런 패턴으로 처리하라"

- 토큰 사용량 중간
- 예시가 임시 학습 데이터 역할
- **예시의 수보다 질이 중요**

</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4">

**Chain-of-Thought**

"단계별로 생각하라" 지시

추론 과정을 명시적으로 유도

- 토큰 사용량 많음
- 다단계 추론에서 큰 효과
- 추론 자체가 출력 토큰 소비

</div>

</v-clicks>

</div>

<!--
[스크립트]
세 가지 전략을 한눈에 비교해보겠습니다.

[클릭] 첫 번째는 Zero-shot입니다. 예시 없이 지시만 줍니다. "고객 문의를 분류하세요"처럼 무엇을 해야 하는지만 전달합니다. 토큰 사용량이 가장 적고 설정이 간단하지만, 모호하거나 복잡한 작업에서 결과가 불안정합니다.

[클릭] 두 번째는 Few-shot입니다. 입력-출력 쌍의 예시를 몇 개 제공합니다. "이런 패턴으로 처리하라"고 알려주는 방식입니다. 예시가 임시 학습 데이터 역할을 합니다. 중요한 점은 예시의 수보다 질이 더 중요하다는 것입니다.

[클릭] 세 번째는 Chain-of-Thought입니다. "단계별로 생각하라"고 지시하여 추론 과정을 명시적으로 유도합니다. 다단계 추론과 조건부 판단에서 큰 효과를 보이지만, 추론 과정 자체가 출력 토큰으로 소비되어 비용이 증가합니다.

[Q&A 대비]
Q: CoT를 쓰면 항상 결과가 더 좋은가요?
A: 아닙니다. 단순한 작업에 CoT를 쓰면 불필요한 추론으로 토큰 낭비가 생기고, 과도한 사고로 오히려 잘못된 결론에 도달할 수도 있습니다.

전환: 실제 코드로 세 전략의 차이를 확인하겠습니다.
시간: 3분
-->

---

# 프롬프트 전략 코드 비교

```python {1-10|12-23|25-37}{maxHeight:'380px'}
def call_llm(messages):
    response = client.chat.completions.create(
        model=MODEL, messages=messages, temperature=0,
    )
    return response.choices[0].message.content


# Zero-shot: 예시 없이 지시만으로 수행
def zero_shot_classify(text):
    messages = [
        {"role": "system", "content": "고객 문의를 분류하세요: 환불, 배송, 제품문의, 기타"},
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


# Few-shot: 예시를 제공하여 패턴 학습 유도
def few_shot_classify(text):
    messages = [
        {"role": "system", "content": "고객 문의를 분류하세요: 환불, 배송, 제품문의, 기타"},
        {"role": "user", "content": "주문한 지 일주일인데 아직 안 왔어요"},
        {"role": "assistant", "content": "배송"},
        {"role": "user", "content": "결제했는데 취소하고 돈 돌려받고 싶어요"},
        {"role": "assistant", "content": "환불"},
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


# Chain-of-Thought: 단계별 추론 유도
def cot_classify(text):
    messages = [
        {"role": "system", "content": """단계별로 분석하세요:
1. 핵심 키워드를 추출하세요
2. 고객의 의도를 파악하세요
3. 카테고리를 선택하세요: 환불, 배송, 제품문의, 기타"""},
        {"role": "user", "content": text},
    ]
    return call_llm(messages)
```

<!--
[스크립트]
세 전략을 실제 코드로 구현한 모습입니다.

[클릭] 공통 LLM 호출 함수입니다. temperature를 0으로 설정하여 결정론적 응답을 얻습니다. Zero-shot은 단 2개의 메시지로 구성됩니다. 간단합니다.

[클릭] Few-shot은 실제 예시를 대화 형태로 삽입합니다. user-assistant 쌍으로 패턴을 보여줍니다. 여기서는 2개의 예시를 넣었습니다.

[클릭] Chain-of-Thought는 시스템 프롬프트에 단계별 추론 지시를 명시합니다. "1. 키워드 추출, 2. 의도 파악, 3. 카테고리 선택"처럼 사고 과정을 구조화합니다.

[DEMO] 실제로 복합 문의 "색상이 다른데 교환 가능하면 교환, 안 되면 환불요"를 각 전략에 넣어보면 흥미로운 차이가 납니다. Zero-shot은 한 단어로, CoT는 추론 과정이 포함된 답을 줍니다.

[Q&A 대비]
Q: Few-shot 예시는 몇 개가 적당한가요?
A: 일반적으로 3~5개가 최적입니다. 5개를 넘으면 성능 향상이 둔화되고 Context만 소비합니다. 핵심은 수보다 질입니다. 경계 케이스를 포함한 다양한 예시 3개가 비슷한 쉬운 예시 10개보다 효과적입니다.

전환: 이 세 전략을 언제 어떻게 선택해야 할지 기준을 알아보겠습니다.
시간: 4분
-->

---

# 전략 선택 기준 — Agent에서의 활용

| 전략 | 토큰 | 적합한 경우 | Agent 활용 예시 |
|------|------|-----------|----------------|
| **Zero-shot** | 최소 | 명확한 단일 지시, 직관적 분류 | 간단한 의도 분류, 키워드 추출 |
| **Few-shot** | 중간 | 패턴이 명확하고 예시로 설명 가능 | 정형화된 분류, 포맷 변환 |
| **CoT** | 많음 | 다단계 추론, 조건부 판단 필요 | 계획 수립, 복잡한 의사결정 |

<v-click>

<div class="mt-4 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4">

**실무 권장**: 각 단계마다 적합한 전략을 다르게 적용하는 **"적응형 전략(Adaptive Strategy)"**

- 의도 분류 → Zero-shot (빠르고 저렴)
- 엔티티 추출 → Few-shot (패턴이 명확)
- 행동 결정 → CoT (비가역적이므로 신중하게)

</div>

</v-click>

<!--
[스크립트]
이 표는 세 전략의 선택 기준입니다.

Zero-shot은 명확한 단일 지시에 최적입니다. Agent에서는 간단한 의도 분류나 키워드 추출에 씁니다.

Few-shot은 패턴이 명확한 경우에 씁니다. "이 형식으로 변환하라"처럼 예시로 설명할 수 있는 작업에 적합합니다.

CoT는 다단계 추론이 필요한 복잡한 판단에 씁니다. 계획 수립이나 고위험 의사결정에 적합합니다.

[클릭] 실무에서 가장 효과적인 접근은 적응형 전략입니다. 하나의 Agent 안에서도 단계마다 다른 전략을 씁니다. 의도 분류는 Zero-shot으로 빠르게, 엔티티 추출은 Few-shot으로 정확하게, 행동 결정은 CoT로 신중하게 처리합니다.

[Q&A 대비]
Q: Agent의 "행동 결정" 단계에 가장 적합한 전략은 무엇인가요?
A: Chain-of-Thought가 가장 적합합니다. 첫째, 행동 실행은 비가역적이므로 신중한 판단이 필요합니다. 둘째, 추론 과정이 로그로 남아 "왜 이 행동을 선택했는지" 감사가 가능합니다. 셋째, 복수의 조건을 종합 판단해야 합니다.

전환: Part 3으로 넘어가서 Structured Output을 알아보겠습니다.
시간: 3분
-->

---
layout: section
---

# Part 3
## Structured Output

Agent 응답을 안정적으로 통제하는 법

<!--
[스크립트]
Part 3에서는 Structured Output을 다룹니다.
Agent에서 LLM의 응답은 "사용자에게 보여줄 텍스트"가 아닙니다.
LLM의 응답은 다음 행동의 입력이 됩니다.
"데이터베이스에서 검색해보겠습니다"라는 자연어 응답으로는, 어떤 도구를 어떤 파라미터로 호출해야 하는지 알 수 없습니다.
자연어 응답을 정규식으로 파싱하려는 시도는 반드시 깨집니다. LLM의 응답 형식이 매번 미묘하게 달라지기 때문입니다.

전환: Structured Output의 원리를 먼저 살펴보겠습니다.
시간: 1분
-->

---

# Structured Output — 왜 필요한가

<div class="grid grid-cols-2 gap-6">
<div>

**문제: 자연어 파싱**

<v-clicks>

```python
# 위험한 패턴 ❌
response = llm.chat("주문 상태를 확인해")
# "주문번호 12345는 현재 배송 중..."

order_id = response.split("주문번호 ")[1].split("는")[0]
# LLM이 "12345번 주문이..."라고 답하면?
# → IndexError 또는 잘못된 값
```

LLM의 응답 형식은
**매번 미묘하게 달라진다**

</v-clicks>

</div>
<div>

**해결: Structured Output**

<v-clicks>

```python
# 안전한 패턴 ✅
class OrderStatus(BaseModel):
    order_id: str
    status: str
    eta: str

# 항상 이 형식으로만 응답
# {"order_id": "12345",
#  "status": "배송중",
#  "eta": "2025-03-07"}
```

JSON Schema로
**형식을 강제한다**

</v-clicks>

</div>
</div>

<!--
[스크립트]
왼쪽과 오른쪽을 비교해보겠습니다.

[클릭] 왼쪽은 자연어 파싱 패턴입니다. LLM의 응답을 split으로 잘라서 필요한 정보를 추출합니다. 처음에는 동작하는 것처럼 보입니다.

[클릭] 하지만 LLM이 "주문번호 12345는..." 대신 "12345번 주문이..." 또는 "주문 12345의 상태는..."으로 답하면 즉시 깨집니다. LLM의 응답 형식은 매번 미묘하게 달라지기 때문입니다.

[클릭] 오른쪽은 Structured Output 패턴입니다. Pydantic 모델로 응답 형식을 정의하고, API에서 이 형식만 출력하도록 강제합니다.

[클릭] 결과는 항상 동일한 JSON 형식입니다. order_id, status, eta가 항상 존재하고 형식이 보장됩니다.

[Q&A 대비]
Q: 정규식으로 충분하지 않나요?
A: 단순한 경우에는 동작하지만, LLM의 응답이 조금만 바뀌어도 즉시 실패합니다. Structured Output은 토큰 생성 단계에서 형식을 강제하므로 근본적으로 다른 접근입니다.

전환: 실제 구현 코드를 살펴보겠습니다.
시간: 4분
-->

---

# Pydantic + OpenAI Structured Output

```python {1-16|18-26|28-36}{maxHeight:'380px'}
from pydantic import BaseModel, Field
from enum import Enum

class Urgency(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TicketClassification(BaseModel):
    """고객 문의 분류 결과"""
    category: str = Field(
        description="문의 카테고리",
        enum=["환불", "배송", "제품문의", "기술지원", "기타"],
    )
    urgency: Urgency = Field(description="긴급도")
    summary: str = Field(description="문의 요약 (1문장)", max_length=100)
    suggested_action: str = Field(description="권장 행동")


def classify_ticket(query: str) -> TicketClassification:
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "고객 문의를 분류하세요."},
            {"role": "user", "content": query},
        ],
        response_format=TicketClassification,
    )
    return response.choices[0].message.parsed


# 실행 결과
result = classify_ticket("배송 받았는데 색상이 다르고 환불 원합니다")
# {
#   "category": "환불",
#   "urgency": "high",
#   "summary": "배송된 상품의 색상이 주문과 다르며 환불을 요청",
#   "suggested_action": "환불 절차 안내 및 반품 접수"
# }
```

<!--
[스크립트]
실제 구현 코드를 단계별로 보겠습니다.

[클릭] 먼저 Pydantic으로 응답 스키마를 정의합니다. category는 5개 옵션 중 하나만 가능하고, urgency는 Enum으로 정의된 값만 허용합니다. summary는 최대 100자로 제한합니다. 이 제약들이 LLM의 출력을 통제합니다.

[클릭] API 호출에서 `response_format=TicketClassification`을 지정합니다. OpenAI의 `client.beta.chat.completions.parse`를 사용하면, 반환값이 자동으로 Pydantic 객체로 변환됩니다.

[클릭] 결과를 보면, 항상 동일한 구조의 JSON이 반환됩니다. category는 반드시 정해진 값 중 하나고, urgency는 Enum 값, summary는 100자 이내입니다. 파싱 실패가 원천 차단됩니다.

[Q&A 대비]
Q: Structured Output을 쓰면 LLM의 창의성이 제한되지 않나요?
A: 그렇습니다. 그리고 그것이 Agent에서는 장점입니다. Agent의 행동 결정은 창의적이면 안 됩니다. 예측 가능하고 파싱 가능한 출력이 필수입니다. 창의성이 필요한 부분은 별도의 자유 텍스트 필드로 분리하면 됩니다.

전환: Agent의 행동 결정 자체도 구조화할 수 있습니다.
시간: 4분
-->

---

# Agent 행동 결정의 구조화

```python {all}
class ToolCall(BaseModel):
    tool_name: str = Field(
        description="호출할 도구 이름",
        enum=["search_db", "send_email", "create_ticket", "escalate"],
    )
    parameters: dict = Field(description="도구에 전달할 파라미터")
    reasoning: str = Field(description="이 도구를 선택한 이유")

class AgentDecision(BaseModel):
    thought: str = Field(description="현재 상황에 대한 분석")
    action: ToolCall = Field(description="실행할 행동")
    is_final: bool = Field(description="이것이 최종 행동인지 여부")
```

<v-click>

<div class="mt-4 grid grid-cols-3 gap-3 text-sm">
<div class="bg-slate-50 dark:bg-slate-800 rounded-lg p-3">

**문법 오류**
정규식: 자주 발생
Structured Output: **없음**

</div>
<div class="bg-slate-50 dark:bg-slate-800 rounded-lg p-3">

**값 유효성**
정규식: 어려움
Structured Output: **Pydantic으로 검증**

</div>
<div class="bg-slate-50 dark:bg-slate-800 rounded-lg p-3">

**유지보수**
정규식: 어려움
Structured Output: **스키마 수정으로 간단**

</div>
</div>

</v-click>

<!--
[스크립트]
Agent의 행동 결정 자체도 Structured Output으로 구조화할 수 있습니다.

AgentDecision 스키마를 보면, thought는 현재 상황 분석, action은 실행할 도구 호출 정보, is_final은 이것이 마지막 행동인지 여부입니다.

ToolCall 안에서 tool_name은 4개 옵션 중 하나만 허용됩니다. 존재하지 않는 도구를 LLM이 만들어낼 수 없습니다.

reasoning 필드는 CoT의 효과를 가져옵니다. LLM이 왜 이 도구를 선택했는지 설명하면서 더 정확한 결정을 내리고, 동시에 감사 로그가 자동으로 생성됩니다.

[클릭] 아래 비교를 보면, Structured Output은 정규식 대비 모든 면에서 우수합니다. 문법 오류가 없고, 값 유효성을 검증할 수 있고, 스키마 수정만으로 유지보수가 쉽습니다.

[Q&A 대비]
Q: JSON 파싱 에러가 발생하면 어떻게 처리하나요?
A: 3단계 방어 전략을 씁니다. 첫째, Structured Output API로 문법적으로 올바른 JSON을 보장합니다. 둘째, Pydantic 검증으로 값의 유효성을 잡아냅니다. 셋째, 파싱 실패 시 에러 메시지를 포함해 재요청합니다. 최대 2~3회 후 사람에게 에스컬레이션합니다.

전환: 마지막 Part 4에서 비용 최적화를 알아보겠습니다.
시간: 3분
-->

---
layout: section
---

# Part 4
## 비용 및 Latency 최적화

80% 절감을 위한 4가지 전략

<!--
[스크립트]
마지막 Part 4입니다. Agent는 한 번의 사용자 요청에 LLM을 여러 번 호출합니다.
단순 챗봇이 1회 호출로 끝나는 반면, Agent는 5~10회 이상 호출할 수 있습니다.
고급 모델로 10턴 Agent를 운영하면, 요청 1건당 0.1~0.5달러, 응답 시간 30초~1분이 소요됩니다.
하루 1,000건 처리 시 월 3,000~15,000달러의 비용이 발생합니다.
이것이 최적화가 필요한 이유입니다.

전환: 비용 구조를 먼저 이해하겠습니다.
시간: 1분
-->

---

# Agent 비용의 3가지 구성 요소

<div class="grid grid-cols-3 gap-4 mt-2">

<v-clicks>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-4">

<strong>① 누적 입력 토큰</strong>

가장 큰 비용 요인

LLM은 Stateless
→ 매 턴마다 전체 이력을 다시 전송

5턴에서 각 800토큰이면
5턴째만 3,200토큰이 이력 소비

</div>

<div class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-4">

<strong>② 출력 토큰</strong>

입력보다 <strong>2~5배 단가</strong> 높음

Structured Output으로
간결한 JSON만 출력
→ 비용 절감

</div>

<div class="bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-4">

<strong>③ Tool 실행 시간</strong>

순차 실행 시
각 Tool 지연이 합산됨

독립적인 호출은
병렬 실행으로
→ 총 지연 = max(개별 지연)

</div>

</v-clicks>

</div>

<!--
[스크립트]
Agent 비용의 구성 요소를 세 가지로 나눌 수 있습니다.

[클릭] 첫 번째이자 가장 큰 요인은 누적 입력 토큰입니다. LLM은 Stateless이므로 매 턴마다 이전 대화 이력 전체를 다시 보내야 합니다. 5턴에서 각 턴 평균 800토큰이면, 5턴째 입력에만 이전 이력으로 3,200토큰이 소비됩니다. 턴이 쌓일수록 기하급수적으로 증가합니다.

[클릭] 두 번째는 출력 토큰입니다. 일반적으로 입력보다 2~5배 단가가 높습니다. Structured Output으로 간결한 JSON만 출력하면 출력 토큰을 크게 줄일 수 있습니다.

[클릭] 세 번째는 Tool 실행 시간입니다. 순차 실행 시 각 Tool의 지연이 합산됩니다. 하지만 상호 의존성이 없는 Tool 호출은 병렬로 실행하면, 총 지연이 max(개별 지연)으로 줄어듭니다. 3개 Tool 각각 2초라면 순차는 6초, 병렬은 2초입니다.

[Q&A 대비]
Q: 입력 토큰과 출력 토큰 중 어느 쪽이 더 비싼가요?
A: 일반적으로 출력 토큰이 입력 토큰보다 훨씬 비쌉니다. 최신 고성능 모델들도 출력 단가가 입력보다 여러 배 높은 경우가 많습니다. 그래서 CoT를 과도하게 쓰면 비용이 빠르게 증가합니다.

전환: 이제 4가지 최적화 전략을 알아보겠습니다.
시간: 4분
-->

---

# 4가지 최적화 전략

<div class="grid grid-cols-2 gap-3 mt-2">

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3">
<strong>① 모델 라우팅</strong><br>
작업 복잡도에 따라 경량/고급 모델을 동적 선택<br>
<span class="text-sm">단순 분류 → gpt-5-mini / 복잡한 판단 → claude-sonnet-4-6</span>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3">
<strong>② 프롬프트 캐싱</strong><br>
반복되는 시스템 프롬프트·Tool 스키마를 캐싱<br>
<span class="text-sm">캐시 히트 시 <strong>최대 90% 절감</strong></span>
</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3">
<strong>③ 병렬 호출</strong><br>
상호 의존이 없는 Tool 호출을 동시에 실행<br>
<span class="text-sm">순차: 3개 × 2초 = 6초 → 병렬: max(2초) = 2초</span>
</div>

<div class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-3">
<strong>④ 대화 이력 압축</strong><br>
오래된 이력을 요약으로 대체<br>
<span class="text-sm">최근 3턴은 원본 유지, 이전 이력은 요약</span>
</div>

</v-clicks>

</div>

<v-click>

<div class="mt-4 bg-green-50 dark:bg-green-900/30 rounded-lg p-3 text-center font-bold">

4가지 조합 시: 비용 <strong>86% 절감</strong> ($0.0500 → $0.0072), 지연 <strong>49% 단축</strong> (18.5초 → 9.5초)

</div>

</v-click>

<!--
[스크립트]
4가지 최적화 전략을 설명하겠습니다.

[클릭] 첫 번째는 모델 라우팅입니다. 작업의 복잡도에 따라 다른 모델을 씁니다. 단순 분류는 gpt-5-mini처럼 저렴한 경량 모델을, 복잡한 판단은 claude-sonnet-4-6 같은 고급 모델을 씁니다. 대부분의 요청이 경량 모델로 처리되면 전체 비용이 크게 줄어듭니다.

[클릭] 두 번째는 프롬프트 캐싱입니다. Agent는 매 턴마다 동일한 시스템 프롬프트와 Tool 스키마를 보냅니다. 이 반복되는 부분을 서버 측에서 캐싱합니다. Anthropic과 OpenAI 모두 캐시된 입력 비용을 크게 줄일 수 있습니다.

[클릭] 세 번째는 병렬 호출입니다. 예를 들어 고객 정보 조회, 주문 이력 조회, 재고 확인을 동시에 실행할 수 있습니다. 순차 실행 6초가 병렬로 2초가 됩니다.

[클릭] 네 번째는 대화 이력 압축입니다. 오래된 대화 이력을 요약으로 대체합니다. 최근 3턴의 원본은 유지하고 이전 이력은 요약해서 압축합니다. 누적 입력 토큰의 폭발적 증가를 막을 수 있습니다.

[클릭] 4가지 전략을 모두 조합하면 실제로 비용 86% 절감, 지연 49% 단축 효과가 나타납니다.

[Q&A 대비]
Q: 모델 라우팅에서 경량 모델이 실수하면 어떻게 하나요?
A: Fallback 패턴을 사용합니다. 경량 모델의 confidence score가 임계값 이하면 상위 모델로 재요청합니다. 대부분의 요청이 경량 모델로 처리되므로 전체 비용은 크게 절감됩니다.

전환: 코드로 최적화 전략을 구현하는 방법을 보겠습니다.
시간: 5분
-->

---

# 최적화 코드 구현 (3가지 예시)

```python {1-14|16-25|27-35}{maxHeight:'380px'}
# 전략 1: 모델 라우팅
class ModelRouter:
    MODELS = {
        "simple":   "gpt-5-mini",         # 빠르고 저렴
        "moderate": "gpt-5.2",            # 균형
        "complex":  "claude-sonnet-4-6",  # 정확
    }

    def select_model(self, task_type: str) -> str:
        if task_type in ["classify", "extract", "format"]:
            return self.MODELS["simple"]
        elif task_type in ["analyze", "summarize"]:
            return self.MODELS["moderate"]
        else:  # plan, decide, reason
            return self.MODELS["complex"]


# 전략 2: 병렬 호출 (asyncio)
async def parallel_tool_calls(tools_to_call: list[dict]) -> list:
    async def call_tool(tool_config):
        result = await tool_config["fn"](**tool_config["params"])
        return {"tool": tool_config["name"], "result": result}

    return await asyncio.gather(*[call_tool(tc) for tc in tools_to_call])


# 전략 3: 대화 이력 압축
class ContextCompressor:
    def compress(self, history: list[dict], max_tokens: int = 2000) -> list[dict]:
        if self.estimate_tokens(history) <= max_tokens:
            return history
        recent = history[-6:]   # 최근 3턴 원본 유지
        older  = history[:-6]
        summary = self.summarize(older)
        return [{"role": "system", "content": f"이전 대화 요약: {summary}"}, *recent]
```

<!--
[스크립트]
세 가지 최적화 전략의 구현 코드입니다. 프롬프트 캐싱은 플랫폼이 자동 처리하므로 코드 예시에서는 제외했습니다.

[클릭] 모델 라우팅입니다. task_type에 따라 다른 모델을 선택합니다. classify나 extract처럼 단순한 작업은 gpt-5-mini로, plan이나 decide처럼 복잡한 작업은 claude-sonnet-4-6으로 라우팅합니다.

[클릭] 병렬 호출입니다. asyncio.gather를 사용하여 여러 Tool 호출을 동시에 실행합니다. 각 Tool은 독립적으로 실행되고 모든 결과가 완료되면 함께 반환됩니다.

[클릭] 대화 이력 압축입니다. 전체 이력이 max_tokens를 초과하면 압축을 시작합니다. 최근 6개 메시지(3턴)는 원본을 유지하고, 이전 이력은 요약으로 대체합니다. 요약된 내용은 시스템 메시지 형태로 앞에 붙입니다.

[DEMO] 실제 10턴 시뮬레이션을 실행해보면 최적화 전후 비용 차이를 직접 확인할 수 있습니다. 이것이 실습 3에서 다룰 내용입니다.

[Q&A 대비]
Q: 프롬프트 캐싱은 어떻게 구현하나요?
A: 별도 구현이 필요 없습니다. OpenAI와 Anthropic 모두 자동 프롬프트 캐싱을 지원합니다. 동일한 시스템 프롬프트 접두사가 반복되면 서버 측에서 자동으로 캐싱합니다. Agent는 매 턴 동일한 시스템 프롬프트를 보내므로 캐싱 효과가 큽니다.

전환: 전체 내용을 정리하겠습니다.
시간: 4분
-->

---

# Session 2 핵심 정리

<v-clicks>

- **Token** — LLM의 처리 단위. 한국어는 영어 대비 **2~3배 토큰 소비**
- **Context Window** — 입력+출력 합계의 상한. Agent 설계 시 실제 가용 공간 계산 필수
- **Hallucination** — Agent에서 가장 위험. 잘못된 판단이 실제 행동으로 실행됨
- **프롬프트 전략** — 단순 → Zero-shot, 패턴 → Few-shot, 복잡한 판단 → CoT
- **Structured Output** — Agent의 필수 요소. 자연어 파싱은 깨지고, JSON Schema가 안정적
- **비용 최적화** — 모델 라우팅 + 대화 이력 압축 + 프롬프트 캐싱 = **80%+ 절감**

</v-clicks>

<v-click>

<div class="mt-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-center">

**오늘의 핵심**: LLM을 블랙박스로 쓰면 Agent는 실패한다.
**원리를 알면 설계하고, 원리를 모르면 디버깅만 한다.**

</div>

</v-click>

<!--
[스크립트]
Session 2의 핵심 내용을 정리하겠습니다.

[클릭] Token — LLM의 처리 단위입니다. 한국어는 영어 대비 2~3배 토큰을 소비합니다. 시스템 프롬프트를 영어로 작성하는 것이 비용 최적화의 첫걸음입니다.

[클릭] Context Window — 입력과 출력 합계의 상한입니다. Agent 설계 시 시스템 프롬프트, Tool 스키마, 대화 이력을 모두 고려한 실제 가용 공간을 계산해야 합니다.

[클릭] Hallucination — Agent에서 가장 위험합니다. 잘못된 판단이 실제 행동으로 실행되기 때문입니다. Grounding, Validation, Confirmation 등 완화 전략을 조합해야 합니다.

[클릭] 프롬프트 전략 — 복잡도에 따라 선택합니다. 단순하면 Zero-shot, 패턴이 있으면 Few-shot, 복잡한 판단은 CoT를 씁니다. 하나의 Agent 안에서도 단계마다 다르게 적용하는 적응형 전략이 효과적입니다.

[클릭] Structured Output — Agent의 필수 요소입니다. 자연어 파싱은 반드시 깨집니다. Pydantic과 JSON Schema로 LLM의 출력 형식을 강제해야 합니다.

[클릭] 비용 최적화 — 모델 라우팅, 대화 이력 압축, 프롬프트 캐싱을 조합하면 80% 이상 절감이 가능합니다.

[클릭] 오늘의 핵심 메시지입니다. LLM을 블랙박스로 쓰면 Agent는 실패합니다. 원리를 알면 설계하고, 원리를 모르면 디버깅만 합니다. 이 6가지 개념은 여러분이 Agent를 설계하는 모든 순간에 적용됩니다.

[Q&A 대비]
Q: 가장 먼저 적용해야 할 최적화가 있다면?
A: Structured Output을 먼저 적용하세요. 비용보다 안정성이 우선입니다. 자연어 파싱은 언제든 깨질 수 있고, 그것이 Agent 전체를 중단시킵니다. Structured Output으로 기반을 다진 뒤 모델 라우팅으로 비용을 최적화하세요.

전환: 실습 안내로 넘어가겠습니다.
시간: 3분
-->

---

# 실습 안내

<div class="grid grid-cols-3 gap-4 mt-2">

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">

**실습 1** (30분)

프롬프트 전략별 응답 비교

- Zero-shot / Few-shot / CoT 직접 구현
- 5가지 고객 문의에 적용
- 결과·비용·토큰 수 비교 표 작성

**난이도**: 기초

</div>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

**실습 2** (35분)

Structured Output으로 행동 결정 구현

- `AgentDecision` 스키마 완성
- 비즈니스 규칙 검증 로직 추가
- 5가지 고객 시나리오 적용

**난이도**: 중급

</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4">

**실습 3** (25분)

비용 최적화 시뮬레이션

- 모델 라우팅 + 이력 압축 구현
- 4가지 설정 조합 비교
- 최적 전략 선택 근거 제시

**난이도**: 심화

</div>

</div>

<!--
[스크립트]
이제 실습 시간입니다. 오늘 배운 내용을 직접 코드로 확인하는 시간입니다.

왼쪽부터 순서대로 실습합니다.

실습 1은 30분 동안 프롬프트 전략을 직접 구현하고 비교합니다. 5가지 고객 문의에 Zero-shot, Few-shot, CoT를 각각 적용하고 결과와 토큰 수를 비교표로 작성합니다.

실습 2는 35분 동안 Structured Output을 구현합니다. AgentDecision 스키마를 완성하고 비즈니스 규칙 검증 로직을 추가합니다.

실습 3은 25분 동안 비용 최적화 시뮬레이터를 구현합니다. 4가지 설정 조합으로 실행하고 최적 전략을 선택하는 근거를 제시합니다.

[Q&A 대비]
Q: 실습 환경은 어떻게 준비하나요?
A: 실습에 사용할 API 키와 Python 패키지가 필요합니다. 실습 가이드 README.md를 참고해서 환경 변수를 설정하면 됩니다. `pip install openai pydantic tiktoken`으로 패키지를 설치하면 바로 시작할 수 있습니다.

전환: 실습 파일을 열고 시작해주세요. 막히는 부분은 언제든지 질문해주세요.
시간: 2분
-->

---
layout: section
transition: fade
---

# Session 3
## Agent 기획서 구조화

<!--
[스크립트]
자, 이제 Session 3로 넘어가겠습니다. 지금까지 Session 1에서 비즈니스 Pain을 발굴하고 Agent 후보를 도출했습니다. Session 2에서는 아키텍처 선택까지 마쳤고요. 이번 세션에서는 그 후보를 실제로 "구현 가능한 기획서"로 만드는 방법을 배웁니다. 기획서는 코딩의 출발점이자, 기획자·개발자·이해관계자 세 그룹이 서로 오해 없이 소통하는 유일한 도구입니다. 2시간 안에 여러분이 직접 기획서를 완성해 가져가실 수 있도록 설계했습니다. 시작하겠습니다.

[Q&A 대비]
Q: Session 2 아직 못 들었는데 Session 3만 들어도 되나요?
A: 네, Session 3는 독립적으로 이해 가능합니다. 핵심은 "비즈니스 문제 → 기획서 → 기술 설계" 변환 흐름이며, 이전 세션 지식이 없어도 따라올 수 있습니다.

전환: "먼저, 왜 기획서 없이 시작하면 안 되는지부터 살펴보겠습니다."
시간: 1분
-->

---

# 기획서 없이 시작하면 생기는 일

<div class="text-xl text-center mt-6 mb-6 bg-red-50 dark:bg-red-900/30 rounded-lg p-4">
2026년에도 반복되는 AI 프로젝트 실패 패턴 → <strong>불명확한 요구사항</strong>
</div>

<v-clicks>

- FAQ 봇이 어느새 주문 관리까지 담당하게 됨 → **범위 무한 확장**
- "잘 되는 건지" 아무도 판단 불가 → **성공 기준 부재**
- 개발자는 JSON 반환, 기획자는 자연어 기대 → **입출력 불일치**
- Agent가 고객 개인정보를 외부 API로 전송 → **제약조건 누락**

</v-clicks>

<!--
[스크립트]
지금도 요구사항이 흐린 상태에서 AI 프로젝트를 시작하면 같은 문제가 반복됩니다. 기획서 없이 시작하면 반드시 네 가지 문제가 발생합니다.

[클릭] 첫 번째, 범위 무한 확장입니다. FAQ 봇으로 시작했는데 어느 순간 주문 취소, 환불 처리까지 담당하게 됩니다. "이 기능도 넣으면 좋지 않아요?" 요청이 끊임없이 들어오기 때문입니다.

[클릭] 두 번째, 성공 기준이 없습니다. 프로젝트가 끝났는데 "잘 된 건가요?"라고 물으면 아무도 답을 못 합니다. 숫자로 된 목표가 없기 때문입니다.

[클릭] 세 번째, 입출력 불일치입니다. 개발자는 JSON 구조체를 반환하도록 만들었는데, 기획자는 자연어 문장을 기대하는 상황이 생깁니다.

[클릭] 네 번째이자 가장 심각한 문제입니다. 제약조건 누락으로 Agent가 고객 개인정보를 외부 API로 전송하는 일이 실제로 발생합니다. 보안 위반이죠.

[Q&A 대비]
Q: 스타트업이라 빠르게 만들어야 하는데 기획서에 시간 쓸 여유가 없어요.
A: MVP 기준으로 A4 2장이면 충분합니다. 기획서 작성에 하루 투자하면 잘못된 구현으로 낭비할 2주를 아낄 수 있습니다.

전환: "그러면 기획서가 정확히 어떤 역할을 하는지 보겠습니다."
시간: 3분
-->

---

# 기획서의 역할: 두 세계의 번역

<div class="grid grid-cols-[1fr_auto_1fr] gap-4 mt-8 items-center overflow-hidden">

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-5 text-center">
<div class="text-lg font-bold text-blue-700 dark:text-blue-300 mb-3">비즈니스팀</div>

- "고객 문의 응답 시간을 줄이고 싶다"
- "CS팀이 너무 힘들다"
- "24시간 응대가 필요하다"

</div>

<div class="text-3xl text-gray-400 font-bold">⟷</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-5 text-center">
<div class="text-lg font-bold text-green-700 dark:text-green-300 mb-3">개발팀</div>

- "LLM API 호출"
- "JSON 스키마 반환"
- "confidence 0.7 임계값"

</div>

</div>

<div class="mt-6 text-center text-lg bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-3">
기획서 = 비즈니스 문제와 기술 구현 사이의 <strong>번역 문서</strong>
</div>

<!--
[스크립트]
기획서가 왜 필요한지 직관적으로 이해하실 수 있도록 그림으로 설명하겠습니다. 왼쪽은 비즈니스팀이 쓰는 언어입니다. "응답 시간을 줄이고 싶다", "CS팀이 힘들다"처럼 사람의 언어로 이야기합니다. 오른쪽은 개발팀의 언어입니다. "LLM API 호출", "JSON 스키마", "confidence 0.7"처럼 기술 언어를 씁니다. 이 두 언어 사이에 통역사가 없으면 서로 다른 걸 만들게 됩니다. 기획서가 바로 그 번역 문서입니다. 비즈니스 언어를 기술 언어로 정확하게 변환해주는 역할이죠.

[Q&A 대비]
Q: 기획서를 누가 작성해야 하나요? 기획자인가요, 개발자인가요?
A: 기획자(또는 PM)가 주도하고 개발자가 검토하는 구조가 이상적입니다. AI Agent 기획은 LLM의 한계를 이해해야 하므로 개발자가 기획 단계부터 반드시 참여해야 합니다.

전환: "이 번역을 어떻게 하는지, 3단계로 설명드리겠습니다."
시간: 2분
-->

---

# 비즈니스 문제 → 기획서 변환 3단계

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 mb-3">
<strong>① 비즈니스 문제 정의</strong><br>
고통점과 현재 프로세스를 <em>수치</em>로 파악한다<br>
<span class="text-sm text-gray-500">예: "CS팀 5명이 하루 200건 문의, 70%가 반복 질문, 평균 응답 2시간"</span>
</div>

<div class="bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-4 mb-3">
<strong>② Agent 기회 식별</strong><br>
자동화 대상 vs 사람 개입 필요를 구분한다<br>
<span class="text-sm text-gray-500">예: "FAQ 검색·답변 초안 작성 → 자동화 / 에스컬레이션 판단 → 사람"</span>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4 mb-3">
<strong>③ Agent 기획서 생성</strong><br>
6가지 구성요소로 명세화한다<br>
<span class="text-sm text-gray-500">목적 · 입력 · 출력 · 제약조건 · 성공 기준 · 범위 경계</span>
</div>

</v-clicks>

<!--
[스크립트]
비즈니스 문제를 기획서로 변환하는 과정은 3단계입니다.

[클릭] 첫 번째 단계는 비즈니스 문제 정의입니다. 막연한 고통점을 수치로 표현합니다. "CS팀이 힘들다"가 아니라 "5명이 하루 200건을 처리하고 70%가 반복 질문이며 평균 응답 시간이 2시간"처럼 구체화합니다.

[클릭] 두 번째 단계는 Agent 기회 식별입니다. 현재 수동 프로세스의 각 단계를 "자동화 가능"과 "사람 개입 필요"로 분류합니다. "수동 반복" 태그가 붙은 단계가 Agent의 먹잇감입니다.

[클릭] 세 번째 단계가 핵심입니다. 6가지 구성요소로 Agent를 완전히 명세화합니다. 이 6가지가 무엇인지는 다음 슬라이드에서 자세히 다루겠습니다.

[Q&A 대비]
Q: 1단계에서 수치가 없으면 어떻게 하나요?
A: 추정치라도 구합니다. 팀장 인터뷰, 업무 일지, 타임 트래킹 툴 등을 활용합니다. "약 2시간 정도로 추정"도 충분합니다.

전환: "이제 기획서의 핵심인 6가지 구성요소를 하나씩 살펴보겠습니다."
시간: 3분
-->

---

# 6가지 구성요소: 기획서의 뼈대

<div class="text-center mb-4 text-gray-500">각 구성요소는 기획자·개발자·이해관계자 간의 <strong>계약(Contract)</strong></div>

<div class="grid grid-cols-3 gap-3 overflow-hidden">

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 text-center">
<div class="text-2xl mb-1">🎯</div>
<div class="font-bold">목적</div>
<div class="text-sm text-gray-500">Agent의 존재 이유 한 문장</div>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 text-center">
<div class="text-2xl mb-1">📥</div>
<div class="font-bold">입력</div>
<div class="text-sm text-gray-500">받는 데이터와 트리거</div>
</div>

<div class="bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-3 text-center">
<div class="text-2xl mb-1">📤</div>
<div class="font-bold">출력</div>
<div class="text-sm text-gray-500">생성하는 결과물</div>
</div>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3 text-center">
<div class="text-2xl mb-1">🔒</div>
<div class="font-bold">제약조건</div>
<div class="text-sm text-gray-500">해서는 안 될 것</div>
</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3 text-center">
<div class="text-2xl mb-1">📊</div>
<div class="font-bold">성공 기준</div>
<div class="text-sm text-gray-500">측정 가능한 목표</div>
</div>

<div class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-3 text-center">
<div class="text-2xl mb-1">🗺️</div>
<div class="font-bold">범위 경계</div>
<div class="text-sm text-gray-500">In / Out of Scope</div>
</div>

</v-clicks>

</div>

<!--
[스크립트]
Agent 기획서는 6가지 핵심 구성요소로 이루어집니다. 하나씩 소개하겠습니다.

[클릭] 첫 번째, 목적입니다. Agent가 왜 존재하는지를 한 문장으로 씁니다. "고객 서비스를 개선한다"가 아니라 "CS팀의 FAQ 자동 답변으로 응답 시간을 2시간에서 30초로 단축한다"처럼요.

[클릭] 두 번째, 입력입니다. Agent가 무엇을 받는지입니다. 타입, 최대 길이, 언어, 예시까지 명시합니다.

[클릭] 세 번째, 출력입니다. Agent가 무엇을 반환하는지입니다. JSON 필드 하나하나까지 정의합니다.

[클릭] 네 번째, 제약조건입니다. Agent가 절대 해서는 안 되는 것입니다. 보안·비즈니스·기술 세 유형으로 나눠 작성합니다.

[클릭] 다섯 번째, 성공 기준입니다. 수치와 측정 방법이 반드시 포함되어야 합니다. "잘 동작한다"는 성공 기준이 아닙니다.

[클릭] 여섯 번째, 범위 경계입니다. "무엇을 한다"만큼 "무엇을 안 한다"가 중요합니다. 이 항목이 없으면 범위 팽창이 100% 발생합니다.

전환: "이 6가지가 어떻게 서로 연결되는지 보겠습니다."
시간: 3분
-->

---

# 기획서 핵심 항목의 연쇄 연결

<div class="mt-6 overflow-hidden">

<div class="flex items-center justify-center gap-2 flex-wrap">

<v-clicks>

<div class="bg-blue-100 dark:bg-blue-900/40 rounded-lg px-4 py-2 font-bold text-blue-700 dark:text-blue-300">목적</div>
<div class="text-gray-400">→ 범위 결정</div>
<div class="bg-orange-100 dark:bg-orange-900/40 rounded-lg px-4 py-2 font-bold text-orange-700 dark:text-orange-300">범위</div>
<div class="text-gray-400">→ 입출력 결정</div>
<div class="bg-green-100 dark:bg-green-900/40 rounded-lg px-4 py-2 font-bold text-green-700 dark:text-green-300">입출력</div>
<div class="text-gray-400">→ 제약 도출</div>
<div class="bg-red-100 dark:bg-red-900/40 rounded-lg px-4 py-2 font-bold text-red-700 dark:text-red-300">제약조건</div>
<div class="text-gray-400">→ 측정 방식 결정</div>
<div class="bg-purple-100 dark:bg-purple-900/40 rounded-lg px-4 py-2 font-bold text-purple-700 dark:text-purple-300">성공 기준</div>

</v-clicks>

</div>

</div>

<v-click>

<div class="mt-8 bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-sm">
<strong>핵심 원칙:</strong> 어느 한 구성요소라도 누락되면 계약이 불완전해진다.<br>
불완전한 계약 → 프로젝트 실패
</div>

</v-click>

<!--
[스크립트]
기획서 핵심 항목들은 독립된 항목이 아니라 연쇄적으로 연결되어 있습니다. 이 화면에서는 입력과 출력을 하나의 흐름으로 묶어 보겠습니다.

[클릭] 목적이 범위를 결정합니다. "FAQ 자동 답변"이 목적이라면 범위는 "FAQ와 관련된 것들"입니다.

[클릭] 범위가 입출력을 결정합니다. FAQ 범위라면 입력은 "고객 문의 텍스트"이고 출력은 "FAQ 답변과 신뢰도 점수"가 됩니다.

[클릭] 입출력이 제약조건을 도출합니다. 고객 메시지를 받는다면 "PII 포함 금지" 제약이 자연스럽게 나옵니다.

[클릭] 제약조건이 성공 기준의 측정 방식을 결정합니다. "PII 감지 정확도 99% 이상"처럼 제약에서 측정 지표가 나옵니다.

[클릭] 결론적으로 하나라도 빠지면 체인이 끊깁니다. 목적 없는 제약은 방향을 잃고, 성공 기준 없는 구현은 완성을 알 수 없습니다.

[Q&A 대비]
Q: 항목을 작성하는 순서가 중요한가요?
A: 목적 → 범위 → 입출력 → 제약 → 성공 기준 순서로 작성하는 것이 권장됩니다. 앞 항목이 뒤 항목의 기반이 되기 때문입니다.

전환: "각 구성요소를 좋은 예와 나쁜 예로 비교해보겠습니다."
시간: 3분
-->

---

# 좋은 기획서 vs 나쁜 기획서: 목적과 입출력

<div class="grid grid-cols-2 gap-6 mt-4 overflow-hidden">

<div>
<div class="text-center font-bold text-red-600 mb-3 text-lg">나쁜 기획서</div>
<v-clicks>
<div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-3 mb-2 text-sm">
<strong>목적:</strong> "고객 서비스를 개선한다"<br>
<span class="text-red-500">→ 10명이 읽으면 10가지 해석</span>
</div>
<div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-3 mb-2 text-sm">
<strong>입력:</strong> "고객 데이터"<br>
<span class="text-red-500">→ 무슨 데이터? 어떤 형식?</span>
</div>
<div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-3 text-sm">
<strong>출력:</strong> "적절한 답변"<br>
<span class="text-red-500">→ JSON? 텍스트? 어떤 필드?</span>
</div>
</v-clicks>
</div>

<div>
<div class="text-center font-bold text-green-600 mb-3 text-lg">좋은 기획서</div>
<v-clicks>
<div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 mb-2 text-sm">
<strong>목적:</strong> "응답 시간 2시간 → 30초 단축"<br>
<span class="text-green-600">→ 모두가 동일하게 이해</span>
</div>
<div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 mb-2 text-sm">
<strong>입력:</strong> "텍스트, 최대 2000자, 한국어/영어"<br>
<span class="text-green-600">→ 타입 + 제한 + 언어 명시</span>
</div>
<div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 text-sm">
<strong>출력:</strong> "JSON: category, confidence, reply"<br>
<span class="text-green-600">→ 필드 하나하나까지 정의</span>
</div>
</v-clicks>
</div>

</div>

<!--
[스크립트]
좋은 기획서와 나쁜 기획서의 차이는 단 하나, 구체성입니다. 왼쪽 나쁜 기획서와 오른쪽 좋은 기획서를 비교해보겠습니다.

[클릭] 나쁜 목적: "고객 서비스를 개선한다." 이 문장을 10명한테 읽히면 10가지 다른 해석이 나옵니다.

[클릭] 좋은 목적: "응답 시간을 2시간에서 30초로 단축한다." 모든 사람이 동일하게 이해합니다. 수치가 있으니까요.

[클릭] 나쁜 입력: "고객 데이터." 무슨 데이터인지, 어떤 형식인지 전혀 알 수 없습니다.

[클릭] 좋은 입력: "텍스트, 최대 2000자, 한국어·영어." 타입과 제한과 언어까지 명시했습니다.

[클릭] 나쁜 출력: "적절한 답변." 개발자 입장에서 이걸 보면 막막합니다.

[클릭] 좋은 출력: JSON에 어떤 필드가 들어가는지까지 정의했습니다.

[잠깐 멈춤] 여기서 핵심 질문을 드립니다. "이 문장을 읽는 사람이 다르게 해석할 여지가 없는가?" 이 기준으로 본인의 기획서를 검토하시면 됩니다.

전환: "제약조건과 성공 기준도 같은 방식으로 비교해보겠습니다."
시간: 3분
-->

---

# 좋은 기획서 vs 나쁜 기획서: 제약과 성공 기준

<div class="grid grid-cols-2 gap-6 mt-4 overflow-hidden">

<div>
<div class="text-center font-bold text-red-600 mb-3 text-lg">나쁜 기획서</div>
<v-clicks>
<div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-3 mb-2 text-sm">
<strong>제약:</strong> "보안을 지킨다"<br>
<span class="text-red-500">→ 무엇을? 어떻게?</span>
</div>
<div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-3 text-sm">
<strong>성공 기준:</strong> "잘 동작한다"<br>
<span class="text-red-500">→ 측정 불가, 주관적 판단</span>
</div>
</v-clicks>
</div>

<div>
<div class="text-center font-bold text-green-600 mb-3 text-lg">좋은 기획서</div>
<v-clicks>
<div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 mb-2 text-sm">
<strong>제약:</strong> "고객 PII(이름·전화번호)를 LLM 프롬프트에 포함 금지. 위반 시 개인정보보호법 위반"<br>
<span class="text-green-600">→ 대상 + 방법 + 위반 영향</span>
</div>
<div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 text-sm">
<strong>성공 기준:</strong> "정확도 90% 이상, 주간 50건 샘플링"<br>
<span class="text-green-600">→ 수치 + 측정 방법 명시</span>
</div>
</v-clicks>
</div>

</div>

<!--
[스크립트]
제약조건과 성공 기준도 같은 원칙이 적용됩니다.

[클릭] 나쁜 제약: "보안을 지킨다." 개발자 셋이 이걸 읽으면 각자 다르게 구현합니다.

[클릭] 좋은 제약: 무엇을 금지하는지(PII), 왜 금지하는지(개인정보보호법 위반), 위반하면 어떤 영향이 있는지까지 명시합니다.

[클릭] 나쁜 성공 기준: "잘 동작한다." 이건 기준이 아닙니다. 누가 판단하냐에 따라 결과가 달라집니다.

[클릭] 좋은 성공 기준: "정확도 90% 이상, 주간 50건 샘플링." 수치와 측정 방법이 있어야 비로소 성공 기준입니다.

[Q&A 대비]
Q: 성공 기준의 수치를 처음에 어떻게 정하나요? 근거가 없는데요.
A: 3단계 접근법을 씁니다. 먼저 현재 수동 프로세스 수준을 측정합니다. 그 다음 업계 벤치마크를 참고합니다. MVP에서는 "현재와 동등 이상"을 목표로 설정합니다. 처음부터 99%를 목표로 하면 프로젝트가 끝나지 않습니다.

전환: "이제 범위 경계, 즉 In/Out of Scope를 살펴보겠습니다."
시간: 3분
-->

---

# 범위 경계: 가장 많은 논쟁이 벌어지는 항목

<div class="grid grid-cols-2 gap-6 mt-6 overflow-hidden">

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-5">
<div class="font-bold text-green-700 dark:text-green-300 text-lg mb-3 text-center">✅ In Scope</div>
<v-clicks>

- FAQ 자동 답변
- 주문 상태 조회
- 문의 카테고리 분류
- 처리 불가 문의 에스컬레이션

</v-clicks>
</div>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-5">
<div class="font-bold text-red-700 dark:text-red-300 text-lg mb-3 text-center">❌ Out of Scope</div>
<v-clicks>

- 환불·결제 처리
- 고객 감정 케어
- 실시간 음성 통화

</v-clicks>
</div>

</div>

<v-click>

<div class="mt-4 bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-3 text-sm text-center">
Out of Scope 문서화 → "기획서에 Out of Scope"라고 객관적 대응 가능
</div>

</v-click>

<!--
[스크립트]
실제 프로젝트에서 가장 많은 논쟁이 벌어지는 항목이 바로 범위 경계입니다.

[클릭] In Scope, 즉 Agent가 하는 일입니다. FAQ 자동 답변, 주문 상태 조회, 카테고리 분류, 에스컬레이션이 이 Agent의 역할입니다.

[클릭] Out of Scope, Agent가 하지 않는 일입니다. 환불 처리, 감정 케어, 음성 통화는 이 Agent가 담당하지 않습니다.

[클릭] Out of Scope를 문서화하는 핵심 이유가 있습니다. "이 기능도 넣으면 좋지 않아요?"라는 요청이 들어올 때, 주관적으로 거절하면 논쟁이 됩니다. 하지만 "기획서에 Out of Scope로 명시되어 있습니다"라고 하면 객관적으로 대응할 수 있습니다.

[Q&A 대비]
Q: Out of Scope로 잡았는데 나중에 필요해지면 어떻게 하나요?
A: 이해관계자 회의를 열어 기획서를 공식 업데이트합니다. 기획서는 "살아있는 문서(Living Document)"입니다. 단, 업데이트 기록을 남겨야 합니다.

Q: 회색 지대는 어떻게 처리하나요?
A: 불명확한 영역은 기본적으로 Out of Scope에 넣습니다. 나중에 명시적으로 결정되면 In으로 이동합니다.

전환: "지금까지 배운 6가지 구성요소를 실제 코드로 표현해보겠습니다."
시간: 3분
-->

---
layout: two-cols-header
---

# 기획서를 코드로 표현하기

::left::

```python {1-8|10-18|all}
from dataclasses import dataclass, field

@dataclass
class AgentSpecTemplate:
    """Agent 기획서 표준 템플릿"""
    purpose: str                        # 1. 목적
    inputs: list[dict] = field(...)     # 2. 입력
    outputs: list[dict] = field(...)    # 3. 출력
    constraints: list[dict] = field(...) # 4. 제약조건
    success_criteria: list[dict] = field(...) # 5. 성공 기준
    in_scope: list[str] = field(...)    # 6. 범위 - In
    out_of_scope: list[str] = field(...) # 6. 범위 - Out
```

::right::

<v-clicks>

```python
cs_agent_spec = AgentSpecTemplate(
    purpose="FAQ 자동 처리로 응답 시간"
            "2시간 → 30초 단축",
    inputs=[{
        "name": "customer_message",
        "max_length": 2000,
        "language": ["ko", "en"],
    }],
    success_criteria=[{
        "metric": "응답 정확도",
        "target": "90% 이상",
        "measurement": "주간 50건",
    }],
)
```

</v-clicks>

<!--
[스크립트]
6가지 구성요소를 Python 데이터클래스로 표현하면 이렇게 됩니다.

[클릭] 먼저 purpose부터 out_of_scope까지 6개 필드가 기획서의 6가지 구성요소와 1:1로 대응됩니다. 코드가 곧 기획서 구조입니다.

[클릭] 실제 값을 대표 필드만 채우면 이렇게 됩니다. purpose에 정량적 목표를 씁니다. inputs에 타입, 길이, 언어를 명시합니다. success_criteria에 수치와 측정 방법을 넣습니다. 나머지 outputs, constraints, in_scope, out_of_scope를 채우면 완전한 기획서가 됩니다.

[DEMO] 실제로 이 코드를 실행하면 기획서 품질을 자동으로 검증하는 validate_spec_quality() 함수와 연동할 수 있습니다. 잠시 후 실습에서 직접 해보겠습니다.

[Q&A 대비]
Q: 기획서를 꼭 코드로 작성해야 하나요?
A: 아닙니다. Notion 테이블, Confluence 문서, Google Docs 어디든 좋습니다. 코드로 표현하는 이유는 기계가 읽고 검증할 수 있기 때문입니다. 특히 validate_spec_quality() 같은 자동 검증 함수를 활용할 때 유용합니다.

전환: "기획서 품질을 자동으로 검증하는 방법을 살펴보겠습니다."
시간: 3분
-->

---

# 기획서 품질 자동 검증

```python {1-6|8-14|16-20}{maxHeight:'350px'}
def validate_spec_quality(spec: dict) -> dict:
    score = 0
    issues = []

    # 목적: 구체적 행동 + 정량적 목표
    if len(spec.get("purpose","")) > 20 and "단축" in spec["purpose"]:
        score += 1

    # 제약조건: 보안 + 비즈니스 + 기술 3종 필수
    types = {c.get("type") for c in spec.get("constraints", [])}
    if {"보안", "비즈니스", "기술"}.issubset(types):
        score += 1

    # 성공 기준: 수치 + 측정 방법
    criteria = spec.get("success_criteria", [])
    if all("target" in c and "measurement" in c for c in criteria):
        score += 1

    grade = "A" if score == 3 else "B" if score == 2 else "C"
    return {"score": f"{score}/3", "grade": grade, "issues": issues}
```

<div class="mt-3 grid grid-cols-2 gap-4">
<div class="bg-green-50 dark:bg-green-900/30 rounded p-2 text-center text-sm">좋은 기획서: <strong>A (3/3)</strong></div>
<div class="bg-red-50 dark:bg-red-900/30 rounded p-2 text-center text-sm">나쁜 기획서: <strong>C (0/3)</strong></div>
</div>

<!--
[스크립트]
기획서를 작성한 뒤 품질을 손으로 검토하는 것은 주관적입니다. 그래서 코드로 자동 검증합니다.

[클릭] 첫 번째 검증: 목적에 구체적 행동과 정량적 목표가 있는가를 확인합니다. 이 예시 코드에서는 "단축" 키워드가 있는지를 대표 조건으로 보여줍니다.

[클릭] 두 번째 검증: 제약조건에 보안·비즈니스·기술 세 유형이 모두 있는가를 확인합니다. 하나라도 빠지면 감점입니다.

[클릭] 세 번째 검증: 성공 기준 모두에 수치 목표(target)와 측정 방법(measurement)이 있는가를 확인합니다. 화면에는 대표 3개 체크만 보여주지만, 실제로는 나머지 항목도 같은 방식으로 확장할 수 있습니다.

결과적으로 좋은 기획서는 A 등급, 나쁜 기획서는 C 등급이 나옵니다. 실습에서는 이 대표 검증을 먼저 통과시키고, 이후 나머지 항목도 확장해보겠습니다.

전환: "이제 기획서에서 기술 설계로 넘어가는 방법을 알아보겠습니다."
시간: 2분
-->

---

# 기획서 → 기술 설계: 1:1 매핑

<div class="grid grid-cols-3 gap-2 mt-2">

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3">
  <div class="font-bold text-blue-700 dark:text-blue-300">목적</div>
  <div class="text-sm mt-1">→ 아키텍처 선택</div>
  <div class="text-xs text-gray-500 mt-1">멀티스텝 자동화 → Agent</div>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3">
  <div class="font-bold text-green-700 dark:text-green-300">입력</div>
  <div class="text-sm mt-1">→ API 인터페이스</div>
  <div class="text-xs text-gray-500 mt-1">텍스트 2000자 → 토큰 제한</div>
</div>

<div class="bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-3">
  <div class="font-bold text-yellow-700 dark:text-yellow-300">출력</div>
  <div class="text-sm mt-1">→ 응답 스키마</div>
  <div class="text-xs text-gray-500 mt-1">JSON → Pydantic BaseModel</div>
</div>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3">
  <div class="font-bold text-red-700 dark:text-red-300">제약조건</div>
  <div class="text-sm mt-1">→ Guardrail</div>
  <div class="text-xs text-gray-500 mt-1">PII 금지 → 마스킹 레이어</div>
</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3">
  <div class="font-bold text-purple-700 dark:text-purple-300">성공 기준</div>
  <div class="text-sm mt-1">→ 테스트·모니터링</div>
  <div class="text-xs text-gray-500 mt-1">정확도 90% → Golden Test Set 50건</div>
</div>

<div class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-3">
  <div class="font-bold text-orange-700 dark:text-orange-300">범위 경계</div>
  <div class="text-sm mt-1">→ 라우터·Fallback</div>
  <div class="text-xs text-gray-500 mt-1">환불 Out → 사람에게 라우팅</div>
</div>

</v-clicks>

</div>

<v-click>

<div class="mt-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 text-sm text-center">
기획서에 "보안을 지킨다" → 기술 설계에 보안 컴포넌트가 없는 상황이 발생해선 안 된다
</div>

</v-click>

<!--
[스크립트]
기획서의 각 항목이 기술 설계의 어떤 요소로 변환되는지 표로 보겠습니다. 이 매핑이 1:1로 이루어져야 합니다.

목적 → 아키텍처 선택. "멀티스텝 자동화가 필요하다"는 목적이 "Agent 아키텍처를 선택한다"는 기술 결정으로 이어집니다.

입력 → API 인터페이스. "텍스트 최대 2000자"는 "토큰 제한 처리 로직"으로 변환됩니다.

출력 → Pydantic BaseModel. "JSON 형식 응답"은 BaseModel 스키마 정의로 구현됩니다.

제약조건 → Guardrail. "PII 금지"는 "PII 마스킹 전처리 레이어"가 됩니다.

성공 기준 → 테스트셋. "정확도 90%"는 "Golden Test Set 50건"으로 구체화됩니다.

[클릭] 가장 자주 발생하는 문제입니다. 기획서에 "보안을 지킨다"라고 써 있는데 기술 설계에 보안 컴포넌트가 하나도 없는 상황. 이런 불일치가 바로 기획서 품질 문제의 결과입니다.

전환: "매핑 과정에서 가장 자주 발생하는 문제를 실제 코드로 보겠습니다."
시간: 2분
-->

---
layout: two-cols-header
---

# PII 마스킹: 제약조건 → 코드 구현

::left::

**기획서 제약조건**

```
type: 보안
rule: 고객 PII를 LLM 프롬프트에
      포함하지 않는다
violation_impact: 개인정보보호법 위반
```

↓ 기술 설계

```
구현: PII 마스킹 전처리 레이어
```

::right::

<v-click>

```python {1-9|11-14}
class PIIMasker:
    PII_PATTERNS = {
        "phone": re.compile(
            r"01[016789]-?\d{3,4}-?\d{4}"
        ),
        "email": re.compile(
            r"[^@]+@[^@]+\.[^@]+"
        ),
    }

    def mask(self, text: str):
        for pii_type, pattern in self.PII_PATTERNS.items():
            text = pattern.sub(f"[{pii_type.upper()}_MASKED]", text)
        return text
```

</v-click>

<v-click>

```
입력: "전화번호는 010-1234-5678입니다"
출력: "전화번호는 [PHONE_MASKED]입니다"
```

</v-click>

<!--
[스크립트]
제약조건이 실제 코드로 어떻게 변환되는지 보겠습니다. 가장 중요한 예시인 PII 마스킹입니다.

왼쪽이 기획서의 제약조건입니다. "고객 PII를 LLM 프롬프트에 포함하지 않는다"라고 써 있습니다. 이게 기술 설계에서 "PII 마스킹 전처리 레이어"가 됩니다.

[클릭] 오른쪽이 실제 구현입니다. 정규식으로 전화번호와 이메일을 감지합니다. 감지되면 [PHONE_MASKED] 같은 플레이스홀더로 교체합니다. 이렇게 처리된 텍스트만 LLM에 전달됩니다.

[클릭] 결과를 보면, 실제 전화번호가 완전히 마스킹됩니다. LLM은 개인 정보를 볼 수 없습니다.

[DEMO] 이 코드를 실습 3에서 직접 작성하게 됩니다. 본인의 기획서 제약조건을 코드로 변환하는 실습입니다.

전환: "에스컬레이션 로직도 같은 방식으로 구현됩니다."
시간: 2분
-->

---

# Fallback 로직: 범위 경계 → 코드 구현

<div class="grid grid-cols-2 gap-6 mt-4 overflow-hidden">

<div>

**기획서 Out of Scope**
```
- 환불 처리
```
**기획서 제약조건**
```
confidence 0.7 미만 →
사람에게 에스컬레이션
```

</div>

<div>

<v-click>

```python {1-8|10-12}
class AgentOutput(BaseModel):
    category: str
    confidence: float = Field(
        ge=0.0, le=1.0
    )
    response_message: str

    def should_escalate(self) -> bool:
        return (
            self.confidence < 0.7
            or self.category == "환불"
        )
```

</v-click>

</div>

</div>

<v-click>

<div class="mt-3 bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-3 text-sm">
기획서 문장 하나가 코드 조건문 하나로 1:1 매핑된다
</div>

</v-click>

<!--
[스크립트]
범위 경계와 제약조건이 어떻게 코드가 되는지 또 다른 예시입니다.

기획서에 두 가지가 정의되어 있습니다. Out of Scope에 "환불 처리", 제약조건에 "confidence 0.7 미만이면 에스컬레이션"입니다.

[클릭] 이게 코드로 변환되면 AgentOutput 모델의 should_escalate 메서드가 됩니다. confidence가 0.7 미만이거나 카테고리가 "환불"이면 True를 반환합니다. 기획서 문장이 코드 조건문으로 그대로 옮겨졌습니다.

[클릭] 핵심 메시지입니다. 기획서 문장 하나가 코드 조건문 하나로 1:1 매핑됩니다. 기획서가 명확하면 코드 작성이 쉬워집니다. 기획서가 모호하면 개발자가 임의로 결정하게 됩니다.

[Q&A 대비]
Q: 기획서에서 기술 설계로 변환할 때 가장 자주 놓치는 것이 뭔가요?
A: 에러 시나리오와 Fallback 동작입니다. "에러 시 적절히 처리한다"라고만 써 있으면 개발자 A는 재시도, B는 기본값 반환, C는 에러 전파로 각자 다르게 구현합니다. 에러 시나리오와 Fallback을 기획서에 명시해야 합니다.

전환: "기술 설계 단계에서 양방향 추적성이 왜 중요한지 보겠습니다."
시간: 2분
-->

---

# 기획서 ↔ 기술 설계: 양방향 추적성

<div class="grid grid-cols-2 gap-6 mt-4 overflow-hidden">

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
<div class="font-bold mb-3">기획서 (SPEC ID 부여)</div>
<v-clicks>

- `SPEC-001`: FAQ 자동 답변
- `SPEC-002`: PII LLM 전송 금지
- `SPEC-003`: confidence 0.7 미만 에스컬레이션
- `SPEC-004`: 응답 시간 30초 이내

</v-clicks>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
<div class="font-bold mb-3">기술 설계 (SPEC 참조)</div>
<v-clicks>

- `PIIMasker` → `SPEC-002`
- `AgentOutput.should_escalate()` → `SPEC-003`
- `asyncio.wait_for(timeout=10)` → `SPEC-004`
- `GoldenTestSet(n=50)` → `SPEC-001`

</v-clicks>
</div>

</div>

<!--
[스크립트]
기획서와 기술 설계 사이에 양방향 추적성이 있어야 합니다. 어떻게 하면 될까요?

[클릭] 기획서의 각 항목에 SPEC ID를 부여합니다. SPEC-001은 FAQ 자동 답변, SPEC-002는 PII 금지, 이런 식입니다.

[클릭] 기술 설계의 각 컴포넌트가 어떤 SPEC를 구현하는지 매핑합니다. PIIMasker는 SPEC-002를 구현합니다. should_escalate()는 SPEC-003을 구현합니다.

이렇게 하면 두 가지 효과가 있습니다. 첫째, 기획서가 변경될 때 영향받는 코드를 즉시 찾을 수 있습니다. 둘째, 코드 리뷰 때 "이 코드가 왜 여기 있지?"라는 질문에 "SPEC-003 때문입니다"라고 답할 수 있습니다.

[Q&A 대비]
Q: SPEC ID 관리가 번거롭지 않나요?
A: 처음에는 그렇게 느껴질 수 있습니다. 하지만 프로젝트가 커질수록 이 추적성이 없으면 "이 코드 지워도 되나요?"라는 질문에 아무도 답을 못 하는 상황이 발생합니다. Git 커밋 메시지에 SPEC ID를 포함시키는 것도 좋은 방법입니다.

전환: "이제 전통 PRD와 Agent 기획서의 차이를 정리하고, 실습으로 넘어가겠습니다."
시간: 2분
-->

---
layout: two-cols-header
---

# 전통 PRD vs Agent 기획서

::left::

**전통 PRD**

<v-clicks>

- 결정론적 동작 명세
- "버튼 클릭 → 주문 생성"
- Fallback 불필요
- LLM 비용 고려 없음
- User Story 중심

</v-clicks>

::right::

**Agent 기획서**

<v-clicks>

- 확률적 동작 포함
- "confidence 0.7 미만 시 에스컬레이션"
- **Fallback 필수**
- **LLM 비용 제약 명시**
- User Story + Guardrail + Fallback

</v-clicks>

<!--
[스크립트]
전통 PRD와 Agent 기획서의 차이를 정리해보겠습니다.

[클릭] 전통 PRD는 결정론적입니다. "버튼을 클릭하면 주문이 생성된다"처럼 입력이 같으면 출력이 항상 같습니다.

[클릭] Agent 기획서는 확률적 동작을 다룹니다. LLM의 출력이 매번 다를 수 있기 때문입니다.

[클릭] 전통 PRD에는 Fallback이 불필요합니다. 결정론적이니까요.

[클릭] Agent에는 Fallback이 필수입니다. confidence가 낮거나 예상치 못한 입력이 들어올 때 어떻게 처리할지를 반드시 정의해야 합니다.

[클릭] 전통 PRD는 LLM 비용을 고려하지 않습니다.

[클릭] Agent 기획서는 API 호출 비용, 토큰 제한, 타임아웃을 제약조건에 명시합니다.

핵심 메시지: Agent 기획서는 전통 PRD를 대체하는 것이 아니라 보완합니다. User Story는 그대로 쓰고 Guardrail과 Fallback을 추가합니다.

전환: "자, 이제 배운 내용을 직접 적용해볼 시간입니다. 실습 1로 넘어가겠습니다."
시간: 2분
-->

---
layout: section
transition: fade
---

# 실습 시간
## I DO → WE DO → YOU DO

<!--
[스크립트]
개념 설명은 여기서 마무리하고 실습으로 넘어갑니다. 오늘 실습은 세 단계로 구성됩니다. 제가 먼저 보여드리고, 함께 해보고, 여러분이 직접 합니다.

전환: "실습 1, 기획서 직접 작성하기부터 시작합니다."
시간: 30초
-->

---

# 실습 1: Agent 기획서 작성

<div class="grid grid-cols-3 gap-4 mt-4 overflow-hidden">

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
<div class="font-bold text-blue-700 dark:text-blue-300 mb-2">I DO (5분)</div>
<div class="text-sm">강사가 "주간 보고서 자동화" Pain을 6가지 구성요소로 변환하는 과정 시연</div>
</div>

<div class="bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-4">
<div class="font-bold text-yellow-700 dark:text-yellow-300 mb-2">WE DO (10분)</div>
<div class="text-sm">"코드 리뷰 자동화 Agent" 시나리오를 함께 분석. 목적 → 입력 → 제약 순서로 진행</div>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
<div class="font-bold text-green-700 dark:text-green-300 mb-2">YOU DO (15분)</div>
<div class="text-sm">Session 1 Agent 후보 1개 선택 → 6가지 항목 모두 작성 → 등급 B 이상 목표</div>
</div>

</div>

<v-click>

<div class="mt-4 bg-gray-50 dark:bg-gray-800 rounded-lg p-3 text-sm">

**YOU DO 체크리스트:**
- `purpose`: "누구를 위해 + 무엇을 + 정량적 목표" 형식
- `constraints`: 보안 1개 + 비즈니스 1개 + 기술 1개 (최소 3개)
- `success_criteria`: 수치 + 측정 방법 (최소 2개)

</div>

</v-click>

<!--
[스크립트]
실습 1입니다. 30분 동안 진행합니다.

I DO 단계, 5분입니다. 제가 "주간 보고서 자동화" Pain을 받아서 6가지 구성요소로 변환하는 과정을 그대로 보여드립니다. 각 항목을 채우면서 왜 이렇게 써야 하는지 설명합니다.

WE DO 단계, 10분입니다. 이번에는 "코드 리뷰 자동화 Agent" 시나리오입니다. 목적 문장부터 함께 작성합니다. 매 단계마다 멈추고 질문을 받겠습니다.

[클릭] YOU DO 단계, 15분입니다. Session 1에서 도출한 Agent 후보 1개를 선택합니다. 세 가지가 핵심입니다. 목적은 "누구를 위해 + 무엇을 + 정량적 목표" 형식으로, 제약조건은 보안·비즈니스·기술 세 유형으로, 성공 기준은 수치와 측정 방법을 포함해서 작성합니다. validate_spec_quality()로 검증해서 B 이상이 목표입니다.

[Q] 이해관계자가 명확하지 않을 때 어떻게 하나요? 잠깐 이야기해볼게요.

전환: "I DO부터 시작하겠습니다."
시간: 1분
-->

---

# 실습 2: 나쁜 기획서 개선하기

<div class="mt-2 bg-red-50 dark:bg-red-900/20 rounded-lg p-4 text-sm mb-4">

```python
bad_spec_to_fix = {
    "purpose": "AI 챗봇을 만들어서 고객 서비스를 개선한다",
    "inputs": [{"name": "user_input"}],           # 타입? 제한? 예시?
    "outputs": [{"name": "answer"}],              # 형식? 필드?
    "constraints": [{"rule": "적절하게 동작해야 한다"}],  # 측정 불가
    "success_criteria": [{"metric": "성능이 좋아야 한다"}], # 주관적
    "in_scope": ["모든 고객 문의 처리"],             # 범위 무한
    "out_of_scope": [],                           # 비어있음!
}
```

</div>

<v-clicks>

- **WE DO**: 목적 + 입력 + 출력 3개 항목을 함께 개선 (8분)
- **YOU DO**: 제약조건 + 성공 기준 + 범위 스스로 개선 → 등급 A 목표 (12분)

</v-clicks>

<!--
[스크립트]
실습 2입니다. 25분 동안 진행합니다. 이번에는 처음부터 작성하는 것이 아니라 나쁜 기획서를 개선하는 연습입니다.

화면에 보이는 bad_spec_to_fix를 보겠습니다. 문제가 6개 항목 전부에 있습니다. purpose는 AI를 수단으로 쓰고 있고 정량적 목표가 없습니다. inputs는 타입도 제한도 없습니다. constraints는 "적절하게"라는 주관적 표현을 씁니다. out_of_scope는 아예 비어있습니다.

[클릭] WE DO에서는 앞 3개 항목을 함께 개선합니다. 제가 이끌고 여러분이 따라오는 방식입니다. 각 항목마다 "왜 이렇게 바꾸는가?"를 반드시 설명합니다.

[클릭] YOU DO에서는 나머지 3개를 스스로 개선합니다. validate_spec_quality()로 개선 전후를 비교해서 A 등급을 목표로 합니다.

전환: "자, 먼저 purpose부터 함께 개선해봅시다."
시간: 1분
-->

---

# 실습 3: 기획서 → 기술 설계 초안 도출

<div class="grid grid-cols-2 gap-4 mt-4 overflow-hidden">

<div>

**I DO (5분)**

강사가 CS Agent 기획서를 `spec_to_technical_design()` 함수로 변환

**WE DO (10분)**

Guardrail 도출 단계 함께 수행

제약조건 3개 → 각각 어떤 기술 컴포넌트로 변환되는지 토론

</div>

<div>

<v-click>

**YOU DO (15분)**

```python
design_supplement = {
    "아키텍처_선택_근거": {
        "선택": "Tool Use / RAG / Hybrid",
        "근거": ["이유 1", "이유 2"],
        "대안_배제_이유": "...",
    },
    "에러_시나리오": [
        {"시나리오": "LLM 타임아웃", "대응": "..."},
        {"시나리오": "입력 언어 미지원", "대응": "..."},
        {"시나리오": "외부 API 장애", "대응": "..."},
    ],
}
```

</v-click>

</div>

</div>

<!--
[스크립트]
실습 3이자 마지막 실습입니다. 30분 동안 진행합니다. 이번 실습의 목표는 작성한 기획서를 기술 설계로 변환하는 것입니다.

I DO에서는 제가 CS Agent 기획서를 spec_to_technical_design() 함수로 변환하는 과정을 보여드립니다. 목적에서 아키텍처를, 제약에서 Guardrail을, 성공 기준에서 테스트 계획을 어떻게 끌어내는지 보여주는 과정입니다.

WE DO에서는 Guardrail 도출을 함께 합니다. 제약조건 3개를 각각 어떤 기술 컴포넌트로 변환하는지 토론 방식으로 진행합니다.

[클릭] YOU DO에서는 두 가지를 보완합니다. 첫째, 아키텍처 선택의 근거를 문서화합니다. "왜 Agent를 선택했고 RAG는 왜 배제했는가?"를 설명할 수 있어야 합니다. 둘째, 에러 시나리오 3개 이상을 정의합니다. LLM 타임아웃, 언어 미지원, API 장애를 어떻게 처리할지를 기획서 제약조건과 연결해서 작성합니다.

[Q&A 대비]
Q: 아키텍처를 아직 정하기 어려운데 어떻게 하나요?
A: "현 시점에서 최선의 선택"을 문서화하면 됩니다. 나중에 프로토타입 결과에 따라 업데이트합니다. 중요한 것은 "왜 이 선택을 했는가"를 기록하는 것입니다.

전환: "실습을 마치고 세션 핵심 정리를 하겠습니다."
시간: 1분
-->

---

# Session 3 핵심 정리

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 mb-2">
<strong>Agent 기획서 = 기획자·개발자·이해관계자 간의 계약</strong><br>
어느 한 구성요소라도 누락되면 프로젝트 실패로 이어진다
</div>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3 mb-2">
<strong>기획서 없이 개발하면 4가지가 반드시 발생한다</strong><br>
범위 확장 · 성공 기준 부재 · 입출력 불일치 · 제약조건 누락
</div>

<div class="bg-yellow-50 dark:bg-yellow-900/30 rounded-lg p-3 mb-2">
<strong>6가지 핵심 구성요소</strong>: 목적 · 입력 · 출력 · 제약조건 · 성공 기준 · 범위 경계<br>
좋은 기획서의 핵심: <strong>구체성과 측정 가능성</strong>
</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 mb-2">
<strong>기획서 → 기술 설계는 1:1 매핑</strong><br>
목적→아키텍처 · 제약→Guardrail · 성공 기준→테스트
</div>

</v-clicks>

<!--
[스크립트]
Session 3의 핵심을 정리합니다.

[클릭] 첫 번째, Agent 기획서는 계약입니다. 기획자, 개발자, 이해관계자 세 그룹이 서명하는 계약서입니다. 하나라도 빠지면 계약이 불완전합니다.

[클릭] 두 번째, 기획서 없이 시작하면 4가지 문제가 반드시 발생합니다. 범위 확장, 성공 기준 부재, 입출력 불일치, 제약조건 누락입니다.

[클릭] 세 번째, 6가지 구성요소를 기억하세요. 목적·입력·출력·제약조건·성공 기준·범위 경계입니다. 좋은 기획서의 핵심은 구체성과 측정 가능성입니다. "잘 동작한다"가 아니라 "정확도 90% 이상, 주간 50건 샘플링"처럼요.

[클릭] 네 번째, 기획서에서 기술 설계로의 전환은 1:1 매핑입니다. 기획서 문장 하나가 코드 컴포넌트 하나로 변환됩니다. 이 매핑이 완전해야 구현이 흔들리지 않습니다.

[Q] 오늘 작성한 기획서를 어디에 저장하면 좋을까요? Notion, Confluence, GitHub 어디든 좋습니다. 중요한 건 팀이 공유하고 버전을 관리하는 것입니다.

전환: "다음 Session 4에서는 Tool Use, RAG, Hybrid 중 어떤 구조가 맞는지 판단하는 방법을 살펴봅니다."
시간: 3분
-->

---

# 다음 세션 예고: Session 4

<div class="grid grid-cols-2 gap-6 mt-8 overflow-hidden">

<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-5">
<div class="font-bold text-gray-500 mb-3">Session 3 (방금)</div>

- 비즈니스 문제 → 기획서 변환
- 6가지 구성요소 작성
- 기획서 품질 검증
- 기획서 → 기술 설계 매핑

</div>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-5">
<div class="font-bold text-blue-700 dark:text-blue-300 mb-3">Session 4 (다음)</div>

- Tool Use와 MCP의 관계 정리
- RAG가 필요한 조건 판단
- Hybrid 패턴 3가지 비교
- 의사결정 트리로 구조 선택

</div>

</div>

<div class="mt-6 text-center text-gray-400 text-sm">
오늘 정리한 요구사항은 Session 4 의사결정 실습에도 그대로 활용됩니다
</div>

<!--
[스크립트]
Session 3를 마무리합니다. 지금까지 비즈니스 문제를 기획서로 변환하고, 기획서를 기술 설계로 매핑하는 전체 흐름을 배웠습니다.

다음 Session 4에서는 오늘 정리한 문제와 요구사항을 바탕으로, Tool Use와 RAG와 Hybrid 중 어떤 구조가 맞는지 판단하는 방법을 다룹니다. 오늘 작성한 기획서가 의사결정의 입력값이 됩니다.

기획서를 잘 만들어두면 Session 4에서 구조 판단이 훨씬 명확해집니다. YOU DO 과제를 꼭 완성해주세요.

5분 휴식 후 Session 4 시작합니다.

[Q&A 대비]
Q: 기획서를 LLM으로 자동 생성하면 어떤가요?
A: LLM이 생성한 초안은 출발점으로만 사용합니다. LLM은 일반적인 구조는 잘 잡아주지만 도메인 특화 제약조건을 빠뜨립니다. LLM 초안 생성 → 도메인 전문가 검토 → 이해관계자 합의의 3단계가 필요합니다.

시간: 2분
-->

---
layout: section
transition: fade
---

# Session 4

## Tool Use · RAG · Hybrid 구조 판단

<!--
[스크립트]
여러분, 드디어 오늘 Day 1의 마지막 세션입니다. Session 1부터 3까지 AI Agent가 무엇인지, 어떻게 설계하는지를 배웠습니다. 이제 마지막 핵심 질문에 답할 차례입니다. "우리가 만들 Agent에는 어떤 구조가 맞는가?" 이 세션이 끝나면 여러분은 Tool Use, RAG, Hybrid 세 가지 접근의 차이를 이해하고, 실제 문제에 어떤 구조를 적용할지 스스로 판단할 수 있게 됩니다. 총 2시간 세션으로 강의와 실습을 함께 진행합니다.

[Q&A 대비]
Q: 오늘 배우는 내용이 실제 개발에서 얼마나 중요한가요?
A: 매우 중요합니다. 아키텍처 선택은 나중에 바꾸기 어렵고, 잘못된 선택은 개발 속도와 유지보수에 큰 영향을 미칩니다.

전환: 먼저 LLM의 근본적인 한계부터 짚어봅시다.
시간: 1분
-->

---
layout: default
transition: slide-left
---

# LLM의 근본적 한계

<div class="overflow-hidden">

<v-clicks>

- LLM은 본질적으로 **텍스트 입력 → 텍스트 출력** 모델이다
- 아무리 뛰어난 추론 능력도, LLM 단독으로는:
  - 현재 날씨를 확인할 수 없다
  - 데이터베이스에서 고객 정보를 조회할 수 없다
  - 외부 서비스에 요청을 보낼 수 없다

</v-clicks>

<v-click>

<div class="mt-8 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

**이 근본적 한계를 해결하기 위해 등장한 것이 Function Calling(Tool Use)이다**

</div>

</v-click>

</div>

<!--
[스크립트]
LLM은 텍스트를 받아서 텍스트를 반환합니다. 이게 전부입니다. 최신 GPT 계열이든, Claude 계열이든, Gemini 계열이든 마찬가지입니다.

[클릭] 이 말이 의미하는 바를 구체적으로 생각해봅시다. 아무리 뛰어난 LLM이라도 혼자서는...

[클릭] 현재 날씨를 확인할 수 없습니다. "서울 오늘 날씨"를 묻는다면, 학습 데이터에서 알고 있는 서울의 일반적인 날씨를 답하거나, 할루시네이션으로 지어낼 수 있습니다. 데이터베이스에서 고객 정보를 조회하는 것도, 외부 서비스에 주문을 보내는 것도 불가능합니다.

[클릭] 이 한계를 해결하기 위해 나온 것이 바로 Tool Use입니다. 벤더마다 Function Calling 같은 이름으로 구현되지만 핵심 아이디어는 같습니다. 오늘 첫 번째 주제로 이걸 배웁니다.

[Q&A 대비]
Q: LLM이 인터넷에 접속한다고 들었는데, 그건 어떻게 되는 건가요?
A: 검색 기능이 있는 LLM은 내부적으로 Tool Use(Function Calling)를 사용해서 검색 API를 호출하는 겁니다. LLM 자체가 인터넷을 직접 접속하는 건 아닙니다.

전환: 그럼 Function Calling이 어떻게 이 한계를 해결하는지, 역사부터 살펴봅시다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# Function Calling의 진화 과정

<div class="overflow-hidden">

<v-clicks>

| 연도 | 사건 | 의미 |
|------|------|------|
| 2023년 초 | OpenAI ChatGPT Plugins 출시 | LLM이 외부 세계와 상호작용 가능, 첫 실험 |
| 2023년 6월 | OpenAI GPT API Function Calling 도입 | Agent 아키텍처의 사실상 표준화 |
| 2024년 | Anthropic MCP 발표 | 벤더 중립적 표준 프로토콜 지향 |

</v-clicks>

<v-click>

<div class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4">

**Function Calling** = 각 벤더별 구현<br>
**MCP(Model Context Protocol)** = Tool + Resource + Prompt + Sampling 표준화

</div>

</v-click>

</div>

<!--
[스크립트]
Function Calling이 어떻게 등장했는지 역사를 빠르게 짚어봅시다.

[클릭] 2023년 초, OpenAI가 ChatGPT Plugins를 출시했습니다. LLM이 외부 서비스와 상호작용할 수 있다는 첫 번째 대규모 실험이었습니다. 반응은 뜨거웠지만, API 형태가 아니라 개발자가 쓰기엔 불편했습니다.

[클릭] 2023년 6월, GPT API에 Function Calling이 공식 도입되면서 상황이 바뀌었습니다. 개발자가 함수를 정의하면 LLM이 적절한 시점에 호출 요청을 반환하는 형태입니다. 이게 Agent 아키텍처의 사실상 표준이 됩니다.

[클릭] 2024년에 Anthropic이 MCP를 발표했습니다. MCP는 Function Calling을 포함하면서, 벤더 종속 없이 어떤 LLM에서도 동일하게 동작하는 표준 프로토콜을 지향합니다.

[클릭] 정리하면, Function Calling은 각 벤더별 구현 방식이고, MCP는 이를 표준화한 프로토콜입니다. 실무에서는 Function Calling과 Tool Use를 거의 같은 의미로 씁니다.

[Q&A 대비]
Q: MCP가 표준이 됐나요? 지금 써야 하나요?
A: 2026년 현재는 여러 도구 생태계가 MCP를 지원하는 흐름으로 가고 있습니다. 학습 목적으로는 Function Calling 같은 벤더별 Tool Use를 먼저 이해하고, MCP는 이를 표준화하려는 프로토콜로 이해하면 됩니다.

전환: 그럼 Function Calling이 실제로 어떻게 동작하는지 메커니즘을 봅시다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# Function Calling 핵심 메커니즘

<div class="grid grid-cols-[1fr_1fr] gap-6 overflow-hidden">

<div>

**LLM이 직접 수행하는 것**

<v-clicks>

- 사용자 메시지 분석 및 의도 파악
- 적합한 Tool 선택 및 파라미터 JSON 생성
- Tool 결과를 바탕으로 자연어 응답 생성

</v-clicks>

</div>

<div>

**개발자 코드가 수행하는 것**

<v-clicks>

- 외부 API 실제 호출 및 데이터 수신
- Tool 호출 결과의 유효성 검증

</v-clicks>

</div>

</div>

<v-click>

<div class="mt-6 bg-green-50 dark:bg-green-900/30 rounded-lg p-4">

**핵심**: LLM은 "무엇을 호출할지 결정"하고, 애플리케이션은 "실제로 호출하고 결과를 검증"한다

</div>

</v-click>

<!--
[스크립트]
Function Calling의 핵심을 명확히 짚어봅시다. 역할 분리입니다.

[클릭] LLM이 직접 수행하는 것은 세 가지입니다. 사용자의 메시지를 읽고 의도를 파악하는 것, 어떤 Tool을 어떤 파라미터로 호출할지 결정하여 JSON으로 출력하는 것, 그리고 Tool 결과를 받아 최종 자연어 응답을 생성하는 것입니다.

[클릭] 반면 개발자가 작성한 애플리케이션 코드가 수행하는 것은 두 가지입니다. LLM이 요청한 Tool을 실제로 실행하여 외부 API를 호출하는 것, 그리고 반환된 JSON의 유효성을 검증하는 것입니다.

[클릭] 이 분리가 핵심입니다. LLM은 판단하고, 코드는 실행합니다. LLM은 실제로 아무 API도 호출하지 않습니다. "이 파라미터로 이 함수를 호출하라"는 지시만 내릴 뿐입니다.

[Q&A 대비]
Q: LLM이 직접 API를 호출하면 안 되나요?
A: 보안상 절대 안 됩니다. LLM의 출력은 신뢰할 수 없는 외부 입력과 같습니다. 반드시 애플리케이션 코드가 검증 후 실행해야 합니다.

전환: 이 과정이 실제로 몇 단계로 진행되는지 구체적인 흐름을 봅시다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# Function Calling 5단계 흐름

<v-clicks>

<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-2 mb-1"><strong>①</strong> 사용자가 메시지를 보낸다</div>
<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-2 mb-1"><strong>②</strong> LLM이 분석하고 <code>tool_calls</code> 응답을 반환한다</div>
<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-2 mb-1"><strong>③</strong> 애플리케이션이 지정된 Tool을 실제로 실행한다</div>
<div class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-2 mb-1"><strong>④</strong> Tool 실행 결과를 대화 이력에 추가한다</div>
<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-2"><strong>⑤</strong> LLM이 Tool 결과를 참고하여 최종 응답을 생성한다</div>

</v-clicks>

<v-click>

<div class="mt-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 text-sm">

하나의 사용자 요청에 이 사이클이 <strong>여러 번 반복</strong>될 수 있다

</div>

</v-click>

<!--
[스크립트]
Function Calling의 전체 흐름을 5단계로 정리해봅시다.

[클릭] 1단계, 사용자가 메시지를 보냅니다. "CUST-123 고객의 최근 주문 상태를 알려줘" 같은 요청입니다.

[클릭] 2단계, LLM이 이 메시지를 분석합니다. "이 요청을 처리하려면 search_orders Tool을 customer_id='CUST-123' 파라미터로 호출해야겠다"고 판단하고, tool_calls JSON을 반환합니다. 텍스트 응답이 아닙니다.

[클릭] 3단계, 애플리케이션 코드가 JSON을 파싱하여 실제 DB나 API를 호출합니다. LLM이 실행하는 게 아니라 우리가 작성한 코드가 실행합니다.

[클릭] 4단계, Tool 실행 결과를 대화 이력에 추가합니다. 마치 "Tool이 이런 결과를 반환했어"라고 LLM에게 알려주는 겁니다.

[클릭] 5단계, LLM이 Tool 결과를 받아 최종 자연어 응답을 생성합니다. "CUST-123 고객님의 최근 주문은 ORD-789로, 노트북 1,500,000원이 배송 완료되었습니다."

[클릭] 그리고 이 사이클이 여러 번 반복될 수 있습니다. 복잡한 요청에서는 LLM이 여러 Tool을 순차적으로 호출하면서 해결합니다.

[Q&A 대비]
Q: 2단계에서 LLM이 Tool을 호출하지 않기로 판단할 수도 있나요?
A: 네, tool_choice를 "auto"로 설정하면 LLM이 스스로 판단합니다. Tool이 필요 없는 질문엔 직접 텍스트 응답을 반환합니다.

전환: 코드로 직접 확인해봅시다.
시간: 2분
-->

---
layout: two-cols-header
transition: slide-left
---

# Function Calling 코드: Tool 정의

::left::

```python {1-15|16-30|all}{maxHeight:'340px'}
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_orders",
            "description": (
                "고객 ID로 주문 이력을 조회합니다. "
                "최근 주문부터 반환합니다. "
                "환불/교환 처리 전 주문 상태 확인에 사용하세요."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "고객 고유 식별자",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "반환할 최대 주문 수",
                    },
                },
                "required": ["customer_id"],
            },
        },
    },
]
```

::right::

<v-clicks>

<div class="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-3 text-sm mt-2">

**description이 핵심**<br>
"언제 이 Tool을 사용해야 하는지"를 명확히 기술해야 LLM이 정확하게 선택한다

</div>

<div class="bg-red-50 dark:bg-red-900/30 rounded-lg p-3 text-sm mt-2">

**Tool 폭발 주의**<br>
Tool이 10개 이상이면 LLM의 선택 정확도가 급격히 떨어진다

</div>

</v-clicks>

<!--
[스크립트]
코드를 봅시다. Tool을 정의하는 부분입니다.

[클릭] Tool은 JSON Schema로 함수 시그니처를 기술합니다. name은 함수명, description은 언제 사용할지에 대한 설명, parameters는 파라미터 정의입니다.

[클릭] required 배열에 필수 파라미터를 명시합니다. customer_id는 필수이고 limit은 선택입니다.

[클릭] 여기서 가장 중요한 게 description입니다. LLM은 description을 읽고 이 Tool을 언제 사용할지 판단합니다. "주문 이력 조회"가 아니라 "환불/교환 처리 전 주문 상태 확인에 사용하세요"처럼 구체적인 사용 맥락을 써야 합니다.

[클릭] 그리고 Tool 수에 주의해야 합니다. Tool이 10개를 넘으면 LLM의 선택 정확도가 떨어질 수 있습니다. Tool 정의가 매 LLM 호출마다 프롬프트에 포함되어 토큰도 소비됩니다.

[Q&A 대비]
Q: Tool description을 한국어로 써도 되나요?
A: 됩니다. 단, 영어 description이 일반적으로 더 정확도가 높다는 실험 결과가 있습니다. 중요한 Tool은 영어로 작성하는 것을 권장합니다.

전환: Tool 정의가 끝났으면, 이제 Agent 루프를 어떻게 구현하는지 봅시다.
시간: 2분
-->

---
layout: two-cols-header
transition: slide-left
---

# Function Calling 코드: Agent 루프

::left::

```python {1-10|11-18|19-28}{maxHeight:'340px'}
def run_agent(user_message: str):
    messages = [
        {"role": "system",
         "content": "당신은 고객 지원 Agent입니다."},
        {"role": "user",
         "content": user_message},
    ]
    # 1차 호출: Tool 호출 여부 판단
    response = client.chat.completions.create(
        model=MODEL, messages=messages,
        tools=tools, tool_choice="auto",
    )
    assistant_msg = response.choices[0].message

    if assistant_msg.tool_calls:
        messages.append(assistant_msg)
        for tc in assistant_msg.tool_calls:
            fn_args = json.loads(tc.function.arguments)
            result = execute_tool(tc.function.name, fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result),
            })
        # 2차 호출: Tool 결과 기반 최종 응답
        final = client.chat.completions.create(
            model=MODEL, messages=messages)
        return final.choices[0].message.content
    return assistant_msg.content
```

::right::

<div class="text-sm mt-2">

<v-click>

**실행 결과**

```
CUST-123 고객님의 최근 주문을 확인했습니다.
- 주문번호: ORD-789
- 상태: 배송 완료
- 상품: 노트북
- 금액: 1,500,000원
```

</v-click>

<v-click>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 mt-4">

Tool이 필요 없는 질문은<br>1차 호출에서 직접 반환

</div>

</v-click>

</div>

<!--
[스크립트]
Agent 루프 코드입니다.

[클릭] 먼저 시스템 프롬프트와 사용자 메시지를 담은 messages 배열을 만듭니다. 그리고 LLM에게 1차 호출을 합니다. tool_choice="auto"로 설정하면 LLM이 스스로 Tool 사용 여부를 판단합니다.

[클릭] LLM이 Tool 호출을 결정하면 tool_calls가 반환됩니다. 각 tool_call을 순회하며 execute_tool을 호출합니다. 결과를 role: "tool"로 messages에 추가합니다.

[클릭] Tool 결과가 모두 추가되면 2차 LLM 호출을 합니다. LLM이 Tool 결과를 보고 최종 자연어 응답을 생성합니다. Tool이 필요 없는 질문이라면 1차 호출에서 바로 content를 반환합니다.

[클릭] 실행 결과입니다. LLM이 search_orders Tool을 호출하여 DB에서 정보를 가져오고, 그 정보를 자연어로 요약해서 반환합니다.

[Q&A 대비]
Q: Tool 결과의 role이 왜 "tool"인가요? "assistant"나 "user"가 아니라?
A: OpenAI API 스펙입니다. LLM이 Tool을 호출했고, Tool이 응답했다는 것을 명확히 구분하기 위해 별도의 role을 사용합니다.

전환: Tool Use의 핵심을 이해했습니다. 이제 두 번째 아키텍처, RAG로 넘어갑시다.
시간: 2분
-->

---
layout: section
transition: fade
---

# 2.

## RAG 아키텍처

<!--
[스크립트]
Tool Use의 핵심과 MCP의 방향성을 이해했습니다. 이제 두 번째 중요한 아키텍처, RAG로 넘어갑니다. RAG는 Retrieval-Augmented Generation의 줄임말로, LLM에게 지식을 주입하는 방법입니다.

전환: 왜 RAG가 필요한지부터 봅시다.
시간: 30초
-->

---
layout: default
transition: slide-left
---

# RAG가 필요한 이유

<div class="overflow-hidden">

<v-clicks>

- LLM은 학습 데이터에 포함된 정보만 "알고 있다"
- 학습 데이터에는 <strong>시간적 한계(cutoff date)</strong>가 있다
- 기업 내부 문서, 비공개 데이터, 최신 정보는 포함되지 않는다

</v-clicks>

<v-click>

<div class="mt-6 bg-orange-50 dark:bg-orange-900/30 rounded-lg p-4">

"우리 회사의 2026년 1분기 환불 정책이 뭐야?"라고 물으면<br>
LLM이 할 수 있는 것은 두 가지뿐이다:<br>
<strong>"모르겠습니다"</strong> 또는 <strong>그럴듯하게 지어내는 것(할루시네이션)</strong>

</div>

</v-click>

<v-click>

<div class="mt-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

**RAG**: LLM에게 질문을 보내기 전에, 먼저 관련된 문서를 찾아서 함께 전달하자

</div>

</v-click>

</div>

<!--
[스크립트]
LLM은 학습 데이터 안에 있는 것만 알 수 있습니다.

[클릭] 학습 데이터에 포함된 정보만 압니다. ChatGPT는 인터넷의 공개 데이터로 학습했습니다.

[클릭] 그런데 학습에는 cutoff date가 있습니다. 모델마다 시점이 다르고, 검색 없이 최신 정보는 보장되지 않습니다.

[클릭] 가장 큰 문제는 기업 내부 데이터입니다. 우리 회사의 환불 정책, 사내 위키, 고객 데이터는 공개된 적이 없으니 LLM이 알 수 없습니다.

[클릭] 그래서 "우리 회사 환불 정책이 뭐야?"라고 물으면 LLM은 두 가지 중 하나를 합니다. 솔직하게 "모르겠습니다"라고 하거나, 일반적인 환불 정책처럼 들리는 내용을 지어냅니다. 후자가 할루시네이션입니다.

[클릭] RAG는 이 문제를 해결하는 아이디어입니다. LLM에게 질문만 보내지 말고, 먼저 관련 문서를 찾아서 함께 보내자는 겁니다. "이 문서를 참고해서 답변해줘."

[Q&A 대비]
Q: Fine-tuning으로 해결할 수 없나요?
A: Fine-tuning은 LLM의 "스타일"과 "기술"을 바꾸는 데 적합합니다. 특정 지식을 주입하려면 데이터가 자주 바뀔수록 RAG가 훨씬 효율적입니다. 환불 정책이 바뀔 때마다 Fine-tuning할 수는 없습니다.

전환: RAG는 세 단계 파이프라인으로 동작합니다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# RAG 파이프라인 3단계

<div class="overflow-hidden">

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 mb-3">

<strong>① Retrieval (검색)</strong><br>
사용자의 질문과 관련성이 높은 문서 조각(chunk)을 검색<br>
<span class="text-sm">사전 준비: 문서 분할(chunking) → 벡터화(embedding) → Vector DB 저장</span>

</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 mb-3">

<strong>② Augmentation (증강)</strong><br>
검색된 문서 조각을 사용자의 질문과 함께 LLM 프롬프트로 구성<br>
<span class="text-sm">top_k 권장값: 3~5 (너무 작으면 정보 누락, 너무 크면 노이즈)</span>

</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3">

<strong>③ Generation (생성)</strong><br>
LLM이 증강된 프롬프트를 입력받아 최종 답변을 생성<br>
<span class="text-sm">제공된 문서를 주요 근거로 사용, temperature 0에 가깝게 설정</span>

</div>

</v-clicks>

<v-click>

<div class="mt-4 text-xl text-center font-bold text-red-600">

"검색이 잘못되면 아무리 뛰어난 LLM도 정확한 답변을 생성할 수 없다"

</div>

</v-click>

</div>

<!--
[스크립트]
RAG는 세 단계 파이프라인으로 동작합니다.

[클릭] 첫 번째 단계, Retrieval입니다. 사용자가 질문을 하면, 먼저 관련 문서를 찾습니다. 이를 위해 사전 준비가 필요합니다. 문서를 적절한 크기로 쪼개고(chunking), 각 chunk를 숫자 벡터로 변환(embedding)하여, Vector DB에 저장해 둡니다. 질문도 벡터로 변환하여 가장 유사한 chunk를 찾습니다.

[클릭] 두 번째 단계, Augmentation입니다. 검색된 문서 조각들을 사용자 질문과 함께 하나의 프롬프트로 만듭니다. "다음 문서를 참고하여 답변하세요. 문서에 없는 내용은 답변하지 마세요." 몇 개의 chunk를 포함할지가 top_k입니다. 3~5개가 적당합니다.

[클릭] 세 번째 단계, Generation입니다. LLM이 이 증강된 프롬프트를 받아 답변을 생성합니다. 이때 LLM은 자신의 내재 지식이 아닌, 우리가 제공한 문서를 근거로 답합니다. 사실 기반 답변을 위해 temperature를 0에 가깝게 설정하는 것이 좋습니다.

[클릭] 가장 중요한 인사이트입니다. RAG의 품질은 검색 단계가 좌우합니다. 아무리 좋은 LLM도 관련 없는 문서를 받으면 잘못된 답변을 생성합니다.

[Q&A 대비]
Q: Vector DB는 무엇을 써야 하나요?
A: 프로토타입에는 FAISS나 ChromaDB가 적합합니다. 프로덕션에는 Pinecone, Weaviate, Qdrant 등을 사용합니다.

전환: 코드로 확인해봅시다.
시간: 3분
-->

---
layout: two-cols-header
transition: slide-left
---

# RAG 코드 구현

::left::

```python {1-12|13-22|23-35}{maxHeight:'340px'}
import numpy as np
from openai import OpenAI

client = OpenAI(api_key="...")

# 문서 준비
documents = [
    "환불 정책: 상품 수령 후 7일 이내 환불 가능.",
    "배송 안내: 일반 배송 2-3 영업일.",
    "포인트: 구매 금액 1% 적립.",
]

# Embedding 함수
def embed(texts):
    r = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [i.embedding for i in r.data]

doc_vecs = embed(documents)

# Retrieval: 코사인 유사도 검색
def retrieve(query: str, top_k: int = 2):
    qv = embed([query])[0]
    scored = []
    for doc, vec in zip(documents, doc_vecs):
        sim = np.dot(qv, vec) / (
            np.linalg.norm(qv) * np.linalg.norm(vec))
        scored.append((doc, float(sim)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:top_k]]
```

::right::

```python
# Augmentation + Generation
def rag_answer(query: str) -> str:
    docs = retrieve(query)
    context = "\n".join(
        f"[문서{i+1}] {d}"
        for i, d in enumerate(docs)
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": (
            f"참고 문서:\n{context}\n\n"
            f"위 문서만 참고하여 답변하고,\n"
            f"문서에 없는 내용은 '확인 불가'라고 답변하세요.\n\n"
            f"질문: {query}"
        )}],
    )
    return resp.choices[0].message.content

# 실행 결과
# rag_answer("전자제품 환불 기한이 어떻게 되나요?")
# → "상품 수령 후 7일 이내 환불 가능합니다."
```

<!--
[스크립트]
RAG 코드를 봅시다.

[클릭] 문서를 준비합니다. 실제 프로덕션에서는 PDF나 위키를 파싱하겠지만, 예제에서는 3개의 문자열로 단순화했습니다.

[클릭] embed 함수로 문서들을 벡터로 변환합니다. OpenAI의 text-embedding-3-small 모델을 사용합니다. doc_vecs에 저장해둡니다. 실제로는 이 단계가 사전 준비 단계이고, Vector DB에 저장합니다.

[클릭] retrieve 함수가 핵심입니다. 질문을 벡터로 변환하고, 문서 벡터들과 코사인 유사도를 계산합니다. 유사도가 높은 순으로 정렬하여 top_k개를 반환합니다.

rag_answer 함수에서 검색 결과를 컨텍스트로 만들어 LLM에 전달합니다. "위 문서만 참고"하고 "문서에 없는 내용은 확인 불가"라고 답하게 하는 것이 핵심 지시문입니다. "전자제품 환불 기한" 질문에 "7일 이내"라고 정확히 답합니다.

[Q&A 대비]
Q: RAG를 사용하면 할루시네이션이 완전히 사라지나요?
A: 줄어들지만 사라지지는 않습니다. 검색된 문서에 답이 없을 때 LLM이 자체 지식으로 채울 수 있습니다. 그래서 프롬프트에 "문서에 없는 내용은 '확인 불가'로 표시하세요" 같은 안전 지시문을 함께 넣는 것이 좋습니다.

전환: RAG는 읽기 전용입니다. 그럼 쓰기가 필요하면 어떻게 할까요? Hybrid로 갑시다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# RAG vs 키워드 검색

<div class="overflow-hidden">

| 구분 | 키워드 검색 (BM25) | 벡터 검색 (RAG) |
|------|------|------|
| 매칭 방식 | 정확히 같은 단어 | 의미적 유사성 |
| "환불 기한" 검색 시 | "환불 기한" 포함 문서만 | "7일 이내 환불 가능" 문서도 매칭 |
| 오타/동의어 | 약함 | 강함 |
| 속도 | 빠름 | 상대적으로 느림 |

<v-click>

<div class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4">

<strong>RAG의 본질적 한계</strong>

- "환불 정책이 뭐야?" → 답할 수 있다
- "환불 처리해줘" → <strong>수행할 수 없다</strong> (읽기 전용)
- 인덱싱 이후 변경된 정보는 반영되지 않는다

</div>

</v-click>

</div>

<!--
[스크립트]
RAG가 기존 키워드 검색과 어떻게 다른지 비교해봅시다.

키워드 검색인 BM25는 정확히 같은 단어가 있어야 매칭됩니다. "환불 기한"을 검색하면 이 두 단어가 모두 있는 문서만 찾습니다. 반면 벡터 검색은 의미적 유사성을 봅니다. "7일 이내 환불 가능"이라는 문서도 찾아낼 수 있습니다. 오타나 동의어에도 강합니다.

속도는 키워드가 빠릅니다. 그래서 실무에서는 두 방식을 결합하는 하이브리드 검색(BM25 + 벡터)을 쓰기도 합니다.

[클릭] 그런데 RAG에는 본질적인 한계가 있습니다. 읽기 전용이라는 겁니다. RAG는 문서를 검색해서 답변을 생성하지만, 실제로 어떤 행동도 수행할 수 없습니다. "환불 처리해줘"는 RAG로 처리할 수 없습니다. 그리고 인덱싱 이후 바뀐 정보는 자동으로 반영되지 않아서 주기적인 재인덱싱이 필요합니다.

[Q&A 대비]
Q: 문서가 자주 바뀌면 RAG를 매번 재구축해야 하나요?
A: 네, 인덱스를 업데이트해야 합니다. 문서 추가/수정이 잦으면 실시간 인덱싱을 지원하는 Vector DB를 선택하거나, 변경 빈도가 높은 데이터는 Tool(실시간 API)로 처리하는 것이 좋습니다.

전환: Tool Use는 행동, RAG는 지식입니다. 실무에서는 둘 다 필요한 경우가 많습니다. Hybrid 아키텍처로 갑시다.
시간: 2분
-->

---
layout: section
transition: fade
---

# 3.

## Hybrid 아키텍처

<!--
[스크립트]
이제 세 번째 주제입니다. Tool Use는 행동 능력, RAG는 지식 주입이었습니다. 실무에서 가치 있는 Agent의 대부분은 행동과 지식을 동시에 필요로 합니다. 이걸 결합한 것이 Hybrid 아키텍처입니다.

전환: 왜 Tool Use만, RAG만으로는 부족한지부터 봅시다.
시간: 30초
-->

---
layout: two-cols-header
transition: slide-left
---

# Tool Use만, RAG만으로 부족한 경우

::left::

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">

**Tool Use만으로 부족한 경우**

<v-clicks>

- 고객 "환불 가능한가요?"
- 주문 상태 조회(Tool): 가능
- 그런데 "환불이 가능한지" 판단하려면 **회사 환불 정책**을 알아야 한다
- 수십 페이지 정책을 Tool 코드에 하드코딩?

</v-clicks>

<v-click>

**→ RAG가 필요하다**

</v-click>

</div>

::right::

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">

**RAG만으로 부족한 경우**

<v-clicks>

- 트러블슈팅 문서에서 "서비스를 재시작하면 해결됩니다" 검색 완료
- 그런데 현재 서버 메모리 사용량은 RAG가 알 수 없다
- "재시작한다"는 행동은 RAG가 수행할 수 없다

</v-clicks>

<v-click>

**→ Tool이 필요하다**

</v-click>

</div>

<!--
[스크립트]
두 아키텍처가 각각 부족한 상황을 봅시다.

[클릭] Tool Use만으로 부족한 경우입니다. 고객이 "환불 가능한가요?"라고 묻습니다. Tool로 주문 상태를 조회합니다. "배송 완료, 3일 전 수령"이라는 결과를 얻었습니다.

[클릭] 그런데 "환불이 가능한지" 판단하려면 회사의 환불 정책을 알아야 합니다. "수령 후 7일 이내 환불 가능"이라는 규정이 있어야 3일 전 수령이 환불 가능하다고 판단할 수 있습니다.

[클릭] 이 정책을 Tool 코드에 하드코딩할 수는 없습니다. 정책은 자주 바뀌고, 수십 페이지 분량일 수 있습니다.

[클릭] RAG가 필요합니다. 정책 문서를 검색해서 판단 근거를 가져와야 합니다.

[클릭] 반대 경우도 봅시다. RAG만으로 부족한 경우입니다. 트러블슈팅 문서에서 해결책을 찾았습니다.

[클릭] 그런데 현재 서버 메모리 상황을 RAG는 알 수 없습니다.

[클릭] "재시작"이라는 행동도 RAG는 수행할 수 없습니다. RAG는 읽기 전용이기 때문입니다.

[클릭] Tool이 필요합니다. 실시간 메트릭 조회와 재시작 명령을 Tool로 구현해야 합니다.

전환: 그럼 Hybrid에는 어떤 패턴이 있을까요?
시간: 2분
-->

---
layout: default
transition: slide-left
---

# Hybrid 아키텍처 3가지 패턴

<div class="overflow-hidden">

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 mb-3">

<strong>패턴 ① RAG as Tool</strong><br>
RAG 검색 기능을 하나의 Tool로 래핑 → Agent Tool 목록에 등록<br>
<span class="text-sm">적합: 요청 유형이 다양하고 예측하기 어려운 범용 Agent</span>

</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 mb-3">

<strong>패턴 ② RAG-then-Act</strong><br>
모든 요청에 RAG로 지식 수집 먼저 → 그 지식을 바탕으로 Tool 호출 판단<br>
<span class="text-sm">적합: 지식 확인이 항상 선행되어야 하는 규정/정책 기반 업무</span>

</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3">

<strong>패턴 ③ Router 기반</strong><br>
경량 모델이 먼저 요청 분류 → RAG / Tool / 둘 다로 라우팅<br>
<span class="text-sm">적합: 요청 유형이 명확히 구분되고 비용 최적화가 중요한 대규모 서비스</span>

</div>

</v-clicks>

</div>

<!--
[스크립트]
Hybrid 아키텍처에는 세 가지 대표 패턴이 있습니다.

[클릭] 첫 번째는 RAG as Tool입니다. RAG 검색 기능을 search_policy()라는 Tool로 래핑합니다. Agent의 Tool 목록에 이 함수를 추가하면, LLM이 스스로 판단해서 필요할 때만 호출합니다. 범용 Agent에 적합합니다.

[클릭] 두 번째는 RAG-then-Act입니다. 모든 요청에 대해 먼저 RAG로 지식을 수집하고, 그 지식을 바탕으로 Tool 호출 여부를 판단합니다. 보험 상담처럼 "약관 확인 → 고객 정보 조회 → 보장 내용 안내"처럼 순서가 정해진 업무에 적합합니다.

[클릭] 세 번째는 Router 기반입니다. 경량 모델이 요청을 먼저 분류합니다. "이건 RAG로 충분해", "이건 Tool이 필요해", "이건 둘 다 필요해"로 분류한 후 해당 경로로 라우팅합니다. 대규모 서비스에서 비용 최적화에 효과적입니다.

[Q&A 대비]
Q: 어느 패턴부터 시작하는 게 좋나요?
A: RAG as Tool이 가장 자연스러운 Hybrid 진입점입니다. 이미 RAG가 있다면 search_policy() 함수로 래핑만 하면 됩니다.

전환: 패턴 선택 기준을 정리해봅시다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# Hybrid 패턴 선택 기준

<div class="overflow-hidden">

| 패턴 | 적합 상황 | 단점 |
|------|---------|------|
| RAG as Tool | 범용 Agent, 유연한 조합 | LLM이 Tool 선택을 놓칠 수 있음 |
| RAG-then-Act | 규정 기반 업무, 순차 흐름 | 단순 질문에서도 RAG 비용 발생 |
| Router | 대규모 서비스, 비용 최적화 | Router 분류 오류 시 정보 누락 |

<v-click>

<div class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4">

<strong>디버깅 용이성도 고려하라</strong>

- <strong>RAG-then-Act</strong>: 항상 같은 순서로 실행 → 로그 추적 쉬움
- <strong>RAG as Tool</strong>: LLM의 자율적 판단에 의존 → 왜 이 Tool을 선택했는지 추적 어려움

<strong>초기에는 디버깅이 쉬운 패턴으로 시작하고, 안정화 후 전환한다</strong>

</div>

</v-click>

</div>

<!--
[스크립트]
각 패턴의 적합 상황과 단점을 비교해봅시다.

RAG as Tool은 유연합니다. LLM이 필요할 때만 RAG를 호출합니다. 하지만 LLM이 RAG 호출을 놓칠 수 있습니다. 정말 필요한 순간에 search_policy()를 호출하지 않는 경우가 발생할 수 있습니다.

RAG-then-Act는 안정적입니다. 항상 같은 순서로 실행되므로 결과가 예측 가능합니다. 하지만 "배송 현황 알려줘"같은 단순 질문에도 RAG가 실행되어 비용이 발생합니다.

Router는 비용 효율적입니다. 하지만 Router가 잘못 분류하면 필요한 정보를 얻지 못할 수 있습니다.

[클릭] 중요한 포인트가 있습니다. 디버깅 용이성입니다. 초기에는 RAG-then-Act처럼 순서가 고정된 패턴으로 시작하세요. 로그 추적이 쉽고 버그를 빠르게 찾을 수 있습니다. 시스템이 안정화된 후에 RAG as Tool이나 Router로 전환하면 됩니다.

[Q&A 대비]
Q: 처음부터 Hybrid를 구축해야 하나요?
A: 절대 아닙니다. MVP는 단일 아키텍처로 시작하세요. RAG를 먼저 구축했다면 "직접 처리해줬으면"이라는 사용자 피드백이 나올 때 Tool을 추가합니다.

전환: 이제 핵심 질문입니다. 어떤 상황에서 어떤 아키텍처를 선택할까요?
시간: 2분
-->

---
layout: section
transition: fade
---

# 4.

## 아키텍처 선택 의사결정 트리

<!--
[스크립트]
세 가지 아키텍처를 모두 배웠습니다. 마지막 개념은 실무에서 가장 어려운 질문, "우리 문제에는 어떤 아키텍처가 맞는가?"에 답하는 의사결정 트리입니다.

전환: 의사결정을 위한 세 가지 축부터 봅시다.
시간: 30초
-->

---
layout: default
transition: slide-left
---

# 의사결정의 3축

<div class="overflow-hidden">

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 mb-3">

<strong>① 데이터 소스</strong><br>
정적 문서(매뉴얼, 정책, FAQ) → <strong>RAG 적합</strong><br>
실시간 API(DB, SaaS API, 모니터링) → <strong>Tool Use 적합</strong><br>
양쪽 모두 → <strong>Hybrid 검토</strong>

</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 mb-3">

<strong>② 상호작용 패턴 (읽기 vs 쓰기)</strong><br>
핵심 구분: 외부 시스템에 변경(side effect)을 가해야 하는가?<br>
읽기만 필요 → RAG 또는 Tool<br>
<strong>쓰기가 하나라도 있으면 Tool은 필수다</strong> (RAG는 읽기 전용)

</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3">

<strong>③ 실시간성</strong><br>
분 단위로 변하는 데이터(재고, 주문 상태) → <strong>Tool 필수</strong><br>
변경 빈도 낮은 데이터(정책, 매뉴얼, 주 1회) → <strong>RAG로 충분</strong>

</div>

</v-clicks>

</div>

<!--
[스크립트]
아키텍처를 선택할 때 세 가지 축으로 질문해봅니다.

[클릭] 첫 번째 축, 데이터 소스입니다. 우리 Agent가 참고하는 데이터가 어디서 오는가? 매뉴얼, 정책, FAQ 같은 정적 문서라면 RAG입니다. 재고 DB, 주문 API 같은 실시간 데이터라면 Tool입니다. 둘 다라면 Hybrid를 검토합니다.

[클릭] 두 번째 축, 읽기냐 쓰기냐입니다. 이게 가장 명확한 기준입니다. Agent가 외부 시스템에 변경을 가해야 하는가? 주문 취소, 이메일 발송, DB에 데이터 저장 같은 쓰기 작업이 하나라도 있으면 Tool은 필수입니다. RAG는 절대로 쓰기를 수행할 수 없습니다.

[클릭] 세 번째 축, 실시간성입니다. 재고가 방금 변했을 수도 있습니다. 서버 메트릭은 매 초 바뀝니다. 이런 분 단위로 변하는 데이터는 Tool로 실시간 조회해야 합니다. 반면 환불 정책이 매분 바뀌지는 않습니다. 주 1회 변경이라면 RAG로 충분합니다.

[Q&A 대비]
Q: 세 가지 축을 다 따져야 하나요? 간단하게 결정할 수 없나요?
A: 빠른 결정을 위한 핵심 질문 하나: "쓰기 작업이 필요한가?" YES면 Tool 필수. NO면 문서량과 데이터 변경 빈도를 봐서 RAG 또는 Simple LLM을 선택합니다.

전환: 세 축을 체계적으로 정리한 의사결정 플로우차트를 봅시다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# 의사결정 플로우차트

<div class="overflow-hidden font-mono text-sm bg-gray-50 dark:bg-gray-900 rounded-lg p-4">

<v-clicks>

```
시작: Agent가 해결하는 문제는 무엇인가?
```

```
Q1: 외부 시스템에 쓰기(생성/수정/삭제) 작업이 필요한가?
├─ YES → Q2: 대량 문서에서 지식 검색도 필요한가?
│         ├─ YES → 🔵 Hybrid (Tool Use + RAG)
│         └─ NO  → 🟢 Tool Use 단독
└─ NO  → Q3: 실시간 데이터 조회가 필요한가?
           ├─ YES → Q4: 정적 문서 검색도 필요한가?
           │         ├─ YES → 🔵 Hybrid (Tool Use + RAG)
           │         └─ NO  → 🟢 Tool Use 단독
           └─ NO  → Q5: 대량 문서 기반 Q&A인가?
                      ├─ YES → 🟡 RAG 단독
                      └─ NO  → ⚪ Simple LLM Call
```

</v-clicks>

</div>

<!--
[스크립트]
세 축을 기반으로 한 의사결정 플로우차트입니다.

[클릭] 시작 질문입니다. Agent가 해결하는 문제가 무엇인가?

[클릭] Q1부터 시작합니다. 외부 시스템에 쓰기 작업이 필요한가? YES라면 바로 Tool이 필요합니다. 그다음 대량 문서 검색도 필요한지를 봅니다. 필요하면 Hybrid, 아니면 Tool Use 단독입니다.

NO라면 Q3으로 갑니다. 실시간 데이터 조회가 필요한가? 주문 상태, 서버 메트릭처럼 실시간이 필요하면 Q4로 갑니다. 정적 문서도 함께 필요하면 Hybrid, 아니면 Tool Use 단독입니다.

실시간도 필요 없다면 Q5. 대량 문서 기반 Q&A인가? 수백 페이지 매뉴얼 검색이 필요하면 RAG 단독, 그것도 아니라면 Simple LLM Call로 충분합니다.

[Q&A 대비]
Q: "대량 문서"의 기준이 뭔가요?
A: 경험적으로 A4 10페이지 이하면 시스템 프롬프트에 직접 포함하는 게 더 간단하고 정확합니다. 10페이지를 초과하면 RAG 도입을 고려합니다.

전환: 실제 사례에 적용해봅시다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# 실제 사례 적용

<div class="overflow-hidden">

| 사례 | 쓰기? | 실시간? | 문서? | 결론 |
|------|-----|------|------|------|
| 사내 HR 규정 Q&A | No | No | Yes (수백 페이지) | **RAG 단독** |
| 고객 주문 환불 처리 | Yes | Yes | Yes (환불 정책) | **Hybrid** |
| 서버 모니터링/자동복구 | Yes | Yes | No | **Tool Use 단독** |
| 마케팅 카피 생성 | No | No | No | **Simple LLM** |

<v-click>

<div class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4">

<strong>경계 사례 처리</strong>: 문서량이 A4 3~4장 이하라면<br>
RAG를 구축하는 것보다 <strong>시스템 프롬프트에 직접 포함</strong>하는 것이 더 간단하고 정확하다

</div>

</v-click>

</div>

<!--
[스크립트]
실제 사례에 의사결정 트리를 적용해봅시다.

사내 HR 규정 Q&A입니다. 쓰기가 필요 없고, 실시간 데이터도 필요 없습니다. 수백 페이지 규정집이 있습니다. Q5에서 RAG 단독이 선택됩니다.

고객 주문 환불 처리입니다. 환불 실행이라는 쓰기 작업이 있습니다. 실시간 주문 상태 조회가 필요합니다. 환불 정책 문서도 필요합니다. Hybrid입니다.

서버 모니터링/자동복구입니다. 재시작이라는 쓰기 작업이 있습니다. 실시간 메트릭이 필요합니다. 정적 문서는 필요 없습니다. Tool Use 단독입니다.

마케팅 카피 생성입니다. 외부 시스템에 쓰지 않습니다. 실시간 데이터도 필요 없습니다. 대량 문서도 없습니다. LLM의 창의성을 활용하면 충분합니다. Simple LLM Call입니다.

[클릭] 경계 사례 하나. 문서가 3~4장 이하라면 RAG를 구축할 필요가 없습니다. 시스템 프롬프트에 직접 넣는 게 더 빠르고, 오히려 정확도가 높은 경우가 많습니다. RAG는 오버엔지니어링이 될 수 있습니다.

[Q&A 대비]
Q: 의사결정을 잘못해서 나중에 아키텍처를 바꿔야 한다면?
A: 초기 설계에서 인터페이스 분리를 해두면 전환 비용이 최소화됩니다. get_refund_policy() 함수를 추상화해두면 내부 구현을 RAG에서 Tool로 바꿔도 Agent 로직은 수정할 필요가 없습니다.

전환: 아키텍처별 비용과 성능 프로파일도 알아두면 좋습니다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# 아키텍처별 비용-성능 프로파일

<div class="overflow-hidden">

| 아키텍처 | LLM 호출 | 지연 | 비용 | 정확도 |
|---------|---------|------|------|--------|
| Simple LLM | 1.0회 | 1.5초 | 1.0x | 60~75% |
| RAG 단독 | 1.5회 | 2.5초 | 1.8x | 75~85% |
| Tool Use 단독 | 2.5회 | 4.0초 | 3.0x | 70~85% |
| Hybrid(RAG+Tool Use) | 3.5회 | 6.0초 | 4.5x | 85~95% |
| Hybrid(Router) | 2.5회 | 4.5초 | 3.2x | 82~92% |

<v-click>

<div class="mt-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 text-sm">

**핵심 인사이트**
- Simple LLM → RAG: 비용 1.8배, 정확도 10~15%p 향상
- Tool Use의 가치는 정확도가 아닌 **"행동 능력"(쓰기 작업)**에 있다
- Hybrid(Router): Hybrid 대비 비용 30% 절감, 정확도 하락 3%p 이내

</div>

</v-click>

</div>

<!--
[스크립트]
아키텍처별로 비용과 성능이 어떻게 다른지 수치로 봅시다.

Simple LLM은 가장 빠르고 저렴합니다. 1.5초, 기준 비용 1.0x. 하지만 기업 내부 지식이 없어서 정확도는 60~75%에 그칩니다.

RAG를 추가하면 비용이 1.8배가 됩니다. Embedding API 비용과 추가 LLM 호출 때문입니다. 하지만 정확도가 10~15%p 향상됩니다.

Tool Use 단독은 2.5회 LLM 호출이 필요합니다. Tool 호출 결과를 반영한 2차 호출 때문입니다. 정확도 향상은 RAG와 비슷하지만, 행동 능력이 추가됩니다.

Hybrid는 모든 것을 결합합니다. 정확도는 85~95%로 가장 높지만, 비용도 4.5배로 가장 비쌉니다.

Hybrid Router는 절충안입니다. 필요한 요청에만 RAG나 Tool을 사용합니다. 비용 30% 절감, 정확도 하락 3%p 이내입니다.

[클릭] 핵심 인사이트입니다. Tool Use의 가치는 정확도 향상이 아니라 쓰기 작업 수행 능력에 있습니다. "할 수 있는가 없는가"의 문제입니다. Hybrid Router는 성능 최적화를 원할 때 좋은 선택입니다.

[Q&A 대비]
Q: 이 수치는 어디서 나온 건가요?
A: 경험적 추정치입니다. 실제 수치는 모델, 도메인, 데이터 품질에 따라 크게 달라집니다. 방향성 참고용으로 이해하면 됩니다.

전환: 이제 실습으로 직접 구현해봅시다.
시간: 2분
-->

---
layout: default
transition: slide-left
---

# 실습 1: Tool Use 기반 Agent 구현

<div class="overflow-hidden">

<div class="grid grid-cols-[1fr_1fr] gap-4">

<div>

<v-clicks>

**목표**: Function Calling 전체 흐름 직접 구현

**30분** (I DO 8분 / WE DO 10분 / YOU DO 12분)

**I DO**: 강사가 `search_orders` Tool 1개로 전체 Agent 루프를 시연

**WE DO**: `cancel_order` Tool을 함께 추가, description 작성법 실습

</v-clicks>

</div>

<div>

<v-click>

**YOU DO 템플릿**

```python
# TODO: 3개 이상의 Tool 정의
tools = [
    {
        "type": "function",
        "function": {
            "name": "...",
            # 언제/왜 사용하는지 (30자 이상)
            "description": "...",
            "parameters": { ... },
        },
    },
]
```

</v-click>

</div>

</div>

<v-click>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 text-sm mt-4">

**검증 기준**: Tool 3개 이상 / description 30자 이상 / LLM이 적절한 Tool 선택 / Tool 불필요 시 직접 답변

</div>

</v-click>

</div>

<!--
[스크립트]
세션의 실습 시간입니다. 첫 번째 실습은 Tool Use 기반 Agent 직접 구현입니다.

[클릭] 목표는 Function Calling의 전체 흐름을 직접 손으로 짜보는 겁니다. 30분 동안 세 단계로 진행합니다.

[클릭] I DO 단계에서 강사가 search_orders Tool 1개를 정의하고, 5단계 흐름 전체를 시연합니다. Tool description의 중요성을 강조합니다.

[클릭] WE DO 단계에서는 cancel_order Tool을 함께 추가합니다. 강사가 이끌고 여러분이 따라갑니다. description을 어떻게 쓰는지, required 파라미터를 어떻게 설정하는지 함께 작성합니다.

[클릭] YOU DO 단계에서는 Session 3에서 여러분이 설계한 Agent에 Tool을 3개 이상 정의하고 Agent 루프를 구현합니다.

[클릭] 검증 기준은 네 가지입니다. Tool이 3개 이상인지, description이 30자 이상으로 상세한지, LLM이 적절한 Tool을 선택하는지, Tool이 불필요한 질문에는 직접 답변하는지입니다.

[Q&A 대비]
Q: 어떤 Tool을 만들어야 할지 모르겠습니다.
A: Session 3에서 설계한 Agent의 Sub-task를 생각해보세요. 외부 시스템 조회나 실행이 필요한 것을 Tool로 만들면 됩니다.

전환: 실습 1이 끝나면 RAG 파이프라인을 직접 구현합니다.
시간: 1분
-->

---
layout: default
transition: slide-left
---

# 실습 2: RAG 파이프라인 구현

<div class="overflow-hidden">

<div class="grid grid-cols-[1fr_1fr] gap-4">

<div>

<v-clicks>

**목표**: Chunking → Embedding → Retrieval → Generation 전체 구현

**30분** (I DO 8분 / WE DO 10분 / YOU DO 12분)

**I DO**: 3개 문서로 RAG 시연, "전자제품 환불 기한" 질문

**WE DO**: top_k를 1, 2, 5로 바꾸며 품질 차이 확인

</v-clicks>

</div>

<div>

<v-click>

**YOU DO 과제**

- 본인 도메인 문서 5개 이상 준비
- 3가지 질문으로 테스트
- top_k 최적값 탐색 기록

</v-click>

<v-click>

<div class="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-3 text-sm mt-3">

**top_k 가이드라인**<br>
- 너무 작으면: 정보 누락<br>
- 너무 크면: 관련 없는 정보 혼입<br>
- 권장: **3~5개**

</div>

</v-click>

</div>

</div>

<v-click>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 text-sm mt-2">

**검증 기준**: 문서 5개 이상 / 3가지 질문 모두 정확한 문서 검색 / top_k 비교 실험 결과 기록

</div>

</v-click>

</div>

<!--
[스크립트]
두 번째 실습은 RAG 파이프라인 직접 구현입니다.

[클릭] RAG의 네 단계를 직접 코드로 짜봅니다. 30분입니다.

[클릭] I DO에서 강사가 3개 문서로 RAG를 구현하고, "전자제품 환불 기한이 어떻게 되나요?"를 질문합니다. 각 단계를 설명하면서 진행합니다.

[클릭] WE DO에서는 top_k 값을 함께 바꿔보며 실험합니다. top_k가 1이면 정보가 부족할 수 있습니다. top_k가 5면 관련 없는 문서도 포함될 수 있습니다. 왜 3~5가 권장값인지 직접 확인합니다.

[클릭] YOU DO에서는 본인 도메인의 문서를 5개 이상 준비합니다. HR 규정이든, 기술 문서든 상관없습니다. 3가지 질문으로 테스트하고 top_k 최적값을 찾습니다.

[클릭] 검증 기준입니다. 문서 5개 이상, 3가지 질문 모두 정확한 문서를 검색, top_k 비교 실험 결과를 기록합니다.

[Q&A 대비]
Q: Chunking은 어떻게 해야 하나요?
A: 예제에서는 문서 1개가 1개의 chunk입니다. 실제로는 큰 문서를 300~800 토큰 단위로 분할합니다. langchain의 RecursiveCharacterTextSplitter를 사용하면 간편합니다.

전환: 실습 1, 2를 완료하면 의사결정 실습을 진행합니다.
시간: 1분
-->

---
layout: default
transition: slide-left
---

# 실습 3: 아키텍처 선택 의사결정 실습

<div class="overflow-hidden">

<div class="grid grid-cols-[1fr_1fr] gap-4">

<div>

<v-clicks>

**목표**: Session 1에서 도출한 Agent 후보에 의사결정 트리 적용

**25분** (I DO 5분 / WE DO 8분 / YOU DO 12분)

**I DO**: "코드 리뷰 자동화" 시나리오로 Hybrid(RAG as Tool) 선택 시연

**WE DO**: "DevOps 장애 대응 자동화"를 함께 분석

</v-clicks>

</div>

<div>

<v-click>

```python
architecture_decision = {
    "candidate_name": "후보 이름",
    "requirements": {
        "needs_write": True,
        "needs_realtime": True,
        "needs_doc_search": False,
    },
    "decision": "Tool Use / RAG / Hybrid",
    "pattern": "RAG as Tool / ...",
    "reasoning": [
        "이유 1: ...",
    ],
    "alternative_considered": "...",
}
```

</v-click>

</div>

</div>

<v-click>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 text-sm mt-2">

**검증 기준**: 3가지 축 모두 분석 / 선택이 Session 3 기획서와 논리적 일치 / 대안 배제 이유 설명

</div>

</v-click>

</div>

<!--
[스크립트]
세 번째 실습은 분석과 설계 중심입니다. 코드가 아닌 의사결정 연습입니다.

[클릭] Session 1에서 여러분이 도출한 Agent 후보 2개에 의사결정 트리를 적용합니다.

[클릭] I DO에서 강사가 "코드 리뷰 자동화" 시나리오로 시연합니다. Q1: 코드베이스 분석은 읽기, PR 코멘트 작성은 쓰기. Q2: 코딩 컨벤션 문서 검색 필요. → Hybrid(RAG as Tool) 선택.

[클릭] WE DO에서 "DevOps 장애 대응 자동화"를 함께 분석합니다. Q1부터 Q5를 단계별로 풀어갑니다.

[클릭] YOU DO는 구조화된 Python dict 형태로 작성합니다. candidate_name, 세 가지 축 요구사항, 최종 결정, 패턴, 이유, 고려했다 배제한 대안을 작성합니다.

[클릭] 검증 기준입니다. 3가지 축이 모두 분석되었는지, 선택이 Session 3 기획서의 목적과 논리적으로 일치하는지, 대안 아키텍처를 고려하고 배제 이유를 설명했는지입니다.

[Q&A 대비]
Q: "대안 아키텍처 배제 이유"를 어떻게 써야 하나요?
A: "RAG 배제 - 실시간 데이터를 API로 수집해야 하므로 정적 문서 검색인 RAG는 부적합" 형태로 씁니다. 왜 다른 선택이 아닌지를 설명하면 됩니다.

전환: 실습까지 모두 마쳤습니다. Day 1 전체를 정리해봅시다.
시간: 1분
-->

---
layout: default
transition: fade
---

# Session 4 핵심 정리

<div class="overflow-hidden">

<v-clicks>

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 mb-2">

<strong>Tool Use(Function Calling / MCP)</strong>: LLM에게 행동 능력(Tool)을 부여한다<br>
<span class="text-sm">LLM은 "무엇을 호출할지 결정", 애플리케이션은 "실제로 호출하고 검증"</span>

</div>

<div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-3 mb-2">

<strong>RAG</strong>: LLM에게 지식(문서)을 주입한다<br>
<span class="text-sm">Retrieval 단계가 전체 품질을 좌우한다. 본질적으로 읽기 전용 시스템</span>

</div>

<div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-3 mb-2">

<strong>Hybrid</strong>: 행동(Tool Use)과 지식(RAG)을 결합한다<br>
<span class="text-sm">RAG as Tool / RAG-then-Act / Router 중 상황에 맞게 선택</span>

</div>

<div class="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-3">

<strong>의사결정 3축</strong>: 쓰기 필요 여부 → 실시간성 → 문서 검색 필요 여부<br>
<span class="text-sm">점진적 접근: 단일 아키텍처에서 시작하여 필요에 따라 Hybrid로 확장</span>

</div>

</v-clicks>

</div>

<!--
[스크립트]
Session 4의 핵심을 정리합니다.

[클릭] Tool Use입니다. Function Calling은 벤더별 구현이고 MCP는 이를 연결하는 표준 방식입니다. 핵심은 역할 분리입니다. LLM은 무엇을 호출할지 결정하고, 코드가 실제로 실행합니다.

[클릭] RAG. LLM에게 지식을 주입합니다. 검색 단계가 품질을 좌우합니다. 읽기 전용이라는 한계를 기억하세요.

[클릭] Hybrid. 두 가지를 결합합니다. 세 가지 패턴 중 상황에 맞게 선택하고, 초기에는 디버깅이 쉬운 패턴으로 시작하세요.

[클릭] 의사결정은 세 가지 축으로 합니다. 쓰기가 필요한가, 실시간성이 필요한가, 대량 문서 검색이 필요한가. 그리고 항상 단일 아키텍처에서 시작하세요.

전환: 이제 Day 1 전체를 한눈에 돌아봅시다.
시간: 1분
-->

---
layout: default
transition: fade
---

# Day 1 종합 정리

<div class="overflow-hidden">

<div class="grid grid-cols-[1fr_1fr] gap-6">

<div>

<v-clicks>

**Session 1: 문제 정의와 구조 판단**
- 언제 Agent가 필요한지 판단 기준
- Pain → Task → Skill → Tool 프레임워크
- RAG vs Agent 선택 기준

**Session 2: LLM 동작 원리와 통제**
- Token · Context Window · Hallucination
- 프롬프트 전략과 Structured Output
- 비용·지연 최적화 전략

</v-clicks>

</div>

<div>

<v-clicks>

**Session 3: Agent 기획서 구조화**
- 6가지 구성요소로 요구사항 명세
- 기획서 품질 자동 검증
- 기획서 → 기술 설계 1:1 매핑

**Session 4: Tool Use · RAG · Hybrid**
- Tool로 행동 능력 부여
- RAG로 지식 주입
- 의사결정 3축으로 아키텍처 선택

</v-clicks>

</div>

</div>

<v-click>

<div class="mt-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-3 text-center">

내일(Day 2)부터는 오늘 배운 개념을 바탕으로 **직접 프로덕션 수준의 Agent를 구현**합니다

</div>

</v-click>

</div>

<!--
[스크립트]
Day 1 전체를 돌아봅시다. 오늘 하루 동안 정말 많은 것을 배웠습니다.

[클릭] Session 1에서는 문제를 먼저 정의하는 법을 배웠습니다. 언제 Agent가 필요한지 판단하고, Pain에서 Tool까지 내려가는 프레임워크로 문제를 구조화했습니다.

[클릭] Session 2에서는 LLM의 동작 원리를 다뤘습니다. Token, Context Window, Hallucination, 프롬프트 전략, Structured Output, 그리고 비용 최적화까지 설계에 직접 필요한 개념을 정리했습니다.

[클릭] Session 3에서는 Agent 기획서를 구조화했습니다. 6가지 구성요소로 요구사항을 명세하고, 품질을 검증하고, 기술 설계로 1:1 매핑하는 법을 봤습니다.

[클릭] Session 4에서는 오늘의 마지막 퍼즐 조각을 맞췄습니다. Tool Use로 행동 능력을 붙이고, RAG로 지식을 주입하고, 의사결정 트리로 상황에 맞는 아키텍처를 선택하는 법을 배웠습니다.

[클릭] 내일부터는 오늘 배운 모든 개념을 바탕으로 실제 프로덕션 수준의 Agent를 직접 구현합니다. 오늘 배운 개념들이 내일 코드로 살아납니다.

[Q&A 대비]
Q: 오늘 배운 것을 복습하려면 어떻게 해야 하나요?
A: 각 세션의 코드 예제를 직접 실행해보세요. 특히 Session 4의 세 실습을 본인 도메인에 맞게 완성해보면 개념이 확실히 잡힙니다.

전환: 마지막으로 내일 준비사항을 안내하고 마무리합니다.
시간: 2분
-->

---
layout: end
transition: fade
---

# Day 1 수고하셨습니다

**내일(Day 2) 준비사항**

- 오늘 실습 코드 로컬에 저장 및 동작 확인
- Session 3 Agent 기획서 최종 정리
- Session 4 실습 3 의사결정 결과 확인

<div class="absolute bottom-10 left-0 right-0 text-center text-sm opacity-50">

AI Agent 개발 실무 과정 · Day 1

</div>

<!--
[스크립트]
오늘 하루 정말 수고하셨습니다. 8시간 동안 AI Agent의 개념부터 아키텍처 설계까지, 방대한 내용을 다뤘습니다.

내일을 위한 준비사항 세 가지입니다. 첫째, 오늘 실습 코드를 로컬에 저장하고 동작을 확인해두세요. 내일 실습의 기반이 됩니다. 둘째, Session 3에서 작성한 Agent 기획서를 최종 정리해두세요. 내일 실제 구현의 시작점이 됩니다. 셋째, Session 4 실습 3의 의사결정 결과를 다시 한번 확인하세요. 내일 어떤 아키텍처로 시작할지 결정에 활용합니다.

질문 있으신 분은 지금 해주시거나, 내일 시작 전에 말씀해주세요. 다들 수고하셨습니다. 내일 만나겠습니다!

[Q&A 대비]
Q: 오늘 배운 라이브러리들을 설치해야 하나요?
A: openai, numpy 패키지가 필요합니다. `pip install openai numpy`로 설치하세요. 실습용 API 키와 예제 문서를 함께 준비해두면 복습이 수월합니다.

Q: 기획서 양식이 정해져 있나요?
A: Session 3 실습에서 사용한 구조화된 딕셔너리 형태를 유지하면 됩니다. 내일 첫 시간에 기획서를 기반으로 설계 리뷰를 진행합니다.

시간: 1분
-->
