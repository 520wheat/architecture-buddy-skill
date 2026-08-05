# Spanner — Global External Consistency + SQL at Scale
- 域: D2 分布式协调与集群
- 来源: Google Spanner OSDI 2012 paper; Cloud Spanner replication / reads-writes / external consistency docs
- 阶段: Phase 4 · 2026-08-05（Architecture Buddy lens corpus）

## 问题类
在多区域复制、可水平分片的数据库里提供**SQL + ACID 事务 + 外部一致性**：如果 T1 在真实时间上先提交、T2 后开始，系统的序列化顺序也必须让 T1 在 T2 之前。

## 硬约束 / 设计目标
- 全局事务顺序要匹配客户端观察到的真实时间顺序（external consistency / strict serializability）
- 数据按 key range / split 扩展，但跨 split 事务仍要成立
- 读路径要支持强读、只读事务、历史快照与备份，不让所有读取都阻塞写入
- 多区域复制要同时服务高可用、地理局部性与强一致
- SQL 抽象不能掩盖 schema、主键、索引、leader 位置带来的物理代价

## 机制（共性）
1. **TrueTime / bounded uncertainty**：时间 API 返回 `[earliest, latest]` 区间；不假装物理时钟是精确点。
2. **Commit wait**：写事务选择全局有意义的 commit timestamp，并等到该时间确定已过去后才对外可见。
3. **Split + Paxos replica set**：数据按连续 key range 分片；每个 split 由 Paxos 组同步复制，leader 处理写，quorum 决定提交。
4. **MVCC timestamp reads**：读在某个 timestamp 上取一致快照；只读事务可无锁运行，历史读/备份/MapReduce 可选过去时间点。
5. **跨组事务协调**：Paxos 复制负责单组日志，跨 split 写事务还需要事务协调（如 2PC）保持 SQL 语义。
6. **Timestamped schema change**：schema change 可注册未来时间戳，读写按时间戳与 schema 变更同步，避免全球阻塞式 DDL。

## 策略（与相邻选项对照）
| 策略 | 适用 | 代价 / 边界 |
|------|------|-------------|
| Spanner-style global SQL | 业务需要跨区域强事务、外部一致性、SQL 访问 | commit wait、quorum、leader placement、跨 split 事务尾延迟 |
| 单区域 SQL + 异步复制 | 多数写在单区域，异地主要灾备/只读 | 全球写入与真实时间顺序不成立 |
| AP/CRDT/事件补偿 | 离线、协作编辑、可合并冲突 | 业务必须接受冲突、补偿和最终收敛 |
| 中央 timestamp oracle / TSO | 可接受集中授时组件 | timestamp 服务成为关键依赖和扩展/高可用问题 |
| HLC/NewSQL 变体 | 想降低硬件授时门槛 | 需逐项验证保证是否等同外部一致性，不能只看 SQL 接口 |

## 显式模式名 / 文献锚点
- External consistency / strict serializability
- TrueTime / bounded clock uncertainty
- Commit wait
- Paxos-replicated split / replicated state machine
- MVCC snapshot read
- Two-phase commit over replicated participants
- Timestamped DDL / non-blocking schema change

## 决策与负面后果
- 强一致全球写不是低延迟魔法：leader 区域、quorum 距离、clock uncertainty 与跨 split 事务都会进入尾延迟。
- Schema 是物理设计的一部分：主键、interleaving/locality、secondary index 会决定数据是否同地、是否放大远程写。
- 强读、bounded stale read、历史读必须分清；把 stale read 包装成「实时」会制造产品语义 bug。
- TrueTime 是基础设施承诺；没有有界不确定性与 commit wait，就不能宣称同等 external consistency。
- 适合需要强全局不变量的 OLTP，不适合作为所有跨地域数据同步、缓存失效、日志或离线冲突合并问题的默认答案。

## 对写作规范的启示
- D2 笔记要把「一致性声明」写成可验证契约：谁排序、按什么时间、何时对外可见。
- 对全球数据库类方案，必须同时写机制与物理代价：time、quorum、placement、schema locality、read freshness。
