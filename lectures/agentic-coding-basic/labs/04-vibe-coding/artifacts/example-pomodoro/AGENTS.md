# AGENTS.md

## 프로젝트 개요
CLI 포모도로 타이머. 25분 집중 / 5분 휴식 사이클을 관리하고, 세션을 JSON에 기록해 통계를 제공한다.

## 언어 및 환경
- Python 3.10+
- 표준 라이브러리만 사용 (json, datetime, time, sys, os, unittest, argparse)
- 외부 패키지 설치 금지

## 프로젝트 구조
```
example-pomodoro/
├── AGENTS.md
├── pomodoro.py       # 메인 진입점, CLI 파싱
├── timer.py          # 타이머 로직 (카운트다운, 출력)
├── storage.py        # 세션 저장/불러오기 (sessions.json)
├── stats.py          # 통계 계산
└── test_pomodoro.py  # 자동화 테스트
```

## 테스트 실행
```bash
python -m pytest test_pomodoro.py -v
# 또는
python -m unittest test_pomodoro -v
```

## 코딩 규칙

### 코드 스타일
- 함수명: snake_case
- 상수: UPPER_SNAKE_CASE (예: FOCUS_DURATION = 25)
- 줄 길이: 100자 이하

### 타이머
- time.sleep()은 timer.py에만 사용
- 타이머 지속 시간은 파라미터로 주입 가능하게 설계 (테스트 용이성)
- 카운트다운 출력은 `\r`로 같은 줄 업데이트 (새 줄 금지)
- 형식: `[=========>         ] MM:SS 남음`

### 데이터 저장
- sessions.json 파일이 없거나 손상됐을 때 빈 리스트로 초기화
- 저장 형식: ISO 8601 날짜/시간 문자열

### 에러 처리
- 파일 I/O는 try/except로 감싸고 사용자에게 한국어로 알린다
- 에러 시 sys.exit(1)로 종료

### 테스트
- 임시 파일 사용 시 tearDown에서 반드시 삭제
- 실제 타이머(time.sleep) 호출 없이 테스트 가능해야 함
- 테스트명: test_<기능>_<시나리오>
