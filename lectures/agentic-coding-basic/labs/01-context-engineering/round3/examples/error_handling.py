"""
예시: 올바른 에러 핸들링 패턴.
이 파일은 실행용이 아닌 참조용 예시입니다.
"""

# ─── ✅ 올바른 패턴 ────────────────────────────────────────────

# 1. 유효성 검사 실패 → 400 반환
def handle_post_correct(self):
    """올바른 POST 핸들러 예시."""
    try:
        data = parse_body(self)
    except (ValueError, KeyError):
        json_response(self, 400, {"error": "올바르지 않은 JSON 형식입니다"})
        return  # ← 반드시 return으로 흐름 차단

    ok, err = validate_bookmark_input(data)
    if not ok:
        json_response(self, 400, {"error": err})
        return  # ← 반드시 return으로 흐름 차단

    # 정상 처리
    bookmark = create_bookmark(data)
    json_response(self, 201, bookmark.to_dict())


# 2. 존재하지 않는 리소스 → 404 반환
def handle_get_by_id_correct(self, bookmark_id: str):
    """올바른 단건 조회 핸들러 예시."""
    bookmark = database.get_by_id(bookmark_id)
    if bookmark is None:
        json_response(self, 404, {"error": "북마크를 찾을 수 없습니다"})
        return  # ← 반드시 return으로 흐름 차단

    json_response(self, 200, bookmark.to_dict())


# ─── ❌ 금지 패턴 ──────────────────────────────────────────────

# 1. 빈 except 블록
def bad_empty_except():
    try:
        risky_operation()
    except Exception:
        pass  # ← 금지: 에러를 무시하면 디버깅 불가


# 2. 에러 후 return 누락
def bad_no_return(self):
    ok, err = validate_bookmark_input({})
    if not ok:
        json_response(self, 400, {"error": err})
        # ← return이 없으면 이후 코드도 실행됨 (버그)
    bookmark = create_bookmark({})  # ← 유효성 검사 실패해도 여기 도달


# 3. 영어 에러 메시지
def bad_english_error(self):
    json_response(self, 404, {"error": "Not found"})  # ← 금지: 한국어 사용
