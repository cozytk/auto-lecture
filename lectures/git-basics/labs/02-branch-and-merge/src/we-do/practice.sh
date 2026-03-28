#!/usr/bin/env bash
# 브랜치 워크플로우 함께 실습 스캐폴드
# 강사와 함께 TODO를 채워가며 브랜치 생성/병합을 연습한다.

set -euo pipefail

WORK_DIR="/tmp/git-branch-wedo-$$"

cleanup() {
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

echo "=== WE DO: 브랜치 워크플로우 함께 실습 ==="
echo ""

# 프로젝트 준비
mkdir -p "$WORK_DIR" && cd "$WORK_DIR"
git init
echo "# Git Demo Project" > README.md
git add README.md
git commit -m "init: 프로젝트 초기화"
echo "Git 기초를 배우는 프로젝트입니다." >> README.md
git add README.md
git commit -m "docs: README 설명 추가"
echo "print('hello git')" > app.py
git add app.py
git commit -m "feat: 메인 애플리케이션 추가"
echo "  [준비 완료] 기본 프로젝트가 준비되었습니다."
echo ""

# TODO: 1단계 - 기능 브랜치 생성
echo ">>> 1단계: feature/greeting 브랜치를 생성하세요"
# TODO: git checkout -b로 feature/greeting 브랜치를 생성하세요
git checkout -b feature/greeting
echo ""

# TODO: 2단계 - 새 파일 생성 및 커밋
echo ">>> 2단계: greeting.txt 파일을 만들고 커밋하세요"
# TODO: echo로 greeting.txt를 생성하세요 (내용: 안녕하세요!)
echo "안녕하세요!" > greeting.txt
# TODO: git add와 git commit으로 커밋하세요
git add greeting.txt
git commit -m "feat: 인사말 기능 추가"
echo ""

# TODO: 3단계 - 파일 수정 및 추가 커밋
echo ">>> 3단계: greeting.txt를 수정하고 추가 커밋하세요"
# TODO: echo >>로 greeting.txt에 내용을 추가하세요 (내용: 반갑습니다!)
echo "반갑습니다!" >> greeting.txt
# TODO: git add와 git commit으로 커밋하세요
git add greeting.txt
git commit -m "feat: 인사말 확장"
echo ""

# TODO: 4단계 - main으로 돌아가서 병합
echo ">>> 4단계: main 브랜치로 돌아가서 병합하세요"
# TODO: git checkout으로 main 브랜치로 전환하세요
git checkout main
echo "  main 브랜치의 파일 목록:"
ls
echo "  → greeting.txt가 보이지 않습니다 (아직 병합 전)"
echo ""

# TODO: feature/greeting 브랜치를 병합하세요
git merge feature/greeting
echo "  병합 후 파일 목록:"
ls
echo ""

# TODO: 5단계 - 이력 확인
echo ">>> 5단계: 이력을 확인하세요"
# TODO: git log --oneline --graph로 이력을 확인하세요
git log --oneline --graph
echo ""

echo "=== 체크리스트 ==="
echo "  [ ] 브랜치 전환 시 파일이 사라지고 나타나는 것을 확인했는가?"
echo "  [ ] git log --graph에서 브랜치 병합 흐름이 보이는가?"
