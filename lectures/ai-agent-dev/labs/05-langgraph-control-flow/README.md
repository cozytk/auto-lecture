# 실습 05: LangGraph Control Flow 구현

## 실습 목적

LangGraph의 Node / Edge / State 구조를 실제 업무 흐름에 적용하여,
Conditional Edge, retry loop, fallback 경로를 가진 제어 흐름을 직접 설계하고 구현한다.

- **연관 세션**: Session 2 - LangGraph 기반 제어 흐름 설계
- **난이도**: 중급
- **예상 소요 시간**: 85분 (I DO 15분 / WE DO 25분 / YOU DO 45분)

## 사전 준비

```bash
just setup
```

- Python 3.10+
- `langgraph` 설치 가능 환경
- Session 1에서 만든 Agent 4요소 설계 메모

---

## I DO: 시연 관찰 (약 15분)

강사가 `src/i-do/control_flow.py`를 실행하며 아래 흐름을 시연한다.

- 요청 분류 (`classify`)
- 유형별 처리 Node 실행 (`access`, `billing`, `incident`)
- 품질 게이트에서 retry / finish / fallback 분기
- 최대 시도 수를 넘기면 fallback으로 전환

### 시연 코드 실행

```bash
just run-i-do
```

### 관찰 포인트

- Node는 전체 State를 덮어쓰지 않고 필요한 필드만 반환한다.
- Conditional Edge는 단순 if-else가 아니라 다음 Node 선택을 그래프 수준에서 노출한다.
- retry loop에는 반드시 종료 조건이 있어야 한다.
- fallback은 실패 숨기기가 아니라 "낮은 품질이지만 종료 가능한 경로"다.

---

## WE DO: 함께 실습 (약 25분)

강사와 함께 `src/we-do/control_flow.py`의 TODO를 채워 그래프를 완성한다.

### 1단계: 요청 유형 분류 함수 완성

- `determine_route()`에서 키워드 기준으로 `access`, `billing`, `incident`를 반환한다.
- 분류 결과가 node 이름과 직접 연결되도록 설계한다.

### 2단계: 품질 게이트 분기 구현

```bash
just run-we-do
```

- `route_after_quality()`에서 `finish`, `fallback`, 또는 원래 route 재시도를 반환한다.
- retry와 fallback의 차이를 로그에 남긴다.

### 3단계: 그래프 연결 확인

- `START -> classify -> 각 handler -> quality_gate` 구조를 점검한다.
- 각 handler 이름과 Conditional Edge 반환값이 일치하는지 확인한다.

---

## YOU DO: 독립 과제 (약 45분)

`src/you-do/control_flow.py`를 완성하세요.

### 과제 설명

"운영 요청 triage Agent"를 구현합니다.

1. `determine_route()`를 완성하여 요청을 `access`, `billing`, `incident`로 분류하세요.
2. `handle_incident()`에서 첫 시도는 낮은 confidence, 재시도 후에는 높은 confidence가 되도록 구현하세요.
3. `quality_gate()`와 `route_after_quality()`를 구현하여 retry / finish / fallback 흐름을 연결하세요.
4. `build_graph()`에서 Conditional Edge와 loop를 완성하세요.
5. `run_demo()`로 3개 시나리오를 실행하세요.

### 시작 방법

```bash
just run
```

### 힌트

<details>
<summary>힌트 1: route 함수 반환값</summary>

`add_conditional_edges()`의 반환값은 다음 node 이름과 맞아야 합니다.

```python
def route_after_quality(state: WorkflowState) -> str:
    if state["confidence"] >= 0.8:
        return "finish"
    if state["attempts"] >= state["max_attempts"]:
        return "fallback"
    return state["route"]
```
</details>

<details>
<summary>힌트 2: retry가 필요한 상태 설계</summary>

retry 여부를 별도 boolean으로 두지 않아도 됩니다. `attempts`, `confidence`, `route`만 있으면 다음 node를 계산할 수 있습니다.
</details>

<details>
<summary>힌트 3: langgraph import 위치</summary>

실습 코드에서는 `build_graph()` 안에서 `StateGraph`, `START`, `END`를 import하면 모듈 import 단계의 의존성을 줄일 수 있습니다.
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

- `determine_route()`가 3개 시나리오를 올바르게 분류하는가
- `route_after_quality()`가 finish / retry / fallback을 구분하는가
- `build_graph()` 함수가 존재하는가
- YOU DO 파일에 TODO가 남아있지 않은가

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| `ValueError`로 unknown path 발생 | 반환값과 node 이름 불일치 | handler 이름과 route 반환 문자열을 맞춘다 |
| 무한 루프 | `attempts` 증가 또는 max 조건 누락 | `handle_*` 또는 gate에서 시도 횟수를 갱신한다 |
| fallback이 절대 실행되지 않음 | finish 조건이 너무 느슨함 | confidence 임계값과 최대 시도 수 조건을 다시 본다 |
