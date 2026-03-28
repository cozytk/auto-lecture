#!/usr/bin/env bash
# 브랜치 독립 과제 - 정답
# 브랜치를 만들어 작업하고 main에 병합하는 전체 흐름이 핵심이다.

set -euo pipefail

WORK_DIR="/tmp/git-branch-youdo-$$"

cleanup() {
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

echo "=== YOU DO: 독립 브랜치 워크플로우 (정답) ==="
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

# 브랜치 생성 및 전환
git checkout -b feature/calculator

# 파일 생성 및 첫 번째 커밋
echo "print(1 + 1)" > calc.py
git add calc.py
git commit -m "feat: 계산기 기능 추가"

# 파일 수정 및 두 번째 커밋
echo "print(2 * 3)" > calc.py
git add calc.py
git commit -m "fix: 계산 로직 변경"

# 병합은 "받아들이는 쪽"에서 실행해야 한다
git checkout main
git merge feature/calculator

echo ">>> 전체 커밋 이력:"
git log --oneline --graph
echo ""

# 병합 완료된 브랜치 삭제
git branch -d feature/calculator
echo ""

# 검증: calc.py가 main에 존재하고 내용이 올바른지 확인
if [ -f calc.py ] && grep -q "print(2 \* 3)" calc.py; then
    echo "=== 성공! 브랜치 병합이 올바르게 완료되었습니다. ==="
else
    echo "=== 실패: calc.py가 없거나 내용이 올바르지 않습니다. ==="
    exit 1
fi
