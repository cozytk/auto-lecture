#!/usr/bin/env bash
# Git 기본 워크플로우 함께 실습 스캐폴드
# 강사와 함께 TODO를 채워가며 실습한다.

set -euo pipefail

WORK_DIR="/tmp/git-wedo-$$"

cleanup() {
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

echo "=== WE DO: 파일 수정과 커밋 사이클 반복 ==="
echo ""

# 프로젝트 준비 (I DO에서 만든 상태를 재현)
mkdir -p "$WORK_DIR" && cd "$WORK_DIR"
git init
echo "# Git Demo Project" > README.md
git add README.md
git commit -m "init: 프로젝트 초기화"
echo "  [준비 완료] git-demo 프로젝트가 초기화되었습니다."
echo ""

# TODO: 1단계 - README.md에 내용 추가
echo ">>> 1단계: README.md에 내용을 추가하세요"
echo "Git 기초를 배우는 프로젝트입니다." >> README.md
echo "  README.md에 내용을 추가했습니다."
echo ""

# TODO: 2단계 - 새 파일 생성
echo ">>> 2단계: app.py 파일을 생성하세요"
# TODO: echo 명령어로 app.py를 생성하세요. 내용은 print('hello git')
echo "print('hello git')" > app.py
echo "  app.py를 생성했습니다."
echo ""

# TODO: 3단계 - 상태 확인
echo ">>> 3단계: git status로 상태를 확인하세요"
# TODO: git status 명령어를 실행하세요
git status
echo ""
echo "  → 빨간색: Working Directory에서 변경된 파일"
echo "  → 녹색: Staging Area에 올라간 파일"
echo ""

# TODO: 4단계 - 파일별로 스테이징하고 커밋
echo ">>> 4단계: README.md를 스테이징하고 커밋하세요"
# TODO: git add와 git commit으로 README.md를 커밋하세요
git add README.md
git commit -m "docs: README 설명 추가"
echo ""

echo ">>> 5단계: app.py를 스테이징하고 커밋하세요"
# TODO: git add와 git commit으로 app.py를 커밋하세요
git add app.py
git commit -m "feat: 메인 애플리케이션 추가"
echo ""

# TODO: 6단계 - 전체 이력 확인
echo ">>> 6단계: git log로 전체 이력을 확인하세요"
# TODO: git log --oneline 명령어를 실행하세요
git log --oneline
echo ""

echo "=== 체크리스트 ==="
echo "  [ ] git status에서 빨간색/녹색 변화를 확인했는가?"
echo "  [ ] git log에 커밋 3개가 보이는가?"
