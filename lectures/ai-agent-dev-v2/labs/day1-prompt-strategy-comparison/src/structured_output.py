"""
Structured Output 실습 템플릿 (WE DO)
강사와 함께 Tool Use 방식 Structured Output을 구현한다.
"""

import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

REVIEW = "배송이 빠르긴 했는데 포장이 엉망이었어요."


# ─── 단계 1: JSON Schema 설계 ─────────────────────────────────────────────────

# TODO: 분류 결과를 담을 JSON Schema를 완성하세요
CLASSIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": [],  # TODO: "긍정", "부정", "중립" 추가
            "description": "",  # TODO: 설명 추가
        },
        "confidence": {
            # TODO: 타입과 범위(minimum, maximum) 추가
        },
        "reason": {
            # TODO: 타입과 설명 추가
        },
    },
    "required": [],  # TODO: 필수 필드 추가
}


# ─── 단계 2: Tool 정의 ────────────────────────────────────────────────────────

# TODO: Tool 정의를 완성하세요
tools = [
    {
        "name": "classify_review",
        "description": "",  # TODO: 언제 이 Tool을 사용하는지 설명
        "input_schema": CLASSIFY_SCHEMA,
    }
]


# ─── 단계 3: API 호출 ─────────────────────────────────────────────────────────

def classify_with_tool(review: str) -> dict:
    """Tool Use로 리뷰를 분류한다."""
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

    # TODO: response.content에서 tool_use 블록을 찾아 .input 반환
    for block in response.content:
        pass  # TODO: block.type == "tool_use" 조건 처리

    return {}  # TODO: 올바른 값 반환


# ─── 단계 4: 에러 처리 추가 ──────────────────────────────────────────────────

def safe_classify(review: str) -> dict:
    """에러 처리가 포함된 안전한 분류 함수."""
    try:
        result = classify_with_tool(review)
        # TODO: result 유효성 검증 (required 필드 존재 여부)
        return result
    except Exception as e:
        # TODO: 에러 발생 시 기본값 반환
        print(f"분류 실패: {e}")
        return {
            "category": "중립",
            "confidence": 0.0,
            "reason": f"분류 실패: {str(e)}",
        }


def main():
    print(f"리뷰: {REVIEW}\n")

    result = safe_classify(REVIEW)

    print("분류 결과:")
    print(f"  카테고리: {result.get('category', 'N/A')}")
    print(f"  신뢰도: {result.get('confidence', 0):.0%}")
    print(f"  이유: {result.get('reason', 'N/A')}")
    print(f"\nJSON 출력:\n{json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    main()
