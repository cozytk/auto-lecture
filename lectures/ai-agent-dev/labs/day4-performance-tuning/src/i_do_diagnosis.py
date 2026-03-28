"""
Day 4 실습 - I DO: Agent 성능 저하 진단

강사가 시연하는 코드이다. 학생은 관찰하며 이해한다.
기준 메트릭(baseline)과 현재 메트릭을 비교하여 저하 원인을 자동으로 진단한다.
"""

from dataclasses import dataclass


# =============================================================================
# 1. 진단 결과 데이터 클래스
# =============================================================================

@dataclass
class DiagnosisResult:
    """진단 결과"""
    area: str       # "prompt", "rag", "tool", "model"
    severity: str   # "critical", "warning", "info"
    metric: str     # 하락한 메트릭 이름
    message: str    # 진단 메시지
    recommendation: str  # 개선 권고


# =============================================================================
# 2. 진단 엔진
# =============================================================================

def diagnose_performance(
    current_metrics: dict,
    baseline_metrics: dict,
    threshold: float = 0.05
) -> list[DiagnosisResult]:
    """성능 메트릭을 비교하여 저하 원인을 진단

    Args:
        current_metrics: 현재 측정된 메트릭 (0.0 ~ 1.0)
        baseline_metrics: 기준 메트릭 (이전 버전)
        threshold: 허용 하락 폭 (기본 5%)

    Returns:
        진단 결과 목록 (심각한 순서로 정렬)
    """
    diagnoses = []

    for metric_name, current_value in current_metrics.items():
        baseline_value = baseline_metrics.get(metric_name)
        if baseline_value is None:
            continue

        drop = baseline_value - current_value

        if drop > threshold:
            # 심각도 판정
            if drop > threshold * 3:
                severity = "critical"
            elif drop > threshold * 1.5:
                severity = "warning"
            else:
                severity = "info"

            # 영역 분류
            area = _classify_area(metric_name)

            # 권고사항
            recommendation = _get_recommendation(metric_name, drop)

            diagnosis = DiagnosisResult(
                area=area,
                severity=severity,
                metric=metric_name,
                message=(
                    f"{metric_name}: {baseline_value:.3f} -> {current_value:.3f} "
                    f"({drop:.3f} 하락, {drop/baseline_value*100:.1f}%)"
                ),
                recommendation=recommendation
            )
            diagnoses.append(diagnosis)

    # 심각도 순 정렬
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    diagnoses.sort(key=lambda d: severity_order.get(d.severity, 3))

    return diagnoses


def _classify_area(metric_name: str) -> str:
    """메트릭 이름으로 영역 분류"""
    area_map = {
        "task_completion_rate": "prompt",
        "exact_match": "prompt",
        "f1_score": "prompt",
        "groundedness": "rag",
        "hallucination_rate": "rag",
        "retrieval_precision": "rag",
        "retrieval_recall": "rag",
        "tool_call_accuracy": "tool",
        "parameter_accuracy": "tool",
        "tool_selection_f1": "tool",
    }
    return area_map.get(metric_name, "model")


def _get_recommendation(metric_name: str, drop: float) -> str:
    """메트릭별 개선 권고"""
    recommendations = {
        "task_completion_rate": (
            "카테고리별 성능 분석 후 약한 영역의 Few-shot 예시를 보강하세요. "
            "실패 케이스의 공통 패턴을 찾아 프롬프트에 반영하세요."
        ),
        "exact_match": (
            "출력 포맷 지시를 프롬프트에 강화하세요. "
            "파싱 로직이 정상 동작하는지 확인하세요."
        ),
        "f1_score": (
            "프롬프트에 핵심 키워드 포함 지시를 추가하세요. "
            "누락되는 정보가 무엇인지 분석하세요."
        ),
        "groundedness": (
            "RAG 검색 결과의 relevance score 임계값을 높이세요. "
            "컨텍스트 기반 답변을 강제하는 프롬프트를 추가하세요."
        ),
        "hallucination_rate": (
            "환각 방지 프롬프트를 강화하세요: "
            "'제공된 정보에만 근거하여 답변하세요. 모르는 것은 모른다고 하세요.'"
        ),
        "retrieval_precision": (
            "임베딩 모델 업데이트 또는 청킹 전략을 재설계하세요. "
            "쿼리 변환(Query Rewriting) 도입을 검토하세요."
        ),
        "retrieval_recall": (
            "검색 top_k 값을 늘리거나 Hybrid Search(키워드+벡터)를 적용하세요."
        ),
        "tool_call_accuracy": (
            "Tool description을 더 구체적으로 재작성하세요. "
            "사용 시점, 파라미터 예시를 포함하세요."
        ),
        "parameter_accuracy": (
            "Tool 파라미터 스키마에 description과 예시를 추가하세요."
        ),
    }
    return recommendations.get(metric_name, "종합 진단이 필요합니다. 로그 분석을 수행하세요.")


# =============================================================================
# 3. 시연 실행
# =============================================================================

def run_diagnosis_demo():
    """진단 시연"""
    print("=" * 60)
    print("Agent 성능 저하 진단 시연")
    print("=" * 60)

    # 시나리오: 프롬프트 변경 후 일부 메트릭이 하락한 상황
    baseline = {
        "task_completion_rate": 0.92,
        "f1_score": 0.85,
        "groundedness": 0.88,
        "hallucination_rate": 0.95,  # 높을수록 좋음 (환각 없는 비율)
        "tool_call_accuracy": 0.90,
        "parameter_accuracy": 0.87,
        "retrieval_precision": 0.82,
    }

    current = {
        "task_completion_rate": 0.78,   # 큰 하락
        "f1_score": 0.80,              # 소폭 하락
        "groundedness": 0.65,          # 큰 하락
        "hallucination_rate": 0.70,    # 큰 하락
        "tool_call_accuracy": 0.88,    # 소폭 하락 (임계값 이내)
        "parameter_accuracy": 0.85,    # 소폭 하락 (임계값 이내)
        "retrieval_precision": 0.60,   # 큰 하락
    }

    print("\n--- Baseline 메트릭 ---")
    for k, v in baseline.items():
        print(f"  {k:25s}: {v:.3f}")

    print("\n--- Current 메트릭 ---")
    for k, v in current.items():
        diff = v - baseline[k]
        marker = " <-- 하락" if diff < -0.05 else ""
        print(f"  {k:25s}: {v:.3f}  ({diff:+.3f}){marker}")

    print("\n--- 진단 결과 ---")
    diagnoses = diagnose_performance(current, baseline)

    if not diagnoses:
        print("  성능 이상 없음. 모든 메트릭이 정상 범위입니다.")
        return

    for d in diagnoses:
        icon = {"critical": "[!!!]", "warning": "[!!]", "info": "[!]"}.get(d.severity, "")
        print(f"\n  {icon} [{d.severity.upper()}] 영역: {d.area}")
        print(f"     {d.message}")
        print(f"     권고: {d.recommendation}")

    # 요약
    print("\n--- 요약 ---")
    areas = set(d.area for d in diagnoses)
    critical_count = sum(1 for d in diagnoses if d.severity == "critical")
    warning_count = sum(1 for d in diagnoses if d.severity == "warning")

    print(f"  총 {len(diagnoses)}개 이슈 발견")
    print(f"  Critical: {critical_count}, Warning: {warning_count}")
    print(f"  영향 영역: {', '.join(areas)}")

    if critical_count > 0:
        print("\n  => 즉시 대응 필요! Critical 이슈부터 해결하세요.")
    elif warning_count > 0:
        print("\n  => Warning 이슈를 1주 내에 해결하세요.")
    else:
        print("\n  => 경미한 이슈. 모니터링을 지속하세요.")


if __name__ == "__main__":
    run_diagnosis_demo()
