// ─── src/components/PostCard.tsx ───
// 게시글 카드 (필수 2, 4)

import type { Post } from "../types";
import CommentList from "./CommentList";

interface PostCardProps {
  post: Post;
  onDelete: (id: number) => Promise<void>;
}

export default function PostCard({ post, onDelete }: PostCardProps) {
  // TODO (필수 4): 삭제 버튼의 onClick에서 onDelete(post.id)를 호출하세요

  return (
    <div className="p-4 rounded-xl border border-slate-200 bg-white space-y-3 hover:shadow-sm transition">
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-slate-800 text-sm leading-snug">
          {post.title}
        </h3>
        <button
          // TODO (필수 4): onClick={() => onDelete(post.id)}
          className="shrink-0 w-7 h-7 flex items-center justify-center rounded-lg text-slate-400 hover:text-rose-500 hover:bg-rose-50 transition"
          title="Delete"
        >
          ✕
        </button>
      </div>
      <p className="text-xs text-slate-500 leading-relaxed">{post.body}</p>
      <CommentList postId={post.id} />
    </div>
  );
}
