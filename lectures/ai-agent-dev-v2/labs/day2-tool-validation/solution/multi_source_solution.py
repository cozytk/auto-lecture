"""
solution: 멀티 소스 정보 수집 Agent (참고 구현)

YOU DO 실습의 정답 코드입니다.
먼저 30분 이상 혼자 시도한 후 참고하세요.
"""

from dataclasses import dataclass, field
from typing import Any
from enum import Enum


# ── 결과 타입 ──────────────────────────────────────────────────────────────────

class ValidationStatus(Enum):
    ALLOWED = "allowed"
    DENIED = "denied"


@dataclass
class ValidationResult:
    status: ValidationStatus
    reason: str = ""

    @classmethod
    def allow(cls) -> "ValidationResult":
        return cls(ValidationStatus.ALLOWED)

    @classmethod
    def deny(cls, reason: str) -> "ValidationResult":
        return cls(ValidationStatus.DENIED, reason)

    @property
    def allowed(self) -> bool:
        return self.status == ValidationStatus.ALLOWED


@dataclass
class PostValidationResult:
    ok: bool
    should_retry: bool = False
    reason: str = ""

    @classmethod
    def success(cls) -> "PostValidationResult":
        return cls(ok=True)

    @classmethod
    def empty(cls) -> "PostValidationResult":
        return cls(ok=False, should_retry=True, reason="결과 없음")

    @classmethod
    def low_quality(cls, reason: str) -> "PostValidationResult":
        return cls(ok=False, should_retry=True, reason=reason)

    @classmethod
    def error(cls, reason: str) -> "PostValidationResult":
        return cls(ok=False, should_retry=False, reason=reason)


# ── Mock 소스 ──────────────────────────────────────────────────────────────────

class MockSources:
    def __init__(self, fail_sources: list[str] = None):
        self.fail_sources = fail_sources or []

    def web_search(self, query: str) -> list[str]:
        if "web_search" in self.fail_sources:
            raise ConnectionError("웹 검색 API 연결 실패")
        return [
            f"[웹] {query}에 관한 최신 뉴스 1",
            f"[웹] {query}에 관한 분석 보고서",
            f"[웹] {query} 관련 전문가 인터뷰",
        ]

    def database(self, query: str) -> list[str]:
        if "database" in self.fail_sources:
            raise TimeoutError("데이터베이스 타임아웃")
        return [
            f"[DB] {query} 관련 저장된 데이터 1",
            f"[DB] {query} 관련 저장된 데이터 2",
        ]

    def cache(self, query: str) -> list[str]:
        if "cache" in self.fail_sources:
            return []
        return [f"[캐시] {query} 캐시된 결과"]

    def llm_knowledge(self, query: str) -> list[str]:
        return [
            f"[LLM] {query}에 대한 일반적인 정보입니다. "
            f"단, 이 답변은 학습 데이터 기준이며 최신 정보가 아닐 수 있습니다."
        ]


# ── 검증 클래스 ────────────────────────────────────────────────────────────────

class MultiSourceValidator:
    MAX_QUERY_LEN = 200
    MIN_QUERY_LEN = 1
    MAX_CONSECUTIVE_SAME = 1

    def pre_validate(
        self,
        source: str,
        query: str,
        call_history: list[str],
    ) -> ValidationResult:
        # 1. 쿼리 길이 검증
        if len(query) < self.MIN_QUERY_LEN:
            return ValidationResult.deny("쿼리가 너무 짧습니다")
        if len(query) > self.MAX_QUERY_LEN:
            return ValidationResult.deny(f"쿼리가 너무 깁니다 (최대 {self.MAX_QUERY_LEN}자)")

        # 2. 동일 소스 연속 호출 검증
        if call_history and call_history[-1] == source:
            return ValidationResult.deny(
                f"동일 소스 연속 호출 차단: {source}"
            )

        return ValidationResult.allow()

    def post_validate(
        self,
        source: str,
        result: Any,
    ) -> PostValidationResult:
        # 1. 타입 검증
        if not isinstance(result, list):
            return PostValidationResult.error(f"예상 타입 불일치: {type(result).__name__}")

        # 2. 빈 결과
        if not result:
            return PostValidationResult.empty()

        # 3. 품질 검증 (최소 2건) — llm_knowledge는 예외
        if source != "llm_knowledge" and len(result) < 2:
            return PostValidationResult.low_quality(
                f"결과 부족: {len(result)}건 (최소 2건 필요)"
            )

        return PostValidationResult.success()


# ── Agent State ────────────────────────────────────────────────────────────────

@dataclass
class AgentState:
    query: str
    call_history: list[str] = field(default_factory=list)
    total_calls: int = 0
    final_answer: str = ""

    MAX_TOTAL_CALLS = 10

    def record_call(self, source: str):
        self.call_history.append(source)
        self.total_calls += 1

    def is_over_limit(self) -> bool:
        return self.total_calls >= self.MAX_TOTAL_CALLS


# ── Agent ──────────────────────────────────────────────────────────────────────

class MultiSourceAgent:
    SOURCES = ["web_search", "database", "cache", "llm_knowledge"]

    def __init__(self, mock_sources: MockSources):
        self.sources = mock_sources
        self.validator = MultiSourceValidator()

    def _call_source(self, source: str, query: str) -> list[str]:
        fn = getattr(self.sources, source)
        return fn(query)

    def _try_source(
        self,
        source: str,
        query: str,
        state: AgentState,
    ) -> list[str] | None:
        # 총 호출 한도 확인
        if state.is_over_limit():
            print(f"  [guard] 총 호출 한도 초과 ({state.MAX_TOTAL_CALLS}회)")
            return None

        # 사전 검증
        pre = self.validator.pre_validate(source, query, state.call_history)
        if not pre.allowed:
            print(f"  [pre_validate] {source} 차단: {pre.reason}")
            return None

        # 실행
        try:
            result = self._call_source(source, query)
            state.record_call(source)
            print(f"  [call] {source} 호출 완료: {len(result)}건")
        except Exception as e:
            state.record_call(source)
            print(f"  [call] {source} 실패: {e}")
            return None

        # 사후 검증
        post = self.validator.post_validate(source, result)
        if post.ok:
            return result
        print(f"  [post_validate] {source} 결과 부적합: {post.reason}")
        return None

    def search(self, query: str) -> str:
        state = AgentState(query=query)
        print(f"검색 쿼리: {query!r}")

        for source in self.SOURCES:
            result = self._try_source(source, query, state)
            if result is not None:
                items = "\n".join(f"- {r}" for r in result)
                return f"**[{source}]** 검색 결과:\n{items}"

        return "정보를 찾을 수 없습니다. (모든 소스 실패)"


# ── 실행 ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    query = "AI Agent 2026 트렌드"

    print("=" * 50)
    print("케이스 1: 웹 검색 성공")
    print("=" * 50)
    agent1 = MultiSourceAgent(MockSources())
    print(agent1.search(query))

    print("\n" + "=" * 50)
    print("케이스 2: 웹 검색 + DB 실패 → 캐시 사용")
    print("=" * 50)
    agent2 = MultiSourceAgent(MockSources(fail_sources=["web_search", "database"]))
    print(agent2.search(query))

    print("\n" + "=" * 50)
    print("케이스 3: 웹 검색 + DB + 캐시 모두 실패 → LLM Fallback")
    print("=" * 50)
    agent3 = MultiSourceAgent(
        MockSources(fail_sources=["web_search", "database", "cache"])
    )
    print(agent3.search(query))

    print("\n" + "=" * 50)
    print("케이스 4: 빈 쿼리 → 사전 검증 차단")
    print("=" * 50)
    agent4 = MultiSourceAgent(MockSources())
    print(agent4.search(""))
