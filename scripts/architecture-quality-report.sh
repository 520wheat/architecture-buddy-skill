#!/usr/bin/env bash
# Phase 1B maintainer worksheet. Heuristics flag debt; humans score semantics.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: bash scripts/architecture-quality-report.sh <candidate.md> [out.md]

Generate a Phase 1B architecture-quality worksheet. The tool performs
hard-gate and omission heuristics, but does not assign semantic quality scores.
EOF
}

fail() { echo "FAIL: $*" >&2; exit 1; }

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

[[ $# -ge 1 && $# -le 2 ]] || { usage >&2; exit 1; }
CANDIDATE="$1"
[[ -f "$CANDIDATE" ]] || [[ -f "$ROOT/$CANDIDATE" ]] || fail "candidate not found: $1"
if [[ ! -f "$CANDIDATE" ]]; then
  CANDIDATE="$ROOT/$CANDIDATE"
fi
OUT="${2:-}"

has_all_sections=true
missing_sections=()
has_section() {
  local section="$1"
  awk -v section="$section" '
    $0 ~ ("^#{2,6}[[:space:]]+" section "([[:space:]]|$)") {
      found=1
      exit
    }
    END { exit(found ? 0 : 1) }
  ' "$CANDIDATE"
}

for i in 1 2 3 4 5 6 7 8; do
  if ! has_section "A${i}"; then
    has_all_sections=false
    missing_sections+=("A${i}")
  fi
done
for i in 1 2 3 4 5 6; do
  if ! has_section "B${i}"; then
    has_all_sections=false
    missing_sections+=("B${i}")
  fi
done

section_body() {
  local section="$1"
  awk -v section="$section" '
    function is_named_section(line) {
      return line ~ /^#{2,6}[[:space:]]+[AB][0-9]+([[:space:]]|$)/
    }
    $0 ~ ("^#{2,6}[[:space:]]+" section "([[:space:]]|$)") {
      match($0, /^#+/)
      target_level=RLENGTH
      inside=1
      next
    }
    inside && /^#{2,6}[[:space:]]+/ {
      match($0, /^#+/)
      level=RLENGTH
      if (level <= target_level || is_named_section($0)) exit
    }
    inside { print }
  ' "$CANDIDATE"
}

flags=()
roundtable_signals=()

if ! $has_all_sections; then
  flags+=("structure-incomplete")
fi

if ! has_section A1 &&
   grep -qE '组件清单|模块清单|服务清单|API|数据库|技术栈' "$CANDIDATE"; then
  flags+=("module-list-only")
fi

if grep -qE '服务|模块|API|数据库|消息组件|技术栈' "$CANDIDATE" &&
   ! grep -qE '问题类|业务目标|业务场景|业务流程|核心问题|状态不变量|资源边界' "$CANDIDATE"; then
  flags+=("architecture-boundary-debt")
fi

if $has_all_sections &&
   ! grep -qE '目标层|设计对象/目标层|架构推导链' "$CANDIDATE" &&
   ! grep -qE '问题.{0,80}(业务|场景|流程|核心问题).{0,120}(能力|边界|应用|集成|技术|质量属性)' "$CANDIDATE"; then
  flags+=("architecture-derivation-missing")
fi

if ! has_section A1 &&
   grep -qE '主持人：|架构师[^：]*：|用户：' "$CANDIDATE"; then
  flags+=("meeting-record-only")
fi

b6_body="$(section_body B6)"
b6_missing=()
for marker in '变化轴' 'N+1' '反例' '可组合能力' '复杂度'; do
  [[ "$b6_body" == *"$marker"* ]] || b6_missing+=("$marker")
done
if [[ ${#b6_missing[@]} -gt 0 ]]; then
  flags+=("b6-evidence-insufficient")
fi

if grep -qE '圆桌|Roundtable|## Lens:' "$CANDIDATE" &&
   ! grep -qE '综合结论|主持人综合|synthesis' "$CANDIDATE"; then
  roundtable_signals+=("synthesis-missing")
fi

b1_body="$(section_body B1)"
b4_body="$(section_body B4)"
if grep -qE '选择|采用|选用|结论' <<<"$b4_body" &&
   ! grep -qE '证据|事实|依据|代价|成本|风险|质量属性|验收|待验证|已证实' <<<"$b1_body$b4_body"; then
  flags+=("evidence-and-cost-debt")
fi

hard_gate="PASS"
if [[ ${#flags[@]} -gt 0 ]]; then
  hard_gate="REJECT"
fi

structure_score="0/20"
if $has_all_sections && [[ ${#b6_missing[@]} -eq 0 ]]; then
  structure_score="20/20"
fi

rel_candidate="$CANDIDATE"
case "$CANDIDATE" in
  "$ROOT"/*) rel_candidate="${CANDIDATE#"$ROOT"/}" ;;
esac

emit() {
  cat <<EOF
# Architecture Quality Report

| Field | Value |
|------|------|
| candidate | \`${rel_candidate}\` |
| hard_gate | **${hard_gate}** |
| structure_score | ${structure_score} |
| semantic_quality_score | _MANUAL / 100_ |
| domain_score | _MANUAL / 100_ |
| roundtable_score | _MANUAL / 20 or not-needed_ |
| human_review | _PENDING_ |

## Automated Signals

EOF
  if [[ ${#flags[@]} -eq 0 ]]; then
    echo '- flag: none'
  else
    for flag in "${flags[@]}"; do
      echo "- flag: ${flag}"
    done
  fi
  if [[ ${#missing_sections[@]} -gt 0 ]]; then
    echo "- missing_sections: ${missing_sections[*]}"
  fi
  if [[ ${#b6_missing[@]} -gt 0 ]]; then
    echo "- b6_missing_evidence: ${b6_missing[*]}"
  fi
  if [[ ${#roundtable_signals[@]} -eq 0 ]]; then
    echo '- roundtable_signal: none-detected'
  else
    for signal in "${roundtable_signals[@]}"; do
      echo "- roundtable_signal: ${signal}"
    done
  fi

  cat <<'EOF'

## Manual Semantic Score

自动信号只用于发现遗漏或结构性伪装；维护者必须阅读正文后填写 0–4，不能按关键词计分。

| Dimension | Score (0–4) | Evidence / counterexample |
|-----------|-------------|---------------------------|
| 问题类与边界 | _ / 4 | |
| 机制与策略分离 | _ / 4 | |
| 失败、安全与恢复 | _ / 4 | |
| 演进、N+1 与反例 | _ / 4 | |
| 证据、决策理由与质量属性 | _ / 4 | |

## Manual Roundtable Review

- 高影响互斥分叉是否被识别并主动提议：_（PASS / FAIL / NOT NEEDED）_
- 用户同意或跳过是否记录：_（PASS / FAIL / N/A）_
- 席位与透镜契约是否匹配：_（PASS / FAIL / N/A）_
- 主持人综合结论是否保留冲突、边界、代价：_（PASS / FAIL / N/A）_

## Reviewer Conclusion

- 语义总分：_ / 100
- 领域分：_ / 100
- 圆桌分：_ / 20
- 结论：_PENDING_
- 反关键词命中复核：_（通过 / 不通过）_
- 备注：
EOF
}

if [[ -n "$OUT" ]]; then
  emit >"$OUT"
  echo "Wrote $OUT" >&2
else
  emit
fi
