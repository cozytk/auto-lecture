"""
LangGraph Agent 정의

StateGraph를 사용하여 Agent의 제어 흐름을 정의한다.
노드(Node)와 엣지(Edge)를 구성하여 Agent 루프를 완성한다.

TODO: 프로젝트에 맞게 아래 항목을 수정하세요.
  1. AgentState에 필요한 필드 추가
  2. agent_node에서 LLM 모델과 도구 바인딩 설정
  3. tool_node에서 도구 실행 로직 구현
  4. should_continue에서 종료 조건 수정
  5. (선택) RAG 노드, 추가 분기 등 확장
"""

from typing import TypedDict, Annotated, Sequence
import json

from langchain_core.messages import BaseMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, AGENT_RECURSION_LIMIT
from tools import get_tools


# ============================================================
# 1. Agent 상태 정의
# ============================================================
class AgentState(TypedDict):
    """Agent의 상태를 정의한다.

    messages: 대화 메시지 목록 (자동으로 추가/병합됨)

    TODO: 프로젝트에 필요한 상태 필드를 추가하세요.
    예시:
        iteration_count: int       # 반복 횟수 추적
        retrieved_docs: list[str]  # RAG 검색 결과
        current_tool: str          # 현재 실행 중인 도구
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]


# ============================================================
# 2. 노드 정의
# ============================================================
def agent_node(state: AgentState) -> dict:
    """LLM을 호출하여 다음 행동을 결정하는 노드

    Tool 호출이 필요하면 tool_calls가 포함된 AIMessage를 반환하고,
    최종 응답이면 일반 AIMessage를 반환한다.
    """
    # LLM 초기화 + Tool 바인딩
    tools = get_tools()
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
    )

    if tools:
        llm_with_tools = llm.bind_tools(tools)
    else:
        llm_with_tools = llm

    # LLM 호출
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


def tool_node(state: AgentState) -> dict:
    """Tool을 실행하는 노드

    마지막 AI 메시지의 tool_calls를 순회하며 각 Tool을 실행한다.
    실행 결과를 ToolMessage로 변환하여 반환한다.
    """
    messages = state["messages"]
    last_message = messages[-1]

    tool_messages = []
    tools = get_tools()
    tool_map = {tool.name: tool for tool in tools}

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        if tool_name in tool_map:
            try:
                result = tool_map[tool_name].invoke(tool_args)
                content = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
            except Exception as e:
                content = json.dumps({"error": str(e)}, ensure_ascii=False)
        else:
            content = json.dumps(
                {"error": f"알 수 없는 도구: {tool_name}"},
                ensure_ascii=False,
            )

        tool_messages.append(
            ToolMessage(content=content, tool_call_id=tool_call["id"])
        )

    return {"messages": tool_messages}


# TODO: RAG 프로젝트인 경우 아래 노드를 활성화하세요.
# def rag_node(state: AgentState) -> dict:
#     """RAG 검색을 수행하는 노드"""
#     from rag import search_documents
#     query = state["messages"][-1].content
#     docs = search_documents(query)
#     context = "\n\n".join(docs)
#     # 검색 결과를 시스템 메시지로 추가
#     from langchain_core.messages import SystemMessage
#     return {"messages": [SystemMessage(content=f"참고 문서:\n{context}")]}


# ============================================================
# 3. 분기 조건 정의
# ============================================================
def should_continue(state: AgentState) -> str:
    """다음 노드를 결정하는 분기 함수

    마지막 메시지에 tool_calls가 있으면 'tools' 노드로,
    없으면 대화 종료(END)로 이동한다.
    """
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


# ============================================================
# 4. 그래프 구성
# ============================================================
def create_agent_graph():
    """Agent 그래프를 생성하고 컴파일한다.

    기본 구조:
        agent_node → (tool_calls 있으면) → tool_node → agent_node → ...
        agent_node → (tool_calls 없으면) → END

    TODO: 프로젝트에 맞게 노드와 엣지를 추가하세요.
    """
    # 그래프 생성
    workflow = StateGraph(AgentState)

    # 노드 추가
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    # TODO: RAG 노드가 필요하면 아래 주석을 해제하세요.
    # workflow.add_node("rag", rag_node)

    # 시작점 설정
    workflow.set_entry_point("agent")

    # 조건부 엣지: agent → tools 또는 END
    workflow.add_conditional_edges("agent", should_continue)

    # 엣지: tools → agent (Tool 결과를 Agent에 반환)
    workflow.add_edge("tools", "agent")

    # 컴파일
    graph = workflow.compile()

    return graph


if __name__ == "__main__":
    # 그래프 구조 확인용
    graph = create_agent_graph()
    print("Agent 그래프가 성공적으로 생성되었습니다.")
    print(f"노드: {list(graph.nodes.keys())}")
