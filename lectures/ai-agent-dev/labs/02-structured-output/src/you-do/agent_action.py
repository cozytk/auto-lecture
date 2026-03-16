"""
YOU DO: Structured Output - 독립 과제

AgentAction 스키마를 완성하고 5가지 고객 시나리오에 적용하세요.
비즈니스 규칙 검증 함수도 구현하세요.
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

test_scenarios = [
    "주문한 제품 환불하고 싶어요",
    "배송이 3일째 안 왔어요",
    "제품 사용법을 모르겠어요. 매뉴얼 있나요?",
    "앱이 자꾸 튕겨요. 어떻게 해야 하나요?",
    "이미 두 번 문의했는데 해결이 안 됐어요",
]


class ActionType(str, Enum):
    SEARCH = "search"
    RESPOND = "respond"
    ESCALATE = "escalate"
    CREATE_TICKET = "create_ticket"


class AgentAction(BaseModel):
    thought: str = Field(description="현재 상황 분석")
    action_type: ActionType = Field(description="선택한 행동")
    # TODO: parameters 필드 추가 (dict 타입, 기본값 빈 dict)
    # TODO: confidence 필드 추가 (float, ge=0.0, le=1.0)
    # TODO: reasoning 필드 추가 (str, 이 행동을 선택한 이유)


def decide_action(customer_message: str) -> AgentAction:
    # TODO: client.beta.chat.completions.parse를 사용해 AgentAction을 반환하세요
    # 시스템 프롬프트에 "환불 관련은 반드시 escalate" 규칙을 포함하세요
    pass


def validate_agent_action(action: AgentAction) -> tuple[bool, str]:
    """
    비즈니스 규칙 검증 함수를 구현하세요.

    규칙 1: confidence > 0.8이면서 action_type == ESCALATE이면 불필요한 에스컬레이션
    규칙 2: thought에 "환불"이 포함되면 action_type은 반드시 ESCALATE이어야 한다
    """
    # TODO: 규칙 1 구현
    # TODO: 규칙 2 구현
    return True, "Valid"


def run_scenarios() -> None:
    print("=== AgentAction 스키마 검증 결과 ===\n")
    for msg in test_scenarios:
        action = decide_action(msg)
        if action is None:
            print(f"문의: {msg}\n결과: 미구현\n")
            continue

        is_valid, reason = validate_agent_action(action)
        status = "통과" if is_valid else f"실패: {reason}"
        print(f"문의: {msg}")
        print(f"  행동: {action.action_type.value}")
        print(f"  검증: {status}")
        print()


if __name__ == "__main__":
    run_scenarios()
