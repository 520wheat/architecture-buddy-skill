# ADR-0019: deliverable 工作流与校准边界

## Status

Accepted

## Context

Skill 能跑完对话却交不出可读架构设计；用户反馈看不懂成品在说什么。
需要完成门禁，并明确「复现/迁移考试」只用于训练 skill。

## Decision

1. 模式：`draft` | `deliverable`；用户要完整架构设计时默认 `deliverable`。
2. 成品：同一文件双层——层 A 叙事（A1–A8）+ 层 B 机制/策略（B1–B5）；缺一层不算完成。
3. `deliverable` 走 S0–S7；未过 S6 禁止宣称完成。
4. 旧 M1–M9 仅为内部映射，不进用户可见正文权威结构。
5. 复现/迁移校准仅维护者/构建期使用；用户 UX 禁止开考、盲写、打分话术。
6. 金标库与三题 PASS 属后续 Phase；本 ADR 锁定边界不锁定金标正文。

## Consequences

- 重写宿主 SKILL 与模板；扩展静态检查与验收 V7。
- ADR-0018 的 UX/FP 规则继续有效，且适用于 deliverable 各阶段。
