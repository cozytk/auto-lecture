"""
Day 4 Lab 1 — Golden Test Evaluation (정답 코드)

YOU DO 과제의 참조용 정답 코드다.
막히면 이 파일을 참조한다.
실행: python solution/evaluate.py --report
"""

import argparse
import json
import os
from collections import defaultdict
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
    category: str
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
# Faithfulness 측정 (완성 버전)
# ──────────────────────────────────────────────

def measure_faithfulness(
    question: str,
    answer: str,
    contexts: list[str]
) -> dict:
    """LM-as-a-Judge로 Faithfulness를 측정한다."""
    context_text = "\n---\n".join(contexts)

    prompt = f"""다음 질문에 대한 답변이 제공된 문서에만 근거하는지 평가하라.

질문: {question}

문서:
{context_text}

답변:
{answer}

평가 기준:
- 답변의 각 문장이 위 문서에 근거하는지 확인한다.
- 문서에 없는 내용을 주장하면 감점한다.
- 근거 있는 문장 수 / 전체 문장 수 = Faithfulness 점수
- 점수: 0.0(전혀 근거 없음) ~ 1.0(완전히 근거 있음)

JSON으로만 응답하라:
{{"score": 0.85, "reason": "답변의 X문장 중 Y문장이 문서에 근거함. 나머지는 문서에 없는 내용."}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )
    return json.loads(response.choices[0].message.content)


def measure_accuracy(
    question: str,
    expected: str,
    actual: str
) -> dict:
    """기대 응답과 실제 응답의 의미적 일치도를 측정한다."""
    prompt = f"""다음 두 응답이 의미적으로 얼마나 일치하는지 평가하라.

질문: {question}

기대 응답:
{expected}

실제 응답:
{actual}

평가 기준:
- 핵심 사실이 일치하는가?
- 누락된 중요 정보가 있는가?
- 잘못된 정보가 포함됐는가?
- 점수: 0.0(완전 불일치) ~ 1.0(완전 일치)

JSON으로만 응답하라:
{{"score": 0.90, "reason": "평가 이유"}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0
    )
    return json.loads(response.choices[0].message.content)


# ──────────────────────────────────────────────
# Pairwise 비교 (YOU DO 추가 구현)
# ──────────────────────────────────────────────

def pairwise_judge(
    question: str,
    response_a: str,
    response_b: str,
    criteria: str = "정확성, 간결성, 문서 근거"
) -> dict:
    """
    두 응답을 비교해 승자를 판정한다.
    위치 편향 제거를 위해 순서를 바꿔 두 번 평가한다.
    """
    def single_eval(r1: str, r2: str, l1: str, l2: str) -> dict:
        prompt = f"""질문: {question}

응답 {l1}: {r1}

응답 {l2}: {r2}

평가 기준: {criteria}

어느 응답이 더 나은가? JSON으로만 응답하라:
{{"winner": "{l1} or {l2} or tie", "reason": "이유"}}"""
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0
        )
        return json.loads(resp.choices[0].message.content)

    result1 = single_eval(response_a, response_b, "A", "B")
    result2 = single_eval(response_b, response_a, "B", "A")

    a_wins = (result1["winner"] == "A" and result2["winner"] == "B")
    b_wins = (result1["winner"] == "B" and result2["winner"] == "A")

    if a_wins:
        return {"winner": "A", "confidence": "high",
                "reason": result1["reason"]}
    elif b_wins:
        return {"winner": "B", "confidence": "high",
                "reason": result2["reason"]}
    else:
        return {"winner": "tie", "confidence": "low",
                "reason": "두 평가 결과가 불일치"}


# ──────────────────────────────────────────────
# Mock Agent
# ──────────────────────────────────────────────

def simple_agent(input_data: dict, contexts: list[str]) -> str:
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
# Golden Test Runner (완성 버전)
# ──────────────────────────────────────────────

class GoldenTestRunner:
    def __init__(self, agent_fn=None):
        self.agent = agent_fn or simple_agent

    def run_single(self, tc: GoldenTestCase) -> TestResult:
        actual = self.agent(tc.input, tc.contexts)

        # 카테고리별 측정 방법 분기
        if tc.category == "faithfulness":
            result = measure_faithfulness(
                tc.input["query"], actual, tc.contexts
            )
        else:
            # accuracy, robustness 모두 기대값과 비교
            result = measure_accuracy(
                tc.input["query"], tc.expected_output, actual
            )

        score = result["score"]
        return TestResult(
            test_id=tc.id,
            category=tc.category,
            passed=score >= tc.tolerance,
            score=score,
            expected=tc.expected_output,
            actual=actual,
            reason=result.get("reason", "")
        )

    def run_all(self, test_cases: list[GoldenTestCase]) -> list[TestResult]:
        results = []
        for i, tc in enumerate(test_cases, 1):
            print(f"  [{i}/{len(test_cases)}] {tc.id} ({tc.category}) ...", end=" ")
            result = self.run_single(tc)
            status = "통과" if result.passed else "실패"
            print(f"{status} (score={result.score:.2f})")
            results.append(result)
        return results


# ──────────────────────────────────────────────
# 보고서 출력 (완성 버전)
# ──────────────────────────────────────────────

def print_report(results: list[TestResult]):
    total = len(results)
    passed = sum(1 for r in results if r.passed)

    print("\n" + "=" * 55)
    print("  Golden Test Set 평가 결과")
    print("=" * 55)
    print(f"  총 테스트  : {total}건")
    print(f"  통과       : {passed}건")
    print(f"  실패       : {total - passed}건")
    print(f"  pass_rate  : {passed / total:.1%}")
    print("-" * 55)

    # 카테고리별 통계
    cat_stats: dict[str, dict] = defaultdict(lambda: {"total": 0, "passed": 0})
    for r in results:
        cat_stats[r.category]["total"] += 1
        if r.passed:
            cat_stats[r.category]["passed"] += 1

    print("\n  카테고리별 결과:")
    for cat, stats in sorted(cat_stats.items()):
        t = stats["total"]
        p = stats["passed"]
        bar = "█" * p + "░" * (t - p)
        print(f"  {cat:<15} {bar} {p}/{t} ({p/t:.0%})")

    # 실패 케이스
    failed = [r for r in results if not r.passed]
    if failed:
        print(f"\n  실패 케이스 ({len(failed)}건):")
        print("-" * 55)
        for r in sorted(failed, key=lambda x: x.score):
            print(f"  [{r.test_id}] score={r.score:.2f} (category={r.category})")
            print(f"    이유: {r.reason[:80]}{'...' if len(r.reason) > 80 else ''}")

    # 개선 권고
    print("\n  개선 권고:")
    print("-" * 55)
    low_cats = [
        c for c, s in cat_stats.items()
        if s["passed"] / s["total"] < 0.75
    ]
    if low_cats:
        for cat in low_cats:
            if cat == "faithfulness":
                print("  - Faithfulness 낮음: RAG 청크 크기 조정 또는 프롬프트에 '문서만 참조' 강조 추가")
            elif cat == "accuracy":
                print("  - Accuracy 낮음: Golden Test에서 실패 케이스를 Few-shot 예시로 프롬프트에 추가")
            elif cat == "robustness":
                print("  - Robustness 낮음: 동의어 처리를 위한 쿼리 재작성(Query Rewriting) 레이어 추가")
    else:
        print("  - 모든 카테고리 pass_rate 75% 이상. 임계값 상향 검토 가능.")

    print("=" * 55)


# ──────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────

def load_test_cases(path: str) -> list[GoldenTestCase]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return [GoldenTestCase(**tc) for tc in raw]


def main():
    parser = argparse.ArgumentParser(description="Golden Test Evaluation (정답)")
    parser.add_argument("--tests", default="src/golden_tests.json")
    parser.add_argument("--my-tests", default=None)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--pairwise", action="store_true",
                        help="v1 vs v2 Pairwise 비교 데모 실행")
    args = parser.parse_args()

    test_path = args.my_tests or args.tests
    print(f"\n테스트 파일 로드: {test_path}")
    test_cases = load_test_cases(test_path)
    print(f"총 {len(test_cases)}개 테스트 케이스\n")

    runner = GoldenTestRunner()
    print("평가 실행 중...")
    results = runner.run_all(test_cases)

    if args.report:
        print_report(results)
    else:
        passed = sum(1 for r in results if r.passed)
        print(f"\n결과: {passed}/{len(results)} 통과 ({passed/len(results):.1%})")

    # Pairwise 데모
    if args.pairwise:
        print("\n\n[Pairwise 비교 데모]")
        q = "파이썬 GIL이란 무엇인가?"
        v1 = "GIL은 전역 인터프리터 잠금입니다."
        v2 = "GIL(Global Interpreter Lock)은 CPython의 뮤텍스로, 한 번에 하나의 스레드만 파이썬 바이트코드를 실행하도록 제한합니다."
        result = pairwise_judge(q, v1, v2)
        print(f"  승자: {result['winner']} (신뢰도: {result['confidence']})")
        print(f"  이유: {result['reason']}")


if __name__ == "__main__":
    main()
