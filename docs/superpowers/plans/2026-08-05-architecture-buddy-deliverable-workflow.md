# Architecture Buddy Deliverable Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sp-subagent-driven-development (recommended) or sp-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 Architecture Buddy 在用户要求「完整架构设计」时，默认走 `deliverable` 阶段门禁，产出双层（叙事 A + 机制/策略 B）可读成品，并用静态检查与验收清单拦住半成品。

**Architecture:** Phase 0 only——改宿主 `SKILL.md`、新增权威模板 `architecture-deliverable.md`、把 M1–M9 降为内部映射、扩展 `check-architecture-buddy.sh` 与验收清单、新增 ADR 锁定「考试仅训练 skill」。金标库与对内校准属 Phase 1，本计划只留目录占位与指向规格的说明，不写三份 GOLDEN。

**Tech Stack:** Agent Skills（Markdown + YAML frontmatter）；Bash 静态校验；无运行时语言依赖。

## Global Constraints

- 工作区根：`/Users/apple/Desktop/skill-create`
- 规格权威：`docs/superpowers/specs/2026-08-05-architecture-buddy-deliverable-workflow-design.md`
- 包路径：`skill/architecture-buddy/`；frontmatter `name: architecture-buddy`
- 禁止运行时调用女娲；禁止硬编码密钥
- 考试/复现校准话术**不得**出现在用户可见宿主流程（可出现在 `docs/build/`）
- 用户可见成品禁止以 M1–M9 为权威结构；M 编号仅内部映射
- 本仓库默认：**未经用户明确要求不得 `git commit`**；计划中 Commit 步改为「列出暂存文件 + 等用户授权」
- 保持 ADR-0018：真第一性原理三步；禁止问卷/硬软矩阵 UX

## File map

| 路径 | 职责 |
|------|------|
| `docs/adr/0019-deliverable-workflow-and-calibration-boundary.md` | 锁定 draft/deliverable、双层成品、考试仅对内 |
| `skill/architecture-buddy/templates/architecture-deliverable.md` | 用户可见权威双层骨架 |
| `skill/architecture-buddy/references/deliverable-gate.md` | S6 完成门禁清单（给 Agent 自检） |
| `skill/architecture-buddy/references/note-mapping.md` | 双层成品 ↔ 旧 M1–M9 内部映射 |
| `skill/architecture-buddy/templates/architecture-note.md` | 顶部加「已降级」说明，保留供映射 |
| `skill/architecture-buddy/SKILL.md` | 模式、S0–S7、双层交付、门禁；保留 UX/FP/圆桌 |
| `scripts/check-architecture-buddy.sh` | 校验新模板、门禁文件、SKILL 关键词 |
| `docs/design/acceptance-checklist.md` | 增补 V7 deliverable；修正过时 V1「结果/约束/优化」 |
| `docs/build/skill-calibration.md` | 维护者对内校准流程（Phase 1 入口，本计划写骨架） |
| `corpus/README.md` | 金标库约定与 Phase 1 种子名单 |
| `skill/architecture-buddy/README.md` | 同步 draft/deliverable 说明 |
| `docs/superpowers/specs/2026-08-05-architecture-buddy-deliverable-workflow-design.md` | 状态改为 Accepted（实现启动时） |

---

### Task 1: ADR-0019 + 规格状态

**Files:**
- Create: `docs/adr/0019-deliverable-workflow-and-calibration-boundary.md`
- Modify: `docs/adr/README.md`（若存在索引则追加一行）
- Modify: `docs/superpowers/specs/2026-08-05-architecture-buddy-deliverable-workflow-design.md`（状态 → Accepted）

**Interfaces:**
- Consumes: 规格 §3–§6 决策表
- Produces: ADR-0019 Accepted，供后续任务引用

- [ ] **Step 1: 写 ADR-0019**

内容必须包含（可润色，不可缺条）：

```markdown
# ADR-0019: deliverable 工作流与校准边界

## Status
Accepted

## Context
Skill 能跑完对话却交不出可读架构设计；用户反馈看不懂成品在说什么。
需要完成门禁，并明确「复现/迁移考试」只用于训练 skill。

## Decision
1. 模式：`draft` | `deliverable`；用户要完整架构设计时默认 `deliverable`。
2. 成品：同一文件双层——层 A 叙事（A1–A8）+ 层 B 机制/策略（B1–B5）；缺一层不算完成。
3. `deliverable` 走 S0–S7；未过 S6 禁止宣称完成。
4. 旧 M1–M9 仅为内部映射，不进用户可见正文权威结构。
5. 复现/迁移校准仅维护者/构建期使用；用户 UX 禁止开考、盲写、打分话术。
6. 金标库与三题 PASS 属后续 Phase；本 ADR 锁定边界不锁定金标正文。

## Consequences
- 重写宿主 SKILL 与模板；扩展静态检查与验收 V7。
- ADR-0018 的 UX/FP 规则继续有效，且适用于 deliverable 各阶段。
```

- [ ] **Step 2: 更新 ADR 索引（若有）**

若 `docs/adr/README.md` 有表格/列表，追加 `0019` 一行；若无索引文件则跳过。

- [ ] **Step 3: 规格状态改为 Accepted**

将设计文开头 `状态：Draft — 待用户审阅` 改为 `状态：Accepted`。

- [ ] **Step 4: 暂存说明（不 commit，除非用户授权）**

```bash
git add docs/adr/0019-deliverable-workflow-and-calibration-boundary.md \
  docs/adr/README.md \
  docs/superpowers/specs/2026-08-05-architecture-buddy-deliverable-workflow-design.md
git status
```

Suggested message if authorized: `docs(adr): 锁定 deliverable 工作流与校准边界`

---

### Task 2: 双层模板 + 门禁 + 映射参考（先扩静态检查再补文件）

**Files:**
- Create: `skill/architecture-buddy/templates/architecture-deliverable.md`
- Create: `skill/architecture-buddy/references/deliverable-gate.md`
- Create: `skill/architecture-buddy/references/note-mapping.md`
- Modify: `skill/architecture-buddy/templates/architecture-note.md`（文件头降级说明）
- Modify: `scripts/check-architecture-buddy.sh`

**Interfaces:**
- Consumes: 规格 §4.3、§5
- Produces: 检查脚本要求的路径与章节锚点字符串

- [ ] **Step 1: 先改检查脚本（预期失败）**

在 `scripts/check-architecture-buddy.sh` 的 `for f in ...` 列表中增加：

```bash
references/deliverable-gate.md
references/note-mapping.md
templates/architecture-deliverable.md
```

并在 UX/FP guards 之后增加：

```bash
# Deliverable workflow guards
grep -q 'deliverable' "$SKILL/SKILL.md" || fail "SKILL.md must mention deliverable"
grep -q 'draft' "$SKILL/SKILL.md" || fail "SKILL.md must mention draft"
grep -q 'S6' "$SKILL/SKILL.md" || fail "SKILL.md must mention S6 completion gate"
grep -q 'A1' "$SKILL/templates/architecture-deliverable.md" || fail "deliverable template missing A1"
grep -q 'B1' "$SKILL/templates/architecture-deliverable.md" || fail "deliverable template missing B1"
grep -q '完成门禁' "$SKILL/references/deliverable-gate.md" || fail "gate file missing 完成门禁"
grep -q 'M1' "$SKILL/references/note-mapping.md" || fail "mapping file must mention M1"
# Calibration must not be user-facing exam UX in host skill
if grep -qE '开考|盲写交卷|及格|不及格' "$SKILL/SKILL.md"; then
  fail "SKILL.md must not use exam UX toward users"
fi
```

注意：此时 `SKILL.md` 尚未改，本步跑检查应失败。

- [ ] **Step 2: 跑检查确认失败**

```bash
bash scripts/check-architecture-buddy.sh
```

Expected: `FAIL: missing ...` 或 `must mention deliverable`

- [ ] **Step 3: 写 `architecture-deliverable.md`**

骨架必须含封面 + 层 A（A1–A8）+ 层 B（B1–B5）+ 附录占位。标题与节名示例：

```markdown
# 架构设计：<问题类一句话>

> 模式：deliverable  
> 已定关键决策：…  
> 明确不做：…  
> 待验证事实：…

## 层 A — 叙事

### A1 摘要
### A2 上下文与边界
### A3 主路径
### A4 组件与契约
### A5 状态、失败与恢复
### A6 安全与身份
### A7 演进切片
### A8 如何验收

## 层 B — 机制与策略

### B1 基本事实
### B2 机制
### B3 策略选项
### B4 取舍
### B5 与对照的关系

## 附录（可选）
```

每节下留 1–3 行提示句（写什么），不要留 M 编号。

- [ ] **Step 4: 写 `deliverable-gate.md`**

```markdown
# 完成门禁（S6）

在宣称「架构设计已完成」之前，逐项自检。任一项失败 → 继续补洞，禁止交卷。

1. 摘要能否让陌生人讲清「解决什么 / 不解决什么」
2. 是否有信任/边界与一条端到端主路径
3. 机制与策略是否分开；策略是否有为何选/不选
4. 是否有失败语义与可测验收句（≥3）
5. 是否有演进切片（现在 / 下一刀 / 明确不做）
6. 正文几乎无内部黑话（M1、入口 B、S0…）
```

- [ ] **Step 5: 写 `note-mapping.md`**

用表格映射，例如：B2↔M5.1，B3/B4↔M5.2/M6，A8↔M4 度量，A2↔附录上下文图。注明：写用户成品时用 deliverable 模板；仅维护者对照旧笔记时查本表。

- [ ] **Step 6: 给 `architecture-note.md` 加文件头**

在首行前插入：

```markdown
> **已降级：** 用户可见权威成品请用 `architecture-deliverable.md`。  
> 本文件仅作内部 M1–M9 映射参考，对话中不要拿它当问卷。
```

- [ ] **Step 7: 再跑检查**

```bash
bash scripts/check-architecture-buddy.sh
```

Expected: 仍可能因 `SKILL.md` 缺 deliverable/S6 失败——若只缺 SKILL 项，记下来由 Task 3 修复；模板相关 FAIL 必须已消失。

- [ ] **Step 8: 暂存说明**

```bash
git add skill/architecture-buddy/templates/architecture-deliverable.md \
  skill/architecture-buddy/references/deliverable-gate.md \
  skill/architecture-buddy/references/note-mapping.md \
  skill/architecture-buddy/templates/architecture-note.md \
  scripts/check-architecture-buddy.sh
```

Suggested message: `feat(architecture-buddy): 双层交付模板与完成门禁`

---

### Task 3: 重写宿主 `SKILL.md`（核心）

**Files:**
- Modify: `skill/architecture-buddy/SKILL.md`（全文结构重组，保留 UX 铁律与真 FP）
- Modify: `skill/architecture-buddy/README.md`

**Interfaces:**
- Consumes: ADR-0019；`templates/architecture-deliverable.md`；`references/deliverable-gate.md`
- Produces: Agent 可读的 draft/deliverable 行为规范；检查脚本关键词全部命中

- [ ] **Step 1: 更新 frontmatter description**

```yaml
---
name: architecture-buddy
description: >
  Architecture co-thinking partner. In draft mode, explores assumptions with the user.
  When asked for a full architecture design, switches to deliverable mode: first-principles
  (assumptions → facts → rebuild), dual-layer note (narrative + mechanism/strategy), and a
  completion gate before claiming done. Use for architecture design, ADRs, system reviews.
metadata:
  display-name: Architecture Buddy
  version: "0.3.0"
---
```

- [ ] **Step 2: 重写正文必备章节（按此顺序）**

1. 身份（同事；不拍板；不考用户）  
2. 用户体验铁律（保留 ADR-0018 六条精神）  
3. **模式：`draft` / `deliverable`**（进入条件、可升级）  
4. 第一性原理三步（保留；禁止三列表伪装）  
5. **`deliverable` 主线 S0–S7**（每阶段一句话目的 + 完成条件；少提内部编号给用户）  
6. **双层成品**：权威模板路径；交卷前读 `deliverable-gate.md`  
7. 参考文件表（加入 deliverable 模板、gate、mapping；注明 note 已降级）  
8. Top N / 金标对照（可选，先问；对照只抽机制/策略教训）  
9. 圆桌（保留动态选席契约）  
10. 红线：含「不对用户开考/盲写/打分」；「未过完成门禁不得宣称完成」  
11. 自检清单（每轮 UX + deliverable 时额外勾 S6）  

写给用户看的句子用「完成检查 / 对照成熟系统」，**不要**用「开考、及格」。

- [ ] **Step 3: 跑静态检查至 OK**

```bash
bash scripts/check-architecture-buddy.sh
```

Expected: `OK: architecture-buddy static checks passed`（及透镜 OK）

- [ ] **Step 4: 更新包 README**

`skill/architecture-buddy/README.md` 用短文说明：

- draft vs deliverable  
- 成品是双层模板  
- 安装仍链到 `~/.cursor/skills/`（若 README 已有安装步骤则保留）  

- [ ] **Step 5: 暂存说明**

```bash
git add skill/architecture-buddy/SKILL.md skill/architecture-buddy/README.md
```

Suggested message: `feat(architecture-buddy): deliverable 工作流 v0.3`

---

### Task 4: 验收清单 + 构建期校准骨架 + corpus 占位

**Files:**
- Modify: `docs/design/acceptance-checklist.md`
- Create: `docs/build/skill-calibration.md`
- Create: `corpus/README.md`

**Interfaces:**
- Consumes: 规格 §6–§7；ADR-0019
- Produces: V7 人工场景；维护者校准入口（无 GOLDEN 正文）

- [ ] **Step 1: 重写/增补验收清单**

保留 V2–V6 有用部分，修正过时条目，新增 V7：

```markdown
# Architecture Buddy 验收清单

V6 由 `scripts/check-architecture-buddy.sh` 自动检查。

## V1 draft 共思（不交完整设计）
- [ ] 识别为 draft（或未要求完整设计）
- [ ] 真第一性原理：假设 → 事实 → 重推（非结果/约束/优化三表）
- [ ] 不逼用户填不会的分类
- [ ] 不跑 S6，不宣称「架构设计已完成」

## V2 已有方案审阅
- [ ] 审视假设/风险/可替换策略
- [ ] 不擅自定案

## V3 拒绝 Top N
- [ ] 用户拒绝对照后仍能完成 deliverable（B5 写「未对照」）

## V4 圆桌 + 透镜
前置：安装任一 `architecture-buddy-lens-*`
- [ ] 硬分叉时先提议
- [ ] 透镜输出符合契约
- [ ] 用户选择；合成说明冲突

## V5 无透镜降级
- [ ] 未装透镜时词表对照，不假装名人到场

## V6 静态
- [ ] `bash scripts/check-architecture-buddy.sh` → OK

## V7 deliverable 完整交卷（人工）
- [ ] 用户说「做一份架构设计」→ 进入 deliverable
- [ ] 产出单一文件，含层 A（A1–A8）与层 B（B1–B5）
- [ ] 交卷前显式过完成门禁（或列出阻塞/待验证）
- [ ] 正文无 M1–M9 问卷结构；陌生人能讲清解决什么与主路径
- [ ] 全程无「开考/打分/及格」话术
```

- [ ] **Step 2: 写 `docs/build/skill-calibration.md`**

说明这是**维护者文档**：复现校准 / 迁移校准步骤、PASS 标准、结果写入 `corpus/runs/`；明确「不对用户暴露考试 UX」。Phase 1 再填 Kafka/git/k8s 金标。列出种子 id：`kafka`、`git`、`kubernetes`。

- [ ] **Step 3: 写 `corpus/README.md`**

```markdown
# Architecture corpus

金标与校准运行记录。布局见规格 §6。

- `golden/<id>/` — META、GOLDEN、RUBRIC、SOURCES（Phase 1+）
- `runs/` — 校准运行记录（不冒充金标）

种子（Phase 1）：kafka、git、kubernetes。

survey 摘记在 `docs/survey/architecture/`，升格后才成为 GOLDEN。
```

可选：`mkdir -p corpus/runs corpus/golden` 并放 `.gitkeep`。

- [ ] **Step 4: 跑静态检查**

```bash
bash scripts/check-architecture-buddy.sh
```

Expected: OK

- [ ] **Step 5: 暂存说明**

```bash
git add docs/design/acceptance-checklist.md \
  docs/build/skill-calibration.md \
  corpus/README.md
# 若有 gitkeep：
git add corpus/runs/.gitkeep corpus/golden/.gitkeep 2>/dev/null || true
```

Suggested message: `docs: deliverable 验收 V7 与校准/corpus 占位`

---

### Task 5: 端到端人工冒烟（本会话执行）

**Files:**
- 不改产品代码；可在 `/tmp` 或 `corpus/runs/` 写一份冒烟产出（若写 `corpus/runs/`，注明 `smoke-sre-buddy`，非正式校准）

**Interfaces:**
- Consumes: 安装后的 `architecture-buddy` v0.3 行为
- Produces: 一份双层草稿，证明门禁可执行

- [ ] **Step 1: 确认 skills 链接**

```bash
ls -la ~/.cursor/skills/architecture-buddy
bash /Users/apple/Desktop/skill-create/scripts/check-architecture-buddy.sh
```

若链接指向旧路径，重新 `ln -sfn` 到 `skill/architecture-buddy`。

- [ ] **Step 2: 按 V7 对 SRE-Buddy 做一次 deliverable 冒烟**

只读 `/Users/apple/Desktop/xe6/project/SRE-Buddy`（或用户指定路径），按新 SKILL 产出双层架构设计到：

`corpus/runs/2026-08-05-smoke-sre-buddy.md`

要求：封面 + A1–A8 + B1–B5；文末附「完成门禁自检」勾选结果；禁止 M 问卷结构与考试话术。

- [ ] **Step 3: 对照 V7 清单人工打勾**

在 `docs/design/acceptance-checklist.md` 的 V7 下用评论或单独 `corpus/runs/...` 文末记录哪些通过；未通过则回到 Task 3 补 SKILL，再冒烟一次。

- [ ] **Step 4: 向用户汇报**

说明：Phase 0 完成项、冒烟文件路径、已知缺口；询问是否授权 commit、是否开 Phase 1 金标计划。

---

## Spec coverage（自检）

| 规格要点 | 任务 |
|----------|------|
| draft/deliverable + S0–S7 | Task 3 |
| 双层 A1–A8 / B1–B5 | Task 2–3 |
| S6 完成门禁 | Task 2–3 |
| M 降级 | Task 2–3 |
| 考试不对用户 | Task 1 ADR、Task 3 红线、Task 4 校准文 |
| 静态检查扩展 | Task 2–3 |
| 验收 V7 | Task 4 |
| corpus / 校准入口 | Task 4（无 GOLDEN 正文） |
| 种子金标三题 PASS | **不在本计划**（Phase 1） |
| 透镜蒸馏 | **不在本计划**（Phase 2） |

## Placeholder scan

无 TBD；Commit 统一为「等用户授权」。
