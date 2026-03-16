"""
WE DO: Function Calling Agent - 함께 실습

강사와 함께 cancel_order Tool을 추가하고 Agent 루프를 완성합니다.
"""

import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_orders",
            "description": (
                "고객 ID로 주문 이력을 조회합니다. "
                "최근 주문부터 반환합니다. "
                "주문 취소/환불 전 주문 상태 확인에 사용하세요."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "고객 ID"},
                    "limit": {"type": "integer", "description": "최대 반환 수"},
                },
                "required": ["customer_id"],
            },
        },
    },
    # TODO: cancel_order Tool을 추가하세요
    # - name: "cancel_order"
    # - description: 주문 취소. 배송 완료 주문은 취소 불가. 취소 가능 여부 확인 후 사용.
    # - parameters: order_id (required), reason (optional)
]


def execute_tool(name: str, args: dict) -> dict:
    if name == "search_orders":
        return {
            "orders": [
                {"order_id": "ORD-001", "status": "processing", "amount": 50000},
                {"order_id": "ORD-002", "status": "delivered", "amount": 30000},
            ]
        }
    # TODO: cancel_order 처리 로직을 추가하세요
    # - order_id가 "ORD-002"이면 status가 "delivered"이므로 취소 불가 반환
    # - 나머지는 취소 성공 반환
    return {"error": f"Unknown tool: {name}"}


def run_agent(user_message: str) -> str:
    messages = [
        {"role": "system", "content": "당신은 고객 지원 Agent입니다."},
        {"role": "user", "content": user_message},
    ]

    # TODO: Tool 호출이 없을 때까지 반복하는 while 루프를 구현하세요
    # 1. LLM 호출 (tools, tool_choice="auto" 포함)
    # 2. tool_calls가 없으면 content 반환
    # 3. tool_calls가 있으면 각 Tool을 실행하고 결과를 messages에 추가
    return "TODO: 구현 필요"


if __name__ == "__main__":
    print(run_agent("CUST-123의 주문을 확인하고 ORD-001을 취소해주세요"))
