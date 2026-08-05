# MCP Architecture Overview
- 域: D8 Agent / 智能体系统（工具与上下文集成边界）
- 来源: https://modelcontextprotocol.io/docs/concepts/architecture
- 阶段: Phase 4 · 2026-08-05（书单可换项）

## 问题类
如何让 AI 应用（Host）以**标准协议**从多个外部程序获取上下文并调用工具，而不把「如何用 LLM / 如何编排 agent」绑死在协议里。

## 硬约束 / 范围
- MCP **只**规定上下文交换协议；不规定 LLM 用法或 agent 编排
- 参与者：Host（AI 应用）→ 每 Server 一个 Client → Server（提供上下文/工具）
- 协议偏 **stateless**：每请求携带版本与 capability 元数据

## 机制（共性）
1. **双层**：Data layer（JSON-RPC 原语）+ Transport layer（连接/帧/鉴权）
2. **Server 三原语**：Tools（可执行动作）/ Resources（只读上下文）/ Prompts（交互模板）
3. **发现**：`server/discover` + `*/list` 动态枚举
4. Host 多路复用：一 Host 多 Client，每 Client 专连一 Server

## 策略（差异/选项）
| 选项 | 含义 | 代价 |
|------|------|------|
| Stdio transport | 本机进程，低开销 | 单 Client 典型；非远程 |
| Streamable HTTP | 远程多 Client；OAuth 等 | 网络与鉴权复杂度 |
| 原语组合 | 同一 Server 可同时暴露 tool/resource/prompt | 边界不清时易把「数据」做成「有副作用的 tool」 |

## 与 D8 其他样本
| 样本 | 关系 |
|------|------|
| Anthropic Effective Agents | 编排/工作流问题类；MCP 是工具集成边界 |
| LangGraph | 运行时状态/HITL；可经 MCP 取工具 |
| OpenAI Agents SDK | 另一编排策略；同样可接外部工具面 |

## 显式模式名
- Client-Server per connection
- Capability negotiation / discovery
- 控制面式「列能力」与数据面式「call/get」分离（弱类比 ZTA 控制/数据面）

## 决策与负面后果
- 标准协议降低集成成本，但不自动解决权限、审计、毒工具
- Host 必须自建：授权、用户确认、观测——协议不管

## 对写作规范的启示
- Agent 架构笔记应分开写：**编排机制** vs **工具/上下文集成机制**（MCP）
- M1：先问「是否需要标准工具面」，再问「是否需要 agentic 编排」
