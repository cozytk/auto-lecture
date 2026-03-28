"""
Tool 정의

Agent가 사용할 수 있는 도구(Tool)를 정의한다.
각 Tool은 @tool 데코레이터로 정의하며, Pydantic 모델로 입력을 검증한다.

TODO: 프로젝트에 맞게 아래 항목을 수정하세요.
  1. 기존 예시 Tool을 삭제하고 프로젝트 Tool 추가
  2. 각 Tool의 입력 스키마를 Pydantic 모델로 정의
  3. Tool 함수 내부에 실제 로직 구현
  4. get_tools()에 새로운 Tool 등록
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# ============================================================
# Tool 입력 스키마 정의 (Pydantic)
# ============================================================
class SearchInput(BaseModel):
    """검색 도구 입력 스키마"""
    query: str = Field(description="검색할 키워드 또는 질문")
    max_results: int = Field(default=5, description="최대 검색 결과 수 (1~10)")


class CalculateInput(BaseModel):
    """계산 도구 입력 스키마"""
    expression: str = Field(description="계산할 수식 (예: '2 + 3 * 4')")


# ============================================================
# Tool 함수 정의
# ============================================================
@tool(args_schema=SearchInput)
def search_tool(query: str, max_results: int = 5) -> str:
    """키워드로 정보를 검색합니다.

    TODO: 실제 검색 로직으로 교체하세요.
    예시: 웹 검색 API, DB 쿼리, 파일 검색 등
    """
    # 스캐폴드: 더미 결과 반환
    return f"'{query}'에 대한 검색 결과 {max_results}건을 찾았습니다. (TODO: 실제 검색 로직 구현)"


@tool(args_schema=CalculateInput)
def calculate_tool(expression: str) -> str:
    """수학 계산을 수행합니다.

    TODO: 프로젝트에 필요 없으면 삭제하세요.
    """
    try:
        # 안전한 수식 계산 (eval 대신 제한된 파서 사용 권장)
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "오류: 허용되지 않은 문자가 포함되어 있습니다."

        result = eval(expression)  # 프로덕션에서는 ast.literal_eval 또는 수식 파서 사용
        return f"계산 결과: {expression} = {result}"
    except Exception as e:
        return f"계산 오류: {str(e)}"


# TODO: 프로젝트에 맞는 Tool을 추가하세요.
# 예시:
#
# class GitHubPRInput(BaseModel):
#     repo: str = Field(description="GitHub 저장소 (owner/repo)")
#     pr_number: int = Field(description="PR 번호")
#
# @tool(args_schema=GitHubPRInput)
# def get_pr_diff(repo: str, pr_number: int) -> str:
#     """GitHub PR의 코드 변경 내용을 가져옵니다."""
#     import httpx
#     response = httpx.get(f"https://api.github.com/repos/{repo}/pulls/{pr_number}")
#     return response.text


# ============================================================
# Tool 목록 반환
# ============================================================
def get_tools() -> list:
    """Agent에 바인딩할 Tool 목록을 반환한다.

    TODO: 프로젝트에 사용할 Tool만 남기세요.
    """
    return [
        search_tool,
        calculate_tool,
    ]


if __name__ == "__main__":
    # Tool 동작 테스트
    tools = get_tools()
    print(f"등록된 Tool 수: {len(tools)}")
    for t in tools:
        print(f"  - {t.name}: {t.description}")

    # 개별 Tool 테스트
    print("\n--- search_tool 테스트 ---")
    print(search_tool.invoke({"query": "LangGraph 사용법", "max_results": 3}))

    print("\n--- calculate_tool 테스트 ---")
    print(calculate_tool.invoke({"expression": "2 + 3 * 4"}))
