"""
YOU DO: 프롬프트 전략 비교 - 독립 과제

5개 고객 문의에 대해 3가지 전략을 각각 적용하고 결과를 비교하세요.
비교 표를 작성하고 각 전략의 장단점을 분석하세요.
"""

import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

test_queries = [
    "주문 취소하고 싶어요",
    "배송이 너무 늦어요. 언제 오나요?",
    "색상이 다른데 교환 가능하면 교환, 안 되면 환불요",
    "지난번에 산 것도 문제였고 이번에도 문제네요",
    "제품은 좋은데 배송 중 파손됐어요. AS가 되나요?",
]


def call_llm(messages: list[dict]) -> tuple[str, int]:
    # TODO: OpenAI client를 사용해 LLM을 호출하고 (응답 텍스트, 토큰 수)를 반환하세요
    pass


def zero_shot_classify(text: str) -> tuple[str, int]:
    # TODO: system 메시지로만 분류하는 zero-shot 전략을 구현하세요
    # 카테고리: 환불, 배송, 제품문의, 기타
    pass


def few_shot_classify(text: str) -> tuple[str, int]:
    # TODO: 3개 예시를 포함한 few-shot 전략을 구현하세요
    # 예시는 경계 케이스(edge case)를 포함할수록 효과적입니다
    pass


def cot_classify(text: str) -> tuple[str, int]:
    # TODO: 단계별 추론을 유도하는 CoT 전략을 구현하세요
    # 출력 형식: 키워드 → 의도 → 카테고리
    pass


def extract_category(cot_result: str) -> str:
    """CoT 결과에서 최종 카테고리만 추출합니다."""
    # TODO: "카테고리:" 이후 텍스트를 파싱하세요
    pass


def run_comparison() -> None:
    """5개 문의에 3가지 전략을 적용하고 비교 표를 출력합니다."""
    print("\n=== 프롬프트 전략 비교 ===\n")
    print(f"{'문의':<35} {'Zero-shot':^12} {'Few-shot':^12} {'CoT':^12} {'총토큰(ZS/FS/CoT)'}")
    print("-" * 90)

    for query in test_queries:
        # TODO: 각 전략 호출 및 결과 수집
        zs_result, zs_tokens = "TODO", 0
        fs_result, fs_tokens = "TODO", 0
        cot_result, cot_tokens = "TODO", 0

        cot_cat = extract_category(cot_result) if cot_result != "TODO" else "TODO"
        print(
            f"{query[:33]:<35} "
            f"{zs_result.strip()[:10]:^12} "
            f"{fs_result.strip()[:10]:^12} "
            f"{cot_cat.strip()[:10]:^12} "
            f"{zs_tokens}/{fs_tokens}/{cot_tokens}"
        )

    print("\n=== 분석 질문 ===")
    print("1. 어떤 유형의 문의에서 전략 간 차이가 가장 컸나요?")
    print("2. CoT가 오히려 불필요했던 경우가 있었나요?")
    print("3. 비용(토큰) 대비 성능이 가장 좋은 전략은 무엇인가요?")


if __name__ == "__main__":
    run_comparison()
