"""
프롬프트 전략 비교 정답 코드
Zero-shot / Few-shot / CoT 세 전략을 구현하고 비교한다.
"""

import os
import time
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

REVIEWS = [
    "배송이 빠르긴 했는데 포장이 엉망이었어요.",
    "제품이 정말 마음에 들어요! 다음에도 구매할게요.",
    "완전 실망입니다. 제품 설명과 실제가 너무 달라요.",
    "그냥 평범한 제품이에요. 딱히 특별하지 않아요.",
]


def measure_call(strategy_name: str, messages: list, system: str = "") -> dict:
    """LLM 호출 시간과 토큰 사용량을 측정한다."""
    start = time.time()

    kwargs: dict = {
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
    Zero-shot: 예시 없이 지시만으로 분류를 요청한다.

    적합 상황: 단순 분류, 빠른 처리, 비용 최소화
    단점: 복잡한 태스크에서 품질 불안정
    """
    messages = [
        {
            "role": "user",
            "content": (
                f"다음 고객 리뷰를 긍정/부정/중립 중 하나로 분류하라.\n"
                f"분류 결과만 한 단어로 답하라.\n\n"
                f"리뷰: {review}"
            ),
        }
    ]
    return measure_call("zero-shot", messages)


def few_shot(review: str) -> dict:
    """
    Few-shot: 예시를 보여주어 출력 형식과 판단 기준을 학습시킨다.

    적합 상황: 출력 형식이 중요한 경우, 도메인 특화 분류
    단점: 프롬프트 길이 증가, 토큰 비용 상승
    """
    messages = [
        {
            "role": "user",
            "content": (
                "고객 리뷰를 긍정/부정/중립으로 분류하라.\n"
                "분류 결과만 한 단어로 답하라.\n\n"
                "예시:\n"
                "리뷰: '정말 만족스러운 제품이에요!' → 긍정\n"
                "리뷰: '배송이 너무 늦어서 화가 납니다.' → 부정\n"
                "리뷰: '평범한 제품이에요. 특별한 점은 없네요.' → 중립\n"
                "리뷰: '품질은 좋은데 가격이 좀 비싸요.' → 중립\n\n"
                f"리뷰: '{review}' →"
            ),
        }
    ]
    return measure_call("few-shot", messages)


def chain_of_thought(review: str) -> dict:
    """
    Chain-of-Thought: 단계별 추론 과정을 포함하도록 유도한다.

    적합 상황: 복잡한 판단, 높은 정확도 요구, 근거 설명 필요
    단점: 출력 토큰 증가, 지연 시간 증가, 비용 상승
    """
    messages = [
        {
            "role": "user",
            "content": (
                f"다음 리뷰를 단계별로 분석하여 긍정/부정/중립으로 분류하라.\n\n"
                f"리뷰: {review}\n\n"
                f"1단계: 리뷰에서 긍정적 표현을 추출하라\n"
                f"2단계: 리뷰에서 부정적 표현을 추출하라\n"
                f"3단계: 긍정과 부정의 비중을 비교하라\n"
                f"4단계: 최종 분류를 결정하라 (긍정/부정/중립)"
            ),
        }
    ]
    return measure_call("cot", messages)


def structured_output(review: str) -> dict:
    """
    Structured Output (Tool Use): JSON Schema로 응답 형식을 강제한다.

    적합 상황: Agent에서 LLM 출력을 다음 로직의 입력으로 사용할 때
    장점: 파싱 안정성 높음, 스키마 위반 응답 거의 없음
    """
    tools = [
        {
            "name": "classify_review",
            "description": (
                "고객 리뷰를 분류하고 결과를 반환한다. "
                "카테고리, 신뢰도, 분류 이유를 포함한다."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["긍정", "부정", "중립"],
                        "description": "리뷰의 전체적인 감정 분류",
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0.0,
                        "maximum": 1.0,
                        "description": "분류 결과에 대한 신뢰도 (0.0 ~ 1.0)",
                    },
                    "reason": {
                        "type": "string",
                        "description": "분류 이유를 1문장으로 설명",
                    },
                },
                "required": ["category", "confidence", "reason"],
            },
        }
    ]

    start = time.time()
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        tools=tools,
        tool_choice={"type": "tool", "name": "classify_review"},
        messages=[{"role": "user", "content": f"리뷰를 분류하라: {review}"}],
    )
    elapsed = time.time() - start

    # Tool Use 결과 추출
    result = {}
    for block in response.content:
        if block.type == "tool_use":
            result = block.input
            break

    return {
        "strategy": "structured-output",
        "response": json.dumps(result, ensure_ascii=False),
        "parsed": result,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "latency_ms": round(elapsed * 1000),
    }


def print_result(result: dict) -> None:
    """결과를 보기 좋게 출력한다."""
    print(f"\n[{result['strategy'].upper()}]")
    response_preview = result["response"][:100]
    if len(result["response"]) > 100:
        response_preview += "..."
    print(f"  응답: {response_preview}")
    print(f"  입력 토큰: {result['input_tokens']}")
    print(f"  출력 토큰: {result['output_tokens']}")
    print(f"  지연: {result['latency_ms']}ms")


def print_summary(results: list) -> None:
    """세 전략의 비교 요약을 출력한다."""
    print("\n" + "=" * 55)
    print("전략 비교 요약")
    print("=" * 55)
    print(f"{'전략':<18} {'입력토큰':>8} {'출력토큰':>8} {'지연(ms)':>10}")
    print("-" * 55)
    for r in results:
        print(
            f"{r['strategy']:<18} "
            f"{r['input_tokens']:>8} "
            f"{r['output_tokens']:>8} "
            f"{r['latency_ms']:>10}"
        )

    # 비용 효율 분석
    print("\n비용 효율 분석:")
    baseline = results[0]["input_tokens"] + results[0]["output_tokens"]
    for r in results:
        total_tokens = r["input_tokens"] + r["output_tokens"]
        ratio = total_tokens / baseline if baseline > 0 else 1.0
        print(f"  {r['strategy']}: 총 {total_tokens} 토큰 (기준 대비 {ratio:.1f}x)")


def main():
    review = REVIEWS[0]
    print(f"분석 대상 리뷰: {review}\n")
    print("=" * 55)

    results = []

    # Zero-shot
    zs = zero_shot(review)
    print_result(zs)
    results.append(zs)

    # Few-shot
    fs = few_shot(review)
    print_result(fs)
    results.append(fs)

    # CoT
    cot = chain_of_thought(review)
    print_result(cot)
    results.append(cot)

    # 요약
    print_summary(results)

    # Structured Output
    print("\n" + "=" * 55)
    print("Structured Output (Tool Use)")
    print("=" * 55)
    so = structured_output(review)
    print_result(so)
    if "parsed" in so:
        parsed = so["parsed"]
        print(f"\n  파싱된 결과:")
        print(f"    카테고리: {parsed.get('category', 'N/A')}")
        print(f"    신뢰도: {parsed.get('confidence', 0):.0%}")
        print(f"    이유: {parsed.get('reason', 'N/A')}")

    # 전략 선택 가이드
    print("\n" + "=" * 55)
    print("전략 선택 가이드 (이 실습 기준)")
    print("=" * 55)
    zs_total = zs["input_tokens"] + zs["output_tokens"]
    fs_total = fs["input_tokens"] + fs["output_tokens"]
    cot_total = cot["input_tokens"] + cot["output_tokens"]

    print(f"  비용 효율: zero-shot ({zs_total}t) < few-shot ({fs_total}t) < cot ({cot_total}t)")
    print("  정확도:    zero-shot < few-shot ≤ cot")
    print("  형식 안정: structured-output이 가장 안정적")
    print("\n  권장:")
    print("    단순 분류 + 비용 우선  → zero-shot")
    print("    형식 일관성 중요       → few-shot")
    print("    복잡한 추론 필요       → cot")
    print("    Agent 다음 단계 입력   → structured-output")


if __name__ == "__main__":
    main()
