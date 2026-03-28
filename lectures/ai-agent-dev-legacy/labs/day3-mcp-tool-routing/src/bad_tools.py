"""
시연용: 모호한 Tool 정의가 선택 정확도에 미치는 영향

이 파일의 Tool 정의는 의도적으로 나쁘게 작성되었습니다.
강사 시연용 — 학생은 수정하지 마세요.
"""

import json
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ── 나쁜 Tool 정의 (의도적으로 모호) ──────────────────────
BAD_TOOLS = [
    {
        "name": "get_current_weather",
        "description": "Gets weather data",  # 너무 짧고 모호
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string"
                    # description, examples 없음
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_weather_forecast",
        "description": "Weather information",  # 현재 날씨와 구분 안 됨
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "days": {"type": "integer"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_web",
        "description": "Search",  # 극도로 모호
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }
]


def mock_tool_call(name: str, input_data: dict) -> dict:
    """Tool 실제 호출 대신 Mock 반환"""
    return {
        "tool_called": name,
        "input": input_data,
        "result": f"[MOCK] {name} 호출됨"
    }


def run_with_bad_tools(query: str) -> dict:
    """모호한 Tool 정의로 Agent 실행"""
    messages = [{"role": "user", "content": query}]

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        tools=BAD_TOOLS,
        messages=messages
    )

    tools_called = []
    for block in response.content:
        if block.type == "tool_use":
            tools_called.append({
                "name": block.name,
                "input": block.input
            })

    return {
        "query": query,
        "tools_called": tools_called,
        "stop_reason": response.stop_reason
    }


# ── 테스트 케이스 ──────────────────────────────────────────
TEST_QUERIES = [
    {
        "query": "서울 지금 날씨 알려줘",
        "expected_tool": "get_current_weather",
    },
    {
        "query": "내일 부산 날씨 예보 알려줘",
        "expected_tool": "get_weather_forecast",
    },
    {
        "query": "파이썬 최신 버전이 뭐야?",
        "expected_tool": "search_web",
    },
]


def main():
    print("=" * 60)
    print("시연: 모호한 Tool 정의의 문제점")
    print("=" * 60)

    correct = 0
    for case in TEST_QUERIES:
        result = run_with_bad_tools(case["query"])
        tools_called = [t["name"] for t in result["tools_called"]]
        is_correct = case["expected_tool"] in tools_called

        status = "PASS" if is_correct else "FAIL"
        if is_correct:
            correct += 1

        print(f"\n[{status}] 쿼리: {case['query']}")
        print(f"  기대 Tool: {case['expected_tool']}")
        print(f"  실제 Tool: {tools_called}")

    accuracy = correct / len(TEST_QUERIES) * 100
    print(f"\n정확도: {correct}/{len(TEST_QUERIES)} ({accuracy:.0f}%)")
    print("\n→ solution/의 good_tools.py와 비교해 보세요!")


if __name__ == "__main__":
    main()
