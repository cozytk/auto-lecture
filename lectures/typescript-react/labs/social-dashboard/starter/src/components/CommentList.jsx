// ─── src/components/CommentList.jsx ───
// 댓글 목록 — 펼치기/접기 (필수 6)
// Props: postId (number)

import { useState } from "react";

const API = "https://jsonplaceholder.typicode.com";

export default function CommentList({ postId }) {
  // TODO (필수 6-a): comments 상태와 open 상태를 만드세요
  // const [comments, setComments] = useState(???)
  // const [open, setOpen] = useState(???)

  const [loading, setLoading] = useState(false);

  // TODO (필수 6-b): toggle 함수를 구현하세요
  //   1. open이 false이고 comments가 비어있으면:
  //      - setLoading(true)
  //      - fetch(`${API}/posts/${postId}/comments`)로 댓글을 가져오세요
  //      - 응답을 comments state에 저장하세요
  //      - setLoading(false)
  //   2. open 상태를 토글하세요
  const toggle = async () => {
    // 여기에 구현하세요
  };

  return (
    <div>
      <button
        onClick={toggle}
        className="text-xs text-indigo-500 hover:text-indigo-700 font-medium transition"
      >
        {loading ? "Loading..." : "Show comments"
        /* TODO: open 상태에 따라 "Hide comments" / "Show comments" 전환 */}
      </button>

      {/* TODO (필수 6-c): open이 true일 때 댓글 목록을 렌더링하세요 */}
      {/* 아래 JSX를 조건부로 보여주세요 */}
      {false && (
        <div className="mt-3 space-y-2 pl-3 border-l-2 border-slate-200">
          {/* TODO: comments.map()으로 각 댓글을 렌더링하세요 */}
          {/* 각 댓글에서 c.name, c.email, c.body를 표시 */}
          <div className="text-xs">
            <span className="font-semibold text-slate-700">Comment Name</span>
            <span className="text-slate-400 ml-1">(email@example.com)</span>
            <p className="text-slate-500 mt-0.5 leading-relaxed">
              Comment body goes here...
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
