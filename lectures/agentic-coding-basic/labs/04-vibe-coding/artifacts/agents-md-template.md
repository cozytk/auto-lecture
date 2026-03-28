# AGENTS.md 템플릿

바이브 코딩 프로젝트에 적합한 AGENTS.md 템플릿.
이 파일을 복사해서 프로젝트 루트에 `AGENTS.md`로 저장하고, 내용을 수정해서 사용한다.

---

## 최소 템플릿 (빠르게 시작하고 싶을 때)

```markdown
# AGENTS.md

## 프로젝트 개요
[한 줄로 프로젝트 설명]

## 언어 및 환경
- Python 3.10+
- 표준 라이브러리만 사용 (외부 패키지 설치 금지)

## 테스트
- `python -m pytest` 또는 `python -m unittest discover`
- 새 기능 추가 시 테스트 필수

## 코딩 규칙
- 함수 하나는 한 가지 일만 한다
- 에러는 조용히 삼키지 말고 명확한 메시지로 출력한다
```

---

## 상세 템플릿 (더 나은 결과를 원할 때)

```markdown
# AGENTS.md

## 프로젝트 개요
[2~3줄로 앱의 목적과 주요 기능 설명]

## 기술 스택
- 언어: Python 3.10+
- 라이브러리: 표준 라이브러리만 (json, datetime, os, sys, time, unittest, csv)
- 테스트: unittest (또는 pytest)

## 프로젝트 구조
```
프로젝트명/
├── AGENTS.md
├── main.py         # 진입점, CLI 파싱
├── core.py         # 핵심 비즈니스 로직
├── storage.py      # 데이터 저장/불러오기
└── test_main.py    # 테스트
```

## 테스트 실행
```bash
python -m pytest                    # pytest 사용 시
python -m unittest discover         # unittest 사용 시
python -m unittest test_main        # 특정 파일만
```

## 코딩 규칙

### 코드 스타일
- 함수명: snake_case (예: `save_session`, `get_stats`)
- 클래스명: PascalCase (예: `SessionManager`)
- 상수: UPPER_SNAKE_CASE (예: `FOCUS_DURATION = 25`)
- 줄 길이: 최대 100자

### 함수 설계
- 함수 하나는 한 가지 일만 한다
- 함수 길이: 20줄 이하 권장
- 파라미터: 3개 이하 권장

### 에러 처리
- 파일 I/O는 항상 try/except로 감싼다
- 에러를 조용히 삼키지 않는다 — 반드시 사용자에게 알린다
- 예외 메시지는 한국어로 작성

### 데이터 저장
- JSON 파일 사용: `data.json`
- 파일이 없으면 기본값으로 초기화 (프로그램 중단 없이)
- 저장 전 데이터 유효성 검증

## CLI 인터페이스 규칙
- 명령어: `python main.py <command> [options]`
- 성공 출력: stdout
- 에러 출력: stderr
- 성공 시 exit code 0, 실패 시 exit code 1

## 테스트 작성 규칙
- 각 함수에 최소 1개 테스트
- 임시 파일 사용 시 tearDown에서 반드시 삭제
- 테스트명: `test_<기능>_<시나리오>` (예: `test_save_session_creates_file`)
- 엣지 케이스 포함: 빈 데이터, 잘못된 입력
```

---

## 시나리오별 추가 규칙 예시

### 포모도로 타이머용 추가 규칙
```markdown
## 타이머 규칙
- 실제 시간 대기(time.sleep)는 timer.py에만 존재
- 테스트 시 타이머 시간을 주입 가능하도록 설계 (기본값 25분, 테스트용 5초)
- 타이머 출력은 \r로 같은 줄 업데이트 (새 줄 출력 금지)
```

### 습관 트래커용 추가 규칙
```markdown
## 날짜 처리 규칙
- 날짜는 항상 ISO 8601 형식 사용: YYYY-MM-DD
- 현재 날짜는 datetime.date.today() 사용
- streak 계산 시 오늘 포함 여부를 명확히 주석으로 표시
```

### Markdown 변환기용 추가 규칙
```markdown
## 파싱 규칙
- 정규식 패턴은 PATTERN 상수로 분리 (인라인 사용 금지)
- 각 Markdown 요소는 독립적인 변환 함수로 분리
- 입력 파일이 없으면 명확한 에러 메시지 출력 후 종료
```

---

## AGENTS.md 작성 팁

1. **처음에 제약 조건 명시**: "표준 라이브러리만 사용"을 적어두면 에이전트가 외부 패키지를 설치하려 하지 않는다.

2. **파일 구조 미리 합의**: 구조를 AGENTS.md에 적어두면 에이전트가 일관된 파일명을 사용한다.

3. **테스트 명령어 명시**: 에이전트가 테스트 실행 방법을 알면 코드 작성 후 자동으로 테스트를 돌린다.

4. **너무 길게 쓰지 않기**: AGENTS.md가 지나치게 길면 에이전트가 중요한 규칙을 놓친다. 핵심만 간결하게.
