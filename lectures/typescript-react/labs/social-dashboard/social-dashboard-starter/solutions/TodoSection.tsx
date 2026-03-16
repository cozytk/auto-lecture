// ─── src/components/TodoSection.tsx (정답) ───

import { useState, useEffect } from "react";
import { Skeleton } from "./ui/Skeleton";
import type { Todo, StatsUpdateFn } from "../types";

const API = "https://jsonplaceholder.typicode.com";

// ── TodoItem (스타일 완성됨) ──
interface TodoItemProps {
  todo: Todo;
  onToggle: (id: number) => void;
}

function TodoItem({ todo, onToggle }: TodoItemProps) {
  return (
    <button
      onClick={() => onToggle(todo.id)}
      className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-left transition text-sm ${
        todo.completed
          ? "bg-emerald-50 text-emerald-700"
          : "bg-white hover:bg-slate-50 text-slate-700"
      }`}
    >
      <div
        className={`w-5 h-5 shrink-0 rounded-md border-2 flex items-center justify-center transition ${
          todo.completed
            ? "border-emerald-500 bg-emerald-500"
            : "border-slate-300"
        }`}
      >
        {todo.completed && (
          <svg
            className="w-3 h-3 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="3"
              d="M5 13l4 4L19 7"
            />
          </svg>
        )}
      </div>
      <span className={todo.completed ? "line-through opacity-60" : ""}>
        {todo.title}
      </span>
    </button>
  );
}

// ── TodoSection ──
interface TodoSectionProps {
  userId: number;
  onStatsUpdate?: StatsUpdateFn;
}

export default function TodoSection({ userId, onStatsUpdate }: TodoSectionProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState<"all" | "pending" | "done">("all");

  // 필수 5-b: userId가 바뀔 때마다 할 일 목록 fetch
  useEffect(() => {
    if (!userId) return;
    setLoading(true);
    const fetchTodos = async () => {
      const res = await fetch(`${API}/todos?userId=${userId}`);
      const data: Todo[] = await res.json();
      setTodos(data);
      setLoading(false);
    };
    fetchTodos();
  }, [userId]);

  // 필수 5-c + 도전 11: 완료 토글 + 통계 콜백
  const toggleTodo = (id: number): void => {
    setTodos((prev) =>
      prev.map((t) => {
        if (t.id !== id) return t;

        // 도전 11: 콜백으로 stats 갱신
        if (t.completed) {
          onStatsUpdate?.("todoDone", (prev) => prev - 1);
        } else {
          onStatsUpdate?.("todoDone", (prev) => prev + 1);
        }

        return { ...t, completed: !t.completed };
      })
    );

    // PATCH 요청 (응답 무시)
    fetch(`${API}/todos/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: true }),
    });
  };

  const filtered = todos.filter((t) => {
    if (filter === "done") return t.completed;
    if (filter === "pending") return !t.completed;
    return true;
  });

  const doneCount = todos.filter((t) => t.completed).length;

  if (loading) {
    return (
      <div className="space-y-2">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-10 w-full" />
        ))}
      </div>
    );
  }

  if (!userId) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex gap-1">
          {(["all", "pending", "done"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1 text-xs font-medium rounded-lg transition ${
                filter === f
                  ? "bg-indigo-500 text-white"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {f === "all" ? "All" : f === "done" ? "Done" : "Pending"}
            </button>
          ))}
        </div>
        <span className="text-xs text-slate-500 font-medium">
          {doneCount}/{todos.length}
        </span>
      </div>

      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-emerald-500 rounded-full transition-all duration-500"
          style={{
            width: `${todos.length ? (doneCount / todos.length) * 100 : 0}%`,
          }}
        />
      </div>

      <div className="space-y-1 max-h-80 overflow-y-auto">
        {filtered.map((todo) => (
          <TodoItem key={todo.id} todo={todo} onToggle={toggleTodo} />
        ))}
      </div>
    </div>
  );
}
