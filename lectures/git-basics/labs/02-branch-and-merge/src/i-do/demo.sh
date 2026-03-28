#!/usr/bin/env bash
# 브랜치 생성과 병합 시연 스크립트
# 강사가 실행하며 브랜치의 전체 라이프사이클을 보여준다.

set -euo pipefail

DEMO_DIR="/tmp/git-branch-ido-$$"

cleanup() {
    rm -rf "$DEMO_DIR"
}
trap cleanup EXIT

echo "=== 브랜치 생성과 병합 시연 ==="
echo ""

# 프로젝트 준비 (실습 1 완료 상태 재현)
mkdir -p "$DEMO_DIR" && cd "$DEMO_DIR"
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
echo "  [준비 완료] 실습 1 상태가 재현되었습니다."
echo ""

# 1. 현재 브랜치 확인
echo ">>> 1단계: 현재 브랜치 확인"
git branch
echo ""

# 2. 새 브랜치 생성 + 전환
echo ">>> 2단계: feature/about 브랜치 생성 및 전환"
git checkout -b feature/about
git branch
echo ""

# 3. 브랜치에서 작업
echo ">>> 3단계: 브랜치에서 파일 생성 및 커밋"
echo "이 프로젝트는 Git 학습용입니다." > about.txt
git add about.txt
git commit -m "docs: about 페이지 추가"
echo ""

# 4. main으로 돌아가서 파일 확인
echo ">>> 4단계: main 브랜치로 돌아가기"
git checkout main
echo "  main 브랜치의 파일 목록:"
ls
echo ""
echo "  → about.txt가 보이지 않는다! 브랜치가 독립된 공간임을 확인."
echo ""

# 5. 병합
echo ">>> 5단계: feature/about 브랜치 병합"
git merge feature/about
echo ""
echo "  병합 후 파일 목록:"
ls
echo ""
echo "  → about.txt가 나타났다! 병합 성공."
echo ""

# 6. 브랜치 삭제
echo ">>> 6단계: 병합 완료된 브랜치 삭제"
git branch -d feature/about
echo ""

# 7. 전체 이력 확인
echo ">>> 7단계: 전체 이력 확인"
git log --oneline --graph
echo ""
echo "=== 시연 완료 ==="
echo "브랜치 라이프사이클: 생성 → 작업 → 병합 → 삭제"
