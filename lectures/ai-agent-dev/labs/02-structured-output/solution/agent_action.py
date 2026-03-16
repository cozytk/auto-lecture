"""
YOU DO 정답: Structured Output - AgentAction 스키마

학생이 과제 완료 후 참고하는 정답 코드입니다.
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
    parameters: dict = Field(default_factory=dict, description="행동 파라미터")
    confidence: float = Field(ge=0.0, le=1.0, description="확신도 (0.0~1.0)")
    reasoning: str = Field(description="이 행동을 선택한 이유")


def decide_action(customer_message: str) -> AgentAction:
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "고객 지원 Agent입니다. 고객 메시지를 분석하고 적절한 행동을 결정하세요.\n"
                    "환불 관련 문의는 반드시 escalate 행동을 선택하세요.\n"
                    "반복 문의나 해결 안 된 경우도 escalate로 처리하세요."
                ),
            },
            {"role": "user", "content": customer_message},
        ],
        response_format=AgentAction,
    )
    return response.choices[0].message.parsed


def validate_agent_action(action: AgentAction) -> tuple[bool, str]:
    """비즈니스 규칙 검증"""
    # 규칙 1: 높은 confidence(>0.8)에서 escalate는 비효율적
    # (확신이 높다는 것은 Agent가 직접 처리 가능하다는 의미)
    if action.action_type == ActionType.ESCALATE and action.confidence > 0.8:
        return False, "높은 confidence에서 escalate는 불필요"

    # 규칙 2: "환불"이 thought에 포함되면 반드시 escalate
    # (환불 처리는 항상 사람 검토 필요)
    if "환불" in action.thought and action.action_type != ActionType.ESCALATE:
        return False, "환불 관련 문의는 escalate 필수"

    return True, "Valid"


def run_scenarios() -> None:
    print("=== AgentAction 스키마 검증 결과 ===\n")
    for msg in test_scenarios:
        action = decide_action(msg)
        is_valid, reason = validate_agent_action(action)
        status = "통과" if is_valid else f"실패: {reason}"
        print(f"문의: {msg}")
        print(f"  행동: {action.action_type.value}, confidence: {action.confidence:.2f}")
        print(f"  이유: {action.reasoning[:60]}...")
        print(f"  검증: {status}")
        print()


if __name__ == "__main__":
    run_scenarios()
