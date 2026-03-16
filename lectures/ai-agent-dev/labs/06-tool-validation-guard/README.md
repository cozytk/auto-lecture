# 실습 06: Tool Validation Guard와 Audit Trail 구현

## 실습 목적

Tool 호출 전 Validation Gate와 호출 후 결과 검증, 감사 로그 기록까지 하나의 LangGraph 흐름으로 묶어
위험한 Tool 호출을 통제 가능한 Agent 구조로 구현한다.

- **연관 세션**: Session 3 - Tool 호출 통제 & Validation
- **난이도**: 중급
- **예상 소요 시간**: 80분 (I DO 15분 / WE DO 25분 / YOU DO 40분)

## 사전 준비

```bash
just setup
```

- Python 3.10+
- `langgraph` 설치 가능 환경
- Session 2 제어 흐름 실습에서 만든 retry / fallback 개념 복습

---

## I DO: 시연 관찰 (약 15분)

강사가 `src/i-do/tool_guard.py`를 실행하며 아래 흐름을 시연한다.

- schema validation
- policy validation
- context validation
- Tool 실행
- result validation
- success / rejection audit 기록

### 시연 코드 실행

```bash
just run-i-do
```

### 관찰 포인트

- Tool 호출은 LLM 출력이라기보다 "신뢰하지 않는 입력"으로 취급한다.
- schema / policy / context를 한 번에 섞지 않고 단계별로 나누면 거부 사유를 설명하기 쉽다.
- 거부도 audit에 남겨야 나중에 디버깅과 규정 준수가 가능하다.
- 실행 성공과 결과 유효성은 다른 문제다.

---

## WE DO: 함께 실습 (약 25분)

강사와 함께 `src/we-do/tool_guard.py`의 TODO를 채워 Validation 파이프라인을 완성한다.

### 1단계: schema / policy 검증 구현

- 필수 파라미터 누락, 범위 초과, 승인 필요 Tool 차단을 구현한다.

### 2단계: context 중복 호출 방지 추가

```bash
just run-we-do
```

- 직전 Tool과 같은 Tool을 반복 호출하는 경우 거부한다.
- call_count와 max_calls를 함께 본다.

### 3단계: audit entry 생성

- 성공 / 거부 모두 `status`, `tool`, `reason`, `call_count`를 남긴다.

---

## YOU DO: 독립 과제 (약 40분)

`src/you-do/tool_guard.py`를 완성하세요.

### 과제 설명

"운영 자동화 Tool Guard"를 구현합니다.

1. `schema_validation()`에서 필수 파라미터와 숫자 범위를 검증하세요.
2. `policy_validation()`에서 승인 필요 Tool과 호출 횟수 제한을 검사하세요.
3. `context_validation()`에서 직전 Tool 반복 호출을 막으세요.
4. `result_validation()`에서 Tool 실행 결과의 구조를 검증하세요.
5. `build_graph()`에서 success / reject 경로와 audit 기록을 연결하세요.

### 시작 방법

```bash
just run
```

### 힌트

<details>
<summary>힌트 1: 스키마 검증 순서</summary>

먼저 필수 파라미터 존재 여부를 확인하고, 그 다음 타입/범위를 확인하면 에러 메시지가 더 읽기 쉬워집니다.
</details>

<details>
<summary>힌트 2: 승인 필요 Tool</summary>

쓰기/삭제 Tool은 자동 승인하지 말고 `approved_by_human` 플래그로 제어하세요.
</details>

<details>
<summary>힌트 3: audit entry 최소 필드</summary>

```python
{
    "status": "approved" or "rejected",
    "tool": state["requested_tool"],
    "reason": state["errors"][-1] if state["errors"] else "ok",
    "call_count": state["call_count"],
}
```
</details>

### 정답 확인

```bash
just run-solution
```

---

## 검증 방법

```bash
just test
```

- 정상 Tool 호출이 schema / policy / context를 통과하는가
- 승인 없는 위험 Tool이 policy 단계에서 거부되는가
- `make_audit_entry()`가 성공/거부 모두 기록하는가
- YOU DO 파일에 TODO가 남아있지 않은가

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| schema는 통과했는데 예상과 다르게 reject됨 | policy/context 규칙 충돌 | 어떤 단계에서 실패했는지 errors를 순서대로 본다 |
| 위험 Tool이 통과함 | 승인 플래그 검사 누락 | `approved_by_human`과 위험 등급 규칙을 연결한다 |
| audit 로그가 비어 있음 | success / reject node에서 entry 추가 누락 | 종료 직전에 audit node를 거치도록 edge를 점검한다 |
