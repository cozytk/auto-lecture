"""
WE DO + YOU DO: Multi-tool Agent 구현 스캐폴드

강사와 함께 빈 칸을 채워나갑니다.
TODO 주석을 찾아 구현하세요.
"""

import json
import os
import asyncio
import time
from typing import Any

def _get_client():
    """anthropic 클라이언트를 지연 초기화 (테스트 환경에서 임포트 오류 방지)"""
    import anthropic  # noqa: PLC0415
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ── Tool 정의 (TODO: description과 parameters를 완성하세요) ───
TOOLS = [
    {
        "name": "get_current_weather",
        # TODO: description을 작성하세요.
        # 힌트: 언제 이 Tool을 쓰는지 + 유사 Tool과의 차이를 명시
        "description": "TODO",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    # TODO: description과 examples 추가
                    "description": "TODO",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "celsius",
                    "description": "온도 단위"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_news",
        # TODO: description 작성 (언제 이 Tool을 쓰는지 명시)
        "description": "TODO",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    # TODO: description과 examples 추가
                    "description": "TODO"
                },
                "max_results": {
                    "type": "integer",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 10,
                    "description": "반환할 최대 뉴스 수"
                }
            },
            "required": ["topic"]
        }
    },
    {
        "name": "calculate",
        # TODO: description 작성 (언제 이 Tool을 쓰는지 명시)
        "description": "TODO",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    # TODO: description과 examples 추가
                    "description": "TODO"
                }
            },
            "required": ["expression"]
        }
    }
    # YOU DO: get_stock_price, translate_text Tool을 추가하세요
]


# ── Mock Tool 실행 함수 ────────────────────────────────────
def _mock_weather(city: str, unit: str = "celsius") -> dict:
    return {
        "city": city,
        "temperature": 22,
        "humidity": 60,
        "condition": "맑음",
        "unit": unit,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def _mock_news(topic: str, max_results: int = 5) -> dict:
    return {
        "topic": topic,
        "articles": [
            {
                "title": f"{topic} 관련 뉴스 {i+1}",
                "summary": f"{topic}에 대한 최신 소식입니다.",
                "url": f"https://news.example.com/{i+1}"
            }
            for i in range(max_results)
        ]
    }


def _mock_calculate(expression: str) -> dict:
    try:
        # 안전한 수식만 허용 (숫자와 연산자만)
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return {"error": "허용되지 않는 문자가 포함되어 있습니다."}
        result = eval(expression)  # noqa: S307
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


def execute_tool(name: str, input_data: dict) -> Any:
    """Tool 이름에 따라 실행 함수 라우팅"""
    tool_map = {
        "get_current_weather": lambda: _mock_weather(
            input_data.get("city", ""),
            input_data.get("unit", "celsius")
        ),
        "get_news": lambda: _mock_news(
            input_data.get("topic", ""),
            input_data.get("max_results", 5)
        ),
        "calculate": lambda: _mock_calculate(
            input_data.get("expression", "")
        ),
        # YOU DO: get_stock_price, translate_text 추가
    }

    fn = tool_map.get(name)
    if fn is None:
        return {"error": f"알 수 없는 Tool: {name}"}
    return fn()


# ── 재시도 패턴 ────────────────────────────────────────────
def execute_tool_with_retry(name: str, input_data: dict, max_retries: int = 3) -> Any:
    """지수 백오프로 재시도"""
    for attempt in range(max_retries):
        try:
            return execute_tool(name, input_data)
        except TimeoutError:
            if attempt == max_retries - 1:
                return {"error": f"Tool '{name}' 응답 시간 초과 (최대 재시도 초과)"}
            wait = 2 ** attempt
            print(f"  [Retry] {attempt+1}/{max_retries} — {wait}초 대기")
            time.sleep(wait)
        except Exception as e:
            return {"error": str(e)}
    return {"error": "최대 재시도 초과"}


# ── Fallback 체인 ──────────────────────────────────────────
_cache: dict[str, tuple[Any, float]] = {}


def get_with_fallback(tool_name: str, args: dict, ttl: int = 300) -> dict:
    """
    Fallback 체인:
    1차: 실시간 Tool 호출
    2차: 캐시 조회
    3차: 기본값 반환

    TODO: 이 함수를 완성하세요
    """
    cache_key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"

    # TODO: 1차 — execute_tool_with_retry 호출
    # 성공 시 캐시에 저장 후 반환

    # TODO: 2차 — 캐시 확인 (TTL 이내면 반환)

    # TODO: 3차 — 기본값 반환
    return {"status": "unavailable", "message": "데이터를 현재 조회할 수 없습니다."}


# ── Agent 루프 ─────────────────────────────────────────────
def run_agent(user_message: str, verbose: bool = True) -> str:
    """
    Multi-tool Agent 루프

    TODO: 빈 칸을 채워 완성하세요
    """
    messages = [{"role": "user", "content": user_message}]

    if verbose:
        print(f"\n질문: {user_message}")
        print("-" * 40)

    iteration = 0
    max_iterations = 10  # 무한루프 방지

    while iteration < max_iterations:
        iteration += 1

        # TODO: client.messages.create 호출
        # model="claude-opus-4-5", max_tokens=4096, tools=TOOLS
        response = None  # TODO

        if verbose and response:
            print(f"[{iteration}] stop_reason: {response.stop_reason}")

        # TODO: stop_reason이 "end_turn"이면 텍스트 응답 반환

        # TODO: Tool 호출 처리
        tool_results = []
        if response:
            for block in response.content:
                if block.type == "tool_use":
                    if verbose:
                        print(f"  Tool 호출: {block.name}({block.input})")

                    # TODO: execute_tool_with_retry로 Tool 실행
                    result = {}  # TODO

                    if verbose:
                        print(f"  Tool 결과: {result}")

                    # TODO: tool_result 블록 구성 (tool_use_id 매핑 필수)
                    tool_results.append({})  # TODO

        # TODO: 메시지 히스토리 업데이트
        # messages에 assistant 응답과 tool_results 추가

    return "최대 반복 횟수 초과"


# ── 정확도 측정 ────────────────────────────────────────────
def measure_accuracy(test_cases: list[dict]) -> float:
    """
    Tool 선택 정확도 측정

    test_cases 형식:
    [{"query": "...", "expected_tool": "tool_name"}, ...]
    """
    correct = 0

    for case in test_cases:
        # 단일 턴으로 Tool 선택만 확인
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=256,
            tools=TOOLS,
            messages=[{"role": "user", "content": case["query"]}]
        )

        tools_selected = [
            block.name
            for block in response.content
            if block.type == "tool_use"
        ]

        is_correct = case["expected_tool"] in tools_selected
        if is_correct:
            correct += 1

        status = "PASS" if is_correct else "FAIL"
        print(f"[{status}] {case['query'][:40]:<40} → {tools_selected}")

    accuracy = correct / len(test_cases) if test_cases else 0
    print(f"\n정확도: {correct}/{len(test_cases)} ({accuracy*100:.0f}%)")
    return accuracy


if __name__ == "__main__":
    # 기본 동작 테스트
    result = run_agent("서울 날씨와 오늘 AI 뉴스를 알려줘")
    print(f"\n최종 답변:\n{result}")
