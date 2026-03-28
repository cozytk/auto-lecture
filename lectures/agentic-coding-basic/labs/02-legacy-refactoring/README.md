# Lab 02: 레거시 코드 리팩토링 + 테스트 생성

**세션**: Session 3 | **소요 시간**: 40분 | **난이도**: 중급

## 학습 목표

- 에이전트를 활용해 지저분한 레거시 코드를 빠르게 리팩토링한다
- 에이전트가 생성한 테스트의 **품질 문제(동어반복 테스트)**를 직접 식별한다
- AGENTS.md에 리팩토링 규칙을 추가해 에이전트 동작을 제어하는 법을 익힌다
- 에이전트의 강점(빠른 구조 개선)과 한계(테스트 의미 검증 부재)를 체험한다

## 실습 구조

```
02-legacy-refactoring/
├── README.md               # 이 파일
├── Justfile                # 실습 명령어 모음
├── src/
│   ├── legacy_analyzer.py  # 의도적으로 지저분한 레거시 코드 (실습 대상)
│   └── data/
│       ├── sample_data.csv # 정상 데이터 (25행)
│       ├── edge_case.csv   # 결측값/이상치 포함 데이터
│       └── empty.csv       # 빈 파일 (헤더만)
├── solution/
│   ├── config.py           # 매직 넘버 → 설정으로 추출
│   ├── main.py             # 진입점
│   ├── analyzer/
│   │   ├── __init__.py
│   │   ├── reader.py       # CSV 읽기
│   │   ├── statistics.py   # 통계 계산
│   │   ├── outlier.py      # 이상치 탐지
│   │   └── reporter.py     # 출력 및 저장
│   └── test_analyzer.py    # 포괄적 테스트 (17개)
└── artifacts/
    └── quality-checklist.md  # 에이전트 테스트 품질 평가 체크리스트
```

---

## I DO: 강사 시연 (10분)

### 목표
레거시 코드에 에이전트가 테스트를 생성하면 어떤 문제가 생기는지 보여준다.

### 시연 순서

**1. 레거시 코드 살펴보기**

```bash
just run   # 실제로 동작하는 코드 확인
```

`src/legacy_analyzer.py`를 열고 문제점들을 짚어본다:
- 하나의 `analyze_data()` 함수에 모든 로직 (약 200줄)
- `scoreList`, `avg2`, `total3` 같은 일관성 없는 네이밍
- 평균/중앙값/표준편차 계산 블록이 score, salary, age에 걸쳐 3번 중복
- `85`, `90`, `1.5` 같은 매직 넘버
- 에러 핸들링 전혀 없음 (`just run-empty` 실행 → ZeroDivisionError 발생)

**2. 에이전트에게 테스트 요청**

에이전트(Opencode)에서 다음 프롬프트를 실행한다:

```
src/legacy_analyzer.py 파일에 대한 단위 테스트를 작성해줘.
파일명은 test_legacy.py로 저장해줘.
```

**3. 생성된 테스트의 문제점 찾기**

에이전트가 생성한 테스트에서 아래 패턴을 찾아 학생들에게 보여준다:

```python
# 동어반복 테스트 예시 (에이전트가 자주 생성하는 패턴)
def test_analyze_runs():
    analyze_data("data/sample_data.csv")  # 단순 실행만 확인, 결과 검증 없음

def test_file_loaded():
    analyze_data("data/sample_data.csv")
    assert results != {}  # 전역변수 참조, 실제 값 검증 없음
```

**핵심 메시지**: 에이전트는 "코드가 실행된다"는 테스트는 잘 만들지만,
"비즈니스 요구사항을 올바르게 구현했는가"를 검증하는 테스트는 스스로 만들기 어렵다.

---

## WE DO: 함께 실습 (15분)

### 목표
에이전트에게 리팩토링을 요청하고, AGENTS.md로 품질을 제어한다.

### 단계별 진행

**Step 1: AGENTS.md 작성 (5분)**

`src/` 디렉토리에 `AGENTS.md` 파일을 직접 작성한다:

```markdown
# 리팩토링 규칙

## 코드 스타일
- 모든 변수명은 snake_case를 사용한다
- 함수 하나는 하나의 역할만 담당한다 (Single Responsibility)
- 매직 넘버는 반드시 이름 있는 상수로 추출한다

## 에러 핸들링
- 파일 읽기는 반드시 try-except로 감싼다
- 빈 데이터에 대해 ValueError를 발생시킨다

## 테스트 요구사항
- 단순 실행 확인이 아닌 예상값을 하드코딩해서 검증한다
- 엣지 케이스(빈 파일, 결측값)를 반드시 테스트한다
- assert 메시지에 예상값과 실제값을 포함한다
```

**Step 2: 에이전트에게 리팩토링 요청 (5분)**

```
AGENTS.md의 규칙을 따라서 legacy_analyzer.py를 리팩토링해줘.
다음 구조로 분리해:
- analyzer/reader.py: CSV 읽기
- analyzer/statistics.py: 통계 계산
- analyzer/outlier.py: 이상치 탐지
- analyzer/reporter.py: 출력
- config.py: 설정값
- main.py: 진입점
```

**Step 3: 테스트 실행 및 확인 (5분)**

```bash
# 리팩토링 전 레거시 코드 실행
just run

# 리팩토링 후 솔루션 실행 — 같은 결과인지 확인
just run-solution

# 테스트 통과 확인
just test
```

결과를 나란히 비교하며 **같은 분석 결과**가 나오는지 확인한다.

### 세션 추적으로 에이전트 분석 전략 관찰 (선택 사항)

세션을 내보내면 에이전트가 레거시 코드를 어떤 순서로 분석했는지 확인할 수 있다.

```bash
opencode session list
opencode export <session-id> > legacy-session.json
```

확인 포인트:
- 에이전트가 **어떤 파일을 먼저 읽었는가?** (테스트 파일? 소스 코드?)
- AGENTS.md 규칙이 에이전트의 **탐색 순서**에 영향을 주었는가?
- 에이전트가 테스트를 **몇 번 실행**했는가? (피드백 루프 횟수)

> 세션 추적 방법은 [부록: 세션 추적 가이드](../../guide/appendix-session-tracking.md)를 참고하라.

---

## YOU DO: 독립 실습 (15분)

### 과제 1: 에이전트가 놓친 엣지 케이스 추가

`solution/test_analyzer.py`를 열고, 에이전트가 놓쳤을 법한 테스트를 직접 추가한다.

추가해야 할 테스트:

```python
# 힌트 1: 모든 값이 같을 때 표준편차는 0이어야 한다
def test_compute_stats_동일값_표준편차_0():
    pass  # 직접 구현

# 힌트 2: 홀수 개 데이터의 중앙값 정확성
def test_compute_stats_홀수개_중앙값():
    pass  # 직접 구현

# 힌트 3: 부서가 하나뿐인 데이터의 그룹화
def test_group_by_category_단일부서():
    pass  # 직접 구현
```

추가 후 테스트를 실행해 통과하는지 확인:
```bash
just test
```

### 과제 2: 커스텀 리뷰어 에이전트 설정

`.opencode/agents/reviewer.md` 또는 에이전트 설정 파일을 만들어,
리팩토링 결과를 자동으로 검토하는 리뷰어 에이전트를 구성한다.

리뷰어가 확인할 항목 예시:
- 매직 넘버가 남아있지 않은가?
- 각 함수가 20줄 이내인가?
- 에러 핸들링이 모든 IO 작업에 적용되었는가?

에이전트에게 `@reviewer 이 리팩토링 결과를 검토해줘`를 요청하고 결과를 확인한다.

### 완료 기준

- [ ] 추가한 테스트 3개가 모두 통과한다
- [ ] 커스텀 리뷰어 에이전트가 리팩토링 결과를 검토했다
- [ ] `artifacts/quality-checklist.md`로 에이전트 생성 테스트를 직접 평가했다

---

## 참고: 레거시 코드의 의도적 문제점 목록

| 문제 | 위치 | 리팩토링 후 |
|------|------|------------|
| 단일 거대 함수 | `analyze_data()` 전체 | 4개 모듈로 분리 |
| camelCase 변수 | `scoreList`, `avg2`, `total3` | `score_values`, `score_mean` 등 |
| 중복 코드 | 평균/중앙값/표준편차 3번 반복 | `compute_stats()` 함수 1개 |
| 매직 넘버 | `1.5`, `0.25`, `0.75`, `85`, `90` | `config.py`의 상수 |
| 에러 핸들링 없음 | 파일 읽기, 형변환 | try-except + ValueError |
| 전역 변수 | `data`, `results`, `fileName` | 함수 반환값으로 대체 |
| 오래된 주석 | `# 2019년 인턴이 작성` | 타입힌트 + 독스트링 |

---

## 빠른 명령어 참고

```bash
just setup          # 환경 확인
just run            # 레거시 코드 실행
just run-edge       # 엣지 케이스 실행
just run-empty      # 빈 파일 실행 (에러 발생)
just run-solution   # 솔루션 코드 실행
just test           # 테스트 실행
just compare        # 레거시 vs 솔루션 출력 비교
just stats          # 코드 통계 (줄 수)
just clean          # 결과 파일 정리
```
