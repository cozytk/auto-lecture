#!/usr/bin/env bash
# Git 기본 워크플로우 독립 과제
# TODO 주석을 채워서 과제를 완성하세요.

set -euo pipefail

WORK_DIR="/tmp/git-youdo-$$"

cleanup() {
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT

echo "=== YOU DO: 독립 커밋 연습 ==="
echo ""

# 프로젝트 준비 (WE DO까지의 상태를 재현)
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

# ============================================================
# 과제: 아래 TODO를 채워서 두 파일을 별도 커밋으로 분리하세요
# ============================================================

# TODO 1: config.txt 파일을 생성하세요 (내용: debug=true)


# TODO 2: app.py를 수정하세요 (내용: print('hello world'))


# TODO 3: config.txt만 스테이징하고 커밋하세요 (메시지: feat: 설정 파일 추가)


# TODO 4: app.py만 스테이징하고 커밋하세요 (메시지: fix: 출력 메시지 수정)


# TODO 5: git log --oneline으로 전체 이력을 확인하세요 (커밋 5개가 보여야 합니다)


echo ""
echo "=== 과제 완료! ==="
echo "git log에 5개의 커밋이 보이면 성공입니다."
