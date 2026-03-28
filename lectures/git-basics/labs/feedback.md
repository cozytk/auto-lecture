# 실습 피드백: git-basics

생성일: 2026-03-16
에이전트: lab-manager

## 실습 실행 요약

| 실습 이름 | 상태 | 비고 |
|----------|------|------|
| 01-git-basic-workflow | 통과 | I DO, WE DO, Solution 모두 정상 동작 |
| 02-branch-and-merge | 통과 | I DO, WE DO, Solution 모두 정상 동작 |

## 가이드 보강 필요 항목

### Git 초기 설정 안내

- **문제**: 가이드에서 `git config --global user.name`과 `git config --global user.email` 설정 안내가 없다. 설정하지 않으면 첫 `git commit`에서 "Please tell me who you are" 오류가 발생한다.
- **제안**: "2. Git의 3가지 영역과 기본 명령어" 섹션의 코드 예제 앞에 Git 초기 설정 단계를 추가한다. 실습 README에는 트러블슈팅에 포함해 두었다.

### main vs master 브랜치 이름

- **문제**: 가이드에서 기본 브랜치를 `main`으로 가정하지만, Git 버전에 따라 `master`가 기본인 경우가 있다. Git 2.28 이전 버전에서는 `master`가 기본이다.
- **제안**: 가이드 사전 요구사항에 `git config --global init.defaultBranch main` 설정을 권장하거나, "Git 버전에 따라 기본 브랜치 이름이 다를 수 있다"는 안내를 추가한다.

## 추가 권장 사항

- 실습 시간이 총 42분(실습1: 20분 + 실습2: 22분)으로 1시간 수업의 70%를 적절히 충족한다.
- 두 실습 모두 `/tmp` 디렉토리에 임시 작업 공간을 생성하고 `trap`으로 자동 정리하므로, 학생 환경을 오염시키지 않는다.
- YOU DO 과제의 난이도가 WE DO에서 한 단계 자연스럽게 확장되어 있어, 학생이 무리 없이 독립 과제에 진입할 수 있다.
