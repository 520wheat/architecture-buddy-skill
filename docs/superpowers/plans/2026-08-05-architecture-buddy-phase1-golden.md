# Architecture Buddy Phase 1 Golden Corpus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sp-subagent-driven-development (recommended) or sp-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立三种子金标（kafka / git / kubernetes）的双层 GOLDEN + RUBRIC，并各完成一次维护者复现校准 PASS，证明 skill 能写出接近正典质量的架构设计。

**Architecture:** 从 `docs/survey/architecture/` 摘记升格为 `corpus/golden/<id>/{META,GOLDEN,RUBRIC,SOURCES}.md`；GOLDEN 严格按 `architecture-deliverable.md` 双层骨架；校准运行写入 `corpus/runs/`（标明 calibration，不冒充金标）。失败则改 skill/模板再跑，不改用户考试 UX。

**Tech Stack:** Markdown corpus；Architecture Buddy skill v0.3；Bash 可选结构检查；无运行时依赖。

## Global Constraints

- 工作区：`/Users/apple/Desktop/skill-create`；分支沿用 `feat/deliverable-workflow`（或当前功能分支）
- 规格：`docs/superpowers/specs/2026-08-05-architecture-buddy-deliverable-workflow-design.md` §6–§7 Phase 1
- 校准文档：`docs/build/skill-calibration.md`
- GOLDEN 必须含层 A（A1–A8）与层 B（B1–B5）；无 M1–M9 问卷结构
- 考试仅维护者；用户 UX 不变
- survey 摘记是原料不是金标；引用公开 URL 写入 SOURCES/META
- **未经用户明确要求不得 git commit**；Commit 步改为暂存说明
- 不运行时调用女娲

## File map

| 路径 | 职责 |
|------|------|
| `corpus/golden/_template/` | 可选：四文件空壳说明（可跳过，直接写三题） |
| `corpus/golden/kafka/{META,GOLDEN,RUBRIC,SOURCES}.md` | Kafka 金标套件 |
| `corpus/golden/git/{META,GOLDEN,RUBRIC,SOURCES}.md` | git 金标套件 |
| `corpus/golden/kubernetes/{META,GOLDEN,RUBRIC,SOURCES}.md` | K8s 金标套件 |
| `corpus/runs/2026-08-05-cal-kafka.md` 等 | 校准候选 + 对照结论 |
| `scripts/check-architecture-buddy.sh` | 增补：三金标目录四文件存在 + GOLDEN 含 A1/B1 |
| `docs/build/skill-calibration.md` | Phase 状态改为 Phase 1 进行中/完成 |
| `corpus/README.md` | 注明种子已填充 |

原料：
- `docs/survey/architecture/D4-kafka.md` + https://kafka.apache.org/documentation/#design
- `docs/survey/architecture/D5-git.md` + https://aosabook.org/en/v2/git.html
- `docs/survey/architecture/D2-kubernetes.md` + https://kubernetes.io/docs/concepts/architecture/

---

### Task 1: 静态检查扩展 + Kafka 金标套件

**Files:**
- Modify: `scripts/check-architecture-buddy.sh`
- Create: `corpus/golden/kafka/META.md`, `GOLDEN.md`, `RUBRIC.md`, `SOURCES.md`

**Interfaces:**
- Consumes: deliverable 模板；D4-kafka survey
- Produces: 可被校准对照的 kafka 金标；检查脚本要求 `corpus/golden/{kafka,git,kubernetes}/{META,GOLDEN,RUBRIC,SOURCES}.md` 与 GOLDEN 含 `### A1` / `### B1`

- [ ] **Step 1: 扩展检查脚本（预期先 FAIL）**

在脚本末尾（lens 检查前后均可）增加：

```bash
for id in kafka git kubernetes; do
  for f in META.md GOLDEN.md RUBRIC.md SOURCES.md; do
    [[ -f "$ROOT/corpus/golden/$id/$f" ]] || fail "missing corpus/golden/$id/$f"
  done
  grep -q '### A1' "$ROOT/corpus/golden/$id/GOLDEN.md" || fail "$id GOLDEN missing ### A1"
  grep -q '### B1' "$ROOT/corpus/golden/$id/GOLDEN.md" || fail "$id GOLDEN missing ### B1"
  grep -q '必中' "$ROOT/corpus/golden/$id/RUBRIC.md" || fail "$id RUBRIC missing 必中"
done
```

- [ ] **Step 2: 跑检查确认 FAIL**

```bash
bash scripts/check-architecture-buddy.sh
```

Expected: missing corpus/golden/...

- [ ] **Step 3: 写 kafka 四文件**

`META.md`：问题类一句话、域 D4、来源 URL、许可说明（引用官方文档/公开设计）。

`SOURCES.md`：至少官方 design 文档 + 本地 survey 路径。

`GOLDEN.md`：完整双层（封面 + A1–A8 + B1–B5）。内容必须覆盖 survey 中的核心机制（持久化追加日志、分区、pull/consumer group、pagecache 等）与策略表；叙事层写清生产者→分区 leader→日志→consumer pull 主路径；B5 可写「金标本体系」。

`RUBRIC.md` 结构：

```markdown
# RUBRIC — kafka

## 必中机制（≥5）
- …

## 必中策略分叉（≥3）
- …

## 叙事完整性
- 层 A/B 齐全；主路径可走通

## 幻觉黑名单（出现则 FAIL）
- 把 Kafka 写成「必须 broker push」
- 声称消息消费后必须从日志删除
- …
```

- [ ] **Step 4: 再跑检查**

仍可能因 git/kubernetes 缺失 FAIL——记下。Kafka 相关 FAIL 必须消失。

- [ ] **Step 5: 暂存说明（不 commit）**

---

### Task 2: git 金标套件

**Files:**
- Create: `corpus/golden/git/{META,GOLDEN,RUBRIC,SOURCES}.md`

**Interfaces:**
- Consumes: D5-git；AOSA Git 章要点
- Produces: git 金标；检查对 git 路径转绿

- [ ] **Step 1: 写四文件**

GOLDEN 必盖：内容寻址对象库、DAG 历史、refs/轻量分支、本地提交与推送解耦、plumbing/porcelain；策略对照 snapshot vs delta、分布式 vs 中央。主路径可用「一次 commit → 对象入库 → 更新 ref」。

RUBRIC：必中机制 ≥5；黑名单含「Git 必须中央服务器才能提交」类幻觉。

- [ ] **Step 2: 跑检查**；git 相关 FAIL 消失

- [ ] **Step 3: 暂存说明**

---

### Task 3: kubernetes 金标套件

**Files:**
- Create: `corpus/golden/kubernetes/{META,GOLDEN,RUBRIC,SOURCES}.md`

**Interfaces:**
- Consumes: D2-kubernetes
- Produces: 三金标目录齐；`check-architecture-buddy.sh` → 全绿

- [ ] **Step 1: 写四文件**

GOLDEN 必盖：控制面/节点分离、声明式 API、controller reconcile、etcd 真相源、API Server 前门、可插拔 CRI/CNI；策略含控制面部署变体。主路径：「kubectl apply → API Server → etcd → controller watch → 节点执行」。

RUBRIC：黑名单含「kubelet 绕过 API 改 etcd 为正规扩展路径」等。

- [ ] **Step 2: 跑检查至 OK**

```bash
bash scripts/check-architecture-buddy.sh
```

Expected: OK（含三金标）

- [ ] **Step 3: 暂存说明**

---

### Task 4: 三题复现校准（维护者）

**Files:**
- Create: `corpus/runs/2026-08-05-cal-kafka.md`
- Create: `corpus/runs/2026-08-05-cal-git.md`
- Create: `corpus/runs/2026-08-05-cal-kubernetes.md`
- Modify（若校准暴露缺口）: `skill/architecture-buddy/**` 最小修补

**Interfaces:**
- Consumes: 三套 GOLDEN+RUBRIC；skill v0.3 deliverable 流程
- Produces: 三份校准记录，各含判定 PASS 或 RETRY+修补后再 PASS

对每个 id（kafka → git → kubernetes）：

- [ ] **Step A: 盲写候选**

按 deliverable 模式，主要依据 `SOURCES.md` + 公开知识与 survey，**不要整段复制 GOLDEN**。产出写入对应 `corpus/runs/2026-08-05-cal-<id>.md` 的上半部分（完整双层）。封面标明 `calibration reproduce` / 非正式金标。

- [ ] **Step B: 对照打分**

在同一文件下半部分写：

```markdown
## 校准对照
- 日期 / skill 版本
- 必中机制命中表（命中/未命中）
- 必中策略命中表
- 幻觉黑名单检查
- S6 结构
- 判定：PASS | RETRY
- 若 RETRY：缺口列表与对 skill/模板的改动（改完重跑，追加第二轮）
```

- [ ] **Step C: 达标门禁**

三题均须最终 **PASS**。若某题 RETRY，允许最小改 skill/references（禁止引入用户考试 UX），再追加一轮候选至 PASS。

- [ ] **Step D: 跑静态检查仍 OK**

- [ ] **Step E: 暂存说明**

---

### Task 5: 文档收尾

**Files:**
- Modify: `docs/build/skill-calibration.md`（Phase 状态表：Phase 1 完成；链到三 GOLDEN 与三 cal runs）
- Modify: `corpus/README.md`（种子已填充）
- Modify: `docs/design/acceptance-checklist.md`（可选 V8：三金标存在 + 三校准 PASS 记录存在）

- [ ] **Step 1: 更新校准文档 Phase 状态**

- [ ] **Step 2: 更新 corpus README**

- [ ] **Step 3: 增补 V8 验收项（人工勾选说明）**

```markdown
## V8 Phase 1 金标与校准（维护者）
- [ ] corpus/golden/{kafka,git,kubernetes} 四文件齐全
- [ ] 三份 cal runs 判定均为 PASS
- [ ] 用户侧 SKILL 仍无开考/打分话术
```

- [ ] **Step 4: 全量检查 OK；向用户汇报并提供提交指令**

---

## Spec coverage

| 要点 | 任务 |
|------|------|
| 三种子 GOLDEN+RUBRIC | 1–3 |
| 各至少一次维护者 PASS | 4 |
| 考试不对用户 | 全程；V8 |
| survey 升格非直接改名 | 1–3 重写双层 |
| 静态检查 | 1、3、4 |

## Placeholder scan

无 TBD；Commit 等用户授权。
