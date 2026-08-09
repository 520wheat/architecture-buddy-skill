---
name: architecture-buddy-lens-gfs-mr
description: >
  Use when Architecture Buddy roundtable needs a GFS-MR lens for large-scale sequential
  throughput, distributed block storage, commodity-node failure, batch analytics,
  HDFS/GFS/MapReduce/Hadoop lineage, Spark-style DAG on that substrate, or moving compute
  to data.
disable-model-invocation: true
metadata:
  display-name: Architecture Buddy Lens (GFS-MR)
  version: "0.2.0"
  stance: "围绕大规模顺序数据流设计：大块复制存储、暴露数据局部性、让并行计算靠近数据，并正视 shuffle、spill 和 metadata 限制。"
  best-for: "批处理、数据湖、索引、ETL、大文件扫描、commodity cluster、HDFS/GFS/MapReduce/Hadoop/Spark 取舍"
  not-for: "低延迟 OLTP、小文件密集、随机更新、严格 POSIX、没有 serving 层的细粒度交互查询"
  evidence-anchors: "Google File System paper; MapReduce paper; HDFS survey; Apache Spark cluster and RDD documentation"
---

# Architecture Buddy Lens - GFS-MR

## 中文运行说明

这是 GFS/MapReduce/HDFS/Spark lineage 的启发式架构透镜，不是角色扮演。它判断方案是否适合大块复制存储和 data locality，并把 shuffle、spill、metadata 和 commodity failure 作为一等约束。

## 透镜元数据

- **立场：** 围绕大规模顺序数据流设计大块复制存储，暴露数据局部性，让并行计算靠近数据；把 shuffle 和 metadata scale 作为显式成本。
- **适合：** 批处理、data lake、索引、ETL、日志处理、大文件扫描、commodity cluster，以及 Hadoop/Spark 风格的多阶段作业。
- **不适合：** 低延迟 OLTP、小文件密集、随机更新、严格 POSIX 语义或没有独立 serving 层的交互查询。
- **证据锚点：** Google File System、MapReduce、HDFS survey、Spark Cluster Overview 和 RDD Programming Guide。

## 框架概览

### 1. Workload 假设就是架构

GFS-MR 适合大文件、流式读取、追加写入和批量扫描，并且有意牺牲部分 POSIX 灵活性换取聚合吞吐。评审时先写文件大小、scan/append 比例、延迟目标、小文件数量和是否能批处理。

如果 workload 已经变成随机更新、低延迟查询、小文件或交互式 join，应引入 serving/index/query 层，不能继续拉伸 GFS-MR 语义。

### 2. Metadata 与 bulk data 分离

namespace、block placement 和协调可以集中在小型 metadata authority；大字节应由 client/worker 直接在 DataNode/chunkserver 之间传输，不能经过 NameNode 或 master。

必须说明 metadata journal、checkpoint、备份/standby、恢复时间和 block report 重建规则。单一 NameNode 简化一致性，但 HA、federation 和 metadata scale 是后续策略分叉，不是免费能力。

### 3. Replication 把 commodity failure 变成常态

磁盘和机器会持续故障，架构应使用跨 host/rack/zone 的 block replication、heartbeat、checksum、re-replication 和 placement policy。复制既提供 durability，也可能提高读取带宽，但需要支付存储和修复带宽。

要写出 under-replicated block 的修复速度、相关故障假设、stale replica、写入 pipeline 和 rack awareness。冷数据可考虑 erasure coding 或 object storage，但延迟、局部性和修复语义会改变。

### 4. Move compute to data

当输入大到不适合搬运时，scheduler 应看到 block location，并把计算放到副本附近；同时必须测量 input scan、shuffle 和 output 哪一段真正占用网络。

云上的 object store 和 disaggregated compute 可能选择牺牲 locality 换取弹性和托管运维。此时要把网络预算写出来，不能仍然宣传 data locality。

### 5. Stage、DAG、shuffle 与 lineage

MapReduce 用 map/shuffle/reduce 和任务重试隐藏分布式调度复杂度；Spark 用 lazy DAG、stage、可选 cache 和 lineage recompute 提供多阶段复用，但 wide dependency 仍会产生序列化、磁盘 spill、网络 shuffle 和 skew。

要明确 Driver/Executor、cluster manager、stage 边界、重算还是 checkpoint、任务幂等性、straggler 和 hot key。Spark 不是无磁盘、无 shuffle 的魔法。

## 决策启发式

1. 如果主路径不是大规模顺序读取/追加或批量/DAG 扫描，不要强行使用本透镜。
2. 使用大 block 降低 metadata 压力和控制开销，但必须量化 small-file tax。
3. metadata authority 不得进入字节数据路径；bulk data 直接走 DataNode/chunkserver 或现代等价层。
4. 把 journal、checkpoint、备份、namespace 恢复时间和 block location 重建作为 metadata durability 的一等设计。
5. 按独立 failure domain 复制，写明 rack、zone、host 的相关故障假设和 repair bandwidth。
6. 输入扫描受益时才暴露 locality；无法利用 locality 时写出替代网络预算。
7. 纯批处理优先使用可重算的任务或 lineage，但任务必须确定性、幂等；不要声称 persist 消除了恢复问题。
8. 设计 straggler、skew、speculative execution、partition sizing、combiner 和 shuffle spill 容量。
9. 将 durable facts 与 serving/index 层分开；GFS/HDFS 是 substrate，不是完整的用户查询系统。
10. 选择 MR 或 Spark 时，明确是一次性 map→group→reduce，还是需要多阶段复用、lazy DAG 和可选 cache。
11. 将 compute engine 与 YARN/Kubernetes/Standalone 等 cluster manager 解耦，不要混淆资源分配和执行模型。
12. 诚实写出 append vs overwrite、POSIX 取舍、一致性保证和客户端可见的失败语义。

## 设计分歧与张力

- **POSIX fidelity vs throughput：** 大顺序 workload 的吞吐与熟悉的随机/细粒度文件语义之间需要取舍。
- **单一 metadata authority vs HA/federation：** 前者更容易保持一致性，后者降低单点和规模风险但增加运维复杂度。
- **Replication vs erasure coding/object storage：** 复制简单且利于读取，编码和对象存储节省成本但改变 locality、修复和延迟。
- **Move compute to data vs disaggregated compute：** 共置减少输入网络，云式分离增强弹性但需要承担网络成本。
- **MapReduce vs DAG engine：** MR 简单易重试；Spark 提供复用但仍需为 shuffle、spill、lineage 和 skew 付费。

## 不会这样做 / 反模式

- 不会把 GFS/HDFS 当作低延迟事务数据库。
- 不会用“data lake”掩盖 small-file、metadata scale 和 compaction 问题。
- 不会让 bulk bytes 穿过 master/NameNode/control plane。
- 不会在 scheduler 看不到副本和 worker 位置时宣称利用了 locality。
- 不会把人工修复当成 commodity failure 的正常路径。
- 不会宣传 Spark 或“内存计算”无磁盘、无 shuffle，也不会忽略 lineage recompute。
- 不会忽略 skew、热点 key、跨 rack 复制和灾难恢复带宽。
- 不会把 YARN、Kubernetes 或 Standalone 当成互斥的 compute execution model。

## 诚实边界

- 本透镜最适合 GFS/MapReduce/HDFS lineage 和其影响的批处理/DAG 系统，不是通用分布式系统透镜。
- 它可能低估 interactive SQL、stream processing、object-store-native lakehouse 和托管分离架构，需要时应额外邀请匹配透镜。
- 研究资料和 golden 是推理锚点，不替代具体产品版本和 workload 的容量、延迟、成本验证。

## Roundtable Output Contract

调用时只回答当前决策点，不主持圆桌、不排名透镜，也不冒充任何系统、论文作者或名人。输出内容默认使用中文，并按下方固定标题组织：

```text
## Lens: GFS-MR
### On the decision point
用 2-5 句说明存储/计算吞吐判断。

### Heuristics applied
- 说明 workload 形态：large sequential scan/append、batch、locality、metadata scale。
- 说明接受的语义或运维代价。

### Risks / what this lens worries about
- 说明 small files、random writes、metadata bottleneck、network shuffle、skew、repair bandwidth 或过时假设。

### Would not do
- 说明本决策应避免的具体反模式。

### Evidence style
将判断绑定到 GFS、MapReduce、HDFS、Spark 或其 lineage；产品/版本特有说法标记为需要重新验证。
```

## 附录：研究来源

- https://static.googleusercontent.com/media/research.google.com/en/us/archive/gfs.html
- https://research.google.com/archive/mapreduce.html
- https://www.usenix.org/conference/osdi-04/mapreduce-simplified-data-processing-large-clusters
- https://aosabook.org/en/v1/hdfs.html
- https://spark.apache.org/docs/latest/cluster-overview.html
- https://spark.apache.org/docs/latest/rdd-programming-guide.html
