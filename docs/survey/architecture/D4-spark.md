# Apache Spark — Cluster & RDD 架构心智
- 域: D4 消息与流式 / 数据并行计算
- 来源: https://spark.apache.org/docs/latest/cluster-overview.html ；https://spark.apache.org/docs/latest/rdd-programming-guide.html
- 阶段: Phase 2 · 2026-08-05

## 问题类
在商品机集群上做**通用数据并行计算**：不仅是一次性 Map→Shuffle→Reduce 批作业，还要支撑**迭代算法、交互查询与多阶段 DAG**，并在节点失败时用血缘重算恢复，而不是假设「全程纯内存、永不落盘」。

## 硬约束（动机）
- 多阶段流水线（不只两阶段 MR）
- 同一数据集跨多轮复用（迭代 / 交互）时避免每次都写外部存储
- 集群资源由外部管理器分配；应用彼此隔离
- 分区并行；宽依赖必须付 shuffle 代价
- 节点天天坏 → 容错是默认路径

## 机制（共性）
1. **Driver + Executor**：Driver 持 SparkContext / 调度；Executor 跑 task 并可缓存分区
2. **惰性变换 + Action 触发**：transformation 只记血缘；action 才物化计算
3. **Job → Stage → Task**：按 shuffle 边界切 stage；窄依赖可流水线进同一 stage
4. **Shuffle（宽依赖）**：跨分区重分布；涉及序列化、磁盘 spill、网络 IO
5. **血缘重算容错**：丢分区则按 lineage 重算；persist 可换速度但不取消容错
6. **对集群管理器无关**：Standalone / YARN / Kubernetes 等只负责拿到 executor 进程

## 策略（差异/选项）
| 策略 | 选择 | 排除/对照 |
|------|------|-----------|
| 作业模型 | 多阶段 DAG + 内存复用 | MapReduce 式每阶段落外部存储的一次性作业 |
| 物化 | 显式 persist/cache（多 StorageLevel） | 默认每 action 全量重算（仍正确，但迭代慢） |
| 部署 | cluster 模式 driver 进集群 | client 模式 driver 在提交端（远距调度成本） |
| 集群管理 | Standalone / YARN / K8s | 与计算引擎绑死的专用资源面 |
| API 层 | RDD 显式血缘 vs DataFrame/SQL 优化计划 | 不取消 stage/shuffle 物理现实 |

## 显式模式名
- Driver–Worker / Master–Executor（应用内）
- Lazy Evaluation + Lineage
- DAG Scheduler / Stage Pipelining
- Shuffle（wide dependency）
- Cache / Persist with StorageLevel

## 决策与负面后果
- 「内存计算」≠ 无磁盘：shuffle 与 spill 会写本地盘；长作业可积压大量 shuffle 文件
- 应用级 executor 隔离 → 跨 SparkContext 不能直接共享内存缓存，需外部存储
- Driver 必须对 executor 可寻址；远距离 driver 伤害调度与收集路径

## 对写作规范的启示
- 先讲问题类（迭代/多阶段/血缘）再挂组件名
- 对照 MR 时写清「放弃了什么」（每 stage 落 HDFS）及换来的代价（内存压力、shuffle 调优）
