"""타이머 로직 모듈."""

import sys
import time
from datetime import datetime

# 기본 지속 시간 (분)
FOCUS_DURATION = 25
BREAK_DURATION = 5


def _render_progress_bar(elapsed: int, total: int, width: int = 20) -> str:
    """진행률 바 문자열을 반환한다.

    예: [=========>         ] 18:32 남음
    """
    remaining = total - elapsed
    filled = int(width * elapsed / total) if total > 0 else 0
    bar = "=" * filled + (">" if filled < width else "") + " " * max(0, width - filled - 1)
    mins, secs = divmod(remaining, 60)
    return f"\r[{bar}] {mins:02d}:{secs:02d} 남음  "


def run_timer(duration_seconds: int, label: str, tick_fn=None) -> tuple:
    """카운트다운 타이머를 실행한다.

    Args:
        duration_seconds: 타이머 총 시간 (초)
        label: 표시할 레이블 ("집중" 또는 "휴식")
        tick_fn: 1초마다 호출되는 콜백 (테스트 주입용). None이면 time.sleep(1) 사용.

    Returns:
        (start_time, end_time, completed)
        completed: 정상 완료 시 True, Ctrl+C 중단 시 False
    """
    start_time = datetime.now()
    print(f"\n[{label} 타이머 시작] {duration_seconds // 60}분 {duration_seconds % 60}초")

    completed = False
    elapsed = 0
    try:
        while elapsed < duration_seconds:
            bar = _render_progress_bar(elapsed, duration_seconds)
            sys.stdout.write(bar)
            sys.stdout.flush()

            if tick_fn is not None:
                tick_fn()
            else:
                time.sleep(1)

            elapsed += 1

        # 완료
        sys.stdout.write(_render_progress_bar(duration_seconds, duration_seconds))
        sys.stdout.write("\n")
        sys.stdout.flush()
        print(f"[{label} 완료!] \a")  # \a = 터미널 벨
        completed = True

    except KeyboardInterrupt:
        sys.stdout.write("\n")
        print(f"\n[{label} 중단됨]")

    end_time = datetime.now()
    return start_time, end_time, completed
