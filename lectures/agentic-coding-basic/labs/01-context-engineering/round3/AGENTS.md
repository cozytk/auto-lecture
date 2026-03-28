# 프로젝트 규칙 (AGENTS.md) — 풍부한 컨텍스트 버전

## 프로젝트 개요
북마크 관리 REST API. Python 표준 라이브러리만 사용하는 경량 웹 서버.
아키텍처 상세는 `architecture.md` 참조. 코드 예시는 `examples/` 참조.

## 핵심 설계 원칙
1. **표준 라이브러리만** — pip install 없음. `http.server`, `json`, `logging`, `dataclasses`, `uuid` 사용.
2. **계층 분리** — 각 모듈은 하나의 책임만 가진다. 레이어 간 의존성은 단방향(app → validators/database → models).
3. **일관된 응답 형태** — 성공: `{"field": value}`, 에러: `{"error": "메시지"}`.
4. **한국어 에러 메시지** — 모든 에러 메시지는 한국어로 작성한다.

## 아키텍처 (요약)
```
클라이언트 ──► app.py (HTTP 라우팅)
                    ├── validators.py (입력 검사)
                    ├── database.py (저장소)
                    └── models.py (데이터 모델)
```
전체 설명: `architecture.md`

## 코딩 컨벤션

### 에러 핸들링
```python
# ✅ 올바른 방식 — examples/error_handling.py 참조
ok, err = validators.validate_bookmark_input(data)
if not ok:
    json_response(self, 400, {"error": err})
    return

# ❌ 금지 — 빈 except 블록
try:
    ...
except Exception:
    pass
```

### 함수 스타일
- 모든 public 함수: Google 스타일 docstring + 타입 힌트 필수
- 예시: `examples/docstring_style.py`

### 로깅
```python
# ✅ 올바른 방식
import logging
logger = logging.getLogger(__name__)
logger.info("북마크 생성: id=%s title=%s", bookmark.id, bookmark.title)

# ❌ 금지
print("북마크 생성:", bookmark.id)
```
로그 포맷: `%(asctime)s [%(levelname)s] %(message)s`

### HTTP 응답 상태 코드
| 상황 | 상태 코드 |
|------|-----------|
| 생성 성공 | 201 |
| 조회/수정/삭제 성공 | 200 |
| 입력 유효성 오류 | 400 |
| 리소스 없음 | 404 |
| 서버 내부 오류 | 500 |

## 데이터 모델 컨벤션

### Bookmark 필드 규칙
- `id`: UUID4 문자열, 생성 시 자동 부여, 수정 불가
- `created_at`: ISO 8601 형식, 생성 시 자동 부여, 수정 불가
- `updated_at`: ISO 8601 형식, 수정 시마다 갱신
- 새 필드 추가 시: `to_dict()`, `from_dict()` 동시 수정 필수

### 신규 필드 추가 패턴
```python
# models.py — examples/add_field.py 참조
@dataclass
class Bookmark:
    # 기존 필드...
    new_field: Optional[str] = None  # 새 필드는 Optional로 기본값 None

    def to_dict(self) -> dict:
        return {
            # 기존 필드...
            "new_field": self.new_field,  # 추가
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Bookmark":
        return cls(
            # 기존 필드...
            new_field=data.get("new_field"),  # 추가 (get으로 하위호환 유지)
        )
```

## 테스트 규칙
- 모든 API 엔드포인트: 성공/실패 케이스 모두 테스트
- 테스트 함수명: `test_<동작>_<조건>_<기댓값>` 패턴
  - 예: `test_create_bookmark_missing_title_returns_400`
- `setUp`에서 DB 파일 삭제 (독립성 보장)
- 테스트 DB: `os.environ["BOOKMARK_DB"] = "test_bookmarks.json"`

### 신규 기능 테스트 체크리스트
- [ ] 정상 케이스 (201/200)
- [ ] 필수 필드 누락 (400)
- [ ] 잘못된 형식 (400)
- [ ] 존재하지 않는 리소스 (404)
- [ ] 필터링이 있으면: 해당 조건 테스트

## 신규 기능 추가 순서 (의무)
1. `models.py` — 데이터 모델에 필드 추가
2. `validators.py` — 유효성 검사 추가
3. `database.py` — 저장소 함수 추가 (필요 시)
4. `app.py` — 라우트 핸들러 추가
5. `test_api.py` — 테스트 추가
6. README curl 예시 업데이트

## 금지 사항
- `flask`, `fastapi`, `requests` 등 외부 패키지 import 금지
- `print()` 로깅 금지 (logging 모듈 사용)
- 빈 except 블록 금지
- 하드코딩된 포트 금지 (`PORT = 8000` 상수 사용)
