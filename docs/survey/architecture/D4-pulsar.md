# Apache Pulsar — Architecture Overview
- 域: D4 消息与流式
- 来源: https://pulsar.apache.org/docs/concepts-architecture-overview/
- 阶段: Phase 2 · 2026-08-05

## 问题类
提供**持久、可扩展、可地理复制**的发布订阅消息平台；计算（broker）与持久存储（BookKeeper）分离，以独立扩展。

## 硬约束
- 消息到达 broker 后需持久直至投递并确认（persistent messaging）
- 多副本落盘
- 云/K8s 下客户端常不能直连所有 broker → 可选 Proxy

## 机制（共性）
1. **Broker 无状态**：HTTP/REST（管理与查找）+ 二进制异步调度
2. **BookKeeper 存消息与 cursor**（分布式 WAL / ledger）
3. **Metadata store**（Oxia/ZK/RocksDB）做协调与元数据
4. **Managed ledger**：单 topic 流抽象，底层多 ledger 滚动
5. **单 writer ledger + 失败恢复定界** → 读者见一致内容
6. **可选 Proxy / 服务发现**：统一入口
7. **实例级 configuration store** + 集群本地 metadata；geo-replicator

## 策略（差异/选项）— 相对 Kafka
| 维度 | Pulsar | Kafka（对照） |
|------|--------|----------------|
| 存储 | 计算与 BookKeeper 存储分离 | 日志常与 broker 共置（经典部署） |
| 元数据 | 独立 metadata store 可选后端 | 控制器/元数据演进路径不同 |
| 入口 | 可选 Proxy 网关 | 客户端发现分区 leader |
| 地理复制 | 一等 replicator | MirrorMaker 等生态方案 |
| 非持久 | 支持 ephemeral non-persistent | 以持久日志为中心 |

## 显式模式名
- Tiered: Stateless Serving + Durable Log Store
- Write-Ahead Log / Ledger
- Gateway (Proxy)
- Geo-replication

## 决策与负面后果
- 组件更多（broker+bookie+metadata）→ 运维面大于「单集群日志」心智
- ledger 单写者模型简化一致，恢复流程成为关键路径

## 对 Buddy
流系统共思：先问「要的是统一公司日志总线，还是计算/存储分离+多租户地理复制？」再在 Kafka/Pulsar 策略间选。
