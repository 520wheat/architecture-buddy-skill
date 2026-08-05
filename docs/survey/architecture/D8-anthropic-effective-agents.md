# Anthropic — Building Effective Agents
- 域: D8 Agent / 智能体系统
- 来源: https://www.anthropic.com/engineering/building-effective-agents
- 阶段: Phase 1 · 2026-08-04

## 问题类
用 LLM + 工具/检索/记忆构建**能完成多步任务的 agentic 系统**；在简单调用、工作流、自治 agent 之间选择合适复杂度。

## 硬约束
- 默认选最简单能用的方案；复杂度必须由评测证明值得
- Agent 用延迟与成本换表现；需明确何时划算
- 工具接口（ACI）与提示同等重要

## 机制（共性）
1. **增强型 LLM** 为基本积木（tools / retrieval / memory）
2. **工作流 vs Agent** 二分：预定义代码路径 vs 模型动态主导
3. **可组合模式族**（见策略）而非唯一框架
4. **环境反馈闭环**（工具结果、测试）作为 ground truth
5. **透明规划 + 护栏/停止条件**

## 策略（差异/选项）— Agent 模式词汇（种子 → P9）
| 模式 | 何时用 | 代价 |
|------|--------|------|
| Prompt chaining | 可干净拆成固定子任务 | 延迟↑换准确 |
| Routing | 类别清晰、需分流优化 | 依赖分类质量 |
| Parallelization（sectioning/voting） | 可并行或需多视角 | 费用↑ |
| Orchestrator-workers | 子任务事先不可预测 | 编排复杂度 |
| Evaluator-optimizer | 有清晰评价标准、可迭代改进 | 多轮成本 |
| Autonomous agent | 开放式、难硬编码路径 | 成本与复合错误风险最高 |
| （更简单）单次 LLM+RAG | 多数应用足够 | — |

## 显式模式名
上文模式表；另强调 MCP 作为工具生态集成策略之一。

## 决策与负面后果
- 框架易掩盖提示与增加不必要复杂度；建议先 API 直连
- Agent 需沙箱与护栏；人机检查点

## 对写作规范的启示
- **When / when not** 专节极强——Buddy 必须问「是否真的需要 agent」
- 模式表带适用条件 = M5 范本
- ACI（工具设计）应进入决策与风险（M6/M7）
