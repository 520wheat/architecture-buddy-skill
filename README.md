# architecture-buddy-skill

让顶级架构师成为你的架构伙伴，成就一份好的架构设计。

用于设计与开发 **Architecture Buddy** skill 的工作区。

## 目录

| 路径 | 用途 |
|------|------|
| `docs/` | ADR 与设计文档（每个阶段结论落盘） |
| `docs/design/00-architecture-buddy-spec.md` | **汇总规格**（Approved） |
| `docs/adr/` | 架构决策记录 |
| `architecture-buddy/` | 主持 skill（运行时可安装） |
| `architecture-buddy-lens-*/` | 架构立场透镜（圆桌按需选席） |

## 约定

- **女娲（nuwa-skill）仅构建期使用**：蒸馏架构立场的思想与做法；不内嵌进运行时。
- 运行时形态见 `docs/adr/0003-runtime-host-and-lens-skills.md`。
- 透镜库与动态选席见 `docs/adr/0016` / `0017` 与 `docs/design/lens-catalog.md`。
