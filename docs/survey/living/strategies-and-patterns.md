# 活表：策略与模式词汇 v1.0

## 按问题域（策略分叉速查）

| 域 | 典型策略分叉 |
|----|----------------|
| D1 接入 | nginx 系边缘高效 vs Envoy 网格可编程 vs Caddy 少部件+原子配置 |
| D2 协调 | etcd vs ZooKeeper（KV/gRPC vs znode/watch/ephemeral）；K8s 声明式调和；Consul 仍可补 |
| D3 存储 | 嵌入式库（SQLite/BDB）vs 服务；NN/DN 分离+副本 vs RAID；SQL→字节码→VM 路径 |
| D4 消息 | Kafka 统一日志总线 vs Pulsar 存算分离；应用内 Postgres 编排（反过度中间件）；EIP 路由五件套 |
| D5 工具链 | Git DAG 分布式；LLVM IR 库式 vs GCC 单体 vs JVM 固定运行时 |
| D6 应用平台 | arc42+ADR 决策链；Django 哲学（松耦合/DRY/显式）；Active Record vs 富领域 |
| D7 安全 | 零信任 vs 边界；ZTA 三部署（Agent-Gateway / Enclave / Portal）× 三驱动；SAMM；ASVS |
| D8 Agent | 工作流 vs 自治 agent；LangGraph vs OpenAI 编排；**MCP = 工具/上下文集成面**（非编排）；先问是否需要 agentic |

## 模式 corpus 入口

| ID | 文件 | Buddy 默认层级 |
|----|------|----------------|
| P1 GoF | `patterns/P1-gof-index.md` | 细粒度 |
| P2 POSA1 | `patterns/P2-posa-vol1-index.md` + deep-three | 架构 |
| P3 PoEAA | `patterns/P3-poeaa-families.md` | 企业 |
| P4 EIP | `patterns/P4-eip-core.md` | 集成 |
| P5 并发分布式 | `patterns/P5-concurrency-distributed.md` | 架构/中间件 |
| P9 Agent | `patterns/P9-agent-patterns-seed.md` | 领域模式（Agent） |

## M5 策略表列约定
`策略或模式 | 层级(架构/企业/集成/并发分布式/Agent/细粒度) | 适用条件 | 代价 | 状态`
