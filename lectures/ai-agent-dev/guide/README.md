# AI Agent 전문 개발 과정

## 과정 개요

AI Agent를 실무에서 설계·구현·운영할 수 있는 전문가를 양성하는 과정이다.
문제 정의부터 시스템 설계, LLM 전략, MCP·RAG 구조 판단까지 전 영역을 다룬다.

**대상**: AI 개발자, 데이터 엔지니어, 기술 리더
**기간**: 5일 (40시간)
**언어**: 한국어

---

## 수업 구성 원칙

- **강의 30% / 실습 70%** 비율 유지
- 모든 실습은 **I DO → WE DO → YOU DO** 3단계로 진행
- 각 세션은 6단계 개념 구조로 설명: 왜 중요한가 → 핵심 원리 → 실무 의미 → 비교 → 주의사항 → 코드 예제

---

## 전체 커리큘럼

### Day 1 — Agent 문제 정의 & LLM 설계 전략

| 세션 | 제목 | 시간 | 핵심 내용 |
|------|------|------|-----------|
| 1 | Agent 문제 정의와 과제 도출 | 2h | Pain→Task→Skill→Tool 프레임워크, 업무 패턴 분류 |
| 2 | LLM 동작 원리 및 프롬프트 전략 심화 | 2h | Context Window, 프롬프트 전략, Structured Output |
| 3 | Agent 기획서 구조화 | 2h | Task→Sub-task→Workflow 분해, I/O 명확화 |
| 4 | MCP · RAG · Hybrid 구조 판단 | 2h | Tool 설계 기준, RAG 구조, Hybrid 설계 |

**Day 1 실습 목록**:
- `labs/agent-problem-definition/` — 개인 업무 기반 Agent 후보 도출 (분석/설계)
- `labs/prompt-strategy-comparison/` — 프롬프트 전략별 응답 비교 (Python 코드)

---

### Day 2 — Agent 제어 흐름 설계 & 상태 관리

| 세션 | 제목 | 시간 | 핵심 내용 |
|------|------|------|-----------|
| 1 | Agent 4요소 구조 설계 | 2h | Goal·Memory·Tool·Control Logic, LangChain/LangGraph/DeepAgents 비교 |
| 2 | LangGraph 기반 제어 흐름 설계 | 2h | Node-Edge-State, 조건부 분기, 5가지 워크플로 패턴 |
| 3 | Tool 호출 통제 & Validation | 2h | Pydantic 스키마, 미들웨어, 무한 루프 방지 |
| 4 | 구조 리팩토링 & 확장성 설계 | 2h | Planner-Executor 분리, Deep Agents 하네스, Observability |

**Day 2 실습 목록**:
- `labs/day2/00_basics/` — 프레임워크 기초 (LangChain, LangGraph, DeepAgents)
- `labs/day2/01_langgraph_workflows/` — LangGraph 그래프 API 및 워크플로 패턴
- `labs/day2/02_tool_middleware/` — Tool 검증 및 미들웨어

### Day 3 — Agent 시스템 통합 (예정)

> 추후 추가 예정

### Day 4 — 평가 · 운영 · 확장 아키텍처 전략

| 세션 | 제목 | 시간 | 핵심 내용 |
|------|------|------|-----------|
| 1 | Agent 품질 평가 체계 설계 | 2h | Accuracy·Faithfulness·Robustness, Golden Test Set, LM-as-a-Judge |
| 2 | Prompt · RAG · Tool 성능 개선 전략 | 2h | 성능 저하 진단, Prompt 버전 관리, Retrieval Drift 대응 |
| 3 | 로그 · 모니터링 · 장애 대응 설계 | 2h | Trace 로그 구조, 장애 유형 분류, Guardrail & Validation |
| 4 | 확장 가능한 서비스 아키텍처 | 2h | Dev–Staging–Prod 분리, Scaling, Multi-Agent, 비용 최적화 |

**Day 4 실습 목록**:
- `labs/day4-golden-test-evaluation/` — Golden Test Set + LM-as-a-Judge 평가 파이프라인 (Python 코드)
- `labs/day4-ops-architecture-design/` — 운영 아키텍처 설계 워크시트 (분석/설계)

### Day 5 — 프로젝트 발표 & 최적화 (예정)

> 추후 추가 예정

---

## 디렉토리 구조

```
ai-agent-dev-v2/
├── guide/
│   ├── README.md              # 이 파일 (전체 개요)
│   ├── day1-session1.md       # Agent 문제 정의와 과제 도출
│   ├── day1-session2.md       # LLM 동작 원리 및 프롬프트 전략
│   ├── day1-session3.md       # Agent 기획서 구조화
│   └── day1-session4.md       # MCP · RAG · Hybrid 구조 판단
├── slides/
│   ├── day1-slides.md         # Day 1 Slidev 슬라이드
│   ├── style.css              # Freesentation 폰트 스타일
│   └── assets/fonts/          # 폰트 파일
└── labs/
    ├── agent-problem-definition/  # 분석/설계 실습
    └── prompt-strategy-comparison/ # 코드 실습
```
