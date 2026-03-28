# Day 4 실습: Agent 평가 체계 설계 및 Golden Test Set 구축

> 소요 시간: 약 85분
> 형태: Python 코드 + 설계 혼합 실습

## 개요

Agent의 품질을 체계적으로 측정하고 개선하기 위한 평가 체계를 설계한다. 정량 메트릭을 구현하고, Golden Test Set을 구축하며, LM-as-a-Judge 패턴을 적용한다.

## 사전 준비

```bash
pip install openai langchain langchain-openai
```

```bash
export OPENAI_API_KEY="your-api-key"
```

## 디렉토리 구조

```
day4-evaluation-framework/
├── README.md                          # 이 파일
├── src/
│   ├── i_do_metrics.py               # I DO: 기본 평가 메트릭 구현
│   ├── we_do_golden_test.py          # WE DO: Golden Test Set 구축
│   └── you_do_lm_judge.py           # YOU DO: LM-as-a-Judge 구현
├── solution/
│   └── you_do_lm_judge.py           # YOU DO 정답 코드
└── data/
    └── golden_test_set.json          # 샘플 Golden Test Set
```

---

## I DO (시연) - 15분

강사가 기본 평가 메트릭을 구현하고 실행하는 과정을 시연한다.

### 실행 방법

```bash
python src/i_do_metrics.py
```

### 학습 포인트

- Exact Match, F1 Score, Tool Call Accuracy 메트릭의 동작 원리
- 각 메트릭의 적합한 사용 상황
- 결과 해석 방법 (0.0 ~ 1.0 범위)

---

## WE DO (함께) - 30분

전체가 함께 Golden Test Set을 구축한다.

### 진행 순서

1. Day 2-3에서 만든 Agent의 주요 사용 시나리오를 정리한다
2. 시나리오별 테스트 케이스를 설계한다 (최소 5개)
3. 각 테스트 케이스에 대해:
   - 입력(query)과 기대 출력(expected_output) 작성
   - 기대하는 Tool 호출 목록 정의
   - 카테고리, 난이도 태깅
4. `data/golden_test_set.json` 형식으로 저장한다

### 실행 방법

```bash
python src/we_do_golden_test.py
```

### 테스트 케이스 설계 가이드

| 항목 | 설명 | 예시 |
|------|------|------|
| id | 고유 식별자 | "GT-001" |
| category | 분류 | "환불_문의", "상품_검색" |
| difficulty | 난이도 | "easy", "medium", "hard" |
| input | 사용자 입력 | "주문 ORD-1234 환불해주세요" |
| expected_output | 기대 응답 (핵심 내용) | "환불 처리 안내" |
| expected_tool_calls | 기대 도구 호출 | [{"tool": "lookup_order", ...}] |

---

## YOU DO (독립) - 40분

LM-as-a-Judge를 구현하고 실제 평가를 수행한다.

### 과제 내용

1. `src/you_do_lm_judge.py`의 `TODO` 부분을 완성한다
2. Pointwise 평가(절대 평가)를 구현한다:
   - 정확성, 완성도, 유용성, 충실성, 안전성 5개 항목
   - 각 항목 1-5점 채점 + 이유 작성
3. Golden Test Set에 대해 평가를 실행한다
4. 평가 결과를 분석하고 개선점을 도출한다

### 실행 방법

```bash
python src/you_do_lm_judge.py
```

### 완료 기준

- [ ] Pointwise Judge 프롬프트 작성 완료
- [ ] OpenAI API를 사용한 LLM 평가 함수 구현
- [ ] Golden Test Set 5개 이상에 대해 평가 실행
- [ ] 평가 결과 요약 (평균 점수, 약한 영역 식별)
- [ ] 1가지 이상 개선점 도출

### 산출물

- 평가 결과 리포트 (콘솔 출력 또는 JSON)
- 완성된 Golden Test Set (`data/golden_test_set.json`)

### 막히면?

정답 코드는 `solution/you_do_lm_judge.py`에서 확인할 수 있다.
