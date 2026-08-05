# Corpus P2 — POSA Vol.1 架构模式索引（起步）
- 阶段: Phase 1 · 2026-08-04
- 来源: Buschmann et al., *Pattern-Oriented Software Architecture Vol.1*（公开目录/综述交叉验证）
- 状态: 骨架已建；逐模式「力/后果」深挖在后续迭代补全

## 覆盖范围
POSA1 八个 **Architectural Patterns**（另有设计模式与惯用法层，本文件只收架构层）。

## 模式索引表

| 模式 | 问题类（摘要） | 关键力 | 关键后果 / 代价 | 层级 | Phase1 样本对照 |
|------|----------------|--------|-----------------|------|-----------------|
| Layers | 按抽象层次分解系统 | 可改性 vs 性能穿透 | 层泄漏、过量层 | 架构 | BDB 子系统；K8s API 分层 |
| Pipes and Filters | 流式分步变换数据 | 可重组 vs 共享状态难 | 批处理开销、错误处理复杂 | 架构 | Envoy filter chain |
| Blackboard | 多知识源协作求解不确定问题 | 机会主义协作 vs 控制流难懂 | 调试难、性能难料 | 架构 | （Agent 规划黑板可对照，慎用） |
| Broker | 分布式对象/服务定位与通信 | 解耦 vs 间接与单点 | 延迟、经纪失效 | 架构 | K8s API Server；服务发现 |
| Model-View-Controller | 交互系统分离模型与表现 | 多视图一致性 vs 复杂度 | 更新风暴 | 架构 | （D6 UI 再深挖） |
| Presentation-Abstraction-Control | 多 Agent 层次交互 UI | 局部代理自治 | 比 MVC 更重 | 架构 | 与多 agent UI 对照 |
| Microkernel | 最小核心 + 可插拔扩展 | 适应性 vs 核心设计难度 | IPC/扩展机制成本 | 架构 | Envoy 扩展；HSC 插件 |
| Reflection | 开放实现/可调整结构行为 | 极度灵活 vs 复杂脆弱 | 难理解、安全风险 | 架构 | 动态配置/热更新相关 |

## 分类（POSA1）
- From Mud to Structure: Layers, Pipes and Filters, Blackboard
- Distributed Systems: Broker（+ 他章交叉）
- Interactive Systems: MVC, PAC
- Adaptable Systems: Microkernel, Reflection

## 对 Architecture Buddy 策略表的直接条目
- 默认优先用上表架构模式名命名 M5 机制/策略
- Envoy → Pipes and Filters + Microkernel 扩展点
- etcd/K8s → Broker（API）+ 共识（P5 再补）不完全等于 POSA Broker，需注明「分布式协调」特化

## 下一步
为每一模式补：完整 Context/Problem/Forces/Solution/Consequences 短文（各 ≤1 页笔记）
