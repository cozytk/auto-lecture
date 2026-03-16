# Session 1: Agent 문제 정의와 과제 도출 (2h)

## 학습 목표
1. AI Agent가 적합한 문제 유형과 부적합한 문제 유형을 구분할 수 있다
2. Pain - Task - Skill - Tool 프레임워크를 활용하여 업무를 체계적으로 분해할 수 있다
3. RAG와 Agent의 구조적 차이를 이해하고 상황에 맞는 아키텍처를 선택할 수 있다

---

## 개념 1: Agent가 적합한 문제 유형 정의

### 왜 이것이 중요한가

"AI Agent"라는 단어가 유행처럼 번지고 있다.
하지만 모든 문제에 Agent가 적합한 것은 아니다.

잘못 적용하면 단순 스크립트로 풀 수 있는 문제에 불필요한 복잡성이 추가된다.
2023~2024년 사이 많은 기업이 "Agent 도입"을 시도했지만 문제 유형을 잘못 판단해 실패했다.

> **Agent를 만들기 전에 먼저 물어야 할 질문:**
> "이 문제가 정말 Agent가 필요한가?"

---

### 핵심 원리

**전통적 자동화** (스크립트, ETL, 크론잡)
→ 사전 정의된 **고정 경로**를 실행
→ 입력이 같으면 **항상 같은 결과**

**AI Agent**
→ 중간 결과를 **관찰**하고, 다음 행동을 **동적으로 결정**
→ 이것이 **Observe → Think → Act 루프**

---

### Agent가 필요한 3가지 조건

**① 멀티스텝 (Multi-step)**
- 작업이 **2단계 이상**의 순차적 과정을 요구
- 단일 API 호출로 끝나는 작업 → **함수 하나로 충분**

**② 동적 판단 (Dynamic Decision)**
- 중간 결과에 따라 **다음 행동이 달라져야** 함
- 분기가 사전 고정 → `if-else`로 충분
- LLM이 상황을 판단해야 할 때 → **Agent 필요**

**③ 도구 활용 (Tool Usage)**
- 외부 API, DB, 파일 시스템과 상호작용
- LLM만으로는 실세계에 영향을 줄 수 없다

---

### 실무에서의 의미

현업에서 Agent 도입 시 흔한 실수 두 가지:
- 단순 자동화를 Agent로 **과잉 설계** → 비용·지연 증가
- 복잡한 업무를 **단순 스크립트로 억지 구현** → 스파게티 코드

올바른 판단 기준을 갖추면 엔지니어링 리소스를 가장 가치 있는 곳에 집중할 수 있다.

---

### 다른 접근법과의 비교

| 구분 | RPA | AI Agent |
|------|-----|----------|
| 동작 방식 | UI 수준 클릭/입력 재현 | API 수준 동적 판단 |
| 판단 능력 | 고정 규칙 의존 | LLM 기반 유연한 판단 |
| UI 변경 시 | 즉시 깨짐 | 영향 없음 |
| 비용 | LLM 호출 없음 | LLM 호출 비용 발생 |

---

### 주의사항

> **LLM 호출 비용과 지연이 발생한다.**
> 비용 대비 효과를 반드시 따져야 한다.
> ETL 파이프라인처럼 흐름이 고정된 작업은 Airflow가 적합하다.

---

### 코드 예제

이를 코드로 표현하면:

```python
# 단순 자동화: 고정된 흐름, 판단 없음
def simple_automation(data):
    cleaned = clean_data(data)
    result = transform(cleaned)
    save(result)
    return result

# Agent: 상황에 따라 판단하고 경로를 선택
def agent_workflow(task):
    plan = llm.think(f"이 작업을 어떻게 처리할까? {task}")

    while not plan.is_complete():
        next_step = plan.get_next_step()

        if next_step.needs_data():
            data = tool_call("search", next_step.query)
            plan.update_context(data)
        elif next_step.needs_action():
            result = tool_call(next_step.tool, next_step.params)
            plan.evaluate_result(result)
        elif next_step.needs_human():
            feedback = request_human_input(next_step.question)
            plan.incorporate_feedback(feedback)

    return plan.final_output()
```

**Agent가 적합한 문제:**

| 조건 | 설명 | 예시 |
|------|------|------|
| 멀티스텝 | 2단계 이상의 순차적 작업 | 데이터 수집 → 분석 → 보고서 생성 |
| 동적 판단 | 중간 결과에 따라 다음 행동이 달라짐 | 에러 유형에 따라 다른 해결책 적용 |
| 도구 활용 | 외부 API, DB, 파일 등과 상호작용 | Slack 읽기 → Jira 티켓 생성 |

```python
# 부적합 1: 단순 변환 (판단 불필요)
def format_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%m/%d/%Y")

# 부적합 2: 단일 질의응답 (멀티스텝 불필요)
def simple_qa(question):
    return llm.chat(question)

# 부적합 3: 실시간 제어 (지연 허용 불가)
def real_time_control(sensor_data):
    if sensor_data.temperature > 100:
        return emergency_shutdown()
```

---

### Q&A

**Q: RPA와 AI Agent의 차이는 무엇인가요?**
A: RPA는 사전 정의된 고정 규칙을 따라 UI를 조작한다.
AI Agent는 LLM 기반으로 **상황에 따라 판단을 변경**한다.
RPA는 "이메일에서 날짜를 추출하여 등록"이라는 고정 흐름을 실행한다.
Agent는 "이 이메일은 일정 변경 요청이니 기존 일정을 수정하자"는 동적 판단이 가능하다.

**Q: 모든 멀티스텝 작업에 Agent를 쓰는 게 좋은가요?**
A: 아니다. 분기 조건이 고정되어 있다면 스크립트가 더 효율적이다.
Agent는 LLM 호출 비용이 발생한다.
"판단이 필요한 분기"가 없다면 오버엔지니어링이다.

<details>
<summary>퀴즈: 다음 중 AI Agent가 가장 적합한 업무는?</summary>

**보기:**
1. CSV 파일 1000개의 컬럼명을 일괄 변경
2. 고객 리뷰를 분석하여 제품별 개선점을 도출하고 Jira 티켓 생성
3. 사내 위키에서 특정 키워드로 문서 검색
4. 매일 9시에 서버 상태를 Slack으로 알림

**힌트**: Agent의 3가지 조건(멀티스텝, 동적 판단, 도구 활용)을 모두 만족하는 것을 찾아보자.

**정답**: 2번. 리뷰 분석(판단) → 개선점 도출(멀티스텝) → Jira API 호출(도구 활용)을 모두 포함한다.
1번은 스크립트, 3번은 RAG, 4번은 크론잡+스크립트로 충분하다.
</details>

---

## 개념 2: Pain - Task - Skill - Tool 프레임워크

### 왜 이것이 중요한가

Agent 설계 시 가장 흔한 실수: **도구(Tool)부터 정하고 문제를 끼워 맞추는 것**

"GPT-4 API가 있으니까 뭔가를 만들어보자"는 접근이 대표적이다.
이 방식은 실제 비즈니스 가치 없이 기술 데모로 끝난다.

McKinsey 2024년 보고서: AI 프로젝트의 70%가 PoC를 넘기지 못한다.
주요 원인 중 하나: **기술 중심 접근**

> 올바른 순서는 **Pain(고통)에서 출발**하여 Tool로 구체화하는 Top-Down 접근이다.

---

### 핵심 원리

**Pain → Task → Skill → Tool** 4단계 설계 방법론.
각 단계는 이전 단계의 "왜?"에 대한 답을 제공한다.

**Pain (고통점)**
→ 수치로 측정 가능한 비효율
→ "불편하다" ❌ / "주당 5시간 소비" ✅

**Task (작업)**
→ Pain에서 반복되는 동사를 추출
→ "수집한다", "분류한다", "작성한다" 각각이 Task

**Skill (능력)**
→ Task를 수행하기 위해 Agent가 갖춰야 할 능력
→ 과도한 기능 추가(feature creep)를 방지

**Tool (도구)**
→ Skill을 실현하는 구체적 기술 구현체
→ LLM API, Vector DB, Slack API 등
→ 항상 **교체 가능**해야 함

---

### 실무에서의 의미

이 프레임워크의 가장 큰 가치: **이해관계자 소통**

개발팀은 Tool 수준에서, 비즈니스팀은 Pain 수준에서 대화한다.
이 프레임워크 없이는 기술 논쟁에 빠져 본질적 질문을 놓친다.

> **Pain에서 시작하면** 비즈니스 가치를 먼저 검증한 후 최적의 기술을 선택할 수 있다.

---

### 다른 접근법과의 비교

| 구분 | Pain-first (Top-Down) | Tool-first (Bottom-Up) |
|------|----------------------|----------------------|
| 시작점 | 비즈니스 고통 | 보유 기술/도구 |
| 결과 | 가치 검증 후 기술 선택 | 기술에 맞는 문제 탐색 |
| 적합 환경 | 프로덕션 개발 | 해커톤, 빠른 프로토타이핑 |
| 함정 | 없음 | "망치를 들면 모든 것이 못으로 보인다" |

---

### 주의사항

> **Tool-first 접근은 "망치를 들면 모든 것이 못으로 보인다" 함정에 빠진다.**
> "Vector DB가 있으니 RAG를 쓰자"로 시작하면
> RAG가 필요 없는 문제에도 RAG를 적용하게 된다.

---

### 코드 예제

이를 코드로 표현하면:

```python
framework = {
    "Pain": {
        "정의": "현재 업무에서 반복적으로 발생하는 비효율/고통",
        "질문": "무엇이 가장 시간을 많이 잡아먹는가?",
        "예시": "신규 입사자 온보딩에 매번 2시간씩 같은 설명을 반복한다",
    },
    "Task": {
        "정의": "Pain을 해결하기 위한 구체적 작업 단위",
        "질문": "그 고통을 없애려면 어떤 작업이 필요한가?",
        "예시": "입사자 질문에 자동 답변 + 필요 문서 전달 + 진행상황 추적",
    },
    "Skill": {
        "정의": "Task를 수행하기 위해 Agent가 갖춰야 할 능력",
        "질문": "그 작업을 하려면 어떤 능력이 필요한가?",
        "예시": "자연어 이해, 문서 검색, 대화 맥락 유지, 업무 시스템 조작",
    },
    "Tool": {
        "정의": "Skill을 실현하는 구체적 기술 구현체",
        "질문": "그 능력을 어떤 도구로 구현할 수 있는가?",
        "예시": "LLM API, Vector DB(RAG), Slack API, Notion API",
    },
}
```

실행 결과:

```
Pain (비즈니스 고통점)
  └→ Task (해결해야 할 구체적 작업)
       └→ Skill (작업 수행에 필요한 능력)
            └→ Tool (능력을 구현하는 도구)
```

---

### Q&A

**Q: Pain이 여러 개면 Agent도 여러 개 만들어야 하나요?**
A: 반드시 그렇지는 않다.
Pain들이 서로 관련된 업무 영역이면 하나의 Agent가 해결 가능하다.
연관성이 없다면 별도 Agent로 분리하는 것이 유지보수에 유리하다.

> **원칙: "하나의 Agent는 하나의 역할(Role)에 집중"**

**Q: Tool을 먼저 정하고 역으로 Pain을 찾는 방식은 왜 안 되나요?**
A: Tool-first 접근은 "망치를 들면 모든 것이 못으로 보인다" 함정에 빠진다.
Pain-first로 접근해야 실제 비즈니스 가치를 검증한 후 최적의 Tool을 선택할 수 있다.

<details>
<summary>퀴즈: 다음 Pain에서 Task를 도출해보자</summary>

**Pain**: "매주 금요일 주간 보고서를 작성하는데 3시간이 걸린다.
Jira 티켓 정리, Git 커밋 요약, Slack 논의 정리를 수동으로 한다."

**힌트**: Pain에서 반복되는 구체적 행동(동사)을 추출하면 Task가 된다.

**정답**:
- Task 1: Jira에서 이번 주 완료/진행 중 티켓 수집 및 분류
- Task 2: Git 저장소에서 이번 주 커밋 내역 수집 및 요약
- Task 3: Slack 채널에서 주요 논의 내용 추출
- Task 4: 수집된 정보를 주간 보고서 템플릿에 맞게 종합 작성

각 Task에 필요한 Skill: API 호출(Jira, Git, Slack), 정보 요약(LLM), 문서 생성(LLM)
</details>

---

## 개념 3: 업무 유형별 Agent 패턴

### 왜 이것이 중요한가

Agent를 백지 상태에서 시작하면 시행착오가 크다.
반복적으로 등장하는 패턴을 알면 설계를 가속할 수 있다.

> 디자인 패턴이 소프트웨어 설계를 가속하듯,
> **Agent 패턴은 Agent 설계를 가속한다.**

---

### 핵심 원리

Agent는 해결하는 문제의 특성에 따라 3가지 패턴으로 분류된다.

**자동화형 (Executor)**
→ 외부 이벤트(트리거)를 받아 일련의 작업을 자동 실행
→ 핵심 가치: "사람이 반복적으로 수행하던 업무를 대신 실행"
→ 설계 핵심: Tool 호출의 안정성과 에러 복구

**분석형 (Analyst)**
→ 여러 소스에서 데이터를 수집하고 인사이트 도출
→ 핵심 가치: "수 시간 걸리는 데이터 분석을 자동화"
→ 설계 핵심: 데이터 수집의 완전성과 분석의 정확성

**계획형 (Planner)**
→ 복잡한 목표를 서브태스크로 분해하고 실행 계획 수립
→ 핵심 가치: "복잡한 프로젝트의 계획과 추적을 자동화"
→ 설계 핵심: 목표 분해의 품질과 재계획(re-planning) 능력

---

### 실무에서의 의미

현업의 대부분 Agent: 하나의 주 패턴에 보조 패턴이 결합된 복합 형태다.

주 패턴을 먼저 정하고 필요한 보조 패턴을 추가하면 복잡도를 관리할 수 있다.
처음부터 "만능 Agent"를 만들려 하면 어느 패턴에서도 품질을 보장하기 어렵다.

---

### 다른 접근법과의 비교

| Agent 패턴 | 전통 소프트웨어 대응 | Agent의 차이점 |
|------------|-------------------|--------------|
| 자동화형 | 메시지 큐 기반 Worker | LLM 기반 유연한 판단 |
| 분석형 | ETL/ELT 파이프라인 | 비결정적 분석 가능 |
| 계획형 | Airflow, Temporal | 동적 재계획 능력 |

---

### 주의사항

> **비결정성(non-determinism)이 증가한다.**
> LLM 기반 판단은 테스트와 모니터링 전략이 달라져야 한다.

---

### 코드 예제

이를 코드로 표현하면:

```python
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, llm, tools: list):
        self.llm = llm
        self.tools = {t.name: t for t in tools}

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        pass

class ExecutorAgent(BaseAgent):
    """자동화형: 트리거 → 판단 → 실행"""
    def run(self, input_data: dict) -> dict:
        classification = self.llm.classify(input_data["event"])
        workflow = self.select_workflow(classification)
        results = []
        for step in workflow.steps:
            tool = self.tools[step.tool_name]
            result = tool.execute(step.params)
            results.append(result)
            if not self.llm.should_continue(results):
                break
        return {"status": "completed", "results": results}

class AnalystAgent(BaseAgent):
    """분석형: 수집 → 분석 → 보고"""
    def run(self, input_data: dict) -> dict:
        raw_data = self.collect_data(input_data["sources"])
        analysis = self.llm.analyze(raw_data, input_data["question"])
        report = self.llm.generate_report(analysis)
        return {"report": report, "insights": analysis.key_findings}

class PlannerAgent(BaseAgent):
    """계획형: 목표 분해 → 계획 → 실행 → 재계획"""
    def run(self, input_data: dict) -> dict:
        goal = input_data["goal"]
        plan = self.llm.decompose(goal)
        for task in plan.tasks:
            result = self.execute_task(task)
            if result.failed:
                plan = self.llm.replan(plan, task, result.error)
        return {"plan": plan, "status": plan.overall_status}
```

---

### Q&A

**Q: 우리 업무에 어떤 패턴이 맞는지 어떻게 판단하나요?**
A: 핵심 질문을 던져보자.
(1) "Agent가 주로 **실행**하는가, **분석**하는가, **계획**하는가?"
(2) "최종 산출물이 **행동의 결과**인가, **보고서**인가, **실행 계획**인가?"

**Q: 분석형 Agent와 RAG의 차이는 무엇인가요?**
A: RAG는 "질문에 대한 정보 검색 및 답변 생성"에 집중하는 단일 패턴이다.
분석형 Agent는 RAG를 **내부 도구로 활용**하면서 데이터 가공, 다단계 추론, 보고서 생성 등 복합 작업을 수행한다.

<details>
<summary>퀴즈: 다음 시나리오는 어떤 Agent 패턴에 해당하는가?</summary>

**시나리오**: "사용자가 '다음 주 화요일에 팀 회의를 잡아줘'라고 말하면,
참석자들의 캘린더를 확인하고, 가능한 시간대를 찾아 회의를 생성하고,
참석자들에게 알림을 보낸다."

**힌트**: Agent가 주로 하는 일이 '실행'인지, '분석'인지, '계획'인지 생각해보자.

**정답**: **자동화형(Executor)**이 주 패턴이다.
트리거(사용자 요청) → 판단(시간대 확인) → 실행(회의 생성, 알림 전송) 흐름이다.
일부 Planner 요소(최적 시간 결정)가 보조적으로 포함된다.
핵심 가치는 "자동 실행"에 있다.
</details>

---

## 개념 4: RAG vs Agent 판단 기준

### 왜 이것이 중요한가

실무에서 가장 자주 발생하는 아키텍처 의사결정: **"RAG로 충분한가, Agent가 필요한가"**

잘못 판단하면 두 방향으로 실패한다.
- RAG로 충분한 문제에 Agent 적용 → 복잡도·비용·지연 증가
- Agent가 필요한 문제에 RAG만 적용 → "검색은 잘 되는데 문제를 해결해주지 않는다"

> 2024년 기준 많은 기업의 AI 챗봇이 후자의 함정에 빠져 있다.
> "알려주는 것 말고, 직접 처리해줬으면 좋겠다."

---

### 핵심 원리

RAG vs Agent 판단은 5가지 축으로 체계화할 수 있다.

**① 상호작용 방식**
→ RAG: 단일 질의-응답(1-turn)에 최적화
→ Agent: 멀티턴 대화와 중간 행동을 포함한 복합 상호작용

**② 외부 시스템 연동**
→ RAG: 본질적으로 **읽기 전용**
→ Agent: **읽기 + 쓰기** 가능 (API 호출로 티켓 생성, 이메일 발송 등)

> **핵심 차이: "쓰기 능력"의 유무**

**③ 판단의 복잡도**
→ RAG: 유사도 기반 검색 ("어떤 문서가 관련 있는가?")
→ Agent: 조건부 분기와 다단계 추론 ("어떤 행동을 해야 하는가?")

**④ 상태 관리**
→ RAG: 기본적으로 Stateless (각 질의가 독립적)
→ Agent: Stateful 동작 (이전 결과가 다음 행동에 영향)

**⑤ 실패 처리**
→ RAG: "정보를 찾을 수 없습니다"로 응답
→ Agent: 대안 전략 시도 → 재시도 → 에스컬레이션

---

### 실무에서의 의미

**점진적 전환**이 가장 현실적인 접근이다.

1. 먼저 RAG로 정보 검색과 답변 기능을 구축
2. 운영하며 "이걸 자동으로 해줬으면 좋겠다"는 요구 수집
3. RAG를 Agent의 하나의 Tool로 통합

→ 리스크 최소화 + 빠른 가치 검증

---

### 다른 접근법과의 비교

| 구분 | Basic RAG | Conversational RAG | Agentic RAG | Agent |
|------|-----------|-------------------|-------------|-------|
| 대화 맥락 | ❌ | ✅ | ✅ | ✅ |
| 쓰기 작업 | ❌ | ❌ | ❌ | ✅ |
| 검색 재작성 | ❌ | ❌ | ✅ | ✅ |
| 복잡도 | 낮음 | 중간 | 중간 | 높음 |

---

### 주의사항

> **RAG로 충분한 문제에 Agent를 적용하면:**
> - LLM 호출 3-4회 (계획 → 검색 → 판단 → 응답)
> - 응답 시간 5-10초
> - 비용 10배 증가

---

### 코드 예제

이를 코드로 표현하면:

```python
def decide_architecture(requirements: dict) -> str:
    """아키텍처 의사결정 트리"""
    if requirements.get("needs_action"):
        if requirements.get("knowledge_base"):
            return "Hybrid (Agent + RAG)"
        return "Agent"

    if requirements.get("multi_step") and requirements.get("dynamic_routing"):
        return "Agent"

    if requirements.get("knowledge_base"):
        if requirements.get("needs_context"):
            return "Conversational RAG"
        return "Basic RAG"

    return "Simple LLM Call"
```

실행 결과:

```
사내 규정 질의응답: → Basic RAG
고객 주문 처리 자동화: → Agent
기술 문서 기반 장애 진단: → Hybrid (Agent + RAG)
제품 설명 생성: → Simple LLM Call
```

---

### Q&A

**Q: Conversational RAG와 Agent의 경계가 모호한데, 어디서 선을 그어야 하나요?**
A: 핵심 기준은 **"외부 시스템에 쓰기 작업을 수행하는가"**이다.
Conversational RAG: 대화 맥락을 유지하며 문서를 검색하고 답변 (모든 작업이 "읽기")
Agent: 검색 결과를 바탕으로 Jira 티켓 생성, 이메일 발송 등 **쓰기 작업(side effect)** 수행
쓰기 작업이 필요한 순간이 Agent 도입 시점이다.

**Q: 처음에 RAG로 시작해서 나중에 Agent로 전환할 수 있나요?**
A: 그렇다. 이것이 권장되는 점진적 접근법이다.
(1) RAG로 정보 검색/답변 기능을 구축
(2) "이걸 자동으로 해줬으면 좋겠다"는 요구가 나오면
(3) RAG를 Agent의 하나의 Tool로 포함시키고 실행 기능을 추가한다.

<details>
<summary>퀴즈: 다음 요구사항에 적합한 아키텍처는?</summary>

**요구사항**: "개발팀에서 코드를 PR로 올리면, 관련 설계 문서를 찾아서 설계 의도와 구현이 일치하는지 분석하고, 불일치하는 부분에 대해 자동으로 리뷰 코멘트를 작성한다."

**힌트**: 이 시스템이 필요로 하는 기능을 나열해보자.
(1) 문서 검색, (2) 코드-문서 비교 분석, (3) 코멘트 작성(쓰기)

**정답**: **Hybrid (Agent + RAG)**
설계 문서 검색에는 RAG가 필요하다.
PR 코드 분석 + 리뷰 코멘트 작성(GitHub API 호출)에는 Agent가 필요하다.
RAG를 Agent의 Tool로 통합하는 Hybrid 구조가 적합하다.
</details>

---

## 실습

### 실습 1: 개인 업무 기반 Agent 후보 도출

- **연관 학습 목표**: 학습 목표 1, 2
- **실습 목적**: Pain-Task-Skill-Tool 프레임워크를 활용하여 실제 업무에서 Agent 후보를 도출한다
- **실습 유형**: 분석
- **난이도**: 기초
- **예상 소요 시간**: 30분 (I DO 5분 / WE DO 10분 / YOU DO 15분)
- **선행 조건**: 없음
- **실행 환경**: 로컬 (문서 작성)

**I DO**: 강사가 자신의 업무 중 "주간 보고서 작성"을 Pain으로 선택하고, Task-Skill-Tool로 분해하는 과정을 시연한다.

**WE DO**: 함께 "고객 문의 분류 및 답변" 업무를 Pain-Task-Skill-Tool로 분해한다. 각 단계마다 멈추고 질문을 받는다.

**YOU DO**:
본인의 현재 업무에서 가장 시간이 많이 소요되는 반복 작업 3개를 나열하고, 각 작업에 대해 아래 템플릿을 작성한다.

```python
agent_candidate = {
    "pain": "여기에 구체적인 고통점 작성",
    "frequency": "일 N회 / 주 N회",
    "time_spent": "회당 N분",
    "tasks": [
        "Task 1: ...",
        "Task 2: ...",
    ],
    "skills": {
        "Task 1": ["필요한 능력 1", "필요한 능력 2"],
        "Task 2": ["필요한 능력 1"],
    },
    "tools": {
        "능력 1": ["구체적 도구/API"],
        "능력 2": ["구체적 도구/API"],
    },
    "agent_suitability": {
        "multi_step": True,
        "dynamic_decision": True,
        "tool_usage": True,
        "verdict": "Agent 적합 / RAG 적합 / 스크립트 적합",
    },
}
```

3개 후보 중 Agent에 가장 적합한 2개를 선정하고 선정 이유를 작성한다.

**정답 예시**:
```python
# 주간 보고서 자동화 예시
agent_candidate = {
    "pain": "매주 금요일 주간 보고서 작성에 3시간 소요",
    "frequency": "주 1회",
    "time_spent": "180분",
    "tasks": [
        "Task 1: Jira에서 완료/진행 중 티켓 수집",
        "Task 2: Git 커밋 내역 수집 및 요약",
        "Task 3: Slack 주요 논의 추출",
        "Task 4: 보고서 템플릿에 맞게 종합",
    ],
    "skills": {
        "Task 1": ["Jira API 호출", "데이터 분류"],
        "Task 2": ["Git API 호출", "텍스트 요약"],
        "Task 3": ["Slack API 호출", "정보 추출"],
        "Task 4": ["정보 통합", "문서 생성"],
    },
    "tools": {
        "Jira API 호출": ["Jira REST API"],
        "텍스트 요약": ["LLM API"],
        "문서 생성": ["Confluence API"],
    },
    "agent_suitability": {
        "multi_step": True,
        "dynamic_decision": True,
        "tool_usage": True,
        "verdict": "Agent 적합",
    },
}
```

---

### 실습 2: RAG vs Agent 구조 선택 이유 작성

- **연관 학습 목표**: 학습 목표 3
- **실습 목적**: 아키텍처 의사결정 트리를 적용하여 구조 선택을 논리적으로 정당화한다
- **실습 유형**: 분석
- **난이도**: 중급
- **예상 소요 시간**: 30분 (I DO 5분 / WE DO 10분 / YOU DO 15분)
- **선행 조건**: 실습 1 완료
- **실행 환경**: 로컬 (문서 작성 + Python 코드 실행)

**I DO**: 강사가 "사내 FAQ 챗봇" 요구사항에 의사결정 트리를 적용하여 Basic RAG를 선택하는 과정을 시연한다.

**WE DO**: "고객 주문 처리 자동화" 시나리오를 함께 분석한다. 5가지 축(상호작용, 쓰기, 판단 복잡도, 상태, 실패처리)을 하나씩 체크한다.

**YOU DO**:
실습 1에서 선정한 2개 Agent 후보 각각에 대해 의사결정 트리를 적용한다.

```python
architecture_decision = {
    "candidate_name": "후보 이름",
    "requirements": {
        "needs_action": True,
        "multi_step": True,
        "needs_context": True,
        "knowledge_base": False,
        "dynamic_routing": True,
    },
    "decision": "Agent / RAG / Hybrid",
    "reasoning": [
        "이유 1: ...",
        "이유 2: ...",
        "이유 3: ...",
    ],
    "alternative_considered": "대안으로 고려한 아키텍처와 배제 이유",
}
```

**정답 예시**:
```python
architecture_decision = {
    "candidate_name": "주간 보고서 자동화",
    "requirements": {
        "needs_action": True,   # Jira, Slack, Git API 쓰기
        "multi_step": True,     # 수집 → 분석 → 작성 3단계
        "needs_context": False,
        "knowledge_base": False,
        "dynamic_routing": True, # 각 소스별 다른 처리
    },
    "decision": "Agent",
    "reasoning": [
        "이유 1: 외부 시스템(Jira, Git, Slack, Confluence) 쓰기 작업 필요",
        "이유 2: 4개 Task가 순차적으로 연결되는 멀티스텝 작업",
        "이유 3: 각 소스의 데이터에 따라 다른 처리가 필요한 동적 판단",
    ],
    "alternative_considered": "RAG 배제 - 정보 검색만 하는 것이 아니라 외부 API에 쓰기 작업이 필요하기 때문",
}
```

---

### 실습 3: 업무 유형별 Agent 패턴 매핑

- **연관 학습 목표**: 학습 목표 1, 2, 3
- **실습 목적**: 실제 업무 시나리오를 Agent 패턴(자동화형/분석형/계획형)에 매핑하고 아키텍처 스케치를 그린다
- **실습 유형**: 분석 + 설계
- **난이도**: 중급
- **예상 소요 시간**: 25분 (I DO 5분 / WE DO 8분 / YOU DO 12분)
- **선행 조건**: 실습 1, 2 완료
- **실행 환경**: 로컬 (문서 작성)

**I DO**: 강사가 "코드 리뷰 Agent"를 예시로 복합 패턴(Planner + Analyst + Executor)을 설명하고 워크플로우 다이어그램을 그린다.

**WE DO**: "DevOps 장애 대응 자동화"를 함께 분석한다. 주 패턴과 보조 패턴을 함께 도출한다.

**YOU DO**:
실습 1에서 선정한 Agent 후보 2개 각각에 대해 패턴을 판별하고 워크플로우를 그린다.

```python
pattern_analysis = {
    "candidate_name": "후보 이름",
    "primary_pattern": "자동화형 / 분석형 / 계획형",
    "secondary_pattern": "없음 또는 보조 패턴",
    "justification": {
        "주 패턴 선택 이유": "...",
        "보조 패턴 필요 이유": "...",
    },
    "workflow_sketch": [
        "Step 1: (입력) → ...",
        "Step 2: (판단) → ...",
        "Step 3: (실행) → ...",
        "Step 4: (출력) → ...",
    ],
}
```

**정답 예시**:
```python
pattern_analysis = {
    "candidate_name": "주간 보고서 자동화",
    "primary_pattern": "자동화형",
    "secondary_pattern": "분석형 (각 소스 데이터 요약)",
    "justification": {
        "주 패턴 선택 이유": "트리거(금요일 스케줄) → 판단 없이 고정 흐름으로 실행",
        "보조 패턴 필요 이유": "Git 커밋, Slack 논의 요약 시 LLM 분석 필요",
    },
    "workflow_sketch": [
        "Step 1: (트리거) 금요일 9시 스케줄 → 실행 시작",
        "Step 2: (수집) Jira API + Git API + Slack API 병렬 호출",
        "Step 3: (분석) LLM으로 각 소스 데이터 요약",
        "Step 4: (출력) 보고서 템플릿에 종합 → Confluence 저장",
    ],
}
```

---

## 핵심 정리
- AI Agent는 **멀티스텝 + 동적 판단 + 도구 활용** 3가지 조건을 만족하는 문제에 적합하다
- Agent 설계는 **Pain → Task → Skill → Tool** 순서로 Top-Down 접근한다 (Tool-first는 함정)
- Agent 패턴은 **자동화형, 분석형, 계획형** 3가지이며, 실무에서는 복합 패턴이 일반적이다
- RAG vs Agent 판단의 핵심 기준은 **외부 시스템에 대한 쓰기(side effect) 필요 여부**다
- 점진적 접근법이 유효하다: **RAG → Conversational RAG → Agent(RAG as Tool)**
