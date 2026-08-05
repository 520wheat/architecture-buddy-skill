# Dependency-Track ADR 集（样本：丢弃 Kafka 等）
- 域: D6 应用与平台
- 来源: https://github.com/DependencyTrack/dependency-track/tree/main/docs/adr
- 代表: ADR-001 drop Kafka；ADR-002 workflow orchestration
- 阶段: Phase 2 · 2026-08-05

## 问题类（ADR-001/002 合读）
供应链组件分析平台如何做**异步工作与通知**：曾引入 Kafka，后因运维复杂度与编排可观测性不佳而回退，改用现有 Postgres 能力。

## 机制（从 ADR 实践抽出）
1. **先写清当前用法与痛点**（Context）
2. **并列 Possible Solutions**（换 broker / IMDG / 就用 Postgres…）
3. **选 C 并写后果与迁移**（采纳、渐进、兼容通知）
4. **后续 ADR 承接缺口**（编排、outbox、follow-up）——决策链

## 策略教训（对消息中间件）
| 策略 | 结果 |
|------|------|
| 上 Kafka 做事件总线 | 运维与心智过重；choreography 难观测 |
| 换轻量 broker | 仍增外部依赖 |
| **Just use Postgres** | 降低运维；用 advisory lock、SKIP LOCKED、批处理等适配 DB |
| Orchestrator 优于纯 choreography | 可观测与可理解性 |

## 与 D4 的交叉
- Kafka/Pulsar 是强工具，**不是默认答案**；问题类若非「公司级日志总线」，可能过重
- Buddy 在 D4/D6 交界必须问运维边界与团队能力（M3）

## 对写作规范的启示
- 生产 ADR 金样：问题→选项表→决定→后果→后续 ADR
- 「撤销先前架构」同样要留下记录（supersede/follow-up）
