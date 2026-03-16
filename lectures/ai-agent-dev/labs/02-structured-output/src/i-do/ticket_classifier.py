"""
I DO: Structured Output으로 Agent 행동 결정 - 시연 코드

강사가 실행하며 시연합니다. 학생은 관찰하며 이해하세요.

핵심 관찰 포인트:
- Pydantic 모델이 LLM 출력의 스키마를 강제한다
- JSON 파싱 오류가 원천적으로 발생하지 않는다
- enum 필드가 허용된 값 외에는 생성되지 않는다
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


class Urgency(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TicketClassification(BaseModel):
    """고객 문의 분류 결과 스키마"""

    category: str = Field(
        description="문의 카테고리",
        json_schema_extra={"enum": ["환불", "배송", "제품문의", "기술지원", "기타"]},
    )
    urgency: Urgency = Field(description="긴급도")
    summary: str = Field(description="문의 요약 (1문장)", max_length=100)
    suggested_action: str = Field(description="권장 행동")


def classify_ticket(query: str) -> TicketClassification:
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "고객 문의를 분류하세요."},
            {"role": "user", "content": query},
        ],
        response_format=TicketClassification,
    )
    return response.choices[0].message.parsed


# Agent에서 행동 결정을 구조화하는 예시
class ToolCall(BaseModel):
    tool_name: str = Field(
        description="호출할 도구 이름",
        json_schema_extra={"enum": ["search_db", "send_email", "create_ticket", "escalate"]},
    )
    parameters: dict = Field(description="도구에 전달할 파라미터")
    # 추론 과정을 남겨 감사(audit) 가능하게 한다
    reasoning: str = Field(description="이 도구를 선택한 이유")


class AgentDecision(BaseModel):
    thought: str = Field(description="현재 상황에 대한 분석")
    action: ToolCall = Field(description="실행할 행동")
    is_final: bool = Field(description="이것이 최종 행동인지 여부")


if __name__ == "__main__":
    test_cases = [
        "배송 받았는데 색상이 다르고 환불 원합니다",
        "주문번호 12345 배송이 언제 되나요?",
        "이 제품 방수 기능이 있나요?",
    ]

    print("=== Structured Output 분류 결과 ===\n")
    for query in test_cases:
        result = classify_ticket(query)
        print(f"문의: {query}")
        print(result.model_dump_json(indent=2))
        print()
