# Day 2 Session 1: Agent 4요소 구조 설계

> **2시간** | AI 개발자, 데이터 엔지니어, 기술 리더 대상

<callout icon="📖" color="blue_bg">
	**학습 목표**
	1. Agent의 4요소(Goal, Memory, Tool, Control Logic)를 정의하고 분리할 수 있다
	2. LangChain, LangGraph, Deep Agents에서 4요소가 어떻게 구현되는지 비교한다
	3. 세 프레임워크의 계층 관계와 선택 기준을 이해한다
	4. 요구사항에 따라 적합한 프레임워크를 판단할 수 있다
</callout>

---

## 왜 중요한가

Agent를 "그냥 LLM + 툴"로 만들면 실패한다.
유지보수가 불가능하고, 버그 위치를 찾을 수 없다.
4요소 구조를 먼저 설계해야 확장 가능한 시스템이 된다.

> **핵심 질문**: "이 Agent가 무엇을 기억하고, 어떻게 판단하며, 무엇을 실행하는가?"

Agent를 잘 설계한다는 것은 **목표-기억-도구-제어**를 분리하는 것이다.
분리되지 않은 Agent는 요구사항 하나에도 전체가 흔들린다.
프로덕션 Agent 장애의 대부분이 제어 흐름 미설계에서 비롯된다.

---

## 1. Agent 4요소 개요

### 왜 이것이 중요한가

Agent 프레임워크마다 용어와 API가 다르다.
하지만 모든 Agent는 동일한 4가지 요소로 구성된다.
4요소를 먼저 이해하면 어떤 프레임워크든 빠르게 적용할 수 있다.

### 핵심 원리

| 요소 | 역할 | 핵심 질문 |
|------|------|-----------|
| **Goal** | 무엇을 달성해야 하는가 | "성공 조건은 무엇인가?" |
| **Memory** | 무엇을 기억하는가 | "어떤 컨텍스트를 유지하는가?" |
| **Tool** | 무엇을 할 수 있는가 | "어떤 외부 능력이 필요한가?" |
| **Control Logic** | 어떻게 판단하는가 | "언제 멈추고, 언제 재시도하는가?" |

```
┌─────────────────────────────────────────────┐
│                   Agent                      │
│                                              │
│   ┌──────────┐          ┌──────────┐        │
│   │   Goal   │          │  Memory  │        │
│   │ "무엇을"  │          │ "기억을"  │        │
│   └────┬─────┘          └────┬─────┘        │
│        └──────┐   ┌─────────┘               │
│               ▼   ▼                          │
│         ┌─────────────┐                      │
│         │Control Logic│                      │
│         │  "어떻게"    │                      │
│         └──────┬──────┘                      │
│                ▼                              │
│         ┌──────────┐                         │
│         │   Tool   │                         │
│         │ "행동을"  │                         │
│         └──────────┘                         │
└─────────────────────────────────────────────┘
```

### 실무에서의 의미

4요소 분리는 유지보수와 테스트를 가능하게 한다.
Goal만 바꾸면 같은 Tool 세트로 다른 작업을 수행한다.
Control Logic만 바꾸면 같은 작업을 다른 전략으로 처리한다.

### 주의사항과 흔한 오해

> **오해 1**: "Tool이 많을수록 Agent가 강력하다"
> Tool이 많으면 LLM이 잘못된 Tool을 선택할 확률이 높아진다. 필요한 최소한의 Tool만 제공하는 것이 핵심이다.

> **오해 2**: "Control Logic은 LLM에게 맡기면 된다"
> LLM은 판단을 돕지만, 최종 제어는 코드가 담당해야 한다. 무한 루프 방지, 최대 스텝 제한은 코드로 강제한다.

---

## 2. 프레임워크 소개

### 왜 이것이 중요한가

이 과정에서는 세 가지 프레임워크를 다룬다.
각 프레임워크는 독립적이 아니라 **계층 구조**를 이룬다.
아래 계층을 이해해야 위 계층을 제대로 활용할 수 있다.

### 핵심 원리: 계층 구조

```
Deep Agents (최상위) ── 자동화 + 내장 도구 + 미들웨어
    ↓ 내부적으로 사용
LangGraph (오케스트레이션) ── 그래프 + 노드 + 엣지 + 상태 관리
    ↓ 내부적으로 사용
LangChain (기반) ── 모델 + 도구 + 프롬프트 + RAG
```

| 프레임워크 | 핵심 역할 | 비유 |
|-----------|----------|------|
| **LangChain** | LLM 호출과 Tool 정의 | 부품 (엔진, 바퀴) |
| **LangGraph** | 실행 흐름 조립 | 설계도 (회로 다이어그램) |
| **Deep Agents** | 완성된 에이전트 하네스 | 완성차 (운전만 하면 됨) |

### 실무에서의 의미

단순한 Tool 호출이면 LangChain만으로 충분하다.
복잡한 분기와 상태 관리가 필요하면 LangGraph를 쓴다.
파일 작업과 자율 계획이 필요하면 Deep Agents가 적합하다.

### 다른 접근법과의 비교

| 기준 | LangChain | LangGraph | Deep Agents |
|------|-----------|-----------|-------------|
| **복잡도** | 낮음 | 중간 | 높음 (자동화) |
| **제어 수준** | ReAct 자동 | 노드 단위 | 미들웨어 기반 |
| **상태 관리** | 메모리 | 체크포인터 | 백엔드 |
| **멀티에이전트** | 핸드오프 | 서브그래프 | 서브에이전트 |
| **파일 I/O** | 수동 | 수동 | 내장 |
| **계획 수립** | 수동 | 수동 | `write_todos` 내장 |

<callout icon="💡" color="gray_bg">
	**실습 안내**: `labs/day2/00_basics/` 노트북에서 세 프레임워크를 직접 실행하며 비교한다.
	`02_langchain_basics.ipynb` → `04_langgraph_basics.ipynb` → `05_deep_agents_basics.ipynb` 순서로 진행한다.
</callout>

---

## 3. Goal — "무엇을 달성할 것인가"

### 왜 이것이 중요한가

Goal은 단순한 task description이 아니다.
**성공 조건**과 **실패 조건**을 포함해야 한다.
잘못 정의된 Goal은 무한 루프의 주요 원인이다.

### 핵심 원리

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

### 프레임워크별 Goal 구현

| | LangChain | LangGraph | Deep Agents |
|--|-----------|-----------|-------------|
| **방식** | `SystemMessage` | `SystemMessage` | `system_prompt` + `AGENTS.md` |
| **주입** | 메시지 리스트 첫 번째 | 노드 내 직접 삽입 | 자동 주입 |
| **확장** | — | — | `memory` 파라미터로 규칙 문서 로드 |

```python
# LangChain / LangGraph
messages = [
    SystemMessage(content="판매 데이터에서 이상치를 탐지한다."),
    HumanMessage(content="2024년 3분기 데이터를 분석해줘"),
]

# Deep Agents — system_prompt + AGENTS.md
agent = create_deep_agent(
    model=model,
    system_prompt="판매 데이터에서 이상치를 탐지한다.",
    memory=["/project/AGENTS.md"],  # 영구 규칙 자동 주입
)
```

<callout icon="💡" color="gray_bg">
	Deep Agents의 `AGENTS.md`는 Claude Code의 `CLAUDE.md`와 동일한 패턴이다.
	Goal이 코드가 아닌 **문서로 관리**되어 비개발자도 수정할 수 있다.
</callout>

### 주의사항과 흔한 오해

> **오해**: "Goal을 자세하게 쓸수록 좋다"
> 너무 긴 Goal은 LLM의 주의를 분산시킨다. 핵심 조건만 명확히 기술한다.

---

## 4. Memory — "무엇을 기억하는가"

### 왜 이것이 중요한가

Agent가 판단하려면 과거 정보가 필요하다.
하지만 모든 것을 기억하면 컨텍스트가 폭발한다.
**무엇을, 얼마나, 어디에** 기억할지 설계하는 것이 핵심이다.

### 핵심 원리: 4가지 메모리 레이어

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

### 프레임워크별 Memory 구현

| | LangChain | LangGraph | Deep Agents |
|--|-----------|-----------|-------------|
| **단기 기억** | `InMemorySaver` + `thread_id` | 동일 | 동일 (내부적으로 LangGraph) |
| **장기 기억** | `InMemoryStore` + 수동 도구 | 동일 | `CompositeBackend` 자동 라우팅 |
| **프로덕션** | 직접 구현 | `PostgresStore` 플러그인 | `StoreBackend` (Redis/PG) |

```python
# LangChain / LangGraph — 단기 기억
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
config = {"configurable": {"thread_id": "session-1"}}

# Deep Agents — 경로 기반 자동 라우팅
agent = create_deep_agent(
    model=model,
    backend=lambda rt: CompositeBackend(
        default=StateBackend(rt),               # / → 임시
        routes={"/memories/": StoreBackend(rt)}, # /memories/ → 영속
    ),
)
# /memories/에 쓰면 → 장기 저장 (자동)
# /scratch.txt에 쓰면 → 스레드 종료 시 소멸
```

<callout icon="💡" color="gray_bg">
	Deep Agents는 에이전트가 **파일 경로만으로** 단기/장기 기억을 구분한다.
	별도 메모리 도구를 만들 필요가 없다.
</callout>

### 주의사항과 흔한 오해

> **오해**: "전체 대화 히스토리를 유지해야 정확하다"
> Working Memory에 전체 히스토리를 담으면 비용이 급증한다. 최근 5~10개 관찰만 유지하고, 오래된 것은 요약하거나 외부 저장소로 이동한다.

---

## 5. Tool — "어떤 행동을 할 수 있는가"

### 왜 이것이 중요한가

Tool은 Agent가 외부 세계와 상호작용하는 유일한 수단이다.
잘 설계된 Tool은 재사용이 가능하고, 독립 테스트가 쉽다.
Tool은 **원자적(atomic)**이어야 한다.

### 핵심 원리

하나의 Tool은 하나의 명확한 역할만 수행한다.

```python
# 나쁜 예: Tool이 너무 많은 일을 함
def search_and_summarize(query: str) -> str:
    results = web_search(query)
    summary = llm_summarize(results)
    save_to_db(summary)
    return summary

# 좋은 예: 각 Tool은 하나의 역할
@tool
def web_search(query: str) -> list[str]: ...

@tool
def summarize_text(text: str) -> str: ...

@tool
def save_result(key: str, value: str) -> bool: ...
```

### 프레임워크별 Tool 구현

| | LangChain | LangGraph | Deep Agents |
|--|-----------|-----------|-------------|
| **커스텀 도구** | `@tool` 데코레이터 | 동일 | 동일 |
| **모델 바인딩** | `create_react_agent(tools=)` | `model.bind_tools()` | `create_deep_agent(tools=)` |
| **파일 I/O** | 직접 구현 | 직접 구현 | **내장** 6종 |
| **계획 수립** | 직접 구현 | 직접 구현 | **내장** `write_todos` |
| **서브에이전트** | 직접 구현 | 서브그래프 | **내장** `task` |

```python
# LangChain / LangGraph — 모든 도구를 직접 정의
@tool
def read_file(path: str) -> str:
    """파일 읽기"""
    with open(path) as f:
        return f.read()

agent = create_react_agent(model, tools=[read_file])

# Deep Agents — 파일 도구 6종이 기본 포함
agent = create_deep_agent(model=model, tools=[my_tool])
# 자동 포함: ls, read_file, write_file, edit_file,
#           glob, grep, write_todos, task
```

### 주의사항과 흔한 오해

> **오해**: "Tool A의 출력을 Tool B에 직접 전달하면 효율적이다"
> Tool 간 직접 연결은 테스트와 디버깅을 불가능하게 만든다. 반드시 Agent State를 통해 중계한다.

---

## 6. Control Logic — "어떻게 판단하고 반복하는가"

### 왜 이것이 중요한가

Control Logic은 4요소 중 **프레임워크 간 차이가 가장 크다.**
ReAct 자동 루프, 그래프 명시적 제어, 미들웨어 파이프라인.
어떤 패턴을 선택하느냐가 Agent의 확장성을 결정한다.

### 핵심 원리

기본 제어 루프는 **Plan → Execute → Observe → Reflect**이다.

```python
class AgentControlLoop:
    def run(self, goal: Goal) -> Result:
        state = AgentState(goal=goal)

        while not state.is_terminal():
            action = self.planner.plan(state)       # Plan
            observation = self.executor.execute(action) # Execute
            state = self.reflector.update(state, observation) # Reflect

            if state.steps >= goal.max_steps:       # Safety
                return state.abort("Max steps exceeded")

        return state.result
```

### 프레임워크별 Control Logic 구현

**LangChain — ReAct 자동 루프**

```
User → LLM → tool_calls? → 도구 실행 → LLM → 반복
                  없으면? → 최종 응답 → END
```

```python
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(model, tools)
agent.invoke({"messages": [...]})  # 내부 루프 자동
```

**LangGraph — 그래프 기반 명시적 제어**

```
START → llm_node → [조건부] → tool_node → llm_node → END
```

```python
builder = StateGraph(MessagesState)
builder.add_node("llm", llm_call)
builder.add_node("tools", tool_node)
builder.add_edge(START, "llm")
builder.add_conditional_edges(
    "llm", should_continue,
    {"tools": "tools", END: END},
)
builder.add_edge("tools", "llm")
graph = builder.compile()
```

**Deep Agents — 미들웨어 파이프라인**

```
User → [TodoList → Memory → Skills → Filesystem
        → SubAgent → HITL] → LLM → 도구 실행 → 반복
```

```python
agent = create_deep_agent(
    model=model,
    interrupt_on={"execute": True},  # 위험한 도구는 승인 필요
)
```

### 다른 접근법과의 비교

| | LangChain | LangGraph | Deep Agents |
|--|-----------|-----------|-------------|
| **패턴** | ReAct (자동) | Graph (명시적) | Middleware (자동+확장) |
| **제어 수준** | 블랙박스 | 노드/엣지 단위 | 미들웨어 인터셉트 |
| **분기/조건** | LLM 판단 위임 | `conditional_edge` | 미들웨어 + LLM |
| **사람 개입** | — | `interrupt()` | `interrupt_on` |

### 주의사항과 흔한 오해

> **오해**: "제어 흐름에 비즈니스 로직을 넣어도 된다"
> 제어(언제 실행하는가)와 비즈니스(무엇을 하는가)를 분리한다. 섞이면 수정 시 전체 흐름이 영향을 받는다.

---

## 7. 종합 비교

### 4요소 × 3프레임워크 매트릭스

| 요소 | LangChain | LangGraph | Deep Agents |
|------|-----------|-----------|-------------|
| **Goal** | `SystemMessage` | `SystemMessage` | `system_prompt` + `AGENTS.md` |
| **Memory** | 체크포인터 + 수동 Store | 체크포인터 + Store | 체크포인터 + `CompositeBackend` 자동 라우팅 |
| **Tool** | `@tool` 직접 정의 | `@tool` + `bind_tools` | `@tool` + **내장 도구 8종** |
| **Control** | ReAct (블랙박스) | Graph (명시적 노드/엣지) | Middleware (자동+확장 가능) |

### 선택 기준

- **LangChain**: 단일 에이전트, 간단한 Tool 호출, RAG
- **LangGraph**: 복잡한 워크플로, 조건부 분기, 사람 개입
- **Deep Agents**: 파일 기반 작업, 자율 계획, 서브에이전트

> **기억할 것**: 세 프레임워크는 경쟁이 아니라 **계층 구조**다. Deep Agents는 LangGraph 위에서, LangGraph는 LangChain 위에서 동작한다.

---

## 비교: Single-step vs Multi-step Agent

| 기준 | Single-step | Multi-step |
|------|------------|------------|
| **판단 횟수** | 1회 | 여러 번 반복 |
| **상태 관리** | 불필요 | 필수 |
| **복잡도** | 낮음 | 높음 |
| **적합한 Task** | 분류, 요약, 변환 | 조사, 계획, 자동화 |
| **실패 복구** | 불가 | 재시도 가능 |

> **판단 기준**: "LLM 한 번 호출로 완료되는가?" → Yes면 Single-step

---

## Q&A

**Q1. Planner와 Executor를 반드시 분리해야 하나요?**

단순한 Agent는 통합해도 됩니다.
하지만 3단계 이상 Multi-step이면 분리를 권장합니다.
분리하면 Planner만 교체해서 전략을 바꿀 수 있습니다.

**Q2. Working Memory의 적절한 크기는?**

일반적으로 최근 5~10개의 관찰을 유지합니다.
오래된 것은 요약해서 보관합니다.
LLM 컨텍스트 창의 20% 이내가 실무 기준입니다.

**Q3. LangChain만으로 충분한 경우는 언제인가요?**

Tool 2~3개, 단일 분기, 상태 불필요한 경우입니다.
`create_react_agent()`가 내부 루프를 자동 처리합니다.
분기가 복잡해지면 LangGraph로 전환합니다.

**Q4. Deep Agents의 내장 도구를 끄고 싶으면?**

`create_deep_agent()`에서 미들웨어를 선택적으로 제거합니다.
`FilesystemMiddleware`를 빼면 파일 도구가 비활성화됩니다.
필요한 미들웨어만 명시적으로 지정할 수 있습니다.

**Q5. 프레임워크를 혼합해서 쓸 수 있나요?**

가능합니다. Deep Agents 내부에서 LangChain 도구를 사용합니다.
LangGraph 그래프도 Deep Agents에 통합할 수 있습니다.
계층 구조이므로 아래 계층 API를 자유롭게 호출합니다.

---

## 퀴즈

**Q1.** Agent의 4요소 중 "언제 멈추고 언제 재시도할지 결정하는" 요소는?

<details>
<summary>💡 힌트</summary>
	Plan → Execute → Observe 사이클을 관장하는 요소입니다.
</details>

<details>
<summary>✅ 정답</summary>
	**Control Logic**
	**설명:** Control Logic은 판단 흐름 전체를 담당한다. Goal 달성 여부를 평가하고, 다음 행동을 결정하며, 실패 시 재시도나 중단을 처리한다.
</details>

---

**Q2.** 다음 중 Single-step Agent가 적합한 경우는?

- A) 여러 사이트를 방문해 정보를 수집하는 경우
- B) 텍스트를 한국어로 번역하는 경우
- C) 에러 로그를 분석하고 자동으로 PR을 올리는 경우
- D) 코드베이스 전체를 리팩토링하는 경우

<details>
<summary>💡 힌트</summary>
	LLM 한 번의 호출로 완료될 수 있는 작업을 찾으세요.
</details>

<details>
<summary>✅ 정답</summary>
	**B**
	**설명:** 번역은 입력 → 출력이 한 번의 LLM 호출로 충분하다. A, C, D는 모두 여러 단계와 외부 정보가 필요한 Multi-step 작업이다.
</details>

---

**Q3.** Deep Agents에서 `backend` 파라미터를 생략하면 어떤 일이 발생하는가?

- A) 로컬 디스크에 파일을 저장한다
- B) 에러가 발생한다
- C) StateBackend가 적용되어 빈 가상 파일시스템이 된다
- D) StoreBackend가 적용되어 Redis에 저장한다

<details>
<summary>💡 힌트</summary>
	기본 백엔드는 에페메럴(ephemeral)입니다.
</details>

<details>
<summary>✅ 정답</summary>
	**C**
	**설명:** `StateBackend`가 기본값이다. 파일을 에이전트 메모리(LangGraph state)에만 저장하므로, 실제 디스크와 완전히 분리된 빈 파일시스템처럼 보인다. 스레드 종료 시 소멸한다.
</details>

---

**Q4.** 세 프레임워크의 계층 관계로 올바른 것은?

- A) LangChain → Deep Agents → LangGraph
- B) Deep Agents → LangGraph → LangChain
- C) LangGraph → LangChain → Deep Agents
- D) 세 프레임워크는 독립적이다

<details>
<summary>💡 힌트</summary>
	"위 계층이 아래 계층을 내부적으로 사용한다"는 관계입니다.
</details>

<details>
<summary>✅ 정답</summary>
	**B**
	**설명:** Deep Agents는 LangGraph 위에서, LangGraph는 LangChain 위에서 동작한다. `create_deep_agent()`의 반환 타입은 LangGraph의 `CompiledStateGraph`이다.
</details>

---

**Q5.** Tool 설계 원칙 중 "원자적(atomic)"이란 무엇을 의미하는가?

<details>
<summary>💡 힌트</summary>
	데이터베이스 트랜잭션의 원자성과 유사한 개념입니다.
</details>

<details>
<summary>✅ 정답</summary>
	**하나의 Tool은 하나의 명확한 역할만 수행한다**
	**설명:** Tool이 원자적이면 독립 테스트가 가능하고 결합이 유연하다. 검색 + 요약 + 저장을 한 Tool에 넣으면 각 단계의 오류를 구분할 수 없다.
</details>

---

## 실습

<callout icon="💡" color="gray_bg">
	이 세션의 실습은 `labs/day2/00_basics/` 노트북을 사용한다.
	프레임워크별 Agent를 직접 만들고 실행하며 4요소를 체감한다.
</callout>

### 🔍 I DO: 프레임워크 기초 체험 {toggle="true"}
	**시간**: 90분
	**노트북 순서**:
	1. `00_setup.ipynb` — 환경 설정, API 키, Langfuse 연결 (15분)
	2. `01_llm_basics.ipynb` — LLM 호출, 메시지 구조, 스트리밍 (15분)
	3. `02_langchain_basics.ipynb` — `@tool`, `create_react_agent()` (20분)
	4. `03_langchain_memory.ipynb` — `InMemorySaver`, `thread_id` (15분)
	5. `04_langgraph_basics.ipynb` — `StateGraph`, Node-Edge-State (25분)

	강사가 각 노트북을 라이브로 실행하며 4요소가 어디에 대응하는지 설명한다.
	<callout icon="💡" color="gray_bg">
		**관찰 포인트**: 같은 "웹 검색 Agent"가 프레임워크마다 어떻게 달라지는가?
	</callout>

### 🤝 WE DO: Deep Agents 체험 {toggle="true"}
	**시간**: 20분
	**노트북**: `05_deep_agents_basics.ipynb`

	함께 `create_deep_agent()`를 실행한다.
	- [ ] 기본 에이전트 생성 (StateBackend)
	- [ ] 파일 도구 6종 확인 (ls, read_file, write_file 등)
	- [ ] FilesystemBackend로 전환하여 로컬 파일 접근
	- [ ] 커스텀 Tool 추가

### 🚀 YOU DO: 프레임워크 비교 분석 {toggle="true"}
	**시간**: 10분
	**노트북**: `06_comparison.ipynb`

	<callout icon="📋" color="yellow_bg">
		**요구사항**
		1. 세 프레임워크로 동일한 작업을 수행하고 결과를 비교한다
		2. 각 프레임워크에서 4요소(Goal, Memory, Tool, Control)가 어디에 대응하는지 정리한다
		3. 본인의 업무에 가장 적합한 프레임워크를 선택하고 이유를 작성한다
	</callout>

<details>
<summary>💡 힌트</summary>
	프레임워크 선택 기준: 복잡도, 제어 수준, 파일 I/O 필요 여부
</details>
