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
        print(
            f"학습 종료: {s['topic']} ({display.format_duration(s['duration_minutes'])})"
        )
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
    sessions = store.list_sessions()
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
            updates = {
                k: v for k, v in entry.items() if k not in ("id", "topic", "tags")
            }
            if updates:
                store.update_session(sid, updates)
            count += 1
    print(f"가져오기 완료: {count}개 세션")


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
    p_list.set_defaults(func=cmd_list)

    # stats
    p_stats = sub.add_parser("stats", help="학습 통계 보기")
    p_stats.set_defaults(func=cmd_stats)

    # export
    p_export = sub.add_parser("export", help="데이터 내보내기 (JSON)")
    p_export.add_argument("--output", "-o", help="출력 파일 경로")
    p_export.set_defaults(func=cmd_export)

    # 주의: cmd_import는 구현되어 있지만 여기에 등록되지 않았다

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
