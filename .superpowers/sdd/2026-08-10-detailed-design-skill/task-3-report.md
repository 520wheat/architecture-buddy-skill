# Task 3 Report

## Status

done

## Changes

- 新增 7 个 detailed-design Prompt：
  - `skill/detailed-design/prompts/clarify-scope.md`
  - `skill/detailed-design/prompts/decompose-design-units.md`
  - `skill/detailed-design/prompts/design-contracts.md`
  - `skill/detailed-design/prompts/design-data-state.md`
  - `skill/detailed-design/prompts/design-behavior-and-failure.md`
  - `skill/detailed-design/prompts/synthesize-deliverable.md`
  - `skill/detailed-design/prompts/review-deliverable.md`
- 更新 `skill/detailed-design/SKILL.md` 的阶段路由与阶段描述，注册新 Prompt 加载条件。

## Verification

- 通过 brief 指定的文件存在性与章节校验。
- 通过 `rg` 路由引用校验。
- 通过占位符自查与改动范围检查。

## Self-review

- 每个 Prompt 都包含 7 个中文章节、显式输出契约、单一当前问题、确认处理、无隐藏上下文与 architecture rollback 说明。
- `DD6` 与 `DD7` 共享 `review-deliverable.md`，用于满足 7 个 Prompt 文件的约束并保留最终门禁。

## Notes

- 未修改 `architecture-buddy` 相关文件。
