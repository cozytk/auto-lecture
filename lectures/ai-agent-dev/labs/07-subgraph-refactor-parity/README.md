# 실습 07: Subgraph Refactor Parity 검증

## 실습 목적

모놀리식 LangGraph를 서브그래프 구조로 리팩토링하고,
리팩토링 전후의 출력과 핵심 상태가 동일하게 유지되는지 parity 기준으로 검증한다.

- **연관 세션**: Session 4 - 구조 리팩토링 & 확장성 설계
- **난이도**: 중급 ~ 심화
- **예상 소요 시간**: 65분 (I DO 10분 / WE DO 20분 / YOU DO 35분)

## 사전 준비

```bash
just setup
```

- Python 3.10+
- `langgraph` 설치 가능 환경
- `lectures/ai-agent-dev/labs/day2/02-refactor-boundary-workshop/README.md`에서 작성한 경계 문서

---

## I DO: 시연 관찰 (약 10분)

강사가 `src/i-do/refactor_parity.py`를 실행하며 아래 흐름을 시연한다.

- 모놀리식 그래프 실행
- 동일 기능의 서브그래프 버전 실행
- 최종 `report`와 `insights` 비교
- parity 체크 결과 출력

### 시연 코드 실행

```bash
just run-i-do
```

### 관찰 포인트

- 리팩토링의 1차 성공 기준은 구조가 아니라 결과 동일성이다.
- 부모 그래프와 서브그래프는 공유 키만 주고받는다.
- 내부 전용 상태는 외부에 노출하지 않아도 parity를 유지할 수 있다.
- parity 기준은 문자열 일치뿐 아니라 핵심 필드 개수와 흐름도 포함할 수 있다.

---

## WE DO: 함께 실습 (약 20분)

강사와 함께 `src/we-do/refactor_parity.py`를 채우며 서브그래프 연결을 완성한다.

### 1단계: collection / analysis 서브그래프 분리

- 모놀리식에서 한 함수에 섞여 있던 수집/분석/보고서 단계를 역할별로 나눈다.

### 2단계: 부모 그래프 연결

```bash
just run-we-do
```

- `add_node()`에 컴파일된 subgraph를 넣는다.
- 부모와 자식이 공유할 키를 다시 점검한다.

### 3단계: parity 체크 작성

- `report`, `insights`, `raw_data` 개수를 비교해 리팩토링 결과를 검증한다.

---

## YOU DO: 독립 과제 (약 35분)

`src/you-do/refactor_parity.py`를 완성하세요.

### 과제 설명

1. `build_monolith()`를 완성하여 수집 -> 분석 -> 보고서 흐름을 가진 기준 그래프를 만드세요.
2. `build_refactored()`에서 collection subgraph와 analysis subgraph를 부모 그래프에 연결하세요.
3. `check_parity()`에서 두 그래프의 `report`, `insights`, `raw_data`를 비교하세요.
4. `run_demo()`로 기준 입력 하나를 실행하고 parity 결과를 출력하세요.
5. 리팩토링 후 내부 전용 키가 부모 결과에 나타나지 않는지 확인하세요.

### 시작 방법

```bash
just run
```

### 힌트

<details>
<summary>힌트 1: subgraph를 node로 연결하기</summary>

```python
collection = build_collection_subgraph()
graph.add_node("collect", collection)
```
</details>

<details>
<summary>힌트 2: parity는 어떤 필드를 비교할까</summary>

최소한 `report`, `insights`, `raw_data` 길이는 비교하세요. 필요한 경우 `messages` 대신 파생 결과만 비교해도 됩니다.
</details>

<details>
<summary>힌트 3: 내부 전용 키 숨기기</summary>

서브그래프에서만 쓰는 `collection_status`, `analysis_mode` 같은 키는 부모 `TypedDict`에 넣지 않으면 됩니다.
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

- `build_monolith()`와 `build_refactored()`가 모두 존재하는가
- `check_parity()`가 `report`, `insights`, `raw_data`를 비교하는가
- YOU DO 파일에 TODO가 남아있지 않은가
- 리팩토링 결과가 parity 통과를 출력하는가

## 트러블슈팅

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| 서브그래프 결과가 부모에 안 보임 | 공유 키 이름 불일치 | 부모/자식 TypedDict의 공통 키를 맞춘다 |
| parity가 계속 실패함 | 리팩토링하면서 비즈니스 로직이 바뀜 | 모놀리식 출력과 서브그래프 출력을 단계별로 비교한다 |
| 부모 결과에 내부 상태가 노출됨 | 부모 State에 내부 키를 넣음 | 내부용 키는 서브그래프 State에만 남긴다 |
