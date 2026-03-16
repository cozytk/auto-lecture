// ─── src/components/CommentList.tsx ───
// 댓글 목록 — 펼치기/접기 (필수 6)

import { useState } from "react";
import type { Comment } from "../types";

const API = "https://jsonplaceholder.typicode.com";

interface CommentListProps {
  postId: number;
}

export default function CommentList({ postId }: CommentListProps) {
  // TODO (필수 6-a): comments 상태와 open 상태를 만드세요
  // const [comments, setComments] = useState<Comment[]>([])
  // const [open, setOpen] = useState(false)

  const [loading, setLoading] = useState(false);

  // TODO (필수 6-b): toggle 함수를 구현하세요
  //   1. open이 false이고 comments가 비어있으면:
  //      - setLoading(true)
  //      - const res = await fetch(`${API}/posts/${postId}/comments`)
  //      - const data: Comment[] = await res.json()
  //      - setComments(data)
  //      - setLoading(false)
  //   2. setOpen(prev => !prev)
  const toggle = async (): Promise<void> => {
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
      {false && (
        <div className="mt-3 space-y-2 pl-3 border-l-2 border-slate-200">
          {/* TODO: comments.map((c) => ...) 으로 각 댓글 렌더링 */}
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
