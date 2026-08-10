# detailed-design

安装：将本目录放入 `~/.codex/skills/detailed-design`，Reload 后使用 `$detailed-design`。

## 入口

- 直接入口：
  1. 用户明确要求详细设计。
  2. 读取当前输入中的 scope、边界、质量目标、pending facts、non-goals。
  3. 进入 DD0→DD7。
- 架构 handoff：
  1. 接收 architecture-buddy 产出的设计、ADR、边界、目标与待验证事实。
  2. 校验 `references/architecture-handoff.md`。
  3. 进入 DD0→DD7；若 handoff 仍不明确，先标 `blocked`。

## 输出

- `overview`
- `module documents`
- `architecture feedback`

输出是文档布局，不是代码布局。

## 目录

- `references/architecture-handoff.md`：输入契约
- `references/detailed-design-gate.md`：完成门禁
- `templates/detailed-design-overview.md`：总览模板
- `templates/module-detailed-design.md`：模块模板
- `templates/architecture-feedback.md`：架构反馈模板

## 产物规则

- 先落盘 overview，再按已确认设计单元顺序落盘模块文档。
- 每个 architecture feedback 条目必须可从 overview 追溯。
- 模板只定义详细设计文档契约，不包含实现代码。
- pending facts 默认保留 `待确认`，直到有显式确认或回退。
- rollback 项必须与触发事实和恢复条件同时记录。

## 边界

本包只产出文档：详细设计契约、审查材料和架构反馈；不生成代码。
本包只产出文档，永远不生成代码。
