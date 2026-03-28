"""
YOU DO 실습: 데이터 파이프라인 Agent

과제: 아래 TODO를 모두 완성하세요.
실행: python src/you_do_pipeline.py
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import random


# ── State 정의 ────────────────────────────────────────────────────────────────

class PipelineState(TypedDict):
    csv_url: str
    data: list[dict]
    missing_ratio: float
    outliers: list
    report: str
    retry_count: Annotated[int, operator.add]
    messages: Annotated[list[str], operator.add]


# ── Mock 데이터 로더 (실제 HTTP 호출 대신 사용) ─────────────────────────────

def _mock_load_csv(url: str) -> list[dict]:
    """Mock CSV 로더: URL에 'fail'이 포함되면 실패를 시뮬레이션"""
    if "fail" in url:
        raise ConnectionError(f"CSV 로드 실패: {url}")
    # 간단한 Mock 데이터 생성
    return [
        {"id": i, "value": random.uniform(0, 100), "category": random.choice(["A", "B", None])}
        for i in range(100)
    ]


# ── Nodes ──────────────────────────────────────────────────────────────────────

def load_data_node(state: PipelineState) -> dict:
    """
    TODO: CSV URL에서 데이터를 로드한다.

    성공 시 반환:
        {"data": [...], "messages": ["로드 완료: N행"]}

    실패 시 반환:
        {"data": [], "retry_count": 1, "messages": ["로드 실패: <오류>"]}
    """
    # TODO: _mock_load_csv를 호출하고 예외를 처리하세요.
    pass


def quality_check_node(state: PipelineState) -> dict:
    """
    TODO: 데이터의 결측값 비율을 계산한다.

    결측값 기준: 딕셔너리에서 값이 None인 필드
    계산 방법: (None 값 개수) / (전체 값 개수)

    반환:
        {"missing_ratio": float, "messages": ["품질 검사 완료: N%"]}
    """
    # TODO: state["data"]를 분석해 missing_ratio를 계산하세요.
    pass


def detect_outliers_node(state: PipelineState) -> dict:
    """
    TODO: 이상치를 탐지한다.

    이상치 기준: value 필드가 평균 ± 2 표준편차를 벗어나는 행
    None 값은 이상치 계산에서 제외한다.

    반환:
        {"outliers": [...], "messages": ["이상치 탐지: N건"]}
    """
    # TODO: value 필드 기준으로 이상치를 탐지하세요.
    pass


def generate_report_node(state: PipelineState) -> dict:
    """
    TODO: 정상 품질 데이터에 대한 보고서를 생성한다.

    보고서 내용:
        - 총 행 수
        - 결측값 비율
        - 이상치 수
        - 이상치 목록 (최대 5건)

    반환:
        {"report": "...", "messages": ["보고서 생성 완료"]}
    """
    # TODO: 마크다운 형식의 보고서를 생성하세요.
    pass


def error_report_node(state: PipelineState) -> dict:
    """
    TODO: 품질 검사 실패 시 오류 보고서를 생성한다.

    반환:
        {"report": "...", "messages": ["오류 보고서 생성"]}
    """
    # TODO: 품질 실패 이유를 포함한 간략한 보고서를 생성하세요.
    pass


# ── 분기 함수 ──────────────────────────────────────────────────────────────────

def after_load(state: PipelineState) -> str:
    """
    TODO: 로드 결과에 따라 다음 Node를 결정한다.

    조건:
        - 데이터가 있으면 → "quality_check"
        - 데이터 없고 retry_count < 2 이면 → "load"   (재시도)
        - 데이터 없고 retry_count >= 2 이면 → "error_report" (포기)
    """
    # TODO: 조건 분기 로직을 구현하세요.
    pass


def after_quality(state: PipelineState) -> str:
    """
    TODO: 품질 검사 결과에 따라 다음 Node를 결정한다.

    조건:
        - missing_ratio <= 0.30 이면 → "detect_outliers"
        - missing_ratio > 0.30 이면 → "error_report"
    """
    # TODO: 품질 기준에 따라 분기하세요.
    pass


# ── 그래프 조립 ────────────────────────────────────────────────────────────────

def build_pipeline():
    """
    TODO: StateGraph를 조립한다.

    Node 목록:
        - "load": load_data_node
        - "quality_check": quality_check_node
        - "detect_outliers": detect_outliers_node
        - "generate_report": generate_report_node
        - "error_report": error_report_node

    Edge 목록:
        - entry point: "load"
        - "load" → conditional: after_load
        - "quality_check" → conditional: after_quality
        - "detect_outliers" → "generate_report"
        - "generate_report" → END
        - "error_report" → END
    """
    g = StateGraph(PipelineState)

    # TODO: Node를 추가하세요.

    # TODO: Entry point를 설정하세요.

    # TODO: Edge를 추가하세요.

    return g.compile()


# ── 실행 ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = build_pipeline()

    # 정상 케이스
    print("=== 정상 케이스 ===")
    result = app.invoke({
        "csv_url": "https://example.com/data.csv",
        "data": [],
        "missing_ratio": 0.0,
        "outliers": [],
        "report": "",
        "retry_count": 0,
        "messages": [],
    })
    print(result["report"])
    print("\n--- 실행 로그 ---")
    for msg in result["messages"]:
        print(f"  {msg}")

    # 실패 케이스 (URL에 'fail' 포함)
    print("\n=== 실패 케이스 ===")
    result2 = app.invoke({
        "csv_url": "https://example.com/fail.csv",
        "data": [],
        "missing_ratio": 0.0,
        "outliers": [],
        "report": "",
        "retry_count": 0,
        "messages": [],
    })
    print(result2["report"])
