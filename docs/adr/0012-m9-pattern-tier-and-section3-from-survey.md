# ADR-0012: 深调研结论固化为 M1–M9，并据此回写 §3

## Status

Accepted

## Context

深调研完成 E1（D1–D8 样本下限）与 E2（P1–P5 + P9）。活表整理为 v1.0。  
首轮 §3 草案需按调研修订：尤其是约束中的信任/一致性假设，以及模式层级（M9）。

## Decision

1. 笔记锚点采用 **M1–M9**（见 `docs/survey/living/mechanisms.md` v1.0）。  
2. **M9** 明确模式词汇层级：架构 / 企业 / 集成 / 并发分布式 / Agent / 细粒度(GoF)。  
3. `docs/design/03-notes-and-templates.md` 升级为 **Proposed（待用户批准）**，内容以活表 v1.0 为准。  
4. 调研知识库继续留在 `docs/survey/`，供构建 Architecture Buddy 时引用；运行时 skill 保持开箱即用、不内嵌女娲。

## Consequences

- §3 批准后即可继续设计 §4（圆桌接口）并进入实现计划。  
- 后续样本只增量更新活表，不轻易改 M 编号。
