"""
YOU DO 실습: 멀티 소스 정보 수집 Agent

과제: 아래 TODO를 모두 완성하세요.
실행: python src/you_do_multi_source.py
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


# ── Mock 소스 구현 ─────────────────────────────────────────────────────────────

class MockSources:
    """실제 외부 API 대신 사용하는 Mock 소스"""

    def __init__(self, fail_sources: list[str] = None):
        """fail_sources: 실패를 시뮬레이션할 소스 이름 목록"""
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
            return []  # 캐시 미스 (예외 없이 빈 결과)
        return [f"[캐시] {query} 캐시된 결과"]

    def llm_knowledge(self, query: str) -> list[str]:
        # LLM 내부 지식은 항상 무언가를 반환
        return [
            f"[LLM] {query}에 대한 일반적인 정보입니다. "
            f"단, 이 답변은 학습 데이터 기준이며 최신 정보가 아닐 수 있습니다."
        ]


# ── 검증 클래스 ────────────────────────────────────────────────────────────────

class MultiSourceValidator:
    MAX_QUERY_LEN = 200
    MIN_QUERY_LEN = 1
    MAX_CONSECUTIVE_SAME = 1  # 동일 소스 연속 최대 허용 횟수

    def pre_validate(
        self,
        source: str,
        query: str,
        call_history: list[str],
    ) -> ValidationResult:
        """
        TODO: Tool 실행 전 검증

        검증 항목:
        1. 쿼리 길이가 MIN_QUERY_LEN ~ MAX_QUERY_LEN 범위인가?
        2. 동일 소스가 연속으로 MAX_CONSECUTIVE_SAME회 초과 호출되었는가?
           예: call_history[-1] == source이면 동일 소스 연속 2회 → 차단

        반환: ValidationResult.allow() 또는 ValidationResult.deny(reason)
        """
        # TODO: 쿼리 길이 검증

        # TODO: 동일 소스 연속 호출 검증

        return ValidationResult.allow()

    def post_validate(
        self,
        source: str,
        result: Any,
    ) -> PostValidationResult:
        """
        TODO: Tool 실행 후 결과 검증

        검증 항목:
        1. result가 list 타입인가? (아니면 error)
        2. result가 비어 있는가? (빈 결과면 should_retry=True)
        3. result 개수가 2 미만인가? (품질 부족이면 should_retry=True)

        반환: PostValidationResult 인스턴스
        """
        # TODO: 타입 검증

        # TODO: 빈 결과 처리

        # TODO: 품질 검증 (최소 2건)

        return PostValidationResult.success()


# ── Agent ──────────────────────────────────────────────────────────────────────

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


class MultiSourceAgent:
    """
    TODO: 멀티 소스 정보 수집 Agent

    소스 우선순위: web_search → database → cache → llm_knowledge
    각 소스마다 사전/사후 검증을 거친 후 결과를 반환한다.
    """

    SOURCES = ["web_search", "database", "cache", "llm_knowledge"]

    def __init__(self, mock_sources: MockSources):
        self.sources = mock_sources
        self.validator = MultiSourceValidator()

    def _call_source(self, source: str, query: str) -> list[str]:
        """소스별 실제 호출"""
        fn = getattr(self.sources, source)
        return fn(query)

    def _try_source(
        self,
        source: str,
        query: str,
        state: AgentState,
    ) -> list[str] | None:
        """
        TODO: 단일 소스를 검증하고 실행한다.

        절차:
        1. state.is_over_limit() 확인 → 초과 시 None 반환
        2. pre_validate 실행 → 거부 시 None 반환 (로그 출력)
        3. 소스 호출 (_call_source) → 예외 시 None 반환 (로그 출력)
        4. state.record_call(source) 호출
        5. post_validate 실행
           - ok이면 result 반환
           - should_retry이면 None 반환 (로그 출력)
           - 그 외이면 None 반환 (로그 출력)
        """
        # TODO: 구현하세요
        pass

    def search(self, query: str) -> str:
        """
        TODO: 우선순위 순서대로 소스를 시도하고 첫 번째 성공 결과를 반환한다.

        모든 소스가 실패하면 "정보를 찾을 수 없습니다." 반환.
        최종 답변을 마크다운 형식으로 포맷한다.
        """
        state = AgentState(query=query)

        for source in self.SOURCES:
            result = self._try_source(source, query, state)
            if result is not None:
                # 결과 포맷팅
                items = "\n".join(f"- {r}" for r in result)
                return f"**[{source}]** 검색 결과:\n{items}"

        return "정보를 찾을 수 없습니다."


# ── 실행 ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    query = "AI Agent 2026 트렌드"

    # 케이스 1: 웹 검색 성공
    print("=" * 50)
    print("케이스 1: 웹 검색 성공")
    print("=" * 50)
    agent1 = MultiSourceAgent(MockSources())
    print(agent1.search(query))

    # 케이스 2: 웹 검색 + DB 실패 → 캐시 성공
    print("\n" + "=" * 50)
    print("케이스 2: 웹 검색 + DB 실패 → 캐시 사용")
    print("=" * 50)
    agent2 = MultiSourceAgent(MockSources(fail_sources=["web_search", "database"]))
    print(agent2.search(query))

    # 케이스 3: 웹 검색 + DB + 캐시 모두 실패 → LLM Fallback
    print("\n" + "=" * 50)
    print("케이스 3: 모두 실패 → LLM Fallback")
    print("=" * 50)
    agent3 = MultiSourceAgent(
        MockSources(fail_sources=["web_search", "database", "cache"])
    )
    print(agent3.search(query))
