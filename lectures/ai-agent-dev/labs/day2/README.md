# Day 2 Lab Pack: 구조 설계 -> 제어 흐름 -> Validation -> 리팩토링

Day 2는 **이론 3 : 실습 7** 비율을 기준으로 운영한다.
이 문서는 Day 2 전체를 하나의 실습 동선으로 이어서 따라갈 수 있도록 정리한 실습 패키지다.

## Day 2 운영 원칙

- Day 2 총 수업 시간: 480분
- 권장 이론 시간: 약 145분
- 권장 실습 시간: 약 335분
- Session 1과 Session 4의 설계/판단 과제는 README 중심 실습으로 운영한다.
- Session 2와 Session 3은 LangGraph 제어 흐름과 Tool 통제 로직을 직접 구현하는 코드 실습으로 운영한다.
- Day 2 마지막 코드 실습은 모놀리식 그래프를 서브그래프 구조로 리팩토링하면서 동작 동일성(parity)을 확인하는 흐름으로 마무리한다.

## Day 2 실습 흐름

| 순서 | 실습 | 형식 | 연관 세션 | 권장 시간 |
|------|------|------|----------|----------|
| 1 | [01-agent-architecture-studio](01-agent-architecture-studio/README.md) | README 중심 | Session 1 | 70분 |
| 2 | [`../05-langgraph-control-flow`](../05-langgraph-control-flow/README.md) | 코드 | Session 2 | 85분 |
| 3 | [`../06-tool-validation-guard`](../06-tool-validation-guard/README.md) | 코드 | Session 3 | 80분 |
| 4 | [02-refactor-boundary-workshop](02-refactor-boundary-workshop/README.md) | README 중심 | Session 4 | 35분 |
| 5 | [`../07-subgraph-refactor-parity`](../07-subgraph-refactor-parity/README.md) | 코드 | Session 4 | 65분 |

**실습 총량 합계**: 335분

## 실습 결과로 남겨야 하는 핵심 산출물

- Agent 4요소 설계 캔버스 1개
- Sub-task 분해표와 의존성 그래프 1개
- Single-step vs Multi-step 판단 기록 1개
- Conditional edge / retry / fallback 설계 메모 1개
- Tool validation 정책표와 감사 로그 샘플 1개
- 모놀리식 -> 서브그래프 리팩토링 경계 문서 1개
- 리팩토링 전후 parity 검증 결과 1개

## 권장 진행 방식

### 1. Session 1 직후

- `01-agent-architecture-studio`에서 Day 1 산출물을 입력으로 사용해 Agent 구조를 먼저 정리한다.
- 이 단계에서는 아직 코드를 만들기보다 Goal / Memory / Tool / Control Logic의 경계와 sub-task 전략을 고정한다.

### 2. Session 2 직후

- `05-langgraph-control-flow`에서 분기, 루프, fallback이 있는 그래프를 직접 구현한다.
- Session 1에서 만든 구조 판단 결과를 State 필드와 edge 설계로 번역하는 데 집중한다.

### 3. Session 3 직후

- `06-tool-validation-guard`에서 Tool 호출 전/후 검증, 거부 사유, audit trail을 코드로 만든다.
- Day 1의 Function Calling 경험을 "통제 가능한 Agent" 구조로 업그레이드하는 단계로 설명한다.

### 4. Session 4 직후

- 먼저 `02-refactor-boundary-workshop`에서 분리 경계, 인터페이스 계약, 체크포인트 전략을 문서로 정리한다.
- 이후 `07-subgraph-refactor-parity`에서 실제로 모놀리식 그래프를 서브그래프 구조로 분해하고 parity를 확인한다.

## Day 2 종료 체크리스트

- [ ] Agent 4요소가 State 필드와 제어 흐름으로 연결되어 있는가
- [ ] Conditional edge와 loop의 종료 조건을 설명할 수 있는가
- [ ] Tool 호출 전에 schema / policy / context 검증 단계를 구분할 수 있는가
- [ ] 위험한 Tool 호출이 왜 차단되었는지 audit trail로 설명할 수 있는가
- [ ] 모놀리식 그래프를 어떤 기준으로 subgraph로 분리했는지 말할 수 있는가
- [ ] 리팩토링 전후 결과가 동일하다는 parity 근거를 제시할 수 있는가

## Day 3로 가져갈 것

Day 3부터는 Day 2에서 만든 구조물을 그대로 사용한다.

- Agent 구조 캔버스 -> Multi-Agent 협업 구조의 입력
- Validation 정책표 -> 인간 승인(HITL) / 안전장치 설계의 기준선
- 리팩토링 경계 문서 -> Supervisor / Subgraph / Checkpoint 확장 설계의 출발점
