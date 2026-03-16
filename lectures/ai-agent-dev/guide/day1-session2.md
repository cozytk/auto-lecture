# Session 2: LLM 동작 원리 및 프롬프트 전략 심화 (2h)

## 학습 목표
1. Context Window, Token, Hallucination의 동작 원리를 이해하고 실무 설계에 반영할 수 있다
2. Zero-shot, Few-shot, Chain-of-Thought 전략의 차이를 이해하고 상황에 맞게 선택할 수 있다
3. Structured Output과 JSON Schema를 활용하여 LLM 응답을 안정적으로 통제할 수 있다

---

## 개념 1: Context Window, Token, Hallucination 이해

### 왜 이것이 중요한가

LLM 기반 Agent 설계 시 반드시 이해해야 할 3가지 제약 조건이 있다.
**Token, Context Window, Hallucination**이다.

이 제약을 모르면 다음 질문에 답할 수 없다:
- "왜 Agent가 갑자기 엉뚱한 답을 하는가?"
- "왜 긴 문서를 처리하지 못하는가?"
- "왜 비용이 예상보다 10배 나오는가?"

> 자동차를 운전하려면 연료 탱크 크기, 연비, 브레이크 성능을 알아야 한다.
> LLM을 활용하려면 이 3가지 제약의 동작 원리를 이해해야 한다.

---

### 핵심 원리: Token

LLM은 글자나 단어 단위가 아닌 **토큰(Token)** 단위로 처리한다.
토큰은 BPE(Byte Pair Encoding) 알고리즘으로 생성된 서브워드 단위다.

**영어**: 약 1 토큰 = 4글자 또는 0.75 단어
**한국어**: 약 1 토큰 = 1~2글자 → 영어 대비 **2~3배 토큰 소비**

> **실무 팁**: 시스템 프롬프트는 영어로 작성하고, 사용자 대면 응답만 한국어로 분리하면
> 성능과 비용 모두 최적화할 수 있다.

---

### 핵심 원리: Context Window

Context Window = LLM이 한 번에 처리할 수 있는 **최대 토큰 수**
= LLM의 "작업 메모리"

**중요한 점**: 입력(프롬프트) + 출력(응답)의 합계가 이 한도를 넘을 수 없다.

Agent에서 Context Window는 특히 중요하다.
- 시스템 프롬프트 + Tool 스키마 + 대화 이력 + 현재 입력을 모두 넣어야 함
- 턴이 누적될수록 대화 이력이 증가 → 가용 공간 감소

> **"Lost in the Middle" 현상**: Context 중간에 위치한 정보를 잘 활용하지 못한다.
> Context Window가 크다고 무조건 좋은 것이 아니다.

---

### 핵심 원리: Hallucination

Hallucination = LLM이 학습 데이터에 없는 정보를 사실인 것처럼 생성하는 현상

LLM은 "가장 그럴듯한 다음 토큰"을 예측하는 확률 모델이다.
학습 데이터에서 답을 찾지 못하면 패턴에 기반한 답을 "만들어낸다."

**Agent에서 Hallucination이 특히 위험한 이유:**
→ 잘못된 판단이 **실제 행동으로 실행**되기 때문

- 존재하지 않는 API 엔드포인트 호출
- 잘못된 SQL 쿼리로 데이터 손상
- 잘못된 금액으로 결제 처리

**완화 전략:**
- **Grounding**: 외부 데이터로 답변 근거 제공
- **Validation**: 행동 전 파라미터 검증
- **Confirmation**: 고위험 행동에 인간 승인
- **Structured Output**: JSON Schema로 출력 형식 강제
- **Temperature 조절**: 사실 기반 작업에서 낮은 값 사용

---

### 실무에서의 의미

3가지 제약은 Agent의 비용, 성능, 안전성에 직접 영향을 미친다.

| 제약 | 이해하면 | 모르면 |
|------|---------|--------|
| Token | 불필요한 비용을 줄일 수 있다 | 예상보다 10배 비용 발생 |
| Context Window | 대화 이력 관리 전략을 설계할 수 있다 | 긴 대화에서 예측 불가 실패 |
| Hallucination | 적절한 안전 장치를 배치할 수 있다 | 프로덕션에서 비가역적 오류 반복 |

---

### 다른 접근법과의 비교

| 구분 | 일반 챗봇 | RAG | Agent |
|------|---------|-----|-------|
| Hallucination 영향 | 잘못된 정보 제공 | 검색 결과와 무관한 답변 | **실제 시스템 변경** |

---

### 주의사항

> **Context Window가 크면 클수록 좋은 것이 아니다.**
> (1) 비용 증가: 입력 토큰이 많으면 비용이 비례 증가
> (2) "Lost in the Middle" 현상: 중간 정보를 잘 활용하지 못함
> (3) 지연 시간: 입력이 길면 첫 토큰까지의 지연(TTFT)이 증가

---

### 코드 예제

이를 코드로 확인하면:

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

# 영어: 약 1 token ~ 4글자
english_text = "The quick brown fox jumps over the lazy dog."
en_tokens = enc.encode(english_text)
print(f"영어: 글자 수 {len(english_text)}, 토큰 수 {len(en_tokens)}")

# 한국어: 약 1 token ~ 1-2글자 (영어 대비 2-3배)
korean_text = "빠른 갈색 여우가 게으른 개를 뛰어넘는다."
ko_tokens = enc.encode(korean_text)
print(f"한국어: 글자 수 {len(korean_text)}, 토큰 수 {len(ko_tokens)}")
```

실행 결과:

```
영어: 글자 수 44, 토큰 수 10
한국어: 글자 수 21, 토큰 수 22
```

Context Window 기준 실제 사용 가능 토큰 계산:

```python
context_windows = {
    "GPT-4o":     {"window": 128_000, "max_output": 16_384},
    "GPT-4.1":    {"window": 1_048_576, "max_output": 32_768},
    "Claude 3.7": {"window": 200_000, "max_output": 128_000},
    "Gemini 2.0": {"window": 1_048_576, "max_output": 8_192},
}

def estimate_capacity(model: str, system_tokens: int, tool_tokens: int):
    spec = context_windows[model]
    usable = spec["window"] - spec["max_output"] - system_tokens - tool_tokens
    print(f"[{model}] 실제 사용 가능: {usable:,} tokens (~A4 {usable // 800}장)")

# Agent: 시스템 프롬프트 2000토큰, Tool 스키마 3000토큰 가정
for model in context_windows:
    estimate_capacity(model, 2000, 3000)
```

---

### Q&A

**Q: Context Window가 크면 클수록 좋은 것 아닌가요?**
A: 반드시 그렇지 않다.
(1) 비용 증가: 입력 토큰이 많으면 비용이 비례 증가한다.
(2) "Lost in the Middle" 현상: 중간에 있는 정보를 잘 활용하지 못하는 경향이 있다.
(3) 지연 시간: 입력이 길면 첫 토큰까지의 지연(TTFT)이 증가한다.
Agent 설계 시 필요한 정보만 선별하여 넣는 것이 중요하다.

**Q: 한국어 프롬프트가 영어 프롬프트보다 성능이 나쁜가요?**
A: 일반적으로 영어 프롬프트가 성능이 더 좋은 경우가 많다.
학습 데이터에서 영어 비중이 압도적으로 높기 때문이다.
같은 내용을 한국어로 표현하면 토큰을 2-3배 소비한다.
실무 팁: **시스템 프롬프트는 영어**, 사용자 대면 응답은 한국어로 분리하면 최적화 가능하다.

<details>
<summary>퀴즈: Agent가 10턴 대화를 할 때, 마지막 턴의 입력 토큰이 급격히 증가하는 이유는?</summary>

**힌트**: Agent는 매 턴마다 "이전 대화 전체"를 LLM에 다시 보내야 한다.

**정답**: LLM은 Stateless이므로, 매 턴마다 이전 대화 이력 전체를 입력에 포함해야 한다.
10턴째에는 1~9턴의 모든 입력+출력이 누적되어 입력 토큰이 급격히 증가한다.
이것이 Agent에서 **대화 이력 관리(요약, 슬라이딩 윈도우)**가 중요한 이유다.
예: 매 턴 평균 800토큰이면 10턴째 입력은 약 7,200토큰이 이전 이력만으로 소비된다.
</details>

---

## 개념 2: Zero-shot / Few-shot / Chain-of-Thought 전략 비교

### 왜 이것이 중요한가

프롬프트 전략은 LLM에게 "어떻게 생각하게 할 것인가"를 결정한다.
같은 LLM, 같은 문제라도 프롬프트 구성에 따라 결과 품질이 극적으로 달라진다.

Agent의 핵심 동작인 "상황 판단 → 행동 결정"의 품질은 프롬프트 전략에 좌우된다.
잘못된 전략을 선택하면:
- 단순한 문제에 과도한 비용
- 복잡한 판단에서 부정확한 결과

---

### 핵심 원리

프롬프트 전략은 3가지로 분류된다.
"LLM에게 제공하는 맥락의 양과 사고 구조의 깊이"에 따라 구분한다.

**Zero-shot**
→ 예시 없이 지시만 전달
→ "고객 문의를 분류하세요" 처럼 무엇을 해야 하는지만 전달
→ 토큰 사용량 최소, 설정 간단
→ 모호하거나 복잡한 작업에서 결과 불안정

**Few-shot**
→ 입력-출력 쌍의 예시를 몇 개 제공
→ "이런 패턴으로 처리하라"고 알려주는 방식
→ 예시가 "임시 학습 데이터" 역할
→ 예시의 수보다 **예시의 질**이 더 중요

**Chain-of-Thought (CoT)**
→ "단계별로 생각하라"고 지시하여 추론 과정을 명시적으로 유도
→ 다단계 추론, 조건부 판단에서 큰 효과
→ 추론 과정 자체가 출력 토큰으로 소비 → 비용 증가

---

### 실무에서의 의미

Agent 설계에서 프롬프트 전략은 "비용-정확도-지연"의 트레이드오프를 결정한다.

단순 분류에 CoT를 쓰면:
→ 비용·지연이 3~5배 증가
→ 정확도 개선은 미미

복잡한 행동 결정에 Zero-shot을 쓰면:
→ 비용은 절약
→ 잘못된 판단으로 Agent가 엉뚱한 행동을 실행

> **실무 권장**: 각 단계마다 적합한 전략을 다르게 적용하는 "적응형 전략(Adaptive Strategy)"

---

### 다른 접근법과의 비교

| 전략 | 토큰 사용량 | 적합한 경우 | Agent 활용 |
|------|------------|-----------|-----------|
| **Zero-shot** | 최소 | 명확한 단일 지시, 직관적 분류 | 간단한 의도 분류, 키워드 추출 |
| **Few-shot** | 중간 | 패턴이 명확하고 예시로 설명 가능 | 정형화된 분류, 포맷 변환, 엔티티 추출 |
| **CoT** | 많음 | 다단계 추론, 조건부 판단 필요 | 계획 수립, 복잡한 의사결정, 에러 분석 |

---

### 주의사항

> **CoT를 단순한 작업에 적용하면:**
> (1) 불필요한 추론으로 토큰 낭비
> (2) 과도한 사고로 잘못된 결론에 도달(overthinking)
>
> CoT는 "사람도 단계별로 생각해야 하는" 복잡한 문제에만 사용하라.

---

### 코드 예제

이를 코드로 구현하면:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

def call_llm(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model=MODEL, messages=messages, temperature=0,
    )
    return response.choices[0].message.content


# 1. Zero-shot: 예시 없이 지시만으로 수행
def zero_shot_classify(text: str) -> str:
    messages = [
        {"role": "system", "content": "고객 문의를 다음 카테고리 중 하나로 분류하세요: 환불, 배송, 제품문의, 기타"},
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


# 2. Few-shot: 예시를 제공하여 패턴 학습 유도
def few_shot_classify(text: str) -> str:
    messages = [
        {"role": "system", "content": "고객 문의를 다음 카테고리 중 하나로 분류하세요: 환불, 배송, 제품문의, 기타"},
        {"role": "user", "content": "주문한 지 일주일인데 아직 안 왔어요"},
        {"role": "assistant", "content": "배송"},
        {"role": "user", "content": "이 제품 사이즈가 어떻게 되나요?"},
        {"role": "assistant", "content": "제품문의"},
        {"role": "user", "content": "결제했는데 취소하고 돈 돌려받고 싶어요"},
        {"role": "assistant", "content": "환불"},
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


# 3. Chain-of-Thought: 단계별 추론 유도
def cot_classify(text: str) -> str:
    messages = [
        {"role": "system", "content": """고객 문의를 분류하세요.

단계별로 분석하세요:
1. 고객이 언급한 핵심 키워드를 추출하세요
2. 고객의 의도(원하는 행동)를 파악하세요
3. 의도에 맞는 카테고리를 선택하세요

카테고리: 환불, 배송, 제품문의, 기타

응답 형식:
키워드: [추출된 키워드]
의도: [파악된 의도]
카테고리: [선택된 카테고리]"""},
        {"role": "user", "content": text},
    ]
    return call_llm(messages)
```

실행 결과 (복합 문의에 대한 비교):

```
=== Zero-shot ===
환불

=== Few-shot ===
환불

=== Chain-of-Thought ===
키워드: [배송, 색상 다름, 교환, 품절, 환불]
의도: [잘못된 상품을 받아 교환을 원했으나 품절로 불가하여 환불을 요청]
카테고리: 환불
```

CoT는 **"왜 환불로 분류했는지" 추론 과정이 로그로 남는다.**
Agent에서는 이 추론 과정이 다음 행동 결정의 핵심 입력이 된다.

---

### Q&A

**Q: Few-shot 예시는 몇 개가 적당한가요?**
A: 일반적으로 **3-5개**가 최적이다.
예시가 3개를 넘으면 성능 향상이 둔화되고, 5개를 넘으면 Context Window만 소비한다.
핵심은 **예시의 수보다 질**이다.
경계 케이스(edge case)를 포함한 다양한 예시 3개가 비슷한 쉬운 예시 10개보다 효과적이다.

**Q: CoT를 쓰면 항상 결과가 더 좋은가요?**
A: 아니다. 단순한 작업에 CoT를 쓰면
(1) 불필요한 추론으로 토큰 낭비
(2) 과도한 사고로 잘못된 결론에 도달(overthinking) 가능
CoT는 **"사람도 단계별로 생각해야 하는" 복잡한 문제**에만 사용하는 것이 원칙이다.

<details>
<summary>퀴즈: Agent의 "행동 결정" 단계에 가장 적합한 프롬프트 전략은?</summary>

**상황**: Agent가 고객 문의를 받고, "환불 처리", "상담원 연결", "FAQ 안내" 중 어떤 행동을 할지 결정해야 한다.
각 행동은 서로 다른 API를 호출하며, 잘못된 결정은 비용이 크다.

**힌트**: 행동의 결과가 되돌리기 어렵고 비용이 큰 결정에는 어떤 전략이 적합할까?

**정답**: **Chain-of-Thought**가 가장 적합하다.
(1) 행동 실행은 비가역적(환불 처리 후 취소 어려움)이므로 신중한 판단 필요
(2) 추론 과정이 로그로 남아 **"왜 이 행동을 선택했는지" 감사(audit)** 가능
(3) 복수의 조건(고객 상태, 주문 이력, 환불 정책)을 종합 판단해야 함
Zero-shot은 판단 근거가 불투명하고, Few-shot만으로는 모든 조건 조합을 커버할 수 없다.
</details>

---

## 개념 3: Structured Output 및 JSON Schema 응답 통제 전략

### 왜 이것이 중요한가

Agent에서 LLM의 응답은 "사용자에게 보여줄 텍스트"가 아니다.
LLM의 응답은 **다음 행동의 입력**이 된다.

"search_db 도구를 호출하겠다"는 결정이 프로그래밍적으로 파싱 가능해야 한다.
"데이터베이스에서 검색해보겠습니다"라는 자연어로는 어떤 도구를 어떤 파라미터로 호출해야 하는지 알 수 없다.

> 자연어 응답을 정규식으로 파싱하려는 시도는 반드시 깨진다.
> LLM의 응답 형식이 매번 미묘하게 달라지기 때문이다.

---

### 핵심 원리

Structured Output = LLM의 출력을 사전에 정의된 스키마에 맞추어 강제하는 기술

**API 수준 강제**
→ OpenAI의 `response_format`, Claude의 `tool_use`
→ 토큰 생성 시 문법적으로 올바른 JSON만 출력하도록 디코딩 단계에서 제약
→ JSON 구문 오류(중괄호 누락, 따옴표 불일치)가 원천적으로 발생하지 않음

**스키마 수준 검증**
→ 문법적으로 올바른 JSON이라도 값이 유효하지 않을 수 있음
→ enum 범위 밖의 값이 들어오는 경우 등
→ Pydantic 같은 검증 라이브러리로 잡아냄

---

### 실무에서의 의미

Structured Output 없이 Agent를 구축하면:
"10번 중 8번은 잘 되는데 2번은 깨지는" 불안정한 시스템이 된다.

다양한 입력 패턴에 의해 LLM의 응답 형식이 예기치 않게 변한다.
한 번의 파싱 실패가 Agent의 전체 워크플로우를 중단시킬 수 있다.

> **Structured Output은 Agent의 기본 요구사항이다.**
> LLM의 "창의성"을 제한하는 것이 Agent에서는 장점이다.
> Agent의 행동 결정은 예측 가능하고 파싱 가능한 출력이 필수다.

---

### 다른 접근법과의 비교

| 방식 | 문법 오류 | 값 유효성 | 유지보수 | 복잡한 구조 |
|------|---------|---------|---------|-----------|
| 정규식 파싱 | 자주 발생 | 어려움 | 어려움 | 불가 |
| Function Calling/Tool Use | 없음 | Pydantic으로 검증 | 쉬움 | 가능 |
| Structured Output API | 없음 | Pydantic으로 검증 | 쉬움 | 가능 |

---

### 주의사항

> **JSON 파싱 에러 발생 시 3단계 방어 전략:**
> (1) Structured Output API 사용: 문법적으로 올바른 JSON 보장
> (2) Pydantic 검증: 값의 유효성 검증
> (3) 재시도(Retry): 파싱 실패 시 에러 메시지 포함하여 재요청 (최대 2-3회)

---

### 코드 예제

이를 코드로 구현하면:

```python
from pydantic import BaseModel, Field
from enum import Enum
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

class Urgency(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TicketClassification(BaseModel):
    """고객 문의 분류 결과"""
    category: str = Field(
        description="문의 카테고리",
        enum=["환불", "배송", "제품문의", "기술지원", "기타"],
    )
    urgency: Urgency = Field(description="긴급도")
    summary: str = Field(description="문의 요약 (1문장)", max_length=100)
    suggested_action: str = Field(description="권장 행동")

def classify_ticket(query: str) -> TicketClassification:
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "고객 문의를 분류하세요."},
            {"role": "user", "content": query},
        ],
        response_format=TicketClassification,
    )
    return response.choices[0].message.parsed

result = classify_ticket("배송 받았는데 색상이 다르고 환불 원합니다")
print(result.model_dump_json(indent=2))
```

실행 결과:

```json
{
  "category": "환불",
  "urgency": "high",
  "summary": "배송된 상품의 색상이 주문과 다르며 환불을 요청",
  "suggested_action": "환불 절차 안내 및 반품 접수"
}
```

Agent에서 행동 결정을 구조화하면:

```python
class ToolCall(BaseModel):
    tool_name: str = Field(
        description="호출할 도구 이름",
        enum=["search_db", "send_email", "create_ticket", "escalate"],
    )
    parameters: dict = Field(description="도구에 전달할 파라미터")
    reasoning: str = Field(description="이 도구를 선택한 이유")

class AgentDecision(BaseModel):
    thought: str = Field(description="현재 상황에 대한 분석")
    action: ToolCall = Field(description="실행할 행동")
    is_final: bool = Field(description="이것이 최종 행동인지 여부")
```

---

### Q&A

**Q: Structured Output을 쓰면 LLM의 창의성이 제한되지 않나요?**
A: 그렇다. 그리고 그것이 **Agent에서는 장점**이다.
Agent의 행동 결정은 "창의적"이면 안 된다.
예측 가능하고 파싱 가능한 출력이 필수다.
창의성이 필요한 부분(보고서 본문 작성 등)은 별도의 자유 텍스트 필드로 분리하면 된다.

**Q: JSON 파싱 에러가 발생하면 어떻게 처리하나요?**
A: 3단계 방어 전략을 쓴다.
(1) **Structured Output API**: OpenAI `response_format` 또는 Claude `tool_use`는 문법적으로 올바른 JSON을 보장한다.
(2) **Pydantic 검증**: 문법은 맞지만 값이 유효하지 않은 경우를 잡아낸다.
(3) **재시도(Retry)**: 파싱 실패 시 에러 메시지를 포함하여 재요청한다. 최대 2-3회 후 사람에게 에스컬레이션한다.

<details>
<summary>퀴즈: 다음 코드의 문제점은 무엇인가?</summary>

```python
response = llm.chat("주문 상태를 확인하고 결과를 알려줘")
# response = "주문번호 12345는 현재 배송 중이며, 내일 도착 예정입니다."

order_id = response.split("주문번호 ")[1].split("는")[0]
status = "배송 중" if "배송 중" in response else "unknown"
```

**힌트**: LLM의 응답 형식은 항상 동일한가?

**정답**: LLM의 자연어 응답은 매번 형식이 달라질 수 있다.
"주문번호 12345는..." 대신 "12345번 주문이..." 또는 "주문 12345의 상태는..."으로 응답할 수 있다.
`split` 기반 파싱은 즉시 깨진다.
올바른 방법: Structured Output으로 `{"order_id": "12345", "status": "배송중", "eta": "2025-03-07"}` 형태로 응답을 강제한다.
</details>

---

## 개념 4: 비용 및 Latency 관점 호출 최적화 설계

### 왜 이것이 중요한가

Agent는 한 번의 사용자 요청에 LLM을 **여러 번 호출**한다.
단순 챗봇이 1회 호출로 끝나는 반면, Agent는 5~10회 이상 호출할 수 있다.

**고급 모델로 10턴 Agent를 운영하면:**
- 요청 1건당 $0.1~$0.5 소요
- 응답 시간 30초~1분
- 하루 1,000건 처리 시 → 월 $3,000~$15,000 비용 발생

---

### 핵심 원리

Agent의 비용과 지연은 3가지 요소로 구성된다.

**① 누적 입력 토큰**
→ 가장 큰 비용 요인
→ LLM은 Stateless → 매 턴마다 이전 대화 이력 전체를 다시 보냄
→ 5턴에서 각 턴 800토큰이면, 5턴째 입력에만 3,200토큰이 이전 이력으로 소비

**② 출력 토큰**
→ 입력 토큰보다 단가가 2~5배 높음
→ Structured Output으로 간결한 JSON만 출력 → 비용 절감

**③ Tool 실행 시간**
→ 순차 실행 시 각 Tool의 지연이 합산
→ 독립적인 Tool 호출은 병렬 실행 → 총 지연을 max(개별 지연)으로 감소

---

### 실무에서의 의미

4가지 최적화 전략을 조합하면 비용 80% 이상, 지연 50% 이상 절감 가능하다.

**① 모델 라우팅 (Model Routing)**
→ 작업 복잡도에 따라 경량 모델과 고급 모델을 동적으로 선택
→ 단순 분류에 GPT-4를 쓸 필요가 없다

**② 프롬프트 캐싱 (Prompt Caching)**
→ 매 턴 반복되는 시스템 프롬프트와 Tool 스키마를 캐싱
→ Anthropic: 캐시 히트 시 90% 절감
→ OpenAI: 50% 절감

**③ 병렬 호출 (Parallel Calls)**
→ 상호 의존이 없는 Tool 호출을 동시에 실행
→ 순차: 3개 × 2초 = 6초 / 병렬: max(2초) = 2초

**④ 대화 이력 압축 (Context Compression)**
→ 오래된 대화 이력을 요약으로 대체
→ 최근 3턴은 원본 유지, 이전 이력은 요약

---

### 다른 접근법과의 비교

| 구분 | API 기반 | 오픈소스 자체 호스팅 |
|------|---------|-------------------|
| 초기 비용 | 낮음 | 높음 (GPU 서버) |
| 대량 처리 비용 | 높음 | 낮음 |
| 관리 부담 | 없음 | 높음 |
| 최신 모델 | 즉시 사용 가능 | 직접 업데이트 필요 |
| 권장 시점 | 초기 ~ 중간 규모 | 트래픽 충분히 증가 후 |

---

### 주의사항

> **모델 라우팅에서 경량 모델이 실수하면 Fallback 패턴을 사용하라.**
> 경량 모델의 confidence score가 임계값 이하면 상위 모델로 재요청한다.
> 대부분의 요청(80-90%)은 경량 모델로 처리 → 전체 비용 크게 절감

---

### 코드 예제

이를 코드로 구현하면:

```python
import asyncio
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

# 전략 1: 모델 라우팅 -- 작업 복잡도에 따라 모델을 동적 선택
class ModelRouter:
    MODELS = {
        "simple": "gpt-4.1-mini",   # 빠르고 저렴 (분류, 추출)
        "moderate": "gpt-4o",        # 균형 (일반 추론)
        "complex": "claude-sonnet",  # 정확 (복잡한 판단)
    }

    def select_model(self, task_type: str) -> str:
        if task_type in ["classify", "extract", "format"]:
            return self.MODELS["simple"]
        elif task_type in ["analyze", "summarize"]:
            return self.MODELS["moderate"]
        else:  # plan, decide, reason
            return self.MODELS["complex"]


# 전략 2: 병렬 호출 -- 독립적인 Tool 호출을 동시에 실행
async def parallel_tool_calls(tools_to_call: list[dict]) -> list:
    async def call_tool(tool_config):
        result = await tool_config["fn"](**tool_config["params"])
        return {"tool": tool_config["name"], "result": result}

    return await asyncio.gather(*[call_tool(tc) for tc in tools_to_call])


# 전략 3: 대화 이력 압축 -- 오래된 이력을 요약으로 대체
class ContextCompressor:
    def compress(self, history: list[dict], max_tokens: int = 2000) -> list[dict]:
        """최근 3턴은 원본 유지, 이전 이력은 요약으로 대체."""
        if self.estimate_tokens(history) <= max_tokens:
            return history
        recent = history[-6:]   # user + assistant 쌍
        older = history[:-6]
        summary = self.summarize(older)
        return [{"role": "system", "content": f"이전 대화 요약: {summary}"}, *recent]
```

최적화 전후 비교:

```
=== 최적화 비교 ===
비용: $0.0500 -> $0.0072 (86% 절감)
지연: 18.5초 -> 9.5초 (49% 단축)
```

---

### Q&A

**Q: 모델 라우팅에서 경량 모델이 실수하면 어떻게 하나요?**
A: **Fallback 패턴**을 사용한다.
경량 모델의 출력에 대해 confidence score를 확인한다.
일정 임계값 이하면 상위 모델로 재요청한다.
대부분의 요청(80-90%)은 경량 모델로 처리되므로 전체 비용은 크게 절감된다.

**Q: 프롬프트 캐싱은 어떻게 동작하나요?**
A: OpenAI와 Anthropic 모두 자동 프롬프트 캐싱을 지원한다.
동일한 프롬프트 접두사(시스템 프롬프트 + Tool 스키마 등)가 반복되면 서버 측에서 캐시한다.
Anthropic: 캐시 히트 시 입력 비용의 90% 절감
OpenAI: 50% 절감
Agent는 매 턴마다 동일한 시스템 프롬프트를 보내므로 캐싱 효과가 크다.

<details>
<summary>퀴즈: Agent가 10턴 대화를 할 때, 가장 효과적인 비용 절감 전략 조합은?</summary>

**보기:**
1. 모든 턴에 최고급 모델 사용 + 프롬프트 캐싱
2. 모델 라우팅 + 대화 이력 압축 + 프롬프트 캐싱
3. 경량 모델만 사용 + 병렬 호출
4. 대화 이력 압축만 적용

**힌트**: 비용의 가장 큰 비중을 차지하는 요소는 "누적되는 입력 토큰"이다.

**정답**: 2번.
(1) **모델 라우팅**으로 단순 단계의 비용을 80% 절감
(2) **대화 이력 압축**으로 10턴째의 누적 입력 토큰을 대폭 감소
(3) **프롬프트 캐싱**으로 반복되는 시스템 프롬프트 비용 절감
이 3가지 조합이 비용과 품질 모두를 최적화한다.
3번은 품질 저하 위험이 있고, 1번과 4번은 부분적 최적화에 그친다.
</details>

---

## 실습

### 실습 1: 프롬프트 전략별 응답 비교

- **연관 학습 목표**: 학습 목표 2
- **실습 목적**: 동일한 문제에 Zero-shot, Few-shot, CoT를 적용하여 응답 품질과 비용 차이를 직접 확인한다
- **실습 유형**: 코드 작성
- **난이도**: 기초
- **예상 소요 시간**: 30분 (I DO 5분 / WE DO 10분 / YOU DO 15분)
- **선행 조건**: OpenRouter API 키 준비
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**I DO**: 강사가 단순 문의("주문 취소하고 싶어요")에 3가지 전략을 각각 적용하고 결과와 토큰 수를 비교한다.

**WE DO**: 복합 문의("색상이 다른데 교환 가능하면 교환, 안 되면 환불요")에 함께 3가지 전략을 적용하고 차이를 분석한다.

**YOU DO**:
아래 5개 고객 문의에 대해 3가지 전략을 각각 적용하고 비교 표를 작성한다.

```python
test_queries = [
    "주문 취소하고 싶어요",
    "배송이 너무 늦어요. 언제 오나요?",
    "색상이 다른데 교환 가능하면 교환, 안 되면 환불요",
    "지난번에 산 것도 문제였고 이번에도 문제네요",
    "제품은 좋은데 배송 중 파손됐어요. AS가 되나요?",
]
```

분석 질문:
- 어떤 유형의 문의에서 전략 간 차이가 가장 컸는가?
- CoT가 오히려 불필요했던 경우가 있는가?
- 비용 대비 성능이 가장 좋은 전략은?

**정답 예시 (비교 표)**:

| 문의 유형 | Zero-shot 결과 | Few-shot 결과 | CoT 결과 | 권장 전략 |
|---------|--------------|-------------|---------|---------|
| 단순 취소 | 환불 | 환불 | 환불 (과도한 추론) | Zero-shot |
| 복합 조건부 | 교환 (부정확) | 환불 | 환불 (정확, 이유 설명) | CoT |

---

### 실습 2: Structured Output으로 Agent 행동 결정 구현

- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: JSON Schema를 활용하여 Agent의 행동 결정을 안정적으로 구조화한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 35분 (I DO 5분 / WE DO 15분 / YOU DO 15분)
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**I DO**: 강사가 `TicketClassification` Pydantic 모델을 정의하고 5개 시나리오에 적용하는 전체 과정을 시연한다.

**WE DO**: 함께 `AgentAction` 스키마를 완성하고 비즈니스 규칙 검증 로직을 추가한다.

**YOU DO**:
아래 Agent 행동 스키마를 완성하고 5가지 고객 시나리오에 적용한다.

```python
from pydantic import BaseModel, Field
from enum import Enum

class ActionType(str, Enum):
    SEARCH = "search"
    RESPOND = "respond"
    ESCALATE = "escalate"
    CREATE_TICKET = "create_ticket"

class AgentAction(BaseModel):
    thought: str = Field(description="현재 상황 분석")
    action_type: ActionType = Field(description="선택한 행동")
    # TODO: parameters, confidence, reasoning 필드 추가
```

검증 함수를 작성하고 비즈니스 규칙 2개 이상을 구현한다.

**정답**:
```python
class AgentAction(BaseModel):
    thought: str = Field(description="현재 상황 분석")
    action_type: ActionType = Field(description="선택한 행동")
    parameters: dict = Field(default_factory=dict, description="행동 파라미터")
    confidence: float = Field(ge=0.0, le=1.0, description="확신도")
    reasoning: str = Field(description="이 행동을 선택한 이유")

def validate_agent_action(action: AgentAction) -> tuple[bool, str]:
    # 규칙 1: 높은 confidence에서 에스컬레이션은 불필요
    if action.action_type == ActionType.ESCALATE and action.confidence > 0.8:
        return False, "높은 confidence에서 에스컬레이션은 불필요"
    # 규칙 2: 환불 관련은 반드시 에스컬레이션
    if "환불" in action.thought and action.action_type != ActionType.ESCALATE:
        return False, "환불 관련 문의는 에스컬레이션 필수"
    return True, "Valid"
```

---

### 실습 3: 비용 최적화 시뮬레이션

- **연관 학습 목표**: 학습 목표 1, 3
- **실습 목적**: 모델 라우팅 + 대화 이력 압축을 적용하여 Agent 비용을 측정하고 비교한다
- **실습 유형**: 코드 작성 + 분석
- **난이도**: 심화
- **예상 소요 시간**: 25분 (I DO 5분 / WE DO 8분 / YOU DO 12분)
- **선행 조건**: 실습 2 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

**I DO**: 강사가 기본 설정(최적화 없음)으로 시뮬레이터를 실행하고 비용·지연 수치를 보여준다.

**WE DO**: 함께 모델 라우팅 로직을 구현하고 효과를 확인한다.

**YOU DO**:
아래 시뮬레이터를 완성하고 4가지 설정 조합으로 실행한다.

```python
class AgentCostSimulator:
    def __init__(self):
        self.pricing = {
            "gpt-4o":       {"input": 2.50, "output": 10.00, "latency_ms": 2000},
            "gpt-4.1-mini": {"input": 0.40, "output": 1.60, "latency_ms": 800},
        }

    def simulate(self, config: dict) -> dict:
        """
        config = {
            "turns": 10,
            "model_routing": True/False,
            "context_compression": True/False,
            "prompt_caching": True/False,
        }
        """
        # TODO: 구현하세요
        pass
```

4가지 설정 조합으로 시뮬레이션을 실행한다:
1. 기본 (최적화 없음)
2. 모델 라우팅만 적용
3. 모델 라우팅 + 이력 압축
4. 모델 라우팅 + 이력 압축 + 프롬프트 캐싱

**정답**:
```python
def simulate(self, config: dict) -> dict:
    turns = config.get("turns", 10)
    model_routing = config.get("model_routing", False)
    context_compression = config.get("context_compression", False)
    prompt_caching = config.get("prompt_caching", False)

    total_cost = 0
    total_latency = 0
    accumulated_tokens = 0

    for turn in range(1, turns + 1):
        model = "gpt-4.1-mini" if (model_routing and turn % 3 != 0) else "gpt-4o"
        price = self.pricing[model]

        if context_compression and accumulated_tokens > 2000:
            accumulated_tokens = 500  # 요약으로 압축

        input_tokens = accumulated_tokens + 500
        output_tokens = 300

        input_cost = (input_tokens / 1e6) * price["input"]
        if prompt_caching:
            input_cost *= 0.5  # 50% 캐싱 할인
        output_cost = (output_tokens / 1e6) * price["output"]

        total_cost += input_cost + output_cost
        total_latency += price["latency_ms"]
        accumulated_tokens += input_tokens + output_tokens

    return {"cost": total_cost, "latency_sec": total_latency / 1000}
```

---

## 핵심 정리
- **Token**은 LLM의 처리 단위이며, 한국어는 영어 대비 2-3배 토큰을 소비한다
- **Context Window** = 입력 + 출력 합계의 상한이며, Agent 설계 시 실제 사용 가능 공간을 계산해야 한다
- **Hallucination**은 Agent에서 특히 위험하다. 잘못된 판단이 실제 행동으로 이어지기 때문이다
- 프롬프트 전략은 **작업 복잡도에 따라 선택**: 단순 → Zero-shot, 패턴 → Few-shot, 복잡한 판단 → CoT
- **Structured Output**은 Agent의 필수 요소다. 자연어 파싱은 깨지고, JSON Schema가 안정적이다
- 비용 최적화의 핵심 3가지: **모델 라우팅 + 대화 이력 압축 + 프롬프트 캐싱**
