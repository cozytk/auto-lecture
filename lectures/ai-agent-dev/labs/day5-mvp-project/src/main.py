"""
Agent 진입점

프로젝트의 메인 실행 파일이다.
Agent를 초기화하고 사용자 입력을 받아 실행한 뒤 결과를 출력한다.
"""

from config import validate_config, SYSTEM_PROMPT
from agent import create_agent_graph


def run_single_query(graph, query: str) -> dict:
    """단일 쿼리 실행"""
    from langchain_core.messages import HumanMessage, SystemMessage

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]

    result = graph.invoke({"messages": messages})

    # 마지막 AI 메시지 추출
    ai_messages = [
        msg for msg in result["messages"]
        if hasattr(msg, "content") and msg.type == "ai" and msg.content
    ]

    if ai_messages:
        return {
            "success": True,
            "response": ai_messages[-1].content,
            "total_messages": len(result["messages"]),
        }
    else:
        return {
            "success": False,
            "response": "Agent가 응답을 생성하지 못했습니다.",
            "total_messages": len(result["messages"]),
        }


def run_interactive(graph):
    """대화형 모드로 Agent 실행"""
    print("=" * 50)
    print("AI Agent MVP")
    print("종료하려면 'quit' 또는 'exit'를 입력하세요.")
    print("=" * 50)

    while True:
        try:
            query = input("\n질문: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("종료합니다.")
            break

        print("처리 중...")
        result = run_single_query(graph, query)

        if result["success"]:
            print(f"\n답변: {result['response']}")
        else:
            print(f"\n오류: {result['response']}")


def main():
    # 1. 설정 검증
    if not validate_config():
        return

    # 2. Agent 그래프 생성
    print("Agent를 초기화합니다...")
    graph = create_agent_graph()
    print("Agent 준비 완료.\n")

    # 3. 대화형 모드 실행
    run_interactive(graph)


if __name__ == "__main__":
    main()
