"""
북마크 관리 REST API 서버
표준 라이브러리(http.server, json, logging)만 사용
"""
import json
import logging
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import database
import validators
from models import Bookmark

PORT = 8000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def json_response(handler, status: int, body: dict) -> None:
    """JSON 응답을 전송한다.

    Args:
        handler: BaseHTTPRequestHandler 인스턴스.
        status: HTTP 상태 코드.
        body: 응답 바디 딕셔너리.
    """
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


def parse_body(handler) -> dict:
    """요청 바디를 JSON으로 파싱한다.

    Args:
        handler: BaseHTTPRequestHandler 인스턴스.

    Returns:
        파싱된 딕셔너리. 바디가 없으면 빈 딕셔너리.

    Raises:
        json.JSONDecodeError: JSON 파싱 실패 시.
    """
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    return json.loads(raw.decode("utf-8"))


class BookmarkHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002
        logger.info("[%s] %s", self.address_string(), format % args)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        # GET /bookmarks
        if path == "/bookmarks":
            bookmarks = database.get_all()
            json_response(self, 200, [b.to_dict() for b in bookmarks])

        # GET /bookmarks/<id>
        elif path.startswith("/bookmarks/"):
            bookmark_id = path[len("/bookmarks/"):]
            bookmark = database.get_by_id(bookmark_id)
            if bookmark is None:
                json_response(self, 404, {"error": "북마크를 찾을 수 없습니다"})
            else:
                json_response(self, 200, bookmark.to_dict())

        # GET /health
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
                logger.error("JSON 파싱 실패")
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
            )
            created = database.create(bookmark)
            json_response(self, 201, created.to_dict())

        else:
            json_response(self, 404, {"error": "경로를 찾을 수 없습니다"})

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path.startswith("/bookmarks/"):
            bookmark_id = path[len("/bookmarks/"):]
            existing = database.get_by_id(bookmark_id)
            if existing is None:
                json_response(self, 404, {"error": "북마크를 찾을 수 없습니다"})
                return

            try:
                data = parse_body(self)
            except (json.JSONDecodeError, ValueError):
                logger.error("JSON 파싱 실패")
                json_response(self, 400, {"error": "올바르지 않은 JSON 형식입니다"})
                return

            ok, err = validators.validate_bookmark_input(data)
            if not ok:
                json_response(self, 400, {"error": err})
                return

            existing.title = data["title"]
            existing.url = data["url"]
            existing.description = data.get("description", existing.description)
            existing.updated_at = datetime.now().isoformat()
            updated = database.update(existing)
            json_response(self, 200, updated.to_dict())

        else:
            json_response(self, 404, {"error": "경로를 찾을 수 없습니다"})

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path.startswith("/bookmarks/"):
            bookmark_id = path[len("/bookmarks/"):]
            deleted = database.delete(bookmark_id)
            if not deleted:
                json_response(self, 404, {"error": "북마크를 찾을 수 없습니다"})
            else:
                json_response(self, 200, {"message": "삭제되었습니다"})

        else:
            json_response(self, 404, {"error": "경로를 찾을 수 없습니다"})


def run(port: int = PORT) -> None:
    """API 서버를 시작한다.

    Args:
        port: 수신 포트 번호.
    """
    server = HTTPServer(("", port), BookmarkHandler)
    logger.info("북마크 API 서버 시작: http://localhost:%d", port)
    print("종료하려면 Ctrl+C를 누르세요")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("서버 종료")
        server.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run(port)
