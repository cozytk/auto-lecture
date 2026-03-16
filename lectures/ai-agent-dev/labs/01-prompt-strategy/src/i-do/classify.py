"""
I DO: 프롬프트 전략 비교 시연 코드

강사가 실행하며 시연합니다. 학생은 관찰하며 이해하세요.
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
    messages = [
        {
            "role": "system",
            "content": "고객 문의를 다음 카테고리 중 하나로 분류하세요: 환불, 배송, 제품문의, 기타",
        },
        {"role": "user", "content": text},
    ]
    return call_llm(messages)


def few_shot_classify(text: str) -> tuple[str, int]:
    messages = [
        {
            "role": "system",
            "content": "고객 문의를 다음 카테고리 중 하나로 분류하세요: 환불, 배송, 제품문의, 기타",
        },
        {"role": "user", "content": "주문한 지 일주일인데 아직 안 왔어요"},
        {"role": "assistant", "content": "배송"},
        {"role": "user", "content": "이 제품 사이즈가 어떻게 되나요?"},
        {"role": "assistant", "content": "제품문의"},
        {"role": "user", "content": "결제했는데 취소하고 돈 돌려받고 싶어요"},
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


def compare_strategies(text: str) -> None:
    print(f"\n{'='*60}")
    print(f"문의: {text}")
    print("=" * 60)

    result, tokens = zero_shot_classify(text)
    print(f"\n[Zero-shot] ({tokens} tokens)\n{result}")

    result, tokens = few_shot_classify(text)
    print(f"\n[Few-shot] ({tokens} tokens)\n{result}")

    result, tokens = cot_classify(text)
    print(f"\n[Chain-of-Thought] ({tokens} tokens)\n{result}")


if __name__ == "__main__":
    # 단순 문의: 전략 간 차이 없음
    compare_strategies("주문 취소하고 싶어요")

    # 복합 문의: CoT가 정확도 향상
    compare_strategies("색상이 다른데 교환 가능하면 교환, 안 되면 환불요")
