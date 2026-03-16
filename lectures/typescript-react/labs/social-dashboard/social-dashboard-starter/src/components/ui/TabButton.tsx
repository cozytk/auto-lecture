// ─── src/components/ui/TabButton.tsx ───
// 탭 전환 버튼 — 이미 완성되어 있으니 그대로 사용하세요

import type { ReactNode } from "react";

interface TabButtonProps {
  active: boolean;
  onClick: () => void;
  children: ReactNode;
}

export default function TabButton({ active, onClick, children }: TabButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition ${
        active
          ? "bg-indigo-500 text-white shadow-sm"
          : "text-slate-500 hover:bg-slate-100"
      }`}
    >
      {children}
    </button>
  );
}
