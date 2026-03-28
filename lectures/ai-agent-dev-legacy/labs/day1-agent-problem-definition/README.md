# 실습: Agent 문제 정의 및 기획서 작성

**유형**: 분석/설계 실습 (README 중심)
**소요 시간**: Session 1 (60분) + Session 3 (60분) = 약 2시간
**관련 세션**: Day 1 Session 1, Session 3, Session 4

---

## 실습 목표

- 실제 업무 기반으로 Agent 후보를 도출한다
- Pain → Task → Skill → Tool 프레임워크를 적용한다
- Agent 기획서(Sub-task + IPO + Workflow)를 완성한다
- MCP / RAG / Hybrid 구조를 선택하고 이유를 설명한다

---

## 디렉토리 구조

```
agent-problem-definition/
├── README.md                     # 이 파일 (실습 가이드)
└── artifacts/
    ├── my-agent-spec.md          # 수강생 작성 (YOU DO)
    ├── example-spec.md           # 모범 답안: AgentSpec
    ├── example-blueprint.md      # 모범 답안: 기획서 + Workflow
    └── example-architecture.md   # 모범 답안: 구조 결정
```

---

## I DO — 강사 시연 (30분)

강사가 자신의 실제 업무를 분석하여 Agent 후보를 도출하고 기획서까지 완성하는 과정을 실시간으로 보여준다.

### 시연 순서

1. **Pain 찾기**: "어떤 업무가 가장 반복적이고 오래 걸리는가?"
2. **프레임워크 적용**: Pain → Task → Skill → Tool 순서로 채우기
3. **패턴 분류**: 자동화형 / 분석형 / Planner형 중 선택
4. **Sub-task 분해**: Task를 3-5개 Sub-task로 나누기
5. **IPO 작성**: 가장 중요한 Sub-task의 Input/Output/Exception 정의
6. **구조 결정**: MCP / RAG / Hybrid 중 선택 + 이유

---

## WE DO — 함께 실습 (40분)

### 단계 1: Pain 찾기 (10분)

아래 질문에 답하며 자신의 Pain을 찾는다.

```
Q1. 매주 반복하는 업무 중 가장 시간이 오래 걸리는 것은?
Q2. "이게 자동화되면 좋겠다"고 생각해본 업무는?
Q3. 실수가 자주 발생해서 검토 시간이 오래 걸리는 업무는?
Q4. 여러 시스템에서 데이터를 모아서 처리해야 하는 업무는?
```

### 단계 2: 프레임워크 적용 (15분)

Pain 하나를 선택하여 아래 템플릿을 채운다.

```markdown
## Agent 후보 #1

**Pain**: [현재의 고통을 구체적으로]
예) "매주 화요일 오전에 Jira, 슬랙, 구글 시트 세 곳에서 데이터를 모아
     주간 보고서를 작성하는 데 2-3시간이 소요된다."

**Task**: [Agent가 수행할 과제]
예) "세 시스템 데이터를 자동 수집하여 주간 보고서를 생성하고 발송한다."

**Skills**:
- [능력 1]
- [능력 2]
- [능력 3]

**Tools**:
- [도구 1]: [용도]
- [도구 2]: [용도]
- [도구 3]: [용도]

**패턴**: 자동화형 / 분석형 / Planner형 (해당하는 것 선택)

**구조**: MCP / RAG / Hybrid (해당하는 것 선택)
**이유**: [1-2문장으로]
```

### 단계 3: 그룹 공유 (15분)

2-3명이 모여 작성한 내용을 공유하고 피드백을 준고받는다.

**피드백 체크리스트**:
- Pain이 구체적인가? ("힘들다"는 Pain이 아니다)
- Task가 측정 가능한 결과를 포함하는가?
- Tool이 Skill을 실제로 구현할 수 있는가?
- 패턴 분류가 적절한가?

---

## YOU DO — 독립 실습 (50분)

### 과제 1: Agent 후보 2개 도출 (20분)

위 프레임워크를 사용하여 자신의 업무에서 Agent 후보를 **2개** 도출한다.
두 후보는 서로 다른 패턴(자동화형 / 분석형 / Planner형)으로 선택하면 좋다.

### 과제 2: 기획서 작성 (20분)

두 후보 중 하나를 선택하여 기획서를 완성한다.

기획서에 포함할 내용:
- Sub-task 3개 이상 (각각 이름과 설명)
- 가장 중요한 Sub-task 1개의 전체 IPO 명세
- Workflow 순서 (ST-1 → ST-2 → ST-3)
- Stateless / Stateful 선택 이유

### 과제 3: 구조 결정 (10분)

기획서를 완성한 Agent에 대해 구조를 결정한다.

결정 문서에 포함할 내용:
- 최종 선택: MCP / RAG / Hybrid
- 선택 이유 3가지 이상
- 비선택 구조의 단점 설명
- 예상 비용 구조 (어떤 비용이 주로 발생하는가)

### 제출 방법

`artifacts/my-agent-spec.md` 파일을 생성하여 과제 1, 2, 3을 모두 작성한다.

---

## 평가 기준

| 항목 | 기준 | 배점 |
|------|------|------|
| Pain 구체성 | 수치나 빈도가 포함된 구체적 Pain | 20점 |
| 프레임워크 완성도 | Pain → Tool 모두 논리적으로 연결 | 30점 |
| 기획서 품질 | Sub-task 분해, IPO 명세의 완성도 | 30점 |
| 구조 판단 | 선택 이유가 논리적이고 근거 있음 | 20점 |

---

## 모범 답안

- `artifacts/example-spec.md` — AgentSpec 모범 답안
- `artifacts/example-blueprint.md` — 기획서 + Workflow 모범 답안
- `artifacts/example-architecture.md` — 구조 결정 모범 답안
