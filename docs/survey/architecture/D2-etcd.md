# etcd — Learning: Why / API Guarantees
- 域: D2 分布式协调与集群
- 来源: https://etcd.io/docs/latest/learning/ · https://etcd.io/docs/v3.5/learning/why/
- 阶段: Phase 1 · 2026-08-04

## 问题类
为大规模分布式系统提供**强一致、可持久的元数据存储与协调原语**（配置、服务发现、选主、分布式锁优化），宁可牺牲部分可用性也要避免脑裂。

## 硬约束
- 永不容忍 split-brain（CP 取向）
- 元数据规模：可靠量级约数 GB，非海量业务数据
- 客户端必须理解超时/选主时「完成性不确定」

## 机制（共性）
1. **单一致复制组 + Raft**：全局 revision 作逻辑时钟
2. **严格可串行化（KV）/ 默认可线性化**；Watch 有序、可靠、可恢复但不保证线性化
3. **MVCC + 历史窗口 + compaction**
4. **Lease / Lock / Election** 等协调原语与存储同体（非外挂 recipes 了事）
5. **Watch** 作为变更通知机制（带 bookmark/resume）

## 策略（差异/选项）— 相对 ZooKeeper / Consul / NewSQL
| 策略 | 相对谁 | 要点 |
|------|--------|------|
| etcd：一致 KV + 原语齐全 | ZooKeeper | 动态成员、MVCC、可靠 watch、gRPC/JSON |
| etcd：只做一致存储，不做完整服务发现产品 | Consul | Consul 是端到端发现；etcd 更适合「存元数据」 |
| 单分片强顺序 | NewSQL | 海量数据/SQL 选 NewSQL；协调选 etcd |
| 可读走 serializable 降延迟 | 线性化默认 | 可能读到相对 quorum 的旧值 |

## 显式模式名 / 文献锚点
- Consensus / Replicated State Machine（Raft）
- Lease + fencing/version validation（文中对照 Chubby sequencer、Kleppmann fencing token）
- Compare-and-swap / 条件事务

## 决策与负面后果
- Lock API **本身不保证**对外部资源的互斥；需资源侧版本校验
- Lease TTL 基于物理时钟 → 服务端已撤、客户端仍可能自认持有
- Watch 延迟无上界；不健康集群可能永远收不到

## 对写作规范的启示
- 优秀架构文会用**对照表**讲清问题类边界（M1）与策略（M5）
- 安全使用条件写进「后果」——对齐 ADR Consequences
