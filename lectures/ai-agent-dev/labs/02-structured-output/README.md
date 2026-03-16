# 실습 02: Structured Output으로 Agent 행동 결정

## 실습 목적

Pydantic 모델과 JSON Schema를 활용하여 LLM의 응답을 안정적으로 구조화하고,
비즈니스 규칙을 코드 수준에서 강제하는 방법을 익힌다.

- **연관 세션**: Session 2 - Structured Output 및 JSON Schema 응답 통제 전략
- **난이도**: 중급
- **예상 소요 시간**: 35분 (I DO 5분 / WE DO 15분 / YOU DO 15분)

## 사전 준비

```bash
export OPENROUTER_API_KEY="your-api-key"
export MODEL="moonshotai/kimi-k2"
just setup
```

---

## I DO: 시연 관찰 (약 5분)

강사가 시연하는 코드를 관찰하세요. 직접 코드를 작성하지 않아도 됩니다.

### 시연 내용

- `TicketClassification` Pydantic 모델 정의
- `client.beta.chat.completions.parse`로 구조화된 응답 받기
- enum 필드가 허용된 값만 생성됨을 확인

### 시연 코드 실행

```bash
just run-i-do
```

### 관찰 포인트

- `response_format=TicketClassification`으로 스키마를 강제한다
- 결과는 바로 Pydantic 객체로 사용 가능하다 (`result.category`, `result.urgency`)
- JSON 파싱 오류가 원천적으로 발생하지 않는다
- `AgentDecision`처럼 중첩 모델도 지원한다

---

## WE DO: 함께 실습 (약 15분)

강사와 함께 `src/we-do/agent_action.py`의 TODO를 채워봅니다.

### 1단계: AgentAction 필드 추가

```python
class AgentAction(BaseModel):
    thought: str = Field(description="현재 상황 분석")
    action_type: ActionType = Field(description="선택한 행동")
    # 함께 추가할 필드:
    parameters: dict = Field(default_factory=dict, description="행동 파라미터")
    confidence: float = Field(ge=0.0, le=1.0, description="확신도")
    reasoning: str = Field(description="이 행동을 선택한 이유")
```

### 2단계: 비즈니스 규칙 구현

```bash
just run-we-do
```

`validate_agent_action` 함수에서 두 가지 규칙을 함께 구현합니다:
- 규칙 1: confidence > 0.8이면서 ESCALATE는 비효율적
- 규칙 2: "환불"이 포함된 thought는 반드시 ESCALATE

---

## YOU DO: 독립 과제 (약 15분)

`src/you-do/agent_action.py`를 완성하세요.

### 과제 설명

1. `AgentAction` 모델에 `parameters`, `confidence`, `reasoning` 필드를 추가하세요
2. `decide_action` 함수를 구현하세요 (환불 → escalate 규칙 포함)
3. `validate_agent_action` 함수에 비즈니스 규칙 2개를 구현하세요
4. `run_scenarios`로 5개 시나리오를 테스트하세요

### 시작 방법

```bash
just run
```

### 힌트

<details>
<summary>힌트 1: confidence 필드 범위 제약</summary>

Pydantic의 `Field`에 `ge`(greater or equal), `le`(less or equal) 인자를 사용합니다:

```python
confidence: float = Field(ge=0.0, le=1.0, description="확신도")
```
</details>

<details>
<summary>힌트 2: client.beta.chat.completions.parse 사용법</summary>

```python
response = client.beta.chat.completions.parse(
    model=MODEL,
    messages=[...],
    response_format=AgentAction,  # Pydantic 모델 클래스를 직접 전달
)
return response.choices[0].message.parsed  # 이미 Pydantic 객체로 반환됨
```
</details>

<details>
<summary>힌트 3: 비즈니스 규칙 구현</summary>

```python
# 규칙 1
if action.action_type == ActionType.ESCALATE and action.confidence > 0.8:
    return False, "높은 confidence에서 escalate는 불필요"

# 규칙 2
if "환불" in action.thought and action.action_type != ActionType.ESCALATE:
    return False, "환불 관련 문의는 escalate 필수"
```
</details>

### 정답 확인

```bash
just run-solution
```

---

## 검증 방법

```bash
just test
```

- 5개 시나리오 모두 결과가 출력되는가
- 환불 문의에서 `escalate` 행동이 선택되는가
- `validate_agent_action`이 규칙 위반을 감지하는가

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| `AttributeError: 'NoneType' object` | `decide_action`이 None 반환 | 함수 구현 확인 |
| `ValidationError: confidence` | 범위 초과 값 | `ge=0.0, le=1.0` Field 설정 확인 |
| `beta` 속성 없음 | openai 구버전 | `pip install --upgrade openai` |
| enum 검증 오류 | 모델이 허용되지 않은 값 생성 | 시스템 프롬프트에 allowed values 명시 |
