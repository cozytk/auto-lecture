# Day 2 실습 01: Agent Architecture Studio

## 실습 목적

Session 1의 핵심 내용을 실제 Agent 설계 문서로 변환하여,
Goal / Memory / Tool / Control Logic의 경계를 명확히 정의하고
Single-step vs Multi-step 구조를 근거 있게 선택할 수 있도록 만든다.

- **연관 세션**: Session 1 - Agent 4요소 구조 설계
- **실습 형식**: README 중심
- **난이도**: 기초 ~ 중급
- **예상 소요 시간**: 70분 (I DO 15분 / WE DO 20분 / YOU DO 35분)

## 산출물

- Agent 4요소 설계 캔버스 1개
- Sub-task 분해표 1개
- Single-step / Multi-step 판단표 1개
- Control Logic 초안 1개

## 사전 준비

- Day 1에서 선정한 최종 후보 1개를 가져온다.
- `lectures/ai-agent-dev/labs/day1/03-agent-spec-studio/README.md`에서 정리한 기획서 초안을 옆에 두고 시작한다.
- Session 1의 4요소, Planner-Executor, 분해 전략 표를 다시 확인한다.

---

## I DO: 시연 관찰 (약 15분)

강사가 "고객 지원 Agent" 사례를 가지고 아래 순서로 구조 설계를 시연한다.

1. Goal 문장을 단일 문장으로 압축한다.
2. Memory를 "대화 히스토리 / 작업 상태 / Tool 결과"로 구분한다.
3. Tool을 읽기/쓰기와 위험 수준 기준으로 분류한다.
4. Planner-Executor가 필요한지 판단한다.
5. Single-step과 Multi-step 중 하나를 선택하고 근거를 남긴다.

### 관찰 포인트

- Goal은 문제 설명이 아니라 종료 조건을 포함한 운영 문장이어야 한다.
- Memory를 너무 많이 잡으면 나중에 State가 비대해진다.
- Tool 목록보다 "언제 어떤 Tool을 호출해야 하는가"가 더 중요하다.
- Multi-step 선택은 "복잡해 보여서"가 아니라 반복/분기/재계획 필요성으로 판단한다.

---

## WE DO: 함께 실습 (약 20분)

팀 전체가 "여행 일정 추천 Agent"를 함께 분석한다.

### 단계 1: Agent 4요소 채우기

| 요소 | 정의 | 설계 메모 |
|------|------|----------|
| Goal | | |
| Memory | | |
| Tool | | |
| Control Logic | | |

### 단계 2: Sub-task 분해

| Sub-task | 설명 | 의존 대상 | 실행 전략 | 필요한 Tool |
|----------|------|----------|----------|------------|
| T1 | | | 순차 / 병렬 / 계층 | |
| T2 | | | 순차 / 병렬 / 계층 | |
| T3 | | | 순차 / 병렬 / 계층 | |

### 단계 3: 구조 판단

| 판단 질문 | Yes / No | 근거 |
|-----------|----------|------|
| Tool 호출이 1회로 끝나는가 | | |
| 이전 결과에 따라 다음 행동이 달라지는가 | | |
| 실패 시 대체 경로가 필요한가 | | |
| 상태 누적이 필요한가 | | |
| 최종 결론: Single-step / Multi-step | | |

---

## YOU DO: 독립 과제 (약 35분)

Day 1에서 선택한 본인 후보 1개를 기준으로 아래 문서를 완성한다.

### 과제 1: Agent 4요소 설계 캔버스

```markdown
## Agent 이름
-

## Goal
- 사용자가 무엇을 얻으면 이 Agent는 종료되는가?

## Memory
| 구분 | 저장 내용 | 왜 필요한가 |
|------|----------|-------------|
| 대화 히스토리 | | |
| 작업 상태 | | |
| Tool 결과 | | |

## Tool
| Tool | 읽기/쓰기 | 위험 수준 | 호출 조건 |
|------|----------|----------|----------|
| | | low / medium / high | |

## Control Logic
- 시작 조건:
- 반복 조건:
- 종료 조건:
- 실패 시 fallback:
```

### 과제 2: Sub-task 분해와 의존성 기록

```markdown
## Sub-task 분해표
| ID | 설명 | depends_on | 전략 | 완료 기준 |
|----|------|------------|------|----------|
| T1 | | | sequential / parallel / hierarchical | |
| T2 | | | sequential / parallel / hierarchical | |
| T3 | | | sequential / parallel / hierarchical | |

## 병렬 가능 지점
-

## Re-planning이 필요한 상황
-
```

### 과제 3: 구조 선택 메모

```markdown
## 구조 판단
- 선택: Single-step / Multi-step

### 선택 이유
1.
2.
3.

### 배제한 대안
- 배제한 구조:
- 배제 이유:

### LangGraph로 옮길 때 필요한 State 핵심 필드
-
-
-
```

---

## 검증 방법

- Goal / Memory / Tool / Control Logic 네 칸이 모두 채워졌는가
- Sub-task가 3~7개 수준으로 분해되었는가
- 병렬 가능 지점과 의존성이 함께 설명되었는가
- Single-step / Multi-step 선택 이유가 반복, 분기, fallback 기준으로 설명되는가

## 예시 산출물

- 모범 답안 예시는 `artifacts/example-output.md`를 참고한다.

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| Goal이 너무 추상적임 | 종료 조건이 없음 | "언제 끝났다고 볼 것인가"를 한 줄로 먼저 쓴다 |
| Tool이 너무 많음 | 실제 호출 조건을 안 적음 | 각 Tool 옆에 "언제 호출하는가"를 추가한다 |
| 모든 작업이 Multi-step처럼 보임 | 실패/분기 기준이 없음 | 1회 Tool 호출로 끝나는지 먼저 체크한다 |

## 다음 실습과 연결

이 실습에서 만든 State 핵심 필드와 Control Logic 메모는 `../05-langgraph-control-flow/README.md`에서 그대로 사용한다.
