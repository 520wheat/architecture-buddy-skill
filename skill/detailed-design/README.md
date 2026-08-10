# detailed-design

安装：将本目录放入 `~/.codex/skills/detailed-design`，Reload 后使用 `$detailed-design`。它也可以由 `architecture-buddy` 在用户同意 handoff 后调用。

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

## 脚本

在本目录中执行：

```bash
python3 scripts/init-design.py --output "<输出目录>" --name "<设计名称>"
python3 scripts/validate-input.py "<架构文件.md>" --adr "<adr-1.md>" --adr "<adr-2.md>"
python3 scripts/validate-deliverable.py "<输出目录>"
```

脚本会初始化 `detailed-design-overview.md`、`modules/`、`architecture-feedback.md`；支持空格和 Unicode 路径。默认拒绝覆盖任一已存在目标，只有用户明确要求时才加 `--force`。
`validate-input.py` 要求正好一个架构 Markdown 文件，`--adr` 至少出现一次且可重复；会检查 `pre-development` 场景、`design-ready` 状态、边界证据、handoff 必填字段、ADR 可读性，以及 pending fact 的默认值 / 原因 / 验证条件 / 回退路径 / 重新打开条件闭环。
`validate-deliverable.py` 只检查一个详细设计输出目录；要求存在 `detailed-design-overview.md` 与至少一个 `modules/*.md`，拒绝 `blocked`，并检查 overview / module 模板证据、跨模块契约、独立 `回退项` 和 pending fact 闭环。

退出码语义：

- `0`：结构校验通过。
- 非 `0`：初始化失败或校验失败；脚本会输出中文错误说明。

边界说明：

- `init-design.py` 只初始化文档工作区，不修改用户项目代码。
- `validate-input.py` 只判断输入契约是否齐全，不推进设计。
- `validate-deliverable.py` 只判断详细设计结构证据是否完整，不判断架构方案或设计质量。

## 产物规则

- 先落盘 overview，再按已确认设计单元顺序落盘模块文档。
- overview 必须包含可列出多条记录的 architecture feedback 索引，至少包含编号、标题、影响模块、状态、反馈文档引用。
- 每个 architecture feedback 条目必须可从 overview 索引追溯。
- 模板只定义详细设计文档契约，不包含实现代码。
- 每个 pending fact 必须显式记录：事实、单阶段默认值、默认原因、验证条件、回退路径、重新打开条件。
- overview 与每个 module 文档都必须保留独立 `回退项` section，且不能被 pending facts 表格替代。
- 每条回退项至少记录：回退触发事实、回退目标、回退动作、恢复条件、关联待确认事实。
- pending facts 默认保留 `待确认`，直到有显式确认、验证完成或按回退路径回退。

## 边界

本包只产出文档：详细设计契约、审查材料和架构反馈；不生成代码。
