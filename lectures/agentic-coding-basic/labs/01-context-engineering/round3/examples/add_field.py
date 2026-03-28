"""
예시: Bookmark에 새 필드(category)를 추가하는 올바른 패턴.
이 파일은 실행용이 아닌 참조용 예시입니다.
"""

# ─── models.py 수정 예시 ───────────────────────────────────────
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class BookmarkWithCategory:
    """카테고리 필드가 추가된 북마크 모델 예시."""

    title: str
    url: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = None
    category: Optional[str] = None           # ← 새 필드 추가
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Bookmark를 직렬화한다."""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "category": self.category,        # ← to_dict에 추가
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BookmarkWithCategory":
        """딕셔너리에서 Bookmark를 역직렬화한다."""
        return cls(
            id=data["id"],
            title=data["title"],
            url=data["url"],
            description=data.get("description"),
            category=data.get("category"),    # ← from_dict에 추가 (.get으로 하위호환)
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )


# ─── validators.py 수정 예시 ──────────────────────────────────
VALID_CATEGORIES = {"tech", "news", "blog", "video", "docs", "other"}


def validate_category(category: Optional[str]):
    """카테고리 유효성 검사 예시.

    Args:
        category: 검사할 카테고리 문자열 (None 허용)

    Returns:
        (valid, error_message) 튜플
    """
    if category is None:
        return True, None  # 선택 필드이므로 None은 허용
    if category not in VALID_CATEGORIES:
        return False, f"category는 {sorted(VALID_CATEGORIES)} 중 하나여야 합니다"
    return True, None


# ─── database.py 수정 예시 ────────────────────────────────────
def get_by_category_example(category: str):
    """카테고리로 필터링하는 저장소 함수 예시.

    Args:
        category: 필터링할 카테고리 문자열

    Returns:
        해당 카테고리의 북마크 목록
    """
    # 실제 구현에서는 _load()를 호출
    # data = _load()
    # return [Bookmark.from_dict(d) for d in data if d.get("category") == category]
    pass


# ─── app.py 라우트 수정 예시 ──────────────────────────────────
# GET /bookmarks?category=tech  쿼리 파라미터로 필터링
#
# def do_GET(self):
#     from urllib.parse import urlparse, parse_qs
#     parsed = urlparse(self.path)
#     path = parsed.path.rstrip("/")
#     params = parse_qs(parsed.query)
#
#     if path == "/bookmarks":
#         category = params.get("category", [None])[0]
#         if category:
#             bookmarks = database.get_by_category(category)
#         else:
#             bookmarks = database.get_all()
#         json_response(self, 200, [b.to_dict() for b in bookmarks])
