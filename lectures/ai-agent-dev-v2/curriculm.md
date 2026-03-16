# AI Agent 전문 개발 과정

## 과정 개요

### 교육 기간

**5 Days (40h)**

### 교육 목표

**MCP·RAG·Hybrid 아키텍처 기반의 고도화된 실무형 AI Agent MVP를 직접 설계·구현하고 운영 역량까지 내재화**

### 핵심 기술 스택

* LLM Strategy
* RAG
* MCP
* LangGraph
* Hybrid Architecture

### Target Audience

* AI 개발자
* 데이터 엔지니어
* 기술 리더

---

# 5-Day Curriculum Overview

## Day 1 — 문제 정의 & 설계

* Agent 문제 정의 및 과제 도출
* LLM 설계 전략 (JSON Schema)
* MCP · RAG · Hybrid 구조 판단

---

## Day 2 — 제어 흐름 & 상태

* LangGraph 기반 제어 흐름 설계
* Tool 호출 통제 및 Validation
* 구조 리팩토링 및 확장성 설계

---

## Day 3 — MCP · RAG 구현

* 외부 API · 데이터 연동 최적화
* RAG 성능 결정 4요소 및 튜닝
* Hybrid 아키텍처 설계 판단

---

## Day 4 — 평가 & 운영 전략

* Agent 품질 평가 체계 설계
* 로그 · 모니터링 · 장애 대응 설계
* 확장 가능한 서비스 아키텍처

---

## Day 5 — MVP Day

### 프로젝트 수행

* 개인별 Agent 프로젝트 MVP 완성
* 성능 개선 및 안정화 집중 개발

### 최종 발표

* 최종 동작 시연 및 구조 설명 발표
* Best Architecture 선정

---

# 핵심 산출물 (Key Outputs)

* 아키텍처 다이어그램
* Golden Test Set & 평가표
* 실무형 Agent MVP

---

# 상세 커리큘럼

# Day 1 — Agent 문제 정의 & LLM 설계 전략

| 과정 제목                    | 시간 | 세부 내용                                                                                                                                              | 실습 예시                                            |
| ------------------------ | -- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Agent 문제 정의와 과제 도출       | 2h | Agent가 적합한 문제 유형 정의<br>Pain → Task → Skill → Tool 프레임워크<br>업무 유형별 Agent 패턴 (자동화형 / 분석형 / Planner형)<br>RAG vs Agent 판단 기준                           | 개인 업무 기반 Agent 후보 2개 도출<br>RAG/Agent 구조 선택 이유 작성 |
| LLM 동작 원리 및 프롬프트 전략 심화   | 2h | Context Window, Token, Hallucination 이해<br>Zero-shot / Few-shot / CoT 전략 비교<br>Structured Output 및 JSON Schema 응답 통제 전략<br>비용·Latency 관점 호출 최적화 설계 | 프롬프트 전략별 응답 비교 실습                                |
| Agent 기획서 구조화            | 2h | Task → Sub-task → Workflow 분해 설계<br>Stateless vs Stateful 구조 이해<br>Input–Process–Output 명확화<br>예외 처리 및 실패 케이스 전략                                   | Agent 구조 다이어그램 설계                                |
| MCP · RAG · Hybrid 구조 판단 | 2h | MCP(Function Calling) Tool 설계 기준<br>RAG 구조 (Chunking / Embedding / Retrieval)<br>Tool 중심 vs RAG 중심 구조 비교<br>Hybrid 설계 시 정확도·비용·확장성 고려              | MCP vs RAG 구조 설계 비교                              |

---

# Day 2 — Agent 제어 흐름 설계 & 상태 관리

| 과정 제목                   | 시간 | 세부 내용                                                                                                                     | 실습 예시                 |
| ----------------------- | -- | ------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| Agent 4요소 구조 설계         | 2h | Goal · Memory · Tool · Control Logic 정의<br>Planner–Executor 구조 설계<br>Sub-task 분해 전략<br>Single-step vs Multi-step Agent 판단 | Agent 상태 다이어그램 작성     |
| LangGraph 기반 제어 흐름 설계   | 2h | Node–Edge–State 구조 이해<br>Conditional 분기 설계<br>Retry / Fallback 전략<br>State Propagation 방식                                 | Workflow 구현           |
| Tool 호출 통제 & Validation | 2h | Function Calling 설계 전략<br>JSON Schema 응답 강제 구조<br>Tool 호출 전후 검증 로직<br>무한 Loop 방지 전략                                       | Tool 실패 시 Fallback 구현 |
| 구조 리팩토링 & 확장성 설계        | 2h | 단일 Agent → 확장형 구조 전환<br>결합도 낮추는 설계 전략<br>Trace 로그 구조 설계 기초<br>유지보수 가능한 구조 기준                                              | 기존 설계 리팩토링            |

---

# Day 3 — MCP · RAG 구현 & 외부 시스템 연동

| 과정 제목                       | 시간 | 세부 내용                                                                                                    | 실습 예시                  |
| --------------------------- | -- | -------------------------------------------------------------------------------------------------------- | ---------------------- |
| MCP(Function Calling) 고급 설계 | 2h | JSON Schema Tool 정의 전략<br>Tool 선택 정확도 향상 Prompt 설계<br>Multi-tool Routing 전략<br>Tool 실패 재시도·Fallback      | 복수 Tool 선택 정확도 비교      |
| 외부 API · 데이터 연동 최적화         | 2h | REST API 연동 및 Latency 최소화<br>비동기 vs 동기 처리 설계<br>Schema Validation / Guardrail<br>인증·보안·Rate Limit 설계     | API 연동 후 검증 로직 비교      |
| RAG 성능을 결정하는 4가지 요소         | 2h | Chunking 전략 비교<br>Embedding 모델 선택<br>Retrieval 튜닝 (Top-k, Threshold, Re-ranking)<br>Hallucination 최소화 전략 | Chunk 전략별 Retrieval 비교 |
| Hybrid 아키텍처 설계              | 2h | MCP 중심 vs RAG 중심 구조 기준<br>Retrieval 이후 Tool 호출 패턴<br>정확도·비용·확장성 Trade-off                                | Hybrid 구조 아키텍처 설계      |

---

# Day 4 — 평가 · 운영 · 확장 아키텍처 전략

| 과정 제목                        | 시간 | 세부 내용                                                                                                 | 실습 예시      |
| ---------------------------- | -- | ----------------------------------------------------------------------------------------------------- | ---------- |
| Agent 품질 평가 체계 설계            | 2h | Accuracy · Faithfulness · Robustness 정의<br>정량 / 정성 평가 설계<br>Golden Test Set 구축<br>LM-as-a-Judge 적용 기준 | 평가 기준 설계   |
| Prompt · RAG · Tool 성능 개선 전략 | 2h | 성능 저하 원인 분석<br>Prompt 버전 관리<br>Retrieval Drift 대응<br>Tool 호출 정확도 개선                                   | 성능 개선 분석   |
| 로그 · 모니터링 · 장애 대응 설계         | 2h | Trace 로그 구조 설계<br>Root Cause 분석 프로세스<br>실패 유형 분류<br>Guardrail & Validation Layer                      | 실패 로그 분석   |
| 확장 가능한 서비스 아키텍처              | 2h | Dev–Staging–Prod 분리 전략<br>Scaling 전략<br>Multi-Agent 구조<br>운영 비용 최적화                                   | 운영 아키텍처 설계 |

---

# Day 5 — 개인 Agent 프로젝트 (MVP Day)

| 과정 제목       | 시간 | 세부 내용                                                                                | 실습 예시                 |
| ----------- | -- | ------------------------------------------------------------------------------------ | --------------------- |
| 프로젝트 설계 확정  | 2h | 문제 정의 재검토<br>MCP/RAG/Hybrid 구조 선택<br>평가 기준 설정<br>MVP 범위 정의                           | 프로젝트 설계서 정리           |
| 핵심 기능 구현    | 2h | Agent 제어 흐름 구현<br>Tool 호출 / Retrieval 개선<br>Structured Output<br>Validation Layer 적용 | MCP + RAG 기반 Agent 구현 |
| 성능 개선 & 안정화 | 2h | Golden Test Set 기반 평가<br>Prompt 튜닝<br>Retrieval 파라미터 조정<br>Latency 최적화               | 성능 리포트 작성             |
| 최종 시연 및 발표  | 2h | 구조 설명 및 Demo<br>성능 개선 Trade-off 설명<br>운영 리스크 대응 전략                                   | 10분 Demo + 5분 Q&A     |