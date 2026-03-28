#!/usr/bin/env python3
"""
studylog - CLI 학습 세션 트래커
사용법: python3 studylog.py <command> [options]
"""

import argparse
import json
import sys

import config
import session
import store
import engine
import display


def cmd_start(args):
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    try:
        s = session.start(args.topic, tags)
        print(f"학습 시작: {s['topic']} (ID: {s['id']})")
    except ValueError as e:
        print(f"오류: {e}")
        sys.exit(1)


def cmd_stop(args):
    try:
        s = session.stop(notes=args.notes or "")
        print(f"학습 종료: {s['topic']} ({display.format_duration(s['duration_minutes'])})")
    except ValueError as e:
        print(f"오류: {e}")
        sys.exit(1)


def cmd_current(args):
    cur = session.current()
    if cur is None:
        print("진행 중인 세션이 없습니다.")
        return
    print(display.render_session(cur))


def cmd_list(args):
    topic_filter = getattr(args, "topic", None)
    sessions = store.list_sessions(topic=topic_filter)
    if not sessions:
        print("기록된 학습 세션이 없습니다.")
        return
    print(display.render_session_list(sessions))


def cmd_stats(args):
    sessions = store.list_sessions()
    if not sessions:
        print("통계를 계산할 데이터가 없습니다.")
        return
    total = engine.total_time(sessions)
    topics = engine.by_topic(sessions)
    streak_days = engine.streak(sessions)
    avg = engine.average_duration(sessions)
    print(display.render_stats(total, topics, streak_days, avg))


def cmd_export(args):
    sessions = store.list_sessions()
    output = json.dumps(sessions, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"내보내기 완료: {args.output} ({len(sessions)}개 세션)")
    else:
        print(output)


def cmd_import(args):
    """JSON 파일에서 세션 가져오기"""
    with open(args.file) as f:
        entries = json.load(f)
    count = 0
    for entry in entries:
        if "topic" in entry and "started_at" in entry:
            store.add_session(entry["topic"], entry.get("tags", []))
            sid = store.list_sessions()[0]["id"]
            updates = {k: v for k, v in entry.items() if k not in ("id", "topic", "tags")}
            if updates:
                store.update_session(sid, updates)
            count += 1
    print(f"가져오기 완료: {count}개 세션")


def cmd_pause(args):
    try:
        s = session.pause()
        print(f"일시정지: {s['topic']} (ID: {s['id']})")
    except ValueError as e:
        print(f"오류: {e}")
        sys.exit(1)


def cmd_resume(args):
    try:
        s = session.resume()
        print(f"재개: {s['topic']} (ID: {s['id']})")
    except ValueError as e:
        print(f"오류: {e}")
        sys.exit(1)


def cmd_goal(args):
    if args.action == "set":
        minutes = args.minutes
        if minutes <= 0:
            print("오류: 목표 시간은 1분 이상이어야 합니다.")
            sys.exit(1)
        store.set_goal(minutes)
        print(f"일일 목표 설정: {display.format_duration(minutes)}")
    elif args.action == "show":
        goal_minutes = store.get_goal()
        sessions = store.list_sessions()
        today_mins = engine.today_minutes(sessions)
        print(display.render_goal(today_mins, goal_minutes))


def build_parser():
    parser = argparse.ArgumentParser(
        prog="studylog",
        description="studylog - CLI 학습 세션 트래커",
    )
    parser.add_argument("--version", action="version", version=config.VERSION)

    sub = parser.add_subparsers(dest="command", metavar="command")
    sub.required = True

    # start
    p_start = sub.add_parser("start", help="학습 세션 시작")
    p_start.add_argument("topic", help="학습 주제")
    p_start.add_argument("--tags", "-t", help="태그 (쉼표 구분)")
    p_start.set_defaults(func=cmd_start)

    # stop
    p_stop = sub.add_parser("stop", help="학습 세션 종료")
    p_stop.add_argument("--notes", "-n", help="학습 메모")
    p_stop.set_defaults(func=cmd_stop)

    # current
    p_cur = sub.add_parser("current", help="현재 진행 중인 세션 확인")
    p_cur.set_defaults(func=cmd_current)

    # list
    p_list = sub.add_parser("list", help="세션 목록 조회")
    p_list.add_argument("--topic", "-t", help="주제 필터 (부분 일치, 대소문자 무시)")
    p_list.set_defaults(func=cmd_list)

    # stats
    p_stats = sub.add_parser("stats", help="학습 통계 보기")
    p_stats.set_defaults(func=cmd_stats)

    # export
    p_export = sub.add_parser("export", help="데이터 내보내기 (JSON)")
    p_export.add_argument("--output", "-o", help="출력 파일 경로")
    p_export.set_defaults(func=cmd_export)

    # import
    p_import = sub.add_parser("import", help="JSON 파일에서 세션 가져오기")
    p_import.add_argument("file", help="가져올 JSON 파일 경로")
    p_import.set_defaults(func=cmd_import)

    # pause
    p_pause = sub.add_parser("pause", help="현재 세션 일시정지")
    p_pause.set_defaults(func=cmd_pause)

    # resume
    p_resume = sub.add_parser("resume", help="일시정지된 세션 재개")
    p_resume.set_defaults(func=cmd_resume)

    # goal
    p_goal = sub.add_parser("goal", help="일일 학습 목표 관리")
    goal_sub = p_goal.add_subparsers(dest="action", metavar="action")
    goal_sub.required = True

    p_goal_set = goal_sub.add_parser("set", help="일일 목표 설정 (분 단위)")
    p_goal_set.add_argument("minutes", type=int, help="목표 시간 (분)")
    p_goal_show = goal_sub.add_parser("show", help="일일 목표 및 진행 상황 표시")
    p_goal.set_defaults(func=cmd_goal)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
