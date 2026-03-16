"""
Structured Output 정답 코드
Tool Use 방식으로 JSON Schema를 강제하여 안정적인 구조화 응답을 받는다.
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

REVIEW = "배송이 빠르긴 했는데 포장이 엉망이었어요."

# ─── JSON Schema 정의 ─────────────────────────────────────────────────────────

CLASSIFY_SCHEMA = {
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
            "description": "분류 결과에 대한 신뢰도 (0.0이 낮음, 1.0이 높음)",
        },
        "reason": {
            "type": "string",
            "description": "분류 이유를 1문장으로 설명한다",
        },
    },
    "required": ["category", "confidence", "reason"],
}

# ─── Tool 정의 ────────────────────────────────────────────────────────────────

tools = [
    {
        "name": "classify_review",
        "description": (
            "고객 리뷰를 긍정/부정/중립으로 분류하고 결과를 반환한다. "
            "분류 결과와 신뢰도, 이유를 포함한 구조화된 응답을 생성한다."
        ),
        "input_schema": CLASSIFY_SCHEMA,
    }
]


# ─── 핵심 분류 함수 ───────────────────────────────────────────────────────────

def classify_with_tool(review: str) -> dict:
    """
    Tool Use로 리뷰를 분류한다.
    tool_choice로 반드시 classify_review Tool을 사용하도록 강제한다.
    """
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        tools=tools,
        tool_choice={"type": "tool", "name": "classify_review"},
        messages=[
            {
                "role": "user",
                "content": f"다음 리뷰를 분류하라: {review}",
            }
        ],
    )

    # Tool Use 결과 추출
    for block in response.content:
        if block.type == "tool_use":
            return block.input  # dict 타입으로 바로 반환됨

    raise ValueError("Tool Use 블록을 찾을 수 없습니다")


# ─── 안전한 래퍼 ─────────────────────────────────────────────────────────────

def safe_classify(review: str) -> dict:
    """
    에러 처리가 포함된 안전한 분류 함수.
    실패 시 기본값을 반환하여 Agent 흐름이 중단되지 않도록 한다.
    """
    try:
        result = classify_with_tool(review)

        # 유효성 검증
        required_fields = ["category", "confidence", "reason"]
        missing = [f for f in required_fields if f not in result]
        if missing:
            raise ValueError(f"필수 필드 누락: {missing}")

        # 범위 검증
        if not (0.0 <= result["confidence"] <= 1.0):
            result["confidence"] = max(0.0, min(1.0, result["confidence"]))

        return result

    except Exception as e:
        print(f"[경고] 분류 실패, 기본값 반환: {e}")
        return {
            "category": "중립",
            "confidence": 0.0,
            "reason": f"분류 실패로 인한 기본값: {str(e)}",
        }


# ─── 배치 처리 예시 ───────────────────────────────────────────────────────────

def batch_classify(reviews: list) -> list:
    """
    여러 리뷰를 배치로 분류한다.
    실패한 항목은 기본값으로 대체하여 전체 처리가 중단되지 않는다.
    """
    results = []
    for i, review in enumerate(reviews):
        print(f"  처리 중 {i+1}/{len(reviews)}: {review[:30]}...")
        result = safe_classify(review)
        results.append({"review": review, "classification": result})
    return results


def main():
    # 단일 분류 테스트
    print(f"리뷰: {REVIEW}\n")

    result = safe_classify(REVIEW)

    print("분류 결과:")
    print(f"  카테고리: {result['category']}")
    print(f"  신뢰도: {result['confidence']:.0%}")
    print(f"  이유: {result['reason']}")
    print(f"\nJSON 원본:\n{json.dumps(result, ensure_ascii=False, indent=2)}")

    # 일반 프롬프트 방식과 차이점 설명
    print("\n" + "=" * 50)
    print("Tool Use vs 일반 프롬프트 차이점")
    print("=" * 50)
    print("일반 프롬프트:")
    print('  응답: "이 리뷰는 중립입니다. 배송 속도는 긍정적이지만..."')
    print("  문제: 자연어 파싱 필요, 형식 불안정")
    print()
    print("Tool Use:")
    print('  응답: {"category": "중립", "confidence": 0.7, "reason": "..."}')
    print("  장점: 항상 JSON, 파싱 안정, Agent 다음 단계에 바로 사용 가능")


if __name__ == "__main__":
    main()
