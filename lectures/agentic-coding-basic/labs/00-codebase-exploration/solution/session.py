"""세션 시작/종료/일시정지/재개 관리"""

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

    # paused 상태라면 먼저 완료 전이 허용
    _validate_transition(active["status"], "completed")

    started = datetime.strptime(active["started_at"], config.get("date_format"))
    ended = datetime.now()
    total_elapsed = int((ended - started).total_seconds() / 60)
    paused_minutes = active.get("paused_minutes", 0)

    # 현재 paused 상태면 paused_at 이후 경과분도 accumulated에 포함되지 않으므로
    # total_elapsed 에서 누적 paused_minutes만 차감
    duration = max(total_elapsed - paused_minutes, 1)

    updates = {
        "ended_at": ended.strftime(config.get("date_format")),
        "duration_minutes": duration,
        "status": "completed",
        "paused_at": None,
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
    total_elapsed = int((datetime.now() - started).total_seconds() / 60)
    paused_minutes = active.get("paused_minutes", 0)

    # 현재 paused 중이면 paused_at 이후 시간도 멈춰있음
    if active["status"] == "paused" and active.get("paused_at"):
        paused_since = datetime.strptime(active["paused_at"], config.get("date_format"))
        extra_paused = int((datetime.now() - paused_since).total_seconds() / 60)
        elapsed = total_elapsed - paused_minutes - extra_paused
    else:
        elapsed = total_elapsed - paused_minutes

    return {**active, "elapsed_minutes": max(elapsed, 0)}


def pause():
    """진행 중인 세션을 일시정지."""
    active = store.get_active()
    if active is None:
        raise ValueError("진행 중인 세션이 없습니다")
    _validate_transition(active["status"], "paused")

    now = datetime.now().strftime(config.get("date_format"))
    updates = {
        "status": "paused",
        "paused_at": now,
    }
    return store.update_session(active["id"], updates)


def resume():
    """일시정지된 세션을 재개."""
    active = store.get_active()
    if active is None:
        raise ValueError("진행 중인 세션이 없습니다")
    _validate_transition(active["status"], "active")

    paused_at_str = active.get("paused_at")
    accumulated = active.get("paused_minutes", 0)

    if paused_at_str:
        paused_at = datetime.strptime(paused_at_str, config.get("date_format"))
        extra = int((datetime.now() - paused_at).total_seconds() / 60)
        accumulated += extra

    updates = {
        "status": "active",
        "paused_at": None,
        "paused_minutes": accumulated,
    }
    return store.update_session(active["id"], updates)


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
