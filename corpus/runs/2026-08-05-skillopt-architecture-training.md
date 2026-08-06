# SkillOpt 训练记录：Architecture Buddy 0.3.3

## 训练对象

- Skill：`skill/architecture-buddy/SKILL.md`
- 版本：`0.3.3`
- SkillOpt：微软 `SkillOpt`，仓库 `https://github.com/microsoft/SkillOpt`
- SkillOpt commit：`8a4c96a23639eee6ce19de7579ac9006b6dd4a2a`
- 运行方式：`SkillOpt-Sleep` + Codex backend
- 目标：优化正式架构设计、圆桌主持和圆桌记录与正式文档分离的行为

## 任务集

任务集：[2026-08-05-skillopt-architecture-tasks.json](2026-08-05-skillopt-architecture-tasks.json)

共 4 个经过审查的任务：

1. Git 正式架构设计
2. 架构圆桌预检、用户同意、透镜契约和综合结论
3. 圆桌记录与正式架构设计分离
4. 架构设计质量评价

任务拆分为 2 个 train、1 个 val、1 个 test，使用规则 judge 检查章节、边界、失败语义和圆桌/正式文档分离要求。

## 结果

| 指标 | 结果 |
|------|------|
| 任务数 | 4 |
| replay 数 | 4 |
| baseline 验证分数 | 0.400 |
| candidate 验证分数 | 1.000 |
| gate | `accept_new_best` |
| Skill 正文接受编辑 | 0 |
| Skill 正文拒绝编辑 | 3 |
| Memory 接受编辑 | 2 |
| token 使用量 | 14,738 |
| 自动采用 | 否 |

## 采用决策

SkillOpt 提议的 3 条 Skill 正文编辑均与现有规则重复，被 gate 拒绝；这说明本轮没有必要直接改写 `SKILL.md`。

验证通过的 2 条记忆层规则是：

- 正式架构设计正文使用 `摘要`、`上下文与边界`、`组件与契约`、`失败`、`安全`、`验收` 等结构，并与圆桌过程分离。
- 圆桌记录明确包含圆桌、用户同意和透镜契约，同时保留预检、双层交付、N+1 与反例要求。

这两条规则只生成在 staging 中，未写入当前 Skill 或项目配置。原始 staging：
`/tmp/architecture-buddy-skillopt-codex.uPswif/project/.skillopt-sleep/staging/20260805-182800/`

## 框架验证

SkillOpt 官方 deterministic experiment 同时通过：

- baseline held-out：`0.3333`
- after held-out：`1.0`
- gate 能阻止有害编辑：`True`

训练环境使用 Python `3.12.13`；系统默认 Python `3.9.6` 不满足 SkillOpt `3.10+` 要求，因此训练使用隔离虚拟环境，未修改项目依赖。
