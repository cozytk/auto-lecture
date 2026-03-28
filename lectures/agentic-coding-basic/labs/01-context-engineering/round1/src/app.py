"""
북마크 관리 REST API 서버
표준 라이브러리(http.server, json)만 사용
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import database
import validators
from models import Bookmark

PORT = 8000


def json_response(handler, status: int, body: dict) -> None:
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


def parse_body(handler) -> dict:
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    return json.loads(raw.decode("utf-8"))


class BookmarkHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002
        print(f"[{self.address_string()}] {format % args}")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query = parse_qs(parsed.query)

        if path == "/bookmarks":
            category = query.get("category", [None])[0]
            if category is None:
                bookmarks = database.get_all()
            else:
                bookmarks = database.get_all_by_category(category)
            json_response(self, 200, [b.to_dict() for b in bookmarks])

        elif path.startswith("/bookmarks/"):
            bookmark_id = path[len("/bookmarks/") :]
            bookmark = database.get_by_id(bookmark_id)
            if bookmark is None:
                json_response(self, 404, {"error": "북마크를 찾을 수 없습니다"})
            else:
                json_response(self, 200, bookmark.to_dict())

        elif path == "/health":
            json_response(self, 200, {"status": "ok"})

        else:
            json_response(self, 404, {"error": "경로를 찾을 수 없습니다"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/bookmarks":
            try:
                data = parse_body(self)
            except (json.JSONDecodeError, ValueError):
                json_response(self, 400, {"error": "올바르지 않은 JSON 형식입니다"})
                return

            ok, err = validators.validate_bookmark_input(data)
            if not ok:
                json_response(self, 400, {"error": err})
                return

            bookmark = Bookmark(
                title=data["title"],
                url=data["url"],
                description=data.get("description"),
                category=data.get("category"),
            )
            created = database.create(bookmark)
            json_response(self, 201, created.to_dict())

        else:
            json_response(self, 404, {"error": "경로를 찾을 수 없습니다"})

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path.startswith("/bookmarks/"):
            bookmark_id = path[len("/bookmarks/") :]
            existing = database.get_by_id(bookmark_id)
            if existing is None:
                json_response(self, 404, {"error": "북마크를 찾을 수 없습니다"})
                return

            try:
                data = parse_body(self)
            except (json.JSONDecodeError, ValueError):
                json_response(self, 400, {"error": "올바르지 않은 JSON 형식입니다"})
                return

            ok, err = validators.validate_bookmark_input(data)
            if not ok:
                json_response(self, 400, {"error": err})
                return

            from datetime import datetime

            existing.title = data["title"]
            existing.url = data["url"]
            existing.description = data.get("description", existing.description)
            existing.category = data.get("category", existing.category)
            existing.updated_at = datetime.now().isoformat()
            updated = database.update(existing)
            json_response(self, 200, updated.to_dict())

        else:
            json_response(self, 404, {"error": "경로를 찾을 수 없습니다"})

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path.startswith("/bookmarks/"):
            bookmark_id = path[len("/bookmarks/") :]
            deleted = database.delete(bookmark_id)
            if not deleted:
                json_response(self, 404, {"error": "북마크를 찾을 수 없습니다"})
            else:
                json_response(self, 200, {"message": "삭제되었습니다"})

        else:
            json_response(self, 404, {"error": "경로를 찾을 수 없습니다"})


def run(port: int = PORT):
    server = HTTPServer(("", port), BookmarkHandler)
    print(f"북마크 API 서버 시작: http://localhost:{port}")
    print("종료하려면 Ctrl+C를 누르세요")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다")
        server.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run(port)
