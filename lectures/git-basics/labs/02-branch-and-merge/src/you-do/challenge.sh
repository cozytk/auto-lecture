#!/usr/bin/env bash
# 브랜치 독립 과제
# TODO 주석을 채워서 과제를 완성하세요.

set -euo pipefail

WORK_DIR="/tmp/git-branch-youdo-$$"

cleanup() {
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

echo "=== YOU DO: 독립 브랜치 워크플로우 ==="
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

# ============================================================
# 과제: 아래 TODO를 채워서 브랜치 워크플로우를 완성하세요
# ============================================================

# TODO 1: feature/calculator 브랜치를 생성하고 전환하세요


# TODO 2: calc.py 파일을 만드세요 (내용: print(1 + 1))


# TODO 3: calc.py를 스테이징하고 커밋하세요 (메시지: feat: 계산기 기능 추가)


# TODO 4: calc.py를 수정하세요 (내용: print(2 * 3))


# TODO 5: 수정된 calc.py를 스테이징하고 커밋하세요 (메시지: fix: 계산 로직 변경)


# TODO 6: main 브랜치로 돌아가세요


# TODO 7: feature/calculator 브랜치를 병합하세요


# TODO 8: git log --oneline --graph로 전체 이력을 확인하세요


# (보너스) TODO 9: 병합 완료된 feature/calculator 브랜치를 삭제하세요


echo ""
echo "=== 과제 완료! ==="
echo "git log에서 브랜치 병합 이력이 보이면 성공입니다."
