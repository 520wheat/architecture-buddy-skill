# Corpus P2 — POSA1 其余五模式深挖（短文）
- 阶段: Phase 4 · 2026-08-05
- 配套: `P2-posa-vol1-index.md`、`P2-posa-deep-three.md`（Layers / Pipes-Filters / Microkernel）
- 来源: Buschmann et al. POSA Vol.1（公开目录/经典综述交叉；非全书摘录）

每模式：Context → Problem → Forces → Solution 要旨 → Consequences → Buddy 钩子

---

## Blackboard

| 项 | 内容 |
|----|------|
| Context | 问题无法由单一算法可靠求解；需多种专业知识协作 |
| Problem | 如何组织机会主义的、数据驱动的协作求解？ |
| Forces | 灵活性 vs 控制流可读性；渐进求解 vs 性能可预期 |
| Solution | 共享黑板 + 知识源 + 控制器；知识源看黑板状态自发贡献 |
| Consequences | 易探索不确定域；调试难、性能难料、控制策略成关键 |
| Buddy | Agent 规划/多专家时可对照；默认警告「别把普通工作流做成黑板」 |
| 层级 | 架构 |

## Broker

| 项 | 内容 |
|----|------|
| Context | 分布式组件需定位、激活、通信 |
| Problem | 如何让客户端不绑死服务器位置与通信细节？ |
| Forces | 解耦与位置透明 vs 间接层延迟与故障域 |
| Solution | 经纪人负责注册、查找、转发/中介；客户端经 Broker 交互 |
| Consequences | 可演化拓扑；Broker 成单点/瓶颈；需冗余与超时策略 |
| Buddy | K8s API Server、服务发现偏此族；**不等于** Raft 共识——勿混名 |
| 层级 | 架构 |

## Model-View-Controller (MVC)

| 项 | 内容 |
|----|------|
| Context | 交互式系统；同一模型多表现、用户输入频繁 |
| Problem | 如何分离模型与表现并保持同步？ |
| Forces | 多视图一致性 vs 更新风暴与复杂度 |
| Solution | Model 持数据与规则；View 展示；Controller 处理输入并协调 |
| Consequences | 可测模型、多 UI；错误接线导致通知循环 |
| Buddy | 与 PoEAA Web MVC 同名；架构笔记标「交互分离」，企业 Web 细节见 P3 |
| 层级 | 架构（企业交叉） |

## Presentation-Abstraction-Control (PAC)

| 项 | 内容 |
|----|------|
| Context | 大型交互系统，多协作代理层次 |
| Problem | 如何让 UI 代理局部自治又组成层次结构？ |
| Forces | 局部自治 vs 整体一致性；比 MVC 更重的结构税 |
| Solution | 每个 PAC Agent = Presentation + Abstraction + Control；树状协作 |
| Consequences | 适合复杂多代理 UI；过重则不如 MVC |
| Buddy | 多 agent「人机界面壳」对照用；默认不推荐中小 Web |
| 层级 | 架构 |

## Reflection

| 项 | 内容 |
|----|------|
| Context | 需在运行时调整结构或行为（开放实现） |
| Problem | 如何在不改客户端的前提下改变实现策略？ |
| Forces | 极度灵活 vs 可理解性/安全/性能 |
| Solution | 元层 + 基层；元对象协议调整基层行为 |
| Consequences | 插件/热更新强大；难推理、攻击面大 |
| Buddy | 动态配置、热加载扩展点时点名；写入 M7 安全与可理解性风险 |
| 层级 | 架构 |

## 对活表的增量
- Broker ≠ 共识；Reflection 默认带安全风险标签
- Blackboard / PAC：高成本模式，适用条件必须写进策略表
