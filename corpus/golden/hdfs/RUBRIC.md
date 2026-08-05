# RUBRIC — hdfs

## 必中机制（≥5）

- 元数据与数据分离：NameNode 保管命名空间与块→节点映射；DataNode 保管块副本
- 文件切成大块；每块独立多副本（默认典型为三副本）跨 DataNode，而非依赖 DN 本地 RAID
- 客户端读写数据时直连 DataNode；NameNode 提供位置/分配，不经 NN 中转块字节
- 命名空间持久化：WAL journal + checkpoint；块位置不在持久 checkpoint 内，靠 DN block report / 心跳重建
- NameNode 不主动对 DN 发复杂推送 RPC；指令捎带在心跳应答中
- （加分）写路径管线（pipeline）复制；读路径按拓扑距离优选副本；暴露块位置 API 支持计算局部性

## 必中策略分叉（≥3）

- 耐久：跨节点多副本冗余 vs 存储节点侧 RAID（对照 Lustre/PVFS 路径）
- 元数据拓扑：单 NameNode（当时设计）vs 后续 HA / Federation 多命名空间
- 元数据耐久辅助：CheckpointNode 周期合并 vs BackupNode 内存同步只读待命
- （加分）journal 提交：批处理 flush-and-sync vs 逐事务同步；POSIX 忠诚 vs 批处理吞吐优先

## 叙事完整性

- 层 A（A1–A8）与层 B（B1–B5）齐全，封面元数据完整
- 主路径可走通：客户端 → NameNode（元数据）→ 直连 DataNode（块读写）→ 副本管线 / 校验与再复制
- 硬约束动机（商品机规模、流式高带宽、计算靠近数据、牺牲部分 POSIX）在摘要或上下文中可见
- 取舍写清放弃了什么（如全 POSIX、DN 侧 RAID 为主耐久、经 NN 中转数据面）及代价

## 幻觉黑名单（出现则 FAIL）

- 声称数据块字节默认经 NameNode 中转读写
- 把 HDFS 耐久主路径写成「依赖 DataNode 本地 RAID」而忽略跨节点副本
- 声称 NameNode 把块副本位置作为持久 checkpoint 的一部分长期落盘
- 把当时单 NameNode 设计说成「天然无 SPOF、无限水平扩展元数据」且无代价叙述
- 声称必须完整 POSIX（随机改写、强一致小文件语义等）才算文件系统
- 整段套用传统集中 SAN/POSIX NAS 叙事而不点出元数据/数据分离与副本策略
