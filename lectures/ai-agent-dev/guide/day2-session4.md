# Session 4: 구조 리팩토링 & 확장성 설계

## 학습 목표
1. 단일 Agent에서 Multi-Agent로의 확장 패턴을 이해하고, 적절한 전환 시점을 판단할 수 있다
2. LangGraph 서브그래프(Subgraph)를 활용하여 Agent 간 통신과 상태 공유를 구현할 수 있다
3. 체크포인트, 메모리 관리를 포함한 상태 관리 확장 전략과 모놀리식에서 모듈형으로의 리팩토링 전략을 적용할 수 있다

---

## 1. 단일 Agent에서 Multi-Agent로의 확장 패턴

### 개념 설명

Agent 개발은 대부분 **단일 그래프(Monolithic Agent)**로 시작한다. 기능이 추가될수록 그래프가 비대해지고 유지보수가 어려워진다. 이 시점에 **Multi-Agent 구조**로 확장해야 한다.

이 전환의 본질은 소프트웨어 공학에서 오래된 원칙인 **관심사의 분리(Separation of Concerns)**와 **단일 책임 원칙(Single Responsibility Principle)**을 Agent 시스템에 적용하는 것이다. 전통적인 소프트웨어에서 하나의 거대한 클래스가 모든 비즈니스 로직을 담당하면 유지보수가 불가능해지듯이, 하나의 StateGraph가 검색, 분석, 보고서 작성, 이메일 발송까지 모두 처리하면 동일한 문제가 발생한다. 각 Node가 공유하는 State 필드가 늘어날수록 하나의 Node를 수정할 때 예상치 못한 부작용(side effect)이 다른 Node에 전파된다. 이것은 마이크로서비스 아키텍처가 모놀리식 애플리케이션의 한계를 극복하기 위해 등장한 맥락과 정확히 같다.

그러나 **모든 Agent를 처음부터 Multi-Agent로 설계하는 것은 오버엔지니어링**이다. Martin Fowler의 "Monolith First" 원칙처럼, 단일 Agent로 시작해서 복잡도가 임계점을 넘었을 때 분리하는 것이 실용적이다. 핵심은 **전환 시점을 정확히 판단**하는 것이다. 아래 표의 신호들이 2개 이상 동시에 나타나면 리팩토링을 고려해야 한다. 특히 "Node 간 의존성 증가"는 가장 위험한 신호인데, 이것은 한 Node의 버그가 전체 시스템으로 전파되는 **결함 전파(Fault Propagation)** 경로가 넓어졌다는 의미이기 때문이다.

Multi-Agent 패턴 선택에서도 실무적 판단이 필요하다. **Supervisor 패턴**은 중앙 집중식으로 디버깅과 모니터링이 쉽지만 Supervisor가 병목이 될 수 있다. **Peer-to-Peer 패턴**은 Agent 간 직접 소통으로 유연하지만 통신 복잡도가 Agent 수의 제곱으로 증가한다(O(n²)). **Hierarchical 패턴**은 대규모 시스템에서 관리 범위를 제한하는 군대의 지휘 체계와 유사하며, 각 레벨의 Supervisor가 7±2개 이하의 하위 Agent만 관리하는 것이 인지 부하 측면에서 이상적이다.

**성장 단계:**

```
Stage 1: 단일 Agent          Stage 2: 기능 분리          Stage 3: Multi-Agent
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────────┐
│  하나의 거대한    │    │  Supervisor      │    │  Orchestrator        │
│  StateGraph      │    │  ├─ Search Node  │    │  ├─ Search Agent     │
│  - search        │ => │  ├─ Analyze Node │ => │  ├─ Analysis Agent   │
│  - analyze       │    │  └─ Report Node  │    │  └─ Report Agent     │
│  - report        │    │  (같은 그래프)    │    │  (각각 독립 그래프)   │
│  - validate      │    └──────────────────┘    └──────────────────────┘
│  - ...           │
└──────────────────┘
```

**전환 판단 기준:**

| 신호 | 설명 | 위험 수준 |
|------|------|----------|
| Node 10개 초과 | 그래프 복잡도가 인지 한계를 넘음 | 높음 |
| State 필드 15개 초과 | State 관리가 어려워짐 | 높음 |
| Node 간 의존성 증가 | 하나 수정 시 다른 Node에 영향 | 중간 |
| 테스트 어려움 | 특정 Node만 단독 테스트하기 힘듦 | 중간 |
| 팀 분업 필요 | 여러 개발자가 동시에 작업해야 함 | 낮음 |

**Multi-Agent 확장 패턴 3가지:**

| 패턴 | 구조 | 적합한 상황 |
|------|------|------------|
| **Supervisor** | 중앙 Agent가 하위 Agent에게 작업 위임 | 명확한 역할 분담, 순차 처리 |
| **Peer-to-Peer** | Agent 간 직접 통신 | 협업 기반 작업, 토론/합의 |
| **Hierarchical** | 다단계 위임 (Supervisor의 Supervisor) | 대규모 복잡 시스템 |

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator


# ============================================================
# Before: 단일 거대 Agent (모든 로직이 하나의 그래프)
# ============================================================

class MonolithState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    search_results: list[str]
    analysis: str
    report: str
    step: str


def monolith_search(state: MonolithState) -> dict:
    results = [f"검색 결과: {state['query']} 관련 데이터"]
    print(f"[Monolith] 검색: {results}")
    return {"search_results": results, "step": "analyze"}


def monolith_analyze(state: MonolithState) -> dict:
    analysis = f"분석 완료: {len(state['search_results'])}건 분석"
    print(f"[Monolith] 분석: {analysis}")
    return {"analysis": analysis, "step": "report"}


def monolith_report(state: MonolithState) -> dict:
    report = f"보고서: {state['analysis']}"
    print(f"[Monolith] 보고서: {report}")
    return {
        "report": report,
        "step": "done",
        "messages": [AIMessage(content=report)],
    }


monolith_graph = StateGraph(MonolithState)
monolith_graph.add_node("search", monolith_search)
monolith_graph.add_node("analyze", monolith_analyze)
monolith_graph.add_node("report", monolith_report)
monolith_graph.add_edge(START, "search")
monolith_graph.add_edge("search", "analyze")
monolith_graph.add_edge("analyze", "report")
monolith_graph.add_edge("report", END)
monolith_app = monolith_graph.compile()

print("=== Before: Monolith Agent ===")
monolith_app.invoke({
    "messages": [HumanMessage(content="시장 분석")],
    "query": "AI Agent 시장",
    "search_results": [],
    "analysis": "",
    "report": "",
    "step": "search",
})


# ============================================================
# After: Supervisor 패턴 Multi-Agent
# ============================================================

# --- Sub-Agent 1: Search Agent ---
class SearchState(TypedDict):
    query: str
    results: list[str]


def search_execute(state: SearchState) -> dict:
    results = [
        f"검색 결과: {state['query']} 관련 데이터 1",
        f"검색 결과: {state['query']} 관련 데이터 2",
    ]
    print(f"  [Search Agent] {len(results)}건 검색 완료")
    return {"results": results}


search_graph = StateGraph(SearchState)
search_graph.add_node("execute", search_execute)
search_graph.add_edge(START, "execute")
search_graph.add_edge("execute", END)
search_agent = search_graph.compile()


# --- Sub-Agent 2: Analysis Agent ---
class AnalysisState(TypedDict):
    data: list[str]
    analysis: str


def analysis_execute(state: AnalysisState) -> dict:
    analysis = f"분석 완료: {len(state['data'])}건 데이터에서 3개 인사이트 도출"
    print(f"  [Analysis Agent] {analysis}")
    return {"analysis": analysis}


analysis_graph = StateGraph(AnalysisState)
analysis_graph.add_node("execute", analysis_execute)
analysis_graph.add_edge(START, "execute")
analysis_graph.add_edge("execute", END)
analysis_agent = analysis_graph.compile()


# --- Sub-Agent 3: Report Agent ---
class ReportState(TypedDict):
    analysis: str
    report: str


def report_execute(state: ReportState) -> dict:
    report = f"[보고서] {state['analysis']} | 결론: 성장 가능성 높음"
    print(f"  [Report Agent] 보고서 생성 완료")
    return {"report": report}


report_graph = StateGraph(ReportState)
report_graph.add_node("execute", report_execute)
report_graph.add_edge(START, "execute")
report_graph.add_edge("execute", END)
report_agent = report_graph.compile()


# --- Supervisor: Sub-Agent들을 조율 ---
class SupervisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    search_results: list[str]
    analysis: str
    report: str


def supervisor_search(state: SupervisorState) -> dict:
    """Search Agent에게 작업 위임"""
    print("[Supervisor] Search Agent 호출")
    result = search_agent.invoke({"query": state["query"], "results": []})
    return {"search_results": result["results"]}


def supervisor_analyze(state: SupervisorState) -> dict:
    """Analysis Agent에게 작업 위임"""
    print("[Supervisor] Analysis Agent 호출")
    result = analysis_agent.invoke({
        "data": state["search_results"],
        "analysis": "",
    })
    return {"analysis": result["analysis"]}


def supervisor_report(state: SupervisorState) -> dict:
    """Report Agent에게 작업 위임"""
    print("[Supervisor] Report Agent 호출")
    result = report_agent.invoke({
        "analysis": state["analysis"],
        "report": "",
    })
    return {
        "report": result["report"],
        "messages": [AIMessage(content=result["report"])],
    }


supervisor_graph = StateGraph(SupervisorState)
supervisor_graph.add_node("search", supervisor_search)
supervisor_graph.add_node("analyze", supervisor_analyze)
supervisor_graph.add_node("report", supervisor_report)
supervisor_graph.add_edge(START, "search")
supervisor_graph.add_edge("search", "analyze")
supervisor_graph.add_edge("analyze", "report")
supervisor_graph.add_edge("report", END)
supervisor_app = supervisor_graph.compile()

print("\n=== After: Supervisor Multi-Agent ===")
supervisor_app.invoke({
    "messages": [HumanMessage(content="시장 분석")],
    "query": "AI Agent 시장",
    "search_results": [],
    "analysis": "",
    "report": "",
})
```

**실행 결과:**
```
=== Before: Monolith Agent ===
[Monolith] 검색: ['검색 결과: AI Agent 시장 관련 데이터']
[Monolith] 분석: 분석 완료: 1건 분석
[Monolith] 보고서: 보고서: 분석 완료: 1건 분석

=== After: Supervisor Multi-Agent ===
[Supervisor] Search Agent 호출
  [Search Agent] 2건 검색 완료
[Supervisor] Analysis Agent 호출
  [Analysis Agent] 분석 완료: 2건 데이터에서 3개 인사이트 도출
[Supervisor] Report Agent 호출
  [Report Agent] 보고서 생성 완료
```

### Q&A

**Q: Sub-Agent 방식과 완전 분리된 마이크로서비스 방식의 차이는?**
A: Sub-Agent는 **같은 프로세스 내**에서 독립 그래프를 호출한다. 네트워크 비용이 없고 State를 직접 전달한다. 마이크로서비스는 각 Agent가 **별도 프로세스/서버**로 실행되며 API로 통신한다. 처음에는 Sub-Agent로 시작하고, 스케일이 필요해지면 마이크로서비스로 전환하는 것이 실용적이다.

**Q: Supervisor 패턴과 Peer-to-Peer 패턴을 어떻게 선택하나요?**
A: 작업이 **명확한 순서(파이프라인)**를 가지면 Supervisor가 적합하다. 예: 검색 -> 분석 -> 보고서. 작업이 **상호 협의/토론**을 필요로 하면 Peer-to-Peer가 적합하다. 예: 코드 리뷰에서 보안 분석가와 성능 분석가가 서로의 의견을 참조하는 경우.

<details>
<summary>퀴즈: Monolith Agent에서 Modular 구조로 전환할 때 가장 먼저 해야 할 일은?</summary>

**힌트**: 코드를 분리하기 전에, 현재 코드의 구조를 먼저 이해해야 합니다.

**정답**: **의존성 분석**이 가장 먼저다. 각 Node가 State의 어떤 필드를 읽고 쓰는지를 매핑하여, 의존성이 적은 그룹부터 분리한다. 의존성 그래프를 그리면 자연스럽게 Sub-Agent 경계가 보인다.
</details>

---

## 2. Agent 간 통신 프로토콜 설계

### 개념 설명

Multi-Agent 시스템에서 Agent 간 통신 방식은 시스템의 **결합도(coupling)**와 **확장성**을 결정한다.

통신 프로토콜 설계가 중요한 이유는 분산 시스템의 근본적인 딜레마에 있다. Agent를 분리하면 각각의 독립성은 높아지지만, Agent 간 **정보 교환의 비용과 복잡도**가 증가한다. 이것은 Conway의 법칙(시스템 구조는 조직 구조를 반영한다)의 소프트웨어 버전이다. Agent 간 통신이 잘 설계되지 않으면, 분리의 이점보다 통신의 오버헤드가 더 커져서 오히려 모놀리식보다 나쁜 결과를 초래한다.

**결합도(coupling)**는 소프트웨어 품질의 가장 중요한 지표 중 하나다. 결합도가 높으면 한 Agent의 내부 변경이 다른 Agent에 연쇄적으로 영향을 미친다. 이를 **변경 전파(Change Propagation)**라 하며, 전파 범위가 넓을수록 유지보수 비용이 기하급수적으로 증가한다. 반대로 결합도가 너무 낮으면(예: 이벤트 기반) 시스템의 전체 흐름을 파악하기 어려워지는 **간접성의 저주(Curse of Indirection)** 문제가 생긴다. 실무에서는 이 두 극단 사이에서 적절한 균형점을 찾아야 한다.

LangGraph에서 권장하는 **메시지 전달 패턴**은 공유 State를 매개로 한 간접 통신이다. 이 방식이 자연스러운 이유는 LangGraph 자체가 State Machine 패러다임 위에 구축되었기 때문이다. 각 Agent는 자신의 State만 알고, Orchestrator의 **어댑터(Adapter)**가 State 간 변환을 담당한다. 이 어댑터 패턴은 GoF 디자인 패턴에서 유래한 것으로, 호환되지 않는 인터페이스를 가진 컴포넌트를 연결하는 **중간 번역 계층** 역할을 한다. Sub-Agent의 내부 State 구조가 변경되어도 어댑터만 수정하면 되므로, 변경의 영향 범위를 어댑터 함수 하나로 격리할 수 있다. 이것이 **인터페이스 계약(Interface Contract)**의 핵심 가치다. 입출력 스키마를 TypedDict로 명시적으로 정의하면, 컴파일 시점에 타입 불일치를 감지할 수 있고, 팀 내에서 Agent 간 "약속"이 문서화되는 효과도 얻는다.

**통신 패턴 3가지:**

| 패턴 | 설명 | 결합도 | 확장성 |
|------|------|--------|--------|
| **직접 호출** | Agent가 다른 Agent를 함수처럼 호출 | 높음 | 낮음 |
| **메시지 전달** | 공유 State를 통한 간접 통신 | 중간 | 중간 |
| **이벤트 기반** | 이벤트를 발행하고 구독하는 방식 | 낮음 | 높음 |

```
직접 호출 (높은 결합도)          메시지 전달 (중간 결합도)
┌──────┐     ┌──────┐      ┌──────┐  State  ┌──────┐
│Agent │────▶│Agent │      │Agent │◀──────▶│Agent │
│  A   │     │  B   │      │  A   │  (공유) │  B   │
└──────┘     └──────┘      └──────┘         └──────┘

이벤트 기반 (낮은 결합도)
┌──────┐  event  ┌─────────┐  event  ┌──────┐
│Agent │────────▶│  Event  │────────▶│Agent │
│  A   │         │  Bus    │         │  B   │
└──────┘         └─────────┘         └──────┘
```

LangGraph에서는 **메시지 전달 패턴**이 가장 자연스럽다. 각 Sub-Agent가 자신만의 State를 갖고, Orchestrator가 **어댑터(Adapter)**를 통해 State를 변환하며 중계한다.

**결합도를 낮추는 3가지 전략:**

| 전략 | 설명 |
|------|------|
| **State 분리** | 각 Sub-Agent는 자신만의 State를 갖는다 |
| **인터페이스 계약** | Sub-Agent 간 통신은 명시적 입출력 스키마로 정의 |
| **어댑터 패턴** | Orchestrator가 State 변환을 담당 |

### 예제

```python
from typing import TypedDict, Annotated, Sequence, Protocol
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator


# ============================================================
# 인터페이스 계약: 입출력 스키마를 명확히 정의
# ============================================================

class SummarizerInput(TypedDict):
    """요약 Agent 입력 계약"""
    text: str
    max_length: int


class SummarizerOutput(TypedDict):
    """요약 Agent 출력 계약"""
    summary: str
    original_length: int


class TranslatorInput(TypedDict):
    """번역 Agent 입력 계약"""
    text: str
    target_lang: str


class TranslatorOutput(TypedDict):
    """번역 Agent 출력 계약"""
    translated: str
    target_lang: str


# ============================================================
# 독립 Sub-Agent 구현 (자신만의 State)
# ============================================================

# --- Summarizer Agent ---
class SummarizerState(TypedDict):
    text: str
    max_length: int
    summary: str
    original_length: int


def summarize(state: SummarizerState) -> dict:
    text = state["text"]
    max_len = state["max_length"]
    summary = text[:max_len] + "..." if len(text) > max_len else text
    print(f"  [Summarizer] {len(text)}자 -> {len(summary)}자")
    return {"summary": summary, "original_length": len(text)}


summarizer_graph = StateGraph(SummarizerState)
summarizer_graph.add_node("summarize", summarize)
summarizer_graph.add_edge(START, "summarize")
summarizer_graph.add_edge("summarize", END)
summarizer_agent = summarizer_graph.compile()


# --- Translator Agent ---
class TranslatorState(TypedDict):
    text: str
    target_lang: str
    translated: str


def translate(state: TranslatorState) -> dict:
    translated = f"[{state['target_lang']}] {state['text']}"
    print(f"  [Translator] -> {state['target_lang']}")
    return {"translated": translated}


translator_graph = StateGraph(TranslatorState)
translator_graph.add_node("translate", translate)
translator_graph.add_edge(START, "translate")
translator_graph.add_edge("translate", END)
translator_agent = translator_graph.compile()


# ============================================================
# Orchestrator: 어댑터 패턴으로 State 변환
# ============================================================

class PipelineState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    input_text: str
    target_lang: str
    summary: str
    translated: str
    log: Annotated[list[str], operator.add]


def step_summarize(state: PipelineState) -> dict:
    """Pipeline State -> Summarizer State 변환 (어댑터)"""
    print("[Pipeline] Summarizer 호출")
    result = summarizer_agent.invoke({
        "text": state["input_text"],
        "max_length": 50,
        "summary": "",
        "original_length": 0,
    })
    return {
        "summary": result["summary"],
        "log": [
            f"요약 완료: {result['original_length']}자 -> "
            f"{len(result['summary'])}자"
        ],
    }


def step_translate(state: PipelineState) -> dict:
    """Pipeline State -> Translator State 변환 (어댑터)"""
    print("[Pipeline] Translator 호출")
    result = translator_agent.invoke({
        "text": state["summary"],
        "target_lang": state["target_lang"],
        "translated": "",
    })
    return {
        "translated": result["translated"],
        "log": [f"번역 완료: -> {state['target_lang']}"],
        "messages": [AIMessage(content=result["translated"])],
    }


pipeline_graph = StateGraph(PipelineState)
pipeline_graph.add_node("summarize", step_summarize)
pipeline_graph.add_node("translate", step_translate)
pipeline_graph.add_edge(START, "summarize")
pipeline_graph.add_edge("summarize", "translate")
pipeline_graph.add_edge("translate", END)
pipeline_app = pipeline_graph.compile()

# 실행
print("=== 요약 + 번역 파이프라인 (어댑터 패턴) ===")
result = pipeline_app.invoke({
    "messages": [HumanMessage(content="문서 처리 요청")],
    "input_text": "인공지능 에이전트는 목표를 설정하고 자율적으로 행동하는 시스템입니다. "
                  "LLM을 두뇌로, Tool을 손발로 사용하여 복잡한 작업을 수행합니다.",
    "target_lang": "en",
    "summary": "",
    "translated": "",
    "log": [],
})

print(f"\n요약: {result['summary']}")
print(f"번역: {result['translated']}")
print(f"로그: {result['log']}")
```

**실행 결과:**
```
=== 요약 + 번역 파이프라인 (어댑터 패턴) ===
[Pipeline] Summarizer 호출
  [Summarizer] 68자 -> 53자
[Pipeline] Translator 호출
  [Translator] -> en

요약: 인공지능 에이전트는 목표를 설정하고 자율적으로 행동하는 시스템입니다. LLM을 두뇌로, T...
번역: [en] 인공지능 에이전트는 목표를 설정하고 자율적으로 행동하는 시스템입니다. LLM을 두뇌로, T...
로그: ['요약 완료: 68자 -> 53자', '번역 완료: -> en']
```

**핵심 포인트:**
- `Summarizer`와 `Translator`는 서로를 전혀 모른다 (결합도 = 0)
- Orchestrator의 어댑터 함수가 State 변환을 담당한다
- Sub-Agent를 교체해도 어댑터만 수정하면 된다

### Q&A

**Q: 어댑터 패턴이 오히려 코드량을 늘리지 않나요?**
A: 단기적으로는 그렇다. 하지만 장기적으로 (1) Sub-Agent를 독립적으로 테스트할 수 있고, (2) Sub-Agent를 다른 파이프라인에서 재사용할 수 있으며, (3) Sub-Agent를 교체해도 다른 컴포넌트에 영향이 없다. Agent가 3개 이상이면 어댑터 패턴의 이점이 코드량 증가를 상회한다.

**Q: 이벤트 기반 통신을 LangGraph에서 구현할 수 있나요?**
A: 직접 지원하지는 않지만, State에 `events: Annotated[list[dict], operator.add]` 필드를 추가하여 이벤트 큐를 시뮬레이션할 수 있다. 각 Agent가 이벤트를 발행(State에 추가)하고, 라우팅 함수가 이벤트를 읽어서 적절한 Agent로 전달하는 방식이다. 프로덕션에서는 Redis Pub/Sub이나 Kafka를 연동하기도 한다.

<details>
<summary>퀴즈: 다음 코드에서 결합도 문제를 찾으세요</summary>

```python
def analyze_node(state):
    raw = state["_search_internal_cache"]
    parsed = state["search_results"]["_raw_response"]["body"]
    return {"analysis": process(raw, parsed)}
```

**힌트**: 이 Node가 접근하는 State 필드의 이름을 보세요. `_` 접두사와 중첩 구조에 주목하세요.

**정답**: (1) `_search_internal_cache`는 search_node의 **내부 구현 상세**(private 필드)에 직접 의존한다. search_node가 캐시 구조를 변경하면 analyze_node가 깨진다. (2) `["_raw_response"]["body"]` 같은 깊은 중첩 접근은 search_node의 응답 구조에 강하게 결합되어 있다. 해결: 어댑터에서 필요한 데이터만 추출하여 `analysis_input` 같은 공개 필드로 전달한다.
</details>

---

## 3. LangGraph 서브그래프(Subgraph) 활용

### 개념 설명

LangGraph는 **서브그래프(Subgraph)**를 네이티브로 지원한다. 서브그래프는 하나의 컴파일된 그래프를 다른 그래프의 Node로 사용하는 기능이다.

서브그래프의 개념은 프로그래밍에서 **함수 추상화**가 등장한 이유와 같다. 복잡한 프로그램을 하나의 main 함수에 모두 작성하면 이해할 수 없는 코드가 된다. 함수로 분리하면 각 함수는 이름만으로 "무엇을 하는지" 드러내고, 내부 구현은 감춘다. 서브그래프는 이 원리를 **그래프 단위**로 확장한 것이다. `add_node("collect", collection_subgraph)`라는 한 줄이 내부적으로 수집, 검증, 재시도까지 포함하는 복잡한 워크플로를 캡슐화한다.

캡슐화(Encapsulation)의 실질적 가치는 **인지 부하 감소**에 있다. 부모 그래프를 읽는 개발자는 `init -> collect -> analyze -> report`라는 4단계 흐름만 파악하면 된다. 각 서브그래프의 내부가 5개의 Node와 복잡한 Conditional Edge를 가지고 있더라도, 그것은 해당 서브그래프를 수정할 때만 알면 된다. George Miller의 연구에 따르면 인간의 작업 기억(Working Memory)은 7±2개 항목만 동시에 처리할 수 있으므로, 서브그래프로 추상화 수준을 계층화하는 것은 인지 과학적으로도 합리적인 설계 전략이다.

서브그래프의 **State 공유 메커니즘**은 특히 주목할 만하다. 부모 State와 서브그래프 State에서 **동일한 키 이름**을 가진 필드가 자동으로 연결된다. 이것은 이름 기반 매핑(Name-based Mapping)으로, 명시적 바인딩 없이도 데이터가 흐를 수 있게 한다. 반대로 서브그래프에만 존재하는 키(예: `retry_count`, `collection_status`)는 부모에게 노출되지 않는다. 이 메커니즘이 캡슐화의 핵심이다. 서브그래프의 내부 구현 상세(재시도 횟수, 중간 상태 등)가 부모로 누출되지 않으므로, 서브그래프 내부를 자유롭게 리팩토링할 수 있다. 다만 이 이름 기반 매핑에는 주의점이 있다. 부모와 서브그래프에서 **같은 이름이지만 다른 의미**의 필드를 사용하면 데이터 충돌이 발생한다. 따라서 공유 키에 대해서는 팀 내에서 **명명 규칙(Naming Convention)**을 합의하고, 가능하면 공유 키의 수를 최소화하는 것이 안전하다.

```
┌─────────────────────────────────────────────────┐
│              Parent Graph                        │
│                                                  │
│  [START] ──▶ [Node A] ──▶ ┌──────────────┐     │
│                             │  Subgraph    │     │
│                             │ ┌──────────┐ │     │
│                             │ │ Node X   │ │     │
│                             │ └────┬─────┘ │     │
│                             │      ▼       │     │
│                             │ ┌──────────┐ │     │
│                             │ │ Node Y   │ │     │
│                             │ └──────────┘ │     │
│                             └──────┬───────┘     │
│                                    ▼             │
│                              [Node B] ──▶ [END]  │
└─────────────────────────────────────────────────┘
```

**서브그래프의 이점:**

| 이점 | 설명 |
|------|------|
| **캡슐화** | 서브그래프 내부 로직이 외부에 노출되지 않음 |
| **재사용** | 동일 서브그래프를 여러 부모 그래프에서 사용 가능 |
| **독립 테스트** | 서브그래프를 단독으로 컴파일하고 테스트 가능 |
| **점진적 확장** | 기존 Node를 서브그래프로 교체하여 복잡도 분산 |

**서브그래프 사용 시 핵심 규칙:**
- 부모 그래프와 서브그래프는 **State 키를 공유**해야 한다 (겹치는 키로 데이터 전달)
- 서브그래프가 부모 State에 없는 키를 사용하면 **내부 전용** 데이터가 된다
- 서브그래프의 `START`/`END`는 부모 그래프의 Edge 연결점이 된다

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator


# ============================================================
# 서브그래프 1: 데이터 수집 파이프라인
# ============================================================

class CollectionState(TypedDict):
    """데이터 수집 서브그래프 State"""
    query: str
    raw_data: list[str]        # 부모와 공유하는 키
    collection_status: str     # 서브그래프 내부 전용 키
    retry_count: int           # 서브그래프 내부 전용 키


def collect_data(state: CollectionState) -> dict:
    """데이터 수집"""
    query = state["query"]
    data = [
        f"[소스A] {query} 관련 데이터 1",
        f"[소스B] {query} 관련 데이터 2",
        f"[소스C] {query} 관련 데이터 3",
    ]
    print(f"  [수집] {len(data)}건 수집 완료")
    return {"raw_data": data, "collection_status": "collected"}


def validate_data(state: CollectionState) -> dict:
    """수집 데이터 검증"""
    valid_count = len(state["raw_data"])
    status = "valid" if valid_count >= 2 else "insufficient"
    print(f"  [검증] {valid_count}건 - {status}")
    return {"collection_status": status}


def route_validation(state: CollectionState) -> str:
    if state["collection_status"] == "valid":
        return "done"
    if state["retry_count"] < 2:
        return "retry"
    return "done"


collection_graph = StateGraph(CollectionState)
collection_graph.add_node("collect", collect_data)
collection_graph.add_node("validate", validate_data)
collection_graph.add_edge(START, "collect")
collection_graph.add_edge("collect", "validate")
collection_graph.add_conditional_edges(
    "validate",
    route_validation,
    {"done": END, "retry": "collect"},
)
collection_subgraph = collection_graph.compile()


# ============================================================
# 서브그래프 2: 분석 파이프라인
# ============================================================

class AnalysisPipelineState(TypedDict):
    """분석 서브그래프 State"""
    raw_data: list[str]       # 부모로부터 전달받는 키
    insights: list[str]       # 부모에게 전달하는 키
    analysis_method: str      # 서브그래프 내부 전용


def extract_patterns(state: AnalysisPipelineState) -> dict:
    """패턴 추출"""
    patterns = [f"패턴_{i}: {d[:20]}에서 추출" for i, d in enumerate(state["raw_data"])]
    print(f"  [패턴 추출] {len(patterns)}개 패턴 발견")
    return {"insights": patterns, "analysis_method": "pattern_extraction"}


def synthesize(state: AnalysisPipelineState) -> dict:
    """인사이트 종합"""
    summary = [f"인사이트: {len(state['insights'])}개 패턴 기반 종합 분석"]
    print(f"  [종합] {summary[0]}")
    return {"insights": summary}


analysis_graph = StateGraph(AnalysisPipelineState)
analysis_graph.add_node("extract", extract_patterns)
analysis_graph.add_node("synthesize", synthesize)
analysis_graph.add_edge(START, "extract")
analysis_graph.add_edge("extract", "synthesize")
analysis_graph.add_edge("synthesize", END)
analysis_subgraph = analysis_graph.compile()


# ============================================================
# 부모 그래프: 서브그래프를 Node로 사용
# ============================================================

class ParentState(TypedDict):
    """부모 그래프 State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    raw_data: list[str]       # 서브그래프와 공유
    insights: list[str]       # 서브그래프와 공유
    final_report: str


def init_node(state: ParentState) -> dict:
    """초기화 Node"""
    print(f"[Parent] 쿼리: {state['query']}")
    return {}


def report_node(state: ParentState) -> dict:
    """최종 보고서 생성"""
    insights_text = "; ".join(state["insights"])
    report = f"[보고서] 쿼리: {state['query']} | {insights_text}"
    print(f"[Parent] 보고서 생성 완료")
    return {
        "final_report": report,
        "messages": [AIMessage(content=report)],
    }


# 부모 그래프 구성 - 서브그래프를 Node로 등록
parent_graph = StateGraph(ParentState)

parent_graph.add_node("init", init_node)
parent_graph.add_node("collect", collection_subgraph)   # 서브그래프를 Node로!
parent_graph.add_node("analyze", analysis_subgraph)     # 서브그래프를 Node로!
parent_graph.add_node("report", report_node)

parent_graph.add_edge(START, "init")
parent_graph.add_edge("init", "collect")
parent_graph.add_edge("collect", "analyze")
parent_graph.add_edge("analyze", "report")
parent_graph.add_edge("report", END)

parent_app = parent_graph.compile()


# 실행
print("=== 서브그래프 활용 예제 ===")
result = parent_app.invoke({
    "messages": [HumanMessage(content="AI 시장 분석 요청")],
    "query": "AI Agent 시장 동향",
    "raw_data": [],
    "insights": [],
    "final_report": "",
})

print(f"\n=== 최종 결과 ===")
print(f"수집 데이터: {len(result['raw_data'])}건")
print(f"인사이트: {result['insights']}")
print(f"보고서: {result['final_report']}")
```

**실행 결과:**
```
=== 서브그래프 활용 예제 ===
[Parent] 쿼리: AI Agent 시장 동향
  [수집] 3건 수집 완료
  [검증] 3건 - valid
  [패턴 추출] 3개 패턴 발견
  [종합] 인사이트: 3개 패턴 기반 종합 분석
[Parent] 보고서 생성 완료

=== 최종 결과 ===
수집 데이터: 3건
인사이트: ['인사이트: 3개 패턴 기반 종합 분석']
보고서: [보고서] 쿼리: AI Agent 시장 동향 | 인사이트: 3개 패턴 기반 종합 분석
```

### Q&A

**Q: 서브그래프를 `add_node`에 직접 전달하면 State는 어떻게 공유되나요?**
A: 부모 State와 서브그래프 State에서 **같은 이름의 키**가 자동으로 공유된다. 예제에서 `raw_data`와 `insights`는 양쪽 State에 동일한 이름으로 존재하므로 자동 전달된다. 서브그래프의 `collection_status`, `retry_count` 같은 키는 부모 State에 없으므로 서브그래프 내부에서만 사용된다.

**Q: 서브그래프 내부에서 에러가 발생하면 부모 그래프에 어떤 영향이 있나요?**
A: 서브그래프의 에러는 **그대로 부모 그래프로 전파**된다. 따라서 서브그래프 내부에서 자체적으로 에러 핸들링(Retry, Fallback)을 구현하거나, 부모 그래프에서 서브그래프 Node 이후에 에러 체크 Conditional Edge를 추가해야 한다.

<details>
<summary>퀴즈: 서브그래프의 `retry_count` 필드가 부모 그래프에서 접근 불가능한 이유는?</summary>

**힌트**: 부모 그래프의 `ParentState`에 `retry_count` 키가 정의되어 있나요?

**정답**: `ParentState`에 `retry_count` 키가 없기 때문이다. LangGraph에서 서브그래프의 출력은 **부모 State에 존재하는 키만** 전달한다. `retry_count`는 `CollectionState`에만 존재하므로 서브그래프 실행이 끝나면 사라진다. 이것이 **캡슐화**의 핵심 메커니즘이다. 필요하다면 부모 State에 해당 키를 추가하여 노출할 수 있다.
</details>

---

## 4. 상태 관리 확장: 체크포인트와 메모리 관리

### 개념 설명

프로덕션 Agent에서는 **장기 실행**, **중단 후 재개**, **대화 히스토리 관리** 등 확장된 상태 관리가 필요하다. LangGraph는 **체크포인터(Checkpointer)**를 통해 이를 지원한다.

체크포인트는 본질적으로 **게임의 세이브 포인트**와 같다. 게임에서 보스전 직전에 저장하면, 실패해도 처음부터 다시 시작할 필요가 없다. Agent 시스템도 마찬가지다. LLM API 호출은 비용이 발생하고, 외부 Tool 실행은 시간이 걸린다. 10단계 워크플로의 8단계에서 네트워크 오류가 발생했을 때, 체크포인트가 없으면 1단계부터 다시 실행해야 한다. 체크포인트가 있으면 7단계의 State를 복원하고 8단계부터 재개할 수 있다. 이것은 단순한 편의 기능이 아니라, **프로덕션 환경의 안정성(Reliability)**을 보장하는 핵심 인프라다.

**Thread 개념**은 웹 애플리케이션의 **세션(Session)**과 동일한 역할을 한다. 웹 서버가 쿠키나 세션 ID로 사용자별 상태를 분리하듯, LangGraph는 `thread_id`로 대화별 State를 격리한다. `user_123`의 3턴짜리 대화와 `user_456`의 1턴짜리 대화가 서로 간섭하지 않는 것은, 각 thread_id가 독립적인 State 스냅샷 체인을 유지하기 때문이다. 이 설계는 멀티 테넌트(Multi-tenant) 서비스에서 필수적이다.

**메모리 프루닝(Memory Pruning)**은 LLM 기반 Agent에서 특히 중요한 문제다. LLM은 컨텍스트 윈도우라는 물리적 한계를 가지고 있으며, 대화가 길어질수록 (1) 토큰 비용이 선형 증가하고, (2) 컨텍스트가 길면 LLM의 주의력(attention)이 분산되어 응답 품질이 저하되는 "Lost in the Middle" 현상이 발생한다. 실무에서는 세 가지 전략을 조합한다. **슬라이딩 윈도우**(최근 N개 메시지만 유지)는 가장 단순하지만 초기 맥락을 잃는다. **요약 압축**(오래된 대화를 LLM으로 요약)은 맥락을 보존하지만 요약 과정에서 추가 비용이 발생한다. **중요 정보 추출**(사용자 이름, 선호도 등을 별도 저장)은 장기 기억으로 기능하여 개인화된 서비스를 가능하게 한다. 저장소 선택도 중요한데, `MemorySaver`는 개발/테스트용이고, 프로덕션에서는 반드시 `SqliteSaver`(단일 서버)나 `PostgresSaver`(분산 환경)를 사용해야 한다. 서버 재시작, 프로세스 크래시, 배포 등의 상황에서 State가 유실되면 사용자 경험이 심각하게 훼손되기 때문이다.

**상태 관리 확장 3대 요소:**

| 요소 | 설명 | 사용 사례 |
|------|------|----------|
| **Checkpointer** | State를 외부 저장소에 자동 저장/복원 | 장기 실행 Agent, 서버 재시작 후 복원 |
| **Thread** | 대화/세션 단위로 State를 분리 | 다중 사용자 동시 서비스 |
| **Memory Pruning** | 오래된 State 정리하여 메모리 절약 | 대화 히스토리 관리, 장기 실행 |

```
┌─────────────────────────────────────────────────┐
│                   Agent 실행                     │
│                                                  │
│  Thread: user_123                                │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐   │
│  │Step 1 │─▶│Step 2 │─▶│Step 3 │─▶│Step 4 │   │
│  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘   │
│      │          │          │           │        │
│      ▼          ▼          ▼           ▼        │
│  [Check-    [Check-    [Check-     [Check-      │
│   point 1]  point 2]  point 3]    point 4]     │
│      │          │          │           │        │
│      └──────────┴──────────┴───────────┘        │
│                      │                           │
│                      ▼                           │
│              [외부 저장소]                        │
│              (SQLite / Redis / PostgreSQL)        │
└─────────────────────────────────────────────────┘
```

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import operator


class ConversationState(TypedDict):
    """체크포인트 데모용 대화 State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    turn_count: int
    context_summary: str


def process_message(state: ConversationState) -> dict:
    """사용자 메시지를 처리하고 응답을 생성한다."""
    user_msg = state["messages"][-1].content
    turn = state["turn_count"]

    # 턴 수에 따라 다른 응답 (시뮬레이션)
    response = f"[턴 {turn + 1}] '{user_msg}'에 대한 응답입니다."
    print(f"[Agent] {response}")

    return {
        "messages": [AIMessage(content=response)],
        "turn_count": turn + 1,
    }


def update_context(state: ConversationState) -> dict:
    """대화 맥락을 요약 업데이트한다."""
    msg_count = len(state["messages"])
    summary = f"총 {msg_count}개 메시지, {state['turn_count']}턴 진행"
    print(f"[Context] {summary}")
    return {"context_summary": summary}


# 그래프 구성
graph = StateGraph(ConversationState)
graph.add_node("process", process_message)
graph.add_node("update_context", update_context)
graph.add_edge(START, "process")
graph.add_edge("process", "update_context")
graph.add_edge("update_context", END)

# 체크포인터 설정 (인메모리 - 프로덕션에서는 SQLite/Redis 사용)
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)


# Thread ID로 세션 분리
thread_config = {"configurable": {"thread_id": "user_123"}}

# 첫 번째 대화
print("=== 대화 1: 첫 번째 메시지 ===")
result1 = app.invoke(
    {
        "messages": [HumanMessage(content="AI Agent란 무엇인가요?")],
        "turn_count": 0,
        "context_summary": "",
    },
    config=thread_config,
)

# 두 번째 대화 (이전 대화가 체크포인트에서 복원됨)
print("\n=== 대화 2: 이어서 질문 ===")
result2 = app.invoke(
    {
        "messages": [HumanMessage(content="LangGraph와의 관계는?")],
    },
    config=thread_config,
)

# 세 번째 대화
print("\n=== 대화 3: 추가 질문 ===")
result3 = app.invoke(
    {
        "messages": [HumanMessage(content="실무에서 어떻게 쓰나요?")],
    },
    config=thread_config,
)

# 상태 확인
print(f"\n=== 최종 상태 ===")
print(f"총 메시지 수: {len(result3['messages'])}")
print(f"턴 수: {result3['turn_count']}")
print(f"컨텍스트: {result3['context_summary']}")

# 다른 사용자는 별도 Thread
other_config = {"configurable": {"thread_id": "user_456"}}
print("\n=== 다른 사용자 (user_456) ===")
other_result = app.invoke(
    {
        "messages": [HumanMessage(content="안녕하세요")],
        "turn_count": 0,
        "context_summary": "",
    },
    config=other_config,
)
print(f"user_456 턴 수: {other_result['turn_count']} (독립적)")
```

**실행 결과:**
```
=== 대화 1: 첫 번째 메시지 ===
[Agent] [턴 1] 'AI Agent란 무엇인가요?'에 대한 응답입니다.
[Context] 총 2개 메시지, 1턴 진행

=== 대화 2: 이어서 질문 ===
[Agent] [턴 2] 'LangGraph와의 관계는?'에 대한 응답입니다.
[Context] 총 4개 메시지, 2턴 진행

=== 대화 3: 추가 질문 ===
[Agent] [턴 3] '실무에서 어떻게 쓰나요?'에 대한 응답입니다.
[Context] 총 6개 메시지, 3턴 진행

=== 최종 상태 ===
총 메시지 수: 6
턴 수: 3
컨텍스트: 총 6개 메시지, 3턴 진행

=== 다른 사용자 (user_456) ===
[Agent] [턴 1] '안녕하세요'에 대한 응답입니다.
[Context] 총 2개 메시지, 1턴 진행
user_456 턴 수: 1 (독립적)
```

**핵심 관찰:**
- `thread_id`가 같으면 이전 대화 State가 **자동으로 복원**된다
- `user_123`은 3턴까지 대화가 누적되고, `user_456`은 독립적으로 1턴만 진행
- `MemorySaver`는 프로세스 메모리에 저장 (프로덕션에서는 `SqliteSaver` 또는 `PostgresSaver` 사용)

### Q&A

**Q: 대화 히스토리가 계속 쌓이면 LLM 컨텍스트 윈도우를 초과하지 않나요?**
A: 맞다. 이것이 **메모리 프루닝(Memory Pruning)**이 필요한 이유다. 실무에서는 (1) 최근 N개 메시지만 유지 (슬라이딩 윈도우), (2) 오래된 대화를 요약하여 압축, (3) 중요 정보만 추출하여 별도 저장하는 전략을 조합한다. LangGraph에서는 State의 `messages` 필드에 커스텀 reducer를 적용하여 자동 프루닝을 구현할 수 있다.

**Q: 체크포인터를 사용하면 성능에 영향이 있나요?**
A: `MemorySaver`는 인메모리이므로 성능 영향이 거의 없다. `SqliteSaver`는 로컬 디스크 I/O가 발생하지만 대부분의 사용 사례에서 무시할 수준이다. `PostgresSaver`는 네트워크 I/O가 추가되므로, 연결 풀링과 비동기 I/O를 활용해야 한다. 핵심은 Node 실행 시간 대비 체크포인트 저장 시간이 **충분히 작아야** 한다는 것이다.

<details>
<summary>퀴즈: `thread_id`가 "user_123"인 상태에서 서버가 재시작되면, `MemorySaver`의 데이터는 어떻게 되나요?</summary>

**힌트**: `MemorySaver`는 "인메모리" 저장소입니다. 프로세스가 종료되면 메모리는?

**정답**: **모든 데이터가 유실**된다. `MemorySaver`는 프로세스 메모리에 저장하므로 서버 재시작 시 체크포인트가 사라진다. 프로덕션에서는 반드시 **영속 저장소**(`SqliteSaver`, `PostgresSaver`)를 사용해야 한다. `SqliteSaver`는 파일 기반이므로 프로세스 재시작 후에도 데이터가 보존된다.
</details>

---

## 5. 리팩토링 전략: 모놀리식 Agent에서 모듈형 Agent로

### 개념 설명

모놀리식 Agent를 모듈형으로 전환하는 과정은 **점진적**이어야 한다. 한 번에 전부 리팩토링하면 기존 동작이 깨질 위험이 크다.

리팩토링(Refactoring)이란 Martin Fowler의 정의에 따르면 **"외부 동작을 변경하지 않으면서 내부 구조를 개선하는 것"**이다. 이 정의에서 핵심은 "외부 동작 변경 없이"라는 제약이다. 리팩토링과 기능 추가를 동시에 하면 문제가 생겼을 때 원인이 구조 변경인지 기능 변경인지 구분할 수 없다. 따라서 리팩토링은 항상 **기존 동작을 보장하는 테스트를 먼저 작성**하고, 테스트가 통과하는 상태를 유지하면서 구조를 변경해야 한다. Agent 시스템에서 이 "테스트"는 동일한 입력(`query`)에 대해 동일한 출력(`report`)이 나오는지 확인하는 통합 테스트다.

점진적 접근이 필수인 이유는 **Big Bang 리팩토링의 실패율**이 극도로 높기 때문이다. 실무에서 "주말 동안 전체 구조를 갈아엎겠다"는 시도는 대부분 월요일에 롤백으로 끝난다. 5단계 전략에서 가장 중요한 단계는 첫 번째인 **의존성 분석**이다. 각 Node가 State의 어떤 필드를 읽고(Read) 어떤 필드를 쓰는지(Write)를 매트릭스로 시각화하면, 자연스러운 분리 경계가 드러난다. 읽기/쓰기 의존성이 겹치지 않는 Node 그룹이 독립적인 Sub-Agent 후보다. 반대로 여러 그룹이 동일한 필드를 읽고 쓴다면, 그 필드는 공유 인터페이스로 승격되어야 한다.

실무에서 자주 간과되는 것이 **유지보수 가능한 구조의 기준**이다. 코드가 "돌아가는 것"과 "유지보수 가능한 것"은 전혀 다르다. 아래 6대 기준은 Robert C. Martin의 SOLID 원칙과 실용주의 프로그래밍(Pragmatic Programming)의 원칙에서 Agent 개발에 적용 가능한 것들을 선별한 것이다. 특히 **"테스트 가능"** 기준이 핵심인데, Node 함수를 Mock 없이 직접 호출하여 테스트할 수 있다면 그 Node는 올바르게 분리된 것이다. 반대로 특정 Node를 테스트하기 위해 전체 그래프를 실행해야 한다면, 그 Node는 다른 Node에 과도하게 의존하고 있다는 신호다. **"설정 가능(Configurable)"** 기준은 하드코딩을 제거하여 동일한 코드를 개발/스테이징/프로덕션 환경에서 다르게 동작시킬 수 있게 하는 것으로, 12-Factor App 방법론의 "설정을 환경에 저장하라"는 원칙의 Agent 버전이다.

**5단계 리팩토링 전략:**

```
Step 1           Step 2           Step 3           Step 4           Step 5
의존성 분석 ──▶ 인터페이스 ──▶ Sub-Agent ──▶ Orchestrator ──▶ 검증 및
               정의             분리            연결            최적화

[의존성 그래프  [입출력 스키마  [독립 그래프   [어댑터로      [동일 결과
 작성]          확정]          생성]          조합]          확인]
```

| 단계 | 목표 | 산출물 |
|------|------|--------|
| **의존성 분석** | Node 간 읽기/쓰기 필드 매핑 | 의존성 매트릭스 |
| **인터페이스 정의** | Sub-Agent 입출력 계약 확정 | TypedDict 스키마 |
| **Sub-Agent 분리** | 독립 실행 가능한 그래프 생성 | 서브그래프 N개 |
| **Orchestrator 연결** | 어댑터로 Sub-Agent 조합 | 부모 그래프 |
| **검증 및 최적화** | 리팩토링 전후 동일 결과 확인 | 통합 테스트 |

**유지보수 가능한 구조 6대 기준:**

| 기준 | 설명 | 검증 방법 |
|------|------|----------|
| **단일 책임** | 각 Node는 하나의 명확한 역할 | Node 이름만으로 역할 설명 가능한가? |
| **테스트 가능** | Node를 독립적으로 테스트 가능 | Mock 없이 Node 함수를 직접 호출 가능한가? |
| **교체 가능** | 특정 Node를 교체해도 다른 Node에 영향 없음 | State 인터페이스만 맞으면 교체 가능한가? |
| **추적 가능** | 실행 흐름을 Trace로 재현 가능 | Trace 로그로 버그 원인을 특정할 수 있는가? |
| **설정 가능** | 하드코딩 없이 동작을 변경 가능 | 환경 변수나 설정 파일로 동작 조절이 가능한가? |
| **점진적 확장** | 기존 코드 수정 없이 기능 추가 가능 | 새 Node 추가만으로 기능 확장이 가능한가? |

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from dataclasses import dataclass
import operator


# ============================================================
# Step 1: 의존성 분석 - 모놀리식 Agent의 Node별 읽기/쓰기 매핑
# ============================================================

DEPENDENCY_MATRIX = """
=== 의존성 매트릭스 ===
Node           | 읽기 필드               | 쓰기 필드
─────────────────────────────────────────────────────────
search         | query                   | search_results
filter         | search_results          | filtered_results
analyze        | filtered_results        | analysis
summarize      | analysis                | summary
report         | summary, analysis       | report

=> 자연스러운 경계:
   Group A: search + filter        (데이터 수집)
   Group B: analyze + summarize    (분석)
   Group C: report                 (출력)
"""


# ============================================================
# Step 2-3: 인터페이스 정의 + Sub-Agent 분리
# ============================================================

@dataclass
class AgentConfig:
    """Agent 동작을 외부에서 설정"""
    max_results: int = 10
    summary_max_length: int = 100
    trace_enabled: bool = True


# --- Sub-Agent: DataCollector ---
class CollectorState(TypedDict):
    query: str
    max_results: int
    results: list[str]


def collect_and_filter(state: CollectorState) -> dict:
    """데이터 수집 + 필터링을 하나의 Sub-Agent에서 처리"""
    max_r = state["max_results"]
    raw = [f"raw_{state['query']}_{i}" for i in range(max_r + 2)]
    filtered = [r for r in raw if not r.endswith("_0")]  # 첫 번째 제외
    print(f"  [Collector] 수집: {len(raw)}건 -> 필터: {len(filtered)}건")
    return {"results": filtered}


collector_graph = StateGraph(CollectorState)
collector_graph.add_node("collect_filter", collect_and_filter)
collector_graph.add_edge(START, "collect_filter")
collector_graph.add_edge("collect_filter", END)
collector_agent = collector_graph.compile()


# --- Sub-Agent: Analyzer ---
class AnalyzerState(TypedDict):
    data: list[str]
    summary_max_length: int
    analysis: str
    summary: str


def analyze_and_summarize(state: AnalyzerState) -> dict:
    """분석 + 요약을 하나의 Sub-Agent에서 처리"""
    data = state["data"]
    analysis = f"분석: {len(data)}건 데이터에서 핵심 패턴 발견"
    summary = analysis[:state["summary_max_length"]]
    print(f"  [Analyzer] {analysis}")
    print(f"  [Analyzer] 요약: {summary}")
    return {"analysis": analysis, "summary": summary}


analyzer_graph = StateGraph(AnalyzerState)
analyzer_graph.add_node("analyze_summarize", analyze_and_summarize)
analyzer_graph.add_edge(START, "analyze_summarize")
analyzer_graph.add_edge("analyze_summarize", END)
analyzer_agent = analyzer_graph.compile()


# --- Sub-Agent: Reporter ---
class ReporterState(TypedDict):
    summary: str
    analysis: str
    report: str


def generate_report(state: ReporterState) -> dict:
    """최종 보고서 생성"""
    report = f"[보고서]\n요약: {state['summary']}\n상세: {state['analysis']}"
    print(f"  [Reporter] 보고서 생성 완료")
    return {"report": report}


reporter_graph = StateGraph(ReporterState)
reporter_graph.add_node("report", generate_report)
reporter_graph.add_edge(START, "report")
reporter_graph.add_edge("report", END)
reporter_agent = reporter_graph.compile()


# ============================================================
# Step 4: Orchestrator - 어댑터로 Sub-Agent 연결
# ============================================================

class OrchestratorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    config: dict
    collected_data: list[str]
    analysis: str
    summary: str
    report: str
    log: Annotated[list[str], operator.add]


def create_collector_adapter(config: AgentConfig):
    """Collector 어댑터 팩토리"""
    def adapter(state: OrchestratorState) -> dict:
        print("[Orchestrator] Collector 호출")
        result = collector_agent.invoke({
            "query": state["query"],
            "max_results": config.max_results,
            "results": [],
        })
        return {
            "collected_data": result["results"],
            "log": [f"수집 완료: {len(result['results'])}건"],
        }
    return adapter


def create_analyzer_adapter(config: AgentConfig):
    """Analyzer 어댑터 팩토리"""
    def adapter(state: OrchestratorState) -> dict:
        print("[Orchestrator] Analyzer 호출")
        result = analyzer_agent.invoke({
            "data": state["collected_data"],
            "summary_max_length": config.summary_max_length,
            "analysis": "",
            "summary": "",
        })
        return {
            "analysis": result["analysis"],
            "summary": result["summary"],
            "log": [f"분석 완료: {result['summary'][:30]}..."],
        }
    return adapter


def create_reporter_adapter():
    """Reporter 어댑터 팩토리"""
    def adapter(state: OrchestratorState) -> dict:
        print("[Orchestrator] Reporter 호출")
        result = reporter_agent.invoke({
            "summary": state["summary"],
            "analysis": state["analysis"],
            "report": "",
        })
        return {
            "report": result["report"],
            "messages": [AIMessage(content=result["report"])],
            "log": ["보고서 생성 완료"],
        }
    return adapter


# 설정 기반 그래프 구성
config = AgentConfig(max_results=3, summary_max_length=50, trace_enabled=True)

orch_graph = StateGraph(OrchestratorState)
orch_graph.add_node("collect", create_collector_adapter(config))
orch_graph.add_node("analyze", create_analyzer_adapter(config))
orch_graph.add_node("report", create_reporter_adapter())
orch_graph.add_edge(START, "collect")
orch_graph.add_edge("collect", "analyze")
orch_graph.add_edge("analyze", "report")
orch_graph.add_edge("report", END)
orch_app = orch_graph.compile()


# ============================================================
# Step 5: 검증 - 리팩토링 전후 결과 비교
# ============================================================

print("=== 모듈형 Agent 실행 ===")
result = orch_app.invoke({
    "messages": [HumanMessage(content="시장 분석 요청")],
    "query": "AI Agent",
    "config": {},
    "collected_data": [],
    "analysis": "",
    "summary": "",
    "report": "",
    "log": [],
})

print(f"\n=== 실행 로그 ===")
for entry in result["log"]:
    print(f"  - {entry}")

print(f"\n=== 최종 보고서 ===")
print(result["report"])


# --- 독립 테스트 데모 ---
print("\n=== Sub-Agent 독립 테스트 ===")

# Collector만 단독 테스트
collector_result = collector_agent.invoke({
    "query": "test_query",
    "max_results": 2,
    "results": [],
})
assert len(collector_result["results"]) > 0
print(f"Collector 테스트 통과: {len(collector_result['results'])}건")

# Analyzer만 단독 테스트
analyzer_result = analyzer_agent.invoke({
    "data": ["data_1", "data_2"],
    "summary_max_length": 30,
    "analysis": "",
    "summary": "",
})
assert len(analyzer_result["analysis"]) > 0
print(f"Analyzer 테스트 통과: {analyzer_result['analysis'][:30]}...")
```

**실행 결과:**
```
=== 모듈형 Agent 실행 ===
[Orchestrator] Collector 호출
  [Collector] 수집: 5건 -> 필터: 4건
[Orchestrator] Analyzer 호출
  [Analyzer] 분석: 4건 데이터에서 핵심 패턴 발견
  [Analyzer] 요약: 분석: 4건 데이터에서 핵심 패턴 발견
[Orchestrator] Reporter 호출
  [Reporter] 보고서 생성 완료

=== 실행 로그 ===
  - 수집 완료: 4건
  - 분석 완료: 분석: 4건 데이터에서 핵심 패턴 발견...
  - 보고서 생성 완료

=== 최종 보고서 ===
[보고서]
요약: 분석: 4건 데이터에서 핵심 패턴 발견
상세: 분석: 4건 데이터에서 핵심 패턴 발견

=== Sub-Agent 독립 테스트 ===
  [Collector] 수집: 4건 -> 필터: 3건
Collector 테스트 통과: 3건
  [Analyzer] 분석: 2건 데이터에서 핵심 패턴 발견
  [Analyzer] 요약: 분석: 2건 데이터에서 핵심 패턴 발견
Analyzer 테스트 통과: 분석: 2건 데이터에서 핵심 패턴 발견...
```

### Q&A

**Q: 팩토리 패턴이 LangGraph에서 왜 유용한가요?**
A: LangGraph의 `add_node`는 함수를 받는다. 팩토리 패턴으로 함수를 생성하면, 같은 구조의 Node를 다른 구현으로 교체할 수 있다. 테스트에서는 mock 함수를, 프로덕션에서는 실제 함수를 주입한다. 이것이 의존성 주입(DI)의 함수형 버전이다.

**Q: 리팩토링 중에 기존 API(입출력)를 유지해야 하나요?**
A: 반드시 유지해야 한다. 리팩토링의 핵심 원칙은 **외부 동작 변경 없이 내부 구조를 개선**하는 것이다. Orchestrator의 입력(`query`)과 출력(`report`)이 리팩토링 전후로 동일해야 한다. 이를 보장하기 위해 리팩토링 전에 **통합 테스트를 먼저 작성**하고, 리팩토링 후 동일 테스트를 통과하는지 확인한다.

<details>
<summary>퀴즈: 유지보수 가능한 구조 6대 기준 중, "설정 가능"이 중요한 이유는?</summary>

**힌트**: 같은 Agent를 개발 환경과 프로덕션 환경에서 실행해야 합니다. `max_results`가 개발에서는 3, 프로덕션에서는 100이라면?

**정답**: 하드코딩된 값은 환경에 따라 코드를 수정해야 한다. `AgentConfig` 같은 설정 객체를 사용하면 **코드 변경 없이** 환경 변수나 설정 파일로 동작을 변경할 수 있다. 개발 환경에서는 `max_results=3, trace_enabled=True`, 프로덕션에서는 `max_results=100, trace_enabled=False`로 동일한 코드를 다르게 동작시킬 수 있다.
</details>

---

## 실습

### 실습 1: Monolith Agent 리팩토링
- **연관 학습 목표**: 학습 목표 1
- **실습 목적**: 실제로 단일 Agent를 분석하고 모듈화된 Multi-Agent 구조로 리팩토링
- **실습 유형**: 코드 작성
- **난이도**: 기초
- **예상 소요 시간**: 25분
- **선행 조건**: Session 1~3 이해
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
아래 Monolith Agent를 분석하고, 3개 이상의 독립 Sub-Agent로 분리하세요.

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator


class BigState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    user_query: str
    search_results: list[str]
    filtered_results: list[str]
    sentiment: str
    summary: str
    translated: str
    report: str
    email_sent: bool
    step: str

# 7개 Node가 모두 BigState를 공유하는 단일 그래프
# search -> filter -> sentiment -> summarize -> translate -> report -> email
```

요구사항:
1. 의존성 분석: 각 Node가 읽고 쓰는 State 필드를 매핑
2. 경계 식별: 자연스러운 Sub-Agent 경계를 찾기 (힌트: 3~4개 그룹)
3. Sub-Agent별 독립 State 정의
4. Orchestrator + 어댑터 구현
5. 리팩토링 전/후 동일한 결과 출력 확인

---

### 실습 2: 서브그래프 + 체크포인트 구현
- **연관 학습 목표**: 학습 목표 2, 3
- **실습 목적**: LangGraph 서브그래프와 체크포인터를 조합하여 중단/재개 가능한 Multi-Agent 시스템 구축
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 35분
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
"다단계 리서치 Agent"를 서브그래프 + 체크포인터로 구현하세요.

요구사항:
1. 3개 서브그래프: `research_subgraph` (자료 수집), `analysis_subgraph` (분석), `writing_subgraph` (보고서 작성)
2. 각 서브그래프는 독립 State를 가지되, `shared_data` 키로 부모와 공유
3. `MemorySaver` 체크포인터를 사용하여 각 서브그래프 완료 시 상태 저장
4. Thread ID 기반으로 세션 분리 (두 명의 사용자가 동시에 사용하는 시나리오)
5. 대화 히스토리가 10개를 넘으면 최근 5개만 유지하는 프루닝 로직 추가

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import operator


class ResearchState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    shared_data: list[str]  # 서브그래프와 공유
    report: str
    thread_metadata: dict


# TODO: research_subgraph 정의
# TODO: analysis_subgraph 정의
# TODO: writing_subgraph 정의
# TODO: 부모 그래프 구성 (서브그래프를 Node로 등록)
# TODO: MemorySaver 체크포인터 설정
# TODO: 두 사용자 시나리오 테스트
# TODO: 메모리 프루닝 로직 구현
```

---

### 실습 3: Day 2 통합 리팩토링
- **연관 학습 목표**: 학습 목표 1, 2, 3
- **실습 목적**: Day 2 전체 내용을 통합하여 프로덕션 수준의 Agent 구조를 설계
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 45분
- **선행 조건**: 실습 1, 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
Day 2에서 배운 모든 개념을 통합하여 "고객 지원 Agent"를 구현하세요.

요구사항 (Day 2 전체 내용 통합):
1. **4요소 설계** (Session 1): Goal, Memory, Tool, Control Logic State 명시
2. **LangGraph 제어 흐름** (Session 2): 질문 분류 -> 처리 -> 검증의 Conditional Edge 흐름
3. **Tool Validation** (Session 3): FAQ 검색 Tool에 Pre/Post validation, 무한 Loop 방지, 감사 로깅
4. **확장성** (Session 4):
   - 3개 Sub-Agent (분류기, FAQ검색기, 응답생성기)로 분리
   - 서브그래프 또는 어댑터 패턴으로 결합도 최소화
   - 체크포인터로 대화 상태 관리
   - `AgentConfig`로 설정 외부화

전체 아키텍처:
```
[Orchestrator]
  ├─ [Classifier Sub-Agent]      # 질문 유형 분류
  │    └─ classify -> route
  ├─ [FAQ Search Sub-Agent]      # FAQ DB 검색 + Validation
  │    └─ validate -> search -> verify_result
  └─ [Response Sub-Agent]        # 최종 응답 생성
       └─ generate -> quality_check
```

최종 검증:
- 3가지 질문 유형(기술/결제/일반)으로 테스트
- 체크포인터를 활용한 대화 지속성 확인
- FAQ 미검색 시 Fallback 경로 동작 확인
- 감사 로그 출력

---

## 핵심 정리
- 단일 Agent가 **Node 10개 / State 15필드**를 넘으면 **Multi-Agent 구조**로 리팩토링한다
- Multi-Agent 확장 패턴은 **Supervisor**(중앙 위임), **Peer-to-Peer**(직접 통신), **Hierarchical**(다단계 위임) 3가지다
- Agent 간 통신에서 **결합도를 낮추는 핵심**: State 분리, 인터페이스 계약, 어댑터 패턴
- LangGraph **서브그래프**는 컴파일된 그래프를 `add_node`에 직접 전달하여 사용하며, 부모와 동일 키 이름으로 State를 공유한다
- **체크포인터**(MemorySaver, SqliteSaver)로 State를 자동 저장/복원하고, **Thread ID**로 세션을 분리한다
- 리팩토링은 **의존성 분석 -> 인터페이스 정의 -> Sub-Agent 분리 -> Orchestrator 연결 -> 검증**의 5단계로 점진적으로 진행한다
- **팩토리 패턴**으로 Node를 생성하면 설정 기반 동작 변경과 테스트 시 mock 주입이 용이하다
