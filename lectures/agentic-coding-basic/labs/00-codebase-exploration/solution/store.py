import json
import uuid
from datetime import datetime
from pathlib import Path

import config


def _data_path():
    raw = config.get("storage_path", "~/.studylog/data.json")
    return Path(raw).expanduser()


def _load():
    path = _data_path()
    if not path.exists():
        return {"sessions": {}, "version": 2}
    with open(path) as f:
        data = json.load(f)
    if data.get("version", 1) == 1:
        data = _migrate_v1(data)
    return data


def _save(data):
    path = _data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _migrate_v1(old_data):
    """v1 형식(리스트)을 v2 형식(딕셔너리)으로 변환"""
    sessions = {}
    for entry in old_data.get("entries", []):
        sid = entry.get("id", uuid.uuid4().hex[:8])
        sessions[sid] = entry
    return {"sessions": sessions, "version": 2}


def add_session(topic, tags=None):
    data = _load()
    sid = uuid.uuid4().hex[:8]
    now = datetime.now().strftime(config.get("date_format"))
    session = {
        "id": sid,
        "topic": topic,
        "tags": tags or [],
        "started_at": now,
        "ended_at": None,
        "duration_minutes": 0,
        "notes": "",
        "status": "active",
        "paused_at": None,
        "paused_minutes": 0,
    }
    data["sessions"][sid] = session
    _save(data)
    return session


def get_session(sid):
    data = _load()
    return data["sessions"].get(sid)


def update_session(sid, updates):
    data = _load()
    if sid not in data["sessions"]:
        return None
    data["sessions"][sid].update(updates)
    _save(data)
    return data["sessions"][sid]


def list_sessions(topic=None):
    data = _load()
    sessions = list(data["sessions"].values())
    if topic is not None:
        keyword = topic.lower()
        sessions = [s for s in sessions if keyword in s["topic"].lower()]
    return sorted(sessions, key=lambda s: s["started_at"], reverse=True)


def delete_session(sid):
    data = _load()
    if sid not in data["sessions"]:
        return False
    del data["sessions"][sid]
    _save(data)
    return True


def get_active():
    for s in list_sessions():
        if s["status"] in ("active", "paused"):
            return s
    return None


def get_goal():
    """저장된 일일 학습 목표(분)를 반환. 없으면 config 기본값."""
    data = _load()
    return data.get("daily_goal_minutes", config.get("daily_goal_minutes", 60))


def set_goal(minutes):
    """일일 학습 목표(분)를 저장."""
    data = _load()
    data["daily_goal_minutes"] = minutes
    _save(data)
