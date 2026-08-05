# ADR-0011: 书单锁定；安全与 Agent 均为必做问题域

## Status

Accepted

## Context

深调研书单需在开工前锁定。用户确认：

- 采纳全部 ★ 默认建议为必读
- **安全（D7）** 升为必做，且不能只有单一材料
- 新增 **Agent / 智能体系统（D8）** 作为必做域（近年关键且快速演化）

## Decision

1. `docs/survey/READING-LIST.md` 状态为 **Locked**。
2. 必做问题域为 **D1–D8**；D7 ≥3 篇，D8 ≥3 篇，其余域按计划 ≥2 篇。
3. 模式 corpus 必做仍为 P1–P5；另设 **P9** 从 D8 维护 Agent 模式词汇。
4. Phase 1 开工包以书单中 Locked 一节为准。

## Consequences

- 退出标准提高（见 `03c` E1 修订）。
- Architecture Buddy 的策略词汇将覆盖安全机制与 agent 编排模式，而不只是经典后端系统。
- Phase 1 即启动安全与 agent 开篇，避免后期才补「新域」。
