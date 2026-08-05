# AOSA — HDFS
- 域: D3 数据存储与查询
- 来源: https://aosabook.org/en/v1/hdfs.html
- 阶段: Phase 1 · 2026-08-04

## 问题类
在数千台商品服务器上**可靠存储超大<fim-middle>数据集**，并以高带宽流式供给计算（MapReduce 等），计算靠近数据。

## 硬约束
- 牺牲部分 POSIX 忠诚换性能
- 元数据与数据分离；元数据需持久与可恢复
- 用多副本而非 RAID 做耐久与带宽

## 机制（共性）
1. **NameNode（元数据）/ DataNode（数据块）分离**
2. **大块 + 多副本**；客户端直连 DataNode 传数据
3. **WAL journal + checkpoint** 保护命名空间镜像
4. **心跳捎带指令**（NameNode 不主动推复杂 RPC 给 DN）
5. **数据局部性 API** 暴露块位置给调度器

## 策略（差异/选项）
| 策略 | 对照 |
|------|------|
| 副本冗余 vs RAID | 与 Lustre/PVFS 不同，对齐 GFS |
| 单 NameNode（当时设计） | 简化一致性，代价是元数据 SPOF/扩展上限 |
| CheckpointNode / BackupNode | 元数据耐久与只读待命的策略演进 |
| 批处理 flush-and-sync | 缓解 journal 同步瓶颈 |

## 显式模式名
- Master-Slave / Primary-Secondary（NN/DN）
- Replication for durability & read bandwidth
- Write-Ahead Log
- Pipeline write（多副本管线）

## 决策与负面后果
- 单 NameNode：当时架构的中心权衡（后续生态才有 HA/Federation）
- Journal 过长 → 重启慢；需每日 checkpoint 纪律

## 对写作规范的启示
- 开篇用规模数字锚定问题类（40PB）——具体场景化 ASR
- 明确「不像传统文件系统」的牺牲 = M1 边界
