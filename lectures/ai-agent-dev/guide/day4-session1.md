# Day 4 Session 1 — Agent 품질 평가 체계 설계

> **세션 목표**: Accuracy·Faithfulness·Robustness 세 축으로 Agent 품질을 정량·정성 측정하고, Golden Test Set과 LM-as-a-Judge를 실무에 적용한다.

---

## 1. 왜 중요한가

### Agent 품질 평가가 없으면 무슨 일이 생기나

Agent를 배포한 뒤 "잘 되는 것 같다"는 직관만 남는다.
버그가 생겨도 언제부터인지 알 수 없다.
신뢰할 수 있는 숫자 없이는 개선 방향을 잡을 수 없다.

> "측정할 수 없으면 개선할 수 없다." — Peter Drucker

**실무 사례**: 한 금융 기업이 RAG 기반 상담 Agent를 운영했다.
사용자 불만이 늘었지만 원인을 특정하지 못했다.
평가 체계를 도입한 뒤 Faithfulness 점수가 0.6임을 발견했고, 청크 크기 조정으로 0.85까지 올렸다.

---

## 2. 핵심 원리

### 2.1 품질 평가 3축

| 축 | 정의 | 측정 대상 |
|---|---|---|
| **Accuracy** | 정답과 얼마나 일치하는가 | 최종 응답 vs. 기대 응답 |
| **Faithfulness** | 출처에 근거한 응답인가 | 응답 vs. 검색된 문서 |
| **Robustness** | 입력 변형에 일관된가 | 표현 바꿔도 같은 답 나오는가 |

### 2.2 평가 유형: 정량 vs. 정성

**정량 평가**
- 자동화 가능. 빠르고 재현 가능하다.
- ROUGE, BLEU, EM(Exact Match), F1 등.
- 단점: 의미적 정확성을 놓칠 수 있다.

**정성 평가**
- 사람이 직접 판단. 신뢰도 높다.
- 비용과 시간이 많이 든다.
- LM-as-a-Judge로 부분 대체 가능.

### 2.3 평가 레벨 구조

```
Unit Level    → 단일 LLM 호출 품질
Step Level    → 하나의 Agent 스텝 (Tool 호출 포함)
Task Level    → 전체 Task 완료 여부
System Level  → 시스템 전체 비용·안전성·UX
```

레벨별로 측정 주기와 담당자가 다르다.
Unit·Step은 CI/CD에서 자동화한다.
Task·System은 주간/월간 리뷰에서 점검한다.

---

## 3. 실무 의미

### 3.1 언제 무엇을 측정하는가

**개발 단계**: Unit/Step 수준 자동화 테스트.
**스테이징**: Task 수준 Golden Test Set 통과 기준 설정.
**운영**: 실시간 Faithfulness 모니터링 + 이상 감지.

### 3.2 평가 기준 수치화 예시

```
Accuracy   ≥ 0.80  → 릴리즈 통과
Faithfulness ≥ 0.75  → RAG 파이프라인 통과
Robustness  ≥ 0.85  → Prompt 변경 후 회귀 없음
```

숫자는 도메인마다 다르다.
처음에는 현재 기준선(Baseline)을 측정하고,
팀이 합의한 목표치를 설정한다.

---

## 4. 비교: 평가 방법론

| 방법 | 자동화 | 비용 | 신뢰도 | 적합한 상황 |
|---|---|---|---|---|
| 규칙 기반 (EM/F1) | O | 낮음 | 중간 | 정형 데이터, 단답형 |
| 임베딩 유사도 | O | 낮음 | 중간 | 의미적 유사성 |
| 사람 평가 | X | 높음 | 높음 | 최종 검증 |
| LM-as-a-Judge | O | 중간 | 높음 | 서술형, 다단계 |

**LM-as-a-Judge가 주목받는 이유**:
GPT-4/Claude 급 모델이 평가자 역할을 한다.
사람 판단과 상관관계가 0.8 이상으로 높다.
비용은 사람보다 10~100배 저렴하다.

---

## 5. 주의사항

### 5.1 LM-as-a-Judge 편향

**위치 편향(Position Bias)**: 먼저 나온 응답을 선호한다.
→ 응답 순서를 무작위로 섞어 평가한다.

**자기 선호 편향(Self-preference Bias)**: 같은 모델이 생성한 응답을 선호한다.
→ 평가 모델을 생성 모델과 다르게 설정한다.

**보상 해킹**: 평가 기준에 과적합된 응답이 나온다.
→ 평가 기준을 주기적으로 변경하고, 사람이 샘플을 교차 검증한다.

### 5.2 Golden Test Set 관리

- 테스트 세트가 학습 데이터에 포함되면 측정값이 오염된다.
- 격리된 저장소에서 버전 관리한다.
- 6개월마다 새 예제를 추가하고 오래된 예제를 갱신한다.

### 5.3 지표 단일화 함정

하나의 지표만 보면 다른 영역이 악화된다.
Accuracy만 올리다 Robustness가 떨어진 사례가 많다.
반드시 복합 지표 대시보드로 관리한다.

---

## 6. 코드 예제

### 6.1 Faithfulness 자동 측정 (RAGAS 스타일)

```python
from openai import OpenAI

client = OpenAI()

def measure_faithfulness(
    question: str,
    answer: str,
    contexts: list[str]
) -> float:
    """
    LM-as-a-Judge로 Faithfulness 측정.
    contexts 내 근거 없는 주장 비율을 감점한다.
    """
    context_text = "\n---\n".join(contexts)
    prompt = f"""다음 질문에 대한 답변이 제공된 문서에만 근거하는지 평가하라.

질문: {question}

문서:
{context_text}

답변:
{answer}

평가 기준:
- 답변의 각 문장이 문서에 근거하는지 확인한다.
- 근거 있는 문장 수 / 전체 문장 수 = Faithfulness 점수
- 0.0(전혀 근거 없음) ~ 1.0(완전히 근거 있음)

JSON으로만 응답하라:
{{"score": 0.0, "reason": "이유"}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )
    import json
    result = json.loads(response.choices[0].message.content)
    return result["score"]


# 사용 예시
score = measure_faithfulness(
    question="파이썬의 GIL이란 무엇인가?",
    answer="GIL은 Global Interpreter Lock으로, 한 번에 하나의 스레드만 파이썬 바이트코드를 실행한다.",
    contexts=[
        "GIL(Global Interpreter Lock)은 CPython 구현의 뮤텍스로, 여러 네이티브 스레드가 동시에 파이썬 바이트코드를 실행하지 못하도록 막는다."
    ]
)
print(f"Faithfulness: {score:.2f}")  # 예: 0.95
```

### 6.2 Golden Test Set 구조 및 실행기

```python
import json
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class GoldenTestCase:
    id: str
    category: str  # "accuracy" | "faithfulness" | "robustness"
    input: dict
    expected_output: str
    tolerance: float = 0.8  # 합격 기준 점수
    tags: list[str] = field(default_factory=list)

@dataclass
class TestResult:
    test_id: str
    passed: bool
    score: float
    actual_output: str
    reason: str

class GoldenTestRunner:
    def __init__(self, agent_fn, judge_fn):
        self.agent = agent_fn
        self.judge = judge_fn

    def run(self, test_cases: list[GoldenTestCase]) -> dict:
        results = []
        for tc in test_cases:
            actual = self.agent(tc.input)
            score = self.judge(
                expected=tc.expected_output,
                actual=actual,
                category=tc.category
            )
            results.append(TestResult(
                test_id=tc.id,
                passed=score >= tc.tolerance,
                score=score,
                actual_output=actual,
                reason=""
            ))

        passed = sum(1 for r in results if r.passed)
        return {
            "total": len(results),
            "passed": passed,
            "pass_rate": passed / len(results),
            "results": results
        }


# Golden Test Set 파일 예시 (golden_tests.json)
SAMPLE_GOLDEN_SET = [
    {
        "id": "acc_001",
        "category": "accuracy",
        "input": {"query": "AWS S3 버킷 생성 방법"},
        "expected_output": "aws s3api create-bucket 명령어 또는 콘솔에서 버킷 이름과 리전을 지정해 생성한다.",
        "tolerance": 0.75
    },
    {
        "id": "rob_001",
        "category": "robustness",
        "input": {"query": "S3에서 버킷 만드는 법 알려줘"},  # 동의어 변형
        "expected_output": "aws s3api create-bucket 명령어 또는 콘솔에서 버킷 이름과 리전을 지정해 생성한다.",
        "tolerance": 0.75
    }
]
```

### 6.3 LM-as-a-Judge 비교 평가 (Pairwise)

```python
def pairwise_judge(
    question: str,
    response_a: str,
    response_b: str,
    criteria: str = "정확성, 간결성, 유용성"
) -> dict:
    """
    두 응답을 비교해 A/B/Tie 판정.
    위치 편향 제거를 위해 순서를 바꿔 두 번 평가한다.
    """
    def single_eval(r1, r2, label1, label2):
        prompt = f"""질문: {question}

응답 {label1}: {r1}

응답 {label2}: {r2}

평가 기준: {criteria}

어느 응답이 더 나은가? JSON으로만 응답하라:
{{"winner": "{label1} or {label2} or tie", "reason": "이유"}}"""
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )
        import json
        return json.loads(resp.choices[0].message.content)

    result1 = single_eval(response_a, response_b, "A", "B")
    result2 = single_eval(response_b, response_a, "B", "A")

    # 두 판정이 일치하면 신뢰도 높음
    if result1["winner"] == "A" and result2["winner"] == "B":
        return {"winner": "A", "confidence": "high"}
    elif result1["winner"] == "B" and result2["winner"] == "A":
        return {"winner": "B", "confidence": "high"}
    else:
        return {"winner": "tie", "confidence": "low"}
```

---

## Q&A

**Q: Accuracy와 Faithfulness의 차이는 무엇인가?**
A: Accuracy는 정답 데이터셋과의 일치도다. Faithfulness는 검색된 문서에 근거하는지 여부다. RAG 시스템에서는 둘 다 독립적으로 측정해야 한다.

**Q: Golden Test Set은 얼마나 만들어야 하는가?**
A: 최소 50건, 이상적으로는 200~500건이다. 카테고리별로 균형 있게 구성한다. 처음에는 20~30건으로 시작해 점진적으로 늘린다.

**Q: 운영 중에 실시간으로 평가하면 비용이 많이 드는가?**
A: 전수 평가는 비용이 높다. 전체 트래픽의 5~10%를 샘플링해 평가하는 방식을 권장한다. 이상 감지는 규칙 기반으로 저비용 유지한다.

**Q: 사람 평가와 LM-as-a-Judge 중 무엇을 우선해야 하는가?**
A: 초기에는 사람 평가로 기준을 잡는다. 이후 LM-as-a-Judge의 판단이 사람과 얼마나 일치하는지 calibration 후 자동화한다. 고위험 도메인(의료, 금융)은 사람 최종 검증을 유지한다.

---

## 퀴즈

**Q1. [단답형] Faithfulness 지표가 낮다는 것은 무엇을 의미하는가?**

<details>
<summary>힌트</summary>
검색된 문서와 최종 응답의 관계를 생각하라.
</details>

<details>
<summary>정답</summary>
응답이 검색된 문서에 근거하지 않고 모델이 만들어낸(환각된) 내용을 포함한다는 의미다.
</details>

---

**Q2. [객관식] LM-as-a-Judge의 위치 편향(Position Bias)을 줄이는 가장 효과적인 방법은?**

A) 평가 횟수를 늘린다
B) 응답 순서를 무작위로 바꿔 두 번 평가한다
C) 더 큰 모델을 사용한다
D) Temperature를 높인다

<details>
<summary>힌트</summary>
편향의 원인이 '순서'라면 해결책도 순서와 관련이 있다.
</details>

<details>
<summary>정답</summary>
B. 응답 A와 B를 바꿔 두 번 평가하고, 두 결과가 일치할 때만 신뢰도를 높음으로 처리한다.
</details>

---

**Q3. [OX] Golden Test Set은 모델 학습 데이터와 같은 저장소에 보관해도 된다.**

<details>
<summary>힌트</summary>
학습 데이터 오염(contamination) 문제를 생각하라.
</details>

<details>
<summary>정답</summary>
X. 학습 데이터에 포함되면 평가 결과가 오염된다. 반드시 격리된 저장소에서 관리해야 한다.
</details>

---

**Q4. [단답형] Robustness를 측정하는 방법을 한 문장으로 설명하라.**

<details>
<summary>힌트</summary>
같은 의미의 다른 표현들을 입력했을 때 어떤 결과를 기대하는가?
</details>

<details>
<summary>정답</summary>
의미적으로 동일하지만 표현이 다른 여러 입력을 넣었을 때 일관된 응답이 나오는지 비율로 측정한다.
</details>

---

**Q5. [서술형] 하나의 지표(예: Accuracy)만 최적화할 때 발생하는 문제를 설명하라.**

<details>
<summary>힌트</summary>
지표 단일화 함정(Goodhart's Law)을 생각하라.
</details>

<details>
<summary>정답</summary>
Accuracy만 최적화하면 모델이 Accuracy 기준에 과적합한 응답을 생성한다. 그 결과 Robustness가 낮아지거나(표현 변형에 취약), Faithfulness가 떨어지는(문서와 무관한 정확한 암기 응답) 현상이 발생한다. 복합 지표를 동시에 관리해야 한다.
</details>

---

## 실습 명세

### I DO — 강사 시연 (30분)

**목표**: 간단한 QA Agent에 Faithfulness 측정 파이프라인을 붙인다.

**순서**:
1. LLM 호출로 간단한 QA 응답 생성
2. `measure_faithfulness()` 함수 구현
3. 5개 테스트 케이스 실행 및 결과 확인
4. 결과 DataFrame으로 시각화

### WE DO — 함께 실습 (40분)

**목표**: Golden Test Set 10건을 설계하고 자동 평가기를 완성한다.

**단계**:
1. 팀별 도메인 선정 (고객 지원 / 기술 문서 / 사내 정책)
2. Accuracy 5건, Robustness 5건 테스트 케이스 작성
3. `GoldenTestRunner` 실행 후 pass_rate 측정
4. 결과 발표 (3분/팀)

### YOU DO — 독립 과제 (50분)

**목표**: 도메인 특화 평가 체계 설계서를 작성한다.

**요구사항**:
- 3축(Accuracy/Faithfulness/Robustness) 각 합격 기준 설정 및 근거
- Golden Test Set 20건 설계 (JSON 파일)
- LM-as-a-Judge 프롬프트 작성 및 편향 제거 전략
- 평가 주기 및 책임자 정의

**산출물**: `evaluation-design.md` + `golden_tests.json`
