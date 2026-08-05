# OpenAI Agents SDK（Swarm 继任）
- 域: D8 Agent / 智能体系统
- 来源: https://openai.github.io/openai-agents-python/ · Swarm README（已指向 SDK）
- 阶段: Phase 1 收官 / Phase 2 交界 · 2026-08-05

## 问题类
用**少量原语**构建可协调多 agent、带护栏与可观测的生产级 agentic 应用；相对「自管循环的 Responses API」提供更高层运行时。

## 硬约束 / 设计原则
1. 功能够用但原语够少，学习曲线平缓
2. 开箱可用，又可精细定制
3. Swarm 为实验教育向；**生产应迁移到 Agents SDK**（官方明确）

## 机制（共性）
1. **Agents**：指令 + 工具 + 内置循环直至任务完成
2. **Handoffs / Agents-as-tools**：委托与协调
3. **Guardrails**：输入/输出校验，可与执行并行，失败快速中止
4. **Sessions**：循环内工作上下文持久
5. **Tracing**：内建轨迹，对接评估/微调
6. **HITL / Sandbox / Realtime** 等专用形态（工作区隔离、语音等）
7. **Python-first 编排**：少新 DSL，多用语言本身

## 策略（差异/选项）
| 策略 | 何时 | 对照 |
|------|------|------|
| Responses API 直连 | 短流程、自管循环/工具/状态 | Anthropic「先 API」；LangGraph「短 agent 可不需要框架」 |
| Agents SDK | 需托管回合、工具、护栏、handoff、session、产物多步 | 比 Swarm 多护栏/追踪/session |
| Swarm（遗留） | 仅学习 handoff 思想 | 非生产路径 |
| Sandbox agents | 需真实文件系统/可恢复长任务工作区 | 对齐 LangGraph 耐久/工作区问题 |

## 与 Anthropic / LangGraph 三方对照（D8 齐套）
| 维度 | Anthropic | LangGraph | OpenAI Agents SDK |
|------|-----------|-----------|-------------------|
| 焦点 | 模式 when/when not | 图运行时耐久/HITL/流 | 少原语 + 护栏/handoff/追踪 |
| 多 agent | Orchestrator-workers 等 | 图节点组合 | Handoff / agents-as-tools |
| 生产叙事 | 简单可组合 | 控制与耐久优先 | Swarm→SDK 演进 |

## 显式模式名（并入 P9）
- Handoff、Guardrail、Session、Agent loop、Sandbox agent

## 对 Buddy
D8 共思默认三角：模式选型（Anthropic）× 运行时能力（LangGraph）× 原语/护栏产品化（OpenAI SDK）；并问是否 Responses/单次调用已够。
