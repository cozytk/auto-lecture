# Session 3: Tool 호출 통제 & Validation

## 학습 목표
1. Tool 호출의 안전성 문제(잘못된 Tool 선택, 파라미터 에러, 무한 호출)를 식별하고 방어 전략을 설계할 수 있다
2. LangGraph에서 Tool 호출 전 Validation 파이프라인과 conditional edge 기반 통제 로직을 구현할 수 있다
3. Tool 호출 결과 검증, 에러 핸들링, 로깅/감사(audit trail)를 체계적으로 설계할 수 있다

---

## 1. Tool 호출의 안전성 문제

### 개념 설명

**왜 Tool 호출 안전성이 Agent 개발의 핵심 과제인가?** Agent가 Tool을 호출한다는 것은 LLM의 판단에 따라 **실제 시스템에 영향을 미치는 행동**이 실행된다는 뜻이다. 단순한 텍스트 생성과는 차원이 다른 문제다. 2023-2024년 초기 Agent 프로젝트(AutoGPT, BabyAGI 등)에서 가장 많이 보고된 사고 유형이 바로 통제되지 않은 Tool 호출이었다. 비용 폭발(Cost Explosion) 사례로, Agent가 루프를 돌며 유료 API를 수천 번 호출하여 한 시간에 수백 달러의 비용이 발생한 경우가 있다. 데이터 손상(Data Corruption) 사례로, 잘못된 파라미터로 DB 업데이트 Tool을 호출하여 프로덕션 데이터가 오염된 경우도 보고되었다. 보안 침해(Security Breach) 위험도 존재하는데, 프롬프트 인젝션에 의해 LLM이 의도하지 않은 Tool(파일 삭제, 권한 변경)을 호출하도록 유도될 수 있다.

이런 위험이 발생하는 근본 원인은 **LLM이 확률적 모델**이라는 점에 있다. 전통적인 소프트웨어에서 함수 호출은 결정론적(deterministic)이다. 같은 입력에 항상 같은 함수를 호출한다. 하지만 LLM은 같은 프롬프트에도 다른 Tool을 선택할 수 있고, 환각(hallucination)에 의해 존재하지 않는 Tool을 호출하려 할 수도 있다. 따라서 Agent에서 Tool 호출은 "신뢰할 수 없는 입력"으로 취급하고, 웹 애플리케이션에서 사용자 입력을 검증하듯 반드시 검증 레이어를 거치도록 설계해야 한다. 이것이 **Zero Trust 원칙**의 Agent 버전이다.

LLM 기반 Agent가 Tool을 호출할 때 발생할 수 있는 위험은 크게 4가지로 분류된다.

| 위험 유형 | 설명 | 실제 사례 |
|-----------|------|----------|
| **잘못된 Tool 선택** | 의도와 다른 Tool을 호출 | "날씨 조회" 요청에 DB 삭제 Tool 호출 |
| **파라미터 에러** | 필수 파라미터 누락, 타입 불일치, 범위 초과 | `age: "스물다섯"` (문자열을 int로 기대하는 필드에 전달) |
| **무한 호출 루프** | 동일 Tool을 반복 호출하여 리소스 고갈 | 검색 결과가 없을 때 무한 재검색 |
| **부수효과 미통제** | 쓰기/삭제 등 비가역 작업을 검증 없이 실행 | 확인 없이 프로덕션 DB 레코드 삭제 |

```
┌─────────────────────────────────────────────────┐
│              Tool 호출 위험 지도                  │
│                                                   │
│  LLM 출력                                         │
│     │                                             │
│     ▼                                             │
│  ┌──────────────┐                                 │
│  │ Tool 선택    │──▶ 잘못된 Tool 선택 위험        │
│  └──────┬───────┘                                 │
│         ▼                                         │
│  ┌──────────────┐                                 │
│  │ 파라미터 구성│──▶ 타입/범위/필수값 에러 위험   │
│  └──────┬───────┘                                 │
│         ▼                                         │
│  ┌──────────────┐                                 │
│  │ Tool 실행    │──▶ 부수효과, 타임아웃 위험      │
│  └──────┬───────┘                                 │
│         ▼                                         │
│  ┌──────────────┐                                 │
│  │ 결과 처리    │──▶ 무한 루프, 잘못된 해석 위험  │
│  └──────────────┘                                 │
└─────────────────────────────────────────────────┘
```

이러한 위험을 체계적으로 방어하려면 Tool 호출 전/중/후 각 단계에 **Validation Gate**를 삽입해야 한다. Session 2에서 다룬 Conditional Edge와 Retry/Fallback 패턴이 이 Gate의 기반이 된다.

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator


class ToolCallRisk(TypedDict):
    """Tool 호출 위험 분석 결과"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    requested_tool: str
    parameters: dict
    risk_level: str       # "low", "medium", "high", "critical"
    risk_reasons: list[str]
    is_approved: bool


# Tool별 위험 등급 정의
TOOL_RISK_REGISTRY = {
    "web_search": {
        "risk_level": "low",
        "side_effects": False,
        "requires_approval": False,
    },
    "db_read": {
        "risk_level": "low",
        "side_effects": False,
        "requires_approval": False,
    },
    "db_write": {
        "risk_level": "high",
        "side_effects": True,
        "requires_approval": True,
    },
    "db_delete": {
        "risk_level": "critical",
        "side_effects": True,
        "requires_approval": True,
    },
    "send_email": {
        "risk_level": "medium",
        "side_effects": True,
        "requires_approval": True,
    },
}


def assess_tool_risk(tool_name: str, parameters: dict) -> ToolCallRisk:
    """Tool 호출의 위험도를 평가한다."""
    reasons = []

    # 1. 등록되지 않은 Tool
    if tool_name not in TOOL_RISK_REGISTRY:
        return {
            "requested_tool": tool_name,
            "parameters": parameters,
            "risk_level": "critical",
            "risk_reasons": [f"미등록 Tool: {tool_name}"],
            "is_approved": False,
            "messages": [],
        }

    registry = TOOL_RISK_REGISTRY[tool_name]
    risk_level = registry["risk_level"]

    # 2. 부수효과 있는 Tool
    if registry["side_effects"]:
        reasons.append(f"{tool_name}은 부수효과가 있는 Tool")

    # 3. 파라미터 비어있음
    if not parameters:
        reasons.append("파라미터가 비어있음")
        risk_level = "high"

    is_approved = not registry["requires_approval"]
    return {
        "requested_tool": tool_name,
        "parameters": parameters,
        "risk_level": risk_level,
        "risk_reasons": reasons,
        "is_approved": is_approved,
        "messages": [],
    }


# 위험 평가 데모
test_cases = [
    ("web_search", {"query": "Python LangGraph 튜토리얼"}),
    ("db_delete", {"table": "users", "where": "id=1"}),
    ("unknown_tool", {}),
    ("send_email", {"to": "user@example.com", "body": "안녕하세요"}),
]

print("=== Tool 호출 위험 평가 ===")
for tool_name, params in test_cases:
    result = assess_tool_risk(tool_name, params)
    status = "승인" if result["is_approved"] else "차단"
    print(f"[{result['risk_level']:>8}] {tool_name:15} -> {status}")
    if result["risk_reasons"]:
        for reason in result["risk_reasons"]:
            print(f"           사유: {reason}")
```

**실행 결과:**
```
=== Tool 호출 위험 평가 ===
[     low] web_search      -> 승인
[critical] db_delete       -> 차단
           사유: db_delete은 부수효과가 있는 Tool
[critical] unknown_tool    -> 차단
           사유: 미등록 Tool: unknown_tool
[  medium] send_email      -> 차단
           사유: send_email은 부수효과가 있는 Tool
```

### Q&A

**Q: LLM이 존재하지 않는 Tool을 호출하려 하면 어떻게 해야 하나요?**
A: 이것은 **환각(hallucination)에 의한 Tool 호출**로, 가장 위험한 패턴 중 하나다. 방어 방법은 두 가지다. (1) Tool 이름을 화이트리스트로 관리하여 등록되지 않은 Tool 호출을 즉시 차단하고, (2) LLM에게 사용 가능한 Tool 목록을 system prompt에 명시적으로 제공하여 환각을 예방한다.

**Q: 모든 Tool 호출에 승인 절차를 넣으면 Agent 자율성이 떨어지지 않나요?**
A: 맞다. 그래서 Tool을 **위험 등급별로 분류**하여, 읽기(read) 작업은 자동 승인하고 쓰기/삭제(write/delete) 작업만 승인 절차를 거치는 것이 일반적이다. 이를 **Tiered Approval** 패턴이라 한다.

<details>
<summary>퀴즈: Agent가 "사용자 데이터 삭제" 요청을 받았을 때, 안전한 처리 순서는?</summary>

**힌트**: Tool 호출 전에 어떤 검증 단계가 필요할까요? 부수효과가 있는 작업의 위험 등급은?

**정답**: (1) 사용자 요청을 파싱하여 `db_delete` Tool 호출 의도를 파악 -> (2) Tool 위험 등급 확인 (`critical`) -> (3) 파라미터 유효성 검증 (삭제 대상 특정) -> (4) 사용자에게 확인 요청 ("정말 삭제하시겠습니까?") -> (5) 승인 후 실행 -> (6) 실행 결과 검증 및 로깅. 핵심은 **비가역 작업은 반드시 명시적 승인**을 거치는 것이다.
</details>

---

## 2. Tool 호출 전 Validation 파이프라인

### 개념 설명

**왜 단일 검증이 아닌 다단계 파이프라인이 필요한가?** 네트워크 보안에서 **심층 방어(Defense-in-Depth)**라는 검증된 원칙이 있다. 방화벽 하나만으로 보안을 지키지 않고, 방화벽 -> IDS -> WAF -> 애플리케이션 검증으로 여러 겹의 방어선을 구축하는 것이다. Tool 호출 검증에도 동일한 원칙이 적용된다. 스키마 검증만으로는 "파라미터 타입은 맞지만 권한이 없는 호출"을 막을 수 없고, 정책 검증만으로는 "권한은 있지만 파라미터가 깨진 호출"을 감지할 수 없다. 각 단계가 서로 다른 유형의 위험을 담당하므로, 어느 한 단계가 우회되더라도 다른 단계에서 잡아낼 수 있다.

이 파이프라인의 설계에서 핵심적인 결정은 **단계 순서**다. Schema -> Policy -> Context 순서로 배치하는 이유는 비용 효율성에 있다. Schema Validation은 순수 로컬 연산(타입 체크, 범위 확인)이므로 비용이 거의 제로다. Policy Validation은 권한 DB 조회나 Rate Limit 카운터 확인 등 약간의 I/O가 필요할 수 있다. Context Validation은 이전 대화 히스토리를 분석해야 하므로 가장 비용이 높다. "비용이 낮은 검증을 먼저" 배치하면, 대부분의 잘못된 호출을 저비용 단계에서 조기 차단하여 전체 시스템 효율을 높일 수 있다.

Tool 호출 전 Validation은 **3단계 파이프라인**으로 구성한다. 각 단계를 LangGraph Node로 구현하고 Conditional Edge로 연결하면, 실패 시 **조기 종료(early exit)**가 가능하다.

```
LLM이 Tool 호출 결정
     │
     ▼
┌──────────────────┐
│ Stage 1: Schema  │  파라미터 타입, 필수값, 범위 검증
│  Validation      │
└────────┬─────────┘
         │ 통과
         ▼
┌──────────────────┐
│ Stage 2: Policy  │  권한, 위험 등급, 호출 빈도 제한
│  Validation      │
└────────┬─────────┘
         │ 통과
         ▼
┌──────────────────┐
│ Stage 3: Context │  현재 상태와의 일관성, 이전 결과와의 연관성
│  Validation      │
└────────┬─────────┘
         │ 통과
         ▼
    Tool 실행 허가
```

| 단계 | 검증 대상 | 실패 시 처리 |
|------|----------|-------------|
| **Schema Validation** | 파라미터 타입, 필수값, 값 범위 | 즉시 거부 + LLM에 교정 요청 |
| **Policy Validation** | Tool 접근 권한, 호출 횟수 제한, 위험 등급 | 거부 또는 승인 대기 |
| **Context Validation** | 현재 대화 맥락과의 일관성, 중복 호출 방지 | 경고 또는 대체 Tool 제안 |

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator


class ValidationState(TypedDict):
    """Validation 파이프라인 State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    tool_name: str
    tool_params: dict
    # Validation 결과
    schema_valid: bool
    policy_valid: bool
    context_valid: bool
    validation_errors: Annotated[list[str], operator.add]
    # 실행 제어
    tool_result: str
    call_count: int
    max_calls: int


# Tool 스키마 정의
TOOL_SCHEMAS = {
    "search_db": {
        "required": ["query"],
        "optional": ["limit", "offset"],
        "param_types": {"query": str, "limit": int, "offset": int},
        "param_ranges": {"limit": (1, 100), "offset": (0, 10000)},
    },
    "send_notification": {
        "required": ["recipient", "message"],
        "optional": ["priority"],
        "param_types": {"recipient": str, "message": str, "priority": str},
        "param_ranges": {},
    },
}

# Tool별 위험 등급 (섹션 1에서 정의한 레지스트리 재활용)
TOOL_RISK_REGISTRY = {
    "search_db": {"risk_level": "low", "requires_approval": False},
    "send_notification": {"risk_level": "medium", "requires_approval": False},
    "db_delete": {"risk_level": "critical", "requires_approval": True},
}


def schema_validation(state: ValidationState) -> dict:
    """Stage 1: 파라미터 스키마 검증"""
    tool = state["tool_name"]
    params = state["tool_params"]
    errors = []

    schema = TOOL_SCHEMAS.get(tool)
    if not schema:
        errors.append(f"스키마 미정의 Tool: {tool}")
        print(f"[Schema] 실패: 스키마 미정의 Tool '{tool}'")
        return {"schema_valid": False, "validation_errors": errors}

    # 필수 파라미터 확인
    for req in schema["required"]:
        if req not in params:
            errors.append(f"필수 파라미터 누락: {req}")

    # 타입 확인
    for key, value in params.items():
        expected_type = schema["param_types"].get(key)
        if expected_type and not isinstance(value, expected_type):
            errors.append(
                f"타입 불일치: {key}={value} "
                f"(expected {expected_type.__name__}, got {type(value).__name__})"
            )

    # 범위 확인
    for key, (min_val, max_val) in schema.get("param_ranges", {}).items():
        if key in params and isinstance(params[key], (int, float)):
            if not (min_val <= params[key] <= max_val):
                errors.append(f"범위 초과: {key}={params[key]} (허용: {min_val}~{max_val})")

    is_valid = len(errors) == 0
    status = "통과" if is_valid else f"실패 ({len(errors)}건)"
    print(f"[Schema Validation] {status}")
    for err in errors:
        print(f"  - {err}")

    return {"schema_valid": is_valid, "validation_errors": errors}


def policy_validation(state: ValidationState) -> dict:
    """Stage 2: 정책 기반 검증 (권한, 빈도 제한, 위험 등급)"""
    tool = state["tool_name"]
    errors = []

    # 호출 횟수 제한 검사
    if state["call_count"] >= state["max_calls"]:
        errors.append(
            f"호출 횟수 초과: {state['call_count']}/{state['max_calls']}"
        )

    # 위험 등급 검사
    risk_info = TOOL_RISK_REGISTRY.get(tool, {})
    if risk_info.get("risk_level") == "critical":
        errors.append(f"Critical 등급 Tool: 자동 실행 불가")

    is_valid = len(errors) == 0
    status = "통과" if is_valid else f"실패 ({len(errors)}건)"
    print(f"[Policy Validation] {status}")
    for err in errors:
        print(f"  - {err}")

    return {"policy_valid": is_valid, "validation_errors": errors}


def context_validation(state: ValidationState) -> dict:
    """Stage 3: 맥락 기반 검증 (중복 호출 방지, 대화 일관성)"""
    errors = []

    # 동일 Tool 연속 호출 감지
    recent_messages = state["messages"][-3:]
    same_tool_count = sum(
        1 for msg in recent_messages
        if isinstance(msg, AIMessage) and state["tool_name"] in msg.content
    )
    if same_tool_count >= 2:
        errors.append(
            f"동일 Tool 연속 호출 감지: {state['tool_name']} ({same_tool_count}회)"
        )

    is_valid = len(errors) == 0
    status = "통과" if is_valid else f"실패 ({len(errors)}건)"
    print(f"[Context Validation] {status}")
    for err in errors:
        print(f"  - {err}")

    return {"context_valid": is_valid, "validation_errors": errors}


def route_after_schema(state: ValidationState) -> str:
    """Schema 검증 통과 여부에 따라 분기"""
    if state["schema_valid"]:
        return "continue"
    return "reject"


def route_after_policy(state: ValidationState) -> str:
    """Policy 검증 통과 여부에 따라 분기"""
    if state["policy_valid"]:
        return "continue"
    return "reject"


def route_after_context(state: ValidationState) -> str:
    """Context 검증 통과 여부에 따라 분기"""
    if state["context_valid"]:
        return "execute"
    return "reject"


def execute_tool(state: ValidationState) -> dict:
    """검증 통과 후 Tool 실행"""
    result = f"{state['tool_name']}({state['tool_params']}) -> 실행 성공"
    print(f"[Tool 실행] {result}")
    return {
        "tool_result": result,
        "call_count": state["call_count"] + 1,
        "messages": [AIMessage(content=f"Tool 결과: {result}")],
    }


def reject_tool(state: ValidationState) -> dict:
    """검증 실패로 Tool 호출 거부"""
    errors = state["validation_errors"]
    msg = f"Tool 호출 거부: {', '.join(errors[-3:])}"
    print(f"[거부] {msg}")
    return {
        "tool_result": "",
        "messages": [AIMessage(content=msg)],
    }


# 그래프 구성
graph = StateGraph(ValidationState)

graph.add_node("schema_check", schema_validation)
graph.add_node("policy_check", policy_validation)
graph.add_node("context_check", context_validation)
graph.add_node("execute", execute_tool)
graph.add_node("reject", reject_tool)

graph.add_edge(START, "schema_check")
graph.add_conditional_edges(
    "schema_check",
    route_after_schema,
    {"continue": "policy_check", "reject": "reject"},
)
graph.add_conditional_edges(
    "policy_check",
    route_after_policy,
    {"continue": "context_check", "reject": "reject"},
)
graph.add_conditional_edges(
    "context_check",
    route_after_context,
    {"execute": "execute", "reject": "reject"},
)
graph.add_edge("execute", END)
graph.add_edge("reject", END)

app = graph.compile()

# 테스트 1: 정상 호출
print("=== 테스트 1: 정상 호출 ===")
app.invoke({
    "messages": [HumanMessage(content="DB에서 사용자 검색")],
    "tool_name": "search_db",
    "tool_params": {"query": "active users", "limit": 10},
    "schema_valid": False,
    "policy_valid": False,
    "context_valid": False,
    "validation_errors": [],
    "tool_result": "",
    "call_count": 0,
    "max_calls": 5,
})

# 테스트 2: 파라미터 에러
print("\n=== 테스트 2: 파라미터 에러 ===")
app.invoke({
    "messages": [HumanMessage(content="DB 검색")],
    "tool_name": "search_db",
    "tool_params": {"limit": 500},  # query 누락, limit 범위 초과
    "schema_valid": False,
    "policy_valid": False,
    "context_valid": False,
    "validation_errors": [],
    "tool_result": "",
    "call_count": 0,
    "max_calls": 5,
})

# 테스트 3: 호출 횟수 초과
print("\n=== 테스트 3: 호출 횟수 초과 ===")
app.invoke({
    "messages": [HumanMessage(content="알림 전송")],
    "tool_name": "send_notification",
    "tool_params": {"recipient": "user@test.com", "message": "테스트"},
    "schema_valid": False,
    "policy_valid": False,
    "context_valid": False,
    "validation_errors": [],
    "tool_result": "",
    "call_count": 5,
    "max_calls": 5,
})
```

**실행 결과:**
```
=== 테스트 1: 정상 호출 ===
[Schema Validation] 통과
[Policy Validation] 통과
[Context Validation] 통과
[Tool 실행] search_db({'query': 'active users', 'limit': 10}) -> 실행 성공

=== 테스트 2: 파라미터 에러 ===
[Schema Validation] 실패 (2건)
  - 필수 파라미터 누락: query
  - 범위 초과: limit=500 (허용: 1~100)
[거부] Tool 호출 거부: 필수 파라미터 누락: query, 범위 초과: limit=500 (허용: 1~100)

=== 테스트 3: 호출 횟수 초과 ===
[Schema Validation] 통과
[Policy Validation] 실패 (1건)
  - 호출 횟수 초과: 5/5
[거부] Tool 호출 거부: 호출 횟수 초과: 5/5
```

### Q&A

**Q: Validation을 3단계로 나누는 이유는 무엇인가요? 한 번에 모두 검사하면 안 되나요?**
A: 한 번에 검사할 수도 있지만, **단계별 분리의 장점**이 크다. (1) **조기 종료(early exit)**: Schema 검증 실패 시 비용이 큰 Policy/Context 검증을 건너뛸 수 있다. (2) **독립적 진화**: 각 단계를 독립적으로 수정/확장할 수 있다. (3) **디버깅 용이**: 어떤 단계에서 실패했는지 정확히 추적할 수 있다.

**Q: 실제 프로덕션에서 파라미터 스키마는 어떻게 관리하나요?**
A: **Pydantic 모델**로 Tool 파라미터를 정의하는 것이 표준이다. LangChain의 `@tool` 데코레이터에 Pydantic 모델을 타입 힌트로 지정하면 자동으로 스키마 검증이 이루어진다. 본 예제에서는 원리를 보여주기 위해 수동 구현했지만, 실무에서는 Pydantic을 적극 활용해야 한다.

<details>
<summary>퀴즈: 다음 Tool 호출이 Validation 파이프라인의 어느 단계에서 거부될까?</summary>

```python
tool_name = "search_db"
tool_params = {"query": "users", "limit": 50}
call_count = 3
max_calls = 5
```

하지만 이전 2회 연속으로 동일한 `search_db` 호출이 있었다면?

**힌트**: Schema와 Policy는 문제없습니다. Context Validation에서는 무엇을 확인하나요?

**정답**: **Stage 3: Context Validation**에서 거부된다. Schema (파라미터 정상)와 Policy (호출 횟수 3/5로 여유)는 통과하지만, 동일 Tool이 연속 2회 이상 호출된 이력이 있으므로 Context Validation의 "중복 호출 방지" 규칙에 걸린다.
</details>

---

## 3. LangGraph에서 Tool 호출 통제 구현

### 개념 설명

**Validation Gate 패턴이란 무엇이며 왜 필요한가?** Section 2에서 다룬 Validation 파이프라인은 "이미 결정된 Tool 호출을 검증"하는 것이었다면, 이번 섹션의 Tool 호출 통제는 "LLM의 실시간 판단을 가로채고(intercept) 통제"하는 더 포괄적인 패턴이다. 핵심 아이디어는 LLM과 Tool 실행 사이에 **게이트키퍼(Gatekeeper)**를 배치하는 것이다. 이 게이트키퍼가 모든 Tool 호출을 중간에서 검사하고, 문제가 있으면 LLM에게 "이 호출은 거부되었으니 다른 방법을 시도하라"고 피드백한다. LLM은 이 피드백을 받아 스스로 교정(self-correction)하여 더 나은 호출을 시도한다.

이 패턴에서 가장 정교한 부분은 **거부 후 교정 루프(Rejection-Correction Loop)**다. 단순히 "거부"만 하면 Agent가 같은 실수를 반복하거나 작업을 포기한다. 거부 시 ToolMessage에 "왜 거부되었는지"와 "어떤 Tool이 허용되는지"를 구체적으로 알려주면, LLM이 대안을 찾아 수렴 속도가 빨라진다. 이것은 프롬프트 엔지니어링에서 "구체적 지시(specific instruction)" 원칙과 동일한 맥락이다. 물론 교정 루프도 무한히 반복될 수 있으므로, `max_iterations` 가드를 반드시 함께 구현해야 한다. 일반적으로 단순 Agent는 3~5회, 복잡한 분석 Agent는 7~10회가 적정 상한이다.

실제 LLM 기반 Agent에서 Tool 호출 통제는 **LLM의 tool_calls 출력을 가로채서 검증하는 패턴**으로 구현한다. LangGraph에서 이 패턴은 다음 구조를 따른다.

```
[LLM Node] ──tool_calls──▶ [Validation Gate] ──통과──▶ [Tool Executor]
                                   │                         │
                                   │ 거부                    │ 결과
                                   ▼                         ▼
                            [Error Handler]            [LLM Node]
                                   │                   (결과 기반
                                   │ 교정 요청          다음 판단)
                                   ▼
                              [LLM Node]
```

핵심 구현 요소:

| 요소 | 역할 | LangGraph 구현 |
|------|------|----------------|
| **Validation Gate** | Tool 호출 전 검증 | Conditional Edge + 검증 Node |
| **Retry with Correction** | 검증 실패 시 LLM에 교정 요청 | 루프 Edge로 LLM Node 재진입 |
| **Max Iteration Guard** | 무한 루프 방지 | State의 iteration_count로 제한 |
| **Tool Whitelist** | 허용 Tool 목록 관리 | State 또는 설정에 정의 |

### 예제

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
import operator


class ToolControlState(TypedDict):
    """Tool 호출 통제 그래프 State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Tool 호출 정보
    pending_tool_call: dict | None  # {"name": str, "args": dict, "id": str}
    tool_result: str
    # 통제 정보
    allowed_tools: list[str]
    iteration: int
    max_iterations: int
    # 추적
    log: Annotated[list[str], operator.add]


def llm_node(state: ToolControlState) -> dict:
    """LLM이 다음 행동을 결정한다.

    실제로는 LLM API를 호출하여 tool_calls를 받는다.
    여기서는 데모를 위해 시나리오별 하드코딩.
    """
    iteration = state["iteration"]

    if iteration == 0:
        tool_call = {
            "name": "search_db",
            "args": {"query": "monthly revenue", "limit": 10},
            "id": "call_001",
        }
        print(f"[LLM] Tool 호출 결정: {tool_call['name']}({tool_call['args']})")
    elif iteration == 1:
        tool_call = {
            "name": "calculate",
            "args": {"expression": "sum(revenue_data)"},
            "id": "call_002",
        }
        print(f"[LLM] Tool 호출 결정: {tool_call['name']}({tool_call['args']})")
    else:
        # 최종 응답 (Tool 호출 없음)
        print("[LLM] 최종 응답 생성 (Tool 호출 없음)")
        return {
            "pending_tool_call": None,
            "iteration": iteration + 1,
            "messages": [AIMessage(content="매출 분석 완료: 총 1,250만원")],
            "log": [f"[{iteration}] LLM: 최종 응답 생성"],
        }

    return {
        "pending_tool_call": tool_call,
        "iteration": iteration + 1,
        "log": [f"[{iteration}] LLM: {tool_call['name']} 호출 결정"],
    }


def validation_gate(state: ToolControlState) -> dict:
    """Tool 호출 Validation Gate: 화이트리스트 및 반복 횟수 검증"""
    tool_call = state["pending_tool_call"]

    if tool_call is None:
        print("[Validation] Tool 호출 없음 - 통과")
        return {"log": ["[Gate] Tool 호출 없음 - 통과"]}

    errors = []

    # 1. Whitelist 검사
    if tool_call["name"] not in state["allowed_tools"]:
        errors.append(f"비허용 Tool: {tool_call['name']}")

    # 2. 반복 횟수 검사
    if state["iteration"] > state["max_iterations"]:
        errors.append(
            f"최대 반복 초과: {state['iteration']}/{state['max_iterations']}"
        )

    if errors:
        error_msg = "; ".join(errors)
        print(f"[Validation] 거부: {error_msg}")
        return {
            "pending_tool_call": None,
            "log": [f"[Gate] 거부: {error_msg}"],
            "messages": [
                ToolMessage(
                    content=f"Tool 호출 거부: {error_msg}. "
                            f"허용된 Tool: {state['allowed_tools']}",
                    tool_call_id=tool_call["id"],
                )
            ],
        }

    print(f"[Validation] 승인: {tool_call['name']}")
    return {"log": [f"[Gate] 승인: {tool_call['name']}"]}


def execute_tool_node(state: ToolControlState) -> dict:
    """승인된 Tool을 실행한다."""
    tool_call = state["pending_tool_call"]
    if tool_call is None:
        return {}

    # Mock 실행
    mock_results = {
        "search_db": "검색 결과: [{'month': '1월', 'revenue': 500}, "
                     "{'month': '2월', 'revenue': 750}]",
        "calculate": "계산 결과: 1250",
    }
    result = mock_results.get(tool_call["name"], "결과 없음")
    print(f"[Tool 실행] {tool_call['name']} -> {result}")

    return {
        "tool_result": result,
        "pending_tool_call": None,
        "messages": [
            ToolMessage(content=result, tool_call_id=tool_call["id"])
        ],
        "log": [f"[Tool] {tool_call['name']} 실행 완료"],
    }


def route_after_llm(state: ToolControlState) -> str:
    """LLM 결과에 따라 분기: Tool 호출 or 최종 응답"""
    if state["pending_tool_call"] is None:
        return "finish"
    return "validate"


def route_after_validation(state: ToolControlState) -> str:
    """Validation 결과에 따라 분기: 실행 or LLM 재요청"""
    if state["pending_tool_call"] is not None:
        return "execute"
    # 거부된 경우: LLM에게 다시 요청
    if state["iteration"] <= state["max_iterations"]:
        return "retry_llm"
    return "finish"


def finish_node(state: ToolControlState) -> dict:
    """실행 완료"""
    print(f"\n[완료] 총 {state['iteration']}회 반복")
    return {"log": [f"[Finish] 완료 (반복: {state['iteration']}회)"]}


# 그래프 구성
graph = StateGraph(ToolControlState)

graph.add_node("llm", llm_node)
graph.add_node("validation_gate", validation_gate)
graph.add_node("execute_tool", execute_tool_node)
graph.add_node("finish", finish_node)

graph.add_edge(START, "llm")
graph.add_conditional_edges(
    "llm",
    route_after_llm,
    {"validate": "validation_gate", "finish": "finish"},
)
graph.add_conditional_edges(
    "validation_gate",
    route_after_validation,
    {"execute": "execute_tool", "retry_llm": "llm", "finish": "finish"},
)
graph.add_edge("execute_tool", "llm")  # Tool 결과를 LLM에 전달하여 다음 판단
graph.add_edge("finish", END)

app = graph.compile()

# 실행
print("=== Tool 호출 통제 데모 ===")
result = app.invoke({
    "messages": [HumanMessage(content="이번 달 매출 분석해줘")],
    "pending_tool_call": None,
    "tool_result": "",
    "allowed_tools": ["search_db", "calculate", "web_search"],
    "iteration": 0,
    "max_iterations": 5,
    "log": [],
})

print("\n=== 실행 로그 ===")
for entry in result["log"]:
    print(f"  {entry}")
```

**실행 결과:**
```
=== Tool 호출 통제 데모 ===
[LLM] Tool 호출 결정: search_db({'query': 'monthly revenue', 'limit': 10})
[Validation] 승인: search_db
[Tool 실행] search_db -> 검색 결과: [{'month': '1월', 'revenue': 500}, {'month': '2월', 'revenue': 750}]
[LLM] Tool 호출 결정: calculate({'expression': 'sum(revenue_data)'})
[Validation] 승인: calculate
[Tool 실행] calculate -> 계산 결과: 1250
[LLM] 최종 응답 생성 (Tool 호출 없음)

[완료] 총 3회 반복

=== 실행 로그 ===
  [0] LLM: search_db 호출 결정
  [Gate] 승인: search_db
  [Tool] search_db 실행 완료
  [1] LLM: calculate 호출 결정
  [Gate] 승인: calculate
  [Tool] calculate 실행 완료
  [2] LLM: 최종 응답 생성
  [Finish] 완료 (반복: 3회)
```

### Q&A

**Q: max_iterations를 얼마로 설정하는 것이 적절한가요?**
A: 작업 복잡도에 따라 다르지만, 일반적으로 **Tool 호출 3~10회** 이내로 설정한다. 경험적으로, 단순 조회 Agent는 3~5회, 다단계 분석 Agent는 7~10회가 적정하다. 핵심은 **무한 루프 방지**가 목적이므로, 예상 최대 호출 횟수의 1.5~2배로 설정하는 것이 안전하다.

**Q: Validation Gate에서 거부된 후 LLM이 같은 Tool을 또 호출하면?**
A: `ToolMessage`로 거부 사유와 허용된 Tool 목록을 LLM에게 전달하기 때문에, 잘 설계된 LLM은 교정된 호출을 시도한다. 그래도 반복되면 `max_iterations` 가드가 무한 루프를 방지한다. 추가로, 동일 Tool 연속 거부 횟수를 State에 추적하여 3회 연속 거부 시 강제 종료하는 패턴도 있다.

<details>
<summary>퀴즈: Validation Gate에서 비허용 Tool이 감지되었을 때, ToolMessage에 "허용된 Tool 목록"을 포함하는 이유는?</summary>

**힌트**: LLM이 다음 호출에서 올바른 Tool을 선택하려면 어떤 정보가 필요할까요?

**정답**: LLM이 **교정(self-correction)** 할 수 있도록 **구체적인 대안을 제시**하기 위해서다. 단순히 "거부됨"이라고만 알려주면 LLM이 같은 실수를 반복할 확률이 높다. 허용된 Tool 목록을 함께 전달하면 LLM이 대안을 선택할 수 있어 수렴 속도가 빨라진다. 이는 프롬프트 엔지니어링의 **"구체적 지시 원칙"**과 동일한 맥락이다.
</details>

---

## 4. Tool 호출 결과 검증 및 에러 핸들링

### 개념 설명

**왜 Tool 실행 "성공"만으로는 충분하지 않은가?** HTTP 200 OK를 받았다고 해서 응답 내용이 올바른 것은 아니다. 외부 API가 빈 결과를 반환하거나, JSON 형식이 깨지거나, 논리적으로 불가능한 값(음수 매출, 미래 날짜의 과거 데이터)을 포함할 수 있다. Agent가 이런 결과를 그대로 LLM에 전달하면, LLM은 잘못된 데이터를 기반으로 추론하여 "자신있게 틀린 답변"을 생성한다. 이것은 환각(hallucination)보다 더 위험한데, 환각은 사용자가 "이상하다"고 느낄 수 있지만 잘못된 데이터 기반 추론은 그럴듯해 보여 발견하기 어렵기 때문이다.

결과 검증은 **구조적 정확성**과 **의미적 정확성**을 분리하여 접근해야 한다. 구조적 검증(L1)은 "데이터가 예상 형식인가"를 확인하며, 실패 시 재시도로 해결 가능한 일시적 문제인 경우가 많다. 의미적 검증(L2)은 "데이터 값이 논리적으로 유효한가"를 확인하며, 실패 시 데이터 소스 자체에 문제가 있을 수 있으므로 대체 Tool이나 LLM 재해석이 필요하다. 일관성 검증(L3)은 "이전 결과와 모순되지 않는가"를 확인하며, 실패 시에도 실제로는 정상(계절 효과, 이벤트 등)일 수 있으므로 경고 수준으로 처리하는 것이 일반적이다.

Tool 실행이 성공했더라도 **결과의 품질**까지 검증해야 한다. Tool 호출 후 검증은 3가지 레벨로 나뉜다.

| 레벨 | 검증 내용 | 예시 |
|------|----------|------|
| **L1: 구조 검증** | 반환 형식이 예상과 일치하는지 | JSON 파싱 가능 여부, 필수 필드 존재 |
| **L2: 의미 검증** | 반환 내용이 논리적으로 유효한지 | 빈 결과, 음수 매출, 미래 날짜 등 |
| **L3: 일관성 검증** | 이전 결과와 모순되지 않는지 | 이전 총합과 부분합 불일치 |

```
Tool 실행 결과
     │
     ▼
┌─────────────────┐
│ L1: 구조 검증   │──실패──▶ 즉시 Retry (파싱 에러)
└────────┬────────┘
         │ 통과
         ▼
┌─────────────────┐
│ L2: 의미 검증   │──실패──▶ 대체 Tool 또는 LLM 재해석
└────────┬────────┘
         │ 통과
         ▼
┌─────────────────┐
│ L3: 일관성 검증 │──실패──▶ 경고 + 사용자 확인
└────────┬────────┘
         │ 통과
         ▼
   결과 승인 (다음 단계)
```

### 예제

```python
import json
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator


class ResultValidationState(TypedDict):
    """Tool 결과 검증 State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    raw_result: str          # Tool 원시 결과
    parsed_result: dict      # 파싱된 결과
    validation_level: str    # 현재 검증 레벨
    is_valid: bool
    errors: Annotated[list[str], operator.add]
    retry_count: int
    max_retries: int
    previous_results: list[dict]  # 이전 결과 (일관성 검증용)


def simulate_tool_call(state: ResultValidationState) -> dict:
    """Tool 호출 시뮬레이션 - 첫 시도는 깨진 JSON, 두 번째는 정상"""
    retry = state["retry_count"]

    if retry == 0:
        raw = '{"revenue": 1500, "month": "invalid-json...'  # 깨진 JSON
        print(f"[Tool] 결과 반환 (시도 {retry + 1}): 깨진 JSON")
    else:
        raw = json.dumps({
            "revenue": 1500,
            "month": "2025-01",
            "items": [
                {"name": "상품A", "amount": 800},
                {"name": "상품B", "amount": 700},
            ]
        })
        print(f"[Tool] 결과 반환 (시도 {retry + 1}): 정상 JSON")

    return {"raw_result": raw, "retry_count": retry + 1}


def validate_structure(state: ResultValidationState) -> dict:
    """L1: 구조 검증 - JSON 파싱 및 필수 필드 확인"""
    raw = state["raw_result"]
    errors = []

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        errors.append(f"JSON 파싱 실패: {str(e)[:50]}")
        print(f"[L1 구조 검증] 실패: JSON 파싱 에러")
        return {
            "parsed_result": {},
            "validation_level": "L1",
            "is_valid": False,
            "errors": errors,
        }

    # 필수 필드 확인
    required_fields = ["revenue", "month"]
    for field in required_fields:
        if field not in parsed:
            errors.append(f"필수 필드 누락: {field}")

    is_valid = len(errors) == 0
    status = "통과" if is_valid else f"실패 ({len(errors)}건)"
    print(f"[L1 구조 검증] {status}")

    return {
        "parsed_result": parsed if is_valid else {},
        "validation_level": "L1",
        "is_valid": is_valid,
        "errors": errors,
    }


def validate_semantics(state: ResultValidationState) -> dict:
    """L2: 의미 검증 - 값의 논리적 유효성 확인"""
    parsed = state["parsed_result"]
    errors = []

    # 매출은 양수여야 함
    if parsed.get("revenue", 0) < 0:
        errors.append(f"비정상 매출: {parsed['revenue']} (음수)")

    # items 합계와 revenue 일치 확인
    if "items" in parsed:
        item_total = sum(item["amount"] for item in parsed["items"])
        if item_total != parsed.get("revenue", 0):
            errors.append(
                f"항목 합계 불일치: items 합={item_total}, "
                f"revenue={parsed.get('revenue')}"
            )

    is_valid = len(errors) == 0
    status = "통과" if is_valid else f"실패 ({len(errors)}건)"
    print(f"[L2 의미 검증] {status}")
    for err in errors:
        print(f"  - {err}")

    return {
        "validation_level": "L2",
        "is_valid": is_valid,
        "errors": errors,
    }


def validate_consistency(state: ResultValidationState) -> dict:
    """L3: 일관성 검증 - 이전 결과와 비교"""
    parsed = state["parsed_result"]
    previous = state.get("previous_results", [])
    errors = []

    if previous:
        last = previous[-1]
        if "revenue" in last and "revenue" in parsed:
            change_rate = (
                abs(parsed["revenue"] - last["revenue"])
                / max(last["revenue"], 1)
            )
            if change_rate > 0.5:
                errors.append(
                    f"매출 급변 경고: {last['revenue']} -> {parsed['revenue']} "
                    f"(변동률: {change_rate:.0%})"
                )

    is_valid = len(errors) == 0
    status = "통과" if is_valid else f"경고 ({len(errors)}건)"
    print(f"[L3 일관성 검증] {status}")
    for err in errors:
        print(f"  - {err}")

    return {
        "validation_level": "L3",
        "is_valid": is_valid,
        "errors": errors,
    }


def handle_success(state: ResultValidationState) -> dict:
    """검증 성공 - 결과 확정"""
    parsed = state["parsed_result"]
    msg = f"검증 완료: 매출 {parsed['revenue']}만원 ({parsed['month']})"
    print(f"[성공] {msg}")
    return {"messages": [AIMessage(content=msg)]}


def handle_failure(state: ResultValidationState) -> dict:
    """최종 실패 처리"""
    all_errors = state["errors"]
    msg = f"Tool 결과 검증 최종 실패: {'; '.join(all_errors[-3:])}"
    print(f"[실패] {msg}")
    return {"messages": [AIMessage(content=msg)]}


def route_after_l1(state: ResultValidationState) -> str:
    """L1 검증 후 분기: 통과 -> L2, 실패 -> Retry 또는 최종 실패"""
    if state["is_valid"]:
        return "l2"
    if state["retry_count"] < state["max_retries"]:
        return "retry"
    return "fail"


def route_after_l2(state: ResultValidationState) -> str:
    """L2 검증 후 분기"""
    if state["is_valid"]:
        return "l3"
    return "fail"


def route_after_l3(state: ResultValidationState) -> str:
    """L3 검증 후 분기 - L3는 경고 수준이므로 실패해도 진행"""
    return "success"


# 그래프 구성
graph = StateGraph(ResultValidationState)

graph.add_node("tool_call", simulate_tool_call)
graph.add_node("validate_l1", validate_structure)
graph.add_node("validate_l2", validate_semantics)
graph.add_node("validate_l3", validate_consistency)
graph.add_node("success", handle_success)
graph.add_node("failure", handle_failure)

graph.add_edge(START, "tool_call")
graph.add_edge("tool_call", "validate_l1")
graph.add_conditional_edges(
    "validate_l1",
    route_after_l1,
    {"l2": "validate_l2", "retry": "tool_call", "fail": "failure"},
)
graph.add_conditional_edges(
    "validate_l2",
    route_after_l2,
    {"l3": "validate_l3", "fail": "failure"},
)
graph.add_conditional_edges(
    "validate_l3",
    route_after_l3,
    {"success": "success"},
)
graph.add_edge("success", END)
graph.add_edge("failure", END)

app = graph.compile()

# 실행: 첫 시도 실패 (JSON 파싱) -> 재시도 -> 성공
print("=== Tool 결과 검증 파이프라인 ===")
result = app.invoke({
    "messages": [HumanMessage(content="1월 매출 데이터 조회")],
    "raw_result": "",
    "parsed_result": {},
    "validation_level": "",
    "is_valid": False,
    "errors": [],
    "retry_count": 0,
    "max_retries": 3,
    "previous_results": [],
})
```

**실행 결과:**
```
=== Tool 결과 검증 파이프라인 ===
[Tool] 결과 반환 (시도 1): 깨진 JSON
[L1 구조 검증] 실패: JSON 파싱 에러
[Tool] 결과 반환 (시도 2): 정상 JSON
[L1 구조 검증] 통과
[L2 의미 검증] 통과
[L3 일관성 검증] 통과
[성공] 검증 완료: 매출 1500만원 (2025-01)
```

### Q&A

**Q: L2 의미 검증에서 "항목 합계와 revenue 불일치"는 Tool의 버그인가요, LLM의 문제인가요?**
A: 대부분 **Tool(외부 API)의 데이터 불일치**다. 하지만 LLM이 Tool 결과를 가공하는 과정에서도 발생할 수 있다. 따라서 L2 검증은 Tool 결과를 LLM에 전달하기 **전에** 수행하여, LLM이 잘못된 데이터를 기반으로 추론하는 것을 방지해야 한다.

**Q: L3 일관성 검증에서 "매출 급변"이 실제로는 정상인 경우도 있지 않나요?**
A: 맞다. L3는 **경고(warning)** 수준이므로 블로킹하지 않는 것이 일반적이다. 급변이 감지되면 사용자에게 "이전 대비 50% 이상 변동이 있습니다"라고 알려주고, 사용자가 판단하도록 한다. 자동 차단하면 정상적인 급변(세일 기간, 시즌 효과 등)도 막히게 된다.

<details>
<summary>퀴즈: Tool이 `{"revenue": -500, "month": "2025-13"}`을 반환했다면, L1~L3 중 어디서 처음 감지될까?</summary>

**힌트**: L1은 JSON 구조와 필수 필드를, L2는 값의 논리적 유효성을 검사합니다. "2025-13"월은 존재할까요?

**정답**: **L2 의미 검증**에서 감지된다. L1(구조 검증)은 JSON 파싱 성공 + `revenue`, `month` 필드 존재로 통과한다. L2에서 `revenue < 0` (음수 매출) 규칙에 걸린다. "2025-13"은 현재 구현에서는 감지하지 못하지만, 날짜 형식 검증 규칙을 추가하면 L2에서 함께 잡을 수 있다.
</details>

---

## 5. Tool 호출 로깅 및 감사(Audit Trail)

### 개념 설명

**왜 Agent에서 감사 로깅이 전통 소프트웨어보다 더 중요한가?** 전통적인 소프트웨어는 코드를 읽으면 실행 경로를 예측할 수 있다. 하지만 Agent의 실행 경로는 **비결정적(non-deterministic)**이다. 같은 사용자 요청에 대해 LLM이 다른 Tool을 선택하거나, 같은 Tool을 다른 파라미터로 호출할 수 있다. 따라서 "코드를 읽는 것"만으로는 Agent가 어떤 경로로 실행되었는지 알 수 없으며, 반드시 실행 시점의 기록(로그)이 있어야 문제를 진단할 수 있다.

감사 로깅은 단순한 `print` 디버깅과 근본적으로 다르다. 구조화된 감사 로그는 **검색 가능하고, 집계 가능하며, 재현 가능**해야 한다. "지난 주에 search_db Tool이 총 몇 번 호출되었는가?", "실패율이 가장 높은 Tool은 무엇인가?", "특정 사용자가 민감한 데이터에 접근한 이력이 있는가?" 같은 질문에 답할 수 있어야 한다. 특히 GDPR이나 개인정보보호법 같은 규정이 적용되는 환경에서는, 민감 데이터에 대한 접근 기록을 일정 기간 보존하는 것이 법적 의무이기도 하다. OpenTelemetry 같은 표준 프레임워크를 따르면 기존 모니터링 인프라(Datadog, Grafana 등)와 통합이 용이하다.

프로덕션 Agent에서 **모든 Tool 호출은 추적 가능해야** 한다. 감사 로그(Audit Trail)는 3가지 목적을 가진다.

| 목적 | 설명 | 활용 |
|------|------|------|
| **디버깅** | 문제 발생 시 호출 경로 추적 | "어떤 Tool이, 어떤 파라미터로, 언제 실패했는가?" |
| **비용 추적** | API 호출 횟수와 비용 모니터링 | "이번 세션에서 외부 API를 몇 회 호출했는가?" |
| **규정 준수** | 민감 데이터 접근 기록 | "누가, 언제, 어떤 데이터에 접근했는가?" |

감사 로그의 필수 필드:

```
┌──────────────────────────────────────────────────────┐
│                   Audit Log Entry                     │
│                                                       │
│  timestamp    : 2025-01-15T14:30:22Z                 │
│  session_id   : sess_abc123                          │
│  tool_name    : search_db                            │
│  parameters   : {"query": "users", "limit": 10}     │
│  validation   : {schema: PASS, policy: PASS}         │
│  result_status: SUCCESS                              │
│  result_size  : 1024 bytes                           │
│  latency_ms   : 150                                  │
│  error        : null                                 │
│  user_id      : user_456                             │
└──────────────────────────────────────────────────────┘
```

### 예제

```python
import time
import uuid
from datetime import datetime, timezone
from typing import TypedDict, Annotated, Sequence
from dataclasses import dataclass, asdict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import operator


@dataclass
class AuditLogEntry:
    """감사 로그 엔트리"""
    timestamp: str
    session_id: str
    tool_name: str
    parameters: dict
    validation_result: str   # "PASS", "FAIL"
    execution_result: str    # "SUCCESS", "FAILURE", "SKIPPED"
    latency_ms: float
    error: str | None = None
    result_summary: str = ""


class AuditState(TypedDict):
    """감사 로깅이 내장된 Agent State"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    session_id: str
    # Tool 호출
    current_tool: str
    current_params: dict
    tool_result: str
    # 감사 로그
    audit_log: Annotated[list[dict], operator.add]
    # 타이밍
    tool_start_time: float
    # 제어
    step: str
    iteration: int


def start_tool_call(state: AuditState) -> dict:
    """Tool 호출 시작 - 타이머 기록"""
    print(f"[시작] Tool: {state['current_tool']}")
    return {"tool_start_time": time.time()}


def validate_and_execute(state: AuditState) -> dict:
    """Validation + 실행 + 로그 기록을 한 Node에서 수행"""
    tool = state["current_tool"]
    params = state["current_params"]
    start_time = state["tool_start_time"]
    session_id = state["session_id"]

    # Validation (간략화)
    allowed_tools = ["search_db", "calculate", "web_search"]
    validation_ok = tool in allowed_tools

    if not validation_ok:
        latency = (time.time() - start_time) * 1000
        log_entry = AuditLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=session_id,
            tool_name=tool,
            parameters=params,
            validation_result="FAIL",
            execution_result="SKIPPED",
            latency_ms=round(latency, 2),
            error=f"비허용 Tool: {tool}",
        )
        print(f"[감사로그] {tool} - Validation FAIL")
        return {
            "tool_result": "",
            "audit_log": [asdict(log_entry)],
            "step": "done",
        }

    # 실행 (Mock)
    time.sleep(0.05)  # 50ms 시뮬레이션
    result = f"{tool} 결과: 데이터 조회 성공 (3건)"

    latency = (time.time() - start_time) * 1000
    log_entry = AuditLogEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        session_id=session_id,
        tool_name=tool,
        parameters=params,
        validation_result="PASS",
        execution_result="SUCCESS",
        latency_ms=round(latency, 2),
        result_summary=result[:100],
    )

    print(f"[감사로그] {tool} - SUCCESS ({latency:.0f}ms)")

    return {
        "tool_result": result,
        "audit_log": [asdict(log_entry)],
        "messages": [AIMessage(content=result)],
        "step": "done",
        "iteration": state["iteration"] + 1,
    }


def report_audit(state: AuditState) -> dict:
    """감사 로그 요약 보고"""
    logs = state["audit_log"]
    total = len(logs)
    success = sum(1 for log in logs if log["execution_result"] == "SUCCESS")
    failed = sum(1 for log in logs if log["execution_result"] != "SUCCESS")
    total_latency = sum(log["latency_ms"] for log in logs)

    report = (
        f"[감사 보고] 세션: {state['session_id']}\n"
        f"  총 호출: {total}건 (성공: {success}, 실패/차단: {failed})\n"
        f"  총 지연: {total_latency:.0f}ms"
    )
    print(report)
    return {"messages": [AIMessage(content=report)]}


# 그래프 구성
graph = StateGraph(AuditState)

graph.add_node("start_call", start_tool_call)
graph.add_node("validate_execute", validate_and_execute)
graph.add_node("report", report_audit)

graph.add_edge(START, "start_call")
graph.add_edge("start_call", "validate_execute")
graph.add_edge("validate_execute", "report")
graph.add_edge("report", END)

app = graph.compile()

session = f"sess_{uuid.uuid4().hex[:8]}"

# 테스트 1: 정상 호출
print("=== 감사 로깅 - 정상 호출 ===")
result1 = app.invoke({
    "messages": [HumanMessage(content="DB 검색")],
    "session_id": session,
    "current_tool": "search_db",
    "current_params": {"query": "active users", "limit": 10},
    "tool_result": "",
    "audit_log": [],
    "tool_start_time": 0.0,
    "step": "start",
    "iteration": 0,
})

# 테스트 2: 비허용 Tool
print("\n=== 감사 로깅 - 비허용 Tool ===")
result2 = app.invoke({
    "messages": [HumanMessage(content="파일 삭제")],
    "session_id": session,
    "current_tool": "file_delete",
    "current_params": {"path": "/data/important.csv"},
    "tool_result": "",
    "audit_log": [],
    "tool_start_time": 0.0,
    "step": "start",
    "iteration": 0,
})

# 감사 로그 상세 출력
print("\n=== 감사 로그 상세 ===")
all_logs = result1["audit_log"] + result2["audit_log"]
for i, log in enumerate(all_logs):
    print(f"\n--- Entry #{i + 1} ---")
    print(f"  Tool: {log['tool_name']}")
    print(f"  Parameters: {log['parameters']}")
    print(f"  Validation: {log['validation_result']}")
    print(f"  Execution: {log['execution_result']}")
    print(f"  Latency: {log['latency_ms']}ms")
    if log["error"]:
        print(f"  Error: {log['error']}")
```

**실행 결과:**
```
=== 감사 로깅 - 정상 호출 ===
[시작] Tool: search_db
[감사로그] search_db - SUCCESS (52ms)
[감사 보고] 세션: sess_a1b2c3d4
  총 호출: 1건 (성공: 1, 실패/차단: 0)
  총 지연: 52ms

=== 감사 로깅 - 비허용 Tool ===
[시작] Tool: file_delete
[감사로그] file_delete - Validation FAIL
[감사 보고] 세션: sess_a1b2c3d4
  총 호출: 1건 (성공: 0, 실패/차단: 1)
  총 지연: 0ms

=== 감사 로그 상세 ===

--- Entry #1 ---
  Tool: search_db
  Parameters: {'query': 'active users', 'limit': 10}
  Validation: PASS
  Execution: SUCCESS
  Latency: 52.0ms

--- Entry #2 ---
  Tool: file_delete
  Parameters: {'path': '/data/important.csv'}
  Validation: FAIL
  Execution: SKIPPED
  Latency: 0.1ms
  Error: 비허용 Tool: file_delete
```

### Q&A

**Q: 감사 로그는 State에 저장하면 메모리 문제가 생기지 않나요?**
A: 맞다. 장기 실행 Agent에서는 State에 로그를 무한히 누적하면 메모리가 증가한다. 실무에서는 **외부 저장소(DB, 로그 서비스)**에 로그를 스트리밍하고, State에는 최근 N건만 유지하는 **슬라이딩 윈도우** 패턴을 사용한다. LangGraph의 checkpointer를 활용하면 State 크기 관리가 더 용이하다.

**Q: 민감한 파라미터(비밀번호, API 키 등)는 어떻게 로깅하나요?**
A: 민감 정보는 **마스킹(masking)** 처리한다. 예: `{"api_key": "sk-***", "password": "***"}`. 로깅 전에 민감 필드 목록을 정의하고 자동 마스킹하는 유틸리티 함수를 만들어야 한다. GDPR이나 개인정보보호법 준수가 필요한 환경에서는 필수다.

<details>
<summary>퀴즈: 감사 로그에서 "validation_result: PASS, execution_result: FAILURE"인 경우는 어떤 상황인가?</summary>

**힌트**: Validation은 통과했지만 실제 실행에서 실패한 경우를 생각해보세요.

**정답**: Validation(스키마, 정책, 컨텍스트)은 모두 통과했으나, **실제 Tool 실행 단계에서 외부 오류가 발생**한 경우다. 예: API 서버 다운, 네트워크 타임아웃, 인증 토큰 만료 등. 이 경우 Retry 전략이 적용되며, 감사 로그에는 각 시도마다 별도 엔트리가 기록되어 "언제, 몇 회 재시도했고, 최종 성공/실패했는지" 추적할 수 있다.
</details>

---

## 실습

### 실습 1: Validation 파이프라인 구축
- **연관 학습 목표**: 학습 목표 1, 2
- **실습 목적**: 3단계 Validation Gate를 LangGraph StateGraph로 직접 구현
- **실습 유형**: 코드 작성
- **난이도**: 기초
- **예상 소요 시간**: 25분
- **선행 조건**: LangGraph StateGraph 기본 이해 (Session 2 완료)
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
"고객 데이터 관리 Agent"의 Tool Validation 파이프라인을 구현하세요.

Agent가 사용할 수 있는 Tool:

| Tool 이름 | 설명 | 위험 등급 |
|-----------|------|----------|
| `get_customer` | 고객 정보 조회 | low |
| `update_customer` | 고객 정보 수정 | medium |
| `delete_customer` | 고객 정보 삭제 | critical |
| `export_data` | 데이터 내보내기 | high |

요구사항:
1. Schema Validation: 각 Tool의 필수 파라미터 검증 (`get_customer`: `customer_id`, `update_customer`: `customer_id` + `fields`, `delete_customer`: `customer_id` + `reason`)
2. Policy Validation: `critical` 등급 Tool은 자동 실행 불가, 호출 횟수 제한 (최대 10회)
3. Context Validation: 같은 `customer_id`에 대해 `get` 없이 `update`/`delete` 시도 시 경고
4. Conditional Edge로 각 단계 통과/거부 분기

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
import operator


class CustomerToolState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    tool_name: str
    tool_params: dict
    schema_valid: bool
    policy_valid: bool
    context_valid: bool
    validation_errors: Annotated[list[str], operator.add]
    call_count: int
    accessed_customers: list[str]  # 이미 조회한 customer_id 목록


# TODO: TOOL_SCHEMAS 정의
# TODO: schema_validation Node 구현
# TODO: policy_validation Node 구현
# TODO: context_validation Node 구현
# TODO: execute_tool, reject_tool Node 구현
# TODO: 각 라우팅 함수 구현
# TODO: StateGraph 구성 및 테스트
```

---

### 실습 2: Tool 호출 결과 검증 시스템
- **연관 학습 목표**: 학습 목표 2, 3
- **실습 목적**: Tool 실행 결과에 대한 다단계 검증을 구현하여 Agent의 신뢰성 향상
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 35분
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
"재무 데이터 분석 Agent"의 Tool 결과 검증 시스템을 구현하세요.

검증 시나리오:
- Tool이 반환하는 재무 데이터 (JSON 형식)의 구조, 의미, 일관성을 3단계로 검증
- L1 실패 시 자동 Retry (최대 2회)
- L2 실패 시 LLM에게 "데이터 이상" 보고
- L3 경고 시 경고 메시지를 포함하여 진행

요구사항:
1. Tool이 반환하는 재무 데이터: `{"quarter": "Q1", "revenue": int, "expenses": int, "profit": int}`
2. L1: JSON 파싱, 필수 필드(`quarter`, `revenue`, `expenses`, `profit`) 확인
3. L2: `profit == revenue - expenses` 확인, 모든 값 양수 확인, quarter 형식(`Q1`~`Q4`) 확인
4. L3: 이전 분기 대비 매출 변동률 30% 이상이면 경고
5. 전체 검증 결과를 감사 로그에 기록

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator
import json


class FinanceValidationState(TypedDict):
    raw_result: str
    parsed_result: dict
    validation_errors: Annotated[list[str], operator.add]
    warnings: Annotated[list[str], operator.add]
    retry_count: int
    max_retries: int
    previous_quarter: dict  # 이전 분기 데이터
    audit_log: Annotated[list[dict], operator.add]


# TODO: simulate_finance_tool Node
# TODO: validate_l1_structure Node
# TODO: validate_l2_semantics Node
# TODO: validate_l3_consistency Node
# TODO: 라우팅 함수 구현
# TODO: StateGraph 구성 및 테스트
```

---

### 실습 3: 완전한 Tool 통제 Agent 구축
- **연관 학습 목표**: 학습 목표 1, 2, 3
- **실습 목적**: Validation + 통제 + 결과 검증 + 로깅을 통합한 프로덕션 수준 Agent 구축
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 45분
- **선행 조건**: 실습 1, 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**과제:**
"주문 처리 Agent"를 구현하세요. 사용자의 주문 관련 요청을 처리하며, 모든 Tool 호출에 대해 완전한 통제와 감사를 수행합니다.

전체 아키텍처:
```
[사용자 요청] -> [LLM Node] -> [Validation Gate] -> [Tool 실행] -> [결과 검증] -> [LLM Node]
                    ^              |                                |
                    |         거부/교정                        재시도/Fallback
                    +──────────────+────────────────────────────────+
```

요구사항:
1. Tool 목록: `check_inventory` (재고 확인), `create_order` (주문 생성), `process_payment` (결제 처리), `send_confirmation` (확인 전송)
2. Validation 파이프라인: Schema + Policy + Context 3단계
3. Tool 결과 검증: L1(구조) + L2(의미) 2단계
4. 에러 핸들링: Retry(최대 2회) + Fallback(재고 부족 시 대기열 등록)
5. 감사 로깅: 모든 Tool 호출에 대한 감사 로그 생성
6. 실행 순서 보장: `check_inventory` -> `create_order` -> `process_payment` -> `send_confirmation`
7. 중간 실패 시 이미 실행된 작업의 보상 트랜잭션(rollback) 고려

---

## 핵심 정리
- Tool 호출의 4가지 주요 위험은 **잘못된 Tool 선택, 파라미터 에러, 무한 호출 루프, 부수효과 미통제**다
- Validation 파이프라인은 **Schema -> Policy -> Context** 3단계로 구성하며, 각 단계에서 Conditional Edge를 통해 조기 종료가 가능하다
- LangGraph에서 Tool 통제는 **Validation Gate Node + Conditional Edge**로 구현하며, 거부 시 **ToolMessage로 교정 정보를 LLM에 전달**한다
- Tool 결과 검증은 **L1(구조), L2(의미), L3(일관성)** 3레벨로, 레벨별 실패 대응(Retry, Fallback, 경고)이 다르다
- **감사 로그(Audit Trail)**는 디버깅, 비용 추적, 규정 준수를 위해 모든 Tool 호출에 필수이며, timestamp/tool_name/parameters/result/latency를 기록한다
- `max_iterations` 가드는 무한 루프 방지의 최종 안전장치이며, 예상 최대 호출 횟수의 1.5~2배로 설정한다
