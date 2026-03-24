# Day 2 Session 2: LangGraph 기반 제어 흐름 설계

> **2시간** | AI 개발자, 데이터 엔지니어, 기술 리더 대상

<callout icon="📖" color="blue_bg">
	**학습 목표**
	1. LangGraph의 Node–Edge–State 구조를 이해하고 구현할 수 있다
	2. 조건 분기(Conditional Edge)로 동적 흐름을 설계할 수 있다
	3. Retry/Fallback 전략을 State 기반으로 구현할 수 있다
	4. 5가지 워크플로 패턴(Chaining, Parallelization, Routing, Orchestrator-Worker, Evaluator-Optimizer)을 구분할 수 있다
</callout>

---

## 왜 중요한가

LLM 호출만으로는 복잡한 워크플로우를 만들 수 없다.
분기, 루프, 상태 전달이 필요한 순간 코드가 엉킨다.
LangGraph는 이 문제를 **그래프 구조**로 해결한다.

> **핵심 질문**: "Agent의 흐름을 어떻게 명확하게 표현하고 제어할 것인가?"

LangGraph는 2024년 말부터 프로덕션 Agent 구현의 표준이 되고 있다.
State Machine 기반이라 흐름이 예측 가능하고 테스트가 쉽다.
2026년 현재 LangGraph 0.3.x 버전 기준으로 설명한다.

---

## 핵심 원리

### Node–Edge–State 구조

LangGraph의 3가지 핵심 개념은 다음과 같다.

```
Node  = 실행 단위 (Python 함수)
Edge  = 흐름 연결 (다음 Node 지정)
State = 흐름 전반에 걸쳐 공유되는 데이터
```

**모든 Node는 State를 받아서 State를 반환한다.**
이것이 LangGraph의 핵심 계약(contract)이다.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# State 정의: 모든 Node가 공유하는 데이터
class WorkflowState(TypedDict):
    query: str
    search_results: list[str]
    analysis: str
    final_answer: str
    retry_count: int

# Node 정의: State → State
def search_node(state: WorkflowState) -> dict:
    results = do_search(state["query"])
    return {"search_results": results}

def analyze_node(state: WorkflowState) -> dict:
    analysis = do_analysis(state["search_results"])
    return {"analysis": analysis}

def generate_node(state: WorkflowState) -> dict:
    answer = do_generate(state["analysis"])
    return {"final_answer": answer}

# 그래프 조립
graph = StateGraph(WorkflowState)
graph.add_node("search", search_node)
graph.add_node("analyze", analyze_node)
graph.add_node("generate", generate_node)

graph.set_entry_point("search")
graph.add_edge("search", "analyze")
graph.add_edge("analyze", "generate")
graph.add_edge("generate", END)

app = graph.compile()
```

### State 설계 원칙

State는 TypedDict 또는 Pydantic 모델로 정의한다.
불변(immutable) 업데이트를 기본으로 한다.
`Annotated`를 사용해 리스트 필드의 병합(merge) 방식을 지정한다.

```python
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    # 단순 덮어쓰기 필드
    query: str
    status: str

    # 리스트 누적 필드 (add: 기존 값에 새 값 추가)
    messages: Annotated[list, operator.add]
    tool_calls: Annotated[list, operator.add]

    # 카운터 (누적 합산)
    retry_count: Annotated[int, operator.add]
```

**왜 Annotated가 필요한가?**
병렬 Node가 동시에 State를 업데이트할 때 충돌을 방지한다.
`operator.add`는 "이 필드는 합산하라"는 의미다.

---

## Workflow vs Agent

Workflow는 흐름이 코드로 고정된 구조다.
Agent는 LLM이 스스로 흐름을 결정하는 구조다.
대부분의 실무 시스템은 Workflow와 Agent를 혼합한다.

![Workflow vs Agent](https://mintcdn.com/langchain-5e9cc07a/-_xGPoyjhyiDWTPJ/oss/images/agent_workflow.png?fit=max&auto=format&n=-_xGPoyjhyiDWTPJ&q=85&s=c217c9ef517ee556cae3fc928a21dc55)

### 5가지 워크플로 패턴

LangGraph 공식 문서에서 정의하는 핵심 패턴이다.

**Prompt Chaining** — LLM 호출을 순차 연결. 이전 출력이 다음 입력이 된다.

![Prompt Chaining](https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/prompt_chain.png?fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=762dec147c31b8dc6ebb0857e236fc1f)

**Parallelization** — 독립적인 작업을 동시에 실행. `Send()` API 활용.

![Parallelization](https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/parallelization.png?fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=8afe3c427d8cede6fed1e4b2a5107b71)

**Routing** — 입력을 분류하여 전문 경로로 분기. `add_conditional_edges` 활용.

![Routing](https://mintcdn.com/langchain-5e9cc07a/dL5Sn6Cmy9pwtY0V/oss/images/routing.png?fit=max&auto=format&n=dL5Sn6Cmy9pwtY0V&q=85&s=272e0e9b681b89cd7d35d5c812c50ee6)

**Orchestrator-Worker** — 오케스트레이터가 태스크를 분해, 워커에게 위임 후 결과 통합.

![Orchestrator-Worker](https://mintcdn.com/langchain-5e9cc07a/ybiAaBfoBvFquMDz/oss/images/worker.png?fit=max&auto=format&n=ybiAaBfoBvFquMDz&q=85&s=2e423c67cd4f12e049cea9c169ff0676)

**Evaluator-Optimizer** — 생성 LLM + 평가 LLM이 품질 기준 달성까지 반복 개선.

![Evaluator-Optimizer](https://mintcdn.com/langchain-5e9cc07a/-_xGPoyjhyiDWTPJ/oss/images/evaluator_optimizer.png?fit=max&auto=format&n=-_xGPoyjhyiDWTPJ&q=85&s=9bd0474f42b6040b14ed6968a9ab4e3c)

### Agent 패턴 — Tool-Calling Loop

Agent는 LLM이 스스로 도구 선택과 실행 순서를 결정한다.
연속 피드백 루프로 동작하며, `create_react_agent`가 이 패턴을 구현한다.

![Agent Pattern](https://mintcdn.com/langchain-5e9cc07a/-_xGPoyjhyiDWTPJ/oss/images/agent.png?fit=max&auto=format&n=-_xGPoyjhyiDWTPJ&q=85&s=bd8da41dbf8b5e6fc9ea6bb10cb63e38)

> **출처**: [LangGraph 공식 문서 — Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

---

## Conditional 분기 설계

### 기본 Conditional Edge

```python
def should_retry(state: WorkflowState) -> str:
    """분기 함수: 반환값이 다음 Node 이름"""
    if state["retry_count"] >= 3:
        return "fail"
    if not state["search_results"]:
        return "retry"
    return "analyze"

graph.add_conditional_edges(
    "search",                        # 이 Node 이후에 분기
    should_retry,                    # 분기 함수
    {
        "analyze": "analyze",        # 반환값 → Node 이름
        "retry": "search",           # 재시도: search로 돌아감
        "fail": END,                 # 종료
    }
)
```

### 복잡한 분기 패턴

```python
def route_by_complexity(state: WorkflowState) -> str:
    """쿼리 복잡도에 따라 다른 처리 경로 선택"""
    query = state["query"]

    if len(query.split()) < 5:
        return "simple_handler"      # 단순 쿼리
    elif "코드" in query or "분석" in query:
        return "code_handler"        # 코드 관련
    else:
        return "complex_handler"     # 복잡 쿼리

graph.add_conditional_edges(
    "classify",
    route_by_complexity,
    {
        "simple_handler": "simple_node",
        "code_handler": "code_node",
        "complex_handler": "complex_node",
    }
)
```

---

## Retry/Fallback 전략

### 재시도 패턴

```python
def search_with_retry(state: WorkflowState) -> dict:
    """실패 시 재시도 횟수를 State에 기록"""
    try:
        results = external_search_api(state["query"])
        return {
            "search_results": results,
            "retry_count": 0,        # 성공 시 리셋
            "last_error": None,
        }
    except Exception as e:
        return {
            "search_results": [],
            "retry_count": 1,        # Annotated[int, operator.add]이므로 누적됨
            "last_error": str(e),
        }

def decide_after_search(state: WorkflowState) -> str:
    if state["search_results"]:
        return "analyze"
    if state["retry_count"] < 3:
        return "search"              # 재시도
    return "fallback"               # Fallback으로 전환

def fallback_node(state: WorkflowState) -> dict:
    """외부 검색 실패 시 LLM 내부 지식으로 답변"""
    answer = llm_answer_from_knowledge(state["query"])
    return {
        "final_answer": f"[Fallback] {answer}",
        "status": "fallback_used",
    }
```

### Fallback 체인 패턴

```
[Primary Tool] → 실패 → [Secondary Tool] → 실패 → [LLM Fallback] → [결과]
```

```python
TOOL_PRIORITY = ["search_api_v2", "search_api_v1", "llm_knowledge"]

def fallback_chain_node(state: WorkflowState) -> dict:
    tried = state.get("tried_tools", [])

    for tool_name in TOOL_PRIORITY:
        if tool_name in tried:
            continue
        try:
            result = TOOLS[tool_name](state["query"])
            return {"search_results": result, "tried_tools": [tool_name]}
        except Exception:
            tried.append(tool_name)

    return {"search_results": [], "status": "all_tools_failed"}
```

---

## State Propagation 방식

### State는 어떻게 전달되는가

LangGraph는 각 Node 실행 후 **반환된 dict를 현재 State에 병합**한다.
반환하지 않은 필드는 이전 값이 유지된다.
이것이 LangGraph의 불변성(immutability) 보장 방식이다.

```
Initial State:
  {query: "AI 뉴스", results: [], analysis: "", retry: 0}

After search_node returns {results: ["뉴스1", "뉴스2"]}:
  {query: "AI 뉴스", results: ["뉴스1", "뉴스2"], analysis: "", retry: 0}
                          ↑ 업데이트됨              ↑ 유지됨

After analyze_node returns {analysis: "요약: ..."}:
  {query: "AI 뉴스", results: ["뉴스1", "뉴스2"], analysis: "요약: ...", retry: 0}
```

### 병렬 Node와 State 병합

`Send` API를 사용하면 병렬 실행이 가능하다.

```python
from langgraph.types import Send

def dispatch_parallel(state: WorkflowState):
    """각 URL에 대해 병렬로 fetch Node 실행"""
    return [
        Send("fetch_node", {"url": url, "original_query": state["query"]})
        for url in state["urls"]
    ]

graph.add_conditional_edges("search", dispatch_parallel)
```

---

## 비교: 제어 흐름 구현 방법

| 방법 | 장점 | 단점 | 적합한 경우 |
|------|------|------|------------|
| **순수 코드** | 단순함, 의존성 없음 | 복잡 흐름 관리 어려움 | 2단계 이하 |
| **LangGraph** | 시각화, 상태 추적, 체크포인트 | 러닝커브 | 3단계 이상 |
| **Celery/Prefect** | 분산 실행, 스케줄링 | 무거움 | 대규모 배치 |
| **직접 State Machine** | 완전한 제어 | 구현 비용 높음 | 특수 요구사항 |

> **선택 기준**: 프로덕션 Agent라면 LangGraph가 현재(2026) 최선

---

## 주의사항

### 1. State를 과도하게 설계하지 않는다

처음부터 모든 필드를 넣으려 하면 복잡해진다.
필요한 필드만 추가하고, 나중에 확장한다.
State 필드가 10개를 넘으면 설계를 재검토한다.

### 2. Node 안에서 다음 Node를 결정하지 않는다

Node는 데이터를 처리하는 역할만 한다.
흐름 결정은 반드시 Edge(conditional edge)에서 한다.
이 분리가 없으면 그래프가 테스트 불가능해진다.

### 3. 무한 루프에 반드시 탈출 조건을 추가한다

재시도 루프에는 항상 최대 횟수를 State에 기록한다.
`retry_count >= MAX_RETRY`면 강제 종료 Edge로 연결한다.

### 4. 체크포인트를 활용한다

LangGraph는 SqliteSaver, PostgresSaver로 State를 영속화할 수 있다.
장시간 실행 Agent는 중간에 실패해도 재개가 가능하다.

```python
from langgraph.checkpoint.sqlite import SqliteSaver

with SqliteSaver.from_conn_string(":memory:") as memory:
    app = graph.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "session-001"}}
    result = app.invoke(initial_state, config=config)
```

---

## 코드 예제: 전체 LangGraph 워크플로우

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# ── State 정의 ──────────────────────────────────
class ResearchState(TypedDict):
    query: str
    search_results: list[str]
    is_sufficient: bool
    final_report: str
    messages: Annotated[list[str], operator.add]
    retry_count: Annotated[int, operator.add]

# ── Nodes ────────────────────────────────────────
def search_node(state: ResearchState) -> dict:
    print(f"[search] 검색 중: {state['query']}")
    # 실제로는 외부 API 호출
    results = [f"결과_{i}" for i in range(3)]
    return {
        "search_results": results,
        "messages": [f"검색 완료: {len(results)}건"],
    }

def evaluate_node(state: ResearchState) -> dict:
    results = state["search_results"]
    is_sufficient = len(results) >= 2
    return {
        "is_sufficient": is_sufficient,
        "messages": [f"평가: {'충분' if is_sufficient else '부족'}"],
    }

def report_node(state: ResearchState) -> dict:
    report = f"# 조사 보고서\n\n쿼리: {state['query']}\n\n"
    report += "\n".join(f"- {r}" for r in state["search_results"])
    return {"final_report": report}

def fallback_node(state: ResearchState) -> dict:
    return {
        "final_report": f"[Fallback] {state['query']}에 대한 충분한 정보를 찾지 못했습니다.",
        "messages": ["Fallback 사용됨"],
    }

# ── 분기 함수 ────────────────────────────────────
def after_evaluate(state: ResearchState) -> str:
    if state["is_sufficient"]:
        return "report"
    if state["retry_count"] < 2:
        return "search"    # 재시도
    return "fallback"

# ── 그래프 조립 ──────────────────────────────────
def build_research_graph():
    g = StateGraph(ResearchState)

    g.add_node("search", search_node)
    g.add_node("evaluate", evaluate_node)
    g.add_node("report", report_node)
    g.add_node("fallback", fallback_node)

    g.set_entry_point("search")
    g.add_edge("search", "evaluate")
    g.add_conditional_edges(
        "evaluate",
        after_evaluate,
        {"report": "report", "search": "search", "fallback": "fallback"},
    )
    g.add_edge("report", END)
    g.add_edge("fallback", END)

    return g.compile()

# ── 실행 ─────────────────────────────────────────
if __name__ == "__main__":
    app = build_research_graph()
    result = app.invoke({
        "query": "2026년 AI Agent 트렌드",
        "search_results": [],
        "is_sufficient": False,
        "final_report": "",
        "messages": [],
        "retry_count": 0,
    })
    print(result["final_report"])
    print("\n--- 실행 로그 ---")
    for msg in result["messages"]:
        print(f"  {msg}")
```

---

## Q&A

**Q1. LangGraph의 Node는 반드시 dict를 반환해야 하나요?**

네, dict를 반환해야 합니다.
반환된 dict의 키-값이 State에 병합됩니다.
Pydantic 모델을 사용하는 경우 `.model_dump()`로 변환합니다.

**Q2. 분기 함수에서 반환할 수 있는 값의 타입은?**

문자열(str) 또는 문자열 리스트(list[str])입니다.
문자열이면 단일 경로, 리스트면 병렬 경로입니다.
`Send` 객체 리스트를 반환하면 동적 병렬 실행도 가능합니다.

**Q3. 체크포인트 없이 장시간 실행하면 어떤 위험이 있나요?**

프로세스가 중단되면 모든 State가 손실됩니다.
처음부터 다시 실행해야 합니다.
API 비용과 시간이 낭비됩니다.
프로덕션 Agent는 반드시 체크포인트를 사용하세요.

**Q4. State 필드에 `Annotated[list, operator.add]`를 쓰는 이유는?**

병렬 Node가 동시에 같은 리스트 필드를 업데이트할 때 데이터 손실을 방지합니다.
`operator.add` 없이는 마지막 Node의 값이 이전 값을 덮어씁니다.
누적이 필요한 로그, 메시지, 결과 목록에는 항상 사용하세요.

---

## 퀴즈

**Q1.** LangGraph에서 Node 함수의 올바른 시그니처는?

- A) `def node(query: str) -> str:`
- B) `def node(state: MyState) -> dict:`
- C) `def node(state: MyState, config: dict) -> MyState:`
- D) `def node(inputs: list) -> list:`

<details>
<summary>힌트 및 정답</summary>

**힌트**: Node는 State를 받아서 State의 일부(업데이트할 필드)를 반환합니다.

**정답**: B

Node는 전체 State를 받고, 업데이트할 필드만 담은 dict를 반환합니다. 반환된 dict가 기존 State에 병합됩니다. C도 가능한 형태이지만, 전체 State를 반환하는 것은 불필요한 오버헤드가 있습니다.
</details>

---

**Q2.** `Annotated[int, operator.add]`로 선언된 `retry_count` 필드에 `{"retry_count": 1}`을 반환하면 어떻게 되는가? 현재 값이 2일 때.

<details>
<summary>힌트 및 정답</summary>

**힌트**: `operator.add`는 덧셈 연산자입니다.

**정답**: 3이 된다 (2 + 1 = 3)

`operator.add`가 지정된 필드는 기존 값에 반환값이 **더해집니다**. 리스트라면 두 리스트가 연결(concatenate)됩니다. 정수라면 합산됩니다.
</details>

---

**Q3.** Conditional Edge의 분기 함수가 `"analyze"`를 반환했는데 매핑에 해당 키가 없다면?

<details>
<summary>힌트 및 정답</summary>

**힌트**: LangGraph는 반환값을 매핑 dict에서 찾아 다음 Node를 결정합니다.

**정답**: 런타임 에러 발생

매핑 dict에 없는 키를 반환하면 LangGraph가 다음 Node를 찾지 못해 에러가 발생합니다. 분기 함수의 모든 가능한 반환값이 매핑에 포함되어야 합니다.
</details>

---

**Q4.** 다음 중 Node에서 하면 안 되는 것은?

- A) 외부 API 호출
- B) State 데이터 가공
- C) 다음에 실행할 Node를 직접 결정
- D) LLM 호출

<details>
<summary>힌트 및 정답</summary>

**힌트**: Node의 역할과 Edge의 역할을 구분하세요.

**정답**: C

흐름 결정(다음 Node 선택)은 Edge(conditional edge)의 역할입니다. Node가 흐름을 직접 결정하면 그래프 구조가 무의미해지고 테스트가 불가능해집니다.
</details>

---

**Q5.** LangGraph 체크포인트의 주요 이점은?

<details>
<summary>힌트 및 정답</summary>

**힌트**: 장시간 실행되는 Agent가 중간에 실패하면 어떻게 될까요?

**정답**: 중간 State를 영속화하여 실패 후 재개(resume)가 가능하다

체크포인트는 각 Step 후 State를 저장합니다. 프로세스가 중단되어도 마지막 저장된 지점부터 재시작할 수 있습니다. API 비용과 시간을 절약하고 안정성을 높입니다.
</details>

---

## 실습

<callout icon="💡" color="gray_bg">
	이 세션의 실습은 `labs/day2/01_langgraph_workflows/` 노트북을 사용한다.
	Graph API로 워크플로를 직접 구현하고 5가지 패턴을 실행한다.
</callout>

### 🔍 I DO: Graph API 기초 {toggle="true"}
	**시간**: 30분
	**노트북**: `01_langgraph_workflows/01_graph_api.ipynb`

	강사가 라이브로 StateGraph를 만들고 실행한다.
	- State 정의 (TypedDict + Annotated)
	- Node 구현 → Edge 연결 → compile → invoke
	- 조건 분기 (add_conditional_edges)
	- 재시도 루프 구현
	<callout icon="💡" color="gray_bg">
		**관찰 포인트**: Node가 반환한 dict가 State에 어떻게 병합되는지 확인한다.
	</callout>

### 🤝 WE DO: 워크플로 패턴 실습 {toggle="true"}
	**시간**: 40분
	**노트북**: `01_langgraph_workflows/02_workflows.ipynb`

	5가지 워크플로 패턴을 함께 실행하고 구조를 분석한다.
	- [ ] Prompt Chaining — 순차 실행
	- [ ] Parallelization — Send()로 병렬 실행
	- [ ] Routing — 조건부 분기로 경로 선택
	- [ ] Orchestrator-Worker — 동적 워커 생성
	- [ ] Evaluator-Optimizer — 반복 개선 루프

### 🚀 YOU DO: 워크플로 설계 {toggle="true"}
	**시간**: 20분

	<callout icon="📋" color="yellow_bg">
		**요구사항**
		1. 본인 업무에 적합한 워크플로 패턴 1개를 선택한다
		2. State, Node, Edge를 정의하고 그래프를 구성한다
		3. 재시도 로직과 무한 루프 탈출 조건을 포함한다
	</callout>

<details>
<summary>💡 힌트</summary>
	워크플로 패턴 선택 기준: 순차 처리 → Chaining, 독립 병렬 → Parallelization, 조건 분기 → Routing
</details>
