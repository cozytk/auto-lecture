# Session 2: LangGraph 기반 제어 흐름 설계

## 학습 목표
1. LangGraph의 Node-Edge-State 구조를 이해하고 Agent 제어 흐름을 그래프로 설계할 수 있다
2. Conditional Edge를 활용하여 동적 분기 로직을 구현할 수 있다
3. Retry/Fallback 전략을 LangGraph 그래프에 내장하여 안정적인 Agent를 구축할 수 있다

---

## 1. Node-Edge-State 구조 이해

### 개념 설명

LangGraph는 Agent의 제어 흐름을 **방향 그래프(Directed Graph)**로 표현한다. 세 가지 핵심 개념을 이해해야 한다.

**왜 그래프 기반 제어 흐름인가?** 초기 LLM 애플리케이션 프레임워크(LangChain의 Chain, Sequential Chain 등)는 제어 흐름을 **선형 체인(linear chain)**으로 표현했다. A -> B -> C처럼 한 방향으로만 흐르는 구조다. 이 방식은 단순한 파이프라인에는 적합하지만, 실제 Agent는 훨씬 복잡한 흐름을 필요로 한다. "분류 결과에 따라 다른 처리 경로를 선택해야 하고", "실패하면 이전 단계로 돌아가야 하며", "특정 조건이 충족될 때까지 반복해야 한다". 선형 체인으로는 이런 제어 흐름을 자연스럽게 표현할 수 없다.

그래프 구조는 이 한계를 근본적으로 해결한다. 컴퓨터 과학에서 **유한 상태 기계(Finite State Machine, FSM)**는 상태(State)와 전이(Transition)로 복잡한 동작을 모델링하는 검증된 패러다임이다. LangGraph는 이 개념을 LLM Agent에 적용하여, Node가 상태에서의 행동(action)을, Edge가 상태 전이(transition)를 표현한다. 이 구조의 가장 큰 장점은 **시각화 가능성과 추론 가능성**이다. 그래프를 그려보면 Agent의 모든 가능한 실행 경로가 한눈에 보이므로, 설계 단계에서 빠진 경로나 무한 루프를 발견할 수 있다.

LangGraph와 비교되는 대안으로 AutoGen(Microsoft), CrewAI, LlamaIndex의 Workflow가 있다. AutoGen은 에이전트 간 대화(conversation) 기반으로 제어 흐름을 관리하여 멀티 에이전트 대화에 강점이 있지만, 세밀한 제어 흐름 설계가 어렵다. CrewAI는 역할(role) 기반으로 에이전트를 조합하여 빠른 프로토타이핑에 유리하지만, 커스텀 제어 로직 구현이 제한적이다. LangGraph는 이들보다 로우레벨이지만, 그만큼 **제어 흐름을 정밀하게 설계**할 수 있어 프로덕션 수준의 Agent 구축에 적합하다.

| 개념 | 역할 | LangGraph 대응 |
|------|------|----------------|
| **Node** | 실행 단위 (함수) | `graph.add_node("name", func)` |
| **Edge** | Node 간 연결 (전이) | `graph.add_edge("a", "b")` |
| **State** | Node 간 공유 데이터 | `TypedDict` 클래스 |

```
+-------------------------------------------------+
|                  StateGraph                      |
|                                                  |
|  State(TypedDict)                                |
|  +---------------------------------------+      |
|  | messages, step, data, ...             |      |
|  +---------------------------------------+      |
|                                                  |
|  [START] --Edge--> [Node A] --Edge--> [Node B]  |
|                        |                         |
|                   Conditional                    |
|                    Edge                          |
|                   /     \                        |
|           [Node C]       [Node D] --> [END]      |
+-------------------------------------------------+
```

**핵심 원칙:**
- Node는 **순수 함수**다. State를 입력받아 State 업데이트(dict)를 반환한다
- Edge는 **데이터 흐름 방향**을 정의한다. 조건부 Edge로 분기가 가능하다
- State는 **불변(immutable) 패턴**으로 관리한다. Node는 전체 State를 교체하지 않고 변경할 필드만 반환한다

Node를 순수 함수로 설계하는 것은 단순한 코딩 규칙이 아니라, 테스트 가능성과 재현 가능성을 확보하기 위한 핵심 전략이다. 순수 함수는 동일한 입력에 항상 동일한 출력을 반환하므로, 특정 Node에 버그가 있을 때 해당 Node만 격리하여 테스트할 수 있다. 다음 코드는 이 세 가지 개념이 실제로 어떻게 조합되는지 보여준다.

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator


class SimpleState(TypedDict):
    """Node 간 공유되는 State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    step_count: int
    current_node: str


def node_a(state: SimpleState) -> dict:
    """첫 번째 처리 단계"""
    print(f"[Node A] 실행 (step: {state['step_count']})")
    return {
        "step_count": state["step_count"] + 1,
        "current_node": "a",
        "messages": [AIMessage(content="Node A 처리 완료")],
    }


def node_b(state: SimpleState) -> dict:
    """두 번째 처리 단계"""
    print(f"[Node B] 실행 (step: {state['step_count']})")
    return {
        "step_count": state["step_count"] + 1,
        "current_node": "b",
        "messages": [AIMessage(content="Node B 처리 완료")],
    }


def node_c(state: SimpleState) -> dict:
    """최종 처리 단계"""
    print(f"[Node C] 실행 (step: {state['step_count']})")
    return {
        "step_count": state["step_count"] + 1,
        "current_node": "c",
        "messages": [AIMessage(content="최종 처리 완료")],
    }


# 그래프 구성
graph = StateGraph(SimpleState)

# Node 등록
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_node("node_c", node_c)

# Edge 연결: START -> A -> B -> C -> END
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", "node_c")
graph.add_edge("node_c", END)

# 컴파일 및 실행
app = graph.compile()

result = app.invoke({
    "messages": [HumanMessage(content="안녕하세요")],
    "step_count": 0,
    "current_node": "start",
})

print(f"\n최종 step_count: {result['step_count']}")
print(f"메시지 수: {len(result['messages'])}")
```

**실행 결과:**
```
[Node A] 실행 (step: 0)
[Node B] 실행 (step: 1)
[Node C] 실행 (step: 2)

최종 step_count: 3
메시지 수: 4
```

### Q&A

**Q: Node 함수가 전체 State를 반환하지 않고 일부만 반환해도 되나요?**
A: 그렇다. LangGraph는 **부분 업데이트(partial update)** 방식이다. Node는 변경하고 싶은 필드만 포함한 dict를 반환하면 된다. 반환하지 않은 필드는 기존 값이 유지된다. `Annotated[Sequence, operator.add]`처럼 reducer를 지정하면 값이 교체가 아닌 누적된다.

**Q: START와 `set_entry_point`의 차이는?**
A: 동일한 기능이다. `graph.add_edge(START, "node_a")`와 `graph.set_entry_point("node_a")`는 같은 의미다. LangGraph 최신 버전에서는 `START` 상수를 사용하는 `add_edge` 방식을 권장한다.

<details>
<summary>퀴즈: 다음 코드에서 `operator.add`가 하는 역할은?</summary>

```python
messages: Annotated[Sequence[BaseMessage], operator.add]
```

**힌트**: 두 Node가 각각 `{"messages": [msg1]}`과 `{"messages": [msg2]}`를 반환하면, 최종 messages는 어떻게 되나요?

**정답**: `operator.add`는 **reducer 함수**로, 해당 필드의 업데이트 방식을 "교체"가 아닌 "누적(append)"으로 지정한다. 즉 각 Node가 반환한 messages가 기존 리스트에 추가된다. 이것이 없으면 마지막 Node의 반환값으로 덮어쓰기된다.
</details>

---

## 2. Conditional Edge 분기 설계

### 개념 설명

실제 Agent는 단순한 직선 흐름이 아니라 **조건에 따라 다른 경로**를 선택해야 한다. LangGraph의 `add_conditional_edges`가 이를 지원한다.

**왜 동적 분기가 Agent의 핵심인가?** Agent와 단순 파이프라인의 결정적 차이가 바로 여기에 있다. 파이프라인은 "A 다음에 항상 B"라는 고정된 흐름을 따르지만, Agent는 "A의 결과에 따라 B 또는 C 또는 D로 간다"는 동적 판단을 수행한다. 현실 세계의 의사결정이 그렇듯이, Agent도 매 순간 상황(State)을 평가하고 최적의 다음 행동을 선택해야 한다. 고객 지원 Agent를 예로 들면, 고객 질문이 기술 문제인지, 결제 문제인지, 일반 문의인지에 따라 완전히 다른 처리 경로를 밟아야 한다.

Conditional Edge는 프로그래밍에서 if-else 분기문과 유사하지만, 중요한 차이가 있다. 일반적인 if-else는 코드 흐름을 분기하고 합류시키는 반면, LangGraph의 Conditional Edge는 **그래프의 토폴로지(topology) 자체를 동적으로 결정**한다. 이 덕분에 분기 조건, 가능한 경로, 합류 지점이 그래프 정의에 명시적으로 드러나며, 실행 전에 모든 가능한 경로를 검증할 수 있다. 이것은 복잡한 Agent를 디버깅할 때 결정적인 이점이다.

실무에서 자주 사용하는 분기 패턴은 세 가지다. **이진 분기**는 성공/실패, 충분/부족 같은 두 가지 경우를 처리하며 가장 단순하다. **다중 분기**는 입력을 N개 카테고리 중 하나로 분류하여 각각 다른 처리 경로로 보내며, 라우팅이나 분류 작업에 적합하다. **루프 분기**는 조건이 충족될 때까지 이전 Node로 돌아가는 패턴으로, 반복 수집이나 재시도에 사용한다. 이 세 패턴을 조합하면 거의 모든 Agent 제어 흐름을 표현할 수 있다. 다만 루프 분기를 사용할 때는 반드시 종료 조건을 명확히 해야 한다. 그렇지 않으면 무한 루프에 빠질 위험이 있으며, 이는 Session 3에서 다루는 핵심 주제다.

```python
graph.add_conditional_edges(
    source="node_name",        # 분기가 시작되는 Node
    path=routing_function,     # State를 받아 다음 Node 이름을 반환하는 함수
    path_map={                 # 반환값 -> 실제 Node 매핑
        "option_a": "node_a",
        "option_b": "node_b",
    },
)
```

**분기 패턴 3가지:**

| 패턴 | 설명 | 사용 상황 |
|------|------|----------|
| **이진 분기** | 조건 하나로 두 경로 중 선택 | 성공/실패, 충분/부족 |
| **다중 분기** | 여러 조건으로 N개 경로 중 선택 | 카테고리 분류, 라우팅 |
| **루프 분기** | 조건 충족 시 이전 Node로 복귀 | 반복 수집, 재시도 |

다음 코드는 고객 질문을 유형별로 분류하여 다른 처리 경로로 라우팅하고, 응답 품질이 낮으면 재시도하는 전체 흐름을 보여준다. 다중 분기(질문 유형별 라우팅)와 루프 분기(품질 기반 재시도)가 하나의 그래프에서 어떻게 조합되는지 주목하라.

### 예제

```python
from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator


class RouterState(TypedDict):
    """라우팅 분기 예제 State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query_type: str        # 질문 유형: "technical", "billing", "general"
    confidence: float      # 응답 신뢰도
    answer: str
    retry_count: int


def classify_query(state: RouterState) -> dict:
    """사용자 질문을 분류한다."""
    user_msg = state["messages"][-1].content

    # 실제로는 LLM으로 분류 (데모용 규칙 기반)
    if "코드" in user_msg or "에러" in user_msg or "버그" in user_msg:
        query_type = "technical"
    elif "결제" in user_msg or "환불" in user_msg or "요금" in user_msg:
        query_type = "billing"
    else:
        query_type = "general"

    print(f"[분류] 질문 유형: {query_type}")
    return {"query_type": query_type}


def handle_technical(state: RouterState) -> dict:
    """기술 질문 처리"""
    answer = "기술팀에서 확인한 결과, 해당 에러는 버전 업데이트로 해결됩니다."
    print(f"[기술] {answer}")
    return {"answer": answer, "confidence": 0.85}


def handle_billing(state: RouterState) -> dict:
    """결제 질문 처리"""
    answer = "결제 관련 문의는 확인 후 24시간 이내 처리됩니다."
    print(f"[결제] {answer}")
    return {"answer": answer, "confidence": 0.92}


def handle_general(state: RouterState) -> dict:
    """일반 질문 처리"""
    answer = "해당 질문에 대한 일반적인 안내를 드립니다."
    print(f"[일반] {answer}")
    return {"answer": answer, "confidence": 0.70}


def quality_check(state: RouterState) -> dict:
    """응답 품질 검증"""
    print(f"[품질검증] 신뢰도: {state['confidence']:.2f}")
    return {"retry_count": state.get("retry_count", 0)}


# === 라우팅 함수들 ===

def route_by_type(state: RouterState) -> str:
    """질문 유형에 따라 다중 분기"""
    return state["query_type"]


def route_by_confidence(state: RouterState) -> str:
    """신뢰도에 따라 루프 또는 완료"""
    if state["confidence"] < 0.8 and state.get("retry_count", 0) < 2:
        return "retry"
    return "finish"


def generate_response(state: RouterState) -> dict:
    """최종 응답 생성"""
    response = f"[최종 응답] {state['answer']} (신뢰도: {state['confidence']:.0%})"
    print(response)
    return {"messages": [AIMessage(content=response)]}


# 그래프 구성
graph = StateGraph(RouterState)

graph.add_node("classify", classify_query)
graph.add_node("technical", handle_technical)
graph.add_node("billing", handle_billing)
graph.add_node("general", handle_general)
graph.add_node("quality_check", quality_check)
graph.add_node("response", generate_response)

# Edge 연결
graph.add_edge(START, "classify")

# 다중 분기: 질문 유형에 따라 라우팅
graph.add_conditional_edges(
    "classify",
    route_by_type,
    {
        "technical": "technical",
        "billing": "billing",
        "general": "general",
    },
)

# 각 처리 Node -> 품질 검증
graph.add_edge("technical", "quality_check")
graph.add_edge("billing", "quality_check")
graph.add_edge("general", "quality_check")

# 루프 분기: 신뢰도 낮으면 재시도
graph.add_conditional_edges(
    "quality_check",
    route_by_confidence,
    {
        "retry": "classify",   # 재분류부터 다시
        "finish": "response",  # 최종 응답 생성
    },
)

graph.add_edge("response", END)

app = graph.compile()

# 실행 테스트
print("=== 기술 질문 ===")
app.invoke({
    "messages": [HumanMessage(content="코드에서 에러가 발생합니다")],
    "query_type": "",
    "confidence": 0.0,
    "answer": "",
    "retry_count": 0,
})

print("\n=== 결제 질문 ===")
app.invoke({
    "messages": [HumanMessage(content="결제 환불 요청합니다")],
    "query_type": "",
    "confidence": 0.0,
    "answer": "",
    "retry_count": 0,
})
```

**실행 결과:**
```
=== 기술 질문 ===
[분류] 질문 유형: technical
[기술] 기술팀에서 확인한 결과, 해당 에러는 버전 업데이트로 해결됩니다.
[품질검증] 신뢰도: 0.85
[최종 응답] 기술팀에서 확인한 결과, 해당 에러는 버전 업데이트로 해결됩니다. (신뢰도: 85%)

=== 결제 질문 ===
[분류] 질문 유형: billing
[결제] 결제 관련 문의는 확인 후 24시간 이내 처리됩니다.
[품질검증] 신뢰도: 0.92
[최종 응답] 결제 관련 문의는 확인 후 24시간 이내 처리됩니다. (신뢰도: 92%)
```

### Q&A

**Q: Conditional Edge의 `path_map`을 생략하면 어떻게 되나요?**
A: `path_map`을 생략하면 routing 함수의 반환값이 **그대로 Node 이름**으로 사용된다. 즉 `route_by_type`이 `"technical"`을 반환하면 `"technical"` 이름의 Node로 이동한다. `path_map`은 반환값과 Node 이름이 다를 때만 필요하다.

**Q: Conditional Edge에서 가능한 모든 경로를 정의하지 않으면?**
A: 런타임에 routing 함수가 정의되지 않은 값을 반환하면 `ValueError`가 발생한다. 모든 가능한 경로를 `path_map`에 명시하거나, 기본(default) 경로를 포함해야 한다.

<details>
<summary>퀴즈: 아래 코드에서 무한 루프가 발생할 수 있는 조건은?</summary>

```python
graph.add_conditional_edges(
    "quality_check",
    route_by_confidence,
    {"retry": "classify", "finish": "response"},
)
```

**힌트**: `route_by_confidence` 함수의 조건을 다시 읽어보세요. `retry_count`는 어디서 증가하나요?

**정답**: 현재 구현에서 `retry_count`가 `quality_check`에서 증가하지 않고 기존 값을 그대로 유지한다. 따라서 `confidence`가 계속 0.8 미만이고 `retry_count`가 0으로 고정되면 무한 루프가 발생한다. 실제 구현에서는 `quality_check` Node에서 `retry_count + 1`을 반환해야 한다. 이것이 바로 Session 3에서 다룰 "무한 Loop 방지 전략"의 핵심이다.
</details>

---

## 3. Retry / Fallback 전략

### 개념 설명

프로덕션 Agent는 반드시 실패에 대비해야 한다. 두 가지 핵심 전략이 있다.

**왜 실패 대비가 Agent에서 특히 중요한가?** 전통적인 소프트웨어에서 함수 호출의 성공률은 거의 100%에 가깝다. 하지만 Agent는 근본적으로 다르다. LLM API 호출은 네트워크 지연, Rate Limit, 서비스 장애의 영향을 받고, LLM의 출력 자체도 비결정적이어서 때로는 잘못된 형식의 응답을 생성한다. 외부 Tool(웹 검색, DB 조회, API 호출)은 각각 고유한 실패 모드를 갖고 있다. 이처럼 Agent의 매 단계마다 실패 가능성이 존재하므로, 실패를 "예외적 상황"이 아닌 "정상적인 실행 경로"로 설계해야 한다.

Retry와 Fallback은 실패 유형에 따라 적용하는 전략이 다르다. **Retry**는 일시적 실패(transient failure)에 대한 대응이다. API 타임아웃, 네트워크 일시 장애, Rate Limit 초과 같은 상황은 시간이 지나면 해결되므로, 잠시 기다렸다가 같은 요청을 다시 보내면 된다. 이때 **지수 백오프(exponential backoff)**를 사용하는 것이 업계 표준이다. 첫 번째 재시도는 1초 대기, 두 번째는 2초, 세 번째는 4초처럼 대기 시간을 점진적으로 늘려 서버에 과부하를 주지 않으면서 성공 확률을 높인다.

**Fallback**은 구조적 실패(structural failure)에 대한 대응이다. Primary Tool이 아예 사용 불가능하거나, 특정 유형의 입력을 처리하지 못하거나, 영구적 장애가 발생한 경우에는 재시도해봐야 같은 결과가 나온다. 이때는 대체 경로(alternative path)로 전환해야 한다. 예를 들어, 실시간 주가 API가 다운되면 캐시된 데이터로 대체하거나, GPT-4가 실패하면 GPT-3.5로 폴백하는 식이다. Fallback의 핵심 원칙은 "품질은 다소 낮더라도 응답을 반환한다"는 것이다. 사용자 입장에서 에러 메시지를 받는 것보다는 불완전하더라도 유용한 응답을 받는 것이 낫다.

실무에서는 Retry와 Fallback을 **계층적으로 적용**하는 것이 일반적이다. 먼저 Retry로 일시적 실패를 처리하고, Retry 횟수를 초과하면 Fallback으로 전환한다. 이때 사용자에게 Fallback이 사용되었음을 투명하게 알려주는 것이 좋은 관행이다.

| 전략 | 설명 | 적용 시점 |
|------|------|----------|
| **Retry** | 동일 작업을 재시도 (일시적 실패 대응) | API 타임아웃, Rate Limit, 네트워크 오류 |
| **Fallback** | 대체 경로로 전환 (구조적 실패 대응) | Tool 미지원 입력, 모델 출력 형식 오류, 영구적 API 장애 |

```
[Tool 호출]
     |
     v
  성공? --Yes--> 다음 단계
     | No
     v
  재시도 가능? --Yes--> [Retry] (최대 N회)
     | No                        |
     v                           v (N회 초과)
  [Fallback] ----------> 대체 로직
```

다음 코드는 Primary Tool이 2번 실패한 후 3번째에 성공하는 시나리오와, 최대 재시도 횟수를 1회로 제한하여 Fallback으로 전환되는 시나리오를 모두 보여준다.

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator
import random


class RetryFallbackState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    retry_count: int
    max_retries: int
    tool_result: str
    error: str
    used_fallback: bool


def call_primary_tool(state: RetryFallbackState) -> dict:
    """Primary Tool 호출 (실패할 수 있음)"""
    retry = state["retry_count"]

    # 시뮬레이션: 3번째 시도에서 성공
    if retry < 2:
        error_msg = f"API 타임아웃 (시도 {retry + 1}/{state['max_retries']})"
        print(f"[Primary Tool] 실패: {error_msg}")
        return {
            "error": error_msg,
            "retry_count": retry + 1,
            "tool_result": "",
        }
    else:
        result = "Primary Tool 실행 성공: 데이터 조회 완료"
        print(f"[Primary Tool] 성공: {result}")
        return {
            "tool_result": result,
            "error": "",
            "retry_count": retry + 1,
        }


def call_fallback_tool(state: RetryFallbackState) -> dict:
    """Fallback Tool 호출"""
    result = "Fallback Tool 실행: 캐시 데이터로 대체 응답"
    print(f"[Fallback Tool] {result}")
    return {
        "tool_result": result,
        "error": "",
        "used_fallback": True,
    }


def generate_answer(state: RetryFallbackState) -> dict:
    """최종 응답 생성"""
    source = "Fallback" if state.get("used_fallback") else "Primary"
    answer = f"[{source}] {state['tool_result']}"
    print(f"[응답] {answer}")
    return {"messages": [AIMessage(content=answer)]}


def route_after_tool(state: RetryFallbackState) -> str:
    """Tool 결과에 따라 Retry / Fallback / 성공 분기"""
    # 성공
    if state["tool_result"] and not state["error"]:
        return "success"
    # 재시도 가능
    if state["retry_count"] < state["max_retries"]:
        return "retry"
    # 재시도 소진 -> Fallback
    return "fallback"


# 그래프 구성
graph = StateGraph(RetryFallbackState)

graph.add_node("primary_tool", call_primary_tool)
graph.add_node("fallback_tool", call_fallback_tool)
graph.add_node("answer", generate_answer)

graph.add_edge(START, "primary_tool")

# Retry/Fallback 분기
graph.add_conditional_edges(
    "primary_tool",
    route_after_tool,
    {
        "success": "answer",
        "retry": "primary_tool",     # 재시도
        "fallback": "fallback_tool",  # 대체 경로
    },
)

graph.add_edge("fallback_tool", "answer")
graph.add_edge("answer", END)

app = graph.compile()

# 실행: 2번 실패 후 3번째 성공
print("=== Retry 후 성공 케이스 (max_retries=3) ===")
result = app.invoke({
    "messages": [HumanMessage(content="데이터 조회 요청")],
    "retry_count": 0,
    "max_retries": 3,
    "tool_result": "",
    "error": "",
    "used_fallback": False,
})

print("\n=== Fallback 케이스 (max_retries=1) ===")
result = app.invoke({
    "messages": [HumanMessage(content="데이터 조회 요청")],
    "retry_count": 0,
    "max_retries": 1,
    "tool_result": "",
    "error": "",
    "used_fallback": False,
})
```

**실행 결과:**
```
=== Retry 후 성공 케이스 (max_retries=3) ===
[Primary Tool] 실패: API 타임아웃 (시도 1/3)
[Primary Tool] 실패: API 타임아웃 (시도 2/3)
[Primary Tool] 성공: Primary Tool 실행 성공: 데이터 조회 완료
[응답] [Primary] Primary Tool 실행 성공: 데이터 조회 완료

=== Fallback 케이스 (max_retries=1) ===
[Primary Tool] 실패: API 타임아웃 (시도 1/1)
[Fallback Tool] Fallback Tool 실행: 캐시 데이터로 대체 응답
[응답] [Fallback] Fallback Tool 실행: 캐시 데이터로 대체 응답
```

### Q&A

**Q: Retry와 Fallback을 동시에 사용해야 하나요?**
A: 일반적으로 두 전략을 **계층적으로 적용**한다. 먼저 Retry로 일시적 실패를 처리하고, Retry 횟수를 초과하면 Fallback으로 전환한다. 일시적 실패(타임아웃)에 바로 Fallback을 사용하면 불필요하게 품질이 저하될 수 있다.

**Q: Retry 간 대기 시간(backoff)은 어떻게 구현하나요?**
A: LangGraph Node 내부에서 `asyncio.sleep()` 또는 `time.sleep()`으로 지수 백오프(exponential backoff)를 구현한다. State에 `retry_count`가 있으므로 `wait_time = 2 ** retry_count`처럼 계산할 수 있다.

<details>
<summary>퀴즈: Fallback Tool의 응답 품질이 Primary보다 낮다면, 사용자에게 어떻게 알려야 하나요?</summary>

**힌트**: State에 `used_fallback` 필드가 있습니다. 이 정보를 최종 응답에 어떻게 반영할 수 있을까요?

**정답**: 최종 응답에 Fallback 사용 여부를 **메타데이터로 포함**한다. 예: "참고: 일시적 서비스 장애로 캐시 데이터 기반 응답입니다. 정확한 결과는 잠시 후 다시 시도해주세요." 이렇게 하면 사용자가 응답 신뢰도를 판단할 수 있다.
</details>

---

## 4. State Propagation 방식

### 개념 설명

LangGraph에서 State는 그래프의 **모든 Node를 관통하며 전파**된다. 올바른 State Propagation을 이해하지 못하면 데이터가 유실되거나 의도치 않게 덮어쓰기될 수 있다.

**왜 State Propagation을 정확히 이해해야 하는가?** Agent 개발에서 가장 디버깅하기 어려운 버그 유형 중 하나가 "State 오염(State corruption)"이다. Node A에서 설정한 값이 Node B를 거치면서 사라지거나, 예상과 다른 값으로 변경되는 현상은 State 업데이트 규칙을 정확히 모를 때 빈번하게 발생한다. 특히 reducer가 적용된 필드와 그렇지 않은 필드가 혼재할 때 혼란이 가중된다.

LangGraph의 State 업데이트는 크게 세 가지 규칙을 따른다. 첫째, **부분 업데이트** -- Node는 변경하고 싶은 필드만 반환하면 되며, 나머지 필드는 기존 값이 그대로 유지된다. 이것은 전체 State를 매번 복사하여 반환하는 비효율을 피하면서도, 의도하지 않은 필드 변경을 방지한다. 둘째, **Reducer 적용** -- `Annotated[type, reducer_fn]`으로 정의된 필드는 새 값이 기존 값을 덮어쓰지 않고, reducer 함수를 통해 병합된다. `operator.add`를 사용하면 리스트는 concat되고 숫자는 합산된다. 셋째, **Reducer 없는 필드** -- reducer가 없는 필드는 단순히 마지막으로 반환된 값으로 교체된다.

이 규칙을 헷갈리면 두 가지 대표적인 실수를 범한다. 하나는 messages 같은 누적 필드를 reducer 없이 정의하여, 이전 대화 히스토리가 매번 덮어씌워지는 것이다. 다른 하나는 counter 같은 단일값 필드에 reducer를 적용하여, 의도치 않게 값이 계속 증가하는 것이다. 아래 코드에서 이 세 가지 규칙이 실제로 어떻게 동작하는지 단계별로 관찰할 수 있다.

**State 업데이트 규칙:**

| 규칙 | 설명 |
|------|------|
| **부분 업데이트** | Node는 변경할 필드만 반환. 나머지는 보존 |
| **Reducer 적용** | `Annotated[type, reducer]`가 있으면 reducer로 병합 |
| **Reducer 없음** | 가장 최근 반환값으로 교체 |
| **미반환 필드** | 이전 값 그대로 유지 |

```
State = {a: 1, b: [1], c: "hello"}
                    |
            Node 1 반환: {a: 2, b: [2]}
                    |
                    v
State = {a: 2, b: [1, 2], c: "hello"}
         ^교체    ^누적(reducer)  ^유지

            Node 2 반환: {c: "world"}
                    |
                    v
State = {a: 2, b: [1, 2], c: "world"}
         ^유지   ^유지       ^교체
```

### 예제

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator


class PropagationState(TypedDict):
    """State Propagation 데모"""
    # Reducer 없음: 마지막 값으로 교체
    current_step: str
    # Reducer 있음: 값이 누적
    log: Annotated[list[str], operator.add]
    # Reducer 없음: 마지막 값으로 교체
    counter: int


def step_one(state: PropagationState) -> dict:
    """Step 1: current_step과 log 업데이트, counter는 건드리지 않음"""
    print(f"[Step 1] counter={state['counter']}, log={state['log']}")
    return {
        "current_step": "step_one_complete",
        "log": ["step_one 실행"],
        # counter를 반환하지 않음 -> 이전 값 유지
    }


def step_two(state: PropagationState) -> dict:
    """Step 2: counter 증가, log 추가"""
    print(f"[Step 2] counter={state['counter']}, log={state['log']}")
    return {
        "current_step": "step_two_complete",
        "log": ["step_two 실행"],   # reducer로 기존 log에 추가됨
        "counter": state["counter"] + 10,  # 교체
    }


def step_three(state: PropagationState) -> dict:
    """Step 3: 최종 확인"""
    print(f"[Step 3] counter={state['counter']}, log={state['log']}")
    return {
        "current_step": "done",
        "log": ["step_three 실행"],
    }


graph = StateGraph(PropagationState)
graph.add_node("step_one", step_one)
graph.add_node("step_two", step_two)
graph.add_node("step_three", step_three)

graph.add_edge(START, "step_one")
graph.add_edge("step_one", "step_two")
graph.add_edge("step_two", "step_three")
graph.add_edge("step_three", END)

app = graph.compile()

result = app.invoke({
    "current_step": "init",
    "log": ["초기화"],
    "counter": 0,
})

print(f"\n=== 최종 State ===")
print(f"current_step: {result['current_step']}")
print(f"log: {result['log']}")
print(f"counter: {result['counter']}")
```

**실행 결과:**
```
[Step 1] counter=0, log=['초기화']
[Step 2] counter=0, log=['초기화', 'step_one 실행']
[Step 3] counter=10, log=['초기화', 'step_one 실행', 'step_two 실행']

=== 최종 State ===
current_step: done
log: ['초기화', 'step_one 실행', 'step_two 실행', 'step_three 실행']
counter: 10
```

핵심 관찰:
- `log`는 `operator.add` reducer로 **누적**됨 (4개 항목)
- `counter`는 reducer 없이 step_two에서 **교체**됨 (0 -> 10)
- `counter`를 step_one에서 반환하지 않았지만 값이 **유지**됨 (0 그대로)

### Q&A

**Q: 커스텀 reducer를 만들 수 있나요?**
A: 가능하다. `operator.add` 대신 커스텀 함수를 사용할 수 있다. 예를 들어 최대값만 유지하는 reducer: `Annotated[int, lambda old, new: max(old, new)]`. 단, reducer 함수는 `(old_value, new_value) -> merged_value` 시그니처를 따라야 한다.

**Q: 복잡한 중첩 State(dict 안의 dict)는 어떻게 관리하나요?**
A: LangGraph에서는 **평탄한(flat) State 구조**를 권장한다. 중첩이 필요하면 별도의 `TypedDict`로 정의하고, 해당 필드 전체를 교체하는 방식으로 관리한다. 깊은 중첩은 reducer 동작을 예측하기 어렵게 만든다.

<details>
<summary>퀴즈: 아래 State 정의에서 Node가 `{"data": [4, 5]}`를 반환하면 최종 data 값은?</summary>

```python
class MyState(TypedDict):
    data: Annotated[list[int], operator.add]

# 초기: {"data": [1, 2, 3]}
```

**힌트**: `operator.add`는 리스트에 대해 어떤 연산을 수행하나요?

**정답**: `[1, 2, 3, 4, 5]`. `operator.add`는 리스트에 대해 `+` 연산(concatenation)을 수행한다. `[1, 2, 3] + [4, 5] = [1, 2, 3, 4, 5]`.
</details>

---

## 실습

### 실습 1: 멀티 경로 라우팅 그래프 구축
- **연관 학습 목표**: 학습 목표 1, 2
- **실습 목적**: Node-Edge-State 구조와 Conditional Edge를 조합하여 실제 라우팅 Agent 구현
- **실습 유형**: 코드 작성
- **난이도**: 기초
- **예상 소요 시간**: 25분
- **선행 조건**: LangGraph 설치 (`pip install langgraph langchain-core`)
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
"문서 처리 Agent"를 구현하세요. 입력 문서의 유형(이메일, 보고서, 계약서)에 따라 다른 처리 경로를 선택합니다.

요구사항:
1. `classify` Node: 문서 유형 분류 (키워드 기반 규칙으로 구현)
2. `process_email` Node: 이메일 처리 (발신자, 제목, 본문 추출)
3. `process_report` Node: 보고서 처리 (핵심 지표 추출)
4. `process_contract` Node: 계약서 처리 (주요 조항 추출)
5. `summarize` Node: 처리 결과 요약
6. Conditional Edge로 문서 유형별 분기

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
import operator

class DocProcessState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    doc_type: str
    extracted_info: dict
    summary: str

# TODO: 각 Node 함수 구현
# TODO: StateGraph 구성 및 Conditional Edge 설정
# TODO: 3가지 유형 문서로 테스트
```

---

### 실습 2: Retry + Fallback 패턴 구현
- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: 프로덕션 수준의 에러 처리 전략을 LangGraph로 구현
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 35분
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
"외부 API 호출 Agent"를 구현하세요. Primary API가 실패하면 Retry하고, 최대 횟수를 초과하면 Fallback API로 전환합니다.

요구사항:
1. Primary API Node: `random.random() < 0.7`이면 실패하는 불안정한 API 시뮬레이션
2. Retry 로직: 최대 3회 재시도, 재시도 간 지수 백오프(1초, 2초, 4초) -- `time.sleep()` 사용
3. Fallback API Node: 항상 성공하지만 응답 품질이 낮은 대체 API
4. 결과 Node: Fallback 사용 여부를 포함한 최종 응답 생성
5. State에 `retry_count`, `errors`, `used_fallback` 추적

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator
import random
import time

class ApiCallState(TypedDict):
    query: str
    result: str
    errors: Annotated[list[str], operator.add]
    retry_count: int
    max_retries: int
    used_fallback: bool

# TODO: primary_api Node (random 실패)
# TODO: fallback_api Node (항상 성공)
# TODO: result Node (최종 응답)
# TODO: route 함수 (retry/fallback/success 분기)
# TODO: StateGraph 구성 및 실행
```

---

### 실습 3: 완전한 Workflow 그래프 설계 및 구현
- **연관 학습 목표**: 학습 목표 1, 2, 3
- **실습 목적**: 모든 개념을 통합하여 실제 업무 시나리오의 Agent Workflow를 구축
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 40분
- **선행 조건**: 실습 1, 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
"데이터 분석 파이프라인 Agent"를 구현하세요.

전체 흐름:
```
[데이터 수집] -> [검증] -> [분석] -> [품질 검사] -> [보고서 생성]
                  |          |           |
                  v          v           v
              [재수집]    [대체분석]   [재분석]
              (Retry)    (Fallback)   (Retry)
```

요구사항:
1. 5개 Node: collect, validate, analyze, quality_check, report
2. validate에서 실패하면 collect로 Retry (최대 2회)
3. analyze에서 실패하면 Fallback 분석 경로로 전환
4. quality_check에서 점수가 낮으면 analyze로 Retry (최대 1회)
5. State에 전체 실행 로그(`Annotated[list, operator.add]`)를 누적
6. 최종 보고서에 사용된 경로와 재시도 횟수를 포함

---

## 핵심 정리
- LangGraph는 **Node(실행 단위), Edge(전이), State(공유 데이터)** 3요소로 Agent 제어 흐름을 표현한다
- Node는 State를 받아 **부분 업데이트 dict**를 반환하는 순수 함수다
- **Conditional Edge**로 State 조건에 따라 동적 분기를 구현한다 (이진/다중/루프)
- **Retry** 전략은 일시적 실패에, **Fallback** 전략은 구조적 실패에 대응한다
- State Propagation에서 `Annotated[type, reducer]`는 **누적**, reducer 없는 필드는 **교체**, 미반환 필드는 **유지**된다
- 평탄한(flat) State 구조가 reducer 동작을 예측하기 쉬우므로 권장된다
