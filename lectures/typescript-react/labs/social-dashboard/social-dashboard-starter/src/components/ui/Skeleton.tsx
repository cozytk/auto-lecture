// ─── src/components/ui/Skeleton.tsx ───
// 로딩 중 표시할 스켈레톤 UI (도전 7)
// 이미 완성되어 있으니 그대로 사용하세요

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className = "" }: SkeletonProps) {
  return (
    <div className={`animate-pulse bg-slate-200 rounded ${className}`} />
  );
}

export function CardSkeleton() {
  return (
    <div className="p-4 rounded-xl border border-slate-200 space-y-3">
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-3 w-1/2" />
      <Skeleton className="h-3 w-2/3" />
    </div>
  );
}
