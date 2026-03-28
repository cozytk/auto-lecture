"""
JSON 파일 기반 북마크 저장소
"""
import json
import logging
import os
from typing import List, Optional

from models import Bookmark

logger = logging.getLogger(__name__)
DB_FILE = os.environ.get("BOOKMARK_DB", "bookmarks.json")


def _load() -> List[dict]:
    """DB 파일에서 북마크 목록을 읽어 반환한다.

    Returns:
        북마크 딕셔너리 목록. 파일이 없으면 빈 리스트.
    """
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: List[dict]) -> None:
    """북마크 목록을 DB 파일에 저장한다.

    Args:
        data: 저장할 북마크 딕셔너리 목록.
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_all() -> List[Bookmark]:
    """모든 북마크를 반환한다.

    Returns:
        Bookmark 인스턴스 목록.
    """
    return [Bookmark.from_dict(d) for d in _load()]


def get_by_id(bookmark_id: str) -> Optional[Bookmark]:
    """ID로 북마크를 조회한다.

    Args:
        bookmark_id: 조회할 북마크 ID.

    Returns:
        Bookmark 인스턴스. 없으면 None.
    """
    for d in _load():
        if d["id"] == bookmark_id:
            return Bookmark.from_dict(d)
    return None


def create(bookmark: Bookmark) -> Bookmark:
    """새 북마크를 저장하고 반환한다.

    Args:
        bookmark: 저장할 Bookmark 인스턴스.

    Returns:
        저장된 Bookmark 인스턴스.
    """
    data = _load()
    data.append(bookmark.to_dict())
    _save(data)
    logger.info("북마크 생성: id=%s title=%s", bookmark.id, bookmark.title)
    return bookmark


def update(bookmark: Bookmark) -> Optional[Bookmark]:
    """북마크를 수정한다.

    Args:
        bookmark: 수정할 내용이 담긴 Bookmark 인스턴스.

    Returns:
        수정된 Bookmark 인스턴스. 없으면 None.
    """
    data = _load()
    for i, d in enumerate(data):
        if d["id"] == bookmark.id:
            data[i] = bookmark.to_dict()
            _save(data)
            logger.info("북마크 수정: id=%s", bookmark.id)
            return bookmark
    return None


def delete(bookmark_id: str) -> bool:
    """북마크를 삭제한다.

    Args:
        bookmark_id: 삭제할 북마크 ID.

    Returns:
        삭제 성공 시 True, 존재하지 않으면 False.
    """
    data = _load()
    new_data = [d for d in data if d["id"] != bookmark_id]
    if len(new_data) == len(data):
        return False
    _save(new_data)
    logger.info("북마크 삭제: id=%s", bookmark_id)
    return True
