"""세션 저장 및 불러오기 모듈."""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "sessions.json")


def _load_raw(filepath: str = DATA_FILE) -> list:
    """JSON 파일에서 세션 목록을 로드한다. 파일 없거나 손상 시 빈 리스트 반환."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("[경고] sessions.json 형식이 잘못됐습니다. 초기화합니다.", file=__import__("sys").stderr)
                return []
            return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"[경고] sessions.json 읽기 실패: {e}. 초기화합니다.", file=__import__("sys").stderr)
        return []


def _save_raw(sessions: list, filepath: str = DATA_FILE) -> None:
    """세션 목록을 JSON 파일에 저장한다."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"[오류] 세션 저장 실패: {e}", file=__import__("sys").stderr)


def save_session(
    start_time: datetime,
    end_time: datetime,
    session_type: str,
    completed: bool,
    filepath: str = DATA_FILE,
) -> None:
    """세션 하나를 저장한다.

    Args:
        start_time: 세션 시작 시각
        end_time: 세션 종료 시각
        session_type: "focus" 또는 "break"
        completed: 정상 완료 여부 (Ctrl+C 중단 시 False)
        filepath: 저장할 파일 경로 (테스트 시 임시 파일 경로 사용)
    """
    sessions = _load_raw(filepath)
    sessions.append(
        {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "session_type": session_type,
            "completed": completed,
        }
    )
    _save_raw(sessions, filepath)


def load_sessions(filepath: str = DATA_FILE) -> list:
    """전체 세션 목록을 반환한다.

    Returns:
        세션 dict 목록. 각 항목:
        {start_time, end_time, session_type, completed}
    """
    return _load_raw(filepath)


def load_sessions_for_date(date_str: str, filepath: str = DATA_FILE) -> list:
    """특정 날짜(YYYY-MM-DD)의 세션 목록을 반환한다."""
    all_sessions = _load_raw(filepath)
    return [s for s in all_sessions if s.get("start_time", "").startswith(date_str)]
