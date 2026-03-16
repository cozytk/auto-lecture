"""
WE DO: Structured Output - AgentAction 스키마 완성

강사와 함께 TODO를 채워가며 실습합니다.
"""

import os
from enum import Enum
from pydantic import BaseModel, Field
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")


class ActionType(str, Enum):
    SEARCH = "search"
    RESPOND = "respond"
    ESCALATE = "escalate"
    CREATE_TICKET = "create_ticket"


class AgentAction(BaseModel):
    thought: str = Field(description="현재 상황 분석")
    action_type: ActionType = Field(description="선택한 행동")
    # TODO: parameters 필드 추가 (dict 타입, 기본값 빈 dict)
    # TODO: confidence 필드 추가 (float, 0.0~1.0 범위 제약)
    # TODO: reasoning 필드 추가 (str, 이 행동을 선택한 이유)


def decide_action(customer_message: str) -> AgentAction:
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "고객 지원 Agent입니다. 고객 메시지를 분석하고 적절한 행동을 결정하세요.\n"
                    "환불 관련은 반드시 escalate 행동을 선택하세요."
                ),
            },
            {"role": "user", "content": customer_message},
        ],
        response_format=AgentAction,
    )
    return response.choices[0].message.parsed


def validate_agent_action(action: AgentAction) -> tuple[bool, str]:
    """비즈니스 규칙 검증"""
    # TODO: 규칙 1 구현 - 높은 confidence(>0.8)에서 escalate는 불필요
    # TODO: 규칙 2 구현 - 환불 관련 thought가 있으면 반드시 escalate
    return True, "Valid"


if __name__ == "__main__":
    test_cases = [
        "주문한 제품 환불하고 싶어요",
        "배송 현황을 알고 싶어요",
        "제품 사용법을 모르겠어요",
    ]

    for msg in test_cases:
        action = decide_action(msg)
        is_valid, reason = validate_agent_action(action)
        print(f"문의: {msg}")
        print(f"행동: {action.action_type}, 검증: {'통과' if is_valid else '실패'} ({reason})")
        print()
