# Git 기본 워크플로우: init부터 commit까지

## 실습 목적

Git의 3영역(Working Directory, Staging Area, Repository)을 직접 경험하고, `git init`, `git add`, `git commit`, `git status`, `git log` 명령어를 체득한다.

## 사전 준비

- Git 설치 완료 (`git --version`으로 확인)
- 터미널(CLI) 기본 조작 가능 (cd, ls, mkdir, echo)

### Git 설치 안내

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update && sudo apt install git -y
```

**macOS**:
```bash
# Xcode Command Line Tools에 포함
xcode-select --install
# 또는 Homebrew로 설치
brew install git
```

설치 후 초기 설정:
```bash
git config --global user.name "본인 이름"
git config --global user.email "본인@이메일.com"
```

---

## I DO: 시연 관찰 (약 3분)

강사가 시연하는 과정을 관찰하세요. 직접 코드를 작성하지 않아도 됩니다.

### 시연 내용

Git 저장소를 초기화하고, 파일을 생성하여 Working Directory → Staging Area → Repository 흐름을 보여준다. `git status` 출력이 각 단계에서 어떻게 변하는지가 핵심이다.

### 시연 코드

`src/i-do/` 디렉토리의 스크립트를 실행합니다:

```bash
bash src/i-do/demo.sh
```

### 관찰 포인트

- `git status`에서 파일이 **빨간색**(Untracked/Modified)에서 **녹색**(Staged)으로 변하는 순간
- `git add` 전후로 `git status` 출력이 어떻게 달라지는지
- `git commit` 후 `git status`가 "clean" 상태가 되는 것
- `git log`에서 커밋 이력이 쌓이는 모습

---

## WE DO: 함께 실습 (약 7분)

강사와 함께 단계별로 명령어를 실행합니다.

### 1단계: README.md에 내용 추가

I DO에서 만든 프로젝트에 이어서 작업합니다. README.md에 설명을 추가합니다:

```bash
echo "Git 기초를 배우는 프로젝트입니다." >> README.md
```

### 2단계: 새 파일 생성

Python 파일을 하나 만듭니다:

```bash
echo "print('hello git')" > app.py
```

### 3단계: 상태 확인

두 파일의 상태를 확인합니다:

```bash
git status
# README.md → modified (빨간색)
# app.py → untracked (빨간색)
```

> 두 파일 모두 빨간색이지만 의미가 다릅니다. README.md는 "수정됨(modified)", app.py는 "추적되지 않음(untracked)"입니다.

### 4단계: 파일별로 스테이징하고 커밋

각 파일을 **별도의 커밋**으로 분리합니다:

```bash
git add README.md
git commit -m "docs: README 설명 추가"

git add app.py
git commit -m "feat: 메인 애플리케이션 추가"
```

### 5단계: 전체 이력 확인

```bash
git log --oneline
# 커밋 3개가 시간 역순으로 표시됨
```

### 확인 체크리스트

- [ ] `git status`에서 빨간색/녹색 변화를 확인했는가?
- [ ] `git log`에 커밋 3개가 보이는가?

참고 스크립트: `src/we-do/practice.sh`

---

## YOU DO: 독립 과제 (약 10분)

아래 과제를 스스로 해결하세요. 막히면 힌트를 참고하세요.

### 과제 설명

1. `config.txt` 파일을 생성하고 `debug=true` 내용을 작성한다
2. `app.py`를 수정하여 `print('hello world')`로 변경한다
3. **두 파일을 별도의 커밋으로 분리**하여 커밋한다 (한 번에 커밋하지 않을 것)
4. `git log --oneline`으로 이력을 확인한다 (총 5개 커밋이 보여야 함)

### 시작 방법

`src/you-do/challenge.sh` 파일의 TODO 주석을 채워서 완성하세요:

```bash
# 직접 터미널에서 명령어를 입력해도 됩니다
# 또는 스크립트를 수정하여 실행할 수도 있습니다
vi src/you-do/challenge.sh
bash src/you-do/challenge.sh
```

### 힌트

<details>
<summary>힌트 1</summary>

`echo "내용" > 파일명`으로 파일을 생성하거나 덮어쓸 수 있습니다.
`>` 는 덮어쓰기, `>>` 는 추가(append)입니다.

</details>

<details>
<summary>힌트 2</summary>

핵심은 `git add`에서 **파일명을 하나만 지정**하는 것입니다.
`git add .`을 쓰면 모든 변경 파일이 한꺼번에 스테이징되므로, 별도 커밋으로 분리할 수 없습니다.

```bash
git add config.txt    # config.txt만 스테이징
git commit -m "..."   # config.txt만 커밋
git add app.py        # 그다음 app.py를 스테이징
git commit -m "..."   # app.py만 커밋
```

</details>

### 정답 확인

과제를 완료한 후 `solution/` 디렉토리에서 정답 코드를 확인할 수 있습니다:

```bash
bash solution/challenge.sh
```

---

## 검증 방법

```bash
# 전체 검증 (Justfile 사용)
just test

# 수동 검증: git log에 5개 커밋이 있는지 확인
git log --oneline | wc -l
# 출력: 5
```

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| `git: command not found` | Git이 설치되지 않음 | 사전 준비의 설치 안내를 따르세요 |
| `nothing to commit` | `git add`를 하지 않고 커밋 시도 | `git add 파일명` 후 다시 커밋하세요 |
| `Please tell me who you are` | Git 사용자 설정이 안 됨 | `git config --global user.name "이름"` 및 `git config --global user.email "이메일"` 실행 |
| 커밋이 5개가 아님 | 파일을 분리하지 않고 한 번에 커밋함 | 처음부터 다시 시도하세요. `git add`에 파일명을 하나만 지정하세요 |
| `fatal: not a git repository` | git init을 하지 않은 디렉토리에서 실행 | `git init`을 먼저 실행하세요 |
