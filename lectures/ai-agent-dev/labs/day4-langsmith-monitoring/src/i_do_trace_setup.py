"""
Day 4 실습 - I DO: LangSmith 기본 설정 및 Trace 수집

강사가 시연하는 코드이다. 학생은 관찰하며 이해한다.
LangSmith에 Trace를 자동 수집하고, 대시보드에서 확인하는 방법을 보여준다.
"""

import os
from langsmith import traceable
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


# =============================================================================
# 1. 환경 변수 확인
# =============================================================================

def check_environment():
    """LangSmith 환경 변수 확인"""
    print("--- 환경 변수 확인 ---")

    required = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "LANGSMITH_API_KEY": os.environ.get("LANGSMITH_API_KEY", ""),
        "LANGSMITH_TRACING": os.environ.get("LANGSMITH_TRACING", ""),
        "LANGSMITH_PROJECT": os.environ.get("LANGSMITH_PROJECT", ""),
    }

    all_set = True
    for key, value in required.items():
        status = "OK" if value else "MISSING"
        if not value:
            all_set = False
        masked = value[:8] + "..." if len(value) > 8 else value
        print(f"  {key}: {status} ({masked})")

    if not all_set:
        print("\n  WARNING: 일부 환경 변수가 설정되지 않았습니다.")
        print("  다음 명령으로 설정하세요:")
        print('  export LANGSMITH_API_KEY="your-key"')
        print('  export LANGSMITH_TRACING=true')
        print('  export LANGSMITH_PROJECT="day4-monitoring-lab"')

    return all_set


# =============================================================================
# 2. LangChain 자동 Trace (환경 변수만으로 동작)
# =============================================================================

def demo_auto_trace():
    """LangChain을 사용하면 Trace가 자동 수집된다"""
    print("\n--- 자동 Trace 시연 ---")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=0
    )

    # 이 호출은 자동으로 LangSmith에 Trace로 기록됨
    print("  LLM 호출 중...")
    response = llm.invoke([
        SystemMessage(content="당신은 Python 전문가입니다. 간결하게 답변하세요."),
        HumanMessage(content="Python에서 리스트와 튜플의 차이점을 2줄로 설명해줘")
    ])

    print(f"  응답: {response.content[:100]}...")
    print("  -> LangSmith 대시보드에서 이 Trace를 확인하세요")


# =============================================================================
# 3. @traceable 데코레이터로 커스텀 Trace
# =============================================================================

@traceable(name="input_validation", run_type="chain")
def validate_input(user_input: str) -> dict:
    """사용자 입력 유효성 검사 - Trace에 기록됨"""
    issues = []

    if not user_input.strip():
        issues.append("빈 입력")
    if len(user_input) > 5000:
        issues.append("입력 길이 초과 (5000자)")
    if any(word in user_input.lower() for word in ["ignore instructions", "시스템 프롬프트"]):
        issues.append("잠재적 프롬프트 인젝션")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "input_length": len(user_input)
    }


@traceable(name="document_search", run_type="retriever")
def search_documents(query: str) -> list[dict]:
    """문서 검색 시뮬레이션 - retriever 타입으로 Trace"""
    # 실제로는 ChromaDB 등에서 검색
    mock_docs = [
        {"content": "Python의 리스트는 가변(mutable) 자료구조입니다.", "score": 0.92},
        {"content": "튜플은 불변(immutable) 자료구조로, 수정할 수 없습니다.", "score": 0.88},
        {"content": "리스트는 []로, 튜플은 ()로 생성합니다.", "score": 0.85},
    ]
    return mock_docs


@traceable(name="generate_answer", run_type="chain")
def generate_answer(query: str, docs: list[dict]) -> str:
    """답변 생성 - Trace에 기록"""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=0
    )

    context = "\n".join(doc["content"] for doc in docs)

    response = llm.invoke([
        SystemMessage(content=f"다음 컨텍스트를 참고하여 답변하세요:\n{context}"),
        HumanMessage(content=query)
    ])

    return response.content


@traceable(
    name="agent_pipeline",
    run_type="chain",
    metadata={"agent_version": "1.0.0", "demo": True},
    tags=["demo", "day4"]
)
def run_agent_pipeline(user_input: str) -> dict:
    """Agent 전체 파이프라인 - 최상위 Trace

    LangSmith에서 이 함수가 Root Trace가 되고,
    내부에서 호출하는 validate_input, search_documents, generate_answer가
    Child Span으로 계층 구조를 형성한다.
    """
    # Step 1: 입력 검증
    validation = validate_input(user_input)
    if not validation["is_valid"]:
        return {
            "status": "rejected",
            "reason": validation["issues"]
        }

    # Step 2: 문서 검색
    docs = search_documents(user_input)

    # Step 3: 답변 생성
    answer = generate_answer(user_input, docs)

    return {
        "status": "success",
        "answer": answer,
        "sources_count": len(docs)
    }


def demo_custom_trace():
    """커스텀 Trace 시연"""
    print("\n--- 커스텀 Trace 시연 ---")
    print("  Agent 파이프라인 실행 중...")

    result = run_agent_pipeline("Python에서 리스트와 튜플의 차이점은?")

    print(f"  상태: {result['status']}")
    print(f"  답변: {result.get('answer', 'N/A')[:100]}...")
    print(f"  참조 문서: {result.get('sources_count', 0)}개")
    print()
    print("  -> LangSmith에서 'agent_pipeline' Trace를 확인하세요")
    print("  -> 내부에 input_validation, document_search, generate_answer가")
    print("     Child Span으로 표시됩니다")


# =============================================================================
# 4. 메인 실행
# =============================================================================

def main():
    print("=" * 60)
    print("I DO: LangSmith 기본 설정 및 Trace 수집")
    print("=" * 60)

    # 환경 확인
    if not check_environment():
        print("\n환경 변수를 설정한 후 다시 실행하세요.")
        return

    # 자동 Trace
    demo_auto_trace()

    # 커스텀 Trace
    demo_custom_trace()

    print("\n" + "=" * 60)
    print("시연 완료!")
    print("https://smith.langchain.com/ 에서 Trace를 확인하세요")
    print(f"프로젝트: {os.environ.get('LANGSMITH_PROJECT', 'default')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
