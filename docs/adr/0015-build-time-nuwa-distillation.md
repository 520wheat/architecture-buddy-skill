# ADR-0015: 构建期女娲蒸馏第一性原理与透镜包

## Status

Proposed

## Context

ADR-0003 已决定：女娲（nuwa-skill）**仅构建期**使用，运行时主持 Skill 与独立透镜 Skill 分离（形态 B）。Design §5 描述了构建期流水线轮廓，但未锁定：

- 蒸馏所用**人物/语料**路径
- 具体 **2–3 个透镜 shortname** 与对应语料
- 构建脚本或 CI 的调用入口

P0/P1 已交付可运行的手写版 `architecture-buddy/SKILL.md`（含「第一性原理共抽」节）与 `architecture-buddy-lens-scaffold/` 草稿透镜。P2 目标是在**不引入运行时 nuwa 依赖**的前提下，用女娲蒸馏加厚主持段并产出真人启发式透镜包。

本 ADR 为 P2 **门闩**：先固化构建期决策与验收标准；**人名与语料待用户选定后**方可将 Status 升为 Accepted 并执行蒸馏。

## Decision

### 调用边界

- 女娲**仅**由 CI 或本地构建脚本（如 `scripts/build-architecture-buddy.sh`，实现另任务）调用。
- 运行时 Skill 包内**不得**引用 nuwa-skill、不得调用女娲；允许保留「构建期可被女娲蒸馏加厚」类说明（与 `check-architecture-buddy.sh` V6 规则一致）。

### 输入

| 输入 | 说明 |
|------|------|
| 活表 | `docs/survey/living/*`（M1–M9、策略、反模式等权威压缩源） |
| 选定语料 | 用户确认的路径列表（人物著作摘录、调研笔记、公开 canon 对照等）；**本 ADR 不预锁名单** |
| 主持 Skill 基底 | 当前 `architecture-buddy/SKILL.md`（身份、流程 A/B/C、M1–M9、Top N、圆桌主持段保持不变） |
| 透镜契约 | Design §4 视角输出格式 + `architecture-buddy-lens-scaffold/SKILL.md` 作为结构模板 |

### 输出

| 产出 | 目标 |
|------|------|
| 主持 Skill | 覆盖或加厚 `architecture-buddy/SKILL.md` 中 **「第一性原理共抽」** 节；其余分区仅因 M/活表升版而做必要同步，不整体重写 |
| 透镜包 | 每个选定人物/视角生成独立目录 `architecture-buddy-lens-<shortname>/`（见 ADR-0014），含符合 §4 契约的 `SKILL.md` |
| 构建记录 | 脚本日志或 manifest 记录：语料路径、活表版本、生成时间（便于回归与 diff） |

建议首批 **2–3** 个透镜；超过 3 需与用户确认是否收敛对照点类型（Design §4）。

### 验收标准（蒸馏完成后）

1. `bash scripts/check-architecture-buddy.sh` 通过（含 V6：无运行时 nuwa 字符串、无密钥、无「我就是某某」）。
2. 每个 `architecture-buddy-lens-<shortname>/SKILL.md` 满足透镜静态检查：`name` 与目录一致；含 `On the decision point` 等 §4 契约小节。
3. 蒸馏后主持 Skill 仍能独立完成 P0/P1 场景（V1–V3、V5；V4 需安装对应透镜）。
4. 调研全文仍留 `docs/survey/`；打进包的是压缩 `references/`，不整本复制。

### 待用户选定后写入 Accepted 版

- [ ] 第一性原理语料路径（可多条）
- [ ] 透镜 shortname 列表（2–3）及各自语料路径
- [ ] 构建脚本路径与是否在 CI 中强制运行

**在本 ADR 为 Proposed 期间，不执行女娲蒸馏。**

## Consequences

- P0/P1 交付不被 P2 阻塞；手写版与 scaffold 透镜继续有效。
- Accepted 后，构建期变更主持「第一性原理」段与新增透镜包，需走本 ADR 记录的语料与 shortname，并 rerun 静态验收。
- 若未来需多派第一性原理切换，可再开 ADR 将 FP 拆为独立 Skill（ADR-0003 B → A 路径）。

## Related

- ADR-0003（运行时 vs 构建期边界）
- ADR-0014（`architecture-buddy` / `architecture-buddy-lens-<shortname>` 命名）
- Design §5（包布局与构建期流水线）
- Design §4（透镜输出契约）
