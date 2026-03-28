# 프로젝트 규칙 (AGENTS.md)

## 프로젝트 개요
북마크 관리 REST API. Python 표준 라이브러리만 사용하는 경량 웹 서버.

## 코딩 컨벤션

### 에러 핸들링
- 모든 HTTP 에러 응답은 `{"error": "메시지"}` 형태를 사용한다
- 400: 입력 유효성 오류 / 404: 리소스 없음 / 500: 서버 오류
- 예외는 절대 무시하지 않는다 (빈 except 블록 금지)

### 함수 스타일
- 모든 public 함수에 Google 스타일 docstring을 작성한다
- 반환 타입을 명시한다 (type hint 필수)
- 함수 하나는 하나의 역할만 한다

### 코드 구조
- `models.py`: 데이터 모델만 (비즈니스 로직 없음)
- `database.py`: 저장소 접근만 (HTTP 로직 없음)
- `validators.py`: 유효성 검사만 (저장소 접근 없음)
- `app.py`: HTTP 라우팅 + 응답 처리

### 로깅
- `print()` 대신 표준 `logging` 모듈을 사용한다
- 로그 포맷: `%(asctime)s [%(levelname)s] %(message)s`
- 요청 로그: `INFO`, 에러 로그: `ERROR`

## 테스트 규칙
- 모든 API 엔드포인트에 테스트가 있어야 한다
- 성공 케이스와 실패 케이스를 모두 테스트한다
- 테스트는 독립적이어야 한다 (setUp에서 DB 초기화)
- 테스트 함수명: `test_<동작>_<조건>` 패턴

## 신규 기능 추가 시 체크리스트
- [ ] `models.py`에 데이터 모델 변경 반영
- [ ] `validators.py`에 유효성 검사 추가
- [ ] `database.py`에 저장소 함수 추가
- [ ] `app.py`에 라우트 핸들러 추가
- [ ] `test_api.py`에 테스트 추가
