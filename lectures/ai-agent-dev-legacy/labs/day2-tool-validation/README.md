# 실습: Tool 호출 통제 & Validation

> **Session 3 연계** | 소요 시간: 90분 | 난이도: 중급

---

## 학습 목표

- Tool 스키마를 Pydantic으로 설계한다
- 사전 검증(Pre-call)과 사후 검증(Post-call)을 구현한다
- Fallback 체인을 우선순위 기반으로 구현한다
- 루프 방지 로직(동일 소스 연속 호출 차단)을 구현한다

## 환경 요구사항

```bash
pip install pydantic langchain-core
```

> 이 실습은 외부 API 호출이 없습니다. Mock 객체만 사용합니다.

---

## I DO: 강사 시연 (15분)

강사가 **안전한 웹 검색 Tool**을 라이브로 구현합니다.

### 시연 내용

1. `SearchInput` Pydantic 스키마 정의
2. 사전 검증: 권한 확인 + 쿼리 길이 + 중복 호출 방지
3. 사후 검증: 빈 결과 처리 + 품질 기준
4. 실패 시 Fallback Tool으로 전환하는 흐름
5. 의도적으로 Tool을 실패시켜 Fallback 동작 확인

### 핵심 관찰 포인트

- 사전 검증이 실제 Tool 호출을 막는 과정
- 사후 검증에서 `should_retry=True`가 Fallback 체인을 어떻게 유발하는지
- call_history로 연속 호출을 어떻게 탐지하는지

---

## WE DO: 함께 실습 (30분)

**데이터 처리 Tool 시스템**을 함께 구현합니다.

`src/we_do_data_tools.py` 파일을 열고 진행합니다.

### Step 1: Tool 스키마 정의 (10분)

```python
from pydantic import BaseModel, Field

class DataLoadInput(BaseModel):
    source: str = Field(
        description=(
            "데이터 소스 경로 또는 URL. "
            "로컬 파일은 절대 경로, URL은 https://로 시작해야 합니다."
        )
    )
    format: str = Field(
        default="csv",
        description="파일 형식 (csv, json, parquet)",
        pattern="^(csv|json|parquet)$",
    )
    # 질문: max_rows 필드가 필요한가? 왜?
```

**논의 포인트**:
- `source` 필드의 의미 검증은 무엇이 있는가?
- `format`에 enum 대신 `pattern` 정규식을 사용한 이유는?

### Step 2: 사전 검증 로직 구현 (10분)

어떤 조건을 검증해야 하는지 함께 논의하고 구현합니다.

```python
def pre_validate(self, source: str, fmt: str) -> ValidationResult:
    # 논의: 어떤 조건을 검사해야 하는가?
    # 1. source가 비어 있지 않은가?
    # 2. format이 허용 목록에 있는가?
    # 3. 로컬 파일이면 경로가 절대 경로인가?
    # 4. URL이면 https://로 시작하는가?
    pass
```

### Step 3: Fallback 체인 구현 (10분)

```python
TOOL_FALLBACK_CHAIN = {
    "load_from_url": ["load_from_cache", "load_from_local"],
    # 함께 추가할 항목:
    # "load_from_cache": ???
    # "load_from_local": ???
}
```

**논의 포인트**:
- Fallback 체인에 순환이 생기면 어떻게 되는가?
- LLM Fallback은 언제 체인의 마지막에 두어야 하는가?

---

## YOU DO: 독립 실습 (45분)

### 과제: 멀티 소스 정보 수집 Agent

`src/you_do_multi_source.py`에서 `TODO` 항목을 완성하세요.

### 요구사항

**소스 우선순위**: `web_search → database → cache → llm_knowledge`

**사전 검증 조건**:
- 쿼리 길이: 1자 이상, 200자 이하
- 동일 소스 연속 호출 금지: call_history 마지막 항목이 현재 소스와 같으면 차단

**사후 검증 조건**:
- 결과 타입이 `list`인가?
- 결과가 비어 있는가? → 빈 결과면 `should_retry=True`
- 결과 개수가 2건 미만인가? → 품질 부족이면 `should_retry=True`

**루프 방지**:
- 총 호출 횟수가 `MAX_TOTAL_CALLS=10`을 초과하면 즉시 중단

### 평가 기준

| 항목 | 확인 내용 |
|------|-----------|
| 사전 검증 | 쿼리 길이 + 연속 호출 금지가 모두 구현되었는가? |
| 사후 검증 | 타입, 빈 결과, 품질 부족을 모두 처리하는가? |
| Fallback 체인 | 우선순위 순서대로 시도하는가? |
| 루프 방지 | 총 호출 횟수 초과 시 중단하는가? |
| LLM Fallback | 모든 소스 실패 시 llm_knowledge로 응답하는가? |

### 실행 방법

```bash
cd labs/day2-tool-validation

# YOU DO 실행
python src/you_do_multi_source.py

# 기대 출력:
# ============================
# 케이스 1: 웹 검색 성공
# ============================
# **[web_search]** 검색 결과:
# - [웹] AI Agent 2026 트렌드에 관한 최신 뉴스 1
# ...
```

---

## 참고: solution 디렉토리

막혔을 때 `solution/multi_source_solution.py`를 참고하세요.
먼저 30분은 혼자 시도해보세요.

```bash
python solution/multi_source_solution.py
```
