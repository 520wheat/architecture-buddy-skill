#!/usr/bin/env bash
# Maintainer tool: structure gate + RUBRIC checklist skeleton (no auto PASS).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: bash scripts/rubric-report.sh <golden_id> <candidate.md> [out.md]

Generate a maintainer RUBRIC checklist report from corpus/golden/<id>/RUBRIC.md
against a candidate deliverable. Structure A1–A8 / B1–B5 must be present.

Does NOT auto-judge PASS — maintainer checks boxes, then writes corpus/runs.

Options:
  -h, --help    Show this help and exit 0
EOF
}

fail() { echo "FAIL: $*" >&2; exit 1; }

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

[[ $# -ge 2 && $# -le 3 ]] || { usage >&2; exit 1; }

GOLDEN_ID="$1"
CANDIDATE="$2"
OUT="${3:-}"

# Resolve candidate path (allow relative to CWD or ROOT)
if [[ ! -f "$CANDIDATE" && -f "$ROOT/$CANDIDATE" ]]; then
  CANDIDATE="$ROOT/$CANDIDATE"
fi
[[ -f "$CANDIDATE" ]] || fail "candidate not found: $2"

GOLDEN_DIR="$ROOT/corpus/golden/$GOLDEN_ID"
GOLDEN_MD="$GOLDEN_DIR/GOLDEN.md"
RUBRIC_MD="$GOLDEN_DIR/RUBRIC.md"

[[ -d "$GOLDEN_DIR" ]] || fail "missing golden dir: corpus/golden/$GOLDEN_ID"
[[ -f "$GOLDEN_MD" ]] || fail "missing $GOLDEN_MD"
[[ -f "$RUBRIC_MD" ]] || fail "missing $RUBRIC_MD"

# Structure gate: ### A1…### A8, ### B1…### B5
missing=()
for i in 1 2 3 4 5 6 7 8; do
  grep -qE "^### A${i}([[:space:]]|$)" "$CANDIDATE" || missing+=("### A${i}")
done
for i in 1 2 3 4 5; do
  grep -qE "^### B${i}([[:space:]]|$)" "$CANDIDATE" || missing+=("### B${i}")
done
if [[ ${#missing[@]} -gt 0 ]]; then
  fail "candidate missing sections: ${missing[*]}"
fi

# Extract "- " list items under ## headings matching needle until next ##
extract_section_items() {
  local file="$1"
  local needle="$2"
  awk -v needle="$needle" '
    /^## / {
      in_sec = (index($0, needle) > 0)
      next
    }
    in_sec && /^- / {
      sub(/^-[[:space:]]+/, "")
      print
    }
  ' "$file"
}

must_hit=()
while IFS= read -r line; do
  [[ -n "$line" ]] && must_hit+=("$line")
done < <(extract_section_items "$RUBRIC_MD" "必中")

blacklist=()
while IFS= read -r line; do
  [[ -n "$line" ]] && blacklist+=("$line")
done < <(extract_section_items "$RUBRIC_MD" "幻觉黑名单")

[[ ${#must_hit[@]} -gt 0 ]] || fail "RUBRIC has no 必中 list items: $RUBRIC_MD"
[[ ${#blacklist[@]} -gt 0 ]] || fail "RUBRIC has no 幻觉黑名单 list items: $RUBRIC_MD"

rel_candidate="$CANDIDATE"
case "$CANDIDATE" in
  "$ROOT"/*) rel_candidate="${CANDIDATE#"$ROOT"/}" ;;
esac

emit() {
  cat <<EOF
# RUBRIC 对照报告 — ${GOLDEN_ID}

**本报告不自动判定 PASS；维护者勾选后写入 corpus/runs**

| 字段 | 值 |
|------|-----|
| golden_id | \`${GOLDEN_ID}\` |
| golden | \`corpus/golden/${GOLDEN_ID}/\` |
| candidate | \`${rel_candidate}\` |
| structure | OK（A1–A8、B1–B5） |

## 必中

EOF
  for item in "${must_hit[@]}"; do
    printf -- '- [ ] %s\n' "$item"
  done

  cat <<'EOF'

## 幻觉黑名单

EOF
  for item in "${blacklist[@]}"; do
    printf -- '- [ ] 未出现：%s\n' "$item"
  done

  cat <<'EOF'

## 维护者结论（人工）

- 判定：_（PASS / RETRY）_
- 备注：

EOF
}

if [[ -n "$OUT" ]]; then
  emit >"$OUT"
  echo "Wrote $OUT" >&2
else
  emit
fi
