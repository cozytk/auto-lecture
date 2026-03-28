"""
예시: Google 스타일 docstring 작성법.
이 파일은 실행용이 아닌 참조용 예시입니다.
"""
from typing import Optional, Tuple


# ─── ✅ 올바른 docstring 패턴 ──────────────────────────────────

def validate_category(category: Optional[str]) -> Tuple[bool, Optional[str]]:
    """카테고리 값의 유효성을 검사한다.

    Args:
        category: 검사할 카테고리 문자열. None이면 유효하다고 판단한다.

    Returns:
        (valid, error_message) 튜플.
        유효하면 (True, None), 유효하지 않으면 (False, "에러 메시지").

    Example:
        >>> validate_category("tech")
        (True, None)
        >>> validate_category("invalid")
        (False, "category는 허용된 값 중 하나여야 합니다")
    """
    if category is None:
        return True, None
    allowed = {"tech", "news", "blog", "video", "docs", "other"}
    if category not in allowed:
        return False, f"category는 {sorted(allowed)} 중 하나여야 합니다"
    return True, None


def get_by_category(category: str) -> list:
    """카테고리로 북마크를 필터링하여 반환한다.

    Args:
        category: 필터링할 카테고리 문자열.

    Returns:
        해당 카테고리의 Bookmark 인스턴스 목록.
        카테고리에 해당하는 항목이 없으면 빈 리스트.

    Raises:
        IOError: DB 파일을 읽을 수 없을 때.
    """
    # 구현 예시
    return []


# ─── ❌ 금지 패턴 ──────────────────────────────────────────────

def bad_no_docstring(x):
    # 설명 없음 — 다른 사람이 이해하기 어렵다
    return x * 2


def bad_no_type_hints(category):  # ← 타입 힌트 없음
    """카테고리 검사."""  # ← Args/Returns 없음
    pass
