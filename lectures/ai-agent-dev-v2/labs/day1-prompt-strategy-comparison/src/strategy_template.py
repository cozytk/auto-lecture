"""
프롬프트 전략 비교 실습 템플릿
수강생이 TODO 주석을 채워 완성한다.
"""

import os
import time
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 실습용 리뷰 샘플
REVIEWS = [
    "배송이 빠르긴 했는데 포장이 엉망이었어요.",
    "제품이 정말 마음에 들어요! 다음에도 구매할게요.",
    "완전 실망입니다. 제품 설명과 실제가 너무 달라요.",
    "그냥 평범한 제품이에요. 딱히 특별하지 않아요.",
]


def measure_call(strategy_name: str, messages: list, system: str = "") -> dict:
    """LLM 호출 시간과 토큰 사용량을 측정한다."""
    start = time.time()

    kwargs = {
        "model": "claude-haiku-4-5",
        "max_tokens": 256,
        "messages": messages,
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)
    elapsed = time.time() - start

    return {
        "strategy": strategy_name,
        "response": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "latency_ms": round(elapsed * 1000),
    }


def zero_shot(review: str) -> dict:
    """
    TODO: Zero-shot 프롬프트를 작성한다.

    요구사항:
    - 예시 없이 지시만으로 리뷰를 긍정/부정/중립으로 분류
    - measure_call 함수로 호출하여 결과 반환
    """
    # TODO: 여기에 프롬프트를 작성하세요
    messages = [
        {
            "role": "user",
            "content": "",  # TODO: Zero-shot 프롬프트 작성
        }
    ]
    return measure_call("zero-shot", messages)


def few_shot(review: str) -> dict:
    """
    TODO: Few-shot 프롬프트를 작성한다.

    요구사항:
    - 긍정/부정/중립 각각 최소 1개 예시 포함
    - 예시 이후 실제 리뷰를 분류
    - measure_call 함수로 호출하여 결과 반환
    """
    # TODO: 여기에 Few-shot 프롬프트를 작성하세요
    messages = [
        {
            "role": "user",
            "content": "",  # TODO: Few-shot 프롬프트 작성 (예시 3개 포함)
        }
    ]
    return measure_call("few-shot", messages)


def chain_of_thought(review: str) -> dict:
    """
    TODO: Chain-of-Thought 프롬프트를 작성한다.

    요구사항:
    - 단계별 분석 과정을 포함 (긍정 표현 추출 → 부정 표현 추출 → 판단)
    - "단계적으로 생각해보자" 또는 단계 명시
    - measure_call 함수로 호출하여 결과 반환
    """
    # TODO: 여기에 CoT 프롬프트를 작성하세요
    messages = [
        {
            "role": "user",
            "content": "",  # TODO: CoT 프롬프트 작성
        }
    ]
    return measure_call("cot", messages)


def structured_output(review: str) -> dict:
    """
    TODO: Structured Output (Tool Use)을 구현한다.

    요구사항:
    - category: "긍정" | "부정" | "중립"
    - confidence: 0.0 ~ 1.0
    - reason: 분류 이유 (1문장)
    - Tool Use 방식으로 JSON Schema 강제
    """
    # TODO: tools 정의를 완성하세요
    tools = [
        {
            "name": "classify_review",
            "description": "",  # TODO: Tool 설명 작성
            "input_schema": {
                "type": "object",
                "properties": {
                    # TODO: category, confidence, reason 필드 추가
                },
                "required": [],  # TODO: required 필드 추가
            },
        }
    ]

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        tools=tools,
        # TODO: tool_choice 설정 (반드시 classify_review Tool 사용하도록)
        messages=[{"role": "user", "content": f"리뷰를 분류하라: {review}"}],
    )

    # TODO: Tool Use 결과를 추출하여 반환
    # response.content에서 tool_use 타입 블록을 찾아 .input을 반환
    return {}


def print_result(result: dict) -> None:
    """결과를 보기 좋게 출력한다."""
    print(f"\n[{result['strategy'].upper()}]")
    print(f"  응답: {result['response'][:100]}...")
    print(f"  입력 토큰: {result['input_tokens']}")
    print(f"  출력 토큰: {result['output_tokens']}")
    print(f"  지연: {result['latency_ms']}ms")


def print_summary(results: list[dict]) -> None:
    """세 전략의 비교 요약을 출력한다."""
    print("\n" + "=" * 50)
    print("전략 비교 요약")
    print("=" * 50)
    print(f"{'전략':<12} {'입력토큰':>8} {'출력토큰':>8} {'지연(ms)':>10}")
    print("-" * 50)
    for r in results:
        print(
            f"{r['strategy']:<12} {r['input_tokens']:>8} {r['output_tokens']:>8} {r['latency_ms']:>10}"
        )


def main():
    review = REVIEWS[0]
    print(f"분석 대상 리뷰: {review}\n")

    results = []

    # TODO: 세 전략을 순서대로 호출하고 결과를 results에 추가
    # 각 결과를 print_result로 출력

    # TODO: print_summary로 비교 요약 출력

    # TODO: structured_output을 호출하고 결과를 출력
    print("\n[STRUCTURED OUTPUT]")
    # ...


if __name__ == "__main__":
    main()
