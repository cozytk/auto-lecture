# Day 1 - Session 1: Agent 문제 정의와 과제 도출

**시간**: 2시간 | **대상**: AI 개발자, 데이터 엔지니어, 기술 리더

---

## 1. 왜 중요한가

### Agent가 모든 문제의 해답이 아니다

LLM 기술이 빠르게 발전하면서 "Agent로 다 해결할 수 있다"는 기대가 높아졌다.
하지만 잘못된 문제에 Agent를 적용하면 오히려 복잡도만 높아진다.
**문제 정의가 곧 프로젝트 성패를 결정한다.**

> 실무에서 Agent 프로젝트가 실패하는 가장 큰 이유:
> "왜 Agent가 필요한지" 명확히 정의하지 않고 시작하기 때문이다.

**이 세션에서 배우는 것**:
- Agent에 적합한 문제 유형 vs 부적합한 문제 유형
- Pain → Task → Skill → Tool 프레임워크
- 업무 유형별 Agent 패턴 분류
- RAG vs Agent 판단 기준

---

## 2. 핵심 원리

### 2-1. Agent에 적합한 문제 유형

**Agent가 빛을 발하는 조건**:

| 조건 | 설명 | 예시 |
|------|------|------|
| 다단계 추론 필요 | 여러 단계를 순차적으로 처리해야 함 | 데이터 수집 → 분석 → 보고서 작성 |
| 도구 사용 필요 | 외부 API, DB, 파일 시스템 접근 | 검색 + 계산 + 저장 |
| 비결정적 흐름 | 상황에 따라 다음 단계가 달라짐 | 에러 처리, 분기 로직 |
| 반복 작업 자동화 | 사람이 하면 지루하고 오래 걸리는 작업 | 이메일 분류, 보고서 집계 |

**Agent가 과잉인 경우**:

| 상황 | 더 나은 대안 |
|------|-------------|
| 단순 Q&A | 일반 챗봇 or RAG |
| 고정 템플릿 생성 | 프롬프트 엔지니어링 |
| 단일 API 호출 | 함수 직접 호출 |
| 정형 데이터 처리 | 전통적 파이프라인 |

---

### 2-2. Pain → Task → Skill → Tool 프레임워크

Agent 설계의 출발점은 **업무의 고통(Pain)**이다.
고통을 먼저 정의하고, 거슬러 올라가며 Tool까지 도출한다.

```
Pain (고통)
  ↓
Task (해결해야 할 과제)
  ↓
Skill (과제를 수행하는 능력)
  ↓
Tool (능력을 구현하는 도구)
```

**예시: 주간 보고서 작성이 너무 오래 걸린다**

```
Pain   → 매주 3시간을 보고서 작성에 낭비
Task   → 여러 시스템 데이터를 모아 요약본 작성
Skill  → 데이터 수집, 수치 해석, 문서 작성
Tool   → Jira API, DB 쿼리, LLM 요약, 슬랙 발송
```

**실습 시 이 프레임워크를 직접 작성해본다.**

---

### 2-3. 업무 유형별 Agent 패턴

Agent는 업무 특성에 따라 3가지 패턴으로 분류된다.

#### 자동화형 (Automation Agent)

**특징**: 정해진 프로세스를 자동 실행
**흐름**: 트리거 → 처리 → 결과 저장

```
예) 매일 오전 9시 → 전날 데이터 집계 → 리포트 생성 → 슬랙 전송
```

적합 조건:
- 반복 주기가 명확하다
- 처리 단계가 고정되어 있다
- 예외 처리보다 정상 흐름이 99%이다

---

#### 분석형 (Analysis Agent)

**특징**: 데이터를 탐색하고 인사이트 도출
**흐름**: 질문 수신 → 데이터 탐색 → 분석 → 결과 설명

```
예) "지난달 이탈 고객의 공통점은?" → DB 조회 → 패턴 분석 → 요약
```

적합 조건:
- 분석 범위가 사전에 고정되지 않는다
- 데이터 소스가 다양하다
- 결과를 자연어로 설명해야 한다

---

#### Planner형 (Planning Agent)

**특징**: 목표를 받아 스스로 계획을 세우고 실행
**흐름**: 목표 → 계획 수립 → 서브태스크 실행 → 결과 통합

```
예) "경쟁사 분석 보고서 만들어줘" → 검색 계획 → 수집 → 비교 → 작성
```

적합 조건:
- 목표가 추상적이고 실행 방법이 다양하다
- 실행 중 피드백을 반영해야 한다
- 실패 시 대안 경로가 필요하다

---

### 2-4. RAG vs Agent 판단 기준

가장 많이 혼동하는 질문: **"RAG로 할까, Agent로 할까?"**

| 기준 | RAG | Agent |
|------|-----|-------|
| 핵심 목적 | 지식 검색 + 생성 | 작업 수행 + 자동화 |
| 도구 사용 | 검색 도구 고정 | 다양한 도구 동적 선택 |
| 상태 관리 | Stateless 가능 | Stateful 필요한 경우 많음 |
| 복잡도 | 상대적으로 단순 | 복잡한 흐름 처리 |
| 적합 예시 | 사내 문서 Q&A | 이슈 자동 처리 |

**판단 질문**:

```
1. 단순히 "찾아서 대답"하면 되는가?  → RAG
2. 외부 시스템과 상호작용이 필요한가?  → Agent
3. 결과를 보고 다음 행동이 달라지는가? → Agent
4. 문서 기반 지식만 필요한가?          → RAG
```

> **실무 팁**: RAG와 Agent는 배타적이지 않다.
> Agent가 RAG를 도구로 사용하는 Hybrid 구조가 많다.

---

## 3. 실무 의미

### 문제 정의가 비용을 결정한다

잘못 정의된 문제에 Agent를 구축하면:
- 개발 비용 증가 (불필요한 복잡도)
- LLM 호출 비용 증가 (과도한 추론)
- 유지보수 어려움 (명확하지 않은 경계)

**좋은 문제 정의의 특징**:

```
✓ "무엇을 입력받아 무엇을 출력하는가" 명확
✓ 성공/실패 기준이 측정 가능
✓ 사람이 수동으로 하던 방식과 비교 가능
✓ 예외 케이스가 사전에 정의됨
```

---

## 4. 비교

### 자동화형 vs 분석형 vs Planner형

| 항목 | 자동화형 | 분석형 | Planner형 |
|------|----------|--------|-----------|
| 입력 | 이벤트/스케줄 | 자연어 질문 | 목표 설명 |
| 계획 | 고정 | 반고정 | 동적 |
| 도구 수 | 적음 (1-3개) | 중간 (3-5개) | 많음 (5개+) |
| 실패 처리 | 단순 재시도 | 대안 쿼리 | 계획 재수립 |
| 개발 난이도 | 낮음 | 중간 | 높음 |
| 비용 | 낮음 | 중간 | 높음 |

---

## 5. 주의사항

### Agent Anti-Pattern

**① 망치를 들면 모든 것이 못으로 보인다**
- LLM으로 할 수 있다고 해서 해야 하는 건 아니다
- 단순 규칙 기반이 더 빠르고 정확한 경우가 많다

**② 문제가 아닌 기술로 시작하는 설계**
- "Claude API를 써서 뭔가 만들자" → 실패 확률 높음
- "이 업무가 왜 힘든가?" → 올바른 출발점

**③ Edge Case 무시**
- Agent는 예외 상황에서 예상치 못한 행동을 한다
- 설계 단계에서 실패 케이스를 미리 나열하라

**④ 평가 기준 없는 배포**
- "잘 작동하는 것 같다"는 기준이 아니다
- 정량 지표를 먼저 정의하라: 정확도, 완료율, 평균 처리 시간

---

## 6. 코드 예제

### Pain → Task → Skill → Tool 정의 템플릿 (Python)

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class AgentSpec:
    """Agent 설계 명세서"""
    pain: str           # 현재의 고통/문제
    task: str           # Agent가 수행할 과제
    skills: List[str]   # 필요한 능력 목록
    tools: List[str]    # 구현에 필요한 도구 목록
    success_metric: str # 성공 기준
    failure_cases: List[str] = field(default_factory=list)

# 예시: 주간 보고서 자동화
weekly_report_agent = AgentSpec(
    pain="매주 3시간을 보고서 수동 작성에 낭비한다",
    task="여러 시스템 데이터를 수집하여 주간 요약 보고서를 자동 생성",
    skills=[
        "데이터 수집 및 집계",
        "수치 해석 및 트렌드 파악",
        "자연어 요약 작성",
        "슬랙 메시지 발송",
    ],
    tools=[
        "jira_api",      # 이슈 현황
        "db_query",      # 지표 데이터
        "llm_summarize", # 요약 생성
        "slack_send",    # 결과 전달
    ],
    success_metric="보고서 작성 시간 3h → 5분 이내 단축",
    failure_cases=[
        "Jira API 응답 없음 → 이전 데이터 사용 or 알림",
        "DB 타임아웃 → 재시도 3회 후 알림",
        "LLM 응답 품질 저하 → 사람 검토 플래그 설정",
    ]
)

# RAG vs Agent 판단 함수
def decide_architecture(spec: AgentSpec) -> str:
    """
    간단한 RAG vs Agent 판단 로직
    실제 프로젝트에서는 더 세밀한 기준을 사용한다.
    """
    needs_tools = len(spec.tools) > 1
    needs_external = any(
        t for t in spec.tools
        if t not in ["llm_summarize", "vector_search"]
    )

    if needs_tools and needs_external:
        return "Agent"
    elif "vector_search" in spec.tools:
        return "RAG"
    else:
        return "Simple LLM"

result = decide_architecture(weekly_report_agent)
print(f"권장 구조: {result}")  # → Agent
```

---

## Q&A

**Q. Agent와 RPA(Robotic Process Automation)의 차이는?**

> RPA는 정해진 UI 흐름을 반복 실행한다.
> Agent는 상황을 이해하고 유연하게 판단한다.
> RPA는 UI가 바뀌면 깨지지만, Agent는 목표 기반으로 대응한다.

**Q. Pain이 여러 개면 Agent도 여러 개 만들어야 하나?**

> 반드시 그렇지 않다.
> Pain들이 공통 Task로 묶이면 하나의 Agent로 처리 가능하다.
> 반대로 Pain이 하나여도 복잡하면 여러 Sub-agent로 분리할 수 있다.

**Q. Agent 적합성 판단 기준이 주관적이지 않나?**

> 맞다. 완전히 객관적인 기준은 없다.
> 하지만 "외부 시스템 상호작용 여부"와 "비결정적 흐름 여부"는 비교적 명확한 기준이 된다.

---

## 퀴즈

### Q1. Agent에 적합한 시나리오는?

다음 중 AI Agent를 적용하기 가장 적합한 시나리오는?

- A) 사내 FAQ 문서에서 질문에 대한 답변 찾기
- B) 고정된 HTML 템플릿에 데이터 채워 넣기
- C) 이슈 티켓을 분석하고 담당자 지정 후 알림 발송
- D) 주어진 텍스트를 영어에서 한국어로 번역

<details>
<summary>힌트</summary>
여러 시스템과의 상호작용이 필요하고, 상황에 따라 다음 행동이 달라지는 것을 찾아라.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: C**

- A → RAG가 적합 (문서 검색 + 답변)
- B → 단순 템플릿 엔진으로 충분
- C → Agent 적합: 이슈 분석(LLM) + 담당자 DB 조회(Tool) + 알림 발송(Tool)
- D → 단순 LLM 호출로 충분

</details>

---

### Q2. Pain → Task → Skill → Tool 순서

다음 빈칸을 올바르게 채워라.

```
Pain: 고객 문의 처리에 하루 4시간 소요
Task: ____
Skill: ____
Tool: ____
```

<details>
<summary>힌트</summary>
Task는 "무엇을 하는가", Skill은 "어떤 능력이 필요한가", Tool은 "무엇으로 구현하는가"를 답한다.
</details>

<details>
<summary>정답 예시</summary>

```
Task: 반복 문의를 자동 분류하고 표준 답변 생성 및 발송
Skill: 문의 분류, 유사 케이스 검색, 답변 생성, 고객 발송
Tool: 티켓 API, 벡터 DB(유사 문의 검색), LLM(답변), 이메일 API
```

정확히 일치하지 않아도 된다. Pain이 Task를 타당하게 설명하고, Tool이 Skill을 구현하면 정답이다.

</details>

---

### Q3. Agent 패턴 분류

다음 시나리오를 자동화형 / 분석형 / Planner형 중 하나로 분류하라.

> "사용자가 '우리 제품의 경쟁사 동향을 분석해줘'라고 입력하면, Agent가 검색 계획을 세우고 여러 소스를 탐색한 뒤 보고서를 작성한다."

<details>
<summary>힌트</summary>
목표가 추상적이고, 실행 방법을 Agent가 스스로 결정해야 하는가?
</details>

<details>
<summary>정답 및 해설</summary>

**정답: Planner형**

- 목표("경쟁사 동향 분석")가 추상적이다
- 실행 계획(어떤 소스를 어떤 순서로 탐색할지)을 Agent가 결정한다
- 탐색 결과에 따라 다음 행동이 달라진다

</details>

---

### Q4. RAG vs Agent 선택

다음 중 RAG가 Agent보다 더 적합한 경우는?

- A) 실시간 주가 데이터를 조회하여 포트폴리오 리밸런싱 제안
- B) 사내 기술 문서 2,000개 중에서 관련 내용을 찾아 답변
- C) 신규 버그 리포트를 분석하여 자동으로 GitHub 이슈 생성
- D) 여러 팀의 일정을 조율하여 최적 회의 시간 제안

<details>
<summary>힌트</summary>
외부 시스템 호출 없이 문서 검색만으로 해결되는 경우를 찾아라.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: B**

- A → 실시간 API 호출 필요 → Agent
- B → 문서 임베딩 + 벡터 검색 + 답변 생성 → RAG
- C → GitHub API 호출 필요 → Agent
- D → 캘린더 API 다중 호출 + 최적화 → Agent

</details>

---

### Q5. Agent Anti-Pattern

다음 중 Agent 설계의 Anti-Pattern에 해당하는 것은?

- A) 실패 케이스를 먼저 목록화하고 처리 방법을 정의한다
- B) "Claude API로 뭔가 자동화해보자"에서 시작한다
- C) 성공 기준을 정량 지표로 먼저 정의한다
- D) Pain을 정의하고 Task로 연결한다

<details>
<summary>힌트</summary>
문제가 아닌 기술에서 시작하는 것이 Anti-Pattern이다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: B**

기술(Claude API)에서 시작하면 문제를 기술에 맞추게 된다.
항상 Pain(고통)에서 시작해야 올바른 Agent 설계가 나온다.

- A, C, D → 모두 올바른 Agent 설계 방법론이다

</details>

---

## 실습 명세

### I DO (강사 시연, 15분)

**강사가 실시간으로 자신의 업무를 분석하여 AgentSpec을 작성한다.**

1. 강사의 실제 반복 업무 1개를 선택한다
2. Pain → Task → Skill → Tool 순서로 채워나간다
3. 자동화형 / 분석형 / Planner형 중 어떤 패턴인지 판단한다
4. RAG vs Agent 중 어떤 구조가 적합한지 설명한다

---

### WE DO (강사 + 수강생 함께, 20분)

**수강생이 자신의 업무 하나를 골라 AgentSpec 초안을 작성한다.**

진행 방식:
1. 강사가 Pain 질문을 유도한다: "어떤 업무가 가장 반복적인가?"
2. 수강생이 Pain을 작성한다 → 강사가 피드백
3. 함께 Task → Skill 도출한다
4. Tool 목록 작성 후 전체 공유

체크포인트:
- Pain이 구체적인가? ("힘들다"는 Pain이 아니다)
- Task가 측정 가능한 성공 기준을 포함하는가?

---

### YOU DO (수강생 독립 실습, 25분)

**개인 업무 기반으로 Agent 후보 2개를 도출하고 이유를 작성한다.**

제출물: `labs/agent-problem-definition/artifacts/` 폴더에 작성

요구사항:
- Agent 후보 2개 각각에 대해 AgentSpec 완성
- 각각에 대해 자동화형/분석형/Planner형 분류
- RAG vs Agent 선택 이유 1-2문장 작성
- 가장 큰 실패 케이스 2개 예상

모범 답안: `labs/agent-problem-definition/artifacts/example-spec.md` 참고
