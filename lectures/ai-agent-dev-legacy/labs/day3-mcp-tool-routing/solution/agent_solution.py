"""
정답 코드: Multi-tool Agent 완성본

YOU DO 과제를 마친 후 참고하세요.
"""

import json
import os
import time
from typing import Any
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ── 완성된 Tool 정의 ───────────────────────────────────────
TOOLS = [
    {
        "name": "get_current_weather",
        "description": (
            "사용자가 특정 도시의 현재 날씨(온도, 습도, 날씨 상태)를 요청할 때 호출. "
            "날씨 예보(내일, 이번 주 등 미래 날씨)는 get_weather_forecast를 사용. "
            "뉴스나 일반 정보 검색은 get_news를 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "도시명 (영문 또는 한글). 예: Seoul, 서울, Tokyo",
                    "examples": ["Seoul", "서울", "New York", "도쿄", "London"]
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
        "name": "get_news",
        "description": (
            "특정 주제에 대한 최신 뉴스나 기사를 검색할 때 호출. "
            "날씨 정보는 get_current_weather를 사용. "
            "수식 계산은 calculate를 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "검색할 뉴스 주제. 구체적일수록 좋음. 예: 'AI 반도체', '삼성전자'",
                    "examples": ["AI 반도체", "삼성전자", "Python 3.13", "2026 World Cup"]
                },
                "max_results": {
                    "type": "integer",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 10,
                    "description": "반환할 최대 뉴스 수 (1~10). 기본값: 5"
                }
            },
            "required": ["topic"]
        }
    },
    {
        "name": "calculate",
        "description": (
            "수식 계산이 필요할 때 호출. "
            "사칙연산, 괄호, 소수점 지원. "
            "날씨나 뉴스 조회는 해당 전용 Tool을 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "계산할 수식. 숫자와 연산자(+,-,*,/,())만 사용 가능. 예: '(100 + 200) * 3'",
                    "examples": ["2 + 3", "(100 + 200) * 3", "1234 / 56.7"]
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_stock_price",
        "description": (
            "특정 주식 종목의 현재 가격 및 등락률을 조회할 때 호출. "
            "뉴스나 일반 정보는 get_news를 사용. "
            "날씨 정보는 get_current_weather를 사용."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "주식 종목 코드 또는 회사명. 예: SAMSUNG, 005930, AAPL, Apple",
                    "examples": ["SAMSUNG", "005930", "AAPL", "Apple", "TSLA"]
                },
                "exchange": {
                    "type": "string",
                    "enum": ["KRX", "NYSE", "NASDAQ", "AUTO"],
                    "default": "AUTO",
                    "description": "거래소. AUTO면 자동 감지. KRX: 한국, NYSE/NASDAQ: 미국"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "translate_text",
        "description": (
            "텍스트를 다른 언어로 번역할 때 호출. "
            "번역이 필요하지 않은 일반 질문에는 사용하지 말 것."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "번역할 원문 텍스트"
                },
                "target_language": {
                    "type": "string",
                    "description": "번역 대상 언어. 예: Korean, English, Japanese, Chinese",
                    "examples": ["Korean", "English", "Japanese", "Chinese", "Spanish"]
                },
                "source_language": {
                    "type": "string",
                    "description": "원문 언어. 비워두면 자동 감지",
                    "default": "auto"
                }
            },
            "required": ["text", "target_language"]
        }
    }
]


# ── Mock 실행 함수 ─────────────────────────────────────────
def _mock_weather(city: str, unit: str = "celsius") -> dict:
    return {
        "city": city, "temperature": 22, "humidity": 60,
        "condition": "맑음", "unit": unit,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def _mock_news(topic: str, max_results: int = 5) -> dict:
    return {
        "topic": topic,
        "articles": [
            {"title": f"{topic} 뉴스 {i+1}", "summary": f"{topic} 관련 최신 소식 {i+1}.",
             "url": f"https://news.example.com/{i+1}"}
            for i in range(max_results)
        ]
    }

def _mock_calculate(expression: str) -> dict:
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return {"error": "허용되지 않는 문자"}
        result = eval(expression)  # noqa: S307
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}

def _mock_stock(symbol: str, exchange: str = "AUTO") -> dict:
    prices = {"SAMSUNG": 75000, "AAPL": 195.0, "TSLA": 248.0}
    price = prices.get(symbol.upper(), 100.0)
    return {
        "symbol": symbol, "exchange": exchange,
        "price": price, "change": +1.5, "change_pct": "+2.0%",
        "currency": "KRW" if exchange == "KRX" else "USD"
    }

def _mock_translate(text: str, target_language: str, source_language: str = "auto") -> dict:
    return {
        "original": text, "translated": f"[{target_language} 번역] {text}",
        "source_language": source_language, "target_language": target_language
    }


def execute_tool(name: str, input_data: dict) -> Any:
    tool_map = {
        "get_current_weather": lambda: _mock_weather(
            input_data.get("city", ""), input_data.get("unit", "celsius")),
        "get_news": lambda: _mock_news(
            input_data.get("topic", ""), input_data.get("max_results", 5)),
        "calculate": lambda: _mock_calculate(input_data.get("expression", "")),
        "get_stock_price": lambda: _mock_stock(
            input_data.get("symbol", ""), input_data.get("exchange", "AUTO")),
        "translate_text": lambda: _mock_translate(
            input_data.get("text", ""),
            input_data.get("target_language", "Korean"),
            input_data.get("source_language", "auto")),
    }
    fn = tool_map.get(name)
    if fn is None:
        return {"error": f"알 수 없는 Tool: {name}"}
    return fn()


def execute_tool_with_retry(name: str, input_data: dict, max_retries: int = 3) -> Any:
    for attempt in range(max_retries):
        try:
            return execute_tool(name, input_data)
        except TimeoutError:
            if attempt == max_retries - 1:
                return {"error": f"Tool '{name}' 응답 시간 초과"}
            time.sleep(2 ** attempt)
        except Exception as e:
            return {"error": str(e)}
    return {"error": "최대 재시도 초과"}


# ── Fallback 체인 ──────────────────────────────────────────
_cache: dict[str, tuple[Any, float]] = {}

def get_with_fallback(tool_name: str, args: dict, ttl: int = 300) -> dict:
    cache_key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"

    # 1차: 실시간 Tool 호출
    try:
        result = execute_tool_with_retry(tool_name, args)
        if "error" not in result:
            _cache[cache_key] = (result, time.time())
            return {"source": "api", "data": result}
    except Exception:
        pass

    # 2차: 캐시 조회
    if cache_key in _cache:
        value, ts = _cache[cache_key]
        if time.time() - ts < ttl:
            return {"source": "cache", "data": value}

    # 3차: 기본값
    return {"source": "default", "data": {"status": "unavailable"}}


# ── Agent 루프 ─────────────────────────────────────────────
def run_agent(user_message: str, verbose: bool = True) -> str:
    messages = [{"role": "user", "content": user_message}]

    if verbose:
        print(f"\n질문: {user_message}")
        print("-" * 40)

    for iteration in range(10):
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages
        )

        if verbose:
            print(f"[{iteration+1}] stop_reason: {response.stop_reason}")

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if verbose:
                    print(f"  Tool: {block.name}({block.input})")
                result = execute_tool_with_retry(block.name, block.input)
                if verbose:
                    print(f"  결과: {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return "최대 반복 횟수 초과"


# ── 정확도 측정 ────────────────────────────────────────────
TEST_CASES = [
    {"query": "서울 지금 날씨는?", "expected_tool": "get_current_weather"},
    {"query": "내일 부산 날씨 예보", "expected_tool": "get_current_weather"},  # 예보도 날씨
    {"query": "오늘 AI 뉴스 알려줘", "expected_tool": "get_news"},
    {"query": "삼성전자 주가 얼마야?", "expected_tool": "get_stock_price"},
    {"query": "애플 주식 현재가", "expected_tool": "get_stock_price"},
    {"query": "125 * 37 계산해줘", "expected_tool": "calculate"},
    {"query": "(1000 + 500) / 3 은?", "expected_tool": "calculate"},
    {"query": "'Hello World'를 한국어로 번역해줘", "expected_tool": "translate_text"},
    {"query": "도쿄 현재 온도는?", "expected_tool": "get_current_weather"},
    {"query": "최신 반도체 뉴스", "expected_tool": "get_news"},
]


def measure_accuracy() -> float:
    correct = 0
    print("\nTool 선택 정확도 측정")
    print("=" * 60)
    for case in TEST_CASES:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=256,
            tools=TOOLS,
            messages=[{"role": "user", "content": case["query"]}]
        )
        selected = [b.name for b in response.content if b.type == "tool_use"]
        ok = case["expected_tool"] in selected
        if ok:
            correct += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {case['query']:<35} → {selected}")

    acc = correct / len(TEST_CASES)
    print(f"\n정확도: {correct}/{len(TEST_CASES)} ({acc*100:.0f}%)")
    return acc


if __name__ == "__main__":
    # 기본 동작
    answer = run_agent("서울 날씨와 삼성전자 주가, 그리고 오늘 AI 뉴스를 알려줘")
    print(f"\n답변:\n{answer}")

    print("\n" + "=" * 60)
    measure_accuracy()
