"""
북마크 데이터 모델
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Bookmark:
    """북마크 데이터 모델.

    Attributes:
        title: 북마크 제목 (최대 200자, 필수)
        url: 북마크 URL (http/https, 필수)
        id: UUID4 식별자 (자동 생성)
        description: 북마크 설명 (선택)
        created_at: 생성 시각 (ISO 8601, 자동 설정)
        updated_at: 최종 수정 시각 (ISO 8601, 자동 설정)
    """

    title: str
    url: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Bookmark를 JSON 직렬화 가능한 딕셔너리로 변환한다.

        Returns:
            모든 필드를 포함한 딕셔너리.
        """
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Bookmark":
        """딕셔너리에서 Bookmark 인스턴스를 생성한다.

        Args:
            data: 북마크 데이터 딕셔너리.

        Returns:
            Bookmark 인스턴스.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            url=data["url"],
            description=data.get("description"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
