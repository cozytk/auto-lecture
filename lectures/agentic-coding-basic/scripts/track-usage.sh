#!/usr/bin/env bash
# track-usage.sh — Opencode 무료 모델 사용량 추적 스크립트
#
# 사용법:
#   ./scripts/track-usage.sh snapshot          # 테스트 전 스냅샷 저장
#   ./scripts/track-usage.sh status            # 현재 전체 사용량 요약
#   ./scripts/track-usage.sh diff              # 스냅샷 이후 사용량 변화
#   ./scripts/track-usage.sh errors [N]        # 최근 N개 에러 (기본 20)
#   ./scripts/track-usage.sh sessions [model]  # 세션별 사용량 (모델 필터 가능)
#   ./scripts/track-usage.sh timeline [hours]  # 시간대별 요청 분포 (기본 5시간)

set -euo pipefail

DB="${OPENCODE_DB:-$HOME/.local/share/opencode/opencode.db}"
SNAPSHOT_DIR="$(dirname "$0")/../.usage-snapshots"

if [[ ! -f "$DB" ]]; then
  echo "❌ Opencode DB를 찾을 수 없습니다: $DB"
  echo "   OPENCODE_DB 환경변수로 경로를 지정하거나 opencode를 먼저 실행하세요."
  exit 1
fi

mkdir -p "$SNAPSHOT_DIR"

# 무료 모델 필터 (opencode 프로바이더 = 무료)
FREE_PROVIDER="opencode"

# ── 함수 ──

cmd_status() {
  echo "═══════════════════════════════════════════════════════════════"
  echo "  Opencode 무료 모델 사용량 현황"
  echo "═══════════════════════════════════════════════════════════════"
  echo ""

  sqlite3 -header -column "$DB" "
    SELECT
      json_extract(data, '$.modelID') AS model,
      COUNT(*) AS requests,
      SUM(json_extract(data, '$.tokens.input')) AS input_tok,
      SUM(json_extract(data, '$.tokens.output')) AS output_tok,
      SUM(json_extract(data, '$.tokens.cache.read')) AS cache_read,
      SUM(json_extract(data, '$.tokens.cache.write')) AS cache_write,
      printf('%.4f', SUM(json_extract(data, '$.cost'))) AS cost_usd,
      datetime(MIN(time_created) / 1000, 'unixepoch', 'localtime') AS first_use,
      datetime(MAX(time_created) / 1000, 'unixepoch', 'localtime') AS last_use
    FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.providerID') = '${FREE_PROVIDER}'
    GROUP BY model
    ORDER BY requests DESC;
  "

  echo ""
  echo "── 전체 합계 ──"
  sqlite3 -header -column "$DB" "
    SELECT
      COUNT(*) AS total_requests,
      SUM(json_extract(data, '$.tokens.input')) AS total_input,
      SUM(json_extract(data, '$.tokens.output')) AS total_output,
      SUM(json_extract(data, '$.tokens.cache.read')) AS total_cache_read,
      COUNT(DISTINCT session_id) AS sessions
    FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.providerID') = '${FREE_PROVIDER}';
  "
}

cmd_snapshot() {
  local snap_file="$SNAPSHOT_DIR/$(date +%Y%m%d_%H%M%S).json"

  sqlite3 -json "$DB" "
    SELECT
      json_extract(data, '$.modelID') AS model,
      COUNT(*) AS requests,
      SUM(json_extract(data, '$.tokens.input')) AS input_tok,
      SUM(json_extract(data, '$.tokens.output')) AS output_tok,
      SUM(json_extract(data, '$.tokens.cache.read')) AS cache_read,
      SUM(json_extract(data, '$.tokens.cache.write')) AS cache_write,
      MAX(time_created) AS last_time
    FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.providerID') = '${FREE_PROVIDER}'
    GROUP BY model;
  " > "$snap_file"

  # 에러 수도 스냅샷에 포함
  local error_count
  error_count=$(sqlite3 "$DB" "
    SELECT COUNT(*) FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.error') IS NOT NULL
      AND json_extract(data, '$.providerID') = '${FREE_PROVIDER}';
  " 2>/dev/null || echo "0")

  echo "✅ 스냅샷 저장: $snap_file"
  echo "   현재 무료 모델 에러 수: $error_count"
  echo ""
  echo "   테스트 후 './scripts/track-usage.sh diff' 로 변화를 확인하세요."
}

cmd_diff() {
  local latest_snap
  latest_snap=$(ls -t "$SNAPSHOT_DIR"/*.json 2>/dev/null | head -1)

  if [[ -z "$latest_snap" ]]; then
    echo "❌ 스냅샷이 없습니다. 먼저 './scripts/track-usage.sh snapshot'을 실행하세요."
    exit 1
  fi

  echo "═══════════════════════════════════════════════════════════════"
  echo "  스냅샷 이후 사용량 변화"
  echo "  기준: $(basename "$latest_snap" .json | sed 's/_/ /g')"
  echo "═══════════════════════════════════════════════════════════════"
  echo ""

  # 현재 데이터
  local current
  current=$(sqlite3 -json "$DB" "
    SELECT
      json_extract(data, '$.modelID') AS model,
      COUNT(*) AS requests,
      SUM(json_extract(data, '$.tokens.input')) AS input_tok,
      SUM(json_extract(data, '$.tokens.output')) AS output_tok,
      SUM(json_extract(data, '$.tokens.cache.read')) AS cache_read,
      SUM(json_extract(data, '$.tokens.cache.write')) AS cache_write
    FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.providerID') = '${FREE_PROVIDER}'
    GROUP BY model;
  ")

  # Python으로 diff 계산 (jq 대신 Python 사용 — macOS 기본 포함)
  python3 -c "
import json, sys

with open('$latest_snap') as f:
    snap = {r['model']: r for r in json.load(f)}

current = {r['model']: r for r in json.loads('''$current''')}

fields = ['requests', 'input_tok', 'output_tok', 'cache_read', 'cache_write']
all_models = sorted(set(list(snap.keys()) + list(current.keys())))

print(f'{'모델':<30} {'요청수':>8} {'입력토큰':>12} {'출력토큰':>12} {'캐시읽기':>12}')
print('─' * 76)

for model in all_models:
    s = snap.get(model, {})
    c = current.get(model, {})
    deltas = []
    for f in fields:
        sv = s.get(f, 0) or 0
        cv = c.get(f, 0) or 0
        deltas.append(cv - sv)

    if any(d != 0 for d in deltas):
        print(f'{model:<30} {deltas[0]:>+8,} {deltas[1]:>+12,} {deltas[2]:>+12,} {deltas[3]:>+12,}')

if not any(
    any((current.get(m, {}).get(f, 0) or 0) - (snap.get(m, {}).get(f, 0) or 0) != 0
        for f in fields)
    for m in all_models
):
    print('  (변화 없음)')
"
}

cmd_errors() {
  local limit="${1:-20}"

  echo "═══════════════════════════════════════════════════════════════"
  echo "  최근 API 에러 (최대 ${limit}건)"
  echo "═══════════════════════════════════════════════════════════════"
  echo ""

  sqlite3 -header -column "$DB" "
    SELECT
      datetime(time_created / 1000, 'unixepoch', 'localtime') AS time,
      json_extract(data, '$.modelID') AS model,
      json_extract(data, '$.providerID') AS provider,
      json_extract(data, '$.error.name') AS error_type,
      json_extract(data, '$.error.data.statusCode') AS status,
      substr(json_extract(data, '$.error.data.message'), 1, 50) AS message,
      session_id
    FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.error') IS NOT NULL
    ORDER BY time_created DESC
    LIMIT ${limit};
  "

  echo ""
  echo "── 에러 유형별 집계 ──"
  sqlite3 -header -column "$DB" "
    SELECT
      json_extract(data, '$.error.name') AS error_type,
      json_extract(data, '$.error.data.statusCode') AS status,
      json_extract(data, '$.modelID') AS model,
      COUNT(*) AS count
    FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.error') IS NOT NULL
    GROUP BY error_type, status, model
    ORDER BY count DESC;
  "
}

cmd_sessions() {
  local model_filter="${1:-}"

  echo "═══════════════════════════════════════════════════════════════"
  echo "  세션별 무료 모델 사용량"
  if [[ -n "$model_filter" ]]; then
    echo "  필터: $model_filter"
  fi
  echo "═══════════════════════════════════════════════════════════════"
  echo ""

  local where_clause="json_extract(m.data, '$.role') = 'assistant' AND json_extract(m.data, '$.providerID') = '${FREE_PROVIDER}'"
  if [[ -n "$model_filter" ]]; then
    where_clause="$where_clause AND json_extract(m.data, '$.modelID') LIKE '%${model_filter}%'"
  fi

  sqlite3 -header -column "$DB" "
    SELECT
      m.session_id,
      s.title AS session_title,
      json_extract(m.data, '$.modelID') AS model,
      COUNT(*) AS requests,
      SUM(json_extract(m.data, '$.tokens.input')) AS input_tok,
      SUM(json_extract(m.data, '$.tokens.output')) AS output_tok,
      SUM(json_extract(m.data, '$.tokens.cache.read')) AS cache_read,
      datetime(MIN(m.time_created) / 1000, 'unixepoch', 'localtime') AS started,
      datetime(MAX(m.time_created) / 1000, 'unixepoch', 'localtime') AS ended,
      CAST((MAX(m.time_created) - MIN(m.time_created)) / 60000 AS INTEGER) AS duration_min
    FROM message m
    JOIN session s ON m.session_id = s.id
    WHERE ${where_clause}
    GROUP BY m.session_id, model
    ORDER BY started DESC
    LIMIT 30;
  "
}

cmd_timeline() {
  local hours="${1:-5}"

  echo "═══════════════════════════════════════════════════════════════"
  echo "  최근 ${hours}시간 요청 분포 (무료 모델)"
  echo "═══════════════════════════════════════════════════════════════"
  echo ""

  local since
  since=$(python3 -c "import time; print(int(time.time() * 1000) - ${hours} * 3600000)")

  sqlite3 -header -column "$DB" "
    SELECT
      strftime('%Y-%m-%d %H:00', datetime(time_created / 1000, 'unixepoch', 'localtime')) AS hour,
      json_extract(data, '$.modelID') AS model,
      COUNT(*) AS requests,
      SUM(json_extract(data, '$.tokens.input')) AS input_tok,
      SUM(json_extract(data, '$.tokens.output')) AS output_tok
    FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.providerID') = '${FREE_PROVIDER}'
      AND time_created >= ${since}
    GROUP BY hour, model
    ORDER BY hour ASC;
  "

  echo ""
  echo "── 시간대별 에러 ──"
  sqlite3 -header -column "$DB" "
    SELECT
      strftime('%Y-%m-%d %H:00', datetime(time_created / 1000, 'unixepoch', 'localtime')) AS hour,
      json_extract(data, '$.error.name') AS error_type,
      json_extract(data, '$.error.data.statusCode') AS status,
      COUNT(*) AS count
    FROM message
    WHERE json_extract(data, '$.role') = 'assistant'
      AND json_extract(data, '$.error') IS NOT NULL
      AND time_created >= ${since}
    GROUP BY hour, error_type, status
    ORDER BY hour ASC;
  "
}

cmd_help() {
  echo "Opencode 무료 모델 사용량 추적"
  echo ""
  echo "사용법: $0 <command> [args]"
  echo ""
  echo "Commands:"
  echo "  status              현재 전체 사용량 요약"
  echo "  snapshot            테스트 전 스냅샷 저장"
  echo "  diff                스냅샷 이후 사용량 변화"
  echo "  errors [N]          최근 N개 에러 (기본 20)"
  echo "  sessions [model]    세션별 사용량 (모델 필터 가능)"
  echo "  timeline [hours]    시간대별 요청 분포 (기본 5시간)"
  echo ""
  echo "테스트 워크플로우:"
  echo "  1. ./scripts/track-usage.sh snapshot    # 테스트 전"
  echo "  2. opencode 에서 무료 모델로 작업 수행"
  echo "  3. ./scripts/track-usage.sh diff         # 사용량 확인"
  echo "  4. ./scripts/track-usage.sh errors       # 에러 확인"
}

# ── 메인 ──
case "${1:-help}" in
  status)    cmd_status ;;
  snapshot)  cmd_snapshot ;;
  diff)      cmd_diff ;;
  errors)    cmd_errors "${2:-20}" ;;
  sessions)  cmd_sessions "${2:-}" ;;
  timeline)  cmd_timeline "${2:-5}" ;;
  help|*)    cmd_help ;;
esac
