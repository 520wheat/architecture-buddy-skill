# Architecture Buddy Phase 2 Expand + Migrate + Distill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sp-subagent-driven-development (recommended) or sp-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 扩三种子外金标（hdfs / spark / agent-runtime），完成一次迁移校准（SRE-Buddy），并从金标库蒸馏/升级至少 1 个透镜（或加固宿主启发式），证明 skill 在未见金标系统上仍能交双层设计。

**Architecture:** Phase 2 按规格 §7：扩库 → 迁移校准 → 构建期蒸馏。Minecraft 本轮不做（缺可靠公开「架构正典」与 survey；列入后续）。Codex 归入问题类 `agent-runtime`（原料：D8 OpenAI Agents / Anthropic Effective Agents）。Hadoop 以 HDFS 设计为正典入口（已有 D3-hdfs survey）。

**Tech Stack:** Markdown corpus；Architecture Buddy skill；现有透镜包；可选对照 `docs/build/nuwa-lens-distill-prompt.md`（构建期，不运行时调女娲）。

## Global Constraints

- 工作区：`/Users/apple/Desktop/skill-create`；分支 `feat/deliverable-workflow`
- 规格 Phase 2；校准边界 ADR-0019（考试不对用户）
- 新 GOLDEN 必须双层 A1–A8 / B1–B5；RUBRIC 含必中+黑名单
- 检查脚本改为扫描 `corpus/golden/*/` 四文件，不再写死仅三 id
- **不 git commit**（等用户授权）；不改 SRE-Buddy 代码
- 透镜：做法立场非名人扮演（ADR-0016）；`disable-model-invocation: true`

## File map

| 路径 | 职责 |
|------|------|
| `scripts/check-architecture-buddy.sh` | 发现式校验所有 `corpus/golden/<id>/` |
| `corpus/golden/hdfs/*` | Hadoop/HDFS 金标 |
| `corpus/golden/spark/*` | Spark 金标（公开设计知识 + 短 META） |
| `corpus/golden/agent-runtime/*` | Agent 运行时/工具编排问题类（Codex 类） |
| `corpus/runs/2026-08-05-mig-sre-buddy.md` | 迁移校准（封存金标对照，正式判定） |
| `skill/architecture-buddy-lens-*/` 或新建透镜 | 至少升级/新增 1 席 |
| `skill/architecture-buddy/references/lens-catalog.md` | 登记新/升级透镜 |
| `docs/build/skill-calibration.md` | Phase 2 状态 |
| `docs/design/acceptance-checklist.md` | V9 |
| `corpus/README.md` | 扩库名单 |

原料：
- HDFS: `docs/survey/architecture/D3-hdfs.md`
- Spark: 公开 Spark 架构文档（写 SOURCES）；可新建短 survey `docs/survey/architecture/D4-spark.md` 若需要
- Agent: `D8-openai-agents-sdk.md`, `D8-anthropic-effective-agents.md`, `D8-langgraph.md`（择要）
- 迁移目标：SRE-Buddy 只读（已有 smoke，本轮写成正式 migration 记录）

---

### Task 1: 发现式金标检查 + HDFS 金标

**Files:**
- Modify: `scripts/check-architecture-buddy.sh`
- Create: `corpus/golden/hdfs/{META,GOLDEN,RUBRIC,SOURCES}.md`
- Optional: 保留 kafka/git/kubernetes 仍被扫描到

- [ ] **Step 1: 改检查脚本**

将写死的 `for id in kafka git kubernetes` 改为发现目录：

```bash
shopt -s nullglob
golden_dirs=("$ROOT"/corpus/golden/*/)
[[ ${#golden_dirs[@]} -ge 3 ]] || fail "expected ≥3 golden dirs"
for dir in "${golden_dirs[@]}"; do
  id="$(basename "$dir")"
  [[ "$id" == _* ]] && continue
  for f in META.md GOLDEN.md RUBRIC.md SOURCES.md; do
    [[ -f "$dir/$f" ]] || fail "missing corpus/golden/$id/$f"
  done
  grep -q '### A1' "$dir/GOLDEN.md" || fail "$id GOLDEN missing ### A1"
  grep -q '### B1' "$dir/GOLDEN.md" || fail "$id GOLDEN missing ### B1"
  grep -q '必中' "$dir/RUBRIC.md" || fail "$id RUBRIC missing 必中"
done
echo "OK: golden corpus checks passed (${#golden_dirs[@]} dirs)"
```

注意：勿与旧循环重复；删掉旧写死循环。

- [ ] **Step 2: 跑检查**（应仍 OK，因已有 3 金标）

- [ ] **Step 3: 写 hdfs 四文件**（质量对齐 kafka GOLDEN；机制含 NameNode/DataNode、块复制、元数据/数据分离等）

- [ ] **Step 4: 检查 OK**

- [ ] **Step 5: 暂存说明（不 commit）**

---

### Task 2: Spark 金标

**Files:**
- Create: `corpus/golden/spark/{META,GOLDEN,RUBRIC,SOURCES}.md`
- Optional Create: `docs/survey/architecture/D4-spark.md`（短摘记，便于溯源）

- [ ] **Step 1: 写 Spark 双层 GOLDEN**

必盖：driver/executor、RDD/DAG 或 DataFrame 执行图、惰性求值与 stage、窄/宽依赖与 shuffle、容错重算；策略对照：MR 一次性作业 vs 内存迭代、集群管理器选项等。

- [ ] **Step 2: RUBRIC ≥5 机制、≥3 策略、幻觉黑名单**（如「Spark 无磁盘/无 shuffle」）

- [ ] **Step 3: 检查 OK**

---

### Task 3: agent-runtime 金标（Codex 类问题）

**Files:**
- Create: `corpus/golden/agent-runtime/{META,GOLDEN,RUBRIC,SOURCES}.md`

- [ ] **Step 1: 定义问题类**

「LLM 编排工具完成任务：规划/调用/观察循环，带权限、人审与可观测边界」——不是某个产品模块图。

- [ ] **Step 2: 写双层 GOLDEN**

原料 D8；机制可含：工具循环、状态/记忆边界、权限与审批闸门、可观测轨迹；策略：单 agent vs graph、同步工具 vs 异步、是否强制 human-in-loop。

- [ ] **Step 3: RUBRIC + 检查 OK**

---

### Task 4: 迁移校准 — SRE-Buddy

**Files:**
- Create: `corpus/runs/2026-08-05-mig-sre-buddy.md`
- 可读参考：`corpus/runs/2026-08-05-smoke-sre-buddy.md`（可重写提升，勿宣称 GOLDEN）

- [ ] **Step 1: 封存规则**

写候选时**不要打开**任何 `corpus/golden/*/GOLDEN.md` 作抄写；可用 skill 模板与 SRE-Buddy 源码。

- [ ] **Step 2: 完整 deliverable 写入 mig 文件**

- [ ] **Step 3: 校准对照**

```markdown
## 迁移校准对照
- S6 结构
- 陌生读者 5 分钟：能否讲清解决什么 / 主路径 / 不做啥
- 最近邻金标（可选 agent-runtime / log-stream 透镜问题类）：是否乱套类比
- 判定：PASS | RETRY
```

必须 **PASS**；RETRY 则最小改 skill 或重写候选。

- [ ] **Step 4: 检查脚本仍 OK**

---

### Task 5: 蒸馏/升级透镜 ≥1

**Files:**
- Modify or Create: one of
  - `skill/architecture-buddy-lens-gfs-mr/SKILL.md`（用 hdfs/spark 金标加厚），或
  - `skill/architecture-buddy-lens-log-stream/SKILL.md`，或
  - 新建 `skill/architecture-buddy-lens-agent-loop/SKILL.md`（推荐：对齐 agent-runtime 金标）
- Modify: `skill/architecture-buddy/references/lens-catalog.md`
- Follow: `docs/build/nuwa-lens-distill-prompt.md` 结构（可手写蒸馏，不强制跑女娲二进制）

- [ ] **Step 1: 新建或升级透镜**（推荐新建 `agent-loop`）

含：3–7 心智模型（证据≥2）、启发式、would not do、圆桌契约、`disable-model-invocation: true`。

- [ ] **Step 2: 登记 lens-catalog**

- [ ] **Step 3: `bash scripts/check-architecture-buddy.sh` → OK（含新透镜）**

---

### Task 6: 文档与验收 V9

**Files:**
- Modify: `docs/build/skill-calibration.md`, `corpus/README.md`, `docs/design/acceptance-checklist.md`

- [ ] **Step 1: Phase 2 状态与链接**

- [ ] **Step 2: V9 清单**

```markdown
## V9 Phase 2 扩库与迁移（维护者）
- [ ] 金标目录 ≥6（原 3 + hdfs/spark/agent-runtime）
- [ ] 迁移校准 mig-sre-buddy 判定 PASS
- [ ] 至少 1 个透镜新建或金标加厚升级
- [ ] 用户侧 SKILL 仍无开考话术
```

- [ ] **Step 3: 全量检查 OK；向用户提供提交指令**

---

## Spec coverage

| 要点 | 任务 |
|------|------|
| 扩库 | 1–3 |
| 迁移校准 | 4 |
| 蒸馏透镜 | 5 |
| 文档 | 6 |
| Minecraft | 明确不做（本轮） |

## Placeholder scan

无 TBD；Commit 等用户。
