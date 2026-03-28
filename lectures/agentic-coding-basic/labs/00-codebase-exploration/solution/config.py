import json
from pathlib import Path

APP_NAME = "studylog"
VERSION = "0.1.4"

_DEFAULT = {
    "storage_path": "~/.studylog/data.json",
    "date_format": "%Y-%m-%d %H:%M",
    "color_enabled": True,
    "streak_reset_hours": 36,
    "daily_goal_minutes": 60,
}

_config_cache = None


def _config_path():
    return Path.home() / ".studylog" / "config.json"


def load():
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    path = _config_path()
    if path.exists():
        with open(path) as f:
            user = json.load(f)
        merged = {**_DEFAULT, **user}
    else:
        merged = dict(_DEFAULT)

    import os
    if os.environ.get("STUDYLOG_DEBUG"):
        merged["debug"] = True

    _config_cache = merged
    return _config_cache


def get(key, fallback=None):
    cfg = load()
    return cfg.get(key, fallback)
