#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/skill/architecture-buddy"
fail() { echo "FAIL: $*" >&2; exit 1; }

[[ -f "$SKILL/SKILL.md" ]] || fail "missing SKILL.md"
head -n 1 "$SKILL/SKILL.md" | grep -q '^---$' || fail "missing YAML frontmatter start"
grep -q '^name: architecture-buddy$' "$SKILL/SKILL.md" || fail "name mismatch"
grep -q '^description:' "$SKILL/SKILL.md" || fail "missing description"
for f in references/mechanisms.md references/strategies-cheatsheet.md references/anti-patterns.md \
         references/lens-catalog.md templates/architecture-note.md templates/problem-class-template.md; do
  [[ -f "$SKILL/$f" ]] || fail "missing $f"
done
# UX / FP guards
grep -q '第一性原理' "$SKILL/SKILL.md" || fail "SKILL.md must define 第一性原理"
grep -q '禁止' "$SKILL/SKILL.md" || fail "SKILL.md must include UX prohibitions"
grep -qE '硬/软/不写|A/B/C/D 考试' "$SKILL/SKILL.md" || fail "SKILL.md must ban quiz/matrix UX"
# V6
nuwa_hits="$(grep -RInE 'nuwa-skill|女娲' "$SKILL" --include='*.md' || true)"
if [[ -n "$nuwa_hits" ]]; then
  runtime_nuwa_hits="$(printf '%s\n' "$nuwa_hits" | grep -vE '构建期|build-time|女娲仅|运行时禁止|不运行时调用|不运行时调用女娲|与女娲所蒸馏' || true)"
  if [[ -n "$runtime_nuwa_hits" ]]; then
    printf '%s\n' "$runtime_nuwa_hits"
    fail "runtime nuwa reference found"
  fi
fi
if grep -RInE '(api[_-]?key|secret|token)\s*[:=]\s*['\''"][^'\''"]+['\''"]' "$SKILL"; then
  fail "possible hardcoded secret"
fi
grep -qi '我就是' "$SKILL/SKILL.md" && fail "impersonation phrase" || true
grep -q '机制' "$SKILL/SKILL.md" || fail "SKILL.md must mention 机制"
grep -q 'Top N' "$SKILL/SKILL.md" || fail "SKILL.md must mention Top N"
echo "OK: architecture-buddy static checks passed"

lens_count=0
for LENS in "$ROOT"/skill/architecture-buddy-lens-*; do
  [[ -d "$LENS" ]] || continue
  lens_count=$((lens_count + 1))
  lens_name="$(basename "$LENS")"
  [[ -f "$LENS/SKILL.md" ]] || fail "missing $lens_name/SKILL.md"
  grep -q "^name: $lens_name$" "$LENS/SKILL.md" || fail "$lens_name name mismatch"
  grep -q 'On the decision point' "$LENS/SKILL.md" || fail "$lens_name missing contract"
  grep -qi '我就是' "$LENS/SKILL.md" && fail "$lens_name impersonation phrase" || true
done
if [[ "$lens_count" -gt 0 ]]; then
  echo "OK: lens checks passed ($lens_count lenses)"
fi
