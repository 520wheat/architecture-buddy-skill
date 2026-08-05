# LangGraph — Overview + Designing an Agent Runtime
- 域: D8 Agent / 智能体系统
- 来源: https://docs.langchain.com/oss/python/langgraph/overview · https://www.langchain.com/blog/building-langgraph
- 阶段: Phase 1 · 2026-08-05

## 问题类
为**长时、有状态、可循环**的 agent/工作流提供生产级编排运行时：在确定性步骤与模型驱动步骤之间精细控制，并处理延迟、失败重试与不确定性。

## 硬约束（相对传统软件的差异）
- 延迟以秒/分钟计，需并行与流式改善体验
- 长任务失败后从头重跑昂贵 → 需 checkpoint
- 非确定性 → 需 HITL、追踪、审批
- 图可以是**有环**的（DAG 框架不够）
- 步骤间额外延迟不可接受（聊天场景）

## 机制（共性）
1. **低层图运行时**：State + Nodes + Edges；少抽象提示/架构
2. **确定性步骤与 agentic 步骤可混布同一图**
3. **持久化 / Checkpoint**：中间状态可恢复，支撑重试与中断
4. **Human-in-the-loop**：任意点中断/恢复/改状态
5. **流式 + 并行**（含避免数据竞争）
6. **任务队列**解耦触发与执行
7. 灵感：Pregel / Beam；接口气质像 NetworkX

## 策略（差异/选项）— 相对 Anthropic 模式文
| 点 | Anthropic | LangGraph |
|----|-----------|-----------|
| 焦点 | 何时用何种工作流/agent 模式 | 生产运行时能力（耐久、HITL、流） |
| 抽象 | 模式可手写几行 API | 刻意低抽象；控制与耐久优先于上手容易 |
| 何时不需要框架 | 单次 LLM 足够 | 短 agent、无工具、单提示 → 可能不需要 LangGraph |
| 与旧基础设施 | — | DAG 框架缺环；Temporal 类缺流式/步进延迟 |

## 显式模式名 / 能力词汇（并入 P9）
- Checkpointing、Streaming、Parallelization、HITL、Task Queue、Tracing
- Cyclic graph orchestration（相对 DAG）
- Mix deterministic + agentic steps

## 决策与负面后果
- 为生产就绪牺牲「最容易上手」
- 仍需上层（LangChain agents / Deep Agents harness）才有更高抽象

## 对写作规范的启示
- 先问「agent 与传统软件差在哪」再列机制——问题驱动
- 用「排除候选框架的理由表」写策略（M5 范本）
