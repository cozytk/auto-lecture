"""
LangGraph 기반 단순 에이전트
- create_react_agent + 도구(tool) 호출
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


# ── 1. 도구 정의 ──
def add(a: float, b: float) -> float:
    """두 수를 더합니다."""
    return a + b


def multiply(a: float, b: float) -> float:
    """두 수를 곱합니다."""
    return a * b


# ── 2. 에이전트 생성 ──
llm = ChatOpenAI(model="gpt-5.4")
tools = [add, multiply]

agent = create_agent(llm, tools)

# ── 3. 실행 ──
if __name__ == "__main__":
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "3.5와 7을 더한 뒤, 그 결과에 2를 곱해줘"}]}
    )

    for msg in result["messages"]:
        print(f"[{msg.type}] {msg.content}")
