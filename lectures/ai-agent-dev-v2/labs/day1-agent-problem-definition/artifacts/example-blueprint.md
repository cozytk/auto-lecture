# 모범 답안: Agent 기획서 + Workflow (과제 2)

> 이 파일은 YOU DO 과제 2의 모범 답안이다.
> Agent 후보 #1 (고객 문의 자동 분류 및 답변)을 기획서로 구체화한 예시다.

---

## Agent 기획서: 고객 문의 자동 분류 Agent

**버전**: 0.1.0
**패턴**: 자동화형
**상태 구조**: Stateless

### 문제 정의

| 항목 | 내용 |
|------|------|
| Pain | 고객 문의 분류·라우팅에 하루 3-4시간 소요 |
| Task | 수신 문의를 자동 분류하고 담당자에게 라우팅 |
| 성공 기준 | 분류 정확도 90% 이상, 처리 시간 15분 → 30초 이내 |

### Stateless 선택 이유

각 문의는 독립적으로 처리된다.
이전 문의의 분류 결과가 현재 문의에 영향을 주지 않는다.
Stateless로 구현하면 여러 인스턴스를 병렬로 실행해 처리량을 높일 수 있다.

---

## Sub-task 분해

### ST-1: 이메일 수신 및 파싱

**설명**: 수신함에서 미처리 이메일을 읽고 표준 포맷으로 변환한다.

**INPUT**:
```python
@dataclass
class EmailFetchInput:
    since_timestamp: datetime  # 마지막 처리 시점 이후
    max_count: int = 50        # 최대 처리 건수
```

**OUTPUT**:
```python
@dataclass
class EmailFetchOutput:
    emails: list[dict]  # [{"id": str, "subject": str, "body": str, "from": str}]
    fetched_count: int
    next_since: datetime
```

**사용 도구**: `email_reader` (IMAP API)

**예외 케이스**:
- IMAP 서버 연결 실패 → AUTO_RETRY 3회 → NOTIFY 후 종료
- 이메일 인코딩 오류 → 해당 이메일 SKIP + 로그 기록

---

### ST-2: 분류 및 긴급도 판단

**설명**: 이메일 내용을 LLM으로 분류하고 긴급도를 판단한다.

**INPUT**:
```python
@dataclass
class ClassifyInput:
    email_id: str
    subject: str
    body: str
```

**OUTPUT**:
```python
@dataclass
class ClassifyOutput:
    email_id: str
    category: Literal["billing", "technical", "shipping", "general", "unknown"]
    urgency: Literal["low", "medium", "high"]
    confidence: float  # 0.0 ~ 1.0
    reason: str        # 분류 근거 1문장
```

**사용 도구**: `llm_classify` (Tool Use + JSON Schema)

**예외 케이스**:
- confidence < 0.6 → HUMAN_REVIEW 플래그 추가
- LLM JSON 파싱 실패 → 재시도 1회 → 실패 시 category="unknown"

---

### ST-3: 유사 케이스 검색

**설명**: 벡터 DB에서 유사한 과거 문의와 답변을 검색한다.

**INPUT**:
```python
@dataclass
class SearchInput:
    query: str      # 현재 문의 내용
    category: str   # ST-2 분류 결과 (필터링에 사용)
    top_k: int = 3
```

**OUTPUT**:
```python
@dataclass
class SearchOutput:
    similar_cases: list[dict]  # [{"question": str, "answer": str, "score": float}]
    found_count: int
```

**사용 도구**: `vector_search` (벡터 DB)

**예외 케이스**:
- 유사 케이스 없음 (found_count == 0) → 빈 리스트 반환 (정상 처리)
- 벡터 DB 연결 실패 → FALLBACK: 빈 리스트 반환 + 로그

---

### ST-4: 답변 초안 생성

**설명**: 분류 결과와 유사 케이스를 바탕으로 답변 초안을 생성한다.

**INPUT**:
```python
@dataclass
class DraftInput:
    original_email: dict       # 원본 이메일
    classification: ClassifyOutput
    similar_cases: list[dict]  # ST-3 결과
```

**OUTPUT**:
```python
@dataclass
class DraftOutput:
    draft_text: str
    needs_human_review: bool  # True면 담당자가 검토 후 발송
    routing_team: str         # billing / tech / shipping / general
```

**사용 도구**: `llm_draft` (LLM Few-shot)

**예외 케이스**:
- urgency == "high" → needs_human_review = True 강제
- confidence < 0.6 → needs_human_review = True 강제

---

### ST-5: 라우팅 및 발송

**설명**: 담당팀에 이메일을 라우팅하고 처리 결과를 기록한다.

**INPUT**:
```python
@dataclass
class RoutingInput:
    original_email: dict
    draft: DraftOutput
    classification: ClassifyOutput
```

**OUTPUT**:
```python
@dataclass
class RoutingOutput:
    success: bool
    routed_to: str
    message_id: str
    logged_at: datetime
```

**사용 도구**: `email_send` (SMTP API), `db_log` (처리 이력 기록)

**예외 케이스**:
- SMTP 전송 실패 → AUTO_RETRY 3회 → NOTIFY + HALT
- DB 로그 실패 → 경고 로그만 (비즈니스 로직 계속 진행)

---

## Workflow

```
[트리거: 새 이메일 수신 or 5분 주기 폴링]
          ↓
[ST-1: 이메일 수신]
          ↓
    수신 성공?
   ↙         ↘
 Yes          No
  ↓            ↓
[이메일 목록]  [NOTIFY → 종료]
  ↓
[각 이메일에 대해 반복]:
  ↓
[ST-2: 분류]
  ↓
[ST-3: 유사 케이스 검색] (병렬 가능)
  ↓
[ST-4: 초안 생성]
  ↓
    검토 필요?
   ↙         ↘
 Yes          No
  ↓            ↓
[인간 검토    [자동 발송]
 큐 추가]
  ↓
[ST-5: 라우팅 + 로그]
  ↓
[완료]
```

```
mermaid:
flowchart TD
    A[트리거] --> B[ST-1: 이메일 수신]
    B --> C{수신 성공?}
    C -->|Yes| D[ST-2: 분류]
    C -->|No| E[NOTIFY → 종료]
    D --> F[ST-3: 유사 케이스 검색]
    F --> G[ST-4: 초안 생성]
    G --> H{검토 필요?}
    H -->|Yes| I[인간 검토 큐]
    H -->|No| J[자동 발송]
    I --> K[ST-5: 라우팅 + 로그]
    J --> K
```

---

## 글로벌 실패 처리

| 상황 | 처리 방법 |
|------|-----------|
| 모든 재시도 소진 | 슬랙 알림 + 운영자 에스컬레이션 |
| 처리 중 예기치 않은 예외 | 해당 이메일 SKIP + 오류 로그 + 계속 진행 |
| 전체 오류율 > 20% | 자동 일시 중단 + 운영자 알림 |
| 처리 지연 > 30분 | 경고 알림 |
