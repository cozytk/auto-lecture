# Day 2 Session 4: 구조 리팩토링 & 확장성 설계

> **2시간** | AI 개발자, 데이터 엔지니어, 기술 리더 대상

<callout icon="📖" color="blue_bg">
	**학습 목표**
	1. 단일 Agent에서 Planner-Executor-Validator 구조로 전환할 수 있다
	2. 결합도를 낮추는 3가지 전략(인터페이스, Event Bus, State 매개체)을 적용할 수 있다
	3. Trace 로그 구조를 설계하고 Langfuse/LangSmith로 연동할 수 있다
	4. Deep Agents 하네스의 자동화 패턴을 이해한다
</callout>

---

## 왜 중요한가

처음에 단순하게 만든 Agent는 반드시 한계를 맞는다.
요구사항이 추가될 때마다 코드가 엉키고, 버그가 늘어난다.
이때 **구조 전환 비용**이 아무리 잘 만든 Agent도 망가뜨린다.

> **핵심 질문**: "지금 이 구조가 6개월 후에도 유지보수 가능한가?"

단일 Agent를 확장형으로 전환하는 것은 기술적 결정이 아닌 **설계 결정**이다.
결합도(coupling)를 낮추면 각 부분을 독립적으로 변경할 수 있다.
Trace 로그는 확장 후 발생하는 문제를 추적하는 유일한 수단이다.

---

## 핵심 원리

### 단일 Agent → 확장형 구조 전환

단일 Agent의 한계는 명확하다.

```
[단일 Agent의 문제]
┌──────────────────────────────────────┐
│ def run_agent(input):                │
│   result1 = llm_call_1(input)        │  ← LLM 호출과 비즈니스 로직이 섞임
│   result2 = tool_call(result1)       │  ← Tool 호출이 직접 연결됨
│   result3 = llm_call_2(result2)      │  ← 중간 상태를 추적할 수 없음
│   return result3                     │
└──────────────────────────────────────┘
```

확장형으로 전환하면:

```
[확장형 구조]
┌─────────┐    ┌──────────┐    ┌───────────┐
│ Planner │ → │ Executor │ → │ Validator │
└─────────┘    └──────────┘    └───────────┘
     ↑                ↑               ↑
  교체 가능        독립 테스트       독립 교체
```

**전환 시점 판단 기준**:
- Tool이 3개를 초과할 때
- 분기 조건이 2개를 초과할 때
- 실행 시간이 10초를 초과할 때
- 팀원이 코드를 혼자 이해하기 어렵다고 할 때

### 전환 절차

단계적으로 전환하는 것이 안전하다.

**Step 1**: 현재 코드에서 책임을 분리한다

```python
# Before: 모든 것이 한 함수에
def run_agent(query: str) -> str:
    plan = llm.invoke(f"Plan for: {query}")
    results = []
    for step in parse_plan(plan):
        result = execute_step(step)
        results.append(result)
    return llm.invoke(f"Summarize: {results}")

# After: 책임별로 분리
class Planner:
    def plan(self, query: str) -> list[Step]:
        response = llm.invoke(f"Plan for: {query}")
        return parse_plan(response)

class Executor:
    def execute(self, step: Step) -> StepResult:
        return execute_step(step)

class Synthesizer:
    def synthesize(self, results: list[StepResult]) -> str:
        return llm.invoke(f"Summarize: {results}")

class AgentOrchestrator:
    def run(self, query: str) -> str:
        steps = self.planner.plan(query)
        results = [self.executor.execute(s) for s in steps]
        return self.synthesizer.synthesize(results)
```

**Step 2**: State를 명시적으로 정의한다

**Step 3**: Tool을 독립 모듈로 분리한다

**Step 4**: 그래프(LangGraph) 구조로 전환한다

---

## 결합도 낮추는 설계 전략

### 결합도(Coupling)란

결합도는 "한 모듈이 변경될 때 다른 모듈이 얼마나 영향받는가"다.
높은 결합도 → 변경 하나가 전체를 흔듦
낮은 결합도 → 각 모듈이 독립적으로 변경 가능

### 3가지 결합도 감소 전략

**전략 1: 인터페이스를 통한 추상화**

```python
from abc import ABC, abstractmethod

# 구체 구현이 아닌 인터페이스에 의존
class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str: ...

class OpenAIProvider(LLMProvider):
    def complete(self, prompt: str) -> str:
        return openai_client.chat(prompt)

class AnthropicProvider(LLMProvider):
    def complete(self, prompt: str) -> str:
        return anthropic_client.messages(prompt)

class Planner:
    # LLMProvider에 의존. 구체 구현 모름
    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def plan(self, query: str) -> list[Step]:
        return self.llm.complete(f"Plan: {query}")
```

**전략 2: Event/Message 기반 통신**

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class AgentEvent:
    type: str
    payload: Any
    source: str

class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list] = {}

    def subscribe(self, event_type: str, handler):
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: AgentEvent):
        for handler in self._subscribers.get(event.type, []):
            handler(event)

# 각 컴포넌트가 직접 연결되지 않음
bus = EventBus()

def on_plan_complete(event: AgentEvent):
    steps = event.payload
    executor.execute_steps(steps)

bus.subscribe("plan_complete", on_plan_complete)
```

**전략 3: State를 중간 매개체로 사용**

```python
# 컴포넌트 간 직접 호출 금지
# 모든 통신은 State를 통해

class PlannerNode:
    def run(self, state: AgentState) -> dict:
        steps = self._plan(state["query"])
        return {"steps": steps}     # State에 기록

class ExecutorNode:
    def run(self, state: AgentState) -> dict:
        steps = state["steps"]      # State에서 읽음
        results = [self._execute(s) for s in steps]
        return {"results": results}
```

---

## Trace 로그 구조 설계 기초

### Trace란

Trace는 Agent 실행의 전체 기록이다.
어떤 Node가, 언제, 어떤 입력으로, 어떤 출력을 냈는지 추적한다.
프로덕션에서 버그를 재현하고 성능을 분석하는 유일한 수단이다.

### Trace 구조

```python
from dataclasses import dataclass, field
from typing import Any
import time
import uuid

@dataclass
class TraceSpan:
    """단일 실행 단위의 Trace"""
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    parent_id: str | None = None
    name: str = ""
    started_at: float = field(default_factory=time.time)
    ended_at: float | None = None
    input: Any = None
    output: Any = None
    error: str | None = None
    metadata: dict = field(default_factory=dict)

    def finish(self, output: Any = None, error: str = None):
        self.ended_at = time.time()
        self.output = output
        self.error = error

    @property
    def duration_ms(self) -> float:
        if self.ended_at:
            return (self.ended_at - self.started_at) * 1000
        return 0.0

@dataclass
class AgentTrace:
    """전체 Agent 실행 Trace"""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    spans: list[TraceSpan] = field(default_factory=list)

    def start_span(self, name: str, parent_id: str = None, **metadata) -> TraceSpan:
        span = TraceSpan(name=name, parent_id=parent_id, metadata=metadata)
        self.spans.append(span)
        return span

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "total_duration_ms": sum(s.duration_ms for s in self.spans),
            "spans": [
                {
                    "id": s.span_id,
                    "name": s.name,
                    "duration_ms": round(s.duration_ms, 2),
                    "error": s.error,
                }
                for s in self.spans
            ],
        }
```

### Trace 통합

```python
class TracedNode:
    """모든 Node의 기반 클래스: 자동으로 Trace를 기록"""

    def __init__(self, name: str, trace: AgentTrace):
        self.name = name
        self.trace = trace

    def run(self, state: dict) -> dict:
        span = self.trace.start_span(
            self.name,
            input_keys=list(state.keys()),
        )
        try:
            result = self._run(state)
            span.finish(output=list(result.keys()) if result else [])
            return result
        except Exception as e:
            span.finish(error=str(e))
            raise

    def _run(self, state: dict) -> dict:
        raise NotImplementedError
```

---

## 유지보수 가능한 구조 기준

### 체크리스트

| 기준 | 확인 방법 |
|------|-----------|
| **단일 책임** | 각 클래스/함수가 한 가지 이유로만 변경되는가? |
| **테스트 가능** | 외부 의존 없이 단위 테스트가 가능한가? |
| **명확한 인터페이스** | 함수 시그니처를 보면 무슨 일을 하는지 아는가? |
| **상태 추적 가능** | 임의 시점의 Agent 상태를 재현할 수 있는가? |
| **교체 가능** | LLM Provider를 바꿔도 다른 코드 수정이 없는가? |
| **관찰 가능** | 프로덕션에서 무슨 일이 일어나는지 로그로 알 수 있는가? |

### 코드 스멜(Code Smell) 탐지

```python
# 스멜 1: God Function (모든 것을 하는 함수)
def process_everything(input, db, llm, cache, slack, email):
    # 100줄...
    pass

# 스멜 2: 암묵적 State (전역 변수로 상태 공유)
_global_context = {}
def node_a():
    _global_context["result"] = llm.invoke(...)  # 위험!

# 스멜 3: 숨겨진 의존성
def analyze(text: str) -> str:
    # 내부에서 몰래 DB에 쓰기 (사이드 이펙트)
    db.save_analysis(text)
    return llm.invoke(text)

# 개선된 버전
def analyze(text: str, *, persist: bool = False) -> AnalysisResult:
    result = AnalysisResult(text=llm.invoke(text))
    return result  # 사이드 이펙트는 호출자가 결정
```

---

## 비교: 구조별 유지보수성

| 구조 | 변경 용이성 | 테스트 용이성 | 관찰 가능성 | 팀 협업 |
|------|------------|--------------|------------|---------|
| **단일 함수** | 매우 낮음 | 어려움 | 없음 | 불가 |
| **클래스 분리** | 중간 | 가능 | 제한적 | 어려움 |
| **LangGraph** | 높음 | 쉬움 | 내장 지원 | 가능 |
| **마이크로서비스** | 매우 높음 | 독립적 | 완전함 | 병렬 가능 |

> **현실적 권장**: 대부분의 Agent → LangGraph + Trace 로그가 최적

---

## 주의사항

### 1. 조기 최적화를 피한다

처음부터 마이크로서비스로 만들 필요 없다.
단순하게 시작하고, 병목이 증명되었을 때 확장한다.
"나중에 확장이 쉬운 구조"와 "지금 당장 최대로 확장된 구조"는 다르다.

### 2. 리팩토링과 기능 추가를 동시에 하지 않는다

구조를 변경할 때는 기능을 동결한다.
기능을 추가할 때는 구조를 유지한다.
둘을 동시에 하면 어떤 변경이 버그를 유발했는지 알 수 없다.

### 3. Trace 없이 프로덕션에 배포하지 않는다

개발 환경에서는 print로 충분하다.
프로덕션에서는 반드시 구조화된 Trace가 필요하다.
LangSmith, Langfuse, OpenTelemetry 중 하나를 선택해 연동한다.

### 4. 인터페이스를 먼저 설계한다

구현보다 인터페이스를 먼저 정의한다.
인터페이스가 안정적이면 구현은 언제든 교체 가능하다.
"어떻게 구현하는가"보다 "어떻게 사용하는가"를 먼저 생각한다.

---

## 코드 예제: 단일 Agent → 확장형 리팩토링

```python
# ══════════════════════════════════════════════
# BEFORE: 리팩토링 전 (단일 함수)
# ══════════════════════════════════════════════
def old_agent(query: str) -> str:
    # 모든 것이 섞여 있음
    plan_prompt = f"Query: {query}\nCreate a 3-step plan."
    plan = llm.invoke(plan_prompt)
    steps = plan.split("\n")

    results = []
    for step in steps:
        if "search" in step.lower():
            result = requests.get(f"https://api.search.com?q={step}").json()
            results.append(str(result))
        elif "analyze" in step.lower():
            result = llm.invoke(f"Analyze: {results}")
            results.append(result)

    final = llm.invoke(f"Summarize: {results}")
    return final


# ══════════════════════════════════════════════
# AFTER: 리팩토링 후 (확장형 구조)
# ══════════════════════════════════════════════
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
import uuid, time

# ── 공통 타입 ─────────────────────────────────
@dataclass
class Step:
    type: str          # "search" | "analyze" | "summarize"
    description: str

@dataclass
class StepResult:
    step: Step
    output: str
    ok: bool
    error: str = ""

@dataclass
class PipelineState:
    query: str
    plan: list[Step] = field(default_factory=list)
    results: list[StepResult] = field(default_factory=list)
    final_answer: str = ""

# ── 인터페이스 ─────────────────────────────────
class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str: ...

class ToolProvider(ABC):
    @abstractmethod
    def search(self, query: str) -> str: ...

# ── 컴포넌트 ──────────────────────────────────
class Planner:
    def __init__(self, llm: LLMProvider):
        self._llm = llm

    def plan(self, query: str) -> list[Step]:
        response = self._llm.complete(
            f"Query: {query}\nCreate steps. Format: TYPE|DESCRIPTION"
        )
        steps = []
        for line in response.strip().split("\n"):
            if "|" in line:
                type_, desc = line.split("|", 1)
                steps.append(Step(type=type_.strip().lower(), description=desc.strip()))
        return steps or [Step(type="analyze", description=query)]

class Executor:
    def __init__(self, llm: LLMProvider, tools: ToolProvider):
        self._llm = llm
        self._tools = tools

    def execute(self, step: Step, context: list[StepResult]) -> StepResult:
        ctx_text = "\n".join(r.output for r in context if r.ok)
        try:
            if step.type == "search":
                output = self._tools.search(step.description)
            else:
                output = self._llm.complete(
                    f"Context: {ctx_text}\nTask: {step.description}"
                )
            return StepResult(step=step, output=output, ok=True)
        except Exception as e:
            return StepResult(step=step, output="", ok=False, error=str(e))

class Synthesizer:
    def __init__(self, llm: LLMProvider):
        self._llm = llm

    def synthesize(self, query: str, results: list[StepResult]) -> str:
        good = [r.output for r in results if r.ok]
        if not good:
            return "처리 중 오류가 발생했습니다."
        return self._llm.complete(
            f"Query: {query}\nResults:\n" + "\n".join(good) + "\n\nSummarize:"
        )

# ── 오케스트레이터 ────────────────────────────
class RefactoredAgent:
    def __init__(
        self,
        llm: LLMProvider,
        tools: ToolProvider,
        trace_enabled: bool = True,
    ):
        self.planner = Planner(llm)
        self.executor = Executor(llm, tools)
        self.synthesizer = Synthesizer(llm)
        self.trace_enabled = trace_enabled
        self._trace_log: list[dict] = []

    def _log(self, event: str, data: Any):
        if self.trace_enabled:
            self._trace_log.append({
                "ts": time.time(),
                "event": event,
                "data": data,
            })

    def run(self, query: str) -> str:
        state = PipelineState(query=query)
        self._log("start", {"query": query})

        # Plan
        state.plan = self.planner.plan(query)
        self._log("planned", {"steps": [s.type for s in state.plan]})

        # Execute
        for step in state.plan:
            result = self.executor.execute(step, state.results)
            state.results.append(result)
            self._log("step_done", {"type": step.type, "ok": result.ok})

        # Synthesize
        state.final_answer = self.synthesizer.synthesize(query, state.results)
        self._log("done", {"answer_len": len(state.final_answer)})

        return state.final_answer

    def get_trace(self) -> list[dict]:
        return self._trace_log


# ── Mock 구현 (테스트용) ──────────────────────
class MockLLM(LLMProvider):
    def complete(self, prompt: str) -> str:
        if "Create steps" in prompt:
            return "search|AI 최신 뉴스\nanalyze|수집된 뉴스 분석"
        return f"[Mock 응답] {prompt[:50]}"

class MockTools(ToolProvider):
    def search(self, query: str) -> str:
        return f"[검색 결과] {query}: 뉴스 3건 발견"


# ── 실행 예시 ─────────────────────────────────
if __name__ == "__main__":
    agent = RefactoredAgent(
        llm=MockLLM(),
        tools=MockTools(),
        trace_enabled=True,
    )

    answer = agent.run("2026년 AI Agent 트렌드를 알려줘")
    print("=== 최종 답변 ===")
    print(answer)
    print("\n=== Trace 로그 ===")
    for entry in agent.get_trace():
        print(f"  [{entry['event']}] {entry['data']}")
```

---

## Q&A

**Q1. 언제 클래스 분리로 충분하고, 언제 LangGraph가 필요한가요?**

클래스 분리로 충분한 경우:
- 순서가 고정된 3단계 이하 파이프라인
- 분기나 루프가 없는 경우

LangGraph가 필요한 경우:
- 조건 분기나 재시도 루프가 있는 경우
- State를 영속화하거나 재개가 필요한 경우
- 그래프를 시각화해야 하는 경우

**Q2. Trace 로그와 일반 로깅의 차이는?**

일반 로그: 개발자를 위한 텍스트 출력. 구조가 없다.
Trace: 인과관계가 있는 구조화된 실행 기록. Span ID로 연결된다.
Trace는 "A가 실행되어 B를 호출하고 C가 실패했다"를 추적할 수 있다.

**Q3. 인터페이스를 추상 기반 클래스로 만들어야 하나요?**

Python에서 ABC는 선택사항이다.
Protocol을 사용하면 더 유연한 덕 타이핑이 가능하다.
중요한 것은 "어떤 메서드를 구현해야 하는가"를 명시하는 것이다.
팀 규모가 클수록 ABC나 Protocol을 사용하는 것이 안전하다.

**Q4. 리팩토링 후 기존 테스트가 깨질까요?**

인터페이스가 유지되면 외부 테스트는 깨지지 않는다.
내부 구현이 바뀌어도 동일한 입력에 동일한 출력이 나와야 한다.
리팩토링 전에 충분한 통합 테스트를 작성해두면 안전망이 생긴다.

---

## 퀴즈

**Q1.** 단일 Agent에서 확장형으로 전환하는 적절한 시점은?

- A) 프로젝트 시작 시점
- B) Tool이 3개를 초과하거나 분기 조건이 2개를 초과할 때
- C) 항상 처음부터 확장형으로 만든다
- D) LLM 호출이 1회를 초과할 때

<details>
<summary>힌트 및 정답</summary>

**힌트**: "조기 최적화를 피한다"는 원칙을 기억하세요.

**정답**: B

단순한 경우에는 단일 구조가 더 효율적입니다. Tool이 3개를 넘거나, 분기가 2개를 넘거나, 실행 시간이 10초를 초과하거나, 팀원이 이해하기 어려워질 때 전환을 고려합니다.
</details>

---

**Q2.** 결합도를 낮추기 위해 State를 중간 매개체로 사용하는 이유는?

<details>
<summary>힌트 및 정답</summary>

**힌트**: Node A가 Node B를 직접 호출한다면 어떤 문제가 생길까요?

**정답**: 컴포넌트 간 직접 의존성을 없애 각 컴포넌트를 독립적으로 교체하고 테스트할 수 있게 하기 위해

State를 통해 통신하면 Node A는 Node B의 존재를 알 필요가 없습니다. Node B를 교체해도 Node A 코드는 수정할 필요가 없습니다.
</details>

---

**Q3.** Trace에서 `span_id`와 `parent_id`를 사용하는 이유는?

<details>
<summary>힌트 및 정답</summary>

**힌트**: 여러 Node가 중첩되어 실행될 때 어떻게 인과관계를 추적할까요?

**정답**: 실행 단위 간의 부모-자식 관계를 추적하여 어떤 Node가 어떤 Node를 호출했는지 파악하기 위해

예를 들어 Orchestrator(parent) → Planner(child) → LLM call(grandchild) 구조를 span_id/parent_id로 연결하면 전체 실행 트리를 재구성할 수 있습니다.
</details>

---

**Q4.** 다음 코드에서 코드 스멜(Code Smell)을 찾으시오.

```python
def analyze(text: str) -> str:
    db.save_analysis(text)  # 내부에서 DB 저장
    return llm.invoke(text)
```

<details>
<summary>힌트 및 정답</summary>

**힌트**: 함수의 이름과 실제로 하는 일이 일치하는지 확인하세요.

**정답**: 숨겨진 사이드 이펙트 (Hidden Side Effect)

`analyze`는 분석만 해야 하는데 내부에서 DB에 저장합니다. 호출자는 DB가 변경되는지 알 수 없습니다. 테스트 시 DB 설정이 필요해져 단위 테스트가 불가능해집니다. `persist=True` 파라미터로 명시적으로 만들어야 합니다.
</details>

---

**Q5.** 리팩토링 시 "기능 추가와 구조 변경을 동시에 하지 않는다"는 원칙의 이유는?

<details>
<summary>힌트 및 정답</summary>

**힌트**: 두 가지 변경이 동시에 일어날 때 버그가 발생하면 어떻게 됩니까?

**정답**: 버그의 원인이 구조 변경인지 기능 추가인지 알 수 없어 디버깅이 불가능해지기 때문이다

리팩토링은 외부 동작을 바꾸지 않는 내부 구조 개선입니다. 기능 추가는 외부 동작을 바꿉니다. 둘을 동시에 하면 어느 변경이 문제를 일으켰는지 추적이 불가능합니다.
</details>

---

## Deep Agents의 확장성 패턴

Deep Agents는 위에서 설명한 리팩토링 패턴을 **자동화**한다.

### 내장된 확장성 도구

| 도구 | 역할 | 대응하는 수동 패턴 |
|------|------|-------------------|
| `write_todos` | 계획 수립 자동화 | Planner 클래스 |
| `task` | 서브에이전트 위임 | Executor 분리 |
| `FilesystemMiddleware` | 파일 I/O 자동화 | Tool 래퍼 |
| `SummarizationMiddleware` | 컨텍스트 자동 압축 | Memory 관리 |

```python
# 수동 구현 (LangGraph)
class Planner: ...
class Executor: ...
class Validator: ...
graph = build_graph(planner, executor, validator)

# Deep Agents — 위 패턴이 자동 내장
agent = create_deep_agent(
    model=model,
    system_prompt="데이터 분석 에이전트입니다.",
    # Planner = write_todos (자동)
    # Executor = 빌트인 도구 + 커스텀 도구
    # Validator = interrupt_on으로 사람 검증
    interrupt_on={"execute": True},
)
```

### Observability: Langfuse / LangSmith

```python
# Langfuse 연동 — callback 하나로 전체 Trace 자동 수집
from langfuse.langchain import CallbackHandler
handler = CallbackHandler()

result = agent.invoke(
    {"messages": [...]},
    config={"callbacks": [handler]},
)
# → Langfuse 대시보드에서 Node별 실행 시간, 비용, 오류 확인
```

<callout icon="💡" color="gray_bg">
	`labs/day2/langfuse-self-host/`에서 로컬 Langfuse 서버를 실행할 수 있다.
	`00_basics/00_setup.ipynb`에서 이미 Langfuse 연동을 설정했다.
</callout>

---

## 실습

<callout icon="💡" color="gray_bg">
	이 세션은 별도 노트북 없이 가이드 내 코드 예제로 진행한다.
	위의 Before/After 코드를 직접 타이핑하며 리팩토링을 체험한다.
</callout>

### 🔍 I DO: 코드 스멜 탐지와 리팩토링 {toggle="true"}
	**시간**: 20분

	강사가 아래 "나쁜 예시" 코드를 라이브로 리팩토링한다.

	```python
	# 리팩토링 대상
	import openai, requests, sqlite3

	global_db = sqlite3.connect("agent.db")

	def do_research(query, model="gpt-4o"):
	    resp = requests.get(f"https://api.example.com?q={query}")
	    results = resp.json()["items"]
	    global_db.execute("INSERT INTO searches VALUES (?)", [query])
	    global_db.commit()
	    analysis = openai.chat.completions.create(
	        model=model,
	        messages=[{"role": "user", "content": f"Analyze: {results}"}]
	    ).choices[0].message.content
	    return analysis
	```

	코드 스멜: God Function, 전역 상태, 숨겨진 사이드 이펙트.
	Planner / Executor / Synthesizer로 분리하고 Trace 추가.

### 🤝 WE DO: Trace 로그 설계 {toggle="true"}
	**시간**: 20분

	함께 TraceSpan 구조를 구현한다.
	- [ ] TraceSpan 클래스 정의 (span_id, parent_id, duration)
	- [ ] TracedNode 기반 클래스로 자동 Trace 기록
	- [ ] Langfuse 대시보드에서 Trace 확인

### 🚀 YOU DO: 리팩토링 실전 {toggle="true"}
	**시간**: 20분

	<callout icon="📋" color="yellow_bg">
		**요구사항**
		1. Session 1~3에서 만든 코드 중 하나를 선택한다
		2. 코드 스멜을 3개 이상 찾아 목록화한다
		3. Planner-Executor-Validator 구조로 리팩토링한다
		4. MockLLM으로 단위 테스트를 작성한다
	</callout>

<details>
<summary>💡 힌트</summary>
	리팩토링 순서: 코드 스멜 발견 → 인터페이스 설계 → 컴포넌트 분리 → Trace 추가. 기능 추가와 구조 변경을 동시에 하지 않는다.
</details>
