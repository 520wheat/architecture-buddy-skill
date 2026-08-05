# SOURCES — kafka

## 权威公开设计

1. Apache Kafka Documentation — Design  
   https://kafka.apache.org/documentation/#design  
   金标机制/策略主依据：持久化日志、pagecache、pull、分区、consumer group、批处理与零拷贝等。

## 本地 survey / 对照摘记

2. `docs/survey/architecture/D4-kafka.md`  
   Phase 2 调研摘记；本金标由其升格为完整双层 deliverable。

3. `docs/survey/architecture/D4-kafka-vs-pulsar.md`（可选对照）  
   仅用于层 B 策略分叉与 B5 教训，不整段套用 Pulsar 叙事。

## 使用约定

- 校准可读本 SOURCES；严校可闭卷，仅对照 GOLDEN + RUBRIC。
- 运行时 skill 不得把本文件当用户考试题库展示。
