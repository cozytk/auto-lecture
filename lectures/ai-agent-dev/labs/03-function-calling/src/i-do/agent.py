"""
I DO: Function Calling 기반 Agent - 시연 코드

강사가 실행하며 시연합니다. 학생은 관찰하며 이해하세요.

핵심 관찰 포인트:
- LLM은 "어떤 Tool을 어떤 파라미터로 호출할지"만 결정한다
- 실제 Tool 실행은 애플리케이션 코드가 담당한다
- Tool 결과가 다시 LLM에 전달되어 최종 응답이 생성된다
"""

import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# Tool 정의: JSON Schema로 함수 시그니처를 기술한다
# description에 "언제/왜 사용하는지"를 명확히 적는 것이 핵심이다
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_orders",
            "description": (
                "고객 ID로 주문 이력을 조회합니다. "
                "최근 주문부터 반환합니다. "
                "환불/교환 처리 전 주문 상태 확인에 사용하세요."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "고객 고유 식별자 (예: CUST-12345)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "반환할 최대 주문 수. 기본값: 10",
                    },
                },
                "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_detail",
            "description": (
                "주문 ID로 상세 정보를 조회합니다. "
                "배송 상태, 상품 목록, 결제 금액을 포함합니다."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "주문 고유 식별자 (예: ORD-789)",
                    },
                },
                "required": ["order_id"],
            },
        },
    },
]


def execute_tool(name: str, args: dict) -> dict:
    """Tool 실행 - 실제 환경에서는 DB/API를 호출한다."""
    if name == "search_orders":
        return {
            "success": True,
            "orders": [
                {"order_id": "ORD-789", "status": "delivered", "date": "2025-03-01"},
                {"order_id": "ORD-756", "status": "cancelled", "date": "2025-02-15"},
            ],
        }
    if name == "get_order_detail":
        return {
            "order_id": args["order_id"],
            "status": "delivered",
            "items": ["노트북 파우치"],
            "amount": 35000,
            "delivered_at": "2025-03-01",
        }
    return {"success": False, "error": f"Unknown tool: {name}"}


def run_agent(user_message: str) -> str:
    """Function Calling Agent 루프"""
    messages = [
        {"role": "system", "content": "당신은 고객 지원 Agent입니다."},
        {"role": "user", "content": user_message},
    ]

    # Tool 호출이 없어질 때까지 루프 실행
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        assistant_msg = response.choices[0].message

        # Tool 호출이 없으면 최종 응답 반환
        if not assistant_msg.tool_calls:
            return assistant_msg.content

        # Tool 결과를 대화 이력에 추가
        messages.append(assistant_msg)
        for tc in assistant_msg.tool_calls:
            fn_args = json.loads(tc.function.arguments)
            result = execute_tool(tc.function.name, fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False),
            })


if __name__ == "__main__":
    test_queries = [
        "CUST-123 고객의 최근 주문을 확인해주세요",
        "ORD-789 주문 상세 정보를 알려주세요",
        # Tool 호출 없이 직접 답변하는 경우
        "고객 지원 운영 시간이 어떻게 되나요?",
    ]

    for query in test_queries:
        print(f"\n질문: {query}")
        print(f"답변: {run_agent(query)}")
