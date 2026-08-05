# SOURCES — etcd

## 权威公开设计

1. etcd Documentation — Learning  
   https://etcd.io/docs/latest/learning/  
   金标机制/策略主依据：Raft 复制组、API 保证、MVCC、watch、lease 等。

2. etcd Documentation — Why etcd  
   https://etcd.io/docs/v3.5/learning/why/  
   问题类边界、相对 ZooKeeper / Consul / NewSQL 的策略对照、安全使用后果。

## 本地 survey / 对照摘记

3. `docs/survey/architecture/D2-etcd.md`  
   Phase 1/2 调研摘记；本金标由其升格为完整双层 deliverable。

4. `docs/survey/architecture/D2-zookeeper.md`（可选对照）  
   仅用于层 B 策略分叉与 B5 教训，不整段套用 ZooKeeper 叙事。

## 使用约定

- 校准可读本 SOURCES；严校可闭卷，仅对照 GOLDEN + RUBRIC。
- 运行时 skill 不得把本文件当用户考试题库展示。
