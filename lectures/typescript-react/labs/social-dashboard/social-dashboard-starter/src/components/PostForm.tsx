// ─── src/components/PostForm.tsx ───
// 게시글 작성 폼 (필수 3)

import { useState } from "react";

interface PostFormProps {
  onSubmit: (data: { title: string; body: string }) => Promise<void>;
}

export default function PostForm({ onSubmit }: PostFormProps) {
  // TODO (필수 3-a): title, body 상태를 만드세요
  // const [title, setTitle] = useState<string>("")
  // const [body, setBody] = useState<string>("")

  const [submitting, setSubmitting] = useState(false);

  // TODO (필수 3-b): 폼 제출 핸들러를 만드세요
  //   1. title이 빈 문자열이면 return (유효성 검사)
  //   2. setSubmitting(true)
  //   3. await onSubmit({ title: title.trim(), body: body.trim() })
  //   4. 제출 후 input 초기화 + setSubmitting(false)
  const handleSubmit = async (): Promise<void> => {
    // 여기에 구현하세요
  };

  return (
    <div className="p-4 rounded-xl border border-dashed border-slate-300 bg-slate-50/50 space-y-3">
      <input
        type="text"
        // TODO: value={title} onChange={(e) => setTitle(e.target.value)}
        placeholder="Post title"
        className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200"
      />
      <textarea
        // TODO: value={body} onChange={(e) => setBody(e.target.value)}
        placeholder="Write something..."
        rows={2}
        className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-200"
      />
      <button
        onClick={handleSubmit}
        disabled={submitting /* TODO: || !title.trim() */}
        className="px-4 py-2 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 disabled:opacity-40 disabled:cursor-not-allowed transition"
      >
        {submitting ? "Posting..." : "Add Post"}
      </button>
    </div>
  );
}
