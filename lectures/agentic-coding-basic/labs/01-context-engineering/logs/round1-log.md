# Round 1 세션 로그: AGENTS.md 없음

> **세션 URL**: https://opncd.ai/share/yCA9ul6e
> **조건**: `round1/` 디렉토리 — AGENTS.md 없이 코드만 제공
> **사용 도구**: OpenCode (Claude)

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

## 에이전트 행동 흐름

### 1단계: 코드 탐색

AGENTS.md가 없으므로 에이전트가 **코드를 직접 읽어 구조를 파악**해야 했다.
기존 코드 파일(models.py, database.py, app.py, test_api.py, validators.py)을 순회하며 패턴을 파악한 뒤 구현에 착수했다.

### 2단계: 구현

에이전트가 수정한 파일과 변경 내용:

---

#### `models.py` — Bookmark 모델에 `category` 필드 추가

```python
@dataclass
class Bookmark:
    title: str
    url: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = None
    category: Optional[str] = None  # 새로 추가
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
```

- `to_dict()` 메서드에 `"category": self.category` 추가
- `from_dict()` 메서드에 `category=data.get("category")` 추가

**변경량**: +4줄

---

#### `database.py` — 카테고리별 필터 함수 추가

```python
def get_all_by_category(category: str) -> List[Bookmark]:
    return [bookmark for bookmark in get_all() if bookmark.category == category]
```

**변경량**: +5줄

---

#### `app.py` — GET 쿼리 파라미터 필터링 + POST/PUT에 category 처리

**GET /bookmarks 엔드포인트:**
- `urllib.parse`에서 `parse_qs` import 추가
- 쿼리 파라미터 추출: `category = query.get("category", [None])[0]`
- category가 None이면 전체 조회, 있으면 `database.get_all_by_category()` 호출

**POST /bookmarks 엔드포인트:**
- Bookmark 생성 시 `category=data.get("category")` 추가

**PUT /bookmarks/{id} 엔드포인트:**
- 업데이트 시 `existing.category = data.get("category", existing.category)` 추가

**변경량**: +19줄, -6줄

---

#### `test_api.py` — 테스트 케이스 추가 + 기존 코드 개선

새로 추가된 테스트:

```python
def test_create_bookmark_with_category(self):
    """category를 포함한 북마크 생성 테스트"""
    status, body = api(
        "POST",
        "/bookmarks",
        {"title": "Tech", "url": "https://tech.com", "category": "tech"},
    )
    self.assertEqual(status, 201)
    self.assertEqual(body["category"], "tech")

def test_list_bookmarks_filtered_by_category(self):
    """여러 카테고리 북마크 생성 후 필터링 테스트"""
    api("POST", "/bookmarks",
        {"title": "Tech", "url": "https://tech.com", "category": "tech"})
    api("POST", "/bookmarks",
        {"title": "News", "url": "https://news.com", "category": "news"})
    api("POST", "/bookmarks",
        {"title": "No Category", "url": "https://none.com"})

    status, body = api("GET", "/bookmarks?category=tech")
    self.assertEqual(status, 200)
    self.assertEqual(len(body), 1)
    self.assertEqual(body[0]["title"], "Tech")
    self.assertEqual(body[0]["category"], "tech")
```

기존 코드 개선:
- HTTPError 처리에 `e.close()` 추가
- `tearDownClass`에 `server.server_close()` 및 `thread.join()` 추가

**변경량**: +43줄, -3줄

---

## 변경 파일 요약

| 파일 | 변경 사항 | 줄 수 변경 |
|------|-----------|-----------|
| `models.py` | category 필드, to_dict, from_dict 추가 | +4 |
| `database.py` | `get_all_by_category()` 함수 추가 | +5 |
| `app.py` | parse_qs import, GET 필터링, POST/PUT category 처리 | +19, -6 |
| `test_api.py` | 카테고리 생성/필터링 테스트 2건, 에러 처리 개선 | +43, -3 |

---

## 관찰 포인트 (Round 1 특성)

### 에이전트가 자율적으로 판단한 사항

| 판단 항목 | 에이전트의 선택 | 비고 |
|-----------|----------------|------|
| 필터링 방식 | 쿼리 파라미터 (`?category=tech`) | 별도 엔드포인트가 아닌 기존 GET에 통합 |
| `parse_qs` 사용 | `urllib.parse.parse_qs()` 사용 | 리스트 반환이므로 `[0]` 인덱싱 필요 |
| category 유효성 검사 | 미추가 (`validators.py` 수정 없음) | 자유 텍스트 허용 |
| 에러 핸들링 스타일 | 기존 코드 패턴 따름 | AGENTS.md 없이 코드에서 패턴 유추 |
| 테스트 함수명 | `test_create_bookmark_with_category` 등 | 자체 판단 (규칙 부재) |
| docstring | 미추가 | 기존 코드에도 없었으므로 생략 |
| logging vs print | 기존 `print` 유지 | `logging` 미전환 |

### AGENTS.md 부재로 인한 특징

1. **코드 탐색에 시간 소요**: 기존 패턴을 파악하기 위해 모든 파일을 먼저 읽어야 했음
2. **컨벤션 비일관**: docstring 없음, logging 미사용 등 코드 품질 규칙이 적용되지 않음
3. **validators.py 미수정**: category에 대한 유효성 검사를 추가하지 않음 (허용값 제한 없음)
4. **자유 판단 다수**: 필터링 방식, 응답 형식, 테스트 구조 등을 에이전트가 임의로 결정

---

## 기술 세부사항

- **쿼리 파라미터 파싱**: `parse_qs()`는 딕셔너리 값을 리스트로 반환하므로 `[0]` 인덱싱 필요
- **선택적 필드**: `Optional[str]`로 선언하여 None 기본값 처리
- **데이터 일관성**: 모든 CRUD 작업에서 category 필드 동일하게 처리
- **하위 호환성**: category 필드가 없는 기존 북마크도 `dict.get()` 사용으로 안전하게 처리
