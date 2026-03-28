#!/usr/bin/env bash
# validate-slides.sh — slide-master 규칙 검증 스크립트
# Usage: ./scripts/validate-slides.sh lectures/{topic}/slides/slides.md

set -euo pipefail

FILE="${1:?Usage: validate-slides.sh <slides.md>}"
[ -f "$FILE" ] || { echo "ERROR: $FILE not found"; exit 1; }

PASS=0
FAIL=0
WARN=0

pass() { ((PASS++)); echo "  ✅ $1"; }
fail() { ((FAIL++)); echo "  ❌ $1"; }
warn() { ((WARN++)); echo "  ⚠️  $1"; }

echo "=== slide-master 규칙 검증: $FILE ==="
echo ""

# --- 기본 통계 ---
TOTAL_SLIDES=$(grep -c '^---$' "$FILE" || true)
echo "📊 총 슬라이드: ~$((TOTAL_SLIDES / 2))장"
echo ""

# --- Rule 16: HTML 태그 안에서 **bold** 사용 금지 ---
echo "[Rule 16] HTML 내 **bold** 검사"
# HTML 태그 안에서 **...** 패턴 찾기
BOLD_IN_HTML=$(grep -n '\*\*[^*]*\*\*' "$FILE" | grep -E '<(div|span|v-click|v-clicks|p|li|ul|ol|td|th|a|h[1-6]|strong|em|label|button)' | head -5 || true)
if [ -z "$BOLD_IN_HTML" ]; then
  pass "HTML 태그 내 **bold** 미사용"
else
  fail "HTML 태그 내 **bold** 발견:"
  echo "$BOLD_IN_HTML" | while read -r line; do echo "    $line"; done
fi

# --- Rule: two-cols-header 금지 ---
echo "[Layout] two-cols-header 사용 검사"
TWO_COLS=$(grep -cn 'layout:.*two-cols-header' "$FILE" || true)
if [ "$TWO_COLS" -eq 0 ]; then
  pass "two-cols-header 미사용"
else
  fail "two-cols-header ${TWO_COLS}회 사용 (grid grid-cols-2 사용 권장)"
fi

# --- Rule 12: 텍스트 전용 3장 연속 검사 ---
echo "[Rule 12] 텍스트 전용 슬라이드 연속 검사"
# 슬라이드별로 시각 요소 여부 확인 (Mermaid, img, HTML/CSS 다이어그램, 플레이스홀더)
RULE12_RESULT=$(awk '
BEGIN { slide=0; text_run=0; max_run=0; visual=0 }
/^---$/ {
  if (slide > 0 && !visual) { text_run++ }
  else { if (text_run > max_run) max_run = text_run; text_run = 0 }
  slide++; visual=0; next
}
/```mermaid/ { visual=1 }
/<img / { visual=1 }
/\.(png|svg|jpg|webp)/ { visual=1 }
/IMAGE:/ || /border-dashed/ { visual=1 }
/\$clicks/ { visual=1 }
/flex.*items-center.*justify-center/ || /grid.*grid-cols/ { visual=1 }
/ring-2.*ring-.*scale/ { visual=1 }
/bg-.*rounded-xl.*shadow/ { visual=1 }
END {
  if (!visual) text_run++
  if (text_run > max_run) max_run = text_run
  if (max_run >= 3) print "FAIL:" max_run
  else print "PASS:" max_run
}
' "$FILE")
RULE12_STATUS="${RULE12_RESULT%%:*}"
RULE12_VAL="${RULE12_RESULT##*:}"
if [ "$RULE12_STATUS" = "FAIL" ]; then
  fail "텍스트 전용 슬라이드 최대 ${RULE12_VAL}장 연속 (3장 이하 권장)"
else
  pass "텍스트 연속 최대 ${RULE12_VAL}장"
fi

# --- $clicks without clicks: frontmatter ---
echo "[\$clicks] clicks: N 프론트매터 검사"
# $clicks를 사용하는 슬라이드 블록에서 clicks: 가 있는지 확인
CLICKS_ISSUES=$(awk '
BEGIN { in_fm=0; has_clicks_fm=0; uses_clicks_var=0; slide_num=0; issues="" }
/^---$/ {
  if (in_fm) {
    in_fm=0
    if (uses_clicks_var && !has_clicks_fm) {
      issues = issues " " slide_num
    }
    has_clicks_fm=0; uses_clicks_var=0
  } else {
    in_fm=1; slide_num++; has_clicks_fm=0; uses_clicks_var=0
  }
  next
}
in_fm && /^clicks:/ { has_clicks_fm=1 }
!in_fm && /\$clicks/ { uses_clicks_var=1 }
END { print issues }
' "$FILE")
if [ -z "$(echo "$CLICKS_ISSUES" | tr -d ' ')" ]; then
  pass "\$clicks 사용 슬라이드에 clicks: 프론트매터 정상"
else
  fail "\$clicks 사용하지만 clicks: 미선언 슬라이드:$CLICKS_ISSUES"
fi

# --- max-h on images ---
echo "[Style] 이미지 max-h 검사"
IMGS_NO_MAXH=$(grep -n '<img ' "$FILE" | grep -v 'max-h' | grep -v 'mermaid' | head -5 || true)
if [ -z "$IMGS_NO_MAXH" ]; then
  pass "모든 img 태그에 max-h 클래스 있음"
else
  COUNT=$(grep '<img ' "$FILE" | grep -v 'max-h' | grep -v 'mermaid' | wc -l | tr -d ' ')
  fail "max-h 없는 img 태그 ${COUNT}개:"
  echo "$IMGS_NO_MAXH" | while read -r line; do echo "    $line"; done
fi

# --- 색상 남용 검사 (text-{color}-{shade} 3종 이상) ---
echo "[Rule 9] 색상 남용 검사 (슬라이드당 3색 이상)"
awk '
BEGIN { slide=0 }
/^---$/ {
  if (slide > 0) {
    n=0; for (c in colors) n++
    if (n >= 3) {
      printf "  슬라이드 %d: %d색 -", slide, n
      for (c in colors) printf " %s", c
      printf "\n"
    }
  }
  slide++; delete colors; next
}
{
  n = split($0, a, "text-")
  for (i=2; i<=n; i++) {
    if (a[i] ~ /^(red|green|blue|yellow|purple|pink|orange|cyan|teal|amber|lime|emerald|violet|fuchsia|rose|indigo|sky)-[0-9]/) {
      split(a[i], parts, /[^a-z0-9-]/)
      colors[parts[1]] = 1
    }
  }
}
END {
  n=0; for (c in colors) n++
  if (n >= 3) {
    printf "  슬라이드 %d: %d색 -", slide, n
    for (c in colors) printf " %s", c
    printf "\n"
  }
}
' "$FILE" > /tmp/color_check.txt
COLOR_ISSUES=$(wc -l < /tmp/color_check.txt | tr -d ' ')
if [ "$COLOR_ISSUES" -eq 0 ]; then
  pass "색상 남용 없음"
else
  warn "${COLOR_ISSUES}개 슬라이드에서 3색 이상 사용:"
  head -3 /tmp/color_check.txt
fi

# --- Mermaid 설정 확인 ---
echo "[Mermaid] setup/mermaid.ts 존재 검사"
SLIDES_DIR=$(dirname "$FILE")
if [ -f "$SLIDES_DIR/setup/mermaid.ts" ]; then
  pass "setup/mermaid.ts 존재"
else
  HAS_MERMAID=$(grep -c '```mermaid' "$FILE" || true)
  if [ "$HAS_MERMAID" -gt 0 ]; then
    fail "Mermaid ${HAS_MERMAID}개 사용하지만 setup/mermaid.ts 없음"
  else
    pass "Mermaid 미사용 — setup 불필요"
  fi
fi

# --- 폰트 설정 확인 ---
echo "[Font] Freesentation 폰트 검사"
if [ -f "$SLIDES_DIR/style.css" ] && grep -q 'Freesentation' "$SLIDES_DIR/style.css"; then
  pass "style.css에 Freesentation 폰트 설정 있음"
else
  warn "style.css에 Freesentation 폰트 설정 없음"
fi

# --- 시각 요소 통계 ---
echo ""
echo "📊 시각 요소 통계:"
MERMAID_COUNT=$(grep -c '```mermaid' "$FILE" || true)
HTML_DIAGRAM=$(grep -c 'flex.*items-center.*justify-center\|grid.*grid-cols' "$FILE" || true)
IMG_COUNT=$(grep -c '<img ' "$FILE" || true)
VCLICK_COUNT=$(grep -c 'v-click\|v-clicks' "$FILE" || true)
VMOTION_COUNT=$(grep -c 'v-motion' "$FILE" || true)
echo "  Mermaid: ${MERMAID_COUNT}개"
echo "  HTML/CSS 다이어그램(추정): ${HTML_DIAGRAM}개"
echo "  이미지: ${IMG_COUNT}개"
echo "  v-click/v-clicks: ${VCLICK_COUNT}개"
echo "  v-motion: ${VMOTION_COUNT}개"

# --- 결과 요약 ---
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "결과: ✅ ${PASS} PASS / ❌ ${FAIL} FAIL / ⚠️  ${WARN} WARN"
if [ "$FAIL" -gt 0 ]; then
  echo "🔴 ${FAIL}개 규칙 위반 발견"
  exit 1
else
  echo "🟢 모든 필수 규칙 통과"
  exit 0
fi
