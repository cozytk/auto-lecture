"""
MCP 서버: Git CLI 도구를 MCP로 래핑하기 — 함께 실습.

강사와 함께 TODO 부분을 채워 넣으세요.
"""

import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("git-tools")


@mcp.tool()
async def git_status(repo_path: str) -> str:
    """Git 저장소의 현재 상태를 조회합니다."""
    # TODO: subprocess.run()으로 git status --short 를 실행하세요.
    #   - capture_output=True, text=True, cwd=repo_path 를 사용합니다.
    #   - returncode가 0이 아니면 에러 메시지를 반환합니다.
    #   - 정상이면 stdout을 반환합니다.
    pass


@mcp.tool()
async def git_log(repo_path: str, count: int = 5) -> str:
    """Git 커밋 히스토리를 조회합니다."""
    # TODO: subprocess.run()으로 git log --max-count={count} --oneline 을 실행하세요.
    #   - count 파라미터를 f-string으로 명령어에 포함시킵니다.
    #   - 에러 처리 패턴은 git_status와 동일합니다.
    pass


if __name__ == "__main__":
    mcp.run()
