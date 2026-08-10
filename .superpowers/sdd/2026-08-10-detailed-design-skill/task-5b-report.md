# Task 5b Report

日期：2026-08-10
工作区：`/Users/apple/Desktop/skill-create/.worktrees/detailed-design-skill`

## 完成内容

- 新增 `skill/detailed-design/scripts/validate-input.py`
- 新增 `skill/detailed-design/scripts/validate-deliverable.py`
- 新增 `skill/detailed-design/scripts/validator_helpers.py`
- 新增 `skill/detailed-design/scripts/test_validate_input.py`
- 新增 `skill/detailed-design/scripts/test_validate_deliverable.py`
- 更新 `skill/detailed-design/README.md`
- 更新 `skill/detailed-design/SKILL.md`

## 行为摘要

### validate-input.py

- 接收一个架构 Markdown 文件和至少一个可重复 `--adr` 参数。
- 拒绝缺失或不可读的架构文件 / ADR 文件。
- 只接受 `pre-development` 场景。
- 只接受 `design-ready` 状态；若出现 `complete`，明确提示只能使用 `draft` / `blocked` / `design-ready`。
- 要求存在架构边界证据。
- 若检测到 handoff 文件或 handoff 契约正文，则检查 `architecture file`、`ADR paths`、`pre-development`、`design-ready`、`scope`、`confirmed boundaries`、`quality targets`、`pending facts`、`non-goals`。
- 检查 pending fact 表格中的 `事实`、`单阶段默认值`、`默认原因`、`验证条件`、`回退路径`、`重新打开条件` 是否完整。
- 失败输出统一以 `输入校验失败：` 开头；成功返回 0 并输出中文说明。

### validate-deliverable.py

- 接收一个详细设计输出目录。
- 要求存在 `detailed-design-overview.md`。
- 要求存在 `modules/` 且至少有一个模块 Markdown 文档。
- 拒绝 overview 状态为 `blocked`；若出现 `complete` 也会拒绝。
- 检查 overview 的核心 section、设计单元索引、架构反馈索引、跨模块契约、待确认事实表、独立回退项表。
- 检查每个模块文档的核心 section、待确认事实表、独立回退项表。
- 失败输出统一以 `详细设计校验失败：` 开头；成功返回 0 并说明“只检查结构证据，不判断架构质量”。

## 测试策略

采用 TDD：

1. 先添加 `test_validate_input.py` 和 `test_validate_deliverable.py`。
2. 在脚本不存在时运行测试，确认红灯。
3. 实现最小校验逻辑。
4. 修正解析细节问题后重复运行 focused tests。

## 覆盖的回归场景

### 输入校验

- 有效 `design-ready`
- 非 `pre-development`
- 非 `design-ready`
- 缺架构边界
- 缺少 `--adr`
- ADR 不可读
- handoff 缺必填字段
- pending fact 缺默认值 / 原因 / 验证条件 / 回退路径 / 重新打开条件

### 交付物校验

- 有效 overview + module
- 缺 overview
- 缺 module
- `blocked`
- 缺跨模块契约
- 缺独立回退项有效证据
- pending fact 闭环不完整

## 验证命令

```bash
python3 -m unittest skill/detailed-design/scripts/test_init_design.py skill/detailed-design/scripts/test_validate_input.py skill/detailed-design/scripts/test_validate_deliverable.py
python3 -m py_compile skill/detailed-design/scripts/*.py
```

## 验证结果

- `unittest`：19 tests，全部通过。
- `py_compile`：全部通过。

## 文档更新

- `README.md` 增加了三个脚本的命令示例、`--adr` 重复参数契约、退出码语义、覆盖行为和“不判断架构质量”的边界说明。
- `SKILL.md` 增加了两个 validator 的 CLI 契约与校验边界。

## 约束与边界

- 仅使用 Python 标准库。
- 未修改 `architecture-buddy` 相关文件。
- 未修改模板内容。
- 未对用户项目做任何代码生成或外部网络访问。
