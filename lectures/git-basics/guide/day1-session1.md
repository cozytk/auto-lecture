# Git 기초: 버전관리 개념부터 브랜치까지

<callout icon="📖" color="blue_bg">
	**학습 목표**
	1. 버전관리의 필요성을 이해하고 Git의 핵심 개념(Working Directory, Staging Area, Repository)을 설명할 수 있다
	2. `git init`, `git add`, `git commit`, `git status`, `git log` 명령어로 로컬 저장소를 관리할 수 있다
	3. 브랜치를 생성하고 병합(merge)하여 독립적인 작업 흐름을 운영할 수 있다
</callout>

---

## 1. 버전관리란 무엇인가

### 왜 이것이 중요한가

코드를 작성하다 보면 이런 경험이 있을 것이다.

`report_final.docx`, `report_final_v2.docx`, `report_진짜최종.docx`...
파일 이름으로 버전을 관리하다 어떤 것이 진짜 최종인지 모르게 된다.

코드에서는 상황이 더 심각하다.
잘 돌아가던 기능을 수정했는데, 이전 상태로 돌아갈 수 없다.
팀원이 같은 파일을 동시에 수정했는데, 누구의 코드가 덮어씌워졌는지 모른다.

**버전관리 시스템(VCS)** 이 바로 이 문제의 해답이다.
파일의 변경 이력을 체계적으로 기록하고, 언제든 과거 상태로 되돌릴 수 있게 해 준다.

> 버전관리가 없으면 → 코드 한 줄 잘못 고치면 **복구 불가능**.
> 버전관리가 있으면 → 언제든 **원하는 시점으로 되돌릴 수 있음**.

### 핵심 원리

**비유로 이해하기**: 게임의 **세이브 포인트**를 떠올려 보십시오.

→ 게임에서 중요한 지점마다 세이브하면, 실패해도 그 지점부터 다시 시작할 수 있다.
→ 버전관리도 동일하다. 코드의 의미 있는 변경마다 "세이브(커밋)"하면, 언제든 그 시점으로 되돌릴 수 있다.

**실제 동작**: 버전관리 시스템은 파일의 **변경 사항(diff)** 을 시간순으로 기록한다.
→ 전체 파일을 매번 복사하는 것이 아니다.
→ "무엇이 바뀌었는지"만 저장하므로 효율적이다.

**비유의 한계**: 게임 세이브는 한 명만 사용하지만, Git은 **여러 사람이 동시에** 각자의 세이브 포인트를 만들고 합칠 수 있다. 이 부분은 뒤에서 배울 브랜치에서 다룬다.

### 실무에서의 의미

실무에서 버전관리는 선택이 아닌 **필수**다.
모든 소프트웨어 회사가 버전관리 시스템을 사용한다.

Linux 커널 프로젝트가 대표적 사례다.
전 세계 수천 명의 개발자가 동시에 코드를 수정하지만, Git 덕분에 체계적으로 관리된다.

### 다른 접근법과의 비교

| 구분 | 파일 복사 방식 | 중앙집중형 VCS (SVN) | 분산형 VCS (Git) |
|------|---------------|---------------------|-----------------|
| 이력 관리 | 파일명으로 구분 | 중앙 서버에 기록 | 로컬+원격 모두 기록 |
| 협업 | 파일 공유 (충돌 빈발) | 서버 연결 필수 | 오프라인 작업 가능 |
| 속도 | - | 서버 의존 (느림) | 로컬 처리 (빠름) |
| 복구 | 사실상 불가능 | 서버 장애 시 위험 | 모든 복제본이 전체 이력 보유 |

### 주의사항과 흔한 오해

> **오해 1**: "Git은 백업 도구다"
> → **실제**: Git은 백업이 아니라 **변경 이력 추적** 도구다. 단순 백업은 파일 복사로도 되지만, "누가, 언제, 왜 바꿨는지"를 기록하는 것이 Git의 핵심 가치다.

> **오해 2**: "Git과 GitHub는 같은 것이다"
> → **실제**: Git은 **로컬에서 동작하는 버전관리 도구**다. GitHub는 Git 저장소를 **온라인에서 호스팅**하는 서비스다. Git 없이 GitHub를 쓸 수 없지만, GitHub 없이 Git은 사용할 수 있다.

### 코드 예제

버전관리의 효과를 터미널에서 확인해 보자:

```bash
# 버전관리 없이: 파일 복사 방식
cp app.py app_v1.py
cp app.py app_v2.py
cp app.py app_final.py
# → 어떤 파일이 최신인지 혼란

# 버전관리 있을 때: Git 방식
git log --oneline
# a1b2c3d 로그인 기능 추가
# e4f5g6h 회원가입 폼 구현
# i7j8k9l 프로젝트 초기 설정
# → 변경 이력이 명확하게 기록됨
```

이 `git log` 명령어에서 보이는 각 줄이 하나의 **커밋(commit)** 이다.
커밋을 만들려면 먼저 Git의 3가지 영역을 이해해야 한다.

### Q&A

**Q: 혼자 개발하는데도 Git이 필요한가요?**
A: 반드시 필요하다. 혼자 개발해도 "어제 수정한 코드로 돌아가고 싶다"는 상황은 반드시 발생한다. Git이 있으면 `git checkout`이나 `git revert`로 즉시 복구할 수 있다. 또한 실험적인 기능을 브랜치로 분리해서 안전하게 시도할 수 있다. 더 깊이 알고 싶다면 'Git branching strategy'를 검색해 보십시오.

**Q: SVN을 쓰던 팀인데 Git으로 바꿔야 하나요? (← 주니어 개발자 배경)**
A: 현재 업계 표준은 Git이다. SVN에서 Git으로 전환하는 가장 큰 이유는 **오프라인 작업**과 **브랜치 비용**이다. SVN은 브랜치를 만드는 데 디렉토리 전체를 복사하지만, Git은 포인터 하나만 생성하므로 거의 비용이 없다. 다만 SVN이 잘 동작하고 있고 팀이 만족한다면, 무리하게 전환할 필요는 없다. 더 깊이 알고 싶다면 'Git vs SVN migration'을 검색해 보십시오.

**Q: Git을 GUI 도구로만 쓰면 안 되나요?**
A: GUI 도구(GitKraken, SourceTree 등)는 시각적으로 편리하다. 하지만 CLI 명령어를 먼저 익혀야 GUI가 내부에서 무엇을 하는지 이해할 수 있다. 문제가 발생했을 때 CLI 없이는 디버깅이 어렵다. CLI를 먼저 익히고 GUI를 병행하는 것을 권장한다. 더 깊이 알고 싶다면 'Git GUI vs CLI'를 검색해 보십시오.

---

## 2. Git의 3가지 영역과 기본 명령어

### 왜 이것이 중요한가

앞서 버전관리가 "세이브 포인트를 만드는 것"이라 했다.
그런데 Git에서 세이브(커밋)를 하려면, 파일이 거치는 **3단계 영역**을 이해해야 한다.

이 구조를 모르면 이런 상황이 벌어진다:
- 파일을 수정했는데 `git commit`이 "nothing to commit"이라고 한다
- 어떤 파일은 커밋에 포함되고 어떤 파일은 빠진다
- `git status`의 출력이 무슨 뜻인지 모르겠다

Git의 3영역을 이해하면, 위 상황이 모두 **당연한 동작**이 된다.

### 핵심 원리

**비유로 이해하기**: **택배 발송 과정**을 떠올려 보십시오.

→ **물건 준비 (Working Directory)**: 집에서 보낼 물건을 고른다. 아직 포장하지 않은 상태다.
→ **박스에 담기 (Staging Area)**: 보낼 물건을 택배 상자에 넣는다. 아직 발송하지는 않았다.
→ **발송 완료 (Repository)**: 택배를 발송한다. 이제 이력이 남고, 추적할 수 있다.

**실제 동작**:

```
Working Directory → (git add) → Staging Area → (git commit) → Repository
   작업 공간              스테이징 영역              저장소
   파일 수정              커밋할 파일 선택            변경 이력 확정
```

→ **Working Directory**: 실제 파일을 편집하는 공간
→ **Staging Area (Index)**: 다음 커밋에 포함할 변경 사항을 모아두는 공간
→ **Repository (.git)**: 커밋된 이력이 영구 저장되는 공간

**비유의 한계**: 택배는 한 번 보내면 끝이지만, Git 커밋은 언제든 **과거 이력을 조회**하고 **되돌릴 수 있다**. 또한 택배 상자에 넣었다가 다시 뺄 수 있듯이, Staging Area에 올린 파일도 `git reset`으로 다시 내릴 수 있다.

### 실무에서의 의미

Staging Area가 있기 때문에 **커밋 단위를 정밀하게 제어**할 수 있다.
파일 10개를 수정했더라도, 관련된 3개만 골라서 하나의 커밋으로 만들 수 있다.

이는 코드 리뷰에서 큰 차이를 만든다.
"로그인 기능 추가"와 "오타 수정"이 한 커밋에 섞여 있으면 리뷰어가 혼란스럽다.
Staging Area 덕분에 의미 있는 단위로 커밋을 분리할 수 있다.

### 다른 접근법과의 비교

| 구분 | Staging Area 없는 VCS (SVN 등) | Git (Staging Area 있음) |
|------|-------------------------------|------------------------|
| 커밋 단위 | 변경된 전체 파일이 커밋됨 | 원하는 파일만 선택 가능 |
| 실수 방지 | 의도치 않은 파일이 포함될 수 있음 | `git status`로 확인 후 커밋 |
| 커밋 메시지 | 여러 작업이 하나에 섞임 | 작업 단위별로 분리 가능 |

### 주의사항과 흔한 오해

> **오해 1**: "`git add`를 하면 커밋이 된다"
> → **실제**: `git add`는 Staging Area에 올리는 것일 뿐이다. 실제 이력에 기록하려면 반드시 `git commit`을 해야 한다. `git add` → `git commit`은 **항상 2단계**다.

> **오해 2**: "한 번 `git add`한 파일은 이후 수정해도 자동으로 스테이징된다"
> → **실제**: `git add` 이후에 파일을 다시 수정하면, **수정된 내용은 스테이징되지 않는다**. 수정할 때마다 `git add`를 다시 해야 한다. Git은 `git add` 시점의 파일 상태를 스냅샷으로 저장한다.

### 코드 예제

Git 저장소를 처음부터 만들어 보자:

```bash
# 1. 프로젝트 디렉토리 생성 및 Git 초기화
mkdir my-project
cd my-project
git init
# Initialized empty Git repository in /my-project/.git/

# 2. 파일 생성 후 상태 확인
echo "Hello Git" > hello.txt
git status
# Untracked files: hello.txt  ← Working Directory에만 있음

# 3. Staging Area에 추가
git add hello.txt
git status
# Changes to be committed: new file: hello.txt  ← Staging Area에 올라감

# 4. 커밋 (Repository에 기록)
git commit -m "첫 번째 커밋: hello.txt 추가"
# [main (root-commit) a1b2c3d] 첫 번째 커밋: hello.txt 추가

# 5. 이력 확인
git log --oneline
# a1b2c3d 첫 번째 커밋: hello.txt 추가
```

잘못된 예 - `git add` 없이 커밋 시도:

```bash
echo "new line" >> hello.txt
git commit -m "내용 추가"
# nothing to commit  ← Staging Area가 비어 있으므로 커밋 불가!

# 올바른 방법: add → commit
git add hello.txt
git commit -m "hello.txt에 내용 추가"
```

이제 기본 명령어로 로컬 저장소를 관리할 수 있다.
그런데 새로운 기능을 실험하고 싶을 때, main 코드를 건드리지 않고 작업할 방법이 필요하다.
다음에 배울 **브랜치**가 바로 그 해결책이다.

### Q&A

**Q: `git add .`과 `git add 파일명`의 차이는 무엇인가요?**
A: `git add .`은 현재 디렉토리의 **모든 변경 파일**을 Staging Area에 올린다. `git add 파일명`은 **지정한 파일만** 올린다. 실무에서는 의도하지 않은 파일(로그, 임시파일 등)이 커밋되는 것을 방지하기 위해 `git add 파일명`으로 명시적으로 추가하는 것을 권장한다. `.gitignore` 파일을 함께 사용하면 더 안전하다. 더 깊이 알고 싶다면 'gitignore patterns'를 검색해 보십시오.

**Q: 커밋 메시지는 어떻게 쓰는 게 좋나요? (← 주니어 개발자 배경)**
A: 커밋 메시지는 **"무엇을 왜 변경했는지"** 를 담아야 한다. "수정함", "업데이트"처럼 모호한 메시지는 나중에 이력을 추적할 때 쓸모가 없다. 일반적으로 `feat: 로그인 기능 추가`, `fix: 비밀번호 검증 오류 수정` 같은 형식을 사용한다. 팀에서 정한 컨벤션이 있다면 그것을 따른다. 더 깊이 알고 싶다면 'Conventional Commits'를 검색해 보십시오.

**Q: `git status`에 나오는 색상(빨간색, 녹색)은 무엇을 의미하나요?**
A: **빨간색**은 Working Directory에서 변경되었지만 아직 스테이징되지 않은 파일이다. **녹색**은 Staging Area에 올라가서 다음 커밋에 포함될 파일이다. 색상만 봐도 "이 파일이 어느 영역에 있는지" 즉시 알 수 있다. `git status`는 Git에서 가장 자주 쓰는 명령어이므로, 출력을 읽는 습관을 들이는 것이 좋다. 더 깊이 알고 싶다면 'git status short format'을 검색해 보십시오.

---

## 3. 브랜치와 병합

### 왜 이것이 중요한가

앞서 `git commit`으로 변경 이력을 기록하는 방법을 배웠다.
그런데 한 가지 질문이 생긴다.

"새로운 기능을 개발하다가 실패하면 어떻게 하지?"

main 브랜치에서 직접 작업하면, 실패한 코드가 원본에 남는다.
이를 되돌리려면 커밋을 하나씩 취소해야 하는데, 이미 다른 사람이 그 위에 작업했다면 큰 문제가 된다.

**브랜치(branch)** 는 이 문제를 해결한다.
원본을 건드리지 않고, **독립된 작업 공간**을 만들어 준다.
실험이 성공하면 합치고, 실패하면 브랜치만 삭제하면 된다.

### 핵심 원리

**비유로 이해하기**: **평행 우주**를 떠올려 보십시오.

→ 현재 세계(main 브랜치)에서 **분기점**을 만들어 평행 우주(새 브랜치)를 생성한다.
→ 평행 우주에서 마음껏 실험한다. 원래 세계에는 영향이 없다.
→ 실험 결과가 좋으면 원래 세계에 **합친다(merge)**.
→ 결과가 나쁘면 평행 우주를 **없애면** 된다.

**실제 동작**:

```
main:      A --- B --- C
                        \
feature:                 D --- E     ← 독립 작업

합친 후(merge):
main:      A --- B --- C --- M       ← D, E의 변경이 반영됨
```

→ 브랜치는 커밋 이력의 **포인터**다.
→ 새 브랜치를 만드는 비용은 거의 **제로**다 (41바이트 파일 하나 생성).
→ `git merge`로 두 브랜치의 변경 사항을 합친다.

**비유의 한계**: 평행 우주와 달리, Git 브랜치는 합칠 때 **충돌(conflict)** 이 발생할 수 있다. 두 브랜치가 같은 파일의 같은 줄을 다르게 수정한 경우다. 이때는 사람이 직접 어떤 내용을 선택할지 결정해야 한다.

### 실무에서의 의미

실무에서 브랜치는 **기능 개발의 기본 단위**다.
하나의 기능 = 하나의 브랜치가 일반적인 워크플로우다.

GitHub에서 Pull Request를 만들 때도 브랜치가 기반이다.
`feature/login` 브랜치에서 작업한 내용을 `main`에 합쳐 달라고 요청하는 것이 PR이다.

### 다른 접근법과의 비교

| 구분 | 브랜치 없이 작업 | 브랜치 사용 |
|------|-----------------|------------|
| 실험 | main에서 직접 수정 → 실패 시 복구 어려움 | 별도 브랜치에서 실험 → 실패해도 삭제만 하면 됨 |
| 협업 | 동시 수정 시 충돌 빈발 | 각자 브랜치에서 작업 후 병합 |
| 배포 | 개발 중인 코드가 배포에 섞임 | main은 항상 안정 상태 유지 |

### 주의사항과 흔한 오해

> **오해 1**: "브랜치를 만들면 파일이 복사된다"
> → **실제**: Git 브랜치는 파일 복사가 아니라 **커밋을 가리키는 포인터**다. 브랜치를 아무리 많이 만들어도 저장 공간이 거의 늘지 않는다. 이것이 SVN의 브랜치(디렉토리 복사)와 근본적으로 다른 점이다.

> **오해 2**: "merge하면 항상 충돌이 난다"
> → **실제**: 두 브랜치가 **같은 파일의 같은 줄**을 수정한 경우에만 충돌이 발생한다. 서로 다른 파일을 수정했거나, 같은 파일이라도 다른 부분을 수정했으면 Git이 자동으로 합친다. 실무에서 충돌은 생각보다 드물다.

> 이 주제에 대해 커뮤니티에서 의견이 나뉘는 부분이 있다:
> **merge vs rebase**. merge는 이력을 있는 그대로 보존하고, rebase는 이력을 깔끔하게 정리한다. 초보자는 merge부터 익히는 것을 권장한다. rebase는 이력을 변경하므로 위험할 수 있다.

### 코드 예제

브랜치를 만들고 병합하는 전체 과정이다:

```bash
# 1. 현재 브랜치 확인
git branch
# * main

# 2. 새 브랜치 생성 및 전환
git checkout -b feature/greeting
# Switched to a new branch 'feature/greeting'

# 3. 브랜치에서 작업
echo "Good morning!" > greeting.txt
git add greeting.txt
git commit -m "인사말 파일 추가"

# 4. main 브랜치로 돌아가기
git checkout main
# greeting.txt가 보이지 않는다 → main에는 영향 없음!

# 5. 브랜치 병합
git merge feature/greeting
# greeting.txt가 main에도 나타난다

# 6. 병합 완료 후 브랜치 삭제 (선택)
git branch -d feature/greeting
```

잘못된 예 - main에서 직접 실험:

```bash
# main 브랜치에서 바로 실험적 코드 작성
echo "experimental code" > experiment.txt
git add experiment.txt
git commit -m "실험 코드"
# → 실패하면 main 이력에 불필요한 커밋이 남음
# → 다른 팀원이 pull하면 실험 코드가 전파됨
```

이 세 가지 개념(버전관리, 3영역, 브랜치)만 이해하면 Git의 핵심을 파악한 것이다.
이후 원격 저장소(GitHub), 협업 워크플로우, rebase 등 심화 주제로 확장할 수 있다.

### Q&A

**Q: 브랜치 이름은 어떻게 짓나요? (← 주니어 개발자 배경)**
A: 팀마다 컨벤션이 다르지만, 널리 쓰이는 패턴은 `feature/기능명`, `fix/버그명`, `hotfix/긴급수정`이다. 예를 들어 `feature/login`, `fix/password-validation` 같은 형식이다. 슬래시(/)로 카테고리를 구분하면 정리가 편하다. 한글보다 영문을 권장한다. 더 깊이 알고 싶다면 'Git branch naming convention'을 검색해 보십시오.

**Q: 충돌(conflict)이 나면 어떻게 해결하나요?**
A: 충돌이 나면 Git이 해당 파일에 `<<<<<<<`, `=======`, `>>>>>>>`로 양쪽 변경 내용을 표시한다. 개발자가 직접 어떤 내용을 남길지 편집한 뒤, `git add`와 `git commit`으로 해결을 확정한다. VS Code 같은 에디터는 충돌을 시각적으로 보여주고 클릭 한 번으로 선택할 수 있게 해 준다. 더 깊이 알고 싶다면 'Git merge conflict resolution'을 검색해 보십시오.

**Q: `git checkout`과 `git switch`는 무엇이 다른가요?**
A: `git checkout`은 브랜치 전환과 파일 복원 두 가지 역할을 동시에 한다. Git 2.23부터 이를 분리하여 `git switch`(브랜치 전환)와 `git restore`(파일 복원)가 도입되었다. 기능은 동일하지만 의도가 더 명확하다. 두 가지 모두 알아두면 좋다. 더 깊이 알고 싶다면 'git switch vs checkout'을 검색해 보십시오.

---

## 퀴즈

**Q1. Git의 3가지 영역을 올바른 순서로 나열한 것은?**

A) Repository → Staging Area → Working Directory
B) Working Directory → Repository → Staging Area
C) Working Directory → Staging Area → Repository
D) Staging Area → Working Directory → Repository

<details>
<summary>💡 힌트</summary>
	파일을 수정하는 곳에서 시작하여, 최종 이력이 저장되는 곳으로 끝난다. 중간에 "선택"하는 단계가 있다.
</details>

<details>
<summary>✅ 정답</summary>
	**C) Working Directory → Staging Area → Repository**
	**설명:** 파일을 Working Directory에서 수정하고, `git add`로 Staging Area에 올린 뒤, `git commit`으로 Repository에 기록한다. 이 순서는 Git의 기본 워크플로우다.
</details>

---

**Q2. 다음 중 `git add` 명령어의 역할로 올바른 것은?**

A) 변경 사항을 Repository에 영구 저장한다
B) 변경 사항을 Staging Area에 올린다
C) 새 브랜치를 생성한다
D) 원격 저장소에서 코드를 가져온다

<details>
<summary>💡 힌트</summary>
	택배 비유를 떠올려 보십시오. `git add`는 물건을 "박스에 담는" 단계에 해당한다.
</details>

<details>
<summary>✅ 정답</summary>
	**B) 변경 사항을 Staging Area에 올린다**
	**설명:** `git add`는 Working Directory의 변경 사항을 Staging Area로 이동시킨다. 실제 이력에 기록하는 것은 `git commit`의 역할이다.
</details>

---

**Q3. `git branch feature/login` 명령어를 실행하면 무엇이 생성되는가? 간단히 설명하시오.**

<details>
<summary>💡 힌트</summary>
	Git에서 브랜치의 실체는 "파일 복사"가 아니다. 커밋 이력에서 특정 시점을 가리키는 것이다.
</details>

<details>
<summary>✅ 정답</summary>
	현재 커밋을 가리키는 **포인터(참조)** 가 하나 생성된다.
	**설명:** Git 브랜치는 커밋의 포인터다. `feature/login`이라는 이름의 포인터가 현재 HEAD가 가리키는 커밋과 같은 커밋을 가리키게 된다. 파일이 복사되는 것이 아니므로 생성 비용이 거의 없다.
</details>

---

**Q4. 다음 상황에서 `git commit`을 실행하면 어떻게 되는가?**

```bash
echo "hello" > a.txt
echo "world" > b.txt
git add a.txt
git commit -m "파일 추가"
```

<details>
<summary>💡 힌트</summary>
	`git add`로 Staging Area에 올린 파일만 커밋 대상이다. 두 파일 중 하나만 `add` 했다.
</details>

<details>
<summary>✅ 정답</summary>
	**a.txt만 커밋되고, b.txt는 커밋되지 않는다.**
	**설명:** `git add a.txt`만 실행했으므로 Staging Area에는 a.txt만 올라가 있다. b.txt는 Working Directory에 Untracked 상태로 남아 있다. 커밋은 Staging Area에 있는 변경 사항만 기록한다.
</details>

---

**Q5. 브랜치 `feature/signup`에서 작업 후 `main`에 병합하려 한다. 올바른 명령어 순서를 작성하시오.**

<details>
<summary>💡 힌트</summary>
	병합은 "받아들이는 쪽"에서 실행한다. 먼저 병합 대상 브랜치로 이동해야 한다.
</details>

<details>
<summary>✅ 정답</summary>
	```bash
	git checkout main
	git merge feature/signup
	```
	**설명:** 병합은 현재 브랜치에 다른 브랜치의 변경 사항을 합치는 것이다. 따라서 먼저 `main`으로 이동(`git checkout main`)한 뒤, `feature/signup`을 병합(`git merge feature/signup`)한다. 순서를 바꾸면 feature 브랜치에 main이 병합되어 의도와 다른 결과가 된다.
</details>

---

## 실습

<callout icon="📖" color="blue_bg">
	**학습 목표:** Git 저장소를 초기화하고, 파일을 커밋하며, 브랜치를 생성/병합하는 전체 과정을 직접 수행할 수 있다.
</callout>

### 실습 1: Git 기본 워크플로우 — init부터 commit까지

- **연관 학습 목표**: 학습 목표 1, 2
- **실습 목적**: Git의 3영역(Working Directory, Staging Area, Repository)을 직접 경험하고 기본 명령어를 체득한다
- **실습 유형**: CLI 명령어 실행
- **난이도**: 기초
- **예상 소요 시간**: 20분 (I DO 3분 / WE DO 7분 / YOU DO 10분)
- **선행 조건**: Git 설치 완료
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

### 🔍 I DO: Git 저장소 생성과 첫 커밋 {toggle="true" color="blue"}
	강사가 터미널에서 시연한다. 학생은 관찰하며 3영역의 흐름을 파악한다.
	```bash
	# 프로젝트 생성 및 초기화
	mkdir git-demo && cd git-demo
	git init

	# 파일 생성
	echo "# Git Demo Project" > README.md

	# 상태 확인 → Untracked (Working Directory)
	git status

	# 스테이징 → Staging Area
	git add README.md
	git status

	# 커밋 → Repository
	git commit -m "init: 프로젝트 초기화"

	# 이력 확인
	git log --oneline
	```
	<callout icon="💡" color="gray_bg">
		**관찰 포인트**: `git status`의 출력이 각 단계에서 어떻게 변하는지 주목하십시오. 빨간색(Untracked/Modified) → 녹색(Staged) → clean 상태로 변한다.
	</callout>

### 🤝 WE DO: 파일 수정과 커밋 사이클 반복 {toggle="true" color="green"}
	강사와 함께 따라 하며, add → commit 사이클을 반복 연습한다.
	1. README.md에 내용을 추가한다
	```bash
	echo "Git 기초를 배우는 프로젝트입니다." >> README.md
	```
	2. 새 파일을 생성한다
	```bash
	echo "print('hello git')" > app.py
	```
	3. 상태를 확인한다
	```bash
	git status
	# README.md → modified (빨간색)
	# app.py → untracked (빨간색)
	```
	4. 파일별로 스테이징하고 커밋한다
	```bash
	git add README.md
	git commit -m "docs: README 설명 추가"

	git add app.py
	git commit -m "feat: 메인 애플리케이션 추가"
	```
	5. 전체 이력을 확인한다
	```bash
	git log --oneline
	```
	- [ ] `git status`에서 빨간색/녹색 변화를 확인했는가?
	- [ ] `git log`에 커밋 3개가 보이는가?

### 🚀 YOU DO: 독립 커밋 연습 {toggle="true" color="purple"}
	<callout icon="📋" color="yellow_bg">
		**요구사항:**
		1. `config.txt` 파일을 생성하고 `debug=true` 내용을 작성한다
		2. `app.py`를 수정하여 `print('hello world')`로 변경한다
		3. **두 파일을 별도의 커밋으로 분리**하여 커밋한다 (한 번에 커밋하지 않을 것)
		4. `git log --oneline`으로 이력을 확인한다
	</callout>

<details>
<summary>💡 힌트</summary>
	`git add`에서 파일명을 하나만 지정하면 해당 파일만 스테이징된다. 스테이징 → 커밋을 두 번 반복하면 된다.
</details>

<details>
<summary>✅ 정답</summary>
	```bash
	# config.txt 생성
	echo "debug=true" > config.txt

	# app.py 수정
	echo "print('hello world')" > app.py

	# 첫 번째 커밋: config.txt
	git add config.txt
	git commit -m "feat: 설정 파일 추가"

	# 두 번째 커밋: app.py
	git add app.py
	git commit -m "fix: 출력 메시지 수정"

	# 이력 확인
	git log --oneline
	# 5개의 커밋이 시간순으로 표시됨
	```
</details>

---

### 실습 2: 브랜치 생성과 병합

- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: 브랜치를 생성하여 독립적으로 작업하고, main에 병합하는 워크플로우를 체득한다
- **실습 유형**: CLI 명령어 실행
- **난이도**: 기초 ~ 중급
- **예상 소요 시간**: 22분 (I DO 4분 / WE DO 8분 / YOU DO 10분)
- **선행 조건**: 실습 1 완료 (git-demo 프로젝트가 존재해야 함)
- **실행 환경**: 로컬 (Linux 기본, macOS 호환)

### 🔍 I DO: 브랜치 생성과 병합 시연 {toggle="true" color="blue"}
	강사가 브랜치의 전체 라이프사이클을 시연한다.
	```bash
	# 현재 브랜치 확인
	git branch
	# * main

	# 새 브랜치 생성 + 전환
	git checkout -b feature/about

	# 브랜치에서 작업
	echo "이 프로젝트는 Git 학습용입니다." > about.txt
	git add about.txt
	git commit -m "docs: about 페이지 추가"

	# main으로 돌아가기
	git checkout main
	ls  # about.txt가 없다!

	# 병합
	git merge feature/about
	ls  # about.txt가 나타난다!

	# 브랜치 삭제
	git branch -d feature/about
	```
	<callout icon="💡" color="gray_bg">
		**핵심 포인트**: `git checkout main`으로 돌아왔을 때 about.txt가 보이지 않는다. 브랜치가 **진짜 독립된 공간**임을 체감할 수 있다.
	</callout>

### 🤝 WE DO: 브랜치 워크플로우 함께 실습 {toggle="true" color="green"}
	강사와 함께 새로운 기능 브랜치를 만들어 작업한다.
	1. 기능 브랜치를 생성한다
	```bash
	git checkout -b feature/greeting
	```
	2. 새 파일을 만들고 커밋한다
	```bash
	echo "안녕하세요!" > greeting.txt
	git add greeting.txt
	git commit -m "feat: 인사말 기능 추가"
	```
	3. 파일을 수정하고 추가 커밋한다
	```bash
	echo "반갑습니다!" >> greeting.txt
	git add greeting.txt
	git commit -m "feat: 인사말 확장"
	```
	4. main으로 돌아가서 병합한다
	```bash
	git checkout main
	git merge feature/greeting
	```
	5. 이력을 확인한다
	```bash
	git log --oneline --graph
	```
	- [ ] 브랜치 전환 시 파일이 사라지고 나타나는 것을 확인했는가?
	- [ ] `git log --graph`에서 브랜치 병합 흐름이 보이는가?

### 🚀 YOU DO: 독립 브랜치 워크플로우 {toggle="true" color="purple"}
	<callout icon="📋" color="yellow_bg">
		**요구사항:**
		1. `feature/calculator` 브랜치를 생성한다
		2. `calc.py` 파일을 만들고 `print(1 + 1)` 코드를 작성한다
		3. 커밋 메시지는 `feat: 계산기 기능 추가`로 한다
		4. `calc.py`를 수정하여 `print(2 * 3)`으로 변경하고 커밋한다
		5. `main` 브랜치로 돌아가서 `feature/calculator`를 병합한다
		6. `git log --oneline --graph`로 전체 이력을 확인한다
		7. (보너스) 병합 완료된 `feature/calculator` 브랜치를 삭제한다
	</callout>

<details>
<summary>💡 힌트</summary>
	브랜치 생성+전환은 `git checkout -b`로 한 번에 할 수 있다. 병합은 "받아들이는 쪽(main)"에서 `git merge`를 실행한다는 것을 기억하십시오.
</details>

<details>
<summary>✅ 정답</summary>
	```bash
	# 1. 브랜치 생성 및 전환
	git checkout -b feature/calculator

	# 2-3. 파일 생성 및 커밋
	echo "print(1 + 1)" > calc.py
	git add calc.py
	git commit -m "feat: 계산기 기능 추가"

	# 4. 수정 및 커밋
	echo "print(2 * 3)" > calc.py
	git add calc.py
	git commit -m "fix: 계산 로직 변경"

	# 5. main으로 이동 후 병합
	git checkout main
	git merge feature/calculator

	# 6. 이력 확인
	git log --oneline --graph

	# 7. (보너스) 브랜치 삭제
	git branch -d feature/calculator
	```
</details>

---

## 핵심 정리

- **버전관리**는 파일의 변경 이력을 체계적으로 기록하는 시스템이다. Git은 분산형 VCS로, 로컬에서 독립적으로 동작한다.
- **Git의 3영역**: Working Directory(작업) → Staging Area(선택) → Repository(확정). `git add`와 `git commit`이 각 영역 사이의 이동을 담당한다.
- **기본 명령어**: `git init`(초기화), `git add`(스테이징), `git commit`(커밋), `git status`(상태 확인), `git log`(이력 조회)
- **브랜치**는 커밋을 가리키는 포인터다. 생성 비용이 거의 없으므로, 기능마다 브랜치를 만드는 것이 좋은 습관이다.
- **병합(merge)** 은 독립된 브랜치의 작업을 합치는 것이다. 같은 파일의 같은 줄을 수정한 경우에만 충돌이 발생한다.
- 다음 단계: 원격 저장소(GitHub), `git push`/`git pull`, 협업 워크플로우(Pull Request)
