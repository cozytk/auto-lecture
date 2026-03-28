"""
Day 4 실습 - YOU DO: 종합 성능 개선 파이프라인

진단 → 개선 → A/B 테스트 → 리포트 생성의 전체 파이프라인을 구현한다.
TODO 부분을 완성하세요.
"""

import os
import json
from datetime import datetime
from openai import OpenAI


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# =============================================================================
# 1. 성능 진단
# =============================================================================

def diagnose(current_metrics: dict, baseline_metrics: dict, threshold: float = 0.05) -> list[dict]:
    """성능 저하 원인 진단

    TODO: baseline과 current를 비교하여 하락한 메트릭을 찾고,
          영역(prompt/rag/tool)과 심각도(critical/warning/info)를 분류하세요.

    Args:
        current_metrics: 현재 메트릭
        baseline_metrics: 기준 메트릭
        threshold: 허용 하락 폭

    Returns:
        진단 결과 목록 [{"metric": "...", "area": "...", "severity": "...", "drop": 0.0}]
    """
    # TODO: 구현하세요
    pass


# =============================================================================
# 2. Prompt 개선
# =============================================================================

def create_improved_prompt(original_prompt: str, diagnosis: list[dict]) -> str:
    """진단 결과를 기반으로 프롬프트를 개선

    TODO: 진단 결과에서 약한 영역을 파악하고,
          해당 영역을 보완하는 개선된 프롬프트를 작성하세요.

    Args:
        original_prompt: 원본 프롬프트
        diagnosis: 진단 결과

    Returns:
        개선된 프롬프트
    """
    # TODO: 구현하세요
    # 힌트:
    # - diagnosis에서 area가 "prompt"인 항목을 확인
    # - "rag" 영역이면 컨텍스트 활용 지시를 추가
    # - "tool" 영역이면 도구 사용 예시를 추가
    pass


# =============================================================================
# 3. A/B 테스트
# =============================================================================

def run_ab_test(
    prompt_a: str,
    prompt_b: str,
    test_cases: list[dict],
    model: str = "gpt-4o-mini"
) -> dict:
    """A/B 테스트 실행

    TODO: 두 프롬프트를 동일한 테스트 케이스에 실행하고 비교하세요.

    Args:
        prompt_a: 원본 프롬프트 (Version A)
        prompt_b: 개선 프롬프트 (Version B)
        test_cases: 테스트 케이스 목록
        model: 사용할 모델

    Returns:
        A/B 테스트 결과
    """
    # TODO: 구현하세요
    # 힌트:
    # 1. 각 테스트 케이스에 대해 prompt_a, prompt_b로 각각 실행
    # 2. LLM Judge로 각 출력에 0-1 점수 부여
    # 3. 평균 점수, 승패, 개선율 계산
    pass


# =============================================================================
# 4. 개선 리포트 생성
# =============================================================================

def generate_report(
    baseline: dict,
    current: dict,
    diagnosis: list[dict],
    ab_result: dict = None
) -> str:
    """성능 개선 리포트 생성

    TODO: Before/After 비교 리포트를 마크다운 형식으로 생성하세요.

    Args:
        baseline: 기준 메트릭
        current: 현재 메트릭
        diagnosis: 진단 결과
        ab_result: A/B 테스트 결과 (선택)

    Returns:
        마크다운 리포트 문자열
    """
    # TODO: 구현하세요
    pass


# =============================================================================
# 5. 전체 파이프라인
# =============================================================================

def run_optimization_pipeline():
    """종합 성능 개선 파이프라인 실행

    1. 진단: 메트릭 비교
    2. 개선: 프롬프트 수정
    3. 검증: A/B 테스트
    4. 리포트: 결과 출력
    """
    print("=" * 60)
    print("종합 성능 개선 파이프라인")
    print("=" * 60)

    # --- 메트릭 정의 ---
    baseline_metrics = {
        "task_completion_rate": 0.90,
        "f1_score": 0.82,
        "groundedness": 0.85,
        "tool_call_accuracy": 0.88,
    }

    current_metrics = {
        "task_completion_rate": 0.75,
        "f1_score": 0.78,
        "groundedness": 0.62,
        "tool_call_accuracy": 0.85,
    }

    # --- 원본 프롬프트 ---
    original_prompt = """당신은 고객 지원 Agent입니다.
고객의 질문에 답변하세요."""

    # --- 테스트 케이스 ---
    test_cases = [
        {
            "input": "주문번호 ORD-1234 환불하고 싶어요",
            "expected": "환불 절차 안내, 주문 확인"
        },
        {
            "input": "배송이 3일째 안 오는데 어떻게 된 건가요?",
            "expected": "배송 상태 확인, 지연 사과, 예상 일정"
        },
        {
            "input": "이 상품 AS 보증 기간이 어떻게 되나요?",
            "expected": "보증 기간 안내, 관련 정책 설명"
        },
    ]

    # --- Step 1: 진단 ---
    print("\n[Step 1] 성능 진단")
    diagnosis = diagnose(current_metrics, baseline_metrics)
    # TODO: 진단 결과 출력

    # --- Step 2: 개선 ---
    print("\n[Step 2] 프롬프트 개선")
    improved_prompt = create_improved_prompt(original_prompt, diagnosis)
    # TODO: 개선 내용 출력

    # --- Step 3: A/B 테스트 ---
    print("\n[Step 3] A/B 테스트")
    ab_result = run_ab_test(original_prompt, improved_prompt, test_cases)
    # TODO: A/B 결과 출력

    # --- Step 4: 리포트 ---
    print("\n[Step 4] 리포트 생성")
    report = generate_report(baseline_metrics, current_metrics, diagnosis, ab_result)
    # TODO: 리포트 출력


if __name__ == "__main__":
    run_optimization_pipeline()
