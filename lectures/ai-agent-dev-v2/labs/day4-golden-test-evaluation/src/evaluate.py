"""
Day 4 Lab 1 — Golden Test Evaluation (WE DO 스캐폴드)

TODO 주석이 있는 곳을 완성하세요.
실행: python src/evaluate.py
"""

import argparse
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ──────────────────────────────────────────────
# 데이터 클래스
# ──────────────────────────────────────────────

@dataclass
class GoldenTestCase:
    id: str
    category: str        # "accuracy" | "faithfulness" | "robustness"
    input: dict
    contexts: list[str]
    expected_output: str
    tolerance: float = 0.75


@dataclass
class TestResult:
    test_id: str
    category: str
    passed: bool
    score: float
    expected: str
    actual: str
    reason: str = ""


# ──────────────────────────────────────────────
# TODO 1: Faithfulness 측정 함수
# ──────────────────────────────────────────────

def measure_faithfulness(
    question: str,
    answer: str,
    contexts: list[str]
) -> dict:
    """
    LM-as-a-Judge로 Faithfulness를 측정한다.
    반환: {"score": float, "reason": str}

    TODO:
    1. contexts를 하나의 문자열로 합친다 (구분자: "\n---\n")
    2. LLM에게 답변의 각 문장이 문서에 근거하는지 평가하는 프롬프트를 작성한다
    3. response_format={"type": "json_object"}로 호출한다
    4. {"score": 0.0~1.0, "reason": "이유"} 형식으로 반환한다
    """
    context_text = "\n---\n".join(contexts)

    prompt = f"""다음 질문에 대한 답변이 제공된 문서에만 근거하는지 평가하라.

질문: {question}

문서:
{context_text}

답변:
{answer}

# TODO: 평가 기준과 JSON 응답 형식 지시문을 여기에 작성하세요
"""

    # TODO: OpenAI API 호출 코드를 작성하세요
    # response = client.chat.completions.create(...)

    # TODO: 응답을 파싱해서 반환하세요
    # return json.loads(...)

    # 임시 반환값 (TODO 완성 후 삭제)
    return {"score": 0.0, "reason": "TODO: 구현 필요"}


# ──────────────────────────────────────────────
# 간단한 Mock Agent (실제 Agent 대신 사용)
# ──────────────────────────────────────────────

def simple_agent(input_data: dict, contexts: list[str]) -> str:
    """
    contexts를 바탕으로 질문에 답하는 간단한 RAG Agent.
    실제 실습에서는 자신의 Agent로 교체한다.
    """
    query = input_data.get("query", "")
    context_text = "\n".join(contexts)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "당신은 도움이 되는 AI 어시스턴트입니다. 제공된 문서를 바탕으로만 답변하세요. 한국어로 간결하게 답변하세요."
            },
            {
                "role": "user",
                "content": f"문서:\n{context_text}\n\n질문: {query}"
            }
        ],
        max_tokens=200,
        temperature=0
    )
    return response.choices[0].message.content


# ──────────────────────────────────────────────
# TODO 2: Golden Test Runner
# ──────────────────────────────────────────────

class GoldenTestRunner:
    def __init__(self, agent_fn=None):
        self.agent = agent_fn or simple_agent

    def run_single(self, tc: GoldenTestCase) -> TestResult:
        """
        단일 테스트 케이스를 실행하고 결과를 반환한다.

        TODO:
        1. self.agent로 actual 응답을 생성한다
        2. measure_faithfulness()로 점수를 계산한다
        3. score >= tc.tolerance이면 passed=True
        4. TestResult를 반환한다
        """
        # TODO: actual 응답 생성
        # actual = self.agent(tc.input, tc.contexts)

        # TODO: 점수 계산
        # result = measure_faithfulness(tc.input["query"], actual, tc.contexts)
        # score = result["score"]

        # TODO: TestResult 반환
        # return TestResult(
        #     test_id=tc.id,
        #     category=tc.category,
        #     passed=score >= tc.tolerance,
        #     score=score,
        #     expected=tc.expected_output,
        #     actual=actual,
        #     reason=result["reason"]
        # )

        # 임시 반환값 (TODO 완성 후 삭제)
        return TestResult(
            test_id=tc.id,
            category=tc.category,
            passed=False,
            score=0.0,
            expected=tc.expected_output,
            actual="TODO: 구현 필요",
            reason="TODO: 구현 필요"
        )

    def run_all(self, test_cases: list[GoldenTestCase]) -> list[TestResult]:
        results = []
        for i, tc in enumerate(test_cases, 1):
            print(f"  [{i}/{len(test_cases)}] {tc.id} ({tc.category}) 실행 중...")
            result = self.run_single(tc)
            results.append(result)
        return results


# ──────────────────────────────────────────────
# TODO 3: 결과 보고서 출력
# ──────────────────────────────────────────────

def print_report(results: list[TestResult]):
    """
    테스트 결과를 카테고리별로 정리해 출력한다.

    TODO:
    1. 전체 pass_rate 계산
    2. 카테고리별 pass_rate 계산
    3. 실패 케이스 목록 출력
    4. 개선 권고 사항 출력
    """
    total = len(results)
    passed = sum(1 for r in results if r.passed)

    print("\n" + "="*50)
    print("  Golden Test Set 평가 결과")
    print("="*50)

    # TODO: 전체 통계 출력
    # print(f"총 테스트: {total}")
    # print(f"통과: {passed}")
    # print(f"pass_rate: {passed/total:.2%}")

    # TODO: 카테고리별 통계 출력
    # categories = set(r.category for r in results)
    # for cat in sorted(categories):
    #     ...

    # TODO: 실패 케이스 출력
    # failed = [r for r in results if not r.passed]
    # if failed:
    #     print("\n실패 케이스:")
    #     for r in failed:
    #         ...

    print("\nTODO: 보고서 출력 구현 필요")


# ──────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────

def load_test_cases(path: str) -> list[GoldenTestCase]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return [GoldenTestCase(**tc) for tc in raw]


def main():
    parser = argparse.ArgumentParser(description="Golden Test Evaluation")
    parser.add_argument("--tests", default="src/golden_tests.json",
                        help="테스트 케이스 JSON 파일 경로")
    parser.add_argument("--my-tests", default=None,
                        help="YOU DO 자신의 테스트 케이스 파일")
    parser.add_argument("--report", action="store_true",
                        help="상세 보고서 출력")
    args = parser.parse_args()

    test_path = args.my_tests or args.tests
    print(f"\n테스트 파일 로드: {test_path}")

    test_cases = load_test_cases(test_path)
    print(f"총 {len(test_cases)}개 테스트 케이스 로드됨\n")

    runner = GoldenTestRunner()
    print("평가 실행 중...")
    results = runner.run_all(test_cases)

    if args.report:
        print_report(results)
    else:
        passed = sum(1 for r in results if r.passed)
        print(f"\n결과: {passed}/{len(results)} 통과")


if __name__ == "__main__":
    main()
