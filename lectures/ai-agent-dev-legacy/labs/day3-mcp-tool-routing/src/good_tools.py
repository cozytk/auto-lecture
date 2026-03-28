"""
시연용: 잘 설계된 Tool 정의 예시

bad_tools.py와 동일한 쿼리에서 정확도를 비교합니다.
강사 시연용 — 학생은 agent.py를 참고하여 자신의 코드를 작성하세요.
"""

import json
import os
import time
import asyncio
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ── 좋은 Tool 정의 (완전한 스키마) ────────────────────────
GOOD_TOOLS = [
    {
        "name": "get_current_weather",
        "description": (
            "사용자가 특정 도시의 현재 날씨(온도, 습도, 상태)를 요청할 때 호출. "
            "날씨 예보(내일, 주간 등 미래 날씨)가 필요하면 get_weather_forecast를 사용. "
            "검색이나 일반 정보 조회는 search_web을 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "도시명 (영문 또는 한글). 예: Seoul, 서울, Tokyo, 도쿄",
                    "examples": ["Seoul", "서울", "New York", "도쿄"]
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "celsius",
                    "description": "온도 단위. 기본값: celsius"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_weather_forecast",
        "description": (
            "사용자가 특정 도시의 미래 날씨 예보(내일, 이번 주, N일 후 등)를 요청할 때 호출. "
            "현재 날씨(지금, 오늘 현재)가 필요하면 get_current_weather를 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "도시명 (영문 또는 한글). 예: Busan, 부산",
                    "examples": ["Busan", "부산", "London"]
                },
                "days": {
                    "type": "integer",
                    "description": "예보 일수 (1~14). 1이면 내일, 7이면 1주일 예보",
                    "minimum": 1,
                    "maximum": 14,
                    "default": 3
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "celsius"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_web",
        "description": (
            "최신 정보, 사실 확인, 일반 지식 검색이 필요할 때 호출. "
            "날씨 정보는 get_current_weather 또는 get_weather_forecast를 사용. "
            "최신 뉴스, 제품 정보, 기술 문서 등을 찾을 때 이 Tool을 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색 쿼리. 구체적일수록 정확한 결과를 반환. 예: 'Python 3.13 새 기능'",
                    "examples": ["Python 3.13 새 기능", "삼성전자 최신 스마트폰", "2026년 AI 트렌드"]
                },
                "max_results": {
                    "type": "integer",
                    "description": "반환할 최대 결과 수 (1~10). 기본값: 5",
                    "minimum": 1,
                    "maximum": 10,
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
]


# ── Mock Tool 실행 ─────────────────────────────────────────
def execute_tool(name: str, input_data: dict) -> dict:
    """실제 API 대신 Mock 데이터 반환"""
    if name == "get_current_weather":
        return {
            "city": input_data.get("city"),
            "temperature": 23,
            "humidity": 65,
            "condition": "맑음",
            "unit": input_data.get("unit", "celsius")
        }
    elif name == "get_weather_forecast":
        return {
            "city": input_data.get("city"),
            "days": input_data.get("days", 3),
            "forecast": [
                {"day": i + 1, "high": 25 - i, "low": 15, "condition": "구름"}
                for i in range(input_data.get("days", 3))
            ]
        }
    elif name == "search_web":
        return {
            "query": input_data.get("query"),
            "results": [
                {"title": f"결과 {i+1}", "url": f"https://example.com/{i+1}"}
                for i in range(input_data.get("max_results", 5))
            ]
        }
    return {"error": f"알 수 없는 Tool: {name}"}


# ── Fallback 체인 ──────────────────────────────────────────
_cache: dict = {}

def get_data_with_fallback(city: str) -> dict:
    """Fallback 체인 시연"""
    # 1차: 실시간 API (Mock)
    try:
        # 실제로는 외부 API 호출
        result = execute_tool("get_current_weather", {"city": city})
        _cache[city] = result  # 성공 시 캐시 저장
        return {"source": "api", "data": result}
    except Exception as e:
        print(f"  [Fallback] API 실패: {e}")

    # 2차: 캐시
    if city in _cache:
        return {"source": "cache", "data": _cache[city]}

    # 3차: 기본값
    return {
        "source": "default",
        "data": {"city": city, "status": "unavailable", "message": "날씨 정보를 현재 조회할 수 없습니다."}
    }


# ── Agent 실행 ─────────────────────────────────────────────
def run_with_good_tools(query: str) -> dict:
    """잘 설계된 Tool 정의로 Agent 실행"""
    messages = [{"role": "user", "content": query}]
    tools_called = []

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            tools=GOOD_TOOLS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            break

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tools_called.append({"name": block.name, "input": block.input})
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return {
        "query": query,
        "tools_called": tools_called,
        "stop_reason": response.stop_reason
    }


# ── 테스트 케이스 (bad_tools.py와 동일) ───────────────────
TEST_QUERIES = [
    {"query": "서울 지금 날씨 알려줘", "expected_tool": "get_current_weather"},
    {"query": "내일 부산 날씨 예보 알려줘", "expected_tool": "get_weather_forecast"},
    {"query": "파이썬 최신 버전이 뭐야?", "expected_tool": "search_web"},
]


def main():
    print("=" * 60)
    print("시연: 잘 설계된 Tool 정의의 효과")
    print("=" * 60)

    correct = 0
    for case in TEST_QUERIES:
        result = run_with_good_tools(case["query"])
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

    print("\n" + "=" * 60)
    print("시연: Fallback 체인")
    print("=" * 60)
    result = get_data_with_fallback("서울")
    print(f"소스: {result['source']}")
    print(f"데이터: {result['data']}")


if __name__ == "__main__":
    main()
