"""
북마크 API 테스트 (Round 2 - 기본 AGENTS.md 있음)
표준 라이브러리만 사용
"""

import json
import os
import threading
import unittest
import urllib.request
import urllib.error

TEST_DB = "test_bookmarks_r2.json"
os.environ["BOOKMARK_DB"] = TEST_DB

from app import BookmarkHandler
from http.server import HTTPServer

TEST_PORT = 18767
BASE_URL = f"http://localhost:{TEST_PORT}"


def api(method: str, path: str, body: dict = None):
    """API 요청 헬퍼. (status, body_dict) 반환."""
    url = BASE_URL + path
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
        req.add_header("Content-Length", str(len(data)))
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


class TestRound2API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("", TEST_PORT), BookmarkHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    # ── 헬스 체크 ──────────────────────────────────────────────
    def test_health_returns_ok(self):
        status, body = api("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    # ── 북마크 생성 ────────────────────────────────────────────
    def test_create_bookmark_success(self):
        status, body = api(
            "POST",
            "/bookmarks",
            {
                "title": "Python 공식 문서",
                "url": "https://docs.python.org",
            },
        )
        self.assertEqual(status, 201)
        self.assertIn("id", body)

    def test_create_bookmark_with_category_success(self):
        status, body = api(
            "POST",
            "/bookmarks",
            {
                "title": "Python 공식 문서",
                "url": "https://docs.python.org",
                "category": "tech",
            },
        )
        self.assertEqual(status, 201)
        self.assertEqual(body["category"], "tech")

    def test_create_bookmark_missing_title_returns_400(self):
        status, body = api("POST", "/bookmarks", {"url": "https://example.com"})
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    def test_create_bookmark_missing_url_returns_400(self):
        status, body = api("POST", "/bookmarks", {"title": "Example"})
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    def test_create_bookmark_invalid_url_returns_400(self):
        status, body = api(
            "POST",
            "/bookmarks",
            {
                "title": "Invalid",
                "url": "not-a-url",
            },
        )
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    # ── 목록 조회 ──────────────────────────────────────────────
    def test_list_bookmarks_empty_returns_empty_list(self):
        status, body = api("GET", "/bookmarks")
        self.assertEqual(status, 200)
        self.assertEqual(body, [])

    def test_list_bookmarks_returns_all(self):
        api("POST", "/bookmarks", {"title": "A", "url": "https://a.com"})
        api("POST", "/bookmarks", {"title": "B", "url": "https://b.com"})
        status, body = api("GET", "/bookmarks")
        self.assertEqual(status, 200)
        self.assertEqual(len(body), 2)

    def test_list_bookmarks_filters_by_category(self):
        api(
            "POST",
            "/bookmarks",
            {
                "title": "Python",
                "url": "https://python.org",
                "category": "tech",
            },
        )
        api(
            "POST",
            "/bookmarks",
            {
                "title": "요리",
                "url": "https://cooking.example.com",
                "category": "food",
            },
        )
        api(
            "POST",
            "/bookmarks",
            {"title": "분류 없음", "url": "https://etc.example.com"},
        )

        status, body = api("GET", "/bookmarks?category=tech")

        self.assertEqual(status, 200)
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["category"], "tech")

    # ── 단건 조회 ──────────────────────────────────────────────
    def test_get_bookmark_success(self):
        _, created = api("POST", "/bookmarks", {"title": "X", "url": "https://x.com"})
        status, body = api("GET", f"/bookmarks/{created['id']}")
        self.assertEqual(status, 200)
        self.assertEqual(body["id"], created["id"])

    def test_get_bookmark_not_found_returns_404(self):
        status, _ = api("GET", "/bookmarks/nonexistent-id")
        self.assertEqual(status, 404)

    # ── 수정 ──────────────────────────────────────────────────
    def test_update_bookmark_success(self):
        _, created = api(
            "POST", "/bookmarks", {"title": "Old", "url": "https://old.com"}
        )
        status, body = api(
            "PUT",
            f"/bookmarks/{created['id']}",
            {
                "title": "New",
                "url": "https://new.com",
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["title"], "New")

    def test_update_bookmark_not_found_returns_404(self):
        status, _ = api(
            "PUT",
            "/bookmarks/nonexistent-id",
            {
                "title": "X",
                "url": "https://x.com",
            },
        )
        self.assertEqual(status, 404)

    # ── 삭제 ──────────────────────────────────────────────────
    def test_delete_bookmark_success(self):
        _, created = api(
            "POST", "/bookmarks", {"title": "Del", "url": "https://del.com"}
        )
        status, _ = api("DELETE", f"/bookmarks/{created['id']}")
        self.assertEqual(status, 200)
        status, _ = api("GET", f"/bookmarks/{created['id']}")
        self.assertEqual(status, 404)

    def test_delete_bookmark_not_found_returns_404(self):
        status, _ = api("DELETE", "/bookmarks/nonexistent-id")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
