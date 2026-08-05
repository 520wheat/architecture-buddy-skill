#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/architecture-buddy"
fail() { echo "FAIL: $*" >&2; exit 1; }

[[ -f "$SKILL/SKILL.md" ]] || fail "missing SKILL.md"
head -n 1 "$SKILL/SKILL.md" | grep -q '^---$' || fail "missing YAML frontmatter start"
grep -q '^name: architecture-buddy$' "$SKILL/SKILL.md" || fail "name mismatch"
grep -q '^description:' "$SKILL/SKILL.md" || fail "missing description"
for f in references/mechanisms.md references/strategies-cheatsheet.md references/anti-patterns.md \
         templates/architecture-note.md templates/problem-class-template.md; do
  [[ -f "$SKILL/$f" ]] || fail "missing $f"
done
# V6
if grep -RInE 'nuwa-skill|女娲' "$SKILL" --include='*.md' | grep -viE '构建期|build-time|不得|禁止|不.*调用'; then
  fail "runtime nuwa reference found"
fi
if grep -RInE '(api[_-]?key|secret|token)\s*[:=]\s*['\''"][^'\''"]+['\''"]' "$SKILL"; then
  fail "possible hardcoded secret"
fi
grep -qi '我就是' "$SKILL/SKILL.md" && fail "impersonation phrase" || true
grep -q 'M1' "$SKILL/SKILL.md" || fail "SKILL.md must mention M1"
grep -q 'Top N' "$SKILL/SKILL.md" || fail "SKILL.md must mention Top N"
echo "OK: architecture-buddy static checks passed"
