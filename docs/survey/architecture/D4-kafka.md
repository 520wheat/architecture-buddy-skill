# Apache Kafka — Design
- 域: D4 消息与流式
- 来源: https://kafka.apache.org/documentation/#design
- 阶段: Phase 2 · 2026-08-05

## 问题类
作为公司级**统一实时数据源平台**：高吞吐日志/事件、可积压、低延迟投递、分区并行处理、机器故障下容错——设计更接近**分布式日志/数据库日志**而非传统消息队列。

## 硬约束（动机）
- 高吞吐（如页面行为海量写入）
- 大 backlog（离线周期性负载）
- 低延迟传统消息场景
- 分区分布式实时派生流
- 故障容错

## 机制（共性）
1. **持久化追加日志**；拥抱文件系统与 OS pagecache（而非惧盘）
2. **顺序写 O(1)**；避免 BTree 式每消费者元数据导致的寻道放大
3. **长时间保留**而非消费即删 → 可重放
4. **消息集批处理 + 通用二进制格式 + sendfile/零拷贝**（SSL 时受限）
5. **Producer 直连分区 leader**；语义分区键
6. **Consumer pull + 长轮询**；位点=分区 offset 整数
7. **Consumer group**：分区内组内单消费者；可 rewind

## 策略（差异/选项）
| 策略 | 选择 | 排除/对照 |
|------|------|-----------|
| 存储 | pagecache 中心日志 | 堆内大缓存（GC/双缓存） |
| 消费模型 | pull | broker push（难匹配异构消费速率） |
| 消费位点 | 客户端侧 offset | broker 逐条 ack 状态机 |
| 分区 | 键哈希语义局部性 | 纯随机（失局部性） |
| 压缩 | 批次端到端压缩 | 逐条压缩（比差） |

## 显式模式名
- Write-Ahead / Commit Log
- Partitioned Log
- Consumer Group / Competing Consumers（组内）
- Batching、Zero-Copy

## 决策与负面后果
- 像队列又允许 rewind → 打破「消费即消失」直觉，换灵活性
- SSL 禁用 sendfile 路径 → 吞吐策略变化
- 多租户要靠极致效率，避免基础设施先于应用垮掉

## 对写作规范的启示
- 开篇用**多用例动机**导出设计（M1/M4→M5）
- 「Don’t fear the filesystem」式破除迷思 = 优秀架构叙述
