"""
북마크 API 테스트
표준 라이브러리(unittest, http.server, threading)만 사용
"""
import json
import os
import sys
import threading
import unittest
import urllib.request
import urllib.error

# 테스트용 DB 파일 설정
TEST_DB = "test_bookmarks.json"
os.environ["BOOKMARK_DB"] = TEST_DB

import database
from app import BookmarkHandler
from http.server import HTTPServer

TEST_PORT = 18765
BASE_URL = f"http://localhost:{TEST_PORT}"


def api(method: str, path: str, body: dict = None):
    """헬퍼: HTTP 요청 실행 후 (status, body_dict) 반환."""
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


class TestBookmarkAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 테스트 서버 시작
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
        # 각 테스트 전에 DB 초기화
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    # ── 헬스 체크 ──────────────────────────────────────────────
    def test_health(self):
        status, body = api("GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    # ── 북마크 생성 ────────────────────────────────────────────
    def test_create_bookmark(self):
        status, body = api("POST", "/bookmarks", {
            "title": "Python 공식 문서",
            "url": "https://docs.python.org",
        })
        self.assertEqual(status, 201)
        self.assertIn("id", body)
        self.assertEqual(body["title"], "Python 공식 문서")
        self.assertEqual(body["url"], "https://docs.python.org")

    def test_create_bookmark_with_description(self):
        status, body = api("POST", "/bookmarks", {
            "title": "GitHub",
            "url": "https://github.com",
            "description": "코드 저장소",
        })
        self.assertEqual(status, 201)
        self.assertEqual(body["description"], "코드 저장소")

    def test_create_bookmark_missing_title(self):
        status, body = api("POST", "/bookmarks", {"url": "https://example.com"})
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    def test_create_bookmark_missing_url(self):
        status, body = api("POST", "/bookmarks", {"title": "Example"})
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    def test_create_bookmark_invalid_url(self):
        status, body = api("POST", "/bookmarks", {
            "title": "Invalid",
            "url": "not-a-url",
        })
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    # ── 북마크 목록 조회 ───────────────────────────────────────
    def test_list_bookmarks_empty(self):
        status, body = api("GET", "/bookmarks")
        self.assertEqual(status, 200)
        self.assertEqual(body, [])

    def test_list_bookmarks(self):
        api("POST", "/bookmarks", {"title": "A", "url": "https://a.com"})
        api("POST", "/bookmarks", {"title": "B", "url": "https://b.com"})
        status, body = api("GET", "/bookmarks")
        self.assertEqual(status, 200)
        self.assertEqual(len(body), 2)

    # ── 북마크 단건 조회 ───────────────────────────────────────
    def test_get_bookmark(self):
        _, created = api("POST", "/bookmarks", {"title": "X", "url": "https://x.com"})
        status, body = api("GET", f"/bookmarks/{created['id']}")
        self.assertEqual(status, 200)
        self.assertEqual(body["id"], created["id"])

    def test_get_bookmark_not_found(self):
        status, body = api("GET", "/bookmarks/nonexistent-id")
        self.assertEqual(status, 404)

    # ── 북마크 수정 ────────────────────────────────────────────
    def test_update_bookmark(self):
        _, created = api("POST", "/bookmarks", {"title": "Old", "url": "https://old.com"})
        status, body = api("PUT", f"/bookmarks/{created['id']}", {
            "title": "New",
            "url": "https://new.com",
        })
        self.assertEqual(status, 200)
        self.assertEqual(body["title"], "New")

    def test_update_bookmark_not_found(self):
        status, _ = api("PUT", "/bookmarks/nonexistent-id", {
            "title": "X",
            "url": "https://x.com",
        })
        self.assertEqual(status, 404)

    # ── 북마크 삭제 ────────────────────────────────────────────
    def test_delete_bookmark(self):
        _, created = api("POST", "/bookmarks", {"title": "Del", "url": "https://del.com"})
        status, body = api("DELETE", f"/bookmarks/{created['id']}")
        self.assertEqual(status, 200)
        _, check = api("GET", f"/bookmarks/{created['id']}")
        self.assertEqual(_, 404)

    def test_delete_bookmark_not_found(self):
        status, _ = api("DELETE", "/bookmarks/nonexistent-id")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
