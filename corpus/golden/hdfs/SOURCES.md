# SOURCES — hdfs

## 权威公开设计

1. The Architecture of Open Source Applications (Volume 1) — The Hadoop Distributed File System  
   https://aosabook.org/en/v1/hdfs.html  
   金标机制/策略主依据：NameNode/DataNode 分离、大块多副本、journal+checkpoint、心跳捎带指令、管线写、机架感知放置、数据局部性 API 等。

## 本地 survey / 对照摘记

2. `docs/survey/architecture/D3-hdfs.md`  
   Phase 1 调研摘记；本金标由其升格为完整双层 deliverable。

## 使用约定

- 校准可读本 SOURCES；严校可闭卷，仅对照 GOLDEN + RUBRIC。
- 运行时 skill 不得把本文件当用户考试题库展示。
