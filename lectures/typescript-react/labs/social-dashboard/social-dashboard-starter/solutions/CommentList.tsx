// ─── src/components/CommentList.tsx (정답) ───

import { useState } from "react";
import type { Comment } from "../types";

const API = "https://jsonplaceholder.typicode.com";

interface CommentListProps {
  postId: number;
}

export default function CommentList({ postId }: CommentListProps) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const toggle = async (): Promise<void> => {
    if (!open && comments.length === 0) {
      setLoading(true);
      const res = await fetch(`${API}/posts/${postId}/comments`);
      const data: Comment[] = await res.json();
      setComments(data);
      setLoading(false);
    }
    setOpen((prev) => !prev);
  };

  return (
    <div>
      <button
        onClick={toggle}
        className="text-xs text-indigo-500 hover:text-indigo-700 font-medium transition"
      >
        {loading ? "Loading..." : open ? "Hide comments" : "Show comments"}
      </button>

      {open && (
        <div className="mt-3 space-y-2 pl-3 border-l-2 border-slate-200">
          {comments.map((c) => (
            <div key={c.id} className="text-xs">
              <span className="font-semibold text-slate-700">{c.name}</span>
              <span className="text-slate-400 ml-1">({c.email})</span>
              <p className="text-slate-500 mt-0.5 leading-relaxed">{c.body}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
