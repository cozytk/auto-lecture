from __future__ import annotations

import operator
from typing import Annotated, TypedDict


TOOL_SCHEMAS = {
    "search_docs": {
        "required": ["query"],
        "ranges": {"limit": (1, 5)},
    },
    "delete_ticket": {
        "required": ["ticket_id"],
        "ranges": {},
    },
}

TOOL_POLICIES = {
    "search_docs": {"requires_approval": False},
    "delete_ticket": {"requires_approval": True},
}


class ValidationState(TypedDict):
    requested_tool: str
    tool_args: dict
    schema_ok: bool
    policy_ok: bool
    context_ok: bool
    result_ok: bool
    call_count: int
    max_calls: int
    last_tool: str
    approved_by_human: bool
    tool_result: dict
    errors: Annotated[list[str], operator.add]
    audit_log: Annotated[list[dict], operator.add]


def schema_validation(state: ValidationState) -> dict:
    schema = TOOL_SCHEMAS.get(state["requested_tool"])
    errors: list[str] = []
    if schema is None:
        errors.append(f"unknown tool: {state['requested_tool']}")
        return {"schema_ok": False, "errors": errors}

    return {"schema_ok": not errors, "errors": errors}


def policy_validation(state: ValidationState) -> dict:
    errors: list[str] = []
    policy = TOOL_POLICIES.get(state["requested_tool"], {"requires_approval": True})
    _ = policy
    return {"policy_ok": not errors, "errors": errors}


def context_validation(state: ValidationState) -> dict:
    errors: list[str] = []
    if state["requested_tool"] == state["last_tool"]:
        errors.append("same tool requested twice in a row")
    return {"context_ok": not errors, "errors": errors}


def execute_tool(state: ValidationState) -> dict:
    if state["requested_tool"] == "search_docs":
        result = {"status": "ok", "items": ["playbook", "runbook"]}
    else:
        result = {"status": "ok", "deleted": state["tool_args"].get("ticket_id", "")}
    return {"tool_result": result, "call_count": state["call_count"] + 1}


def result_validation(state: ValidationState) -> dict:
    errors: list[str] = []
    _ = state
    return {"result_ok": not errors, "errors": errors}


def make_audit_entry(state: ValidationState, status: str, reason: str) -> dict:
    return {
        "status": status,
        "tool": state["requested_tool"],
        "reason": reason,
        "call_count": state["call_count"],
    }


def record_success(state: ValidationState) -> dict:
    return {"audit_log": [make_audit_entry(state, "approved", "ok")]}


def record_rejection(state: ValidationState) -> dict:
    reason = state["errors"][-1] if state["errors"] else "rejected"
    return {"audit_log": [make_audit_entry(state, "rejected", reason)]}


def route_after_schema(state: ValidationState) -> str:
    return "policy" if state["schema_ok"] else "reject"


def route_after_policy(state: ValidationState) -> str:
    return "context" if state["policy_ok"] else "reject"


def route_after_context(state: ValidationState) -> str:
    return "execute" if state["context_ok"] else "reject"


def route_after_result(state: ValidationState) -> str:
    return "success" if state["result_ok"] else "reject"


def build_graph():
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(ValidationState)
    graph.add_node("schema", schema_validation)
    graph.add_node("policy", policy_validation)
    graph.add_node("context", context_validation)
    graph.add_node("execute", execute_tool)
    graph.add_node("result", result_validation)
    graph.add_node("success", record_success)
    graph.add_node("reject", record_rejection)

    graph.add_edge(START, "schema")
    graph.add_conditional_edges(
        "schema", route_after_schema, {"policy": "policy", "reject": "reject"}
    )
    graph.add_conditional_edges(
        "policy", route_after_policy, {"context": "context", "reject": "reject"}
    )
    graph.add_conditional_edges(
        "context", route_after_context, {"execute": "execute", "reject": "reject"}
    )
    graph.add_edge("execute", "result")
    graph.add_conditional_edges(
        "result", route_after_result, {"success": "success", "reject": "reject"}
    )
    graph.add_edge("success", END)
    graph.add_edge("reject", END)
    return graph.compile()


def run_demo() -> None:
    app = build_graph()
    result = app.invoke(
        {
            "requested_tool": "search_docs",
            "tool_args": {"query": "incident playbook", "limit": 3},
            "schema_ok": False,
            "policy_ok": False,
            "context_ok": False,
            "result_ok": False,
            "call_count": 0,
            "max_calls": 3,
            "last_tool": "",
            "approved_by_human": False,
            "tool_result": {},
            "errors": [],
            "audit_log": [],
        }
    )
    print(result["audit_log"][-1])


if __name__ == "__main__":
    run_demo()
