# Session 4: 최종 시연 및 발표 (2h)

## 학습 목표
1. MVP Agent의 핵심 가치를 5분 발표로 구조적으로 전달하고 Live Demo를 성공적으로 수행할 수 있다
2. 피어 리뷰를 통해 다른 프로젝트의 아키텍처를 평가하고 건설적 피드백을 제공할 수 있다
3. 5일간 학습한 Agent 개발 전 과정을 종합하고 프로덕션 고도화를 위한 다음 단계를 설계할 수 있다

---

## 활동 1: 발표 구성 - 5분 발표 가이드

### 설명

5분은 짧다. 10분 발표에서는 각 구간을 여유 있게 배분할 수 있지만, 5분 발표는 한 문장이라도 낭비하면 핵심을 전달하지 못한다. 5분 발표의 구조는 "문제 -> 솔루션 -> 데모 -> 결과 -> 다음 단계"의 5단계를 따른다. 각 단계에 정확히 1분씩 배분하되, 데모에 가장 많은 비중을 두고 싶다면 문제와 다음 단계를 30초로 압축하여 데모를 2분으로 확장할 수 있다.

**5분 발표 구조 (문제 -> 솔루션 -> 데모 -> 결과 -> 다음 단계)**

| 구간 | 시간 | 내용 | 핵심 질문 | 슬라이드 수 |
|------|------|------|----------|------------|
| 1. 문제 (Problem) | 45초 | Pain Point, 대상 사용자, 현재 방식의 한계 | "왜 이 Agent가 필요한가?" | 1장 |
| 2. 솔루션 (Solution) | 45초 | 아키텍처 선택 근거, 구조 다이어그램 | "어떻게 해결하는가?" | 1장 |
| 3. 데모 (Demo) | 1분 30초 | Happy Path + Edge Case 실제 시연 | "실제로 동작하는가?" | 터미널 전환 |
| 4. 결과 (Results) | 1분 | Golden Test Set 결과, 개선 전후 비교 | "얼마나 잘 동작하는가?" | 1장 |
| 5. 다음 단계 (Next) | 1분 | 한계점, 확장 계획, 배운 점 | "앞으로 어떻게 발전시킬 것인가?" | 1장 |

**5분 발표 스크립트 작성 도구**

```python
"""presentation_builder.py - 5분 발표 스크립트를 구조화한다."""


def build_presentation_script(
    project_name: str,
    pain_point: str,
    target_user: str,
    architecture: str,
    arch_reason: str,
    demo_scenarios: list[dict],
    golden_test_result: dict,
    improvements: list[dict],
    limitations: list[str],
    next_steps: list[str],
) -> str:
    """5분 발표 스크립트를 생성한다.

    각 구간의 예상 소요 시간과 핵심 메시지를 포함하여
    발표자가 시간 안에 전달할 수 있도록 구조화한다.
    """
    script = []

    # 1. 문제 정의 (45초)
    script.append("=" * 60)
    script.append("[1/5] 문제 정의 (45초)")
    script.append("=" * 60)
    script.append(f"프로젝트: {project_name}")
    script.append(f"대상 사용자: {target_user}")
    script.append(f"Pain Point: {pain_point}")
    script.append("")
    script.append("--- 스크립트 ---")
    script.append(f'"현재 {target_user}는 {pain_point}라는 문제를 겪고 있습니다.')
    script.append(f' 이 Agent는 이 문제를 해결하기 위해 만들어졌습니다."')
    script.append("")

    # 2. 솔루션 (45초)
    script.append("=" * 60)
    script.append("[2/5] 솔루션 - 아키텍처 (45초)")
    script.append("=" * 60)
    script.append(f"아키텍처: {architecture}")
    script.append(f"선택 근거: {arch_reason}")
    script.append("")
    script.append("--- 스크립트 ---")
    script.append(f'"이 문제의 핵심은 [X]이기 때문에 {architecture} 구조를 선택했습니다.')
    script.append(f' {arch_reason}"')
    script.append("")

    # 3. 데모 (1분 30초)
    script.append("=" * 60)
    script.append("[3/5] Live Demo (1분 30초)")
    script.append("=" * 60)
    for i, scenario in enumerate(demo_scenarios, 1):
        name = scenario.get("name", f"시나리오 {i}")
        query = scenario.get("query", "")
        expected = scenario.get("expected", "")
        script.append(f"  시나리오 {i}: {name}")
        script.append(f"    입력: {query}")
        script.append(f"    기대 결과: {expected}")
    script.append("")
    script.append("--- 스크립트 ---")
    script.append('"실제로 동작하는 모습을 보여드리겠습니다."')
    script.append('"[터미널 전환 후 demo_script.py 실행]"')
    script.append("")

    # 4. 결과 (1분)
    script.append("=" * 60)
    script.append("[4/5] 결과 - 평가 (1분)")
    script.append("=" * 60)
    accuracy = golden_test_result.get("accuracy", "N/A")
    faithfulness = golden_test_result.get("faithfulness", "N/A")
    latency = golden_test_result.get("avg_latency_ms", "N/A")
    script.append(f"  Accuracy: {accuracy}")
    script.append(f"  Faithfulness: {faithfulness}")
    script.append(f"  평균 응답 시간: {latency}ms")
    if improvements:
        script.append("  개선 사항:")
        for imp in improvements:
            metric = imp.get("metric", "")
            before = imp.get("before", "")
            after = imp.get("after", "")
            script.append(f"    - {metric}: {before} -> {after}")
    script.append("")

    # 5. 다음 단계 (1분)
    script.append("=" * 60)
    script.append("[5/5] 다음 단계 (1분)")
    script.append("=" * 60)
    if limitations:
        script.append("  현재 한계:")
        for lim in limitations:
            script.append(f"    - {lim}")
    if next_steps:
        script.append("  확장 계획:")
        for step in next_steps:
            script.append(f"    - {step}")
    script.append("")
    script.append("--- 스크립트 ---")
    script.append('"이상으로 발표를 마치겠습니다. 질문 있으시면 말씀해주세요."')

    return "\n".join(script)


# 사용 예시
if __name__ == "__main__":
    script = build_presentation_script(
        project_name="사내 문서 Q&A Agent",
        pain_point="사내 문서가 흩어져 있어 필요한 정보를 찾는 데 평균 15분 소요",
        target_user="신입 개발자",
        architecture="RAG",
        arch_reason="정적 문서 검색이 핵심이므로 실시간 Tool 호출보다 RAG가 적합",
        demo_scenarios=[
            {
                "name": "Happy Path - 배포 절차 질문",
                "query": "배포 절차가 어떻게 되나요?",
                "expected": "사내 문서 기반 단계별 안내",
            },
            {
                "name": "Edge Case - 범위 밖 질문",
                "query": "오늘 점심 메뉴 추천해줘",
                "expected": "범위 밖 질문 안내 + 가능한 질문 유형 제시",
            },
        ],
        golden_test_result={
            "accuracy": 0.85,
            "faithfulness": 0.90,
            "avg_latency_ms": 1200,
        },
        improvements=[
            {"metric": "Accuracy", "before": 0.70, "after": 0.85},
            {"metric": "Faithfulness", "before": 0.65, "after": 0.90},
        ],
        limitations=["멀티턴 대화 미지원", "이미지 포함 문서 처리 불가"],
        next_steps=["멀티턴 대화 지원", "문서 자동 갱신 파이프라인 구축"],
    )
    print(script)
```

```
# 실행 결과 (일부)
============================================================
[1/5] 문제 정의 (45초)
============================================================
프로젝트: 사내 문서 Q&A Agent
대상 사용자: 신입 개발자
Pain Point: 사내 문서가 흩어져 있어 필요한 정보를 찾는 데 평균 15분 소요

--- 스크립트 ---
"현재 신입 개발자는 사내 문서가 흩어져 있어 필요한 정보를 찾는 데
 평균 15분 소요라는 문제를 겪고 있습니다.
 이 Agent는 이 문제를 해결하기 위해 만들어졌습니다."

============================================================
[3/5] Live Demo (1분 30초)
============================================================
  시나리오 1: Happy Path - 배포 절차 질문
    입력: 배포 절차가 어떻게 되나요?
    기대 결과: 사내 문서 기반 단계별 안내
  시나리오 2: Edge Case - 범위 밖 질문
    입력: 오늘 점심 메뉴 추천해줘
    기대 결과: 범위 밖 질문 안내 + 가능한 질문 유형 제시
```

**5분 안에 전달해야 할 핵심 메시지 체크리스트**

| # | 핵심 메시지 | 확인 | 빠뜨리면 잃는 것 |
|---|-----------|------|-----------------|
| 1 | 이 Agent가 해결하는 구체적 문제 1개 | [ ] | 문제 적합성 20% 전체 |
| 2 | 아키텍처 선택 근거 1~2문장 | [ ] | 기술 구현 40%의 절반 |
| 3 | 동작하는 Demo (Happy Path 최소 1개) | [ ] | 데모 품질 20% 전체 |
| 4 | 정량적 평가 결과 (숫자 1개 이상) | [ ] | 기술 구현 평가 근거 |
| 5 | 한계점과 다음 단계 (솔직한 회고) | [ ] | 발표력 20%의 차별화 포인트 |

### Q&A

**Q: 5분 안에 문제 정의, 아키텍처, 데모, 결과, 다음 단계를 모두 다루는 것이 가능한가요?**

A: 가능하다. 핵심은 "각 구간에서 한 가지 메시지만 전달"하는 것이다. 문제 정의에서 Pain Point 3개를 나열하면 시간이 부족하지만, "가장 핵심적인 Pain Point 1개"를 선명하게 말하면 30초면 충분하다. 아키텍처도 "MCP를 선택한 이유 한 문장"이면 된다. 모든 세부사항을 다루려 하면 5분을 넘기지만, 각 구간의 핵심 한 문장만 준비하면 4분 30초에 끝낼 수 있다. 나머지 30초는 Q&A 전환에 쓴다.

**Q: 슬라이드 없이 발표해도 되나요?**

A: 된다. 터미널 + 마크다운 문서만으로도 효과적인 발표가 가능하다. (1) `design.md`를 화면에 띄워 문제 정의와 아키텍처를 설명하고, (2) 터미널에서 `demo_script.py`를 실행하여 Live Demo를 보여주고, (3) `report.md`를 열어 평가 결과를 설명하면 된다. 화려한 슬라이드보다 동작하는 데모가 평가에서 훨씬 높은 점수를 받는다. 다만 화면 전환이 매끄럽도록 tmux 분할 또는 탭 정리는 미리 해둔다.

<details>
<summary>퀴즈: 5분 발표에서 데모에 1분 30초(전체의 30%)를 배정하는 이유는?</summary>

**힌트**: 발표 평가 기준에서 "데모 품질"과 "기술 구현"의 배점을 확인해보자.

**정답**: "데모 품질"(20%)과 "기술 구현"(40%)의 합이 전체 배점의 60%를 차지한다. 기술 구현 점수는 "실제로 동작하는 것을 보여줘야" 받을 수 있으므로, Demo는 사실상 60% 배점에 영향을 준다. 5분 중 1분 30초(30%)를 데모에 투자하는 것은 이 60% 배점을 확보하기 위한 전략적 배분이다. 아키텍처 설명이 아무리 좋아도 Demo가 없으면 "구현하지 않은 설계"로 평가받는다. Happy Path 1개와 Edge Case 1개를 보여주면 구현 완성도와 안정성을 동시에 증명할 수 있다.
</details>

---

## 활동 2: 발표 평가 기준표와 질의응답 대응 전략

### 설명

발표 평가는 4개 항목으로 구성된다. 평가 기준을 미리 파악하면 발표 준비의 우선순위를 전략적으로 설정할 수 있다. 특히 "기술 구현"이 40%로 가장 높은 비중을 차지하므로, 동작하는 Demo 확보가 최우선이다.

**발표 평가 기준표**

| 항목 | 배점 | 평가 내용 | A등급 (90%+) | B등급 (75~89%) | C등급 (60~74%) |
|------|------|----------|-------------|---------------|---------------|
| 기술 구현 | 40% | MVP가 동작하는가? 코드 품질은? | Demo 성공 + Edge Case 처리 + Validation 구현 | Demo 성공 + Happy Path 동작 | 부분 동작 또는 Demo 불안정 |
| 문제 적합성 | 20% | 문제 정의가 명확하고 Agent가 적합한 해결책인가? | Pain Point 선명 + Before/After 대비 + 정량 목표 | Pain Point 명확 + 해결 방향 제시 | 문제 정의가 모호하거나 Agent 필요성 불충분 |
| 데모 품질 | 20% | Live Demo가 매끄럽고 설득력 있는가? | Happy Path + Edge Case + 장애 대응 시연 | Happy Path 성공 + 안정적 진행 | Demo 실행은 되나 불안정 |
| 발표력 | 20% | 구조적 전달, Trade-off 설명, 질의응답 대응 | 5단계 구조 + Trade-off 근거 + Q&A 탁월 | 구조적 발표 + Q&A 대응 가능 | 내용 전달은 되나 구조 미흡 |

**등급 기준**

| 등급 | 점수 | 기준 |
|------|------|------|
| A (Best Architecture) | 90% 이상 | 전 항목 우수, Trade-off 설명 탁월, Demo + Q&A 모두 매끄러움 |
| B | 75~89% | 대부분 항목 충족, Demo 성공, 발표 구조 명확 |
| C | 60~74% | 핵심 기능 동작, 일부 항목 미흡 |
| D | 60% 미만 | Demo 실패 또는 주요 항목 미충족 |

**항목별 점수 극대화 전략**

```python
"""scoring_strategy.py - 항목별 점수 극대화 가이드."""


SCORING_GUIDE = {
    "기술 구현 (40%)": {
        "description": "가장 높은 배점. Demo 성공이 필수.",
        "must_do": [
            "Happy Path Demo 최소 1개 성공",
            "Edge Case 처리 1개 이상 시연",
            "코드에서 Input/Output Validation 존재",
            "에러 발생 시 사용자 친화적 메시지 반환",
        ],
        "bonus": [
            "LangGraph StateGraph 기반 제어 흐름",
            "Golden Test Set 기반 정량 평가 결과 제시",
            "Prompt 버전 관리 (v1 -> v2 비교)",
        ],
        "common_mistakes": [
            "Demo 없이 코드만 설명 (동작 증명 불가)",
            "모든 기능을 보여주려다 시간 초과",
            "에러 핸들링 없이 예외 발생 시 크래시",
        ],
    },
    "문제 적합성 (20%)": {
        "description": "Agent가 이 문제의 적합한 해결책인지 판단.",
        "must_do": [
            "Pain Point를 한 문장으로 명확히 정의",
            "대상 사용자를 구체적으로 특정",
            "Agent 없는 현재 방식(Before)과 Agent 도입 후(After) 대비",
        ],
        "bonus": [
            "정량적 목표 제시 (예: 검색 시간 15분 -> 30초)",
            "Day 1 문제 정의 프레임워크 활용 증거",
        ],
        "common_mistakes": [
            "문제가 너무 광범위 (모든 것을 해결하려 함)",
            "Agent가 아닌 단순 검색/스크립트로 해결 가능한 문제",
            "사용자가 누구인지 불분명",
        ],
    },
    "데모 품질 (20%)": {
        "description": "Live Demo의 안정성과 설득력.",
        "must_do": [
            "Demo 스크립트 사전 작성 (demo_script.py)",
            "최소 2회 리허설 완료",
            "백업 응답 준비 (API 실패 대비)",
        ],
        "bonus": [
            "Streaming 응답으로 실시간 출력",
            "청중의 즉석 질문 1개 실시간 처리",
            "응답 시간 실시간 표시",
        ],
        "common_mistakes": [
            "리허설 없이 즉흥 Demo (높은 실패 확률)",
            "API 키 미설정으로 Demo 시작 불가",
            "터미널 글자가 작아서 뒤에서 안 보임",
        ],
    },
    "발표력 (20%)": {
        "description": "구조적 전달 능력과 질의응답 대응.",
        "must_do": [
            "5단계 구조(문제->솔루션->데모->결과->다음 단계) 준수",
            "5분 시간 내 완료",
            "Trade-off 1개 이상 근거와 함께 설명",
        ],
        "bonus": [
            "실패한 시도를 학습 근거로 설명",
            "질문에 대해 코드/데이터 근거로 즉답",
            "Day 1~4 학습 내용과의 연결점 언급",
        ],
        "common_mistakes": [
            "시간 초과로 결과/다음 단계 생략",
            "Trade-off 없이 '다 잘 된다'고만 주장",
            "Q&A에서 '모르겠습니다'로만 응답",
        ],
    },
}


def print_scoring_guide():
    """평가 가이드를 출력한다."""
    for category, guide in SCORING_GUIDE.items():
        print(f"\n{'=' * 50}")
        print(f"  {category}")
        print(f"  {guide['description']}")
        print(f"{'=' * 50}")

        print("\n  [필수 항목]")
        for item in guide["must_do"]:
            print(f"    - {item}")

        print("\n  [가산점 항목]")
        for item in guide["bonus"]:
            print(f"    + {item}")

        print("\n  [흔한 실수]")
        for item in guide["common_mistakes"]:
            print(f"    x {item}")


if __name__ == "__main__":
    print_scoring_guide()
```

```
# 실행 결과 (일부)
==================================================
  기술 구현 (40%)
  가장 높은 배점. Demo 성공이 필수.
==================================================

  [필수 항목]
    - Happy Path Demo 최소 1개 성공
    - Edge Case 처리 1개 이상 시연
    - 코드에서 Input/Output Validation 존재
    - 에러 발생 시 사용자 친화적 메시지 반환

  [가산점 항목]
    + LangGraph StateGraph 기반 제어 흐름
    + Golden Test Set 기반 정량 평가 결과 제시
    + Prompt 버전 관리 (v1 -> v2 비교)

  [흔한 실수]
    x Demo 없이 코드만 설명 (동작 증명 불가)
    x 모든 기능을 보여주려다 시간 초과
    x 에러 핸들링 없이 예외 발생 시 크래시
```

**질의응답 대응 전략**

Q&A 시간은 5분이다. 질문에 대한 답변은 30초 이내로 핵심만 전달한다. 길게 답변하면 질문을 1~2개밖에 받지 못하고, 짧고 정확하게 답변하면 4~5개를 소화할 수 있다. 질문이 많을수록 발표력 점수가 올라간다.

**Q&A 대응 프레임워크: PREP 법칙**

| 단계 | 설명 | 예시 |
|------|------|------|
| **P**oint (결론) | 질문에 대한 답을 먼저 말한다 | "RAG를 선택한 이유는 정적 문서 검색이 핵심이기 때문입니다." |
| **R**eason (근거) | 왜 그런지 1문장으로 설명한다 | "실시간 API 호출이 필요 없고, 문서 50건을 벡터 검색하면 충분합니다." |
| **E**xample (증거) | 코드나 데이터로 뒷받침한다 | "실제로 Golden Test에서 Accuracy 0.85를 달성했습니다." |
| **P**oint (반복) | 결론을 다시 한번 요약한다 | "따라서 이 문제에는 RAG가 가장 적합했습니다." |

**예상 질문 Top 10과 대응 방향**

| # | 예상 질문 | 답변 방향 | 활용할 근거 |
|---|----------|----------|------------|
| 1 | "왜 이 아키텍처를 선택했나요?" | 문제 특성과 구조의 인과관계 | Day 1 아키텍처 판단 기준표 |
| 2 | "할루시네이션을 어떻게 방지하나요?" | Faithfulness 검증 + Prompt 제한 | Session 3 평가 결과 |
| 3 | "성능을 더 개선할 수 있는 방법은?" | 시도하지 못한 개선과 예상 효과 | Session 3 실험 기록 |
| 4 | "프로덕션에 배포하려면 뭐가 더 필요한가요?" | 운영 리스크 + 모니터링 + 확장 계획 | Day 4 운영 설계 |
| 5 | "가장 어려웠던 부분은?" | 기술적 도전과 해결 과정 | 실제 디버깅/개선 경험 |
| 6 | "다른 모델로 바꾸면 결과가 달라지나요?" | MODEL 환경변수로 교체 가능 + 예상 차이 | OpenRouter 멀티 모델 구조 |
| 7 | "비용은 얼마나 드나요?" | 토큰 사용량 기반 비용 추정 | Session 3 latency 프로파일 |
| 8 | "데이터가 바뀌면 어떻게 대응하나요?" | 재색인 전략 또는 Tool 업데이트 절차 | Day 3 RAG 파이프라인 |
| 9 | "멀티턴 대화는 어떻게 확장하나요?" | LangGraph checkpointer + 대화 히스토리 관리 | Day 2 상태 관리 |
| 10 | "이 Agent와 ChatGPT의 차이는?" | 도메인 특화 + 검증된 데이터 기반 + Tool 연동 | 프로젝트 차별점 |

**답변할 수 없는 질문에 대한 대응**

모르는 질문을 받았을 때 최악의 답변은 "모르겠습니다"이고, 차선은 "좋은 질문입니다"로 시간을 끄는 것이다. 가장 좋은 대응은 다음 패턴을 따르는 것이다.

```
# 모르는 질문 대응 패턴
1. 솔직하게 인정: "해당 부분은 이번 MVP에서는 다루지 못했습니다."
2. 관련 경험 연결: "다만 유사한 문제로 [X]를 시도한 경험이 있고,"
3. 가설 제시: "[Y] 접근법이 효과적일 것으로 예상합니다."
4. 다음 단계로 연결: "프로덕션 단계에서 검증할 계획입니다."
```

### Q&A

**Q: 질문이 공격적이거나 예상 밖일 때 어떻게 대응하나요?**

A: 공격적 질문은 대부분 "왜 이렇게 했느냐"는 의사결정 근거를 묻는 것이다. 방어하지 말고 근거를 제시한다. "좋은 지적입니다. 저도 [대안]을 검토했는데, [이유]로 현재 방식을 선택했습니다. 말씀하신 접근도 유효하며, 다음 단계에서 비교 실험해볼 가치가 있습니다." 핵심은 (1) 질문을 인정하고, (2) 근거를 제시하고, (3) 대안을 열어두는 것이다. "그건 틀렸습니다"라고 반박하면 발표력 점수가 크게 떨어진다.

<details>
<summary>퀴즈: Q&A에서 "PREP 법칙"의 핵심 이점은 무엇인가?</summary>

**힌트**: 5분이라는 Q&A 시간 제약과, 답변의 명확성을 동시에 고려해보자.

**정답**: PREP 법칙의 핵심 이점은 "결론을 먼저 말하므로 30초 안에 핵심을 전달할 수 있다"는 것이다. 일반적인 답변은 배경 설명 -> 근거 -> 결론 순서로 진행하여 1~2분이 걸리지만, PREP는 결론 -> 근거 -> 증거 -> 결론 순서로 30초 안에 완결된다. 5분 Q&A에서 PREP로 답변하면 6~8개 질문을 소화할 수 있지만, 배경부터 시작하면 2~3개밖에 못 받는다. 질문을 많이 받을수록 "폭넓은 기술 이해"를 증명하므로 발표력 점수가 올라간다.
</details>

---

## 활동 3: 피어 리뷰 체크리스트

### 설명

발표를 듣는 것도 학습이다. 다른 사람의 프로젝트를 구조적으로 평가하면 (1) 자신의 프로젝트를 객관적으로 돌아보는 시각을 얻고, (2) 다양한 아키텍처 접근법을 비교할 수 있으며, (3) 건설적 피드백을 주는 연습이 된다. 피어 리뷰는 발표 평가와 별개로, 동료 학습(Peer Learning)의 핵심 도구이다.

**피어 리뷰 체크리스트**

```python
"""peer_review.py - 피어 리뷰 체크리스트 및 피드백 생성."""
import os
import json
from dataclasses import dataclass, field
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


@dataclass
class PeerReviewItem:
    """피어 리뷰 개별 항목."""
    category: str
    question: str
    score: int = 0          # 1~5점
    comment: str = ""


@dataclass
class PeerReview:
    """피어 리뷰 전체."""
    reviewer: str
    presenter: str
    project_name: str
    items: list[PeerReviewItem] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)     # 잘한 점 (최소 2개)
    improvements: list[str] = field(default_factory=list)   # 개선 제안 (최소 1개)
    one_thing_learned: str = ""   # 이 발표에서 배운 것 1가지

    def average_score(self) -> float:
        """평균 점수를 계산한다."""
        if not self.items:
            return 0.0
        return sum(item.score for item in self.items) / len(self.items)

    def to_markdown(self) -> str:
        """피어 리뷰를 마크다운으로 변환한다."""
        lines = [
            f"# 피어 리뷰: {self.project_name}",
            f"- 리뷰어: {self.reviewer}",
            f"- 발표자: {self.presenter}",
            f"- 평균 점수: {self.average_score():.1f}/5.0",
            "",
            "## 항목별 평가",
            "",
            "| 카테고리 | 질문 | 점수 | 코멘트 |",
            "|---------|------|------|--------|",
        ]

        for item in self.items:
            stars = "+" * item.score + "-" * (5 - item.score)
            lines.append(
                f"| {item.category} | {item.question} | "
                f"{stars} ({item.score}/5) | {item.comment} |"
            )

        lines.extend([
            "",
            "## 잘한 점",
        ])
        for s in self.strengths:
            lines.append(f"- {s}")

        lines.extend([
            "",
            "## 개선 제안",
        ])
        for i in self.improvements:
            lines.append(f"- {i}")

        lines.extend([
            "",
            f"## 배운 점: {self.one_thing_learned}",
        ])

        return "\n".join(lines)


# 피어 리뷰 체크리스트 템플릿
PEER_REVIEW_TEMPLATE = [
    PeerReviewItem(
        category="문제 정의",
        question="Pain Point가 구체적이고 Agent가 적합한 해결책인가?",
    ),
    PeerReviewItem(
        category="문제 정의",
        question="대상 사용자와 사용 시나리오가 명확한가?",
    ),
    PeerReviewItem(
        category="아키텍처",
        question="MCP/RAG/Hybrid 선택 근거가 논리적인가?",
    ),
    PeerReviewItem(
        category="아키텍처",
        question="구조 다이어그램이 이해하기 쉬운가?",
    ),
    PeerReviewItem(
        category="구현",
        question="Live Demo가 성공적으로 동작했는가?",
    ),
    PeerReviewItem(
        category="구현",
        question="Edge Case나 에러 처리가 구현되어 있는가?",
    ),
    PeerReviewItem(
        category="평가",
        question="정량적 평가 결과(Golden Test Set)가 제시되었는가?",
    ),
    PeerReviewItem(
        category="평가",
        question="개선 전후 비교가 근거와 함께 설명되었는가?",
    ),
    PeerReviewItem(
        category="발표",
        question="5분 안에 핵심 메시지가 구조적으로 전달되었는가?",
    ),
    PeerReviewItem(
        category="발표",
        question="Trade-off를 근거와 함께 설명했는가?",
    ),
]


def generate_feedback_summary(reviews: list[PeerReview]) -> str:
    """여러 피어 리뷰를 종합하여 피드백 요약을 생성한다."""
    if not reviews:
        return "리뷰가 없습니다."

    all_strengths = []
    all_improvements = []
    category_scores: dict[str, list[int]] = {}

    for review in reviews:
        all_strengths.extend(review.strengths)
        all_improvements.extend(review.improvements)
        for item in review.items:
            if item.category not in category_scores:
                category_scores[item.category] = []
            category_scores[item.category].append(item.score)

    lines = [
        f"# 피어 리뷰 종합 ({len(reviews)}명)",
        "",
        "## 카테고리별 평균 점수",
        "",
        "| 카테고리 | 평균 | 응답 수 |",
        "|---------|------|--------|",
    ]

    for cat, scores in category_scores.items():
        avg = sum(scores) / len(scores)
        lines.append(f"| {cat} | {avg:.1f}/5.0 | {len(scores)} |")

    lines.extend([
        "",
        "## 공통 강점",
    ])
    for s in set(all_strengths):
        count = all_strengths.count(s)
        if count >= 2:
            lines.append(f"- {s} ({count}명 언급)")

    lines.extend([
        "",
        "## 공통 개선 제안",
    ])
    for i in set(all_improvements):
        count = all_improvements.count(i)
        if count >= 2:
            lines.append(f"- {i} ({count}명 언급)")

    return "\n".join(lines)


# 사용 예시
if __name__ == "__main__":
    # 리뷰 작성 예시
    review = PeerReview(
        reviewer="김철수",
        presenter="이영희",
        project_name="사내 문서 Q&A Agent",
        items=[
            PeerReviewItem("문제 정의", "Pain Point가 구체적인가?", 4, "신입 개발자 대상이 명확"),
            PeerReviewItem("아키텍처", "선택 근거가 논리적인가?", 5, "RAG 선택 근거 탁월"),
            PeerReviewItem("구현", "Demo가 성공했는가?", 4, "Happy Path 완벽, Edge Case 1개"),
            PeerReviewItem("발표", "구조적 전달인가?", 3, "시간 약간 초과"),
        ],
        strengths=[
            "RAG 아키텍처 선택 근거가 매우 논리적",
            "Demo에서 실시간 스트리밍 응답이 인상적",
        ],
        improvements=[
            "Edge Case 처리를 한 가지 더 보여주면 좋겠음",
        ],
        one_thing_learned="Faithfulness 평가에 LLM-as-a-Judge를 활용하는 방법",
    )

    print(review.to_markdown())
```

```
# 실행 결과
# 피어 리뷰: 사내 문서 Q&A Agent
- 리뷰어: 김철수
- 발표자: 이영희
- 평균 점수: 4.0/5.0

## 항목별 평가

| 카테고리 | 질문 | 점수 | 코멘트 |
|---------|------|------|--------|
| 문제 정의 | Pain Point가 구체적인가? | ++++- (4/5) | 신입 개발자 대상이 명확 |
| 아키텍처 | 선택 근거가 논리적인가? | +++++ (5/5) | RAG 선택 근거 탁월 |
| 구현 | Demo가 성공했는가? | ++++- (4/5) | Happy Path 완벽, Edge Case 1개 |
| 발표 | 구조적 전달인가? | +++-- (3/5) | 시간 약간 초과 |

## 잘한 점
- RAG 아키텍처 선택 근거가 매우 논리적
- Demo에서 실시간 스트리밍 응답이 인상적

## 개선 제안
- Edge Case 처리를 한 가지 더 보여주면 좋겠음

## 배운 점: Faithfulness 평가에 LLM-as-a-Judge를 활용하는 방법
```

**피어 리뷰 작성 규칙**

| # | 규칙 | 이유 |
|---|------|------|
| 1 | 잘한 점을 먼저, 최소 2개 | 건설적 피드백의 기본. 강점 인식이 동기부여가 됨 |
| 2 | 개선 제안은 구체적으로 | "더 잘했으면"이 아니라 "Edge Case를 1개 더 추가하면" |
| 3 | 점수만 주지 않기 | 점수 없이 코멘트만으로도 가치 있지만, 코멘트 없는 점수는 무의미 |
| 4 | 배운 점 1가지 반드시 작성 | 모든 발표에서 배울 점이 있다. 이것이 피어 리뷰의 핵심 |
| 5 | 비교하지 않기 | "A보다 못하다"가 아니라 "이 부분을 이렇게 하면 더 좋겠다" |

**Best Architecture 선정 기준**

Best Architecture는 단순히 점수가 가장 높은 프로젝트가 아니라, 아래 기준을 종합적으로 평가하여 선정한다.

| 기준 | 설명 | 가중치 |
|------|------|--------|
| 문제-구조 정합성 | 문제의 특성과 아키텍처 선택이 논리적으로 일관되는가 | 높음 |
| 기술적 깊이 | 단순 구현을 넘어 "왜"를 설명할 수 있는가 | 높음 |
| Trade-off 인식 | 개선의 비용을 인지하고 의사결정 근거를 제시하는가 | 중간 |
| 확장 가능성 | MVP를 넘어 프로덕션으로 발전할 수 있는 설계인가 | 중간 |
| 평가 체계 성숙도 | 정량적 평가로 품질을 측정하고 개선하는 체계가 있는가 | 중간 |

### Q&A

**Q: 피어 리뷰를 할 때 기술 수준이 달라서 제대로 평가하기 어렵습니다.**

A: 피어 리뷰의 목적은 "전문가 수준의 코드 리뷰"가 아니라 "사용자 관점의 피드백"이다. 기술적으로 깊이 평가하지 못해도, "문제 정의가 명확했는가?", "Demo가 설득력 있었는가?", "발표를 듣고 이 Agent를 사용하고 싶어졌는가?"는 누구나 판단할 수 있다. 실제 프로덕션 환경에서도 기술팀이 아닌 비즈니스 이해관계자의 피드백이 제품 방향을 결정하는 경우가 많다. "이해가 잘 안 됐다"는 피드백 자체가 "설명이 부족하다"는 의미 있는 신호이다.

<details>
<summary>퀴즈: 피어 리뷰에서 "잘한 점을 먼저 2개 이상" 적는 규칙의 목적은?</summary>

**힌트**: 심리학에서 "피드백 샌드위치(Feedback Sandwich)"라는 개념을 떠올려보자.

**정답**: 이 규칙은 피드백 수용성을 높이기 위한 것이다. 심리학 연구에 따르면 부정적 피드백을 먼저 받으면 방어적 태도가 활성화되어 이후 건설적 제안도 거부하게 된다. 반면 강점 인식 후 개선 제안을 받으면 (1) "내 노력을 알아주는 사람의 조언"으로 받아들이고, (2) 개선 동기가 높아진다. 또한 "잘한 점을 찾는 과정"에서 리뷰어 자신도 다른 접근법의 장점을 학습하게 된다. 피어 리뷰의 가장 큰 수혜자는 리뷰를 받는 사람이 아니라, 리뷰를 작성하는 사람이다.
</details>

---

## 활동 4: 과정 종합 정리 - 5일간 학습 내용 맵

### 설명

Day 5 Session 4는 과정의 마지막이다. 5일간 학습한 내용을 전체 맥락에서 조망하고, 각 Day에서 배운 것이 어떻게 연결되어 최종 MVP를 만들어냈는지 정리한다. 이 종합 정리는 단순한 복습이 아니라, "흩어진 개념들 사이의 연결고리를 발견"하는 과정이다.

**5일간 학습 흐름 맵**

```
Day 1: 왜 만드는가? (문제 정의)
  |
  |-- Session 1: Agent 문제 정의와 과제 도출
  |     "이 문제가 Agent로 풀 가치가 있는가?"
  |
  |-- Session 2: LLM 동작 원리 및 프롬프트 전략 심화
  |     "LLM이 어떻게 동작하고, 어떻게 제어하는가?"
  |
  |-- Session 3: Agent 기획서 구조화
  |     "문제 -> 솔루션 -> MVP 범위를 어떻게 정의하는가?"
  |
  |-- Session 4: MCP / RAG / Hybrid 구조 판단
  |     "이 문제에 어떤 아키텍처가 적합한가?"
  |
  v
Day 2: 어떻게 설계하는가? (아키텍처)
  |
  |-- Session 1: Agent 4요소 구조 설계
  |     "LLM + Tool + Memory + Control의 역할은?"
  |
  |-- Session 2: LangGraph 기반 제어 흐름 설계
  |     "Agent의 상태 전이를 어떻게 관리하는가?"
  |
  |-- Session 3: Tool 호출 통제 & Validation
  |     "Tool 호출을 어떻게 검증하고 제어하는가?"
  |
  |-- Session 4: 구조 리팩토링 & 확장성 설계
  |     "MVP에서 프로덕션으로 어떻게 확장하는가?"
  |
  v
Day 3: 무엇을 연결하는가? (통합)
  |
  |-- Session 1: MCP(Function Calling) 고급 설계
  |     "Tool을 어떻게 정의하고 LLM에 제공하는가?"
  |
  |-- Session 2: 외부 API / 데이터 연동 최적화
  |     "외부 시스템 연동의 안정성을 어떻게 확보하는가?"
  |
  |-- Session 3: RAG 성능을 결정하는 4가지 요소
  |     "Chunking, Embedding, Retrieval, Generation을 어떻게 최적화하는가?"
  |
  |-- Session 4: Hybrid 아키텍처 설계
  |     "MCP + RAG를 어떻게 통합하는가?"
  |
  v
Day 4: 어떻게 검증하는가? (품질)
  |
  |-- Session 1: Agent 품질 평가 체계 설계
  |     "Accuracy, Faithfulness, Robustness를 어떻게 측정하는가?"
  |
  |-- Session 2: Prompt / RAG / Tool 성능 개선 전략
  |     "병목을 어떻게 찾고 개선하는가?"
  |
  |-- Session 3: 로그 / 모니터링 / 장애 대응 설계
  |     "운영 중 문제를 어떻게 감지하고 대응하는가?"
  |
  |-- Session 4: 확장 가능한 서비스 아키텍처
  |     "단일 Agent에서 서비스로 어떻게 성장하는가?"
  |
  v
Day 5: 직접 만들어본다 (구현)
  |
  |-- Session 1: 프로젝트 설계 확정
  |     "문제 -> 아키텍처 -> MVP 범위 -> Golden Test Set"
  |
  |-- Session 2: 핵심 기능 구현
  |     "스캐폴딩 -> Agent 코어 -> Tool/RAG -> Prompt -> Validation"
  |
  |-- Session 3: 성능 개선 & 안정화
  |     "평가 -> 튜닝 -> Edge Case -> 에러 핸들링 -> 데모 준비"
  |
  |-- Session 4: 최종 시연 및 발표 <-- 현재
        "발표 -> 평가 -> 피어 리뷰 -> 종합 정리 -> 다음 단계"
```

**Day별 핵심 키워드와 MVP 연결**

| Day | 핵심 질문 | 핵심 키워드 | MVP에서의 적용 |
|-----|----------|------------|---------------|
| Day 1 | 왜 만드는가? | 문제 정의, 프롬프트 전략, 아키텍처 판단 | `design.md`의 문제 정의 + 아키텍처 선택 근거 |
| Day 2 | 어떻게 설계하는가? | Agent 4요소, LangGraph, Tool Validation | `agent.py`의 StateGraph + Tool 검증 로직 |
| Day 3 | 무엇을 연결하는가? | MCP 고급, API 연동, RAG 최적화, Hybrid | `tools.py` / `rag.py`의 외부 시스템 연동 |
| Day 4 | 어떻게 검증하는가? | Golden Test Set, 성능 개선, 모니터링, 운영 | `evaluator.py`의 평가 + `report.md`의 결과 |
| Day 5 | 직접 만들어본다 | 설계 확정, 구현, 개선, 발표 | 동작하는 MVP + 성능 리포트 + 발표 |

**"연결고리 발견" 워크시트**

아래 질문에 자신의 프로젝트를 기준으로 답해본다. 각 질문은 Day 간의 연결고리를 확인하는 것이다.

```python
"""course_reflection.py - 5일 과정 회고 워크시트."""


REFLECTION_QUESTIONS = [
    {
        "connection": "Day 1 -> Day 5",
        "question": "Day 1에서 정의한 문제가 Day 5 MVP에서 실제로 해결되었는가?",
        "follow_up": "해결되지 않았다면, 어디서 범위가 변경되었고 왜 변경했는가?",
    },
    {
        "connection": "Day 1 -> Day 2",
        "question": "Day 1에서 선택한 아키텍처(MCP/RAG/Hybrid)가 Day 2 설계에서 그대로 유지되었는가?",
        "follow_up": "변경되었다면, 설계 과정에서 어떤 새로운 제약을 발견했는가?",
    },
    {
        "connection": "Day 2 -> Day 3",
        "question": "Day 2에서 설계한 Tool/RAG 구조가 Day 3 통합에서 수정 없이 동작했는가?",
        "follow_up": "수정이 필요했다면, 설계 단계에서 무엇을 놓쳤는가?",
    },
    {
        "connection": "Day 3 -> Day 4",
        "question": "Day 3에서 구현한 통합 코드의 품질을 Day 4 평가 체계로 측정할 수 있었는가?",
        "follow_up": "측정할 수 없었다면, 평가 체계의 어떤 부분이 부족했는가?",
    },
    {
        "connection": "Day 4 -> Day 5",
        "question": "Day 4에서 학습한 성능 개선 전략을 Day 5 MVP에 적용했는가?",
        "follow_up": "적용하지 못했다면, 시간 부족인가 아니면 기술적 난이도인가?",
    },
    {
        "connection": "전체",
        "question": "5일 과정에서 가장 큰 '아하 모먼트'는 무엇이었는가?",
        "follow_up": "그 순간이 프로젝트에 어떤 영향을 주었는가?",
    },
]


def print_reflection_worksheet():
    """회고 워크시트를 출력한다."""
    print("=" * 60)
    print("  5일 과정 회고 워크시트")
    print("=" * 60)

    for i, q in enumerate(REFLECTION_QUESTIONS, 1):
        print(f"\n--- [{i}/{len(REFLECTION_QUESTIONS)}] {q['connection']} ---")
        print(f"  Q: {q['question']}")
        print(f"  Follow-up: {q['follow_up']}")
        print(f"  나의 답: ___________________________________")
        print()


if __name__ == "__main__":
    print_reflection_worksheet()
```

```
# 실행 결과 (일부)
============================================================
  5일 과정 회고 워크시트
============================================================

--- [1/6] Day 1 -> Day 5 ---
  Q: Day 1에서 정의한 문제가 Day 5 MVP에서 실제로 해결되었는가?
  Follow-up: 해결되지 않았다면, 어디서 범위가 변경되었고 왜 변경했는가?
  나의 답: ___________________________________

--- [6/6] 전체 ---
  Q: 5일 과정에서 가장 큰 '아하 모먼트'는 무엇이었는가?
  Follow-up: 그 순간이 프로젝트에 어떤 영향을 주었는가?
  나의 답: ___________________________________
```

### Q&A

**Q: 5일이라는 시간이 Agent 개발을 배우기에 충분한가요?**

A: 5일은 "Agent 개발의 전체 사이클을 한 번 경험"하기에 충분하다. 문제 정의 -> 설계 -> 구현 -> 평가 -> 발표라는 사이클을 한 번 완주하면, 이후 어떤 Agent 프로젝트든 이 프레임워크를 적용할 수 있다. 5일 과정의 가치는 "특정 기술을 깊이 배우는 것"이 아니라 "Agent 개발의 사고 프레임워크를 체득하는 것"이다. 구체적인 기술(LangGraph, RAG 최적화, 프롬프트 엔지니어링)은 프레임워크가 잡힌 후에 프로젝트를 반복하면서 자연스럽게 심화된다.

<details>
<summary>퀴즈: Day 1~5의 핵심 질문(왜/어떻게/무엇을/검증/구현)의 순서가 중요한 이유는?</summary>

**힌트**: 소프트웨어 엔지니어링에서 "요구사항 -> 설계 -> 구현 -> 테스트"의 순서와 비교해보자.

**정답**: 이 순서는 "왜(Why) -> 어떻게(How) -> 무엇(What) -> 검증(Verify) -> 구현(Build)"으로, 문제 이해 없이 설계하면 잘못된 구조를, 설계 없이 구현하면 스파게티 코드를, 검증 없이 배포하면 장애를 만든다. 특히 Agent 개발에서 이 순서가 더 중요한 이유는, LLM의 비결정적 특성 때문에 "무엇을 만들지"보다 "왜 만드는지"와 "어떻게 검증할지"가 프로젝트 성패를 결정하기 때문이다. Day 1에서 문제를 잘못 정의하면 Day 5에서 "잘 동작하지만 쓸모없는 Agent"가 만들어진다. 반대로 Day 1에서 문제를 선명하게 정의하면, Day 2~4의 모든 의사결정이 자연스럽게 정렬된다.
</details>

---

## 활동 5: 다음 단계 가이드와 MVP 완성도 체크리스트

### 설명

과정이 끝난 후가 진짜 시작이다. 5일간 만든 MVP는 "가능성 증명(Proof of Concept)"이다. 이것을 프로덕션 수준으로 발전시키려면 세 가지 방향의 고도화가 필요하다: (1) Agent 자체의 성능 고도화, (2) 프로덕션 배포를 위한 인프라 구축, (3) 지속 학습을 위한 커뮤니티와 리소스 활용.

**다음 단계 로드맵**

```python
"""next_steps.py - MVP 이후 고도화 로드맵."""
from dataclasses import dataclass


@dataclass
class RoadmapItem:
    """로드맵 항목."""
    phase: str
    title: str
    description: str
    tasks: list[str]
    timeline: str
    prerequisites: list[str]


ROADMAP = [
    # Phase 1: Agent 고도화
    RoadmapItem(
        phase="Phase 1",
        title="Agent 고도화",
        description="MVP의 핵심 기능을 강화하고 커버리지를 확장한다.",
        tasks=[
            "멀티턴 대화 지원 (LangGraph checkpointer 활용)",
            "Golden Test Set 확장 (20개 -> 50개 이상)",
            "Prompt 최적화 (A/B 테스트로 최적 버전 선택)",
            "RAG: Reranker 도입 (Cohere Rerank, Cross-Encoder)",
            "MCP: Tool 체이닝 고도화 (복합 작업 자동 분해)",
            "Structured Output 고도화 (복잡한 JSON Schema)",
            "에러 복구 자동화 (retry + fallback + graceful degradation)",
        ],
        timeline="1~2주",
        prerequisites=["Day 5 MVP 완성"],
    ),
    # Phase 2: 프로덕션 배포
    RoadmapItem(
        phase="Phase 2",
        title="프로덕션 배포",
        description="MVP를 실제 사용자가 접근할 수 있는 서비스로 전환한다.",
        tasks=[
            "API 서버 구축 (FastAPI + Uvicorn)",
            "인증/인가 (API Key 또는 OAuth2)",
            "rate limiting (사용자별 요청 제한)",
            "로깅 인프라 (구조화 로깅 + 중앙 수집)",
            "모니터링 대시보드 (Grafana / Datadog)",
            "CI/CD 파이프라인 (테스트 자동화 + 배포 자동화)",
            "Docker 컨테이너화 + Kubernetes 배포",
            "비용 관리 (일일 예산 제한 + 알림)",
        ],
        timeline="2~4주",
        prerequisites=["Phase 1 완료", "인프라 접근 권한"],
    ),
    # Phase 3: 운영 안정화
    RoadmapItem(
        phase="Phase 3",
        title="운영 안정화",
        description="프로덕션 환경에서의 안정적 운영 체계를 구축한다.",
        tasks=[
            "장애 대응 런북 작성",
            "자동 스케일링 설정",
            "A/B 테스트 프레임워크 (Prompt/모델 비교)",
            "사용자 피드백 수집 파이프라인",
            "정기 평가 자동화 (주간 Golden Test 실행)",
            "문서/데이터 자동 갱신 파이프라인",
            "보안 감사 (Prompt Injection 방어 강화)",
        ],
        timeline="4~8주",
        prerequisites=["Phase 2 완료", "실사용자 피드백"],
    ),
]


def print_roadmap():
    """로드맵을 출력한다."""
    print("=" * 60)
    print("  MVP -> 프로덕션 로드맵")
    print("=" * 60)

    for item in ROADMAP:
        print(f"\n{'─' * 60}")
        print(f"  {item.phase}: {item.title} ({item.timeline})")
        print(f"  {item.description}")
        print(f"{'─' * 60}")
        print(f"  선행 조건: {', '.join(item.prerequisites)}")
        print(f"  작업 목록:")
        for task in item.tasks:
            print(f"    [ ] {task}")


if __name__ == "__main__":
    print_roadmap()
```

```
# 실행 결과 (일부)
============================================================
  MVP -> 프로덕션 로드맵
============================================================

----------------------------------------------------------
  Phase 1: Agent 고도화 (1~2주)
  MVP의 핵심 기능을 강화하고 커버리지를 확장한다.
----------------------------------------------------------
  선행 조건: Day 5 MVP 완성
  작업 목록:
    [ ] 멀티턴 대화 지원 (LangGraph checkpointer 활용)
    [ ] Golden Test Set 확장 (20개 -> 50개 이상)
    [ ] Prompt 최적화 (A/B 테스트로 최적 버전 선택)
    [ ] RAG: Reranker 도입 (Cohere Rerank, Cross-Encoder)
    ...
```

**커뮤니티 리소스 가이드**

| 카테고리 | 리소스 | 설명 | 활용 방법 |
|---------|--------|------|----------|
| 공식 문서 | [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/) | StateGraph, 제어 흐름, 체크포인터 | Agent 고도화 시 레퍼런스 |
| 공식 문서 | [Anthropic MCP 스펙](https://modelcontextprotocol.io/) | Tool 프로토콜 표준 | MCP 서버/클라이언트 구현 |
| 공식 문서 | [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) | Tool Calling 패턴 | Tool 설계 개선 |
| 프레임워크 | [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/) | RAG 파이프라인 구축 | RAG 성능 최적화 |
| 프레임워크 | [LlamaIndex](https://docs.llamaindex.ai/) | 데이터 프레임워크 | RAG 고급 패턴 (Reranker, Hybrid Search) |
| 평가 | [RAGAS](https://docs.ragas.io/) | RAG 평가 프레임워크 | Faithfulness, Relevancy 자동 평가 |
| 평가 | [DeepEval](https://docs.confident-ai.com/) | LLM 평가 프레임워크 | Golden Test Set 자동화 |
| 배포 | [FastAPI](https://fastapi.tiangolo.com/) | API 서버 프레임워크 | Agent를 API로 서빙 |
| 모니터링 | [LangSmith](https://docs.smith.langchain.com/) | LLM 애플리케이션 관찰 도구 | 프로덕션 모니터링 + 디버깅 |
| 커뮤니티 | [LangChain Discord](https://discord.gg/langchain) | 개발자 커뮤니티 | 질문, 사례 공유, 최신 동향 |

**MVP 완성도 체크리스트**

이 체크리스트는 발표 전 최종 점검 도구이다. 모든 항목을 통과할 필요는 없지만, "필수" 항목은 반드시 확인한다.

```python
"""mvp_checklist.py - MVP 완성도 최종 점검."""
from dataclasses import dataclass


@dataclass
class ChecklistItem:
    """체크리스트 항목."""
    category: str
    item: str
    priority: str     # "필수" | "권장" | "선택"
    related_score: str  # 관련 평가 항목
    checked: bool = False


MVP_CHECKLIST = [
    # 문제 정의 (문제 적합성 20%)
    ChecklistItem(
        "문제 정의", "Pain Point가 한 문장으로 정의되어 있다",
        "필수", "문제 적합성 20%",
    ),
    ChecklistItem(
        "문제 정의", "대상 사용자가 구체적으로 특정되어 있다",
        "필수", "문제 적합성 20%",
    ),
    ChecklistItem(
        "문제 정의", "Before/After 대비가 명확하다",
        "권장", "문제 적합성 20%",
    ),

    # 아키텍처 (기술 구현 40%)
    ChecklistItem(
        "아키텍처", "MCP/RAG/Hybrid 선택 근거가 1~2문장으로 설명 가능하다",
        "필수", "기술 구현 40%",
    ),
    ChecklistItem(
        "아키텍처", "구조 다이어그램(텍스트 또는 이미지)이 있다",
        "권장", "기술 구현 40%",
    ),
    ChecklistItem(
        "아키텍처", "LangGraph StateGraph 기반 제어 흐름이 구현되어 있다",
        "권장", "기술 구현 40%",
    ),

    # 구현 (기술 구현 40%)
    ChecklistItem(
        "구현", "Agent가 Happy Path에서 정상 동작한다",
        "필수", "기술 구현 40%",
    ),
    ChecklistItem(
        "구현", "Edge Case 1개 이상 처리된다",
        "필수", "기술 구현 40%",
    ),
    ChecklistItem(
        "구현", "Input Validation이 구현되어 있다",
        "권장", "기술 구현 40%",
    ),
    ChecklistItem(
        "구현", "에러 발생 시 사용자 친화적 메시지를 반환한다",
        "권장", "기술 구현 40%",
    ),
    ChecklistItem(
        "구현", "Prompt에 버전 표시가 있다 (v1, v2 등)",
        "선택", "기술 구현 40%",
    ),

    # 평가 (기술 구현 40%)
    ChecklistItem(
        "평가", "Golden Test Set이 최소 3개 이상 정의되어 있다",
        "필수", "기술 구현 40%",
    ),
    ChecklistItem(
        "평가", "정량적 평가 결과(숫자)가 있다",
        "필수", "기술 구현 40%",
    ),
    ChecklistItem(
        "평가", "Baseline 대비 개선 결과가 있다",
        "권장", "기술 구현 40%",
    ),

    # 데모 (데모 품질 20%)
    ChecklistItem(
        "데모", "Demo 스크립트(demo_script.py)가 작성되어 있다",
        "필수", "데모 품질 20%",
    ),
    ChecklistItem(
        "데모", "최소 2회 리허설을 완료했다",
        "필수", "데모 품질 20%",
    ),
    ChecklistItem(
        "데모", "백업 응답이 준비되어 있다",
        "권장", "데모 품질 20%",
    ),
    ChecklistItem(
        "데모", "터미널 폰트 크기가 뒤에서도 읽을 수 있다",
        "권장", "데모 품질 20%",
    ),

    # 발표 (발표력 20%)
    ChecklistItem(
        "발표", "5단계 구조(문제->솔루션->데모->결과->다음 단계)로 구성했다",
        "필수", "발표력 20%",
    ),
    ChecklistItem(
        "발표", "Trade-off를 1개 이상 근거와 함께 설명할 수 있다",
        "필수", "발표력 20%",
    ),
    ChecklistItem(
        "발표", "예상 Q&A 5개 이상 답변을 준비했다",
        "권장", "발표력 20%",
    ),
    ChecklistItem(
        "발표", "5분 시간 내 발표를 완료할 수 있다 (리허설 확인)",
        "필수", "발표력 20%",
    ),
]


def run_checklist(checklist: list[ChecklistItem]) -> dict:
    """체크리스트를 실행하고 결과를 집계한다."""
    results = {
        "total": len(checklist),
        "checked": 0,
        "필수_total": 0,
        "필수_checked": 0,
        "권장_total": 0,
        "권장_checked": 0,
        "선택_total": 0,
        "선택_checked": 0,
        "by_category": {},
    }

    for item in checklist:
        results[f"{item.priority}_total"] += 1
        if item.checked:
            results["checked"] += 1
            results[f"{item.priority}_checked"] += 1

        if item.category not in results["by_category"]:
            results["by_category"][item.category] = {"total": 0, "checked": 0}
        results["by_category"][item.category]["total"] += 1
        if item.checked:
            results["by_category"][item.category]["checked"] += 1

    return results


def print_checklist(checklist: list[ChecklistItem]):
    """체크리스트를 카테고리별로 출력한다."""
    print("=" * 60)
    print("  MVP 완성도 체크리스트")
    print("=" * 60)

    current_category = ""
    for item in checklist:
        if item.category != current_category:
            current_category = item.category
            print(f"\n  [{current_category}] ({item.related_score})")

        status = "[v]" if item.checked else "[ ]"
        priority_tag = f"({item.priority})"
        print(f"    {status} {priority_tag:6s} {item.item}")

    results = run_checklist(checklist)
    print(f"\n{'─' * 60}")
    print(f"  전체: {results['checked']}/{results['total']}")
    print(f"  필수: {results['필수_checked']}/{results['필수_total']}")
    print(f"  권장: {results['권장_checked']}/{results['권장_total']}")
    print(f"  선택: {results['선택_checked']}/{results['선택_total']}")

    # 필수 미충족 항목 경고
    missing_required = [
        item for item in checklist
        if item.priority == "필수" and not item.checked
    ]
    if missing_required:
        print(f"\n  [경고] 필수 미충족 항목 {len(missing_required)}개:")
        for item in missing_required:
            print(f"    - [{item.category}] {item.item}")


if __name__ == "__main__":
    print_checklist(MVP_CHECKLIST)
```

```
# 실행 결과
============================================================
  MVP 완성도 체크리스트
============================================================

  [문제 정의] (문제 적합성 20%)
    [ ] (필수)   Pain Point가 한 문장으로 정의되어 있다
    [ ] (필수)   대상 사용자가 구체적으로 특정되어 있다
    [ ] (권장)   Before/After 대비가 명확하다

  [아키텍처] (기술 구현 40%)
    [ ] (필수)   MCP/RAG/Hybrid 선택 근거가 1~2문장으로 설명 가능하다
    [ ] (권장)   구조 다이어그램(텍스트 또는 이미지)이 있다
    [ ] (권장)   LangGraph StateGraph 기반 제어 흐름이 구현되어 있다

  [구현] (기술 구현 40%)
    [ ] (필수)   Agent가 Happy Path에서 정상 동작한다
    [ ] (필수)   Edge Case 1개 이상 처리된다
    [ ] (권장)   Input Validation이 구현되어 있다
    [ ] (권장)   에러 발생 시 사용자 친화적 메시지를 반환한다
    [ ] (선택)   Prompt에 버전 표시가 있다 (v1, v2 등)

  [평가] (기술 구현 40%)
    [ ] (필수)   Golden Test Set이 최소 3개 이상 정의되어 있다
    [ ] (필수)   정량적 평가 결과(숫자)가 있다
    [ ] (권장)   Baseline 대비 개선 결과가 있다

  [데모] (데모 품질 20%)
    [ ] (필수)   Demo 스크립트(demo_script.py)가 작성되어 있다
    [ ] (필수)   최소 2회 리허설을 완료했다
    [ ] (권장)   백업 응답이 준비되어 있다
    [ ] (권장)   터미널 폰트 크기가 뒤에서도 읽을 수 있다

  [발표] (발표력 20%)
    [ ] (필수)   5단계 구조(문제->솔루션->데모->결과->다음 단계)로 구성했다
    [ ] (필수)   Trade-off를 1개 이상 근거와 함께 설명할 수 있다
    [ ] (권장)   예상 Q&A 5개 이상 답변을 준비했다
    [ ] (필수)   5분 시간 내 발표를 완료할 수 있다 (리허설 확인)

----------------------------------------------------------
  전체: 0/22
  필수: 0/12
  권장: 0/8
  선택: 0/2

  [경고] 필수 미충족 항목 12개:
    - [문제 정의] Pain Point가 한 문장으로 정의되어 있다
    - [문제 정의] 대상 사용자가 구체적으로 특정되어 있다
    ...
```

### Q&A

**Q: MVP 완성도가 낮아도 발표를 해야 하나요?**

A: 반드시 해야 한다. 발표의 목적은 "완벽한 결과물을 자랑하는 것"이 아니라 "문제 해결 과정을 구조적으로 설명하는 것"이다. 구현이 50%만 완료되었더라도 (1) 왜 이 문제를 선택했는지, (2) 어떤 구조를 설계했는지, (3) 어디까지 구현했고 어디서 막혔는지, (4) 막힌 원인은 무엇이고 어떻게 해결할 계획인지를 설명하면 충분히 의미 있는 발표이다. "완성하지 못한 이유"를 기술적으로 분석할 수 있다면, 그 자체가 학습의 증거이다.

**Q: 과정이 끝난 후 혼자 공부를 계속하려면 어떻게 해야 하나요?**

A: 세 가지를 권장한다. 첫째, 이번 MVP를 Phase 1(Agent 고도화)까지 발전시켜 본다. 멀티턴 지원, Golden Test Set 확장, Prompt 최적화를 순서대로 진행하면 1~2주 안에 실력이 눈에 띄게 향상된다. 둘째, 다른 아키텍처로 새 프로젝트를 시도한다. 이번에 RAG를 했다면 MCP로, MCP를 했다면 Hybrid로 프로젝트를 하나 더 만들어보면 아키텍처 판단력이 크게 성장한다. 셋째, LangChain/LangGraph 커뮤니티(Discord, GitHub)에서 다른 사람의 프로젝트를 읽고, 자신의 프로젝트를 공유한다. 피드백을 주고받는 것이 가장 빠른 학습 경로이다.

<details>
<summary>퀴즈: MVP 체크리스트에서 "필수" 항목 12개 중 가장 먼저 확인해야 할 항목은?</summary>

**힌트**: 발표 평가 기준에서 가장 높은 배점(40%)을 차지하는 항목과 연결해보자.

**정답**: "Agent가 Happy Path에서 정상 동작한다"(구현 카테고리, 기술 구현 40%)를 가장 먼저 확인해야 한다. 이유: (1) 기술 구현이 40%로 가장 높은 배점이며, (2) Demo 품질(20%)도 동작하는 Agent가 있어야 점수를 받을 수 있으므로, 사실상 60%의 점수가 "Agent가 동작하는가"에 달려 있다. 문제 정의가 아무리 훌륭해도 Demo에서 Agent가 동작하지 않으면 최대 40점(문제 적합성 20% + 발표력 20%)밖에 받을 수 없다. 따라서 발표 준비의 최우선 순위는 "Happy Path Demo가 안정적으로 동작하는 것"이다.
</details>

---

## 실습: 최종 발표 및 피어 리뷰

### 5분 발표 + 5분 Q&A + 피어 리뷰
- **연관 학습 목표**: 학습 목표 1, 2, 3
- **실습 목적**: MVP Agent를 구조적으로 발표하고, 피어 리뷰를 통해 상호 학습한다
- **실습 유형**: 프로젝트 발표
- **난이도**: 심화
- **예상 소요 시간**: 90분 (준비 30분 + 발표/Q&A 50분 + 피어 리뷰 10분)
- **선행 조건**: Day 5 Session 1~3 전체
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

#### 실습 요구사항

1. **발표 자료 최종 점검 (15분)**
   - MVP 완성도 체크리스트(`mvp_checklist.py`) 실행
   - 필수 항목 미충족 시 우선순위 수정
   - Demo 스크립트 최종 리허설 (1회)

2. **발표 환경 점검 (5분)**
   - API 키 확인: `echo $OPENROUTER_API_KEY | head -c 10`
   - Demo 스크립트 실행 테스트: `python demo_script.py`
   - 터미널 설정 (폰트 크기, 배경색, 불필요한 알림 끄기)

3. **Q&A 대비 (10분)**
   - 예상 질문 5개 이상 PREP 형식으로 답변 준비
   - "모르는 질문" 대응 패턴 숙지
   - Trade-off 설명 1개 이상 준비

4. **발표 실행 (인당 10분: 5분 발표 + 5분 Q&A)**
   - 5단계 구조 준수: 문제 -> 솔루션 -> 데모 -> 결과 -> 다음 단계
   - 시간 초과 시 데모 우선, 다음 단계 생략 가능

5. **피어 리뷰 작성 (발표당 5분)**
   - `peer_review.py` 체크리스트 기반 평가
   - 잘한 점 2개 + 개선 제안 1개 + 배운 점 1개 반드시 작성
   - 작성 완료 후 발표자에게 전달

#### 발표 순서 운영 가이드

```
# 발표 운영 타임라인 (5명 기준, 90분)

00:00 ~ 00:30  발표 준비 (체크리스트 + 리허설 + 환경 점검)
00:30 ~ 00:40  발표자 1 (5분 발표 + 5분 Q&A)
00:40 ~ 00:50  발표자 2 (5분 발표 + 5분 Q&A)
00:50 ~ 01:00  발표자 3 (5분 발표 + 5분 Q&A)
01:00 ~ 01:10  발표자 4 (5분 발표 + 5분 Q&A)
01:10 ~ 01:20  발표자 5 (5분 발표 + 5분 Q&A)
01:20 ~ 01:30  피어 리뷰 작성 + 전달 + 종합 피드백
```

#### 산출물 목록

| # | 산출물 | 파일명 | 설명 |
|---|--------|--------|------|
| 1 | 프로젝트 설계서 | `design.md` | Session 1에서 작성한 설계 문서 |
| 2 | Agent 코드 | `agent.py`, `tools.py`, `rag.py` 등 | Session 2에서 구현한 코드 |
| 3 | 평가 결과 | `report.md` | Session 3에서 작성한 성능 리포트 |
| 4 | Demo 스크립트 | `demo_script.py` | Session 3에서 작성한 데모 스크립트 |
| 5 | 발표 자료 | 슬라이드 또는 마크다운 | Session 4에서 준비한 발표 자료 |
| 6 | 피어 리뷰 | `peer_review_{reviewer}_{presenter}.md` | Session 4에서 작성한 피어 리뷰 |

---

## 핵심 정리
- **5분 발표는 구조가 전부이다**: 문제 -> 솔루션 -> 데모 -> 결과 -> 다음 단계. 각 구간에서 핵심 한 가지만 전달하면 시간 안에 끝난다
- **기술 구현 40%가 최대 배점이다**: Demo가 동작해야 60%(기술 구현 40% + 데모 품질 20%)를 확보할 수 있다. 발표 준비의 최우선은 Happy Path Demo 안정화
- **PREP 법칙으로 Q&A를 장악하라**: 결론 먼저, 근거 한 문장, 증거 한 가지, 결론 반복. 30초 안에 끝내면 질문을 많이 받을 수 있다
- **피어 리뷰는 리뷰어가 가장 많이 배운다**: 다른 프로젝트를 구조적으로 평가하면 자신의 프로젝트를 객관적으로 돌아보는 시각을 얻는다
- **5일 과정의 가치는 프레임워크 체득이다**: 문제 정의 -> 설계 -> 구현 -> 평가 -> 발표의 사이클을 한 번 완주했으므로, 이후 어떤 Agent 프로젝트든 이 프레임워크를 적용할 수 있다
- **과정이 끝난 후가 진짜 시작이다**: MVP는 가능성 증명이다. Phase 1(Agent 고도화) -> Phase 2(프로덕션 배포) -> Phase 3(운영 안정화) 로드맵을 따라 발전시켜 나간다
