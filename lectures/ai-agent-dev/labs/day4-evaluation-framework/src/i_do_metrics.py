"""
Day 4 실습 - I DO: 기본 평가 메트릭 구현 및 시연

강사가 시연하는 코드이다. 학생은 관찰하며 이해한다.
Agent 응답의 품질을 자동으로 측정하는 메트릭을 구현한다.
"""

import json
from collections import Counter
from dataclasses import dataclass, asdict


# =============================================================================
# 1. 평가 결과 데이터 클래스
# =============================================================================

@dataclass
class EvalResult:
    """평가 결과를 담는 데이터 클래스"""
    metric_name: str
    score: float  # 0.0 ~ 1.0
    details: dict


# =============================================================================
# 2. 기본 메트릭 구현
# =============================================================================

def exact_match(prediction: str, reference: str) -> EvalResult:
    """Exact Match: 정확히 일치하는지 평가

    가장 엄격한 메트릭이다. 완전히 동일한 문자열일 때만 1.0.
    분류 작업, 짧은 답변에 적합하다.
    """
    score = 1.0 if prediction.strip() == reference.strip() else 0.0
    return EvalResult(
        metric_name="exact_match",
        score=score,
        details={"prediction": prediction[:100], "reference": reference[:100]}
    )


def f1_score(prediction: str, reference: str) -> EvalResult:
    """F1 Score: 토큰 단위 부분 일치 평가

    Exact Match보다 유연하다.
    답변의 핵심 단어가 포함되었는지 측정한다.
    """
    pred_tokens = prediction.lower().split()
    ref_tokens = reference.lower().split()

    if not pred_tokens or not ref_tokens:
        return EvalResult(metric_name="f1_score", score=0.0, details={})

    common = Counter(pred_tokens) & Counter(ref_tokens)
    num_common = sum(common.values())

    if num_common == 0:
        return EvalResult(
            metric_name="f1_score",
            score=0.0,
            details={"precision": 0, "recall": 0}
        )

    precision = num_common / len(pred_tokens)
    recall = num_common / len(ref_tokens)
    f1 = 2 * precision * recall / (precision + recall)

    return EvalResult(
        metric_name="f1_score",
        score=round(f1, 4),
        details={"precision": round(precision, 4), "recall": round(recall, 4)}
    )


def tool_call_accuracy(
    predicted_calls: list[dict],
    expected_calls: list[dict]
) -> EvalResult:
    """Tool Call Accuracy: 도구 호출 정확도 평가

    Agent가 올바른 도구를 올바른 파라미터로 호출했는지 측정한다.

    Args:
        predicted_calls: Agent가 실제로 호출한 도구 목록
            [{"tool": "search", "args": {"query": "..."}}]
        expected_calls: 기대하는 도구 호출 목록
    """
    if not expected_calls:
        score = 1.0 if not predicted_calls else 0.0
        return EvalResult(
            metric_name="tool_call_accuracy",
            score=score,
            details={"message": "도구 호출이 필요 없는 케이스"}
        )

    correct = 0
    total = len(expected_calls)
    matched = []
    unmatched = []

    for expected in expected_calls:
        found = False
        for predicted in predicted_calls:
            if (predicted["tool"] == expected["tool"] and
                predicted.get("args") == expected.get("args")):
                correct += 1
                matched.append(expected["tool"])
                found = True
                break
        if not found:
            unmatched.append(expected["tool"])

    score = correct / total
    return EvalResult(
        metric_name="tool_call_accuracy",
        score=round(score, 4),
        details={
            "correct": correct,
            "total": total,
            "predicted_count": len(predicted_calls),
            "matched_tools": matched,
            "unmatched_tools": unmatched
        }
    )


def task_completion_rate(results: list[dict]) -> EvalResult:
    """Task Completion Rate: 작업 완료율

    여러 작업의 성공/실패를 종합하여 완료율을 계산한다.

    Args:
        results: [{"task_id": "1", "completed": True, "error": None}]
    """
    if not results:
        return EvalResult(
            metric_name="task_completion_rate",
            score=0.0,
            details={"message": "평가할 작업이 없습니다"}
        )

    completed = sum(1 for r in results if r["completed"])
    total = len(results)
    score = completed / total

    failed_tasks = [
        {"id": r["task_id"], "error": r.get("error", "unknown")}
        for r in results
        if not r["completed"]
    ]

    return EvalResult(
        metric_name="task_completion_rate",
        score=round(score, 4),
        details={
            "completed": completed,
            "total": total,
            "failed_tasks": failed_tasks
        }
    )


# =============================================================================
# 3. 종합 평가 실행
# =============================================================================

def run_evaluation_demo():
    """메트릭 시연 실행"""
    print("=" * 60)
    print("Agent 평가 메트릭 시연")
    print("=" * 60)

    # --- Exact Match ---
    print("\n--- 1. Exact Match ---")
    em1 = exact_match("환불이 완료되었습니다.", "환불이 완료되었습니다.")
    em2 = exact_match("환불 처리 완료했습니다.", "환불이 완료되었습니다.")
    print(f"  동일한 응답:  score = {em1.score}")
    print(f"  유사한 응답:  score = {em2.score}  (엄격하게 불일치)")

    # --- F1 Score ---
    print("\n--- 2. F1 Score ---")
    f1_1 = f1_score(
        "주문번호 ORD-1234의 환불을 처리해 드리겠습니다. 3-5 영업일 소요됩니다.",
        "주문번호 ORD-1234의 환불이 완료되었습니다. 3-5 영업일 내에 환불됩니다."
    )
    f1_2 = f1_score(
        "오늘 날씨가 좋습니다.",
        "주문번호 ORD-1234의 환불이 완료되었습니다."
    )
    print(f"  유사한 응답:  score = {f1_1.score}  (precision={f1_1.details['precision']}, recall={f1_1.details['recall']})")
    print(f"  무관한 응답:  score = {f1_2.score}  (전혀 다른 내용)")

    # --- Tool Call Accuracy ---
    print("\n--- 3. Tool Call Accuracy ---")
    tc1 = tool_call_accuracy(
        predicted_calls=[
            {"tool": "lookup_order", "args": {"order_id": "ORD-1234"}},
            {"tool": "process_refund", "args": {"order_id": "ORD-1234", "type": "full"}}
        ],
        expected_calls=[
            {"tool": "lookup_order", "args": {"order_id": "ORD-1234"}},
            {"tool": "process_refund", "args": {"order_id": "ORD-1234", "type": "full"}}
        ]
    )
    tc2 = tool_call_accuracy(
        predicted_calls=[
            {"tool": "search_product", "args": {"query": "환불"}}
        ],
        expected_calls=[
            {"tool": "lookup_order", "args": {"order_id": "ORD-1234"}},
            {"tool": "process_refund", "args": {"order_id": "ORD-1234", "type": "full"}}
        ]
    )
    print(f"  정확한 호출:  score = {tc1.score}  {tc1.details}")
    print(f"  잘못된 호출:  score = {tc2.score}  unmatched={tc2.details['unmatched_tools']}")

    # --- Task Completion Rate ---
    print("\n--- 4. Task Completion Rate ---")
    tcr = task_completion_rate([
        {"task_id": "1", "completed": True, "error": None},
        {"task_id": "2", "completed": True, "error": None},
        {"task_id": "3", "completed": False, "error": "Tool timeout"},
        {"task_id": "4", "completed": True, "error": None},
        {"task_id": "5", "completed": False, "error": "LLM parse error"},
    ])
    print(f"  완료율:  score = {tcr.score}  ({tcr.details['completed']}/{tcr.details['total']})")
    print(f"  실패 작업: {tcr.details['failed_tasks']}")

    # --- 종합 ---
    print("\n" + "=" * 60)
    print("종합: 모든 메트릭은 0.0 ~ 1.0 범위")
    print("  1.0 = 완벽, 0.0 = 완전 실패")
    print("  실제 운영에서는 여러 메트릭을 조합하여 종합 점수를 산출한다")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation_demo()
