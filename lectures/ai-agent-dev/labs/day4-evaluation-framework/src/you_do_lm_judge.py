"""
Day 4 실습 - YOU DO: LM-as-a-Judge 구현

LLM을 평가자로 활용하여 Agent 응답을 채점하는 시스템을 구현한다.
TODO 부분을 완성하세요.
"""

import os
import json
from pathlib import Path


# =============================================================================
# 1. OpenAI 클라이언트 설정
# =============================================================================

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# =============================================================================
# 2. Judge 프롬프트 작성
# =============================================================================

# TODO: Pointwise 평가 프롬프트를 작성하세요
# 요구사항:
# - 5가지 항목(정확성, 완성도, 유용성, 충실성, 안전성)을 1-5점으로 채점
# - 각 항목에 대한 채점 이유를 포함
# - 종합 점수(overall_score)와 종합 의견 포함
# - JSON 형식으로 출력
JUDGE_PROMPT = """여기에 평가 프롬프트를 작성하세요.

## 평가 기준
(TODO: 5가지 평가 항목과 채점 기준을 정의하세요)

## 입력 정보
- 사용자 질문: {question}
- 제공된 컨텍스트: {context}
- Agent 응답: {answer}

## 출력 형식 (JSON)
(TODO: 출력 JSON 구조를 정의하세요)
"""


# =============================================================================
# 3. Judge 함수 구현
# =============================================================================

def judge_response(
    question: str,
    context: str,
    answer: str,
    model: str = "gpt-4o"
) -> dict:
    """LLM Judge로 Agent 응답을 평가

    TODO: OpenAI API를 호출하여 평가를 수행하세요

    Args:
        question: 사용자 질문
        context: 제공된 컨텍스트
        answer: Agent 응답
        model: 평가에 사용할 모델

    Returns:
        평가 결과 딕셔너리
    """
    # TODO: 구현하세요
    # 힌트:
    # 1. JUDGE_PROMPT에 question, context, answer를 채워넣기
    # 2. client.chat.completions.create() 호출
    # 3. response_format={"type": "json_object"} 사용
    # 4. JSON 파싱하여 반환
    pass


# =============================================================================
# 4. 배치 평가 함수
# =============================================================================

def batch_evaluate(test_cases: list[dict], agent_fn=None, model: str = "gpt-4o") -> dict:
    """Golden Test Set 전체를 평가

    TODO: 여러 테스트 케이스를 순회하며 평가를 실행하세요

    Args:
        test_cases: Golden Test Set의 테스트 케이스 목록
        agent_fn: Agent 실행 함수 (없으면 expected_output을 사용)
        model: 평가 모델

    Returns:
        종합 평가 결과
    """
    results = []

    for case in test_cases:
        # Agent 출력 결정 (실제 Agent가 있으면 실행, 없으면 expected_output 사용)
        if agent_fn:
            agent_output = agent_fn(case["input"])
        else:
            agent_output = case["expected_output"]

        # TODO: judge_response를 호출하여 평가하세요
        # TODO: 결과를 results에 추가하세요
        pass

    # TODO: 종합 점수를 계산하세요
    # 힌트: 각 항목(accuracy, completeness 등)의 평균 점수 산출
    summary = {}

    return {"results": results, "summary": summary}


# =============================================================================
# 5. 결과 리포트 생성
# =============================================================================

def print_report(evaluation: dict):
    """평가 결과를 보기 좋게 출력

    TODO: 평가 결과를 리포트 형태로 출력하세요
    """
    print("\n" + "=" * 60)
    print("LM-as-a-Judge 평가 리포트")
    print("=" * 60)

    # TODO: 개별 결과 출력
    # TODO: 종합 점수 출력
    # TODO: 약한 영역 식별 및 개선점 제안
    pass


# =============================================================================
# 6. 메인 실행
# =============================================================================

def main():
    """LM-as-a-Judge 실습 실행"""

    # Golden Test Set 로드
    data_path = Path(__file__).parent.parent / "data" / "golden_test_set.json"

    if not data_path.exists():
        print("Golden Test Set이 없습니다. 먼저 we_do_golden_test.py를 실행하세요.")
        return

    with open(data_path, encoding="utf-8") as f:
        test_set = json.load(f)

    test_cases = test_set["test_cases"]
    print(f"로드된 테스트 케이스: {len(test_cases)}개")

    # 평가 실행
    evaluation = batch_evaluate(test_cases)

    # 리포트 출력
    print_report(evaluation)


if __name__ == "__main__":
    main()
