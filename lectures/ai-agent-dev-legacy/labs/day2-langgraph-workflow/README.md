# 실습: LangGraph 기반 워크플로우 구현

> **Session 2 연계** | 소요 시간: 90분 | 난이도: 중급

---

## 학습 목표

- LangGraph의 Node–Edge–State 구조를 직접 구현한다
- Conditional Edge로 조건 분기와 재시도 루프를 만든다
- State Propagation이 어떻게 동작하는지 체험한다
- 체크포인트로 State를 영속화하는 방법을 익힌다

## 환경 요구사항

```bash
pip install langgraph langchain-openai pydantic
export OPENAI_API_KEY="your-key"
```

> OpenAI API Key가 없으면 `src/mock_llm.py`의 MockLLM을 사용하세요.

---

## I DO: 강사 시연 (15분)

강사가 **뉴스 요약 워크플로우**를 라이브로 구현합니다.

### 시연 내용

1. `WorkflowState` TypedDict 정의
2. `search_node`, `evaluate_node`, `report_node` 구현
3. `StateGraph`로 그래프 조립
4. `add_conditional_edges`로 재시도 루프 추가
5. 의도적으로 실패시켜 Fallback 흐름 확인

### 핵심 관찰 포인트

- Node 함수가 받는 인자와 반환하는 값의 형식
- `Annotated[int, operator.add]`가 실제로 누적되는 과정
- 분기 함수의 반환값이 Edge 매핑에서 어떻게 사용되는지

---

## WE DO: 함께 실습 (30분)

**코드 리뷰 워크플로우**를 함께 구현합니다.

### Step 1: State 설계 (10분)

`src/we_do_code_review.py` 파일을 열고 State를 완성하세요.

```python
from typing import TypedDict, Annotated
import operator

class CodeReviewState(TypedDict):
    pr_url: str
    code_content: str       # fetch 후 채워짐
    issues: list[str]       # analyze 후 채워짐
    review_comment: str     # format 후 채워짐
    retry_count: Annotated[int, operator.add]
    messages: Annotated[list[str], operator.add]
    # 질문: 어떤 필드가 더 필요한가?
```

**논의 포인트**:
- `retry_count`는 왜 `Annotated[int, operator.add]`인가?
- `code_content`는 왜 일반 `str`인가?
- `is_fetch_success` 같은 플래그 필드가 필요한가?

### Step 2: Node 구현 (15분)

3개의 Node를 순서대로 구현합니다.

```python
def fetch_pr_node(state: CodeReviewState) -> dict:
    """PR URL에서 코드를 가져온다 (Mock)"""
    pr_url = state["pr_url"]
    # TODO: Mock으로 구현
    # 성공 시: {"code_content": "...", "messages": ["fetch 완료"]}
    # 실패 시: {"code_content": "", "retry_count": 1, "messages": ["fetch 실패"]}
    pass

def analyze_node(state: CodeReviewState) -> dict:
    """코드를 분석해 이슈를 찾는다 (LLM 호출)"""
    code = state["code_content"]
    # TODO: LLM 또는 Mock으로 구현
    pass

def format_node(state: CodeReviewState) -> dict:
    """이슈를 리뷰 댓글 형식으로 변환한다"""
    issues = state["issues"]
    # TODO: 마크다운 형식으로 포맷
    pass
```

### Step 3: 재시도 로직 추가 (5분)

```python
def after_fetch(state: CodeReviewState) -> str:
    """fetch 결과에 따라 다음 Node 결정"""
    if state["code_content"]:
        return "analyze"
    if state["retry_count"] < 2:
        return "fetch"    # 재시도
    return "error"        # 포기

# 그래프에 추가
graph.add_conditional_edges(
    "fetch",
    after_fetch,
    {"analyze": "analyze", "fetch": "fetch", "error": END}
)
```

---

## YOU DO: 독립 실습 (45분)

### 과제: 데이터 파이프라인 Agent

CSV URL을 입력받아 다음 단계를 수행하는 LangGraph 워크플로우를 구현하세요.

### 요구사항

**Step 1: 데이터 로드**
- CSV URL에서 데이터를 로드한다
- 실패 시 최대 2회 재시도한다

**Step 2: 품질 검사**
- 결측값 비율을 계산한다
- 결측값 30% 초과 시 `quality_failed` 경로로 분기한다

**Step 3: 분기 처리**
- 품질 통과 → 이상치 탐지 → 통계 보고서 생성
- 품질 실패 → 간략 오류 보고서 생성

**Step 4: 보고서 출력**
- 두 경로 모두 최종 `report` 필드에 결과를 저장한다

### 시작 파일

`src/you_do_pipeline.py`에서 시작하세요.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class PipelineState(TypedDict):
    csv_url: str
    data: list[dict]
    missing_ratio: float
    outliers: list
    report: str
    retry_count: Annotated[int, operator.add]
    messages: Annotated[list[str], operator.add]

# TODO: 아래 Node들을 구현하세요
def load_data_node(state: PipelineState) -> dict: ...
def quality_check_node(state: PipelineState) -> dict: ...
def detect_outliers_node(state: PipelineState) -> dict: ...
def generate_report_node(state: PipelineState) -> dict: ...
def error_report_node(state: PipelineState) -> dict: ...

# TODO: 그래프를 조립하세요
def build_pipeline() -> ...:
    g = StateGraph(PipelineState)
    # ...
    pass
```

### 평가 기준

| 항목 | 확인 내용 |
|------|-----------|
| State 설계 | TypedDict 필드가 올바르게 정의되었는가? |
| 분기 함수 | 모든 케이스(품질통과/실패/재시도)를 처리하는가? |
| 재시도 | retry_count가 State에 올바르게 누적되는가? |
| 루프 탈출 | 재시도 횟수 초과 시 강제 종료되는가? |
| 두 경로 | 품질통과/실패 두 경로 모두 report를 생성하는가? |

### 실행 방법

```bash
cd labs/day2-langgraph-workflow
python src/you_do_pipeline.py

# 기대 출력:
# [load] CSV 데이터 로드 완료: 100행
# [quality] 결측값 비율: 5.2%
# [outliers] 이상치 3건 탐지
# [report] 보고서 생성 완료
```

---

## 참고: solution 디렉토리

막혔을 때 `solution/pipeline_solution.py`를 참고하세요.
단, 먼저 30분은 혼자 시도해보세요.

```bash
# solution 실행
python solution/pipeline_solution.py
```
