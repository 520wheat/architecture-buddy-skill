# skill-create

用于设计与开发 **Architecture Buddy** skill 的工作区。

## 目录

| 路径 | 用途 |
|------|------|
| `docs/` | ADR 与设计文档（每个阶段结论落盘） |
| `docs/adr/` | 架构决策记录 |
| `Architecture Buddy/` | 最终交付的 skill 本体（运行时可安装） |

## 约定

- **女娲（nuwa-skill）仅构建期使用**：蒸馏第一性原理与架构师视角；不内嵌进运行时。
- 运行时形态见 `docs/adr/0003-runtime-host-and-lens-skills.md`。
