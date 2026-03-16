# Day 1 - Session 2: LLM 동작 원리 및 프롬프트 전략 심화

**시간**: 2시간 | **대상**: AI 개발자, 데이터 엔지니어, 기술 리더

---

## 1. 왜 중요한가

### 프롬프트는 Agent의 두뇌 설계다

Agent를 만든다는 것은 LLM을 코드로 제어한다는 뜻이다.
LLM이 어떻게 작동하는지 모르면 Agent 동작을 예측할 수 없다.
**프롬프트 전략이 결과 품질과 비용을 동시에 결정한다.**

> 잘못 설계된 프롬프트로 만든 Agent는 비싸고, 느리고, 부정확하다.
> 올바른 프롬프트 전략은 비용 50%, 지연 30%를 줄일 수 있다.

**이 세션에서 배우는 것**:
- Context Window와 Token의 실무적 의미
- Hallucination 원인과 완화 전략
- Zero-shot / Few-shot / CoT 전략 비교
- Structured Output (JSON Schema) 응답 통제
- 비용·Latency 관점의 호출 최적화

---

## 2. 핵심 원리

### 2-1. Context Window와 Token 이해

#### Token이란?

LLM은 텍스트를 **Token** 단위로 처리한다.
Token은 단어나 글자의 조각이다. 정확한 크기는 모델마다 다르다.

```
"AI Agent를 설계하자" → 약 7-10 토큰
"Hello World"         → 약 2-3 토큰
한국어는 영어보다 토큰 효율이 낮다 (같은 의미에 더 많은 토큰)
```

**실용적 Token 계산 기준** (2026년 기준):

| 단위 | 대략적 토큰 수 |
|------|---------------|
| 영어 단어 1개 | 1-2 토큰 |
| 한국어 글자 1개 | 1-2 토큰 |
| A4 페이지 (영문) | 약 500 토큰 |
| 코드 100줄 | 약 500-1,000 토큰 |

#### Context Window란?

LLM이 한 번에 처리할 수 있는 **최대 토큰 수**다.
System Prompt + User Message + 대화 이력 + 출력 모두 포함된다.

```
Context Window 예시 (모델별 차이 있음):
├── System Prompt     : 500 토큰
├── 대화 이력         : 2,000 토큰
├── 현재 사용자 입력  : 300 토큰
└── 출력 (Max Tokens) : 1,000 토큰
    = 총 3,800 토큰 사용
```

**Agent 설계 시 주의사항**:
- 긴 대화 이력은 Context를 빠르게 소모한다
- Context 초과 시 앞부분이 잘리거나 에러 발생
- RAG의 검색 결과도 Context를 소모한다

---

### 2-2. Hallucination 이해와 완화

#### Hallucination이란?

LLM이 사실이 아닌 내용을 자신감 있게 생성하는 현상이다.
확률 기반 모델의 구조적 한계다.

**Hallucination이 자주 발생하는 상황**:

```
① 최신 정보가 필요한 질문 (학습 데이터 이후 사건)
② 구체적 수치, 날짜, 인용 요청
③ 너무 제약이 없는 열린 질문
④ 모델이 잘 모르는 도메인의 세부 사항
```

#### 완화 전략

| 전략 | 설명 | 예시 |
|------|------|------|
| 근거 요청 | "왜 그렇게 생각하는지 설명하라" | CoT 프롬프트 |
| 출처 제공 | 관련 문서를 Context에 포함 | RAG 결합 |
| 불확실성 명시 | "모르면 모른다고 답하라" | System Prompt |
| 검증 루프 | 생성 후 별도 검증 단계 | 자기 검토 프롬프트 |
| 구조화 출력 | JSON Schema로 응답 제한 | Structured Output |

---

### 2-3. Zero-shot / Few-shot / CoT 전략 비교

#### Zero-shot

지시만 제공하고 예시 없이 수행을 요청한다.

```python
prompt = """
다음 고객 리뷰를 긍정/부정/중립으로 분류하라.

리뷰: "배송이 빠르긴 했는데 포장이 엉망이었어요."
"""
```

**장점**: 프롬프트가 짧다, 토큰 효율이 좋다
**단점**: 복잡한 작업에서 품질 저하
**적합**: 단순 분류, 번역, 요약

---

#### Few-shot

작업 방식을 예시(shot)로 보여준다.

```python
prompt = """
고객 리뷰를 긍정/부정/중립으로 분류하라.

예시 1:
리뷰: "제품이 정말 마음에 들어요!"
분류: 긍정

예시 2:
리뷰: "완전 실망입니다. 다시는 안 사요."
분류: 부정

예시 3:
리뷰: "평범한 제품이에요. 딱히 특별하지 않네요."
분류: 중립

리뷰: "배송이 빠르긴 했는데 포장이 엉망이었어요."
분류:
"""
```

**장점**: 출력 형식과 품질이 안정적
**단점**: 토큰 사용량 증가
**적합**: 형식이 중요한 작업, 도메인 특화 분류

---

#### Chain-of-Thought (CoT)

단계적 추론 과정을 포함하도록 유도한다.

```python
# Standard CoT
prompt = """
다음 문제를 단계별로 생각하며 풀어라.

문제: 창고에 박스가 150개 있다. 오전에 47개를 출고하고,
오후에 23개를 입고했다. 현재 박스는 몇 개인가?

단계별 풀이:
"""

# Zero-shot CoT (마법의 문장)
prompt = """
창고에 박스가 150개 있다. 오전에 47개를 출고하고,
오후에 23개를 입고했다. 현재 박스는 몇 개인가?

단계적으로 생각해보자.
"""
```

**장점**: 복잡한 추론 정확도 대폭 향상
**단점**: 출력 토큰이 많아져 비용/지연 증가
**적합**: 수학 문제, 논리 추론, 복잡한 판단

---

#### 전략 선택 가이드

```
작업이 단순한가? (분류, 번역)
  → Zero-shot 먼저 시도

출력 형식이 중요한가? (특정 구조 필요)
  → Few-shot 사용

여러 단계의 추론이 필요한가?
  → CoT 사용

비용이 제약인가?
  → Zero-shot > Few-shot > CoT 순으로 선택
```

---

### 2-4. Structured Output과 JSON Schema

Agent에서 LLM 출력은 대부분 다음 로직의 **입력**으로 사용된다.
자연어 응답을 파싱하는 것은 불안정하다.
**JSON Schema로 응답 형식을 강제하면 안정성이 크게 높아진다.**

#### 기본 Structured Output 예시

```python
import anthropic
import json

client = anthropic.Anthropic()

# JSON Schema 정의
response_schema = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["긍정", "부정", "중립"]
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
        },
        "reason": {
            "type": "string",
            "description": "분류 이유 (1문장)"
        }
    },
    "required": ["category", "confidence", "reason"]
}

def classify_review(review: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        system=f"""당신은 리뷰 분류 전문가다.
반드시 다음 JSON 형식으로만 응답하라:
{json.dumps(response_schema, ensure_ascii=False, indent=2)}
다른 텍스트는 절대 포함하지 마라.""",
        messages=[{
            "role": "user",
            "content": f"리뷰: {review}"
        }]
    )

    # 응답 파싱
    result = json.loads(response.content[0].text)
    return result

# 실행
review = "배송이 빠르긴 했는데 포장이 엉망이었어요."
result = classify_review(review)
print(f"분류: {result['category']}")
print(f"신뢰도: {result['confidence']:.0%}")
print(f"이유: {result['reason']}")
```

#### Tool Use를 활용한 Structured Output

```python
# Tool Use 방식 (더 안정적)
tools = [{
    "name": "classify_review",
    "description": "리뷰를 분류하고 결과를 반환한다",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "enum": ["긍정", "부정", "중립"]},
            "confidence": {"type": "number"},
            "reason": {"type": "string"}
        },
        "required": ["category", "confidence", "reason"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=256,
    tools=tools,
    tool_choice={"type": "tool", "name": "classify_review"},
    messages=[{"role": "user", "content": f"리뷰 분류: {review}"}]
)

# Tool Use 결과 추출
tool_result = response.content[0].input
print(tool_result)  # dict로 바로 사용 가능
```

---

### 2-5. 비용·Latency 최적화

#### 비용 계산 기본

```
비용 = (입력 토큰 × 입력 단가) + (출력 토큰 × 출력 단가)

일반적으로: 출력 단가 > 입력 단가 (3-5배)
```

**최적화 전략 우선순위**:

```
1순위: 모델 선택 최적화
   → 작업 복잡도에 맞는 모델 사용
   → 단순 분류에 고성능 모델 불필요

2순위: 출력 길이 제한
   → max_tokens 적절히 설정
   → 불필요한 설명 요청 제거

3순위: 입력 압축
   → 불필요한 Context 제거
   → 프롬프트 중복 제거

4순위: 캐싱 활용
   → Prompt Caching (반복 System Prompt)
   → 같은 질문에 캐시 응답
```

#### Latency 최적화

```python
import asyncio
import anthropic

client = anthropic.Anthropic()

# 병렬 호출로 Latency 단축
async def parallel_classify(reviews: list[str]) -> list[dict]:
    """여러 리뷰를 병렬로 분류한다"""
    tasks = [classify_review_async(r) for r in reviews]
    results = await asyncio.gather(*tasks)
    return results

# Streaming으로 체감 응답 속도 개선
def stream_response(prompt: str):
    """스트리밍으로 응답을 실시간 출력한다"""
    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
```

---

## 3. 실무 의미

### 프롬프트 전략이 Agent 아키텍처를 결정한다

**단순 호출 패턴** (Zero-shot):
- 단일 LLM 호출로 완결
- 빠르고 저렴하지만 복잡한 작업에 불안정

**계획-실행 패턴** (CoT + Tool Use):
- LLM이 계획을 세우고 Tool을 순서대로 호출
- 복잡한 작업에 적합하지만 비용과 지연 증가

**검증 패턴** (Few-shot + 자기 검토):
- 생성 후 별도 검증 단계 추가
- 정확도 향상, 비용 약 2배

**선택 기준**:

```
비용 < 정확도 → Zero-shot 먼저 시도
정확도 > 비용 → Few-shot + 검증
추론 필요     → CoT 필수
형식 중요     → Structured Output 필수
```

---

## 4. 비교

### 프롬프트 전략별 특성 비교

| 전략 | 토큰 사용 | 정확도 | 응답 속도 | 추천 상황 |
|------|-----------|--------|-----------|-----------|
| Zero-shot | 낮음 | 보통 | 빠름 | 단순 작업 |
| Few-shot | 중간 | 높음 | 중간 | 형식 중요 |
| CoT | 높음 | 높음 | 느림 | 복잡한 추론 |
| CoT + Few-shot | 매우 높음 | 매우 높음 | 느림 | 고정확도 필요 |

---

## 5. 주의사항

### 프롬프트 설계 실수

**① System Prompt 비대화**
- System Prompt가 너무 길면 매 호출마다 비용 증가
- 핵심만 남기고 나머지는 Few-shot이나 Tool Description으로 이동

**② JSON 파싱 실패 처리 누락**
- LLM이 가끔 JSON 형식을 어기는 응답을 한다
- 항상 try-except로 파싱 에러를 처리하라

**③ max_tokens 과소 설정**
- CoT 응답은 예상보다 길어질 수 있다
- 잘린 응답은 파싱 에러를 유발한다

**④ 모델 과사용**
- 모든 작업에 최고 성능 모델을 쓸 필요 없다
- 단계별로 적합한 모델을 선택하라

**⑤ 프롬프트 인젝션 무시**
- 사용자 입력이 System Prompt를 오염시킬 수 있다
- 사용자 입력을 항상 별도 태그로 감싸라

---

## 6. 코드 예제

### 전략별 비교 실습

```python
import anthropic
import time
import json

client = anthropic.Anthropic()

def measure_call(strategy_name: str, messages: list, system: str = "") -> dict:
    """LLM 호출 시간과 토큰 사용량을 측정한다"""
    start = time.time()

    kwargs = {
        "model": "claude-haiku-4-5",
        "max_tokens": 256,
        "messages": messages,
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)
    elapsed = time.time() - start

    return {
        "strategy": strategy_name,
        "response": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "latency_ms": round(elapsed * 1000),
    }

review = "배송이 빠르긴 했는데 포장이 엉망이었어요."

# Zero-shot
zero_shot = measure_call(
    "zero-shot",
    messages=[{
        "role": "user",
        "content": f"다음 리뷰를 긍정/부정/중립으로 분류하라.\n리뷰: {review}"
    }]
)

# Few-shot
few_shot = measure_call(
    "few-shot",
    messages=[{
        "role": "user",
        "content": f"""리뷰를 분류하라.

예시:
리뷰: "정말 좋아요!" → 긍정
리뷰: "실망입니다." → 부정
리뷰: "그냥 평범해요." → 중립

리뷰: "{review}" →"""
    }]
)

# CoT
cot = measure_call(
    "cot",
    messages=[{
        "role": "user",
        "content": f"""다음 리뷰를 단계별로 분석하여 긍정/부정/중립으로 분류하라.

리뷰: {review}

1단계: 긍정적 표현 추출
2단계: 부정적 표현 추출
3단계: 전체 감정 판단
4단계: 최종 분류"""
    }]
)

# 결과 비교
for result in [zero_shot, few_shot, cot]:
    print(f"\n[{result['strategy'].upper()}]")
    print(f"응답: {result['response'][:80]}...")
    print(f"입력 토큰: {result['input_tokens']}")
    print(f"출력 토큰: {result['output_tokens']}")
    print(f"지연: {result['latency_ms']}ms")
```

---

## Q&A

**Q. Context Window가 길수록 무조건 좋은가?**

> 길수록 더 많은 정보를 처리할 수 있지만, 비용도 증가한다.
> 또한 Context가 길어지면 LLM이 중간 정보를 놓치는 "lost in the middle" 현상이 발생한다.
> 필요한 정보만 Context에 포함하는 것이 중요하다.

**Q. Hallucination을 완전히 없앨 수 있는가?**

> 현재 기술로는 완전히 제거하기 어렵다.
> RAG로 근거 문서를 제공하고, Structured Output으로 범위를 제한하고, 검증 단계를 추가하면 대폭 줄일 수 있다.
> Agent 설계 시 "LLM이 틀릴 수 있다"는 전제로 검증 로직을 포함하라.

**Q. 어떤 모델을 선택해야 하는가?**

> 2026년 기준, 단계별로 다른 모델을 사용하는 것이 효율적이다.
> 단순 분류·라우팅은 작은 모델, 복잡한 추론·생성은 큰 모델을 사용한다.
> 비용 대비 품질 테스트를 먼저 하고 결정하라.

---

## 퀴즈

### Q1. Context Window 이해

Agent가 실행 중 "context length exceeded" 에러가 발생했다. 가장 먼저 확인해야 할 것은?

- A) LLM 모델 버전
- B) System Prompt + 대화 이력 + 현재 입력의 총 토큰 수
- C) 인터넷 연결 상태
- D) API 키 유효성

<details>
<summary>힌트</summary>
Context Window는 모든 입력의 합산이다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: B**

Context Window 초과는 입력 토큰 총합이 한계를 넘었을 때 발생한다.
System Prompt, 대화 이력, 현재 사용자 입력, RAG 검색 결과 모두 포함된다.
긴 대화 이력이나 대용량 문서가 주요 원인인 경우가 많다.

</details>

---

### Q2. 프롬프트 전략 선택

다음 시나리오에 가장 적합한 프롬프트 전략은?

> "보험 청구서 PDF를 분석하여 청구 유효성을 판단해야 한다. 판단 근거를 단계별로 설명해야 하며, 실수 허용 범위가 매우 낮다."

<details>
<summary>힌트</summary>
단계별 추론이 필요하고 정확도가 중요한 경우의 전략은?
</details>

<details>
<summary>정답 및 해설</summary>

**정답: CoT + Few-shot 조합**

- CoT: 단계별 추론 근거 명시 → 정확도 향상
- Few-shot: 올바른 판단 예시 제공 → 일관성 확보
- Structured Output 추가: 판단 결과를 JSON으로 강제하면 더욱 안정적

Zero-shot은 실수 허용 범위가 낮은 도메인에 부적합하다.

</details>

---

### Q3. Structured Output 장점

Tool Use를 활용한 Structured Output의 가장 큰 장점은?

- A) 응답 속도가 빨라진다
- B) 비용이 낮아진다
- C) 응답이 항상 지정한 스키마를 따른다
- D) Context Window가 늘어난다

<details>
<summary>힌트</summary>
Tool Use는 LLM이 특정 형식으로 응답을 강제하는 메커니즘이다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: C**

Tool Use는 LLM이 반드시 지정한 JSON Schema 형식으로 응답하도록 강제한다.
이는 일반 프롬프트보다 훨씬 안정적이다.
응답 파싱 실패율이 크게 줄어들어 Agent의 안정성이 향상된다.

</details>

---

### Q4. 비용 최적화

다음 중 LLM 호출 비용을 줄이는 데 가장 효과적인 방법은?

- A) max_tokens를 무조건 크게 설정한다
- B) 모든 작업에 동일한 최고 성능 모델을 사용한다
- C) 작업 복잡도에 맞는 모델을 선택하고 불필요한 Context를 제거한다
- D) System Prompt를 매우 상세하게 작성한다

<details>
<summary>힌트</summary>
비용 = 입력 토큰 × 단가 + 출력 토큰 × 단가
</details>

<details>
<summary>정답 및 해설</summary>

**정답: C**

비용 최적화의 핵심은 두 가지다:
1. 모델 선택: 단순 작업에 고성능 모델 불필요
2. 토큰 최소화: 불필요한 Context, 중복 프롬프트 제거

A, B, D는 모두 비용 증가 요인이다.

</details>

---

### Q5. Hallucination 완화

LLM 기반 의료 정보 서비스를 만들 때 Hallucination 위험을 가장 효과적으로 줄이는 방법은?

- A) 더 큰 모델을 사용한다
- B) 의학 문서를 Context에 포함하고 "제공된 정보 외에는 답하지 말라"고 지시한다
- C) 응답 온도(temperature)를 높인다
- D) max_tokens를 늘린다

<details>
<summary>힌트</summary>
Hallucination은 모델이 근거 없이 생성할 때 발생한다. 근거를 강제하면?
</details>

<details>
<summary>정답 및 해설</summary>

**정답: B**

RAG 방식으로 실제 의학 문서를 Context에 포함하고, 해당 문서만 근거로 사용하도록 지시하면 Hallucination을 크게 줄일 수 있다.

- A: 더 큰 모델도 Hallucination을 완전히 없애지 못한다
- C: 온도를 높이면 오히려 더 창의적(= 부정확한) 응답이 나올 수 있다
- D: max_tokens는 응답 길이만 제어한다

</details>

---

## 실습 명세

### I DO (강사 시연, 15분)

**강사가 같은 태스크에 Zero-shot, Few-shot, CoT를 적용하고 결과를 비교한다.**

1. 리뷰 분류 태스크 선택
2. 각 전략으로 프롬프트 작성 후 API 호출
3. 응답 품질, 토큰 수, 지연 시간 비교
4. 언제 어떤 전략을 선택할지 설명

---

### WE DO (강사 + 수강생 함께, 20분)

**수강생이 Structured Output 실습을 함께 진행한다.**

진행 방식:
1. 강사가 JSON Schema 정의 방법 설명
2. 수강생이 자신의 도메인에 맞는 Schema 설계
3. Tool Use 방식으로 호출 코드 작성
4. 응답 파싱 및 에러 처리 추가

체크포인트:
- Schema에 required 필드가 명시되었는가?
- 파싱 에러 처리 코드가 있는가?

---

### YOU DO (수강생 독립 실습, 25분)

**3가지 프롬프트 전략을 실제 코드로 비교 실습한다.**

제출물: `labs/prompt-strategy-comparison/src/` 폴더에 작성

요구사항:
- 동일한 분류/추출 태스크에 Zero-shot, Few-shot, CoT 각각 적용
- 각 전략의 토큰 수, 지연 시간, 응답 품질 기록
- 어떤 상황에서 어떤 전략이 적합한지 주석으로 작성
- Structured Output(JSON)으로 응답 받기 구현

정답 코드: `labs/prompt-strategy-comparison/solution/` 참고
