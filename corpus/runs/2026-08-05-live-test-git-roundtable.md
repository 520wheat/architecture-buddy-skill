# 架构设计：分布式内容寻址版本历史——圆桌校准版

> 模式：deliverable
> 测试对象：`https://github.com/git/git`，官方仓库 `master`，检出提交 `5b24717`
> 本次圆桌测试：主持人识别到高影响互斥分叉后主动提议；测试用户明确同意；加载 2 个匹配透镜
> 问题类：多人协作的文件树版本历史，需要离线记录、分支合并、内容完整性和可选择的跨仓库分享
> 明确不做：代码托管产品、代码审查、CI/CD、工单、实时协同编辑、访问控制中心

## 圆桌提议与用户选择

在主策略形成前，主持人识别出三个高影响互斥分叉：

- Git 历史应被理解为追加日志，还是内容寻址快照与父指针 DAG？
- refs 发布是否需要中央强一致协调，还是每个仓库可以本地更新再交换？
- 逻辑快照模型与 pack/delta 物理压缩是否应保持分离？

主持人先说明原因：这些分叉会改变历史真相、提交边界和故障语义，单一视角容易把存储优化或远程工作流误写成核心架构。**用户同意圆桌。**

席位选择：

- `log-stream`：检验追加、重放、消费位点和日志作为事实来源的适用边界；Git 的 pack 传输和历史追加容易诱发错误类比。
- `raft-cp`：检验 refs 发布是否真的需要多数派、leader 和线性化元数据；用于明确 Git 的本地可写边界，而不是把 Git 当作 etcd。

## Lens: Log Stream
### On the decision point
Git 的 commit 历史具有追加和可遍历的一面，但 Git 的事实来源不是单一消费日志：对象库保存可寻址的 blob/tree/commit，refs 只是可变发布指针。pack 是对象传输与存储表示，不应成为业务事件日志。

### Heuristics applied
- 先问谁消费事实、谁拥有位点；Git 的 fetch 通过共同对象协商，不是消费者 offset 推进。
- 区分可重放对象与不可逆副作用；Git 可以重新遍历对象，但不会由日志自动完成业务动作。
- 检查保留成本和重放边界；reflog、gc、shallow/partial clone 都会改变可恢复范围。

### Risks / what they'd worry about
- 把 commit 误写成只能顺序消费的事件，丢失分支、共同祖先和任意对象访问。
- 把 pack 或 receive-pack 误写成跨仓库事务日志，掩盖 ref 发布条件与对象完整性检查。
- 宣称 replay 天然安全，忽略历史重写、不可达对象回收和缺失对象边界。

### Would not do
- 不会把 Kafka/Pulsar 式 broker、consumer group 或 offset 作为 Git 核心组件。
- 不会用“追加日志”替代 blob/tree/commit 对象模型。

### Evidence style
以 Git 的对象格式、pack 格式、fetch negotiation、reflog 与 shallow/partial clone 文档验证；用实际 clone/fetch/repack/fsck 行为检查重放和恢复边界。

## Lens: Raft CP
### On the decision point
Git 的本地 ref 更新不是 CP 集群元数据协调问题。单个仓库需要锁、旧值检查和后端事务语义来发布指针，但不需要所有仓库共享一个多数派 leader 才能 commit。远程 push 是另一仓库的发布策略，不是本地历史的线性化前提。

### Heuristics applied
- 先问失败是否是“两个权威同时写入同一控制面”；本地仓库之间没有共同的实时写入控制面。
- 把小而关键的元数据与高吞吐对象数据分开；refs 是发布元数据，blob/pack 是数据面。
- 明确超时后的不确定性；push 失败或非快进不应删除本地对象，应由用户重试、合并或改写。

### Risks / what they'd worry about
- 把远程中央仓库误认为 Git 的共识层，失去离线 commit 和多 remote 工作流。
- 把 ref 后端的锁/事务夸大成跨仓库多数派一致性。
- 把 pack、对象库或大文件放进一个假想的 quorum 控制面，造成错误容量和可用性模型。

### Would not do
- 不会为了保证分支唯一性给所有仓库加中央 Raft 服务。
- 不会把 push 的远程 ACL、非快进检查写成“Git 本地 commit 必须经过 leader 批准”。

### Evidence style
以 refs API、files/reftable 后端、receive-pack 更新路径和本地离线 commit 行为验证；若部署在托管平台，再单独验证宿主认证、ACL、高可用和 ref policy。

## 圆桌综合结论

两个席位都反对把 Git 套入“中央追加日志 + 多数派提交”的架构。主持人保留三条边界：

1. **逻辑真相：** 不可变内容寻址对象、tree 快照和多父 commit DAG。
2. **发布语义：** refs/HEAD 是可变命名和发布层；本地 commit 先成立，push/fetch 后发生。
3. **物理优化：** loose、pack、delta、MIDX、commit-graph、bitmap 和协议协商只优化存储/遍历/传输，不重定义逻辑历史。
4. **接口分层：** plumbing 原语承载对象、索引、refs 和传输机制，porcelain 命令把这些能力组合成用户工作流。

## 层 A — 叙事

### A1 摘要

Git 让贡献者在本地独立记录文件树历史，再按需与其他仓库交换历史。成功意味着断网也能 commit，分支可以廉价发散，merge 能表达多父关系，相同内容可复用，损坏或缺失对象能被发现。Git 不解决代码托管、审查、CI 或远程 ACL。

### A2 上下文与边界

工作树是可编辑状态；index 是下一次提交的候选状态；`.git` 中的对象库、refs、HEAD、reflog 和配置是仓库状态；远程仓库是交换和发布节点。对象哈希提供寻址和完整性，不提供身份认证或保密性。

### A3 主路径

修改工作树 → `git add` 写入或复用 blob 并更新 index → `git commit` 根据 index 写 tree 和 commit → 更新当前分支 ref → 需要分享时读取远程 refs、协商共同对象、发送 pack → 远程校验并更新 ref → 另一仓库 fetch/clone 后恢复对象和工作树。

### A4 组件与契约

| 组件 | 契约 |
|------|------|
| Working Tree | 可与历史不一致，承载未提交变化 |
| Index | 选择性暂存、冲突 stages、sparse 状态，不等于当前 commit |
| Object Database | blob/tree/commit/tag 逻辑不可变，由对象 ID 寻址 |
| Refs / HEAD / Reflog | 可变发布指针和恢复线索，分支不是目录复制 |
| Merge / Revision | 通过父指针和可达性处理发散、共同祖先和合并 |
| Transport | 交换 refs 和缺失对象，不改变对象身份 |
| Pack / Graph Index | 物理优化，不改变逻辑对象和历史语义 |
| Plumbing / Porcelain | 底层对象、索引、引用原语与面向用户的工作流命令分层；高层命令组合底层契约 |

### A5 状态、失败与恢复

工作树/index 不一致表现为未暂存或冲突；非快进 push 或 ref 条件失败不发布新 ref；对象校验失败或缺失必须显式报错；reflog、其他 remote、fsck 和仍未被 gc 的对象提供恢复路径。shallow/partial clone 的不完整性必须保留为显式边界。

### A6 安全与身份

对象 ID、pack/index 校验和接收检查提供完整性；远程认证、ref ACL、签名和 hooks 提供身份与授权。不能把哈希地址当作保密机制，也不能把远程仓库策略写成 Git 本地提交的安全边界。

### A7 演进切片

- **现在：** 对象寻址、快照 tree、commit DAG、refs/HEAD、index、离线 commit 和仓库间 push/fetch。
- **下一刀：** pack/repack、MIDX、commit-graph、bitmap、sparse-index、partial clone、协议协商和 reftable 后端。
- **明确不做：** 中央共识提交、线性修订号替代 DAG、分支整树复制、把 pack 当用户可见历史模型。

### A8 如何验收

1. 断网初始化、add、commit 成功，当前 ref 指向新 commit。
2. 两分支各自提交后 merge，结果 commit 有两个父节点。
3. 未改变的文件在不同 commit 中保持相同对象 ID。
4. 本地 commit 后 push 到 bare remote，另一仓库 clone 后 ref 与对象一致。
5. repack 后 fsck 通过；制造非快进、冲突和缺失对象时分别得到可观察失败态。

## 层 B — 机制与策略

### B1 基本事实

- **已证实：** Git 仓库分离工作树、index、对象库和 refs；完整本地仓库可离线形成历史。
- **已证实：** blob/tree/commit/tag 由对象 ID 寻址，tree 组织快照，commit 父指针组织历史。
- **已证实：** commit 可有多个父；refs/HEAD 是可变命名层；pack、index、commit-graph 和 bitmap 是优化层。
- **已证实：** fetch/push 通过 ref 广播、共同对象协商和 pack 交换；支持 shallow/partial 等不完整仓库边界。
- **待验证：** 具体托管平台的 ACL、认证、签名、容量、延迟和故障域策略。

### B2 机制

1. 内容寻址对象库。
2. 可复用的 blob/tree 快照。
3. 支持发散和合并的 commit DAG。
4. 轻量可变 refs/HEAD 发布层。
5. 工作树—index—对象库三态。
6. loose/pack/delta 和遍历索引的物理优化。
7. 面向缺失对象的仓库间差集同步。
8. ref 发布与对象回收分离。
9. plumbing / porcelain 分层：底层对象、索引、refs 和传输原语承载稳定机制；面向用户的命令组合成 add、commit、merge、push、fetch 等工作流。

### B3 策略选项

| 维度 | Git 选择 | 主要替代 |
|------|----------|----------|
| 内容 | DAG 快照，pack delta 仅作压缩 | delta changeset 主模型 |
| 历史 | 多父 DAG | 强制线性历史 |
| 分发 | 本地 commit、按需 push/fetch | 中央提交事务 |
| 暂存 | 独立 index | 工作树整体直接提交 |
| refs | files/reftable 后端 | 业务代码直接操作存储布局 |
| 完整度 | full/shallow/partial 按需选择 | 所有 clone 必须全量 |

### B4 取舍

选择内容寻址快照、历史 DAG、可变 refs、独立 index 和仓库间同步，是因为它同时满足离线工作、廉价分支、可解释合并、完整性和多发布面。代价是用户要理解 commit 与 push、index 与工作树、reflog 与 gc，以及不完整 clone 的边界；大仓库还需要 pack 和索引维护。

### B5 与对照的关系

- `log-stream` 席位的教训：追加和重放不是 Git 的全部真相；不能用消费 offset 或 broker 日志替代可寻址对象和 DAG。
- `raft-cp` 席位的教训：ref 更新需要局部锁/事务和发布策略，但 Git 的本地 commit 不需要跨仓库多数派；中央协调应留在托管平台边界。
- 中央线性 VCS 的教训：提交与公共发布拆开，换来离线与多仓库，代价是更高概念负担。

## 附录：证据基线与完成检查

- 官方仓库：`https://github.com/git/git`
- 检出提交：`5b24717`
- 关键证据：`Documentation/gitrepository-layout.adoc`、`gitformat-index.adoc`、`gitformat-pack.adoc`、`gitprotocol-v2.adoc`、`gitformat-commit-graph.adoc`、`technical/reftable.adoc`
- 实现入口：`repository.c`、`refs.c`、`read-cache.c`、`object-file.c`、`fetch-pack.c`、`send-pack.c`、`upload-pack.c`

| 检查项 | 结果 |
|--------|------|
| 问题与非目标清楚 | pass |
| 信任边界和主路径完整 | pass |
| 机制/策略分离且有圆桌合成 | pass |
| 失败语义和 5 条验收句 | pass |
| 演进切片与明确不做 | pass |
| 圆桌提议、用户同意、2 个透镜契约、综合结论 | pass |
