"""CLI 포모도로 타이머 — 메인 진입점."""

import argparse
import sys

from storage import save_session
from stats import print_stats
from timer import run_timer, FOCUS_DURATION, BREAK_DURATION


def cmd_start(args):
    """집중 타이머 실행."""
    duration = args.duration if args.duration else FOCUS_DURATION * 60
    start_time, end_time, completed = run_timer(duration, "집중")
    save_session(start_time, end_time, "focus", completed)


def cmd_break(args):
    """휴식 타이머 실행."""
    duration = args.duration if args.duration else BREAK_DURATION * 60
    start_time, end_time, completed = run_timer(duration, "휴식")
    save_session(start_time, end_time, "break", completed)


def cmd_stats(_args):
    """통계 출력."""
    print_stats()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pomodoro",
        description="CLI 포모도로 타이머",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # start
    start_parser = subparsers.add_parser("start", help="집중 타이머 시작 (기본 25분)")
    start_parser.add_argument(
        "--duration",
        type=int,
        default=None,
        metavar="초",
        help="타이머 시간(초). 기본값: 1500(25분). 테스트 시 짧은 값 사용 가능.",
    )
    start_parser.set_defaults(func=cmd_start)

    # break
    break_parser = subparsers.add_parser("break", help="휴식 타이머 시작 (기본 5분)")
    break_parser.add_argument(
        "--duration",
        type=int,
        default=None,
        metavar="초",
        help="타이머 시간(초). 기본값: 300(5분).",
    )
    break_parser.set_defaults(func=cmd_break)

    # stats
    stats_parser = subparsers.add_parser("stats", help="오늘의 통계 출력")
    stats_parser.set_defaults(func=cmd_stats)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
