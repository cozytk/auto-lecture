# 실습 01: 프롬프트 전략 비교 (Zero-shot / Few-shot / CoT)

## 실습 목적

동일한 고객 문의 분류 문제에 Zero-shot, Few-shot, Chain-of-Thought 세 가지 프롬프트 전략을 적용하여
응답 품질과 비용(토큰) 차이를 직접 확인한다.

- **연관 세션**: Session 2 - LLM 동작 원리 및 프롬프트 전략 심화
- **난이도**: 기초
- **예상 소요 시간**: 30분 (I DO 5분 / WE DO 10분 / YOU DO 15분)

## 사전 준비

```bash
# 환경 변수 설정
export OPENROUTER_API_KEY="your-api-key"
export MODEL="moonshotai/kimi-k2"   # 기본값, 변경 가능

# 의존성 설치
just setup
```

---

## I DO: 시연 관찰 (약 5분)

강사가 시연하는 코드를 관찰하세요. 직접 코드를 작성하지 않아도 됩니다.

### 시연 내용

- 단순 문의("주문 취소하고 싶어요")에 3가지 전략 적용
- 복합 문의("색상 다름 → 교환 불가 시 환불")에 3가지 전략 적용
- 토큰 사용량과 결과 정확도 비교

### 시연 코드 실행

```bash
just run-i-do
```

### 관찰 포인트

- Zero-shot은 단순 문의에서 충분하다
- Few-shot은 패턴 예시로 LLM 동작을 조정한다
- CoT는 복합 조건 문의에서 추론 과정을 남기며 정확도를 높인다
- CoT는 토큰을 2~3배 더 소비한다

---

## WE DO: 함께 실습 (약 10분)

강사와 함께 단계별로 코드를 완성합니다.

### 1단계: Zero-shot 구현

`src/we-do/classify.py`의 `zero_shot_classify` 함수에서 TODO를 채웁니다:

```python
# system 메시지에 카테고리 목록을 명시한다
{"role": "system", "content": "고객 문의를 다음 카테고리 중 하나로 분류하세요: 환불, 배송, 제품문의, 기타"}
```

### 2단계: Few-shot 예시 추가

`few_shot_classify` 함수에 3개 예시 쌍(user/assistant)을 추가합니다:

```python
{"role": "user", "content": "주문한 지 일주일인데 아직 안 왔어요"},
{"role": "assistant", "content": "배송"},
```

### 3단계: CoT 프롬프트 작성

`cot_classify` 함수에 단계별 추론 지시를 작성합니다:

```python
# 1. 키워드 추출  2. 의도 파악  3. 카테고리 선택
# 응답 형식 명시: "키워드: ... / 의도: ... / 카테고리: ..."
```

### 실행 확인

```bash
just run-we-do
```

---

## YOU DO: 독립 과제 (약 15분)

아래 과제를 스스로 해결하세요. 막히면 힌트를 참고하세요.

### 과제 설명

`src/you-do/classify.py`를 완성하세요:

1. `call_llm` 함수: OpenAI client로 LLM 호출 후 `(응답 텍스트, 토큰 수)` 반환
2. `zero_shot_classify`, `few_shot_classify`, `cot_classify` 세 함수 구현
3. `extract_category`: CoT 결과에서 "카테고리:" 이후 텍스트 파싱
4. `run_comparison`: 5개 문의 × 3가지 전략 결과를 표로 출력

### 시작 방법

```bash
cd src/you-do
python classify.py
```

### 힌트

<details>
<summary>힌트 1: call_llm 구현</summary>

```python
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0,
)
content = response.choices[0].message.content
tokens = response.usage.total_tokens
return content, tokens
```
</details>

<details>
<summary>힌트 2: Few-shot 예시 선택 기준</summary>

예시의 수보다 질이 중요합니다. 경계 케이스(edge case)를 포함하세요.
예: "교환 원하지만 품절 시 환불" 같은 복합 조건 예시
</details>

<details>
<summary>힌트 3: extract_category 구현</summary>

```python
if "카테고리:" in cot_result:
    return cot_result.split("카테고리:")[-1].strip().split("\n")[0]
return cot_result.strip()
```
</details>

### 정답 확인

과제를 완료한 후 `solution/classify.py`에서 정답 코드를 확인할 수 있습니다.

```bash
just run-solution
```

---

## 검증 방법

```bash
just test
```

- 5개 문의 모두 분류 결과가 출력되는가
- Zero-shot 토큰 < Few-shot 토큰 < CoT 토큰 순서인가
- 복합 문의("색상 다름+교환 불가→환불")에서 CoT가 가장 정확한가

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| `AuthenticationError` | API 키 미설정 | `export OPENROUTER_API_KEY="..."` |
| `ModelNotFoundError` | 모델명 오류 | `export MODEL="moonshotai/kimi-k2"` |
| CoT 결과 파싱 실패 | 응답 형식이 다름 | `extract_category`에서 fallback 처리 추가 |
| 토큰 수가 0으로 표시 | `usage` 미반환 | `response.usage`가 None인 경우 처리 |
