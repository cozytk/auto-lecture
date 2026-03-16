# Day 2 Session 3: Tool 호출 통제 & Validation

> **2시간** | AI 개발자, 데이터 엔지니어, 기술 리더 대상

---

## 왜 중요한가

Tool 호출은 Agent의 가장 위험한 지점이다.
외부 시스템을 변경하거나, 비용이 발생하거나, 되돌릴 수 없는 행동을 한다.
검증 없는 Tool 호출은 프로덕션 장애의 주요 원인이다.

> **핵심 질문**: "Agent가 Tool을 호출하기 전, 호출 중, 호출 후 무엇을 검증해야 하는가?"

2026년 현재 LLM은 여전히 잘못된 인자로 Tool을 호출한다.
JSON Schema 강제와 사전/사후 검증이 이를 방지한다.
무한 루프 방지는 프로덕션 운영의 필수 요소다.

---

## 핵심 원리

### Function Calling 설계 전략

Function Calling은 LLM이 Tool을 호출하는 표준 메커니즘이다.
LLM은 어떤 Tool을 어떤 인자로 호출할지 **JSON으로 결정**한다.
이 JSON을 그대로 실행하면 안 된다. 반드시 검증이 필요하다.

```
사용자 요청
    ↓
[LLM] → Tool 호출 결정 → {"name": "send_email", "args": {...}}
    ↓
[검증 레이어] ← 여기서 차단 또는 통과
    ↓
[Tool 실행]
    ↓
[결과 검증]
    ↓
[LLM에 결과 반환]
```

### Tool 스키마 설계

Tool 스키마는 LLM이 올바른 인자를 생성하도록 유도한다.
설명이 명확할수록 LLM이 정확하게 호출한다.
제약 조건(enum, pattern, minimum 등)을 스키마에 포함한다.

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(
        description="검색할 키워드. 한국어 또는 영어. 최대 100자.",
        max_length=100,
    )
    max_results: int = Field(
        default=5,
        description="반환할 최대 결과 수",
        ge=1,
        le=20,
    )
    language: str = Field(
        default="ko",
        description="결과 언어 코드",
        pattern="^[a-z]{2}$",
    )

@tool(args_schema=SearchInput)
def web_search(query: str, max_results: int = 5, language: str = "ko") -> list[dict]:
    """웹에서 정보를 검색합니다.
    실시간 뉴스, 최신 정보, 특정 사실 확인에 사용하세요.
    LLM이 이미 알고 있는 일반 지식에는 사용하지 마세요.
    """
    # 실제 구현
    return search_api(query, max_results, language)
```

**Tool 설명 작성 원칙**:
- 언제 사용하는가 (use-case)
- 언제 사용하면 안 되는가 (anti-use-case)
- 인자의 의미와 제약

---

## JSON Schema 응답 강제 구조

### Structured Output 강제

LLM이 JSON을 자유롭게 생성하면 파싱 오류가 발생한다.
`with_structured_output`으로 스키마를 강제한다.

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal

class ToolDecision(BaseModel):
    """LLM의 Tool 호출 결정"""
    reasoning: str = Field(description="호출 이유")
    tool_name: Literal["web_search", "calculate", "send_email", "done"]
    confidence: float = Field(ge=0.0, le=1.0)
    args: dict

llm = ChatOpenAI(model="gpt-4o")
structured_llm = llm.with_structured_output(ToolDecision)

decision = structured_llm.invoke(
    "사용자 요청: AI 뉴스를 검색해줘. 사용 가능한 Tools: web_search, calculate, send_email, done"
)
# → ToolDecision(tool_name="web_search", confidence=0.95, ...)
```

### 응답 파싱 안전장치

```python
import json
from pydantic import ValidationError

def safe_parse_tool_call(raw_response: str) -> ToolDecision | None:
    """LLM 응답을 안전하게 파싱"""
    try:
        data = json.loads(raw_response)
        return ToolDecision(**data)
    except json.JSONDecodeError:
        # JSON 파싱 실패: LLM에 재요청
        return None
    except ValidationError as e:
        # 스키마 검증 실패: 오류 내용을 LLM에 피드백
        print(f"검증 실패: {e}")
        return None
```

---

## Tool 호출 전후 검증 로직

### 사전 검증 (Pre-call Validation)

Tool을 실행하기 전에 인자를 검증한다.
**의미적 검증**(semantic validation)이 핵심이다.
스키마 검증은 필요 조건이지 충분 조건이 아니다.

```python
class ToolValidator:
    def pre_validate(
        self,
        tool_name: str,
        args: dict,
        state: AgentState,
    ) -> ValidationResult:
        """Tool 실행 전 검증"""

        # 1. 권한 검증
        if tool_name in RESTRICTED_TOOLS:
            if not state.has_permission(tool_name):
                return ValidationResult.deny("권한 없음")

        # 2. 인자 의미 검증
        if tool_name == "send_email":
            email = args.get("to", "")
            if not self._is_valid_email(email):
                return ValidationResult.deny(f"유효하지 않은 이메일: {email}")

        # 3. 중복 호출 검증
        if self._is_duplicate_call(tool_name, args, state):
            return ValidationResult.deny("동일한 호출이 이미 실행됨")

        # 4. 비용 검증
        estimated_cost = self._estimate_cost(tool_name, args)
        if estimated_cost > state.remaining_budget:
            return ValidationResult.deny(f"예산 초과: {estimated_cost}")

        return ValidationResult.allow()
```

### 사후 검증 (Post-call Validation)

Tool 실행 결과를 검증한다.
빈 결과, 이상한 형식, 오류 응답을 처리한다.

```python
class ToolResultValidator:
    def post_validate(
        self,
        tool_name: str,
        result: Any,
        state: AgentState,
    ) -> ValidatedResult:
        """Tool 실행 후 결과 검증"""

        # 1. 결과 타입 검증
        expected_type = TOOL_OUTPUT_TYPES.get(tool_name)
        if not isinstance(result, expected_type):
            return ValidatedResult.error(f"예상 타입 불일치: {type(result)}")

        # 2. 빈 결과 처리
        if not result:
            return ValidatedResult.empty(
                message=f"{tool_name} 결과 없음",
                should_retry=True,
            )

        # 3. 결과 품질 검증
        if tool_name == "web_search":
            if len(result) < 2:
                return ValidatedResult.low_quality("검색 결과 부족")

        return ValidatedResult.ok(result)
```

### 검증 파이프라인 통합

```python
class SafeToolExecutor:
    def __init__(self, tools: dict, validator: ToolValidator):
        self.tools = tools
        self.validator = validator

    def execute(
        self,
        tool_name: str,
        args: dict,
        state: AgentState,
    ) -> ToolExecution:
        # 사전 검증
        pre_check = self.validator.pre_validate(tool_name, args, state)
        if not pre_check.allowed:
            return ToolExecution.denied(pre_check.reason)

        # 실행
        try:
            tool_fn = self.tools[tool_name]
            result = tool_fn(**args)
        except Exception as e:
            return ToolExecution.error(str(e))

        # 사후 검증
        post_check = self.validator.post_validate(tool_name, result, state)
        if post_check.has_error:
            return ToolExecution.invalid(post_check.message)

        return ToolExecution.success(result)
```

---

## 무한 루프 방지 전략

### 루프 발생 패턴

LLM이 루프에 빠지는 주요 패턴은 3가지다.

**패턴 1: 동일 Tool 반복 호출**
```
search("AI") → 결과 없음 → search("AI") → 결과 없음 → ...
```

**패턴 2: 서로 다른 Tool이 순환**
```
analyze() → needs_data → fetch() → needs_analysis → analyze() → ...
```

**패턴 3: 목표 달성 불가 루프**
```
write_report() → quality_check() → revision_needed → write_report() → ...
```

### 루프 방지 구현

```python
class LoopGuard:
    def __init__(self, max_steps: int = 20, max_same_tool: int = 3):
        self.max_steps = max_steps
        self.max_same_tool = max_same_tool

    def check(self, state: AgentState) -> LoopCheckResult:
        # 1. 최대 스텝 수 초과
        if state.total_steps >= self.max_steps:
            return LoopCheckResult.abort("최대 스텝 수 초과")

        # 2. 동일 Tool 연속 호출 횟수 초과
        recent = state.recent_tool_calls(n=self.max_same_tool)
        if len(set(recent)) == 1 and len(recent) == self.max_same_tool:
            return LoopCheckResult.abort(
                f"동일 Tool 연속 {self.max_same_tool}회 호출: {recent[0]}"
            )

        # 3. 동일 인자 반복 호출 탐지
        last_call = state.last_tool_call
        second_last = state.second_last_tool_call
        if last_call and second_last:
            if last_call == second_last:
                return LoopCheckResult.abort("동일 호출 반복 탐지")

        return LoopCheckResult.ok()

class AgentWithLoopGuard:
    def run(self, goal: Goal) -> Result:
        state = AgentState(goal=goal)
        guard = LoopGuard(max_steps=20, max_same_tool=3)

        while not state.is_terminal():
            # 루프 감시
            check = guard.check(state)
            if not check.ok:
                state.abort(check.reason)
                break

            action = self.decide(state)
            result = self.executor.execute(action, state)
            state.update(action, result)

        return state.result
```

---

## Tool 실패 시 Fallback 구현

### Fallback 전략 3가지

**전략 1: 대체 Tool 사용**
```python
FALLBACK_MAP = {
    "search_api_premium": "search_api_free",
    "gpt4_summary": "gpt35_summary",
    "live_stock_price": "cached_stock_price",
}

def execute_with_fallback(tool_name: str, args: dict) -> Any:
    try:
        return TOOLS[tool_name](**args)
    except ToolError:
        fallback = FALLBACK_MAP.get(tool_name)
        if fallback:
            return TOOLS[fallback](**args)
        raise
```

**전략 2: 부분 결과 활용**
```python
def search_with_partial_fallback(
    urls: list[str],
) -> list[dict]:
    results = []
    for url in urls:
        try:
            content = fetch_url(url)
            results.append({"url": url, "content": content, "ok": True})
        except Exception as e:
            # 실패한 URL은 건너뛰고 부분 결과 수집
            results.append({"url": url, "error": str(e), "ok": False})

    successful = [r for r in results if r["ok"]]
    if not successful:
        raise AllToolsFailedError("모든 URL 접근 실패")

    return successful
```

**전략 3: LLM 내부 지식으로 대체**
```python
def answer_with_fallback(query: str, search_failed: bool) -> str:
    if search_failed:
        # 검색 실패 시 LLM 내부 지식으로 답변
        prompt = f"""
검색 도구가 일시적으로 사용 불가합니다.
당신의 학습 데이터 기반으로 다음 질문에 답하세요.
단, 실시간 정보가 필요한 경우 "최신 정보 확인 불가"를 명시하세요.

질문: {query}
"""
        return llm.invoke(prompt).content
    return search_and_answer(query)
```

---

## 비교: 검증 방식

| 검증 방식 | 시점 | 역할 | 구현 위치 |
|-----------|------|------|-----------|
| **Schema 검증** | 호출 전 | 타입, 필수 필드 확인 | Pydantic |
| **의미 검증** | 호출 전 | 비즈니스 규칙 확인 | ToolValidator |
| **권한 검증** | 호출 전 | 실행 허용 여부 | ToolValidator |
| **결과 검증** | 호출 후 | 출력 품질 확인 | ToolResultValidator |
| **루프 감시** | 매 스텝 | 반복 패턴 탐지 | LoopGuard |

---

## 주의사항

### 1. Tool 설명을 LLM이 읽는다는 것을 잊지 않는다

Docstring과 Field description이 LLM의 판단 근거다.
모호한 설명은 잘못된 호출을 유발한다.
"언제 쓰는가"와 "언제 쓰면 안 되는가"를 명시한다.

### 2. 사전 검증과 스키마 검증을 혼동하지 않는다

스키마 검증: 형식이 올바른가 (타입, 길이, 패턴)
사전 검증: 의미가 올바른가 (권한, 비즈니스 규칙)
둘 다 필요하다.

### 3. 실패를 LLM에게 알려야 한다

Tool 실패를 무시하면 LLM이 성공한 줄 알고 다음 단계로 넘어간다.
실패 정보를 State에 기록하고 LLM에 피드백한다.

### 4. 되돌릴 수 없는 Tool은 특별히 관리한다

이메일 발송, 파일 삭제, API 결제 등은 한 번 실행하면 되돌릴 수 없다.
추가 확인 단계나 dry-run 모드를 구현한다.
프로덕션에서는 human-in-the-loop를 고려한다.

---

## 코드 예제: 완전한 Tool 검증 시스템

```python
from dataclasses import dataclass
from typing import Any, Callable
from enum import Enum
import time

class ValidationStatus(Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    ERROR = "error"

@dataclass
class ValidationResult:
    status: ValidationStatus
    reason: str = ""

    @classmethod
    def allow(cls): return cls(ValidationStatus.ALLOWED)

    @classmethod
    def deny(cls, reason: str): return cls(ValidationStatus.DENIED, reason)

@dataclass
class ToolCall:
    name: str
    args: dict
    timestamp: float = 0.0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()

    def __eq__(self, other):
        return self.name == other.name and self.args == other.args

@dataclass
class AgentExecutionState:
    goal: str
    total_steps: int = 0
    call_history: list[ToolCall] = None

    def __post_init__(self):
        if self.call_history is None:
            self.call_history = []

    def record_call(self, call: ToolCall):
        self.call_history.append(call)
        self.total_steps += 1

    def recent_calls(self, n: int) -> list[ToolCall]:
        return self.call_history[-n:]

class ToolOrchestrator:
    """Tool 실행의 단일 진입점"""

    def __init__(
        self,
        tools: dict[str, Callable],
        max_steps: int = 20,
        max_repeat: int = 3,
    ):
        self.tools = tools
        self.max_steps = max_steps
        self.max_repeat = max_repeat

    def pre_validate(
        self,
        call: ToolCall,
        state: AgentExecutionState,
    ) -> ValidationResult:
        # 최대 스텝 수 검사
        if state.total_steps >= self.max_steps:
            return ValidationResult.deny(
                f"최대 스텝({self.max_steps}) 초과"
            )

        # 반복 호출 검사
        recent = state.recent_calls(self.max_repeat)
        if len(recent) == self.max_repeat:
            if all(c == call for c in recent):
                return ValidationResult.deny(
                    f"동일 호출 {self.max_repeat}회 반복 탐지"
                )

        # Tool 존재 검사
        if call.name not in self.tools:
            return ValidationResult.deny(f"알 수 없는 Tool: {call.name}")

        return ValidationResult.allow()

    def execute(
        self,
        call: ToolCall,
        state: AgentExecutionState,
    ) -> dict:
        # 사전 검증
        pre = self.pre_validate(call, state)
        if pre.status != ValidationStatus.ALLOWED:
            return {
                "status": "denied",
                "reason": pre.reason,
                "result": None,
            }

        # 실행
        state.record_call(call)
        try:
            result = self.tools[call.name](**call.args)
            return {"status": "ok", "result": result, "error": None}
        except Exception as e:
            return {"status": "error", "result": None, "error": str(e)}


# ── 사용 예시 ─────────────────────────────────────
def mock_search(query: str) -> list[str]:
    if query == "fail":
        raise ConnectionError("검색 API 연결 실패")
    return [f"{query} 결과_{i}" for i in range(3)]

def mock_summarize(texts: list[str]) -> str:
    return f"요약: {', '.join(texts[:2])}"

orchestrator = ToolOrchestrator(
    tools={"search": mock_search, "summarize": mock_summarize},
    max_steps=10,
    max_repeat=3,
)

exec_state = AgentExecutionState(goal="AI 뉴스 요약")

# 정상 호출
r1 = orchestrator.execute(
    ToolCall("search", {"query": "AI 2026"}),
    exec_state,
)
print(r1)  # {"status": "ok", "result": [...], "error": None}

# 실패 호출 → Fallback 필요
r2 = orchestrator.execute(
    ToolCall("search", {"query": "fail"}),
    exec_state,
)
print(r2)  # {"status": "error", "result": None, "error": "검색 API 연결 실패"}
```

---

## Q&A

**Q1. Tool Docstring이 LLM 성능에 얼마나 영향을 미치나요?**

실험에 따르면 명확한 docstring이 Tool 선택 정확도를 20~40% 향상시킵니다.
"언제 사용하는가", "언제 사용하면 안 되는가"를 포함하는 것이 핵심입니다.
짧고 명확한 설명이 길고 모호한 설명보다 낫습니다.

**Q2. 사전 검증을 통과한 호출이 실패하면 어떻게 처리하나요?**

실패 정보를 State에 기록하고 LLM에 피드백합니다.
재시도 횟수에 따라 다른 전략을 선택합니다.
1회: 동일 인자로 재시도 / 2회: 대체 Tool 시도 / 3회: Fallback.

**Q3. 루프 방지의 max_steps는 어떻게 결정하나요?**

Task의 예상 복잡도를 기준으로 설정합니다.
일반적으로 예상 단계 수의 2~3배로 설정합니다.
너무 작으면 정상 종료 전에 중단되고, 너무 크면 루프 방지 효과가 없습니다.

**Q4. 되돌릴 수 없는 Tool은 어떻게 안전하게 처리하나요?**

Dry-run 모드를 먼저 실행해서 결과를 LLM에 확인시킵니다.
Human-in-the-loop 게이트를 추가해 사람이 승인하도록 합니다.
실행 로그를 상세히 남겨 감사(audit) 가능하게 합니다.

---

## 퀴즈

**Q1.** Tool 스키마에서 `Field(description="...")` 작성 시 가장 중요한 내용은?

<details>
<summary>힌트 및 정답</summary>

**힌트**: LLM은 이 description을 읽고 언제 이 Tool을 써야 할지 판단합니다.

**정답**: 언제 사용하는가 + 언제 사용하면 안 되는가

Tool을 부적절하게 사용하는 상황을 명시적으로 기술해야 LLM이 올바른 판단을 합니다. 예: "실시간 정보가 필요할 때 사용하세요. LLM이 이미 알고 있는 사실에는 사용하지 마세요."
</details>

---

**Q2.** 다음 중 "의미 검증(semantic validation)"에 해당하는 것은?

- A) `max_results`가 정수(int)인지 확인
- B) `email` 필드가 `@`를 포함하는지 확인
- C) `query` 필드의 길이가 100자 이하인지 확인
- D) 필수 필드가 모두 존재하는지 확인

<details>
<summary>힌트 및 정답</summary>

**힌트**: "의미"는 형식이 아니라 비즈니스 규칙과 관련됩니다.

**정답**: B

이메일 형식 검증은 문자열 타입 확인(A, C, D)과 달리 "이 값이 유효한 이메일인가"라는 의미를 검증합니다. A, C, D는 스키마 검증(형식)에 해당합니다.
</details>

---

**Q3.** Tool 실패 Fallback 전략 중 "LLM 내부 지식으로 대체"의 단점은?

<details>
<summary>힌트 및 정답</summary>

**힌트**: LLM의 학습 데이터에는 어떤 한계가 있나요?

**정답**: 최신 정보나 실시간 데이터를 제공할 수 없다

LLM 내부 지식은 학습 시점까지의 정보만 포함합니다. 오늘의 주가, 최신 뉴스, 실시간 날씨 등은 제공이 불가능합니다. 사용자에게 "최신 정보 확인 불가" 상태임을 명시해야 합니다.
</details>

---

**Q4.** 무한 루프 방지에서 "동일 인자 반복 호출 탐지"가 필요한 이유는?

<details>
<summary>힌트 및 정답</summary>

**힌트**: 다른 Tool을 번갈아 호출해도 루프가 발생할 수 있습니다.

**정답**: 최대 스텝 수 검사만으로는 탐지할 수 없는 조기 루프를 발견하기 위해

예를 들어 max_steps=20인데 3번째 스텝부터 동일 호출이 반복된다면, 20번까지 기다리지 않고 조기에 탐지하고 중단할 수 있습니다. 비용과 시간을 절약합니다.
</details>

---

**Q5.** `with_structured_output()`을 사용해 Tool 결정을 받는 주요 이점은?

<details>
<summary>힌트 및 정답</summary>

**힌트**: LLM이 자유롭게 JSON을 생성하면 어떤 문제가 생길까요?

**정답**: LLM이 반드시 지정된 스키마에 맞는 JSON을 생성하도록 강제하여 파싱 오류를 방지한다

자유 생성 시 LLM은 필드를 빠뜨리거나, 타입을 틀리거나, JSON 형식을 깨뜨릴 수 있습니다. `with_structured_output`은 Pydantic 모델로 응답을 강제해 이 문제를 해결합니다.
</details>

---

## 실습 명세

### 주제: Tool 실패 시 Fallback 구현

**목표**: Tool 호출 전후 검증과 Fallback 체인을 구현하여 안정적인 Tool 실행 시스템을 만든다.

---

### I DO (강사 시연, 15분)

강사가 "안전한 웹 검색 Tool"을 라이브로 구현한다.

- Pydantic 스키마로 Tool 정의
- 사전 검증 레이어 추가
- 실패 시 Fallback Tool로 전환하는 흐름 시연
- 의도적으로 Tool을 실패시켜 Fallback 동작 확인

---

### WE DO (함께 실습, 30분)

"데이터 처리 Tool 시스템"을 함께 구현한다.

**Step 1**: Tool 스키마 정의 (10분)

```python
class DataLoadInput(BaseModel):
    source: str = Field(description="??")
    format: str = Field(description="??")
    # 함께 완성
```

**Step 2**: 사전 검증 로직 구현 (10분)

어떤 조건을 검증해야 하는지 함께 논의하고 구현한다.

**Step 3**: Fallback 체인 구현 (10분)

```python
TOOL_FALLBACK_CHAIN = {
    "load_from_url": ["load_from_cache", "load_from_local"],
    # 함께 추가
}
```

---

### YOU DO (독립 실습, 45분)

**과제**: "멀티 소스 정보 수집 Agent"의 Tool 검증 시스템을 구현하라.

**요구사항**:
- 3개의 정보 소스(웹 검색, 데이터베이스, 캐시)에서 정보를 수집한다
- 각 소스마다 사전/사후 검증을 구현한다
- 소스 우선순위: 웹 검색 → 데이터베이스 → 캐시 순으로 Fallback
- 모든 소스 실패 시 LLM 내부 지식으로 응답한다
- 루프 방지: 동일 소스에 2회 이상 연속 시도하지 않는다

**평가 기준**:
- 사전 검증이 형식 검증과 의미 검증을 모두 포함하는가?
- Fallback 체인이 완전히 구현되었는가?
- 루프 방지 로직이 올바르게 동작하는가?
- 실패 상황을 LLM에 올바르게 피드백하는가?

**solution/** 디렉토리에 참고 구현 포함.
