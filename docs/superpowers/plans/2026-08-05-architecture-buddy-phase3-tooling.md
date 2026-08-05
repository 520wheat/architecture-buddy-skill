# Architecture Buddy Phase 3 Tooling + Blind-Spot Goldens Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sp-subagent-driven-development (recommended) or sp-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 落地 Phase 3：半自动 RUBRIC 对照报告工具、skill↔金标版本矩阵，并补盲区金标 `etcd` + `minecraft`（各带 RUBRIC；etcd 做一次复现校准 PASS）。

**Architecture:** 维护者工具放 `scripts/` + `docs/build/`；版本矩阵 `corpus/COMPAT.md` 记录「哪版 skill 通过哪些金标/校准」；扩库继续双层 GOLDEN 惯例。Minecraft 以「共享模拟世界 / 客户端预测与权威服」问题类写金标，SOURCES 标明公开资料边界，不假装有官方架构白皮书。

**Tech Stack:** Bash + Markdown；现有 `check-architecture-buddy.sh`；无新运行时依赖。

## Global Constraints

- 工作区：`/Users/apple/Desktop/skill-create`；分支 `feat/deliverable-workflow`
- 规格 §7 Phase 3；ADR-0019（校准不对用户）
- **不 git commit**（等用户）
- 半自动报告**不能**宣称自动 PASS；只做结构检查 + 从 RUBRIC 生成人工勾选表
- 用户侧 SKILL 不引入考试话术

## File map

| 路径 | 职责 |
|------|------|
| `scripts/rubric-report.sh` | 候选 vs 金标：结构门禁 + 导出 RUBRIC 勾选骨架 |
| `docs/build/rubric-report.md` | 工具用法（维护者） |
| `corpus/COMPAT.md` | skill 版本 ↔ 金标/校准 PASS 矩阵 |
| `corpus/golden/*/META.md` | 增补 `corpus_version` / `skill_calibrated` 字段（新金标必填；旧金标批量补一行） |
| `corpus/golden/etcd/*` | CP 协调盲区金标 |
| `corpus/golden/minecraft/*` | 游戏模拟世界问题类金标 |
| `corpus/runs/2026-08-05-cal-etcd.md` | etcd 复现校准 PASS |
| `docs/build/skill-calibration.md` / `corpus/README.md` / acceptance V10 | 收尾 |

---

### Task 1: `rubric-report.sh` + 文档

**Files:**
- Create: `scripts/rubric-report.sh`
- Create: `docs/build/rubric-report.md`
- Modify: `scripts/check-architecture-buddy.sh`（可选：检查 `rubric-report.sh` 可执行且 `--help` 退出 0）

- [ ] **Step 1: 实现脚本**

用法：

```bash
bash scripts/rubric-report.sh <golden_id> <candidate.md> [out.md]
```

行为：
1. 校验 `corpus/golden/<id>/{GOLDEN,RUBRIC}.md` 与候选存在
2. 结构：候选含 `### A1`…`### A8`、`### B1`…`### B5`（缺则 FAIL 退出非 0）
3. 从 RUBRIC 提取「必中」列表项（`- ` 行），写入报告为 `- [ ] …`
4. 提取「幻觉黑名单」为 `- [ ] 未出现：…`
5. 报告头部写明：**本报告不自动判定 PASS；维护者勾选后写入 corpus/runs**
6. `--help` 打印用法，exit 0

- [ ] **Step 2: 用已有 cal-kafka 冒烟跑一遍**

```bash
bash scripts/rubric-report.sh kafka corpus/runs/2026-08-05-cal-kafka.md /tmp/rubric-kafka.md
head -40 /tmp/rubric-kafka.md
```

Expected: exit 0；含勾选骨架

- [ ] **Step 3: 写 docs/build/rubric-report.md**

- [ ] **Step 4: 暂存说明**

---

### Task 2: 版本矩阵 `corpus/COMPAT.md` + META 字段

**Files:**
- Create: `corpus/COMPAT.md`
- Modify: 全部现有 `corpus/golden/*/META.md`（补兼容字段）
- Modify: `skill/architecture-buddy/SKILL.md` frontmatter 确认 version（当前 0.3.0）

- [ ] **Step 1: 写 COMPAT.md**

表格列：`skill_version` | `golden_id` | `cal_run` | `result` | `date`  
填入 Phase 1/2 已知 PASS（cal-kafka/git/kubernetes、mig-sre-buddy）与 skill `0.3.0`。

- [ ] **Step 2: META 约定**

每个 META 增加（YAML 或列表均可）：

```markdown
- corpus_version: "1"
- skill_calibrated: "0.3.0"   # 最近通过复现校准的 skill 版本；无则写 none
```

旧金标：三种子写 0.3.0；hdfs/spark/agent-runtime 写 none 或 0.3.0-mig-adjacent（如实：无专属 cal 则 `none`）。

- [ ] **Step 3: 暂存说明**

---

### Task 3: etcd 金标 + 复现校准

**Files:**
- Create: `corpus/golden/etcd/{META,GOLDEN,RUBRIC,SOURCES}.md`
- Create: `corpus/runs/2026-08-05-cal-etcd.md`
- Read: `docs/survey/architecture/D2-etcd.md`

- [ ] **Step 1: 写 etcd 双层 GOLDEN**（Raft、MVCC、watch、lease、线性化读路径等）

- [ ] **Step 2: RUBRIC**

- [ ] **Step 3: 复现校准候选 + 对照 PASS**（勿整段抄 GOLDEN）

- [ ] **Step 4: 更新 COMPAT 一行；META skill_calibrated: 0.3.0**

- [ ] **Step 5: check + rubric-report.sh etcd cal 文件 → exit 0**

---

### Task 4: minecraft 金标（盲区）

**Files:**
- Create: `corpus/golden/minecraft/{META,GOLDEN,RUBRIC,SOURCES}.md`
- Optional: `docs/survey/architecture/D9-minecraft-sim.md` 短摘记

- [ ] **Step 1: 问题类定调**

「多人共享体素/实体模拟世界：权威状态、客户端预测、兴趣区域同步、可模组扩展」——不是「怎么写 Java 插件」。

- [ ] **Step 2: 双层 GOLDEN**

机制方向（须在文中讲清并 SOURCES 标注公开依据）：服务端权威、tick 模拟、区块/兴趣管理、协议同步、模组/数据驱动扩展边界。策略：单线程 tick vs 并行区域、代理/群组服、客户端预测强度。

诚实边界：无官方完整架构白皮书则 META/B1 标明「基于公开社区/wiki/协议资料的合理重构，非厂商正典」。

- [ ] **Step 3: RUBRIC + check OK**

- [ ] **Step 4: COMPAT 记 golden 存在、cal `none`（本轮不做 minecraft 复现考，除非时间充裕）**

---

### Task 5: 文档收尾 V10

**Files:**
- Modify: `docs/build/skill-calibration.md`, `corpus/README.md`, `docs/design/acceptance-checklist.md`

- [ ] **Step 1: Phase 3 完成状态与链接**

- [ ] **Step 2: V10**

```markdown
## V10 Phase 3 工具与盲区（维护者）
- [ ] `scripts/rubric-report.sh` 可对 cal 候选生成勾选报告
- [ ] `corpus/COMPAT.md` 记录 skill 0.3.0 与已知 PASS
- [ ] 金标含 etcd、minecraft
- [ ] etcd 复现校准 PASS
```

- [ ] **Step 3: 全量 check OK；提交指令交给用户**

---

## Spec coverage

| 要点 | 任务 |
|------|------|
| 半自动 RUBRIC 报告 | 1 |
| 版本挂钩 | 2、3 |
| 补盲区 | 3–4 |
| 文档 | 5 |

## Placeholder scan

无 TBD；Commit 等用户。
