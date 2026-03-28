# Lab 03: 자기 수정 피드백 루프 구축

**세션**: Session 4 | **시간**: 25분 | **난이도**: 중급

## 학습 목표

- 에이전트의 비대화형(non-interactive) 실행 모드를 이해한다
- 테스트 실패 → 에이전트 수정 → 재검증 피드백 루프를 직접 구현한다
- 자동화 루프(Ralph 원리)가 왜 강력한지 체험한다

## 준비

```bash
# Python 3.8 이상 필요 (표준 라이브러리만 사용)
python3 --version

# 실습 디렉토리로 이동
cd labs/03-feedback-loop

# 환경 확인
just setup
```

---

## I DO (5분) — 강사 시연

### 1. 버그 확인: 테스트 3개가 실패합니다

```bash
just test
```

예상 출력:
```
FAIL: test_score_calculation_with_string_values
FAIL: test_case_insensitive_answer
FAIL: test_delete_cleans_stats

Ran 8 tests in 0.XXXs
FAILED (failures=3)
```

테스트가 정확히 3개 실패해야 정상입니다. 테스트 코드는 올바르고, 버그는 모두 `src/` 코드에 있습니다.

### 2. 에이전트가 자동으로 1개 버그를 수정하는 모습 시연

```bash
cd src

# 비대화형 모드로 에이전트 실행 (중요: 사람이 개입하지 않음)
opencode run "test_vocab.py를 실행하면 test_case_insensitive_answer가 실패합니다.
quiz.py의 check_answer() 함수를 분석하고 버그를 수정해주세요.
test_vocab.py는 수정하지 마세요."
```

수정 후 테스트 재실행:
```bash
python -m unittest test_vocab.TestCaseInsensitiveAnswer -v
```

**핵심 관찰**: 에이전트가 코드를 분석하고, 버그를 찾고, 수정까지 자동으로 수행했습니다. 이 과정을 루프로 돌리면 모든 버그를 자동으로 수정할 수 있습니다.

---

## WE DO (10분) — 함께 자동화 스크립트 완성

`src/auto_fix.sh` 템플릿에 TODO 부분을 함께 채워봅니다.

### 단계 1: 테스트 실행 추가

```bash
# TODO 1 자리에 다음을 추가
python -m unittest test_vocab -v 2>&1 | tee "$TEST_OUTPUT_FILE" | tee -a "$LOG_FILE"
TEST_EXIT_CODE=${PIPESTATUS[0]}
```

### 단계 2: 성공 조건 추가

```bash
# TODO 2, 3 자리에 다음을 추가
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "모든 테스트 통과! 완료."
    exit 0
fi
```

### 단계 3: 에이전트 호출 추가

```bash
# TODO 4 자리에 다음을 추가
opencode run "다음 테스트 실패를 분석하고 코드를 수정해주세요:
$(cat $TEST_OUTPUT_FILE)
test_vocab.py는 수정하지 마세요."
```

### 함께 첫 번째 버그 수정

이전에 시연한 quiz.py 버그를 초기화하고, 스크립트를 실행해봅니다:

```bash
# (강사가 버그를 다시 되돌린 경우)
bash auto_fix.sh
```

---

## YOU DO (10분) — 나머지 버그 자동화 루프로 수정

### 목표

완성된 `auto_fix.sh`를 사용하여 나머지 2개 버그를 자동으로 모두 수정합니다.

### 시작하기

```bash
cd src

# 현재 실패 상태 확인
python -m unittest test_vocab -v

# 자동 수정 루프 실행
bash auto_fix.sh
```

### 성공 기준

```bash
# 모든 테스트 통과 확인
python -m unittest test_vocab -v
# 결과: Ran 8 tests in 0.XXXs
#       OK
```

### 기록 양식

실습을 진행하면서 다음을 기록하세요:

| 항목 | 내용 |
|------|------|
| 총 시도 횟수 | ___ 회 |
| 버그 1 (stats.py) | 에이전트 분석: ___ / 수정 방법: ___ |
| 버그 2 (quiz.py) | 에이전트 분석: ___ / 수정 방법: ___ |
| 버그 3 (vocab.py) | 에이전트 분석: ___ / 수정 방법: ___ |
| 가장 흥미로운 점 | ___ |
| 한계나 문제점 | ___ |

### 세션 데이터로 피드백 루프 분석 (선택 사항)

비대화형 모드(`opencode run`)로 자동 수정을 실행한 경우, 세션 데이터에서 피드백 루프를 정량적으로 분석할 수 있다.

```bash
opencode session list
opencode export <session-id> > feedback-session.json
```

분석 포인트:
- **Bash 도구 호출 횟수**: 테스트를 몇 번 실행했는가? → 피드백 루프 반복 횟수
- **Edit → Bash 패턴**: 수정(Edit) 후 테스트(Bash) 실행이 몇 사이클 반복되었는가?
- **최종 성공까지 소요 시간**: 첫 번째 Bash 호출부터 마지막 성공적 Bash 호출까지

> 이 데이터는 "에이전트의 자기 수정 능력"을 정량적으로 평가하는 근거가 된다.
> 세션 추적 방법은 [부록: 세션 추적 가이드](../../guide/appendix-session-tracking.md)를 참고하라.

### 토론 주제

루프가 끝난 후 다음을 생각해보세요:
- 에이전트가 항상 올바른 버그를 찾았나요? 틀린 곳을 수정한 경우는?
- 몇 번 시도 만에 성공했나요? 왜 그런 차이가 생겼을까요?
- 이 루프를 실제 프로젝트에 적용한다면 어떤 조건이 필요할까요?

---

## 막혔을 때

### 힌트 보기

```bash
just hints
```

### 솔루션 확인

```bash
# 솔루션으로 테스트 전부 통과 확인
just test-solution

# 솔루션 코드 직접 확인
cat solution/vocab.py
cat solution/quiz.py
cat solution/stats.py
cat solution/auto_fix.sh
```

### 버그 요약

| 파일 | 버그 유형 | 위치 | 수정 방법 |
|------|----------|------|---------|
| `stats.py` | 타입 에러 | `calculate_score()` | `int(correct)` 변환 추가 |
| `quiz.py` | 로직 버그 | `check_answer()` | `.lower()` 변환 추가 |
| `vocab.py` | 데이터 무결성 | `delete_word()` | stats도 함께 삭제 |

---

## 정리

```bash
# 데이터 파일 정리
just clean
```
