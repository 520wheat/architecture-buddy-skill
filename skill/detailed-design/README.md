# detailed-design

安装：将本目录放入 `~/.codex/skills/detailed-design`，Reload 后使用 `$detailed-design`。

## 入口

- 直接入口：用户明确要求详细设计。
- 架构 handoff：先接收 architecture-buddy 产出的设计、ADR、边界、目标与待验证事实，再进入本包。

## 输出

- overview
- module documents
- architecture feedback

## 目录

- `references/architecture-handoff.md`：输入契约
- `references/detailed-design-gate.md`：完成门禁

## 边界

本包不生成代码，只产出详细设计契约与审查材料。
