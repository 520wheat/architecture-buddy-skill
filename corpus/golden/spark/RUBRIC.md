# RUBRIC — spark

## 必中机制（≥5）

- Driver（用户 main / SparkContext）与 Executor（跑 task、可跨 task 保留分区数据）职责分离
- 惰性求值：transformation 只构建血缘/执行图；action 才触发 Job
- Job 划分为 Stage；Stage 边界由需要跨分区重分布的 **shuffle（宽依赖）** 切开；窄依赖可流水线进同一 Stage
- Shuffle 是昂贵路径：涉及序列化、本地磁盘（含 spill）、网络 IO——不是「纯内存魔法」
- 容错靠 **lineage 重算**丢失分区；persist/cache 加速复用但不取消血缘恢复叙事
- （加分）对 Cluster Manager 无关：Standalone / YARN / Kubernetes 等只负责申请 executor；应用级 executor 隔离；client vs cluster 部署模式

## 必中策略分叉（≥3）

- 作业模型：多阶段 DAG + 工作集内存复用 vs MapReduce 式每阶段物化到外部存储的一次性作业
- 物化策略：显式 persist/cache（及 StorageLevel：内存/磁盘/复制）vs 默认每 action 按血缘重算
- 集群资源面：Standalone vs YARN vs Kubernetes（引擎与资源管理器解耦）
- （加分）部署：cluster 模式（driver 进集群）vs client 模式（driver 在提交端）；API：RDD 显式图 vs DataFrame/SQL 优化计划（仍服从 stage/shuffle）

## 叙事完整性

- 层 A（A1–A8）与层 B（B1–B6）齐全，封面元数据完整；B6 需包含变化轴、N+1、反例及能力/复杂度边界证据
- 主路径可走通：Driver 连接 Cluster Manager → 获得 Executor → 惰性构图 → Action 触发 → Stage/Task 调度 →（可选）Shuffle → 结果/缓存
- 硬约束动机（多阶段、迭代/交互复用、分区并行、商品机故障）在摘要或上下文中可见
- 取舍写清放弃了什么（如 MR 每 stage 落外部存储、假装无 shuffle/无磁盘）及代价

## 幻觉黑名单（出现则 FAIL）

- 声称 Spark「无磁盘 / 永不 shuffle / 全程纯内存」
- 声称 Executor 失败后数据永久丢失且无法按血缘重算（否认 lineage 容错）
- 把 Spark 写成必须绑死某一种 Cluster Manager，或无法跑在 YARN/K8s 等外部资源面上
- 把 transformation 写成默认立即全量物化（否认惰性），或把 action 与 transformation 混为一谈
- 把宽依赖/shuffle 说成与窄依赖一样可无代价流水线、无 stage 边界
- 整段套用「MapReduce 两阶段且每阶段必须落 HDFS」叙事而不点出 DAG/内存复用差异，或相反把 Spark 说成取消了分区并行与 shuffle
