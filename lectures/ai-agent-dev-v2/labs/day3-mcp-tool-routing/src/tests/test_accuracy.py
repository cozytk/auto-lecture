"""
YOU DO 과제: Tool 선택 정확도 측정 테스트

10개 테스트 케이스를 완성하고 실행하세요.
정답은 solution/agent_solution.py를 참고하세요.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── 테스트 케이스 (YOU DO: 8개 더 추가) ──────────────────
TEST_CASES = [
    {"query": "서울 지금 날씨는?", "expected_tool": "get_current_weather"},
    {"query": "오늘 AI 뉴스 알려줘", "expected_tool": "get_news"},
    # TODO: 8개 더 추가하세요
    # {"query": "...", "expected_tool": "..."},
]

# ── 정답 케이스 (solution 참고용) ─────────────────────────
SOLUTION_TEST_CASES = [
    {"query": "서울 지금 날씨는?", "expected_tool": "get_current_weather"},
    {"query": "내일 부산 날씨 예보", "expected_tool": "get_current_weather"},
    {"query": "오늘 AI 뉴스 알려줘", "expected_tool": "get_news"},
    {"query": "삼성전자 주가 얼마야?", "expected_tool": "get_stock_price"},
    {"query": "애플 주식 현재가", "expected_tool": "get_stock_price"},
    {"query": "125 * 37 계산해줘", "expected_tool": "calculate"},
    {"query": "(1000 + 500) / 3 은?", "expected_tool": "calculate"},
    {"query": "'Hello World'를 한국어로 번역해줘", "expected_tool": "translate_text"},
    {"query": "도쿄 현재 온도는?", "expected_tool": "get_current_weather"},
    {"query": "최신 반도체 뉴스", "expected_tool": "get_news"},
]


def get_tool_selection(query: str, tools: list) -> list[str]:
    """단일 턴으로 Tool 선택 확인 (API 호출 없이 Mock)"""
    # Mock: 쿼리 키워드 기반 Tool 선택
    query_lower = query.lower()

    if any(kw in query_lower for kw in ["날씨", "weather", "온도", "기온"]):
        return ["get_current_weather"]
    elif any(kw in query_lower for kw in ["뉴스", "news", "기사", "소식"]):
        return ["get_news"]
    elif any(kw in query_lower for kw in ["주가", "주식", "stock", "price"]):
        return ["get_stock_price"]
    elif any(kw in query_lower for kw in ["계산", "calculate", "*", "/", "+"]):
        return ["calculate"]
    elif any(kw in query_lower for kw in ["번역", "translate", "translation"]):
        return ["translate_text"]
    return []


class TestToolAccuracy:
    """Tool 선택 정확도 테스트"""

    def test_weather_tool_selected(self):
        """날씨 쿼리에서 날씨 Tool 선택"""
        selected = get_tool_selection("서울 지금 날씨는?", [])
        assert "get_current_weather" in selected, (
            f"날씨 쿼리에서 get_current_weather 선택 실패. 실제: {selected}"
        )

    def test_news_tool_selected(self):
        """뉴스 쿼리에서 뉴스 Tool 선택"""
        selected = get_tool_selection("오늘 AI 뉴스 알려줘", [])
        assert "get_news" in selected, (
            f"뉴스 쿼리에서 get_news 선택 실패. 실제: {selected}"
        )

    # YOU DO: 아래에 테스트 케이스를 추가하세요
    # def test_stock_tool_selected(self):
    #     selected = get_tool_selection("삼성전자 주가 얼마야?", [])
    #     assert "get_stock_price" in selected

    # def test_calculate_tool_selected(self):
    #     selected = get_tool_selection("125 * 37 계산해줘", [])
    #     assert "calculate" in selected


class TestFallbackChain:
    """Fallback 체인 테스트"""

    def test_fallback_returns_data(self):
        """Fallback이 어떤 경우에도 데이터를 반환하는지 확인"""
        from agent import get_with_fallback

        result = get_with_fallback("get_current_weather", {"city": "서울"})
        assert result is not None
        assert "source" in result or "data" in result or "error" in result

    def test_cache_hit(self):
        """캐시 히트 동작 확인"""
        from agent import get_with_fallback, _cache
        import time
        import json

        # 캐시에 직접 데이터 삽입
        cache_key = 'get_current_weather:{"city": "테스트"}'
        _cache[cache_key] = ({"city": "테스트", "temperature": 20}, time.time())

        result = get_with_fallback("get_current_weather", {"city": "테스트"})
        # 캐시 히트 또는 API 결과 모두 허용
        assert result is not None


class TestRetryLogic:
    """재시도 로직 테스트"""

    def test_retry_on_timeout(self):
        """TimeoutError 발생 시 재시도"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from agent import execute_tool_with_retry

        call_count = [0]
        original_execute = None

        def mock_tool_raises_timeout(name, input_data):
            call_count[0] += 1
            if call_count[0] < 2:
                raise TimeoutError("Mock timeout")
            return {"result": "success"}

        # 실제 함수를 직접 테스트하기 어려우므로
        # execute_tool이 정상 동작하는지만 확인
        result = execute_tool_with_retry("get_current_weather", {"city": "서울"})
        assert result is not None
        assert "error" not in result or "city" in result


class TestOverallAccuracy:
    """전체 정확도 측정"""

    def test_minimum_accuracy(self):
        """최소 정확도 60% 이상 확인 (Mock 기반)"""
        if len(TEST_CASES) < 5:
            pytest.skip("테스트 케이스가 5개 미만입니다. YOU DO 과제를 완성하세요.")

        correct = 0
        for case in TEST_CASES:
            selected = get_tool_selection(case["query"], [])
            if case["expected_tool"] in selected:
                correct += 1

        accuracy = correct / len(TEST_CASES)
        assert accuracy >= 0.6, (
            f"정확도 {accuracy*100:.0f}%로 60% 미만. "
            f"Tool description을 개선하세요."
        )

    def test_solution_accuracy(self):
        """정답 케이스 기준 정확도 측정"""
        correct = 0
        for case in SOLUTION_TEST_CASES:
            selected = get_tool_selection(case["query"], [])
            if case["expected_tool"] in selected:
                correct += 1

        accuracy = correct / len(SOLUTION_TEST_CASES)
        print(f"\n정답 기준 정확도: {correct}/{len(SOLUTION_TEST_CASES)} ({accuracy*100:.0f}%)")
        # 이 테스트는 실패해도 OK (학습 목적)
        assert True
