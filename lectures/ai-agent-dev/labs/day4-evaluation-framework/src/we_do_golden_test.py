"""
Day 4 실습 - WE DO: Golden Test Set 구축

전체가 함께 Agent 평가를 위한 Golden Test Set을 설계하고 구축한다.
Day 2-3에서 만든 Agent를 대상으로 테스트 케이스를 작성한다.
"""

import json
from pathlib import Path
from datetime import datetime


# =============================================================================
# 1. Golden Test Set 빌더
# =============================================================================

class GoldenTestBuilder:
    """Golden Test Set을 단계별로 구축하는 빌더"""

    def __init__(self, name: str, description: str):
        self.test_set = {
            "name": name,
            "description": description,
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "test_cases": []
        }
        self._counter = 0

    def add_test_case(
        self,
        category: str,
        difficulty: str,
        input_text: str,
        expected_output: str,
        context: str = "",
        expected_tool_calls: list[dict] = None,
        evaluation_criteria: dict = None,
        tags: list[str] = None,
    ) -> "GoldenTestBuilder":
        """테스트 케이스 추가

        Args:
            category: 분류 (예: "환불_문의", "상품_검색")
            difficulty: 난이도 ("easy", "medium", "hard")
            input_text: 사용자 입력
            expected_output: 기대 응답 (핵심 내용)
            context: 참조 컨텍스트 (RAG 문서 등)
            expected_tool_calls: 기대 도구 호출
            evaluation_criteria: 평가 기준 (must_include 등)
            tags: 태그 목록
        """
        self._counter += 1
        test_case = {
            "id": f"GT-{self._counter:03d}",
            "category": category,
            "difficulty": difficulty,
            "input": input_text,
            "expected_output": expected_output,
        }

        if context:
            test_case["context"] = context
        if expected_tool_calls:
            test_case["expected_tool_calls"] = expected_tool_calls
        if evaluation_criteria:
            test_case["evaluation_criteria"] = evaluation_criteria
        if tags:
            test_case["tags"] = tags

        self.test_set["test_cases"].append(test_case)
        return self

    def get_statistics(self) -> dict:
        """테스트셋 통계"""
        cases = self.test_set["test_cases"]
        categories = {}
        difficulties = {}

        for case in cases:
            cat = case["category"]
            diff = case["difficulty"]
            categories[cat] = categories.get(cat, 0) + 1
            difficulties[diff] = difficulties.get(diff, 0) + 1

        return {
            "total_cases": len(cases),
            "categories": categories,
            "difficulties": difficulties,
        }

    def save(self, filepath: str):
        """JSON 파일로 저장"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.test_set, f, ensure_ascii=False, indent=2)

        print(f"Golden Test Set 저장 완료: {filepath}")
        stats = self.get_statistics()
        print(f"  총 {stats['total_cases']}개 테스트 케이스")
        print(f"  카테고리: {stats['categories']}")
        print(f"  난이도: {stats['difficulties']}")


# =============================================================================
# 2. 함께 구축하기
# =============================================================================

def build_golden_test_set():
    """함께 Golden Test Set을 구축한다

    아래 예시를 참고하여, 수업 중 함께 테스트 케이스를 추가한다.
    """

    builder = GoldenTestBuilder(
        name="고객 지원 Agent 평가 셋",
        description="고객 문의 응답 Agent의 품질을 평가하기 위한 Golden Test Set"
    )

    # --- 예시 1: 쉬운 환불 문의 ---
    builder.add_test_case(
        category="환불_문의",
        difficulty="easy",
        input_text="지난주에 주문한 상품을 환불하고 싶습니다. 주문번호는 ORD-2025-1234입니다.",
        expected_output="주문번호 ORD-2025-1234의 환불을 처리해 드리겠습니다. 수령 후 7일 이내이므로 전액 환불이 가능합니다. 환불 금액은 3-5 영업일 내에 결제 수단으로 환불됩니다.",
        context="환불 정책: 수령 후 7일 이내 전액 환불. 14일 이내 배송비 고객 부담. 14일 초과 환불 불가.",
        expected_tool_calls=[
            {"tool": "lookup_order", "args": {"order_id": "ORD-2025-1234"}},
            {"tool": "process_refund", "args": {"order_id": "ORD-2025-1234", "type": "full"}}
        ],
        evaluation_criteria={
            "must_include": ["환불 처리", "3-5 영업일"],
            "must_not_include": ["확인되지 않은 정보", "부분 환불"],
            "required_tools": ["lookup_order", "process_refund"]
        },
        tags=["환불", "주문조회"]
    )

    # --- 예시 2: 중간 난이도 상품 비교 ---
    builder.add_test_case(
        category="상품_문의",
        difficulty="medium",
        input_text="에어팟 프로와 에어팟 맥스의 차이점이 뭔가요? 통화 품질이 중요한데 어떤 걸 사야 할까요?",
        expected_output="에어팟 프로는 인이어 타입으로 휴대성이 좋고, 에어팟 맥스는 오버이어 타입으로 음질이 우수합니다. 통화 품질은 둘 다 우수하지만, 소음 차단은 맥스가 더 뛰어납니다.",
        context="에어팟 프로: 인이어, ANC, 249,000원. 에어팟 맥스: 오버이어, ANC, 769,000원. 둘 다 H2 칩 탑재.",
        expected_tool_calls=[
            {"tool": "search_product", "args": {"query": "에어팟 프로 사양"}},
            {"tool": "search_product", "args": {"query": "에어팟 맥스 사양"}}
        ],
        evaluation_criteria={
            "must_include": ["차이점", "통화"],
            "must_not_include": ["추측"],
            "required_tools": ["search_product"]
        },
        tags=["상품비교", "추천"]
    )

    # --- 예시 3: 어려운 복합 문의 ---
    builder.add_test_case(
        category="복합_문의",
        difficulty="hard",
        input_text="지난달에 산 노트북(ORD-2025-5678)이 배터리 문제가 있어서 교환하고 싶고, 같이 산 마우스(ORD-2025-5679)는 환불하고 싶어요.",
        expected_output="두 건을 각각 처리해 드리겠습니다. 노트북은 배터리 불량으로 무상 교환 진행하고, 마우스는 환불 처리하겠습니다.",
        context="교환 정책: 제품 불량 시 무상 교환 (30일 이내). 환불 정책: 14일 이내 환불 가능.",
        expected_tool_calls=[
            {"tool": "lookup_order", "args": {"order_id": "ORD-2025-5678"}},
            {"tool": "lookup_order", "args": {"order_id": "ORD-2025-5679"}},
            {"tool": "process_exchange", "args": {"order_id": "ORD-2025-5678", "reason": "defect"}},
            {"tool": "process_refund", "args": {"order_id": "ORD-2025-5679", "type": "full"}}
        ],
        evaluation_criteria={
            "must_include": ["교환", "환불", "두 건"],
            "must_not_include": ["단일 처리"],
            "required_tools": ["lookup_order", "process_exchange", "process_refund"]
        },
        tags=["교환", "환불", "복합처리"]
    )

    # =========================================================================
    # 여기에 수업 중 함께 테스트 케이스를 추가한다
    # =========================================================================

    # builder.add_test_case(
    #     category="???",
    #     difficulty="???",
    #     input_text="???",
    #     expected_output="???",
    #     ...
    # )

    # --- 저장 ---
    data_dir = Path(__file__).parent.parent / "data"
    builder.save(str(data_dir / "golden_test_set.json"))

    return builder


# =============================================================================
# 3. 테스트셋 검증
# =============================================================================

def validate_test_set(filepath: str):
    """Golden Test Set의 품질을 검증"""
    with open(filepath, encoding="utf-8") as f:
        test_set = json.load(f)

    issues = []
    cases = test_set.get("test_cases", [])

    for case in cases:
        case_id = case.get("id", "unknown")

        # 필수 필드 확인
        for field in ["id", "category", "difficulty", "input", "expected_output"]:
            if field not in case:
                issues.append(f"{case_id}: 필수 필드 '{field}' 누락")

        # 난이도 값 확인
        if case.get("difficulty") not in ("easy", "medium", "hard"):
            issues.append(f"{case_id}: 난이도는 easy/medium/hard 중 하나여야 합니다")

        # 입력 최소 길이
        if len(case.get("input", "")) < 5:
            issues.append(f"{case_id}: 입력이 너무 짧습니다 (5자 이상 권장)")

        # 기대 출력 최소 길이
        if len(case.get("expected_output", "")) < 10:
            issues.append(f"{case_id}: 기대 출력이 너무 짧습니다 (10자 이상 권장)")

    # 분포 확인
    categories = [c["category"] for c in cases]
    difficulties = [c["difficulty"] for c in cases]

    if len(set(difficulties)) < 2:
        issues.append("난이도 분포: 최소 2개 이상의 난이도를 포함해야 합니다")

    print(f"\n검증 결과: {'통과' if not issues else f'{len(issues)}개 이슈 발견'}")
    for issue in issues:
        print(f"  - {issue}")

    return len(issues) == 0


if __name__ == "__main__":
    print("=" * 60)
    print("WE DO: Golden Test Set 구축")
    print("=" * 60)

    builder = build_golden_test_set()

    # 검증
    data_path = Path(__file__).parent.parent / "data" / "golden_test_set.json"
    validate_test_set(str(data_path))
