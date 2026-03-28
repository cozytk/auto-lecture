# Day 4 실습: Agent 성능 분석 및 개선

> 소요 시간: 약 85분
> 형태: Python 코드 실습

## 개요

Agent의 성능 저하를 진단하고, Prompt 버전 관리 및 A/B 테스트를 통해 체계적으로 성능을 개선한다.

## 사전 준비

```bash
pip install openai
```

```bash
export OPENAI_API_KEY="your-api-key"
```

## 디렉토리 구조

```
day4-performance-tuning/
├── README.md                              # 이 파일
├── src/
│   ├── i_do_diagnosis.py                 # I DO: 성능 저하 진단
│   ├── we_do_prompt_versioning.py        # WE DO: Prompt 버전 관리 + A/B 테스트
│   └── you_do_optimization.py            # YOU DO: 종합 성능 개선 파이프라인
└── solution/
    └── you_do_optimization.py            # YOU DO 정답 코드
```

---

## I DO (시연) - 15분

강사가 성능 저하를 진단하는 과정을 시연한다.

### 실행 방법

```bash
python src/i_do_diagnosis.py
```

### 학습 포인트

- 기준 메트릭(baseline)과 현재 메트릭 비교 방법
- 성능 하락 원인을 자동으로 분류하는 진단 코드
- 심각도에 따른 대응 우선순위 결정

---

## WE DO (함께) - 30분

전체가 함께 Prompt 버전 관리와 A/B 테스트를 구현한다.

### 진행 순서

1. PromptRegistry에 프롬프트 2개 버전(v1, v2)을 등록한다
2. v1은 기본 프롬프트, v2는 Few-shot 예시를 추가한 개선 버전
3. A/B 테스트를 실행하여 두 버전을 비교한다
4. 결과를 분석하여 승자를 결정한다

### 실행 방법

```bash
python src/we_do_prompt_versioning.py
```

---

## YOU DO (독립) - 40분

종합 성능 개선 파이프라인을 완성한다.

### 과제 내용

1. `src/you_do_optimization.py`의 `TODO` 부분을 완성한다
2. 전체 파이프라인 구현:
   - 진단: 메트릭 비교로 저하 원인 특정
   - 개선: Prompt 수정 적용
   - 검증: A/B 테스트로 개선 효과 확인
   - 리포트: Before/After 비교 출력
3. 자신의 Agent에 적용하여 실제 개선 결과를 확인한다

### 실행 방법

```bash
python src/you_do_optimization.py
```

### 완료 기준

- [ ] 진단 함수 구현 (baseline vs current 비교)
- [ ] Prompt 개선 버전 작성
- [ ] A/B 테스트 실행 및 결과 분석
- [ ] Before/After 비교 리포트 생성
- [ ] 개선 효과 수치로 확인

### 산출물

- 성능 개선 리포트 (Before/After 메트릭 비교)

### 막히면?

정답 코드는 `solution/you_do_optimization.py`에서 확인할 수 있다.
