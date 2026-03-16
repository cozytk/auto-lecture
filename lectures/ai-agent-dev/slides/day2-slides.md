---
theme: default
title: AI Agent 전문 개발 과정 - Day 2
transition: slide-left
mdc: true
---

# AI Agent 전문 개발 과정

## Day 2: 구조 설계에서 리팩토링까지

<div class="mt-8 text-lg text-gray-500 overflow-hidden">
Session 1: Agent 4요소와 구조 판단<br>
Session 2: LangGraph 제어 흐름 설계<br>
Session 3: Tool Validation Guard와 Audit Trail<br>
Session 4: Subgraph 리팩토링과 Parity 검증
</div>

<div v-motion :initial="{ y: 24, opacity: 0 }" :enter="{ y: 0, opacity: 1 }" class="mt-8 inline-block bg-blue-50 dark:bg-blue-900/30 rounded-lg px-5 py-3 text-sm font-medium">
오늘의 운영 원칙: 이론 3 · 실습 7
</div>

<!--
[스크립트]
안녕하세요. Day 2는 Day 1에서 정한 MVP 후보를 이제 실제 구조와 코드로 바꾸는 날입니다. 오늘은 Agent를 State로 쪼개고, LangGraph로 제어 흐름을 만들고, Tool 호출을 통제하고, 마지막에는 모놀리식 그래프를 서브그래프로 리팩토링해 parity까지 확인합니다. 발표보다 실습 비중이 훨씬 크기 때문에 슬라이드는 방향만 짚고 바로 랩으로 넘어가겠습니다.

[Q&A 대비]
Q: Day 2는 Day 1을 몰라도 들을 수 있나요?
A: 가능은 하지만 비효율적입니다. Day 1에서 정한 문제 정의와 MVP 후보가 오늘 모든 설계의 입력값이 됩니다.

Q: 오늘도 개념 설명이 길게 있나요?
A: 핵심 개념만 짧게 정리하고 대부분의 시간은 실습과 코드 리뷰에 사용합니다.

전환: 먼저 오늘 수업이 어떤 비율로 운영되는지부터 보겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# Day 2 운영 맵

<div class="grid grid-cols-[4fr_6fr] gap-6 overflow-hidden mt-4">
  <div>
    <div v-motion :initial="{ scale: 0.9, opacity: 0 }" :enter="{ scale: 1, opacity: 1 }" class="bg-blue-50 dark:bg-blue-900/30 rounded-xl p-6 text-center">
      <div class="text-5xl font-bold text-blue-700 dark:text-blue-300">145분</div>
      <div class="mt-2 text-sm">핵심 이론 정리</div>
    </div>
    <div v-motion :initial="{ scale: 0.9, opacity: 0 }" :enter="{ scale: 1, opacity: 1, transition: { delay: 160 } }" class="bg-green-50 dark:bg-green-900/30 rounded-xl p-6 text-center mt-4">
      <div class="text-5xl font-bold text-green-700 dark:text-green-300">335분</div>
      <div class="mt-2 text-sm">Lab Pack 실습</div>
    </div>
  </div>
  <div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">Session 1 후 <code>01-agent-architecture-studio</code></div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">Session 2 후 <code>05-langgraph-control-flow</code></div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">Session 3 후 <code>06-tool-validation-guard</code></div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">Session 4 후 <code>02-refactor-boundary-workshop</code></div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 text-sm">마지막에 <code>07-subgraph-refactor-parity</code></div>

    <div v-click class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4 text-sm">
      오늘의 기준선은 <strong>설명보다 handoff</strong>입니다.<br>
      슬라이드에서 결정 기준을 만들고, 랩에서 바로 고정합니다.
    </div>
  </div>
</div>

<!--
[스크립트]
Day 2는 480분 전체 중 약 145분만 이론입니다. 나머지 335분은 실습입니다. 그래서 오늘 슬라이드의 목적은 정보를 많이 보여주는 것이 아니라, 각 세션에서 무엇을 결정하고 어떤 랩으로 넘겨야 하는지 명확히 하는 데 있습니다. [클릭] Session 1 뒤에는 구조 설계 워크숍으로 갑니다. [클릭] Session 2 뒤에는 LangGraph 제어 흐름 실습으로 바로 이어집니다. [클릭] Session 3 뒤에는 Tool Guard 실습으로 넘어갑니다. [클릭] Session 4 뒤에는 먼저 경계 문서를 만들고, [클릭] 마지막에 parity 검증까지 갑니다. [클릭] 오늘은 이해했다에서 끝나면 안 되고, 반드시 문서나 코드 산출물로 남겨야 합니다.

[Q&A 대비]
Q: 이론 설명을 줄이면 개념 이해가 부족하지 않나요?
A: 그래서 Session guide를 Source of Truth로 두고, 슬라이드에서는 판단 기준만 압축합니다. 부족한 설명은 가이드와 랩에서 보완합니다.

Q: 랩을 다 못 끝내면 어떻게 하나요?
A: 각 세션마다 최소 산출물을 정해두었기 때문에, 완성보다 핵심 구조를 남기는 것을 우선합니다.

전환: 그럼 Day 1에서 무엇을 가져와야 오늘 작업이 이어지는지 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# Day 1 입력값

<div class="grid grid-cols-2 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">문제 정의 결과</div>
    <div class="text-sm">어떤 Pain을 해결할지 이미 정해져 있어야 합니다.</div>
  </div>
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">프롬프트 비교 경험</div>
    <div class="text-sm">어떤 Tool 통제 규칙이 필요한지 감이 있어야 합니다.</div>
  </div>
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">구조 판단표</div>
    <div class="text-sm">Single-step인지, Multi-step인지 출발선이 있어야 합니다.</div>
  </div>
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-blue-700 dark:text-blue-300">최종 MVP 후보 1개</div>
    <div class="text-sm">오늘 모든 실습은 이 후보를 구조화하는 과정입니다.</div>
  </div>
</div>

<!--
[스크립트]
Day 2는 빈 종이에서 시작하지 않습니다. [클릭] 첫째, 어떤 문제를 풀지 정의한 결과가 있어야 합니다. [클릭] 둘째, Day 1에서 프롬프트를 비교해본 경험이 있어야 Tool 통제 기준을 세울 수 있습니다. [클릭] 셋째, 이미 구조 판단표가 있어야 Single-step인지 Multi-step인지 빠르게 결정할 수 있습니다. [클릭] 마지막으로 가장 중요하게, MVP 후보 1개가 있어야 합니다. 오늘은 새로운 아이디어를 계속 만드는 날이 아니라, 선택한 후보 하나를 구조와 코드로 밀어붙이는 날입니다.

[Q&A 대비]
Q: Day 1에서 후보를 여러 개 뽑았으면 어떻게 하나요?
A: 오늘은 하나만 고르세요. 구조 설계와 랩 실습은 집중도가 중요해서 후보를 여러 개 들고 가면 끝까지 못 갑니다.

Q: Day 1 산출물이 부족하면 오늘 실습을 못 하나요?
A: 못 하지는 않지만 시작 속도가 느려집니다. 부족한 부분은 Session 1 워크숍에서 먼저 복구합니다.

전환: 오늘 끝날 때 반드시 남겨야 하는 산출물을 먼저 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# 설계 산출물

<v-clicks>

- Agent State 초안 1개
- Sub-task 분해표 1개
- Single-step / Multi-step 판단 기록 1개
- Conditional Edge 분기표 1개
- Retry / Fallback 정책 메모 1개

</v-clicks>

<div v-click class="mt-6 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-sm">
이 다섯 개가 없으면 랩을 했더라도 <strong>구조가 남지 않은 것</strong>입니다.
</div>

<!--
[스크립트]
오늘 전반부 산출물은 구조 문서입니다. [클릭] Agent State 초안이 있어야 하고, [클릭] Sub-task 분해표가 있어야 하며, [클릭] Single-step인지 Multi-step인지 선택 이유가 남아야 합니다. [클릭] Session 2에서는 Conditional Edge 분기표가 필요하고, [클릭] Retry와 Fallback 정책 메모도 남겨야 합니다. [클릭] 이 문서가 없으면 코드를 잠깐 실행했더라도 재사용이 불가능합니다. Day 3와 Day 4로 연결되는 기반 문서라고 생각하시면 됩니다.

[Q&A 대비]
Q: 꼭 문서 형식으로 남겨야 하나요?
A: 네. Day 2는 설계 근거를 외부화하는 날입니다. 머릿속 이해만으로는 다음 세션에서 재현되지 않습니다.

Q: 코드가 잘 되면 문서는 생략해도 되나요?
A: 안 됩니다. 오늘은 구조를 설명할 수 있어야 하는 날이어서 문서와 코드가 함께 있어야 합니다.

전환: 후반부에는 검증 산출물이 추가됩니다.
시간: 2분
-->

---
transition: slide-left
---

# 검증 산출물

<v-clicks>

- Tool Validation 규칙표 1개
- Audit Trail 샘플 1개
- 리팩토링 경계 문서 1개
- 리팩토링 전후 parity 결과 1개
- Day 2 통합 Agent 프로토타입 1개

</v-clicks>

<div v-click class="mt-6 bg-green-50 dark:bg-green-900/30 rounded-lg p-4 text-sm">
Day 2의 완료 기준은 <strong>동작했다</strong>가 아니라 <strong>설명 가능하고 검증 가능하다</strong>입니다.
</div>

<!--
[스크립트]
후반부 산출물은 검증 중심입니다. [클릭] Tool Validation 규칙표가 있어야 하고, [클릭] 실제 Audit Trail 샘플이 있어야 합니다. [클릭] Session 4에서는 어디서 그래프를 끊을지 경계 문서를 남겨야 하고, [클릭] 리팩토링 전후 parity 결과도 필요합니다. [클릭] 마지막으로 통합 Agent 프로토타입까지 있어야 Day 2를 제대로 마친 것입니다. [클릭] 즉 오늘의 핵심은 구조, 통제, 검증입니다.

[Q&A 대비]
Q: parity 결과는 테스트 로그만 있으면 되나요?
A: 최소한 어떤 필드를 비교했고 왜 같다고 판단했는지까지 남기는 것이 좋습니다.

Q: Audit Trail은 성공 로그만 남기면 되나요?
A: 아닙니다. 거부와 실패가 더 중요합니다. 왜 막혔는지를 남겨야 나중에 설명할 수 있습니다.

전환: 이제 Session 1로 들어가겠습니다. 첫 질문은 구조를 어디서부터 자를 것인가입니다.
시간: 2분
-->

---
layout: section
transition: fade
---

# Session 1
## Agent 4요소와 구조 판단

<div v-motion :initial="{ y: 30, opacity: 0 }" :enter="{ y: 0, opacity: 1 }" class="mt-8 text-sm text-gray-500">
핵심 질문: Agent를 어떤 State와 실행 단위로 쪼갤 것인가
</div>

<!--
[스크립트]
Session 1에서는 구조를 정합니다. 아직 그래프를 복잡하게 그리기 전에, Agent를 어떤 상태 필드로 모델링할지, 어떤 단위로 분해할지, Single-step으로 갈지 Multi-step으로 갈지를 결정합니다. Day 2 전체에서 가장 중요한 선행 판단입니다.

[Q&A 대비]
Q: Session 1에서 바로 LangGraph 코드를 쓰나요?
A: 아주 일부만 보지만, 중심은 구조 결정입니다. 코드 구현은 Session 2부터 본격화됩니다.

Q: 구조 판단을 빨리 끝내도 되나요?
A: 이 판단을 대충 하면 이후 세션에서 그래프를 계속 다시 뜯게 됩니다.

전환: 먼저 이 세션의 핵심 질문을 한 줄로 잡아보겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# 먼저 정할 것

<div class="flex items-center justify-center h-64 overflow-hidden">
  <div v-motion :initial="{ scale: 0.86, opacity: 0 }" :enter="{ scale: 1, opacity: 1 }" class="text-center bg-amber-50 dark:bg-amber-900/30 rounded-xl p-8 border-2 border-amber-300 max-w-[760px]">
    <div class="text-3xl font-bold text-amber-700 dark:text-amber-300 mb-4">"이 Agent의 State는 무엇이고, 실행 단위는 어디까지인가?"</div>
    <div class="text-lg text-gray-600 dark:text-gray-300">좋은 Session 2 코드는 좋은 Session 1 구조에서만 나옵니다</div>
  </div>
</div>

<!--
[스크립트]
Session 1의 핵심 질문은 이것입니다. 이 Agent의 State는 무엇이고, 실행 단위는 어디까지인가. LangGraph를 배우기 전에 이 질문이 먼저입니다. State가 모호하면 Node가 섞이고, 실행 단위가 모호하면 Planner와 Executor가 뒤엉킵니다. 오늘 Session 2와 Session 3의 품질은 사실상 여기서 결정됩니다.

[Q&A 대비]
Q: 우선 코드를 짜고 나중에 State를 정리하면 안 되나요?
A: 가능하지만 대부분 되돌아오게 됩니다. State가 먼저 고정돼야 그래프가 안정됩니다.

Q: 실행 단위라는 말은 Node를 뜻하나요?
A: 네, 실무적으로는 Node와 거의 같은 뜻으로 보시면 됩니다. 다만 더 넓게는 Sub-task 단위까지 포함합니다.

전환: 그 구조의 기본 뼈대가 바로 Agent 4요소입니다.
시간: 2분
-->

---
transition: slide-left
---

# 4요소는 State 뼈대

<div class="grid grid-cols-2 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-red-50 dark:bg-red-900/30 rounded-lg p-4">
    <div class="font-bold text-red-700 dark:text-red-300 mb-1">Goal</div>
    <div class="text-sm">무엇을 끝내면 이 Agent가 성공인가</div>
  </div>
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
    <div class="font-bold text-blue-700 dark:text-blue-300 mb-1">Memory</div>
    <div class="text-sm">무엇을 기억해야 다음 판단이 가능한가</div>
  </div>
  <div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
    <div class="font-bold text-green-700 dark:text-green-300 mb-1">Tool</div>
    <div class="text-sm">외부 세계에 어떤 방식으로 접근하는가</div>
  </div>
  <div v-click class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4">
    <div class="font-bold text-purple-700 dark:text-purple-300 mb-1">Control Logic</div>
    <div class="text-sm">언제 반복하고, 분기하고, 멈출 것인가</div>
  </div>
</div>

<!--
[스크립트]
Agent 4요소는 개념 설명용 표가 아니라 State 설계의 뼈대입니다. [클릭] Goal은 성공 조건이고, [클릭] Memory는 다음 판단에 필요한 맥락이며, [클릭] Tool은 외부 접근 수단이고, [클릭] Control Logic은 반복과 분기와 종료 조건입니다. 오늘 Session 1의 핵심은 이 네 요소를 추상 용어로 두지 않고 실제 State 필드와 제어 규칙으로 바꾸는 것입니다.

[Q&A 대비]
Q: 4요소가 모두 별도 필드여야 하나요?
A: 꼭 1:1 필드는 아니지만, 네 요소에 대응하는 정보가 State나 설정에 분명히 있어야 합니다.

Q: Tool은 State에 꼭 넣어야 하나요?
A: 사용 가능한 Tool 목록이나 허용 범위는 보통 State나 설정 레이어에 명시하는 편이 좋습니다.

전환: 먼저 Goal을 어떻게 써야 하는지 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# Goal은 종료 문장

<v-clicks>

- 문제 설명이 아니라 종료 조건이어야 합니다
- "언제 끝났다고 볼 것인가"가 한 줄에 있어야 합니다
- 모호한 Goal은 Control Logic을 흐리게 만듭니다
- 좋은 Goal은 평가 기준까지 같이 줍니다

</v-clicks>

<div v-click class="mt-6 bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-sm">
나쁜 예: 고객 문의를 잘 처리한다<br>
좋은 예: FAQ로 해결하거나, 실패 시 담당자에게 에스컬레이션하고 종료한다
</div>

<!--
[스크립트]
Goal은 추상적인 비전 문장이 아니라 종료 문장입니다. [클릭] 문제 설명이 아니어야 하고, [클릭] 언제 끝났다고 판단할지 포함해야 하며, [클릭] 그래야 Control Logic이 흔들리지 않습니다. [클릭] 좋은 Goal은 나중에 평가 기준으로도 사용됩니다. [클릭] 예를 들어 고객 문의 Agent라면, FAQ로 해결하거나 실패 시 담당자에게 에스컬레이션하고 종료한다고 써야 합니다. 그래야 무한히 검색만 하는 구조를 막을 수 있습니다.

[Q&A 대비]
Q: Goal에 성공률이나 SLA도 넣어야 하나요?
A: 가능하면 좋습니다. 특히 운영 Agent라면 응답 시간, 정확도, 에스컬레이션 조건이 포함되면 더 좋습니다.

Q: Goal이 여러 개인 경우는요?
A: 우선순위를 둬서 하나의 주 Goal로 압축하세요. 여러 Goal을 동등하게 두면 제어가 흔들립니다.

전환: 그다음은 Memory입니다. State가 커지는 가장 흔한 원인이죠.
시간: 2분
-->

---
transition: slide-left
---

# Memory는 셋만 먼저

<div class="grid grid-cols-3 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">대화 히스토리</div>
    <div class="text-sm">사용자 요구와 맥락</div>
  </div>
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">작업 상태</div>
    <div class="text-sm">현재 step, 반복 횟수, route</div>
  </div>
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">Tool 결과</div>
    <div class="text-sm">다음 판단에 필요한 중간 산출물</div>
  </div>
</div>

<div v-click class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4 text-sm">
Memory를 많이 담는 것보다 <strong>다음 판단에 필요한 것만 남기는 것</strong>이 더 중요합니다.
</div>

<!--
[스크립트]
Memory는 처음부터 크게 잡지 마세요. [클릭] 대화 히스토리, [클릭] 작업 상태, [클릭] Tool 결과 이 세 범주로 시작하면 대부분 충분합니다. [클릭] 핵심은 모든 것을 저장하는 것이 아니라 다음 판단에 필요한 것만 남기는 것입니다. State가 비대해지면 Session 2에서 reducer와 propagation이 복잡해지고, Session 4에서 서브그래프 분리가 어려워집니다.

[Q&A 대비]
Q: 검색 결과 원문을 전부 State에 저장해야 하나요?
A: 보통은 아닙니다. 다음 단계에 필요한 요약본이나 핵심 필드만 저장하는 편이 안전합니다.

Q: Memory와 Checkpoint는 같은 개념인가요?
A: 아닙니다. Memory는 실행 중 상태 자체이고, Checkpoint는 그 상태를 저장하고 복원하는 메커니즘입니다.

전환: 이제 Tool을 어떻게 설계할지 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# Tool은 목록보다 규칙

<v-clicks>

- Tool 이름보다 호출 조건이 중요합니다
- 읽기 / 쓰기 구분이 먼저입니다
- 위험 수준을 함께 기록해야 Session 3이 쉬워집니다
- 허용되지 않은 Tool은 처음부터 경계 밖에 둡니다

</v-clicks>

<div v-click class="mt-6 bg-green-50 dark:bg-green-900/30 rounded-lg p-4 text-sm">
`search_db`, `web_search`, `send_notification`처럼<br>
<strong>용도 + 부수효과 + 위험 수준</strong>을 같이 적어두세요.
</div>

<!--
[스크립트]
Tool 설계에서 자주 하는 실수가 목록만 길게 쓰는 것입니다. [클릭] 중요한 것은 이름이 아니라 언제 호출하는가입니다. [클릭] 그래서 읽기와 쓰기 구분을 먼저 하고, [클릭] 위험 수준을 함께 적어야 Session 3에서 Validation 정책으로 자연스럽게 연결됩니다. [클릭] 애초에 허용하지 않을 Tool은 구조 밖으로 두는 것이 좋습니다. [클릭] Tool을 기술 명세가 아니라 운영 규칙으로 기록한다고 생각하세요.

[Q&A 대비]
Q: 같은 Tool을 읽기와 쓰기로 동시에 쓸 수 있나요?
A: 가능하지만 호출 모드를 분리해 적는 것이 좋습니다. 예를 들어 DB read와 DB write는 사실상 다른 위험도로 봐야 합니다.

Q: Tool이 아직 확정되지 않았으면요?
A: 구체 구현체가 아니라 역할 수준으로 먼저 적어도 됩니다. 다만 읽기/쓰기와 위험도는 미리 정해야 합니다.

전환: 마지막 요소는 Control Logic입니다. 여기서 루프와 종료 조건이 정해집니다.
시간: 2분
-->

---
transition: slide-left
---

# Control Logic이 품질을 만든다

<div class="grid grid-cols-[1fr_1fr_1fr] gap-4 overflow-hidden mt-4">
  <div v-click class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4 text-center">
    <div class="font-bold mb-2">시작 조건</div>
    <div class="text-sm">언제 그래프를 시작하는가</div>
  </div>
  <div v-click class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4 text-center">
    <div class="font-bold mb-2">반복 조건</div>
    <div class="text-sm">언제 재시도하거나 재계획하는가</div>
  </div>
  <div v-click class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4 text-center">
    <div class="font-bold mb-2">종료 조건</div>
    <div class="text-sm">언제 finish 또는 escalate 하는가</div>
  </div>
</div>

<div v-click class="mt-6 bg-red-50 dark:bg-red-900/30 rounded-lg p-4 text-sm">
Control Logic이 비어 있으면 Session 2의 loop가 길어지고, Session 3의 guard가 뒤늦게 붙습니다.
</div>

<!--
[스크립트]
Control Logic은 단순한 if-else가 아니라 운영 규칙입니다. [클릭] 언제 시작하는지, [클릭] 언제 반복하는지, [클릭] 언제 종료하는지를 먼저 써야 합니다. [클릭] 이 정의가 없으면 그래프가 길어지고 guard가 계속 뒤에 붙습니다. 실무에서는 Session 2에서 루프를 만들기 전에 Control Logic 메모를 먼저 보는 습관이 중요합니다.

[Q&A 대비]
Q: 종료 조건은 하나만 있어야 하나요?
A: 보통 성공 종료와 실패 종료, 에스컬레이션 종료처럼 여러 개가 있습니다. 다만 각각을 명시해야 합니다.

Q: 재계획은 어디에 포함되나요?
A: 반복 조건 안에 포함됩니다. 어떤 실패나 새로운 정보가 들어왔을 때 Planner로 되돌릴지 적어두면 됩니다.

전환: 이제 Planner와 Executor를 언제 분리해야 하는지 판단해보겠습니다.
시간: 2분
-->

---
layout: two-cols-header
transition: slide-left
---

# Planner vs Executor

::left::

<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 h-56 overflow-hidden">

**Single-step에 가까울 때**

<v-clicks>

- Tool 호출이 1회면 충분
- 중간 결과가 다음 행동을 바꾸지 않음
- 실패 시 단순 재시도로 끝남

</v-clicks>

</div>

::right::

<div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 h-56 overflow-hidden">

**Planner-Executor가 필요할 때**

<v-clicks>

- Sub-task 분해가 먼저 필요
- 실행 결과가 계획을 바꿀 수 있음
- 실패 시 re-planning이 필요함

</v-clicks>

</div>

<!--
[스크립트]
Planner-Executor 패턴은 강력하지만 모든 Agent에 필요한 것은 아닙니다. 왼쪽처럼 Tool 호출이 사실상 한 번이면 끝나고, 중간 결과가 다음 행동을 바꾸지 않으면 Single-step에 가깝습니다. 반면 오른쪽처럼 먼저 Sub-task를 분해해야 하고, 실행 결과에 따라 계획이 바뀌며, 실패 시 재계획이 필요하다면 Planner와 Executor를 분리하는 편이 좋습니다.

[Q&A 대비]
Q: Planner-Executor를 쓰면 항상 더 좋은가요?
A: 아닙니다. 단순한 작업에는 오히려 비용과 복잡도만 늘립니다.

Q: Planner가 없으면 Multi-step Agent를 못 만드나요?
A: 꼭 그렇진 않습니다. 하지만 단계 수가 늘어날수록 계획과 실행 분리가 유지보수에 유리합니다.

전환: Sub-task를 어떻게 쪼개야 하는지도 함께 봐야 합니다.
시간: 3분
-->

---
transition: slide-left
---

# 분해 전략은 셋

<div class="grid grid-cols-3 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-orange-50 dark:bg-orange-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-orange-700 dark:text-orange-300">순차 분해</div>
    <div class="text-sm">이전 결과가 다음 입력이 되는 경우</div>
  </div>
  <div v-click class="bg-teal-50 dark:bg-teal-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-teal-700 dark:text-teal-300">병렬 분해</div>
    <div class="text-sm">서로 의존하지 않는 수집 작업</div>
  </div>
  <div v-click class="bg-indigo-50 dark:bg-indigo-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-indigo-700 dark:text-indigo-300">계층 분해</div>
    <div class="text-sm">큰 작업을 더 작은 계획 단위로 재귀 분해</div>
  </div>
</div>

<div v-click class="mt-6 bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-sm">
실무 팁: 첫 번째 초안은 보통 <strong>3~7개 Sub-task</strong> 범위에서 가장 관리하기 쉽습니다.
</div>

<!--
[스크립트]
Sub-task 분해 전략은 세 가지입니다. [클릭] 순차 분해는 보고서 생성처럼 앞 단계 결과가 다음 단계 입력이 되는 경우입니다. [클릭] 병렬 분해는 여러 소스에서 독립적으로 데이터를 모을 때 적합합니다. [클릭] 계층 분해는 복잡도가 높아서 한 번 더 계획을 쪼개야 할 때 사용합니다. [클릭] 처음 초안을 만들 때는 3개에서 7개 정도의 Sub-task가 가장 다루기 쉽습니다. 너무 적으면 추상적이고, 너무 많으면 제어가 어려워집니다.

[Q&A 대비]
Q: 병렬 분해는 무조건 빠른가요?
A: 아니요. 병렬 실행 오버헤드와 결합 비용이 있기 때문에 의존성이 없을 때만 의미가 있습니다.

Q: 계층 분해는 언제 과하다고 보나요?
A: 한 단계 더 쪼갤수록 실행과 디버깅 비용이 급증합니다. 실제로 필요한 복잡도인지 먼저 보세요.

전환: 결국 마지막 판단은 Single-step과 Multi-step 중 어디에 서는가입니다.
시간: 3분
-->

---
transition: slide-left
---

# 구조 선택 기준

<v-clicks>

- Tool 호출이 1회면 Single-step 우선
- 이전 결과가 다음 행동을 바꾸면 Multi-step 검토
- fallback 경로가 필요하면 Multi-step 쪽입니다
- 상태 누적이 핵심이면 그래프 구조가 필요합니다

</v-clicks>

<div v-click class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4 text-sm">
오늘 기본 원칙은 <strong>Single-step 우선</strong>입니다.<br>
복잡도가 증명될 때만 그래프를 늘립니다.
</div>

<!--
[스크립트]
구조 선택 기준은 네 줄로 정리할 수 있습니다. [클릭] Tool 호출이 사실상 1회면 Single-step부터 시작합니다. [클릭] 이전 결과가 다음 행동을 바꾸면 Multi-step을 검토합니다. [클릭] fallback 경로가 필요하면 그래프 구조가 유리합니다. [클릭] 상태 누적이 핵심이면 그래프 구조가 필요합니다. [클릭] 오늘의 기본 원칙은 Single-step 우선입니다. 복잡도가 증명될 때만 Multi-step으로 갑니다.

[Q&A 대비]
Q: 복잡해 보이는 요청이면 무조건 Multi-step인가요?
A: 아닙니다. 실제로는 단일 조회와 단일 응답으로 해결되는 경우가 많습니다. 겉보기에 속지 말고 Tool 수와 분기 수를 보세요.

Q: 나중에 Multi-step으로 바꾸기 어렵지 않나요?
A: State와 인터페이스를 잘 잡아두면 점진적 전환이 가능합니다. 그래서 Session 1이 중요합니다.

전환: 이제 첫 랩으로 넘어갈 준비가 됐습니다.
시간: 2분
-->

---
transition: slide-left
---

# 실습 01 handoff

<div class="grid grid-cols-[6fr_4fr] gap-6 overflow-hidden mt-4">
  <div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">Goal / Memory / Tool / Control Logic 캔버스 작성</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">Sub-task 분해표와 의존성 기록</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">Single-step / Multi-step 선택 이유 문서화</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 text-sm">Day 1 MVP 후보 1개만 대상으로 진행</div>
  </div>
  <div>
    <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-sm">
      <div class="font-bold mb-2">연결 랩</div>
      <div>`01-agent-architecture-studio`</div>
      <div class="mt-2">예상 시간: 70분</div>
    </div>
  </div>
</div>

<div class="absolute bottom-6 left-14 text-xs opacity-50">
`lectures/ai-agent-dev/labs/day2/01-agent-architecture-studio/README.md`
</div>

<!--
[스크립트]
이제 첫 번째 랩으로 넘어갑니다. [클릭] Agent 4요소 캔버스를 작성하고, [클릭] Sub-task 분해표와 의존성을 남기고, [클릭] Single-step인지 Multi-step인지 선택 이유를 문서화합니다. [클릭] 오늘은 후보를 하나만 잡고 끝까지 갑니다. 이 랩의 결과물이 Session 2의 State 필드와 route 설계로 그대로 이어집니다.

[Q&A 대비]
Q: 이 랩에서 코드를 꼭 써야 하나요?
A: 중심은 README 기반 설계입니다. 다만 원하면 간단한 State 초안 코드를 같이 적어도 됩니다.

Q: 어떤 산출물이 최소 통과선인가요?
A: 4요소 캔버스, Sub-task 분해표, 구조 선택 메모 세 가지입니다.

전환: 랩을 마치고 오면 Session 2에서 이 문서를 그래프로 바꾸겠습니다.
시간: 3분
-->

---
layout: section
transition: fade
---

# Session 2
## LangGraph 제어 흐름 설계

<div v-motion :initial="{ y: 30, opacity: 0 }" :enter="{ y: 0, opacity: 1 }" class="mt-8 text-sm text-gray-500">
핵심 질문: 그래프 제어 흐름을 어떻게 설계할 것인가
</div>

<!--
[스크립트]
Session 2에서는 Session 1에서 만든 구조 문서를 LangGraph 그래프로 옮깁니다. Node, Edge, State를 맞추고, Conditional Edge와 Retry/Fallback을 실제로 작동하는 제어 흐름으로 바꾸는 단계입니다. 오늘 구현 감각을 가장 많이 얻는 세션이기도 합니다.

[Q&A 대비]
Q: LangChain보다 LangGraph를 먼저 배우는 이유가 뭔가요?
A: Day 2의 핵심은 제어 흐름이기 때문입니다. 단순 체인보다 그래프가 오늘 주제에 더 직접적입니다.

Q: Session 2가 끝나면 바로 프로덕션 Agent가 되나요?
A: 아직 아닙니다. Session 3의 Validation Guard가 붙어야 운영 가능한 구조가 됩니다.

전환: 먼저 왜 그래프가 필요한지부터 보겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# 체인보다 그래프

<div class="grid grid-cols-[1fr_1fr] gap-6 overflow-hidden mt-4">
  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-5">
    <div class="font-bold mb-3">Linear Chain</div>
    <div v-click class="text-sm mb-2">A → B → C</div>
    <div v-click class="text-sm mb-2">항상 같은 경로</div>
    <div v-click class="text-sm">분기와 루프 표현이 약함</div>
  </div>
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-5">
    <div class="font-bold mb-3 text-blue-700 dark:text-blue-300">State Graph</div>
    <div v-click class="text-sm mb-2">A → B 또는 C</div>
    <div v-click class="text-sm mb-2">상황에 따라 route 결정</div>
    <div v-click class="text-sm">retry / fallback / loop 표현 가능</div>
  </div>
</div>

<!--
[스크립트]
Day 2에서 체인보다 그래프를 강조하는 이유는 간단합니다. 왼쪽의 선형 체인은 항상 같은 경로를 탑니다. 반면 우리가 만들 Agent는 같은 요청이라도 상황에 따라 다른 다음 행동을 선택해야 합니다. 그래서 오른쪽처럼 route를 바꾸고, retry와 fallback을 넣고, loop도 표현할 수 있는 그래프가 필요합니다.

[Q&A 대비]
Q: 단순 파이프라인이면 그래프가 과한가요?
A: 맞습니다. 그 경우는 체인이나 Single-step 구조가 더 낫습니다. 그래프는 분기와 반복이 필요할 때 가치가 큽니다.

Q: 그래프를 쓰면 시각화가 쉬워지나요?
A: 네. 가능한 경로를 설계 단계에서 한눈에 볼 수 있다는 것이 큰 장점입니다.

전환: 그래프를 구성하는 가장 기본 단위 세 개를 다시 정리하겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# Node · Edge · State

<div class="grid grid-cols-3 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">Node</div>
    <div class="text-sm">실행 단위 함수</div>
  </div>
  <div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">Edge</div>
    <div class="text-sm">다음 실행 경로</div>
  </div>
  <div v-click class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">State</div>
    <div class="text-sm">Node 사이 공유 데이터</div>
  </div>
</div>

<div v-click class="mt-6 bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-sm">
실무 해석: <strong>Node는 일</strong>, <strong>Edge는 결정</strong>, <strong>State는 근거</strong>입니다.
</div>

<!--
[스크립트]
LangGraph를 가장 실용적으로 이해하는 방식은 이 세 줄입니다. [클릭] Node는 실제 일을 하는 함수이고, [클릭] Edge는 다음 실행 경로를 정하는 연결이며, [클릭] State는 Node 사이를 흐르는 공유 데이터입니다. [클릭] 실무적으로 보면 Node는 일, Edge는 결정, State는 근거입니다. 이 셋 중 하나가 모호하면 그래프가 빠르게 복잡해집니다.

[Q&A 대비]
Q: Node가 너무 커지면 어떤 문제가 생기나요?
A: 테스트가 어려워지고 Session 4에서 서브그래프로 나누기 힘들어집니다.

Q: Edge에 비즈니스 로직을 많이 넣어도 되나요?
A: route 함수는 가볍고 명확할수록 좋습니다. 복잡한 판단은 State와 Node 설계를 다시 보는 것이 낫습니다.

전환: 그다음으로 많이 헷갈리는 것이 State 업데이트 규칙입니다.
시간: 2분
-->

---
transition: slide-left
---

# State 업데이트 규칙

<v-clicks>

- Node는 전체 State를 다시 쓰지 않습니다
- 바뀐 필드만 dict로 반환합니다
- reducer가 있으면 누적되고, 없으면 교체됩니다
- 반환하지 않은 필드는 그대로 유지됩니다

</v-clicks>

<div v-click class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4 text-sm">
`messages`와 `log`는 보통 누적,<br>
`current_step`와 `confidence`는 보통 교체입니다.
</div>

<!--
[스크립트]
LangGraph State 업데이트는 부분 업데이트가 기본입니다. [클릭] Node는 전체 State를 덮어쓰지 않고, [클릭] 바뀐 필드만 반환합니다. [클릭] reducer가 있는 필드는 누적되고, 없는 필드는 교체됩니다. [클릭] 반환하지 않은 필드는 유지됩니다. [클릭] 그래서 messages나 log는 누적 reducer를 두고, current_step이나 confidence는 교체하는 경우가 많습니다.

[Q&A 대비]
Q: reducer를 아무 필드에나 붙여도 되나요?
A: 가능하지만 의도가 분명해야 합니다. counter에 잘못 붙이면 예상치 못한 누적이 생깁니다.

Q: 중첩 dict도 이렇게 관리하나요?
A: 가능은 하지만 복잡해집니다. Day 2에서는 평탄한 State를 권장합니다.

전환: 이제 그래프가 Agent다워지는 지점, Conditional Edge를 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# Conditional Edge 패턴

<div class="grid grid-cols-3 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-cyan-50 dark:bg-cyan-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-cyan-700 dark:text-cyan-300">이진 분기</div>
    <div class="text-sm">success / fail</div>
  </div>
  <div v-click class="bg-cyan-50 dark:bg-cyan-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-cyan-700 dark:text-cyan-300">다중 분기</div>
    <div class="text-sm">access / billing / incident</div>
  </div>
  <div v-click class="bg-cyan-50 dark:bg-cyan-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-cyan-700 dark:text-cyan-300">루프 분기</div>
    <div class="text-sm">retry / finish / fallback</div>
  </div>
</div>

<div v-click class="mt-6 bg-red-50 dark:bg-red-900/30 rounded-lg p-4 text-sm">
루프를 설계할 때는 <strong>종료 조건이 먼저</strong>입니다. route 함수가 아니라 종료 조건부터 씁니다.
</div>

<!--
[스크립트]
Conditional Edge는 세 가지 패턴만 기억하면 됩니다. [클릭] 성공과 실패를 나누는 이진 분기, [클릭] 요청 유형별로 보내는 다중 분기, [클릭] retry와 finish와 fallback을 오가는 루프 분기입니다. [클릭] 특히 루프 분기를 설계할 때는 route 함수보다 종료 조건을 먼저 써야 무한 루프를 막을 수 있습니다.

[Q&A 대비]
Q: route 함수 반환값은 꼭 node 이름과 같아야 하나요?
A: path_map을 쓰면 달라도 되지만, 초반에는 같게 두는 편이 훨씬 덜 헷갈립니다.

Q: 분기 로직이 많아지면 어떻게 해야 하나요?
A: 분류 기준을 별도 Node에서 먼저 정리하고 route 함수는 그 결과만 읽게 하세요.

전환: 그다음은 운영 안정성을 만드는 Retry와 Fallback입니다.
시간: 2분
-->

---
transition: slide-left
---

# Retry와 Fallback

<div class="grid grid-cols-[1fr_1fr] gap-6 overflow-hidden mt-4">
  <div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-5">
    <div class="font-bold mb-3 text-green-700 dark:text-green-300">Retry</div>
    <div v-click class="text-sm mb-2">일시적 실패 대응</div>
    <div v-click class="text-sm mb-2">같은 작업을 다시 시도</div>
    <div v-click class="text-sm">최대 횟수와 backoff 필요</div>
  </div>
  <div class="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-5">
    <div class="font-bold mb-3 text-amber-700 dark:text-amber-300">Fallback</div>
    <div v-click class="text-sm mb-2">구조적 실패 대응</div>
    <div v-click class="text-sm mb-2">대체 경로로 전환</div>
    <div v-click class="text-sm">품질 저하를 감수하고 종료</div>
  </div>
</div>

<!--
[스크립트]
Retry와 Fallback은 비슷해 보이지만 전혀 다른 전략입니다. 왼쪽 Retry는 일시적 실패에 대응합니다. 같은 작업을 다시 시도하는 것이고, 최대 횟수와 backoff가 필요합니다. 오른쪽 Fallback은 구조적 실패에 대응합니다. 같은 시도를 반복하지 않고 대체 경로로 전환합니다. 품질은 조금 낮아질 수 있지만, 사용자는 종료 가능한 결과를 받게 됩니다.

[Q&A 대비]
Q: 실패하면 항상 Retry부터 해야 하나요?
A: 일시적 실패라면 그렇습니다. 하지만 입력 형식 불일치나 미지원 요청이면 바로 Fallback이나 Reject가 맞습니다.

Q: Fallback은 실패를 숨기는 것 아닌가요?
A: 아닙니다. 낮은 품질의 대체 경로임을 로그와 응답에 남겨야 합니다.

전환: 아주 짧은 코드로 Conditional Edge 구조를 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# route 함수 예시

```python {1-4|6-8|10-14}
def route_after_quality(state):
    if state["confidence"] >= 0.8:
        return "finish"

    if state["attempts"] >= state["max_attempts"]:
        return "fallback"

    return state["route"]

graph.add_conditional_edges(
    "quality_gate",
    route_after_quality,
    {"finish": "finish", "fallback": "fallback",
     "incident": "incident", "billing": "billing"},
)
```

<!--
[스크립트]
이 코드는 Day 2에서 가장 자주 보게 될 route 함수 형태입니다. [클릭] confidence가 기준 이상이면 finish로 갑니다. [클릭] 최대 시도 수를 넘기면 fallback으로 갑니다. [클릭] 둘 다 아니면 원래 route로 다시 보냅니다. [클릭] 그리고 add_conditional_edges에서 반환값을 실제 Node에 연결합니다. 핵심은 route 함수가 짧고 읽기 쉬워야 한다는 점입니다.

[Q&A 대비]
Q: 왜 원래 route를 State에 저장하나요?
A: 재시도 시 어디로 되돌아가야 하는지 route 함수가 알아야 하기 때문입니다.

Q: finish와 fallback을 같은 handler에서 처리해도 되나요?
A: 가능하지만 의미가 다르므로 초반에는 분리하는 편이 로그와 디버깅에 유리합니다.

전환: 이제 Session 2 랩으로 바로 넘어가겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# 실습 05 handoff

<div class="grid grid-cols-[6fr_4fr] gap-6 overflow-hidden mt-4">
  <div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm"><code>classify</code>와 유형별 handler를 연결합니다</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm"><code>quality_gate</code>에서 retry / finish / fallback을 나눕니다</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">Session 1의 구조 메모를 State 필드로 번역합니다</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 text-sm">route 반환값과 node 이름을 반드시 맞춥니다</div>
  </div>
  <div>
    <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-sm">
      <div class="font-bold mb-2">연결 랩</div>
      <div>`05-langgraph-control-flow`</div>
      <div class="mt-2">예상 시간: 85분</div>
    </div>
  </div>
</div>

<div class="absolute bottom-6 left-14 text-xs opacity-50">
`lectures/ai-agent-dev/labs/05-langgraph-control-flow/README.md`
</div>

<!--
[스크립트]
Session 2 랩에서는 실제로 그래프를 만듭니다. [클릭] classify와 handler를 연결하고, [클릭] quality_gate에서 retry, finish, fallback을 나눕니다. [클릭] Session 1에서 만든 구조 메모를 이제 State 필드로 바꿉니다. [클릭] 가장 흔한 실수는 route 반환값과 node 이름 불일치이니 그 부분을 꼭 점검하세요.

[Q&A 대비]
Q: 이 랩의 최소 완료 기준은 무엇인가요?
A: build_graph가 완성되고, 세 시나리오가 의도한 route로 흐르는지 확인하면 최소 통과입니다.

Q: fallback까지 구현해야 하나요?
A: 네. Day 2에서는 성공 경로만이 아니라 실패 종료 경로까지 설계해야 합니다.

전환: 랩 이후에는 Tool 호출을 통제하는 Session 3으로 가겠습니다.
시간: 3분
-->

---
layout: section
transition: fade
---

# Session 3
## Tool Validation Guard

<div v-motion :initial="{ y: 30, opacity: 0 }" :enter="{ y: 0, opacity: 1 }" class="mt-8 text-sm text-gray-500">
핵심 질문: Tool 호출을 어떻게 통제하고 검증할 것인가
</div>

<!--
[스크립트]
Session 3에서는 Agent를 운영 가능한 구조로 만듭니다. Session 2에서 만든 그래프는 잘 동작할 수 있지만, Tool 호출이 무제한이거나 잘못된 파라미터를 그대로 실행하면 위험합니다. 그래서 Validation Guard와 결과 검증, Audit Trail을 붙입니다.

[Q&A 대비]
Q: Tool Guard는 보안 기능인가요, 품질 기능인가요?
A: 둘 다입니다. 안전과 운영 품질을 동시에 지키는 계층입니다.

Q: Session 2 그래프를 버리고 다시 만드나요?
A: 아닙니다. Session 2 그래프에 검증 계층을 추가하는 개념으로 보시면 됩니다.

전환: 왜 Tool 호출을 제로 트러스트로 봐야 하는지부터 시작하겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# Tool 호출은 비신뢰 입력

<div class="flex items-center justify-center h-60 overflow-hidden">
  <div v-motion :initial="{ scale: 0.88, opacity: 0 }" :enter="{ scale: 1, opacity: 1 }" class="text-center bg-red-50 dark:bg-red-900/30 rounded-xl p-8 border-2 border-red-300 max-w-[760px]">
    <div class="text-3xl font-bold text-red-700 dark:text-red-300 mb-4">LLM이 고른 Tool 호출도 그대로 믿지 않습니다</div>
    <div class="text-lg text-gray-600 dark:text-gray-300">웹 입력을 검증하듯 Agent의 action도 검증합니다</div>
  </div>
</div>

<!--
[스크립트]
Session 3의 핵심 관점은 이것입니다. LLM이 골랐다고 해서 Tool 호출을 신뢰하지 않습니다. Tool 호출도 결국 확률 모델이 만든 출력이기 때문에, 사용자 입력처럼 검증 대상입니다. 이 관점이 없으면 잘못된 Tool 선택, 파라미터 에러, 무한 호출, 부수효과 사고가 모두 한 번에 들어옵니다.

[Q&A 대비]
Q: LLM이 function calling으로 구조화된 출력을 주면 안전하지 않나요?
A: 형식이 맞는 것과 안전한 것은 다릅니다. 권한, 정책, 맥락은 별도 검증이 필요합니다.

Q: 모든 Tool 호출을 사람 승인으로 돌려야 하나요?
A: 아닙니다. 읽기 Tool은 자동 승인, 위험 Tool만 승인 대기처럼 계층화하는 것이 일반적입니다.

전환: 어떤 위험을 막아야 하는지 먼저 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# 위험 지도

<v-clicks>

- 잘못된 Tool 선택
- 파라미터 타입 / 범위 에러
- 무한 호출 루프
- 쓰기 / 삭제 부수효과 미통제

</v-clicks>

<div v-click class="mt-6 bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-sm">
Day 2의 목표는 Tool 호출을 많이 하게 만드는 것이 아니라<br>
<strong>설명 가능한 호출만 통과시키는 것</strong>입니다.
</div>

<!--
[스크립트]
Tool 호출 위험은 크게 네 가지입니다. [클릭] 잘못된 Tool 선택, [클릭] 파라미터 에러, [클릭] 무한 호출 루프, [클릭] 부수효과 미통제입니다. [클릭] 그래서 Day 2에서 중요한 것은 Tool을 많이 연결하는 것이 아니라, 어떤 호출이 왜 통과했고 왜 막혔는지를 설명 가능하게 만드는 것입니다.

[Q&A 대비]
Q: 가장 흔한 사고는 무엇인가요?
A: 실무에서는 무한 재시도와 잘못된 파라미터 전달이 가장 흔합니다.

Q: 읽기 Tool도 위험한가요?
A: 네. 비용 폭발이나 정보 과다 노출 같은 문제가 있을 수 있어서 제한은 필요합니다.

전환: 그 위험을 막는 기본 구조가 Validation 파이프라인입니다.
시간: 2분
-->

---
transition: slide-left
---

# Validation은 3단계

<div class="grid grid-cols-3 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">Schema</div>
    <div class="text-sm">필수값, 타입, 범위</div>
  </div>
  <div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">Policy</div>
    <div class="text-sm">권한, 위험 등급, 호출 한도</div>
  </div>
  <div v-click class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4">
    <div class="font-bold mb-2">Context</div>
    <div class="text-sm">지금 이 호출이 맥락상 맞는가</div>
  </div>
</div>

<div v-click class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4 text-sm">
낮은 비용의 검증을 앞에 두면 대부분의 잘못된 호출을 빨리 차단할 수 있습니다.
</div>

<!--
[스크립트]
Validation은 세 단계로 나눕니다. [클릭] Schema는 타입과 범위를 보고, [클릭] Policy는 권한과 위험도와 호출 한도를 봅니다. [클릭] Context는 지금 이 호출이 정말 필요한지, 중복은 아닌지를 봅니다. [클릭] 이 순서가 중요한 이유는 앞단 검증이 더 싸고 빠르기 때문입니다. 값이 깨졌는데 정책 검증부터 할 이유가 없죠.

[Q&A 대비]
Q: 세 단계를 한 함수에서 처리해도 되나요?
A: 가능하지만 실패 사유를 설명하기 어려워집니다. Day 2에서는 분리하는 편이 학습에도 운영에도 좋습니다.

Q: Context Validation은 꼭 필요한가요?
A: 네. 타입은 맞아도 같은 Tool을 세 번 연속 부르는 식의 비정상 흐름을 여기서 잡습니다.

전환: 이 검증이 그래프 안에서 어떻게 작동하는지 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# Validation Gate 루프

<div class="grid grid-cols-[3fr_2fr_3fr] gap-4 overflow-hidden mt-6 items-center">
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-center">LLM Node</div>
  <div v-click class="text-center text-2xl font-bold text-gray-400">→</div>
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-center">Validation Gate</div>
</div>

<div class="grid grid-cols-[3fr_2fr_3fr] gap-4 overflow-hidden mt-4 items-center">
  <div v-click class="bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4 text-center">ToolMessage로 교정 요청</div>
  <div v-click class="text-center text-2xl font-bold text-gray-400">←</div>
  <div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4 text-center">Tool Executor</div>
</div>

<!--
[스크립트]
Validation Gate는 LLM과 Tool 실행 사이에 서는 게이트키퍼입니다. [클릭] LLM이 Tool 호출을 제안하면, [클릭] Validation Gate가 먼저 검사합니다. [클릭] 통과한 것만 Tool Executor로 갑니다. [클릭] 거부되면, [클릭] ToolMessage로 왜 막혔는지 설명하고, [클릭] 다시 LLM에게 교정 기회를 줍니다. 이 rejection-correction 루프가 있어야 Agent가 같은 실수를 줄일 수 있습니다.

[Q&A 대비]
Q: 거부되면 바로 종료하지 않는 이유가 뭔가요?
A: 잘못된 Tool 하나가 막혔다고 전체 목표가 실패한 것은 아니기 때문입니다. LLM이 대안을 고를 수 있어야 합니다.

Q: 그러면 무한히 교정 루프가 돌지 않나요?
A: 그래서 iteration guard가 반드시 함께 들어갑니다.

전환: Tool 실행 후에도 검증은 한 번 더 필요합니다.
시간: 2분
-->

---
transition: slide-left
---

# 결과 검증은 별도다

<v-clicks>

- L1 구조 검증: 파싱 가능한가
- L2 의미 검증: 값이 논리적으로 맞는가
- L3 일관성 검증: 이전 결과와 모순되지 않는가

</v-clicks>

<div v-click class="mt-6 bg-red-50 dark:bg-red-900/30 rounded-lg p-4 text-sm">
HTTP 200과 실행 성공은 <strong>유효한 결과</strong>와 같은 말이 아닙니다.
</div>

<!--
[스크립트]
Tool이 성공했다고 끝이 아닙니다. [클릭] 먼저 구조 검증으로 파싱 가능한지 보고, [클릭] 의미 검증으로 값이 논리적으로 맞는지 보고, [클릭] 마지막으로 이전 결과와 모순 없는지 봅니다. [클릭] HTTP 200이 왔다고 그 데이터가 유효한 것은 아닙니다. 이 구분이 없으면 Agent가 그럴듯하게 틀린 답을 내기 쉽습니다.

[Q&A 대비]
Q: L3까지 항상 막아야 하나요?
A: 보통 L3는 경고 수준으로 두는 경우가 많습니다. 실제 급변이 정상일 수도 있기 때문입니다.

Q: 구조 검증 실패면 Retry가 맞나요?
A: 대개 그렇습니다. 깨진 JSON이나 일시적 형식 오류는 재시도로 복구될 수 있습니다.

전환: 이런 모든 흐름을 설명 가능하게 만드는 것이 Audit Trail입니다.
시간: 2분
-->

---
transition: slide-left
---

# Audit Trail 최소 필드

<div class="grid grid-cols-2 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">실행 맥락</div>
    <div class="text-sm">timestamp, session_id, user_id</div>
  </div>
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">호출 정보</div>
    <div class="text-sm">tool_name, parameters, call_count</div>
  </div>
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">검증 결과</div>
    <div class="text-sm">schema / policy / context pass or fail</div>
  </div>
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-blue-700 dark:text-blue-300">실행 결과</div>
    <div class="text-sm">status, latency, error, result summary</div>
  </div>
</div>

<!--
[스크립트]
Audit Trail은 print 로그보다 훨씬 구조적이어야 합니다. [클릭] 실행 맥락, [클릭] 호출 정보, [클릭] 검증 결과, [클릭] 실행 결과가 최소 필드입니다. 이 정도가 있어야 나중에 어떤 Tool이 왜 거부됐는지, 실패가 어디서 발생했는지, 비용이 어디서 나갔는지 설명할 수 있습니다.

[Q&A 대비]
Q: 성공 로그보다 실패 로그가 더 중요한가요?
A: 네. 운영에서는 실패와 거부를 설명할 수 있는 로그가 더 중요합니다.

Q: latency까지 꼭 남겨야 하나요?
A: 가능하면 남기는 것이 좋습니다. 병목 지점과 외부 Tool 품질을 판단하는 데 도움이 됩니다.

전환: 짧은 코드로 Tool Guard 구조를 확인해보겠습니다.
시간: 2분
-->

---
layout: two-cols-header
transition: slide-left
---

# Guard 핵심 코드

::left::

```python {1-8|10-15}
def route_after_schema(state):
    return "continue" if state["schema_valid"] else "reject"

def route_after_policy(state):
    return "continue" if state["policy_valid"] else "reject"

def route_after_context(state):
    return "execute" if state["context_valid"] else "reject"
```

::right::

<v-clicks>

- 각 단계가 통과 여부를 명시적으로 남깁니다
- reject는 실패가 아니라 설명 가능한 차단입니다
- execute까지 가는 경로를 좁게 만드는 것이 핵심입니다

</v-clicks>

<!--
[스크립트]
Tool Guard 코드의 핵심은 복잡한 조건문이 아니라 단계적 분기입니다. 왼쪽처럼 schema, policy, context 각각이 통과면 계속, 아니면 reject를 반환합니다. [클릭] 각 단계가 결과를 명시적으로 남겨야 하고, [클릭] reject를 실패가 아니라 설명 가능한 차단으로 봐야 하며, [클릭] execute까지 가는 경로를 좁게 만드는 것이 핵심입니다.

[Q&A 대비]
Q: reject 후에도 audit를 남겨야 하나요?
A: 반드시 남겨야 합니다. 실제 운영에서는 reject 로그가 정책 개선에 더 유용합니다.

Q: context 단계에서 자주 막히면 어떤 신호인가요?
A: 그래프 설계나 Tool 선택 전략이 불안정하다는 신호일 수 있습니다.

전환: 이제 Session 3 랩으로 넘어갑니다.
시간: 2분
-->

---
transition: slide-left
---

# 실습 06 handoff

<div class="grid grid-cols-[6fr_4fr] gap-6 overflow-hidden mt-4">
  <div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">schema / policy / context 검증을 나눕니다</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">승인 없는 위험 Tool은 policy에서 차단합니다</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-2 text-sm">결과 검증과 audit entry를 success / reject 모두에 남깁니다</div>
    <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 text-sm">Session 2의 retry 감각을 guard 안으로 가져옵니다</div>
  </div>
  <div>
    <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-sm">
      <div class="font-bold mb-2">연결 랩</div>
      <div>`06-tool-validation-guard`</div>
      <div class="mt-2">예상 시간: 80분</div>
    </div>
  </div>
</div>

<div class="absolute bottom-6 left-14 text-xs opacity-50">
`lectures/ai-agent-dev/labs/06-tool-validation-guard/README.md`
</div>

<!--
[스크립트]
Session 3 랩에서는 Tool Guard를 실제로 구현합니다. [클릭] schema, policy, context를 나누고, [클릭] 승인 없는 위험 Tool은 policy에서 막고, [클릭] success와 reject 모두 audit entry를 남기고, [클릭] Session 2에서 배운 retry 감각을 검증 파이프라인 안으로 가져옵니다. 여기서부터 Agent는 단순 데모가 아니라 운영 가능 구조에 가까워집니다.

[Q&A 대비]
Q: 이 랩에서 가장 중요한 통과 기준은 무엇인가요?
A: 위험 Tool이 policy 단계에서 차단되고, 성공/거부 모두 audit에 남는 것입니다.

Q: 결과 검증까지 다 못 하면요?
A: 최소한 구조 검증과 audit 기록까지는 반드시 남기세요. 그래야 다음 단계 parity 비교가 가능합니다.

전환: 마지막 Session 4에서는 구조를 확장 가능한 형태로 정리하겠습니다.
시간: 3분
-->

---
layout: section
transition: fade
---

# Session 4
## Subgraph 리팩토링과 확장

<div v-motion :initial="{ y: 30, opacity: 0 }" :enter="{ y: 0, opacity: 1 }" class="mt-8 text-sm text-gray-500">
핵심 질문: 구조를 어떻게 확장 가능한 형태로 리팩토링할 것인가
</div>

<!--
[스크립트]
Session 4의 목표는 기능 추가가 아니라 구조 개선입니다. Day 2 앞선 세션에서 만든 그래프가 커지기 시작하면 어디서 경계를 끊어야 하는지, 어떤 State를 공개 계약으로 삼고 어떤 것은 내부로 숨길지, 체크포인트는 어디에 둘지 결정해야 합니다. 마지막에는 리팩토링 전후 parity까지 확인합니다.

[Q&A 대비]
Q: 오늘 바로 Multi-Agent까지 가나요?
A: 개념은 다루지만 중심은 서브그래프와 모듈 경계입니다. Multi-Agent 확장은 그 다음 단계로 보시면 됩니다.

Q: 리팩토링은 성능 최적화 시간인가요?
A: 오늘은 구조와 유지보수성 중심입니다. 성능보다 경계와 계약이 먼저입니다.

전환: 먼저 언제 모놀리식 그래프를 나눠야 하는지 보겠습니다.
시간: 1분
-->

---
transition: slide-left
---

# 나눌 시점의 신호

<v-clicks>

- Node 수가 10개를 넘기기 시작합니다
- State 필드가 15개 이상으로 늘어납니다
- 한 Node 수정이 다른 Node를 자주 깨뜨립니다
- 특정 Node를 단독 테스트하기 어렵습니다

</v-clicks>

<div v-click class="mt-6 bg-red-50 dark:bg-red-900/30 rounded-lg p-4 text-sm">
리팩토링 기준은 파일 수가 아니라 <strong>State 의존성</strong>입니다.
</div>

<!--
[스크립트]
모놀리식 그래프를 나눌 시점에는 몇 가지 신호가 있습니다. [클릭] Node 수가 많아지고, [클릭] State 필드가 비대해지고, [클릭] 한 Node 수정이 다른 Node를 깨뜨리고, [클릭] 단독 테스트가 어려워집니다. [클릭] 중요한 것은 파일 수가 아니라 State 의존성입니다. 어떤 Node들이 같은 필드를 자주 읽고 쓰는지가 경계의 기준입니다.

[Q&A 대비]
Q: 작은 프로젝트도 미리 나누는 게 낫지 않나요?
A: 과하면 오히려 관리 비용만 늘어납니다. 먼저 단일 구조로 의미 있는 복잡도가 생겼는지 보세요.

Q: 테스트가 어렵다는 기준은 뭔가요?
A: 특정 Node 하나를 검증하려고 전체 그래프를 다 돌려야 하면 이미 강하게 결합된 상태입니다.

전환: 나눌 때는 통신 계약을 같이 설계해야 합니다.
시간: 2분
-->

---
transition: slide-left
---

# 경계 뒤에는 계약

<div class="grid grid-cols-[1fr_1fr] gap-6 overflow-hidden mt-4">
  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-5">
    <div class="font-bold mb-3">나쁜 경계</div>
    <div v-click class="text-sm mb-2">내부 캐시 구조를 직접 참조</div>
    <div v-click class="text-sm mb-2">깊은 중첩 필드를 그대로 노출</div>
    <div v-click class="text-sm">부모가 자식 구현 상세를 알아야 함</div>
  </div>
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-5">
    <div class="font-bold mb-3 text-blue-700 dark:text-blue-300">좋은 경계</div>
    <div v-click class="text-sm mb-2">입력 키와 출력 키를 고정</div>
    <div v-click class="text-sm mb-2">어댑터가 State 변환 담당</div>
    <div v-click class="text-sm">내부 전용 State는 숨김</div>
  </div>
</div>

<!--
[스크립트]
그래프를 나눌 때는 코드 분리보다 계약이 먼저입니다. 왼쪽처럼 내부 캐시 구조나 깊은 중첩 필드를 그대로 참조하면 경계가 있어도 의미가 없습니다. 반면 오른쪽처럼 입력 키와 출력 키를 고정하고, 어댑터가 State 변환을 맡고, 내부 전용 State를 숨기면 나중에 서브그래프를 교체하기 쉬워집니다.

[Q&A 대비]
Q: 어댑터가 추가되면 코드가 더 길어지지 않나요?
A: 짧게는 그렇지만 변경 영향 범위를 크게 줄여줍니다. Agent 수가 늘수록 이 이점이 커집니다.

Q: 내부 전용 State의 예시는 무엇인가요?
A: retry_count, 임시 캐시, collection_status 같은 값이 대표적입니다.

전환: 그 계약을 실제 구조로 옮기는 도구가 서브그래프입니다.
시간: 2분
-->

---
transition: slide-left
---

# 서브그래프의 가치

<div class="grid grid-cols-2 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-green-700 dark:text-green-300">캡슐화</div>
    <div class="text-sm">수집 내부 재시도 로직을 부모가 몰라도 됩니다</div>
  </div>
  <div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-green-700 dark:text-green-300">재사용</div>
    <div class="text-sm">같은 수집 파이프라인을 다른 부모 그래프에서도 씁니다</div>
  </div>
  <div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-green-700 dark:text-green-300">독립 테스트</div>
    <div class="text-sm">서브그래프만 따로 실행해 검증할 수 있습니다</div>
  </div>
  <div v-click class="bg-green-50 dark:bg-green-900/30 rounded-lg p-4">
    <div class="font-bold mb-2 text-green-700 dark:text-green-300">점진적 확장</div>
    <div class="text-sm">Node 하나를 서브그래프로 교체하며 진화시킵니다</div>
  </div>
</div>

<!--
[스크립트]
서브그래프의 가치는 네 가지로 정리할 수 있습니다. [클릭] 캡슐화, [클릭] 재사용, [클릭] 독립 테스트, [클릭] 점진적 확장입니다. Day 2에서는 특히 캡슐화와 parity 검증이 중요합니다. 내부 재시도 로직을 숨긴 채도 부모 그래프가 같은 결과를 낼 수 있어야 좋은 리팩토링입니다.

[Q&A 대비]
Q: 서브그래프를 쓰면 자동으로 Multi-Agent가 되나요?
A: 아닙니다. 아직은 같은 프로세스 안의 모듈화에 가깝습니다. Multi-Agent는 그 위 단계입니다.

Q: 부모와 자식 사이에 어떤 키가 공유되나요?
A: 보통 같은 이름을 가진 키만 공유합니다. 그래서 명명 규칙이 중요합니다.

전환: 장기 실행 관점에서는 체크포인트와 thread도 함께 봐야 합니다.
시간: 2분
-->

---
transition: slide-left
---

# 체크포인트와 thread

<div class="grid grid-cols-3 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-center">
    <div class="font-bold mb-2">Checkpointer</div>
    <div class="text-sm">중단 후 재개</div>
  </div>
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-center">
    <div class="font-bold mb-2">thread_id</div>
    <div class="text-sm">세션 분리</div>
  </div>
  <div v-click class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-center">
    <div class="font-bold mb-2">Pruning</div>
    <div class="text-sm">오래된 memory 정리</div>
  </div>
</div>

<div v-click class="mt-6 bg-amber-50 dark:bg-amber-900/30 rounded-lg p-4 text-sm">
긴 작업, 재개 가치가 큰 작업, 멀티 사용자 환경부터 우선 적용합니다.
</div>

<!--
[스크립트]
Session 4에서는 상태 관리 확장도 같이 봅니다. [클릭] Checkpointer는 중단 후 재개를 가능하게 하고, [클릭] thread_id는 사용자나 세션을 분리하고, [클릭] pruning은 오래된 memory를 정리합니다. [클릭] 모든 그래프에 한 번에 붙이기보다, 긴 작업과 재개 가치가 큰 작업부터 우선 적용하는 것이 현실적입니다.

[Q&A 대비]
Q: Checkpointer 없이도 데모는 되는데 꼭 필요한가요?
A: 데모는 되지만 운영 환경에서는 중단 복구와 긴 대화 관리가 필요해집니다.

Q: MemorySaver를 그대로 써도 되나요?
A: 학습과 데모에는 좋지만, 프로덕션에서는 영속 저장소로 가는 것이 맞습니다.

전환: 이제 리팩토링 순서를 한 장으로 정리하겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# 리팩토링 5단계

<v-clicks>

- 의존성 매트릭스 작성
- 인터페이스 계약 고정
- Subgraph 후보 분리
- Orchestrator로 다시 연결
- 리팩토링 전후 parity 확인

</v-clicks>

<div v-click class="mt-6 bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-sm">
핵심은 <strong>구조를 바꿔도 결과는 같아야 한다</strong>는 점입니다.
</div>

<!--
[스크립트]
리팩토링은 다섯 단계로 가져가면 안정적입니다. [클릭] 먼저 의존성 매트릭스를 쓰고, [클릭] 인터페이스 계약을 고정하고, [클릭] 서브그래프 후보를 분리하고, [클릭] Orchestrator로 다시 연결하고, [클릭] 마지막에 parity를 확인합니다. [클릭] 구조가 좋아졌다는 말보다 결과가 같다는 증명이 먼저여야 합니다.

[Q&A 대비]
Q: parity를 나중에 한 번만 보면 되나요?
A: 작게 나눌수록 자주 보는 편이 안전합니다. 큰 폭 리팩토링 후 한 번에 보면 원인 파악이 어렵습니다.

Q: 통합 테스트가 없으면 어떻게 하나요?
A: 최소한 핵심 출력 필드와 데이터 개수라도 비교해 parity 기준을 만드세요.

전환: 그래서 Day 2의 정의된 완료 상태가 바로 parity입니다.
시간: 2분
-->

---
transition: slide-left
---

# Parity가 완료 정의

<div class="grid grid-cols-[1fr_1fr] gap-6 overflow-hidden mt-4">
  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-5">
    <div class="font-bold mb-3">비교 필드</div>
    <div v-click class="text-sm mb-2"><code>report</code></div>
    <div v-click class="text-sm mb-2"><code>insights</code></div>
    <div v-click class="text-sm"><code>raw_data</code> 길이</div>
  </div>
  <div class="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-5">
    <div class="font-bold mb-3 text-purple-700 dark:text-purple-300">추가 확인</div>
    <div v-click class="text-sm mb-2">내부 전용 키가 부모에 새지 않는가</div>
    <div v-click class="text-sm mb-2">리팩토링 후 흐름 설명이 쉬워졌는가</div>
    <div v-click class="text-sm">테스트 단위가 더 작아졌는가</div>
  </div>
</div>

<!--
[스크립트]
Parity는 단순 문자열 비교가 아닙니다. 왼쪽처럼 report, insights, raw_data 개수 같은 핵심 결과를 먼저 비교합니다. 그리고 오른쪽처럼 내부 전용 키가 부모에 새지 않았는지, 흐름 설명이 쉬워졌는지, 테스트 단위가 더 작아졌는지도 같이 봅니다. Day 2 리팩토링의 완료 정의는 prettier한 구조가 아니라 parity 통과입니다.

[Q&A 대비]
Q: 완전히 같은 문자열이 아니면 실패인가요?
A: 핵심 비즈니스 결과가 같다면 허용 범위를 정할 수 있습니다. 다만 무엇을 동일성 기준으로 볼지 먼저 합의해야 합니다.

Q: 내부 키가 부모에 보이면 왜 문제인가요?
A: 캡슐화가 깨졌다는 뜻입니다. 이후 변경 영향 범위가 커집니다.

전환: 마지막 두 개 랩이 바로 이 리팩토링 경계와 parity를 담당합니다.
시간: 2분
-->

---
transition: slide-left
---

# Session 4 handoff

<div class="grid grid-cols-2 gap-6 overflow-hidden mt-4">
  <div class="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-5">
    <div class="font-bold mb-3 text-blue-700 dark:text-blue-300">문서 랩</div>
    <div v-click class="text-sm mb-2"><code>02-refactor-boundary-workshop</code></div>
    <div v-click class="text-sm mb-2">의존성 매트릭스 작성</div>
    <div v-click class="text-sm">공개 키 / 내부 키 분리</div>
  </div>
  <div class="bg-green-50 dark:bg-green-900/30 rounded-lg p-5">
    <div class="font-bold mb-3 text-green-700 dark:text-green-300">코드 랩</div>
    <div v-click class="text-sm mb-2"><code>07-subgraph-refactor-parity</code></div>
    <div v-click class="text-sm mb-2">모놀리식과 서브그래프 비교</div>
    <div v-click class="text-sm">parity 체크 함수 작성</div>
  </div>
</div>

<div class="absolute bottom-6 left-14 text-xs opacity-50">
`lectures/ai-agent-dev/labs/day2/02-refactor-boundary-workshop/README.md` · `lectures/ai-agent-dev/labs/07-subgraph-refactor-parity/README.md`
</div>

<!--
[스크립트]
Session 4는 두 단계로 갑니다. [클릭] 먼저 `02-refactor-boundary-workshop`에서 의존성 매트릭스와 공개 키, 내부 키를 문서로 정리합니다. [클릭] 그 다음 `07-subgraph-refactor-parity`에서 실제 코드를 나누고 parity를 확인합니다. [클릭] 문서 없이 바로 코드를 뜯는 것보다, [클릭] 경계를 먼저 합의하고 들어가는 편이 훨씬 빠릅니다. [클릭] 마지막 코드 랩에서는 모놀리식과 서브그래프 결과를 반드시 비교하세요.

[Q&A 대비]
Q: 두 랩 중 하나만 하면 안 되나요?
A: 학습 효과가 크게 줄어듭니다. 문서 랩이 경계를 만들고, 코드 랩이 그 경계를 검증합니다.

Q: parity 체크는 어디까지 구현해야 하나요?
A: 최소한 README에 적힌 `report`, `insights`, `raw_data` 비교는 반드시 들어가야 합니다.

전환: 이제 Day 2 전체 종료 기준을 확인하고 마무리하겠습니다.
시간: 3분
-->

---
transition: slide-left
---

# Day 2 종료 기준

<v-clicks>

- State / Node / Edge로 구조를 설명할 수 있는가
- Tool 호출 전 Validation 단계를 구분할 수 있는가
- loop, retry, fallback 종료 조건을 말할 수 있는가
- 리팩토링 전후 parity 근거를 제시할 수 있는가
- Day 3 확장의 입력물을 실제로 남겼는가

</v-clicks>

<!--
[스크립트]
Day 2가 끝났다고 말하려면 다섯 가지를 설명할 수 있어야 합니다. [클릭] 구조를 State, Node, Edge로 설명할 수 있어야 하고, [클릭] Validation 단계를 구분할 수 있어야 하며, [클릭] loop와 retry와 fallback 종료 조건을 말할 수 있어야 하고, [클릭] parity 근거를 제시할 수 있어야 하며, [클릭] Day 3로 넘길 입력물을 실제로 남겨야 합니다. 오늘은 이해보다 재사용 가능한 산출물이 중요합니다.

[Q&A 대비]
Q: 통합 Agent 프로토타입까지 못 만들면 실패인가요?
A: 핵심 구조와 검증 산출물이 남아 있다면 일부 미완성은 괜찮습니다. 하지만 parity까지는 가능한 범위에서 꼭 시도해야 합니다.

Q: Day 3 입력물은 정확히 무엇인가요?
A: 구조 캔버스, Validation 정책표, 리팩토링 경계 문서가 대표적입니다.

전환: 마지막으로 Day 3와 연결되는 포인트를 보겠습니다.
시간: 2분
-->

---
transition: slide-left
---

# Day 3로 넘길 것

<div class="grid grid-cols-3 gap-4 overflow-hidden mt-4">
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">구조 캔버스</div>
    <div class="text-sm">Multi-Agent 협업 구조의 입력</div>
  </div>
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">Validation 정책표</div>
    <div class="text-sm">HITL과 안전장치 기준선</div>
  </div>
  <div v-click class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
    <div class="font-bold mb-2">리팩토링 경계 문서</div>
    <div class="text-sm">Supervisor / Subgraph 확장의 출발점</div>
  </div>
</div>

<div v-click class="mt-6 bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 text-sm">
Day 2의 산출물은 하루치 숙제가 아니라 <strong>다음 날 아키텍처 입력값</strong>입니다.
</div>

<!--
[스크립트]
Day 2 산출물은 Day 3의 재료가 됩니다. [클릭] 구조 캔버스는 Multi-Agent 협업 구조의 입력이 되고, [클릭] Validation 정책표는 사람 승인과 안전장치 설계의 기준선이 되고, [클릭] 리팩토링 경계 문서는 Supervisor와 Subgraph 확장의 출발점이 됩니다. [클릭] 그러니 오늘 문서와 로그를 대충 넘기지 마세요. 내일 바로 다시 꺼내 씁니다.

[Q&A 대비]
Q: Day 3에서는 오늘 만든 코드를 그대로 쓰나요?
A: 네. 적어도 구조와 검증 정책은 그대로 재사용합니다.

Q: 오늘 통합 프로토타입이 거칠어도 괜찮나요?
A: 괜찮습니다. 다만 경계와 규칙과 parity 근거는 남겨야 합니다.

전환: 마지막으로 Day 2 마무리 안내를 드리겠습니다.
시간: 2분
-->

---
layout: end
transition: fade
---

# Day 2 수고하셨습니다

**오늘 바로 확인할 것**

- 구조 캔버스와 분기표 저장
- Tool Guard audit 로그 보관
- parity 결과 캡처 또는 기록

<div v-motion :initial="{ y: 18, opacity: 0 }" :enter="{ y: 0, opacity: 1 }" class="absolute bottom-10 left-0 right-0 text-center text-sm opacity-50">
AI Agent 개발 실무 과정 · Day 2
</div>

<!--
[스크립트]
오늘도 수고 많으셨습니다. Day 2는 설명을 듣는 날이 아니라 구조를 고정하고, 제어 흐름을 만들고, Tool 호출을 통제하고, 리팩토링 결과를 검증하는 날이었습니다. 수업이 끝나기 전에 구조 캔버스와 분기표를 저장하고, Tool Guard audit 로그를 보관하고, parity 결과를 캡처해두세요. 이 세 가지가 내일 아침 다시 출발하는 기준선이 됩니다.

[Q&A 대비]
Q: 오늘 결과물을 어디까지 정리해야 하나요?
A: README, 코드, 로그 세 층으로 남기면 가장 좋습니다. 최소한 README와 핵심 실행 결과는 남겨두세요.

Q: 내일 다시 처음부터 세팅하나요?
A: 아닙니다. 오늘 만든 구조와 코드 위에서 확장합니다. 그래서 정리가 중요합니다.

시간: 1분
-->
