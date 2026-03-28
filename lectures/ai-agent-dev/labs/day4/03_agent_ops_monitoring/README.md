### Agent 운영 모니터링 실습

Trace 로그 구조, 장애 분류, Guardrail, 운영 지표 집계까지 Agent 시스템을 안정적으로 운영하기 위한 모니터링 체계를 학습한다.

### 학습 목표

- Langfuse로 Agent 호출 전체를 Trace/Span으로 기록하고 조회한다
- 4가지 장애 유형(LLM 품질, Tool 실행, 시스템)을 시뮬레이션하고 식별한다
- PII 마스킹, 프롬프트 인젝션 감지 등 Input/Output Guardrail을 구현한다
- 미들웨어 패턴으로 Guardrail을 리팩터링한다
- Trace 데이터에서 운영 지표를 집계하고 알림 임계값을 설정한다

### 실습 구성

| 단계 | 내용 |
|------|------|
| Trace 구조 | Agent 호출의 Trace → Span 기록 구조 이해 |
| 장애 시뮬레이션 | LLM 품질, Tool 실행, 시스템 장애 재현 |
| Guardrail | PII 마스킹, 프롬프트 인젝션 감지, 통합 파이프라인 |
| 미들웨어 리팩터링 | PIIMiddleware, ModelCallLimit, 프로덕션 스택 조합 |
| 운영 지표 | Trace 데이터 기반 대시보드, 알림 임계값 설정 |
| Score 기록 | Langfuse Score로 품질 피드백 기록 |

### 사전 준비

- OpenAI API Key
- Langfuse 환경 (트레이스 기록용)
