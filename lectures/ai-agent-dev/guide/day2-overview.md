# Day 2 운영 가이드

Day 2는 **이론 3 : 실습 7** 비율로 운영한다.
기존 세션 가이드는 그대로 Source of Truth로 사용한다.
이 문서는 Day 2 전체 진행 순서와 실습 연결만 정리한다.

## Day 2 운영 원칙

- Day 2 총 수업 시간: 480분
- 권장 이론 시간: 약 145분
- 권장 실습 시간: 약 335분
- 세션 가이드는 개념 설명용 기준 문서다.
- 실습은 Day 2 전용 Lab Pack에서 이어서 운영한다.
- 슬라이드는 Day 2 전용 덱으로 압축 운영한다.

## Day 2 빠른 시작

| 구분 | 파일 | 용도 |
|------|------|------|
| Day 2 운영 맵 | [day2-overview.md](day2-overview.md) | 전체 진행 순서, 실습 연결, 종료 기준 |
| Session 1 가이드 | [day2-session1.md](day2-session1.md) | Agent 4요소, Planner-Executor, 구조 판단 |
| Session 2 가이드 | [day2-session2.md](day2-session2.md) | LangGraph 제어 흐름, Conditional Edge, Retry/Fallback |
| Session 3 가이드 | [day2-session3.md](day2-session3.md) | Tool Validation, 통제 로직, 감사 로깅 |
| Session 4 가이드 | [day2-session4.md](day2-session4.md) | Multi-Agent 확장, 서브그래프, 리팩토링 |
| Day 2 Lab Pack | [`../labs/day2/README.md`](../labs/day2/README.md) | Day 2 전체 실습 동선 |
| Day 2 Slide Deck | [`../slides/day2-slides.md`](../slides/day2-slides.md) | Day 2 전용 강의 진행 슬라이드 |

## Day 1에서 받아오는 입력

Day 2는 Day 1 산출물을 그대로 사용한다.

- Day 1 문제 정의 결과 -> Agent 목표와 구조 입력
- Day 1 프롬프트 전략 비교 -> Tool 통제 기준
- Day 1 구조 판단표 -> Day 2 확장 설계 기준선
- Day 1 MVP 후보 1개 -> Day 2 통합 실습 대상

## Day 2 세션별 운영 맵

| 세션 | 핵심 질문 | 가이드 기준 | 권장 이론 | 권장 실습 | Lab Pack handoff | Slide handoff |
|------|-----------|-------------|-----------|-----------|------------------|---------------|
| Session 1 | Agent를 어떤 State와 실행 단위로 쪼갤 것인가 | [day2-session1.md](day2-session1.md) | 35분 | 55분 | Agent 구조 설계 워크숍, Planner-Executor 초안 | Day 2 Deck Section 1 |
| Session 2 | 그래프 제어 흐름을 어떻게 설계할 것인가 | [day2-session2.md](day2-session2.md) | 35분 | 55분 | LangGraph 라우팅 실습, Retry/Fallback 패턴 실습 | Day 2 Deck Section 2 |
| Session 3 | Tool 호출을 어떻게 통제하고 검증할 것인가 | [day2-session3.md](day2-session3.md) | 35분 | 55분 | Validation gate, 결과 검증, 감사 로그 실습 | Day 2 Deck Section 3 |
| Session 4 | 구조를 어떻게 확장 가능한 형태로 리팩토링할 것인가 | [day2-session4.md](day2-session4.md) | 40분 | 50분 | Subgraph, Multi-Agent, Day 2 통합 구현 | Day 2 Deck Section 4 |

## Day 2 실습 흐름

| 순서 | 실습 | 형식 | 연관 세션 | 권장 시간 | 실제 파일 |
|------|------|------|----------|----------|-----------|
| 1 | Agent 구조 설계 워크숍 | README 중심 | Session 1 | 70분 | [`../labs/day2/01-agent-architecture-studio/README.md`](../labs/day2/01-agent-architecture-studio/README.md) |
| 2 | LangGraph Control Flow 구현 | 코드 | Session 2 | 85분 | [`../labs/05-langgraph-control-flow/README.md`](../labs/05-langgraph-control-flow/README.md) |
| 3 | Tool Validation Guard와 Audit Trail | 코드 | Session 3 | 80분 | [`../labs/06-tool-validation-guard/README.md`](../labs/06-tool-validation-guard/README.md) |
| 4 | 리팩토링 경계 워크숍 | README 중심 | Session 4 | 35분 | [`../labs/day2/02-refactor-boundary-workshop/README.md`](../labs/day2/02-refactor-boundary-workshop/README.md) |
| 5 | Subgraph Refactor Parity 검증 | 코드 | Session 4 | 65분 | [`../labs/07-subgraph-refactor-parity/README.md`](../labs/07-subgraph-refactor-parity/README.md) |

**실습 총량 목표**: 335분

## 강사용 진행 순서

### 1. Session 1 직후

- `day2-session1.md`의 개념 설명은 짧게 정리하고 바로 `01-agent-architecture-studio`로 넘긴다.
- 이 워크숍 안에서 4요소 설계, sub-task 분해, 구조 판단을 한 번에 묶어 처리한다.

### 2. Session 2 직후

- 세션 가이드의 예제는 분기 설계 기준으로만 사용한다.
- 구현 감각은 `05-langgraph-control-flow` 단일 코드 랩에서 확보한다.
- 이 시점에 학생별 그래프 초안을 반드시 남긴다.

### 3. Session 3 직후

- Validation 규칙을 말로만 끝내지 않는다.
- `06-tool-validation-guard`에서 허용 Tool, 호출 한도, 결과 검증, audit trail을 한 흐름으로 구현하게 한다.
- 감사 로그는 Day 4 평가 체계의 입력으로 연결한다.

### 4. Session 4 직후

- 통합 구현 전에 `02-refactor-boundary-workshop`으로 리팩토링 기준을 먼저 합의한다.
- 이후 `07-subgraph-refactor-parity`에서 실제 분리와 parity 검증을 수행한다.
- Session 4는 문서 -> 코드 순서로 운영한다.

## Day 2에서 남겨야 하는 핵심 산출물

- Agent State 초안 1개
- Planner-Executor 또는 동등한 제어 흐름 그래프 1개
- Conditional Edge 분기표 1개
- Retry/Fallback 정책 메모 1개
- Tool Validation 규칙표 1개
- Audit Trail 설계 또는 로그 예시 1개
- 리팩토링 전후 구조 비교 1개
- Day 2 통합 Agent 프로토타입 1개

## Day 2 종료 체크리스트

- [ ] Day 1에서 가져온 MVP 후보가 Day 2 구조로 구체화되었는가
- [ ] State, Node, Edge 기준으로 Agent 구조를 설명할 수 있는가
- [ ] Tool 호출 전 Validation 규칙을 명시적으로 정의했는가
- [ ] Retry, Fallback, Loop guard를 그래프 수준에서 설명할 수 있는가
- [ ] Session 4 통합 구현이 Day 3의 MCP/RAG 확장 입력으로 쓸 수 있는가

## 다음 산출물 연결

- Day 2 guide는 세션별 설명의 Source of Truth다.
- Day 2 Lab Pack은 이 문서의 실습 흐름을 그대로 따른다.
- Day 2 Slide Deck은 이 문서의 세션별 운영 맵을 발표 흐름으로 압축한다.
