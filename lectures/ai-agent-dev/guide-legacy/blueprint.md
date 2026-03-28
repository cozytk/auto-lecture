# AI Agent 전문 개발 과정 — Day 1 Blueprint
<!-- blueprint-version: 1.0 -->
<!-- status: draft -->

## META
- **주제**: AI Agent 전문 개발 과정
- **수강 대상**: AI 개발자, 데이터 엔지니어, 기술 리더 — Python 경험 있고 LLM API 호출 경험 1회 이상. Agent 설계/구현은 초보~중급
- **사전 요구사항**: Python 3.12+, VS Code, GitHub Copilot, Git, uv
- **기간**: 5일 (40시간) — 이 문서는 **Day 1만** 다룸
- **비율**: 강의 30% / 실습 70%
- **실행 환경**: Local (Linux/macOS), VS Code + GitHub Copilot

## 학습 목표
1. AI Agent가 적합한 문제 유형을 구분하고, Pain→Task→Skill→Tool 프레임워크로 업무를 분석할 수 있다
2. Token, Context Window, Hallucination 등 LLM 핵심 개념을 이해하고, 상황별 프롬프트 전략(Zero-shot/Few-shot/CoT)을 선택할 수 있다
3. 복잡한 업무를 Task→Sub-task→Workflow로 분해하고, 실무형 Agent 기획서를 작성할 수 있다
4. MCP, RAG, Hybrid 아키텍처의 차이를 비교하고 주어진 문제에 최적 구조를 판단할 수 있다

## DAY 1 — 문제 정의 & 설계

### [09:00-11:00] Agent 문제 정의와 과제 도출 (120분)
<!-- session: d1s1 -->
**학습 목표**: #1

#### 블록 1: Agent란 무엇인가 (15분) [강의]
<!-- block: d1s1b1 -->
- **핵심 메시지**: Agent는 목표를 받으면 스스로 계획-실행-관찰을 반복하는 시스템이다 — 단순 LLM 호출과 근본적으로 다르다
- **개념**: Agent 정의 (추론-행동-관찰 루프), Agent 구성요소 (LLM, Memory, Tools, Env), Agent vs 단순 LLM 호출 비교
- **교수법**: 실무 사례 제시 → 정의 → 비교표로 차이 명확화
- **슬라이드**: 5장, 시각: Mermaid 구성요소 다이어그램 + 비교표
- **핵심 비유**: "인턴 vs 자판기 — 자판기는 버튼 누르면 고정 결과, 인턴은 목표를 주면 알아서 계획하고 실행"

#### 블록 2: Agent가 적합한 문제 판별 (10분) [강의]
<!-- block: d1s1b2 -->
- **핵심 메시지**: 모든 문제에 Agent가 필요한 건 아니다 — "판단이 필요한 반복 업무"가 Agent의 스윗 스팟
- **개념**: 적합한 문제 4가지 유형, 부적합한 문제 4가지 유형, Pain→Task→Skill→Tool 프레임워크
- **교수법**: 적합/부적합 예시 → 프레임워크 소개 → 실무 적용 데모
- **슬라이드**: 4장, 시각: 적합/부적합 2x2 매트릭스 + 프레임워크 흐름도
- **혼동 주의**: "RAG도 Agent인가?" — RAG는 검색 증강이고 Agent는 자율 행동 시스템. 겹칠 수 있지만 동의어 아님

#### 블록 3: Agent 후보 도출 실습 (85분) [실습]
<!-- block: d1s1b3 -->
- **실습 유형**: README 중심
- **난이도**: 기초
- **연관 학습 목표**: #1
- **I DO** (15분): 강사의 실제 업무에서 Pain→Task→Skill→Tool 분석 시연 + Agent 후보 2개 도출 과정
- **WE DO** (30분): 수강생이 각자 업무를 분석하되, 강사가 3명 지목하여 함께 프레임워크 적용. 중간 점검
- **YOU DO** (40분): 개인 업무 기반 Agent 후보 2개 도출 + RAG/Agent 구조 선택 이유 작성. 모범 답안 제공
- **기술 스택**: 워크시트 (마크다운 템플릿)
- **검증 방법**: 산출물 확인 — Agent 후보 2개 + 구조 선택 근거 문서

#### Q&A Bank
| # | 유형 | 질문 | 핵심 답변 |
|---|------|------|-----------|
| 1 | 흔한 오해 | ChatGPT도 Agent 아닌가요? | ChatGPT는 대화형 LLM. 도구 호출+자율 계획 없이는 Agent가 아님. Plugins/GPTs는 Agent에 가까워지는 중 |
| 2 | 논쟁적 | Agent가 정말 필요한 경우가 얼마나 되나요? | 대부분의 업무는 잘 설계된 프롬프트+RAG로 충분. Agent는 다단계 판단이 필수인 10~20%의 복잡 업무에 적합 |
| 3 | 배경별 | 데이터 엔지니어인데 Agent를 어디에 쓸 수 있나요? | ETL 파이프라인 모니터링, 데이터 품질 이상 감지 후 자동 조치, 스키마 변경 영향 분석 등 |

#### 혼동 포인트
- **Agent vs Chatbot**: Chatbot은 대화 UI, Agent는 자율 행동 시스템. Agent가 Chatbot UI를 쓸 수 있지만 동의어 아님
- **자동화 스크립트 vs Agent**: 스크립트는 고정 로직, Agent는 LLM으로 동적 판단. if-else 분기가 폭발하면 Agent 도입 시점

---

### [11:00-11:15] 쉬는 시간 (15분)

---

### [11:15-13:15] LLM 동작 원리 및 프롬프트 전략 심화 (120분)
<!-- session: d1s2 -->
**학습 목표**: #2

#### 블록 1: LLM 핵심 개념 (15분) [강의]
<!-- block: d1s2b1 -->
- **핵심 메시지**: Agent 개발자는 Token, Context Window, Temperature 세 가지를 반드시 이해해야 LLM을 통제할 수 있다
- **개념**: Token과 토큰화 (한국어 vs 영어 비용 차이), Context Window (모델별 비교), Temperature (결정적 vs 창의적)
- **교수법**: 시각화 → 모델별 비교표 → Agent에서의 권장값
- **슬라이드**: 5장, 시각: Context Window 구성 다이어그램 + 모델별 비교표 + Temperature 스펙트럼
- **핵심 비유**: "Context Window는 책상 크기 — 책상이 크면 많은 자료를 펼칠 수 있지만, 비용도 커진다"

#### 블록 2: Hallucination과 프롬프트 전략 (20분) [강의]
<!-- block: d1s2b2 -->
- **핵심 메시지**: Hallucination은 피할 수 없지만, 프롬프트 전략과 Structured Output으로 통제 가능하다
- **개념**: Hallucination 발생 원인 3가지, Zero-shot/Few-shot/CoT 전략 비교, Structured Output (JSON Schema), 비용·Latency 최적화
- **교수법**: 실패 사례 → 원인 분석 → 전략별 비교 → JSON Schema 데모
- **슬라이드**: 7장, 시각: 전략 비교표 + JSON Schema 코드 예시 + 비용 계산 예시
- **혼동 주의**: "Few-shot이 항상 Zero-shot보다 좋은가?" — 아님. 토큰 비용 대비 정확도 향상이 미미하면 Zero-shot이 낫다

#### 블록 3: 프롬프트 전략 비교 실습 (85분) [실습]
<!-- block: d1s2b3 -->
- **실습 유형**: 코드
- **난이도**: 기초~중급
- **연관 학습 목표**: #2
- **I DO** (15분): 동일 과제를 Zero-shot → Few-shot → CoT로 호출하며 응답 품질 비교 시연. Structured Output 적용
- **WE DO** (30분): 수강생이 함께 프롬프트를 작성하고 API를 호출. 각 전략별 응답을 비교하고 비용 계산
- **YOU DO** (40분): 주어진 3개 시나리오에 최적 전략 선택 + JSON Schema 응답 통제 구현. solution/ 제공
- **기술 스택**: Python, OpenAI API, Pydantic
- **검증 방법**: 테스트 실행 — 3개 시나리오 모두 유효한 JSON 응답 반환

---

### [13:15-14:15] 점심 시간 (60분)

---

### [14:15-16:15] Agent 기획서 구조화 (120분)
<!-- session: d1s3 -->
**학습 목표**: #3

#### 블록 1: Task 분해와 Workflow 설계 (20분) [강의]
<!-- block: d1s3b1 -->
- **핵심 메시지**: Agent에게 큰 목표를 던지면 실패한다 — Task→Sub-task→Step으로 분해해야 각 단계의 정확도가 올라간다
- **개념**: 3단계 분해 (Task→Sub-task→Step), MECE 원칙, 단일 책임 원칙, Workflow 패턴 (순차/병렬/조건분기)
- **교수법**: 실패 사례("주간 보고서 작성해줘") → 분해 과정 → Workflow 다이어그램
- **슬라이드**: 6장, 시각: Mermaid Task 분해 트리 + Workflow 패턴 3종 다이어그램
- **핵심 비유**: "레고 조립 설명서 — 한번에 완성품을 만들지 않고, 블록 단위로 조립하고 검증"

#### 블록 2: Agent 기획서 작성법 (15분) [강의]
<!-- block: d1s3b2 -->
- **핵심 메시지**: 좋은 Agent 기획서는 Input-Process-Output이 명확하고 예외 처리 전략이 포함되어 있다
- **개념**: Stateless vs Stateful 구조, Input-Process-Output 정의, 예외 처리 전략 (Retry, Fallback, Circuit Breaker)
- **교수법**: 기획서 템플릿 소개 → 좋은/나쁜 예시 비교 → 예외 처리 패턴
- **슬라이드**: 5장, 시각: 기획서 템플릿 + Stateless vs Stateful 비교 다이어그램 + 예외 처리 흐름도

#### 블록 3: Agent 기획서 작성 실습 (85분) [실습]
<!-- block: d1s3b3 -->
- **실습 유형**: README 중심
- **난이도**: 중급
- **연관 학습 목표**: #3
- **I DO** (15분): "주간 보고서 자동 생성 Agent" 기획서를 라이브로 작성. Task 분해 → Workflow → I/O → 예외 처리
- **WE DO** (30분): 수강생이 Session 1에서 도출한 Agent 후보 중 1개를 선택하여 함께 기획서 작성. 강사가 중간 피드백
- **YOU DO** (40분): 나머지 Agent 후보로 독립적으로 기획서 완성. 구조 다이어그램 포함. artifacts/ 모범 답안 제공
- **기술 스택**: 마크다운 템플릿, Mermaid (다이어그램)
- **검증 방법**: 산출물 확인 — 기획서 (Task 분해 + Workflow + I/O + 예외 처리) 완성도

---

### [16:15-16:30] 쉬는 시간 (15분)

---

### [16:30-18:30] MCP · RAG · Hybrid 구조 판단 (120분)
<!-- session: d1s4 -->
**학습 목표**: #4

#### 블록 1: MCP와 Function Calling (15분) [강의]
<!-- block: d1s4b1 -->
- **핵심 메시지**: MCP는 LLM과 외부 도구 연결의 표준 프로토콜이다 — Function Calling의 상위 개념으로 재사용성을 높인다
- **개념**: Function Calling 메커니즘 (LLM은 실행하지 않고 호출 명세만 출력), MCP 프로토콜 (Client-Server 분리, JSON-RPC), MCP vs 직접 Function Calling 비교, 도구 설계 기준
- **교수법**: Sequence Diagram → MCP 아키텍처 → 비교표 → 설계 원칙
- **슬라이드**: 5장, 시각: Mermaid Sequence Diagram (Function Calling 흐름) + MCP 아키텍처 다이어그램 + 비교표

#### 블록 2: RAG와 Hybrid 아키텍처 (20분) [강의]
<!-- block: d1s4b2 -->
- **핵심 메시지**: RAG는 "검색 후 생성", MCP는 "행동 후 생성" — 문제에 따라 하나 또는 둘 다 필요하다
- **개념**: RAG 파이프라인 (Chunking→Embedding→Retrieval), RAG vs Tool 중심 구조 비교, Hybrid 아키텍처 (Retrieval 후 Tool 호출 패턴), 정확도·비용·확장성 트레이드오프
- **교수법**: RAG 파이프라인 시각화 → Tool 중심과 비교 → Hybrid 패턴 소개 → 의사결정 프레임워크
- **슬라이드**: 7장, 시각: RAG 파이프라인 다이어그램 + MCP vs RAG 비교표 + Hybrid 아키텍처 다이어그램 + 의사결정 플로차트

#### 블록 3: MCP vs RAG 구조 설계 실습 (85분) [실습]
<!-- block: d1s4b3 -->
- **실습 유형**: README 중심
- **난이도**: 중급
- **연관 학습 목표**: #4
- **I DO** (15분): 주어진 시나리오(고객 문의 자동 응답 Agent)를 MCP, RAG, Hybrid 관점에서 분석하고 구조 선택 과정 시연
- **WE DO** (30분): 2번째 시나리오(사내 문서 검색+API 연동 Agent)를 함께 분석. 트레이드오프 토론
- **YOU DO** (40분): Session 1에서 도출한 개인 Agent 후보에 최적 구조 선택 + 아키텍처 다이어그램 + 선택 근거 문서. artifacts/ 모범 답안 제공
- **기술 스택**: 마크다운, Mermaid (아키텍처 다이어그램)
- **검증 방법**: 산출물 확인 — 아키텍처 다이어그램 + MCP/RAG/Hybrid 선택 근거 + 트레이드오프 분석

#### Q&A Bank
| # | 유형 | 질문 | 핵심 답변 |
|---|------|------|-----------|
| 1 | 흔한 오해 | RAG가 항상 Agent보다 싸지 않나요? | 초기 비용은 RAG가 낮지만, 임베딩 유지보수·인덱스 갱신 비용까지 고려하면 단순 도구 호출이 더 쌀 수 있음 |
| 2 | 트러블슈팅 | MCP Server는 어떻게 배포하나요? | stdio(로컬), SSE(원격) 두 가지. 이 과정에서는 stdio로 로컬 실습, Day 3에서 SSE 원격 구성 |
| 3 | 논쟁적 | LangChain 안 쓰고 LangGraph만 써도 되나요? | LangGraph는 LangChain 위에 구축됐지만 독립 사용 가능. 이 과정에서는 LangGraph 중심으로 진행 |

#### 혼동 포인트
- **Function Calling vs MCP**: Function Calling은 메커니즘(LLM이 호출 명세 출력), MCP는 프로토콜(도구 서버-클라이언트 표준). MCP가 Function Calling을 포함하는 상위 개념
- **RAG vs Vector Search**: Vector Search는 RAG의 Retrieval 단계 구현 방식 중 하나. RAG = Retrieval + Augmented Generation 전체 파이프라인

---

## 슬라이드 설계 노트
- 총 예상 슬라이드: ~50장 (세션당 ~12장)
- 텍스트 전용 3장 연속 금지 — 각 세션에 Mermaid 다이어그램, 비교표, 코드 블록 교차 배치
- 커버 슬라이드: "AI Agent 전문 개발 과정 — Day 1: 문제 정의 & 설계"
- 섹션 구분: Agent 문제 정의 | LLM 프롬프트 전략 | Agent 기획서 | MCP·RAG·Hybrid
- 특별 슬라이드: Pain→Task→Skill→Tool 프레임워크 인터랙티브 (v-click 단계별 공개)

## 실습 총괄
| # | 실습명 | 세션 | 형식 | 난이도 | 시간 | block |
|---|--------|------|------|--------|------|-------|
| 1 | Agent 후보 도출 | d1s1 | README | 기초 | 85분 | d1s1b3 |
| 2 | 프롬프트 전략 비교 | d1s2 | 코드 | 기초~중급 | 85분 | d1s2b3 |
| 3 | Agent 기획서 작성 | d1s3 | README | 중급 | 85분 | d1s3b3 |
| 4 | MCP vs RAG 구조 설계 | d1s4 | README | 중급 | 85분 | d1s4b3 |
총 실습: 340분 / 전체: 480분 (71%)
