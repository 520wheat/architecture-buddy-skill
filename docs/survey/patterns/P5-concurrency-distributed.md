# Corpus P5 — 并发与分布式模式
- 阶段: Phase 3 · 2026-08-05
- 来源: Raft 论文（Ongaro/Ousterhout）；POSA Vol.2（Schmidt et al.）；与 D2 etcd/K8s 交叉
- 状态: 核心词汇齐备（E2 满足）

## A. 分布式共识 / 复制状态机（Raft）

### 问题类
一组机器作为**一致群体**工作，在部分成员失败时仍安全；典型实现是**复制日志 → 确定性状态机**。

### 机制
1. 共识模块维护复制日志；状态机按序执行相同命令 → 相同状态  
2. **强 Leader**：日志条目只从 leader 流向 follower（简化）  
3. 问题分解：Leader election / Log replication / Safety / Membership change  
4. 多数派可用即服务；非拜占庭；不靠时钟保证一致性（时钟差最多影响可用性）  
5. 成员变更用 **joint consensus**（两配置多数重叠）

### 策略（相对 Paxos）
| 策略 | Raft | Paxos 痛点（论文视角） |
|------|------|------------------------|
| 可理解性优先 | 分解 + 缩状态空间 | 难教难实现 |
| 以日志为中心 | 顺序追加 | single-decree 再拼日志更绕 |
| 强领导 | 先选主再协调 | 对称 peer 模型不便实践 |
| 随机超时选主 | 简单解决冲突 | — |

### 样本钩子
- etcd：Raft 复制组 + revision  
- 反面：把共识库当海量业务库（已在 etcd why）

### Buddy 问句
- 要的是 CP 元数据协调，还是 AP 业务数据？  
- 多数派延迟与分区行为团队能否接受？

---

## B. POSA Vol.2 — 并发与网络对象（17 模式）

### 四组

| 组 | 模式 | 问题类摘要 |
|----|------|------------|
| Service Access & Configuration | Wrapper Facade, Component Configurator, Interceptor, Extension Interface | 访问 OS/组件、可配置扩展 |
| Event Handling | **Reactor**, **Proactor**, Asynchronous Completion Token, **Acceptor-Connector** | 事件多路复用与连接角色分离 |
| Synchronization | Scoped Locking, Strategized Locking, Thread-Safe Interface, Double-Checked Locking | 锁策略与线程安全接口 |
| Concurrency | **Active Object**, Monitor Object, **Half-Sync/Half-Async**, **Leader/Followers**, Thread-Specific Storage | 并发执行模型 |

### 与 Phase1/2 样本对照
| 模式 | 样本 |
|------|------|
| Reactor / 事件循环 | Envoy Dispatcher；nginx event model |
| Half-Sync/Half-Async | 异步 I/O + 同步工作线程分层 |
| Leader/Followers | 线程池轮流等事件（对照 Envoy multi-worker 差异要讲清） |
| Active Object | 队列化方法执行（对照 actor/agent 循环，勿混） |
| Acceptor-Connector | 连接建立与处理解耦 |
| Interceptor / Extension Interface | Envoy filter；Caddy modules |

### Buddy 使用规则
- 网络服务性能架构：先 POSA2 事件/并发组，再谈业务分层（POSA1）  
- Agent 的「循环」≠ Active Object，需分清问题类  

## 对 Architecture Buddy 策略表的直接条目
- 分布式协调：Replicated State Machine + Raft/Paxos 族  
- 数据面：Reactor / Proactor / Half-Sync-Half-Async / 多 worker shared-nothing  
