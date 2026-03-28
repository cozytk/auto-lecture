"""
MCP 서버: Git CLI 도구를 MCP로 래핑하는 완성 예제.

강사 시연용 — 학생은 관찰만 합니다.
"""

import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("git-tools")


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


@mcp.tool()
async def git_diff(repo_path: str, staged: bool = False) -> str:
    """변경된 파일의 diff를 조회합니다."""
    cmd = ["git", "diff"]
    if staged:
        cmd.append("--cached")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=repo_path,
    )
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout or "(변경사항 없음)"


@mcp.tool()
async def git_branch_list(repo_path: str, all_branches: bool = False) -> str:
    """브랜치 목록을 조회합니다."""
    cmd = ["git", "branch"]
    if all_branches:
        cmd.append("-a")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=repo_path,
    )
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout or "(브랜치 없음)"


if __name__ == "__main__":
    mcp.run()
