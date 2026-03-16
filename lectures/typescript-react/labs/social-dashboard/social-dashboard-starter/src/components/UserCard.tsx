// ─── src/components/UserCard.tsx ───
// 사용자 카드 컴포넌트 — 스타일 완성됨, 그대로 사용하세요

import type { User } from "../types";

interface UserCardProps {
  user: User;
  selected: boolean;
  onClick: (user: User) => void;
}

export default function UserCard({ user, selected, onClick }: UserCardProps) {
  return (
    <button
      onClick={() => onClick(user)}
      className={`w-full text-left p-4 rounded-xl border transition-all duration-200 ${
        selected
          ? "border-indigo-400 bg-indigo-50 shadow-md shadow-indigo-100"
          : "border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm"
      }`}
    >
      <div className="flex items-center gap-3">
        <div
          className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
            selected
              ? "bg-indigo-500 text-white"
              : "bg-slate-100 text-slate-600"
          }`}
        >
          {user.name.charAt(0)}
        </div>
        <div className="min-w-0">
          <div className="font-semibold text-slate-800 text-sm truncate">
            {user.name}
          </div>
          <div className="text-xs text-slate-500 truncate">{user.email}</div>
          <div className="text-xs text-slate-400 truncate">
            {user.company.name}
          </div>
        </div>
      </div>
    </button>
  );
}
