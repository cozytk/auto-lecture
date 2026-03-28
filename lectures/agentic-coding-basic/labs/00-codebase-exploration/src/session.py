"""세션 시작/종료 관리"""

from datetime import datetime

import config
import store


def start(topic, tags=None):
    active = store.get_active()
    if active:
        raise ValueError(
            f"이미 진행 중인 세션이 있습니다: {active['topic']} (ID: {active['id']})"
        )
    return store.add_session(topic, tags)


def stop(notes=""):
    active = store.get_active()
    if active is None:
        raise ValueError("진행 중인 세션이 없습니다")

    started = datetime.strptime(active["started_at"], config.get("date_format"))
    ended = datetime.now()
    duration = int((ended - started).total_seconds() / 60)

    updates = {
        "ended_at": ended.strftime(config.get("date_format")),
        "duration_minutes": max(duration, 1),
        "status": "completed",
    }
    if notes:
        updates["notes"] = notes

    return store.update_session(active["id"], updates)


def current():
    """현재 세션 정보 반환. 없으면 None."""
    active = store.get_active()
    if active is None:
        return None

    started = datetime.strptime(active["started_at"], config.get("date_format"))
    elapsed = int((datetime.now() - started).total_seconds() / 60)
    return {**active, "elapsed_minutes": elapsed}


def _validate_transition(current_status, target_status):
    valid = {
        "active": ["completed", "paused"],
        "paused": ["active", "completed"],
        "completed": [],
    }
    allowed = valid.get(current_status, [])
    if target_status not in allowed:
        raise ValueError(
            f"'{current_status}' → '{target_status}' 전이는 허용되지 않습니다"
        )
