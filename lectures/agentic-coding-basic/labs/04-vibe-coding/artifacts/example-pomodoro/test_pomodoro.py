"""포모도로 타이머 자동화 테스트."""

import json
import os
import tempfile
import unittest
from datetime import datetime, date, timedelta
from unittest.mock import patch


class TestStorage(unittest.TestCase):
    """storage.py 테스트."""

    def setUp(self):
        # 각 테스트마다 임시 파일 사용
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.filepath = self.tmp.name
        # 빈 JSON 배열로 초기화
        with open(self.filepath, "w") as f:
            json.dump([], f)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_save_session_creates_entry(self):
        """세션 저장 후 파일에 1개 항목이 있어야 한다."""
        from storage import save_session, load_sessions
        start = datetime(2024, 1, 15, 9, 0, 0)
        end = datetime(2024, 1, 15, 9, 25, 0)
        save_session(start, end, "focus", True, filepath=self.filepath)
        sessions = load_sessions(filepath=self.filepath)
        self.assertEqual(len(sessions), 1)

    def test_save_session_stores_correct_fields(self):
        """저장된 세션에 필수 필드가 모두 있어야 한다."""
        from storage import save_session, load_sessions
        start = datetime(2024, 1, 15, 9, 0, 0)
        end = datetime(2024, 1, 15, 9, 25, 0)
        save_session(start, end, "focus", True, filepath=self.filepath)
        session = load_sessions(filepath=self.filepath)[0]
        self.assertIn("start_time", session)
        self.assertIn("end_time", session)
        self.assertEqual(session["session_type"], "focus")
        self.assertTrue(session["completed"])

    def test_save_multiple_sessions(self):
        """여러 세션을 저장하면 모두 누적되어야 한다."""
        from storage import save_session, load_sessions
        for i in range(3):
            start = datetime(2024, 1, 15, 9 + i, 0, 0)
            end = datetime(2024, 1, 15, 9 + i, 25, 0)
            save_session(start, end, "focus", True, filepath=self.filepath)
        sessions = load_sessions(filepath=self.filepath)
        self.assertEqual(len(sessions), 3)

    def test_load_sessions_missing_file_returns_empty(self):
        """파일이 없을 때 빈 리스트를 반환해야 한다."""
        from storage import load_sessions
        missing = "/tmp/nonexistent_pomodoro_test_123456.json"
        sessions = load_sessions(filepath=missing)
        self.assertEqual(sessions, [])

    def test_load_sessions_corrupted_file_returns_empty(self):
        """손상된 JSON 파일일 때 빈 리스트를 반환해야 한다."""
        from storage import load_sessions
        with open(self.filepath, "w") as f:
            f.write("{ invalid json !!!")
        sessions = load_sessions(filepath=self.filepath)
        self.assertEqual(sessions, [])

    def test_load_sessions_for_date_filters_correctly(self):
        """날짜 필터가 정확하게 동작해야 한다."""
        from storage import save_session, load_sessions_for_date
        # 오늘 세션 2개
        today = date.today()
        for i in range(2):
            start = datetime(today.year, today.month, today.day, 9 + i, 0, 0)
            end = datetime(today.year, today.month, today.day, 9 + i, 25, 0)
            save_session(start, end, "focus", True, filepath=self.filepath)
        # 어제 세션 1개
        yesterday = today - timedelta(days=1)
        start = datetime(yesterday.year, yesterday.month, yesterday.day, 9, 0, 0)
        end = datetime(yesterday.year, yesterday.month, yesterday.day, 9, 25, 0)
        save_session(start, end, "focus", True, filepath=self.filepath)

        today_sessions = load_sessions_for_date(today.isoformat(), filepath=self.filepath)
        self.assertEqual(len(today_sessions), 2)


class TestStats(unittest.TestCase):
    """stats.py 테스트."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.filepath = self.tmp.name
        with open(self.filepath, "w") as f:
            json.dump([], f)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def _add_session(self, session_type, completed, date_offset=0, duration_minutes=25):
        """테스트용 세션 추가 헬퍼."""
        from storage import save_session
        target = date.today() - timedelta(days=date_offset)
        start = datetime(target.year, target.month, target.day, 9, 0, 0)
        end = datetime(target.year, target.month, target.day, 9, duration_minutes, 0)
        save_session(start, end, session_type, completed, filepath=self.filepath)

    def test_get_today_stats_empty(self):
        """세션이 없으면 모든 통계가 0이어야 한다."""
        from stats import get_today_stats
        stats = get_today_stats(filepath=self.filepath)
        self.assertEqual(stats["focus_count"], 0)
        self.assertEqual(stats["total_focus_minutes"], 0)
        self.assertEqual(stats["break_count"], 0)

    def test_get_today_stats_counts_completed_focus(self):
        """완료된 집중 세션만 카운트해야 한다."""
        from stats import get_today_stats
        self._add_session("focus", True)
        self._add_session("focus", True)
        self._add_session("focus", False)  # 미완료 — 카운트 안 됨
        stats = get_today_stats(filepath=self.filepath)
        self.assertEqual(stats["focus_count"], 2)

    def test_get_today_stats_total_minutes(self):
        """총 집중 시간이 정확해야 한다."""
        from stats import get_today_stats
        self._add_session("focus", True, duration_minutes=25)
        self._add_session("focus", True, duration_minutes=25)
        stats = get_today_stats(filepath=self.filepath)
        self.assertAlmostEqual(stats["total_focus_minutes"], 50, delta=0.1)

    def test_get_streak_zero_when_no_sessions_today(self):
        """오늘 세션이 없으면 streak은 0이어야 한다."""
        from stats import get_streak
        # 어제 세션만 추가
        self._add_session("focus", True, date_offset=1)
        streak = get_streak(filepath=self.filepath)
        self.assertEqual(streak, 0)

    def test_get_streak_counts_consecutive_days(self):
        """연속된 날의 streak을 정확히 세야 한다."""
        from stats import get_streak
        self._add_session("focus", True, date_offset=0)  # 오늘
        self._add_session("focus", True, date_offset=1)  # 어제
        self._add_session("focus", True, date_offset=2)  # 그제
        streak = get_streak(filepath=self.filepath)
        self.assertEqual(streak, 3)


class TestTimer(unittest.TestCase):
    """timer.py 테스트."""

    def test_render_progress_bar_start(self):
        """시작 시점(elapsed=0) 진행률 바 형식 확인."""
        from timer import _render_progress_bar
        bar = _render_progress_bar(0, 100)
        self.assertIn("]", bar)
        self.assertIn("남음", bar)

    def test_render_progress_bar_end(self):
        """완료 시점(elapsed==total) 진행률 바가 꽉 차야 한다."""
        from timer import _render_progress_bar
        bar = _render_progress_bar(100, 100)
        self.assertIn("]", bar)

    def test_run_timer_completes_with_fast_tick(self):
        """tick_fn 주입으로 실제 sleep 없이 타이머가 완료되어야 한다."""
        from timer import run_timer
        start, end, completed = run_timer(duration_seconds=3, label="테스트", tick_fn=lambda: None)
        self.assertTrue(completed)
        self.assertIsInstance(start, datetime)
        self.assertIsInstance(end, datetime)
        self.assertGreaterEqual((end - start).total_seconds(), 0)

    def test_run_timer_interrupted_returns_not_completed(self):
        """KeyboardInterrupt 발생 시 completed=False를 반환해야 한다."""
        from timer import run_timer

        call_count = [0]

        def tick_that_interrupts():
            call_count[0] += 1
            if call_count[0] >= 2:
                raise KeyboardInterrupt()

        _, _, completed = run_timer(duration_seconds=10, label="테스트", tick_fn=tick_that_interrupts)
        self.assertFalse(completed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
