# Day 4 실습: LangSmith 기반 모니터링 구축

> 소요 시간: 약 85분
> 형태: Python 코드 실습 (LangSmith 핵심)

## 개요

LangSmith를 활용하여 Agent의 실행을 추적(Trace)하고, 운영 메트릭을 수집하며, 이상 감지와 알럿을 설정한다.

## 사전 준비

```bash
pip install langsmith langchain langchain-openai openai
```

```bash
export OPENAI_API_KEY="your-api-key"
export LANGSMITH_API_KEY="your-langsmith-api-key"
export LANGSMITH_TRACING=true
export LANGSMITH_PROJECT="day4-monitoring-lab"
```

LangSmith 계정이 없으면 https://smith.langchain.com/ 에서 무료 가입한다.

## 디렉토리 구조

```
day4-langsmith-monitoring/
├── README.md                              # 이 파일
├── src/
│   ├── i_do_trace_setup.py               # I DO: LangSmith 기본 설정 및 Trace
│   ├── we_do_custom_trace.py             # WE DO: 커스텀 Trace 및 메트릭
│   └── you_do_monitoring.py              # YOU DO: 모니터링 대시보드 + 알럿
└── solution/
    └── you_do_monitoring.py              # YOU DO 정답 코드
```

---

## I DO (시연) - 15분

강사가 LangSmith 기본 설정과 Trace 수집을 시연한다.

### 실행 방법

```bash
python src/i_do_trace_setup.py
```

### 학습 포인트

- 환경 변수 설정만으로 자동 Trace 수집
- LangSmith 대시보드에서 Trace 확인하는 방법
- Trace의 계층 구조 (Root → Child spans)
- 실행 시간, 토큰 사용량, 에러 정보 확인

### 확인 사항

실행 후 https://smith.langchain.com/ 에서:
1. 프로젝트 "day4-monitoring-lab" 선택
2. Runs 탭에서 방금 실행한 Trace 확인
3. Trace를 클릭하여 세부 정보 (입력, 출력, 시간) 확인

---

## WE DO (함께) - 30분

전체가 함께 커스텀 Trace와 메트릭 수집을 구현한다.

### 진행 순서

1. `@traceable` 데코레이터로 커스텀 함수를 Trace에 포함시킨다
2. 메타데이터를 태깅하여 검색/필터링을 용이하게 한다
3. LangSmith Python 클라이언트로 Trace 데이터를 프로그래매틱하게 조회한다
4. 일일 메트릭(성공률, 지연시간, 토큰 사용량)을 산출한다

### 실행 방법

```bash
python src/we_do_custom_trace.py
```

---

## YOU DO (독립) - 40분

모니터링 대시보드와 알럿을 설정한다.

### 과제 내용

1. `src/you_do_monitoring.py`의 `TODO` 부분을 완성한다
2. 구현 항목:
   - 일일 운영 메트릭 자동 산출 (성공률, p50/p95 지연시간, 토큰, 비용)
   - Guardrail 구현 (프롬프트 인젝션 탐지 + PII 마스킹)
   - 에러 패턴 분석 (유사 에러 그루핑)
   - 알럿 조건 설정 (성공률 하락, 지연시간 증가)

### 실행 방법

```bash
python src/you_do_monitoring.py
```

### 완료 기준

- [ ] LangSmith Trace가 정상 수집되는지 확인
- [ ] 커스텀 함수가 Trace 계층에 포함되는지 확인
- [ ] 메트릭 산출 함수 구현 (성공률, 지연시간, 토큰)
- [ ] Guardrail 동작 확인 (인젝션 차단, PII 마스킹)
- [ ] 알럿 조건이 올바르게 트리거되는지 확인

### 산출물

- 모니터링 메트릭 리포트 (콘솔 출력)
- Guardrail 동작 확인 로그

### 막히면?

정답 코드는 `solution/you_do_monitoring.py`에서 확인할 수 있다.
