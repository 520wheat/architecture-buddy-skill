# Skill 校准（维护者 / 构建期）

**受众：维护者与构建流程。不对用户暴露。**

复现/迁移「考试」只用于训练与校准 `architecture-buddy`（模板、门禁、透镜启发式），**不是**用户产品功能。用户对话禁止开考、盲写、打分、及格/不及格话术（ADR-0019；规格 §6.1）。

金标正文与三题 PASS 属 **Phase 1**；本文锁定流程与目录约定，**不**内嵌 GOLDEN 全文。

## 目的

- 用金标 + RUBRIC 检验 skill 是否能产出可读双层 deliverable
- 失败时改 skill/模板后再跑，不为凑 PASS 改用户 UX
- 校准通过率是构建质量信号，不是面向终端用户的功能

## 布局

见规格 §6.2 与仓库 `corpus/README.md`：

| 路径 | 作用 |
|------|------|
| `corpus/golden/<id>/` | META、GOLDEN、RUBRIC、SOURCES（Phase 1+） |
| `corpus/runs/<date>-<id>.md` | 校准运行记录（不冒充金标） |
| `docs/survey/architecture/` | 调研摘记；升格后才成为 GOLDEN |

## 种子 id（Phase 1）

| id | 问题类（概要） | GOLDEN | 校准 run（PASS） |
|----|----------------|--------|------------------|
| `kafka` | 日志/流式集成 | [`corpus/golden/kafka/`](../../corpus/golden/kafka/) | [`corpus/runs/2026-08-05-cal-kafka.md`](../../corpus/runs/2026-08-05-cal-kafka.md) |
| `git` | 内容寻址 + 分布式协作史 | [`corpus/golden/git/`](../../corpus/golden/git/) | [`corpus/runs/2026-08-05-cal-git.md`](../../corpus/runs/2026-08-05-cal-git.md) |
| `kubernetes` | 声明式控制面 / 协调循环 | [`corpus/golden/kubernetes/`](../../corpus/golden/kubernetes/) | [`corpus/runs/2026-08-05-cal-kubernetes.md`](../../corpus/runs/2026-08-05-cal-kubernetes.md) |

Phase 1 三种子 GOLDEN + RUBRIC 已齐，且各有一次维护者复现校准 **PASS**。Hadoop、Spark 等属 Phase 2。

## 复现校准

1. 抽题（系统 id，如 `kafka`）
2. 用当前 skill 按 `deliverable` 产出候选（默认可读 SOURCES；严校可闭卷）
3. 对照 GOLDEN + RUBRIC：机制/策略命中、叙事完整性（层 A + 层 B）、幻觉黑名单
4. 判定 **PASS** / **RETRY**；失败则改 skill/模板再跑
5. 将过程与结论写入 `corpus/runs/<YYYY-MM-DD>-<id>.md`

### PASS 标准（复现）

- 候选满足层 A（A1–A8）与层 B（B1–B5），且过 S6 结构完整性
- RUBRIC 必中点命中；无 RUBRIC 黑名单幻觉
- 机制/策略与 GOLDEN 同问题类对齐（允许表述差异，不允许乱套类比）

## 迁移校准

用于目标尚无 GOLDEN、或本次校准故意封存金标时：

1. 完整 `deliverable` → 单一双层成品
2. 过 S6；维护者（或第二会话）做陌生读者约 5 分钟抽检
3. 可选：与最近邻金标对照，检查乱套类比
4. 记入 `corpus/runs/`（标明 migration，勿当 GOLDEN）

### PASS 标准（迁移）

- 双层齐全且过 S6
- 陌生读者能讲清：解决什么、边界、主路径
- 无明显把邻近系统叙事整段套用到本目标

## 与用户侧的边界

- 用户侧完成门禁只有 S6（结构完整性），无开考/打分
- S3 可选「对照成熟系统」共思时，只抽机制/策略教训进层 B，禁止整段抄金标叙事
- 运行时不调用女娲；金标/RUBRIC/survey 仅构建期蒸馏原料（ADR-0015/0016）

## Phase 状态

| Phase | 本文相关交付 |
|-------|----------------|
| 0 | 本文件 + `corpus/` 占位；无 GOLDEN 正文 |
| 1（完成） | 三种子 GOLDEN+RUBRIC；各至少一次维护者 PASS（见上表链接） |
| 2+ | 扩库、蒸馏、半自动对照报告 |
