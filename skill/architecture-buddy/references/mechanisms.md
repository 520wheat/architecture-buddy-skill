# Mechanisms (runtime cheat sheet)
Source: docs/survey/living/mechanisms.md — compressed for skill runtime.
User-visible authority is templates/architecture-deliverable.md (dual layer A/B).
M1–M9 below are internal mapping only; see references/note-mapping.md.
Do not invent new M numbers; do not put M numbers in user-facing deliverable body.

## 映射到笔记锚点（M）

| M | 名称 | 合并自 K | 含义（一句话） |
|---|------|----------|----------------|
| M1 | 问题类与边界 | K1 | 先定义一类问题与非目标 |
| M2 | 干系人与关注点 | K2 部分 | 谁在乎什么（含安全关注点） |
| M3 | 约束与假设 | K2, K7 相关 | 硬约束 + **一致性/信任假设**（显性） |
| M4 | ASR / 质量目标 | K3, K11, K12 | 场景化质量目标；可引用 ASVS 类检查清单 |
| M5 | 机制与策略 | K4, K5, K7, K10, K13–K19 | 共性机制 vs 可选项；优先公共模式名；常出现控制面/数据面或元数据/数据分离 |
| M6 | 决策与理由 | K6 | Context / Options / Decision / Consequences |
| M7 | 权衡、风险、未决 | K6, K16 | 含负面后果、敏感点、推迟项 |
| M8 | 证据与学习痕迹 | K8, K9 | Top N、圆桌、canon、Design Lessons、When not |
| M9 | 模式词汇层级 | K5, K19 + P1–P5/P9 | 架构/企业/集成/并发分布式优先；GoF 默认细粒度 |

## 机制明细（去重后）

| ID | 机制 | 关键证据 |
|----|------|----------|
| K1 | 问题类与非目标先行 | etcd 对照；HDFS；Anthropic when not |
| K2 | 信任/威胁/一致性假设显性化 | ZTA；etcd CP；Envoy threat model |
| K3 | 质量与规模场景化 | HDFS 40PB；Agent 成本/延迟 |
| K4 | 机制 vs 策略分离 | K8s variations；Agent 模式族 |
| K5 | 公共模式命名 | POSA/PoEAA/EIP/Raft |
| K6 | 决策含负面后果 | etcd lock；DT ADR；BDB 演进 |
| K7 | 控制面·数据面 / 元数据·数据分离 | K8s；HDFS；Envoy；Pulsar |
| K8 | When not / Design Lessons | Anthropic；BDB；LLVM |
| K9 | 组织参考架构与可验证清单 | SAMM；ASVS |
| K10 | 配置不可变/原子替换 | Caddy |
| K13 | 日志型消息（追加+保留+位点） | Kafka |
| K14 | Serving 与持久存储分离 | Pulsar |
| K15 | 内容寻址 / DAG | Git |
| K16 | 避免过重中间件 | Dependency-Track |
| K17 | 一等 IR 枢纽 | LLVM |
| K20 | 可理解的共识分解（选主/复制/安全） | Raft |
| K21 | 事件驱动并发模型族（Reactor 等） | POSA2；Envoy |
| K22 | 逻辑组件 vs 部署模型分离（安全） | NIST ZTA PE/PA/PEP vs Agent/Enclave/Portal |
| K23 | 框架哲学清单承载机制、子系统表承载策略 | Django design philosophies |
| K24 | 嵌入式存储：编译→VM→页缓存→VFS | SQLite |

## 已否决的膨胀
- 不把每个领域特性都升格为新 M（如「IR」留在 M5 策略/机制条目）
- GoF 不单独占 M；归 M9 细粒度层
