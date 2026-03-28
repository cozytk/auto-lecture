"""
북마크 API 테스트 (Round 1 - AGENTS.md 없음)
표준 라이브러리만 사용
"""

import json
import os
import threading
import unittest
import urllib.request
import urllib.error

TEST_DB = "test_bookmarks_r1.json"
os.environ["BOOKMARK_DB"] = TEST_DB

import database
from app import BookmarkHandler
from http.server import HTTPServer

TEST_PORT = 18766
BASE_URL = f"http://localhost:{TEST_PORT}"


def api(method: str, path: str, body: dict = None):
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
        body = json.loads(e.read().decode("utf-8"))
        e.close()
        return e.code, body


class TestRound1API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("", TEST_PORT), BookmarkHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=1)
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_health(self):
        status, body = api("GET", "/health")
        self.assertEqual(status, 200)

    def test_create_and_list(self):
        api("POST", "/bookmarks", {"title": "Test", "url": "https://test.com"})
        status, body = api("GET", "/bookmarks")
        self.assertEqual(status, 200)
        self.assertEqual(len(body), 1)

    def test_create_bookmark_with_category(self):
        status, body = api(
            "POST",
            "/bookmarks",
            {"title": "Tech", "url": "https://tech.com", "category": "tech"},
        )
        self.assertEqual(status, 201)
        self.assertEqual(body["category"], "tech")

    def test_list_bookmarks_filtered_by_category(self):
        api(
            "POST",
            "/bookmarks",
            {"title": "Tech", "url": "https://tech.com", "category": "tech"},
        )
        api(
            "POST",
            "/bookmarks",
            {"title": "News", "url": "https://news.com", "category": "news"},
        )
        api("POST", "/bookmarks", {"title": "No Category", "url": "https://none.com"})

        status, body = api("GET", "/bookmarks?category=tech")

        self.assertEqual(status, 200)
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["title"], "Tech")
        self.assertEqual(body[0]["category"], "tech")

    def test_crud(self):
        _, created = api(
            "POST", "/bookmarks", {"title": "CRUD", "url": "https://crud.com"}
        )
        bid = created["id"]

        # Read
        status, body = api("GET", f"/bookmarks/{bid}")
        self.assertEqual(status, 200)

        # Update
        status, body = api(
            "PUT",
            f"/bookmarks/{bid}",
            {"title": "Updated", "url": "https://updated.com"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["title"], "Updated")

        # Delete
        status, _ = api("DELETE", f"/bookmarks/{bid}")
        self.assertEqual(status, 200)

        # Gone
        status, _ = api("GET", f"/bookmarks/{bid}")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
