# 아키텍처 문서

## 개요
북마크 관리 REST API — Python 표준 라이브러리만 사용하는 경량 웹 서버.

## 모듈 구조
```
round3/src/
├── app.py          # HTTP 서버 진입점, 라우팅, 응답 처리
├── models.py       # 데이터 모델 (Bookmark dataclass)
├── database.py     # JSON 파일 기반 저장소
├── validators.py   # 입력 유효성 검사
└── test_api.py     # 통합 테스트
```

## 의존성 그래프
```
app.py
  ├── models.py       (Bookmark 생성, to_dict 호출)
  ├── database.py     (CRUD 함수 호출)
  └── validators.py   (validate_bookmark_input 호출)

database.py
  └── models.py       (Bookmark.from_dict, .to_dict 호출)

validators.py
  └── (의존성 없음 — 순수 함수)

models.py
  └── (의존성 없음 — dataclass만)
```

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | /health | 헬스 체크 |
| GET | /bookmarks | 전체 목록 조회 |
| GET | /bookmarks/{id} | 단건 조회 |
| POST | /bookmarks | 생성 |
| PUT | /bookmarks/{id} | 수정 |
| DELETE | /bookmarks/{id} | 삭제 |

## 데이터 모델

### Bookmark
```json
{
  "id": "uuid4-string",
  "title": "문자열 (최대 200자, 필수)",
  "url": "http(s)://... (필수)",
  "description": "문자열 또는 null (선택)",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

## 저장소
- 파일: `bookmarks.json` (기본값, `BOOKMARK_DB` 환경 변수로 재정의 가능)
- 형식: JSON 배열, UTF-8 인코딩
- 동시성: 단일 프로세스 단일 스레드 가정 (잠금 없음)

## 에러 응답 형식
```json
{"error": "에러 메시지 (한국어)"}
```

## 확장 포인트
신규 필드를 추가할 때:
1. `Bookmark.to_dict()` + `Bookmark.from_dict()` 동시 수정
2. `validators.py`에 유효성 검사 추가
3. 필터링이 필요하면 `database.py`에 `get_by_<field>()` 함수 추가
4. `app.py`에 쿼리 파라미터 파싱 추가 (예: `?category=tech`)

## 쿼리 파라미터 파싱 패턴
```python
from urllib.parse import urlparse, parse_qs

parsed = urlparse(self.path)
params = parse_qs(parsed.query)
category = params.get("category", [None])[0]
```
