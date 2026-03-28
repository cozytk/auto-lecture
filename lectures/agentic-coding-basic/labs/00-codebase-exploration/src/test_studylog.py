"""
studylog 단위 테스트
실행: python3 -m unittest test_studylog -v
"""

import json
import os
import sys
import shutil
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))


class StudylogTestBase(unittest.TestCase):
    """각 테스트마다 임시 저장소를 사용하는 베이스 클래스."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.tmp_dir, "data.json")

        import config
        import store

        config._config_cache = None
        self._orig_default = dict(config._DEFAULT)
        config._DEFAULT["storage_path"] = self.data_file

        from pathlib import Path

        self._orig_data_path = store._data_path
        store._data_path = lambda: Path(self.data_file)

    def tearDown(self):
        import config
        import store

        config._config_cache = None
        config._DEFAULT.update(self._orig_default)
        store._data_path = self._orig_data_path
        shutil.rmtree(self.tmp_dir, ignore_errors=True)


# ── store 테스트 ──────────────────────────────────────────────


class TestAddSession(StudylogTestBase):
    def test_add_returns_session_with_id(self):
        import store

        s = store.add_session("Python")
        self.assertIn("id", s)
        self.assertEqual(len(s["id"]), 8)

    def test_add_saves_topic(self):
        import store

        s = store.add_session("JavaScript")
        self.assertEqual(s["topic"], "JavaScript")

    def test_add_sets_status_active(self):
        import store

        s = store.add_session("Go")
        self.assertEqual(s["status"], "active")

    def test_add_persists_to_file(self):
        import store

        store.add_session("Rust")
        self.assertTrue(os.path.exists(self.data_file))

    def test_add_with_tags(self):
        import store

        s = store.add_session("Python", tags=["기초", "문법"])
        self.assertEqual(s["tags"], ["기초", "문법"])


class TestListSessions(StudylogTestBase):
    def test_empty_returns_empty(self):
        import store

        self.assertEqual(store.list_sessions(), [])

    def test_sorted_by_started_at_desc(self):
        import store

        data = {
            "sessions": {
                "aaa": {
                    "id": "aaa",
                    "topic": "이전",
                    "started_at": "2024-01-01 09:00",
                    "status": "completed",
                    "tags": [],
                    "duration_minutes": 30,
                    "ended_at": "2024-01-01 09:30",
                    "notes": "",
                },
                "bbb": {
                    "id": "bbb",
                    "topic": "최신",
                    "started_at": "2024-01-02 09:00",
                    "status": "completed",
                    "tags": [],
                    "duration_minutes": 60,
                    "ended_at": "2024-01-02 10:00",
                    "notes": "",
                },
            },
            "version": 2,
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f)

        sessions = store.list_sessions()
        self.assertEqual(sessions[0]["topic"], "최신")


class TestDeleteSession(StudylogTestBase):
    def test_delete_existing(self):
        import store

        s = store.add_session("삭제 대상")
        self.assertTrue(store.delete_session(s["id"]))
        self.assertIsNone(store.get_session(s["id"]))

    def test_delete_nonexistent(self):
        import store

        self.assertFalse(store.delete_session("없는id"))


# ── session 테스트 ────────────────────────────────────────────


class TestSession(StudylogTestBase):
    def test_start_creates_active_session(self):
        import session

        s = session.start("테스트 주제")
        self.assertEqual(s["status"], "active")
        self.assertEqual(s["topic"], "테스트 주제")

    def test_start_while_active_raises(self):
        import session

        session.start("첫 번째")
        with self.assertRaises(ValueError):
            session.start("두 번째")

    def test_stop_completes_session(self):
        import session

        session.start("종료 테스트")
        s = session.stop(notes="완료")
        self.assertEqual(s["status"], "completed")
        self.assertIsNotNone(s["ended_at"])

    def test_stop_without_active_raises(self):
        import session

        with self.assertRaises(ValueError):
            session.stop()

    def test_current_returns_none_when_idle(self):
        import session

        self.assertIsNone(session.current())

    def test_current_returns_session_with_elapsed(self):
        import session

        session.start("경과 시간 테스트")
        cur = session.current()
        self.assertIsNotNone(cur)
        self.assertIn("elapsed_minutes", cur)


# ── engine 테스트 ─────────────────────────────────────────────


class TestEngine(StudylogTestBase):
    def _make_sessions(self):
        return [
            {
                "topic": "Python",
                "status": "completed",
                "duration_minutes": 60,
                "started_at": "2024-03-01 09:00",
                "tags": ["기초"],
            },
            {
                "topic": "Python",
                "status": "completed",
                "duration_minutes": 45,
                "started_at": "2024-03-02 14:00",
                "tags": ["심화"],
            },
            {
                "topic": "JavaScript",
                "status": "completed",
                "duration_minutes": 30,
                "started_at": "2024-03-02 16:00",
                "tags": [],
            },
            {
                "topic": "Go",
                "status": "active",
                "duration_minutes": 0,
                "started_at": "2024-03-03 09:00",
                "tags": [],
            },
        ]

    def test_total_time_excludes_active(self):
        import engine

        total = engine.total_time(self._make_sessions())
        self.assertEqual(total, 135)

    def test_by_topic(self):
        import engine

        topics = engine.by_topic(self._make_sessions())
        self.assertEqual(topics["Python"]["minutes"], 105)
        self.assertEqual(topics["Python"]["count"], 2)

    def test_average_duration(self):
        import engine

        avg = engine.average_duration(self._make_sessions())
        self.assertEqual(avg, 45.0)

    def test_average_duration_empty(self):
        import engine

        self.assertEqual(engine.average_duration([]), 0)


# ── display 테스트 ────────────────────────────────────────────


class TestDisplay(StudylogTestBase):
    def test_format_duration_minutes(self):
        import display

        self.assertEqual(display.format_duration(45), "45분")

    def test_format_duration_hours(self):
        import display

        self.assertEqual(display.format_duration(120), "2시간")

    def test_format_duration_mixed(self):
        import display

        self.assertEqual(display.format_duration(90), "1시간 30분")

    def test_render_session_list_empty(self):
        import display

        result = display.render_session_list([])
        self.assertIn("없습니다", result)


# ── CLI 통합 테스트 ───────────────────────────────────────────


class TestCLI(StudylogTestBase):
    def test_start_command(self):
        from studylog import build_parser

        parser = build_parser()

        captured = StringIO()
        with patch("sys.stdout", captured):
            args = parser.parse_args(["start", "CLI 테스트"])
            args.func(args)

        self.assertIn("학습 시작", captured.getvalue())

    def test_list_command_empty(self):
        from studylog import build_parser

        parser = build_parser()

        captured = StringIO()
        with patch("sys.stdout", captured):
            args = parser.parse_args(["list"])
            args.func(args)

        self.assertIn("없습니다", captured.getvalue())


if __name__ == "__main__":
    unittest.main()
