# Day 1 Lab Pack: 문제 정의 -> 프롬프트 -> 기획서 -> 구조 판단

Day 1은 **이론 3 : 실습 7** 비율을 기준으로 운영한다.
이 문서는 Day 1 전체 실습 동선을 한 번에 따라갈 수 있도록 정리한 실습 패키지다.

## Day 1 운영 원칙

- Day 1 총 수업 시간: 480분
- 권장 이론 시간: 약 145분
- 권장 실습 시간: 약 335분
- 실습은 **코드 실습 + README 중심 실습**을 함께 사용한다.
- 코드가 학습 목표에 직접 기여하지 않으면 억지로 Python 파일을 만들지 않는다.

## Day 1 실습 흐름

| 순서 | 실습 | 형식 | 연관 세션 | 권장 시간 |
|------|------|------|----------|----------|
| 1 | [01-agent-opportunity-workshop](01-agent-opportunity-workshop/README.md) | README 중심 | Session 1 | 75분 |
| 2 | [`../01-prompt-strategy`](../01-prompt-strategy/README.md) | 코드 | Session 2 | 30분 |
| 3 | [`../02-structured-output`](../02-structured-output/README.md) | 코드 | Session 2 | 35분 |
| 4 | [02-cost-latency-design-clinic](02-cost-latency-design-clinic/README.md) | README 중심 | Session 2 | 20분 |
| 5 | [03-agent-spec-studio](03-agent-spec-studio/README.md) | README 중심 | Session 3 | 75분 |
| 6 | [`../03-function-calling`](../03-function-calling/README.md) | 코드 | Session 4 | 30분 |
| 7 | [`../04-rag-pipeline`](../04-rag-pipeline/README.md) | 코드 | Session 4 | 30분 |
| 8 | [04-architecture-decision-clinic](04-architecture-decision-clinic/README.md) | README 중심 | Session 4 | 25분 |
| 9 | Day 1 실습 회고 및 연결 | README 중심 | Day 1 전체 | 15분 |

**실습 총량 합계**: 335분

## 실습 결과로 남겨야 하는 핵심 산출물

- Agent 후보 2개 이상과 선정 근거
- 프롬프트 전략 비교 결과표
- Structured Output 설계 규칙 요약
- 비용/Latency 최적화 설계 메모
- Agent 기획서 초안 1개
- 기획서 품질 개선 기록 1개
- 기술 설계 보완 메모 1개
- MCP / RAG / Hybrid 의사결정표 1개

## 권장 진행 방식

### 1. Session 1 직후

- `01-agent-opportunity-workshop`으로 Pain-Task-Skill-Tool 분석부터 시작한다.
- 아직 코드를 만들지 않는다.
- Day 1의 나머지 모든 실습에서 사용할 후보 2개를 여기서 확정한다.

### 2. Session 2 직후

- 코드 실습 2개(`01-prompt-strategy`, `02-structured-output`)를 수행한다.
- 이어서 `02-cost-latency-design-clinic`에서 "어떤 전략을 언제 쓸지"를 문서로 정리한다.

### 3. Session 3 직후

- `03-agent-spec-studio`에서 Day 1 오전에 고른 후보를 실제 기획서로 변환한다.
- 이 산출물은 Session 4 실습과 Day 5 MVP 설계의 입력값으로 사용한다.

### 4. Session 4 직후

- 코드 실습 2개(`03-function-calling`, `04-rag-pipeline`)로 실행 감각을 확보한다.
- 마지막에 `04-architecture-decision-clinic`으로 MCP / RAG / Hybrid 선택을 정리한다.

## Day 1 종료 체크리스트

- [ ] Agent 후보 2개가 Pain 기준으로 정리되었는가
- [ ] Session 2의 전략 선택 결과를 비용/정확도 관점에서 설명할 수 있는가
- [ ] Agent 기획서가 목적, 입력, 출력, 제약, 성공 기준, 범위를 모두 포함하는가
- [ ] Session 4에서 MCP / RAG / Hybrid 중 하나를 선택하고 대안을 배제한 이유를 말할 수 있는가
- [ ] Day 5 MVP로 이어질 핵심 후보 1개를 확정했는가

## Day 2로 가져갈 것

Day 2부터는 Day 1에서 만든 산출물을 그대로 사용한다.

- Session 1/3 워크숍 결과 -> Day 2 구조 설계 입력
- Session 2 전략 비교 결과 -> Day 2 Tool/Validation 설계 기준
- Session 4 의사결정표 -> Day 3~5 아키텍처 기준선
