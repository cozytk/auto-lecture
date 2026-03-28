"""통계 계산 모듈."""

from datetime import date
from storage import load_sessions_for_date, load_sessions


def get_today_stats(filepath: str = None) -> dict:
    """오늘의 통계를 계산해 반환한다.

    Returns:
        {
            "focus_count": 완료된 집중 세션 수,
            "total_focus_minutes": 총 집중 시간(분),
            "break_count": 완료된 휴식 세션 수,
        }
    """
    kwargs = {"filepath": filepath} if filepath else {}
    today = date.today().isoformat()
    sessions = load_sessions_for_date(today, **kwargs) if filepath else load_sessions_for_date(today)

    focus_count = 0
    total_focus_minutes = 0
    break_count = 0

    for s in sessions:
        if not s.get("completed"):
            continue
        if s.get("session_type") == "focus":
            focus_count += 1
            total_focus_minutes += _duration_minutes(s)
        elif s.get("session_type") == "break":
            break_count += 1

    return {
        "focus_count": focus_count,
        "total_focus_minutes": total_focus_minutes,
        "break_count": break_count,
    }


def get_streak(filepath: str = None) -> int:
    """오늘까지 포모도로를 1개 이상 완료한 연속 일수를 반환한다.

    오늘 완료된 세션이 없으면 streak은 0.
    """
    kwargs = {"filepath": filepath} if filepath else {}
    all_sessions = load_sessions(**kwargs) if filepath else load_sessions()

    # 집중 세션 완료일 집합
    completed_dates = set()
    for s in all_sessions:
        if s.get("completed") and s.get("session_type") == "focus":
            day = s.get("start_time", "")[:10]
            if day:
                completed_dates.add(day)

    streak = 0
    current = date.today()
    while current.isoformat() in completed_dates:
        streak += 1
        from datetime import timedelta
        current = current - timedelta(days=1)

    return streak


def _duration_minutes(session: dict) -> float:
    """세션의 지속 시간을 분 단위로 반환한다."""
    from datetime import datetime
    try:
        start = datetime.fromisoformat(session["start_time"])
        end = datetime.fromisoformat(session["end_time"])
        delta = end - start
        return delta.total_seconds() / 60
    except (KeyError, ValueError):
        return 0.0


def print_stats(filepath: str = None) -> None:
    """오늘의 통계를 터미널에 출력한다."""
    stats = get_today_stats(filepath)
    streak = get_streak(filepath)

    print("\n===== 오늘의 포모도로 통계 =====")
    print(f"  완료한 포모도로: {stats['focus_count']}개")
    print(f"  총 집중 시간:    {stats['total_focus_minutes']:.0f}분")
    print(f"  연속 달성일:     {streak}일")
    print("================================\n")
