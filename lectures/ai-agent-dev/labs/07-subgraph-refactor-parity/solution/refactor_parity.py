from __future__ import annotations

import operator
from typing import Annotated, TypedDict


class ParentState(TypedDict):
    query: str
    raw_data: list[str]
    insights: Annotated[list[str], operator.add]
    report: str


def collect_data(state: ParentState) -> dict:
    data = [f"{state['query']} 데이터 1", f"{state['query']} 데이터 2"]
    return {"raw_data": data}


def analyze_data(state: ParentState) -> dict:
    insights = [f"{len(state['raw_data'])}건 기반 인사이트"]
    return {"insights": insights}


def write_report(state: ParentState) -> dict:
    report = f"[보고서] {state['query']} | {'; '.join(state['insights'])}"
    return {"report": report}


def build_monolith():
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(ParentState)
    graph.add_node("collect", collect_data)
    graph.add_node("analyze", analyze_data)
    graph.add_node("report", write_report)
    graph.add_edge(START, "collect")
    graph.add_edge("collect", "analyze")
    graph.add_edge("analyze", "report")
    graph.add_edge("report", END)
    return graph.compile()


class CollectionState(TypedDict):
    query: str
    raw_data: list[str]
    collection_status: str


def build_collection_subgraph():
    from langgraph.graph import END, START, StateGraph

    def collect(state: CollectionState) -> dict:
        data = [f"{state['query']} 데이터 1", f"{state['query']} 데이터 2"]
        return {"raw_data": data, "collection_status": "done"}

    graph = StateGraph(CollectionState)
    graph.add_node("collect", collect)
    graph.add_edge(START, "collect")
    graph.add_edge("collect", END)
    return graph.compile()


class AnalysisState(TypedDict):
    query: str
    raw_data: list[str]
    insights: Annotated[list[str], operator.add]
    report: str
    analysis_mode: str


def build_analysis_subgraph():
    from langgraph.graph import END, START, StateGraph

    def analyze(state: AnalysisState) -> dict:
        return {
            "insights": [f"{len(state['raw_data'])}건 기반 인사이트"],
            "analysis_mode": "summary",
        }

    def report(state: AnalysisState) -> dict:
        return {"report": f"[보고서] {state['query']} | {'; '.join(state['insights'])}"}

    graph = StateGraph(AnalysisState)
    graph.add_node("analyze", analyze)
    graph.add_node("report", report)
    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", "report")
    graph.add_edge("report", END)
    return graph.compile()


def build_refactored():
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(ParentState)
    graph.add_node("collect", build_collection_subgraph())
    graph.add_node("analyze", build_analysis_subgraph())
    graph.add_edge(START, "collect")
    graph.add_edge("collect", "analyze")
    graph.add_edge("analyze", END)
    return graph.compile()


def check_parity(monolith_result: dict, refactored_result: dict) -> bool:
    return (
        monolith_result["report"] == refactored_result["report"]
        and monolith_result["insights"] == refactored_result["insights"]
        and monolith_result["raw_data"] == refactored_result["raw_data"]
    )


def run_demo() -> None:
    initial = {
        "query": "AI Agent 시장 동향",
        "raw_data": [],
        "insights": [],
        "report": "",
    }
    monolith = build_monolith().invoke(initial)
    refactored = build_refactored().invoke(initial)
    print(monolith["report"])
    print(refactored["report"])
    print({"parity": check_parity(monolith, refactored)})


if __name__ == "__main__":
    run_demo()
