# Architecture Quality Report

| Field | Value |
|------|------|
| candidate | `corpus/runs/2026-08-05-cal-agent-runtime.md` |
| hard_gate | **PASS** |
| structure_score | 20/20 |
| semantic_quality_score | **95 / 100** |
| domain_score | **100 / 100** |
| roundtable_score | **0 / 20** (no process record) |
| human_review | **PASS with process gap** |

## Automated Signals

- flag: none
- roundtable_signal: none-detected

## Manual Semantic Score

自动信号只用于发现遗漏或结构性伪装；维护者必须阅读正文后填写 0–4，不能按关键词计分。

| Dimension | Score (0–4) | Evidence / counterexample |
|-----------|-------------|---------------------------|
| 问题类与边界 | **4 / 4** | 工具循环、环境边界、非目标和信任边界明确 |
| 机制与策略分离 | **4 / 4** | loop、ACI、权限、HITL、tracing 与复杂度阶梯分离 |
| 失败、安全与恢复 | **4 / 4** | 工具失败、护栏、人审、checkpoint 和身份边界具体 |
| 演进、N+1 与反例 | **4 / 4** | 有复杂度阶梯、演进切片、when/when not 和反例 |
| 证据、决策理由与质量属性 | **3 / 4** | 机制依据和验收充分，组织级阈值/成本仍待验证 |

## Manual Roundtable Review

- 高影响互斥分叉是否被识别并主动提议：**FAIL**（未记录）
- 用户同意或跳过是否记录：**N/A**
- 席位与透镜契约是否匹配：**N/A**
- 主持人综合结论是否保留冲突、边界、代价：**N/A**

## Reviewer Conclusion

- 语义总分：**95 / 100**
- 领域分：**100 / 100**
- 圆桌分：**0 / 20**
- 结论：**RETRY**
- 反关键词命中复核：**通过**
- 备注：正文可作为高质量架构设计，但 agent/workflow、HITL 和运行时厚度都有高影响分叉，baseline 未记录圆桌提议。
