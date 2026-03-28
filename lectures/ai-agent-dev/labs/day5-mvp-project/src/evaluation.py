"""
평가 스크립트

Golden Test Set을 기반으로 Agent의 성능을 자동 평가한다.
정확도, 응답 시간, 토큰 사용량 등을 측정하고 결과를 리포트한다.

TODO: 프로젝트에 맞게 아래 항목을 수정하세요.
  1. evaluate_single()에서 정답 판정 로직 수정
  2. 프로젝트 고유의 평가 지표 추가
  3. (선택) LLM-as-a-Judge 평가 추가
"""

import json
import time
from pathlib import Path

from config import validate_config
from agent import create_agent_graph
from main import run_single_query


# ============================================================
# 1. Golden Test Set 로드
# ============================================================
def load_test_set(path: str = "./data/golden_test_set.json") -> list[dict]:
    """Golden Test Set을 로드한다."""
    test_path = Path(path)
    if not test_path.exists():
        print(f"Golden Test Set이 없습니다: {path}")
        print("data/golden_test_set.json 파일을 작성하세요.")
        return []

    with open(test_path, "r", encoding="utf-8") as f:
        test_set = json.load(f)

    print(f"Golden Test Set 로드 완료: {len(test_set['test_cases'])}건")
    return test_set["test_cases"]


# ============================================================
# 2. 단건 평가
# ============================================================
def evaluate_single(
    graph,
    test_case: dict,
) -> dict:
    """단일 테스트 케이스를 평가한다.

    Args:
        graph: 컴파일된 Agent 그래프
        test_case: 테스트 케이스 dict

    Returns:
        dict: 평가 결과
    """
    input_text = test_case["input"]
    expected = test_case["expected_output"]
    category = test_case.get("category", "unknown")

    # Agent 실행 + 시간 측정
    start_time = time.time()
    try:
        result = run_single_query(graph, input_text)
        elapsed = time.time() - start_time
        response = result["response"]
        success = result["success"]
    except Exception as e:
        elapsed = time.time() - start_time
        response = f"실행 오류: {str(e)}"
        success = False

    # 정답 판정
    # TODO: 프로젝트에 맞는 정답 판정 로직을 구현하세요.
    # 현재는 expected_output의 키워드가 응답에 포함되어 있는지 확인합니다.
    if isinstance(expected, list):
        # expected가 키워드 리스트인 경우: 모든 키워드 포함 여부
        passed = success and all(kw.lower() in response.lower() for kw in expected)
    elif isinstance(expected, str):
        # expected가 문자열인 경우: 포함 여부
        passed = success and expected.lower() in response.lower()
    else:
        passed = False

    return {
        "input": input_text,
        "expected": expected,
        "actual": response,
        "passed": passed,
        "category": category,
        "elapsed_seconds": round(elapsed, 2),
    }


# ============================================================
# 3. 전체 평가 실행
# ============================================================
def run_evaluation(
    graph,
    test_cases: list[dict],
) -> dict:
    """전체 Golden Test Set을 평가한다."""
    results = []

    print(f"\n{'='*60}")
    print(f"평가 실행 시작 ({len(test_cases)}건)")
    print(f"{'='*60}")

    for i, tc in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] {tc['input'][:50]}...")
        result = evaluate_single(graph, tc)

        status = "PASS" if result["passed"] else "FAIL"
        print(f"  결과: {status} (소요: {result['elapsed_seconds']}초)")
        if not result["passed"]:
            print(f"  기대: {result['expected']}")
            print(f"  실제: {result['actual'][:100]}...")

        results.append(result)

    return analyze_results(results)


# ============================================================
# 4. 결과 분석
# ============================================================
def analyze_results(results: list[dict]) -> dict:
    """평가 결과를 분석하여 요약 리포트를 생성한다."""
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed

    # 카테고리별 분석
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "passed": 0}
        categories[cat]["total"] += 1
        if r["passed"]:
            categories[cat]["passed"] += 1

    # 응답 시간 분석
    times = [r["elapsed_seconds"] for r in results]
    avg_time = sum(times) / len(times) if times else 0
    max_time = max(times) if times else 0
    min_time = min(times) if times else 0

    # 리포트 생성
    report = {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / total * 100, 1) if total > 0 else 0,
        },
        "by_category": {
            cat: {
                "total": data["total"],
                "passed": data["passed"],
                "pass_rate": round(data["passed"] / data["total"] * 100, 1),
            }
            for cat, data in categories.items()
        },
        "timing": {
            "avg_seconds": round(avg_time, 2),
            "max_seconds": round(max_time, 2),
            "min_seconds": round(min_time, 2),
        },
        "failed_cases": [r for r in results if not r["passed"]],
    }

    # 리포트 출력
    print(f"\n{'='*60}")
    print("평가 결과 요약")
    print(f"{'='*60}")
    print(f"전체 성공률: {report['summary']['pass_rate']}% ({passed}/{total})")
    print(f"\n카테고리별:")
    for cat, data in report["by_category"].items():
        print(f"  {cat}: {data['pass_rate']}% ({data['passed']}/{data['total']})")
    print(f"\n응답 시간:")
    print(f"  평균: {report['timing']['avg_seconds']}초")
    print(f"  최대: {report['timing']['max_seconds']}초")
    print(f"  최소: {report['timing']['min_seconds']}초")

    if report["failed_cases"]:
        print(f"\n실패 케이스 ({len(report['failed_cases'])}건):")
        for fc in report["failed_cases"]:
            print(f"  - [{fc['category']}] {fc['input'][:50]}...")

    return report


# ============================================================
# 메인 실행
# ============================================================
def main():
    # 설정 검증
    if not validate_config():
        return

    # Golden Test Set 로드
    test_cases = load_test_set()
    if not test_cases:
        return

    # Agent 생성
    print("Agent를 초기화합니다...")
    graph = create_agent_graph()

    # 평가 실행
    report = run_evaluation(graph, test_cases)

    # 결과 저장
    output_path = "./data/evaluation_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n평가 결과가 저장되었습니다: {output_path}")


if __name__ == "__main__":
    main()
