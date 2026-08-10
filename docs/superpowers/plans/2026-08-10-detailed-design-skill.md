# 详细设计 Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sp-subagent-driven-development (recommended) or sp-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有架构透镜统一为 `architecture-buddy` 内部资源，并新增可由架构设计交接或直接调用的 `detailed-design` Skill，产出面向开发实现的详细设计文档。

**Architecture:** `architecture-buddy` 继续负责架构设计和 `design-ready` 门禁，内部 `lenses/` 按需提供领域视角；`detailed-design` 作为独立 Skill 通过显式 Markdown 交接承接架构设计。详细设计由阶段 Prompt 驱动，使用独立模板和 Python 标准库校验脚本生成总览、模块文档和架构回退项。

**Tech Stack:** Markdown、YAML、Python 3 标准库、POSIX shell；不增加第三方依赖。

## Global Constraints

- 只支持代码系统的详细设计。
- 只承接 `pre-development/design-ready` 的架构设计。
- 不读取已有项目代码，不做 `reference/retrospective` 反向详细设计。
- 不生成代码、代码空骨架、数据库迁移或可编译实现。
- 不改变模块边界、数据归属、信任边界、一致性模型或核心质量属性。
- 详细设计发现架构级冲突时，暂停并回退到 `architecture-buddy`。
- 复用现有圆桌主持和架构透镜机制，不新增详细设计透镜。
- 现有 8 个透镜迁移到 `skill/architecture-buddy/lenses/`，不再作为独立安装包。
- Prompt、模板、参考资料和脚本必须自包含，不引用 `docs/`、`corpus/`、本机绝对路径或开发仓库文件。
- 脚本只使用 Python 标准库，不联网、不调用 SkillOpt、不修改用户项目。
- 默认不覆盖、不删除用户输出目录中的文件；目录迁移只处理本仓库已确认的旧透镜目录。
- 用户可见运行内容使用中文，协议字段、技术术语、路径和命令保留英文。

---

### Task 1: 统一架构透镜目录

**Files:**
- Move: `skill/architecture-buddy-lens-agent-loop/SKILL.md` -> `skill/architecture-buddy/lenses/agent-loop.md`
- Move: `skill/architecture-buddy-lens-dynamo-ap/SKILL.md` -> `skill/architecture-buddy/lenses/dynamo-ap.md`
- Move: `skill/architecture-buddy-lens-gfs-mr/SKILL.md` -> `skill/architecture-buddy/lenses/gfs-mr.md`
- Move: `skill/architecture-buddy-lens-log-stream/SKILL.md` -> `skill/architecture-buddy/lenses/log-stream.md`
- Move: `skill/architecture-buddy-lens-raft-cp/SKILL.md` -> `skill/architecture-buddy/lenses/raft-cp.md`
- Move: `skill/architecture-buddy-lens-scaffold/SKILL.md` -> `skill/architecture-buddy/lenses/scaffold.md`
- Move: `skill/architecture-buddy-lens-spanner-sql/SKILL.md` -> `skill/architecture-buddy/lenses/spanner-sql.md`
- Move: `skill/architecture-buddy-lens-zta-resource/SKILL.md` -> `skill/architecture-buddy/lenses/zta-resource.md`
- Modify: `skill/architecture-buddy/references/lens-catalog.md`
- Modify: `skill/architecture-buddy/SKILL.md`
- Delete: the eight empty legacy lens directories after successful migration

**Interfaces:**
- Consumes: the existing eight lens `SKILL.md` files and the current lens catalog.
- Produces: eight internal lens Markdown resources whose domain guidance and five-part roundtable output contract are unchanged; all host references resolve to `lenses/*.md`.

- [ ] **Step 1: Record the existing lens inventory**

Run:

```bash
find skill -maxdepth 2 -type f -path '*/SKILL.md' | sort
```

Expected: one host Skill and eight lens Skills are listed before migration.

- [ ] **Step 2: Create the internal lens directory**

Run:

```bash
mkdir -p skill/architecture-buddy/lenses
```

Expected: `skill/architecture-buddy/lenses` exists and contains no files before migration.

- [ ] **Step 3: Move each lens and remove Skill-only metadata**

Move the eight files using the exact mapping in the Files section. In each moved file, remove the Agent Skill frontmatter fields `name`, `description`, and `disable-model-invocation`; retain the display name, version, stance, best-for, not-for, evidence anchors, domain guidance, and the complete `Roundtable Output Contract` as internal lens metadata and content.

- [ ] **Step 4: Update the lens catalog and host references**

Replace every install-package path such as `architecture-buddy-lens-raft-cp/SKILL.md` with `architecture-buddy/lenses/raft-cp.md`. State that lenses are internal resources loaded by the host and are not individually installed.

- [ ] **Step 5: Remove legacy directories after content comparison**

For each lens, compare the moved body with the original body and confirm the output contract is present. Then remove only the eight named legacy directories.

- [ ] **Step 6: Verify the migration**

Run:

```bash
test "$(find skill/architecture-buddy/lenses -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" = 8
test "$(find skill -maxdepth 1 -type d -name 'architecture-buddy-lens-*' | wc -l | tr -d ' ')" = 0
rg -n 'architecture-buddy-lens-' skill/architecture-buddy skill/README.md README.md skill/release-manifest.tsv
```

Expected: the first two commands succeed; the final command produces no legacy package references.

- [ ] **Step 7: Commit the independently reviewable migration**

```bash
git add -A skill/architecture-buddy \
  skill/architecture-buddy-lens-agent-loop \
  skill/architecture-buddy-lens-dynamo-ap \
  skill/architecture-buddy-lens-gfs-mr \
  skill/architecture-buddy-lens-log-stream \
  skill/architecture-buddy-lens-raft-cp \
  skill/architecture-buddy-lens-scaffold \
  skill/architecture-buddy-lens-spanner-sql \
  skill/architecture-buddy-lens-zta-resource
git commit -m "refactor(skill): 统一架构透镜目录"
```

### Task 2: Create the detailed-design package contract

**Files:**
- Create: `skill/detailed-design/SKILL.md`
- Create: `skill/detailed-design/README.md`
- Create: `skill/detailed-design/agents/openai.yaml`
- Create: `skill/detailed-design/references/architecture-handoff.md`
- Create: `skill/detailed-design/references/detailed-design-gate.md`

**Interfaces:**
- Consumes: an explicit architecture handoff containing the architecture file, ADR paths, `pre-development`, `design-ready`, scope, confirmed boundaries, quality targets, pending facts, and non-goals.
- Produces: a standalone Skill contract with direct and handoff entry points, DD0-DD7 phase routing, strict architecture rollback rules, and the output state values `draft`, `blocked`, and `design-ready`.

- [ ] **Step 1: Write the failing package contract check**

Run:

```bash
test -f skill/detailed-design/SKILL.md
```

Expected: FAIL because the package does not exist yet.

- [ ] **Step 2: Create the package directories**

Run:

```bash
mkdir -p skill/detailed-design/{agents,prompts,references,templates,scripts}
```

- [ ] **Step 3: Write `SKILL.md`**

The frontmatter must use `name: detailed-design`, a description beginning with `Use when`, and a display name. The body must define:

```text
Role: implementation-level design partner for code systems.
Accepted scene: pre-development only.
Required input: architecture design plus ADR or equivalent handoff.
Entry points: architecture-buddy handoff and direct user invocation.
Phases: DD0 input validation, DD1 scope, DD2 contracts, DD3 data/state,
DD4 behavior/failure, DD5 cross-cutting rules, DD6 testing/order, DD7 review.
Rollback: architecture-level conflict pauses the flow and returns to architecture-buddy.
Outputs: overview, module documents, and architecture feedback.
Forbidden: source-code reading, code generation, architecture override.
```

Each phase must load only its corresponding Prompt and must explain why the current question is being asked before asking one question.

- [ ] **Step 4: Write the handoff reference**

`architecture-handoff.md` must define the required fields, acceptable file-based or message-based handoff, path resolution rules, and the difference between a missing non-critical fact and a blocking architecture fact.

- [ ] **Step 5: Write the completion gate reference**

`detailed-design-gate.md` must check module coverage, interface/data/state completeness, cross-module consistency, failure semantics, concurrency, security, observability, tests, defaults for pending facts, and rollback items. It must explicitly state that keyword presence is not quality proof.

- [ ] **Step 6: Write package README and Agent metadata**

The README must document direct installation, architecture handoff, output layout, and the fact that the package does not generate code. `openai.yaml` must describe the Skill without copying the entire workflow into the description.

- [ ] **Step 7: Verify the package contract**

Run:

```bash
test -f skill/detailed-design/SKILL.md
rg -n '^name: detailed-design$|^description:.*Use when|DD0|DD7|design-ready|blocked|architecture-buddy' skill/detailed-design/SKILL.md
python3 - <<'PY'
from pathlib import Path
required = [
    Path('skill/detailed-design/SKILL.md'),
    Path('skill/detailed-design/README.md'),
    Path('skill/detailed-design/agents/openai.yaml'),
    Path('skill/detailed-design/references/architecture-handoff.md'),
    Path('skill/detailed-design/references/detailed-design-gate.md'),
]
missing = [str(path) for path in required if not path.is_file() or not path.read_text().strip()]
if missing:
    raise SystemExit('missing or empty: ' + ', '.join(missing))
PY
```

Expected: all commands succeed and no required file is empty.

- [ ] **Step 8: Commit the package contract**

```bash
git add skill/detailed-design
git commit -m "feat(skill): 增加详细设计 Skill 契约"
```

### Task 3: Add detailed-design workflow Prompts

**Files:**
- Create: `skill/detailed-design/prompts/clarify-scope.md`
- Create: `skill/detailed-design/prompts/decompose-design-units.md`
- Create: `skill/detailed-design/prompts/design-contracts.md`
- Create: `skill/detailed-design/prompts/design-data-state.md`
- Create: `skill/detailed-design/prompts/design-behavior-and-failure.md`
- Create: `skill/detailed-design/prompts/synthesize-deliverable.md`
- Create: `skill/detailed-design/prompts/review-deliverable.md`
- Modify: `skill/detailed-design/SKILL.md`

**Interfaces:**
- Consumes: the explicit output of the preceding phase; no Prompt may depend on hidden conversation state.
- Produces: phase-specific Markdown blocks that the next phase can consume, with one current question and explicit user confirmation points.

- [ ] **Step 1: Define the shared Prompt contract**

Every Prompt must include these sections in Chinese:

```text
何时加载
目标
输入
执行
输出契约
不得做
阻塞处理
```

Every output must identify confirmed facts, pending facts, decisions, affected files, and the single next question.

- [ ] **Step 2: Write scope and decomposition Prompts**

`clarify-scope.md` validates the handoff, asks for scope only when absent, and blocks on architecture-level omissions. `decompose-design-units.md` maps confirmed architecture modules to detailed-design units and asks the user to confirm order or exclusions.

- [ ] **Step 3: Write contract and data/state Prompts**

`design-contracts.md` covers module responsibilities, allowed callers, forbidden edges, interfaces, request/response, errors, versions, and idempotency. `design-data-state.md` covers fields, constraints, ownership, lifecycle, state transitions, invariants, visibility, persistence, and concurrency without changing architecture-level ownership or consistency.

- [ ] **Step 4: Write behavior/failure and synthesis Prompts**

`design-behavior-and-failure.md` requires an end-to-end flow and structured failure evidence for timeout, disconnect, duplicate request, missing external confirmation, dependency failure, and partial success. `synthesize-deliverable.md` produces overview, module documents, and architecture feedback references.

- [ ] **Step 5: Write review Prompt**

`review-deliverable.md` applies the detailed-design gate, distinguishes `draft`, `blocked`, and `design-ready`, and refuses to claim completion when a blocking architecture fact or cross-module inconsistency remains.

- [ ] **Step 6: Register loading conditions in `SKILL.md`**

The main Skill must map DD0-DD7 to the seven Prompt files and state that only one phase Prompt is loaded at a time.

- [ ] **Step 7: Verify Prompt completeness**

Run:

```bash
for file in skill/detailed-design/prompts/*.md; do
  test -s "$file"
  rg -q '^## (何时加载|目标|输入|执行|输出契约|不得做|阻塞处理)$' "$file"
done
rg -n 'prompts/(clarify-scope|decompose-design-units|design-contracts|design-data-state|design-behavior-and-failure|synthesize-deliverable|review-deliverable)\.md' skill/detailed-design/SKILL.md
```

Expected: all seven files contain the shared sections and all seven are referenced by the host Skill.

- [ ] **Step 8: Commit the workflow Prompts**

```bash
git add skill/detailed-design/SKILL.md skill/detailed-design/prompts
git commit -m "feat(skill): 增加详细设计流程 Prompt"
```

### Task 4: Add detailed-design templates and artifact rules

**Files:**
- Create: `skill/detailed-design/templates/detailed-design-overview.md`
- Create: `skill/detailed-design/templates/module-detailed-design.md`
- Create: `skill/detailed-design/templates/architecture-feedback.md`
- Modify: `skill/detailed-design/prompts/synthesize-deliverable.md`
- Modify: `skill/detailed-design/README.md`

**Interfaces:**
- Consumes: confirmed phase outputs from Task 3.
- Produces: a stable overview/module/feedback artifact contract used by the initialization and validation scripts.

- [ ] **Step 1: Write the overview template**

The template must contain these concrete sections: metadata and architecture input, scope and non-goals, design-unit index, module relationship, cross-module contracts, end-to-end flows, unified failure/concurrency/security/observability rules, test strategy, implementation order, pending facts, rollback items, and completion state.

- [ ] **Step 2: Write the module template**

The template must contain: responsibility and boundary, dependencies and forbidden edges, external/internal interfaces, request/response and field constraints, error semantics, state machine and invariants, behavior and sequence, timeout/retry/idempotency/concurrency, permissions/audit/logging/metrics/tracing/configuration, tests, acceptance conditions, and pending facts.

- [ ] **Step 3: Write the architecture feedback template**

The template must record the blocking fact, conflicting design item, affected module, architecture-level question, impact, current state, recovery condition, and the upstream architecture or ADR location to revisit.

- [ ] **Step 4: Bind synthesis to the templates**

Update `synthesize-deliverable.md` to generate the overview first, then one module document per confirmed design unit, and to link every architecture feedback item from the overview. It must not output implementation code.

- [ ] **Step 5: Verify artifact headings**

Run:

```bash
for file in skill/detailed-design/templates/*.md; do test -s "$file"; done
rg -n '架构输入|设计范围|跨模块契约|实现顺序|状态机|幂等|并发|测试|架构回退' skill/detailed-design/templates/*.md
```

Expected: all three templates are non-empty and the required design evidence is present.

- [ ] **Step 6: Commit the artifact contract**

```bash
git add skill/detailed-design/templates skill/detailed-design/prompts/synthesize-deliverable.md skill/detailed-design/README.md
git commit -m "feat(skill): 增加详细设计产物模板"
```

### Task 5: Implement deterministic detailed-design scripts

**Files:**
- Create: `skill/detailed-design/scripts/init-design.py`
- Create: `skill/detailed-design/scripts/validate-input.py`
- Create: `skill/detailed-design/scripts/validate-deliverable.py`
- Modify: `skill/detailed-design/SKILL.md`
- Modify: `skill/detailed-design/README.md`

**Interfaces:**
- Consumes: architecture Markdown, repeated `--adr` paths, a detailed-design output directory, and the three templates from Task 4.
- Produces: initialized output files, non-zero validation errors for invalid input or incomplete output, zero for structurally valid artifacts.

- [ ] **Step 1: Write failing CLI checks**

Run:

```bash
python3 skill/detailed-design/scripts/init-design.py --help
python3 skill/detailed-design/scripts/validate-input.py --help
python3 skill/detailed-design/scripts/validate-deliverable.py --help
```

Expected: FAIL because the scripts do not exist.

- [ ] **Step 2: Implement `init-design.py`**

The CLI must accept `--output DIR` and `--name NAME`, create `detailed-design-overview.md`, `modules/`, and `architecture-feedback.md`, refuse to overwrite any existing target file, support `--force` only when explicitly supplied, and work with spaces and Chinese characters in the output path.

- [ ] **Step 3: Implement `validate-input.py`**

The CLI must accept one architecture file and repeatable `--adr PATH` arguments. It must reject missing files, non-`pre-development` scenes, non-`design-ready` states, missing architecture boundary evidence, missing required handoff fields when handoff mode is used, and unreadable ADR paths. It must accept non-critical pending facts only when each has a default, reason, trigger, and rollback path.

- [ ] **Step 4: Implement `validate-deliverable.py`**

The CLI must accept one output directory, require the overview and at least one module document, reject `blocked` output, require the overview headings and module evidence from Task 4, require cross-module contract and rollback references, and return zero only for structurally complete output. It must state that it does not judge architecture quality.

- [ ] **Step 5: Verify scripts with temporary fixtures**

Run:

```bash
tmp_dir="$(mktemp -d)"
python3 skill/detailed-design/scripts/init-design.py --output "$tmp_dir/design" --name "SRE Buddy"
python3 skill/detailed-design/scripts/init-design.py --output "$tmp_dir/design" --name "SRE Buddy" >/dev/null 2>&1 && exit 1 || true
python3 -m py_compile skill/detailed-design/scripts/*.py
rm -rf "$tmp_dir"
```

Expected: initialization succeeds once, the second initialization refuses overwrite, Python compilation succeeds, and the temporary directory is removed.

- [ ] **Step 6: Document the CLI contract**

Add exact command examples, exit-code semantics, overwrite behavior, path behavior, and the non-quality-judgment boundary to the package README and `SKILL.md`.

- [ ] **Step 7: Commit the scripts**

```bash
git add skill/detailed-design/scripts skill/detailed-design/SKILL.md skill/detailed-design/README.md
git commit -m "feat(skill): 增加详细设计校验工具"
```

### Task 6: Connect architecture-buddy handoff and release metadata

**Files:**
- Modify: `skill/architecture-buddy/SKILL.md`
- Modify: `skill/architecture-buddy/README.md`
- Modify: `skill/architecture-buddy/references/lens-catalog.md`
- Modify: `skill/architecture-buddy/agents/openai.yaml`
- Modify: `skill/README.md`
- Modify: `README.md`
- Modify: `skill/release-manifest.tsv`
- Modify: `skill/detailed-design/README.md`
- Modify: `skill/detailed-design/agents/openai.yaml`

**Interfaces:**
- Consumes: the unified lens tree from Task 1 and the detailed-design package from Tasks 2-5.
- Produces: a discoverable two-package release where architecture-buddy asks before handoff and both direct and handoff detailed-design entry points are documented.

- [ ] **Step 1: Write the failing release checks**

Run:

```bash
test "$(rg -c '^architecture-buddy\\t|^detailed-design\\t' skill/release-manifest.tsv)" = 2
rg -q '是否继续生成面向开发实现的详细设计' skill/architecture-buddy/SKILL.md
rg -q 'detailed-design' skill/README.md README.md
```

Expected: FAIL because the manifest and host Skill do not yet describe the new package and handoff.

- [ ] **Step 2: Add the host handoff section**

After the existing architecture delivery gate, add the exact handoff question and the explicit fields from the approved specification. State that user refusal ends the architecture flow normally and user consent transfers to `detailed-design`.

- [ ] **Step 3: Update host lens loading**

Change the catalog and `SKILL.md` so lenses are loaded from `lenses/*.md`, preserve the dynamic seating rules and complete output contract, and remove instructions that tell users to install lens packages separately.

- [ ] **Step 4: Update package metadata and manifest**

Declare exactly two installable packages: `architecture-buddy` and `detailed-design`. Keep package versions explicit, remove the eight lens package rows, and make README installation commands iterate only over the two direct Skill directories.

- [ ] **Step 5: Verify release metadata**

Run:

```bash
test "$(find skill -mindepth 1 -maxdepth 1 -type d -exec test -f '{}/SKILL.md' ';' -print | wc -l | tr -d ' ')" = 2
test "$(rg -c '^architecture-buddy\\t|^detailed-design\\t' skill/release-manifest.tsv)" = 2
rg -n 'architecture-buddy-lens-|lens-.*SKILL.md' skill README.md
```

Expected: the first two commands succeed; the final command produces no old package-install instructions.

- [ ] **Step 6: Commit host integration**

```bash
git add skill/architecture-buddy skill/detailed-design skill/README.md README.md skill/release-manifest.tsv
git commit -m "feat(skill): 接入详细设计交接流程"
```

### Task 7: Run end-to-end package verification

**Files:**
- Modify: only files that fail the verification checks from Tasks 1-6.

**Interfaces:**
- Consumes: the complete two-package runtime tree and all deterministic scripts.
- Produces: verified install layout, successful script checks, and a clean diff without stale package references or external runtime dependencies.

- [ ] **Step 1: Validate all Python scripts**

```bash
python3 -m py_compile skill/architecture-buddy/scripts/*.py skill/detailed-design/scripts/*.py
```

Expected: exit code 0.

- [ ] **Step 2: Validate the architecture package**

```bash
rg -q 'Roundtable Output Contract' skill/architecture-buddy/lenses/*.md
```

Expected: lens contracts are present. The architecture validator is not used as the detailed-design validator and may reject the feature specification because it is not an architecture deliverable.

- [ ] **Step 3: Run detailed-design valid and invalid fixtures**

Create temporary Markdown fixtures with `pre-development`, `design-ready`, module boundary, interface, data/state, ADR, and pending-fact sections. Confirm `validate-input.py` accepts the valid fixture and rejects each of: `draft`, `blocked`, missing boundary, missing ADR, and pending fact without a rollback path. Confirm `validate-deliverable.py` accepts a complete overview plus module file and rejects missing module evidence and blocked state.

- [ ] **Step 4: Check package self-containment**

Run:

```bash
rg -n '/Users/|/var/|docs/|corpus/|skillopt|nuwa' skill/architecture-buddy skill/detailed-design README.md skill/README.md
```

Expected: no development-only absolute paths or forbidden runtime dependencies are found. Any `docs/` mention must be an explanatory non-runtime reference in a top-level README, not a required runtime path.

- [ ] **Step 5: Check formatting and status**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only intended implementation files are modified or untracked.

- [ ] **Step 6: Commit verification fixes if required**

```bash
git add skill README.md
git commit -m "test(skill): 验证详细设计 Skill 发行包"
```

Run this commit only when Task 7 required a fix. If no fix is needed, retain the prior task commits and record the verification output in the final handoff.
