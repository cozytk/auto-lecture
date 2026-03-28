from datetime import datetime, timedelta
from collections import defaultdict

import config


def total_time(sessions):
    return sum(
        s.get("duration_minutes", 0)
        for s in sessions
        if s["status"] == "completed"
    )


def by_topic(sessions):
    """주제별 학습 시간 집계"""
    topics = defaultdict(lambda: {"count": 0, "minutes": 0})
    for s in sessions:
        if s["status"] != "completed":
            continue
        t = s["topic"]
        topics[t]["count"] += 1
        topics[t]["minutes"] += s.get("duration_minutes", 0)
    return dict(sorted(topics.items(), key=lambda x: x[1]["minutes"], reverse=True))


def by_day(sessions):
    """일별 학습 시간 집계"""
    days = defaultdict(lambda: {"count": 0, "minutes": 0})
    fmt = config.get("date_format")
    for s in sessions:
        if s["status"] != "completed":
            continue
        day = datetime.strptime(s["started_at"], fmt).strftime("%Y-%m-%d")
        days[day]["count"] += 1
        days[day]["minutes"] += s.get("duration_minutes", 0)
    return dict(sorted(days.items(), reverse=True))


def streak(sessions):
    """연속 학습일 수 계산

    주의: started_at은 로컬 시각 문자열이다.
    datetime.now().date()와 비교하므로 자정 근처 세션에서
    날짜가 하루 어긋날 수 있다.
    """
    fmt = config.get("date_format")
    study_dates = set()
    for s in sessions:
        if s["status"] != "completed":
            continue
        day = datetime.strptime(s["started_at"], fmt).date()
        study_dates.add(day)

    if not study_dates:
        return 0

    today = datetime.now().date()

    if today not in study_dates and (today - timedelta(days=1)) not in study_dates:
        return 0

    # 오늘부터 거슬러 올라가며 연속일 계산
    if today in study_dates:
        count = 0
        check = today
        while check in study_dates:
            count += 1
            check -= timedelta(days=1)
        return count

    # 오늘 학습 안 했으면 어제부터 계산
    count = 0
    check = today - timedelta(days=1)
    while check in study_dates:
        count += 1
        check -= timedelta(days=1)
    return count


def average_duration(sessions):
    completed = [s for s in sessions if s["status"] == "completed"]
    if not completed:
        return 0
    total = sum(s.get("duration_minutes", 0) for s in completed)
    return round(total / len(completed), 1)


def today_minutes(sessions):
    """오늘 완료된 세션의 총 학습 시간(분)"""
    fmt = config.get("date_format")
    today = datetime.now().date()
    total = 0
    for s in sessions:
        if s["status"] != "completed":
            continue
        day = datetime.strptime(s["started_at"], fmt).date()
        if day == today:
            total += s.get("duration_minutes", 0)
    return total


def _legacy_score(sessions):
    """이전 버전의 점수 계산 (더 이상 사용하지 않음)"""
    score = 0
    for s in sessions:
        score += s.get("duration_minutes", 0) * 10
        if s.get("tags"):
            score += len(s["tags"]) * 5
    return score
