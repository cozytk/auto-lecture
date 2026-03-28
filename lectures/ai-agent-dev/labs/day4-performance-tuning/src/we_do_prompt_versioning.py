"""
Day 4 실습 - WE DO: Prompt 버전 관리 + A/B 테스트

전체가 함께 Prompt Registry를 구축하고 A/B 테스트를 실행한다.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from openai import OpenAI


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# =============================================================================
# 1. Prompt Registry
# =============================================================================

class PromptRegistry:
    """프롬프트 버전 관리 레지스트리"""

    def __init__(self, storage_dir: str = "./prompt_registry"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._prompts: dict[str, list[dict]] = {}

    def register(self, name: str, template: str, description: str = "") -> dict:
        """새로운 프롬프트 버전 등록"""
        if name not in self._prompts:
            self._prompts[name] = []

        versions = self._prompts[name]
        version = len(versions) + 1

        # 중복 체크
        content_hash = hashlib.sha256(template.encode()).hexdigest()[:12]
        for v in versions:
            if v.get("hash") == content_hash:
                print(f"  이미 등록된 프롬프트입니다 (v{v['version']})")
                return v

        version_info = {
            "name": name,
            "version": version,
            "hash": content_hash,
            "template": template,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "is_active": version == 1,  # 첫 버전을 기본 활성
        }

        versions.append(version_info)
        print(f"  등록 완료: {name} v{version} - {description}")
        return version_info

    def get_template(self, name: str, version: int = None) -> str:
        """프롬프트 템플릿 조회"""
        versions = self._prompts.get(name, [])
        if not versions:
            raise ValueError(f"프롬프트 '{name}'이 등록되지 않았습니다")

        if version:
            for v in versions:
                if v["version"] == version:
                    return v["template"]
            raise ValueError(f"v{version}이 존재하지 않습니다")

        # 활성 버전 반환
        for v in versions:
            if v["is_active"]:
                return v["template"]
        return versions[-1]["template"]

    def list_versions(self, name: str) -> list[dict]:
        """버전 목록 조회"""
        return [
            {
                "version": v["version"],
                "description": v["description"],
                "is_active": v["is_active"],
                "hash": v["hash"],
                "created_at": v["created_at"]
            }
            for v in self._prompts.get(name, [])
        ]


# =============================================================================
# 2. A/B 테스트
# =============================================================================

class PromptABTest:
    """두 프롬프트 버전을 비교하는 A/B 테스트"""

    def __init__(self, prompt_a: str, prompt_b: str, test_name: str = "ab_test"):
        self.prompt_a = prompt_a
        self.prompt_b = prompt_b
        self.test_name = test_name

    def run(self, test_cases: list[dict], model: str = "gpt-4o") -> dict:
        """A/B 테스트 실행"""
        results_a = []
        results_b = []

        for i, case in enumerate(test_cases):
            print(f"  테스트 {i+1}/{len(test_cases)}...")

            # Version A 실행
            output_a = self._call_llm(self.prompt_a, case["input"], model)

            # Version B 실행
            output_b = self._call_llm(self.prompt_b, case["input"], model)

            # 평가 (LLM Judge)
            score_a = self._judge(case, output_a, model)
            score_b = self._judge(case, output_b, model)

            results_a.append({"input": case["input"], "output": output_a, "score": score_a})
            results_b.append({"input": case["input"], "output": output_b, "score": score_b})

        return self._summarize(results_a, results_b)

    def _call_llm(self, system_prompt: str, user_input: str, model: str) -> str:
        """LLM 호출"""
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0,
            max_tokens=500
        )
        return response.choices[0].message.content

    def _judge(self, case: dict, output: str, model: str) -> float:
        """LLM Judge로 0-1 점수 산출"""
        judge_prompt = f"""다음 AI 응답의 품질을 0.0~1.0 사이 점수로 평가하세요.

질문: {case['input']}
기대 답변 핵심: {case.get('expected', '없음')}
실제 답변: {output}

JSON으로 응답하세요: {{"score": 0.0~1.0, "reason": "..."}}"""

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": judge_prompt}],
            temperature=0,
            response_format={"type": "json_object"},
            max_tokens=200
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("score", 0.5)

    def _summarize(self, results_a: list, results_b: list) -> dict:
        """결과 요약"""
        scores_a = [r["score"] for r in results_a]
        scores_b = [r["score"] for r in results_b]

        mean_a = sum(scores_a) / len(scores_a) if scores_a else 0
        mean_b = sum(scores_b) / len(scores_b) if scores_b else 0

        wins_a = sum(1 for a, b in zip(scores_a, scores_b) if a > b)
        wins_b = sum(1 for a, b in zip(scores_a, scores_b) if b > a)
        ties = sum(1 for a, b in zip(scores_a, scores_b) if a == b)

        winner = "A" if mean_a > mean_b else ("B" if mean_b > mean_a else "tie")
        improvement = ((mean_b - mean_a) / mean_a * 100) if mean_a > 0 else 0

        return {
            "test_name": self.test_name,
            "total_cases": len(scores_a),
            "version_a": {"mean_score": round(mean_a, 4), "wins": wins_a},
            "version_b": {"mean_score": round(mean_b, 4), "wins": wins_b},
            "ties": ties,
            "winner": winner,
            "improvement_pct": round(improvement, 2),
        }


# =============================================================================
# 3. 함께 실습하기
# =============================================================================

def run_demo():
    """Prompt 버전 관리 + A/B 테스트 시연"""
    print("=" * 60)
    print("WE DO: Prompt 버전 관리 + A/B 테스트")
    print("=" * 60)

    # --- Registry에 프롬프트 등록 ---
    print("\n--- 1. 프롬프트 등록 ---")
    registry = PromptRegistry()

    # Version 1: 기본 프롬프트
    prompt_v1 = """당신은 고객 지원 Agent입니다.
고객의 질문에 정확하고 친절하게 답변하세요.
확인되지 않은 정보는 제공하지 마세요."""

    registry.register(
        name="customer_support",
        template=prompt_v1,
        description="기본 프롬프트 (지시만)"
    )

    # Version 2: Few-shot 예시 추가
    prompt_v2 = """당신은 고객 지원 Agent입니다.
고객의 질문에 정확하고 친절하게 답변하세요.
확인되지 않은 정보는 제공하지 마세요.

## 응답 예시

### 예시 1
고객: 배송이 얼마나 걸리나요?
답변: 주문 후 1-2 영업일 내에 출고되며, 출고 후 1-2일 이내에 도착합니다. 도서산간 지역은 1-2일 추가 소요될 수 있습니다.

### 예시 2
고객: 환불하고 싶어요.
답변: 환불을 도와드리겠습니다. 주문번호를 알려주시면 환불 가능 여부를 확인해 드리겠습니다. 수령 후 7일 이내라면 전액 환불이 가능합니다.

위 예시처럼 구체적인 정보를 포함하여 답변하세요."""

    registry.register(
        name="customer_support",
        template=prompt_v2,
        description="Few-shot 예시 추가 (구체적 답변 유도)"
    )

    # 버전 목록 확인
    print("\n--- 등록된 버전 ---")
    for v in registry.list_versions("customer_support"):
        active = " (활성)" if v["is_active"] else ""
        print(f"  v{v['version']}: {v['description']}{active}")

    # --- A/B 테스트 ---
    print("\n--- 2. A/B 테스트 실행 ---")

    test_cases = [
        {
            "input": "주문한 상품이 아직 안 왔어요. 언제 오나요?",
            "expected": "배송 상태 확인 안내, 예상 도착일 안내"
        },
        {
            "input": "이 제품 교환 가능한가요? 사이즈가 안 맞아서요.",
            "expected": "교환 가능 여부, 교환 절차 안내"
        },
        {
            "input": "결제했는데 취소하고 싶어요.",
            "expected": "주문 취소 절차, 환불 일정 안내"
        },
    ]

    ab_test = PromptABTest(
        prompt_a=prompt_v1,
        prompt_b=prompt_v2,
        test_name="customer_support_v1_vs_v2"
    )

    print("  A/B 테스트 진행 중 (API 호출)...")
    result = ab_test.run(test_cases, model="gpt-4o-mini")

    # 결과 출력
    print("\n--- 3. A/B 테스트 결과 ---")
    print(f"  테스트명: {result['test_name']}")
    print(f"  테스트 케이스: {result['total_cases']}개")
    print(f"  Version A (기본): 평균 {result['version_a']['mean_score']:.3f}, 승리 {result['version_a']['wins']}건")
    print(f"  Version B (Few-shot): 평균 {result['version_b']['mean_score']:.3f}, 승리 {result['version_b']['wins']}건")
    print(f"  무승부: {result['ties']}건")
    print(f"  승자: Version {result['winner']}")
    print(f"  B의 개선율: {result['improvement_pct']:+.1f}%")

    if result["winner"] == "B":
        print("\n  => Version B(Few-shot)가 우세합니다. 프로덕션 배포를 권장합니다.")
    elif result["winner"] == "A":
        print("\n  => Version A(기본)가 우세합니다. B를 재검토하세요.")
    else:
        print("\n  => 유의미한 차이 없음. 추가 테스트가 필요합니다.")


if __name__ == "__main__":
    run_demo()
