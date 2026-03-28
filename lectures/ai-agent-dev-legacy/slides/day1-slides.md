---
theme: default
title: 'Day 1 — Agent 문제 정의 & LLM 설계 전략'
titleTemplate: '%s | AI Agent 전문 개발'
info: |
  AI Agent 전문 개발 과정 Day 1
  대상: AI 개발자, 데이터 엔지니어, 기술 리더
drawings:
  persist: false
transition: slide-left
mdc: true
css: style.css
canvasWidth: 980
aspectRatio: 16/9
---

# AI Agent 전문 개발 과정

## Day 1 — Agent 문제 정의 & LLM 설계 전략

<div class="mt-8 text-gray-500">
대상: AI 개발자 · 데이터 엔지니어 · 기술 리더
</div>

<!--
[스크립트]
안녕하세요. AI Agent 전문 개발 과정 Day 1을 시작하겠습니다.
오늘은 Agent를 만들기 전에 반드시 알아야 할 기초를 다룹니다.
코드보다 "왜"와 "어떻게"에 집중하는 하루입니다.

[Q&A 대비]
"오늘 코드를 많이 짜나요?" — 개념과 설계 위주지만 실습 코드도 있습니다.

전환: 오늘 하루 전체 일정을 먼저 보겠습니다.
시간: 2분
-->

---
transition: fade
layout: default
---

# 오늘의 일정

<v-clicks>

- **Session 1 (09:00–11:00)** — Agent 문제 정의와 과제 도출
- **Session 2 (11:00–13:00)** — LLM 동작 원리 및 프롬프트 전략
- **점심 (13:00–14:00)**
- **Session 3 (14:00–16:00)** — Agent 기획서 구조화
- **Session 4 (16:00–18:00)** — MCP · RAG · Hybrid 구조 판단

</v-clicks>

<v-click>

<div class="box-blue mt-6">
강의 30% · 실습 70% — 모든 실습은 I DO → WE DO → YOU DO
</div>

</v-click>

<!--
[스크립트]
[click] Session 1에서는 Agent가 적합한 문제와 그렇지 않은 문제를 구분합니다.
[click] Session 2는 LLM의 내부 동작과 프롬프트 전략을 다룹니다.
[click] 점심 후
[click] Session 3에서 Agent 기획서를 직접 작성해봅니다.
[click] Session 4는 MCP, RAG, Hybrid 구조를 언제 어떻게 선택하는지 배웁니다.
[click] 실습 비율이 70%입니다. 오늘 배운 내용을 바로 적용해볼 수 있습니다.

전환: Session 1을 시작합니다.
시간: 2분
-->

---
transition: fade
layout: section
---

# Session 1

## Agent 문제 정의와 과제 도출

<!--
[스크립트]
첫 번째 세션입니다. Agent를 만들기 전 가장 중요한 단계, 문제 정의입니다.

전환: Agent가 모든 문제의 해답이 아닙니다.
시간: 30초
-->

---
transition: slide-left
---

# Agent가 실패하는 가장 큰 이유

<v-click>

<div class="box-red text-xl mt-6">
"왜 Agent가 필요한지" 정의하지 않고 시작하기 때문이다
</div>

</v-click>

<v-clicks>

- 기술에서 시작 → 문제를 기술에 끼워 맞춤
- 성공 기준 없음 → "잘 되는 것 같다"로 마무리
- 실패 케이스 미정의 → 런타임에 놀라게 됨

</v-clicks>

<!--
[스크립트]
Agent 프로젝트 실패 원인의 80%가 기술이 아니라 문제 정의에 있습니다.
[click] "Claude API로 뭔가 만들어보자"에서 시작하면 이렇게 됩니다.
[click] 기술에서 시작하면 문제를 기술에 맞추게 됩니다.
[click] 성공 기준이 없으면 언제 완성인지 알 수 없습니다.
[click] 실패 케이스를 미리 정의하지 않으면 운영 중에 당황합니다.

전환: 그렇다면 Agent에 적합한 문제는 무엇인가?
시간: 3분
-->

---
transition: slide-left
---

# Agent에 적합한 문제

<v-clicks>

- **다단계 추론** — 여러 단계를 순차적으로 처리
- **도구 사용** — 외부 API, DB, 파일 시스템 접근
- **비결정적 흐름** — 상황에 따라 다음 단계가 달라짐
- **반복 자동화** — 사람이 하면 지루하고 느린 작업

</v-clicks>

<v-click>

<div class="mt-4 grid grid-cols-2 gap-4">
<div class="col-left">

**Agent가 과잉인 경우**
- 단순 Q&A → 챗봇 or RAG
- 고정 템플릿 → 프롬프트
- 단일 API 호출 → 직접 호출

</div>
<div class="col-right">

**Agent가 필요한 경우**
- 이슈 분류 + 담당자 지정 + 알림
- 데이터 수집 + 분석 + 보고서
- 조건별 분기 + 예외 처리

</div>
</div>

</v-click>

<!--
[스크립트]
[click] 다단계 추론이 필요한 경우입니다. 한 번의 LLM 호출로 끝나지 않습니다.
[click] 외부 시스템과 상호작용이 필요한 경우입니다.
[click] 상황에 따라 다음 행동이 달라지는 경우입니다.
[click] 반복 작업을 자동화하는 경우입니다.
[click] 왼쪽은 Agent가 과잉인 경우, 오른쪽은 진짜 Agent가 필요한 경우입니다.
단순한 작업에 Agent를 적용하면 복잡도만 높아집니다.

전환: Pain → Task → Skill → Tool 프레임워크를 소개합니다.
시간: 5분
-->

---
transition: slide-left
---

# Pain → Task → Skill → Tool

<div class="text-center mt-4">

```
Pain (고통)  →  Task (과제)  →  Skill (능력)  →  Tool (도구)
```

</div>

<v-click>

**예시: 주간 보고서 작성이 너무 오래 걸린다**

</v-click>

<v-clicks>

| 단계 | 내용 |
|------|------|
| Pain | 매주 3시간을 보고서 수동 작성에 낭비 |
| Task | 여러 시스템 데이터를 모아 요약 보고서 생성 |
| Skill | 데이터 수집, 수치 해석, 문서 작성, 발송 |
| Tool | Jira API, DB 쿼리, LLM 요약, 슬랙 발송 |

</v-clicks>

<!--
[스크립트]
Agent 설계의 출발점은 항상 Pain입니다. 기술이 아닙니다.
[click] 예시를 보겠습니다. 주간 보고서 작성이 너무 오래 걸린다는 Pain이 있습니다.
[click] Pain에서 Task로: 여러 시스템 데이터를 모아 요약 보고서를 생성하는 것이 과제입니다.
[click] Task에서 Skill로: 어떤 능력이 필요한지 나열합니다.
[click] Skill에서 Tool로: 각 능력을 어떤 도구로 구현할지 결정합니다.
Pain → Task → Skill → Tool 순서로 내려가야 합니다. 반대 방향은 안 됩니다.

전환: 업무 유형별로 Agent 패턴이 다릅니다.
시간: 5분
-->

---
transition: slide-left
---

# Agent 3가지 패턴

<div class="grid grid-cols-3 gap-4 mt-4">

<v-click>

<div class="box-blue">

**자동화형**
- 트리거 → 처리 → 저장
- 흐름이 고정됨
- 예: 일간 보고서 발송

</div>

</v-click>

<v-click>

<div class="box-yellow">

**분석형**
- 질문 → 탐색 → 설명
- 데이터 소스 다양
- 예: 이탈 고객 분석

</div>

</v-click>

<v-click>

<div class="box-red">

**Planner형**
- 목표 → 계획 → 실행
- 흐름이 동적
- 예: 경쟁사 분석 보고서

</div>

</v-click>

</div>

<v-click>

<div class="box-green mt-6">
난이도: 자동화형 &lt; 분석형 &lt; Planner형 · 비용도 동일 순서
</div>

</v-click>

<!--
[스크립트]
[click] 자동화형은 정해진 프로세스를 반복 실행합니다. 가장 단순하고 비용도 낮습니다.
[click] 분석형은 데이터를 탐색하고 인사이트를 도출합니다. 질문에 따라 탐색 범위가 달라집니다.
[click] Planner형은 목표를 받아 스스로 계획을 세우고 실행합니다. 가장 복잡합니다.
[click] 처음 Agent를 만든다면 자동화형부터 시작하는 것을 권장합니다.

전환: RAG와 Agent를 언제 선택해야 할까요?
시간: 5분
-->

---
transition: slide-left
---

# RAG vs Agent 판단 기준

<div class="grid grid-cols-2 gap-6 mt-4">

<div class="col-left">

**RAG 선택**
- 단순히 "찾아서 대답"하면 됨
- 문서 기반 지식만 필요
- 외부 시스템 조작 불필요
- 예: 사내 문서 Q&A

</div>

<div class="col-right">

**Agent 선택**
- 외부 시스템과 상호작용 필요
- 결과 보고 다음 행동이 달라짐
- 여러 단계 처리 필요
- 예: 이슈 자동 처리

</div>

</div>

<v-click>

<div class="box-blue mt-6">
RAG와 Agent는 배타적이지 않다. Agent가 RAG를 도구로 사용하는 Hybrid도 많다.
</div>

</v-click>

<!--
[스크립트]
가장 많이 받는 질문 중 하나입니다. RAG로 할까, Agent로 할까?
왼쪽이 RAG가 적합한 경우, 오른쪽이 Agent가 필요한 경우입니다.
[click] 중요한 점은 둘이 배타적이지 않다는 것입니다.
실무에서는 Agent가 RAG를 하나의 도구로 사용하는 구조가 흔합니다.

전환: 퀴즈를 풀어보겠습니다.
시간: 5분
-->

---
transition: slide-left
---

# 퀴즈: Agent 적합성 판단

<div class="text-center text-lg mt-4 mb-6">
다음 중 AI Agent 적용이 가장 적합한 시나리오는?
</div>

<div class="relative">

<div class="grid grid-cols-2 gap-4">

<div class="bg-gray-100 rounded p-4">A) 사내 FAQ 문서에서 답변 찾기</div>
<div class="bg-gray-100 rounded p-4">B) 고정 HTML 템플릿에 데이터 채우기</div>
<div class="bg-gray-100 rounded p-4">C) 이슈 분석 + 담당자 지정 + 알림 발송</div>
<div class="bg-gray-100 rounded p-4">D) 텍스트를 영어에서 한국어로 번역</div>

</div>

<v-click-hide>
<div class="absolute inset-0 bg-white/0"></div>
</v-click-hide>

<v-click>
<div class="quiz-answer mt-4">
정답: <strong>C</strong> — 다단계 처리 + 외부 시스템 조작 + 비결정적 흐름
</div>
</v-click>

</div>

<!--
[스크립트]
잠시 생각해보세요.
[click] 정답은 C입니다.
A는 RAG가 적합하고, B는 템플릿 엔진으로 충분합니다.
D는 단순 LLM 호출로 됩니다.
C는 이슈 분석, 담당자 DB 조회, 알림 발송 — 세 가지 다른 시스템이 필요합니다.

전환: Session 1 실습을 시작합니다.
시간: 3분
-->

---
transition: fade
layout: section
---

# Session 1 실습

## I DO → WE DO → YOU DO

<!--
전환: 강사 시연부터 시작합니다.
시간: 30초
-->

---
transition: slide-left
---

# 실습: Agent 후보 도출

<v-clicks>

- **I DO (15분)**: 강사가 실제 업무를 Pain → Tool로 분해
- **WE DO (20분)**: 수강생이 자신의 업무 1개를 함께 분해
- **YOU DO (25분)**: 개인 업무 기반 Agent 후보 2개 도출

</v-clicks>

<v-click>

<div class="box-blue mt-6">

**YOU DO 제출물**
- Agent 후보 2개의 Pain → Task → Skill → Tool
- 각각의 패턴 분류 (자동화형/분석형/Planner형)
- RAG vs Agent 선택 이유

</div>

</v-click>

<!--
[스크립트]
[click] 강사가 먼저 실제 업무를 분석해서 보여드립니다.
[click] 그다음 함께 수강생 업무를 분석합니다.
[click] 마지막으로 스스로 Agent 후보 2개를 도출합니다.
[click] 제출물은 이 세 가지입니다. 서식은 자유입니다.

전환: Session 2로 넘어갑니다.
시간: 1분
-->

---
transition: fade
layout: section
---

# Session 2

## LLM 동작 원리 및 프롬프트 전략 심화

<!--
[스크립트]
Session 2입니다. LLM이 어떻게 작동하는지 이해하면 Agent 동작을 예측할 수 있습니다.

전환: Token과 Context Window부터 시작합니다.
시간: 30초
-->

---
transition: slide-left
---

# Token과 Context Window

<v-clicks>

- **Token**: LLM이 처리하는 최소 단위 (단어·글자 조각)
- **한국어**는 영어보다 토큰 효율이 낮음
- **Context Window**: 한 번에 처리 가능한 최대 토큰 수

</v-clicks>

<v-click>

```
Context Window 구성:
├── System Prompt     : 500 토큰
├── 대화 이력         : 2,000 토큰
├── 현재 사용자 입력  : 300 토큰
└── 출력 (Max Tokens) : 1,000 토큰
    = 총 3,800 토큰 사용
```

</v-click>

<v-click>

<div class="box-red">
Context 초과 시: 앞부분이 잘리거나 에러 발생 → RAG 검색 결과도 포함됨에 주의
</div>

</v-click>

<!--
[스크립트]
[click] Token은 LLM이 처리하는 최소 단위입니다.
[click] 한국어는 같은 의미를 영어보다 더 많은 토큰으로 표현합니다.
[click] Context Window는 한 번에 처리할 수 있는 총 토큰 수입니다.
[click] System Prompt부터 출력까지 모두 합산됩니다.
[click] 초과하면 앞 내용이 잘려나갑니다. RAG 검색 결과도 Context를 소모합니다.

전환: Hallucination이란 무엇이고 어떻게 줄일 수 있을까요?
시간: 5분
-->

---
transition: slide-left
---

# Hallucination 이해

<v-click>

<div class="box-red">
<strong>Hallucination</strong>: LLM이 사실이 아닌 내용을 자신감 있게 생성하는 현상
</div>

</v-click>

<v-clicks>

**자주 발생하는 상황**
- 학습 데이터 이후의 최신 정보 요청
- 구체적 수치, 날짜, 인용 요청
- 너무 열린 질문 (제약 없음)
- 모델이 잘 모르는 도메인 세부사항

</v-clicks>

<v-click>

<!-- IMAGE: LLM이 자신있게 틀린 정보를 말하는 AI 로봇 일러스트. 검색 키워드: "AI hallucination confident wrong answer illustration" -->

</v-click>

<!--
[스크립트]
[click] Hallucination은 모델의 구조적 한계입니다. 완전히 없앨 수는 없습니다.
[click] 최신 정보를 물어보면 학습 당시의 정보를 "현재"인 것처럼 답합니다.
[click] 구체적 수치를 요청하면 그럴듯한 숫자를 만들어냅니다.
[click] 제약이 없으면 창의적으로 만들어냅니다.
[click] 도메인 전문 지식은 표면만 알고 깊이가 없는 경우가 많습니다.

전환: Hallucination 완화 전략을 보겠습니다.
시간: 4분
-->

---
transition: slide-left
---

# Hallucination 완화 전략

<div class="grid grid-cols-2 gap-4 mt-4">

<v-click>

<div class="box-blue">

**RAG 결합**
관련 문서를 Context에 포함
"제공된 문서만 근거로 사용하라"

</div>

</v-click>

<v-click>

<div class="box-green">

**불확실성 명시**
System Prompt에 추가:
"모르면 모른다고 답하라"

</div>

</v-click>

<v-click>

<div class="box-yellow">

**Structured Output**
JSON Schema로 응답 범위 제한
임의 생성 공간 축소

</div>

</v-click>

</div>

<v-click>

<div class="box-red mt-4">
Agent 설계 원칙: "LLM이 틀릴 수 있다"는 전제로 검증 로직을 항상 포함하라
</div>

</v-click>

<!--
[스크립트]
[click] RAG를 결합하면 모델이 실제 문서를 근거로 답변합니다.
[click] System Prompt에 불확실성을 인정하도록 지시하면 모르는 것을 꾸며내지 않습니다.
[click] Structured Output으로 응답 형식을 제한하면 임의 생성 공간이 줄어듭니다.
[click] 가장 중요한 원칙입니다. LLM이 틀릴 수 있다는 전제로 설계해야 합니다.

전환: 프롬프트 전략 세 가지를 비교합니다.
시간: 4분
-->

---
transition: slide-left
---

# 프롬프트 전략: Zero-shot

<v-click>

지시만 제공하고 예시 없이 수행을 요청한다.

</v-click>

<v-click>

```python
prompt = """
다음 고객 리뷰를 긍정/부정/중립으로 분류하라.
리뷰: "배송이 빠르긴 했는데 포장이 엉망이었어요."
"""
```

</v-click>

<v-click>

<div class="grid grid-cols-2 gap-4 mt-4">
<div class="box-green">
장점: 프롬프트 짧음 · 토큰 효율 좋음
</div>
<div class="box-red">
단점: 복잡한 작업에서 품질 저하
</div>
</div>

</v-click>

<v-click>

<div class="box-blue mt-2">
적합: 단순 분류, 번역, 요약
</div>

</v-click>

<!--
[스크립트]
[click] Zero-shot은 가장 단순한 전략입니다. 예시 없이 지시만 합니다.
[click] 코드를 보면 매우 짧습니다.
[click] 짧고 효율적이지만 복잡한 작업에서 품질이 불안정합니다.
[click] 단순한 작업에 먼저 시도해보세요.

전환: Few-shot을 보겠습니다.
시간: 4분
-->

---
transition: slide-left
---

# 프롬프트 전략: Few-shot

<v-click>

작업 방식을 예시(shot)로 보여준다.

</v-click>

<v-click>

```python
prompt = """
리뷰: "정말 좋아요!" → 긍정
리뷰: "완전 실망입니다." → 부정
리뷰: "그냥 평범해요." → 중립

리뷰: "배송이 빠르긴 했는데 포장이 엉망이었어요." →
"""
```

</v-click>

<v-click>

<div class="grid grid-cols-2 gap-4 mt-4">
<div class="box-green">
장점: 출력 형식·품질 안정적
</div>
<div class="box-red">
단점: 토큰 사용량 증가
</div>
</div>

</v-click>

<!--
[스크립트]
[click] Few-shot은 예시를 보여주는 방식입니다.
[click] 긍정·부정·중립 예시를 먼저 보여주면 LLM이 형식을 이해합니다.
[click] 출력이 더 일관적이지만 토큰을 더 사용합니다.
출력 형식이 중요하거나 도메인 특화 작업에 적합합니다.

전환: Chain-of-Thought를 보겠습니다.
시간: 4분
-->

---
transition: slide-left
---

# 프롬프트 전략: Chain-of-Thought

<v-click>

단계적 추론 과정을 포함하도록 유도한다.

</v-click>

<v-click>

```python
# 마법의 한 문장
prompt = """
보험 청구서를 분석하여 유효성을 판단하라.

단계적으로 생각해보자.
"""
```

</v-click>

<v-click>

<div class="grid grid-cols-2 gap-4 mt-4">
<div class="box-green">
장점: 복잡한 추론 정확도 대폭 향상
</div>
<div class="box-red">
단점: 출력 토큰 증가 → 비용·지연 상승
</div>
</div>

</v-click>

<v-click>

<div class="box-blue mt-2">
적합: 수학 문제, 논리 추론, 복잡한 판단
</div>

</v-click>

<!--
[스크립트]
[click] Chain-of-Thought는 단계적 추론을 유도합니다.
[click] "단계적으로 생각해보자"라는 한 문장이 정확도를 크게 높입니다.
[click] 복잡한 추론 정확도가 높아지지만 응답이 길어집니다.
[click] 수학 계산이나 복잡한 판단이 필요한 경우에 사용합니다.

전환: 세 전략을 비교합니다.
시간: 4분
-->

---
transition: slide-left
---

# 프롬프트 전략 비교

| 전략 | 토큰 | 정확도 | 속도 | 적합 상황 |
|------|------|--------|------|-----------|
| Zero-shot | 낮음 | 보통 | 빠름 | 단순 작업 |
| Few-shot | 중간 | 높음 | 중간 | 형식 중요 |
| CoT | 높음 | 높음 | 느림 | 복잡 추론 |
| CoT + Few-shot | 매우 높음 | 매우 높음 | 느림 | 고정확도 |

<v-click>

<div class="box-blue mt-4">

**선택 가이드**
- 비용 제약 → Zero-shot 먼저 시도
- 형식 중요 → Few-shot
- 추론 필요 → CoT
- 고정확도 + 형식 → CoT + Few-shot

</div>

</v-click>

<!--
[스크립트]
표로 정리하면 이렇습니다.
[click] 선택 기준은 간단합니다. 비용이 중요하면 Zero-shot부터, 형식이 중요하면 Few-shot, 추론이 필요하면 CoT입니다.
실무에서는 Zero-shot으로 시작해서 품질이 부족하면 Few-shot, 그래도 부족하면 CoT로 올라갑니다.

전환: Structured Output을 보겠습니다.
시간: 4분
-->

---
transition: slide-left
---

# Structured Output

<v-click>

<div class="box-blue">
Agent에서 LLM 출력은 다음 로직의 <strong>입력</strong>이 된다.<br>
자연어 파싱은 불안정하다 → JSON Schema로 형식을 강제하라.
</div>

</v-click>

<v-click>

```python
# Tool Use 방식 (가장 안정적)
tools = [{
    "name": "classify_review",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "enum": ["긍정", "부정", "중립"]},
            "confidence": {"type": "number"},
            "reason": {"type": "string"}
        },
        "required": ["category", "confidence", "reason"]
    }
}]
```

</v-click>

<v-click>

<div class="box-green mt-2">
Tool Use로 강제하면 스키마 위반 응답이 거의 없다
</div>

</v-click>

<!--
[스크립트]
[click] Agent에서 LLM 출력은 보통 다음 단계의 입력으로 사용됩니다.
자연어로 받으면 파싱이 불안정합니다.
[click] Tool Use를 사용하면 LLM이 반드시 지정한 JSON Schema 형식으로 응답합니다.
[click] Tool Use 방식이 일반 프롬프트보다 훨씬 안정적입니다.

전환: 비용 최적화를 봅니다.
시간: 4분
-->

---
transition: slide-left
---

# 비용·Latency 최적화

<v-clicks>

- **1순위**: 모델 선택 — 작업에 맞는 모델 사용
- **2순위**: 출력 길이 제한 — max_tokens 적절히 설정
- **3순위**: 입력 압축 — 불필요한 Context 제거
- **4순위**: 캐싱 활용 — 반복 System Prompt 캐시

</v-clicks>

<v-click>

<div class="grid grid-cols-2 gap-4 mt-4">
<div class="col-left">

**Latency 단축**
- 병렬 API 호출
- 스트리밍 응답
- 작은 모델 우선

</div>
<div class="col-right">

**비용 공식**
```
비용 = 입력토큰 × 단가
     + 출력토큰 × 단가
(출력 단가 > 입력 단가)
```

</div>
</div>

</v-click>

<!--
[스크립트]
[click] 가장 효과적인 비용 절감은 모델 선택입니다. 단순 분류에 최고 성능 모델은 낭비입니다.
[click] 출력 길이를 제한하세요. CoT는 예상보다 길어질 수 있습니다.
[click] 불필요한 Context를 제거하세요. 매 호출마다 토큰이 소비됩니다.
[click] 반복되는 System Prompt는 캐싱으로 비용을 줄일 수 있습니다.
[click] Latency는 병렬 호출과 스트리밍으로 체감 속도를 높일 수 있습니다.

전환: Session 2 실습입니다.
시간: 4분
-->

---
transition: slide-left
---

# 퀴즈: 프롬프트 전략 선택

<div class="text-center text-lg mt-4 mb-6">
보험 청구서 유효성 판단 — 단계별 근거 설명 필요, 실수 허용 낮음<br>
어떤 전략이 가장 적합한가?
</div>

<div class="relative">

<div class="grid grid-cols-2 gap-4">
<div class="bg-gray-100 rounded p-4">A) Zero-shot</div>
<div class="bg-gray-100 rounded p-4">B) Few-shot</div>
<div class="bg-gray-100 rounded p-4">C) CoT + Few-shot</div>
<div class="bg-gray-100 rounded p-4">D) 단순 LLM 호출</div>
</div>

<v-click-hide>
<div class="absolute inset-0 bg-white/0"></div>
</v-click-hide>

<v-click>
<div class="quiz-answer mt-4">
정답: <strong>C</strong> — 단계별 추론(CoT) + 일관된 형식(Few-shot) 조합
</div>
</v-click>

</div>

<!--
[스크립트]
생각해보세요.
[click] 정답은 C입니다. 단계별 근거가 필요하면 CoT, 형식이 일관돼야 하면 Few-shot입니다.
실수 허용이 낮은 도메인에서는 두 전략을 조합합니다.

전환: Session 2 실습입니다.
시간: 2분
-->

---
transition: fade
layout: section
---

# Session 2 실습

## 프롬프트 전략별 응답 비교

<!--
전환: 코드로 직접 비교합니다.
시간: 30초
-->

---
transition: slide-left
---

# 실습: 전략 비교 코드

<v-clicks>

- **I DO (15분)**: 강사가 Zero/Few/CoT를 같은 태스크로 비교
- **WE DO (20분)**: Structured Output (Tool Use) 함께 구현
- **YOU DO (25분)**: 자신의 태스크에 세 전략 적용 + 토큰·지연 비교

</v-clicks>

<v-click>

<div class="box-blue mt-6">

**YOU DO 제출물** (`labs/prompt-strategy-comparison/src/`)
- 동일 태스크에 3가지 전략 코드
- 토큰 수 · 지연 · 품질 비교 결과
- Structured Output (JSON) 구현

</div>

</v-click>

<!--
[스크립트]
[click] 강사가 먼저 같은 태스크에 세 전략을 모두 적용합니다.
[click] 함께 Structured Output을 구현합니다.
[click] 스스로 자신의 태스크에 세 전략을 적용하고 결과를 비교합니다.
[click] 제출물은 코드와 비교 결과입니다.

전환: 점심 후 Session 3으로 넘어갑니다.
시간: 1분
-->

---
transition: fade
layout: section
---

# Session 3

## Agent 기획서 구조화

<!--
[스크립트]
Session 3입니다. 점심 먹고 오셨나요? Agent 기획서를 실제로 작성해봅니다.

전환: 기획 없는 Agent는 방향 없는 자동화입니다.
시간: 30초
-->

---
transition: slide-left
---

# 기획서가 필요한 이유

<v-clicks>

- 개발자: 개발 범위 명확화
- QA: 테스트 케이스 도출
- 운영자: 모니터링 포인트 파악
- 팀 전체: 커뮤니케이션 도구

</v-clicks>

<v-click>

<div class="box-red mt-4">
"어디서 시작해서 어디서 끝나는지" 모르면<br>
테스트도 못하고 예외 처리도 할 수 없다
</div>

</v-click>

<!--
[스크립트]
[click] 개발자는 기획서로 개발 범위를 명확히 합니다.
[click] QA는 기획서의 IPO에서 테스트 케이스를 도출합니다.
[click] 운영자는 어디를 모니터링해야 하는지 알 수 있습니다.
[click] 팀 전체의 커뮤니케이션 도구가 됩니다.
[click] 가장 큰 이유입니다. 경계가 없으면 아무것도 할 수 없습니다.

전환: Task를 Sub-task로 분해하는 방법입니다.
시간: 3분
-->

---
transition: slide-left
---

# Task → Sub-task 분해 원칙

<v-clicks>

- 하나의 Sub-task = 하나의 책임
- 독립적으로 테스트 가능해야 함
- Sub-task 출력 = 다음 Sub-task 입력

</v-clicks>

<v-click>

```
주간 보고서 Agent:
ST-1: 데이터 수집 (Jira API, DB 쿼리)
  ↓
ST-2: 데이터 정제 (원시 → 표준 포맷)
  ↓
ST-3: 요약 생성 (LLM)
  ↓
ST-4: 배포 (슬랙, 이메일)
```

</v-click>

<!--
[스크립트]
[click] 하나의 Sub-task는 하나의 책임만 가집니다.
[click] 독립적으로 테스트할 수 있어야 합니다.
[click] Sub-task 출력이 다음 Sub-task 입력이 됩니다. 이 연결이 Workflow입니다.
[click] 주간 보고서 Agent를 4개 Sub-task로 분해한 예시입니다.
각 단계가 명확하고 독립적입니다.

전환: Stateless vs Stateful을 보겠습니다.
시간: 5분
-->

---
transition: slide-left
---

# Stateless vs Stateful

<div class="grid grid-cols-2 gap-6 mt-4">

<div class="col-left">

**Stateless**
- 각 호출이 독립적
- 이전 실행을 기억 안 함
- 수평 확장 쉬움
- 재시도 안전
- 예: 티켓 분류, 번역

</div>

<div class="col-right">

**Stateful**
- 이전 실행 결과 기억
- 단계적 처리 가능
- 대화형 상호작용 지원
- 체크포인트 필요
- 예: 리서치 Agent

</div>

</div>

<v-click>

<div class="box-blue mt-4">

**선택 기준**: 이전 결과가 다음 실행에 필요한가?<br>
→ Yes: Stateful &nbsp;&nbsp;&nbsp; No: Stateless

</div>

</v-click>

<!--
[스크립트]
왼쪽이 Stateless, 오른쪽이 Stateful입니다.
[click] 핵심 질문은 하나입니다. 이전 실행 결과가 다음에 필요한가?
필요하면 Stateful, 아니면 Stateless로 시작하세요.
Stateless가 더 단순하고 확장성이 좋습니다.

전환: IPO 명세 작성을 보겠습니다.
시간: 5분
-->

---
transition: slide-left
---

# Input–Process–Output 명세

<v-click>

모든 Sub-task는 I/O가 명확해야 한다.

</v-click>

<v-click>

```python
@dataclass
class TicketInput:
    ticket_id: str
    content: str
    priority: Literal["low", "medium", "high"] = "medium"

@dataclass
class TicketOutput:
    category: Literal["bug", "feature", "question", "unclassified"]
    severity: int   # 1-5
    assignee: str
    confidence: float  # 0.0-1.0
```

</v-click>

<v-click>

<div class="box-yellow mt-2">
Python dataclass나 Pydantic으로 명시하면 오류를 조기에 발견한다
</div>

</v-click>

<!--
[스크립트]
[click] 모든 Sub-task는 입출력이 명확해야 합니다. 명확하지 않으면 테스트할 수 없습니다.
[click] Python dataclass를 사용하면 입출력 타입을 코드로 명시할 수 있습니다.
[click] 타입이 명시되면 Sub-task 간 연결에서 타입 불일치 오류를 조기에 발견합니다.

전환: 실패 처리 전략을 봅니다.
시간: 4분
-->

---
transition: slide-left
---

# 예외 처리 전략

<v-clicks>

- **AUTO_RETRY** — 네트워크 오류, 타임아웃 → 자동 재시도
- **FALLBACK** — LLM 파싱 실패 → 기본값 사용
- **NOTIFY** — 비정상 데이터 → 알림 발송
- **HUMAN_REVIEW** — 비즈니스 오류 → 사람 검토
- **HALT** — 데이터 손상 → 전체 중단

</v-clicks>

<v-click>

<div class="box-red mt-4">
"외부 API 실패 · 데이터 오류 · LLM 응답 오류" — 이 세 범주만 커버해도 80%를 처리한다
</div>

</v-click>

<!--
[스크립트]
[click] 네트워크 오류는 자동으로 재시도합니다.
[click] LLM 파싱 실패는 기본값으로 대체합니다.
[click] 비정상 데이터는 알림을 발송합니다.
[click] 비즈니스 로직 오류는 사람이 검토해야 합니다.
[click] 데이터 손상은 전체를 멈춰야 합니다.
[click] 이 세 가지만 잘 처리해도 대부분의 실패를 커버합니다.

전환: 퀴즈입니다.
시간: 4분
-->

---
transition: slide-left
---

# 퀴즈: Workflow 순서 오류

<div class="text-lg mt-4 mb-4">
다음 Workflow에서 문제점은?
</div>

<v-click>

```
ST-1: 보고서 생성 (LLM 요약)
ST-2: 데이터 수집 (DB 쿼리)
Workflow: ST-1 → ST-2
```

</v-click>

<v-click>

<div class="quiz-answer mt-4">
<strong>순서 오류</strong>: ST-1은 ST-2의 결과물이 필요하다.<br>
올바른 순서: ST-2(데이터 수집) → ST-1(보고서 생성)
</div>

</v-click>

<!--
[스크립트]
[click] 이 Workflow를 보면 문제가 보이시나요?
[click] ST-1 보고서 생성은 데이터가 있어야 가능합니다. 그런데 데이터 수집이 ST-2입니다.
Sub-task 간 의존 관계를 항상 먼저 확인하고 순서를 정의해야 합니다.

전환: Session 3 실습입니다.
시간: 2분
-->

---
transition: fade
layout: section
---

# Session 3 실습

## Agent 구조 다이어그램 설계

<!--
전환: 기획서를 실제로 작성합니다.
시간: 30초
-->

---
transition: slide-left
---

# 실습: 기획서 작성

<v-clicks>

- **I DO (15분)**: Session 1 Agent 후보를 기획서로 구조화
- **WE DO (20분)**: Sub-task 3-5개로 분해, IPO 1개 완성
- **YOU DO (25분)**: 전체 기획서 + Workflow 다이어그램 완성

</v-clicks>

<v-click>

<div class="box-blue mt-6">

**YOU DO 제출물** (`labs/agent-problem-definition/artifacts/`)
- Workflow 다이어그램 (텍스트 또는 mermaid)
- 모든 Sub-task IPO 명세
- Stateless/Stateful 선택 이유
- 실패 케이스 3개 이상

</div>

</v-click>

<!--
[스크립트]
[click] 강사가 Session 1의 Agent 후보를 기획서로 만드는 것을 보여드립니다.
[click] 함께 Sub-task를 분해하고 IPO를 작성합니다.
[click] 스스로 전체 기획서를 완성합니다.
[click] 제출물은 다이어그램과 IPO 명세입니다.

전환: Session 4로 넘어갑니다.
시간: 1분
-->

---
transition: fade
layout: section
---

# Session 4

## MCP · RAG · Hybrid 구조 판단

<!--
[스크립트]
마지막 Session입니다. 오늘 배운 내용을 바탕으로 구조를 결정하는 방법을 배웁니다.

전환: MCP(Function Calling)부터 시작합니다.
시간: 30초
-->

---
transition: slide-left
---

# MCP (Function Calling) 이해

<v-click>

<div class="box-blue">
LLM이 직접 코드를 실행하는 것이 아니라<br>
<strong>"이 Tool을 이 인자로 호출하라"는 명령을 생성</strong>하고<br>
실제 실행은 시스템이 담당한다
</div>

</v-click>

<v-click>

```
사용자 요청 → LLM → Tool 호출 명령 생성
                            ↓
                      실제 Tool 실행
                            ↓
                      결과를 LLM에 전달
                            ↓
                      최종 응답 생성
```

</v-click>

<!--
[스크립트]
[click] MCP에서 중요한 점은 LLM이 직접 코드를 실행하지 않는다는 것입니다.
LLM은 "어떤 Tool을 어떤 인자로 호출할지"를 결정합니다.
[click] 흐름을 보면 LLM이 Tool 호출 명령을 생성하고, 시스템이 실제로 실행한 뒤, 결과를 다시 LLM에 전달합니다.

전환: 좋은 Tool 설계 기준을 봅니다.
시간: 4분
-->

---
transition: slide-left
---

# 좋은 Tool 설계 기준

<v-clicks>

- **단일 책임**: 하나의 Tool = 하나의 명확한 기능
- **명확한 Description**: LLM이 언제 이 Tool을 쓸지 이해
- **명확한 에러 응답**: LLM이 이해하는 에러 메시지

</v-clicks>

<v-click>

```python
# 나쁜 예시
def manage_everything(action: str, data: dict) -> dict:
    """모든 데이터 관리"""  # LLM이 언제 써야 할지 모름

# 좋은 예시
def get_user_by_id(user_id: str) -> dict:
    """사용자 ID로 프로필 정보를 조회한다"""
```

</v-click>

<v-click>

<div class="box-red mt-2">
Tool이 15개를 넘으면 LLM의 선택 정확도가 떨어진다<br>
→ 그룹화하거나 Sub-agent로 분리하라
</div>

</v-click>

<!--
[스크립트]
[click] 하나의 Tool은 하나의 기능만 담당합니다.
[click] Description이 명확해야 LLM이 언제 이 Tool을 쓸지 판단할 수 있습니다.
[click] 에러도 LLM이 이해할 수 있는 메시지로 반환해야 합니다.
[click] 코드를 보면 차이가 명확합니다. manage_everything은 LLM이 이해하기 어렵습니다.
[click] Tool이 너무 많으면 LLM이 올바른 선택을 못합니다. 15개 이하로 유지하세요.

전환: RAG 구조를 봅니다.
시간: 5분
-->

---
transition: slide-left
---

# RAG 구조 흐름

<v-click>

```
[색인 단계]
문서 수집 → 청킹 → 임베딩 → 벡터 DB 저장

[검색 단계]
사용자 질문 → 질문 임베딩 → 유사도 검색
          → 관련 청크 추출 → Context 구성
          → LLM 답변 생성
```

</v-click>

<v-clicks>

- **청킹**: 문서를 적절한 크기로 분할 (500토큰 권장)
- **임베딩**: 텍스트 → 벡터 변환 (같은 모델 유지 필수)
- **유사도 검색**: 질문과 가장 관련 있는 청크 추출
- **chunk_overlap**: 청크 간 겹침으로 문맥 연결

</v-clicks>

<!--
[스크립트]
[click] RAG는 두 단계로 나뉩니다. 색인(인덱싱)과 검색입니다.
[click] 청킹은 문서를 적절한 크기로 나눕니다. 너무 크면 검색 정밀도 저하, 너무 작으면 문맥 손실입니다.
[click] 임베딩은 텍스트를 벡터로 변환합니다. 색인과 검색 시 반드시 같은 모델을 사용해야 합니다.
[click] 유사도 검색으로 질문과 가장 관련 있는 청크를 찾습니다.
[click] chunk_overlap은 청크 간 겹치는 부분으로 문맥이 끊기지 않게 합니다.

전환: 세 구조를 비교합니다.
시간: 5분
-->

---
transition: slide-left
---

# Tool 중심 vs RAG 중심 비교

<div class="grid grid-cols-2 gap-4 mt-4">

<div class="col-left">

**MCP (Tool 중심)**
- 실시간 데이터 지원
- 외부 시스템 조작 가능
- Tool 수에 따라 복잡도 증가
- API 의존성 높음

</div>

<div class="col-right">

**RAG 중심**
- 정적 지식 Q&A에 강함
- 근거 있는 답변 가능
- 실시간 데이터 미지원
- 검색 품질에 의존

</div>

</div>

<v-click>

<div class="box-yellow mt-4">

**판단 질문**
- 실시간 데이터 필요한가? → MCP
- 외부 시스템 조작 필요한가? → MCP
- 정적 문서 기반 Q&A인가? → RAG

</div>

</v-click>

<!--
[스크립트]
왼쪽이 MCP(Tool 중심), 오른쪽이 RAG 중심입니다.
[click] 판단 질문 세 가지입니다. 실시간 데이터가 필요하면 MCP, 외부 시스템 조작이 필요하면 MCP, 정적 문서 Q&A면 RAG입니다.

전환: Hybrid 구조를 봅니다.
시간: 4분
-->

---
transition: slide-left
---

# Hybrid 구조

<v-click>

```
사용자 요청 → LLM: 전략 판단
    ↙                    ↘
RAG 검색              Tool 호출
(정적 문서)          (실시간 데이터)
    ↘                    ↙
         결과 통합
              ↓
         최종 답변
```

</v-click>

<v-click>

<div class="box-red mt-4">
Hybrid는 복잡하고 비싸다.<br>
먼저 "RAG만으로 안 되는가?", "Tool만으로 안 되는가?"를 확인하라.
</div>

</v-click>

<!--
[스크립트]
[click] Hybrid는 RAG와 Tool을 함께 사용합니다. LLM이 상황에 따라 RAG를 쓸지 Tool을 쓸지 판단합니다.
[click] Hybrid를 기본 선택으로 삼지 마세요. 두 구조 모두 필요한 이유가 명확할 때만 선택합니다.

전환: 세 구조 종합 비교입니다.
시간: 3분
-->

---
transition: slide-left
---

# 구조 종합 비교

| 항목 | MCP | RAG | Hybrid |
|------|-----|-----|--------|
| 실시간 데이터 | 지원 | 미지원 | 지원 |
| 외부 조작 | 가능 | 불가 | 가능 |
| 구현 복잡도 | 중간 | 중간 | 높음 |
| 운영 비용 | API 비용 | 임베딩 비용 | 높음 |
| 지식 Q&A | 제한적 | 강함 | 강함 |

<v-click>

<div class="box-blue mt-4">
선택 순서: RAG 검토 → MCP 검토 → Hybrid (최후 수단)
</div>

</v-click>

<!--
[스크립트]
표로 한눈에 비교합니다.
[click] 중요한 원칙입니다. 단순한 구조로 해결되는지 먼저 확인하세요.
Hybrid는 가장 마지막에 선택하는 구조입니다.

전환: 퀴즈입니다.
시간: 3분
-->

---
transition: slide-left
---

# 퀴즈: 구조 선택

<div class="text-center text-lg mt-2 mb-4">
고객 서비스 Agent:<br>
제품 매뉴얼(PDF 500p)에서 답변 + 주문 현황 실시간 조회
</div>

<div class="relative">

<div class="grid grid-cols-2 gap-4">
<div class="bg-gray-100 rounded p-4">A) MCP만 사용</div>
<div class="bg-gray-100 rounded p-4">B) RAG만 사용</div>
<div class="bg-gray-100 rounded p-4">C) Hybrid (RAG + MCP)</div>
<div class="bg-gray-100 rounded p-4">D) 단순 LLM 호출</div>
</div>

<v-click-hide>
<div class="absolute inset-0 bg-white/0"></div>
</v-click-hide>

<v-click>
<div class="quiz-answer mt-4">
정답: <strong>C</strong> — 매뉴얼 검색(RAG) + 주문 조회(MCP Tool) 모두 필요
</div>
</v-click>

</div>

<!--
[스크립트]
생각해보세요.
[click] 정답은 C입니다. 두 가지 다른 정보 소스가 필요합니다.
매뉴얼은 정적 문서이므로 RAG, 주문 현황은 실시간 데이터이므로 MCP Tool이 필요합니다.
이 경우 Hybrid가 불가피합니다.

전환: 마지막 실습입니다.
시간: 2분
-->

---
transition: fade
layout: section
---

# Session 4 실습

## MCP vs RAG 구조 설계 비교

<!--
전환: Day 1 마지막 실습입니다.
시간: 30초
-->

---
transition: slide-left
---

# 실습: 구조 설계 비교

<v-clicks>

- **I DO (15분)**: 두 시나리오에 MCP/RAG/Hybrid 판단 과정 시연
- **WE DO (20분)**: Agent 후보에 구조 선택 + 체크리스트 적용
- **YOU DO (25분)**: 최종 구조 결정 문서 작성

</v-clicks>

<v-click>

<div class="box-blue mt-6">

**YOU DO 제출물** (`labs/agent-problem-definition/artifacts/`)
- 최종 구조 결정 (MCP/RAG/Hybrid)
- 선택 이유 3가지 이상
- 비선택 구조의 단점
- 예상 비용 구조

</div>

</v-click>

<!--
[스크립트]
[click] 강사가 실제 시나리오에 판단 과정을 보여드립니다.
[click] 함께 체크리스트를 적용해 구조를 선택합니다.
[click] 스스로 최종 구조를 결정하고 이유를 작성합니다.
[click] 제출물은 결정 문서입니다.

전환: Day 1 전체를 정리합니다.
시간: 1분
-->

---
transition: fade
---

# Day 1 정리

<v-clicks>

- **Session 1**: Pain → Task → Skill → Tool, Agent 패턴 3가지, RAG vs Agent
- **Session 2**: Token·Context·Hallucination, Zero/Few/CoT, Structured Output, 비용 최적화
- **Session 3**: Sub-task 분해, Stateless/Stateful, IPO 명세, 예외 처리 전략
- **Session 4**: MCP Tool 설계, RAG 구조, Hybrid 선택 기준

</v-clicks>

<v-click>

<div class="box-green mt-6">

**핵심 메시지**
- Agent는 문제에서 시작한다. 기술에서 시작하지 않는다.
- 가장 단순한 구조를 먼저 시도한다.
- 실패 케이스를 설계 단계에서 정의한다.

</div>

</v-click>

<!--
[스크립트]
[click] Session 1에서 문제 정의 프레임워크를 배웠습니다.
[click] Session 2에서 LLM 동작 원리와 프롬프트 전략을 배웠습니다.
[click] Session 3에서 Agent 기획서를 구조화하는 방법을 배웠습니다.
[click] Session 4에서 구조 판단 기준을 배웠습니다.
[click] 오늘의 핵심 메시지입니다. 항상 문제에서 시작하고, 단순하게 시작하고, 실패를 미리 설계하세요.

내일은 이 기반 위에서 실제 Agent를 구현합니다. 수고하셨습니다!
시간: 5분
-->

---
transition: fade
layout: center
---

# Q&A

<div class="text-2xl text-gray-500 mt-6">
오늘 배운 내용 중 궁금한 점을 질문해주세요.
</div>

<div class="mt-8 text-gray-400">
Day 2 예고: Agent 개발 기초 — 실제 코드로 Agent 구현
</div>

<!--
[스크립트]
오늘 하루 수고하셨습니다. 질문 있으시면 지금 해주세요.
내일은 오늘 설계한 기획서를 바탕으로 실제 코드로 Agent를 구현합니다.
오늘 작성한 기획서와 실습 제출물을 꼭 완성해두세요.

시간: 10분 (Q&A)
-->
