# 深调研书单（Locked）

## Status

**Locked（2026-08-04）** — 按 ★ 默认建议采纳；D7 安全升为必做且多样本；新增 **D8 Agent**。

标记含义：`[必读]` / `[可换]` / `[已有]` / `[扩展]`

退出标准见 `docs/design/03c-deep-survey-plan.md`（已同步：D7/D8 计入必做域）。

---

## 轨 A：架构样本

### D1 · Web / 边缘与接入（≥2 新篇）

| 标记 | 条目 | URL |
|------|------|-----|
| `[已有]` | AOSA nginx（复查） | https://aosabook.org/en/v2/nginx.html |
| `[必读]` | Envoy architecture overview | https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/arch_overview |
| `[必读]` | Caddy architecture | https://caddyserver.com/docs/architecture |

### D2 · 分布式协调与集群（≥2）

| 标记 | 条目 | URL |
|------|------|-----|
| `[必读]` | etcd learning docs | https://etcd.io/docs/latest/learning/ |
| `[必读]` | Kubernetes cluster architecture | https://kubernetes.io/docs/concepts/architecture/ |
| `[可换]`→`[已读]` | ZooKeeper Overview | https://zookeeper.apache.org/doc/current/zookeeperOver.html |
| `[可换]` | Consul architecture | https://developer.hashicorp.com/consul/docs/architecture |

### D3 · 数据存储与查询（≥2）

| 标记 | 条目 | URL |
|------|------|-----|
| `[必读]` | AOSA Berkeley DB | https://aosabook.org/en/v1/bdb.html |
| `[必读]` | AOSA HDFS | https://aosabook.org/en/v1/hdfs.html |
| `[可换]`→`[已读]` | SQLite Architecture | https://www.sqlite.org/arch.html |

### D4 · 消息与流式（≥2）

| 标记 | 条目 | URL |
|------|------|-----|
| `[必读]` | Kafka design | https://kafka.apache.org/documentation/#design |
| `[必读]` | Pulsar architecture overview（与 Kafka 对照） | https://pulsar.apache.org/docs/concepts-architecture-overview/ |
| `[可换]` | NATS concepts/overview | https://docs.nats.io/nats-concepts/overview |
| `[可换]` | RabbitMQ docs（可靠性/路由模型） | https://www.rabbitmq.com/docs |

### D5 · 语言运行时 / VCS / 工具链（≥2）

| 标记 | 条目 | URL |
|------|------|-----|
| `[必读]` | AOSA Git | https://aosabook.org/en/v2/git.html |
| `[必读]` | AOSA **LLVM**（已锁定） | https://aosabook.org/en/v1/llvm.html |
| `[可换]` | V8 / JVM 公认架构综述（开读时选定 URL） | — |

### D6 · 应用与平台架构（≥2）

| 标记 | 条目 | URL |
|------|------|-----|
| `[已有]`→`[必读]` | arc42 HTML Sanity Checker（深读 Strategy + Decisions） | https://hsc.aim42.org/arc42/hsc_arc42.html |
| `[必读]` | Dependency-Track ADR 集（已锁定） | https://github.com/DependencyTrack/dependency-track/tree/main/docs/adr |
| `[可换]`→`[已读]` | Django design philosophies | https://docs.djangoproject.com/en/stable/misc/design-philosophies/ |

### D7 · 安全架构（必做，≥3 — 不能只看一篇）

安全是独立问题域：威胁模型、信任边界、身份/授权、纵深防御、零信任等，需多样本对照机制/策略。

| 标记 | 条目 | 说明 | URL |
|------|------|------|-----|
| `[必读]` | **NIST SP 800-207 Zero Trust Architecture** | 零信任问题类与逻辑组件 | https://csrc.nist.gov/pubs/sp/800/207/final |
| `[必读]` | **OWASP SAMM · Secure Architecture**（及 Design 相关 practice） | 安全架构能力与参考架构成熟度 | https://owaspsamm.org/model/design/secure-architecture/ |
| `[必读]` | **OWASP ASVS**（架构相关章）或 **OWASP Application Security Verification** 中架构要求综述 | 可验证的安全架构要求清单气质 | https://owasp.org/www-project-application-security-verification-standard/ |
| `[可换]` | NIST SP 800-204 / 微服务安全 或同等 | 云原生服务安全对照 | （开读时锁定） |
| `[可换]` | 经典威胁建模（STRIDE/PASTA 综述）+ 一份落地架构案例 | 威胁模型如何驱动架构 | （开读时锁定） |
| `[扩展]` | 密钥管理 / PKI 参考架构长文 | 专项加深 | — |

### D8 · Agent / 智能体系统架构（必做，≥3）

近年高速演化的问题类：工具增强 LLM、工作流 vs 自治、编排、记忆、人机环、可观测与护栏。需多来源，避免只跟一家框架。

| 标记 | 条目 | 说明 | URL |
|------|------|------|-----|
| `[必读]` | **Anthropic · Building Effective Agents** | 工作流模式与自治 agent 的问题类划分 | https://www.anthropic.com/engineering/building-effective-agents |
| `[必读]` | **LangGraph · Building LangGraph（设计原则）** + Graph API/Overview | Agent runtime：状态、持久化、HITL | https://www.langchain.com/blog/building-langgraph · https://docs.langchain.com/oss/python/langgraph/overview |
| `[必读]` | **OpenAI · Agents / Swarm 或 Agents SDK 设计叙述**（开读时锁定现行官方文） | 另一家的编排与切换策略对照 | https://openai.com/index/swarm/ （若失效则换现行 Agents 文档） |
| `[可换]` | AutoGen / Semantic Kernel 架构概述 | 多 agent 协作另一策略 | （开读时锁定） |
| `[可换]`→`[已读]` | MCP（Model Context Protocol）架构概述 | 工具/上下文集成边界 | https://modelcontextprotocol.io/docs/concepts/architecture |
| `[扩展]` | 生产 agent 系统公开复盘（可观测、评估、护栏） | 证据与反模式 | — |

---

## 轨 B：模式文献 corpus

| 标记 | ID | Corpus | 阶段 |
|------|-----|--------|------|
| `[必读]` | **P2** | POSA Vol.1 架构模式（逐模式索引表） | Phase 1 |
| `[必读]` | **P3** | PoEAA（按模式族对照；领域逻辑+数据源+Web 先完成） | Phase 1 |
| `[必读]` | **P1** | GoF（按创建；层级=细粒度） | Phase 2 |
| `[必读]` | **P4** | EIP（与 D4 交叉） | Phase 2 |
| `[必读]` | **P5** | 并发/分布式模式（POSA Vol.2 或等价 + 与 Raft 等对照） | Phase 2–3 |
| `[扩展]` | P6 | Richards & Ford 架构风格章 | — |
| `[扩展]` | P7 | UI 架构模式综述 | — |
| `[扩展]` | P8 | POSA Vol.4/5 或 Release It! 稳定性格局 | — |
| `[扩展]` | **P9** | Agent 模式小册（从 D8 样本抽「agent 模式词汇」；可与 Anthropic 模式表对齐） | 与 D8 并行维护 |

---

## Phase 1 开工包（Locked）

**架构样本（新读）**
1. Envoy architecture overview  
2. etcd learning docs  
3. Kubernetes cluster architecture  
4. AOSA Berkeley DB  
5. AOSA HDFS  
6. NIST SP 800-207（安全开篇）  
7. Anthropic Building Effective Agents（Agent 开篇）  

**复查（不计新篇额度，但写差分笔记）**  
- AOSA nginx；HSC arc42  

**模式**
1. POSA Vol.1 架构模式索引表起步  
2. PoEAA：领域逻辑 + 数据源 + Web 三族对照表  

**Phase 1 结束检查**：活表 v0.1；D1–D3 进度过半；D7/D8 已启动；P2/P3 有实质条目。

---

## 变更记录

| 日期 | 变更 |
|------|------|
| 2026-08-04 | 初稿草案 |
| 2026-08-04 | Locked：采纳全部 ★；D7 安全必做且 ≥3；新增 D8 Agent ≥3 |
