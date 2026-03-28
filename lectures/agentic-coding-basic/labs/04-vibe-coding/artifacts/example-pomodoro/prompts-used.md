# 사용한 프롬프트 기록

이 예시 프로젝트를 만들 때 실제로 사용한 프롬프트 순서.
바이브 코딩이 어떻게 진행되는지 참고할 수 있다.

---

## Prompt 1: AGENTS.md 작성 (직접 작성)

AGENTS.md는 직접 작성했다. 에이전트에게 주는 지시문이므로 팀이 먼저 합의하고 작성해야 한다.

```
# AGENTS.md 내용 직접 작성 — 생략 (파일 참고)
```

---

## Prompt 2: 프로젝트 구조 생성

```
AGENTS.md를 읽고 CLI 포모도로 타이머 프로젝트를 만들어줘.

지금은 빈 파일만 만들어도 돼. 각 파일 상단에 모듈 역할을 docstring으로만 써줘.
파일 구조:
- pomodoro.py (메인 진입점, argparse로 start/break/stats 명령 처리)
- timer.py (카운트다운 타이머)
- storage.py (세션 저장/불러오기, sessions.json)
- stats.py (통계 계산)
- test_pomodoro.py (테스트)
```

**결과**: 5개 파일의 뼈대 생성. 각 파일에 docstring과 빈 함수 시그니처.

---

## Prompt 3: storage.py 구현

```
storage.py를 구현해줘. AGENTS.md의 규칙을 따라줘.

요구사항:
- save_session(start_time, end_time, session_type, completed, filepath=DATA_FILE)
  → sessions.json에 추가 저장
- load_sessions(filepath=DATA_FILE) → 전체 세션 리스트 반환
- load_sessions_for_date(date_str, filepath=DATA_FILE) → 해당 날짜 세션만 반환
- filepath 파라미터: 테스트에서 임시 파일 경로를 주입할 수 있도록 기본값은 DATA_FILE

예외 처리:
- 파일 없음 → 빈 리스트 반환
- JSON 파싱 실패 → 경고 출력 후 빈 리스트 반환
```

**결과**: 완성된 storage.py. filepath 주입 패턴 덕분에 테스트가 쉬워졌다.

---

## Prompt 4: storage.py 테스트

```
test_pomodoro.py에 storage.py에 대한 unittest를 작성해줘.

테스트할 항목:
1. 세션 저장 후 1개 항목 존재 확인
2. 저장된 세션의 필수 필드 확인 (start_time, end_time, session_type, completed)
3. 여러 세션 저장 후 누적 확인
4. 파일 없을 때 빈 리스트 반환 확인
5. 손상된 JSON 파일일 때 빈 리스트 반환 확인
6. 날짜 필터(load_sessions_for_date) 동작 확인

주의: 각 테스트는 임시 파일(tempfile)을 사용하고, tearDown에서 삭제해줘.
```

**결과**: 6개 테스트 모두 통과. `python -m unittest test_pomodoro.TestStorage -v`

---

## Prompt 5: timer.py 구현

```
timer.py를 구현해줘.

요구사항:
- run_timer(duration_seconds, label, tick_fn=None) → (start_time, end_time, completed)
  - tick_fn이 None이면 time.sleep(1) 사용
  - tick_fn이 있으면 그것을 호출 (테스트 주입용)
  - KeyboardInterrupt 발생 시 completed=False 반환
- 카운트다운 출력: \r로 같은 줄 업데이트
  - 형식: [=========>         ] 18:32 남음
  - 진행률 바 너비: 20칸
- 완료 시 \a (터미널 벨) 출력

_render_progress_bar(elapsed, total, width=20) 함수를 별도로 만들어서
단위 테스트가 가능하게 해줘.
```

**결과**: tick_fn 주입 덕분에 실제 time.sleep 없이 테스트 가능.

---

## Prompt 6: timer.py 테스트 추가

```
test_pomodoro.py에 timer.py 테스트를 추가해줘.

1. _render_progress_bar 시작/완료 시점 형식 확인
2. tick_fn 주입으로 실제 sleep 없이 타이머 완료 확인
3. KeyboardInterrupt 발생 시 completed=False 반환 확인
   - tick_fn에서 2번째 호출 시 KeyboardInterrupt 발생시키는 방식
```

**결과**: 4개 테스트 추가. 실제 타이머 동작 없이 1초 안에 테스트 완료.

---

## Prompt 7: stats.py 구현

```
stats.py를 구현해줘.

요구사항:
- get_today_stats(filepath=None) → {focus_count, total_focus_minutes, break_count}
  - 오늘 날짜의 완료된 세션만 집계
- get_streak(filepath=None) → 오늘까지 집중 세션을 1개 이상 완료한 연속 일수
  - 오늘 세션이 없으면 0
- print_stats() → 통계를 보기 좋게 터미널 출력

filepath 파라미터: storage 함수에 그대로 전달 (테스트 주입용)
```

---

## Prompt 8: stats.py 테스트 추가

```
test_pomodoro.py에 stats.py 테스트를 추가해줘.

1. 세션 없을 때 모든 통계 0 확인
2. 완료/미완료 세션 구분 카운트 확인
3. 총 집중 시간(분) 정확성 확인
4. 오늘 세션 없을 때 streak=0 확인
5. 연속 3일 세션 있을 때 streak=3 확인

각 테스트는 임시 파일 사용. date_offset 파라미터로 날짜를 조정하는
_add_session 헬퍼 메서드를 만들어줘.
```

---

## Prompt 9: pomodoro.py (메인) 구현

```
pomodoro.py를 구현해줘.

argparse로 아래 명령어를 처리:
- python pomodoro.py start [--duration 초] → 집중 타이머 (기본 1500초=25분)
- python pomodoro.py break [--duration 초] → 휴식 타이머 (기본 300초=5분)
- python pomodoro.py stats → 오늘의 통계 출력

--duration 옵션: 테스트 시 짧은 값(예: 5초)으로 빠르게 확인 가능
타이머 완료 후 자동으로 세션 저장
```

---

## Prompt 10: 통합 테스트

```
모든 테스트를 실행해줘.
python -m unittest test_pomodoro -v

실패하는 테스트가 있으면 원인을 분석하고 수정해줘.
```

**결과**: 전체 테스트 통과. 총 14개 테스트.

---

## 총 프롬프트 수: 10개 (AGENTS.md 제외)
## 소요 시간: 약 35분
## 최종 테스트: 14개 모두 통과

---

## 배운 점

**잘 된 것**:
- `filepath` 파라미터 주입 패턴 덕분에 실제 파일 없이 테스트 가능
- `tick_fn` 주입으로 time.sleep 없이 타이머 테스트
- 기능 하나 구현 → 즉시 테스트 → 다음 기능 순서가 효과적

**안 된 것 (개선 가능)**:
- Prompt 3에서 처음에 filepath 주입 패턴을 요청하지 않아 나중에 리팩토링 필요했음
- AGENTS.md에 미리 "테스트 주입 가능하게 설계" 규칙을 넣었어야 함
