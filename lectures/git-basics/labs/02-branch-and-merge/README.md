# 브랜치 생성과 병합

## 실습 목적

브랜치를 생성하여 독립적으로 작업하고, main에 병합하는 워크플로우를 체득한다. 브랜치 전환 시 파일이 사라지고 나타나는 것을 직접 체험하여, 브랜치가 독립된 작업 공간임을 이해한다.

## 사전 준비

- Git 설치 완료 (`git --version`으로 확인)
- **실습 1(Git 기본 워크플로우) 완료**: `git init`, `git add`, `git commit`을 사용할 수 있어야 함
- 터미널(CLI) 기본 조작 가능

---

## I DO: 시연 관찰 (약 4분)

강사가 시연하는 과정을 관찰하세요. 직접 코드를 작성하지 않아도 됩니다.

### 시연 내용

브랜치의 전체 라이프사이클(생성 → 작업 → 병합 → 삭제)을 보여준다. 특히 브랜치 전환 시 파일 시스템이 어떻게 바뀌는지가 핵심이다.

### 시연 코드

`src/i-do/` 디렉토리의 스크립트를 실행합니다:

```bash
bash src/i-do/demo.sh
```

### 관찰 포인트

- `git checkout main`으로 돌아왔을 때 **about.txt가 보이지 않는 것** -- 브랜치가 진짜 독립된 공간
- `git merge` 후 about.txt가 **다시 나타나는 것** -- 병합이 변경 사항을 합치는 과정
- `git branch -d`로 병합 완료된 브랜치를 정리하는 것 -- 브랜치 라이프사이클의 마무리
- `git log --oneline --graph`에서 브랜치 이력이 시각적으로 표현되는 것

---

## WE DO: 함께 실습 (약 8분)

강사와 함께 새로운 기능 브랜치를 만들어 작업합니다.

### 1단계: 기능 브랜치 생성

`feature/greeting` 브랜치를 만들고 전환합니다:

```bash
git checkout -b feature/greeting
```

> `git checkout -b`는 브랜치 **생성과 전환을 동시에** 수행합니다. `git branch feature/greeting` + `git checkout feature/greeting`과 같습니다.

### 2단계: 파일 생성 및 커밋

인사말 파일을 만들고 커밋합니다:

```bash
echo "안녕하세요!" > greeting.txt
git add greeting.txt
git commit -m "feat: 인사말 기능 추가"
```

### 3단계: 파일 수정 및 추가 커밋

인사말을 확장합니다:

```bash
echo "반갑습니다!" >> greeting.txt
git add greeting.txt
git commit -m "feat: 인사말 확장"
```

### 4단계: main으로 돌아가서 병합

```bash
# main으로 돌아가기
git checkout main

# 이 시점에서 ls를 해보세요. greeting.txt가 없습니다!
ls

# 병합
git merge feature/greeting

# 다시 ls를 해보세요. greeting.txt가 나타납니다!
ls
```

### 5단계: 이력 확인

```bash
git log --oneline --graph
```

### 확인 체크리스트

- [ ] 브랜치 전환 시 파일이 사라지고 나타나는 것을 확인했는가?
- [ ] `git log --graph`에서 브랜치 병합 흐름이 보이는가?

참고 스크립트: `src/we-do/practice.sh`

---

## YOU DO: 독립 과제 (약 10분)

아래 과제를 스스로 해결하세요. 막히면 힌트를 참고하세요.

### 과제 설명

1. `feature/calculator` 브랜치를 생성한다
2. `calc.py` 파일을 만들고 `print(1 + 1)` 코드를 작성한다
3. 커밋 메시지는 `feat: 계산기 기능 추가`로 한다
4. `calc.py`를 수정하여 `print(2 * 3)`으로 변경하고 커밋한다
5. `main` 브랜치로 돌아가서 `feature/calculator`를 병합한다
6. `git log --oneline --graph`로 전체 이력을 확인한다
7. (보너스) 병합 완료된 `feature/calculator` 브랜치를 삭제한다

### 시작 방법

`src/you-do/challenge.sh` 파일의 TODO 주석을 채워서 완성하세요:

```bash
vi src/you-do/challenge.sh
bash src/you-do/challenge.sh
```

### 힌트

<details>
<summary>힌트 1</summary>

브랜치 생성과 전환을 동시에 하려면 `git checkout -b 브랜치이름`을 사용합니다.

</details>

<details>
<summary>힌트 2</summary>

병합은 **"받아들이는 쪽"** 에서 실행해야 합니다. `feature/calculator`를 `main`에 합치려면:

```bash
git checkout main              # 먼저 main으로 이동
git merge feature/calculator   # 그다음 병합
```

순서를 바꾸면 feature 브랜치에 main이 병합되어 의도와 다른 결과가 됩니다.

</details>

<details>
<summary>힌트 3 (보너스)</summary>

병합 완료된 브랜치를 삭제하려면 소문자 `-d` 를 사용합니다:

```bash
git branch -d feature/calculator
```

대문자 `-D`는 병합되지 않은 브랜치도 강제 삭제하므로, 일반적으로 `-d`를 사용하는 것이 안전합니다.

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

# 수동 검증
# 1. main 브랜치에 calc.py가 존재하는지 확인
ls calc.py

# 2. calc.py 내용이 올바른지 확인
cat calc.py
# 출력: print(2 * 3)

# 3. git log에서 병합 이력 확인
git log --oneline --graph
```

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| `error: pathspec 'main' did not match` | main 브랜치가 아닌 master 브랜치 사용 | `git branch`로 기본 브랜치 이름 확인 후 해당 이름 사용 |
| `Already on 'feature/...'` | 이미 해당 브랜치에 있음 | `git branch`로 현재 브랜치 확인 |
| `merge: feature/calculator - not something we can merge` | 브랜치 이름 오타 | `git branch`로 정확한 브랜치 이름 확인 |
| `CONFLICT (content)` | 같은 파일의 같은 줄을 양쪽에서 수정 | 이 실습에서는 충돌이 발생하지 않아야 함. 처음부터 다시 시도 |
| `error: The branch 'feature/...' is not fully merged` | 병합하지 않고 브랜치 삭제 시도 | 먼저 `git merge`로 병합한 뒤 삭제하세요 |
| `fatal: A branch named 'feature/calculator' already exists` | 이전 실행에서 브랜치가 남아 있음 | `git branch -d feature/calculator`로 삭제 후 다시 생성 |
