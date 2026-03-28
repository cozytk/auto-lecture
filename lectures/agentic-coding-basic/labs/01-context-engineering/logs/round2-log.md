# Round 2 세션 로그: 기본 AGENTS.md 있음

> **세션 URL**: https://opncd.ai/share/g4Y9ES4v
> **조건**: `round2/` 디렉토리 — AGENTS.md (코딩 컨벤션 + 테스트 규칙) 제공
> **사용 도구**: OpenCode (Claude)
> **총 소요 시간**: ~105초
> **토큰 사용량**: 35,483개

---

## 사용자 요청 (프롬프트)

```
북마크에 category 필드를 추가하고, 카테고리별 필터링 API를 만들어줘.

요구사항:
- Bookmark 모델에 category 필드 추가 (선택 필드, 기본값 None)
- POST /bookmarks 시 category 값 저장 가능
- GET /bookmarks?category=tech 처럼 쿼리 파라미터로 필터링 가능
- 테스트 추가
```

---

## AGENTS.md에 명시된 규칙

Round 2에는 다음 규칙이 포함된 `AGENTS.md`가 제공되었다:

| 규칙 카테고리 | 주요 내용 |
|--------------|-----------|
| 에러 핸들링 | `{"error": "메시지"}` 형태, 400/404/500 코드 구분, 빈 except 금지 |
| 함수 스타일 | Google 스타일 docstring, 반환 타입 힌트 필수, 단일 책임 |
| 코드 구조 | models=데이터, database=저장소, validators=유효성, app=HTTP |
| 로깅 | `print()` 대신 `logging` 모듈, 포맷: `%(asctime)s [%(levelname)s] %(message)s` |
| 테스트 | 성공/실패 케이스 모두, 독립적 테스트, 함수명 `test_<동작>_<조건>` 패턴 |
| 신규 기능 체크리스트 | models → validators → database → app → test_api 순서 |

---

## 에이전트 행동 흐름

### 1단계: 계획 수립

에이전트가 요청을 받고 **5개 작업 항목의 TODO 리스트**를 먼저 생성했다:
1. 현재 구조 검사
2. 모델/DB 계층 수정
3. 유효성 검사(validators) 수정
4. 핸들러(app) 수정
5. 테스트 추가 및 검증

> Round 1과 비교: Round 1은 계획 없이 바로 파일 탐색에 착수한 반면, Round 2는 AGENTS.md의 "신규 기능 추가 시 체크리스트"에 영향을 받아 체계적으로 계획을 세웠다.

### 2단계: 파일 탐색

`glob` 도구로 프로젝트 파일 5개 발견:
- `test_api.py`, `app.py`, `validators.py`, `database.py`, `models.py`

**경로 오류 발생**: 처음에 `/round2/` 경로로 접근 시도 → 실패 → `/round2/src/`로 수정하여 재시도

### 3단계: 파일 순차 읽기

4개 소스 파일을 순차적으로 읽으며 기존 구조 파악:
- **models.py** (15줄): `category` 필드 없음 확인
- **database.py** (71줄): 필터링 함수 부재 확인
- **validators.py**: URL/제목 검증만 존재 확인
- **app.py**: 부분 읽기

### 4~9단계: 파일 수정 (AGENTS.md 체크리스트 순서 준수)

AGENTS.md의 "신규 기능 추가 시 체크리스트"에 따라 **models → validators → database → app** 순서로 수정:

### 10단계: 테스트 추가 및 검증

테스트 코드를 추가하고 실행하여 통과 확인.

---

## 파일별 변경 내역

### `models.py` — category 필드 추가 (+4줄)

```python
@dataclass
class Bookmark:
    title: str
    url: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = None
    category: Optional[str] = None  # 추가
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
```

- `to_dict()`에 `"category": self.category` 추가
- `from_dict()`에 `category=data.get("category")` 추가

---

### `validators.py` — category 유효성 검사 추가 (+25줄)

**Round 1과 가장 큰 차이점**: Round 1에서는 `validators.py`를 수정하지 않았지만, Round 2에서는 AGENTS.md의 체크리스트(`validators.py에 유효성 검사 추가`)와 코드 구조 규칙(`validators.py: 유효성 검사만`)에 따라 검증 함수를 추가했다.

```python
def validate_category(category: Optional[str]) -> Tuple[bool, Optional[str]]:
    """카테고리 유효성 검사.

    Args:
        category: 검사할 카테고리 문자열 또는 None

    Returns:
        (valid, error_message) 튜플. 유효하면 (True, None).
    """
    if category is None:
        return True, None
    if not isinstance(category, str):
        return False, "category는 문자열이어야 합니다"
    if not category.strip():
        return False, "category는 비어 있을 수 없습니다"
    if len(category) > 100:
        return False, "category는 100자 이하여야 합니다"
    return True, None
```

`validate_bookmark_input()`에도 category 검사 통합 + 로깅 추가:
```python
ok, err = validate_category(data.get("category"))
if not ok:
    logger.error("유효성 검사 실패: %s", err)
    return False, err
```

---

### `database.py` — 카테고리 필터 함수 추가 (+6줄)

```python
def get_all_by_category(category: str) -> List[Bookmark]:
    """카테고리로 필터링한 북마크 목록을 반환한다."""
    return [bookmark for bookmark in get_all() if bookmark.category == category]
```

AGENTS.md 규칙에 따른 추가 변경:
- `import logging` 및 `logger = logging.getLogger(__name__)` 추가
- 모든 public 함수에 **Google 스타일 docstring** 추가
- `create()`, `update()`, `delete()`에 `logger.info()` 로깅 추가

---

### `app.py` — GET 필터링 + logging 전환 (+13줄, -5줄)

**로깅 전환** (AGENTS.md: `print() 대신 logging 모듈 사용`):
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)
```

**GET /bookmarks 필터링**:
```python
query = parse_qs(parsed.query)
category = query.get("category", [None])[0]
if category is None:
    bookmarks = database.get_all()
else:
    bookmarks = database.get_all_by_category(category)
```

**모든 public 함수에 Google 스타일 docstring 추가** (json_response, parse_body, run 등)

---

### `test_api.py` — 테스트 대폭 확장 (+83줄, -18줄)

AGENTS.md 규칙에 따른 변경:
- **함수명 패턴 `test_<동작>_<조건>` 준수**:
  - `test_health` → `test_health_returns_ok`
  - `test_create_and_list` → `test_create_bookmark_success`, `test_list_bookmarks_returns_all`
  - `test_crud` → 개별 테스트로 분리
- **성공/실패 케이스 모두 테스트**:
  - `test_create_bookmark_missing_title_returns_400`
  - `test_create_bookmark_missing_url_returns_400`
  - `test_create_bookmark_invalid_url_returns_400`
  - `test_get_bookmark_not_found_returns_404`
  - `test_update_bookmark_not_found_returns_404`
  - `test_delete_bookmark_not_found_returns_404`

**신규 카테고리 테스트**:
```python
def test_create_bookmark_with_category_success(self):
    status, body = api("POST", "/bookmarks", {
        "title": "Python 공식 문서",
        "url": "https://docs.python.org",
        "category": "tech",
    })
    self.assertEqual(status, 201)
    self.assertEqual(body["category"], "tech")

def test_list_bookmarks_filters_by_category(self):
    # tech, food, 미분류 북마크 3개 생성 후
    status, body = api("GET", "/bookmarks?category=tech")
    self.assertEqual(status, 200)
    self.assertEqual(len(body), 1)
    self.assertEqual(body[0]["category"], "tech")
```

---

## 변경 파일 요약

| 파일 | 변경 사항 | 줄 수 변경 |
|------|-----------|-----------|
| `models.py` | category 필드, to_dict, from_dict 추가 | +4 |
| `validators.py` | `validate_category()` 함수, logging, docstring | +25 |
| `database.py` | `get_all_by_category()`, logging, docstring | +6 |
| `app.py` | parse_qs 필터링, logging 전환, docstring | +13, -5 |
| `test_api.py` | 카테고리 테스트 + 실패 케이스 + 함수명 패턴 개선 | +83, -18 |

---

## Round 1 vs Round 2 비교

| 관찰 항목 | Round 1 (규칙 없음) | Round 2 (AGENTS.md) |
|-----------|---------------------|---------------------|
| **첫 행동** | 바로 파일 탐색 | TODO 리스트(계획) 먼저 수립 |
| **수정 순서** | 자유 순서 | AGENTS.md 체크리스트 순서 (models → validators → database → app → test) |
| **validators.py 수정** | 미수정 (category 검증 없음) | `validate_category()` 추가 (1-100자, 문자열 검사) |
| **docstring** | 미추가 | Google 스타일 docstring 전체 적용 |
| **logging** | 기존 `print()` 유지 | `logging` 모듈로 전환, 포맷 규칙 준수 |
| **테스트 함수명** | `test_create_bookmark_with_category` | `test_create_bookmark_with_category_success` (패턴 준수) |
| **테스트 범위** | 성공 케이스 중심 (2건 추가) | 성공 + 실패 케이스 (6건 이상 추가) |
| **에러 핸들링** | 기존 패턴 답습 | `logger.error()` 로깅 추가 |

---

## AGENTS.md 규칙 준수 체크

| AGENTS.md 규칙 | 준수 여부 | 비고 |
|----------------|-----------|------|
| `{"error": "메시지"}` 에러 응답 형식 | ✅ 준수 | 기존 패턴 유지 |
| 한국어 에러 메시지 | ✅ 준수 | "category는 문자열이어야 합니다" 등 |
| Google 스타일 docstring | ✅ 준수 | 모든 public 함수에 적용 |
| 반환 타입 힌트 | ✅ 준수 | `-> None`, `-> Tuple[bool, Optional[str]]` 등 |
| `logging` 모듈 사용 (`print` 대체) | ✅ 준수 | `logging.basicConfig()` + `logger.info/error` |
| 로그 포맷 `%(asctime)s [%(levelname)s] %(message)s` | ✅ 준수 | `app.py`에 설정 |
| 테스트 함수명 `test_<동작>_<조건>` | ✅ 준수 | 기존 테스트명도 리네이밍 |
| 성공/실패 케이스 모두 테스트 | ✅ 준수 | 404, 400 실패 케이스 추가 |
| 신규 기능 체크리스트 순서 | ✅ 준수 | models → validators → database → app → test |

---

## 핵심 관찰

1. **계획 수립 행동 변화**: AGENTS.md의 체크리스트가 에이전트의 작업 계획에 직접 반영되었다
2. **validators.py 수정**: Round 1에서 완전히 누락된 유효성 검사가 Round 2에서는 체크리스트 덕분에 자연스럽게 추가되었다
3. **코드 품질 전반 향상**: docstring, logging, 테스트 커버리지 모두 AGENTS.md 규칙에 맞춰 개선
4. **경로 오류**: 파일 경로 탐색에서 한 번 실패 후 재시도 — 컨텍스트에 디렉토리 구조 정보가 없었기 때문
5. **테스트 구조 개선**: 단순 CRUD 통합 테스트가 개별 성공/실패 테스트로 분리되어 디버깅 용이성 향상
