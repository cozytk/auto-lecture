"""
solution: 데이터 파이프라인 Agent (참고 구현)

YOU DO 실습의 정답 코드입니다.
먼저 30분 이상 혼자 시도한 후 참고하세요.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import random
import statistics


# ── State ─────────────────────────────────────────────────────────────────────

class PipelineState(TypedDict):
    csv_url: str
    data: list[dict]
    missing_ratio: float
    outliers: list
    report: str
    retry_count: Annotated[int, operator.add]
    messages: Annotated[list[str], operator.add]


# ── Mock 로더 ─────────────────────────────────────────────────────────────────

def _mock_load_csv(url: str) -> list[dict]:
    if "fail" in url:
        raise ConnectionError(f"CSV 로드 실패: {url}")
    random.seed(42)
    rows = []
    for i in range(100):
        value = random.uniform(0, 100)
        # 10%는 None (결측값)
        category = random.choice(["A", "B", None]) if random.random() > 0.9 else random.choice(["A", "B"])
        rows.append({"id": i, "value": value, "category": category})
    # 이상치 2개 추가
    rows[10]["value"] = 999.0
    rows[50]["value"] = -999.0
    return rows


# ── Nodes ──────────────────────────────────────────────────────────────────────

def load_data_node(state: PipelineState) -> dict:
    url = state["csv_url"]
    try:
        data = _mock_load_csv(url)
        print(f"[load] 로드 완료: {len(data)}행")
        return {
            "data": data,
            "messages": [f"로드 완료: {len(data)}행"],
        }
    except Exception as e:
        print(f"[load] 실패: {e}")
        return {
            "data": [],
            "retry_count": 1,
            "messages": [f"로드 실패: {e}"],
        }


def quality_check_node(state: PipelineState) -> dict:
    data = state["data"]
    if not data:
        return {"missing_ratio": 1.0, "messages": ["데이터 없음"]}

    total_values = 0
    none_count = 0
    for row in data:
        for v in row.values():
            total_values += 1
            if v is None:
                none_count += 1

    ratio = none_count / total_values if total_values > 0 else 0.0
    pct = round(ratio * 100, 1)
    print(f"[quality] 결측값 비율: {pct}%")
    return {
        "missing_ratio": ratio,
        "messages": [f"품질 검사 완료: {pct}% 결측"],
    }


def detect_outliers_node(state: PipelineState) -> dict:
    data = state["data"]
    values = [row["value"] for row in data if row.get("value") is not None]

    if len(values) < 2:
        return {"outliers": [], "messages": ["이상치 탐지 불가: 데이터 부족"]}

    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    threshold = 2 * stdev

    outliers = [
        row for row in data
        if row.get("value") is not None and abs(row["value"] - mean) > threshold
    ]
    print(f"[outliers] 이상치: {len(outliers)}건")
    return {
        "outliers": outliers,
        "messages": [f"이상치 탐지: {len(outliers)}건 (기준: 평균±2σ)"],
    }


def generate_report_node(state: PipelineState) -> dict:
    data = state["data"]
    outliers = state["outliers"]
    missing_pct = round(state["missing_ratio"] * 100, 1)

    outlier_lines = "\n".join(
        f"  - ID {o['id']}: value={o['value']:.1f}"
        for o in outliers[:5]
    )

    report = f"""# 데이터 파이프라인 보고서

## 개요
- 총 행 수: {len(data)}행
- 결측값 비율: {missing_pct}%
- 이상치 수: {len(outliers)}건

## 이상치 목록 (최대 5건)
{outlier_lines if outlier_lines else "  이상치 없음"}

## 결론
데이터 품질 기준(결측 30% 이하)을 통과했습니다.
"""
    print("[report] 보고서 생성 완료")
    return {
        "report": report,
        "messages": ["보고서 생성 완료"],
    }


def error_report_node(state: PipelineState) -> dict:
    missing_pct = round(state["missing_ratio"] * 100, 1)
    retry = state["retry_count"]

    if not state["data"]:
        reason = f"데이터 로드 실패 (재시도 {retry}회 초과)"
    else:
        reason = f"데이터 품질 기준 미달 (결측값 {missing_pct}% > 30%)"

    report = f"""# 오류 보고서

## 실패 원인
{reason}

## 조치 권장
- 원본 데이터 소스를 점검하세요.
- 결측값 처리 후 재시도하세요.
"""
    print(f"[error_report] {reason}")
    return {
        "report": report,
        "messages": [f"오류 보고서 생성: {reason}"],
    }


# ── 분기 함수 ──────────────────────────────────────────────────────────────────

def after_load(state: PipelineState) -> str:
    if state["data"]:
        return "quality_check"
    if state["retry_count"] < 2:
        return "load"
    return "error_report"


def after_quality(state: PipelineState) -> str:
    if state["missing_ratio"] <= 0.30:
        return "detect_outliers"
    return "error_report"


# ── 그래프 조립 ────────────────────────────────────────────────────────────────

def build_pipeline():
    g = StateGraph(PipelineState)

    g.add_node("load", load_data_node)
    g.add_node("quality_check", quality_check_node)
    g.add_node("detect_outliers", detect_outliers_node)
    g.add_node("generate_report", generate_report_node)
    g.add_node("error_report", error_report_node)

    g.set_entry_point("load")

    g.add_conditional_edges(
        "load",
        after_load,
        {
            "quality_check": "quality_check",
            "load": "load",
            "error_report": "error_report",
        },
    )
    g.add_conditional_edges(
        "quality_check",
        after_quality,
        {
            "detect_outliers": "detect_outliers",
            "error_report": "error_report",
        },
    )
    g.add_edge("detect_outliers", "generate_report")
    g.add_edge("generate_report", END)
    g.add_edge("error_report", END)

    return g.compile()


# ── 실행 ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = build_pipeline()

    initial = {
        "csv_url": "",
        "data": [],
        "missing_ratio": 0.0,
        "outliers": [],
        "report": "",
        "retry_count": 0,
        "messages": [],
    }

    # 정상 케이스
    print("=" * 50)
    print("정상 케이스")
    print("=" * 50)
    result = app.invoke({**initial, "csv_url": "https://example.com/data.csv"})
    print(result["report"])
    print("실행 로그:")
    for msg in result["messages"]:
        print(f"  {msg}")

    # 로드 실패 케이스
    print("\n" + "=" * 50)
    print("로드 실패 케이스 (재시도 후 포기)")
    print("=" * 50)
    result2 = app.invoke({**initial, "csv_url": "https://example.com/fail.csv"})
    print(result2["report"])
    print("실행 로그:")
    for msg in result2["messages"]:
        print(f"  {msg}")
