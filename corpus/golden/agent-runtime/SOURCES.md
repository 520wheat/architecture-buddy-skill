# SOURCES — agent-runtime

## 权威公开设计 / 工程文

1. OpenAI Agents SDK（Python）文档  
   https://openai.github.io/openai-agents-python/  
   金标原语/护栏主依据：Agents、工具循环、Handoffs、Guardrails、Sessions、Tracing；相对 Swarm 的生产路径叙事。

2. Anthropic Engineering — Building Effective Agents  
   https://www.anthropic.com/engineering/building-effective-agents  
   金标模式选型主依据：增强型 LLM；工作流 vs Agent；prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer；when/when not；工具接口（ACI）与护栏。

3. LangGraph — Overview / Agent Runtime 设计叙事  
   https://docs.langchain.com/oss/python/langgraph/overview  
   https://www.langchain.com/blog/building-langgraph  
   金标运行时能力依据（择要）：有状态图、checkpoint、HITL 中断恢复、流式/并行、任务队列；短 agent 可不需要框架。

## 本地 survey / 对照摘记

4. `docs/survey/architecture/D8-openai-agents-sdk.md`  
5. `docs/survey/architecture/D8-anthropic-effective-agents.md`  
6. `docs/survey/architecture/D8-langgraph.md`  
   Phase 1/2 调研摘记；本金标由其升格为完整双层 deliverable（问题类语言，非产品拓扑抄写）。

## 使用约定

- 校准可读本 SOURCES；严校可闭卷，仅对照 GOLDEN + RUBRIC。
- 运行时 skill 不得把本文件当用户考试题库展示。
- 金标锚定「LLM + 工具编排运行时」问题类；Codex / Cursor / 具体 IDE agent 产品名仅作问题类示例，禁止把金标写成某一产品模块图。
