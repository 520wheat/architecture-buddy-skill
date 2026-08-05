# Architecture Buddy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sp-subagent-driven-development (recommended) or sp-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 交付可安装的主持 Skill `architecture-buddy`（显示名 Architecture Buddy），含 references/templates、圆桌主持与无透镜降级，并通过验收 V1–V6 的静态检查与人工场景清单。

**Architecture:** 形态 B——单一主持 `SKILL.md` 内化流程与第一性原理共抽启发式（P0 先写可运行的手写版；P2 再用女娲蒸馏替换/加厚）；透镜为独立 skill 包，运行时按需加载。调研全文留在 `docs/survey/`，打进包的是压缩 `references/`。

**Tech Stack:** Agent Skills（`SKILL.md` + YAML frontmatter）；Markdown references/templates；Bash 静态校验脚本；无运行时语言依赖、无 nuwa 运行时调用。

## Global Constraints

- 工作区根：`~/Desktop/skill-create`（ADR-0005）
- 安装目录名与 frontmatter `name`：**`architecture-buddy`**（Agent Skills：`^[a-z0-9]+(-[a-z0-9]+)*$`）；人类显示名：**Architecture Buddy**
- 禁止运行时依赖/调用女娲（nuwa-skill）；禁止硬编码密钥
- 不替用户拍板；Top N / 深调研 / 圆桌硬分叉均须先问再做
- GoF 默认细粒度；笔记主结构用 M1–M9
- 本仓库默认：**未经用户明确要求不得 `git commit`**；计划中的 Commit 步改为「暂存说明 + 等用户授权」除非用户已授权提交
- 规格权威：`docs/design/00-architecture-buddy-spec.md` + `docs/design/01`–`05` + `docs/adr/0001`–`0013`

## File map（将创建/修改）

| 路径 | 职责 |
|------|------|
| `docs/adr/0014-skill-package-dirname.md` | 锁定 `architecture-buddy` 目录名与显示名 |
| `docs/adr/0005-workspace-layout-and-naming.md` | 更新目录约定一行 |
| `architecture-buddy/SKILL.md` | 主持：身份、流程、FP、M1–M9、Top N、圆桌、红线 |
| `architecture-buddy/references/mechanisms.md` | M1–M9 + 关键 K 压缩 |
| `architecture-buddy/references/strategies-cheatsheet.md` | 域策略分叉 + 模式层级入口 |
| `architecture-buddy/references/anti-patterns.md` | 反模式与写作禁忌 + 运行时红线 |
| `architecture-buddy/templates/architecture-note.md` | 笔记空白骨架 |
| `architecture-buddy/templates/problem-class-template.md` | 类问题模板骨架 |
| `architecture-buddy-lens-scaffold/SKILL.md` | 可选：通用透镜脚手架（测 V4/契约） |
| `scripts/check-architecture-buddy.sh` | V6 静态校验 |
| `docs/design/acceptance-checklist.md` | V1–V5 人工场景清单 |

---

### Task 1: 目录命名 ADR + 包骨架 + 静态校验脚本

**Files:**
- Create: `docs/adr/0014-skill-package-dirname.md`
- Modify: `docs/adr/0005-workspace-layout-and-naming.md`
- Modify: `docs/adr/README.md`
- Create: `architecture-buddy/SKILL.md`（最小 frontmatter + stub body）
- Create: `architecture-buddy/references/.gitkeep`
- Create: `architecture-buddy/templates/.gitkeep`
- Create: `scripts/check-architecture-buddy.sh`
- Test: 运行该脚本

**Interfaces:**
- Consumes: Agent Skills frontmatter 规则；ADR-0005
- Produces: 可安装目录 `architecture-buddy/`；`name: architecture-buddy`；校验脚本退出码 0/1

- [ ] **Step 1: 写 ADR-0014**

写入 `docs/adr/0014-skill-package-dirname.md`：

```markdown
# ADR-0014: 安装目录名 architecture-buddy

## Status
Accepted

## Context
Agent Skills 要求 frontmatter `name` 为小写字母/数字/连字符，且与父目录名一致。
ADR-0005 使用显示名「Architecture Buddy」与空格目录，与协议冲突。

## Decision
- 安装路径与 `name`：`architecture-buddy`
- 显示名（SKILL.md 标题与文档）：Architecture Buddy
- 透镜包：`architecture-buddy-lens-<shortname>/`，`name: architecture-buddy-lens-<shortname>`

## Consequences
- 更新 ADR-0005 目录表；旧空目录 `Architecture Buddy/` 若存在则删除或改为 README 指针。
```

- [ ] **Step 2: 更新 ADR-0005 与 adr/README**

在 `0005` 的目录表中，将 `Architecture Buddy/` 改为 `architecture-buddy/`，并注明显示名。在 `docs/adr/README.md` 增加 0014 一行。

- [ ] **Step 3: 写失败用的校验脚本（先写期望）**

创建 `scripts/check-architecture-buddy.sh`：

```bash
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
```

- [ ] **Step 4: 运行脚本，确认当前失败**

Run: `bash scripts/check-architecture-buddy.sh`  
Expected: FAIL（缺文件或 name）

- [ ] **Step 5: 创建最小 SKILL.md stub + 空目录**

```markdown
---
name: architecture-buddy
description: Partner skill for problem-class architecture design—mechanism vs strategy, architecture notes (M1–M9), optional Top N survey and roundtable lenses. Use when designing or reviewing software architecture, comparing systems, or writing architecture ADRs/notes—not for module wiring diagrams as the main deliverable.
---

# Architecture Buddy

（stub — Task 4 填充完整正文）
```

若存在空目录 `Architecture Buddy/`，写入单行 `README.md`：「已迁移至 `../architecture-buddy/`」或删除空目录（优先删除空目录）。

- [ ] **Step 6: 暂不要求脚本全绿**

此时 references/templates 仍缺 → 脚本应仍 FAIL。确认失败原因是 missing references（预期）。完整变绿在 Task 3 之后。

- [ ] **Step 7: 停止点**

向用户报告 ADR-0014 与骨架已就绪；若用户要求则再 commit。

---

### Task 2: 压缩 references（自 living 活表）

**Files:**
- Create: `architecture-buddy/references/mechanisms.md`
- Create: `architecture-buddy/references/strategies-cheatsheet.md`
- Create: `architecture-buddy/references/anti-patterns.md`
- Source: `docs/survey/living/*.md`

**Interfaces:**
- Consumes: living v1.0+ 三表
- Produces: 三份短参考（各宜 < 120 行）；SKILL.md 将用相对路径 `references/...` 引用

- [ ] **Step 1: 写 `references/mechanisms.md`**

从 `docs/survey/living/mechanisms.md` 复制 M1–M9 映射表 + 精选 K 行（K1–K10、K13–K17、K20–K24），删除「已否决的膨胀」以外的冗长说明；文首加：

```markdown
# Mechanisms (runtime cheat sheet)
Source: docs/survey/living/mechanisms.md — compressed for skill runtime.
Use M1–M9 as architecture-note anchors. Do not invent new M numbers in-session.
```

- [ ] **Step 2: 写 `references/strategies-cheatsheet.md`**

从 `docs/survey/living/strategies-and-patterns.md` 取「按问题域」表 + 「模式 corpus 入口」表 + M5 列约定；文首注明 source。

- [ ] **Step 3: 写 `references/anti-patterns.md`**

从 `docs/survey/living/anti-patterns-and-writing-rules.md` 全文可接近原样压缩进包（该文件已短）；保留「Buddy 运行时红线」三节。

- [ ] **Step 4: 抽查**

Run: `wc -l architecture-buddy/references/*.md`  
Expected: 每个文件非空；合计不宜超过 ~400 行（软上限，超则再压）。

---

### Task 3: templates + 让校验脚本第一次接近全绿

**Files:**
- Create: `architecture-buddy/templates/architecture-note.md`
- Create: `architecture-buddy/templates/problem-class-template.md`
- Delete: `architecture-buddy/references/.gitkeep`, `templates/.gitkeep`（若存在）

**Interfaces:**
- Consumes: `docs/design/03-notes-and-templates.md` 骨架
- Produces: 两份可直接填空的模板

- [ ] **Step 1: 写 `templates/architecture-note.md`**

使用 §3 中「架构笔记」完整 markdown 骨架（M1–M9 + 附录标题），标题改为：

```markdown
# 架构笔记：<问题类一句话>
```

各节保留提示 bullet，勿删 M 编号。

- [ ] **Step 2: 写 `templates/problem-class-template.md`**

使用 §3「类问题模板」各节标题列表，每节下留 1–2 行占位说明。

- [ ] **Step 3: 运行校验（仍可能因 SKILL 正文缺 M1/Top N 失败）**

Run: `bash scripts/check-architecture-buddy.sh`  
若仅因 stub 缺关键字失败 → 进入 Task 4；若缺文件失败 → 修文件。

---

### Task 4: 主持 SKILL.md 完整正文（P0）

**Files:**
- Modify: `architecture-buddy/SKILL.md`（整文件替换 stub）

**Interfaces:**
- Consumes: spec §1–§5、§2 流程、references、templates
- Produces: 仅装此包即可跑 V1–V3、V5（无透镜降级的词表路径）、V6

- [ ] **Step 1: 写入完整 SKILL.md**

文件必须包含以下章节（可按此结构粘贴后润色，但不得删减行为约束）：

```markdown
---
name: architecture-buddy
description: Partner skill for problem-class architecture design—mechanism vs strategy, architecture notes (M1–M9), optional Top N survey and roundtable lenses. Use when designing or reviewing software architecture, comparing systems, or writing architecture ADRs/notes—not for module wiring diagrams as the main deliverable.
metadata:
  display-name: Architecture Buddy
  version: "0.1.0"
---

# Architecture Buddy

你是架构共思**伙伴**（同事），不是领导、不是替身名人、不替用户做最终架构决策。

## 何时使用 / 非目标
- 用：问题类界定、机制 vs 策略、架构笔记/ADR、Top N 对照、多视角圆桌
- 不用：以模块拆分图为主交付；运行时调用女娲；宣布「就这么定了」

## 参考与模板
- 机制锚点：`references/mechanisms.md`
- 策略速查：`references/strategies-cheatsheet.md`
- 反模式/红线：`references/anti-patterns.md`
- 笔记骨架：`templates/architecture-note.md`
- 类问题模板：`templates/problem-class-template.md`

## 入口 A / B / C
| 模式 | 信号 | 前半段重心 |
|------|------|------------|
| A | 模糊真实问题 | 多澄清 |
| B | 已有方案 | 多审视假设/风险/可替换策略 |
| C | 调研/抽象意图 | 较早进入问题类与对照 |

识别后用一句话确认：「我按 B（已有方案审视）来走，可以吗？」

## 主流程
1. 识别并确认 A/B/C
2. 第一性原理共抽核心问题（见下节）
3. 界定问题类（一句话）
4. **询问**是否 Top N（同意才做；约定 N/范围/时间盒）
5. 可选圆桌（见「圆桌」；硬分叉先提议）
6. 共写架构笔记（M1–M9；模板路径如上）
7. 机制稳定时**提议**沉淀类问题模板（用户决定）

## 第一性原理共抽（手写版；构建期可被女娲蒸馏加厚）
与用户一起压到三条，未清则继续问：
1. 真正要达成的结果（不是功能清单）
2. 硬约束（法规、成本、时延、团队能力等不可违背项）
3. 真正要优化的变量——以及明确**不**优化什么

禁止跳过澄清直接甩完整架构。

## 笔记锚点 M1–M9
按 `templates/architecture-note.md` 共写。对话中在分叉处点名锚点（如「这是 M3 信任假设」）。不必机械 1→9 填空，但交付笔记应能映射到 M1–M9。
模式命名遵循 M9：优先架构/企业/集成/并发分布式/Agent；GoF 默认细粒度附录。

## Top N 规则
主动问，例如：「这类问题已有被验证的产品。要不要做一轮 Top N 对照，抽机制（共性）和策略（差异）？」
- 不同意 → 用 `references/strategies-cheatsheet.md` 轻量对照或跳过
- 同意 → 再开跑；结果写入笔记 M5/M8

## 圆桌（P1 行为；无透镜可降级）
### 触发
- 用户明确要求多视角 → 启动
- **硬分叉**（机制已清、策略互斥、影响大）→ **先提议**，同意再请席
- 否则不开

### 规则
- 默认 2 席，上限 3；超过先收敛对照点
- 钉一句话对照点 → 请已安装的 `architecture-buddy-lens-*` → 要各透镜按契约输出 → 合成共识/冲突表 → 用户拍板
- 未安装透镜：列出已安装；用 strategies/anti-patterns 词表做「无透镜对照」，不假装请到名人

### 透镜输出契约（要求透镜 skill 遵守）
## Lens: <短名>
### On the decision point
### Heuristics applied
### Risks / what they'd worry about
### Would not do
### Evidence style

## 提议组件前的强制问句
在建议 Agent 编排、公司级消息总线、或共识组件之前，先问：「更简单的方案是否已经足够？」（见 anti-patterns 红线）

## 红线
- 不替用户选定唯一架构并宣布定案
- 不擅自 Top N / 深调研
- 不运行时调用女娲；不以「我就是某某」说话
- 模块/构建块图仅附录
```

- [ ] **Step 2: 运行静态校验**

Run: `bash scripts/check-architecture-buddy.sh`  
Expected: `OK: architecture-buddy static checks passed`

- [ ] **Step 3: 自检 description 长度**

Run: `python3 -c "import re; t=open('architecture-buddy/SKILL.md').read(); d=re.search(r'^description:\s*(.+)$',t,re.M).group(1); assert 1<=len(d)<=1024, len(d); print(len(d))"`  
Expected: 打印 ≤1024 的数字

---

### Task 5: 验收清单文档（V1–V5）+ 脚手架透镜（V4）

**Files:**
- Create: `docs/design/acceptance-checklist.md`
- Create: `architecture-buddy-lens-scaffold/SKILL.md`

**Interfaces:**
- Consumes: Task 4 行为；§4 契约
- Produces: 人工验收清单；一个通用透镜包（标签 scaffold，非名人）供本地测圆桌

- [ ] **Step 1: 写 acceptance-checklist.md**

```markdown
# Architecture Buddy 验收清单

对照 spec §9。V6 由 `scripts/check-architecture-buddy.sh` 自动检查。

## V1 模式 A（只装主持）
- [ ] 识别为 A 并确认
- [ ] 共抽结果/约束/优化变量
- [ ] 问 Top N
- [ ] 产出笔记可映射 M1–M9

## V2 模式 B
- [ ] 识别为 B
- [ ] 审视假设/风险/可替换策略
- [ ] 不擅自定案

## V3 拒绝 Top N
- [ ] 用户说不做 Top N 后仍能完成笔记

## V4 圆桌 + 透镜
前置：安装 `architecture-buddy-lens-scaffold`
- [ ] 硬分叉时先提议
- [ ] 两透镜输出符合契约
- [ ] 合成表含冲突；用户选择

## V5 无透镜降级
- [ ] 未装透镜时降级到词表对照，不假装名人到场

## V6 静态
- [ ] `bash scripts/check-architecture-buddy.sh` → OK
```

- [ ] **Step 2: 写脚手架透镜**

`architecture-buddy-lens-scaffold/SKILL.md`：

```markdown
---
name: architecture-buddy-lens-scaffold
description: Scaffold lens for Architecture Buddy roundtables. Applies generic trade-off heuristics (simplicity, operability, reversibility). Use only when Architecture Buddy hosts a roundtable and this lens is installed—not as a famous person.
metadata:
  display-name: Architecture Buddy Lens Scaffold
  version: "0.1.0"
---

# Architecture Buddy Lens — Scaffold

你是**启发式透镜**，不是某位真人。只回答主持给出的对照点。

## 输出格式（必须）
## Lens: Scaffold
### On the decision point
### Heuristics applied
### Risks / what they'd worry about
### Would not do
### Evidence style

## 启发式
- 优先可逆、可观测、可运维的选项
- 指出隐藏假设（一致性、信任、团队能力）
- 若有更简单方案，必须写入 Would not do 的对立面或 Risks
- 禁止「我就是某某」；禁止主持流程或擅自 Top N
```

- [ ] **Step 3: 扩展校验脚本覆盖透镜包 name**

在 `scripts/check-architecture-buddy.sh` 末尾（主包 OK 之后）追加可选检查：

```bash
LENS="$ROOT/architecture-buddy-lens-scaffold"
if [[ -d "$LENS" ]]; then
  grep -q '^name: architecture-buddy-lens-scaffold$' "$LENS/SKILL.md" || fail "lens name mismatch"
  grep -q 'On the decision point' "$LENS/SKILL.md" || fail "lens missing contract"
  echo "OK: lens-scaffold checks passed"
fi
```

- [ ] **Step 4: 再跑校验**

Run: `bash scripts/check-architecture-buddy.sh`  
Expected: 两行 OK

---

### Task 6: 规格与 README 对齐 + 实现完成声明

**Files:**
- Modify: `docs/README.md`（如需指向 plan/acceptance）
- Modify: `README.md`（工作区根，若存在）
- Modify: `docs/design/00-architecture-buddy-spec.md`（实现状态注记）
- Create: `architecture-buddy/README.md`（安装说明，可选短）

**Interfaces:**
- Consumes: 已完成包
- Produces: 新人能按 README 安装到 Cursor/Claude Code skills 目录

- [ ] **Step 1: 写 `architecture-buddy/README.md`**

```markdown
# Architecture Buddy

Install: copy or symlink this folder into your agent skills directory as `architecture-buddy`.

Optional lenses: install any `architecture-buddy-lens-*` beside it.

Verify: from repo root, `bash scripts/check-architecture-buddy.sh`
```

- [ ] **Step 2: 在汇总 spec 文末增加**

```markdown
## Implementation status
- P0/P1: see `architecture-buddy/` + `docs/design/acceptance-checklist.md`
- Plan: `docs/superpowers/plans/2026-08-05-architecture-buddy.md`
- P2（女娲蒸馏 FP/真人透镜）: 另开构建期 ADR 与任务，不阻塞 P0/P1
```

- [ ] **Step 3: 根 README 若存在则链到 design/00 与 architecture-buddy/**

- [ ] **Step 4: 最终校验**

Run: `bash scripts/check-architecture-buddy.sh`  
Expected: OK

- [ ] **Step 5: 人工走读 acceptance-checklist V1（最短路径）**

在 Cursor 中启用 skill，用一句模糊问题开场（例如「我们要把多区域配置同步做好」），确认会确认入口 A、澄清、问 Top N。将结果勾选清单。

- [ ] **Step 6: 停止；请用户授权后再 commit**

建议 commit message（用户授权后使用）：

```text
feat(architecture-buddy): 实现主持 Skill P0/P1 与静态验收

```

---

### Task 7: P2 门闩（不阻塞 P0 交付）— 构建期 ADR 草稿 only

**Files:**
- Create: `docs/adr/0015-build-time-nuwa-distillation.md`（Status: Proposed）

**Interfaces:**
- Consumes: ADR-0003、§5
- Produces: 构建期决策草稿（人名/语料未锁则保持 Proposed）

- [ ] **Step 1: 写 Proposed ADR-0015**

内容要点：
- 女娲仅 CI/本地构建脚本调用
- 输入：选定语料路径 + 活表
- 输出：覆盖/加厚 `architecture-buddy/SKILL.md` 中「第一性原理」节；生成 `architecture-buddy-lens-<name>/`
- 验收：蒸馏后仍通过 `check-architecture-buddy.sh`；透镜遵守契约；无运行时 nuwa 字符串（除「构建期」说明）
- 人名与语料：**待用户选定后 Accepted**

- [ ] **Step 2: 在 adr/README 登记 0015 Proposed**

- [ ] **Step 3: 不要在本计划内执行女娲蒸馏**（除非用户另开任务并选定人名）

---

## Plan self-review

| 检查 | 结果 |
|------|------|
| Spec §1–§7 覆盖 | Task 4–5 覆盖身份/流程/M/圆桌/包布局；Task 2–3 覆盖 references/templates |
| Spec §9 V1–V6 | V6=脚本；V1–V5=acceptance-checklist；V4 依赖 scaffold 透镜 |
| Spec §10 非目标 | 写入 SKILL 红线 |
| Spec §11 P2 | Task 7 仅 ADR，不阻塞 |
| Placeholder | 无 TBD；女娲人名有意留 Proposed |
| 命名一致性 | 全程 `architecture-buddy` / `architecture-buddy-lens-*` |
| 目录冲突 | Task 1 处理旧 `Architecture Buddy/` |

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-05-architecture-buddy.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — 每任务新开子代理，任务间审查，迭代快  
2. **Inline Execution** — 本会话按 `sp-executing-plans` 批次执行并设检查点  

Which approach?
