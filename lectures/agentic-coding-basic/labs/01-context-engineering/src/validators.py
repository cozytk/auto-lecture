"""
북마크 입력 유효성 검사
"""
from urllib.parse import urlparse
from typing import Tuple, Optional


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """URL 유효성 검사. (valid, error_message) 반환."""
    if not url:
        return False, "url은 필수 항목입니다"
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, "url은 http 또는 https로 시작해야 합니다"
    if not parsed.netloc:
        return False, "유효하지 않은 url 형식입니다"
    return True, None


def validate_title(title: str) -> Tuple[bool, Optional[str]]:
    """제목 유효성 검사. (valid, error_message) 반환."""
    if not title or not title.strip():
        return False, "title은 필수 항목입니다"
    if len(title) > 200:
        return False, "title은 200자 이하여야 합니다"
    return True, None


def validate_bookmark_input(data: dict) -> Tuple[bool, Optional[str]]:
    """북마크 생성/수정 요청 데이터 전체 유효성 검사."""
    ok, err = validate_title(data.get("title", ""))
    if not ok:
        return False, err
    ok, err = validate_url(data.get("url", ""))
    if not ok:
        return False, err
    return True, None
