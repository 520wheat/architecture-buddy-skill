# RUBRIC — etcd

## 必中机制（≥5）

- 单一致复制组 + Raft（或等价多数派共识）；全局 revision 作逻辑时钟
- KV 严格可串行化 / 默认线性化读路径；写经 quorum
- MVCC + 历史窗口 + compaction（非「只有当前值」）
- Watch：有序、可靠、可恢复（bookmark/resume），但不保证线性化
- Lease（及基于其的 Lock / Election 等）与存储同体，非纯外挂 recipes
- 元数据量级（约数 GB 心智），非海量业务数据仓库
- CP 取向：不容忍 split-brain；客户端须理解超时/选主时完成性不确定

## 必中策略分叉（≥3）

- 一致 KV + 原语齐全 vs ZooKeeper 式层次 znode + 客户端拼装
- 只做强一致元数据存储 vs Consul 式端到端服务发现产品
- 单分片强顺序 vs NewSQL / 分片海量数据路径
- （加分）默认可线性化读 vs 可读走 serializable 降延迟（可能读到相对 quorum 的旧值）

## 叙事完整性

- 层 A（A1–A8）与层 B（B1–B6）齐全，封面元数据完整；B6 需包含变化轴、N+1、反例及能力/复杂度边界证据
- 主路径可走通：客户端写/条件事务 → Raft 提交 → MVCC revision → 线性化读 / Watch 通知
- 硬约束动机（反脑裂、元数据规模、超时不确定）在摘要或上下文中可见
- 取舍写清放弃了什么（如 AP 优先、当大数据仓库、Lock 即外部互斥）及代价

## 幻觉黑名单（出现则 FAIL）

- 声称 etcd「可容忍 split-brain / 默认 AP」或脑裂可接受
- 把 etcd 写成海量业务数据 / 通用 SQL 数据仓库
- 声称 Watch 保证线性化（与 KV 默认可线性化混为一谈且不点出差异）
- 声称 Lock API 本身已保证对外部资源的互斥（无需资源侧版本/fencing）
- 把 Lease TTL 说成「绝不存在服务端已撤、客户端仍自认持有」的物理时钟无瑕疵
- 整段套用「最终一致 K/V 缓存」叙事而不点出 Raft/线性化差异
