# Lab 1 — Golden Test Evaluation

> **목표**: Agent 품질 평가 파이프라인을 직접 구현한다.
> Golden Test Set을 설계하고, LM-as-a-Judge로 Faithfulness를 자동 측정하며, 결과를 대시보드로 출력한다.

**소요 시간**: 약 2시간
**형태**: Python 코드 실습
**전제 조건**: Python 3.11+, OpenAI API 키

---

## 디렉토리 구조

```
day4-golden-test-evaluation/
├── README.md          # 이 파일
├── Justfile           # 실습 실행 명령어
├── src/
│   ├── evaluate.py    # WE DO 스캐폴드 (빈칸 채우기)
│   ├── golden_tests.json  # WE DO 테스트 케이스
│   └── requirements.txt
└── solution/
    ├── evaluate.py    # YOU DO 정답 코드
    └── golden_tests.json
```

---

## I DO — 강사 시연

> 강사가 완성된 코드를 단계별로 실행하며 시연한다. 학생은 관찰하며 개념을 익힌다.

### 시연 1: Faithfulness 측정 함수

강사는 `solution/evaluate.py`의 `measure_faithfulness()` 함수를 실행한다.

**시연 내용**:
- LLM을 평가자로 사용해 응답이 문서에 근거하는지 점수화
- 5개 샘플 케이스 실행 → 결과 확인
- Faithfulness 점수가 낮은 케이스의 원인 분석

**핵심 관찰 포인트**:
- 프롬프트에서 "각 문장이 문서에 근거하는지"를 명시적으로 묻는다
- `temperature=0`으로 재현 가능한 결과를 만든다
- JSON 응답 형식으로 자동 파싱한다

### 시연 2: Golden Test Set 실행기

`GoldenTestRunner`로 10개 테스트 케이스를 실행한다.

**시연 내용**:
- JSON 파일에서 테스트 케이스 로드
- 자동 실행 후 pass_rate 계산
- pandas DataFrame으로 결과 시각화

```
결과 예시:
총 테스트: 10
통과: 8
pass_rate: 0.80

실패 케이스:
- acc_003: score=0.62 (tolerance=0.75)
- rob_005: score=0.71 (tolerance=0.75)
```

### 시연 3: Pairwise 비교 평가

두 버전의 응답(v1 vs v2)을 비교해 어느 쪽이 더 나은지 판정한다.

**핵심 관찰**: 순서를 바꿔 두 번 평가해 위치 편향을 제거한다.

---

## WE DO — 함께 실습

> 강사가 이끌고 학생이 따라하며 함께 완성한다.

### Step 1: 환경 설정 (5분)

```bash
just setup
```

`.env` 파일에 API 키를 설정한다:

```
OPENAI_API_KEY=sk-...
```

### Step 2: 테스트 케이스 확인 (5분)

`src/golden_tests.json`을 열어 테스트 케이스 구조를 확인한다:

```json
[
  {
    "id": "acc_001",
    "category": "accuracy",
    "input": {"query": "파이썬 GIL이란 무엇인가?"},
    "contexts": ["GIL(Global Interpreter Lock)은 CPython 구현의 뮤텍스다..."],
    "expected_output": "GIL은 한 번에 하나의 스레드만 파이썬 바이트코드를 실행하도록 제한한다.",
    "tolerance": 0.75
  }
]
```

### Step 3: 빈칸 채우기 (25분)

`src/evaluate.py`를 열어 `# TODO` 주석 위치를 완성한다.

```bash
just run
```

**빈칸 위치**:
1. `measure_faithfulness()` — LLM 평가 프롬프트 완성
2. `GoldenTestRunner.run()` — 점수와 합격 여부 계산
3. `print_report()` — 결과 출력 포맷

### Step 4: 결과 확인 및 토론 (10분)

- pass_rate가 예상보다 낮은 케이스를 찾는다
- 낮은 점수의 원인을 팀과 토론한다
- 프롬프트 수정으로 개선 가능한지 확인한다

```bash
just report
```

---

## YOU DO — 독립 과제

> 학생이 스스로 도전한다. 막히면 `solution/` 폴더를 참조한다.

### 과제: 도메인 특화 평가 파이프라인 구축

**시나리오**: 사내 HR 정책 QA Agent의 품질을 평가하는 파이프라인을 만든다.

**요구사항**:

1. **Golden Test Set 20건 설계** (`my_golden_tests.json`)
   - Accuracy 8건
   - Faithfulness 6건
   - Robustness 6건 (동의어 표현 변형)

2. **Faithfulness 측정 함수 개선**
   - 현재: 단순 문장 수 비율
   - 개선: 핵심 주장(claim) 단위로 측정

3. **Pairwise 비교 평가 구현**
   - v1 프롬프트 vs v2 프롬프트 비교
   - 위치 편향 제거 로직 포함

4. **결과 보고서 출력**
   - 카테고리별 pass_rate
   - 실패 케이스 상위 3건 원인 분석
   - 개선 권고 사항 1개 이상

**실행 방법**:
```bash
just you-do
```

**완료 기준**:
- 20건 중 15건 이상 통과 (pass_rate ≥ 0.75)
- Pairwise 비교에서 v2가 v1보다 우수하거나 동등
- 보고서 자동 출력

**막히면**: `solution/evaluate.py`에서 각 함수의 구현을 참조한다.

---

## 채점 기준

| 항목 | 배점 | 기준 |
|---|---|---|
| Golden Test Set 설계 | 30점 | 20건, 카테고리 균형, tolerance 합리적 |
| Faithfulness 측정 | 30점 | 프롬프트 명확, JSON 파싱, 점수 정확 |
| Pairwise 비교 | 20점 | 순서 무작위화, 신뢰도 판정 |
| 보고서 출력 | 20점 | 카테고리별 분석, 개선 권고 포함 |

---

## 참고 자료

- [RAGAS 공식 문서](https://docs.ragas.io/)
- [LLM-as-a-Judge 논문](https://arxiv.org/abs/2306.05685)
- `guide/day4-session1.md` — 평가 체계 설계 이론
