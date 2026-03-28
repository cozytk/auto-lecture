---
transition: slide-left
---

# Git 기본 명령어

```bash {all|1-3|5-8|10-12}
# 1. 저장소 초기화
mkdir my-project
cd my-project
git init

# 2. 파일 추가 및 스테이징
echo '# My Project' > README.md
git add README.md
git status

# 3. 커밋
git commit -m '프로젝트 초기화'
git log --oneline
```

<v-clicks>

- `git init`: 현재 디렉토리를 Git 저장소로
- `git add`: Working → Staging
- `git commit`: Staging → Repository

</v-clicks>

<!--
[스크립트]

자, 이제 Git의 가장 기본이 되는 세 가지 명령어를 직접 터미널에서 실행해보겠습니다. init, add, commit — 이 세 단계만 기억하시면 됩니다.

[코드 블록 전체가 보일 때]
화면에 보이는 코드가 전체 흐름인데요, 크게 세 단계로 나뉩니다. 하나씩 따라가 볼게요.

[1-3번 줄: 저장소 초기화]
먼저 첫 번째 단계, 저장소 초기화입니다.
- `mkdir my-project` — 프로젝트 폴더를 하나 만들어줍니다. 아직은 그냥 평범한 빈 폴더예요.
- `cd my-project` — 해당 폴더로 이동하고요.
- `git init` — 이게 핵심입니다. 이 명령어를 치는 순간 이 폴더 안에 `.git`이라는 숨겨진 디렉토리가 생깁니다. 이 `.git` 폴더가 버전 관리의 모든 정보를 담고 있는 거예요. 즉, `git init`을 해야 비로소 "Git 저장소"가 되는 겁니다.

[5-8번 줄: 파일 추가 및 스테이징]
두 번째 단계, 파일을 만들고 스테이징하는 부분입니다.
- `echo '# My Project' > README.md` — README 파일을 하나 만들어줍니다. 지금 이 파일은 Working Directory에만 존재하는 상태예요. Git은 아직 이 파일의 존재를 모릅니다.
- `git add README.md` — 이 명령어로 README.md를 Staging Area에 올려줍니다. "이 파일을 다음 커밋에 포함시킬게요"라고 Git한테 알려주는 거죠. 앞에서 배운 세 영역 기억나시죠? Working Directory에서 Staging Area로 넘기는 단계가 바로 이겁니다.
- `git status` — 현재 상태를 확인하는 명령어입니다. 실행하면 README.md가 초록색으로 "Changes to be committed"라고 뜰 거예요. 스테이징이 잘 됐다는 뜻이죠. 이 명령어는 앞으로 정말 자주 쓰게 될 겁니다. 뭔가 헷갈릴 때 `git status` 치면 현재 상황을 알려주니까요.

[10-12번 줄: 커밋]
마지막 세 번째 단계, 커밋입니다.
- `git commit -m '프로젝트 초기화'` — Staging Area에 올라가 있는 파일들을 하나의 스냅샷으로 찍어서 Repository에 저장합니다. `-m` 뒤에 오는 건 커밋 메시지인데요, 이 변경이 뭔지 설명하는 메모라고 생각하시면 됩니다. 나중에 히스토리를 볼 때 이 메시지가 보이니까 의미 있게 적어주는 게 좋습니다.
- `git log --oneline` — 커밋 이력을 한 줄씩 깔끔하게 보여주는 명령어입니다. 방금 만든 '프로젝트 초기화' 커밋이 보일 거예요. 앞에 붙는 알파벳+숫자 조합은 커밋 해시라고 하는데, 각 커밋의 고유 ID입니다.

[v-clicks 불릿 포인트]
정리하면 이렇습니다.
- `git init`은 일반 폴더를 Git 저장소로 만들어주는 거고요,
- `git add`는 Working Directory에서 Staging Area로 파일을 올리는 거고,
- `git commit`은 Staging Area의 내용을 Repository에 확정 저장하는 겁니다.

이 init, add, commit 세 단계가 Git의 가장 기본적인 워크플로입니다. 이걸 손에 익을 때까지 반복하시면 나머지 명령어들은 다 여기서 확장되는 거예요.
-->
