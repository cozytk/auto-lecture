from __future__ import annotations

import operator
from typing import Annotated, Any, Literal, TypedDict


StateUpdate = dict[str, Any]


class WorkflowState(TypedDict):
    request: str
    route: str
    attempts: int
    max_attempts: int
    confidence: float
    result: str
    used_fallback: bool
    logs: Annotated[list[str], operator.add]


def determine_route(request: str) -> Literal["access", "billing", "incident"]:
    lowered = request.lower()
    if "권한" in request or "비밀번호" in request or "access" in lowered:
        return "access"
    if "결제" in request or "환불" in request or "invoice" in lowered:
        return "billing"
    return "incident"


def classify_request(state: WorkflowState) -> StateUpdate:
    route = determine_route(state["request"])
    return {"route": route, "logs": [f"classify -> {route}"]}


def handle_access(state: WorkflowState) -> StateUpdate:
    attempts = state["attempts"] + 1
    return {
        "attempts": attempts,
        "confidence": 0.93,
        "result": "권한 요청 절차와 필요한 승인 단계를 안내했습니다.",
        "logs": [f"access attempt {attempts}"],
    }


def handle_billing(state: WorkflowState) -> StateUpdate:
    attempts = state["attempts"] + 1
    return {
        "attempts": attempts,
        "confidence": 0.88,
        "result": "결제 상태를 확인하고 환불 정책 링크를 제공했습니다.",
        "logs": [f"billing attempt {attempts}"],
    }


def handle_incident(state: WorkflowState) -> StateUpdate:
    attempts = state["attempts"] + 1
    confidence = 0.54 if attempts == 1 else 0.86
    result = (
        "장애 초동 대응 체크리스트를 제공했습니다."
        if attempts == 1
        else "재시도 후 장애 범위와 우선 조치를 정리했습니다."
    )
    return {
        "attempts": attempts,
        "confidence": confidence,
        "result": result,
        "logs": [f"incident attempt {attempts} -> {confidence:.2f}"],
    }


def quality_gate(state: WorkflowState) -> StateUpdate:
    decision = route_after_quality(state)
    return {"logs": [f"quality_gate -> {decision}"]}


def route_after_classify(state: WorkflowState) -> str:
    return state["route"]


def route_after_quality(state: WorkflowState) -> str:
    if state["confidence"] >= 0.8:
        return "finish"
    if state["attempts"] >= state["max_attempts"]:
        return "fallback"
    return state["route"]


def fallback_handler(state: WorkflowState) -> StateUpdate:
    return {
        "used_fallback": True,
        "confidence": 1.0,
        "result": "추가 맥락이 부족해 운영 담당자에게 수동 검토를 요청했습니다.",
        "logs": ["fallback -> manual handoff"],
    }


def finish_node(state: WorkflowState) -> StateUpdate:
    return {"logs": [f"finish -> fallback={state['used_fallback']}"]}


def build_graph():
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(WorkflowState)
    _ = graph.add_node("classify", classify_request)
    _ = graph.add_node("access", handle_access)
    _ = graph.add_node("billing", handle_billing)
    _ = graph.add_node("incident", handle_incident)
    _ = graph.add_node("quality_gate", quality_gate)
    _ = graph.add_node("fallback", fallback_handler)
    _ = graph.add_node("finish", finish_node)

    _ = graph.add_edge(START, "classify")
    _ = graph.add_conditional_edges(
        "classify",
        route_after_classify,
        {
            "access": "access",
            "billing": "billing",
            "incident": "incident",
        },
    )
    _ = graph.add_edge("access", "quality_gate")
    _ = graph.add_edge("billing", "quality_gate")
    _ = graph.add_edge("incident", "quality_gate")
    _ = graph.add_conditional_edges(
        "quality_gate",
        route_after_quality,
        {
            "access": "access",
            "billing": "billing",
            "incident": "incident",
            "fallback": "fallback",
            "finish": "finish",
        },
    )
    _ = graph.add_edge("fallback", "finish")
    _ = graph.add_edge("finish", END)
    return graph.compile()


def run_demo() -> None:
    app = build_graph()
    scenarios = [
        "비밀번호 재설정 권한을 열어주세요",
        "결제 영수증과 환불 상태를 확인하고 싶어요",
        "배포 후 서비스 장애가 발생했습니다",
    ]
    for request in scenarios:
        initial: WorkflowState = {
            "request": request,
            "route": "",
            "attempts": 0,
            "max_attempts": 2,
            "confidence": 0.0,
            "result": "",
            "used_fallback": False,
            "logs": [],
        }
        result = app.invoke(initial)
        print(f"=== {request} ===")
        print(result["result"])
        print(result["logs"])
        print()


if __name__ == "__main__":
    run_demo()
