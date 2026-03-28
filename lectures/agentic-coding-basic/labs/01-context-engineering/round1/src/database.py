"""
JSON 파일 기반 북마크 저장소
"""

import json
import os
from typing import List, Optional

from models import Bookmark

DB_FILE = os.environ.get("BOOKMARK_DB", "bookmarks.json")


def _load() -> List[dict]:
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: List[dict]) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_all() -> List[Bookmark]:
    return [Bookmark.from_dict(d) for d in _load()]


def get_all_by_category(category: str) -> List[Bookmark]:
    return [bookmark for bookmark in get_all() if bookmark.category == category]


def get_by_id(bookmark_id: str) -> Optional[Bookmark]:
    for d in _load():
        if d["id"] == bookmark_id:
            return Bookmark.from_dict(d)
    return None


def create(bookmark: Bookmark) -> Bookmark:
    data = _load()
    data.append(bookmark.to_dict())
    _save(data)
    return bookmark


def update(bookmark: Bookmark) -> Optional[Bookmark]:
    data = _load()
    for i, d in enumerate(data):
        if d["id"] == bookmark.id:
            data[i] = bookmark.to_dict()
            _save(data)
            return bookmark
    return None


def delete(bookmark_id: str) -> bool:
    data = _load()
    new_data = [d for d in data if d["id"] != bookmark_id]
    if len(new_data) == len(data):
        return False
    _save(new_data)
    return True
