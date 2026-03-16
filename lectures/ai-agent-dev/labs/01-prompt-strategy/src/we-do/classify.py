"""
WE DO: 프롬프트 전략 비교 - 함께 실습

강사와 함께 TODO를 채워가며 실습합니다.
"""

import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


def call_llm(messages: list[dict]) -> tuple[str, int]:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    content = response.choices[0].message.content
    tokens = response.usage.total_tokens
    return content, tokens


def zero_shot_classify(text: str) -> tuple[str, int]:
    # TODO: system 메시지에 카테고리 목록을 포함한 분류 지시를 작성하세요
    # 카테고리: 환불, 배송, 제품문의, 기타
    messages = [
        {
            "role": "system",
            "content": "TODO: 분류 지시 작성",
        },
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


def few_shot_classify(text: str) -> tuple[str, int]:
    # TODO: 예시 3개를 messages 리스트에 추가하세요
    # 예시: "주문 지연" → "배송", "사이즈 문의" → "제품문의", "환불 요청" → "환불"
    messages = [
        {
            "role": "system",
            "content": "고객 문의를 다음 카테고리 중 하나로 분류하세요: 환불, 배송, 제품문의, 기타",
        },
        # TODO: 예시 쌍을 추가하세요 (user/assistant 번갈아)
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


def cot_classify(text: str) -> tuple[str, int]:
    # TODO: 단계별 추론을 유도하는 system 프롬프트를 작성하세요
    # 1. 키워드 추출  2. 의도 파악  3. 카테고리 선택
    messages = [
        {
            "role": "system",
            "content": "TODO: CoT 프롬프트 작성",
        },
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


def compare_all(queries: list[str]) -> None:
    print(f"{'문의':<30} {'Zero-shot':^10} {'Few-shot':^10} {'CoT':^10}")
    print("-" * 65)
    for text in queries:
        zs, _ = zero_shot_classify(text)
        fs, _ = few_shot_classify(text)
        cot_result, _ = cot_classify(text)
        # CoT 결과에서 카테고리만 추출
        cot_cat = cot_result.split("카테고리:")[-1].strip() if "카테고리:" in cot_result else cot_result
        print(f"{text[:28]:<30} {zs.strip():^10} {fs.strip():^10} {cot_cat.strip()[:8]:^10}")


if __name__ == "__main__":
    test_queries = [
        "주문 취소하고 싶어요",
        "배송이 너무 늦어요",
        "색상이 다른데 교환 불가면 환불요",
    ]
    compare_all(test_queries)
