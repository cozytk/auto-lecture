import config

_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_CYAN = "\033[36m"
_YELLOW = "\033[33m"
_GREEN = "\033[32m"
_RED = "\033[31m"
_MAGENTA = "\033[35m"


def _c(code, text):
    if config.get("color_enabled", True):
        return f"{code}{text}{_RESET}"
    return str(text)


def format_duration(minutes):
    minutes = int(minutes)
    if minutes < 60:
        return f"{minutes}분"
    h, m = divmod(minutes, 60)
    if m == 0:
        return f"{h}시간"
    return f"{h}시간 {m}분"


def render_session(session):
    lines = [
        _c(_CYAN, "─" * 45),
        _c(_BOLD, f"  {session['topic']}"),
        _c(_DIM, f"  ID: {session['id']}  |  상태: {session['status']}"),
        _c(_DIM, f"  시작: {session['started_at']}"),
    ]
    if session.get("ended_at"):
        lines.append(_c(_DIM, f"  종료: {session['ended_at']}"))
        lines.append(
            _c(_GREEN, f"  학습 시간: {format_duration(session['duration_minutes'])}")
        )
    if session.get("elapsed_minutes") is not None:
        lines.append(
            _c(_YELLOW, f"  경과: {format_duration(session['elapsed_minutes'])} (진행 중)")
        )
    if session.get("tags"):
        tags_str = ", ".join(session["tags"])
        lines.append(_c(_MAGENTA, f"  태그: {tags_str}"))
    if session.get("notes"):
        lines.append(f"  메모: {session['notes']}")
    lines.append(_c(_CYAN, "─" * 45))
    return "\n".join(lines)


def render_session_list(sessions):
    if not sessions:
        return "기록된 학습 세션이 없습니다."

    lines = [f"총 {len(sessions)}개 세션\n"]
    for s in sessions:
        status_icon = {"active": "▶", "completed": "✓", "paused": "⏸"}.get(
            s["status"], "?"
        )
        if s["status"] == "completed":
            dur = format_duration(s.get("duration_minutes", 0))
        else:
            dur = "진행 중"
        id_part = _c(_DIM, f"[{s['id']}]")
        topic_part = _c(_BOLD, s["topic"])
        dur_part = _c(_GREEN if s["status"] == "completed" else _YELLOW, dur)
        date_part = _c(_DIM, s["started_at"])
        lines.append(f"  {status_icon} {id_part} {topic_part}  {dur_part}  {date_part}")

    return "\n".join(lines)


def render_stats(total, topic_data, streak_days, avg_dur):
    lines = [
        _c(_BOLD, "📊 학습 통계"),
        "",
        f"  총 학습 시간: {_c(_GREEN, format_duration(total))}",
        f"  연속 학습일: {_c(_YELLOW, f'{streak_days}일')}",
        f"  평균 세션: {_c(_CYAN, format_duration(avg_dur))}",
    ]
    if topic_data:
        lines.append("")
        lines.append(_c(_BOLD, "  주제별 학습 시간:"))
        for topic, data in topic_data.items():
            lines.append(
                f"    {topic}: {format_duration(data['minutes'])} ({data['count']}회)"
            )
    return "\n".join(lines)


def _render_progress_bar(current, total, width=20):
    """진행 바 렌더링 (목표 기능 추가 시 활용 예정)"""
    if total == 0:
        return "[" + " " * width + "]"
    filled = int(width * min(current / total, 1.0))
    bar = "█" * filled + "░" * (width - filled)
    pct = min(current / total * 100, 100)
    return f"[{bar}] {pct:.0f}%"
