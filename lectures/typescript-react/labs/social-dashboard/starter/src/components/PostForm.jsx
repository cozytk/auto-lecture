// ─── src/components/PostForm.jsx ───
// 게시글 작성 폼 (필수 3)
// Props: onSubmit (function) — 부모에서 전달받은 게시글 추가 함수

import { useState } from "react";

export default function PostForm({ onSubmit }) {
  // TODO (필수 3-a): title, body 상태를 만드세요
  // const [title, setTitle] = useState(???)

  // TODO (필수 3-b): 폼 제출 핸들러를 만드세요
  //   1. title이 빈 문자열이면 return (유효성 검사)
  //   2. onSubmit({ title, body })를 호출하세요
  //   3. 제출 후 input을 초기화하세요
  const handleSubmit = () => {
    // 여기에 구현하세요
  };

  return (
    <div className="p-4 rounded-xl border border-dashed border-slate-300 bg-slate-50/50 space-y-3">
      <input
        type="text"
        // TODO: value와 onChange를 연결하세요
        placeholder="Post title"
        className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200"
      />
      <textarea
        // TODO: value와 onChange를 연결하세요
        placeholder="Write something..."
        rows={2}
        className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-200"
      />
      <button
        onClick={handleSubmit}
        // TODO: title이 비어있으면 disabled 처리하세요
        className="px-4 py-2 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 disabled:opacity-40 disabled:cursor-not-allowed transition"
      >
        Add Post
      </button>
    </div>
  );
}
