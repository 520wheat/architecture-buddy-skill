# Corpus P4 — EIP 路由与管理加深
- 阶段: Phase 4 · 2026-08-05
- 配套: `P4-eip-core.md`
- 来源: https://www.enterpriseintegrationpatterns.com/

## 路由五模式（问题 → 解 → 代价 → Buddy 问句）

| 模式 | 问题 | 解要旨 | 关键代价 | Buddy 问句 |
|------|------|--------|----------|------------|
| **Content-Based Router** | 同一逻辑功能落到多个物理系统 | 按消息内容选通道 | 路由器成变更热点；规则需可维护（可升规则引擎） | 路由规则谁拥有？变化频率？ |
| **Message Filter** | 只需部分消息 | 条件丢弃/放行 | 静默丢弃需可观测 | 过滤在生产者还是中间？ |
| **Splitter** | 组合消息需分片处理 | 拆成子消息 | 需关联与聚合策略 | 如何保证部分失败语义？ |
| **Aggregator** | 相关消息需合成 | 按关联集齐再发 | 状态、超时、乱序 | 超时与不完整集怎么处理？ |
| **Resequencer** | 乱序到达需还原序 | 缓冲重排 | 缓冲与延迟 | 顺序是业务硬约束吗？ |

相关：Scatter-Gather、Routing Slip、Process Manager——流程更重时再用；先问是否真需要编排中心（对照 DT 反过度中间件）。

## System Management（组级）

| 关注 | 模式族直觉 | Buddy 钩子 |
|------|------------|------------|
| 可见性 | Wire Tap / Message History / Message Store | 集成系统如何审计与排障？ |
| 控制 | Control Bus | 运行时调参/启停通道？ |
| 失败 | Dead Letter Channel / Invalid Channel | 毒消息与暂时失败分流 |

## 与 D4 交叉（更新）
- Kafka：分区键 ≈ 有序子流；consumer group ≈ Competing Consumers；应用侧常实现 Content-Based Router
- Pulsar：多租户/订阅模型使 Pub-Sub 与点对点策略更显式
- **不要**把 EIP 目录当成「必须上 ESB」的许可证

## 对活表
- M5 集成策略表优先用上表五名 + Dead Letter + Competing Consumers
- M7：路由器维护热点、聚合超时 = 常见风险条目
