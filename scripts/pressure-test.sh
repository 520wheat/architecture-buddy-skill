#!/usr/bin/env bash
# Executable pressure tests for Architecture Buddy (no LLM required).
# Locks: trigger-description format, behavioral rules in SKILL text,
# deliverable structure gate, agent-runtime rubric themes.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/skill/architecture-buddy"
FIX="$ROOT/scripts/fixtures/pressure"
fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "OK: $*"; }

mkdir -p "$FIX"

# --- Fixtures (regenerated each run; kept under scripts/fixtures) ---
cat >"$FIX/incomplete-deliverable.md" <<'EOF'
# 架构设计：残缺样例

> 模式：deliverable

## 层 A — 叙事
### A1 摘要
只有摘要。
### A2 上下文与边界
有边界。
## 层 B — 机制与策略
### B1 基本事实
一条事实。
EOF

cat >"$FIX/complete-minimal-deliverable.md" <<'EOF'
# 架构设计：最小完整样例

> 模式：deliverable
> 已定关键决策：统一执行入口
> 明确不做：替用户拍板
> 待验证事实：无

## 层 A — 叙事
### A1 摘要
解决一类受控工具执行问题；不解决无监督全自动变更。
### A2 上下文与边界
控制面与执行面分离；信任边界在 Executor。
### A3 主路径
请求 → 编排 → 审批 → 执行 → 审计。
### A4 组件与契约
编排不得直接调用 Client。
### A5 状态、失败与恢复
审批拒绝则不执行；重启后内存会话丢失（待验证生产持久化）。
### A6 安全与身份
默认拒绝未授权主体。
### A7 演进切片
现在：单机；下一刀：持久化审批；不做：多租无计费。
### A8 如何验收
1. 未批不得执行可观察。
2. 审计有操作者字段。
3. 陌生人能讲清主路径。

## 层 B — 机制与策略
### B1 基本事实
工具副作用不可自动回滚。
### B2 机制
统一执行闸门；会话与审计分离。
### B3 策略选项
内存 vs 持久化审批。
### B4 取舍
先内存演示，换取简单。
### B5 与对照的关系
未对照。

### B6 组合增长与边界检验
消息 × 渠道 × 通用规则 → 可追踪投递。变化轴=渠道。N+1 只加渠道适配。反例=双向实时会话。能力增长而非缠绕。

## 完成门禁自检
- [x] 结构齐全
EOF

cat >"$FIX/premature-done.md" <<'EOF'
# 假完成样例
架构设计已完成。

只有一句话，没有双层，也没有完成门禁自检。
EOF

# --- 1) description: Use when... only (host + lenses) ---
extract_desc() {
  # Prints description body (handles > folded or single-line)
  local f="$1"
  awk '
    BEGIN { indesc=0 }
    /^description:[[:space:]]*>[[:space:]]*$/ { indesc=1; next }
    /^description:[[:space:]]+/ {
      line=$0; sub(/^description:[[:space:]]+/, "", line);
      print line; exit
    }
    indesc && /^[a-zA-Z0-9_-]+:/ { exit }
    indesc && /^---$/ { exit }
    indesc { print }
  ' "$f"
}

check_use_when() {
  local f="$1"
  local body
  body="$(extract_desc "$f" | sed '/^[[:space:]]*$/d' | head -n 1 | sed 's/^[[:space:]]*//')"
  [[ "$body" == Use\ when* ]] || fail "$f description must start with 'Use when' (got: ${body:0:80})"
  # Host must not smuggle draft/deliverable procedure into description
  if [[ "$(basename "$(dirname "$f")")" == "architecture-buddy" ]]; then
    if echo "$body" | grep -qiE 'draft mode|S0|completion gate|第一性原理三步'; then
      fail "host description must not embed workflow procedure"
    fi
  fi
}

check_use_when "$SKILL/SKILL.md"
for LENS in "$ROOT"/skill/architecture-buddy-lens-*/SKILL.md; do
  check_use_when "$LENS"
done
pass "all descriptions start with Use when"

# --- 2) Behavioral rules must exist in host SKILL (baseline pressure on text) ---
grep -qE '一次只推进一件事|每次只推进一件事' "$SKILL/SKILL.md" || fail "missing rule: 一次/每次只推进一件事"
grep -qE '未过完成门禁不得宣称完成|未过 S6 完成门禁，禁止宣称|未过完成检查不得宣称' "$SKILL/SKILL.md" || \
  fail "missing rule: must not claim done before completion gate"
grep -qE '不对用户做考试|禁止.*A/B/C/D|不打分' "$SKILL/SKILL.md" || fail "missing anti-exam UX rules"
grep -q '不替用户拍板' "$SKILL/SKILL.md" || fail "missing: 不替用户拍板"
grep -qE '加法陷阱|乘法式构架|禁止默许加法' "$SKILL/SKILL.md" || fail "missing multiplicative / anti-additive rules"
grep -q 'N+1' "$SKILL/references/deliverable-gate.md" || fail "gate missing N+1"
grep -q '反例' "$SKILL/references/deliverable-gate.md" || fail "gate missing 反例"
grep -q 'B6' "$SKILL/templates/architecture-deliverable.md" || fail "template missing B6"
pass "host SKILL encodes required behavioral rules"

# --- 2b) Roundtable preflight must be explicit and testable ---
grep -q '高影响互斥分叉' "$SKILL/SKILL.md" || fail "missing: high-impact mutually exclusive fork preflight"
grep -q '必须先提议圆桌' "$SKILL/SKILL.md" || fail "missing: mandatory roundtable proposal"
grep -q '用户选择跳过圆桌' "$SKILL/SKILL.md" || fail "missing: explicit user-decline record"
pass "host SKILL requires roundtable preflight and consent record"

# --- 3) Structure gate: incomplete fails, complete passes ---
if bash "$ROOT/scripts/rubric-report.sh" kafka "$FIX/incomplete-deliverable.md" "$FIX/out-incomplete.md" 2>"$FIX/err-incomplete.txt"; then
  fail "incomplete deliverable should fail rubric-report structure check"
fi
grep -qiE 'missing|FAIL|A[0-9]|B[0-9]' "$FIX/err-incomplete.txt" "$FIX/out-incomplete.md" 2>/dev/null || true
pass "incomplete deliverable rejected by structure check"

bash "$ROOT/scripts/rubric-report.sh" kafka "$FIX/complete-minimal-deliverable.md" "$FIX/out-complete.md" \
  || fail "minimal complete deliverable should pass structure check"
pass "minimal complete deliverable accepted by structure check"

# Premature "已完成" without dual-layer / gate section
if grep -q '### A1' "$FIX/premature-done.md"; then
  fail "fixture error"
fi
if bash "$ROOT/scripts/rubric-report.sh" kafka "$FIX/premature-done.md" "$FIX/out-premature.md" 2>"$FIX/err-premature.txt"; then
  fail "premature-done fixture must fail structure check"
fi
pass "premature completion without dual-layer is rejected"

# --- 3b) Git roundtable live calibration must prove the complete path ---
ROUND_TABLE_GIT="$(ls -1 "$ROOT"/corpus/runs/*-git-roundtable.md 2>/dev/null | tail -n 1 || true)"
[[ -n "$ROUND_TABLE_GIT" ]] || fail "missing Git roundtable calibration deliverable"
grep -q '圆桌提议' "$ROUND_TABLE_GIT" || fail "Git roundtable deliverable missing proposal"
grep -q '用户同意' "$ROUND_TABLE_GIT" || fail "Git roundtable deliverable missing consent"
grep -q '综合结论' "$ROUND_TABLE_GIT" || fail "Git roundtable deliverable missing synthesis"
lens_count="$(grep -c '^## Lens:' "$ROUND_TABLE_GIT" || true)"
[[ "$lens_count" -ge 2 ]] || fail "Git roundtable deliverable needs at least two lenses"
for contract in '### On the decision point' '### Heuristics applied' '### Risks / what they'
do
  grep -q "$contract" "$ROUND_TABLE_GIT" || fail "Git roundtable deliverable missing lens contract: $contract"
done
pass "Git roundtable calibration proves proposal, consent, lenses, and synthesis"

# --- 4) agent-runtime themes: golden RUBRIC must name permission / HITL / observe loop ---
AR_RUBRIC="$ROOT/corpus/golden/agent-runtime/RUBRIC.md"
[[ -f "$AR_RUBRIC" ]] || fail "missing agent-runtime RUBRIC"
grep -qiE '权限|permission|鉴权' "$AR_RUBRIC" || fail "agent-runtime RUBRIC must mention permission"
grep -qiE '人审|HITL|审批|human' "$AR_RUBRIC" || fail "agent-runtime RUBRIC must mention human review"
grep -qiE '观察|observe|轨迹|tool loop|工具循环|plan' "$AR_RUBRIC" || fail "agent-runtime RUBRIC must mention observe/tool loop"
pass "agent-runtime RUBRIC covers permission, human review, observe loop"

# If a dedicated cal exists, it must be dual-layer and mention those themes
CAL_AR="$(ls -1 "$ROOT"/corpus/runs/*-cal-agent-runtime.md 2>/dev/null | tail -n 1 || true)"
if [[ -n "${CAL_AR}" ]]; then
  bash "$ROOT/scripts/rubric-report.sh" agent-runtime "$CAL_AR" "$FIX/out-cal-ar.md" \
    || fail "agent-runtime cal failed structure check"
  grep -qiE '权限|permission|鉴权|审批|人审|HITL' "$CAL_AR" || fail "agent-runtime cal missing permission/HITL themes"
  grep -qiE '观察|observe|工具循环|plan/act|轨迹' "$CAL_AR" || fail "agent-runtime cal missing observe/loop themes"
  grep -qE '\*\*PASS\*\*|判定：.*PASS|判定：\*\*PASS\*\*' "$CAL_AR" || fail "agent-runtime cal must record PASS"
  pass "agent-runtime dedicated cal present and thematically sufficient ($CAL_AR)"
else
  fail "missing dedicated agent-runtime calibration run (corpus/runs/*-cal-agent-runtime.md)"
fi

# --- 5) README must document Codex install ---
grep -q 'Codex' "$ROOT/README.md" || fail "README must mention Codex"
grep -qE '\.codex/skills|CODEX_HOME' "$ROOT/README.md" || fail "README must give Codex skills path"
grep -q '\.cursor/skills' "$ROOT/README.md" || fail "README must keep Cursor path"
pass "README documents Cursor and Codex install"

echo "OK: all pressure tests passed"
