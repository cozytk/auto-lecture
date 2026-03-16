// ─── src/components/PostForm.tsx (정답) ───

import { useState } from "react";

interface PostFormProps {
  onSubmit: (data: { title: string; body: string }) => Promise<void>;
}

export default function PostForm({ onSubmit }: PostFormProps) {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (): Promise<void> => {
    if (!title.trim()) return;
    setSubmitting(true);
    try {
      await onSubmit({ title: title.trim(), body: body.trim() });
      setTitle("");
      setBody("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-4 rounded-xl border border-dashed border-slate-300 bg-slate-50/50 space-y-3">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Post title"
        className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-200"
      />
      <textarea
        value={body}
        onChange={(e) => setBody(e.target.value)}
        placeholder="Write something..."
        rows={2}
        className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-200"
      />
      <button
        onClick={handleSubmit}
        disabled={submitting || !title.trim()}
        className="px-4 py-2 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 disabled:opacity-40 disabled:cursor-not-allowed transition"
      >
        {submitting ? "Posting..." : "Add Post"}
      </button>
    </div>
  );
}
