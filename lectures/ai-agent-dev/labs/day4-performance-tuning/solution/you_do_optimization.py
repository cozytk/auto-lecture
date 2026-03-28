"""
Day 4 실습 - YOU DO 정답: 종합 성능 개선 파이프라인

진단 → 개선 → A/B 테스트 → 리포트 생성의 완성 코드이다.
"""

import os
import json
from datetime import datetime
from openai import OpenAI


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# =============================================================================
# 1. 성능 진단
# =============================================================================

AREA_MAP = {
    "task_completion_rate": "prompt",
    "f1_score": "prompt",
    "exact_match": "prompt",
    "groundedness": "rag",
    "hallucination_rate": "rag",
    "retrieval_precision": "rag",
    "tool_call_accuracy": "tool",
    "parameter_accuracy": "tool",
}


def diagnose(current_metrics: dict, baseline_metrics: dict, threshold: float = 0.05) -> list[dict]:
    """성능 저하 원인 진단"""
    issues = []

    for metric, current_val in current_metrics.items():
        baseline_val = baseline_metrics.get(metric)
        if baseline_val is None:
            continue

        drop = baseline_val - current_val

        if drop > threshold:
            severity = "critical" if drop > threshold * 3 else ("warning" if drop > threshold * 1.5 else "info")
            area = AREA_MAP.get(metric, "model")

            issues.append({
                "metric": metric,
                "area": area,
                "severity": severity,
                "baseline": baseline_val,
                "current": current_val,
                "drop": round(drop, 4),
                "drop_pct": round(drop / baseline_val * 100, 1),
            })

    # 심각도 순 정렬
    order = {"critical": 0, "warning": 1, "info": 2}
    issues.sort(key=lambda x: order.get(x["severity"], 3))

    return issues


# =============================================================================
# 2. Prompt 개선
# =============================================================================

def create_improved_prompt(original_prompt: str, diagnosis: list[dict]) -> str:
    """진단 결과를 기반으로 프롬프트 개선"""
    improvements = []

    areas_affected = set(d["area"] for d in diagnosis)

    if "rag" in areas_affected:
        improvements.append(
            "\n## 중요: 컨텍스트 기반 답변\n"
            "반드시 제공된 컨텍스트 정보에 근거하여 답변하세요.\n"
            "컨텍스트에 없는 정보는 '확인이 필요합니다'라고 안내하세요.\n"
            "절대 추측하거나 지어내지 마세요."
        )

    if "tool" in areas_affected:
        improvements.append(
            "\n## 도구 사용 가이드\n"
            "- 주문 관련 질문: 먼저 lookup_order로 주문 정보를 확인하세요\n"
            "- 상품 관련 질문: search_product로 상품 정보를 검색하세요\n"
            "- 환불 요청: lookup_order 확인 후 process_refund를 호출하세요"
        )

    if "prompt" in areas_affected:
        improvements.append(
            "\n## 응답 형식\n"
            "1. 고객의 요청을 정확히 파악하세요\n"
            "2. 필요한 도구를 호출하여 정보를 확인하세요\n"
            "3. 구체적인 정보(일정, 금액, 절차)를 포함하여 답변하세요\n"
            "4. 다음 단계가 있다면 안내하세요\n"
            "\n## 응답 예시\n"
            "고객: 환불하고 싶어요 (ORD-1234)\n"
            "답변: 주문 ORD-1234를 확인했습니다. 수령 후 7일 이내이므로 전액 환불이 가능합니다. "
            "환불을 진행하겠습니다. 3-5 영업일 내에 결제 수단으로 환불됩니다."
        )

    improved = original_prompt + "\n".join(improvements)
    return improved


# =============================================================================
# 3. A/B 테스트
# =============================================================================

def run_ab_test(
    prompt_a: str,
    prompt_b: str,
    test_cases: list[dict],
    model: str = "gpt-4o-mini"
) -> dict:
    """A/B 테스트 실행"""
    scores_a = []
    scores_b = []

    for i, case in enumerate(test_cases):
        print(f"  테스트 {i+1}/{len(test_cases)}...")

        # Version A
        resp_a = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt_a},
                {"role": "user", "content": case["input"]}
            ],
            temperature=0,
            max_tokens=500
        )
        output_a = resp_a.choices[0].message.content

        # Version B
        resp_b = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt_b},
                {"role": "user", "content": case["input"]}
            ],
            temperature=0,
            max_tokens=500
        )
        output_b = resp_b.choices[0].message.content

        # Judge
        score_a = _judge(case, output_a, model)
        score_b = _judge(case, output_b, model)

        scores_a.append(score_a)
        scores_b.append(score_b)

    mean_a = sum(scores_a) / len(scores_a)
    mean_b = sum(scores_b) / len(scores_b)
    wins_a = sum(1 for a, b in zip(scores_a, scores_b) if a > b)
    wins_b = sum(1 for a, b in zip(scores_a, scores_b) if b > a)
    improvement = ((mean_b - mean_a) / mean_a * 100) if mean_a > 0 else 0

    return {
        "total_cases": len(test_cases),
        "version_a": {"mean_score": round(mean_a, 4), "wins": wins_a},
        "version_b": {"mean_score": round(mean_b, 4), "wins": wins_b},
        "winner": "A" if mean_a > mean_b else ("B" if mean_b > mean_a else "tie"),
        "improvement_pct": round(improvement, 2),
    }


def _judge(case: dict, output: str, model: str) -> float:
    """LLM Judge"""
    prompt = f"""AI 응답의 품질을 0.0~1.0 점수로 평가하세요.

질문: {case['input']}
기대 답변 핵심: {case.get('expected', '없음')}
실제 답변: {output}

JSON 응답: {{"score": 0.0~1.0, "reason": "..."}}"""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
        max_tokens=200
    )
    return json.loads(resp.choices[0].message.content).get("score", 0.5)


# =============================================================================
# 4. 리포트 생성
# =============================================================================

def generate_report(
    baseline: dict,
    current: dict,
    diagnosis: list[dict],
    ab_result: dict = None
) -> str:
    """성능 개선 리포트 생성"""
    lines = [
        "# 성능 개선 리포트",
        f"**생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 1. 메트릭 비교 (Baseline vs Current)",
        "",
        "| 메트릭 | Baseline | Current | 변화 | 판정 |",
        "|--------|----------|---------|------|------|",
    ]

    for metric in sorted(set(list(baseline.keys()) + list(current.keys()))):
        b = baseline.get(metric, 0)
        c = current.get(metric, 0)
        change = c - b
        direction = "+" if change > 0 else ""
        verdict = "개선" if change > 0.01 else ("저하" if change < -0.01 else "유지")
        lines.append(f"| {metric} | {b:.4f} | {c:.4f} | {direction}{change:.4f} | {verdict} |")

    lines.extend(["", "## 2. 진단 결과", ""])
    if diagnosis:
        for d in diagnosis:
            lines.append(f"- **[{d['severity'].upper()}]** {d['metric']}: "
                        f"{d['baseline']:.3f} -> {d['current']:.3f} "
                        f"({d['drop_pct']}% 하락, 영역: {d['area']})")
    else:
        lines.append("이상 없음.")

    if ab_result:
        lines.extend([
            "",
            "## 3. A/B 테스트 결과",
            "",
            f"- Version A (원본): 평균 {ab_result['version_a']['mean_score']:.3f}",
            f"- Version B (개선): 평균 {ab_result['version_b']['mean_score']:.3f}",
            f"- 승자: Version {ab_result['winner']}",
            f"- 개선율: {ab_result['improvement_pct']:+.1f}%",
        ])

    lines.extend(["", "## 4. 권고 사항", ""])
    if ab_result and ab_result["winner"] == "B" and ab_result["improvement_pct"] > 5:
        lines.append("개선 버전(B)이 명확히 우세합니다. **프로덕션 배포를 권장**합니다.")
    elif ab_result and ab_result["winner"] == "B":
        lines.append("소폭 개선. 추가 테스트 케이스로 검증 후 배포를 검토하세요.")
    else:
        lines.append("추가 개선이 필요합니다. 진단 결과를 참고하여 다른 접근을 시도하세요.")

    return "\n".join(lines)


# =============================================================================
# 5. 파이프라인 실행
# =============================================================================

def run_optimization_pipeline():
    """종합 성능 개선 파이프라인"""
    print("=" * 60)
    print("종합 성능 개선 파이프라인")
    print("=" * 60)

    baseline_metrics = {
        "task_completion_rate": 0.90,
        "f1_score": 0.82,
        "groundedness": 0.85,
        "tool_call_accuracy": 0.88,
    }

    current_metrics = {
        "task_completion_rate": 0.75,
        "f1_score": 0.78,
        "groundedness": 0.62,
        "tool_call_accuracy": 0.85,
    }

    original_prompt = """당신은 고객 지원 Agent입니다.
고객의 질문에 답변하세요."""

    test_cases = [
        {"input": "주문번호 ORD-1234 환불하고 싶어요", "expected": "환불 절차 안내"},
        {"input": "배송이 3일째 안 오는데요?", "expected": "배송 상태 확인, 지연 사과"},
        {"input": "이 상품 AS 보증 기간이 어떻게 되나요?", "expected": "보증 기간, 정책 안내"},
    ]

    # Step 1: 진단
    print("\n[Step 1] 성능 진단")
    diagnosis = diagnose(current_metrics, baseline_metrics)
    for d in diagnosis:
        print(f"  [{d['severity'].upper()}] {d['metric']}: {d['drop_pct']}% 하락 (영역: {d['area']})")

    # Step 2: 개선
    print("\n[Step 2] 프롬프트 개선")
    improved_prompt = create_improved_prompt(original_prompt, diagnosis)
    print(f"  원본 길이: {len(original_prompt)}자")
    print(f"  개선 길이: {len(improved_prompt)}자")
    print(f"  추가 영역: {set(d['area'] for d in diagnosis)}")

    # Step 3: A/B 테스트
    print("\n[Step 3] A/B 테스트")
    ab_result = run_ab_test(original_prompt, improved_prompt, test_cases)
    print(f"  Version A: {ab_result['version_a']['mean_score']:.3f}")
    print(f"  Version B: {ab_result['version_b']['mean_score']:.3f}")
    print(f"  승자: Version {ab_result['winner']} ({ab_result['improvement_pct']:+.1f}%)")

    # Step 4: 리포트
    print("\n[Step 4] 리포트")
    report = generate_report(baseline_metrics, current_metrics, diagnosis, ab_result)
    print(report)


if __name__ == "__main__":
    run_optimization_pipeline()
