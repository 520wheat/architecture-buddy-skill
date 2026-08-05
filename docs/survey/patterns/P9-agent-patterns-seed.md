# Corpus P9 — Agent 模式词汇（种子，从 D8 抽取）
- 阶段: Phase 1 · 2026-08-04
- 来源: Anthropic Building Effective Agents；后续对齐 LangGraph / OpenAI
- 状态: 种子表；Phase 2 用 LangGraph/OpenAI 校准

| 模式名 | 问题类 | 力 / 适用 | 后果 | 来源 |
|--------|--------|-----------|------|------|
| Augmented LLM | 单步智能增强 | 工具/检索/记忆接口清晰 | 仍非多步自治 | Anthropic |
| Prompt Chaining | 固定多步流水线 | 可分解子任务 | 延迟↑ | Anthropic |
| Routing | 分流专业化 | 分类可靠 | 分错则错 | Anthropic |
| Parallelization | 并行或投票 | 独立子任务/需共识 | 费用↑ | Anthropic |
| Orchestrator-Workers | 动态分解委托 | 子任务不可预知 | 编排复杂 | Anthropic |
| Evaluator-Optimizer | 可评价的迭代打磨 | 有清晰标准 | 多轮成本 | Anthropic |
| Autonomous Agent | 开放式多轮工具环 | 信任+沙箱+停止条件 | 成本与复合错误 | Anthropic |
| Workflow vs Agent（元区分） | 选复杂度 | 可预测 vs 灵活 | 选错浪费或失控 | Anthropic |
| ACI（Agent-Computer Interface） | 工具契约设计 | 如 HCI 同等投入 | 工具难用→整系统失败 | Anthropic |

## 写作规则（进反模式表）
- 先问是否需要 agentic；多数时候单次 LLM+RAG 足够
- 每个模式必须写 when/when not

## Phase 1 增补（LangGraph）
| 模式/能力 | 问题类 | 力 | 后果 | 来源 |
|-----------|--------|----|------|------|
| Cyclic graph runtime | 需循环的 agent 图 | DAG 不够 | 需专用运行时 | LangGraph |
| Checkpointing | 长任务失败重试 | 重头跑昂贵 | 持久化与恢复复杂度 | LangGraph |
| Streaming | 感知延迟 | 真延迟难再降 | 需流协议与 UX | LangGraph |
| HITL interrupt/resume | 非确定性需人审 | 开放式输入输出 | 产品与状态设计 | LangGraph |
| Mix deterministic+agentic | 可靠与灵活并存 | 全 LLM 不可控 | 图设计纪律 | LangGraph |
| Task queue | 触发与执行解耦 | 减少一类失败 | 运维面 | LangGraph |

## Phase 2 增补（OpenAI Agents SDK）
| 模式/能力 | 问题类 | 力 | 后果 | 来源 |
|-----------|--------|----|------|------|
| Handoff | 多 agent 委托 | 专业化分工 | 边界与上下文过滤 | OpenAI SDK |
| Guardrail | 输入输出安全/策略 | 需 fail-fast | 并行校验设计 | OpenAI SDK |
| Session | 跨回合工作记忆 | 自管历史成本高 | 与存储后端耦合 | OpenAI SDK |
| Sandbox agent | 隔离工作区长任务 | 文件/环境真实 | 基础设施依赖 | OpenAI SDK |
| Responses API vs SDK | 选抽象层 | 短 vs 托管循环 | 可混用 | OpenAI SDK |
