// ─── src/components/TodoSection.jsx ───
// 할 일 관리 (필수 5)
// Props: userId (number)

import { useState, useEffect } from "react";
import { Skeleton } from "./ui/Skeleton";

const API = "https://jsonplaceholder.typicode.com";

// ── TodoItem (스타일 완성됨) ──
function TodoItem({ todo, onToggle }) {
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

export default function TodoSection({ userId }) {
  // TODO (필수 5-a): todos 상태를 만드세요
  // const [todos, setTodos] = useState([])

  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("all");

  // TODO (필수 5-b): userId가 바뀔 때마다 할 일 목록을 fetch하세요
  //   - URL: `${API}/todos?userId=${userId}`
  //   - 힌트: useEffect의 의존성 배열에 userId를 넣으세요
  //   - userId가 없으면 fetch하지 마세요
  useEffect(() => {
    if (!userId) return;
    // 여기에 fetch 로직을 구현하세요
  }, [userId]);

  // TODO (필수 5-c): 완료 토글 함수를 구현하세요
  //   - 해당 todo의 completed를 반전시키세요
  //   - PATCH `${API}/todos/${id}`로 요청도 보내세요 (응답은 무시해도 OK)
  //   - 힌트: setTodos(prev => prev.map(...))
  const toggleTodo = (id) => {
    // 여기에 구현하세요
  };

  // 필터링 로직 (완성됨 — filter 상태에 따라 목록을 걸러냅니다)
  const todos = []; // TODO: 위에서 만든 state로 교체하세요
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
      {/* 필터 버튼 + 완료 카운트 */}
      <div className="flex items-center justify-between">
        <div className="flex gap-1">
          {["all", "pending", "done"].map((f) => (
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

      {/* 진행률 바 */}
      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-emerald-500 rounded-full transition-all duration-500"
          style={{
            width: `${
              todos.length ? (doneCount / todos.length) * 100 : 0
            }%`,
          }}
        />
      </div>

      {/* 할 일 목록 */}
      <div className="space-y-1 max-h-80 overflow-y-auto">
        {filtered.map((todo) => (
          <TodoItem key={todo.id} todo={todo} onToggle={toggleTodo} />
        ))}
      </div>
    </div>
  );
}
