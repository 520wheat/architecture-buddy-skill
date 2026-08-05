# ADR-0005: 工作区布局与命名

## Status

Accepted

## Context

本项目在独立工作区推进，需与业务仓库（如 SRE-Buddy）解耦；  
阶段结论需要可追溯落盘；skill 交付物需要固定存放位置。

## Decision

- **工作区根目录**：`~/Desktop/skill-create`
- **Skill 名称**：Architecture Buddy
- **目录约定**：

| 路径 | 用途 |
|------|------|
| `docs/` | ADR 与设计文档 |
| `docs/adr/` | 决策记录 |
| `docs/design/` | 分节设计说明 |
| `Architecture Buddy/` | 开发完成的 skill 本体 |

每个 brainstorm / 设计阶段的结论写入 ADR 或 design 文档，不依赖聊天记录作为唯一真相源。

## Consequences

- Agent 默认在本工作区读写；skill 交付物不散落在其他仓库。
- 文档与 skill 分离：docs 解释决策，Architecture Buddy 只放可安装运行的 skill 文件。
