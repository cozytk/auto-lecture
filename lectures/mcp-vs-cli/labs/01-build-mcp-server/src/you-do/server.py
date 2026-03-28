"""
MCP 서버: Git CLI 도구를 MCP로 래핑하기 — 독립 과제.

WE DO에서 완성한 git_status, git_log는 이미 구현되어 있습니다.
TODO 표시된 git_diff와 git_branch_list를 직접 구현하세요.
"""

import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("git-tools")


# --- WE DO에서 완성한 도구 (수정 불필요) ---


@mcp.tool()
async def git_status(repo_path: str) -> str:
    """Git 저장소의 현재 상태를 조회합니다."""
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True,
        cwd=repo_path,
    )
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout or "(변경사항 없음)"


@mcp.tool()
async def git_log(repo_path: str, count: int = 5) -> str:
    """Git 커밋 히스토리를 조회합니다."""
    result = subprocess.run(
        ["git", "log", f"--max-count={count}", "--oneline"],
        capture_output=True,
        text=True,
        cwd=repo_path,
    )
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout or "(커밋 없음)"


# --- 여기서부터 직접 구현하세요 ---


@mcp.tool()
async def git_diff(repo_path: str, staged: bool = False) -> str:
    """변경된 파일의 diff를 조회합니다.

    Args:
        repo_path: Git 저장소 경로
        staged: True이면 스테이징된 변경사항만 표시
    """
    # TODO: git diff 명령어를 실행하세요.
    #   - staged=True이면 --cached 플래그를 추가합니다.
    #   - subprocess.run() 패턴은 위의 도구와 동일합니다.
    pass


@mcp.tool()
async def git_branch_list(repo_path: str, all_branches: bool = False) -> str:
    """브랜치 목록을 조회합니다.

    Args:
        repo_path: Git 저장소 경로
        all_branches: True이면 원격 브랜치도 포함
    """
    # TODO: git branch 명령어를 실행하세요.
    #   - all_branches=True이면 -a 플래그를 추가합니다.
    #   - subprocess.run() 패턴은 위의 도구와 동일합니다.
    pass


if __name__ == "__main__":
    mcp.run()
