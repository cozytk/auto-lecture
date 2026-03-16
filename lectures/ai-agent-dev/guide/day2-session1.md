# Session 1: Agent 4요소 구조 설계

## 학습 목표
1. Agent를 구성하는 4요소(Goal, Memory, Tool, Control Logic)의 역할과 상호작용을 설명할 수 있다
2. Planner-Executor 패턴을 이해하고 Sub-task 분해 전략을 설계할 수 있다
3. Single-step Agent와 Multi-step Agent의 차이를 판단하고 적절한 구조를 선택할 수 있다

---

## 1. Agent 4요소 개요: Goal, Memory, Tool, Control Logic

### 개념 설명

AI Agent는 단순한 LLM 호출과 달리 **목표를 가지고 자율적으로 행동**하는 시스템이다. ChatGPT에 질문을 던지고 답변을 받는 것은 "1회성 입출력 함수 호출"에 불과하다. 반면 Agent는 스스로 다음에 무엇을 해야 할지 판단하고, 필요한 도구를 선택하며, 중간 결과를 기억하면서 목표를 향해 반복적으로 행동한다. 이 차이를 만드는 핵심 구성 요소가 바로 4가지다.

**왜 이 4요소 프레임워크가 등장했는가?** 2023년 이후 LLM 기반 자율 시스템을 설계하려는 시도가 폭발적으로 증가하면서, 연구자와 엔지니어들은 "잘 동작하는 Agent"와 "실패하는 Agent"를 구분짓는 공통 패턴을 발견했다. AutoGPT, BabyAGI, HuggingGPT 같은 초기 Agent 프로젝트들이 보여준 교훈은 명확했다. 목표 없이 방황하는 Agent, 이전 시도를 기억하지 못해 같은 실수를 반복하는 Agent, 도구를 사용하지 못해 "생각만 하는" Agent, 다음 행동을 결정하지 못해 무한 루프에 빠지는 Agent -- 이 모든 실패 유형이 4가지 요소 중 하나 이상이 결여되어 있었다.

이 4요소를 현실 세계에 비유하면 이해가 쉽다. **Goal**은 팀의 미션 스테이트먼트다. "이번 분기 매출 20% 성장"이라는 목표가 없으면 팀원들은 무엇을 해야 할지 모른다. **Memory**는 팀의 공유 지식 베이스이자 회의록이다. 지난 회의에서 무엇을 결정했는지, 어떤 데이터를 이미 수집했는지 기록하지 않으면 매번 처음부터 시작해야 한다. **Tool**은 팀원들이 사용하는 실무 도구(Slack, Jira, 데이터베이스, 이메일)다. 아무리 똑똑한 팀이라도 도구 없이는 실행력이 제로다. **Control Logic**은 프로젝트 매니저의 판단력이다. "이 데이터가 충분한가?", "다음에 어떤 도구를 써야 하는가?", "이제 멈춰야 하는가?"를 결정하는 두뇌 역할을 한다.

학계에서는 이와 유사한 구조가 여러 프레임워크로 제안되어 왔다. ReAct(Reasoning + Acting)는 추론과 행동을 번갈아 수행하며, LATS(Language Agent Tree Search)는 트리 탐색 기반으로 최적 행동 경로를 찾는다. Reflexion은 자기 반성 메커니즘을 추가하여 이전 실패로부터 학습한다. 이들 모두 결국 "목표 설정 -> 맥락 기억 -> 도구 사용 -> 다음 행동 결정"이라는 공통 골격을 공유하며, 이것이 곧 Goal-Memory-Tool-Control Logic 4요소 프레임워크의 본질이다.

| 요소 | 역할 | 예시 |
|------|------|------|
| **Goal** | Agent가 달성해야 할 목표 정의 | "사용자 질문에 대해 DB를 조회하여 정확한 답변 제공" |
| **Memory** | 과거 상호작용과 중간 결과 저장 | 대화 히스토리, 이전 Tool 호출 결과, 작업 상태 |
| **Tool** | 외부 세계와 상호작용하는 도구 | API 호출, DB 조회, 파일 읽기/쓰기, 웹 검색 |
| **Control Logic** | 다음 행동을 결정하는 제어 로직 | 조건 분기, 반복, 종료 조건, 에러 처리 |

```
+-----------------------------------------+
|                 Agent                    |
|                                          |
|   +----------+     +--------------+     |
|   |   Goal   |---->|Control Logic |     |
|   +----------+     +------+-------+     |
|                           |              |
|                    +------+------+       |
|                    v             v       |
|              +----------+ +----------+  |
|              |  Memory  | |   Tool   |  |
|              +----------+ +----------+  |
+-----------------------------------------+
```

실무에서 주의할 점은 4요소의 **균형**이다. Goal이 지나치게 추상적이면 Agent가 방향을 잡지 못하고, 지나치게 구체적이면 유연성을 잃는다. Memory에 모든 것을 저장하면 context window를 초과하고, 너무 적게 저장하면 맥락을 잃는다. Tool이 너무 많으면 LLM이 올바른 Tool을 선택하지 못하고, 너무 적으면 실행 능력이 제한된다. Control Logic이 복잡하면 디버깅이 어렵고, 단순하면 예외 상황에 대처하지 못한다. 이 균형을 잡는 것이 Agent 설계의 핵심 역량이다.

다음 코드에서는 이 4요소를 LangGraph의 `TypedDict` State로 명시적으로 모델링하여, Agent의 동작을 투명하고 추적 가능하게 만드는 방법을 보여준다.

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """Agent 4요소를 State로 모델링"""
    # Goal: 사용자가 달성하고자 하는 목표
    goal: str
    # Memory: 대화 히스토리 (누적)
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Tool: 사용 가능한 도구 목록
    available_tools: list[str]
    # Control Logic: 현재 단계와 반복 횟수
    current_step: str
    iteration_count: int
    max_iterations: int


# 초기 상태 예시
initial_state: AgentState = {
    "goal": "사용자 질문에 대해 정확한 답변 제공",
    "messages": [],
    "available_tools": ["search_db", "calculate", "web_search"],
    "current_step": "plan",
    "iteration_count": 0,
    "max_iterations": 5,
}

print(f"Goal: {initial_state['goal']}")
print(f"Available Tools: {initial_state['available_tools']}")
print(f"Current Step: {initial_state['current_step']}")
```

**실행 결과:**
```
Goal: 사용자 질문에 대해 정확한 답변 제공
Available Tools: ['search_db', 'calculate', 'web_search']
Current Step: plan
```

### Q&A

**Q: 왜 LLM만으로는 Agent가 아닌가요?**
A: LLM은 단일 입출력 함수다. 목표를 설정하고, 중간 결과를 기억하며, 외부 도구를 사용하고, 다음 행동을 스스로 결정하는 제어 루프가 있어야 비로소 Agent라 할 수 있다. 핵심은 **자율적 의사결정 루프**의 존재 여부다.

**Q: Memory는 단순 대화 히스토리와 어떻게 다른가요?**
A: 대화 히스토리는 Memory의 한 부분이다. Agent Memory에는 대화 히스토리 외에도 작업 상태(어떤 step까지 완료했는지), Tool 호출 결과 캐시, 이전 판단의 근거 등이 포함된다. LangGraph에서는 이를 `State`에 명시적으로 모델링한다.

<details>
<summary>퀴즈: Agent 4요소 중 "다음에 어떤 Tool을 호출할지"를 결정하는 요소는?</summary>

**힌트**: 조건 분기, 반복, 종료 조건 등을 담당하는 요소를 생각해보세요.

**정답**: **Control Logic**. Goal이 방향을 제시하고, Memory가 맥락을 제공하며, Tool이 실행 수단이라면, Control Logic은 이 모든 정보를 종합하여 다음 행동을 결정하는 두뇌 역할을 한다.
</details>

---

## 2. Planner-Executor 구조 설계

### 개념 설명

복잡한 작업을 처리하는 Agent는 **계획(Plan)과 실행(Execute)을 분리**하는 것이 효과적이다. 이것이 Planner-Executor 패턴이다.

**이 패턴이 왜 필요한가?** 인간이 복잡한 프로젝트를 수행할 때를 생각해보자. "경쟁사 분석 보고서를 작성해라"라는 지시를 받으면, 우리는 바로 글을 쓰기 시작하지 않는다. 먼저 무엇을 조사해야 하는지 계획을 세우고, 각 조사 항목을 하나씩 실행하며, 중간 결과에 따라 계획을 수정한다. Agent도 마찬가지다. LLM에게 복잡한 요청을 한 번에 처리하라고 하면, context window 한계, 환각(hallucination), 누락 등의 문제가 빈번하게 발생한다. 계획과 실행을 분리하면 이 문제를 구조적으로 해결할 수 있다.

Planner-Executor 패턴의 핵심 가치는 **관심사의 분리(Separation of Concerns)**에 있다. Planner는 "무엇을 해야 하는가"에 집중하고, Executor는 "어떻게 실행하는가"에 집중한다. 이 분리 덕분에 각각을 독립적으로 개선할 수 있다. 예를 들어, Planner의 계획 품질이 떨어지면 프롬프트를 개선하거나 더 강력한 모델을 사용하면 되고, Executor의 실행 속도가 느리면 병렬 처리를 도입하면 된다. 둘이 결합되어 있으면 어디를 고쳐야 하는지 파악하기 어렵다.

이 패턴에서 가장 중요한 것은 **피드백 루프(Re-planning)**다. 현실 세계에서 계획대로 일이 진행되는 경우는 드물다. DB에 예상한 데이터가 없거나, API 호출이 실패하거나, 중간 결과가 예상과 다를 수 있다. 이때 Executor의 실행 결과를 Planner에게 피드백하여 계획을 수정하는 메커니즘이 없으면, Agent는 잘못된 계획을 끝까지 수행하다가 의미 없는 결과를 생성한다. 반면 Re-planning이 잘 설계되면, Agent는 마치 숙련된 프로젝트 매니저처럼 상황 변화에 유연하게 대응할 수 있다.

실무에서 이 패턴을 적용할 때 주의할 점이 있다. 첫째, Planner가 생성하는 sub-task의 granularity(세분화 수준)가 적절해야 한다. 너무 세분화하면 LLM 호출 비용이 증가하고, 너무 추상적이면 Executor가 실행할 수 없다. 둘째, Re-planning의 빈도를 조절해야 한다. 매 step마다 Re-planning을 하면 비용이 폭증하고, 전혀 하지 않으면 유연성을 잃는다. 일반적으로 "Executor가 실패하거나 예상 외 결과를 반환했을 때"만 Re-planning을 트리거하는 것이 실용적이다.

```
+-----------+     +------------+     +-----------+
|   User    |---->|  Planner   |---->| Executor  |
|  Request  |     | (Sub-task  |     | (각 task  |
|           |     |  분해)     |     |  실행)    |
+-----------+     +------------+     +-----+-----+
                       ^                    |
                       |    결과 피드백      |
                       +--------------------+
```

- **Planner**: 사용자 요청을 분석하여 실행 가능한 Sub-task 목록으로 분해
- **Executor**: 각 Sub-task를 순차/병렬로 실행하고 결과를 Planner에 피드백
- **피드백 루프**: 실행 결과를 바탕으로 계획을 수정 (Re-planning)

다음 코드는 이 패턴을 LangGraph StateGraph로 구현한 예시다. Planner가 sub-task 목록을 생성하면 Executor가 순차적으로 실행하고, 모든 task가 완료되면 종료하는 흐름을 보여준다.

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import operator


class PlanExecuteState(TypedDict):
    """Planner-Executor 패턴의 State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    plan: list[str]           # Planner가 생성한 sub-task 목록
    current_task_index: int   # 현재 실행 중인 task 인덱스
    results: list[str]        # 각 task의 실행 결과
    is_complete: bool


def planner_node(state: PlanExecuteState) -> dict:
    """사용자 요청을 sub-task로 분해한다."""
    user_message = state["messages"][-1].content

    # 실제로는 LLM을 호출하여 계획을 생성한다
    # 여기서는 데모를 위해 하드코딩
    plan = [
        "1단계: 사용자 의도 파악",
        "2단계: 필요한 데이터 조회",
        "3단계: 결과 종합 및 응답 생성",
    ]
    print(f"[Planner] 계획 수립 완료: {len(plan)}개 sub-task")
    for task in plan:
        print(f"  - {task}")

    return {"plan": plan, "current_task_index": 0, "results": []}


def executor_node(state: PlanExecuteState) -> dict:
    """현재 sub-task를 실행한다."""
    idx = state["current_task_index"]
    task = state["plan"][idx]

    # 실제로는 Tool 호출이나 LLM 추론을 수행한다
    result = f"[완료] {task} -> 성공"
    print(f"[Executor] {result}")

    new_results = list(state["results"]) + [result]
    return {
        "results": new_results,
        "current_task_index": idx + 1,
    }


def should_continue(state: PlanExecuteState) -> str:
    """모든 task가 완료되었는지 확인한다."""
    if state["current_task_index"] >= len(state["plan"]):
        return "complete"
    return "continue"


def finish_node(state: PlanExecuteState) -> dict:
    """최종 결과를 정리한다."""
    summary = "\n".join(state["results"])
    print(f"\n[Finish] 모든 작업 완료:\n{summary}")
    return {
        "is_complete": True,
        "messages": [AIMessage(content=f"작업 완료:\n{summary}")],
    }


# 그래프 구성
workflow = StateGraph(PlanExecuteState)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("finish", finish_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")
workflow.add_conditional_edges(
    "executor",
    should_continue,
    {"continue": "executor", "complete": "finish"},
)
workflow.add_edge("finish", END)

app = workflow.compile()

# 실행
result = app.invoke({
    "messages": [HumanMessage(content="최근 매출 데이터를 분석해줘")],
    "plan": [],
    "current_task_index": 0,
    "results": [],
    "is_complete": False,
})
```

**실행 결과:**
```
[Planner] 계획 수립 완료: 3개 sub-task
  - 1단계: 사용자 의도 파악
  - 2단계: 필요한 데이터 조회
  - 3단계: 결과 종합 및 응답 생성
[Executor] [완료] 1단계: 사용자 의도 파악 -> 성공
[Executor] [완료] 2단계: 필요한 데이터 조회 -> 성공
[Executor] [완료] 3단계: 결과 종합 및 응답 생성 -> 성공

[Finish] 모든 작업 완료:
[완료] 1단계: 사용자 의도 파악 -> 성공
[완료] 2단계: 필요한 데이터 조회 -> 성공
[완료] 3단계: 결과 종합 및 응답 생성 -> 성공
```

### Q&A

**Q: 모든 Agent에 Planner-Executor 패턴이 필요한가요?**
A: 아니다. 단순한 Q&A Agent나 단일 Tool만 호출하는 Agent에는 오히려 과잉 설계다. 이 패턴은 **복수의 단계를 순차적으로 실행해야 하거나**, **중간 실패 시 계획을 수정해야 하는** 복잡한 시나리오에 적합하다.

<details>
<summary>퀴즈: Planner-Executor 패턴에서 Re-planning이 필요한 상황은?</summary>

**힌트**: Executor가 특정 sub-task를 실행했을 때, 예상과 다른 결과가 나오면 어떻게 해야 할까요?

**정답**: Executor의 실행 결과가 예상과 다르거나, Tool 호출이 실패하거나, 새로운 정보가 발견되어 기존 계획이 유효하지 않을 때 Re-planning이 필요하다. 예: DB 조회 결과 데이터가 없어서 외부 API로 전환해야 하는 경우.
</details>

---

## 3. Sub-task 분해 전략

### 개념 설명

효과적인 Agent는 복잡한 요청을 **실행 가능한 단위(Sub-task)**로 분해한다. 분해 품질이 Agent 성능을 좌우한다.

**왜 Sub-task 분해가 중요한가?** LLM의 가장 큰 한계 중 하나는 "한 번에 처리할 수 있는 복잡도의 상한"이다. 연구에 따르면 LLM은 단일 프롬프트로 3~4단계 이상의 추론 체인을 안정적으로 수행하기 어렵다. 복잡한 작업을 작은 단위로 분해하면, 각 단계에서 LLM이 집중해야 할 범위가 줄어들어 정확도가 크게 향상된다. 이것은 인간이 복잡한 수학 문제를 풀 때 한 번에 답을 구하지 않고 중간 단계를 나눠 푸는 것과 같은 원리다.

Sub-task 분해에는 세 가지 핵심 전략이 있으며, 작업의 특성에 따라 적절한 전략을 선택해야 한다. **순차 분해**는 이전 단계의 출력이 다음 단계의 입력이 되는 파이프라인 형태로, 데이터 처리나 문서 작성 같은 작업에 적합하다. **병렬 분해**는 독립적인 작업들을 동시에 수행하여 전체 실행 시간을 단축하는 전략으로, 여러 소스에서 데이터를 수집하는 작업에 효과적이다. **계층적 분해**는 큰 작업을 하위 작업으로 재귀적으로 분해하는 방식으로, 복잡도가 매우 높은 프로젝트에 사용한다.

실무에서 분해 품질을 결정짓는 핵심 요소는 **의존성 그래프**다. 각 sub-task 간의 의존 관계를 명확히 파악해야 어떤 task를 병렬로 실행할 수 있고, 어떤 순서로 실행해야 하는지 결정할 수 있다. 의존성을 잘못 파악하면 불필요하게 순차 실행하여 시간을 낭비하거나, 필요한 데이터 없이 실행하여 오류가 발생한다. 또한 sub-task의 적정 개수는 **3~7개**가 경험적으로 좋다. 이 범위를 벗어나면 관리 복잡도가 증가하거나 분해가 불충분해진다.

**분해 전략 3가지:**

| 전략 | 설명 | 적합한 상황 |
|------|------|------------|
| **순차 분해** | 단계별로 의존성 있는 task 나열 | 이전 결과가 다음 입력이 되는 경우 |
| **병렬 분해** | 독립적인 task를 동시 실행 | 서로 의존하지 않는 작업들 |
| **계층적 분해** | 큰 task를 하위 task로 재귀 분해 | 복잡도가 매우 높은 작업 |

다음 코드는 "경쟁사 분석 보고서 작성"이라는 복잡한 요청을 Sub-task로 분해하고, 각 task의 의존 관계와 실행 전략을 명시적으로 모델링하는 예시다.

```python
from typing import TypedDict, Literal
from dataclasses import dataclass


@dataclass
class SubTask:
    """실행 가능한 단위 작업"""
    id: str
    description: str
    tool_needed: str | None
    depends_on: list[str]  # 의존하는 task ID 목록
    strategy: Literal["sequential", "parallel", "hierarchical"]


def decompose_request(request: str) -> list[SubTask]:
    """사용자 요청을 Sub-task로 분해한다.

    실제 구현에서는 LLM을 호출하여 분해한다.
    여기서는 "경쟁사 분석 보고서 작성" 요청을 예시로 보여준다.
    """
    tasks = [
        SubTask(
            id="t1",
            description="경쟁사 목록 조회",
            tool_needed="db_query",
            depends_on=[],
            strategy="sequential",
        ),
        SubTask(
            id="t2a",
            description="경쟁사 A 매출 데이터 수집",
            tool_needed="web_search",
            depends_on=["t1"],
            strategy="parallel",
        ),
        SubTask(
            id="t2b",
            description="경쟁사 B 매출 데이터 수집",
            tool_needed="web_search",
            depends_on=["t1"],
            strategy="parallel",
        ),
        SubTask(
            id="t3",
            description="수집 데이터 비교 분석",
            tool_needed=None,  # LLM 추론만 사용
            depends_on=["t2a", "t2b"],
            strategy="sequential",
        ),
        SubTask(
            id="t4",
            description="보고서 생성",
            tool_needed="file_write",
            depends_on=["t3"],
            strategy="sequential",
        ),
    ]
    return tasks


# 분해 결과 시각화
tasks = decompose_request("경쟁사 분석 보고서 작성")
print("=== Sub-task 분해 결과 ===")
for task in tasks:
    deps = ", ".join(task.depends_on) if task.depends_on else "없음"
    tool = task.tool_needed or "LLM 추론"
    print(f"[{task.id}] {task.description}")
    print(f"     전략: {task.strategy} | 도구: {tool} | 의존: {deps}")
```

**실행 결과:**
```
=== Sub-task 분해 결과 ===
[t1] 경쟁사 목록 조회
     전략: sequential | 도구: db_query | 의존: 없음
[t2a] 경쟁사 A 매출 데이터 수집
     전략: parallel | 도구: web_search | 의존: t1
[t2b] 경쟁사 B 매출 데이터 수집
     전략: parallel | 도구: web_search | 의존: t1
[t3] 수집 데이터 비교 분석
     전략: sequential | 도구: LLM 추론 | 의존: t2a, t2b
[t4] 보고서 생성
     전략: sequential | 도구: file_write | 의존: t3
```

### Q&A

**Q: Sub-task를 너무 잘게 쪼개면 문제가 되나요?**
A: 그렇다. 과도한 분해는 LLM 호출 횟수를 증가시키고, 각 단계에서 context loss가 발생할 수 있다. 경험적으로 **3~7개 sub-task**가 적정하며, 단일 Tool 호출로 완료되는 수준이 이상적이다.

<details>
<summary>퀴즈: t2a와 t2b를 병렬로 실행할 수 있는 이유는?</summary>

**힌트**: 두 task의 `depends_on` 필드를 확인해보세요. 서로를 참조하고 있나요?

**정답**: t2a와 t2b는 모두 t1에만 의존하고, 서로에 대한 의존성이 없다. 따라서 t1 완료 후 두 task를 동시에 실행할 수 있다. 이것이 병렬 분해의 핵심 조건: **상호 의존성이 없는 task**.
</details>

---

## 4. Single-step vs Multi-step Agent 판단

### 개념 설명

Agent를 설계할 때 가장 먼저 결정해야 할 것은 **Single-step인가 Multi-step인가**이다.

**이 판단이 왜 중요한가?** Agent 개발에서 가장 흔한 실수는 두 가지 극단이다. 하나는 단순한 작업에 Multi-step Agent를 적용하여 불필요한 복잡성과 비용을 초래하는 것이고, 다른 하나는 복잡한 작업에 Single-step Agent를 고집하여 품질 저하와 실패를 겪는 것이다. 올바른 판단을 내리려면 "작업의 본질적 복잡도"를 정확히 파악해야 한다.

Single-step Agent는 **한 번의 LLM 호출과 0~1회의 Tool 호출**로 완료되는 단순한 구조다. "오늘 서울 날씨 알려줘"라는 요청은 날씨 API를 한 번 호출하고 결과를 정리하면 끝이다. 이런 작업에 Planner-Executor 패턴을 적용하면 오히려 응답 시간이 느려지고 비용만 증가한다. 반면 Multi-step Agent는 **여러 번의 LLM 호출과 Tool 호출**이 필요하며, 이전 단계의 결과에 따라 다음 행동이 달라지는 구조다. "AI Agent 시장을 분석하고 경쟁사 비교 보고서를 작성해줘"라는 요청은 검색, 데이터 수집, 분석, 보고서 작성이라는 여러 단계를 거쳐야 하며, 중간에 수집된 데이터에 따라 추가 검색이 필요할 수도 있다.

실무에서 권장하는 접근법은 **"Single-step 우선 원칙"**이다. 먼저 Single-step으로 구현하고, 다음 세 가지 신호가 나타나면 Multi-step으로 전환한다. (1) Tool 호출 결과에 따라 다른 Tool을 호출해야 하는 경우, (2) 한 번의 응답으로 사용자 요구를 충족할 수 없는 경우, (3) 중간 실패에 대한 대체 경로(Fallback)가 필요한 경우. 이 점진적 접근법은 YAGNI(You Aren't Gonna Need It) 원칙과도 부합한다. 처음부터 Multi-step으로 설계하면, 실제로는 필요하지 않은 복잡성을 도입하게 되는 경우가 많다.

| 구분 | Single-step Agent | Multi-step Agent |
|------|-------------------|------------------|
| **구조** | LLM 1회 호출 + Tool 0~1회 | LLM 여러 회 호출 + Tool 여러 회 |
| **제어 흐름** | 직선형 (Linear) | 루프/분기 (Graph) |
| **State 관리** | 불필요 또는 최소 | 필수 (State 누적) |
| **적합한 작업** | FAQ 응답, 단순 계산, 단일 조회 | 리서치, 데이터 분석, 복합 워크플로우 |
| **구현 복잡도** | 낮음 | 높음 |
| **실패 처리** | 단순 재시도 | Fallback, Re-planning |

**판단 기준 플로우차트:**

```
사용자 요청 도착
     |
     v
Tool 호출이 필요한가? --No--> 단순 LLM 응답 (Agent 불필요)
     | Yes
     v
Tool 호출이 1회로 충분한가? --Yes--> Single-step Agent
     | No
     v
이전 결과에 따라 다음 행동이 달라지는가? --No--> 병렬 Single-step
     | Yes
     v
Multi-step Agent
```

두 구조의 차이를 직접 비교해보자. 아래 코드에서 Single-step Agent는 단일 노드로 즉시 결과를 반환하고, Multi-step Agent는 수집-평가-종합이라는 루프를 반복하며 충분한 데이터가 모일 때까지 작업을 계속한다.

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import operator


# === Single-step Agent 예시 ===
class SingleStepState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    result: str


def single_step_agent(state: SingleStepState) -> dict:
    """단일 단계로 완료하는 Agent. Tool 1회 호출로 끝."""
    query = state["messages"][-1].content

    # Tool 호출 (단순 조회)
    result = f"'{query}'에 대한 답변: 42도입니다."  # 실제로는 Tool 호출
    print(f"[Single-step] 입력: {query}")
    print(f"[Single-step] 결과: {result}")
    return {
        "result": result,
        "messages": [AIMessage(content=result)],
    }


single_workflow = StateGraph(SingleStepState)
single_workflow.add_node("agent", single_step_agent)
single_workflow.set_entry_point("agent")
single_workflow.add_edge("agent", END)
single_app = single_workflow.compile()


# === Multi-step Agent 예시 ===
class MultiStepState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    step: str
    data_collected: list[str]
    iteration: int


def research_node(state: MultiStepState) -> dict:
    """정보 수집 단계"""
    iteration = state["iteration"]
    new_data = f"데이터_{iteration}: 관련 정보 발견"
    collected = list(state.get("data_collected", [])) + [new_data]
    print(f"[Multi-step] 수집 #{iteration}: {new_data}")
    return {
        "data_collected": collected,
        "iteration": iteration + 1,
        "step": "evaluate",
    }


def evaluate_node(state: MultiStepState) -> dict:
    """수집 결과 평가 -- 충분한지 판단"""
    count = len(state["data_collected"])
    print(f"[Multi-step] 평가: {count}개 데이터 수집됨")
    return {"step": "evaluate"}


def synthesize_node(state: MultiStepState) -> dict:
    """최종 답변 생성"""
    data = state["data_collected"]
    answer = f"총 {len(data)}개 데이터를 기반으로 종합 분석 완료"
    print(f"[Multi-step] 종합: {answer}")
    return {
        "messages": [AIMessage(content=answer)],
        "step": "done",
    }


def need_more_data(state: MultiStepState) -> str:
    """데이터가 충분한지 판단"""
    if len(state["data_collected"]) < 3:
        return "need_more"
    return "sufficient"


multi_workflow = StateGraph(MultiStepState)
multi_workflow.add_node("research", research_node)
multi_workflow.add_node("evaluate", evaluate_node)
multi_workflow.add_node("synthesize", synthesize_node)

multi_workflow.set_entry_point("research")
multi_workflow.add_edge("research", "evaluate")
multi_workflow.add_conditional_edges(
    "evaluate",
    need_more_data,
    {"need_more": "research", "sufficient": "synthesize"},
)
multi_workflow.add_edge("synthesize", END)
multi_app = multi_workflow.compile()

# 실행 비교
print("=== Single-step Agent ===")
single_app.invoke({
    "messages": [HumanMessage(content="오늘 서울 기온")],
    "result": "",
})

print("\n=== Multi-step Agent ===")
multi_app.invoke({
    "messages": [HumanMessage(content="AI Agent 시장 분석")],
    "step": "research",
    "data_collected": [],
    "iteration": 1,
})
```

**실행 결과:**
```
=== Single-step Agent ===
[Single-step] 입력: 오늘 서울 기온
[Single-step] 결과: '오늘 서울 기온'에 대한 답변: 42도입니다.

=== Multi-step Agent ===
[Multi-step] 수집 #1: 데이터_1: 관련 정보 발견
[Multi-step] 평가: 1개 데이터 수집됨
[Multi-step] 수집 #2: 데이터_2: 관련 정보 발견
[Multi-step] 평가: 2개 데이터 수집됨
[Multi-step] 수집 #3: 데이터_3: 관련 정보 발견
[Multi-step] 평가: 3개 데이터 수집됨
[Multi-step] 종합: 총 3개 데이터를 기반으로 종합 분석 완료
```

### Q&A

**Q: Single-step으로 시작했다가 Multi-step으로 전환해야 할 때는?**
A: 프로젝트 초기에는 Single-step으로 시작하는 것을 권장한다. 다음 신호가 나타나면 Multi-step으로 전환을 고려한다: (1) Tool 호출 결과에 따라 다른 Tool을 호출해야 하는 경우, (2) 한 번의 응답으로 사용자 요구를 충족할 수 없는 경우, (3) 중간 실패에 대한 대체 경로가 필요한 경우.

<details>
<summary>퀴즈: 다음 중 Multi-step Agent가 필요한 시나리오는?</summary>

**(a)** 현재 환율을 조회하여 알려주기
**(b)** 여러 뉴스 소스를 검색하고, 요약하고, 신뢰도를 평가하여 보고서 작성
**(c)** 사용자가 입력한 텍스트를 영어로 번역

**힌트**: 어떤 작업이 여러 단계의 Tool 호출과 중간 판단을 필요로 하나요?

**정답**: **(b)**. 뉴스 검색(Tool) -> 요약(LLM) -> 신뢰도 평가(LLM + Tool) -> 보고서 작성(Tool)으로 다단계 실행과 중간 결과 기반 판단이 필요하다. (a)와 (c)는 단일 Tool 호출 또는 단일 LLM 호출로 충분하므로 Single-step이 적합하다.
</details>

---

## 실습

### 실습 1: Agent 4요소 State 모델링
- **연관 학습 목표**: 학습 목표 1
- **실습 목적**: 실제 비즈니스 시나리오에 대해 Agent 4요소를 State로 모델링하는 연습
- **실습 유형**: 코드 작성
- **난이도**: 기초
- **예상 소요 시간**: 20분
- **선행 조건**: Python TypedDict 기본 이해
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
다음 시나리오에 대해 `AgentState`를 설계하세요.

> "고객 문의를 접수하면, FAQ DB를 검색하고, 답변이 없으면 담당자에게 에스컬레이션하는 고객 지원 Agent"

요구사항:
1. Goal, Memory, Tool, Control Logic 각각에 해당하는 필드를 정의할 것
2. FAQ 검색 결과와 에스컬레이션 여부를 State에 포함할 것
3. 최대 검색 횟수 제한을 State에 반영할 것

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator


class CustomerSupportState(TypedDict):
    """고객 지원 Agent의 State를 설계하세요."""
    # TODO: Goal 관련 필드
    # TODO: Memory 관련 필드
    # TODO: Tool 관련 필드
    # TODO: Control Logic 관련 필드
    pass
```

---

### 실습 2: Planner-Executor 그래프 구축
- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: Planner-Executor 패턴을 LangGraph StateGraph로 직접 구현
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 35분
- **선행 조건**: 실습 1 완료, LangGraph StateGraph 기본 이해
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
"여행 계획 Agent"를 Planner-Executor 패턴으로 구현하세요.

요구사항:
1. Planner Node: 여행지, 일정, 예산 정보를 기반으로 sub-task 분해
2. Executor Node: 각 sub-task를 순차적으로 실행 (실제 Tool 호출은 mock)
3. Conditional Edge: 모든 task 완료 시 종료, 아니면 다음 task 실행
4. Re-planning: Executor에서 실패한 task가 있으면 Planner로 돌아가 계획 수정

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
import operator


class TravelPlanState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    plan: list[str]
    current_task_index: int
    results: list[str]
    failed_tasks: list[str]
    replan_count: int


# TODO: planner_node 구현
# TODO: executor_node 구현
# TODO: should_continue 조건 함수 구현
# TODO: StateGraph 구성 및 실행
```

---

### 실습 3: Agent 구조 판단 워크시트
- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: 실제 비즈니스 시나리오에서 Single-step vs Multi-step 판단 능력 배양
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 25분
- **선행 조건**: 실습 1, 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
아래 5개 시나리오 각각에 대해 (1) Agent 유형 판단, (2) 이유, (3) State 스키마 초안을 작성하세요.

| # | 시나리오 | Agent 유형 | 이유 | State 핵심 필드 |
|---|----------|-----------|------|-----------------|
| 1 | Slack 메시지를 받으면 적절한 채널로 라우팅 | ? | ? | ? |
| 2 | 코드 리뷰 요청 시 보안/성능/스타일 다각도 분석 | ? | ? | ? |
| 3 | 주가 데이터를 조회하여 현재 가격 알려주기 | ? | ? | ? |
| 4 | 사용자 선호도 기반 맞춤 여행 일정 생성 | ? | ? | ? |
| 5 | PDF 문서에서 특정 조항을 찾아 요약 | ? | ? | ? |

판단 후, 시나리오 2 또는 4 중 하나를 골라 LangGraph `StateGraph`로 구현하세요.

---

## 핵심 정리
- Agent는 **Goal, Memory, Tool, Control Logic** 4요소로 구성된다
- LangGraph에서 4요소는 `TypedDict` State에 명시적으로 모델링한다
- **Planner-Executor 패턴**은 복잡한 작업을 Sub-task로 분해하여 단계별로 실행하는 구조다
- Sub-task 분해 전략은 **순차, 병렬, 계층적** 3가지이며, 의존성 그래프를 기반으로 선택한다
- **Single-step Agent**는 단순 조회에, **Multi-step Agent**는 다단계 추론이 필요한 작업에 적합하다
- 프로젝트 초기에는 Single-step으로 시작하고, 복잡도가 증가하면 Multi-step으로 점진적으로 전환한다
