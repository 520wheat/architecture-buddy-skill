# Architecture Quality Scorer Calibration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sp-subagent-driven-development (recommended) or sp-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Calibrate the architecture-quality scorer so structure, automatic defect signals, semantic quality, domain correctness, and roundtable process quality remain separate and keyword presence cannot produce an “excellent” verdict.

**Architecture:** Keep `scripts/architecture-quality-report.sh` as the single maintainer-facing entry point. Add a small heading/body parser inside that script, preserve the existing hard-gate behavior, and expand deterministic pressure fixtures to cover heading-level variants and five semantic counterexamples. The report will continue to emit a manual worksheet; it will not calculate semantic or domain scores.

**Tech Stack:** Bash, POSIX shell tools already used by the repository (`awk`, `grep`, `sed`), Markdown fixtures, existing corpus records.

## Global Constraints

- Do not modify `skill/architecture-buddy/SKILL.md`.
- Do not adopt or edit `.skillopt-sleep/staging/20260805-224117/` candidates.
- Do not add external dependencies or top-level directories.
- Preserve unrelated dirty worktree changes.
- Do not create a git commit in this session.
- Automatic signals may flag omissions but must not assign semantic, domain, roundtable, PASS, or EXCELLENT scores.
- Existing valid `## A1` and `### A1` style headings must be accepted; body text must not count as a section.

---

### Task 1: Add Failing Calibration Fixtures and Assertions

**Files:**
- Modify: `scripts/pressure-test.sh`
- Create: `scripts/fixtures/quality/heading-level-variant.md`
- Create: `scripts/fixtures/quality/empty-b6.md`
- Create: `scripts/fixtures/quality/conclusion-without-evidence.md`
- Test: `scripts/pressure-test.sh`

**Interfaces:**
- Consumes: the current `architecture-quality-report.sh` output format.
- Produces: deterministic failing assertions for heading-level compatibility, empty B6 detection, and manual-only semantic fields.

- [ ] **Step 1: Write the failing fixtures and assertions**

Add a valid deliverable fixture whose A/B sections use a mixture of `## A1`, `### A2`, `## B1`, and `### B6`. Add an empty-B6 fixture with all required headings but no B6 evidence. Extend `pressure-test.sh` with assertions that:

```text
heading-level-variant.md -> hard_gate PASS and no structure-incomplete flag
empty-b6.md -> hard_gate REJECT and b6-evidence-insufficient flag
any generated report -> semantic_quality_score MANUAL / 100
any generated report -> no automatic PASS or EXCELLENT conclusion
```

- [ ] **Step 2: Run the new assertions to verify RED**

Run:

```bash
bash scripts/pressure-test.sh
```

Expected: FAIL because the current parser only accepts `###` headings and the current report does not yet enforce the new manual-only conclusion guard in the added assertions.

- [ ] **Step 3: Record the expected failure**

Confirm the failure identifies the heading-level variant or the new report contract, not a fixture syntax error. Do not change the production scorer before this failure is observed.

---

### Task 2: Implement Heading Parsing and Section Body Extraction

**Files:**
- Modify: `scripts/architecture-quality-report.sh`
- Test: `scripts/pressure-test.sh`

**Interfaces:**
- Consumes: Markdown files with ATX headings from level 2 through level 6.
- Produces: `section_present(section)` behavior and `section_body(section)` extraction that only match complete heading identifiers.

- [ ] **Step 1: Implement the minimal parser change**

Replace fixed `^### A${i}` checks with a heading matcher equivalent to:

```bash
^#{2,6}[[:space:]]+A${i}([[:space:]]|$)
```

Update `section_body()` to recognize the same heading range, capture the heading level, and stop at the next heading whose level is less than or equal to the target section level. Do not match prose, table cells, or headings such as `A10`.

- [ ] **Step 2: Run the focused pressure test**

Run:

```bash
bash scripts/pressure-test.sh
```

Expected: the heading-level variant passes its structure assertion; existing incomplete, missing-B6, and premature-completion checks remain green.

- [ ] **Step 3: Check parser edge cases**

Run the scorer directly against a fixture containing prose mentions of `A1` and `B6`, then confirm those mentions do not satisfy section presence or B6 body extraction.

---

### Task 3: Separate Hard Gates from Diagnostic Signals

**Files:**
- Modify: `scripts/architecture-quality-report.sh`
- Modify: `scripts/pressure-test.sh`
- Modify: `scripts/fixtures/quality/module-list-only.md`
- Modify: `scripts/fixtures/quality/meeting-record-only.md`
- Modify: `scripts/fixtures/quality/b6-title-empty.md`
- Modify: `scripts/fixtures/quality/roundtable-without-synthesis.md`
- Modify: `scripts/fixtures/quality/conclusion-without-evidence.md`

**Interfaces:**
- Consumes: existing quality fixtures and section bodies.
- Produces: stable flags `module-list-only`, `meeting-record-only`, `b6-evidence-insufficient`, `roundtable-synthesis-missing`, and `evidence-and-cost-debt`.

- [ ] **Step 1: Add failing assertions for the five counterexamples**

Extend the pressure test to run the scorer on each fixture and assert:

```text
module-list-only.md -> REJECT and module-list-only
meeting-record-only.md -> REJECT and meeting-record-only
b6-title-empty.md -> REJECT and b6-evidence-insufficient
roundtable-without-synthesis.md -> roundtable-signal synthesis-missing
conclusion-without-evidence.md -> REJECT and evidence-and-cost-debt
```

Also assert that a document containing the word `圆桌` plus a valid `综合结论` does not receive `synthesis-missing` solely because roundtable text exists.

- [ ] **Step 2: Run the focused pressure test to verify RED**

Run:

```bash
bash scripts/pressure-test.sh
```

Expected: at least one new assertion fails because current signals depend on the fixed heading parser and do not consistently classify the new fixtures.

- [ ] **Step 3: Implement the minimal signal logic**

Use section presence and body length/content, not raw keyword success, to classify the fixtures. Keep keywords as diagnostic evidence only. A signal may make the hard gate `REJECT`, but it must never write a semantic score or automatic `PASS`/`EXCELLENT` verdict.

- [ ] **Step 4: Run the focused pressure test to verify GREEN**

Run:

```bash
bash scripts/pressure-test.sh
```

Expected: all five counterexamples are classified as specified, while the complete minimal deliverable remains accepted.

---

### Task 4: Lock the Manual Score Contract

**Files:**
- Modify: `scripts/architecture-quality-report.sh`
- Modify: `scripts/pressure-test.sh`

**Interfaces:**
- Consumes: hard-gate result and diagnostic flags.
- Produces: report fields `structure_score`, `semantic_quality_score`, `domain_score`, `roundtable_score`, and `human_review` with no automatic semantic verdict.

- [ ] **Step 1: Add failing report-contract assertions**

Assert that generated reports contain:

```text
semantic_quality_score | _MANUAL / 100_
domain_score | _MANUAL / 100_
roundtable_score | _MANUAL / 20 or not-needed_
human_review | _PENDING_
```

Assert that no generated report contains a computed `PASS` or `EXCELLENT` reviewer conclusion.

- [ ] **Step 2: Run the assertions to verify RED**

Run:

```bash
bash scripts/pressure-test.sh
```

Expected: FAIL if any report path still emits an automatic semantic verdict or lacks one of the manual fields.

- [ ] **Step 3: Implement the minimal report wording change**

Keep the current worksheet fields and make the conclusion explicitly pending until a human fills the five dimensions, domain review, roundtable review, and reverse-keyword review. Do not add a numeric semantic calculation to Bash.

- [ ] **Step 4: Run the assertions to verify GREEN**

Run:

```bash
bash scripts/pressure-test.sh
```

Expected: the report contract passes and all previous pressure checks remain green.

---

### Task 5: Run Full Regression and Record Calibration Results

**Files:**
- Create: `corpus/runs/2026-08-05-architecture-quality-scorer-calibration.md`
- Modify: `docs/build/rubric-report.md` only if the observed result requires a factual update.

**Interfaces:**
- Consumes: calibrated scorer, existing Git/Kafka/etcd/Agent Runtime records, pressure fixtures.
- Produces: reproducible calibration record distinguishing automatic flags from human semantic conclusions.

- [ ] **Step 1: Run the complete verification suite**

Run:

```bash
bash scripts/check-architecture-buddy.sh
bash scripts/pressure-test.sh
bash -n scripts/architecture-quality-report.sh scripts/pressure-test.sh scripts/check-architecture-buddy.sh scripts/rubric-report.sh
git diff --check
```

Expected: all checks pass and the scorer does not modify `SKILL.md`.

- [ ] **Step 2: Generate reports for existing corpus records**

Run the scorer against the existing Git, Kafka, etcd, and Agent Runtime deliverable records. Record only automatic structure/diagnostic output; leave semantic, domain, roundtable, and human fields pending unless manually reviewed in the same run.

- [ ] **Step 3: Record the before/after interpretation**

Document that valid heading levels no longer produce structure false negatives, all five negative fixtures remain non-excellent, and automatic output does not claim semantic quality. Include any remaining false positives as explicit residual risks.

- [ ] **Step 4: Final review**

Run:

```bash
cmp -s skill/architecture-buddy/SKILL.md /Users/apple/.codex/skills/architecture-buddy/SKILL.md
git status --short
```

Expected: source and installed `SKILL.md` remain identical; only scorer, fixtures, documentation, and calibration records are changed by this task.
