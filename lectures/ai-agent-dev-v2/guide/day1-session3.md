# Day 1 - Session 3: Agent 기획서 구조화

**시간**: 2시간 | **대상**: AI 개발자, 데이터 엔지니어, 기술 리더

---

## 1. 왜 중요한가

### 기획 없는 Agent는 방향 없는 자동화다

코드를 먼저 짜고 싶은 충동이 있다.
하지만 명확하지 않은 Agent는 개발 중반에 방향을 잃는다.
**구조화된 기획서가 개발 속도와 품질을 동시에 높인다.**

> "어디서 시작해서 어디서 끝나는지" 모르면
> 테스트도 못하고 예외 처리도 할 수 없다.

**이 세션에서 배우는 것**:
- Task → Sub-task → Workflow 분해 방법
- Stateless vs Stateful 구조의 차이와 선택
- Input–Process–Output 명확화
- 예외 처리 및 실패 케이스 전략

---

## 2. 핵심 원리

### 2-1. Task → Sub-task → Workflow 분해

복잡한 Agent는 하나의 거대한 프롬프트로 구현할 수 없다.
**Task를 작은 Sub-task로 분해하고, 연결 순서를 Workflow로 정의한다.**

#### 분해 원칙

```
하나의 Sub-task는 하나의 책임만 가진다.
Sub-task는 독립적으로 테스트 가능해야 한다.
Sub-task 출력이 다음 Sub-task 입력이 된다.
```

#### 분해 예시: 주간 보고서 Agent

```
Task: 주간 보고서 자동 생성

Sub-task 분해:
├── ST-1: 데이터 수집
│   ├── Jira 이슈 현황 가져오기
│   ├── DB 지표 쿼리
│   └── 슬랙 주요 메시지 수집
│
├── ST-2: 데이터 정제 및 구조화
│   ├── 원시 데이터 → 표준 포맷 변환
│   └── 이상치 및 누락 값 처리
│
├── ST-3: 요약 생성
│   ├── 지표 트렌드 분석
│   └── 자연어 요약 작성 (LLM)
│
└── ST-4: 배포
    ├── 슬랙 채널 발송
    └── 이메일 발송

Workflow: ST-1 → ST-2 → ST-3 → ST-4
```

#### Workflow 다이어그램 작성

```
[트리거: 월요일 오전 9시]
         ↓
[ST-1: 데이터 수집]
         ↓
     수집 성공?
    ↙         ↘
  Yes           No
   ↓             ↓
[ST-2: 정제]  [에러 알림]
   ↓             ↓
[ST-3: 요약]  [종료]
   ↓
[ST-4: 배포]
   ↓
[완료 로그]
```

---

### 2-2. Stateless vs Stateful 구조

Agent 설계의 중요한 선택: **상태를 어디에 저장하는가?**

#### Stateless (상태 없음)

각 호출이 독립적이다. 이전 실행을 기억하지 않는다.

```python
# Stateless Agent 예시
def classify_ticket(ticket_content: str) -> dict:
    """
    호출할 때마다 독립적으로 분류.
    이전 분류 결과를 참조하지 않는다.
    """
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=128,
        messages=[{
            "role": "user",
            "content": f"티켓 분류: {ticket_content}"
        }]
    )
    return parse_result(response)
```

**장점**:
- 구현이 단순하다
- 수평 확장이 쉽다 (여러 인스턴스 동시 실행)
- 실패 시 재시도가 안전하다

**적합**:
- 단발성 처리 (티켓 분류, 번역)
- 독립적인 배치 작업
- 이전 결과가 다음에 영향 없는 경우

---

#### Stateful (상태 있음)

이전 실행 결과를 기억하고 다음 실행에 활용한다.

```python
# Stateful Agent 예시
class ResearchAgent:
    def __init__(self):
        self.memory = []          # 수집한 정보
        self.visited_urls = set() # 방문한 URL
        self.findings = []        # 발견한 인사이트

    def search(self, query: str) -> str:
        # 이전 findings를 Context에 포함
        context = "\n".join(self.findings[-5:])  # 최근 5개

        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            system=f"지금까지 발견한 내용:\n{context}",
            messages=[{"role": "user", "content": f"검색: {query}"}]
        )

        result = response.content[0].text
        self.findings.append(result)  # 상태 업데이트
        return result
```

**장점**:
- 긴 작업을 단계적으로 처리 가능
- 이전 결과를 기반으로 다음 행동 결정
- 대화형 상호작용 지원

**적합**:
- 다단계 리서치
- 대화형 Assistant
- 장기 프로젝트 관리

---

#### 선택 기준

```
이전 실행 결과가 다음 실행에 필요한가?
  → Yes: Stateful
  → No: Stateless

동시에 여러 인스턴스를 실행해야 하는가?
  → Yes: Stateless 선호
  → No: 상관없음

실행 중간에 사람이 개입할 수 있는가?
  → Yes: Stateful (중간 상태 저장 필요)
  → No: 상관없음
```

---

### 2-3. Input–Process–Output 명확화

모든 Sub-task는 I/O가 명확해야 한다.
명확하지 않으면 테스트할 수 없다.

#### IPO 템플릿

```
Sub-task 이름: [명확한 동사 + 명사]
─────────────────────────────────────
INPUT
  - 타입: [dict / str / list / ...]
  - 필수 필드: [필드명: 타입, 설명]
  - 옵션 필드: [필드명: 타입, 기본값]
  - 예시:
    {
      "ticket_id": "PROJ-123",
      "content": "로그인 버튼이 클릭되지 않음",
      "priority": "high"
    }

PROCESS
  - 처리 단계: [번호로 나열]
  - 사용 도구: [LLM / API / DB / ...]
  - 판단 로직: [분기 조건]

OUTPUT
  - 타입: [dict / str / list / ...]
  - 필드: [필드명: 타입, 설명]
  - 예시:
    {
      "category": "bug",
      "severity": 3,
      "assignee": "backend-team",
      "reason": "UI 인터랙션 오류"
    }
─────────────────────────────────────
예외 케이스:
  - content가 비어있으면 → 에러 반환
  - category 분류 불가 → "unclassified" 반환
```

#### 실무 예시: 이슈 분류 Sub-task

```python
from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class TicketInput:
    """이슈 분류 Sub-task 입력"""
    ticket_id: str
    content: str
    priority: Literal["low", "medium", "high"] = "medium"

@dataclass
class TicketOutput:
    """이슈 분류 Sub-task 출력"""
    category: Literal["bug", "feature", "question", "unclassified"]
    severity: int  # 1-5
    assignee: str
    reason: str
    confidence: float  # 0.0-1.0

def classify_ticket(input: TicketInput) -> TicketOutput:
    """
    INPUT: TicketInput (ticket_id, content, priority)
    PROCESS:
      1. LLM으로 카테고리 분류
      2. 우선순위 기반 심각도 결정
      3. 카테고리 기반 담당자 라우팅
    OUTPUT: TicketOutput (category, severity, assignee, reason)
    EXCEPTION:
      - content 빈 값 → ValueError
      - LLM 응답 파싱 실패 → category="unclassified"
    """
    if not input.content.strip():
        raise ValueError(f"빈 content: {input.ticket_id}")

    # ... LLM 호출 및 처리 ...
    pass
```

---

### 2-4. 예외 처리 및 실패 케이스 전략

Agent는 실패할 수 있다. **실패를 설계해야 한다.**

#### 실패 유형 분류

| 유형 | 예시 | 처리 전략 |
|------|------|-----------|
| 외부 API 실패 | Jira 타임아웃 | 재시도 + 대체 데이터 |
| LLM 응답 오류 | JSON 파싱 실패 | 재시도 + 기본값 |
| 데이터 오류 | 필수 필드 누락 | 검증 후 조기 실패 |
| 비즈니스 로직 오류 | 예산 초과 | 사람에게 에스컬레이션 |
| 무한 루프 | Agent가 같은 행동 반복 | 최대 시도 횟수 제한 |

#### 재시도 전략

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """지수 백오프 재시도 데코레이터"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise  # 마지막 시도 실패 시 예외 전파
                    print(f"시도 {attempt}/{max_attempts} 실패: {e}")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1.0)
def call_jira_api(ticket_id: str) -> dict:
    """Jira API 호출 (실패 시 최대 3회 재시도)"""
    # ... API 호출 ...
    pass
```

#### 에스컬레이션 전략

```python
from enum import Enum

class EscalationLevel(Enum):
    AUTO_RETRY = "auto_retry"          # 자동 재시도
    FALLBACK = "fallback"              # 대체 처리
    NOTIFY = "notify"                  # 알림 발송
    HUMAN_REVIEW = "human_review"      # 사람 검토 요청
    HALT = "halt"                      # 전체 중단

def handle_failure(error: Exception, context: dict) -> EscalationLevel:
    """에러 유형에 따라 에스컬레이션 수준 결정"""
    error_type = type(error).__name__

    if error_type in ["TimeoutError", "ConnectionError"]:
        return EscalationLevel.AUTO_RETRY
    elif error_type == "JSONDecodeError":
        return EscalationLevel.FALLBACK
    elif error_type == "InsufficientFundsError":
        return EscalationLevel.HUMAN_REVIEW
    elif error_type == "DataCorruptionError":
        return EscalationLevel.HALT
    else:
        return EscalationLevel.NOTIFY
```

---

## 3. 실무 의미

### 기획서가 팀 커뮤니케이션 도구다

잘 작성된 기획서는:
- 개발자 → 개발 범위 명확화
- QA → 테스트 케이스 도출
- 기획자 → 요구사항 검증
- 운영자 → 모니터링 포인트 파악

IPO 명세는 단위 테스트의 기반이 된다:
```
Input → 테스트 입력값
Output → 기대 출력값
Exception → 에러 케이스 테스트
```

---

## 4. 비교

### Stateless vs Stateful 비교

| 항목 | Stateless | Stateful |
|------|-----------|----------|
| 구현 복잡도 | 낮음 | 높음 |
| 확장성 | 매우 좋음 | 제한적 |
| 실패 복구 | 단순 재시도 | 체크포인트 필요 |
| 메모리 사용 | 낮음 | 높음 |
| 적합 패턴 | 자동화형 | Planner형 |
| 디버깅 | 쉬움 | 어려움 |

---

## 5. 주의사항

### 기획서 작성 실수

**① Sub-task 경계가 모호함**
- "데이터 처리"는 너무 광범위하다
- "원시 JSON → 정규화 DataFrame 변환"처럼 구체적으로 작성하라

**② 성공 케이스만 정의**
- 실패 케이스를 미리 정의하지 않으면 런타임에 놀라게 된다
- "외부 API가 실패하면 어떻게 되는가?" 반드시 답하라

**③ 상태 저장 위치 미결정**
- Stateful Agent에서 상태를 어디에 저장할지 미리 결정하라
- 메모리? DB? Redis? 결정 기준: 재시작 후에도 유지돼야 하는가?

**④ 입출력 타입 불일치**
- Sub-task A의 출력이 Sub-task B의 입력 타입과 맞아야 한다
- Python dataclass나 Pydantic으로 명시하면 오류를 조기에 발견한다

---

## 6. 코드 예제

### 완성된 Agent 기획서 코드 템플릿

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from enum import Enum

class AgentType(Enum):
    AUTOMATION = "자동화형"
    ANALYSIS = "분석형"
    PLANNER = "Planner형"

class StateType(Enum):
    STATELESS = "stateless"
    STATEFUL = "stateful"

@dataclass
class SubTask:
    """Sub-task 명세"""
    id: str
    name: str
    description: str
    input_schema: Dict
    output_schema: Dict
    tools: List[str]
    failure_cases: List[Dict]  # [{"condition": ..., "action": ...}]

@dataclass
class AgentBlueprint:
    """Agent 기획서 전체 구조"""
    # 기본 정보
    name: str
    version: str = "0.1.0"
    agent_type: AgentType = AgentType.AUTOMATION
    state_type: StateType = StateType.STATELESS

    # 문제 정의
    pain: str = ""
    task: str = ""
    success_metric: str = ""

    # 구조 설계
    subtasks: List[SubTask] = field(default_factory=list)
    workflow: List[str] = field(default_factory=list)  # subtask id 순서

    # 글로벌 실패 처리
    global_failures: List[Dict] = field(default_factory=list)

    def validate(self) -> List[str]:
        """기획서 완성도 검증"""
        issues = []
        if not self.pain:
            issues.append("Pain 정의 필요")
        if not self.success_metric:
            issues.append("성공 기준 정의 필요")
        if not self.subtasks:
            issues.append("Sub-task 최소 1개 이상 필요")
        if not self.workflow:
            issues.append("Workflow 순서 정의 필요")
        # 워크플로우의 모든 ID가 subtask에 존재하는지 확인
        subtask_ids = {st.id for st in self.subtasks}
        for wf_id in self.workflow:
            if wf_id not in subtask_ids:
                issues.append(f"Workflow에 존재하지 않는 subtask: {wf_id}")
        return issues

# 실제 사용 예시
weekly_report = AgentBlueprint(
    name="주간 보고서 자동화 Agent",
    agent_type=AgentType.AUTOMATION,
    state_type=StateType.STATELESS,
    pain="매주 3시간을 보고서 수동 작성에 낭비",
    task="Jira/DB 데이터를 수집하여 주간 요약 보고서 자동 생성 및 발송",
    success_metric="보고서 생성 시간 3h → 5분 이하, 정확도 95% 이상",
    subtasks=[
        SubTask(
            id="ST-1",
            name="데이터 수집",
            description="Jira와 DB에서 주간 데이터 수집",
            input_schema={"week_start": "date", "week_end": "date"},
            output_schema={"jira_issues": "list", "db_metrics": "dict"},
            tools=["jira_api", "db_query"],
            failure_cases=[
                {"condition": "Jira API 타임아웃", "action": "AUTO_RETRY x3"},
                {"condition": "DB 연결 실패", "action": "NOTIFY + HALT"},
            ]
        ),
        SubTask(
            id="ST-2",
            name="요약 생성",
            description="수집된 데이터를 LLM으로 요약",
            input_schema={"jira_issues": "list", "db_metrics": "dict"},
            output_schema={"summary_text": "str", "highlights": "list"},
            tools=["llm_summarize"],
            failure_cases=[
                {"condition": "LLM 응답 품질 저하", "action": "HUMAN_REVIEW 플래그"},
            ]
        ),
    ],
    workflow=["ST-1", "ST-2"],
)

# 검증
issues = weekly_report.validate()
if issues:
    print("기획서 문제점:", issues)
else:
    print("기획서 검증 완료")
```

---

## Q&A

**Q. Sub-task 분해는 얼마나 세분화해야 하는가?**

> 독립적으로 테스트할 수 있는 최소 단위가 적당하다.
> 너무 세분화하면 오케스트레이션 복잡도가 높아진다.
> 너무 크게 묶으면 실패 원인 파악이 어렵다.
> "하나의 도구를 사용하는 단위"가 좋은 기준이다.

**Q. Stateful Agent에서 상태를 잃으면 어떻게 하는가?**

> 체크포인트(Checkpoint) 전략을 사용한다.
> 각 Sub-task 완료 시 상태를 영속 저장소(DB, Redis)에 저장한다.
> 실패 시 마지막 체크포인트부터 재시작한다.

**Q. 예외 처리를 미리 다 정의할 수 있는가?**

> 모든 경우를 미리 정의하기는 어렵다.
> 하지만 "외부 의존성 실패", "데이터 오류", "LLM 응답 오류" 세 범주만 커버해도 80%의 실패를 처리할 수 있다.
> 나머지는 운영 중 발견되는 대로 추가한다.

---

## 퀴즈

### Q1. Sub-task 분해 원칙

다음 중 올바른 Sub-task 분해 원칙이 아닌 것은?

- A) 하나의 Sub-task는 하나의 책임만 가진다
- B) Sub-task는 독립적으로 테스트 가능해야 한다
- C) 하나의 Sub-task에 가능한 많은 기능을 묶어 효율을 높인다
- D) Sub-task 출력이 다음 Sub-task 입력이 된다

<details>
<summary>힌트</summary>
단일 책임 원칙(SRP)이 Sub-task 분해에도 적용된다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: C**

하나의 Sub-task에 많은 기능을 묶으면 단일 책임 원칙을 위반한다.
실패 시 어디서 문제가 생겼는지 파악하기 어렵고, 부분 재시도가 불가능해진다.
각 Sub-task는 명확하고 단일한 목적을 가져야 한다.

</details>

---

### Q2. Stateful vs Stateless 선택

다음 시나리오에서 Stateful 구조가 반드시 필요한 경우는?

- A) 이메일 제목에서 카테고리를 추출하는 작업 (건당 독립 처리)
- B) PDF를 텍스트로 변환하는 작업
- C) 사용자와 대화하며 점진적으로 요구사항을 수집하는 작업
- D) 이미지에서 텍스트를 OCR하는 작업

<details>
<summary>힌트</summary>
이전 결과를 기억하고 다음 행동에 활용해야 하는 경우는?
</details>

<details>
<summary>정답 및 해설</summary>

**정답: C**

대화형 요구사항 수집은 이전 대화 내용을 기억해야 한다.
사용자가 말한 내용을 누적해서 기억하지 못하면 대화가 처음부터 다시 시작된다.
A, B, D는 각 입력이 독립적으로 처리되므로 Stateless로 충분하다.

</details>

---

### Q3. IPO 명세 작성

다음 Sub-task의 IPO 명세에서 빠진 항목은?

```
Sub-task: 이슈 분류
INPUT: ticket_content (str)
OUTPUT: {"category": str, "assignee": str}
PROCESS: LLM으로 카테고리 분류 후 담당자 매핑
```

- A) 입력 타입
- B) 출력 타입
- C) 예외 케이스
- D) 처리 단계

<details>
<summary>힌트</summary>
IPO 명세에서 실패 시 처리 방법을 정의하는 항목은?
</details>

<details>
<summary>정답 및 해설</summary>

**정답: C**

예외 케이스(실패 처리)가 없다.
최소한 다음을 정의해야 한다:
- content가 비어있으면?
- LLM 응답 파싱 실패하면?
- 매핑되는 담당자가 없으면?

예외 케이스 없는 IPO는 미완성이다.

</details>

---

### Q4. 실패 처리 전략

다음 중 "외부 결제 API가 간헐적으로 타임아웃 발생"에 가장 적합한 처리 전략은?

- A) 즉시 전체 Agent를 중단한다
- B) 지수 백오프를 적용한 자동 재시도를 3회 시도한다
- C) 사람에게 즉시 에스컬레이션한다
- D) 오류를 무시하고 다음 단계를 진행한다

<details>
<summary>힌트</summary>
간헐적 네트워크 오류는 재시도로 해결되는 경우가 많다.
</details>

<details>
<summary>정답 및 해설</summary>

**정답: B**

간헐적 타임아웃은 네트워크 문제인 경우가 많아 재시도로 해결된다.
지수 백오프(1초 → 2초 → 4초)로 서버에 부담을 주지 않으면서 재시도한다.
3회 후에도 실패하면 그때 에스컬레이션을 결정한다.

</details>

---

### Q5. Workflow 설계

다음 Workflow에서 문제점은?

```
ST-1: 보고서 생성 (LLM 요약)
ST-2: 데이터 수집 (DB 쿼리)
Workflow: ST-1 → ST-2
```

<details>
<summary>힌트</summary>
ST-1은 ST-2의 결과물이 필요하지 않은가?
</details>

<details>
<summary>정답 및 해설</summary>

**순서가 잘못되었다.**

ST-1(보고서 생성)은 ST-2(데이터 수집)의 결과를 입력으로 사용한다.
데이터가 없는데 보고서를 먼저 생성할 수 없다.
올바른 Workflow: ST-2(데이터 수집) → ST-1(보고서 생성)

Sub-task 간 의존 관계를 항상 확인하고 순서를 정의해야 한다.

</details>

---

## 실습 명세

### I DO (강사 시연, 15분)

**강사가 실시간으로 Session 1에서 도출한 Agent 후보를 기획서로 구조화한다.**

1. AgentBlueprint 템플릿 선택
2. Sub-task 분해 (화이트보드 또는 코드)
3. 각 Sub-task의 IPO 명세 작성
4. Workflow 다이어그램 그리기
5. 실패 케이스 3개 이상 정의

---

### WE DO (강사 + 수강생 함께, 20분)

**수강생이 자신의 Agent 후보를 기획서로 변환한다.**

진행 방식:
1. Session 1의 AgentSpec을 기반으로 시작
2. Task를 3-5개 Sub-task로 분해
3. 가장 중요한 Sub-task 1개의 IPO 완성
4. Stateless vs Stateful 선택 이유 작성

체크포인트:
- Sub-task 간 I/O가 연결되는가?
- 실패 케이스가 최소 2개 정의되었는가?

---

### YOU DO (수강생 독립 실습, 25분)

**Agent 구조 다이어그램을 완성하고 기획서를 작성한다.**

제출물: `labs/agent-problem-definition/artifacts/` 폴더에 작성

요구사항:
- Workflow 다이어그램 (텍스트 또는 mermaid)
- 모든 Sub-task의 IPO 명세
- Stateless/Stateful 선택 이유
- 실패 케이스 및 처리 전략 (최소 3개)

모범 답안: `labs/agent-problem-definition/artifacts/example-blueprint.md` 참고
