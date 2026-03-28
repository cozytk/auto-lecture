# Lab 04: 바이브 코딩 — 처음부터 앱 만들기

> **캡스톤 실습** | 60분 | 팀 과제 (2~3인)

코드를 한 줄도 직접 작성하지 않고, 프롬프트만으로 동작하는 앱을 완성한다.
오늘 배운 에이전틱 코딩의 모든 기법을 총동원하라.

---

## 타임라인

| 시간 | 활동 |
|------|------|
| 0:00 ~ 0:05 | 전체 설명 및 규칙 안내 |
| 0:05 ~ 0:10 | 팀 구성 + 시나리오 선택 |
| 0:10 ~ 0:50 | **바이브 코딩** (핵심 40분) |
| 0:50 ~ 1:00 | 발표 준비 및 팀별 발표 |

---

## 바이브 코딩 규칙

### 반드시 지켜야 할 것

1. **코드를 직접 타이핑하지 않는다** — 모든 코드는 에이전트가 작성
2. **AGENTS.md는 직접 작성해도 된다** — 에이전트에게 주는 지시문이므로 예외
3. **에러 메시지는 복사해서 에이전트에게 전달** — 직접 수정하지 않는다
4. **Claude Code(또는 동급 AI 코딩 에이전트)를 사용** — 일반 ChatGPT 제외

### 권장 사항

- 팀원 한 명이 드라이버(타이핑), 나머지는 프롬프트 전략가로 역할 분담
- 프롬프트를 보내기 전에 팀원과 먼저 합의
- `artifacts/prompt-strategy.md`를 참고해 체계적으로 진행
- 막히면 `artifacts/example-pomodoro/prompts-used.md` 참고

---

## 시나리오 선택

6개 시나리오 중 하나를 선택한다. 팀별로 중복 불가.

| # | 시나리오 | 난이도 | 파일 |
|---|----------|--------|------|
| 1 | CLI 포모도로 타이머 | ★☆☆ | `scenarios/scenario-01-pomodoro.md` |
| 2 | 터미널 습관 트래커 | ★★☆ | `scenarios/scenario-02-habit-tracker.md` |
| 3 | Markdown → HTML 변환기 | ★★☆ | `scenarios/scenario-03-md-converter.md` |
| 4 | 팀 회고 보드 | ★★★ | `scenarios/scenario-04-retro-board.md` |
| 5 | 코드 스니펫 매니저 | ★★☆ | `scenarios/scenario-05-snippet-manager.md` |
| 6 | 자유 주제 | 자유 | `scenarios/scenario-06-free-topic.md` |

> **초보자 팀 추천**: 시나리오 1 (포모도로) — 완성 예시 포함

---

## 시작하기

### 1단계: AGENTS.md 작성 (5분)
```
# 새 프로젝트 폴더 생성 후 AGENTS.md 작성
mkdir my-vibe-project
cd my-vibe-project
# AGENTS.md 직접 작성 (템플릿: artifacts/agents-md-template.md 참고)
```

### 2단계: Claude Code 열기
```
claude
```

### 3단계: 첫 번째 프롬프트
`artifacts/prompt-strategy.md`의 Step 1(프로젝트 구조)부터 시작한다.

---

## 발표 포맷 (팀당 3분)

1. **시나리오 소개** — 어떤 앱을 만들었나
2. **AGENTS.md 설명** — 에이전트에게 어떤 규칙을 줬나
3. **동작 시연** — 실제 앱 실행
4. **핵심 프롬프트 공유** — 가장 효과적이었던 프롬프트 1~2개
5. **배운 점** — 잘 된 것, 안 된 것

---

## 평가 기준

자세한 루브릭: `artifacts/rubric.md`

| 항목 | 배점 |
|------|------|
| 동작 여부 | 30점 |
| 코드 품질 | 20점 |
| 프롬프트 전략 | 20점 |
| 발표/시연 | 15점 |
| 도전 정신 | 15점 |

**합계: 100점**

---

## 참고 자료

- `artifacts/prompt-strategy.md` — 바이브 코딩 전략 가이드
- `artifacts/agents-md-template.md` — AGENTS.md 템플릿
- `artifacts/rubric.md` — 평가 루브릭
- `artifacts/example-pomodoro/` — 완성 예시 (시나리오 1)
