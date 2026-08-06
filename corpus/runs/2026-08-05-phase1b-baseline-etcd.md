# Architecture Quality Report

| Field | Value |
|------|------|
| candidate | `corpus/runs/2026-08-05-cal-etcd.md` |
| hard_gate | **REJECT** |
| structure_score | 0/20 |
| semantic_quality_score | **95 / 100** |
| domain_score | **100 / 100** |
| roundtable_score | **0 / 20** (no process record) |
| human_review | **PASS with gate failure** |

## Automated Signals

- flag: structure-incomplete
- flag: b6-evidence-insufficient
- missing_sections: B6
- b6_missing_evidence: 变化轴 N+1 反例 可组合能力 复杂度
- roundtable_signal: none-detected

## Manual Semantic Score

自动信号只用于发现遗漏或结构性伪装；维护者必须阅读正文后填写 0–4，不能按关键词计分。

| Dimension | Score (0–4) | Evidence / counterexample |
|-----------|-------------|---------------------------|
| 问题类与边界 | **4 / 4** | CP 元数据协调边界、非目标和信任边界清楚 |
| 机制与策略分离 | **4 / 4** | Raft/MVCC/Watch/Lease 与 AP、ZK、NewSQL 分叉分开 |
| 失败、安全与恢复 | **4 / 4** | 多数不可用、超时消歧、compaction 和 fencing 有恢复语义 |
| 演进、N+1 与反例 | **3 / 4** | 有演进和反例，但旧候选缺 B6 的组合增长证据 |
| 证据、决策理由与质量属性 | **4 / 4** | 线性化、Watch 差异、Lease 窗口与验收均有依据 |

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
- 备注：领域内容优秀，但 B6 缺失触发硬门禁；先补组合边界，再判断是否达到优秀。
