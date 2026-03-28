#!/usr/bin/env bash
# Git 기본 워크플로우 시연 스크립트
# 강사가 실행하며 학생에게 3영역 흐름을 보여준다.

set -euo pipefail

DEMO_DIR="/tmp/git-demo-ido-$$"

cleanup() {
    rm -rf "$DEMO_DIR"
}
trap cleanup EXIT

echo "=== Git 기본 워크플로우 시연 ==="
echo ""

# 1. 프로젝트 생성 및 Git 초기화
echo ">>> 1단계: 프로젝트 생성 및 Git 초기화"
mkdir -p "$DEMO_DIR" && cd "$DEMO_DIR"
git init
echo ""

# 2. 파일 생성 후 상태 확인 (Working Directory)
echo ">>> 2단계: 파일 생성 후 상태 확인"
echo "# Git Demo Project" > README.md
git status
echo ""
echo "  → README.md가 Untracked 상태 (Working Directory에만 존재)"
echo ""

# 3. Staging Area에 추가
echo ">>> 3단계: git add로 Staging Area에 추가"
git add README.md
git status
echo ""
echo "  → README.md가 녹색으로 변경 (Staging Area에 올라감)"
echo ""

# 4. 커밋 (Repository에 기록)
echo ">>> 4단계: git commit으로 Repository에 기록"
git commit -m "init: 프로젝트 초기화"
echo ""

# 5. 파일 수정 → add → commit 사이클
echo ">>> 5단계: 수정 → add → commit 사이클"
echo "Git 기초를 배우는 프로젝트입니다." >> README.md
echo "print('hello git')" > app.py

echo "  현재 상태 확인:"
git status
echo ""

git add README.md
git commit -m "docs: README 설명 추가"

git add app.py
git commit -m "feat: 메인 애플리케이션 추가"

# 6. 전체 이력 확인
echo ""
echo ">>> 6단계: 전체 이력 확인"
git log --oneline
echo ""
echo "=== 시연 완료 ==="
echo "Working Directory → (git add) → Staging Area → (git commit) → Repository"
