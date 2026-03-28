# MCP 서버 만들기 — CLI 도구를 MCP로 감싸기

## 실습 목적

기존 CLI 도구를 MCP 서버로 래핑하는 패턴을 직접 구현하여, MCP의 동작 원리(JSON-RPC 통신, 도구 등록, 정형 응답)를 체득한다.

## 사전 준비

- Python 3.10 이상 설치
- `uv` 패키지 매니저 설치 (또는 `pip` 사용 가능)
- 터미널에서 `git --version` 실행 가능해야 함 (CLI 도구 래핑 대상)
- Claude Desktop 또는 MCP Inspector (선택 — 최종 연동 테스트용)

```bash
# uv 설치 (없는 경우)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python 버전 확인
python3 --version
```

---

## I DO: 시연 관찰 (약 10분)

강사가 시연하는 코드를 관찰하세요. 직접 코드를 작성하지 않아도 됩니다.

### 시연 내용

강사가 `git status`와 `git log`를 MCP 도구로 제공하는 서버를 만들고, MCP Inspector로 호출하는 과정을 보여줍니다.

### 시연 코드

`src/i-do/` 디렉토리의 코드를 실행합니다:

```bash
# 의존성 설치
just setup

# MCP 서버 실행 (MCP Inspector에서 연결)
just run
```

### 관찰 포인트

- MCP 서버가 도구(tool)를 **등록**하는 방법: `@mcp.tool()` 데코레이터
- CLI 명령어(`git status`)를 실행하고 결과를 **정형 JSON**으로 반환하는 흐름
- MCP Inspector에서 도구 목록이 **동적으로 검색(discovery)** 되는 모습
- CLI 출력(비정형 텍스트)과 MCP 응답(정형 JSON)의 차이

---

## WE DO: 함께 실습 (약 15분)

강사와 함께 단계별로 MCP 서버를 완성합니다.

### 1단계: 프로젝트 초기화

```bash
cd src/we-do/
```

`server.py` 파일을 열어봅시다. 기본 구조가 준비되어 있습니다.

### 2단계: git_status 도구 구현

`src/we-do/server.py`의 첫 번째 TODO를 함께 채워봅시다:

```python
@mcp.tool()
async def git_status(repo_path: str) -> str:
    """Git 저장소의 현재 상태를 조회합니다."""
    # TODO: subprocess로 git status를 실행하고 결과를 반환하세요
```

**함께 확인할 것**:
- `subprocess.run()`에서 `capture_output=True`와 `text=True`를 왜 쓰는가?
- 에러 처리: `returncode != 0`일 때 어떻게 할 것인가?

### 3단계: git_log 도구 구현

두 번째 TODO를 함께 채워봅시다:

```python
@mcp.tool()
async def git_log(repo_path: str, count: int = 5) -> str:
    """Git 커밋 히스토리를 조회합니다."""
    # TODO: subprocess로 git log를 실행하고 결과를 반환하세요
```

**함께 확인할 것**:
- `count` 파라미터를 CLI 명령어에 어떻게 전달하는가?
- MCP 도구의 파라미터 타입이 자동으로 JSON Schema로 변환되는 점

### 4단계: 서버 실행 및 테스트

```bash
# 서버 실행
uv run python server.py

# 다른 터미널에서 MCP Inspector로 테스트
npx @modelcontextprotocol/inspector uv run python server.py
```

---

## YOU DO: 독립 과제 (약 15분)

아래 과제를 스스로 해결하세요. 막히면 힌트를 참고하세요.

### 과제 설명

`src/you-do/server.py`에 아래 2개의 MCP 도구를 **직접** 추가하세요:

1. **`git_diff`**: 변경된 파일의 diff를 보여주는 도구
   - 파라미터: `repo_path` (str), `staged` (bool, 기본값 False)
   - `staged=True`이면 스테이징된 변경사항만 표시

2. **`git_branch_list`**: 브랜치 목록을 보여주는 도구
   - 파라미터: `repo_path` (str), `all_branches` (bool, 기본값 False)
   - `all_branches=True`이면 원격 브랜치도 포함

### 시작 방법

`src/you-do/` 디렉토리의 템플릿 코드를 수정하세요:

```bash
cd src/you-do/
# TODO가 표시된 부분을 채워 넣으세요
```

### 힌트

<details>
<summary>힌트 1: git diff 명령어 구성</summary>

`git diff`는 기본적으로 워킹 디렉토리의 변경사항을 보여줍니다.
스테이징된 변경사항을 보려면 `--cached` (또는 `--staged`) 플래그를 추가합니다.

```python
cmd = ["git", "diff"]
if staged:
    cmd.append("--cached")
```
</details>

<details>
<summary>힌트 2: git branch 명령어 구성</summary>

`git branch`는 로컬 브랜치만 보여줍니다.
원격 브랜치를 포함하려면 `-a` 플래그를 사용합니다.

```python
cmd = ["git", "branch"]
if all_branches:
    cmd.append("-a")
```
</details>

<details>
<summary>힌트 3: 에러 처리 패턴</summary>

I DO와 WE DO에서 본 패턴을 재활용하세요:

```python
result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_path)
if result.returncode != 0:
    return f"Error: {result.stderr}"
return result.stdout
```
</details>

### 정답 확인

과제를 완료한 후 `solution/` 디렉토리에서 정답 코드를 확인할 수 있습니다.

```bash
diff src/you-do/server.py solution/server.py
```

---

## 검증 방법

```bash
# 전체 검증 실행
just test
```

검증 항목:
- [ ] 서버가 에러 없이 시작되는가
- [ ] MCP Inspector에서 도구 4개(git_status, git_log, git_diff, git_branch_list)가 보이는가
- [ ] 각 도구를 호출했을 때 올바른 결과가 반환되는가
- [ ] 존재하지 않는 경로를 입력했을 때 에러 메시지가 반환되는가

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| `ModuleNotFoundError: mcp` | MCP SDK 미설치 | `uv add "mcp[cli]"` 실행 |
| `git: command not found` | Git 미설치 | OS별 Git 설치 (brew install git / apt install git) |
| MCP Inspector 연결 실패 | Node.js 미설치 또는 버전 낮음 | `node --version`으로 18+ 확인 |
| `Permission denied` 에러 | 저장소 접근 권한 없음 | `repo_path`가 유효한 git 저장소인지 확인 |
| `not a git repository` | 잘못된 경로 지정 | `.git` 디렉토리가 있는 경로를 지정 |
