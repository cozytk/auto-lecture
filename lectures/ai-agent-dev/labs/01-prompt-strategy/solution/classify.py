"""
YOU DO 정답: 프롬프트 전략 비교

학생이 과제 완료 후 참고하는 정답 코드입니다.
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
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content, response.usage.total_tokens


def zero_shot_classify(text: str) -> tuple[str, int]:
    messages = [
        {
            "role": "system",
            "content": "고객 문의를 다음 카테고리 중 하나로 분류하세요: 환불, 배송, 제품문의, 기타",
        },
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


def few_shot_classify(text: str) -> tuple[str, int]:
    # 경계 케이스를 포함한 다양한 예시: 예시의 질이 수보다 중요하다
    messages = [
        {
            "role": "system",
            "content": "고객 문의를 다음 카테고리 중 하나로 분류하세요: 환불, 배송, 제품문의, 기타",
        },
        {"role": "user", "content": "주문한 지 일주일인데 아직 안 왔어요"},
        {"role": "assistant", "content": "배송"},
        {"role": "user", "content": "이 제품 사이즈가 어떻게 되나요?"},
        {"role": "assistant", "content": "제품문의"},
        # 복합 조건 경계 케이스: 교환+환불 중 환불이 우선
        {"role": "user", "content": "색상이 달라서 교환 원하는데 품절이면 환불해주세요"},
        {"role": "assistant", "content": "환불"},
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


def cot_classify(text: str) -> tuple[str, int]:
    messages = [
        {
            "role": "system",
            "content": """고객 문의를 분류하세요.

단계별로 분석하세요:
1. 고객이 언급한 핵심 키워드를 추출하세요
2. 고객의 의도(원하는 행동)를 파악하세요
3. 의도에 맞는 카테고리를 선택하세요

카테고리: 환불, 배송, 제품문의, 기타

응답 형식:
키워드: [추출된 키워드]
의도: [파악된 의도]
카테고리: [선택된 카테고리]""",
        },
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


def extract_category(cot_result: str) -> str:
    """CoT 결과에서 최종 카테고리만 추출합니다."""
    if "카테고리:" in cot_result:
        return cot_result.split("카테고리:")[-1].strip().split("\n")[0]
    return cot_result.strip()


def run_comparison() -> None:
    print("\n=== 프롬프트 전략 비교 ===\n")
    print(f"{'문의':<35} {'Zero-shot':^12} {'Few-shot':^12} {'CoT':^12} {'총토큰(ZS/FS/CoT)'}")
    print("-" * 90)

    results = []
    for query in test_queries:
        zs_result, zs_tokens = zero_shot_classify(query)
        fs_result, fs_tokens = few_shot_classify(query)
        cot_result, cot_tokens = cot_classify(query)
        cot_cat = extract_category(cot_result)

        results.append({
            "query": query,
            "zero_shot": zs_result.strip(),
            "few_shot": fs_result.strip(),
            "cot": cot_cat.strip(),
            "tokens": (zs_tokens, fs_tokens, cot_tokens),
        })

        print(
            f"{query[:33]:<35} "
            f"{zs_result.strip()[:10]:^12} "
            f"{fs_result.strip()[:10]:^12} "
            f"{cot_cat.strip()[:10]:^12} "
            f"{zs_tokens}/{fs_tokens}/{cot_tokens}"
        )

    print("\n=== 분석 결과 ===")
    print("차이 가장 큰 유형: 복합 조건 문의 (교환+환불) - CoT가 정확도 향상")
    print("CoT 불필요한 경우: 단순 취소/배송 문의 - Zero-shot으로 충분")
    print("비용 대비 최적: Zero-shot (단순), CoT (복합 판단 필요 시)")


if __name__ == "__main__":
    run_comparison()
