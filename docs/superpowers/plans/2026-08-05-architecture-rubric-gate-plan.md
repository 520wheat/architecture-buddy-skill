# Architecture Rubric Gate Implementation Plan

> **For agentic workers:** Execute this plan inline with test-first checkpoints. Do not adopt the staged SkillOpt candidate or modify `skill/architecture-buddy/SKILL.md`.

**Goal:** Make the architecture deliverable evaluator enforce the authoritative `A1–A8` and `B1–B6` contract and require minimal, observable B6 boundary evidence.

**Architecture:** Keep deterministic structure and minimum-evidence checks in `scripts/rubric-report.sh`; keep scenario fixtures in `scripts/pressure-test.sh`; synchronize human-facing checklists and golden rubrics without adding new runtime skill rules. The checks are omission guards, not claims of semantic architecture quality.

**Tech Stack:** Bash, Markdown fixtures, existing repository verification scripts.

## Global Constraints

- Preserve unrelated dirty worktree changes.
- Do not modify or adopt `skill/architecture-buddy/SKILL.md` or staged SkillOpt proposals.
- Use `apply_patch` for manual edits.
- Run the failing test before changing the evaluator.
- Do not auto-commit.

### Task 1: Lock the Missing-B6 Failure

**Files:**
- Modify: `scripts/pressure-test.sh`
- Test fixture: generated at `scripts/fixtures/pressure/missing-b6.md`

- [ ] Add a candidate fixture with A1–A8 and B1–B5 but no B6.
- [ ] Add an assertion that `rubric-report.sh` rejects the fixture.
- [ ] Run `bash scripts/pressure-test.sh` and confirm RED because the current evaluator incorrectly accepts the fixture.

### Task 2: Enforce B6 and Minimum Evidence

**Files:**
- Modify: `scripts/rubric-report.sh`

- [ ] Change the structure loop and emitted report from B1–B5 to B1–B6.
- [ ] Add a B6 section extractor that fails when B6 lacks each minimum marker: `变化轴`, `N+1`, `反例`, `可组合能力`, and `复杂度`.
- [ ] Rerun the missing-B6 test and confirm GREEN.
- [ ] Add a failing-B6-evidence fixture/check and verify it is rejected.

### Task 3: Synchronize Maintainer Contracts

**Files:**
- Modify: `docs/design/acceptance-checklist.md`
- Modify: `corpus/golden/*/RUBRIC.md`

- [ ] Change every stale B1–B5 structural statement to B1–B6.
- [ ] State that B6 checks are minimum omission evidence and do not auto-judge architecture quality.
- [ ] Run repository-wide search to confirm no stale structural B1–B5 statement remains in the maintained evaluator docs.

### Task 4: Full Verification

**Files:**
- No additional source changes expected.

- [ ] Run `bash scripts/pressure-test.sh`.
- [ ] Run `bash scripts/check-architecture-buddy.sh`.
- [ ] Run `bash scripts/rubric-report.sh git corpus/runs/git-architecture-design.md /tmp/git-architecture-review.md` and confirm B6 is reported.
- [ ] Run JSON checks and `git diff --check`.
- [ ] Confirm the runtime skill source and installed copy are unchanged.
