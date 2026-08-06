# SkillOpt Phase 1B 质量训练记录：Architecture Buddy 0.3.4

## 运行信息

- Skill：`skill/architecture-buddy/SKILL.md`
- 版本：`0.3.4`
- SkillOpt：微软 `SkillOpt`
- SkillOpt commit：`8a4c96a23639eee6ce19de7579ac9006b6dd4a2a`
- 任务集：`2026-08-05-skillopt-architecture-tasks-v3.json`
- backend：Codex
- staging：`.skillopt-sleep/staging/20260805-224117/`
- `auto_adopt`：`false`

本轮使用真实 Codex backend 生成并记录训练证据；最终 SkillOpt report 的 replay 标记为 `mock`、`n_sessions=0`，因此这里的 held-out 结果是对已记录输出的 replay/gate 结果，不宣称是六次全新的 live 会话。

## 结果

| 指标 | 结果 |
|------|------|
| 任务数 | 6 |
| baseline held-out | `0.4330357143` |
| candidate held-out | `1.0000000000` |
| 绝对提升 | `+0.5669642857` |
| gate | `accept_new_best` |
| 接受候选编辑 | 6 |
| 自动采用 | 否 |
| tokens | `32705` |

候选达到显著提升，但该分数主要验证结构与规则 judge，不能单独证明架构设计在技术正确性、证据质量或取舍深度上优秀。

## SkillOpt 候选

Skill 规则候选：

1. `deliverable` 输出使用明确的 `A1`、`A8`、`B1`、`B6` Markdown 标题。
2. 选择主策略前明确写出“高影响互斥分叉”并提议圆桌；同意后最多三席，席位契约包含 `### Risks / what they'd worry about`。
3. 用户拒绝圆桌时记录“已提议圆桌，用户选择跳过圆桌”，随后继续使用“策略/反模式词表”做轻量对照，不伪造透镜。

Memory 候选还补充了正式架构双层范围、圆桌同意/跳过证据和无匹配透镜降级规则。

所有候选均保留在 staging；没有执行 adopt，没有覆盖源码或安装目录。

## 质量解读

本轮暴露的残余问题：

- 结构 judge 仍可能把真实存在的 `### A1` 等标题判为缺失，说明结构评分器需要继续校准。
- 某些训练样本以关键词检查“取舍”“停止复制”“用户同意”等行为，存在关键词命中替代语义质量的风险。
- 当前候选没有证明 Git、Kafka、etcd 等真实系统的技术准确性；仍需人工审阅和 held-out 反例测试。

因此本轮结论是：

- **结构/规则可测分数：显著提升，candidate 通过 gate。**
- **语义架构质量：不能仅凭 `1.0` 判定优秀，需结合 Phase 1B 五维人工审阅。**
- **采用决策：暂不 adopt。**

## 产物

- `report.md`
- `report.json`
- `diagnostics.json`
- `evidence.jsonl`
- `proposed_SKILL.md`

均位于 `.skillopt-sleep/staging/20260805-224117/`。
