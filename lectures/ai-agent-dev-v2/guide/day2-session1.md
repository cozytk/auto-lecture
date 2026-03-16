# Day 2 Session 1: Agent 4요소 구조 설계

> **2시간** | AI 개발자, 데이터 엔지니어, 기술 리더 대상

---

## 왜 중요한가

Agent를 "그냥 LLM + 툴"로 만들면 실패한다.
유지보수가 불가능하고, 버그 위치를 찾을 수 없다.
4요소 구조를 먼저 설계해야 확장 가능한 시스템이 된다.

> **핵심 질문**: "이 Agent가 무엇을 기억하고, 어떻게 판단하며, 무엇을 실행하는가?"

Agent를 잘 설계한다는 것은 **목표-기억-도구-제어**를 명확히 분리하는 것이다.
분리되지 않은 Agent는 한 가지 요구사항 변경에도 전체가 흔들린다.
2026년 현재 프로덕션 Agent 장애의 60% 이상이 제어 흐름 미설계에서 비롯된다.

---

## 핵심 원리

### Agent 4요소

| 요소 | 역할 | 핵심 질문 |
|------|------|-----------|
| **Goal** | 무엇을 달성해야 하는가 | "성공 조건은 무엇인가?" |
| **Memory** | 무엇을 기억하는가 | "어떤 컨텍스트를 유지하는가?" |
| **Tool** | 무엇을 할 수 있는가 | "어떤 외부 능력이 필요한가?" |
| **Control Logic** | 어떻게 판단하는가 | "언제 멈추고, 언제 재시도하는가?" |

### Goal (목표 정의)

Goal은 단순한 task description이 아니다.
**성공 조건(Exit Condition)**과 **실패 조건(Abort Condition)**을 포함한다.
잘못 정의된 Goal은 무한 루프의 주요 원인이다.

```python
# 나쁜 예: 목표가 모호함
goal = "데이터를 분석해"

# 좋은 예: 조건이 명확함
goal = Goal(
    description="판매 데이터에서 이상치를 탐지한다",
    success_condition="이상치 목록과 근거 보고서 생성 완료",
    abort_condition="데이터 접근 실패 또는 3회 재시도 초과",
    max_steps=10
)
```

### Memory (기억 구조)

Memory는 4가지 레이어로 구분한다.

```
┌─────────────────────────────────────┐
│ Episodic Memory  (이번 대화/세션)    │ ← 가장 빠름, 가장 휘발성
├─────────────────────────────────────┤
│ Working Memory   (현재 Task 상태)   │ ← Agent State에 보관
├─────────────────────────────────────┤
│ Semantic Memory  (도메인 지식)      │ ← Vector DB, RAG
├─────────────────────────────────────┤
│ Procedural Memory (실행 패턴)       │ ← 프롬프트, Few-shot
└─────────────────────────────────────┘
```

**Working Memory**가 핵심이다.
Agent State에 무엇을 담을지 결정하는 것이 설계의 핵심이다.
너무 많으면 컨텍스트가 오염되고, 너무 적으면 판단이 틀린다.

### Tool (도구 정의)

Tool은 **원자적(atomic)**이어야 한다.
하나의 Tool은 하나의 명확한 역할만 수행한다.
Tool 간 의존성이 생기면 제어 흐름이 복잡해진다.

```python
# 나쁜 예: Tool이 너무 많은 일을 함
def search_and_summarize(query: str) -> str:
    results = web_search(query)
    summary = llm_summarize(results)
    save_to_db(summary)
    return summary

# 좋은 예: 각 Tool은 하나의 역할
@tool
def web_search(query: str) -> list[SearchResult]: ...

@tool
def summarize_text(text: str) -> str: ...

@tool
def save_result(key: str, value: str) -> bool: ...
```

### Control Logic (제어 논리)

Control Logic은 **언제 무엇을 할지 결정**한다.
Plan → Execute → Observe → Reflect → 반복 구조가 기본이다.
각 단계에서 실패 시 어떻게 처리할지를 미리 정의해야 한다.

```python
class AgentControlLoop:
    def run(self, goal: Goal) -> Result:
        state = AgentState(goal=goal)

        while not state.is_terminal():
            # Plan: 다음 행동 결정
            action = self.planner.plan(state)

            # Execute: 행동 실행
            observation = self.executor.execute(action)

            # Reflect: 결과 평가
            state = self.reflector.update(state, observation)

            # Safety: 무한 루프 방지
            if state.steps >= goal.max_steps:
                return state.abort("Max steps exceeded")

        return state.result
```

---

## 실무 의미

### Planner-Executor 구조

프로덕션 Agent에서 가장 많이 사용되는 패턴이다.
**Planner**는 전략을 결정하고, **Executor**는 실행만 담당한다.
이 분리가 없으면 Agent가 "왜 이걸 했는지" 추적이 불가능하다.

```
사용자 요청
    ↓
[Planner LLM]
  - 목표 분해
  - Sub-task 생성
  - 순서 결정
    ↓
[Task Queue]
  [task1] [task2] [task3]
    ↓
[Executor]
  - Tool 호출
  - 결과 수집
  - 상태 업데이트
    ↓
[결과 통합]
```

### Sub-task 분해 전략

복잡한 Goal을 원자적 Sub-task로 분해한다.
각 Sub-task는 독립적으로 실행 가능해야 한다.
의존성이 있으면 DAG(Directed Acyclic Graph) 구조로 관리한다.

```python
# 복잡한 목표를 Sub-task로 분해
goal = "경쟁사 3곳의 가격을 비교하고 보고서를 작성하라"

sub_tasks = [
    SubTask(id="t1", action="search_competitor_a_price", deps=[]),
    SubTask(id="t2", action="search_competitor_b_price", deps=[]),
    SubTask(id="t3", action="search_competitor_c_price", deps=[]),
    SubTask(id="t4", action="compare_prices", deps=["t1","t2","t3"]),
    SubTask(id="t5", action="write_report", deps=["t4"]),
]
```

---

## 비교: Single-step vs Multi-step Agent

| 기준 | Single-step | Multi-step |
|------|------------|------------|
| **판단 횟수** | 1회 | 여러 번 반복 |
| **상태 관리** | 불필요 | 필수 |
| **복잡도** | 낮음 | 높음 |
| **적합한 Task** | 분류, 요약, 변환 | 조사, 계획, 자동화 |
| **실패 복구** | 불가 | 재시도 가능 |
| **비용** | 낮음 | 높음 |

**언제 Single-step을 써야 하는가**
- 입력 → 출력이 한 번의 LLM 호출로 충분할 때
- 상태가 필요 없을 때
- 실패 복구가 필요 없을 때

**언제 Multi-step을 써야 하는가**
- 외부 정보 수집이 필요할 때
- 이전 결과를 다음 단계가 참조할 때
- 동적으로 계획이 바뀔 수 있을 때

> **판단 기준**: "LLM 한 번 호출로 완료되는가?" → Yes면 Single-step

---

## 주의사항

### 1. Goal을 지나치게 추상적으로 정의하지 않는다

"좋은 결과를 만들어라"는 Goal이 아니다.
Agent가 스스로 성공 여부를 판단할 수 없으면 루프에 빠진다.
반드시 **검증 가능한(verifiable)** 조건으로 정의한다.

### 2. Memory에 모든 것을 담지 않는다

Working Memory에 전체 히스토리를 담으면 컨텍스트가 폭발한다.
필요한 정보만 선택적으로 State에 유지한다.
오래된 정보는 요약하거나 외부 저장소로 이동한다.

### 3. Tool을 직접 연결하지 않는다

Tool A의 출력을 Tool B가 직접 소비하는 구조를 피한다.
반드시 Agent State를 통해 중계한다.
직접 연결은 테스트와 디버깅을 불가능하게 만든다.

### 4. Control Logic에 비즈니스 로직을 섞지 않는다

제어 흐름(언제 실행하는가)과 비즈니스 로직(무엇을 하는가)을 분리한다.
섞이면 수정 시 전체 흐름이 영향을 받는다.

---

## 코드 예제: Agent 4요소 구현

```python
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

# ── 1. Goal ──────────────────────────────────────
@dataclass
class Goal:
    description: str
    success_condition: str
    abort_condition: str
    max_steps: int = 10

# ── 2. Memory / State ─────────────────────────────
class AgentStatus(Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ABORTED = "aborted"

@dataclass
class AgentState:
    goal: Goal
    steps: int = 0
    status: AgentStatus = AgentStatus.RUNNING
    context: dict[str, Any] = field(default_factory=dict)
    history: list[dict] = field(default_factory=list)

    def is_terminal(self) -> bool:
        return self.status != AgentStatus.RUNNING

    def update(self, key: str, value: Any):
        self.context[key] = value
        self.steps += 1

# ── 3. Tool ──────────────────────────────────────
def make_tool(name: str, fn):
    """Tool 래퍼: 실행 결과를 표준 형식으로 반환"""
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            return {"tool": name, "status": "ok", "result": result}
        except Exception as e:
            return {"tool": name, "status": "error", "error": str(e)}
    wrapper.__name__ = name
    return wrapper

# ── 4. Control Logic ─────────────────────────────
class SimpleAgent:
    def __init__(self, tools: list):
        self.tools = {t.__name__: t for t in tools}

    def plan(self, state: AgentState) -> dict:
        """다음 실행할 Tool과 인자를 결정"""
        # 실제로는 LLM이 결정. 여기서는 단순 예시
        if "data" not in state.context:
            return {"tool": "fetch_data", "args": {"url": "..."}}
        if "analysis" not in state.context:
            return {"tool": "analyze", "args": {"data": state.context["data"]}}
        return {"tool": "done", "args": {}}

    def run(self, goal: Goal) -> AgentState:
        state = AgentState(goal=goal)

        while not state.is_terminal():
            # Safety check
            if state.steps >= goal.max_steps:
                state.status = AgentStatus.ABORTED
                break

            # Plan
            action = self.plan(state)
            if action["tool"] == "done":
                state.status = AgentStatus.SUCCESS
                break

            # Execute
            tool_fn = self.tools.get(action["tool"])
            if not tool_fn:
                state.status = AgentStatus.FAILED
                break

            observation = tool_fn(**action["args"])
            state.history.append({"action": action, "obs": observation})

            # Reflect
            if observation["status"] == "error":
                state.status = AgentStatus.FAILED
                break

            state.update(action["tool"], observation["result"])

        return state
```

---

## Q&A

**Q1. Planner와 Executor를 반드시 분리해야 하나요?**

단순한 Agent는 통합해도 됩니다.
하지만 3단계 이상 Multi-step이면 분리를 권장합니다.
분리하면 Planner만 교체해서 전략을 바꿀 수 있습니다.

**Q2. Working Memory의 적절한 크기는?**

일반적으로 최근 5~10개의 관찰(observation)을 유지합니다.
오래된 것은 요약해서 보관합니다.
LLM 컨텍스트 창의 20% 이내로 유지하는 것이 실무 기준입니다.

**Q3. Sub-task 분해는 LLM이 하나요, 코드가 하나요?**

복잡한 분해는 LLM이 합니다.
단순 반복 패턴은 코드로 처리합니다.
혼합 방식: 코드가 템플릿을 제공하고 LLM이 세부 내용을 채웁니다.

**Q4. Goal의 성공 조건을 어떻게 검증하나요?**

자동 검증 가능한 조건을 선호합니다.
예: "파일이 생성되었는가", "HTTP 200 응답이 왔는가"
주관적 품질 평가는 별도 Evaluator Agent를 사용합니다.

---

## 퀴즈

**Q1.** Agent의 4요소 중 "언제 멈추고 언제 재시도할지 결정하는" 요소는?

<details>
<summary>힌트 및 정답</summary>

**힌트**: Plan → Execute → Observe 사이클을 관장하는 요소입니다.

**정답**: Control Logic

Control Logic은 판단 흐름 전체를 담당합니다. Goal의 달성 여부를 평가하고, 다음 행동을 결정하며, 실패 시 재시도나 중단을 처리합니다.
</details>

---

**Q2.** 다음 중 Single-step Agent가 적합한 경우는?

- A) 여러 사이트를 방문해 정보를 수집하는 경우
- B) 텍스트를 한국어로 번역하는 경우
- C) 에러 로그를 분석하고 자동으로 PR을 올리는 경우
- D) 코드베이스 전체를 리팩토링하는 경우

<details>
<summary>힌트 및 정답</summary>

**힌트**: LLM 한 번의 호출로 완료될 수 있는 작업을 찾으세요.

**정답**: B

번역은 입력 → 출력이 한 번의 LLM 호출로 충분합니다. A, C, D는 모두 여러 단계와 외부 정보가 필요한 Multi-step 작업입니다.
</details>

---

**Q3.** Working Memory에 대한 설명으로 틀린 것은?

- A) 현재 Task의 실행 상태를 보관한다
- B) Agent State에 저장된다
- C) 모든 대화 히스토리를 무제한으로 보관해야 한다
- D) 너무 많으면 컨텍스트가 오염된다

<details>
<summary>힌트 및 정답</summary>

**힌트**: 컨텍스트 창의 크기 제한을 생각해보세요.

**정답**: C

Working Memory는 선택적으로 관리해야 합니다. 전체 히스토리를 무제한으로 보관하면 LLM 컨텍스트 창이 초과되고 비용이 급증합니다. 오래된 정보는 요약하거나 외부 저장소로 이동합니다.
</details>

---

**Q4.** Tool 설계 원칙 중 "원자적(atomic)"이란 무엇을 의미하는가?

<details>
<summary>힌트 및 정답</summary>

**힌트**: 데이터베이스 트랜잭션의 원자성과 유사한 개념입니다.

**정답**: 하나의 Tool은 하나의 명확한 역할만 수행한다

Tool이 원자적이면 독립적으로 테스트 가능하고, 다른 Tool과의 결합이 유연해집니다. 하나의 Tool이 검색 + 요약 + 저장을 모두 하면 각 단계의 오류를 구분할 수 없습니다.
</details>

---

**Q5.** Sub-task를 DAG 구조로 관리하는 이유는?

<details>
<summary>힌트 및 정답</summary>

**힌트**: DAG = Directed Acyclic Graph. "방향이 있고 순환이 없는 그래프"입니다.

**정답**: 의존성이 있는 Sub-task를 올바른 순서로 실행하고, 병렬 실행 가능한 것들을 동시에 처리하기 위해

t1, t2, t3이 독립적이면 병렬로 실행하고, t4가 t1~t3에 의존하면 모두 완료 후 실행합니다. DAG 구조 없이는 이 조율이 불가능합니다.
</details>

---

## 실습 명세

### 주제: Agent 상태 다이어그램 작성 및 구현

**목표**: 실제 Agent의 4요소를 분석하고 상태 전이 다이어그램을 설계한 뒤, Python으로 구현한다.

---

### I DO (강사 시연, 15분)

강사가 "뉴스 요약 Agent"의 4요소를 라이브로 설계한다.

```
Goal: 오늘의 AI 뉴스 3건을 요약하고 Slack에 발송
  - 성공 조건: 3건 요약 + Slack 발송 완료
  - 중단 조건: 뉴스 사이트 접근 불가 / 5회 재시도 초과

Memory:
  - Working: {urls: [], articles: [], summaries: [], sent: bool}

Tool:
  - search_news(keyword) → list[URL]
  - fetch_article(url) → str
  - summarize(text) → str
  - send_slack(msg) → bool

Control:
  - Step 1: search_news
  - Step 2: fetch_article × 3 (병렬)
  - Step 3: summarize × 3
  - Step 4: send_slack
  - 실패 시: 최대 3회 재시도 후 중단
```

상태 전이:
```
[IDLE] → [SEARCHING] → [FETCHING] → [SUMMARIZING] → [SENDING] → [DONE]
                ↓               ↓              ↓             ↓
            [FAILED]        [FAILED]       [FAILED]      [FAILED]
                ↓               ↓              ↓             ↓
            [RETRY]         [RETRY]        [RETRY]       [RETRY]
```

---

### WE DO (함께 실습, 30분)

"주식 가격 알림 Agent"를 함께 설계한다.

**Step 1**: Goal 정의 (5분)

함께 작성:
- 목표 설명문
- 성공 조건
- 중단 조건
- 최대 스텝 수

**Step 2**: Memory/State 설계 (10분)

```python
@dataclass
class StockAlertState:
    # 여기에 무엇을 담을지 함께 결정
    goal: Goal
    # ??? 추가할 필드들을 함께 논의
```

**Step 3**: Tool 목록 작성 (5분)

어떤 Tool이 필요한가? 이름과 인터페이스를 함께 정의한다.

**Step 4**: Control Logic 의사코드 작성 (10분)

```python
def run_stock_alert_agent(ticker: str, threshold: float):
    # 함께 작성
    pass
```

---

### YOU DO (독립 실습, 45분)

**과제**: "코드 리뷰 Agent"의 4요소를 독자적으로 설계하고 구현하라.

**요구사항**:
- GitHub PR URL을 입력받아 코드를 분석하고 리뷰 댓글을 작성한다
- Goal, Memory, Tool, Control Logic을 각각 명시적으로 정의한다
- 상태 전이 다이어그램을 ASCII 또는 Mermaid로 그린다
- Python 클래스로 구조를 구현한다 (실제 API 호출은 Mock 사용)

**평가 기준**:
- Goal에 성공/실패 조건이 명시되어 있는가?
- Tool이 원자적으로 설계되었는가?
- Control Logic에 무한 루프 방지가 포함되어 있는가?
- State 구조가 최소한의 정보만 담고 있는가?

**solution/** 디렉토리에 참고 구현 포함.
