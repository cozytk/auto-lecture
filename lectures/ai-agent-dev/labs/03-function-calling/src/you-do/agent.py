"""
YOU DO: Function Calling Agent - 독립 과제

본인의 Agent에 맞는 Tool을 3개 이상 정의하고 Agent 루프를 구현하세요.
아래 주간 보고서 자동화 시나리오를 사용하거나 Session 3에서 설계한 Agent를 구현하세요.
"""

import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

# 시나리오: 주간 보고서 자동화 Agent
# Pain: 매주 금요일 주간 보고서 작성에 3시간 소요
# Tasks: Jira 티켓 조회 / Git 커밋 요약 / Slack 논의 추출 / Confluence 저장

# TODO: 아래 3개 Tool을 완성하세요 (description은 30자 이상 상세히 작성)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_jira_tickets",
            "description": "TODO: 이 Tool이 언제/왜 사용되는지 30자 이상으로 설명하세요",
            "parameters": {
                "type": "object",
                "properties": {
                    # TODO: team_id, week_start 파라미터를 정의하세요
                },
                "required": [],  # TODO: 필수 파라미터를 지정하세요
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_git_commits",
            "description": "TODO: 30자 이상 description",
            "parameters": {
                "type": "object",
                "properties": {
                    # TODO: repo, since 파라미터를 정의하세요
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_report",
            "description": "TODO: 30자 이상 description",
            "parameters": {
                "type": "object",
                "properties": {
                    # TODO: title, content 파라미터를 정의하세요
                },
                "required": [],
            },
        },
    },
]


def execute_tool(name: str, args: dict) -> dict:
    """Tool 실행 - 실제 환경에서는 각 서비스 API를 호출한다."""
    if name == "get_jira_tickets":
        # TODO: 더미 Jira 티켓 데이터를 반환하세요
        return {}
    if name == "get_git_commits":
        # TODO: 더미 Git 커밋 데이터를 반환하세요
        return {}
    if name == "save_report":
        # TODO: 저장 성공 응답을 반환하세요
        return {}
    return {"error": f"Unknown tool: {name}"}


def run_agent(user_message: str) -> str:
    """Function Calling Agent 루프를 구현하세요."""
    messages = [
        {
            "role": "system",
            "content": (
                "당신은 주간 보고서 자동화 Agent입니다. "
                "요청된 팀의 주간 활동을 Jira와 Git에서 수집하여 보고서를 작성하세요."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    # TODO: Tool 호출이 없을 때까지 반복하는 Agent 루프를 구현하세요
    return "TODO: Agent 루프 구현 필요"


# 검증용 테스트 입력
test_inputs = [
    # Tool 호출이 필요한 질문
    "backend 팀의 2025-03-03 주간 보고서를 작성해주세요",
    # Tool 호출이 필요 없는 질문
    "주간 보고서는 보통 어떤 내용으로 구성되나요?",
    # 여러 Tool을 순차 호출해야 하는 질문
    "backend 팀 Jira 완료 티켓과 Git 커밋을 수집해서 보고서로 저장해주세요",
]

if __name__ == "__main__":
    print("=== Function Calling Agent 테스트 ===\n")
    for query in test_inputs:
        print(f"질문: {query}")
        result = run_agent(query)
        print(f"답변: {result}\n")
