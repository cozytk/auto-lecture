"""
YOU DO 정답: Function Calling Agent - 주간 보고서 자동화

학생이 과제 완료 후 참고하는 정답 코드입니다.
"""

import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = os.environ.get("MODEL", "moonshotai/kimi-k2")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_jira_tickets",
            "description": (
                "팀의 주간 Jira 티켓을 조회합니다. "
                "완료(Done)와 진행 중(In Progress) 티켓을 모두 반환합니다. "
                "주간 보고서 작성 시 팀 작업 현황 파악에 사용하세요."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "team_id": {
                        "type": "string",
                        "description": "팀 식별자 (예: backend, frontend)",
                    },
                    "week_start": {
                        "type": "string",
                        "description": "조회 주 시작일 (YYYY-MM-DD 형식)",
                    },
                },
                "required": ["team_id", "week_start"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_git_commits",
            "description": (
                "Git 저장소의 주간 커밋 내역을 조회합니다. "
                "커밋 메시지와 작성자를 포함합니다. "
                "주간 보고서의 개발 활동 섹션 작성에 사용하세요."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "repo": {
                        "type": "string",
                        "description": "저장소 이름 (예: backend-api)",
                    },
                    "since": {
                        "type": "string",
                        "description": "조회 시작일 (YYYY-MM-DD 형식)",
                    },
                },
                "required": ["repo", "since"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_report",
            "description": (
                "완성된 주간 보고서를 저장합니다. "
                "Confluence 또는 지정된 저장소에 보고서를 업로드합니다. "
                "모든 데이터 수집과 요약이 완료된 후 마지막에 호출하세요."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "보고서 제목 (예: backend팀 2025-03-03 주간 보고서)",
                    },
                    "content": {
                        "type": "string",
                        "description": "보고서 본문 (마크다운 형식)",
                    },
                },
                "required": ["title", "content"],
            },
        },
    },
]


def execute_tool(name: str, args: dict) -> dict:
    """Tool 실행 - 실제 환경에서는 각 서비스 API를 호출한다."""
    if name == "get_jira_tickets":
        return {
            "team": args.get("team_id"),
            "week": args.get("week_start"),
            "tickets": [
                {"id": "BE-101", "title": "API 인증 모듈 구현", "status": "Done"},
                {"id": "BE-102", "title": "데이터베이스 마이그레이션", "status": "Done"},
                {"id": "BE-103", "title": "성능 최적화", "status": "In Progress"},
            ],
        }
    if name == "get_git_commits":
        return {
            "repo": args.get("repo"),
            "commits": [
                {"hash": "a1b2c3", "message": "feat: JWT 토큰 갱신 로직 추가", "author": "kim"},
                {"hash": "d4e5f6", "message": "fix: 세션 만료 버그 수정", "author": "lee"},
                {"hash": "g7h8i9", "message": "refactor: DB 커넥션 풀 설정 개선", "author": "park"},
            ],
        }
    if name == "save_report":
        # 실제 환경에서는 Confluence API 등을 호출한다
        print(f"\n[보고서 저장됨]\n제목: {args.get('title')}\n내용 길이: {len(args.get('content', ''))}자")
        return {"success": True, "url": "https://confluence.example.com/weekly-report"}
    return {"error": f"Unknown tool: {name}"}


def run_agent(user_message: str) -> str:
    """Function Calling Agent 루프"""
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

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        assistant_msg = response.choices[0].message

        if not assistant_msg.tool_calls:
            return assistant_msg.content

        messages.append(assistant_msg)
        for tc in assistant_msg.tool_calls:
            fn_args = json.loads(tc.function.arguments)
            result = execute_tool(tc.function.name, fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False),
            })


test_inputs = [
    "backend 팀의 2025-03-03 주간 보고서를 작성해주세요",
    "주간 보고서는 보통 어떤 내용으로 구성되나요?",
    "backend 팀 Jira 완료 티켓과 Git 커밋을 수집해서 보고서로 저장해주세요",
]

if __name__ == "__main__":
    print("=== Function Calling Agent 테스트 ===\n")
    for query in test_inputs:
        print(f"질문: {query}")
        result = run_agent(query)
        print(f"답변: {result}\n")
