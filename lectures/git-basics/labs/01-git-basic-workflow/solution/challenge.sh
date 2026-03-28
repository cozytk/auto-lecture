#!/usr/bin/env bash
# Git 기본 워크플로우 독립 과제 - 정답
# 두 파일을 별도의 커밋으로 분리하는 것이 핵심이다.

set -euo pipefail

WORK_DIR="/tmp/git-youdo-$$"

cleanup() {
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

echo "=== YOU DO: 독립 커밋 연습 (정답) ==="
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
echo "  [준비 완료] WE DO까지의 상태가 재현되었습니다."
echo ""

# config.txt 생성
echo "debug=true" > config.txt

# app.py 수정
echo "print('hello world')" > app.py

# 핵심: 파일별로 분리하여 커밋한다.
# git add .으로 전체를 올리면 하나의 커밋에 섞이므로, 파일명을 지정한다.
git add config.txt
git commit -m "feat: 설정 파일 추가"

git add app.py
git commit -m "fix: 출력 메시지 수정"

# 이력 확인
echo ">>> 전체 커밋 이력:"
git log --oneline
echo ""

COMMIT_COUNT=$(git log --oneline | wc -l | tr -d ' ')
if [ "$COMMIT_COUNT" -eq 5 ]; then
    echo "=== 성공! 5개의 커밋이 확인되었습니다. ==="
else
    echo "=== 실패: 커밋 수가 $COMMIT_COUNT개입니다. 5개여야 합니다. ==="
    exit 1
fi
