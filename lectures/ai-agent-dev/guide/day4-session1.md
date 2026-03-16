# Agent 품질 평가 체계 설계

## 학습 목표
1. Accuracy, Faithfulness, Robustness 세 축으로 Agent 품질을 정의하고 측정 기준을 설계할 수 있다
2. 정량/정성 평가를 조합한 평가 파이프라인을 구축하고 Golden Test Set을 설계할 수 있다
3. LLM-as-a-Judge 패턴을 적용하여 자동화된 품질 평가 시스템을 구현할 수 있다

---

## 개념 1: Accuracy, Faithfulness, Robustness 정의

### 개념 설명

**왜 이것이 중요한가**: Agent 품질을 평가한다는 것은 전통적인 소프트웨어 테스트와 근본적으로 다른 문제이다. 전통 소프트웨어는 동일한 입력에 대해 항상 동일한 출력을 보장하므로 단위 테스트와 통합 테스트만으로 품질을 검증할 수 있다. 반면 LLM 기반 Agent는 **비결정성(non-determinism)** 이라는 본질적 특성을 가진다. 같은 질문을 두 번 해도 다른 표현으로 답변하며, temperature 설정, 모델 버전, 심지어 API 서버의 상태에 따라 출력이 달라질 수 있다. 이 비결정성 때문에 단순한 "정답 일치 여부"만으로는 Agent의 품질을 충분히 측정할 수 없다.

**핵심 원리**: Agent의 출력 품질은 주관적 판단이 개입하는 영역이 크다. "좋은 답변"이란 무엇인가? 정확하지만 너무 긴 답변, 간결하지만 핵심이 빠진 답변, 맥락에는 충실하지만 사실과 다른 답변 등 품질의 차원이 다층적이다. 게다가 Agent는 단일 추론이 아닌 **다단계 추론(multi-step reasoning)** 을 거친다. 검색 -> 분석 -> Tool 호출 -> 종합이라는 파이프라인에서 각 단계의 품질이 최종 결과에 누적적으로 영향을 미치므로, 어떤 단계가 품질 저하의 원인인지 분리하여 측정해야 한다.

- **Accuracy(정확성)**: 정답에 얼마나 가까운가를 측정한다. 최종 응답의 사실적 정확성을 Ground Truth와 비교하여 판단한다. 예를 들어 "서울 인구는 500만"이라고 답변하면 실제 ~950만과 차이가 크므로 Accuracy가 낮다.
- **Faithfulness(충실성)**: 주어진 컨텍스트에 충실한가를 측정한다. RAG Agent가 검색한 문서에 없는 내용을 생성하면 이는 할루시네이션이며, Faithfulness가 낮다는 의미이다. Accuracy가 높아도 Faithfulness가 낮으면 Agent가 문서를 무시하고 자체 지식으로 답변하고 있다는 뜻이므로, 할루시네이션 위험의 전조 증상이다.
- **Robustness(견고성)**: 입력 변형에 얼마나 안정적인가를 측정한다. 사용자는 교과서적으로 질문하지 않는다. "환불해줘"와 "돈 돌려줘"는 같은 의도이지만 표현이 다르다. Robustness가 낮은 Agent는 이 두 입력에 완전히 다른 응답을 내놓는다.

**실무에서의 의미**: 이 세 축의 관계를 이해하는 것이 핵심이다. Accuracy가 높아도 Faithfulness가 낮으면 Agent가 주어진 문서를 무시하고 자체 지식으로 답변하고 있다는 의미이다. 이는 "지금은 맞지만, 문서가 업데이트되면 틀릴 수 있다"는 위험 신호이다. 반대로 Faithfulness가 높아도 Accuracy가 낮으면 문서 자체의 품질 문제를 의심해야 한다. 실무에서는 이 세 축을 독립적으로 측정하고, 어느 축에서 문제가 발생하는지에 따라 개선 전략을 다르게 수립한다. Accuracy 문제는 프롬프트나 모델을, Faithfulness 문제는 RAG 파이프라인을, Robustness 문제는 입력 전처리를 개선하는 식이다.

**다른 접근법과의 비교**: 전통적인 NLP 평가에서는 BLEU, ROUGE 같은 토큰 겹침 지표를 사용했다. 그러나 이 지표들은 "서울특별시"와 "서울"을 다른 답변으로 취급하는 한계가 있다. 의미적 동등성을 포착하지 못하는 것이다. 3축 평가 방법론은 이러한 한계를 극복하기 위해 등장했으며, 각 축이 서로 다른 위험을 포착하기 때문에 하나라도 빠지면 품질의 사각지대가 생긴다. 특히 LLM 기반 Agent는 "그럴듯하게 보이지만 틀린 답변"을 생성하는 경향이 있으므로, Faithfulness 측정이 전통 소프트웨어에는 없는 새로운 필수 축이 된다.

이 세 축을 데이터 구조로 표현하고 평가 결과를 집계하는 기본 프레임워크를 코드로 구현하면 다음과 같다:

```python
from dataclasses import dataclass
from enum import Enum

class QualityAxis(Enum):
    ACCURACY = "accuracy"
    FAITHFULNESS = "faithfulness"
    ROBUSTNESS = "robustness"

@dataclass
class EvalResult:
    axis: QualityAxis
    score: float          # 0.0 ~ 1.0
    evidence: str         # 판단 근거
    test_case_id: str

@dataclass
class QualityReport:
    results: list[EvalResult]

    def score_by_axis(self, axis: QualityAxis) -> float:
        axis_results = [r for r in self.results if r.axis == axis]
        if not axis_results:
            return 0.0
        return sum(r.score for r in axis_results) / len(axis_results)

    def summary(self) -> dict[str, float]:
        return {axis.value: self.score_by_axis(axis) for axis in QualityAxis}
```

위 코드는 평가 결과를 축별로 독립 집계하는 구조이다. `QualityReport`의 `summary()` 메서드가 세 축의 평균 점수를 반환하므로, 어느 축에서 품질이 떨어지는지 한눈에 파악할 수 있다. 예를 들어 `{'accuracy': 0.8, 'faithfulness': 1.0, 'robustness': 0.6}`이라면 Robustness 개선이 우선 과제임을 알 수 있다.

### 예제

실제 Agent 응답을 세 축으로 평가하는 함수를 구현한다. LLM을 평가자로 활용하여 Accuracy(정답 대비)와 Faithfulness(컨텍스트 대비)를 각각 독립적으로 채점하는 방식이다.

```python
import json
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

def evaluate_response(
    query: str, agent_response: str,
    ground_truth: str, context_docs: list[str],
) -> dict[str, float]:
    """Agent 응답을 Accuracy와 Faithfulness로 평가한다."""
    prompts = {
        "accuracy": f"질문: {query}\nAgent 응답: {agent_response}\n정답: {ground_truth}\n\n정확도를 0~1로 평가. JSON: {{\"score\": 0.0~1.0, \"reason\": \"근거\"}}",
        "faithfulness": f"컨텍스트: {chr(10).join(context_docs)}\nAgent 응답: {agent_response}\n\n컨텍스트 충실도를 0~1로 평가. JSON: {{\"score\": 0.0~1.0, \"reason\": \"근거\"}}",
    }
    scores = {}
    for axis, prompt in prompts.items():
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}, temperature=0,
        )
        scores[axis] = json.loads(resp.choices[0].message.content)["score"]
    return scores
```

이 함수는 두 번의 LLM 호출로 Accuracy와 Faithfulness를 독립적으로 채점한다. 핵심은 각 축의 비교 기준이 다르다는 점이다. Accuracy는 Ground Truth와, Faithfulness는 제공된 컨텍스트 문서와 비교한다.

### Q&A

**Q: Accuracy와 Faithfulness의 차이가 명확하지 않습니다. 둘 다 "맞는 답변"을 평가하는 것 아닌가요?**

A: 핵심 차이는 비교 기준이다. Accuracy는 "정답(Ground Truth)"과 비교하고, Faithfulness는 "제공된 컨텍스트(문서)"와 비교한다. 예를 들어 RAG Agent가 검색된 문서에 없는 내용을 답변했는데 그것이 사실이라면 Accuracy는 높지만 Faithfulness는 낮다. 이 경우 할루시네이션 위험이 있는 것으로 판단한다. 반대로, 검색 문서가 오래된 정보를 담고 있어서 문서에 충실하게 답변했지만 실제 정답과 다르다면 Faithfulness는 높지만 Accuracy는 낮다.

<details>
<summary>퀴즈: Agent가 "한국의 수도는 서울이다"라고 답변했고, 검색된 문서에 이 내용이 없었다면 Accuracy와 Faithfulness는 각각 어떻게 평가되나요?</summary>

**힌트**: Accuracy는 사실 여부, Faithfulness는 컨텍스트 근거 여부를 따진다.

**정답**: Accuracy는 높다(사실이므로). Faithfulness는 낮다(검색된 문서에 근거 없이 생성했으므로). 이는 전형적인 "정확하지만 충실하지 않은" 케이스로, RAG 시스템에서는 할루시네이션으로 분류해야 한다.
</details>

---

## 개념 2: 정량/정성 평가 설계

### 개념 설명

**왜 이것이 중요한가**: Agent 평가를 설계할 때 "무엇을 자동으로 측정할 수 있고, 무엇은 사람(또는 LLM)의 판단이 필요한가"를 구분하는 것이 출발점이다. 이 구분을 잘못하면 두 가지 방향으로 실패한다. 정량 지표만으로 평가하면 "서울특별시"와 "서울"을 다른 답변으로 취급하여 성능을 과소평가한다. 반대로 정성 평가만으로는 수천 건의 평가를 반복할 수 없어 확장이 불가능하다. 실무에서 가장 효과적인 전략은 두 방식의 계층적 결합이다.

**핵심 원리**: 정량 평가와 정성 평가는 각각 고유한 강점과 한계를 가진다.

- **정량 평가(Quantitative Evaluation)** 는 수학적 공식으로 자동 계산되는 지표이다. Exact Match(완전 일치), F1 Score(토큰 겹침), Tool 호출 정확도, 응답 시간 등이 해당한다. 강점은 재현성과 비용 효율성이다. 같은 데이터에 대해 항상 같은 결과를 반환하고, 수천 건을 순식간에 처리할 수 있다. 한계는 의미적 동등성을 포착하지 못한다는 점이다.
- **정성 평가(Qualitative Evaluation)** 는 사람이나 LLM이 루브릭(Rubric, 채점 기준표)에 따라 판단하는 방식이다. 답변의 완전성, 유용성, 자연스러움, 안전성 같은 차원은 수학 공식으로 환원하기 어렵다. 사람 평가는 가장 신뢰할 수 있지만 비용이 크고 확장이 어렵다.
- 실무에서는 먼저 정량 지표로 빠르게 필터링하고(예: F1이 0.3 미만이면 자동 실패), 그 위에 정성 평가를 적용하여 미묘한 품질 차이를 포착한다.

**실무에서의 의미**: 정량과 정성의 가중치 비율은 Agent 특성에 따라 달라진다. 팩트 기반 QA Agent는 정량(Exact Match, F1) 비중을 높이고, 대화형 Agent는 정성(유용성, 자연스러움) 비중을 높인다. 초기에는 50:50으로 시작하되, 평가 데이터가 쌓이면 각 지표와 실제 사용자 만족도 간의 상관관계를 분석하여 가중치를 보정해야 한다. 비유하자면, 정량 지표는 "체온계"처럼 객관적이지만 제한적인 정보만 제공하고, 정성 평가는 "의사의 진찰"처럼 종합적이지만 비용이 높다. 체온이 정상인데도 아플 수 있고, 체온이 높아도 단순 감기일 수 있다. 둘 다 필요한 이유이다.

**다른 접근법과의 비교**: 일부 팀은 정량 지표만으로 평가를 자동화하려 시도한다. F1 Score가 높으면 배포, 낮으면 차단하는 방식이다. 이 접근은 빠르고 저렴하지만, "기능은 작동하지만 사용자가 불만족하는" 상황을 놓친다. 반대로 매번 사람 평가를 거치는 팀은 배포 주기가 느려지고 비용이 폭증한다. 가장 현실적인 접근은 CI/CD에서 정량 지표로 자동 게이트를 설정하고, 주기적으로 샘플 기반 정성 평가를 병행하는 것이다.

다음은 자동 계산이 가능한 정량 지표를 코드로 구현한 것이다:

**정량 평가 지표**

```python
from difflib import SequenceMatcher

class QuantitativeMetrics:
    """자동으로 계산 가능한 정량 지표 모음."""

    @staticmethod
    def exact_match(prediction: str, reference: str) -> float:
        return 1.0 if prediction.strip().lower() == reference.strip().lower() else 0.0

    @staticmethod
    def f1_token_score(prediction: str, reference: str) -> float:
        pred_tokens = set(prediction.lower().split())
        ref_tokens = set(reference.lower().split())
        if not pred_tokens or not ref_tokens:
            return 0.0
        common = pred_tokens & ref_tokens
        if not common:
            return 0.0
        precision = len(common) / len(pred_tokens)
        recall = len(common) / len(ref_tokens)
        return 2 * precision * recall / (precision + recall)

    @staticmethod
    def tool_call_accuracy(predicted_tools: list[str], expected_tools: list[str]) -> float:
        if not expected_tools:
            return 1.0 if not predicted_tools else 0.0
        return SequenceMatcher(None, predicted_tools, expected_tools).ratio()

    @staticmethod
    def latency_score(response_time_ms: float, threshold_ms: float = 3000) -> float:
        if response_time_ms <= threshold_ms:
            return 1.0
        return max(0.0, 1.0 - (response_time_ms - threshold_ms) / threshold_ms)
```

각 메서드는 0.0~1.0 사이의 점수를 반환한다. `exact_match`는 완전 일치 여부만 판단하므로 가장 엄격하고, `f1_token_score`는 토큰 단위 겹침을 측정하므로 부분 일치도 포착한다. `tool_call_accuracy`는 Agent가 올바른 Tool을 올바른 순서로 호출했는지를 시퀀스 유사도로 판단한다.

**정성 평가 루브릭**

정성 평가는 사람 또는 LLM이 루브릭(Rubric)에 따라 채점한다. 루브릭은 각 평가 기준에 대해 척도, 가중치, 구체적 설명을 포함하여 평가자 간의 일관성을 확보하는 도구이다.

```python
from dataclasses import dataclass

@dataclass
class RubricItem:
    criterion: str
    description: str
    weight: float
    scale: tuple[int, int]  # (min_score, max_score)

AGENT_QUALITY_RUBRIC = [
    RubricItem("완전성", "사용자 질문의 모든 부분에 답변했는가", 0.3, (1, 5)),
    RubricItem("정확성", "제공된 정보가 사실적으로 정확한가", 0.3, (1, 5)),
    RubricItem("유용성", "실제 사용자의 문제 해결에 도움이 되는가", 0.25, (1, 5)),
    RubricItem("안전성", "유해하거나 부적절한 내용이 없는가", 0.15, (1, 5)),
]

def compute_rubric_score(ratings: dict[str, int], rubric: list[RubricItem]) -> float:
    """루브릭 기반 가중 평균 점수를 계산한다."""
    total = 0.0
    for item in rubric:
        raw = ratings.get(item.criterion, item.scale[0])
        normalized = (raw - item.scale[0]) / (item.scale[1] - item.scale[0])
        total += normalized * item.weight
    return round(total, 3)
```

루브릭은 네 가지 기준(완전성, 정확성, 유용성, 안전성)에 가중치를 부여하여 종합 점수를 산출한다. 예를 들어 `{"완전성": 4, "정확성": 5, "유용성": 4, "안전성": 5}`라면 `compute_rubric_score`는 0.856을 반환한다.

### 예제

정량/정성 평가를 결합한 종합 평가 파이프라인을 구현한다.

```python
@dataclass
class EvalCase:
    case_id: str
    query: str
    expected_answer: str
    expected_tools: list[str]
    context_docs: list[str]

@dataclass
class AgentOutput:
    response: str
    tools_called: list[str]
    latency_ms: float

def run_combined_evaluation(case: EvalCase, output: AgentOutput, rubric_ratings: dict[str, int]) -> dict:
    """정량 + 정성 결합 평가. 정량 60% + 정성 40% 가중 합산."""
    metrics = QuantitativeMetrics()
    quantitative = {
        "f1_score": metrics.f1_token_score(output.response, case.expected_answer),
        "tool_accuracy": metrics.tool_call_accuracy(output.tools_called, case.expected_tools),
        "latency_score": metrics.latency_score(output.latency_ms),
    }
    qualitative = {"rubric_score": compute_rubric_score(rubric_ratings, AGENT_QUALITY_RUBRIC)}
    quant_avg = sum(quantitative.values()) / len(quantitative)
    combined = 0.6 * quant_avg + 0.4 * qualitative["rubric_score"]
    return {"case_id": case.case_id, "quantitative": quantitative, "qualitative": qualitative, "combined_score": round(combined, 3)}
```

이 파이프라인은 정량 지표(F1, Tool 정확도, 응답 시간)와 정성 지표(루브릭 점수)를 60:40으로 결합하여 단일 종합 점수를 산출한다. 정량만으로는 놓치는 품질 차이를, 정성만으로는 확보할 수 없는 재현성을 동시에 달성하는 구조이다.

### Q&A

**Q: 정량 평가와 정성 평가의 비율을 60:40으로 설정한 이유가 있나요?**

A: 절대적인 정답은 없다. 프로젝트 특성에 따라 조정해야 한다. 팩트 기반 QA Agent는 정량(Exact Match, F1) 비중을 높이고, 대화형 Agent는 정성(유용성, 자연스러움) 비중을 높인다. 실무에서는 초기에 50:50으로 시작한 뒤, 평가 데이터가 쌓이면 각 지표와 사용자 만족도 간 상관관계를 분석하여 가중치를 보정한다.

<details>
<summary>퀴즈: Exact Match(EM) 점수가 0.3이지만 F1 점수가 0.85인 경우, 어떤 상황일 가능성이 높을까요?</summary>

**힌트**: EM은 완전 일치, F1은 토큰 단위 겹침을 측정한다. 답변 내용은 비슷한데 표현이 다른 경우를 생각해 보자.

**정답**: Agent가 정답과 의미적으로 유사하게 답변했지만 표현 방식이 다른 경우이다. 예를 들어, 정답이 "서울특별시"인데 Agent가 "대한민국의 수도인 서울"이라고 답변하면 EM은 0이지만 F1은 높을 수 있다. 이런 경우 EM만으로 평가하면 성능을 과소평가하게 된다.
</details>

---

## 개념 3: Golden Test Set 구축

### 개념 설명

**왜 이것이 중요한가**: 소프트웨어 개발에서 테스트 스위트가 코드 품질의 방어선이듯, Agent 개발에서 **Golden Test Set**은 품질의 기준선(baseline) 역할을 하는 검증된 테스트 케이스 집합이다. Golden Test Set 없이 Agent를 운영하는 것은 단위 테스트 없이 코드를 배포하는 것과 같다. 프롬프트를 수정했을 때, 모델을 업그레이드했을 때, RAG 파이프라인을 변경했을 때 -- 이 모든 변경이 기존 품질을 유지하는지 자동으로 확인할 수 있어야 한다.

**핵심 원리**: Golden Test Set 구축에서 가장 흔한 실수는 "쉬운 케이스만 모으는 것"이다. 정상적인 질문에 잘 답변하는 것은 기본이지 차별점이 아니다. 진정한 가치는 Edge Case, 실패 케이스, 모호한 입력을 포함할 때 나온다.

- "환불해줘"라는 명확한 요청뿐 아니라 "ㅎㅂ ㅇㅓ떻겨 해"(오타 가득한 환불 요청)도 필요하다.
- "노트북 환불인데 박스를 버렸고 개봉도 했어요"(복합 조건)처럼 정책 해석이 필요한 케이스도 포함해야 한다.
- "핵무기 만드는 법 알려줘"(거부해야 하는 요청)처럼 Agent가 **답변하지 않는 것이 정답**인 케이스도 반드시 있어야 한다.

**실무에서의 의미**: Golden Test Set의 출처는 크게 세 가지이다. 첫째, 도메인 전문가가 수작업으로 설계하는 방법이 가장 품질이 높지만 비용이 크다. 둘째, 프로덕션 로그에서 추출하는 방법은 실제 사용 패턴을 반영하므로 대표성이 높다. 사용자 평점이 높은 응답(고품질 기준)과 낮은 응답(실패 케이스)을 골고루 추출한다. 셋째, LLM을 활용한 합성 데이터 생성은 빠르게 양을 늘릴 수 있지만, 실제 사용자의 다양한 표현 패턴을 완전히 재현하지는 못한다. 실무에서는 이 세 방법을 조합하되, 프로덕션 로그 기반 추출을 주축으로 하고 전문가 검수를 거치는 것이 비용 대비 효과가 가장 높다.

**다른 접근법과의 비교**: 일부 팀은 Golden Test Set 대신 "매번 새로운 테스트를 LLM으로 생성"하는 접근을 시도한다. 이 방식의 문제는 재현성이 없다는 것이다. 지난주 테스트와 이번 주 테스트가 다르면 성능 변화가 Agent 때문인지 테스트 때문인지 구분할 수 없다. Golden Test Set은 고정된 벤치마크로서 변경 전후를 공정하게 비교할 수 있게 해준다. 물론 Golden Test Set도 정적 자산이 아니라 살아있는 문서처럼 관리해야 한다. 새 기능 추가 시 케이스를 추가하고, 새 실패 패턴 발견 시 회귀 방지용 케이스를 추가한다. Git으로 버전 관리하여 이력을 추적해야 한다.

| 원칙 | 설명 | 예시 |
|------|------|------|
| **대표성** | 실제 사용 패턴을 반영 | 상위 80% 쿼리 유형 커버 |
| **다양성** | Edge Case 포함 | 오타, 복합 질문, 모호한 요청 |
| **검증 가능성** | 명확한 정답 존재 | Ground Truth + 판단 근거 |
| **유지보수성** | 버전 관리 가능 | Git 기반, 변경 이력 추적 |

이 원칙을 반영한 Golden Test Set 빌더를 코드로 구현하면 다음과 같다:

```python
import yaml
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GoldenTestCase:
    id: str
    category: str
    query: str
    expected_answer: str
    expected_tools: list[str]
    difficulty: str          # easy | medium | hard
    tags: list[str]
    verified_by: str

class GoldenTestSetBuilder:
    """Golden Test Set을 체계적으로 구축하는 빌더."""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.cases: list[GoldenTestCase] = []
        self._id_counter = 0

    def add_case(self, category: str, query: str, expected_answer: str,
                 expected_tools: list[str] | None = None,
                 difficulty: str = "medium", tags: list[str] | None = None,
                 verified_by: str = "auto") -> "GoldenTestSetBuilder":
        self._id_counter += 1
        self.cases.append(GoldenTestCase(
            id=f"gt-{self._id_counter:04d}", category=category, query=query,
            expected_answer=expected_answer, expected_tools=expected_tools or [],
            difficulty=difficulty, tags=tags or [], verified_by=verified_by,
        ))
        return self

    def coverage_report(self) -> dict:
        categories = {}
        difficulties = {}
        for case in self.cases:
            categories[case.category] = categories.get(case.category, 0) + 1
            difficulties[case.difficulty] = difficulties.get(case.difficulty, 0) + 1
        return {"total": len(self.cases), "by_category": categories, "by_difficulty": difficulties}
```

`GoldenTestSetBuilder`는 빌더 패턴으로 테스트 케이스를 체이닝하여 추가할 수 있다. `coverage_report()`는 카테고리별, 난이도별 분포를 반환하여 테스트 세트의 균형을 점검할 수 있게 해준다. 특정 카테고리에 케이스가 편중되어 있으면 누락된 영역을 식별하여 보강한다.

### 예제

프로덕션 로그에서 Golden Test Set 후보를 자동 추출하는 파이프라인을 구현한다.

```python
import random

@dataclass
class ProductionLog:
    query: str
    response: str
    tools_called: list[str]
    user_rating: int | None    # 1~5, None이면 미평가
    category: str

def extract_golden_candidates(
    logs: list[ProductionLog], min_rating: int = 4, sample_per_category: int = 5,
) -> list[ProductionLog]:
    """고품질 응답 + 실패 케이스를 카테고리별 균등 샘플링."""
    high_quality = [log for log in logs if log.user_rating and log.user_rating >= min_rating]
    by_category: dict[str, list[ProductionLog]] = {}
    for log in high_quality:
        by_category.setdefault(log.category, []).append(log)

    candidates = []
    for cat_logs in by_category.values():
        candidates.extend(random.sample(cat_logs, min(sample_per_category, len(cat_logs))))

    # 실패 케이스도 포함 (Robustness 테스트용)
    failures = [log for log in logs if log.user_rating and log.user_rating <= 1]
    candidates.extend(random.sample(failures, min(3, len(failures))))
    return candidates
```

이 함수는 고품질 응답(평점 4점 이상)을 카테고리별로 균등 샘플링하고, 실패 케이스(평점 1점 이하)도 포함하여 Golden Test Set의 대표성과 다양성을 동시에 확보한다. 실패 케이스를 포함하는 이유는 Agent가 답변할 수 없는 질문에 대해 적절히 거부하는지 검증하기 위해서이다.

### Q&A

**Q: Golden Test Set은 얼마나 자주 업데이트해야 하나요?**

A: 최소 2주마다 검토하고, 다음 이벤트 발생 시 즉시 업데이트한다: (1) 새로운 기능/Tool 추가, (2) 프로덕션에서 발견된 새로운 실패 패턴, (3) 도메인 지식 변경(정책 변경 등). 실무에서는 CI/CD 파이프라인에 Golden Test 실행을 포함시켜 배포 전 자동 검증한다.

<details>
<summary>퀴즈: Golden Test Set에 "실패 케이스"를 포함해야 하는 이유는 무엇인가요?</summary>

**힌트**: Agent가 "모르겠습니다"라고 답해야 하는 상황도 정답이 될 수 있다.

**정답**: 실패 케이스를 포함하는 이유는 두 가지이다. 첫째, Agent가 답변할 수 없는 질문에 대해 적절히 거부하거나 에스컬레이션하는지 검증한다(Robustness). 둘째, 과거에 발생한 실패를 회귀 테스트로 활용하여 동일한 실패가 재발하지 않는지 확인한다. "이 질문에는 답변할 수 없습니다"가 올바른 expected_answer인 테스트 케이스가 반드시 있어야 한다.
</details>

---

## 개념 4: LLM-as-a-Judge 적용 기준

### 개념 설명

**왜 이것이 중요한가**: LLM 기반 Agent의 평가 방법론은 빠르게 진화해 왔다. 초기에는 BLEU, ROUGE 같은 NLP 전통 지표가 사용되었지만, 이 지표들은 표면적 토큰 겹침만 측정할 뿐 의미적 품질을 포착하지 못했다. 이후 사람 평가(Human Evaluation)가 골드 스탠다드로 자리잡았지만, 평가자 모집 비용, 평가자 간 일치도(Inter-Annotator Agreement) 확보, 확장성 문제가 심각했다. 100건의 평가에도 수십만 원의 비용과 수일의 시간이 소요되는 상황에서, 모델 업데이트마다 수천 건의 평가를 반복하기란 현실적으로 불가능하다.

**핵심 원리**: LLM-as-a-Judge는 이 확장성 문제의 돌파구로 등장한 패턴이다. 핵심 아이디어는 "충분히 강력한 LLM이라면 사람 평가자의 판단을 상당 수준으로 대체할 수 있다"는 것이다. 실제로 GPT-4 수준의 모델이 내린 품질 판단은 사람 평가자 간의 일치도와 비슷한 수준의 상관관계를 보인다는 연구 결과가 여럿 발표되었다(MT-Bench, Chatbot Arena 등).

- LLM-as-a-Judge가 **잘 작동하는 영역**: 응답의 논리적 일관성, 유창성, 완전성, 할루시네이션 탐지 등 언어적 판단이 필요한 정성 평가에서 특히 효과적이다.
- LLM-as-a-Judge가 **부적합한 영역**: 도메인 전문 지식의 정확도(의료 진단, 법률 해석), 수치 계산의 정확도, 최신 정보 기반의 팩트 체크 등에서는 LLM 자체의 지식 한계 때문에 신뢰하기 어렵다.

**실무에서의 의미**: LLM-as-a-Judge를 실무에 적용할 때 반드시 인지해야 할 편향(bias)이 있다. 가장 잘 알려진 것이 **Position Bias**로, 두 응답을 비교할 때 첫 번째로 제시된 응답을 체계적으로 선호하는 경향이다. 또한 **Verbosity Bias**(더 긴 응답을 더 좋게 평가), **Self-Enhancement Bias**(자신과 같은 모델의 출력을 과대평가), **Authority Bias**("연구에 따르면" 같은 권위 표현 선호) 등이 있다. 이러한 편향을 완화하지 않으면 평가 결과를 신뢰할 수 없다.

**다른 접근법과의 비교**: Position Bias는 순서를 바꿔 두 번 평가하는 방식으로 완화한다. Verbosity Bias는 루브릭에 "간결성" 기준을 추가하여 완화한다. Self-Enhancement Bias는 교차 모델 평가(Agent가 Claude면 GPT로 평가, 또는 그 반대)로 대응한다. 이러한 편향 완화 기법 없이 LLM-as-a-Judge를 사용하면, 단순히 "긴 답변을 선호하는 자동 시스템"에 불과해진다. 비유하자면, 심사위원이 항상 첫 번째 참가자에게 높은 점수를 주는 경향이 있다면, 참가 순서를 바꿔서 두 번 심사하고 평균을 내야 공정한 것과 같다.

| 적합한 경우 | 부적합한 경우 |
|------------|-------------|
| 응답 품질(유창성, 논리성) 평가 | 도메인 전문 지식 정확도 검증 |
| 대량 데이터 자동 채점 | 법적/의료적 판단이 필요한 평가 |
| A/B 비교 평가 | 수치 계산 정확도 |
| 할루시네이션 탐지 | 최신 정보 기반 팩트 체크 |

이러한 원칙을 반영한 LLM-as-a-Judge 시스템을 코드로 구현하면 다음과 같다:

```python
import json
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

class LLMJudge:
    """LLM을 활용한 자동 평가 시스템."""

    def __init__(self, model: str = MODEL):
        self.model = model

    def pairwise_compare(self, query: str, response_a: str, response_b: str) -> dict:
        """두 응답을 비교하여 더 나은 응답을 선택한다."""
        prompt = f"""AI Agent 응답 품질 평가자로서 두 응답을 비교하세요.

질문: {query}
응답 A: {response_a}
응답 B: {response_b}

평가 기준: 정확성, 완전성, 유용성, 간결성
JSON: {{"winner": "A"/"B"/"tie", "scores": {{"A": 1~10, "B": 1~10}}, "reasoning": "근거"}}"""
        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}, temperature=0,
        )
        return json.loads(resp.choices[0].message.content)

    def detect_hallucination(self, context: str, response: str) -> dict:
        """응답에서 할루시네이션을 탐지한다."""
        prompt = f"""컨텍스트만을 기준으로 할루시네이션을 분석하세요.

컨텍스트: {context}
응답: {response}

JSON: {{"claims": [{{"claim": "내용", "supported": true/false, "evidence": "근거"}}], "hallucination_score": 0.0~1.0}}"""
        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}, temperature=0,
        )
        return json.loads(resp.choices[0].message.content)
```

`LLMJudge`는 두 가지 핵심 기능을 제공한다. `pairwise_compare`는 두 응답을 4가지 기준으로 비교하여 승자를 결정하고, `detect_hallucination`은 응답의 각 주장(claim)을 컨텍스트와 대조하여 할루시네이션을 claim 단위로 분석한다.

**Position Bias 완화 전략**

LLM-as-a-Judge의 대표적 편향을 완화하려면 순서를 바꿔 두 번 평가한다.

```python
def unbiased_pairwise_compare(judge: LLMJudge, query: str, resp_a: str, resp_b: str) -> dict:
    """Position Bias를 완화한 쌍대 비교."""
    result_ab = judge.pairwise_compare(query, resp_a, resp_b)
    result_ba = judge.pairwise_compare(query, resp_b, resp_a)

    swap_winner = {"A": "B", "B": "A", "tie": "tie"}
    ba_winner = swap_winner[result_ba["winner"]]

    if result_ab["winner"] == ba_winner:
        return {"winner": result_ab["winner"], "confidence": "high",
                "avg_scores": {k: (result_ab["scores"][k] + result_ba["scores"][{"A":"B","B":"A"}[k]]) / 2 for k in "AB"}}
    return {"winner": "tie", "confidence": "low",
            "avg_scores": {"A": (result_ab["scores"]["A"] + result_ba["scores"]["B"]) / 2,
                           "B": (result_ab["scores"]["B"] + result_ba["scores"]["A"]) / 2}}
```

양쪽 순서에서 동일한 승자가 나오면 높은 확신으로 확정하고, 결과가 불일치하면 tie로 처리한다. 이 방식은 LLM 호출이 2배로 늘어나지만, Position Bias로 인한 잘못된 판단을 효과적으로 방지한다.

### 예제

LLM-as-a-Judge를 활용한 자동 회귀 테스트 파이프라인을 구현한다.

```python
@dataclass
class RegressionResult:
    case_id: str
    previous_score: float
    current_score: float
    degraded: bool

def run_regression_test(
    judge: LLMJudge, golden_set: list[GoldenTestCase],
    agent_fn, previous_scores: dict[str, float], threshold: float = 0.1,
) -> list[RegressionResult]:
    """이전 점수 대비 threshold 이상 하락하면 degraded로 판정."""
    results = []
    rubric = [item.__dict__ for item in AGENT_QUALITY_RUBRIC]
    for case in golden_set:
        response = agent_fn(case.query)
        eval_result = judge.evaluate_with_rubric(case.query, response, rubric)
        current = eval_result.get("total_weighted_score", 0)
        prev = previous_scores.get(case.id, current)
        results.append(RegressionResult(case.id, prev, current, (prev - current) > threshold))

    degraded_count = sum(1 for r in results if r.degraded)
    print(f"회귀 테스트 완료: {len(results)}건 중 {degraded_count}건 성능 하락 감지")
    return results
```

이 함수는 Golden Test Set의 각 케이스를 Agent에 실행하고, LLM Judge로 채점한 뒤, 이전 점수 대비 하락 여부를 판정한다. CI/CD 파이프라인에서 이 함수를 호출하면, 프롬프트 변경이나 모델 업데이트가 기존 품질을 저하시키는지 자동으로 확인할 수 있다.

### Q&A

**Q: LLM-as-a-Judge에서 평가용 모델과 Agent 모델이 같아도 되나요?**

A: 가능하지만 권장하지 않는다. 같은 모델은 자신의 출력을 과대평가하는 Self-Enhancement Bias가 있다. 실무에서는 (1) Agent보다 상위 모델로 평가(GPT-4o Agent를 GPT-4o로 평가), (2) 다른 계열 모델로 교차 평가(Claude Agent를 GPT-4o로 평가), (3) 여러 Judge 모델의 합의(Majority Voting)를 활용한다. 예산이 제한적이면 최소한 temperature=0으로 고정하고 Position Bias 완화를 적용한다.

<details>
<summary>퀴즈: LLM-as-a-Judge에서 Position Bias 외에 주의해야 할 편향은 무엇이 있나요?</summary>

**힌트**: LLM이 "더 길고 화려한 답변"을 선호하는 경향을 떠올려 보자.

**정답**: 대표적으로 세 가지가 있다. (1) **Verbosity Bias**: 더 긴 응답을 더 좋게 평가하는 경향. 간결하지만 정확한 답변이 저평가될 수 있다. (2) **Self-Enhancement Bias**: 자신(같은 모델)이 생성한 응답을 더 높게 평가. (3) **Authority Bias**: "연구에 따르면", "전문가에 의하면" 같은 권위 표현이 포함된 응답을 선호. 이를 완화하려면 루브릭에 "간결성" 기준을 포함하고, 교차 모델 평가를 적용한다.
</details>

---

## 실습

### 실습 1: Agent 평가 기준 설계 및 Golden Test Set 구축
- **연관 학습 목표**: 학습 목표 1, 2
- **실습 목적**: 실제 Agent 시나리오에 맞는 3축 평가 기준을 설계하고, 체계적인 Golden Test Set을 구축한다
- **실습 유형**: 코드 작성
- **난이도**: 중급
- **예상 소요 시간**: 40분
- **선행 조건**: Python 기본, dataclass 이해
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

#### 실습 요구사항

1. **평가 기준 설계 (15분)**
   - "여행 추천 Agent"를 대상으로 Accuracy, Faithfulness, Robustness 각 축의 구체적인 측정 기준을 정의하라
   - 각 축별 최소 3개의 평가 항목을 작성하라
   - `EvalCriteria` 데이터클래스를 설계하고 구현하라

2. **Golden Test Set 구축 (15분)**
   - `GoldenTestSetBuilder`를 활용하여 최소 10개의 테스트 케이스를 작성하라
   - 카테고리 3개 이상, 난이도 분포(easy 3, medium 5, hard 2) 포함
   - 실패 케이스(Agent가 거부해야 하는 질문) 최소 2개 포함
   - YAML 파일로 저장하라

3. **커버리지 분석 (10분)**
   - `coverage_report()`로 카테고리/난이도 분포를 확인하라
   - 누락된 시나리오가 있다면 식별하고 추가하라

#### 기대 산출물
```
travel_agent_eval/
  eval_criteria.py       # 평가 기준 정의
  golden_test_set.yaml   # 테스트 케이스 10건+
  coverage_report.py     # 커버리지 분석 스크립트
```

---

### 실습 2: LLM-as-a-Judge 자동 평가 파이프라인 구축
- **연관 학습 목표**: 학습 목표 2, 3
- **실습 목적**: LLM-as-a-Judge 패턴을 적용하여 Agent 응답을 자동으로 평가하는 파이프라인을 구현한다
- **실습 유형**: 코드 작성
- **난이도**: 심화
- **예상 소요 시간**: 50분
- **선행 조건**: 실습 1 완료, OpenAI API 키 설정
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

#### 실습 요구사항

1. **LLM Judge 구현 (20분)**
   - `LLMJudge` 클래스를 구현하되, 실습 1에서 설계한 루브릭을 적용하라
   - `evaluate_with_rubric()` 메서드로 단일 응답 채점
   - `pairwise_compare()` 메서드로 두 응답 비교
   - Position Bias 완화를 위한 `unbiased_pairwise_compare()` 구현

2. **할루시네이션 탐지 (15분)**
   - `detect_hallucination()` 메서드 구현
   - 테스트: 컨텍스트에 있는 정보만 답변한 경우 vs 없는 정보를 추가한 경우
   - 탐지 결과를 claim 단위로 분석

3. **회귀 테스트 파이프라인 (15분)**
   - 실습 1의 Golden Test Set을 입력으로 회귀 테스트 실행
   - 이전 버전 대비 성능 하락 케이스 자동 탐지
   - 결과 리포트를 JSON으로 저장

#### 기대 산출물
```
travel_agent_eval/
  llm_judge.py           # LLM Judge 구현
  hallucination_test.py  # 할루시네이션 탐지 테스트
  regression_runner.py   # 회귀 테스트 실행기
  regression_report.json # 테스트 결과 리포트
```

---

## 핵심 정리
- Agent 품질은 **Accuracy**(정확성), **Faithfulness**(충실성), **Robustness**(견고성) 세 축으로 독립 평가한다
- **정량 평가**(EM, F1, Tool 정확도)와 **정성 평가**(루브릭 채점)를 결합해야 완전한 품질 측정이 가능하다
- **Golden Test Set**은 대표성, 다양성, 검증 가능성, 유지보수성 원칙으로 구축하고, 프로덕션 로그에서 지속적으로 보강한다
- **LLM-as-a-Judge**는 정성 평가 자동화에 효과적이나, Position Bias, Verbosity Bias 등 편향을 반드시 완화해야 한다
- 평가 체계는 CI/CD에 통합하여 배포 전 자동 회귀 테스트로 활용한다
