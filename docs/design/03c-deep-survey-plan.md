# 深调研计划：多领域架构洞见 × 模式文献库

## Status

**Phase 3 完成（E1–E4）**；§3 已 Approved。Phase 4 为自主加深（ADR-0013），不阻塞设计推进。

## 目标

在「机制 vs 策略」框架下，建立足够厚的、可复查的学习资产，使 Architecture Buddy：

1. 知道优秀架构描述**通常写什么、怎么写**（跨领域共性 = 机制）
2. 知道各领域/模式库提供哪些**可命名策略**与适用边界
3. 能帮助使用者与作者持续学习，而不是复述两三篇范文

## 退出标准（何时才允许批准 §3）

同时满足：

| # | 标准 |
|---|------|
| E1 | **架构样本**：至少覆盖 **8 个问题域（D1–D8）**；D1–D6、D8 每域 ≥ **2** 篇；**D7 安全 ≥ 3** 篇（合计 ≥ 17）。书单见 `docs/survey/READING-LIST.md`（Locked） |
| E2 | **模式文献**：至少完成 **5 个模式 corpus（P1–P5）** 的结构化笔记；并维护 **P9 Agent 模式词汇**（可从 D8 抽取，不要求独立成书） |
| E3 | 产出三张活表：`机制表`、`策略/模式词汇表`、`反模式与写作禁忌`（随调研更新） |
| E4 | 用活表回写 §3；若与 M1–M8 冲突则修订骨架并记 ADR |

首轮 `03b`（nginx / HSC / PoEAA 浏览）**不计**入 E1/E2 的完成数，只作种子。

---

## 轨 A：多领域架构样本（问题域清单）

每域选取「作者讲清为何、有取舍、可迁移」的材料；优先 AOSA、官方 architecture 文档、高质量 ADR 集、经典系统论文级设计综述。

| 域 ID | 问题域 | 候选样本方向（待填具体篇目） | 最少篇数 |
|-------|--------|------------------------------|----------|
| D1 | Web / 边缘与接入 | AOSA nginx；Caddy/Envoy/其他反向代理或网关架构文 | 2 |
| D2 | 分布式协调与集群 | 如 etcd/ZooKeeper/Consul；Kubernetes 控制面设计文 | 2 |
| D3 | 数据存储与查询 | 如 SQLite/Berkeley DB/Postgres/LevelDB 类架构叙述；AOSA 数据库章 | 2 |
| D4 | 消息与流式 | 如 Kafka/Pulsar/NATS 设计；EIP 所服务的问题类实例 | 2 |
| D5 | 语言运行时 / 编译 / 工具链 | 如 V8/JVM 概述、LLVM、Git（内容寻址）AOSA 章 | 2 |
| D6 | 应用与平台架构 | 如 Django/Rails；arc42/ADR 集 | 2 |
| D7 | **安全架构（必做）** | 零信任、SAMM Secure Architecture、ASVS 等，**≥3**，禁止单篇代表整域 | 3 |
| D8 | **Agent / 智能体系统（必做）** | Anthropic 有效 agent 模式、LangGraph runtime、另一家编排对照等，**≥3** | 3 |

**记录模板**（每篇一篇短记，存 `docs/survey/architecture/`）：

```markdown
# <标题>
- 域: D?
- 问题类:
- 硬约束:
- 机制（共性）:
- 策略（差异/选项）:
- 显式模式名:
- 决策与负面后果:
- 对写作规范的启示:
- 来源 URL:
```

---

## 轨 B：模式文献 corpus

| Corpus ID | 文献 / 体系 | 阅读产出要求 |
|-----------|-------------|--------------|
| P1 | GoF *Design Patterns* | 按创建（创建/结构/行为）各提炼：典型问题类、力、后果；标注「架构笔记中的默认层级=细粒度」 |
| P2 | POSA（至少 Vol.1 架构模式全集要点；Vol.2/4 按需） | 每个架构模式：问题类、结构、后果；标为 M5 优先词汇 |
| P3 | Fowler *PoEAA* | 按章/模式族（领域逻辑、数据源、Web、并发…）做策略对照表 |
| P4 | Hohpe *Enterprise Integration Patterns* | 消息通道/路由/转换等：问题类与模式目录 |
| P5 | 并发与分布式模式（如 *POSA Vol.2*、Lea、或 *Distributed Systems* 常用模式综述） | 与 D2/D4 交叉验证 |
| P6（扩展） | UI 架构模式（MVC/MVP/MVVM…）、OSS 架构风格综述（Richards/Ford） | 按需 |

**记录模板**（每 corpus 一份，存 `docs/survey/patterns/`）：

```markdown
# Corpus <P?>
## 覆盖范围
## 模式索引表（名 | 问题类 | 力 | 关键后果 | 层级）
## 与其他 corpus 的重叠/冲突
## 对 Architecture Buddy 策略表的直接条目
```

---

## 活表（调研中维护）

路径：`docs/survey/living/`

| 文件 | 内容 |
|------|------|
| `mechanisms.md` | 跨域稳定出现的写作与思考机制（可修正 M1–M8） |
| `strategies-and-patterns.md` | 可命名策略/模式词汇 + 适用条件 + 代价 |
| `anti-patterns-and-writing-rules.md` | 反模式；架构笔记不该怎么写 |

---

## 分期建议

| 期 | 内容 | 产出 |
|----|------|------|
| Phase 1 | D1–D3 开工包 + D7/D8 各开篇 1 篇 + P2/P3 骨架（见 READING-LIST Phase 1） | 活表 v0.1 |
| Phase 2 | D4–D6 补齐 + D7/D8 补到 ≥3 + P1/P4 | 活表 v0.2 |
| Phase 3 | P5 + P9 + 缺口回填；修订 M1–M8 | 活表 v1.0 → 回写 §3 |

每期结束做一次短复盘（机制有无增减），再开下一期。

## 与首轮 `03b` 的关系

`03b` = 种子假说。深调研可以**推翻或改写**其中条目；冲突时以活表与新 ADR 为准。
