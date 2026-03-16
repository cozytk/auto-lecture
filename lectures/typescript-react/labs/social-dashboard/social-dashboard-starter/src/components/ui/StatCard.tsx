// ─── src/components/ui/StatCard.tsx ───
// 대시보드 통계 카드 (도전 8)
// 이미 완성되어 있으니 그대로 사용하세요

type ColorKey = "blue" | "emerald" | "amber" | "purple" | "rose" | "cyan";

interface StatCardProps {
  icon: string;
  label: string;
  value: string | number | null;
  color: ColorKey;
}

const COLORS: Record<ColorKey, string> = {
  blue: "bg-blue-50 text-blue-600 border-blue-200",
  emerald: "bg-emerald-50 text-emerald-600 border-emerald-200",
  amber: "bg-amber-50 text-amber-600 border-amber-200",
  purple: "bg-purple-50 text-purple-600 border-purple-200",
  rose: "bg-rose-50 text-rose-600 border-rose-200",
  cyan: "bg-cyan-50 text-cyan-600 border-cyan-200",
};

export default function StatCard({ icon, label, value, color }: StatCardProps) {
  return (
    <div className={`rounded-xl border p-4 ${COLORS[color]}`}>
      <div className="flex items-center gap-2 mb-1">
        <span className="text-lg">{icon}</span>
        <span className="text-xs font-semibold uppercase tracking-wider opacity-70">
          {label}
        </span>
      </div>
      <div className="text-2xl font-bold">{value ?? "—"}</div>
    </div>
  );
}
