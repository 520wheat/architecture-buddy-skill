# SOURCES — spark

## 权威公开设计

1. Apache Spark Documentation — Cluster Mode Overview  
   https://spark.apache.org/docs/latest/cluster-overview.html  
   金标部署/组件主依据：Driver、Executor、Cluster Manager（Standalone / YARN / Kubernetes）、Application / Job / Stage / Task 术语、client vs cluster 部署模式。

2. Apache Spark Documentation — RDD Programming Guide  
   https://spark.apache.org/docs/latest/rdd-programming-guide.html  
   金标执行/容错主依据：惰性 transformation vs action、shuffle 与代价（磁盘/序列化/网络）、persist/cache 与 StorageLevel、血缘重算、broadcast / accumulator。

## 本地 survey / 对照摘记

3. `docs/survey/architecture/D4-spark.md`  
   Phase 2 调研摘记；本金标由其升格为完整双层 deliverable。

4. （对照，非主依据）MapReduce / HDFS 心智 — `docs/survey/architecture/D3-hdfs.md` 与 `corpus/golden/hdfs/`  
   仅用于层 B 策略分叉与 B5：一次性落盘作业 vs 内存友好迭代 DAG；不整段套用 HDFS 存储叙事。

## 使用约定

- 校准可读本 SOURCES；严校可闭卷，仅对照 GOLDEN + RUBRIC。
- 运行时 skill 不得把本文件当用户考试题库展示。
- 金标锚定公开文档中的经典执行心智（RDD/DAG/stage/shuffle）；DataFrame/Catalyst 等为演进层，不取消物理 stage 与 shuffle。
